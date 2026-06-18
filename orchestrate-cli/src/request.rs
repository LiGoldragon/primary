//! Project argv into the typed [`signal_orchestrate::OrchestrateRequest`].
//!
//! The CLI accepts the convenience argv form (`claim <lane> <scope> ...
//! -- <reason>`); this module decodes that form into the typed Rust
//! value the contract owns. The daemon owns durable state; lock files
//! are a compatibility projection of accepted daemon claims.

use signal_orchestrate::{
    Observation, OrchestrateRequest, RoleClaim, ScopeReason, ScopeReference,
    schema::lib::{
        Input as SchemaInput, RoleIdentifier as SchemaRoleIdentifier,
        RoleName as SchemaRoleName, RoleRelease as SchemaRoleRelease,
    },
};

use crate::error::{Error, Result};
use crate::lane::Lane;
use crate::scope::NormalizedScope;

pub fn claim_request(
    lane: Lane,
    scopes: &[NormalizedScope],
    reason: &str,
) -> Result<OrchestrateRequest> {
    let role = lane.role_name()?;
    let scope_references: Vec<ScopeReference> =
        scopes.iter().map(NormalizedScope::as_reference).collect();
    let reason = ScopeReason::from_text(reason).map_err(|_| Error::InvalidScopeReason)?;

    Ok(OrchestrateRequest::Claim(RoleClaim {
        role,
        scopes: scope_references,
        reason,
    }))
}

pub fn release_request(lane: Lane) -> Result<SchemaInput> {
    lane.role_name()?;
    let role = SchemaRoleName::new(SchemaRoleIdentifier::new(lane.as_token().to_string()));
    Ok(SchemaInput::Release(SchemaRoleRelease::new(role)))
}

pub fn observation_request() -> OrchestrateRequest {
    OrchestrateRequest::Observe(Observation::Roles)
}
