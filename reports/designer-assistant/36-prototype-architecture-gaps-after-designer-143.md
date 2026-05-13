# Prototype Architecture Gaps After Designer 143

Date: 2026-05-13  
Role: designer-assistant  
Scope: `reports/designer/143-prototype-readiness-gap-audit.md`, plus the
designer's per-repo absorption pass reported immediately afterward.

## Position

`reports/designer/143-prototype-readiness-gap-audit.md` is the right current
prototype plan. The designer's follow-up commits also settle several items
that were open when I began this pass:

- `signal-persona` now owns the supervision relation and documents a typed
  `SpawnEnvelope`.
- `signal-persona-mind` now names
  `ChannelMessageKind::MessageIngressSubmission`.
- `signal-persona-message` now documents `MessageKind`,
  `StampedMessageSubmission`, and `MessageRequestUnimplemented`.
- `signal-persona-terminal` now documents `TerminalRequestUnimplemented`,
  `WriteInjection.injection_sequence`, and the prototype `TerminalName`
  namespace.
- `persona` now documents the two reducer snapshots, manager restore, and
  socket metadata verification before `ComponentReady`.
- `persona-message` now sketches `MessageDaemonRoot`, `SupervisionPhase`,
  `UserSocketListener`, `OriginStamper`, and `RouterClient`.

That means the remaining issue is narrower: not "do we know the prototype
shape?" but "are the architecture documents and contracts now precise enough
that operators cannot implement two different prototypes while both claiming
to follow the docs?"

My answer: mostly yes, but there are still a few contract-level ambiguities and
stale lower sections that should be cleaned before the full prototype witness
hardens.

## Highest Priority

### 1. `signal-persona-message` still describes the old CLI-to-router relation

The new content in `signal-persona-message/ARCHITECTURE.md` adds the right
pieces: `MessageKind`, `StampedMessageSubmission`, and
`MessageRequestUnimplemented`. But the top of the file still says the channel
is:

```text
message-cli -> persona-router
```

and still says the CLI writes bytes to the router's Unix socket.

The settled engine topology is:

```text
message CLI -> persona-message-daemon -> persona-router
```

That needs to be reflected as relation architecture, not only as a payload
addition. Otherwise the operator can implement a direct CLI-to-router path and
still point at the first paragraph of the contract doc.

Recommended doc shape:

```text
signal-persona-message owns two named relations:

1. Client message relation
   message CLI -> persona-message-daemon
   root family: MessageClientRequest / MessageClientReply

2. Router ingress relation
   persona-message-daemon -> persona-router
   root family: MessageIngressRequest / MessageIngressReply
```

If the team wants to keep one `MessageRequest` / `MessageReply` root family,
the architecture should say explicitly that the same root family is used on two
different socket relations, and explain where `StampedMessageSubmission` is
legal. Right now the document says "one relation" while also introducing a
bridge record that implies two relations.

### 2. `persona-message/ARCHITECTURE.md` header and body still disagree

The header and §1.5 are now correct: `persona-message` owns the CLI and
`persona-message-daemon`, and the daemon has a Kameo actor topology.

But the lower sections still say:

- the diagram is `message CLI -> persona-router`;
- the component requires `PERSONA_MESSAGE_ROUTER_SOCKET`;
- the proxy does not build or run a daemon;
- the proxy does not depend on an actor runtime;
- the code map lacks a daemon binary and actor modules.

This is now the most dangerous stale prose in the runtime docs because it is
exactly the surface the operator needs to implement next. The body should be
rewritten around:

```text
message CLI:
  reads one NOTA record
  sends one Signal frame to message.sock
  receives one Signal reply
  prints one NOTA reply

persona-message-daemon:
  reads signal-persona::SpawnEnvelope
  binds message.sock 0660
  classifies peer credentials
  stamps ingress context
  forwards to router.sock 0600
  owns no durable ledger
```

### 3. The `SpawnEnvelope` name now covers child context and launch execution

`persona/ARCHITECTURE.md` still says a "resolved spawn envelope" carries
executable path, argv, environment, state path, socket path, socket mode, and
peer sockets. `signal-persona/ARCHITECTURE.md` now documents a typed
`SpawnEnvelope` that carries the child context but not the executable command.

Those are two different records:

- manager-internal launch plan: executable, argv, environment, command
  override, process group, restart state;
- child-readable spawn context: engine id, component kind/name, state dir,
  socket path/mode, manager socket, peer sockets, supervision version.

I recommend one of these two cleanups:

1. Rename the contract type to `ComponentSpawnContext`, leaving
   `ComponentSpawnEnvelope` as the manager-internal Rust type.
2. Keep `SpawnEnvelope` in the contract, but rename the internal manager record
   to `ResolvedComponentLaunch`.

The important point: the child should not receive "the command used to launch
me" as part of its typed domain context. That is manager launch state, not
child configuration.

### 4. `ComponentName` has two meanings across contracts

The prototype path touches both:

- `signal-persona::ComponentName`: open runtime instance identifier.
- `signal-persona-auth::ComponentName`: closed first-stack component enum.

The new `SpawnEnvelope` prose says:

```text
component_name: ComponentName (from signal-persona-auth)
```

inside `signal-persona`, where `ComponentName` already names the open instance
newtype. That is a naming collision waiting to happen.

Recommended naming direction:

```text
signal-persona::ComponentInstanceName
signal-persona-auth::ComponentPrincipal
signal-persona::ComponentKind
```

If the names do not change immediately, each architecture doc should at least
spell the distinction inline whenever both appear. The spawn context and
ingress context will otherwise invite accidental imports of the wrong
`ComponentName`.

## Prototype Semantics Still Needing One Sentence Each

### Supervision `Unimplemented` is now a settled choice, but constrain it

I would not have added `SupervisionUnimplemented` to the minimum supervision
relation. Now that it is documented, the safety rule should be:

```text
The four prototype supervision requests must be implemented by every
first-stack daemon. SupervisionUnimplemented is only for future supervision
variants outside the current prototype surface.
```

`ComponentHello`, `ComponentReadinessQuery`, `ComponentHealthQuery`, and
`GracefulStopRequest` are what make a process a Persona component. A daemon
that returns `SupervisionUnimplemented` for those should fail the readiness
witness.

### State directory for stateless components

`persona` lists component redb files for mind, router, harness, and terminal.
`signal-persona` says the `SpawnEnvelope.state_dir` may be empty when
stateless. `persona-message` says it owns no redb.

Pick the exact prototype rule:

```text
Every component receives a state directory. Stateless components may leave it
empty and must not open a redb file until they own durable state.
```

That keeps startup uniform without inventing `message.redb`.

### First prototype should use structural channels, not live mind adjudication

`persona-router` correctly says misses are parked and sent to `persona-mind`
for adjudication. For the first live-message prototype, the route should not
miss: engine setup installs structural channels, including:

```text
Internal(Message) -> Internal(Router)
  kind: MessageIngressSubmission
  duration: Permanent
```

That means the first prototype proves delivery wiring. The next prototype can
prove the parked-message choreography path:

```text
router park -> mind adjudication -> channel grant -> router retry
```

If live mind adjudication is required in prototype one, the architecture still
needs mind storage/reducer details for choreography. I recommend not making
that part of prototype one.

### Harness delivery resolution is still the least specified runtime edge

The path:

```text
router -> harness -> terminal -> terminal-cell
```

still needs one exact mapping:

```text
MessageRecipient / role name
  -> harness instance
  -> TerminalName
  -> terminal-cell session
```

`signal-persona-terminal` now says `TerminalName` is role-name scoped for the
prototype. That is good. `persona-harness` should mirror it: for prototype one,
the recipient resolves to a role-named harness, and that harness resolves to
the same role-named terminal session.

### Message timestamp authority

`signal-persona-message` documents `StampedMessageSubmission` with
`stamped_at: TimestampNanos`. The architecture should name who mints it.

I recommend:

- `persona-message-daemon` mints the ingress observation time for audit.
- `persona-router` mints the durable message slot and commit time when it
  persists the accepted message.

The ingress timestamp is provenance. The router commit time is durable message
state.

## Contract-by-Contract Status

### `signal-persona`

Ready enough for prototype design, with two cleanups:

- disambiguate open component instance name vs closed component principal;
- separate child spawn context from manager launch command state.

The supervision root-family split is good.

### `signal-persona-auth`

Ready enough. It has the right trust posture: `IngressContext` and
`MessageOrigin` are provenance, not proof.

Needed before implementation: document the SO_PEERCRED mapping for
`message.sock`, at least for:

```text
engine owner uid/gid -> ConnectionClass::Owner
other local uid      -> ConnectionClass::NonOwnerUser
```

### `signal-persona-message`

Not yet clear enough. It has the new payloads, but the relation framing is
still stale. This should be fixed before `persona-message-daemon` is
implemented.

### `signal-persona-mind`

Ready for structural-channel prototype use. Do not require live adjudication in
prototype one unless a separate mind choreography storage/reducer track lands.

### `signal-persona-harness`

Mostly ready. It already has `HarnessRequestUnimplemented`. It still needs the
recipient-to-harness and harness-to-terminal naming rule mirrored from the
terminal contract.

### `signal-persona-terminal`

Ready enough for prototype one. `TerminalName` role-name scope and
`WriteInjection.injection_sequence` are good additions.

### `signal-persona-system`

Ready enough as a skeleton. No focus or Niri behavior is needed for prototype
one.

### `signal-criome`

Correctly out of scope. Do not pull BLS/Criome into the local engine prototype.
Local prototype trust is socket ACLs, peer credentials, and manager-minted
spawn context.

## Implementation Drift To Watch

These are not architecture blockers, but they are places where stale names can
become state if operators are not careful:

- `persona-router` still documents that the current projection collapses
  `ChannelMessageKind` into `DirectMessage`. That must be replaced by the full
  endpoint/kind table key before the `MessageIngressSubmission` witness counts.
- `persona-message` currently has no daemon binary in its listed code map.
  The architecture must not let the CLI remain the only executable.
- Any remaining `message-proxy` script or test names should be treated as
  cleanup unless they are explicitly negative tests that prevent the name from
  returning.

## Recommended Operator Acceptance Shape

Prototype one should have two witnesses.

First witness: supervision and sockets.

```text
persona-daemon starts six children
each child reads spawn context
each child binds its socket at the requested mode
manager verifies socket metadata
manager probes ComponentHello and ComponentReadinessQuery
manager records ComponentSpawned, SocketBound, ComponentReady
persona status reads reduced engine-status snapshot
```

Second witness: fixture delivery.

```text
message CLI -> message.sock
persona-message-daemon stamps ingress context
persona-message-daemon forwards to router.sock
router authorizes via structural MessageIngressSubmission channel
router sends MessageDelivery to role-named harness
harness resolves same role-named TerminalName
harness asks terminal for gate + WriteInjection
terminal forwards to terminal-cell
terminal-cell transcript contains the message bytes
router records delivery result
```

No real Codex/Claude/Pi harness, no live mind adjudication, no restart backoff,
no Criome, and no system focus in this witness.

## Bottom Line

The post-143 architecture is close to prototype-ready. The main remaining
problem is not missing concepts; it is relation exactness. Clean up
`signal-persona-message` and `persona-message` so they no longer describe the
old direct CLI-to-router path, disambiguate component identity names, and state
the first prototype's structural-channel assumption. After that, operators
should be able to implement without inventing architecture in source.

## See Also

- `reports/designer/143-prototype-readiness-gap-audit.md` — current canonical
  prototype gap sweep.
- `reports/designer/142-supervision-in-signal-persona-no-message-proxy-daemon.md`
  — six-component first stack and supervision-in-`signal-persona` decision.
- `reports/designer-assistant/35-post-142-correction-file-audit.md` — earlier
  file-level audit of stale proxy/router-public wording.
- `/git/github.com/LiGoldragon/signal-persona-message/ARCHITECTURE.md` — main
  contract doc still needing relation cleanup.
- `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md` — runtime doc
  whose lower sections still need to match its corrected header.
