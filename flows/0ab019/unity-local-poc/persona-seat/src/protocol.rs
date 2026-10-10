//! Private Mentci-to-Persona Signal contract. Public SubmitPsyche is never a
//! Persona request; only Mentci constructs Apply after accepting its Unity
//! route capability. The Persona Unix listener also checks the kernel peer PID.

use signal_mentci::{ConversationObservation, Provenance, RosterObservation};

const PRIVATE_TAG: [u8; 16] = *b"PersonaPOCWire01";

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug)]
pub struct PersonaEnvelope {
    tag: [u8; 16],
    request: PersonaRequest,
}

impl PersonaEnvelope {
    pub fn new(request: PersonaRequest) -> Self {
        Self { tag: PRIVATE_TAG, request }
    }

    pub fn into_request(self) -> Option<PersonaRequest> {
        (self.tag == PRIVATE_TAG).then_some(self.request)
    }
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug)]
pub enum PersonaRequest {
    ObserveRoster(RosterObservation),
    ObserveConversation(ConversationObservation),
    ApplyPsyche(PersonaApply),
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug)]
pub struct PersonaApply {
    pub request_identifier: String,
    pub flow_identifier: String,
    pub psyche_text: String,
    pub accepted_ingress: AcceptedIngress,
    pub provenance: Provenance,
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug)]
pub enum AcceptedIngress {
    UnityPoc,
}

impl PersonaApply {
    pub fn from_accepted_unity(request_identifier: String, flow_identifier: String, psyche_text: String) -> Self {
        Self {
            request_identifier,
            flow_identifier,
            psyche_text,
            accepted_ingress: AcceptedIngress::UnityPoc,
            provenance: Provenance::PsycheViaUnity,
        }
    }
}

#[cfg(test)]
mod tests {
    use signal::{Restorable, Signal, Signalizable};
    use signal_mentci::{PsycheSubmission, Query};

    use super::PersonaEnvelope;

    #[test]
    fn public_submit_query_is_not_a_persona_request() {
        let public = Query::SubmitPsyche(PsycheSubmission {
            request_identifier: "r1".into(),
            flow_identifier: "effa1b".into(),
            psyche_text: "synthetic".into(),
        });
        let bytes = public.signalize().expect("public signal");
        let private = Signal::<PersonaEnvelope>::from(signal::ByteViewable::bytes(&bytes).to_vec());
        assert!(match private.restore() {
            Err(_) => true,
            Ok(envelope) => envelope.into_request().is_none(),
        });
    }
}
