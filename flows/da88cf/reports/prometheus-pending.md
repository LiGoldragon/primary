# Prometheus pending deploy: running system vs declared main

Read-only survey from ouranos, 2026-09-25 ~21:20–21:35 CST. Nothing was deployed, built, pushed or submitted. Grades: **W** = witnessed by this subflow, **I** = inferred, **C** = claimed by another flow's record, **U** = unknown.

## Headline

1. Prometheus runs CriomOS `da85c4a9` (branch `prometheus-usb-bus-property-5f38bc`). That revision is **not on CriomOS main**. Lojix did not activate it: it was switched in by hand over root SSH on 09-24 at 21:03. **W**
2. CriomOS main (`d193bafc`, 2026-09-25 20:08; it moved from `f09f3c83` while this survey ran) lacks 13 branch commits. Among them are the Prometheus USB-downlink binding fix and the Lojix 7 pin (`a67f5773`). Main still pins Lojix `c4bba4fa`, which is 6.0.0. **W**
3. **So a deploy of main as it stands would regress Prometheus**: the USB bridge binding and the Lojix 7 package would both be lost. The same would happen to Ouranos, whose Nexus is Lojix 7.0.0. Before any deploy, main has to integrate the branch. **I**, from the diff.
4. The "stale Horizon materialization" is not a Lojix-side blocker for a Horizon-mode deploy. Both the Prometheus and Ouranos `complete-host/horizon/horizon.json` that Lojix currently holds carry `node.machine.hardware`. The stale input was a separately supplied tree dated June 19. **W** for the files, **I** for the attribution.

## 1. What Prometheus runs now (all W, over `ssh -o BatchMode=yes prometheus.goldragon.criome`)

| Item | Value |
|---|---|
| `nixos-version --json` | `26.11.20260813.0e251e2`, nixpkgs `0e251e24a4f2…` |
| `/run/current-system` | `/nix/store/7f8kpzcnj3x03p5057fvs91k6wjvjwqz-nixos-system-prometheus-26.11.20260813.0e251e2` |
| `/run/booted-system` | the same path |
| `/nix/var/nix/profiles/system` | `system-55-link`, which resolves to the same path. Set 2026-09-24 21:03:42 CST, and the only generation link left |
| `nix-env --list-generations` | refused as user li (`system.lock: Permission denied`), so `ls -l` of the profiles was used instead |
| deriver | `/nix/store/0baaavlazpangvbn6cm2gd3g1sjhjh29-…drv` |
| uptime / boot | booted Fri 2026-09-25 21:15:44 CST; clocks on both hosts agree. The brief's "~21:57" does not match Prometheus's own journal |
| `systemctl --failed` | 0 units |
| relevant running units | `nix-serve`, `tailscaled`, `yggdrasil` (no lojix, flow, orchestrate, headscale, hydra or harmonia) |

Running == booted == current profile: **yes (W)**.

**Provenance of generation 55.**
- Journal of boot -1: root SSH from ouranos's Yggdrasil address `201:6de1:…:fb1d`, then `switching to system configuration /nix/store/7f8kpzcn…` at 09-24 21:03:43. **W**
- The Codex transcript of Field Astra 5f38bc (`rollout-2026-09-24T15-53-42-01a0d568…`) names the source as "CriomOS `da85c4a9e75595ba6908d0ebcd8eec9cd39d9552`". **C**
- Confirmed independently: evaluating `github:LiGoldragon/CriomOS?rev=da85c4a9…#nixosConfigurations.target.config.system.build.toplevel.drvPath` against Lojix's current Prometheus complete-host inputs gives exactly `0baaavlazpangvbn6cm2gd3g1sjhjh29`. **W**

## 2. What Lojix says

Cluster is `goldragon` and nodes are `prometheus` and `ouranos`. The ordinary socket is `/run/lojix/ordinary.sock`. The Nexus is `lojix-7.0.0` (`lojix.service`). **W**

**Owner-socket mismatch (W):** the environment sets `LOJIX_OWNER_SOCKET=/run/lojix/owner.sock`, but the socket that exists is `/run/lojix/meta.sock`. `lojix-meta` will not connect until `LOJIX_OWNER_SOCKET=/run/lojix/meta.sock` is supplied. 38de5b noted this too.

**`Query.ByNode.{ goldragon prometheus None }` (W).** The generations list is **empty**: Lojix has no Current or Recent generation for Prometheus. Deployments:

| # | Action | CriomOS rev | Terminal |
|---|---|---|---|
| 5 | Evaluate | 5c10f5d7 | Failed Eval (test-vm-host null address) |
| 6 | Evaluate | 5dc34239 | Succeeded |
| 8 | Evaluate | 5807f8e9 | Failed Eval (assertions) |
| 11 | Evaluate | 38c5bd51 | Succeeded |
| 12 | Realize | 38c5bd51 | Failed Build (NAR downloads from `nix.prometheus` timed out) |
| 16 | Evaluate | 9d93d621 | Succeeded |
| 17, 18 | Realize | 9d93d621 | Succeeded |
| 19 | ActivateNow | 9d93d621 | Failed Activate (bootloader: `nix-env --list-generations` interrupted) |
| 30 | Evaluate | eebeab5a | Failed Eval (`05-test-vm-vmt0` address null; fixed by `f9343c68` "Accept both VmHost field spellings") |
| 31 | TestActivation | f9343c68 | Failed Build. Partial-file NAR downloads of large `.gguf` model files (Nemotron-120B, GLM-4.7) from `nix.prometheus`; then interrupted. 5f38bc's log says it terminated 31 to take the store lock |

**`Query.ByNode.{ goldragon ouranos None }` (W).** Current CompleteHost is generation 4 at CriomOS `36653a12`. Current UserEnvironment is generation 27 at `cef11110`. Since then, Lojix has recorded no host deploy. The running ouranos system contains Lojix 7.0.0, so the host changed outside Lojix. **I**

**Horizon cluster data (W).**
- `goldragon` main is `8c4d03de` (2026-09-20). It pins horizon-rs `ee8d6f8d`, which is an ancestor of horizon-rs main `b45d6ad4`.
- The proposal store path `/nix/store/p61bn3w1qgl3lhx5gm96crw1f1qlr0gg-horizon-definition/horizon-definition.datom` exists: regular file, 0444, 6079 bytes. Per `flows/00f95a/materialization-ouranos-flow-0.10.7/report.md` it is the output of goldragon `8c4d03de`.

**"Stale Horizon materialization", concretely.**
- Source: `flows/b7da5d/receipts/flow-0107-declarative-preflight.md`. CriomOS `f09f3c83` evaluated "with the supplied Lojix materialized inputs" failed at `modules/nixos/metal/default.nix:21`, `attribute 'hardware' missing` at `horizon.node.machine.hardware`, and "the used Horizon materialization records June 19". Relayed by 38de5b as "stale Horizon materialization blocks the Evaluate-only path". **C**
- Lojix's live materializations do have the field:
  - `/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/horizon/horizon.json` (09-12) has `hardware` (12 cores, ThinkPadT14Gen5Intel).
  - `…/prometheus/complete-host/horizon/horizon.json` (09-24 14:05) has `hardware` (8 cores, GMKtec EVO-X2, 128 GiB).
  - **W**
- The June-dated trees are `…/ouranos/os-only` (06-20) and `full-os` / `home` (07-03). They are the likely stale input. **I**
- Horizon-mode deploys re-materialize from the proposal on each request: deployment 30's lock-update message shows the inputs refreshed at `lastModified` 2026-09-24. **W**
- The blocker is therefore a hand-supplied stale tree plus the old Lojix 6 pin on CriomOS main. It is not Lojix state. **I**

## 3. Declared source vs what is running

**CriomOS main** (`git ls-remote`, W): `d193bafca6d7848d8fa3813533ceb78f3228a07e`, 2026-09-25 20:08 -06:00, "Update Ouranos field-clj home package". Commits on main today:
- `d193baf` pins Home `478b4ea0`
- `f09f3c8` pins Home `5d647e96`, Flow 0.10.7
- `4f63afe` pins field-clj

**On `da85c4a9` (running) but not on main (13 commits, W):**
- `da85c4a` Bind USB downlinks by stable udev bus role (networkd.nix, router, new check)
- `88900f2` Herdr Codex next-home
- `1f8f70b`, `462051b`, `a414198` Message pre-open preservation
- `69ee992`, `4f24e46` Herdr predecessor adoption
- `742bc9c`, `77544a8` Flow runtime endpoints
- `8dff77e` Flow 0.6 Home with compatible Lojix
- **`123a91f` Pin compatible Lojix (`a67f5773`, 7.0.0)**
- `068e06e`, `e9f8714` Flow pins

The branch's Home pin `04446e78` has diverged from Home main `478b4ea0`: 16 commits ahead and 7 behind (GitHub compare, W). Its extra commits are the Herdr, Message and Claude-bypass repairs.

**Other unmerged CriomOS branches from the last two days (W):**
- `flow07-ouranos-b7da5d` (+15)
- `flow-main-opencode-luna6` (+14)
- `flow-final-aba74675-luna6` (+13)
- `prometheus-usb-downlink-5f38bc` (+1)
- `field-astra-5f38bc-flow-pins` (+12)
- `field/flow-message-deploy-eb7bae` (+1)

All the Flow-lineage branches carry the Lojix `a67f5773` pin; main does not. Older ones:
- `proposal/348e7b-prometheus-single-model` holds `9d93d621` and `38c5bd51`, the 09-16 Qwen-only LargeAi catalog and Prosody. Neither is on main.
- Main pins criomos-lib `6e3bcb08`. CriomOS-lib main `c74b2224` is "Keep only Qwen3.5-122B on LargeAi nodes, the living's word 2026-09-16". So the living's 09-16 catalog word is neither running nor on main. Main still pulls the Nemotron and GLM gguf closures that broke deployment 31.

**Pin table.** Main lock = CriomOS `d193baf` lock or Home `478b4ea0` lock. Running = `da85c4a9`. Remote main head from `gh api` / `git ls-remote` (W).

| Input (via) | Pinned on main | Running (da85c4a9) | Remote main head | Behind main? | Moved tonight (09-25)? |
|---|---|---|---|---|---|
| criomos-home (CriomOS) | 478b4ea0 | 04446e78 (diverged) | 478b4ea0 | no, but divergent from running | 4 commits |
| lojix (CriomOS) | c4bba4fa (6.0.0) | a67f5773 (7.0.0, branch `lojix-horizon-datom31-00f95a`, +2 on lojix main) | c4bba4fa | lojix main is itself behind the needed 7.0.0 | 0 |
| orchestrate (CriomOS, Home) | 9070cbb8 | 9070cbb8 | 9070cbb8 | no | 0 |
| nixpkgs | 0e251e24 | 0e251e24 | 0e251e24 | no | 0 |
| criomos-lib | 6e3bcb08 | 6e3bcb08 | c74b2224 | yes (Qwen-only catalog, 09-16) | 0 |
| spirit | 008d8ca0 | 008d8ca0 | 6aa87018 | yes | 1 |
| clavifaber | d0488014 | ? | 4b719005 (v0.6.0) | yes (09-12) | 0 |
| flow (Home) | 8df890ba (0.10.7) | older (0.6 line) | 34aaf787 (0.12.2) | yes | 25 commits, 0.10.7→0.12.2 |
| field-clj (Home) | 75d77597 | absent/older | 75d77597 | no | 11 |
| aggregator (Home) | f777eb2a | ? | cc3ec4fd (0.8.1) | yes | 2, bump to 0.8.1 |
| message (Home) | fe0d0456 | ? | 93306407 | yes (09-18) | 0 |
| herdr (Home, upstream herdrdev v0.8.2) | 9eb52145 | ? | U (not a LiGoldragon repo) | U | U |
| messenger-clj | not a Home input yet | none | dfcf91f0 | n/a | 53. Lock 6820 (00f95a) is adding `modules/home/profiles/min/messenger-clj.nix` now |
| ethos-zero | transitive only | | cf7dd128 | U (transitive pins not traced) | 7 |
| signal-lojix / meta-signal-lojix | transitive via lojix | | ff023945 / 631d832e | a67f5773's meta pair `b500561f` is an ancestor of meta main | 0 |
| goldragon (cluster data) | proposal from 8c4d03de | same | 8c4d03de | no | 0 |
| horizon-rs | via goldragon ee8d6f8d | same | b45d6ad4 | 4 behind, ancestor | 0 |

Other LiGoldragon inputs behind main, all with no commits tonight: agent, annas-mcp, claude-answers, CriomOS-lib, harness, listener, mirror (deprecated), noctalia, repository-ledger, prompt-relay-source. Full list with revisions: scratchpad `heads.tsv`.

**Drv comparison (W, same Prometheus inputs):**
- running `da85c4a9` gives `0baaav…`
- `864e01b` (merge base) gives `zkrrvr4l…`
- `f09f3c83` gives `2cfv1z62…`

Main differs from what is running.

## 4. Deployment path

**Mode: `Horizon`, not `Direct`.** 00f95a's packet records that Direct mode loses capabilities. Every Prometheus deployment Lojix has recorded (5–31) used Horizon-materialized inputs. **C/W**

**Activation.** CriomOS `ARCHITECTURE.md` (main):

> Deploying to a large-AI node … use the safe `BootOnce` / boot-mode activation path rather than `Switch` … until console or out-of-band access and operator sign-off exist.

That makes the action `ScheduleBootOnce` (or `SetBootProfile`), not `ActivateNow`. On 09-24 5f38bc switched live under the living's explicit waiver (`flows/5f38bc/log.md` §"Immediate Prometheus deployment authority"). No such waiver is on record for tonight. **U**

**Shape reference.** No receipt shows a Lojix-succeeded Prometheus activation: Lojix has never reached a Prometheus generation. The nearest shapes are:
- the Ouranos packet `flows/00f95a/materialization-ouranos-flow-0.10.7/lojix-evaluate.request`, the current Lojix 7 grammar;
- Lojix deployment 19's witnessed transport `root@prometheus.goldragon.criome`.

`flows/eb7bae/materialization-20260924/lojix-preflight.request` is retired and wrong-target: BaseHost, `nix-ssh` transport, selector `nixosConfigurations.prometheus`. Do not use it.

**Forms, in order.** `<C>` is the integrated CriomOS main revision (40 hex). Submit each only after the previous one terminates `Succeeded`, re-querying with `Query.ByDeployment`.

```text
LOJIX_OWNER_SOCKET=/run/lojix/meta.sock lojix-meta 'Deploy.Host.{ goldragon prometheus CompleteHost /nix/store/p61bn3w1qgl3lhx5gm96crw1f1qlr0gg-horizon-definition/horizon-definition.datom SecretsDirectory./git/github.com/LiGoldragon/goldragon/secrets github:LiGoldragon/CriomOS?rev=<C> { ssh-ng://root@prometheus.goldragon.criome root@prometheus.goldragon.criome } Horizon { nixosConfigurations.target.config.system.build.toplevel } NixosSystemdBootV1 Evaluate RequireImmutable Some.@/etc/nix/machines [] }'
```

then the same request with `Realize` in place of `Evaluate`, then with `ScheduleBootOnce`, followed by an operator-attended reboot.

Notes on the forms:
- **Secrets.** `SecretsDirectory.<path>` is the `signal_lojix::SecretsInput::SecretsDirectory` variant (`meta-signal-lojix/tests/generated_contract.rs`). `goldragon/secrets` holds the same four `.sops` files as Lojix's current Prometheus secrets materialization. **W** for the file names, **I** that this is the right source. `NoSecrets` only suits Evaluate. The sibling Headscale report writes `SecretsDirectory.{…}`; the glued form above follows the variant-payload grammar and `flows/542442/reports/authored-skill-review.md`.
- **Proposal.** If the Headscale/Tailscale slice changes goldragon, rebuild `.#horizon-definition` and substitute the new store path.
- **Order across hosts.** The sibling Headscale plan wants Ouranos deployed first (controller), then Prometheus.

**Risk (I, from deployment 31 and `df`).**
- Lojix realizes the closure through ouranos's store (`nix build --max-jobs 0 --builders @/etc/nix/machines` on ouranos). Prometheus's closure contains very large gguf models, and ouranos `/nix` has 75 GB free (92% used).
- With main's criomos-lib `6e3bcb08` catalog, Realize will again try to pull the Nemotron-120B and GLM files onto ouranos.
- Moving to criomos-lib `c74b2224` (Qwen-only, the living's 09-16 word) shrinks that closure. Whether Lojix can realize on the target store without routing through ouranos is **U**.

**Producer-before-consumer pushes that `RequireImmutable` needs:**
1. **lojix.** `a67f5773` exists only on branch `lojix-horizon-datom31-00f95a`; lojix main is `c4bba4fa` (6.0.0). A pushed branch revision resolves immutably, so it is not strictly required. But the policy "fixes on main" needs it merged to lojix main first, and CriomOS main pinned to it. Its Horizon (`ee8d6f8d`) and meta (`b500561f`) producers are already on their mains.
2. **Flow.** If 0.12.2 is to be declared: `34aaf787` is on flow main. 00f95a holds lock 6820 to pin Flow and messenger-clj into Home. Wait for that push.
3. **aggregator 0.8.1** (`cc3ec4fd`) is on main, if Home is to take it. Whether tonight's plan includes it is **U**.
4. **CriomOS-home.** Integrate the `04446e78` lineage (Herdr, Message, Claude-bypass repairs) with main `478b4ea0` plus 00f95a's pins. Push the result as Home main `H`.
5. **criomos-lib.** Already on main (`c74b2224`); only a CriomOS repin is needed.
6. **goldragon.** Only if the Headscale slice changes cluster data. Then push it, and rebuild the proposal.
7. **CriomOS.** Merge `prometheus-usb-bus-property-5f38bc` into main. Pin lojix `a67f5773` (or its main successor), Home `H`, and criomos-lib as decided. Then evaluate on Prometheus-built inputs and push as `<C>`. This is the `main-feature-integration` shape; it is not decided here.

## 5. Ownership and locks

**Deploy ownership.**
- `flows/b7da5d/log.md` (latest entry): after Fable da88cf merges, "Field Sol … deploy Ouranos then Prometheus through typed Lojix". Fable holds a Field-mutation hold. So Field Sol b7da5d is the planned deployer, and da88cf gates integration. **C**
- `flows/00f95a/log.md:9`: "Field's separate Prometheus deployment remains assigned to its Terra worker". That is 5f38bc's `prometheus_recovery`, which produced gen 55 out-of-band. **C**
- The Lojix producer/consumer owner 753e69 is retired; Mind is to name a fresh owner (`flows/38de5b/log.md:264`). **C**

**`orchestrate 'Observe.Locks'` (W), relevant entries:**
- **6820** CriomOSPinIntegration (00f95a): CriomOS-home `flake.nix`/`flake.lock`/`modules/home/default.nix`/`messenger-clj.nix`/check, "Pin-Flow-and-messenger-clj". Live and relevant: Home main will move again.
- **4928** PrometheusFreshMaterialization (eb7bae): `flows/eb7bae/materialization-20260924` (retired packet).
- **4373** PrometheusVmTesting6db4fe: `/var/lib/microvms/vm-testing` on Prometheus.
- **4062**, **4051/4070/4164** (753e69, retired owner): lojix and signal-lojix worktrees.
- **846, 900, 903, 907, 908** and related (542442, a stale cascade per 38de5b): CriomOS horizon-integration worktrees.
- No lock is held on the canonical `/git/github.com/LiGoldragon/CriomOS`, `lojix` or `goldragon` checkouts.

## Unknowns

- Whether tonight's plan activates live (`ActivateNow`, waiver) or boot-once. ARCHITECTURE says boot-once.
- Whether Realize can avoid staging the large gguf closure on ouranos (75 GB free).
- Flow version to declare (0.12.2) and whether aggregator 0.8.1 is part of "tonight's fixes".
- Herdr's upstream head; transitive ethos-zero and signal-* pins inside lojix `a67f5773` and orchestrate `9070cbb8`, not traced.
- Whether the `git+ssh` field-clj input resolves inside the Lojix Nexus evaluation environment.
- Content overlap between Home main and the `04446e78` lineage (for example two "Declare Flow Nexus launch environment" commits, `09c56b37` and `8be78063`).

## Sources

- Live: `ssh prometheus.goldragon.criome` (nixos-version, readlink, `ls -l` profiles, journal boot -1 at 21:03, `nix-store -q --deriver`); `lojix 'Query.ByNode.{ goldragon prometheus|ouranos None }'`; `orchestrate 'Observe.Locks'`; `/var/lib/lojix/generated-inputs/goldragon/*/complete-host/`; `/etc/nix/machines`; `df /nix`.
- Evaluations: `nix eval … drvPath` at CriomOS `da85c4a9`, `864e01be`, `f09f3c83` with Lojix's Prometheus inputs.
- Git: `git ls-remote` and `gh api` for all pinned repos; CriomOS and CriomOS-home checkouts under `/git/github.com/LiGoldragon/`.
- Records: `flows/b7da5d/receipts/flow-0107-declarative-preflight.md`, `flows/b7da5d/log.md`, `flows/00f95a/materialization-ouranos-flow-0.10.7/{report.md,lojix-evaluate.request}`, `flows/eb7bae/materialization-20260924/COMMANDS.md`, `flows/5f38bc/log.md`, `flows/38de5b/log.md`, `flows/38de5b/reports/wave-2026-09-25.md`, `flows/0384e0/reports/past-zeus-deploys.md`, `flows/da88cf/reports/headscale-repair.md`, CriomOS `ARCHITECTURE.md`.
- Transcript: `/home/li/.codex-next/sessions/2026/09/24/rollout-2026-09-24T15-53-42-01a0d568-fb12-7153-b6bd-86525a604099.jsonl` and `…13-54-26-01a0d4fb…jsonl` (gen 55 source claim and local build on Prometheus).
- Scratch evidence: `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/prometheus-pending/` (`lojix-*.txt`, `heads.tsv`, `eval.out`, `locks.txt`).
