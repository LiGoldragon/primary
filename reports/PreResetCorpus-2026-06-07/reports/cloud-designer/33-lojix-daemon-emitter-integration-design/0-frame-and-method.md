# 33 — design: integrate lojix's daemon needs into the core-crate emitter

cloud-designer lane, 2026-06-06. Psyche decision (from report 32's three forks):
*"let's design a change that integrates lojix's needs with the core crate."*
Plus: owner-auth **rejects on uid mismatch** (fail-closed). Captured as Spirit
`tj99` (emitter-integration direction) and `9v7h` (fail-closed owner auth).

This supersedes report 32's "defer the daemon adoption / just file a
requirement" option. The psyche chose to actively design the emitter evolution
so the GENERATED daemon hosts lojix's load-bearing properties — then lojix (and
cloud, the second per-request-engine daemon) adopt the generated daemon instead
of maintaining hand-written forks.

## What the generated daemon must host (the requirements, from report 32)

The emitted daemon (`schema-rust-next` `daemon_emit.rs` → `src/schema/daemon.rs`,
consuming `triad-runtime`) today is serial and single-tier-typed. To host lojix
it must grow four properties, each one a property lojix's hand-written
`daemon.rs` already has and proved at M1:

1. **Concurrency** — offload each request onto `triad_runtime::BoundedWorkers`
   with a fresh per-request engine over a shared `Arc<Store>`, so a multi-minute
   `nix` build never blocks the accept loop or the other socket (the M1 "~4 ms
   query during a deploy" win; intents `2alg`/`k6w1`).
2. **Two typed wire contracts into one Nexus root** — the owner/meta tier is a
   first-class typed engine path (`nexus::SignalInput::MetaInput`), not the
   current raw `handle_meta_stream` escape hatch.
3. **Transport hardening** — the generated `WorkingTransport` carries the
   per-request max-frame (audit R1, 8 MiB) and read-timeout (audit R2, 10 s)
   bounds.
4. **Fail-closed owner auth** — `ConnectionContext` (`SO_PEERCRED`) on the owner
   socket; on a uid mismatch the connection is **rejected** (intent `9v7h`).

## Method

A design workflow grounds the proposal in the actual source, drafts it, then
stress-tests it against every consumer:

- **Ground** (parallel deep-reads, written as `1`-`3`):
  - `1-emitter-internals.md` — `schema-rust-next/daemon_emit.rs` in full: the
    `ComponentDaemon` trait, `GeneratedDaemonRuntime` spine, `DaemonBinder`,
    `WorkingTransport`, the `NexusDaemonShape` schema declaration + the `build.rs`
    switch, the meta escape hatch, option-B streaming — with exact signatures
    and the precise extension points a change would touch.
  - `2-runtime-seams.md` — `triad-runtime`: `MultiListenerDaemon::serve_streams`
    (the serial call site), the `MultiListenerRuntime` trait, `BoundedWorkers`,
    `ConnectionContext`, the `DaemonConfiguration` trait — where concurrency,
    peer-creds, and bounds slot in, and what is generic vs component-specific.
  - `3-consumer-impact.md` — every emitter consumer the change must not break:
    `cloud` (the 2nd per-request-engine daemon), `message` (Kameo actor, needs
    `&mut self` + its own concurrency), `spirit`, `repository-ledger` if present.
    What each requires the design to preserve.
- **Design draft** — one agent drafts the integrated proposal from the ground
  facts (`4-design-draft.md`).
- **Adversarial review** (parallel, written as `5`) — independent critics on
  distinct lenses: (a) does it actually host all four lojix properties without
  regression; (b) does it break or awkwardly constrain the other consumers; (c)
  is the new schema surface coherent with NOTA/positional + the
  emitter's token-based discipline.
- **Synthesis** — the orchestrator authors the final design (`6-design.md`, the
  highest-numbered file): the concrete schema-declaration extension, the emitter
  change, the triad-runtime change, what lojix's `daemon.rs` collapses to, the
  cloud adoption, and a staged migration plan.

The design is a proposal for psyche review BEFORE implementation — this turn ends
at a reviewable design, not landed emitter code.
