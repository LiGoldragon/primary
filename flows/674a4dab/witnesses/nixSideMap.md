## Nix Side Map of the CriomOS Stack

Method: code read flake.nix, flake.lock, modules/**/*.nix across CriomOS, CriomOS-home, CriomOS-lib, CriomOS-pkgs, criomos-horizon-config, curriculum-deploy, primary, horizon-rs, lojix, dotos, datom, spirit, orchestrate, hexis
Method: probe find -name '*.nix' | wc -l
Method: probe wc -l $(find ... -name '*.nix')
Method: probe python3 flake.lock parser for input graph, nixpkgs pins, follows
Method: probe grep -rn for behavesAs, size, horizon, overlays, homeConfigurations, secrets, imports, matchBlocks

### 1. Flake-Input Graph

```
                              ┌──────────────────────────────────┐
                              │         lojix (daemon)           │
                              │  Materializes per-deploy:        │
                              │   system, horizon, secrets,      │
                              │   deployment overrides           │
                              └──────────┬───────────────────────┘
                                         │ overrides inputs at eval time
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │                          CriomOS (the system)                       │
  │  inputs.nixpkgs ──────────── LiGoldragon/nixpkgs (fork, ref=main)  │
  │  inputs.blueprint ────────── numtide/blueprint                      │
  │  inputs.home-manager ─────── nix-community/home-manager             │
  │  inputs.sops-nix ─────────── Mic92/sops-nix                         │
  │  inputs.rust-overlay ─────── oxalica/rust-overlay                   │
  │  inputs.rust-build ───────── LiGoldragon/rust-build                 │
  │  inputs.criomos-lib ──────── LiGoldragon/CriomOS-lib                │
  │  inputs.orchestrate ──────── LiGoldragon/orchestrate (commit pin)   │
  │  inputs.spirit ───────────── LiGoldragon/spirit (commit pin)        │
  │  inputs.lojix ────────────── LiGoldragon/lojix (commit pin)         │
  │  inputs.brightness-ctl ───── LiGoldragon/brightness-ctl             │
  │  inputs.microvm ──────────── astro/microvm.nix                      │
  │  inputs.repository-ledger ── LiGoldragon/repository-ledger          │
  │  inputs.mirror ───────────── LiGoldragon/mirror                     │
  │  inputs.router ───────────── LiGoldragon/router                     │
  │  inputs.criome ───────────── LiGoldragon/criome                     │
  │  inputs.clavifaber ──────── LiGoldragon/clavifaber                  │
  │  inputs.pkgs ─────────────── LiGoldragon/CriomOS-pkgs ◄────────┐   │
  │  inputs.criomos-home ─────── LiGoldragon/CriomOS-home ◄─────┐  │   │
  │  inputs.system ───────────── path:./stubs/no-system (stub)   │  │   │
  │  inputs.horizon ──────────── path:./stubs/no-horizon (stub)  │  │   │
  │  inputs.deployment ───────── path:./stubs/default-deployment │  │   │
  │  inputs.secrets ──────────── path:./stubs/no-secrets (stub)  │  │   │
  │                                                              │  │   │
  │  follows chains:                                             │  │   │
  │    criomos-home.nixpkgs → nixpkgs                            │  │   │
  │    criomos-home.home-manager → home-manager                  │  │   │
  │    criomos-home.criomos-lib → criomos-lib                    │  │   │
  │    criomos-home.rust-overlay → rust-overlay                  │  │   │
  │    criomos-home.horizon → horizon                            │  │   │
  │    criomos-home.system → system                              │  │   │
  │    criomos-home.pkgs → pkgs                                  │  │   │
  │    criomos-home.orchestrate → orchestrate                    │  │   │
  │    criomos-home.spirit → spirit                              │  │   │
  │    pkgs.nixpkgs → nixpkgs                                    │  │   │
  │    pkgs.system → system                                      │  │   │
  │    clavifaber.rust-build → rust-build                        │  │   │
  │    all others .nixpkgs → nixpkgs                             │  │   │
  └──────────────────────────────────────────────────────────────────────┘
                                                                 │  │
  ┌──────────────────────────────────────────────────────────────┐│  │
  │                    CriomOS-home (user env)                   ││  │
  │  inputs.nixpkgs ── LiGoldragon/nixpkgs (fork)               ││  │
  │  inputs.blueprint ── numtide/blueprint                       ││  │
  │  inputs.crane ── ipetkov/crane                               ││  │
  │  inputs.rust-overlay ── oxalica/rust-overlay                 ││  │
  │  inputs.home-manager ── nix-community/home-manager           ││  │
  │  inputs.system ── path:./stubs/no-system (stub)              ││  │
  │  inputs.pkgs ── LiGoldragon/CriomOS-pkgs                    │┘  │
  │  inputs.horizon ── path:./stubs/no-horizon (stub)            │   │
  │  inputs.criomos-lib ── LiGoldragon/CriomOS-lib               │   │
  │  inputs.hexis ── LiGoldragon/hexis                            │   │
  │  inputs.stylix ── danth/stylix                                │   │
  │  inputs.niri-flake ── sodiboo/niri-flake                      │   │
  │  inputs.noctalia ── LiGoldragon/noctalia (commit pin)         │   │
  │  inputs.llm-agents ── numtide/llm-agents.nix (commit pin)    │   │
  │    *** keeps its OWN nixpkgs (NixOS/nixpkgs, not the fork)   │   │
  │  inputs.herdr ── herdrdev/herdr (tag v0.8.2)                  │   │
  │  inputs.orca-ide ── Samuka007/nix-orca (commit pin)           │   │
  │  inputs.spirit ── LiGoldragon/spirit (commit pin)             │   │
  │  inputs.agent ── LiGoldragon/agent (commit pin)               │   │
  │  inputs.aggregator ── LiGoldragon/aggregator (commit pin)     │   │
  │  inputs.orchestrate ── LiGoldragon/orchestrate (commit pin)   │   │
  │  inputs.message ── LiGoldragon/message (commit pin)           │   │
  │  inputs.chroma ── LiGoldragon/chroma (commit pin)             │   │
  │  inputs.chroma-emacs ── LiGoldragon/chroma-emacs (commit pin) │   │
  │  inputs.listener ── LiGoldragon/listener                      │   │
  │  inputs.substack-cli ── LiGoldragon/substack-cli              │   │
  │  inputs.claude-answers ── LiGoldragon/claude-answers          │   │
  │  inputs.google-workspace-cli ── googleworkspace/cli           │   │
  │  inputs.pi-session-namer ── LiGoldragon/pi-session-namer      │   │
  │  inputs.pyproject-nix ── pyproject-nix/pyproject.nix          │   │
  │  inputs.uv2nix ── pyproject-nix/uv2nix                       │   │
  │  inputs.pyproject-build-systems ── pyproject-nix/build-sys    │   │
  │                                                               │   │
  │  non-flake source inputs (flake=false):                       │   │
  │    yt-dlp, visualjj-vsix, claude-code-vsix,                   │   │
  │    codex-chatgpt-vsix, annas-mcp, mentci-src, pi-src,         │   │
  │    agent-intercom-{pi,codex,claude,opencode,orchestrator,     │   │
  │    core}-src, pi-linkup-src, pi-utils-ui-src,                  │   │
  │    pi-subagents-src, primary-generated-src,                    │   │
  │    agent-intercom-{tsx,typebox,esbuild,esbuild-linux-x64,     │   │
  │    esbuild-linux-arm64,get-tsconfig,resolve-pkg-maps}-src,    │   │
  │    pi-ultra-subagents-src, pi-ultra-subagents-typebox-src,    │   │
  │    pi-continue-src, pi-web-access-*-src (~20 npm tarballs)    │   │
  │                                                               │   │
  │  All .nixpkgs follow → nixpkgs except llm-agents              │   │
  │  crane, agent, aggregator, message, listener follow → crane   │   │
  └───────────────────────────────────────────────────────────────┘   │
                                                                      │
  ┌───────────────────────────────────────────────────────────────┐    │
  │                     CriomOS-pkgs                              │    │
  │  inputs.nixpkgs ── LiGoldragon/nixpkgs (fork)                │◄───┘
  │  inputs.system ── path:./stubs/no-system (stub)               │
  │  inputs.nix-vscode-extensions ── nix-community/...            │
  │    .nixpkgs follows → nixpkgs                                 │
  │  Output: pkgs = import nixpkgs { system; allowUnfree=true;    │
  │    overlays = [ nix-vscode-extensions, openldap-noCheck,      │
  │    spamassassin-noCheck, gtk4-dmabuf-patch ] }                │
  └───────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────┐
  │                       CriomOS-lib                             │
  │  No inputs (pure library flake).                              │
  │  Outputs: lib = { constants, importJSON, mkJsonMerge,         │
  │                   fetchHfModel }                              │
  └───────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────┐
  │                   criomos-horizon-config                      │
  │  NOT a flake. Contains horizon.dotos only.                    │
  │  horizon-rs CLI reads this DOTOS, projects per-node JSON.     │
  │  lojix writes that JSON as a content-addressed flake.         │
  └───────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────┐
  │                     primary (workspace)                       │
  │  inputs.dotos, dotos-config, dotos-text-query,                │
  │    tree-sitter-dotos ── all non-flake (commit pins)           │
  │  inputs.curriculum-deploy ── LiGoldragon/curriculum-deploy    │
  │  inputs.curriculum ── non-flake (commit pin)                  │
  │  inputs.nixpkgs follows → curriculum-deploy/nixpkgs           │
  │  Output: apps for generate-skills / check-skills              │
  └───────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────┐
  │                   curriculum-deploy                            │
  │  inputs.nixpkgs ── NixOS/nixpkgs (pinned commit, NOT fork)   │
  │  inputs.flake-utils ── numtide/flake-utils                    │
  │  inputs.rust-build ── LiGoldragon/rust-build                  │
  │  inputs.curriculum ── non-flake (commit pin)                  │
  │  Output: Rust binary curriculum-deploy                        │
  └───────────────────────────────────────────────────────────────┘

Independent tool repos (not consumed by CriomOS/Home directly):
  horizon-rs: NixOS/nixpkgs (unstable), fenix, crane
  lojix:      NixOS/nixpkgs (unstable), flake-utils, fenix, crane
  dotos:      NixOS/nixpkgs (unstable), flake-utils, rust-build
  datom:      NixOS/nixpkgs (unstable), flake-utils, rust-build
```

#### Nixpkgs duplication across the locked graph

When CriomOS evaluates with its lock, 5 distinct nixpkgs revisions are present:

| Lock node | Owner | Rev (prefix) | Entered via |
|-----------|-------|-------------|-------------|
| nixpkgs_4 | LiGoldragon | 0e251e24a4f2 | Root nixpkgs (the fork) — all follows chain here |
| nixpkgs   | NixOS | f83fc3c307e7 | herdr (no follows) |
| nixpkgs-stable | NixOS | b6018f87da91 | stylix.nixpkgs-stable |
| nixpkgs_2 | NixOS | 174eb786fb68 | llm-agents (deliberately keeps its own) |
| nixpkgs_3 | NixOS | e7a3ca8092b6 | orca-ide (no follows) |

CriomOS-home's own lock has the same 5 pattern.

#### Key follows chains

- CriomOS forces CriomOS-home to share its nixpkgs, home-manager, criomos-lib, rust-overlay, horizon, system, pkgs, orchestrate, and spirit.
- CriomOS-pkgs gets nixpkgs and system from CriomOS via follows.
- Rust service repos (agent, aggregator, message, listener) get crane and nixpkgs from CriomOS-home via follows.
- spirit gets nixpkgs from its consumer (CriomOS or CriomOS-home).

**Unfollowed divergences:**
- llm-agents: deliberately keeps NixOS/nixpkgs (different pnpm attrs needed).
- herdr: its own NixOS/nixpkgs, no follows from Home.
- orca-ide: its own NixOS/nixpkgs, no follows from Home.
- stylix: brings nixpkgs-stable (NixOS/nixpkgs stable branch).
- curriculum-deploy: its own NixOS/nixpkgs pin.
- horizon-rs, lojix, dotos, datom: each independently pin NixOS/nixpkgs (unstable). Not consumed as flake inputs by the deploy graph.

### 2. "Where Is X Defined" Tables

#### Host/Node Identity and Hardware Facts

| What | Defined in | Consumed by |
|------|-----------|-------------|
| Cluster topology (nodes, users, services, domain) | criomos-horizon-config/horizon.dotos | horizon-rs CLI → lojix → CriomOS (via horizon input override) |
| Node species, behavesAs, size | horizon-rs (Rust schema, projected JSON) | CriomOS modules (normalize, edge, users, nix, network, nspawn, router, vm-testing, test-vm-guest, test-vm-host, agent-intercom, spirit, lojix-persona-development); CriomOS-home modules (min/*, med/*, max/*, vscodium) |
| Hardware model | horizon.node.machine.model | CriomOS hardware-adjustments, CriomOS-home sway.nix |
| System tuple (x86_64-linux etc.) | lojix writes content-addressed system flake | CriomOS-pkgs (system.system), CriomOS (inputs.system) |
| networking.hostName | CriomOS network/default.nix: horizon.node.name | NixOS networking stack |
| networking.hosts | CriomOS network/default.nix: from horizon.exNodes | NixOS, test-vm-host |

#### User Identity

| What | Defined in | Consumed by |
|------|-----------|-------------|
| User list + per-user attrs (trust, size, sshPubKeys, extraGroups, hasPubKey, useColemak, isMultimediaDev, enableLinger) | horizon-rs projected JSON → horizon.users | CriomOS users.nix (system users); CriomOS userHomes.nix (home filter); CriomOS-home flake.nix mkHomeConfiguration; CriomOS-home modules via user arg |
| home.username, home.homeDirectory | CriomOS-home flake.nix mkHomeConfiguration | home-manager |
| home.stateVersion | CriomOS-home flake.nix ("26.05") AND CriomOS userHomes.nix ("26.05") | home-manager — **DUAL DEFINITION** |

#### Capability/Size/Tier Gates

| Gate | Source | Files consuming it |
|------|--------|-------------------|
| node.behavesAs.edge | horizon-rs projection | CriomOS: edge/, normalize, users, hardware-adjustments, disks; Home: niri, sfwbar, waybar, chroma, dictation, ui-priority, active-network |
| node.behavesAs.center | horizon-rs | CriomOS: networkd, nspawn, nix/client |
| node.behavesAs.router | horizon-rs | CriomOS: router/, dnsmasq, wifi-pki, resolver, networkd |
| node.behavesAs.bareMetal | horizon-rs | CriomOS: hardware-adjustments, disks/liveiso |
| node.behavesAs.testVm | horizon-rs | CriomOS: test-vm-guest, test-vm-host |
| node.behavesAs.largeAi | horizon-rs | Home: pi-models.nix |
| node.size.{min,medium,large,max} | horizon-rs | CriomOS: normalize, nix/retention-agent, edge, nspawn; Home: nearly all profile modules |
| user.size.{min,medium,large,max} | horizon-rs (per-user) | Home: bitwarden, pi-models, agent-intercom, default-opener, spirit, message, aggregator, chroma, dictation, sway, cli-tools, codium, max, browser-use, vscodium, qutebrowser |
| user.trust.{min,medium} | horizon-rs | CriomOS: users.nix (extraGroups); Home: min/default.nix |
| AgentIntercomLocal service | horizon.node.services | CriomOS: agent-intercom.nix, users.nix; Home: agent-intercom.nix |
| AgentIntercomGraphical service | horizon.node.services | CriomOS: agent-intercom.nix, users.nix; Home: agent-intercom.nix |
| PersonaDevelopment service | horizon.node.services | CriomOS: lojix-persona-development, repository-receive; Home: spirit.nix |

#### Package Definitions for Agent/Desktop Tools

| Tool | Defined in | Consumed by |
|------|-----------|-------------|
| Claude Code (CLI) | Home packages/claude-code/default.nix (from llm-agents input) | Home profiles/med/cli-tools.nix |
| Claude Code (VSCode ext) | Home flake.nix: claude-code-vsix input (marketplace file) | Home vscodium/vscodium/default.nix |
| Claude Desktop | Home overlays/claude-desktop.nix (overlay on nixpkgs.claude-desktop) | Home via pkgs overlay |
| Codex (CLI/TUI) | Home packages/codex/default.nix + tui.nix (from llm-agents input) | Home agent-intercom.nix |
| Codex (VSCode ext) | Home flake.nix: codex-chatgpt-vsix input (marketplace file) | Home vscodium/vscodium/default.nix |
| ChatGPT | (same as Codex VSCode ext — codex-chatgpt-vsix) | Home vscodium |
| Emacs | Home profiles/med/emacs.nix + emacs/ignis-themes.nix | Home default module |
| VSCodium | Home profiles/med/codium.nix + vscodium/vscodium/default.nix | Home default module |
| Pi (coding agent CLI) | Home packages/pi/default.nix (from pi-src non-flake input) | Home profiles/med/cli-tools.nix |
| Agent Intercom | Home packages/agent-intercom/default.nix (from multiple non-flake inputs) | Home profiles/min/agent-intercom.nix |
| Herdr | Home flake.nix: herdr input (tag v0.8.2, own flake) | Home (agent harness) |
| Orca | Home flake.nix: orca-ide input (commit pin, own flake) | Home (agent harness) |
| Mentci | Home packages/mentci/default.nix (from mentci-src non-flake) | Home profiles |
| Browser-use | Home packages/browser-use/default.nix (uv2nix toolchain) | Home profiles/max/browser-use.nix |

#### Overlays

| Overlay | Defined in | Applied where |
|---------|-----------|---------------|
| nix-vscode-extensions | CriomOS-pkgs flake.nix | pkgs set (allowUnfree=true) |
| openldap doCheck=false | CriomOS-pkgs flake.nix | pkgs set |
| spamassassin doCheck=false | CriomOS-pkgs flake.nix | pkgs set |
| gtk4 DMA-buffer patch | CriomOS-pkgs flake.nix | pkgs set |
| claude-desktop | CriomOS-home overlays/claude-desktop.nix | CriomOS-home pkgs (via composeManyExtensions) |
| yt-dlp | CriomOS-home overlays/yt-dlp.nix | CriomOS-home pkgs |

#### Nixpkgs Pin

| Pin | Repo | Rev prefix |
|-----|------|-----------|
| LiGoldragon/nixpkgs (fork, ref=main) | CriomOS, CriomOS-home, CriomOS-pkgs (all via follows) | 0e251e24a4f2 |
| NixOS/nixpkgs (llm-agents own) | CriomOS-home → llm-agents | 174eb786fb68 |
| NixOS/nixpkgs (herdr own) | CriomOS-home → herdr | f83fc3c307e7 |
| NixOS/nixpkgs (orca-ide own) | CriomOS-home → orca-ide | e7a3ca8092b6 |
| NixOS/nixpkgs (stylix-stable) | CriomOS-home → stylix | b6018f87da91 |
| NixOS/nixpkgs (curriculum-deploy) | primary → curriculum-deploy | 2d1e72b652ee (independent) |

#### Home Manager Version

| Source | Consumed by |
|--------|------------|
| nix-community/home-manager (follows from CriomOS to CriomOS-home) | Both repos share one pin via follows |

#### Secrets Paths

| What | Defined in | Consumed by |
|------|-----------|-------------|
| sops-nix module import | CriomOS modules/nixos/secrets.nix | NixOS sops |
| sops.age.sshKeyPaths | CriomOS secrets.nix: /etc/ssh/ssh_host_ed25519_key | sops-nix |
| secrets sopsFiles | CriomOS stubs/no-secrets: empty by default | lojix overrides per deploy from cluster repo |
| gopass secrets (e.g. goldragon.criome/local-llm-api-token) | CriomOS-home pi-models.nix (gopass show command) | Pi model config |

#### Hostnames/IPs/SSH

| What | Defined in |
|------|-----------|
| networking.hostName | CriomOS network/default.nix from horizon.node.name |
| LAN subnet 10.18.0.0/24, gateway 10.18.0.1 | CriomOS-lib constants AND criomos-horizon-config/horizon.dotos — **DUAL DEFINITION** |
| SSH matchBlocks (prometheus.goldragon.criome) | CriomOS-home min/default.nix (hardcoded) |
| SSH host keys for builders | CriomOS nix/builder.nix from horizon.node |
| Yggdrasil network config | CriomOS-lib constants |

#### Deployment Selection

| What | Defined in |
|------|-----------|
| Deploy orchestration | lojix daemon (Rust binary) |
| Input overrides (system, horizon, secrets, deployment) | lojix writes content-addressed flakes, overrides CriomOS inputs |
| deployment.includeHome | CriomOS stubs/default-deployment (default true); lojix can override |
| deployment.includeAllFirmware | CriomOS stubs/default-deployment (default true) |
| Deployment selection (which manifests) | /home/li/primary/manifests/ (currently empty directory) |

### 3. Build Path

1. **horizon-rs** reads criomos-horizon-config/horizon.dotos (DOTOS format), projects per-(cluster, node, user) JSON.
2. **lojix** (daemon-based deploy orchestrator) takes a deploy request, runs horizon-rs projection, and writes:
   - A content-addressed system flake (system = "x86_64-linux")
   - A content-addressed horizon flake (the projected JSON as Nix attrset)
   - A content-addressed secrets flake (from cluster repo's sops files)
   - Optionally a deployment flake (e.g. includeHome = false)
   Then evaluates CriomOS with --override-input for each.
3. **CriomOS** evaluates nixosConfigurations.target:
   - pkgs comes from CriomOS-pkgs (instantiates nixpkgs with system + overlays).
   - CriomOS-home's pkgs is used directly: (builtins.head (builtins.attrValues inputs.criomos-home.homeConfigurations)).pkgs.
   - nixosSystem receives pkgs, horizon, system, deployment, inputs, constants, criomos-lib as specialArgs.
   - Imports nixosModules.criomos (the top aggregate) which imports all system modules.
   - When includeHome, imports userHomes.nix which wires home-manager.sharedModules = [ inputs.criomos-home.homeModules.default ].
4. **CriomOS-home** homeModules.default wraps blueprint's module + imports stylix, niri-flake, noctalia home modules. Forces _module.args.inputs to CriomOS-home's own inputs (not CriomOS's).
5. **homeConfigurations** are produced two ways:
   - Embedded: inside nixosConfigurations.target via home-manager nixos module (canonical for deploy).
   - Standalone: CriomOS-home.homeConfigurations from mkHomeConfiguration using horizon.users (exposed as independentHomeConfigurations by CriomOS for equivalence checking).
6. **Data format**: horizon data enters as Nix attrsets (projected from JSON by lojix). No checked-in generated JSON files were found in CriomOS or CriomOS-home. The criomos-horizon-config/horizon.dotos is the authored source (DOTOS format, read by horizon-rs Rust CLI). CriomOS-lib carries data/largeAI/llm.json (LLM model metadata).

### 4. Size

| Repository | .nix files | Lines of Nix | Modules | Checks | Packages | Stubs |
|-----------|-----------|-------------|---------|--------|----------|-------|
| CriomOS | 84 | 9,177 | 49 (modules/nixos/) | 25 (checks/) | — | 4 |
| CriomOS-home | 118 | 15,132 | 23 (modules/home/) | 46 (checks/) | 29 (packages/) | 2 |
| CriomOS-lib | 5 | 356 | — | — | — | — |
| CriomOS-pkgs | 2 | 73 | — | — | — | 1 |
| **Total** | **209** | **24,738** | **72** | **71** | **29** | **7** |

Lock file sizes: CriomOS ~170 nodes, CriomOS-home ~207 nodes.

Non-flake source inputs in CriomOS-home: ~40+ (npm tarballs, VSIX files, git repos as source).

CriomOS-home carries no vendored Nix trees. Its packages/ directory builds derivations from flake-pinned source inputs (npm tarballs, VSIX files, git sources).

### 5. Unknowns

1. **Exact horizon-rs projection output shape.** The projected JSON schema (what fields horizon-rs emits for node, user, cluster, behavesAs, size, services, machine, exNodes) is defined in the horizon-rs Rust source under lib/ and cli/. Exact field set not fully read.

2. **How lojix writes the content-addressed horizon/system/secrets flakes.** The Rust source references FlakeInputOverride and horizon_materialized, but the exact template/mechanism was not fully traced.

3. **What CriomOS-test-cluster contains** and whether it carries additional horizon configs or test node definitions.

4. **The full set of secrets keys.** Only the sops integration point (secrets.nix) and the stub were read; actual sopsFile paths are injected by lojix from cluster repos at deploy time.

5. **Whether any LiGoldragon crate repos (signal-*, spirit-judge, etc.) consumed transitively by CriomOS carry their own Nix modules.** The CriomOS lock shows ~60 LiGoldragon repos as inputs, but most are consumed via the spirit, lojix, or other top-level flake that re-exports their packages.

6. **The nixpkgs fork's delta.** LiGoldragon/nixpkgs ref=main is used by the deploy graph; its patches/differences from upstream NixOS/nixpkgs were not inspected.

7. **Exact noctalia, niri-flake, stylix option surfaces** and their interaction with CriomOS-home modules.

8. **The rust-build flake's exact contents.** Used by dotos, datom, clavifaber, orchestrate, curriculum-deploy, spirit; provides lib.${system}.fromPkgs and fromToolchainFile.

9. **Whether goldragon (no flake.nix) carries any Nix-consumed data files.** Listed in the namespace but has no flake.

10. **The full list of Agent Intercom npm dependency inputs.** CriomOS-home carries ~20 individual npm tarball inputs for Agent Intercom + Pi web-access; the dependency closure and build mechanism in packages/agent-intercom/default.nix and packages/pi-web-access/default.nix were not fully read.
