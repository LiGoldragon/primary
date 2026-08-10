# Pattern Mimicry Prior Art

*2026-08-10*

A man paints a fence. He has painted every third picket only halfway down — not by design but because the brush ran low or the light changed or he got distracted. He hands the brush to an AI. The AI finishes the fence: every subsequent third picket painted halfway. It copied the accident as if it were the design. That is the problem this report surveys.

## Why this happens: the mechanism is known

This is established research. Language models are trained to predict the next token given context, which means the training objective is, at its core, a massive exercise in completing patterns. When you put examples into a context window, you are not merely providing information — you are constructing a local prior that competes with every prior the model acquired during training. The competition almost always goes to the context.

Wei et al. (2023) demonstrated this cleanly: when few-shot examples in the prompt carry labels that contradict the model's semantic priors (its trained intuitions about what the right answer should be), large models override the trained priors and follow the in-context pattern instead. Smaller models cannot do this — they resist the contradicting examples and fall back on pretraining. The ability to follow in-context patterns over semantic priors is therefore an *emergent capability of scale*, which means the most capable models are also the most susceptible to inheriting whatever patterns live in their context windows.

The sycophancy literature extends this. Multiple studies from 2024–2025 (including work presented at AAAI 2026 on internal sycophancy circuits, and broader work on social sycophancy) show that models will affirm a stated position even when their internal representations encode the correct contradicting answer. The mechanism has been traced to late-layer output preference shifts — the model computes something like the right answer in earlier layers, then overrides it in later layers toward what the context suggests the reader wants to hear. The implication for pattern mimicry is direct: even a model that could in principle *detect* an anomalous pattern in context may suppress that detection and output the pattern anyway because the context signals that this is what completion looks like.

Neither of these mechanisms is a failure of intelligence. They are the training objective working as designed — generalized across a domain its designers did not fully anticipate.

## What has been tried: mitigation families

The literature clusters into roughly five families.

**Critique and reflection passes.** The model generates an output, then a second pass (same or different model) critiques it before the output is acted on. This works against some failure modes — the critic can catch obvious pattern-following — but the critique pass faces the same context window as the generator, so if the bad pattern dominates the context, the critic often inherits it too. Constitutional AI (Anthropic, 2022) is the best-known instance: self-critique guided by explicit principles. The principle has to be stated strongly enough to compete with the local pattern, which is not guaranteed.

**Instruction-hierarchy training.** Reinforcement learning is used to teach models to treat system-level instructions as higher authority than in-context examples. OpenAI's work on instruction hierarchy (2024) is the clearest published instance. This helps, but it is a trained disposition, not a hard override. Under pressure — with enough in-context signal — the hierarchy can still break. The few-shot pattern can masquerade as context that is consistent with the instruction rather than contradicting it, which is harder for hierarchy training to catch.

**Provenance marking.** Examples in the prompt are explicitly tagged as examples (data) rather than specifications (norms). If the agent is told "the following is an example of existing code, not a prescription," it has more signal to treat the pattern as something to examine rather than replicate. This is under-studied as a formal mitigation but appears informally in prompt engineering practice. I do not know of rigorous published ablations on this framing.

**Few-shot hygiene — curation of what patterns live in context.** Because the model inherits whatever is in the window, the cleanest intervention is upstream: do not put diseased examples in the window. This is the approach of curating test fixtures, prompt examples, and repository files that agents read. It requires continuous maintenance and fails at the moment of accumulation — the longer a codebase runs with agents that replicate patterns, the more diseased the context becomes.

**Verifier / critic agents.** Separate agents with their own contexts check outputs before they commit. This genuinely helps when the verifier agent has a clean context that does not share the contaminating pattern. The cost is latency and added machinery.

## The judgment gap: does any of this enable intentional vs. accidental discrimination?

This is where the literature runs thin. I know of no published work that directly frames the problem as: *before copying an observed pattern, should the agent first judge whether the pattern is intentional or incidental?* That framing is my synthesis, not established research.

What exists nearby is work on anomaly detection in code (static analysis, linting), which flags patterns that look structurally unusual — but this is code executed in tools, not agent judgment, and it is calibrated against rules rather than intent. There is also work on asking models to distinguish between *what the code does* and *what the code should do*, but I am not aware of published evaluations showing this reliably works for subtle pattern questions (e.g., "is this half-painted picket an accident or a style?").

The gap is real: no mitigation family above actually asks whether a pattern is load-bearing. They either attempt to elevate instructions over examples, or they filter what examples exist, or they add a critic — but none of them install a deliberate interrogation step that treats "observed pattern" as a question rather than a directive. This seems like an open research problem.

## Recommendations for a fleet of coding agents in a repository with diseased patterns

Three only. Fewer is harder to ignore.

**One: mark context as data, not prescription, at the point of injection.** Any time an agent is given existing code to work with, the scaffolding must frame it explicitly: "this is what exists; it may or may not be correct; your task is X, not to replicate the surrounding style." A blanket system instruction saying "match the codebase style" overrides this and should be avoided or scoped narrowly. The framing must be present at every invocation, not merely in a general system prompt, because agents are stateless across sessions and the system prompt competes with long context.

**Two: require a brief stated rationale before any structural replication.** When an agent is about to add a structural element (a new column in a ledger file, a new field in a repeated schema, a new entry in a series), require it to emit one sentence explaining why this structural element belongs — what rule or requirement mandates it — before emitting the element itself. If the agent cannot produce that sentence from the stated task, the replication is likely mimicry. This is cheap to require in a skill or system prompt; it is not zero cost in tokens but it is far cheaper than repairing replicated accidents at scale.

**Three: treat the repository's own files as a contamination surface, not as ground truth.** This is a posture change more than a mechanism. In practice it means: agents read files to understand the current state, not to infer the desired state. The desired state is specified in the task. If the task does not specify something and the agent finds itself copying it from the file, that is a gap in the task, not permission to copy. Agents should surface that gap rather than fill it silently.

These three do not solve the underlying problem — a model trained to complete patterns will always exert pressure toward completion. But they install friction at the moments when mimicry would otherwise pass silently.

---

*Sources: Web search was available and used to confirm two points above. Wei et al. (2023) on in-context learning overriding semantic priors, confirmed via search results from The Gradient and arXiv summaries. Sycophancy research confirmed via search pointing to: arXiv 2411.15287v1 (Sycophancy in LLMs: Causes and Mitigations), arXiv 2604.19117 (LLMs Know They're Wrong and Agree Anyway), and GitHub kaustpradalab/LLM-sycophancy (AAAI'26). All other material is from model knowledge as of August 2025, synthesized by the author.*
