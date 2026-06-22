# Spirit Real Authorization Trace Status

## Summary

The source-side milestone is implemented and tested: `spirit` observing mode now asks criome for a real authorization answer, waits long enough to see the answer, emits a structured trace event for that authorization-return point, and still does not block fan-out in observing mode. Gating mode remains fail-closed. The socket-only bootstrap path now observes criome's signed `AuthorizationGrant`; unsigned request material is not an approval artifact.

The live `spirit-daemon.service` is not yet using this path. It is still the already-running Nix package from June 21, built without the new commits and without production configuration that arms the criome gate.

## What Landed

- `signal-introspect` `74b020a80d9d` — adds `IntrospectionTarget::Spirit` and `TraceLayer::Authorization`, with a round-trip witness for `Spirit / Authorization / AuthorizationObserved`.
- `signal-introspect` `ba6fba733df2` — manifests the new trace target in `INTENT.md`.
- `spirit` `c5ba07f95d5d` — changes observing mode from fire-and-forget to real criome round-trip; adds `GateDecision::Observed(ObservedAuthorization)` and emits `AuthorizationObserved` trace events.
- `spirit` `122c93694d44` — manifests the observing-mode intent update in `INTENT.md`.
- `signal-criome` `0125e66e` — exposes `AuthorizationGrant` signatures/expiry so consumers and tests can assert the signed approval artifact.
- `criome` `825cc8ac` — AutoApprove over `AuthorizeSignalCall` now mints, stores, and returns a criome-master signed `AuthorizationGrant`.
- `spirit` `d2d5d97e` — owner-configured socket-only gates now submit `AuthorizeSignalCall`, require `AuthorizationGranted`, and trace the signed-return point in observing mode.
- `mentci-egui` `4c16bd33` from the earlier slice — compact header and resizable approval panel.

## Current Flow

```mermaid
sequenceDiagram
    participant Spirit as spirit
    participant Criome as criome
    participant Introspect as introspect
    participant Mentci as mentci

    Spirit->>Spirit: local record lands
    Spirit->>Criome: AuthorizeSignalCall(head digest)
    Criome-->>Spirit: AuthorizationGranted(signed grant)
    Spirit->>Introspect: ComponentTraceEvent(Spirit, Authorization, AuthorizationObserved)
    Spirit->>Spirit: observing mode still ships
    Mentci->>Introspect: query trace pane
```

## Verified

- `signal-introspect`: `cargo test --all-targets --quiet`
- `criome`: `cargo test --test daemon_skeleton`
- `spirit`: `cargo test --features mirror-shipper --test criome_gate_1of1 --quiet`
- `spirit`: `cargo test --features testing-trace --test instrumentation_logging --quiet`
- `spirit`: `cargo test --features nota-text,testing-trace --test process_boundary cli_receives_testing_trace_events_from_daemon_trace_socket --quiet`
- `spirit`: `cargo check --features testing-trace,mirror-shipper --bin spirit-daemon --quiet`

## Live Service Reality

`systemctl --user status spirit-daemon.service` currently shows the production service still running:

```text
/nix/store/5i1233d5i7j2sqdyvq4870xbdjmgji57-spirit/bin/spirit-daemon
/nix/store/yrj3592irzixijzdjiflp1qcdklvl0mp-spirit-daemon-configuration/spirit.config.rkyv
```

That means the source commits above are not deployed yet. Also, the deploy config still needs a real criome gate arming path: the current `SpiritDaemonConfiguration` carries `TraceSocketPath` and `AuthorizationMode`, but not the local criome socket plus attestor material needed to call `Engine::arm_criome_gate` outside tests.

## Next Cut

```mermaid
flowchart TD
    A[Build traced mirrored spirit package] --> B[Extend daemon startup or meta config with criome gate arming]
    B --> C[Home profile writes trace socket and Observing mode]
    C --> D[Restart actual spirit-daemon.service]
    D --> E[Introspect ingests Spirit AuthorizationObserved events]
    E --> F[Mentci shows the running system authorization stream]
```

The next implementation should be the deploy/config cut:

1. Add a production configuration path for the criome gate: local criome socket plus the 1-of-1 attestor material.
2. Add or select a `spirit` package output that builds `spirit-daemon` with both `testing-trace` and `mirror-shipper`.
3. Update the home profile to pass a trace socket, `AuthorizationMode::Observing`, and the criome gate configuration into the actual user service.
4. Start or wire `introspect` so it listens on that trace socket.
5. Point Mentci’s trace pane at the live introspect data for `IntrospectionTarget::Spirit`, `TraceLayer::Authorization`.

## Resolution: Meta Configure

The psyche corrected the open question: criome gate arming is owner policy and belongs on the meta signal, not startup-only binary configuration. This matches existing intent (`cgd8`, `ur16`, `7sx6`): configuration verbs live in the meta-signal contract and bootstrap/runtime config share a `Configure` vocabulary.

Implemented follow-up:

- `meta-signal-spirit` `f31d4cc758ac` extends `ConfigureRequest` / `ConfigureReceipt` with `SelectedCriomeGateTarget`.
- `spirit` wires that target into `Engine::configure`: `Socket(path)` arms the local criome gate, `Default`/`None` clears it.
- The bootstrap target carries only the criome socket. Spirit submits a simple per-head `AuthorizeSignalCall`; criome `AutoApprove` returns the signed `AuthorizationGrant`, and spirit traces that return while still proceeding in observing mode. This is the first production/demo shape. `ClientApproval` for the same signal-call grant-completion path remains the next mentci-facing signing increment; quorum signer/key material remains the later contract shape.
