# Bearings — lane-startup standard

*Method note: this brief was produced by a 4-reader bearings fan-out (lane
model, task-graph vocabulary, existing Spirit intent, alignment/dispatch
rules), synthesised from the source files and the live Spirit store.*

The lane intent: define the standard for how a named lane *opens* — a
mandatory bearings subagent flow plus mandatory psyche alignment questions —
and the task-graph vocabulary that flow produces.

## Grounded facts (what is true today)

### The lane model

- A **discipline** is permanent identity (skills, authority class,
  persona-mind memory, signing key); a **lane** is one throwaway work
  session named for that session's intent (`newLanesDesign`,
  `schemaWorkAudit`). The lane carries its discipline as metadata.
  (`skills/session-lanes.md:3-25`, `orchestrate/AGENTS.md:17-47`.)
- In the registry a lane's role is a NOTA vector whose **last token is the
  base discipline**, preceding tokens the specialization:
  `[NewLanesDesign Designer]`. The daemon renders it to a hyphen-joined
  lowercase filesystem identifier (`new-lanes-design-designer`).
  (`skills/session-lanes.md:44-49`.)
- An agent learns its lane from the harness/psyche session identity — the
  intent name owning `orchestrate/<lane>.lock` and `reports/<lane>/`. Do
  not infer it from discipline or borrow a neighbour's name.
  (`skills/session-lanes.md:35-42`.)
- Session lifecycle is three phases: **smart zone** (early ~100k-token
  high-fidelity window for the main agent's deepest thinking and intent
  alignment) → **fleet** (launch fresh-context sub-agents primed with
  settled conclusions, each writing one numbered report) → **drain**
  (every idea routes to intent / work / abandon). (`skills/session-lanes.md:102-120`;
  Spirit `69fa`, the 100k smart-zone principle.)
- Lane retirement: delete `reports/<lane>/`, append one entry to
  `protocols/retired-lanes.md` (lane name, discipline, git revision range,
  transcript pointer, drain date, one-line decision), retire in the daemon.
  (`skills/session-lanes.md:123-145`, `orchestrate/AGENTS.md:441-457`.)

### Task-graph vocabulary (already defined in `skills/intent-alignment.md`)

The alignment interview exists to discover the **task dependency graph**.
Its node taxonomy (`skills/intent-alignment.md:21-43`):

- **Goal node** — the user-visible state that counts as done.
- **Input nodes** — repos, reports, branches, credentials, services,
  profile state the work depends on.
- **Decision nodes** — choices only the psyche can answer.
- **Work nodes** — edits, builds, migrations, activations, reports.
- **Verification nodes** — tests, commands, visible UI behavior, deployment
  checks that prove a work node.
- **Parallel nodes** — independent audits or implementation slices
  delegable without overlapping writes.

A linear checklist is a *projection* of this graph, not the source of
truth. Implementable work is linked into a bead dependency graph
(`bd dep <blocker> --blocks <blocked>`). Spirit `iq7m` (Correction) makes
the dependency graph the documented core of the skill.

### Existing Spirit intent (load-bearing for this lane)

- `2o3g` (Constraint, certainty **Maximum**): "Agents dispatch subagents
  only when the psyche explicitly authorizes it (a per-keystroke AGENTS.md
  override for all workspace agents). When authorized, treat subagents as
  asynchronous sidecar work… Block on a subagent only when the psyche asks
  or is waiting on nothing else."
- `xrxy` (Decision, High): the prime designer chair runs parallel subagent
  workflows **by default** — a designer-specific exception to the
  no-subagents default; does not extend to second/assistant designer lanes
  unless the psyche says so.
- `xlfo` (Decision, High): a dispatched subagent **inherits the
  dispatcher's lane, lock, and report-numbering slot** — writes into the
  dispatcher's report subdir, never its own lane; parallel subagents get
  report numbers assigned before launch.
- `69fa` (Principle): the first ~100k-token window is reserved for the main
  agent's deepest thinking and intent alignment; then launch a fleet of
  fresh-context sub-agents primed with settled conclusions.
- `ky10` (Decision): the skill is named `intent-alignment` and is the
  **default for interactive agents** — align before planning/building;
  narrowly-specialized ship-trained agents are exempt.
- `l6kw` (Correction, High) & `qjrf` (Principle): ask the psyche when a
  load-bearing variable (authority, priority, scope, safety, privacy,
  certainty, importance, rollout, decision-ownership) would otherwise be
  guessed; don't synthesise and self-authorize.
- `0xqp` (Principle): running a Spirit `Observe` is standard routine, done
  proactively at the start of substantive work — not only when the gate
  flags ambiguity.
- `7hrd` (Correction, VeryHigh): a working order (create-report,
  dispatch-subagent, audit-X) is **task state, not intent** — capture only
  the durable intent inside a task prompt.

## Contradictions (current contract vs. the psyche's new direction)

### 1. The no-subagents default vs. a mandatory bearings fan-out

The new direction *mandates* a bearings subagent flow as part of how
**every** lane opens. The current contract forbids exactly that by default:

- AGENTS.md hard override: "Don't dispatch subagents unless the psyche asks
  — except the designer protocol… Default for operator, system-operator,
  system-maintainer, poet, editor, assistant, counselor and their lanes:
  do the work yourself."
- Spirit `2o3g` (certainty **Maximum**): subagents only on explicit psyche
  authorization.
- Only `xrxy` carves an exception, and only for the **prime designer**.

A standard that mandates a bearings fan-out at every lane open would
override `2o3g`/the hard override for **all** disciplines — not just
designer. That is a genuine policy change the psyche must authorize, and
(if affirmed) it should land as a Spirit edit to `2o3g` (Clarify/Supersede),
not a fresh sibling record. Note `2o3g` already allows non-blocking sidecars
"where they materially reduce audit, checklist, or verification risk" — a
bearings fan-out plausibly fits that clause, but extending it to a *mandatory
every-lane* gate for every discipline is a stronger claim than the record
makes.

### 2. "One focused question per turn" vs. "ask a few questions"

The new direction frames mandatory psyche alignment as "ask a few
questions". The current contract is explicit the other way:

- AGENTS.md: "one focused question per turn in plain prose… never the
  structured questionnaire UI."
- `skills/intent-alignment.md:46-50`: "Ask exactly one focused question per
  turn… never a batch of questions." The back-and-forth rhythm is named as
  the method itself.

"A few questions" reads as a batch, which the contract forbids. Either the
standard means "a few questions, one per turn, sequentially" (compatible —
just clarify wording) or it means a literal batch up front (a real reversal
needing psyche authorization and a Spirit edit).

### 3. Register/retire CLI: which socket? (internal doc conflict, not psyche)

`skills/session-lanes.md` routes lane register/retire through
**`meta-orchestrate`** (the owner socket) and renders the lane id as the
hyphenated lowercase form (`new-lanes-design-designer`).
`orchestrate/AGENTS.md` uses plain **`orchestrate`** and shows the lane id
echoed back as the camelCase input (`newLanesDesign`). These two source
files disagree on both the binary and the id form. The standard must pick
one and reconcile the docs; flag to the orchestrator before encoding the
register step into the lane-open ritual.

## Psyche questions (deduped, prioritized — feed the alignment interview)

1. **Does the mandatory bearings fan-out apply to every discipline, or only
   designer (and maybe operator)?** This is the load-bearing fork: it either
   overrides the Maximum-certainty `2o3g` constraint workspace-wide or stays
   a designer-protocol extension. Recommendation: scope it to designer +
   any lane the psyche explicitly opens "with bearings," and capture the
   change as a Clarify/Supersede on `2o3g`, not a new record.

2. **Is a bearings fan-out mandatory on *every* lane open, or only when the
   request isn't already crisp enough to execute?** The existing alignment
   default already exempts clear directives and ship-trained specialists
   (`ky10`). Recommendation: gate the fan-out on the same
   "not-crisp-enough" trigger rather than firing it unconditionally, so a
   one-line "do X" order doesn't spawn four readers.

3. **"A few questions" — sequential one-per-turn, or a literal up-front
   batch?** Recommendation: keep one-per-turn (the contract's named method);
   "a few" = a small ordered sequence, not a questionnaire. If the psyche
   really wants a batch, that reverses `intent-alignment.md` and needs an
   explicit edit.

4. **Where does the bearings-flow standard live — a new `skills/` file, an
   edit to `skills/session-lanes.md`, or both?** Recommendation: extend
   `session-lanes.md` with a "lane open" section and cross-link
   `intent-alignment.md`, rather than a third overlapping skill.

5. **Register/retire socket: confirm `orchestrate` vs. `meta-orchestrate`
   and the lane-id form** so the standard encodes the correct ritual.
   (Internal-doc conflict above; the psyche or an operator who knows the
   deployed daemon should settle it.)

## Exact command shapes (verbatim from the readers)

### Orchestrate — register / observe / retire

Per `orchestrate/AGENTS.md:56-69` (working `orchestrate` CLI):

```sh
orchestrate "(Register ([NewLanesDesign Designer] Structural))"
# -> (LaneRegistered (newLanesDesign [NewLanesDesign Designer] Structural))

orchestrate "(Observe Lanes)"
# -> (LanesObserved [ ...(LaneRegistration LaneIdentifier Role LaneAuthority)... ])

orchestrate "(Retire (Lane newLanesDesign))"
# -> (LaneRetired newLanesDesign)
```

Per `skills/session-lanes.md:63-79,139-141` (owner socket variant — note the
conflict flagged above):

```sh
meta-orchestrate "(Register ([NewLanesDesign Designer] Structural))"
# -> (LaneRegistered (new-lanes-design-designer [NewLanesDesign Designer] Structural))

orchestrate "(Observe Lanes)"
# -> (LanesObserved [(new-lanes-design-designer [NewLanesDesign Designer] Structural)])

meta-orchestrate "(Retire (Lane new-lanes-design-designer))"
```

`Role` is a vector of identifier tokens, last token the discipline;
`LaneAuthority` is one of `Structural` or `Support`.

### Spirit — Observe / Record / edit

Observe (proactive routine; `skills/spirit-cli.md:256-333`):

```sh
spirit "(PublicTextSearch [routing protocol])"
spirit "(Observe ((Full [(Information Documentation)]) Any Any Any (Some Constraint) (Exact Zero) (AtLeastCertainty Minimum) Any))"
spirit "(Lookup abcd)"
```

Record (seven-field `Entry` + two-field `Justification`;
`skills/spirit-cli.md:100-106`):

```sh
spirit "(Record (([<Domain> ...] <Kind> [description] <Certainty> <Importance> <Privacy> [<referent> ...]) ([([verbatim quote] (Some [antecedent question or context])) ...] [reasoning])))"
# Kind       ∈ { Decision Principle Correction Clarification Constraint }
# Certainty  ∈ { Zero Minimum VeryLow Low Medium High VeryHigh Maximum }
# Importance uses the same Magnitude ladder; Minimum is the ordinary default.
# Privacy    uses the same Magnitude ladder; Zero is open/public.
```

Edit an existing record (`skills/spirit-cli.md:168-205`) — use these when the
psyche is clarifying/correcting/superseding, **not** a new `Record`:

```sh
spirit "(Clarify (abcd [corrected description] ([([verbatim psyche clarification] (Some [what was being clarified]))] [reasoning for why this is an edit of abcd])))"
spirit "(Supersede ([abcd] [([<Domain> ...] <Kind> [replacement description] <Certainty> <Importance> <Privacy> [<referent> ...])] ([([verbatim psyche override] (Some [prior record being replaced]))] [reasoning for replacement])))"
spirit "(Retire (abcd ([([verbatim psyche retirement] None)] [reasoning for retirement])))"
spirit "(ChangeRecord (abcd ([<Domain> ...] <Kind> [replacement description] <Certainty> <Importance> <Privacy> [<referent> ...]) ([([verbatim psyche edit] (Some [target record being edited]))] [reasoning])))"
```

For this lane specifically: if the psyche affirms the mandatory bearings
flow, the right move is a **`Clarify` or `Supersede` of `2o3g`**, not a new
sibling record.
