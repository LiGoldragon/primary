# Designer roadmap — skills next-steps

Date: 2026-05-06
Author: Claude (designer)
Sources: wide subagent audit of `~/primary` + `lore/` + per-repo state;
direct read of `system-specialist.md` and the operator's recent reports.

---

## State of the workspace

The skills system is past bootstrap. Four workspace skills exist
(`autonomous-agent`, `skill-editor`, `stt-interpreter`,
`system-specialist`); two repo skills (`criome`, `sema`); one bead
tracking the per-repo rollout. The orchestration protocol is mature
(role claims, override mechanism, reports exempt with role
subdirectories). The operator and designer have run a clean
parallel-edit cycle through lock + rebase + push.

The user's framing — **lore = tool documentation; skills = how to
use the tools, which to pick, when to apply them** — names a real
boundary. Several lore docs sit on the wrong side of it. Several
skills don't exist yet that already-mature substance is asking for.

---

## Lore-vs-skills migration table

Per the user's framing, each lore doc gets a verdict:

| File | Verdict | Reason |
|---|---|---|
| `lore/programming/beauty.md` | **Migrate to skill** | Pure discipline; criterion + diagnostic catalogue. |
| `lore/programming/abstractions.md` | **Migrate to skill** | Pure discipline ("verb belongs to noun"); zero tool reference. |
| `lore/programming/naming.md` | **Migrate to skill** | Discipline + offender table; same shape as `stt-interpreter.md`. |
| `lore/programming/push-not-pull.md` | **Migrate to skill** | Pure discipline ("polling is wrong"); orthogonal to any tool. |
| `lore/programming/micro-components.md` | **Migrate to skill** | Discipline (one capability per crate per repo) + the LLM-context argument. |
| `lore/rust/style.md` | **Split** | Discipline (methods on types, no ZST holders, domain newtypes, one-object-in-out, error enums) → skill. Pure-Rust syntax (`Cargo.toml` snippets, trait-domain table, thiserror reference) → stays as lore reference. |
| `lore/rust/ractor.md` | **Stay** | Tool reference: cargo features, four-piece template, `RpcReplyPort` mechanics. |
| `lore/rust/rkyv.md` | **Stay** | Tool reference: cargo features, derive aliases, encode/decode API. |
| `lore/rust/nix-packaging.md` | **Stay** | Tool reference: canonical flake.nix, crane + fenix mechanics. |
| `lore/nix/integration-tests.md` | **Split** | "Two patterns" framing → skill; concrete derivation snippets stay as lore. |
| `lore/bd/basic-usage.md` | **Split** | "bd vs files — when each is the right home" → skill; CLI reference stays. |
| `lore/jj/, dolt/, annas/, linkup/, substack/, nix/{basic-usage,flakes}` | **Stay** | Pure CLI reference. |

Net: **5 pure migrations**, **3 splits**, **9 stay**.

---

## High-leverage skills not yet existing

Each is made of substance that already exists somewhere — recategorizing
it into a skill is the cheapest growth.

### 1. `skills/rust-discipline.md` — workspace
The Rust-specific discipline (methods on types, no ZST holders, domain
newtypes, one-object-in-out, no anyhow/eyre, `*Details` companion
rejection, direction-encoded names). My persona audit was *exactly this
skill applied as a one-shot review*. With the skill landed, future Rust
scaffolds run the discipline at write-time and audit reports become rare.
**Highest leverage.** Lifted mostly from `lore/rust/style.md`'s
discipline half.

### 2. `skills/design-report.md` — workspace
How to write a design report — when mermaid vs ASCII, what's a
code-snippet violation vs a sample, the present-tense rule, the
report→ARCHITECTURE.md flow direction, role-subdir placement. The
discipline is currently distributed across 5 places in `lore/AGENTS.md`;
agents inferring it from style is wasted thought. Substantial reports
have just landed (operator's harness-design + persona-core +
terminal-research, my persona audit) — the convention is mature enough
to capture.

### 3. `skills/repo-bootstrap.md` — workspace
How to bring a fresh repo to canonical shape: `AGENTS.md` shim →
`CLAUDE.md` shim → `ARCHITECTURE.md` → `skills.md` → flake template →
`bd init` → `jj git init --colocate` → first commit + push. Persona is
in this state right now; `primary-bmy` will hit ~30 repos that need it.
A single bootstrap skill replaces five-doc archaeology.

### 4. `skills/harness-control.md` — workspace
The terminal-harness boundary (TypedKeys / BracketedPaste / RawBytes,
the layered observation model, when WezTerm vs portable-pty vs ttyd,
why slash commands must be terminal input not model messages). The
operator's 463-line research report is the substance; a skill makes it
reusable beyond the operator's head.

### 5. `persona/skills.md` — repo
The persona-naming-discipline findings from my audit, framed as
skill-permanent rather than report-one-shot. No `Persona*` prefix; no
`*Record` suffix; verb-shaped struct names → noun form; uniform `*Id`;
`State`/`StateSnapshot` companion forbidden. The audit's findings are
skill-shaped, not report-shaped.

---

## Concerns

**`autonomous-agent.md` is over the soft cap** (244 lines vs ~150).
Two sub-sections ("Cross-references" + "Editing skill files") overlap
with `skill-editor.md` — moving those there shrinks
`autonomous-agent.md` ~40 lines without losing substance.

**`system-specialist.md` has a runbook embedded** (lines 96–141, the
Cluster Nix signing section). Symptom + diagnostic commands +
workaround ladder is tool-reference shape, not skill shape. Belongs in
`lore/nix/` or `CriomOS/skills.md` once it exists.

**Frontmatter convention drift**. Lore docs carry
`source:`/`fetched:`/`trimmed:` frontmatter; skills don't. At the
migration boundary, drop the frontmatter — the file location
(`skills/`) carries the equivalent signal ("this is workspace
discipline, not upstream-trimmed reference"). Worth naming this rule
in `skill-editor.md` before more migrations land.

**Forward references in repo skills.** `criome/skills.md` and
`sema/skills.md` "See also" sections name nexus/signal/forge/arca/prism
skills that don't exist yet. Not broken (the references are by repo
name, not URL — they resolve when the destination lands), but worth
tracking which dead pointers shrink as the rollout moves forward.

**A `skills/index.md`** might be worth introducing as the lore→skill
boundary widens. `lore/AGENTS.md`'s "Tool basics" curated index
currently includes the discipline docs; once those migrate, the lore
index halves and the skills cluster needs its own index — or a curated
listing in `skill-editor.md`.

---

## What I'm doing in this turn

To make the migration story concrete rather than theoretical, I'm
landing **one pilot migration**: `lore/programming/beauty.md` →
`~/primary/skills/beauty.md`, including the cross-reference updates in
`lore/AGENTS.md` so the workspace stays coherent. This establishes the
pattern (drop frontmatter, prefix `# Skill —`, add "What this skill is
for" section, update referrers) for the remaining four programming/
files plus the rust/style.md split.

If the pilot reads cleanly to you, the natural next batch is the rest
of `programming/*` (4 more files) as one commit, then the
`rust/style.md` split as a separate, more careful pass.

---

## Questions

1. **Migration cadence** — do you want me to land the remaining four
   `programming/*` migrations in this session, or pace them across
   sessions so each one gets reviewed?
2. **`skills/index.md`** — worth introducing now (before the migration
   wave widens), or wait until 8–10 skills exist and the index is
   obviously needed?
3. **Frontmatter rule** — confirm: drop frontmatter on migrated docs,
   add origin marker (`migrated from lore/<path> on YYYY-MM-DD`) for
   one revision, or skip the marker entirely?
4. **Order of new-skill priorities** — `rust-discipline.md` first
   (because audits will keep happening until it exists), or
   `design-report.md` first (because every agent writes reports)? My
   lean: rust-discipline.

---

## See also

- this report's source audit (subagent, in-conversation; not file-saved)
- `~/primary/reports/designer/2026-05-06-persona-audit.md`
- `~/primary/reports/designer/2026-05-06-skills-bootstrap-status.md`
- `~/primary/skills/skill-editor.md` (canonical conventions)
- the operator's `reports/operator/2026-05-06-terminal-harness-control-research.md`
  (substance for the proposed `harness-control.md` skill)
