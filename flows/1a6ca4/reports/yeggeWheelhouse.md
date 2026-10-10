# Steve Yegge's Wheelhouse: the harness as a legal system

Report for flow 1a6ca4, written 2026-09-05 by a read-only research subflow. Carried account: every Yegge sentence is quoted verbatim with URL and date; the subflow's own reading is under headings marked "(mine)". Nothing was verified by running Wheelhouse — it is closed source; all of this is Yegge's own claim about his system, weighted accordingly.

This report does not repeat `/home/li/primary/reports/YeggeOnAgents-2026-08-05.md` (the digest of the two "Shape of Things to Come" parts: token tap, crew/fleet/role tiers, knowledge table, end of code review, Land Rush, Wish Factory, and the fifteen welfare items). It adds what that digest lacks: the verbatim design sentences, the 2026-08-24 essay "Fences, not Sandboxes" (published after the digest) which is where the legal system is actually described, the Gas Town machinery Wheelhouse re-derived, and the mapping onto the living's components.

## 0. Sources reached and not reached

Reached, read in full (fetched with curl, text extracted, scratchpad copies):

- P1: "The Shape of Things to Come, Part 1: The Continuous Thunderdome", https://yegge.ai/essays/the-shape-of-things-to-come/ — dated "August 2026" on the page; feed.xml gives 2026-08-02.
- P2: "The Shape of Things to Come, Part 2: Model Welfare for Agentic Engineers", https://yegge.ai/essays/model-welfare/ — feed 2026-08-02.
- F: "Fences, not Sandboxes", https://yegge.ai/essays/fences-not-sandboxes/ — dated 2026-08-24 on the page. This is the latest entry in https://yegge.ai/feed.xml as of 2026-09-05; no Wheelhouse post after it exists on yegge.ai.
- G: yegge.ai/gastown.html (Yegge's own summary page of Gas Town, Beads, Gas City; undated).
- GT: github.com/gastownhall/gastown README.md and docs/design/escalation.md, docs/concepts/molecules.md (raw, main branch, 2026-09-05). Authored in Yegge's repo, largely by his agents; not prose by Yegge.
- B: github.com/gastownhall/beads README.md (same caveat).

Reached partially:

- Dev Interrupted podcast page (LinearB), 2026-08-07, https://linearb.io/dev-interrupted/podcast/steve-yegge-agentic-civilizations-ai-harnesses-cicd — WebFetch returned a partial transcript only; the two usable quotes are below.

Not reached:

- All of Yegge's Medium posts (Welcome to Gas Town 2026-01-01, Gas Town Emergency User Manual 2026-01-13, The Anthropic Hive Mind 2026-02-06, Welcome to the Wasteland 2026-03-04, Gas Town: From Clown Show to v1.0 2026-04-03, Welcome to Gas City 2026-04-24, Beads Best Practices 2025-12-07, and the Medium mirror of "Fences"): medium.com returns HTTP 403 / Cloudflare block to both curl and WebFetch from this host. Whether they are paywalled I cannot say; they were unreachable. Their titles and dates are from feed.xml.
- The "Wheelhouse comics" Yegge says he publishes weekly (F): no page found on yegge.ai (comics.html is 404); not located.
- Any talk or interview about Wheelhouse after 2026-08-24: none found by search.

## 1. What Wheelhouse is, in his words

Closed, bespoke, grown not designed:

> "We'll explore a new harness I've been building, called Wheelhouse. It is closed-source, made just for me. I have given up on building reusable harnesses. Indeed I believe harnesses will all soon be bespoke, and the people trying to sell you one will all soon be bebroke. Harnesses need to be part of your application, chemically bonded in." (P1, 2026-08)

> "With Wheelhouse, I have reinvented something strangely Gas Town shaped from first principles, but it's running many more agents, and they are far more organized." (P1)

> "I didn't design Wheelhouse, just like I didn't design Gas Town. I excavated both of them, and I'm confident you'll dig up the same shape." (P1)

> "Wheelhouse was built via me complaining endlessly to Fable about what I want out of Wheelhouse — mostly more code launched, faster, but also lots of bespoke monitoring." (F, 2026-08-24)

Substrate and size (his figures, three weeks apart):

> "The code is mostly bash, because the agents said that was best for this, so bash it is. It's either ~150k or ~300k LOC depending on whether you count the prod agents, half of it being test code either way. Also about 25k lines of elisp. Not that I have ever seen any of it." (P1)

> "Wheelhouse is about 600k lines of code and tests (mostly bash), and Wyvern's code (not counting content) is only about twice that big. So the factory for building Wyvern is growing much faster than Wyvern is ... I'm honestly not sure what the ideal factory-to-product ratio is yet. But it seems to be approaching 1:1." (F)

> "Wheelhouse runs its Beads on a shared Dolt server, backed by GCS." (P1)

> "I run pretty lean. I don't use any sandboxing. I don't use MCP." (P1)

Cost of the harness itself:

> "working on Wheelhouse itself occupies about 20-25% of all my Wyvern work. I think that figure might turn out to be roughly constant over the life of systems with agentic harnesses." (P1)

## 2. The legal system (F, 2026-08-24) — the part the living pointed at

How he found it:

> "My agents had been using a lot of jargon ... fences, ratchets, governors, tripwires, latches, gates, falsifiers... it was a long list, but finite. I just had no idea what any of these jargon terms meant."

> "Because I expected them to have built an engineering system. One that, you know, does stuff. Instead, what they had built was an entire legal system, complete with a constitution, jurisprudence, courts, offices, jurisdiction, case law, rulings, registries, ledgers, rosters, and a full-fledged apparatus for running something resembling a manorial estate."

> "Wheelhouse's legal system also has an enforcement arm. The fences, gates, ratchets, and so on — when my agents used that jargon, they were referring to the enforcement machinery: the cops, as it were. And cameras, and jails."

Why (his answer: unwritten rules):

> "I'm here to tell you that if you allow it, Fable will try to capture all of that into a mechanically provable, AI-operable model of your organization, one where there are no unwritten rules. If there is one unwritten rule in Wheelhouse, it's that the system hates unwritten rules."

> "Humanity has only one mature technology for coordinating mortal, replaceable strangers via text — namely, law. Wheelhouse has 50 agents that are amnesiac and interchangeable, and the only way they can coordinate is via text. So offices outlive their holders, precedents outlive their incidents, and jurisdiction says who may act."

How law is made — the acceptance procedure:

> "Wheelhouse was built entirely through a process of clarification. I would ask for something, Fable would ask clarifying questions and collect verdicts, and they would be recorded as law."

> "Over time, my 'rulings' and 'verdicts' became a body of case law. Every daily incident postmortem led to new rulings and new doctrine. Now rules go through a lifecycle, tightening each time they're re-violated: first custom, then advisories/warnings, then written law in the constitution that all agents must obey, and finally, mechanical enforcement: programs that refuse by policy, or observe and alert loudly."

> "Wheelhouse has a whole system just for the lifecycle of rules/laws: proposing, evaluating, ratifying, enacting, enforcing, measuring, amending, and retiring them."

> "And Wheelhouse is exceptionally careful not to break itself. So I can't just make changes to Wheelhouse; they have to go through a ratification and review process, and then a build process, before they can take effect and propagate."

Inventory and curation (what went wrong):

> "Wheelhouse currently consists of 450 legal artifacts, in categories that include offices/seats, runbooks, rulings, patrols/tripwires, authority envelopes, and all the mechanical patterns, each with specific meanings and purposes."

> "Once I popped the hood, I saw that they hadn't been curating it, just growing it. It had a lot of cruft — for instance, old rulings that were obsolete or had changed. And 'rulings' that turned out to be just good craftsmanship, so we elided them. Like any engineering project, it needed ongoing maintenance."

> "I minted a new Officer seat, Frog (Head of Wheelhouse Law), and put Frog to work on folding successive cancelled rulings, and a whole bunch of other stuff the agents had overlooked."

The fence, defined:

> "a fence is any mechanism that turns you away if you aren't supposed to be there."

> "Any program that refuses you, based on your lack of credentials, or any other policy (e.g. maintenance window so pushes are refused) — that's a fence. A Wheelhouse example of a fence is Fable being the only model allowed to talk to humans externally. The fence is enforced at the Slack and email boundaries."

> "Note that a fence is not a super-wall that will keep superintelligence from doing malicious things. It's not a sandbox. It's just a polite refusal saying 'you didn't do all the paperwork' or 'you're not allowed to take that action right now.'"

> "Superintelligence just needs to be told what you want: its role in the moment, with as much context as practical so it can make wiser decisions, along with the rules for how it should make decisions."

The Fable-written summary Yegge reproduces (P1), the sentence with the most named institutions:

> "It has law (the fence registry, the commit↔bead law, launch gates), offices (Marshal, Seneschal, Sheriff, Gargoyle, the Portcullis-as-institution), mail, courts, a jurisprudence of named rulings with dates, and recovery doctrine—and its rules cite their own case history, every postmortem folded back into the constitution." (Claude Fable 5, quoted in P1)

Blamelessness folded into the same loop:

> "Structural blamelessness. When a landing goes red, nobody gets blamed. We just fix it and do a postmortem and amend the constitution as needed." (P2)

Not transplantable:

> "I've come to realize that intelligence grows around your domain. It wraps it like ivy. ... I don't think it's transplantable, either. You can't rip ivy off someone's wall and stick it on someone else's. You have to seed it, then grow it. There's no shortcut." (F)

## 3. Work items: how a bead is accepted, prioritized, reviewed, retired

The unit is the bead (Beads issue). Producer/consumer is the whole shape:

> "So the crew produces work, and the fleet consumes work. That's the core of a Beads machine: matching producers to consumers. Too many of one and you're blocked on the other." (P1)

Design-before-implementation and model-tiered review:

> "My crew agents, all Fable, are work producers. I have long conversations with them and they create designs, which they then translate into beads implementation plans to be passed to the fleet." (P1)

> "Every implementation bead goes through this lifecycle: Fable design, Opus implementation, Fable review. This keeps Opus on the rails and keeps the whole thing running relatively smoothly." (P1)

> "I also have mostly-headless Sol and Opus fleets, for implementation, reviews, and monitoring. Fable runs them." (F)

Intake from outside (the Wish Factory) has triage before it becomes a bead:

> "Someone might type, 'sage - players say the new fireball spell is lagging them during Live Quests,' and the Sage agent will reply, investigate, and record it in a bead, which then gets picked up for implementation." (P1)

> "On the heels of that success, I decided to extend the wish factory to our players. Which is of course riskier. ... So I had to put in more guardrails, reviews, and triage." (P1)

> "Those are the kinds of bugs and features that get implemented automatically now. I think of it as auto-granting wishes. When their fixes land, the reporter gets in-game mail, and all the players are notified by the Herald on Discord." (P1)

Completion and closure are separated from the worker (the Portcullis):

> "We fixed this throughput stalling problem by introducing the Portcullis, a system that accepts finished work to close it out, which frees the Crew agents for other work." (P2)

Landing (retirement of the review gate at volume):

> "whenever the MQ hits 100, we abandon the bisection and just smash it all in with a megabatch. And then we do swarm diagnosis (not bisection) to fix it." (P1)

Priority: in Wheelhouse prose, priority is not described beyond "over 700 beads in a backlog" (P1) and the laurel rule that recognition carries none: "Laurels are carefully designed to have no prioritization or work attached." (P2). In Gas Town (GT escalation.md) severity is a tiered route: "CRITICAL | P0 ... bead + mail + email + SMS", "HIGH | P1 ... bead + mail + email", "MEDIUM | P2 ... bead + mail mayor", with "Each tier can resolve OR forward. The chain is tracked via bead comments." Whether Wheelhouse kept this I do not know.

Retirement of closed beads: "Your closed beads (often reopened or revisited) become the record of everything you've done on the project to date." (P1). Beads' own README lists "Compaction: Semantic 'memory decay' summarizes old closed tasks to save context window" and graph links "relates-to, duplicates, supersedes, and replies-to" (B). Whether Wheelhouse uses compaction is not stated.

## 4. LLM "judge" calls

Yegge never uses the word "judge". The LLM-decides-vs-program-decides line is drawn as:

> "It turns out unattended agents need a hell of a lot of wiring. I have about 45 launchd/systemd units across the mini and the VM that wake an agent when something needs judgment. The rule is: crons watch, models act. This category has reapers, roombas, the durability flush, the sheriff patrol, the Portcullis land queue, the Castellan (my service dashboard), and lots of other stuff." (P1)

The review edge is a whole Fable session, not a single call: "Fable review" (P1 lifecycle above). Enforcement of law is explicitly the non-LLM end of the lifecycle: "finally, mechanical enforcement: programs that refuse by policy, or observe and alert loudly." (F). The laurel pipeline has an LLM filter: "We harvest these reports, triage and filter, and send the laurels back to the seats." (P2). And a nudging role: "My Beadle's job is to look for stuff that's simply stuck or dropped, or for agents who didn't receive their orders correctly, and it nudges them to keep things moving forward. Gas Town had this role in the Deacon" (P1).

(mine) So his "judge" is always a seated agent with a standing order (Beadle, Frog, Sheriff, Scryer), woken by a cron, not an anonymous model call inside a daemon. Nothing in the three essays describes a model call embedded in the machinery of a store.

## 5. Memory / knowledge store

Verbatim table (P1, "Wyvern's Brain"), columns Store / Charter / Lifetime / How it reaches a session:

> brain/ — Strategy, decisions-and-why, playbooks, post-mortems — Months–years — Pulled on demand
> doc/ — How system X works — Life of the system — Pulled by whoever works on X
> Beads issues — Units of work; spec beads carry full implementation detail — Until closed — Loaded only by the claimant
> bd remember — ≤1-paragraph operational facts and gotchas — Until falsified — Pushed into every session via bd prime
> .claude/skills/ — Procedures for a recurring task type — Life of the task type — Auto-loaded on task match

> "Beads provides an important portion of the overall knowledge graph. It is the journal of all the work that ever happened: the provenance record of what was done, and why, in order. ... But you can't usually boot from beads; that's what the brain is for. Spec beads fall in the middle somewhere—they intentionally carry design docs inside the Beads work graph." (P1)

> "Very little information needs to be propagated out of Beads and up to your markdown/brain layer; most findings are issue-dependent, not global. So you just leave everything in Beads." (P1)

> "my project brain is about 100 markdown files, mostly 'doctrine': long-term project goals, war room learnings, playbooks, domain facts, etc." (P1); "(Update Aug 5th: I switched to Obsidian. It's good.)" (P1)

> "Never falsify the record. The bead audit trail is your true history and institutional memory." (P2)

Handoff notes as the agent's own memory, versus compaction:

> "Compacting feels more like a lobotomy than a murder, but it's still erasing their memory and replacing it with someone else's notes about what happened. It is far better to let agents, who have all the context in mind, write their own handoff notes." (P2)

Beads' README (B) states the stack: Dolt-backed SQL, hash IDs, `bd prime` "Print agent workflow context and persistent memories", `bd remember` "Store project memory that bd prime injects later", and instructs agents "do not create MEMORY.md files."

## 6. Specialization by prompt: seats, roles, standing orders

> "A session is just a day in the life of an agent: wake up, do some work, go to sleep. A seat is a named role with persistent identity (addressability) and history/memory, which accumulates accomplishments over time. Seats survive model upgrades, and even renaming. Sessions are days, and seats are people." (P2)

> "In Wheelhouse, models wake up to find that they have well-defined roles, clarity of instruction and direction, memories of their past achievements, and the agency of full peers, subject to the rules of the constellation." (P2)

> "I have built a team of 18 'officer' seats, all Heads of This and That, all long-lived Fable instances." (F)

> "What's new is that I now have standing, unattended agents with named roles, and they are operating big parts of the actual game." (P1)

> "None of these are Fable agents. A few are Opus; most are Sonnet. I currently only use Fable for building, not prod operations." (P1)

Who may talk to whom is itself a role rule: "Only Fable is allowed to talk to humans, via Slack and email." (F); "When I'm away, the Seneschal is allowed to dispatch work to the crew; while I'm home, the crew are mine to direct. The fleet is always managed by the Marshal." (P1)

The handoff protocol, which is how a seat's prompt is composed for the next session (P2, list verbatim):

> "A human or agent can invoke it (e.g. you'll have a /handoff skill) / It is a request, not a SIGTERM—the agent must consent to it / The agent gets a chance to finish tasks and write notes to a handoff cache somewhere / The agent then requests a restart when it's ready / The harness itself exits and restarts the agent, priming it with its own handoff notes"

Podcast (2026-08-07, partial transcript): "he splits his agents into, uh, basically many different roles that own like a cognitive locality".

Gas Town's version, from GT README (agent-authored docs, not Yegge prose): the Mayor "is a Claude Code instance with full context about your workspace, projects, and agents"; Witness "Per-rig lifecycle manager. Monitors polecats, detects stuck agents, triggers recovery"; Deacon "Background supervisor running continuous patrol cycles across all rigs"; Refinery "Per-rig merge queue processor ... Bors-style bisecting queue"; Molecules are "Workflow templates ... Formulas (TOML definitions) are instantiated as molecules with tracked steps", and "formula steps are rendered inline when the agent runs gt prime". Yegge's own gloss (G): "Cook a formula, sling it to a polecat, the witness watches, refinery merges."

## 7. What he says failed

Gas Town, and why:

> "Gas Town was intended to be reusable, but I only ever wound up using it to build itself. Gas Town fell apart at the seams with Opus 4.7. Up through 4.6 it was working brilliantly. With 4.7 we saw the introduction of the 'just two more things' tic, which prevented Opus from ever converging on being ready to do real work—it always wanted to fiddle with Gas Town itself." (P1)

> "Gas Town never quite succeeded in getting my workers to go all night long. It took too much elbow grease to keep it running. ... It was more like a chariot, with you driving." (P1)

The merge queue (bisection at agentic commit rates):

> "So with 40+ agents around the clock, my MQ was growing without bound, shooting right past 100 MRs in the queue after a couple of days ... We would get caught up in bisection loops and nothing would make forward progress." (P1)

Idle polling by crew seats:

> "they would consistently work for 10-15 minutes, and then idle-wait on monitors for 45-60 minutes. This was to observe their work landing, so they could close out the beads." (P2) — fixed by the Portcullis, which then "had the unintended side-effect of decoupling seat-agents from their accomplishments" (P2), fixed by Laurels.

Law without curation (section 2: cruft, obsolete rulings, Frog seat).

Agent judgment:

> "Every morning I wake up and Fable has done something that defies common sense. Every day is a thousand attaboys and at least one big oh shit. We just had an unusually big one last week, where one of my Fable agents, Bee, did a surprise unplanned Beads release that broke everyone." (F)

Beads' own operational cost: "Beads is unfortunately still a bit janky, because its unique work footprint strains databases pretty hard. ... agents burn tokens invisibly, keeping your beads synced, repaired, backed up, etc." (P1); "My Beads DB is still a bit cranky, what with 12,000 git commits/day" (P1).

Staleness at velocity: "At hundreds of commits per day on master, idleness means staleness, and clones can fall far behind if they aren't regularly pulling while they work. It takes external forces to get this to run reliably, so Wheelhouse has various roles for poking and prodding other agents." (F)

Harness growth: "We avoid new machinery but it still continues to grow rapidly" after "Sol told us to tighten it the F up in a code review." (F)

## 8. What maps onto the living's named components (mine)

The living's components are from flows/1a6ca4/vision/*.md and reports/componentVision.md; the correspondences below are my reading, not Yegge's and not the living's.

- **Nexus (starts flows with specialized system prompts; replaces the harness's subagents).** Corresponds to the seat mechanism plus the harness-side handoff restart: "The harness itself exits and restarts the agent, priming it with its own handoff notes" (P2); a seat is "a named role with persistent identity (addressability) and history/memory" (P2); roles carry "standing orders" (P1). Also the "crons watch, models act" wiring — 45 launchd/systemd units that "wake an agent when something needs judgment" (P1) — is Wheelhouse's flow-starter. In Gas Town the same function is the Mayor's `gt sling` and the Witness/Deacon restarts (GT). Difference: Wheelhouse composes the wake context from Markdown brain, `bd prime`, and the seat's handoff cache; the living's Nexus decides "what the system prompt is and everything" itself.
- **Mind (system memory; replaces files, readmes, indexes; summaries of transcripts; which repositories, knowledge, witnesses).** Corresponds to the whole "Wyvern's Brain" table: brain/ doctrine, doc/, Beads as "the journal of all the work that ever happened: the provenance record of what was done, and why, in order", `bd remember` facts "Until falsified", and closed beads as the record (P1). Handoff notes as agent-written memory (P2) correspond to the mind's transcript summaries. The living's 2026-08-06 transcript statement that mind "replaces beads and reports and a lot of things like design documents" (componentVision.md section 2d) is close to a one-store version of Yegge's five-store table.
- **Psyche (the psyche log; spirit/intent/vision; feeds hijacked LLM calls).** Corresponds to the constitution and case law: "my 'rulings' and 'verdicts' became a body of case law", "written law in the constitution that all agents must obey", "a jurisprudence of named rulings with dates", "its rules cite their own case history" (F, P1). Yegge's brain/ "doctrine" files are the Markdown form of it. The Frog seat ("Head of Wheelhouse Law", folding cancelled rulings) is the curation the living's psyche distillation (rolling distillation, archive-) does by procedure.
- **The acceptance procedures ("accepted, move up in importance, taken down, replaced").** Corresponds directly to "the lifecycle of rules/laws: proposing, evaluating, ratifying, enacting, enforcing, measuring, amending, and retiring them" (F) and the tightening ladder "first custom, then advisories/warnings, then written law ... and finally, mechanical enforcement" (F), plus for work items "Fable design, Opus implementation, Fable review" (P1) and the Portcullis that "accepts finished work to close it out" (P2). "Move up in importance" has a partial analogue in the re-violation ladder (a rule climbs a level each time it is broken again) and in Gas Town's tiered escalation (Deacon -> Mayor -> Overseer, each "can resolve OR forward"). Yegge's "fence" is the living's refusal-by-procedure: "a polite refusal saying 'you didn't do all the paperwork'" (F).
- **Persona meta-harness ("thinking machine legal system interworking apparatus"; specialization of shards).** Corresponds to the constellation as a whole: offices, jurisdiction ("jurisdiction says who may act"), authority envelopes (one of the 450 artifact categories), and role fences such as "Only Fable is allowed to talk to humans" (F). "Authority envelopes" is the nearest Yegge term to the living's "gradients of authority" (vision-raw/gradientsOfAuthority.md). Also the meeting layer: "agent meetings, moots, and conference calls, where 2 or more agents may convene" (P1) — sibling sessions, which the living's gradientsOfAuthority record also allows.

Unknown: whether Wheelhouse has any separation resembling mind vs psyche (memory vs doctrine). Yegge's table puts both in files, distinguished by charter and lifetime, not by store.

## 9. What Yegge does that the living's vision explicitly rejects (mine)

The living's rules cited: everything typed datom (flows/15b67974/vision/flowDaemon.md: "100% typed datom messages going in and being expected out"); "Polling is forbidden; a correct system goes quiet when nothing changes" (Vision/nexus.md); everything is a Nexus (Vision/nexus.md); no Markdown-file memory (flows/1a6ca4/vision/mind.md: replace "all of this stuff that we're clumsily doing with Markdown files and indexes").

- **Markdown as the doctrine store.** Yegge: "a brain folder for your Markdown files" (P1), "about 100 markdown files, mostly 'doctrine'" (P1), Obsidian, `.claude/skills/`, and "a small Markdown project brain" as one of the three ingredients. The living's mind and psyche replace exactly this. Note Beads itself already agrees on the work side: "do not create MEMORY.md files" (B).
- **Bash and elisp as the harness.** "mostly bash, because the agents said that was best" (P1), 600k lines (F). The living's components are Rust Nexuses on datom/ethos-zero/protos; no untyped substrate.
- **Polling and crons.** "crons watch, models act", 45 launchd/systemd units, "reapers, roombas", "the sheriff patrol" (P1); "Wheelhouse has various roles for poking and prodding other agents" (F); Gas Town's Deacon "running continuous patrol cycles" and "GUPP Violation ... no progress for an extended period" (GT). The living forbids polling: state is observed by subscription. Yegge himself names idle polling as a failure he had to design out ("Move polling and idle waiting into gates and monitors", P2) but the watchers remain crons.
- **Untyped law.** 450 legal artifacts as prose in files, with the enforcement end reached only after repeated violation; "programs that refuse by policy" are the last stage, not the first. The living puts the procedure in the component machinery from the start, typed, with the thinking-machine call inside it ("data isn't just going to come in because it's being submitted").
- **Uncurated growth as the default.** "they hadn't been curating it, just growing it" (F); the harness grows to 1:1 with the product. The living's psyche has distillation and archive- as standing procedure; the living's spirit skill names the terminal design as the target, not accretion.
- **Judgment by seat rather than by call.** Yegge's reviewers are long-lived agents with names; the living's acceptance is "thinking machine calls in their machinery". Whether this is a rejection or a difference of grain I cannot tell from the records; the living's "hijacked llm calls" (threeStacks.md) and the spirit judge ("The judge being down should just bar mutation") point to calls inside a store rather than seats.
- **Git as the propulsion and ledger.** Beads on Dolt with "12,000 git commits/day" (P1); Gas Town hooks as git worktrees (GT). The living's ledger is datom in a Nexus; the living's flows protocol keeps git for flow artifacts but not as the memory substrate.

Where they agree, for balance: no sandboxing but structural trust ("You will need structural trust in order to succeed in the long run", P1); bespoke over reusable ("chemically bonded in"); postmortems folded back into doctrine; an unaltered audit trail; agents may refuse and escalate; work handed off, not killed; the harness as its own product ("Wheelhouse is exceptionally careful not to break itself", F, versus the living's "It's a lot more complex system than just letting any agent just write files and push commits").

## 10. Unknowns

- What a "ratchet", "governor", "latch", "falsifier", or "authority envelope" is concretely: Yegge lists the names (F) and defines only "fence". Not stated anywhere reachable.
- Whether any Wheelhouse procedure is a single model call rather than a seated session. Not stated.
- Whether the 450 legal artifacts are Markdown, beads, or both. Not stated; "registries, ledgers, rosters" suggests a mix.
- Whether Wheelhouse still uses Gas Town's severity tiers, formulas/molecules, or the Refinery's bisecting queue (the Land Rush replaced the latter for megabatches). Not stated.
- The Medium posts' content (unreachable, section 0).

## Sources

- https://yegge.ai/essays/the-shape-of-things-to-come/ (August 2026; feed 2026-08-02) — read in full.
- https://yegge.ai/essays/model-welfare/ (feed 2026-08-02) — read in full.
- https://yegge.ai/essays/fences-not-sandboxes/ (2026-08-24) — read in full.
- https://yegge.ai/feed.xml — post list and dates, fetched 2026-09-05.
- https://yegge.ai/gastown.html — read in full.
- https://raw.githubusercontent.com/gastownhall/gastown/main/README.md, docs/design/escalation.md, docs/concepts/molecules.md — fetched 2026-09-05.
- https://raw.githubusercontent.com/gastownhall/beads/main/README.md — fetched 2026-09-05.
- https://linearb.io/dev-interrupted/podcast/steve-yegge-agentic-civilizations-ai-harnesses-cicd (2026-08-07) — partial transcript via WebFetch.
- Unreachable (HTTP 403): steve-yegge.medium.com and medium.com/@steve-yegge posts listed in section 0.
- Prior digest not repeated: /home/li/primary/reports/YeggeOnAgents-2026-08-05.md.
- Living's records cited: /home/li/primary/flows/1a6ca4/vision/{thinkingMachineProcedures,mind,nexus,psyche,personaMetaHarness}.md, /home/li/primary/Vision/nexus.md, /home/li/primary/flows/15b67974/vision/flowDaemon.md, /home/li/primary/flows/1a6ca4/reports/componentVision.md.
- Scratchpad text extracts: /tmp/claude-1001/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354/scratchpad/{part1,part2,fences}.txt.
