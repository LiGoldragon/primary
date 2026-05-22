# Mind/Orchestrate Payload Shape And CLI Dispatch Option A Sketch

Follow-up to the prior research turn that posed open questions about the
mind→orchestrate vocabulary and the working/policy CLI socket dispatch. The
psyche has supplied substantial answers; this report integrates them and
sketches Option A in code form.

## What Was Captured To Intent

Logged this turn:

- `intent/persona.nota` — eleven entries: mind/orchestrate boundary as
  concept/mechanism split, agent registry shape, reuse-over-spawn lean,
  context-compaction responsibility, abstract-job decomposition,
  owner-channel programmability of orchestration policies, skills-bundle-into-roles,
  router as channel-gate, default open mind-channel for all agents,
  skill bundle delivery at boot, on-demand extension skills.
- `intent/signal.nota` — CLI dispatch rejection of options B and C; option A
  candidate pending sketch.
- `intent/workspace.nota` — foundational principle: anything that can be done
  mechanically will not be done by agents.

## On "Carrying A Sum"

The psyche asked what "sum" means. In type-theory vocabulary, a *sum type* is
a type whose value is one of several alternatives — Rust's `enum`, OCaml's
`type t = A | B of int | C of string`, Haskell's `data`. Contrasted with
*product types* (structs: every field present together). When the prior
research said "a request carrying a sum," it meant the request body is an
enum variant — one of several distinct shapes, only one inhabited at a time.

Concretely in this workspace: `SpiritOperation` (in
`signal-persona-spirit`) is a sum:

```rust
pub enum SpiritOperation {
    State(Statement),
    Record(Entry),
    Observe(Observation),
    Watch(Subscription),
    Unwatch(SubscriptionToken),
    Tap(...),
    Untap(...),
}
```

The phrase "the request carries a sum" means "the request body is a value of
some enum, not a struct." Going forward this report uses the explicit phrase
*"enum variant"* or *"tagged union"* in place of *"sum"* — the latter is
unfamiliar vocabulary even though it is the established term in type theory.

## Option A: signal-cli Macro Sketch

The contracts already supply everything Option A needs. Confirmed by reading
`signal-persona-spirit::SpiritOperation` (working) and
`owner-signal-persona-spirit::OwnerSpiritOperation` (policy): each enum's
variant tags (State / Record / Observe / Watch / Unwatch / Tap / Untap on the
working side; Start / Drain / Reload / Register / Retire on the policy side)
have **no overlap**. The CLI can dispatch on the head tag with zero
ambiguity, statically determined at compile time.

### Hand-Written Form (No Macro)

Today's `persona-spirit/src/bin/spirit.rs` is three lines. The Option A shape
expanded inline is roughly:

```rust
use persona_spirit::{Result, SingleArgument};
use signal_persona_spirit::SpiritOperation;
use owner_signal_persona_spirit::OwnerSpiritOperation;

fn main() -> Result<()> {
    let argument = SingleArgument::from_environment()?;
    let nota = argument.as_nota_str();
    let head_tag = peek_head_tag(nota)?;

    match head_tag {
        // Working contract operations
        "State" | "Record" | "Observe" | "Watch" | "Unwatch" | "Tap" | "Untap" => {
            let operation: SpiritOperation = decode(nota)?;
            send_to_working_socket(operation)
        }
        // Policy contract operations
        "Start" | "Drain" | "Reload" | "Register" | "Retire" => {
            let operation: OwnerSpiritOperation = decode(nota)?;
            send_to_policy_socket(operation)
        }
        other => bail!("unknown operation tag: {other}"),
    }
}
```

This is correct but mechanical noise: the variant lists are duplicated from
the contracts. If a contract adds an operation, the CLI silently drops it.

### Macro Form

The macro takes the two contract crate names and expands to the dispatch
above, with the variant lists derived from the contract enums at compile
time:

```rust
// in persona-spirit/src/bin/spirit.rs
signal_frame::signal_cli! {
    cli spirit;
    working signal_persona_spirit::SpiritOperation;
    policy  owner_signal_persona_spirit::OwnerSpiritOperation;
    socket  "persona-spirit";  // socket-name prefix; .ord and .own suffixes
}
```

Macro responsibilities:

1. At compile time, inspect both operation enums (already `NotaEnum`-derived
   in `signal-persona-spirit/src/lib.rs:198-206` and
   `owner-signal-persona-spirit/src/lib.rs:91-100`).
2. Build a compile-time set of working variant tags and a compile-time set of
   policy variant tags.
3. Compile-time check: error if any tag is in both sets. This is the
   guarantee that makes dispatch unambiguous — and it makes naming
   collisions a build-time failure, not a runtime confusion.
4. Generate the `fn main()` that peeks the head tag, matches, decodes the
   correct enum, and sends to the corresponding socket using the existing
   `SpiritClient`/`OwnerSpiritClient` machinery.

For `persona-spirit` today this would replace the three-line `spirit.rs` with
the macro invocation above. The hand-written `spirit.rs` becomes a fallback
for components that need custom CLI behavior, but the default for every
component triad is the macro.

### What signal-frame Needs To Add

`signal-frame::macros` already owns `signal_channel!`. Adding `signal_cli!`
is additive — same crate, same input style (the contract crate path). It
reads the existing `NotaEnum`-derived metadata; no new derive is required on
the contracts.

The one extra capability needed is a *head-tag peek* on a NOTA string
without full decode. `nota_codec::Decoder` can already do this — read one
token and stop. The macro emits a small helper that peeks the head tag and
dispatches, then calls the full enum decoder.

### Socket Locate

The macro takes a socket-name prefix; the working socket is
`<prefix>.ord.sock` and the policy socket is `<prefix>.own.sock` (or
whatever naming convention `persona-spirit/src/runtime.rs` already
establishes). This is a convention; the macro should match it rather than
invent a new one.

### Failure Modes

- Unknown tag → exit with `unknown operation tag: <tag>` and exit code 2.
  No NOTA reply is emitted because no contract framed the request.
- Decode error after tag match → the tag was a working tag, but the payload
  failed to decode as `SpiritOperation` — exit with the codec error message.
- Socket send error → exit with the connection error message.

All three are mechanical mappings to non-zero exit codes; agents get the
error text on stderr and the exit code on the process.

## Walkthrough Of Prior Research Questions With Psyche Input

The prior research turn posed several open questions. Status after this
turn's psyche input:

### Q1 — Cognitive vocabulary (verbs and abstractions) for mind→orchestrate messages

**Resolved.** The vocabulary is abstract-job-shape, not mechanism-shape.
Examples the psyche gave: "we need research done on such-and-such topic
by skill-type-Y agent"; "we need a new REST component developed to do X
named Y." The orchestrator decomposes into mechanical sequences; mind never
states the sequence.

**Still open (design follow-up):** the concrete NOTA record shape for these
abstract job requests. Candidates: `ResearchTopic { topic, skill_type,
priority }`, `CreateComponent { component_name, behavior_description,
component_kind }`, `RefineDocument { path, refinement_intent }`. Designer
work, not blocked on psyche.

### Q2 — Authorized channel concept — orchestrate or more abstract?

**Resolved.** The router is the channel-gate; channel authorization lives in
`owner-signal-persona-router`. Agents query the router to enumerate
reachable agents. Orchestrator is separate — it allocates agents and
sequences work, not channels.

**Still open:** the read-side API on the router. Candidates: `(Observe
ReachableAgents)`, `(Observe ChannelGrants)`. Designer-lane.

### Q3 — "Carrying a sum"

**Resolved by clarification.** Sum = enum variant / tagged union (see
section above). Going forward use "enum variant" or "tagged union."

### Q4 — Mind-orchestrate payload — endpoints, router-level, or purpose?

**Resolved.** Purpose level. The payload expresses *what is to be done*, not
*who is to do it* or *where to reach them*. Endpoint and router-level
decisions belong to orchestrate and router respectively.

### Q5 — CLI working/policy dispatch — Option A / B / C?

**Resolved.** Options B (NOTA wrapper requiring agent to name the socket)
and C (try-parse cascade) are rejected. Option A — compile-time macro
dispatch — is the chosen shape. See sketch above.

**Still open:** the macro's exact surface name (`signal_cli!` vs extending
`signal_channel!` with an optional CLI block). Both are fine; the cleaner
separation is a separate `signal_cli!` macro, but a `signal_channel!`
extension with `cli yes;` is also workable. Designer judgment.

## New Design Questions Raised By This Turn's Input

These follow from the psyche's substantive input on mind/orchestrate/router/skills
and are likely designer-lane unless flagged for psyche.

### N1 — Agent-type enum scope (designer / psyche-touch)

The psyche named designer, coding, research, system-specialist as agent
types. The workspace's existing role enum (in skills/role-lanes.md) names
operator, designer, system-specialist, poet. There's overlap but not
identity. The agent registry's type enum should reconcile with the existing
role taxonomy or explicitly diverge. **Question for psyche:** is "agent
type" the same enum as "role" (operator/designer/system-specialist/poet
plus a few new ones like research/coding), or is it a separate broader
taxonomy that includes things like "auditor" and "infrastructure"?

### N2 — Orchestration policy NOTA record shape (designer-lane)

The psyche described policy as "when this typed job class arrives, run
such-and-such sequence of agent-type assignments; on success → next; on
failure → handler." Sketch in NOTA:

```nota
(Policy
  (JobClass NewComponent)
  (Sequence
    (Step (AgentType Infrastructure) (Goal "create repo and boilerplate")
          (SuccessCondition "structure exists") (OnFailure Halt))
    (Step (AgentType Auditor) (Goal "verify boilerplate")
          (SuccessCondition "audit ok") (OnFailure RetryWith Infrastructure))
    (Step (AgentType Coding) (Goal "implement behavior")
          (SuccessCondition "tests pass") (OnFailure Escalate))))
```

This is designer-derived from psyche's prose; it should land as a design
proposal report, not as intent.

### N3 — Skill bundle delivery message shape (designer-lane)

The psyche specified "one message carrying all skills for the role." Sketch:

```nota
(SkillBundle
  (Role RustCoding)
  (Skills (Skill "naming" "...content...") (Skill "jj" "...content...") ...))
```

The skill content shape (markdown? NOTA? hash-only with content-addressable
fetch?) is open. Designer-lane.

### N4 — Extension skill request shape (designer-lane)

The psyche specified an agent asking the mind for additional skills mid-task.
Sketch:

```nota
(RequestExtensionSkills (Skills "advanced-macros" "lifetime-tricks"))
```

Reply uses the same `SkillBundle` shape as boot. Designer-lane.

### N5 — Context-compaction threshold (psyche-touch eventually, not urgent)

The psyche left the threshold open. Default proposal: compact on
reassignment (always compact when an agent finishes a task and is reassigned
to a new abstract job, regardless of current context size). Alternative: a
percentage threshold (e.g., 70% of context window). Compact-on-reassignment
is simpler and matches the workspace's "reuse-over-spawn" lean — every
reassignment is a natural compaction boundary.

### N6 — Reachable-agents query semantics (designer-lane)

When an agent asks the router "which agents can I reach," does it get the
list filtered by what the asking agent is authorized to talk to, or the full
running-agents list? Default: filter by channel-grant. Otherwise the query
leaks information about the orchestration topology to agents that shouldn't
see it. Designer-lane unless psyche has a view.

## Items Still Needing Psyche

Only one carries enough weight to ask:

- **N1 (agent-type enum scope).** Naming the agent-type enum requires
  knowing whether it equals the role enum (just with research/coding/
  auditor/infrastructure added) or is a separate broader taxonomy. Both are
  workable but the choice shapes the orchestrate component's data model and
  the future role-creation flow.

Everything else is designer-derivable from the intent captured this turn.

## Recommended Next Slice

1. Land `signal-frame::signal_cli!` macro per the sketch above. Smallest
   plausible scope: dispatch + decode + socket send + compile-time tag
   uniqueness check.
2. Replace `persona-spirit/src/bin/spirit.rs` with the macro invocation as
   the first witness.
3. Designer-lane proposals on N2–N6 once the macro is in place — these are
   the persona-orchestrate / persona-mind / persona-router design shapes
   that follow from the intent captured this turn.
