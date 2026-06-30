# Verifier Ledger

Task: adversarial verification for epic `primary-5rzf`, bead `primary-5rzf.4`.

Scope: verified the Phase-1 sweep outputs in:

- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md`
- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/TrackerSweep-Candidates.md`
- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/DocsSkillsSweep-Candidates.md`
- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/CodeSweep-Candidates.md`

Rules applied: a confirmed entry names the new thing, old thing, locator, and evidence. Evidence is a rename, finished effort still described as active, explicit deprecate/replace/supersede statement, or landed work making the old shape dead. Items missing a part or requiring a psyche/private ruling are suspects/unresolved. Items with live remaining scope or compatibility evidence are rejected/not stale. No Spirit intent records or `/home/li/primary/private-repos` were inspected.

## CONFIRMED FOR TRACKER KILL (.5)

### T1. `primary-xj51` finished-but-open offline first-e2e integration

- New thing: offline first-e2e stack and criome Part 1 mainlined across `spirit`, `mirror`, `meta-signal-spirit`, `router`, `signal-router`, `signal-criome`, and `criome`.
- Old thing it killed: open tracker task `primary-xj51` to integrate that stack to main.
- Locator: `primary-xj51`.
- Evidence: `bd --readonly show primary-xj51 --long --json` shows status `open`, while notes say the 5-branch offline-e2e stack and criome Part 1 are mainlined and "Status lags reality"; comments record 2026-06-17 mainline commits and green verification, with only a network-only Nix fetch caveat.
- Original source file: `TrackerSweep-Candidates.md`, candidate 1.
- Recommended kill bead: `.5`.

### T2. `primary-hj4.1.4` legacy `persona-mind` subscription child

- New thing: `mind` rename plus the schema-emission porting plan for stateful persona runtimes; live deltas landed through `SubscriptionSupervisor`.
- Old thing it killed: `persona-mind` post-commit graph subscription delta delivery tracker child.
- Locator: `primary-hj4.1.4`.
- Evidence: `bd --readonly show primary-hj4.1.4 primary-0m1u.1 --long --json` shows the child still `in_progress` with `repo:persona-mind`; parent `primary-hj4.1` is closed as superseded by the schema-emission porting plan; child comments say commits `c4a80e83` and `5f5870fc` landed and verified typed live deltas; `primary-0m1u.1` close reason says `persona-mind`, `signal-persona-mind`, and `owner-signal-persona-mind` were renamed to `mind`, `signal-mind`, and `owner-signal-mind`.
- Original source file: `TrackerSweep-Candidates.md`, candidate 2.
- Recommended kill bead: `.5`.

### T3. `primary-uq04.2` wholesale terminal `signal_cli!` migration child

- New thing: schema-emission macro work through `nota-next` / `schema-next` / `schema-rust-next`, with narrower contract-foundation migration before generated CLI work.
- Old thing it killed: blocked task to migrate all nine `persona-terminal` binaries wholesale to `signal_cli!`.
- Locator: `primary-uq04.2`.
- Evidence: `bd --readonly show primary-uq04.2 primary-uq04 --long --json` shows child status `blocked`; parent `primary-uq04` is closed as superseded by the schema-emission pivot; the child audit says the bead is too broad and "Do not replace the 9 binaries wholesale with signal_cli!".
- Original source file: `TrackerSweep-Candidates.md`, candidate 3.
- Recommended kill bead: `.5`.

### T4. `primary-uq04.3` `message_validate_output` `signal_cli!` child

- New thing: schema-emission macro work through `nota-next` / `schema-next` / `schema-rust-next`, with contract-foundation migration and owner-boundary definition first.
- Old thing it killed: blocked task to migrate `persona-message` `message_validate_output` to `signal_cli!`.
- Locator: `primary-uq04.3`.
- Evidence: `bd --readonly show primary-uq04.3 primary-uq04 --long --json` shows child status `blocked`; parent `primary-uq04` is closed as superseded; child audit says `message_validate_output` is a validator, not a daemon thin-client CLI, and says not to replace it with `signal_cli!`.
- Original source file: `TrackerSweep-Candidates.md`, candidate 4.
- Recommended kill bead: `.5`.

### T5. `primary-uq04.4` Nexus parse/render `signal_cli!` child

- New thing: a separate Nexus architecture decision for standalone translator tools or a future `signal-nexus` triad contract/daemon client surface.
- Old thing it killed: blocked task to migrate Nexus `parse` and `render` binaries to `signal_cli!`.
- Locator: `primary-uq04.4`.
- Evidence: `bd --readonly show primary-uq04.4 primary-uq04 --long --json` shows child status `blocked`; parent `primary-uq04` is closed as superseded; child audit says `nexus-parse` and `nexus-render` are standalone stdin/stdout translators, not daemon clients, and names the replacement decision surface.
- Original source file: `TrackerSweep-Candidates.md`, candidate 5.
- Recommended kill bead: `.5`.

### T6. `primary-2chb` redirected persona-orchestrate deploy bead

- New thing: second-designer 162 consolidation plus the schema-emission porting plan for persona-stack runtimes.
- Old thing it killed: open deployment bead rooted in retired `/151` persona-orchestrate readiness/deploy framing.
- Locator: `primary-2chb`.
- Evidence: `bd --readonly show primary-2chb primary-c620 --long --json` shows `primary-2chb` still `open` while its notes redirect from retired `/151`; blocker `primary-c620` is closed as superseded by the schema-emission porting plan.
- Original source file: `TrackerSweep-Candidates.md`, candidate 6.
- Recommended kill bead: `.5`.

## CONFIRMED FOR DOCS KILL (.6)

### D1. `mind` replaced `persona-mind`

- New thing: `mind`.
- Old thing it killed: `persona-mind` as component/name in docs and generated skill prose.
- Locator: `/home/li/primary/INTENT.md:121-126`; `/home/li/primary/ARCHITECTURE.md:67-68`; `/home/li/primary/orchestrate/AGENTS.md:19-21` and `:403-407`; `/home/li/primary/repos/skills/modules/rust-crate-layout/full.md:34-36`; generated mirrors at `/home/li/primary/.agents/skills/rust-crate-layout/SKILL.md:39-41` and `/home/li/primary/.claude/skills/rust-crate-layout/SKILL.md:39-41`.
- Evidence: handoff explicitly says "`persona-mind` is a dead name -- the thing is `mind` now"; `primary-0m1u.1` close reason independently confirms the rename shipped.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C1.
- Recommended kill bead: `.6`.

### D2. `signal-mind` replaced `signal-persona-mind`

- New thing: `signal-mind`.
- Old thing it killed: `signal-persona-mind`.
- Locator: `/home/li/primary/orchestrate/AGENTS.md:347-350` and `:367-368`.
- Evidence: `bd --readonly show primary-0m1u.1 --long --json` close reason says `signal-persona-mind` was renamed to `signal-mind`; `/home/li/primary/protocols/active-repositories.md:64` lists `signal-mind`; `/git/github.com/LiGoldragon/signal-mind` exists and `/git/github.com/LiGoldragon/signal-persona-mind` is missing.
- Original source file: `DocsSkillsSweep-Candidates.md`, suspect S1 promoted after independent rename check.
- Recommended kill bead: `.6`.

### D3. Daemon-backed `orchestrate` replaced argv-compatible helper/crate

- New thing: daemon-backed `orchestrate` component CLI and `meta-orchestrate`.
- Old thing it killed: `tools/orchestrate` argv helper, local `orchestrate-cli/` compatibility crate, and old `claim <role> <scope> -- <reason>` shell grammar.
- Locator: `/home/li/primary/orchestrate/ARCHITECTURE.md:5-16` and `:101-116`; `/home/li/primary/orchestrate/AGENTS.md:153-176`.
- Evidence: architecture line 16 says the helper/crate are retired; line 103 says the compatibility layer is deprecated; AGENTS lines 174-176 say the old helper is retired and should not be relied on.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C2.
- Recommended kill bead: `.6`.

### D4. Typed worktree registry replaced `verify-jj`

- New thing: typed worktree registry observed with `orchestrate "(Observe Worktrees)"`, plus ordinary repo `jj` commands/reports.
- Old thing it killed: old `verify-jj` compatibility command.
- Locator: `/home/li/primary/orchestrate/AGENTS.md:310-320`.
- Evidence: lines 316-319 say `verify-jj` belonged to the retired helper and name the daemon-native replacement surface.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C3.
- Recommended kill bead: `.6`.

### D5. Session lanes replaced fixed role-named lanes

- New thing: registered per-session lanes with dynamic lifecycle.
- Old thing it killed: fixed role-named/ordinal/qualifier lanes as the lane model.
- Locator: `/home/li/primary/ARCHITECTURE.md:67-80`; `/home/li/primary/orchestrate/AGENTS.md:34-47`.
- Evidence: both locators say fixed role-named/ordinal/qualifier lane shapes are retired as the lane model and lanes now register per session.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C4.
- Recommended kill bead: `.6`.

### D6. Topic affinity/topic labels replaced role-labeled beads

- New thing: topic-affinity pickup and topic labels.
- Old thing it killed: `role:*` bead labels and discipline-pool-via-role-label rule.
- Locator: `/home/li/primary/orchestrate/AGENTS.md:379-388`.
- Evidence: lines 381-384 say beads do not carry `role:*` labels and the earlier discipline-pool rule is retired.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C5.
- Recommended kill bead: `.6`.

### D7. Deployed `spirit` CLI replaced intent file append / `intent/*.nota`

- New thing: deployed `spirit` CLI per `intent-log` and `spirit-cli` skills.
- Old thing it killed: intent capture as file append surface and `intent/*.nota` substrate.
- Locator: `/home/li/primary/orchestrate/AGENTS.md:148-151`.
- Evidence: the locator says intent capture is no longer file append, there is no legacy-file fallback, and `intent/*.nota` is retired.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C6.
- Recommended kill bead: `.6`.

### D8. `lojix` / `meta-lojix` replaced deprecated `lojix-cli`

- New thing: `lojix` read interface and privileged `meta-lojix` deploy interface.
- Old thing it killed: deprecated `lojix-cli` for OS operations.
- Locator: `/home/li/primary/repos/skills/modules/operating-system-operations/full.md:11`; metadata lines in `/home/li/primary/repos/skills/manifests/active-outputs.nota:34` and `/home/li/primary/repos/skills/manifests/skills-roster.nota:45`; generated runtime mirrors at `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md` and `/home/li/primary/.claude/skills/operating-system-operations/SKILL.md`.
- Evidence: source skill line 11 says not to use deprecated `lojix-cli` and names the current interfaces.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C7.
- Recommended kill bead: `.6`.

### D9. Logged-fold migration replaced copy-everything migration binaries

- New thing: `spirit-migrate-store` logged-fold migration using prior store log as fold input from version 9 onward.
- Old thing it killed: `spirit-migrate-production` and `spirit-upgrade-store`.
- Locator: `/home/li/primary/repos/spirit-guardian-config/INTENT.md:219-235`.
- Evidence: lines 219-235 say copy-everything binaries retired, name both old binaries, and say `spirit-migrate-store` is the one migration entry point.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C8.
- Recommended kill bead: `.6`.

### D10. `SubscribeIntent` and `Untap` replaced old `Watch` / `Unwatch` coverage

- New thing: `SubscribeIntent` for records subscription and `Untap` for token-based cancellation.
- Old thing it killed: old `Watch` records subscription and uncovered cancellation half of `Watch`/`Unwatch`.
- Locator: `/home/li/primary/repos/spirit-guardian-config/ARCHITECTURE.md:423-436`.
- Evidence: lines 431-433 say old `Watch` is covered by `SubscribeIntent` and the missing cancellation half is restored by `Untap`.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C9.
- Recommended kill bead: `.6`.

### D11. Generated Signal/Nexus/SEMA triad replaced old `persona-spirit` actor tree for the ported behavior

- New thing: schema-visible Signal/Nexus/SEMA flow using `CommandEffect(ClassifyState(...))`, `CommandSemaWrite(Record(...))`, and generated SEMA write root.
- Old thing it killed: reviving the old `persona-spirit` actor tree for that behavior.
- Locator: `/home/li/primary/repos/spirit-guardian-config/ARCHITECTURE.md:358-368`.
- Evidence: lines 366-368 say the behavior is ported without reviving the old actor tree in the daemon.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C10.
- Recommended kill bead: `.6`.

### D12. Owner-only `CollectRemovalCandidates` replaced old working-signal deletion path

- New thing: owner-only `CollectRemovalCandidates` meta operation backed by `Engine::collect_removal_candidates` and a separate archive database.
- Old thing it killed: old persona-spirit physical-deletion path on the working signal.
- Locator: `/home/li/primary/repos/spirit-guardian-config/ARCHITECTURE.md:406-421`.
- Evidence: lines 406-408 say the deletion path was ported from old persona-spirit but moved off the working signal.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C11.
- Recommended kill bead: `.6`.

### D13. Typed NOTA codec replaced previous serde-based path

- New thing: typed text codec for NOTA with closed-enum dispatch.
- Old thing it killed: previous serde-based path.
- Locator: `/home/li/primary/.claude/worktrees/nota-codec-mockup-2/README.md:55-60`.
- Evidence: line 60 says it replaces the previous serde-based path.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C12.
- Recommended kill bead: `.6`.

### D14. First-class skill targets replaced command/prompt invocation extras

- New thing: first-class `AgentsSkill` and `ClaudeSkill` target surfaces.
- Old thing it killed: command/prompt extras as current generated invocation surfaces.
- Locator: `/home/li/primary/repos/skills/skills.md:14-15`.
- Evidence: line 15 says command/prompt extras are not current generated invocation surfaces.
- Original source file: `DocsSkillsSweep-Candidates.md`, candidate C13.
- Recommended kill bead: `.6`.

## CONFIRMED FOR CODE KILL (.7)

### C1. Persona runtime still exposes `persona-mind` for `mind`

- New thing: `mind` component/repo and `mind-daemon`.
- Old thing it killed: `persona-mind` component name/path.
- Locator: `/git/github.com/LiGoldragon/persona/src/engine.rs:445` and `:544`; `/git/github.com/LiGoldragon/persona/flake.nix:21` and `:187`.
- Evidence: handoff says `persona-mind` is dead and the thing is `mind`; `primary-0m1u.1` says the rename shipped; `/home/li/primary/protocols/active-repositories.md:24` lists `mind`; `/git/github.com/LiGoldragon/mind/Cargo.toml:1-23` declares `mind` / `mind-daemon`; `/git/github.com/LiGoldragon/persona-mind` is missing.
- Original source file: `CodeSweep-Candidates.md`, candidate C1.
- Recommended kill bead: `.7`.

### C2. Primary workspace points at dead `persona-mind` checkout path

- New thing: `/git/github.com/LiGoldragon/mind`.
- Old thing it killed: `/git/github.com/LiGoldragon/persona-mind`.
- Locator: `/home/li/primary/primary.code-workspace:16-17`.
- Evidence: handoff and `primary-0m1u.1` confirm `persona-mind` renamed to `mind`; `/home/li/primary/protocols/active-repositories.md:24` lists `/git/github.com/LiGoldragon/mind`; `/git/github.com/LiGoldragon/persona-mind` is missing.
- Original source file: `CodeSweep-Candidates.md`, candidate C2.
- Recommended kill bead: `.7`.

### C3. `lojix` README still points new work to superseded `horizon-re-engineering`

- New thing: `horizon-leaner-shape` feature arc.
- Old thing it killed: `horizon-re-engineering` as the branch/worktree to pick up new `lojix` work.
- Locator: `/git/github.com/LiGoldragon/lojix/README.md:16-19`.
- Evidence: `/home/li/primary/protocols/active-repositories.md:134-147` says `horizon-leaner-shape` supersedes `horizon-re-engineering` as of 2026-05-17 and new work belongs on `horizon-leaner-shape`; the README still says first implementation lands on `horizon-re-engineering`.
- Original source file: `CodeSweep-Candidates.md`, candidate C3.
- Recommended kill bead: `.7`.

### C4. Workspace/code-repo docs still point at `signal-persona-mind`

- New thing: `signal-mind`.
- Old thing it killed: `signal-persona-mind`.
- Locator: `/home/li/primary/primary.code-workspace:72-73`; `/git/github.com/LiGoldragon/meta-signal-router/skills.md:14`.
- Evidence: `primary-0m1u.1` close reason says `signal-persona-mind` was renamed to `signal-mind`; `/home/li/primary/protocols/active-repositories.md:64` lists `signal-mind`; `/git/github.com/LiGoldragon/signal-mind` exists and `/git/github.com/LiGoldragon/signal-persona-mind` is missing.
- Original source file: `CodeSweep-Candidates.md`, suspect S1 promoted after independent rename check.
- Recommended kill bead: `.7`.

## SUSPECTS / UNRESOLVED FOR .8

### S1. `primary-36iq.7.1` quote-delimited NOTA examples after rename lock

- Surface: tracker.
- New thing: unclear.
- Old thing: remaining quote-delimited NOTA examples and possible pre-rename Persona/signal references.
- Locator: `primary-36iq.7.1`.
- Missing/blocked part: no evidence that the rename lock cleared or that the old tracker item is dead. This may be a docs/examples sweep item rather than stale tracker noise.
- Original source file: `TrackerSweep-Candidates.md`, suspect `primary-36iq.7.1`.

### S2. `subagent-session-workflow` obsolete/deleted skill

- Surface: docs.
- New thing: not explicitly named at the hit; likely active manifest plus current role/session-lane generation model, but that is an inference.
- Old thing: `subagent-session-workflow`.
- Locator: `/home/li/primary/repos/skills/ARCHITECTURE.md:75-77`; `/home/li/primary/repos/skills/manifests/skills-roster.nota:76`.
- Missing/blocked part: explicit replacement/new thing. Evidence only says obsolete/deleted and `Deleted NoEmission`.
- Original source file: `DocsSkillsSweep-Candidates.md`, suspect S3.

### S3. `router Wi-Fi` and `persona-engine-sandbox` absent from scoped docs/skills

- Surface: docs.
- New thing: unknown.
- Old thing: `router Wi-Fi`; `persona-engine-sandbox`.
- Locator: no scoped docs/skills locator found; targeted `rg` over the scoped docs/skills surfaces returned no hits.
- Missing/blocked part: locator and replacement/new thing in docs/skills. Tracker/code have separate live or suspect evidence; there is no docs kill item.
- Original source file: `DocsSkillsSweep-Candidates.md`, suspect S6.

### S4. Router Wi-Fi code/config surface

- Surface: code.
- New thing: unknown/incomplete; possible horizon-projected Wi-Fi policy and secret references, but the full replacement is not proven landed.
- Old thing: router Wi-Fi configuration surface.
- Locator: `/git/github.com/LiGoldragon/CriomOS/checks/router-wifi-secret/default.nix:7-12`; `/git/github.com/LiGoldragon/CriomOS/checks/router-wifi-horizon-policy/default.nix:7-17`; `/git/github.com/LiGoldragon/CriomOS/modules/nixos/router/default.nix:91-93`.
- Missing/blocked part: complete replacement/new thing and proof of deadness. Tracker `primary-a61` says Wi-Fi remains intentional transitional debt.
- Original source file: `CodeSweep-Candidates.md`, suspect S2.

### S5. `schema-rust-next` migration status disagreement

- Surface: code.
- New thing: `RustModuleRenderer` plus `proc_macro2::TokenStream` / `quote!` token wrappers.
- Old thing: `RustWriter` / hand-rolled string emitter.
- Locator: `/home/li/primary/protocols/active-repositories.md:37`; `/git/github.com/LiGoldragon/schema-rust-next/INTENT.md:106-114`; `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs` (`RustModuleRenderer`, `emit_item_tokens`, remaining `line` method for generated header).
- Missing/blocked part: this looks like a docs correction in `active-repositories.md`, not a code deletion item for `.7`. Keep off the confirmed code-kill track unless rerouted by a later docs/tracker decision.
- Original source file: `CodeSweep-Candidates.md`, suspect S3.

### S6. `terminal` versus `terminal-cell`

- Surface: code.
- New thing: `terminal-cell` for active V1 harness Claude/Codex terminal tests.
- Old thing: `terminal` / `persona-terminal` as a V1 harness test route.
- Locator: `/git/github.com/LiGoldragon/persona/flake.nix:59-62` and `:213-216`; `/git/github.com/LiGoldragon/harness/ARCHITECTURE.md:312-315`; `/home/li/primary/protocols/active-repositories.md:32`.
- Missing/blocked part: live evidence conflicts. Active map says use `terminal-cell` directly for V1 harness work, but `persona` still carries a supervised terminal topology. Needs a targeted ruling before deletion.
- Original source file: `CodeSweep-Candidates.md`, suspect S4.

## REJECTED / NOT STALE

### R1. `primary-vhb6` horizon re-engineering tracker item

- Surface: tracker.
- Reason rejected: old thing still has live remaining scope. `bd --readonly show primary-vhb6 --long --json` comments list remaining closure copy, activation/current-generation promotion, rollback, sema-backed GC-root records, cache retention, and CriomOS/Home cutover from `lojix-cli`.
- Original source file: `TrackerSweep-Candidates.md`, suspect `primary-vhb6`.

### R2. `primary-ihee` horizon-leaner-shape / horizon-re-engineering combine

- Surface: tracker.
- Reason rejected: no proof of completed combine or repo-by-repo landings. Issue remains `open`; comment recommends future per-repo splits after re-audit.
- Original source file: `TrackerSweep-Candidates.md`, suspect `primary-ihee`.

### R3. `primary-a61` router Wi-Fi tracker item

- Surface: tracker.
- Reason rejected: tracker explicitly says "Do not remove the current WPA3-SAE/password Wi-Fi yet" and later says SSID/country policy and test-cluster Wi-Fi constraints remain open.
- Original source file: `TrackerSweep-Candidates.md`, suspect `primary-a61`.

### R4. `primary-a18` persona-engine-sandbox tracker item

- Surface: tracker.
- Reason rejected: landed namespace and dev-stack smokes do not close remaining scope. Comments still list provider-specific Codex/Claude auth smokes and host credential mutation witnesses.
- Original source file: `TrackerSweep-Candidates.md`, suspect `primary-a18`.

### R5. `primary-n98t` partial TypeIs deletion inside still-live branch landing bead

- Surface: tracker.
- Reason rejected: issue still has live scope. Notes say horizon-rs branch integrated, but goldragon doris declaration remained unmerged.
- Original source file: `TrackerSweep-Candidates.md`, suspect `primary-n98t`.

### R6. `primary-o2kc` spirit-next to spirit rename cleanup

- Surface: tracker.
- Reason rejected: issue remains open with live cross-repo old-name triage and transitional symlink scope.
- Original source file: `TrackerSweep-Candidates.md`, suspect `primary-o2kc`.

### R7. `primary-devn.1.4` open child under implemented prototype parent

- Surface: tracker.
- Reason rejected: child comments list remaining manager/message/harness observations and live persona-introspect query path; `primary-4ddb.1` remains open for current introspect CLI work.
- Original source file: `TrackerSweep-Candidates.md`, suspect `primary-devn.1.4`.

### R8. `primary-36iq.3` bracket-string Spirit examples

- Surface: tracker.
- Reason rejected: live blocker remains. Notes say installed `/home/li/.nix-profile/bin/spirit` and `spirit-v0.1.1` still reject bracket strings, so live Spirit guidance cannot switch yet.
- Original source file: `TrackerSweep-Candidates.md`, suspect `primary-36iq.3`.

### R9. Broad docs claim that `horizon re-engineering` is stale in `INTENT.md`

- Surface: docs.
- Reason rejected: scoped doc evidence is conflicting and still live. `/home/li/primary/INTENT.md:101-109` says two deploy stacks coexist and the lean rewrite has not been cut over; `/home/li/primary/protocols/active-repositories.md:149-192` also says production and daemon reshape still coexist. The specific stale `lojix` README branch pointer is confirmed separately as code C3.
- Original source file: `DocsSkillsSweep-Candidates.md`, suspect S2.

### R10. `skills-roster.nota` as a stale surface

- Surface: docs.
- Reason rejected: docs explicitly say it remains live for compatibility checks and archived/deleted skill modeling. See `/home/li/primary/repos/skills/README.md:27-32` and `/home/li/primary/repos/skills/skills.md:9-12`.
- Original source file: `DocsSkillsSweep-Candidates.md`, suspect S4.

### R11. Retired NOTA sigils and legacy double-quoted strings bundled together

- Surface: docs.
- Reason rejected: old shape is mixed. `/home/li/primary/.claude/worktrees/nota-codec-mockup-2/ARCHITECTURE.md:131-141` says retired sigils are rejected, but legacy double-quoted string forms still decode. Not safe as a single kill item.
- Original source file: `DocsSkillsSweep-Candidates.md`, suspect S5.

### R12. `persona-spirit-daemon` deployment cleanup names

- Surface: code.
- Reason rejected: old names appear as intentional conflicts/absence guards, not dead consumers. `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix:173-200` starts `spirit-daemon` and conflicts with old services; `/git/github.com/LiGoldragon/CriomOS-home/checks/spirit-deployment/default.nix:129-134` asserts old services are absent.
- Original source file: `CodeSweep-Candidates.md`, suspect S5.

## VERIFICATION COMMANDS / EVIDENCE CHECKS

- Read handoff and sweep outputs with `sed -n`:
  - `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md`
  - `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/TrackerSweep-Candidates.md`
  - `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/DocsSkillsSweep-Candidates.md`
  - `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/CodeSweep-Candidates.md`
- Read tracker doctrine: `sed -n '1,220p' /home/li/primary/.agents/skills/beads/SKILL.md`.
- Checked Phase-1 and verifier bead status: `bd --readonly show primary-5rzf.1 primary-5rzf.2 primary-5rzf.3 primary-5rzf.4 --long --json`.
- Checked tracker candidates and suspects with serialized `bd --readonly show ... --long --json` plus concise `jq` extraction. The embedded Dolt backend produced one lock collision during an early parallel read; subsequent `bd` reads were serialized and succeeded.
- Checked close command shape with `bd close --help`; it supports `bd close [id...] --reason <reason>`.
- Checked docs evidence with targeted `nl -ba ... | sed -n ...` reads for `INTENT.md`, `ARCHITECTURE.md`, `orchestrate/AGENTS.md`, `orchestrate/ARCHITECTURE.md`, skill source/generated files, `spirit-guardian-config`, `skills.md`, and visible non-private `.claude/worktrees/nota-codec-mockup-2` docs.
- Checked code evidence with targeted `nl -ba`, `rg`, and existence probes for `/git/github.com/LiGoldragon/persona`, `/git/github.com/LiGoldragon/mind`, `/git/github.com/LiGoldragon/signal-mind`, `/git/github.com/LiGoldragon/lojix`, `/git/github.com/LiGoldragon/CriomOS`, `/git/github.com/LiGoldragon/CriomOS-home`, `/git/github.com/LiGoldragon/schema-rust-next`, `/git/github.com/LiGoldragon/harness`, and `/git/github.com/LiGoldragon/meta-signal-router`.
- Confirmed `/git/github.com/LiGoldragon/persona-mind` and `/git/github.com/LiGoldragon/signal-persona-mind` are missing, while `/git/github.com/LiGoldragon/mind` and `/git/github.com/LiGoldragon/signal-mind` exist.

Not checked:

- No `/home/li/primary/private-repos` inspection.
- No Spirit intent record sweep.
- No `/nix/store` filesystem search.
- No tests/builds; this was evidence verification only.
- No deletion/cleanup edits.
- No commits or pushes.

## TRACKER CLOSEOUT STATUS

Observed status: `primary-5rzf.1`, `primary-5rzf.2`, `primary-5rzf.3`, and `primary-5rzf.4` were all `open` when checked with `bd --readonly show ... --long --json`.

Local tracker rules: the `beads` skill says to close a bead only after acceptance criteria pass and include evidence. `bd close --help` supports closing one or more issues with `--reason`.

Closeout action taken: none. This verifier worker is operating under a read-only scout contract that allows writing the assigned output only and forbids tracker state changes outside that output. The Phase-1 tracker gap was verified and preserved here, but the beads were not closed.

Precise closeout instruction for a non-read-only worker after accepting this ledger:

```sh
bd close primary-5rzf.1 primary-5rzf.2 primary-5rzf.3 --reason "Phase-1 sweep outputs completed and verified by /home/li/primary/agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md."
bd close primary-5rzf.4 --reason "Verifier ledger produced at /home/li/primary/agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md; confirmed entries gate primary-5rzf.5/.6/.7 and suspects feed primary-5rzf.8."
```

