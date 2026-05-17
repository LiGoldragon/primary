//! Claim / release / status flows.
//!
//! Each flow projects argv into a typed
//! [`signal_persona_mind::MindRequest`] and reduces the projection into
//! the lock-file side effect plus a typed outcome the caller can render.
//! The legacy shell helper's plain-text rendering is built on top of
//! [`StatusReport`] and the per-flow outcomes in [`crate::render`].

use signal_persona_mind::MindRequest;

use crate::error::{Error, Result};
use crate::lane::Lane;
use crate::lockfile::{LockEntry, LockFile};
use crate::overlap;
use crate::registry::LaneRegistry;
use crate::request;
use crate::scope::{NormalizedScope, RawScope};
use crate::workspace::Workspace;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ClaimOverlapDescription {
    pub own_lane: Lane,
    pub own_scope: NormalizedScope,
    pub peer_lane: Lane,
    pub peer_scope: NormalizedScope,
    pub peer_reason: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ClaimOutcome {
    Accepted {
        request: MindRequest,
        lane: Lane,
        scopes: Vec<NormalizedScope>,
        reason: String,
    },
    Rejected {
        request: MindRequest,
        lane: Lane,
        overlaps: Vec<ClaimOverlapDescription>,
    },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReleaseOutcome {
    pub request: MindRequest,
    pub lane: Lane,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LaneStatus {
    pub lane: Lane,
    pub lock: LockFile,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StatusReport {
    pub request: MindRequest,
    pub lanes: Vec<LaneStatus>,
}

pub fn claim(
    workspace: &Workspace,
    registry: &LaneRegistry,
    lane: Lane,
    raw_scopes: Vec<RawScope>,
    reason: &str,
    working_directory: &std::path::Path,
) -> Result<ClaimOutcome> {
    if raw_scopes.is_empty() {
        return Err(Error::InvalidScopeReason);
    }

    let scopes: Vec<NormalizedScope> = raw_scopes
        .iter()
        .map(|raw| NormalizedScope::from_raw(raw, working_directory))
        .collect::<Result<Vec<_>>>()?;

    for (raw, scope) in raw_scopes.iter().zip(scopes.iter()) {
        if let NormalizedScope::Path(path) = scope {
            let as_path = std::path::Path::new(path.as_str());
            if workspace.is_beads_scope(as_path) {
                return Err(Error::BeadsScopeForbidden {
                    path: as_path.to_path_buf(),
                });
            }
            // raw is kept available so future error refinements can
            // echo the user's input verbatim instead of the normalized
            // form.
            let _ = raw;
        }
    }

    let request = request::claim_request(lane, &scopes, reason)?;

    let entries: Vec<LockEntry> = scopes
        .iter()
        .cloned()
        .map(|scope| LockEntry {
            scope,
            reason: if reason.is_empty() {
                None
            } else {
                Some(reason.to_string())
            },
        })
        .collect();
    let lock = LockFile::new(entries);
    lock.write(&workspace.lock_path(lane))?;

    let overlaps = detect_overlaps(workspace, registry, lane, &scopes)?;
    if !overlaps.is_empty() {
        // Roll the claim back so peer agents see the lane idle again.
        LockFile::default().write(&workspace.lock_path(lane))?;
        return Ok(ClaimOutcome::Rejected {
            request,
            lane,
            overlaps,
        });
    }

    Ok(ClaimOutcome::Accepted {
        request,
        lane,
        scopes,
        reason: reason.to_string(),
    })
}

pub fn release(workspace: &Workspace, lane: Lane) -> Result<ReleaseOutcome> {
    let request = request::release_request(lane);
    LockFile::default().write(&workspace.lock_path(lane))?;
    Ok(ReleaseOutcome { request, lane })
}

pub fn status(workspace: &Workspace, registry: &LaneRegistry) -> Result<StatusReport> {
    let request = request::observation_request();
    let mut lanes = Vec::new();
    for lane in registry.lanes() {
        let lock = LockFile::read(&workspace.lock_path(lane))?;
        lanes.push(LaneStatus { lane, lock });
    }
    Ok(StatusReport { request, lanes })
}

fn detect_overlaps(
    workspace: &Workspace,
    registry: &LaneRegistry,
    own_lane: Lane,
    own_scopes: &[NormalizedScope],
) -> Result<Vec<ClaimOverlapDescription>> {
    let mut overlaps = Vec::new();
    for peer in registry.peer_lanes(own_lane) {
        let peer_lock = LockFile::read(&workspace.lock_path(peer))?;
        for peer_entry in peer_lock.entries() {
            for own_scope in own_scopes {
                if overlap::overlap(own_scope, &peer_entry.scope) {
                    overlaps.push(ClaimOverlapDescription {
                        own_lane,
                        own_scope: own_scope.clone(),
                        peer_lane: peer,
                        peer_scope: peer_entry.scope.clone(),
                        peer_reason: peer_entry.reason.clone(),
                    });
                }
            }
        }
    }
    Ok(overlaps)
}
