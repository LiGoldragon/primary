//! Verification for workspace `push-*` jj bookmarks.
//!
//! The repository list comes from `protocols/active-repositories.md`.
//! This module does not discover repositories by walking the filesystem.

use std::collections::{BTreeMap, BTreeSet};
use std::fmt::{self, Write};
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

use crate::error::{Error, Result};
use crate::lane::Lane;
use crate::lockfile::LockFile;
use crate::scope::NormalizedScope;
use crate::workspace::Workspace;

const SECONDS_PER_DAY: u64 = 86_400;
const DIVERGENCE_LIMIT_DAYS: u64 = 7;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TrackedRepository {
    pub name: String,
    pub path: PathBuf,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PushBookmark {
    pub name: String,
    pub commit_identifier: String,
    pub commit_timestamp_seconds: u64,
    pub age_days: u64,
    pub has_remote: bool,
    pub ancestor_of_main: bool,
}

impl PushBookmark {
    pub fn delete_candidate(&self) -> bool {
        self.ancestor_of_main
    }

    pub fn rebase_or_abandon_candidate(&self) -> bool {
        !self.ancestor_of_main && self.age_days > DIVERGENCE_LIMIT_DAYS
    }

    pub fn local_only_without_home(&self) -> bool {
        !self.has_remote && !self.ancestor_of_main
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RepositoryVerification {
    Scanned {
        repository: TrackedRepository,
        bookmarks: Vec<PushBookmark>,
    },
    Skipped {
        repository: TrackedRepository,
        reason: String,
    },
    Failed {
        repository: TrackedRepository,
        reason: String,
    },
}

impl RepositoryVerification {
    pub fn bookmarks(&self) -> &[PushBookmark] {
        match self {
            RepositoryVerification::Scanned { bookmarks, .. } => bookmarks,
            RepositoryVerification::Skipped { .. } | RepositoryVerification::Failed { .. } => &[],
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VerifyReport {
    pub source: PathBuf,
    pub repositories: Vec<RepositoryVerification>,
}

impl VerifyReport {
    pub fn has_findings(&self) -> bool {
        self.repositories
            .iter()
            .any(|verification| match verification {
                RepositoryVerification::Scanned { bookmarks, .. } => {
                    bookmarks.iter().any(|bookmark| {
                        bookmark.delete_candidate()
                            || bookmark.rebase_or_abandon_candidate()
                            || bookmark.local_only_without_home()
                    })
                }
                RepositoryVerification::Skipped { .. } => false,
                RepositoryVerification::Failed { .. } => true,
            })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReleaseGuard {
    pub repositories: Vec<RepositoryVerification>,
}

impl ReleaseGuard {
    pub fn has_blockers(&self) -> bool {
        self.repositories
            .iter()
            .any(|verification| match verification {
                RepositoryVerification::Scanned { bookmarks, .. } => {
                    bookmarks.iter().any(PushBookmark::local_only_without_home)
                }
                RepositoryVerification::Skipped { .. } => false,
                RepositoryVerification::Failed { .. } => true,
            })
    }
}

pub fn verify_workspace(workspace: &Workspace, now: SystemTime) -> Result<VerifyReport> {
    let source = workspace.active_repositories_path();
    let repositories = tracked_repositories(workspace)?;
    Ok(VerifyReport {
        source,
        repositories: verify_repositories(repositories, now),
    })
}

pub fn release_guard(workspace: &Workspace, lane: &Lane, now: SystemTime) -> Result<ReleaseGuard> {
    let lock = LockFile::read(&workspace.lock_path(lane))?;
    let repositories = repositories_for_lock(&lock, &tracked_repositories(workspace)?);
    Ok(ReleaseGuard {
        repositories: verify_repositories(repositories, now),
    })
}

pub fn tracked_repositories(workspace: &Workspace) -> Result<Vec<TrackedRepository>> {
    let path = workspace.active_repositories_path();
    let text = fs::read_to_string(&path)
        .map_err(|source| Error::ActiveRepositoryMapRead { path, source })?;
    Ok(parse_tracked_repositories(&text))
}

pub fn parse_tracked_repositories(text: &str) -> Vec<TrackedRepository> {
    let mut repositories = Vec::new();
    let mut seen = BTreeSet::new();

    for line in text.lines() {
        let trimmed = line.trim();
        if !trimmed.starts_with('|') || trimmed.contains("---") {
            continue;
        }
        let cells: Vec<&str> = trimmed
            .trim_matches('|')
            .split('|')
            .map(str::trim)
            .collect();
        if cells.len() < 2 || cells[0].eq_ignore_ascii_case("repository") {
            continue;
        }
        let path_text = unquote_code(cells[1]);
        if !path_text.starts_with('/') {
            continue;
        }
        let path = PathBuf::from(path_text);
        if seen.insert(path.clone()) {
            repositories.push(TrackedRepository {
                name: unquote_code(cells[0]).to_string(),
                path,
            });
        }
    }

    repositories
}

pub fn repositories_for_lock(
    lock: &LockFile,
    repositories: &[TrackedRepository],
) -> Vec<TrackedRepository> {
    let claimed_paths: Vec<PathBuf> = lock
        .entries()
        .iter()
        .filter_map(|entry| match &entry.scope {
            NormalizedScope::Path(path) => Some(PathBuf::from(path.as_str())),
            NormalizedScope::Task(_) => None,
        })
        .collect();

    repositories
        .iter()
        .filter(|repository| {
            claimed_paths.iter().any(|claimed_path| {
                claimed_path.starts_with(&repository.path)
                    || repository.path.starts_with(claimed_path)
            })
        })
        .cloned()
        .collect()
}

pub fn render_report(report: &VerifyReport, output: &mut impl Write) -> fmt::Result {
    writeln!(
        output,
        "verify-jj: scanned {} tracked repositories from {}",
        report.repositories.len(),
        report.source.display()
    )?;
    for verification in &report.repositories {
        render_repository_verification(verification, output)?;
    }
    Ok(())
}

pub fn render_release_guard(guard: &ReleaseGuard, output: &mut impl Write) -> fmt::Result {
    writeln!(
        output,
        "release refused: unresolved local-only push-* bookmarks"
    )?;
    for verification in &guard.repositories {
        match verification {
            RepositoryVerification::Scanned {
                repository,
                bookmarks,
            } => {
                let blockers: Vec<&PushBookmark> = bookmarks
                    .iter()
                    .filter(|bookmark| bookmark.local_only_without_home())
                    .collect();
                if blockers.is_empty() {
                    continue;
                }
                writeln!(
                    output,
                    "{} ({})",
                    repository.name,
                    repository.path.display()
                )?;
                for bookmark in blockers {
                    writeln!(
                        output,
                        "  {} {}: local-only and not an ancestor of main",
                        bookmark.name, bookmark.commit_identifier
                    )?;
                }
            }
            RepositoryVerification::Failed { repository, reason } => {
                writeln!(
                    output,
                    "{} ({}): verification failed: {}",
                    repository.name,
                    repository.path.display(),
                    reason
                )?;
            }
            RepositoryVerification::Skipped { .. } => {}
        }
    }
    writeln!(
        output,
        "Run tools/orchestrate verify-jj, then land on main, push the bookmark, or abandon/rebase deliberately before release."
    )
}

fn verify_repositories(
    repositories: Vec<TrackedRepository>,
    now: SystemTime,
) -> Vec<RepositoryVerification> {
    repositories
        .into_iter()
        .map(|repository| verify_repository(repository, now))
        .collect()
}

fn verify_repository(repository: TrackedRepository, now: SystemTime) -> RepositoryVerification {
    if !repository.path.exists() {
        return RepositoryVerification::Skipped {
            repository,
            reason: "path does not exist".to_string(),
        };
    }
    if !repository.path.join(".jj").exists() {
        return RepositoryVerification::Skipped {
            repository,
            reason: "not a colocated jj repository".to_string(),
        };
    }

    match read_push_bookmarks(&repository.path, now) {
        Ok(bookmarks) => RepositoryVerification::Scanned {
            repository,
            bookmarks,
        },
        Err(reason) => RepositoryVerification::Failed { repository, reason },
    }
}

fn read_push_bookmarks(
    repository: &Path,
    now: SystemTime,
) -> std::result::Result<Vec<PushBookmark>, String> {
    let rows = run_jj(
        repository,
        &[
            "bookmark",
            "list",
            "push-*",
            "--all-remotes",
            "-T",
            r#"name ++ "\t" ++ remote ++ "\t" ++ normal_target.commit_id().short(12) ++ "\t" ++ normal_target.committer().timestamp().format("%s") ++ "\n""#,
        ],
    )?;
    let now_seconds = now
        .duration_since(UNIX_EPOCH)
        .map_err(|error| format!("system clock is before unix epoch: {error}"))?
        .as_secs();

    let grouped = parse_bookmark_rows(&rows)?;
    let mut bookmarks = Vec::new();
    for local in grouped.into_values().filter_map(|group| group.local) {
        let ancestor_of_main = bookmark_is_ancestor_of_main(repository, &local.name)?;
        bookmarks.push(PushBookmark {
            name: local.name,
            commit_identifier: local.commit_identifier,
            commit_timestamp_seconds: local.commit_timestamp_seconds,
            age_days: now_seconds.saturating_sub(local.commit_timestamp_seconds) / SECONDS_PER_DAY,
            has_remote: local.has_remote,
            ancestor_of_main,
        });
    }
    bookmarks.sort_by(|left, right| left.name.cmp(&right.name));
    Ok(bookmarks)
}

fn bookmark_is_ancestor_of_main(
    repository: &Path,
    bookmark: &str,
) -> std::result::Result<bool, String> {
    let revset = format!(
        "bookmarks(exact:\"{}\")::main",
        escape_revset_string(bookmark)
    );
    let output = run_jj(
        repository,
        &[
            "log",
            "-r",
            &revset,
            "--no-graph",
            "-T",
            "commit_id.short()",
        ],
    )?;
    Ok(!output.trim().is_empty())
}

fn run_jj(repository: &Path, arguments: &[&str]) -> std::result::Result<String, String> {
    let output = Command::new("jj")
        .arg("--ignore-working-copy")
        .arg("--no-pager")
        .arg("--color")
        .arg("never")
        .arg("-R")
        .arg(repository)
        .args(arguments)
        .output()
        .map_err(|error| format!("could not run jj: {error}"))?;
    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        return Err(stderr.trim().to_string());
    }
    Ok(String::from_utf8_lossy(&output.stdout).into_owned())
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct BookmarkRow {
    name: String,
    remote: Option<String>,
    commit_identifier: String,
    commit_timestamp_seconds: u64,
}

#[derive(Debug, Default, Clone, PartialEq, Eq)]
struct BookmarkGroup {
    local: Option<LocalBookmark>,
    remote_names: BTreeSet<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct LocalBookmark {
    name: String,
    commit_identifier: String,
    commit_timestamp_seconds: u64,
    has_remote: bool,
}

fn parse_bookmark_rows(text: &str) -> std::result::Result<BTreeMap<String, BookmarkGroup>, String> {
    let mut rows = Vec::new();
    for (line_index, line) in text.lines().enumerate() {
        if line.trim().is_empty() {
            continue;
        }
        let cells: Vec<&str> = line.split('\t').collect();
        if cells.len() != 4 {
            return Err(format!(
                "unexpected jj bookmark row at line {}: {line}",
                line_index + 1
            ));
        }
        let commit_timestamp_seconds = cells[3].parse::<u64>().map_err(|error| {
            format!(
                "invalid timestamp in jj bookmark row at line {}: {error}",
                line_index + 1
            )
        })?;
        rows.push(BookmarkRow {
            name: cells[0].to_string(),
            remote: if cells[1].is_empty() {
                None
            } else {
                Some(cells[1].to_string())
            },
            commit_identifier: cells[2].to_string(),
            commit_timestamp_seconds,
        });
    }
    Ok(group_bookmark_rows(rows))
}

fn group_bookmark_rows(rows: Vec<BookmarkRow>) -> BTreeMap<String, BookmarkGroup> {
    let mut grouped: BTreeMap<String, BookmarkGroup> = BTreeMap::new();
    for row in rows {
        let group = grouped.entry(row.name.clone()).or_default();
        match row.remote {
            None => {
                group.local = Some(LocalBookmark {
                    name: row.name,
                    commit_identifier: row.commit_identifier,
                    commit_timestamp_seconds: row.commit_timestamp_seconds,
                    has_remote: false,
                });
            }
            Some(remote) if remote != "git" => {
                group.remote_names.insert(remote);
            }
            Some(_) => {}
        }
    }

    for group in grouped.values_mut() {
        if let Some(local) = &mut group.local {
            local.has_remote = !group.remote_names.is_empty();
        }
    }
    grouped
}

fn render_repository_verification(
    verification: &RepositoryVerification,
    output: &mut impl Write,
) -> fmt::Result {
    match verification {
        RepositoryVerification::Scanned {
            repository,
            bookmarks,
        } => {
            writeln!(
                output,
                "{} ({}): {} open push-* bookmarks",
                repository.name,
                repository.path.display(),
                bookmarks.len()
            )?;
            render_bookmark_group(
                "delete candidates",
                bookmarks
                    .iter()
                    .filter(|bookmark| bookmark.delete_candidate()),
                output,
            )?;
            render_bookmark_group(
                "rebase-or-abandon candidates",
                bookmarks
                    .iter()
                    .filter(|bookmark| bookmark.rebase_or_abandon_candidate()),
                output,
            )?;
            render_bookmark_group(
                "local-only without clear home",
                bookmarks
                    .iter()
                    .filter(|bookmark| bookmark.local_only_without_home()),
                output,
            )?;
        }
        RepositoryVerification::Skipped { repository, reason } => {
            writeln!(
                output,
                "{} ({}): skipped ({})",
                repository.name,
                repository.path.display(),
                reason
            )?;
        }
        RepositoryVerification::Failed { repository, reason } => {
            writeln!(
                output,
                "{} ({}): failed ({})",
                repository.name,
                repository.path.display(),
                reason
            )?;
        }
    }
    Ok(())
}

fn render_bookmark_group<'a>(
    title: &str,
    bookmarks: impl Iterator<Item = &'a PushBookmark>,
    output: &mut impl Write,
) -> fmt::Result {
    let bookmarks: Vec<&PushBookmark> = bookmarks.collect();
    if bookmarks.is_empty() {
        return Ok(());
    }
    writeln!(output, "  {title}:")?;
    for bookmark in bookmarks {
        writeln!(
            output,
            "    {} {} ({} days old)",
            bookmark.name, bookmark.commit_identifier, bookmark.age_days
        )?;
    }
    Ok(())
}

fn unquote_code(cell: &str) -> &str {
    cell.strip_prefix('`')
        .and_then(|without_prefix| without_prefix.strip_suffix('`'))
        .unwrap_or(cell)
}

fn escape_revset_string(value: &str) -> String {
    value.replace('\\', "\\\\").replace('"', "\\\"")
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lockfile::LockEntry;

    #[test]
    fn active_repository_map_yields_absolute_paths_only() {
        let text = r#"
| Repository | Path | Current role |
|---|---|---|
| `primary` | `/home/li/primary` | Workspace coordination. |
| `lojix` | `github:LiGoldragon/lojix` | Replacement. |
| `chroma` | `/git/github.com/LiGoldragon/chroma` | Active. |
"#;

        let repositories = parse_tracked_repositories(text);
        assert_eq!(
            repositories,
            vec![
                TrackedRepository {
                    name: "primary".to_string(),
                    path: PathBuf::from("/home/li/primary"),
                },
                TrackedRepository {
                    name: "chroma".to_string(),
                    path: PathBuf::from("/git/github.com/LiGoldragon/chroma"),
                },
            ]
        );
    }

    #[test]
    fn bookmark_rows_group_local_and_real_remote_refs() {
        let rows = "\
push-alpha\t\tabc\t100\n\
push-alpha\tgit\tabc\t100\n\
push-beta\t\tdef\t200\n\
push-beta\torigin\tccc\t100\n";

        let grouped = parse_bookmark_rows(rows).expect("parse rows");
        let alpha = grouped.get("push-alpha").expect("alpha");
        assert!(!alpha.local.as_ref().expect("alpha local").has_remote);
        let beta = grouped.get("push-beta").expect("beta");
        assert!(beta.local.as_ref().expect("beta local").has_remote);
    }

    #[test]
    fn repositories_for_lock_matches_nested_claim_paths() {
        let repositories = vec![
            TrackedRepository {
                name: "primary".to_string(),
                path: PathBuf::from("/home/li/primary"),
            },
            TrackedRepository {
                name: "chroma".to_string(),
                path: PathBuf::from("/git/github.com/LiGoldragon/chroma"),
            },
        ];
        let lock = LockFile::new(vec![LockEntry {
            scope: NormalizedScope::from_raw(
                &crate::scope::RawScope::new("/home/li/primary/tools/orchestrate"),
                Path::new("/"),
            )
            .expect("path scope"),
            reason: None,
        }]);

        let matched = repositories_for_lock(&lock, &repositories);
        assert_eq!(matched, vec![repositories[0].clone()]);
    }
}
