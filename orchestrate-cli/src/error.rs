//! Crate-owned error enum per `~/primary/skills/rust/errors.md`.
//!
//! Every variant is structured. Foreign error types convert via
//! `#[from]`. The crate never surfaces `anyhow` / `eyre` /
//! `Box<dyn Error>` at any boundary.

use std::io;
use std::path::PathBuf;

use signal_persona_mind as contract;

use crate::lane::Lane;
use crate::scope::RawScope;

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("unknown lane token: {token}")]
    UnknownLane { token: String },

    #[error("lane {lane} appears in registry but is missing from the closed Lane enum — update orchestrate-cli to mirror orchestrate/roles.list")]
    LaneNotInEnum { lane: String },

    #[error("role registry has no entries — check {path}")]
    EmptyRoleRegistry { path: PathBuf },

    #[error("role registry malformed at {path}:{line}: {message}")]
    RoleRegistryParse {
        path: PathBuf,
        line: usize,
        message: String,
    },

    #[error("lock file read failed at {path}")]
    LockRead {
        path: PathBuf,
        #[source]
        source: io::Error,
    },

    #[error("lock file write failed at {path}")]
    LockWrite {
        path: PathBuf,
        #[source]
        source: io::Error,
    },

    #[error("registry read failed at {path}")]
    RegistryRead {
        path: PathBuf,
        #[source]
        source: io::Error,
    },

    #[error("path normalization failed for {input}: {message}")]
    PathNormalization { input: String, message: String },

    #[error(
        "scope refers to BEADS; BEADS is shared coordination state and is never claimed. \
         Drop {path:?} and run bd directly, or claim a specific bead with [bead-id]."
    )]
    BeadsScopeForbidden { path: PathBuf },

    #[error("claim {own_scope} (held by {own_lane}) overlaps {peer_scope} (held by {peer_lane})")]
    ClaimOverlap {
        own_lane: Lane,
        own_scope: String,
        peer_lane: Lane,
        peer_scope: String,
    },

    #[error("invalid task token {raw:?}: {message}")]
    InvalidTaskToken { raw: String, message: String },

    #[error("scope is neither an absolute/relative path nor a bracketed task token: {raw}")]
    UnclassifiableScope { raw: RawScope },

    #[error("contract refused {role_token} (no matching signal-persona-mind RoleName variant — workspace registry has lanes the contract does not yet know)")]
    LaneOutsideContract { role_token: String },

    #[error("scope reason must be non-empty and single-line")]
    InvalidScopeReason,

    #[error(transparent)]
    Contract(#[from] contract::Error),
}
