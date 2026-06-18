---
title: 424/3 — Nix and workspace hygiene audit
role: operator
variant: Audit
date: 2026-06-18
topics: [nix, workspace-hygiene, remotes, jj, worktrees]
parent_meta_report: reports/operator/424-Refresh-context-maintenance-audit
slot: 3
description: |
  Bounded read-only audit of the last few days' operator work around Nix
  remote-only discipline, missing flakes, forbidden local path references,
  active repository registration, orchestration locks, jj push bookmarks, and
  worktree cleanliness.
---

# 424/3 — Nix and workspace hygiene audit

## Scope

This is a read-only hygiene pass over the repositories named by the `424`
frame and the recent operator trail `406` through `423`: `criome`,
`signal-criome`, `meta-signal-criome`, `signal-standard`,
`signal-mentci`, `meta-signal-mentci`, `mentci`, `mentci-lib`,
`mentci-egui`, and the `schema-next` namespace worktree.

No code, lock, active-repository, Nix, Cargo, or jj state was intentionally
changed. The only write from this subagent is this report.

## Commands

| Command | Purpose | Result |
|---|---|---|
| `nix config show \| rg '^(builders\|builders-use-substitutes\|max-jobs\|substituters\|trusted-public-keys\|trusted-users)'` | Inspect daemon-side Nix configuration without searching `/nix/store`. | Remote builder file is configured; local `max-jobs` remains `1`. |
| `sed -n '1,80p' /etc/nix/machines` | Inspect the configured remote builder line named by Nix. | `ssh-ng://nix-ssh@prometheus.goldragon.criome` is configured for `x86_64-linux`. |
| `rg -n '(criome\|signal-criome\|meta-signal-criome\|signal-standard\|signal-mentci\|meta-signal-mentci\|mentci\|mentci-lib\|mentci-egui\|schema-next)' protocols/active-repositories.md` | Check active repository registration. | All audited repos are registered except `mentci-egui`. |
| `tools/orchestrate status` | Inspect live lane locks. | Only `operator.lock` is active, on `/git/github.com/LiGoldragon/mind`; no audited repo is locked. |
| `tools/orchestrate verify-jj` | Scan active repositories for `push-*` bookmark hygiene. | Exit `2`: unrelated stale/delete candidates exist; audited active repos have zero `push-*` bookmarks. |
| `jj -R <repo> st --no-pager` and `jj -R <repo> bookmark list --all-remotes` | Check touched repo cleanliness and local/remote `main` alignment. | All audited canonical repos are clean; local `main` matches `origin` in the local jj remote view. |
| `rg -n '(path:/git\|git\+file:\|url\s*=\s*"path:\|path\s*=\s*"/git\|/git/github.com\|--override-input[^\n]*path:)' ... -g 'flake.nix' -g 'flake.lock' -g '*.nix' -g 'Cargo.toml' -g 'Cargo.lock'` | Search touched repo Nix/Cargo surfaces for forbidden local paths. | No matches. |
| `rg -n '"type": "path"\|path:/git\|git\+file' <flake.lock files>` | Check flake locks for local path nodes. | No matches. |
| `rg -n '/nix/store/' ... -g 'flake.nix' -g 'flake.lock' -g '*.nix' -g 'Cargo.toml' -g 'Cargo.lock'` | Check touched repo config files for frozen store paths. | No matches. |
| `rg -n '(path:/git\|git\+file:\|--override-input[^\n]*path:/git\|/nix/store/)' reports/operator/40[6-9]-*.md reports/operator/41[0-9]-*.md reports/operator/42[0-3]-*.md` | Check recent reports for forbidden-path claims or raw store paths. | No actual local override use; operator `410` pastes two raw `/nix/store/...` outputs. |
| `find /home/li/wt/github.com/LiGoldragon -mindepth 2 -maxdepth 2 -type d -print` | List feature worktrees under the LiGoldragon namespace. | Many worktrees exist; focused checks covered the recent criome, schema-next, and signal-standard worktrees. |

## Nix Discipline

The code/config side is clean for the forbidden pattern the prompt named:
there are no `path:/git/...` overrides, no `git+file:` flake refs, no `/git`
absolute Cargo path dependencies, and no raw `/nix/store` literals in the
audited `flake.nix`, `flake.lock`, `*.nix`, `Cargo.toml`, or `Cargo.lock`
surfaces.

Recent report evidence mostly follows remote-ref discipline:

| Report | Nix evidence shape | Hygiene note |
|---|---|---|
| operator `406` | `nix build --refresh ... github:LiGoldragon/criome/main#...` | Good remote flake ref shape. |
| operator `410` | `git+https://github.com/LiGoldragon/...?...#checks...` | Remote ref is good, but the report pastes raw store paths and uses `--builders ''`, so it is not a remote-builder proof. |
| operator `414` and `415` | `nix flake check github:LiGoldragon/.../<rev>` | Good immutable remote-ref proof. |
| operator `419` | local `nix flake check --print-build-logs` on a dirty snapshot, then cached clean run | Weak as standalone proof, but later operator `420` covers the same repos with pushed remote refs. |
| operator `420` | `nix flake check ... 'git+ssh://git@github.com/LiGoldragon/<repo>?ref=main'` | Good remote ref shape, chosen because unauthenticated `github:` hit rate limits. |
| operator `423` | `nix flake check github:LiGoldragon/signal-standard` and `github:LiGoldragon/mentci-lib` | Good for repos with flakes; notes that new Mentci component repos still lack flakes. |

The current daemon config supports remote builders:
`builders = @/etc/nix/machines`, and `/etc/nix/machines` points at
`ssh-ng://nix-ssh@prometheus.goldragon.criome`. I did not run a fresh
remote-builder smoke test in this audit. If the next report wants to prove
builder scheduling, the witness should be a small uncached remote-ref build
with `--option max-jobs 0 --option builders '@/etc/nix/machines'`, and any
returned store path should stay in a shell variable rather than being pasted
into prose.

## Flakes

| Repository | `flake.nix` | `flake.lock` | Nix gate status |
|---|---:|---:|---|
| `criome` | yes | yes | Remote flake checks exist in recent reports. |
| `signal-criome` | yes | yes | Remote flake checks exist in recent reports. |
| `meta-signal-criome` | yes | yes | Flake exists; not a focus of the recent Nix reports. |
| `signal-standard` | yes | yes | Remote `nix flake check` passed in operator `423`. |
| `signal-mentci` | no | no | Cargo/clippy only; Nix gate unavailable. |
| `meta-signal-mentci` | no | no | Cargo/clippy only; Nix gate unavailable. |
| `mentci` | no | no | Cargo/clippy only; Nix gate unavailable. |
| `mentci-lib` | yes | yes | Remote `nix flake check` passed in operator `420` and `423`. |
| `mentci-egui` | yes | yes | Remote SSH flake check passed in operator `420`; not scanned by `verify-jj` because it is not registered active. |
| `schema-next` | yes | yes | Flake exists; namespace POC worktree report ran `nix flake check`. |

The actionable flake gap is narrow: `signal-mentci`, `meta-signal-mentci`, and
`mentci` need flakes before Mentci can claim all new component repos are
Nix-gated. That matches operator `423`'s remaining-work note.

## Active Repository Map

`protocols/active-repositories.md` includes the newly active core repos:
`signal-standard`, `mentci`, `signal-mentci`, and `meta-signal-mentci`. It also
includes `schema-next`, `signal-criome`, `meta-signal-criome`, `criome`, and
`mentci-lib`.

`mentci-egui` is the only touched repo absent from the active map. That may be
right if the egui shell is adjacent rather than active, but it means
`tools/orchestrate verify-jj` will not scan it. Direct jj checks show it is
currently clean and its local `main` matches `origin`.

## Locks And JJ

`tools/orchestrate status` shows one live claim:
`operator.lock` holds `/git/github.com/LiGoldragon/mind` for "port mind
component to current strict contract stack." All other lanes are idle. This
audit did not touch or release that lock, and no audited repo is currently
locked.

`tools/orchestrate verify-jj` scanned 77 active repositories and returned exit
code `2` because of three unrelated `push-*` findings:

| Repository | Bookmark | Finding |
|---|---|---|
| `primary` | `push-assistant-spirit-privacy-test-2026-06-04` | Fourteen-day-old rebase-or-abandon candidate for `assistant: test spirit privacy setting`, adding `reports/assistant/4-spirit-privacy-setting-test-2026-06-04.md`. |
| `primary` | `push-counselor-spirit-privacy-migration-2026-06-04` | Fourteen-day-old rebase-or-abandon candidate for `counselor: spirit privacy mechanism + record migration report`, adding `reports/counselor/4-spirit-privacy-mechanism-and-record-migration-2026-06-04.md`. |
| `signal-spirit` | `push-wsqkzxmkqoqz` | Delete candidate for `signal-spirit: add negative guideline guardian reason`; the same commit is also named by `guardian-negative-guideline-reason`. |

The audited active repos themselves have zero `push-*` bookmarks in
`verify-jj`: `schema-next`, `signal-standard`, `signal-criome`,
`meta-signal-criome`, `mentci`, `signal-mentci`, `meta-signal-mentci`,
`criome`, and `mentci-lib` all report clean bookmark state. Direct checks add
`mentci-egui` to that clean set.

Primary itself is not clean during this meta-report assembly. Before this file
was written, `jj st` showed uncommitted report files from other lanes and
slots: `reports/designer/690-engine-audit/0-frame-and-method.md`,
`reports/operator/424-Refresh-context-maintenance-audit/0-frame-and-method.md`,
and `reports/operator/424-Refresh-context-maintenance-audit/2-reports-intent-audit.md`.
This is expected while the `424` meta-report is still assembling, but the final
orchestrator pass should commit the whole primary working copy, not path-scope
a single report.

## Worktrees

The canonical audited checkouts under `/git/github.com/LiGoldragon/...` are
clean. Local `main` matches `origin` for each audited canonical repo in the
local jj remote view.

Focused worktree findings:

| Worktree | State |
|---|---|
| `/home/li/wt/github.com/LiGoldragon/schema-next/schema-namespaces-poc` | Clean; branch `schema-namespaces-poc` is present locally and at `origin`. |
| `/home/li/wt/github.com/LiGoldragon/criome/cluster-root-admission-ceremony` | Clean; branch is present locally and at `origin`. |
| `/home/li/wt/github.com/LiGoldragon/criome/attested-moment-majority-guard-139` | Dirty: modified `src/language.rs` and `tests/language.rs`. This appears to be active scoped majority-guard work, not part of the already-landed canonical `criome` main state. |
| `/home/li/wt/github.com/LiGoldragon/signal-standard/attendance-fanout-139` | Clean; branch is present locally and at `origin`. |
| `/home/li/wt/github.com/LiGoldragon/signal-standard/main` | Clean but suspiciously named: the worktree directory is `main`, while `@-` is `signal-standard-bootstrap`, behind current `main`. Verify whether this is obsolete before relying on it. |

The broader worktree inventory has many active-looking feature directories
across cloud, router, schema, signal, sema, and spirit topics. This audit did
not inspect all of them; it only checked the recent criome, schema-next, and
signal-standard paths connected to operator `406`-`423`.

## Follow-Up Tasks

1. Add flakes to `signal-mentci`, `meta-signal-mentci`, and `mentci`, then run
   pushed-remote `nix flake check` for each. This closes the current Mentci Nix
   gate gap.

2. Decide whether `mentci-egui` is active enough for
   `protocols/active-repositories.md`. If yes, register it so `verify-jj` scans
   it; if no, leave it out and say in the Mentci synthesis that it is adjacent.

3. Clean the three `verify-jj` bookmark findings: rebase/land/abandon the two
   old primary privacy-report branches, and delete the merged auto `push-*`
   bookmark in `signal-spirit`.

4. Standardize future Nix proof text: use pushed remote refs, avoid
   `path:/git/...` and `git+file:`, avoid `--builders ''` unless the point is
   explicitly local-only, and never paste raw `/nix/store/...` outputs into
   reports.

5. Triage the dirty criome worktree
   `/home/li/wt/github.com/LiGoldragon/criome/attested-moment-majority-guard-139`
   with its owning lane: either finish and push it, or record the blocker and
   leave the branch/worktree intentionally active.

6. Verify whether `/home/li/wt/github.com/LiGoldragon/signal-standard/main` is
   an obsolete bootstrap worktree. If it is obsolete, remove the worktree and
   branch through the normal jj worktree cleanup flow.
