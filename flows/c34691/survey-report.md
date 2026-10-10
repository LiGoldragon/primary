# Flow Survey — What's Open, What's Landed

*Flow c34691 · 2026-09-04*

A survey of the 11 most recent flows (b9f4f6 through 81c0dc) against the current state of the codebase, Vision tree, and deployed artifacts. Each open item is classified by what blocks it: the psyche's ruling, code work, or process hygiene.

---

## The Landscape

Primary holds no shipping code — it is the coordination workspace that owns discipline, protocols, skills, and the authoritative inventory of ~190 component repositories. The Vision tree has 10 distilled topics (datom, ethos, nexus, protos, orchestrate, remembering, distillation, ethosMonolith, flowNexus, x11) plus ~90 vision-raw files and per-flow vision directories.

The most recent work divides into three streams:

- **The datom/ethos/protos/orchestrate stack** — a multi-flow design-to-realization arc spanning flows 4decf7 → e4a40e → ad19b1 → 1c282d → 6329f1
- **Infrastructure maintenance** — ChatGPT Desktop repairs, Codex updates, Zeus deployments, Claude flow-ID fixes (flows 444e5e, 5a3ee4)
- **Emerging directions** — Wispr overlay integration (81c0dc), flow-division design (b9f4f6), psyche system design (78c93c)

---

## What Landed

### The ProtoformStack (flow 6329f1)

The largest realization in the window. A 14-stop branch train delivered:

| Component | Version | Status |
|-----------|---------|--------|
| protos | 0.15.1 | Merged, deployed |
| datomic | 0.9.0 | Merged, deployed |
| ethos-zero | 1.3.0 | Merged, deployed |
| signal-orchestrate | 0.20.0 | Merged, deployed |
| meta-signal-orchestrate | 0.14.0 | Merged, deployed |
| orchestrate | 0.29.0 | Merged, deployed |
| claude-answers | 0.5.0 | Ported, deployed |
| curriculum-deploy | 0.5.0 | Ported, deployed |

Two deployments to Ouranos succeeded. The orchestrate skill landed in Curriculum. A POC witness verified the MVP reply verbatim.

### Vision Distillations

- **Datom** — full notation, syntax, de/serialization, and Meaning landed in Vision/datom.md
- **Datom Meaning** — parenthesized structured strings, explicitly designed but postponed in code
- **Kinds Identity** — moved from kinds.md to Vision/ethos.md; "kind is an ethos concept" ruled
- **Distillation practice** — 7-rule distillation skill crystallized from flow 4decf7
- **Kind and Naming** — approved and landed in Vision/kinds.md

### Skill Lines Landed

- behavior: synthesis carries each claim's origin (b9f4f6)
- psyche-interraction: "before asking or presenting, explain" (b9f4f6)
- skill-designing: "a new line replaces the line it resembles" (b9f4f6)
- psyche-distillation: fresh words rule (e4a40e)
- main-flow: locating is subflow work (e4a40e)

### Infrastructure

- Claude flow-ID initialization repaired, harness-specific rendering verified (444e5e) — complete
- Codex updated 0.152.1 → 0.153.2, CriomOS flake lock updated, li deployment 159 succeeded (5a3ee4)
- Pi marked deprecated — "pi is slop" (5a3ee4)

---

## What's Open

### Awaiting the Psyche

These items are designed or proposed but need the psyche's word to land.

| # | Item | Origin | State |
|---|------|--------|-------|
| 1 | **Declaration distillate** — example approved, but the landing word for the prose was never given | ad19b1 | Prose re-shown, not landed |
| 2 | **Map merit** — the psyche questioned whether key-value maps have existential merit vs. vectors of structs | ad19b1 | Research dispatched to reports/mapMerit.md; no report exists |
| 3 | **Nexus and sema anatomy** — promised for distillation, never proposed | 4decf7 | Not started |
| 4 | **Situated examples** — plain type, plain kind, kind association, signal type, Nexus type, sema type, mixed type | 4decf7, e4a40e | Never presented |
| 5 | **Dialect skills** — protos, datom, ethos on Curriculum branch DialectSkills (9f14475c) | 6329f1 | Branch exists, not presented to psyche |
| 6 | **Backslash escape in parentheses** — protos writer chose it, vision leaves it undesigned | 6329f1 | To surface to psyche |
| 7 | **"Never carry what you have not understood"** — proposed for spirit, wording not ruled | ad19b1 | Awaiting ruling |
| 8 | **Four anatomy questions and two Intent candidates** from flow-division design | b9f4f6 | Presented, awaiting psyche |
| 9 | **Distillation top-stratum** — three ruled sentences held | b9f4f6 | Awaiting psyche |
| 10 | **Wispr overlay direction chosen** — sticky all-workspace overlay, Meta+letter toggle, status bar, hands-free dictation | 81c0dc | Direction selected, implementation not started, specific keybind not chosen |

### Code — Incomplete or Blocked

| # | Item | Origin | State |
|---|------|--------|-------|
| 11 | **Repin3 cascade** — third re-pin (datomic on protos 0.15.1, ethos-zero, both signal crates, orchestrate importing datomic:Situated, claude-answers, curriculum-deploy, primary flake input) | 6329f1 | Dispatched, never returned or recorded |
| 12 | **Zeus deployment 158 failed** — CopyClosure BuilderUnreachable (Prometheus builder unreachable) | 5a3ee4 | Chronic; same failure as deployment 30 |
| 13 | **Bird UserEnvironment blocked** by Zeus failure | 5a3ee4 | Blocked on #12 |
| 14 | **Wispr overlay implementation** — authorized but no system change made | 81c0dc | Blocked on #10 (keybind not chosen) |

### Process — Orphaned or Undocumented

| # | Item | Origin | State |
|---|------|--------|-------|
| 15 | **Flow 2812d4** — empty directory, no log, no vision, no index | — | Abandoned |
| 16 | **Flow 78c93c** — vision records but no log or index entry | 78c93c | Orphaned |
| 17 | **Flow 1c282d** — vision records but no log | 1c282d | Under-documented |
| 18 | **Machine-generated content rule** — "machine-generated pasted content should not be logged as psyche" | 78c93c | Not landed as skill line |
| 19 | **Witness reuse concept** — natural-language witness indexing with cheap thinking-machine model | 78c93c | Undesigned, unrealized |
| 20 | **read-critical agent description** — deployed line is the one psyche called "really bad"; approved line not deployed | b9f4f6 | Conflict unresolved |
| 21 | **Vocabulary entries missing** — flow-flow, top stratum, program flow, aspect, subflow, child flow | b9f4f6 | Not created |

---

## Vision Coverage

The distilled Vision tree (Vision/) is well-maintained for the core stack — datom, ethos, nexus, protos, orchestrate, remembering, and distillation all have substantive approved entries. But several live design directions exist only in vision-raw or per-flow vision directories:

**Undistilled in vision-raw, carrying standing direction:**
- assembly.md — registry + assembly file design (TryFrom supersedes Create)
- attunement.md — cohesion/health aspect
- flowsNotAgents.md — sessions are flows; aspects not individuals
- mentci.md — Mentci daemon; front-ends not Rust; Qt for Linux
- spirit.md — entry-file placement; skill retires when entry files carry it
- surveyingAllFlows.md — the psyche's desire for flow surveying (Overseer aspect)
- skillDesigning.md, skillVoice.md, skillTypes.md — skill system design

**Empty vision-raw files (topic named, never captured):**
- hexis, flowDaemon, flowArtifacts, flowKnowledge, realizer, nexus, agent-intercom

**Per-flow vision not promoted:**
- 1c282d: Protosizable, Structure → Protoform vocabulary rulings
- 78c93c: witness reuse, machine-generated content
- 81c0dc: Wispr interaction direction

---

## Pattern Notes

Three patterns emerge from the survey:

**The design-to-realization arc works.** Flows 4decf7 → e4a40e → ad19b1 → 1c282d → 6329f1 show a clear progression from distillation through vocabulary ruling to a deployed multi-repo branch train. The distilled Vision entries and the ProtoformStack deployment are evidence of the pipeline functioning end to end.

**Design flows leave tails.** Each design flow generates proposals, anatomy questions, and situated examples that the psyche hasn't ruled on yet. These accumulate — 4decf7's situated examples were still unaddressed two flows later in ad19b1. The per-flow vision directories that hold these items are reachable only by remembering or direct traversal, so they risk being lost.

**Infrastructure issues recur.** The Zeus/Prometheus builder-unreachable failure appeared in deployment 30 and recurred in deployment 158. No root-cause fix has been attempted.
