# Persona-orchestrate: don't create the component

*Research into whether `tools/orchestrate` should be reshaped as a
`persona-orchestrate` daemon with its own `signal-persona-orchestrate`
contract. The evidence says no — the verbs already live in
`signal-persona-mind`, and `persona-mind` is explicitly the
central-state daemon that owns them. The shortest path is straight
mind-CLI absorption, not a new component.*

Date: 2026-05-17

Author: second-designer-assistant

---

## TL;DR

`signal-persona-mind` already defines the typed orchestrate verbs:
`RoleClaim`, `RoleRelease`, `RoleHandoff`, `RoleObservation`,
`ActivitySubmission`. They appear at
`signal-persona-mind/src/lib.rs:418, 450, 466, 543, 580` as record
types, and at lines 1756-1760 they are wired into the channel macro
as `Assert RoleClaim`, `Retract RoleRelease`, `Mutate RoleHandoff`,
`Match RoleObservation`, `Assert ActivitySubmission`. The
`persona-mind` daemon already parses these requests (see
`persona-mind/src/text.rs:242, 264, 757-782`).

`persona-mind`'s ARCHITECTURE.md describes the daemon as "**Central
Kameo actor system for Persona coordination, work memory, and the
command-line mind**" — coordination is one of the three slices the
daemon was designed to carry, not a candidate for splitting out.

Creating `persona-orchestrate` + `signal-persona-orchestrate` would
fragment one semantically unified slice (role claims, activity, work
graph, ready/blocked queries) across two daemons, violating the
"central workspace state" principle the workspace already committed
to.

**Recommendation:** no `persona-orchestrate` component. The Rust
rewrite design in report 2 needs revision — the bridge is shorter
than it framed.

---

## Evidence

### 1. `signal-persona-mind` already owns the orchestrate verbs

```
$ grep -n 'RoleClaim\|RoleRelease\|RoleHandoff\|RoleObservation\|ActivitySubmission' \
    /git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs

418:pub struct RoleClaim {
450:pub struct RoleRelease {
466:pub struct RoleHandoff {
543:pub struct RoleObservation;
580:pub struct ActivitySubmission {
…
1756:            Assert RoleClaim(RoleClaim),
1757:            Retract RoleRelease(RoleRelease),
1758:            Mutate RoleHandoff(RoleHandoff),
1759:            Match RoleObservation(RoleObservation),
1760:            Assert ActivitySubmission(ActivitySubmission),
```

The signal_channel! macro at lines 1756-1760 wires each role-shaped
record into the daemon's request/reply protocol using the
`signal-core` verb prefix (`Assert`, `Retract`, `Mutate`, `Match`).
Reply records (`ClaimAcceptance`, `ClaimRejection`,
`ReleaseAcknowledgment`, `HandoffAcceptance`, `HandoffRejection`,
`RoleSnapshot` containing `ClaimEntry` + recent activity) follow the
same pattern in the same file.

### 2. `persona-mind` daemon already implements request parsing

```
$ grep -n 'RoleClaim\|RoleRelease' \
    /git/github.com/LiGoldragon/persona-mind/src/text.rs

242:pub struct RoleClaim {
248:impl RoleClaim {
255:        Ok(contract::MindRequest::RoleClaim(contract::RoleClaim {
264:pub struct RoleRelease {
268:impl RoleRelease {
270:        contract::MindRequest::RoleRelease(contract::RoleRelease {
757:    RoleClaim(RoleClaim),
758:    RoleRelease(RoleRelease),
781:            Self::RoleClaim(claim) => claim.into_contract(),
782:            Self::RoleRelease(release) => Ok(release.into_contract()),
```

The daemon has NOTA-text → typed-request decoding for the role verbs.
The contract-layer types (`contract::RoleClaim`, etc.) are the
signal-persona-mind records; the text-layer types are the daemon's
parsing surface.

### 3. `persona-mind` is explicitly the central-state daemon

`persona-mind/ARCHITECTURE.md` (cited by the research):

> "**Central Kameo actor system for Persona coordination, work
> memory, and the command-line mind**"
>
> "`persona-mind` owns Persona's central workspace state: role
> claims, handoffs, activity, work items, notes, dependencies,
> decisions, aliases, event history, and ready/blocked views."

`§7` of that ARCHITECTURE.md (cited at line 442) names
"role claim/release/handoff/activity behavior" as
persona-mind's explicit owned scope.

This is not a daemon that's about to split; it's a daemon explicitly
designed to be one place for these three slices.

### 4. The workspace's own destination already names persona-mind

`orchestrate/AGENTS.md` §"Command-line mind target" (the doc this
lane just moved from `protocols/orchestration.md`):

> "The target implementation is the Rust `mind` CLI backed by a
> long-lived `persona-mind` daemon and the `signal-persona-mind`
> contract."
>
> "Lock files are current helper state only. They are not imported,
> read, or projected by `persona-mind`; they retire at the workspace
> cutover boundary."

The workspace already committed to mind-CLI absorption. The research
confirms the destination's plumbing is already in place.

### 5. No `persona-orchestrate` or `signal-persona-orchestrate` repo exists

```
$ ls /git/github.com/LiGoldragon/ | grep -E '^(persona|signal-persona)'

persona, persona-harness, persona-introspect, persona-message,
persona-mind, persona-router, persona-sema, persona-system,
persona-terminal

signal-persona, signal-persona-auth, signal-persona-harness,
signal-persona-introspect, signal-persona-message, signal-persona-mind,
signal-persona-router, signal-persona-system, signal-persona-terminal,
signal-persona-terminal-test
```

Neither `persona-orchestrate` nor `signal-persona-orchestrate` is
present. There is no draft, no signal contract, no skeleton. That
absence is also evidence — if the workspace's structural pattern
called for a separate orchestrate component, it would already have
been drafted by the same hand that drafted `persona-message`,
`persona-router`, etc. It wasn't, because role coordination is
already mind-shaped.

### 6. Cross-component imports confirm the pattern

`persona-router/src/router.rs:27-30` imports
`AdjudicationDeny`, `ChannelDuration`, `ChannelEndpoint`, `ChannelGrant`
from `signal-persona-mind`. The pattern: when component A needs B's
state, A imports B's *signal contract*. Persona-router talks to mind
through signal-persona-mind. If orchestrate had been a separate
component, the same pattern would apply — a hypothetical persona-X
needing to ask "who's claimed this scope?" would import
signal-persona-orchestrate. Instead, every component that touches role
state reaches signal-persona-mind.

---

## Implication for report 2 — the Rust rewrite design

Report 2 of this lane
(`reports/second-designer-assistant/2-orchestrate-rust-rewrite-design-2026-05-17.md`)
framed the Rust rewrite as **the bridge** between today's shell helper
and the eventual mind-CLI absorption. Two specific claims in that
report need revision in light of this research:

### Claim that needs revision

> §"End-state design" calls for a new Rust crate (`orchestrate-cli`)
> with its own typed Nota request/reply vocabulary
> (`(Request (Claim …))`, `(Reply (Claimed …))`, etc.) reading
> `orchestrate/roles.nota`.

**This is now redundant.** The typed request/reply vocabulary
*already exists* in `signal-persona-mind`. The bridge crate would
duplicate the verb shapes that the destination contract already
defines. Three options:

1. **Skip the bridge.** Rewrite `tools/orchestrate` directly as a
   thin client over `persona-mind`'s Unix socket using the existing
   `signal-persona-mind` records. No `orchestrate-cli` crate. No
   `signal-persona-orchestrate` contract. No intermediate vocabulary.
   The interim `orchestrate/roles.list` retires when the rewrite
   lands; lock files retire when `persona-mind` is the canonical
   coordination state.
2. **Keep the bridge crate but reuse signal-persona-mind.** Build
   `orchestrate-cli` as a Rust binary that doesn't define its own
   vocabulary — it imports `signal-persona-mind`, decodes argv into
   `MindRequest::RoleClaim(…)` directly, and (during the
   shell-helper era) writes lock files as a side effect. When
   persona-mind is the canonical store, the lock-file side effect
   drops and the bridge becomes a pure mind client.
3. **Land the shell helper as-is.** Skip the Rust rewrite. The
   shell helper is fine for the remaining shell-helper era;
   investing in a Rust bridge is wasted work if the mind CLI is
   the real destination.

Option 1 is the cleanest. Option 2 hedges. Option 3 saves the work
entirely.

### Claim that's still correct

The rest of report 2 (the existing lock-file format must be
preserved bit-for-bit during the shell-helper era; the role registry
externalisation is a transitional move; the actor-system shape
isn't needed for one-shot CLI; the BEADS bridge stays) all remains
correct under any of the three options above.

### Recommended supersession

Report 2 should be marked as superseded-in-part by this report's
§"Implication." Operator picking up bead `primary-68cb` should read
both reports together. If the user picks option 1 or option 3, I'd
file a follow-up report (4) that restates the rewrite scope; if
option 2, the existing report 2 stays load-bearing with the noted
revision.

---

## Why this matters beyond orchestrate

The pattern this research surfaces is general: **when a verb is about
state the central daemon already owns, don't build a parallel daemon
to "host" the CLI.** Build the CLI as a thin client. The temptation
to create `persona-orchestrate` is the same shape as the temptation
to create `mind-tools` or `mind-cli-bridge` — a wrapper that
duplicates the destination's vocabulary because the wrapper feels
like it needs its own contract.

The workspace's discipline (per `skills/micro-components.md`) is that
each component owns one capability. The capability "coordinate who
is working on what right now" is the same shape as "track work items
and ready/blocked queries" is the same shape as "remember
decisions" — they're all *mind state*. They land on `persona-mind`
because that's the daemon that owns mind state.

---

## Open question for the user

The three options above for the Rust rewrite are real choices. My
weak default is **option 1** — skip the bridge crate, rewrite
`tools/orchestrate` directly as a thin signal-persona-mind client.
Reasons:

- Avoids inventing parallel vocabulary that the destination contract
  already covers.
- Shorter path to the eventual `mind '<NOTA>'` shape — once the
  client is in place, the only remaining change is that `mind` CLI
  becomes the canonical entry point (and `tools/orchestrate` either
  retires or becomes a 5-line wrapper that translates argv → NOTA →
  `mind`).
- Lock-file maintenance moves from "shell parses + writes" to "Rust
  client writes them as side effects of mind requests" — same
  shape, less surface area.

But option 3 is honest about the cost. The shell helper works
today. If the user expects `mind` CLI to land in the near term,
spending Rust-rewrite time on a bridge that retires soon may be the
wrong investment. Operator's appetite + the timing of the
persona-mind cutover are the load-bearing inputs.

I have not edited report 2 or the bead description in light of this
finding — that needs the user's direction first.

---

## See also

- this workspace's `orchestrate/AGENTS.md` §"Command-line mind target"
  — the destination this research confirms.
- this workspace's
  `reports/second-designer-assistant/2-orchestrate-rust-rewrite-design-2026-05-17.md`
  — the design report this research partially supersedes.
- this workspace's
  `reports/second-designer-assistant/1-role-skill-consolidation-survey-2026-05-17.md`
  — the survey that started this arc.
- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs` —
  the existing typed orchestrate vocabulary (lines 418-580, 1756-1760).
- `/git/github.com/LiGoldragon/persona-mind/src/text.rs` — the
  daemon's request parsing for the same vocabulary (lines 242-782).
- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md` — the
  central-state framing that makes orchestrate one of three slices,
  not a candidate for its own component.
- `skills/micro-components.md` — one capability, one crate, one repo
  — the principle that says "central workspace state" doesn't
  fragment.
- BEADS `primary-68cb` — the operator pickup bead for the Rust
  rewrite; needs updating after the user picks option 1 / 2 / 3.
