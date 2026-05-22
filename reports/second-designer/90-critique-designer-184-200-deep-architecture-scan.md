# Critique of Designer 184-200 Deep Architecture Scan

Date: 2026-05-16
Role: designer-assistant

## Scope

This critiques the designer morning scan:

- gap reports: `reports/designer/184` through `reports/designer/193`
- prior-art reports: `reports/designer/194` through `reports/designer/199`
- master synthesis: `reports/designer/200`

The report is organized by component. Each component section reads its gap
report together with the relevant prior-art reports and with the master
synthesis. I also checked current source where a designer report looked likely
to be stale.

## Top Corrections Before Operators Use /200

1. `persona-message` is cleaner than /187 and /200 say.

   Current code has typed daemon configuration for message socket, router
   socket, supervision socket, socket modes, and owner identity. The stale claim
   is that daemon router/supervision socket discovery still falls back to
   environment variables. I found only CLI-side `SignalMessageSocket::
   from_environment()` for `PERSONA_MESSAGE_SOCKET` / `PERSONA_SOCKET_PATH`.
   That may still deserve a typed CLI configuration path, but it is not the
   same problem as a supervised daemon silently ignoring its spawn envelope.

2. `signal-persona-router` has already removed the `Unknown` delivery status
   that /193 and /200 still cite.

   Current `RouterDeliveryStatus` is closed: `Accepted`, `Routed`, `Delivered`,
   `Deferred`, `Failed`. Missing message slots are represented as
   `RouterMessageTraceMissing`, not a sentinel status. The closed-sum critique
   should move to places that still have `Unknown`, especially
   `signal-persona-introspect`.

3. `terminal-cell` is partially split already, but not fully.

   The client-side API already has `control.sock` and `data.sock` concepts.
   The daemon path still binds a single `cell.sock`. /189 is directionally
   correct, but the operator task is not "invent the split"; it is "finish the
   split and make daemon, client, persona-terminal, tests, and architecture
   agree."

4. /200 contains estimates and dated forecast language.

   ESSENCE rejects software time estimates. /200's "1 week", "next month",
   and "next quarter" framing should be removed before it becomes a canonical
   operator handoff. Replace with ordered dependency gates and witnesses.

5. The contract dependency recommendation must use named API references, not
   raw revisions.

   The `signal-persona-*` contract crates currently depend on `signal-core`
   by bare git URL with no branch/tag/bookmark. That is a real stability gap.
   The fix should follow the workspace's named-reference policy: stable API
   branch, bookmark, or tag. Do not recommend raw `rev = ...` pins.

## Component Critiques

## 1. Persona Engine Manager

Reports read together: /184, /194, /196, /199, /200.

### What the designer got right

/184 correctly finds three serious prototype gaps:

- readiness is currently shaped as retry loops and sleep intervals;
- manager event logging is not yet a real lifecycle/status reducer pair;
- child exit observation is not first-class enough for a supervised engine.

The prior-art reports support this well. OTP, Akka, and systemd all point
toward explicit lifecycle events, restart semantics, and readiness facts.
Event-sourcing prior art supports manager snapshots as projections over an
event log.

### Critique

The polling critique needs one more distinction. Polling as a state-change
architecture is forbidden. A bounded startup reachability probe is not the same
sin. The right architecture should say:

- readiness is ultimately pushed or explicitly answered by the component;
- manager may use bounded connect/probe retries only while establishing a
  supervised child boundary;
- a retry loop must not become the engine's ongoing health model.

The proposed "SocketBound pushed by child" also needs a concrete transport
story. A child cannot push a socket-bound observation before the control
relation exists unless the manager provides an already-open channel or uses
systemd-style socket activation. Otherwise the manager can only verify the
filesystem socket after spawning. The architecture should choose one of these:

- manager binds sockets and passes file descriptors or paths to children;
- child binds sockets, then manager verifies path, type, owner, mode, and
  protocol readiness;
- child emits readiness on a separate supervision socket that the manager owns.

Snapshot design is also under-specified. An eager snapshot on clean shutdown is
not a crash-recovery strategy. If the daemon crashes after event append but
before snapshot, startup must either replay from the event log or treat the
snapshot as a cache that can be behind. /196 gestures at this, but /200's
"snapshot reducers" move reads too complete.

### Recommendation

Keep the two reducers named in `/200`, but make the architecture explicit:

- engine-lifecycle reducer: launched, ready, exited, expected shutdown,
  unexpected failure;
- engine-status reducer: what CLI status and introspection read;
- event log is authoritative;
- snapshots are acceleration, not truth.

## 2. Persona Mind

Reports read together: /185, /194, /195, /196, /200.

### What the designer got right

The StoreKernel blocking concern is real. Current code routes redb/sema-engine
work through actor message handlers, and that should not become async-runtime
blocking under load. The "Template 2" prior-art answer is the right shape:
stateful storage work belongs behind a dedicated blocking lane owned by a
named actor or worker.

The choreography gap is also real. Mind needs a real noun for channel policy,
authorization, route grants, temporary grants, denial reasons, and audit.
"ChoreographyAdjudicator" is much better than letting policy leak into router.

### Critique

/195's strongest claim about subscription close is too absolute. It says Path A
means unsubscribe should not be a request-side relation. In an async Signal
world, a consumer-initiated close is naturally a control operation. The better
shape is:

- client sends a typed retraction/close operation for a subscription token;
- server replies or emits a final `SubscriptionRetracted` event;
- the event stream then ends.

That keeps push-stream semantics without pretending the consumer has no
control message to send. This matters because `signal-persona-mind` and
`signal-persona-system` already contain request-side subscription retraction
shapes. Do not delete them reflexively because a prior-art report overcorrected.

The choreography actor also needs a state model before implementation:

- pending adjudications;
- active grants;
- grant expiration and retraction;
- source and target channel identity;
- reason records for allow, deny, defer;
- audit/introspection projection.

### Recommendation

Implement StoreKernel isolation and subscription push before deep choreography.
But before deleting subscription retraction variants, settle the Signal
subscription lifecycle as "request close plus reply-side final event."

## 3. Persona Router

Reports read together: /186, /195, /196, /198, /200.

### What the designer got right

/186 sees the router correctly as structurally close to the intended topology:
message ingress, channel authority, mind adjudication, harness delivery, and
observation surface are named concepts rather than one large command handler.

The report also correctly flags:

- `MindAdjudicationOutbox` is in-memory;
- observation contracts exist but the daemon does not yet serve them as a real
  introspection surface;
- harness delivery currently uses a blocking-ish helper shape that deserves a
  clearer actor or worker lane.

### Critique

The report undersells the launch/configuration problem. `ChannelAuthority`
persisting to redb "if tables are present" is not a strong engine invariant.
The daemon launch path must guarantee the authority has its typed store path
and tables from configuration, then witnesses should prove that channel
authority state survives restart.

The in-memory `MindAdjudicationOutbox` is acceptable only if it is explicitly
transient. If it means "messages waiting for mind decision," then it is
prototype-risky and needs a recovery rule. If it means "runtime queue backed by
a durable channel-decision record," then the report should say so.

The closed-sum critique in /193 and /200 is stale for router delivery status.
Current `signal-persona-router` already uses `RouterMessageTraceMissing`
instead of `RouterDeliveryStatus::Unknown`. Keep this as a positive example
for other contracts, especially introspect.

### Recommendation

Next router design move should be a restart witness:

1. accept message;
2. persist channel/adjudication state;
3. restart router;
4. query observation surface;
5. prove the state comes back as typed Signal, not in-memory coincidence.

## 4. Persona Message

Reports read together: /187, /198, /199, /200.

### What the designer got right

The current `persona-message` direction is strong:

- `persona-message-daemon` is the supervised component;
- CLI is a client, not the daemon itself;
- message ingress is user-writable boundary input;
- SO_PEERCRED origin stamping belongs at this boundary;
- router forwarding is Signal-shaped.

### Critique

/187 is stale on daemon configuration. Current code reads a typed
`MessageDaemonConfiguration` from `nota-config` in the daemon binary and passes
message socket, router socket, supervision socket, socket modes, and owner
identity into `MessageDaemon::from_configuration`. The environment fallback I
found is CLI-side message socket discovery, not daemon router/supervision
discovery.

That matters because /200 carries the stale problem into its cross-cutting
"retire env fallback" move. The move is still valid globally, but
`persona-message` should be marked mostly corrected. Remaining question:
should CLI socket discovery be allowed as user convenience, or should every CLI
also accept a typed NOTA config/argv source? That is a smaller and more precise
question than "daemon ignores spawn envelope."

/187 also calls `MessageOriginStamper` a "pure behavior" smell. I disagree with
the proposed fix if it becomes a free function. The concept has data
(`OwnerIdentity`) and behavior (mapping peer credentials to message origin). It
can be a valid policy/value object. If the name feels too agentic, rename it to
`MessageOriginPolicy` or make it a field-owned method on the daemon root. Do
not flatten it into anonymous helper code.

Router submission from daemon handlers may still be too blocking. That should
be solved with a real `RouterClient` lane or actor, not by weakening the
message daemon topology.

### Recommendation

Correct /187 and /200 before operators act:

- daemon typed config: mostly done;
- CLI env discovery: still open policy;
- origin stamping: keep as named data-bearing policy or root-owned method;
- router client I/O: move to a named client lane if tests show blocking.

## 5. Persona Harness

Reports read together: /188, /195, /197, /198, /199, /200.

### What the designer got right

The main gaps are real:

- harness kind is not fully closed around production vs fixture cases;
- daemon launch path still hardcodes Pi in places;
- supervision/config still uses environment-variable paths;
- terminal delivery is not a clean daemon-to-daemon Signal boundary;
- observation push for typed harness state is missing.

### Critique

The "terminal delivery is library-shaped, not Signal" critique needs precision.
The source imports implementation-facing `persona_terminal::contract` shapes.
The problem is not merely "a library exists." The problem is that harness should
depend on the terminal contract surface and speak to the terminal daemon over a
boundary, rather than bind itself to persona-terminal implementation internals.

Transcript push needs privacy discipline. Do not turn "harness observation
push" into raw transcript fanout. Prior design says raw terminal bytes stay in
terminal-cell/persona-terminal storage. Harness should publish typed delivery,
lifecycle, provider, and quota observations plus sequence pointers where
needed.

/188 also uses time estimates. Those should not be copied into operator
handoffs.

### Recommendation

Use a fixture-first harness witness:

1. launch harness with typed configuration;
2. `HarnessKind::Fixture` or equivalent closed test variant;
3. deliver a typed message through Signal;
4. hand terminal injection to terminal daemon over the contract boundary;
5. emit typed delivery observation;
6. prove no raw transcript is pushed to router or mind.

## 6. Persona Terminal and Terminal Cell

Reports read together: /189, /195, /197, /200.

### What the designer got right

The high-level prior-art conclusion is right: terminal-cell has two planes.

- control plane: Signal commands, subscriptions, health, attach leases,
  injection requests;
- data plane: raw PTY bytes, direct enough to preserve terminal behavior.

The architecture also correctly protects the input gate as a minimal fast path.

### Critique

/189 should distinguish partial scaffold from live daemon behavior. Current
`TerminalCellClient` already has `control_socket` and `data_socket`. Current
daemon binding still uses a single `cell.sock`. So the work is a convergence
task across daemon, client, persona-terminal supervisor, tests, and docs.

The output fanout critique is mostly right but slightly too compressed. Current
`TerminalOutputFanout` writes to the active viewer or reserved backlog, then
tells the `TerminalCell` actor to append transcript and broadcast deltas. This
is better than raw transcript writes in the same viewer stream, but it still
couples output flow to a synchronous fanout thread and an actor mailbox. The
needed witness is not "does code contain a broadcast channel?" The witness is:

- slow or stalled viewer does not block transcript append;
- transcript append does not block raw viewer output;
- control messages remain responsive while data plane is busy;
- detach/reattach preserves expected backlog behavior.

The naming confusion around daemon vs supervisor is valid. Persona-terminal
must be explicit about which binary supervises terminal-cell instances and
which sockets it owns.

### Recommendation

Before more feature work, finish one terminal-cell integration slice:

1. daemon binds `control.sock` and `data.sock`;
2. client and persona-terminal use the split;
3. control socket speaks Signal;
4. data socket remains raw PTY bytes;
5. Nix witness proves slow viewer and busy transcript do not corrupt input
   latency.

## 7. Persona Introspect

Reports read together: /190, /195, /196, /198, /200.

### What the designer got right

/190 correctly identifies persona-introspect as a high-value development
component and correctly keeps it out of peer redb files. The right model is:
introspect stores its own observations and asks live peer daemons over Signal.

The report also correctly says the daemon/store/supervision shell exists, while
peer query behavior is mostly scaffold.

### Critique

`Unknown` is still a problem here. Current `signal-persona-introspect` has
`ComponentReadiness::Unknown` and `DeliveryTraceStatus::Unknown`. If these are
wire-visible states, they violate the closed-sum discipline. They should be
replaced by precise states such as:

- `NotObservedYet`;
- `PeerSocketMissing`;
- `PeerSocketUnreachable`;
- `PeerQueryUnimplemented`;
- `TraceMissing`;
- `TraceStatusUnavailable`.

The report says client actors can remain while returning unimplemented. That is
acceptable only if they have a real typed `Unimplemented` boundary and a test.
An actor that exists only as a manifest name is the exact scaffold rot the
actor-system skill warns against.

Push subscriptions can wait, but first-use introspection should not wait for
push. A useful prototype can start with target-specific `Match` queries against
manager, router, terminal, and message.

### Recommendation

Make introspect's first implementation smaller and sharper:

1. one live peer client;
2. one typed target-specific `Match` query;
3. one sema-engine stored observation;
4. one NOTA rendering;
5. no `Unknown` sentinels.

## 8. Persona System

Reports read together: /191, /194, /195, /199, /200.

### What the designer got right

The pause is honest. `persona-system` has a real Niri focus/event-stream shape,
but the broader Persona prototype can progress without forcing focus policy or
privileged OS actions into the first engine path.

Focus tracking being push-shaped is also good. This is not a polling problem.

### Critique

/195 again overcorrects around subscription retraction. If a client subscribes
to focus observations, it needs a way to close that subscription. A request-side
close/retract operation plus final reply/event is cleaner than saying close is
only reply-side.

The component name remains weak. "System" is too broad for a component that is
currently compositor/window/focus shaped. Keeping it paused avoids forcing a
rename now, but the naming question should remain open.

Force-focus style requests are rightly deferred. When they return, the name
should not promise success. `FocusIntervention` or `FocusRequest` with typed
backend/policy failure replies remains the better shape.

### Recommendation

Do not put persona-system on the critical prototype path until terminal and
message routing are live. Keep its useful push-focus work, but defer privileged
actions and naming until the need becomes concrete.

## 9. Kernel Stack: signal-core and sema-engine

Reports read together: /192, /194-/199, /200.

### What the designer got right

The kernel stack is in much better shape than the component daemons:

- six Signal root verbs are settled for now;
- request/reply frames and streaming frames are separated;
- async exchange identifiers exist;
- the proc macro has compile-fail witnesses;
- sema-engine has the right split from sema-kernel.

### Critique

/192 says "production-ready" too strongly for `sema-engine`. It may be kernel
ready, but the workspace now wants to use it outside Persona for `lojix`. That
needs a consumer recipe:

- minimal contract crate;
- daemon store initialization;
- assert/mutate/retract/match examples;
- index creation and query example;
- snapshot/restart example;
- Nix check that exercises a non-Persona consumer.

The single-owner writer rule is also not yet strong enough. If it is a runtime
discipline only, the report should say so and demand a witness. If it can be
type-enforced, that belongs in the sema-engine API.

The subscription lifecycle question is still a kernel/channel design issue.
/200 treats it as implementation sweep, but the "request close plus final
event" semantics need to be written once before every contract invents its own
shape.

### Recommendation

Call the kernel stack "ready for first external consumer hardening," not
"done." Use `lojix` as the proving consumer for sema-engine and signal-core,
but keep the first slice small and tested.

## 10. Signal-Persona Contracts

Reports read together: /193, /195, /198, /199, /200.

### What the designer got right

The macro adoption and relation discipline are mostly in the right place. The
workspace now has typed contract crates instead of unbounded shared-type
buckets, and the proc macro moves repeated request/reply boilerplate into a
single language surface.

### Critique

The closed-sum inventory needs a fresh source pass before action. Router's
`Unknown` status is already gone. Introspect's `Unknown` statuses remain. Mind's
`UnknownRoleName` is more subtle: if it means "the requested role name is not
registered," it may be a legitimate domain error despite the word "Unknown."
The smell is strongest when `Unknown` means "we failed to model this state."

The dependency-pinning critique is real but must be phrased correctly. Bare git
URL dependencies to `signal-core` mean contract crates silently track whatever
the remote default branch points at. The workspace should use named stable API
references: branches, bookmarks, or tags. Do not use raw revisions as the
standard recommendation.

The Path A subscription advice should be rewritten. Standardize this instead:

- subscribe request opens a stream and returns a typed token;
- stream emits typed events;
- client may send typed close/retract operation for the token;
- server acknowledges with a final reply/event and ends the stream;
- no raw socket close as semantic protocol.

### Recommendation

Run a contract-by-contract source audit with three output columns:

- true closed-sum violation;
- legitimate domain-missing state but badly named;
- already corrected since the designer scan.

## Master Synthesis /200

### What works

/200 is valuable as a broad map. The eight moves are directionally good:

1. eliminate ongoing polling;
2. isolate StoreKernel blocking work;
3. add child-exit observation;
4. add manager snapshot reducers;
5. implement subscription push/close semantics;
6. finish terminal-cell control/data split;
7. close sentinel/unknown sums;
8. retire daemon env fallback.

### What must be corrected

The synthesis should not be treated as implementation-ready until it absorbs
these corrections:

- remove time estimates and forecast horizons;
- mark `persona-message` daemon typed config as mostly corrected;
- remove stale router `Unknown` finding;
- rephrase dependency stability as named API refs, not raw revision pins;
- distinguish bounded startup reachability probes from ongoing polling;
- define subscription close semantics before deleting retraction requests;
- say terminal-cell split is partially scaffolded but not live in daemon;
- describe snapshots as projections over an authoritative event log.

### Missing synthesis layer

/200 lists moves, but the engine still needs a witness matrix. Each move should
name the exact proof that will make it true:

| Move | Needed witness |
| --- | --- |
| Readiness without polling | child becomes ready without ongoing sleep loop; startup retry bounded and named |
| StoreKernel blocking lane | slow redb/sema operation does not block unrelated actor messages |
| Child exit | unexpected child death becomes typed manager event and status projection |
| Reducers | restart reads event log/snapshot and returns same status |
| Subscription lifecycle | subscribe, event, close, final event, stream end |
| Terminal split | slow viewer cannot delay input/control plane |
| Closed sums | source scan finds no sentinel `Unknown` for unmodeled states |
| Typed config | daemon startup uses spawn envelope/NOTA config, not ambient env fallback |

## Questions For The User

1. Should CLI socket discovery via environment variables be allowed as user
   convenience, or should every CLI use the same typed NOTA/argv configuration
   discipline as daemons?

2. Do you agree that subscription close should be a request/control operation
   plus a final reply/event, rather than removing request-side retraction
   variants entirely?

3. Should `persona-system` remain a paused component while the first prototype
   proves message, router, harness, terminal, and introspect, or should focus
   observations be pulled into the first prototype witness?

4. For stable contract dependencies, should the first named API reference be a
   branch/bookmark such as `signal-core-api-v1`, or a release tag once the
   external `lojix` consumer compiles?
