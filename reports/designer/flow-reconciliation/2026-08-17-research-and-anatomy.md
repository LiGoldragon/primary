# Surveying all flows: research and aspect anatomy

Status: preliminary Design synthesis for psyche review; not an accepted architecture or an implemented role skill.

Research date: 2026-08-17.

## Finding

The desired capability is not maintenance, and surveying is only its first movement. It is a closed loop that keeps Athena's account of intended work reconciled with evidence of what its flows have actually done, keeps every discrepancy visible until it is resolved or explicitly accepted, and returns unresolved work to the right locus of attention.

This survey found no single settled name for that whole. Its parts are established as meta-level architecture, metareasoning, execution monitoring, process conformance checking, provenance, durable execution, workflow orchestration, observability, and operational assurance. Current skill ecosystems implement strong bounded pieces, but the repositories reviewed did not contain a mature skill that discovers and reconciles the whole ecology of flows, sessions, goals, branches, trackers, handoffs, external commitments, and completion evidence.

The strongest aspect-name hypothesis is **Reconciliation**. It names the essential operation without implying a person or authority. **Assurance** is the strongest alternative if the psyche wants the name to emphasize the desired confidence rather than the operation that creates it. The name should not land until the aspect's authority is ruled.

## Psyche already expressed

At Spirit level, the relevant governing expressions are:

> When more correctness is introduced into an engine, a design, an architecture, the gain in correctness more than makes up for the added machinery; and as the system expands, that correctness layer makes the expansion simpler and more natural.

> Keep observations, hypotheses, and unknowns separate. Keep unknown causes unknown.

> Seek disconfirming evidence. Do not seed audits with suspected conclusions.

> Weigh evidence by origin, not repetition.

No relevant Intent entry was located in the current tree.

The closest prior Vision is:

> I think the biggest lesson from this is that we need to routinely look at the very high-level view of what we're building, because then it would have been obvious to me right away. … you would want him to have, like, a very clear view of the whole engine from a high level. That's really what I mean.

The current Vision is preserved verbatim in `psyche/Vision/surveyingAllFlows.md`.

Agent synthesis from other governing Vision entries:

- `psyche/Vision/flowsNotAgents.md`: flows are flows rather than little people, and aspect names are single-word concepts rather than person-implying roles;
- `psyche/Vision/managementDelegation.md`: managers retain the high-level view and do not investigate implementation detail;
- `psyche/Vision/attunement.md`: shards do not inherit authority merely from their identity;
- `psyche/Vision/awarenessIsGeneralUnderstanding.md`: awareness is general understanding rather than a carry-all task-state narration;
- `psyche/Vision/sessionLogging.md` and `psyche/Vision/psycheLogStructure.md`: session records and ancestry can supply traceable evidence for later verification;
- `psyche/Vision/testTravesties.md`: a claimed test without an adequate witness is not evidence.

Provisional naming implication: `Overseer` appears to fit poorly even if oversight remains part of the description, because it implies an individual and unruled executive authority. This is Design analysis, not a psyche ruling.

## What current skill ecosystems contain

The repository survey covered official and widely used ecosystems plus smaller repositories with unusually close concepts.

| Pattern | Representative artifact | What it contributes | What it does not do |
|---|---|---|---|
| Completion proof | [Superpowers: verification-before-completion](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) | Fresh evidence before completion claims; delegated work is independently checked | Does not discover all project work |
| Continuous lifecycle monitoring | [Codex: babysit-pr](https://github.com/openai/codex/tree/main/.codex/skills/babysit-pr) | Watches CI, review, mergeability, retries, and terminal conditions until a PR is genuinely ready | One PR only |
| Authoritative workflow state | [OpenAI Symphony specification repository](https://github.com/openai/symphony/tree/main) | Issue-driven dispatch, retries, reconciliation, active/terminal states, and cleanup; worker exit is not equivalent to done | Sees configured tracker work only |
| Audit completeness | [GitHub awesome-copilot: quality-playbook](https://github.com/github/awesome-copilot/tree/main/skills/quality-playbook) | Coverage matrix, progress log, completeness report, reconciliation, explicit partial/fail verdicts | One code-quality audit only |
| Work-front discovery | [Matt Pocock: wayfinder](https://github.com/mattpocock/skills/tree/main/skills/engineering/wayfinder) | Ownership, dependency graph, frontier of unblocked/unclaimed work, fog-of-war categories | One mapped initiative only |
| Queue continuity | [Matt Pocock: triage](https://github.com/mattpocock/skills/tree/main/skills/engineering/triage) and [handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) | Durable state, oldest-first queues, resumability, compact transfer | Tracker/session scope only |
| Per-task self-monitoring | [Microsoft AutoGen: Magentic-One](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/magentic-one.html) | Task Ledger, Progress Ledger, loop detection, satisfaction check, replanning | One orchestrated task only |
| Conformance and coverage | [Trail of Bits skills](https://github.com/trailofbits/skills) | Spec-to-code compliance, coverage analysis, risk and blast-radius review | Code/security surfaces only |
| Durable runtime | [LangGraph](https://github.com/langchain-ai/langgraph) and [CrewAI Flows](https://docs.crewai.com/) | Checkpoints, persisted state, routing, resumability, supervision primitives | Cannot discover work never modeled in the runtime |

Smaller but conceptually close artifacts contribute `Coverage Ledger`, explicit `not covered`, one owner per decision, dependency evidence, residual-risk declaration, and closure only after required nodes are evidenced. These confirm the vocabulary, but do not demonstrate a project-wide meta-flow.

### The gap

Across the surveyed repositories, no mature artifact demonstrated all of these together:

1. enumerate every declared source of work and every observable flow;
2. discover undocumented, abandoned, duplicated, or orphaned work;
3. connect each commitment to ownership, dependencies, acceptance criteria, and evidence;
4. reconcile session, tracker, branch, worktree, CI, message, and artifact state;
5. distinguish claimed completion from verified completion;
6. keep discrepancies durable across sessions;
7. route each unresolved discrepancy without becoming its implementer.

That combination is the proposed aspect's differentiator.

## The wider field

The idea has a deep lineage even though the combined capability does not have one standard name.

| Field | Established idea | Relevance |
|---|---|---|
| AI architecture | [Genesereth's meta-level architecture](https://cdn.aaai.org/AAAI/1983/AAAI83-001.pdf) | A meta-level process reasons about base-level processes and control choices |
| Rational control of reasoning | [Russell and Wefald's metareasoning](https://iiif.library.cmu.edu/file/Newell_box00014_fld01011_doc0001/Newell_box00014_fld01011_doc0001.pdf) | Monitoring and reasoning themselves consume resources and need bounded value-of-computation decisions |
| Plan-based AI | [Plan execution monitoring](https://publications.ri.cmu.edu/plan-execution-monitoring-through-detection-of-unmet-expectations-about-action-outcomes) | Compare expected outcomes with observed outcomes; correct or replan when expectations fail |
| Process mining | [Conformance checking](https://wires.onlinelibrary.wiley.com/doi/10.1002/widm.1045) | Align event logs with an expected process to expose omissions, reorderings, and deviations |
| Distributed coordination | [Commitments and conventions](https://eprints.soton.ac.uk/id/eprint/252090) and [Contract Net](https://reidgsmith.com/The_Contract_Net_Protocol_Dec-1980.pdf) | Make promises, ownership, conditions, and monitoring explicit |
| Traceability | [W3C PROV](https://www.w3.org/TR/prov-primer/) | Record what was generated, used, performed, and attributed so important claims can be checked |
| Reliable workflow systems | [Temporal durable execution](https://docs.temporal.io/) | Persist state, retries, timers, dependencies, signals, and recovery across failures |
| Current agent design | [Anthropic's orchestrator-workers and evaluator-optimizer patterns](https://www.anthropic.com/engineering/building-effective-agents) | Useful components, while warning that agentic complexity adds latency, cost, and failure modes |
| Operational AI assurance | [NIST AI RMF](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) and [NIST AI 800-4](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-4.pdf) | Ongoing monitoring, assigned responsibility, incident response, override, change management, recovery, and deactivation |
| Agent observability | [OpenTelemetry GenAI conventions](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) | Emerging shared fields for workflow, agent, tool, conversation, and evaluation traces |
| Systems safety | [STPA](https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf) | Control requires explicit boundaries, hazards, constraints, feedback, and responsibility |

`AgentOps`, `LLMOps`, and `control tower` are current umbrella terms, but they do not specify this architecture precisely. NIST's 2026 survey describes deployed-AI monitoring terminology and practice as still nascent.

## Proposed essence

Provisional agent-authored formulation for psyche review:

> The aspect reconciles Athena's intended work with the best available evidence of its actual state. It preserves attention on every discrepancy until the discrepancy is verified as resolved, explicitly accepted, or returned to the psyche as an unknown that requires judgment.

This formulation leads with the desired state: continuity between intent, work, and reality. It does not define the aspect as a police function and does not blame a flow for a discrepancy.

## High-level anatomy

```text
intent, goals, sessions, dispatches, trackers, VCS, CI, messages, effects
                                  │
                                  ▼
                 append-only event and provenance ledger
                                  │
                  deterministic state/coverage checks
                                  │
                                  ▼
                 periodic and event-triggered meta-flow
             compare → classify → seek evidence → reconcile
                                  │
                                  ▼
      verified state + discrepancies + unknowns + proposed routing
                                  │
                                  ▼
            manager / local flow / verifier / harness / psyche
                                  │
                         new evidence or ruling
                                  └──────────────► ledger
```

### Substrate

The meta-flow should read a canonical, deterministic substrate rather than ingest every transcript and tool call into one enormous context.

1. **Flow registry** — identity, dynamic name, parent and siblings, aspect, scope, capabilities, authority, privacy and risk class.
2. **Commitment graph** — goal, owner, dependencies, acceptance criteria, expected artifacts, deadline or heartbeat, escalation policy.
3. **Event and provenance ledger** — append-only lifecycle events and references to durable effects.
4. **Source adapters** — session logs, beads/goals, version-control state, GitHub and CI, manifests, deployments, messages, external systems. Trackers and beads contribute observations and issue state; they do not become authority or handover merely by being read here.
5. **Discrepancy ledger** — each finding, evidence, freshness, confidence, owner, disposition, and verification state.

### Evidence levels

Every important completion assertion should distinguish:

- **claim** — what a flow says occurred;
- **trace** — what the harness observed occurring;
- **effect** — what durable external state demonstrates occurred.

A successful tool return is not necessarily an effect. A missing trace is not proof that no work occurred. Self-report is evidence, but it is not self-certifying.

### Flow states

`discovered → planned → assigned → running → waiting/blocked → needs-review → completed-claimed → completed-verified`

Exceptional or terminal dispositions include `failed`, `cancelled`, `abandoned`, `superseded`, and `unknown/stale`.

The critical separation is between `completed-claimed` and `completed-verified`. A goal is not closed merely because a worker stopped, a tool returned success, a handoff exists, or a PR turned green.

### Reconciliation cycle

1. **Census** — enumerate declared work sources and observable flows.
2. **Orient** — reconstruct the high-level work and dependency graph without entering implementation detail.
3. **Compare** — align intended state, reported state, traces, and durable effects.
4. **Classify** — verified, incomplete, blocked, stale, orphaned, duplicated, drifted, contradictory, or unknown.
5. **Seek proportionate evidence** — deterministic checks first; semantic review only where meaning must be interpreted.
6. **Route** — return a discrepancy to the flow that owns it, a dedicated verifier, the manager, the harness, or the psyche.
7. **Verify disposition** — retain the finding until evidence or an authoritative acceptance resolves it.
8. **Record limits** — state uncovered sources, stale evidence, confidence, and sampling choices.

### Triggers

- event-driven at assignment, blocking, handoff, completion claim, cancellation, and authority-changing events;
- periodic whole-system sweeps to detect orphaned and stale work;
- lifecycle gates before commits, pushes, PR readiness, deployment, goal closure, session retirement, and repository retirement;
- on demand when the psyche or another flow asks for the high-level view.

### Outputs

The primary output is not a dashboard. It is an actionable, evidence-backed account containing:

- what work and flows are in scope;
- verified completion versus claimed completion;
- the open frontier and its ownership;
- stale, orphaned, duplicated, or lost work;
- missing handoffs, evidence, dependencies, or decisions;
- discrepancies between intent, claim, trace, and effect;
- unknowns and explicit coverage limits;
- proposed routing and the authority needed for each action;
- changes since the last survey.

## Boundaries

The aspect should not silently absorb the work of neighboring functions.

- **Management** prioritizes and delegates. Reconciliation tells management where the account and evidence do not close.
- **Local flows** understand implementation detail and perform the work.
- **Verification/testing/review flows** examine particular artifacts deeply.
- **The meta-harness** owns durable state transitions, messaging, scheduling, retries, and allowed actuation.
- **The psyche** rules intent, ambiguity that changes meaning, and acceptance where evidence cannot determine value.
- **Reconciliation** maintains the high-level work account, detects discrepancies, requests proportionate evidence from local or verifier flows, routes findings, and verifies their disposition. It remains at the high level and does not investigate implementation detail itself.

It is not a private psyche, a chronological scratchpad, a universal implementer, or an omniscient judge. In the current authority model it should be advisory: it may create findings and requests, but it may not restart, reassign, stop, close, or mutate another flow until the psyche grants those actions explicitly through the harness.

## Why a single global overseer is the wrong architecture

A central LLM receiving every detail would become the largest context bottleneck and the largest correlated failure domain. It would see stale snapshots, expose excessive private data, overload attention, and tempt the system into micromanagement.

The disconfirming literature is strong:

- [Ashby's Law of Requisite Variety](https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf) implies that a regulator cannot control disturbances it cannot represent; uninstrumented flows remain invisible.
- [Google SRE](https://sre.google/sre-book/monitoring-distributed-systems/) warns that alerts must be actionable and humans cannot stare at dashboards indefinitely.
- [NIST AI 800-4](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-4.pdf) identifies incomplete visibility, rapid change, privacy, scaling review, Goodhart's Law, and the streetlight effect.
- LLM judges exhibit position and other systematic biases; the producer and certifier should not rely on the same model, prompt, and evidence channel ([MT-Bench judge study](https://arxiv.org/abs/2306.05685)).
- Monitoring sensitive prompts, outputs, tool arguments, and results creates privacy and security duties, not merely storage concerns ([OpenTelemetry guidance](https://opentelemetry.io/blog/2025/ai-agent-observability/)).

The provisional Design recommendation is therefore hierarchical and event-sourced: local evidence remains near bounded work; deterministic state and provenance are shared; parent levels consume compact summaries and explicit escalations; semantic surveys are periodic and budgeted.

## Proposed invariants

1. Every finding distinguishes observation, hypothesis, and unknown.
2. Every material claim carries source, authority, freshness, and confidence.
3. Completion claims never become verified completion without proportionate external evidence.
4. Missing evidence becomes `unknown`, never silently `done` or `not done`.
5. Every registered commitment has one visible owner or is explicitly orphaned.
6. Every discrepancy remains durable until verified, accepted by the proper authority, superseded, or cancelled with provenance.
7. Coverage limits and uninstrumented sources appear in every survey.
8. Deterministic checks own deterministic facts; an LLM interprets semantics rather than replacing state machinery.
9. The aspect cannot grant itself authority.
10. Monitoring has explicit cost, context, privacy, retention, and recursion budgets.

## Naming

| Candidate | Strength | Problem |
|---|---|---|
| **Reconciliation** | Names the actual compare-and-close operation; established across data, processes, and durable systems; single concept; no person implied | Does not immediately evoke vigilance or whole-system scope; already generic vocabulary in the workspace |
| **Assurance** | Names the desired evidence-backed confidence; established in AI governance and TEVV | Can sound like a guarantee and overlap quality assurance |
| **Oversight** | Directly conveys high-level view and is the concept form of `Overseer` | Implies governance and authority; can sound bureaucratic |
| **Stewardship** | Conveys care, continuity, and not losing work | Implies custody/governance; less precise about evidence; risks collision with existing Steward vocabulary |
| **Attunement** | Existing nearby psyche vocabulary for keeping parts in balance | Earlier material was tentative; does not clearly mean completion verification |
| **Vigilance** | Strong watchfulness and anomaly detection | Suggests endless monitoring; weak on reconciliation and closure |
| **Integrity** | Evokes wholeness and consistency between parts | Very broad; overloaded with security and moral meanings |
| **Closure** | Strong on work not falling through cracks | Too terminal; misses ongoing state, drift, and coherence |

Current recommendation: use **Reconciliation** as the Design working name, not a landed psyche ruling. Its role phrase can be “whole-flow reconciliation” or “flow reconciliation” when disambiguation is needed. If the psyche grants executive authority rather than advisory routing, reconsider **Oversight** or **Stewardship**.

## Rulings needed next

These are anatomy questions, not implementation questions.

1. **Intent** — Is the intent that no committed work become invisible, or that Athena continuously preserve coherence between psyche intent, flow claims, and real effects? The latter is broader and more foundational.
2. **Authority** — May the aspect only report and request, or may it reopen, retry, reassign, stop, cancel, or close work?
3. **Universe** — Does “all flows” mean one workspace, every Athena workspace, all current sessions, all recorded historical commitments, or every connected external system?
4. **Evidence** — Which effects are required for different classes of completion, and when is independent or human verification mandatory?
5. **Observability** — Which lifecycle events must every flow emit, what data may cross flow boundaries, and how long is it retained?
6. **Cadence** — Which transitions trigger immediate reconciliation, and how often should the global sweep run under a bounded budget?
7. **Disposition** — When work is deliberately abandoned or superseded, who can accept that residue and make it terminal?
8. **Identity** — Is this a distinct aspect/role skill, a Design sub-flow, or a meta-harness service presented through a role skill?

No implementation or role-skill wording should be produced until these boundaries are ruled.
