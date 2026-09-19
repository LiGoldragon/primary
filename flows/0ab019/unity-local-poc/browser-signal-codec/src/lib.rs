//! Restricted browser projection of the Mentci Signal contract.
//!
//! The only exported constructors are the three POC queries. Each decoder
//! accepts its paired response or the common typed unavailability reply. The
//! WebSocket message itself is always one complete canonical Signal frame;
//! JavaScript receives plain view objects only after validated restoration.

mod frame;

use frame::{CanonicalFrame, POC_MAX_BODY_BYTES};
use js_sys::{Array, Object, Reflect};
use signal::{Framable, FrameCapacity};
use signal_mentci::{
    ActivitySource, ConversationCursor, ConversationObservation, CorrelationStatus, FlowState,
    OperationFailure, Provenance, PsycheSubmission, Query, Response, Restorable,
    RosterObservation, Signal, Signalizable, SourceKind, SourceStatus,
    SubmissionDisposition, SubmissionReason, Unavailability,
};
use wasm_bindgen::prelude::*;

const MAX_IDENTIFIER_BYTES: usize = 256;
const MAX_COMPOSITION_BYTES: usize = 64 * 1024;
const MAX_CONVERSATION_ENTRIES: usize = 100;

/// Carries only byte and projection limits, never domain policy or authority.
#[wasm_bindgen]
pub struct BrowserSignalCodec {
    frame_capacity: FrameCapacity,
}

#[wasm_bindgen]
impl BrowserSignalCodec {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self {
            frame_capacity: FrameCapacity::from(POC_MAX_BODY_BYTES),
        }
    }

    pub fn encode_observe_roster(&self, request_id: String) -> Result<Vec<u8>, JsValue> {
        self.identifier(&request_id)?;
        self.encode(Query::ObserveRoster(RosterObservation {
            request_identifier: request_id,
        }))
    }

    pub fn encode_observe_conversation(
        &self,
        request_id: String,
        flow_id: String,
        cursor: JsValue,
    ) -> Result<Vec<u8>, JsValue> {
        self.identifier(&request_id)?;
        self.identifier(&flow_id)?;
        self.encode(Query::ObserveConversation(ConversationObservation {
            request_identifier: request_id,
            flow_identifier: flow_id,
            conversation_cursor_option: self.parse_cursor(cursor)?,
        }))
    }

    pub fn encode_submit_psyche(
        &self,
        request_id: String,
        flow_id: String,
        text: String,
    ) -> Result<Vec<u8>, JsValue> {
        self.identifier(&request_id)?;
        self.identifier(&flow_id)?;
        if text.trim().is_empty() || text.len() > MAX_COMPOSITION_BYTES {
            return Err(JsValue::from_str("Composition is empty or exceeds the POC limit."));
        }
        self.encode(Query::SubmitPsyche(PsycheSubmission {
            request_identifier: request_id,
            flow_identifier: flow_id,
            psyche_text: text,
        }))
    }

    pub fn decode_roster_observed(&self, message: &[u8]) -> Result<JsValue, JsValue> {
        match self.restore(message)? {
            Response::RosterObserved(snapshot) => {
                let out = Object::new();
                self.put(&out, "request_id", &JsValue::from_str(&snapshot.request_identifier))?;
                self.put(&out, "observed_at_nanos", &JsValue::from_str(&snapshot.timestamp_nanos.to_string()))?;
                self.put(&out, "source_status", &JsValue::from_str(self.source_status(&snapshot.source_status)))?;
                let flows = Array::new();
                for flow in snapshot.flows {
                    let item = Object::new();
                    self.put(&item, "flow_id", &flow.flow_identifier_option.map_or(JsValue::NULL, |id| JsValue::from_str(&id)))?;
                    self.put(&item, "name", &JsValue::from_str(&flow.flow_name))?;
                    self.put(&item, "seat", &JsValue::from_str(&flow.seat_label))?;
                    self.put(&item, "state", &JsValue::from_str(self.flow_state(&flow.flow_state)))?;
                    self.put(&item, "pane_id", &JsValue::from_str(&flow.pane_identifier))?;
                    self.put(&item, "terminal_id", &JsValue::from_str(&flow.terminal_identifier))?;
                    self.put(&item, "correlation_status", &JsValue::from_str(self.correlation_status(&flow.correlation_status)))?;
                    self.put(&item, "last_activity_at_nanos", &self.optional_nanos(flow.timestamp_nanos_option))?;
                    self.put(&item, "last_activity_source", &JsValue::from_str(self.activity_source(&flow.activity_source)))?;
                    flows.push(&item);
                }
                self.put(&out, "flows", &flows)?;
                Ok(out.into())
            }
            Response::OperationUnavailable(failure) => self.failure(failure),
            _ => Err(JsValue::from_str("Expected RosterObserved or OperationUnavailable.")),
        }
    }

    pub fn decode_conversation_observed(&self, message: &[u8]) -> Result<JsValue, JsValue> {
        match self.restore(message)? {
            Response::ConversationObserved(snapshot) => {
                if snapshot.entries.len() > MAX_CONVERSATION_ENTRIES {
                    return Err(JsValue::from_str("Conversation exceeds the POC entry limit."));
                }
                let out = Object::new();
                self.put(&out, "request_id", &JsValue::from_str(&snapshot.request_identifier))?;
                self.put(&out, "flow_id", &JsValue::from_str(&snapshot.flow_identifier))?;
                self.put(&out, "observed_at_nanos", &JsValue::from_str(&snapshot.timestamp_nanos.to_string()))?;
                self.put(&out, "source_status", &JsValue::from_str(self.source_status(&snapshot.source_status)))?;
                self.put(&out, "snapshot_bytes", &JsValue::from_str(&snapshot.snapshot_bytes.to_string()))?;
                self.put(&out, "current_bytes", &JsValue::from_str(&snapshot.current_bytes.to_string()))?;
                self.put(&out, "window_start", &JsValue::from_str(&snapshot.window_start.to_string()))?;
                self.put(&out, "window_end", &JsValue::from_str(&snapshot.window_end.to_string()))?;
                self.put(&out, "older_cursor", &snapshot.conversation_cursor_option.map_or(JsValue::NULL, |cursor| self.cursor_view(cursor)))?;
                let entries = Array::new();
                for entry in snapshot.entries {
                    let item = Object::new();
                    self.put(&item, "entry_id", &JsValue::from_str(&entry.entry_identifier))?;
                    self.put(&item, "sequence", &JsValue::from_str(&entry.sequence.to_string()))?;
                    self.put(&item, "source_ordinal", &JsValue::from_str(&entry.source_ordinal.to_string()))?;
                    self.put(&item, "occurred_at_nanos", &JsValue::from_str(&entry.timestamp_nanos.to_string()))?;
                    self.put(&item, "text", &JsValue::from_str(&entry.entry_text))?;
                    self.put(&item, "source_kind", &JsValue::from_str(self.source_kind(&entry.source_kind)))?;
                    self.put(&item, "provenance", &JsValue::from_str(self.provenance(&entry.provenance)))?;
                    self.put(&item, "attributed_actor", &entry.attributed_actor_option.map_or(JsValue::NULL, |actor| JsValue::from_str(&actor)))?;
                    entries.push(&item);
                }
                self.put(&out, "entries", &entries)?;
                Ok(out.into())
            }
            Response::OperationUnavailable(failure) => self.failure(failure),
            _ => Err(JsValue::from_str("Expected ConversationObserved or OperationUnavailable.")),
        }
    }

    pub fn decode_psyche_submitted(&self, message: &[u8]) -> Result<JsValue, JsValue> {
        match self.restore(message)? {
            Response::PsycheSubmitted(receipt) => {
                let out = Object::new();
                self.put(&out, "request_id", &JsValue::from_str(&receipt.request_identifier))?;
                self.put(&out, "disposition", &JsValue::from_str(self.disposition(&receipt.submission_disposition)))?;
                self.put(&out, "reason", &receipt.submission_reason_option.map_or(JsValue::NULL, |reason| JsValue::from_str(self.submission_reason(&reason))))?;
                self.put(&out, "relay_id", &receipt.relay_identifier_option.map_or(JsValue::NULL, |value| JsValue::from_str(&value)))?;
                self.put(&out, "event_id", &receipt.event_identifier_option.map_or(JsValue::NULL, |value| JsValue::from_str(&value)))?;
                self.put(&out, "receipt_at_nanos", &JsValue::from_str(&receipt.timestamp_nanos.to_string()))?;
                self.put(&out, "receipt_grade", &JsValue::from_str(self.receipt_grade(&receipt.receipt_grade)))?;
                Ok(out.into())
            }
            Response::OperationUnavailable(failure) => self.failure(failure),
            _ => Err(JsValue::from_str("Expected PsycheSubmitted or OperationUnavailable.")),
        }
    }
}

impl BrowserSignalCodec {
    fn cursor_view(&self, cursor: ConversationCursor) -> JsValue {
        let out = Object::new();
        for (name, value) in [
            ("native_session_id", cursor.native_session_identifier),
            ("file_device", cursor.file_device.to_string()),
            ("file_inode", cursor.file_inode.to_string()),
            ("snapshot_bytes", cursor.snapshot_bytes.to_string()),
            ("before_byte", cursor.before_byte.to_string()),
        ] {
            let _ = self.put(&out, name, &JsValue::from_str(&value));
        }
        out.into()
    }

    fn parse_cursor(&self, value: JsValue) -> Result<Option<ConversationCursor>, JsValue> {
        if value.is_null() || value.is_undefined() { return Ok(None); }
        let field = |name: &str| -> Result<String, JsValue> {
            Reflect::get(&value, &JsValue::from_str(name))?
                .as_string().ok_or_else(|| JsValue::from_str("Conversation cursor field is missing."))
        };
        let integer = |name| -> Result<i64, JsValue> {
            field(name)?.parse().map_err(|_| JsValue::from_str("Conversation cursor integer is invalid."))
        };
        Ok(Some(ConversationCursor {
            native_session_identifier: field("native_session_id")?,
            file_device: integer("file_device")?,
            file_inode: integer("file_inode")?,
            snapshot_bytes: integer("snapshot_bytes")?,
            before_byte: integer("before_byte")?,
        }))
    }

    fn identifier(&self, value: &str) -> Result<(), JsValue> {
        if value.is_empty() || value.len() > MAX_IDENTIFIER_BYTES {
            return Err(JsValue::from_str("Identifier is empty or exceeds the POC limit."));
        }
        Ok(())
    }

    fn encode(&self, query: Query) -> Result<Vec<u8>, JsValue> {
        let signal = query.signalize().map_err(|_| JsValue::from_str("Signal archive failed."))?;
        let message = signal.framed(self.frame_capacity)
            .map_err(|_| JsValue::from_str("Signal frame exceeds the POC limit."))?;
        CanonicalFrame::try_from(message.as_slice())
            .map_err(|_| JsValue::from_str("Signal produced an invalid frame."))?;
        Ok(message)
    }

    fn restore(&self, message: &[u8]) -> Result<Response, JsValue> {
        let frame = CanonicalFrame::try_from(message)
            .map_err(|_| JsValue::from_str("WebSocket message is not one canonical Signal frame."))?;
        Signal::<Response>::from(frame.body().to_vec())
            .restore()
            .map_err(|_| JsValue::from_str("Signal archive was rejected."))
    }

    fn put(&self, object: &Object, key: &str, value: &JsValue) -> Result<(), JsValue> {
        Reflect::set(object, &JsValue::from_str(key), value).map(|_| ())
    }

    fn optional_nanos(&self, value: Option<i64>) -> JsValue {
        value.map_or(JsValue::NULL, |nanos| JsValue::from_str(&nanos.to_string()))
    }

    fn source_status(&self, value: &SourceStatus) -> &'static str {
        match value {
            SourceStatus::Complete => "complete",
            SourceStatus::Partial => "partial",
            SourceStatus::Unavailable => "unavailable",
        }
    }

    fn flow_state(&self, value: &FlowState) -> &'static str {
        match value {
            FlowState::Working => "working",
            FlowState::Idle => "idle",
            FlowState::Blocked => "blocked",
            FlowState::Stopped => "stopped",
            FlowState::Unknown => "unknown",
        }
    }

    fn correlation_status(&self, value: &CorrelationStatus) -> &'static str {
        match value {
            CorrelationStatus::Verified => "verified",
            CorrelationStatus::Unknown => "unknown",
            CorrelationStatus::Unavailable => "unavailable",
        }
    }

    fn activity_source(&self, value: &ActivitySource) -> &'static str {
        match value {
            ActivitySource::Herdr => "Herdr",
            ActivitySource::Transcript => "Transcript",
            ActivitySource::Unknown => "Unknown",
        }
    }

    fn source_kind(&self, value: &SourceKind) -> &'static str {
        match value {
            SourceKind::UserInput => "user-input",
            SourceKind::FinalResponse => "final-response",
        }
    }

    fn provenance(&self, value: &Provenance) -> &'static str {
        match value {
            Provenance::PsycheViaUnity => "PsycheViaUnity",
            Provenance::Machine => "Machine",
            Provenance::Unknown => "Unknown",
        }
    }

    fn disposition(&self, value: &SubmissionDisposition) -> &'static str {
        match value {
            SubmissionDisposition::Accepted => "accepted",
            SubmissionDisposition::Held => "held",
            SubmissionDisposition::Rejected => "rejected",
        }
    }

    fn submission_reason(&self, value: &SubmissionReason) -> &'static str {
        match value {
            SubmissionReason::UnknownFlow => "UnknownFlow",
            SubmissionReason::UnresolvedSession => "UnresolvedSession",
            SubmissionReason::TargetUnavailable => "TargetUnavailable",
            SubmissionReason::EmptyText => "EmptyText",
            SubmissionReason::PolicyHold => "PolicyHold",
        }
    }

    fn receipt_grade(&self, value: &signal_mentci::ReceiptGrade) -> &'static str {
        match value {
            signal_mentci::ReceiptGrade::IngressAccepted => "IngressAccepted",
            signal_mentci::ReceiptGrade::TransportAccepted => "TransportAccepted",
            signal_mentci::ReceiptGrade::TargetPresented => "TargetPresented",
        }
    }

    fn failure(&self, failure: OperationFailure) -> Result<JsValue, JsValue> {
        let out = Object::new();
        self.put(&out, "request_id", &JsValue::from_str(&failure.request_identifier))?;
        self.put(&out, "source_status", &JsValue::from_str("unavailable"))?;
        let reason = match failure.unavailability {
            Unavailability::PersonaUnavailable => "PersonaUnavailable",
            Unavailability::CorrelationUnresolved => "CorrelationUnresolved",
            Unavailability::SourceUnreadable => "SourceUnreadable",
            Unavailability::TransportUnavailable => "TransportUnavailable",
            Unavailability::SnapshotChanged => "SnapshotChanged",
            Unavailability::ResourceLimit => "ResourceLimit",
        };
        self.put(&out, "reason", &JsValue::from_str(reason))?;
        Ok(out.into())
    }
}
