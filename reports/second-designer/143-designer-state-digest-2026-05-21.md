# 143 — Designer-state digest (2026-05-21)

*Synthesis of the designer-lane state of play after reading the 13
load-bearing designer reports remaining in `reports/designer/` per
the /259 sweep. Written to give the next designing-protocol session
(and any operator picking up the migration beads in /130–/142) a
single entry point to what the designer has been doing.*

## 1 · Scope of this digest

**Read fully this turn (13 reports):**

- `/256-signal-spirit-post-fix-audit-2026-05-20.md`
- `/258-persona-signal-triad-audit-2026-05-21.md` (read previously)
- `/259-session-handover-2026-05-21.md`
- `/260-schema-migration-discipline.md`
- `/261-schema-version-surface-research.md`
- `/263-schema-specification-language-design.md` (absorbs the
  superseded `/262-content-addressable-schema-layout-schema.md`)
- `/264-designing-protocol-and-role-spaces.md`
- `/265-spirit-master-upgrade-test-result.md`
- `/266-persona-pi-triad-design.md`
- `/267-v2-intent-substrate-certainty-drift.md`
- `/252-engine-management-rename.md`
- `pi-api-surface-notes.md`

**Background not re-read this turn (substance absorbed via others):**

- `/214-criome-architecture-record-2026-05-17.md`
- `/234-concept-designer-role.md`
- `/238-signal-architecture-redirection-contract-local-verbs.md`
- `/246-v4-bundled-fix-deep-design-with-examples.md`
- `/248-three-layer-changes-for-operators.md`
- `/249-component-intent-gap-analysis.md` (60K; substance ladders into /252, /258)
- `/257-signal-contracts-names-and-shape-audit.md` (the audit-wave agents read this on /130–/142 prompts)

## 2 · Major threads in current designer work

### 2.1 · Schema migration discipline (new major thread; 4 reports today)

The thread the operator's spirit pin will hit first.

- `/260` surfaces the problem (a persona daemon + persistent redb
  evolve together when contract or storage schema changes; today
  there is no migration pattern). Psyche selected **Approach C —
  in-process versioned reads**: per-record schema-version tag,
  read-side migration into current shape, optional write-back.
- `/261` analyses the version-surface question Approach C left
  open (per-component vs per-record-type vs layered). Recommends
  **Option C, layered** — per-record-type machinery + per-component
  label.
- `/263` designs the schema specification language **fresh**, scoped
  to the workspace's Rust subset (named-field structs, tagged enums,
  transparent newtypes, fixed-width scalars; **no tuples ever**).
  Cap'n Proto is the closest reference point; the workspace language
  is more explicit (layout commitments stated, not inferred from
  field IDs; positional declaration; content-addressable identity
  not nominal type IDs; append-only declared, not implicit through
  ordinal monotonicity). The content-addressable framing (Blake3 of
  canonical schema text = contract version; layout-bound annotations
  carry rkyv headroom commitments) and the schema-change classes
  (zero-cost / append-only / structural) were absorbed from the
  retired `/262` predecessor (whose aski-stack-as-foundation framing
  was corrected by psyche — aski-core / askic / askicc are analog
  past experience, not the foundation to extend). Six design
  questions remain open.

### 2.2 · Per-role protocols + designer-as-bridge (/264, settled Maximum)

Two settled records reshape how psyche-to-agent dialogue works
**today**:

- Each role carries a **protocol**: designing protocol (psyche talks
  to a designer), operational protocol (psyche talks to an
  operator), poet protocol. The role-label drives interpretation;
  the agent does not infer mode.
- The designing-protocol workflow:
  `psyche → designer logs intent → designer writes report → designer
  files beads → operator implements via beads`. **The designer does
  not jump the rail to implement.** The operator stays on their
  side.

Sections 3–6 of /264 (role-spaces as per-role Git repos, per-agent
Criome identities, `shortest_id()`, LLM-call fallback chains) are
designing-mode speculative at Medium certainty. Do not act on them
as settled.

### 2.3 · Persona-pi triad (new component — /266 + pi-api-surface-notes)

A new triad joining the persona family. Settled architectural
distinctions:

- **Dual-path communication**: terminal-cell (Unix I/O, PTY bytes)
  and harness API (Pi extension surface) both live at the same
  time. Not the same as persona-terminal's control/data carve-out;
  both persona-pi paths are typed and inside the wire discipline.
- **Persona-pi is the substrate for the Codex arm of composite-
  designer**: composite role runs Claude (Claude Code) and Codex
  (persona-pi) in parallel; orchestrator selects-or-merges (policy
  itself speculative).
- **Pi extension namespace adapts from flat snake_case to typed-
  noun method trees**: `query_negative_database_from_behind`
  becomes `NegativeDatabase.from_behind(...)`. Per
  `skills/abstractions.md`'s verb-belongs-to-noun rule.

The pi-api-surface-notes research grounds the design: Pi is Mario
Zechner's `pi-mono` (`@mariozechner/pi-coding-agent`), four built-in
tools (`read`, `write`, `edit`, `bash`), flat `pi.*` ExtensionAPI,
closure-state TypeScript extensions. The "query_negative_database_from_behind"
verbal reference was STT mangling of Pi's canonical `db_query`
example. Six points of divergence between Pi and workspace
discipline are flagged for resolution.

### 2.4 · Substrate cutover progress (/259, /265, /267-v2)

- `/259` confirms spirit triad is post-migration in excellent shape;
  engine-manager triad is next; bead `primary-77hh` landed
  (signal-frame `653773b`); bead `primary-k3bu` landed in
  signal-frame (`b375e20`); `primary-u0lh` pending. **/259 also
  notes /258 was a designer "misfire"** — psyche meant the
  persona-spirit triad re-audit, designer read it as engine-manager.
  Substance still valuable (engine-manager IS a real next slice).
- `/265` validates additive variant insertion at end (zero-cost)
  vs mid-position (wire-break). The master-vs-deployed test confirms
  rkyv-headroom holds for end-appended variants. Recommends a Nix
  flake check `checks.<system>.spirit-upgrade-compat` cartesian-
  product over deployed/master daemon × deployed/master CLI.
- `/267-v2` finds 7 records in `intent/*.nota` using `Certainty High`
  that the deployed Spirit rejects. Designer proposes the working
  mapping `High → Maximum`.

### 2.5 · Engine-management rename plan (/252)

Multi-repo rename: `Supervision*` types → `EngineManagement*` types
across `signal-persona` + 9 consumer repos + `persona/src/supervisor.rs`
→ `engine_manager.rs`. Adds the `EngineManagement` prefix exception
to the prefix-drop rule (justified: disambiguates from Kameo
`*Supervisor` actor-tree convention). **NOT yet executed.** Order
of operations: signal-persona first, persona second, consumers in
parallel third, docs last.

## 3 · Connections to the audit wave (`/130–/142`)

The audit wave I dispatched on this turn intersects designer's
recent work in five ways:

1. **`/258` was the template I followed in agent prompts.** Despite
   being a designer "misfire" (per /259), its audit shape is the
   right shape; the agents used it correctly.

2. **The `/264` designer-as-bridge workflow is exactly the workflow
   the audit wave executes.** Psyche prompt → intent capture →
   reports filed (designer-assistant lane) → beads `primary-e1pm`
   through `primary-k2mh` filed → operator picks up. This report
   itself is the same pattern.

3. **Schema migration discipline (/260–/263) is a dimension the
   migration beads do not yet address.** Per-component migrations
   onto signal-frame should eventually also adopt the schema
   specification language. The beads currently say "migrate to
   the current foundation libraries"; they do not say "and adopt
   the new schema language as it lands." This is fine for now
   (the schema language is still being designed), but the beads
   should be updated when /263's design settles.

4. **Designer's open psyche calls (Q1, Q4, Q5 from /259) overlap
   with my aggregated open questions.** See §4 below.

5. **Persona-pi is NEW** — not in `protocols/active-repositories.md`
   and not in the audit wave. The triad design (/266) is current
   work; no migration needed yet. Future audit wave that includes
   persona-pi should reference /266 + pi-api-surface-notes.

## 4 · Aggregated open psyche calls across the designer surface

Items needing psyche attention, drawn from the designer reports.

### From /259 §"Open psyche calls" (the designer's standing list)

- **Q1**: Single-field timestamps in runtime/protocol contexts
  (vs the two-field rule for intent records). `TimestampNanos(u64)`
  in signal-persona for `component_started_at` / `drain_completed_at`;
  `TimestampNanoseconds(u64)` in owner-signal-persona-router for
  `ChannelDuration::TimeBound`. Designer lean: single-field OK for
  protocol; drop ns → seconds.
- **Q4**: `ChannelMessageKind` 12-variant closed enum (in
  `owner-signal-persona-router`). Agent-cultivated per /249 gap
  #22. Closed-enum vs data-token (string)?
- **Q5**: Mind channel-choreography verb set —
  `Grant` / `Extend` / `Revoke` / `List` / `Deny` were "TBD" in
  the 2026-05-19T20:30:00Z Decision. Lock names before mind
  migrates.

### From /267-v2 §"Open psyche questions"

- **Certainty mapping**: confirm or override `High → Maximum`
  for the 7 drifted intent records (designer's proposed default).
  Alternatives: `High → Medium`; per-record decision.
- **Skill discipline**: should `skills/intent-log.md` add a hard
  rule forbidding non-canonical certainty tokens?
- **Pre-migration enum audit**: any other closed-world enums to
  audit before broader file → spirit migration begins?

### From /263 §"Open design questions worth psyche input"

- Where do channel-leg layout annotations live (inline, at
  channel level, or implicit append-only)? Designer lean:
  implicit append-only.
- Are struct-level layout annotations load-bearing, or write-only?
  Designer lean: drop until a concrete case demands them.
- One schema file per contract, or many that combine? Open.
- Same language for owner-signal contracts, or different? Designer
  lean: same.
- Which scalar types are built-ins? `Date` / `Time` candidates
  for built-in promotion.
- Inline payloads for one-off variants — keep the no-anonymous-
  types rule absolute?

### From /266 §"Open psyche questions"

- Is the dual-path shape (terminal-cell + harness API) unique to
  persona-pi or a general pattern for future structured-API
  harnesses? Designer lean: probably general.
- Per-agent Criome identity composition with composite-designer
  arms (waits on /264 §4 Criome direction).
- Composite-designer arms read the same designer skills?

### From the audit wave (already in primary's last chat reply but listed for completeness)

- `EffectEmitted` payload type: variant-name rule only (a) vs
  payload-type rule (b)? 8+ pending observable blocks depend.
- Lifecycle verbs (Start/Drain/Reload/Retire) on owner contracts
  for non-spirit components?
- Observable block on owner contracts (per /131, /133, /136, /258
  disagree on lean)?
- persona-orchestrate destination scope (lock-helper stays or
  replaces)?
- persona-orchestrate owner contract policy-programmability shape?
- Engine vs EngineManagement crate-split?
- persona-mind plane split (graph + memory)?
- persona-terminal per-plane split?
- persona-message channel split (ingress vs delivery)?
- persona-harness TerminalEndpoint binding (owner or working)?
- repository-ledger Receive/Observe lift to Record(Capture)?
- lojix observable block (debug-the-debugger universal)?
- criome observable block (same question)?

## 5 · What I'd flag from this synthesis

Five items where designer-state intersection with my migration
wave most needs your weight:

1. **Schema specification language landing intersects every
   per-component migration.** /263's language design needs to
   settle (the 6 open design questions) before per-component
   migrations adopt schema-version stamping. Without the language
   in hand, migration beads `primary-e1pm` through `primary-k2mh`
   land at "current foundation libraries"; they do NOT yet land
   at "current schema specification." The two-step migration
   risks ossifying the first shape if operators land it before
   /263's questions settle.

2. **/258 misfire — does the engine-manager re-audit (`primary-k2mh`)
   stay, or should the audit also produce a real persona-spirit
   re-audit?** Per /259, /258 was meant to be a persona-spirit
   re-audit. My `/142` re-audit (engine-manager) caught real gaps
   /258 missed. A separate persona-spirit re-audit might still be
   wanted in the designer-assistant lane.

3. **Designer's standing Q5 (mind channel-choreography verb set)
   blocks `primary-e1pm` mind migration in a real way.** The mind
   migration bead names "redesign signal tree first" but the
   verb set is the load-bearing part of that redesign. Operator
   needs the names before contract work begins.

4. **Persona-pi is a new triad that should have a bead too.** The
   migration wave covered 13 components; persona-pi makes 14.
   /266 is the designer sketch; the bead would carry the
   pi-api-surface-notes + /266 + the dual-path constraint to
   the operator who builds the triad. Designer lean: file the
   bead once /266 §7 questions settle.

5. **The certainty-vocabulary drift (/267-v2) is a substrate-migration
   concern that touches every future file → spirit hand-relog
   pass.** The High → Maximum default mapping needs confirmation
   before any operator starts the broader relog work.

## 6 · See also

- All 13 designer reports read this turn (listed §1).
- `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md` — prior designer-assistant work on mind→orchestrate payload + signal_cli! Option A.
- `reports/second-designer/130–142` — the migration audit wave this digest contextualises.
- Beads `primary-e1pm` through `primary-k2mh` — the 13 per-component migration beads filed off the audit wave (all P1).
- Standing beads `primary-77hh` (landed), `primary-k3bu` (landed in signal-frame), `primary-u0lh` (pending P2).

This digest retires when (a) the next designer-state digest
supersedes it, OR (b) the migration wave's beads are claimed and
operator picks up. Until then, this is the catch-up artifact.
