# 268 - Persona-pi operator-input brief

*This is an operator-input brief, not a design report. The
persona-pi triad is not yet ready for direct implementation: the
design conversation in `reports/designer/266-persona-pi-triad-design.md`
(triad sketch with deliberate dual-path and namespace adaptation)
plus the API-surface notes in
`reports/designer/pi-api-surface-notes.md` (the actual Pi extension
shape Mario Zechner ships) settle the direction, but several design
forks remain open. The operator's job, on the basis of this brief, is
to write an exploratory implementation proposal that takes a concrete
position on each fork. The prime designer will then review the
operator's proposal in a later turn. Reports referenced here are the
canonical source for the substance — this brief points at them
and frames the forks the operator must close, not the substance the
operator must re-derive.*

> **2026-05-22 correction:** Package scope is `@earendil-works/`
> (GitHub canonical: `earendil-works/pi`), **not** `@mariozechner/`
> as referenced below. Mario Zechner is still the author; the
> package moved to the `earendil-works` org with the monorepo
> split (`pi-coding-agent`, `pi-agent-core`, `pi-ai`, `pi-tui`).
> Persona-pi work should target the new scope. See
> `reports/designer/281-headless-pi-research.md` for the full
> updated picture.
>
> **2026-05-22 scope rollback (supersedes prior banner):** The
> earlier 2026-05-22 banner that subsumed DeepSeek into persona-pi
> (spirit record 151) was a misframe. Per psyche Correction
> 2026-05-22 (spirit record 152, supersedes 151): DeepSeek-as-library
> belongs in a NEW workspace component `persona-llm-client` (a
> lightweight Rust-shaped library embeddable in daemons), not in
> persona-pi. persona-pi remains as designed in /266 — the
> Pi-runtime-harness adaptation, full agent loop, dual-path. The
> operator's persona-pi proposal does NOT need to cover DeepSeek.
> DeepSeek is `persona-llm-client`'s concern, designed separately.

## 1. The prior work, in summary

### `reports/designer/266-persona-pi-triad-design.md` - the triad sketch

Designer's load-bearing sketch for persona-pi. Names it as a new
triad in the persona family alongside spirit / mind / orchestrate /
router / harness / terminal / introspect: standard three-leg shape
(`persona-pi` runtime + `signal-persona-pi` working contract +
`owner-signal-persona-pi` policy contract), CLI named `pi`, daemon
`persona-pi-daemon`. The sketch's two settled architectural pieces
are **dual-path communication** (terminal-cell I/O **and** harness
API in parallel, both first-class, both typed) and **namespace
adaptation** (Pi's flat snake_case verbs adapt into typed-noun
records — the example given is `query_negative_database_from_behind`
collapsing to `NegativeDatabase.from_behind`). Persona-pi is the
substrate for the **Codex arm of the composite-designer role**:
Claude runs in Claude Code; Codex runs in persona-pi; the
orchestrator selects-or-merges. Persona-pi's default config is
GPT-latest with Maximum Thinking, declared in `bootstrap-policy.nota`
per `skills/component-triad.md` invariant 5. Speculative pieces are
flagged inline in /266 §6 (Pi-API specifics, select/merge policy,
composite-roles-beyond-designer, authority graph placement,
persona-terminal interaction, observability shape).

### `reports/designer/pi-api-surface-notes.md` - the actual Pi surface

Research feed grounding /266 in the real Pi extension surface.
Identifies Pi as Mario Zechner's `@mariozechner/pi-coding-agent`
(npm package, domain `pi.dev`), packaged as `pi-mono`. Names the
four canonical built-in tools (`read`, `write`, `edit`, `bash`),
the flat `pi.*` ExtensionAPI (`pi.registerTool`,
`pi.registerCommand`, `pi.registerProvider`, `pi.on`, `pi.events`,
`pi.exec`, `pi.setModel`, `pi.setSessionName`, `pi.appendEntry`, …),
the full event surface (`session_start`, `tool_call`, `tool_result`,
`before_provider_request`, `model_select`, etc.), the
shared-state canonical example (`db_connect`/`db_query`/`db_close`
with closure-held connection and `session_shutdown` hook), and
**six load-bearing divergences from workspace discipline**: flat
tool namespace vs typed-noun records; flat `pi.*` method bag vs
typed record API; TypeScript closure state vs typed signal types;
free-form TypeScript args vs single-NOTA-argument rule; npm
distribution vs Nix-flake; user-editable system prompt vs
designer-owned protocol. Surfaces five open psyche-clarification
questions whose answers shape the implementation proposal.

### `reports/second-system-assistant/3-mario-zechner-ai-agent-points.md`

Prior workspace research on Mario's broader thesis. Establishes Pi's
*why*: Mario felt Claude Code became unstable, opaque, and prone to
silent prompt / default changes that broke long-running workflows.
Pi exists to give the user full control over the harness — minimal
core, sub-1000-token system prompt, no built-in plan mode / MCP /
subagents / background processes, everything else in extensions.
Mario's central technical objection is **context control**.
Persona-pi inherits that harness-control discipline, then layers
the workspace's typed-contract / triad / NOTA-only discipline on top.

### `intent/persona.nota` records 43-47 - the persona-pi psyche statements

These five records are the load-bearing psyche material /266 cites:

- **43 (Decision Maximum)** persona-pi is a new triad component in
  the persona family; standard daemon + working signal + policy
  signal shape; the load-bearing architectural distinction is
  **dual-path communication** (terminal-cell + harness API
  in parallel, both live at once).
- **44 (Principle Maximum)** role determines model: designer ->
  Claude; advisor -> Codex; persona-pi default -> GPT-latest with
  Maximum Thinking. Composite roles compose the parts.
- **45 (Decision Medium)** the first concrete composite role is the
  composite designer: Claude AND Codex run in parallel against the
  same prompt; the orchestrator selects-or-merges.
- **46 (Principle Maximum)** namespace adaptation: Pi's flat
  snake_case functions decompose into typed noun-method records;
  persona-pi's extension namespace does NOT mirror Pi's native one.
- **47 (Decision Medium)** persona-pi's bootstrap default is
  GPT-latest with Maximum Thinking; pre-configured in
  `bootstrap-policy.nota`, mutable thereafter only through
  owner-signal `Mutate` per the triad invariants.

The verbatim quotes and context paragraphs land in /266 itself and
in `intent/persona.nota` as the records get logged. The operator
treats /266's reading of these records as canonical for this brief.

## 2. The proposal-shaped questions the operator must answer

The operator's proposal needs to take a concrete position on each
of the following forks. None has a single right answer; each is
where the design conversation has been in flight.

### 2.1 Pi extension shape - which ExtensionAPI hooks does persona-pi register?

`pi-api-surface-notes.md` §"ExtensionAPI methods" enumerates the
full `pi.*` surface. The persona-pi extension does not need to
register every hook. The proposal must name, concretely, which
hooks persona-pi *does* register and why:

- **Tools** - which custom tools does persona-pi add beyond the
  four built-ins? Which of the built-ins does it leave active, and
  which (if any) does it replace with persona-shaped equivalents
  routed through Signal? (The `bash` built-in versus a router-gated
  exec is one obvious fork.)
- **Commands / shortcuts / flags** - does persona-pi register any
  slash commands, keyboard shortcuts, or invocation flags? The
  workspace's flag-free single-argument rule constrains how
  `pi.registerFlag` can be used at all.
- **Providers** - does persona-pi register its own provider entry
  for GPT-latest with Maximum Thinking, or rely on Pi's built-in
  provider catalogue? (Record 47 says the default is set; the
  *mechanism* is the question.)
- **Message renderers** - what custom `appendEntry` types does
  persona-pi need? At minimum, persona-pi probably emits typed
  records when reporting harness-API operations back to the
  terminal cell.
- **Lifecycle hooks** - which `pi.on(...)` listeners are
  load-bearing? `session_start`, `session_shutdown`, and the
  `tool_call`/`tool_result` pair almost certainly are; the rest
  is a scope question.

### 2.2 Signal contract shape - what does `signal-persona-pi` expose?

`signal-persona-pi` is the working (ordinary-peer) contract. The
proposal must declare the operation roots, replies, and events:

- **Operation roots** - /266 §2.5 settles that the contract carries
  operation roots that distinguish the dual-path at the type level
  (terminal-cell vs harness-API operations should NOT collapse into
  one bag). What are the concrete operation-root variants? Sketch
  at least a top-level enum and a representative sub-enum per
  branch (e.g. a `HarnessApiOperation` with one or two noun-typed
  variants per /266 §3.4).
- **Replies** - one reply variant per operation root, per the
  workspace's contract macro shape. Name the load-bearing payload
  records.
- **Events** - per the universal Tap/Untap mandate
  (`intent/persona.nota` record on persona-introspect, 2026-05-21
  "debug the debugger"), `signal-persona-pi` declares an
  `observable` block emitting `OperationReceived` and
  `EffectEmitted`. Name the typed event payloads.

### 2.3 Owner contract shape - what does `owner-signal-persona-pi` expose?

The owner contract carries the policy / authority surface. Pi's
configurable surfaces include the active model, thinking level,
provider set, session name, label, active tools, system prompt,
and skill bundle. Each of these is a candidate for
owner-signal mutation by an authoritative caller (orchestrate or
mind, depending on the authority placement settled in §2.7).

The proposal must:

- Name the policy-state records that live in persona-pi's
  sema-engine database per triad invariant 5 (e.g. model selection,
  thinking level, active-tools set, system-prompt bundle).
- Sketch the owner-signal `Mutate` variants that change them.
- Distinguish policy state (bootstrapped from
  `bootstrap-policy.nota`, mutable only via owner Mutate) from
  working state (produced by operation; see §2.6).

### 2.4 Dual-path surface area - terminal-cell vs harness-API

/266 §2 settles that both paths are first-class but does not yet
draw the boundary in code. The proposal must name what flows on
each side:

- **Terminal-cell path** - the Unix-side I/O surface. What does
  persona-pi forward to the terminal cell? Does persona-pi use
  persona-terminal internally (a daemon-to-daemon Signal client
  relationship per `skills/component-triad.md` §"Named carve-outs"
  #3), or implement its own terminal-cell surface in-tree? /266 §6.5
  flags this as undesigned.
- **Harness-API path** - the typed programmatic surface. Which
  Pi extension hooks (from §2.1) project to harness-API operations
  on the wire? What is the smallest noun catalogue that lets the
  composite designer's Codex arm exercise a non-trivial
  multi-turn task end-to-end?

### 2.5 Composite-designer integration - how do Claude and Codex run in parallel?

Per `intent/persona.nota` record 45, the composite designer fans
out the psyche prompt to Claude-in-Claude-Code AND Codex-in-persona-pi.
The orchestrator step selects-or-merges. /266 §6.2 marks select/merge
as speculative. The operator's proposal sketches the integration:

- Who is the orchestrator process? (`persona-orchestrate` is the
  natural candidate but /266 §6.4 flags this as not yet stated.)
- How does the same prompt land in both arms? Is the prompt a
  single NOTA record passed twice, or does each arm receive a
  different framing?
- Where does Codex's harness-API output flow back to? Does
  persona-pi's Signal contract carry composite-designer-aware
  reply shapes, or is composite-designer responsible for assembling
  arm outputs from generic persona-pi replies?
- What's the minimum machinery to demonstrate the composite
  designer end-to-end? (See §2.7 first-slice.)

### 2.6 Storage - does persona-pi own a sema database?

Per `skills/component-triad.md` invariant 5, every triad daemon's
durable state lives in a sema-engine database (one `<component>.redb`
opened through `sema-engine`), split into policy tables (changed via
owner Mutate) and working tables (produced by operation).

The proposal must declare:

- Whether persona-pi has working state at all, or is essentially a
  stateless harness wrapper that holds only policy state. Candidates
  for working state: in-flight session metadata, conversation
  transcripts, tool-call history, harness-API operation logs.
- If working state exists, name the table categories and
  representative records.
- The bootstrap-policy.nota's initial declaration (model =
  GPT-latest, thinking-level = Maximum, plus whatever else the
  initial policy needs).

### 2.7 First-slice scope - minimum-viable persona-pi for the composite designer

`intent/persona.nota` is rich with first-slice discipline: ship raw,
ship usable, defer integration ceremony, let the agent use the
component in raw form first. Apply that here.

The proposal names the smallest persona-pi that lets the
composite-designer role function end-to-end:

- Which subset of the dual-path is in the first slice? Plausibly:
  full terminal-cell pass-through; a deliberately small
  harness-API operation set (one or two noun-typed verbs, just
  enough to demonstrate the namespace-adaptation discipline).
- Which orchestrator integration is in the first slice? Plausibly:
  a minimal composite-designer driver that fans out, collects two
  outputs, and surfaces both to the psyche (the select/merge
  policy stays speculative per /266 §6.2; surfacing both is the
  honest first behaviour).
- Which Pi extension hooks are in the first slice? Plausibly:
  registerTool for one custom tool, the tool_call/tool_result
  event pair, session_start/session_shutdown, and not much else.

The proposal is allowed to defer everything else into a sequel.

## 3. Workspace constraints the operator must observe

These are not negotiable. The proposal must visibly honour each.

- **Component triad** (`skills/component-triad.md`) - the five
  invariants and the single-argument rule. Persona-pi is a normal
  triad and obeys them all: thin CLI with one Signal peer (the
  daemon), daemon's external surface is exclusively
  `signal-frame` frames, three verb layers (Contract Operation /
  Component Command / Sema Operation), working + owner authority
  tiers, policy + working state in one sema-engine DB.
- **NOTA-only argument language** - every binary (the `pi` CLI
  and the `persona-pi-daemon`) takes exactly one argument: a NOTA
  string, a path to a NOTA file, or a path to a signal-encoded
  file. No flags. If new configuration is needed, the contract's
  NOTA schema gets a new field.
- **Typed records over flags** (`skills/typed-records-over-flags.md`)
  - any yes/no question whose "yes" carries data is a typed record,
  not a boolean. This applies to persona-pi's policy records,
  working records, and contract payloads.
- **Methods on nouns** (`skills/abstractions.md`) - every reusable
  verb belongs to a noun. The namespace-adaptation rule from /266 §3
  is this discipline applied to Pi's flat extension surface; the
  same rule governs every other type the proposal introduces.
- **No tuples in workspace Rust subset** (`intent/nota.nota`
  2026-05-20 "tuples are poorly specified structs") - the NOTA
  layer has no tuples and the Rust subset that maps to NOTA records
  must use named structs throughout. The proposal's contract
  payload sketches use named-field shapes, never positional
  tuples.
- **Universal Magnitude type** - the workspace is consolidating
  scalar-with-unit values into a shared `Magnitude` type rather
  than per-component magnitude newtypes. Any persona-pi field
  carrying a measurable value (token counts, thinking levels
  expressed numerically, durations, sizes) uses the shared type.
  The operator confirms the current location of `Magnitude` by
  reading the most recent `intent/component-shape.nota` record
  about it and the shared-data-type-library record before
  drafting the proposal.
- **Branches / leaves vocabulary** - the workspace's settled
  vocabulary for typed-record trees: a record's positional fields
  are its branches and leaves (leaves are terminal scalars,
  branches are nested records). The proposal uses this vocabulary
  when describing the operation-root and reply-tree shapes. (Look
  for the most recent record in `intent/nota.nota` or
  `intent/workspace.nota`; the vocabulary settled during the
  recent NOTA grammar work.)

## 4. What this brief is not

- Not an implementation specification. The forks in §2 are open;
  the operator closes them in the proposal.
- Not a list of beads to file. Beads come after the proposal lands
  and the prime designer reviews it.
- Not a finished architecture. /266 is the architecture sketch;
  this brief points at it.
- Not a re-derivation of /266 or `pi-api-surface-notes.md`. The
  substance lives in those reports; this brief frames the operator's
  task on top of them.

## 5. Deliverable

The operator writes an implementation proposal in their own lane.
The proposal closes each fork in §2 with a concrete position,
visibly honours each constraint in §3, names the first slice in
§2.7 explicitly, and calls out any new psyche-clarification
questions surfaced while closing the forks. When it lands, the
prime designer reviews it in a sequel report and lands the agreed
design back into /266 (or its successor) as the canonical
architecture.

## See also

- `reports/designer/266-persona-pi-triad-design.md` - the triad
  architecture sketch.
- `reports/designer/pi-api-surface-notes.md` - the real Pi
  ExtensionAPI surface and the six divergences from workspace
  discipline.
- `reports/second-system-assistant/3-mario-zechner-ai-agent-points.md`
  - prior workspace research on Mario's broader thesis.
- `intent/persona.nota` records 43-47 - the psyche statements
  this brief and /266 stand on.
- `skills/component-triad.md` - the universal triad shape.
- `skills/typed-records-over-flags.md` - yes-with-data is a record.
- `skills/abstractions.md` - verb belongs to noun; the forcing
  function behind namespace adaptation.
- `intent/component-shape.nota` - settled component-shape
  vocabulary, including the universal Magnitude type.
- `intent/nota.nota` - tuples forbidden; branches / leaves
  vocabulary.

This brief retires when the operator's implementation proposal
lands and the prime designer's review report supersedes it.
