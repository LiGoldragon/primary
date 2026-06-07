# 34 — the best daemon shape, designed bottom-up (zero compatibility)

cloud-designer, 2026-06-07. Psyche directive: *"I want the best design… from
the bottom up all the way. I don't want any kind of backward compatibility or
bending over backwards to not offend another component. All components will be
offended… there's no production."* Captured: Spirit `ax2k` (Maximum) + new
AGENTS.md hard override.

This **supersedes report 33's design frame** (`33/6-design.md`), which was built
around opt-in, byte-stable regeneration, and not-disturbing `message`/`spirit` —
exactly the compatibility reflex the psyche rejected. The *ground facts* in
`33/1-3` (emitter internals, runtime seams, consumer shapes) remain valid and are
reused; only the design target changes: **the single best daemon the emitter
should generate, with every component expected to change to fit it.**

## The reframe

Stop asking "how do we add a concurrent option without breaking the serial
daemon." Ask: **what is the one best daemon the schema-derived emitter generates,
such that each component's hand-written code is mostly the real algorithm** (the
ESSENCE readability thesis) — and let `lojix`, `cloud`, `message`, `spirit`,
`repository-ledger` all conform to it. Breaking all five at once is expected and
fine.

## The pivotal fork this redesign must resolve

The schema-derived daemons (`lojix`/`cloud`/`spirit`) are **sync, thread-based**
(`MultiListenerDaemon` + `BoundedWorkers`). But the workspace truth-pin says
*"Actor runtime: direct kameo today. Actor density is required: runtime roots are
actors…"*, and `message` IS a kameo actor daemon. So: **is the one best generated
daemon a thread-per-request system or an actor system?** This is the load-bearing
architectural question; the proposals must each take a clear position and
reconcile with the actor-density intent.

## Method — judge panel (best design wins)

- **Propose** (parallel, written `1`-`3`): three INDEPENDENT best-architecture
  proposals, each from a distinct philosophy, each under a hard zero-compatibility
  mandate (every component changes; non-disruption is never a virtue). Candidate
  philosophies: (1) unified thread-per-request — one generated daemon shape,
  everything (incl. `message`) conforms; (2) actor-native — the generated daemon
  IS a kameo actor system per the actor-density pin; (3) two merit-chosen
  archetypes (request/reply vs streaming) the emitter selects on design merit, not
  compat. Each answers: concurrency model, daemon archetype count, meta/owner tier
  model, the hand-written hook surface, how all five consumers map on, transport +
  auth as always-on, and — honestly — what each component loses.
- **Judge** (parallel): three judges score the proposals strictly against the
  ESSENCE priority order — Clarity > Correctness > Introspection > Beauty — plus
  the readability thesis and the actor-density pin, and each renders a verdict on
  the actor-vs-thread fork.
- **Synthesize** (`5-redesign.md`, highest-numbered): the orchestrator authors the
  best design from the winning proposal, grafting the best ideas from the others,
  and states plainly what every component must change. The actor-vs-thread
  resolution, if intent does not settle it, is surfaced as a crisp psyche question
  — not inferred.

The deliverable is the best design and (if needed) one sharp open question — not
landed code.
