# 727 — Thin end-to-end guard proof: built green + parallel-lane finding

The psyche said "do it" — the thin end-to-end proof from `726`/`725` Q4 is built
and green on a designer feature branch. Building it surfaced a parallel-lane
convergence with operator and one schema design finding worth feeding back.

## What landed (designer demonstrator)

Branch `workflow-engine-thin-slice` (orchestrate), commit `8cacad8` "orchestrate:
thin end-to-end workflow engine — real agent-effect dispatch + criome proof",
based on operator's main `bfe4f6d`, pushed; **remote main untouched**.

- **orchestrate gains the effect plane** (`schema/nexus.schema`): `NexusWork +=
  EffectCompleted(EffectOutput)`, `NexusAction += CommandEffect(EffectInput)`,
  `EffectInput[(CallAgent AgentStepCall)]`, `EffectOutput[(AgentStepCompleted
  AgentStepResult)]` — mirroring agent's own `CallProvider` seam. build.rs adds
  signal-agent as a third dependency schema.
- **`WorkflowEngine`** (`src/workflow_engine.rs`) actually dispatches a step to
  the **agent** component (FixtureProvider, offline) with a NOTA-output guardian
  prompt (`OutputMode::Nota`, `ReasoningEffort::High`, `ThinkingMode::Enabled`),
  awaits the completion off the mailbox, parses it to a real
  `signal_criome::EvaluationDecision`, combines via `CombinationRule`, and builds
  the **unsigned local-plane `WorkflowReceipt`** (`ic4o`).
- **Discipline held:** all logic is methods on `WorkflowEngine`/`WorkflowCombination`/
  `StepDecision` or trait impls (`TryFrom<&Completion> for StepDecision`,
  `DecisionAuthorization`); typed per-crate `Error` variants; no free functions.

### Green, cross-crate, real

`tests/workflow_engine_thin_slice.rs` — 3 tests, all pass (full suite + `clippy
--features nota-text --all-targets -D warnings` clean):

- **(a)** one-step `WorkflowDefinition` (Unanimous) → fixture agent → `Authorized`
  → `WorkflowReceipt`.
- **(b)** that receipt in `Evidence.workflow_receipts` → criome's **landed**
  evaluator (`store.evaluate`, criome `cd9791db`) → `Ok(Authorized)`. Real
  signal-criome `7b3d5b2f` / criome nouns — `WorkflowReceipt` is the shared type,
  so the orchestrate-produced receipt is literally what criome consumes.
- **(d)** empty `workflow_receipts` → `Ok(Escalate(EscalationTarget::Workflow(digest)))`.

So produce → adopt and escalate-when-absent are proven across orchestrate + agent
+ criome, offline and non-blocking.

## The parallel-lane finding

Both lanes built this slice — the parallel-lane model in action:

- **Operator's main `bfe4f6d`** ("orchestrate: produce fixture workflow receipts")
  is a **synchronous stub**: it fabricates `Authorized` *without ever calling the
  agent*, and does not prove the criome seam.
- **This branch** built *on* `bfe4f6d` and replaced the stub with a **real
  agent-effect engine** (actually dispatches to agent, parses the completion) plus
  the **end-to-end criome integration proof** operator flagged as the next slice.

So the demonstrator supersedes the stub with the real dispatch and proves the seam
operator hadn't yet. Operator owns main and integration: the recommendation is to
**integrate this branch's real engine + criome proof into main**, replacing the
stub, then carry the production depth (durable SEMA run record, multi-step DAG,
escalation) per `726`'s build order.

## Design finding — signal-orchestrate mirror duplication

signal-orchestrate carries **duplicate mirror types** (its own `StepOutcome` /
`EvaluationDecision`, distinct from the signal-criome nouns). Routing typed step
outcomes through the generated nexus structs is therefore lossy/tedious. The build
worked around it by carrying the **raw agent `Completion`** on the effect plane and
parsing to the contract `StepOutcome` in-engine — keeping **one type world**
(signal-criome's `EvaluationDecision`) from step outcome to receipt to criome.

The cleaner long-term fix (recommend): the orchestrate nexus effect schema
references signal-criome nouns directly, **or** signal-orchestrate drops the mirror
duplication and cross-imports signal-criome — exactly the "source of truth remains
signal-criome" principle from `725`. The mirror duplication is the same anti-pattern
the `722` audit flagged elsewhere (hand-maintained parallel vocabularies); fixing it
keeps the guard-decision type singular across the whole chain.

## Toolchain note (resolved)

A fresh resolve bumped schema-rust-next to `90d853c3`, against which signal-agent
main fails its artifact-freshness check (`RetiredStructFieldSyntax "Model."`).
Resolved by seeding `Cargo.lock` from current main (schema-rust-next `e4ac3baf` —
the pin agent + orchestrate both build against) and adding only the new crates.
This is a live pin-skew between signal-agent and the latest schema-rust-next that
operator/system should reconcile when next touching signal-agent.

## Next

1. Operator integrates the real engine + criome proof to main (replacing the stub).
2. signal-orchestrate mirror-duplication cleanup (one type world).
3. Production depth per `726`: durable SEMA run record (self-resume), multi-step
   DAG (parallel/series), escalation (workflow / smarter-agent / psyche-via-mentci).
4. Then criome receipt-consumption in spirit's real path, and the multi-node
   co-signature plane.
