//! Loader for `orchestrate/roles.list`.
//!
//! The interim registry is a bash-readable text file: one lane per
//! line, optional `assistant-of:<main-role>` or
//! `parallel-of:<main-role>` marker. Comments
//! (`# ...`) and blank lines are ignored.
//!
//! [`LaneRegistry`] validates every lane through the
//! `signal-orchestrate` role-token type, then preserves the
//! registry order for status rendering.

use std::fs;
use std::path::{Path, PathBuf};

use crate::error::{Error, Result};
use crate::lane::Lane;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LaneDescriptor {
    pub lane: Lane,
    pub assistant_of: Option<Lane>,
    pub parallel_of: Option<Lane>,
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
            let lane = Lane::from_token(lane_token)?;

            let mut assistant_of = None;
            let mut parallel_of = None;
            for marker in fields {
                if let Some(role) = marker.strip_prefix("assistant-of:") {
                    let main = Lane::from_token(role).map_err(|_| Error::RoleRegistryParse {
                        path: path.clone(),
                        line: line_number,
                        message: format!("unknown main role in assistant-of marker: {role}"),
                    })?;
                    assistant_of = Some(main);
                } else if let Some(role) = marker.strip_prefix("parallel-of:") {
                    let main = Lane::from_token(role).map_err(|_| Error::RoleRegistryParse {
                        path: path.clone(),
                        line: line_number,
                        message: format!("unknown main role in parallel-of marker: {role}"),
                    })?;
                    parallel_of = Some(main);
                } else {
                    return Err(Error::RoleRegistryParse {
                        path: path.clone(),
                        line: line_number,
                        message: format!("unrecognised marker: {marker}"),
                    });
                }
            }

            descriptors.push(LaneDescriptor {
                lane,
                assistant_of,
                parallel_of,
            });
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
        self.descriptors
            .iter()
            .map(|descriptor| descriptor.lane.clone())
    }

    pub fn descriptors(&self) -> &[LaneDescriptor] {
        &self.descriptors
    }

    pub fn require_lane(&self, lane: &Lane) -> Result<()> {
        if self
            .descriptors
            .iter()
            .any(|descriptor| &descriptor.lane == lane)
        {
            Ok(())
        } else {
            Err(Error::UnknownLane {
                lane: lane.clone(),
                registry: self.source_path.clone(),
            })
        }
    }

    pub fn peer_lanes<'a>(&'a self, lane: &'a Lane) -> impl Iterator<Item = Lane> + 'a {
        self.lanes().filter(move |other| other != lane)
    }

    pub fn source_path(&self) -> &Path {
        &self.source_path
    }
}
