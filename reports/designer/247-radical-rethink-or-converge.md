# 247 — Radical rethink, or converge?

*The psyche asked whether the whole architecture (signal-frame /
signal-sema / signal-executor / signal-<contract>) should be torn
up — different repos, different engine, different everything.
This report engages honestly: lays out the candidate
alternatives, tests each against existing psyche commitments,
assesses what the current direction is delivering versus failing
to deliver, and recommends.*

## 0 · TL;DR

**Recommendation: hold the current direction; the right pivot is
attention, not architecture.**

The /246 churn (v1 → v2 → v3-in-progress) is **convergence**, not
divergence — each revision corrected a real mechanical gap
surfaced by code-touching analysis (`/140`, `/141`, `/142`). The
infrastructure crates are arriving at the right shape.

But: three sessions on signal-frame / signal-executor /
signal-channel macro grammar is a lot of attention on
infrastructure with no live persona daemon end-to-end yet. The
real risk isn't that the architecture is wrong — it's that
we're polishing the protocol while persona-spirit, persona-mind,
persona-orchestrate, repository-ledger, etc. don't yet
demonstrate value at the cognitive layer.

The pivot worth making: stop iterating on signal-frame for now;
finish the `/246-v3` refinements (small bundle); land
`signal-repository-ledger` as the worked-example pilot end-to-end
with the executor + observability; then let the next round of
infrastructure questions surface from use, not from speculation.

If after the pilot lands the architecture STILL feels wrong,
re-open this rethink.

## 1 · The question

> consider if we should have a completely different approach
> altogether; different repositories, different engine, etc etc

Three axes the psyche's "etc etc" implicitly opens:
- **Different repositories.** Is the signal-frame / signal-sema /
  signal-executor / signal-<contract> split right?
- **Different engine.** Should sema-engine itself be replaced?
- **Different everything.** Language, IPC, storage, runtime
  model.

Engaging each below.

## 2 · What the workspace has committed to (anchor points)

Before considering alternatives, name the commits the psyche has
made that any alternative must honor. From the intent log:

| Commit | Source |
|---|---|
| Persona is a meta-AI system; spirit animates | `intent/persona.nota` 2026-05-19T14:00 + ESSENCE.md |
| Each component is a triad: daemon + thin CLI + signal contract pair | `intent/component-shape.nota` + skills/component-triad.md |
| Contract-local verbs; sema-execution-language separate | `intent/component-shape.nota` 2026-05-19T19:30+ |
| NOTA is the only text format | `skills/language-design.md` Rule 0 |
| Components are LLM-mediated; agents are the thinking layer | `intent/persona.nota` (LLM-mediation intrinsic) |
| Backward compatibility is not a constraint | ESSENCE.md |
| Beauty is the criterion | ESSENCE.md |
| Rust as the implementation language | Implied by current crate ecosystem; no explicit re-commit, but every contract assumes it |

These narrow the space considerably. An alternative that crosses
one of these crosses psyche-stated direction; if the alternative
is right anyway, the commit needs re-evaluation, not just the
architecture.

## 3 · Candidate radical alternatives

Seven alternatives worth thinking through, ranked by how far they
push against current commitments:

### A — Replace sema-engine with a real database (SurrealDB, FoundationDB, EdgeDB)

Sema operations (Assert/Mutate/Retract/Match/Subscribe/Validate)
need an engine. The current direction implies a custom
sema-engine over `redb`. A real DB has solved atomicity, schema
evolution, query planning, change-feed subscriptions.

**What it preserves**: Sema as the wire vocabulary; the verb
spine; per-component contracts; persona-spirit + mind + etc.

**What it breaks**: the custom sema-engine arc retires; redb
might or might not survive depending on the chosen DB.

**Honest assessment**: this is the cleanest "different engine"
move. Sema-engine doesn't fully exist yet — there's a stub. The
abstraction layer (`SemaEngine` trait in signal-executor) holds
the line; the actual engine can be a real DB behind that trait.
Worth considering when the executor implementation work starts
needing real persistence. Not urgent now.

### B — Drop per-component signal-* contracts; use a workspace-wide schema

Instead of `signal-persona-spirit`, `signal-persona-mind`, etc.,
have one workspace schema with all typed records. Components are
just subscribed views.

**What it preserves**: typed records, Sema execution.

**What it breaks**: contract-locality (just affirmed by psyche —
"every domain has its own verbs"); ownership of components;
versioning per component.

**Honest assessment**: crosses a hard commit. Off the table.

### C — Drop signal-frame; use Cap'n Proto or gRPC for IPC

Current direction has a custom length-prefixed rkyv envelope
with a hand-built macro. Cap'n Proto has solved schema +
versioning + RPC. gRPC has solved IPC at scale.

**What it preserves**: the cognitive layer (spirit/mind/etc.),
contract-local verbs (at a different syntactic layer).

**What it breaks**: NOTA as text vocabulary (Cap'n Proto and
gRPC have their own); rkyv (replaced); the macro
(replaced).

**Honest assessment**: NOTA is a hard commit (`skills/language-design.md`
§0 "NOTA is the only text syntax. … No new text formats. Ever").
gRPC/Cap'n Proto cross this. The IPC layer COULD be replaced
under the same NOTA text surface if the wire format is
abstracted — but signal-frame is small enough that the cost of
custom + NOTA-aligned is reasonable. Off the table for now.

### D — Drop Rust

Use a different language with stronger algebraic types (Idris,
Lean) or actor-model native (Erlang, Elixir). The typed-rejection
problem and the macro-as-DSL pattern are easier in some other
languages.

**What it preserves**: nothing structural; the redesign is
total.

**What it breaks**: every existing crate; the ecosystem
investment; the LLM agents' Rust familiarity (agents code in
Rust efficiently; less so in Idris).

**Honest assessment**: nuclear. Cost compounds with every
existing line of Rust. No psyche-stated reason to do this. Off
the table.

### E — Drop the macro; write contracts by hand

The macro is large and growing. Just write each contract crate's
types + codec + frame plumbing by hand.

**What it preserves**: every architectural concept.

**What it breaks**: ~hundreds of lines of boilerplate per
contract; consistency across contracts (the macro enforces
shape).

**Honest assessment**: the macro is delivering real value. Hand-
writing every contract would not just slow implementation — it
would invite drift across components. The macro is the
discipline carrier. Keep it.

### F — Replace per-component daemons with agents-inside-persona-mind

Instead of daemons with sockets + Lowering impls, all components
are agents running inside persona-mind. Mind is the universal
substrate; components are typed views.

**What it preserves**: persona-as-meta-AI; spirit / mind / etc.

**What it breaks**: component-triad (`skills/component-triad.md`
is the most-cited skill in the workspace); per-component
isolation; the daemon-as-process boundary.

**Honest assessment**: this is the deepest critique. If the
endgame is everything-in-mind (the eventual self-hosting form
the workspace gestures at), then today's per-component daemons
are transitional. But: the psyche has clearly said
component-triad is the universal stateful component shape. The
transitional shape is the right shape for today's needs.

Worth holding open as a future evolution. Not for now.

### G — Synchronous everywhere

Drop async/await. Daemons run synchronous; requests queue. Simpler
mental model, simpler executor.

**What it preserves**: most of the stack.

**What it breaks**: subscription streams, long-running observation,
concurrent client handling.

**Honest assessment**: persona components need to serve multiple
agents concurrently and stream observation events. Sync wouldn't
serve this. Off the table.

## 4 · What the /246 churn actually shows

Three revisions in one session is a lot. Is it convergence or
divergence?

| Revision | What changed | What drove the change |
|---|---|---|
| v1 → v2 | Hole 3 from `Lowering`-with-projection to separate `ObservationProjection` + `FrameObserverBridge` | `/141` analysis: separation of concerns; daemons that don't observe don't pay |
| v2 → v3 (in progress) | `AcceptedOutcome::Aborted` splits into `OperationAborted` + `BatchAborted`; engine fail stays in `Reply::Accepted`; `ObservedLowering: Lowering` extension trait; drop `Lowering::EngineError` | `/142` logic probe in real Rust code: surfaced fake `failed_at: 0` for engine errors; clean trait inheritance |

Each revision was driven by code-touching analysis, not by
shifting goalposts. Each was a real improvement. The design is
**arriving at its right shape** — exactly the ESSENCE-stated
beauty criterion: the structure clarifies itself through
iteration.

If three revisions surfaced three corrections, that's evidence
the design is sound and the iterations are convergent.
Divergent design would produce conflicting revisions (revision N
contradicts revision N+1's premise). That's not what's
happening.

## 5 · What's actually missing

The infrastructure is converging. What's NOT converging:
**end-to-end persona-component value**.

The workspace has:
- ✓ signal-frame: real crate, macro works.
- ✓ signal-sema: real crate, verbs + patterns.
- ✓ signal-executor: real crate, Lowering + Executor + observer integration.
- ✓ Two settled pilot contracts (signal-repository-ledger
  request side; spirit's IntentEntry-to-Entry rename pass).
- ✓ Migration plan + skill discipline.
- ✗ **No daemon end-to-end exercising the full stack.**
  - repository-ledger daemon exists but hasn't migrated to signal-frame yet.
  - persona-spirit daemon exists but is partial (no Lowering impl yet; no observable wiring).
- ✗ **No live observer subscription against a real daemon.**
- ✗ **No demonstration that the architecture serves the cognitive
  layer (intent capture; mind queries; orchestrate work-graph).**

The cost of three more revisions of infrastructure isn't lost
work — but it IS delayed feedback from the cognitive layer
where the real architectural pressure lives. The architecture's
real test is whether intent flows from spirit to mind cleanly,
whether mind can answer queries, whether orchestrate routes
work. None of those are tested by another macro grammar
refinement.

## 6 · Verdict

The current direction is on track architecturally; the right
pivot is attention.

**Action**:

1. **Finish `/246-v3` refinements as a small bundle** —
   `AcceptedOutcome` split, `ObservedLowering: Lowering`
   extension, engine-fail stays in Accepted+BatchAborted, drop
   `Lowering::EngineError`. This is ≤ a day of operator work.
2. **Pivot to the pilot**: complete `signal-repository-ledger` +
   `repository-ledger` end-to-end per `/241` Phase 2. The
   pilot exercises the full stack; whatever holes remain in
   the infrastructure surface there.
3. **Then evaluate** whether the architecture is still right.
   The pilot tells us more than any number of designer
   reports.

If the pilot reveals structural problems that can't be
incremental-fixed, re-open this rethink with new evidence. If the
pilot lands cleanly, the architecture is validated and we move
to Phase 3.

**What I'm NOT recommending**:
- Tearing up signal-frame / signal-executor / signal-sema.
- Replacing sema-engine with a real DB now (defer until executor
  implementation needs persistence).
- Changing IPC, language, or runtime model.
- Adding more macro-grammar features beyond what `/246-v3` calls
  for.

The architecture is at a checkpoint. The right next move is to
DEMONSTRATE it works at the cognitive layer, not to keep
polishing it at the infrastructure layer.

## 7 · One open question for the psyche

If you disagree — if there's a specific structural concern that
prompted "completely different approach altogether" that I
haven't surfaced here — name it. The seven alternatives in §3
cover the moves I can think of, but I'm not seeing the
architecture failing in a way that demands tearing up.

If the prompt was rather a check ("are you still aware of the
alternatives?" rather than "go pick one"), then the answer is
yes — they're on the table; the verdict is "not now."

## 8 · References

- `reports/designer/246-v2-bundled-fix-deep-design-with-examples.md` —
  the current direction's design spec.
- `reports/operator/142-signal-frame-executor-bundled-fix-logic-probe.md` —
  the code-probe that revealed v3 refinements.
- `reports/designer/241-signal-architecture-migration-guide.md` —
  the migration plan; Phase 2 is the pilot.
- `intent/component-shape.nota` — anchor points for the
  current direction.
- `ESSENCE.md` — beauty is the criterion; backward compatibility
  is not a constraint.
- `skills/component-triad.md` — the universal stateful component
  shape (heavily committed).
- `skills/language-design.md` Rule 0 — NOTA is the only text
  format.
