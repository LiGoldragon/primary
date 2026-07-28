# Estate inventory — 2026-07-28

## Scope and method

Read-only snapshot of `/home/li/primary` and `/git/github.com/LiGoldragon`, taken between approximately 14:10 and 14:31 CEST. No fetch, update, merge, commit, push, deletion, deployment, or repository mutation was performed. All repository facts below come from local Jujutsu metadata, so remote facts mean “last locally known”, not live GitHub state.

`bd ready --json` could not be read because another process holds the embedded Dolt database lock. That is an observation about the audit environment, not evidence that no tracked work exists.

The estate changed while this audit ran: primary was clean at the initial snapshot and later had an uncommitted modification to `orchestrate/worktrees.nota`. Treat every cleanliness result as a point-in-time observation, especially primary.

## Executive decision queue

Do not remove, update, or publish any of these without explicit psyche approval.

1. Preserve and assign the five dirty canonical working copies and three dirty pilot workspaces. Their changes may be intentional, and one consists of a sole editor-backup file.
2. Decide whether to repair or retire the two stale canonical workspaces (`meta-signal-lojix`, `signal-lojix`). A stale Jujutsu workspace needs an update before its working-copy truth can be assessed; an update changes state, so it was deliberately not run.
3. Resolve the orphan-like linked worktree `synchronizer-release-train-p0-p2` before any broad worktree cleanup. It points into primary’s Git worktree metadata but Jujutsu reports no repository there; it also contains extensive retained material.
4. Explicitly classify the clean, July 15 cargo-repair/migration workspaces before removing them. Several are clean and at main, but cleanliness plus naming does not prove their work is superseded.
5. Review bookmark divergence/deletion only after deciding the preservation items above. Pushing deleted bookmarks or reconciling divergent bookmarks changes remote or history state.

## Observations

### Estate size and baseline health

| Surface | Observation |
| --- | --- |
| Canonical repositories | 166 top-level roots with both `.git` directory and `.jj` workspace metadata |
| Canonical clean / dirty / stale | 159 / 5 / 2 at the audit snapshot |
| Separate Jujutsu workspaces | 42 top-level roots with `.jj` but no local `.git` directory; 39 clean and 3 dirty |
| Primary | `origin` is `git@github.com:LiGoldragon/primary.git`; `main` is locally aligned with the last-known `@git` and `@origin` at `8626e768` initially; it became dirty during the audit (`orchestrate/worktrees.nota`) |
| Remotes | The canonical roots overwhelmingly use a GitHub `origin`; exceptions observed include upstream `kameo`, and `github` plus local-gitolite `origin` for `signal-repository-ledger` / `repository-ledger` |
| Main bookmarks | 12 canonical repositories have a last-known `main@*` non-convergence, listed below |

The clean canonical roots whose last-known `main`, `@git`, and `@origin` agree are ordinary inventory, not cleanup candidates merely for existing. The audited root includes active infrastructure, component libraries, schema/signal families, content repositories, and retired components. In particular, `domain-criome`, `signal-domain-criome`, and `terminal` label themselves inactive/retired in their main commit messages; that is not evidence authorizing removal of their checkouts or remotes.

### Dirty and stale canonical repositories

| Repository | State | Direct evidence | Required decision |
| --- | --- | --- | --- |
| `CriomOS-test-cluster` | dirty | Modified synthetic cluster fixture files plus new `lib/nestedReachability.nix` and `lib/nestedSpike.nix`; parent `nested-vm-reachability*` | Preserve and identify owner; this is a test-cluster change, not disposable residue |
| `TheBookOfSol` | dirty | Modified/deleted essay, index, personal, and source-extract Markdown files | Preserve; content changes require editorial ownership and cannot be inferred from filenames |
| `meta-signal-mind` | dirty | `src/schema/lib.rs` modified | Preserve; generated/contract provenance unknown |
| `meta-signal-persona` | dirty | `src/schema/lib.rs` modified | Preserve; generated/contract provenance unknown |
| `schema` | dirty | Untracked `schemas/#spirit-min.schema#` editor-backup-style file | Decide whether to recover or discard only after identifying the owning editor/session |
| `meta-signal-lojix` | stale | Jujutsu: working copy not updated since operation `4e1291c8d92b` | Repair-or-retire decision required before any inspection that updates it |
| `signal-lojix` | stale | Jujutsu: working copy not updated since operation `6fa1f26bd8f8` | Repair-or-retire decision required before any inspection that updates it |

### Dirty pilot workspaces

All three are independently bookmarked `schema-vision-redesign-arch-docs` changes and have a modified `ARCHITECTURE.md`; they should be treated as preserved documentation work, not automatically redundant pilot debris.

| Workspace | Parent / bookmark evidence |
| --- | --- |
| `meta-signal-spirit-schema-dotted-syntax-pilot` | parent `meta-signal-spirit-dotted-syntax-pilot`; working-copy description records strict dotted import-path conformance documentation |
| `signal-spirit-schema-dotted-syntax-pilot` | parent `signal-spirit-dotted-syntax-pilot`; working-copy description records strict dotted-syntax conformance documentation |
| `spirit-schema-dotted-syntax-pilot` | parent `spirit-schema-dotted-syntax-pilot`; working-copy description records the same schema-syntax teaching correction |

### Extra workspace inventory and evidence of purpose

“Purpose” is an observation when it comes from the directory/workspace name or parent description; it is not proof that the worktree is still needed. All listed workspaces were clean unless marked otherwise.

| Workspace family | Paths | Evidence of purpose / current state |
| --- | --- | --- |
| CriomOS deployment/recovery | `CriomOS-listener-criome-recovery`, `CriomOS-spirit-domain-all`, `CriomOS-spirit-judge-deploy` | Names and parents point to Listener/Criome recovery, Spirit v11/Domain-All pinning, and remote judge-chain deployment evidence; clean |
| CriomOS-home deployment/recovery | `CriomOS-home-laptop-colemak-merge`, `CriomOS-home-listener-criome-recovery`, `CriomOS-home-listener-zddv4`, `CriomOS-home-spirit-domain-all` | Names and parent commits point to Colemak merge, Listener history recovery, cancel-shortcut work, and Spirit deployment check; clean |
| Cluster / Lojix exploration | `CriomOS-test-cluster-spirit-domain-all`, `lojix-inspect-store` | Names/parents point to a fixed Spirit stack and read-only Lojix store inspection; clean |
| Mentci integration/migration | `mentci-current-graph-integration`, `mentci-dependency-cascade`, `mentci-lib-cargo-migration`, `mentci-lib-mentci-signal-family-migration` | Integration/cascade/migration names; two cargo/migration paths parent at main; clean, candidate only for confirmation |
| Meta-signal Criome/Mentci repair | `meta-signal-criome-cargo-source-repair`, `meta-signal-criome-mentci-contract-migration`, `meta-signal-mentci-cargo-source-repair`, `meta-signal-mentci-client-cargo-source-repair`, `meta-signal-mentci-client-mentci-signal-family-migration`, `meta-signal-mentci-mentci-signal-family-migration` | Cargo-source-repair and schema-contract migration names; several parent at main, others retain named migration commits; clean |
| Meta-signal investigation | `meta-signal-mind-mind-judge-diagnostic`, `meta-signal-orchestrate-session-lane-clear` | Names/parents point to Mind/Judge diagnosis and Orchestrate session-lane lifecycle; clean |
| Schema-pilot family | `meta-signal-spirit-schema-dotted-syntax-pilot`, `signal-domain-schema-dotted-syntax-pilot`, `signal-spirit-schema-dotted-syntax-pilot`, `spirit-schema-dotted-syntax-pilot` | Explicit dotted-syntax pilot names; the meta/signal/spirit workspaces are dirty as detailed above, signal-domain is clean |
| Mind / Orchestrate | `mind-domain-all-repin`, `orchestrate-session-lane-storage`, `orchestrate-writer-ordering` | Named component repin and session-lane lifecycle/ordering work; clean |
| Pi subagents | `pi-subagents-nested-roles-preference-training`, `pi-subagents-nicobailon-closeout`, `pi-subagents-nicobailon-optional-list-consistency` | Named training, closeout, and list-consistency work; clean; no direct evidence of supersession |
| Schema retirement | `schema-structural-pipe-retirement` | Parent says structural pipe syntax retirement; clean |
| Signal component repair/migration | `signal-criome-cargo-source-repair`, `signal-criome-mentci-contract-migration`, `signal-mentci-cargo-source-repair`, `signal-mentci-mentci-signal-family-migration`, `signal-message-cargo-source-repair`, `signal-persona-cargo-source-repair`, `signal-router-cargo-source-repair`, `signal-terminal-dependency-cascade` | Names and parents describe cargo-source repair, contract migration, and dependency cascade; clean; the paths at `main` are review candidates, not proven removable |
| Spirit judge | `spirit-judge-hardening` | Parent says remove bootstrap-only AGENTS pointer; clean |
| Terminal-cell | `terminal-cell-dependency-cascade` | Parent says consume current terminal contract; clean |

There is one additional non-Jujutsu-linked directory: `synchronizer-release-train-p0-p2`. Its `.git` file points to `/home/li/primary/.git/worktrees/synchronizer-release-train-p0-p2`, but `jj --repository` says there is no Jujutsu repo. Its mtime is 2026-07-15 and it contains substantial `.agents`, `.beads`, reports, and `agent-outputs` material. This is the strongest cleanup-risk item: it may be an old primary Git worktree, but no evidence here permits deletion.

### Primary workspaces

Primary records seven Jujutsu workspace entries: `default`, `MindJudgePromptRewrite-NarrowThirdPass`, `MindJudgePromptRewrite-TargetedSecondPass`, `mind-judge-fixture-label-cleanup`, `mind-live-judge-eval-rerun`, `primary-fix-audit-stale-repo-operator`, and `primary-fix-audit-stale-repo-operator-v2`. The four `mind-*` / `MindJudge*` names provide a plausible purpose. The two `primary-fix-audit-stale-repo-operator*` names lack a meaningful current description, so their purpose is unknown. `jj workspace list` does not expose physical paths; no cleanup action should be based solely on these names.

### Bookmark and remote divergence requiring review

The following are last-known non-converged `main` remote-tracking states. They are history/remote decisions, not cleanup proof.

| Repository | Last-known difference |
| --- | --- |
| `mentci-lib` | `main@git` behind 1 commit; `origin` matches local main |
| `meta-signal-criome`, `meta-signal-mentci`, `meta-signal-mentci-client`, `signal-mentci` | `main@git` behind 2 commits; `origin` matches local main |
| `meta-signal-repository-ledger` | `main@github` behind 1; local `@git` and `origin` match main |
| `repository-ledger` | `main@git` behind 1 and `@github` behind 4; `origin` matches main |
| `signal-criome` | `main@git` behind 5; `origin` matches main |
| `signal-frame` | `main@git` behind 6; `origin` matches main |
| `signal-orchestrate`, `signal-orchestrator-message`, `signal-terminal` | `main@git` behind 1; `origin` matches main |

Additional divergence or deletion markers were observed outside `main`, notably in the production-adjacent `CriomOS`, `CriomOS-home`, `horizon-rs`, and `spirit` repositories. Deleted-bookmark markers are also present in `CriomOS-home`, `core-ethos`, `core-logos`, `core-nomos`, `signal-domain`, `signal-message`, `signal-orchestrate`, `signal-sema-storage`, `signal-spirit-judge`, `structural-codec`, `textual-rust`, and `version-projection`. Jujutsu itself warns that pushing these would permanently delete the remote bookmarks. No remote push or bookmark operation was attempted.

### Deployment pointers and service observations

At the snapshot, `/run/current-system` pointed to `nixos-system-ouranos-26.05.20260422.0726a0e`; `/nix/var/nix/profiles/system` pointed to `system-153-link`; the Home Manager profile pointed to `home-manager-952-link`, and its current GC root pointed to a Home Manager generation updated on 2026-07-28 13:42 CEST.

Service observation is inconsistent across read-only queries: one unit-list invocation reported `listener.service` and `orchestrate-daemon.service` active and `spirit-judge.service` failed, while immediate direct `systemctl status/show` calls reported all four named units not found. This could reflect a manager/namespace boundary or an intervening environment change. It is insufficient evidence for a deployment-health conclusion. Do not restart, deploy, or repair from this audit; first choose the authoritative host/manager context.

## Hypotheses, explicitly unproven

1. The clean July 15 cargo-source-repair and dependency-cascade workspaces may be post-landing scaffolds. Their parent at `main` supports that hypothesis for several paths, but does not prove their physical workspace or ancillary files are disposable.
2. The three dirty dotted-schema pilots look like a coordinated documentation pass because all modify `ARCHITECTURE.md` under the same bookmark. The changes may nevertheless differ materially, so deduplication needs content review.
3. The stale Lojix workspaces may be obsolete, but stale metadata can also hide unincorporated work; only a state-changing refresh followed by review would disconfirm either possibility.
4. The `synchronizer-release-train-p0-p2` directory may be a stale primary-linked worktree. Its retained files and active-ish July 15 mtime disconfirm treating it as an obviously abandoned empty directory.

## Unknowns and limits

- No remote fetch was authorized, so this report cannot say whether GitHub changed after the locally cached tracking refs.
- Ownership, active sessions, and the required retention period for every extra workspace are not encoded reliably in Jujutsu metadata.
- The locked beads database prevented checking existing work tracking.
- No exhaustive content diff was read for dirty workspaces; doing so would increase exposure to content unrelated to cleanup and still would not supply owner authorization.
- Deployment service health is unknown until queried from a verified authoritative systemd manager context.

## Recommended approval order

1. Name owners and desired disposition for dirty/stale/orphan-like items.
2. Choose the authoritative deployment/status context and decide whether operational diagnosis is in scope.
3. Review non-main bookmark divergence and deleted markers repository-by-repository.
4. Only then authorize a narrowly scoped, recoverable cleanup plan for confirmed superseded workspaces.
