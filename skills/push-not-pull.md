# Skill — push, not pull

*The principle is in `ESSENCE.md`. This skill is how to act
on it: how to recognise polling, how to design a
subscription, and how to escalate when the producer can't
push.*

---

## What this skill is for

When you have a producer of state and a consumer of changes,
this skill applies. The principle — **polling is forbidden;
producers push; consumers subscribe** — lives in `ESSENCE.md`
§"Polling is forbidden". Read it before reading further;
this skill assumes the rule and only describes how to act.

If you find yourself reaching for a polling loop, stop.
Apply the steps below.

---

## How to apply when designing

When designing or reading a producer-consumer interaction:

1. **Find the producer.** What component owns the state the
   consumer cares about?
2. **Find or build the producer's subscription primitive.**
   A callback registration, an event stream, a long-lived
   RPC, a Unix-socket subscriber pattern, an `inotify` watch
   on a file, a `timerfd` deadline. The shape varies; the
   contract is the same — the producer pushes; the consumer
   registers once.
3. **Write the consumer as a subscriber.** No `sleep(N)` in
   the consumer's main loop; no `interval` timers; no
   "check every K seconds" comments.
4. **If the producer can't push**, escalate (see below). Do
   not write a poll loop "for now."

In actor systems, each actor's mailbox is already a push
channel; nothing in the actor model requires polling. In
databases with change feeds, subscribe to the feed. In UIs
over a backing store, the store emits change events.

---

## When the producer can't push — the escalation rule

If the producer's subscription primitive doesn't exist yet,
the right path is one of:

1. **Build the primitive in the producer.** Usually the
   right answer if the producer is in scope.
2. **Replace the producer.** If the producer can't be
   modified, replace it with one that can push.
3. **Defer the dependent feature.** Real-time behavior
   waits until push ships. State this explicitly; don't
   pretend the feature is shipping.
4. **Escalate.** If none of (1)–(3) resolve the case at
   hand, the question goes up — to the next level of design
   responsibility, and ultimately to the human.

**Escalation is the correct outcome** when no push answer
is found. It is not a failure mode; it is the discipline
working. The human (or the next level of authority) decides
whether a new carve-out is justified, whether the producer
should be rebuilt, or whether the feature should wait.

The wrong outcome — falling back to a poll — is never the
answer. A poll once written is rarely removed; the cost is
paid forever.

---

## The named carve-outs

`ESSENCE.md` names three carve-outs that look polling-shaped
but aren't:

- **Reachability probes** ("is service X alive?").
- **Backpressure-aware pacing** (consumer drains its own
  buffer; producer still pushes).
- **Deadline-driven OS timers** (`timerfd` and equivalents;
  the kernel pushes the wake).

These three are exhaustive. When a design seems to need
polling and *none* of the three apply, the design needs an
escalation, not a fourth de-facto carve-out. Reach for the
escalation rule above; don't invent a local exception.

---

## Common pull-shaped traps

Patterns that smell ok but are actually polling:

- **A loop that re-reads a file every N ms** to detect
  changes. Polling. Replace with `inotify` (Linux) /
  `kqueue` (BSD/macOS) / a producer daemon emitting events
  on a Unix socket.
- **`sleep_ms(50); observe_again` for stable-state
  detection.** Polling. Replace with a producer event for
  the state transition you actually care about.
- **A retry timer for "unknown" state.** Polling. Replace
  with the event that resolves the unknown; if no such
  event exists, escalate.
- **A consumer "ticker" that drives reconciliation.**
  Polling. Replace with subscription + reactive
  reconciliation triggered by events.
- **"Check every poll-interval, debounce flickers."** The
  debounce is hiding the polling. Replace with the
  push-event source.
- **Asking an LLM agent to "check inbox every few turns."**
  Same anti-pattern at a higher level. Inbox should be
  pushed into the harness's terminal stream by a router, not
  pulled by the model.

When you catch one of these, the right move is either fix
it (build or wire the push primitive) or escalate.

---

## Recognising the symptom

Polling shows up as **wake-when-nothing-changed**. A
process that:

- shows steady syscall traffic on `strace -c` while idle,
- holds a near-constant context-switch rate visible in
  `/proc/<pid>/status`,
- emits log lines on a clock independent of input,

is polling. Push-correct systems go quiet when they have
nothing to do.

---

## See also

- `~/primary/ESSENCE.md` §"Polling is forbidden" — the
  canonical rule.
- this workspace's `skills/abstractions.md` — every
  reusable verb belongs to a noun; same discipline applied
  to behavior dispatch.
- this workspace's `skills/beauty.md` — when polling feels
  necessary, the right structure usually hasn't been found
  yet.
- this workspace's `skills/micro-components.md` —
  components communicate via subscription primitives, not
  by polling each other.
