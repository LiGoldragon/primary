//! Bounded, one-shot Codex transcript projection for the exact approved seat.
//! It intentionally omits user-role records: role alone never proves psyche.

use std::{
    collections::HashSet,
    fs::File,
    io::{BufRead, BufReader, Read},
};

use serde_json::Value;
use time::{format_description::well_known::Rfc3339, OffsetDateTime};

use crate::{
    correlation::MarkerSession,
    known_codex::{EXACT_ROLLOUT, FLOW_ID, NATIVE_UUID},
};

const MAX_READ_BYTES: usize = 4 * 1024 * 1024;
const MAX_LINE_BYTES: usize = 256 * 1024;
const MAX_CANDIDATES: usize = 500;
const MAX_COMPLETED_TURNS: usize = 2048;
const MAX_ENTRY_TEXT_BYTES: usize = 64 * 1024;

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum HistoryStatus {
    Partial,
    Unavailable,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct FinalEntry {
    pub global_id: String,
    pub source_ordinal: u64,
    pub occurred_at_nanos: i64,
    pub text: String,
    pub attributed_actor: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct HistoryPage {
    pub status: HistoryStatus,
    pub entries: Vec<FinalEntry>,
    pub scanned_bytes: usize,
    pub truncated: bool,
}

struct Candidate {
    turn_id: String,
    entry: FinalEntry,
}

/// The caller must pass the MarkerSession returned by exact correlation. One
/// request scans only the initial bounded page; it neither tails nor polls.
pub fn read_initial_page(session: &MarkerSession) -> HistoryPage {
    let unavailable = || HistoryPage {
        status: HistoryStatus::Unavailable,
        entries: Vec::new(),
        scanned_bytes: 0,
        truncated: false,
    };
    if session.flow_id != FLOW_ID
        || session.native_session_id != NATIVE_UUID
        || session.exact_transcripts.len() != 1
        || session.exact_transcripts[0] != std::path::Path::new(EXACT_ROLLOUT)
    {
        return unavailable();
    }
    let path = &session.exact_transcripts[0];
    let Ok(file) = File::open(path) else { return unavailable(); };
    let Ok(size) = file.metadata().map(|metadata| metadata.len()) else { return unavailable(); };
    let mut reader = BufReader::new(file);
    let mut candidates = Vec::new();
    let mut completed = HashSet::new();
    let mut seen_items = HashSet::new();
    let mut scanned = 0;
    let mut ordinal = 0_u64;
    let mut truncated = false;

    while scanned < MAX_READ_BYTES {
        let permitted = (MAX_READ_BYTES - scanned).min(MAX_LINE_BYTES + 1);
        let mut line = String::new();
        let Ok(read) = reader.by_ref().take(permitted as u64).read_line(&mut line) else {
            truncated = true;
            break;
        };
        if read == 0 { break; }
        scanned += read;
        ordinal += 1;
        if !line.ends_with('\n') && scanned < size as usize {
            truncated = true;
            break;
        }
        let Ok(record) = serde_json::from_str::<Value>(&line) else {
            truncated = true;
            continue;
        };
        if record.get("type").and_then(Value::as_str) == Some("event_msg")
            && record.pointer("/payload/type").and_then(Value::as_str) == Some("task_complete")
        {
            if let Some(turn_id) = record.pointer("/payload/turn_id").and_then(Value::as_str) {
                if completed.len() == MAX_COMPLETED_TURNS { truncated = true; break; }
                completed.insert(turn_id.to_owned());
            }
            continue;
        }
        if record.get("type").and_then(Value::as_str) != Some("response_item")
            || record.pointer("/payload/type").and_then(Value::as_str) != Some("message")
            || record.pointer("/payload/role").and_then(Value::as_str) != Some("assistant")
            || record.pointer("/payload/phase").and_then(Value::as_str) != Some("final_answer")
        {
            continue;
        }
        let Some(turn_id) = record.pointer("/payload/internal_chat_message_metadata_passthrough/turn_id").and_then(Value::as_str) else {
            truncated = true;
            continue;
        };
        let Some(item_id) = record.pointer("/payload/id").and_then(Value::as_str) else {
            truncated = true;
            continue;
        };
        if !seen_items.insert(item_id.to_owned()) { continue; }
        let Some(stamp) = record.get("timestamp").and_then(Value::as_str)
            .and_then(|value| OffsetDateTime::parse(value, &Rfc3339).ok())
        else { truncated = true; continue; };
        let Ok(stamp_nanos) = i64::try_from(stamp.unix_timestamp_nanos()) else {
            truncated = true;
            continue;
        };
        let Some(blocks) = record.pointer("/payload/content").and_then(Value::as_array) else {
            truncated = true;
            continue;
        };
        for (block_index, block) in blocks.iter().enumerate() {
            if block.get("type").and_then(Value::as_str) != Some("output_text") { continue; }
            let Some(text) = block.get("text").and_then(Value::as_str) else { truncated = true; continue; };
            if text.is_empty() || text.len() > MAX_ENTRY_TEXT_BYTES { truncated = true; continue; }
            if candidates.len() == MAX_CANDIDATES { truncated = true; break; }
            candidates.push(Candidate {
                turn_id: turn_id.to_owned(),
                entry: FinalEntry {
                    global_id: format!("codex:{NATIVE_UUID}:{turn_id}:{item_id}:{block_index}"),
                    source_ordinal: ordinal,
                    occurred_at_nanos: stamp_nanos,
                    text: text.to_owned(),
                    attributed_actor: String::from("MindSol POC"),
                },
            });
        }
        if candidates.len() == MAX_CANDIDATES { truncated = true; break; }
    }
    let entries = candidates.into_iter()
        .filter(|candidate| completed.contains(&candidate.turn_id))
        .map(|candidate| candidate.entry)
        .collect();
    HistoryPage {
        // User input, compaction, tool, and uncertain turns are omitted, so
        // even a fully scanned file is never presented as complete history.
        status: HistoryStatus::Partial,
        entries,
        scanned_bytes: scanned,
        truncated: truncated || (scanned as u64) < size,
    }
}
