# Workspace Agent Model

I now have complete, directly-grounded coverage of every key question. Here are my structured findings.

# Agent-Operating Model of `/home/li/primary` — Situational Map

Scope: read-only reconstruction of the workspace + agent-operating model. All claims cite a path; FACT = literally stated in a doc/command output, INFERENCE = my interpretation. No files written (per brief). Private/personal substance excluded.

## 1. The operating model in brief

`primary` is a coordination *workspace*, not a component — it "owns discipline, protocols, skills, reports, and the authoritative inventory of active code repos" and "ships no code" (`/home/li/primary/ARCHITECTURE.md` §top, §3). Everything that ships lives in `/git/github.com/LiGoldragon/<repo>`. The workspace is described as "the apex of the agent-discipline graph" (`ARCHITECTURE.md` §0). Its whole job is to hold the rules under which agents build the actual software stack ("Persona / Criome stack").

### 1a. Psyche / Spirit / Intent / Matter

FACT (`AGENTS.md` §Intent; `ARCHITECTURE.md` §0.5 "The intent layer"; `.claude/skills/intent-log/SKILL.md`):
- "The psyche is the human." Only the psyche is a source of new intent; "agent messages and agent-written files are not psyche."
- Intent is *primordial and rare*: "the default response to a psyche utterance is not to capture." When intent is unclear/absent/contradicted, agents must ask, not infer — "inferring intent the psyche did not state is forbidden."
- **Intent vs. Matter split**: capture through **Spirit** only a statement that is `directive, durable, and universal`, and never private/personal to public Spirit. **Matter** (single-component, architectural, tool-usage, task-state, or "instructions about operating Spirit itself") goes to "code, docs, tracker items, or skill source."
- Intent classification kinds are deployed enum variants: `Decision`, `Principle`, `Correction`, `Clarification`, `Constraint` (`intent-log/SKILL.md` §Classification).
- The deployed **Spirit store** is "the raw psyche-statement log and the sole intent substrate"; supersession is always explicit and only the psyche can supersede (`ARCHITECTURE.md` §0.5).
- Capture is incomplete until it is **manifested** into the narrow guidance surface agents actually read (workspace `ARCHITECTURE.md`, repo `ARCHITECTURE.md`/code, `AGENTS.md`, README, skills, tracker) — `.claude/skills/intent-log/SKILL.md` §Manifestation; skill `intent-manifestation`.

INFERENCE: This is a deliberate two-layer memory architecture — a small append-only *intent* substrate (Spirit) sitting strictly upstream of a larger *matter* layer (docs/code/skills). "Intent precedes structure … a downstream rule that conflicts with intent loses" is stated as an invariant (`ARCHITECTURE.md` §6). The scarcity rule ("intent is rare") is an explicit guard against agents polluting the psyche's voice with their own inferences.

### 1b. Orchestration model — lanes, intent-only orchestrator, two gates

FACT — Disciplines vs. lanes (`orchestrate/AGENTS.md` §Disciplines and lanes; `ARCHITECTURE.md` §2):
- A **discipline** is a *permanent identity* (skills, authority class, persistent persona identity: mind memory + signing key). There are **nine**: `designer, operator, system-operator, system-maintainer, poet, editor, videographer, assistant, counselor`.
- A **lane** is *one throwaway work-session* named for its intent (e.g. `newLanesDesign`, `schemaWorkAudit`). It carries a discipline as metadata — in the orchestrate registry the lane's role is a NOTA vector whose **last token is the base discipline**, preceding tokens are specializations: `[NewLanesDesign Designer]`. It owns `orchestrate/<lane>.lock` and `reports/<lane>/`, and is registered/drained/retired per session.
- Roles pair advisor+executor: designer advises / operator executes; counselor advises / assistant executes for the psyche's private affairs (`ARCHITECTURE.md` §2).

FACT — the orchestrator role (`.claude/skills/orchestration/SKILL.md`):
- The orchestrator is an **intent-only lane**: "it interviews, gates, dispatches, and synthesizes. It refuses direct task work even when the psyche says 'you do it' … 'please implement'."
- Its **complete action space** is closed: psyche-facing reply, read-only Spirit query, worker dispatch, reading worker output, synthesis. "No other direct tool call is an orchestration action." It "does not inspect files, command output, links, status, or systems directly" — if ground truth is needed it dispatches a worker and reads only that output.
- **Two explicit approval gates**: (1) *Alignment locked* — no planning or dispatch before the psyche locks alignment; (2) *Method approved* — after alignment, propose worker method and wait for approval before dispatching implementation workers. "A request to implement does not bypass these gates."
- Worker/model matching is by intensity but "Do not encode concrete model names in doctrine or prompts." Select an agent type "whose generated role packet already embeds the required doctrine."

INFERENCE: The orchestrator is engineered as a pure router with no hands — a strict separation between *deciding what should happen* (orchestrator + psyche) and *doing it* (dispatched workers with their own role packets). The two gates make the human psyche the mandatory bottleneck twice per work unit, consistent with "treat the psyche as authority, bottleneck, and limited attention."

### 1c. Doctrine / skills generation system

FACT (`/git/github.com/LiGoldragon/skills/README.md` + `ARCHITECTURE.md`; `AGENTS.md` §Hard Boundaries; Explore survey):
- Skills and agent files under `.agents/`, `.claude/`, `.codex/`, `.pi/` are **generated** from `LiGoldragon/skills`. They are not hand-edited runtime surfaces.
- Generator = a Rust CLI that "assembles active modules from a NOTA output manifest and a module dependency index, then writes generated outputs into a caller-supplied workspace root." Run via `nix run github:LiGoldragon/skills#generate-skills -- <workspace-root>`; drift-checked with `check-skills`.
- Source layout: skill modules `modules/<name>/`, role modules `roles/<name>/`, archived (non-emitted) modules `skills/archive/`. Active manifest `manifests/active-outputs.nota`; dependency index `manifests/module-dependencies.nota`; legacy roster `manifests/skills-roster.nota`.
- **Module kinds**: `RuntimeSkill` (may emit as a skill), `RoleSource` (role packet root), `RoleComposition` (generator-only packet component, cannot emit as a standalone skill).
- **Output targets**: `AgentsSkill` → `.agents/skills/<name>/SKILL.md` (shared Pi+Codex); `ClaudeSkill` → `.claude/skills/<name>/SKILL.md`; role packets → `.claude/agents/<role>.md`, `.codex/agents/<role>.toml`, `.pi/agents/<role>.md`.
- Counts observed: **55** skill dirs under `.claude/skills/`; **11** generated role packets per harness surface (`.claude/agents/`, `.codex/agents/`, `.pi/agents/`): general-code-implementer, intent-curator, intent-translator, nix-auditor, operating-system-implementer, repo-scaffolder, repository-closeout, rust-auditor, scout, skill-editor, tracker-weaver.
- **Role packets embed doctrine inline**. Verified directly against `.claude/agents/scout.md`: YAML frontmatter (`name`, `description`) → `# Role - scout` (Contract/Workflow/Boundaries/Verification/Output) → `## Module - agent output protocol` → `## Module - edit coordination core` → `## Skill — spirit query`. Each packet = role source + curated included modules + dependency-expanded modules, so "routine role work starts from the packet" (`AGENTS.md` §Startup; `ARCHITECTURE.md` §2). Codex `.toml` flattens the same body into a `developer_instructions` field.
- `skills/*.md` skill bodies "are not emitted when no consuming harness needs them"; the generated *role packet* is what agents actually read (`skills/README.md`).

INFERENCE: Doctrine is compiled, not authored in place. The single source (`LiGoldragon/skills`) fans out to three harnesses (Claude, Codex, Pi) so heterogeneous agents converge on identical doctrine. Role packets are self-contained context bundles — the design intent (stated in `AGENTS.md` §Startup) is to keep the *boot contract small* and push the bulk of doctrine into on-demand packets rather than forcing every agent to read everything at startup ("reading it does not become the session's first context drain").

### 1d. NOTA — the workspace's text data format

FACT:
- NOTA is the positional, S-expression-like record format used across the workspace edges. "NOTA records are positional; use bare atoms for strings when canonical" (`AGENTS.md` §Hard Boundaries). Design discipline: positional records, named variants, bare atoms, data-in-records (`.claude/skills/nota-design/SKILL.md`).
- It is the **text projection at human/agent edges**, not the inter-component wire: "No NOTA between components. Daemons exchange binary protocol data; the CLI is the translation/debugging surface" (`ARCHITECTURE.md` §"Wire and identity discipline"). Schema-emitted Rust types and NOTA renderings are "two projections of one symbol-path identity space."
- Concrete uses observed: the repos inventory manifest is NOTA (`protocols/repos-manifest.nota` — one `(Repo <name> <remote> (Family …) <kind> <lifecycle> <doctrine-home> [flags])` per repo); the `orchestrate` CLI takes "exactly one NOTA request and prints exactly one NOTA reply" (`orchestrate/ARCHITECTURE.md`); the `spirit` CLI takes inline NOTA (`.claude/skills/spirit-query/SKILL.md`); lane registration uses NOTA vectors (`orchestrate/AGENTS.md`).

INFERENCE: NOTA is the workspace's universal human-readable projection layer — one grammar spanning config manifests, CLI request/reply, and intent records — while typed binary (rkyv) is reserved for daemon-to-daemon traffic. It is the "text form where the idea language is expressed" (schema is a NOTA dialect, per `active-repositories.md` schema-next row).

### 1e. Coordination mechanisms

FACT (`orchestrate/AGENTS.md`, `orchestrate/ARCHITECTURE.md`, `AGENTS.md`):
- **Orchestrate claims**: before editing shared files/repos, claim exact paths via the `orchestrate` daemon-backed CLI (`orchestrate "(Claim (<lane> [(Path …)|(Task …)] [reason]))"` / `(Release <lane>)`). The daemon `orchestrate-daemon` owns state in `orchestrate/orchestrate.redb`; `orchestrate/<lane>.lock` files are **read-only projections** (gitignored runtime state — `.gitignore` lines 39-44). Two scope kinds: path locks (nested/equal overlap) and task locks (exact-match).
- **Lock narrowly, never the whole space** (psyche record 2586): claim only specific files, never `/home/li/primary`; over-locking is named the root cause of "branch-dancing on primary." Component migrations lock one component at a time (record `cb0j`).
- **Version control**: on primary, work on `main` directly with `jj` (Jujutsu, colocated Git). "No raw git except documented escape hatches." Every description-taking jj command uses an inline message (never opens an editor). **"Commit the whole working copy eagerly and impersonally"** (records 2589, 2620) — janitorial full-copy commits keep history linear and prevent forked bases.
- **Reports are exempt from the claim flow** when written in the lane's own `reports/<lane>/`. A lane writes only its own directory. On drain: every idea routes to exactly one of intent (Spirit) / work (a bead) / abandon; the report directory is deleted and one row is appended to `protocols/retired-lanes.md`.
- **Work tracking (beads)**: `.beads/` is a **transitional** store, "never a claim scope," any agent may create/update/close at any time. Beads use topic labels; pick by topic affinity, not prescribed lane (psyche 2026-05-19). Destination is the typed `signal-mind` / `mind.redb` work graph ("do not add new BEADS integrations").
- **Worktrees**: when a local repo/worktree is owned by another agent, work from `main` in an isolated feature worktree and file a bead; register worktrees via `meta-orchestrate "(RegisterWorktree …)"`.
- **Repos inventory**: `protocols/repos-manifest.nota` is the single source of truth for which repos exist and their status; a coverage run filters `lifecycle = Active` and iterates `/git/github.com/LiGoldragon/<name>` directly. The `repos/` symlink index is retired (`ARCHITECTURE.md` §3).

## 2. Design principles this model encodes

- **Intent is upstream of everything; ask, never infer** — FACT (`AGENTS.md` §Intent; `ARCHITECTURE.md` §6 invariant "Intent precedes structure").
- **Separate the human's voice (intent) from the machine's structure (matter)** — FACT (`AGENTS.md` §Intent; `intent-log/SKILL.md`).
- **Orchestrator has no hands; workers have no authority** — closed action space + two approval gates — FACT (`orchestration/SKILL.md`).
- **Doctrine is compiled from one source and fanned out to all harnesses** — FACT (`skills/README.md`; `AGENTS.md` §Hard Boundaries).
- **Keep the boot contract tiny; push bulk doctrine into on-demand role packets** — FACT (`AGENTS.md` §Startup).
- **Ephemeral session identity (lane) carries a persistent identity (discipline)** — FACT (`orchestrate/AGENTS.md`).
- **Lock narrowly, commit everything, work on main** — FACT (`orchestrate/AGENTS.md`; psyche records 2586/2589/2620).
- **Chat/harness output is the default surface; reports only when the file is the working surface** — FACT (`AGENTS.md` §Output; `reporting` skill).
- **Typed binary between daemons; NOTA only at the human/agent edge; schema is source of truth** — FACT (`ARCHITECTURE.md` §"Wire and identity discipline").
- **Clarity > correctness > introspection > beauty; no backward-compat for systems being born; push-not-poll** — FACT (`ARCHITECTURE.md` §0.5).
- **"Today vs. eventually" named distinctly** (e.g. `sema`/`Sema`, `criome`/`Criome`) — FACT (`ARCHITECTURE.md` §0.5).
- INFERENCE: the whole design treats *agent context as the scarce resource* — small boot contract, embedded packets, short identifiers ("one token per character"), report-drain discipline, and delegation all optimize for keeping any single agent's context lean.
- INFERENCE: the model is being built to eventually *replace its own file-based coordination with typed daemons* — lock files → `orchestrate.redb`; beads → `signal-mind`; intent files → Spirit store. The workspace is bootstrapping the very system (Persona) that will run it.

## 3. Evolution note (May–Jul 2026)

FACT (jj history in `/home/li/primary`):
- Initialized **2026-05-06** (`7063610a Initialize primary workspace`); day-1 commits created `ESSENCE.md` ("project-agnostic intent doc"), bootstrapped skills (`autonomous-agent, skill-editor, stt-interpreter`), and ran `bd init`.
- **~3,066 revisions** total (not ~300 as the brief stated — flagging the discrepancy), heavily front-loaded: **1,615 in May, 1,434 in June, 16 on Jul 1** — ~50-60 commits/day, consistent with the "commit the whole working copy eagerly" discipline and many concurrent lanes.
- Milestone arc (verbatim first-lines):
  - `628b163d newLanesDesign: cut workspace to the dynamic session-lane model` — introduced the lane model.
  - `bc0a3b5d pin generated role packet V1` / `65268157 report role packet V1 landing` — role-packet doctrine generation landed.
  - `0fd75c69 … intent files deprecated — all intent driven from Spirit`; `a8e9336b doctrine: eliminate ESSENCE.md + workspace INTENT.md, rehome into ARCHITECTURE.md §0.5` — the intent layer moved off static files onto the Spirit store; ESSENCE.md/INTENT.md are now **gone** (confirmed absent).
  - Spirit GC: `d3e2fd34 archive-first removal of 631 legacy MATTER records`, `8048683e archive + remove 739 zero-cert records` — the intent substrate was pruned of matter.
  - `b85d696e protocols: stand up authoritative repos-manifest.nota + supersede overlapping inventories` then `ff0d10c1 workspace: retire repos/ symlink index in favor of manifest` — inventory moved from symlinks/`RECENT-REPOSITORIES.md` to the NOTA manifest.
  - Recent (Jul 1): `601d6368 regenerate skills for tracker lock retries`, `3faf4cc3 regenerate skill runtime surfaces` — ongoing generator regeneration.

INFERENCE: The trajectory is *consolidation of scattered coordination surfaces into single authoritative substrates*: many intent files → one Spirit store; many inventory files → one manifest; hand-edited skills → one generator; ad-hoc roles → generated packets; file locks → one daemon. The workspace has been aggressively refactoring its own operating model roughly every few days.

## 4. Current state and visible open threads / tensions

- **`lore/AGENTS.md` is stale vs. primary** — FACT: `/git/github.com/LiGoldragon/lore/AGENTS.md` (lines 13-14, 78) still lists `ESSENCE.md`/`INTENTION.md` as the required-reading upstream intent doc "living at the workspace's root (e.g. `~/primary/ESSENCE.md`)", but primary eliminated those files and rehomed the content into `ARCHITECTURE.md §0.5`. The "canonical cross-workspace contract" (`ARCHITECTURE.md` §4) has not caught up with the workspace's own evolution.
- **Report/artifact accumulation vs. the drain discipline** — FACT: `reports/` holds ~15 lane directories and `agent-outputs/` holds ~90 entries, while `retired-lanes.md` records only **1** retired lane. Additionally ~15 loose audit `.md` files sit at the workspace *root* (e.g. `lojix-*.md`, `context.md`, `criomos-*.md`) rather than under `reports/<lane>/`. INFERENCE: the "drain and retire → delete the directory, append one row" discipline (`orchestrate/AGENTS.md` §Drain and retire) is not keeping pace with production; artifacts are accumulating faster than lanes retire.
- **Two overlapping role vocabularies** — FACT: `orchestrate/AGENTS.md` defines **9 disciplines**; the generator emits **11 role packets** with different names (scout, rust-auditor, intent-curator, …). INFERENCE: the persistent-discipline model and the generated-worker-packet model are not a 1:1 mapping; the relationship between them is not spelled out in one place.
- **Transitional substrates mid-migration** — FACT: BEADS is explicitly "transitional" → `signal-mind`/`mind.redb` (`ARCHITECTURE.md` §1, `orchestrate/AGENTS.md`); `orchestrate/roles.list` is a "transitional seed"; `repos/` holds "residual local checkouts … pending migration"; `RECENT-REPOSITORIES.md` is a "superseded stub." Several `.redb` backups exist (`orchestrate.redb.pre-v3-*`, `.pre-nota-next-*`), evidence of in-place schema migrations.
- **Deprecated/retired items** — FACT (`repos-manifest.nota`): `persona-pi`, `WebPublish`, `AnaSeahawk-website` are `Deprecated` (remote archived + local deleted); `OwnerSignal` is deprecated in favor of `MetaSignal` (`ARCHITECTURE.md` §0.6). Naming migrations still settling: "Menchie"→`mentci`, "engine-manager"→`Persona`, `sim`→`sema`.
- **"nota signal" vocabulary "proposed but not yet hardened"** — FACT (`ARCHITECTURE.md` §"signal the noun is ambiguous").
- **Much of the isolation model is design-only** — FACT: role-space (per-role Git sub-workspaces, SSH-key-gated push) is "a recorded design direction — much of it is not yet implemented" (`ARCHITECTURE.md` §2).

## 5. Explicit UNKNOWNS / not checked

- **Spirit store contents** — I ran no `spirit` queries; the actual intent records (numeric IDs like 2586, `cb0j`, etc.) referenced in doctrine were not inspected. Private/elevated-privacy intent is out of scope and was not touched.
- **Generator internals** — I read `skills/README.md` + the survey's read of `skills/ARCHITECTURE.md`, but did not inspect the Rust `src/` or the manifest NOTA files (`active-outputs.nota`, `module-dependencies.nota`) directly, so the exact module→packet composition rules are known only from prose.
- **Live daemon state** — I did not query the running `orchestrate-daemon` (`Observe Lanes/Roles/Worktrees`); active-lane facts come from filesystem projections (`orchestrate/*.lock`, `reports/` dirs), which may lag daemon state.
- **`mind` / `signal-mind` typed work graph** — the migration target for beads was not inspected; its readiness is unknown.
- **Whether root-level `.md` audit files are intentional** — they may be an authorized system-operator/lojix working convention rather than a discipline violation; I did not find a doc authorizing root-level (non-`reports/`) report placement.
- **Commit-count discrepancy** — brief said "~300 jj commits"; actual `jj log -r 'all()'` count is 3,066. I did not reconcile which figure the brief intended (possibly counted a different repo, or Git-visible non-empty commits only).

Key files for a downstream synthesis worker: `/home/li/primary/AGENTS.md`, `/home/li/primary/ARCHITECTURE.md` (esp. §0.5, §0.6, §2, §3, §6), `/home/li/primary/orchestrate/AGENTS.md`, `/home/li/primary/orchestrate/ARCHITECTURE.md`, `/home/li/primary/protocols/repos-manifest.nota`, `/home/li/primary/protocols/retired-lanes.md`, `/home/li/primary/.claude/skills/orchestration/SKILL.md`, `/home/li/primary/.claude/skills/intent-log/SKILL.md`, `/home/li/primary/.claude/agents/scout.md`, `/git/github.com/LiGoldragon/skills/README.md`, and `/git/github.com/LiGoldragon/lore/AGENTS.md` (stale).