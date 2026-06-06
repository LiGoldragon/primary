# 330 - Router Meta Policy Socket And Production Readiness

Date: 2026-06-06
Role: operator

## Summary

This operator slice carried the component migration forward after the
message daemon migration. It did not complete the full schema-generated
router daemon cutover, but it did fix the concrete two-socket blocker for
router: the daemon now has a working signal socket and a separate
meta-policy socket, and the meta socket drives real router state
mutations through typed nouns.

The work landed across three router-surface repos:

- `meta-signal-router` `2649b4c` - refreshed the wire contract against the
  current generator and added signal-frame round-trip witnesses.
- `signal-router` `8ea7a10` - made the ordinary router daemon
  configuration carry the required meta socket path and mode.
- `router` `63b13e8` then `00e7ee4` - bound the meta socket, decoded
  `meta-signal-router` frames with `triad-runtime`'s length-prefixed
  codec, and routed `Grant`, `Extend`, `Revoke`, and `Deny` into real
  router behavior.

## What Changed

`meta-signal-router` is now a real current wire contract surface. Its
generated schema file carries the short-header frame helpers expected by
the daemon side, and tests prove every `Input` and `Output` operation
round-trips through the contract-local signal frame.

`signal-router` now describes the two daemon sockets in typed
configuration: `router_socket_path` / `router_socket_mode` for ordinary
work and `meta_router_socket_path` / `meta_router_socket_mode` for
policy control. The docs were moved from stale `owner-signal-router`
language to `meta-signal-router`.

`router` now has:

- `RouterDaemon::bind_meta_listener`, `RouterMetaConnection`, and a
  `RouterMetaServer` loop for the meta socket.
- `ApplyMetaRouterPolicy` as the typed actor command entering the router
  runtime from the meta socket.
- `Grant` mapped to `GrantChannel`.
- `Extend` mapped to a new `ExtendChannel` operation that updates memory
  and `RouterTables`.
- `Revoke` mapped to a new `RetractChannelByIdentifier` operation that
  tombstones memory and `RouterTables`.
- `Deny` mapped through a unified adjudication-denial helper that clears
  `RouterRoot.pending`, the `MindAdjudicationOutbox`, the
  `ChannelAuthority` adjudication queue, and the durable
  `adjudication_pending` table row.

The router docs and intent file now call the durable store `router.sema`
instead of `router.redb`. The implementation still uses the existing
`sema` kernel through `RouterTables`; the file-extension rename is the
intent-facing correction, not a full sema-engine rewrite of router.

## Sidecar Findings And Fixes

I dispatched one read-only verifier on the uncommitted router diff. It
found two real blockers after the first router commit had already been
pushed, so I fixed forward with commit `00e7ee4`.

Finding 1: one bad meta connection killed the whole meta listener. The
original `RouterMetaServer::run` propagated `handle_stream` errors with
`?`, so a working-signal frame sent to the meta socket would terminate
the meta server thread. Fix: per-connection errors are logged and the
listener loop continues. Witness:
`meta_server_survives_bad_connection_before_valid_grant` starts the real
meta server, sends a wrong working frame, then sends a valid meta
`Grant` through the same listener and requires `ChannelGranted`.

Finding 2: meta `Deny` only removed `RouterRoot.pending`; it did not
clear channel-authority adjudication state or the durable table row. Fix:
the denial path now asks the owning nouns to clear their state:
`MindAdjudicationOutbox` handles `ClearMindAdjudication`,
`ChannelAuthority` handles `ClearAdjudicationRequest`, and
`RouterTables::remove_adjudication` removes the persisted row. Witness:
`meta_deny_clears_pending_adjudication_from_runtime_and_tables`.

## Verification

`meta-signal-router`:

- `META_SIGNAL_ROUTER_UPDATE_SCHEMA_ARTIFACTS=1 cargo check`
- `cargo check --all-features`
- `cargo test` - 5 tests passed
- `cargo clippy --all-targets --all-features -- -D warnings`

`signal-router`:

- `cargo fmt --all`
- `cargo test`
- `cargo clippy --all-targets --all-features -- -D warnings`

`router` after the sidecar fixes:

- `cargo fmt --all`
- `cargo test` - 45 tests passed plus doc-tests
- `cargo clippy --all-targets --all-features -- -D warnings`
- `git diff --check`

The new router witnesses include:

- meta socket mode binding
- meta socket accepts `meta-signal-router` frames
- meta socket rejects working `signal-message` frames at the codec level
- real meta server survives a bad connection before a valid grant
- meta Grant becomes visible through ordinary `signal-router`
  observation
- meta Revoke disables a channel visible through ordinary observation
- meta Extend updates the durable channel lifetime
- meta Deny clears runtime and durable adjudication state

## Production Readiness State

The two-socket router blocker is fixed for this component slice. A
triad daemon can now have an ordinary working socket and a separate meta
policy socket without putting meta commands on the working signal
surface.

The router behavior is still partly handwritten. It is now a better
behavioral target for the generated daemon path, not the final generated
router cutover. The full production migration still needs:

- router's ordinary signal surface to leave legacy `signal_core` and
  become a schema-emitted `WireContract`;
- router's daemon loop to migrate to the generated `triad_main` spine,
  not the current hand-written daemon loop;
- router's internal Nexus and SEMA operations to be expressed in plane
  schemas so the feature surface is visible in `schema/nexus.schema` and
  `schema/sema.schema`;
- the broader SEMA modernization to continue replacing repo-local
  storage vocabulary with schema/engine-owned storage nouns;
- process-level end-to-end tests that run the long-lived daemon with
  both sockets, not only connection-pair and actor/runtime witnesses.

## Operator Read

The important architectural correction from this slice is that
meta-policy is not a CLI flag or an ordinary working message. It is a
separate Signal door with its own contract, socket, frame decoder, and
typed runtime command. The router now enforces that separation in code:
working signal frames do not decode on the meta socket, and meta
channel-policy operations mutate router state through typed actor
messages.

This does not remove the need for generated schema planes. It makes the
expected generated shape concrete: when router is fully migrated, the
same operations should appear in the router Nexus schema as internal
verbs and objects, and the generated daemon should reproduce the
two-socket behavior without reintroducing handwritten listener glue.
