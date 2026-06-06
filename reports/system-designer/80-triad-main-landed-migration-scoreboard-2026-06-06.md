---
title: 80 — triad_main landed on main — migration scoreboard + corrected recipe
role: system-designer
variant: Contextualization
date: 2026-06-06
topics: [triad-main, component-migration, schema-rust-next, daemon, scoreboard, cloud-pilot, message, intent-refresh]
description: |
  Re-orientation after the context break. triad_main (the emitted daemon
  module) LANDED on main across schema-rust-next, triad-runtime, and spirit —
  resolving last session's central uncertainty. My stray codec fix integrated
  cleanly; the divergence is gone. This report is the migration scoreboard per
  ocu7, the corrected per-component recipe (superseding report 77's
  pre-triad_main shape), how my reports 76-79 now stand against the new intent
  records, and the concrete remaining work — chiefly retiring the wrong-shape
  cloud pilot I left on main last session.
---

# 80 — triad_main landed; the migration scoreboard

## What changed while I was away — the central fact

Last session I stopped and asked the psyche two confirmation questions because
I had discovered `triad_main` was implemented + green on the
`designer-daemon-emit-2026-06-06` branches but **not on main**, and I had
created a divergence by pushing a codec fix to schema-rust-next main separately.

**Both are resolved.** The entire triad_main line integrated to main:

- **schema-rust-next main** (`33337d74` land triad_main daemon emitter —
  token-based; then `b75c7f50` deliver disambiguation; `6685e7b3` ConnectionContext
  into `handle_working_input`). My stray codec fix `799f6787` (emit the basic
  frame codec for wire-facing targets incl WireContract) is **in the ancestor
  chain on main** — it integrated cleanly, no divergence remains.
- **triad-runtime main** (`33b9531a` ConnectionContext; + `DaemonConfiguration`
  trait, `ExitReport`, and `BoundedWorkers` — see below).
- **spirit main** (`d406d198` land triad_main pilot — emitted daemon; `bd04eac7`
  thread ConnectionContext). Spirit is now the proven pilot exactly as designed
  in report 542: one-line bin (`SpiritDaemon::run_to_exit_code()`), `src/daemon.rs`
  is **only** the `impl ComponentDaemon for SpiritDaemon` escape hatch
  (209 lines), `src/schema/daemon.rs` is emitted.

So the migration target is live on main and there is a proven exemplar. The
pre-triad_main recipe in report 77 (hand-write the ~190-line daemon shell) is
**superseded** — the corrected recipe is below.

## Intent refresh — the records that reframe my work

| Record | Kind | What it settles |
|---|---|---|
| **ocu7** | Decision | THE migration directive: mind, message, orchestrate, router, terminal-control, spirit (pilot done), persona migrate onto triad_main + the Signal/Nexus/SEMA engine traits. triad_main audited + obvious flaws fixed as migration proceeds. |
| **lnhj** | Decision | Captures report 542: triad_main! is an EMITTED source-visible `src/schema/daemon.rs`, not a literal macro. Streaming is Option B (emitter generates pub/sub wiring from declared `Schema::streams()`). |
| **g3ax** | Decision | The emitted spine must thread per-connection `ConnectionContext` (SO_PEERCRED via `UnixStream::peer_cred`) into `handle_working_input`, so message/router/persona mint origin tags from peer credentials. The spine had regressed message origin to a constant Owner tag; now fixed (landed on main). |
| **1g8y** | Clarification | **Corrects my report 79**: terminal-control maps to the EXISTING `terminal` repo — migrate `terminal`. There is NO separate terminal-control component to create. |
| **k6w1** | Principle | Daemon connection-concurrency (bounded thread-per-connection worker) belongs in triad-runtime, reused by every daemon. Realized: `triad-runtime/src/workers.rs` `BoundedWorkers`; lojix already consumes it. Resolves last session's serial-single-flight concern. |
| **2alg** | Decision | lojix serves connections concurrently; per-request in-flight state; durable Store is the brief-locked shared point; long nix effects hold no global lock; bounded by a permit cap. |
| **ug6i** | Principle | Contract Rust is ALWAYS regenerated from schema; stale artifacts are a failure; `write_or_check` freshness gate must run fleet-wide. (Captured last session.) |
| **3nqt / 8bea / tdsu** | Correction/Principle | Auto-retry transient errors (529, connection-close, the subagent-no-StructuredOutput hiccup) — main agent AND dispatched work. Directly addresses my workflow-capture failure last session: build retry into the dispatch, never surface a transient blip as terminal. |
| **3pfh** | Decision | spirit archive (meta-signal Configure ArchiveTarget) is redirect-forward-only — re-points future writes/reads; prior records stay put, not migrated forward. |
| **own9** | Correction | The entire at-binder surface is abandoned in nota-next; authored surface is the positional bracket/brace form. |

## The migration scoreboard (ocu7 + report 542)

| Component | State | Detail |
|---|---|---|
| **schema-rust-next** | ✅ emitter landed | token-based daemon emitter on main; codec fix integrated; ConnectionContext hook |
| **triad-runtime** | ✅ shells landed | `BoundedWorkers` (k6w1), `DaemonConfiguration`, `ExitReport`, `ConnectionContext`, listener shells, `Runner::drive` |
| **spirit** | ✅ migrated (pilot) | single-listener; emitted daemon + `impl ComponentDaemon`; one-line bin; streaming Option-B emitted |
| **message** | ✅ migrated | single-listener (`NexusDaemonShape::new(message-daemon, signal)`); peer-cred origin via g3ax. **BUT stateless** — see alom note below |
| **lojix** | ◑ partial | consumes `BoundedWorkers` (k6w1); still hand-written `triad-port/src/daemon.rs` — not yet on the emitted daemon |
| **cloud** | ✗ WRONG SHAPE | still hand-written `src/schema_daemon.rs` + `src/daemon.rs` on main AND origin (`4db0e266`) — my last-session pilot in the pre-triad_main shape. **Retire into emitted multi-listener triad_main** (report 542's named multi-listener pilot) |
| **orchestrate** | ✗ todo | hand-written `src/daemon.rs` |
| **domain-criome** | ✗ todo | hand-written `src/daemon.rs` |
| **router** | ✗ todo | no daemon yet (INTENT only); g3ax names it a peer-cred origin minter |
| **mind** | ✗ todo | no daemon yet (INTENT only) |
| **terminal** (=terminal-control, 1g8y) | ✗ todo | no daemon yet (INTENT only) |
| **persona** | ✗ todo | concept schema only |

## The corrected per-component recipe (supersedes report 77)

What spirit and message actually did — the real, proven recipe:

1. **Declare a `NexusDaemonShape` in `build.rs`** — process name + listener
   tier(s). Single-listener: `NexusDaemonShape::new("x-daemon", WorkingListenerTier::new("signal"))`.
   Multi-listener (cloud): add the meta/owner tier.
2. **Turn on the daemon emitter** — `src/schema/daemon.rs` is generated +
   freshness-checked by the same `write_or_check` gate guarding signal/nexus/sema.
3. **Hand-write only `impl ComponentDaemon`** — the record-1488 escape hatches:
   `type Configuration/Engine/Error`, `PROCESS_NAME`, **required** `build_runtime`
   (open the Store/Engine), `handle_working_input` (one Input → one Output, now
   taking `&ConnectionContext` per g3ax), optional owner/meta hatch + stream
   filter/event policy.
4. **Bin is a one-liner** — `XDaemon::run_to_exit_code()`.
5. **Delete** the hand-written `DaemonCommand`/`Daemon`/`*DaemonRuntime`/generic
   `DaemonError`/hand-rolled SubscriptionHub — all emitted now.

The whole report-77 gap table about hand-writing the daemon shell is obsolete;
the only real per-component decision is single-vs-multi listener and what
`build_runtime` opens.

## How my reports 76-79 stand now

- **76 (message↔router overlap)** — holds. message is the SO_PEERCRED trust
  boundary; g3ax confirms it operationally (peer-cred origin minting threaded
  through the emitted spine). Keep separate. ✓
- **77 (port recipe + per-component plans)** — recipe section **superseded** by
  the corrected recipe above. The per-component roadmap (which components, in
  what order) remains useful but should read against the scoreboard.
- **78 (terminal raw-data-plane carve-out)** — dissolved (already banner'd);
  terminal-cell is a library/binary, not a daemon.
- **79 (terminal-layer decomposition → terminal-control)** — **refined by
  1g8y**: the decomposition stands, but terminal-control is the EXISTING
  `terminal` repo, not a new component. No new repo to create.

## Concrete remaining work (mine to surface, not yet to charge into)

1. **Retire the wrong-shape cloud pilot** — cloud is the one place my last-session
   work sits in the wrong shape on main + origin. Per report 542 cloud is the
   multi-listener pilot: declare a multi-tier `NexusDaemonShape`, turn on the
   emitter, reduce `schema_daemon.rs` to `impl ComponentDaemon`, delete the
   hand-written `CloudRuntime`/`ListenerRole`/`serve_*`. This proves multi-listener
   emission the way spirit proved single.
2. **alom existence-log is NOT built** — message migrated **stateless**
   (`schema/sema.schema` = `NoDurableState`/`Stateless`). The existence-log
   (Option A) the psyche chose is still unbuilt; message currently records no
   durable existence facts. This needs a deliberate sema-plane design on the new
   emitted shape, not the pre-triad_main shape I last sketched.
3. **Fleet-wide regen + freshness gate (ug6i)** — assert the `write_or_check`
   gate runs in every component's build so stale artifacts can't persist.
4. **Remaining ports (ocu7)** — orchestrate, domain-criome, lojix (finish onto
   emitted daemon), router, mind, terminal, persona.

## Lane note

ocu7's ports land on main in code repos, which per 6xzu is operator-owned;
spirit + message were already migrated on main (operator work). The cloud
retirement is the natural designer pilot (542 names it), proving multi-listener
emission. I'll confirm split-of-labor with the psyche before touching main.
