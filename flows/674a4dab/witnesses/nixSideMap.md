# Nix Side Map of the CriomOS Stack

Method: code read /git/github.com/LiGoldragon/CriomOS/flake.nix, /git/github.com/LiGoldragon/CriomOS-home/flake.nix, /git/github.com/LiGoldragon/CriomOS-pkgs/flake.nix, /git/github.com/LiGoldragon/CriomOS-lib/flake.nix, /git/github.com/LiGoldragon/criomos-horizon-config/horizon.dotos, /git/github.com/LiGoldragon/horizon-rs/flake.nix, /git/github.com/LiGoldragon/dotos/flake.nix, /git/github.com/LiGoldragon/datom/flake.nix, /git/github.com/LiGoldragon/curriculum-deploy/flake.nix, /git/github.com/LiGoldragon/spirit/flake.nix, /git/github.com/LiGoldragon/lojix/flake.nix, /git/github.com/LiGoldragon/orchestrate/flake.nix, /git/github.com/LiGoldragon/rust-build/flake.nix, /git/github.com/LiGoldragon/agent/flake.nix, /home/li/primary/flake.nix, all modules and checks in CriomOS and CriomOS-home
Method: probe nix flake metadata --json /git/github.com/LiGoldragon/CriomOS
Method: probe find ... -name '*.nix' | wc -l (each repo)
Method: probe grep -rn (horizon, hostName, secrets, tier, Edge, claude, codex, emacs, codium, overlays, etc.) across CriomOS and CriomOS-home

## 1. Flake Input Graph

```
                             LiGoldragon/nixpkgs (fork, ref=main)
                                        |
          .---------+----------+--------+--------+--------+--------+----- ... (all follows)
          |         |          |        |        |        |        |
     CriomOS   CriomOS-home  CriomOS-pkgs  sops-nix  home-mgr  rust-overlay  blueprint ...
          |         |          |
          |    (follows:       +--> nix-vscode-extensions (follows nixpkgs)
          |     nixpkgs,
          |     home-mgr,     system stub ............... (follows from CriomOS)
          |     criomos-lib,  
          |     rust-overlay,
          |     horizon,
          |     system,
          |     pkgs,
          |     orchestrate,
          |     spirit)
          |         |
          |         +--> own inputs: niri-flake, noctalia(pin), stylix, crane,
          |         |    llm-agents(own nixpkgs!), herdr, orca-ide, chroma(pin),
          |         |    chroma-emacs(pin), claude-answers, substack-cli,
          |         |    hexis, google-workspace-cli, listener, agent(pin),
          |         |    aggregator(pin), message(pin), orchestrate(pin*),
          |         |    spirit(pin), pi-session-namer, mentci-src(non-flake),
          |         |    primary-generated-src(non-flake),
          |         |    pyproject-nix, uv2nix, pyproject-build-systems,
          |         |    annas-mcp(non-flake), yt-dlp(non-flake),
          |         |    visualjj-vsix(file), claude-code-vsix(file),
          |         |    codex-chatgpt-vsix(file),
          |         |    ~35 agent-intercom npm tarballs (non-flake)
          |         |
          |         +-- (* orchestrate pin here: 5b495422... via follows from CriomOS;
          |                CriomOS-home's own flake.nix declares e0f3bc5e... but CriomOS
          |                overrides it to 5b495422 via follows)
          |
          +--> brightness-ctl, clavifaber (+rust-build follows), criome,
          |    lojix(pin), microvm.nix, mirror, repository-ledger, router,
          |    spirit(pin), rust-build, orchestrate(pin), criomos-lib
          |
          +--> STUBS (path:./stubs/...):
          |       system   -> no-system  (throws; lojix overrides)
          |       horizon  -> no-horizon (throws; lojix overrides)
          |       deployment -> default-deployment (includeHome=true, includeAllFirmware=true)
          |       secrets  -> no-secrets (empty sopsFiles; lojix overrides from cluster repo)
          |
          +--> pkgs = CriomOS-pkgs (follows nixpkgs + system)

primary (workspace)
   +--> curriculum-deploy (own nixpkgs pin, flake-utils, rust-build, Curriculum)
   +--> dotos-*, tree-sitter-dotos, Curriculum (all non-flake)

curriculum-deploy --> own nixpkgs pin (NixOS/nixpkgs commit), rust-build
horizon-rs --> NixOS/nixpkgs?ref=nixos-unstable, fenix, crane
dotos --> nixpkgs-unstable, flake-utils, rust-build
datom --> nixpkgs-unstable, flake-utils, rust-build
lojix --> nixpkgs-unstable, flake-utils, fenix, crane
spirit --> nixpkgs-unstable, flake-utils, rust-build
          +--> spirit-judge(pin), spirit-judge-config(pin), judge-provider(pin=codex-cli-nix)
          +--> ~15 non-flake source inputs (kameo, nota, schema, sema, signal-*, triad-runtime, criome...)
orchestrate --> nixpkgs-unstable, flake-utils, rust-build
rust-build --> nixpkgs-unstable, flake-utils, fenix, crane
agent --> nixpkgs-unstable, flake-utils, fenix, crane

goldragon         -- no flake.nix (DOTOS data: datom.dotos, synchronizer.dotos, secrets/)
criomos-horizon-config -- no flake.nix (DOTOS data: horizon.dotos, 12 lines)
```

### Nixpkgs Paths (where the same upstream enters through different paths)

| Upstream | Paths | Mechanism |
|---|---|---|
| nixpkgs | CriomOS (LiGoldragon/nixpkgs main) unified via follows to home, pkgs, all NixOS inputs | All follow CriomOS root |
| nixpkgs | llm-agents (numtide/llm-agents.nix) keeps its **own** nixpkgs, does NOT follow | **Two nixpkgs** in one closure |
| nixpkgs | standalone Rust repos (lojix, spirit, orchestrate, dotos, datom, horizon-rs, agent, rust-build) each declare NixOS/nixpkgs?ref=nixos-unstable | Overridden by follows when consumed from CriomOS/CriomOS-home |
| nixpkgs | curriculum-deploy pins a specific NixOS/nixpkgs commit | Independent third pin (via primary) |
| home-manager | CriomOS root; CriomOS-home follows from root | Unified |
| crane | CriomOS-home owns; agent + aggregator + listener + message follow from it | Unified within Home |
| rust-build | CriomOS root; clavifaber follows; spirit, orchestrate, dotos, datom each declare own | Overridden by follows only for clavifaber; spirit/orchestrate get follows from CriomOS too |
| fenix | lojix, agent, rust-build each declare own; not a CriomOS root input | Each standalone build has own fenix |
| orchestrate | CriomOS pins 5b495422; CriomOS-home's flake.nix declares e0f3bc5e but follows override | Unified via follows |
| spirit | CriomOS pins 008d8ca0; CriomOS-home follows from CriomOS | Unified via follows |

## 2. Where Is X Defined

### Host/Node Identity and Hardware Facts

| Thing | Defined in | Consumed in |
|---|---|---|
| Node name, species, system, size, behavesAs, services, machine model, hasVideoOutput, useColemak, enableNetworkManager, adminSshPubKeys, sshPubKeyLine, criomeDomainName, wifiCert, builderConfigs | horizon-rs (Rust) projects from horizon.dotos into JSON; lojix materializes as `horizon` flake input | CriomOS: normalize.nix, edge/, metal/, network/, nix/builder.nix, users.nix, userHomes.nix, llm.nix, agent-intercom.nix, complex.nix, nspawn.nix, vm-testing/, router/, repository-receive.nix, mirror.nix, persona-router.nix, test-vm-host.nix, test-vm-guest.nix, test-substrate.nix. CriomOS-home: profiles/min/dictation.nix, all size-gated modules |
| Hardware model adjustments | CriomOS modules/nixos/hardware-adjustments/ | Consumed by metal/default.nix |
| networking.hostName | CriomOS modules/nixos/network/default.nix (= node.name from horizon) | Also set in multiple check fixtures |
| Disk layout | CriomOS modules/nixos/disks/ (preinstalled, liveiso, pod) | criomos.nix imports preinstalled |

### User Identity

| Thing | Defined in | Consumed in |
|---|---|---|
| User set (name, trust tiers, sshPubKeys, extraGroups, enableLinger, hasPubKey) | horizon-rs projects from horizon.dotos | CriomOS users.nix, userHomes.nix; CriomOS-home flake.nix mkHomeConfiguration |
| home.username, home.homeDirectory | CriomOS-home flake.nix mkHomeConfiguration | All home modules |
| home.stateVersion | CriomOS userHomes.nix ("26.05") **and** CriomOS-home flake.nix mkHomeConfiguration ("26.05") | **Defined in two places** (currently same value) |

### Capability/Size/Tier Gates

| Gate | Evaluated from | Key consumers |
|---|---|---|
| size.min, size.med, size.max (= atLeast predicates on node size) | horizon.node.size (horizon-rs derived) | CriomOS: edge/ (min/med/max package tiers), metal/ (firmware, libvirtd), normalize.nix. CriomOS-home: profiles/min/, med/, max/ |
| behavesAs.edge | horizon.node.behavesAs | CriomOS: edge/, normalize.nix, users.nix. CriomOS-home: dictation, niri, sfwbar, waybar |
| behavesAs.testVm | horizon.node.behavesAs | CriomOS: test-vm-guest.nix, test-vm-host.nix |
| AgentIntercomLocal, AgentIntercomGraphical | horizon.node.services (service vector) | CriomOS: agent-intercom.nix, users.nix. CriomOS-home: flake.nix (system gate), packages/agent-intercom |
| graphical gate (x86_64-linux only for graphical) | CriomOS-home flake.nix agentIntercomGraphicalSupported | CriomOS-home checks and packages |
| PersonaDevelopment capabilities | horizon.node.services PersonaDevelopment.capabilities | CriomOS: repository-receive.nix, mirror.nix |

### Package Definitions for Agent/Desktop Tools

| Package | Defined in | Source |
|---|---|---|
| Claude Code (CLI) | CriomOS-home packages/claude-code/ | Delegates to llm-agents.packages.claude-code |
| Claude Code (VSIX) | CriomOS-home flake.nix input claude-code-vsix | marketplace.visualstudio.com file download |
| Claude Desktop | CriomOS-home overlays/claude-desktop.nix (claudeDesktopWithDeclaredClaudeCode) | Patches nixpkgs claude-desktop to use declared claude-code |
| Codex (CLI) | CriomOS-home packages/codex/ | Delegates to llm-agents.packages.codex |
| Codex (VSIX = chatgpt) | CriomOS-home flake.nix input codex-chatgpt-vsix | marketplace.visualstudio.com file download |
| Emacs | CriomOS-home modules/home/profiles/med/emacs.nix + emacs/ignis-themes.nix | nixpkgs emacs + chroma-emacs resident |
| VSCodium | CriomOS-home modules/home/profiles/med/codium.nix + modules/home/vscodium/ | nixpkgs vscodium + extension overlays from CriomOS-pkgs |
| ChatGPT | No standalone package; Codex VSIX is named `chatgpt` in marketplace | See Codex VSIX above |
| Agent Intercom | CriomOS-home packages/agent-intercom/ | Built from ~15 npm tarball inputs + dataforxyz repos |
| Pi (continue/linkup/subagents/ultra-subagents/web-access) | CriomOS-home packages/pi-*/ | npm tarball inputs + earendil-works/pi, LiGoldragon forks |

### Overlays

| Overlay | Defined in | Applied where |
|---|---|---|
| nix-vscode-extensions.overlays.default | CriomOS-pkgs flake.nix | Baked into pkgs |
| openldap doCheck=false | CriomOS-pkgs flake.nix | Baked into pkgs |
| spamassassin doCheck=false | CriomOS-pkgs flake.nix | Baked into pkgs |
| gtk4 DMA-buffer patch | CriomOS-pkgs flake.nix | Baked into pkgs |
| claude-desktop patching | CriomOS-home overlays/claude-desktop.nix | Applied via CriomOS-home overlays/ |
| yt-dlp | CriomOS-home overlays/yt-dlp.nix | Applied via CriomOS-home overlays/ |
| CriomOS-home packageOverlays (aggregated) | CriomOS-home overlays/default.nix | pkgs.extend in CriomOS-home flake outputs |
| nixpkgs.overlays = mkOverride 0 [] | CriomOS normalize.nix:174 | Prevents downstream overlay injection on the NixOS target |

### Nixpkgs Pin

| Pin | Location |
|---|---|
| LiGoldragon/nixpkgs?ref=main (fork of nixpkgs-unstable) | CriomOS, CriomOS-home, CriomOS-pkgs (all aligned via follows) |
| NixOS/nixpkgs?ref=nixos-unstable | lojix, spirit, orchestrate, rust-build, agent, horizon-rs (standalone; overridden by follows when consumed) |
| NixOS/nixpkgs/nixpkgs-unstable | dotos, datom |
| numtide/llm-agents.nix own nixpkgs | llm-agents (NOT unified; separate package set) |
| NixOS/nixpkgs/<specific commit> | curriculum-deploy (via primary) |

### Home Manager Version

| Source | Location |
|---|---|
| nix-community/home-manager (latest) | CriomOS root input; CriomOS-home follows from it |

### Secrets Paths

| Secret | Defined in | Consumed in |
|---|---|---|
| sops.age.sshKeyPaths = /etc/ssh/ssh_host_ed25519_key | CriomOS secrets.nix | sops-nix module |
| sops.secrets.localLlmApiToken | CriomOS llm.nix | sopsFile from inputs.secrets.sopsFiles.localLlmApiToken |
| Router Wi-Fi SAE passwords | CriomOS router/default.nix | sopsFile from inputs.secrets.sopsFiles |
| secrets input itself | CriomOS flake.nix stub (empty); lojix overrides from cluster repo | Every sops consumer |
| goldragon/secrets/ directory | goldragon repo (not a flake) | Manually managed; lojix materializes the override |

### Hostnames/IPs/SSH

| Thing | Defined in |
|---|---|
| networking.hostName | CriomOS network/default.nix (= horizon.node.name) |
| LAN subnet 10.18.0.0/24, gateway 10.18.0.1 | CriomOS-lib constants AND criomos-horizon-config horizon.dotos **dual definition** |
| SSH known hosts | CriomOS normalize.nix (mkNodeKnownHost from horizon.exNodes) |
| SSH authorized keys | CriomOS users.nix (from horizon user.sshPubKeys + node.adminSshPubKeys) |
| Nix builder SSH | CriomOS nix/builder.nix (from horizon.node.builderConfigs) |
| Headscale port 8443 | CriomOS-lib constants |

### Deployment Selection

| Mechanism | Location |
|---|---|
| DOTOS manifests (.dotos files in primary/manifests/) | Currently empty directory |
| horizon.dotos (cluster/node declaration) | criomos-horizon-config (12-line DOTOS file) |
| goldragon datom.dotos, synchronizer.dotos | goldragon repo (not Nix) |
| Lojix orchestrator | Materializes system/horizon/deployment/secrets stubs at deploy time |
| deployment input shape (includeHome, includeAllFirmware) | CriomOS stubs/default-deployment/flake.nix; lojix overrides |

## 3. Build Path

```
horizon.dotos (criomos-horizon-config)
       |
       v
horizon-rs (Rust CLI: `horizon-cli project`)
       |  produces per-node JSON "horizon" flake
       v
lojix (deploy orchestrator)
  |  reads cluster config, produces:
  |    - system flake (tiny: `system = "x86_64-linux"`)
  |    - horizon flake (projected JSON for this node)
  |    - deployment flake (includeHome, includeAllFirmware)
  |    - secrets override (from goldragon/secrets/)
  |  overrides CriomOS's stub inputs via --override-input
  v
CriomOS/flake.nix evaluates:
  1. inputs.system.system -> system tuple
  2. inputs.horizon.horizon -> full horizon data (JSON parsed by Nix)
  3. inputs.pkgs (CriomOS-pkgs) -> import nixpkgs { system; overlays }
  4. inputs.criomos-home.homeConfigurations -> pkgs (gets the exact extended pkgs)
  5. nixosSystem { pkgs; specialArgs = { horizon, system, deployment, inputs, constants }; }
     modules = [ readOnlyPkgs, home-manager (if includeHome), criomos module ]
  6. criomos.nix imports ~25 module files covering the full system
  7. userHomes.nix embeds CriomOS-home's homeModules.default per user (filtered by hasPubKey)
  |
  outputs:
    nixosConfigurations.target = the NixOS system
    homeConfigurations = projection from target.config.home-manager.users (not independent eval)
    independentHomeConfigurations = CriomOS-home's own homeConfigurations (for comparison)
```

Data from horizon-rs enters as **Nix-evaluable JSON** (a flake whose output is an attrset). No generated Nix files are checked in; horizon.dotos is the authored source and horizon-rs projects it to JSON at deploy time. The `system` stub is likewise a tiny generated flake.

No generated or vendored Nix trees are checked into any repository.

## 4. Size

| Repository | Nix Lines | Nix Files | Modules | Checks |
|---|---|---|---|---|
| CriomOS | 9,177 | 84 | 49 | 25 |
| CriomOS-home | 15,132 | 118 | 39 | 46 |
| CriomOS-lib | 356 | 5 | 0 | 0 |
| CriomOS-pkgs | 73 | 2 | 0 | 0 |
| spirit | 1,296 | 2 | 0 | 0 |
| rust-build | 223 | 2 | 0 | 0 |
| lojix | 208 | 1 | 0 | 0 |
| clavifaber | 173 | 1 | 0 | 0 |
| orchestrate | 114 | 1 | 0 | 0 |
| dotos | 112 | 1 | 0 | 0 |
| brightness-ctl | 84 | 3 | 0 | 0 |
| horizon-rs | 82 | 1 | 0 | 0 |
| agent | 78 | 1 | 0 | 0 |
| datom | 73 | 1 | 0 | 0 |
| curriculum-deploy | 65 | 1 | 0 | 0 |
| **Total** | **~27,246** | **~224** | **88** | **71** |

No vendored or generated Nix trees found in any repository.

## 5. Unknowns

1. **goldragon/secrets/ structure**: the secrets directory exists but its internal structure (which sopsFiles, which age keys) was not inspected (private data).
2. **Exact lojix deploy invocation**: how lojix passes `--override-input` for system/horizon/deployment/secrets — inspecting lojix source was not in scope.
3. **LiGoldragon/nixpkgs fork delta**: how far the fork has diverged from upstream nixpkgs-unstable.
4. **llm-agents internal nixpkgs version**: which nixpkgs commit llm-agents uses for its separate package set.
5. **CriomOS-home packages/agent-intercom build**: exactly how the ~15 npm tarball inputs are assembled (the package/default.nix was not read in full).
6. **spirit flake full outputs shape**: the outputs section was cut at 80 lines; the full service/package export surface is partially known.
7. **CriomOS-test-cluster repo**: exists under LiGoldragon but was not surveyed.
8. **Whether manifests/ was recently emptied or is intentionally blank**: the directory exists in primary but contains no files.
9. **horizon-rs projected JSON schema**: the exact set of fields the Nix side expects from the projected horizon was inferred from grep, not from a formal schema document.
10. **niri-flake's own nixpkgs**: overridden by follows; whether niri-flake or stylix carry any non-followed transitive inputs is not confirmed.
11. **llm-agents crane/fenix vs CriomOS-home crane**: llm-agents has its own build toolchain; whether that creates duplicate Rust toolchains in the closure is unknown.
12. **primary flake.nix full outputs**: only the inputs section was read (it outputs workspace skill surfaces, not system configurations).
