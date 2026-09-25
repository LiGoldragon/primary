# Flow 0.10.4: predecessor and remembered flows in a per-launch bundle

An Opus subflow of 38de5b did this on 2026-09-25. It follows the main-flow ruling: the one-line Claude first prompt no longer carries the LaunchProfile's Predecessor and Remembered flows, and they go into the system-prompt bundle, which is per launch.

- Repository: github.com/LiGoldragon/flow. The work was done in a fresh scratchpad clone (`flow-bundle-38de5b-q7`) based on d864f54 (0.10.3).
- Pushed to main: 84e2304d3861c96c7817fc4942d329d15c005f1d "Flow 0.10.4: predecessor and remembered flows go into a per-launch bundle". `git ls-remote origin main` returned 84e2304.
- Tests: 100 before (89+6+3+1+1) and 103 after (92+6+3+1+1), with 0 failed. `cargo clippy --all-targets` gives 0 warnings, and `cargo fmt --check` is clean. `nix flake check` was not run.
- Version rule, from the versioning skill: a public behaviour change updates the version surface. This change does not touch the wire, the storage, the argv shape or the signal-flow contract. The new internal `CompositionError::LaunchBundleUnwritable` maps onto the existing `CompositionRefused`. That makes it a patch: 0.10.4. Cargo.toml, Cargo.lock, flake.nix, UPGRADES.md and README.md were updated.
- Orchestrate lock 6494 was taken and released.

## What changed

- `composition::LaunchBundles` holds the directory for per-launch copies: `~/.local/state/flow/launch-bundles/` (`DefaultConfiguration::launch_bundle_directory`). `file_for(profile)` gives `launch-<short>.md`, where `<short>` is the 8-hex launch-request short form that the remote-control name also uses.
  - Two tests constrain the name. `composed_prompt_carries_no_hash_request_id_or_source_text` forbids the request ID and any hex run of 16 or more. `claude_launch_records_its_remote_control_flag` forbids the `flow-<short>` name in the body.
- `RendersLaunchSection for LaunchProfile` builds the section. It emits `Predecessor: <flow-id>\n` when `flow_id_option` is Some, and `Remembered: <id>, <id>\n` when the list is non-empty. The IDs are listed without their depth, as the brief says. Otherwise it emits nothing.
- For Claude, the composer writes the copy at compose time, which is Start. The copy holds the caller's raw bytes. If there is a section, a newline is added when the file lacks one, then a blank line, then the section. When there is no section, the copy is byte-identical to the caller's file. The write goes to a temp file and is then renamed. The one-line prompt says `Read <copy> for your launch mode`.
- `HerdrCli` holds the same `LaunchBundles` (`with_launch_bundles`) and passes `--system-prompt-file <copy>`. `RunningNexus::open` builds one `LaunchBundles` and gives it to both the composer and HerdrCli.
- For Codex, the trimmed bundle text gets `\n\n` plus the section at its end, and that text still opens the first block. No file is written for Codex.
- The profile stored in `ComposedLaunch` is unchanged, so the idempotent re-Start comparison still holds.

## Fixtures

- `claude_launch_copy_carries_predecessor_and_remembered_and_leaves_the_caller_bundle` checks five things:
  - the copy is at its own path;
  - its content is exactly `fixture bundle\n\nPredecessor: 1b8ac0\nRemembered: 836818, 2c4f10\n`;
  - the caller's bytes are unchanged;
  - the line names the copy, not the caller's file, and contains no Predecessor or Remembered;
  - `ClaudeFirstLine::fits` holds and the prompt is canonical.
- `launch_copy_and_codex_bundle_carry_no_section_when_nothing_is_remembered`: when both fields are unset, the copy equals the caller's file byte for byte, and the Codex block goes straight from the bundle to `$spirit`.
- `launch_copy_keeps_a_section_on_its_own_lines_after_a_trailing_newline`.
- Updated tests:
  - The Codex expected-block tests now include the section.
  - The Claude head-commands test now names the copy.
  - The Herdr argv test now expects `--system-prompt-file <copy>` and checks that the copy differs from the caller's path.
- `claude_line_at_the_limit_is_kept_and_one_past_it_is_refused` is unchanged and green.

## Open, and not witnessed

- There has been no live Start. Nobody has watched Claude read the copy.
- Codex's `# Flow launch` block still carries its own `Predecessor:` and `Remembered flows: id@depth` lines, so the information appears twice. The ruling did not ask for their removal.
- Copies are never pruned; one small file accumulates per Claude launch.
- The 8-hex short form could collide across launch requests, and a collision would overwrite the other launch's copy. The remote-control name carries the same risk.
