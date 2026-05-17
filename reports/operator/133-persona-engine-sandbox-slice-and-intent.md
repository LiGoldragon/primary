# 133 - Persona engine sandbox slice and architecture intent

Date: 2026-05-17
Role: operator
Scope: Persona meta repository, live Pi sandbox, component-ingress
messaging, three-harness route witnesses

## 0 - Short read

This slice connected two previously separate proofs:

- A live local-model Pi harness inside `terminal-cell` can call a `message`
  command from its tool surface.
- A manager-started Persona engine can route messages through
  `persona-message`, `persona-router`, `persona-harness`,
  `persona-terminal`, and `terminal-cell`.

The new combined witness starts a live Pi harness, starts the
manager-owned three-harness engine, has Pi invoke the real `message` CLI,
and proves the deterministic `initiator -> responder -> reviewer -> owner`
chain completes through the engine.

The strongest result is not that Pi generated the right sentence. The
result is that the engine now has a runnable, inspectable witness for this
boundary:

```text
live local model
  -> terminal-cell PTY
  -> message CLI
  -> persona-message daemon
  -> persona-router daemon
  -> persona-harness daemons
  -> persona-terminal supervisors
  -> terminal-cell PTYs
  -> owner inbox
```

## 1 - Commits landed

| Repo | Commit | Meaning |
|---|---|---|
| `persona` | `d38fb607` | Add the live Pi -> managed three-harness smoke. |
| `persona` | `1814da8f` | Decode generated three-harness daemon configs in tests. |
| `persona` | `480d6a96` | Clarify that component ingress is local authority-boundary input, not strong auth proof. |
| `signal-persona-message` | `3ad4c81e` | Document owner/external ingress plus manager-created component-instance ingress. |

The prior foundation this slice depended on was already in place:

- `signal-persona-auth` can name `InternalComponentInstance` origins.
- `signal-persona-message` can configure component ingress sockets.
- `persona-message` can bind those sockets and stamp component-instance
  origins.
- `persona-router` maps component-instance origins to actor sender names.
- `persona` manager writes per-instance configs and component ingress
  sockets for `initiator`, `responder`, and `reviewer`.

## 2 - What the new live smoke does

New app:

```sh
nix run .#persona-engine-sandbox-terminal-cell-pi-managed-harness-smoke
```

The app is Nix-created. It uses the same outer sandbox runner as the other
terminal-cell smokes, but with a new harness mode:

```text
persona-engine-sandbox
  --test terminal-cell
  --harness pi-managed-harness
```

The internal sequence is:

```text
1. Start terminal-cell-daemon.
2. Start Pi inside terminal-cell with bash tool enabled.
3. Start persona-daemon with PERSONA_ENGINE_TOPOLOGY=three-harness-chain.
4. Wait for manager-created message/router/harness/terminal sockets.
5. Wait for deterministic terminal runners:
     initiator-runner-ready
     responder-runner-ready
     reviewer-runner-ready
6. Put a wrapper named message on Pi's PATH.
7. Pi runs:
     message '(Send initiator start-three-harness-task)'
8. persona-message stamps owner/external origin for Pi's owner-ingress send.
9. router delivers to initiator harness.
10. initiator terminal runner sends through its own
    message-ingress/initiator.sock.
11. responder sends through message-ingress/responder.sock.
12. reviewer sends through message-ingress/reviewer.sock.
13. owner inbox contains sender reviewer and body reviewer completed task.
```

The final artifact from the successful run:

```text
/tmp/persona-pi-managed.666FuS
```

Key files:

```text
artifacts/pi-message-command.txt
  (Send initiator start-three-harness-task)

artifacts/pi-managed-harness-owner-inbox.nota
  (RouterInboxListing [(RouterInboxEntry 4 reviewer "reviewer completed task")])
```

## 3 - Architecture intent as I understand it

Persona is not a single binary that contains all behavior. It is an engine
manager plus a set of supervised components. The meta repo's job is to wire
the components together, start them with typed configuration, and provide
deployment/sandbox witnesses.

The intended component boundaries look like this:

```text
                 owner / agent CLI
                       |
                       v
              persona-message daemon
              stamps local ingress origin
                       |
                       v
              persona-router daemon
       decides route, stores message state
                       |
                       v
              persona-harness daemon
        owns harness-facing delivery surface
                       |
                       v
            persona-terminal supervisor
        owns terminal control/session surface
                       |
                       v
                 terminal-cell
          owns PTY bytes and transcript
```

The manager sits above this path:

```text
persona-daemon / EngineManager
  |
  | writes spawn envelopes and daemon configs
  | starts supervised component processes
  | scopes all sockets and state under engine id
  v
message + router + harnesses + terminals + other components
```

Important intent points:

- Daemon-first: CLIs are clients. They do not own runtime state.
- Signal contracts own cross-component vocabulary.
- Components own their own daemon sockets and state files.
- The manager creates component launch context, but does not route domain
  messages in-process.
- Origins are derived at ingress boundaries. Callers do not submit their own
  origin as trusted data.
- `terminal-cell` remains the low-level PTY/transcript primitive. Persona
  terminal logic sits above it.
- Tests should prove actual boundaries: sockets, frames, files, process
  launch, captures, and durable state. In-process mocks alone are not enough.

## 4 - Message ingress model

`persona-message` now has two ingress classes:

```text
Owner/external ingress:
  socket: message.sock
  caller: owner CLI or owner-run live harness
  origin minted by persona-message:
    MessageOrigin::External(...)

Component-instance ingress:
  socket: message-ingress/<instance>.sock
  caller: supervised component instance
  origin minted by persona-message:
    MessageOrigin::InternalComponentInstance(...)
```

This is the key rule:

```text
The client sends MessageSubmission.
The daemon stamps StampedMessageSubmission.
The router only trusts the stamped form.
```

That rule keeps sender/origin out of untrusted message text.

## 5 - What changed in tests

### Live sandbox witness

Added:

```text
persona-engine-sandbox-terminal-cell-pi-managed-harness-smoke
```

It proves live Pi can initiate a real engine route into the
manager-started harness chain.

### Stronger config witness

The existing instance-specific config check was shallow: it proved the files
existed and the old shared filenames did not.

It now decodes the generated NOTA configs:

```text
message-daemon.nota
  -> exactly three component ingress sockets
  -> origins are Harness initiator/responder/reviewer
  -> paths end in message-ingress/<name>.sock
  -> modes are 0600

<name>-terminal-daemon.nota
  -> socket path belongs to <name>-terminal
  -> supervision socket belongs to <name>-terminal
  -> store path belongs to <name>-terminal.redb
  -> store path stays under the engine state root

<name>-daemon.nota
  -> harness_name == <name>
  -> harness_kind == Fixture for this prototype
  -> socket path belongs to <name>
  -> terminal_socket_path points at <name>-terminal.sock
```

New named Nix check:

```sh
nix build .#checks.x86_64-linux.persona-three-harness-chain-writes-instance-specific-daemon-configurations
```

## 6 - Verification run

Commands run:

```sh
bash -n scripts/persona-engine-sandbox \
        scripts/persona-engine-sandbox-terminal-cell-smoke

nix --option max-jobs 0 --option cores 2 build --no-link \
  .#checks.x86_64-linux.persona-engine-sandbox-terminal-cell-script-builds

nix --option max-jobs 0 --option cores 2 run \
  .#persona-engine-sandbox-terminal-cell-pi-managed-harness-smoke

nix --option max-jobs 0 --option cores 2 build --no-link \
  .#checks.x86_64-linux.persona-three-harness-chain-writes-instance-specific-daemon-configurations
```

The live smoke passed twice while developing. The final successful run used
artifact root:

```text
/tmp/persona-pi-managed.666FuS
```

Process sweep after the run found no lingering Persona or terminal-cell
processes from that sandbox.

## 7 - What is good

The engine now has a meaningful total-path witness. A local model can run
inside the terminal harness, invoke the same command an agent would use, and
cause a manager-started engine topology to deliver and relay messages across
multiple supervised components.

The witness is also inspectable. It leaves:

- Pi terminal transcript.
- The exact command Pi invoked.
- Manager-created daemon configs.
- Terminal captures for each deterministic harness.
- The final router inbox record.

This matters because failures can now be localized by artifact, not by
guessing.

## 8 - What is still lacking

### 8.1 Router bootstrap vocabulary is still duplicated

The manager still writes router bootstrap NOTA text using local structs in
`persona/src/direct_process.rs`. The parser and operation types live in
`persona-router`.

Current state:

```text
persona manager writes text:
  (RegisterActor ...)
  (GrantDirectMessage ...)

persona-router parses text:
  RouterBootstrapOperation::from_nota(...)
```

This works, and the smoke proves router accepts the manager-written text, but
it is not yet an ideal contract boundary. The next stronger version is either:

- move the bootstrap vocabulary into the appropriate contract crate, or
- add a Nix-backed witness that feeds the manager-written bootstrap through
  the router's actual parser as a typed parser check.

### 8.2 Component ingress is local provenance, not full auth

The current component-ingress model is correct for the prototype: the
manager creates sockets with mode `0600`, gives each component the socket
path it should use, and `persona-message` derives origin from the accepted
socket.

It is not a cryptographic or multi-user proof. A same-uid process that knows
another component's ingress socket path is not ruled out by this slice. The
architecture wording now says this plainly:

```text
current local enforcement = path ownership + socket mode + sandbox discipline
stronger per-component proof = future auth substrate
```

### 8.3 The chain harnesses are deterministic fixtures

The live Pi harness initiates the route, but the three receiving harnesses
are deterministic shell runners. That is the right current witness because
it isolates engine routing. It does not yet prove three autonomous live Pi
agents can read a skill, decide to message, and complete a task without
being scripted.

### 8.4 The smoke is still shell-heavy

The shell scripts are useful because they create readable artifacts and
exercise real processes. But as architecture hardens, more typed validators
should replace raw `grep` checks for:

- router bootstrap records;
- daemon configuration content;
- inbox records;
- terminal capture records.

The direct-process config test is the first move in that direction.

## 9 - Next implementation moves

Highest signal next steps:

1. Add a router-bootstrap parser witness or move bootstrap records into the
   contract layer so `persona` and `persona-router` stop sharing vocabulary
   by copied text.
2. Add a second live-harness smoke where a live Pi receives a routed message
   through the managed harness/terminal path and replies with `message`.
3. Add typed artifact validators for terminal captures and router inbox
   instead of shell-only `grep`.
4. Keep the deterministic chain as a regression anchor while introducing
   live harnesses one at a time.

My current reading: the Persona Engine is no longer just a daemon scaffold.
It has a runnable, cross-component message path. It is still a prototype
because the engine path is proven through deterministic fixture receivers
and shell orchestration, but the shape now matches the intended architecture
closely enough to keep replacing scaffolding with real component actors and
typed contracts without changing the visible test story.
