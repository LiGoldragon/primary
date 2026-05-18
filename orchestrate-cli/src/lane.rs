//! The workspace's role lanes.
//!
//! Lanes are the per-instance coordination identities — one lock file
//! per lane, one report subdirectory per lane. `Lane` mirrors the
//! current `orchestrate/roles.list` registry as a closed enum so call
//! sites get exhaustive `match` coverage.
//!
//! Each lane maps to a [`signal_persona_orchestrate::RoleName`] variant via
//! [`Lane::role_name`]. The contract mirrors the current workspace lane
//! list, including the second-assistant lanes.

use std::fmt;

use signal_persona_orchestrate::RoleName;

use crate::error::Error;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Lane {
    Operator,
    OperatorAssistant,
    SecondOperatorAssistant,
    Designer,
    DesignerAssistant,
    SecondDesignerAssistant,
    SystemSpecialist,
    SystemAssistant,
    SecondSystemAssistant,
    Poet,
    PoetAssistant,
}

impl Lane {
    pub const ALL: [Self; 11] = [
        Self::Operator,
        Self::OperatorAssistant,
        Self::SecondOperatorAssistant,
        Self::Designer,
        Self::DesignerAssistant,
        Self::SecondDesignerAssistant,
        Self::SystemSpecialist,
        Self::SystemAssistant,
        Self::SecondSystemAssistant,
        Self::Poet,
        Self::PoetAssistant,
    ];

    pub const fn as_token(self) -> &'static str {
        match self {
            Self::Operator => "operator",
            Self::OperatorAssistant => "operator-assistant",
            Self::SecondOperatorAssistant => "second-operator-assistant",
            Self::Designer => "designer",
            Self::DesignerAssistant => "designer-assistant",
            Self::SecondDesignerAssistant => "second-designer-assistant",
            Self::SystemSpecialist => "system-specialist",
            Self::SystemAssistant => "system-assistant",
            Self::SecondSystemAssistant => "second-system-assistant",
            Self::Poet => "poet",
            Self::PoetAssistant => "poet-assistant",
        }
    }

    pub fn from_token(token: &str) -> Result<Self, Error> {
        for lane in Self::ALL {
            if lane.as_token() == token {
                return Ok(lane);
            }
        }
        Err(Error::UnknownLane {
            token: token.to_string(),
        })
    }

    pub fn lock_file_name(self) -> String {
        format!("{}.lock", self.as_token())
    }

    /// Project the workspace-side lane onto the contract-side
    /// [`RoleName`].
    pub const fn role_name(self) -> RoleName {
        match self {
            Self::Operator => RoleName::Operator,
            Self::OperatorAssistant => RoleName::OperatorAssistant,
            Self::SecondOperatorAssistant => RoleName::SecondOperatorAssistant,
            Self::Designer => RoleName::Designer,
            Self::DesignerAssistant => RoleName::DesignerAssistant,
            Self::SecondDesignerAssistant => RoleName::SecondDesignerAssistant,
            Self::SystemSpecialist => RoleName::SystemSpecialist,
            Self::SystemAssistant => RoleName::SystemAssistant,
            Self::SecondSystemAssistant => RoleName::SecondSystemAssistant,
            Self::Poet => RoleName::Poet,
            Self::PoetAssistant => RoleName::PoetAssistant,
        }
    }
}

impl fmt::Display for Lane {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_token())
    }
}
