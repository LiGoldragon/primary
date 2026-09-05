# Current architecture

This is a carried account from `/root/current_architecture`, transcript thread `01a07139-22a6-7912-a3b9-6520c58be819`: the main source report (ordinal 219), the pinned Horizon correction (ordinal 254), the package matrix (ordinal 294), and the Nixpkgs image-interface follow-up (ordinal 316). Statements below are relayed observations unless marked inference. No evaluation or build was run by that witness.

**Terminology correction, 2026-09-05:** narrative use of “Datomic” for the pure-data format and pipeline was an editorial error in the carried report. This report uses “datom” per the user's correction; literal source identifiers and quoted historical spellings remain unchanged.

## Current graph

The observed path is:

```text
cluster proposal.datom + cluster secrets/*.sops
        -> Lojix Horizon materialization
        -> narHash-bound horizon, system, deployment, and secrets inputs
        -> CriomOS target flake with override inputs
        -> nix eval <selector>.drvPath / nix build the derivation
        -> copy or activate only for a host or user deployment action
```

Lojix currently accepts cluster name, node name, proposal source, and materialization shape. It loads one proposal and calls `ClusterProposal::project` directly. There is no external default-node input or merge operation. CriomOS exposes one public OS output, `nixosConfigurations.target`. The materialized deployment input controls `includeHome`: `BaseHost` sets `includeHome = false` and `includeAllFirmware = false`; `CompleteHost` enables both. Home Manager is imported only when `includeHome` is true.

## Node and image boundaries

`NodeSpecies` has no live-installer variant. `MachineSpecies` and `Arch` are separate substrate facts, and `Arch::X86_64` projects to `x86_64-linux`. `behavesAs.iso` is a derived heuristic, `!virtual_machine && io.disks.is_empty()`, rather than an explicit installer kind. `NodeService` is an independent capability vector for services such as Tailnet, builder/cache, and VM host. Deployment composition (`CompleteHost`, `BaseHost`, and `UserEnvironment`) is separate from Horizon.

The current `CriomOS/modules/nixos/disks/liveiso.nix` sets ISO metadata and USB/EFI flags, but `CriomOS/modules/nixos/criomos.nix` imports `disks/preinstalled.nix` and never imports `liveiso.nix`. No inspected source exports `system.build.isoImage` or imports an installation-CD module; the public target remains `nixosConfigurations.target`. Lojix can evaluate a request-supplied selector and has a daemon-free `BuildOnly` mode, but it has no ISO artifact or ISO delivery/activation action. These are source observations only.

The root Nixpkgs input is `github:LiGoldragon/nixpkgs?ref=main`, locked to `0e251e24a4f24e036a084b6b4b2d2491af4167f4`. The lock does not declare a named NixOS release channel for this root input. The exact release represented by that fork revision, and support for `system.build.images`, remain unverified. The inspected source witnesses neither `system.build.images` nor `system.build.isoImage` as a selected CriomOS output.

## Pinned Horizon correction

The Horizon library compiled by the inspected Lojix revision is `horizon-rs@f8c5808466a47c2fd741cf0b119d73e8ba2add3d`. It uses the older datom proposal representation and lacks the newer `AgentIntercomLocal` and `AgentIntercomGraphical` `NodeService` variants. The separately checked-out Horizon source at `6f8e68074957b3803b92dd90ba236be2256fed6c` has moved those types to DOTOS and is not an ancestor continuation of the pinned revision. An external default-node input must therefore be decoded and merged in the pinned datom-compatible representation; treating the local DOTOS tree as the executable Lojix schema would be wrong.

In the pinned library, `ClusterProposal::project` rejects a viewpoint node absent from `nodes`. It derives the node fields, `exNodes`, build and cache inventories, `adminSshPubKeys`, users, groups, and key rollups from the proposal. `behavesAs.iso` is still only the empty-disk heuristic. These observations support the following design conclusion.

## Synthetic default-node seam

**Inference from the projection algorithm:** merge a deterministic external synthetic node into `ClusterProposal.nodes` before projection if the installer is to be a selectable viewpoint and to appear consistently in rendered Horizon. This lets existing validation and derivation run once: Pod host-set and architecture checks, Tailnet-controller singleton checks, trust filtering, addresses, domains, user/key filling, `exNodes`, build/cache facts, and cluster rollups. Patching the projected Horizon afterward would duplicate derivation and leave cluster views inconsistent.

The seam does not settle default-source identity or pinning, duplicate-name behavior, whether defaults may contribute services, keys, or addresses, or whether every Lojix materialization and test path receives the same merged proposal. The merge would be before `ProjectableProposal::project`; current `HorizonMaterializationCommand`, deployment wire records, and bootstrap Horizon input carry no such source. Keeping it external to Lojix's hardcoded defaults is an inference required by the requested boundary.

## Configuration repository boundary

The current-architecture follow-up witnessed `criomos-horizon-config@e222d3a7128484d8163a1a5bf90fbf1a4a15b6ef` as a pan-Horizon repository, not a cluster-data repository. Its only authored record is `horizon.dotos`, a global `HorizonProposal` for identity, DNS suffixes, and temporary LAN data. It contains no cluster nodes, users, keys, providers, generated defaults, or encrypted secrets. The repository's own boundary assigns per-cluster `datom.dotos`, nodes, users, trust, public keys, provider choices, and secrets to separate cluster repositories. This distinction is a witnessed ownership declaration; the follow-up did not inspect a particular cluster repository or encrypted file.

Therefore, the pan-Horizon repository is not an existing home for the synthetic installer node. **Inference:** the default remains an external input to be merged with the per-cluster proposal before Horizon projection, subject to identifying the actual cluster-data repository and its pinned revision.

The data-layout follow-up identified the active cluster repository as `/git/github.com/LiGoldragon/goldragon@2a139455ba6d2f71c3ba60bf56452c0be446f0d3`. Its `proposal.datom` is the sole positional `Text<ClusterProposal>` datom source for nodes, users, trust, and access; sibling encrypted `secrets/` ciphertext exists but was not inspected. The repository has no `flake.nix`, Nix adapter, or `datom.dotos`. Lojix `d3c0ac...` requires the canonical proposal as a regular absolute `proposal.datom`, rejects non-datom input, projects it, and derives secrets from its sibling directory. It has no `horizon.dotos` or `datom.dotos` join. This is a witnessed current pipeline fact. The newer pan-Horizon DOTOS documentation is therefore not wired into the active datom Lojix path.

**Inference:** a defaults-aware installer change must preserve this active datom boundary or deliberately redesign the join; it cannot assume that the pan-Horizon DOTOS repository is already part of Lojix materialization.

## Global constants and shared node definitions

The current-architecture witness rechecked `criomos-horizon-config@e222d3a7128484d8163a1a5bf90fbf1a4a15b6ef`. Its one authored record calls itself `HorizonProposal` and carries operator `LiGoldragon`, suffixes `criome` and `criome.net`, and a `TransitionalIpv4Lan` with network `10.18.0.0/24`, gateway `10.18.0.1`, DHCP range `10.18.0.100–10.18.0.240`, and a single-router transitional annotation. The terminal `[]` has no implemented schema naming its field. Documentation suggests reserved subdomains, but that field meaning remains unverified.

Neither local `horizon-rs@6f8e68074957b3803b92dd90ba236be2256fed6c` nor the Lojix-pinned Horizon `@f8c5808466a47c2fd741cf0b119d73e8ba2add3d` has a consumer for this global `HorizonProposal` file. The current Horizon CLI accepts only cluster, node, and proposal stdin; pinned Lojix still consumes canonical `proposal.datom`. A workspace replacement-stack record describes this global configuration as net-new and not yet consumed, while constants remain in cluster data. README wording about reading both inputs is forward-looking and is not an integration witness.

**Inference:** new shared general node definitions are a distinct category alongside global constants and cluster data. No existing schema, selection rule, or merge rule for that category was found.

## Node classification follow-up

The current-architecture witness rechecked the node classification in transcript thread `01a07139-22a6-7912-a3b9-6520c58be819`. `NodeSpecies` is an exclusive enum, but several variants bundle standard role facets: `Center` -> `center`; `LargeAi` -> `center + largeAi`; `LargeAiRouter` -> `center + largeAi + router`; `Hybrid` -> `edge + router + nextGen`; `Edge` -> `edge + lowPower`; `EdgeTesting` -> `edge + nextGen + lowPower`; `Router` -> `router`; `TestVm` -> `testVm`; and `CloudNode` -> `cloudNode`. `MediaBroadcast` and `RouterTesting` have no standard role facet.

`MachineSpecies` is independent: `Metal` derives bare-metal and non-virtual behavior, while `Pod` derives virtual behavior. Node services overlap independently. GUI and `hasVideoOutput` derive from `edge`; `iso` remains `!virtualMachine && disks.empty`. There is no `LiveIso` or `Installed` enum, and the `iso` facet does not provide complete image behavior; `disks/liveiso.nix` remains unimported. Comments for `TestVm` and `CloudNode` mix purpose, substrate, and destination, while derivation itself does not enforce intended species/machine pairings. CriomOS gates predominantly use projected booleans, and no runtime consumer for `cloudNode` was witnessed. These are classification facts only, not an approved replacement taxonomy.

If merged pre-projection, the node reaches network host entries, Yggdrasil and link-local address projections, SSH known hosts, builder/cache configuration, trusted build keys, image-exchange keys, and projected users. Lojix copies encrypted ciphertext from the proposal's sibling `secrets/` directory; adding a node does not create a secret, although enabling an existing secret consumer can expose missing-secret failures. A synthetic node is usable only in paths that use the same defaults-aware materialization.

## Credentials and package reach

`includeHome = false` omits Home Manager only. It does not omit `users.nix`, `normalize.nix`, or OpenSSH. Current NixOS creates projected users and SSH keys, assigns root the projected `adminSshPubKeys`, and disables password authentication. The user projection does not derive `wheel`, and no examined system module grants projected users sudo. No examined system module supplies an initial or hashed password for ordinary users. The dormant ISO module sets plaintext `root.initialPassword = "r"`, which conflicts with the requested protected non-root TTY login. The SOPS base module configures age decryption through `/etc/ssh/ssh_host_ed25519_key`; Lojix copies ciphertext but does not inspect it. A non-root TTY account, sudo policy, encrypted password, and boot-time decryption identity require explicit composition.

The package witness found these current paths:

- `CriomOS/modules/nixos/normalize.nix` supplies base `openssh`, `ntfs3g`, and `fuse`; its ISO branch adds `btrfs-progs`, `dosfstools`, `parted`, `nmap`, `vim`, and `htop`.
- `CriomOS/modules/nixos/complex.nix` currently defaults `includeComplex` on when the deployment record omits it, so a BaseHost projection can still receive Clavifaber.
- The network aggregate brings in Yggdrasil, while metal defaults include firmware policy, graphics, `fwupd`, and hardware packages. Edge desktop facilities are gated by `behavesAs.edge`.
- Home sources are in the separate `CriomOS-home/home/...` checkout. `home/default.nix` imports min, medium, and max profiles; profile `mkIf` gates are cumulative by user size. The min profile already includes a large developer and AI toolset; medium and max add browsers, desktop applications, multimedia, and browser-use tooling.

`BaseHost` is the clearest current boundary for a no-Home image, but it still inherits the normal system aggregate and the ISO heuristic's tools and metal stack. An ISO assembly can reuse package derivations when inputs and outputs match; changing Horizon/default-node materialization changes dependent input hashes. No closure-size or build-time claim follows from source alone.

## Sources

- **Witnessed source, CriomOS `14a246f5b64c31d1208d9edd76f05acd9b4828b1`:** `flake.nix:109-164,239-304`; `modules/nixos/criomos.nix:16-79`; `modules/nixos/disks/liveiso.nix:16-39`; `modules/nixos/disks/preinstalled.nix:1-64`; `modules/nixos/normalize.nix:80-215`; `modules/nixos/users.nix:17-62`; `modules/nixos/secrets.nix:1-10`; `modules/nixos/network/default.nix:26-91`; `modules/nixos/nix/builder.nix:52-81`; `modules/nixos/complex.nix:14-36`; `modules/nixos/edge/default.nix:9-167`; `modules/nixos/metal/default.nix:323-545`; `modules/nixos/userHomes.nix:19-50`.
- **Witnessed source, CriomOS-home `a83210d3e0afd44fcdb9fa893fa582a22913146f`:** `home/default.nix:27-95`; `home/base.nix:139-176`; `home/profiles/min/default.nix:220-345,443-502,684-695,750-804`; `home/profiles/med/default.nix:88-165`; `home/profiles/max/default.nix:43-107`; `home/profiles/max/browser-use.nix:306`.
- **Witnessed pinned source, Horizon `f8c5808466a47c2fd741cf0b119d73e8ba2add3d`:** `lib/src/proposal.rs:1-120`; `lib/src/horizon.rs:31-159,163-203`; `lib/src/node.rs:157-223,355-500,510-589`; `lib/src/user.rs:78-157`; `lib/src/species.rs:10-57`.
- **Witnessed source, Lojix `d3c0ac9032250e0b12ade7d8c71a8fc8311ab5bf`:** `Cargo.toml:47-64`; `Cargo.lock:685-688`; `src/runtime_flow.rs:79-145,4978-5006`; `src/bootstrap.rs:60-125,663-677,1850-1958`; `src/runtime_model.rs:478-507`; `src/adapters.rs:224-225`; `src/schema_runtime.rs:4389-4435,4617-4661,4746-4843,4862-4957,4978-5035,6202-6294`; `tests/horizon_materialization_contract.rs:1-20`.
- **Witnessed pin follow-up, CriomOS:** `flake.nix:5,239-289`; `flake.lock:2233-2247,2281-2295,2913-2919`; root Nixpkgs lock node `nixpkgs_3`.
- **Witnessed configuration follow-up, `criomos-horizon-config@e222d3a7128484d8163a1a5bf90fbf1a4a15b6ef`:** `horizon.dotos:1`; repository `AGENTS`, `ARCHITECTURE`, and `README` boundary statements separating pan-Horizon data from per-cluster repositories.
- **Witnessed data-layout follow-up, `goldragon@2a139455ba6d2f71c3ba60bf56452c0be446f0d3`:** `index protocols/active-repositories.md:122`; repository `AGENTS`, `README`, and `ARCHITECTURE`; `proposal.datom` and sibling `secrets/` layout. **Witnessed Lojix boundary:** `src/schema_runtime.rs:35,4640,4671` in `d3c0ac...`.
- **Witnessed global-configuration follow-up, `criomos-horizon-config@e222d3a7128484d8163a1a5bf90fbf1a4a15b6ef`:** `horizon.dotos:1`; repository `AGENTS`, `ARCHITECTURE`, and `README`; local/pinned Horizon and Lojix input boundaries; workspace replacement-stack record describing the configuration as net-new and not yet consumed.
- **Witnessed node-classification follow-up, local Horizon `6f8e68074957b3803b92dd90ba236be2256fed6c`:** `lib/src/species.rs:10`; `lib/src/node.rs:151`; `lib/src/machine.rs:10`; CriomOS `modules/nixos/normalize.nix:98`, `modules/nixos/edge/default.nix:93`, `modules/nixos/test-vm-guest.nix:45`, and `modules/nixos/disks/liveiso.nix:16`.
