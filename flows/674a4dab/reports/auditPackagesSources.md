# Audit: the package / source-of-truth plane

Evidence base: CriomOS origin/main `45e83fb`, CriomOS-home origin/main
`ed6832c`, CriomOS-pkgs `c64ea0e`, CriomOS-lib `6e3bcb0`, all fetched
from GitHub via `nix flake metadata github:LiGoldragon/...`. Lock files
at those commits. Store-path measurements where realized.

The nixSideMap witness was written against detached local HEADs (CriomOS
`21af0c3`, CriomOS-home `4e36d44`). Between those and origin/main:
llm-agents was removed, `owned-agents/` directory created,
`criomos.corePackages` options added, claude-desktop overlay removed,
AgentIntercomGraphical decomposition landed. This audit reflects
origin/main throughout.

---

## 1. The plane as it is

### Tool/package table

| Tool | Source pin | Derivation location | nixpkgs | Consumers | TUI/Desktop/Ext share derivation? |
|------|-----------|---------------------|---------|-----------|-----------------------------------|
| Claude Code CLI | GCS binary via `hashes.json` (v2.1.250) | `owned-agents/claude-code/` | Fork `0e251e24` | cli-tools, agent-intercom, pi-models, claude-remote-control | Yes: all via `config.criomos.corePackages.claude` |
| Claude Code VSIX | Marketplace VSIX input (v2.1.250) | flake.nix `claude-code-vsix` | Fork | vscodium module | Native binary replaced with `corePackages.claude` |
| Claude Desktop | Anthropic `.deb` via `hashes.json` (v1.37937.3) | `owned-agents/claude-desktop/` | Fork | `desktopEnabled` gate | Patches asar to use `corePackages.claude` |
| Codex CLI | `fetchFromGitHub` openai/codex `rust-v0.150.1` | `owned-agents/codex/` | Fork | agent-intercom, pi-models | Yes: all via `config.criomos.corePackages.codex` |
| Codex TUI | Shell wrapper around CLI | `owned-agents/codex/tui.nix` | Fork | remote-control service | Same binary as CLI |
| Codex/ChatGPT VSIX | Marketplace VSIX input (v26.5825.32147) | flake.nix `codex-chatgpt-vsix` | Fork | vscodium module | Different codebase (JS sidebar, not Rust CLI) |
| ChatGPT Desktop | OpenAI `.deb` via `hashes.json` (v26.825.31414) | `owned-agents/chatgpt/` | Fork | `desktopEnabled` gate | Links `codexDesktopGate` (wraps `corePackages.codex`) |
| Pi | `pi-src` non-flake input (earendil-works/pi v0.84.1) | `packages/pi/` | Fork | cli-tools (medium) | N/A |
| Agent Intercom | 6 non-flake git inputs + ~20 npm tarballs | `packages/agent-intercom/` | Fork | min profile (always on) | N/A |
| Mentci | `mentci-src` non-flake input | `packages/mentci/` | Fork | profiles | N/A |
| Browser-use | `uv.lock` in `packages/browser-use/` | `packages/browser-use/` | Fork | max/large tier | N/A |
| Herdr | `herdr` flake input (tag v0.8.2) | herdr's own flake | **herdr's NixOS/nixpkgs** `f83fc3c3` | agent harness | Own nixpkgs, not followed |
| Orca | `orca-ide` flake input (commit pin) | orca's own flake | **orca's NixOS/nixpkgs** `e7a3ca80` | agent harness | Own nixpkgs, not followed |
| VSCodium | nixpkgs | `profiles/med/codium.nix` + `vscodium/vscodium/` | Fork | medium users | N/A |
| Emacs | nixpkgs | `profiles/med/emacs.nix` | Fork | medium users | N/A |
| Spirit | `spirit` flake input (commit pin) | spirit's own flake | Fork (via follows) | PersonaDevelopment service | N/A |
| Orchestrate | `orchestrate` flake input (commit pin) | orchestrate's own flake | Fork (via follows) | OS + Home | N/A |
| Niri | `niri-flake` input | niri-flake's own flake | Fork (primary follows), **NixOS stable** `b6018f87` (nixpkgs-stable) | edge desktop | N/A |
| yt-dlp | `yt-dlp-src` non-flake input | `overlays/yt-dlp.nix` | Fork | mpv and direct | N/A |

### nixpkgs revisions in the deploy closure (4 distinct)

| Rev prefix | Owner | Date | Brought by | Followed? |
|-----------|-------|------|-----------|-----------|
| `0e251e24a4f2` | LiGoldragon (fork) | 2026-08-13 | Root nixpkgs. All follows chain here. | Primary |
| `f83fc3c307e7` | NixOS | 2026-05-21 | herdr (no follows) | **No** -- 3 months stale |
| `e7a3ca8092b6` | NixOS | 2026-07-11 | orca-ide (no follows) | **No** -- 7 weeks stale |
| `b6018f87da91` | NixOS | 2026-06-30 | niri-flake nixpkgs-stable (stable branch) | **No** -- stable branch |

### Measured closure duplication

Three distinct glibc store paths coexist in the system closure:

| Store path | Version | Size | Source |
|-----------|---------|------|--------|
| `0d8g8n0a-glibc-2.42-67` | 2.42-67 | 37.7 MB | Fork `0e251e24` |
| `57iz3655-glibc-2.42-61` | 2.42-61 | 37.7 MB | herdr `f83fc3c3` |
| `ias8xacs-glibc-2.42-67` | 2.42-67 | 37.7 MB | orca `e7a3ca80` |

Orca's glibc is the same version as the fork's but a different store
path (different nixpkgs evaluation, different input hash). This pattern
repeats across every transitive dependency (openssl, zlib, bash, etc.),
multiplying the cost. Conservative estimate: each extra nixpkgs adds
200--500 MB of duplicate closure.

---

## 2. Findings

### 2.1 Four nixpkgs revisions: herdr and orca bring unfollowed copies

**Evidence.** CriomOS-home `flake.lock` at `ed6832c`: 4 distinct
nixpkgs nodes. herdr (v0.8.2 tag) brings `f83fc3c3` (May 2026, 3
months behind the root pin). orca-ide (commit pin) brings `e7a3ca80`
(Jul 2026, 7 weeks behind). niri-flake brings `b6018f87` on the stable
branch. None are followed.

Store evidence: glibc duplicated three ways (see table above). Each
extra nixpkgs costs hundreds of MB in closure, adds eval time (each
must be imported separately), and introduces version skew (herdr's
glibc is patch level 61 while the root's is 67).

**Psyche departure.** "show me how criomos-core works, and how you deal
with nixpkgs across all the repos" (01a0437d:4200). The unanswered
question remains open. The follows chain covers most inputs, but herdr
and orca break it.

**Severity.** Blocks a stated design.

**Disconfirming evidence.** herdr and orca are third-party flakes. Their
maintainers did not set up `follows` inputs. The CriomOS-home consumer
*could* add `herdr.inputs.nixpkgs.follows = "nixpkgs"` and
`orca-ide.inputs.nixpkgs.follows = "nixpkgs"` -- this is standard Nix
practice, costs one line per input, and does not require upstream
cooperation. For niri-flake, the primary nixpkgs already follows; only
`nixpkgs-stable` is independent, and this is structural to how
niri-flake tracks stable NixOS. **The disconfirming case does not
survive for herdr or orca; it partially survives for niri-flake's stable
pin.**

---

### 2.2 LiGoldragon/nixpkgs fork: zero local commits

**Evidence.** GitHub API: fork is 0 commits ahead of NixOS/nixpkgs.
HEAD `0e251e24` exists verbatim in NixOS/nixpkgs. All patches live in
CriomOS-pkgs overlays, not in the fork.

**Psyche departure.** None explicit -- the fork was never discussed. But
the fork is an indirection: `github:LiGoldragon/nixpkgs?ref=main`
rather than `github:NixOS/nixpkgs?rev=0e251e24...`. The living ruled
"indirection is bad design" (01a030a1:605).

**Severity.** Adds unasked machinery. The fork provides namespace
stability (the URL stays constant regardless of upstream
reorganization), which is a marginal benefit.

**Disconfirming evidence.** A fork allows future patches without
changing the URL in every consumer's flake.nix. The nix-input-upgrade
skill notes "A nixpkgs fork with no local commits can be
fast-forwarded via the GitHub API without cloning." The fork makes the
lunar update trivial: fast-forward the fork, `nix flake update nixpkgs`
everywhere, done. **This case is weak but not empty** -- the
convenience is real, the indirection cost is small.

---

### 2.3 CriomOS-pkgs: a separate repository for 4 overlays

**Evidence.** CriomOS-pkgs `c64ea0e`: 2 Nix files, 73 lines. Contains
4 overlays: nix-vscode-extensions, openldap doCheck=false,
spamassassin doCheck=false, gtk4 DMA-buffer fetchpatch. Its purpose is
an eval-cache boundary: `import nixpkgs { ... }` is keyed on
`(nixpkgs.narHash, system.narHash, overlays)`, so it caches across
CriomOS source edits.

**Psyche departure.** "every concept should really have its repo"
(98fbfa47). The question is whether "the overlaid nixpkgs set" is a
concept. The living never discussed CriomOS-pkgs directly; an agent
said "CriomOS-pkgs remains the general package universe" (01a0437d:4298)
and the living did not object.

**Severity.** Cosmetic. The eval-cache benefit is real and documented.
4 overlays in 73 lines is not "cramming" -- it is appropriately minimal.

**Disconfirming evidence.** The eval-cache boundary is a proven Nix
pattern. If overlays move to criomos-core, the eval-cache must be
rebuilt on every criomos-core change, defeating the purpose. **The
disconfirming case survives.** CriomOS-pkgs is correctly separated.

---

### 2.4 nix-vscode-extensions overlay applied twice

**Evidence.** CriomOS-pkgs `flake.nix` applies
`nix-vscode-extensions.overlays.default`. CriomOS-home `flake.nix:443`
applies it again in `packageOverlays`. CriomOS-home's `pkgs` is built
by extending CriomOS-pkgs's already-overlaid `pkgs` with
`composeManyExtensions packageOverlays`.

**Psyche departure.** "declared once, used everywhere" (01a038be:436).
Applying the same overlay twice is the opposite: defined twice, applied
twice.

**Severity.** Duplicates a source. The second application is redundant
-- nix-vscode-extensions is already in the `pkgs` set from CriomOS-pkgs.
The practical cost is small (overlays are idempotent for attribute
addition), but it signals a misunderstanding of the layering.

**Disconfirming evidence.** CriomOS-home must also work standalone
(not consumed by CriomOS). In standalone mode, `pkgs` might not come
from CriomOS-pkgs. If CriomOS-home's `packageOverlays` must be
self-sufficient for standalone operation, the duplication is
defensive. **This case partially survives** if standalone Home is
still a supported configuration; it does not survive if all Home
evaluation goes through CriomOS.

---

### 2.5 CriomOS-lib: constants that belong in Horizon

**Evidence.** CriomOS-lib `lib/default.nix`:
`constants.network.lan = { subnetPrefix = "10.18.0"; gateway = "10.18.0.1"; subnet = "10.18.0.0/24" }`.
This is also defined in `criomos-horizon-config/horizon.dotos`. The
nixSideMap witness flags this as a **DUAL DEFINITION**.

`constants.network.yggdrasil`, `constants.network.headscale`,
`constants.fileSystem.*`, `constants.network.nix.*` are architecture-
level constants shared between OS and Home -- genuine library material.

`fetchHfModel`, `importJSON`, `mkJsonMerge` are pure utility functions.
`mkJsonMerge` is reportedly deprecated for hexis.

**Psyche departure.** "core supersedes lib" (01a030e8:540). CriomOS-lib
still exists and is consumed. The living deferred criomos-core ("right
now") but did not retract the design. LAN config duplicating Horizon
departs from "whatever in home is currently originating in the OS must
originate from the horizon" (01a02b4b:905).

**Severity.** Blocks a stated design (dual definition of cluster
topology). The lib-to-core migration is deferred, not cancelled.

**Disconfirming evidence.** CriomOS-lib is a pure flake with no inputs.
Moving its contents to criomos-core requires criomos-core to exist
first. The living explicitly deferred criomos-core. Until then,
CriomOS-lib is the working carrier. **The case survives as a deferral,
not as a permanent shape.** The LAN dual definition has no defense.

---

### 2.6 VSIX version strings require manual lockstep

**Evidence.** Claude Code VSIX is pinned at version 2.1.250 in the
flake input URL (`...anthropic.claude-code/2.1.250/vspackage`). The
CLI is pinned at 2.1.250 in `hashes.json`. These are independent
sources. No automation ensures they stay aligned.

Similarly, Codex VSIX (26.5825.32147) is pinned in the URL; the
Codex CLI (0.150.1) is in `hashes.json`. These are intentionally
different (different codebases), but the VSIX version must still track
its upstream.

**Psyche departure.** "we should have a way that ensures the tui and
desktop versions line up" (01a0338f:369). The `corePackages` option
ensures the CLI binary is shared, but the VSIX's JS/extension code
version is a separate concern that could diverge.

For Claude Code: the postInstall step replaces the native binary, so
version skew between VSIX JS shell and CLI binary is cosmetic. For
Codex VSIX: it is a different product entirely (ChatGPT sidebar) and
version alignment is not meaningful.

**Severity.** Cosmetic for Claude Code (binary is forced). Not
applicable for Codex (different codebase).

**Disconfirming evidence.** The `update.py` scripts and `updater`
passthru metadata exist for each owned-agent package, enabling
automation. The gap is that VSIX input URLs in `flake.nix` are not
covered by these updaters. **Automation would close this; the
architecture is not wrong, the tooling is incomplete.**

---

### 2.7 Two Rust toolchain providers: rust-build vs direct crane+fenix

**Evidence.** `rust-build` (LiGoldragon/rust-build): wraps crane+fenix
with cargo-artifact normalization. Used by spirit, orchestrate,
clavifaber, curriculum-deploy. Direct crane+fenix: used by agent,
aggregator, message, listener. Both ultimately use crane+fenix; the
difference is rust-build's normalization layer and unified API.

Rust repos consumed as flake inputs (spirit, orchestrate, agent, etc.)
all follow the consumer's nixpkgs. Their toolchain pins (fenix nightly)
come from their own locks or via rust-build's lock. Multiple
rust-build revisions appear in the lock (3 distinct), and multiple
crane revisions (7 distinct).

**Psyche departure.** Not directly addressed by the psyche.

**Severity.** Duplicates a source. Two ways to do the same thing. The
normalization rust-build provides is genuine engineering, but the
crane+fenix repos do not benefit from it.

**Disconfirming evidence.** The crane+fenix repos (agent, aggregator,
message, listener) predate rust-build. Migrating them to rust-build
requires updating each repo's flake.nix and verifying reproducibility.
This is straightforward but costs migration effort. **The case does not
survive as a permanent design -- all Rust repos should converge on one
toolchain provider.**

---

### 2.8 ~48 non-flake inputs: appropriate single-source pinning

**Evidence.** CriomOS-home `flake.nix` at `ed6832c` has 48 non-flake
inputs: 3 VSIX files, 1 yt-dlp git source, 1 Go source (annas-mcp),
1 Rust source (mentci), 6 Agent Intercom component repos, ~33 npm
tarballs for Agent Intercom and Pi web-access dependency trees.

Each non-flake input is the single source for its component. The npm
tarballs are the vendored dependency closure -- each is a content-
addressed registry tarball with a hash.

**Psyche departure.** None. This is correct single-source pinning. The
flake.nix is large because the inputs are numerous, but each is
necessary and pinned.

**Severity.** None. Observation only.

**Disconfirming evidence.** N/A.

---

### 2.9 CriomOS gets pkgs from Home, not from CriomOS-pkgs directly

**Evidence.** CriomOS `flake.nix`:
```
(builtins.head (builtins.attrValues inputs.criomos-home.homeConfigurations)).pkgs
```
CriomOS-home's overlay composition (including the yt-dlp overlay and
the redundant nix-vscode-extensions overlay) is the authority for the
OS's package set.

**Psyche departure.** Not directly addressed.

**Severity.** Cosmetic. This creates a dependency from OS evaluation on
Home's homeConfigurations output, which is correct for ensuring both
share the same `pkgs` set.

**Disconfirming evidence.** This is the mechanism that ensures OS and
Home share one `pkgs` set. Without it, they would import nixpkgs
separately. **The case survives.**

---

### 2.10 _module.args.inputs = lib.mkForce inputs

**Evidence.** CriomOS-home `flake.nix:757`:
```nix
_module.args.inputs = lib.mkForce inputs;
```
This forces every Home module to see CriomOS-home's own flake inputs
rather than whatever CriomOS passes via `extraSpecialArgs`.

**Psyche departure.** "indirection is bad design" (01a030a1:605). The
`mkForce` is a blunt instrument that severs the connection between the
consumer's input namespace and the module's view. However, it serves
the equivalence principle: embedded and standalone Home see the same
inputs.

**Severity.** Cosmetic. The mechanism works as intended for the
standalone/embedded equivalence goal.

**Disconfirming evidence.** Without `mkForce`, embedded Home modules
would see CriomOS's inputs (which include different repos and follows
chains), breaking standalone equivalence. The living ruled "no
difference between embedded and independent home" (01a02b4b:880).
**This mechanism directly serves that ruling. The case survives.**

---

### 2.11 criomos.corePackages: the realized interim step works

**Evidence.** `modules/home/core-packages.nix` declares
`criomos.corePackages.codex` and `criomos.corePackages.claude` as Home
Manager options with defaults pointing to `owned-agents/codex/` and
`owned-agents/claude-code/`. All consuming modules read from
`config.criomos.corePackages.*`.

Claude Desktop's asar is patched to use `corePackages.claude`.
ChatGPT Desktop links `codexDesktopGate` wrapping `corePackages.codex`.
VSCodium's Claude Code extension replaces its native binary with
`corePackages.claude`.

**Psyche departure.** This IS the psyche-directed design: "Let's just
create an option in criomos-home to define the codex and claude core
packages, and reuse that definition wherever the package is needed,
from the realized (config) side" (01a0437d:4304).

**Severity.** None. This fulfills the interim step.

**Disconfirming evidence.** N/A. The implementation matches the ruling.

---

### 2.12 Stateful installation: none found

**Evidence.** All software installation is declarative via Nix. Claude
Desktop is patched to use the declared Claude Code binary, preventing
it from downloading its own. No flatpak, snap, or GNOME Software
references found. The `patch-runtime.mjs` script in
`owned-agents/claude-desktop/` rewrites the app's asar to point at
the Nix-declared `claude` binary.

**Psyche departure.** None. Fulfills "we dont allow installing software
statefully" (01a038be:1034) and "force it to use our Claude code"
(01a03e02:~140).

**Severity.** None.

---

## 3. Disconfirming evidence summary

| Finding | Strongest counter-argument | Survives? |
|---------|---------------------------|-----------|
| 2.1 Four nixpkgs | herdr/orca are third-party; adding follows is one line each | **No** for herdr/orca. Partially for niri stable. |
| 2.2 Fork with 0 commits | Fork enables trivial lunar update via fast-forward | **Weak but nonzero** |
| 2.3 CriomOS-pkgs separation | Eval-cache boundary is proven and working | **Yes** |
| 2.4 Double nix-vscode-extensions | Standalone Home needs self-sufficient overlays | **Partial** (if standalone is supported) |
| 2.5 CriomOS-lib LAN constants | criomos-core deferred, lib is working carrier | **Yes** as deferral; LAN dual def has no defense |
| 2.6 VSIX manual lockstep | Updater automation exists, gap is tooling not architecture | **Yes** (architecture correct) |
| 2.7 Two Rust toolchains | Historical; migration is straightforward | **No** as permanent design |
| 2.9 OS gets pkgs from Home | Ensures shared pkgs set | **Yes** |
| 2.10 mkForce inputs | Serves embedded/standalone equivalence ruling | **Yes** |

---

## 4. End-shape

The package plane than which none better is possible for this psyche:

```
                    horizon.dotos
                         |
                    horizon-rs (standalone Rust CLI)
                         |
                      lojix (standalone Rust daemon)
                         |
                         | (override-input at deploy time)
                         v
    ┌─────────────────────────────────────────────────────────────┐
    │                    NixOS/nixpkgs                            │
    │              (pinned rev, lunar cadence)                    │
    │           No fork. Direct github:NixOS/nixpkgs.            │
    └────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    v                 v
    ┌──────────────────────┐  ┌──────────────────────────────────┐
    │   criomos-pkgs       │  │         criomos-core             │
    │   (eval-cache)       │  │  Supersedes CriomOS-lib.         │
    │                      │  │  Exports:                        │
    │  import nixpkgs {    │  │   constants (no LAN -- from      │
    │    overlays = [      │  │     Horizon only)                 │
    │      vscode-ext,     │  │   utilities (fetchHfModel,       │
    │      openldap,       │  │     importJSON)                  │
    │      spamassassin,   │  │   corePackages.claude (owned)    │
    │      gtk4-patch      │  │   corePackages.codex  (owned)    │
    │    ];                │  │   corePackages.claude-desktop     │
    │  }                   │  │   corePackages.chatgpt           │
    │                      │  │   llm.json (model catalog)       │
    │  nixpkgs follows     │  │                                  │
    │  consumer            │  │  nixpkgs follows consumer        │
    └──────────┬───────────┘  └──────────┬───────────────────────┘
               │                         │
               │    ┌────────────────────┘
               │    │
               v    v
    ┌──────────────────────────────────────────────────────────────┐
    │                      CriomOS-home                           │
    │                                                             │
    │  inputs: nixpkgs, criomos-pkgs, criomos-core,              │
    │    home-manager, niri-flake, stylix, herdr, orca,          │
    │    spirit, orchestrate, agent, ...                          │
    │                                                             │
    │  ALL .nixpkgs follow → nixpkgs (including herdr, orca)     │
    │  niri-flake.nixpkgs-stable: sole exception (stable branch) │
    │                                                             │
    │  config.criomos.corePackages.* from criomos-core            │
    │  owned-agents/ expressions stay here (build wiring)         │
    │  but package identity (version, source) from criomos-core   │
    │                                                             │
    │  homeModules.default: _module.args.inputs = mkForce inputs  │
    │  (embedded/standalone equivalence preserved)                │
    │                                                             │
    │  All Rust tool inputs follow consumer's nixpkgs             │
    │  All Rust tools use rust-build (single toolchain provider)  │
    └───────────────────────────┬──────────────────────────────────┘
                                │
                                │ follows: nixpkgs, home-manager,
                                │   criomos-core, criomos-pkgs,
                                │   spirit, orchestrate, ...
                                v
    ┌──────────────────────────────────────────────────────────────┐
    │                        CriomOS                              │
    │                                                             │
    │  inputs: nixpkgs, criomos-home, criomos-pkgs,              │
    │    criomos-core, home-manager, rust-build,                  │
    │    spirit, orchestrate, lojix, ...                          │
    │                                                             │
    │  ALL .nixpkgs follow → nixpkgs                              │
    │  pkgs from criomos-pkgs (directly, not via Home eval)       │
    │  Home overlays (yt-dlp) applied at Home level only          │
    │                                                             │
    │  system, horizon, secrets, deployment: stubs overridden     │
    │    by lojix at deploy time                                  │
    └──────────────────────────────────────────────────────────────┘
```

### Changes from current state to end-shape

| Change | What moves | Migration |
|--------|-----------|-----------|
| Follow herdr's nixpkgs | Add `herdr.inputs.nixpkgs.follows = "nixpkgs"` in CriomOS-home flake.nix | One line. Eval-test herdr builds against fork nixpkgs. |
| Follow orca's nixpkgs | Add `orca-ide.inputs.nixpkgs.follows = "nixpkgs"` in CriomOS-home flake.nix | One line. Eval-test orca builds against fork nixpkgs. |
| Remove nix-vscode-extensions double-apply | Remove from CriomOS-home `packageOverlays` (it is already in CriomOS-pkgs) | One line deletion. Verify standalone Home still has extensions (if standalone is supported, move the overlay to the standalone path only). |
| Create criomos-core | New repository. Move from CriomOS-lib: constants (minus LAN -- that comes from Horizon), fetchHfModel, importJSON, llm.json. Move from CriomOS-home owned-agents/: the `hashes.json` + version identity for claude-code, codex, claude-desktop, chatgpt. CriomOS-home keeps the build expressions (they need pkgs), criomos-core owns version/source identity. | Multi-step. Bottom-up: create criomos-core, push, update CriomOS-home to consume it, push, update CriomOS follows. |
| Retire CriomOS-lib | After criomos-core absorbs its contents. All consumers update `criomos-lib` → `criomos-core`. | After criomos-core is stable. |
| Remove LAN dual definition | LAN config comes from Horizon only. Remove `constants.network.lan` from CriomOS-lib/criomos-core. | Requires tracing all consumers of `constants.network.lan` and routing them through Horizon data. |
| Converge Rust toolchains | Migrate agent, aggregator, message, listener from direct crane+fenix to rust-build. | Per-repo: replace `inputs.crane` + `inputs.fenix` with `inputs.rust-build`, update flake.nix build expressions to use `rust-build.lib.${system}.fromPkgs`. |
| Eliminate fork (optional) | Replace `github:LiGoldragon/nixpkgs?ref=main` with `github:NixOS/nixpkgs?rev=<commit>` everywhere. Lunar update changes the rev in one place (criomos-pkgs), consumers follow. | Low priority. The fork's marginal convenience may not be worth removing. |

### Vertical-slice migration order

1. **herdr/orca follows** (immediate, no compatibility path, eliminates 2 nixpkgs revisions and ~400 MB closure duplication)
2. **Remove double vscode-extensions overlay** (immediate)
3. **Create criomos-core** with constants + utilities from CriomOS-lib (deferred per psyche ruling; do when the living authorizes)
4. **Move version identity** for claude/codex to criomos-core (concurrent with 3)
5. **Converge Rust toolchains** on rust-build (independent of 1--4)
6. **Eliminate LAN dual definition** (requires Horizon schema work, concurrent with 3)
7. **Retire CriomOS-lib** (after 3 and 6)

No compatibility paths. Each step replaces the old shape in every
consumer.

---

## 5. Unknowns

1. **Whether standalone Home (not embedded in CriomOS) is still a
   supported configuration.** This affects whether the double
   vscode-extensions overlay and the `packageOverlays` self-sufficiency
   are necessary.

2. **Whether herdr and orca build cleanly against the fork nixpkgs.**
   Adding follows is trivial, but herdr pinned to May nixpkgs and may
   depend on package versions that changed in the Aug pin. Eval-testing
   is required.

3. **What data niri-flake's nixpkgs-stable actually contributes to the
   closure.** It may be used only for niri's own build or it may leak
   into the Home closure.

4. **The exact closure size overhead per extra nixpkgs.** Glibc alone
   is ~37.7 MB per copy; the full transitive duplication across all
   shared libraries was not measured.

5. **Whether criomos-core should also carry the build expressions
   (the default.nix files in owned-agents/) or only the version
   identity (hashes.json, source URLs).** The living's "one central
   location where the derivation is defined" (01a0437d:486) suggests
   the full derivation, but the derivations need `pkgs` which comes
   from the consumer.

6. **Whether the impure tools in CriomOS-lib's tools/ directory
   (using `import <nixpkgs>`) are still used.** They are not consumed
   by the build, but their presence violates the flake purity model.

7. **The niri-flake and stylix option surfaces** and their interaction
   with CriomOS-home modules -- whether they bring runtime dependencies
   from the stable nixpkgs into the Home closure.

---

## Sources

| Source | Commit / Rev | What was read |
|--------|-------------|---------------|
| CriomOS origin/main | `45e83fb` | flake.nix, flake.lock (247 nodes), modules/nixos/agent-intercom.nix |
| CriomOS-home origin/main | `ed6832c` | flake.nix (74 inputs), flake.lock (202 nodes), owned-agents/\*, packages/\*, overlays/\*, modules/home/core-packages.nix, vscodium/, lib/owned-agent-packages.nix |
| CriomOS-pkgs | `c64ea0e` | flake.nix, flake.lock, stubs/ (entire repo, 5 files) |
| CriomOS-lib | `6e3bcb0` | flake.nix, lib/\*, data/largeAI/llm.json, tools/ (entire repo, 13 files) |
| LiGoldragon/nixpkgs | `0e251e24` | GitHub API compare (0 ahead, ~9080 behind NixOS/nixpkgs) |
| numtide/llm-agents.nix | (removed from Home) | flake.nix, flake.lock, packages/ (confirmed removal) |
| LiGoldragon/rust-build | `56d18735` (via spirit lock) | flake.nix (API: fromPkgs, fromToolchainFile, fromPkgsWithToolchain) |
| herdr v0.8.2 | store path `n4fsjxky` | Closure inspection (glibc 2.42-61) |
| orca-ide | store path in closure | Closure inspection (glibc 2.42-67, different hash from fork) |
| Psyche report | `flows/674a4dab/reports/psychePackagesSources.md` | All psyche statements quoted verbatim from that report |
| Nix side map | `flows/674a4dab/witnesses/nixSideMap.md` | Structural reference, updated where origin/main differs |
