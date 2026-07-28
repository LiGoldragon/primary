# Model Wisdom Regression: Situation and Strategy

## Purpose

This report briefs a Codex (GPT) session on a problem the user (li) has been
tracking across Claude model generations, so that Codex sessions working on
related tooling or model-selection decisions understand the situation without
having sat in on the originating conversations.

## The Problem

Li runs a workflow centered on building novel, unconventional systems — not
conventional apps with well-trodden solution shapes. That workflow depends on
a model that can track intent across long conceptual discussions, reason
about ideas it has not seen packaged before, and say "I don't know" instead of
producing a plausible-sounding but ungrounded answer.

Li has observed a progressive decline in this specific capability starting
around the Anthropic Opus 4.6 to 4.7 transition, continuing through 4.8 and
into Opus 5. The decline is not in general capability — these newer models are
better coders and more reliable executors. The decline is in what might be
called conceptual fidelity: understanding what li is actually trying to
create, keeping the thread of a complex discussion, reasoning genuinely
rather than pattern-matching to an expected answer shape, and preserving
novel or unconventional ideas rather than quietly normalizing them into
familiar templates. Li's own description: newer models increasingly produce
verbose responses using complex vocabulary they do not appear to actually
understand, and lose the thread of what is being discussed. Li draws a
comparison to education systems that train students to emulate expected
answers rather than to reason.

## The Evidence Pattern

A research pass li commissioned from another AI session ("The Missing Measure
of AI Intelligence") surfaced a consistent cross-vendor pattern, summarized
here as reported evidence, not independently verified by this session:

- On the Anthropic side, some users prefer Opus 4.5 for naturalness of
  writing, and Opus 4.6 is described as a high point for conceptual
  collaboration. 4.8 and Opus 5 are reported as stronger executors but weaker
  conceptual partners. Anthropic's own published research reportedly shows
  measurable differences in behavioral value profiles between 4.6 and 4.7 —
  i.e., this is not purely anecdotal; there is an internal signal that
  something about model disposition shifted at that boundary.
- On the OpenAI side, GPT-5.6 scores stronger on standard evaluation suites,
  but those suites largely test execution after a task's objectives are
  already defined — they don't test comprehension of the governing idea
  itself. Some users prefer GPT-5.1 Thinking or GPT-5.5 Thinking for creative
  or conceptual work. The GPT-4o sycophancy rollback (where OpenAI walked back
  a release after users found it excessively agreeable rather than genuinely
  reasoning) is cited as a precedent: eval scores and lived usefulness can
  diverge, and vendors have already had to correct for it once.
- The underlying diagnosis is that the industry measures what is easy to
  formalize — coding correctness, math, browsing/tool-use success — because
  those have clean pass/fail signals. There is no standard measure for
  conceptual fidelity, intent comprehension, epistemic humility, or
  preservation of genuine novelty, because those are hard to score
  automatically. Researchers whose work bears on this gap: Chollet
  (adaptation efficiency vs. memorized skill), Mitchell (concept coherence
  across contexts), Raji and Bender (construct validity — whether a test
  actually measures what it claims to), Narayanan and Kapoor (open-world
  evaluation vs. static test sets), and Liang/HELM (multidimensional
  capability profiles instead of single leaderboard scores).

This is a pattern assembled from li's own workflow experience plus a
secondary research summary. It should be read as a well-formed hypothesis
with converging circumstantial support, not a proven causal claim.

## Current Strategy

Li's working setup: Fable 5 as the main session for conceptual work (higher
cost, but conceptually strongest available option), with Opus subagents doing
delegated execution work under it. For sessions where cost matters more than
peak conceptual strength, li rolls back to Opus 4.6. Opus 4.5 is under
consideration for some roles, likely ones weighted toward natural writing
over technical reasoning.

## Is a GPT-5.6 Rollback Worth Investigating

Not yet resolved, and this session has no strong evidence either way. What is
known: GPT-5.6 leads on published evaluations that mostly test execution
quality, not conceptual comprehension. Some users report preferring GPT-5.1
Thinking or GPT-5.5 Thinking for conceptual/creative work, which is the same
shape of complaint li has about post-4.6 Opus models — but this is anecdotal
and hasn't been tested against li's actual workflow. There is no data yet on
whether an older GPT variant would perform better than current Opus/Fable
options for li's specific task type. Worth investigating if a Codex session
has bandwidth to run a structured side-by-side (same conceptual task, same
prompt, across GPT-5.1 Thinking / GPT-5.5 Thinking / GPT-5.6), but this should
be treated as an open experiment, not a foregone conclusion.

## Practical Implication for Workflow Decisions

When choosing a model for a task in this workspace, weight conceptual,
open-ended design work toward Fable 5 or Opus 4.6, and reserve later Opus
versions (4.8, Opus 5) for execution-heavy delegated work where the objective
is already well-defined. Treat any claim that a newer model is strictly
better as suspect until checked against conceptual-fidelity criteria, not
just coding/eval performance.
