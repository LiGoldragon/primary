# 724 — Design: the general guard substrate (criome guard-contract + orchestrate workflow-execution)

Concrete contract shapes for the general substrate the psyche chose to build
first (Spirit `m3ms`, extending `pviw`). Grounded in the *current* deployed
contracts, so this is extension where possible. Designer-level shape; operator
carries production depth.

The headline: **most of criome's guard-contract algebra already exists.** The net-
new is a single cognitive-guard rule + an extended verdict vocabulary in criome,
and orchestrate's workflow-execution surface (genuinely greenfield).

## 1 — What already exists (criome)

`signal-criome` already carries the typed policy language `pviw` describes:

```nota
Contract { Rule }
Rule [
  (SignedBy Identity)            ;; a named signer
  (All (Vector ContractDigest))  ;; conjunction
  (Any (Vector ContractDigest))  ;; disjunction
  (Threshold Threshold)          ;; k-of-n quorum
  (ActiveAfter TimedRule)        ;; time-lock open
  (ActiveUntil TimedRule)        ;; time-lock close
  (TimeSwitch TimeSwitch)        ;; time-varying threshold
  (Agreement AgreementRule)      ;; divergence-reconciliation
  EscalateToPsyche
]
EvaluationDecision [ Authorized (Rejected EvaluationRejectionReason) EscalateToPsyche ]
```

plus `AdmitContract`, `LookupContract`, `EvaluateAuthorization(AuthorizationEvaluation)`,
`Evidence { component operation stamp EvidenceSignatures Agreements }`, and the
`AuthorizedObjectUpdate` fan-out. The deterministic guards (signatures, quorums,
time-locks) and the verify-only verdict path are **done**. What's missing is the
cognitive guard — a rule that binds to an LLM workflow — and the richer outcome
set (`pviw`: approve/reject/defer/non-judge/escalate).

## 2 — Net-new in criome: the cognitive guard

A `Workflow` rule variant and a generalized escalation/verdict vocabulary. criome
stays **verify-only**: the workflow runs in orchestrate and returns a *signed*
content-addressed verdict that criome verifies exactly like a signature.

```nota
;; NEW Rule variant — a cognitive guard clause
Rule [ ... existing ...
  (Workflow WorkflowGuard)
]

WorkflowGuard {
  workflow.WorkflowDigest    ;; content-addressed workflow definition (authored in mind)
  executor.Identity          ;; the orchestrate identity whose signed verdict criome accepts
}

;; GENERALIZED decision — pviw's full closed outcome set
EvaluationDecision [
  Authorized
  (Rejected EvaluationRejectionReason)
  Deferred                   ;; NEW — defer is first-class (pviw)
  NonJudgement               ;; NEW — abstain/non-judge is first-class (pviw, LLM default)
  (Escalate EscalationTarget) ;; GENERALIZES EscalateToPsyche
]

EscalationTarget [
  Psyche
  (Workflow WorkflowDigest)        ;; escalate to a more complex workflow
  (SmarterAgent Identity)
  (All (Vector EscalationTarget))  ;; combination — every target must verdict (psyche AND workflow)
  (Any (Vector EscalationTarget))  ;; first verdict wins
]
```

The signed verdict orchestrate returns, carried inside the existing `Evidence`
and verified by criome (no new content — only references, per `pviw` "verdicts
never carry new content"):

```nota
WorkflowVerdict {
  workflow.WorkflowDigest
  operation.OperationDigest
  outcome.EvaluationDecision           ;; the workflow's own closed outcome
  provenance.WorkflowProvenanceDigest  ;; -> orchestrate's run log (the LLM logs)
  stamp.AttestedMoment
  signature.StampedSignatureEnvelope   ;; signed by the executor Identity
}
```

criome's evaluation of a `Workflow` clause: if a matching signed `WorkflowVerdict`
is present in `Evidence`, verify the executor signature + freshness and adopt its
outcome; if absent, return `(Escalate (Workflow <digest>))` so the caller drives
the run. That keeps criome a pure verifier and makes "run the guard workflow" an
explicit escalation step, not hidden execution inside the auth component.

## 3 — Net-new in orchestrate: workflow execution

orchestrate has no execution surface today. It gains one — the DAG runner the
psyche reached for ("*sends that to orchestrate as a unique workflow… executed
with agents, either in parallel or in series or the combination*").

```nota
;; NEW ordinary roots on signal-orchestrate
(RunWorkflow WorkflowRunRequest)
(ObserveWorkflowRun WorkflowRunObservation opens WorkflowRunStream)
;; NEW replies
(WorkflowRunAccepted WorkflowRunHandle)
(WorkflowVerdictProduced WorkflowVerdict)   ;; cross-imported from signal-criome
(WorkflowRunLogReported WorkflowRunLog)

WorkflowRunRequest {
  workflow.WorkflowDigest               ;; the DAG, resolved from mind
  operation.AuthorizedObjectReference   ;; what is being judged (content-addressed, no payload)
  contract.ContractDigest               ;; the criome guard contract this run satisfies
}

WorkflowRunHandle { RunDigest }

;; the LLM logs the psyche wants ("orchestrate has llm logs")
WorkflowRunLog {
  RunDigest
  StepLogs.(Vector StepLog)
}
StepLog {
  step.StepName
  attestation.ModelAttestation
  outcome.StepOutcome
}
ModelAttestation {
  provider.ProviderName
  model.ModelName
  host.HostName              ;; WHERE it ran
  call.OperationDigest       ;; content-addressed prompt+response
}
```

The workflow *definition* (the DAG) lives in **mind** (it owns "the work graph"):

```nota
WorkflowDefinition {
  Steps.(Vector WorkflowStep)
  combination.CombinationRule     ;; how step outcomes compose into the verdict
  escalation.(Optional EscalationTarget)
}
WorkflowStep {
  name.StepName
  prompt.PromptTemplateDigest     ;; the agent Call spec
  provider.(Optional ProviderName)
  Dependencies.(Vector StepName)  ;; DAG edges: independent = parallel, dependent = series
}
CombinationRule [ (Threshold StepThreshold) Unanimous AnyApprove ]
```

orchestrate's engine: resolve the DAG from mind, topologically dispatch each step
as an `agent::Call` (independent steps in parallel, dependents in series), apply
`CombinationRule` to step outcomes, on `Deferred`/`NonJudgement`/threshold-miss
follow `escalation` (recurse into a bigger workflow, a smarter agent, or the
psyche via mentci), then sign the `WorkflowVerdict` and persist the
`WorkflowRunLog`. agent is unchanged — it already executes one `Call`.

## 4 — The other components (assembly, little net-new)

- **agent** — unchanged; each step is one `Call(Prompt)`. (Streaming later.)
- **mind** — stores `WorkflowDefinition`s in its work graph; resolves a `WorkflowDigest`.
- **introspect** — the workflow run emits trace events on the existing trace plane (reports 716/722); the execution trace is observable end-to-end.
- **mentci** — a status-board pane subscribing to criome `AuthorizedObjectUpdate` + orchestrate `WorkflowRunStream` + introspect traces; the psyche-facing live view (`7x5z`).

## 5 — End-to-end flow

```mermaid
sequenceDiagram
  participant Op as guarded op (e.g. spirit intent-admit)
  participant Cr as criome (verify-only)
  participant Or as orchestrate (executor)
  participant Mi as mind (graph)
  participant Ag as agent (step)
  participant In as introspect (trace)
  participant Me as mentci (board)

  Op->>Cr: EvaluateAuthorization(contract, object, evidence)
  Cr->>Cr: walk Rule; deterministic clauses verified inline
  Cr-->>Op: Escalate(Workflow w)   %% workflow clause, no verdict yet
  Op->>Or: RunWorkflow(w, object, contract)
  Or->>Mi: resolve WorkflowDefinition(w)
  Or->>Ag: Call(step) ... parallel / series per DAG
  Ag-->>Or: completion (per step)
  Or->>In: trace events (which model, where)
  Or->>Or: combine outcomes; escalate if needed (bigger wf / psyche via Me)
  Or-->>Op: WorkflowVerdict (signed, + provenance -> run log)
  Op->>Cr: EvaluateAuthorization(contract, object, evidence + WorkflowVerdict)
  Cr->>Cr: verify executor signature + freshness; adopt outcome
  Cr-->>Op: Authorized | Rejected | Deferred
  Cr->>Me: AuthorizedObjectUpdate (status board)
```

## 6 — The spirit guardian as the first guard contract

Once the substrate exists, spirit's intent guardian is *one instance*: the
"admit intent record" operation is guarded by a criome contract
`(Workflow guardianWorkflowRef)`, whose `WorkflowDefinition` (in mind) is the
guardian's judgment — the justification-read dimensions, closed rejection set,
and atomic accept/reject from `kasm`/`7xnx`/`i59i` become that workflow's steps
and `CombinationRule`. spirit stops running its own guardian; orchestrate runs the
guardian workflow; criome verifies the signed verdict. Per the psyche's chosen
staging, this migration happens **after** the general substrate is built.

## 7 — Build plan + next step

| Component | Work | Size |
|---|---|---|
| signal-criome | add `Workflow` rule, `WorkflowGuard`, extend `EvaluationDecision` + `EscalationTarget`, `WorkflowVerdict` | small (extend) |
| signal-orchestrate | new `RunWorkflow`/`ObserveWorkflowRun` surface, run-log types | medium (greenfield contract) |
| orchestrate | the DAG-execution engine (dispatch agent, combine, escalate, sign) | large (greenfield engine) |
| signal-mind / mind | `WorkflowDefinition` storage + resolve | medium |
| agent | none | — |
| introspect | workflow trace events (reuse plane) | small |
| mentci | status-board pane | small |

**Proposed next step (designer):** stand up the two contract families first —
the criome `Workflow`-rule extension and the orchestrate workflow-execution
contract — on a feature branch (`~/wt/.../signal-criome` and
`~/wt/.../signal-orchestrate`), as the demonstrable shape, with round-trip tests.
The orchestrate engine (the large piece) follows once the contracts are agreed.
This is the "build the general substrate first" path.

## 8 — Update after psyche input: two planes of trust, composition, operator items

The psyche added the trust model and answered the open items. Operator captured
the trust model as Spirit `ic4o`; this section folds it into the design.

### 8.1 — The signing model, corrected (`ic4o`)

> Per Spirit `ic4o` (Decision High): [criome guard workflow trust has two planes:
> a local execution chamber treats co-resident trusted components (criome
> orchestrate agent introspect mentci) as one collaborating local system for
> first-substrate workflow receipts; the independent authority layer is the criome
> quorum layer, where peer nodes run their own LLM workflows and produce their own
> signatures over the content-addressed object or verdict, with the system
> observing expected peer co-signatures and surfacing missing ones.]

So §2/§5's "orchestrate signs, criome verifies" is the **multi-node** behavior,
not the local one. Corrected:

- **Local plane (now):** orchestrate returns a content-addressed workflow
  **receipt**; criome adopts it *by trust* (co-resident component) with **no
  inter-component signature verification** — the psyche: *"Right now we're just
  trusting all the components. We're running in a trusted state… the Creom is
  essentially the same program."* criome signs the resulting authorized object
  with its own BLS key, as today. The operation reaches criome as a
  content-addressed **reference + digest, never full content** (psyche: *"content
  addressed"*).
- **Multi-node plane (build toward now):** a second criome (on Prometheus)
  independently runs its own workflow and signs the same content-addressed object
  → **double-signatures**; a watcher surfaces objects missing an expected
  co-signature. This is `pviw`'s cross-party quorum and `7let`'s "1-of-1 local
  toward multi-machine quorum," promoted to an always-on resilience mechanism.

So the local artifact is a *receipt*, not a cross-verified verdict:

```nota
WorkflowReceipt {            ;; local plane — trusted, content-addressed, not cross-verified
  workflow.WorkflowDigest
  operation.OperationDigest
  outcome.EvaluationDecision
  provenance.WorkflowProvenanceDigest  ;; -> orchestrate run log
}

;; multi-node plane — the co-signature + the watcher's model
ObjectCoSignature {
  object.AuthorizedObjectReference
  signer.Identity                      ;; the peer criome
  signature.StampedSignatureEnvelope
}
CoSignatureExpectation {
  object.AuthorizedObjectReference
  ExpectedSigners.(Vector Identity)
  ObservedSigners.(Vector Identity)    ;; watcher surfaces Expected minus Observed
}
```

### 8.2 — Composition is generic from day one

Per operator's recommendation and the psyche's "programmable combinations
including psyche AND LLM," composition is a generic tree, not a fixed
`AllOf(LLM, Psyche)`. criome's existing `Rule` `All`/`Any` plus a single
verdict-composition enum cover it:

```nota
Composition [
  (AllOf (Vector Composition))
  (AnyOf (Vector Composition))
  (Threshold CompositionThreshold)
  (Escalate EscalationTarget)
  (WorkflowStep StepName)
  (Signature Identity)
]
;; "psyche AND LLM" = (AllOf [(WorkflowStep guardian) (Escalate Psyche)])
```

### 8.3 — Multi-node double-signature flow

```mermaid
flowchart LR
  obj["content-addressed object / verdict"]
  subgraph nodeA["node A (local)"]
    wA["criome-A: run workflow (orchestrate)"] --> sA["criome-A signs"]
  end
  subgraph nodeB["node B (Prometheus)"]
    wB["criome-B: run its OWN workflow"] --> sB["criome-B signs"]
  end
  obj --> wA
  obj --> wB
  sA --> dbl["object carries double signature"]
  sB --> dbl
  dbl --> watch["watcher: ExpectedSigners minus ObservedSigners"]
  watch -->|"missing co-signature"| alert["surfaced via introspect / mentci"]
```

### 8.4 — Operator's five open items — designer position

| # | Item | Resolution |
|---|---|---|
| 1 | Full content vs digest at criome | **Content-addressed reference + digest only** (psyche: "content addressed"); criome never holds full content. Full content/provenance lives in orchestrate/introspect. |
| 2 | What signs the verdict first | **Local plane: no inter-component signing** (trusted chamber); criome signs the authorized object with its own key. **Multi-node: independent criomes double-sign**; per-step agent/model BLS provenance is a later refinement. (`ic4o`) |
| 3 | Blocking semantics | **Non-blocking first.** Build the substrate with real grants/verdicts, trace the return, then flip spirit to blocking Gating in a later explicit step (psyche: "sounds correct"). |
| 4 | Composition shape | **Generic `Composition` enum now** (AllOf/AnyOf/Threshold/Escalate) — agree with operator; §8.2. |
| 5 | Production tag scope | **Tag the whole deployed surface** CriomOS-home uses for spirit (spirit, signal-spirit, meta-signal-spirit, criome, signal-criome, mentci, introspect, triad-runtime pins) — agree with operator. Operator's lane to apply + capture; designer defers. |

### 8.5 — Build order (revised)

The multi-node double-sign + watcher is now part of "build the general substrate"
(psyche: *"start running a second criome on Prometheus… double signatures… watch
for when that doesn't happen"*). So: **(a)** criome `Workflow`-rule + receipt +
composition and **(b)** orchestrate workflow-execution are the local-plane
contracts (designer feature branches first); **(c)** the second criome +
double-sign + watcher is the multi-node plane — system-operator/cluster-operator
deploys a second criome on Prometheus, coordinated with the contract work. I
proceed to (a)+(b) on feature branches; (c) coordinates with the system lane.
