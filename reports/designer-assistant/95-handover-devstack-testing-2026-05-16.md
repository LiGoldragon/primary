# 95 — Handover: dev-stack testing coherence, 2026-05-16

Role: designer-assistant
Date: 2026-05-16

This is a context-maintenance handover for the hands-on Persona engine
coherence pass that followed `88-persona-engine-wide-audit-2026-05-16`
(originally landed as `86-` and renumbered during 2026-05-16
context maintenance to resolve a collision with
`86-cluster-secret-binding-arc.md`).
It records only the load-bearing residue: what changed, what is still
open, and where to resume.

## What landed in working trees

### persona-router

Repository: `/git/github.com/LiGoldragon/persona-router`

The router daemon connection path now accepts two frame families on
`router.sock`:

- `signal-persona-message` frames for message ingress;
- `signal-persona-router::RouterFrame` Match requests for read-side
  observation.

The new observation path decodes a length-prefixed `RouterFrame`, sends
`ApplyRouterObservation` to `RouterRuntime`, and writes a typed router
reply. It does not bypass `RouterObservationPlane`.

Touched files:

- `src/router.rs`
- `src/error.rs`
- `src/lib.rs`
- `tests/observation_truth.rs`
- `flake.nix`
- `ARCHITECTURE.md`

New named witness:

- `router-daemon-accepts-router-observation-frames`

### persona-introspect

Repository: `/git/github.com/LiGoldragon/persona-introspect`

`RouterClient` is now the first live peer client. When
`TargetSocketDirectory.router_socket` is configured,
`prototype_witness()` sends a typed `RouterRequest::Summary` over a
length-prefixed `signal-persona-router` frame and composes the reply into
`PrototypeWitness.router_seen`.

This is a prototype one-shot `Match` query, not the final Subscribe
stream. The architecture now says that this shape is allowed only as an
explicit witness path and not as a timer loop.

Touched files:

- `src/runtime.rs`
- `src/error.rs`
- `Cargo.toml`
- `Cargo.lock`
- `tests/actor_runtime_truth.rs`
- `tests/store.rs`
- `flake.nix`
- `ARCHITECTURE.md`
- `src/daemon.rs`, `tests/daemon.rs`, and
  `tests/actor_discipline_truth.rs` only changed by formatting.

New named witness:

- `test-router-client-live-summary`

### persona

Repository: `/git/github.com/LiGoldragon/persona`

`scripts/persona-dev-stack` was updated for the current
`persona-terminal-signal` CLI:

- old: `--socket "$PERSONA_TERMINAL_SOCKET"`
- new: `--control-socket "$PERSONA_TERMINAL_SOCKET"`

This fixed the dev-stack smoke failure where the terminal CLI treated
`--socket` as a literal socket path and the terminal capture artifact was
empty.

## Verification

Passed:

```sh
cargo test --quiet
```

in:

- `/git/github.com/LiGoldragon/persona-router`
- `/git/github.com/LiGoldragon/persona-introspect`

Passed named Nix witnesses:

```sh
nix build .#checks.$system.router-daemon-accepts-router-observation-frames --option substituters '' -L
nix build .#checks.$system.test-router-client-live-summary --option substituters '' -L
```

Passed full dev-stack smoke after the terminal CLI flag fix:

```sh
nix run .#persona-dev-stack-smoke --option substituters '' -L
```

The successful dev-stack run printed:

```text
persona dev stack smoke=passed
```

## What's open

The changes above are not committed or pushed yet.

`persona-introspect` is not fully live. It only queries router. The
manager and terminal clients still hold socket paths and supervise, but
they do not yet speak real peer observation protocols.

The top-level `persona-dev-stack-smoke` still does not launch or verify
`persona-introspect`; it currently proves the message/router/harness/
terminal path.

The router/introspect bridge is a one-shot Match request. The final
shape remains Subscribe streams with initial snapshot plus pushed
deltas, once the peer stream contracts and daemon event paths exist.

`persona-introspect` gained a `signal-persona-router` dependency pinned
to `branch = "main"`. The wider stable named-reference discipline is not
finished: `signal-core` still needs its stable API branch/bookmark/tag,
and downstream crates still need to consume that named reference.

`reports/designer-assistant/88-persona-engine-wide-audit-2026-05-16.md`
has a maintenance note marking its stale findings. Do not read findings
1, 5, or the router-facing part of 6 as current without that note.

## Next-session targets

1. Review and commit the three repo changes if the diffs still match the
   intended architecture.
2. Add `persona-introspect` to the full dev-stack smoke or create a
   sibling smoke that starts router plus introspect as separate daemons
   and verifies `PrototypeWitness.router_seen`.
3. Decide the next live introspection client: manager readiness/status is
   probably more useful than terminal because it closes the supervision
   loop.
4. Keep router one-shot Match as a prototype witness only. Do not grow it
   into timer polling.
5. Resume the stable named-reference work with `signal-core` first, then
   update the signal-persona contract family.

## Side notes

note: The Nix clean-source path did not include newly added test files in
two component repos. The working fix was to fold the new witnesses into
already tracked test files. If this recurs, the repo clean-source policy
should be corrected rather than normalized as a test-layout constraint.

note: The dev-stack smoke is now more valuable than the per-component
tests because it catches flag drift and flake-input drift that local
component tests cannot see.
