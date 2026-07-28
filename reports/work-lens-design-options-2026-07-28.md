# Work-lens design options — 2026-07-28

## Purpose and evidence boundary

This is a design proposal for two read-only, editor-neutral surfaces. It does
not choose a terminal, Emacs, Codium, or dedicated-window experience, install
anything, call a mutating control-plane operation, or assert that the proposed
control-plane API exists.

The intent is a compact answer to four different questions that should not be
collapsed into one claim:

1. What is the magnitude and shape of this selected JJ diff?
2. What JJ operation/change context is visible at this particular snapshot?
3. What has Orchestrate explicitly recorded about lanes, claims, worktrees,
   and lifecycle transitions?
4. What work/evidence is recorded in Beads?

The installed JJ 0.40.0, `difft`, Emacs, VSCodium/VisualJJ, and `bd` make the
first surface and a no-change trial **wired**. The proposed pure Orchestrate
control-plane observation and append-only lifecycle receipts are
**contract-only**: the deployed 0.16.0 command rejects `Observe ControlPlane`,
and the reliability audit establishes that existing observations may reconcile
state. The second surface must therefore not query current Orchestrate
observations until the advertised pure-read contract is deployed and proven.

The relevant existing evidence is the [visibility tooling audit](visibility-tooling-audit-2026-07-28.md), the
[Orchestrate reliability proposal](orchestrate-reliability-proposal-2026-07-28.md),
the [estate inventory](estate-inventory-2026-07-28.md), and the
[core operations audit](core-operations-audit-2026-07-28.md). In particular,
a missing local worktree is not cleanup proof, and a working control-plane
socket is not lifecycle proof.

## Stage 1: `change-radar`

`change-radar` is a tiny local command that renders a selected JJ comparison.
It is deliberately a condensation layer, not a new version-control client,
source analyser, agent manager, or editor plugin. It accepts no mutation
subcommand, never invokes `jj` without `--ignore-working-copy`, and holds no
state beyond the lifetime of its process.

### Exact input and output contract

The command accepts a repository directory plus an explicit comparison:

```text
change-radar [--repo PATH] --from REV --to REV
change-radar [--repo PATH] --working-copy-baseline
```

`--working-copy-baseline` is shorthand for the documented default comparison
selected by the tool (initially the parent of the recorded `@` change to `@`),
and its rendered header must expand the actual resolved revisions. A caller
who needs a different comparison supplies both revisions; the program never
guesses a branch, remote, or review base. Before rendering, it resolves a
canonical repository root and captures the resolved `from`/`to` change and
commit identifiers, JJ version, command start/end time, command exit status,
and the current JJ operation identifier where available.

For one comparison it runs these exact read-only subprocesses with a closed
environment and no pager:

```sh
jj --ignore-working-copy --no-pager --color=never diff --from "$from" --to "$to" --summary
jj --ignore-working-copy --no-pager --color=never diff --from "$from" --to "$to" --stat
jj --ignore-working-copy --no-pager --color=never diff --from "$from" --to "$to" --types
```

The adapter parses these three JJ views into one versioned in-memory document:

```text
RadarDocument/v1 {
  repositoryRoot, jjVersion, from, to, observedAt, jjOperationId?,
  snapshotMode: "ignore-working-copy",
  files: [{path, summaryKind, oldType?, newType?, addedLines?, removedLines?,
           magnitudeKnown, labels[]}],
  directories: [{path, filesChanged, filesDeleted, filesTypeChanged,
                 addedLines?, removedLines?, magnitudeKnown}],
  input: [{name, exitStatus, elapsedMs, parseStatus, rawDigest}]
}
```

`summaryKind` is only JJ's added/modified/deleted result. `oldType` and
`newType` are only the file kinds emitted by `--types` (for example, ordinary
file or symlink); a type transition is separate from a line change. A binary
or otherwise non-countable item has `magnitudeKnown: false`, not a fabricated
zero. The command retains raw command output only in process memory and offers
`--show-raw` to print it to the invoking terminal. Parser fixtures are pinned
to the supported JJ grammar/version. A new or malformed grammar is a visible
input failure, never a silently incomplete green report.

Rules for `generated`, `lock`, and `configuration` are an optional declarative
path-rule list packaged with the command. Initial labels can cover explicit
lockfile names, `*.nix`, recognised configuration filenames, and conventional
generated/build paths. They are **attention labels**, not provenance: a path
matching `generated` is not said to be generated, and an unlabelled path is
not said to be hand-written. Per-repository rules may add labels; they cannot
hide deletion/type-change rows or alter raw JJ totals.

### Terminal wireframe

```text
change-radar  primary  @-  ->  @     recorded JJ state • 14:44:36 CEST
JJ 0.40.0 • op 9014e01f • working copy deliberately NOT scanned

! REVIEW FIRST  1 deleted file • 0 type changes • 12 changed files
  DELETE  orchestrate/worktrees.nota                         1 line
  TYPE    none

MAGNITUDE  +1,714  -25 lines (known text) • 12 files • 3 top-level areas
  reports/              10 files  +1,713  -24   [CONFIG?]
  orchestrate/           1 file      +0   -1
  …

HOTSPOTS (path-rule labels; not provenance)
  LOCK/CONFIG? reports/*.md?  (rule disabled by default)
  CONFIG?       orchestrate/worktrees.nota

FILES  [D] deletion  [T] type transition  [A] added  [M] modified
  [D] orchestrate/worktrees.nota
  [M] reports/orchestrate-reliability-proposal-2026-07-28.md  +244
  …

Open safely: copy `jj diff --from <resolved> --to <resolved> -- <path>`
Input: complete • 0 parse errors • press r to show raw, q to quit
```

The tool remains useful without a full-screen interface: plain text is its
baseline, while an optional interactive filter can be a later replacement for
the `FILES` list. Directory totals are path aggregation, not a dependency
tree. The deletion/type section is always above magnitude and cannot be folded
away by a long report list.

### Visual semantics and accessibility

Every important state has a word and shape as well as colour:

| Meaning | Marker and accessible colour | Rule |
| --- | --- | --- |
| deletion | `[D]`, `DELETE`, high-contrast vermilion | always in the first section |
| type transition | `[T]`, `TYPE`, purple | always adjacent to deletions |
| unusually large known line delta | `!`, amber | threshold is stated and configurable |
| ordinary modification/addition | `[M]`/`[A]`, blue/teal | no implication of safety |
| configured/generated/lock attention label | `?` suffix, amber outline | rule match, never provenance |
| fresh complete input | `• complete`, dark/light-safe neutral + green accent | success and completeness are separate fields |
| stale, partial, unavailable, or invalid input | `STALE`, `PARTIAL`, `UNAVAILABLE`, or `INVALID` text plus gray/amber/red | no aggregate conclusion |

Use a colour-blind-safe blue/teal/amber/vermilion palette with sufficient
contrast in both terminal themes. Never encode priority solely through red vs
green; symbols, section order, count, and plain-language labels must survive
monochrome terminals and screen readers. `NO DELETIONS` is shown only after a
successful complete summary/type parse, never as the empty-state fallback.

### Freshness and failure behaviour

The header always says `recorded JJ state` because `--ignore-working-copy`
intentionally avoids snapshotting filesystem changes. It means the display is
non-mutating but can omit edits made after JJ last recorded its working copy.
It must never say “current files” in that mode. A caller can rerun it; the tool
does not poll the repository in the background.

If one input exits non-zero, times out, has unknown grammar, or resolves a
different revision than the header, the screen starts with `INPUT INVALID` and
prints the command name, status, elapsed time, and a safe bounded diagnostic.
It does not merge the other two outputs into a seemingly complete total. If a
path cannot be classified across views, it appears as `[?] uncorrelated` and
the overall result is `PARTIAL`. A missing `jj` executable or a non-JJ
directory is `UNAVAILABLE`; it is not “no changes.”

### Drill-down, without editor coupling

Each row exposes the resolved comparison and path as copyable commands:

```sh
jj diff --from <resolved-from> --to <resolved-to> -- <path>
jj show <resolved-to>
```

The terminal tool may also print a local file path. It must not claim support
for an Emacs, Codium, or VisualJJ URI until the installed version has a tested
link contract. A graphical host can offer “open this local path” adapters, but
the canonical drill-down remains the resolved JJ command and path.

## Stage 2: local read-only Work Lens

Work Lens is a local projection joining four labelled streams. It is not a
control plane and contains no claim, release, lane, worktree, Beads, VCS,
deployment, or agent-lifecycle action. Its refresh controls only rerun
advertised pure reads; there are no write buttons, bulk cleanup actions,
terminal command execution controls, or automatic remediation.

### Source contracts and admission gate

The lens stores only its current derived view in memory. Each source result has
`source`, `schemaVersion`, `requestedAt`, `respondedAt`, `asOf`, `complete`,
`cursor?`, `transportStatus`, `semanticStatus`, `rawDigest`, and a bounded
diagnostic. A local monotonic clock measures age; source timestamps are shown
without pretending clocks are synchronized.

| Stream | Required input | Displayed, and expressly not displayed |
| --- | --- | --- |
| Change radar / JJ | `RadarDocument/v1`; bounded `jj --ignore-working-copy operation log --op-diff --summary` adapter; optional `jj workspace list` adapter | selected comparison, operation IDs/descriptions, change magnitude, workspace names. No claim that an operation description proves a push, rebase, review, or landing. |
| Orchestrate capability | proposed `ControlPlaneObserved/v1` below | exact server build/protocol/capability evidence. A missing, refused, incompatible, or non-pure reply blocks all other Orchestrate polling. |
| Orchestrate ownership | proposed pure, bounded `LanesObserved/v1`, `ClaimsObserved/v1`, `WorktreesObserved/v1`, and `LifecycleObserved/v1` snapshots | row fields and receipt correlations only. No path scan, reconciliation, timestamp touch, side effect, or “absence means abandoned” heuristic. |
| Beads | `bd list --json` plus on-demand `bd show <id> --json`, through a versioned adapter | issue ID, title, status, assignee/claim state when present, dependencies, and explicitly attached evidence/check records. No inference from title, status, or a missing database. |

Proposed canonical preflight reply, in NOTA terms, is:

```text
(ControlPlaneObserved
  (ControlPlane/v1
    [serverVersion buildRevision ordinaryProtocolRevision metaProtocolRevision]
    [(Capability ObserveControlPlane ControlPlane/v1 Pure)
     (Capability ObserveLanes Lanes/v1 Pure)
     (Capability ObserveClaims Claims/v1 Pure)
     (Capability ObserveWorktrees Worktrees/v1 Pure)
     (Capability ObserveLifecycle Lifecycle/v1 Pure)]
    generatedAt))
```

`Pure` is a behavioral promise with a required regression proof: replying must
not read a filesystem worktree, reconcile/reap a store row, change a timestamp,
start work, write a receipt, or otherwise mutate a store. Its server version,
build revision, protocol revisions, capability schemas, and `generatedAt` are
the exact compatibility facts needed by a lens. The daemon may omit a
capability; it may not advertise it as pure merely because it uses an
observation-shaped verb.

The subsequent snapshot schemas must use opaque row IDs and a hard `limit`
with cursor/`complete` semantics. At minimum: lane ID/status/timestamps,
claim ID/lane ID/explicit scope/status/timestamps, worktree ID/lane ID/repo
identity/registered path or redacted-path handle/status/disposition/timestamps,
and append-only lifecycle receipt ID/correlation ID/operation/disposition/
typed reason/timestamp. Free-form prompts, agent transcripts, credentials,
command output, and source content are out of contract. A refusal is a normal
semantic result and must be rendered as such, not treated as an empty table.

The current deployment has not supplied this contract. Until it does, its
Orchestrate panel is `UNSAFE TO POLL — PURE CONTRACT NOT ADVERTISED`, with a
link to the reliability proposal; it must not fall back to screen-scraping
NOTA or call `Observe Lanes` merely to make the dashboard look populated.

### Work Lens wireframe and graphical hosts

```text
┌ Work Lens — local/read-only ─ repo: primary ─ refresh: 14:44:36 CEST ─────┐
│ JJ   ● recorded state  8s   @- → @   12 files  +1714/-25   [Open radar]    │
│ CP   ⊘ unsafe to poll: ControlPlane/v1 missing                              │
│ Beads ● fresh  11s     6 open, 0 in progress       [Open primary-m8w]      │
├───────────────────┬────────────────────────────────────────────────────────┤
│ ATTENTION         │ SELECTED: DELETE orchestrate/worktrees.nota             │
│ [D] 1 deleted     │ JJ: resolved revisions, type old→absent, known -1 line │
│ [!] 1 large area  │ Ownership: unavailable — no pure control-plane proof    │
│ [⊘] agent panel   │ Evidence: no bead relation asserted                     │
├───────────────────┼────────────────────────────────────────────────────────┤
│ CHANGE AREAS      │ DRILL DOWN                                              │
│ reports/ 10 +…    │ copy JJ diff command • copy local path • show raw input │
│ orchestrate/ 1 -1 │ VisualJJ/Emacs/Codium adapter only if locally enabled   │
├───────────────────┴────────────────────────────────────────────────────────┤
│ Sources: JJ complete • Orchestrate unavailable (not zero) • Beads complete  │
└─────────────────────────────────────────────────────────────────────────────┘
```

The same document can be rendered in either of two host forms without changing
its facts:

1. a small loopback-only standalone window/webview with keyboard navigation;
2. an Emacs buffer or Codium side panel that consumes the local document and
   delegates file opening to that editor.

Both hosts use the identical `RadarDocument` and Work Lens source envelopes.
Neither becomes a new JJ or Orchestrate authority, and neither substitutes
VisualJJ's history tree. The eventual choice is therefore an interaction and
attention decision, not an architecture fork.

Freshness labels are per source: default `FRESH` is at or below 30 seconds,
`AGING` is 30 seconds to five minutes, and `STALE` is over five minutes; these
thresholds are displayed and configurable. A successful nonempty `cursor` or
`complete: false` is `PARTIAL`, never a full count. Failure preserves the last
in-memory result only if clearly labelled `STALE (last good at …)`; on a first
failure it shows `UNAVAILABLE`, not zero agents/claims/worktrees. The source
table stays visible at all times so a colourful attention card cannot conceal
that a data source is absent.

### Privacy boundary and non-inferences

Work Lens binds only to the local user/session, makes no network request,
telemetry, cloud sync, screenshot upload, or persistent history by default,
and does not read source files to decorate a diff. It accepts no remote
connection. Full local paths, claim reasons, and Beads descriptions are shown
only on explicit drill-down; the overview uses repository identity and a
redacted path representation. Export, if ever requested, is a separate,
redacted feature rather than an incidental copy of an agent's private work.

It must never infer any of the following:

- that a path's agent/lane claim identifies the author, current editor, or
  exclusive owner of a code change;
- that a deletion is safe, intentional, reviewed, committed, pushed, landed,
  or even present in the unrecorded working copy;
- that a type change, generated/configuration label, line total, or directory
  aggregate reveals semantic impact, architecture, test impact, or provenance;
- that a missing path, stale claim, idle lane, incomplete receipt history, or
  old worktree is abandoned or may be cleaned up;
- that a receipt or a Beads “done” status proves tests passed, deployment
  succeeded, or a stated outcome is true without the linked check witness;
- that a source's silence, refusal, malformed reply, lock contention, or
  unavailable control plane means “nothing is happening”; or
- that an operation-log description establishes its cause beyond what JJ
  explicitly records.

## Smallest no-change trial now

Run this in an existing JJ repository; it installs, writes, claims, refreshes,
or deploys nothing. It is the manual Stage-1 baseline, using only already
installed JJ and the terminal:

```sh
jj --ignore-working-copy --no-pager --color=always diff --summary
jj --ignore-working-copy --no-pager --color=always diff --stat
jj --ignore-working-copy --no-pager --color=always diff --types
```

Review the deletion/type output first, then totals, then a selected
Difftastic-backed `jj diff`. Do **not** include current `orchestrate '(Observe
Lanes)'`, `Observe Worktrees`, or a broad Beads query in the no-change trial:
the current Orchestrate observations are not proved pure, and Beads may be
locked/unavailable. Record those as unavailable rather than widening the
trial's effects or guessing status. A successful short trial should answer one
question only: did the deletion-first, directory-condensed reading order make
a real multi-file agent change easier to review?

## Declarative Nix packaging boundary

No packaging is proposed for activation yet. If the trial is accepted, keep
the layers separate:

| Boundary | Declarative owner and contents | Must not contain |
| --- | --- | --- |
| `change-radar` source package | a dedicated source repository/flake or an agreed existing tooling home; executable, parser fixtures, packaged label rules, unit tests | mutable repository state, editor-specific code, a daemon, or control-plane credentials |
| Home exposure | `CriomOS-home` module exposes the package on `PATH` and a read-only rule-file option | imperative install, extension marketplace update, or a replacement `EDITOR` policy |
| Work Lens package | local renderer/adapter with a loopback-only optional launcher and schema fixtures | Orchestrate mutation client, filesystem cleanup, telemetry, or a persistent transcript store |
| Orchestrate dependency | `orchestrate`/signal schema sources implement and test pure observations and receipts; `CriomOS-home` pins compatible revisions and passes build revision | a GUI workaround that parses mutable current `Observe` text |

Nix evaluation, package build, parser/schema tests, and any Home activation are
separate evidence gates. A candidate must first pass fixture tests for JJ
summary/stat/types parsing, failure rendering, and source-envelope version
mismatch; then independently evaluate and build its flake/module. Activation
requires a separate decision and an after-activation pure-read witness. No
`/nix/store` inspection or managed-output patching is part of this plan.

## Decision that remains with psyche

After a real no-change trial, one UX choice cannot be inferred from the
configuration: should Work Lens primarily live as a **dedicated local window**
or as a **panel/buffer inside the editor already being used**? The common
read-only schema, terminal `change-radar`, VisualJJ deep drill-down, and Nix
boundaries intentionally remain valid for either answer.
