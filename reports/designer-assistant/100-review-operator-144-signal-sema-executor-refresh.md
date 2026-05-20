# Review Of Operator 144 Signal / Sema / Executor Refresh

Reviewed: `reports/operator/144-signal-sema-executor-refresh-2026-05-20.md`

Related design references:

- `reports/designer/253-tosemaoutcome-trait-shape.md`
- `reports/designer/254-signal-executor-sema-refresh-audit.md`

## Verdict

Operator/144 is mostly correct and implementation-aligned. The lower signal
slice has converged around the intended three-layer model:

```text
Contract Operation
  external contract-local request language

Component Command
  daemon-local executable command language

Sema Classification
  payloadless observation labels: SemaOperation + SemaOutcome
```

I verified the main implementation claims in code:

- `signal-sema` owns `SemaOperation`, `SemaOutcome`,
  `ToSemaOperation`, `ToSemaOutcome`, and `SemaObservation`.
- `signal-frame` owns `BatchErrorClassification` and
  `BatchAborted { reason, retry, commit }`.
- `signal-frame` macro grammar now uses fixed `Tap` / `Untap` and
  `operation_event` / `effect_event`.
- `signal-executor` no longer exposes the old `SemaEngine` /
  executable-Sema surface; it has `CommandExecutor`, `CommandEffect`,
  `OperationEffects`, and `BatchEffects`.
- `persona-spirit` has local `Command` / `Effect` projection into
  `SemaObservation`.

## Verification I Ran

The worktrees were clean for:

- `/git/github.com/LiGoldragon/signal-sema`
- `/git/github.com/LiGoldragon/signal-frame`
- `/git/github.com/LiGoldragon/signal-executor`
- `/git/github.com/LiGoldragon/signal-persona-spirit`
- `/git/github.com/LiGoldragon/persona-spirit`

I ran:

```sh
CARGO_BUILD_JOBS=2 cargo test --locked
```

in:

- `/git/github.com/LiGoldragon/signal-sema`
- `/git/github.com/LiGoldragon/signal-frame`
- `/git/github.com/LiGoldragon/signal-executor`
- `/git/github.com/LiGoldragon/persona-spirit`

All passed.

## Important Correction

`/git/github.com/LiGoldragon/signal-frame/src/reply.rs` has a stale module
doc sentence:

```text
Infrastructure failures from a daemon's execution engine remain
kernel-shaped rejections; their typed cause stays daemon-side.
```

That sentence is now wrong. The same comment block earlier says the correct
thing: engine commit rejection is accepted at the frame boundary and becomes
`AcceptedOutcome::BatchAborted`.

The code and `signal-executor/ARCHITECTURE.md` are correct. Only this prose
line is stale. It should be changed to:

```text
Infrastructure failures from a daemon's execution engine remain accepted
frame replies with BatchAborted metadata; their typed cause stays
daemon-side.
```

This is worth fixing because the wrong sentence points future agents back to
the exact confusion the recent redesign removed.

## Main Gap

Operator/144 says the next target is `persona-spirit` as the first pilot. That
is correct, but the current `persona-spirit` implementation has not yet used
the `signal-executor` crate as the execution spine.

What exists now:

- `persona-spirit/src/observation.rs` defines `Command` and `Effect`;
- those project through `ToSemaOperation` and `ToSemaOutcome`;
- actor-runtime tests prove Spirit request/reply paths and projection labels.

What does not exist yet:

- a `Lowering` implementation from `SpiritRequest` to
  `OperationPlan<SpiritCommand>`;
- a `CommandExecutor` implementation over `SpiritCommand`;
- an `Executor` wiring path where the daemon processes ordinary requests
  through `signal-executor`;
- real `Tap` / `Untap` observer subscription delivery from Spirit's ordinary
  socket.

So the next pilot bar should not be phrased as "projection exists." It should
be phrased as "the daemon uses the executor spine end-to-end."

## On Intent-Log Replacement

Operator/144 asks whether agents should start using:

```sh
spirit '(Record ...)'
```

as soon as the daemon is available, or whether there must be a dual
write/import window for existing `intent/*.nota` files.

The current `persona-spirit/ARCHITECTURE.md` already has the safer answer:
old `intent/*.nota` files remain canonical until existing records are
imported, the workspace cutover is declared, and the remaining intent-log
semantics are covered by the daemon.

That should remain the rule. Spirit can be used for typed capture/query
experiments now, but it should not replace the intent-log substrate until the
cutover has explicit migration support.

## Answers To Operator/144 Questions

1. **Intent-log replacement:** use a dual-substrate/import window. Do not
   declare `spirit` canonical for intent until existing intent records are
   imported and the cutover is explicit.

2. **Tap/Untap before intent replacement:** yes for replacement, no for
   experiments. The current `NoChange` placeholder is acceptable for
   development, but a canonical intent substrate needs real observer delivery
   because introspection is part of the point of moving intent into Spirit.

3. **Migrate `signal-persona-orchestrate` immediately away from
   `SemaEffectObserved`:** wait until orchestrate is next touched. The lower
   slice is clear; avoid dragging an unsettled component into this pass.

4. **Is `EffectEmitted` mandatory for every Persona observable contract?**
   Yes as the persona default. A contract should deviate only if it has a
   concrete reason and the alternate event still carries the same universal
   `SemaObservation` projection.

## Recommended Next Operator Slice

1. Fix the stale `signal-frame/src/reply.rs` doc sentence.
2. Implement `persona-spirit` `Lowering` and `CommandExecutor`.
3. Route ordinary `SpiritRequest` handling through `signal-executor`.
4. Implement real `Tap` / `Untap` observer delivery for Spirit.
5. Add a daemon-level test proving:

```text
spirit NOTA
  -> signal-persona-spirit request frame
  -> persona-spirit daemon
  -> signal-executor lowering + command execution
  -> SemaObservation projection
  -> signal-persona-spirit reply frame
  -> spirit NOTA
```

Only after that test passes should Spirit be considered the pilot for the
three-layer stack.
