# Tracker Sweep Candidates

Task: Phase-1 tracker-only staleness/deprecation sweep for epic `primary-5rzf`, bead `primary-5rzf.1`.

Scope: read-only `bd` inspection across open and recently closed tracker issues/epics. I did not inspect `/home/li/primary/private-repos`, did not sweep Spirit intent records, did not edit tracker state, did not delete, close, claim, commit, or push.

Evidence rule used: a confirmed candidate must name the new thing, the old thing it killed, an issue-id locator, and evidence. Anything missing one of those parts is listed under SUSPECTS.

## CANDIDATES

### 1. `primary-xj51` finished-but-open integration bead

- New thing: the offline first-e2e stack and criome Part 1 mainlined across `spirit`, `mirror`, `meta-signal-spirit`, `router`, `signal-router`, `signal-criome`, and `criome`.
- Old thing it killed: the open tracker task `primary-xj51` to integrate the offline first-e2e stack to main.
- Locator: `primary-xj51`.
- Evidence: `bd show primary-xj51 --long --json` shows the issue is still `open`, but its notes say: "the 5-branch offline-e2e stack + criome Part 1 are mainlined ... Status lags reality". Its comments record operator completion on 2026-06-17 for signal-router, router, signal-criome, criome, mirror, meta-signal-spirit, and spirit, with green tests/checks except a network-only nix fetch caveat.

### 2. `primary-hj4.1.4` legacy persona-mind graph subscription child still open

- New thing: the schema-emission porting plan for stateful persona runtimes, plus the already-landed in-process `SubscriptionSupervisor` live-delta actor/event-log path.
- Old thing it killed: the legacy `persona-mind` post-commit graph subscription delta delivery tracker child.
- Locator: `primary-hj4.1.4`.
- Evidence: `bd show primary-hj4.1.4 primary-0m1u.1 --long --json` shows the item is still `in_progress` and still labeled `repo:persona-mind`. Its parent `primary-hj4.1` is closed as superseded by the schema-emission porting plan. The child comments say `persona-mind` commit `c4a80e83` landed typed thought/relation live deltas with tests, and later `5f5870fc` passed full `nix flake check`; the only stated reason for leaving it open was uncertainty about an external streaming/client surface.
- Rename evidence: `primary-0m1u.1` closed with `persona-mind -> mind`, `signal-persona-mind -> signal-mind`, and `owner-signal-persona-mind -> owner-signal-mind` shipped and verified.

### 3. `primary-uq04.2` blocked signal_cli child under superseded sweep

- New thing: schema-emission macro work through `nota-next` / `schema-next` / `schema-rust-next`, and a narrower future terminal contract migration rather than wholesale CLI replacement.
- Old thing it killed: the blocked task to migrate all nine `persona-terminal` binaries to `signal_cli!`.
- Locator: `primary-uq04.2`.
- Evidence: `bd show primary-uq04.2 primary-uq04 --long --json` shows `primary-uq04.2` is still `blocked`, while parent `primary-uq04` is closed as "Superseded by the schema-emission pivot". The child audit comment says the bead is "too broad and not mechanically executable", that most binaries are local adapters/validators, and "Do not replace the 9 binaries wholesale with signal_cli!".

### 4. `primary-uq04.3` blocked signal_cli child under superseded sweep

- New thing: schema-emission macro work through `nota-next` / `schema-next` / `schema-rust-next`, with contract-foundation migration/slicing before any generated CLI path.
- Old thing it killed: the blocked task to migrate `persona-message` `message_validate_output` to `signal_cli!`.
- Locator: `primary-uq04.3`.
- Evidence: `bd show primary-uq04.3 primary-uq04 --long --json` shows `primary-uq04.3` is still `blocked`, while parent `primary-uq04` is closed as "Superseded by the schema-emission pivot". The parent comment says remaining decomposed children are blocked by design/code-shape mismatches and that "Next useful work is contract-foundation migration/slicing, not more blind signal_cli replacement."

### 5. `primary-uq04.4` blocked signal_cli child under superseded sweep

- New thing: either a separate Nexus architecture decision for standalone translator tools or a future `signal-nexus` triad contract/daemon client surface.
- Old thing it killed: the blocked task to migrate Nexus `parse` and `render` binaries to `signal_cli!`.
- Locator: `primary-uq04.4`.
- Evidence: `bd show primary-uq04.4 primary-uq04 --long --json` shows `primary-uq04.4` is still `blocked`, while parent `primary-uq04` is closed as "Superseded by the schema-emission pivot". The child audit comment says `nexus-parse` and `nexus-render` are standalone stdin/stdout translators, not daemon clients, and names the replacement decision surface.

### 6. `primary-2chb` redirected persona-orchestrate deploy bead still open

- New thing: second-designer 162 consolidation plus the schema-emission porting plan for persona-stack runtimes.
- Old thing it killed: the open `primary-2chb` deployment bead rooted in the retired `/151` persona-orchestrate readiness/deploy framing.
- Locator: `primary-2chb`.
- Evidence: `bd show primary-2chb --long --json` shows the issue is still `open`, but its notes say: "Redirect (second-designer 162 consolidation 2026-05-23): /151 retired; relevant context migrated to reports/second-designer/162-contract-repo-lens-and-consolidation/5-older-and-triad-consolidation.md". Its blocker `primary-c620` is closed as superseded by the schema-emission porting plan.

## SUSPECTS

### `primary-vhb6` horizon re-engineering

- Plausible stale shape: handoff named "horizon re-engineering" as finished long ago but still described as active.
- Locator: `primary-vhb6`.
- Missing rule part: evidence that all 15 steps and the `lojix-cli` to `lojix` daemon cutover actually completed. `bd show primary-vhb6 --long --json` shows many landed slices, but the issue body says it closes only when all 15 step beads close plus cutover completes, and comments still list remaining activation/copy/rollback/cache-retention work.

### `primary-ihee` horizon-leaner-shape / horizon-re-engineering combine

- Plausible stale shape: `horizon-leaner-shape` and `horizon-re-engineering` are described as the same feature arc, with final branch name `horizon-leaner-shape`.
- Locator: `primary-ihee`.
- Missing rule part: evidence that the combine and repo-by-repo landings actually completed. The issue is still `open`; its comment recommends future per-repo splits rather than proving closure.

### `primary-a61` router Wi-Fi mystery / transitional debt

- Plausible stale shape: router Wi-Fi hard-coded SSID/country/SAE secret in Nix modules, with Horizon-projected Wi-Fi policy and `SecretReference` as the replacement.
- Locator: `primary-a61`.
- Origin trace: created by `li` on `2026-05-12T13:05:48Z`; linked to horizon re-engineering as step 5 of 15 in a `2026-05-14` comment; comments cite system-specialist work and report `reports/system-specialist/121-sops-nix-wifi-secret-integration.md`.
- Missing rule part: landed work killing the old shape. The comments explicitly say "Do not remove the current WPA3-SAE/password Wi-Fi yet" and later that SSID/country policy and test-cluster Wi-Fi constraints remain open.

### `primary-a18` persona-engine-sandbox mystery / agent-driven work

- Plausible stale shape: agent-driven `persona-engine-sandbox` work with dedicated provider-auth smoke scope.
- Locator: `primary-a18`.
- Origin trace: created by `li` on `2026-05-11T21:57:42Z`; comments name designer-assistant research, operator fixes, `persona` commits `8995d3f6` and `bedaac58`, and reports/designer-assistant/23.
- Missing rule part: no replacement/new thing that kills this tracker item. The namespace bug fix landed, but provider-specific Codex/Claude auth smokes and host credential mutation witnesses remain listed as open.

### `primary-n98t` partial TypeIs deletion inside still-live branch landing bead

- Plausible stale shape: `TypeIs` one-hot deleted and replaced by `BehavesAs` derived from `NodeSpecies`.
- Locator: `primary-n98t`.
- Missing rule part: proof the whole tracker item is dead. Notes say the horizon-rs `cloud-designer-cloud-node-species` branch integrated to main, but the `goldragon` doris declaration remained unmerged at the time of the note, so the issue still has live scope.

### `primary-o2kc` spirit-next to spirit rename cleanup

- Plausible stale shape: `spirit-next -> spirit` internal rename landed.
- Locator: `primary-o2kc`.
- Missing rule part: proof that the open issue is dead. Notes say internal rename landed, but cross-repo old-name references still need triage and transitional symlinks remain.

### `primary-devn.1.4` open child under implemented prototype parent

- Plausible stale shape: child issue under closed parent `primary-devn.1`.
- Locator: `primary-devn.1.4`.
- Missing rule part: evidence that a new thing killed the remaining child scope. The parent is closed as implemented, but the child comments list remaining manager/message/harness observations and a live persona-introspect query path; `primary-4ddb.1` now relates to current introspect CLI work, so this needs verifier judgment.

### `primary-36iq.3` bracket-string Spirit examples

- Plausible stale shape: code-side bracket-string consumer migration pushed and verified.
- Locator: `primary-36iq.3`.
- Missing rule part: proof the live blocker is gone. Notes explicitly say installed `spirit` and `spirit-v0.1.1` still reject bracket strings, so workspace live Spirit guidance should not teach bracket strings yet.

### `primary-36iq.7.1` remaining quote-delimited NOTA examples after rename lock

- Plausible stale shape: still references pre-rename Persona/signal repos such as `persona-mind` and `persona-router` after the rename wave.
- Locator: `primary-36iq.7.1`.
- Missing rule part: evidence that the rename lock cleared and the old tracker item is dead. It may be a docs/examples sweep item rather than stale tracker noise; needs verifier judgment.

## Mystery Origin Traces

- `primary-a61`: created by `li` at `2026-05-12T13:05:48Z`; linked by comment to horizon re-engineering `primary-vhb6` step 5; later comments record system-specialist research and partial implementation. It appears to have originated from the horizon/CriomOS literal-purge migration, not from a standalone psyche ask in the tracker body.
- `primary-a18`: created by `li` at `2026-05-11T21:57:42Z`; comments name designer-assistant local probes and operator implementation commits. It appears to have originated from sandbox runner/provider-auth research and follow-up implementation, not from a psyche-authored tracker body.

## Commands And Queries Run

- `sed -n '1,220p' /home/li/primary/.agents/skills/beads/SKILL.md`
- `sed -n '1,260p' /home/li/primary/agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md`
- `bd --help`
- `bd list --help`
- `bd query --help`
- `bd show --help`
- `bd export --help`
- `bd --readonly show primary-5rzf --long --json`
- `bd --readonly list --parent primary-5rzf --all --long --json --limit 0`
- `bd --readonly list --all --long --json --limit 0`
- `bd --readonly --json query --all "title=persona-mind OR description=persona-mind OR notes=persona-mind" --long --limit 0`
- `bd --readonly --json query --all "title=horizon OR description=horizon OR notes=horizon" --long --limit 0 | jq ...`
- `bd --readonly --json show primary-vhb6 --long`
- `bd --readonly --json show primary-ihee primary-n98t primary-unig primary-x8by --long`
- `bd --readonly --json query --all "title=superseded OR description=superseded OR notes=superseded" --long --limit 0 | jq ...`
- `bd --readonly --json query "(title=replaced OR description=replaced OR notes=replaced OR title=renamed OR description=renamed OR notes=renamed OR title=retired OR description=retired OR notes=retired OR title=deprecated OR description=deprecated OR notes=deprecated)" --long --limit 0 | jq ...`
- `bd --readonly --json query "title=duplicate OR description=duplicate OR notes=duplicate" --long --limit 0 | jq ...`
- `bd --readonly --json query --all "title=router OR description=router OR notes=router" --long --limit 0 | jq ...`
- `bd --readonly --json show primary-a61 primary-nvs8 --long`
- `bd --readonly --json query --all "title=persona-engine-sandbox OR description=persona-engine-sandbox OR notes=persona-engine-sandbox" --long --limit 0 | jq ...`
- `bd --readonly --json show primary-a18 --long`
- `bd --readonly --json query "(landed/shipped/DONE/complete terms across title/description/notes)" --long --limit 0 | jq ...`
- `bd --readonly --json show primary-xj51 primary-36iq.3 primary-36iq primary-o2kc primary-oq0n primary-xslx --long`
- `bd --readonly --json query "(status lags reality/candidate for close terms)" --long --limit 0 | jq ...`
- `bd --readonly --json query "title=persona-mind OR description=persona-mind OR notes=persona-mind" --long --limit 0 | jq ...`
- `bd --readonly --json show primary-hj4.1.4 primary-36iq.7.1 primary-0m1u.1 --long`
- `bd --readonly --json list --all --long --limit 0 | jq ... open children with closed parents ...`
- `bd --readonly --json show primary-devn.1.4 primary-uq04.2 primary-uq04.3 primary-uq04.4 primary-uq04 --long`
- `bd --readonly --json list --status open,in_progress,blocked --label-any repo:persona-mind,repo:signal-persona-mind,repo:owner-signal-persona-mind --long --limit 0 | jq ...`
- `bd --readonly --json show primary-2chb --long`

Notes on command behavior: an initial parallel set of read-only `bd` calls hit the embedded Dolt exclusive lock for all but one command, so subsequent `bd` reads were serialized. One broad label-regex exploration produced a `jq` null-label error after partial output; it was not used as candidate evidence.

## Not Checked

- No Spirit intent records were queried or swept.
- `/home/li/primary/private-repos` was not inspected.
- No code or docs repo contents were swept in this tracker bead, except issue text that names repo paths or reports.
- No destructive verifier action was taken; the verifier bead `primary-5rzf.4` remains the only deletion gate.
