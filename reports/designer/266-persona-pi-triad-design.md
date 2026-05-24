# 266 - Persona-Pi triad architecture sketch

**Status:** superseded by `/309 §7` for pi-triad shape; this report preserves the alternatives that informed the choice.

*Designer sketch of the persona-pi triad following the psyche's
2026-05-21 design dump (intent/persona.nota records 43-47).
Persona-pi is the Pi harness adapted into a persona-component
triad. The load-bearing architectural distinction is **dual-path
communication** (terminal-cell + harness API in parallel), not
one or the other.*

Speculative material is marked inline (e.g. `(designing-mode
speculative)`). Future agents should not act on speculative
sections as settled.

## 1. Where persona-pi sits in the component family

(Settled. intent/persona.nota record 43 - Decision Maximum.)

The persona system today is a family of triad components:
`persona-spirit` (apex, psyche-facing), `persona-mind` (state,
memory, skill store), `persona-orchestrate` (role claims, agent
lifecycle), `persona-router` (channel gating), `persona-terminal`
(terminal cell I/O), `persona-harness` (executes work), `persona`
(engine-manager, apex infrastructure).

**Persona-pi joins this family as a new triad** with the standard
shape per `skills/component-triad.md`:

```
persona-pi/                       runtime
  src/bin/persona-pi-daemon.rs    long-lived daemon
  src/bin/pi.rs                   thin CLI client
  bootstrap-policy.nota           first-start policy declaration
signal-persona-pi/                ordinary wire vocabulary
owner-signal-persona-pi/          owner-only authority/configuration
```

The CLI name `pi` is the thin client; the daemon is
`persona-pi-daemon`. The two signal contracts split by
who-can-call.

### What persona-pi is, conceptually

Persona-pi is **the Pi harness adapted for the persona system**.
Pi is a pre-existing harness; record 43 references it as an
established artifact. Persona-pi wraps that harness as a triad
component, bringing it under the persona authority graph, the
observability discipline, and the signal-tree philosophy.

The persona-pi daemon **runs an agent** in the same sense
persona-harness does. Where persona-harness wraps Claude/Codex
CLI harnesses, persona-pi wraps Pi.

## 2. The dual-path architecture

(Settled. intent/persona.nota record 43 - Decision Maximum.)

The agent inside persona-pi has **two communication surfaces**,
both live at the same time:

| Path | What it carries | Why |
|---|---|---|
| **Terminal-cell path** | Unix-side I/O: stdin/stdout/stderr, PTY bytes, file reads, shell commands | Pi is a Unix-native harness; standard CLI/file ops flow here |
| **Harness API path** | Direct calls into Pi's extension API: structured queries, model invocations, agent-internal control | Pi exposes a richer programmatic surface that bypasses the terminal abstraction |

### Why both, not one

A persona-harness agent today is *confined* to its terminal cell -
all interaction with the outside world flows through PTY bytes
that persona-terminal forwards. That confinement is load-bearing
for ordinary CLI agents (one observability point, one
authorization boundary).

Persona-pi breaks that confinement *deliberately*. Pi exposes
capabilities the terminal abstraction cannot represent faithfully -
structured tool calls, harness-level control, direct
extension-method invocation. Forcing those through the terminal
would either flatten them into stringified protocols (losing type
information) or require a parallel control protocol inside the
PTY stream (a wire violation).

The dual-path shape says: terminal cell carries Unix I/O; harness
API carries structured programmatic surface. Both are first-class.

### Data-flow shape

```
       persona-pi-daemon (signal-persona-pi surface)
              |                              |
              v                              v
       terminal cell                  harness API
       (Unix I/O, PTY bytes)          (Pi extension surface)
              |                              |
              +--------------+---------------+
                             v
                    Pi harness running the agent
```

Both surfaces are live at the same time. The agent in Pi
interacts through whichever surface matches the operation.

### Implication for the contract

`signal-persona-pi` must carry operation roots that distinguish
the two paths at the type level. The exact root shape is design
work (and partly depends on the Pi API surface - see §6.1), but
the principle is settled: terminal-cell operations and
harness-API operations should not collapse into one
undifferentiated bag.

### Distinction from persona-terminal's carve-out

`skills/component-triad.md` §"Named carve-outs" already names
persona-terminal's split `control.sock` (Signal) vs `data.sock`
(raw viewer bytes) - a high-bandwidth bytes carve-out.
Persona-pi's dual-path is **not** the same carve-out: both
persona-pi paths are typed and stay inside the wire discipline.
Persona-pi's pattern is new: two typed surfaces, both
load-bearing for different *kinds* of operation.

## 3. Extension layer and namespace adaptation

(Settled. intent/persona.nota record 46 - Principle Maximum.)

Pi's native extension namespace is **flat**: long underscored
function names with wide argument lists, e.g.
`query_negative_database_from_behind`. The persona system's
signal-tree philosophy rejects flat function namespaces
(`skills/abstractions.md`: verbs belong to nouns). Persona-pi's
extension namespace **does not mirror Pi's native one**.

### The translation rule

Each flat Pi extension function decomposes into a **noun** (the
typed object), a **method** (the verb that belongs to the noun),
and a **method argument record**.

Worked example from psyche:

| Pi native (flat) | Persona-pi extension (typed object tree) |
|---|---|
| `query_negative_database_from_behind(...)` | `NegativeDatabase.from_behind(...)` |
| `query_negative_database_from_front(...)` | `NegativeDatabase.from_front(...)` |
| `query_negative_database_from_below(...)` | `NegativeDatabase.from_below(...)` |
| `query_negative_database_from_above(...)` | `NegativeDatabase.from_above(...)` |

The noun `NegativeDatabase` collects every verb that has it as
the natural receiver. Direction (`from_behind`, `from_front`,
…) is a method on the noun, not a function suffix.

### Why this matters

`skills/abstractions.md` §"The forcing function" gives the
rationale: when a verb appears as a free function or flat
underscored name, the owning noun is hidden. Naming the noun
produces a recursive enum-shaped namespace where related verbs
cluster naturally on their owning type. The translation is the
same discipline applied to every signal-tree in the workspace.

### Shape of the harness-API operation root

The contract's harness-API operation root is **a sum of noun
types**, each with method variants. Illustrative shape (not the
actual variant set):

```
HarnessApiOperation
  ::NegativeDatabase(NegativeDatabaseOperation)
    NegativeDatabaseOperation
      ::FromBehind(FromBehindRequest)
      ::FromFront(FromFrontRequest)
      ::FromBelow(FromBelowRequest)
      ::FromAbove(FromAboveRequest)
  ::OtherNoun(...)
```

The recursive enum shape lets queries select on noun, on method,
or on (noun, method) pair - the pattern `signal-sema` uses for
class observation.

### Which Pi extensions get adapted (speculative-pending-research)

The full inventory of Pi's native extension surface is not in
this report. The Pi-API-research subagent's notes were expected
at `reports/designer/pi-api-surface-notes.md` but that file does
not exist at writing time. **The adaptation rule (one noun per
domain, one method per verb-direction) is settled even though
the inventory is not.** A successor report can draft the noun
catalogue once the research lands.

## 4. The composite-designer flow

(Settled. intent/persona.nota record 45 - Decision Medium.)

Record 45 introduces the first concrete **composite role**: the
designer role runs **Claude AND Codex in parallel** against the
same prompt, with an orchestrator step that selects from or
merges the outputs.

Persona-pi is the substrate for the Codex parallel arm. Today's
Claude designer runs in its own harness (Claude Code); the
composite-designer's parallel runs Codex inside persona-pi.

### Flow shape

```
              psyche prompt
                    |
                    v
            composite designer role
                  /     \
   parallel fan-out
                /         \
   Claude in              Codex inside
   Claude Code            persona-pi
                \         /
                 \       /
       orchestrator's select/merge
                    |
                    v
   designer output (intent records, reports, beads)
```

### Why persona-pi hosts the Codex arm

Codex is a CLI harness; ordinary CLI agents already route through
persona-harness. What persona-pi adds for the composite-designer
case is **structured access to Codex's harness API alongside the
terminal cell** - the same dual-path from §2. The
composite-designer needs more than a stdin/stdout transcript: it
needs typed access to structured output, tool-use records, and
control surfaces. The harness-API path carries those; the
terminal-cell path carries the ordinary CLI traffic. The Claude
arm runs in Claude Code for the symmetric reason.

### Settled vs speculative here

**Settled:** composite designer exists; runs Claude and Codex in
parallel; orchestrator step selects-or-merges; Codex arm runs in
persona-pi.

**Speculative (designing-mode):** the actual select/merge policy
(see §6.2); whether composite roles beyond designer will exist
(record 45 names this as the *first*, not a pattern); the
orchestrator's identity (persona-orchestrate is the natural
candidate but record 45 does not name it).

## 5. Model-by-role principle and persona-pi's default

(Settled. intent/persona.nota records 44 + 47.)

Record 44 (Principle Maximum) declares: **role determines model.**

| Role | Model |
|---|---|
| Designer | Claude |
| Advisor | Codex |
| Persona Pi (default) | GPT-latest with Maximum Thinking |

Composite roles are possible (record 45 is the first); a
composite role's model choice is the union of its parts.

Record 47 (Decision Medium) sets persona-pi's default config:
GPT-latest with Maximum Thinking, pre-configured. Per
`skills/component-triad.md` invariant #5, this lives in
persona-pi's `bootstrap-policy.nota` as policy state, mutable
afterwards only through owner-signal `Mutate` verbs.

### What the mapping does NOT mean

It does not mean any persona binary embeds a model. Per
`intent/persona.nota` record 8 (in workspace INTENT.md form),
persona components are dumb mechanism; LLM calls are made by
the agents that drive them. The role-model mapping is **which
model the role's agent invokes when making an LLM call** -
policy at the agent level, expressed at the role boundary.

### Interaction with LLM-call fallback chains (speculative)

`/264` §6 sketches per-call default + fallback chains. The
role-model mapping provides the default; fallbacks cover
failure. Composition is unsketched in psyche material.
**(designing-mode speculative.)**

## 6. Speculative pieces flagged

Each item is **not yet settled**. Future agents should not treat
these as designer commitments.

### 6.1 Harness API surface (speculative-pending-research)

What Pi's actual harness API surface looks like - which extension
nouns exist, which verbs each carries, which arguments shape - is
not in this report. The Pi-API-research subagent's expected
output at `reports/designer/pi-api-surface-notes.md` does not
exist at writing. **All Pi-API specifics are
speculative-pending-research** until that file lands. Successor
report can draft the noun catalogue.

### 6.2 Orchestrator select/merge policy (designing-mode speculative)

Record 45 says "selects or merges" without specifying when each
applies. Open variants: always-merge (concatenate /
cross-reference); always-select-one (a single tie-breaker rule);
domain-dependent (different policies per operation class);
surfaced (both outputs to psyche); LLM-mediated (a third model
adjudicates). **Do not act on a particular policy as if settled.**

### 6.3 Composite roles beyond designer (designing-mode speculative)

Record 45 calls the composite-designer the *first* concrete
composite role. Whether other composite roles will exist is
direction, not commitment. **Do not generalise to a "composite
role pattern" without further psyche intent.**

### 6.4 Authority graph placement (designing-mode speculative)

Where persona-pi sits in the persona authority graph
(engine-manager → spirit → mind → orchestrate → ...) is not
stated. The likely shape is orchestrate-owns-pi (since orchestrate
owns harness, router, terminal per `intent/persona.nota`
2026-05-19T15:30:00Z), but this is not explicit.

### 6.5 Interaction with persona-terminal (designing-mode speculative)

Persona-pi's terminal-cell path overlaps conceptually with
persona-terminal (both deal with Unix-side I/O for an agent).
Whether persona-pi *uses* persona-terminal internally, or
implements its own terminal-cell surface in-tree, is undesigned.
The duplication question is real; should surface as a designer
follow-up before implementation begins.

### 6.6 Observability discipline

Per `intent/persona.nota` 2026-05-21T10:00:00Z ("debug the
debugger"), every persona component is observable. Persona-pi
must declare `observable` blocks on both signal channels. Whether
the harness-API path needs different operation/effect events from
the terminal-cell path is design work. **Tap/Untap mandate applies;
specifics are speculative.**

## 7. Open psyche questions

**Q1 - Is the dual-path shape unique to persona-pi, or does it
generalise?** Record 43 frames the dual-path as persona-pi's
load-bearing distinction. But persona-harness is single-path. If
the dual-path is right for persona-pi, is it right for any future
component wrapping a structured-API harness? If so, this becomes
a named triad sub-pattern in `skills/component-triad.md`.
*Designer lean: probably general; this is psyche territory.*

**Q2 - Relationship between persona-pi's agent identity and
Criome identity (speculative on both sides).** `/264` §4
sketches per-agent Criome identities. If composite-designer
runs Claude in one harness and Codex in persona-pi, does each
arm have its own Criome identity, or do they share the
composite-designer's role identity? Waits for Criome direction
to settle.

**Q3 - Does the Codex-in-persona-pi arm of composite-designer
read the same designer skills as Claude's arm?** Per `/264` §1
the designing protocol is the psyche-to-designer interface; in
the composite both arms receive the same psyche prompt. Whether
both arms also read the same designer skills, and whether
persona-pi's bootstrap-policy.nota carries the designer skill
bundle or expects mind to ship it on boot per
`intent/persona.nota` record 40 (skill loading from mind), is
undesigned. *Most-likely answer: same skills, mind delivers on
boot; persona-pi bootstrap path is unsketched.*

## See also

- `intent/persona.nota` records 43-47 (persona-pi triad,
  per-role model, composite designer, namespace adaptation,
  default config). Verbatim source.
- `reports/designer/264-designing-protocol-and-role-spaces.md`
  - persona-pi substrates the composite-designer of `/264` §2;
  the per-role-protocol model of `/264` §1 grounds the
  model-by-role principle here.
- `skills/component-triad.md` - the triad-shape discipline
  persona-pi follows.
- `skills/abstractions.md` - the verb-belongs-to-noun rule the
  namespace adaptation enforces.
- `skills/nota-design.md` - the typed-record vocabulary the
  adapted extension namespace uses.

This report retires when (a) Pi-API-research lands and the noun
catalogue is drafted in a successor, AND (b) psyche addresses
§7, AND (c) persona-pi moves from designer sketch into operator
beads. Until then, this is the canonical sketch.
