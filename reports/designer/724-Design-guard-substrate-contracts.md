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
This is the "build the general substrate first" path; I'll proceed to the contract
branches unless you want to refine the shapes above first.
