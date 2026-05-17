# Skill — component triad (daemon + CLI + signal-* contract)

*The universal shape for every stateful capability in the workspace.
Daemon owns state and speaks Signal. CLI is a thin bridge — one NOTA in,
one NOTA out, exactly one peer. Contract crate owns the typed wire
vocabulary and the per-variant verb mapping. Read this before designing
or auditing any new component.*

---

## The shape

Every stateful capability in this workspace is a **triad**:

```
<component>/             repo for the runtime
  src/lib.rs             component library
  src/bin/<name>-daemon  long-lived daemon binary (actor root + storage)
  src/bin/<name>         thin CLI client binary
signal-<component>/      repo for the typed wire vocabulary
  src/lib.rs             signal_channel! { ... } declaration
                         + per-variant SignalVerb mapping
  tests/round_trip.rs    rkyv + NOTA round-trips
```

Three load-bearing invariants. Each becomes a witness test (per
`skills/architectural-truth-tests.md`):

1. **The CLI has exactly one Signal peer — its own daemon.** No CLI is a
   workspace multiplexer; no CLI directly opens another component's
   database, socket, or in-memory state. The CLI is a text adapter for
   *one* daemon's contract.

2. **The daemon's external surface is exclusively `signal-core` frames.**
   No `serde_json` socket, no NOTA on the wire between components, no
   parallel control protocol. NOTA exists at three named projection
   edges — CLI argv/stdin, daemon ↔ harness terminal, audit/debug dumps
   — never inter-component.

3. **The verb is declared per-variant in the contract crate, not typed
   by the user.** Each `signal_channel!` request enum variant carries
   one of the six `SignalVerb` roots; the CLI's NOTA sugar omits the
   verb because the contract resolves it from the payload type.

The triad is filesystem-enforced (per `skills/micro-components.md`): one
daemon + CLI in `<component>` (typically one Cargo crate with two
`[[bin]]` entries), one contract in `signal-<component>`. The contract
crate carries no runtime, no actors, no `tokio`.

---

## Why this shape

A CLI invocation is a short-lived process. It cannot supervise actors,
own a `redb` handle across requests, hold subscription streams, or
sequence operation IDs. **A daemon does all four.** The CLI exists
because humans and early agents need a text bridge into the typed wire;
once peer components speak Signal directly (which they already do —
`persona-introspect`'s daemon queries `persona-router` over
`signal-persona-router`), the CLI is no longer load-bearing for that
path.

The CLI is **eventually obsolete machinery**. Keep CLI-side logic thin
accordingly. Per `lojix/ARCHITECTURE.md` §"CLI/daemon boundary": *"Until
agents can speak binary Signal directly, the CLI exists only to
translate human/agent text into daemon Signal and daemon Signal back
into text."*

---

## The six verbs and what each one means

The `SignalVerb` set is closed at six roots (in `signal-core/src/verb.rs`):

| Verb | Direction | What it means |
|---|---|---|
| `Assert` | bottom-up or peer | append a new typed fact / event / row |
| `Mutate` | **top-down authority order** — *"change this, I don't care what you think"*. Authority issues; subordinate obeys and confirms | replace / transition a record at stable identity |
| `Retract` | top-down authority order | tombstone / remove a typed fact |
| `Match` | any direction | one-shot pattern / range / key query |
| `Subscribe` | observer ↔ producer | initial state + commit-deltas (push, not poll) |
| `Validate` | any direction | dry-run an operation without commit |

**Mutate is the authority verb.** When persona-mind issues a `Mutate` to
`persona-orchestrate`, mind is *ordering* a change, not asserting a
fact. The recipient obeys and confirms; the issuer transitions its own
state from *possibly-mutated* to *now-mutated* on the confirmation, and
only then proceeds to any downstream order (spawn the harness, install
the channel, deliver the message). The Mutate chain is how the system
maintains correctness *from the top down*. Without the explicit
authority-verb framing, the same chain devolves into ambiguous
"requests" with no protocol for who has the right to refuse.

**Subscribe flows the other way.** Authority *observes* state via
push-subscriptions from down-tree (per `skills/push-not-pull.md`),
*decides*, and *orders* via Mutate down-tree. Observation up, authority
down.

**Assert is for new facts.** When a CLI user sends a message, the
component asserts the message exists. When a sensor records an
observation, it asserts the observation. No authority chain — just *a
new typed fact entered the system*.

The contract crate (`signal-<component>`) declares the verb per request
variant inside the `signal_channel!` macro. The CLI's NOTA-sugar
omits the verb keyword because every variant maps to exactly one verb.
Concrete: `message '(Send recipient "hi")'` desugars to
`(Assert (MessageSubmission (MessageRecipient recipient) (MessageBody "hi")))`
because `signal-persona-message` declares `MessageSubmission → Assert`.

---

## Named carve-outs

These look like triad violations but aren't. Each is *narrow*; do not
extend the pattern of carve-outs.

1. **Pure libraries don't need a daemon.** `signal-core`, `sema`,
   `sema-engine`, `horizon-rs` (projection library) own no state and
   cross no process; the triad does not apply. A test CLI like
   `horizon-cli` for ad-hoc projection is convenience, not a triad.

2. **Data-plane bytes that cannot afford Signal framing.** When a
   component has a high-bandwidth byte path (raw PTY bytes, video,
   audio), the data plane is a separate socket outside the triad. The
   control plane still follows the triad. Canonical example:
   `persona-terminal`'s `control.sock` (Signal) vs `data.sock` (raw
   viewer bytes); raw bytes flow viewer ↔ `terminal-cell` `data.sock`
   directly. Document the exception in the component's ARCH.

3. **A daemon may be a Signal client of any number of peer daemons.**
   `persona-introspect`'s daemon opens client connections to
   `persona-router`, `persona-terminal`, `persona-manager` over their
   contracts. This is the right shape. **The CLI's "exactly one peer"
   constraint does not extend to daemons** — fanning out across peers is
   how daemons compose. What the daemon may not do is bypass another
   daemon's contract (no opening another component's redb, no shared
   in-memory state).

---

## The witness tests every triad ships

Each constraint becomes a test (per `skills/architectural-truth-tests.md`).
Use these exact names so the discipline reads at a glance:

| Test | Proves |
|---|---|
| `<component>-cli-accepts-one-nota-record-and-prints-one-nota-reply` | The CLI is one-NOTA-in-one-NOTA-out. |
| `<component>-cli-has-exactly-one-signal-peer` | The CLI cannot multiplex across daemons. |
| `<component>-daemon-rejects-non-signal-traffic-on-its-socket` | The daemon's external surface is exclusively `signal-core` frames. |
| `<component>-signal-verb-mapping-covers-every-request-variant` | Every request variant has a declared `SignalVerb`. |
| `<component>-cli-cannot-open-peer-database-or-socket` | The CLI never bypasses its daemon. |

---

## Authority chain — worked example

Persona's correctness is maintained top-down via Mutate chains.
Concrete: when persona-mind decides a new agent needs a channel grant
so it can talk to the router:

```mermaid
flowchart TB
    mind["persona-mind<br/>(authority root)"]
    orch["persona-orchestrate<br/>(spawning / supervision)"]
    router["persona-router<br/>(channel authority)"]
    harness["persona-harness<br/>(executes work)"]

    mind  -- "1. Mutate: spawn agent X in lane Y" --> orch
    orch  -- "2. ack mutated"                     --> mind
    mind  -- "3. Mutate: install channel grant"   --> router
    router -- "4. ack mutated"                     --> mind
    mind  -- "5. Mutate: spawn harness w/ rights" --> orch
    orch  -- "6. spawn"                            --> harness
    orch  -- "7. ack mutated"                     --> mind

    harness -. "Subscribe: lifecycle events"  .-> mind
    router  -. "Subscribe: delivery events"   .-> mind
    orch    -. "Subscribe: agent lifecycle"   .-> mind
```

At each Mutate step the issuer holds *possibly-mutated* state until the
ack arrives; only then does it advance to the next order. Replies are
not opinions — they are confirmations. The authority chain is what
makes the next step safe: the harness is not spawned with channel
rights until the router has confirmed the channel exists.

---

## When this skill applies

- **Designing a new stateful component.** Default to the triad. If the
  shape doesn't fit, write down which named carve-out justifies the
  divergence — or escalate to the user before deviating.
- **Auditing an existing component.** Check it against the three
  invariants and the witness tests. Surface deviations in a report.
- **Reading a component's `ARCHITECTURE.md`.** The ARCH should *cite*
  this skill and only state component-specific carve-outs — not
  restate the universal invariants.

---

## See also

- `~/primary/ESSENCE.md` §"Micro-components" — the one-capability-one-
  crate-one-repo rule the triad applies on top of.
- `~/primary/skills/micro-components.md` — file-system-enforced
  per-capability boundary; the triad is the *shape inside the
  boundary*.
- `~/primary/skills/contract-repo.md` — what lives in a `signal-*`
  contract crate; the verb spine; the boundary table for where NOTA
  renders.
- `~/primary/skills/actor-systems.md` §"Runtime roots are actors" —
  the daemon's actor-root shape.
- `~/primary/skills/push-not-pull.md` — Subscribe, not poll.
- `~/primary/skills/architectural-truth-tests.md` — witness-test
  discipline for the constraints above.
- `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md` — the wire
  kernel; closed six-root verb set; `signal_channel!` macro.
- `~/primary/reports/designer/209-component-triad-daemon-cli-contract-2026-05-17.md`
  — the audit that established this skill's scope.
- `~/primary/reports/designer/210-component-triad-decisions-and-mutate-authority-2026-05-17.md`
  — Mutate's authority semantics, the orchestrate component context,
  follow-ups.
