//! Workspace coordination helper.
//!
//! `orchestrate-cli` is the Rust port of the shell `tools/orchestrate`
//! helper. It accepts the same `claim` / `release` / `status` argv
//! surface, projects the operation into a typed
//! `signal_persona_mind::MindRequest`, and keeps the on-disk
//! `orchestrate/<lane>.lock` files bit-compatible with the shell era.
//!
//! Direct routing to `persona-mind`'s socket is deferred until the
//! daemon is the canonical store; the lock files are a serialised
//! projection of the typed records.
//!
//! Design surface: [`crate::workspace::Workspace`] holds the workspace
//! paths; [`crate::registry::LaneRegistry`] loads `orchestrate/roles.list`;
//! [`crate::claim::ClaimOutcome`] / [`crate::claim::Workspace`] drive the
//! claim/release flow against typed scopes and lock files.

pub mod claim;
pub mod error;
pub mod lane;
pub mod lockfile;
pub mod overlap;
pub mod registry;
pub mod render;
pub mod request;
pub mod scope;
pub mod workspace;

pub use claim::{ClaimOutcome, ReleaseOutcome, StatusReport};
pub use error::Error;
pub use lane::Lane;
pub use lockfile::{LockFile, LockEntry};
pub use registry::{LaneDescriptor, LaneRegistry};
pub use scope::{NormalizedScope, RawScope};
pub use workspace::Workspace;
