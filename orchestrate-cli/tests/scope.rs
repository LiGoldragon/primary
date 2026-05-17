use std::path::Path;

use orchestrate_cli::NormalizedScope;
use orchestrate_cli::scope::RawScope;

#[test]
fn absolute_path_passes_through_unchanged() {
    let raw = RawScope::new("/home/li/primary/skills/foo.md");
    let normalized = NormalizedScope::from_raw(&raw, Path::new("/home/li")).unwrap();
    assert_eq!(
        normalized.lock_file_form(),
        "/home/li/primary/skills/foo.md"
    );
}

#[test]
fn relative_path_is_resolved_against_working_directory() {
    let raw = RawScope::new("primary/skills/foo.md");
    let normalized = NormalizedScope::from_raw(&raw, Path::new("/home/li")).unwrap();
    assert_eq!(
        normalized.lock_file_form(),
        "/home/li/primary/skills/foo.md"
    );
}

#[test]
fn parent_components_are_resolved_lexically() {
    let raw = RawScope::new("/home/li/primary/../primary/skills");
    let normalized = NormalizedScope::from_raw(&raw, Path::new("/home/li")).unwrap();
    assert_eq!(normalized.lock_file_form(), "/home/li/primary/skills");
}

#[test]
fn current_components_are_stripped() {
    let raw = RawScope::new("/home/li/./primary/./skills/./foo.md");
    let normalized = NormalizedScope::from_raw(&raw, Path::new("/home/li")).unwrap();
    assert_eq!(
        normalized.lock_file_form(),
        "/home/li/primary/skills/foo.md"
    );
}

#[test]
fn double_slashes_collapse() {
    let raw = RawScope::new("/home//li//primary//skills");
    let normalized = NormalizedScope::from_raw(&raw, Path::new("/home/li")).unwrap();
    assert_eq!(normalized.lock_file_form(), "/home/li/primary/skills");
}

#[test]
fn bracketed_task_token_yields_task_scope() {
    let raw = RawScope::new("[primary-68cb]");
    let normalized = NormalizedScope::from_raw(&raw, Path::new("/home/li")).unwrap();
    assert_eq!(normalized.lock_file_form(), "[primary-68cb]");
    matches!(normalized, NormalizedScope::Task(_));
}

#[test]
fn empty_brackets_fall_through_to_path_normalization() {
    // Matches the shell helper's permissive regex (`^\[.+\]$` rejects
    // empty brackets; everything else falls through to normal_path).
    // Encoded here as a witness so a future refactor that tightens
    // this surface lands an explicit decision rather than silent drift.
    let raw = RawScope::new("[]");
    let normalized = NormalizedScope::from_raw(&raw, Path::new("/home/li")).unwrap();
    assert_eq!(normalized.lock_file_form(), "/home/li/[]");
}

#[test]
fn task_token_with_inner_bracket_is_rejected() {
    let raw = RawScope::new("[primary-[bad]]");
    let result = NormalizedScope::from_raw(&raw, Path::new("/home/li"));
    assert!(result.is_err(), "{result:?}");
}

#[test]
fn escape_above_root_is_rejected() {
    let raw = RawScope::new("/../../etc/passwd");
    let result = NormalizedScope::from_raw(&raw, Path::new("/home/li"));
    assert!(result.is_err(), "{result:?}");
}
