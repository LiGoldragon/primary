# Session handoff — 2026-05-06 → 2026-05-07

Date: 2026-05-07
Author: Claude (designer)

A wrap-up of two days of designer-side work in `~/primary` and
across the workspace. Written for context compaction and for
the next session (mine or another agent's) to pick up cleanly.

---

## Session summary

Started 2026-05-06 with `~/primary/` freshly initialised and an
empty memory directory. Worked through, in sequence:

1. Orientation across `~/primary/` and the 35 linked repos.
2. Drafted the **golden document** `~/primary/ESSENCE.md`
   (project-agnostic intent: clarity → correctness →
   introspection → beauty; choosing data formats; language
   instincts; documentation layers; how agents apply this).
3. Decoupled `lore/` from sema-ecosystem references; relocated
   gas-city/lojix-cli content; deleted INTENTION.md (substance
   absorbed into ESSENCE).
4. Built the **skills system** under `~/primary/skills/` —
   workspace-level skills for cross-cutting capabilities;
   per-repo `skills.md` for project-specific intent.
5. Audited the operator's persona scaffold and the
   persona-message prototype; produced design reports for the
   reducer-based messaging fabric and the WezTerm-based
   real-harness test architecture.
6. Reinforced the Rust documentation surface (ractor, testing,
   discipline); added the **language-design** workspace skill
   absorbing aski's design instincts.
7. Captured new rules as they landed: no-harness-memory,
   BEADS-is-transitional, no-`git+file://`, the `*Handle`
   pattern, tone-in-chat-replies, the
   test-script-as-named-script rule.
8. Consolidation pass (this turn): efficiency-of-instruction
   added to ESSENCE; `style.md` trimmed to toolchain
   reference; sync-façade duplication between ractor.md and
   testing.md removed.

Operator (Codex) worked in parallel through the
operator/designer lock protocol, building the orchestration
helper, the persona scaffold, persona-message, persona-wezterm,
and the real-harness test substrate.

---

## What was built — by category

### Workspace skills (`~/primary/skills/`)

| Skill | What it is | Notes |
|---|---|---|
| `autonomous-agent.md` | When to act on routine obstacles without asking | Operator added "stateful test command → named script" + "JJ-colocate first" + orchestration-claim sections; designer added "skills.md after substantive work" + edit-via-skill-editor cross-reference |
| `skill-editor.md` | Conventions for naming, location, format, cross-references of skill files | The meta-skill |
| `stt-interpreter.md` | STT mistranscription table for workspace-specific words | Includes aski-lineage caveat absorbed from ex-memory |
| `version-control.md` | jj + always-push + logical commits + standard fixes | Absorbed from autonomous-agent + lore/AGENTS sections |
| `beauty.md` | Beauty as criterion | Migrated from lore/programming |
| `abstractions.md` | Verb belongs to noun | Migrated |
| `naming.md` | Full English words | Migrated |
| `push-not-pull.md` | Producers push, consumers subscribe | Migrated |
| `micro-components.md` | One capability per crate per repo | Migrated |
| `rust-discipline.md` | Methods on types, error enums, `*Handle`, etc. | Synthesized; references lore/rust/{style,ractor,testing,rkyv,nix-packaging} |
| `nix-discipline.md` | Flake input forms; lock-side pinning; no-`git+file://`; store-path hygiene | Captures the no-`git+file://` rule from the operator-steer |
| `language-design.md` | 17 instincts when designing a notation | Distilled from aski/spec/design + ESSENCE summary |

### Per-repo skills

- `criome/skills.md` — engine intent, "criome and sema are
  meant to be eventually impossible to improve…"
- `sema/skills.md` — store intent, same deepest-value claim,
  what sema owns vs doesn't.

### Lore changes (`/git/github.com/ligoldragon/lore/`)

- **`AGENTS.md`** — rewritten project-agnostic; required-reading
  order (intent doc → this file → repo's AGENTS → ARCHITECTURE
  → skills.md); skills layer documented; tone rule in
  session-response section; index updated to include
  `nix-discipline`, `language-design`, `testing.md`.
- **`INTENTION.md`** — deleted (substance generic in ESSENCE).
- **`programming/`** — directory deleted (5 files migrated to
  workspace skills).
- **`rust/style.md`** — trimmed to toolchain reference only
  (Cargo.toml, cross-crate deps, pin strategy). ~120 lines
  down from 749. Discipline content lives in
  `skills/rust-discipline.md`.
- **`rust/ractor.md`** — extended with `*Handle` consumer-
  surface section, `pre_start` pool initialization, sync
  façade (structural side; test fixture moved to testing.md),
  `actor.get_name()` in supervisor override.
- **`rust/testing.md`** — new file. Sync façade on State,
  tests in separate files, tempfile pattern, two-process
  integration via `CARGO_BIN_EXE_*`, when to test actors
  directly.
- **`rust/rkyv.md`, `rust/nix-packaging.md`** — light edits
  for project-name decoupling.
- **`nix/basic-usage.md`** — Operational rules section
  collapsed to a pointer at `skills/nix-discipline.md`.
- **`nix/integration-tests.md`** — rewritten with abstract
  daemon names (`engine`, `frontend`, `frontend-cli`).
- **`gas-city/`, `lojix-cli/`** — directories deleted
  (content relocated to `gascity/engdocs/operating.md` +
  `engdocs/vocabulary.md`, and to `lojix-cli/docs/basic-usage.md`).
- **`jj/, dolt/, bd/, annas/, linkup/, substack/`** —
  light edits removing project-specific references.

### `~/primary/` structure changes

- **`AGENTS.md`** — refreshed to point at ESSENCE,
  lore/AGENTS, protocols/orchestration, skills/. Carries
  no-harness-memory rule, BEADS-is-transitional note.
- **`protocols/orchestration.md`** — Reports section added
  (role-owned subdirs, exempt from claim flow); Overrides
  section added (named one-job lock-bypass).
- **`reports/designer/`** and **`reports/operator/`**
  subdirectories created.
- **Memory directory** at `~/.claude/projects/-home-li-primary/memory/`
  **deleted** — no harness-dependent memory rule landed.

### Designer reports

| Report | Topic |
|---|---|
| `2026-05-06-skills-bootstrap-status.md` | Initial skills inventory + concerns |
| `2026-05-06-persona-audit.md` | Naming audit on persona scaffold (5 issues) |
| `2026-05-06-skills-roadmap.md` | Lore→skills migration plan + 5 high-leverage skill candidates |
| `2026-05-06-persona-messaging-design.md` | Big design report: typed records, one reducer, harness nodes |
| `2026-05-06-persona-message-audit.md` | Skeptical audit of persona-message prototype + round-trip scenario expansion |
| `2026-05-07-real-harness-test-architecture.md` | WezTerm-based harness test architecture |
| `2026-05-07-rust-doc-audit.md` | Rust doc audit: 4 ractor lifts + 5 gaps + discipline check |
| `2026-05-07-session-handoff.md` | This report |

---

## Key decisions / rules that landed

The non-obvious ones a fresh session needs to know:

- **BEADS is transitional substrate.** `.beads/` is used today
  for convenience; persona's typed messaging fabric is the
  destination. No persona↔bd bridge will be built. Memorialised
  in `~/primary/AGENTS.md` and `persona-messaging-design.md`.
- **No harness-dependent memory.** Memory and persistent
  agent state live in workspace files (`skills/`, `lore/`,
  `reports/`, `protocols/`, `.beads/`); never in
  Claude-specific memory dirs or any agent-private store.
- **Lore = tool reference; skills = how-we-use-it.** The
  boundary is now clean. `lore/programming/` migrated;
  `lore/rust/style.md` trimmed; `lore/nix/basic-usage.md`'s
  operational rules → `skills/nix-discipline.md`.
- **Efficiency of instruction** (added to ESSENCE this turn):
  each rule lives in one canonical place; cross-reference
  over duplication; an agent should never have to choose
  between two versions of the same rule.
- **No `git+file://` for flake inputs.** Use `github:` for
  committed forms; `--override-input path:...` for local
  iteration. Captured in `skills/nix-discipline.md`.
- **`*Handle` consumer surface** for every actor: the four
  internal pieces (`Actor` ZST, `State`, `Arguments`,
  `Message`) plus the `*Handle` external piece that owns the
  spawn result. Captured in `lore/rust/ractor.md` and
  `skills/rust-discipline.md`.
- **Tone in chat replies: state results.** Don't narrate
  process, don't apologise, don't pre-announce. The chat
  reply is for what changed and what's next; substance goes
  in reports. Captured in `lore/AGENTS.md`.
- **Operator/designer lock protocol** with `tools/orchestrate`
  helper: `claim <role> <paths> -- <reason>` before any edit;
  `release <role>` after. Reports subdirs are exempt;
  one-job overrides are explicit.
- **Override mechanism**: the user can grant a one-job
  override that bypasses the claim flow for a specific edit.
  Overrides are named at the call site; don't persist beyond
  the named scope.

---

## Operator's parallel work

Last observed (this turn): operator active on persona-message
+ persona-wezterm, "finish daemon transport and run fresh
message setup."

Earlier work landed by operator during this session:
- `tools/orchestrate` helper (the bash script for lock
  claim/release).
- `protocols/orchestration.md` (initial draft; designer added
  Reports + Overrides sections later).
- `~/primary/AGENTS.md` initial setup with operator/designer
  identity.
- `.beads/` initialisation + initial bead seeding.
- Persona scaffold (`persona/src/{schema, request, state}.rs`)
  — the audit target.
- Persona-message naive round-trip prototype.
- Persona-wezterm (the harness substrate, just spawned).
- Three operator reports: gas-city-harness-design,
  persona-core-state-machine, terminal-harness-control-research.
- Several rule-additions to `skills/autonomous-agent.md`
  (orchestration-claim, JJ-colocate, named-test-scripts,
  refined cross-reference rules).
- Migration of nota-codec dep from `git+file://` to
  `github:` (after user steer; captured the new rule into
  `skills/nix-discipline.md`).

---

## Unresolved threads

These are open as of this handoff:

1. **Verb-form vs noun-form Commands** (persona scaffold). My
   audit recommended noun-form (`HarnessDeclaration` instead
   of `DeclareHarness`); operator's scaffold uses verb-form;
   no decision yet. See `reports/designer/2026-05-06-persona-audit.md`
   §1, `reports/designer/2026-05-06-persona-messaging-design.md`
   open question 4.

2. **persona-message simplification** — audit recommended
   deleting `Authorization`, `Delivery`, lifecycle enums,
   `Object/Document`, `Check`, `Validated`, `SchemaExample`
   and `::example()` factories until they have behavior to
   drive. Operator hasn't applied the trim yet; was actively
   writing real-harness tests when last seen.

3. **The five ractor gaps** (registry, `pg` pubsub, hot-reload,
   sync-thread bridge, `pre_start` panic handling) — flagged
   in `reports/designer/2026-05-07-rust-doc-audit.md` §4.
   Wait until practice exists before documenting.

4. **Three rust-discipline expansion candidates** (default
   `#[derive]` set, generics naming, async patterns) — also
   flagged in the rust-doc-audit. Wait until practice
   supports.

5. **`primary-bmy`** bead — per-repo `skills.md` rollout for
   the ~30 repos still missing one. Designed as
   incremental, agent-driven (agents create the skill after
   substantive work in a repo). Don't batch.

6. **`primary-jwi`** bead — operator's "harden orchestrate
   helper into a typed Persona component." Operator's work.

7. **The rust-doc-audit's questions** — the user said "I like
   all your suggestions; implement them" and I did
   (4 ractor lifts, testing.md, language-design, nix-discipline,
   `*Handle` formalization, style.md trim). The remaining
   questions (#3 about a separate testing.md — done; #4 near-term
   gaps; #5 mining aski for language-design — done) are now
   resolved.

---

## Where to find things — map

### For agents picking up cold

Read in order:

1. `~/primary/ESSENCE.md` — workspace intent.
2. `lore/AGENTS.md` — canonical agent contract; Tool basics
   index links every other doc.
3. `~/primary/AGENTS.md` — workspace-specific (roles,
   orchestration, no-harness-memory, BEADS-transitional).
4. `~/primary/protocols/orchestration.md` — claim/release
   helper, reports exemption, override mechanism.
5. `~/primary/skills/autonomous-agent.md` and `skill-editor.md`
   — start there; read others on demand.

### Quick reference table

| If you want to know… | Look at… |
|---|---|
| Workspace intent | `ESSENCE.md` |
| How to act autonomously | `skills/autonomous-agent.md` |
| How to write/edit a skill | `skills/skill-editor.md` |
| How to commit and push | `skills/version-control.md` |
| Rust discipline | `skills/rust-discipline.md` |
| Nix discipline | `skills/nix-discipline.md` |
| Language-design instincts | `skills/language-design.md` |
| ractor patterns (how the framework works) | `lore/rust/ractor.md` |
| Rust testing patterns | `lore/rust/testing.md` |
| Cargo.toml / cross-crate deps | `lore/rust/style.md` |
| crane + fenix flake layout | `lore/rust/nix-packaging.md` |
| rkyv usage | `lore/rust/rkyv.md` |
| jj CLI | `lore/jj/basic-usage.md` |
| nix CLI | `lore/nix/basic-usage.md` |
| Nota grammar | `nota` repo's `README.md` |
| Persona messaging design (typed records, reducer) | `reports/designer/2026-05-06-persona-messaging-design.md` |
| Persona-message prototype audit | `reports/designer/2026-05-06-persona-message-audit.md` |
| Real-harness test architecture | `reports/designer/2026-05-07-real-harness-test-architecture.md` |
| Workspace coordination (locks, BEADS) | `protocols/orchestration.md` |

---

## Suggested pickup points (for next session)

In rough priority order:

1. **Watch operator's persona-message + persona-wezterm work
   land**; once the round-trip + WezTerm-based real-harness
   tests pass, audit them against the design reports.

2. **Verb-form vs noun-form decision** for persona Commands
   — surface it for resolution. Pick one; rename the other.

3. **persona-message simplification** — once operator has a
   moment, the audit's deletion list is still applicable.

4. **CriomOS-home `skills.md`** — `stt-interpreter.md` has a
   forward reference to it for the speech-to-text tool's
   description. Dead pointer until that skill lands; an
   agent doing CriomOS-home work should write it.

5. **Per-repo skills rollout** (bead `primary-bmy`) —
   incremental, agent-driven. Each agent doing real work in
   a repo missing `skills.md` writes it before finishing.

6. **Five ractor gaps**: when persona's reducer needs an
   actor registry or pg pubsub, document them at the same
   time as the implementation.

7. **Three rust-discipline expansions** (default `#[derive]`,
   generics naming, async patterns): when persona-message /
   persona-wezterm code accumulates enough examples, lift
   patterns into the discipline.

---

## Closing notes

The workspace is healthier than it was 48 hours ago.
`lore/` is project-decoupled; the skills system is in place
with 12 workspace skills + 2 repo skills + an active rollout
bead; the persona substrate has a design report, an audit, and
a real-harness test architecture; the orchestration protocol
is mature; the no-harness-memory rule is canonical; the
efficiency-of-instruction principle is in ESSENCE. Several
small consolidations landed in this turn (style.md trim,
sync-façade dedup, ESSENCE addition).

Operator's persona-message + persona-wezterm work is the
hinge — once those tests run end-to-end with cross-harness
prompt injection, the messaging fabric has crossed the
demonstration threshold and the next layer (the durable
reducer, content-addressed storage, the harness adapter
library) becomes worth the effort.

Designer idle on completion of this handoff; releasing the
lock.

---

## See also

- All designer reports under `reports/designer/`.
- Operator's reports under `reports/operator/` (especially
  `2026-05-06-terminal-harness-control-research.md` for the
  substrate substance behind real-harness tests).
- `reports/2026-05-06-gas-city-fiasco.md` — workspace-historical
  post-mortem; predates the role split.
- `reports/2026-05-06-primary-handoff.md` —
  workspace-historical handoff that started this session;
  predates ESSENCE / skills / orchestration protocol /
  designer reports.
