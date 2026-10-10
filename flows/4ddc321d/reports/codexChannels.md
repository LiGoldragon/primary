# Codex CLI channels: stratum identity and retention

## Question 1: Are commentary and final in the same stratum?

**Yes.** Commentary and final are both `ResponseItem::Message` with
`role: "assistant"`, differing only by a `phase` field
(`MessagePhase::Commentary` vs `MessagePhase::FinalAnswer`). They occupy the
same position in the context: the assistant's output stream. They are not
different input strata; they are tags within one stratum.

The hypothesis holds: the harmony/Responses format gives the model output
channels inside one assistant turn, and those channels differ in visibility and
retention policy, not in context position. In context-strata terms, they are the
same stratum -- the assistant's own output -- and neither is an input stratum at
all.

In the BEM (realtime) transport, the model emits three bracket-prefixed
channels (`[ANALYSIS]`, `[COMMENTARY]`, `[FINAL]`) within a single text stream.
Analysis and commentary both map to `MessagePhase::Commentary`; only final maps
to `MessagePhase::FinalAnswer`. In the HTTP/SSE transport, the API returns
separate `response.output_item.done` events, each carrying the `phase` field.

## Question 2: Does commentary help the LLM work?

**Yes -- commentary is load-bearing working memory, not just user-facing
decoration.** Pre-compaction, commentary messages are retained in conversation
history and replayed to the model in every subsequent turn. Post-compaction,
they are dropped (along with final-answer messages) and replaced by the
compaction summary.

### Evidence, ranked

**1. Local source code (strongest)**

The history recording function `is_api_message`
(`codex-rs/core/src/context_manager/history.rs:575`) admits all
`ResponseItem::Message` where `role != "system"` -- no phase check. Commentary
messages are recorded identically to final-answer messages. The `for_prompt()`
function returns all recorded items without phase filtering. The HTTP transport
path sends the full history as `input` in every API request.

After compaction, `is_retained_for_remote_compaction_v2`
(`codex-rs/core/src/compact_remote_v2.rs:533`) retains only `user | developer |
system` role messages. Both commentary and final-answer assistant messages are
dropped and replaced by the encrypted compaction summary.

**2. OpenAI documentation (corroborating)**

The Codex Prompting Guide states: "If assistant `phase` metadata is dropped
during history reconstruction, significant performance degradation can occur."
And: "preserve and resend phase on all assistant messages." This confirms the
model is trained to expect phase annotations and that commentary items in
history are not dead weight -- they serve as labeled context the model uses to
distinguish its working notes from its completed output.

**3. Codex CLI PR evidence (corroborating)**

PR #19832 (openai/codex) fixes a bug where phase was lost during message
conversion, confirming the project treats phase preservation as a correctness
requirement. Inter-agent messages are tagged `MessagePhase::Commentary` because
they are "assistant-authored in-between updates, not completed final answers."

### Retention summary

| Item kind | Replayed pre-compaction? | Survives compaction? |
|-----------|--------------------------|---------------------|
| Assistant (commentary) | Yes | No (summarized) |
| Assistant (final_answer) | Yes | No (summarized) |
| Reasoning (encrypted) | Yes | No (summarized) |
| User message | Yes | Yes |
| Developer message | Yes | Conditional |

### Functional consequences

Commentary costs generation tokens when emitted and input tokens on every
subsequent turn until compaction. It is not free context -- it accumulates
alongside all other history items. But the model can build on its own prior
commentary within a session: assumptions stated in commentary, partial results
reported, and working observations are all visible to the model in later turns.

The base prompt instruction that "users should never need to read earlier
commentary updates, since they are collapsed after the final answer is shown"
describes the UI behavior, not the model's context. The model sees everything;
the user sees only the final answer by default.

## Unknowns

1. **Server-side processing**: Whether the OpenAI server does additional
   processing of phase-tagged items beyond what the client sends (differential
   weighting, attention masking, selective replay). The client sends them
   identically; server behavior is not observable from code.

2. **Why phase matters for performance**: The docs say dropping phase degrades
   performance but do not explain the mechanism. It could be attention pattern
   disruption or training data alignment.

3. **Server-side compaction internals**: The server's `/responses/compact`
   endpoint produces an opaque encrypted summary. What the server retains from
   commentary vs final items inside that summary is unknown.

4. **Analysis channel distinctness**: The BEM path maps both `[ANALYSIS]` and
   `[COMMENTARY]` to `MessagePhase::Commentary`. Whether the model internally
   distinguishes these two, or whether the Responses API has a separate
   representation for analysis content (possibly as `ResponseItem::Reasoning`),
   is not fully determined. The harmony format spec mentions dropping "previous
   CoT content" after a final-channel completion, which may refer to analysis
   specifically, but this is a claim from docs, not verified from code.

## Proposed context-strata addition

Draft for psyche review -- not to be landed by this flow.

```
Channels within an output stratum

A harness may define named channels (e.g. commentary, final) within the
assistant's output. These are not separate strata; they are tags on items
within one stratum -- the assistant's own output. They differ in visibility
(the UI may collapse commentary after the final answer) and in retention
policy (compaction may summarize them differently), but they occupy the
same context position and the model sees all of them until compaction
intervenes.

Verified for: Codex CLI 0.149.1, harmony/Responses format. Commentary and
final are both ResponseItem::Message with role "assistant", phase field
distinguishing them. Both are replayed to the model pre-compaction. Both
are dropped post-compaction.
```

## Sources

### Witness records (own code reads)

- `flows/4ddc321d/witnesses/codexChannelWireFormat.md` -- MessagePhase enum,
  ResponseItem::Message phase field, is_api_message, compaction retention,
  BEM channel mapping, HTTP transport, reasoning items. All at tag
  `rust-v0.149.1` in `/git/github.com/openai/codex`.

### Prior flow witnesses

- `flows/4ddc321d/witnesses/codexSkillMentionMechanics.md` -- skill injection
  mechanics at same tag.

### Prior flow reports

- `flows/4ddc321d/reports/codex56Context.md` -- 5.6 base context block
  inventory, channel instructions at lines 25-27.

### External documentation (carried claims)

- OpenAI Codex Prompting Guide: phase preservation requirement,
  "significant performance degradation" if phase dropped.
  URL: https://platform.openai.com/docs/guides/codex (section on
  conversation history reconstruction).
- OpenAI Responses API reference: `phase` field on `ResponseOutputMessage`.
  URL: https://platform.openai.com/docs/api-reference/responses
- OpenAI PR #19832 (openai/codex): phase preservation fix for inter-agent
  messages.

### Local source (code-read paths at rust-v0.149.1)

- `codex-rs/protocol/src/models.rs` -- MessagePhase enum (893-901),
  ResponseItem::Message (940-965), Reasoning item (976-988)
- `codex-rs/core/src/context_manager/history.rs` -- is_api_message (575-596)
- `codex-rs/core/src/compact_remote_v2.rs` -- is_retained_for_remote_compaction_v2 (527-557)
- `codex-rs/core/src/realtime_conversation/bem.rs` -- channel-to-phase mapping (10-14)
- `codex-rs/core/src/client.rs` -- HTTP transport, full history in input (~580-640)
