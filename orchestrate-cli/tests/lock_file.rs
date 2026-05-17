use std::path::Path;

use orchestrate_cli::{LockEntry, LockFile, NormalizedScope};
use orchestrate_cli::scope::RawScope;

fn scope(raw: &str) -> NormalizedScope {
    NormalizedScope::from_raw(&RawScope::new(raw), Path::new("/")).unwrap()
}

#[test]
fn round_trip_preserves_scopes_and_reasons() {
    let lock = LockFile::new(vec![
        LockEntry {
            scope: scope("/home/li/primary/skills/foo.md"),
            reason: Some("syncing claim docs".to_string()),
        },
        LockEntry {
            scope: scope("[primary-68cb]"),
            reason: Some("rust port of tools/orchestrate".to_string()),
        },
    ]);

    let rendered = lock.render();
    let parsed = LockFile::parse(&rendered, "/tmp/test.lock").unwrap();
    assert_eq!(parsed, lock);
}

#[test]
fn rendering_matches_shell_format_byte_for_byte() {
    let lock = LockFile::new(vec![LockEntry {
        scope: scope("/home/li/primary/skills/foo.md"),
        reason: Some("syncing claim docs".to_string()),
    }]);
    assert_eq!(
        lock.render(),
        "/home/li/primary/skills/foo.md # syncing claim docs\n"
    );
}

#[test]
fn rendering_without_reason_omits_separator() {
    let lock = LockFile::new(vec![LockEntry {
        scope: scope("/home/li/primary/orchestrate"),
        reason: None,
    }]);
    assert_eq!(lock.render(), "/home/li/primary/orchestrate\n");
}

#[test]
fn blank_lines_and_comment_only_lines_are_dropped() {
    let raw = "\n# header comment\n/home/li/primary/skills/foo.md # reason\n\n# trailer\n";
    let lock = LockFile::parse(raw, "/tmp/test.lock").unwrap();
    assert_eq!(lock.entries().len(), 1);
    assert_eq!(
        lock.entries()[0].scope.lock_file_form(),
        "/home/li/primary/skills/foo.md"
    );
    assert_eq!(
        lock.entries()[0].reason.as_deref(),
        Some("reason")
    );
}

#[test]
fn missing_file_means_idle() {
    let lock = LockFile::read(Path::new("/tmp/does-not-exist.orchestrate.lock")).unwrap();
    assert!(lock.is_idle());
}
