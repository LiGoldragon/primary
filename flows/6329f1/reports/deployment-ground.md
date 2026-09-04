# Deployment Ground: Orchestrate 0.27.0 on Ouranos

Witnessed 2026-09-04 by subflow of flow 6329f1.
Method: `hostname`, `systemctl --user status`, `orchestrate 'Observe.Locks'`,
`nix store ping --store ssh://prometheus`, `git status`, `git log`, `git branch`,
`nixos-version`, `home-manager generations`, Lojix `Query.ByNode`, `nix build`,
`orchestrate-upgrade-preflight`, mount-namespace rehearsal nexus startup,
`Observe.Locks` against rehearsal nexus. No production state was modified.

---

## 1. Host Identity

- Hostname: `ouranos`
- Lojix identity: `goldragon/ouranos`
- System: NixOS 26.11.20260813.0e251e2 (Zokor)
- Running system store path: `/nix/store/sd0h59z66mggbqnnd5r8am5ai3hbbd34-nixos-system-ouranos-26.11.20260813.0e251e2`
- Current home-manager generation: 1001 at `/nix/store/5k0k95w2vnimfnfxq7f8hk3y2d353yy3-home-manager-generation`

## 2. Running Orchestrate Service

- Binary: `/nix/store/pbjprrhnas2vijypwz87zrnzla92f8d5-orchestrate-0.26.0/bin/orchestrate-nexus`
- Active since: 2026-08-29 06:37:25 CEST (6 days)
- PID: 2052947
- Sema store: `~/.local/state/orchestrate-nexus/orchestrate-nexus.sema` (454656 bytes)
- Ordinary socket: `/run/user/1001/orchestrate-nexus/orchestrate.sock`
- Meta socket: `/run/user/1001/orchestrate-nexus/meta-orchestrate.sock`

## 3. Build and Switch Method

### System (NixOS)

CriomOS at `/git/github.com/LiGoldragon/CriomOS`. The system is deployed via
Lojix `Deploy.Host` (CompleteHost, NixosSystemdBootV1). Current CompleteHost
deployment: 138 (Lojix `Current`).

### Home (home-manager)

CriomOS-home at `/git/github.com/LiGoldragon/CriomOS-home`, consumed through
CriomOS's `criomos-home` input. Home is deployed via Lojix
`Deploy.UserEnvironment` (HomeManagerNixProfileV1). Current UserEnvironment
deployment: 155 (Lojix `Current`), source revision
`36b13be289e94a31f8260017953bae9dabe8366a` (CriomOS main).

Recent ouranos UserEnvironment deployments reference CriomOS (not CriomOS-home
directly), using the output selector `(homeConfigurations.li.activationPackage)`
from CriomOS's flake outputs. This means CriomOS's `follows` override
(`criomos-home.inputs.orchestrate.follows = "orchestrate"`) is effective:
only CriomOS's `orchestrate` input pin needs updating.

Neither `nixos-rebuild switch --flake` nor standalone `home-manager switch` is
the deployed method. Lojix owns the deployment.

### Current Orchestrate Input Pins

CriomOS `flake.nix`:
```
orchestrate.url = "github:LiGoldragon/orchestrate/dadd537bbd2ed2ffc5260fffc5735f9f020cc774"
```
This is v0.26.0 (origin/main of orchestrate).

CriomOS-home `flake.nix` (own, overridden by `follows`):
```
orchestrate.url = "github:LiGoldragon/orchestrate/e0f3bc5e8b963089e560383b2a4eb7d30cda1f82"
```
This is v0.25.0. Irrelevant when deployed through CriomOS (the `follows` override
carries CriomOS's pin).

### Running System vs CriomOS Main

CriomOS main: `36b13be` ("Advance CriomOS-home fixed ChatGPT input").
Current UserEnvironment deployment source: `36b13be`. Matches.
Current CompleteHost deployment 138 source: `7cd12262874fc5f6c1ed133dc3ef56c669d29959`.
CriomOS main has advanced since the last Host deployment.

No `configuration-revision` file exists at `/run/current-system/`.

## 4. Checkout State

### CriomOS (`/git/github.com/LiGoldragon/CriomOS`)

- Detached HEAD at `36b13be` (same as `main` and `origin/main`)
- Working tree clean, nothing to commit
- No uncommitted or unpushed state that a deploy commit would collide with

### CriomOS-home (`/git/github.com/LiGoldragon/CriomOS-home`)

- Detached HEAD at `433958a` (same as `main` and `origin/main`)
- Working tree clean, nothing to commit
- No uncommitted or unpushed state that a deploy commit would collide with

## 5. Remote Builder

```
nix store ping --store ssh://prometheus
```
Result: reachable. Store URL `ssh://prometheus`. The configured Nix builder at
`/etc/nix/machines` is `ssh-ng://nix-ssh@prometheus.goldragon.criome`.

Builds should use `Some.@/etc/nix/machines` as the optional builder field in
Lojix deployments.

## 6. Exact Command Sequence for the Deployer

### Prerequisites

1. Orchestrate's `ProtoformStack` branch (tip `e631bad92ef2`) is merged to main
   with the documentation commit on top. Note the final pushed revision as
   `<ORCH-REV>`.

### Source update

2. In `/git/github.com/LiGoldragon/CriomOS/flake.nix`, replace the orchestrate
   input:
   ```
   orchestrate.url = "github:LiGoldragon/orchestrate/<ORCH-REV>";
   ```

3. Lock update:
   ```
   nix flake lock --update-input orchestrate
   ```
   (in the CriomOS checkout)

4. Commit and push:
   ```
   git add flake.nix flake.lock
   git commit -m "Pin orchestrate 0.27.0 (<ORCH-REV>)"
   git push origin main
   ```
   Note the pushed CriomOS revision as `<CRIOM-REV>`.

### Deployment

5. Deploy the home environment via Lojix:
   ```
   LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix \
     'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=<CRIOM-REV> (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
   ```
   Wait for `DeployAccepted.(<deploy-id> ...)`.

6. Poll until terminal:
   ```
   LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByDeployment.(<deploy-id>)'
   ```
   Repeat until terminal state (`Succeeded`, `Rejected`, or `Failed`).

7. After successful activation, restart the user service (home-manager does not
   auto-restart changed user services; no `startServices` is configured):
   ```
   systemctl --user restart orchestrate-nexus
   ```

### Verification

8. Confirm the new binary:
   ```
   systemctl --user status orchestrate-nexus
   ```
   ExecStart should reference `orchestrate-0.27.0`.

9. Confirm wire format and lock preservation:
   ```
   orchestrate 'Observe.Locks'
   ```
   Locks must appear in spaced datom format with all pre-existing lock IDs,
   names, flows, paths, and reasons intact.

10. Confirm Lojix agrees:
    ```
    LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon ouranos None)'
    ```
    Current UserEnvironment deployment should be the new `<deploy-id>`.

## 7. Store Compatibility Rehearsal

### Method

1. Copied `~/.local/state/orchestrate-nexus/orchestrate-nexus.sema` (454656
   bytes, live 0.26.0 store) to a scratch directory. The live service was not
   stopped or touched.

2. Built orchestrate at `e631bad92ef2` (ProtoformStack tip) via `nix build` in
   a detached worktree at
   `/home/li/wt/github.com/LiGoldragon/orchestrate/orchestrate-rehearsal-6329f1`,
   remote-built on `ssh://prometheus`. Build succeeded. Orchestrate Lock 631
   held for the worktree path during the rehearsal.

3. Ran `orchestrate-upgrade-preflight` (0.27.0 binary) against the copied store:
   ```
   active legacy PathLock rows: 0
   ```
   The 0.27.0 preflight reads the 0.26.0 store successfully. No legacy rows
   block the upgrade.

4. Started the 0.27.0 `orchestrate-nexus` against the copied store using
   `unshare --mount --map-root-user` to shadow the live socket directory with
   an empty tmpfs. The nexus resumed the persisted socket configuration from the
   0.26.0 store, bound its sockets, and printed `orchestrate-nexus ready`.

5. Ran `Observe.Locks` through the 0.27.0 client against the rehearsal nexus.

6. Stopped the rehearsal nexus, removed the scratch copy and the worktree,
   released Orchestrate Lock 631.

### Rehearsal Observe.Locks (0.27.0 nexus, 0.26.0 store)

```
Observed.Locks.[ { 440 WisprAuthWitness run_wispr_live_witness [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness ] "[create isolated workspace for one authorized witness]" } { 441 WisprEdgeProxy implement_wispr_edge_proxy [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588 ] "[implement offline EdgeProxy witness in isolated workspace]" } { 631 orchestrate-rehearsal-6329f1 6329f1 [ /home/li/wt/github.com/LiGoldragon/orchestrate/orchestrate-rehearsal-6329f1 ] "[store compatibility rehearsal for orchestrate 0.27.0 deployment]" } ]
```

### Live Observe.Locks (0.26.0 nexus)

```
Observed.Locks.[{440 WisprAuthWitness run_wispr_live_witness [/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness] [create isolated workspace for one authorized witness]} {441 WisprEdgeProxy implement_wispr_edge_proxy [/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588] [implement offline EdgeProxy witness in isolated workspace]} {631 orchestrate-rehearsal-6329f1 6329f1 [/home/li/wt/github.com/LiGoldragon/orchestrate/orchestrate-rehearsal-6329f1] [store compatibility rehearsal for orchestrate 0.27.0 deployment]}]
```

### Comparison

All three locks appear in both replies with identical IDs, names, flows, paths,
and reasons:

| Field    | Lock 440           | Lock 441              | Lock 631                       |
|----------|--------------------|-----------------------|--------------------------------|
| ID       | 440                | 441                   | 631                            |
| Name     | WisprAuthWitness   | WisprEdgeProxy        | orchestrate-rehearsal-6329f1   |
| Flow     | run_wispr_live_witness | implement_wispr_edge_proxy | 6329f1                    |
| Path     | listener-wispr-auth-witness | listener-wispr-edge-proxy-01a05588 | orchestrate-rehearsal-6329f1 |
| Reason   | create isolated workspace... | implement offline EdgeProxy... | store compatibility rehearsal... |

The 0.27.0 output uses spaced datom (spaces between fields, quoted reasons with
curly quotes) vs 0.26.0's compact datom (no spaces, bracket-delimited reasons).
The semantic content is identical.

### Wire incompatibility (expected)

The 0.27.0 ordinary client cannot speak to the 0.26.0 nexus:
```
Unreachable.{ /run/user/1001/orchestrate-nexus/orchestrate.sock "failed to fill whole buffer" }
```
This is the expected wire format change between signal-orchestrate versions.
The new client requires the new nexus. After restart, the installed wrapper
will use the 0.27.0 client against the 0.27.0 nexus.

### Verdict

**Compatible.** The 0.27.0 nexus reads the 0.26.0 sema store, resumes its
persisted configuration, and serves all existing locks with correct content.
No migration step, `orchestrate-upgrade-preflight` remediation, or store reset
is required. The upgrade is a drop-in restart.

## Sources

- `hostname` on ouranos, 2026-09-04
- `systemctl --user status orchestrate-nexus` on ouranos, 2026-09-04
- `orchestrate 'Observe.Locks'` (live 0.26.0), 2026-09-04
- `LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon ouranos None)'`, 2026-09-04
- `nix store ping --store ssh://prometheus`, 2026-09-04
- `git status`, `git log`, `git branch` in CriomOS and CriomOS-home checkouts, 2026-09-04
- `nixos-version`, `readlink /run/current-system`, 2026-09-04
- `nix build` of orchestrate at e631bad92ef2 via ssh://prometheus, 2026-09-04
- `orchestrate-upgrade-preflight` (0.27.0) against copied 0.26.0 store, 2026-09-04
- `unshare --mount` rehearsal: 0.27.0 nexus against copied 0.26.0 store, 2026-09-04
- `Observe.Locks` (0.27.0 client against rehearsal nexus), 2026-09-04
- `flows/6329f1/reports/orchestrate-edge.md` section 5 (Deployment), witnessed 2026-09-04
- `flows/966be8/log.md` (Zeus Lojix deployment evidence)
- `flows/01a038be/witnesses/codexHomeActivation.md` (ouranos UserEnvironment evidence)
- CriomOS `flake.nix` (`orchestrate.url`, `criomos-home.inputs.orchestrate.follows`)
- CriomOS-home `modules/home/profiles/min/orchestrate.nix`
