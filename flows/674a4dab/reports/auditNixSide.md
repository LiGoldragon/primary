# Audit: Nix Side of the CriomOS Stack

Method: code read of flake.nix, all modules, checks, stubs, gates, overlays, and packages across CriomOS, CriomOS-home, CriomOS-lib, CriomOS-pkgs, and criomos-horizon-config. No builds; `nix eval` and `nix flake metadata` only. Evidence by file:line. Psyche statements quoted from `flows/674a4dab/reports/psycheOsHomeGoldragon.md` and `flows/674a4dab/reports/psycheLojix.md`. Repository origin data from `flows/674a4dab/reports/psycheStackOrigins.md`.

**Origin note**: The CriomOS/CriomOS-home split (2026-04-23), CriomOS-lib extraction (2026-04-25), CriomOS-pkgs extraction (2026-04-27), and criomos-horizon-config creation (2026-05-17) were all agent-executed with no surviving psyche quote ordering them. The psyche's own later rulings (Home equivalence fed only from Horizon; one shared source consumed directly; criomos-core supersedes CriomOS-lib) are the authority. Weighed accordingly throughout.

---

## 1. Planes as they are

| Repository | Concerns actually held | Concerns that do not belong |
|---|---|---|
| **CriomOS** (84 .nix, 9177 lines) | System modules (49): normalize, users, network, nix, edge, metal, disks, secrets, lojix, spirit, criome, mirror, persona-router, repository-receive, nspawn, llm, agent-intercom, vm-testing, hardware-adjustments. Checks (25). Stubs (4). Bootstrap app re-export. Home-activation-equivalence check. | `pkgs` extraction from Home (flake.nix:160); embedded Home wiring passes `constants` from CriomOS-lib (userHomes.nix:44); agent-intercom.nix uses AgentIntercomGraphical gate (line 11); `normalize.nix:174` force-clears overlays (contradicts pkgs-from-Home flow); `mirror.nix:30` force-disabled dead module |
| **CriomOS-home** (118 .nix, 15132 lines) | Home modules (23 + profiles), packages (29), overlays (2), checks (46). 80 flake inputs (48 non-flake source tarballs). | `agent-intercom.nix:28` gates on AgentIntercomGraphical; `agent-intercom.nix:36` gates on x86_64 (`homeSystem == "x86_64-linux"`); `min/default.nix:534` hardcodes `prometheus.goldragon.criome` SSH matchBlock; `flake.nix:456` hardcodes `agentIntercomGraphicalSupported = system: system == "x86_64-linux"`; `llm-agents` keeps its own NixOS/nixpkgs (not the fork); `herdr`, `orca-ide` each keep independent nixpkgs pins |
| **CriomOS-lib** (5 .nix, 356 lines) | Constants (filesystem paths, network addresses), fetchHfModel helper, importJSON, mkJsonMerge | `constants.network.lan` (subnet `10.18.0.0/24`, gateway `10.18.0.1`) duplicates horizon.dotos:8-9; entire repository superseded by psyche-approved criomos-core |
| **CriomOS-pkgs** (2 .nix, 73 lines) | Instantiates nixpkgs with system + overlays (nix-vscode-extensions, openldap-noCheck, spamassassin-noCheck, gtk4 DMA-buffer patch) | Clean; concern is correctly scoped |
| **criomos-horizon-config** (not a flake) | Authored horizon.dotos — cluster topology, nodes, users, services | Clean; the authored source of truth for Horizon |

---

## 2. Findings

### F1. OS extracts pkgs from Home's first homeConfiguration

**What it is**: CriomOS flake.nix:160 reads `(builtins.head (builtins.attrValues inputs.criomos-home.homeConfigurations)).pkgs` — the OS's package set comes from whichever Home configuration `builtins.attrValues` returns first (order undefined by the Nix spec).

**Evidence**: `CriomOS/flake.nix:160`:
```nix
pkgs = (builtins.head (builtins.attrValues inputs.criomos-home.homeConfigurations)).pkgs;
```
Then passed as the `pkgs` argument to `nixosSystem` (line 241) and to `home-manager.extraSpecialArgs` (userHomes.nix:44).

**Psyche departure**: "there should be no difference between the embedded and independent home. the part which is shared ought to be directly from lojix-emitted horizon output, or from a shared nix machinery which uses the said horizon as input only" (psycheOsHomeGoldragon §Home equivalence, 2026-08-23). The pkgs set should come from CriomOS-pkgs (which it does via follows), not extracted backwards from Home's evaluation.

**Disconfirming evidence**: The comment says "CriomOS-home constructs its standalone Home configurations from an extension of the shared package set. Use that exact package-set value for the NixOS target as well, so the embedded Home projection and the independently exposed Home configuration retain one activation identity." This ensures the `home-activation-equivalence` check passes (identical store paths). Without it, Home's overlays (claude-desktop, yt-dlp) would not be in the OS's pkgs and the two activation packages would differ.

**Survival**: The equivalence concern is real, but the solution inverts the dependency: OS depends on Home's evaluation rather than both depending on a shared source. criomos-core or an extended CriomOS-pkgs that includes Home's overlays would resolve this without the inversion.

**Severity**: Blocks the psyche's stated design (Home determines OS pkgs).

---

### F2. normalize.nix force-clears overlays at priority 0

**What it is**: `CriomOS/modules/nixos/normalize.nix:174`: `nixpkgs.overlays = mkOverride 0 [];` — forcibly removes all overlays after the pkgs set was already imported with them.

**Evidence**: Line 174. The comment says "Overlays are bad - force them off."

**Psyche departure**: Not directly ruled on, but this creates a contradiction: pkgs enters with overlays (from CriomOS-pkgs), then normalize tries to clear them. With `readOnlyPkgs` active (flake.nix:252), `nixpkgs.overlays` is effectively a no-op (the pkgs import already happened). But the priority-0 override prevents any module from declaring overlays.

**Disconfirming evidence**: With `readOnlyPkgs`, this is defensive rather than operational — it can't change the already-imported pkgs. It prevents accidental overlay declarations in downstream modules.

**Survival**: Defensible as a guard, but the comment "Overlays are bad" misrepresents the design — overlays are applied (in CriomOS-pkgs), just not here.

**Severity**: Cosmetic / adds unasked machinery.

---

### F3. Embedded Home receives `constants` from the OS evaluation

**What it is**: `CriomOS/modules/nixos/userHomes.nix:44` passes `constants` (from CriomOS-lib) into Home via `extraSpecialArgs`.

**Evidence**:
```nix
extraSpecialArgs = {
  inherit horizon constants pkgs;
  homeSystem = pkgs.stdenv.hostPlatform.system;
};
```
Home modules then use `constants` (e.g., `min/default.nix` uses `constants.fileSystem.home.ensuredDirectories`; `dnsmasq.nix` and others use `constants.network.lan`).

**Psyche departure**: "whatever in home is currently originating in the OS must originate from the horizon or the extended-horizon" (psycheOsHomeGoldragon §Home equivalence, 2026-08-23). Constants come from CriomOS-lib, not Horizon.

**Disconfirming evidence**: CriomOS-home's standalone mkHomeConfiguration (flake.nix:596-610) does NOT receive constants in its extraSpecialArgs — only `horizon` and `user`. So embedded and independent Home already diverge: embedded Home has `constants`, independent Home does not.

**Survival**: Does not survive. The embedded/independent divergence is exactly what the psyche ruled against.

**Severity**: Blocks the psyche's stated design (OS evaluation leaks into embedded Home).

---

### F4. AgentIntercomGraphical still used as a gate

**What it is**: The `AgentIntercomGraphical` node service is still referenced as a gate in both CriomOS and CriomOS-home.

**Evidence**:
- `CriomOS/modules/nixos/agent-intercom.nix:11`: `graphicalEnabled = nodeServices.has ... "AgentIntercomGraphical";`
- `CriomOS/modules/nixos/users.nix:10-11,24`: same check, used for uinput group
- `CriomOS-home/modules/home/profiles/min/agent-intercom.nix:28`: `graphicalEnabled = hasCapability "AgentIntercomGraphical";`
- `CriomOS-home/flake.nix:456`: `agentIntercomGraphicalSupported = system: system == "x86_64-linux";`

**Psyche departure**: "AgentIntercomGraphical is a total misnomer and is now involved in a bunch of things it has nothing to do with" (psycheOsHomeGoldragon §AgentIntercomGraphical, 2026-08-28). "We don't need to gate agent intercom, it should be on any node that has Claude/codex" (same, L803). "Remove the x86 gate" (same, L845).

**Disconfirming evidence**: None. The psyche explicitly ruled the flag must be removed and decomposed. "Implement and merge on main then deploy ouranos and zeus" (L274) was the authorization.

**Survival**: Does not survive.

**Severity**: Blocks the psyche's stated design (three concepts conflated in one flag; x86 gate unjustified).

---

### F5. x86_64 gate for desktop apps

**What it is**: Desktop apps (Claude Desktop, ChatGPT/Codex Desktop) are gated on x86_64 architecture in CriomOS-home.

**Evidence**:
- `CriomOS-home/modules/home/profiles/min/agent-intercom.nix:36`: `graphicalSupported = homeSystem == "x86_64-linux";`
- `CriomOS-home/flake.nix:456`: `agentIntercomGraphicalSupported = system: system == "x86_64-linux";`
- Assertion at line 86-88: "graphical Agent Intercom requires x86_64-linux Desktop support"

**Psyche departure**: "Why is x86 a gate for the apps?" / "Remove the x86 gate" (psycheOsHomeGoldragon, 2026-08-28, L803, L845).

**Severity**: Blocks the psyche's stated design.

---

### F6. LAN subnet dual definition

**What it is**: The LAN subnet (10.18.0.0/24) and gateway (10.18.0.1) are defined in both CriomOS-lib and criomos-horizon-config.

**Evidence**:
- `CriomOS-lib/lib/default.nix:96-99`: `lan = { subnetPrefix = "10.18.0"; gateway = "10.18.0.1"; subnet = "10.18.0.0/24"; }`
- `criomos-horizon-config/horizon.dotos:8-10`: `[10.18.0.0/24]`, `[10.18.0.1]`, `(DhcpPool [10.18.0.100] [10.18.0.240])`

**Psyche departure**: "one source per shared thing" — implied by "abstract the common ground between OS and home to a separate repo, and using that repo as the source for anything that is shared between them" (psycheLojix §Common ground, 2026-08-24).

**Disconfirming evidence**: CriomOS-lib constants are consumed by modules at eval time (dnsmasq, headscale, nordvpn, wireguard, yggdrasil, wifi-eap, wifi-pki). The horizon.dotos values are consumed by horizon-rs at projection time. They serve different evaluation pipelines — but they must agree on the same values.

**Survival**: Does not survive. One source should feed both.

**Severity**: Duplicates a source.

---

### F7. home.stateVersion triple definition

**What it is**: `home.stateVersion = "26.05"` is set in three places.

**Evidence**:
- `CriomOS/modules/nixos/userHomes.nix:16`
- `CriomOS-home/flake.nix:605`
- (System stateVersion at `CriomOS/modules/nixos/normalize.nix:215` is separate: `system.stateVersion`)

**Psyche departure**: One source per shared thing.

**Disconfirming evidence**: Both are embedded in their respective evaluation contexts and must agree. A single source in criomos-core could export this.

**Severity**: Duplicates a source.

---

### F8. Hardcoded SSH matchBlock for prometheus

**What it is**: CriomOS-home hardcodes an SSH matchBlock for `prometheus.goldragon.criome`.

**Evidence**: `CriomOS-home/modules/home/profiles/min/default.nix:534-538`:
```nix
matchBlocks."prometheus.goldragon.criome prometheus" = {
  hostname = "prometheus.goldragon.criome";
  serverAliveInterval = 20;
  serverAliveCountMax = 3;
};
```

**Psyche departure**: "nothing in this should hardwire bird or zeus anywhere" (psycheLojix §Universal cluster fixes, 2026-08-09). "I don't want setup-specific scripts in general repos" (psycheOsHomeGoldragon §Setup-independent interfaces, 2026-08-14).

**Disconfirming evidence**: The comment says "Host-specific for now; could be derived from the cluster's NixBuilder node once a generic resolver exists." This acknowledges the violation and defers the fix.

**Survival**: Does not survive. The builder matchBlock should be derived from Horizon's builder configs.

**Severity**: Blocks the psyche's stated design (hardwired per host).

---

### F9. mirror.nix force-disabled dead module

**What it is**: `CriomOS/modules/nixos/mirror.nix:30`: `mirrorEnabled = false && mirrorEligible;` — the module is permanently disabled via a leading `false &&` but remains fully wired with its flake input.

**Evidence**: Lines 15-30. Comment explains: "The legacy standalone mirror-0.1.2 daemon crash-loops on a redb HeadFamily table type-signature mismatch."

**Psyche departure**: Spirit principle — "Do not preserve an older shape for compatibility's sake." The module exists solely to keep the re-enable path short.

**Disconfirming evidence**: The mirror flake input is used by persona-router tests and the module structure is part of the planned persistent-Spirit-mirror. Removing the module would also remove the flake input, breaking tests.

**Survival**: Partially survives — the input is needed, but the dead module body is compatibility machinery.

**Severity**: Adds unasked machinery.

---

### F10. CriomOS-home input sprawl (80 inputs, 48 non-flake)

**What it is**: CriomOS-home declares 80 flake inputs, of which 48 are non-flake source tarballs (npm packages, VSIX files, git sources).

**Evidence**: `CriomOS-home/flake.nix` inputs block — 80 `url =` lines. Includes ~20 individual npm tarballs for agent-intercom and pi-web-access, plus individual VSIX files for VS Code extensions.

**Psyche departure**: "I would rather keep the flake very minimal; an entry point" (psycheOsHomeGoldragon §Flake structure, 2026-08-19). "every concept should really have its repo" (psyche-raw/Vision/everyConceptShouldHaveItsRepo.md).

**Disconfirming evidence**: Non-flake inputs are how Nix pins source tarballs without vendoring. Each npm tarball is a pinned dependency of agent-intercom or pi; they can't be reduced without moving agent-intercom packaging to its own flake. The psyche's own ruling "an orca repo is smarter than cramming more stuff in the home repo" supports splitting these out.

**Survival**: Partially survives for individual packages, but the aggregate sprawl violates minimal-flake. Agent-intercom's npm inputs should live in an agent-intercom flake.

**Severity**: Adds unasked machinery.

---

### F11. Per-tool nixpkgs divergence

**What it is**: Three CriomOS-home inputs keep their own NixOS/nixpkgs pin instead of following the fork.

**Evidence**:
- `llm-agents`: deliberately keeps NixOS/nixpkgs (different pnpm attrs)
- `herdr` (v0.8.2): no follows
- `orca-ide`: no follows
- Total: 5 distinct nixpkgs revisions in the locked evaluation graph

**Psyche departure**: Implicit in one-source principle. But the psyche has not explicitly ruled on per-tool nixpkgs.

**Disconfirming evidence**: llm-agents deliberately keeps its own nixpkgs because it needs different pnpm attributes. This is a genuine technical requirement, not carelessness.

**Survival**: Partially survives for llm-agents. herdr and orca-ide should follow.

**Severity**: Cosmetic (herdr/orca-ide); necessary divergence (llm-agents).

---

### F12. Hardcoded "prometheus" in pi-models.nix

**What it is**: CriomOS-home `profiles/min/pi-models.nix:37` hardcodes `"prometheus"` as the LLM server node name.

**Evidence**: Line 37 (node name used to resolve the LLM API endpoint).

**Psyche departure**: Same as F8 — nothing hardwired per host.

**Additional hardcoded values in CriomOS-home:**
- `min/default.nix:101-113`: 11 hardcoded `/home/li/...` Codex project trust paths
- `browser-use.nix:71`: `goldragon.criome/local-llm-api-token` gopass path (cluster-specific)

**Severity**: Blocks the psyche's stated design (hardwired per host).

---

### F13. CriomOS-lib should be superseded by criomos-core

**What it is**: CriomOS-lib exists as a separate repository holding constants, helpers, and data files consumed by both CriomOS and CriomOS-home.

**Evidence**: CriomOS-lib/flake.nix exports `lib = { constants, importJSON, mkJsonMerge, fetchHfModel }`.

**Psyche departure**: "core is more accurate than lib, yes, so superseding is the right perspective" (psycheOsHomeGoldragon §Common ground, 2026-08-25). "Then find all the commonality between the OS and home repos, then make a proposal on moving the source of it all in a new criomos-core repo" (2026-08-24).

**Severity**: Blocks the psyche's stated design (criomos-core not yet created).

---

### F14. serviceName helper function tripled

**What it is**: The `serviceName` helper (extracts a service variant's string name from the Horizon services list) is independently defined in three CriomOS-home modules.

**Evidence**:
- `CriomOS-home/modules/home/profiles/min/agent-intercom.nix:7-16`
- `CriomOS-home/modules/home/profiles/min/spirit.nix:22-31`
- `CriomOS-home/modules/home/profiles/min/default.nix:33-42`
- Also independently in `CriomOS/modules/nixos/node-services.nix` (exported as a module)

The CriomOS OS side correctly extracted this into a shared `node-services.nix` module. The CriomOS-home side has three independent inline copies.

**Psyche departure**: "one source per shared thing, consumed directly" — three copies of the same function.

**Severity**: Duplicates a source. Should be a single helper in criomos-core or in CriomOS-home's own shared module.

---

### F15. element.nix orphan: system-level service in Home

**What it is**: `CriomOS-home/modules/home/profiles/med/element.nix` declares `systemd.services.nginx-element` with `wantedBy = [ "multi-user.target" ]` — a system-level service defined in a Home Manager repo.

**Evidence**: File exists at `modules/home/profiles/med/element.nix`. The module aggregate at `modules/home/default.nix:86` correctly does NOT import it (comment: "NOT importing ./profiles/med/element.nix here — that file declares systemd.services.nginx-element (system-level, not user). It belongs in a CriomOS NixOS module, not in this home-manager aggregate.").

**Psyche departure**: "every concept in its own repository" — a system-level service does not belong in the Home profile repo.

**Severity**: Cosmetic (file is orphaned, never imported). Should be removed or moved to CriomOS.

---

### F16. Legacy/transitional patterns in CriomOS-home

**What it is**: Several transitional or backward-compatibility patterns remain in Home modules.

**Evidence**:
- `pi-models.nix:76`: `compat = { supportsStore = false; supportsDeveloperRole = false; ... }` — compatibility block
- `spirit.nix:89-91`: `migrateObsoleteSpiritJudgeOverride` — removes stale systemd override drop-in
- `spirit.nix:152-164`: `Conflicts` list with 12 versioned `persona-spirit-daemon-v*` service names
- `min/default.nix` activation: `removeDeprecatedCodexCollab` — removes retired Codex V1 collab feature flag

**Psyche departure**: Spirit: "Backward compatibility is never a design variable."

**Severity**: Adds unasked machinery (transitional). Each is a migration step that should be removed once all nodes have passed through it.

---

### F17. Checks — what they prove and what they cost

CriomOS carries 25 checks; CriomOS-home carries 46; total 71.

**CriomOS checks by type:**

| Type | Count | Examples | Cost |
|---|---|---|---|
| Role/policy evaluation guards | 12 | nspawn-role-policy, nix-role-policy, mirror-role-policy, spirit-role-policy, persona-router-role-policy, resolver-role-policy, vm-testing-prometheus-policy, repository-receive-role-policy, bluetooth-resume-power, desktop-audio, metal-firmware, laptop-keyboard | Eval + build (nixosSystem eval + runCommand touch) |
| Config roundtrip (NOTA→rkyv) | 3 | lojix-daemon-config-roundtrip, criome-daemon-config-roundtrip, clavifaber-publication-request | Eval + build (runs the actual encoder binary) |
| Source-text assertions | 4 | legacy-chroma-runtime, devshell-repository-layout, router-wifi-horizon-policy, router-wifi-secret | Eval only (readFile + assert) |
| Transport/ownership witnesses | 2 | agent-intercom-transport, agent-intercom-command-ownership | Build (runs binaries in check derivation) |
| Activation equivalence | 1 | home-activation-equivalence | Eval + full Home build (builds both embedded and independent activation packages) |
| Pin/contract validation | 1 | lojix-ownership | Eval (compares lock file revisions) |
| Network/security | 2 | headscale-selfsigned-cert, wireguard-untrusted-proxy, image-exchange-keys-scoped-to-co-hosts | Eval + build |

**CriomOS-home checks by type:**

| Type | Count | Examples | Cost |
|---|---|---|---|
| Behavioral/contract tests | ~28 | agent-intercom, agent-intercom-local, codex-remote-control, orchestrate-service-path, message-service-path, spirit-deployment, aggregator-deployment, bird-home-isolation, noctalia-settings-composition, default-opener, ghostty-primary-selection, keyboard-layout-policy, codex-tui, yt-dlp | Eval + build (evaluates HM config or builds package) |
| Source-text assertions | ~11 | no-easyeffects, desktop-shell-launch, editor-heavy-autostart, emacs-rust-analyzer-autostart, home-profile-absence, vscodium-casual, system-projection-boundary, listener-level-widget, solar-time-widget, active-network-widget | Eval only (readFile + assert/grep) |
| Smoke tests (runs binary) | ~7 | gws, leta, playwright-cli, rust-toolchain, main-contract-pins, dolthub-create-database, ai-agent-launch-orchestration | Eval + build (runs binary) |

**Observation across both repos**: The source-text assertions (4 in CriomOS + ~11 in CriomOS-home = ~15 total) are change-detectors — they search source text with `hasInfix`/grep rather than testing behavior. Per the testing skill: "A test that searches or compares source text is a change-detector: it fails on any edit and catches no behavior — never write one."

CriomOS change-detectors: `legacy-chroma-runtime`, `devshell-repository-layout`, `router-wifi-horizon-policy`, `router-wifi-secret`.
CriomOS-home change-detectors: `no-easyeffects`, `desktop-shell-launch`, `editor-heavy-autostart`, `emacs-rust-analyzer-autostart`, `home-profile-absence`, `vscodium-casual`, `system-projection-boundary`.

**Cost**: Most checks are eval-time + a trivial `runCommand "... " {} 'touch "$out"'`. The expensive ones are: `home-activation-equivalence` (builds both embedded and independent Home activation packages), `agent-intercom-command-ownership` (builds agent-intercom + user profiles + runs binaries), `codex-remote-control-vm` (NixOS test VM), Claude Desktop checks (`claude-desktop-declared-cli`, `-egl-linkage`, `-launcher-linkage` — Electron patching + xvfb), and the roundtrip checks (build + run encoder binaries). The role-policy checks call `lib.nixosSystem` which is expensive to evaluate but produces only a `touch "$out"` derivation.

---

## 3. Disconfirming evidence

| Finding | Strongest countercase | Survives? |
|---|---|---|
| F1 (pkgs from Home) | Ensures identical activation packages for the equivalence check | No — the equivalence can be achieved by both consuming pkgs from a shared source (criomos-core/extended CriomOS-pkgs with Home overlays) |
| F2 (overlay force-clear) | With readOnlyPkgs, this is a defensive no-op preventing accidental overlay declarations | Partially — the guard is defensible, the comment is wrong |
| F3 (constants leak) | Standalone Home doesn't receive constants, so the divergence is already present and untested | No — this is the exact divergence the psyche ruled against |
| F4 (AgentIntercomGraphical) | None | No |
| F5 (x86 gate) | Some Electron apps may genuinely not build on aarch64 | No — the psyche ruled "each package's actual build support decides", not a blanket arch gate |
| F6 (LAN dual def) | Different evaluation pipelines (Nix vs Rust) | No — one source should feed both |
| F7 (stateVersion) | Each evaluation context sets it independently; they agree today | No — one source is better |
| F8 (prometheus matchBlock) | Comment acknowledges the violation and defers to a generic resolver | No — deferral is not justification |
| F9 (mirror dead module) | The flake input is needed by other tests | Partially — input stays, dead module body should be removed |
| F10 (input sprawl) | Non-flake inputs are the standard Nix mechanism for pinning sources | Partially — individual packages should own their deps in their own flakes |
| F11 (per-tool nixpkgs) | llm-agents has genuine pnpm attr requirements | Yes for llm-agents; No for herdr/orca-ide |
| F12 (prometheus in pi-models) | The LLM server genuinely runs on prometheus today | No — should come from Horizon |
| F13 (lib→core) | CriomOS-lib works today | No — psyche explicitly ruled superseding |
| F14 (serviceName tripled) | Each module needs the function in its own let binding | No — extract to a shared module |
| F15 (element.nix orphan) | Kept for reference | No — remove or move to CriomOS |
| F16 (legacy patterns) | Protect against stale state on old nodes | Temporarily — remove after all nodes migrate |
| F17 source-text checks | They guard against specific regressions cheaply | No — they catch edits, not behavior |

---

## 4. End-shape

The psyche's criteria: one source per shared thing, consumed directly; no indirection; embedded and independent Home identical, fed from Horizon only; the flake a minimal entry point; nothing hardwired per host; gates named for what they actually gate; no setup-specific scripts; every concept in its own repository.

### Repositories

| Repository | Holds |
|---|---|
| **criomos-core** (new, supersedes CriomOS-lib) | Shared constants, helpers, data. Single source for LAN addressing, filesystem paths, stateVersion. Exports namespaces consumed by both CriomOS and CriomOS-home. Home overlays (claude-desktop, yt-dlp) move here as overlay definitions exported alongside constants. |
| **CriomOS** | System modules only. Consumes pkgs from CriomOS-pkgs (which applies criomos-core overlays). Consumes criomos-core for constants. Thin Home embedding shim (userHomes.nix) passes only `horizon` and `pkgs` — no constants. |
| **CriomOS-home** | Home modules, profiles. Consumes criomos-core for constants and overlays. Minimal flake: concept-scoped packages (agent-intercom, pi, etc.) move to their own flakes. |
| **CriomOS-pkgs** | Instantiates nixpkgs + criomos-core overlays for the (nixpkgs-rev, system) tuple. Both OS and Home consume this single pkgs. |
| **criomos-horizon-config** | Authored horizon.dotos. Single source for all cluster topology, including LAN addressing (criomos-core derives from it or both derive from horizon-rs projection). |
| **agent-intercom** (new) | Agent Intercom packaging + its npm dependencies. Own flake. |

### Dependency diagram

```
                   horizon.dotos
                        │
                   horizon-rs (projects JSON)
                        │
                      lojix (materializes inputs)
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       system        horizon       secrets
          │             │
          ▼             │
    ┌──────────┐        │
    │CriomOS-  │        │
    │  pkgs    │◄──── criomos-core (overlays)
    └────┬─────┘        │
         │              │
    ┌────▼──────────────▼──────────────┐
    │              CriomOS             │
    │  system modules                  │
    │  thin Home embedding:            │
    │    extraSpecialArgs = {          │
    │      horizon; pkgs;              │  ◄── no constants
    │    };                            │
    │  sharedModules = [home.default]  │
    └──────────────┬───────────────────┘
                   │ follows
    ┌──────────────▼───────────────────┐
    │           CriomOS-home           │
    │  home modules + profiles         │
    │  consumes: horizon, pkgs,        │
    │    criomos-core (constants)      │
    │  gates: Edge + cumulative Medium │
    │    for desktop; Claude/Codex     │
    │    presence for AgentIntercom    │
    └──────────────────────────────────┘
```

### Gate decomposition (replacing AgentIntercomGraphical)

- **Desktop apps** (Claude Desktop, ChatGPT, Codex Desktop): gated on `behavesAs.edge && user.size.medium` — the Edge node concept plus cumulative Medium. No architecture gate.
- **AgentIntercom** (coi, cci, MCP servers): present wherever Claude/Codex CLI packages are present. No separate gate.
- **Graphical prerequisites** (at-spi2-core, uinput, portal screencast): gated on `behavesAs.edge`. Already done in edge/default.nix — merge agent-intercom.nix graphical block into edge.

### Migration — vertical slices

Each slice leaves the system deployable.

**Slice 1**: Remove AgentIntercomGraphical and x86 gates.
- CriomOS: `agent-intercom.nix` — replace `graphicalEnabled` with `behavesAs.edge`; remove `graphicalEnabled` from `users.nix`
- CriomOS-home: `agent-intercom.nix` — replace `graphicalEnabled` with `behavesAs.edge && mediumEnabled`; remove `graphicalSupported` x86 check
- Deploy Ouranos and Zeus

**Slice 2**: Remove hardcoded host references.
- CriomOS-home: derive SSH matchBlocks from Horizon builder configs
- CriomOS-home: derive pi-models LLM endpoint from Horizon
- Deploy

**Slice 3**: Create criomos-core.
- Move CriomOS-lib contents to criomos-core
- Move Home overlays (claude-desktop, yt-dlp) to criomos-core
- Both CriomOS and CriomOS-home switch from criomos-lib to criomos-core
- CriomOS-pkgs applies criomos-core overlays
- Deploy

**Slice 4**: Fix Home embedding.
- CriomOS/userHomes.nix: remove `constants` from extraSpecialArgs
- CriomOS-home modules: receive constants from criomos-core directly (via its own input), not from OS specialArgs
- CriomOS/flake.nix: get pkgs from CriomOS-pkgs directly, not extracted from Home
- Verify home-activation-equivalence still passes
- Deploy

**Slice 5**: Reduce Home input sprawl.
- Move agent-intercom packaging to its own flake (with its npm deps)
- Move pi packaging to its own flake
- CriomOS-home consumes them as single flake inputs
- Deploy

**Slice 6**: Remove source-text change-detector checks.
- Replace `legacy-chroma-runtime`, `devshell-repository-layout`, `router-wifi-horizon-policy`, `router-wifi-secret` with behavioral equivalents or remove (they guard things that other checks already cover or that are structurally impossible)
- Deploy

**Slice 7**: Clean dead module.
- Remove mirror.nix module body (keep flake input)
- Deploy

---

## 5. Unknowns

1. **Whether criomos-core and extended-horizon are the same repository.** The psyche named both concepts; their convergence is unresolved (psycheOsHomeGoldragon §Tensions, point 1).

2. **Whether llm-agents' nixpkgs divergence is still necessary.** The pnpm attribute requirement may have been resolved in newer nixpkgs.

3. **Whether herdr and orca-ide would break under the fork's nixpkgs.** Not tested.

4. **The exact horizon-rs projection schema.** Which fields it emits for builder configs, LLM endpoints, and SSH matchBlock data — needed for Slices 2 and 4.

5. **Whether Home's `constants` are consumed anywhere in the independent (standalone) evaluation path.** If not, the embedded-receives-constants divergence is currently masked, not tested.

6. **What Zeus's empty services list `[]` means.** Zeus is defined as Edge/Max/Max with no services. Whether this is the intended shape or an omission is unresolved.

---

## Sources

### Code (current main as of 2026-08-28)
- `CriomOS/flake.nix` — flake structure, pkgs extraction (line 160), target evaluation
- `CriomOS/modules/nixos/normalize.nix` — overlay clearing (line 174), size/species gates
- `CriomOS/modules/nixos/userHomes.nix` — embedded Home wiring, constants leak (line 44)
- `CriomOS/modules/nixos/agent-intercom.nix` — AgentIntercomGraphical gate (line 11)
- `CriomOS/modules/nixos/users.nix` — AgentIntercomGraphical in uinput (lines 10-11, 24)
- `CriomOS/modules/nixos/mirror.nix` — force-disabled dead module (line 30)
- `CriomOS/modules/nixos/node-services.nix` — service name extraction helper
- `CriomOS/gates/agent-intercom-command-ownership.nix` — ownership check
- `CriomOS/home-activation-equivalence.nix` — equivalence check
- `CriomOS/stubs/` — no-system, no-horizon, no-secrets, default-deployment
- `CriomOS/checks/` — 25 checks (4 source-text, 12 role-policy, 3 roundtrip, etc.)
- `CriomOS-home/flake.nix` — 80 inputs, homeConfigurations, agentIntercomGraphicalSupported
- `CriomOS-home/modules/home/profiles/min/agent-intercom.nix` — AgentIntercomGraphical (line 28), x86 gate (line 36)
- `CriomOS-home/modules/home/profiles/min/default.nix` — prometheus matchBlock (line 534)
- `CriomOS-home/modules/home/profiles/min/pi-models.nix` — hardcoded prometheus (line 37)
- `CriomOS-lib/lib/default.nix` — LAN constants (lines 96-99)
- `CriomOS-pkgs/flake.nix` — pkgs instantiation with overlays
- `criomos-horizon-config/horizon.dotos` — LAN addressing (lines 8-10)

### Psyche records (quoted from flow 674a4dab reports)
- `flows/674a4dab/reports/psycheOsHomeGoldragon.md` — Home equivalence, common ground, AgentIntercomGraphical decomposition, setup-independent interfaces, universal fixes, flake minimality
- `flows/674a4dab/reports/psycheLojix.md` — embedded/independent Home equivalence, common ground, simplicity, universal cluster fixes, setup-independent interfaces
- `flows/674a4dab/witnesses/nixSideMap.md` — flake-input graph, dual definitions, size table
