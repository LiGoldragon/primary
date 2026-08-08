---
title: 311 - Cycle - day review and new Spirit production readiness
role: operator
variant: Cycle
date: 2026-06-04
topics: [spirit, persona-spirit, schema-next, schema-rust-next, triad-runtime, production-readiness, runner, sema, meta-signal, verification]
description: |
  End-of-day operator cycle review: what landed, what remains important,
  where the schema-derived Spirit stands relative to production Spirit, which
  design problems are still hard, and the questions that should steer the next
  cycle.
---

# 311 - Cycle - day review and new Spirit production readiness

## Executive read

This was a high-movement day. Several things that were still described as
unbuilt in the morning reports are now landed on main:

- `schema-next` loads multiple schema modules per package and preserves the
  resolver through nested imports.
- `schema-rust-next` owns the shared generation driver, per-plane runtime
  emission, daemon-local `SignalRuntime`, and the generated Nexus runner
  adapter.
- `triad-runtime` owns the shared recursive Nexus runner core:
  `Runner`, `NextStep`, `RunnerEngines`, `ContinuationLimit`, and
  `ContinuationExhausted`.
- `spirit` is now the canonical schema-derived Spirit repo, split into
  `schema/signal.schema`, `schema/nexus.schema`, and `schema/sema.schema`,
  generated into `src/schema/{signal,nexus,sema}.rs`, and running through
  `sema-engine` over `.sema`.
- `cloud` and `domain-criome` are no longer just carrying authored schemas:
  their `build.rs` files now call the shared daemon-runtime generation driver
  against ordinary and meta signal contract metadata.

So the day did not merely settle design. It moved the substrate. The old
critical path `driver -> spirit split -> core runner` is mostly closed. The
new critical path is `daemon runner shell -> production parity/migration ->
separate real signal/meta-signal Spirit repos -> cutover proof`.

The current production Spirit is still `persona-spirit`. It is also currently
dirty in its local checkout with migration-related edits
(`Cargo.toml`, `flake.nix`, `src/migration.rs`, and
`src/bin/spirit-migrate-0-5-to-0-5-2.rs`). I did not touch or commit that
checkout for this report; the state matters because production Spirit should
not be treated as clean or idle.

## What landed today

### Schema substrate

`schema-next` main is at commit `b14d14f7` (`schema-next: preserve resolver
through nested imports`). The important landed pieces are:

- multi-module loading (`load_modules`) for packages with several `.schema`
  files;
- package self-registration so sibling plane schemas can import each other;
- nested import resolver preservation, needed when one imported plane imports
  another plane beneath it.

The live concern in `schema-next` is not the loader anymore. It is bead
`primary-vllc` (dual-lowering bare-header bug): the registry lowering path
still lowers a bare PascalCase enum variant to payload `None`
(`src/declarative.rs:1846-1850`), while the `SchemaSource` path resolves a
same-named namespace payload (`src/source.rs:765-772`). That is the biggest
Schema correctness issue because it means the two lowering routes can silently
disagree on whether a root/header variant carries data.

`schema-rust-next` main is at commit `e7d5f395` (`schema-rust: allow generated
plane namespace modules`). The important landed pieces are:

- `RustEmissionTarget::SignalRuntime`, so the daemon-local signal schema emits
  `SignalEngine` while public contracts remain `WireContract`;
- `GenerationPlan` / `ModuleEmission` / `GenerationDriver`, so component
  `build.rs` files do not hand-roll schema orchestration;
- generated `NexusRunnerAdapter` and total `NexusAction -> NextStep`
  projection, so the recursive loop can live in `triad-runtime`;
- runtime-module feature gating so generated runtime files can stay binary
  daemon nouns unless a NOTA surface is opted in.

The live concern in `schema-rust-next` is now cleanup and correctness, not the
main architecture: bead `primary-j0wo` says self-package imports emit
`spirit::...` and require the workaround `extern crate self as spirit;` in
`spirit/src/lib.rs`; bead `primary-myku` asks for the Rust item token model so
the emitter stops being hundreds of hand-indented string writes.

### Runtime substrate

`triad-runtime` main is at commit `e40d1e96` (`triad-runtime: narrow runner
read callbacks`). It now owns:

- the length-prefixed binary frame codec;
- the single-NOTA-argument classification noun (`ComponentCommand` /
  `ComponentArgument`);
- typed trace frames and trace socket support;
- the shared recursive Nexus runner core in `src/runner.rs`.

The runner core is real and small: `Runner::drive` loops over exactly five
outcomes (`Reply`, `SemaWrite`, `SemaRead`, `RunEffect`, `Continue`) and
spends a typed continuation budget before every non-reply step. The component
supplies a typed budget-exhausted reply instead of panicking.

What did not land is the full daemon shell: listener binding, stale socket
cleanup, transport handoff, generated one-line main, meta listener handling,
and the single engine-owner loop for multiple listeners. I opened
`primary-es8u` (extract daemon listener/startup runner beyond Nexus loop) to
track this separately from the closed core-runner bead.

### New Spirit

`spirit` main is at commit `8d0e32cf` (`spirit: split runtime schemas by
plane`). The current shape is the cleanest schema-derived Spirit has had:

- `build.rs` calls `GenerationPlan::new(...).with_module(signal_runtime)
  .with_module(nexus_runtime).with_module(sema_runtime)`.
- `schema/lib.schema`, `schema/lib.asschema`, and `src/schema/lib.rs` are gone.
- `schema/{signal,nexus,sema}.schema`, matching `.asschema` files, and
  `src/schema/{signal,nexus,sema}.rs` are checked in.
- `SignalRuntime`, `NexusRuntime`, and `SemaRuntime` are distinct generated
  planes.
- `Store` uses `sema-engine` over `*.sema`; the daemon has no direct redb
  dependency in its runtime code.
- `NexusEngine::execute` now delegates to the generated runner adapter and
  `triad_runtime::Runner`, while handwritten Nexus implements only the
  decision step, SEMA read/write hooks, effect hook, and budget-exhausted reply.
- Tests cover real `.sema` durability, process boundary, typed trace, and
  binary daemon/text CLI separation.

This means report 514's "no SignalEngine emission home" problem is resolved
by the distinction in report 515: public signal contract schema emits
`WireContract`; daemon-local `schema/signal.schema` emits `SignalRuntime`.

### Cloud and domain-criome

`cloud` and `domain-criome` both now use the shared driver in `build.rs`:

- `cloud/build.rs` reads `signal-cloud` and `meta-signal-cloud` schema
  metadata, then builds a `GenerationPlan::daemon_runtime(...)`.
- `domain-criome/build.rs` reads `signal-domain-criome` and
  `meta-signal-domain-criome` metadata, then builds the same daemon runtime
  plan.

Their remaining problem is runtime maturity, not schema wiring. Both still
defer real sema-engine persistence/provider work in their architecture. The
runtime daemon beads remain live, especially `primary-kbmi.2` for
domain-criome.

## Production readiness of the new Spirit

### What is strong enough now

The new `spirit` is a credible development pilot and the current exemplar for
the three-plane runtime shape. It has crossed the line from "concept" to
"running schema-derived daemon":

- generated wire, Nexus, and SEMA types are in the runtime path;
- the daemon receives binary frames and does not parse NOTA;
- the CLI is the text edge and emits binary signal frames to the daemon;
- storage is durable through `sema-engine` and `.sema`, not raw redb in daemon
  code;
- the recursive Nexus loop is shared library code, not a 47-line handwritten
  loop inside `decide`;
- the process-boundary tests prove the daemon/CLI boundary and `.sema`
  durability.

That is enough to keep building the next production Spirit on this repo. It is
also enough to stop treating `spirit-next` as a separate future thing: the repo
is `spirit`; older `spirit-next` names are compatibility or historical cleanup.

### What blocks production cutover

It is not ready to replace `persona-spirit` in production.

The missing pieces are not cosmetic:

1. **Full daemon runner shell.** `spirit/src/daemon.rs` still owns generic Unix
   socket binding, stale socket removal, accept-loop mechanics, and transport
   handoff. The core Nexus runner landed, but the daemon-level runner is still
   the next extraction.

2. **Real triad repo boundary.** The pilot still keeps its signal schema inside
   the daemon repo. Production shape wants `spirit` plus a real
   `signal-spirit` and `meta-signal-spirit`. Existing `signal-spirit` is a
   small MVP surface and does not match the six-operation pilot surface.

3. **Meta policy leg.** New Spirit has no production meta-signal policy path
   equivalent to the policy/supervision side of `persona-spirit`. The naming is
   now meta, not owner, but the old production repository still contains many
   legacy owner-signal strings because it is the deployed stack.

4. **Production feature parity.** We have not produced a fresh parity matrix
   after the split and runner work. At minimum the cutover has to reconcile
   current production features around identities/policy, version handover,
   short identifiers, privacy/certainty changes, removal/archive behavior, and
   migration binaries.

5. **Data migration.** `persona-spirit` still uses a sema-engine database named
   `persona-spirit.redb` in production docs/code. New `spirit` uses `.sema`.
   There is no completed production data migration from existing production
   records into the new `.sema` store.

6. **Schema upgrade/diff.** `spirit/ARCHITECTURE.md` still names generated
   `UpgradeFrom` / `AcceptPrevious` as present but unimplemented. Production
   replacement needs a real previous-version boundary, not only a copy-test of
   the current store.

7. **Verification speed.** `scripts/check-local-schema-stack` currently
   executes a full `nix flake check` with local overrides. A run that sat for
   about 27 minutes and was interrupted is a failed or suspect verification,
   not a soft caveat. I opened `primary-vjl5` (split slow Spirit local-stack
   verification into fast and full checks) for a fast consumer check plus a
   named slow full-flake path with progress/timeout expectations.

## Important unfinished work

### P1: Schema correctness before more fan-out

Fix `primary-vllc` (schema-next dual-lowering bare-header bug). This is the
most conceptually dangerous open item because Schema is supposed to become the
codec and source of truth. If two lowerers disagree about whether a bare header
carries a payload, then the shorthand/sugar surface is not reliable enough to
be multiplied across components.

The fix should lean toward one correct lowering path, not patching symptoms in
both. The current better path is `SchemaSource`, because it knows the namespace
and has the rule that a bare variant can resolve to a same-named payload.

### P1: Daemon runner shell

Do `primary-es8u` next after the cycle report. The core recursive runner is
done; the remaining extraction is the host-shell machinery every daemon would
otherwise copy:

- configuration loading from one binary argument;
- listener binding and stale socket cleanup;
- length-prefixed frame transport;
- ordinary plus meta listener shape;
- lifecycle order;
- one engine-owner loop when there are multiple listeners.

This is where strict engine separation becomes structurally enforced. If every
daemon still hand-writes its own `daemon.rs`, the audit surface remains open.

### P1: Wire vocabulary cleanup

`primary-d4h5` (rename remaining legacy owner-signal policy repos to
meta-signal) and `primary-ka39` (remove Sema classification words from public
contract wires) are still important. They are not blocking the new `spirit`
compile, but they block clean conceptual propagation. A public contract that
says SEMA words or old owner naming keeps teaching agents the wrong boundary.

### P1/P2: Production Spirit parity and migration

`persona-spirit` remains production and has active migration work in the local
checkout. Relevant open items:

- `primary-u4tl` integrates production cleanup commits in `persona-spirit`;
- `primary-dn1e` adds `ChangePrivacy`;
- `primary-ohpk` adds a prominent production marker so agents stop editing the
  wrong Spirit;
- the current dirty 0.5.2 migration work needs an owner/operator finish or
  handoff.

The production migration question is larger than any one of those beads:
what exact shape moves current production Spirit data and semantics into the
schema-derived `.sema` stack?

### P2: Emitter shape and cleanup

`primary-j0wo` should remove the `extern crate self as spirit;` workaround by
emitting `crate::...` for self-package imports. `primary-myku` should move
schema-rust-next toward a Rust item/impl/match token model so indentation and
emission structure are owned once instead of spread across string writes.

These are not production blockers by themselves, but they reduce error rates
before more components copy the generator output.

### Cloud/domain-criome and peripheral SEMA adoption

`cloud` and `domain-criome` now have real generated runtime schema artifacts.
The next work is making their runtime behavior real: sema-engine persistence,
provider IO, meta policy application, and domain authority behavior.

`primary-y0ec` remains the peripheral sema-engine boundary track. Its notes say
`chroma` has a next-branch sema-engine fix, `orchestrator` should likely retire,
and `schema-next`'s redb-backed `AsschemaStore` still needs an explicit adopt
or exempt decision.

## Hardest design problems still open

### 1. Signal has two meanings, and agents will keep collapsing them

The distinction is now implemented, but it remains cognitively fragile:

- public contract repo signal schema: `WireContract`, no engines;
- daemon-local `schema/signal.schema`: `SignalRuntime`, emits
  `SignalEngine`.

This is correct and future-oriented. It is also easy to misstate. Every future
port and report should explicitly say which signal schema it means.

### 2. The runner must not become a fourth engine

The runner owns mechanism: loop, listener, lifecycle, budget, and handoff.
It does not own communication semantics, decision semantics, or database
semantics. That boundary is still hard because the remaining daemon shell
touches sockets, Signal admission, Nexus execution, and SEMA lifecycle in one
place.

The safe next implementation is phase-based:

- finish one-listener daemon shell for `spirit`;
- then add ordinary plus meta listener shape with listener threads only
  decoding and handing accepted work to one engine-owner loop;
- defer real scheduler/backpressure until there is evidence.

### 3. SEMA engine has to match the architecture, not just absorb calls

The user intent is strict: SEMA owns database work, hides redb behind `.sema`,
and the daemon should not contain database boilerplate. New `spirit` now does
that better than earlier pilots, but sema-engine API pressure remains:

- numeric record identifiers and rich topic/privacy predicates need first-class
  support where they are truly generic;
- component-specific predicates should stay component-specific;
- `.sema` must be the visible file type;
- raw redb in component daemons should be treated as boundary drift unless
  explicitly exempted.

The ideal future is sema-engine as the database kernel every daemon uses, with
component SEMA schemas mapping generated domain roots onto kernel operations.

### 4. Schema as codec requires one authoritative lowering

The goal is bigger than "emit Rust." Schema should be its own codec, with a
shorthand authored language that lowers reliably to typed artifacts and then to
Rust/rkyv/NOTA surfaces. That makes the dual-lowering bug and the sugar syntax
gap urgent. Until one path is authoritative, every new shorthand creates a risk
that two paths treat it differently.

The same concern applies to Rust emission: string-writing works for now, but a
Rust item token model is the right shape before the generator grows much more.

### 5. Production migration is not just code migration

The new Spirit can break development freely, but production contains durable
human intent records. The cutover design must answer:

- how current `persona-spirit` records migrate;
- whether old identifiers remain meaningful;
- which privacy/certainty/update operations must preserve timestamps;
- how version handover and rollback work;
- whether production keeps a `spirit-next` deployment slot during handover.

This is likely the most consequential non-generator design problem left.

## Most important questions

1. **Cutover threshold.** Should new `spirit` be allowed to replace
   `persona-spirit` only after real `signal-spirit` and `meta-signal-spirit`
   repos exist and the daemon imports them, or is a single-repo pilot acceptable
   for an early controlled replacement? My lean: no production replacement
   until the repo triad and meta path are real.

2. **Production parity list.** Which production Spirit features are mandatory
   for first cutover? My proposed minimum is record/observe/lookup/count/remove,
   certainty and privacy mutation, short identifier display, removal/archive
   behavior, version handover, and a migration path from current production
   storage.

3. **`signal-spirit` direction.** Should we replace the current MVP
   `signal-spirit` with the six-operation wire surface now generated inside
   new `spirit`, then create `meta-signal-spirit` beside it? My lean: yes, but
   after the daemon-runner shell is underway so the generated contract does not
   bake another temporary runtime shape.

4. **Verification standard.** Should any local-stack check that is silent past a
   fixed threshold, for example ten minutes, be treated as failed unless it
   announces a known heavyweight build? My lean: yes. A 27-minute interrupted
   run is not useful evidence.

5. **Production storage migration.** Do we first move production
   `persona-spirit` toward `.sema` naming and migration discipline, or leave it
   stable and build a one-time exporter/importer into the new `spirit` store?
   My lean: avoid churning production storage until the new cutover path exists,
   then migrate explicitly.

## Suggested next cycle

1. Fix `primary-vllc` first, because Schema correctness underwrites every
   generated component.
2. Implement `primary-vjl5`, the fast local-stack verification split, so every
   later step has a falsifiable check that does not take an unbounded flake
   matrix detour.
3. Implement `primary-es8u`, the daemon-level runner shell beyond the landed
   Nexus loop, with `spirit` as the reference consumer.
4. Do a fresh production parity audit: current `persona-spirit` main plus its
   dirty migration work versus new `spirit` main after the split.
5. Decide and then build the real `signal-spirit` / `meta-signal-spirit` repo
   boundary.
6. Only then talk about replacing production `persona-spirit`; until then,
   `spirit` is the correct next implementation, not the production daemon.

## Verification status

Verified by inspection for this report:

- `spirit`, `schema-next`, `schema-rust-next`, `triad-runtime`, `cloud`, and
  `domain-criome` are clean on their current checkouts.
- `persona-spirit` is dirty with migration-related edits; I did not modify it.
- Primary now has two new beads: `primary-es8u` for the daemon-level runner
  shell and `primary-vjl5` for local-stack verification speed/falsifiability.

I did not rerun the full Rust or Nix suites for this report. The report is a
cycle review over already-landed work plus source/bead inspection. The one
verification claim I do make strongly is negative: the interrupted
`scripts/check-local-schema-stack` run is not passing evidence.
