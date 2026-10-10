# Cause Identification and Source-Level Remediation: Research Report

## Scope

Research into primary and authoritative thinking on identifying the cause of a failure and remediating it at its source, with extraction of what transfers to LLM-agent failure in a skill-governed multi-flow system. Conducted 2026-08-28.

## I. Systems Safety and Accident Analysis

### Leveson: STAMP and CAST

**Origin:** Primary. Nancy Leveson, *Engineering a Safer World* (MIT Press, 2011, open access). CAST Handbook (MIT, sunnyday.mit.edu).

**Claims:**

- Accidents result from inadequate control or enforcement of safety-related constraints, not from component failure chains. The system's control structure -- its controllers, controlled processes, and feedback channels -- is the unit of analysis.
- CAST (Causal Analysis based on System Theory) is a five-step method: (1) assemble basic information and define boundaries; (2) model the existing safety control structure for the hazard; (3) analyze each component's contribution, including the mental model held by each controller and why it was wrong; (4) identify systemic control structure flaws (communication, safety information system, management design, culture, economic pressures, environmental dynamics); (5) create recommendations as control structure improvements, not patches to individual components.
- Event-chain models (dominoes, Swiss cheese) are fundamentally inadequate for complex systems because they seek a linear causal chain; real accidents arise from the interaction of multiple factors, none individually sufficient.
- "Don't assume accidents are due to one 'root cause' or a few 'probable causes'... most accidents are actually due to many interacting causes."

**Transferable method steps:**

- Model the control structure: who/what governs the agent's behavior (skills, prompts, context assembly), what feedback it receives, what it controls.
- For each controller in the structure, ask: what was its mental model (the context the agent had)? How did that model differ from reality? What information was missing or incorrect?
- Identify flaws in the control structure itself (the skill architecture, context pipeline, feedback channels), not in the individual output.

### Dekker: The New View of Human Error

**Origin:** Primary. Sidney Dekker, *The Field Guide to Understanding 'Human Error'* (3rd ed., Routledge, 2014).

**Claims:**

- The "old view" treats error as the cause of failure; the "new view" treats error as a symptom of deeper trouble in the system. "Human error" is not an explanation but the starting point for investigation.
- To understand why an action made sense to the actor at the time, reconstruct their "local rationality": what they knew, what their goals were, what pressures they faced, what cues they had. Avoid hindsight bias -- the knowledge that things went wrong was not available to the actor.
- Counterfactual reasoning ("they should have done X instead") is a trap: it replaces investigation with judgment.
- The organization, not the individual, is the appropriate level for remediation.

**Transferable method steps:**

- Reconstruct the agent's local rationality: given the context it received, was its output rational? If yes, the fault lies in the context, not the agent.
- Avoid hindsight framing: do not say the agent "should have known" something that was not in its context.
- Remediate at the organizational level: the skill, the context assembly, the feedback mechanism -- not the individual output.

### Hollnagel and Woods: Resilience Engineering, Safety-II

**Origin:** Primary. Erik Hollnagel, *Safety-I and Safety-II* (Ashgate, 2014). Erik Hollnagel, David Woods, Nancy Leveson (eds.), *Resilience Engineering: Concepts and Precepts* (Ashgate, 2006).

**Claims:**

- Safety-I defines safety as freedom from unacceptable risk (absence of bad outcomes). Safety-II defines safety as the ability to succeed under varying conditions. Both success and failure arise from the same performance variability.
- "Human error" is not a meaningful category of cause. Hollnagel's "No View" argues the concept should be abandoned entirely.
- Instead of asking "what went wrong," ask "what normally goes right, and what changed?" Success and failure share the same mechanisms; understanding normal performance variability is prerequisite to understanding failure.

**Transferable method steps:**

- When an agent output is wrong, identify what varied from cases where the same skill produces correct output. The mechanism is the same; the difference is in the conditions.
- Study successful runs, not only failures, to understand the boundary conditions of the skill.

### Reason: Swiss Cheese Model and Latent Conditions

**Origin:** Primary. James Reason, *Managing the Risks of Organizational Accidents* (Ashgate, 1997).

**Claims:**

- No single failure, human or technical, is sufficient to cause an accident. Accidents require the alignment of holes in multiple defense layers.
- Latent conditions are pre-existing weaknesses designed into the system (by its architects, procedures, management decisions) that lie dormant until triggered by an active error. They are the "resident pathogens" of the system.
- Active errors at the sharp end (the point of operation) are consequences, not causes. The real leverage is in fixing latent conditions at the blunt end (system design, management, procedures).

**Transferable method steps:**

- When an agent produces a wrong output (active error at the sharp end), look for latent conditions in the skill design, context pipeline, or system architecture that allowed the error.
- Fix latent conditions (skill rules, context assembly), not the sharp-end manifestation.

### Rasmussen: Drift and Boundaries

**Origin:** Primary. Jens Rasmussen, "Risk management in a dynamic society: A modelling problem," *Safety Science* 27(2-3), 1997.

**Claims:**

- Systems drift toward the boundary of acceptable performance under pressure (economic, workload, efficiency). This drift is a feature of normal adaptation, not a failure.
- The drift is gradual and invisible from inside the system because each individual step is locally rational.
- Prevention requires making the safety boundary visible and counteracting the gradient pressures that push toward it.

**Transferable method step:**

- When a skill-governed system produces increasing numbers of bad outputs, look for drift: have the skills or context assembly been gradually adapted toward efficiency or brevity in ways that eroded the safety constraints?

### Critiques of "Root Cause" and 5-Whys

**Origin:** Primary (Allspaw), secondary (various). John Allspaw, "The Infinite Hows," Kitchen Soap blog, 2014. Google SRE Book, Chapter 15 (Beyer et al., O'Reilly, 2016).

**Claims (Allspaw):**

- "Root causes" are not discovered but constructed: the investigator chooses where to start asking and where to stop. "We've 'found' a root cause when we stop looking."
- "Why?" leads to "who?" -- the method naturally converges on blaming people. Allspaw proposes asking "how?" instead -- seeking narratives and conditions.
- The 5-Whys method assumes linear, single-strand causation; real incidents have multiple diverse contributing conditions.
- Better methods: structured narrative debriefing, Hollnagel's FRAM, Leveson's CAST, Rasmussen's AcciMap.

**Claims (Google SRE):**

- Blameless postmortems focus on "identifying the contributing causes of the incident without indicting any individual or team."
- "You can't 'fix' people, but you can fix systems and processes to better support people making the right choices."
- Investigate "the systematic reasons why an individual or team had incomplete or incorrect information."

**Transferable method steps:**

- Do not seek a single root cause. Seek contributing conditions.
- Ask "how did this happen?" not "why did this happen?" -- trace the mechanism, not the blame.
- Frame the investigation in terms of incomplete or incorrect information -- what was the agent missing?

## II. Debugging as Science

### Zeller: Why Programs Fail

**Origin:** Primary. Andreas Zeller, *Why Programs Fail: A Guide to Systematic Debugging* (2nd ed., Morgan Kaufmann, 2009).

**Claims:**

- Debugging is the application of the scientific method: observe the failure, form a hypothesis about its cause, design an experiment that could refute the hypothesis, run the experiment, update the hypothesis.
- Delta debugging: systematically minimize the input (or the difference between a passing and a failing case) to isolate the minimal change that triggers the failure.
- Cause-effect chains: trace backward from the observed failure to the earliest point in the execution where state diverged from correct. The cause is the earliest divergence that, if corrected, would prevent the failure.

**Transferable method steps:**

- Apply the scientific method: hypothesis, experiment, refutation. Do not assume the first plausible explanation is correct.
- Delta-debug the context: what is the minimal difference between a context that produces a correct output and one that produces the wrong output?
- Trace the cause-effect chain: from the wrong output, work backward through the agent's reasoning to find the earliest point where its state (understanding, plan, assumptions) diverged from correct. That divergence points to the missing or incorrect context.

### Agans: Nine Rules of Debugging

**Origin:** Primary. David J. Agans, *Debugging: The 9 Indispensable Rules* (AMACOM, 2002).

**Claims (the nine rules):**

1. Understand the system (read the manual before theorizing).
2. Make it fail (reproduce the problem consistently).
3. Quit thinking and look (observe the actual failure, don't theorize from assumptions).
4. Divide and conquer (binary search the problem space).
5. Change one thing at a time (isolate variables).
6. Keep an audit trail (document every step and result).
7. Check the plug (verify fundamental prerequisites).
8. Get a fresh view (seek external perspectives).
9. If you didn't fix it, it ain't fixed (prove the fix works by cycling broken-to-fixed).

**Transferable method steps:**

- Rule 1 maps directly: understand the skill before theorizing about the failure.
- Rule 2: reproduce the failure with the same context.
- Rule 3: read the actual agent output and trace, don't theorize from the symptom.
- Rule 5: change one context element at a time to isolate which one matters.
- Rule 9: after modifying a skill, verify the fix by re-running the failing case *and* checking that previously passing cases still pass.

### Counterfactual/Actual Causation: Pearl, Halpern-Pearl

**Origin:** Primary. Judea Pearl, *Causality: Models, Reasoning and Inference* (2nd ed., Cambridge University Press, 2009). Halpern and Pearl, "Causes and Explanations: A Structural-Model Approach," *British Journal for the Philosophy of Science*, 2005.

**Claims:**

- An actual cause of an event is a minimal set of conditions such that, had those conditions been different (the counterfactual intervention), the event would not have occurred, while holding other conditions fixed.
- Structural equation models formalize counterfactual reasoning: define the variables, their functional relationships, and test which interventions change the outcome.
- The "but-for" test: event A is a cause of event B if, but for A, B would not have occurred.

**Transferable method steps:**

- For a wrong agent output, ask the counterfactual: "but for this specific context element (or its absence), would the output have been wrong?" If the answer is no, that element is an actual cause.
- Minimality: the cause is the smallest set of context changes that would flip the output from wrong to right. This prevents over-broad remediation.
- This maps directly to "what missing or incorrect context produced this output" -- the counterfactual identifies the specific context deficiency.

## III. LLM-Agent Failure Analysis (2024-2026)

### "Why Do Multi-Agent LLM Systems Fail?" -- MAST Taxonomy

**Origin:** Primary. Mehta et al., arXiv:2503.13657, March 2025. Accepted at a major venue (OpenReview).

**Claims:**

- First multi-agent system failure taxonomy (MAST): 14 failure modes in 3 categories: (i) system design issues, (ii) inter-agent misalignment, (iii) task verification.
- MAST-Data: 1600+ annotated traces across 7 MAS frameworks.
- "Many failures stem from poor system design, not model performance. Agents operate with incorrect assumptions, ignore peer input, or fail to verify their outputs."
- An LLM-as-a-Judge pipeline achieves 94% accuracy and 0.77 Cohen's kappa against expert annotations.

**Transferable insight:**

- The majority of multi-agent failures are system design issues, not model capability issues. This directly supports the spirit principle: "An agent is a machine; it does not misbehave."

### AgentDebug / AgentErrorTaxonomy

**Origin:** Primary. "Where LLM Agents Fail and How They Can Learn From Failures," arXiv:2509.25370, September 2025 (ICLR 2025 submission, OpenReview).

**Claims:**

- AgentErrorTaxonomy: 17 error types across 5 modules (memory, reflection, planning, action, system-level).
- A single root-cause error propagates through subsequent decisions (cascading failure). Isolating the root-cause step, not the visible symptom, is essential.
- AgentDebug: a two-stage pipeline that (a) isolates the root-cause failure step and (b) generates targeted corrective feedback.
- Targeted feedback from AgentDebug yields up to 26% relative improvement in task success.

**Transferable method steps:**

- Distinguish root-cause steps from cascade steps in the agent's trace. The fix belongs at the root-cause step.
- Targeted feedback (correcting the specific deficiency) outperforms generic retry or broad re-prompting.

### TRAIL: Trace Reasoning and Agentic Issue Localization

**Origin:** Primary. arXiv:2505.08638, May 2025.

**Claims:**

- 148 human-annotated traces with a formal taxonomy of agentic error types, grounded in established benchmarks.
- Even the best models (Gemini 2.5 Pro) score only 11% on TRAIL, indicating that automated trace debugging is far from solved.
- Traces from both single and multi-agent systems, focusing on real-world applications.

**Transferable insight:**

- Automated failure localization in agent traces is extremely difficult; the method must not rely on the agent itself to identify its own failure cause without structured support.

### TraceElephant: Full-Trace Failure Attribution

**Origin:** Primary. "Seeing the Whole Elephant," arXiv:2604.22708, April 2026.

**Claims:**

- Full execution traces (including inputs and context, not just outputs) improve failure attribution accuracy by up to 76% over partial-observation approaches.
- "Missing inputs obscure many failure causes."

**Transferable method step:**

- The full context the agent received must be examined, not just its output. Attributing failure from output alone misses the cause in the majority of cases.

### CausalFlow: Causal Attribution and Counterfactual Repair

**Origin:** Primary. arXiv:2605.25338, May 2026.

**Claims:**

- Treats execution traces as sequential chains of dependent steps.
- Computes Causal Responsibility Scores (CRS) via step-level counterfactual intervention to identify failure-inducing steps.
- Generates "minimally edited repairs that flip the final outcome to success" -- counterfactual repair.
- "Causal attribution is necessary for reliable improvement across diverse agent tasks" -- heuristic refinement alone is insufficient.

**Transferable method steps:**

- Counterfactual intervention at the step level: for each step, ask "if this step had been different, would the outcome have changed?" The steps with highest causal responsibility are the causes.
- Minimal repair: change only what is necessary. This is the counterfactual minimality principle applied to remediation.

### Anthropic: Building Effective Agents

**Origin:** Primary. Anthropic engineering blog, "Building effective agents," December 2024.

**Claims:**

- The most successful implementations use simple, composable patterns, not complex frameworks.
- Tool optimization matters more than prompt optimization: "We spent more time optimizing tools than the overall prompt."
- "Poka-yoke your tools" -- change parameters and interfaces to make mistakes structurally impossible, rather than adding instructions not to make them.
- When agents made mistakes (e.g., using relative vs. absolute filepaths), the fix was to change the tool interface (require absolute paths), not to add a prompt instruction.

**Transferable method steps:**

- When an agent repeatedly makes a class of error, change the interface or context structure to make the error impossible, rather than adding a rule telling it not to.
- Simplicity is a safety property: complexity creates latent conditions.

## IV. Remediation: Turning Diagnosis into Durable Fix

### Fixing at the Right Level

**Grounding sources:** Leveson (control structure improvements), Dekker (organizational remediation), Google SRE (systemic fixes), Anthropic (poka-yoke).

**Converging principle:** The fix belongs at the level where the cause originates. If the cause is missing context, the fix is in the context assembly. If the cause is an ambiguous skill rule, the fix is in the skill. If the cause is a missing feedback channel, the fix is in the control structure. Patching the individual output addresses none of these.

### Action Items That Stick

**Grounding sources:** Google SRE Chapter 15, incident.io analysis of postmortem action item failure.

**Claims:**

- Action items fail when they have diffused ownership (assigned to a team, not a person), vague framing ("improve X" rather than "add/remove/change X"), disconnection from the workflow where they'd be executed, and no follow-up cadence.
- Effective action items: named owner, outcome-oriented verb, measurable deliverable, explicit deadline, integration into existing task tracking.
- Verification: publicize when a fix prevents a recurrence, so the feedback loop closes.

### Failure Modes of Remediation Itself

**Grounding sources:** Dekker (procedural drift), Rasmussen (drift toward boundaries), Turner (via Dekker), research on railway worker rule perception (ScienceDirect, 2020).

**Claims:**

- **Over-correction / rule accretion:** Each incident adds a rule; rules accumulate into a body that practitioners cannot follow. 95% of railway workers in one study believed work couldn't be completed on time if all rules were followed. 80% believed rules mainly concerned assigning blame.
- **Procedure fetish:** Tasks are done to be auditable rather than useful, creating "a system of checks consistent only with itself and less connected to how risk actually builds up."
- **Drift from relevance:** The organization's "administratively constructed picture of the world" slowly drifts away from frontline reality (Turner, via Dekker).
- **Symptom-fixing:** Fixing the visible output rather than the cause, leading to whack-a-mole remediation that never converges.

**Transferable method steps:**

- Every rule addition must be justified against the cause it addresses. A rule that does not address an identified cause is accretion.
- Prefer structural changes (interface changes, context assembly changes) over behavioral instructions (rules telling the agent what not to do).
- After adding a rule, check: does the total rule set remain followable? Does each rule still address an active cause?
- Regression verification: the fix must be testable. A fix that cannot be verified as effective is not a fix.

## V. Candidate Method: Steps for Diagnosing Agent Failure at Source

When an agent output is identified as wrong, an agent following this method would execute these steps:

### Step 1: Record the failure without attributing cause

Capture the wrong output, the context the agent received, and the expected output. Do not hypothesize yet.

*Grounding:* Zeller (scientific method: observe before hypothesizing), Dekker (avoid hindsight bias), Spirit ("keep observations, hypotheses, and unknowns separate").

### Step 2: Reconstruct the agent's local rationality

Given the context the agent had, was the output rational? Read the actual trace, not a summary. Ask: "given what the agent knew, does its output make sense?"

*Grounding:* Dekker (local rationality), Allspaw (ask "how," not "why"), Agans (Rule 3: quit thinking and look), TraceElephant (full traces improve attribution by 76%).

**If the output was rational given the context:** the cause is in the context (missing, incorrect, or ambiguous information in the prompt/skill/context assembly). Proceed to Step 3a.

**If the output was irrational given the context:** the cause may be a model capability limit or a context that was present but not attended to. Proceed to Step 3b.

### Step 3a: Identify the context deficiency (counterfactual)

Ask: "What context, if added or corrected, would have produced the right output?" This is the Halpern-Pearl counterfactual: the cause is the minimal context change that flips the output from wrong to right.

*Grounding:* Halpern-Pearl (actual causation, minimality), CausalFlow (counterfactual intervention), Zeller (delta debugging -- minimize the difference between passing and failing cases), Spirit ("determine the lacking or incorrect context which produced it").

### Step 3b: Investigate model-context interaction

If the context was adequate but the output was wrong, investigate: was the context too long, ambiguous, or contradictory? Was a relevant instruction buried or competing with another? Is this a known model limitation?

*Grounding:* MAST (system design issues category), Reason (latent conditions), Hollnagel (performance variability under varying conditions).

**Note:** Sources disagree here on whether this case exists meaningfully for well-prompted agents. Leveson, Dekker, and the spirit principle all hold that the agent's behavior is a function of its context; MAST and AgentDebug show empirically that the vast majority of failures trace to system design, not model capability. Step 3b should be reached rarely; if it is reached frequently, that itself indicates a control structure flaw (the skills are not governing effectively).

### Step 4: Trace the cause to its origin in the control structure

The context deficiency identified in Step 3a has a source: a skill rule that is missing, ambiguous, or incorrect; a context assembly step that drops or distorts information; a feedback channel that does not exist. Model the control structure (Leveson CAST Step 2) and identify which controller failed and why.

*Grounding:* Leveson CAST (model the control structure, identify flaws at each level), Reason (latent conditions at the blunt end), Google SRE ("investigate the systematic reasons why... incomplete or incorrect information").

### Step 5: Design a minimal structural fix at the origin

Fix the cause at its source: modify the skill, repair the context assembly, add the missing feedback channel. The fix should be:

- **Minimal:** change only what is necessary to address the identified cause (Halpern-Pearl minimality, CausalFlow minimal repair).
- **Structural, not behavioral:** prefer changing the interface to make the error impossible over adding a rule telling the agent not to make it (Anthropic poka-yoke, Leveson control structure improvement).
- **Specific and verifiable:** the fix must have a named owner, a concrete change, and a test that demonstrates it works (Google SRE action items, Agans Rule 9).

*Grounding:* Anthropic (poka-yoke), Leveson CAST Step 5 (recommendations as control structure improvements), CausalFlow (minimal repair), Agans Rule 9 (if you didn't fix it, it ain't fixed).

### Step 6: Verify the fix and check for over-correction

- Re-run the failing case with the fix applied. Confirm the output is now correct.
- Re-run previously passing cases. Confirm they still pass.
- Review the total rule/skill set: does the fix add accretion? Does it create a contradictory or unfollowable instruction set?

*Grounding:* Agans Rule 9 (verify), Dekker/Turner (procedure accretion), Rasmussen (drift), Hollnagel Safety-II (both success and failure arise from the same variability).

### Step 7: Record what was found and what was changed

Document: the wrong output, the context deficiency, the control structure flaw, the fix applied, and the verification result. This is the audit trail that prevents repeated investigation of the same class of failure.

*Grounding:* Agans Rule 6 (keep an audit trail), Google SRE (postmortem documentation), Spirit ("keep observations, hypotheses, and unknowns separate").

## VI. Where Sources Disagree

**On whether "root cause" is a useful concept:** Allspaw and Dekker reject it entirely as a constructed artifact. Leveson rejects single-cause framing but uses multi-causal analysis. Zeller's delta debugging and Halpern-Pearl's actual causation provide formal methods for identifying minimal causes, which function as rigorous replacements for the informal "root cause" concept. AgentDebug uses the term "root-cause failure" to mean the earliest failure step in a cascade, which is closer to Zeller than to traditional root cause analysis. *Inference:* The term "root cause" should be avoided; "origin of the context deficiency" or "earliest contributing condition" is more precise.

**On the role of the individual actor vs. the system:** Safety science (Leveson, Dekker, Hollnagel, Reason) unanimously holds that the system, not the individual, is the appropriate target of remediation. In an agent system, the "individual" is the agent instance and the "system" is the skill/context architecture. The LLM-agent literature (MAST, AgentDebug, CausalFlow) arrives at the same conclusion from a different direction: failures are system design issues, not model capability issues. *No disagreement here across sources.*

**On automated vs. human diagnosis:** TRAIL shows that even the best current models score 11% on trace debugging tasks, suggesting automated failure localization is far from reliable. CausalFlow and AgentDebug show that structured methods can improve this significantly. *Inference:* The method should be structured enough that an agent can follow it, but should not rely on the agent to freely diagnose its own failure without the structure.

**On structural vs. behavioral fixes:** Anthropic strongly favors structural changes (poka-yoke). Safety science favors control structure improvements. Neither advocates adding behavioral rules as a primary remediation strategy, though both acknowledge that some rules are necessary. The rule-accretion literature warns that behavioral rules are the path of least resistance and tend to accumulate without bound. *Inference:* Prefer structural fixes; use behavioral rules only when the structure cannot be changed, and sunset rules when the structure is later improved.

## Sources

### Books and Primary Papers

- Leveson, Nancy G. *Engineering a Safer World: Systems Thinking Applied to Safety.* MIT Press, 2011. Open access: https://direct.mit.edu/books/oa-monograph/2908/Engineering-a-Safer-WorldSystems-Thinking-Applied
- Leveson, Nancy G. *CAST Handbook.* MIT. http://sunnyday.mit.edu/CAST-Handbook.pdf
- Dekker, Sidney. *The Field Guide to Understanding 'Human Error'.* 3rd ed. Routledge, 2014. https://www.routledge.com/The-Field-Guide-to-Understanding-Human-Error/Dekker/p/book/9781472439055
- Hollnagel, Erik. *Safety-I and Safety-II: The Past and Future of Safety Management.* Ashgate, 2014.
- Hollnagel, Erik, David Woods, and Nancy Leveson, eds. *Resilience Engineering: Concepts and Precepts.* Ashgate, 2006.
- Reason, James. *Managing the Risks of Organizational Accidents.* Ashgate, 1997.
- Rasmussen, Jens. "Risk management in a dynamic society: A modelling problem." *Safety Science* 27(2-3), 1997.
- Zeller, Andreas. *Why Programs Fail: A Guide to Systematic Debugging.* 2nd ed. Morgan Kaufmann, 2009.
- Agans, David J. *Debugging: The 9 Indispensable Rules for Finding Even the Most Elusive Software and Hardware Problems.* AMACOM, 2002.
- Pearl, Judea. *Causality: Models, Reasoning and Inference.* 2nd ed. Cambridge University Press, 2009.
- Halpern, Joseph Y. and Judea Pearl. "Causes and Explanations: A Structural-Model Approach." *British Journal for the Philosophy of Science*, 2005.
- Beyer, Betsy et al. *Site Reliability Engineering.* O'Reilly, 2016. Chapter 15: https://sre.google/sre-book/postmortem-culture/

### Blog Posts and Online Primary Sources

- Allspaw, John. "The Infinite Hows (or, the Dangers of the Five Whys)." Kitchen Soap, 2014. https://www.kitchensoap.com/2014/11/14/the-infinite-hows-or-the-dangers-of-the-five-whys/
- Anthropic. "Building effective agents." Anthropic engineering blog, December 2024. https://www.anthropic.com/engineering/building-effective-agents
- incident.io. "Why Do Post-Mortem Action Items Fail?" https://incident.io/blog/why-do-post-mortem-action-items-fail-how-to-make-incident-follow-ups-actually-get-done

### LLM-Agent Failure Research (2024-2026)

- Mehta et al. "Why Do Multi-Agent LLM Systems Fail?" arXiv:2503.13657, March 2025. https://arxiv.org/abs/2503.13657
- "Where LLM Agents Fail and How They Can Learn From Failures" (AgentDebug / AgentErrorTaxonomy). arXiv:2509.25370, September 2025. https://arxiv.org/abs/2509.25370
- "TRAIL: Trace Reasoning and Agentic Issue Localization." arXiv:2505.08638, May 2025. https://arxiv.org/abs/2505.08638
- "Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems" (TraceElephant). arXiv:2604.22708, April 2026. https://arxiv.org/abs/2604.22708
- "CausalFlow: Causal Attribution and Counterfactual Repair for LLM Agent Failures." arXiv:2605.25338, May 2026. https://arxiv.org/abs/2605.25338
- "Who is Introducing the Failure? Automatically Attributing Failures of Multi-Agent Systems via Spectrum Analysis." arXiv:2509.13782, September 2025. https://arxiv.org/abs/2509.13782

### Rule Accretion and Remediation Failure Modes

- "How deregulation can become overregulation." *Safety Science*, 2020. https://www.sciencedirect.com/science/article/pii/S0925753520301697
- Joel Parker Henderson. CAST summary. https://github.com/joelparkerhenderson/causal-analysis-based-on-system-theory
- Embedded Artistry. Agans' nine rules summary. https://embeddedartistry.com/blog/2017/09/06/debugging-9-indispensable-rules/

### Safety Science Overviews (Secondary, Used for Context Only)

- "Safety-II and Resilience Engineering in a Nutshell." *Safety Science*, 2020. https://www.sciencedirect.com/science/article/pii/S2093791120303619
- PSNet/AHRQ. "Safety I, Safety II, and the New Views of Safety." https://psnet.ahrq.gov/primer/safety-i-safety-ii-and-new-views-safety
- UL SIS. "Understanding STAMP, STPA, and CAST." https://www.ul.com/sis/blog/introduction-to-stamp-stpa-and-cast
