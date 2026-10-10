//! Restricted SubmitPsyche seam. A decoded query is insufficient: dispatch
//! additionally requires the capability minted by the accepted Unity route.

use signal_mentci::PsycheSubmission;

use crate::ingress::AcceptedUnityRoute;

const MAX_COMPOSITION_BYTES: usize = 64 * 1024;

/// A distinct typed payload produced inside Mentci after ingress acceptance.
/// Its text is byte-for-byte the client's original composition.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PsycheInput {
    request_id: String,
    flow_id: String,
    text: String,
}

impl PsycheInput {
    pub fn request_id(&self) -> &str { &self.request_id }
    pub fn flow_id(&self) -> &str { &self.flow_id }
    pub fn text(&self) -> &str { &self.text }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum SubmissionHold {
    EmptyText,
    TextTooLarge,
}

/// Only this function may construct the Persona-bound psyche payload. There is
/// deliberately no path from a machine-typed Signal route to this capability.
pub fn accepted_unity_submission(
    _accepted_route: &AcceptedUnityRoute,
    submission: PsycheSubmission,
) -> Result<PsycheInput, SubmissionHold> {
    if submission.psyche_text.trim().is_empty() {
        return Err(SubmissionHold::EmptyText);
    }
    if submission.psyche_text.len() > MAX_COMPOSITION_BYTES {
        return Err(SubmissionHold::TextTooLarge);
    }
    Ok(PsycheInput {
        request_id: submission.request_identifier,
        flow_id: submission.flow_identifier,
        text: submission.psyche_text,
    })
}

#[cfg(test)]
mod tests {
    use super::{accepted_unity_submission, SubmissionHold};
    use crate::ingress::LocalUnityListener;
    use signal_mentci::PsycheSubmission;

    #[test]
    fn accepted_route_preserves_raw_text() {
        let listener = LocalUnityListener::new("127.0.0.1:38081".parse().expect("listener"))
            .expect("loopback listener");
        let route = listener.accept(
            "127.0.0.1:42000".parse().expect("peer"),
            "/signal",
            "http://127.0.0.1:38081",
        ).expect("accepted route");
        let raw = String::from("  exact input  \n");
        let input = accepted_unity_submission(&route, PsycheSubmission {
            request_identifier: String::from("request-1"),
            flow_identifier: String::from("flow-1"),
            psyche_text: raw.clone(),
        }).expect("nonempty text");
        assert_eq!(input.text, raw);
        assert_eq!(accepted_unity_submission(&route, PsycheSubmission {
            request_identifier: String::from("request-2"),
            flow_identifier: String::from("flow-1"),
            psyche_text: String::from(" \n "),
        }), Err(SubmissionHold::EmptyText));
    }
}
