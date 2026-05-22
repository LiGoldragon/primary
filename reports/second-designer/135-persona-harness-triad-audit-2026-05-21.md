# 135 — persona-harness triad audit (2026-05-21)

*Audit of the persona-harness triad: `signal-persona-harness` (the
working signal contract), `persona-harness` (the daemon + thin CLI),
and `owner-signal-persona-harness` (MISSING — proposed below). Triad
shape, name compliance, and migration distance against the
post-/255 / /256 / /257 / /258 baseline.*

## 0 · TL;DR

The persona-harness triad is in the same pre-migration shape as the
unmigrated half of /257. It is **one leg short** — `owner-signal-
persona-harness` does not exist. Stack of stale shape, in priority:

- **Owner contract MISSING**, but per the triad invariant
  (`skills/component-triad.md` §"Two authority tiers — both part of
  the triad") every stateful component must ship both surfaces
  together; intentional gap acknowledged at
  `intent/component-shape.nota` 2026-05-19T20:30:00Z. Proposed shape
  in §3 below — narrow lifecycle/policy surface (Start / Drain /
  Reload / Configure / GrantTerminalEndpoint / RevokeTerminalEndpoint
  / Retire), modelled on the spirit owner contract.
- **`signal-persona-harness` still on `signal-core` + universal
  verbs** (`Assert / Match / Retract / Subscribe` prefixes;
  `signal_persona_harness/src/lib.rs:349-381`). Same gap as /257 §1.1
  for unmigrated contracts.
- **`persona-harness` daemon does not use `signal-executor`** —
  same gap /258 §2.2 surfaced for engine-manager; spirit fixed it
  in `786ab311`.
- **`Harness*` ancestry prefixes on most contract types** —
  `HarnessName`, `HarnessStatus`, `HarnessHealth`, `HarnessReadiness`,
  `HarnessStarted`, `HarnessStopped`, `HarnessCrashed`,
  `HarnessTranscriptSnapshot`, `HarnessTranscriptToken`,
  `HarnessTranscriptSequence`, `HarnessSubscriptionRetracted`,
  `HarnessOperationKind`, `HarnessRequestUnimplemented`,
  `HarnessUnimplementedReason`, `HarnessDaemonConfiguration`.
- **No observable block**; per `intent/persona.nota`
  2026-05-21T10:00:00Z (*"debug the debugger"*) and
  `intent/component-shape.nota` 2026-05-20T02:00:00Z (mandatory
  Tap/Untap), the engine-manager-tier-and-below components are not
  exempt from this.
- **`HarnessRequestUnimplemented { harness, operation, reason }`** —
  carries both a redundant `operation` field (per /257 §1.6) AND a
  redundant `harness` field (the operation payload already names
  the harness; same positional-alignment argument).
- **Daemon contains flag-style argument parsing**
  (`persona-harness/src/daemon.rs:531-587` — `--socket`, `--harness`,
  `--kind`, `--terminal-socket`) AND reads environment variables
  (`PERSONA_HARNESS_TERMINAL_SOCKET` line 184;
  `PERSONA_SOCKET_MODE` line 199). Both violate the NOTA-only
  argument rule
  (`skills/component-triad.md` §"The single argument rule"). The
  `from_configuration` typed path exists; the legacy flag path
  should retire.
- **Direct in-process terminal-library call**
  (`persona-harness/src/daemon.rs:415` →
  `persona-harness/src/terminal.rs:153-157`
  `TerminalTransportBinding::from_socket_path(...).handle_request(...)`)
  — the harness daemon hand-rolls the terminal write through a
  library binding rather than acting as a Signal client of
  `persona-terminal`. ARCH calls this "transitional" but per /150
  §6.5 (*"NO direct string injection path that bypasses
  router/terminal guards"*) it is the load-bearing path that must
  go through the Signal contract with the input-gate authority
  surface intact. This is the most architecturally significant gap
  in this triad.
- **CLI does not exist as a separate thin client.** The component
  ships one binary: `persona-harness-daemon` (main.rs handles both
  legacy CLI and typed config). Per /150 §2 the CLI is the daemon
  binary with `-daemon` removed; here it should be
  `persona-harness` binary, named `harness` per the CLI naming
  Decision at `intent/component-shape.nota` 2026-05-20T13:00:00Z
  (CLI = daemon name minus `-daemon`).

**Priority for migration slice**: (1) propose + implement
`owner-signal-persona-harness` (the missing leg); (2) signal-core
→ signal-frame + contract-local verbs in working signal; (3) drop
`Harness*` ancestry prefixes; (4) NOTA-only argument path in daemon
+ separate thin CLI binary; (5) signal-executor migration; (6)
observable block; (7) drop direct terminal library call → become
real Signal client of `persona-terminal`.

The owner-signal proposal in §3 below is what this audit's caller
asked for; the working-contract findings are alongside as the
matching context.

## 1 · /257 findings status

Mapped against /257's universal patterns:

### /257 §1.1 — Old universal-verb shape

**Status: NOT FIXED.**
`signal-persona-harness/src/lib.rs:349-381` —

```rust
signal_channel! {
    channel Harness {
        request HarnessRequest {
            Assert MessageDelivery(MessageDelivery),
            Assert InteractionPrompt(InteractionPrompt),
            Retract DeliveryCancellation(DeliveryCancellation),
            Match HarnessStatusQuery(HarnessStatusQuery),
            Subscribe SubscribeHarnessTranscript(SubscribeHarnessTranscript) opens HarnessTranscriptStream,
            Retract HarnessTranscriptRetraction(HarnessTranscriptToken),
        }
        ...
    }
}
```

Six universal-verb prefixes still in place. Target shape, post-/256
discipline:

- `Assert MessageDelivery(MessageDelivery)` → `operation Deliver(MessageDelivery)`
  (the doubling on the request side: `MessageDelivery` is the
  payload noun, `Deliver` is the verb).
- `Assert InteractionPrompt(InteractionPrompt)` → `operation Prompt(InteractionPrompt)`
  (or `operation Surface(InteractionPrompt)` if the verb intends
  "surface this to the human in the harness"; psyche call).
- `Retract DeliveryCancellation(DeliveryCancellation)` →
  `operation Cancel(DeliveryCancellation)`. (Note: cancellation
  in-flight isn't really a Retract at the working-signal layer; it
  is its own contract-local verb.)
- `Match HarnessStatusQuery(HarnessStatusQuery)` → `operation Query(StatusQuery)`
  or, if the channel grows other read targets, `operation Query(Query)`
  with `Query::Status(StatusQuery)` as the inner variant per /257
  §1.4 (lift the repeated category).
- `Subscribe SubscribeHarnessTranscript(SubscribeHarnessTranscript)` →
  `operation Watch(TranscriptSubscription) opens TranscriptStream`
  (Spirit-style; drop the `Subscribe` and `Harness` prefixes).
- `Retract HarnessTranscriptRetraction(HarnessTranscriptToken)` →
  `operation Unwatch(TranscriptToken)`.

### /257 §1.2 — Doubling smell

**Status: PRESENT.** `Assert MessageDelivery(MessageDelivery)`,
`Match HarnessStatusQuery(HarnessStatusQuery)`,
`Subscribe SubscribeHarnessTranscript(SubscribeHarnessTranscript)` —
all three exhibit "verb verb noun" doubling. Fixes named in §1.1.

### /257 §1.4 — Repeated-suffix smell

**Status: PARTIAL.** The 10-variant `HarnessEvent` reply (line
359-370) has clusters worth lifting:

- `HarnessStarted` + `HarnessStopped` + `HarnessCrashed` — three
  lifecycle-event reply variants. These really are independent
  events (clean shutdown vs crash carries different consequences),
  but they share the `Harness*` ancestry and the lifecycle category.
  Could lift to `Lifecycle(LifecycleEvent)` with the three as inner
  variants, OR keep them flat (the discriminator matters at the
  type level).
- `DeliveryCompleted` + `DeliveryFailed` — past-tense pair (success
  + explicit-failure); clean per the convention from /258 §2.6's
  `Launched / LaunchRejected` shape. Keep.
- `HarnessTranscriptSnapshot` + `HarnessSubscriptionRetracted` —
  subscription-lifecycle replies; macro will own these once
  observable + macro fixes land.

Designer lean: lift `*Started / *Stopped / *Crashed` into a single
`Lifecycle(LifecycleEvent)` variant since they share semantics
("the harness transitioned to state X"), with `LifecycleEvent` as
an enum carrying the typed reason / detail.

### /257 §1.5 — Ancestry-prefixed type names

**Status: NOT FIXED.** 14+ types carry the `Harness` prefix despite
the crate name supplying that context. Per ESSENCE §Naming,
inside `signal-persona-harness` the crate IS the ancestry; the
prefix is repetition.

Drops:

| Today | Target |
|---|---|
| `HarnessName` | `Name` (or keep `HarnessName` if used cross-crate as a domain noun; verify) |
| `HarnessStatusQuery` | `StatusQuery` |
| `HarnessStatus` | `Status` |
| `HarnessHealth` | `Health` |
| `HarnessReadiness` | `Readiness` |
| `HarnessStarted` | `Started` (or absorb into `Lifecycle::Started`) |
| `HarnessStopped` | `Stopped` |
| `HarnessCrashed` | `Crashed` |
| `HarnessTranscriptSnapshot` | `TranscriptSnapshot` |
| `HarnessTranscriptToken` | `TranscriptToken` |
| `HarnessTranscriptSequence` | `TranscriptSequence` |
| `HarnessSubscriptionRetracted` | `SubscriptionRetracted` |
| `HarnessOperationKind` | `OperationKind` (macro-emitted once /257 §3.1.2 lands) |
| `HarnessRequestUnimplemented` | `RequestUnimplemented` |
| `HarnessUnimplementedReason` | `UnimplementedReason` |
| `HarnessDaemonConfiguration` | `DaemonConfiguration` |
| `SubscribeHarnessTranscript` | `Subscription` (the verb is `Watch`; payload is the subscription record) |
| `HarnessTranscriptRetraction` | `Unwatch` (the verb-shape close variant) |
| `HarnessTranscriptStream` | `TranscriptStream` |

**Keep** (these name domain concepts, not the crate):

- `HarnessKind` — `Kind` alone is too thin at use sites where
  multiple `*Kind` enums coexist; or it could be just `Kind` inside
  the crate and aliased on import. Borderline; designer lean: keep
  `HarnessKind` because `Kind` is too generic at every reader
  outside this crate.
- `MessageDelivery`, `MessageSender`, `MessageBody`, `MessageSlot`
  — `Message` is the payload-domain noun, not the crate name.
  These are the same types as in `signal-persona-message`; /257
  §1.12 flagged the collision. Designer lean: extract these to
  `signal-persona-types` (or fold into `signal-persona-auth` /
  `signal-persona`) and let both contracts import.
- `TranscriptObservation`, `TranscriptLine` (if exported) — `Transcript`
  is the payload-domain noun. Keep.
- `InteractionPrompt`, `InteractionResolved` — `Interaction` is the
  domain noun. Keep.
- `DeliveryCompleted`, `DeliveryFailed`, `DeliveryCancellation`,
  `DeliveryFailureReason` — `Delivery` is the domain. Keep.

### /257 §1.6 — `*RequestUnimplemented` redundancy

**Status: NOT FIXED + DOUBLE OFFENDER.**
`signal-persona-harness/src/lib.rs:209-213` —

```rust
pub struct HarnessRequestUnimplemented {
    pub harness: HarnessName,
    pub operation: HarnessOperationKind,
    pub reason: HarnessUnimplementedReason,
}
```

Two redundant fields: `operation` (per /257 §1.6 — reply is
positionally aligned with request), and `harness` (the operation
payload already carries the `HarnessName`; same positional argument
once the daemon serves one harness only). Target:

```rust
pub struct RequestUnimplemented {
    pub reason: UnimplementedReason,
}
```

### /257 §1.7 — Empty marker records

**Status: NOT PRESENT.** Verified — no empty `pub struct X {}` in
the contract. ✓

### /257 §1.10 — No observable block

**Status: NOT FIXED.** The `channel Harness { ... }` block has no
`observable { ... }`. Per the
`intent/component-shape.nota` 2026-05-20T02:00:00Z mandate (Tap/Untap
mandatory for persona components) AND the
`intent/persona.nota` 2026-05-21T10:00:00Z reaffirmation (every
persona component including the apex is observable), the harness
channel must add:

```rust
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

### /257 §1.11 — Single-field timestamps

**Status: PRESENT.** `HarnessTranscriptSequence(u64)` and the
`message_slot: MessageSlot(u64)` field are sequence/identity, not
timestamps — fine. But the daemon's wire path through
`persona/src/supervision_readiness.rs` (used by the spawn-envelope
witness via `signal-persona::TimestampNanos`) inherits the
nanosecond-precision issue surfaced in /257 §1.11. Out of scope
for the harness triad; resolves with the workspace-wide timestamp
decision.

### /257 §1.13 — `supervision::` namespace stale

**Status: AFFECTS.** `HarnessDaemonConfiguration` carries
`supervision_socket_path` and `supervision_socket_mode` (line
523-526) inherited from `signal-persona`'s yet-to-be-renamed
`SupervisionProtocolVersion` namespace. Renames when /252 executes.

## 2 · New findings specific to this triad

### 2.1 — Direct in-process terminal library call (the /150 §6.5 blocker)

`persona-harness/src/daemon.rs:392-426` — the `message_delivery_event`
handler, on receipt of `MessageDelivery`, instantiates a
`HarnessTerminalDelivery` and calls `deliver_text` which (via
`persona-harness/src/terminal.rs:147-167`) hand-rolls a
`TerminalTransportBinding::from_socket_path(...).handle_request(binding.input_request(bytes))`
call against the terminal socket. This is a synchronous library
call into `persona-terminal`'s code, NOT a Signal frame round-trip
through `signal-persona-terminal`.

Three concerns:

1. **Bypasses the input gate.** `signal-persona-terminal` carries a
   `TerminalInput` operation with associated guard records
   (per /258's terminal section; verify in
   `signal-persona-terminal/src/lib.rs`). When the harness daemon
   calls `transport.handle_request(...)` in-process, it inherits
   whatever the library-side enforcement is — which is not the
   same as the Signal-frame-mediated gate the router/mind expect
   to police. The "no direct string injection path that bypasses
   router/terminal guards" line in /150 §6.5 is exactly about this.
2. **Skips the typed-reply wire shape.** The handler unwraps a
   `TerminalReply::TerminalInputAccepted` (terminal.rs:158) — a
   typed wire reply — out of an in-process library call. Means
   the executor / observer projection for the cross-component
   `EffectEmitted` event never fires; persona-introspect can't
   observe this delivery as a typed terminal operation, only as a
   harness-local effect.
3. **Violates the daemon-as-Signal-client shape.** Per
   `skills/component-triad.md` §"A daemon may be a Signal client
   of any number of peer daemons", composing daemons is done by
   speaking Signal to peers. The harness daemon should open a
   client connection to `persona-terminal`'s socket and send a
   `signal-persona-terminal::TerminalInput` operation frame.

The harness daemon should be `persona-terminal`'s Signal client for
the input plane. ARCH §1 calls the in-process adapter
"transitional"; /150 confirms it must retire.

### 2.2 — Daemon hand-parses flags AND reads environment variables

`persona-harness/src/daemon.rs:531-587` —

```rust
match argument.to_string_lossy().as_ref() {
    "--socket" => ...,
    "--harness" => ...,
    "--kind" => ...,
    "--terminal-socket" => ...,
    ...
}
```

And env vars at line 184 (`PERSONA_HARNESS_TERMINAL_SOCKET`) and
line 199 (`PERSONA_SOCKET_MODE`).

Both violate the universal argument rule (`skills/component-triad.md`
§"The single argument rule"). The typed
`HarnessDaemonConfiguration` path in
`persona-harness/src/main.rs:11-13` exists — it should be the
sole path. The legacy `--socket --harness --kind --terminal-socket`
plus env-var fallback retires.

### 2.3 — No separate thin CLI binary

Per the CLI Decision at
`intent/component-shape.nota` 2026-05-20T13:00:00Z (CLI binary
name = daemon name minus `-daemon`), the harness should ship
two binaries:

- `persona-harness-daemon` (the long-lived process).
- `harness` (the thin client — single NOTA-or-path argument,
  no flags, generated socket dispatch per /129).

Today there is one binary that branches on argv[0] shape
(`main.rs:18-31` checks if first arg starts with `(` or has
`.nota`/`.rkyv` extension). The thin CLI is missing.

### 2.4 — `persona-harness` daemon does not use `signal-executor`

Same gap as /258 §2.2 for engine-manager. Verified via
`Cargo.toml`: depends on `signal-core` (line 24), not
`signal-frame` and not `signal-executor`. Verified via grep: no
`signal_executor::` imports, no `Lowering for` impls, no
`CommandExecutor for` impls.

The request path
(`persona-harness/src/daemon.rs:166-181, 360-477`) directly
dispatches via the Kameo actor mesh:

- `HarnessRequestHandler::event_for_request` (line 377-390) does a
  big `match request` and returns a `HarnessEvent`.
- No typed `Command` / `Effect` enum decoupled from the contract.
- No `OperationPlan<Command>` shape.
- No `OperationReceived` / `EffectEmitted` projection.

The migration is structurally identical to spirit's (and the
engine-manager triad's pending equivalent per /258 §2.2): wrap the
actor mesh behind a `CommandExecutor` impl, define `HarnessCommand`
/ `HarnessEffect` enums, implement `Lowering`, route the request
through `signal_executor::Executor::execute`.

### 2.5 — `HarnessOperationKind` is hand-maintained AND mirrored downstream

`signal-persona-harness/src/lib.rs:152-162` declares
`HarnessOperationKind` by hand; `lib.rs:383-396` matches it by
hand against every request variant; `persona/src/engine_event.rs`
re-exports it. Per /257 §3.1.2, the macro should generate this.

### 2.6 — Hand-written `From<Payload> for HarnessEvent` impls

`signal-persona-harness/src/lib.rs:399-488` — 17 hand-rolled
`From<Payload> for Reply` impls (10 for `HarnessEvent`, 6 for
`HarnessRequest`, 1 for `HarnessStreamEvent`). Per
`intent/component-shape.nota` 2026-05-21T01:15:44+02:00 the macro
should auto-generate these. Retires when the macro fix lands.

### 2.7 — `HarnessDaemonConfiguration.harness_kind: HarnessKind` and the daemon-local `HarnessKind`

The signal contract defines `HarnessKind` (line 501-509:
`Codex / Claude / Pi / Fixture`), and the daemon imports it
(`persona-harness/src/lib.rs:16` re-exports a daemon-local
`HarnessKind`), with a `HarnessKind::from_contract(...)`
conversion (`daemon.rs:49`). Two `HarnessKind` types — one in the
contract, one in the runtime — converted across the boundary.

Looks defensible IF the runtime needs richer state on the kind
(e.g., adapter behavior dispatched on it). But verify the runtime
version (`harness.rs:HarnessKind`) actually adds capability; if it
mirrors the contract enum without adding behavior, retire the
runtime version and use the contract type directly.

### 2.8 — `persona-harness/CLAUDE.md` references stale `signal-core`

Same kind of substrate-doc gap as /258 §2.5; verifies via Cargo.toml
that this triad's whole stack is still on `signal-core` rather
than the workspace-current `signal-frame` + `signal-executor` +
`signal-sema`. The whole triad is pre-migration.

## 3 · Proposed owner signal (`owner-signal-persona-harness`)

### Why it must exist

`skills/component-triad.md` §"Two authority tiers — both part of
the triad" — a daemon with only the ordinary signal surface "is
not yet triad-shaped". The intent-log basis is
`intent/component-shape.nota` 2026-05-18T22:15:57Z (*"owner-signal-
<component> is part of the triad, not a follow-up arc"*), softened
slightly by 2026-05-19T20:30:00Z (*"the 5 missing owner-signal-
persona-* repos … are intentionally missing — moving fast; the
owner-signal pattern is recent. Don't backfill them by assumption;
let them emerge as each component's owner discipline crystallizes"*).

The harness's owner discipline crystallizes around three areas:

1. **Daemon lifecycle**: Start (with generation), Drain (graceful
   stop), Reload (re-read bootstrap-policy), Retire (final stop +
   tombstone). Mirrors `owner-signal-persona-spirit` exactly.
2. **Terminal-endpoint policy**: GrantTerminalEndpoint and
   RevokeTerminalEndpoint — the harness's connection to its
   downstream terminal is policy-controlled by the owner
   (orchestrate, per the workspace's authority chain
   `skills/component-triad.md` §"Authority chain — worked example").
3. **Harness-kind binding**: ConfigureKind — the runtime variant
   binding (`Codex`/`Claude`/`Pi`/`Fixture`). Today this is
   passed once in the spawn envelope at boot; an owner-mutate path
   lets orchestrate re-bind a generic harness slot to a different
   kind without a full daemon restart.

The authority surface above the harness daemon is
`persona-orchestrate` (per `skills/component-triad.md`'s
canonical chain *"orchestrate owns router and harness"*); so the
caller of `owner-signal-persona-harness` is orchestrate.

### Operation roots + payload sketches

Conservative shape — mirrors `owner-signal-persona-spirit`'s seven
operations (Start / Drain / Reload / Register / Retire) plus the
two harness-specific surfaces (terminal-endpoint grant/revoke,
kind binding):

```text
channel OwnerHarness {
    operation Start(Start),
    operation Drain(Drain),
    operation Reload(BootstrapPolicy),
    operation Retire(Retirement),
    operation GrantTerminalEndpoint(TerminalEndpointGrant),
    operation RevokeTerminalEndpoint(TerminalEndpointRevocation),
    operation ConfigureKind(KindConfiguration),
}
```

Payload sketches (positional NOTA records, no labels per the NOTA
discipline; types named per the no-ancestry rule — these live
inside `owner-signal-persona-harness` so no `Harness*` prefix):

```text
Start(Generation)                       // owner orders daemon to enter Running.
Drain                                   // graceful stop; no payload.
BootstrapPolicy                         // re-read bootstrap-policy.nota.
Retirement(IdentityName)                // final stop with name witness.

TerminalEndpointGrant(WirePath)         // owner grants this harness the right
                                        // to deliver into the terminal at
                                        // this socket path.

TerminalEndpointRevocation              // owner revokes terminal access; harness
                                        // continues to run but cannot deliver.

KindConfiguration(HarnessKind)          // owner rebinds the harness's runtime
                                        // variant (Codex / Claude / Pi / Fixture).
```

`IdentityName` and `Generation` mirror the spirit owner contract's
naming. The single-argument NOTA rule means each operation root
carries one positional payload — even when that payload is just an
enum or a transparent newtype.

### Reply variants

Past-tense + explicit-rejection pattern, per the workspace
convention (`*ed` for success, `*Rejected` for typed failure,
plus `RequestUnimplemented` for not-yet-built):

```text
reply Reply {
    Started(Started),                          // generation acknowledged
    DrainedAndStopped(DrainedAndStopped),      // graceful stop complete
    BootstrapPolicyReloaded(BootstrapPolicyReloaded),
    Retired(Retired),
    TerminalEndpointGranted(TerminalEndpointGranted),
    TerminalEndpointRevoked(TerminalEndpointRevoked),
    KindConfigured(KindConfigured),
    Rejected(OrderRejection),                  // typed per-operation failure
    RequestUnimplemented(RequestUnimplemented),
}
```

Payload sketches for the new replies:

```text
TerminalEndpointGranted(WirePath)                  // confirms the path now bound.
TerminalEndpointRevoked                            // confirms revocation.
KindConfigured(HarnessKind)                        // confirms the new kind.

OrderRejection(OperationKind, OrderRejectionReason)
                                                   // typed failure with operation
                                                   // tag + reason variant. Cleaner
                                                   // than the doubled-operation
                                                   // /257 §1.6 pattern because
                                                   // here the rejection sits OUT
                                                   // of the positional reply
                                                   // alignment and needs the tag.

OrderRejectionReason :=
    HarnessNotRunning
    | TerminalEndpointInvalid
    | TerminalEndpointAlreadyBound
    | KindMismatch
    | OwnerAuthorityNotRecognised
```

`RequestUnimplemented` per /257 §1.6 carries only the reason:

```text
RequestUnimplemented(UnimplementedReason)

UnimplementedReason :=
    NotBuiltYet
    | DependencyNotReady
    | PolicyStoreUnavailable
```

### Bootstrap-policy file

Per `skills/component-triad.md` §5 ("Policy state ... first-start
population: from `bootstrap-policy.nota` in the component's
repo"), the harness daemon's first start reads
`persona-harness/bootstrap-policy.nota` carrying the initial
terminal-endpoint grant (if any) and the kind binding. Subsequent
changes go only through owner Mutate (i.e., through this owner
contract).

Sketch — positional NOTA, no labels:

```text
(BootstrapPolicy
    (KindConfiguration Codex)
    (TerminalEndpointGrant "/run/persona/terminal-claude.sock"))
```

### Conservative posture

What this proposal does NOT do:

- Does NOT add observability verbs (Tap/Untap) here. The
  observability surface lives on the ordinary contract per the
  2026-05-19T20:00:00Z Decision (*"Subscribing to that hook is done
  on the daemon's normal (public) socket, not the owner socket"*).
- Does NOT carry the harness's working-side operations
  (MessageDelivery / InteractionPrompt / Subscribe). Those stay in
  the working signal.
- Does NOT settle whether `ConfigureKind` is the right shape — the
  current code passes kind through the spawn envelope at boot. If
  the workspace decides re-binding is out of scope, drop
  `ConfigureKind` and let `Retire` + spawn-fresh be the only path.
  Conservative posture: include `ConfigureKind` but flag it as the
  most speculative root in this proposal (psyche call).
- Does NOT mint new lifecycle verbs beyond
  `Start / Drain / Reload / Retire`. The spirit owner contract's
  shape is the canonical reference; harness inherits unchanged.

### Open question on this proposal

Is the terminal-endpoint binding really owner-policy, or is it
working-signal (orchestrate's working-channel order to the harness
daemon)? Argument for owner: terminal access is the harness's
authority surface and survives across restarts (policy state).
Argument for working: the bind/unbind is operational, not "policy"
in the Bhagavad-Gita-foundational sense. The conservative posture
above puts it in owner because filesystem-permission enforcement
(per `skills/component-triad.md` §4) is the right gate for "who
can tell the harness to talk to which terminal" — and that is
exactly what owner-only sockets enforce.

## 4 · Recommended next slice

In priority order, scoped to the persona-harness triad. Each item
is structurally identical to a step the spirit migration already
took (/255 + /256); cross-reference there for the worked pattern.

1. **Land `owner-signal-persona-harness`** per §3. Repository
   creation needed (per `intent/component-shape.nota`
   2026-05-19T20:00:00Z, psyche authorized creating signal-frame /
   signal-sema repos; the owner-signal-persona-harness creation
   needs the same psyche approval before the operator runs it).
2. **Migrate `signal-persona-harness` to `signal-frame`** +
   contract-local verbs per §1's renames. Drop the universal-verb
   prefixes; lift the doubled `HarnessStatusQuery /
   SubscribeHarnessTranscript / MessageDelivery` to verb-form
   contract-local operations.
3. **Drop `Harness*` ancestry prefixes** per §1.5 (~14+ types).
4. **Add observable block** to the working contract per §1.10 +
   `intent/persona.nota` 2026-05-21T10:00:00Z.
5. **Drop `*RequestUnimplemented.harness` and `.operation`** per
   §1.6 (double-redundancy here).
6. **Migrate `persona-harness` daemon to `signal-executor`** per
   §2.4. This is the structural change that brings parity with
   spirit (`786ab311`).
7. **Retire flag-style argv parsing + env-var reads** per §2.2.
   Single typed-NOTA-config path only.
8. **Split out a separate thin CLI binary** (`harness`) per §2.3
   and the 2026-05-20T13:00:00Z naming Decision. Use the generated
   signal_cli! dispatch macro per /129.
9. **Retire the direct terminal-library call** per §2.1. The
   harness daemon becomes `persona-terminal`'s Signal client; the
   input plane goes over `signal-persona-terminal` typed frames.
   This is the load-bearing /150 §6.5 fix.

Steps 1–5 are mechanical contract / daemon edits. Step 6 is the
significant structural change. Steps 7–8 are daemon cleanup. Step
9 is the architecturally important cross-component wiring that
restores the router/terminal guard chain.

## 5 · References

- `/150` — operator triad signal/sema migration current state;
  §6.5 names the *"NO direct string injection path that bypasses
  router/terminal guards"* requirement load-bearing for this audit.
- `/255`, `/256` — spirit migration template (the harness triad
  should follow the same shape).
- `/257` — workspace-wide signal contract name/shape audit;
  signal-persona-harness is listed in the "still on `signal-core`"
  half.
- `/258` — engine-manager triad audit, structurally identical
  shape to this one.
- `/129` — `signal_cli!` macro sketch for two-socket CLI dispatch.
- `/100` — recent designer-assistant review of operator/144 on the
  signal-sema-executor refresh.
- `intent/component-shape.nota` 2026-05-18T22:15:57Z (owner-signal
  ships with ordinary, not a follow-up arc), 2026-05-19T20:30:00Z
  (intentionally-missing owner repos), 2026-05-20T02:00:00Z
  (Tap/Untap mandatory), 2026-05-20T12:11:26Z (every stateful
  component has an owner contract), 2026-05-20T13:00:00Z (CLI =
  daemon name minus `-daemon`), 2026-05-21T10:30:00Z (modules-not-
  options for macro disambiguation).
- `intent/persona.nota` 2026-05-21T10:00:00Z (every persona
  component is observable, including the apex).
- `intent/signal.nota` 2026-05-20T17:30:00Z (CLI socket dispatch
  Correction).
- `skills/component-triad.md` (the canonical invariants).
- `skills/naming.md` (the two paired naming rules).
- `protocols/active-repositories.md` (persona-harness =
  "Harness process/session control boundary").
- `owner-signal-persona-spirit/src/lib.rs:104-121` (canonical
  template the owner-signal-persona-harness proposal mirrors).
- `owner-signal-persona-router/src/lib.rs:270-307` (second
  template, used for the typed-rejection-with-OperationKind shape
  carried into the OrderRejection proposal here).
- Code under audit:
  `signal-persona-harness/src/lib.rs` (530 lines),
  `persona-harness/src/daemon.rs`, `persona-harness/src/terminal.rs`,
  `persona-harness/src/main.rs`, `persona-harness/Cargo.toml`,
  `persona-harness/ARCHITECTURE.md`,
  `persona-harness/skills.md`,
  `persona-harness/AGENTS.md`.

This report retires when (a) `owner-signal-persona-harness` is
created with substance close to §3, AND `signal-persona-harness`
+ `persona-harness` follow the spirit migration template, OR (b)
a successor audit supersedes.
