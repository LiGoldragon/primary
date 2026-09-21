# Flow and Message rollout and rollback gate — ouranos

**Status, 2026-09-21:** plan only. No service restart, store migration, binary
switch, or remote Nix build has occurred. Field `6db4fe` owns lifecycle and
activation sequencing; Field `9ddcbc` owns the scoped CriomOS-home consumer
preparation under Orchestrate lock `3776`. Mind Medium `2c61af` leads the
contract; retained `f72ab7`, contacted through `0ab019`, is the sole Flow
store, signal-flow, and Message candidate writer. The protected `553901`
locks `1834` and `1835` remain intact.

## Current host and source boundary

The installed `flow-nexus.service` runs `/home/li/.local/bin/flow-nexus` and
uses `/run/user/1001/flow/{flow.sock,flow-meta.sock}` with durable
`/home/li/.local/state/flow/flow.sema`. The installed
`message-daemon.service` runs `/home/li/.local/bin/message-nexus` with the
binary configuration `/home/li/.local/state/message/message-daemon.signal`,
ordinary/owner sockets under `/run/user/1001/message/`, and a Message store.
These are manually installed user units. Their installed binaries have not
been proved equal to the candidate source revisions. The declarative Home
Message pin currently names `fe0d04561051da85292a058ab156e286b7494aa4`
and its unit selects `message-daemon` by default; that is not current runtime
parity. Flow has no active declarative consumer pin. The scoped preparation
on CriomOS-home branch `field/flow-message-consumers-9ddcbc` at `e1096a16`
adds a disabled Flow module and an explicit Message binary selector without
changing either running unit. Home flake pin and check registration remain
unreserved and unedited.

Ouranos configures only `ssh-ng://nix-ssh@prometheus.goldragon.criome` as a
remote Nix builder. On this date DNS and the Yggdrasil route resolved, while
bounded SSH to port 22 and `nix store ping` timed out. Field `6db4fe` has the
peer-side physical/network recovery coordination. A local build is not an
accepted substitute for the remote build gate.

## Store ownership gate before a switch

The current Root decision prefers the existing redb ownership mechanism if
behavioral tests prove exclusive ownership of the same physical store across
processes, aliases, and raw Sema openers. The required property is exclusive
ownership **before any initialization or mutation**, lasting for the entire
engine lifetime. Contention must surface a typed failure such as
`StoreError::StoreAlreadyOpen`; all other lock, I/O, or unsupported-alias
errors fail closed. A separate sibling lock file is a **conditional fallback**
only if the existing mechanism does not satisfy that property. If adopted,
acquire it before `Engine::open`, retain it until after engine drop, and never
unlink or replace it. An application-only guard does not cover a legacy daemon
or raw Sema opener that bypasses it.

Before taking a state copy or starting migration, Field must stop admission,
quiesce both old services in the agreed one-at-a-time order, and witness no
remaining process, open file descriptor, or other writer against the exact
store identities and their physical aliases. The check must account for the
legacy/raw-Sema bypass; a candidate application guard contention test alone
cannot prove old-writer absence. Record process identity, open-file observations,
socket state, service stop result, and a quiescent store checkpoint. Preserve
the store files and inode identities, any fallback sibling lock files,
unit/config bytes, binary store paths and hashes, and typed schema/migration
versions. No
snapshot is called consistent while a writer can still mutate either store.

Luna's exact source trace is `sema-engine 516f01fe` → `sema 51d7927` →
`redb 4.3.0`. Redb's default `ExclusiveWriter` indicates refusal of a second
open on the same physical database, including in one process. This is source
evidence, not an executed behavioral receipt. Root and `f72ab7` decide
whether a fallback guard is needed after the two-opener proof. `commit_atomic`
holds a write lock over one preflight and Sema write; it does not add an
expected-value CAS for a hypothetical multiprocess future.

## Build and acceptance gates

1. Pin immutable, remote-verified Flow, Message, signal-flow, signal-message,
   and other required wire revisions as one coherent dependency set. Reserve
   the exact Home flake and check-registration files separately. Build the
   pair and checks on the configured remote Nix builder only. Match installed
   binary hashes and runtime configuration to those outputs before activation.
2. Run remote Nix behavioral tests against the existing backend first:
   same-process and two-process second opens; physical path aliases; raw Sema
   opener against the same database; reopen after drop and process termination;
   crash recovery; persisted gate/permit and ambiguous hold. Confirm that
   exclusive ownership begins before initialization or mutation and ends
   only after engine drop. If these tests show a gap, choose a fallback with
   Root and `f72ab7`, then test its own contention, engine-open-failure drop,
   unsupported aliases, persistent lockfile, and no-deletion race separately.
   Rustfmt and source review are not compile or behavior receipts.
3. Verify a typed migration version and a reversible or forward-compatible
   store path from each quiescent checkpoint. Demonstrate rollback with
   queued entries and ambiguous attempts written **after** that checkpoint.
   Restoring only the old snapshot would discard those events and is forbidden.
   If the old binary cannot read the new schema and no lossless reverse
   migration exists, rollback to that binary is blocked; retain the new
   state and use a forward repair instead.
4. Switch one service at a time under Field `6db4fe`, retaining the untouched
   other service and a recorded stop point. Verify sockets, process identity,
   binary/source parity, store guard ownership, and typed health before moving
   to the next service. Keep unrelated checkup wake disabled.
5. Use exactly one disposable recipient. Prove Flow admission/permit acquire,
   Message transport submission and actual target-side delivery, then Flow
   permit release **only after confirmed transport**. Retain ambiguous
   attempts with exact attempt and binding across restart; never auto-replay
   or release them by deadline. Test busy, stale binding, restart, and crash
   between transport confirmation and Flow release. Refresh gates new
   admissions atomically: an attempt acquired before `begin_refresh` may
   finish; later acquire refuses, and release does not reopen the gate.
6. Prove a fresh Flow launch and respawn separately from delivery: native
   expanded skill and context receipts, accepted model/effort profile,
   Flow/native identity, exact route, target-side readiness, and independent
   successor acceptance. A failed launch keeps the queue held and does not
   reopen or reroute the predecessor. After accepted successor readiness,
   each queued message chooses one new binding, never a mixed/broadcast set.

The deployed result is accepted only after all gates have witnessed receipts.
Missing builder connectivity, schema compatibility, no-bypass proof, or
single-recipient target delivery keeps the current services in place.
