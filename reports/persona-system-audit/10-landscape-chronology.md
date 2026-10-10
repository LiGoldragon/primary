# Landscape & Repository Chronology

I now have enough evidence to compile the full structured map. Here is the complete report:

---

## Situational Map — Commit-Volume Chronology and Repo Topology

**Scope:** LiGoldragon GitHub account, local clones at `/git/github.com/LiGoldragon/`, primary workspace at `/home/li/primary`. Read-only scout pass. Commands run: `gh repo list`, `gh api .../commits`, `git log`, `jj log`, filesystem inspection of `/home/li/primary/ARCHITECTURE.md`, `protocols/repos-manifest.nota`, `protocols/active-repositories.md`. Today: 2026-07-01.

---

### 1. Local Source Areas

**`/home/li/primary/repos/`** — empty (verified `ls -la`: only `.` and `..`). The ARCHITECTURE.md §3 confirms the `repos/` symlink index was retired; it is no longer the inventory surface.

**`/home/li/primary/private-repos/`** — does not exist (not created). ARCHITECTURE.md §5 notes it is gitignored and separate from `repos/`; it is simply absent on this machine.

**`/git/github.com/LiGoldragon/`** — canonical clone location per ARCHITECTURE.md §3. Approximately 70+ repos cloned here, including all active repos listed in `protocols/repos-manifest.nota`.

**`/home/li/primary/`** — a Jujutsu (JJ) repo. 300 commits. All in May-July 2026 (the workspace was initialized May 6, 2026).

---

### 2. Full Repo Table

All 152 GitHub repos (LiGoldragon account), sorted by creation date, role-guessed from descriptions and manifest.

**Pre-AI era (2022-2025) — 6 repos**

| Repo | Vis | Role guess | Created | Last push | Approx commits | Purpose |
|---|---|---|---|---|---|---|
| goldragon | pub | content/personal | 2022-09-20 | 2026-07-01 | low | Personal site / profile |
| maisiliym | pub | predecessor-OS | 2022-10-08 | 2026-05-09 | unknown | (no description; Nix) |
| criomos-archive | pub | predecessor-OS | 2023-02-17 | 2026-04-27 | unknown | "A linux-based OS to host the Criome" — archived NixOS predecessor |
| password-store | PRIV | content/personal | 2023-02-18 | 2026-06-20 | low | Password store |
| kibord | pub | content/hardware | 2023-07-11 | 2026-06-11 | low | C keyboard firmware |
| qmkBinaries | pub | content | 2023-11-13 | 2026-05-30 | low | QMK keyboard binaries |

**AI era — books and content (2025-Jan 2026) — 4 repos**

| Repo | Vis | Role guess | Created | Last push | Approx commits | Purpose |
|---|---|---|---|---|---|---|
| TheBookOfSol | pub | content | 2025-05-30 | 2026-06-30 | unknown | Personal writings |
| ArtificialIntelligence | pub | content | 2026-01-04 | 2026-05-18 | 2 | Likely notes/experiments |
| BookOfLuna | pub | content | 2026-01-04 | 2026-05-18 | 2 | Book content |
| WebPublish | pub | tooling (deprecated) | 2025-12-06 | 2026-06-11 | unknown | "Deprecated: remote archived + local deleted" per manifest |

**AI-agent coding start — Mentci-AI (Feb 2026)**

| Repo | Vis | Role guess | Created | Last push | Approx commits | Purpose |
|---|---|---|---|---|---|---|
| Mentci-AI | pub | predecessor | 2026-02-18 | 2026-03-22 | 164 | NixOS/Nix configuration for Mentci AI system — the repo where the Feb 20 spike landed |

**Predecessor cluster — Mentci v1/v2 + aski/noesis/samskara (March-April 2026)**

| Repo | Vis | Role guess | Created | Last push | Approx commits | Purpose |
|---|---|---|---|---|---|---|
| aski-core | pub | predecessor | 2026-01-13 | 2026-04-20 | 64 | Aski language core (all 64 commits landed Apr 16-20) |
| mentci-box | pub | predecessor-Nix | 2026-03-05 | 2026-03-23 | small | NixOS host for Mentci |
| mentci-launch | pub | predecessor | 2026-03-05 | 2026-03-06 | small | Rust launcher for Mentci |
| mentci-stt | pub | predecessor | 2026-03-05 | 2026-03-06 | small | Speech-to-text for Mentci |
| mentci-user | pub | predecessor | 2026-03-05 | 2026-03-20 | small | User component for Mentci |
| samskara | pub | predecessor | 2026-03-05 | 2026-04-15 | 73 | "Pure datalog agent — sees only relations, owns samskara.cozo" |
| mentci-mcp | pub | predecessor | 2026-03-05 | 2026-03-06 | small | MCP connector for Mentci |
| mentci-execute | pub | predecessor | 2026-03-06 | 2026-03-09 | small | Execution component |
| jcodemunch-mcp | pub | tooling | 2026-03-07 | 2026-03-07 | small | Token-efficient MCP for GitHub code |
| lsp-pi | pub | tooling | 2026-03-08 | 2026-03-08 | small | LSP integration for pi coding agent |
| oh-my-pi | pub | tooling | 2026-03-09 | 2026-03-10 | small | "AI Coding agent for terminal — hash-anchored edits" |
| chronos-lib | pub | predecessor-support | 2026-03-08 | 2026-03-08 | small | Shared chronos defaults for Mentci |
| samskara-lojix-contract | pub | predecessor | 2026-03-16 | 2026-04-06 | unknown | "Datalog schema contract between Samskara and Lojix agents" |
| criome-cozo | pub | predecessor | 2026-03-16 | 2026-04-06 | unknown | "CozoDB wrapper — shared DB primitives for Criome agents" |
| Mentci-v1 | pub | predecessor | 2026-03-16 | 2026-04-06 | 90 | "VersionOne workspace — Nix flake tying Samskara + Lojix" |
| samskara-codegen | pub | predecessor | 2026-03-18 | 2026-04-06 | small | Codegen for Samskara |
| bibliotheca | pub | tooling | 2026-03-20 | 2026-04-06 | small | "Rust client library for Anna's Archive" |
| criome-rt | pub | predecessor | 2026-03-20 | 2026-03-20 | small | "Criome runtime — process jails with network namespace isolation" |
| CriomOS-v2 | pub | predecessor-OS | 2026-03-20 | 2026-03-20 | small | "CriomOS v2 — standard runtime substrate for Criome components" |
| library | PRIV | content | 2026-03-21 | 2026-06-13 | small | "Curated reference library for Mentci v1 astrological ontology" |
| arca | pub | supporting | 2026-03-21 | 2026-07-01 | low | Content-addressed tree (arca) |
| samskara-core | pub | predecessor | 2026-03-21 | 2026-04-06 | small | Samskara core |
| criome-stored | pub | predecessor | 2026-03-21 | 2026-03-28 | small | Criome storage daemon (first gen) |
| samskara-reader | pub | predecessor | 2026-03-22 | 2026-03-28 | small | Samskara reader |
| tree-sitter-cozo | pub | tooling | 2026-03-23 | 2026-03-23 | small | Tree-sitter grammar for CozoScript |
| noesis-schema | pub | predecessor | 2026-03-24 | 2026-04-06 | small | "Noesis schema — typed binary agent harness CozoScript definitions" |
| noesis | pub | predecessor | 2026-03-24 | 2026-04-06 | small | "Noesis — typed binary agent harness, capnp RPC replacing MCP JSON-RPC" |
| lojix-macros | pub | predecessor | 2026-03-24 | 2026-04-06 | small | "Proc macros from samskara datalog schema" |
| sema | pub | main-line (thread) | 2026-03-24 | 2026-07-01 | 108 | "Sema — the symbolism layer of logical intent." (history to 2019) |
| veri-core | pub | predecessor | 2026-03-24 | 2026-04-20 | unknown | "Sema Core — Phase/Dignity, Astrality, Structure" |
| mentci-archive | pub | predecessor | 2026-03-26 | 2026-04-27 | 748 | "Mentci — Sema/Noesis workspace" — MAIN predecessor work surface |
| Pi-Mentci | pub | predecessor-Nix | 2026-03-27 | 2026-04-20 | small | "Minimal Nix-packaged Pi environment for Mentci" |
| astro-aski | pub | predecessor-support | 2026-04-01 | 2026-05-30 | unknown | "Astrological chart software — domain model in aski" |
| aski-cc | pub | predecessor | 2026-04-02 | 2026-05-30 | unknown | "aski compiler — Surface DB, macro expansion, aski-to-kernel pipeline" |
| semac | pub | predecessor | 2026-04-02 | 2026-05-25 | unknown | "aski Rust backend — Kernel Aski parser, codegen, rustc integration" |
| pi-delegate | pub | tooling | 2026-04-02 | 2026-04-03 | small | "Delegate tasks to Claude, Gemini, Codex, Pi via their official CLIs" |
| askicc | pub | predecessor | 2026-04-02 | 2026-04-20 | small | aski compiler variant |
| vscode-aski | pub | predecessor | 2026-04-04 | 2026-04-16 | small | VS Code tree-sitter extension for Aski |
| tree-sitter-aski | pub | predecessor | 2026-04-05 | 2026-04-05 | small | Aski tree-sitter grammar |
| nexus-spec-archive | pub | predecessor | 2026-04-07 | 2026-05-30 | 26 | "Relational dialect of aski — declaration + protocol language for typed binary Worlds" |
| substack-cli | pub | tooling | 2026-04-07 | 2026-07-01 | small | "Command-line tool for publishing Substack posts" |
| arbor | pub | supporting/shelved | 2026-04-07 | 2026-04-09 | small | "Content-addressed tree over rkyv + blake3" (shelved per criome ARCH docs) |
| askic | pub | predecessor | 2026-04-13 | 2026-04-20 | small | "askic — the aski compiler, written in aski" |
| synth-core | pub | predecessor | 2026-04-15 | 2026-04-20 | small | "aski-core — type definitions for aski" |
| aski-archive | pub | predecessor | 2026-04-16 | 2026-04-16 | small | "aski repo archive (pre-v017 history with bloated target/)" |
| corec | pub | predecessor | 2026-04-16 | 2026-04-20 | small | "corec — core compiler: .aski → Rust with rkyv derives" |
| domainc | pub | predecessor | 2026-04-17 | 2026-04-19 | small | "domainc — rkyv parse tree → per-program Rust domain crate" |
| veric | pub | predecessor | 2026-04-17 | 2026-04-20 | small | "veric — aski verifier" |
| aski | pub | predecessor | 2026-04-20 | 2026-04-25 | 64 | "Aski — text notation for specifying sema. Language spec, editor modes, tree-sitter grammar" |
| workspace | pub | predecessor-Nix | 2026-04-22 | 2026-05-02 | unknown | "AI-driven workspace: Nix flake via numtide/blueprint" — transitional workspace |
| mentci-tools | pub | predecessor-Nix | 2026-04-22 | 2026-04-27 | small | "Shared CLI wrappers (Dolt, etc.) for the mentci-* workspace" |
| lore | pub | main-line support | 2026-04-22 | 2026-07-01 | unknown | "Curated docs from upstream tools + our discoveries" |
| annas-mcp | pub | tooling | 2026-04-24 | 2026-05-09 | small | "MCP server and CLI tool for Anna's Archive" |
| caraka-samhita | pub | content | 2026-04-24 | 2026-06-05 | low | "Philological study of the Caraka Saṃhitā" |
| lojix-archive | pub | predecessor | 2026-04-24 | 2026-05-01 | 51 | "Archived first-generation CriomOS deploy CLI" |

**Main-line current system (April 2026 - present)**

The following are all Active in `repos-manifest.nota`. Grouped by family:

*CriomOS family:*

| Repo | Vis | Role | Created | Last push | Local commits | Purpose |
|---|---|---|---|---|---|---|
| CriomOS | pub | main-line platform | 2026-04-23 | 2026-07-01 | 413 | "Network-neutral NixOS platform." — canonical rewrite on Apr 23 |
| CriomOS-home | pub | main-line platform | 2026-04-23 | 2026-07-01 | unknown | "Home profile for CriomOS as a standalone blueprint flake" |
| CriomOS-lib | pub | main-line platform | 2026-04-25 | 2026-06-11 | unknown | "Shared helpers + data files for CriomOS and CriomOS-home" |
| CriomOS-pkgs | pub | main-line platform | 2026-04-26 | 2026-07-01 | unknown | "CriomOS pkgs axis — nixpkgs instantiation + overlays" |
| CriomOS-emacs | pub | main-line platform | 2026-04-23 | 2026-06-08 | unknown | "Emacs distribution for the CriomOS home profile" |
| CriomOS-test-cluster | pub | main-line platform | 2026-05-12 | 2026-07-01 | unknown | "Independent CriomOS fixture cluster" |
| criomos-horizon-config | pub | main-line data | 2026-05-17 | 2026-07-01 | unknown | Horizon configuration data |

*Core Persona/Criome stack:*

| Repo | Vis | Role | Created | Last push | Local commits | Purpose |
|---|---|---|---|---|---|---|
| nexus | pub | main-line core | 2026-04-23 | 2026-07-01 | 85 | "Typed semantic text vocabulary written in NOTA syntax" |
| nexus-cli | pub | main-line core | 2026-04-23 | 2026-06-30 | unknown | CLI surface for Nexus-shaped NOTA records |
| signal | pub | main-line core | 2026-04-25 | 2026-07-01 | 75 | "Sema-ecosystem record vocabulary" (rkyv messaging schema) |
| criome | pub | main-line core | (2024-05-28 init) | 2026-07-01 | 152 | "Validating record-graph daemon at the heart of the sema-ecosystem" |
| sema | pub | main-line core (thread) | 2026-03-24 | 2026-07-01 | 108 | "Typed storage kernel (redb + rkyv + schema guard)" |
| sema-engine | pub | main-line core | 2026-05-14 | 2026-07-01 | unknown | "Typed database verb engine over sema and signal-core" |
| persona | pub | main-line APEX | 2026-05-07 | 2026-07-01 | 199 | "Persona meta-repo; wires the stack. Meta-AI system." |
| spirit | pub | main-line core | 2026-05-26 | 2026-07-01 | 265 | "Active production Spirit implementation — intent store daemon" |
| forge | pub | main-line | 2026-04-25 | 2026-07-01 | 22 | "lojix daemon. Forge + store + deploy actors" |
| lojix | pub | main-line | 2026-05-13 | 2026-07-01 | unknown | "Long-lived deploy orchestrator daemon" |
| horizon-rs | pub | main-line | 2026-04-23 | 2026-07-01 | unknown | "horizon schema, type-check, and method-computation CLI for CriomOS" |
| mirror | pub | main-line | 2026-06-12 | 2026-07-01 | unknown | "Payload-blind append-ingest mirror daemon: sema version-control remote" |
| cloud | pub | main-line | 2026-05-23 | 2026-07-01 | unknown | "Criome cloud provider API daemon" |
| domain-criome | pub | main-line | 2026-05-23 | 2026-07-01 | unknown | "Criome domain registry, projection daemon" |
| repository-ledger | pub | main-line | 2026-06-01 | 2026-06-20 | unknown | "Gitolite repository event ledger daemon" |

*Persona component daemons:*

| Repo | Vis | Role | Created | Last push | Local commits | Purpose |
|---|---|---|---|---|---|---|
| mind | pub | main-line | 2026-05-07 | 2026-07-01 | unknown | "Central Persona state component" |
| message | pub | main-line | 2026-05-07 | 2026-07-01 | unknown | "Engine message ingress" |
| router | pub | main-line | 2026-05-07 | 2026-07-01 | unknown | "Message routing and delivery coordination" |
| harness | pub | main-line | 2026-05-07 | 2026-07-01 | unknown | "Interactive harness abstraction for Persona" |
| system | pub | main-line | 2026-05-07 | 2026-07-01 | unknown | "Portable OS and window-manager boundary for Persona" |
| terminal | pub | main-line (inactive) | 2026-05-07 | 2026-06-30 | unknown | "Persona terminal session owner" (currently inactive; use terminal-cell) |
| terminal-cell | pub | main-line | 2026-05-10 | 2026-06-30 | unknown | "Prototype durable terminal session owner with transcript replay" |
| introspect | pub | main-line | 2026-05-13 | 2026-06-30 | unknown | "Persona inspection-plane daemon" |
| orchestrate | pub | main-line | 2026-05-18 | 2026-06-30 | unknown | "Cascade orchestrator / runtime that runs the set of component daemons" |
| agent | pub | main-line | 2026-06-09 | 2026-07-01 | unknown | "LLM-API-call component daemon (provider HTTP API calls)" |
| upgrade | pub | main-line | 2026-05-24 | 2026-06-30 | unknown | "Upgrade triad runtime scaffold" |
| persona-spirit | pub | main-line | 2026-05-19 | 2026-06-08 | unknown | "Persona psyche to mind interface component" |
| mentci | pub | main-line | 2026-06-18 | 2026-07-01 | 47 | "Programmable human approval daemon" |
| mentci-lib | pub | main-line | 2026-04-29 | 2026-07-01 | 40 | "Heavy application logic for the mentci interaction surface" |
| mentci-egui | pub | main-line | 2026-04-29 | 2026-07-01 | 42 | "First incarnation of the mentci interaction surface (egui shell)" |
| listener | pub | main-line | 2026-07-01 | 2026-07-01 | new | "Listener speech-to-text CLI and supervised daemon scaffold" |

*Schema layer:*

| Repo | Vis | Role | Created | Last push | Local commits | Purpose |
|---|---|---|---|---|---|---|
| schema-next | pub | main-line | 2026-05-26 | 2026-06-30 | unknown | "Replacement schema macro engine and assembled schema model" |
| nota-next | pub | main-line | 2026-05-26 | 2026-06-30 | unknown | "Replacement NOTA structural reader for the schema-derived stack" |
| schema-rust-next | pub | main-line | 2026-05-26 | 2026-06-30 | unknown | "Replacement Rust emission layer — lowers schema-in-Rust into Rust interface code" |
| tree-sitter-schema | pub | main-line | 2026-06-13 | 2026-06-13 | small | "Tree-sitter grammar for authored SEMA schema files" |
| tree-sitter-nota | pub | main-line | 2026-06-13 | 2026-06-13 | small | "Tree-sitter grammar for raw NOTA structure" |

*Signal / MetaSignal contracts (all main-line):* signal-derive, signal-frame, signal-standard, signal-sema, signal-agent, signal-cloud, signal-criome, signal-domain-criome, signal-forge, signal-harness, signal-introspect, signal-lojix, signal-listener, signal-mentci, signal-mentci-client (PRIV), signal-message, signal-mind, signal-mirror, signal-orchestrate, signal-persona, signal-repository-ledger, signal-router, signal-spirit, signal-system, signal-terminal, signal-upgrade, signal-version-handover, meta-signal-{agent,cloud,criome,domain-criome,harness,introspect,lojix,listener,mentci,mentci-client,message,mind,mirror,orchestrate,persona,repository-ledger,router,spirit,system,terminal,upgrade,version-handover}. All created April-June 2026, all pushed through July 2026.

*Tooling / support:*

| Repo | Vis | Role | Created | Last push | Purpose |
|---|---|---|---|---|---|
| primary | pub | workspace | 2026-05-06 | 2026-07-01 | Coordination workspace (this repo, 300 jj commits) |
| skills | pub | tooling | 2026-06-26 | 2026-07-01 | Skill packets source (generates .claude/.pi/.codex agent files) |
| lore | pub | tooling | 2026-04-22 | 2026-07-01 | Cross-workspace agent discipline and lore |
| rust-build | pub | tooling | 2026-06-18 | 2026-07-01 | "Shared Nix build policy for LiGoldragon Rust repositories" |
| triad-runtime | pub | tooling | 2026-06-02 | 2026-07-01 | "Shared runtime support for schema-derived Signal/Nexus/SEMA triad daemons" |
| version-projection | pub | tooling | 2026-05-22 | 2026-07-01 | "Shared projection and compatibility-policy library" |
| hexis | pub | tooling | 2026-04-28 | 2026-06-19 | "Managed-mutable config reconciliation with per-key modes" |
| chroma | pub | tooling | 2026-05-08 | 2026-07-01 | "One Rust daemon for theme, warmth, and brightness, controlled via NOTA" |
| chronos | pub | tooling | 2026-05-08 | 2026-07-01 | "Daemon publishing zodiacal time, sunrise/sunset, and twilight events" |
| brightness-ctl | pub | tooling | 2026-04-23 | 2026-06-19 | "Brightness control daemon — laptop backlight + idle dimming" |
| clavifaber | pub | tooling | 2026-04-23 | 2026-07-01 | "GPG to X.509 certificate tool for CriomOS WiFi PKI" |
| whisrs | pub | tooling (fork) | 2026-05-11 | 2026-06-11 | "Linux-first voice-to-text dictation tool for Wayland" (fork) |
| kameo | pub | tooling (fork) | 2026-05-16 | 2026-06-19 | "Fault-tolerant async actors for Rust" (fork) |
| kameo-testing | pub | tooling | 2026-05-10 | 2026-06-19 | "Kameo 0.20 testing bed and source for the Kameo skill" |
| substack-cli | pub | tooling | 2026-04-07 | 2026-07-01 | "Command-line tool for Substack posts" |
| claude-answers | pub | tooling | 2026-07-01 | 2026-07-01 | "Recall answers to Claude Code questions from session transcripts" |
| nota-config | pub | tooling | 2026-05-15 | 2026-07-01 | "Typed configuration input for Persona-stack binaries" |

---

### 3. Commit-Volume Timeline

All dates are author timestamps from `git log --date=short` or `gh api`.

```
2019-2022   sema (legacy): ~17 commits spread across 2019-2022 — "biosphere" project
            (pre-AI, solo work)

2023        criomos-archive active; kibord; ~5-10 commits/year pace overall

2025        TheBookOfSol published; WebPublish (now deprecated)

2026-01-04  ArtificialIntelligence created: 1 commit on Jan 4
            BookOfLuna created: 1 commit on Jan 4
2026-01-07  sema: 2 commits (tentative early AI-touching — astrological ontology notes)
2026-01-11  sema: 1 commit
2026-01-13  aski-core repo created (no commits until April — likely placeholder)

            *** INFLECTION POINT 1: AI-ASSISTED CODING SPIKE ***
2026-02-18  Mentci-AI created: 3 commits
2026-02-20  Mentci-AI: 117 commits IN ONE DAY — clearest evidence of AI-agent-driven work
2026-02-21  Mentci-AI: 43 commits
2026-02-22  Mentci-AI: 90 commits
2026-02-23  Mentci-AI: 52 commits
2026-02-25  Mentci-AI: 37 commits
2026-02-27  Mentci-AI: 56 commits
2026-03-01  Mentci-AI: 30 commits ... sustained 15-35/day through March 20

2026-03-05  Mentci v1 predecessor system: mentci-box, samskara, noesis, criome-rt, CriomOS-v2
            and a dozen micro-repos created in a single burst

2026-03-16  Mentci-v1 workspace Nix flake created (90 commits, active to Apr 6)
2026-03-24  sema repo pushed to GitHub (carries 2019-2026 history)
2026-03-26  mentci-archive created: 748-commit main workspace for aski/noesis/samskara
            2 commits on Mar 26; 3 commits Mar 26-28; then resumes Apr 6...

            *** PREDECESSOR ERA PEAK ***
2026-04-06  mentci-archive: 15 commits; ramps to 8-27/day through Apr 22
2026-04-07  nexus-spec-archive: 27 commits on Apr 7 (aski relational dialect)
2026-04-13  aski toolchain repos: askic, synth-core, corec, veric — dense commit days
2026-04-16  aski-core: 9 commits; 21 on Apr 17; 19 on Apr 19 (the aski language rewrite)
2026-04-22  mentci-archive: last commits (Apr 22) — predecessor work surface closes

            *** INFLECTION POINT 2: ARCHITECTURE RESET / MAIN-LINE BIRTH ***
2026-04-23  CriomOS created with "canonical rewrite" first commit — replaces criomos-archive
            nexus created: 17 commits on Apr 25, 9 on Apr 26, 14 on Apr 27
            criome: active (was initialized 2024-05-28 but dormant until now)
            signal created: 75 total commits starting Apr 25
            sema: 3 commits Apr 25, 8 on Apr 27 — reactivated for new stack

2026-04-25  Dense multi-repo day: nexus (9 commits), criome (doc storm), sema (3 commits)
2026-04-29  mentci-lib, mentci-egui created (new mentci — different from predecessor)

2026-05-06  *** Primary workspace initialized (jj init) ***
            67 jj commits in week 18 (May 4-10)
2026-05-07  persona started: "scaffold core state contract"
2026-05-12  persona: 20 commits; 8 on May 13; 9 on May 14; 15 on May 15; 18 on May 16; 20 on May 17
            (dense burst: Persona component architecture being built)
2026-05-22  persona: 16 commits; 18 on May 23 (second burst)

            *** INFLECTION POINT 3: SCHEMA-DERIVED STACK ***
2026-05-26  spirit created: 4 commits May 26, 13 on May 27, 16 on May 30
            schema-next, nota-next, schema-rust-next all created May 26
2026-05-27-31  spirit: 13-16 commits/day
2026-06-01-08  spirit: 5-8 commits/day; schema-next/nota-next active

            *** SCHEMA BURST: MOST INTENSE SINGLE-REPO PERIOD ***
2026-06-09  spirit: 13 commits
2026-06-10  spirit: 18 commits
2026-06-11  spirit: 19 commits (peak)
2026-06-12  spirit: 18 commits
2026-06-13  spirit: 13 commits
2026-06-14  spirit: 7 commits ... through June 22 (9 commits)
2026-06-15  CriomOS: 16 commits (platform work continues)
2026-06-17  criome: 12 commits (authentication layer intensive)
2026-06-18  criome: 7 commits; CriomOS: 11 commits
2026-06-19  criome: 5 commits; CriomOS: 11 commits
2026-07-01  listener repo created (STT component); claude-answers created
            Current state: ~10 repos pushed today
```

Primary workspace jj commit volume by week:
- Week 18 (May 4-10): 67 commits
- Week 19 (May 11-17): 38 commits
- Week 20 (May 18-24): 26 commits
- Week 21 (May 25-31): 79 commits
- Week 22 (Jun 1-7): 75 commits
- Week 23 (Jun 8-14): 2 commits
- Week 25 (Jun 22-28): 2 commits
- Week 26 (Jun 29-Jul 5): 11 commits (in progress)

---

### 4. Main-Line and Predecessor Picks

**MAIN LINE: The Persona / Criome Stack**

Candidate: the multi-repo Rust system centered on `persona`, `spirit`, `sema`, `nexus`, `signal`, `criome`, and the `CriomOS` platform layer, plus the full Signal/MetaSignal contract family.

Evidence:
1. ARCHITECTURE.md (primary workspace, §0.5) states explicitly: "What the workspace is building: Persona — a meta-AI system that organises models into a structure emulating human intelligence, animated by persona-spirit."
2. The system-level name is "the Criome stack" (ARCHITECTURE.md §0.7).
3. `protocols/repos-manifest.nota` (the authoritative inventory) classifies 100+ repos as `Active` and maps them to families: Persona, Criome, Signal, MetaSignal, Schema, Sema, Nota, CriomOS — all forming a single unified system.
4. `protocols/active-repositories.md` explicitly calls out "the active Persona / Sema / Signal / Nexus / NOTA stack" as the current core.
5. All these repos are still receiving commits as of today (2026-07-01).
6. Most commit-dense active repos: spirit (265 commits, May-July), persona (199, May-July), CriomOS (413, April-July), criome (152, with dense bursts June 2026).
7. The apex repo `persona` started May 6-7, 2026, and has been the declared meta-repo for the whole system since.

Alternatives considered:
- `spirit` alone: most commit-dense single repo (265 commits), but it is one component ("intent store") of the larger Persona system, not the whole system.
- `schema-next`/`nota-next`: the most recently intensively developed subsystem (Inflection 3), but they are a layer of the same Persona/Criome stack, not a separate flagship.

**PREDECESSOR: Mentci v1/v2 — aski / noesis / samskara system**

Candidate: the system built February-April 2026, centered on the `mentci-archive` workspace (748 commits, March-April 2026), using the `aski` language, `samskara` (datalog agent, CozoDB), `noesis` (capnp RPC harness), and `Mentci-v1` (Nix workspace).

Evidence:
1. Repository names: `mentci-archive`, `lojix-archive`, `nexus-spec-archive`, `aski-archive`, `Mentci-v1` — all carry the "archive" marker, the canonical retirement signal in this codebase.
2. GitHub descriptions explicitly use "archive": "Archived first-generation CriomOS deploy CLI" (lojix-archive); "Mentci — Sema/Noesis workspace" (mentci-archive).
3. The `mentci-archive` repo has 748 commits (March-April 2026) and was the main work surface before being abandoned April 22, 2026.
4. criome's ARCHITECTURE.md early commits (April 23-25) explicitly reference "mentci-next renamed mentci" and "canonical rewrite" — signaling the transition away from the predecessor.
5. The transition date is precise: mentci-archive closes April 22; CriomOS "canonical rewrite" and nexus creation happen April 23. The architecture reset is a one-day inflection.
6. `Mentci-v1` (90 commits) and `Mentci-AI` (164 commits) are the workspace and Nix-config layers of the predecessor system.

Alternatives considered:
- `sema` (the 2019 project) as predecessor: `sema` is not a predecessor in the sense of being replaced — it is the COMMON THREAD running from 2019 through the predecessor era and into the main line. The typed storage concept in `sema` was carried forward, not replaced. It is better characterized as "the persistent substrate" than "the predecessor."
- `criomos-archive` (2023) as the deepest predecessor: this predates the AI era entirely and was replaced by `CriomOS` (canonical rewrite, April 23, 2026). It is a valid predecessor in the OS-platform lineage, but not the project that directly preceded the current flagship in the AI-coding era.
- The `Mentci-AI` repo alone as predecessor: it is the FIRST AI-assisted project (the Feb 20 spike), but it is the Nix-config layer, not the main code. The real predecessor work surface is `mentci-archive` (the Rust/aski codebase, 748 commits).

---

### 5. Targeted Source List for Deeper Workers

**Main line — reading list:**

| Surface | Path | Priority |
|---|---|---|
| Workspace architecture | `/home/li/primary/ARCHITECTURE.md` | Read first — complete system topology, vocabulary, patterns |
| Repos manifest | `/home/li/primary/protocols/repos-manifest.nota` | Authoritative repo inventory with families and lifecycle |
| Active repos attention map | `/home/li/primary/protocols/active-repositories.md` | Today-vs-eventual distinctions, per-repo narratives |
| persona apex architecture | `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` | Top-level wiring of the stack |
| spirit architecture | `/git/github.com/LiGoldragon/spirit/ARCHITECTURE.md` | Most actively developed single repo; intent store; schema-derived stack exemplar |
| criome architecture | `/git/github.com/LiGoldragon/criome/ARCHITECTURE.md` | BLS auth daemon; the stack's core; has the most detailed commit history narrative |
| nexus architecture | `/git/github.com/LiGoldragon/nexus/ARCHITECTURE.md` | Typed semantic text vocabulary / NOTA runtime |
| sema architecture | `/git/github.com/LiGoldragon/sema/ARCHITECTURE.md` | Typed storage kernel (redb + rkyv) |
| schema-next architecture | `/git/github.com/LiGoldragon/schema-next/ARCHITECTURE.md` | Schema-derived stack engine |
| CriomOS architecture | `/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md` | NixOS platform layer |
| signal architecture | `/git/github.com/LiGoldragon/signal/ARCHITECTURE.md` | Wire contract vocabulary |
| lore AGENTS.md | `/git/github.com/LiGoldragon/lore/AGENTS.md` | Cross-workspace agent discipline (cited as canonical in primary ARCH) |

**Date ranges worth a dedicated commit dive (main line):**
- 2026-04-23 to 2026-04-28: Architecture reset week — nexus, CriomOS, signal, criome, sema all started or restarted here
- 2026-05-06 to 2026-05-23: Persona burst — the component-daemon architecture being built
- 2026-05-26 to 2026-06-13: Schema-derived stack wave — spirit, schema-next, nota-next, schema-rust-next
- 2026-06-09 to 2026-06-29: Most intensive single-repo work (spirit 13-19 commits/day); criome authentication layer

**Predecessor — reading list:**

| Surface | Path / Source | Notes |
|---|---|---|
| mentci-archive | GitHub: LiGoldragon/mentci-archive | NOT locally cloned. 748 commits, Mar 26 - Apr 22. Main predecessor work surface. |
| Mentci-AI | GitHub: LiGoldragon/Mentci-AI | NOT locally cloned. 164 commits, Feb 18 - Mar 20. NixOS config layer. |
| Mentci-v1 | GitHub: LiGoldragon/Mentci-v1 | NOT locally cloned. 90 commits, Mar 16 - Apr 6. Nix workspace tying it together. |
| nexus-spec-archive | GitHub: LiGoldragon/nexus-spec-archive | NOT locally cloned. 26 commits, Apr 7 - May 30. The aski relational dialect. |
| lojix-archive | GitHub: LiGoldragon/lojix-archive | NOT locally cloned. 51 commits. First-gen deploy CLI. |
| sema (2019-2025 history) | `/git/github.com/LiGoldragon/sema` | Locally cloned; `git log --before=2026-01-01` to see the pre-AI history (22 commits) |

**Date ranges worth a dedicated commit dive (predecessor):**
- 2026-02-18 to 2026-03-20: Mentci-AI spike — the first AI-coding burst (164 commits including 117 on Feb 20)
- 2026-03-26 to 2026-04-22: mentci-archive peak — 748 commits over 28 days (~27/day peak Apr 7-15); the aski/noesis system being built

---

### 6. Observations vs Interpretations vs Unknowns

**OBSERVATIONS (directly verified):**

- `/home/li/primary/repos/` is empty (ls verified). `/home/li/primary/private-repos/` does not exist.
- Canonical clone location is `/git/github.com/LiGoldragon/` per ARCHITECTURE.md §3 and confirmed by file inspection.
- Primary workspace has exactly 300 jj commits, all in May-July 2026 (initialized May 6, 2026 per `jj log --tail`).
- Mentci-AI GitHub repo has 117 commits on 2026-02-20 (verified via `gh api` paginate + sort + uniq -c).
- mentci-archive has 748 commits total; active March 26 - April 22, 2026 (verified via gh API).
- sema local repo has commits going back to 2019-11-06 (git log --reverse) with author "li" throughout.
- CriomOS first commit is 2026-04-23 with message "canonical rewrite with blueprint + NixOS modules" (git log --reverse).
- nexus created 2026-04-23, 85 total commits, densest days April 25-27 (17, 9, 14).
- spirit repo: 265 commits, May 26 - July 1, 2026; most active June 9-13 (13-19/day).
- persona repo: 199 commits, May 6 - July 1; most active May 12-17 and May 22-23.
- `protocols/repos-manifest.nota` (read directly) names 100+ repos as `Active`, lists `persona-pi`, `WebPublish`, `AnaSeahawk-website` as `Deprecated`.
- `protocols/active-repositories.md` (read directly) labels the current system "the active Persona / Sema / Signal / Nexus / NOTA stack."
- ARCHITECTURE.md (read directly) states: "What the workspace is building: Persona — a meta-AI system that organises models into a structure emulating human intelligence, animated by persona-spirit."

**INTERPRETATIONS (inferences from evidence):**

- The Feb 20, 2026 burst (117 commits in one day in Mentci-AI) marks the start of AI-assisted coding, not "late January." The brief says "late January / early February" but the earliest spike found is February 18-20. If there were earlier AI-assisted commits, they are not reflected in any GitHub repo active before Feb 18.
- The April 23-25, 2026 transition from aski/noesis/mentci-archive to nexus/CriomOS/signal represents a deliberate architectural reset, not organic evolution — the "canonical rewrite" language in CriomOS's first commit and the immediate silence in mentci-archive (closed April 22) are strong signals.
- The `sema` repo is a carrier of continuous identity: it bridges 2019 → predecessor era → main line. It is not "replaced" by either transition; it is the persistent substrate.
- `mentci` in the current system (created June 18, 2026) shares a name with the predecessor `mentci-archive` but is a completely different codebase ("programmable human approval daemon" vs. the old aski-based workspace).
- The `criome` repo initialized 2024-05-28 with a single `(init)` commit was almost certainly a placeholder; real development started April 2026. The two-year gap between init and substantive commits supports this.

**UNKNOWNS (not checked or unresolvable from available evidence):**

- Commit counts for most of the ~70 locally cloned signal-* and meta-signal-* repos (did not iterate all; only checked a representative sample).
- Whether there were AI-assisted commits before February 18, 2026 in repos not yet on GitHub (private/local-only repos that were later pushed or deleted).
- Content of private repos: `keel`, `assistant-reports`, `counselor-reports`, `schema-core`, `mentci-mcp-gateway`, `aski-lib`, `aski-cli`, `nix-hash-patcher` were not inspected (not cloned locally based on checks).
- Full commit breakdown for many predecessor repos (mentci-archive daily histogram was only available monthly via `gh api`; I could not get full per-day data without additional pagination).
- The `worktrees/` directory at `/home/li/worktrees/` contains `lojix-holistic-test-cluster`, `criome-authorization-submit-stream`, `github.com`, `primary-skill-runtime-reconcile`, `specified-schema-ir-poc` — these appear to be feature worktrees or JJ workspace alternates; their commit counts and relationship to the main repos were not inspected.
- Whether `maisiliym` (Nix, 2022, no description) is a predecessor to criomos-archive or unrelated — not checked.
- The `aski-core` repo was created 2026-01-13 but has no commits before April 16 (all 64 commits land April 16-20). Whether it was a very early empty placeholder or a force-push that erased earlier history is unresolved.