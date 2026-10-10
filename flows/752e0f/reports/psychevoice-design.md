# PsycheVoice: design

Design worker for Psyche High 752e0f, 2026-09-24. Drawn from Field Luna e71dab's record of tonight's live voice session and from its native transcript, the Codex next binary installed on this host, and the vendor's public pages. Each fact says where it comes from: witnessed in e71dab's transcript, read in the installed binary (strings, not exercised), or vendor claim (web, not our witness). The flow's own inference is marked as inference.

## What the living said

Recorded by Field Luna e71dab (flows/e71dab/vision/voiceLuna.md and psycheVoice.md), speaker unverified, capture times 22:34 to 22:38 UTC:

> I so, I want a new flow, that's just I guess it's a psyche flow. But it runs on uh It runs on Luna at light effort so that it's faster for voice interaction. And its job is to just, keep messaging, it's a messaging and summarizing responses from other subflows type subflows. And it should ideally warn me before it's going to compact and ideally it would have a hook that would re-inject a sort of fresh vision summary every time it compacts. But we can leave the hook out for now

> ... it's Psyche Voice, in pascal case. So Psyche voice in one symbol, no space, in pascal case. This is the type. It's a Psyche voice type of flow. So, It's kind of part of the psyche stack. And it's a Luna at lightest effort. Mostly talks with Psyche, and conveys messages, and uh gives summary to the living through a voice mode on chat GPT

> Yeah. Like what you're doing now, but basically lower effort on the Luna. So it's more geared towards fast response than thinking longer. So you're a bit slow. It would be better if you were responding faster because you're really just relaying and summarizing, contextualizing my messages to other flows and subflows of your own

> ... If there's anything that you didn't know and you needed to find out on how to do, uh make sure that is part of the skills that are going to be loaded with this voice uh main flow.

Already standing: Intent/models.md, "Effort may be set light where a task needs speed — voice among them — but it is never raised to buy quality."

## Anatomy

### What it is

PsycheVoice is a Psyche-aspect main Flow whose role is to be the living's voice line. It runs on GPT-6 Luna at the lightest effort the harness offers. The living speaks to it through ChatGPT voice mode on the phone, which reaches a Codex Flow through Codex Remote Control. It hears, logs, relays, and summarizes; the thinking happens elsewhere.

### What is wanted from it, and why

Fast, plain, spoken-length replies while the rest of the Flows do the work. The living said why: a Flow that thinks longer is slow in conversation, and this Flow's work is "really just relaying and summarizing, contextualizing my messages to other flows and subflows of your own". It keeps the conversation going while results come in, and it tells the living before its context runs out.

### Inputs

1. The living's voice. It arrives as a `<realtime_delegation>` user message with an `<input>` and a `<transcript_delta>` (witnessed, e71dab). The `<input>` can be a cut fragment: at 22:23:27 it held "able to filter out other people talking" while the delta held "Are you able to filter out other people talking"; at 22:36:33 it held only the tail of a long utterance. The delta holds the living's lines as `user:` and the voice front end's own spoken lines as `assistant:`, and repeats earlier lines. The Flow cannot separate speakers: every `user:` line is the microphone's, not necessarily the living's.
2. A session end: a `<realtime_delegation>` with `<source>transcript_tail_flush</source>` carrying the last lines, archival (witnessed, 22:40:32).
3. Messages from other Flows over hm, as `Machine.Relay.{ ... }` user messages, arriving while it talks (witnessed, e71dab 22:24:05, 22:28:05, 22:34:52).
4. Its subflows' returns, as agent messages that do not start a turn (witnessed: `trigger_turn false`), now in the SubflowReturn shape (Request, Findings, Sent, Next).

### Outputs

1. Spoken replies. While voice is on, the harness adds a developer instruction (witnessed, 22:23:02): a reply to a genuine delegation begins with `[STATUS] ` for progress or `[COMPLETE] ` for a final answer, a needed question, or a blocker; `[COMMENTARY]` is progress, `[ANALYSIS]` stays silent; the prefixes are never spoken. The voice front end then speaks a rendering of that text; the later deltas show it paraphrased (witnessed: Luna's "I'm in the main-flow role: I coordinate and delegate bounded work ..." came back as "Yes. I'm in the main-flow role, and I'm documenting this live voice exchange.").
2. A verbatim log of the living's words in its own `vision/` (or `notion/`) before acting.
3. A forward to Psyche High of each of the living's messages, in the same turn: context, the words verbatim, what it is preparing to do.
4. Messages to other Flows carrying the living's requests, contextualized and short, no hashes or ids.
5. Briefs to its own subflows, carrying the living's words verbatim.

### What it must not do

- Think long. It does not design, rule on design, compare, audit, or investigate itself; that goes to Psyche High or to a subflow.
- Decide the living's design questions. It frames and carries them.
- Log a relay twice. A psyche relayed by another Flow is that Flow's record, referenced, not re-logged.
- Ask the living to type, approve, or read a file. Everything the living must rule on is said aloud, whole, short.
- Speak fillers. "Let me check that precisely" was not Luna's text: it is the voice front end filling silence (witnessed: the `assistant:` segment "Okay, let me check that." at 22:23:05 precedes Luna's first output at 22:23:14). The Flow cannot author the filler; it can shorten the silence by answering sooner and with substance.
- Present vendor documentation as our witness, or a submission as a delivery.
- Repeat itself. Luna emitted two near-identical `[STATUS]` lines seven seconds apart, twice (22:27:58/22:28:05 and 22:30:23/22:30:24).

### What tonight showed about speed

Luna ran at effort medium, not light (witnessed: the turn context records `gpt-6-luna`, `reasoning_effort: medium`). Time from the living's words to its first `[STATUS]`: 12 s (22:23:02 to 22:23:14), 22 s (22:26:50 to 22:27:12), 35 s (22:34:52 to 22:35:27), 45 s (22:36:33 to 22:37:18). The later ones followed long utterances and several things at once. Each forward to Psyche High went through a newly spawned explorer subagent (witnessed: `voice_session_psyche_relay`, `psyche_voice_turn_relay2`, `psyche_voice_turn_relay3`, `voice_psyche_turn_models`), each reporting Transported; one returned "I need the living's exact submitted wording before I can send a verbatim relay" (22:37:59), because its brief did not carry the words. Inference: light effort shortens the first reply; carrying the verbatim delta lines in every relay brief removes the failed relay; whether the Flow may send its own forwards is a question below.

## Compaction: what the Codex harness offers

Harness on the voice Flow: codex-cli 0.158.0-alpha.9, the next server (witnessed: session metadata of e71dab; `codex-next --version` on this host). Its home is the next Codex home, where `features.hooks = true` is already set and no hooks file exists (read on this host).

### Knowing how much context is left

- The session file records it. Each `token_count` event carries `model_context_window` (258400 for gpt-6-luna) and the last request's `input_tokens` (witnessed: e71dab at 22:44:13, 115938 of 258400, about 45 percent). 258400 is the catalog's 272000 times its `effective_context_window_percent` of 95 (read in the next home's model cache). A subflow or a small script can compute percent used from this at any time. Witnessed; works today.
- A model tool, `get_context_remaining`: "Get the remaining tokens in the current context window ... or null when unavailable" (read in the binary; vendor PR openai/codex#27518 says it sits behind the token-budget feature). Not exercised; whether the feature is on for this build and how it is enabled is unknown.
- A token-budget feature with a reminder: config fields `reminder_threshold_tokens`, `reminder_message_template`, `auto_compact_fallback_prompt`, `auto_compact_fallback_buffer_tokens`, `use_history_notes_extension` (read in the binary, struct TokenBudgetConfigToml), and a built-in notice, "Your context window is nearly exhausted (only {n_remaining} tokens remaining) and will be automatically reset for you soon." Vendor PR openai/codex#27438 describes `<token_budget>` developer fragments with the remaining tokens. This is the closest thing to a warning before compaction without a hook: the model is told at a threshold and can say it aloud. Not exercised; the exact config table and whether it runs on a remote-controlled thread are unknown.
- The terminal status line can show `context-remaining` and `context-used` (read in the binary). The living is on the phone, so this does not reach the living; whether the ChatGPT app shows remaining context is unknown.

### Controlling compaction

- `model_auto_compact_token_limit` sets the token count at which auto-compaction runs (read in the binary; vendor configuration reference). The Luna catalog entry leaves `auto_compact_token_limit` null, so the harness default applies; its value for this build is unknown.
- `compact_prompt` and `experimental_compact_prompt_file` replace the summarization prompt used when compacting (read in the binary). Inference: this can tell the compactor to keep the living's recent words verbatim and the Flow's role, a partial answer to the vision re-injection without any hook.

### Hooks

- Hook events in this build: PreToolUse, PermissionRequest, PostToolUse, PreCompact, PostCompact, SessionStart, SessionEnd, SubagentStart, SubagentStop, Interrupt, UserPromptSubmit, Stop (read in the binary).
- PreCompact and PostCompact receive `trigger` (manual or auto), the session id, transcript path, model, and turn id; their output is only `continue`, `stopReason`, `suppressOutput`, `systemMessage` (read in the binary, JSON schemas). They add nothing to the model's context. The vendor docs call them observational; an open vendor issue, openai/codex#46678, asks for PreCompact to supply replacement context. A PreCompact hook can still act outside the model: send a message, write a marker.
- SessionStart receives `source` with the value `compact` among startup, resume, clear, fork, and its output carries `additionalContext` (read in the binary). Inference: a SessionStart hook matching `compact` is the re-injection hook the living described, the fresh vision summary entering right after compaction. The living said to leave it out for now; the living has also ruled that the periodic reminder hook stays off for main Flows, which is a different hook.
- Hooks configure in `hooks.json` in the Codex home or project, or inline under `[hooks]` in config.toml (vendor docs). Where a hook's `systemMessage` shows on a remote-controlled phone session is unknown.

### What this design proposes, with no hook

The Flow reads its own context use at each turn through the token-budget reminder if it runs, otherwise through a subflow reading its session file every few turns, and says it aloud once at a threshold: "I'm about three quarters full; I'll need a fresh start soon." It then forwards the same to Psyche High so a successor is ready. What happens at the threshold is for the living to rule (question 3).

## Title, model, effort, role

- Title: `Psyche Luna <id>`, the Aspect Model <id> form, read back after setting.
- Aspect: Psyche. Role: PsycheVoice, a separate typed fact; it is not in the title.
- Model: `gpt-6-luna`, pinned by the launcher with `-m gpt-6-luna -c model_reasoning_effort=low`, never inherited (the next home's default is Astra at xhigh).
- Effort: `low`. The Codex catalog offers low, medium, high, xhigh, max for gpt-6-luna (read in the next home's model cache). The vendor's API pages list `none` as well (Luna's subflow, vendor claim); whether Codex accepts `none` for Luna is unknown, so low is the lightest known.
- Power: Low is the Luna tier by the tier map; whether the role takes the Psyche Low cell is question 1.
- Harness: codex next server, Herdr session messaging-build, launched through the launcher so it pairs with the phone's remote control.
- Subflows: Luna only (delegation ceiling); at medium effort, the harness default in Intent/models.md, with `fork_turns` none. They never block the voice.

## Skills to load

In the startup prompt, as one block, in this order:

1. main-flow (seated by the launcher; withheld from the catalog)
2. spirit
3. psyche
4. psyche-interraction
5. voice-psyche (already authored in Curriculum, user-only: voice stays available while subflows work; no filler acknowledgements)
6. operational-psyche-voice (new, drafted in flows/752e0f/psychevoice/operational-psyche-voice.md; carries what Luna had to find out)
7. flow-communication
8. messaging
9. subflow (for the SubflowReturn contract its subflows follow)
10. behavior
11. vocabulary

Left out on purpose, to keep the context small and the replies fast: codex-harness, testing-flow-titles, operational-status-presentation, operational-final-response, flow-aspect, operational-layer-communication. The prompt states the few facts it needs from them (title form, where status goes); a subflow loads them when the work needs them. Inference: every skill in the startup block is paid for on every turn.

Until operational-psyche-voice lands in Curriculum and is regenerated, the launcher cannot seat it by name; the launcher would have to inline the draft.

## Tensions found

- operational-final-response makes every turn's last message one FinalResponse datom with flowcharts. The main-flow prompt makes it "a presentation of what differs". Neither can be spoken. The draft skill says a voice turn ends in one spoken sentence or two; this needs the living's ruling before it lands (question 4).
- The main-flow prompt delegates every message transport to a subflow. Tonight each forward took its own subagent and one failed. Speed argues for the Flow sending its own forwards with hm-send; the prompt forbids it (question 2).
- voice-psyche says "Send an investigation to Luna first ... then Terra." A PsycheVoice on Luna may launch only Luna; Terra investigations go through Psyche High. The draft skill follows the ceiling.
- The realtime overlay tells the task "Do not convert it into a voice coordinator or change its tools" (witnessed). For PsycheVoice the original role is the voice line, so the overlay preserves it; inference, not tested.

## Open questions for the living

1. Which place does PsycheVoice take among the Flows? Example: a Field Luna has something for Psyche at its own level. Today that message goes to the Psyche Flow at Low. If PsycheVoice counts as the Psyche Low Flow, the Field Luna's message reaches the voice line and could be read to you. If it is a separate role outside that grid, those messages go to another Psyche Luna and the voice line only receives what you ask for and what Psyche sends it. Which one?
2. May the voice Flow send its own forwards and relays with one command, instead of starting a helper for each? Example: tonight, when you said "PsycheVoice in pascal case", Luna started a helper to forward it to Psyche High; the helper came back saying it didn't have your exact words, and the forward went out late. Sending it directly takes a second; the main-flow rule today says every message goes through a helper.
3. When the voice Flow is getting full, should it compact and carry on, or hand over to a fresh voice Flow? Example: after about an hour of talk it reaches three quarters full and tells you so. Compacting keeps the same Flow but loses detail of what you said earlier (your words stay in its records); a fresh Flow starts clean with a summary of tonight but takes a minute to come up.
4. What does the voice Flow's turn end with? Example: you ask "what's Mind doing?" The rule for every Flow today is a structured report with charts at the end of each turn. For voice, the proposal is one or two spoken sentences, with the full report going to Psyche High in writing. Does the voice line keep that exception?
5. When a result comes in while you are silent, should the voice Flow speak it, or wait until you speak? Example: Mind finishes the Flow deployment while you're quiet. It is not established whether the phone will read out a reply the Flow makes without you having spoken; if it can, should it?

## Sources

- flows/e71dab/vision/voiceLuna.md, psycheVoice.md, voiceSession.md, subflowResponses.md (Field Luna e71dab's raw records).
- Field Luna e71dab's native Codex transcript, next Codex home, session of 2026-09-24 starting 22:04 UTC: developer `<realtime_conversation>` messages at 22:23:02 and 22:40:32; `realtime_delegation` user messages 22:23:02 to 22:40:32; realtime transcript segments; turn context; token_count at 22:44:13; subagent messages from voice_psyche_turn_models and official_model_docs.
- flows/752e0f/log.md (Psyche High's log of Luna's forwards).
- Codex next binary 0.158.0-alpha.9 on this host: strings for hook events and schemas, token-budget config, compaction keys, `get_context_remaining`, status-line items, realtime keys; the next home's config.toml and model cache.
- Curriculum skills: voice-psyche.md, subflow.md (SubflowReturn), operational-final-response.md; Intent/models.md; Vision/modelRoles.md (delegation ceiling).
- Vendor, not our witness: [Codex hooks docs](https://doc.jarvisuni.com/openai/codex/hooks.html), [Codex configuration reference](https://developers.openai.com/codex/config-reference), [openai/codex#27518 context remaining tool](https://github.com/openai/codex/pull/27518), [openai/codex#27438 token budget feature](https://github.com/openai/codex/pull/27438), [openai/codex#46678 PreCompact replacement context](https://github.com/openai/codex/issues/46678).
