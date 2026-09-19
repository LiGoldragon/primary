//! Persona owns Herdr and transcript observation for the one reviewed flow.

use std::time::{SystemTime, UNIX_EPOCH};

use signal_mentci::{
    ActivitySource, ConversationEntry, ConversationObservation, ConversationSnapshot,
    CorrelationStatus, FlowSnapshot, FlowState, OperationFailure, Provenance, Response,
    RosterObservation, RosterSnapshot, SourceKind, SourceStatus, Unavailability,
};

use crate::{
    correlation::ExactBindings,
    history::{read_page, Format, HistoryError},
    known_claude::{self, KnownClaudeMarker},
    known_codex::{self, KnownCodexMarker},
    ledger::AttemptLedger,
    live_herdr::{read_claude_pane, read_known_pane, read_roster},
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
    let Some(seats) = read_roster() else {
        return unavailable(observation.request_identifier, Unavailability::PersonaUnavailable);
    };
    let Some(stamp) = now_nanos() else {
        return unavailable(observation.request_identifier, Unavailability::SourceUnreadable);
    };
    let flows = seats.into_iter().map(|seat| {
        let expected_codex = seat.name == "mind-sol-of-0ab019" && seat.pane_id == "wC:p2";
        let expected_claude = seat.name == "psyche-fable-of-b05237" && seat.pane_id == "w4:p7";
        let verified = if expected_codex {
            read_known_pane().is_some_and(|live| {
                let marker = KnownCodexMarker { process_id: live.pane.process_id };
                ExactBindings::new(vec![known_codex::approved_binding(live.pane.process_id)])
                    .resolve(known_codex::FLOW_ID, &[live.pane], &marker).is_ok()
            })
        } else if expected_claude {
            read_claude_pane().is_some_and(|live| {
                let marker = KnownClaudeMarker { process_id: live.pane.process_id };
                ExactBindings::new(vec![known_claude::approved_binding(live.pane.process_id)])
                    .resolve(known_claude::FLOW_ID, &[live.pane], &marker).is_ok()
            })
        } else { false };
        let flow_identifier_option = if verified {
            Some(if expected_codex { known_codex::FLOW_ID } else { known_claude::FLOW_ID }.into())
        } else { None };
        let correlation_status = if verified { CorrelationStatus::Verified }
            else if expected_codex || expected_claude { CorrelationStatus::Unavailable }
            else { CorrelationStatus::Unknown };
        let flow_state = match seat.state.as_str() {
            "working" => FlowState::Working,
            "idle" => FlowState::Idle,
            "blocked" => FlowState::Blocked,
            "stopped" | "done" => FlowState::Stopped,
            _ => FlowState::Unknown,
        };
        FlowSnapshot {
            flow_identifier_option,
            flow_name: seat.name,
            seat_label: seat.agent,
            flow_state,
            timestamp_nanos_option: None,
            activity_source: ActivitySource::Herdr,
            pane_identifier: seat.pane_id,
            terminal_identifier: seat.terminal_id,
            correlation_status,
        }
    }).collect();
    Response::RosterObserved(RosterSnapshot {
        request_identifier: observation.request_identifier,
        timestamp_nanos: stamp,
        source_status: SourceStatus::Complete,
        flows,
    })
}

pub fn observe_conversation(observation: ConversationObservation) -> Response {
    if observation.flow_identifier != known_codex::FLOW_ID
        && observation.flow_identifier != known_claude::FLOW_ID {
        return unavailable(observation.request_identifier, Unavailability::CorrelationUnresolved);
    }
    let session = if observation.flow_identifier == known_codex::FLOW_ID {
        let Some(live) = read_known_pane() else {
            return unavailable(observation.request_identifier, Unavailability::PersonaUnavailable);
        };
        let marker = KnownCodexMarker { process_id: live.pane.process_id };
        ExactBindings::new(vec![known_codex::approved_binding(live.pane.process_id)])
            .resolve(known_codex::FLOW_ID, &[live.pane], &marker)
    } else {
        let Some(live) = read_claude_pane() else {
            return unavailable(observation.request_identifier, Unavailability::PersonaUnavailable);
        };
        let marker = KnownClaudeMarker { process_id: live.pane.process_id };
        ExactBindings::new(vec![known_claude::approved_binding(live.pane.process_id)])
            .resolve(known_claude::FLOW_ID, &[live.pane], &marker)
    };
    let Ok(session) = session else {
        return unavailable(observation.request_identifier, Unavailability::CorrelationUnresolved);
    };
    let format = if observation.flow_identifier == known_codex::FLOW_ID { Format::Codex } else { Format::Claude };
    let page = match read_page(&session.exact_transcripts[0], &session.native_session_id,
        format, observation.conversation_cursor_option) {
        Ok(page) => page,
        Err(HistoryError::Unavailable) => return unavailable(observation.request_identifier, Unavailability::SourceUnreadable),
        Err(HistoryError::SnapshotChanged) => return unavailable(observation.request_identifier, Unavailability::SnapshotChanged),
        Err(HistoryError::ResourceLimit) => return unavailable(observation.request_identifier, Unavailability::ResourceLimit),
    };
    let Some(stamp) = now_nanos() else {
        return unavailable(observation.request_identifier, Unavailability::SourceUnreadable);
    };
    let status = if page.older_cursor.is_none() && !page.incomplete {
        SourceStatus::Complete
    } else { SourceStatus::Partial };
    let entries = page.entries.into_iter().enumerate().filter_map(|(index, entry)| {
        Some(ConversationEntry {
            entry_identifier: entry.global_id,
            sequence: i64::try_from(index).ok()?,
            source_ordinal: i64::try_from(entry.source_ordinal).ok()?,
            timestamp_nanos: entry.occurred_at_nanos,
            entry_text: entry.text,
            source_kind: if entry.user_input { SourceKind::UserInput } else { SourceKind::FinalResponse },
            provenance: if entry.user_input { Provenance::Unknown } else { Provenance::Machine },
            attributed_actor_option: entry.actor,
        })
    }).collect();
    Response::ConversationObserved(ConversationSnapshot {
        request_identifier: observation.request_identifier,
        flow_identifier: observation.flow_identifier,
        timestamp_nanos: stamp,
        source_status: status,
        snapshot_bytes: i64::try_from(page.snapshot_bytes).unwrap_or_default(),
        current_bytes: i64::try_from(page.current_bytes).unwrap_or_default(),
        window_start: i64::try_from(page.window_start).unwrap_or_default(),
        window_end: i64::try_from(page.window_end).unwrap_or_default(),
        conversation_cursor_option: page.older_cursor,
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
