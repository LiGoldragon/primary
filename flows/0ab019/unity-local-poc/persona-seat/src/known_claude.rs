//! One reviewed Claude seat. The full UUID is checked against the marker,
//! live native process task descriptor, and exact transcript sessionId.

use std::{
    fs::{self, File}, io::{BufRead, BufReader}, os::unix::fs::PermissionsExt,
    path::{Path, PathBuf},
};

use crate::correlation::{FlowBinding, HarnessKind, MarkerBackedSource, MarkerSession};

pub const FLOW_ID: &str = "c8d79f";
pub const NATIVE_UUID: &str = "c8d79f66-5ea6-4034-94e4-b685bd359393";
const MARKER_ID: &str = "c8d79f665ea6403494e4b685bd359393";
const PANE: &str = "w4:p7";
const TERMINAL: &str = "term_65bc83deb7ba928";
const MARKER: &str = "/home/li/primary/flows/.c8d79f.flow-id";
pub const EXACT_TRANSCRIPT: &str = "/home/li/.claude/projects/-home-li-primary/c8d79f66-5ea6-4034-94e4-b685bd359393.jsonl";
const EXACT_TASKS: &str = "/tmp/claude-1001/-home-li-primary/c8d79f66-5ea6-4034-94e4-b685bd359393/tasks";

pub fn approved_binding(process_id: u32) -> FlowBinding {
    FlowBinding {
        flow_id: FLOW_ID.into(), pane_id: PANE.into(), terminal_id: TERMINAL.into(),
        process_id, native_session_id: NATIVE_UUID.into(), harness: HarnessKind::Claude,
    }
}

pub struct KnownClaudeMarker { pub process_id: u32 }

fn marker_matches() -> bool {
    let path = Path::new(MARKER);
    let Ok(meta) = fs::symlink_metadata(path) else { return false; };
    if !meta.is_file() || meta.file_type().is_symlink()
        || meta.permissions().mode() & 0o777 != 0o600 { return false; }
    fs::read_to_string(path).is_ok_and(|value| value == format!(
        "version=1\nharness=claude\nidentity={MARKER_ID}\nalias={FLOW_ID}\n"))
}

fn process_holds_exact_tasks(pid: u32) -> bool {
    let Ok(descriptors) = fs::read_dir(format!("/proc/{pid}/fd")) else { return false; };
    descriptors.filter_map(Result::ok).any(|entry| fs::read_link(entry.path())
        .is_ok_and(|target| target == Path::new(EXACT_TASKS)))
}

fn transcript_matches() -> bool {
    let path = Path::new(EXACT_TRANSCRIPT);
    let Ok(meta) = fs::symlink_metadata(path) else { return false; };
    if !meta.is_file() || meta.file_type().is_symlink() { return false; }
    let Ok(file) = File::open(path) else { return false; };
    let Some(Ok(first)) = BufReader::new(file).lines().next() else { return false; };
    serde_json::from_str::<serde_json::Value>(&first).ok()
        .and_then(|record| record.get("sessionId").and_then(serde_json::Value::as_str)
            .map(str::to_owned)).as_deref() == Some(NATIVE_UUID)
}

impl MarkerBackedSource for KnownClaudeMarker {
    fn read_exact_session(&self, flow_id: &str) -> Option<MarkerSession> {
        if flow_id != FLOW_ID || !marker_matches()
            || !process_holds_exact_tasks(self.process_id) || !transcript_matches()
        { return None; }
        Some(MarkerSession {
            flow_id: FLOW_ID.into(), pane_id: PANE.into(), terminal_id: TERMINAL.into(),
            process_id: self.process_id, native_session_id: NATIVE_UUID.into(),
            harness: HarnessKind::Claude,
            exact_transcripts: vec![PathBuf::from(EXACT_TRANSCRIPT)],
        })
    }
}
