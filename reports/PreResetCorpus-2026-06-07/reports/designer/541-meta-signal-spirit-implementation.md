---
title: 541 — meta-signal-spirit owner-config contract + daemon meta-listener
role: designer
variant: Decision
date: 2026-06-06
topics: [spirit, meta-signal, component-triad, configure, archive-target, multi-listener, owner-only, wire-contract]
description: |
  Implemented the meta-signal-spirit owner-only CONFIGURATION contract (psyche
  oszy): a wire-only (Configure ArchiveTarget) operation routed over an
  owner-only meta socket, with the daemon migrated to MultiListenerDaemon.
  Built + verified end-to-end on branch designer-meta-signal-2026-06-06. Two
  design calls surfaced for the psyche; one emitter follow-up for schema-rust-next.
---

# 541 — meta-signal-spirit implementation

## What landed (branch `designer-meta-signal-2026-06-06`, off spirit main `bc28feb`)

The owner-policy leg of Spirit's component triad — the first of the three
standing production blockers — implemented end-to-end:

- **The contract** (`schema/meta-signal.schema`, wire-only, crate-local fourth
  module per intent `pb1g`): `[Configure]` Input root → `ConfigureRequest {
  ArchiveTarget }`; `[Configured Rejected]` Output roots → `ConfigureReceipt {
  ArchiveTarget DatabaseMarker }` / `ConfigureRejection { ConfigureRejectionReason
  DatabaseMarker }` with `ConfigureRejectionReason [ArchiveTargetUnwritable
  InternalError]`. `DatabaseMarker` is cross-imported crate-locally from
  `spirit:signal`. Generated `WireContract` into `src/schema/meta_signal.rs` —
  no Nexus/SEMA/engine traits (verified).
- **The daemon**: migrated `SingleListenerDaemon` → `MultiListenerDaemon` with a
  `SpiritListener { Working, Meta }` tag. `Daemon::run` binds the working socket
  always and the **previously-unwired** `config.meta_socket_path` *only when
  set*, at filesystem mode **`0o600`** — that is the owner-only gate
  (triad-runtime has no peer-credential check; owner-only == socket perms).
  `handle_meta_stream` decodes `Configure` and applies it via `Engine::configure`
  → `Nexus::set_archive_target` → `Store::set_archive_target`, which re-opens the
  sema-engine database at the new archive target.

## Verified (three adversarial dimensions, all clean)

- **Build/test reality:** `cargo build`/`test`(72)/`clippy -D` all green from a
  forced clean rebuild; the `build.rs write_or_check` freshness guard passes
  (committed `meta_signal.rs` matches fresh generation).
- **Wire-only + triad discipline:** the contract carries no engine planes; the
  data ops (Record/Observe/Remove/…) stay in `signal.schema` unchanged; rust-
  discipline clean (no free fns, no ZST, typed `thiserror` errors).
- **End-to-end (the decisive one):** a live test spawns the real `Daemon::run`,
  binds both sockets, sends `Configure` over the **meta** socket, asserts the
  `Configured` receipt, then writes a `Record` over the **working** socket and
  observes it back at the *new* database file — proving the durable effect, not
  a no-op ack. Plus negative isolation (working socket rejects a meta frame) and
  back-compat (no meta socket binds when `meta_socket_path` is None).

## Two design calls for the psyche

1. **Archive semantics = REDIRECT (not migrate).** `set_archive_target`
   re-points *future* writes/reads to the new `.sema` database; records already
   in the *previous* file are **left in place** — neither copied forward nor
   deleted. This was the implementation's flagged open question. Is redirect the
   intended meaning of "where to put archives," or do you want **migrate-forward**
   (move/copy existing records to the new target)?
2. **`Configure` is deliberately extensible but currently archive-only.** `oszy`
   named only the archive target, so `RetentionPolicy` and other daemon policy
   were left out — the `Configure` root stays a non-breaking `Optional` wire
   addition for later. Confirm archive-target-only is the right initial scope, or
   name the other config you want in.

## One emitter follow-up (schema-rust-next)

The meta contract needed a **hand-written frame codec** (`src/meta_transport.rs`)
because the `WireContract` target emits the per-root `short_header` constants but
**not** `encode/decode_signal_frame` — `gb95` gated signal-frame to
`emits_signal()` targets, and `WireContract` is false. But a wire contract
transported over a socket *needs* framing. Two consequences:
- This **retroactively justifies keeping `short_header` in `WireContract`**
  (audit 539 finding #4 asked whether it was orphaned — it isn't; the meta
  codec consumes it).
- The clean fix is to have `schema-rust-next` **emit the frame codec for
  socket-transported wire contracts** so it's generated, not hand-written. The
  hand-written `meta_transport.rs` is a correct bridge until then.

## Deferred (scoped, flagged — not gaps in this slice)

- No meta CLI client (the daemon-only slice); a future meta CLI mirrors
  `src/bin/spirit.rs`.
- The `validate_owner_socket_mode` guard isn't added (the meta mode is a
  hardcoded `0o600`, nothing to validate until it's config-driven).
- `ListenerPollInterval` left at the 10ms default.

## Handoff

Branch is ready for operator integration onto spirit main (operator owns main).
The two remaining production blockers stand: the Nix-built subscription-streaming
witness, and the `persona-spirit` → schema-derived Spirit cutover proof.

Per psyche 2026-06-06 ("use subagents to implement that" → "configuration … (Configure …)").
