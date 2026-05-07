# Niri input gate — audit

Date: 2026-05-07
Author: Claude (designer)

An audit of the operator's
`reports/operator/7-minimal-niri-input-gate.md`. The report
is materially well-shaped: push-not-pull discipline holds
end-to-end, scope is genuinely minimal, the actor model is
clean, the audit questions surface uncertainty rather than
hide it. This audit replaces the prior gate audit (deleted
in the same hygiene pass that landed this one).

---

## What the report gets right

- **Push-not-pull throughout.** Niri's IPC EventStream is
  the producer; the router subscribes; the router never asks
  Niri "who is focused?" on a clock. The conditional
  subscription (subscribe on first focus-blocked delivery,
  unsubscribe when the focus-blocked queue empties) lands
  the discipline cleanly without leaving a stream open
  forever.
- **`blocked_on_unknown` stays queued with no timer.** Per
  push-not-pull's strict form: if no producer can resolve
  the unknown, no retry timer fakes a resolution. The
  message stays. (See Concerns §3 for the bounded-memory
  follow-up.)
- **Closed enums for block reasons.** The three reasons
  (`blocked_on_focus`, `blocked_on_non_empty_input`,
  `blocked_on_unknown`) are an exhaustive set. Each is
  paired with the producer that resolves it. No
  string-tagged dispatch.
- **Two-predicate gate.** The gate is now `focus +
  input-buffer-empty`, not `focus + prompt-empty + idle`.
  Merging the two non-focus predicates into one
  *input-buffer-empty* check is a real structural
  simplification: one observer (`InputBufferActor`) replaces
  two; one waiting state (`WaitingForInput`) replaces two.
  The merge holds because "input buffer is empty" implicitly
  requires the prompt to be showing — when the harness is
  generating output, there is no input buffer to be empty,
  so the gate stays blocked. One signal subsumes both
  conditions.
- **Actor model with method ownership.** The methods table
  spells out which actor owns which verb. `RouterActor`
  owns queue/subscriptions. `HarnessActor` owns target state
  + delivery. `NiriFocusSourceActor` owns the IPC stream.
  No free-floating delivery function; the verb belongs to
  the noun that owns the data.
- **Tests-first, fixtures-first.** Recorded Niri JSON-line
  fixtures drive the router state machine before live Niri
  is involved. The fixture-fake-live progression keeps the
  test surface tractable.
- **Self-aware audit questions.** Five explicit open
  questions, each tied to a concrete tension. This is the
  shape design reports should take.
- **Race acknowledged, not papered over.** "Safe observation
  → human can still type before terminal bytes are
  submitted" is named. The mitigations narrow the window;
  they do not pretend to close it. The destination (native
  adapters / focus lease) is the eventual answer.

---

## Concerns

### 1. Non-Niri systems — name the deferral rule

The report's scope is Niri only. Per `ESSENCE.md`
§"Polling is forbidden" and the no-polling delivery design
(report 12), the implication: **on systems without Niri,
focus-gated delivery is unavailable.** Messages with
`blocked_on_focus` for harnesses on a non-Niri system stay
queued indefinitely until the user discharges them, the
TTL expires, or a different `DesktopEventSource`
implementation lands.

The report should state this rule explicitly. Right now
it's implicit ("focus-unobservable → message queued"); a
fresh reader could reasonably wonder whether the gate falls
back to something. The answer is no — by design.

### 2. `WaitingUnknown` needs TTL for memory bounds

Per the no-polling delivery design (report 12) §7, the one
acceptable timer carve-out is a **deadline-driven OS timer**
(`timerfd` or equivalent) for TTL expiry on pending
messages. The Niri gate report doesn't mention TTL.

Without a TTL, a `WaitingUnknown` message stays in memory
forever. Push-not-pull permits indefinite deferral *as a
discipline*; bounded queues require a TTL clock as the one
named carve-out.

Worth a paragraph in the report stating: *every pending
message has a TTL (default 24h); expiry is event-driven
via OS-pushed timerfd; expired messages move to an
`Expired` state in the durable log*.

### 3. Niri window-id stability — make rebind explicit

The audit table flags this as an open question. The clean
answer for the workspace's discipline:

- **Niri window IDs are stable for a window's lifetime.**
  When the window closes, the ID is gone.
- **The `HarnessActor` holds the binding** and emits a
  `BindingLost` event when its window closes. Pending
  deliveries for that target either re-bind (when a fresh
  window for the same harness opens) or expire (per TTL).
- **Explicit rebind, never inferred.** A new window
  matching the harness's `app_id` / title is *a candidate*
  for rebind; the rebind itself is an explicit operation
  (CLI command or registry rule), not an automatic match.

The report's "harness registry binds a Persona harness to a
Niri window id" sentence is the right shape; the BindingLost
event closes the loop.

### 4. `HarnessActor` methods — collapse to one entry point

The methods table lists "decide delivery, deliver, defer"
as three method-shapes. Cleaner: **one entry point** —
`AttemptDelivery(message) -> Decision` where
`Decision = Delivered | Deferred(BlockReason)`. The
deciding and the delivering are implicit in the
implementation; the API is a single typed call returning a
typed result.

This pairs with the closed `BlockReason` enum and avoids
the "verb in three pieces" smell.

### 5. Subscription multiplicity — single subscription per source

The conditional-subscription section discusses
subscribe-on-first-block / unsubscribe-on-empty. Implicit:
**a single subscription per source-target pair** (or per
source, depending on the source's filtering capability).
Five messages blocked on focus for the same target trigger
**one** Niri subscription, not five.

The state machine should make this explicit: the
`subscribed_targets` set on `NiriFocusSourceActor` (or
`focus_blocked_count` per target on `RouterActor`) gates
when the IPC stream opens and closes.

### 6. "Input buffer empty" needs a precise definition

The merge of prompt-empty + idle into input-buffer-empty is
clean *if* the recognizer can correctly identify the
"input buffer exists and is empty" state. Different
harnesses paint their input buffers differently:

- Pi: a prompt box; the input buffer is the line(s) inside
  it.
- Claude: a `> ` line at the bottom; input is the rest of
  that line.
- Codex: a `>` marker; same shape.

When the harness is mid-generation, there is no input
buffer at all — that should map to *not empty* (or
*unknown*), since the gate must stay blocked.

The report should specify the recognizer's two predicates
explicitly: *(a) is an input buffer present? (b) does it
contain only the prompt chrome with no user characters?*
Both must be true to count as "empty." Either false → the
gate stays blocked. The per-harness recognizer logic lives
in a closed `Harness` enum (operator's report 12 §3.1
naming) with per-variant methods.

### 7. Relationship to the broader no-polling design

Report 12 (`no-polling-delivery-design.md`) names the
broader push-primitive surface: WezTerm Lua, X11, Sway,
Hyprland, plus parsed-screen-state events. The Niri gate
is the first concrete slice. Worth one sentence in the
Niri report stating *this is the Niri-only first cut of
report 12's push-primitive surface; other compositors land
as parallel `DesktopEventSource` implementations, and the
input-buffer observer becomes the harness-side equivalent.*

---

## Operator's audit questions — designer's reads

The operator posed five explicit questions. My reads:

### Q1 — Is conditional subscription worth the complexity?

**Yes.** The state is trivial: a counter or set of
focus-blocked targets, one branch on increment-from-zero
(open stream), one branch on decrement-to-zero (close
stream). The cost is ~10 lines. The benefit is the system
goes quiet when no work is pending, which makes idle-process
syscall traces clean (per report 12 §9.1's verification
plan). Keep it.

### Q2 — Is Niri window id stable enough?

**Stable per window lifetime; explicit rebind across
window-close-reopen.** See Concern §3. The HarnessActor
emits `BindingLost` on close; pending deliveries either
rebind explicitly or expire via TTL. Don't auto-rebind on
matching `app_id` / title.

### Q3 — Block input-buffer events until live screen parsing exists?

**Yes** — that's push-not-pull's deferral discipline.
Without `InputBufferChanged` events from
`InputBufferActor`, input-buffer-gated delivery is
unavailable. The message stays queued. Don't loosen the
gate to be "permissive" while waiting for the events;
the loosening would be a poll (re-check on each focus
event, hope the input buffer is still empty).

The fixture-first test plan in the report works for this:
recorded terminal output drives the gate's
input-buffer predicate before live screen parsing exists.
But live delivery on a real harness waits for live events.

### Q4 — `WaitingUnknown` manually dischargeable only?

**Manual discharge plus TTL expiry.** See Concern §2.
Manual discharge is a CLI command the user runs to clear
the unknown. TTL expiry is the OS-pushed timerfd carve-out
that bounds memory. No retry-on-clock; if neither manual
discharge nor TTL fires, the message stays. That's the
discipline.

### Q5 — `persona-router` as a separate repo before coding?

**Yes**, per `skills/micro-components.md`: routing is a
distinct capability from the message contract. The router's
shape (queue + subscriptions + actors + endpoint dispatch)
is its own domain; persona-message stays the contract crate
and CLI. Separate repos let each evolve under its own
concerns without bleeding internals.

The split also matters for the operator's `primary-jwi`
bead — when the orchestrate helper becomes a typed Persona
component, `persona-router` is the natural neighbor it
talks to.

---

## Recommendations

In priority order:

1. **Add the non-Niri deferral rule.** One paragraph in the
   report explicitly stating: *on systems without the Niri
   IPC socket, focus-gated delivery is unavailable;
   focus-blocked messages stay queued until TTL expiry or
   manual discharge.*
2. **Add TTL specification.** One paragraph: *every pending
   message has a TTL (default 24h, configurable per-actor
   in the harness registry); expiry uses OS-pushed timerfd;
   expired messages move to `Expired` and are released from
   the queue.*
3. **Specify `BindingLost` event.** When a Niri window
   closes, `HarnessActor` emits `BindingLost(target)`. The
   router catches it and either rebinds (if a registry rule
   matches) or moves pending deliveries to expire-only state.
4. **Define "input buffer empty" precisely.** Two predicates:
   *(a) input buffer present?* and *(b) contains only prompt
   chrome with no user characters?* Both true → empty.
   Otherwise → not empty / unknown. Per-harness recognizer
   in a closed `Harness` enum.
5. **Collapse `HarnessActor` methods to one entry point.**
   `AttemptDelivery(message) -> Decision`.
6. **Make subscription multiplicity explicit.** One sentence:
   *one Niri IPC subscription is held while any focus-blocked
   delivery is pending; the subscription closes when the
   focus-blocked queue empties.*
7. **Cross-reference report 12.** One sentence positioning
   the Niri gate as the first slice of the broader
   push-primitive surface.

(1)–(4) are the substantive design refinements. (5)–(7) are
documentation tightening. All seven fit in a single edit
pass on the operator's report.

---

## Observation on the supersession

This audit replaces the prior gate audit (deleted in the
hygiene pass that landed this report). The substance of
the prior audit is now absorbed: every prior concern is
either resolved in the operator's update history (typed
enums, harness-kind enum, sunset rule, polling carve-out
named, event-driven retry) or restated here in terms of
the Niri-specific design. Report 12 (`no-polling-delivery-design`)
remains the broader-surface reference. Report 4
(`persona-messaging-design`) remains the destination
architecture.

---

## See also

- `~/primary/reports/operator/7-minimal-niri-input-gate.md`
  — the audit target.
- `~/primary/reports/designer/12-no-polling-delivery-design.md`
  — the broader push-primitive surface; this report's Niri
  slice is one cut of that surface.
- `~/primary/reports/designer/4-persona-messaging-design.md`
  — the destination architecture; the router is a stepping
  stone toward the persona reducer.
- `~/primary/ESSENCE.md` §"Polling is forbidden" — the rule
  the design observes throughout.
- `~/primary/skills/push-not-pull.md` — the practical skill.
- `~/primary/skills/micro-components.md` — the rule that
  motivates the `persona-router` repo split.

---

*End report.*
