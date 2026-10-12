# Research: forcing an answer from the pieces at hand instead of noticing what is missing

Web research, 2026-10-12, flow 33752b. Question: what has been published, built or written about the failure where a model forces an answer together from the pieces it has instead of noticing which pieces are missing and asking; and about the remedies (list unknowns before acting, ask clarifying questions, abstain, check the design against a model of the whole).

Verification status. Every quote marked *verified* was read at the source URL (arXiv abstract page, ACL Anthology page, publisher page, raw repository file, or the author's page) during this research. Items marked *unverified* rest on search-engine summaries or secondary citations only; the source page was not read. Years and venues are as the source states them.

## The best twelve

### 1. Kalai, Nachum, Vempala, Zhang (OpenAI / Georgia Tech) — "Why Language Models Hallucinate" (2025)

URL: https://arxiv.org/abs/2509.04664 (companion post: https://openai.com/index/why-language-models-hallucinate/, not read; returned 403)

Idea, verbatim (verified, arXiv abstract): training and evaluation procedures "reward guessing over acknowledging uncertainty"; "language models are optimized to be good test-takers".

What they built: a statistical account. Hallucinations are errors of binary classification (is this a valid output?), and the pressure to guess comes from benchmarks that score a wrong answer and an "I don't know" identically. The fix proposed is not another hallucination benchmark but changing "the scoring of existing benchmarks" so that abstention is not penalised below a wrong guess; the abstract calls this a "socio-technical mitigation".

Measured result: none in the abstract; the paper is analytical. The birthday example (guessing a date wins 1/365 of the time; "I don't know" wins never) is from the blog post as relayed by search, unverified.

### 2. Kirichenko, Ibrahim, Chaudhuri, Bell (Meta FAIR) — "AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions" (2025)

URL: https://arxiv.org/abs/2506.09038 (code: github.com/facebookresearch/AbstentionBench, unverified)

Idea, verbatim (verified): "abstention is an unsolved problem, and one where scaling models is of little use"; "reasoning fine-tuning degrades abstention"; "a carefully crafted system prompt can boost abstention in practice".

What they built: a benchmark of 20 datasets covering unknown answers, underspecification, false premises, subjective questions and outdated information, scoring whether a model declines when it should.

Measured result: reasoning fine-tuning degrades abstention by 24% on average (verified, abstract), including in the math and science domains the reasoning models are trained on. A system prompt helps but "does not resolve models' fundamental inability to reason about uncertainty" (verified paraphrase of abstract).

### 3. Wen, Yao, Feng, Xu, Tsvetkov, Howe, Wang (U. Washington / AI2) — "Know Your Limits: A Survey of Abstention in Large Language Models" (TACL 2024)

URL: https://arxiv.org/abs/2407.18418

Idea, verbatim (verified): "Abstention, the refusal of large language models (LLMs) to provide an answer"; the authors "introduce a framework to examine abstention from three perspectives: the query, the model, and human values".

What they built: a survey and taxonomy; metrics such as Abstain-ECE (expected calibration error with abstention) and Coverage@Acc (fraction answered while holding a target accuracy). The affiliation is from search summaries, unverified; the author list is verified.

Measured result: none (survey).

### 4. Zhang, Diao, Lin, Fung, Lian, Wang, Chen, Ji, Zhang — "R-Tuning: Instructing Large Language Models to Say 'I Don't Know'" (NAACL 2024)

URL: https://arxiv.org/abs/2311.09677

Idea, verbatim (verified): instruction tuning makes models complete every answer; the paper targets "the propensity for these models to generate non-existent facts" and trains them to "refrain from responding to questions beyond its parametric knowledge".

What they built: Refusal-Aware Instruction Tuning. Compare what the base model actually knows with what the instruction data asks; label the gap as "I don't know"; fine-tune on that.

Measured result: R-Tuning "effectively improves a model's ability to answer known questions" and refuse unknown ones; refusal "was found to be a meta-skill that could be generalized to other tasks" (verified). Numeric figures are in the paper body, not read.

### 5. Mu, Shi, Wang, Yu, Zhang, Wang, Liu, Wang — "ClarifyGPT: Empowering LLM-based Code Generation with Intention Clarification" (2023; ESEC/FSE 2024)

URL: https://arxiv.org/abs/2310.10996

Idea, verbatim (verified): the framework gives the model the "ability to identify ambiguous requirements and ask targeted clarifying questions".

What they built: a three-step prompt pipeline. Detect ambiguity by sampling several code candidates and testing whether they agree (a code-consistency check); if they disagree, prompt the model to "generate targeted clarifying questions"; fold the answers into the requirement and regenerate. A simulated user stands in for the human during large-scale evaluation.

Measured result (verified): with ten human participants on MBPP-sanitized, GPT-4 Pass@1 rose "from 70.96% to 80.80%"; across four benchmarks the automated average rose "from 68.02% to 75.75%" for GPT-4 and 58.55% to 67.22% for ChatGPT.

### 6. Wang, Shi, Ling, Chan, Wang, Lee, Yuan, Huang, Jiao, Lyu (CUHK) — "Learning to Ask: When LLM Agents Meet Unclear Instruction" (2024; EMNLP 2025)

URL: https://arxiv.org/abs/2409.00557

Idea, verbatim (verified): facing missing arguments, LLMs "tend to arbitrarily generate the missed argument, which may lead to hallucinations and risks". The remedy, Ask-when-Needed, "prompts LLMs to ask questions to users whenever they encounter obstacles due to unclear instructions".

What they built: NoisyToolBench, a tool-use benchmark of real, unclear instructions, each annotated with the ideal clarifying questions, simulated answers and the correct final API calls; ToolEvaluator, an automatic scorer that counts right questions, right calls after clarification and redundant questions.

Measured result: the abstract says AwN "significantly outperforms existing frameworks for tool learning in the NoisyToolBench" without figures (verified). The CUHK affiliation is unverified.

### 7. Vijayvargiya, Zhou, Yerukola, Sap, Neubig (CMU) — "Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering" (2025; ICLR 2026)

URL: https://arxiv.org/abs/2502.13069

Idea, verbatim (verified): "Our findings reveal that models struggle to distinguish between well-specified and underspecified instructions."

What they built: underspecified rewrites of SWE-bench Verified issues, with a simulated user who holds the full specification and answers the agent's questions. Underspecification is defined as information whose absence would stop an expert from producing a working fix.

Measured result (verified): when the agent interacts to obtain the missing details, performance improves "up to 74%" over the non-interactive setting. The CMU affiliation is unverified.

### 8. Edwards and Schuster — "Ask or Assume? Uncertainty-Aware Clarification-Seeking in Coding Agents" (2026)

URL: https://arxiv.org/abs/2603.26233

Idea, verbatim (verified): the authors "systematically evaluate the clarification-seeking abilities of LLM agents" on an underspecified SWE-bench Verified; their scaffold "decouples underspecification detection from code execution".

What they built: a multi-agent scaffold in which one agent judges whether the task is underspecified and asks, and another executes. The agent asks more on harder tasks and less on easy ones.

Measured result (verified): 69.40% task resolve rate, significantly above a single-agent baseline (61.20% per search summary, unverified) and close to the 70.80% an agent gets with the fully specified issue (search summary, unverified).

### 9. Suri, Mathur, Lipka, Dernoncourt, Rossi, Manocha (Adobe / U. Maryland) — "Structured Uncertainty guided Clarification for LLM Agents" (2025)

URL: https://arxiv.org/abs/2511.08798

Idea, verbatim (verified): "LLM agents with tool-calling capabilities often fail when user instructions are ambiguous or incomplete"; "we present ClarifyBench, the first multi-turn dynamic tool-calling disambiguation benchmark".

What they built: ClarifyBench (document editing, vehicle control, stock trading, travel, file systems; normal, ambiguous and infeasible queries, with an LLM user simulator); SAGE-Agent, which chooses which clarifying question to ask from structured uncertainty over the tool-call arguments; and an uncertainty-weighted GRPO training recipe.

Measured result (verified): SAGE-Agent gets 7-39% higher coverage on ambiguous tasks while asking 1.5-2.7x fewer questions than prompting and uncertainty baselines; When2Call accuracy rose from 36.5% to 65.2% (3B) and 36.7% to 62.9% (7B). Affiliations unverified.

### 10. Sui, Duede, Wu, So — "Confabulation: The Surprising Value of Large Language Model Hallucinations" (ACL 2024)

URL: https://aclanthology.org/2024.acl-long.770/ and https://arxiv.org/abs/2406.04175

Idea, verbatim (verified): "hallucinated outputs display increased levels of narrativity and semantic coherence relative to veridical outputs"; this "suggests, counter-intuitively, that the tendency for LLMs to confabulate may be intimately associated with a positive capacity for coherent narrative-text generation".

What they built: a measurement study across hallucination benchmarks, scoring narrativity and coherence of hallucinated vs. true outputs, framed on the clinical notion of confabulation (false memory produced without intent to deceive) and on "a human propensity to utilize increased narrativity as a cognitive resource for sense-making" (verified). This is the closest published account of hallucination as forced coherence: the false output is *more* coherent than the true one. The authors treat this as a resource rather than a defect.

Measured result: the narrativity/coherence effect above; figures in the paper body, not read.

### 11. GitHub — Spec Kit, `spec-driven.md` and the `clarify` command (2025)

URLs: https://github.com/github/spec-kit (read raw: `spec-driven.md`, `templates/commands/clarify.md`)

Idea, verbatim (verified, `spec-driven.md`): "**Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question]" / "**Don't guess**: If the prompt doesn't specify something, mark it". Rationale: "This prevents the common LLM behavior of making plausible but potentially incorrect assumptions."

What they built: a spec-first workflow (constitution; specify, plan, tasks, implement) whose templates force the model to write `[NEEDS CLARIFICATION: ...]` markers instead of filling gaps, a checklist gate ("No [NEEDS CLARIFICATION] markers remain") before planning, and a `clarify` command whose description reads (verified): "Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec."

Measured result: none published.

### 12. Nova Elvaris — "The Assumption Inventory Prompt: Catch Hidden Requirements Before You Code" (DEV Community, March; year not shown on page)

URL: https://dev.to/novaelvaris/the-assumption-inventory-prompt-catch-hidden-requirements-before-you-code-1j6n

Idea, verbatim (verified): "When you ask an LLM to help you build something, it will happily fill in missing requirements with plausible defaults."

What they built: a preflight prompt beginning "Before proposing a solution, do an Assumption Inventory." Steps: restate the goal; list at least eight assumptions grouped by product/UX, data and edge cases, security/privacy, performance/scale, ops; rate each Low/Medium/High risk; ask up to five clarifying questions on the highest-risk ones; if unanswered, propose safe defaults and continue.

Measured result: none; practitioner prompt.

## Also found, lower rank or unverified

- Zhang, Deng, Ren, Ng, Chua — "Ask-before-Plan: Proactive Language Agents for Real-World Planning" (Findings of EMNLP 2024), https://arxiv.org/abs/2406.12639. Task "Proactive Agent Planning": predict the need for clarification from the conversation and environment, gather information with tools, then plan. Benchmark built on TravelPlanner; method is a Clarification-Execution-Planning multi-agent framework. Unverified at source (search summary only).
- Liu et al. — "AgentAbstain: Do LLM Agents Know When Not to Act?" (2026), https://arxiv.org/abs/2607.10059. Verified: existing evaluations "mostly focus on task success rather than whether agents know when to abstain"; 263 paired should-act/should-abstain tasks in 42 sandboxes; best of 17 frontier models reached 59.5% paired accuracy; abstention is "largely independent of general task-solving capability"; names a "post-hoc abstention" failure, where the agent acts irreversibly before noticing the trigger.
- Lathkar — "Anchored Confabulation: Partial Evidence Non-Monotonically Amplifies Confident Hallucination in LLMs" (2026), https://arxiv.org/abs/2604.25931. Verified: a single-author preprint claiming that partial evidence raises confident hallucination (PHC 0.613 to 0.656 then falls with more evidence, N=160) and that an "epistemic humility prompt" reduces the spike by -0.118. Directly on-topic (pieces present make forcing more likely, not less) but single-author, unreviewed; weigh accordingly.
- Yang, Chern, Qiu, Neubig, Liu — "Alignment for Honesty" (2023), https://arxiv.org/abs/2312.07000. Introduces "idk responses" and metrics for a model allowed to say "I don't know", plus honesty-oriented fine-tuning. Unverified at source.
- Wu et al. — "ClarifyCoder: Clarification-Aware Fine-Tuning for Programmatic Problem Solving" (2025), https://arxiv.org/abs/2504.16331. Fine-tunes code LLMs to ask; reports 63.61% communication rate and 51.93% good-question rate on ambiguous tasks, judged by GPT-4o-mini. Unverified at source.
- ClarEval (2026), https://arxiv.org/abs/2603.00187: 2,250 instances injecting Missing Goals, Missing Premises, Ambiguous Terminology into HumanEval and LiveCodeBench tasks. Unverified.
- Harnad — "On LLM 'Hallucination' vs 'Confabulation'" (Skywritings, 24 Aug 2025), https://generic.wordpress.soton.ac.uk/skywritings/2025/08/24/on-llm-hallucination-vs-confabulation/. Verified: argues the clinical analogy is to anosognosic confabulation (Capgras, Cotard), where the brain generates "internally coherent explanations for anomalous experiences", and warns "no one knows the underlying mechanism".
- McJohn and McJohn — "AI Mistakes: 'Confabulation' and Abduction, not 'Hallucination'" (Suffolk Law faculty paper), https://dc.suffolk.edu/cgi/viewcontent.cgi?article=1386&context=suls-faculty. Argues for the term confabulation; notes that in 1990s computer vision "hallucination" meant filling in missing pixels. Unverified.
- Cristobal Santana — "Hallucination vs Confabulation: Why LLMs Invent Answers Instead of Saying 'I Don't Know'" (Substack, 30 June 2026), https://cristobalsantana.substack.com/p/hallucination-vs-confabulation-why. Verified practitioner post: "It has a single mode: produce the most probable continuation of this text"; "Most benchmarks score a wrong answer and an 'I don't know' the same way: both get zero." Recommends making "the documents don't cover this" a valid answer, confidence thresholds, repeated sampling to detect scatter, and deliberately testing with ungroundable questions.
- Guillermo de la Puente — "Best simple Cursor Rules for better results" (8 June 2025), https://guillermodlpa.com/blog/cursor-rules-for-better-results. Verified: rules "Don't implement changes when you aren't sure." and "Before implementing code changes, ask for confirmation on the approach." Reported effect: "The results I get have dramatically changed, and I can oversee and direct the agent much more", with the caveat that it holds only "as long as the conversation isn't very long".
- Methodshop — "This Simple AI Prompt Hack Helps Prevent LLM Assumptions", https://methodshop.com/ai-prompt-hack-llm-assumptions/. A one-line prompt asking the model to list the details it needs and the assumptions it would otherwise make; the post argues the confidently adjacent answer is harder to catch than a hallucination. Unverified (page returned 403).
- Anthropic — Claude Code `AskUserQuestion` tool and plan mode, https://code.claude.com/docs/en/agent-sdk/approvals. Per the SDK docs as summarised by search: Claude asks for input when it "has clarifying questions through AskUserQuestion", most commonly in plan mode before proposing a plan; a `tools` allowlist must include it or the model cannot ask. Unverified at source.
- Counterpoint. OpenAI — "GPT-5 prompting guide", section "Prompting for more eagerness", https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide. Verified: the recommended `<persistence>` block says "Do not ask the human to confirm or clarify assumptions, as you can always adjust later", "decide what the most reasonable assumption is, proceed with it," "and document it for the user's reference after you finish acting". This is the opposite remedy for autonomous runs: act on a stated assumption and log it, instead of asking. Note it still requires the assumption be made explicit.

## What the field converges on

1. The forcing is trained in. Kalai et al. and Santana both locate it in scoring that pays nothing for "I don't know"; AbstentionBench finds reasoning training makes it worse; R-Tuning finds the fix must be trained in too, and that refusal generalises once learned.
2. Detection and asking are separate skills. Ambig-SWE: models cannot tell specified from underspecified. DiscoBench and Ask-or-Assume: decoupling the judge of underspecification from the executor is what works. SAGE-Agent: choose the question from structured uncertainty, not from prose.
3. Interaction pays. Ambig-SWE up to +74%; ClarifyGPT +10 points Pass@1 with real humans; Ask-or-Assume closes nearly the whole gap to full specification.
4. Forced coherence is measurable. Sui et al.: the hallucinated output is more coherent than the true one. Lathkar (unreviewed): partial evidence raises confident hallucination.
5. Practitioner remedies all make the unknowns explicit before action: `[NEEDS CLARIFICATION]` markers with a gate that none remain (Spec Kit); an assumption inventory with risk ratings (Elvaris); "ask for confirmation on the approach" rules (de la Puente); a `clarify` step of at most five targeted questions. Even the counterpoint (OpenAI's eagerness prompt) requires the assumption be named and documented.
6. Not found: any published work that checks a design against an explicit model of the complete whole (the "missing-piece" check from the whole, rather than from the pieces). Spec Kit's checklist gate is the nearest practice; AgentAbstain's paired should-act/should-abstain tasks are the nearest evaluation.
