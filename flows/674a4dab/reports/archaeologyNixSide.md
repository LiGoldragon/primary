# Nix-Side Archaeology

How each structural shape came to be: commits, dates, psyche evidence.
All file references cite `origin/main` of the respective repository unless noted.

## 1. Stub Flake Inputs (stubs/no-horizon, no-system, no-secrets, default-deployment)

### Observations

The stub-override architecture was introduced in CriomOS across three sessions:

- **2026-04-24**, commit `7a7ff9e7de`: `stubs/no-horizon/flake.nix` added; CriomOS declares `horizon` as a flake input defaulting to `path:./stubs/no-horizon`, to be overridden by lojix at deploy time. Same session, commit `cbeb2328e1`: `stubs/no-system` added for the system-tuple input. Commit `d8b8add4f5` introduced the "ractor tool design" report describing ephemeral-flake-input architecture with lojix as orchestrator.
- **2026-05-02**, commit `6794016a38`: `stubs/default-deployment` added (deployment-shape input: `includeHome`, `includeAllFirmware`).
- **2026-05-14**, commits `b7b7d5043d` / `e0f8db287e`: `stubs/no-secrets` added for sops integration.

The lojix repo's earliest commit is 2026-05-13; its `--override-input` mechanism postdates the stubs.

All commit messages use structured agent tuple format. Author is "li" (matching machine gitconfig, consistent with agents committing under the machine user).

**Psyche evidence**: No Codex sessions exist before 2026-05-09. No Claude Code transcripts survive from April-May 2026 for the Criopolis project. No typed psyche message was found requesting the stub-override architecture.

### Inference

The stub-override architecture was designed and implemented by an agent on 2026-04-24 as part of the CriomOS rewrite. The design is coherent and well-documented in commit messages. No evidence that the psyche asked for this specific shape; equally, no evidence the psyche was absent from the session.

### Unknown

Whether the psyche directed the April 24 session that produced this. No transcript evidence survives.

---

## 2. pkgs from CriomOS-home's homeConfigurations; normalize.nix mkOverride 0 []

### Observations

**`pkgs = (builtins.head (builtins.attrValues inputs.criomos-home.homeConfigurations)).pkgs`**

- Introduced **2026-08-23**, commit `4c3da1562c49`, message: "criomos: preserve Home package-set equivalence gate".
- Replaced `pkgs = inputs.pkgs.pkgs` (using CriomOS-pkgs) with extraction from CriomOS-home's homeConfigurations.
- Purpose: ensure the pkgs set used by the NixOS side is identity-equal to the one CriomOS-home evaluates, so that embedded and standalone home configurations produce the same closure.

On the same day the psyche said:

> "to me, this looks like a need to abstract the common ground between OS and home to a separate repo, and using that repo as the source for anything that is shared between them. indirection is bad design"
> -- flow `01a030a1/vision/commonGround.md`, 2026-08-24T00:58:00+02:00

The psyche's direction was toward a neutral shared repo, not the `builtins.head` indirection. The agent implemented a different mechanical solution.

**`nixpkgs.overlays = mkOverride 0 []`** (normalize.nix line 174 at `origin/main`)

- Present since the first CriomOS commit `eff6eea67de3`, 2026-04-23, scaffolded from the criomos-archive.
- The criomos-archive (CriomOS--dev) carried the comment "# Overlays are bad - force them off" alongside this line.
- On 2026-04-24, commit `cbeb2328e1b6` introduced `readOnlyPkgs` (NixOS module making `pkgs.config` / `overlays` read-only), a more structured companion.
- On 2026-04-27, commit `82dffa579c6f` extracted overlays into CriomOS-pkgs. The psyche said: "fine, just create another repo then, and put the overlay in it" (per commit message; no surviving transcript for this date).

### Inference

The `builtins.head` pkgs-from-home pattern was an agent decision to solve a package-set identity problem; the psyche's expressed direction on 2026-08-24 was toward a shared neutral repo, not this indirection. The `mkOverride 0 []` is legacy from the criomos-archive, likely agent-originated. The "fine, just create another repo" quote (from commit message, not transcript) suggests the psyche accepted rather than originated the CriomOS-pkgs extraction.

### Unknown

The psyche's original words about CriomOS-pkgs ("fine, just create another repo") are known only from the commit message, not from a verified transcript.

---

## 3. CriomOS-home Input Sprawl

### Observations

**llm-agents (keeps its own NixOS/nixpkgs)**

- First added 2026-04-23 in the scaffold from criomos-archive (commit `87863634758c`).
- Removed 2026-04-24 (commit `d0893a1e7dfd`) by an agent calling it "unused indirection."
- Re-added 2026-04-27 (commit `ef7a17562d45`). Per commit message, the psyche said: "I am using claude-code and codex 12 hours a day, so why the fuck would I want to drop it?!" (STT-uncorrected)
- Originally followed the fork nixpkgs. **Unfollowed 2026-06-03** (commit `f614a7884363`): agent decision, commit says "its package set follows fast tool packaging and currently needs newer pnpm attributes than the profile-wide nixpkgs pin provides." No Codex session exists for that date. No psyche ask found.

**herdr + orca-ide (each with own NixOS/nixpkgs)**

- Both added 2026-08-23 (commit `00b3ab2a6407`). Neither was wired with `follows`. These are third-party flakes (herdrdev/herdr, Samuka007/nix-orca) that declare their own nixpkgs input. No psyche user message found asking for herdr or orca in Codex sessions on that date. Agent decision with no recorded psyche ask.

**stylix (brings nixpkgs-stable)**

- Present from the first commit (2026-04-23), inherited from criomos-archive. stylix is a third-party flake (danth/stylix) that declares its own `nixpkgs-stable` input. This is inherent to stylix's flake structure, not a CriomOS-home choice.

**Non-flake VSIX inputs**

- First VSIX (visualjj): 2026-04-27 (commit `edde59e7bb7f`), converted to `type=file` flake input. Per commit message, the psyche said: "I would prefer if those things are fetched as a nix flake input (the llm models are another story)." The VSIX-as-flake-input pattern was psyche-directed.

**Non-flake npm tarballs (Agent Intercom, Pi)**

- Pi (npm): 2026-04-29 (commit `410680bd5334`), replaced pi-mentci wrapper flake with direct `buildNpmPackage` from non-flake `pi-src` input.
- Agent Intercom adapters: first appeared 2026-07-26 (commit `13eca8b6052f`, authored 2026-07-20). Individual npm tarball inputs proliferated because Node.js dependencies were pinned as individual flake inputs rather than using a lockfile-driven fetcher. No psyche ask found for a separate source per dependency.

### Inference

The psyche asked for tools to be present and for sources to be tracked as flake inputs ("I would prefer if those things are fetched as a nix flake input"). The per-tool nixpkgs divergence was not psyche-directed: it arose from (1) third-party flakes (stylix, herdr, orca-ide) packaging their own nixpkgs with no `follows` wired, and (2) an agent decision to unfollow llm-agents' nixpkgs for pnpm compatibility. The npm tarball sprawl was an agent packaging decision to satisfy Nix's pure evaluation, not a psyche request for a separate source per dependency.

### Unknown

Whether the psyche was present in the session that unfollowed llm-agents' nixpkgs (2026-06-03). No transcript survives.

---

## 4. Dual Definitions

### Observations

**`home.stateVersion`**

- In CriomOS `userHomes.nix`: added 2026-04-24, commit `31d49adca5`, "phase8, wire" -- wiring home-manager end-to-end via lojix eval.
- In CriomOS-home `flake.nix`: added 2026-05-03, commit `9f14bdd246`, "Expose direct home configurations" -- creating the standalone `mkHomeConfiguration` path for equivalence checking.
- No psyche transcripts exist for either date. Two separate agents, in separate sessions, each needed `home.stateVersion` for their respective codepaths (embedded NixOS home-manager vs. standalone homeConfigurations). Neither saw the other's work.

**LAN subnet (`10.18.0.0/24`, gateway `10.18.0.1`)**

- In CriomOS-lib `constants`: added 2026-05-03, commit `bf3528bb98`, "Expose shared constants". Hardcoded in `lib/default.nix` as `constants.network.lan`.
- In the horizon data (goldragon `datom.dotos`): the LAN data entered when horizon-rs was promoted to own the cluster topology. The horizon.dotos version carries an explicit annotation: `[TEMPORARY: single-router IPv4 LAN until IPv6-first networking lands]`, showing architectural awareness.
- CriomOS-lib constants predate the horizon schema and were not cleaned up when horizon took over.

**`node.services` parsing**

- In CriomOS `node-services.nix`: added 2026-05-18, commit `2715480498`, "criomos: consume node service variants". A shared Nix library exporting `has`, `payload`, `servicesList` functions. Imported by agent-intercom.nix, lojix-persona-development.nix, persona-router.nix, mirror.nix, repository-receive.nix, vm-testing.
- In CriomOS-home `profiles/min/agent-intercom.nix`: added 2026-07-20, commit `13eca8b605`, "home: configure Agent Intercom adapters". Contains an inline `serviceName` function and `hasCapability` helper -- functionally identical to CriomOS's `node-services.nix` but reimplemented locally because CriomOS-home cannot import CriomOS's files (separate repos, separate eval contexts).

### Inference

All three dual definitions are accidental consequences of the repo split. No psyche request or acknowledgment of any of them was found. The `home.stateVersion` duplication came from two agents working independently on different codepaths. The LAN subnet duplication came from CriomOS-lib predating the horizon schema without cleanup. The `node.services` reimplementation came from the structural inability of CriomOS-home to import CriomOS's shared library -- `criomos-lib` would be the natural home for this parser, but it was not placed there.

The psyche's later statements (2026-08-24) about abstracting "common ground between OS and home to a separate repo" and "indirection is bad design" are retrospective -- they describe the direction to resolve these duplications, not their origin.

### Unknown

Whether any agent ever surfaced these duplications to the psyche before 2026-08-24.

---

## 5. The CriomOS / CriomOS-home / CriomOS-lib / CriomOS-pkgs Split

### Observations

**Pre-split history (CriomOS--dev monorepo)**

- Root commit rebased to 2020-03-12. A NixOS monorepo containing system config, home-manager modules (`nix/homeModule/`), lib (`criomos-lib.nix`), and pkgs (`nix/mkPkgs/`).
- Home module existed since at least 2022-08-13.
- `criomos-lib.nix` "separated" internally on 2026-01-11.

**CriomOS-v2 (intermediate)**

- Single commit 2026-03-20: "fresh rewrite -- composable Nix infrastructure replacing monolithic NixOS builder". An intermediate repo with flake input overrides.

**The four-way split (2026-04-23 to 2026-04-26)**

- CriomOS + CriomOS-home: 2026-04-23, first commits same day.
- CriomOS-lib: 2026-04-25.
- CriomOS-pkgs: 2026-04-26 (per psyche: "fine, just create another repo then, and put the overlay in it" -- from commit message).

No Codex or Claude Code transcripts exist for April 2026. All four repos were created in a 3-day span, suggesting agent-driven restructuring during the CriomOS-v2 rewrite. The CriomOS--dev commit authorship shows Mentci AI involvement.

**Psyche on the split (later, retrospective)**

> "to me, this looks like a need to abstract the common ground between OS and home to a separate repo, and using that repo as the source for anything that is shared between them. indirection is bad design"
> -- flow `01a030a1/vision/commonGround.md`, 2026-08-24T00:58:00+02:00

> "Then find all the commonality between the OS and home repos, then make a proposal on moving the source of it all in a new criomos-core repo which would export them as exported namespaces for criomos and criomos-home to use"
> -- flow `01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`, 2026-08-24T01:17:47+02:00

> "I think core is more accurate than lib, yes, so superseding is the right perspective."
> -- flow `01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`, 2026-08-25T14:03:52+02:00

### Inference

The four-repo split on 2026-04-23--26 was executed by an agent (likely Mentci AI, given CriomOS--dev commit authorship). No transcript shows the psyche requesting the original four-way split. The psyche's August 2026 statements acknowledge the split's premise but critique its current shape, proposing criomos-core to supersede CriomOS-lib and resolve the duplications the split produced.

### Unknown

Whether the psyche reviewed or directed the April 2026 split at the time it happened. The absence of transcripts from that period means this cannot be confirmed or denied.

---

## 6. The Follows Web

### Observations

Follows were added incrementally across six commits in CriomOS:

1. **2026-04-23**, commit `eff6eea`: CriomOS scaffold -- initial `criomos-home.inputs.nixpkgs.follows = "nixpkgs"` and `criomos-home.inputs.home-manager.follows = "home-manager"`.
2. **2026-04-25**, commit `4507a4c`: `criomos-home.inputs.criomos-lib.follows = "criomos-lib"` added as part of CriomOS-lib extraction.
3. **2026-05-03**, commit `152779e`: `criomos-home.inputs.{horizon,system,pkgs}.follows` added ("Forward deploy inputs to home").
4. **2026-06-15**, commit `18e6ed9`: `criomos-home.inputs.rust-overlay.follows` ("align criomos home rust overlay input").
5. **2026-07-04**, commit `e427719`: `criomos-home.inputs.spirit.follows` ("pin guardian spirit").
6. **2026-07-17**, commit `b83f19c`: `criomos-home.inputs.orchestrate.follows` ("pin unrestricted pi-subagents runtime").

**`_module.args.inputs` forcing** was introduced in CriomOS-home, commit `a78644d`, 2026-04-25. The commit message says: "override _module.args.inputs to CriomOS-home own inputs (architecture fix for home-tcj per Li 2026-04-25 + reports/0019)". The phrase "per Li" confirms the psyche asked for this fix.

### Inference

The initial follows (nixpkgs, home-manager) are standard Nix practice, part of the scaffold, likely agent-originated. The `_module.args.inputs` forcing was explicitly asked for by the psyche ("per Li 2026-04-25") as an architecture fix -- ensuring CriomOS-home modules see their own inputs rather than CriomOS's, even when evaluated embedded inside a NixOS configuration. The later follows (rust-overlay, spirit, orchestrate) were added incrementally by agents as each input was added to CriomOS-home and needed alignment -- no transcript evidence of psyche asking for them specifically.

### Unknown

The psyche's exact words from 2026-04-25 are not recoverable. The `reports/0019` referenced in the commit is in the CriomOS repo (not verified). No Codex sessions exist before 2026-05-09.

---

## Map Conflict: goldragon/datom.dotos vs criomos-horizon-config/horizon.dotos

### Resolution

**`criomos-horizon-config/horizon.dotos` does not exist.** No file named `horizon.dotos` exists anywhere on disk, and no directory named `criomos-horizon-config` exists as a repository.

**The actual cluster proposal file is `goldragon/datom.dotos`**, located at `/home/li/wt/github.com/LiGoldragon/goldragon/p99n-gold-main/datom.dotos`. Its header:

```
;; goldragon -- production cluster proposal for the LiGoldragon kriom.
;; Schema: horizon-rs ClusterProposal (positional records, source-decl order).
```

It contains node definitions (balboa, ouranos, etc.) as DOTOS-format brace records with hardware model, SSH keys, disk layout, and user attributes.

Lojix receives the proposal source path as a `ProposalSource` string parameter per deployment request; it is not hardcoded. The goldragon repo's `datom.dotos` is the production cluster's file.

The structural map's "criomos-horizon-config/horizon.dotos" appears to be either a planned-but-not-yet-created repository or a conceptual name used in architecture documents that maps to what is currently `goldragon/datom.dotos`.

---

## Sources

- CriomOS git history: `/home/li/wt/github.com/LiGoldragon/CriomOS/p99n-criomos-main` (jj-managed; `origin/main` at `45e83fbc`, 2026-08-28)
- CriomOS-home git history: `/home/li/wt/github.com/LiGoldragon/CriomOS-home/p99n-home-main` (jj-managed; `origin/main` at `ed6832cf`, 2026-08-28)
- Lojix git history: `/home/li/wt/github.com/LiGoldragon/lojix`
- Goldragon cluster data: `/home/li/wt/github.com/LiGoldragon/goldragon/p99n-gold-main/datom.dotos`
- Psyche vision records: `/home/li/primary/flows/01a030a1/vision/commonGround.md`, `/home/li/primary/flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`
- Nix-side structural map: `/home/li/primary/flows/674a4dab/witnesses/nixSideMap.md`
- Codex transcripts searched: `~/.codex/sessions/2026/` (earliest session found: 2026-05-09)
- Claude Code transcripts searched: `~/.claude/projects/-home-li-Criopolis/`, `~/.claude/projects/-home-li-primary/`

## Correction by flow 674a4dab (2026-08-28) — the map conflict

The subflow's statement that `criomos-horizon-config/horizon.dotos` does not exist is wrong: it searched under `/home/li/wt/` only. The repository exists at `/git/github.com/LiGoldragon/criomos-horizon-config` (origin/main `e222d3a`) and holds `horizon.dotos`, a `HorizonProposal` carrying `DomainSuffixes [criome] [criome.net]` and `TransitionalIpv4Lan 10.18.0.0/24 / 10.18.0.1` with a DHCP pool. The cluster proposal (nodes, users) is `goldragon/datom.dotos`, as the Rust map said. At origin/main, CriomOS `flake.nix` carries no reference to criomos-horizon-config and horizon-rs's Rust source has no reader for it (only its AGENTS.md/ARCHITECTURE.md/skills.md mention it); the Rust-side archaeology likewise found horizon-rs main does not consume it. Witness: `flows/674a4dab/witnesses/workingCopyState.md`.
