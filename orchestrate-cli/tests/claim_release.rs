use std::fs;
use std::path::{Path, PathBuf};

use orchestrate_cli::claim::{self, ClaimOutcome};
use orchestrate_cli::registry::LaneRegistry;
use orchestrate_cli::scope::RawScope;
use orchestrate_cli::{Lane, LockFile, Workspace};
use tempfile::TempDir;

const REGISTRY: &str = r#"operator
operator-assistant                assistant-of:operator
second-operator-assistant         assistant-of:operator
designer
designer-assistant                assistant-of:designer
second-designer-assistant         assistant-of:designer
system-specialist
system-assistant                  assistant-of:system-specialist
second-system-assistant           assistant-of:system-specialist
poet
poet-assistant                    assistant-of:poet
"#;

struct Fixture {
    _temp: TempDir,
    workspace: Workspace,
    registry: LaneRegistry,
}

impl Fixture {
    fn new() -> Self {
        let temp = tempfile::tempdir().expect("tempdir");
        let workspace = Workspace::new(temp.path());
        fs::create_dir_all(workspace.orchestrate_dir()).unwrap();
        fs::write(workspace.role_registry(), REGISTRY).unwrap();
        let registry =
            LaneRegistry::load(workspace.role_registry()).expect("registry load");
        Self {
            _temp: temp,
            workspace,
            registry,
        }
    }

    fn workspace_path(&self) -> &Path {
        self.workspace.root()
    }

    fn under_root(&self, relative: &str) -> String {
        let mut path = PathBuf::from(self.workspace.root());
        path.push(relative);
        path.to_string_lossy().into_owned()
    }

    fn read_lock(&self, lane: Lane) -> String {
        match fs::read_to_string(self.workspace.lock_path(lane)) {
            Ok(text) => text,
            Err(_) => String::new(),
        }
    }
}

#[test]
fn claim_writes_lock_file_in_shell_format() {
    let fixture = Fixture::new();
    let scope_text = fixture.under_root("skills/foo.md");
    let outcome = claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Operator,
        vec![RawScope::new(scope_text.clone())],
        "syncing claim docs",
        fixture.workspace_path(),
    )
    .expect("claim succeeds");
    assert!(matches!(outcome, ClaimOutcome::Accepted { .. }));

    let lock_text = fixture.read_lock(Lane::Operator);
    assert_eq!(
        lock_text,
        format!("{scope_text} # syncing claim docs\n")
    );
}

#[test]
fn release_clears_the_lock_file() {
    let fixture = Fixture::new();
    let scope_text = fixture.under_root("skills/foo.md");
    claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Operator,
        vec![RawScope::new(scope_text)],
        "syncing",
        fixture.workspace_path(),
    )
    .expect("claim");
    claim::release(&fixture.workspace, Lane::Operator).expect("release");
    let lock = LockFile::read(&fixture.workspace.lock_path(Lane::Operator)).unwrap();
    assert!(lock.is_idle());
}

#[test]
fn second_claim_on_overlapping_path_is_rejected_and_rolled_back() {
    let fixture = Fixture::new();
    let path = fixture.under_root("skills/foo.md");

    claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Operator,
        vec![RawScope::new(path.clone())],
        "first claim",
        fixture.workspace_path(),
    )
    .expect("first claim");

    let outcome = claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Designer,
        vec![RawScope::new(path.clone())],
        "second claim",
        fixture.workspace_path(),
    )
    .expect("second claim returns Ok");

    match outcome {
        ClaimOutcome::Rejected { overlaps, .. } => {
            assert_eq!(overlaps.len(), 1);
            assert_eq!(overlaps[0].own_lane, Lane::Designer);
            assert_eq!(overlaps[0].peer_lane, Lane::Operator);
        }
        ClaimOutcome::Accepted { .. } => panic!("expected rejection on overlap"),
    }

    // Designer's lock should be cleared after rollback.
    let designer_lock = LockFile::read(&fixture.workspace.lock_path(Lane::Designer)).unwrap();
    assert!(designer_lock.is_idle());

    // Operator's lock survives untouched.
    let operator_lock = LockFile::read(&fixture.workspace.lock_path(Lane::Operator)).unwrap();
    assert!(!operator_lock.is_idle());
}

#[test]
fn task_lock_overlaps_only_on_exact_match() {
    let fixture = Fixture::new();

    claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Operator,
        vec![RawScope::new("[primary-68cb]")],
        "rust port",
        fixture.workspace_path(),
    )
    .expect("first claim");

    let conflict = claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Designer,
        vec![RawScope::new("[primary-68cb]")],
        "review",
        fixture.workspace_path(),
    )
    .expect("conflict claim");
    assert!(matches!(conflict, ClaimOutcome::Rejected { .. }));

    let non_conflict = claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Designer,
        vec![RawScope::new("[primary-different]")],
        "review",
        fixture.workspace_path(),
    )
    .expect("non-conflict claim");
    assert!(matches!(non_conflict, ClaimOutcome::Accepted { .. }));
}

#[test]
fn mixed_kinds_do_not_overlap() {
    let fixture = Fixture::new();
    let path = fixture.under_root("skills/foo.md");

    claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Operator,
        vec![RawScope::new(path)],
        "path claim",
        fixture.workspace_path(),
    )
    .expect("path claim");

    let task_claim = claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Designer,
        vec![RawScope::new("[primary-68cb]")],
        "task claim",
        fixture.workspace_path(),
    )
    .expect("task claim");
    assert!(matches!(task_claim, ClaimOutcome::Accepted { .. }));
}

#[test]
fn beads_scope_is_rejected_as_a_path() {
    let fixture = Fixture::new();
    let beads_path = fixture.under_root(".beads");
    fs::create_dir_all(&beads_path).unwrap();

    let result = claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Operator,
        vec![RawScope::new(beads_path)],
        "claim beads",
        fixture.workspace_path(),
    );

    assert!(result.is_err(), "{result:?}");
    let message = format!("{}", result.unwrap_err());
    assert!(message.contains("BEADS"), "{message}");
}

#[test]
fn status_lists_every_lane_in_registry_order() {
    let fixture = Fixture::new();
    let path = fixture.under_root("skills/foo.md");
    claim::claim(
        &fixture.workspace,
        &fixture.registry,
        Lane::Operator,
        vec![RawScope::new(path)],
        "syncing",
        fixture.workspace_path(),
    )
    .expect("claim");

    let report = claim::status(&fixture.workspace, &fixture.registry).expect("status");
    let lanes: Vec<Lane> = report.lanes.iter().map(|status| status.lane).collect();
    assert_eq!(
        lanes,
        vec![
            Lane::Operator,
            Lane::OperatorAssistant,
            Lane::SecondOperatorAssistant,
            Lane::Designer,
            Lane::DesignerAssistant,
            Lane::SecondDesignerAssistant,
            Lane::SystemSpecialist,
            Lane::SystemAssistant,
            Lane::SecondSystemAssistant,
            Lane::Poet,
            Lane::PoetAssistant,
        ]
    );
    let operator_status = report
        .lanes
        .iter()
        .find(|status| status.lane == Lane::Operator)
        .expect("operator status");
    assert!(!operator_status.lock.is_idle());
}
