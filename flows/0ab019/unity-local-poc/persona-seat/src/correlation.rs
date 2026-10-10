//! Persona's exact live binding gate. No prefix matching or path globbing is
//! permitted between a logical flow and a native transcript session.

use std::path::PathBuf;

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum HarnessKind {
    Claude,
    Codex,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct LivePane {
    pub pane_id: String,
    pub terminal_id: String,
    pub process_id: u32,
    pub native_session_id: String,
    pub harness: HarnessKind,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct FlowBinding {
    pub flow_id: String,
    pub pane_id: String,
    pub terminal_id: String,
    pub process_id: u32,
    pub native_session_id: String,
    pub harness: HarnessKind,
}

/// A Persona-owned reading of the Herdr marker, not a path supplied by Mentci.
/// The concrete marker reader must provide complete exact rollout paths.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct MarkerSession {
    pub flow_id: String,
    pub pane_id: String,
    pub terminal_id: String,
    pub process_id: u32,
    pub native_session_id: String,
    pub harness: HarnessKind,
    pub exact_transcripts: Vec<PathBuf>,
}

pub trait MarkerBackedSource {
    fn read_exact_session(&self, flow_id: &str) -> Option<MarkerSession>;
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum CorrelationRefusal {
    NoExactBinding,
    AmbiguousBinding,
    MissingMarker,
    MarkerMismatch,
    MissingExactTranscript,
}

#[derive(Clone, Debug, Default)]
pub struct ExactBindings {
    records: Vec<FlowBinding>,
}

impl ExactBindings {
    pub fn new(records: Vec<FlowBinding>) -> Self {
        Self { records }
    }

    /// The live pane and the marker-backed registration must agree on every
    /// native identity field. A flow alias alone never selects a transcript.
    pub fn resolve(
        &self,
        flow_id: &str,
        live_panes: &[LivePane],
        markers: &impl MarkerBackedSource,
    ) -> Result<MarkerSession, CorrelationRefusal> {
        let matching: Vec<&FlowBinding> = self.records.iter().filter(|record| {
            record.flow_id == flow_id && live_panes.iter().any(|pane| {
                record.pane_id == pane.pane_id
                    && record.terminal_id == pane.terminal_id
                    && record.process_id == pane.process_id
                    && record.native_session_id == pane.native_session_id
                    && record.harness == pane.harness
            })
        }).collect();
        let binding = match matching.as_slice() {
            [] => Err(CorrelationRefusal::NoExactBinding),
            [record] => Ok(*record),
            _ => Err(CorrelationRefusal::AmbiguousBinding),
        }?;
        let marker = markers.read_exact_session(flow_id)
            .ok_or(CorrelationRefusal::MissingMarker)?;
        if marker.flow_id != binding.flow_id
            || marker.pane_id != binding.pane_id
            || marker.terminal_id != binding.terminal_id
            || marker.process_id != binding.process_id
            || marker.native_session_id != binding.native_session_id
            || marker.harness != binding.harness
        {
            return Err(CorrelationRefusal::MarkerMismatch);
        }
        if marker.exact_transcripts.is_empty() {
            return Err(CorrelationRefusal::MissingExactTranscript);
        }
        Ok(marker)
    }
}

#[cfg(test)]
mod tests {
    use super::{CorrelationRefusal, ExactBindings, FlowBinding, HarnessKind, LivePane, MarkerBackedSource, MarkerSession};
    use std::path::PathBuf;

    fn binding() -> FlowBinding {
        FlowBinding {
            flow_id: String::from("fixture-flow"),
            pane_id: String::from("pane-a"),
            terminal_id: String::from("terminal-a"),
            process_id: 100,
            native_session_id: String::from("11111111-2222-3333-4444-555555555555"),
            harness: HarnessKind::Codex,
        }
    }

    struct FixtureMarker(MarkerSession);

    impl MarkerBackedSource for FixtureMarker {
        fn read_exact_session(&self, _flow_id: &str) -> Option<MarkerSession> {
            Some(self.0.clone())
        }
    }

    fn marker() -> FixtureMarker {
        let binding = binding();
        FixtureMarker(MarkerSession {
            flow_id: binding.flow_id,
            pane_id: binding.pane_id,
            terminal_id: binding.terminal_id,
            process_id: binding.process_id,
            native_session_id: binding.native_session_id,
            harness: binding.harness,
            exact_transcripts: vec![PathBuf::from("/synthetic/exact-rollout.jsonl")],
        })
    }

    fn pane() -> LivePane {
        LivePane {
            pane_id: String::from("pane-a"),
            terminal_id: String::from("terminal-a"),
            process_id: 100,
            native_session_id: String::from("11111111-2222-3333-4444-555555555555"),
            harness: HarnessKind::Codex,
        }
    }

    #[test]
    fn exact_native_identity_resolves() {
        let bindings = ExactBindings::new(vec![binding()]);
        assert_eq!(bindings.resolve("fixture-flow", &[pane()], &marker()), Ok(marker().0));
    }

    #[test]
    fn flow_alias_without_exact_native_identity_is_refused() {
        let bindings = ExactBindings::new(vec![binding()]);
        let mut replacement = pane();
        replacement.native_session_id = String::from("11111111-2222-3333-4444-999999999999");
        assert_eq!(bindings.resolve("fixture-flow", &[replacement], &marker()), Err(CorrelationRefusal::NoExactBinding));
    }

    #[test]
    fn marker_uuid_mismatch_is_held() {
        let bindings = ExactBindings::new(vec![binding()]);
        let mut wrong = marker();
        wrong.0.native_session_id = String::from("11111111-2222-3333-4444-999999999999");
        assert_eq!(bindings.resolve("fixture-flow", &[pane()], &wrong), Err(CorrelationRefusal::MarkerMismatch));
    }
}
