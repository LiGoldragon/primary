//! Persona-owned, exact read of the one approved Herdr pane.

use std::{path::Path, process::Command};

use serde_json::Value;

use crate::{
    correlation::{HarnessKind, LivePane},
    known_codex::NATIVE_UUID,
};

const PANE_ID: &str = "wC:p2";
const TERMINAL_ID: &str = "term_65bc91cf241bf2b";

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ObservedPane {
    pub pane: LivePane,
    pub state: String,
}

fn herdr_json(arguments: &[&str]) -> Option<Value> {
    let output = Command::new("herdr").args(arguments).output().ok()?;
    if !output.status.success() || output.stdout.len() > 64 * 1024 {
        return None;
    }
    serde_json::from_slice(&output.stdout).ok()
}

pub fn read_known_pane() -> Option<ObservedPane> {
    let pane = herdr_json(&["pane", "get", PANE_ID])?;
    if pane.pointer("/result/pane/pane_id")?.as_str()? != PANE_ID
        || pane.pointer("/result/pane/terminal_id")?.as_str()? != TERMINAL_ID
        || pane.pointer("/result/pane/agent")?.as_str()? != "codex"
    {
        return None;
    }
    let state = pane.pointer("/result/pane/agent_status")?.as_str()?.to_owned();
    let process = herdr_json(&["pane", "process-info", "--pane", PANE_ID])?;
    if process.pointer("/result/process_info/pane_id")?.as_str()? != PANE_ID {
        return None;
    }
    let processes = process.pointer("/result/process_info/foreground_processes")?.as_array()?;
    if processes.len() != 1 { return None; }
    let argv = processes[0].get("argv")?.as_array()?;
    let program = argv.first()?.as_str()?;
    if Path::new(program).file_name()?.to_str()? != "codex" { return None; }
    let process_id = u32::try_from(processes[0].get("pid")?.as_u64()?).ok()?;
    Some(ObservedPane {
        pane: LivePane {
            pane_id: PANE_ID.into(),
            terminal_id: TERMINAL_ID.into(),
            process_id,
            // This is an expectation only; known_codex independently checks
            // the marker, open process FD, and rollout session_meta.
            native_session_id: NATIVE_UUID.into(),
            harness: HarnessKind::Codex,
        },
        state,
    })
}
