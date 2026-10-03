Presentation.{ «Context» }

## Part 1. What he wants

### Why this matters

A machine's output is a function of what is in its head.

> "the context *is you*"

-- typed, 2026-08-14.

### The strata and their authority

Text reaches a machine at one of three strata: top, middle, bottom. A higher stratum outranks a lower one.

> "strata is better than rung."

-- typed, 2026-08-18.

The point of the strata is a gradient of authority, tied to his own layering of Spirit, Intent and Vision, so a machine knows which instruction wins.

> "I really want to drive a system of gradients of authority so that agents know what to favor and what to disfavor."

-- spoken, 2026-08-10.

The top stratum is the harness's own standing instructions, which the harness composes for every agent, subagents included. No parent writes it for a child.

> "the builtin prompt instructs agents how to behave in the harness and how to use tools,etc. theres no way the parent is outputting all that for every subagent."

-- typed, 2026-08-14.

The top stratum is where the universal rules go, with Spirit above all.

> "Top stratum is where we want universal invariants. The rest is good"

-- typed, 2026-08-19.

> "I would want spirit on top in any case"

-- typed, 2026-08-18.

The middle stratum is the typed prompt and what the harness places beside it: entry files, loaded skills, a subflow's brief. Its source is not knowable to the machine.

> "all we know is its the typed prompt. where the prompt came from is unknown, so we cant say its from the user"

-- typed, 2026-08-18.

A skill loaded through the skill interface enters at the middle stratum, the same as the prompt. That is why skills work at all.

> "skills have the same authority as the user prompt."

-- spoken, 2026-08-13.

His own words to any flow travel in the middle stratum until they are distilled; then they rise.

> "My words have to go in the middle layer until we even find a way to distill, and then it goes into the top layer. The distillation goes into the top layer."

-- spoken, 2026-09-13.

> "the ongoing talk with the psyche of any flow is going to have to be through the middle stratum of its context."

-- spoken, 2026-09-14.

The bottom stratum is everything a flow fetches or says itself: tool output, files it opens, reports from its subflows, its own words. It binds nothing. A rule nobody anchored in a skill or entry file is just data.

> "Anything not anchored in a skill or claude/agents.md file is just data laying aound, with no authority"

-- typed, 2026-08-14.

Every layer carries only its own facts. This is standing Intent: "A value at any layer carries the context it makes sense in, and no layer carries a fact that belongs to another." (distilled, 2026-09-09).

### The system prompt: the top stratum, rewritten

He wants the stock system prompts of Claude and Codex replaced.

> "I want to replace claude and codex's system prompts with a version that doesnt incentivize the sort of behavior im constantly steering against."

-- typed, 2026-08-23.

What replaces it is our distilled Spirit, Intent and steady Vision, which also frees room in the prompt.

> "Also if we put all of our steady, well-distilled vision, intent, and spirit in the system prompt instead of in the prompt, then we have more room. We would replace whatever conflicts, even with our words, or modify it and it would give us a better behavior even."

-- 2026-09-25.

The stock prompt is first cut apart and every line classified, so each part can be kept, replaced or dropped on its own.

> "We need to break that down into modules. We can't just make this one thing. That's absurd. The system prompt is huge."

-- typed, 2026-10-03.

The classified pieces live as data, per harness and per model.

> "All categorized basically into data files, probably some kind of Markdown with Datom and Ethos syntax everywhere: specify data and then show data basically."

-- 2026-09-25.

Different jobs get different top strata. He called these words a draft of his thoughts the same day, so they stand as direction, not ruling.

> "In my vision, we're going to have different top stratums for different jobs. The top stratum will be programmable per flow."

-- spoken, 2026-08-30.

Rules that belong to one harness or model go in that harness's system prompt, not in Spirit.

> "It's not spirit level; it's specific to the model. Maybe we have a cloud core system, and that's where it would go. It's part of the system prompt."

-- typed, 2026-09-17.

### Entry files

The entry files (the Claude and Codex instruction files the harness reads at start) are ours entirely. What is particular to one machine goes in secondary files linked from them, which load at the same stratum.

> "this would also entail taking over entry files completly, leaving workspace specifics into secondary files loaded with the @ prefix, which does apparently load them at the same stratum"

-- typed, 2026-08-22.

> "the variables file should be directly linked in the entry file, so they enter middle statum"

-- typed, 2026-08-18.

Nothing in them explains what the harness already does.

> "dont explain things that the harness does automatically; agents.md is builtin to the harness. dont explain what everybody knows"

-- typed, 2026-08-25.

One authored source generates both harnesses' entry files. Proposed: once the context standard runs, they become one more output of it: the same modules, selected for the entry-file place.

### The meta-harness

Every flow gets a top stratum built for it, by our own harness above the vendor's: the meta-harness. Flow is that meta-harness today.

> "every session is unique and has the top layer, I guess we're going to call it, fed its own set of skills and style guidelines"

-- spoken, 2026-08-10.

It is his first priority now.

> "The most important thing we need now is to improve the meta harness: how easy it is to restart flows, how easy it is to deploy skills, and how much it becomes the implementation that we want with the correctness and the anatomy that we want."

-- typed, 2026-10-01.

### What a context module is

A skill is a piece of prompt. The same piece can sit in the system prompt, in the first prompt, or wait to be loaded. Each such piece is a context module.

> "Essentially, the system that we have for skill is really just like a prompt system, so we can use these either in the system prompt or in the prompt, or just let the agent have these skills available to load. So these would be different kinds of context modules, let's say."

-- spoken, 2026-10-03.

A module is a Markdown file with a type and a name. The type cannot be called a kind, and a role is a type.

> "I don't see `role` as a kind here, and I don't like `kind` because it collides with our use for `kind`, which is more basic."

-- typed, 2026-10-03.

Flow keeps a registry: for each module its type, its name, and where it lives. New modules are registered over Flow's meta socket.

> "Every flow call, or the flow database, has a registry of where each context module is located."

-- spoken, 2026-10-03.

One standard fills both the skills and the system prompt. Flow uses it; Curriculum implements it, and keeps its name.

> "a very extensive design for this system that can both populate the skills and the system prompt. It's a standard for now that Flow can use and that we'll also implement in curriculum, which we could possibly rename context or maybe keep it curriculum (because the word context is used a lot so I think it's better to keep it curriculum)."

-- typed, 2026-10-03.

### How modules compose a system prompt and a skill

A launch names, for each place, which modules to load. Flow inserts them.

> "We pass a list of which type and name for the context we want to load at each layer in the system prompt and in the origin startup prompt. They accept these values, and the flow nexus just inserts those values in the right places."

-- spoken, 2026-10-03.

Nothing is written twice. A selection is a vector: one entry per type, each carrying the names it wants. Names map to locations elsewhere.

> "It could be a vector with the variant, like vision, and each of the variants contains all of the names of the modules that it wants. Somewhere else in the database, those module names correspond with the path, so that's configured separately, right?"

-- typed, 2026-10-03.

Proposed: each role has one configuration with three places (system prompt, first prompt, loadable), each a vector of selections, plus its model. Flow composes the first two at launch by plain code, with no model in the loop; Curriculum's generator writes the loadable ones as each harness's skill trees from the same registry. The first prompt is one block, with what matters at the top.

> "one block of text, one user prompt only. We are not passing multiple prompts into a fresh session. Golden rule: put it at the top."

-- typed, 2026-09-24.

### The smallest, highest-signal context

> "They're just producing the best output based on the smallest, most concentrated, highest signal-to-noise context that we can assemble."

-- spoken, 2026-10-03.

That means distilled words over raw ones.

> "But it's more clear and it's more compact, so it offers more signal to noise."

-- spoken, 2026-08-22.

Small is not thin: a new flow gets its context placed in its head, not files to read.

> "My new flows are not getting a nice fat user prompt for context. They're told to read files, which yields lower-quality context."

-- typed, 2026-09-29.

### What differs per harness

One source; each harness gets its own blocks, chosen by a template in the Markdown.

> "Depending on Codex, Claude, or all of the harnesses that we're going to support, it's going to emit the different blocks that depend on whether or not it's Claude or Codex, with the templating language in Markdown that we supposedly already have implemented."

-- typed, 2026-10-03.

What each harness blocks or refuses is written into that harness's skill.

> "If anything is ever blocked by a model or by something, we need to document it under that harness and what category of block it is in the harness skill."

-- typed, 2026-09-17.

Proposed: the generator alone knows each vendor's shapes. On Claude the system-prompt place replaces the stock prompt through its system-prompt file. On Codex it replaces the base instructions through the instructions file, because Codex's developer instructions rank below the base instructions. Loadable modules go to each harness's skill tree; a subagent's definition is generated from its role.

### What a subflow receives, and what it does not

He wants part of a main flow's system prompt kept from its subagents.

> "I would like to be able to program the main flow a certain way but not its subagents in its system prompt."

-- typed, 2026-10-03.

Some startup modules are for chosen flows only, and machines cannot load them.

> "It's just that we don't need the models to see it because it's a skill that's only given to certain flows and not their subagents."

-- typed, 2026-09-24.

A subagent's standing context comes from its own definition, never from a repeated brief.

> "No, the main flow should not put anything in every brief. That's what subagent definitions are for. The subagent launch should require as few tokens as possible."

-- spoken, 2026-10-03.

Proposed: a subflow receives the harness's own built-in instructions, its role's modules, its loadable skills, and a brief carrying only the task. It does not receive its main flow's system-prompt modules or withheld startup modules. Whether each harness keeps the parent's replaced prompt from its subagents is to be witnessed in the harness code before the design relies on it.

### How an edit to the system prompt is proposed and lands

He wants to change the system prompt through a steady stream of small proposals he can approve at a glance.

> "I want to modify the system prompt. I want to use the new flow. I want skills that do skill edits. I want a constant flow of small skill edit proposals, not huge ones, so that I can say yes quickly."

-- typed, 2026-10-03.

Distilling his words is that editing, and everything is stored once.

> "That's what vision distillation is now, because when you distill vision, you put it into a vision file, which is a skill."

-- typed, 2026-10-03.

> "We only store the stuff once, and we have different rules for who can edit what and what type."

-- typed, 2026-10-03.

Proposed: a proposal names one module, shows its lines before and after, and says which stratum and roles it reaches. He answers yes or no. On yes, a program lands the change in Curriculum, regenerates every harness's output and registers the module; the next launch of those roles carries it. No flow edits a prompt by hand. Because he cannot read Claude's system prompt through anything the harness offers, the proposal itself shows him the full text that will stand.

## Part 2. What exists today

The context-strata skill is deployed. It names three strata: the harness's standing instructions on top; the typed prompt, entry files, skills loaded through the skill interface and subflow briefs in the middle; what a flow fetches or says itself at the bottom, with no authority. Promotion moves text up; seizing a harness means authoring its top stratum.

Curriculum's generator renders skill bodies per harness, read in its code. Directives stand alone on a line: if claude, if codex, if pi, else, endif, and raw to pass directive text through untouched. It writes a Claude tree and a Codex tree; Pi is recognised but never written. A skill marked user-only is withheld from the machine on both. Two skill sources use the directives. Role packets are copied as written, without templating.

## Part 3. Questions

1. Build the context standard as drawn in «Curriculum: the context standard», with the Codex system-prompt place moved to the replaced base instructions? Yes, or comment.
2. Cut both stock system prompts into typed modules first, every line marked behavior, personality, operational safety or harness use, so each later edit touches one module? Yes.
3. A system-prompt edit reaches you as one module, before and after, and a program lands it on your yes. Yes?
4. Which modules go in every flow's system prompt: 1 Spirit only; 2 Spirit and Intent; 3 Spirit, Intent and steady Vision chosen per role?
