//! Scope types — `RawScope` for argv input, `NormalizedScope` for the
//! canonical lock-file projection.
//!
//! The shell helper distinguishes scope kinds purely by the bracketed
//! form: `^\[.+\]$` is a task lock; everything else is a path.
//! `NormalizedScope` preserves that bimodal shape but binds the values
//! to the contract's typed primitives ([`WirePath`] and [`TaskToken`])
//! so the projection into `signal_persona_mind::ScopeReference` is a
//! pure structural lift.

use std::fmt;
use std::path::{Component, Path, PathBuf};

use signal_persona_mind::{ScopeReference, TaskToken, WirePath};

use crate::error::{Error, Result};

/// The raw scope a user typed on the command line. Always a string;
/// scope kind is decided at normalization time.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RawScope(String);

impl RawScope {
    pub fn new(input: impl Into<String>) -> Self {
        Self(input.into())
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for RawScope {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.0)
    }
}

/// A scope projected into its typed kind. Path scopes carry an absolute
/// normalized path (the equivalent of `realpath -m` on the shell side);
/// task scopes carry the bare bracketed token without the brackets.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum NormalizedScope {
    Path(WirePath),
    Task(TaskToken),
}

impl NormalizedScope {
    /// Project the raw input. Relative paths are resolved against the
    /// supplied working directory; `..` components are popped without
    /// touching the filesystem (matching `realpath -m`'s "lexical"
    /// semantics, never requiring the path to exist).
    pub fn from_raw(raw: &RawScope, working_directory: &Path) -> Result<Self> {
        let value = raw.as_str().trim();

        if let Some(token) = task_token_in_brackets(value) {
            let task = TaskToken::from_wire_token(token).map_err(|_| Error::InvalidTaskToken {
                raw: value.to_string(),
                message: "task tokens must be non-empty, contain no whitespace, and no inner '['/']'".to_string(),
            })?;
            return Ok(Self::Task(task));
        }

        if value.is_empty() {
            return Err(Error::UnclassifiableScope { raw: raw.clone() });
        }

        let resolved = lexical_resolve(value, working_directory)?;
        let path_string = resolved.to_string_lossy().into_owned();
        let wire = WirePath::from_absolute_path(path_string.clone()).map_err(|_| {
            Error::PathNormalization {
                input: raw.as_str().to_string(),
                message: format!("not a stable absolute path after normalization: {path_string}"),
            }
        })?;
        Ok(Self::Path(wire))
    }

    pub fn as_reference(&self) -> ScopeReference {
        match self {
            Self::Path(path) => ScopeReference::Path(path.clone()),
            Self::Task(task) => ScopeReference::Task(task.clone()),
        }
    }

    /// Canonical lock-file rendering. Path scopes render as the
    /// absolute path; task scopes render as `[token]` so the bracketed
    /// human form is preserved.
    pub fn lock_file_form(&self) -> String {
        match self {
            Self::Path(path) => path.as_str().to_string(),
            Self::Task(task) => format!("[{}]", task.as_str()),
        }
    }
}

impl fmt::Display for NormalizedScope {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.lock_file_form())
    }
}

fn task_token_in_brackets(value: &str) -> Option<&str> {
    let stripped = value.strip_prefix('[')?.strip_suffix(']')?;
    if stripped.is_empty() {
        None
    } else {
        Some(stripped)
    }
}

fn lexical_resolve(input: &str, working_directory: &Path) -> Result<PathBuf> {
    let absolute = if Path::new(input).is_absolute() {
        PathBuf::from(input)
    } else {
        working_directory.join(input)
    };

    let mut normalized = PathBuf::new();
    for component in absolute.components() {
        match component {
            Component::Prefix(_) => {
                return Err(Error::PathNormalization {
                    input: input.to_string(),
                    message: "windows path prefixes are not supported".to_string(),
                });
            }
            Component::RootDir => normalized.push("/"),
            Component::CurDir => {}
            Component::ParentDir => {
                if !normalized.pop() {
                    return Err(Error::PathNormalization {
                        input: input.to_string(),
                        message: "parent component escapes the filesystem root".to_string(),
                    });
                }
            }
            Component::Normal(part) => normalized.push(part),
        }
    }

    if normalized.as_os_str().is_empty() {
        normalized.push("/");
    }

    Ok(normalized)
}
