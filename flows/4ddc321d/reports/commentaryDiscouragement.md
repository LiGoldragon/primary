# Discouraging commentary: prior art, levers, and risks

## 1. Prior experiments

### Instruction-level suppression (community, issue report)

**openai/codex #36509**: A user added an AGENTS.md rule equivalent to "emit
commentary only for material findings, blockers, scope changes, or final
verification." Observed result: the model acknowledged the rule but continued
emitting routine commentary. The user had to repeat the instruction more than
three times within one session. The model treated the stock base context's
60-second commentary mandate as stronger than the project-level instruction.
No report of content leaking between channels (commentary into final or vice
versa); the failure was non-compliance, not channel confusion.

### Verbosity reduction causing commentary-only stops (community, harness issue)

**earendil-works/pi #4026**: When the `openai-codex-responses` integration
changed default `text.verbosity` from `"medium"` to `"low"`, gpt-5.3-codex
began emitting commentary/planning text instead of tool calls and then ending
the turn early. The model would output "I changed X/Y/Z" summaries without
having made any tool calls. Users had to manually "continue" multiple times.
The fix was reverting to `verbosity: "medium"`.

This is the closest observed experiment to discouraging commentary: reducing
verbosity caused the model to substitute commentary for action, not to
suppress commentary in favor of action.

### Commentary loops consuming tokens (community, multiple issues)

**openai/codex #29581**: The model gets stuck repeating similar commentary
messages with no new output, consuming tokens for up to an hour without
producing a final answer or clear failure. Multiple duplicates exist (#28111,
#28158, #28751, #29557). These are not instruction-suppression experiments,
but they document that commentary emission is already a significant token cost
even under the stock prompt.

**openai/codex #17480**: Interrupted commentary-heavy streams can produce
visible retry narration that resets the no-progress detector, keeping the
session alive without converging on a completed response.

### Context cost awareness (community, feature requests)

Several issues document user awareness that commentary is a context cost
driver:

- **openai/codex #36669**: Requests model-callable context-management tools
  for selective compaction, motivated by verbose tool output and completed
  work consuming context.
- **openai/codex #39936**: Requests model-controlled per-turn reasoning
  retention, noting that much reasoning (and by analogy, commentary) is
  "only transiently useful."
- **openai/codex #26845**: Reports that Codex desktop starts fresh chats
  with ~31k tokens of fixed overhead from skill/tool injection alone.
- **openai/codex #38953**: Requests range-based message compaction.

None of these specifically target commentary suppression at the instruction
level. The community focus is on post-hoc context management, not on
reducing emission at the source.

### No found experiments discouraging commentary via base context rewrite

No OpenAI cookbook, research writeup, blog post, or community discussion
was found where someone rewrote the base context to reserve commentary for
rare cases and measured the effect. The stock prompt's 60-second mandate has
not been publicly challenged as a design parameter.

## 2. Vendor levers

### model_verbosity / text.verbosity

The only output-control lever in Codex CLI 0.149.1 is `model_verbosity`
(config.toml key), which maps to the Responses API `text.verbosity` parameter
(`Low`/`Medium`/`High`). This controls overall output length, not commentary
specifically. It affects both commentary and final-answer output equally.

As of the 2026-08-25 server catalog snapshot, no model (including the three
5.6 variants) has `support_verbosity: true`. The parameter is defined in the
protocol but not enabled for any current model.

The earendil-works/pi #4026 finding shows that `text.verbosity = "low"`
degraded tool-calling behavior rather than suppressing commentary.

### Personality settings

The personality variants (default, friendly, pragmatic) are injected as a
separate developer-role message describing communication style. None reference
commentary frequency or emission.

### No commentary-specific config keys

No config key, CLI flag, server-catalog field, or per-model setting controls
commentary frequency, emission, or retention. Commentary behavior is
controlled entirely by the base context instructions.

### Base context override

The `config.toml` key `instructions` (or `model_instructions_file`) can
replace the entire server-catalog base context. This is the mechanism by which
a replacement base context with rare-commentary instructions would take
effect. The priority chain is: config `base_instructions` > resumed-thread
instructions > server-catalog `instructions_template`.

## 3. Client-side cost elimination

### What the code allows

The history gate (`is_api_message` in `history.rs:575`) checks `role` only;
no phase check exists. The `for_prompt()` path returns all recorded items
without filtering. A harness could add a phase-based filter in either
location to drop prior-turn commentary items from the replayed history.
This is a client-side change to `codex-rs/core/src/context_manager/history.rs`;
no server cooperation is required.

### What the vendor warns against

Two vendor sources warn about phase handling in history:

**Codex Prompting Guide** (cookbook): "Correctly preserving `phase` on
assistant items is required for `gpt-5.3-codex`. If assistant `phase`
metadata is dropped during history reconstruction, significant performance
degradation can occur."

**Deployment Checklist** (API docs): "When you send that history back on
follow-up requests for `gpt-5.3-codex` and later models, preserve and resend
`phase` on assistant messages so the model can distinguish progress updates
from the final result. This helps reduce early stopping, making the agent
more likely to continue until it reaches the final answer."

### What the warning covers

Both warnings specifically address dropping the `phase` field from assistant
messages that remain in history — i.e., sending back a message that was
`phase: "commentary"` without its phase tag, so the model cannot distinguish
it from a final answer.

Neither warning addresses dropping entire commentary items from history. The
deployment checklist's rationale — "so the model can distinguish progress
updates from the final result" — implies the concern is mislabeled items, not
absent items. If all commentary items were removed, there would be no
unlabeled items to confuse with final answers.

However, this is inference. No vendor source explicitly blesses or condemns
dropping whole commentary items. The model may rely on seeing its own prior
commentary for cross-turn continuity (the codexChannels report documents
that commentary functions as working memory). Dropping it could cause the
model to re-derive context already established, or to lose track of
assumptions it stated in earlier commentary.

### PR #19832 (phase preservation fix)

This PR fixed a bug where phase was lost when converting between
`ResponseInputItem::Message` and `ResponseItem::Message` at the inter-agent
boundary. The fix explicitly sets `MessagePhase::Commentary` on inter-agent
messages. This confirms that OpenAI treats phase preservation as a
correctness requirement for messages that remain in history, but does not
speak to whether removing whole commentary items is safe.

## 4. Risks of instruction-level discouragement

### Observed risk: content substitution (verbosity reduction)

The earendil-works/pi #4026 finding is the strongest evidence of a specific
failure mode: when output was constrained (via `text.verbosity = "low"`),
the model emitted commentary-like "status update" text instead of making
tool calls, then stopped. The constraint did not suppress commentary; it
caused the model to substitute commentary for action.

A rare-commentary instruction could trigger the same pattern: the model
might pad final answers with working notes that would otherwise have been
commentary, or emit planning text as part of a tool call's reasoning rather
than as a separate commentary message.

### Expected risk: blind users during long turns

The stock base context mandates commentary "at least within every 6 steps
or 10 tool calls." If commentary is reserved for rare cases, users will
see no output during long tool-calling sequences. openai/codex #30945
documents a related failure: commentary-only assistant turns are hidden
under "Worked for Xs" in the desktop app, and if the model marks
in-progress commentary as `task_complete`, the turn silently ends. Rare
commentary would make this worse by extending the silent periods.

### Expected risk: unasked blocking questions

Commentary is the channel through which the model surfaces blocking
questions before producing a final answer. If the instruction discourages
commentary, the model might either skip asking the question (proceeding
on wrong assumptions) or embed the question in the final answer (wasting
the final-answer channel on a question rather than a result).

### Expected risk: loss of cross-turn working memory

Commentary items are replayed to the model and function as working memory
(codexChannels report, §2). If the instruction succeeds in reducing
commentary, the model loses the ability to build on stated assumptions,
partial results, and working observations in later turns. This cost is
compounding: the longer the session, the more working memory is lost.

### Mitigating design

A rare-commentary instruction would pair naturally with client-side
commentary filtering. If the model emits less commentary, there is less
to accumulate in context. And if the harness also filters prior-turn
commentary from replayed history, the instruction and the filter reinforce
each other: the model is told not to rely on commentary as working memory,
and the harness ensures it cannot.

The risk profile is different for a replacement base context that the
psyche controls end-to-end versus a stock prompt that must serve all
users. The stock prompt's 60-second mandate is a safe default for unknown
workloads. A purpose-built prompt can accept the tradeoff of silent
periods in exchange for context efficiency, because the user (the psyche)
knows the work style and can adapt.

## Unknowns

1. **No direct experiment**: No one has publicly tried a base context that
   reserves commentary for rare cases and measured task performance. All
   evidence is indirect (verbosity reduction, instruction non-compliance,
   commentary loops).

2. **Server-side phase processing**: Whether the OpenAI server does
   differential processing of phase-tagged items (attention masking,
   selective weighting) beyond what the client sends. If the server
   weights commentary items differently, dropping them from client-side
   history could have effects beyond what the client-side code predicts.

3. **Model-version sensitivity**: The warnings cite `gpt-5.3-codex`
   explicitly. Whether 5.6 models have the same sensitivity to phase
   metadata and commentary presence is unknown.

4. **Verbosity interaction**: Whether `text.verbosity` interacts with
   commentary-discouraging instructions (amplifying the content-substitution
   failure) is untested.

## Sources

### Witness records (own code reads)

- `flows/4ddc321d/witnesses/codexChannelWireFormat.md` — MessagePhase enum,
  is_api_message, for_prompt, compaction retention. Tag `rust-v0.149.1`.
- `flows/4ddc321d/witnesses/codexCommentaryLevers.md` — model_verbosity,
  personality, history filtering absence, config search. Tag `rust-v0.149.1`.

### Prior flow reports

- `flows/4ddc321d/reports/codexChannels.md` — commentary as working memory,
  retention lifecycle, compaction behavior.
- `flows/4ddc321d/reports/codex56Context.md` — 5.6 base context block
  inventory, commentary mandate at lines 34-41.

### External documentation (carried claims)

- OpenAI Codex Prompting Guide: "Correctly preserving `phase` on assistant
  items is required for `gpt-5.3-codex`. If assistant `phase` metadata is
  dropped during history reconstruction, significant performance degradation
  can occur." Cadence recommendation: "aim every 1–3 execution steps; hard
  floor: at least within every 6 steps or 10 tool calls."
  URL: https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide

- OpenAI API Deployment Checklist: "preserve and resend `phase` on assistant
  messages so the model can distinguish progress updates from the final
  result."
  URL: https://developers.openai.com/api/docs/guides/deployment-checklist

- OpenAI Reasoning Models guide: phase field documentation.
  URL: https://developers.openai.com/api/docs/guides/reasoning

### GitHub issues and PRs (community reports)

- openai/codex #36509: AGENTS.md commentary-suppression rule ignored by model.
  URL: https://github.com/openai/codex/issues/36509
- openai/codex #29581: Commentary loop consuming tokens without progress.
  URL: https://github.com/openai/codex/issues/29581
- openai/codex #17480: Commentary-heavy retry loops.
  URL: https://github.com/openai/codex/issues/17480
- openai/codex #30945: Commentary-only turn marked task_complete.
  URL: https://github.com/openai/codex/issues/30945
- openai/codex #36669: Model-callable selective compaction request.
  URL: https://github.com/openai/codex/issues/36669
- openai/codex #39936: Model-controlled reasoning retention.
  URL: https://github.com/openai/codex/issues/39936
- openai/codex #26845: Context overhead from skill/tool injection.
  URL: https://github.com/openai/codex/issues/26845
- openai/codex #38953: Range-based message compaction.
  URL: https://github.com/openai/codex/issues/38953
- openai/codex #19832: Phase preservation fix for inter-agent messages.
  URL: https://github.com/openai/codex/pull/19832
- earendil-works/pi #4026: text.verbosity="low" regresses tool-calling,
  causes commentary-only stops.
  URL: https://github.com/earendil-works/pi/issues/4026
