# Back audit: approved vision since 2026-10-12, and its implementation

Subflow of d68c82. Host clock at writing: 2026-10-18 12:40 CST.

Marks: **W** witnessed by this subflow (code, git, herdr, systemd read now); **C** a claim read in a flow log, not re-witnessed; **I** this subflow's inference.
Status: **Impl** implemented, **Part** partial, **Not** not implemented. "(ctx)" marks a statement whose only implementation is the module being composed into flows.

## What was read

- psyche-context origin/main, 2026-10-12 00:00 -06:00 through bf5da81 (2026-10-17 18:05), every diff (W).
- Approvals: commit messages; flows/d68c82/log.md (lines 286-2188); flows/d68c82/receipts/flow-comments-2026-10-17.edn; logs of da2038, 33752b, 65f93a, 3960eb, e4b7d7, df159a, 875960, 9519a1, c5f24b, 42265e (all C).
- Implementation: origin/main and branches of flow 67b80b, Curriculum 2ec286, messenger-clj c2edb8, field-context 8ef1ca, mind-context d58197, ethos-zero (main 07714b; ethos-proposals, ethos-basics), protos and datom-codec (ethos-proposals), harness, CriomOS 36c21d, CriomOS-home 56d9a9, goldragon dc57e8, chronos; Primary config/main-flow, tools/; running services; `herdr agent list` (all W).

## Deployment facts the rows rely on (W)

- flow-nexus.service runs flow 0.35.11; curriculum-nexus.service active since 2026-10-18 11:58.
- CriomOS-home flake.lock pins psyche-context 53f68b6 (2026-10-16). The served psyche source (/nix/store/3i31df…-source) lacks 23ec573, d5fb9c1, dde8584 and bf5da81: no "Markdown is never shown", no "one datom struct", no "The type ethos". The curriculum unit also references an old psyche-skills source with a skills/ folder (mmjf2h…); which of the two is served is not established.
- mind-context is pinned at e3fcd4f, behind main d58197.
- Each landing reaches flows only after a CriomOS-home re-pin and rebuild (CriomOS-home 56d9a9 and c4b8ea "Pin current book context").
- SKILL_VARIABLES.md names `psyche-context/skills`, `mind-context/skills` and `field-context/skills`. None of these paths exists.
- Book tools (book-check.mjs, book-build.clj, book-code.html, book-fetch.mjs) are modified and uncommitted in Primary.

## Model roles

| # | Landed line (short) | Commit, date | Implied implementation | Evidence | Status |
|---|---|---|---|---|---|
| MR1 | Layer table: Primary Fable/Astra … Quaternary Haiku/Luna low | 228fc49, 10-12 | Flow model configuration; Curriculum roles | Curriculum e11f4f "role depths and models in line with the layer table" (W). Psyche flow Secondary 17c364 runs on Codex, though the table puts Psyche Secondary on Opus and keeps Astra to main flows (W herdr). The conflict is still to be proposed to him (C d68c82 log). | Part |
| MR2 | Terra abandoned | 9bddd08, 10-12 | Flow stable models; checks | flow df20545 "Drop Terra from the stable Codex models"; a CriomOS-home check refuses Terra in the Flow initializer (W). Residue: CriomOS-home pi-models.nix still lists gpt-5.6-terra (W). | Impl |
| MR3 | Vertical fallback routing struck | 1399275, 10-14 | messenger-clj routing | No vertical or nearest-layer routing in messenger-clj src (W, absence) | Impl |
| MR4 | "seat" replaced by "metaflow" or "flow" | 1d6e6fb, c301353, 10-16 | Vocabulary across modules and code | "seat" is still used in flow (26 files), Curriculum (40) and mind-context (9); field-context has none (W). No review record found for this landing (W, log grep). | Part |
| MR5 | A flow named Primary is named by layer, not by effort | 29119ab, 10-12 | (ctx) | Module served (W) | Impl (ctx) |

Owner: Flow 17c364 for the model setting, Curriculum through Mind core 0c85a3 (C).

## Psyche, crystallization, interaction

| # | Landed line | Commit, date | Implied implementation | Evidence | Status |
|---|---|---|---|---|---|
| PS1 | Vision is short-term or long-term | 4ce3789, 10-13 | (ctx) | intent-psyche is composed in all three aspect configs (W) | Impl (ctx) |
| PS2 | A line he approves is psyche, and it leaves the mind or field module it sat in | 366695a, 10-13 | Moving reviewed lines out of machine modules | A sweep found 31 places in 21 machine skills (C 33752b:134). No witness that they were moved. | Part |
| PS3 | Spirit holds beyond this system | 366695a, 10-13 | (ctx) | served (W) | Impl (ctx) |
| PS4 | What he reviews line by line becomes psyche; he skims knowledge proposals | 03aa854, 10-13 | Book form: knowledge shown as modules | field f2abe48 requires exact context modules outside proposals (W). Books 64-66 show knowledge modules (C). | Part |
| PS5 | Crystallization replaces distillation as the method's name | 5eecff3, 10-13 | Renames in field, mind, Curriculum and tools | field-context has no "distillation" (W); Curriculum 753d0e8 (W); mind-context keeps it only in evidence and review files (W) | Impl |
| PS6 | vision-remembering drops the deleted dependency | b615e96, 10-13 | module | W | Impl |
| PS7 | operation- dependencies mapped to compensation-, inquiry- and knowledge- | c91454e, 10-13 | The target modules exist | All five targets exist in field-context and mind-context (W) | Impl |
| PS8 | The context modules belong in a context repository; Psyche's is psyche-context | 455d677, 10-16 | Repository, Curriculum, skill variables | Repository exists and Curriculum reads it (W). SKILL_VARIABLES points at a missing skills/ path (W). | Part |
| PS9 | A question is intelligible on its own | 5a18f9c, 10-12 | (ctx) | intent-psyche-interaction composed (W) | Impl (ctx) |
| PS10 | spirit renamed spirit-core | 38a0f6f, 10-12 | Curriculum, configs | Curriculum tests use spirit/core.md (W) | Impl |

## Design

| # | Landed line | Commit | Status |
|---|---|---|---|
| D1 | Before a design, the unknowns are listed against the complete concept (intent-design) | 28ae42e, 10-12 | Impl (ctx), composed (W) |
| D2 | No one knows ahead that the pieces are enough (vision-design) | 69d9c8b, 10-12 | Impl (ctx) |

## Main flow

| # | Landed line | Commit | Evidence | Status |
|---|---|---|---|---|
| M1 | The seat prompt becomes intent-main-flow, composed into SYSTEM | 2d8ff48, 10-13 | intent-main-flow is in config/main-flow psyche/mind/field.edn, and Curriculum checks compose it (W). The old copy, tools/main-flow-mode/system-prompt.md, still exists and differs only by "seats" (W). Its retirement was ordered (C 33752b:174). The 10-16 ruling "nothing in tools/" applies to it. | Part |
| M2 | A question about conduct is answered from own context and presented to him | a20f9dd, 10-16 | module (W) | Impl (ctx) |

## Context modules

| # | Landed line | Commit | Implied implementation | Evidence | Status |
|---|---|---|---|---|---|
| C1 | Psyche rules over Mind, and Mind over Field; a contradicted line is removed | 03aa854, 10-13 | Audits and removals | none witnessed (I) | Part |
| C2 | Mind's second type is inquiry | 03aa854, 10-13 | mind-context inquiry/ | 10 inquiry modules (W) | Impl |
| C3 | Knowledge modules are audited periodically; a variation goes to inquiry | 03aa854, 10-13 | Periodic audit | No timer or audit found. Field's heartbeat design was sent for ruling (C 42265e:516). | Not |
| C4 | Dense and precise; a statement lives in one module (intent) | bf03117, 10-14 | Composition and enforcement | Composed in all three configs (W). Nothing enforces one statement per module (I). | Part |
| C5 | A reviewed or asked-about subject has a module with room | 37ecd20, 10-14 | Modules exist per subject | No CriomOS vision module (W ls). vision-living-communication was ruled and does not exist (W ls). | Part |
| C6 | A module declares its placement | e1a300e, 10-15 | `placement:` front matter; Curriculum | mind-context has 12 such modules and field-context 19; psyche-context has 0 (W). Curriculum derives SYSTEM for spirit and intent (W src/startup.rs:83). | Part |
| C7 | One folder per type; no folder is called skills | 8bf1b25, 10-15 | Repository layouts; Curriculum; variables | All three main layouts migrated (W). Curriculum tests layout v2 (W). SKILL_VARIABLES is stale, and the old psyche-skills source with skills/ is still referenced by the unit (W). | Part |
| C8 | The vocabulary is context modules; skill is the legacy name | 455d677, 10-16 | Vocabulary | "skill" remains in variables, CLAUDE.md and Curriculum (W) | Part |
| C9 | A role section per layer, Primary to Quaternary, plus topic sections | 455d677, 10-16 | role/ by layer | field-context and mind-context role/ folders are flat; psyche-context has no role/ (W) | Not |

Owner: Curriculum lane under Mind core 0c85a3; Field 42265e for pins (C).

## Flow

Includes three lines he approved and that are not landed: F16-F18, from da2038 book 5, ruled 2026-10-16. P1 was "a good long-term vision"; P2 and P5 were "This is good" (C da2038:476). psyche-context vision/flow.md still carries the old wording (W).

| # | Line (short) | Commit, date | Evidence | Status |
|---|---|---|---|---|
| F1 | A flow is one linear chat; many flows resemble a synthetic intelligence | 4077058, 10-14 | (ctx) | Impl (ctx) |
| F2 | Anybody may call Flow; the CLI checks the calling process | 67d358d, 10-14 | Identify resolves through the Herdr server ancestor (flow 09bbe9f) (W commit). On 10-17 sends from d68c82 and Field were refused CallerUnknown/Unidentified (C). | Part |
| F3 | Flow exposes the harness; Message uses it; later Message sends through Flow's socket | 67d358d, 10-14 | Flow 0.35.7 adds a send tool (W). messenger-clj a6f3475 routes Flow-managed sends through Message (W). 22 flows remain on the old route (C book 65). | Part |
| F4 | A needed metaflow is started whether running or not, and fed its modules and prompt | e3823d6, 10-14 | Fresh wake works on 0.35.10 (C). waking.rs:103 never wakes a Primary (W). The idle-awake drain defect left sends Queued; 804eb9's book never arrived (C). | Part |
| F5 | Flow is for starting flows cheaply: clean, lean, specialized | 2faca02, 10-15 | Direct-text starter in 0.35.0 (W). Lean flows were ordered 10-18 and are not built (C). | Part |
| F6 | Psyche, Mind and Field go under one metaflow | 455d677, 10-16 | Flow holds 4 flows and 22 are on the old route (C book 65). 17c364 and 804eb9 are launched by Flow (W herdr). | Part |
| F7 | Queued vision is injected with the waking request; no waking per accumulation | 455d677, 10-16 | waking.rs wakes only for Order, Question, Psyche, Psyches (W). The drain defect is open on branch flow-crash-safe-drain-17c364 (W). | Part |
| F8 | To the Nexus, a module's location is its registry entry | 455d677, 10-16 | Curriculum 925a55c "compose context by registry IDs over the wire" (W) | Impl |
| F9 | The system prompt is composed of typed modules; its anatomy is in ethos, from a study | 455d677, 10-16 | Composition by type (W). No ethos anatomy drawn from a study was found (I). | Part |
| F10 | A main flow's part of the prompt is not passed to subagents | 455d677, 10-16 | Separate role compositions in Curriculum (W). The exclusion itself is not witnessed (I). | Part |
| F11 | Modules live outside the flow repository, so a change causes no Nix rebuild | 455d677, 10-16 | They are outside (W). Every landing needs a CriomOS-home pin and rebuild (W flake.lock, 56d9a9). | Part |
| F12 | Long term a hash check; short term none | d5fb9c1, 10-17 | Curriculum computes sha256 payload digests (W src/claude_agent.rs) | Impl |
| F13 | A title is one datom struct `{ Psyche core Secondary <id> }` | dde8584, 10-17 (+29119ab) | 24 of 26 herdr titles have this form. Field 42265e and Mind 41fa34 read `Field.{ Sol 42265e }` (W). The line is not in the served pin (W). | Part |
| F14 | A flow id is six characters, lengthened when two collide | dde8584, 10-17 | harness src/flow_id.rs: a Collision extends the candidate, with a test (W) | Impl |
| F15 | The ancestor-naming sentence is deleted | dde8584, 10-17 | The heading is left empty; a ruling was asked (C) | Impl |
| F16 | Unlanded: a metaflow sleeps as soon as its turn ends with the harness idle and an empty queue | ruled 10-16 | waking.rs sleeps_at Idle/Done (W). Codex seats are not slept (C da2038:215). | Part |
| F17 | Unlanded: an asleep metaflow wakes on order, question or his words; a result or notice waits | ruled 10-16 | waking.rs:93-100 (W) | Impl |
| F18 | Unlanded: waking queues for that metaflow while Flow serves every other request | ruled 10-16 | Not witnessed (I) | Part |
| F19 | A topic goes idle; whether to wake it is judged by a small model | 9bba4bf, 10-12 | No small-model wake judgment in flow (W grep; waking by request type only) | Not |
| F20 | A topic name is camelCase and uncapitalized | 9bba4bf, 10-12 | 0.34.5 lowercases the topic in native titles (W). Live topics Spirit, Nexus, Tools, Prototyping, Communication, PrimaryCommitting and InstructionWitness are capitalized (W herdr). | Part |
| F21 | A flow id is the hash of the session id; Flow chooses the session id where it can; no flow declares its id | 9bba4bf, 10-12 | flow-id claim helper and harness flow_id.rs (W). Choosing the id before start is not witnessed (I). | Part |
| F22 | Closed set of request types; Flow owns lock and delivery; Message subscribes to Flow's events | 9bba4bf, 10-12 | Request types are in Flow (W). Message's subscription is not witnessed (I). | Part |
| F23 | An idle metaflow gets its whole queue oldest first; refresh queues | 9bba4bf, 10-12 | Drain defect: Queued messages stayed undelivered 10-17 and 10-18 (C) | Part |

Owner: Psyche flow Secondary 17c364 on Codex, and Mind flow Primary 9896d8 (W herdr). There is no Mind flow Secondary (W).

## Books and Illustrator

| # | Line | Commit | Evidence | Status |
|---|---|---|---|---|
| B1 | A book is a proposal into modules, red and green | 03aa854, 10-13 | book-build renders red and green. book-check refuses prose outside proposals, and field f2abe48 requires it (W). The latest tool changes are uncommitted (W). | Impl |
| B2 | No verbatim quote; records not shown | 574ad11, 10-14 | book-check refuses only block quotes (`quote-block-in-book`, W line 150). Inline quotes pass (I). | Part |
| B3 | References in references/, archived on landing | 574ad11, 10-14 | references/ directories exist (W). Archiving on landing is not witnessed. | Part |
| B4 | Figure grammar; a figure keeps every box, label and arrow | 8bd55fe, 10-13 | field role/illustrator-faithfulness.md says "free of the source boxes and arrows" (W), which contradicts it. Fable's «What a book is» 2nd proposes the fix (C). | Part |
| B5 | An idea reaches him as a picture first; colours mean the same everywhere | 5fdc73f, 10-16 | Standards in field 24d5820 (W commit). «Ethos categories and sugar» was published 10-18 with no figure (C). A no-figure refusal exists in book-build, uncommitted (C). | Part |
| B6 | A proposal is drawn as well as written | 5fdc73f, 10-16 | No per-proposal figure requirement in the tools (I) | Part |
| B7 | A proposal touching code shows the code | d5fb9c1, 10-17 | No tool check (I) | Part |
| B8 | Every comment redoes its book; a new topic gets its own book | d5fb9c1, 10-17 | The relay goes only to d68c82. 46 of 66 Flow comments were not forwarded (C receipts/comment-routing-2026-10-17.md). Book 61 is unruled. | Part |
| B9 | Markdown is never shown in a code block | bf5da81, 10-17 | `markdown-in-code-block` refusal in book-check (W, uncommitted). The line is not in the served pin (W). | Impl |
| B10 | The first edition is mostly questions | 8e8234b, 10-12 | (ctx) | Impl (ctx) |
| B11 | The book is the center of development | 0a6a8a3, 10-12 | (ctx) | Impl (ctx) |

Owner: d68c82 subflows edit Primary tools. Field 42265e owns the role modules. Illustrator ac0558 and Publisher c6d989 were closed after they failed (C). The Illustrator is callable by any caller through Curriculum 379f47 (W).

## Messaging

| MS1 | A hash or identifier in a message is six characters | f37708c, 10-16 | messenger-clj prints attempt ids at 12 characters (W core.clj:511,659). 160 of 512 messages to d68c82 carried full hashes (C). | Part |

## Ethos, datom, protos

| # | Line | Commit | Evidence | Status |
|---|---|---|---|---|
| E1 | datom: any whitespace may follow the separator | 23ec573, 10-16 | protos ethos-proposals d8a290d; datom-codec ethos-proposals repins it (W). Neither main has it (protos main 10-02) (W). | Part |
| E2 | protos: whitespace, line break included, may follow a separator | 23ec573, 10-16 | same | Part |
| E3 | `Type` is a single-field variant carrying one declaration | 23ec573, 10-16 | ethos-zero ethos-proposals fixtures/commit-message.ethos and lib.rs:155 (W). Not on main (W). | Part |
| E4 | Unlanded ruling: long term every trait in Ethos; short term do without | ruled 10-16 (C d68c82:1957) | ethos-basics ca11693 "refuse a declared type that bears no trait" (W branch). ethos-zero generates no traits; Flow has 209 hand-written traits (C). | Part |

Owner: Psyche ethos Secondary 804eb9, whose subflows commit to ethos-zero branches (C). There is no Mind ethos flow (W).

## Nexus

| N1 | The Nexus is an architecture; everything made is a Nexus | d5fb9c1, 10-17 | Flow, Curriculum, Message and Orchestrate run as Nexus services (W systemd). messenger-clj and Primary tools/*.mjs and *.clj are not Nexuses (W). | Part |
| N2 | A Nexus's vision is split by its code modules | d5fb9c1, 10-17 | vision/nexus.md is one file (W) | Not |

Owner: Psyche nexus Secondary a275c0. 058f16's pane is still listed (W). There is no Mind nexus flow.

## Clojure

| CL1 | One shared construct mapping: Ethos to Malli, Datom to EDN, recoverable | 4d80d68, 10-14 | Only demonstrations exist, in flows/5b9075/handoffs (W). No repository and no knowledge/clojure module (W). | Part |

Owner: Mind Prototyping e4b7d7 and 5b9075.

## CriomOS (Git server, Nix builds)

| G1 | The cluster's Git server: role GitServer, Gitolite, cluster keys, no web interface, GitHub mirror | 7d4dc5b, 10-16 | CriomOS modules/nixos/repository-receive.nix runs Gitolite on capability `PersonaDevelopment.[ GitoliteServer ]` in goldragon (W). It is not a GitServer role, it takes the first admin key only, and mirror.nix is disabled on all hosts (W). Not live-probed. | Part |
| NB1 | Builds live in the remote builder's store; one registry profile; the rest collected by recency and frequency | f81b7b2, 10-16 | The remote builder exists (NixBuilder variable). There is no registry profile or recency/frequency collector in CriomOS or CriomOS-home (W grep). nix-heuristic-gc has no frequency input (C). | Part |

Owner: Field core 42265e and 44cda5. There is no CriomOS vision module.

## Chronos

| CH1 | Unlanded, ruled 10-18: «Chronos, the golden example» 4th "may land" | none | There is no vision/chronos.md (W). chronos main a5cf51 (09-06); the newest branch 500094 (10-04) has `todo!` ×6 in src/sky.rs (W). | Not |

Owner: Psyche chronos Secondary 504f11 (984e88 is still listed) and Mind Prototyping (C).

## Topic flows (W herdr agent list, flows/*/continuation.json)

| Topic | Size (I) | Psyche flow | Mind flow | Gap |
|---|---|---|---|---|
| Flow | big | flow Secondary 17c364 (on Codex) | flow Primary 9896d8 | No Mind flow Secondary, though a Primary starts only after its Secondary. Psyche Secondary runs on Astra. |
| Ethos | big | ethos Secondary 804eb9 | none | Mind ethos topic flow missing |
| Books and Illustrator | big | none (d68c82 does it) | none | No topic flow in any aspect; Field Illustrator and Publisher closed |
| Context modules (Curriculum, pins) | big | none (d68c82) | none (Mind core 0c85a3) | Mind topic flow missing |
| Nexus | medium | nexus Secondary a275c0 | none | Mind nexus flow missing |
| Chronos | medium | chronos Secondary 504f11 | Prototyping e4b7d7 and 5b9075 | covered through Prototyping |
| Messaging | medium | none | none (Mind Tools 47d946/0430eb, scope unknown) | unclear owner |
| CriomOS | small now | none | none (Field core) | no vision module |
| Model roles, Psyche | small | core d68c82 | none | none |

These are listed as live panes but were retired or replaced (W herdr, C logs): da2038, 65f93a, 058f16, 984e88. Field 42265e and Mind 41fa34 keep the old title form.

## Not done in this subflow

- flow-evidence was not loaded, because the Skill tool is unavailable here.
- Provenance receipt evidence: unavailable.
- No Beads were opened or closed.
- No build or test was run.
- No host or service was probed live, except systemd units and herdr on Ouranos.
