# Predecessor & Mentci Era

I have enough grounded evidence. Here are the structured findings.

---

# Predecessor System Reconstruction (Feb–Apr 2026, LiGoldragon)

## 0. Method and a data correction

I shallow/full-cloned the target repos into `/tmp/pre-<name>` and read entry docs + commit narratives. All GitHub repos are under `LiGoldragon/`. Commit messages are written in a NOTA-style positional tuple format and are unusually narrative (each carries an `evolution`/`drift`/`violation` rationale field), which makes the arc reconstructable from `git log` alone.

**Correction to the brief:** the two commit counts are swapped. `git log` shows **Mentci-AI = 748 commits (2026-02-18 → 2026-03-20)** and **mentci-archive = 164 commits (2026-03-26 → 2026-04-23)**. The 117-commit Feb-20 burst is in Mentci-AI.

**Key dating anomaly:** `aski-core` was created **2026-01-13** (`gh repo view`), a month before the Feb "first AI-coding" burst — unexplained (see Unknowns).

---

## 1. What the psyche was building (the through-line)

FACT. It was never one thing; it was a **stack** with a single obsession: **SEMA — a typed binary format where "domain variants ARE the bytes, no strings, no unsized data, zero-copy, deterministic"** (`/tmp/pre-mentci-archive/RESTART-CONTEXT.md:33-40`; `/tmp/pre-samskara/CLAUDE.md:26-35`). Everything else (the aski text language, CozoDB, capnp, nexus, criome, lojix) was scaffolding to make SEMA real and to let LLM agents operate on it efficiently.

FACT. The thesis behind SEMA is **token/cognition efficiency for LLMs**: "moving from text-based Aski to fully specified structured trees of enumerators, LLM cognition becomes two to three orders of magnitude more efficient than text" (`/tmp/pre-Mentci-AI/Library/architecture/AskiPositioning.md:22`).

FACT. **Astrology was baked into the ontology**, not decorative. Samskara's world model is "rooted in astrological category theory: Solar/Lunar polarity… the subdivision chain 2→3→7→12→36→72→360" (`/tmp/pre-Mentci-v1/Core/ARCHITECTURE.md:41-46`). `veri-core` (originally `sema-core`) init commit: "three pillars — Phase/Dignity + Astrality (15 domains, Young measures, Chaldean decans, Hellenistic rulerships) + Structure" (commit 2026-03-24). Mentci-AI shipped "Ecliptic Chronographic Versioning" — releases tagged with zodiac degrees, e.g. `release: v0.12.1.15 (♓︎ 1° 15')` (Mentci-AI log, 2026-02-19).

So: **an agent runtime + an OS + a sema ontology, all at once** — with the sema format (astrologically-typed) as the destiny and the LLM-agent as the primary consumer.

---

## 2. Dated narrative arc

**Phase 1 — Feb 18-20 · Mentci-AI (748 commits).** "A Nix-and-Rust AI daemon workspace built around Sema Object Style, JJ-first version control" (`/tmp/pre-Mentci-AI/CLAUDE.md:18`). The Feb-20 burst introduced the `.aski` DSL (`.aski-flow`, `aski-fs`, `aski-astral`), astrology library, and criome "jail" isolation (`MentciBoxIsolation.md`, `JailCommitProtocol.md`). Early churn included a "full transition to Clojure (Babashka)" (2026-02-19) later abandoned for all-Rust. aski was already split into **lojix** (technical variant) and **sajban** (natural-language variant) (`AskiPositioning.md:24-29`).

**Phase 2 — Mar 5-16 · datalog substrate.** `samskara` created 2026-03-05: "the first sema world… an agent that exists entirely within typed relations" on **CozoDB** (`/tmp/pre-samskara/CLAUDE.md:1-16`). `Mentci-v1` (2026-03-16) formalized a **two-agent model**: Samskara (pure datalog) + Lojix (DSL transpiler) that "never interact directly. All communication flows through shared datalog relations" in `samskara-lojix-contract` (`/tmp/pre-Mentci-v1/Core/ARCHITECTURE.md:9-32`). `lojix-macros` derived typed Rust from the datalog schema (`domain!`/`product!`/`morphism!`/`fold!`). The datalog choice is argued at length in `/tmp/pre-Mentci-v1/Drafts/Datalog-LLM-Perfect-Match.md` (see §3).

**Phase 3 — Mar 20-24 · criome runtime + binary wire.** `criome-rt` (2026-03-20): "process jails using Linux network namespaces with optional WireGuard tunnels" (`README`). `CriomOS-v2` (2026-03-20): "standard runtime substrate… Pure Nix infrastructure." `noesis` (2026-03-24): a **capnp RPC harness replacing MCP JSON-RPC** — "typed binary agent harness" (repo desc), proven round-trip "50 domain enums, 396 variants, 2.9MB binary," culminating in a "pure binary harness — after text preamble ALL messages are raw capnp bytes" (noesis log, 2026-03-25).

**Phase 4 — Mar 26 → Apr 21 · the aski compiler era (mentci-archive = "Mentci, the sema workspace").** Mentci was created "sema/noesis workspace flake — independent from samskara old stack" (mentci-archive first commit). This is where the bulk of predecessor design lives. It became a **10-stage compiler pipeline**: `corec → synth-core → aski-core → veri-core → askicc → askic → veric → domainc → semac → rsc → askid` (`/tmp/pre-mentci-archive/RESTART-CONTEXT.md:86-100`). The syntax churned violently — **v0.13 → v0.14 → v0.15 → v0.16 → v0.17 → v0.18 → v0.19 → v0.20 → v0.21 in ~11 days** (Apr 10-21; `session-history.md` + mentci-archive log), ending at **v0.21 "Identity-is-Location"** where the filesystem encodes identity (`RESTART-CONTEXT.md:43-62`). Repos were renamed repeatedly (`aski-rs→semac`, `aski-core→synth-core`, `aski→aski-core`, then new `LiGoldragon/aski`) and the org consolidated `Criome/* → LiGoldragon/*` (2026-04-20).

**Phase 5 — Apr 7-8 · nexus is born.** `nexus-spec-archive` created 2026-04-07: "aski schema + nexus message syntax with assert/observe/mutate… language design needed a home" (first commit). `arbor` (prolly-tree versioning over rkyv+blake3) added 2026-04-08 because "nexus database needs a versioned storage primitive."

**Phase 6 — Apr 22-23 · THE PIVOT (aski pipeline abandoned).** `NEXUS-DESIGN.md` (Apr 22) then `MIGRATION.md` (Apr 23, 916 lines — `/tmp/pre-mentci-archive/MIGRATION.md`). Mentci archived. New stack: **LLM agent → `nexus` CLI → criome → arbor → criome-store** (`MIGRATION.md:47-76`).

**Phase 7 — Apr 24-25 · the SECOND, deeper reset (the real "canonical rewrite").** `lojix` re-scaffolded as a fresh repo 2026-04-24. `aski/CLAUDE.md` banner (Apr 25): **"aski is dead." "aski was the wrong way… it was the wrong way."** — and crucially, the successor workspace `mentci-next` "does **not** treat aski as a design input" (`/tmp/pre-aski/CLAUDE.md:3-18`). nexus was rebuilt **on `nota`** (positional records), not on aski grammar (`/tmp/pre-nexus-spec-archive/README.md:1-13`, refreshed Apr 25).

---

## 3. Tech-choice rationale

- **datalog / CozoDB (samskara).** FACT. `/tmp/pre-Mentci-v1/Drafts/Datalog-LLM-Perfect-Match.md` is an explicit manifesto: datalog is "the maximal subset of logic programming that guarantees termination" → "Non-terminating queries are liveness failures… Datalog eliminates this by construction" (agent can't hang); "roughly 12 syntactic constructs… Every additional construct is an opportunity for hallucination"; closed-world assumption "enables action through commitment" where open-world "creates paralysis"; "An LLM generating Datalog is not programming. It is reasoning, and the database is checking its work." CozoDB specifically for unifying "relational + graph + vector… CozoDB as hippocampus" (agent memory).
- **capnp RPC replacing MCP (noesis).** FACT. Motive = get strings/JSON off the wire between LLM and world: "typed binary agent harness, capnp RPC replacing MCP JSON-RPC" (repo desc); noesis proved "bytes in, bytes out… tokenizer sees byte-level tokens" (noesis log 2026-03-25). INFERENCE: same efficiency thesis as SEMA, applied to the transport.
- **the aski DSL + compiler pipeline.** FACT. aski = "a human-readable text projection of sema… the stepping stone that makes sema visible so the system can be built" (`/tmp/pre-aski/CLAUDE.md:24-36`). It was a *frontend to author sema*; the pipeline's job was to compile `.aski` down to pure `.sema` bytes. Design principles: no keywords, delimiter-first, position defines meaning, names must be full words (`MIGRATION.md:443-469`).
- **Mentci workspace.** FACT. A multi-repo (git-submodule/symlink) coordination shell; Mentci-the-*repo* (workspace) is distinct from Mentci-the-*concept* (the planned visual human UI for sema) (`MIGRATION.md:88-90`).
- **criome runtime / CriomOS.** FACT. "What an OS is to processes, the criome is to agents" (`MIGRATION.md:73`). Concretely: network-namespace process jails + WireGuard so agent subprocesses (e.g. MCP servers) run isolated with transparent stdio (`criome-rt/README`).
- **nexus.** FACT. A messaging syntax for the LLM↔world boundary, invoked as a plain CLI (`echo '(...)' | nexus`) — deliberately **rejecting MCP's JSON-schema negotiation** ("CLI over MCP… MCP's JSON-schema negotiation is rejected," `MIGRATION.md:491`).

---

## 4. Why it was abandoned/reset — strongest evidence

This is **well-documented**, and it happened in **two nested waves**:

**Wave 1 (Apr 23, aski compiler pipeline) — `MIGRATION.md:37-43` states two reasons in priority order:**
- **(a) short-lifespan-by-design.** "Mentci was always the planned human UI for sema… Aski-as-UI was a scaffold Mentci would replace within days… Investing months in a multi-repo compiler toolchain (askic + askicc + synth + synth-core + aski-core + veric + veri-core + tree-sitter-aski + emacs modes + the v0.21 spec) for a few-day scaffold is a bad trade."
- **(b) "A database is much simpler than a parser pipeline."** "For the job aski-as-UI was doing… a database with a schema does the same thing with a fraction of the infrastructure. No grammar, no synth, no askic/askicc, no verifier, no tree-sitter. Just a schema and a store."
- Plus the workspace-noise reason: Mentci archived because it churned through "v0.15 → v0.19 → v0.20 → v0.21… multiple CLAUDE.md rewrites. The noise is no longer worth the signal" (`MIGRATION.md:31-35`).

**Wave 2 (Apr 24-25, aski *entirely*) — `/tmp/pre-aski/CLAUDE.md:3-18`:** even Wave-1's plan to *carry aski's design into nexus* was reversed. **"aski is dead… aski was the wrong way."** The banner explicitly forbids reasoning from aski axioms (Identity-is-Location, syntax-v021, the compile pipeline) to the current sema architecture, and notes the doc exists "to block aski-contamination that repeatedly crept into mentci-next/reports/061 despite multiple corrections from Li." nexus was re-based on `nota`, not aski.

**INFERENCE (strong, from state, not a single quote):** the compiler pipeline collapsed under its own weight and never produced working sema. At abandonment nearly every downstream stage was a stub: `askic` = "one-line lib.rs," `veric` = deleted/placeholder, `semac`/`domainc`/`rsc`/`askid` = "not built," and the critical-path blocker `askic-assemble` "doesn't exist" (`RESTART-CONTEXT.md:306-380`). Months of effort went into grammar versions and rkyv type-contracts; **no stage ever emitted a real `.sema` byte.** The "database is simpler" realization is the psyche noticing the pipeline was infrastructure with no output.

---

## 5. Carried-forward vs. dropped ledger

Carry-forward is corroborated by this workspace's own `AGENTS.md` (NOTA, CriomOS, lojix, component/daemon) and the loaded skill set (`component-architecture` "Signal/Nexus/SEMA runtime," `nota-design`, `operating-system-operations` "Lojix interfaces"), plus `/tmp/pre-lojix-archive/ARCHITECTURE.md` which describes the *current* three-pillar main line.

**CARRIED FORWARD**
- **SEMA** — the typed-binary format, the whole point; survives. FACT.
- **NOTA** — positional record format nexus was rebuilt on; the survivor of the "wire format" idea (`nexus-spec-archive/README.md:1-13`; this workspace's AGENTS.md "NOTA records are positional"). FACT.
- **nexus** — messaging protocol (assert/observe/mutate/shape/negate; pattern `(| |)`, bind `@`, negate `!`) survives as the query layer (`nexus-spec-archive/README.md`; current `component-architecture` skill). FACT.
- **criome / CriomOS** — runtime + OS layer survives (`criome-rt`, `CriomOS-v2`; current `operating-system-operations` skill; `lojix-archive/ARCHITECTURE.md` references live criome). FACT.
- **lojix** — CriomOS deploy CLI survives as the "forge family" human entry point (`/tmp/pre-lojix-archive` is the *current-era* lojix-cli, incl. `horizon-lib`, `nota`, `signal`, `forge`, `arca`). FACT.
- **signal contracts + component = daemon + thin CLI** — `lojix-archive/ARCHITECTURE.md:66-75` ("the signal contract… lives in signal; this CLI consumes the effect-bearing subset") matches current `component-architecture`/`contract-repo`/`micro-components` skills. FACT.
- **micro-repo / data-ownership / contract-only-coupling** — from Mentci-v1's two-agent model into current micro-component discipline. FACT/INFERENCE.
- **jj-mandatory + always-push + nexus-style commit messages** — verbatim into current AGENTS.md. FACT.
- **Phase/Dignity lattice** (Becoming→Manifest→Retired; Delusion<Uncertain<Seen<Proven<Eternal, `/tmp/pre-samskara/CLAUDE.md:11-14`) → *possibly* the current Spirit intent certainty/importance model. INFERENCE, weak — not proven.

**DROPPED**
- **The entire aski text language + compiler pipeline** (`corec`, `synth-core`, `aski-core`, `askicc`, `askic`, `veric`, `veri-core`, `domainc`, `semac`-as-compiler, `rsc`, `askid`, `tree-sitter-aski`, emacs modes) — FACT (`MIGRATION.md:17-25`; aski death banner).
- **Identity-is-Location (II-L)** and aski's syntax-v021 — FACT (aski banner forbids reasoning from it).
- **MCP / JSON-RPC** as the LLM surface — FACT (replaced by capnp, then by nexus CLI).
- **capnp RPC (noesis v1)** — FACT (noesis reset commit 2026-04-06: "clear capnp harness — rewrite in aski," then aski itself dropped).
- **CozoDB / datalog / the two-agent Samskara+Lojix model** — FACT (samskara direction "CozoDB → nexus over arbor," `/tmp/pre-samskara/CLAUDE.md:26`; storage replaced by arbor prolly-trees + criome-store). Notably **the name "samskara" was retired and made unspeakable** at Li's request (`MIGRATION.md:492`, "`samskara` is not spoken").
- **Clojure/Babashka stack** — FACT (dropped early for all-Rust, Feb 19-20).
- **Astrology-as-ontology** (Astrality pillar, Chaldean decans, Ecliptic Chronographic Versioning) — appears DROPPED from the visible current main line. INFERENCE, weak (no astrology in current AGENTS.md/skills; I did not exhaustively search the live repo).

---

## 6. Unknowns / not checked

- **The actual successor workspace `mentci-next`** — I did not clone it. Its `docs/architecture.md` §10 "Rejected framings" is named by `/tmp/pre-aski/CLAUDE.md:16-18` as the definitive rejection record; that is the single best remaining source and should be read by the synthesis worker.
- **Precise start of the current main line.** The pivot is Apr 23 (MIGRATION.md); the *deeper* "aski is wrong" break is Apr 25. Whether the current `/home/li/primary` "canonical rewrite" is Apr 23, Apr 25, or later is not pinned to a commit — I inferred it from doc dates, not from the live main-line git history (which I did not inspect; read-only scope + it wasn't in the target list).
- **`aski-core` created 2026-01-13** — a full month pre-burst. Could be an abandoned earlier experiment or a placeholder; unexplained.
- **Phase/Dignity → current Spirit certainty/importance lineage** — plausible but unproven.
- **`criome-cozo` and `criome-stored` READMEs returned empty** via API; I have only their repo descriptions ("CozoDB wrapper crate — shared DB primitives"; created 2026-03-16 / 2026-03-21).
- **Did not read** the actual `aski/spec/design.md` body, the live `nexus`/`nexus-serde`/`arbor`/`criome-store` code, or the Mentci-AI astrology docs in depth — only their pointers and summaries.
- **`veri-core`'s "Astrality" three-pillar schema** confirms astrology reached the *type foundation*, but I did not verify whether any astral domains survive in current SEMA.

**Cited local artifacts (all under `/tmp/pre-*`, cloned read-only from GitHub):** `pre-mentci-archive/{MIGRATION.md,RESTART-CONTEXT.md,session-history.md,CLAUDE.md}`, `pre-aski/CLAUDE.md`, `pre-Mentci-v1/Core/ARCHITECTURE.md` + `Drafts/Datalog-LLM-Perfect-Match.md`, `pre-samskara/CLAUDE.md`, `pre-noesis/CLAUDE.md`, `pre-veri-core/CLAUDE.md`, `pre-nexus-spec-archive/README.md`, `pre-Mentci-AI/{CLAUDE.md,Library/architecture/AskiPositioning.md}`, `pre-lojix-archive/{README.md,ARCHITECTURE.md}`, plus `gh` metadata and `criome-rt`/`CriomOS-v2` READMEs via API.