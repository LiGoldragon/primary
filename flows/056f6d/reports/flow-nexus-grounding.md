# Flow Nexus grounding — what it is today, from sources

Method: read of three repositories at recorded revisions, read of the deployed
binaries' own usage text and of the live process/socket/unit state, and three
read-only `flow resolve` calls against the running ordinary socket. No service
was started, stopped, or configured; nothing outside this file was written.
Every claim below is marked **observed** (this flow saw it), **designed-only**
(present in code or prose but not exercised here), or **unknown**.

---

## 1. Repositories

`SKILL_VARIABLES.md` (revision: working tree of `/home/li/primary` at flow
056f6d, lines 1–14) carries no Flow Nexus variable. It does carry
`Repository root: /git` (line 12) and `Curriculum skills:
/git/github.com/LiGoldragon/Curriculum/skills` (line 7). The repositories were
located by name under that root. Observed.

| Repository | Path | Revision read | Head commit |
|---|---|---|---|
| flow (the Nexus) | `/git/github.com/LiGoldragon/flow` | `61d765e4814035c2c0a1424e670a1b62da3d10b6` | `61d765e 2026-09-17 20:30 Park native fallback when a registered Herdr route goes stale` |
| signal-flow (ordinary wire) | `/git/github.com/LiGoldragon/signal-flow` | `968ae3b00a64ebcb1ef05e21a0a55cee55ad015c` | `968ae3b 2026-09-17 19:50 Add Herdr route identity to Flow signal` |
| meta-signal-flow (meta wire) | `/git/github.com/LiGoldragon/meta-signal-flow` | `aa6104012e1d9c9b9650590e502c51fbea902e81` | `aa61040 2026-09-17 20:01 Pin routed Flow Signal in meta contract` |

Crate versions: `flow` workspace `0.3.0`
(`/git/github.com/LiGoldragon/flow/Cargo.toml:6`); `signal-flow` `1.1.0`
(`signal-flow/Cargo.toml:3`); `meta-signal-flow` `1.1.0`
(`meta-signal-flow/Cargo.toml:3`). Observed. The `0.3` in the messaging skill's
"Flow Nexus 0.3" matches the `flow` workspace version, not the wire crates.

Two further repositories are load-bearing and were read at their revisions:

| Repository | Path | Revision read | Why |
|---|---|---|---|
| harness | `/git/github.com/LiGoldragon/harness` | `75ff8a2acf56b6f4f489993a94eecfced2d792a0` | owns the `flow-id` binary |
| message (Message Nexus) | `/git/github.com/LiGoldragon/message` | `55657f4e90716071b55fa9dc133eb7d2083b7182` | the only observed consumer of `ResolveRecipient` |

Disconfirming search: `find /git -maxdepth 4 -iname "*flow*"` and `-iname
"*signal*"` returned no second flow-nexus candidate under any other org; the
only three matches under `LiGoldragon` are the three above. Observed.

---

## 2. The signal ethos of Flow Nexus

A signal ethos exists for both sockets, and it is the generation source, not a
description of hand-written Rust. `signal-flow/build.rs:1–18` reads
`ethos/signal.ethos`, regenerates, and **asserts byte equality** with
`src/generated/signal.rs` (lines 14–17) — the checked-in Rust is proven to be
the ethos's output at build time. `signal-flow/src/lib.rs:6` re-exports the
ethos text itself as `pub const ETHOS`, and `:7` binds `WIRE_VERSION` to the
crate version. Observed.

### Ordinary ethos, reproduced in full

`/git/github.com/LiGoldragon/signal-flow/ethos/signal.ethos` at `968ae3b`,
lines 1–5:

```
Signal
[]
[ Start.StartRequest Restart.RestartRequest ResolveRecipient.RecipientResolutionRequest ]
[ Started.Started Restarted.Restarted RecipientResolved.FlowNode StartRejected.StartRejection RestartRejected.RestartRejection RecipientResolutionRejected.RecipientResolutionRejection ]
[ FlowId.String SessionId.String TurnId.String FlowType.String Generation.Integer EndpointPath.String HerdrSessionName.String HerdrAgentName.String HerdrPaneId.String HerdrTerminalId.String OriginClue.{ FlowId SessionId TurnId } StartRequest.{ FlowType OriginClue } RestartRequest.{ FlowId OriginClue } RecipientResolutionRequest.FlowId HarnessKind.[ Codex Claude ] RouteReadiness.[ Ready Parked ] EndpointSelection.[ Available.{ EndpointPath RouteReadiness } Unavailable ] HerdrRoute.{ HerdrSessionName HerdrAgentName HerdrPaneId HerdrTerminalId } HerdrRouteSelection.[ Available.HerdrRoute Unavailable ] FlowLifecycle.[ Pending Active ] FlowNode.{ FlowId SessionId HarnessKind EndpointSelection HerdrRouteSelection OriginClue FlowLifecycle } Started.{ FlowId SessionId OriginClue } Restarted.{ FlowId SessionId Generation } StartRejection.[ UnknownFlowType LaunchRefused OriginUnavailable ] RestartRejection.[ ProvenanceMismatch UnknownFlow ResumeRefused ] RecipientResolutionRejection.[ UnknownFlow FlowUnavailable ] ]
```

Line 2 is the empty import list: the ordinary contract imports nothing.

### Meta ethos, reproduced in full

`/git/github.com/LiGoldragon/meta-signal-flow/ethos/signal.ethos` at `aa61040`,
lines 1–5:

```
Signal
[ signal_flow:[ FlowNode ] ]
[ Configure.ConfigureRequest ConsumeReset.ResetRequest RegisterFlow.FlowNode ]
[ Configured.Configured ResetConsumed.ResetOutcome FlowRegistered.FlowNode ConfigureRejected.ConfigureRejection ResetRejected.ResetRejection FlowRegistrationRejected.FlowRegistrationRejection ]
[ OrdinarySocketPath.String MetaSocketPath.String Configuration.{ OrdinarySocketPath MetaSocketPath } ConfigureRequest.Configuration IdempotencyKey.String CreditId.String CreditSelection.[ Next Specific.CreditId ] ResetRequest.{ IdempotencyKey CreditSelection } Activation.[ NexusRestartRequired ] Configured.{ Configuration Activation } ResetOutcome.[ Reset NothingToReset NoCredit AlreadyRedeemed ] ConfigureRejection.[ StoreRefused ] ResetRejection.[ AdapterUnavailable ProtocolRefused ] FlowRegistrationRejection.[ StoreRefused UnknownOrUnclaimedIdentity ConflictingBinding ] ]
```

Line 2 is the one edge the meta contract carries: it imports `FlowNode` from
`signal_flow`, so meta registration and ordinary resolution share one record
shape.

### Every query with its paired responses and typed refusals

Ordinary socket (`signal-flow` 1.1.0, ethos lines 3–5):

| Query | Success response | Typed refusal (closed) |
|---|---|---|
| `Start(StartRequest{ FlowType, OriginClue })` | `Started{ FlowId, SessionId, OriginClue }` | `StartRejected.[ UnknownFlowType, LaunchRefused, OriginUnavailable ]` |
| `Restart(RestartRequest{ FlowId, OriginClue })` | `Restarted{ FlowId, SessionId, Generation }` | `RestartRejected.[ ProvenanceMismatch, UnknownFlow, ResumeRefused ]` |
| `ResolveRecipient(FlowId)` | `RecipientResolved(FlowNode)` | `RecipientResolutionRejected.[ UnknownFlow, FlowUnavailable ]` |

Meta socket (`meta-signal-flow` 1.1.0, ethos lines 3–5):

| Query | Success response | Typed refusal (closed) |
|---|---|---|
| `Configure(Configuration{ OrdinarySocketPath, MetaSocketPath })` | `Configured{ Configuration, Activation.[ NexusRestartRequired ] }` | `ConfigureRejected.[ StoreRefused ]` |
| `ConsumeReset(ResetRequest{ IdempotencyKey, CreditSelection.[ Next \| Specific.CreditId ] })` | `ResetConsumed(ResetOutcome.[ Reset, NothingToReset, NoCredit, AlreadyRedeemed ])` | `ResetRejected.[ AdapterUnavailable, ProtocolRefused ]` |
| `RegisterFlow(FlowNode)` | `FlowRegistered(FlowNode)` | `FlowRegistrationRejected.[ StoreRefused, UnknownOrUnclaimedIdentity, ConflictingBinding ]` |

Note that `ResetOutcome` is a success *response*, not a refusal: `NoCredit` and
`AlreadyRedeemed` arrive as `ResetConsumed`, so an outcome is vocabulary and a
refusal is a separate head. Observed in the ethos and in
`flow/crates/flow-nexus/src/lib.rs:126–132`.

### Types carried on the wire

Scalars/aliases (all `String` except `Generation.Integer` → `i64`, confirmed
generated at `signal-flow/src/generated/signal.rs:3–21`): `FlowId`,
`SessionId`, `TurnId`, `FlowType`, `Generation`, `EndpointPath`,
`HerdrSessionName`, `HerdrAgentName`, `HerdrPaneId`, `HerdrTerminalId`,
`OrdinarySocketPath`, `MetaSocketPath`, `IdempotencyKey`, `CreditId`.

Records: `OriginClue{FlowId,SessionId,TurnId}`, `StartRequest`,
`RestartRequest`, `HerdrRoute{4 Herdr fields}`,
`FlowNode{FlowId,SessionId,HarnessKind,EndpointSelection,HerdrRouteSelection,OriginClue,FlowLifecycle}`,
`Started`, `Restarted`, `Configuration`, `ResetRequest`, `Configured`.

Closed enums: `HarnessKind.[Codex Claude]`, `RouteReadiness.[Ready Parked]`,
`EndpointSelection.[Available.{EndpointPath RouteReadiness} Unavailable]`,
`HerdrRouteSelection.[Available.HerdrRoute Unavailable]`,
`FlowLifecycle.[Pending Active]`, `CreditSelection.[Next Specific.CreditId]`,
`Activation.[NexusRestartRequired]`, `ResetOutcome.[4]`, plus the five rejection
enums above. No catch-all variant appears in either file. Observed.

Observation beside the vocabulary rule: `FlowNode` carries `SessionId`,
`EndpointPath`, and four `Herdr*` names — harness-implementation and
transport-topology language on the public wire, alongside the domain language
the ethos otherwise keeps.

---

## 3. Process anatomy

**Executable — observed.** `flow-nexus`, built from
`flow/crates/flow-nexus/src/main.rs` (28 lines). Installed at
`/home/li/.local/bin/flow-nexus`, 3508368 bytes, mtime
`2026-09-17 17:52:55`.

**Start — observed.** `fn main()` takes no arguments
(`flow-nexus/src/main.rs:6`). It creates
`/home/li/.local/state/flow` and `/run/user/1001/flow` (lines 7–10), opens the
store, then spawns **one thread** for the ordinary socket (lines 22–24) and
serves the meta socket on the main thread (lines 25–27). Both are plain
blocking `UnixListener::accept()` loops handling one frame per connection
(`lib.rs:197–202`, `:216–221`).

**Default configuration — observed, hard-coded in the executable.**
`flow-nexus/src/main.rs:11–16` passes literals: store
`/home/li/.local/state/flow/flow.sema`, Codex control socket
`/home/li/.codex/app-server-control/app-server-control.sock`, model
`gpt-5.6-terra`, timeout 10s. Socket defaults are separate constants in the
store: `DEFAULT_ORDINARY_SOCKET = "/run/user/1001/flow/flow.sock"` and
`DEFAULT_META_SOCKET = "/run/user/1001/flow/flow-meta.sock"`
(`flow-nexus/src/store.rs:27–28`). A fresh store persists them; a populated
store resumes them (`main.rs:19` reads `store.configuration()` and binds to
what comes back).

**Sema store — observed.** One `.sema` file reached only through
`sema-engine` (`store.rs:11–14`). Four tables (`store.rs:21–24`):
`flow_nexus_flows`, `flow_nexus_state`, `flow_nexus_configuration`,
`flow_nexus_herdr_routes`. Records: `FlowRecord{flow_id, flow_type, origin,
thread_id, harness_kind, endpoint_selection, lifecycle, generation}`
(`store.rs:30–40`), `FlowHerdrRouteRecord` (`:55–59`),
`FlowStoreState{next_flow_number}` (`:67–71`), `FlowStoreConfiguration`
(`:79–82`). On disk, observed: `/home/li/.local/state/flow/flow.sema`,
1056768 bytes, mtime `2026-09-18 08:14`, plus a migration backup
`flow.sema.pre-v5-20260917T1749`.

**Sockets — observed.** Two, both bound with `fs::set_permissions(... 0o600)`
immediately after `UnixListener::bind` (`lib.rs:194–196`, `:213–215`). On disk:
`/run/user/1001/flow/flow.sock` and `/run/user/1001/flow/flow-meta.sock`, both
`srw-------  li users`, mtime `2026-09-18 08:14`. The README states plainly
that the meta edge "is not a security boundary between processes running as
that same user" (`flow/README.md:38–41`).

**Actors — observed absent.** There are no Kameo actors, no mailboxes, and no
async runtime anywhere in `flow-nexus`. `RunningNexus` is a plain struct of
three fields — `store`, `codex`, `herdr` (`lib.rs:24–28`) — shared across the
two socket loops by `Arc` (`main.rs:18–21`). Dispatch is a synchronous `match`
in `Dispatches::dispatch` / `dispatch_meta` (`lib.rs:35–154`).

**Request path, frame to reply — observed for `ResolveRecipient`, designed-only
for the rest.** Wire framing is a 4-byte big-endian `u32` length prefix and an
rkyv archive, with a 1 MiB cap, implemented by the `Frame` unit struct
(`lib.rs:224–276`). The path:

1. CLI builds a typed `Query`, `rkyv::to_bytes`, writes length then bytes
   (`flow/crates/flow/src/main.rs:89–93`).
2. Nexus accepts, `Frame::read_query` → `rkyv::from_bytes::<Query>`
   (`lib.rs:199`, `:249–252`).
3. `dispatch` matches the head (`lib.rs:36–110`).
   - `Start`: maps `flow_type` to a goal string — **only `"codex-medium"` is
     accepted**, everything else returns `StartRejected(UnknownFlowType)`
     (`lib.rs:40–44`); reserves a pending flow in the store; calls
     `CodexAdapter::start_codex_observed`, persisting the thread id inside the
     callback before the first turn (`lib.rs:46–64`); then `confirm_started`.
   - `Restart`: `store.authorize_restart`, then an explicit check that
     `origin_clue.session_id == token.thread_id`
     (`lib.rs:80–82`) — provenance is the caller's own session, not a token.
   - `ResolveRecipient`: store lookup, then `claude::refresh_readiness(node)`,
     then `herdr.refresh_route(...)` (`lib.rs:99–109`).
4. `Frame::write_response` writes length + rkyv archive (`lib.rs:201`).
5. The CLI decodes and textualizes as datom for the terminal:
   `reply.datomize(vec![]).protosize().textualize()`
   (`flow/crates/flow/src/main.rs:106–110`).

**Adapters — designed-only here (not exercised by this flow).**
`CodexAdapter` speaks WebSocket/JSON-RPC over `codex app-server proxy`, and its
own header says it "never falls back to a direct Unix-socket client"
(`flow-nexus/src/codex.rs:1–3`, 794 lines). `HerdrCli` shells out to
`herdr --session <name> api snapshot` and parses JSON
(`flow-nexus/src/herdr.rs:81–96`). `claude.rs` reads
`/home/li/.claude/jobs/<short>/state.json` and
`/home/li/.claude/daemon/roster.json`, checks session match, `backend=="daemon"`,
lifecycle not in `done|concluded|killed`, status in `idle|busy`, no field
containing "permission", a live pid under `/proc`, and that the rendezvous
socket's grandparent `control.sock` equals the stored endpoint
(`claude.rs:8–9`, `:19–75`). Failing any of these returns
`RouteReadiness::Parked` rather than removing the endpoint (`claude.rs:77–82`).

**Identity gate — designed-only.** `RegisterFlow` is refused unless a
`flows-root/.<flow-id>.flow-id` marker exists, is a regular non-symlink file,
decodes as `version=1 / harness=… / identity=<32 lowercase hex> / alias=…`
(+ optional `uuid-version=`), and its alias and harness match the node
(`herdr.rs:157–236`). Observed on disk: `/home/li/primary/flows/.c7128c.flow-id`
and `.056f6d.flow-id` both carry exactly that five-line v4 form, mode `0600`.

---

## 4. CLIs

**`flow` — observed.** `/home/li/.local/bin/flow`, 606336 bytes, mtime
`2026-09-17 17:52:55`, byte-identical in size to
`flow/target/release/flow` (mtime `17:50:23`). Source:
`flow/crates/flow/src/main.rs` (190 lines). It fronts the ordinary socket,
default `/run/user/1001/flow/flow.sock`, overridable by `FLOW_SOCKET`
(`:114`). Its own usage line, printed by the installed binary:

```
usage: flow start <predefined-type> | flow restart <flow-id> | flow resolve <flow-id>
```

It speaks Signal: rkyv + length prefix on a Unix socket (`:89–103`), and it
textualizes the typed reply to datom on the way out (`:106–110`). It never
opens a database and reaches no other Nexus.

It also *infers* caller identity before sending: `caller_origin` reads
`FLOW_ID`, `CODEX_THREAD_ID` / `CODEX_SESSION_ID` / `CLAUDE_SESSION_ID`, and
`TURN_ID`, and where `FLOW_ID` is absent it derives one from the session UUID by
substring — `codex_flow_id` takes `[len-9 .. len-3]` of the last dash group,
`claude_flow_id` takes the first six characters (`:32–65`, tests `:148–158`).

**`flow-meta` — observed.** `/home/li/.local/bin/flow-meta`, 615008 bytes, same
mtime. Source: `flow/crates/flow-meta/src/main.rs` (204 lines). Fronts
`/run/user/1001/flow/flow-meta.sock`, overridable by `FLOW_META_SOCKET`
(`:136–138`). Identical framing (`:117–131`), same datom textualization
(`:143`). Its three verbs are `reset`, `register-codex` / `register-claude`,
and `configure`.

**`flow-meta register-claude` — the command named in
`flows/c7128c/log.md:5`.** At HEAD it takes `<flow-id> <session-id>
<herdr-session> <herdr-agent> <herdr-pane> <herdr-terminal> [endpoint]`
(`flow-meta/src/main.rs:37–91`; usage string `:111`). It constructs a
`FlowNode` client-side: `HarnessKind::Claude`, `FlowLifecycle::Active`,
`turn_id: "unavailable"`, and — for Claude with no explicit endpoint — an empty
endpoint path, which becomes `EndpointSelection::Unavailable` (`:52–70`).
Where an endpoint is given, Codex gets `RouteReadiness::Ready` and Claude gets
`Parked` (`:64–68`). It then sends `Query::RegisterFlow` over the meta socket.
So it is a privileged Signal call, not a file write — but the *typing is done
in the client*, and the Nexus receives an already-assembled `FlowNode`.

**`flow-id` — observed, and it is a different program in a different
repository.** `/home/li/.nix-profile/bin/flow-id` →
`/nix/store/b4wzlwmzbfis6ys2b1svh531dplxxyd3-harness-0.3.4/bin/flow-id`, an
ELF binary from the **harness** repo, declared at
`harness/Cargo.toml:28–29` (`name = "flow-id"`, `path = "src/bin/flow_id.rs"`).
Per `harness/README.md:3–18` it is the parent-flow identity helper: `flow-id
codex --flows-root DIR` or `flow-id claude --flows-root DIR --parent-session
UUID`; Codex claims from `[23:29]` of its normalized UUID, Claude claims the
first six hex characters; it takes a per-alias lock, writes a private versioned
marker through a same-directory temp file, and "prints only the claimed hex
alias".

**`flow-id` does not speak Signal.** It is flag-driven (`--flows-root`,
`--parent-session`), it prints text, and it writes the marker file directly.
It is the *producer* of the `.{alias}.flow-id` marker that `flow-nexus`'s
`VerifiesFlowClaim` later reads off the filesystem (`herdr.rs:167–180`). The
two components communicate through the filesystem, not over a socket. Observed.
This is also why `Curriculum/skills/main-flow.md:21` can say "The main flow
runs a shell command only for `flow-id`" — it is a local helper, not a client.

---

## 5. Deployment — is a Flow Nexus running?

**Yes. Observed, by four independent signs.**

- systemd user unit: `flow-nexus.service  loaded active running  Flow Nexus`.
  Unit file present at `/home/li/.config/systemd/user/flow-nexus.service`;
  source `flow/deployment/flow-nexus.service:1–13`
  (`ExecStart=%h/.local/bin/flow-nexus`, `Restart=on-failure`,
  `After=`/`Requires=codex-remote-control.service`).
- Process: pid `3727637`, `/home/li/.local/bin/flow-nexus`, started
  `Fri Sep 18 08:14:46 2026`.
- Sockets on disk: both `flow.sock` and `flow-meta.sock` present in
  `/run/user/1001/flow`, mode `srw-------`, mtime matching the process start.
- Live reply. Three read-only `flow resolve` calls against the ordinary socket:

  ```
  $ flow resolve c7128c
  RecipientResolved.{ c7128c c7128cb2-3ac6-424e-8db3-d5f3313ffea0 Claude Unavailable { c7128c c7128cb2-3ac6-424e-8db3-d5f3313ffea0 unavailable } Active }
  $ flow resolve 056f6d
  RecipientResolutionRejected.UnknownFlow
  $ flow resolve zzzzzz
  RecipientResolutionRejected.UnknownFlow
  ```

  This is a resolution witness for flow `c7128c` at 2026-09-18, and nothing
  more: it is not a transport, presentation, or read receipt for anything.

**Installation route — observed, and it is not Nix.** The three binaries are
plain files in `~/.local/bin` (not symlinks), mtime `2026-09-17 17:52:55`,
matching the sizes in `flow/target/release/`. `nix profile list` shows no flow
entry. Compare `message` 0.12.0 in the same directory, which *is* a symlink
into `/nix/store/…-message-0.12.0/`. `flow/README.md:78–82` describes exactly
this manual install and adds: "Declarative environments should package the same
unit and binaries instead of retaining this local copy." Observed.

**The deployed build is behind the repository HEAD — observed.** The installed
`flow-meta` prints:

```
usage: flow-meta reset <idempotency-key> [credit-id] | flow-meta register-codex|register-claude <flow-id> <session-id> [endpoint] | flow-meta configure <ordinary-socket> <meta-socket>
```

— no Herdr arguments. HEAD's usage string
(`flow-meta/src/main.rs:104`, `:111`) requires four. Correspondingly the live
`flow resolve c7128c` reply has **six** datom elements, while HEAD's own
round-trip test asserts **seven** (`flow/crates/flow/src/main.rs:185–188`), the
extra one being `HerdrRouteSelection`. The binaries were built at 17:52, which
is commit `51cfc00 2026-09-17 17:52 Revalidate Claude routes on Flow
resolution`. The Herdr-route commits — `signal-flow 968ae3b` (19:50),
`meta-signal-flow 63370c0`/`aa61040` (19:50/20:01), `flow 3de045d` (19:58) and
`61d765e` (20:30) — are committed but **not deployed**. Observed.

Consequence, inferred by this flow: the `flow-meta register-claude` form
documented in `flow/README.md:34–36` and the whole Herdr-binding validation path
in `herdr.rs` cannot be exercised against the running Nexus without a rebuild
and restart. The `flow-meta register-claude` call recorded in
`flows/c7128c/log.md:5` was necessarily the older two-argument form.

---

## 6. Relation to Hacky Messenger and Message Nexus

The messaging skill (`Curriculum/skills/messaging.md`, revision
`61cdc5315bb2e21b56461e42f4a6a2b03b5fcc77`) draws four layers: Herdr 0.8.2 as
transport (line 8), Hacky Messenger as "the live compatibility bridge … a
bridge, not Flow Nexus or Message Nexus" (line 10), Flow Nexus 0.3 as "the
identity and resolution design" that "does not itself prove transport or
durable delivery" (line 12), and Message Nexus 0.12 as installed for durable
attempts and receipts (line 14). The code matches that drawing, with one
asymmetry worth naming.

**Message Nexus does consume Flow Nexus — observed in code.**
`message/Cargo.toml:49` pins `signal-flow` at **exactly the revision this
report read**, `rev = "968ae3b00a64ebcb1ef05e21a0a55cee55ad015c"` — the peer
depends on the wire type repo, never on the flow crate.
`message/src/nexus_delivery.rs:1–3` states the shape: "Direct Message Nexus
delivery through Flow resolution and harness protocols. This is deliberately
inside the daemon. The ordinary CLI only sends one typed Message Signal; it
never selects or executes a harness bridge." `FlowResolver::resolve`
(`:48–74`) connects to `/run/user/1001/flow/flow.sock` (const at `:26`, env
override `FLOW_SOCKET` at `:36`), sends `FlowQuery::ResolveRecipient`, and maps
`RecipientResolved → Some(node)`, `RecipientResolutionRejected → None`. The
delivery trait's own doc comment holds the receipt grade honestly:
"`Accepted` records transport submission only. It does not claim that the
target harness consumed, interpreted, or completed the submitted message"
(`:77–85`). This is the design in `flow/DESIGN.md:39–42`: "Message Nexus
consumes that typed reply instead of maintaining a second identity registry."

Deployment: `message-nexus` is running (pid `3297488`,
`/home/li/.local/bin/message-nexus /home/li/.local/state/message/message-daemon.signal`),
unit `message-daemon.service` active. Observed. Whether its live build
contains `nexus_delivery` was not established — **unknown**; only the source at
`55657f4e` was read.

**Hacky Messenger does not consume Flow Nexus — observed, by absence.**
`/home/li/primary/tools/hacky-messenger/` (with wrappers `hm-send`,
`hm-send-abrupt`, `hm-register`, `hm-list`, `messenger`; `hm-send` is a
4-line bash `exec python3 …/hm.py send`) contains **no** match for
`flow.sock`, `ResolveRecipient`, `FLOW_SOCKET`, `flow resolve`, or `flow-meta`.
It calls `herdr` directly (`hm.py:27–29`, `:92`, `:96`, `:158–163`) and keeps
its own registry with its own conflict rule — "Flow already registered to a
different terminal; retire its registry file explicitly" (`hm.py:111`). So
Hacky Messenger maintains precisely the second identity registry that
`DESIGN.md:39–42` says Message Nexus avoids. That is the asymmetry: the bridge
in live use bypasses the resolution component, while the durable component that
does use it is behind it in the stack.

---

## 7. Divergence between the code and the vision texts

Recorded as observation beside the vision text. No verdicts.

**a. What Flow Nexus is *for*.** `Vision/flowNexus.md:5–7`: "The Flow Nexus sets
up and starts a model flow: its working directory, system prompt, training
files and instruction prompt." `:11–13`: "A Nexus component decides the system
prompt and everything about a launch, replacing the harness's subagents with
specialized harnesses launched with specialized system prompts." In code, the
whole of launch is: one hard-coded `flow_type` string `"codex-medium"` mapped to
one hard-coded goal sentence, and anything else refused
(`lib.rs:40–44`). No system prompt, no training files, no skill provisioning,
no Claude launch path. The working directory is created by the Codex child's
environment, described at `flow/README.md:74–76`. The largest live use of the
component is instead `ResolveRecipient`, which the vision file does not mention
at all.

**b. `Vision/flowNexus.md:29–32`, "A replaced session is reaped by the refresh
itself … so a dead end is never left registered and addressable."** In code
there is no reaping. Stale bindings are *parked*, not removed:
`herdr.refresh_route` sets `HerdrRouteSelection::Unavailable` and downgrades
the endpoint to `RouteReadiness::Parked` while leaving the row
(`herdr.rs:67–79`), and `claude.rs:77–82` does the same. The row stays
registered and stays resolvable.

**c. `Vision/nexus.md:107–110`, "The engine inside a Nexus is driven by Kameo
actors."** No actor, mailbox, or async runtime exists in `flow-nexus`; two
blocking accept loops share an `Arc<RunningNexus>` (`main.rs:18–27`,
`lib.rs:197–202`, `:216–221`). The vision's own escape clause — "Arc-Mutex is
permitted" (`nexus.md:110`) — covers the sharing but not the absence of actors.

**d. `Vision/nexus.md:117–125`, "State is observed by subscription … Polling is
forbidden; a correct system goes quiet when nothing changes."** There is no
subscription surface in either ethos — every response is a one-shot reply to a
one-shot query. And resolution polls on every request: it forks
`herdr … api snapshot` as a subprocess (`herdr.rs:81–96`) and re-reads
`state.json`, `roster.json`, `/proc/<pid>`, and two socket paths
(`claude.rs:19–75`). `flow/README.md:43–46` states this as the intended
behavior: "Claude resolution rechecks the job state, daemon roster, rendezvous
socket, control socket, and worker process on every request."

**e. `Vision/nexus.md:83–92`, "First configuration": a metadata tree records
whether meta `Configure` was ever done, and "while it is unset Configure is
accessible on the ordinary socket."** Not present. `Configure` exists only in
the meta ethos (`meta-signal-flow/ethos/signal.ethos:3`), and the store keeps a
single `configured` key with the `Configuration` value and no was-it-ever-done
flag (`store.rs:26`, `:79–88`).

**f. `Vision/nexus.md:66–72`, routing through a router with a wrapping enum in
the shared signal repository.** No router is involved: `flow` and `message`
both `UnixStream::connect` the socket path directly
(`flow/crates/flow/src/main.rs:89`, `message/src/nexus_delivery.rs:49`).

**g. `Vision/signal.md:30–33`, "The textual form is datom; a CLI actualizes it
and sends signal."** The reply direction holds — both CLIs textualize to datom
(`flow/.../main.rs:106–110`, `flow-meta/.../main.rs:143`). The request
direction does not: no CLI parses datom. Both hand-build the typed value from
verb-plus-positional-strings (`flow/.../main.rs:67–85`,
`flow-meta/.../main.rs:21–106`), which is also what the loaded `nexus` skill
describes as "exactly one positional argument: a typed input object in datom
textual data format. No flags, no subcommands." `flow start|restart|resolve` and
`flow-meta reset|register-codex|register-claude|configure` are subcommands.

**h. The frame envelope has no owner.** The loaded `nexus` skill has the wire
type repo own "the frame envelope and its encode/decode". Neither ethos
declares a frame, and neither generated crate carries one. The identical 4-byte
big-endian length prefix, 1 MiB cap, and rkyv call are hand-written in four
places: `flow-nexus/src/lib.rs:227–242`, `flow/crates/flow/src/main.rs:89–102`,
`flow-meta/src/main.rs:117–130`, and `message/src/nexus_delivery.rs:55–67`.
A `signal-frame` repository exists at `/git/github.com/LiGoldragon/signal-frame`
— whether it defines this envelope was **not** read; unknown.

**i. `Vision/signal.md:34–37`, "The meta signal is never optional."** Held.
Both contracts exist as separate crates with separate semver.

**j. Free functions.** The loaded `nexus` skill has `fn main()` as the only
production free function. Observed exceptions, unmarked at their sites:
`claude::refresh_readiness`, `refresh_at`, `parked`, `read_json`,
`roster_worker`, `string`, `normalized` (`claude.rs:11–102`), and
`codex_flow_id` / `claude_flow_id` (`flow/crates/flow/src/main.rs:57–65`).
Elsewhere the trait discipline is followed closely, including trait-shaped
constructors with a stated reason (`store.rs:125–131`).

---

## 8. Skills and vision touched

Authored Curriculum skills (`/git/github.com/LiGoldragon/Curriculum/skills`,
revision `61cdc5315bb2e21b56461e42f4a6a2b03b5fcc77`):

| Part | Skill | Where |
|---|---|---|
| The Nexus shape: sockets, CLIs, wire repos, Sema, traits | `skills/nexus.md` | whole file |
| Flow Nexus's place among the messaging layers; receipt grades | `skills/messaging.md` | lines 8–18, esp. 10, 12, 14 |
| `flow-id` as the one shell command a main flow runs | `skills/main-flow.md` | lines 21, 30, 33, 39 |
| `flow-id` argument-shape failure, recorded as operator experience | `skills/codex-harness.md` | line 43 |
| Field refresh seats named from `<ancestor-flow-id>` | `skills/refresh.md` | line 11 |
| "A passing isolated Luna test is … not proof that a production Field seat, Flow Nexus, or messaging route exists" | `skills/field.md` | lines 13, 25 |

Vision topics (`/home/li/primary/Vision`, working tree at flow 056f6d):

| Part | Topic | Where |
|---|---|---|
| What Flow Nexus is for; runtime repo; session naming; reaping | `Vision/flowNexus.md` | 1–32 |
| Sockets, default clients, configuration, actors, subscription, graph | `Vision/nexus.md` | 1–125 |
| The ethos form itself — the worked `Lock`/`Release` example | `Vision/signal.md` | 19–28 |
| Message-is-a-datom; interrupt is not delivery | `Vision/messaging.md` | 1–25 |

Psyche vision under `flows/*/vision/` (searched `Vision/`, `vision-raw/`, and
`flows/*/vision/` for `Flow Nexus`):

| Part | File | Where |
|---|---|---|
| `flow` starts or refreshes; `message` sends; meta socket for usage reset | `flows/da1e3f/vision/operational-flowVsMessage.md` | 3–20 |
| Predefined flow types, near-zero arguments, "training on how to get the training it needs" | `flows/9993b5/vision/easyFlowDispatch.md` | 3–10 |
| Flow CLI is the interface; the Mind holds the memory | `flows/9993b5/vision/flowAnatomy.md` | 3–9 |
| `flow list` / attach, launcher-process provenance, reuse Herdr's UI | `flows/108ab0/vision/operational-flowCliListAttachProvenance.md` | 3–9 |
| Report-is-transcript; archive-nexus | `flows/b05237/vision/operational-reportIsTranscript.md`, `flows/acbb6006/vision/archive-nexus.md` | mention only |

The `easyFlowDispatch` predefinition is visible in code as exactly one
predefined type; `operational-flowVsMessage`'s division of labour is held
exactly (`flow` has no send verb; the reset lives behind `flow-meta`);
`flowAnatomy`'s "Flow is not where the memory lives" is held — the `.sema` store
holds identity and routing rows only, not transcripts; `flow list` and the
launcher-provenance attach from `108ab0` are absent from both ethos files and
from both CLIs.

---

## Sources

Repositories, at the revisions read:

- `/git/github.com/LiGoldragon/flow` @ `61d765e4814035c2c0a1424e670a1b62da3d10b6`
  — `README.md:1–90`, `DESIGN.md:1–61`, `Cargo.toml:6`,
  `deployment/flow-nexus.service:1–13`,
  `crates/flow-nexus/src/main.rs:1–28`, `crates/flow-nexus/src/lib.rs:1–276`,
  `crates/flow-nexus/src/store.rs:1–140`, `crates/flow-nexus/src/herdr.rs:1–236`,
  `crates/flow-nexus/src/claude.rs:1–102`, `crates/flow-nexus/src/codex.rs:1–45`,
  `crates/flow/src/main.rs:1–190`, `crates/flow-meta/src/main.rs:1–204`
- `/git/github.com/LiGoldragon/signal-flow` @ `968ae3b00a64ebcb1ef05e21a0a55cee55ad015c`
  — `ethos/signal.ethos:1–5`, `src/lib.rs:1–7`, `build.rs:1–18`,
  `src/generated/signal.rs:1–60`, `Cargo.toml:2–3`
- `/git/github.com/LiGoldragon/meta-signal-flow` @ `aa6104012e1d9c9b9650590e502c51fbea902e81`
  — `ethos/signal.ethos:1–5`, `Cargo.toml:2–3`
- `/git/github.com/LiGoldragon/harness` @ `75ff8a2acf56b6f4f489993a94eecfced2d792a0`
  — `README.md:1–18`, `Cargo.toml:28–29`
- `/git/github.com/LiGoldragon/message` @ `55657f4e90716071b55fa9dc133eb7d2083b7182`
  — `Cargo.toml:49`, `src/nexus_delivery.rs:1–90`
- `/git/github.com/LiGoldragon/Curriculum` @ `61cdc5315bb2e21b56461e42f4a6a2b03b5fcc77`
  — `skills/messaging.md:1–22`, `skills/main-flow.md:21,30,33,39`,
  `skills/refresh.md:11`, `skills/field.md:13,25`, `skills/codex-harness.md:43`

Primary working tree at flow 056f6d:

- `/home/li/primary/SKILL_VARIABLES.md:1–14`
- `/home/li/primary/Vision/flowNexus.md:1–32`, `Vision/nexus.md:1–125`,
  `Vision/signal.md:1–43`, `Vision/messaging.md:1–25`
- `/home/li/primary/flows/da1e3f/vision/operational-flowVsMessage.md:1–20`
- `/home/li/primary/flows/9993b5/vision/easyFlowDispatch.md:1–10`
- `/home/li/primary/flows/9993b5/vision/flowAnatomy.md:1–9`
- `/home/li/primary/flows/108ab0/vision/operational-flowCliListAttachProvenance.md:1–9`
- `/home/li/primary/flows/c7128c/log.md:5`
- `/home/li/primary/flows/.c7128c.flow-id`, `/home/li/primary/flows/.056f6d.flow-id`
- `/home/li/primary/tools/hacky-messenger/hm.py:27–163`,
  `/home/li/primary/tools/hm-send:1–4`

Live observations, 2026-09-18, this flow, read-only:

- `systemctl --user list-units --all` — `flow-nexus.service` active/running;
  `message-daemon.service` active/running;
  `codex-remote-control.service` active/running
- `ps -o pid,lstart,args` — pid `3727637` `/home/li/.local/bin/flow-nexus`,
  started `Fri Sep 18 08:14:46 2026`; pid `3297488` `message-nexus`
- `ls -la /run/user/1001/flow/` — `flow.sock`, `flow-meta.sock`, `srw-------`
- `ls -la /home/li/.local/state/flow/` — `flow.sema` 1056768 bytes,
  `flow.sema.pre-v5-20260917T1749`
- `ls -la --time-style=full-iso /home/li/.local/bin/flow*` — three plain files,
  mtime `2026-09-17 17:52:55`
- installed `flow` and `flow-meta` usage text, printed with no arguments
- `flow resolve c7128c` → `RecipientResolved.{ … }` (6 elements);
  `flow resolve 056f6d` and `flow resolve zzzzzz` →
  `RecipientResolutionRejected.UnknownFlow`
- `nix profile list` — no flow entry
- absence searches: `grep -rn "flow.sock\|ResolveRecipient\|FLOW_SOCKET\|flow-meta" /home/li/primary/tools/hacky-messenger/` → no match;
  `find /git -maxdepth 4 -iname "*flow*"` → only the three `LiGoldragon` repos
