//! One explicitly approved live Codex seat. No flow-directory or rollout glob.
//! A restarted pane, new rollout, or missing marker is unavailable until its
//! exact native mapping is observed and reviewed again.

use std::{
    fs::{self, File},
    io::{BufRead, BufReader},
    os::unix::fs::PermissionsExt,
    path::{Path, PathBuf},
};

use crate::correlation::{FlowBinding, HarnessKind, MarkerBackedSource, MarkerSession};

pub const FLOW_ID: &str = "effa1b";
pub const NATIVE_UUID: &str = "01a0b68e-e703-7d21-b908-7a7effa1bf8b";
const MARKER_IDENTITY: &str = "01a0b68ee7037d21b9087a7effa1bf8b";
const PANE_ID: &str = "wC:p2";
const TERMINAL_ID: &str = "term_65bc91cf241bf2b";
const MARKER_PATH: &str = "/home/li/primary/flows/.effa1b.flow-id";
pub const EXACT_ROLLOUT: &str = "/home/li/.codex/sessions/2026/09/18/rollout-2026-09-18T16-06-53-01a0b68e-e703-7d21-b908-7a7effa1bf8b.jsonl";

pub fn approved_binding(process_id: u32) -> FlowBinding {
    FlowBinding {
        flow_id: FLOW_ID.into(),
        pane_id: PANE_ID.into(),
        terminal_id: TERMINAL_ID.into(),
        process_id,
        native_session_id: NATIVE_UUID.into(),
        harness: HarnessKind::Codex,
    }
}

/// Construct only from the PID returned for the exact Herdr pane's foreground
/// Codex process. The process file descriptors must still hold the approved
/// exact rollout; an arbitrary caller path never enters this type.
pub struct KnownCodexMarker {
    pub process_id: u32,
}

impl MarkerBackedSource for KnownCodexMarker {
    fn read_exact_session(&self, flow_id: &str) -> Option<MarkerSession> {
        if flow_id != FLOW_ID || !marker_matches(Path::new(MARKER_PATH)) {
            return None;
        }
        let rollout = Path::new(EXACT_ROLLOUT);
        if !process_holds_exact_rollout(self.process_id, rollout)
            || !rollout_session_meta_matches(rollout)
        {
            return None;
        }
        Some(MarkerSession {
            flow_id: FLOW_ID.into(),
            pane_id: PANE_ID.into(),
            terminal_id: TERMINAL_ID.into(),
            process_id: self.process_id,
            native_session_id: NATIVE_UUID.into(),
            harness: HarnessKind::Codex,
            exact_transcripts: vec![PathBuf::from(EXACT_ROLLOUT)],
        })
    }
}

fn marker_matches(path: &Path) -> bool {
    let Ok(metadata) = fs::symlink_metadata(path) else { return false; };
    if !metadata.is_file() || metadata.file_type().is_symlink()
        || metadata.permissions().mode() & 0o777 != 0o600
    {
        return false;
    }
    let Ok(contents) = fs::read_to_string(path) else { return false; };
    marker_text_matches(&contents)
}

fn marker_text_matches(contents: &str) -> bool {
    contents == format!(
        "version=1\nharness=codex\nidentity={MARKER_IDENTITY}\nalias={FLOW_ID}\n"
    )
}

fn process_holds_exact_rollout(process_id: u32, rollout: &Path) -> bool {
    let Ok(descriptors) = fs::read_dir(format!("/proc/{process_id}/fd")) else { return false; };
    descriptors.filter_map(Result::ok).any(|descriptor| {
        fs::read_link(descriptor.path()).is_ok_and(|target| target == rollout)
    })
}

fn rollout_session_meta_matches(path: &Path) -> bool {
    let Ok(file) = File::open(path) else { return false; };
    let Some(Ok(first_line)) = BufReader::new(file).lines().next() else { return false; };
    let Ok(value) = serde_json::from_str::<serde_json::Value>(&first_line) else { return false; };
    value.get("type").and_then(serde_json::Value::as_str) == Some("session_meta")
        && value.pointer("/payload/id").and_then(serde_json::Value::as_str) == Some(NATIVE_UUID)
}

#[cfg(test)]
mod tests {
    use super::{marker_text_matches, FLOW_ID};

    #[test]
    fn marker_requires_full_identity_and_exact_alias() {
        assert!(marker_text_matches(&format!("version=1\nharness=codex\nidentity=01a0b68ee7037d21b9087a7effa1bf8b\nalias={FLOW_ID}\n")));
        assert!(!marker_text_matches("version=1\nharness=codex\nidentity=wrong\nalias=effa1b\n"));
    }
}
