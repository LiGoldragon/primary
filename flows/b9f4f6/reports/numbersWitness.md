# Witness: Six Numbers from Research Claims

Flow b9f4f6, dispatched to verify six claims relayed to the psyche from parent research subflows.

## Method

For each claim, fetched the paper's arXiv abstract page and (where needed) the full HTML text at arxiv.org/html/. Located the verbatim sentence carrying the number, identified the quantity it measures, and compared against the relayed claim. For the sixth claim (maker-checker, "sourced from fork"), conducted extensive arXiv searches to locate the primary source.

---

## 1. arXiv 2512.08296: "+80.8% on decomposable financial reasoning to -70.0% on sequential planning"

**Claimed:** The claim "+80.8% on decomposable financial reasoning to -70.0% on sequential planning". What is -70.0% a change of? Relative to what? On which task? Also: does the paper give a cause for the sequential-planning loss?

**Verbatim sentence from paper:**
"Relative performance change compared to single-agent baseline ranges from **+80.8% on decomposable financial reasoning to −70.0% on sequential planning**" (arXiv abstract, https://arxiv.org/abs/2512.08296)

**What it measures:** 
- **+80.8%**: Performance improvement of centralized multi-agent systems on Finance Agent tasks, measured as success rate relative to single-agent baseline (0.631 vs. 0.349).
- **-70.0%**: Performance degradation of independent multi-agent architecture on PlanCraft sequential planning tasks, measured as success rate relative to single-agent baseline (0.170 vs. 0.568).

**Cause given in paper:**
The paper identifies multiple causes via mechanistic analysis in the full text (https://arxiv.org/html/2512.08296):
1. **Unnecessary task decomposition:** Sequential tasks require few direct steps but multi-agent systems fragment them into parallel subtasks.
2. **Token budget depletion:** Coordination overhead consumes reasoning capacity without improving task resolution.
3. **Lack of verification:** Independent architecture has no error correction, so individual mistakes propagate unchecked.
4. **Coordination overhead exceeds task complexity:** Verbatim: "coordination overhead becomes counterproductive when coordination complexity exceeds task complexity."

**Status: CONFIRMED verbatim** (exact numbers, exact quantity measured, cause documented).

---

## 2. arXiv 2606.05976: "self-correction median ~17%; relabelled as external memory +53.3 percentage points; role tag ~30 points"

**Claimed:** Self-correction of own errors median ~17%; relabelled as external memory median +53.3 percentage points; role tag alone ~30 points.

**Verbatim sentences from paper** (https://arxiv.org/html/2606.05976):
- Self-correction baseline: "The median L0_self correction rate across experiments is approximately **16.7%** on the Qwen-72B math failure pool."
- Relabelled as external memory: "The <memory> condition achieved a **+53.3 percentage point increase**, reaching 70.0% correction rate on the same pool."
- Role tag contribution: "the role tag itself contributed approximately **30 percentage points** beyond label-free syntactic boundaries."

**Status: DIFFERS SLIGHTLY** 
- Claimed "~17%" but paper reports 16.7%. The tilde (~) suggests approximation, so 16.7% rounds to 17%, but the paper is precise at 16.7%.
- +53.3 percentage points: CONFIRMED verbatim.
- ~30 percentage points for role tag: CONFIRMED verbatim (exact match).

---

## 3. arXiv 2604.11322: "irrelevant-tool invocation 41.9% aligned, 90.4% high alignment, <0.2% random"

**Claimed:** Irrelevant-tool invocation 41.9% when structurally aligned, 90.4% at high alignment, <0.2% random pairing.

**Verbatim sentences from paper** (https://arxiv.org/html/2604.11322):
- Structural alignment: "Tool invocation errors **rise sharply to 41.9%** when query attributes can be validly assigned to tool parameters, despite the tool being semantically irrelevant."
- High alignment degree: "The error rate escalates further to **90.4% as the alignment degree increases.**"
- Random pairing baseline: "The error rate remains **negligible (<0.2%)** when tools are randomly paired with queries."

**Status: CONFIRMED verbatim** (all three numbers exact, baseline and conditions clearly specified).

---

## 4. arXiv 2511.16660: "test-time guidance improves performance up to 66.7% on complex problems"

**Claimed:** Test-time guidance improves performance up to 66.7% on complex problems; models possess but fail to spontaneously deploy meta-cognitive controls.

**Verbatim sentence from paper** (https://arxiv.org/abs/2511.16660):
"Leveraging these patterns, we develop test-time reasoning guidance that automatically scaffold successful structures, **improving performance by up to 66.7% on complex problems.**"

**Models possess but fail to deploy:**
Verbatim: "Models possess behavioral repertoires associated with success but fail to deploy them spontaneously."

**Status: CONFIRMED verbatim** (exact number, exact task qualifier "complex problems", meta-cognitive control finding confirmed).

---

## 5. arXiv 2605.13414 (TRIAGE): "extended reasoning improves accuracy but does not improve metacognitive control; binding the budget breaks triage"

**Claimed:** Extended reasoning improves accuracy but does not improve metacognitive control; "binding the budget breaks triage."

**Verbatim sentences from paper** (https://arxiv.org/html/2605.13414):
- Extended reasoning effect: "Within the paired-mode models, base accuracy increases with extended reasoning on most (model, dataset) pairs... Extended reasoning leaves [metacognitive control] essentially unchanged or worsens it on roughly half of paired configurations."
- Further: "Object-level capability and metacognitive control thus dissociate empirically: a longer trace can solve more problems without making the planner any better at deciding which ones to attempt."

**"Binding the budget breaks triage" claim:**
Searched the full text for this phrase or synonymous claims. NOT FOUND in the abstract, methods, results, or conclusion sections reviewed. The paper discusses budget constraints and regret bounds (ηU, ηE) but does not use the phrase "binding the budget breaks triage" or make a claim equivalent to it.

**Status: DIFFERS**
- Extended reasoning improving accuracy: CONFIRMED.
- Not improving metacognitive control: CONFIRMED.
- "Binding the budget breaks triage" phrase or equivalent claim: NOT FOUND in paper.

---

## 6. Maker-checker claim (July 2026): "70% of production loops use deterministic verification rather than LLM-based review"

**Claimed:** Self-approval causes grade drift without quality gain; 70% of production loops use deterministic verification rather than LLM-based review.

**Search method:**
- Searched arXiv for "maker-checker", "maker checker", "self-approval", "grade drift", "deterministic verification production", "production loops verification"
- Searched for papers from July 2026 and surrounding months (June–August 2026)
- Searched for combinations of terms: "70% deterministic", "production loops", "LLM review vs deterministic"
- Reviewed papers that appeared in results (SkillEvo, The Kitchen Loop, Pramana, MedSci Skills, SPL Language, etc.) for the exact claim

**Results:**
- Found multiple 2026 papers addressing verification and production systems (arXiv 2607.19795, 2605.20312, 2605.14675, 2608.13120, 2603.25697, 2606.09500, 2607.07727, 2602.15485)
- Found papers comparing LLM-based vs. deterministic verification in production (MedSci Skills showed deterministic outperforming LLM)
- Did NOT find a paper with the specific claim: "70% of production loops use deterministic verification rather than LLM-based review"
- Did NOT find a paper citing "self-approval causes grade drift without quality gain" in this context

**Status: NOT FOUND**
No primary source located for this claim despite extensive searches. The report marked it "[Sourced from fork]" with no URL, and no arXiv paper matching this exact claim could be identified.

---

## Summary Table

| # | Paper | Claim | Status | Notes |
|---|-------|-------|--------|-------|
| 1 | arXiv 2512.08296 | +80.8% / -70.0% | CONFIRMED | Verbatim with cause (coordination overhead, task decomposition, token budget, error propagation) |
| 2 | arXiv 2606.05976 | ~17% / +53.3pp / ~30pp | DIFFERS (slightly) | Paper: 16.7% (not 17%); other numbers exact |
| 3 | arXiv 2604.11322 | 41.9% / 90.4% / <0.2% | CONFIRMED | All three numbers verbatim, baseline and conditions clear |
| 4 | arXiv 2511.16660 | 66.7% complex problems | CONFIRMED | Verbatim; meta-cognitive control claim confirmed |
| 5 | arXiv 2605.13414 | Extended reasoning / metacognition / "binding breaks triage" | DIFFERS | First two claims confirmed; "binding the budget breaks triage" phrase not found in paper |
| 6 | Maker-checker (July 2026) | 70% deterministic verification | NOT FOUND | No primary source located despite extensive arXiv searches |

---

## Sources

1. arXiv 2512.08296: https://arxiv.org/abs/2512.08296 and https://arxiv.org/html/2512.08296
2. arXiv 2606.05976: https://arxiv.org/abs/2606.05976 and https://arxiv.org/html/2606.05976
3. arXiv 2604.11322: https://arxiv.org/abs/2604.11322 and https://arxiv.org/html/2604.11322
4. arXiv 2511.16660: https://arxiv.org/abs/2511.16660
5. arXiv 2605.13414: https://arxiv.org/abs/2605.13414 and https://arxiv.org/html/2605.13414
6. Maker-checker (July 2026): No primary source found; reported as "[Sourced from fork]" in flow composition ontologies report
