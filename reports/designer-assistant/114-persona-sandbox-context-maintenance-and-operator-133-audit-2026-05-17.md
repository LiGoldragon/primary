# 114 - Persona Sandbox Context Maintenance And Operator 133 Audit

Date: 2026-05-17  
Role: designer-assistant

## Purpose

This report does two jobs:

1. Performs topic-scoped context maintenance for the Persona engine
   sandbox/dev-stack arc.
2. Audits `reports/operator/133-persona-engine-sandbox-slice-and-intent.md`
   against the current implementation and prior critiques.

This is the current designer-assistant reading for the sandbox slice.

## Context Maintenance

### Current reading set

Use these as current:

| Report | Current substance |
|---|---|
| `reports/operator/133-persona-engine-sandbox-slice-and-intent.md` | Operator's current implementation report for the live Pi -> managed three-harness sandbox witness. |
| `reports/operator-assistant/146-follow-up-on-145-after-operator-fixes-2026-05-17.md` | Current operator-assistant audit after the earlier three-harness findings were fixed. |
| This report | Designer-assistant context roll-forward and critique. |

Treat these as historical unless a specific detail is needed:

| Report | Current status |
|---|---|
| `reports/designer-assistant/21-sandbox-full-engine-testing-gap-review.md` | Historical: the sandbox has moved beyond "envelope only" into live Pi + manager-started route witnesses. Some Codex/Claude credential-isolation notes may still matter, but not as current sandbox state. |
| `reports/designer-assistant/23-persona-daemon-supervision-and-nix-dependency-review.md` | Historical for the current sandbox slice; still useful for future process-supervision/systemd tradeoffs. |
| `reports/designer-assistant/88-persona-engine-wide-audit-2026-05-16.md` | Historical broad audit; several findings were already marked stale by later context maintenance. |
| `reports/designer-assistant/95-handover-devstack-testing-2026-05-16.md` | Superseded by the current managed-harness witness and this report. |
| `reports/operator-assistant/145-operator-three-harness-follow-up-audit-2026-05-17.md` | Partially stale. Use operator-assistant/146 for current status; only the router-bootstrap critique remains live. |

### Load-bearing residue carried forward

- The Persona sandbox arc has graduated from "sandbox envelope" to a
  real live path: a local Pi harness inside `terminal-cell` invokes the
  real `message` CLI, which enters a manager-started Persona engine.
- The manager-started topology now has per-instance message ingress
  sockets for `initiator`, `responder`, and `reviewer`; follow-up sends
  no longer fall back through owner ingress.
- `persona-message` stamps origin from the accepted ingress boundary.
  The client still sends plain `MessageSubmission`.
- Component ingress is local provenance, not strong auth. Current
  enforcement is socket path + mode + sandbox discipline; same-uid
  confusion remains possible until the future auth substrate.
- The receiving chain is still deterministic fixture behavior, not
  three autonomous live agents.
- Router bootstrap vocabulary is the strongest remaining contract smell:
  `persona` writes NOTA records that `persona-router` parses, but the
  vocabulary is not shared through a contract crate.
- Stateful shell witnesses are valuable, but the next hardening should
  replace the remaining `grep` assertions with typed decoders/validators
  where possible.

## What I Verified

I inspected:

- `reports/operator/133-persona-engine-sandbox-slice-and-intent.md`
- `reports/operator-assistant/146-follow-up-on-145-after-operator-fixes-2026-05-17.md`
- `/git/github.com/LiGoldragon/persona`
- `/git/github.com/LiGoldragon/signal-persona-message`
- `/git/github.com/LiGoldragon/persona-message`

Targeted verification passed in `/git/github.com/LiGoldragon/persona`:

```sh
nix --option max-jobs 1 --option cores 2 build --no-link \
  .#checks.x86_64-linux.persona-three-harness-chain-writes-instance-specific-daemon-configurations \
  .#checks.x86_64-linux.persona-three-harness-router-bootstrap-is-manager-written \
  .#checks.x86_64-linux.persona-engine-sandbox-terminal-cell-script-builds -L
```

I did not rerun the full live Pi smoke. Operator and
operator-assistant both report successful live runs, and the source
shape matches those reports. Re-running the prompt-bearing local-model
smoke is useful before declaring a release milestone, but not necessary
for this critique.

## How Operator-Assistant 146 Changes The Reading

`reports/operator-assistant/146-follow-up-on-145-after-operator-fixes-2026-05-17.md`
is the right baseline for this audit. It says four earlier concerns from
operator-assistant/145 are closed:

| Earlier concern | Current state after 146 |
|---|---|
| `signal-persona-message` architecture was owner-only stale | Closed. The architecture now names `message.sock` and `message-ingress/<instance>.sock`. |
| Component ingress overclaimed auth strength | Closed in wording. Architecture now says path ownership, socket mode, and sandbox discipline; stronger proof is future auth substrate. |
| Instance-specific config witness was shallow | Closed. The witness decodes typed daemon configurations. |
| `pi-managed-harness` was WIP | Closed. The live Nix app exists and was verified by operator-assistant. |

I agree with all four closures. This report does not revive those
findings. Where I still discuss component ingress, fixture receivers, or
shell witnesses, I am using the refined post-146 framing:

- component ingress is correct as local provenance, but not
  cryptographic component auth;
- the live Pi managed-harness smoke is real, but its downstream
  harnesses are deterministic fixtures;
- shell artifacts are useful and inspectable, but the next hardening
  should replace remaining `grep` checks with typed validators.

The one live finding from operator-assistant/146 is still live here:
router bootstrap vocabulary remains duplicated between `persona` and
`persona-router`. This report sharpens the recommendation: a parser
witness is useful immediately, but contract ownership is the cleaner
destination if bootstrap persists.

## Update After Component-Triad / Authority-Direction Landing

After this report first landed, designer report 210 and its associated
edits added a canonical `skills/component-triad.md` and an
authority-direction column for the six Signal verbs. That new material
does not change this audit's verdict, but it makes the router-bootstrap
critique sharper.

The relevant new rules:

- A stateful component is a triad: daemon + thin CLI + `signal-*`
  contract.
- A CLI has exactly one Signal peer: its own daemon.
- A contract crate owns the typed wire vocabulary and per-variant verb
  mapping.
- `Mutate` is the top-down authority verb. Channel grants are not
  "requests for an opinion"; they are authority orders that the
  subordinate applies and confirms.
- `persona-router/ARCHITECTURE.md` now says channel grants are inbound
  `Mutate` orders: obey, commit, confirm; keep possibly-mutated state
  until commit.

Applied to operator/133:

- The live Pi path conforms to the triad: Pi invokes the `message` CLI;
  that CLI talks only to `persona-message-daemon`; the CLI does not talk
  to router, harness, terminal, or stores directly.
- The component-ingress sockets also fit the daemon-first model:
  managed harness runners use the `message` client surface; the message
  daemon stamps origin and forwards to router.
- The router-bootstrap gap becomes more serious, not less. The bootstrap
  file carries `GrantDirectMessage` records, which are semantically
  channel-grant authority changes. If this shape persists, those records
  should be typed in the router contract surface, not handcrafted in the
  manager as private NOTA strings.

Practical consequence: a parser witness is still useful as an immediate
guard, but the triad/authority-direction discipline makes contract
ownership the proper destination. The manager may mint the bootstrap as
startup configuration, but the vocabulary it mints must be router-owned
or contract-owned, not manager-local string convention.

## Verdict

Operator/133 is substantially accurate and should be treated as a real
milestone. The sandbox now proves a meaningful route:

```text
live local model in terminal-cell
  -> real message CLI
  -> persona-message daemon
  -> persona-router daemon
  -> managed harness instances
  -> persona-terminal supervisors
  -> terminal-cell PTYs
  -> owner inbox
```

The correct caveat is that the route is still a prototype route. The
first live model initiates the chain, but the three downstream harness
behaviors are deterministic terminal runners. That is acceptable and
useful; it should not be described as "three autonomous agents working
together" yet.

## Strong Points

### 1. The live model now enters the managed engine

The `pi-managed-harness` mode in
`scripts/persona-engine-sandbox-terminal-cell-smoke` starts Pi with bash
tooling, writes a wrapper named `message` onto Pi's `PATH`, and has Pi
invoke:

```text
message '(Send initiator start-three-harness-task)'
```

The wrapper records the exact command for artifacts, then execs the real
`message` binary. This proves the important boundary: a prompt-bearing
local model can use the same command surface an agent would use to enter
the Persona engine.

### 2. Component follow-up sends use component ingress

The managed terminal launcher derives each terminal's component ingress
socket:

```text
message-ingress/<terminal-name>.sock
```

The deterministic runners set `PERSONA_MESSAGE_SOCKET` to that socket
before sending follow-up messages. `persona-message` then stamps
`MessageOrigin::InternalComponentInstance(...)` from the accepted socket
configuration.

This closes the earlier fake-chain concern where follow-up sends could
look like owner messages. The final owner inbox sender is `reviewer`.

### 3. Configuration witnesses are now typed enough to matter

`tests/direct_process.rs` no longer only checks filenames for the
three-harness topology. It decodes:

- `MessageDaemonConfiguration`
- `TerminalDaemonConfiguration`
- `HarnessDaemonConfiguration`

The test verifies component ingress count and modes, terminal socket and
store paths, harness names, harness kind `Fixture`, and harness-terminal
pairing. That is a real architectural witness, not just a shell smoke.

### 4. Documentation now names the authority model honestly

`signal-persona-message/ARCHITECTURE.md` describes two ingress classes:

- `message.sock` for owner/external clients;
- `message-ingress/<instance>.sock` for manager-created component
  instance clients.

It also states that the accepted socket chooses the origin; the client
does not send sender/origin in-band. That matches the implementation.

## Critique

### High - Router bootstrap vocabulary is still in the wrong place

Current code in `persona/src/direct_process.rs` defines local private
records:

```text
RouterBootstrapDocument
RouterBootstrapHarness
RouterBootstrapGrant
```

Those local records emit NOTA heads such as:

```text
RegisterActor
Actor
EndpointTransport
GrantDirectMessage
```

But the actual parser and operation model live in `persona-router`.
That means the manager and router share a wire vocabulary by duplicated
text convention instead of by a contract.

Operator/133 names this correctly, but the recommended options are not
equally strong:

- A parser witness proves the text still parses today.
- Moving the bootstrap records into the appropriate contract crate fixes
  vocabulary ownership.

Recommendation: prefer the contract move unless the bootstrap is about
to disappear. A parser witness is a good temporary guard, but it should
not become the final architecture.

### High - The downstream harnesses are fixtures, not live agents

The report is honest about this in section 8.3. This caveat should stay
prominent.

The receiving path uses deterministic terminal runners generated in the
Persona flake. The runners print `*-runner-ready`, read lines, and call
`message` with scripted handoff payloads:

```text
initiator -> responder -> reviewer -> owner
```

That is the right shape for isolating engine routing, but it only proves
that the engine can carry the chain. It does not prove that a routed
message can wake a live autonomous harness, get read semantically, and
produce a non-scripted response.

Next witness should add one live receiver, not jump directly to three
live receivers:

```text
live Pi initiator
  -> deterministic responder
  -> deterministic reviewer
```

or:

```text
fixture owner send
  -> live Pi receiver
  -> message reply
```

The second shape is probably more valuable because it proves inbound
managed-harness delivery to a live model.

### Medium - Component ingress is provenance, not identity proof

The current local enforcement is:

```text
manager chooses socket path
manager writes daemon config
persona-message binds socket mode 0600
component is configured with its ingress socket
```

This is enough for prototype local provenance. It is not strong
per-component identity. A same-uid process with the path to
`message-ingress/reviewer.sock` can still attempt to connect unless
the sandbox/process boundary prevents it.

Operator/133 states this correctly. The next reports should keep using
"local provenance" or "authority-boundary input", not "component auth".

### Medium - The live smoke is still shell-orchestrated

The shell script is useful because it is readable and leaves artifacts.
The remaining problem is not "shell bad"; it is that some evidence is
still string-grep evidence:

- router bootstrap checks are string containment;
- terminal capture checks decode expected text to hex, then grep;
- inbox checks grep the NOTA output.

These should not block the current milestone. The typed configuration
decode witness already improved the most important part. But the next
hardening pass should introduce typed artifact validators for:

- router bootstrap;
- router inbox listing;
- terminal capture records.

### Medium - The smoke relies on prototype launchers

The "prototype launcher" names are acceptable because they mostly exec
real component binaries:

- `persona-router-prototype-launcher` execs `persona-router-daemon`;
- `persona-harness-prototype-launcher` execs `persona-harness-daemon`;
- `persona-message-prototype-launcher` execs `persona-message-daemon`.

The special case is `persona-three-harness-terminal-launcher`, which
wraps `persona-terminal-supervisor` with a deterministic runner script.
This is the fixture behavior that makes the chain inspectable.

The report should keep distinguishing:

```text
real component daemon path
fixture terminal-runner behavior
```

Without that distinction, future readers may think the whole downstream
chain is more agent-real than it is.

### Low - Temporary artifact roots are evidence, not durable records

Operator/133 names a successful artifact root:

```text
/tmp/persona-pi-managed.666FuS
```

That is useful forensic evidence from the run. It is not durable
workspace state. Future reports should name the artifact schema and the
Nix app/check that reproduces it more prominently than any one `/tmp`
path.

## Recommended Next Work

1. Move router bootstrap vocabulary into a contract crate, likely the
   router contract, unless the bootstrap path is about to be replaced.
2. Add a typed bootstrap parser witness now, even if the contract move
   is the larger fix.
3. Add one live receiver witness. The smallest high-signal target is a
   managed live Pi harness receiving a routed message and replying with
   `message`.
4. Add typed validators for inbox and capture artifacts so the stateful
   shell smokes rely less on `grep`.
5. Keep the deterministic three-harness chain as a regression anchor
   even after live receivers land. It isolates routing failures better
   than a fully autonomous chain would.

## Bottom Line

Operator/133 is good work and mostly good framing. The Persona engine is
past "daemon scaffold" for this path: it now has a live local-model
entry into a manager-started, cross-component route.

The honest prototype boundary is:

```text
live initiator, deterministic receivers, local provenance, shell witness
```

The next best architecture move is to make router bootstrap a typed
contract-owned vocabulary and then add one live managed receiver.
