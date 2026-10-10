---
title: 82 — repo sprawl, the skill that caused it, sema/signal-sema, spirit-next, orchestrate's old deps
role: system-designer
variant: Findings
date: 2026-06-07
topics: [repository-sprawl, major-break-via-new-repo, sema, signal-sema, sema-engine, spirit-next, orchestrate, triad-main, cleanup, ug6i]
description: |
  The psyche found garbage in the repo list (dated design passes, mockups,
  repros, an old gascity, a literally-named signal-frame-worktrees) and asked:
  who's making repos instead of branches, is there a skill that tells them to,
  what is signal-sema, what is spirit-next, and why does orchestrate still
  depend on old crates. Answers, grounded in inspection, plus a cleanup
  proposal that needs psyche go-ahead before any repo is deleted.
---

# 82 — repo sprawl + orchestrate's old deps

## 1. Yes, a skill told agents to make repos. It is now retired.

`skills/major-break-via-new-repo.md` (per former psyche 2026-05-26, record
811) instructed: *"when an architectural break is large enough … create a new
repository with a `-next` / `-v2` / longer descriptive suffix and develop in
parallel … `gh repo create LiGoldragon/<name>-next`."*
`skills/double-implementation-strategy.md` reinforced it with a "designer
track" that created `design-`-prefixed throwaway repos.

That is the source of the sprawl. Per psyche 2026-06-07 (Spirit `op4b` +
`53bj`) both are corrected: **a feature branch has no limits — wipe the tree
and rebuild from scratch on a branch; major breaks are branches, and a new
repository is only for a genuinely new project.** Done this session:

- deleted `skills/major-break-via-new-repo.md`
- `skills/repository-management.md` — new §"When to create a new repository"
- `skills/feature-development.md` — new §"A branch has no limits"
- `skills/double-implementation-strategy.md` — rebased both tracks onto branches
- `skills.nota` + `workspace-vocabulary.md` — index + glossary updated

## 2. The garbage inventory (clear throwaway repos)

These are **real GitHub repos** under `LiGoldragon/`, checked out in `/git`,
symlinked in `repos/`. They should have been branches:

| Repo | What it is | Verdict |
|---|---|---|
| `design-deep-spirit-2026-05-26` | dated design pass | delete (was a branch's worth of work) |
| `design-deep-spirit-next-pass-2026-05-26` | dated design pass | delete |
| `design-nota-from-schema` | design pass | delete |
| `design-signal-frame-schema` | design pass | delete |
| `signal-frame-mockup-stable-caller-id-1` | mockup | delete |
| `kameo-supervised-shutdown-repro` | bug repro | delete |
| `signal-frame-worktrees` | literally a repo named "worktrees" | delete |
| `gascity`, `gascity-nix` | old project, no longer used | confirm with psyche, then delete/archive |
| `test-city` | scratch | confirm, delete |
| `kameo-testing`, `kameo-testing-assistant` | kameo spike repos | confirm, delete |

Larger families that also smell, flagged for a dedicated audit (not deleting
blind):

- **`owner-signal-*`** (`owner-signal-agent`, `-mind`, `-persona`,
  `-persona-spirit`, `-terminal`, `-version-handover`, `-sema-upgrade`,
  `-cloud`, `-upgrade`, `-domain-criome`): the **OwnerSignal contracts are
  DEPRECATED** — `MetaSignal` is canonical (Spirit `hnpo`). The whole
  `owner-signal-*` family is legacy and is a delete/archive candidate set
  once consumers are confirmed off them.
- **`signal-*` proliferation** (~40 `signal-X` repos): some are live triad
  working contracts, but several look like one-off or superseded contracts.
  Needs a per-repo "is anything depending on this" pass.
- **`-archive` repos** (`lojix-archive`, `criomos-archive`, `nexus-spec-archive`):
  intentional archives — keep, but they don't need `repos/` symlinks.

A full repo-by-repo audit is its own task (this looks like exactly the
mechanical rules-and-flaws work the auditor role `ek8w` is meant for). Nothing
above gets deleted without explicit psyche go-ahead — deleting a GitHub repo
is irreversible and outward-facing.

## 3. spirit-next — a symlink, not a repo

`/git/github.com/LiGoldragon/spirit-next` is a **symlink → `spirit`** (same
remote `git@github.com:LiGoldragon/spirit.git`). The psyche's read is exactly
right: "spirit-next is just pointing to spirit." It is a compatibility shim
left over from when `spirit-next` was a separate `-next` repo that got
consolidated into `spirit`. Cleanup: remove the symlink; verify whether a
stale `spirit-next` GitHub repo still exists and delete it if so. (`spirit`
itself uses branches now — `designer-daemon-emit-2026-06-06`, etc. — so no
`-next` repo is needed.)

## 4. sema / sema-engine / signal-sema — what each actually is

The psyche's worry was "is orchestrate talking to an external SEMA database
over the wire?" The answer is **no** — but orchestrate IS on old deps.

- **`sema-engine`** (INTENT: *"the exclusive database-operation boundary for
  state-bearing components. Component daemons do not open redb, define redb
  tables, run redb transactions…"*) — the **in-process library** every
  state-bearing triad daemon embeds. This is the correct new core crate
  (Spirit `fosp`). There is NO separate sema daemon over the wire; each
  daemon owns its SEMA in-process.
- **`sema`** (README: *"the sema database kernel: typed, version-guarded table
  access over redb"*) — a lower-level **DB kernel library**. `sema-engine` is
  the boundary that wraps the kernel concern; a component depending on `sema`
  **directly** bypasses the `sema-engine` exclusive boundary — that's a
  migration smell.
- **`signal-sema`** (README: *"Sema observation vocabulary: payloadless
  operation classes Assert / Mutate / Retract / Match / Subscribe / Validate …
  Component daemons consume this crate when they project their local executable
  Commands and Effects into cross-component observer labels"*) — this is an
  **observability / tracing vocabulary**, NOT a wire contract to a database
  service. It does not mean orchestrate talks to a sema daemon. (Whether
  orchestrate still needs it is a separate question; it's about cross-component
  observer labels.)

So: there is no "SEMA component talking over the wire to do database stuff."
The `signal-sema` name is misleading but it's an observer-label vocabulary.

## 5. orchestrate is NOT migrated to the new core

`orchestrate/Cargo.toml` dependencies:

```
sema                    = { git … }              # OLD — direct DB kernel, bypasses sema-engine boundary
sema-engine             = { git … }              # new core (good)
signal-orchestrate      = { … branch=main }      # its triad working contract
meta-signal-orchestrate = { … branch=main }      # its triad meta contract
signal-executor         = { … branch=main }      # ? likely legacy
signal-frame            = { … branch=main }      # new core (good)
signal-sema             = { … branch=main }      # observer vocabulary (see above)
signal-version-handover = { … branch=main }      # ? likely legacy
triad-runtime           = { … branch=main }      # new core (good)
nota-codec, version-projection                    # support
```

The tells that orchestrate predates the triad_main migration:
- depends on **`sema` directly** (should be `sema-engine`-only per `fosp`);
- carries `signal-executor` / `signal-version-handover` (legacy signal crates);
- it still has a **hand-written `src/daemon.rs`** (per the migration scoreboard
  in report 80) — not yet on the emitted `triad_main` daemon.

orchestrate is on the ocu7 migration list and needs the same treatment cloud
just got: drop the direct `sema` dep (embed `sema-engine`), prune legacy
signal crates, and retire its hand-written daemon onto the emitted triad_main.

## 6. Recommended cleanup order (all needs psyche go-ahead before deleting)

1. Delete the clear throwaway repos (table in §2, top block) — design passes,
   mockups, repros, `signal-frame-worktrees`. Branch-worthy work that became
   repos; nothing depends on them.
2. Remove the `spirit-next` symlink (+ delete the stale GitHub repo if it exists).
3. Confirm + retire the old projects (`gascity*`, `test-city`, `kameo-testing*`).
4. Schedule the `owner-signal-*` (deprecated, `hnpo`) and `signal-*`
   proliferation audit as a dedicated pass (auditor-shaped).
5. Migrate orchestrate onto triad_main + sema-engine (ocu7).

Deleting GitHub repos is irreversible and outward-facing — I will not delete
any without explicit go-ahead per repo or per batch.
