# skillPromotionAndLayering

## 2026-09-16 — a path from distilled vision to skill; vision-as-skill, rationale as extended; spirit and intent in the top stratum; flows launch with skills as features

Context: after correcting the harness model ontology in the artifact comment thread, the living opened the shape of skills as a whole — how distilled vision becomes a skill, how a skill is layered, how it loads across harnesses, and how a flow launches with a skill set as its features.

> You should create a path from the most current distilled vision that conflicts with the skills that deal with the same topic and propose updates to the skills. In other words, we should almost make the core part of the vision a skill. Maybe the extended part is not so specific, knowing the general aspect of the topic, like a skill does, and belongs in a different file. Actually, we just call the skill the extended, the rationale, or whatever.
>
> We break up the skill into more levels so the agent doesn't have to load it all. The vision is the skill, so it's easier for the agent to load it, and then a layer if he needs to. The spirit and the intent are also part of the system prompt as important guidelines. All of the vision can be loaded as skills in the third layer by calling the skills, even in Codex. If you type the skill with the loading $, then in the prompt itself, it's going to load the skill at the right layer. It makes the prompt craft easier, and because you can make those not even accessible to the agent, you can make them sort of per-call optional skills, if they're for specialized behavior, I guess, but not anything that contains knowledge. That should be loadable by any agent that wants to know anything.
>
> Something like the main flow is to alter the behavior of a flow, right? That's different. Those are like behavior modules, skills, and they are just usable through the prompt. We need a way for the flow, one of the flow commands, to launch a flow with these particular skills, so they just get loaded in the prompt, right? They're like features. This is the main flow, right? It's an expert on this. It's a doubter, right? It's a critique. It's a visualizer that can create visualizations. It knows all of these software things and how to operate them, or it's a web browser that operates web apps for the user or whatever.

-- psyche, typed.

## Rules the shape encodes

- **Distilled vision is the source. Skills mirror it.** When a distilled Vision statement conflicts with a skill on the same topic, the skill is updated to match the vision, not the other way around.
- **A vision statement's *core* is the skill body.** Imperative, minimal, positive-shape — the form skill-designing already asks for.
- **A vision statement's *extended* material becomes the `<skill>-rationale`.** The why, the concepts, the historical anchors — loaded only by psyche-facing flows or when a flow explicitly needs the reasoning.
- **Spirit and Intent live in the top stratum.** They enter the system prompt (base instructions on Codex; system prompt on Claude), not through the Skill tool.
- **Vision-derived skills live in the middle stratum, load-on-demand.** The Skill tool call (`Skill` on Claude, `$<skill-name>` on Codex) puts them in the middle stratum, at the right sub-layer for the harness.
- **`$<skill-name>` loads a skill from inside a prompt.** Cross-harness: the syntax works whether the prompt is going to Claude or Codex. When placed in the prompt itself, the harness resolves it and loads the skill at the right layer.
- **Two kinds of skills.** *Behavior modules* alter how a flow acts (main-flow, psyche-interraction, spirit as top-stratum). *Knowledge skills* teach a domain (datom, nexus, harness ontologies, the mind's fact rows). Knowledge is loadable by any agent that wants to know. A behavior module may be marked not-accessible for per-call opt-in specialisation — but knowledge never is.
- **A flow launches with a chosen skill set as its features.** The flow-launch command names skills to preload. Those skills define what the flow *is* — an expert on X, a doubter, a critique, a visualizer, an operator of certain software, a web-browser flow. Features, not capabilities.

## The promotion path (proposed)

For a distilled Vision statement `V` on topic `T`:

1. Find every skill whose topic overlaps `T` (search `Curriculum skills/` and any active skill index).
2. If `V` **conflicts** with existing skill text, draft a skill update — a diff — in the form skill-designing wants (exact replacement text, no descriptions of what should be written).
3. If `V` **extends** the skill without conflict, place the addition in the `<skill>-rationale` if the material is why/context/concepts, or in the skill body if it is imperative and minimal.
4. If `V` is **new to skill territory**, propose a new skill (body from the core; rationale from the extended material).
5. Every promotion carries a psyche citation (the Vision entry ID / commit hash / date) per `escalationHierarchy.md`.
6. Curriculum edits themselves are the living's word.

## Feature launch (proposed)

A flow-launch command takes a role name and a feature bundle. The feature bundle is a list of skills preloaded in the flow's middle stratum via the `$<skill-name>` syntax at prompt-craft time.

Sketch (subject to the living's word):

```
flow-launch role=<role> features=[<skill-name>, <skill-name>, …] ...
```

The middle stratum then carries: the ad hoc role skill body inline, plus each feature skill loaded by `$<skill>` reference. The flow acts as an expert on those features.

## Consequences for prior work in this flow

- `flows/48cff7/proposals/*` — these become candidate promotions. Each proposal already has a description + body + placement; the promotion path picks them up when the living authorizes Curriculum edits.
- `flows/48cff7/vision/harnessModelOntology.md` — the *facts* in it belong in the mind (once running); the *shape* addition (persona sits on Codex, Claude uses model names) belongs in the harness skills.
- `flows/48cff7/vision/escalationHierarchy.md` — the citation rule already stated there aligns exactly with rule 5 above.

## Open questions worth the living's word

1. Confirm `$<skill-name>` is the exact syntax and that it is honoured by both Claude and Codex harnesses.
2. Whether a knowledge skill's *rationale* is always loaded with its body, or only on separate demand.
3. What "not accessible to the agent" means for a behavior module — hidden from the skills index but loadable by the launcher, or loadable only by the harness on the living's word.
4. Whether "feature" is the settled name for the launch-preloaded skill set, or if another word fits better.
5. Where the flow-launch command lives — a Nexus (`flow-nexus` with signal-flow), a Curriculum skill, or a shell tool.
