# DOTOS orphan claim recovery audit — 2026-08-04

## Scope and safety boundary

This report records only an Orchestrate ownership transition. No checkout,
file content, Jujutsu operation, bookmark, commit, push, fetch, rebase, or
worktree-record mutation is authorized by this transition. The sole filesystem
write is this report.

## Pre-transition provenance

Both orphan lanes descend from Codex parent session
`019fb972-681d-7d21-bf42-7c56ba4d0645`, not a current Spirit train.

| Lane | Registration | Last known holder/recovery | Claim set |
|---|---|---|---|
| `dotos_components` | namespace `1785523934403578482`, 2026-07-31 20:52:14 CEST; owner `([SessionName Rename] Structural)`; details `[rename component nota surfaces]` | creator `019fb984-89d9-70d2-8776-3bf9d62e33d7`, `/root/components_worker`, Helmholtz; recovery `019fb9b5-8d98-7ba0-8d88-b63c0f990811`, `/root/resume_components`, Euclid; final session event 2026-07-31T19:47:44Z | 26 paths, claim namespace `1785524000218846540`, reason `[dotos rename component roots]` |
| `dotos_foundations` | namespace `1785523910030603253`, 2026-07-31 20:51:50 CEST; owner `([SessionName Discipline] Structural)`; details `[rename DOTOS across foundation signal repositories]` | creator `019fb984-600e-74b1-b266-264679b59faf`, `/root/foundations_worker`, Epicurus; recovery `019fb9b5-69d2-7c71-9af4-d958bdeb1576`, `/root/resume_foundations`, Linnaeus; final session event 2026-07-31T19:48:12Z | 79 paths, claim namespace `1785523920987619867`, reason `[signal family rename work]` |

Read-only corroboration before transition found no `dotos_components` or
`dotos_foundations` session in `SessionsObserved`, no matching Agent record,
and no matching process command line. The auditor also found no worktree row
for either lane. Their session JSONLs end without a terminal handoff.

For every recovery target, pre-state was read without changing the working
copy using `jj --ignore-working-copy op log`, `jj --ignore-working-copy log -r
'@ | @- | main | main@origin'`, and `jj diff --summary`. The 83 ordinary
targets produced stored working-copy diffs; the two stale targets refused only
the diff read with the following existing errors:

- `meta-signal-lojix`: stale since operation `4e1291c8d92b`.
- `signal-lojix`: stale since operation `6fa1f26bd8f8`.

No stale workspace was updated. The pre-state identifies the following exact
dirty/stale recovery set; every name expands to
`/git/github.com/LiGoldragon/<name>`.

### Components — 22 dirty

`cloud`, `criome`, `domain-criome`, `harness`, `listener`, `lojix`, `mentci`,
`mentci-egui`, `mentci-lib`, `message`, `mind`, `mind-judge`, `mirror`,
`orchestrate`, `persona`, `persona-spirit`, `repository-ledger`, `router`,
`spirit`, `system`, `terminal`, `upgrade`.

### Foundations — 61 dirty

`meta-signal-aggregator`, `meta-signal-cloud`, `meta-signal-criome`,
`meta-signal-criome-cargo-source-repair`,
`meta-signal-criome-mentci-contract-migration`, `meta-signal-domain-criome`,
`meta-signal-harness`, `meta-signal-introspect`, `meta-signal-listener`,
`meta-signal-mentci`, `meta-signal-mentci-cargo-source-repair`,
`meta-signal-mentci-client`, `meta-signal-mentci-client-cargo-source-repair`,
`meta-signal-mentci-client-mentci-signal-family-migration`,
`meta-signal-mentci-mentci-signal-family-migration`,
`meta-signal-mind-mind-judge-diagnostic`, `meta-signal-mirror`,
`meta-signal-orchestrate`, `meta-signal-orchestrate-session-lane-clear`,
`meta-signal-persona`, `meta-signal-repository-ledger`, `meta-signal-router`,
`meta-signal-spirit`, `meta-signal-spirit-schema-dotted-syntax-pilot`,
`meta-signal-system`, `meta-signal-upgrade`, `meta-signal-version-handover`,
`signal-aggregator`, `signal-cloud`, `signal-criome`,
`signal-criome-cargo-source-repair`,
`signal-criome-mentci-contract-migration`, `signal-derive`,
`signal-domain-criome`, `signal-domain-schema-dotted-syntax-pilot`,
`signal-forge`, `signal-harness`, `signal-introspect`, `signal-listener`,
`signal-mentci`, `signal-mentci-cargo-source-repair`,
`signal-mentci-client`, `signal-mentci-mentci-signal-family-migration`,
`signal-message-cargo-source-repair`, `signal-mind-judge`, `signal-mirror`,
`signal-orchestrate`, `signal-orchestrator-judge`,
`signal-orchestrator-message`, `signal-persona-cargo-source-repair`,
`signal-repository-ledger`, `signal-router`,
`signal-router-cargo-source-repair`, `signal-sema`, `signal-spirit`,
`signal-spirit-judge`, `signal-spirit-schema-dotted-syntax-pilot`,
`signal-standard`, `signal-system`, `signal-terminal-dependency-cascade`,
`signal-version-handover`.

### Foundations — 2 stale

`meta-signal-lojix`, `signal-lojix`.

### Clean paths deliberately not reclaimed — 20

Components: `agent`, `horizon-rs`, `mind-tests`, `terminal-cell`.

Foundations: `meta-signal-agent`, `meta-signal-message`, `meta-signal-mind`,
`meta-signal-terminal`, `signal-agent`, `signal-domain`, `signal-ethos`,
`signal-logos`, `signal-message`, `signal-mind`, `signal-nomos`,
`signal-persona`, `signal-sema-storage`, `signal-sema-translator`,
`signal-terminal`, `signal-upgrade`.

## Required transition

Retire only the two named orphan lanes, then claim the 85 listed dirty/stale
paths under `dotos_orphan_recovery`. This has no multi-command transaction, so
the replies must be validated with no intervening probes. The separate clean
Spirit worktree claim must use new lane `spirit_luna_docs_train`; the retired
`SpiritV14Implementation` worktree row is preserved as an orphaned bookkeeping
fact and is not changed.

## Post-transition

The transition completed in one noninteractive sequential invocation after the
85-path request had been constructed and counted locally. Each typed reply was
validated before the next command:

1. `(LaneRetired dotos_components)`
2. `(LaneRetired dotos_foundations)`
3. `ClaimAcceptance` for `dotos_orphan_recovery`, echoing all 85 paths in the
   recovery set above.

There was no refusal, partial result, or observed race. Post-observation no
longer contains either retired lane. `dotos_orphan_recovery` is active; its
accepted recovery claim contains 85 paths. None of the 20 clean paths appears
in that request.

### Verified non-mutation boundary

Post-transition `jj status` returned `Working copy changes` for all 83 dirty
targets and the same stale-working-copy refusal for both stale targets: 85
expected states and zero mismatches. The transition invoked only Orchestrate;
it did not run a Jujutsu mutation, filesystem mutation, bookmark operation,
or worktree lifecycle request. This verifies preservation of the pre-existing
dirty/stale working-copy classifications, not a complete before/after equality
ledger for every file content, Jujutsu operation head, or bookmark reference.
Those stronger per-repository comparisons were not retained and are not
claimed here. The pre/post `SpiritV14Implementation` worktree fingerprint is
unchanged:

```text
@   1edbfc4e208cac567c035381e86fbc743d38e3a7 (empty)
@-  44ab8e97c7c7513ea6ef2a3bb81dab8ac4babff8
    spirit: release v14 intent model and destructive v13 migration
main / main@origin = 44ab8e97c7c7513ea6ef2a3bb81dab8ac4babff8
```

The existing worktree row remains unchanged and still says repository `spirit`,
branch/lane `SpiritV14Implementation`, status `Active`, and
`AncestorOfMain`. That retired-lane mismatch is recorded, not repaired.

### New documentation-worktree claim

After confirming that worktree is clean and its parent equals `main`, the new
lane was registered and claimed without touching the checkout:

```text
(LaneRegistered ((SpiritLunaDocsTrain spirit_luna_docs_train
  ([SpiritLunaDocsTrain Documentation] Structural)
  [maintain current Spirit user documentation from clean worktree])
  1785842074757117678 Active))
(ClaimAcceptance (spirit_luna_docs_train
  [(Path /home/li/wt/github.com/LiGoldragon/spirit/SpiritV14Implementation)]))
```

`AgentsObserved` has no old or new orphan-recovery agent record, and
`WorktreesObserved` remains unchanged. No worktree row was registered,
concluded, archived, or otherwise changed.
