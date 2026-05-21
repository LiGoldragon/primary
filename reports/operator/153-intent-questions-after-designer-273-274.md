# 153 - Intent questions after designer 273 and 274

Operator report, 2026-05-21. This is a clarification pass after
designer's latest synthesis: `/273` on schema migration, `/274` on
forge skeleton reconciliation, `/268` on persona-pi operator input,
and the current Spirit-vs-file substrate state.

## What I checked

I logged the user's prompt through the deployed Spirit CLI as record
96:

```nota
(RecordAccepted ((96 workspace Clarification "operator should read latest designer synthesis and surface biggest intent questions" Maximum)))
```

I read:

- `reports/designer/273-schema-migration-synthesis-post-operator-151.md`
- `reports/designer/274-forge-skeleton-reconciliation.md`
- `reports/operator/151-spirit-deployed-version-and-schema-migration.md`
- `reports/designer/268-persona-pi-operator-input.md`

I also queried the deployed Spirit daemon and confirmed that the
dual-substrate drift designer flagged is real in practice:

- Spirit has workspace records 74 and 75 for forge family and
  workspace-owned content-addressed store.
- `intent/workspace.nota` does not contain those records.
- The deployed Spirit daemon still rejects `Observe Topics`; the
  current branch supports it, but production is behind that wire
  addition.

That means any operator or subagent that reads only file intent will
miss current design intent, and any agent that assumes current Spirit
wire shape against production will trip over deployed-vs-current
drift.

## Code decision

I did not implement new code in this pass.

The only clearly settled code item from the latest response,
Magnitude, already landed in `signal-sema` and I already migrated
Spirit's `Certainty` consumer. The next possible code slices are not
safe without a design choice:

- `sema-upgrade` can be created only after choosing Shape A/Shape B
  and the first commit-sequence scope.
- `persona-pi` explicitly needs an operator implementation proposal
  before code.
- `forge` has existing crates, but `/274` asks whether to keep them
  as criome-stack executor skeletons and what to do with `Deploy`.
- `signal-persona-mind::ItemPriority` can collapse to `Magnitude`
  only after psyche affirms the semantic merge.

## Biggest intent questions

### 1. Sema-upgrade first, or per-component migration library first?

`/273` gives two convergent implementation shapes:

- Shape A: create the sema-upgrade triad first, then make Spirit's
  migration library the first driven migration.
- Shape B: build Spirit's `schema/current.rs`,
  `schema/version_1.rs`, and `migration/version_1_to_1.rs` first,
  then wrap it with sema-upgrade later.

Designer leans Shape A. I need the psyche call because this decides
whether the next code is a new triad repo family or a focused
Spirit-internal migration library.

My operator lean: Shape A if the goal is to train the workspace on
the real architecture; Shape B only if production Spirit needs a
near-term migration faster than sema-upgrade can be born.

### 2. Commit sequence scope and timing

`/273` says live-copy migration needs a durable high-water mark at
the sema-engine pressure point. Two choices matter:

- scope: one commit sequence per sema database, or per component;
- timing: implement this before sema-upgrade exists, or allow the
  first Spirit migration to use stop-old-start-new and land commit
  sequence before the second migration.

Designer leans per-database and allows stop-old-start-new for the
first production migration.

My operator lean: per-database sequence in sema-engine, but do not
block the very first Spirit storage migration on zero-downtime
machinery if the migration can run in a write-free window.

### 3. Schema visibility: annotation or file placement?

`/273` splits historical types into public signal types and private
runtime storage wrappers. The schema DSL needs to know which family
each record belongs to.

The choice:

- explicit `(public)` / `(private)` visibility annotations in one
  canonical schema artefact;
- infer visibility from where the schema file lives.

Designer leans annotation.

My operator lean: annotation. It avoids treating filesystem layout as
semantic truth, and it lets sema-upgrade hash one canonical component
schema.

### 4. Dual-substrate transition rule

Designer is already logging through Spirit. File intent is now
stale for at least records 74 and 75. The deployed Spirit query also
proved production's wire shape is behind the current branch.

The immediate question:

Until sema-upgrade or a bridge tool closes the transition, should all
agents treat Spirit as the primary intent substrate and file intent
as historical fallback, with a standing rule to query both when
researching current intent?

My operator lean: yes. Any current architecture or implementation
pass should query Spirit first, then files. Reports should cite
Spirit record identifiers when the record is not in file substrate.

### 5. Does `ItemPriority` collapse to `Magnitude` now?

`/269` identifies `signal-persona-mind::ItemPriority` as a strong
collapse candidate. Spirit's `Certainty` is now migrated to
`Magnitude`; mind still has a separate priority enum.

The choice:

- migrate `ItemPriority` to `Magnitude` now;
- keep priority as a distinct domain scale.

My operator lean: migrate it only if psyche explicitly affirms that
priority and certainty share the same seven-rung scale. The code
change is easy; the semantic merge is the important part.

### 6. Persona-pi: proposal priority vs infrastructure priority

`/268` says persona-pi is not implementation-ready. The operator
deliverable is an implementation proposal that closes extension
hooks, signal contract shape, owner contract shape, dual-path
boundary, composite-designer integration, storage, and first-slice
scope.

The question:

Should my next substantive report be the persona-pi implementation
proposal, or should I prioritize sema-upgrade / commit-sequence
foundation first?

My operator lean: sema-upgrade first if the immediate risk is losing
state during fast Spirit iteration; persona-pi proposal first if the
goal is to unlock the composite-designer workflow.

### 7. Forge: keep existing `forge` as criome executor?

`/274` reconciles existing `forge` / `signal-forge` with `/271`.
The biggest decision is whether existing `forge` stays as the
criome-stack executor and `forge-nix-builder` is extracted under it,
or whether existing `forge` becomes the general nix builder and
criome policy moves above it.

My operator lean: keep existing `forge` as the criome-stack executor
and extract `forge-nix-builder` as a library later. Less churn, and
it respects the existing authority model.

### 8. Does `Deploy` belong in `signal-forge`?

`signal-forge` currently has `Build` and `Deploy`; `/271` framed
forge more as build-system family. If deploy stays, forge is a
broader effect executor. If deploy moves, `signal-forge` narrows to
build/store effects and deploy belongs to lojix or another authority
leg.

My operator lean: keep `Deploy` in `signal-forge` for now because
the existing skeleton explicitly frames forge as criome's effect
executor, not only as a builder. Revisit when lojix's daemon
contract is current.

## Recommendation

The two questions I most need answered before code are:

1. Should the next implementation slice be sema-upgrade Shape A
   (new triad first) or Shape B (Spirit migration library first)?
2. Should all current agents treat Spirit as primary intent substrate
   and file intent as historical fallback until a bridge closes the
   dual-substrate gap?

Everything else is important, but those two decide the next operator
work lane and how we avoid rebuilding stale intent into code.

