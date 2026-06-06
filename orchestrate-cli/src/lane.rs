//! The workspace's role lanes.
//!
//! Lanes are the per-instance coordination identities — one lock file
//! per lane, one report subdirectory per lane. `Lane` is a validated
//! token loaded from `orchestrate/roles.list`; the registry, not this
//! crate, is the current source of truth for which lanes exist.

use std::fmt;

use signal_orchestrate::RoleName;

use crate::error::Error;

#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct Lane(String);

impl Lane {
    pub fn from_token(token: &str) -> Result<Self, Error> {
        RoleName::from_wire_token(token).map_err(Error::Contract)?;
        Ok(Self(token.to_string()))
    }

    pub fn as_token(&self) -> &str {
        &self.0
    }

    pub fn lock_file_name(&self) -> String {
        format!("{}.lock", self.as_token())
    }

    /// Project the workspace-side lane onto the contract-side role
    /// identifier.
    pub fn role_name(&self) -> Result<RoleName, Error> {
        RoleName::from_wire_token(self.as_token()).map_err(Error::Contract)
    }
}

impl fmt::Display for Lane {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_token())
    }
}
