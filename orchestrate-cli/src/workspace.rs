//! Workspace paths.
//!
//! [`Workspace`] resolves the canonical layout the orchestration helper
//! cares about: the lane lock directory, the role registry file, and
//! the BEADS root. It is independent of any current-working-directory
//! state and is therefore safe to pass around tests.

use std::path::{Path, PathBuf};

use crate::lane::Lane;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Workspace {
    root: PathBuf,
}

impl Workspace {
    pub fn new(root: impl Into<PathBuf>) -> Self {
        Self { root: root.into() }
    }

    pub fn root(&self) -> &Path {
        &self.root
    }

    pub fn orchestrate_dir(&self) -> PathBuf {
        self.root.join("orchestrate")
    }

    pub fn role_registry(&self) -> PathBuf {
        self.orchestrate_dir().join("roles.list")
    }

    pub fn lock_path(&self, lane: Lane) -> PathBuf {
        self.orchestrate_dir().join(lane.lock_file_name())
    }

    pub fn beads_root(&self) -> PathBuf {
        self.root.join(".beads")
    }

    pub fn is_beads_scope(&self, path: &Path) -> bool {
        path == self.beads_root() || path.starts_with(self.beads_root())
    }
}
