# Multi-host occupied runtime baseline

Captured read-only in the required order on 2026-11-13. Canonical destinations are
`<node>.goldragon.criome`, established by the goldragon cluster data and retained
deployment/builder transports. Each SSH command required `hostname` and `id -un`
to establish node and user; no alternate destination was tried.

## Observations

### ouranos

`li@ouranos.goldragon.criome` answered as hostname `ouranos`, user `li` (uid 1001).
The Home Manager profile is exactly
`/nix/store/sd47c969srp0gh5kz86c2v658nr81x84-home-manager-generation` (Lojix
generation 527); `~/.nix-profile` resolves to
`/nix/store/l38l3igqhdig1cvl5i8pa12wp86ivc4i-profile`.

The occupied declared and loaded user services are:

| unit | unit store file | live/declarative executable | state and relevant behavior |
|---|---|---|---|
| `codex-remote-control.service` | `0cz1…-codex-remote-control.service/...` | `4p67nm261bqy549q2isd4ifydqrfqy48-codex-0.167.1/bin/codex` | active/running; PID 2676; `Restart=always`; `KillMode=control-group`; no drop-ins |
| `codex-remote-control-next.service` | `4npk…-codex-remote-control-next.service/...` | `g2sfx3dccpi3294i1p70vafpaa84jfb8-codex-next-0.158.0-alpha.9/bin/codex` | active/running; PID 2701; `Restart=no`; `KillMode=process`; `After=` and `Conflicts=` the recovery unit; no drop-ins |
| `codex-remote-control-next-5ck97j38j3sb.service` | `4v0f…-codex-remote-control-next-5ck97j38j3sb.service/...` | `r0k59hi2q6di7xhmqxp11vygy4hclzyy-codex-next-candidate-0.161.0-alpha.2/bin/codex` | active/running; PID 2727; `Restart=on-failure`; `KillMode=control-group`; no drop-ins |
| `flow-nexus-0540.service` | `l4p1…-flow-nexus-0540.service/...` | `fs53xwvgp9kbam4sbc25671hdrvnl37q-flow-configured-0.54.7/bin/flow-nexus-daemon` | active/running; PID 1016330; `Restart=on-failure`; `KillMode=control-group`; no drop-ins |
| `flow-configure-0540.service` | `kglm…-flow-configure-0540.service/...` | `9mh4…-configure-flow-0540/bin/configure-flow-0540` | active/exited oneshot; `Restart=no`; requires/after Flow Nexus and is wanted by it; no drop-ins |

All three server PIDs' `/proc/<pid>/exe` and command lines agree with their loaded
units. Stable and next therefore match the intended universal occupied selections
`4p67…` and `g2sf…`; Flow matches intended daemon `fs53…`. The configure command's
Nexus body is `qz73…-flow-0540-nexus.datom`, which maps the stable model family to
compiled client `1qc6…-codex-stable-flow-client`; live gpt-6 panes instead use the
preserved `43h6…-codex-next-flow-client`, as that body specifies.

The five exact static-unit SHA-256 values and full unit texts/properties are in
`raw/ouranos-unit-hashes.txt` and `raw/ouranos.txt`. The Flow unit hash is the known
actual-527 `4b119b…`. Current Herdr continuity evidence names panes/sessions for
Field core 374411 and Mind core 1541ef, both with executable `43h6…`; full identifiers
are retained at the end of `raw/ouranos.txt`. The generation-527 query bodies needed
for later comparison remain at `flows/d09f73/generation527-flow-query-bodies.txt`.

The `Requires=flow-nexus-0540.service` relation above is recorded only as a unit
property; it establishes no stop or restart propagation result.

### zeus

Canonical SSH to `li@zeus.goldragon.criome` timed out before hostname/user evidence.
No runtime, profile, unit, process, pane, or query-state fact was obtained.

### prometheus

Canonical SSH to `li@prometheus.goldragon.criome` timed out before hostname/user
evidence. No runtime, profile, unit, process, pane, or query-state fact was obtained.

## Conflicts and unknowns

No occupied-path conflict is observed on ouranos. Zeus and Prometheus remain wholly
unknown, so this inventory cannot establish a universal selection or authorize a
shared-main change. Their canonical access must succeed and all of the same evidence
must be captured before source publication or any host's separately authorized
switch. Prometheus is the builder/AP and remains last and alone in the stated future
sequence.

The new Home candidate has no materialized generation in this lane. Candidate static
unit diffs, pinned sd-switch reachability, full gate, and actual old/candidate query
comparison therefore remain source/proof requirements. Immediately before each
future switch, all live paths, PIDs, profiles, pane/session identifiers and unit
properties require fresh revalidation; this report is baseline evidence only.

## Raw evidence

- `raw/ouranos.txt`
- `raw/ouranos-unit-hashes.txt`
- `raw/zeus.txt`
- `raw/prometheus.txt`
