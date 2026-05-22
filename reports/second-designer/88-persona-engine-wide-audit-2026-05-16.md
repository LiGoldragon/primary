# Persona Engine Wide Audit — 2026-05-16

Date: 2026-05-16
Role: designer-assistant

> **Context-maintenance update, later 2026-05-16:** this audit was
> followed by a hands-on coherence pass. Findings 1, 5, and the
> router-facing half of finding 6 are no longer current in the
> working trees:
>
> - `persona-router` now accepts length-prefixed
>   `signal-persona-router::RouterFrame` Match requests on
>   `router.sock` and routes them through `RouterObservationPlane`.
> - `persona-introspect::RouterClient` now sends a live
>   `RouterSummaryQuery` and composes the typed reply into
>   `PrototypeWitness.router_seen`.
> - `persona/scripts/persona-dev-stack` now uses
>   `persona-terminal-signal --control-socket`, and
>   `nix run .#persona-dev-stack-smoke --option substituters '' -L`
>   passed after that fix.
>
> These are local, uncommitted repo edits at this maintenance point.
> Remaining open: `persona-introspect` only has the router peer wired;
> manager and terminal clients are still scaffolds; the dev-stack smoke
> still does not launch or verify `persona-introspect`; stable named
> references for `signal-core` and peer contracts remain incomplete.

## Scope

The user said two designer subagents were still in flight:

- Phase-3 `/199`: typed-configuration sweep
- Phase-3 `/194`: actor/supervision audit

This audit focuses on the rest of today's Persona engine work, while noting
places where those in-flight tracks visibly affect the tree. I inspected the
current active Persona/Sema/Signal stack, today's commit history, current
source, current dirty working trees, and representative witnesses.

## Representative Checks Run

Passed:

- `persona-router`: `cargo test --quiet --test observation_truth`
- `terminal-cell`: `cargo test --quiet --test production_witnesses slow_transcript_append_does_not_block_viewer_output`
- `persona`: `cargo test --quiet --test manager_store constraint_manager_store_rebuilds_snapshots_from_event_log_after_snapshot_truncation`
- `signal-persona-introspect`: `cargo test --quiet --test round_trip introspection_status_enums_are_closed_no_unknown_variants`
- `signal-persona-router`: `cargo test --quiet --test canonical_examples`
- `signal-persona-terminal`: `cargo test --quiet --test canonical_examples`
- `persona-harness`: `cargo test --quiet --test subscription_truth`

Failed:

- `persona`: `nix run .#persona-dev-stack-smoke`

Failure:

```text
persona-router reported unexpected readiness line:
persona-router-daemon socket=/tmp/persona-dev-stack.../router-daemon.nota
```

This is the most important finding in the audit.

## High-Priority Findings

## 1. Full Nix Dev-Stack Is Red Because The Flake Assembles Stale Inputs

The current `persona/scripts/persona-dev-stack` writes a typed
`RouterDaemonConfiguration` file and launches:

```sh
persona-router-daemon "$router_daemon_configuration"
```

Current `persona-router` `main` understands that shape:

- `src/main.rs` checks whether argv[1] is a typed configuration source;
- `RouterDaemon::from_configuration` binds the configured router socket;
- local current `persona-router` HEAD is `a973edd`.

But `persona/flake.lock` still pins `persona-router` to `23a856d`, which is
before `5914022 persona-router: accept typed RouterDaemonConfiguration via
argv`. The locked binary treats the config path as a legacy socket argument
and prints:

```text
persona-router-daemon socket=/tmp/.../router-daemon.nota
```

That exactly matches the failed smoke.

### Stale Persona Flake Inputs

Current `persona/flake.lock` lags local active heads:

| Input | Locked | Current head | Ahead |
| --- | --- | --- | --- |
| `persona-harness` | `202befa` | `44239ed` | 7 |
| `persona-introspect` | `0c031d2` | `1760034` | 8 |
| `persona-message` | `aa474bc` | `8988191` | 1 |
| `persona-mind` | `af19a16` | `3e3465f` | 3 |
| `persona-router` | `23a856d` | `a973edd` | 9 |
| `persona-system` | `21f1fba` | `7e17c7f` | 5 |
| `persona-terminal` | `b5bd009` | `58fe7c0` | 8 |
| `signal-persona` | `b1c42ff` | `6737668` | 4 |
| `signal-persona-mind` | `51ac78b` | `743a406` | 3 |
| `signal-persona-system` | `081698c` | `dae8f07` | 9 |
| `terminal-cell` | `f87d1da` | `5494679` | 9 |

This means component-local tests can be green while the assembled Persona
engine is red. The integration witness is the source of truth for the stack;
right now it is failing.

### Recommendation

Before claiming any full-engine milestone, update the `persona` flake inputs
to compatible component revisions and rerun:

```sh
nix run .#persona-dev-stack-smoke
```

If the typed-config sweep is still in flight, make that sweep own the lock
bump and smoke rerun as its final witness.

## 2. Terminal Plane Split Is Real And Good, But Not Yet Proven Through The Pinned Stack

Today's terminal work is substantial and mostly aligned:

- `terminal-cell` daemon now accepts separate `control.sock` and `data.sock`.
- `TerminalCellSocketClient` models both sockets.
- control-only commands reject raw attach.
- `ViewerFanout` and `TranscriptScriber` replace the old single
  `OutputFanout`.
- A bounded drop-oldest transcript notice queue prevents slow transcript
  append from blocking viewer output.
- `signal-persona-terminal::TerminalSessionObservation` carries typed
  `TerminalControlSocketPath` and `TerminalDataSocketPath`.

The representative slow-transcript witness passed.

Remaining gap:

- `persona/flake.lock` still pins old `terminal-cell` and `persona-terminal`
  inputs, so the full Persona stack is not yet proving this new terminal shape
  through Nix.
- `persona-terminal` registry now records both paths, but production viewer
  adapters consuming the `data_socket_path` remain a later step.

### Recommendation

Treat terminal-cell two-plane separation as locally implemented, but do not
call it full-engine landed until the Persona flake lock is bumped and a
dev-stack or terminal-specific Nix witness proves the pinned stack uses the
split.

## 3. Closed-Sum Contract Sweep Mostly Corrected Earlier Findings

The closed-sum work has progressed since my previous critique:

- `signal-persona-router` removed `RouterDeliveryStatus::Unknown`.
- `signal-persona-introspect` removed `ComponentReadiness::Unknown` and
  `DeliveryTraceStatus::Unknown`, moving "not observed yet" to `Option<>`
  wrappers.
- `signal-persona-system`, `signal-persona-harness`, and
  `signal-persona-mind` now have the request-side retract plus final ack
  subscription lifecycle shape.
- Canonical NOTA example tests landed across several contract crates.

The representative router/terminal/introspect canonical and closed-sum tests
passed.

Remaining caution:

- `UnknownKindForVerb` from `nota-codec` appears in generated decode errors.
  That is not the same as a domain `Unknown` wire status.
- Positive rejection causes such as `UnknownRoleName`, `UnknownTerminal`,
  or `UnknownSigner` are not automatically violations if they mean "the named
  entity is not registered." They should still be reviewed for naming, but
  they are not the open-world placeholder that closed-sum discipline forbids.

### Recommendation

The closed-sum finding from `/200` should be updated: router and introspect
are no longer examples of the old `Unknown` problem. The next contract concern
is stable dependency references, not sentinel statuses.

## 4. Signal-Core Stable Named Reference Is Still Not Done

Every `signal-persona-*` contract crate I checked still depends on
`signal-core` by bare git URL, for example:

```toml
signal-core = { git = "https://github.com/LiGoldragon/signal-core.git" }
```

No stable API branch/bookmark is visible in the local `signal-core` checkout.

This is consistent with the user's decision: `signal-core` is the first good
target for a stable named API reference, but it has not landed yet.

### Recommendation

Once `signal-core` declares its first stable API lane, update contract crates
to a named branch/bookmark/tag. Do not use raw revisions as the standard.

## 5. Router Observation Plane Exists, But Router-Daemon Observation Ingress Does Not

Local `persona-router` has a real `RouterObservationPlane` actor and the
observation truth tests pass. This is good.

However, the router daemon's live Unix-socket loop still only reads
`SignalMessageFrame` through `read_signal_input()`. It does not yet accept
`signal-persona-router::RouterFrame` requests from `persona-introspect`.

Current daemon path:

- accept Unix connection;
- decode message-ingress frame;
- ask `RouterRuntime` with `ApplySignalMessage`;
- write message reply.

Missing path:

- accept router observation frame;
- ask `RouterRuntime` with `ApplyRouterObservation`;
- write router observation reply.

### Recommendation

The next router/introspect integration slice should add daemon-level
`RouterFrame` ingress. The in-process observation plane is not enough for the
engine until another daemon can call it over a real socket.

## 6. Persona Introspect Is Still A Skeleton Consumer

`persona-introspect` improved:

- it uses `Option<>` instead of `Unknown`;
- it has typed configuration support;
- it stores observations through sema-engine;
- it has actor-density/source witnesses.

But the peer clients are not live. `ManagerClient`, `RouterClient`, and
`TerminalClient` currently carry socket paths and expose `socket()`, but no
query messages or socket protocol. `IntrospectionRoot::prototype_witness`
still returns:

```rust
manager_seen: None,
router_seen: None,
terminal_seen: None,
delivery_status: None,
```

### Recommendation

Do not describe `persona-introspect` as inspecting the engine yet. It is a
well-structured local observation recorder and daemon shell. The first useful
introspection slice is:

1. router daemon accepts `RouterFrame`;
2. `RouterClient` sends `RouterSummaryQuery`;
3. `PrototypeWitness.router_seen` becomes `Some(...)` from a live peer reply;
4. introspect stores that observation and renders it.

## 7. Harness Subscription Producer Is Real, But Not Wired Into The Harness Daemon

The `persona-harness` subscription actor plane is good local work:

- `TranscriptSubscriptionManager`;
- per-subscription `TranscriptStreamingReplyHandler`;
- `TranscriptDeltaPublisher`;
- slow-subscriber isolation witness;
- final retraction acknowledgement witness.

The representative `subscription_truth` suite passed.

But `HarnessRequestHandler::event_for_request` still only implements:

- `MessageDelivery`;
- `HarnessStatusQuery`;

Every other request, including `SubscribeHarnessTranscript` and
`HarnessTranscriptRetraction`, returns typed `HarnessRequestUnimplemented`.

### Recommendation

Say precisely: the producer-side actor pattern is implemented and tested
in-process; it is not yet the daemon's live Signal subscription surface.
The next slice should wire `SubscribeHarnessTranscript` and
`HarnessTranscriptRetraction` through the daemon and replace the test sink
with a socket-writer actor.

## 8. Persona Mind Remains A Major Bottleneck

Today's mind work is honest about the gaps:

- `ReplySupervisor` was renamed to `ReplyShaper`.
- subscription close semantics landed in `signal-persona-mind`;
- StoreKernel Template 2 is deferred because `kameo::spawn_in_thread()`
  closes parent-visible child state before the redb-owning actor value drops;
- choreography/adjudication handlers remain design work;
- subscription push delivery remains deferred.

The important practical consequence: `persona-mind` is not yet ready to serve
as the engine's live policy/adjudication plane.

### Recommendation

Do not block the first message/terminal prototype on full mind choreography.
But before claiming a full Persona engine, the mind needs at least one live
policy path:

- accept channel/message adjudication request;
- produce grant/deny/defer;
- persist the decision;
- expose it to router and introspect.

## 9. Manager Event Log And Snapshot Work Is Directionally Good

The manager work improved significantly:

- component child exit is observed by watcher tasks;
- `ComponentExited` events are appended;
- lifecycle/status snapshot reducers exist;
- snapshots rebuild from event log;
- unfinished spawn arcs become `ComponentOrphaned`;
- the representative rebuild witness passed.

Caution:

- the "event append and snapshot reduce share one transaction" witness is a
  source-scan test. The implementation does put both calls in one
  `self.database.write(...)` closure, so the source scan is not baseless, but
  it is still weaker than a behavioral crash/restart witness.
- the full dev-stack is currently red through Nix, so this manager work is
  not yet proved in the assembled engine.

### Recommendation

Keep the manager work, but add a stronger Nix-chained restart witness after
the flake inputs are updated:

1. start manager;
2. append lifecycle events;
3. stop/crash manager;
4. reopen from the same redb;
5. verify status from rebuilt snapshots.

## 10. Typed Configuration Is Partially Landed, But The Stack Is Inconsistent

Settled and committed:

- `persona-message` daemon typed config;
- `persona-router` daemon typed config in local HEAD;
- `persona-introspect` daemon typed config in local HEAD;
- `persona-terminal` supervisor typed config in local HEAD;
- contract records for several daemon configurations.

Still inconsistent:

- `persona/src/direct_process.rs` writes typed config only for `Message`,
  `Router`, and `Introspect`.
- `TerminalDaemonConfiguration` exists, but the manager does not write it yet.
- `persona-system` and `persona-harness` have uncommitted typed-config-related
  edits in their working trees, so their state is not settled.
- the Persona Nix flake lock is stale enough that the dev-stack assembles
  incompatible binaries and scripts.

### Recommendation

Typed config should end with one stack-level witness, not per-daemon claims:

```sh
nix run .#persona-dev-stack-smoke
```

That witness is currently red.

## Dirty Working Trees

These repos have uncommitted changes at audit time:

| Repo | Dirty files | Interpretation |
| --- | --- | --- |
| `persona-message` | `ARCHITECTURE.md` | likely designer/actor-supervision in-flight |
| `persona-system` | Cargo + daemon/supervision files | likely typed-config or supervision in-flight |
| `persona-harness` | Cargo + daemon/harness/supervision files | likely typed-config or supervision in-flight |

I did not treat these as settled work.

## Overall Assessment

The day's local component work is much better than the morning gap reports:

- terminal-cell control/data split is now real;
- closed-sum contract cleanup is mostly real;
- router observation plane is real in-process;
- manager event/reducer work is real;
- message/router/introspect typed-config surfaces exist locally;
- harness subscription producer actor pattern is real in-process.

The engine as a whole is not yet coherent because the integration layer is
behind the component layer:

- `persona` flake inputs are stale;
- `persona-dev-stack-smoke` is red;
- router observation is not exposed over daemon socket;
- introspect has no live peer query;
- harness subscription actor plane is not wired into daemon requests;
- mind policy/choreography is still deferred;
- some typed-config and actor/supervision work is still in dirty working
  trees.

## Suggested Next Order

1. Finish or pause the in-flight typed-config and actor/supervision edits so
   working trees are clean.
2. Bump `persona` flake inputs to compatible heads.
3. Make `nix run .#persona-dev-stack-smoke` green again.
4. Add router-daemon `RouterFrame` observation ingress.
5. Wire `persona-introspect::RouterClient` to query the live router daemon.
6. Wire harness transcript subscribe/retract into the daemon.
7. Revisit mind choreography once the message/terminal/introspect path is live.
