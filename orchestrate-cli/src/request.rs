//! Project argv into the typed [`signal_persona_orchestrate::OrchestrateRequest`].
//!
//! The CLI accepts the convenience argv form (`claim <lane> <scope> ...
//! -- <reason>`); this module decodes that form into the typed Rust
//! value the contract owns. The lock-file projection is the side
//! effect; the [`OrchestrateRequest`] is the source-of-truth shape
//! that will eventually ship over the `persona-orchestrate` socket.

use signal_persona_orchestrate::{
    OrchestrateRequest, RoleClaim, RoleObservation, RoleRelease, ScopeReason, ScopeReference,
};

use crate::error::{Error, Result};
use crate::lane::Lane;
use crate::scope::NormalizedScope;

pub fn claim_request(
    lane: Lane,
    scopes: &[NormalizedScope],
    reason: &str,
) -> Result<OrchestrateRequest> {
    let role = lane.role_name();
    let scope_references: Vec<ScopeReference> =
        scopes.iter().map(NormalizedScope::as_reference).collect();
    let reason = ScopeReason::from_text(reason).map_err(|_| Error::InvalidScopeReason)?;

    Ok(OrchestrateRequest::RoleClaim(RoleClaim {
        role,
        scopes: scope_references,
        reason,
    }))
}

pub fn release_request(lane: Lane) -> OrchestrateRequest {
    let role = lane.role_name();
    OrchestrateRequest::RoleRelease(RoleRelease { role })
}

pub fn observation_request() -> OrchestrateRequest {
    OrchestrateRequest::RoleObservation(RoleObservation)
}
