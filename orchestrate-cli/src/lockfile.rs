//! Lock-file projection.
//!
//! Each line of an `orchestrate/<lane>.lock` file is one held scope,
//! optionally annotated with a ` # <reason>` suffix. Blank lines and
//! pure comment lines (a leading `#`) are ignored on read, matching
//! the shell helper's `awk` filter.
//!
//! Writers render scopes through [`NormalizedScope::lock_file_form`] so
//! the on-disk text is byte-identical to the shell output.

use std::fs;
use std::path::{Path, PathBuf};

use crate::error::{Error, Result};
use crate::scope::NormalizedScope;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LockEntry {
    pub scope: NormalizedScope,
    pub reason: Option<String>,
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct LockFile {
    entries: Vec<LockEntry>,
}

impl LockFile {
    pub fn new(entries: Vec<LockEntry>) -> Self {
        Self { entries }
    }

    pub fn entries(&self) -> &[LockEntry] {
        &self.entries
    }

    pub fn is_idle(&self) -> bool {
        self.entries.is_empty()
    }

    pub fn read(path: &Path) -> Result<Self> {
        let text = match fs::read_to_string(path) {
            Ok(text) => text,
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => return Ok(Self::default()),
            Err(source) => {
                return Err(Error::LockRead {
                    path: path.to_path_buf(),
                    source,
                });
            }
        };
        Self::parse(&text, path)
    }

    pub fn parse(text: &str, path: impl AsRef<Path>) -> Result<Self> {
        let mut entries = Vec::new();
        for raw_line in text.lines() {
            let trimmed = raw_line.trim();
            if trimmed.is_empty() || trimmed.starts_with('#') {
                continue;
            }

            let (scope_text, reason) = match trimmed.find(" # ") {
                Some(index) => {
                    let (left, right) = trimmed.split_at(index);
                    let reason_text = right
                        .strip_prefix(" # ")
                        .expect("split_at returns the boundary unchanged")
                        .trim()
                        .to_string();
                    let reason_opt = if reason_text.is_empty() {
                        None
                    } else {
                        Some(reason_text)
                    };
                    (left.trim().to_string(), reason_opt)
                }
                None => (trimmed.to_string(), None),
            };

            let scope = parse_scope(&scope_text, path.as_ref())?;
            entries.push(LockEntry { scope, reason });
        }
        Ok(Self { entries })
    }

    pub fn render(&self) -> String {
        let mut out = String::new();
        for entry in &self.entries {
            out.push_str(&entry.scope.lock_file_form());
            if let Some(reason) = &entry.reason {
                out.push_str(" # ");
                out.push_str(reason);
            }
            out.push('\n');
        }
        out
    }

    pub fn write(&self, path: &Path) -> Result<()> {
        if let Some(parent) = path.parent() {
            if !parent.as_os_str().is_empty() {
                fs::create_dir_all(parent).map_err(|source| Error::LockWrite {
                    path: path.to_path_buf(),
                    source,
                })?;
            }
        }
        fs::write(path, self.render()).map_err(|source| Error::LockWrite {
            path: path.to_path_buf(),
            source,
        })
    }
}

fn parse_scope(text: &str, source: &Path) -> Result<NormalizedScope> {
    let raw = crate::scope::RawScope::new(text);

    // Lock-file paths are already absolute on the canonical write path;
    // resolve against `/` so even a hand-edited relative line lands as
    // an absolute lock entry without depending on caller cwd.
    let working_directory = PathBuf::from("/");
    NormalizedScope::from_raw(&raw, &working_directory).map_err(|err| match err {
        Error::PathNormalization { input, message } => Error::PathNormalization {
            input,
            message: format!("{message} (from {source})", source = source.display()),
        },
        other => other,
    })
}
