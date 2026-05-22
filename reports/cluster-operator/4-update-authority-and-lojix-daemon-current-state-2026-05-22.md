# Update authority and lojix daemon current state

## Summary

The new `lojix` daemon is a real working development daemon, but it is
not ready to ship as the Bird-on-Zeus update authority path.

The production path on Zeus still runs through `lojix-cli`, not through
`lojix-daemon`. Production `lojix-cli` can deploy FullOS, OS-only, and
home-only flows today, but system activation still assumes root SSH to
the target. There is no narrow local update helper, no Horizon
`SystemUpdateGrant`, and no per-user local privilege path yet.

The latest psyche clarification supersedes the older branch part of
`reports/cluster-operator/1-bird-zeus-local-update-authority-design.md`:
Bird/Aether should update from LiGoldragon `main` by default for now,
not from a Bird-specific system branch. Later this can move to a stable
tag policy, but the current raw production reference is `main`.

## Intent captured

The current correction was recorded in Spirit:

```text
record 176, topic zeus, Decision:
Bird/Zeus update authority uses LiGoldragon main by default, not per-user branches.
```

This means the helper policy should fill in production refs such as:

```text
github:LiGoldragon/CriomOS/main
github:LiGoldragon/CriomOS-home/main
```

instead of requiring Aether to maintain a branch as the normal update
source.

## What exists in the new lojix daemon

Repo: `/git/github.com/LiGoldragon/lojix`

Branch: `horizon-leaner-shape`

The daemon exists and is not just a report artifact:

- `lojix-daemon` binds a Unix socket.
- `lojix` is a thin client that talks only to `lojix-daemon`.
- Requests are framed through `signal-core` carrying `signal-lojix`
  records.
- `RuntimeRoot` routes requests to actors.
- `DeploymentLedger` uses `sema-engine` over redb.
- Generation queries read sema-backed generation records.
- Deployment observation subscriptions can stream live events.
- Build-only deployment jobs can project Horizon, run Nix, pin realized
  outputs as GC roots, record built generations, and push observations.
- `CriomeAuthorization` exists as an actor boundary before effects.

Verification I ran:

```text
cd /git/github.com/LiGoldragon/lojix
cargo test
```

Result: all tests passed. The green suite covers socket round trips,
streaming observations, sema persistence, typed configuration
boundaries, and build-only deployment witnesses.

## What does not exist in the new lojix daemon

The daemon is not a production update daemon yet.

Missing pieces:

- Real activation is explicitly rejected. `BuildOnlyRequest` accepts
  build-only deployments and rejects activation/eval actions before any
  tool runs.
- Real Criome RPC is absent. `CriomeAuthorizationPolicy::production`
  is currently `Unavailable` until the Criome socket client lands; tests
  use a fake grant policy.
- Peer daemon communication is not implemented. `RuntimeConfiguration`
  has `peer_daemons`, but there is no deployed daemon-to-daemon protocol
  for distributed updates.
- The current code still uses `signal-core`, `SignalVerb`, and direct
  request matching. It has not migrated to the latest `signal-frame` /
  `signal-executor` / daemon-local `Command` and `Effect` architecture
  described in the recent signal redesign reports.
- The daemon is not wired into production CriomOS. `CriomOS` still
  consumes `lojix-cli`; `lojix-daemon` is described as planned/new-stack
  infrastructure.

This is good progress, but it is not the shortest path to Bird updating
Zeus.

## What exists in production lojix-cli

Repo: `/git/github.com/LiGoldragon/lojix-cli`

Production `lojix-cli` is the active deploy tool. It already has:

- `FullOs`
- `OsOnly`
- `HomeOnly`
- projection through `horizon-rs`
- generated flake input materialization
- local and remote home activation paths
- root-over-SSH system activation paths
- Boot, Switch, Test, and BootOnce system action handling

Verification I ran:

```text
cd /git/github.com/LiGoldragon/lojix-cli
cargo test
```

Result: all tests passed.

The important limitation: system activation is still remote-root shaped.
`SystemActivation` constructs `ssh root@<target>` invocations. For
Bird-on-Zeus, that is exactly the boundary we do not want.

## Bird on Zeus current authority state

Current code facts:

- Bird exists in `goldragon/datom.nota`.
- Bird has a Zeus public key.
- Bird has `Medium` trust, not `Max`.
- `horizon-rs` gives broad admin/root SSH material only through the
  `Max` trust path.
- Therefore Bird does not get root SSH today, which is correct.

Missing authority pieces:

- `horizon-rs` has no `SystemUpdateGrant`.
- `goldragon/datom.nota` has no Bird-on-Zeus update grant.
- CriomOS has no `criomos-local-update` helper.
- CriomOS has no sudo rule granting Bird exactly that helper.
- `lojix-cli` has no local system activation mode for a root-owned
  helper running on the target node.
- There are no Nix witnesses proving that the grant does not add Bird to
  `wheel`, `nixdev`, root SSH, or trusted Nix user lists.

## Recommended shipping path

Do not wait for the new daemon RPC stack to ship Bird-on-Zeus updates.
Ship a narrow production slice first:

1. Add `SystemUpdateGrant` to `horizon-rs`.
2. Add the Goldragon fact granting Bird update authority on Zeus.
3. Project the grant only onto the target node's Horizon view.
4. Add a CriomOS module that renders `/run/current-system/sw/bin/criomos-local-update`.
5. Add a command-specific sudo rule allowing Bird to run only that helper.
6. Teach production `lojix-cli` a local system activation target, so the
   helper can run `nix-env -p /nix/var/nix/profiles/system --set ...`
   and `switch-to-configuration` locally instead of SSHing to
   `root@zeus`.
7. Make the helper accept only a tiny NOTA request, probably:

```nota
(LocalUpdate HomeProfile)
(LocalUpdate FullSwitch)
```

The helper fills in the rest:

- cluster: `goldragon`
- node: `zeus`
- user: caller, must be `bird`
- source: policy-selected Goldragon proposal
- system ref: `github:LiGoldragon/CriomOS/main`
- home ref: `github:LiGoldragon/CriomOS-home/main`
- builder and substituters: policy-selected defaults

The helper should not accept arbitrary proposal paths, arbitrary flake
refs, arbitrary target nodes, or arbitrary users.

## Constraint witnesses needed

Horizon:

- `system_update_grant_round_trips_from_nota`
- `system_update_grant_projects_only_on_target_node`
- `bird_medium_trust_does_not_gain_admin_ssh`

CriomOS:

- `system_update_grant_installs_one_sudo_command`
- `system_update_grant_does_not_add_wheel_or_nixdev`
- `system_update_grant_does_not_add_root_authorized_key`
- `local_update_helper_rejects_ungranted_user`
- `local_update_helper_rejects_wrong_node`
- `local_update_helper_uses_ligoldragon_main_refs_by_default`

`lojix-cli`:

- `local_system_activation_does_not_construct_ssh_invocation`
- `remote_system_activation_still_constructs_ssh_invocation`
- `local_boot_once_uses_systemd_run_without_ssh`

End to end:

- Build the Zeus projection with Bird's grant.
- Build the Zeus CriomOS config.
- Assert the generated sudo rule names exactly the helper path.
- Assert Bird remains outside broad admin groups.

## Open questions

### 1. Should the first helper expose only two verbs?

I recommend the first public helper surface be:

```nota
(LocalUpdate HomeProfile)
(LocalUpdate FullSwitch)
```

That matches the current psyche statement: Bird can ask agents to update
her home profile or do a full system switch. `Test` and `BootOnce` are
useful engineering actions, but they may be internal policy expansions
rather than user-facing helper requests.

### 2. Should the first implementation patch production or the new daemon?

I recommend production first. The new daemon is the better long-term
shape, but it lacks activation, real Criome RPC, daemon-to-daemon
coordination, current signal-executor migration, and production service
wiring. The production slice is smaller and directly deployable to Zeus.

### 3. Should the helper be shell or Rust?

I recommend Rust if this is more than a one-hour experiment. The helper
is a root boundary. It should parse a tiny NOTA record, reject unknown
shapes precisely, and construct the full `lojix-cli` request from
compiled policy. A shell wrapper is acceptable only if it accepts no
dynamic fields except an exact action token.

