# Flow 0.10.7: receipt after ambiguity, routes keyed on ids, argv deduped

An Opus subflow of 38de5b did this on 2026-09-25. It covers the three faults Psyche Medium e51411 saw on the first real Flow Start: successor PsycheV2.{ Opus 88475f }, launched through Flow 0.10.5.

- Repository: github.com/LiGoldragon/flow. The work was done in a fresh clone in the scratchpad (`flow-0107-38de5b-q9`).
- Main moved to 0.10.6 (a1a5175, 5b59761) while I worked, and I rebased onto it.
- Revision pushed to main: 8df890ba1bc34a9bd575e75ab4796b4e0dc7b0fd, "Flow 0.10.7: receipt promotes after ambiguity, routes keyed on ids, argv deduped". `git ls-remote origin main` returned 8df890b.
- Tests:
  - Before, on 5e1382f: 6+3+94+1+1.
  - Before, on the rebased base 5b59761: 6+3+99+1+1.
  - After: 6+3+102+1+1, with 0 failed.
- `cargo clippy --all-targets` shows 0 warnings, and `cargo fmt --check` is clean.
- Version rule, from the versioning skill: a public behaviour change updates the version surface. Here the observer, route and argv behaviour changed. The signal-flow wire and the store schema did not: there is no new record kind and no new field. 0.10.7 is therefore the next patch after 0.10.6. Cargo.toml, Cargo.lock, flake.nix, UPGRADES.md and DESIGN.md were updated.
- Local `nix build` (`--option builders '' --option substituters https://cache.nixos.org --option max-jobs auto`): ok, `/nix/store/shql7ivn3qrg0b964dqlcj6y6cnypmc8-flow-0.10.7`, and its `flow-nexus --version` prints `flow-nexus 0.10.7`.
- Orchestrate lock 6585 was taken and released.

## Live evidence

- Launch request `psyche-opus-successor-e51411-1`. It was found in e51411's transcript, in the Start datom and its StartAmbiguous reply.
- `flow 'LaunchStatus.psyche-opus-successor-e51411-1'` answers `LaunchPending`, phase `PromptAmbiguous`. Its details:
  - skills main-flow (119d98a9…) and refresh (07b97916…); both files still hash the same;
  - agent `claude-86b6e54cb9618d95d6d8ceaa`, w17, w17:p1, term_65c5883e612c88a;
  - boundary `Existing.{ dev 66306, inode 54141100, offset 2920, prefix 827699c4… }`. The current file's first 2920 bytes still hash to 827699c4…, so the cursor is intact.
- Transcript `~/.claude/projects/-home-li-primary/88475fd7-e328-4e11-9094-db2139a08fe0.jsonl` (Claude Code 2.1.280). The line numbers below are its records:
  - 13: the `/main-flow` command record. It carries `stackedOriginalInput` = `/main-flow /refresh <arg>`. The body hash matches the intent's ad31b16a…, and the line is 793 UTF-16 units long.
  - 14: the expansion (isMeta, turnCompanion), ending `ARGUMENTS: <arg>`.
  - 22: the `/refresh` command record (stackedExpansion true, turnOrigin human), with the same argument.
  - 23: its expansion.
  - 43: Read of the bundle.
  - 45–104: thirteen Skill-tool loads the instruction asked for (spirit … metaflow). Two of them, herdr and file-editing, were in one assistant turn, at 82–83.
  - 115–148: Bash, Agent and Read work.
  - 150: the assistant `FLOW_LAUNCH_RECEIPT_V2` (uuid 2a04ed93…, model claude-opus-5-5, effort medium).
- **Why it stayed ambiguous.** The observer confirmed the stacked commands and both expansions. At line 45 it then met a Skill `tool_use` with `skill_index == len(selection)` and returned Err "native Claude Skill invocation order differs from intent". `promote_ambiguous` maps an Err to Ambiguous. In 0.10.5 promotion also runs only on a repeated Start or on an open `Observe.Launch`, and e51411 did neither.
- **A second blocker.** `verify_native_target` ran `herdr agent get <launch agent name>` and matched the name. The child had renamed its agent: `herdr agent get claude-86b6e54c…` now answers `agent_not_found`, while `agent get w17:p1` answers with name `psyche-opus-88475f`. Even a correct observer would have stayed ambiguous.
- **Argv.** `herdr pane process-info --pane w17:p1` shows `claude --dangerously-skip-permissions --dangerously-skip-permissions --settings … --remote-control flow-4db1ff116af254cf …`. The installed `claude` (claude-code-2.1.280 wrapper) execs `.claude-wrapped --dangerously-skip-permissions "$@"`, and Flow added its own copy.
- **Live replay.** A throwaway ignored test, not committed, ran the 0.10.7 `observe_native_target_receipt` with this exact stored intent against the real transcript and real Herdr (read-only `agent get w17:p1`). It returned `Observed`, native turn 2a04ed93-95e9-4f91-b9ce-4cc43b73bc48.

## Changes

1. **Receipt after ambiguity** (launching.rs, store.rs, main.rs).
   - `PromotesAmbiguousLaunches::promote_ambiguous_launches` runs on its own thread in flow-nexus from startup. It reads `ambiguous_launch_attempts()`, meaning PromptAmbiguous with no outcome, and opens one `TranscriptWatch` per launch.
   - It looks at each launch once, then again on every change to that launch's transcript, and calls `promote_serially`. That runs under the dispatch gate, then `settle`.
   - It waits on `LaunchChanges` (the Condvar) and never on a timer.
   - Observe.Launch is unchanged and still promotes on its own watch.
   - The observer also changed. Once the first turn and every selected skill are confirmed, only the receipt is looked for, so later Skill loads, work and notices are ignored. An isMeta plain-text user row is never read as typed input.
2. **Routes** (herdr.rs, herdr/launch.rs).
   - `agent_matches_binding` matches pane id, terminal id and harness. The session is the snapshot's own, and the name is not matched.
   - `ReadsHerdrRoster::current_route` returns the route carrying the live agent name, and `refresh_route` reports it. ResolveRecipient, Send and Stop therefore see the new name.
   - `verify_native_target` targets `agent get <pane id>` and checks workspace, pane, terminal and native session.
   - Launch-time `agent start`, `agent get`, the `/rename` prompt and the first prompt still use the launch name, which is current at that moment.
3. **Argv** (herdr/launch.rs). Flow no longer pushes `--dangerously-skip-permissions`. `--settings '{"permissions":{"defaultMode":"bypassPermissions"}}'` stays.

Fixtures:
- `claude_receipt_after_further_skill_loads_and_work_is_observed`. It uses the 88475f shape: rename notice, two stacked records with their flags, attachments, Read, four extra Skill loads (two in one turn), Bash, a plain assistant line, then the receipt, which reaches Observed. It was witnessed failing with the new guard disabled.
- `a_receipt_after_ambiguity_promotes_with_no_subscriber_and_no_second_start`. The promoter thread, the transcript write and LaunchStatus together reach Started, with no `agent prompt` and no `pane create`. It was witnessed failing without the promoter.
- `a_renamed_agent_keeps_its_route_and_reports_its_current_name`. It registers, renames to `psyche-opus-88475f`, and `ResolveRecipient` stays Available with the new name and the same session, pane and terminal. `route_is_available` is true, and `pane_presence` is Present.
- The stale-route test now varies terminal, pane, harness and interactive. The name was dropped from it.
- The Claude argv fixture asserts each `--` flag once in the pane argv, meaning the wrapper's prefix plus Flow's arguments.

## `flow 'List.{}'` for 88475f (fix not deployed; the unit was not touched)

```
{ 88475f 88475fd7-e328-4e11-9094-db2139a08fe0 Claude Unavailable Available.{ messaging-build claude-86b6e54cb9618d95d6d8ceaa w17:p1 term_65c5883e612c88a } { e51411 e5141130-9a4a-4b8f-b405-67d941a7b320 handover-successor } Pending }
```

The running Nexus is 0.10.5 (`flow --version`), and LaunchStatus is still `PromptAmbiguous`. This is unchanged.

## Open, and not witnessed

- There is no live promotion yet. It needs 0.10.7 activated, which is Field Sol b7da5d's call. On its first startup pass the promoter should look at this launch once and promote it; the replay above predicts `Observed`.
  - That depends on main-flow/SKILL.md and refresh/SKILL.md keeping the hashes stored in the intent. A regeneration that changes either file before activation makes the observer refuse it as "native skill source changed", and the launch stays ambiguous.
  - 88475f is not a replacement launch, so promotion records `Started` and nothing is reaped.
- The Pending → Active promotion of the Flow row still needs an ordinary Send marker. LaunchStatus becoming Started does not make the List lifecycle Active.
- The promoter re-reads an ambiguous transcript on every change until it settles. A launch whose observer refuses for good, and whose flow keeps working, is re-read on each write. That costs work, but it is not a loop.
- The argv dedupe assumes the installed `claude` prepends the flag. On a host whose `claude` does not, Flow's launch runs in settings bypass mode without the flag. That was read from code and has not been witnessed.
- The stored route's agent name stays the launch name in the store. Only resolution reports the live name, and no store write was added.
