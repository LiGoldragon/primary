# Persona service observation contract

**Status:** owner decision and anatomy supplement, 2026-09-23. The initial
slice is configuration-driven and read-only. It authorizes no implementation,
reservation, build, activation, restart, or service policy change.

## Decided producer boundary

Use existing `signal-persona` `ethos/signal.ethos` as the ordinary typed
service-observation wire producer. `meta-signal-persona` is reserved for
privileged control only if a later accepted policy needs it; the initial slice
adds no control verbs. `PersonaDaemonConfiguration` remains the binary
configuration producer through the existing service-crate
configuration/schema/build pipeline. No JSON format, ad-hoc configuration, or
parallel controller is introduced.

This is a design decision, not evidence that a consumer, writer, or runtime
already accepts it. Baseline common remote is `9469b0a`; case-distinct candidate
repositories are `Persona` `b6f6ef0a` and `persona`
`09ee526cbde8dd6a9dc54b1b3583e2a034d0e063`. Neither case nor newer revision
selects the canonical producer. Field owner acknowledgement remains pending;
no writer or path is assigned.

## Read-only typed contract

Configuration declares an explicit unit allowlist and system or user-manager
scope, including expected manager identity, user UID/bus identity where needed,
and provider/freshness expectations. A payload cannot name arbitrary units or
turn a wildcard into monitoring authority. No environment, raw `ExecStart`
arguments, or secrets are collected; relevant configured values must be
redacted.

```text
ObserveService{allowlisted_unit, manager_scope}
  → ServiceSnapshot{
      requested_unit,
      observed_active_state, observed_sub_state, result, job,
      process, exec_time_monotonic, boot_identity,
      provider, observed_at, received_at, freshness, provenance
    }
  | Unknown | Inaccessible | Rejected
```

Requested unit and observed service state remain distinct. Application health,
model context, Flow lifecycle, and Message delivery are never inferred from an
active unit. Native D-Bus change subscription is used when the selected manager
supports it: publish an initial snapshot then typed changes. Subscription gap,
manager restart, inaccessible bus, provider mismatch, or lost continuity emits
`Unknown`/discontinuity; it never fabricates freshness or starts a polling loop.
`SystemdStatus.ActiveState` is reused and extended as a read-only interface,
not widened into Start/Stop authority.

## Ownership and integration

The authoritative producer publishes first with version compatibility; a
service-observer consumer then reads it through the existing manager socket and
store. Their schemas and compatibility are owned by their actual source owners
once acknowledged. Persona observes configured service facts and supervised
component status; it does not gain restart rights or become a duplicate
controller. Flow retains native identity/lifecycle, Message retains ordinary
delivery, and Orchestrate retains cooperative file-revision policy rather than
lifecycle transaction authority.

The inspected Persona implementation has binary rkyv configuration with manager
socket/store paths and typed engine/component status, but its manual unit and
direct-process helpers do not establish general systemd observation. CriomOS
currently declares `persona-router`, not a Persona daemon. Thus a later bounded
`services.persona` module may own daemon identity, state/runtime directories and
generated existing configuration only after source ownership and initial
producer work are accepted. It must observe existing managers, never duplicate
their restart ownership.

## Current Codex boundary

Field-attributed report `95a9e91e31a5e7cad0721e6b4f4a736ca5e0353a` records a
safe desktop close: the desktop GUI and its private server stopped, while
managed Codex PID `2087`, its control socket and integrator `347255` remained.
It does not prove why desktop attachment had failed or repair it. The proposed
`CODEX_HOME`/socket layout is uninstalled; no migration or Desktop attachment
fix is claimed before supported backup/migration and attachment/coexistence
proof. Preserve current writers and endpoints.

## First proof and open decisions

The first accepted proof is a disposable, configured allowlist fixture that
shows initial snapshot, a native change where supported, disconnect/manager
restart discontinuity, inaccessible scope, redaction, and no restart side
effect. It is not deployment acceptance. Required decisions still needing an
actual source owner are canonical package/repository, consumer pins, exact
manager adapter paths, and version compatibility. Do not treat this packet as
owner acceptance while those are unresolved.

## Sources

- Field report `flows/6fb948/reports/persona-service-and-codex-boundary-20260923.md`
  at `95a9e91e31a5e7cad0721e6b4f4a736ca5e0353a`: observed desktop/process
  boundary and Persona source limits; no service-observer implementation.
- Current living architecture decision relayed through `4b0f60`: retain
  `signal-persona` ordinary producer and existing binary configuration pipeline;
  source-owner acknowledgement remains pending.
- `flows/4b0f60/reports/flow-anatomy-flashbook-source.md`: component ownership
  anatomy; not a rendered flashbook or runtime receipt.
