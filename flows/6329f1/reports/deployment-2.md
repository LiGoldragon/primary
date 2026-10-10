# Deployment 2: Orchestrate 0.29.0 and claude-answers 0.5.0 on Ouranos

Witnessed 2026-09-04 by subflow of flow 6329f1.

## Pre-deploy verification

UPGRADES.md entries for 0.28.0 and 0.29.0 both confirm no store or wire
change. `git diff 9585484..1c0dd769 -- src/store.rs src/transport.rs` shows
only rustfmt formatting changes (import line wrapping, expression line
breaking). No logic change.

## 1. CriomOS-home Input Bump

Orchestrate Lock 655 acquired on `/git/github.com/LiGoldragon/CriomOS-home`.

```
$ nix flake lock --update-input claude-answers
* Updated input 'claude-answers':
    'github:LiGoldragon/claude-answers/651c1b35afa6ec773c30ddc693c01e2d1260eea8?narHash=sha256-HoXKsbjbQDY/E7yGs7Eg%2BSLWfVTanqQ6iY0rhIpMV2U%3D' (2026-08-12)
  -> 'github:LiGoldragon/claude-answers/a2edb6777b602b19349e179df64a515b79ace8e9?narHash=sha256-PBBsHu8rYPrYWFaMm9Yra0w1oCzft%2BAvQBAsjdtUlcE%3D' (2026-09-04)
```

Lock file verified: `claude-answers` node `rev` is `a2edb6777b602b19349e179df64a515b79ace8e9`.

```
$ git commit -m "Pin claude-answers 0.5.0 on the ProtoformStack train"
[main f1d56e3] Pin claude-answers 0.5.0 on the ProtoformStack train
 1 file changed, 3 insertions(+), 3 deletions(-)

$ git push origin main
To ssh://github.com/LiGoldragon/CriomOS-home
   b36502d..f1d56e3  main -> main
```

CriomOS-home rev: `f1d56e3eb72a721a346897e894f75a8f26a51bd3`

Orchestrate Lock 655 released.

## 2. CriomOS Input Bumps

Orchestrate Lock 657 acquired on `/git/github.com/LiGoldragon/CriomOS`.

flake.nix updated:
- `orchestrate.url` set to `github:LiGoldragon/orchestrate/1c0dd769c82720ad9c45ca70adb2ec5bd3a1af40`
- `criomos-home.url` set to `github:LiGoldragon/CriomOS-home/f1d56e3eb72a721a346897e894f75a8f26a51bd3`

```
$ nix flake lock --update-input orchestrate --update-input criomos-home
* Updated input 'criomos-home':
    'github:LiGoldragon/CriomOS-home/b36502d1188f6541651cb0ae57a93b9126007807' (2026-09-04)
  -> 'github:LiGoldragon/CriomOS-home/f1d56e3eb72a721a346897e894f75a8f26a51bd3' (2026-09-04)
* Updated input 'criomos-home/claude-answers':
    'github:LiGoldragon/claude-answers/651c1b35afa6ec773c30ddc693c01e2d1260eea8' (2026-08-12)
  -> 'github:LiGoldragon/claude-answers/a2edb6777b602b19349e179df64a515b79ace8e9' (2026-09-04)
* Updated input 'orchestrate':
    'github:LiGoldragon/orchestrate/9585484738ce0748d0cf23f0431285f9693ca2ec' (2026-09-04)
  -> 'github:LiGoldragon/orchestrate/1c0dd769c82720ad9c45ca70adb2ec5bd3a1af40' (2026-09-04)
```

Lock file verified: orchestrate `1c0dd769c82720ad9c45ca70adb2ec5bd3a1af40`, criomos-home `f1d56e3eb72a721a346897e894f75a8f26a51bd3`, claude-answers `a2edb6777b602b19349e179df64a515b79ace8e9`.

```
$ git commit -m "Deploy orchestrate 0.29.0 and claude-answers 0.5.0"
[main ef4383a] Deploy orchestrate 0.29.0 and claude-answers 0.5.0
 2 files changed, 13 insertions(+), 13 deletions(-)

$ git push origin main
To ssh://github.com/LiGoldragon/CriomOS
   2c34e94..ef4383a  main -> main
```

CriomOS rev: `ef4383aff7d027e8b0580ff0f5c9cf21eee40816`

Orchestrate Lock 657 released.

## 3. Pre-deploy Lock Snapshot

```
$ orchestrate 'Observe.Locks'
Observed.Locks.[ { 639 DialectSkills 6329f1 [ /home/li/wt/github.com/LiGoldragon/Curriculum/Curriculum-DialectSkills-6329f1 ] “draft protos datom ethos skills on Curriculum branch” } { 440 WisprAuthWitness run_wispr_live_witness [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness ] “[create isolated workspace for one authorized witness]” } { 441 WisprEdgeProxy implement_wispr_edge_proxy [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588 ] “[implement offline EdgeProxy witness in isolated workspace]” } { 656 ethos-zero-copy 6329f1 [ /git/github.com/LiGoldragon/ethos-zero /home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-zero-copy-6329f1 ] “derive Copy for unit-only enums” } { 658 protos-situated 6329f1 [ /git/github.com/LiGoldragon/protos ] “add PartialEq Eq to Situated” } ]
```

## 4. Lojix Deployment

### Request

```
$ LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix \
    'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=ef4383aff7d027e8b0580ff0f5c9cf21eee40816 (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

### Reply

```
DeployAccepted.(160 (4157 4157))
```

### Observation

Polled `Query.ByDeployment.(160)` every 15 seconds. Terminal state reached:

```
Queried.([] [(160 160 (UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.ef4383aff7d027e8b0580ff0f5c9cf21eee40816) Some.(4157 4157) Completed Some.(4190 4190) Some.Succeeded)] (4194 4194))
```

Terminal state: **Succeeded**

## 5. Service Restart and Verification

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
     Active: active (running) since Fri 2026-09-04 14:05:05 CEST; 6s ago
 Invocation: d3ed5f657f8246f9a0431500b04a903f
   Main PID: 3234310 (orchestrate-nex)
      Tasks: 1 (limit: 37849)
     Memory: 612K (peak: 2.2M)
        CPU: 4ms
     CGroup: /user.slice/user-1001.slice/user@1001.service/app.slice/orchestrate-nexus.service
             3234310 /nix/store/pbf5ym1klj47x5yay6d6nscx4fjhwa35-orchestrate-0.29.0/bin/orchestrate-nexus

Sep 04 14:05:05 ouranos systemd[2305]: Started Orchestrate Nexus path-reservation service.
Sep 04 14:05:05 ouranos orchestrate-nexus[3234310]: orchestrate-nexus ready
```

ExecStart store path: `/nix/store/pbf5ym1klj47x5yay6d6nscx4fjhwa35-orchestrate-0.29.0/bin/orchestrate-nexus`

### Observe.Locks (post-restart)

```
$ orchestrate 'Observe.Locks'
Observed.Locks.[ { 639 DialectSkills 6329f1 [ /home/li/wt/github.com/LiGoldragon/Curriculum/Curriculum-DialectSkills-6329f1 ] “draft protos datom ethos skills on Curriculum branch” } { 440 WisprAuthWitness run_wispr_live_witness [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness ] “[create isolated workspace for one authorized witness]” } { 441 WisprEdgeProxy implement_wispr_edge_proxy [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588 ] “[implement offline EdgeProxy witness in isolated workspace]” } { 656 ethos-zero-copy 6329f1 [ /git/github.com/LiGoldragon/ethos-zero /home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-zero-copy-6329f1 ] “derive Copy for unit-only enums” } ]
```

Pre-deploy locks 639, 440, 441, 656 preserved with correct IDs, names, flows,
paths, and reasons. Lock 658 (protos-situated) was released by another flow
during the build -- not a deployment concern.

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

Library.{ { 0 29 0 } [ protos:[ Extent ] datomic:[ Fault ] signal_orchestrate:Refusal ] [ Situated.{ Option<Extent> Fault } ClientFailure.[ Unreadable.Situated Unreachable.{ Text Text } Refused.Refusal ] ] [] [] }
(exit 0)
```

The ethos includes the generated client-failure Library at version `{ 0 29 0 }`.

### Lock/Release round-trip

```
$ orchestrate 'Lock.{ Deploy029 6329f1 [ /tmp/deploy029-6329f1 ] “second deployment” }'
Locked.{ 659 Deploy029 6329f1 [ /tmp/deploy029-6329f1 ] “second deployment” }

$ orchestrate 'Release.659'
Released.{ 659 Deploy029 6329f1 [ /tmp/deploy029-6329f1 ] “second deployment” }
```

### Datom fault (malformed input)

```
$ orchestrate 'Lock.{ broken'
Unreadable.{ Some.{ 5 13 } Structural.{ { 5 13 } Unclosed.Braced } }
(exit 1)
```

Exact match with the expected output.

### Unreachable (bad socket)

```
$ ORCHESTRATE_SOCKET=/no/such.sock /nix/store/pbf5ym1klj47x5yay6d6nscx4fjhwa35-orchestrate-0.29.0/bin/orchestrate 'Observe.Locks'
Unreachable.{ /no/such.sock "No such file or directory (os error 2)" }
(exit 1)
```

Note: the installed wrapper unconditionally exports `ORCHESTRATE_SOCKET`, so
the direct binary was used for this test.

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

Library.{ { 0 29 0 } [ protos:[ Extent ] datomic:[ Fault ] meta_signal_orchestrate:Refusal ] [ Situated.{ Option<Extent> Fault } ClientFailure.[ Unreadable.Situated Unreachable.{ Text Text } Refused.Refusal ] ] [] [] }
(exit 0)
```

### claude-answers (no argument)

```
$ claude-answers
[]
(exit 0)
```

No answers in the latest transcript for the current project -- expected
behavior for `Latest` with no matching question-answer pairs.

### claude-answers All

```
$ claude-answers All
[ { “What makes the Nomos-side type “not the same thing” as its Logos counterpart?” “Escape holes” “” } { “Should the Nomos/Logos phase split be enforced by the Rust compiler, or is validation-time enforcement by the existing TemplateValue substrate sufficient?” explain “” } { “Where should the “no holes remain” guarantee live for the Nomos-to-Logos transformation?” “> pub visibility: Visibility,           // fixed: always literal\n\ncould we possibly want to support an evaluation to resolve visibility? wouldnt that create a problem? Isnt the point to have complete flexibility in nomos to create any level of sugar syntax in ethos?  ” “” } { “In what order should the skills/standards agent work the four beads?” “Traits first (Recommended)” “” } { “What is the canonical exception list for the impls-under-traits standard?” “Broad + audit note (Recommended)” “” } ]
(exit 0)
```

Five question-answer datoms returned from all project transcripts.

### claude-answers store path

```
$ readlink -f $(command -v claude-answers)
/nix/store/51s4yif9931i0s4v94csyl138716616w-claude-answers-0.5.0/bin/claude-answers
```

### Lojix node confirmation

```
$ lojix 'Query.ByNode.(goldragon ouranos None)'
```

Deployment 160 is `Current` for UserEnvironment with source rev
`ef4383aff7d027e8b0580ff0f5c9cf21eee40816` and store path
`/nix/store/sni5x7yx75nx7c0zq9fkvrs3g9c9n6gs-home-manager-generation`.

## 6. ProtoformStack.datom

Updated `/home/li/primary/release-trains/ProtoformStack.datom`:
- Type shape changed from `Deployment` to `Vector<Deployment>` (Library `2 0 0`)
- Added 7 second-wave stops (8--14): datomic 0.9.0, ethos-zero 1.2.0,
  signal-orchestrate 0.20.0, meta-signal-orchestrate 0.14.0, orchestrate 0.29.0,
  claude-answers 0.5.0, curriculum-deploy 0.5.0
- Deployment value changed from single `Deployed.{ ouranos 83b3a8f }` to
  `[ Deployed.{ ouranos 83b3a8f }  Deployed.{ ouranos ef4383a } ]`
- Not committed per the brief.

## Final State

| Item | Value |
|------|-------|
| CriomOS-home rev | `f1d56e3eb72a721a346897e894f75a8f26a51bd3` |
| CriomOS rev | `ef4383aff7d027e8b0580ff0f5c9cf21eee40816` |
| Lojix deployment ID | 160 |
| Lojix terminal state | Succeeded |
| Orchestrate store path | `/nix/store/pbf5ym1klj47x5yay6d6nscx4fjhwa35-orchestrate-0.29.0/bin/orchestrate-nexus` |
| claude-answers store path | `/nix/store/51s4yif9931i0s4v94csyl138716616w-claude-answers-0.5.0/bin/claude-answers` |
| Home-manager generation | `/nix/store/sni5x7yx75nx7c0zq9fkvrs3g9c9n6gs-home-manager-generation` |
| Service status | active (running) since Fri 2026-09-04 14:05:05 CEST |
| Locks preserved | 639 (DialectSkills), 440 (WisprAuthWitness), 441 (WisprEdgeProxy), 656 (ethos-zero-copy) |
| Issues | None |

## Sources

- `nix flake lock --update-input claude-answers` in CriomOS-home, 2026-09-04
- `git commit`, `git push` in CriomOS-home, 2026-09-04
- `nix flake lock --update-input orchestrate --update-input criomos-home` in CriomOS, 2026-09-04
- `git commit`, `git push` in CriomOS, 2026-09-04
- `orchestrate 'Observe.Locks'` pre-deploy, 2026-09-04
- `meta-lojix Deploy.UserEnvironment` via owner socket, 2026-09-04
- `lojix Query.ByDeployment.(160)` via ordinary socket, 2026-09-04
- `systemctl --user restart orchestrate-nexus`, 2026-09-04
- `systemctl --user status orchestrate-nexus`, 2026-09-04
- `orchestrate 'Observe.Locks'` post-restart, 2026-09-04
- `orchestrate` (ethos), `orchestrate Lock/Release`, `orchestrate 'Lock.{ broken'`, 2026-09-04
- `ORCHESTRATE_SOCKET=/no/such.sock` direct binary test, 2026-09-04
- `meta-orchestrate` (ethos), 2026-09-04
- `claude-answers` (no arg), `claude-answers All`, `readlink -f $(command -v claude-answers)`, 2026-09-04
- `lojix Query.ByNode.(goldragon ouranos None)`, 2026-09-04
- `deployment.md` (first deployment reference), flow 6329f1
- `repin2.md` (what changed since first deployment), flow 6329f1
