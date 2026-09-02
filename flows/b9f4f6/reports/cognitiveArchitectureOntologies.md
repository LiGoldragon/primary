# Cognitive-Architecture and Metacognition Ontologies Applied to LLM Agents

**Flow:** b9f4f6  
**Date:** 2026-09-02  
**Scope:** 2024–2026 uptake of cognitive-architecture ontologies, metacognition frameworks, and formal ontologies of thinking as applied to LLM agents. Primary sources preferred; sourced claims, training-knowledge claims, and inferences labelled.

---

## 1. CoALA — Cognitive Architectures for Language Agents

**Division proposed** (verbatim from the paper):

- **Memory:** Working memory (active variables for the current decision cycle), plus three long-term stores: procedural (implicit in LLM weights + explicit in agent code), semantic (world/self knowledge, initialised from DBs or built by reasoning), episodic (prior decision-cycle experience — training pairs, trajectories, event histories).
- **Action space:** External actions (physical, dialogue, digital environments) and internal actions: retrieval (long-term → working memory), reasoning (transform working memory contents), learning (working memory → long-term memory).
- **Decision-making cycle:** Repeated propose → evaluate → select → execute loop. Planning interleaves reasoning and retrieval across sub-stages; execution invokes procedures from the agent code.

**Composition model:** The decision cycle is "analogous to a program's 'main' procedure … that runs in loops continuously." Agent code divides into action procedures and decision-making procedures; the latter can nest the former. There is no explicit meta-level that selects *which* cognitive process to invoke — the choice "emerges from the agent's programmed decision-making procedures and environmental context." The LLM call synthesises working-memory contents into a prompt; its output is parsed back into working-memory variables.

**Basis:** Theoretical — draws on classical cognitive architectures (SOAR, ACT-R) applied retrospectively to organise ~100 recent agent papers (Sumers, Yao et al., September 2023, published TMLR February 2024).

**Critiques (sourced):**
- "Procedural Memory Is Not All You Need" (2025) argues procedural-memory-centric LLM architectures fail in complex, dynamic environments requiring flexible reasoning and recall. [Source: https://arxiv.org/pdf/2505.03434]
- CoALA's simplicity is "both its strength and its limitation" — a conceptual framework, not a comprehensive solution. [Source: https://www.cognee.ai/blog/fundamentals/cognitive-architectures-for-language-agents-explained]
- A 2025 governance paper ("From Craft to Constitution") critiques CoALA-style architectures for lacking explicit governance and constraint mechanisms. [Source: https://arxiv.org/pdf/2510.13857]

**What it predicts about which thinking a task needs:** Nothing explicit. The framework describes the *space* of possible architectures but does not itself contain a classifier or meta-level selector.

[Source: https://arxiv.org/abs/2309.02427, https://arxiv.org/html/2309.02427v3]

---

## 2. Minsky — Society of Mind and Emotion Machine

### 2a. Society of Mind (1986)

**Division:** Intelligence emerges from many small, specialised "agents" (not LLM agents — simple processes), none individually intelligent. No central controller; coherent behaviour arises from interaction among agents organised in societies, with "K-lines" linking agents activated together.

**Composition:** Society — flat or loosely hierarchical. Agents compete and cooperate; higher-level agencies (e.g., "Builder") coordinate lower-level ones. The composition is heterarchical: there is no single stack; different agencies can claim control.

**Basis:** Theoretical/architectural, no experimental validation.

### 2b. The Emotion Machine (2006)

**Division — six levels of mental activity** (verbatim):

1. **Instinctive reactions** — innate responses that help survival
2. **Learned reactions** — conditioned stimulus-response pairs
3. **Deliberative thinking** — considering several alternatives and choosing the best
4. **Reflective thinking** — reacting to internal mental events, not just external ones
5. **Self-reflective thinking** — engaging models of oneself and one's possible futures
6. **Self-conscious reflection** — thinking about "higher" values and ideals

**Meta-level mechanism — Critics and Selectors:** Minsky introduces "critics" that detect problems at each level and "selectors" that activate alternative "Ways to Think." When one way of thinking fails, a critic fires, switching the system to a different resource (way to think). This is the explicit "level above" mechanism: a critic monitors the current process and triggers a change in cognitive strategy.

**Composition:** Vertical tower — each level monitors and can override the ones below. But the levels are not a strict pipeline; critics can fire cross-level.

**Current application to LLMs (training-knowledge claim, corroborated by search):** Multi-agent LLM systems (AutoGen, CrewAI, etc.) are widely discussed as "Society of Mind" realisations, with specialised LLM agents cooperating. A 2025 paper applies the Society of Mind framework to real-time strategy games with hierarchical multi-agent LLM reasoning. However, no rigorous mapping of Minsky's six levels onto LLM architectures was found in 2024–2026 literature — the references are analogical, not formal.

[Sources: https://medium.com/@adnanmasood/minskys-society-of-mind-in-2025-durable-ideas-dated-machinery-pragmatic-leadership-lessons-7519d09a5bc9, https://arxiv.org/pdf/2508.06042]

---

## 3. Dennett — Tower of Generate-and-Test

**Division — four kinds of creatures** (verbatim from Dennett 1995):

1. **Darwinian creatures** — adapt only via genetic evolution across generations; no within-lifetime learning
2. **Skinnerian creatures** — learn via trial-and-error reinforcement; must act to learn
3. **Popperian creatures** — simulate actions internally, "letting hypotheses die in their stead" (Popper); anticipate outcomes before acting
4. **Gregorian creatures** — extend cognition with language, tools, and culture; cumulative knowledge and abstract thought

**Composition:** Strict tower — each level subsumes the ones below. A Gregorian creature is also Popperian, Skinnerian, and Darwinian. The "level above" is implicit in the tower structure: higher creatures have richer internal models and can pre-test more before acting.

**Basis:** Theoretical (evolutionary epistemology).

**Application to LLMs (2024–2026):** No substantial direct application found. The framework was used in earlier robotics work (Storybots, 2021). Winfield (2007) proposed "Walterian creatures" between Skinnerian and Popperian. The 2025–2026 agent literature does not explicitly invoke Dennett's tower, though the idea of internal simulation before action (Popperian) is structurally present in all chain-of-thought and planning-before-acting architectures.

**What it predicts:** A task requiring internal simulation before acting demands at least a Popperian agent; a task requiring cultural/linguistic tools demands a Gregorian agent. The hierarchy predicts that more complex tasks require higher levels of generate-and-test.

[Sources: https://academic.oup.com/book/25912/chapter-abstract/193644342, https://alanwinfield.blogspot.com/2007/04/walterian-creatures.html]

---

## 4. Stanovich — Tripartite Mind

**Division** (verbatim from Stanovich 2011, "Rationality and the Reflective Mind"):

1. **Autonomous mind (TASS — The Autonomous Set of Systems)** — fast, parallel, automatic processes; includes both innate modules and overlearned routines
2. **Algorithmic mind** — sustains processing of decoupled secondary representations in cognitive simulation; measured by IQ-type tests; individual differences in computational power
3. **Reflective mind** — detects the need to interrupt autonomous processing and begin simulation; initiates and sustains override; individual differences in thinking dispositions (need for cognition, open-mindedness)

**Key insight vs. dual-process theory:** Stanovich argues the traditional "System 2" must be split. The algorithmic mind is *how well* you can reason; the reflective mind is *whether you notice you should reason* and *what epistemic standards you apply*. Rationality is a more encompassing construct than intelligence because it requires the reflective mind, not just the algorithmic one.

**Composition:** The reflective mind monitors autonomous processing and triggers algorithmic-mind engagement when override is warranted. The algorithmic mind does the computational work. The autonomous mind runs by default.

**Meta-level:** The reflective mind *is* the meta-level — it decides when to engage effortful thinking and which standards to apply.

**Application to LLMs (2024–2026):** The AAAI 2022 Fall Symposium explicitly mapped System 1 and System 2 onto the Common Model of Cognition, referencing Stanovich's refinement. However, no 2024–2026 paper was found that directly implements Stanovich's tripartite division in an LLM agent. The tripartite structure is implicitly present in work that distinguishes "fast" LLM output, "slow" chain-of-thought reasoning, and a meta-level that decides when to use which — but this connection remains informal.

[Sources: https://www.semanticscholar.org/paper/Distinguishing-the-reflective,-algorithmic,-and-Is-Stanovich/435b8ce2b431ff1797008ae4633ba4fd3549c8fc, https://arxiv.org/pdf/2305.09091]

---

## 5. Dual-Process Theory as Applied to LLM Agents

### 5a. The Basic Mapping

**System 1 (fast, intuitive, automatic)** → LLM's direct single-pass output, heuristic-driven, low-latency.  
**System 2 (slow, deliberate, analytical)** → Chain-of-thought, multi-step reasoning, planning, self-correction.

### 5b. Key 2024–2026 Works

**Brady et al. (2025), Nature Reviews Psychology:** LLMs mimic both System-1 and System-2-like responses depending on prompting. However, LLM "cognitive" biases reflect training-data patterns, not dual-process architecture. The mapping is "not fully analogous to human dual-process cognition" — LLMs exhibit non-human biases (hallucination). The authors caution against treating the mapping as more than metaphorical. [Source: https://www.nature.com/articles/s44159-025-00506-1]

**Marzouk et al. (2025), "Reasoning on a Spectrum":** Operationalises dual-process theory via preference alignment. System-1-aligned models show higher token confidence, shorter responses, fewer hedging words. System-2-aligned models show greater uncertainty, longer elaborations. A dynamic entropy-based selector outperforms both on 12/13 benchmarks by choosing the system whose output has lower normalised entropy + entropy variance. [Source: https://arxiv.org/html/2502.12470]

**DPT-Agent (2025):** System 1 = Finite-state Machine + code-as-policy (executes every 0.25s). System 2 = LLM-driven Theory of Mind + asynchronous reflection (runs periodically). The two systems run asynchronously — System 2 periodically updates "Behavior Guidelines" that shape System 1's code-as-policy generation. No explicit switching trigger; System 2 runs on a timer (every λ timesteps). [Source: https://arxiv.org/abs/2502.11882]

**DualSpec (2026):** A System-1.x Planner decomposes deep-research tasks into sub-steps, assigning System 1 (speculative, fast) strategies to simple sub-steps and System 2 (deliberative, LLM-intensive) to complex ones. A lightweight confidence-based semantic verifier checks speculated actions. [Source: https://arxiv.org/html/2603.07416v1]

### 5c. Disagreements

- Brady et al. (2025) argue the dual-process mapping is metaphorical and potentially misleading; LLM biases have different origins than human cognitive biases.
- Marzouk et al. (2025) show a *continuous spectrum* rather than a binary split: "a monotonic change in accuracy" through interpolated models.
- Stanovich (see §4) argues the binary split is insufficient even for humans — you need three levels, not two.
- The DPT-Agent and DualSpec papers treat the division as an engineering choice (which subsystem handles which sub-task) rather than a cognitive claim.

---

## 6. Nelson–Narens Metacognition and LLM Metacognition

### 6a. The Framework

Nelson and Narens (1990) organise cognition into two interacting levels:

- **Object level** — where primary cognitive processes occur
- **Meta level** — maintains a model of the object-level process

The two levels interact through:
- **Monitoring** — information flows from object level to meta level (confidence judgments, feeling of knowing, ease of learning)
- **Control** — meta level modifies object-level processing (allocation of study time, selection of strategies, termination of search)

### 6b. Key 2024–2026 Applications to LLMs

**Monitor-Generate-Verify / MGV (2025):** Formalises metacognition for LLM reasoning as three phases. Monitor assesses difficulty and retrieves strategy knowledge (agent, task, strategy variables). Generate selects and executes a reasoning strategy based on monitoring output, with resource allocation inverse to confidence. Verify evaluates outcomes and updates metacognitive knowledge. Introduces dynamic confidence thresholds: λ^(τ+1) = λ^(τ) · β_τ (thresholds lower as search cost accumulates). [Source: https://arxiv.org/html/2511.04341v2]

**TRIAGE (2025):** Operationalises three Nelson-Narens control functions prospectively: selection (which problems to attempt), allocation (how much compute per problem), termination (ex-ante budget cutoffs). Key finding: extended reasoning (e.g., o1-style) improves accuracy but *does not improve metacognitive control* — models rarely honour their own budget allocations. Only Gemini 2.5 Flash achieved positive triage efficiency across all benchmarks. The reasoning-accuracy paradox: "binding the budget breaks triage" for nearly all models. [Source: https://arxiv.org/html/2605.13414v1]

**MIRROR Benchmark (2025):** Decomposes LLM metacognition into four hierarchical levels: Level 0 (atomic self-knowledge — per-question calibration), Level 1 (cross-domain transfer — does calibration in one domain predict another), Level 2 (compositional prediction — can the model predict performance on multi-domain tasks), Level 3 (adaptive self-regulation — translating self-knowledge into action). Key finding: models demonstrate above-chance Level 0 but systematically fail at Levels 2–3. External architectural constraints reduce confident-failure rates by 76%, but exposing models to their own calibration scores yields negligible improvement. [Source: https://arxiv.org/html/2604.19809v1]

**Metacognitive Monitoring Battery (2025):** A 524-item cross-domain assay grounded in Nelson-Narens, applying human psychometric methodology to LLMs across six cognitive domains (learning, metacognitive calibration, social cognition, attention, executive function, prospective regulation). [Source: https://arxiv.org/pdf/2604.15702]

**Xiong et al. (2024):** Found pervasive overconfidence when LLMs verbalise confidence — predominantly in the 80–100% range. Scholten et al. (2024) argued LLMs exhibit "metacognitive myopia" — lacking genuine monitoring-control coupling.

### 6c. The Knowing-Doing Gap

The consistent finding across MIRROR, TRIAGE, and related work: LLMs have some monitoring capacity (they can produce above-chance confidence estimates) but poor control capacity (they do not reliably act on that monitoring — they do not adjust resource allocation, strategy selection, or termination based on what they "know" about their own competence).

---

## 7. Resource-Rational Analysis and Rational Metareasoning

### 7a. The Framework

Lieder & Griffiths (2020) propose that human cognition is *resource-rational*: cognitive strategies are optimal given computational constraints. A resource-rational agent allocates finite compute where expected return is highest.

**Rational metareasoning** (Russell & Wefald 1991, extended by Lieder & Griffiths) formalises this as: before computing further, estimate the Value of Computation (VOC) — the expected improvement in decision quality minus the computational cost. Compute more only when VOC > 0.

### 7b. Application to LLMs

**RaM — Rational Metareasoning for LLMs (2024):** Griffiths is a co-author. Defines VOC for LLM reasoning chains as:

VOC(c,b) = E[max_a' E[U(a')|b'] − max_a E[U(a)|b]] − cost(c)

Operationalised as a reward function: R_π(x,y,z) = U_π(z|x,y) − C(z), where utility measures how much a reasoning chain increases correct-output likelihood and cost equals token count × scaling factor γ. Uses Expert Iteration: generate K chains per problem, filter by positive advantage (VOC > 0), fine-tune, repeat. Results: 23–32% fewer tokens vs. STaR, 35–42% vs. CoT prompting, without accuracy loss. On easy problems, 50.3% length reduction; hard problems retain longer reasoning. [Source: https://arxiv.org/abs/2410.05563]

**TRIAGE (2025, see §6b):** Tests prospective resource allocation — models must commit budgets before execution. Finding: current models fail at rational compute allocation even when they can solve the underlying problems.

**"Not All Errors Are Equal" (2026):** Proposes consequence-aware compute allocation — allocating reasoning tokens based on the *cost of error* rather than problem difficulty alone. [Source: https://arxiv.org/html/2606.04402]

### 7c. What This Predicts

Resource-rational analysis predicts that the right amount of thinking depends on both task difficulty and the marginal value of additional computation. It provides a formal criterion for the "level above": a metareasoning module that estimates VOC and allocates compute accordingly. The empirical finding is that current LLMs lack this module — they overthink easy problems and underthink hard ones (or allocate uniformly).

---

## 8. Newell's Bands and SOAR/ACT-R Hybrids with LLMs

### 8a. Newell's Bands

Newell (1990, "Unified Theories of Cognition") proposed four bands of cognition at different time scales:

1. **Biological band** (~1ms–100ms) — neural circuit operations
2. **Cognitive band** (~100ms–10s) — elementary cognitive operations, production firings
3. **Rational band** (~10s–hours) — goal-directed problem solving, planning
4. **Social band** (~hours–months) — organisational and cultural processes

**Composition:** Bands are nested by time scale. Each band's operations are composed of many operations from the band below.

### 8b. SOAR and ACT-R

**SOAR:** Uses production rules in a recognise-act cycle. All knowledge as productions. Problem solving via universal subgoaling. Learning via chunking (compiling deliberate solutions into productions).

**ACT-R:** Modular: declarative memory (chunks), procedural memory (productions), perceptual-motor modules. Subsymbolic layer assigns activation to chunks and utility to productions, enabling Bayesian-rational retrieval and conflict resolution.

### 8c. Hybrid LLM Integration (2024–2025)

**Cognitive LLMs / LLM-ACTR (Wu et al., 2025):** Integrates ACT-R cognitive traces with LLaMA-2 13B via LoRA fine-tuning. ACT-R generates decision traces at novice/intermediate/expert levels; these are embedded and injected into the LLM's hidden layers. The LLM serves as System 1 (fast, intuitive); ACT-R provides System 2 grounding (deliberate, cognitively plausible). Tested on manufacturing decision-making. [Source: https://arxiv.org/pdf/2408.09176, https://journals.sagepub.com/doi/10.1177/29498732251377341]

**Cognitive AI Framework 2.0 (2025):** Advances simulation of human thought by combining cognitive architecture principles with LLM capabilities. [Source: https://arxiv.org/pdf/2502.04259]

**Heartbeat-driven scheduling (2025):** Proposes a scheduling model inspired by Newell's bands where an LLM agent's cognitive activities are triggered at different temporal rhythms, separating reactive (fast) from reflective (slow) processing. [Source: https://arxiv.org/pdf/2604.14178]

**Key tension:** Classical architectures (SOAR, ACT-R) provide formal grounding and human-aligned constraints but are rigid and domain-specific. LLMs provide flexibility and language competence but lack formal cognitive structure. Current hybrids inject cognitive traces into LLMs rather than achieving genuine architectural integration.

---

## 9. LeCun's Modular World-Model Architecture

### 9a. The Architecture (from LeCun's 2022 "A Path Towards Autonomous Machine Intelligence")

Seven modules:

1. **Perception** — estimates current state of the world from sensory input
2. **World model** — predicts plausible future states as a function of imagined actions (using JEPA — Joint Embedding Predictive Architecture)
3. **Actor** — proposes action sequences and selects those that reduce expected cost
4. **Cost module (intrinsic)** — fixed, non-learned objectives (avoid damage, maintain homeostasis)
5. **Critic (trainable cost)** — predicts long-term consequences; learns to estimate downstream costs
6. **Short-term memory** — workspace holding current and imagined states during reasoning
7. **Configurator** — adjusts all other modules based on current task/subgoal; executive controller

### 9b. Two Modes of Operation

- **Mode 1 (Reactive):** Familiar, time-critical situations — practiced skills executed quickly without deep world-model simulation
- **Mode 2 (Deliberate):** Novel or complex problems — configurator activates intensive planning via world-model simulation of multiple futures

### 9c. Hierarchical Planning (H-JEPA)

Three levels of abstraction: low-level sensory details, middle-level object interactions, high-level abstract goals. The configurator decomposes complex goals into subgoals and activates appropriate abstraction levels for different planning horizons.

### 9d. 2025–2026 Status

- V-JEPA 2 (June 2025): trained on 1M hours of internet video, ~80% success on zero-shot robotic manipulation.
- V-JEPA 2.1 (March 2026): improved temporal consistency.
- LeCun left Meta in early 2026 to co-found AMI Labs ($1.03B funding) specifically to build general-purpose world models.
- The full seven-module architecture with a working configurator has *not* been demonstrated. V-JEPA implementations cover perception and world model; the configurator, cost module, and actor remain architectural proposals.

[Sources: https://kodu.ut.ee/~hadachi/Lecture_Notes/lecun_vision_ai_lecture_notes.html, https://www.taskade.com/blog/ai-world-models, https://www.turingpost.com/p/jepa]

### 9e. What It Predicts

The configurator is the explicit meta-level: it decides whether to use Mode 1 (reactive) or Mode 2 (deliberate) and configures the world model for the current task. This is the most architecturally explicit "level above" in any framework reviewed here. However, the mechanism by which the configurator itself decides is unspecified.

---

## 10. Global Workspace Theory Implementations

### 10a. The Theory

Baars' Global Workspace Theory (GWT, 1988) proposes that consciousness arises from a "global workspace" — a shared information bus that receives competing inputs from specialised modules. When a module's signal "wins" the competition, it is "broadcast" globally, making it available to all other modules. This broadcast-and-compete cycle is the mechanism of conscious access.

### 10b. Key Implementations (2024–2026)

**Yoshida et al. (2024):** Argues that if GWT is correct, language agents (LLM-based) might already satisfy the sufficient conditions for phenomenal consciousness, or could easily be made to. They articulate a methodology for applying consciousness theories to AI systems. [Source: https://arxiv.org/abs/2410.11407]

**CTM-AI — Conscious Turing Machine (Blum, Blum & Blum, 2025–2026):** The first practical instantiation of the Conscious Turing Machine, grounding GWT in a formal 7-tuple machine model. Uses up-tree competition for workspace access and down-tree broadcast. Processors range from specialised experts (vision-language models, search engines) to unspecialised general-purpose learners. All processors have equal priority; competition is dynamic at each iteration. Submitted to ICLR 2026; monograph forthcoming 2026. [Source: https://arxiv.org/pdf/2605.04097]

**Embodied GWT agent (2024):** Trained to navigate 3D environments with audiovisual inputs; the global workspace architecture outperformed standard recurrent architectures at smaller working memory sizes. [Source: https://frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2024.1352685]

### 10c. Composition

GWT's composition is broadcast-and-compete: modules are parallel and specialised; the workspace is the shared bus. There is no hierarchy among modules (any can win); the "level above" is the competition-and-broadcast mechanism itself, which is emergent rather than designed.

---

## 11. Active Inference with LLMs

### 11a. The Framework

Active inference (Friston 2010) proposes that adaptive systems minimise *expected free energy* (EFE) — a cost function combining:
- **Pragmatic value** (utility — achieving desired outcomes)
- **Epistemic value** (information gain — reducing uncertainty about the world)

This unifies exploration and exploitation under a single objective. Agents maintain generative models of the world and act to confirm predictions or resolve uncertainty.

### 11b. Application to LLMs (2024–2025)

**Mazzaglia et al. (2024):** Treats LLM behaviour as approximate active inference, where the model's next-token prediction approximates free-energy minimisation over a world model implicit in its weights. [Source: https://ceur-ws.org/Vol-3923/Paper_3.pdf]

**Kucharski et al. (2024):** Active inference for self-organising multi-LLM systems using a "Bayesian thermodynamic approach." Models prompt combinations and search strategies as state factors; free-energy minimisation drives exploration. Three state factors (prompt, search, information states) with seven observation modalities. [Source: https://arxiv.org/abs/2412.10425]

**EFE-based Planning (2025):** Expected free energy as variational inference, extending active inference to structured planning problems. [Source: https://arxiv.org/abs/2504.14898]

### 11c. What It Predicts

Active inference predicts that an agent should seek information (epistemic actions) when uncertainty is high and exploit (pragmatic actions) when the model is confident. The "level above" is the EFE computation itself — it determines whether to explore or exploit. This provides a principled, Bayesian answer to the meta-question "what kind of thinking does this task need?"

### 11d. Limitations

No large-scale LLM agent system has been demonstrated using active inference as its primary decision framework. The implementations remain small-scale or domain-specific. The relationship between next-token prediction and free-energy minimisation is theorised but contested.

---

## 12. Formal Cognitive Ontologies

### 12a. Cognitive Atlas

The Cognitive Atlas (Poldrack et al., 2011, ongoing) is a collaborative ontology of mental processes used in cognitive neuroscience. Two branches:
- **Cognitive concepts** — mental processes (working memory, cognitive control, episodic memory) with formal definitions and hierarchical relationships
- **Tasks** — experimental paradigms linked to the concepts they measure

Its primary function is enabling cross-study comparison of fMRI datasets. It is *not* used to organise AI evaluation — no 2024–2026 work was found applying it to benchmark LLM cognition.

[Source: https://www.cognitiveatlas.org/]

### 12b. MindOntology and Others

No active project called "MindOntology" was found in 2024–2026 literature. The search returned the Cognitive Atlas as the primary formal cognitive ontology. The "Problem of Cognitive Ontology" is an active research area in philosophy of neuroscience (Pitt Center for Philosophy of Science runs a seminar series), but it has not produced a competing formal ontology used in AI.

### 12c. Bloom's Taxonomy

Bloom's Taxonomy (Remember, Understand, Apply, Analyse, Evaluate, Create) continues to be used to structure AI-based cognitive assessment, including LLM evaluation (sourced from search results, 2025). However, it is a pedagogical framework, not a cognitive-science ontology.

### 12d. Benchmark Taxonomies of Reasoning Kinds

**Tripartite reasoning taxonomy** (used in LogiGLUE, LogiEval, Multi-LogiEval, and the 2025 abductive reasoning survey):
- Deductive — non-defeasible, monotonic, non-ampliative (truth-preserving)
- Inductive — defeasible, non-monotonic, ampliative (pattern-generalising)
- Abductive — defeasible, non-monotonic, ampliative (explanation-generating)

Key finding from the abductive reasoning survey (2025): "Strong deductive or inductive capabilities do not reliably predict strong abductive reasoning performance." The three are dissociable in LLMs. [Source: https://arxiv.org/html/2604.08016v1]

Additional reasoning types in benchmarks but not formally ontologised: causal reasoning, analogical reasoning, spatial reasoning, temporal reasoning, commonsense reasoning.

### 12e. Agent-Capability Taxonomies (2025–2026)

**Comprehensive Survey on Agent Skills (2025):** Defines skills as tuples S = (M, R, C) — root instruction, auxiliary resources, applicability conditions. Taxonomy is by resource type (text-backed, code-backed, hybrid) and lifecycle (representation, acquisition, retrieval, evolution), *not* by cognitive type. [Source: https://arxiv.org/html/2605.07358v1]

**Agentic Ontology of Work / AOW (2026):** Eight entity types for enterprise agents: Agents, Skills, Intents, Contexts, Policies, Memory, Confidence, Outcomes. This is a deployment ontology, not a cognitive one. [Source: https://kenhuangus.substack.com/p/why-ontology-matters-for-agentic]

**Six-dimensional agent taxonomy (2025):** Core Components, Cognitive Architecture, Learning, Multi-Agent Systems, Environments, Evaluation. The "Cognitive Architecture" dimension subdivides into planning types (linear chains, tree-based search, hierarchical decomposition, inference-time reasoning) and reflection mechanisms (verbal reinforcement, self-correction, tool-interactive validation). [Source: https://arxiv.org/html/2601.12560v1]

### 12f. No Unified Ontology of Thinking for AI

No single, comprehensive, formal "ontology of thinking" or "cognitive-skill taxonomy for AI" was found that is both (a) grounded in cognitive science and (b) actually used to organise AI evaluation or agent design in 2024–2026. The benchmark taxonomies use the deductive/inductive/abductive split. The agent taxonomies use engineering categories (planning, retrieval, tool use). The cognitive ontologies (Cognitive Atlas) remain in neuroscience. These three remain disconnected.

---

## 13. Cross-Cutting Analysis

### 13a. What Compositions Are Proposed

| Framework | Composition model | Meta-level mechanism |
|-----------|------------------|---------------------|
| CoALA | Loop (decide-act cycle) | Implicit in code — no explicit meta-level |
| Minsky (EM) | Tower (six levels) + critics | Critics detect failure, selectors switch strategy |
| Dennett | Tower (four creatures) | Implicit — higher creatures subsume lower |
| Stanovich | Three-layer monitor-override | Reflective mind *is* the meta-level |
| Dual-process | Binary or spectrum | Varies — entropy (Marzouk), timer (DPT-Agent), task decomposition (DualSpec) |
| Nelson-Narens | Two-level monitor-control | Monitoring informs control; control modifies object-level |
| Resource-rational | Formal VOC computation | Metareasoning computes VOC before each reasoning step |
| Newell/SOAR/ACT-R | Bands (time-scale nesting) | Subsymbolic utilities (ACT-R) or universal subgoaling (SOAR) |
| LeCun | Pipeline (7 modules) + modes | Configurator selects Mode 1 vs Mode 2 |
| GWT | Broadcast-and-compete | Competition mechanism is the meta-level (emergent) |
| Active inference | Free-energy minimisation loop | EFE balances epistemic vs pragmatic value |

### 13b. Sharpest Disagreements

1. **Is the meta-level a designed module or an emergent property?** LeCun's configurator and Stanovich's reflective mind say designed. GWT and active inference say emergent from competition/optimisation. CoALA says it does not exist as a separate component.

2. **Is dual-process theory a useful framing for LLMs?** Brady et al. (2025, Nature Reviews Psychology) argue it is metaphorical and potentially misleading. Marzouk et al. (2025) and DPT-Agent (2025) treat it as productive engineering. Stanovich says the binary split is wrong even for humans.

3. **Does better reasoning imply better metacognition?** TRIAGE (2025) provides strong evidence that it does *not*: extended reasoning improves accuracy but degrades resource allocation. This contradicts intuitions from Minsky (higher levels subsume lower) and is consistent with Stanovich (the reflective mind is separate from the algorithmic mind).

4. **Are there discrete kinds of thinking or a continuum?** Minsky, Dennett, and Stanovich propose discrete levels. Marzouk et al. (2025) demonstrate a monotonic continuum. The reasoning-benchmark taxonomy (deductive/inductive/abductive) treats kinds as discrete and empirically shows they are dissociable.

5. **The knowing-doing gap.** MIRROR, TRIAGE, and Xiong et al. consistently find that LLMs can monitor (produce calibrated signals) but cannot control (act on those signals). This is the central empirical finding of LLM metacognition research 2024–2026 and it cuts against any architecture that assumes monitoring enables control (as Nelson-Narens' framework predicts for humans).

### 13c. Unknowns

- Whether LeCun's configurator can be implemented (no working version exists as of 2026).
- Whether the knowing-doing gap is fundamental to transformer architectures or an artefact of training objectives.
- Whether the deductive/inductive/abductive taxonomy is the right cognitive ontology for evaluating AI, or whether additional categories (causal, analogical, spatial, metacognitive) need formal treatment.
- Whether any of these frameworks' prescriptions about "which thinking a task needs" can be operationalised as a meta-level module that outperforms simple heuristics (token budget, difficulty classifier).
- Whether Minsky's critic-selector mechanism can be made to work in practice for LLM agents at the scale of real tasks.

---

## Sources

### Primary Papers (accessed/fetched)
- [CoALA — Sumers, Yao et al., 2023/2024](https://arxiv.org/abs/2309.02427)
- [DPT-Agent — Leveraging Dual Process Theory, 2025](https://arxiv.org/abs/2502.11882)
- [Reasoning on a Spectrum — Marzouk et al., 2025](https://arxiv.org/html/2502.12470)
- [RaM — Rational Metareasoning for LLMs — Gureckis, Griffiths et al., 2024](https://arxiv.org/abs/2410.05563)
- [MGV — Monitor-Generate-Verify, 2025](https://arxiv.org/html/2511.04341v2)
- [TRIAGE — Metacognitive Control, 2025](https://arxiv.org/html/2605.13414v1)
- [MIRROR — Metacognitive Calibration Benchmark, 2025](https://arxiv.org/html/2604.19809v1)
- [Metacognitive Monitoring Battery, 2025](https://arxiv.org/pdf/2604.15702)
- [GWT and Language Agents — Yoshida et al., 2024](https://arxiv.org/abs/2410.11407)
- [CTM-AI — Blum, Blum & Blum, 2025–2026](https://arxiv.org/pdf/2605.04097)
- [Cognitive LLMs / LLM-ACTR — Wu et al., 2025](https://arxiv.org/pdf/2408.09176)
- [Abductive Reasoning Taxonomy, 2025](https://arxiv.org/html/2604.08016v1)
- [Agent Taxonomy — Agentic AI, 2025](https://arxiv.org/html/2601.12560v1)
- [Agent Skills Survey, 2025](https://arxiv.org/html/2605.07358v1)
- [DualSpec, 2026](https://arxiv.org/html/2603.07416v1)
- [Active Inference Multi-LLM, 2024](https://arxiv.org/abs/2412.10425)
- [Not All Errors Are Equal, 2026](https://arxiv.org/html/2606.04402)
- [Dual-Process Theory and LLM Decision-Making — Brady et al., Nature Reviews Psychology, 2025](https://www.nature.com/articles/s44159-025-00506-1)
- [Active Inference and NLMs, 2024](https://ceur-ws.org/Vol-3923/Paper_3.pdf)
- [LeCun Architecture Lecture Notes](https://kodu.ut.ee/~hadachi/Lecture_Notes/lecun_vision_ai_lecture_notes.html)
- [Society of Mind Meets Real-Time Strategy, 2025](https://arxiv.org/pdf/2508.06042)
- [Heartbeat-Driven Autonomous Thinking, 2025](https://arxiv.org/pdf/2604.14178)

### Review and Context Sources
- [Minsky's Society of Mind in 2025 — Masood](https://medium.com/@adnanmasood/minskys-society-of-mind-in-2025-durable-ideas-dated-machinery-pragmatic-leadership-lessons-7519d09a5bc9)
- [CoALA Explained — Cognee](https://www.cognee.ai/blog/fundamentals/cognitive-architectures-for-language-agents-explained)
- [Cognitive Atlas](https://www.cognitiveatlas.org/)
- [Stanovich — Tripartite Mind](https://www.semanticscholar.org/paper/Distinguishing-the-reflective,-algorithmic,-and-Is-Stanovich/435b8ce2b431ff1797008ae4633ba4fd3549c8fc)
- [Ontology for Agentic AI, 2026](https://kenhuangus.substack.com/p/why-ontology-matters-for-agentic)
- [World Models — Taskade, 2026](https://www.taskade.com/blog/ai-world-models)
- [JEPA Deep Dive — TuringPost](https://www.turingpost.com/p/jepa)
- [Procedural Memory Not Enough, 2025](https://arxiv.org/pdf/2505.03434)
- [Embodied GWT Agent, 2024](https://frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2024.1352685)
- [Metacognitive LLM Frameworks — EmergentMind](https://www.emergentmind.com/topics/metacognition-driven-llm-frameworks)
- [LLMs Show No Individuated Metacognition, 2025](https://arxiv.org/pdf/2605.24299)
- [System 1/2 in Common Model of Cognition, AAAI 2022](https://arxiv.org/pdf/2305.09091)
- [From Craft to Constitution — Governance, 2025](https://arxiv.org/pdf/2510.13857)
- [Dennett — Towers and Trees](https://academic.oup.com/book/25912/chapter-abstract/193644342)
