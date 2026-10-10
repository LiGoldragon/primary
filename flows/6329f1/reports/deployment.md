# Deployment: Orchestrate 0.27.0 on Ouranos

Witnessed 2026-09-04 by subflow of flow 6329f1.

## 1. CriomOS Input Bump

Orchestrate Lock 632 acquired on `/git/github.com/LiGoldragon/CriomOS`.

```
$ grep orchestrate.url /git/github.com/LiGoldragon/CriomOS/flake.nix
    orchestrate.url = "github:LiGoldragon/orchestrate/9585484738ce0748d0cf23f0431285f9693ca2ec";
```

```
$ nix flake lock --update-input orchestrate
warning: updating lock file "/git/github.com/LiGoldragon/CriomOS/flake.lock":
* Updated input 'orchestrate':
    'github:LiGoldragon/orchestrate/dadd537bbd2ed2ffc5260fffc5735f9f020cc774?narHash=sha256-bzz9oi2fl3ffG6fY8c437Cc2nNc5q2y4QptZH8zVvik%3D' (2026-08-29)
  -> 'github:LiGoldragon/orchestrate/9585484738ce0748d0cf23f0431285f9693ca2ec?narHash=sha256-mDpKFUQsiosF%2BPUwLws0Jp4e3Ef68I3SKfHjSIkEfY0%3D' (2026-09-04)
```

Lock file verified: `orchestrate` node `rev` is `9585484738ce0748d0cf23f0431285f9693ca2ec`.

```
$ git commit -m "Pin orchestrate 0.27.0 (9585484738ce)"
[main 83b3a8f] Pin orchestrate 0.27.0 (9585484738ce)
 2 files changed, 5 insertions(+), 5 deletions(-)

$ git push origin main
To ssh://github.com/LiGoldragon/CriomOS
   36b13be..83b3a8f  main -> main
```

CriomOS rev: `83b3a8f51bec2e2bdf7bec8e61adc81ae089e45e`

Orchestrate Lock 632 released.

## 2. Lojix Deployment

### Request

```
$ LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix \
    'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=83b3a8f51bec2e2bdf7bec8e61adc81ae089e45e (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

### Reply

```
DeployAccepted.(156 (4022 4022))
```

### Observation

Polled `Query.ByDeployment.(156)` every 15 seconds. Intermediate state was `Building` through 8 polls. Terminal state reached at poll 9:

```
Queried.([] [(156 156 (UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.83b3a8f51bec2e2bdf7bec8e61adc81ae089e45e) Some.(4022 4022) Completed Some.(4055 4055) Some.Succeeded)] (4059 4059))
```

Terminal state: **Succeeded**

## 3. Service Restart and Verification

### Pre-restart observation

The `ActivateNow` activation automatically restarted `orchestrate-nexus`.
By the time the terminal `Succeeded` was observed, the service was already
running the 0.27.0 binary (active since 11:28:34 CEST). The pre-restart
`Observe.Locks` was therefore captured from the 0.27.0 nexus, not the 0.26.0
nexus. This is acceptable: the locks survived the activation restart.

```
$ orchestrate 'Observe.Locks'
Observed.Locks.[ { 440 WisprAuthWitness run_wispr_live_witness [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness ] "“ create isolated workspace for one authorized witness” " } { 441 WisprEdgeProxy implement_wispr_edge_proxy [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588 ] "“ implement offline EdgeProxy witness in isolated workspace” " } ]
```

### Manual restart

```
$ systemctl --user restart orchestrate-nexus
(exit 0)
```

### Service status

```
$ systemctl --user status orchestrate-nexus
  orchestrate-nexus.service - Orchestrate Nexus path-reservation service
     Loaded: loaded (/home/li/.config/systemd/user/orchestrate-nexus.service; enabled; preset: ignored)
     Active: active (running) since Fri 2026-09-04 11:29:39 CEST; 6s ago
 Invocation: 3cb988c5169d499f9d1f740f96adab79
   Main PID: 3029476 (orchestrate-nex)
      Tasks: 1 (limit: 37849)
     Memory: 604K (peak: 2.5M)
        CPU: 7ms
     CGroup: /user.slice/user-1001.slice/user@1001.service/app.slice/orchestrate-nexus.service
             3029476 /nix/store/pnwkgajkgzlipvg38yyp1xzngc2nkl08-orchestrate-0.27.0/bin/orchestrate-nexus

Sep 04 11:29:39 ouranos systemd[2305]: Started Orchestrate Nexus path-reservation service.
Sep 04 11:29:39 ouranos orchestrate-nexus[3029476]: orchestrate-nexus ready
```

ExecStart store path: `/nix/store/pnwkgajkgzlipvg38yyp1xzngc2nkl08-orchestrate-0.27.0/bin/orchestrate-nexus`

### Observe.Locks (post-restart)

```
$ orchestrate 'Observe.Locks'
Observed.Locks.[ { 440 WisprAuthWitness run_wispr_live_witness [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness ] "“ create isolated workspace for one authorized witness” " } { 441 WisprEdgeProxy implement_wispr_edge_proxy [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588 ] "“ implement offline EdgeProxy witness in isolated workspace” " } ]
```

Both pre-existing locks (440, 441) preserved with correct IDs, names, flows,
paths, and reasons. Output uses spaced datom delimiters and curly-quoted reasons.

### Ethos (no argument)

```
$ orchestrate
; Orchestrate Lock signal -- the ordinary wire contract.
;
; The Lock family: acquire, release, observe coordination locks.
; Every lock carries an integer id, a name, a flow, absolute paths,
; and a reason.

Signal.{ 1 0 0 }

[]

[ Lock.LockRequest  Release.LockId  Observe.ObserveSelection ]

[ Locked.Lock  Released.Lock  Observed.Observation
  LockRejected.LockRejection  ReleaseRejected.ReleaseRejection ]

[ LockId.Integer
  LockName.Text
  FlowId.Text
  LockPath.Text
  LockReason.Text
  LockRequest.{ LockName FlowId Vector<LockPath> LockReason }
  Lock.{ LockId LockName FlowId Vector<LockPath> LockReason }
  LockOverlap.{ LockPath Lock }
  LockRejection.[ DuplicateName.Lock  PathOverlap.LockOverlap ]
  ReleaseRejection.[ UnknownLockId ]
  ObserveSelection.[ Locks ]
  Observation.[ Locks.Vector<Lock> ] ]

; Orchestrate CLI client failure vocabulary.
; Library.{ 0 27 0 }
; [ protos:[ Integer Extent ]
;   datomic:[ Fault ] ]
; [ Situated.{ Option<Extent> Fault }
;   ClientFailure.[ Unreadable.Situated  Unreachable.{ Text Text }  Refused.Refusal ] ]
; []
; []
(exit 0)
```

### Lock/Release round-trip

```
$ orchestrate 'Lock.{ DeployWitness 6329f1 [ /tmp/deploy-witness-6329f1 ] “deployment verification” }'
Locked.{ 633 DeployWitness 6329f1 [ /tmp/deploy-witness-6329f1 ] "“ deployment verification” " }

$ orchestrate 'Release.633'
Released.{ 633 DeployWitness 6329f1 [ /tmp/deploy-witness-6329f1 ] "“ deployment verification” " }
```

### Nonsense (datom fault)

```
$ orchestrate 'Nonsense'
Unreadable.{ None Corporal.{ [] Shape.{ Variant Nonsense } } }
(exit 1)
```

Datom fault on stderr, exit 1. Correct.

### meta-orchestrate (no argument)

```
$ meta-orchestrate
; Orchestrate meta signal -- the privileged wire contract.
;
; Configuration: set socket paths for the Nexus.

Signal.{ 1 0 0 }

[]

[ Configure.Configure ]

[ Configured.Configure  ConfigurationRejected.ConfigurationRejection ]

[ OrdinarySocketPath.Text
  MetaSocketPath.Text
  Configure.{ OrdinarySocketPath MetaSocketPath }
  ConfigurationRefusal.[ InvalidConfiguration ]
  ConfigurationRejection.{ Configure ConfigurationRefusal } ]

; Meta-orchestrate CLI client failure vocabulary.
; Library.{ 0 13 0 }
; [ protos:[ Integer Extent ]
;   datomic:[ Fault ] ]
; [ Situated.{ Option<Extent> Fault }
;   ClientFailure.[ Unreadable.Situated  Unreachable.{ Text Text }  Refused.Refusal ] ]
; []
; []
(exit 0)
```

### Lojix node confirmation

```
$ LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon ouranos None)'
```

Deployment 156 is `Current` for UserEnvironment with source rev
`83b3a8f51bec2e2bdf7bec8e61adc81ae089e45e` and store path
`/nix/store/6r7z59czs9s7j9b83w97r9y1jxh01lhk-home-manager-generation`.

## 4. Records Updated

### ProtoformStack.datom

`Deployment` enum gained `Deployed.{ Text Text }` variant. Value changed from
`BranchesPushed` to `Deployed.{ ouranos 83b3a8f }`.

### UPGRADES.md

Rollout section corrected on orchestrate main (commit `281e070`, pushed).
Changes: input bump is CriomOS (not CriomOS-home) due to `follows` override;
deployment is via Lojix `Deploy.UserEnvironment` with `ActivateNow`, not
`nixos-rebuild switch`; activation restarts the service automatically.

## Final State

| Item | Value |
|------|-------|
| CriomOS rev | `83b3a8f51bec2e2bdf7bec8e61adc81ae089e45e` |
| Lojix deployment ID | 156 |
| Lojix terminal state | Succeeded |
| Orchestrate store path | `/nix/store/pnwkgajkgzlipvg38yyp1xzngc2nkl08-orchestrate-0.27.0/bin/orchestrate-nexus` |
| Home-manager generation | `/nix/store/6r7z59czs9s7j9b83w97r9y1jxh01lhk-home-manager-generation` |
| Service status | active (running) since Fri 2026-09-04 11:29:39 CEST |
| Locks preserved | 440 (WisprAuthWitness), 441 (WisprEdgeProxy) |
| Issues | None |

## Sources

- `nix flake lock --update-input orchestrate` in CriomOS, 2026-09-04
- `git commit`, `git push` in CriomOS, 2026-09-04
- `meta-lojix Deploy.UserEnvironment` via owner socket, 2026-09-04
- `lojix Query.ByDeployment.(156)` via ordinary socket, 2026-09-04 (9 polls)
- `orchestrate 'Observe.Locks'` pre- and post-restart, 2026-09-04
- `systemctl --user restart orchestrate-nexus`, 2026-09-04
- `systemctl --user status orchestrate-nexus`, 2026-09-04
- `orchestrate` (ethos), `orchestrate Lock/Release`, `orchestrate Nonsense`, 2026-09-04
- `meta-orchestrate` (ethos), 2026-09-04
- `lojix Query.ByNode.(goldragon ouranos None)`, 2026-09-04
- `deployment-ground.md` (pre-deployment state), flow 6329f1
