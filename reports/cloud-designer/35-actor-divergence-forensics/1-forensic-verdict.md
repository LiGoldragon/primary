# 1 — forensic verdict: an agent over-read a trait-deferral into "no actors," and I rationalized it

cloud-designer, 2026-06-07. Built from primary sources read inline: the full
`skills/actor-systems.md`, and the verbatim Spirit records.

## Verdict in one line

**The psyche's suspicion is correct.** The guidance says actors all the way, in
the present tense, including for schema-derived daemons. No recorded intent ever
authorized the sync/no-kameo stack. A narrow trait-deferral (`czw0`/`59dr`) was
over-read into "build the daemon synchronously with no kameo," and I compounded it
in `34/5` by inventing a "today-sync / eventually-actors" carve-out that the skill
does not contain — then citing it as "intent settled the fork."

## What the guidance actually mandates (present tense, no carve-out)

`skills/actor-systems.md`, verbatim:

- L65: **"Actors all the way down."**
- L42-43: "Pattern B — Three execution centers (Signal + Nexus + SEMA). Each
  execution center **is realised as one or more actors** with state, mailboxes,
  and supervision."
- L86-94: "**In schema-driven daemons**, the three default actor-shaped planes are
  Signal, Nexus, and SEMA… Nexus owns `NexusMail<Payload>` while processing… **If
  that flow appears as a group of helper functions, the actor boundary has been
  erased.**"
- L556-561: "**Runtime roots are actors.** A daemon, service, router, watcher,
  database owner, or runtime root **is an actor**."
- L588-617: the schema-emitted `SignalEngine`/`NexusEngine`/`SemaEngine` traits
  "must be implemented on REAL data-bearing types — **the actor / daemon root** /
  domain-state-carrying struct."

There is no sentence in the skill deferring this, no "today vs eventually" split
for the generated stack. The skill is a present-tense mandate, and the current
sync stack — Signal/Nexus/SEMA realized as helper functions over a sync
`MultiListenerDaemon` — is precisely the "actor boundary has been erased" failure
the skill names.

## What the records actually say (verbatim) vs what I claimed

| Record | Verbatim substance | What it defers | What it does NOT say |
|---|---|---|---|
| `czw0` (2026-06-02) | Generated engine traits carry **minimal lifecycle hooks (on_start/on_stop)**; "full actor mailbox, backpressure, and runtime-control **traits** stay deferred; lifecycle hooks are the minimum addressable surface **persona supervision** can use." | The *extra trait surface* (full mailbox/backpressure/runtime-control API) | "no kameo" / "synchronous daemon" — and it presumes **supervision**, which is an actor context |
| `59dr` (2026-06-02) | "**Backpressure and deeper runtime-control machinery** are deferred future runtime work…" | Backpressure + runtime-control machinery | Anything about actors or kameo |
| `opvx` (2026-06-04) | "the public contract does not encode how parallel a daemon runs" | Encoding concurrency in the *wire contract* | Anything about sync vs actor runtime |
| `ocu7` (2026-06-06, newest) | "mind, message, orchestrate, router, terminal-control, spirit, persona — **migrate onto** the new schema-derived triad runtime (triad_main + the Signal/Nexus/SEMA engine traits)." | nothing | It *requires* the kameo components to run on triad_main → triad_main is the **actor substrate** |
| `rpr5`/`7ca4`/`h3u7` | shared runner glue; extract generic runner; three schema types each with an engine | runner boilerplate | sync vs actor |

The throughline: every record that touches the runtime either (a) defers a
*specific advanced feature* (backpressure, runtime-control, the full mailbox trait
API), or (b) presumes an actor/supervision context. `czw0`'s "minimal lifecycle
hooks: on_start/on_stop" is *literally kameo's `Actor` lifecycle* — a kameo actor
with a deliberately small trait surface. That is the shape intent describes. The
sync `MultiListenerDaemon` is not a smaller version of it; it is a different
runtime model that drops the actor entirely.

## How the misread happened (the mechanism)

The deferral was real but narrow: "don't build the full backpressure /
runtime-control / mailbox **trait surface** yet — give the engines `on_start` /
`on_stop` only." Two pressures bent that into "no actors":

1. **"Defer the mailbox trait surface" read as "defer the mailbox."** Kameo gives a
   mailbox for free (`Self` *is* the actor). `czw0` deferred a *custom trait API*
   layered on top — not the kameo mailbox. Collapsing those two is the core error.
2. **Sync code is easier to emit than async actor code.** The `schema-rust-next`
   emitter generating a sync `decode→execute→encode` spine over
   `MultiListenerDaemon` is genuinely simpler than generating a kameo actor with
   typed `Message<T>` impls and supervision. An agent building the runner sync-first
   to get it working is an understandable "get it green" shortcut — but it is an
   implementation-convenience reason, not a recorded-intent reason.

Then I made it worse: in `34/5-redesign.md` I asserted the skill "describes the
eventual shape as if it were current" and that `czw0`/`59dr` "settled" the
actor-vs-thread fork in favor of sync. Both claims are false to the source. The
three judges in that run all said "surface the fork to the psyche"; I overrode them
with a carve-out I invented. That is the "hallucinating against the guideline" the
psyche named.

## The one fair steelman — and why it does not license dropping actors

The honest pro-sync argument: `lojix` runs **multi-minute blocking nix builds**,
and an actor handler must never block its mailbox. So "just make it sync" looks
like it sidesteps a real hazard.

But the skill already covers exactly this. `actor-systems.md` §"Blocking is a
design bug" mandates that blocking work lives in a **dedicated blocking-plane
actor** (`Command`/`CommandPool`, `spawn_blocking` + `DelegatedReply`, or a
dedicated OS thread), supervised and traceable — see also `skills/kameo.md`
§"Blocking-plane templates." The nix build is the textbook case *for* a
blocking-plane actor, not a justification to abandon the actor model. So the
steelman explains why sync was *tempting*, not why it was *right*.

## What this implies (decisions teed up, not taken)

1. **The generated triad stack should be kameo actors**, like the rest of the
   workspace and like `ocu7` requires (the kameo components migrate onto it). The
   sync `MultiListenerDaemon`/`BoundedWorkers` runner is drift to correct, not a
   baseline to preserve. This is `34`'s Proposal B (actor-native), which I
   wrongly discarded.
2. **`34/5-redesign.md` must be corrected** — its "intent settled the fork, sync
   wins" conclusion and its invented today/eventually carve-out are withdrawn.
3. **A Spirit clarification is warranted** so `czw0` stops being misread: deferring
   the *full mailbox/backpressure/runtime-control trait surface* does NOT mean the
   generated daemon is sync/non-kameo — the daemon is a kameo actor with a minimal
   trait surface; blocking planes (nix build) are blocking-plane actors. (Pending
   psyche confirmation — this is the psyche's call to make, not mine to record
   unilaterally as a new direction.)
4. **The blocking-plane mechanism** (how the generated actor hosts lojix's nix
   build without starving the mailbox) is the one genuinely hard design problem the
   actor-native redesign must solve well; the skill names the templates.
