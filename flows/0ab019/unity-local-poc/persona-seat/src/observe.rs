//! Persona owns Herdr and transcript observation for the one reviewed flow.

use std::time::{SystemTime, UNIX_EPOCH};

use signal_mentci::{
    ActivitySource, ConversationEntry, ConversationObservation, ConversationSnapshot,
    FlowSnapshot, FlowState, OperationFailure, Provenance, Response,
    RosterObservation, RosterSnapshot, SourceKind, SourceStatus, Unavailability,
};

use crate::{
    codex_history::{read_initial_page, HistoryStatus},
    correlation::ExactBindings,
    known_codex::{approved_binding, KnownCodexMarker, FLOW_ID},
    ledger::AttemptLedger,
    live_herdr::read_known_pane,
    protocol::PersonaRequest,
    send::submit,
};

fn now_nanos() -> Option<i64> {
    i64::try_from(SystemTime::now().duration_since(UNIX_EPOCH).ok()?.as_nanos()).ok()
}

fn unavailable(request_identifier: String, why: Unavailability) -> Response {
    Response::OperationUnavailable(OperationFailure {
        request_identifier,
        unavailability: why,
    })
}

pub fn observe_roster(observation: RosterObservation) -> Response {
    let Some(live) = read_known_pane() else {
        return unavailable(observation.request_identifier, Unavailability::PersonaUnavailable);
    };
    let binding = ExactBindings::new(vec![approved_binding(live.pane.process_id)]);
    let marker = KnownCodexMarker { process_id: live.pane.process_id };
    if binding.resolve(FLOW_ID, &[live.pane], &marker).is_err() {
        return unavailable(observation.request_identifier, Unavailability::CorrelationUnresolved);
    }
    let Some(stamp) = now_nanos() else {
        return unavailable(observation.request_identifier, Unavailability::SourceUnreadable);
    };
    let flow_state = match live.state.as_str() {
        "working" => FlowState::Working,
        "idle" => FlowState::Idle,
        "blocked" => FlowState::Blocked,
        "stopped" => FlowState::Stopped,
        _ => FlowState::Unknown,
    };
    Response::RosterObserved(RosterSnapshot {
        request_identifier: observation.request_identifier,
        timestamp_nanos: stamp,
        source_status: SourceStatus::Partial,
        flows: vec![FlowSnapshot {
            flow_identifier: FLOW_ID.into(),
            flow_name: String::from("MindSol POC"),
            seat_label: String::from("labelled Persona POC"),
            flow_state,
            timestamp_nanos_option: None,
            activity_source: ActivitySource::Herdr,
        }],
    })
}

pub fn observe_conversation(observation: ConversationObservation) -> Response {
    if observation.flow_identifier != FLOW_ID {
        return unavailable(observation.request_identifier, Unavailability::CorrelationUnresolved);
    }
    let Some(live) = read_known_pane() else {
        return unavailable(observation.request_identifier, Unavailability::PersonaUnavailable);
    };
    let binding = ExactBindings::new(vec![approved_binding(live.pane.process_id)]);
    let marker = KnownCodexMarker { process_id: live.pane.process_id };
    let Ok(session) = binding.resolve(FLOW_ID, &[live.pane], &marker) else {
        return unavailable(observation.request_identifier, Unavailability::CorrelationUnresolved);
    };
    let page = read_initial_page(&session);
    if page.status == HistoryStatus::Unavailable {
        return unavailable(observation.request_identifier, Unavailability::SourceUnreadable);
    }
    let Some(stamp) = now_nanos() else {
        return unavailable(observation.request_identifier, Unavailability::SourceUnreadable);
    };
    let entries = page.entries.into_iter().enumerate().filter_map(|(index, entry)| {
        Some(ConversationEntry {
            entry_identifier: entry.global_id,
            sequence: i64::try_from(index).ok()?,
            source_ordinal: i64::try_from(entry.source_ordinal).ok()?,
            timestamp_nanos: entry.occurred_at_nanos,
            entry_text: entry.text,
            source_kind: SourceKind::FinalResponse,
            provenance: Provenance::Machine,
            attributed_actor_option: Some(entry.attributed_actor),
        })
    }).collect();
    Response::ConversationObserved(ConversationSnapshot {
        request_identifier: observation.request_identifier,
        flow_identifier: observation.flow_identifier,
        timestamp_nanos: stamp,
        source_status: SourceStatus::Partial,
        entries,
    })
}

pub fn respond(request: PersonaRequest, ledger: &AttemptLedger) -> Response {
    match request {
        PersonaRequest::ObserveRoster(observation) => observe_roster(observation),
        PersonaRequest::ObserveConversation(observation) => observe_conversation(observation),
        PersonaRequest::ApplyPsyche(apply) => submit(apply, ledger),
    }
}
