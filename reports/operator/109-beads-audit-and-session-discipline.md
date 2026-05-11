# BEADS Audit and Session Discipline

Operator pass over open BEADS on 2026-05-11.

This report exists because the open queue had drifted into three different
shapes: real work, stale umbrellas, and memory aids that should either be
closed or turned into skills. I used three read-only explorer audits plus local
verification before closing anything.

## What Changed

Closed during this pass:

| Bead | Why closed |
|---|---|
| `primary-5s0` | Fixed in `lojix-cli` commit `9d077d0e`: `.gitignore` now excludes `/result` and `/result-*`. |
| `primary-qfs` | Resolved: `LiGoldragon/chronos` now contains the new Chronos daemon project; local `main` is `5030b1c7`. |
| `primary-3m0` | Closed as a stale ClaviFaber umbrella. Remaining work is already tracked by child beads `primary-8b3`, `primary-e3c`, and `primary-mm0`. |
| `primary-jwi` | Superseded by the command-line mind target in `protocols/orchestration.md` and active `primary-9iv`. The old shell-helper + BEADS-query framing is not the target. |
| `primary-b1p` | Closed as a one-off watch item, not a task. If the Codex paste-image symptom recurs, file a fresh bead with current evidence. |

Discipline edits landed in this pass:

- `AGENTS.md` now lists `skills/beads.md` as required workspace reading.
- `skills/autonomous-agent.md` now has a session-end checklist: re-read the
  claimed bead, close/update it, then release locks.
- `skills/beads.md` now names beads as session anchors for non-trivial work.
- `protocols/orchestration.md` now ties release flow to closing or updating
  any claimed bead.

## Remaining P1

| Bead | Assessment | Next action |
|---|---|---|
| `primary-2w6` | Real and urgent. `persona-message` still has text-file ledger/pending files and polling. | Keep open. Migrate message state/delivery into router-owned durable state with push delivery. |
| `primary-9iv` | Real but stale wording. `persona-mind` exists and has daemon/socket flow, but the bead still mentions old `persona-orchestrate` and lock-file projection. | Refresh the bead or close/reopen under current command-line mind acceptance. Do not close yet; persona-mind still needs cutover hardening. |

## Remaining P2

| Bead | Assessment | Next action |
|---|---|---|
| `primary-0ty` | Real. `skills/rust-discipline.md` still contains free-function examples; designer reports also have old examples. | Sweep skills first; designer-owned report examples can be a separate designer pass. |
| `primary-28v` | Partly done, not closeable. Contract names landed, but stale names remain in READMEs and `persona-system` command surface (`SubscribeFocus`). | Narrow to remaining consumer/doc names, or split root-variant naming into a fresh bead. |
| `primary-3fa` | Real. Focus/input observation types still compete across `signal-persona-system`, `persona-system`, and router prompt observation. | Keep open. Decide contract ownership vs boundary translation. |
| `primary-3ro` | Stale composite. `persona-system` slice is done; `persona-message` ledger slice remains; `persona-mind` premise changed after the store split; terminal slice depends on terminal redesign. | Split into current, repo-specific beads. Do not work from the old five-item list directly. |
| `primary-4zr` | Real but partly done. Sema internal names and `OpenMode` landed; `lib.rs` split and `reader_count` cleanup remain. | Keep open, narrowed to remaining sema hygiene. |
| `primary-8b3` | Real system-specialist work. CriomOS still has yggdrasil key ownership outside clavifaber. | Keep open. Implement consolidation after clavifaber key path is stable. |
| `primary-aww` | Real operator-assistant work. `signal` still carries duplicate kernel modules while `signal-core` is the authority. | Keep open. Needs coordinated cross-repo cascade. |
| `primary-b7i` | Real. Message body is a typed string wrapper, not a typed Nexus record. | Keep open. Include message, harness, router consumers. |
| `primary-bkb` | Real. `persona-wezterm::TerminalDelivery` still has blocking handler shape. | Keep open for operator-assistant or terminal owner. |
| `primary-ddx` | Real coordinated rename. Repo/consumer crates still use `sema`; `protocols/active-repositories.md` still notes rename pending. | Keep open. Needs freeze window across consumers. |
| `primary-e3c` | Real but stale label. Designer placement moved this out of clavifaber into a sibling cluster-trust component. | Keep open but update labels/dependencies before implementation. |
| `primary-gl6` | Real designer-owned report edit. `reports/designer/72-harmonized-implementation-plan.md` still frames Nexus/NOTA as alternatives. | Keep open for designer; rewrite to "NOTA syntax, Nexus vocabulary." |
| `primary-kxb` | Partly resolved. Channel granularity and text-language decisions are closed; ZST exception and terminal adapter protocol remain. | Split into two decision beads or designer reports, then close this aggregate. |
| `primary-mm0` | Real but stale wording. Clavifaber moved from daemon phrasing to one-shot convergence runner. | Keep open, refresh wording before implementation. |
| `primary-npd` | Real. `horizon-rs` still has serde derives/attributes on input proposal types. | Keep open. Mechanical Rust cleanup. |
| `primary-obm` | Real system-specialist/design boundary work. Lore still has Nix references while primary has Nix discipline. | Keep open. Decide which lore docs stay as tool refs vs migrate to skills. |
| `primary-rhh` | Real designer-assistant decision. `persona-mind` still has `ActorKind` as a parallel namespace. | Keep open. Decide keep/drop before more topology churn. |
| `primary-tlu` | Partly done. Major `Persona*` contract names are gone; remaining `PersonaRole` / old persona-sema naming needs judgment. | Keep open but narrow to current remaining names. |
| `primary-vtq` | Real. `horizon-rs` still does not pin `nota-codec` / derive revs in the manifest. | Keep open. Pin and verify downstream. |

## Remaining P3/P4

| Bead | Assessment | Next action |
|---|---|---|
| `primary-6nf` | Likely stale. It targets old `orchestrator/src/state.rs`; persona-mind has replaced the center of gravity. | Review whether `orchestrator` is still active. If not, close as superseded by persona-mind. |
| `primary-fgk` | Real. `chronos` still has `todo!()` sky bodies. It is no longer blocked by repo conflict. | Keep open and promote if Chronos becomes active. |
| `primary-jsi` | Real. `skills/kameo.md` exists, but lore lacks `rust/kameo.md`. | Keep open for system/lore reference work. |
| `primary-oba` | Blocked. Depends on `primary-obm`; one dependency is still open. | Leave open until `primary-obm` lands. |
| `primary-oil` | Mixed/stale. Some whisrs work landed; remaining gaps should be split. | Refresh against current whisrs code and close the original if split. |
| `primary-uea` | Real design work. Cross-machine signal remains unaddressed. | Keep open for designer/system design. |
| `primary-bly` | Deferred trigger. The local workaround may already be gone, but upstream WezTerm issues remain open. | Keep as low-priority trigger or convert to deferred status. |

## Discipline Decision

The important correction is not "check BEADS more often" as a vague habit.
The rule is sharper:

```text
If work has a definition of done and may survive context compaction,
it needs a bead.

If a bead is claimed, the session cannot end until the bead is closed
or updated with the next action.
```

The lock file says what the agent is actively touching now. The bead says what
the workspace still expects after this harness forgets the thread. Both are
needed until `persona-mind` replaces them with typed role/work state.

## Recommendation

Next cleanup wave:

1. Close or refresh `primary-6nf` after checking whether `orchestrator` is still
   active.
2. Split stale aggregates: `primary-3ro`, `primary-kxb`, `primary-oil`.
3. Let role owners take their lanes:
   - operator: `primary-2w6`, `primary-9iv`, `primary-0ty`
   - operator-assistant: `primary-aww`, `primary-bkb`, `primary-ddx`
   - designer/designer-assistant: `primary-gl6`, `primary-rhh`
   - system roles: `primary-8b3`, `primary-mm0`, `primary-e3c`, `primary-jsi`

After this report lands, close `primary-38c` with the commit that contains this
report and the skill/protocol reinforcement.
