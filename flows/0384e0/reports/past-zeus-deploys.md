# Past Zeus CriomOS deployments

## 1. Flows that deployed or attempted to deploy CriomOS to Zeus

Most recent first:

| Flow | Approximate date | Outcome |
|------|-----------------|---------|
| 5a3ee4 | 2026-09-04 | Deployments 158, 162 failed (stale LAN transport); deployment 165 succeeded; Bird UE 166 failed (wrong SSH user), 167 succeeded; 181 succeeded |
| 01a05cd5 | 2026-09-04 | Deployment 125 Realize-only on stale LAN route (no activation); deployments 126–128 succeeded over hostname transport |
| 01a05833 | 2026-08-29 | Deployments 113 failed (eval assertion — Claude Remote Control workingDirectory); 114–115 partial (Codex WorkingDirectory literal, Claude trust scalar); 120–122 succeeded |
| 01a030b7 | 2026-08-24 | Deployment 53 failed activation (Clavifaber Dotos syntax); 54 TestActivation + 55 ActivateNow succeeded on corrected source |
| 01a02b46 | 2026-08-23 | Deployments 28 Evaluate + 29 Realize succeeded; deployment 30 TestActivation failed (CopyClosure timeout over Wi-Fi) |
| 966be8 | 2026-09-03 | Parent of 01a02b46/01a030b7. Deployment 150 failed (stale LAN route); deployment 151 succeeded. No verbatim commands in this lane |

Evidence status: every deployment number and terminal state above is traced to a witnessed Lojix query or a flow-lane record that attributes itself to a direct Lojix query. The 966be8 flow log describes deployments 150 and 151 in prose but contains no verbatim commands or witness files; 966be8 is the parent of 01a02b46 and 01a030b7 and summarizes their work.

## 2. Verbatim working request strings

### CompleteHost template (early form — stale LAN transport, old proposal basename)

Source: `flows/01a02b46/reports/zeusRequestInputs.md` and `flows/01a02b46/witnesses/zeusDeployment.md` (witnessed Lojix probes, 2026-08-23).

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.Host.(goldragon zeus CompleteHost /git/github.com/LiGoldragon/goldragon/datom.dotos github:LiGoldragon/CriomOS?rev=d04f6dafce19b7b4f093c35716739f36d75973ba (ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 Evaluate RequireImmutable Some.@/etc/nix/machines [])'
```

The same form with `Realize`, `TestActivation`, and `ActivateNow` substituted for `Evaluate`. Deployments 28 (Evaluate) and 29 (Realize) succeeded with this form; deployment 30 (TestActivation) failed at CopyClosure.

### CompleteHost corrected form (hostname transport)

Source: `flows/01a05cd5/log.md` and `flows/01a05cd5/witnesses/zeusTransport.md` (witnessed Lojix probes and SSH/Nix store probes, 2026-09-04).

The corrected transport pair, witnessed as reachable:

```
(ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome)
```

Deployments 126 (Realize), 127 (TestActivation), 128 (ActivateNow) all succeeded using this transport with CriomOS `2929538c510ce2f84bf5317cfe21f450d5140b9d`.

Flow 5a3ee4 independently reached the same corrected transport and succeeded with deployment 165 (CompleteHost) and 181 (CompleteHost).

### Proposal source path correction

Source: `flows/01a05c80/log.md` (psyche-approved skill correction).

The proposal source was renamed from `datom.dotos` to `proposal.datom`. The current path on disk is:

```
/git/github.com/LiGoldragon/goldragon/proposal.datom
```

The Lojix skill was corrected in Curriculum commit `b71104d1`. All deployments after this correction use `proposal.datom`.

### Ordinary query

Source: `flows/d098fa2d/witnesses/liveState.md` and `flows/7a9f4c12/witnesses/lojixState.md` (witnessed probes).

```sh
LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon zeus None)'
```

### UserEnvironment for Bird on Zeus (working form)

Source: `flows/5a3ee4/log.md` (flow prose, not a separate witness file).

Deployment 167 succeeded with root-mediated transport `(ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome)`. Deployment 166 failed with `ssh-ng://bird@zeus.goldragon.criome` because there is no SSH key for bird from Ouranos.

## 3. Rejected and failed request strings

### CopyClosure timeout — deployment 30

Source: `flows/01a02b46/witnesses/zeusDeployment.md`, `flows/01a02b46/witnesses/copyFailureMapping.md` (witnessed probes and code read).

Request: the early-form template with `TestActivation` and transport `(ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome)`.

Terminal reply (from Lojix query):
```
Failed Some.(683 683) Some.Failed.(CopyClosure BuilderUnreachable)
```

Actual cause (witnessed from Zeus SSH journal): the copy session ran exactly 2700 seconds (the Lojix effect timeout), then disconnected. The Wi-Fi transfer was too slow.

### CopyClosure — stale LAN transport — deployments 150, 158, 162

Source: `flows/966be8/log.md` (flow prose for 150), `flows/5a3ee4/log.md` (flow prose for 158/162).

Deployments 158 and 162 used `ssh-ng://root@192.168.18.95`; `nix copy` failed immediately with "No route to host." Zeus was no longer on LAN. Lojix mapped all to `BuilderUnreachable`.

### Activation failure — deployment 53 (Clavifaber Dotos syntax)

Source: `flows/01a030b7/log.md` and `flows/01a030b7/witnesses/lojixDeployments.md` (witnessed Lojix query).

Terminal reply:
```
Failed Some.Failed.(Activate ActivationFailed)
```

Cause: `complex-init.service` sent legacy Dotos syntax to Clavifaber 0.2.0 which expected curly Dotos. The partial test activation changed `/run/current-system` while leaving the persistent profile at generation 63.

### Eval assertion failure — deployment 113

Source: `flows/01a05833/log.md` (flow prose).

CompleteHost Realize 113 failed before build/activation because materialized evaluation asserted that the enabled Claude Remote Control policy requires an explicit absolute non-home workingDirectory.

### Activation defects exposed by TestActivation — deployments 115 and successive attempts before 120

Source: `flows/01a05833/log.md` (flow prose).

Three separate defects surfaced during test activations before the final successful 120–122 sequence:
1. Codex unit's WorkingDirectory was the literal `/home/li/primary`; Bird cannot traverse `/home/li`.
2. Obsolete scalar Claude trust format.
3. Hexis unable to traverse the legacy scalar during migration.

### FlakeReferenceMalformed — deployment 56

Source: `flows/01a030b7/witnesses/criomosB8xZeus.md` (witnessed Lojix probe).

Deployment 56 was immediately rejected as `FlakeReferenceMalformed`; no target action. The verbatim malformed reference is not recorded in the witness; the correct reference succeeded as deployment 57.

### UserEnvironment SSH key failure — deployment 166

Source: `flows/5a3ee4/log.md` (flow prose).

Bird UserEnvironment with `ssh-ng://bird@zeus.goldragon.criome` failed at CopyClosure — no SSH key for bird from Ouranos. Corrected to root-mediated transport.

### Cross-node misroute — deployment 49

Source: `flows/01a02fe5/log.md` and `flows/01a02fe5/witnesses/sshRecovery.md` (witnessed probes).

Deployment 49 requested the logical user environment for `goldragon zeus li` while routing copy and activation through `li@ouranos`. Lojix preserved both values verbatim: Horizon selected Zeus's identity, and activation installed that Zeus closure on Ouranos as Home generation 973. This broke SSH by selecting a keygrip with no local secret key.

## 4. Order of operations

Source: `flows/01a02b46/reports/zeusRequestInputs.md` (flow report), `flows/01a05833/log.md` (flow prose), `flows/01a05cd5/log.md` (flow prose), `flows/5a3ee4/log.md` (flow prose).

### Pre-deployment

1. Push all producer revisions before the consumer revision that pins them. Order: provider repo → CriomOS-home → CriomOS. Each must be an immutable pushed commit before the next pins it.
2. Verify the proposal source (`/git/github.com/LiGoldragon/goldragon/proposal.datom`) is an existing absolute regular non-symlink file.
3. Verify Zeus transport: SSH reachability (`ssh -o BatchMode=yes -o StrictHostKeyChecking=yes root@zeus.goldragon.criome`) and Nix store reachability (`nix store info --store ssh-ng://root@zeus.goldragon.criome`).
4. Verify Lojix daemon is running: `systemctl is-active lojix-daemon.service`, both sockets exist.

### Deployment sequence

Each action is a separate durable deployment with its own deployment ID. Lojix does not pass one stage's closure path into the next stage. Nix may reuse the same store path through its local store or configured substitutes when the inputs are identical, but each stage still receives a new deployment identity and produces its own terminal record.

1. **Evaluate** — evaluates only; proves the source compiles. Optional but recommended.
2. **Realize** — evaluates and builds the closure. Proves the build succeeds.
3. **TestActivation** — evaluates, builds, copies closure to target, and test-activates. Changes `/run/current-system` but not the persistent profile or boot default.
4. **ActivateNow** — evaluates, builds, copies, and persistently activates. Changes the persistent system profile and boot default.

After each `meta-lojix` submission, the reply is `DeployAccepted.(id (marker marker))` — admission only. Poll with:
```sh
LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon zeus None)'
```
until a terminal record appears (`Succeeded`, `Failed`, or `Rejected`).

### Post-deployment

Verify live state via SSH: `readlink /run/current-system`, `nixos-rebuild list-generations`, `systemctl --failed`, service status for Bird/Li Home Manager units.

## 5. Environment facts

Source: `flows/01a02b46/reports/zeusRequestInputs.md` (flow report), `flows/d098fa2d/reports/zeusUpdatePath.md` (flow report), `flows/3cb84d07/witnesses/lojixController.md` (witnessed probe).

| Variable | Value | Source |
|----------|-------|--------|
| `LOJIX_OWNER_SOCKET` | `/run/lojix/owner.sock` | witnessed in multiple flows |
| `LOJIX_ORDINARY_SOCKET` | `/run/lojix/ordinary.sock` | witnessed in multiple flows |
| Proposal source (current) | `/git/github.com/LiGoldragon/goldragon/proposal.datom` | current filesystem; psyche-approved correction in `flows/01a05c80/log.md` |
| Proposal source (old, stale) | `/git/github.com/LiGoldragon/goldragon/datom.dotos` | no longer exists on disk |
| Transport (current) | `(ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome)` | witnessed in `flows/01a05cd5/witnesses/zeusTransport.md` |
| Transport (stale, do not use) | `(ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome)` | Zeus left LAN; causes immediate "No route to host" |
| Hostname derivation | `zeus.goldragon.criome` = `<node>.<cluster>.<internal suffix>` | psyche-corrected derivation in `flows/966be8/vision/clusterData.md` |
| Builder | `Some.@/etc/nix/machines` | witnessed in `flows/01a02b46/reports/zeusRequestInputs.md` |

The daemon must be running (`lojix-daemon.service` active) before any request. Both socket paths are live only while the daemon is active.

## 6. Lessons, corrections, and traps

### Transport: do not use the LAN IP

Source: `flows/966be8/log.md` (correction from psyche), `flows/01a05cd5/log.md` (correction from psyche), `flows/5a3ee4/log.md` (diagnosis).

The direct-Ethernet IP `192.168.18.95` was a historical operational preference. Zeus left the LAN. Multiple flows (966be8, 5a3ee4, 01a05cd5) repeated this mistake. The correct transport is `(ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome)`, derived from cluster data as `<node>.<cluster>.<internal suffix>`.

**Psyche correction** (flows/966be8/vision/clusterData.md): "Your first proposal, 'put Zeus' current transfer and activation routes into cluster data,' seems to misunderstand what cluster data is. ... Inferring the name of the host from the cluster data is extremely straightforward. That's probably all that's missing: just an explanation of how one is derived from the other."

### Proposal source renamed

Source: `flows/01a05c80/log.md` (psyche-approved skill correction).

The Lojix skill previously said `datom.dotos`; the actual Lojix parser requires `proposal.datom`. The psyche approved the exact replacement. Using the old name will cause rejection.

### TestActivation changes live state even when it fails

Source: `flows/01a030b7/log.md` (flow prose), `flows/01a02b46/witnesses/zeusDeployment.md` (witnessed probe).

Deployment 53 failed activation but changed `/run/current-system` while leaving the persistent profile at the old generation. The Lojix ledger and the target's live state must be inspected separately after any activation failure.

### Lojix drops activation/copy stderr

Source: `flows/01a02b46/witnesses/copyFailureMapping.md` (witnessed code read and probes), `flows/58a86d/log.md` (flow prose).

`fail_pipeline` logs only the effect stage name and maps every `CopyClosure` failure to `BuilderUnreachable` and every `Activate` failure to `ActivationFailed`. The captured `nix copy` or activation stderr is not persisted. This has been a known diagnostic gap across multiple flows.

### Cross-node identity mismatch is not rejected

Source: `flows/01a02fe5/log.md` and `flows/01a02fe5/witnesses/sshRecovery.md` (witnessed probes).

Lojix accepts a request where the logical node (what is built) differs from the activation destination (which machine is changed). Deployment 49 installed a Zeus closure on Ouranos. The skill now says: "Before a state-changing deployment, verify that they identify the same node. If they do not, stop."

### UserEnvironment Bird requires root transport

Source: `flows/5a3ee4/log.md` (flow prose).

`ssh-ng://bird@zeus.goldragon.criome` fails because bird has no SSH key from Ouranos. Use `ssh-ng://root@zeus.goldragon.criome` for the Nix store URI and `root@zeus.goldragon.criome` for the SSH destination. (Lojix 0.20.3 also added automatic root-derived copy, but the explicit root form is the witnessed working path.)

### Same-host TestActivation killed the daemon (fixed in 0.20.2)

Source: `flows/01a05833/log.md` (flow prose).

On Ouranos, TestActivation 109 stopped `lojix-daemon` from its own service cgroup. This was fixed in Lojix 0.20.2 (commit `34a8e9c2e6af`). Zeus deployments are remote, so this trap does not apply there, but it matters if Ouranos is being deployed in the same session.

### Push producers before consumers

Source: `flows/01a02b46/reports/zeusRequestInputs.md` (flow report).

`RequireImmutable` requires an exact source revision. Push producer revisions before pushing the consumer revision that pins them. The order is: provider repo → CriomOS-home → CriomOS. Each immutable reference must be publicly resolvable before the next level pins it.

### Pending Datom migration (flow 542442, not yet live)

Source: `flows/542442/reports/lojix-implementation.md` and `flows/542442/reports/authored-skill-review.md` (flow reports, not deployed).

Flow 542442 is migrating the entire Lojix stack from Dotos to Datom. The changes include:
- Request syntax changes from parenthesized Dotos `Deploy.Host.(...)` to braced Datom `Deploy.Host.{ ... }`
- Proposal source changes from `proposal.datom` to `horizon-definition.datom`
- A new `SecretsInput` field added after `ProposalSource`: bare `NoSecrets` or `SecretsDirectory.<path>`
- Lojix advances from 0.20.x to 0.21.0 with store schema v5

**None of this is deployed.** The live daemon on Ouranos remains 0.20.x with Dotos syntax, `proposal.datom`, and store schema v4. The main flow must use the current live syntax, not the pending migration syntax. If the 542442 migration lands before or during deployment, the request shape changes.

## Sources

- `flows/01a02b46/witnesses/zeusDeployment.md` — witnessed Lojix probes, 2026-08-23
- `flows/01a02b46/witnesses/copyFailureMapping.md` — witnessed code read and probes
- `flows/01a02b46/witnesses/transportAndLink.md` — witnessed SSH/Nix transport probes
- `flows/01a02b46/reports/zeusRequestInputs.md` — flow report with typed templates
- `flows/01a030b7/log.md` — flow log, deployments 53–55
- `flows/01a030b7/witnesses/lojixDeployments.md` — witnessed Lojix query
- `flows/01a030b7/witnesses/criomosB8xZeus.md` — witnessed deployment and live-state
- `flows/d098fa2d/reports/zeusUpdatePath.md` — flow report with generic template
- `flows/d098fa2d/witnesses/pipeline.md` — witnessed code read of Lojix pipeline
- `flows/d098fa2d/witnesses/liveState.md` — witnessed Lojix query
- `flows/7a9f4c12/witnesses/lojixState.md` — witnessed Lojix query
- `flows/966be8/log.md` — flow log, deployments 150–151
- `flows/966be8/vision/clusterData.md` — psyche correction on transport derivation
- `flows/01a05833/log.md` — flow log, deployments 113–122
- `flows/01a05cd5/log.md` — flow log, deployments 125–128
- `flows/01a05cd5/witnesses/zeusTransport.md` — witnessed transport probes
- `flows/5a3ee4/log.md` — flow log, deployments 158–181
- `flows/58a86d/log.md` — flow log, deployments 190–195 (Ouranos only)
- `flows/01a02fe5/log.md` — flow log, cross-node misroute
- `flows/01a02fe5/witnesses/sshRecovery.md` — witnessed SSH recovery
- `flows/491750ff/witnesses/homeDeployment.md` — witnessed UserEnvironment deploy
- `flows/01a05c80/log.md` — proposal.datom correction
- `flows/542442/reports/lojix-implementation.md` — flow report, Datom migration (not deployed)
- `flows/542442/reports/authored-skill-review.md` — flow report, new Datom request syntax (not deployed)
- Current filesystem: `/git/github.com/LiGoldragon/goldragon/proposal.datom` exists; `datom.dotos` and `horizon-definition.datom` do not
