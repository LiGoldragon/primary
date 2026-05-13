# 144 — Prototype architecture: final cleanup after DA/36

*Designer report. Follow-up to /143 after my §5 absorption
pass landed twelve ARCH commits across the workspace.
Designer-assistant/36 audited the result and caught: (1) the
two contract docs I added new sections to but left the
old relation framing stale; (2) two naming overloads that
will collide if not fixed now; (3) several prototype-scope
decisions /143 left implicit. This report lands the
clarifications and the inline ARCH fixes; it does **not**
introduce new prototype scope.*

---

## 0 · TL;DR

DA/36's reading is right: the post-/143 architecture is close
to prototype-ready, but two ARCH docs still describe the
pre-/142 direct CLI-to-router path in their lower sections,
and two name overloads (`ComponentName` across two crates;
`SpawnEnvelope` as both child-readable context and
manager-internal launch state) need disambiguation before
operator implements against them.

This report:

1. **Acknowledges /143 §5 absorption is complete** (twelve
   ARCH commits across signal-persona, signal-persona-mind,
   signal-persona-message, signal-persona-terminal, persona,
   persona-mind, persona-router, persona-message,
   persona-harness, persona-system, persona-terminal,
   terminal-cell — per /143 §5 plus the four post-summary
   ones).

2. **Lands the four DA/36 highest-priority cleanups** (§2):
   - `signal-persona-message/ARCH` rewritten to a
     two-relation framing — *client message* (CLI →
     daemon) and *router ingress* (daemon → router).
   - `persona-message/ARCH` lower sections rewritten to
     match the §1.5 daemon topology that already landed.
   - `SpawnEnvelope` (child-readable typed wire form in
     `signal-persona`) split conceptually from
     `ResolvedComponentLaunch` (manager-internal Rust
     composite holding executable/argv/env/restart state).
   - `ComponentName` collision flagged for operator rename
     (kept for now; both crates' docs gain inline
     disambiguation notes).

3. **Lands six prototype-scope design clarifications**
   (§3):
   - Supervision `Unimplemented` is **only** for future
     supervision-relation variants — the four prototype
     variants (Hello / Readiness / Health / GracefulStop)
     must be implemented by every supervised daemon, not
     stubbed.
   - State-dir rule: every component receives a state dir;
     stateless components leave it empty and do not open a
     redb until they own durable state.
   - **Structural-channel-only prototype one**: the
     `Internal(Message) → Internal(Router)` channel with
     kind `MessageIngressSubmission` and duration
     `Permanent` is installed by engine setup; the message
     route does not miss; live mind adjudication is
     prototype two.
   - Harness delivery resolution mapping made explicit:
     `MessageRecipient` / role-name → harness instance →
     `TerminalName` → terminal-cell session, with
     role-name namespace alignment between
     `signal-persona-harness` and `signal-persona-terminal`.
   - `StampedMessageSubmission.stamped_at` timestamp
     authority: `persona-message` mints the ingress
     observation time (provenance); `persona-router` mints
     the durable commit time when persisting the accepted
     message.
   - SO_PEERCRED mapping in `signal-persona-auth`:
     engine-owner uid/gid → `ConnectionClass::Owner`; other
     local uid → `ConnectionClass::NonOwnerUser`.

4. **Names the two-witness prototype-one acceptance**
   (§4 — taken verbatim from DA/36's recommendation): supervision-and-sockets witness, then fixture-delivery
   witness. Operator's `primary-devn` track 17 absorbs
   both witnesses.

5. **Operator bead `primary-devn` updated** with the
   above + a follow-up rename track for the `ComponentName`
   disambiguation (§5).

---

## 1 · /143 §5 absorption — status confirmation

DA/36 §0 enumerated what landed via my absorption pass.
Confirmed complete (all twelve commits pushed to main):

| Repo | Commit | What landed |
|---|---|---|
| `signal-persona` | `5c79b384` | `SpawnEnvelope` record + `SupervisionUnimplemented` variant + constraints |
| `signal-persona-mind` | `611c4e69` | `MessageIngressSubmission` channel-kind + `MindRequestUnimplemented` |
| `signal-persona-message` | `06b14183` | `MessageKind` + `StampedMessageSubmission` + `MessageRequestUnimplemented` |
| `signal-persona-terminal` | `7841b9f0` | `TerminalRequestUnimplemented` + `injection_sequence` + `TerminalName` scope |
| `persona` | `2659d838` | `SpawnEnvelope` ref + two-reducer schema + manager-restore + socket-metadata |
| `persona-mind` | `de3823dd` | §6.5 supervision-relation reception |
| `persona-router` | `dbbf3408` | §1.5 supervision + `MessageIngressSubmission` note + schema-version guard |
| `persona-message` | `22a1cb03` | §1.5 daemon actor topology |
| `persona-harness` | `aa11e4bf` | §1.5 `HarnessLifecycle` FSM + supervision |
| `persona-system` | `6a31c60b` | §1.5 supervision (skeleton mode) |
| `persona-terminal` | `e1d8c58f` | §1.5 supervision + prompt-pattern lifecycle + gate forwarding + message-landing endpoint |
| `terminal-cell` | `dbae3614` | dropped "transitional" qualifier on Signal control + socket mode |

Plus the report itself at `7188ac67` on primary's main and
operator bead `primary-devn` updated.

DA/36's verdict: "mostly yes" the architecture is precise
enough. The remaining issues are scoped at the relation-
framing level, not at the prototype-shape level. This
report addresses each one.

---

## 2 · DA/36 highest-priority cleanups

### 2.1 `signal-persona-message` — two-relation framing

**Problem (DA/36 §1)**: the contract doc's header still
says the channel is `message-cli → persona-router` with
the CLI writing bytes to the router's UDS. My §5
absorption added the new payloads (`MessageKind`,
`StampedMessageSubmission`, `MessageRequestUnimplemented`)
but left the upstream relation framing intact. An operator
reading the doc top-down could still implement the old
direct-to-router path and point at paragraph one.

**Resolution**: the contract owns **two named relations
sharing one root family** (`MessageRequest` /
`MessageReply`), wired across two different sockets:

```text
Relation A — Client message
  endpoint:   message CLI (sender) → persona-message (receiver)
  socket:     message.sock (mode 0660)
  payloads:   MessageRequest::MessageSubmission     (CLI → daemon)
              MessageRequest::InboxQuery
              MessageReply::*

Relation B — Router ingress
  endpoint:   persona-message (sender) → persona-router (receiver)
  socket:     router.sock (mode 0600)
  payloads:   MessageRequest::StampedMessageSubmission (daemon → router, with origin tag)
              MessageReply::*
```

**Why one root family across two relations**: the two
relations share the same domain vocabulary (message submission,
inbox query, message slot, message body); only the
stamp/forwarding bridge changes shape. Per
`skills/contract-repo.md` §"Contracts name a component's
wire surface", one contract crate may carry one or more
relations, and one root family may serve more than one
sender-receiver pair if the payloads are mutually
exclusive (i.e., `StampedMessageSubmission` is legal only
on Relation B; plain `MessageSubmission` is legal only on
Relation A). The ARCH names each variant's legal relation
explicitly so audit can reject misuse.

The contract crate ARCH gets the two-relation table at the
top, with the existing `MessageKind` /
`StampedMessageSubmission` / `MessageRequestUnimplemented`
sections folded under "Relation B" or "Cross-relation
records" as appropriate.

(ARCH edit lands inline in this commit; see §5.1.)

### 2.2 `persona-message` — stale lower sections

**Problem (DA/36 §2)**: my §5 absorption added §1.5
("Daemon actor topology") at the top but didn't touch:

- §0 TL;DR diagram showing `message CLI → persona-router`
  (wrong; should be `message CLI → persona-message-daemon
  → persona-router`).
- §2 "The proxy owns no durable message state. It requires
  `PERSONA_MESSAGE_ROUTER_SOCKET`..." (wrong; the CLI
  connects to `message.sock`, not `router.sock`).
- §3 "length-prefixed Signal frame transport to the
  configured router socket" (wrong; to the daemon socket).
- §4 invariants "The proxy does not build or run a daemon"
  and "The proxy does not depend on an actor runtime"
  (both **wrong** now; the daemon IS the component).
- Code map missing the daemon binary.

**Resolution**: full rewrite of the lower sections to match
the §1.5 topology that already landed. ARCH edit lands
inline; see §5.2.

### 2.3 `SpawnEnvelope` — split from manager launch state

**Problem (DA/36 §3)**: `persona/ARCH` describes a
"resolved spawn envelope" carrying executable path, argv,
environment, *state path, socket path, socket mode, peer
sockets*; `signal-persona/ARCH` now documents a typed
`SpawnEnvelope` with only the child-readable subset
(engine_id, kind, name, state_dir, socket_path, socket_mode,
peer_sockets, manager_socket, supervision_protocol_version).
These are two records sharing a name. The child should not
receive "the command used to launch me" as part of its typed
domain context.

**Resolution**: the contract type `signal-persona::SpawnEnvelope`
is **the child-readable typed wire form**. The manager-
internal Rust composite is `ResolvedComponentLaunch`, which
carries:

```text
ResolvedComponentLaunch
  | executable_path:     PathBuf
  | argv:                Vec<OsString>
  | environment:         BTreeMap<OsString, OsString>
  | working_directory:   Option<PathBuf>
  | process_group_mode:  ProcessGroupMode
  | restart_policy:      RestartPolicy
  | spawn_envelope:      SpawnEnvelope          (the typed payload the child reads)
```

`DirectProcessLauncher` consumes `ResolvedComponentLaunch`,
forks/execs the executable, and writes the embedded
`SpawnEnvelope` to the per-component envelope file
(`/var/run/persona/<engine-id>/<component>.envelope`) at
spawn time. The child reads only the `SpawnEnvelope`.

**Why keep `SpawnEnvelope` on the contract side**: the typed
contract field is the *boundary* — that's what the child
binds to. Rust-internal manager records can change shape
without touching the wire. `ResolvedComponentLaunch` is
operator's lane (in `persona/src/launch/`).

ARCH edits land inline in `persona/ARCH` and
`signal-persona/ARCH`; see §5.3 and §5.5.

### 2.4 `ComponentName` collision

**Problem (DA/36 §4)**: two crates own a type named
`ComponentName`:

- `signal-persona::ComponentName` — *open* runtime
  instance identifier (newtype around a validated string).
- `signal-persona-auth::ComponentName` — *closed* enum of
  the six first-stack component principals (`Mind`,
  `Router`, `Message`, `System`, `Harness`, `Terminal`).

`SpawnEnvelope` was written with `component_name:
ComponentName (from signal-persona-auth)`, sitting inside
`signal-persona`'s record where `ComponentName` already
means the open newtype. This is a collision waiting to bite.

**Resolution** (designer decision; operator rename
follows): rename to disambiguate:

- `signal-persona::ComponentInstanceName` (open
  instance, validated)
- `signal-persona-auth::ComponentPrincipal` (closed
  enum of first-stack principals)
- `signal-persona::ComponentKind` — unchanged (closed
  enum of component classes)

The rename touches two contract crates plus every consumer
(`persona`, `persona-router`, `persona-mind`,
`persona-harness`, etc.). Filed as a new track on
`primary-devn` (§5.7).

**Until the rename lands**, the ARCH docs gain inline
disambiguation notes wherever both names appear. ARCH
edits land inline; see §5.5 + §5.6.

---

## 3 · Prototype-scope design clarifications

DA/36 surfaced six small clarifications that /143 left
implicit. Each is a one-paragraph rule landing here.

### 3.1 Supervision `Unimplemented` constrained

`SupervisionUnimplemented` is **only** for future
supervision-relation variants that grow beyond the current
four-op surface (`ComponentHello`,
`ComponentReadinessQuery`, `ComponentHealthQuery`,
`GracefulStopRequest`). Every supervised first-stack
daemon **must** implement those four — a daemon that
replies `SupervisionUnimplemented` to any of them fails the
prototype readiness witness.

The architectural-truth witness:

```text
supervision_unimplemented_only_for_future_variants
  — assert that none of the prototype daemons reply
    SupervisionUnimplemented to ComponentHello,
    ComponentReadinessQuery, ComponentHealthQuery, or
    GracefulStopRequest. Future-variant reply is allowed
    only for variants not in the prototype-scope enum.
```

(ARCH edit lands inline in `signal-persona/ARCH`; see §5.5.)

### 3.2 State directory for stateless components

The prototype rule:

> **Every component receives a state directory via its
> `SpawnEnvelope.state_dir`. Stateless components (today:
> `persona-message`, `persona-system` in skeleton
> mode) leave the directory empty and do not open a redb
> file until they own durable state.**

This keeps startup uniform without forcing the message
daemon or paused system daemon to invent a `message.redb`
or `system.redb`. Manager prepares the directory at
spawn-envelope mint time per engine convention; child
opens it only if it has state to persist.

(ARCH edit lands in `signal-persona/ARCH` and
`persona/ARCH`; see §5.3, §5.5.)

### 3.3 Structural-channel-only prototype one

Per DA/36 §"First prototype should use structural channels,
not live mind adjudication": **prototype one's
live-message path does not miss its channel**. Engine
setup installs the structural channel:

```text
Internal(Message) → Internal(Router)
  kind:     MessageIngressSubmission
  duration: Permanent (engine setup)
```

Router's `ChannelAuthority` returns *channel found* for
every prototype-one ingress; no parked-message,
no `AdjudicationRequest` to mind, no live choreography
loop. The choreography path (park → mind adjudication →
channel grant → router retry) is **prototype two** — when
the structural-channel-only path is real and a need to
deny / time-bound / grant ad-hoc channels surfaces.

This simplifies what `persona-mind` needs for prototype
one: the supervision relation + the `Unimplemented`
replies for choreography ops are sufficient.
Mind's storage/reducer for choreography lands in prototype
two.

(ARCH edit lands in `persona-mind/ARCH` and
`persona-router/ARCH`; see §5.6.)

### 3.4 Harness delivery resolution mapping

`signal-persona-terminal/ARCH` already says `TerminalName`
is role-name scoped for the prototype (per /143 §3
Agent C + the §5 absorption). `persona-harness/ARCH`
should mirror it explicitly:

```text
Recipient resolution (prototype one):
  MessageRecipient (role name, e.g. "designer")
    → harness instance: role-named harness from harness registry
    → TerminalName: same role-named terminal session
    → terminal-cell session: cell bound to the role-named terminal
```

One harness per role for prototype one. Future cases
(multiple harnesses per role, harness pools, etc.) get a
richer namespace when they surface.

(ARCH edit lands in `signal-persona-harness/ARCH`; see
§5.4.)

### 3.5 `StampedMessageSubmission.stamped_at` authority

Per DA/36 §"Message timestamp authority": two distinct
timestamps, two distinct minters:

| Field | Minted by | Meaning |
|---|---|---|
| `StampedMessageSubmission.stamped_at` | `persona-message` | Ingress observation time. Audit/provenance. |
| `Router::commit_time` (on `MessageSlot` persistence) | `persona-router` | Durable commit time. Source of truth for "when did this message land in the engine." |

Ingress timestamp is provenance; router commit time is
durable message state. Router writes its own commit time
when persisting the accepted message; it does not adopt
the ingress timestamp as durable truth.

(ARCH edit lands in `signal-persona-message/ARCH`; see
§5.1.)

### 3.6 SO_PEERCRED mapping in `signal-persona-auth`

The auth crate carries `ConnectionClass` as provenance, not
proof — but the *mapping* from kernel-peer credentials to
class hasn't been written down anywhere. Concrete rule for
prototype one:

```text
On message.sock (the only user-writable socket):
  SO_PEERCRED.uid == engine_owner_uid  →  ConnectionClass::Owner
  SO_PEERCRED.uid != engine_owner_uid  →  ConnectionClass::NonOwnerUser(uid)

On internal sockets (0600 — only persona-user processes
can connect):
  SO_PEERCRED.uid == persona_system_uid  →  ConnectionClass::Internal
  (other uids are rejected at the kernel level)
```

The `engine_owner_uid` comes from the manager catalog
(`OwnerIdentity::User(Uid)`). The `persona_system_uid` is
the deployment's `persona` system user.

(ARCH edit lands in `signal-persona-auth/ARCH`; see §5.4.)

---

## 4 · The two-witness prototype acceptance

DA/36 §"Recommended Operator Acceptance Shape" articulates
the prototype-one acceptance as two witnesses. Adopted
verbatim:

**Witness 1 — supervision and sockets**:

```text
persona-daemon starts six children
each child reads spawn context from /var/run/persona/<engine-id>/<component>.envelope
each child binds its socket at the requested mode
manager verifies socket metadata (type/path/mode)
manager probes ComponentHello and ComponentReadinessQuery for each child
manager records: ComponentSpawned, SocketBound, ComponentReady (per child)
engine-status-snapshot shows all six in Running
engine-lifecycle-snapshot shows all six in Ready
persona status returns the engine-status snapshot

Negative: a child that fails to bind, binds the wrong mode,
or returns SupervisionUnimplemented for any of the four
prototype-scope ops fails the witness.
```

**Witness 2 — fixture delivery**:

```text
message CLI parses NOTA `(Send fixture "hello")`
CLI connects to message.sock, sends MessageRequest::MessageSubmission
persona-message receives, stamps MessageOrigin::External(Owner) from SO_PEERCRED
persona-message forwards MessageRequest::StampedMessageSubmission to router.sock
router checks channel table: Internal(Message) → Internal(Router) kind MessageIngressSubmission found (Permanent, installed at engine setup)
router resolves recipient "fixture" → HarnessKind::Fixture instance
router sends signal-persona-harness::MessageDelivery to harness.sock
harness resolves "fixture" → TerminalName::new("fixture")
harness calls AcquireInputGate { pattern_id } on terminal-supervisor
terminal forwards to fixture cell; cell returns GateAcquired { lease, PromptState::Clean }
harness calls WriteInjection { lease, "hello", injection_sequence: 0 }
cell writes "hello" to child PTY
cell returns InjectionAck
harness reports DeliveryCompleted to router via signal-persona-harness
router persists delivery_results row
fixture cell's transcript contains "hello"

Negative: no real Codex/Claude/Pi harness needed (Fixture is enough)
Negative: no live mind adjudication needed (structural channel covers it)
Negative: no restart backoff, no Criome, no system focus, no multi-engine
```

Both witnesses fire green via `nix flake check` /
`nix run .#...`. Operator's `primary-devn` track 17 lands
both.

---

## 5 · ARCH-doc edits landing inline with this report

### 5.1 `signal-persona-message/ARCH`

Rewrite §"Channel" and §"Record source" + the example to
the two-relation framing per §2.1. The new payloads
(`MessageKind`, `StampedMessageSubmission`,
`MessageRequestUnimplemented`) stay; the example shows
both sockets.

Add the `stamped_at` authority paragraph per §3.5.

### 5.2 `persona-message/ARCH`

Rewrite §0 TL;DR diagram, §2 State and Ownership, §3
Boundaries, §4 Invariants, Code Map per §2.2. Keep §1.5
(daemon actor topology — already correct).

### 5.3 `persona/ARCH` (manager apex)

Rename mentions of "resolved spawn envelope" carrying
executable/argv/environment to **`ResolvedComponentLaunch`**
(the manager-internal record); keep the typed
`SpawnEnvelope` reference for the child-readable subset
per §2.3.

Add §"State directory for stateless components" per §3.2.

### 5.4 `signal-persona-auth/ARCH`

Add §"SO_PEERCRED → ConnectionClass mapping" per §3.6.

### 5.5 `signal-persona/ARCH`

- Add §"`SpawnEnvelope` vs `ResolvedComponentLaunch`"
  disambiguation per §2.3.
- Add inline note where `SpawnEnvelope.component_name`
  is described: the field uses
  `signal-persona-auth::ComponentName` (the closed
  principal enum), **not** `signal-persona::ComponentName`
  (the open instance newtype). Track the rename to
  `ComponentPrincipal` / `ComponentInstanceName` in the
  operator bead.
- Add §"State directory for stateless components" per §3.2
  to the `SpawnEnvelope` section.
- Add §"Supervision `Unimplemented` constraint" per §3.1.

### 5.6 `signal-persona-harness/ARCH`

Add §"Recipient → harness → terminal resolution mapping"
per §3.4.

### 5.7 Tracks for `primary-devn` bead

New tracks for operator:

- **Track 18**: Rename `signal-persona::ComponentName`
  → `ComponentInstanceName` and
  `signal-persona-auth::ComponentName` →
  `ComponentPrincipal`. Coordinated wire bump.
- **Track 19**: Define `persona::launch::ResolvedComponentLaunch`
  as the manager-internal launch record; have
  `DirectProcessLauncher` consume it and emit the typed
  `SpawnEnvelope` as the envelope file. Drop conflation
  in code.
- **Track 20**: Witness "structural-channel-only
  prototype-one": engine setup installs `Internal(Message)
  → Internal(Router) MessageIngressSubmission Permanent`;
  router's channel-check returns *found* for prototype
  ingress; no `AdjudicationRequest` reaches mind during
  Witness 2.

---

## 6 · What this report does NOT change

- **Prototype scope**: still the six-component first stack
  + the live fixture-message path per /143 §1. No new
  components, no new contracts, no new live-message
  endpoints.
- **`/143`**: stays as the canonical prototype-readiness
  audit. This report extends, does not supersede.
- **Operator's general direction** on `primary-devn`:
  tracks 1–17 remain valid. Tracks 18–20 are additive.

---

## 7 · Open questions

| # | Question | Owner | Recommendation |
|---|---|---|---|
| Q1 | Rename `ComponentName` immediately, or defer? | Operator | Defer rename to track 18; until then, ARCH docs have inline disambiguation notes |
| Q2 | `ResolvedComponentLaunch` vs `LaunchPlan` naming for the manager-internal record? | Operator | Use `ResolvedComponentLaunch` to mirror "this is the *resolved* shape after command resolution"; the prior "launch configuration" term in `persona/ARCH` §1.7 is the *unresolved* shape |
| Q3 | Does `StampedMessageSubmission` belong in `signal-persona-message` or in `signal-persona-auth` (since the origin tag is the auth crate's responsibility)? | Designer | Keep in `signal-persona-message`: it's a message domain record that *embeds* `signal-persona-auth::MessageOrigin`. Putting it in auth would mean the auth crate carries message-domain payloads, which violates `skills/contract-repo.md` §"Contracts name a component's wire surface" |

---

## See also

- `~/primary/reports/designer/143-prototype-readiness-gap-audit.md`
  — the canonical prototype-readiness audit this report
  extends.
- `~/primary/reports/designer-assistant/36-prototype-architecture-gaps-after-designer-143.md`
  — DA's review whose findings this report absorbs.
- `~/primary/reports/designer-assistant/35-post-142-correction-file-audit.md`
  — earlier audit of stale proxy/router-public wording
  (referenced by DA/36).
- `~/primary/reports/designer/142-supervision-in-signal-persona-no-message-proxy-daemon.md`
  — six-component first stack + supervision-in-`signal-persona`.
- `~/primary/reports/designer/127-decisions-resolved-2026-05-11.md`
  — closed enums (no `Other`); `MessageBody(String)` stays
  freeform with `MessageKind` for specificity.
- `~/primary/skills/contract-repo.md` §"Contracts name a
  component's wire surface" — multi-relation contract
  crates; one root family per relation OR one root family
  across relations with payload-by-payload legality named.
- `~/primary/skills/architectural-truth-tests.md` — witness
  pattern for §3.1's constrained-`Unimplemented` witness.
- `/git/github.com/LiGoldragon/signal-persona-message/ARCHITECTURE.md`
  — edited per §5.1.
- `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md`
  — edited per §5.2.
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md`
  — edited per §5.3.
- `/git/github.com/LiGoldragon/signal-persona-auth/ARCHITECTURE.md`
  — edited per §5.4.
- `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md`
  — edited per §5.5.
- `/git/github.com/LiGoldragon/signal-persona-harness/ARCHITECTURE.md`
  — edited per §5.6.
- bead `primary-devn` — updated description per §5.7 with
  tracks 18–20.
