# 352 — Intent log audit: flagged for psyche review

## Frame (per psyche 2026-05-26 records 717-719; audit-don't-delete discipline)

Per psyche 2026-05-26 (records 717, 718, 719): walk the Spirit intent
log; flag suspected duplicates, misalignments, and hallucinated records
for psyche review; do not delete or supersede anything. Only the psyche
supersedes intent. The deliverable is this flagged-records report.

Records 712-719 of 2026-05-26 set the audit baseline: schema defines
data types only (713); the schema-defines-effects direction
(EffectTable / FanOutTargets / StorageDescriptor as authored features)
was agent-hallucinated, not psyche-authorized (716, 718); agents must
not infer to close incomplete designs (718); the audit FLAGS, never
supersedes (719). Records authored during the 656-705 schema-
crystallization arc are the primary suspect zone — that's where most
of the drift accumulated.

This audit walks the v0.2.0 spirit database (records 1-719,
2026-05-21 through 2026-05-26 09:56:45 UTC) as the canonical intent
surface going forward. The v0.1.0 database is the cutover-source and
covers the same record set; legacy `intent/*.nota` files are handled
separately by the timestamp-preserving extractor (bead primary-h1vl).

## Scope walked

Walked topic-by-topic in decreasing-record-count order. Per topic the
walk read every record description, looked at certainty and kind,
and cross-checked against:
- record 716 (psyche-authorized vs agent-drifted distinction)
- record 718 (don't-infer-from-incomplete-design)
- explicit supersession chains within the log
- the five-kind classifier (Decision / Principle / Correction /
  Clarification / Constraint)
- the work-instruction-vs-intent test from `skills/intent-log.md`

Topics walked end-to-end:

| Topic | Records | Notes |
|---|---|---|
| schema | 96 | Schema-crystallization arc (records 656-714) is the densest drift zone. |
| workspace | 94 | Largely clean psyche statements; some retired-lane duplicates. |
| component-shape | 61 | Has the InteractTrait/EffectTable/FanOutTargets cluster (660-666). |
| persona | 53 | Several supersession chains; some persona-pi overlap. |
| nota | 46 | Bracket-string discipline arc has many incremental duplicates. |
| spirit | 42 | Acknowledgement-shape cluster has obvious duplicates. |
| signal | 43 | Tier-1 short-header arc has incremental records. |
| schema-language | 22 | Overlaps with `schema` and `nota` — record housing problem. |
| cloud | 20 | Two pass clusters (281-296 then 679-689) describe same direction. |
| reports | 20 | Context-maintenance principle restated several times. |

Smaller topics scanned for outliers and synthesis-style description
patterns:

- intent (4), intent-log (7), orchestrate (8), workflow (8),
  persona-pi (14), version-control (5), naming (6), testing (9),
  agent-contract (5), reporting (4), versioning (4), domain (4),
  domain-criome (9), beads (4), deploy (12), operator (7),
  architecture (3), designer (2), sema (6), signal-short-header (4)
- single-record agent-introduced narrow topics: 11 records (listed
  below in "Suspected hallucinations — narrow synthesis topics")

## Flagged duplicates

The audit groups duplicates by intent-substance cluster. Each cluster
lists record IDs, the shared substance in one line, and a
recommendation. The psyche picks which records survive; the audit
does not pick.

### D1 — Spirit acknowledgement shape (token-cheap, no echo)

Records: **14 + 15 + 17 + 18 + 674** (Maximum certainty each)
- 14 Correction [RecordAccepted schema should not produce nested echo noise]
- 15 Constraint [Spirit accept replies must be token-cheap]
- 17 Constraint [Spirit write acknowledgements should be token-cheap and should not echo submitted intent content]
- 18 Correction [Spirit accepted-record reply schema should avoid nested summary-shaped acknowledgements]
- 674 Decision [Spirit record acknowledgements stay terse]

All five say the same thing in slightly different words on the same
day (2026-05-21). Likely one psyche statement captured five times as
the agent re-wrote it across the conversation. Recommend: keep 17
(most explicit and broadest) plus 674 (recent Decision), supersede the
other three; OR keep just 17.

### D2 — Spirit version tags (schema-aware versioning)

Records: **13 + 16 + 31**
- 13 Decision [Spirit releases need schema-aware version numbers] Maximum
- 16 Principle [Spirit releases need version tags that signal schema compatibility] Medium
- 31 Constraint [Deployed Spirit versions should be tagged before schema migration planning] Maximum

Same substance, three different kinds + certainties on 2026-05-21.
Recommend: keep 13 OR 31; the Principle 16 reads like agent-rewriting.

### D3 — Intent capture uses Spirit

Records: **19 + 167 + 168**
- 19 Correction [Intent capture should use Spirit during this session] Medium
- 167 Correction [Intent logging uses Spirit] Maximum
- 168 (workspace topic) Correction [Intent logging uses Spirit] Maximum

168 and 167 are word-for-word identical (different topics). 19 says
the same thing with weaker certainty. Recommend: keep 167 OR 168
(probably 168 since `workspace` is the natural topic for substrate
choice). Supersede 19.

### D4 — Bracket-string discipline (the long arc)

Records: **22 + 23 + 24 + 25 + 26 + 27 + 34 + 66 + 67 + 81 + 142
+ 401 + 677 + 690 + 698 + 701 + 705** (all `nota` topic, 2026-05-21
through 2026-05-25)

This is a real design arc with genuine incremental decisions:
- 22-34 are exploration (Minimum→Medium); not duplicates per se but
  exploration that 26+27 resolved at Maximum.
- 66 + 67 + 142 + 401 + 677 + 690 + 698 reinforce the same rule
  (avoid double-quote NOTA strings) repeatedly across sessions.
- 698 is most explicit ("brackets ARE the string form; quotation
  marks do NOT form string types"); 705 explains the
  embedding-safety property; 701 covers the shell-double-quote rule.

Recommend: psyche may want to retain 26, 27, 698, 701, 705 (the load-
bearing rules) and supersede the exploration chain (22-25, 34, 66, 67,
81, 142, 401, 677, 690). Alternatively, leave everything (repetition
IS signal per `intent-log.md` "Record everything").

### D5 — Cloud component direction (two pass clusters)

Records: **281 + 282 + 283 + 294 + 295 + 296** (Medium/Minimum,
2026-05-21) and **679-689** (Maximum, 2026-05-25).

Both clusters cover: cloud component scope, Cloudflare DNS first
target, provider build-time opt-ins, cache-with-Cloudflare-as-source-
of-truth, env-var credential. The 2026-05-21 cluster is exploration at
Medium; the 2026-05-25 cluster is the same content at Maximum.

Specific overlaps:
- 281 + 294 + 296: cloud owns cloud-provider API management
- 282 + 685: Cloudflare DNS first
- 283 + 295 + 342: provider build-time opt-ins
- 686 + 681: cache is provider-backed

Recommend: keep 294, 295, 296, 311 (Mutate/Query split), 325 (owner
signal), 342 from the first cluster; the 679-689 cluster restates them
at Maximum and adds the production-slice work-instructions (679, 682,
683, 684, 685, 687, 688, 689). Either supersede the earlier Medium
records or supersede the later Maximum cluster — the duplication is
clear.

### D6 — Persona naming (Persona, persona-daemon)

Records: **215 + 216**
- 215 Correction [The engine-manager daemon's canonical short name is 'Persona' ...] Maximum
- 216 Clarification [Persona ... is composed of two binaries from the persona repo: 'persona' (CLI) and 'persona-daemon' ...] Maximum

215 names the entity Persona; 216 elaborates that it's composed of two
binaries. Same psyche moment; 216 mostly refines 215. Recommend: keep
216 (which absorbs 215's content) or keep both since 216 explicitly
extends 215.

### D7 — Persona is a permissioned system daemon

Records: **238 + 239**
- 238 Clarification [Persona is a permissioned system daemon] Maximum
- 239 Constraint [Persona runs as a permissioned system daemon (privileged, supervising component daemons)] Maximum

Word-for-word near-duplicates; same day. Recommend: keep 239 (richer
phrasing, Constraint is structurally stronger than Clarification here).

### D8 — Agent identity & cryptographic basis

Records: **124 + 125 + 134** and the persona-pi 76-79 set
- 124 Principle [Not all calls labeled 'agent' are agents — runtime functions vs cryptographically-identified agents]
- 125 Decision [Long-lived agents have cryptographic identity tied to Criome public key]
- 134 Correction [Criome cryptography is BLS12-381, not Ed25519] (corrects 125)
- 38 Decision [Each agent has its own Criome identity] (Medium)

124 + 125 are tightly related — 125 implements what 124 distinguishes.
38 is at Medium certainty saying essentially what 125 says at Maximum.
Recommend: keep 124 + 125 + 134; supersede 38 (covered by 125).

### D9 — persona-pi initial profile

Records: **44 + 47** (persona) and **76 + 77 + 78 + 79** (persona-pi),
plus **223 + 224 + 225 + 226** (persona-pi later restatement)
- 44 Principle [Per-role model selection — Claude designer, Codex advisor, GPT-latest+MaxThinking is Pi default]
- 47 Decision [Persona Pi default config — GPT latest with Maximum Thinking]
- 76 Principle [Persona Pi is the Codex advisor harness] Maximum
- 77 Principle [Composite design should run Claude and Codex in parallel] Maximum
- 78 Principle [Pi should expose terminal-cell + harness API surfaces] Maximum
- 79 Principle [Pi extension APIs adapted into signal-tree vocabulary] Maximum

76-79 are the same substance as 43+44+45+46+47 captured under the
`persona-pi` topic instead of `persona`. Possibly the agent captured
each piece twice, once per natural topic. Recommend: keep one set;
psyche picks topic preference (`persona-pi` is more specific).

### D10 — Lane identifier policy (forever vs reusable)

Records: **117 + 118 → 211** (explicit supersession chain)
- 117 Decision (workspace) [retired lane identifiers can disappear, lane name rolls forward]
- 118 Decision (persona) [Lane identifiers in persona-orchestrate's registry are reserved forever ...]
- 211 Correction (persona) [Lane identifiers in persona-orchestrate's registry are NOT reserved forever ... supersedes intent 117/118]

This supersession is already explicit in 211. Recommend: psyche
confirm that 117 and 118 are formally retired; this is the cleanest
existing supersession candidate in the log.

### D11 — DeepSeek-as-library

Records: **151 → 157 → 158** (explicit supersession chain)
- 151 Decision [DeepSeek-as-library subsumed into persona-pi triad] Maximum
- 157 Correction [Record 151 is superseded; intent is workspace-native Persona LLM client library]
- 158 Decision [New component: persona-llm-client]

Already explicit in 157. Recommend: psyche confirm 151 is retired
(157 already says so).

### D12 — Context maintenance / report reduction

Records: **107 + 119 + 120 + 122 + 130 + 362 + 646 + 651**

All eight say variants of "reports are not an accumulating archive;
context maintenance reduces / refreshes / agglomerates active reports".
107 is the foundational principle; later records restate. Recommend:
keep 107 + 362 (which explicitly authorises aggressive consolidation)
and 218 (which moves diagram/table/heading content into reports);
supersede 119, 120, 122, 130, 646, 651.

### D13 — Schema-language records duplicate schema records

The `schema-language` topic (22 records, 425-466) duplicates a lot of
`schema` and `nota` records covering the same syntactic decisions:
- 440 (no outer wrapper) duplicates schema 449, schema 458, nota 433
- 441 (header root is enum-vector) duplicates schema 472, schema 477
- 425 (curly-brace map name-value) duplicates nota 418
- 426 (no comments) duplicates nota 419
- 452-457 (cluster of syntactic rules) duplicates nota 429, 434, 435, 437

Recommend: psyche may want to retain ONE topic for schema-syntax. The
`schema-language` topic and the schema-syntax portion of `nota` should
likely collapse into `schema` or a dedicated `schema-syntax` topic.

### D14 — Designer/operator branch-and-rebase workflow

Records: **516 + 518 + 519** (workspace)
- 516 Decision [Designers work on feature branches; operators maintain main]
- 518 Decision [designers work on their own feature branches in ~/wt; operators create maintain and rebase for main]
- 519 Decision [second-designer port orchestrate to schema engine + no-downtime upgrade in parallel with operator]

516 and 518 are the same intent, captured by two agents in the same
turn (the reflexive duplication pattern mentioned in AGENTS.md). 519
is a separate dispatch order. Recommend: keep 518 (richer); supersede
516 OR keep both for the lineage.

### D15 — Designer end-of-pass commit-and-push

Records: **578 + 581 + 583**
- 578 Principle (workflow) [Agents finish dirty passes by committing and pushing their work] Maximum
- 581 Constraint (workflow) [Agents commit and push at the end of each dirty work pass] Maximum
- 583 Principle (workspace) [every designer pass ends with commit-and-push ...] Maximum

Same substance, three records same day (2026-05-25). Recommend: keep
583 (workspace topic, richest phrasing); supersede 578 + 581.

### D16 — domain-criome no-provider-vocabulary

Records: **321 + 346 + 352**
- 321 Constraint [domain-criome runtime excludes provider APIs and direct CLI store access]
- 346 Constraint [Keep domain-criome contract vocabulary provider-neutral and record-only]
- 352 Constraint [Domain-criome contracts keep provider vocabulary out]

Three statements of the same constraint on the same day. Recommend:
keep 346 (most explicit); supersede 321 + 352.

### D17 — signal-persona-auth rename pass

Records: **261 + 264 + 269 + 277 + 278**

Layered rename arc; 264 names the rename (auth → origin), 269 files
operator beads for the full pass, 277 bundles primary-fka1.1 +
primary-7ru6, 278 says the same as 277 at Medium. 277 supersedes 278.
Recommend: keep 262 (forbid-abbreviation principle, general), 264
(rename decision), 277 (bundling); supersede 261 (rename announce
already absorbed into 264), 269 (operator work-order), 278 (duplicate
of 277).

### D18 — Persona Pi YOLO + safety prompts

Records: **306 + 333 + 336**
- 306 (workspace) Correction [Pi operator-safety must not ask permission solely because a repository is dirty]
- 333 (persona-pi) Correction [Pi operator-safety dirty-repository prompt must disappear from live Pi]
- 336 (persona-pi) Constraint [Pi operator-safety must not create repeated confirmation burden during normal work]

306 + 333 are word-for-word duplicates across topics. 336 is the
broader rule that subsumes them. Recommend: keep 336; supersede 306 +
333 OR keep 336 + 333.

## Flagged misalignments

Records that contradict newer corrections or each other. The audit
flags; psyche decides what survives.

### M1 — Schema-defines-effects cluster contradicted by 713/715/716/718

Records 660-665 captured the InteractTrait + EffectTable + FanOut
direction at Maximum certainty on 2026-05-25 13:34:55. Within minutes
record 666 (2026-05-25 15:48:42) explicitly retracted 660 and 665
("The InteractTrait abstraction was overengineered; methods are
interactions") but PRESERVED 661 (effect-table match-driven dispatch)
and 662 (actor fan-out execution) as "still valid".

Then on 2026-05-26 records 713, 715, 716 came in. 713 says **schema
defines data types ONLY — no effects no fan-out targets no effect
tables ... EffectTable + FanOutTargets ... are drift that needs
retraction**. 716 says **the psyche never authorized [the schema-
defines-effects] direction; agents hallucinated it**.

This means:
- **660** (InteractTrait, InteractionActor mediation) — already
  retracted by 666 internally; ALSO contradicted by 668 ("the
  'interact trait' formulation from records 660 + 665 + 666 was the
  wrong shape"). Now further contradicted by 713/716.
- **661** (EffectTable match-driven dispatch — kept by 666) —
  contradicted by 713 ("no effect tables") and 716 (psyche never
  authorized).
- **662** (Actor fan-out execution — kept by 666) — contradicted by
  713 ("no fan-out targets") and 716.
- **663** (workspace Constraint to embed schema-crystallized
  principles EVERYWHERE) — explicitly names "interact trait and
  interaction actor mediation; effect table mapping; actor fan-out
  execution" as load-bearing principles to embed in ESSENCE / AGENTS
  / skills / per-repo INTENT / ARCHITECTURE files. Per 716, those
  three principles were agent-introduced and never authorized by the
  psyche. So 663's "embed everywhere" mandate is built on
  hallucinated substance.
- **664** (workspace Decision to dispatch a CONVERSION OF HERESY
  sweep) — likewise built on the same hallucinated substance; the
  sweep's scope explicitly includes "(e) interact-trait plus
  interaction-actor mediation, (f) effect-table match-driven
  dispatch, (g) actor fan-out execution" — three principles that 713
  and 716 explicitly retract or never-authorized.
- **665** (refines 660) — already retracted by 666.
- **666** (retracts 660 + 665; KEEPS 661, 662) — 661 + 662 retention
  is contradicted by 713 + 716. 666 itself is partially still valid
  (the InteractTrait retraction part) but the "still valid" portion
  (661 + 662 preservation) is now superseded.
- **668** (says 660+665+666 was wrong shape; introduces "schemas
  warrant from need-to-interact" reframing) — 668 itself may survive
  but cites 660/665/666 internally; the reframing-on-cited-records
  needs review.
- **669, 670** (Components have TWO schema categories; multiple
  schemas per repo) — these survive the schema-defines-effects
  retraction since they're about schema scope not schema-defines-
  runtime-behavior. Likely keep.
- **710** (Schema-driven POC must include EffectTable closure tests)
  — directly contradicted by 713. Recommend: psyche supersede the
  EffectTable-closure-test portion.
- **511** doesn't exist in this analysis; the actual sweep records
  are 663+664; both should be reviewed in light of 716.

The cleanest action: **psyche supersede 660, 661, 662, 663, 664, 665,
710** (the schema-defines-effects cluster + its embed-everywhere
mandate). 666 stays as the historical InteractTrait retraction
(though its "still valid" carve-out for 661+662 is now itself
superseded). 668 + 669 + 670 stay as the schemas-warrant-per-channel
reframing.

**This is the highest-impact flag in the audit.** The drift cluster
includes 6+ Maximum-certainty records, two of which (663, 664)
mandate workspace-wide propagation of the very principles that 713
and 716 say were never authorized. If left in the log, future agents
encountering 663 + 664 will dispatch heresy-sweep work on substance
the psyche has retracted.

### M2 — Schema component-shape principles 659 (two languages) survives partially

Record 659 says every component has TWO schema-derived vocabularies:
INTERNAL EFFECT language + EXTERNAL WIRE language. Record 666 says
two-languages "still valid". Record 669 refines this — components
have EXTERNAL (wire + storage) and INTERNAL (actor messages) schema
categories; two-languages becomes "wider taxonomy" of one-schema-per-
channel. Record 670 lands the storage-with-daemon convention.

Then 713 says "schema defines data types ONLY", which doesn't strictly
contradict 659 (data types organized into different vocabularies is
still data types) — but the INTERNAL "EFFECT language" framing in
659 reads as schema-defining-effects, which 713 retracts. The "effect
vocabulary" wording in 659 is suspect.

Flag: psyche review whether 659's "INTERNAL EFFECT language"
phrasing should be clarified — the substance of internal actor
message vocabularies stays valid (669 + 670 cover that) but the
"effect" framing carries the now-retracted overlap.

### M3 — InteractTrait survivors in 652, 653, 654, 655

Records:
- 652 (interact-trait-universal-interaction) Decision [Universal
  Interact trait: every object implements interact(other_object)...]
- 653 (match-as-logic-substrate) Principle [Most workspace logic is
  MATCHES between two domains...]
- 654 (typed-unavailable-at-unmatched-cases) Decision [When a match
  has no defined behavior, response is TYPED error]
- 655 (async-state-query-via-actor-system) Principle [When an
  interaction needs engine state including outbound queries, becomes
  ASYNC...]

All four authored 2026-05-25 13:00-13:01, immediately before the
schema-crystallization cluster (656-662). 652 (Universal Interact
trait) is exactly the InteractTrait abstraction that 666 retracted
("The InteractTrait abstraction was overengineered; methods are
interactions").

653, 654, 655 are partial survivors — `match-as-logic-substrate` is a
broader pattern that may stand independently of InteractTrait;
`typed-unavailable-at-unmatched-cases` is a generic enum-typed-error
discipline; `async-state-query-via-actor-system` is the actor-system
async pattern. The narrow synthesis-topic shape of each (one record
per topic, verbose synthesis description) makes them feel agent-
introduced even where the substance survives.

Flag: psyche review whether 652 should be superseded along with 660
(both InteractTrait); 653/654/655 may stand but should perhaps move
into broader topics (`component-shape` for matches; `signal` for typed
errors; `persona` for actor-system async).

### M4 — workspace 246 (Design C rejected) vs 252 (Design D adopted)

Records 246 + 252 land back-to-back: 246 rejects "Design C" (client-
side discovery), 252 adopts "Design D" (Persona-orchestrated FD
handoff). Both are at Maximum. The 246-252 pair is internally
consistent (D not C) but reads as the kind of fast-moving design churn
where the psyche may want to keep just the positive (252) and let the
negative-decision (246) retire as historical lineage absorbed by the
positive decision.

Flag: psyche may collapse 246 + 252 into just 252.

### M5 — workspace 86 + 117 + 211 lane-naming churn

Records 86 (second-designer assignment), 117 (lane retirement
rules), 211 (lane retirement rules SUPERSEDES 117/118). 86 + 117 are
mostly historical churn that 211 already retired. The 211 record
itself notes 117/118 supersession. Flag: psyche confirm 86 and 117
are formally retired; their substance lives downstream.

## Flagged suspected hallucinations

The strongest hallucination signals are: (a) records whose description
reads like agent-synthesis ("the X principle implies that Y must also
hold"); (b) verbose multi-paragraph descriptions; (c) narrow agent-
introduced topics with a single very-long record; (d) records that
"close the loop" on a half-specified design; (e) topics that grew
suspiciously fast in a short period.

### H1 — Narrow synthesis topics from the schema-crystallization arc

Each of these is the SINGLE record on its own narrow topic, all
authored 2026-05-25 within the schema-crystallization arc:

| ID | Topic | Cert | Pattern |
|---|---|---|---|
| 587 | macro-decides-projection-module-location | Maximum | Single-record narrow topic, verbose synthesis description |
| 603 | macro-two-phase-dispatch | Maximum | Same pattern |
| 604 | micro-macros-composable | Maximum | Same pattern |
| 605 | macro-lazy-loading-with-index-pass | Maximum | Same pattern |
| 606 | macro-library-core-vs-extension | Maximum | Same pattern |
| 607 | macro-output-module-per-schema | Maximum | Note: id 620 in my dump, may be 607 vs 620 — flag both |
| 614 | field-names-derived-from-type-names | Maximum | Same pattern |
| 615 | divergent-field-names-via-newtype | Maximum | Same pattern |
| 616 | everything-reduces-to-structs | Maximum | Same pattern |
| 620 | macro-output-module-per-schema | Maximum | Same pattern |
| 621 | fully-qualified-names-internal-representation | Maximum | Same pattern |

11 records, 11 narrow synthesis topics, each Maximum certainty. The
pattern (one verbose synthesis record per agent-named topic) is the
hallucination signal: each topic name reads like an agent's
section-heading-for-its-own-design-thinking rather than a name the
psyche reasons about. The descriptions read like the agent's
internal-design synthesis prose.

Some of the substance MAY survive (field-name-from-type-name is
plausibly psyche intent per the discussion of struct field syntax;
two-phase macro dispatch may also be load-bearing). The flag is the
SHAPE — too narrow, too verbose, too synthesised — not necessarily
the content.

Flag: psyche review the substance per record; consider consolidating
into the `schema` or `nota` topic (or a unified `schema-syntax`
topic) and dropping the synthesised single-record topics.

### H2 — workspace 663 + 664 (vast conversion of heresy)

663 is a Maximum Constraint mandating EMBED EVERYWHERE for the
schema-crystallized principles. 664 is a Maximum Decision
dispatching a workspace-wide HERESY-CONVERSION sweep. Both rest on
the schema-defines-effects cluster (660-662) which 713 + 716 say was
agent-hallucinated. The grandiose "vast conversion of heresy"
framing in 664 is the verbose-synthesis pattern.

Flag: psyche confirm 663 + 664 are retired with the underlying
cluster (M1). If retained, they direct sweeps on retracted substance.

### H3 — workspace 645 + 647 (intent-cut and constraint-table audits)

- 645 Principle [Agents should track intent cut position and hot
  topic windows] Medium
- 647 Principle [Maintain full constraint tables and audit them
  against new intent] Medium

Both 2026-05-25, Medium certainty, abstract phrasing. "Intent cut
position" and "hot topic windows" and "full constraint tables" read
like agent-coined terminology rather than psyche vocabulary. No clear
psyche-prompt provenance. Flag: psyche review — are these psyche-
spoken phrases or agent-synthesis prose?

### H4 — workspace 414 (MVP development as active workspace phase)

414 Clarification [MVP development is the active workspace phase —
all design, audit, and operator work prioritizes MVP migration
urgency. Counter-ego work folds critique with active advancement and
concrete fix execution.] Maximum

The "counter-ego work folds critique with active advancement and
concrete fix execution" reads like agent-synthesis. The first half is
plausibly psyche intent (urgent MVP focus); the second half
("counter-ego ... folds ... concrete fix execution") reads like the
agent generating discipline language. Flag: psyche review the second
half.

### H5 — workspace 451 (subagents authorized for schema-design)

451 Constraint [Subagents are authorized for the schema-design
task.] Maximum

Reads as a session-specific work-instruction captured as Constraint.
Per `intent-log.md`, work instructions are not intent: "implement X,
fix Y" — the task assignment is the witness. This authorisation,
being session-scoped, has no future-session use.

Flag: psyche review whether 451 is work-instruction or intent.

### H6 — workspace 538 / 539 + 547 / 549 cluster (workflow imperatives)

- 538 Correction [Work orders are not intent records] Maximum
- 539 Principle [subagent dispatch must always be non-blocking ...] Maximum
- 547 Principle [in a test, anything blocking the test gets unblocked inside the test itself ...] Maximum
- 549 Decision [the schema reader uses a multi-pass NOTA-first model ...] Maximum

These four span 2026-05-25 morning. 538 + 539 are real psyche
discipline statements. 547 is borderline (reads like generic
workspace methodology rather than a specific psyche statement). 549
captures a specific design model (multi-pass NOTA-first reader); the
substance is plausibly psyche, but the verbose-synthesis description
shape warrants review.

Flag: psyche review 547 + 549 for whether the descriptions match the
psyche's actual statement.

### H7 — Records 542 + 545 — work orders dressed as Decision

- 542 Decision [Psyche directs full design report on the upgrade
  mechanism with visuals ... Second-designer to research what has
  been tested re new-spirit-talks-to-old-spirit and deliver the
  design.] Maximum
- 545 Decision [Psyche wants the full upgrade mechanism documented
  end-to-end ...] Maximum

Both records are session-specific work directives that the agent
captured as Decision records. Per the work-instruction-vs-intent
test: "will an agent in a different session need to know this fact?"
Both are scoped to specific report dispatches; future sessions don't
need to know the directive existed.

Per record 538 ("Work orders are not intent records"), these are
exactly the kind of capture that 538 explicitly forbids. They may be
gap-fills from the originating session (the work-order vs intent
distinction came AFTER they were captured).

Flag: psyche review 542 + 545; likely retire.

### H8 — agent-contract 375-379 — operator work-orders

All five `agent-contract` records (375, 376, 377, 378, 379) are
authored 2026-05-22 in support of a single rename operation:
"Implement /318 R10 agent contract rename"; "Do not edit persona-
agent daemon"; "Rename only after confirming no external dependents";
"Use jj non-interactively"; "Run cargo with CARGO_BUILD_JOBS=2".

These are operator-task-execution constraints, not psyche intent
about agent-contract substance. They're work-order discipline rules
captured as Constraint records, all at Maximum certainty.

Flag: psyche review 375-379; likely retire the whole topic. The jj-
inline rule is already captured at workspace level in 237.

### H9 — workspace 384 (Avoid unrelated repository edits during U6)

384 Constraint [Avoid unrelated repository edits during U6] Maximum

"U6" is a session-specific work-claim handle. This is a session-
scoped instruction, not intent. Future sessions don't know what U6
was. Flag: psyche review — likely retire.

### H10 — workspace 347 + 349 + 350 — claim-and-jj operator instructions

- 347 Constraint [Claim primary-kbmi.2.1 scopes as second-system-assistant before editing and release when done] Maximum
- 349 Constraint [Use jj and run full checks for every changed domain-criome runtime branch] Maximum
- 350 Correction [Use system-specialist lane rather than second-system-assistant for primary-kbmi.2.1 scope claim] Maximum

All three are operator work-order constraints scoped to a specific
bead. 350 explicitly corrects 347. These should be operator-bead
descriptions, not intent records.

Flag: psyche review 347 + 349 + 350; likely retire.

### H11 — orchestrate 382 + version-control 386 — assistant-lane work orders

- 382 (orchestrate) Correction [Operator worker should use an assistant lane lock for this repo scaffold] Medium
- 386 (version-control) Constraint [Use inline jj workflow for U6 commit and push] Maximum

Same session-scoped pattern as H9 + H10. Flag: review for retire.

### H12 — Suspected gap-fills from the parallel-designer turn

Per AGENTS.md "forwarded prompts" rule, when one agent's prompt is
forwarded to a second agent, both may capture. Records 516 + 518 are
the explicit example: same intent captured by two agents in the same
turn (the reflexive-duplication failure mode that AGENTS.md 2026-05-25
calls out at record 539 cluster).

Possible additional pairs to review for the same pattern (same-
substance + close timestamps):
- 95 + 96 (workspace) — designer-downstream-work principle + clarification
- 211 + 212 (persona / reports) — corrections from same turn
- 576 + 577 (workflow / workspace) — different topics, same turn

Flag: psyche review for gap-fill-or-reflexive-duplicate distinction
per record 716/513-519 lessons.

## Records that survived audit (high-confidence real)

The substance of the workspace is mostly load-bearing real intent.
Surviving high-confidence clusters:

- **Workspace discipline core**: 5 (no-subagents-unless-told), 35-37
  (role protocols), 213 (lane-retirement context-maintenance), 222
  (3-7 chat items), 231 (meta-report directories), 232 (chat-as-
  paraphrase), 218 (long content in reports), 237 (jj inline),
  255-256 (designer authority + audit-feeds-beads), 538 (work-orders-
  are-not-intent), 539 (background subagents), 583 (commit-and-push),
  672 (next/main/previous vocab), 692 (schema/signal/sema triad),
  712 (no free functions), 716 (psyche-authored vs agent-drifted),
  717 (intent lives in its scope), 718 (don't infer), 719 (audit
  policy).
- **Naming + NOTA core**: 22-27 + 698 + 701 + 705 (bracket strings,
  shell-double-quote), 262 (no-abbreviation), 261 (Identifier rule).
- **Spirit + intent-log substrate**: 6 (use Spirit), 7 (track
  deployed version), 11 (CLI documented), 70 (universal Magnitude),
  71 (sema-upgrade), 168 (intent logging uses Spirit), 691 (intent
  capture should be dense).
- **Component-triad core**: 1 (CLIs are thin Signal clients), 10
  (schema migration), 21 (in-process versioned reads), 41 (Nix-flake
  upgrade), 70 (Magnitude), 159 (audio components), 240 (systemd
  units), 252 (FD handoff Design D), 270 (component naming
  convention), 280 (drop persona- prefix), 668 (schemas warrant per
  channel), 669 (external + internal schema categories), 670 (schema
  file homes), 692 (schema/signal/sema triad), 695 (rkyv single
  encoded representation), 696 (upgrade mechanism), 698 (bracket
  strings).
- **Recording-system arc**: 59-63 (always-on Prometheus capture,
  intent boundary markers, voice filtering), 105 (laptop → ai-node
  topology), 116 (Gemma 4 release), 126 (intent-capture is a
  function not an agent).
- **Persona engine**: 124-125 (function vs agent; cryptographic
  identity), 134 (BLS12-381), 204-209 (priority destinations,
  sema-upgrade prerequisite, persona before spirit), 215-216
  (Persona naming), 240 (systemd), 246/252 (FD handoff), 304-305
  (persona-pi repo), 329-332 (agent component, router, harness).

The workspace intent log substantially survives the audit — the
flagged records are concentrated in two zones: (a) the schema-
crystallization drift (656-715 substantially affected) and (b) work-
order-captured-as-intent leakage (a small set of session-scoped
records).

## Audit methodology

- Walked the v0.2.0 spirit database 1-719 records via
  `spirit-v0.2.0 "(Observe (Records ((Some <topic>) None
  DescriptionOnly)))"` per topic in descending record-count order.
- For high-count topics (schema, workspace, component-shape, persona,
  nota, spirit, signal, schema-language, reports, cloud), reviewed
  every record description.
- For lower-count topics, scanned for outliers (verbose-synthesis,
  narrow-topic patterns, work-order leakage).
- For the schema-crystallization arc (655-715 IDs), cross-referenced
  with provenance timestamps to identify session-bounded drift.
- Cross-checked every flagged record against records 712-719 (the
  2026-05-26 corrections).
- Did NOT delete, supersede, or capture supersession records (per
  record 719 audit-don't-delete discipline).
- Did NOT touch `intent/*.nota` legacy files.

The audit prefers under-flagging to over-flagging. Where uncertain
about agent-introduced vs psyche-authored, the audit flags rather
than dismissing; the psyche makes the call.

## Recommendations to psyche

### Highest impact — schema-defines-effects drift cluster

The cluster 660 (InteractTrait), 661 (EffectTable), 662 (FanOut), 663
(embed-everywhere mandate), 664 (heresy sweep), 665 (refinement), 710
(POC must include EffectTable closure tests) is the largest drift
identified. Records 666, 668, 713, 715, 716, 718 progressively retracted
or contradicted this cluster, but the original Maximum-certainty
records are still in the log and 663 + 664 still mandate embedding
the now-retracted principles workspace-wide.

**Recommended consolidated supersession**: psyche supersede 660-665
+ 710 with one Correction saying "the InteractTrait, EffectTable,
FanOutTargets, and schema-defines-effects direction was agent-
introduced and never psyche-authorized; the substance from records
659, 668-670 about per-channel schema scope survives; the
schema-as-data discipline from 713-716 is the canonical position."

Then 663 + 664 should be superseded with explicit notes that the
sweep-target list contained agent-hallucinated items.

### Second-impact — work-order leakage

Retire records that captured session-scoped work directives as
intent: 347, 349, 350, 375, 376, 377, 378, 379, 382, 384, 386, 451,
542, 545. Recommend: psyche pass through, mark "retire — work order
not intent" on each (or batch them as one supersession Correction).

### Third-impact — duplicate clusters

For each duplicate cluster in this report (D1 through D18), psyche
picks survivors and supersedes. The audit's suggestion in each
cluster is a starting point.

### Fourth-impact — narrow synthesis topics

The 11 narrow agent-introduced topics in H1 should consolidate into
broader topics or retire. Some substance may survive (field-name-
derivation; two-phase dispatch); the topic shape should not.

### Process going forward

Per record 718 ("Don't infer; ask the psyche"), agents should ask
when design feels under-specified rather than generating-and-
recording the missing pieces. This audit confirms the failure mode
the rule prevents: the schema-crystallization arc generated a large
cluster of plausibly-shaped synthesis that landed in the log as if
it were psyche-authorized.

Per record 717, future intent records should land in the file
(workspace, repo) that owns their scope — schema-syntax intent should
not leak into workspace-level INTENT.md.

Per record 567 (already in the log: "the spirit intent log requires
garbage collection") and record 719 (this audit's framing), the next
substantive step is psyche-driven supersession of the flagged
clusters, then a Spirit feature for marking records superseded vs
active.

## Audit artifact summary

- **Records walked**: 1-719 (the full v0.2.0 db).
- **Topics walked end-to-end**: 10 high-count (schema, workspace,
  component-shape, persona, nota, spirit, signal, schema-language,
  cloud, reports).
- **Topics scanned for outliers**: ~20 lower-count topics.
- **Duplicate clusters flagged**: 18 (D1-D18).
- **Misalignment groups flagged**: 5 (M1-M5).
- **Suspected hallucination groups flagged**: 12 (H1-H12).
- **Records on the highest-impact flag (schema-defines-effects)**:
  660, 661, 662, 663, 664, 665, 710 (7 records), plus ripple into
  710's EffectTable-closure-test mandate.
- **Work-order-as-intent records flagged**: ~14 records.

This report is the audit output. Psyche review and supersession
decisions land as new Spirit records; this report does not.
