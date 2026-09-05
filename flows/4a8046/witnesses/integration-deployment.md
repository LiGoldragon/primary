# Integration and deployment witness

Date of observation: 2026-09-05. This witness records the exact portable
source pair, the validation boundary, the durable profile-only realization,
and the recovery procedure for the authorized activation. It does not record
an activation: no `ActivateNow`, profile switch, Home activation, service
restart, reboot, rollback, or retry has been submitted by this integration
worker.

## Portable source pair

The final Home producer is the pushed `integration-deployment-4a8046` bookmark
in `LiGoldragon/CriomOS-home` at
`fbceccc76dd9a161b79846c8c960788578a0bdf4`. It descends from current Home
main `a83210d3e0afd44fcdb9fa893fa582a22913146f` and carries:

* Codex `0.153.4` from `590bb08428a09596d9d5fbc3adf054d0027bc567`.
* The Home-side Wispr reconnect reset from
  `ff111978e72359d2f9057a129246d9a37cc10475`.
* The VSCodium removal from
  `befd92780ffe4c0ed9de002d73ec7aff158d4d91`, which removes the failing
  activation hook described in `activation-readiness.md`.
* Wispr Flow input `033231a1255024447c6a4183c41f4ea9c1fa063f`.
* A lock-file repair that removes only the three VSCodium inputs already
  removed from `flake.nix`: `claude-code-vsix`, `codex-chatgpt-vsix`, and
  `visualjj-vsix`.

The final consumer is the pushed `integration-deployment-4a8046` bookmark in
`LiGoldragon/CriomOS` at
`7a440b495003c60a8d32a23425390f18052280ec`. It descends from the observed
current consumer main `14a246f5b64c31d1208d9edd76f05acd9b4828b1` and pins the
Home producer above in both `flake.nix` and `flake.lock`. Its locked Home
source hash is `sha256-/pRCY847X3FPnUAE68Wk9gJObt+iq9griO7X1fJkDUk=`.

Both integration workspaces were clean after their commits and pushes. The
public `main` bookmarks have not been advanced by this worker.

## Validation state

The final consumer's read-only `nixosConfigurations` evaluation exposes the
single materialized target name `target`.

Direct standalone evaluation of CriomOS-home checks was deliberately not
treated as a green test: its unmaterialized flake requires the OS-provided
`system` input and stops with `CriomOS-home: no system input was provided`.
This is the expected boundary for this source; the affected Home checks must
be evaluated from the Lojix-projected consumer target. No affected durable
check is claimed green by this witness.

Lojix deployment 196 is the fresh validation path for the exact consumer. It
was admitted as a profile-only `Realize`, with `Horizon`, output
`homeConfigurations.li.activationPackage`, source policy `RequireImmutable`,
and builder specification `@/etc/nix/machines`. The daemon's remote build
invocation uses `--option max-jobs 0` and an explicit builder, so it does not
fall back to a local build. At this observation it is still in `Building` and
has no terminal result.

## Target and admission plan

The proposal source is an existing regular, non-symlinked file:
`/git/github.com/LiGoldragon/goldragon/proposal.datom`.

The direct identity probe for the required transport returned `ouranos` and
`li` for:

```text
ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome
```

The target selection is `UserEnvironment.li` on `goldragon/ouranos`. The
node's existing current user-environment ledger record is deployment 195,
whose immutable source is `14a246f5b64c31d1208d9edd76f05acd9b4828b1`.

After deployment 196 reaches `Completed / Succeeded` and the affected checks
are green against the final source, submit exactly one short admission request:

```sh
meta-lojix 'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=7a440b495003c60a8d32a23425390f18052280ec (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

`ActivateNow` is expected to restart the Codex owner. The request admission
will therefore be separated from observation: immediately preserve its
deployment identifier, then a fresh surviving session must query it through
the ordinary socket. Do not depend on the submitting tool connection through
that restart.

## Pre-activation baseline

Immediately before the pending realization completes, the ledger confirms
deployment 194 (`fd6e2752…`) and deployment 195 (`14a246f5…`) as completed
user-environment activations. Deployment 195 is the current Home generation.
The live profile resolves to
`/nix/store/prs01bm2rkxfvggc4sdld4vz5rksirz1-profile`; current-home resolves
to `/nix/store/wc70jrsx59lc6z5kqjy4a6d6hrjp6j20-home-manager-generation`.
The active `codex-remote-control.service` uses Codex `0.153.3`, is active and
running with `NRestarts=0`, and owns the expected socket at
`/home/li/.codex/app-server-control/app-server-control.sock`.

Orchestrate lock 784 reserves the profile root, current-home root, generated
Codex unit, and expected socket through the activation. This prevents a
second coordinated flow from changing those target paths while the final
activation is admitted and observed.

## Recovery handles

The in-progress realization survives this worker and is observed with:

```sh
lojix 'Query.ByDeployment.(196)'
```

For the later activation, replace `196` with the identifier returned by
`DeployAccepted`. Query until Lojix reports a terminal record. On success,
independently verify the ledger's current generation, Home Manager roots,
`~/.nix-profile`, generated Codex unit, one owner of the expected Codex
socket, active executable/version, and stable `NRestarts`. On failure, capture
the profile, roots, unit, process, socket, journal, and ledger record before
any retry.

## Sources

* `flows/4a8046/witnesses/activation-readiness.md`
* Lojix ordinary queries for deployments 195 and 196
* `meta-lojix` admission reply for deployment 196
* The final producer and consumer immutable source revisions listed above
* `/git/github.com/LiGoldragon/goldragon/proposal.datom`
