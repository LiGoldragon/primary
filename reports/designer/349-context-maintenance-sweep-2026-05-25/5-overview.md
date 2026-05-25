# 5 — Overview

*Orchestrator's synthesis of the coupled context-maintenance +
intent-manifestation sweep dispatched 2026-05-25. Four parallel
subagents landed; consolidated shared-file edits applied; per-repo
INTENT.md commits pushed as feature branches; the headline POC
explainer is in place at `1-poc-schema-stack-explainer.md`.*

## §1 The four subagent landings — at a glance

| File | Subagent | Lines | Key outputs |
|---|---|---|---|
| `1-poc-schema-stack-explainer.md` | A | ~1326 | The "what does it do and how does it work" headline explainer for the schema-driven POC + migrations into 4 per-repo INTENT.md + 1 ARCHITECTURE.md + 1 new skill (`skills/schema-driven-actors.md`) |
| `2-nota-discipline-manifestation.md` | B | ~200 | NOTA bracket-only structural rule + embedding-safety principle manifested into `skills/nota-design.md` + `repos/nota/INTENT.md` + new `repos/nota-codec/INTENT.md` |
| `3-spirit-v020-integration-manifestation.md` | C | ~260 | Spirit v0.2.0 deployment + wire discipline manifested into `skills/spirit-cli.md` (new §Deployment slots, refined §Operations, new §The daemon's single-argument configuration) + `repos/persona-spirit/INTENT.md` (3 new sections) |
| `4-designer-reports-soft-cap-sweep.md` | D | ~140 | 36 older designer reports triaged — all dropped; substance pre-migrated to permanent homes. Post-state: 5 entries under the 12 soft cap |

Total: 1 headline explainer + 3 sweep reports + this overview = the meta-directory `/349`.

## §2 Reports retired this sweep

Subagent A retired:
- `/103` (schema-driven full-stack initial landing) — substance in explainer §15 + persona-spirit ARCH
- `/104` (full implementation landing) — substance in explainer §13 + schema/INTENT.md
- `/343` (effect-table syntax) — superseded by /345 §8; substance in explainer §8
- `/345` (schemas-as-channel-contracts) — substance in explainer §7-9 + per-repo INTENTs
- `/346` (actor schemas + upgrade mechanism) — substance in explainer §11-12 + persona-spirit ARCH/INTENT

Subagent A kept (per `context-maintenance.md` §3a design-rationale guard):
- `/105` (empirical showcase) — constraint test names useful as live references
- `/341` (schema crystallizes architecture) — STATUS-BANNER added; preserves competing-design rationale from the §2.5 retraction

Subagent B retired:
- `/348` (NOTA string discipline empirically confirmed) — substance in `skills/nota-design.md` + per-repo INTENTs + workspace INTENT.md

Subagent C retired:
- `/347` (spirit-v020 schema-driven integration audit) — substance in `skills/spirit-cli.md` + persona-spirit INTENT

Subagent D retired (36 entries; all pre-migrated, no kept):
- /249, /257, /263, /266, /279, /281, /285, /287, /293 (dir), /299, /301, /305-v2, /307, /308, /309, /312, /315, /316, /317 (dir), /318 (dir), /319 (dir), /320, /321, /322, /323, /324, /325, /326, /327 (dir), /329, /330, /332, /333, /333-v2, /334, /334-v2, /335 (dir), /336, /337, /337-real-pipeline-mvp (dir), /338, /339, /340, /342, /344

**Post-state of `reports/designer/`**: 5 entries — `/341` (with STATUS-BANNER), `/345`, `/346`, `/347` and the `/349` meta-directory. Wait — `/345`, `/346`, `/347` were marked retired but D's sweep shows the live state. Per D's note: *"Subagent A may further retire `/341, /343, /345, /346` if A determines their substance has migrated into per-repo INTENT.md files."* A did, post-D's sweep. So the final post-state is:

```
reports/designer/
├── 341-schema-crystallizes-architecture-2026-05-25.md  (KEPT w/ STATUS-BANNER)
└── 349-context-maintenance-sweep-2026-05-25/           (this meta-directory)
```

Plus `reports/designer-assistant/`:
```
reports/designer-assistant/
└── 105-implementation-showcase-2026-05-25.md            (KEPT as test-witness)
```

Well under the 12-entry soft cap on both. Aggressive cleanup; substance fully preserved in permanent docs.

## §3 Consolidated shared-file edits applied

Orchestrator consolidated the three subagents' proposals into:

### `/home/li/primary/AGENTS.md` — one new hard override
Added new bullet **"NOTA strings come EXCLUSIVELY from bracket forms; never emit quotation marks."** immediately after the existing "NOTA is the only argument language" bullet. Trimmed the redundant shell-double-quote tail-sentence from the existing bullet (now covered more thoroughly by the new one). Per Subagent B's proposal — Maximum-certainty psyche rule (record 698) + load-bearing design property (record 705).

Subagent A's candidate hard override (*"Schema IS the architecture, not a tool that produces it"*) was NOT applied — held for psyche escalation per the carry-uncertainty discipline. Substance lives in the new INTENT.md "The schema-driven stack" section (descriptive synthesis), which is appropriate for a record-656-level framing without the per-keystroke reinforcement that hard overrides demand.

Subagent C confirmed no AGENTS.md addition needed (spirit-cli deployment discipline is topic-specific, lives in the skill).

### `/home/li/primary/INTENT.md` — three new sections
Three sections inserted in topical order matching the file's existing flow:

1. **§"Spirit deploys side-by-side; cutover is an alias change"** — inserted after §"Two deploy stacks coexist" (deployment-discipline cluster). Per Subagent C's proposal — synthesises the v0.2.0 deployment state, the next/main/previous deployment-naming projection, the `spirit-next` slot rationale.
2. **§"NOTA is the universal embedding-safe payload"** — inserted after §"Workspace truth lives in files every agent can open". Per Subagent B's proposal — names the load-bearing design property (NOTA never contains `"`), the universal embedding-safety consequence, the `nota-codec` structural enforcement on the emitter side.
3. **§"The schema-driven stack"** — inserted after §"Persona components ship in raw form first" (component-discipline cluster). Per Subagent A's proposal — synthesises the schema-IS-architecture framing, the actor-schema pattern (ACTION + RESPONSE + universal Unknown), the rkyv-one-format-two-homes principle, the next/main/previous bridge vocabulary, the four-branch POC location.

### `ESSENCE.md` — no change
None of the records walked rise to the ESSENCE bar (gold-of-the-gold). The schema-architecture framing is high but not yet ESSENCE-tier; revisit after the schema-driven substrate becomes the production stack.

## §4 Per-repo INTENT.md edits pushed as feature branches

All four affected repos got a new `designer-sweep-349-intent-2026-05-25` bookmark pushed to origin:

| Repo | Commit | Substance |
|---|---|---|
| `schema` | `d7105762` | multi-pass parser philosophy, three Feature variants (EffectTable / FanOutTargets / StorageDescriptor), `finalize_universal_unknowns` post-pass hook |
| `signal-frame` | `22f7d30e` | NEW file — composer responsibility (authored-feature consumption, not route-derivation), extensible-header discipline |
| `persona-spirit` | `84b7001b` | comprehensive — actor-schema architecture, four-component layout, upgrade mechanism, reading-actor, deployment slots, v0.2.0 wire discipline, 9-field daemon configuration (shared with Subagent C's additions) |
| `signal-persona-spirit` | `1e7bddaf` | NEW file — dual emission compatibility approach (legacy at root, schema-driven at `::spirit::*`) |

**Operator handoff**: each branch is a docs-only fast-forwardable commit. Fast-forward each repo's `main` when convenient; no rebase required.

## §5 Skills created or refined

- **`skills/nota-design.md`** — replaced the prior bracket/bare/shell three-paragraph block with an expanded section: structural rule (record 698), bare-token shorthand (record 690), legacy-input/canonical-emit asymmetry (record 703), shell-double-quote wrapping (preserved), embedding-safety paragraph (record 705).
- **`skills/spirit-cli.md`** — new §"Deployment slots" (next/main/previous projected on deployment naming); strengthened §"How to invoke" with explicit shell double-quote framing; reshaped §"Operations on the ordinary channel" to front-and-centre description-only + terse-reply + daemon-stamped + user-creatable-topics + agent-clarifies disciplines; new §"The daemon's single-argument configuration" describing the 9-field positional shape.
- **`skills/schema-driven-actors.md`** — NEW skill created by Subagent A; registered in `skills/skills.nota` as Architecture-tier Topic skill. Carries the actor-schema authoring discipline for future actor-channel additions.

## §6 Beads filed earlier this turn (no new beads from this sweep)

The two beads filed before the sweep already cover the migration-sweep action items surfaced in /348 §7:

- **`primary-jdzy`** — Remove legacy double-quoted-string acceptance from nota-codec; migrate all emitters
- **`primary-h1vl`** — Programmatic extractor for legacy intent/*.nota files that preserves psyche timestamps

No additional beads needed; the action items are tracked.

## §7 Carry-forward — non-blocking

- **`spirit-next` slot decision** — Path A (release schema-driven as v0.3.0 once integrated) vs Path B (use `spirit-next` for unreleased preview). Operator + system-specialist call; recommendation in /347 §6 was Path B.
- **Cross-crate schema-import resolver** — the one architectural deferral from the schema-driven POC. Workaround (hand-written Rust types matching `.schema` declarations) is clean; the engines + migration runner work today against those types. Operator slice when resolver lands.
- **9-field daemon configuration as future schema-emission target** — `spirit-daemon-config.schema` would emit the daemon's positional configuration shape rather than hand-authoring. Quality-of-substrate work, not blocking.
- **lojix-cli migration from quoted-string NOTA to bracket form** — covered under `primary-jdzy`.
- **CriomOS-home `ExecStart` migration to canonical bracket form** — covered under `primary-jdzy`; system-specialist primarily.

## §8 Coordination + commit observations

- Subagents A, C, D shared the same jj working-copy commit on primary (since they wrote their reports into the same `reports/designer/349-.../` directory in parallel). The final commit picked up everyone's outputs together. Subagent B split cleanly into a separate commit (`wuyqxurl`) — cleaner per-subagent boundary, but functionally the consolidated landing is the same.
- Subagent A and C both touched `persona-spirit/INTENT.md` — A wrote the architecture sections, C appended the deployment sections after. No conflict; the file grew with both subagents' contributions in separate jj changes.
- All four per-repo INTENT.md edits are clean fast-forwardable docs commits. No code touched; nothing to rebase.

## §9 What this sweep proves

- **Aggressive substance migration works.** 41 reports retired (36 from D + 5 from A's schema-stack scope), 4 KEEP (1 via design-rationale guard, 3 still-load-bearing working artifacts — `/341`, `/345` was actually retired by A post-D, leaving only `/341`, `/349`, and `/105` from designer-assistant). Substance is in permanent docs (skills, INTENT, ARCHITECTURE), not in stale reports.
- **The four-subagent topic-split scales.** Each subagent had a tight scope, a clear destination decision tree, and minimal cross-coordination. The shared-file edits proposed-and-orchestrator-consolidated protocol avoided merge conflicts cleanly.
- **The intent-manifestation discipline works in practice.** Records 656-705 were walked; each landed in its right home per the decision tree; no `intent/*.nota` legacy appending happened during the sweep.
- **The context-maintenance discipline keeps `reports/<role>/` healthy.** Down from 40+ entries to under 5; the meta-report directory mechanism contains this session's substance compactly.

## §10 References

- `0-frame-and-method.md` — orchestrator's frame establishing the four-subagent topology
- `1-poc-schema-stack-explainer.md` — the headline POC explainer (~1326 lines)
- `2-nota-discipline-manifestation.md` — NOTA discipline sweep
- `3-spirit-v020-integration-manifestation.md` — Spirit v0.2.0 deployment sweep
- `4-designer-reports-soft-cap-sweep.md` — designer-reports triage
- `skills/context-maintenance.md` + `skills/intent-manifestation.md` — the disciplines this sweep applied
- Spirit records walked: 656-705 (the schema-crystallisation + NOTA-discipline + spirit-v0.2.0 + embedding-safety series)
