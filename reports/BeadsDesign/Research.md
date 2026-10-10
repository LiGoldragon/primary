# Beads research — data model, lifecycle, prior usage, and its relation to context handovers

Read-only research for a design pass. No recommendations below; facts, commands, quotes, and paths only.

## 1. Where beads lives

- CLI: `bd` at `/home/li/.nix-profile/bin/bd`, version `1.0.0 (dev)`. Upstream project: `steveyegge/beads` (per `.beads/README.md`, "Beads - AI-Native Issue Tracking").
- A separate, unrelated repo `github.com/gastownhall/beads` is ghq-cloned at `/git/github.com/gastownhall/beads` — not used by the live store; not the same project as `bd`'s upstream (steveyegge/beads is not ghq-cloned anywhere found).
- The live store for this workspace is **one centralized database** at `/home/li/primary/.beads/`, not per-repo, despite many other repos under `/git/github.com/LiGoldragon/*/.beads/` (e.g. `signal/.beads`, `CriomOS/.beads`, `forge/.beads`, ~24 repos total) each carrying their own `.beads/` directory. Whether those are live/duplicate stores or dormant scaffolding from `bd init` was not verified; only `/home/li/primary/.beads` was queried.
- Backend: embedded Dolt (a git-like versioned SQL database), per `.beads/metadata.json`:
  ```
  {"database":"dolt","backend":"dolt","dolt_mode":"embedded","dolt_database":"primary","project_id":"b4fe6b05-2438-45cd-8005-45274df57509"}
  ```
- Git-tracked files (`git ls-files .beads`): only `.beads/.gitignore`, `.beads/README.md`, `.beads/config.yaml`, `.beads/metadata.json`. Two commits touch `.beads` in `primary`'s history: `11aab1238ebf bd init: initialize beads issue tracking` and `e26710799 workspace commit operator coordination state`. Everything else — the actual Dolt data directory (`embeddeddolt/`), `backup/` (Dolt `.darc` archive snapshots), `interactions.jsonl` (audit trail), `push-state.json`, `last-touched` — is gitignored (confirmed via `git status --ignored=matching -- .beads`). **The issue data itself is not committed to git; only the bootstrap scaffolding is.**
- Command surface (`bd help`, abridged to the categories that matter): `create`, `create-form`, `q` (quick-capture, ID-only output), `update`, `close`, `reopen`, `edit` (`$EDITOR`), `assign`, `label`/`tag`, `dep`, `link`, `priority`, `comment`/`comments`, `note`, `children`, `epic`, `swarm`, `gate`, `merge-slot`, `list`, `show`, `search`, `query`, `find-duplicates`, `stale`, `count`, `history`, `diff`, `graph`, `lint`, `status`, `statuses`, `types`, `export`/`import`, `backup`, `federation`, `branch`, `vc`, `bootstrap`, `doctor`, `where`, `info`, `context`, `compact`, `flatten`, `gc`, `purge`, `rename-prefix`, `promote`, `migrate`, `sql` (not supported in embedded mode — see below), `worktree`, `kv`, `remember`/`recall`/`memories`/`forget`.

## 2. Data model

Derived from `bd create/update/show/list --help`, the beads source at `/git/github.com/gastownhall/beads`, and a full export of the live store (`bd export --all -o export.jsonl`, 1515 records, see §7). Keys actually observed on real records, with the count of records (out of 1515) carrying each:

| Field | Present on | Notes |
|---|---|---|
| `id` | 1515/1515 | e.g. `primary-o2cd`, `primary-o2cd.6` (dotted = child of `primary-o2cd` via a `parent-child` dependency edge, not a separate ID scheme) |
| `title` | 1515/1515 | only field that's unconditionally required |
| `status` | 1515/1515 | `open`, `in_progress`, `blocked`, `deferred`, `closed` in this store; `bd statuses` also lists `pinned`, `hooked` as valid values |
| `priority` | 1515/1515 | integer 0–4 (0=highest/critical .. 4=backlog), default 2 |
| `issue_type` | 1515/1515 | `task`, `epic`, `feature`, `bug`, `decision`, `chore`, `event` seen; `bd types` also lists `merge-request`/`mr`, `molecule`/`mol`, `gate`, `convoy` |
| `created_at` / `updated_at` | 1515/1515 | RFC3339 |
| `dependency_count` / `dependent_count` / `comment_count` | 1515/1515 | derived counters, always present even at 0 |
| `created_by` | 1487/1515 | see §7 — always `li`, never an agent identity |
| `owner` | 1486/1515 | e.g. `li@goldragon.criome.net` |
| `description` | 1484/1515 | free text; see §7 for how much of it is process/how-to instruction rather than goal |
| `labels` | 1347/1515 | array of strings, multi-valued, glob/regex filterable, include `role:*` convention (see §7) |
| `closed_at` | 1123/1515 | only on closed issues |
| `close_reason` | 1088/1515 | free text |
| `dependencies` | 775/1515 | array of typed edges: `{issue_id, depends_on_id, type, created_at, created_by, metadata}`; types seen: `parent-child`, `blocks`; `bd dep`/`bd link` also support `tracks`, `related`, `discovered-from`, `conditional-blocks`, `waits-for` per `--help` |
| `acceptance_criteria` | 495/1515 | free text |
| `notes` | 315/1515 | free-text append log — in practice used for large running verbatim records (see §7, `primary-56d1` epic) |
| `assignee` | 79/1515 | see §7 for value distribution |
| `design` | 14/1515 | free text |
| `spec_id` | 9/1515 | cross-reference to an external spec |

Not required: everything except `title` — type/status/priority all default. Additional fields exist in the CLI surface but were not observed populated in this store: `estimate` (minutes), `due`/`defer` dates, `metadata` (arbitrary JSON key/values), `external-ref` (e.g. `gh-9`, `jira-ABC`), `mol-type` (`swarm`/`patrol`/`work`), `skills-required`, and the ephemeral-wisp fields (`--ephemeral`, wisp-type `heartbeat`/`ping`/`patrol`/`gc_report`/`recovery`/`error`/`escalation`).

Relations: parent/child is a `dependency` of type `parent-child` (not a separate schema field) — `bd children <id>` lists them, `bd epic`/`bd swarm` manage epic/swarm structures on top of the same dependency graph. Blocking is `type: blocks`. No size-limit documentation was found in the CLI help for title/description/notes length; the only related control is `output.title-length` in `config.yaml` (default 255), which truncates command *feedback display* only, not the stored value.

Store alternative: `config.yaml` documents a `no-db: true` mode where `.beads/issues.jsonl` becomes the source of truth instead of Dolt — not enabled here (`export.auto: false`, no-db unset/false).

## 3. Lifecycle

- Create: `bd create "<title>" -t <type> -p <priority> -d "<description>"`, or `bd q` for quick-capture (prints only the new ID), or `bd create-form` for an interactive form, or batch-create from markdown/graph JSON (`bd create --help` mentions this).
- Claim: `bd update <id> --claim` — sets assignee to the caller and status to `in_progress`; documented as idempotent.
- Update: `bd update <id> [flags]`, `bd edit <id>` (opens `$EDITOR` on a field), `bd priority <id> <n>`, `bd label`/`bd tag`, `bd assign <id> <who>`.
- Dependency wiring: `bd dep <blocker-id> --blocks <blocked-id>`, `bd link`.
- Close: `bd close <id> --reason "..."`, with `--claim-next` (auto-grab the next-priority ready item) and `--continue` (auto-advance a molecule's steps) flags.
- Reopen: `bd reopen <id>`.
- Ordering: **priority (0–4) is hand-set**; **readiness is derived** — `bd ready`/`bd list --ready` computes open issues with no unresolved blockers (distinct from a naive status filter); `bd blocked` shows what's currently waiting on a dependency.
- Delete/cleanup: `bd delete`, `bd purge` (permanently deletes closed *ephemeral* issues only), `bd gc` (runs decay + compact + Dolt GC as one pipeline; default decay window 90 days for closed issues).
- Wisps: `--ephemeral` issues live in a separate `wisps` table excluded from normal Dolt versioning and JSONL export; `bd promote` copies a wisp into the permanent, versioned table (preserving ID/labels/deps/events/comments).

No field or command in the live surface distinguishes "psyche created this" from "agent created this" — see §7.

## 4. Concurrency behavior

Directly observed mid-research: `bd status`/`bd info`/`bd where` failed with

```
Error: failed to open database: embeddeddolt: another process holds the exclusive lock on /home/li/primary/.beads/embeddeddolt; the embedded backend supports only one writer at a time — use the dolt server backend for concurrent access
```

and cleared on retry a few minutes later; the holding PID could not be identified via a `/proc/*/fd` scan (either very short-lived contention, or held in a namespace this process cannot see). Confirmed by checking `.beads/embeddeddolt/.lock` again later in the same session — it existed but `bd where` succeeded, i.e. the lock is transient/per-writer, not permanently stuck. `bd sql` — floated as a possible route to answer counting questions directly — is **not supported in embedded mode** ("Error: 'bd sql' is not yet supported in embedded mode"); the export-then-analyze route (`bd export --all -o file.jsonl`) was used instead.

This is a real, reproducible, current failure mode, and the workspace's own prior usage independently discovered and recorded it. From the (now-deleted, recovered via `jj`) pre-slashdown skill `modules/work-tracking/full.md` in the skills repo at revision `7f5753642f1d-`:

> Run `bd` tracker commands sequentially, not through parallel tool calls or concurrent shells. `bd` uses a single-writer embedded Dolt store; if a command reports the exclusive `.beads/embeddeddolt` lock, wait for the owning operation to finish and retry the same command. Do not spawn concurrent retries. Treat the lock as a blocker only after several short retries fail, and report the exact command and error.

And from `modules/bead-weaver/full.md` at the same revision:

> Run `bd` commands sequentially, not through parallel tool calls. If embedded Dolt reports the exclusive `.beads/embeddeddolt` lock, wait for the owning operation to finish and retry the same command; do not spawn concurrent retries.

And, independently, from a real operator postmortem after a June 1 2026 bead-cleanup session (`reports/operator/272-bead-staleness-audit-implementation-2026-06-01/4-postmortem.md`, recovered via `jj file show -r b1a5f8ca1d43`, this exact report no longer exists at HEAD — see §6):

> The BEADS backend is sensitive to parallel `bd` commands. Parallel reads caused embedded-Dolt exclusive-lock errors. Future cleanup agents should run `bd` commands sequentially or use a server-backed mode if available.

Today's slashed-down `skills/skills/bead-weaver.md` and `work-tracking.md` (see §6) carry **none** of this — the sequential-only rule and the lock-retry protocol were cut in the "reduce reusable guidance" pass.

The same pre-slashdown `bead-weaver` module also documents a second concurrency hazard, orthogonal to the Dolt lock — an Orchestrate-level claim on the `.beads/` path itself:

> Do not claim `.beads/`. Treat an Orchestrate `.beads/` claim as invalid agent policy state; force-release or remove it instead of treating it as a lock.

Today's slashed skill retains only the bare instruction "Do not claim `.beads/`" with no explanation of why or what to do if one is found (the force-release/remove guidance is gone).

Beyond the embedded-Dolt single-writer lock, `bd`'s own command surface includes two purpose-built multi-agent coordination primitives, distinct from the database lock: `bd gate` (async coordination gates — wait conditions of type human/timer/gh:run/gh:pr/bead) and `bd merge-slot` (an exclusive-access mutex modeled as a bead: metadata `holder` + priority-ordered `waiters` queue, for serializing conflict resolution). Their existence — as bd features layered on top of the database — implies the database's own concurrency story was judged insufficient for coordinating multiple simultaneous agents.

## 5. Discovery / query surface

- `bd search` — title/ID substring and fast ID-prefix match; filterable by assignee/label/status/priority range/dates/description-contains/notes-contains/external-ref.
- `bd query "<expr>"` — boolean query language over `status`, `priority`, `type`, `assignee`, `owner`, `label`, `title`, `description`, `notes`, `created`/`updated`/`closed` dates (with relative-date support), `id`, `spec`, `pinned`, `ephemeral`, `template`, `parent`, `mol_type`.
- `bd list` — the heaviest filter surface: `--status`, `--priority`/`--priority-min`/`--priority-max`, `--assignee`/`--no-assignee`, `--label`/`--label-any`/`--label-pattern`/`--label-regex`/`--no-labels`, `--title`/`--title-contains`/`--desc-contains`/`--notes-contains`, `--created-after`/`-before`, `--updated-after`/`-before`, `--closed-after`/`-before`, `--due-*`/`--defer-*`/`--overdue`/`--deferred`, `--parent`/`--no-parent`, `--type`/`--exclude-type`, `--mol-type`, `--has-metadata-key`/`--metadata-field`, `--ready`, `--pinned`/`--no-pinned`, `--empty-description`, tree vs `--flat`, `--sort` (priority/created/updated/closed/status/id/title/type/assignee), `--format` (`dot`/`digraph`/Go template).
- `bd find-duplicates` — Jaccard token similarity or LLM-based semantic dedup.
- `bd stale` — no-update-in-N-days.
- `bd history <id>` / `bd diff` / `bd graph` — version and structural views riding the Dolt commit history.

## 6. Limitations

- Single-writer embedded Dolt backend (§4) — the documented fix is a Dolt *server* backend, not in use here.
- **History is lossy by design.** `bd compact` squashes Dolt commits older than a threshold (default 30 days) into one; `bd flatten` is described as squashing *all* history into a single commit, "irreversible — all commit history is lost"; `bd gc` runs decay (deletes closed issues past a default 90-day window) + compact + Dolt GC in one pipeline. `bd restore <id>` can recover pre-compaction description/notes only if Dolt history still contains them — once flattened or GC'd, they cannot be recovered. Corroborated directly: `reports/designer/449-bead-staleness-audit-2026-06-01.md` and its implementation postmortem — both real, substantial reports about this exact store — **no longer exist at the current HEAD of `primary`**; they were recovered here only via `jj file show -r b1a5f8ca1d43 <path>` against a historical revision, i.e. they were deleted from the live tree by a later "retire stale reports" sweep (`c93c98884898 context-maintenance sweep: retire ~100 stale reports`, `878b68254448 operator: retire stale reports after state-of-art sweep`, `d8128ca92b24 designer: context maintenance sweep`). This is a report-corpus lossiness pattern, not a beads-internal one, but it means the workspace's own history of *how it used beads* is itself subject to the same "delete when it looks stale" discipline that was applied to the beads themselves.
- **IDs are adaptive-length, not uniform.** Per the observed `bd rename-prefix` command (rewrites every ID's prefix workspace-wide, including text references to it) and the dotted child-ID convention (`primary-56d1.48`), IDs are stable once assigned but the ID *scheme* is not: `rename-prefix` exists specifically to repair "corrupted" multi-prefix databases, i.e. prefix collisions/mistakes are a real, recovered-from failure mode, not a hypothetical one.
- **Wisps are second-class and TTL'd.** Ephemeral issues (`--ephemeral`) are excluded from normal Dolt versioning and JSONL export, live in a separate table, and are subject to `bd purge` (permanent deletion of closed ephemeral beads). `bd promote` is the only path from wisp to permanent record.
- **No hard field-size limit found in the CLI surface**, but in practice the `notes` field is used as an unbounded free-text append log rather than discrete structured entries — the `primary-56d1` epic (see §7) carries several kilobytes of running verbatim ruling text in one `notes` field, i.e. the field degrades into a wall of text under real use rather than staying a list of discrete records.
- **`created_by`/`actor` does not distinguish who is behind the keyboard.** Every one of the 1487 records with a `created_by` value carries `li` (the remaining 28 have none). Because `bd`'s `--actor` defaults to `$BEADS_ACTOR`/git `user.name`/`$USER`, and every agent in this workspace runs as the same Unix user, **the store cannot tell a bead the psyche typed from one an agent typed**, unless a bead's own text says so.
- `bd doctor` is the documented first troubleshooting step for local database health/corruption; this was not needed during this research (the lock cleared on its own).

## 7. Shape of the live store (`bd export --all -o export.jsonl`, 1515 records)

Status: `closed` 1123, `open` 364, `in_progress` 16, `blocked` 11, `deferred` 1.

Type: `task` 1358, `epic` 55, `feature` 41, `bug` 36, `decision` 12, `chore` 12, `event` 1.

Priority: `2` 708, `1` 640, `3` 147, `0` 11, `4` 9.

Age (of the 392 non-closed records, computed against 2026-07-26): minimum 0 days, maximum 75 days, median 21 days; 55 of the 392 are older than 30 days. Time-to-close (of the 1123 closed records with both timestamps): median 4.16 hours, maximum 1313.4 hours (~54.7 days).

Creator/actor: `created_by` is `li` on 1487/1515 records and empty on 28 — **not distinguishable between the psyche and an agent** (see §6). `assignee` (79/1515 populated) skews toward role-shaped values rather than individuals: `li` 46, `operator` 7, `designer-assistant` 6, `operator-assistant` 5, `system-maintainer` 4, `GoldenBridge` 3, plus 8 more with 1 each (including feature-branch-named values like `SignalSpiritUseSignalDomain`, `GoldenBridge`). Labels carrying `role:*` (multiple per record allowed): `role:operator` 309, `role:designer` 66, `role:system-specialist` 66 (a label later documented as a retired lane name — see the 449 audit in §8), `role:cloud-designer` 4, `role:system-designer` 3, `role:second-operator` 2, plus singletons.

**How much of the corpus carries how-to/process instructions rather than only a goal.** Of the 1484 records with a non-empty `description`, a heuristic scan for dispatch/process markers — literal `"Worker handoff"`, a `"Constraints:"` section, an `"Evidence signal"` section, an `"Out of scope:"` section, `"Session "`/`"Lane "` naming jargon, an explicit thinking-effort directive (`"xhigh"`), a `"Definition of done"` section, a code fence, or an explicit tool-command mention (`bd `, `jj `, `cargo `, `nix flake`, `git commit`, `"claim only"`, `"register session"`) — found **495/1484 (33.4%)** carrying at least one such marker. A representative example, `primary-o2cd.6` ("Audit Spirit main consolidation and production verification"), has a description containing a full dispatch template: a goal paragraph, then "**Worker handoff**: use xhigh thinking. Register Session SpiritMainConsolidation / Lane SpiritMainConsolidationAudit Fresh. Prefer read-only repo inspection; claim only any report path you write...", then "**Definition of done**", "**Evidence signal**", and "**Constraints**"/"**Out of scope**" sections. This is a concrete instance of a bead specifying *how* the work should be approached (thinking level, session/lane registration, evidence format, tool-call style) rather than only the goal.

## 8. Prior usage in this workspace, and what happened to it

No single verbatim psyche statement was found declaring "we are stopping beads" or naming a specific incident that ended the practice. What the record shows instead is a documented pivot away from investing further in `bd`, followed several weeks later by a large, independently-discovered staleness problem, followed by a partial cleanup, followed by declining and then (per `interactions.jsonl`) apparently ceasing activity in the week before this research.

**a) May 6, 2026 — beads declared transitional, in favor of a "Persona" messaging fabric.** Commit `e8ef3b60b6c3 design: BEADS is transitional; Persona messaging replaces it` amends `reports/designer/2026-05-06-persona-messaging-design.md` (this is designer-authored design rationale — the file contains no verbatim quotation from the psyche):

> **Note on scope.** BEADS itself is transitional in this workspace — Persona's messaging fabric is what replaces it, not a system that runs alongside it. The lessons below are about *what shape we lift* into Persona, not about *what surface Persona exposes to bd-the-tool*. There is no Persona-bd bridge in the destination.

and later in the same file:

> 5. **What replaces BEADS in the final shape?** **Persona does.** BEADS is transitional substrate — used now because we have it and it works for short tracked items, not because it's part of the destination. The persona messaging fabric subsumes the role... Implication for design: don't carve out a "BEADS adapter." Don't bridge persona to bd. Treat bd-tracked items today as convenience-only and design Persona's record set so it can absorb them when the time comes.

The companion commit `e4d3e50bd19d AGENTS: refresh — required reading, where-things-live map, BEADS-transitional note` added to (the then-current) `AGENTS.md`:

> ## BEADS is transitional
>
> `.beads/` exists today for convenience. The destination is **Persona's typed messaging fabric** — see `reports/designer/2026-05-06-persona-messaging-design.md` for the design. Don't build a Persona↔bd bridge; don't deepen the bd investment. Use bd for short-tracked-item coordination today; design new shapes assuming bd goes away.

Neither of these lines survives in the current `AGENTS.md` (read at the start of this task) — the "BEADS is transitional" section, the required-reading list, and the where-things-live map from that revision have all since been replaced by the present, much shorter `AGENTS.md`. Whether "Persona" (the messaging fabric) was ever built was not traced further; note that the workspace also has an unrelated legacy `persona-*` repo family (persona-mind, persona-orchestrate, persona-spirit, persona-router, persona-harness, persona-introspect, etc.) that is a component stack, not the messaging fabric — see (b), where that whole component family is itself independently declared obsolete three and a half weeks later.

**b) June 1, 2026 — a bead-staleness audit found the backlog had drifted heavily following an architecture pivot.** `reports/designer/449-bead-staleness-audit-2026-06-01.md` (recovered via `jj file show -r b1a5f8ca1d43`; **this file no longer exists at current HEAD**, i.e. it was itself later deleted in a "retire stale reports" sweep):

> The bead store carries **269 open beads** (1 P0, 67 P1, 162 P2, 48 P3)... Substrate has drifted heavily; the dominant pattern is pre-pivot persona-stack work that the schema/NOTA-next/upgrade-as-SEMA arc has now subsumed... Combined with the 68 P0/P1: roughly **180-200 stale beads** + **40-58 actionable beads**, ratio ~3:1 stale-to-current.

The report names five patterns explaining the staleness, the clearest being:

> #### Pattern 4 — the bead store's "epic" abstraction has soured
>
> The store has 9+ epics... All but `primary-kbmi` and `primary-ipjx`... are wholly superseded. Per `skills/beads.md` §"Anti-pattern A: durable-backlog beads", epics that don't close are anti-pattern. The pivot made every epic's "definition of done" unreachable; the epics have been carrying superseded plans for weeks.

That report cites a `skills/beads.md` with an explicit staleness heuristic and anti-pattern list that predates even the pre-slashdown `work-tracking`/`bead-weaver` modules recovered in §6/§9 below — i.e. there was an even earlier, more elaborate local bead-usage doctrine (`skills/beads.md`, a repo-local file in `primary/skills/` at that time, distinct from the central `LiGoldragon/skills` generator) that itself is now gone; only quotations of it survive inside this recovered audit report.

**c) The follow-through cleanup independently rediscovered the concurrency lock.** `reports/operator/272-bead-staleness-audit-implementation-2026-06-01/4-postmortem.md` (same recovery method, also deleted from current HEAD):

> The open-bead queue moved from 269 to 209. The P0 queue is empty. The P1 queue moved from 64 to 15...
>
> The BEADS backend is sensitive to parallel `bd` commands. Parallel reads caused embedded-Dolt exclusive-lock errors. Future cleanup agents should run `bd` commands sequentially or use a server-backed mode if available.

The postmortem explicitly left the bulk of the P2/P3 layer (the ~85-95-plus-more beads the audit judged stale) untouched, deferring a second pass: "This session intentionally avoided closing the broad extrapolated P2/P3 layer except direct stale dependencies. The next cleanup pass should query the remaining P2/P3 clusters sequentially and close them with the same family-note style." No evidence of that second pass was found in the material reviewed.

**d) Activity continued, at declining apparent rate, through mid-July, then stopped.** `.beads/interactions.jsonl` (the local, gitignored audit trail — see §1) contains 1330 `field_change` events, 100% `actor: "li"`, spanning **2026-05-06 through 2026-07-19**, with no entries after that date (today is 2026-07-26 — one week of apparent inactivity at the time of this research). Many entries in the final days before the cutoff are large epics being closed with explicit **psyche-ruling quotations** embedded as `reason` text, e.g. (from `primary-56d1.31`, closed 2026-07-17):

> PSYCHE RULING (chat 2026-07-17). Verbatim reply to parity slate item 1:
> "1. I think thats because I of the TextualForm vs CoreForm (which I think could be called EncodedForm?) - Strings are Strings"

and (from `primary-oay8`, closed 2026-07-19, the last substantive entry before the gap):

> Obsoleted by Ruling 6 (2026-07-19): old components schema-language/schema-rust deprecated with eventual deletion and NO rework; reinforced by Ruling 4 (old lineage not adapted, new pipeline is THE generator).

The pattern in the final weeks is consistent with (b)/(c): a fast-moving architecture pivot (schema/NOTA-next, then a further "Ruling"-driven convergence pass in mid-July) generating and then obsoleting beads faster than the store could stay curated, rather than any single decision to stop. No entry in `interactions.jsonl`, and no report found under `reports/` or in `jj log` commit messages searched for "bead", states a reason for the week-long gap itself.

**e) The current, terse `work-tracking.md`/`bead-weaver.md` skills are a 2026-07-20 distillation that dropped the operational specifics documented above.** Commit `7f5753642f1d` in `LiGoldragon/skills` ("skills: reduce reusable guidance") is independently described, in `reports/SkillsCorpusRedesign/context-handover.md` (written 2026-07-25, five days later, by the same effort this task is part of), as:

> Commit `7f5753642f1d` (2026-07-20, "skills: reduce reusable guidance") deleted 87% of the doctrine corpus — roles 519 lines to 78, skills 4371 to 568 — and it deleted the load-bearing specifics first, because a reserved-keyword list looks like noise next to a sensible-sounding generality. That commit is the cautionary case for this whole effort.

The pre-slashdown modules (`modules/work-tracking/full.md`, `modules/bead-weaver/full.md`, recovered via `jj file show -r '7f5753642f1d-' <path>` in the skills repo) carried the sequential-lock-retry rule (§4), a staleness heuristic (below), a "keep bead text executable" checklist, and an anti-pattern list — all absent from the current generated skill. The staleness heuristic, from `modules/work-tracking/full.md`:

> Age is an important factor in a bead's staleness, though not the sole test and not an auto-close threshold. The older an open bead, the more its retention must be justified rather than assumed: as a rough gradient, roughly two weeks old is suspicious and about a month old is strongly suspect. Keep an old bead only when it still maps to an actively developed line of work, shown by recent commits; otherwise treat it as a candidate to close as invalidated with a reversible reason.

and its anti-pattern list:

> - beads that restate a prompt without acceptance criteria;
> - umbrella beads that hide independent work;
> - closing because code was written but not validated;
> - keeping an old bead open by inertia when nothing active maps to it;
> - using comments as an archive;
> - creating repo-specific process doctrine in the bead body.

This last anti-pattern — "creating repo-specific process doctrine in the bead body" — is close to, but not identical with, the rule the psyche is now applying going forward (bead carries only vision/goal/intention/references, never how-to); the pre-slashdown doctrine forbade *doctrine* in the bead body, not *task-execution instructions* in general, and — per §7 — roughly a third of the live corpus's descriptions carry the latter regardless.

## 9. Handover versus bead — field by field

Sources: current generated `context-handover` skill (`/git/github.com/LiGoldragon/skills/skills/context-handover.md`, 7 lines), its pre-slashdown ancestor (`modules/context-handover/full.md` at `7f5753642f1d-`, recovered via `jj`), and a real handover document, `/home/li/primary/reports/SkillsCorpusRedesign/context-handover.md` (written 2026-07-25).

**What a real handover carries, with no bead field to hold it:**

- **A prose vision section carrying the psyche's own invariants/values in his own recognizable language**, e.g. the "Vision" section's bullets ("An instruction earns its place only by changing behavior...", "A rule needs evidence...", full paragraphs of reasoning) — a bead's closest field is `description`, which is one flat text block with no dedicated "this is standing intent, not this task's goal" marker, and no field distinguishes psyche-authored invariant text from agent-authored task text.
- **A dedicated "style the psyche rejects, in his own words" section quoting him verbatim** (e.g. `"this is stupid. do not try to swallow your tongue, and do not kill your family."`) — a bead has no field for direct-quote-with-attribution; a quote can only go in `notes`/`description`/`close_reason` as undifferentiated text.
- **"How he works" — a characterization of his working style** (iterates by rejection, punishes both asking-when-derivable and acting-without-a-ruling) — no bead field models a *person's* working style; this is orthogonal to any single work item.
- **"What landed" — a structured account of multiple cross-repo commits as completed fact**, with a table (role/depth/model matrix) — a bead's `dependencies`/`close_reason` can reference commits in text but has no tabular or multi-repo-commit-ledger field; the real handover's landed-work table has no analog.
- **"Open, needing the psyche" — a numbered list of specific unresolved questions**, each addressed to the psyche and requiring a ruling — closest to a bead's `blocked` status plus a comment, but a handover's open-questions list is addressed to a *person* for a *decision*, not modeled as work blocked on another *bead*.
- **"Research already paid for, still unconsumed" — pointers to specific commissioned research documents with one-line theses**, explicitly framed as "read before re-deriving" — a bead's `spec_id`/`dependencies` can point at one artifact but has no field for an annotated reading list with per-item theses.
- **"My own failures this session, so they are not repeated" — a self-critique log** — no bead field models an agent's own procedural failure independent of the task's outcome.
- **A focus-scoping rule**: the pre-slashdown `context-handover` module states the handover must be scoped to one focus and must **exclude** "the session's own opinions, recommendations, and interpretive framings" and "reasoning trails, apologies, tool and work chronology, stale branches, resolved mistakes, routine working-copy state" — a bead has no scoping mechanism; it is inherently one work item, not a filtered view over a whole session.
- **Ephemerality of the handover artifact itself**: both the current and pre-slashdown context-handover doctrine say "Print handover content in the agent response. Never write a handover to a file" — i.e. by design a handover is *not* meant to persist as a queryable record at all (though in practice, per the report paths found, they are sometimes written to `reports/` anyway, e.g. `reports/logos/protos-engine-psyche-handover-2026-07-20.md`, `2026-07-21.md`, `reports/logos/psyche-vision-handover-2026-07-19.md`, `reports/field-readiness/HANDOVER.md`, several `reports/legacy-disposition/HANDOVER-*.md` files) — a bead, by contrast, is always a persistent, queryable, ID-addressed row.

**What a bead carries, with no field in a handover document:**

- **A stable, queryable identifier** (`id`) other artifacts can reference and `bd dep` can link against — a handover is a prose document with no addressable sub-parts.
- **A typed status/lifecycle** (`open`/`in_progress`/`blocked`/`deferred`/`closed`, with `bd update --claim`/`bd close` as state transitions) — a handover has no state machine; it is written once, per the "ends active lanes" rule ("Do not inherit a lane through handover; the next worker receives a new lane").
- **A typed dependency graph** (`parent-child`, `blocks`, `tracks`, `related`, etc.) connecting it to other structured items — a handover's "References" section is prose pointers, not typed, directional, machine-traversable edges.
- **Priority as a queryable, sortable scalar** (`bd list --priority`/`--sort priority`) — a handover has no priority field; everything in it is, by its own doctrine, already filtered to what matters.
- **Labels for cross-cutting classification and bulk querying** (`bd list --label`) — a handover has no equivalent; it is a one-off document, not part of a queryable population.
- **An audit trail of field changes** (`.beads/interactions.jsonl`, §1/§8) — every status/priority change is timestamped and attributed; a handover has no change history of its own (each new handover is a fresh document, not a diff against the last one).
- **Assignee/owner as structured fields** (`bd assign`, `owner`) — a handover has no notion of "assigned to X"; it is addressed to whoever opens the next session.

## 10. Skill-to-skill references — what's actually supported

**The skills-repo generator (`/git/github.com/LiGoldragon/skills/src/assembly.rs`, `manifests/module-dependencies.nota`, `manifests/skill-module-compositions.nota`, `manifests/target-module-insertions.nota`) does have a dependency/composition graph — but it operates only at build time, over "modules" (the reusable prose fragments like `modules/work-tracking/full.md` recovered in §8), not at agent-runtime over "skills."** `ModuleIndex::expanded_paths` (assembly.rs, ~line 1224) walks `module_dependencies` to expand a list of module identifiers into an ordered list of module paths, which the generator then concatenates into a single flat output file per skill or per role packet (`ModuleExpansion::append`, guarding against `Error::ModuleDependencyCycle`). By the time an agent ever sees a generated skill file (e.g. `skills/skills/work-tracking.md`), it is already fully flattened, static prose with no live links back to other modules or skills — there is nothing left at runtime for any loader to resolve. This mechanism answers "how is one skill's text assembled from reusable fragments," not "can skill A cause skill B to load."

**No frontmatter field for a skill declaring a dependency on another skill was found in any of the three loaders':**

- **Pi** (`/home/li/.local/share/criomos/pi/package/docs/skills.md`) documents the full `SKILL.md` frontmatter field set explicitly: `name` (required), `description` (required), `license`, `compatibility`, `disable-model-invocation`. No `depends`/`requires`/`see-also` field exists. Pi explicitly implements "the [Agent Skills standard](https://agentskills.io/specification)," the same standard Claude Code's own skill format follows, so the absence of a dependency field here is strong evidence Claude Code's frontmatter has none either (not independently verified against an Anthropic-authored spec document in this pass). Pi's own description of the loading mechanism: "At startup, pi scans skill locations and extracts names and descriptions... The system prompt includes available skills in XML format... When a task matches, the agent uses `read` to load the full SKILL.md (models don't always do this; use prompting or `/skill:name` to force it)" — i.e. progressive disclosure with the *agent's own judgment or an explicit human command* as the only two paths to loading a second skill, not a declared dependency the harness resolves automatically.
- **Codex** (`/tmp/openai-docs-cache/codex-manual.md`) documents `skills.config` as a per-skill enable/disable toggle (by `path`) and documents skills as something Codex can be told to invoke (`$codex-security:security-diff-scan`, `Use $codex-security:triage-finding to...`) or that AGENTS.md/skill text can request subagent delegation for — no dependency-declaration field or mechanism between two skills was found in this cache.
- **The generated `codex-skill-loading.md` module** (`/git/github.com/LiGoldragon/skills/skills/codex-skill-loading.md`, current terse form) states only: "Do not reload a complete pasted skill unless freshness or source verification is required" — implying Codex's own convention is to paste a skill's full body inline once loaded (consistent with no lazy/reference-based re-fetch mechanism), and explicitly discourages redundant reloading rather than describing any chaining capability.

**Conclusion actually supported by the evidence:** all three loaders use progressive disclosure — name + description always resident, full body loaded on demand — and description is consequently the only field in reach for such an instruction. But none of the three loaders parses the description (or any other frontmatter field) for a machine-actionable "read skill X" directive; a skill telling an agent to read another named skill would be **plain prose in the body or description**, acted on only if the agent chooses to (or is told to) invoke its own `read`/`Skill` tool against that other skill — there is no declared-dependency field, and no automatic expansion, in the generator or in any of the three runtime loaders.
