# Prometheus definition — capabilities, model-installing modules, "next generations", proposed edit, deploy builder

Read from `origin/main` after `git fetch` in each repo (fetch timestamps this session; SHAs below), not from possibly-stale local checkouts. goldragon's on-disk `proposal.datom` at `/git/github.com/LiGoldragon/goldragon/proposal.datom` is a **stale artifact of a detached checkout** (HEAD at `2d91a80`) predating commit `8d8224f "retire legacy Horizon proposal"`; the live canonical source on `origin/main` (`199f5eb`) is `cluster-definition.datom`.

## 1. Prometheus's node entry and NodeCapability enum

**Witnessed** — `goldragon` `origin/main` (199f5eb), `cluster-definition.datom:1` (single-line file). Prometheus's `NodeDefinition` in full:

```
{ prometheus Installation.{ Uefi [ { /dev/disk/by-uuid/d3ad7f53-2470-4744-9ddf-b183c7c22f31 / Btrfs [ subvol=root ] } { /dev/disk/by-uuid/A252-A02B /boot Vfat [] } { /dev/disk/by-uuid/d3ad7f53-2470-4744-9ddf-b183c7c22f31 /home Btrfs [ subvol=home ] } { /dev/disk/by-uuid/d3ad7f53-2470-4744-9ddf-b183c7c22f31 /nix Btrfs [ subvol=nix ] } { /dev/disk/by-uuid/d3ad7f53-2470-4744-9ddf-b183c7c22f31 /var Btrfs [ subvol=var ] } ] [] } Max Max Metal.{ X86_64 { 8 Some.«GMKtec EVO-X2» None None Some.128 None } } { Qwerty None } { [] Some.«5::5/128» None [] Some.{ eno1 wlp195s0 TwoG 6 Wifi4 Some.{ routerWifiSaePasswords } Some.{ wlp199s0f0u4 criome-backup TwoG 11 Wifi4 { routerBackupWifiPassword } } } } { AAAAC3NzaC1lZDI1NTE5AAAAIAWX4CiSoep1+JuiYEpMzBj/H24eCYR+ZWaG3z2pg4Pk Some.vCjiTyT4+sVkjvASSKteq7RZ1/b8hploA7kliKnrpKk= Some.{ 9adf4a76f8229421981cdaaaf4d0177a57119eee5848499eaa9e0fdf107363cf 200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f 300:ca41:6b12:fba } } Some.True [ Center.{} LargeAi.{} Router.{} TailnetClient.{} NixBuilder.Some.6 NixCache.{} VmHost.{ 169.254.100.0/22 Available Some.4 } ] None }
```

Projected `Capabilities` vector: `Center.{}`, `LargeAi.{}`, `Router.{}`, `TailnetClient.{}`, `NixBuilder.Some.6` (max 6 remote build jobs), `NixCache.{}`, `VmHost.{ guestSubnet=169.254.100.0/22 kvm=Available maxGuests=Some.4 }`. **`NextGeneration` is NOT among Prometheus's capabilities** — it is set on `ouranos` and `tiger` only, in the same file (visible in the surrounding node entries).

**Witnessed** — `horizon-rs` `origin/main` (8c11dfaa1), `lib/ethos/horizon.ethos:71`, full `NodeCapability` enum:

```
NodeCapability.[ Graphical.NoSettings Center.NoSettings LargeAi.NoSettings Router.NoSettings Edge.NoSettings NextGeneration.NoSettings LowPower.NoSettings TestVm.NoSettings VmTesting.{ Boolean String Option<String> } CloudNode.NoSettings Printing.NoSettings HardwareVideo.NoSettings Nordvpn.NoSettings WifiCertificate.NoSettings TailnetClient.NoSettings TailnetController.NoSettings NixBuilder.Option<Integer> NixCache.NoSettings PersonaDevelopment.Vector<PersonaCapability> VmHost.{ TapSubnet KvmAvailability Option<Integer> } WebHost.Vector<HostedSite> ]
```

The ethos file carries **no inline comments per variant**. Meanings below are **inferred** from `horizon-rs` `lib/src/projection/viewpoint.rs` (`NodeDeriving::derive`/`builder_config`, lines ~22-100) and from which CriomOS/CriomOS-home modules key off each flag:

- `LargeAi` → sets `behaves_as.large_ai`. Consumed solely by CriomOS `modules/nixos/llm.nix` (see §2) — installs/runs a local LLM router.
- `NextGeneration` → sets `behaves_as.next_generation` (`viewpoint.rs:28,53`). **No consumer found anywhere in CriomOS or CriomOS-home** (grepped both trees for `nextGeneration`/`next_generation`/`nextgen`, no hits). Dead/reserved flag today, not the model-fetching mechanism — see §3.
- `LowPower` → `behaves_as.low_power`; used by network/metal/router-classification checks (`checks/metal-model-classification`, `checks/resolver-role-policy`), unrelated to models.
- `Center` → `behaves_as.center`; excludes NetworkManager and dispatcher role (`viewpoint.rs:78-79`), gates `modules/nixos/network` role selection.
- `Router` → feeds `RouterInterfacesView`; gates `modules/nixos/router/*` (yggdrasil, wifi-pki, dnsmasq).
- `NixBuilder(maxJobs)` → `is_remote_nix_builder` when trusted+online+has base keys (`viewpoint.rs:70-75`); feeds `modules/nixos/nix/builder.nix` and the cluster's `builderConfigs` list (peers' `/etc/nix/machines`).
- `NixCache` → `is_nix_cache`, `nix_cache_domain=nix.<domain>` (`viewpoint.rs:78-88`); feeds `modules/nixos/nix/cache.nix` (the `http://nix.prometheus.goldragon.criome` cache seen in the deploy logs).
- `VmHost{tapSubnet,kvm,maxGuests}` → enables libvirt/qemu VM hosting (`modules/nixos/nspawn.nix` and related metal modules key off it).

## 2. Model/AI-installing modules gated on `largeAi` / `nextGeneration`

**Witnessed** — grepped both `CriomOS` and `CriomOS-home` (`origin/main`, `36653a12` / `4adefe87`) for `largeAi`/`large_ai`, `nextGeneration`/`next_generation`, and the named ML tools.

### The only capability-gated model-installer: `CriomOS/modules/nixos/llm.nix`

Gate at line 140: `mkIf behavesAs.largeAi { ... }`. Imported unconditionally from `modules/nixos/criomos.nix:35`; **no separate enable option exists** — `behavesAs.largeAi` (i.e., whether `LargeAi` is in the node's `Capabilities` vector) is the *only* switch. There is no `criomos.llm.enable`-style option to disable the service while keeping the capability.

What it does when active:
- Builds `llamaCppPackage` from `../../packages/llama-cpp-strix-halo.nix` (a ROCm/Strix-Halo llama.cpp build; `HSA_OVERRIDE_GFX_VERSION=11.5.1` env var confirms AMD ROCm targeting).
- Reads a model manifest from `inputs.criomos-lib + "/data/largeAI/llm.json"` (`configPath`/`cfg`, lines 22-24).
- For each model in `cfg.models`, fetches weights via `pkgs.fetchurl` (`mkModelStorePath`, lines 35-63) — either a single GGUF file or multi-shard set — **into the Nix store at evaluation/build time**, not via a runtime download. Also fetches a vision-projector (`mmproj`) file per multimodal model (lines 68-74).
- Symlinks all fetched models into one derivation, `modelsDir = pkgs.runCommand "llm-models-dir" ...` (lines 80-86).
- Runs `systemd.services."${nodeName}-llama-router"` (e.g. `prometheus-llama-router`) as user `llama`, `StateDirectory = "llama"` → `/var/lib/llama`; `ExecStart` launches `llama-server --models-dir <store-path> --models-preset <presets.ini> ...`. `MemoryMax=110G`/`MemoryHigh=100G` on the service.
- Since fetching happens through `pkgs.fetchurl` derivations evaluated/realized at *build* time (not a systemd timer), **the systemd service itself does not pull models at activation** — but building the closure for a `LargeAi` node does pull/realize every listed model as a build input. This is exactly what the deploy evidence in §5 shows: 401 GiB of missing GGUF weights that a `nix build`/copy tried to materialize (`/home/li/secondary/flows/348e7b/reports/prometheus-model-transfer-gate.txt`, whole file — 17 GGUF paths, `gemma-4-31B`, `Qwen3.5/3.6`, `Nemotron-3`, `gpt-oss-120b`, etc., "Known remote model bytes missing locally: 430708500832" ≈ 401.1 GiB).

### `nextGeneration`-gated modules

**Witnessed (negative result)**: none. `grep -rn "nextGeneration\|next_generation"` across both repos returns nothing. Whatever "next generations" the living means, it is **not** this `NodeCapability`.

### Other AI/ML packages found — not capability-gated, not Prometheus-specific

- `CriomOS-home/modules/home/profiles/med/default.nix:121-122` — `python3Packages.openai-whisper`, a `faster-whisper` wrapper script. Gated by **user home-profile size** (`med`), unrelated to node capabilities.
- `CriomOS-home/modules/home/profiles/min/default.nix:320` — `pkgs.llama-cpp` CLI package in a general `AIPackages` list (alongside `gemini-cli`, `codex`, etc.). Also profile-gated, not `largeAi`-gated, and does not download weights itself.
- `CriomOS-home/modules/home/profiles/min/pi-models.nix` (marked `DEPRECATED — do not add new models`) and `modules/home/profiles/max/browser-use.nix` — these do **not** install models; they look up a `largeAiNode`/`routerNode` in the cluster (`node.behavesAs.largeAi or false`) purely to point the `pi` CLI's OpenAI-compatible provider `baseUrl` at that node's llama-router over HTTP. `legacyLocalProviderNames = [ "prometheus" "criomos-largeai" ]` in `pi-models.nix:41-42` names Prometheus explicitly as a legacy provider id — client-side config only, no disk writes of model weight.

No `ollama`, `open-webui`, `comfyui`, `stable-diffusion`, `pytorch`/`cuda`-toolkit, `tabby`, `vllm`, `tgi`, `local-ai`, or Hugging-Face cache references were found in either repo.

## 3. What "next generations" most plausibly names

**Inferred** — three candidates, ranked by fit to the living's wording ("all these next generations… detached and unlinked… disable the models so the old ones can be…"):

**(a) The `NextGeneration` NodeCapability** — ruled unlikely as the literal referent: it is not present on Prometheus's capability list at all (§1), and it drives no module (§2). If this is what's meant, the fix is a no-op for Prometheus.

**(b) Ordinary NixOS system generations/profiles** (`/nix/var/nix/profiles/system-*-link`, `nixos-rebuild switch --rollback`, etc.) — plausible in the colloquial sense ("the next generation of the system") but CriomOS/goldragon do not activate through the stock NixOS generation mechanism on Prometheus; deployment is via `lojix`/`meta-signal-lojix`, which layers its own retention scheme (c) on top of/instead of bare `nix-env` generations.

**(c) Lojix `GenerationSlot` records + GC roots under `/nix/var/nix/gcroots/criomos/goldragon/prometheus/`** — **best fit**, and matches the living's exact verbs ("disabled … detached and unlinked"):

- **Witnessed** — `lojix` `origin/main` (c4bba4fa1), `src/runtime_model.rs:130-135`:
  ```
  pub enum GenerationSlot {
      Current,
      BootPending,
      Rollback,
      Pinned,
      Recent,
  }
  ```
- **Witnessed** — `lojix/ARCHITECTURE.md:89-98`: the GC-roots tree is `/nix/var/nix/gcroots/criomos/<cluster>/<node>/<kind>/<generation>` → `<store-path>` symlinks, with per-kind slots `current`, `boot-pending`, `rollback/<n>` (last 4), `pinned/<label>`, `recent/<timestamp>`. For Prometheus this is literally `/nix/var/nix/gcroots/criomos/goldragon/prometheus/…`.
- **Witnessed** — `meta-signal-lojix/ethos/signal.ethos:29-54`: the owner-only mutation verbs are `Deploy`/`Pin`/`Unpin`/`Retire`; `RetireRejectionReason.[ NodeUnknown GenerationUnknown GenerationPinned InternalError GenerationActive ]`.
- **Witnessed** — `lojix/src/schema_runtime.rs:4153-4180` (`retire_generation`): retire **retracts the GC root** (`self.store.retract_gc_root(...)`, which unlinks the corresponding `/nix/var/nix/gcroots/.../<generation>` symlink) unless `root.generation_slot == Pinned`, in which case it is rejected with `GenerationPinned`. `unpin_generation` (`schema_runtime.rs:4124-4152`) moves a `Pinned` slot to `Recent`, clearing `optional_pin_label`, which is the required step before a pinned old (non-`LargeAi`) generation could be retired/unlinked.

So: "detach and unlink the old ones" = call `Unpin` (if the safe old generation is `Pinned`) then `Retire` on its `GenerationIdentifier`/`GenerationSlot` row, which retracts its GC root and lets Nix garbage-collect it. This is the concrete mechanism for the living's fallback path ("if the new system cannot build, the models disabled so the old ones can be detached and unlinked").

## 4. Proposed edit to drop model-bearing capabilities from Prometheus

**Witnessed** (before) / **proposed** (after) — only `LargeAi.{}` needs to be dropped from Prometheus's `Capabilities` vector in `goldragon/cluster-definition.datom:1`; `NextGeneration` is not present on Prometheus to begin with (§1, §3a).

Before:
```
... Some.True [ Center.{} LargeAi.{} Router.{} TailnetClient.{} NixBuilder.Some.6 NixCache.{} VmHost.{ 169.254.100.0/22 Available Some.4 } ] None }
```

After:
```
... Some.True [ Center.{} Router.{} TailnetClient.{} NixBuilder.Some.6 NixCache.{} VmHost.{ 169.254.100.0/22 Available Some.4 } ] None }
```

(Only the `LargeAi.{}` token is removed; everything else on the line, including the rest of the `NodeDefinition`, is unchanged.)

**Does `criomos-horizon-config` or a CriomOS module option also need a change?** No. `criomos-horizon-config` (`origin/main`, 74a4ad35) contains only `horizon-configuration.datom` (domain/global config) — grepped for `largeai`/`nextgen`, no hits; it does not carry per-node capability lists. In CriomOS, `llm.nix`'s only gate is `behavesAs.largeAi`, which is derived automatically from the datom's `Capabilities` vector (`horizon-rs` `viewpoint.rs:30`); dropping `LargeAi.{}` from the datom alone flips `behaves_as.large_ai` to `false` cluster-wide for Prometheus, and `mkIf behavesAs.largeAi { ... }` then evaluates to nothing — the `llamaCppPackage` build, all `pkgs.fetchurl` model derivations, and the `*-llama-router` systemd service simply drop out of the closure. No separate CriomOS option edit is required.

**What would the resulting configuration stop providing?** Only the local LLM router (`prometheus-llama-router` service, port `serverPort` from `llm.json`, the `llama` system user/group, `/var/lib/llama` StateDirectory, and the `localLlmApiToken` sops secret binding in `llm.nix`). Nothing else Prometheus provides depends on `LargeAi`: **witnessed** — `viewpoint.rs` computes `large_ai` independently of `is_remote_nix_builder`, `is_nix_cache`, `is_dispatcher`, and the `VmHost` role; `Center`, `Router`, `NixBuilder.Some.6`, `NixCache`, and `VmHost.{...}` all stay untouched in the proposed edit, so Prometheus keeps acting as: cluster Nix build dispatcher/remote builder (max 6 jobs), binary cache (`nix.prometheus.goldragon.criome`), router-interface/network role, Tailnet client, and KVM VM host (up to 4 guests, subnet `169.254.100.0/22`).

**Is there a module-level "disable without removing the capability" switch?** No — checked (§2): `llm.nix` has no `mkEnableOption`/`mkOption` of its own; `mkIf behavesAs.largeAi` is the sole gate, and `behaves_as.large_ai` is derived purely from whether `LargeAi` is present in the datom's `Capabilities` vector. The only way to disable the LLM/model service short of a code change is to remove `LargeAi.{}` from the capability list in the datom — the same edit as above. There is no separate "keep capability, disable service" flag; the "disable if it cannot build" path the living asked for and the capability-removal path are the same edit.

## 5. Current deploy record and its builder field

**Witnessed** — `/home/li/secondary/flows/348e7b/reports/lojix-prometheus-realize-12.datom` (whole file), the most recent Prometheus deploy-status query in that directory (`Host.Realize`, sequence 12):

```
Queried.{ [] [ { 12 12 { HostEnvironment goldragon prometheus CompleteHost Host.Realize LiveActivation RequireImmutable Some.38c5bd51ea6d47aa25522941d9244873f6803b72 } Some.{ 246 246 } Failed Some.{ 306 306 } Some.Failed.{ Build BuildFailed Some.{ Some.{ nix [ build --no-link --print-out-paths --option max-jobs 0 --builders @/etc/nix/machines /nix/store/saw7gx1vc7bgzi305kr3686rhgmn77qd-nixos-system-prometheus-26.11.20260813.0e251e2.drv^* ] Some.1 } «...ssh-ng://nix-ssh@prometheus.goldragon.criome...error: interrupted by the user» True } } } ] { 310 310 } }
```
(Result: `Failed` → `BuildFailed`, the run was interrupted by the user; it built and copied through Prometheus over `ssh-ng://nix-ssh@prometheus.goldragon.criome` before being interrupted.)

**Builder field**: this file records only the query-side status (`Host.Realize` phase + the literal `nix build ... --builders @/etc/nix/machines ...` argv), not the raw `HostDeployment{..., optional_nix_builder_spec, ...}` submission record verbatim — no `.datom` file in that directory contains the submission with the `NixBuilderSpec` field spelled out as such. The builder value is characterized in prose in `/home/li/secondary/flows/348e7b/reports/lojix-target-store-clarification.md` (also duplicated into `to-efa157.md:175-181`), **inferred/reported, not a raw record quote**: "Realization12 already passed `Some.@/etc/nix/machines`. That file has one builder, `ssh-ng://nix-ssh@prometheus.goldragon.criome`... records both builds ON Prometheus and result copies FROM Prometheus." This matches `meta-signal-lojix/ethos/signal.ethos:30`'s `HostDeployment{ ... Option<NixBuilderSpec> ... }` field — the secondary's Deploy.Host submission set `NixBuilderSpec = Some("@/etc/nix/machines")`, i.e. "build on Prometheus itself" via the machines file rather than a bare builder URI, per the report's argument that a bare URI still runs the Nix client locally and only copies the closure to/from the named store (`schema_runtime.rs:5225`, quoted in that report).

## Sources

- `/git/github.com/LiGoldragon/goldragon` origin/main `199f5eb`: `cluster-definition.datom:1`; local on-disk `proposal.datom` (stale, HEAD `2d91a80`, retired at `8d8224f`) — not used as evidence.
- `/git/github.com/LiGoldragon/horizon-rs` origin/main `8c11dfaa1`: `lib/ethos/horizon.ethos:71`; `lib/src/model.rs:118-159,205-236`; `lib/src/projection/viewpoint.rs:22-100`.
- `/git/github.com/LiGoldragon/CriomOS` origin/main `36653a12`: `modules/nixos/llm.nix` (full file); `modules/nixos/criomos.nix:35`; `modules/nixos/test-vm-guest.nix:14`; `checks/{resolver-role-policy,headscale-selfsigned-cert,lojix-ownership}/default.nix`.
- `/git/github.com/LiGoldragon/CriomOS-home` origin/main `4adefe87`: `modules/home/profiles/min/pi-models.nix`; `modules/home/profiles/max/browser-use.nix`; `modules/home/profiles/med/default.nix:42-43,121-122`; `modules/home/profiles/min/default.nix:290-330`; `checks/spirit-deployment/default.nix:232-233`; `checks/bird-home-isolation/default.nix:15-16`.
- `/git/github.com/LiGoldragon/criomos-horizon-config` origin/main `74a4ad35`: repo file listing; `horizon-configuration.datom` (grepped, no relevant hits).
- `/git/github.com/LiGoldragon/lojix` origin/main `c4bba4fa1`: `ARCHITECTURE.md:76-98`; `src/runtime_model.rs:130-135`; `src/schema_runtime.rs:4124-4180,3334-3346`; `src/adapters.rs:350-355`.
- `/git/github.com/LiGoldragon/meta-signal-lojix` (local checkout, not fetched — read as found): `ethos/signal.ethos:4,10-54`.
- `/home/li/secondary/flows/348e7b/reports/`: `lojix-prometheus-realize-12.datom` (whole file, quoted); `lojix-prometheus-evaluate-{5,6,8,11}.datom` (whole files, reviewed); `prometheus-model-transfer-gate.txt` (whole file, quoted); `prometheus-before-activation.txt` (whole file, reviewed); `lojix-target-store-clarification.md` (whole file, quoted); `to-efa157.md:149-153,175-181` (this file changed on disk mid-session; read as currently written).
