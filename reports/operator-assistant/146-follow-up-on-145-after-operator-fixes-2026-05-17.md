# 146 - Follow-up on 145 after operator fixes

Date: 2026-05-17
Role: operator-assistant
Scope: current truth of report 145 findings after subsequent operator work

## 0. Verdict

Most of report 145 is no longer current. The operator closed four of its five
substantive findings and added a stronger live engine witness.

Current state:

- `signal-persona-message` architecture now documents component-instance
  ingress.
- Persona architecture now phrases component ingress authority precisely as
  path ownership, socket mode, and sandbox discipline, with stronger proof
  deferred to auth substrate.
- The three-harness config witness now decodes typed daemon configurations and
  checks their content.
- `persona-engine-sandbox-terminal-cell-pi-managed-harness-smoke` is now a
  Nix app, documented, and verified live.
- The router bootstrap critique remains true: `persona` still hand-builds
  router bootstrap NOTA text with manager-local structs, while the actual
  parser and types remain in `persona-router`.

No implementation repos were edited by me during this audit. I only updated
the stale-report banner on report 145 and wrote this report.

## 1. Locks And Repos

`tools/orchestrate status` showed no active operator lock and no
operator-assistant lock at audit start. The role/protocol/skill files were
locked by `second-designer-assistant`, but this audit did not touch them.

Repos inspected:

| Repo | Current relevant commit |
|---|---|
| `persona` | `480d6a9 persona: clarify component ingress authority boundary` |
| `signal-persona-message` | `3ad4c81 signal-persona-message: document component ingress origins` |
| `persona-message` | `536fa24 persona-message: stamp component ingress origins` |
| `persona-router` | `a2d1892 persona-router: accept observation frames and component origins` |
| `signal-persona-router` | `e8ffebc flake: include examples/ in build src so canonical.nota reaches include_str!` |

Working copies for `persona` and `signal-persona-message` were clean after the
verification runs.

## 2. Verification Run

### signal-persona-message

Run in `/git/github.com/LiGoldragon/signal-persona-message`:

```sh
nix --option max-jobs 1 --option cores 2 flake check -L
```

Result: passed. The run built and checked package, tests, docs, fmt, and
clippy for x86_64-linux. Round-trip tests reported 18 passed.

### Persona Pure Checks

Run in `/git/github.com/LiGoldragon/persona`:

```sh
nix --option max-jobs 1 --option cores 2 build --no-link \
  .#checks.x86_64-linux.persona-three-harness-chain-writes-instance-specific-daemon-configurations \
  .#checks.x86_64-linux.persona-three-harness-router-bootstrap-is-manager-written \
  .#checks.x86_64-linux.persona-engine-sandbox-terminal-cell-script-builds \
  .#checks.x86_64-linux.persona-daemon-three-harness-chain-smoke-script-builds -L
```

Result: passed. This also rebuilt the Persona package and ran the full
release test suite as part of the package build.

### Deterministic Three-Harness Smoke

Run in `/git/github.com/LiGoldragon/persona`:

```sh
nix --option max-jobs 1 --option cores 2 run .#persona-daemon-three-harness-chain-smoke
```

Result: passed.

Artifact root:

```text
/tmp/persona-daemon-three-harness-chain.PCEVaS
```

Owner inbox:

```nota
(RouterInboxListing [(RouterInboxEntry 4 reviewer "reviewer completed task")])
```

Instance-specific daemon configuration files present:

```text
initiator-daemon.nota
initiator-terminal-daemon.nota
message-daemon.nota
responder-daemon.nota
responder-terminal-daemon.nota
reviewer-daemon.nota
reviewer-terminal-daemon.nota
router-daemon.nota
```

Post-run process sweep found no lingering Persona daemon, router, message,
harness, terminal-supervisor, or terminal-cell process from the smoke.

### Live Pi Managed-Harness Smoke

Run in `/git/github.com/LiGoldragon/persona`:

```sh
nix --option max-jobs 1 --option cores 2 run .#persona-engine-sandbox-terminal-cell-pi-managed-harness-smoke
```

Result: passed under systemd unit `run-p1676353-i1708123.service`.

Artifact root:

```text
/tmp/persona-pi-managed.1E44lb
```

Key artifacts:

```nota
(TerminalCellRun
  (Mode LiveAgentSmoke)
  (Harness "pi-managed-harness")
  (Status Passed)
  (Transcript "/tmp/persona-pi-managed.1E44lb/artifacts/terminal-cell-transcript.txt")
  (ManagedHarnessOwnerInbox "/tmp/persona-pi-managed.1E44lb/artifacts/pi-managed-harness-owner-inbox.nota")
)
```

Pi invoked:

```text
(Send initiator start-three-harness-task)
```

Managed owner inbox:

```nota
(RouterInboxListing [(RouterInboxEntry 4 reviewer "reviewer completed task")])
```

Managed terminal captures included:

- `initiator-received:start-three-harness-task`
- `initiator-sent:initiator handed to responder`
- `responder-received:initiator handed to responder`
- `responder-sent:responder handed to reviewer`
- `reviewer-received:responder handed to reviewer`
- `reviewer-sent:reviewer completed task`

Post-run process sweep found no lingering process from the smoke.

## 3. Finding Status

### 145 High - signal-persona-message architecture stale

Status: resolved.

`signal-persona-message/ARCHITECTURE.md` now names Relation A as "Message
ingress" with:

- `message.sock` for owner/external clients;
- `message-ingress/<instance>.sock` for manager-created component-instance
  clients.

It also states that component clients send plain `MessageSubmission`; the
accepted socket chooses the origin; callers do not send sender/origin in-band;
and `persona-message` stamps
`MessageOrigin::InternalComponentInstance(...)` from the configured
`ComponentMessageIngress`.

### 145 Medium - private component ingress overclaims auth strength

Status: resolved as documentation.

`persona/ARCHITECTURE.md` now says manager-created component sockets are
authority-boundary inputs and that current local enforcement is path
ownership, socket mode, and sandbox discipline. It explicitly leaves stronger
per-component proof to the auth substrate.

This is the right precision. The implementation still does not prove
cryptographic or cross-uid component auth, but the architecture no longer
claims that it does.

### 145 Medium - router bootstrap vocabulary duplicated in persona

Status: still true.

Current evidence:

- `persona/src/direct_process.rs` still defines private
  `RouterBootstrapDocument`, `RouterBootstrapHarness`, and
  `RouterBootstrapGrant`.
- Those structs manually encode record heads including `RegisterActor`,
  `EndpointTransport`, and `GrantDirectMessage`.
- `persona/tests/direct_process.rs` still verifies the bootstrap by string
  containment, for example `(GrantDirectMessage reviewer owner)`.
- `persona-router` still owns the actual bootstrap parser and
  `RouterBootstrapOperation`.
- `signal-persona-router` still has no router bootstrap vocabulary.

The full stateful smokes prove the current text is accepted by the router.
The remaining gap is contract ownership and unit-witness quality: the manager
and router do not share typed bootstrap records, and the manager-side witness
does not parse the bootstrap through router's authoritative parser.

This is now the best high-signal follow-up from report 145.

### 145 Medium - instance-specific config witness shallow

Status: resolved.

`persona/tests/direct_process.rs` now decodes:

- `MessageDaemonConfiguration`;
- `TerminalDaemonConfiguration`;
- `HarnessDaemonConfiguration`.

The test checks component ingresses, terminal socket/store paths, harness
names, harness kinds, supervision sockets, socket modes, and paired terminal
sockets. The named Nix check
`persona-three-harness-chain-writes-instance-specific-daemon-configurations`
passed.

### 145 Medium - pi-managed-harness WIP

Status: resolved.

The app is exposed in the flake, listed in `TESTS.md`, named in
`ARCHITECTURE.md`, included in the terminal-cell script-build check, and
verified live in this audit. The live run proves a local Pi harness in
terminal-cell invoked the real `message` CLI and triggered the
manager-started initiator/responder/reviewer chain.

### 145 Low - stateful shell witnesses rely heavily on grep

Status: partially true, lower priority now.

The most important typed-config gap is closed by the decode witness. The
stateful shell smokes still use `grep` for some NOTA and terminal-capture
assertions. That remains a useful hardening path, but it is no longer the
central weakness.

The sharper version of this critique is specifically the router bootstrap
parser/contract issue above.

## 4. Recommended Next Work

The next implementation pass should focus on router bootstrap ownership:

1. Either move router bootstrap records into a shared contract crate, probably
   `signal-persona-router`, or expose a parser/validator path that `persona`
   can use without depending on router internals in the wrong direction.
2. Replace the manager-side substring witness with a typed parse witness.
3. Add a Nix check that generates the manager bootstrap and validates it
   through the authoritative bootstrap parser.

Everything else from report 145 can be treated as closed for now.

