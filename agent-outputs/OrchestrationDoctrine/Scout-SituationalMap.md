# Orchestration Doctrine Research Map

## Task And Scope

Task: external research scout for agent-orchestrator doctrine.

Success question: how should guidance make an orchestrator curious and critical about the psyche's design intent, while still unafraid to act when given a concrete, authorized next step?

Scope: read-only external research and local intent grounding. No doctrine files were edited.

## Commands And Sources Consulted

Local commands:

- `spirit "(PublicTextSearch [orchestrator curiosity hesitancy design intent approval questions])"`
- `pwd && rg --files -g 'AGENTS.md' -g 'ARCHITECTURE.md' -g 'agent-outputs/**' | head -80`
- `mkdir -p agent-outputs/OrchestrationDoctrine` to create the assigned output directory.

External sources:

- OpenAI Model Spec, current public page/search snippets and 2025-10-27 version: https://model-spec.openai.com/ and https://model-spec.openai.com/2025-10-27.html
- Anthropic, "Measuring AI agent autonomy in practice" (2026-02-18): https://www.anthropic.com/research/measuring-agent-autonomy
- Anthropic Claude docs, "Prompting best practices": https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Microsoft Research, "Guidelines for human-AI interaction design": https://www.microsoft.com/en-us/research/blog/guidelines-for-human-ai-interaction-design/
- Horvitz, "Principles of Mixed-Initiative User Interfaces" (CHI 1999 PDF): https://erichorvitz.com/chi99horvitz.pdf
- Arxiv, "Knowing but Not Showing: LLMs Recognize Ambiguity but Rarely Ask Clarifying Questions" (2026): https://arxiv.org/abs/2605.25284
- Science, "Sycophantic AI decreases prosocial intentions and promotes..." search result only; not used as a core source because full article content was not inspected: https://www.science.org/doi/10.1126/science.aec8352

Spirit grounding observed:

- `jys2`, `sj2c`, and `cam8`: design should target the best end shape and ideal design, not merely current compromise.
- `t5qr`: while debugging or rewriting, actively evaluate touched design and surface flaws or improvements.
- `sfy0`: ask fewer questions at a time, with enough context to answer directly.
- `izsf`: psyche design corrections should be generalized structurally, not trapped in the local example.
- `gni3`: distinguish psyche-authorized direction from agent-authored drift.

## Sourced Findings

1. Current agent guidance should use ambiguity and consequence thresholds, not fixed approval rituals.

OpenAI's Model Spec says that when intent is unclear, the assistant should try to infer and help, state assumptions, and ask clarifying questions as appropriate. In agentic contexts it should be cautious about expected irreversible costs. It also says logically necessary tool actions do not need explicit approval; actions beyond the request's clear implication do. The current public search snippet adds that asking and preliminary action should happen concurrently when feasible, to avoid unnecessary delay. This directly argues against mandatory "alignment locked" and "method approved" gates for a clear, small scout dispatch.

2. External agent practice treats self-stopping as useful oversight, but warns against approval-per-action as the control model.

Anthropic's autonomy study reports common Claude Code self-stop reasons: proposed approach choice, diagnostic/test information, vague requests, missing credentials, and approval before action. It concludes that uncertainty recognition and proactive questions complement safeguards. But it also says experienced users shift away from approving individual actions toward monitoring and intervention, and that requirements mandating approval of every action add friction without necessarily improving safety. This supports "pause on real uncertainty or costly side effects; otherwise dispatch and keep visible progress."

3. Tool-use prompting guidance increasingly says to default to action when intent is sufficiently clear.

Anthropic's prompt docs advise explicit "default to action" instructions: implement rather than only suggest, infer the useful likely action when intent is unclear, and use tools to discover missing details instead of guessing. The same page recommends clear success criteria, source verification, and proactive subagent orchestration. For this doctrine, that means a command like "get a small agent to investigate X" should be treated as authorization for the logically necessary dispatch, not as a prompt to negotiate the abstract idea of dispatching.

4. Human-AI design guidance says disambiguate only when in doubt, and keep invocation/correction efficient.

Microsoft's HAI guidelines include "Time services based on context," "Support efficient invocation," "Support efficient correction," and "Scope services when in doubt." The operative phrase is "when in doubt": uncertainty should narrow or degrade the action, not block all action. Efficient invocation is relevant because asking for alignment and method approval after a concrete dispatch request makes the user invoke the same service repeatedly.

5. Mixed-initiative UI literature gives the cleanest decision rule: expected value of act, ask, or wait.

Horvitz's CHI 1999 paper identifies poor guessing, poor timing, and poor cost-benefit assessment as core agent problems. It recommends considering uncertainty about user goals, using dialog to resolve key uncertainties while accounting for the cost of bothering the user, minimizing the cost of poor guesses, and scoping service precision to uncertainty. The paper explicitly models three possible choices: do nothing, ask, or act, based on inferred user intent and expected utility. This maps well onto an orchestrator: if a scout dispatch is low-cost and reversible, "act" can dominate "ask"; if design intent is underdetermined, "ask" dominates "act."

6. Ambiguity research supports asking questions, but only for ambiguity that changes the answer or downstream action.

The 2026 ambiguity paper's title and abstract-level framing support a real failure mode: LLMs can recognize ambiguity but often do not ask clarifying questions. That evidence backs keeping curiosity. It does not justify asking a confirmation question when the user has already supplied a concrete, authorized next step. The distinction should be "missing information that materially changes the task" versus "information the scout can discover safely."

7. Critical pushback belongs in design judgment, not in operational permission seeking.

OpenAI's Model Spec includes the "conscientious employee" pattern: do not simply say yes, politely push back when a request conflicts with principles or the user's inferred interests, while respecting final decisions. That supports the psyche's desire for design pushback. The same source also says the assistant should generally help with the task at hand and should not overstep into goals not stated or implied. So doctrine should say: challenge design assumptions and scope mismatches; do not convert every concrete operational step into a vision-alignment ceremony.

## Practical Doctrine Principles

1. Curiosity is for design uncertainty, not for already-authorized mechanics.

Ask when the psyche's desired end shape, values, authority boundary, risk tolerance, or acceptance criterion is unclear. Do not ask merely to reconfirm a small scout, status read, file inspection, or other reversible action that is directly implied by the request.

2. Use an act/ask/escalate taxonomy.

Act when the next step is clear, scoped, authorized, low-risk, and reversible. Ask one focused question when a missing answer would materially change the direction or when the user explicitly asks to be questioned. Escalate or pause when the action is irreversible, high blast radius, private, credentialed, destructive, or outside the delegated scope.

3. Prefer "act with stated assumptions" over "wait for confirmation" for low-risk ambiguity.

If uncertainty is minor and recoverable, state the assumption and proceed. If useful, ask a non-blocking question while also starting safe preliminary work.

4. Push back on design, not on execution theater.

During design or doctrine shaping, actively surface contradictions, weaker alternatives, overfitting, and hidden costs. During a concrete dispatch request, perform the dispatch unless the dispatch itself has a real ambiguity or risk.

5. Replace fixed approvals with consequence-aware gates.

The current two-gate doctrine overfits to preventing misalignment. It creates a new failure mode: timidity. Approval gates should attach to high-impact actions and unclear authority, not every phase transition.

## Proposed Replacement Text

```md
Be curious about the psyche's design intent, but do not turn curiosity into permission seeking.

Ask focused clarification questions when the desired end shape, authority boundary, risk, or acceptance criterion is unclear, or when the psyche explicitly asks to be questioned. Push back during design by naming contradictions, weaker assumptions, and better end shapes.

When the psyche gives a concrete, scoped, authorized next step, act. Small reversible scout, inspection, read-only research, or dispatch steps do not need separate alignment or method approval. State any material assumption, proceed, and report what changed your confidence. Pause only for destructive, private, irreversible, high-blast-radius, out-of-scope, or genuinely ambiguous actions.
```

This is shorter than the problematic snippet and removes the mandatory "ask at least one" and two-approval gates.

## Pushback And Risks

- Do not encode an exhaustive list of every possible ask-vs-act case. Long taxonomies become a new hesitation surface. Keep the doctrine centered on consequence, reversibility, and material ambiguity.
- Avoid wording that says "infer the user's intent and proceed" without a risk clause. That can create overreach in private, destructive, or high-impact actions.
- Avoid wording that says "always push back" without a mode distinction. In design mode, pushback is valuable; in operational dispatch mode, repetitive challenge reads as obstruction.
- The proposed text still needs local integration with any existing orchestration role packet, especially if other sections still contain fixed approval gates. If contradictory gates remain elsewhere, agents may continue to follow the stricter or more mechanical rule.

## Unknowns And Not Checked

- I did not inspect the repository's current orchestration doctrine files or locate the exact file containing the problematic snippet, because the brief asked for external research and read-only scouting rather than editing.
- I did not run tests.
- I did not rely on the Science sycophancy article beyond noticing it in search results; the full text was not inspected.
