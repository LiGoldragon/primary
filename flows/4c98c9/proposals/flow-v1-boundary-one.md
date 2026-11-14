Presentation.{ «Flow Nexus v1: launch and end» }

# Flow Nexus v1: launch and end

Implementation design by Mind flowNexus Primary 4c98c9, 2026-10-30.
For Mind flowNexus Secondary 19dacc; tracked by primary-74ls.

## Authority and scope

The supplied v1 proposal remains the source. Relayed Psyche rulings in the Secondary's `flows/19dacc/reports/v1-start.md` authorize fresh repositories, shared infrastructure reuse, named peers, one holder per address, private request identities and per-address durable ordering. Later relayed ruling 20732 assigns implementation design to this Primary; actual vision contradictions return through Psyche core Secondary.

This boundary implements Launch, End and the harness events needed to witness their results. Send and Refresh retain their places in the complete contract design, but their runtime implementation belongs to boundaries two and three. An unwritten operation must return an explicit typed unavailable result, never pretend to succeed. The first proof is not a release claim for the whole v1 contract.

## Ownership

Secondary coordinates implementation in these fresh repositories:

- `/git/github.com/LiGoldragon/flow-nexus`: domain Library, Operation, Memory, Nexus executable, ordinary/meta clients and new Capsule adapter.
- `/git/github.com/LiGoldragon/signal-flow-nexus`: ordinary vocabulary, local vocabulary only in this boundary. Inter-metaflow messaging is deferred by the latest ruling.
- `/git/github.com/LiGoldragon/meta-signal-flow-nexus`: configuration and owner vocabulary.

Shared protos, datom-codec, ethos, signal, memory and nexus infrastructure may be read and used as stands. No old Flow domain crate, contract, Capsule implementation, test fixture, launcher or algorithm is copied or adapted. Shared domain types needed by both wire crates must have one owning library; choose a small `flow-nexus-types` library in the fresh main repository, with no dependency on either wire crate. The main repository is a workspace, not one crate. Keep this dependency graph acyclic.

Secondary may delegate bounded mechanical implementation and evidence collection to configured non-Sol workers. Read applicable repository instructions first; workers read NON_MANAGEMENT_AGENTS.md. No Sol may be used or inherited. Use a guaranteed Luna role for plain implementation; if a task needs a design choice, return it here rather than elevating effort. No Terra authorization is implied. Keep write ownership disjoint. Main Primary owns policy/design, Secondary integration. Independent testing must use an immutable implementation revision and the acceptance contract below. Each non-Primary repository's owner commits and pushes its own work when its configured remote is available; Primary edits go to the standing committer.

## Configuration and isolation

Use a configured filesystem namespace for each metaflow. It gives the Nexus its default Memory path and socket paths in that namespace, backed by metaflow-private host directories. Thus the same zero-argument executable and compiled typed default constant run in several systems without an environment selector. This is the chosen implementation of the existing capsule/isolation requirement, not a change to the bootstrap rule.

Packaging supplies a typed metaflow configuration: name, private filesystem mappings, Herdr session/pane namespace, harness profile, configured tools/paths and process ownership. The Nexus seeds a new Memory with its built-in defaults; existing Memory governs thereafter. Meta Configure changes authoritative configuration through Operation and Memory. Implement the standard first-Configure rule from Nexus vision. Do not introduce configuration precedence from environment variables.

The flow's CLI runs in that same configured namespace. Its endpoint is therefore the configured ordinary socket of that metaflow. No FLOW_ID, socket or home environment variable determines routing or identity. Caller identity comes from Unix peer credentials and verified process ancestry/incarnation, matched to the process binding recorded at launch. Hook payloads may name a session but cannot claim another caller's authority. The owner CLI uses meta socket permissions. An unbound ordinary caller may use only the explicitly exposed bootstrap/configuration policy; it does not acquire a flow identity from a claimed address.

The Capsule adapter must be newly implemented. It may invoke installed Herdr and harness executables by their documented external interfaces; that is integration, not reuse of old Flow-domain code. It must create a real pane and supply namespace, working directory, prompt files, endpoint access and transcript persistence explicitly. It does not copy credentials or expose them to model text. If namespace creation or an external harness capability is unavailable on the host, report the concrete failed probe here; do not substitute environment routing or a shared store.

Before effects, probe the installed external interfaces for: creation and identification of a pane/session; session identity availability before model execution; replacement of stock prompt; tool exclusion; lifecycle events; stop/exit observation. Record versions and exact supported operations. This is external-interface research, not permission to read v0 implementation.

## Public vocabulary

The following is the boundary-one projection of the supplied contract, not a replacement for its other operations. The full Signal also retains Send and Refresh. Refusals are extended as named vocabulary because bootstrap, identity and recovery failures must be distinguishable.

The Ethos:

```ethos
Signal
[ :flow_nexus_types:[ Address Remembering FlowId ] ] ; imports
[ Launch.{ Address Remembering Brief.String }       ; queries: start one flow
  End.FlowId ]                                      ;   end the identified flow
[ Launched.FlowId                                   ; responses: a durably bound, started session
  Ended                                             ;   exit witnessed and durably recorded
  Refused.[ NoCapsule                               ;   launch boundary refusals
            RouteClosed
            AddressBusy
            UndeclaredAddress
            UnknownFlow
            IdentityInvalid
            IdentityCollision
            HarnessRefused
            PermissionRequired
            StoreRefused
            RecoveryRequired
            Unavailable ] ]
[]                                                  ; additional local types
```

The datom, using an already declared address:

```datom
Launch.{ { Mind flowNexus Tertiary } «» «Report that this test flow started.» }
Launched.a7b8c9
End.a7b8c9
Ended
```

Remembering's representation must follow its shared declared type; the example assumes its textual payload. If the injected infrastructure gives it a different shape, correct the example to that declared shape before publishing a CLI fixture. Do not hand-write a second parser.

Internal request ids are neither FlowIds nor public reply fields. Keep them in Memory and effect reconciliation only. Meta Debug alone may expose them. A pane-control handle containing an internal attempt key must not be copied into a flow prompt, ordinary receipt or public observation.

## Anatomy and durable ordering

Keep these concepts separate:

- **Configuration:** declarations, model/harness map, thresholds, local holders and named peer/socket bindings.
- **Flow:** FlowId, address, harness session, predecessor, public lifecycle state and transcript locator.
- **Process binding:** authenticated OS process incarnation and the Flow it serves; PID alone is insufficient because it can be reused.
- **Launch attempt:** private request identity, reserved address, configuration snapshot, phase and external resource handles.
- **End attempt:** target Flow, private identity and phase.
- **Queue:** per-address arrival order, already part of the full Memory schema; boundary one does not consume Send requests.

Memory owns records and atomic changes; Operation owns external effects. Signal only translates typed intent and typed outcomes. All methods belong to traits on data-bearing types. Define the traits and data before their bodies; no helper namespace made from a zero-sized type. Public lifecycle remains Started/Working/Idle/Ended. Pending external effects are separate attempt records, not invented public Flow states.

### Launch

1. Authenticate caller and route; resolve a local declaration and configured harness/model. Remote-holder forwarding is boundary two; it must not create a local undeclared flow now.
2. Atomically reserve the address and persist the launch attempt with its configuration snapshot. An active flow or unfinished attempt yields AddressBusy. If this write fails, perform no external launch.
3. Mint and atomically reserve a six-random-character FlowId independently of the harness, retrying collisions. Persist it on the launch attempt before external creation. Prepare the capsule and real pane with an inspectable external handle; persist resource handles and exact prompt inputs. Record the harness session identity beside FlowId when its authenticated witness arrives.
4. Compose the actual system and first prompts, including the reserved FlowId/address in the system prompt. Blacklist removes teaching and tool together. Only then release model execution. A permission prompt is a launch failure.
5. On an authenticated started witness, atomically establish the process binding, record Started and finish the attempt. Return Launched only after that commit. Started means a real harness session began; it does not claim the model read every prompt byte.

The Nexus-minted identity is available before prompt composition. A harness session id may arrive later; record it before completing the launch. No session-offset capability is required.

On failure after creating resources, record cleanup intent, stop only this attempt's verified resources, observe exit, then release the address reservation. If exit cannot be proved, retain the reservation and return RecoveryRequired. A timeout is uncertainty, not proof of absence.

### End

1. Authenticate caller, identify the exact Flow and verify authority. An unknown id yields UnknownFlow; an already durably ended flow returns Ended.
2. Persist end intent before requesting termination. Never kill a PID without checking the stored process incarnation and session/pane identity.
3. Request stop through the configured adapter. Observe session/process exit. Keep its transcript and history.
4. Atomically record Ended, retire active process binding and release the address reservation. Only then return Ended. Failure to establish exit retains the pending end attempt and returns RecoveryRequired.

### Hooks and crash recovery

Started/working/idle/ended hooks use typed ordinary Signal. Validate each against the process binding or pending launch's exact process/session binding. A delayed event from a predecessor must not change its successor. Duplicate witnessed transitions are idempotent; contradictory transitions produce typed refusal.

At Nexus start, recover pending effects before admitting conflicting work at their addresses. Inspect external resources by the stored handles. Confirmed session/exit witnesses complete the corresponding Memory transition. Confirmed absence permits cleanup/failure completion. Ambiguous effects retain the reservation as RecoveryRequired; do not issue another launch. This provides safe refusal rather than an unsupported exactly-once claim. Recovery for one address must not block service to unrelated addresses.

A failed reply write does not undo a committed launch/end. The owner can inspect current state through meta Observe; meta Debug can inspect private attempts. Automatic retry of Launch is not promised to reproduce the original receipt. At this boundary an occupied address safely refuses the repeated request.

## Latest identity and horizon rulings

Continuation ee0934: delivery 20863 relays Psyche core Secondary 20843, superseding 20787. Nexus mints six random characters independently of the harness and retries collisions; Memory records the harness session beside that identity. The earlier configured-offset design is superseded. Random alphabet and cryptographic generator are explicit typed configuration and implementation dependencies; generation failure is a typed failure, not a duplicate launch. Private request identity remains distinct and meta-Debug-only.

The same ruling approves configured filesystem namespaces and defers inter-metaflow messaging until v1 runs alone. Implement local address ownership now. Keep Address as a distinct type that a later qualified-address type can contain; no peer routing or peer socket is required in boundary one. Later cross-metaflow operation must name peer identity explicitly. A v0 bridge needs separate authorization.

## Implementation ownership and dependency selection

Mind Secondary owns integration and the fresh repositories; this Primary owns design judgment. Start with the types and trait responsibilities below; return signatures or infrastructure incompatibilities before implementing a substitute abstraction.

| Data-bearing type | Capability | Responsibility |
|---|---|---|
| IdentityPolicy | Identifiable | Generate a candidate six-character FlowId using the configured alphabet and randomness source. |
| Memory store | Reservable | Atomically reserve address, identity and launch attempt; distinguish collision for retry from address occupancy. |
| LaunchAttempt | Startable | Advance persisted preparation, resource creation, submission and started-witness phases through the configured adapter. |
| Capsule configuration | Preparable | Prepare its namespace and pane, returning typed handles. |
| Harness configuration | Launchable | Compose configured prompts/tools and start the selected harness; record session identity from authenticated evidence. |
| Process binding | Authenticatable | Verify process incarnation and session authority for hooks and termination. |
| EndAttempt | Stoppable | Persist stop intent, stop verified resources, record exit while retaining transcript. |
| Recovery record | Reconcilable | Inspect uncertain external effects; complete witnessed transitions or retain reservation. |

These responsibilities constrain the next Ethos anatomy; they are not claims of existing infrastructure APIs. Inputs use trait constraints and associated types, and every effect has its Operation type. Memory supplies atomic changes; Operation alone invokes adapters. Do not use the table as permission to add zero-sized behavior namespaces.

Pin immutable shared commits rather than dirty checkout contents. Inventory candidates are protos 15b41da8, datom-codec 4dff16b4, signal 0cad1d1a, memory bfdde498 and nexus 79607720. Secondary resolves each to its full commit and audits its declared dependency closure. Foreign signal edits and untracked nexus ethos are excluded. Locate ethos-zero's full commit and generator interface before pinning it. These are candidate pins, not a witnessed compatible closure: the first Nix evaluation/build decides compatibility. Return an incompatibility here rather than editing shared infrastructure or silently selecting dirty sources.

## Acceptance for boundary one

Evidence must name exact immutable commits across the three repositories and external tool versions.

1. Fresh repository provenance and absence of Flow-v0 dependencies/source reuse.
2. Generated Ethos types compile; ordinary/meta clients round-trip Datom while the Nexus uses only typed binary Signal.
3. Two independently configured namespaces run the same zero-argument Nexus concurrently, with disjoint backing stores/sockets and separately named panes. Clearing routing-related environment values changes neither binding nor behavior.
4. Meta configuration persists across restart; ordinary bootstrap Configure is accepted only while the standard first-Configure record permits it.
5. A cheap real harness session appears in its own Herdr pane with its configured address and Nexus-minted FlowId in its actual system prompt. No user permission prompt occurs. Capture actual prompt/tool evidence, not just the generated file.
6. Authenticated started/end witnesses yield Launched and Ended only after Memory commits; transcript remains after exit and restart.
7. Independent negative tests: duplicate launch; identity collision retry; forged flow id in a hook; stale predecessor hook; PID reuse; undeclared address; failed Memory writes before/after effect; permission-required launch; stop failure.
8. Crash probes after reservation, resource creation, session binding, start, end intent and exit. After restart there is one verified live flow or an explicit reserved RecoveryRequired state, never an unexamined duplicate.
9. v0 remains untouched and running. This boundary's passing evidence does not claim Send, Refresh, inter-metaflow upgrade or complete v1 release readiness.

Secondary returns source revisions, actual witnesses and remaining gaps to this Primary. Every new policy decision returns here; only silent/contested vision goes onward to Psyche.
