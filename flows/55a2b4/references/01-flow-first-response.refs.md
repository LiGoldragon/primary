# Refs for «Flow: the first response» (flow 55a2b4, 2026-10-14)

Not rendered. Records the proposals draw on, read whole with their flow context.

## P1 first prompt and first response
- flows/d68c82/vision/flow.md «a refreshed flow starts by crystallizing its topic», 2026-10-14, STT: loads context modules, is given raw psyche with context, first and last response is a crystallization proposal; «no point in making an LLM start without giving it something to do».
- flows/d68c82/vision/flow.md «A metaflow's default task», 2026-10-14, STT: default task is a proposal or a question.
- flows/445410/vision/flow.md, 2026-10-09, STT (also 9fed42, 73ada7, f5a6e9 abridged): worst thing is to make a flow say «You're ready»; first last response is a presentation in its role (Psyche for vision, Mind for implementation and knowledge, Field its own). Choice 1.1 carries this earlier, aspect-shaped wording.
- flows/5578cc/vision/flow.md, 2026-10-03T16:17, typed, book comment: the flow id is in the prompt; anything deterministic is code, not LLM work.

## P2 startup context is data
- flows/d68c82/vision/flow.md, 2026-10-14, STT: «a default startup context ... I don't want any values, such as prompts, hard-coded into code».
- flows/d68c82/vision/flow.md «Flow starting configured in EDN, per aspect and per metaflow», 2026-10-13T17:47, STT. The EDN reader pattern itself is book A's (flows/df159a/brief-patterns.md) and is not repeated here.
- Audit flows/d68c82/reports/clojure-migration-2026-10-14.edn: 58 hard-coded values, 13 of them prompts, 14 models, 8 skill lists.

## P3 Flow, Nexus, Ethos together; Flow bootstrapped first
- flows/d68c82/vision/flow.md «Flow, Nexus and Ethos together; Flow is the bootstrap», 2026-10-14, STT (uncommitted at reading): three aspects, language / runtime architecture / Flow «the most important component to bootstrap»; «Bootstrap persona, the meta harness, since starting flows like clean lean flows, specialized flows, or refreshing flows is a central part, a cornerstone». Choice 3.1 reads «persona» as the module home (vision-persona).
- flows/88475f/vision/flow.md, 2026-09-24, relayed by e51411: «Flow deploys first» (already in vision-flow.md L26).
- flows/d68c82/vision/flow.md, 2026-10-13T17:52 and 2026-10-13: cheap to start specialized flows; lean flows for Fable.

## P4 short-term prototypes in Clojure
- flows/d68c82/vision/flow.md «Short-term prototypes are written in Clojure», undated, commit eb5215 of 2026-10-13, STT: «If any prototype doesn't use Clojure it's going to have to be rewritten in Clojure».
- flows/d68c82/vision/flow.md, 2026-10-14, book comment: «strip down some of these Clojure flows so that they're way more efficient to spawn».
- Builds on book 14 P1–P3 (flows/df159a/books/14-short-term-prototypes-clojure.md, Version 6, unruled). «Starter first» follows from P3, not from an order.
- Audit: live non-Clojure files 24 (mjs 19, sh 4, py 1); the starter is tools/claude-main-flow-launch.mjs, codex-main-flow-launch.mjs, opencode-main-flow-launch.mjs, native-*-launch*.mjs, main-flow-mode/launch-config.mjs, spirit-system-prompt.mjs, context-refresh.mjs, context-refresh-hook.mjs, secondary-first.mjs.

## Pattern
- flows/d68c82/reports/startup-prompt-draft.md: config/main-flow/first-prompt.edn and tools/first_prompt.clj; removes STARTUP_INSTRUCTION (claude-main-flow-launch.mjs L47, L132). The page shows it once as the standard entry point, per his 2026-10-14 words in flows/df159a/vision/books.md.

## Held out of the page (tensions, in log.md)
- Refresh thresholds 2026-10-07 / 10-13 / 10-14; compaction statements of 2026-10-13 (order unrecorded); lock ownership 10-07 reversed 10-11 (module carries 10-11).
