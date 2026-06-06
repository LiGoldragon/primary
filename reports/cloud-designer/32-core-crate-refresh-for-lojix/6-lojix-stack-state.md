# lojix stack state — hand-written vs newly-generated/hosted, for the core-crate refresh

Survey of the CURRENT new lojix stack (`/git/github.com/LiGoldragon/lojix/triad-port`
and the two contract `triad-port/` dirs) against the LATEST core-crate HEADs, to scope
the re-alignment. lojix is M1-done and sits exactly on the drift baseline; the core
crates have moved decisively underneath it in the last 24h.

## 0 · Drift baseline confirmed, and the headline

lojix's `triad-port/Cargo.lock` pins exactly the task's baseline:

| crate | lojix pins | core HEAD (2026-06-06) | moved? |
|---|---|---|---|
| schema-rust-next | `c0a331a` | `6685e7b` | YES — daemon emitter + ConnectionContext landed |
| triad-runtime | `fdfd1831` | `33b9531` | YES — `DaemonConfiguration` + `ExitReport` + `ConnectionContext` |
| nota-next | `fb600e3` | `f0e435a` | minor (`#[shape(keyword=…)]` derive) |
| nota-codec | `f761421` | `24e7823` | docs/intent only |
| nota-config | `bd9173a` | `bd9173a` | none |

The two contracts (`signal-lojix`, `meta-signal-lojix`) pin schema-rust-next `ec0678c`
(`emit triad role trait impls`) — a THIRD rev, divergent from lojix's `c0a331a` and from
HEAD, but both `c0a331a` and `ec0678c` are ancestors of HEAD, so the whole stack can
move forward to the daemon-emitter HEAD on one linear bump.

**Headline:** schema-rust-next HEAD now EMITS an entire per-component daemon module
(`schema-rust-next/src/daemon_emit.rs`, 979 lines, landed `33337d7` 2026-06-06):
`ComponentDaemon` hook trait, `DaemonCommand` argv parsing, `GeneratedDaemonRuntime`
decode→execute→encode spine, single/multi listener selection, `DaemonError`,
`DaemonEntry::run_to_exit_code`, and option-B streaming. triad-runtime HEAD provides the
matching `DaemonConfiguration` trait + `ExitReport` + `ConnectionContext`
(`triad-runtime/src/process.rs`). lojix HAND-WROTE every one of these in `daemon.rs`
(276 lines) and `bin/lojix-daemon.rs`. The hand-written daemon is now almost entirely a
candidate for replacement by the generated one — with two load-bearing caveats below.

## 1 · What lojix hand-wrote that the core crates would now GENERATE or HOST

### 1.1 The daemon loop / `MultiListenerRuntime` impl — GENERATED now (must-port, with a concurrency caveat)

`daemon.rs:121-166` is `LojixRuntime` implementing `triad_runtime::MultiListenerRuntime`
over a two-socket `MultiListenerDaemon` (`daemon.rs:70-81`). The generated
`GeneratedDaemonRuntime<Daemon>` (`daemon_emit.rs:829-859`) is exactly this: it owns the
engine, implements `MultiListenerRuntime` (`daemon_emit.rs:769-795`) with a
`ListenerTier { Working, Meta }` enum (`daemon_emit.rs:866-890`) that is the structural
twin of lojix's hand-rolled `ListenerRole { Ordinary, Owner }` (`daemon.rs:40-53`), and a
`handle_working_stream` (`daemon_emit.rs:834-852`) that IS the decode→execute→encode spine
lojix hand-wrote as `RequestWorker::serve_ordinary` (`daemon.rs:189-199`).

Coupling: the loop is GENERIC. Nothing in lojix's loop is lojix-specific except (a) the
two-tier role split — which the emitter handles natively via `NexusDaemonShape` +
`with_meta_tier` (`daemon_emit.rs:44-72`), and (b) the per-request engine construction,
which moves into the `build_runtime` hook.

**CAVEAT — concurrency regression.** This is the single most important finding for the
port. lojix's `LojixRuntime::handle_stream` (`daemon.rs:151-165`) does NOT serve inline:
it offloads each connection onto a shared `triad_runtime::BoundedWorkers` pool
(`daemon.rs:158-164`) and returns immediately, so the accept loop stays responsive on
both sockets while a multi-minute `nix` build runs. That is the M1 concurrency win
(intent 2alg/k6w1: a query answered in ~4ms during a deploy). The GENERATED
`GeneratedDaemonRuntime::handle_stream` (`daemon_emit.rs:781-794`) runs the work
SYNCHRONOUSLY — it calls `self.handle_working_stream(stream)` inline. And
`MultiListenerDaemon::serve_streams` calls `runtime.handle_stream(...)` inline in the
accept loop (`triad-runtime/src/daemon.rs:368-377`). So adopting the generated daemon
AS-IS would REGRESS lojix to a serial daemon — a long deploy would block every query and
the other socket. The generated daemon has no `BoundedWorkers` offload anywhere.

Conclusion: the daemon loop is a must-port, but it is BLOCKED on the generated daemon
gaining a concurrency story (offload `handle_working_stream` onto `BoundedWorkers`, or a
hook that lets the component wrap the worker dispatch). This is the most important thing
to raise upstream with schema-rust-next / triad-runtime before lojix throws away its
hand-written concurrent loop. Until then, lojix must KEEP its hand-written daemon or
upstream the offload first.

### 1.2 `DaemonConfiguration` — now a triad-runtime TRAIT, lojix has a struct of the same name (small, must-align)

lojix hand-wrote `DaemonConfiguration` as a STRUCT (`lib.rs:94-100`): four fields
(`ordinary_socket_path`, `ordinary_socket_mode`, `owner_socket_path`,
`owner_socket_mode`), `NotaRecord` + rkyv + `impl_rkyv_configuration!`. triad-runtime HEAD
now defines `DaemonConfiguration` as a TRAIT (`process.rs:90-117`): `socket_path()`,
`meta_socket_path() -> Option`, `database_path()`, `trace_socket_path() -> Option`,
`meta_socket_mode() -> Option<SocketMode>`. The generated `ComponentDaemon` requires
`type Configuration: DaemonConfiguration` (`daemon_emit.rs:379`).

Name collision, but compatible shapes: lojix's struct maps cleanly onto the trait
(`ordinary_socket_path` → `socket_path`, `owner_socket_path`/`owner_socket_mode` →
`meta_socket_path`/`meta_socket_mode`). Gap: lojix's config has NO `database_path` because
its `Store` is in-memory `Mutex` tables (`lib.rs:166-185`) — the trait REQUIRES
`database_path()`. So aligning means adding a `database_path` field (even if unused until
sema-engine/redb lands) and implementing the trait. Coupling: GENERIC; this is plumbing.
The fields are renamed but the authority-tier semantics are preserved by the trait's
`socket` (working) vs `meta_socket` (owner) split.

### 1.3 Socket wiring + owner-mode validation — GENERATED bind, but lojix's security guard must move into config (small)

`daemon.rs:67-104` hand-wires the two `ListenerSocket`s with their modes, and
`validate_owner_socket_mode` (`daemon.rs:99-104`) refuses an owner mode granting
other-access (audit R3). The generated `DaemonBinder::bind` (`daemon_emit.rs:498-522`)
builds the same two `ListenerSocket`s from the configuration's `socket_path()` /
`meta_socket_path()` / `meta_socket_mode()`, applying the schema-declared
`MetaListenerTier::socket_mode()` as the default. The generated bind does NOT carry
lojix's reject-insecure-owner-mode guard. So porting means re-expressing
`InsecureOwnerSocketMode` (`lib.rs:60-61`, `daemon.rs:99-104`) inside the
`DaemonConfiguration` impl or `build_runtime`, not on the loop. Coupling: the guard is
mildly lojix-specific (it encodes the no-peer-cred-yet authority model), but the bind
itself is generic.

### 1.4 Per-request engine plumbing — moves to `build_runtime` + the engine becomes long-lived (medium, semantics shift)

lojix builds a FRESH `SchemaRuntime` per request over a shared `Arc<Store>`
(`daemon.rs:158-161, 215-231`; `schema_runtime.rs:324-330`). The generated daemon builds
the engine ONCE in `build_runtime` (`daemon_emit.rs:391, 502-503`) and the
`GeneratedDaemonRuntime` holds it for the daemon's whole life — `handle_working_input`
takes `&Self::Engine` (`daemon_emit.rs:412`), an immutable borrow shared across calls.

This is a real semantics shift, not just plumbing. lojix's per-request `SchemaRuntime`
carries MUTABLE in-flight pipeline cursor state (`active_deploy`, `active_operation` —
`schema_runtime.rs:26-34`) that MUST stay per-request (intent 2alg: concurrent deploys
must not corrupt each other's cursor). The generated `&Engine` is shared and immutable.
So the port cannot simply make `SchemaRuntime` the `Engine`: the long-lived `Engine` must
hold only the shared `Arc<Store>`, and the per-request mutable cursor must be created
INSIDE `handle_working_input` (the engine builds a fresh `SchemaRuntime` per call, exactly
as the daemon does today, just relocated). This is doable but is the part that needs
care — and it interacts with the §1.1 concurrency caveat (if the generated spine is
serial, the per-request isolation is moot but the responsiveness is lost).

### 1.5 The frame codec usage — GENERATED (small, free win)

lojix hand-uses `LengthPrefixedCodec` with an 8 MiB `MaximumFrameLength` (`daemon.rs:25,
131`; audit R1 bounds a hostile prefix) and a 10s read timeout (`daemon.rs:30, 190, 202`;
audit R2). The generated spine uses a `WorkingTransport` (`daemon_emit.rs:836`) that owns
read/write framing. The audit-R1/R2 hardening (max frame + read timeout) is lojix-specific
hardening that the generated `WorkingTransport` may or may not carry — must verify the
generated transport's bounds match lojix's R1/R2 before trusting the port. Coupling:
generic, but the specific bounds are lojix security decisions worth preserving.

### 1.6 `ConnectionContext` / peer-auth — NEWLY HOSTED, and it fills a KNOWN lojix gap (medium, high-value)

This is the freshest core development (triad-runtime `33b9531` + schema-rust-next
`6685e7b`, both 2026-06-06). `ConnectionContext` (`process.rs:31-79`) carries the
kernel-vouched `SO_PEERCRED` triple (uid/gid/pid via `rustix::net::sockopt::socket_peercred`,
no unsafe), and the generated spine threads `&ConnectionContext` into
`handle_working_input` (`daemon_emit.rs:412`, `daemon_emit.rs:843-849`) so a component can
mint an origin from the OS trust boundary rather than trusting payload claims.

This DIRECTLY addresses lojix's audit R3 (`daemon.rs:96-98`): lojix today rests the owner
tier's authority ENTIRELY on the socket file mode, with NO peer-credential check, and the
hand-written daemon has no access to peer creds at all. `ConnectionContext` is the
upstream-hosted primitive that lets lojix do a real owner-tier peer-credential check
(e.g. require uid in the cluster-operator group). High value, but see §3: the META tier in
the generated daemon is a full escape hatch (`handle_meta_stream`), so lojix would thread
`ConnectionContext::from_stream` itself on the owner socket — the generated auto-threading
only covers the WORKING tier.

### 1.7 The per-crate `Error` enum + `Result` — partially SUBSUMED (small)

lojix hand-wrote a `thiserror` `Error` (`lib.rs:28-86`) and `Result` (`lib.rs:88`). The
generated daemon emits its OWN `DaemonError<Daemon>` (`daemon_emit.rs:940`) and requires
the component's `type Error: Display + From<FrameError> + From<SignalFrameError> +
From<ListenerError>` (`daemon_emit.rs:382`). lojix's `Error` already has `From<FrameError>`
(`lib.rs:42-43`) and `From<SignalFrameError>` via the named variants, but would need to add
`From<ListenerError>` and possibly drop variants now owned by `DaemonError`
(`ExpectedSingleArgument`, `FlagArgument`, argv handling — `lib.rs:51-55` — are now in
`DaemonCommand`). Coupling: generic; small surface trim.

### 1.8 The `bin/lojix-daemon.rs` entry — GENERATED via `DaemonEntry::run_to_exit_code` (small)

lojix's daemon bin (`bin/lojix-daemon.rs`) hand-decodes config and calls
`Daemon::new(configuration).run()`, hand-mapping errors to exit code 2. The generated
`DaemonEntry::run_to_exit_code` (`daemon_emit.rs:975`) + `ExitReport`
(`process.rs:119-154`) is exactly this component-agnostic tail. Trivial replacement.

## 2 · What is genuinely lojix-specific and STAYS hand-written regardless

These are NOT candidates for generation; they are the component's reason to exist and the
emitter explicitly leaves them as `ComponentDaemon` escape hatches (record 1488).

- **The nix effect plane.** `schema_runtime.rs:1150-1416` — `NixCommand` (the typed
  `nix`/`ssh` invocation noun) and the seven `run_*` effect methods doing real
  `std::process::Command` IO. This is the Nexus side's real-world effect plane; the
  emitter never generates effect bodies (it generates the `EffectCommand`/`EffectResult`
  CATALOG types in `nexus.rs:122-168`, which lojix already checks in). MUST stay.
- **The deploy pipeline routing.** `schema_runtime.rs:350-783` — `decide_*`,
  `DeployPipeline`, `DeployStage`, `DeployAction`, the effect-continuation chain, and the
  M1 reject-guard (`unsupported_deploy_reason`, `schema_runtime.rs:448-464`). This is the
  hand-written `NexusEngine::decide` brain. The emitter generates the `NexusEngine` TRAIT
  + the `Runner` driver (`nexus.rs:1233-1320`) but NOT `decide` — that is the whole point
  of a hand-written runtime. MUST stay.
- **The `Store` semantics.** `lib.rs:104-185` + `schema_runtime.rs:787-1148` — the four
  `Mutex`-backed tables, the sequence counters, and the `apply_sema`/`observe_sema` table
  logic implementing `SemaEngine`. The emitter generates the `SemaEngine` trait + the
  sema table RECORD types (`schema/sema.rs`) but not the table mutation logic. MUST stay
  (and is destined to migrate to sema-engine/redb, an independent follow-on — see §4).
- **The owner-tier `handle_meta_stream` body.** Because the generated daemon treats the
  meta tier as a full escape hatch (§3), the owner socket's read/decode/route/encode
  (lojix's `serve_owner`, `daemon.rs:201-210`) stays hand-written even after the port.

## 3 · Does the schema declare a daemon / streaming / ConnectionContext? (question d)

**No schema-file change is required to adopt the generated daemon; a `build.rs` change is.**
The daemon emitter is turned ON not by a `.schema` declaration but by adding a
`ModuleEmission::daemon_module("lib", NexusDaemonShape::new(PROCESS_NAME,
WorkingListenerTier::new("signal_lojix::schema::lib")).with_meta_tier(MetaListenerTier
…))` to the build plan (`build.rs:125-136`). The `NexusDaemonShape` reads the EXISTING
working-contract module's schema; it does not require new schema records. lojix's current
`build.rs` (`triad-port/build.rs:28, 77`) uses `GenerationPlan::daemon_runtime` which emits
only `nexus` + `sema` runtime modules (`schema-rust-next/src/build.rs:44-52`) and NO
daemon module — so adopting the generated daemon is a build-plan addition, not a schema
edit. The env var driving regen is `LOJIX_UPDATE_SCHEMA_ARTIFACTS` (`build.rs:36`); the
checked-in `src/schema/*.rs` is in sync under the current pinned emitter (clean working
tree, `// @generated by schema-rust-next` header present).

**Streaming: the contract deliberately declares NO stream, so the streaming emitter is
OFF.** `signal-lojix/triad-port/schema/lib.schema:12-15` explicitly documents: "no
event/stream root, no opens/belongs … the Watch/Unwatch SUBSCRIPTION HANDSHAKE is
authored in the emittable form (ordinary request → SubscriptionToken)". So
`emits_stream: false`, and the generated daemon would NOT carry the option-B
registry/publish wiring (`daemon_emit.rs:319-365` are all gated on `emits_stream`).
lojix's push-not-pull subscription delivery (ARCHITECTURE.md §"Push, never poll") is
therefore NOT something the latest emitter would auto-generate — it would require the
CONTRACT schema to add a real `(Stream { … })` declaration first (cf. the
`daemon-stream.schema` fixture, `IntentEventStream (Stream {…})`). Today lojix's
`open_subscription`/`close_subscription` (`schema_runtime.rs:374-395`) just hand the token
back; no events are pushed. This is a deferred-feature alignment, not a refresh gap.

**ConnectionContext is hosted, not schema-declared.** It is threaded automatically into the
WORKING tier only (`daemon_emit.rs:412`); the META/owner tier is a full escape hatch
(`handle_meta_stream`, `daemon_emit.rs:343`, `daemon_emit.rs:790`) so lojix would call
`ConnectionContext::from_stream` itself for owner peer-auth.

## 4 · The contracts (signal-lojix / meta-signal-lojix) triad-port

Both contracts emit a single `lib` wire-contract module (`signal-lojix/triad-port/build.rs:23`
→ `GenerationPlan::wire_contract`). They pin schema-rust-next `ec0678c` (`emit triad role
trait impls`), one rev-line ahead of lojix's `c0a331a` on a divergent branch; both are
ancestors of HEAD. Bumping the contracts to the daemon-emitter HEAD would re-emit their
`src/schema/lib.rs` through the newer wire-contract path (the `799f678` "emit the basic
frame codec for wire-facing targets" fix and the Plane-token/tokenization chain
`e332b5e`..`9ca8754` all touch wire-contract emission), so the contracts' generated code
WILL change on the bump — verify the re-emit is clean (`*_UPDATE_SCHEMA_ARTIFACTS`) and
that the `encode/decode_signal_frame` surface lojix's daemon/client depend on is stable.

One known contract-level wart, independent of the refresh: the two contracts' short-header
ordinals COLLIDE (meta `Deploy` == ordinary `Query` == 0x0), so the client's tier
disambiguation (`client.rs:77-91`) relies on rkyv layout divergence, not a structural tier
discriminator (audit R7). The proper fix (a tier bit in the short header) is upstream of
lojix in signal-frame/schema-rust-next; worth flagging in the synthesis as a contract-side
item the refresh could carry.

## 5 · Port/adopt/align recommendations (must-port vs nice-to-have)

### MUST-PORT (the refresh's core re-alignment)

1. **Adopt the generated daemon module — BUT only after the generated spine gains a
   concurrency story.** (large; risk: HIGH) Replacing `daemon.rs`'s `LojixRuntime` with
   `impl ComponentDaemon for Lojix` + `ModuleEmission::daemon_module` collapses
   §1.1–1.3, 1.5, 1.7, 1.8 into ~one `impl` block. BUT the generated
   `handle_working_stream` is SYNCHRONOUS (`daemon_emit.rs:781-794`), so a naive port
   REGRESSES the M1 concurrency win. Resolve the §1.1 caveat first (upstream a
   `BoundedWorkers` offload into the generated spine, or keep the hand-written loop and
   adopt only the hook trait + config trait). Do NOT port the loop blindly.

2. **Align `DaemonConfiguration` to the triad-runtime trait.** (small; risk: low) Rename
   fields to the trait's `socket`/`meta_socket` vocabulary, add `database_path` (even if
   unused pre-redb), and `impl DaemonConfiguration`. Re-express the
   `InsecureOwnerSocketMode` guard (§1.3) in the impl, not the loop.

3. **Thread `ConnectionContext` for owner-tier peer-auth (audit R3 fix).** (medium; risk:
   medium) Use `ConnectionContext::from_stream` on the owner socket to require a
   cluster-operator uid/gid, closing the "authority rests entirely on socket file mode"
   gap. On the working tier the generated spine threads it for free; on the owner tier
   (escape hatch) lojix calls it itself.

### NICE-TO-HAVE / DEFERRED

4. **Bump the contracts to the daemon-emitter HEAD and re-emit.** (small; risk: low-medium)
   Unifies all three repos on one emitter rev; re-emits contract `src/schema/lib.rs`
   through the newer wire-contract path. Verify clean re-emit + stable
   `encode/decode_signal_frame`.

5. **Defer the push-not-pull subscription delivery to a CONTRACT schema stream.** (large;
   risk: medium) The latest emitter generates option-B publish/subscribe ONLY when the
   contract declares a `(Stream {…})`. lojix's ARCHITECTURE promises push events but the
   contract deliberately omits a stream root. To get GENERATED subscription wiring, add a
   stream to `signal-lojix/lib.schema` first; otherwise the hand-rolled token handshake
   stays. This is feature work, not refresh drift.

6. **Trim argv/flag `Error` variants now owned by `DaemonCommand`.** (small; risk: low)
   Once the generated daemon owns argv, drop `ExpectedSingleArgument`/`FlagArgument` from
   lojix's `Error` (`lib.rs:51-55`).

### EXPLICITLY NOT APPLICABLE

- **sema-engine `e1aeef1` "add identified mutation"** — does NOT bear on lojix today.
  lojix's `Store` is in-memory `Mutex` tables (`lib.rs:166-185`) and does NOT depend on
  sema-engine at all (it is not in `Cargo.toml`). The redb/sema-engine migration is a
  named follow-on (`lib.rs:10-12, 162-165`); sema-engine HEAD movement matters only when
  that migration starts, not for the current refresh.
- **nota-codec `24e7823` / nota-config (unchanged)** — docs/intent only; no code bearing.
- **nota-next `f0e435a` (`#[shape(keyword=…)]`)** — a new derive shape on nota-next; lojix's
  generated code uses `NotaDecode`/`NotaEncode` derives (`nexus.rs:27-32`) and does not
  consume the new keyword-node shape; no action unless a future schema feature needs it.
