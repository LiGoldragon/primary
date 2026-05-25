*Kind: Audit · Topic: operator/180 schema field name + upgrade context · Date: 2026-05-25 · Lane: second-designer (counter-ego)*

# 179 — Audit: operator /180 (meta-directory) schema field name + upgrade context

## §1 Scope

Per psyche directive 2026-05-25 ("audit"), apply intent 511 (audit cycle) to `reports/operator/180-schema-field-name-and-upgrade-context-2026-05-25/` (4-file meta-directory: 0-frame, 1-subagent-synthesis, 2-implementation-and-tests, 3-overview).

What /180 landed: two commits + a P0 blocker named + 7 remaining gaps enumerated:
- `signal-frame` `e4e1581c` — "preserve schema field names in macro emission"
- `signal-persona-spirit` `03d160b5` — "name schema fields for macro emission"
- P0 blocker `primary-602y` named: rebuild persona-spirit v0.1.0.1 retrofit against current post-ShortHeader `signal-frame`

## §2 Implementation-vs-design alignment

| Design element | /180 implementation | Match |
|---|---|---|
| Schema preserves field names (nota-designer/8 deviation #2) | `SchemaField { name, schema_type }` replaces positional `Vec<SchemaType>`; reader preserves `schema::Field::name()` | ✓ MAJOR step — partial address of intent 506 (data-carrying macro variants with input structs) |
| Field-name source = schema, not macro | `spirit.schema` declares `Entry topic kind summary context certainty quote`; macro consumes explicit names | ✓ correct ownership boundary |
| Removed Spirit-specific hardcoding | `Entry + Magnitude => certainty` + `RecordSummary + RecordIdentifier => identifier` hacks deleted | ✓ clean |
| ShortHeader generation uses schema field names | Updated emit | ✓ schema-derived |
| NOTA box-form codec uses schema field names | Updated emit | ✓ schema-derived |
| Validation walks `SchemaField.schema_type` | Updated | ✓ |
| `cargo fmt + clippy + test + nix flake check` | All green on both repos | ✓ |
| `signal-persona-spirit/short_header` test | passing | ✓ |
| `signal-persona-spirit/box_form` test | round trips `(Entry Decision High)` boxed | ✓ |
| v0.1.0→v0.1.1 migration projection tests | still pass | ✓ |

**Verdict**: /180 cleanly closes the Spirit-specific-field-hardcoding gap by lifting the field-name source up into the schema itself. This is a load-bearing step toward the named-input-struct vision from nota-designer/8 + intent 506.

## §3 The P0 blocker — `primary-602y` (v0.1.0.1 retrofit wire-format mismatch)

**The finding** (from `/333-v2` per /180 §"What remains"): deployed Spirit v0.1.0.1 (operator/178 `primary-wdl6`) was built BEFORE ShortHeader landed in `signal-frame`. Current v0.1.1 emits + consumes ShortHeaders on every frame; v0.1.0.1 does not. Cross-version handover (v0.1.0 ↔ v0.1.1) on production CANNOT WORK because the daemons cannot parse each other's frames.

**Why this is severe**: my prior audit `/178` (of second-operator/186) concluded orchestrate's handover was "code-complete". By analogy I'd have concluded Spirit's handover is also code-complete — operator/178 wired the three-socket topology, the marker ceremony works in nspawn-pair-of-same-version tests. But cross-version tests against the DEPLOYED v0.1.0.1 binary would fail at the first frame because v0.1.0.1's wire format doesn't include the ShortHeader prefix that v0.1.1 expects (or strips it as garbage).

**What the test coverage missed**: designer's `spirit-nspawn-handover-socket` worktree per /333 §3 exercises the 3-step ceremony — but presumably between two daemons built from the same source revision, so both have ShortHeader. The cross-revision compatibility was implicitly assumed-but-not-tested. My /178 audit didn't catch this because it focused on /186's per-message integrity (marker fidelity via sema-engine commit_sequence) rather than wire-format-compatibility across deployed-revision pairs.

**Implication for my /178 audit**: I should add a row to the deviation table — "cross-version wire-format compatibility validated against deployed v0.1.0.1": NOT YET; gated on `primary-602y`. Recommendation in /178 §7 stands but needs primary-602y at top of the priority list.

**Action**: operator/180 names `primary-602y` as the next slice. Backporting ShortHeader-emit + ShortHeader-consume to the v0.1.0.1 maintenance branch (or rebuilding v0.1.0.1 from current `signal-frame` with the protocol-aware retrofit re-applied). Standard backport pattern; operator has the playbook from `primary-wdl6`.

## §4 Mirror phase-ordering divergence — Spirit vs Orchestrate

**The divergence** (per /180 overview §"Open implementation/design gaps"): "current Spirit accepts Mirror only after `HandoverCompleted`, while the design needs Mirror during handover."

**Cross-reference**: second-operator/186 places orchestrate's Mirror in the marker-to-readiness window (per /333 §8 + /175 §6 Phase 3 design). Spirit's implementation diverges — Mirror handler exists but the wiring effectively requires `HandoverCompleted` first.

**Code observation**: `persona-spirit/src/daemon.rs:1420-1450` shows the upgrade-operation reply dispatch. `freezes_public_writes` triggers on `ReadyToHandover`; `closes_public_sockets` triggers on `HandoverCompleted`; `may_reopen_public_writes` triggers on `RecoverFromFailure`. No explicit Mirror-during-handover wiring in this conditional flow — Mirror would need to be handled in `SpiritRoot::SubmitUpgradeRequest` actor logic, but per /180 the wiring there triggers post-completion only.

**Severity assessment**: Spirit doesn't NEED Mirror functionally (empty payload per /175 §9 — sync writes, no in-memory critical state). So Spirit's Mirror handling being post-completion is essentially vestigial — it never gets exercised in practice because Spirit's Mirror is empty. BUT: if Mirror is wired wrong for Spirit, the implementation could mislead future components copying Spirit's pattern. Pattern-consistency matters.

**Recommendation**: align Spirit's Mirror handling with /186's orchestrate pattern (Mirror in marker-to-readiness window). Even if Spirit's Mirror payload is empty, the wiring should accept Mirror in the same phase as orchestrate so the pattern generalizes cleanly. Small slice; high pattern-consistency value.

## §5 The named-field-in-schema landing — addresses nota-designer/8 deviation #2

**Background**: nota-designer/8 §"Deviation 2 — schema erases macro input object roles" flagged that `schema/src/declaration.rs` modeled records as `Record(Vec<TypeExpression>)` and `Payload::Fields(Vec<TypeExpression>)` — positional vectors that ERASE field-name roles. Intent 506 + nota-designer/8 §"Reusable Lowering Shape" called for named input structs (`EnumDefinitionInput`, `RecordDefinitionInput`, etc.) where field names live at the Rust model layer.

**What /180 does**: introduces `SchemaField { name, schema_type }` at the macro-model layer; `spirit.schema` declares field names explicitly; macro consumes them. This is PARTIAL closure of nota-designer/8 deviation #2 — field-name PRESERVATION (in the schema crate's parser output → macro model) is there, but the full named-input-struct-per-macro-variant pattern (separate `HeaderRootInput`, `EnumDefinitionInput`, etc.) is not yet. The direction is correct; the destination needs another step.

**What still remains** from nota-designer/8 deviation #2: the `BuiltinMacroVariant` enum carrying typed input structs per variant rather than the current generic `Vec<SchemaField>` shape. Designer's /334-v2 §3.4 says this is misframed — the variants exist with different shape than nota-designer/8 imagined. Worth a fresh small audit to settle the post-/180 deviation-#2 state.

## §6 Deviation-table updates for /176 §13 + /333 §13 + /178 §6

These rows should now reflect /180:

| Row | Before /180 | After /180 |
|---|---|---|
| Schema preserves field names | NOT (positional `Vec<TypeExpression>` erases field names) | WIRED — `SchemaField { name, schema_type }` preserved end-to-end |
| Field-name macro hardcoding | YES (`Entry + Magnitude => certainty`, etc.) | RETIRED — schema owns field names |
| `spirit.schema` explicit field names | NOT | WIRED for all relevant records |
| Cross-version wire-format compat (deployed v0.1.0.1 ↔ v0.1.1) | implicit-but-unverified | EXPLICIT GAP — P0 blocker `primary-602y` |
| Spirit Mirror phase ordering | post-completion (vestigial; Spirit Mirror is empty) | UNCHANGED — needs alignment with /186 orchestrate pattern (marker-to-readiness) |
| Owner signal schema coverage | behind ordinary | UNCHANGED — open gap |
| Schema diffs → VersionProjection | hand-written (signal-persona-spirit/src/migration.rs) | UNCHANGED — still hand-written |
| Storage schema descriptors | not yet schema-derived | UNCHANGED |
| Divergence wire | typed minimally (per /186) | UNCHANGED — abort/recovery policy still not enforced |
| Recovery executor | wire-only | UNCHANGED — no real recovery executor |

## §7 Recommendations

In priority order:

1. **`primary-602y` first** — P0 blocker for production cutover. Operator's recommendation matches; no production handover until this lands.

2. **Align Spirit's Mirror handling with /186 orchestrate pattern** — small slice, high pattern-consistency value. Even with Spirit's empty payload, the wiring shape should generalize.

3. **My prior /178 §3 recommendation (backport ShortHeader-validation + marker-consistency to Spirit)** — still relevant but now subordinate to primary-602y. /186's positive deviations should land in the SAME backport pass as primary-602y to minimize cutover thrash.

4. **Fresh audit of nota-designer/8 deviation #2 post-/180** — /180 closed the field-name preservation part; the named-input-struct-per-variant part remains. Worth ~50 LoC of read + a half-page report to settle the current state.

5. **The 7 remaining gaps from /180 §"Open implementation/design gaps"** — each is operator-actionable bead: Divergence enforcement, Recovery executor, VersionProjection generation, storage descriptors, owner signal coverage. Sequence by dependency.

## §8 Convergence with intent 569-571 (designer's multi-pass macro captures)

/180's `SchemaField { name, schema_type }` is exactly the shape implied by intent **569** (iterative-to-fixed-point macro application) + **570** (dependency-ordered namespace, basic first) + **571** (newtype emits Rust single-tuple struct wrapping inner data). The field-name preservation step is the FIRST PASS of the multi-pass macro model designer captured — every macro now sees named fields, not positional indexes. Subsequent passes (macro identification, application, assembly) can rely on field names being load-bearing data not "lossy positional encoding".

This convergence means: /180 + designer /334-v2 + intent 569-571 form a consistent next-iteration vector. Operator implementing one slice of the multi-pass pipeline; designer capturing the full pipeline; my /178 + /179 auditing the slices as they land.

## §9 What this audit does NOT do

- Does NOT recommend operator close any /180-related beads (operator owns bead state)
- Does NOT block /180 from being on main — it's already there; this is REVIEW
- Does NOT propose new design — only forward-notes for next operator slices
- Does NOT capture new psyche intent (no new psyche directives in /180)
- Does NOT re-audit second-operator/186 or sub-agent A's /177 (covered in /178)

## §10 References

- `reports/operator/180-schema-field-name-and-upgrade-context-2026-05-25/` — the meta-directory under audit (4 files)
- `reports/designer/333-v2-upgrade-mechanism-corrections-from-real-world-test.md` — source of the P0 finding
- `reports/designer/333-upgrade-mechanism-full-design-explained.md` — design baseline
- `reports/designer/334-v2-multi-pass-nota-first-schema-reader.md` — multi-pass design that /180 implements one slice of
- `reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` — deviation #2 partially closed by /180
- `reports/second-designer/178-audit-second-operator-186-orchestrate-upgrade-socket-2026-05-25.md` — my prior audit; this report extends its deviation table
- `reports/second-designer/176-upgrade-mechanism-soup-to-nuts-2026-05-25.md` — deviation table to update
- `reports/second-operator/186-orchestrate-upgrade-socket-implementation-2026-05-25.md` — orchestrate Mirror pattern that Spirit should align to
- `/git/github.com/LiGoldragon/signal-frame/` commit `e4e1581c`
- `/git/github.com/LiGoldragon/signal-persona-spirit/` commit `03d160b5`
- `/git/github.com/LiGoldragon/persona-spirit/src/daemon.rs:1420-1450` — upgrade operation reply dispatch (showing Mirror not wired in pre-completion conditional flow)
- Intent records 511 (audit cycle), 506 (data-carrying macro variants with input structs), 569 (iterative-to-fixed-point macro), 570 (dependency-ordered namespace), 571 (newtype = Rust single-tuple struct), 574 (workflow rolls forward globally)
