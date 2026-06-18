//! Crate-owned error enum per `~/primary/skills/rust/errors.md`.
//!
//! Every variant is structured. Foreign error types convert via
//! `#[from]`. The crate never surfaces `anyhow` / `eyre` /
//! `Box<dyn Error>` at any boundary.

use std::io;
use std::path::PathBuf;
use std::string::FromUtf8Error;

use signal_orchestrate as contract;

use crate::lane::Lane;
use crate::scope::RawScope;

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("role registry has no entries — check {path}")]
    EmptyRoleRegistry { path: PathBuf },

    #[error("role registry malformed at {path}:{line}: {message}")]
    RoleRegistryParse {
        path: PathBuf,
        line: usize,
        message: String,
    },

    #[error("unknown lane {lane}; add it to {registry} before using it")]
    UnknownLane { lane: Lane, registry: PathBuf },

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

    #[error("input/output failure: {0}")]
    Io(#[from] io::Error),

    #[error("active repository map read failed at {path}")]
    ActiveRepositoryMapRead {
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

    #[error("scope reason must be non-empty and single-line")]
    InvalidScopeReason,

    #[error(transparent)]
    Contract(#[from] contract::Error),

    #[error(transparent)]
    Nota(#[from] nota_next::NotaDecodeError),

    #[error(transparent)]
    CommandLine(#[from] signal_frame::CommandLineError),

    #[error("orchestrate client failed with status {status}: {stderr}")]
    ClientFailed { status: String, stderr: String },

    #[error("orchestrate client output was not UTF-8: {0}")]
    ClientOutputUtf8(FromUtf8Error),

    #[error("daemon startup configuration rkyv encode failed")]
    StartupConfigurationEncode,

    #[error("daemon build failed with status {status}")]
    DaemonBuildFailed { status: String },

    #[error("daemon exited before becoming ready with status {status}")]
    DaemonExitedBeforeReady { status: String },

    #[error("daemon did not become ready at {socket}")]
    DaemonReadinessTimeout { socket: PathBuf },

    #[error("daemon executable path has no parent: {path}")]
    DaemonExecutableHasNoParent { path: PathBuf },

    #[error("unexpected daemon reply: {message}")]
    UnexpectedDaemonReply { message: String },
}
