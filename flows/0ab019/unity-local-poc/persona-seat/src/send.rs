//! One-shot controlled POC submission. Persona freshly rebinds the exact seat
//! before invoking the fixed, source-packaged messenger bridge with three
//! arguments. Bridge exit alone is not a target-side presentation witness.

use std::{
    io::Read,
    process::{Command, Stdio},
    thread,
    time::{Duration, Instant, SystemTime, UNIX_EPOCH},
};

use signal_mentci::{
    Provenance, ReceiptGrade, Response, SubmissionDisposition,
    SubmissionReason, SubmissionReceipt,
};

use crate::{
    correlation::ExactBindings,
    known_claude,
    known_codex,
    ledger::{AttemptLedger, Begin},
    live_herdr::{read_claude_pane, read_known_pane},
    protocol::{AcceptedIngress, PersonaApply},
};

const BRIDGE: &str = "/nix/store/qsc0gqcnlwazyanz4kf4lk5xb9anri89-primary-messaging-runtime/bin/msg-psyche-poc";
const BRIDGE_DEADLINE: Duration = Duration::from_secs(8);
const MAX_COMPOSITION_BYTES: usize = 64 * 1024;

fn now_nanos() -> Option<i64> {
    i64::try_from(SystemTime::now().duration_since(UNIX_EPOCH).ok()?.as_nanos()).ok()
}

fn held(request_identifier: String, reason: SubmissionReason) -> Response {
    Response::PsycheSubmitted(SubmissionReceipt {
        request_identifier,
        submission_disposition: SubmissionDisposition::Held,
        submission_reason_option: Some(reason),
        relay_identifier_option: None,
        event_identifier_option: None,
        timestamp_nanos: now_nanos().unwrap_or_default(),
        receipt_grade: ReceiptGrade::IngressAccepted,
    })
}

fn conflict(request_identifier: String) -> Response {
    Response::PsycheSubmitted(SubmissionReceipt {
        request_identifier,
        submission_disposition: SubmissionDisposition::Rejected,
        submission_reason_option: Some(SubmissionReason::PolicyHold),
        relay_identifier_option: None,
        event_identifier_option: None,
        timestamp_nanos: now_nanos().unwrap_or_default(),
        receipt_grade: ReceiptGrade::IngressAccepted,
    })
}

fn transport_accepted(request_identifier: String, timestamp_nanos: i64) -> Response {
    Response::PsycheSubmitted(SubmissionReceipt {
        request_identifier,
        submission_disposition: SubmissionDisposition::Accepted,
        submission_reason_option: None,
        relay_identifier_option: None,
        event_identifier_option: None,
        timestamp_nanos,
        receipt_grade: ReceiptGrade::TransportAccepted,
    })
}

fn invoke_once(request_id: &str, flow_id: &str, verbatim: &str) -> bool {
    let Ok(mut child) = Command::new(BRIDGE)
        .arg(request_id)
        .arg(flow_id)
        .arg(verbatim)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn() else { return false; };
    let Some(mut stdout) = child.stdout.take() else { return false; };
    let reader = thread::spawn(move || {
        let mut bounded = Vec::new();
        let result = stdout.by_ref().take(4097).read_to_end(&mut bounded);
        let _ = std::io::copy(&mut stdout, &mut std::io::sink());
        if result.is_err() || bounded.len() > 4096 { None } else { String::from_utf8(bounded).ok() }
    });
    let deadline = Instant::now() + BRIDGE_DEADLINE;
    loop {
        match child.try_wait() {
            Ok(Some(status)) => {
                let output = reader.join().ok().flatten();
                let expected = match flow_id {
                    "effa1b" => "Delivered.{ effa1b mind-sol-of-0ab019 }\n",
                    "c8d79f" => "Delivered.{ c8d79f psyche-fable-of-b05237 }\n",
                    _ => return false,
                };
                return status.success() && output.as_deref() == Some(expected);
            }
            Err(_) => { let _ = child.kill(); let _ = child.wait(); let _ = reader.join(); return false; },
            Ok(None) if Instant::now() >= deadline => {
                let _ = child.kill();
                let _ = child.wait();
                let _ = reader.join();
                return false;
            }
            Ok(None) => thread::sleep(Duration::from_millis(50)),
        }
    }
}

fn exact_live_process(flow_id: &str) -> Option<u32> {
    match flow_id {
        known_codex::FLOW_ID => {
            let live = read_known_pane()?;
            let pid = live.pane.process_id;
            let binding = ExactBindings::new(vec![known_codex::approved_binding(pid)]);
            let marker = known_codex::KnownCodexMarker { process_id: pid };
            binding.resolve(flow_id, &[live.pane], &marker).ok().map(|_| pid)
        }
        known_claude::FLOW_ID => {
            let live = read_claude_pane()?;
            let pid = live.pane.process_id;
            let binding = ExactBindings::new(vec![known_claude::approved_binding(pid)]);
            let marker = known_claude::KnownClaudeMarker { process_id: pid };
            binding.resolve(flow_id, &[live.pane], &marker).ok().map(|_| pid)
        }
        _ => None,
    }
}

pub fn submit(apply: PersonaApply, ledger: &AttemptLedger) -> Response {
    let request_id = apply.request_identifier;
    if !matches!(apply.accepted_ingress, AcceptedIngress::UnityPoc)
        || apply.provenance != Provenance::PsycheViaUnity
    {
        return held(request_id, SubmissionReason::PolicyHold);
    }
    if !matches!(apply.flow_identifier.as_str(), known_codex::FLOW_ID | known_claude::FLOW_ID) {
        return held(request_id, SubmissionReason::UnknownFlow);
    }
    if apply.psyche_text.trim().is_empty() {
        return held(request_id, SubmissionReason::EmptyText);
    }
    if apply.psyche_text.len() > MAX_COMPOSITION_BYTES {
        return held(request_id, SubmissionReason::PolicyHold);
    }
    let flow_id = apply.flow_identifier.as_str();
    match ledger.begin(&request_id, flow_id, &apply.psyche_text) {
        Ok(Begin::PreviousAccepted(stamp)) => return transport_accepted(request_id, stamp),
        Ok(Begin::PreviousUncertain) => return held(request_id, SubmissionReason::PolicyHold),
        Ok(Begin::Conflict) => return conflict(request_id),
        Ok(Begin::Fresh) => {},
        Err(_) => return held(request_id, SubmissionReason::PolicyHold),
    }
    let Some(pre_pid) = exact_live_process(flow_id) else {
        return held(request_id, SubmissionReason::TargetUnavailable);
    };
    if invoke_once(&request_id, flow_id, &apply.psyche_text) {
        if exact_live_process(flow_id) != Some(pre_pid) {
            return held(request_id, SubmissionReason::UnresolvedSession);
        }
        // Exit success attests only that the fixed bridge submitted transport
        // to Messenger, not that the target pane presented or read the text.
        let Some(stamp) = now_nanos() else {
            return held(request_id, SubmissionReason::PolicyHold);
        };
        if ledger.record_transport_accepted(&request_id, stamp).is_ok() {
            transport_accepted(request_id, stamp)
        } else {
            held(request_id, SubmissionReason::PolicyHold)
        }
    } else {
        // The bridge may have acted before failure or timeout. Never retry.
        held(request_id, SubmissionReason::PolicyHold)
    }
}
