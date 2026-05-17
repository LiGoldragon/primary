//! `tools/orchestrate` binary entry point.
//!
//! Argv surface (matches the shell helper):
//! ```text
//! orchestrate claim <lane> <scope> [more-scopes] -- <reason>
//! orchestrate release <lane>
//! orchestrate status
//! ```
//! Lock files land at `<workspace>/orchestrate/<lane>.lock` in the
//! existing format. The typed [`signal_persona_mind::MindRequest`]
//! projection is constructed for every flow; once `persona-mind` is
//! the canonical store the binary forwards the typed request to its
//! socket instead of writing the lock file directly.

use std::env;
use std::path::{Path, PathBuf};
use std::process::ExitCode;

use std::io::Write;
use std::process::Command;
use std::process::Stdio;

use orchestrate_cli::claim::{self, ClaimOutcome};
use orchestrate_cli::lane::Lane;
use orchestrate_cli::registry::LaneRegistry;
use orchestrate_cli::render;
use orchestrate_cli::scope::RawScope;
use orchestrate_cli::workspace::Workspace;

const EXIT_USAGE: u8 = 64;
const EXIT_CONFLICT: u8 = 2;
const EXIT_ERROR: u8 = 70;

fn main() -> ExitCode {
    let arguments: Vec<String> = env::args().skip(1).collect();
    match run(arguments) {
        Ok(code) => ExitCode::from(code),
        Err(message) => {
            eprintln!("{message}");
            ExitCode::from(EXIT_ERROR)
        }
    }
}

fn run(arguments: Vec<String>) -> Result<u8, String> {
    let workspace = locate_workspace().map_err(stringify)?;
    let registry =
        LaneRegistry::load(workspace.role_registry()).map_err(stringify)?;
    let working_directory = env::current_dir()
        .map_err(|error| format!("could not read current working directory: {error}"))?;

    let mut arguments = arguments.into_iter();
    let subcommand = arguments.next().unwrap_or_default();

    match subcommand.as_str() {
        "claim" => handle_claim(&workspace, &registry, arguments, &working_directory),
        "release" => handle_release(&workspace, &registry, arguments),
        "status" => handle_status(&workspace, &registry),
        "-h" | "--help" | "help" | "" => {
            print!("{}", usage(&registry));
            Ok(0)
        }
        _ => {
            eprint!("{}", usage(&registry));
            Ok(EXIT_USAGE)
        }
    }
}

fn handle_claim(
    workspace: &Workspace,
    registry: &LaneRegistry,
    mut arguments: std::vec::IntoIter<String>,
    working_directory: &Path,
) -> Result<u8, String> {
    let lane_token = arguments
        .next()
        .ok_or_else(|| usage(registry))?;
    let lane = Lane::from_token(&lane_token).map_err(stringify)?;

    let mut scopes = Vec::new();
    let mut reason_parts: Vec<String> = Vec::new();
    let mut consuming_reason = false;
    for argument in arguments {
        if !consuming_reason && argument == "--" {
            consuming_reason = true;
            continue;
        }
        if consuming_reason {
            reason_parts.push(argument);
        } else {
            scopes.push(RawScope::new(argument));
        }
    }

    if scopes.is_empty() {
        eprint!("{}", usage(registry));
        return Ok(EXIT_USAGE);
    }
    let reason = reason_parts.join(" ");

    let outcome = claim::claim(workspace, registry, lane, scopes, &reason, working_directory)
        .map_err(stringify)?;
    let report = claim::status(workspace, registry).map_err(stringify)?;

    let mut lock_state = String::new();
    render::render_lock_state(&report, &mut lock_state)
        .map_err(|error| format!("render error: {error}"))?;
    print!("{lock_state}");
    let _ = std::io::stdout().flush();
    run_beads_listing(workspace);

    let mut conflict_stderr = String::new();
    let mut conflict_stdout = String::new();
    render::render_outcome_claim_conflicts(&outcome, &mut conflict_stderr, &mut conflict_stdout)
        .map_err(|error| format!("render error: {error}"))?;
    if !conflict_stderr.is_empty() {
        eprint!("{conflict_stderr}");
    }
    if !conflict_stdout.is_empty() {
        // The shell helper re-prints state after rolling back; mirror
        // that here so the cleared lock surfaces in the same stream.
        let cleared_report = claim::status(workspace, registry).map_err(stringify)?;
        let mut cleared_lock_state = String::new();
        render::render_lock_state(&cleared_report, &mut cleared_lock_state)
            .map_err(|error| format!("render error: {error}"))?;
        print!("{conflict_stdout}{cleared_lock_state}");
        let _ = std::io::stdout().flush();
        run_beads_listing(workspace);
    }

    if matches!(outcome, ClaimOutcome::Rejected { .. }) {
        Ok(EXIT_CONFLICT)
    } else {
        Ok(0)
    }
}

fn handle_release(
    workspace: &Workspace,
    registry: &LaneRegistry,
    mut arguments: std::vec::IntoIter<String>,
) -> Result<u8, String> {
    let lane_token = arguments
        .next()
        .ok_or_else(|| usage(registry))?;
    if arguments.next().is_some() {
        eprint!("{}", usage(registry));
        return Ok(EXIT_USAGE);
    }
    let lane = Lane::from_token(&lane_token).map_err(stringify)?;
    let _outcome = claim::release(workspace, lane).map_err(stringify)?;
    let report = claim::status(workspace, registry).map_err(stringify)?;
    let mut lock_state = String::new();
    render::render_lock_state(&report, &mut lock_state)
        .map_err(|error| format!("render error: {error}"))?;
    print!("{lock_state}");
    let _ = std::io::stdout().flush();
    run_beads_listing(workspace);
    Ok(0)
}

fn handle_status(workspace: &Workspace, registry: &LaneRegistry) -> Result<u8, String> {
    let report = claim::status(workspace, registry).map_err(stringify)?;
    let mut lock_state = String::new();
    render::render_lock_state(&report, &mut lock_state)
        .map_err(|error| format!("render error: {error}"))?;
    print!("{lock_state}");
    let _ = std::io::stdout().flush();
    run_beads_listing(workspace);
    Ok(0)
}

fn run_beads_listing(workspace: &Workspace) {
    if !workspace.beads_root().exists() {
        println!("No BEADS database found.");
        return;
    }
    let status = Command::new("bd")
        .args([
            "--readonly",
            "list",
            "--status",
            "open",
            "--flat",
            "--no-pager",
            "--limit",
            "20",
        ])
        .current_dir(workspace.root())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .status();
    match status {
        Ok(exit) if !exit.success() => {
            println!("BEADS open-task check failed.");
        }
        Err(_) => {
            println!("BEADS open-task check failed.");
        }
        _ => {}
    }
}

fn locate_workspace() -> Result<Workspace, String> {
    if let Ok(explicit) = env::var("ORCHESTRATE_WORKSPACE_ROOT") {
        let root = PathBuf::from(explicit);
        if !root.join("orchestrate").join("roles.list").exists() {
            return Err(format!(
                "ORCHESTRATE_WORKSPACE_ROOT={} does not contain orchestrate/roles.list",
                root.display()
            ));
        }
        return Ok(Workspace::new(root));
    }

    let binary_path = env::current_exe()
        .map_err(|error| format!("could not resolve current executable: {error}"))?;
    let mut probe = binary_path.parent().map(Path::to_path_buf);
    while let Some(candidate) = probe {
        if candidate.join("orchestrate").join("roles.list").exists() {
            return Ok(Workspace::new(candidate));
        }
        probe = candidate.parent().map(Path::to_path_buf);
    }

    Err("could not locate workspace root (no ancestor of the binary contains orchestrate/roles.list). Set ORCHESTRATE_WORKSPACE_ROOT to override.".to_string())
}

fn stringify<T: std::fmt::Display>(value: T) -> String {
    value.to_string()
}

fn usage(registry: &LaneRegistry) -> String {
    let lanes: Vec<String> = registry
        .lanes()
        .map(|lane| lane.as_token().to_string())
        .collect();
    format!(
        r#"Usage:
  tools/orchestrate claim <role> <scope> [more-scopes] -- <reason>
  tools/orchestrate release <role>
  tools/orchestrate status

Roles: {roles}

Scopes: each <scope> is either
  - an absolute path:    /home/li/primary/skills/foo.md
  - a task lock:         '[primary-f99]'      (quote in shell)

Lock files (orchestrate/<role>.lock) are plain text. Empty file means idle.
Each line is one scope, optionally followed by ` # <reason>`.
"#,
        roles = lanes.join(", ")
    )
}
