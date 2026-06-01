# 461.6 — Proof-of-usage witness research

*Kind: Review · Topics: proof-of-usage, witness-ladder, architectural-truth-tests, spirit-1341 · 2026-06-01*

## Topic arc

Operator's earlier-day Spirit capture **1341 (Constraint Maximum)**
named what's forbidden: "Positive grep deployment checks are not
allowed as proof of a live architecture or behavior. A build or
deployment check must compile, execute, round-trip, or otherwise
exercise the real path; grep may only be used as a narrow negative
guard to prove a retired symbol or forbidden pattern is absent."

The negative discipline landed pre-dispatch in:

- `skills/architectural-truth-tests.md` §"No positive grep as
  deployment proof" (line 47)
- `skills/testing.md` §"No positive grep deployment checks" (line 39)

The psyche then directed designer to research the **positive
complement**: "It doesn't prove the architecture is live, it just
proves it's in the file. We need to make sure it's actually used.
Research this."

Designer 459 was that research. It built a **three-layer
proof-of-usage model** (STATIC / RUNTIME / BEHAVIORAL) with per-layer
witness catalogue + cost ratings + the choose-cheapest-sufficient
discipline + three worked examples. Plus two tool-upgrade proposals
(an `architectural-witness` cargo subcommand reading
`witnesses.toml`, and an `assert_trait_method_called!` macro for
trait-call-site assertions).

The skill upgrade proposed in 459's §"Skill upgrade proposal"
identified `skills/architectural-truth-tests.md` as the canonical
home for the positive complement.

## Current canonical surface

| Surface | What it carries |
|---|---|
| `skills/architectural-truth-tests.md` §"Proof-of-usage ladder — choose cheapest sufficient" (NEWLY LANDED this sweep) | Three-layer model; per-layer witness catalogue with cost columns; the choose-cheapest-sufficient discipline; three worked examples; cross-reference to §"No positive grep" as the forbidden case below Layer 1. |
| `skills/architectural-truth-tests.md` §"No positive grep as deployment proof" (earlier today) | The negative discipline; cited as "below Layer 1" in the new section. |
| `skills/testing.md` §"No positive grep deployment checks" (earlier today) | Parallel surface for testing-discipline scope. |

The positive + negative discipline is now complete in the skills.

## Stale / forward / migrate / keep bands by lane

### Designer lane

| Report | Action | Reason |
|---|---|---|
| 459 — Proof-of-usage witness research | DROP-CANDIDATE | The three-layer model + per-layer witnesses + choose-cheapest-sufficient + worked examples are all migrated to `skills/architectural-truth-tests.md` §"Proof-of-usage ladder". Spirit 1341 is the primordial intent record. The two tool-upgrade proposals (architectural-witness cargo subcommand + assert_trait_method_called macro) are future operator-bead work; they don't block the skill landing. The open questions named at end (mutation testing defaults, coverage gates, cargo subcommand build/borrow, witness-catalogue-meets-flake-check) are surfaced as future-design candidates but not gating. |

### Operator lane

No operator reports in this cluster. The negative discipline landings
in `architectural-truth-tests.md` and `testing.md` earlier today were
operator-authored; the positive complement is designer-authored.

## Landing evidence

The substance from designer 459 migrated as follows (specific
section mapping):

| 459 section | Landing in `architectural-truth-tests.md` |
|---|---|
| §"The three-layer model" diagram | §"Proof-of-usage ladder" intro mermaid (5 nodes: Layer 1, Layer 2, Layer 3, strength/cost rise) |
| §"Layer 1 — STATIC witnesses" table | §"Layer 1 — STATIC (compile-time type-system reference)" — six rows, cost columns |
| §"Layer 2 — RUNTIME witnesses" table | §"Layer 2 — RUNTIME (execution path taken)" — six rows, cost columns |
| §"Layer 3 — BEHAVIORAL witnesses" table | §"Layer 3 — BEHAVIORAL (removal breaks observable behavior)" — five rows, cost columns |
| §"The choose-cheapest-sufficient discipline" | §"The choose-cheapest-sufficient discipline" paragraph + the "positive grep sits below Layer 1" connector |
| §"Worked examples — Example 1 (Layer 1 emission)" | §"Worked examples" — "Type T is emitted by the schema chain" |
| §"Worked examples — Example 2 (Layer 2 recorder)" | §"Worked examples" — "Runtime X uses trait method Y" |
| §"Worked examples — Example 3 (Layer 2 process boundary)" | §"Worked examples" — "Daemon round-trips through the wire" |

The migration is comprehensive; every load-bearing element of 459's
research now lives in the skill. The report retires cleanly.

The two tool-upgrade proposals (459 §"Two concrete tool-upgrade
proposals") were NOT migrated to the skill because:

- They're build-tool work, not discipline. A skill encodes how to
  think about proof; tools accelerate it.
- They're not yet built. Premature inclusion would have the skill
  cite a non-existent tool.
- The future operator-bead pickup ledger is the right home (a bead
  per tool when operator is ready to file).

## Drop ownership / handoff

**Designer lane** (this sweep): 459 drops in the commit that lands
the migration.

**Future operator beads** (not gating this sweep): consider filing
beads for:

1. `architectural-witness` cargo subcommand reading a workspace
   `witnesses.toml` catalogue.
2. `assert_trait_method_called!` macro for trait-call-site
   assertions.

These are nice-to-have accelerants; the discipline is what's
load-bearing.

## Open psyche-review items surfaced

The five open questions named in 459 §"Open questions" remain
unsettled but don't gate the skill landing. Surfacing them here for
the orchestrator:

1. **Mutation testing as a workspace default?** Layer 3 is the
   strongest witness but expensive. Worth a focused designer report
   on which architectural claims warrant mutation testing.
2. **Coverage gates as architectural witnesses?** Specific paths
   requiring coverage proof in the witness catalogue.
3. **`assert_called!` vs hand-written fakes?** Trade-off between
   standardization and flexibility.
4. **Architectural-witness cargo subcommand — build or borrow?**
   Could be a thin wrapper over `cargo test --test`.
5. **Witness catalogue / Nix flake check relationship?** Each
   `cargo architectural-witness` invocation as a flake check.

None gate the skill landing; all are candidates for follow-on work.

## Cross-references

- Spirit record 1341 (Constraint Maximum) — the primordial intent.
- `skills/architectural-truth-tests.md` §"Proof-of-usage ladder" — the new landing.
- `skills/architectural-truth-tests.md` §"No positive grep" — the negative discipline (cited as below Layer 1).
- `skills/testing.md` §"No positive grep deployment checks" — parallel surface.
- `skills/skill-editor.md` §"Skills never reference reports" — the discipline that makes 459's retirement safe.
