# Fable refresh authority audit: what the living authorized

Audit subflow of Psyche Opus dc53b4, at c56100's request, 2026-09-27. Read-only. Nothing was launched, edited (except this file), stopped, routed, sent, or used as a credential. Messaging is blocked on this host, so nothing was sent.

Times are transcript timestamps in UTC. The living's local zone is America/Mexico_City (UTC-6).

## What was built on, and what is fresh

Taken from Fable 8904b1's work and re-checked against the primary records:
- `flows/8904b1/reports/refresh-order-records.md`: 1ac573 reap records (09-17/18), e167d8 refresh hook (09-26), f55ec8 layers (09-16), the 93ba9f and b7ba00 records (09-26), and the refresh and main-flow skill text.
- `flows/8904b1/log.md`, entries from "context audit; refresh asked" through "successor draft revised": the 56ae53 and c56100 messages, and c56100's exact-word provenance for the >200k quote and the e51411 quote.
- `flows/8904b1/reports/psyche-seat-successor-plan.md` and `receipts/psyche-seat-successor-ground.md`: context sizes (Fable about 207k tokens with the status line at 21%, which implies a window of about 1M), and the finding that Flow has no rule against two seats holding one role.

Fresh in this audit (8904b1's search did not report these):
- The living's raw turns in the transcripts of 93ba9f, e167d8 and 56ae53, with exact timestamps. They include three utterances that are absent from 8904b1's report: "Let's pass this over to Luna Field and figure out if she can't, why." (17:42Z), "Yeah tell Luna to make sure we reaped and archived all the old flows." (17:50Z), and "Let's stop this Fable high ... to the right Fable." (18:10:26Z).
- The living's permission to start a Fable successor (e167d8, 15:57Z). A later census showed that this crossover produced the three live Fables behind the alarm.
- The earlier threshold records (6cc91b 09-14, f55ec8 09-16, b80e55 09-20). They correct 8904b1's finding that no record in the living's words gives 200k.
- The earlier reap and authority records: cf3553 (09-18), b81560 (09-19), b05237 (09-18/19), 33ba2b (09-18) and 5f38bc (09-24).
- Curriculum history: the "crossover-only / explicit authority" clause of the refresh skill entered on 2026-09-18 (61cdc53, "Add Field Astra and Sol refresh succession"). It came from an operational interpretation, not from the living's words.
- Where c56100's "duplicate WORKING roles" wording comes from.

## 1. The living's words, by date (verbatim)

**2026-09-14, STT, to 6cc91b** (`flows/6cc91b/vision/flowLifecycle.md`):
> At a certain maximum, at 60%, the flow basically has to change over, but it can restart if the conversation shifts dramatically. It can restart and repopulate itself with a better context for that emphasis in a fresh flow, starting from having around 200,000 tokens of context, right? 20, 30% for Claude, and I don't know what that is for Astra.

and:
> The old flow will wind down and maybe be archived or something ... I guess a concluded thread could be reawakened to ask a question if we want, but maybe because of how long the cache lasts, it would be expensive to do that, so it's better not to.

**2026-09-16 evening, typed, to f55ec8** (`flows/f55ec8/vision/flowRefresh.md`):
> You should make it a good practice to start when you're getting to 30% of your context as a Fable agent, right? That's 300,000 tokens. That's a lot, so it's better to restart with a clean.

**2026-09-17, typed, to f55ec8, at 512k** (same file):
> And you need to restart yourself. You're way too big now. ... It costs too much money to run you now.

**2026-09-17, to 1ac573** (`flows/1ac573/vision/operational-reapReplacedSessions.md`):
> When a session gets replaced, it has to be reaped so it doesn't keep getting messages. ... when we refresh a flow, it takes out that end from receiving messages, right?

**2026-09-18, to Field Sol 33ba2b** (`flows/33ba2b/vision/operational-fieldRefreshSuccession.md`). The source words concern only the Field seats:
> I would like a field Astra and a new field Sol for you. ... Make that core skill vision for refresh.

The record's next sentence, "The predecessor stays crossover-only ... it is not automatically retired or unrouted", is labelled "Operational interpretation". It is not the living's words.

**2026-09-18, living, primary conversation** (`flows/cf3553/vision/operational-fieldWorkersAreReapers.md`, `operational-fieldReapingJudgmentAndExecution.md`):
> The field workers are the reapers. ... The field is what maintains the field healthy, which means also killing off, cutting off the dead pieces.

> Well, you can always use your best judgment to see that something has replaced something. Astro can do that, right? Given the right context, even Sol can make the right call, or you can use Opus. ... You could have a field old Opus that takes care of judging if something is dead or not by investigating the transcript ... The authorization can be given because the old Opus said yes, and the field Luna can now reap because the job is trivial, right?

**2026-09-19, relayed verbatim by Field Astra cf3553 to b81560** (`flows/b81560/vision/operational-reapingOnRefreshAndFlowEndHook.md`):
> Why are you sending messages to flows that are over? You're wasting our power waking up flows that should be reaped. ... Dead sessions should basically be ended immediately.

> your reaping is too conservative. get luna to reap. you havent even reaped your own ancestor, which is pretty lame

> Whenever you refresh a flow, you need to reap the ancestor, right?

**2026-09-19, direct to b81560** (`operational-retiredResponseAndReaping.md`):
> If it's a retired response to a flow that has a successor, then this means that it needs to be reaped.

**2026-09-19, direct to Psyche Sonnet (subflow of b05237)** (`flows/b05237/vision/operational-datomFinalResponseLowJudgmentReap.md`):
> if a flow gives its last final response and it's clearly this Datom type final response ... then we don't need a lot of judgment to reap.

**2026-09-20, to b80e55, input mode not established** (`flows/b80e55/vision/refreshThresholdAndCacheSnapshot.md`):
> You can restart a flow, especially if it's above 30%, like 200,000 to 300,000 tokens, which is different for Claude, right? 200K to 300K is like a refresh ...

**2026-09-24, STT, to Field Astra 5f38bc; reconstructed** (`flows/5f38bc/vision/flowLifecycle.md`):
> No, I don't even know why there were two fields sold. I only want one, obviously.

**2026-09-26 15:57:44Z, to e167d8** (e167d8 transcript `e167d857-…jsonl:2859`, queued user turn):
> I don't know what the registration rule you're talking about is but you can start a Fable successor. Let's use the new Flow, 0.16 ...

This is what led to b7ba00 being launched as a crossover successor ("took over from 38de5b (crossover, stays for evidence)", `flows/e167d8/log.md:192`). The census that followed (`log.md:213`): "three Fable seats — 38de5b medium (working), da88cf HIGH (five background tasks), b7ba00 HIGH (working)".

**2026-09-26 16:10:18Z and 16:11:43Z, STT, to e167d8** (`e167d857-…jsonl:3115, 3140`). The records give "~14:10/~14:15", which matches neither UTC nor local time.
> Okay we have a lot of problems right now. We have two Fable flows running, which is costing us a lot of money, and one of them was on high. Somebody is going to be running to fuck the mess to fix their fuck-up and we need to close these sessions when they're done. This needs to happen right now.

(`flows/e167d8/log.md:200` gives "[fix] the mess". The raw STT reads "fuck the mess".)
> ... there's more than one Fable ... We have to take urgent action to stop bad model flows from being started or from continuing on when they should be stopped.

**2026-09-26 17:42:16Z, to 93ba9f** (`93ba9ff6-…jsonl:297`; records: `flows/93ba9f/vision/automation.md`, `sessionClosing.md`). The final sentence below is fresh:
> Psyche, your predecessor, Flow, says closing me is up to you, which is nonsense. Nothing is up to me. Everything is being automated. ... I'm not going to close or start anything or type anything anywhere ever. No one is. The user interface is going to be Unity and these harnesses are just going to be a background mechanism. ... I'm not going to close anything. ... Let's just teach the system to close panes, to close sessions itself. Let's pass this over to Luna Field and figure out if she can't, why.

**2026-09-26 17:48:39Z, to 93ba9f** (`:453`; `flows/93ba9f/vision/flowLaunching.md`):
> Yeah I never said freeze all launches. Everything that has a big context should be refreshed and everything that has been abandoned needs to be reaped. I've been emphasizing this all along. Sometimes it's not that all launches are frozen; it's that somebody launched too many flows that were on the same role and then launched the flow with too high an effort. I said this is wrong. We need to make sure it doesn't happen again so let's make sure the code makes sure it doesn't happen again.

**2026-09-26 17:50:22Z, to 93ba9f** (`:485`; in `flows/93ba9f/log.md:15`, not in any vision file):
> Yeah tell Luna to make sure we reaped and archived all the old flows.

**2026-09-26 18:10:11Z and 18:10:26Z, to 93ba9f** (`:714`, `:736`; the second is only in `flows/93ba9f/log.md:24`):
> I think I still see a fable on high effort that still seems to be working. Give everybody the authority to come down on things like the high-effort model and make sure these flows are stopped and that all of their context is given to whoever carries the torch for them. If there isn't one then they have to restart a new flow. Let's keep field Luna on that. She has all the authority to stop and start flows. As long as she's told, she doesn't have the authority to decide. She has the authority to do it once she's told to do it.

> Let's stop this Fable high that's burning a hole in our pocket and pass everything over that he was doing to the right Fable.

(At 18:13:23Z the living stood down on this: "Okay well, that flow is on medium ...".)

**2026-09-26 18:14:55Z, to 93ba9f** (`flows/93ba9f/vision/primarySeats.md`):
> We should make it clear that models should refrain from talking to the primary models. They should usually aggregate some thoughts together and investigate before talking to it.

**2026-09-26 22:24:48Z and 22:26:16Z, typed, to Mind Sol 56ae53, after the power failure** (`01a0de4c-…5366f.jsonl:256, 303`; `flows/56ae53/log.md`, a working log):
> We're just in recovery mode ... If you find a flow that's old, above 200,000 tokens, or especially above 200,000 tokens, even Claude, you should just get maybe a sonnet agent to put together a restart prompt from the transcript of that abandoned session and refresh it. I think it is better. Just give it a bunch of fresh psyche rather than reanimate a 200,000- to 300,000-token session.

> We should have: - the two Psyki flows: Fable and Opus, primary and secondary ...

**From 2026-09-26 22:30Z through 2026-09-27 09:31Z** I found no further words of the living on refresh, Fable succession, reaping or retirement. I searched the transcripts of 56ae53, c56100, 9ac67c, 6fe957, 184bd8, 139366, 8904b1, 38f337 and dc53b4. Every later statement on the subject is a machine relay or a machine synthesis.

## 2. What the living authorized (grounded in the words above)

- **Refreshing a large context.** Authorized as a standing principle: "Everything that has a big context should be refreshed" (09-26, 17:48Z). The living gave the numbers repeatedly and lowered them over time: 60% (09-14), then "30% ... as a Fable agent ... 300,000 tokens" (09-16), then "above 30%, like 200,000 to 300,000" (09-20), then "above 200,000 tokens, even Claude" (09-26, said of old or abandoned sessions during recovery).
- **Launching a Fable successor.** On 09-26 the living said "you can start a Fable successor" (15:57Z) for that day's seat. No record found authorizes a successor to 8904b1 by name. Applying the principle to 8904b1 is an inference. It is a strong one for size, since 8904b1 was at about 245k by Mind Sol's claim.
- **Effort.** Medium: "We haven't designed a flow that uses high effort so there shouldn't be any launched."
- **Number of seats per role.** One Field Sol ("I only want one, obviously", 09-24). The recovery target counts one Fable ("the two Psyki flows: Fable and Opus"). "Pass everything ... to the right Fable" names a single Fable. "Too many flows that were on the same role ... I said this is wrong ... make sure the code makes sure it doesn't happen again."
- **The predecessor after a refresh.** It stops receiving messages and is reaped: "when we refresh a flow, it takes out that end from receiving messages" (09-17). "Whenever you refresh a flow, you need to reap the ancestor" (09-19). "Dead sessions should basically be ended immediately" (09-19). "We need to close these sessions when they're done. This needs to happen right now" (09-26). The living never said the predecessor must be killed before the successor starts. The living has twice asked that a concluded flow not be woken ("better not to", 09-14; "I don't want to reawaken an old flow just to tell it that it has a successor", fd0f97).
- **Who reaps or retires.** Field does. Field Luna executes: "get luna to reap" (09-19); "the field Luna can now reap because the job is trivial" (09-18); "She has all the authority to stop and start flows ... once she's told" (09-26). Judgment that "something has replaced something" may come from Field Astra, Field Sol or a Field "old Opus" (09-18). Little judgment is needed when the last response is a FinalResponse datom (09-19). On 09-26, "Give everybody the authority to come down on" high-effort flows. The living exercises no closing authority personally: "Nothing is up to me ... Let's just teach the system to close ... Let's pass this over to Luna Field."

## 3. What skills and seats have ruled (not the living)

- **Refresh skill** (Curriculum `skills/refresh.md`): "sixty percent", and "do not restart below twenty percent". The clause "The predecessor is crossover-only ... never kill, retire, conclude, silence, or automatically remove its routing as a side effect of refresh. Explicit authority is required for any retirement or routing withdrawal" was introduced on 2026-09-18 (commit 61cdc53). Its source is the 33ba2b operational interpretation of the Field-seat refresh. The "sixty percent" figure matches the living's 09-14 words, which were later lowered. `Vision/flowNexus.md` holds the reviewed distillation "A replaced session is reaped by the refresh itself ... a dead end is never left registered and addressable", which sits in tension with the skill clause.
- **8904b1**: "Never two Fables" (its own sentence, now withdrawn). Crossover with the predecessor silent. "The alarm was about seats still receiving messages". 8904b1 marked that last sentence as its own inference.
- **56ae53** (to c56100 and 38f337, 08:53Z): "latest ruling: 'I never said freeze all launches. Everything that has a big context should be refreshed,' with objection to duplicate working roles and high effort. The earlier direct >200k refresh instruction applies to Fable 8904b1. Canonical refresh allows a medium successor launch with old Fable silent/crossover-only ... perform final route reap only under supported refresh automation or explicit authority." It cites as sources `flows/93ba9f/vision/flowLaunching.md` and `flows/56ae53/log.md`. **No new utterance of the living lies behind it.** The word "working" in "duplicate working roles" is 56ae53's. The living said "too many flows that were on the same role". Applying the rule to 8904b1, and the crossover and reap terms, come from 56ae53 and the refresh skill.
- **c56100**: "the latest relayed living ruling supports refreshing the large-context Fable, while prohibiting duplicate WORKING roles". This passes on 56ae53's synthesis.
- **38f337's draft at 2aa16efa** (`flows/38f337/successor-prompt-fable.md`, `handoff-fable.md`). It presents 56ae53's synthesis as "the living's ruling relayed via 56ae53". That includes "A medium-effort successor launch is authorized" and "The old Fable is NOT stopped before the launch". The handoff still states 8904b1's inference as fact: "The alarm was about seats still receiving messages ... not about two seats merely co-existing during a crossover." It dates the alarm "~14:10/~14:15", while the transcript gives 16:10–16:11Z. Its reap gate says "Who performs the reap is not yet authorized". The living's words above name the performer (Field and Luna) and leave only who tells Luna.

## 4. Resolving the three 26 September conflicts

**(1) Duplicate working roles (two Fables).** The living's words object to more than one seat on a role: "too many flows that were on the same role", "more than one Fable", "two Fable flows running, which is costing us a lot of money", "I only want one" (Field Sol). The word "working" is 56ae53's gloss. Nothing the living said draws a line between a working duplicate and an idle one. The only case the living met in fact was a crossover. b7ba00 was launched under "you can start a Fable successor", with 38de5b and da88cf kept as "crossover, stays for evidence". Both predecessors were still doing work (38de5b running merge subflows, da88cf with background tasks at high). The living's response was "close these sessions when they're done. This needs to happen right now."
Verdict: the living has not forbidden a brief overlap while a successor starts. The living did forbid predecessors that keep running, and asked for them to be closed once done. They are also not to be woken: messages wake them, and "we need to close these sessions when they're done" and "Dead sessions should basically be ended immediately" apply. A "silent crossover" that lasts until some later, unnamed authority acts is the skill's design, and the 09-26 alarm arose under exactly that design. The words above support the overlap only as far as the successor's readiness, followed promptly by the predecessor's close.

**(2) Refresh at large context (>200k) vs the 60% rule.** Resolved in favour of the living's later words. The 60% figure is the living's own from 09-14. The living lowered it for Fable to "30% ... 300,000 tokens" (09-16), then to "above 30%, like 200,000 to 300,000" (09-20) and "above 200,000 tokens, even Claude" (09-26). On 09-26 the living also said "Everything that has a big context should be refreshed." The skill text was never updated. 8904b1 at about 245k is past the 200k word and below the Fable-specific 300k/30% word. Both are the living's. The later and more general 09-26 wording favours refreshing. The skill's "do not restart below twenty percent" does not block it, since 8904b1 is at about 25% of a window of about 1M.

**(3) Who may retire a predecessor or withdraw its route.** Mostly resolved; one gap is left. 8904b1 read "Luna stops and starts once told" and "Nothing is up to me ... No one is" as a tension. The full 17:42Z turn removes it. "No one" means no human types into harnesses. The same turn says "Let's just teach the system to close panes, to close sessions itself. Let's pass this over to Luna Field". Eight minutes later it says "tell Luna to make sure we reaped and archived all the old flows". Together with 09-18 and 09-19, the living's allocation is this:
- A Field judge decides that "something has replaced something": Field Astra, Field Sol or a Field old Opus. Little judgment is needed when the last response is a FinalResponse datom.
- Field Luna executes the stop, reap and archive once told.
- The refresh should reap the ancestor.
- "Everybody" may call down a high-effort flow.
The gap: the living has not said who "tells" Luna when the predecessor is a Psyche seat (Fable). It could be the Field judge, the launching seat, or Psyche. On 09-26 a Psyche seat (93ba9f) did the telling, and the living accepted it. The skill's "explicit authority" clause names no holder and has no verbatim ground found.

## 5. Unknowns

- No words of the living name 8904b1, or ask for its successor, after the power failure. Applying "big context should be refreshed" and ">200,000 tokens" to it is inference. The 22:24Z sentence speaks of "that abandoned session", and 8904b1 is live.
- Who tells Luna for a Psyche seat (see (3)).
- How long an overlap the living tolerates between successor start and predecessor close. The living has given no duration.
- Whether "take that end out of receiving messages" (09-17) means before the successor is ready or after. The words do not say.
- The "~14:10/~14:15" times in the e167d8, b7da5d and 56ae53 records do not match the transcript (16:10–16:11Z, 10:10 local).

## Sources

- `/home/li/wt/primary/56ae53/flows/8904b1/reports/refresh-order-records.md`, `reports/psyche-seat-successor-plan.md`, `receipts/psyche-seat-successor-ground.md`, `log.md` (entries 2026-09-27 from "the worker's effort" to "successor draft revised")
- Transcripts: `/home/li/.claude/projects/-home-li-primary/93ba9ff6-d24a-4dd0-a5c7-f98fab5ca9de.jsonl` lines 297, 453, 485, 714, 736, 770, 815; `…/e167d857-17e7-441b-b38b-54941a77a77a.jsonl` lines 2859, 3115, 3140; `/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T09-18-59-01a0de4c-554d-7343-bbc5-e4256ae5366f.jsonl` lines 256, 303; c56100 `rollout-2026-09-26T20-11-11-01a0e0a1-7075-7cc2-928d-13fc56100504.jsonl` line 1338; 38f337 `38f33758-…jsonl` lines 1302, 1320
- Records: `flows/6cc91b/vision/flowLifecycle.md`, `flows/f55ec8/vision/flowRefresh.md`, `flows/b80e55/vision/refreshThresholdAndCacheSnapshot.md`, `flows/1ac573/vision/operational-reapReplacedSessions.md`, `flows/33ba2b/vision/operational-fieldRefreshSuccession.md`, `flows/cf3553/vision/operational-fieldWorkersAreReapers.md`, `flows/cf3553/vision/operational-fieldReapingJudgmentAndExecution.md`, `flows/b81560/vision/operational-reapingOnRefreshAndFlowEndHook.md`, `flows/b81560/vision/operational-retiredResponseAndReaping.md`, `flows/b05237/vision/operational-datomFinalResponseLowJudgmentReap.md`, `flows/fd0f97/vision/flowLifecycle.md`, `flows/5f38bc/vision/flowLifecycle.md`, `flows/93ba9f/vision/{flowLaunching,automation,sessionClosing,primarySeats}.md`, `flows/93ba9f/log.md` lines 15, 24, `flows/b7ba00/vision/modelFlows.md`, `flows/e167d8/log.md` lines 191–213, `flows/56ae53/log.md`, `flows/56ae53/vision/model-flow-emergency.md`, `Vision/flowNexus.md`
- Skill text as written-rule evidence: `.claude/skills/refresh/SKILL.md` at primary main; Curriculum `skills/refresh.md` history (61cdc53 2026-09-18, d3ea294 2026-09-24)
- Sonnet's draft: `flows/38f337/successor-prompt-fable.md`, `flows/38f337/handoff-fable.md` at 2aa16efa
