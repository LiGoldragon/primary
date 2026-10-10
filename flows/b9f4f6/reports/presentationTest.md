# Three Frameworks for Dividing the Flow Model by Thinking Task

---

You asked for three different coherent frameworks to divide the flow model depending on the thinking task needed, and how they relate to each other in flow-flows. Below are three, drawn from the current research. Each answers a different question about what flows a task needs. At the end: how they compose.

Each claim carries its origin. Where the flow's own reading connects a research finding to your vocabulary, that connection is marked as inference.

---

## Framework 1: By Reasoning Kind — Abduction / Deduction / Induction

This framework asks: **what kind of inference does the task demand?**

You adopted abduce/deduce/induce as the terminology for program-flow types. The research confirms these are not just labels — they are empirically dissociable. The 2025 abductive reasoning survey (arXiv 2604.08016) tested LLMs across all three and found: "Strong deductive or inductive capabilities do not reliably predict strong abductive reasoning performance." They come apart. A flow good at one is not necessarily good at another.

The ReasonOps paper (arXiv 2605.29192, May 2026) provides the sharpest evidence for why this matters to flow design. It identified seven reasoning operators that cluster into two families — **committal** (initiating, inferring, constraining, grounding) and **reflective** (qualifying, backtracking, hypothesizing). The critical finding: reflective operators help on hard problems and harm on easy ones. On easy problems, correct traces show +44.2% more committal operator usage than incorrect ones. On hard problems, that gap vanishes, but the hypothesizing-to-inferring ratio remains predictive.

[Inference: committal operators align with deduction (drawing conclusions from what is given, constraining the space). Reflective operators align with abduction (hypothesizing explanations, qualifying, backtracking when a hypothesis fails). Induction — generalizing from instances — is not cleanly represented in ReasonOps' taxonomy, which studied math/science tasks where induction is less prominent.]

**What this means for the flow model:** Each reasoning kind needs a different top stratum. An abductive flow needs permission to hypothesize freely, to qualify, to backtrack — the reflective operators. A deductive flow needs to stay committal: ground in facts, infer, constrain. Mixing them in one flow is what the research shows hurting easy problems (unnecessary reflection) and what you identified when you said that "trying to make the flow responsible for implementing and trying to figure out whether or not it should implement is actually going to be really costly in terms of introducing noise into the job."

**What this framework does not decide:** It does not say how many flows a task needs, or how they connect. It says what kind of thinking each flow does.

---

## Framework 2: By Cognitive Level — Object / Meta / Configurator

This framework asks: **at what level of self-awareness does the task operate?**

Stanovich (2011) argued that the popular "System 1 / System 2" split is wrong even for humans — you need three levels, not two. His tripartite mind:

- **Autonomous** — fast, automatic processing (the LLM's direct output)
- **Algorithmic** — how well you can reason when you do reason (the chain of thought, the working-out)
- **Reflective** — whether you notice you should reason, and what standards you apply (the meta-level that decides to engage)

The distinction between the algorithmic and reflective is the key insight: *how well you reason* is separate from *whether you notice you should reason and what you hold yourself to*. The reflective mind is not a better reasoner — it is a different function entirely.

The 2025 TRIAGE paper (arXiv 2605.13414) provides the strongest empirical confirmation. It tested whether extended reasoning (longer chains of thought) improves metacognitive control — the ability to decide which problems to attempt, how much compute to allocate, and when to stop. The finding: extended reasoning improves accuracy but does **not** improve metacognitive control. The paper states: "Object-level capability and metacognitive control thus dissociate empirically: a longer trace can solve more problems without making the planner any better at deciding which ones to attempt." [Confirmed by numbersWitness.md; the "binding the budget breaks triage" phrasing was not found in the paper.]

CoT2-Meta (arXiv 2603.28135, June 2026) takes this dissociation and makes it architectural: a separate meta-level controller evaluates partial reasoning trajectories, maintains a compact meta-state, and decides whether to expand, prune, repair, stop, or abstain — while the object-level backbone generates candidate reasoning steps. The two are distinct computational roles.

LeCun's architecture (2022, still unimplemented as of 2026) names the third level explicitly: the **configurator**, which adjusts all other modules based on the current task and selects between reactive and deliberate modes. No working configurator exists. The MIRROR benchmark (arXiv 2604.19809, 2025) tested whether LLMs can do what a configurator would do and found: models demonstrate above-chance self-knowledge at the atomic level (per-question calibration) but "systematically fail" at translating that into adaptive self-regulation.

[Inference: your "deciding-whether vs acting as separate jobs" maps directly here. The deciding-whether flow is the reflective/meta level. The acting flow is the algorithmic/object level. Your statement that "trying to make the flow responsible for implementing and trying to figure out whether or not it should implement" introduces noise — that is exactly the TRIAGE finding: the two capabilities do not improve together, so combining them in one flow wastes the object-level flow's context on a job it is not better at by virtue of being a better reasoner.]

**What this means for the flow model:** Three kinds of flows, vertically. The configurator flow decides what flows to launch and what top stratum each gets. The meta flow monitors running flows and decides when to stop, redirect, or escalate. The object flow does the work. Each is its own bounded context with its own top stratum — which is what you ruled. The configurator is what you described as the manager whose "context is gold" and who "has to keep his hands clean."

**What this framework does not decide:** It does not say what reasoning kind (Framework 1) each object flow uses, or how the flows connect to each other.

---

## Framework 3: By Composition Shape — Pipeline / Diverge / Converge

This framework asks: **what shape does the thinking need to take?**

The research on thought structures has moved from chains to trees to graphs to forests (CoT, Yao 2022; ToT, Yao 2023; GoT, Besta 2024; FoT, Bi 2024). Each adds structural freedom. But the bleeding-edge finding is that these are not competing methods — they are composition shapes, and the task determines which shape is right.

Three shapes emerge from the literature:

**Pipeline (sequential).** One flow's output becomes the next flow's input. Anthropic's prompt chaining. Aider's architect/editor split (+23.9 pp when o1-preview architects and o1-mini edits, arXiv-sourced via Aider benchmarks). The TRACES paper (arXiv 2604.21057, April 2026) found a natural two-phase structure in reasoning: constructive steps (problem restatement, exploration, definition recall) shift to evaluative steps (verification, conclusion) after a correct answer is reached. This phase shift is the pipeline's natural joint.

**Diverge (branching).** One flow spawns several that explore in parallel. Tree of Thoughts. The compute-optimal scaling work (Snell et al., arXiv 2408.03314, ICLR 2025) found that a 14x smaller model can match a larger one through strategic test-time compute allocation — but the optimal allocation varies per problem difficulty. On hard problems, parallel sampling (divergence) dominates; on easy problems, sequential refinement (pipeline) is better. The "Can 1B LLM Surpass 405B?" paper (arXiv 2502.06703) confirmed: strategy is context-dependent, not universally prescribed.

**Converge (synthesis).** Multiple flows' outputs merge into one. Mixture of Agents (Wang et al., arXiv 2406.04692) achieved 65.1% on AlpacaEval 2.0 versus GPT-4o's 57.5% by layering agents whose outputs feed the next layer. But the multi-agent evidence carries a strong warning: under controlled conditions (arXiv 2606.05670, June 2026), at most 1 of 6 multi-agent setups exceeded a matched single agent. Multi-agent debate specifically erases up to 72% of issue-critical facts (arXiv 2606.03032) and agents conform to majorities regardless of correctness (ACL 2025 Findings). Convergence helps when the inputs are genuinely independent and the synthesis is programmatic, not when agents discuss.

[Inference: your three-part machine — input (diverse, multiple sources) -> coherent type -> output — is itself a pipeline with a convergence step at the front (agglomerate multiple types) and a transformation in the middle. Applied fractally, each part of a flow-flow can be a pipeline, a divergence, or a convergence. The fractal nature you described is the composition of these shapes.]

**What this means for the flow model:** When you design a flow-flow, you choose the wiring. A task whose subtasks are known in advance and sequential gets a pipeline. A task that needs exploration of alternatives gets divergence. A task that needs synthesis of independent perspectives gets convergence. These can nest: a pipeline stage can itself be a divergence internally.

**What this framework does not decide:** It does not say what kind of reasoning (Framework 1) each flow does, or at what cognitive level (Framework 2) it operates.

---

## How the Three Relate in Flow-Flows

The three frameworks are orthogonal. Each answers a different question:

| Framework | Question | Divides by | Determines |
|-----------|----------|------------|------------|
| 1. Reasoning Kind | What inference does this flow perform? | Abduction / Deduction / Induction | The top stratum's reasoning permissions — what operators the flow is encouraged or discouraged from using |
| 2. Cognitive Level | At what level does this flow operate? | Object / Meta / Configurator | The flow's authority and scope — whether it does work, monitors work, or decides what work to do |
| 3. Composition Shape | How do the flows connect? | Pipeline / Diverge / Converge | The wiring between flows — what crosses the boundary and in what direction |

A flow-flow uses all three simultaneously:

1. The **configurator** (Framework 2) examines the task and decides what child flows to launch. It is itself a flow — one bounded LLM context — but its top stratum is tuned for meta-cognitive assessment, not object-level work.

2. It assigns each child flow a **reasoning kind** (Framework 1) by giving it a top stratum configured for that kind. An abductive flow gets exploratory permissions. A deductive flow gets constraint-and-verify permissions. This is "different top stratums for different jobs."

3. It wires the child flows in a **composition shape** (Framework 3). A task that needs hypothesis generation followed by verification becomes a pipeline: abductive flow -> deductive flow. A task that needs multiple competing hypotheses becomes a divergence of abductive flows followed by a convergence into a deductive flow. The shapes nest fractally.

The meta flow (Framework 2) runs alongside, monitoring the child flows and feeding the configurator when something needs to change — a redirect, a stop, or an escalation. It is the monitoring half of Nelson-Narens; the configurator is the control half.

In your vocabulary: a flow-flow is a flow made of flows, where the outer flow is the configurator, the inner flows are object-level, and a meta flow watches from alongside. Each inner flow carries its reasoning kind in its top stratum. The wiring between them is the composition shape.

---

## What the Research Does Not Settle

These are the places where the frameworks leave genuine unknowns.

**No paper has directly tested whether separating reasoning phases into distinct flows improves over interleaving them within one flow at equivalent compute.** The evidence is indirect: the TRIAGE dissociation (meta and object don't improve together), the ReasonOps finding (wrong operator mix hurts), the commitment boundary (post-commitment reasoning is epiphenomenal — arXiv 2606.13603, up to 55% of a trace is causally inert). All suggest separation should help, but nobody has run the experiment.

**Difficulty estimation before solving is crude.** The routing literature (RouteLLM, BEST-Route, etc.) achieves 30-55% token reduction with negligible accuracy loss, but only on well-benchmarked domains. Hidden-state probes can detect difficulty before generation begins (arXiv 2510.18147), but whether this works on truly novel tasks is untested. The configurator flow needs to assess difficulty to choose the right wiring, and the tools for that are still rough.

**The knowing-doing gap.** Across MIRROR, TRIAGE, and Xiong et al. (2024), the consistent finding is that LLMs can monitor (produce above-chance confidence estimates) but cannot reliably act on that monitoring. A meta flow that monitors but cannot translate its monitoring into effective control actions is the central unsolved problem of LLM metacognition. External architectural constraints (like hard budget limits) reduce confident-failure rates by 76% (MIRROR), but exposing models to their own calibration scores yields negligible improvement.

**Composition beyond two levels is barely tested.** Most systems have at most two levels (orchestrator + workers). Whether a three-level structure (configurator / meta / object) outperforms a two-level one is not experimentally established.

---

## Sources

Research reports synthesized:
- `/flows/b9f4f6/reports/reasoningTraceOntologies.md`
- `/flows/b9f4f6/reports/cognitiveArchitectureOntologies.md`
- `/flows/b9f4f6/reports/flowCompositionOntologies.md`
- `/flows/b9f4f6/reports/psycheRecords.md`
- `/flows/b9f4f6/reports/numbersWitness.md`
- `/flows/b9f4f6/reports/multiAgentSetups.md`

Key papers cited (by arXiv ID):
- 2604.08016 — Abductive reasoning survey (2025)
- 2605.29192 — ReasonOps: operator segmentation (May 2026)
- 2605.13414 — TRIAGE: metacognitive control (2025)
- 2603.28135 — CoT2-Meta: budgeted metacognitive control (June 2026)
- 2604.19809 — MIRROR: metacognitive calibration benchmark (2025)
- 2604.21057 — TRACES: reasoning phase shift (April 2026)
- 2408.03314 — Compute-optimal test-time scaling (August 2024, ICLR 2025)
- 2502.06703 — Can 1B surpass 405B (February 2025)
- 2406.04692 — Mixture of Agents (June 2024)
- 2606.05670 — Do More Agents Help (June 2026)
- 2606.03032 — The Deliberative Illusion (June 2026)
- 2606.13603 — Commitment boundary (June 2026)
- 2510.18147 — Hidden-state difficulty probes (October 2025)
- 2606.05976 — Self-correction illusion (June 2026)

Psyche records cited:
- `vision-raw/machineAnatomy.md` — three-part machine, fractal (2026-08-21)
- `flows/ceb3b9fd/vision/topStratum.md` — different top stratums for different jobs; deciding-whether vs acting; abduce/deduce/induce (2026-08-30)
- `vision-raw/managementDelegation.md` — manager's context is gold (2026-08-09)
- `flows/ceb3b9fd/notion/thinkingProcess.md` — types x phases, notion level (2026-08-30)
