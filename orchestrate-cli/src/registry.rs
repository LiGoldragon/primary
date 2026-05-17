//! Loader for `orchestrate/roles.list`.
//!
//! The interim registry is a bash-readable text file: one lane per
//! line, optional `assistant-of:<main-role>` marker. Comments
//! (`# ...`) and blank lines are ignored.
//!
//! [`LaneRegistry`] checks the loaded set against the closed
//! [`crate::Lane`] enum so any drift between the on-disk registry and
//! the Rust port surfaces as a typed
//! [`Error::LaneNotInEnum`](crate::Error::LaneNotInEnum) at load time
//! rather than silently failing later.

use std::fs;
use std::path::{Path, PathBuf};

use crate::error::{Error, Result};
use crate::lane::Lane;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LaneDescriptor {
    pub lane: Lane,
    pub assistant_of: Option<Lane>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LaneRegistry {
    descriptors: Vec<LaneDescriptor>,
    source_path: PathBuf,
}

impl LaneRegistry {
    pub fn load(path: impl Into<PathBuf>) -> Result<Self> {
        let path = path.into();
        let text = fs::read_to_string(&path).map_err(|source| Error::RegistryRead {
            path: path.clone(),
            source,
        })?;
        Self::parse_with_source(&text, path)
    }

    pub fn parse(text: &str) -> Result<Self> {
        Self::parse_with_source(text, PathBuf::from("<memory>"))
    }

    fn parse_with_source(text: &str, path: PathBuf) -> Result<Self> {
        let mut descriptors = Vec::new();

        for (index, raw_line) in text.lines().enumerate() {
            let line_number = index + 1;
            let trimmed = raw_line.trim();
            if trimmed.is_empty() || trimmed.starts_with('#') {
                continue;
            }

            let mut fields = trimmed.split_whitespace();
            let lane_token = fields
                .next()
                .expect("non-empty trimmed line has at least one token");
            let lane = Lane::from_token(lane_token).map_err(|_| Error::LaneNotInEnum {
                lane: lane_token.to_string(),
            })?;

            let mut assistant_of = None;
            for marker in fields {
                if let Some(role) = marker.strip_prefix("assistant-of:") {
                    let main = Lane::from_token(role).map_err(|_| Error::RoleRegistryParse {
                        path: path.clone(),
                        line: line_number,
                        message: format!("unknown main role in assistant-of marker: {role}"),
                    })?;
                    assistant_of = Some(main);
                } else {
                    return Err(Error::RoleRegistryParse {
                        path: path.clone(),
                        line: line_number,
                        message: format!("unrecognised marker: {marker}"),
                    });
                }
            }

            descriptors.push(LaneDescriptor { lane, assistant_of });
        }

        if descriptors.is_empty() {
            return Err(Error::EmptyRoleRegistry { path });
        }

        Ok(Self {
            descriptors,
            source_path: path,
        })
    }

    pub fn lanes(&self) -> impl Iterator<Item = Lane> + '_ {
        self.descriptors.iter().map(|descriptor| descriptor.lane)
    }

    pub fn descriptors(&self) -> &[LaneDescriptor] {
        &self.descriptors
    }

    pub fn peer_lanes(&self, lane: Lane) -> impl Iterator<Item = Lane> + '_ {
        self.lanes().filter(move |other| *other != lane)
    }

    pub fn source_path(&self) -> &Path {
        &self.source_path
    }
}
