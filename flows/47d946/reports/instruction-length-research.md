# Instruction length and adherence: bounded research

Research date: 2026-10-14. Scope: primary empirical papers and first-party
provider documentation relevant to context modules and loaded skills. The
evidence does not support a universal ideal module size in words or tokens.

## Findings

### 1. Input capacity is a budget, not an adherence guarantee

OpenAI's API documentation treats the context window as a limit shared by
input and possible output. Its truncation documentation gives a concrete
example: with a 32k context model and 4,096 maximum output tokens, only
28,224 tokens remain for context before truncation. It also documents that
truncation can remove the oldest messages. This is a product constraint, not
a measured rule that a module of any particular size is optimal.

Source: [OpenAI Realtime client session reference](https://platform.openai.com/docs/api-reference/realtime-beta-server-events/session/update#realtime-session-object-truncation),
accessed 2026-10-14. The documentation is current product behavior guidance,
not a controlled adherence experiment.

### 2. Multiple constraints and composition predict failure better than raw words

Wen et al., *ComplexBench* (NeurIPS 2024 Datasets and Benchmarks Track;
arXiv v1 2024-07-04, v3 2024-10-31), evaluated 15 models from 6B to 72B,
including GPT-4-1106 and Claude-3-Opus. The benchmark combines four constraint
types, 19 constraint dimensions, and four composition types (including
simultaneous, chained, and conditional constraints), with rule and model-based
checking. The paper reports that GPT-4-1106's aggregate score over its
scoring questions was 0.800 and that performance fell as composition became
more complex. For nested multi-layer Selection, GPT-4 reached only 14.9% in
the coherent test. These are constraint-composition results, not module-length
results: the paper does not vary a module's word/token length while holding
the number and type of constraints constant. The aggregate score should not
be converted into a percentage of failed instructions.

Source: [ComplexBench paper](https://arxiv.org/abs/2407.03978), especially
the [full HTML results](https://arxiv.org/html/2407.03978v3), accessed
2026-10-14. Model versions, generation cap, and scores are reported in the
paper's evaluation section and Table 5.

Chen et al., *SIFo* (EMNLP 2024 Findings; arXiv v1 2024-06-28, v2
2024-10-03), evaluated GPT-4 (gpt-4-0613), Claude-3 Opus, and open models on
800 objectively checked examples across four tasks. Each sequence contained
2–6 dependent steps; average instruction length was 12.9–24.6 tokens and
average context length 35.8–68.2 tokens depending on task. Every evaluated
model's step-level performance declined as sequence position increased, with
the decline beginning at the second step. Their separate six-constraint
permutation probe (20 samples × 6! orders) found that order changed adherence,
but the best position pattern differed by model and constraint type.

This supports tracking the number, dependency, and placement of requirements.
It does not justify a 20-token or 70-token module limit: those were benchmark
descriptives, not an optimization sweep, and the contexts were short.

Source: [SIFo paper](https://arxiv.org/abs/2406.19999), with methods and
results in the [full HTML](https://arxiv.org/html/2406.19999v2), accessed
2026-10-14.

### 3. Output-length adherence is a separate variable from input length

Zhang et al., *LIFEBench* (arXiv v1 2025-05-22, v2 2025-06-11), evaluated 26
models on 10,800 English and Chinese instances with requested output lengths
from 16 to 8,192 words, and extended tests to 32k words. Most models were
reasonable on short requests but deteriorated sharply beyond a model/task
dependent point. Under the paper's Equal-To control, 23 of 26 models scored
below 60; under At-Least, 18 of 26 scored below 40 at 8,192 words. Long input
and output windows did not by themselves improve length adherence. This is
evidence about output constraints and generation behavior, not about the
ideal size of an instruction module.

Source: [LIFEBench paper](https://arxiv.org/abs/2505.16234), with protocol
and results in the [full HTML](https://arxiv.org/html/2505.16234v2), accessed
2026-10-14.

### 4. Position and structure guidance exists, but provider guidance is not a universal law

Anthropic's current prompting guide recommends putting long-form data near
the top, with the query after it, and reports up to 30% improvement in its
tests for queries at the end in complex multi-document inputs. It also
recommends explicit structure (for example, XML tags separating instructions,
context, and inputs) and sequential lists when order/completeness matter.
This is useful operational guidance for arranging loaded context, but the
page does not specify a universal module size, publish the test protocol in
the cited section, or establish that the same placement effect applies to
skills/modules across models.

Source: [Anthropic long-context prompting guidance](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables#long-context-prompting),
accessed 2026-10-14. The guide currently describes multiple Claude model
families; its recommendations should be treated as provider guidance tied to
their tests, not as cross-provider causal evidence.

### 5. Agent Skills authoring guidance gives a line bound, not an empirically optimal token bound

Anthropic's public Agent Skills platform overview gives an explicit Level 2
token-cost description: the `SKILL.md` body is loaded when triggered and costs
"Under 5k tokens." It also gives Level 1 metadata as approximately 100 tokens
per Skill and Level 3+ resources as having no cost until accessed. Separately,
Anthropic's authoring material recommends keeping the `SKILL.md` body under
500 lines and moving detailed material into referenced files. These are
documented loading/budget and authoring recommendations, not controlled
experiments establishing that 5,000 tokens or 500 lines maximizes adherence.
The overview's "Under 5k tokens" is a descriptive Level 2 budget target for
the platform's progressive-disclosure architecture; it is not a measured
cross-model optimum. Line length and content density vary, so 500 lines cannot
be converted reliably to a token threshold.

Source: [Anthropic Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
(Level 1–3 token-cost table) and the [Anthropic-maintained skill-creator guide](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md),
accessed 2026-10-14. The GitHub guide states the under-500-line recommendation
and the platform overview states the Level 2 "Under 5k tokens" budget.

### 6. Instruction hierarchy is a distinct axis

Wallace et al., *The Instruction Hierarchy* (arXiv v1 2024-04-19), trained
models to prioritize system over user over third-party instructions and
evaluated prompt-injection robustness and over-refusal. Their setup
decomposed compositional requests into smaller instruction pieces and placed
them at different privilege levels. The reported trained model improved
robustness by up to 63% on the main attack evaluations and generalized by up
to 34% on held-out evaluations. This demonstrates that role/privilege and
conflict structure can dominate raw prompt length; it does not measure module
size or prove that splitting instructions improves ordinary adherence.

Source: [The Instruction Hierarchy](https://arxiv.org/abs/2404.13208),
accessed 2026-10-14. The paper is a training/evaluation study, not a
provider authoring guide.

## What can safely be carried into context-module design

The evidence supports treating these as separate measurements:

* **Context-window budget:** total serialized input plus reserved output and
  tool/schema overhead; exceeding it can trigger truncation or rejection.
* **Individual module size:** words/tokens in one authored module. No source
  located here establishes a universal optimum.
* **Cumulative loaded instruction size:** the sum of all system/developer
  instructions and loaded modules. It consumes budget and may increase the
  number of requirements the model must track, but the reviewed studies do
  not isolate this variable from task content.
* **Constraint load:** number, type, composition, and dependency of
  requirements. ComplexBench and SIFo directly measure this and find
  degradation even with short inputs.
* **Placement/position:** location in the prompt or sequence. SIFo's
  permutation probe and its sequential results show model- and task-specific
  position effects. Retrieval studies such as “Lost in the Middle” should not
  be converted into universal module-splitting thresholds: they test finding
  information, not authored skill adherence.
* **Output length:** requested or maximum response length. LIFEBench shows
  this has its own failure curve and should not be used as a proxy for input
  instruction capacity.

Practical implication supported by these boundaries: measure module tokens and
cumulative loaded tokens for budget safety; keep each requirement explicit and
auditable; count constraints and dependencies; and test placement and adherence
on the actual model/task mix. Treat a split as a hypothesis to test, not as a
research-established token threshold.

## Open inquiries

1. For a fixed model and task family, how does adherence change when the same
   requirements are serialized as one module versus several modules, with
   total tokens, order, privilege, and examples held constant?
2. Does cumulative instruction length have an independent effect after holding
   constraint count, semantic complexity, output length, and context position
   constant?
3. What is the interaction between module boundaries/labels and instruction
   hierarchy? Existing evidence supports structure and privilege separately,
   but not their joint optimum.
4. How do results differ across current Claude/Codex model versions and their
   actual skill-loading mechanisms? The reviewed papers mostly use 2023–2024
   model versions, while provider documentation is guidance rather than an
   independently reproducible benchmark.
5. Which metric should govern a module: per-constraint pass rate, all-
   constraints pass rate, sequential depth, task success, or budget/cost?
   ComplexBench and SIFo show that these metrics can disagree.

## Evidence boundary

No reviewed primary source supports a universal ideal context-module size in
words or tokens. The strongest defensible claim is conditional: module size is
bounded by the model's available context budget, while adherence depends on
constraint count/composition, position, hierarchy, task, and output demands;
the useful threshold must be established by controlled tests on the target
model and workload.

## Direct long-input instruction-following evidence

Two additional benchmarks directly vary long input context while measuring
instruction-following. They narrow the evidence gap, but neither varies the
length of an isolated authored skill/module while holding all other factors
constant.

* **LIFBench — Wu et al., arXiv v1 2024-11-11, v3 2025-07-23.**
  [Paper and full text](https://arxiv.org/abs/2411.07037)
  ([HTML](https://arxiv.org/html/2411.07037v3)). It evaluates 20 models on
  2,766 examples across 11 tasks and three long-context scenarios. The
  instruction is deliberately kept short and placed at the end; the varied
  input is the context body, controlled from 4K through 128K tokens (the
  corpus can extend to 2M). Most models' instruction-following scores decline
  significantly as context grows, particularly beyond 16K–32K tokens, though
  the curve is model/task dependent. GPT-4o's overall score across the six
  intervals was 0.776 at 4K, 0.807 at 8K, 0.801 at 16K, 0.779 at 32K, 0.721
  at 64K, and 0.666 at 128K. The authors use automatic rubric scoring and
  task-specific output caps; some longest inputs were right-truncated for
  models that could not fit them. This is strong evidence about cumulative
  long-context input and adherence, not an optimum for the instruction body.

* **LongIns — Gavin et al., arXiv v1 2024-06-25, v3 2025-08-13.**
  [Paper and full text](https://arxiv.org/abs/2406.17588)
  ([HTML](https://arxiv.org/html/2406.17588v3)). It constructs GIST, LIST,
  and LIMT exams from concatenated instruction questions at seven total
  context lengths: 256, 512, 1,024, 2,048, 4,096, 8,192, and 16,384 tokens,
  with controlled incorrect-answer density. GPT-4o accuracy in the global
  single-task setting fell from 76.31 at 256 tokens to 51.15 at 16,384;
  GPT-4-Turbo fell from 73.89 to 44.22. Models were more sensitive to the
  number/density of questions even when total test-paper length was held
  constant. The authors state that GPT-4-class models were challenged by
  16K, despite advertised 128K context. Limitations: synthetic concatenated
  data, and the task is detecting incorrect answers rather than general skill
  execution. It therefore measures long-context instruction processing, not
  standalone skill-file length.

Together these studies support a model/workload-specific long-context test at
4K, 8K, 16K, 32K, 64K, and 128K where feasible. They do not support selecting
one universal module boundary, and they leave a direct experiment on isolated
module length as an open inquiry.
