# Removals — executing unused-survey's "safe unattended tonight" items 1-4, 7, 8

Delegated by main flow f6db8d: take out what's unused, test it, use test
branches. Items 5 (harness) and 6 (orchestrate) skipped — held by a
sibling. Marking convention as in `unused-survey.md`: **[W]** witnessed by
this flow, **[R]** relayed from a prior report.

## Coordination

Acquired two Orchestrate locks before touching shared repos, released
after landing/pushing:

- `1123 F6db8dRemovalsCriomosHome` — every CriomOS-home path touched by
  items 1, 2, 7 plus `CriomOS/flake.lock` (untouched in the end).
  Released after push.
- `1124 F6db8dRemovalsTerminalCell` — `terminal-cell/Cargo.toml`,
  `terminal/Cargo.toml`, `mentci/Cargo.toml` for item 4. Released after
  push.

`Observe.Locks` at the start showed no overlap with any live lock.
Items 3 and 8 (local disk residue, not repo edits) were cross-checked
against the same live lock snapshot before deletion instead of taking
new locks (see §3, §8); nothing acquired a lock on any path I removed.

## 1 & 7 — CriomOS-home: fzf orphans and dead compositor stack

**Never landed on main.** All work on branch `f6db8d-removals` from
`main` (`caffe9a1`), pushed to origin. CriomOS-home's own working copy
had a pre-existing, unrelated uncommitted change
(`packages/codex-artifact-gateway/*`, matching live lock 1019
`CodexArtifactBrowserFlow` owned by flow f7941a) sitting on a separate
commit outside `main`; I built the test branch as a fresh child of
`main` and never touched that commit. **[W]**

Removed, matching the survey exactly:

- `modules/home/profiles/min/fzfDark.nix`, `fzfLight.nix`,
  `fzfBase16map.nix` — re-grepped the whole repo myself: zero references
  anywhere; only `fzfColemak.nix` is reachable from
  `profiles/min/default.nix`. **[W]**
- `modules/home/profiles/min/hyprland.nix`, `sway.nix`, `swayConf.nix`,
  `waybar.nix` — re-grepped: the only estate hits are unrelated same-word
  matches (`swaylock`, `swaync.enable`, a qutebrowser search-engine URL,
  a stylix `waybar.enable` option), not imports. Confirmed absent from
  `homeModules.default`'s import closure. **[W]**
- `checks/keyboard-layout-policy/default.nix` — removed the two assert
  arms and their `readFile`s of `swayConf.nix`/`hyprland.nix` (the arms
  existed only to prove those files stale); kept the three niri assert
  arms, which are the check's real purpose.

**Gate — home generation derivation hash, before and after.** CriomOS-home's
flake throws on `system`/`horizon` until the OS-owned deployment path
overrides them, so a bare `nix eval`/`nix flake check` on `homeConfigurations`
cannot run standalone. Built a small wrapper flake
(`/tmp/.../scratchpad/gate-wrapper`) that takes CriomOS-home as a path
input, overrides only `system`, and calls
`home-manager.lib.homeManagerConfiguration` directly with
`homeModules.default` and a minimal synthetic `horizon`/`user` fixture
(same pattern already used by `checks/codex-remote-control/default.nix`).
Evaluated `activationPackage.drvPath` before my edit and again after
(re-pinning the wrapper's `criomos-home` input to the new working-tree
content in between, no other change):

    before: vn9gwsr2j4hl81sh5lwx7m5c4bvp2dr8-home-manager-generation.drv
    after:  vn9gwsr2j4hl81sh5lwx7m5c4bvp2dr8-home-manager-generation.drv

**Byte-identical.** **[W]** This is strong evidence (drvPath is
content-addressed on every input to the derivation) that removing these
seven files and the check arm changes nothing about what any user's home
generation evaluates to.

Also ran `nix flake check --builders '' --impure` (impure/unfree-allowed
because the repo's own `platform-tools` package throws on the unfree
gate regardless of my change) on the branch: every `packages` and
`devShells` derivation in the flake evaluated clean. `checks` itself hit
`CriomOS-home: no system input was provided` — a structural,
repo-wide characteristic (documented in CriomOS's own `AGENTS.md` for
the sibling flake) unrelated to this diff; the `homeConfigurations`
gate above is the meaningful proof for this change. **[W]**

Pushed: `github.com/LiGoldragon/CriomOS-home` branch `f6db8d-removals`,
commit `4cb132ec04ecf550bfc9a6b0d14a71cf6806889f`.

**Landing note.** Not landed on main — the brief for CriomOS-home items
is explicit: test branch only, never land, never deploy. Ready for a
human or a deploy-authorized flow to open a PR from
`f6db8d-removals` whenever that's wanted.

## 2 — CriomOS-home: dead `primary-generated-src` input

Same branch, same commit as above (bundled — all three touch adjacent
lines/files and share one gate run).

Re-grepped `primary-generated-src` across the whole repo myself: zero
consumers, confirming the survey. **[W]** Removed the four-line input
block from `flake.nix` and ran `nix flake lock`, which dropped the
matching `flake.lock` entry (`Removed input 'primary-generated-src'`,
18 lines). Did not touch `CriomOS/flake.lock`'s transitive line —
re-pinning CriomOS's `criomos-home` input is a deploy decision on a
different repo and out of scope for a never-deploy test branch.

Gate the survey specified — `nix flake check` locally with
`--builders ''` — run and result folded into §1/§7 above (same repo,
same run).

## 3 — Local residue: empty report dirs and confirmed-archived/contained clones

Re-witnessed every item myself, live, immediately before deleting (not
relayed from the survey):

| path | re-witness | action |
|---|---|---|
| `persona-role-general-code-implementer-reports` | `ls -la`: only `.`/`..`, no `.git` | deleted |
| `persona-role-SchemaTrainExpansion-reports` | `ls -la`: only `.`/`..`, no `.git` | deleted |
| `CriomOS-home-spirit-main-f53aacdd` | `git status --porcelain` clean; `git branch --contains HEAD` lists local `worktree-scaffold-path` **and** `remotes/origin/worktree-scaffold-path` — HEAD is pushed | deleted |
| `signal-legacy` | `git status --porcelain` clean; `gh repo view --json isArchived` → `{"isArchived":true}` | deleted |
| `signal-derive-legacy` | `git status --porcelain` clean; `gh repo view --json isArchived` → `{"isArchived":true}` | deleted |

None of the five paths appeared in the live `Observe.Locks` snapshot.
`du -sh` before deletion: 4.0K + 4.0K + 5.2M + 6.3M + 1.6M ≈ 13 MB total.
**[W]**

## 4 — terminal-cell: dead `dotos-text` feature

Test branch `f6db8d-removals` from `main`
(`e44c41a3`, "Port terminal cell to generated terminal Signal contract"),
pushed. Also removed seven stray `result-N` symlinks (nix build-result
symlinks into `/nix/store`, dated Sept 9, untracked) sitting in the
working copy before committing — build residue, not source, left out of
the commit.

Re-verified myself: `dotos-text = []` in `terminal-cell/Cargo.toml` has
no `#[cfg(feature = "dotos-text")]` site anywhere in `terminal-cell/src`.
`terminal/Cargo.toml` declares its *own*, unrelated `dotos-text` feature
on itself (gating a `dep:dotos` optional dependency, not touching
`terminal-cell`'s copy); `mentci/Cargo.toml`'s `dotos-text` mentions are
features on *other* git dependencies (`mentci-lib`, `signal-introspect`,
`signal-mentci`), not on `terminal-cell`. Neither consumer's
`terminal-cell` dependency line requests the feature. **[W]** Removed
the one line.

**Gate, partial.**

- `nix flake check` in terminal-cell (no `--builders ''` — this repo has
  no unfree/eval-only reason to force local building, so it ran through
  the configured remote builder as usual, per the nix-workflow rule
  against building locally): **all checks passed** (packages, apps,
  devShell, formatter, and all 5 derivation checks green on
  `ssh-ng://nix-ssh@prometheus.goldragon.criome`). **[W]**
- `cargo check` in `terminal`: **blocked**, pre-existing and unrelated —
  the repo's working copy already carries a large uncommitted change
  (17 modified files: `Cargo.toml`, most of `src/`, docs) from other,
  unfinished work, and its `[patch."…signal-terminal.git"]` block is
  presently self-contradictory (`error: patch for 'signal-terminal'
  points to the same source, but patches must point to different
  sources`). Not something to fix or commit under this task's lock,
  which covers only `terminal/Cargo.toml`. **[W]**
- `cargo check` in `mentci`: **blocked**, pre-existing and unrelated —
  fails during a transitive dependency's build script
  (`meta-signal-criome`'s `build.rs`) with
  `unresolved import 'schema_rust::bootstrap::BootstrapInterfaceGeneration'`,
  a version-skew error several dependency hops away from
  `terminal-cell`. **[W]**

**Landing note — not landed.** The brief's instruction for item 4 was
"land on main if green," gated by the survey's own prescription (flake
check in terminal-cell, cargo check in terminal and mentci). Two of
those three legs are blocked by breakage that predates and is unrelated
to this change (confirmed above), so the full prescribed gate is not
green even though the structural argument for safety is solid (neither
consumer requests the removed feature, so its removal cannot regress
either build once they're unblocked for their own reasons). Left on
`terminal-cell` branch `f6db8d-removals`, commit
`f572839e1d152936238c009a2552a079f2cef1a6`, pushed. A version bump was
withheld along with the landing — bump when this lands.

## 8 — Orphaned `target/` build output under `/home/li/wt`

Re-witnessed live, not relayed: for every `target/` directory under
`/home/li/wt` (`find /home/li/wt -type d -name target`, 39 found,
totalling the same shape the survey described), I derived each
worktree's repo name and re-ran `git -C <canonical-repo> worktree list`
myself, and cross-checked the worktree root against a fresh
`Observe.Locks` snapshot taken at the start of this task. **[W]**

Result:

- 3 REGISTERED (still linked worktrees of their canonical repo) — left
  untouched: `curriculum-deploy/curriculum-deploy-ProtoformStack-6329f1`,
  `ethos-zero/ethos-zero-keepgoing-6329f1`,
  `orchestrate/orchestrate-keepgoing-6329f1`.
- 6 carry a **live** Orchestrate lock on the worktree root right now —
  left untouched even though `git worktree list` says orphaned, because
  a lock overrides a stale worktree-list reading:
  `listener/listener-wispr-edge-proxy-01a05588` (lock 441),
  `meta-signal-lojix/meta-signal-lojix-datom-542442` (locks 869/870),
  `meta-signal-orchestrate/meta-signal-datom-542442` (lock 855),
  `orchestrate/datom-signal-542442` (lock 853),
  `signal-lojix/signal-lojix-datom-542442` (lock 868),
  `signal-orchestrate/signal-datom-542442` (lock 854).
- 33 are neither registered nor locked — deleted only the `target/`
  directory itself (confirmed each held the standard Cargo shape —
  `CACHEDIR.TAG`, `debug/`, `tmp/` — before deleting; never touched
  anything beside `target/`, so no source was at risk even for the
  three whose worktree root has no `.git` at all
  (`ethos-zero-e3-nexus-runtime`, `meta-signal-ethos-zero-e3-contract`,
  `signal-ethos-zero-e3-contract` — plain directories, not git
  worktrees, but their `target/` is still ordinary rebuildable Cargo
  output).

Full per-directory disposition is at
`/tmp/claude-1001/-home-li-primary/f6db8d14-1dfe-472d-914e-9c441f852834/scratchpad/wt-report.txt`
(session-local scratch, not durable evidence — the table above and the
before/after `df` are the durable record).

## Disk, before and after

Live `df -h /` during this task (shared machine — many other flows were
concurrently running `nix flake check`/build during this window, so the
raw deltas carry that noise; item 3's ~13 MB is far below that noise
floor and is only witnessed via `du` on the five paths, not via `df`):

| point | used | free |
|---|---|---|
| before item 3 | 734G | 136G |
| before item 8 / after item 3 | 736G | 134G |
| after item 8 | 678G | 191G |

Item 8 alone freed **57 GiB** (`df` delta, `789212213248` →
`~727287582720` bytes used — 33 `target/` directories, `du -sch`
summed to 58G before deletion, consistent with the `df` delta net of
concurrent estate activity). Item 3 freed ≈13 MB (`du`-witnessed, not
resolvable in the noisy `df` delta).

## Sources

- `/home/li/primary/flows/f6db8d/reports/unused-survey.md` — the ranked
  items this report executes.
- `/git/github.com/LiGoldragon/CriomOS-home` — `flake.nix`, `flake.lock`,
  `modules/home/profiles/min/*.nix`, `checks/keyboard-layout-policy/default.nix`,
  branch `f6db8d-removals` — read and edited by this flow.
- `/git/github.com/LiGoldragon/terminal-cell`, `terminal`, `mentci` —
  `Cargo.toml` files, read and (terminal-cell only) edited by this flow.
- Orchestrate `Observe.Locks`, taken live at the start of this task and
  re-consulted before every deletion in §8.
- `gh repo view --json isArchived` for `signal-legacy`,
  `signal-derive-legacy` — run by this flow.
- `git status --porcelain`, `git branch --contains`, `git worktree list`,
  `du`, `df` — run by this flow throughout.
