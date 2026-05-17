use orchestrate_cli::NormalizedScope;
use orchestrate_cli::overlap::overlap;
use signal_persona_mind::{TaskToken, WirePath};

fn path(value: &str) -> NormalizedScope {
    NormalizedScope::Path(WirePath::from_absolute_path(value.to_string()).unwrap())
}

fn task(value: &str) -> NormalizedScope {
    NormalizedScope::Task(TaskToken::from_wire_token(value.to_string()).unwrap())
}

#[test]
fn equal_paths_overlap() {
    assert!(overlap(&path("/a/b"), &path("/a/b")));
}

#[test]
fn nested_path_overlaps_parent() {
    assert!(overlap(&path("/a/b"), &path("/a/b/c")));
    assert!(overlap(&path("/a/b/c"), &path("/a/b")));
}

#[test]
fn siblings_do_not_overlap() {
    assert!(!overlap(&path("/a/b"), &path("/a/c")));
}

#[test]
fn prefix_substring_is_not_path_overlap() {
    assert!(!overlap(&path("/a/bug"), &path("/a/b")));
}

#[test]
fn equal_tasks_overlap() {
    assert!(overlap(&task("primary-f99"), &task("primary-f99")));
}

#[test]
fn different_tasks_do_not_overlap() {
    assert!(!overlap(&task("primary-f99"), &task("primary-aaa")));
}

#[test]
fn mixed_kinds_never_overlap() {
    assert!(!overlap(&path("/a/b"), &task("primary-f99")));
    assert!(!overlap(&task("primary-f99"), &path("/a/b")));
}
