//! One-shot controlled POC submission. Persona freshly rebinds the exact seat
//! before invoking the fixed, source-packaged messenger bridge with three
//! arguments. Bridge exit alone is not a target-side presentation witness.

use std::{
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
    known_codex::{approved_binding, KnownCodexMarker, FLOW_ID},
    ledger::{AttemptLedger, Begin},
    live_herdr::read_known_pane,
    protocol::{AcceptedIngress, PersonaApply},
};

const BRIDGE: &str = "/nix/store/rc7vng7pgrfd0k55424n3wl60cs2i7z6-primary-messaging-runtime/bin/msg-psyche-poc";
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
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn() else { return false; };
    let deadline = Instant::now() + BRIDGE_DEADLINE;
    loop {
        match child.try_wait() {
            Ok(Some(status)) => return status.success(),
            Err(_) => return false,
            Ok(None) if Instant::now() >= deadline => {
                let _ = child.kill();
                let _ = child.wait();
                return false;
            }
            Ok(None) => thread::sleep(Duration::from_millis(50)),
        }
    }
}

pub fn submit(apply: PersonaApply, ledger: &AttemptLedger) -> Response {
    let request_id = apply.request_identifier;
    if !matches!(apply.accepted_ingress, AcceptedIngress::UnityPoc)
        || apply.provenance != Provenance::PsycheViaUnity
    {
        return held(request_id, SubmissionReason::PolicyHold);
    }
    if apply.flow_identifier != FLOW_ID {
        return held(request_id, SubmissionReason::UnknownFlow);
    }
    if apply.psyche_text.trim().is_empty() {
        return held(request_id, SubmissionReason::EmptyText);
    }
    if apply.psyche_text.len() > MAX_COMPOSITION_BYTES {
        return held(request_id, SubmissionReason::PolicyHold);
    }
    match ledger.begin(&request_id, FLOW_ID, &apply.psyche_text) {
        Ok(Begin::PreviousAccepted(stamp)) => return transport_accepted(request_id, stamp),
        Ok(Begin::PreviousUncertain) => return held(request_id, SubmissionReason::PolicyHold),
        Ok(Begin::Conflict) => return conflict(request_id),
        Ok(Begin::Fresh) => {},
        Err(_) => return held(request_id, SubmissionReason::PolicyHold),
    }
    let Some(live) = read_known_pane() else {
        return held(request_id, SubmissionReason::TargetUnavailable);
    };
    let binding = ExactBindings::new(vec![approved_binding(live.pane.process_id)]);
    let marker = KnownCodexMarker { process_id: live.pane.process_id };
    if binding.resolve(FLOW_ID, &[live.pane], &marker).is_err() {
        return held(request_id, SubmissionReason::UnresolvedSession);
    }
    if invoke_once(&request_id, FLOW_ID, &apply.psyche_text) {
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
