//! Overlap detection — matches the shell helper's `scopes_overlap`.
//!
//! Two scopes overlap iff they're the same kind AND collide:
//! - Path vs path: nested or equal.
//! - Task vs task: exact-match on the bracketed token.
//! - Mixed kinds: never overlap.

use std::path::Path;

use crate::scope::NormalizedScope;

pub fn overlap(left: &NormalizedScope, right: &NormalizedScope) -> bool {
    match (left, right) {
        (NormalizedScope::Path(left), NormalizedScope::Path(right)) => {
            path_overlap(left.as_str(), right.as_str())
        }
        (NormalizedScope::Task(left), NormalizedScope::Task(right)) => left.as_str() == right.as_str(),
        _ => false,
    }
}

fn path_overlap(left: &str, right: &str) -> bool {
    if left == right {
        return true;
    }
    let left_path = Path::new(left);
    let right_path = Path::new(right);
    left_path.starts_with(right_path) || right_path.starts_with(left_path)
}

// Tests live in `tests/overlap.rs` per skills/rust/crate-layout.md.
