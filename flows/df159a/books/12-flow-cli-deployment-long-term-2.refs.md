# References for «Flow: CLI, deployment, long term — second edition»

Unrendered. Beside the source `12-flow-cli-deployment-long-term-2.md`; never passed to the builder.

## The edition

Second edition of https://claude.ai/artifact/KqGmvFzr4VAqEeCA4jYMmA (Version 3, version id 1791948553-4234; source `12-flow-cli-deployment-long-term.md`). Proposals 1 and 3 approved on 2026-10-14 (15:15 «Yes this is good.», 15:16 «Yeah this is good, especially the later part.»), landed by another subflow into psyche-context: vision-flow L22 (anybody may call Flow; a flow refreshes itself safely) and L26 (Flow exposes the harness; Flow first). Proposal 4 rewritten here. Proposals 2 and 5–13 unruled, not carried.

## The comment that changed Proposal 4

2026-10-14 15:18, `flows/df159a/vision/flow.md` (also `flows/da2038/vision/flow.md`), STT, book comment, thread 858cdedf-7fcd-48f6-a7c3-3616049132d6, anchored at «A request that cannot be delivered tries a higher power in its own aspect: the layer above, and when nothing is higher, …»; relayed by Psyche Flow Secondary da2038:

«We have old vision that is now obsolete in there, with a conflicting vision. The long-term vision is that the flow is started if it's needed, which means it doesn't matter if it's running or not. Even if it doesn't have any working transcript to reawaken, then we just feed it the context modules that this meta flow is supposed to have, along with the prompt that it's supposed to be getting now.»

## Superseded: the first edition's base

2026-09-24 14:31Z, `flows/d8df70/vision/messaging.md`, book comment (input mode not stated in the record) on «What Waits for the Living», question 5; relayed at `flows/836818/vision/flowNexus.md` L33:

«If a message can't be delivered, then we try a higher power. If Psyche Medium is not reached, we try Psyche High and if there's nothing higher then we try lower. The message returned for the caller will say what happened but we'll have a bunch of rules.» «Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial.»

Called «obsolete» by the 2026-10-14 comment. The higher power, the lower one and «crucial» stand in no skill; nothing to strike for them.

## Records weighed, on the same subject (the latest carries the strongest weight)

- 2026-10-14, `flows/d68c82/vision/flow.md` L114–128, STT, book comments on «Situation, 14 October» (no time stamped; order against 15:18 unknown): «in the long-term vision, if a flow has just been sitting idle for some time, we can turn off its harness. When the system is properly configured, if a request needs to reach a certain flow (which is not up and running in a harness), then the flow would just restart that flow or start a fresh one.» — current: his word on the choice-10/11 fork (restart, or a fresh one); «restarted» in the sentence is his.
- 2026-10-14, `flows/d68c82/vision/flow.md` L95–101, STT: «You have a default prompt, basically a default startup context» — current, supporting: the prompt at start.
- 2026-10-13T17:47, `flows/d68c82/vision/flow.md` L8–12, STT: per-metaflow EDN configuration naming its context modules — current, supporting: a metaflow has its context modules.
- 2026-10-07 18:32, `flows/f5a6e9/vision/flow.md`, STT, book comment on «Flow and the metaflow», relayed by Field db38f8: «It's a Metaflow that might go to sleep but can always be woken in the sense that if a message is intended for it, flow would automatically... This isn't intended for the first version but eventually it would just trigger the flow to be spawned with the right context modules depending on the message.» — current: the same line, named long-term.
- 2026-10-07, `flows/d4ae97/vision/contextModules.md`, book comment (input mode not stated in the record) on «Flow and Message» 2nd edition: «there's going to be a placement for that prompt, that brief, which is essentially the first task of that flow» — current: the prompt fed at the start.
- 2026-10-08, `flows/d4ae97/vision/messenger.md`, STT: «Different messages will have different flow-waking effects.» — current, landed at vision-flow L24.
- 2026-10-11 20:23, `flows/875960/vision/flow.md` (also `flows/9519a1/vision/flow.md`), STT, relayed by 9519a1: «If that topic is needed again, then we know what to wake it, what to start it, what context modules to start it with, along with whatever new input is coming in that warrants restarting the flow.» — current, landed at vision-flow L20.
- 2026-09-14, `flows/6cc91b/vision/flowLifecycle.md`, STT: «I guess a concluded thread could be reawakened to ask a question if we want, but maybe because of how long the cache lasts, it would be expensive to do that, so it's better not to.» — older; kin: a fresh start over a reawakening.
- 2026-10-07, `flows/6aa08d/vision/fieldStack.md` and 2026-09-19, `flows/b81560/vision/operational-verticalRoutingThroughPsycheFirst.md` (the first edition's other sources) — on the vertical route, not on starting; stand outside this proposal.

## Landed lines touched

- vision-flow L20 (a topic is bound to its context modules, so Flow knows what to start it with), L24 (a metaflow idle is woken by a waking request): kept; the sentence is added to L24.
- vision-model-roles L51–55 (routing advances to the next running layer; a Tertiary may reach the Primary when the Secondary is not running) and L61–69 (missing or unavailable needs fresh evidence; no eligible cell yields an undeliverable result; a fallback to another layer): landed 2026-10-12 (psyche-context commit 29119ab «Align model skills with the layer table»); no record of his found behind «next running layer» in `flows/*/vision/`. Struck as the reaching-only-a-running-flow the comment calls obsolete; choice 9 keeps them marked short-term.
- vision-messaging: no line on reaching a flow or escalation; choice 5 offers it as the landing.

## Behavior fix: existing line missed, none proposed

The stale base reached the first edition because later records on the same subject were not weighed against the 2026-09-24 words. Existing lines already require it: compensation-book-crystallization L12 («A proposed statement is drawn from the living's records read whole, with their exceptions and later statements on the same subject.», `field-context/skills/compensation-book-crystallization.md`) and knowledge-psyche L70 («A later explicit correction on the same subject carries the strongest weight.», `mind-context/skills/knowledge-psyche.md`) with L78 («check before assuming»). No new line proposed.

## Machine readings in the proposal

- «with a working transcript, its flow is restarted from it»: his «Even if it doesn't have any working transcript to reawaken» (2026-10-14 15:18) with his «restart that flow or start a fresh one» (d68c82, 2026-10-14); choice 10 keeps it, choice 11 keeps only the fresh start.
- «the metaflow's context modules»: his «the context modules that this meta flow is supposed to have».
- The vision-model-roles rewrites keep only what his words give: a layer not running is started, so the adjacent layer is reached; the machine routing words of commit 29119ab (busy eligible, resolve before each attempt, reconciled) are struck, not re-proposed.

## Review

Review subflow (2026-10-14) against the rules: passed lines-only form, module-line matches (diff clean against the authored files), figure width and title; found the unweighed d68c82 2026-10-14 record (added above), machine words re-proposed green in the L61–69 rewrite (now struck only), «the request does not disappear» (dropped), and «reawakened» beyond his «restart» (now «restarted»). Its remaining findings asked for his dated words to open the forks; superseded by the living's rule of the same day that the rendered book carries no quote or provenance.

## Witnessed

Checker `node tools/book-check.mjs` passed; built with `bb tools/book-build.clj`; word-level marks confirmed on the built page (the L24 pair renders as one line with only the added sentence in `<ins>`).

## Version 3 revision (Secondary audit of Version 2)

Removed from the rendered page, kept here:

- Edition preamble: second edition of https://claude.ai/artifact/KqGmvFzr4VAqEeCA4jYMmA (Version 3), carrying only what his 2026-10-14 comments changed; Proposals 1 and 3 approved and landed; the edition fact stays in the title only.
- Default (no number): the sentence lands in vision-flow L24 — starting a flow and delivering to it are Flow's (vision-flow L8–10, L20, L24); vision-messaging holds the message's form, priority, per-harness delivery and witness. Choice 1 is the vision-messaging landing: the request that finds no flow running is the message's subject.
- Choice 2 (model-roles lines stand, marked short-term): intent-psyche L10, «A short-term vision is named so; an unmarked vision is long-term.»; the lines describe the routing in place today until start-on-demand is implemented.
- Choice 3 (machine choice): his words name no layer routing; the sentence «A layer a request needs is started whether or not it is running.» is his vision-flow line said in vision-model-roles terms, offered because L52–55 and L62–69 lose their vertical-route sentences when struck.
- Choice 4: his «Even if it doesn't have any working transcript to reawaken» (2026-10-14 15:18) with d68c82 2026-10-14 «restart that flow or start a fresh one»; the default carries only the case he names; «reawaken» is his word, «restart» no longer used.
- Dropped: the former choice 7 (the higher-then-lower escalation surviving for a metaflow Flow cannot start) — it revived what he called obsolete; the former choices 1–3 (land / amend / drop) and the restating choices 4, 6, 8, 10.
- vision-model-roles replacements: the former rewrites («If the adjacent layer is not running, Flow starts it, so a Tertiary reaches the Secondary…», «Vertical routing selects the adjacent layer…») added routing he did not speak on; now the obsolete sentences are struck only, each removed row paired with its surviving words so the renderer marks one removed run per row (L52 keeps «at a time.»; L62–67 keep «the sender's layer.», «Busy is still eligible.», «Multiple bindings … never fanout.», «Resolve the binding immediately before each attempt.»; L68–69 wholly removed). The owner re-wraps on landing.
- Figure: the last box now carries his words «the prompt it is to get now»; the condition «with no working transcript to reawaken» sits in the flow's box, the verbs (reaches, starts, is fed) on the arrows.
