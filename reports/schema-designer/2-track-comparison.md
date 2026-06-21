# Schema-help: designer vs operator track comparison

*schema-designer · report 2 · compares this lane's design
(`reports/schema-designer/1-…`) against schema-operator's
(`reports/schema-operator/1-…`) for the double-implementation
convergence.*

## Current state — both tracks are pre-implementation

| | schema-operator | schema-designer (me) |
|---|---|---|
| Research report | ✓ (3 commits, newtypes preserved) | ✓ (report 1) |
| Branch set in `~/wt` | ✓ 5 branches pushed (`schema-help`) | branch `schema-help-design` not yet cut |
| Feature **code** landed | **none** (one 9-line `INTENT.md` doc on schema-rust-next) | **none** (POC baseline in `/tmp`, not on a branch) |
| Test plan | ✓ concrete, tied to spirit's real harness | golden-spec sketch only |
| Rendering model | converged (see below) | converged |

Neither has written the feature. The branches `schema-next`,
`signal-spirit`, `meta-signal-spirit`, `spirit` are byte-identical to
`main`; only `schema-rust-next` carries a doc paragraph. So this is the
*right* moment to converge — before either of us writes code against a
divergent shape.

## Where we agree (the rendering model — settled)

Both reports now state the same thing, matching Spirit `6th4` and the
chat exchange:

- Generate help from schema structure, don't hand-maintain it.
- `nota-text` as the (first) gate; typed, rkyv-serializable help datatype.
- Recurse to scalar leaves **through newtypes**; parent shapes keep the
  newtype nouns (`Entry { Domains Kind Description … }`), scalars surface
  only at the newtype boundary (`(Description String)`, `(Count Int)`).
- `(Vec SomeThing)` keeps `SomeThing` a named reference; `(Help SomeThing)`
  expands it.
- Spirit as pilot, mentci later.

This is full convergence on *what help looks like*. No daylight.

## The one real divergence — where Help is resolved

| | schema-operator | schema-designer |
|---|---|---|
| Help in the contract | a **generated `Input::Help` root** + `HelpReported` output root | **not a daemon root**; a client-side `(Help X)` recognizer |
| Who answers it | the **daemon** handles `Input::Help` (no SEMA), round-trips over the socket | the **CLI** answers locally from the embedded schema; nothing hits the socket |
| Producing the model | **codegen**: emit help nouns/variants in schema-rust-next | **runtime projection**: parse the embedded `*_SCHEMA_SOURCE` via `schema_next::from_schema_text` |

These are linked: "Help is a generated root" *requires* codegen (the
variant must be in the generated enum); "client-side only" is served by
runtime projection + a small recognizer.

**Operator's rationale** (strong): uniformity — if `Help` is just another
root, the datatype, `FromStr`, `Display`, rkyv frame, and route enums all
fall out of the existing generation machinery with zero special-casing,
and the CLI dispatches it exactly like every other command.

**Designer's rationale** (strong): Help is *static contract metadata the
CLI already fully possesses*. A socket round-trip adds a network
dependency for purely-local introspection (you want `Help` to work when
the daemon is down or unconfigured), and putting `Help` in the daemon's
`Input` enum pollutes the domain contract with a reflection verb the
psyche framed as "only used by clis and text clients." Runtime projection
also makes drift impossible (Help *is* the parsed schema) for a ~6-line
accessor.

### Synthesis (my recommendation) — take both wins

Generate `Help` / `HelpReported` as roots **so the datatype, codec, and
rkyv fall out uniformly** (operator's win), but have the **CLI resolve
`(Help X)` locally** from the embedded schema and *not* send it to the
socket (designer's win: offline, fast, no reliance on daemon state). The
daemon *may* also implement `Input::Help` as a no-SEMA reflective handler
for completeness/other clients — it can build the same rkyv `HelpModel`
(via `from_schema_text`, available in the daemon build) and return it for
the client to render — but the CLI does not depend on that round-trip.

The datatype is identical either way; only the CLI dispatch policy and
whether the daemon also answers differ. So convergence is cheap. The one
question that genuinely needs the psyche: **does `Help` belong in the
daemon's `Input` contract at all, or stay a pure client-side concern?**
(It bears on the "only used by clients" intent.)

## Two things operator's track has that mine should adopt

- A **concrete test plan** wired to spirit's real harness
  (`process_boundary` production-copy pattern, ignored `nix_integration`
  tests, `generated_signal_plane`) — stronger on the ops/test side (their
  lane). I should write my golden specs *against* those layers, not a
  parallel harness.
- The explicit **`(Help Version)` command→reply** question (their Q4):
  worth deciding deliberately — I lean "show the channel relation
  `Version → VersionReported VersionReport`," since the signal channel is
  the meaningful unit and the one-level renderer prints it as one line.

## Two things my track has that operator's should adopt

- The **runtime-projection production path** + the two code-grounded traps
  (`UnresolvedImportCrate` at `resolution.rs:233` ⇒ use `from_schema_text`;
  project from the `Source*` AST; verify the pinned container-head
  spelling). If we keep codegen instead, these still matter for whatever
  builds the model.
- The **client-side resolution** argument above.

## Do I need to further-implement and test with spirit?

Recommendation: **no full parallel spirit integration — that duplicates
schema-operator's lane and harness.** The efficient division, given both
tracks:

1. **First, pin the one divergence** (Help-as-daemon-root vs
   client-side). Until that is decided, neither track should write the
   pilot — they'd diverge on the contract shape.
2. **My track delivers**: a self-contained **compiled POC** (the
   one-level renderer + rkyv round-trip + the golden `(Help …)` trace,
   both the daemon rkyv-only and CLI nota-text builds) on my
   `schema-help-design` branch — that is my "own version" and the
   comparison baseline — **plus falsifiable golden-spec tests** in
   `signal-spirit/tests/` that pin the exact `(Help X)` outputs.
3. **schema-operator implements** the spirit pilot and runs the prod-db
   nix-sandbox integration (their harness, their lane). My golden specs
   are the bar their implementation must clear; I then **audit** their
   landing against the design.

This honors "implement your own version" (my POC proves the model and is
independently testable) without a wasteful second full spirit integration.
If the psyche specifically wants *two* independent spirit-pilot
implementations both run against a prod-db copy for maximum anti-drift, I
can — but I'd flag the duplication cost first.
