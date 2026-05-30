# 439 — Context maintenance: designer-lane sweep after the schema/NOTA stack push

*Kind: Maintenance ledger · Topics: context-maintenance, designer-lane, sweep, retire, landing-evidence · 2026-05-30 · designer lane*

*End-of-session checkpoint per `skills/context-maintenance.md`. Trigger:
context at 60% used, plus the designer-lane report count crossed soft cap
(22 reports against the 12 cap from `skills/reporting.md`). Scope: this
session's designer reports (421-438) — the schema/NOTA/Spirit stack push
that landed across nota-next, schema-next, schema-rust-next, spirit-next
on main. The sweep applies the topic-recency rule per skill §2 (the topic
is "schema-NOTA-Spirit stack design" with operator's whole-stack tours and
implementation reports as the cross-lane reference).*

## 1. Topic arc

The session pushed the schema/NOTA stack from "@-sigil declarations + macro
data" through "strict-brace key/value + macro-node structural matching" with
operator implementations landing per slice. Spirit records 1216-1263 captured
the durable intent; per-repo INTENT.md + ARCHITECTURE.md absorbed the
architecture; operator reports 240-259 document the implementation passes.

Three era-shifts within the session:
1. **Codec opt-in landed** (records 1236-1238): rkyv-universal + NOTA-opt-in
   via feature gate; daemon binary zero-NOTA closure proven by source-guard
   + socket-negative tests.
2. **Assembled schema went live** (records 1248-1255): durable `.asschema`
   artifact, `RustModule` data model, MacroLibraryData with structural
   patterns.
3. **Strict-brace + macro-nodes** (records 1259, 1263): brace = key/value
   strict, value-side `*` shorthand, `MacroNodeDefinition` with structural
   cases as data.

## 2. Current canonical surface

- **Strict-brace syntax**: `reports/designer/437-strict-brace-key-value-explanation-and-implementation-try.md` + `reports/operator/256-strict-brace-key-value-schema-implementation.md`
- **Macro-node structural matching**: `reports/designer/438-macro-nodes-at-nota-layer-vision-focused-on-critical-parts.md` + `reports/operator/258-macro-node-structural-matching-implementation.md`
- **Whole-stack current**: `reports/operator/248-schema-nota-spirit-whole-stack-tour.md` is the canonical implementation-state walkthrough.
- **Live `.asschema` discipline**: `reports/designer/434-live-assembled-schema-bootstrap-and-loop-closure.md` + `reports/operator/250-asschema-live-artifact-implementation-2026-05-30.md` + `reports/operator/252-asschema-artifact-gap-closure-2026-05-30.md`
- **Codec opt-in implementation**: `reports/operator/246-nota-surface-split-for-lean-daemons-2026-05-30.md` + `reports/designer/430-codec-opt-in-research-rkyv-base-nota-on-top.md`

Plus operator self-audit `reports/operator/251-schema-asschema-self-audit-against-designer-434.md` as the canonical example of the audit-precision discipline (informed `skills/designer.md` §"Audit precision").

## 3. Retired this sweep — designer lane

Twelve reports/directories drop with landing-evidence:

| Path | Reason | Landing |
| ---- | ------ | ------- |
| `reports/designer/421-nota.md` | NOTA substrate spec migrated to permanent docs | nota-next `INTENT.md` + `ARCHITECTURE.md`; Spirit records 1216, 1229, 1232, 1235, 1259 |
| `reports/designer/422-schema.md` | Schema spec migrated | schema-next `INTENT.md` + `ARCHITECTURE.md`; Spirit records 1226, 1232, 1235, 1259 |
| `reports/designer/423-signal-nexus-sema.md` | Plane spec absorbed | spirit-next `ARCHITECTURE.md`; operator 248 §5 |
| `reports/designer/424-schema-nota-extension-full-correctness-design-intent.md` | Full-correctness intent absorbed into forward visions | reports/designer/430, 431, 434, 437, 438 |
| `reports/designer/425-implementation-avoidance-audit/` | Bootstrap audit; target landed (operator built genuine implementation) | operator 241 + subsequent |
| `reports/designer/426-schema-implementation-deep-review.md` | Audit; target addressed by operator | operator 242 + subsequent slices |
| `reports/designer/427-schema-stack-as-implemented-now.md` | State snapshot; superseded by operator's living view | operator 248 |
| `reports/designer/428-at-sigil-declaration-syntax-spec.md` | @-sigil syntax superseded by strict-brace | reports/designer/437 + Spirit record 1259 + operator 256 (compat parser kept temporarily, target syntax is strict-brace) |
| `reports/designer/429-whole-stack-presentation-nota-to-spirit.md` | First whole-stack synthesis, superseded twice | reports/operator/248 (canonical current state) |
| `reports/designer/432-audit-operator-slice-1-codec-opt-in-and-binary-config.md` | Audit; target landed and matured (operator 247, 250, 256) | Slice-1 fully integrated on main |
| `reports/designer/433-whole-stack-comprehensive-every-part-with-code.md` | Comprehensive walkthrough, partial syntax supersession, the runtime + emission sections absorbed by operator 248 + 250 + 256 | operator 248 (whole-stack), 437 (syntax revision), 258 (macro-nodes) |
| `reports/designer/436-next-move-vision-self-hosting-macros-from-core-schema.md` | Self-hosting macros vision; absorbed by operator's lean | operator 255 + 258 |

Per the design-rationale guard (skill §3a): none of the dropped reports
enumerate competing design alternatives that aren't otherwise preserved.
Reports proposing alternatives — codec mechanism options (430), four-gap
ordering alternatives (435), `(Derive)` vs `*` (437) — are KEPT (§4).

## 4. Kept this sweep — designer lane (with rationale)

Six session reports remain load-bearing as forward design or design rationale:

| Path | Rationale |
| ---- | --------- |
| `reports/designer/430-codec-opt-in-research-rkyv-base-nota-on-top.md` | Design rationale — three mechanism options (Cargo feature single-crate, two-crate, per-target emission, hybrid); chosen mechanism landed on main but the alternatives are preserved for future feature-split decisions. |
| `reports/designer/431-daemon-zero-nota-state-aware-startup-multi-signal.md` | Forward — slice 2 (state-aware startup + standby + multi-signal + numerator) not yet on main; prototype exists on `daemon-zero-nota-2026-05-30` branch. |
| `reports/designer/434-live-assembled-schema-bootstrap-and-loop-closure.md` | Forward — Stage 4 (macro-table from core.schema) and Stage 5 (self-hosting loop closure) still ahead; operator 254/255/258 are advancing through these. |
| `reports/designer/435-vision-for-the-four-remaining-gaps.md` | Design rationale + forward — four-gap framing with alternate orderings (deploy-pressure, developer-extensibility); operator 253 settled an ordering but the alternatives + the schema-diff/upgrade shape (Gap D) remain ahead. |
| `reports/designer/437-strict-brace-key-value-explanation-and-implementation-try.md` | Design rationale — proposed `(Derive)` value-side marker as more NOTA-canonical; operator chose `*` per psyche preference. Alternatives preserved for future revisits. |
| `reports/designer/438-macro-nodes-at-nota-layer-vision-focused-on-critical-parts.md` | Live forward — macro-nodes-at-NOTA-layer not yet realized; operator 258 is the bootstrap-floor first cut; the lift to nota-next + named-captures + Match-output + conflict-detection are the next slices. |

Older designer reports (351, 352, 412, 415) retained as outside this sweep's
scope; their next maintenance pass will assess them.

Post-sweep designer-lane count: 6 session reports + 4 older + this ledger = **11 reports**, under the 12-cap.

## 5. Cross-lane observations (not actions)

The operator-lane cadence this session demonstrated several patterns worth
recording (operator owns drops in their lane; this report just notes the
state):

- Operator's **implementation report → self-audit pair** pattern (250→251,
  252→253, 256→257, 258→259) is the canonical audit-precision shape;
  documented in `skills/designer.md` §"Audit precision".
- Operator-lane likely also over soft cap (20 reports 240-259); a future
  cross-lane sweep should look at operator-side retirement candidates.
  Likely landing for operator-side drops: each implementation report retires
  once its slice is fully verified + integrated (commits on main + tests
  passing + INTENT.md/ARCHITECTURE.md updated). Many of operator's 240-258
  meet that bar.

## 6. Designer next-session targets

Concrete pickup points for the next designer session:

1. **Audit operator's macro-node lift to nota-next** when it lands. Reference
   designer 438 §6 critical decisions 1, 4, 5 (layer placement, named
   captures, Match output). Use the audit-precision discipline.
2. **Vision for slice 2 of 431** (state-aware startup + standby + multi-signal
   + numerator) — operator deferred the coordinated migration; once the Nix
   proof harness migration plan is on the table, design the integration with
   the prototype branch.
3. **Stage 5 self-hosting loop closure** — once macro-table-from-core.schema
   lands (operator 258 first cut → next slice's nota-next lift), the loop
   closure is reachable. Forward vision in 434 §6 + 438 §8.
4. **Schema-core support nouns extraction (Gap 3 of 435)** — depends on
   stable cross-crate import resolution; not yet started.
5. **SchemaDiff + UpgradePlan (Gap 4 of 435)** — depends on stable
   `.asschema` artifact comparison; the new `AsschemaArtifact` shape unblocks
   the structural shape, but the diff types + upgrade plan + emitter changes
   remain.

## 7. The one-line summary

Twelve designer reports retire with named landings (mostly to per-repo
permanent docs + Spirit records + operator's living implementation reports);
six session reports stay as forward design + design rationale; four older
reports parked for next sweep; designer-lane is now back under soft cap.
The schema/NOTA/Spirit stack's current canonical surface is operator 248
+ 256 + 258 for implementation state; designer 430/431/434/435/437/438 for
forward visions and design alternatives.
