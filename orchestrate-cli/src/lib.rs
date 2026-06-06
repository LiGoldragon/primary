//! Workspace coordination helper.
//!
//! `orchestrate-cli` is the Rust compatibility surface for
//! `tools/orchestrate`. It accepts the existing `claim` / `release` /
//! `status` argv shape, projects the operation into a typed
//! `signal_orchestrate::OrchestrateRequest`, and sends it to the
//! long-lived `orchestrate` daemon. Lock files are a daemon projection
//! kept for humans and transitional agents.
//!
//! Design surface: [`crate::workspace::Workspace`] holds the workspace
//! paths; [`crate::registry::LaneRegistry`] loads `orchestrate/roles.list`;
//! [`crate::claim::ClaimOutcome`] / [`crate::claim::Workspace`] drive the
//! claim/release flow against typed scopes and lock files.

pub mod claim;
pub mod daemon_client;
pub mod error;
pub mod lane;
pub mod lockfile;
pub mod overlap;
pub mod registry;
pub mod render;
pub mod request;
pub mod scope;
pub mod verify_jj;
pub mod workspace;

pub use claim::{ClaimOutcome, ReleaseOutcome, StatusReport};
pub use error::Error;
pub use lane::Lane;
pub use lockfile::{LockEntry, LockFile};
pub use registry::{LaneDescriptor, LaneRegistry};
pub use scope::{NormalizedScope, RawScope};
pub use workspace::Workspace;
