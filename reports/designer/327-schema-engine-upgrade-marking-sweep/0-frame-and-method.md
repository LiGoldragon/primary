*Kind: Frame · Topic: schema-engine-upgrade-marking-sweep · Date: 2026-05-24*

# 327 · Frame — schema-engine upgrade marking sweep

## §1 Psyche directive + intent context

> "use subagents to do a wide intent implementation (intent and architecture repo files edit) on all our components - tell them to mark any of them for update to schema-based engine that need to, basically all of them."

The current schema-language MVP design (per `/326-v13` + `/324` + operator/174) is structurally stable. Every component in the workspace will eventually convert its hand-written `signal_channel!` + Layer 2 Command/Effect + storage code into a single `<component>/<component>.schema` file consumed by the brilliant macro library (`primary-ezqx.1`). This sweep marks every component's ARCHITECTURE.md (and INTENT.md where it exists) with a "pending schema-engine upgrade" section so future operators reading any component's ARCH see the migration target + cross-references to the canonical designer reports.

## §2 Four-subagent dispatch

- `0-frame-and-method.md` — this file
- `1-core-persona-triads.md` — Subagent A · spirit + mind + router + message + orchestrate
- `2-adjacent-persona-triads.md` — Subagent B · terminal + harness + introspect + system + engine-management + agent
- `3-engine-and-agent-harness.md` — Subagent C · persona + upgrade + persona-pi + signal-persona + signal-persona-origin
- `4-libraries-and-workspace-domains.md` — Subagent D · libraries (signal-frame, signal-sema, sema-engine, nota suite, version-projection, signal-executor) + workspace-domain components (forge, cloud, domain-criome, lojix, horizon-rs)
- `5-overview.md` — orchestrator synthesis after subagents return

## §3 The marking format

Each subagent edits ARCHITECTURE.md (and INTENT.md if present) in every relevant repo. Add a NEW section near the END of each ARCH file (before "See also" if present):

### §3.1 For component triads (daemons + signal contracts)

```markdown
## Pending schema-engine upgrade

**Status:** scheduled for migration to schema-language-based contract per `reports/designer/326-v13-spirit-complete-schema-vision.md` + `reports/designer/324-migration-mvp-spirit-handover-re-specification.md`.

**Target:** this component's hand-written `signal_channel!` invocation + Layer 2 Command/Effect + storage types convert to a single `<component>/<component>.schema` file. The brilliant macro library (`primary-ezqx.1`) reads the schema + emits all the wire types + ShortHeader projection + dispatcher + VersionProjection + storage descriptors.

**Sequence:** [per-component sequencing note — Spirit is the MVP pilot landing first via `primary-ezqx.1`; this component follows after pilot succeeds and per-component schema cutover beads land]

**Per-component concerns:** [optional list of specifics — e.g., upgrade timing relative to dependents, hand-written sema-bridge logic preserved, special storage shape, blockers]

**References:**
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — uniform header form + schema-language design
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` — migration MVP + handover state
- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md` — Spirit MVP worked example
- `reports/operator/174-schema-import-header-design-critique-2026-05-24.md` — header/body/feature separation + lowering rules
```

### §3.2 For substrate libraries (signal-frame, signal-sema, sema-engine, nota suite, version-projection, signal-executor)

```markdown
## Macro-pattern integration

**Status:** integrated into the brilliant macro library pattern per `reports/designer/326-v13-spirit-complete-schema-vision.md §3` (schemas as macro-pattern instance).

**Role:** this crate provides [substrate concern — codec / vocabulary / storage / etc.] consumed by the macro library that processes `.schema` files.

**Integration target:** [per-library note — what THIS crate's role is in the macro pipeline]

**References:**
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — schema language + macro pattern
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` — migration MVP
- `reports/operator/174-schema-import-header-design-critique-2026-05-24.md` — lowering + AssembledSchema form
```

## §4 Hard constraints

- **Edit ARCHITECTURE.md** of each repo in scope. Also edit INTENT.md when present.
- **One new section per file**, placed near the end (before "See also" if present).
- **Per-component concerns** field is OPTIONAL — populate only when concrete specifics exist; leave empty otherwise.
- **No other content changes.** Don't restructure existing ARCH content; don't fix typos; don't update other sections. Add ONE section only.
- **NOTA examples (if any)** use bracket-string form per `primary-36iq` (`[text]` not `"text"`).
- **Mermaid label discipline** per `/home/li/primary/skills/mermaid.md` §"Label sizing" — short prose nodes, IDs in sibling tables. (Probably no mermaid needed for these edits.)
- **No emojis. No `---` horizontal-rule lines.**
- **jj headless ONLY** if committing: `jj describe -m '<msg>'` per `skills/jj.md`.
- **Commit per-repo** with message `<component>: mark pending schema-engine upgrade per /326-v13 + /324`.
- **Push if remotes exist** — many of these repos auto-sync; use `jj git push --branch main` or equivalent only if the remote is configured + push-safe.
- **Each subagent produces a triage report** at `reports/designer/327-schema-engine-upgrade-marking-sweep/<N>-<slice-name>.md` listing edits + deferrals + any blockers encountered.
- **If a repo doesn't have ARCHITECTURE.md** (some smaller crates may not), CREATE a minimal one with the schema-engine upgrade section + a short component description. Don't skip; the absence is itself a gap worth filling.

## §5 What this sweep does NOT do

- Does NOT modify code (no `src/`, no Cargo.toml).
- Does NOT actually convert any component to `.schema` form (that's operator's `primary-ezqx.1` + per-component cutover beads).
- Does NOT update CLAUDE.md, AGENTS.md, README.md.
- Does NOT touch reports outside `reports/designer/327-…/` (operator/second-designer lanes own theirs).
- Does NOT capture spirit intent (psyche directive went straight to designer dispatch).

## §6 Per-slice repo inventory

### §6.1 Slice A (Subagent A) — core persona triads

| Component | Repos |
|---|---|
| spirit | `/git/github.com/LiGoldragon/persona-spirit` + `/git/github.com/LiGoldragon/signal-persona-spirit` (still on old names per /318 pilot block) |
| mind | `/git/github.com/LiGoldragon/mind` + `/git/github.com/LiGoldragon/signal-mind` |
| router | `/git/github.com/LiGoldragon/router` + `/git/github.com/LiGoldragon/signal-router` |
| message | `/git/github.com/LiGoldragon/message` + `/git/github.com/LiGoldragon/signal-message` |
| orchestrate | `/git/github.com/LiGoldragon/orchestrate` + `/git/github.com/LiGoldragon/signal-orchestrate` |

### §6.2 Slice B (Subagent B) — adjacent persona triads + agent

| Component | Repos |
|---|---|
| terminal | `terminal` + `signal-terminal` + `terminal-cell` if present |
| harness | `harness` + `signal-harness` |
| introspect | `introspect` + `signal-introspect` |
| system | `system` + `signal-system` |
| engine-management | `signal-engine-management` (+ daemon if exists) |
| agent | `signal-agent` (+ daemon if exists; per /309 + R10 rename) |

### §6.3 Slice C (Subagent C) — engine + agent-harness + persona contracts

| Component | Repos |
|---|---|
| persona | `persona` + `signal-persona` |
| persona-origin | `signal-persona-origin` |
| upgrade | `upgrade` + `signal-upgrade` + `owner-signal-upgrade` if exists |
| persona-pi | `persona-pi` (agent-harness backend; keeps `persona-` prefix per spirit 371) |

### §6.4 Slice D (Subagent D) — substrate libraries + workspace-domain components

Substrate libraries (use macro-pattern integration marking format §3.2):
- `signal-frame` + `signal-frame-macros`
- `signal-sema`
- `sema-engine` + `sema` + `semac`
- `nota` + `nota-codec` + `nota-derive` + `nota-config`
- `version-projection`
- `signal-executor`
- `signal-derive`

Workspace-domain components (use triad marking format §3.1):
- `forge` + `signal-forge`
- `cloud` + `signal-cloud`
- `domain-criome` + `signal-domain-criome`
- `lojix` + `signal-lojix` + `lojix-cli`
- `horizon-rs`
- `signal-criome`
- `signal-repository-ledger`
- Other signal-* contracts not yet covered

## §7 What the overview (file 5) integrates

After subagents return:

1. Tally of components marked (per slice + total)
2. Components deferred or blocked (with reasons)
3. Cross-cutting observations (e.g., common gaps in ARCH structure, components without ARCH)
4. What carries forward — concrete operator-actionable items
5. Cross-references to update in upstream design reports (`/324`, `/326-v13`) if any
