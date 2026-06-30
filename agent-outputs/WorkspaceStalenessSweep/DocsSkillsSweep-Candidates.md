# Docs and Skills Sweep Candidates

Task: Phase-1 read-only docs/skills sweep for epic `primary-5rzf`, bead `primary-5rzf.2`.

Scope used: workspace `AGENTS.md`, `INTENT.md`, `ARCHITECTURE.md`, `README*`; non-private repo docs under `/home/li/primary/repos`; skill source modules and skills repo docs under `/home/li/primary/repos/skills`; generated runtime skill surfaces under `/home/li/primary/.agents/skills` and `/home/li/primary/.claude/skills`; visible non-private `.claude/worktrees/nota-codec-mockup-2` docs because they are in the requested doc-file classes.

Boundaries honored for evidence: no `/home/li/primary/private-repos` inspection; no Spirit intent record sweep; no edits outside this assigned report. One early broad `rg` command included `agent-outputs/` because it was not yet excluded; that output was discarded and no candidates below rely on it.

Evidence rule used: a CANDIDATE below names the new thing, old thing, locator, and evidence. Entries missing any part are under SUSPECTS.

## CANDIDATES

### C1. `mind` replaced the `persona-mind` name

- New thing: `mind`.
- Old thing it killed: `persona-mind` as a component/name in docs and generated skill prose.
- Source-vs-generated flag: mixed.
- Locators:
  - Source doc: `/home/li/primary/INTENT.md:121-126` says `.beads/` destination is `persona-mind`'s native typed work graph.
  - Source doc: `/home/li/primary/ARCHITECTURE.md:67-68` says a discipline includes `persona-mind memory`.
  - Source doc: `/home/li/primary/orchestrate/AGENTS.md:19-21` and `:403-407` say discipline identity uses `persona-mind memory`.
  - Skill source: `/home/li/primary/repos/skills/modules/rust-crate-layout/full.md:34-36` says `mind` is a thin client to the long-lived `persona-mind` daemon.
  - Generated runtime: `/home/li/primary/.agents/skills/rust-crate-layout/SKILL.md:39-41` and `/home/li/primary/.claude/skills/rust-crate-layout/SKILL.md:39-41` carry the same text.
- Evidence: `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md:12` explicitly says `"persona-mind" is a dead name -- the thing is "mind" now.`

### C2. Daemon-backed `orchestrate` CLI replaced the argv-compatible helper/crate

- New thing: daemon-backed `orchestrate` component CLI using one NOTA request/reply with `orchestrate-daemon`, plus `meta-orchestrate` for meta-policy.
- Old thing it killed: `tools/orchestrate` argv-compatible helper, local `orchestrate-cli/` compatibility crate, and old `claim <role> <scope> -- <reason>` shell grammar.
- Source-vs-generated flag: source docs.
- Locators:
  - `/home/li/primary/orchestrate/ARCHITECTURE.md:5-16` names the current component CLI and says the old helper/crate are retired.
  - `/home/li/primary/orchestrate/ARCHITECTURE.md:101-114` describes the retired compatibility surface and includes old command examples.
  - `/home/li/primary/orchestrate/AGENTS.md:153-176` names the current daemon CLI and says the old helper is retired.
- Evidence: `/home/li/primary/orchestrate/ARCHITECTURE.md:103` says the compatibility layer is deprecated and should be removed from active use; `/home/li/primary/orchestrate/AGENTS.md:174-176` says the old helper is retired and should not be extended or relied on.

### C3. Typed worktree registry replaced `verify-jj`

- New thing: typed worktree registry observed with `orchestrate "(Observe Worktrees)"`, plus normal repo `jj` commands and reports for non-modeled hygiene.
- Old thing it killed: old `verify-jj` compatibility command.
- Source-vs-generated flag: source doc.
- Locator: `/home/li/primary/orchestrate/AGENTS.md:310-320`.
- Evidence: `/home/li/primary/orchestrate/AGENTS.md:316-318` says old `verify-jj` belonged to the retired helper and names the daemon-native replacement surface.

### C4. Session lanes replaced fixed role-named lanes

- New thing: registered per-session lanes with discipline metadata and dynamic register/observe/retire lifecycle.
- Old thing it killed: fixed role-named lanes such as `operator`, `second-operator`, `cluster-operator`, `schema-designer`, plus ordinal and qualifier lane shapes as the lane model.
- Source-vs-generated flag: source docs.
- Locators:
  - `/home/li/primary/ARCHITECTURE.md:67-80`.
  - `/home/li/primary/orchestrate/AGENTS.md:34-47`.
- Evidence: both locators explicitly say fixed role-named/ordinal/qualifier lane shapes are retired as the lane model and that lanes now register per session.

### C5. Topic affinity/topic labels replaced role-labeled beads

- New thing: any agent picks up any bead by topic affinity; filing uses topic labels such as `nota`, `persona`, `criome`, `horizon`.
- Old thing it killed: `role:*` bead labels and the discipline-pool-via-role-label rule.
- Source-vs-generated flag: source doc.
- Locator: `/home/li/primary/orchestrate/AGENTS.md:379-388`.
- Evidence: `/home/li/primary/orchestrate/AGENTS.md:381-384` says beads do not carry `role:*` labels and the earlier discipline-pool-via-role-label rule is retired.

### C6. Deployed `spirit` CLI replaced intent file append / `intent/*.nota`

- New thing: deployed `spirit` CLI per `skills/intent-log.md` and `skills/spirit-cli.md`.
- Old thing it killed: intent capture as a file append surface and the `intent/*.nota` substrate.
- Source-vs-generated flag: source doc.
- Locator: `/home/li/primary/orchestrate/AGENTS.md:148-151`.
- Evidence: locator says intent capture is no longer a file append surface, there is no legacy-file fallback, and `intent/*.nota` is retired. This is a docs hit only; no Spirit intent records were swept.

### C7. `lojix` and `meta-lojix` replaced deprecated `lojix-cli`

- New thing: current `lojix` read interface and privileged `meta-lojix` deploy interface.
- Old thing it killed: deprecated `lojix-cli`.
- Source-vs-generated flag: mixed.
- Locators:
  - Skill source: `/home/li/primary/repos/skills/modules/operating-system-operations/full.md:11`.
  - Skill source metadata: `/home/li/primary/repos/skills/manifests/active-outputs.nota:34` and `/home/li/primary/repos/skills/manifests/skills-roster.nota:45` mention avoiding deprecated `lojix-cli`.
  - Generated runtime: `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md:3` and `:16`.
  - Generated runtime: `/home/li/primary/.claude/skills/operating-system-operations/SKILL.md:3` and `:16`.
- Evidence: the skill source line explicitly says not to use deprecated `lojix-cli` and names the current interfaces.

### C8. Logged-fold migration with `spirit-migrate-store` replaced copy-everything migration binaries

- New thing: migration as a logged fold through `spirit-migrate-store`, using the previous store's log as fold input from version 9 onward.
- Old thing it killed: copy-everything migration binaries, specifically `spirit-migrate-production` and `spirit-upgrade-store`.
- Source-vs-generated flag: source docs.
- Locator: `/home/li/primary/repos/spirit-guardian-config/INTENT.md:219-235`.
- Evidence: locator says copy-everything binaries retired, names `spirit-migrate-production` and `spirit-upgrade-store` as retired, and says `spirit-migrate-store` is the one migration entry point.

### C9. `SubscribeIntent` and `Untap` replaced old `Watch` / `Unwatch` coverage

- New thing: `SubscribeIntent` for records subscription, plus `Untap` for token-based cancellation.
- Old thing it killed: old `Watch` records subscription and the un-covered cancellation half of `Watch`/`Unwatch`.
- Source-vs-generated flag: source doc.
- Locator: `/home/li/primary/repos/spirit-guardian-config/ARCHITECTURE.md:423-436`.
- Evidence: `/home/li/primary/repos/spirit-guardian-config/ARCHITECTURE.md:431-433` says old `Watch` is already covered by `SubscribeIntent` and the remaining cancellation half is restored by `Untap`.

### C10. Generated Signal/Nexus/SEMA triad replaced the old `persona-spirit` actor tree for the ported behavior

- New thing: schema-visible Signal/Nexus/SEMA flow where Nexus emits `CommandEffect(ClassifyState(...))` then `CommandSemaWrite(Record(...))` and SEMA persists through the generated write root.
- Old thing it killed: reviving the old `persona-spirit` actor tree for that behavior.
- Source-vs-generated flag: source doc.
- Locator: `/home/li/primary/repos/spirit-guardian-config/ARCHITECTURE.md:358-368`.
- Evidence: locator says the behavior is ported without reviving the old actor tree in the daemon.

### C11. Owner-only `CollectRemovalCandidates` meta operation replaced the old working-signal deletion path

- New thing: owner-only `CollectRemovalCandidates` on the meta socket, backed by `Engine::collect_removal_candidates` and a separate archive database.
- Old thing it killed: the old persona-spirit physical-deletion path on the working signal.
- Source-vs-generated flag: source doc.
- Locator: `/home/li/primary/repos/spirit-guardian-config/ARCHITECTURE.md:406-421`.
- Evidence: `/home/li/primary/repos/spirit-guardian-config/ARCHITECTURE.md:406-408` says the component's only physical-deletion path was ported from old persona-spirit but moved off the working signal.

### C12. Typed NOTA codec replaced the previous serde-based path

- New thing: typed text codec for NOTA with closed-enum dispatch at the boundary.
- Old thing it killed: previous serde-based path.
- Source-vs-generated flag: source doc in visible non-private worktree.
- Locator: `/home/li/primary/.claude/worktrees/nota-codec-mockup-2/README.md:55-60`.
- Evidence: `/home/li/primary/.claude/worktrees/nota-codec-mockup-2/README.md:60` says it replaces the previous serde-based path.

### C13. First-class `AgentsSkill` / `ClaudeSkill` targets replaced command/prompt generated invocation extras

- New thing: first-class `AgentsSkill` and `ClaudeSkill` target surfaces.
- Old thing it killed: command/prompt extras as generated invocation surfaces.
- Source-vs-generated flag: source skill repo doc.
- Locator: `/home/li/primary/repos/skills/skills.md:14-15`.
- Evidence: locator says active role-only components are modeled as `RoleComposition`, treats `AgentsSkill` and `ClaudeSkill` as first-class target surfaces, and says command/prompt extras are not current generated invocation surfaces.

## SUSPECTS

### S1. `signal-persona-mind` may be a dead contract name, but the replacement name is not proven

- New thing: unknown; likely something in the `mind` family, but no scoped source explicitly names `signal-mind`.
- Old thing: `signal-persona-mind`.
- Source-vs-generated flag: source docs.
- Locators: `/home/li/primary/orchestrate/AGENTS.md:347-350` and `:367-368`.
- Evidence status: handoff proves `persona-mind` -> `mind`, but the scoped docs do not explicitly prove the contract rename from `signal-persona-mind` to a specific new contract name.

### S2. `horizon re-engineering` appears as a named ghost in the handoff, but scoped docs only show related active rewrite prose

- New thing: unclear; possibly the completed/current post-reengineering horizon/deploy stack.
- Old thing: horizon re-engineering as an active/incomplete effort.
- Source-vs-generated flag: source doc.
- Locator: `/home/li/primary/INTENT.md:101-109` describes the lean rewrite, new daemon/thin CLI/lean horizon as living on rewrite branches and not cut over.
- Evidence status: `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md:13` says "horizon re-engineering" finished long ago but is still described as active. The scoped doc hit may be that stale description, but it lacks a precise new replacement/cutover locator.

### S3. `subagent-session-workflow` is obsolete/deleted, but no replacement is named at the hit

- New thing: not named at the hit; likely active manifest plus role/session-lane generation model, but this is inferred.
- Old thing: `subagent-session-workflow`.
- Source-vs-generated flag: source docs/source metadata.
- Locators: `/home/li/primary/repos/skills/ARCHITECTURE.md:75-77`; `/home/li/primary/repos/skills/manifests/skills-roster.nota:76`.
- Evidence status: architecture says `subagent-session-workflow` is obsolete and remains deleted, and the roster marks it `Deleted NoEmission`; missing explicit new thing.

### S4. `skills-roster.nota` may look legacy, but docs say it remains live for compatibility checks

- New thing: `manifests/active-outputs.nota` plus `manifests/module-dependencies.nota` for normal generation.
- Old thing: `manifests/skills-roster.nota`.
- Source-vs-generated flag: source docs.
- Locators: `/home/li/primary/repos/skills/README.md:27-32`; `/home/li/primary/repos/skills/ARCHITECTURE.md:24-27`; `/home/li/primary/repos/skills/skills.md:9-12`.
- Evidence status: not a confirmed stale candidate because the same docs explicitly say `skills-roster.nota` remains parseable/used for legacy checks and archived/deleted skill modeling.

### S5. Retired NOTA sigils and legacy double-quoted strings are mentioned, but the old string form still decodes

- New thing: canonical bracket/block string rendering and current NOTA token vocabulary.
- Old thing: retired sigils, `@`, piped delimiters, and legacy double-quoted string forms.
- Source-vs-generated flag: source doc in visible non-private worktree.
- Locator: `/home/li/primary/.claude/worktrees/nota-codec-mockup-2/ARCHITECTURE.md:131-145`.
- Evidence status: retired sigils are rejected, but double-quoted strings still decode; this is compatibility behavior, not a confirmed dead old shape.

### S6. `router Wi-Fi` and `persona-engine-sandbox` were not found in scoped docs/skill surfaces

- New thing: unknown.
- Old thing: `router Wi-Fi`; `persona-engine-sandbox`.
- Source-vs-generated flag: no in-scope hit found.
- Locator: no in-scope locator from the scoped searches. The terms appear in the handoff at `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md:14-15`.
- Evidence status: no candidate can be formed from docs/skills because the required old/new/locator/evidence set is absent in scoped surfaces.

## Search Commands Run

- `find /home/li/primary -path /home/li/primary/private-repos -prune -o -maxdepth 3 \( -name AGENTS.md -o -name INTENT.md -o -name ARCHITECTURE.md -o -name README.md -o -name README -o -name 'SKILL.md' \) -print`
- `find /home/li/primary -path /home/li/primary/private-repos -prune -o -path /home/li/primary/.git -prune -o -path /home/li/primary/result -prune -o \( -name AGENTS.md -o -name INTENT.md -o -name ARCHITECTURE.md -o -iname 'README*' \) -type f -print | sort`
- `find /home/li/primary/repos/skills /home/li/primary/skills /home/li/primary/.agents/skills /home/li/primary/.claude/skills -path /home/li/primary/private-repos -prune -o -type f \( -name 'SKILL.md' -o -name '*.md' \) -print | sort`
- `find /home/li/primary/.claude -maxdepth 4 -type f | sort | sed -n '1,260p'`
- `find /home/li/primary -path /home/li/primary/private-repos -prune -o -path /home/li/primary/result -prune -o -path /home/li/primary/agent-outputs -prune -o -path /home/li/primary/reports -prune -o \( -name AGENTS.md -o -name INTENT.md -o -name ARCHITECTURE.md -o -iname 'README*' \) -type f -print | sort`
- `rg -n --hidden --glob '!private-repos/**' --glob '!result/**' --glob 'AGENTS.md' --glob 'INTENT.md' --glob 'ARCHITECTURE.md' --glob 'README*' --glob 'CLAUDE.md' -i 'persona-mind|persona mind|\bmind\b|horizon re-engineering|horizon|router wi-?fi|wi-?fi|wifi|persona-engine-sandbox|sandbox|deprecated|deprecate|replace|replaced|renamed|rename|superseded|supersede|legacy|dead name|finished|active|ongoing' /home/li/primary`
- Discarded early broad search, not used for evidence because it included out-of-scope `agent-outputs/`: `rg -n --hidden --glob '!private-repos/**' --glob '!result/**' -i 'persona-mind|horizon re-engineering|router wi-?fi|persona-engine-sandbox' /home/li/primary`
- `rg -n -i 'persona-mind|persona mind|\bmind\b|horizon re-engineering|horizon|router wi-?fi|wi-?fi|wifi|persona-engine-sandbox|sandbox|deprecated|deprecate|replace|replaced|renamed|rename|superseded|supersede|legacy|dead name|finished|active|ongoing' /home/li/primary/repos/skills/modules /home/li/primary/repos/skills/roles /home/li/primary/repos/skills/skills.md /home/li/primary/repos/skills/AGENTS.md /home/li/primary/repos/skills/ARCHITECTURE.md /home/li/primary/repos/skills/README.md`
- `rg -n -i 'persona-mind|persona mind|\bmind\b|horizon re-engineering|horizon|router wi-?fi|wi-?fi|wifi|persona-engine-sandbox|sandbox|deprecated|deprecate|replace|replaced|renamed|rename|superseded|supersede|legacy|dead name|finished|active|ongoing' /home/li/primary/.agents/skills /home/li/primary/.claude/skills`
- `rg -n --hidden --glob '!private-repos/**' --glob '!result/**' --glob '!agent-outputs/**' --glob '!reports/**' -i 'lojix-cli|tools/orchestrate|orchestrate-cli|legacy-file fallback|legacy helper|legacy shell|argv compatibility|shell helper|signal-persona-mind|persona-mind' /home/li/primary/AGENTS.md /home/li/primary/ARCHITECTURE.md /home/li/primary/INTENT.md /home/li/primary/orchestrate /home/li/primary/repos/skills /home/li/primary/.agents/skills /home/li/primary/.claude/skills`
- `rg -n --hidden --glob '!private-repos/**' --glob '!result/**' --glob '!agent-outputs/**' --glob '!reports/**' -i 'horizon re-engineering|re-engineering|router wi-?fi|persona-engine-sandbox' /home/li/primary/AGENTS.md /home/li/primary/ARCHITECTURE.md /home/li/primary/INTENT.md /home/li/primary/orchestrate /home/li/primary/repos/skills /home/li/primary/.agents/skills /home/li/primary/.claude/skills`
- `rg -n --hidden --glob '!private-repos/**' --glob '!result/**' --glob '!agent-outputs/**' --glob '!reports/**' -i 'active-outputs\.nota|skills-roster\.nota|compatibility input|legacy checks|active manifest|deleted modules|archived modules|no active emission' /home/li/primary/repos/skills /home/li/primary/.agents/skills /home/li/primary/.claude/skills /home/li/primary/AGENTS.md /home/li/primary/ARCHITECTURE.md /home/li/primary/INTENT.md /home/li/primary/orchestrate`
- `rg -n --hidden --glob '!private-repos/**' --glob '!result/**' --glob '!agent-outputs/**' --glob '!reports/**' -i 'old monolithic|lean rewrite|rewrite branches|has not been cut over|cutover|active repositories|protocols/active-repositories|retired|deprecated' /home/li/primary/AGENTS.md /home/li/primary/ARCHITECTURE.md /home/li/primary/INTENT.md /home/li/primary/orchestrate /home/li/primary/repos/skills /home/li/primary/.agents/skills /home/li/primary/.claude/skills`
- `rg -n --hidden --glob '!private-repos/**' --glob '!result/**' --glob '!agent-outputs/**' --glob '!reports/**' -i 'skills/skills\.nota|subagent-session-workflow|command/prompt extras|generated invocation|persona-mind|signal-persona-mind|lojix-cli|tools/orchestrate|verify-jj|intent/\*\.nota|intent/.*nota|legacy-file fallback' /home/li/primary/repos/skills /home/li/primary/.agents/skills /home/li/primary/.claude/skills /home/li/primary/AGENTS.md /home/li/primary/ARCHITECTURE.md /home/li/primary/INTENT.md /home/li/primary/orchestrate`
- `rg -n --hidden --glob '!private-repos/**' --glob '!result/**' --glob '!agent-outputs/**' --glob '!reports/**' -i 'deprecated|retired|obsolete|superseded|replaced|replacement|no legacy|legacy .*fallback|old .*retired|old .*deprecated|do not use|do not extend|not current|dead|deleted' /home/li/primary/AGENTS.md /home/li/primary/ARCHITECTURE.md /home/li/primary/INTENT.md /home/li/primary/orchestrate /home/li/primary/repos/skills/modules /home/li/primary/repos/skills/roles /home/li/primary/repos/skills/README.md /home/li/primary/repos/skills/ARCHITECTURE.md /home/li/primary/repos/skills/skills.md /home/li/primary/.agents/skills /home/li/primary/.claude/skills`
- `find /home/li/primary/repos/skills/skills/archive -maxdepth 1 -type f -print | sort | xargs -r rg -n -i 'persona-mind|horizon|router wi-?fi|persona-engine-sandbox|deprecated|retired|obsolete|replaced|superseded|lojix-cli|tools/orchestrate|skills/skills\.nota|subagent-session-workflow'`
- `rg -n --hidden --glob '!private-repos/**' --glob '!result/**' --glob '!agent-outputs/**' --glob '!reports/**' -i 'role label|role-labeled|discipline-pool|fixed role|second-designer|cluster-operator|ordinal|qualifier|session lane|lane model|retired' /home/li/primary/ARCHITECTURE.md /home/li/primary/orchestrate/AGENTS.md /home/li/primary/orchestrate/ARCHITECTURE.md /home/li/primary/orchestrate/roles.list /home/li/primary/repos/skills/modules /home/li/primary/.agents/skills /home/li/primary/.claude/skills`
- `rg -n --hidden -i 'deprecated|retired|obsolete|superseded|replaced|replaces|old|legacy|persona-mind|horizon re-engineering|router wi-?fi|persona-engine-sandbox' /home/li/primary/.claude/worktrees/nota-codec-mockup-2/AGENTS.md /home/li/primary/.claude/worktrees/nota-codec-mockup-2/ARCHITECTURE.md /home/li/primary/.claude/worktrees/nota-codec-mockup-2/README.md`
- `rg -n -i 'deprecated|retired|obsolete|superseded|replaced|replaces|old|legacy|persona-mind|horizon re-engineering|router wi-?fi|persona-engine-sandbox' /home/li/primary/repos/spirit-guardian-config/AGENTS.md /home/li/primary/repos/spirit-guardian-config/ARCHITECTURE.md /home/li/primary/repos/spirit-guardian-config/INTENT.md /home/li/primary/repos/spirit-guardian-config/README.md`
- `rg -n -i 'replaces|retired|old|legacy|deprecated|obsolete|supersed|not .*current|do not use|replaced' /home/li/primary/repos/spirit-guardian-config/AGENTS.md /home/li/primary/repos/spirit-guardian-config/ARCHITECTURE.md /home/li/primary/repos/spirit-guardian-config/INTENT.md /home/li/primary/repos/spirit-guardian-config/README.md`

## Checks, Unknowns, and Blockers

- Checks run: read-only searches and line-number inspections only; no tests were run because this was a docs/skills audit.
- Output written: this file only.
- Blockers: none for the report.
- Not checked: `/home/li/primary/private-repos`, Spirit intent records, `/nix/store`, deletion safety, and code-level deadness outside doc/skill evidence.
- Follow-up: verifier bead `primary-5rzf.4` must refute or accept each candidate before any deletion work.
