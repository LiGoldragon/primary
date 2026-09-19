//! Exact-session, on-demand transcript pages. One request seeks at most one
//! four-MiB window; no whole-file RAM load, tail, polling, or path discovery.

use std::{
    collections::{HashSet, VecDeque},
    fs::{self, File},
    io::{BufRead, BufReader, Read, Seek, SeekFrom},
    os::unix::fs::MetadataExt,
    path::Path,
};

use serde_json::Value;
use signal_mentci::ConversationCursor;
use time::{format_description::well_known::Rfc3339, OffsetDateTime};

const MAX_WINDOW_BYTES: u64 = 4 * 1024 * 1024;
const MAX_LINE_BYTES: u64 = 256 * 1024;
const MAX_ENTRIES: usize = 100;
const MAX_RECORDS: usize = 20_000;
const MAX_ENTRY_TEXT_BYTES: usize = 64 * 1024;
const MAX_OUTPUT_TEXT_BYTES: usize = 128 * 1024;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Format { Codex, Claude }

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum HistoryError { Unavailable, SnapshotChanged, ResourceLimit }

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct HistoryEntry {
    pub global_id: String,
    /// Absolute source line-start byte offset, a monotone global ordinal.
    pub source_ordinal: u64,
    pub occurred_at_nanos: i64,
    pub text: String,
    pub actor: Option<String>,
    pub user_input: bool,
}

#[derive(Clone, Debug, PartialEq)]
pub struct HistoryPage {
    pub entries: Vec<HistoryEntry>,
    pub snapshot_bytes: u64,
    pub current_bytes: u64,
    pub window_start: u64,
    pub window_end: u64,
    pub older_cursor: Option<ConversationCursor>,
    pub incomplete: bool,
}

fn number(value: u64) -> Result<i64, HistoryError> {
    i64::try_from(value).map_err(|_| HistoryError::ResourceLimit)
}

fn make_cursor(uuid: &str, meta: &fs::Metadata, snapshot: u64, before: u64)
    -> Result<Option<ConversationCursor>, HistoryError>
{
    if before == 0 { return Ok(None); }
    Ok(Some(ConversationCursor {
        native_session_identifier: uuid.into(),
        file_device: number(meta.dev())?,
        file_inode: number(meta.ino())?,
        snapshot_bytes: number(snapshot)?,
        before_byte: number(before)?,
    }))
}

fn stamp(record: &Value) -> Result<i64, ()> {
    let value = record.get("timestamp").and_then(Value::as_str).ok_or(())?;
    let parsed = OffsetDateTime::parse(value, &Rfc3339).map_err(|_| ())?;
    i64::try_from(parsed.unix_timestamp_nanos()).map_err(|_| ())
}

fn codex(record: &Value, uuid: &str, offset: u64,
    seen: &mut HashSet<String>, user_turns: &mut HashSet<String>)
    -> Result<Vec<HistoryEntry>, ()>
{
    if record.get("type").and_then(Value::as_str) != Some("response_item")
        || record.pointer("/payload/type").and_then(Value::as_str) != Some("message")
    { return Ok(Vec::new()); }
    let role = record.pointer("/payload/role").and_then(Value::as_str);
    let user = role == Some("user");
    let final_answer = role == Some("assistant")
        && record.pointer("/payload/phase").and_then(Value::as_str) == Some("final_answer");
    let user_kinds = record.pointer("/payload/internal_chat_message_metadata_passthrough/content_item_kinds")
        .and_then(Value::as_array).is_some_and(|kinds| kinds.len() == 1
            && kinds[0].as_str() == Some("user.text"));
    if !(final_answer || (user && user_kinds)) { return Ok(Vec::new()); }
    let turn = record.pointer("/payload/internal_chat_message_metadata_passthrough/turn_id")
        .and_then(Value::as_str).ok_or(())?;
    let item = record.pointer("/payload/id").and_then(Value::as_str).ok_or(())?;
    if !seen.insert(item.to_owned()) || (user && !user_turns.insert(turn.to_owned())) {
        return Ok(Vec::new());
    }
    let when = stamp(record)?;
    let blocks = record.pointer("/payload/content").and_then(Value::as_array).ok_or(())?;
    let mut entries = Vec::new();
    for (index, block) in blocks.iter().enumerate() {
        let kind = if user { "input_text" } else { "output_text" };
        if block.get("type").and_then(Value::as_str) != Some(kind) { continue; }
        let text = block.get("text").and_then(Value::as_str).ok_or(())?;
        if text.is_empty() { continue; }
        if text.len() > MAX_ENTRY_TEXT_BYTES { return Err(()); }
        entries.push(HistoryEntry {
            global_id: format!("codex:{uuid}:{turn}:{item}:{index}"),
            source_ordinal: offset, occurred_at_nanos: when, text: text.into(),
            actor: (!user).then(|| String::from("MindSol POC")), user_input: user,
        });
    }
    Ok(entries)
}

fn claude(record: &Value, uuid: &str, offset: u64, seen: &mut HashSet<String>)
    -> Result<Vec<HistoryEntry>, ()>
{
    if record.get("sessionId").and_then(Value::as_str) != Some(uuid)
        || record.get("isMeta").and_then(Value::as_bool) == Some(true)
        || record.get("isSidechain").and_then(Value::as_bool) == Some(true)
    { return Ok(Vec::new()); }
    let kind = record.get("type").and_then(Value::as_str);
    let user = kind == Some("user");
    let final_answer = kind == Some("assistant")
        && record.pointer("/message/stop_reason").and_then(Value::as_str) == Some("end_turn");
    if !user && !final_answer { return Ok(Vec::new()); }
    let id = if user { record.get("uuid") } else { record.pointer("/message/id") }
        .and_then(Value::as_str).ok_or(())?;
    if !seen.insert(format!("{kind:?}:{id}")) { return Ok(Vec::new()); }
    let when = stamp(record)?;
    let content = record.pointer("/message/content").ok_or(())?;
    let texts: Vec<&str> = if user {
        match content.as_str() {
            Some(text) => vec![text],
            None => content.as_array().map(|blocks| blocks.iter()
                .filter(|block| block.get("type").and_then(Value::as_str) == Some("text"))
                .filter_map(|block| block.get("text").and_then(Value::as_str)).collect())
                .unwrap_or_default(),
        }
    } else {
        content.as_array().ok_or(())?.iter()
            .filter(|block| block.get("type").and_then(Value::as_str) == Some("text"))
            .filter_map(|block| block.get("text").and_then(Value::as_str)).collect()
    };
    let mut entries = Vec::new();
    for (index, text) in texts.into_iter().enumerate() {
        if text.is_empty() { continue; }
        if text.len() > MAX_ENTRY_TEXT_BYTES { return Err(()); }
        entries.push(HistoryEntry {
            global_id: format!("claude:{uuid}:{id}:{index}"), source_ordinal: offset,
            occurred_at_nanos: when, text: text.into(),
            actor: (!user).then(|| String::from("Fable POC")), user_input: user,
        });
    }
    Ok(entries)
}

pub fn read_page(path: &Path, uuid: &str, format: Format, prior: Option<ConversationCursor>)
    -> Result<HistoryPage, HistoryError>
{
    let meta = fs::symlink_metadata(path).map_err(|_| HistoryError::Unavailable)?;
    if !meta.file_type().is_file() || meta.file_type().is_symlink() {
        return Err(HistoryError::Unavailable);
    }
    let current = meta.len();
    let (snapshot, end) = match prior {
        None => (current, current),
        Some(cursor) => {
            if cursor.native_session_identifier != uuid
                || cursor.file_device != number(meta.dev())?
                || cursor.file_inode != number(meta.ino())?
                || cursor.snapshot_bytes < 0 || cursor.before_byte <= 0
                || cursor.before_byte > cursor.snapshot_bytes
                || current < cursor.snapshot_bytes as u64
            { return Err(HistoryError::SnapshotChanged); }
            (cursor.snapshot_bytes as u64, cursor.before_byte as u64)
        }
    };
    let raw_start = end.saturating_sub(MAX_WINDOW_BYTES);
    let file = File::open(path).map_err(|_| HistoryError::Unavailable)?;
    let mut reader = BufReader::new(file);
    reader.seek(SeekFrom::Start(raw_start)).map_err(|_| HistoryError::Unavailable)?;
    let mut position = raw_start;
    if raw_start != 0 {
        let mut prefix = Vec::new();
        let count = reader.by_ref().take((end - position).min(MAX_LINE_BYTES + 1))
            .read_until(b'\n', &mut prefix).map_err(|_| HistoryError::Unavailable)?;
        if prefix.last() != Some(&b'\n') { return Err(HistoryError::ResourceLimit); }
        position += count as u64;
    }
    let aligned_start = position;
    let mut entries = VecDeque::new();
    let mut output_bytes = 0_usize;
    let mut seen = HashSet::new();
    let mut user_turns = HashSet::new();
    let mut incomplete = false;
    let mut retained_start = aligned_start;
    let mut records = 0_usize;
    while position < end {
        records += 1;
        if records > MAX_RECORDS { return Err(HistoryError::ResourceLimit); }
        let line_start = position;
        let mut line = Vec::new();
        let count = reader.by_ref().take((end - position).min(MAX_LINE_BYTES + 1))
            .read_until(b'\n', &mut line).map_err(|_| HistoryError::Unavailable)?;
        if count == 0 { incomplete = true; break; }
        position += count as u64;
        if line.last() != Some(&b'\n') { incomplete = true; break; }
        let Ok(record) = serde_json::from_slice::<Value>(&line) else { incomplete = true; continue; };
        let projected = match format {
            Format::Codex => codex(&record, uuid, line_start, &mut seen, &mut user_turns),
            Format::Claude => claude(&record, uuid, line_start, &mut seen),
        };
        match projected {
            Ok(projected) => for entry in projected {
                output_bytes += entry.text.len();
                entries.push_back(entry);
                while entries.len() > MAX_ENTRIES || output_bytes > MAX_OUTPUT_TEXT_BYTES {
                    let removed: HistoryEntry = entries.pop_front().ok_or(HistoryError::ResourceLimit)?;
                    output_bytes -= removed.text.len();
                    retained_start = entries.front().map_or(line_start, |first| first.source_ordinal);
                }
            },
            Err(()) => incomplete = true,
        }
    }
    let start = retained_start.max(aligned_start);
    Ok(HistoryPage {
        entries: entries.into_iter().collect(), snapshot_bytes: snapshot,
        current_bytes: current, window_start: start, window_end: end,
        older_cursor: make_cursor(uuid, &meta, snapshot, start)?, incomplete,
    })
}

#[cfg(test)]
mod tests {
    use std::{fs::{self, OpenOptions}, io::Write};

    use serde_json::json;

    use super::{read_page, Format, HistoryError, MAX_WINDOW_BYTES};

    fn fixture(name: &str) -> std::path::PathBuf {
        std::env::temp_dir().join(format!("unity-history-{name}-{}", std::process::id()))
    }

    #[test]
    fn codex_pages_cover_fixed_snapshot_and_report_append() {
        let path = fixture("codex");
        let uuid = "11111111-2222-3333-4444-555555555555";
        let mut file = OpenOptions::new().write(true).create_new(true).open(&path).expect("fixture");
        let user = json!({"type":"response_item","timestamp":"2026-09-19T00:00:00Z",
            "payload":{"type":"message","role":"user","id":"user-1",
            "internal_chat_message_metadata_passthrough":{"turn_id":"turn-1","content_item_kinds":["user.text"]},
            "content":[{"type":"input_text","text":"synthetic unknown origin"}]}});
        writeln!(file, "{user}").expect("user");
        let filler = "x".repeat(4096);
        while file.metadata().expect("metadata").len() < MAX_WINDOW_BYTES {
            writeln!(file, "{}", json!({"type":"event_msg","payload":{"type":"progress","synthetic":filler}})).expect("filler");
        }
        let final_answer = json!({"type":"response_item","timestamp":"2026-09-19T00:00:01Z",
            "payload":{"type":"message","role":"assistant","phase":"final_answer","id":"final-1",
            "internal_chat_message_metadata_passthrough":{"turn_id":"turn-1"},
            "content":[{"type":"output_text","text":"synthetic final"}]}});
        writeln!(file, "{final_answer}").expect("final");
        drop(file);
        let newest = read_page(&path, uuid, Format::Codex, None).expect("latest");
        assert_eq!(newest.entries.len(), 1);
        assert!(newest.older_cursor.is_some());
        let cursor = newest.older_cursor.clone();
        let mut append = OpenOptions::new().append(true).open(&path).expect("append");
        writeln!(append, "{}", json!({"type":"event_msg"})).expect("append line");
        drop(append);
        let older = read_page(&path, uuid, Format::Codex, cursor).expect("older");
        assert_eq!(older.entries.len(), 1);
        assert!(older.entries[0].user_input);
        assert!(older.older_cursor.is_none());
        assert!(older.current_bytes > older.snapshot_bytes);
        fs::remove_file(path).expect("cleanup");
    }

    #[test]
    fn changed_snapshot_cursor_is_refused() {
        let path = fixture("cursor");
        fs::write(&path, b"{\"type\":\"system\"}\n").expect("fixture");
        let first = read_page(&path, "uuid", Format::Claude, None).expect("first");
        assert!(first.older_cursor.is_none());
        let wrong = signal_mentci::ConversationCursor {
            native_session_identifier: "other".into(), file_device: 1, file_inode: 1,
            snapshot_bytes: 10, before_byte: 1,
        };
        assert_eq!(read_page(&path, "uuid", Format::Claude, Some(wrong)), Err(HistoryError::SnapshotChanged));
        fs::remove_file(path).expect("cleanup");
    }

    #[test]
    fn claude_end_turn_only_and_user_is_not_living_proof() {
        let path = fixture("claude");
        let uuid = "11111111-2222-3333-4444-555555555555";
        let rows = [
            json!({"type":"user","sessionId":uuid,"uuid":"u1","timestamp":"2026-09-19T00:00:00Z","message":{"content":"synthetic input"}}),
            json!({"type":"assistant","sessionId":uuid,"uuid":"a1","timestamp":"2026-09-19T00:00:01Z","message":{"id":"m1","stop_reason":"tool_use","content":[{"type":"text","text":"not final"}]}}),
            json!({"type":"assistant","sessionId":uuid,"uuid":"a2","timestamp":"2026-09-19T00:00:02Z","message":{"id":"m2","stop_reason":"end_turn","content":[{"type":"text","text":"synthetic final"}]}}),
        ];
        let mut file = OpenOptions::new().write(true).create_new(true).open(&path).expect("fixture");
        for row in rows { writeln!(file, "{row}").expect("row"); }
        drop(file);
        let page = read_page(&path, uuid, Format::Claude, None).expect("page");
        assert_eq!(page.entries.len(), 2);
        assert!(page.entries[0].user_input);
        assert!(!page.entries[1].user_input);
        assert!(page.older_cursor.is_none());
        fs::remove_file(path).expect("cleanup");
    }
}
