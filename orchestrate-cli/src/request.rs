//! Project argv into the typed [`signal_persona_mind::MindRequest`].
//!
//! The CLI accepts the convenience argv form (`claim <lane> <scope> ...
//! -- <reason>`); this module decodes that form into the typed Rust
//! value the contract owns. The lock-file projection is the side
//! effect; the [`MindRequest`] is the source-of-truth shape that will
//! eventually ship over the `persona-mind` socket.

use signal_persona_mind::{
    MindRequest, RoleClaim, RoleObservation, RoleRelease, ScopeReason, ScopeReference,
};

use crate::error::{Error, Result};
use crate::lane::Lane;
use crate::scope::NormalizedScope;

pub fn claim_request(
    lane: Lane,
    scopes: &[NormalizedScope],
    reason: &str,
) -> Result<MindRequest> {
    let role = lane.role_name();
    let scope_references: Vec<ScopeReference> = scopes
        .iter()
        .map(NormalizedScope::as_reference)
        .collect();
    let reason = ScopeReason::from_text(reason).map_err(|_| Error::InvalidScopeReason)?;

    Ok(MindRequest::RoleClaim(RoleClaim {
        role,
        scopes: scope_references,
        reason,
    }))
}

pub fn release_request(lane: Lane) -> MindRequest {
    let role = lane.role_name();
    MindRequest::RoleRelease(RoleRelease { role })
}

pub fn observation_request() -> MindRequest {
    MindRequest::RoleObservation(RoleObservation)
}
