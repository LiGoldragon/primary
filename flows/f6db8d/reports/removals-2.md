# Removals 2 — harness dead binaries, interactive Rust relock, two open questions

Subflow of main flow f6db8d. Two items delegated from `unused-survey.md`
and `dependency-survey.md`. Everything below is witnessed by this flow
on this host on 2026-09-11/12 unless marked relayed.

Locks observed before any repository was touched (`orchestrate
'Observe.Locks'`). Two acquired, both released before this report was
written: 1207 `HarnessDeadTestBinaryRemoval` on
`/git/github.com/LiGoldragon/harness`; 1208
`CriomosHomeRustOverlayRelock`, narrowed to
`flake.nix`/`flake.lock`/`modules/home/profiles/min/pi-models.nix`/`modules/home/default.nix`
in `CriomOS-home` after a first, wider request was refused
`PathOverlap` against lock 1019 (`CodexArtifactBrowserFlow`) on other
`CriomOS-home` paths.

## 1. harness — the two dead test binaries (unused-survey item 5)

`harness-claude-artifact-observer-test.rs` (145 lines) and
`harness-claude-session-stream-test.rs` (479 lines) were declared as
`[[bin]]` entries in `harness/Cargo.toml` but appeared in neither
`harness/flake.nix`'s four apps nor its check suite.

**Other-callers check, done before touching anything**, per the
survey's explicit condition: `ClaudeArtifactObserver` (the type both
dead binaries imported) is also used by real library code in
`harness/src/claude.rs` — `ClaudeArtifactEventWatcher::from_observer`
(:328) holds one as a field, and `ClaudeArtifactSnapshot::from_observer`
(:972) reads through one. Neither caller lives in the two dead
binaries. Removing the binaries therefore does not touch the observer
type, its constructors, or either of those real callers.

Change: deleted both source files and their two `[[bin]]` blocks in
`Cargo.toml`. Nothing else in the crate referenced either binary name.

Gate: `nix flake check -L --builders ''` in `harness` — **all checks
passed** (exit 0; only the aarch64-linux system was skipped, as the
check itself reports). `reports/nota-pins.md`'s note that harness's
`cargo update` is blocked upstream (on the retired `nota` package) did
not come into play: `nix flake check` builds against the committed
`Cargo.lock` as-is and does not invoke `cargo update`.

Landed on `main`: `8604a07305fe13b9d4de1b810e7863c247952ed7`. Verified
with `git ls-remote https://github.com/LiGoldragon/harness.git main`.

## 2. CriomOS-home — interactive Rust 1.96.0 → 1.97.1 (dependency-survey Tier 0 item 3)

**Where the input lives.** `rust-overlay` is CriomOS-home's own
top-level flake input (`flake.nix:16-17`), locked at `892c035d7c2f`
(2026-08-13). It is a distinct pin from `rust-overlay_2`'s sibling
inside `herdr`'s sub-lock. Relocking the top-level input alone does not
move the *served* interactive Rust version, though: the actual
toolchain is built in `packages/rust-toolchain/default.nix` as
`(inputs.rust-overlay.lib.mkRustBin { } pkgs).stable."1.96.0".minimal`
— a **hardcoded version string**, not `stable.latest`. Both the lock
and the string had to move together.

Change, on test branch `f6db8d-rust-relock`, branched from `main`
(`caffe9a17cc5`):
- `nix flake lock --update-input rust-overlay` — `892c035d7c2f`
  (2026-08-13) → `ab777f900c3d` (2026-09-11).
- `packages/rust-toolchain/default.nix`: `"1.96.0"` → `"1.97.1"`.

**Gate.** CriomOS-home cannot evaluate standalone: its `system` input is
a deliberate throwing stub (`stubs/no-system`) that only lojix
overrides at real deploy time, and building `checks.x86_64-linux.*` or
`homeConfigurations.*` needs it. Rather than invoke lojix (never
deploy), this flow supplied a **local, non-committed**
`--override-input system 'path:...'` pointing at a one-line stub flake
returning `{ system = "x86_64-linux"; }` — an evaluation-only
substitution, not a deploy. Building
`checks.x86_64-linux.rust-toolchain` against that override produced, in
full: `cargo 1.97.1`, `rustc 1.97.1`, `rustfmt 1.9.0-stable`, `clippy
0.1.97`, `rust-analyzer 1.97.1` — all newly built, not cached. **Green.**

Pushed, not landed: `f6db8d-rust-relock` at
`37db5a8bb435fb4baa9d9b319c7b8e49f31d82c8`. Verified with `git ls-remote
https://github.com/LiGoldragon/CriomOS-home.git f6db8d-rust-relock`.

**Landing note.** The branch is a clean two-line diff (`flake.lock`
input bump + one version string) on top of current `main`
(`caffe9a17cc5`), gated green by the method above. It does not touch
`CriomOS`'s own `rust-overlay` pin, which is a separate top-level input
there (also locked 2026-08-13) that forces CriomOS-home's copy by
`follows` only when CriomOS-home is consumed *through* CriomOS. Anyone
landing this should decide whether to move CriomOS's own pin in the
same sweep — otherwise a build reached via CriomOS's `follows` override
will still resolve rust-overlay to the older revision and undo the
practical effect of this bump for any consumer that goes through
CriomOS rather than through CriomOS-home directly.

## 3. Two determinations on the same branch, neither landed

### 3.1 dependency-survey Tier 3 item 13 — `primary-generated-src`

Re-grepped independently, on `main`, before any change:
`grep -rn primary-generated-src flake.nix modules/ packages/ checks/`
returns exactly one hit — the input's own declaration at
`flake.nix:219`. Zero consumers. This confirms the dependency-survey's
and unused-survey's independent finding.

Separately, this flow found — pre-existing on disk, not created by this
flow — a **different** local branch, `f6db8d-removals` (parent
`4cb132ec04ec`, off `main` `caffe9a17cc5`), that already removes this
exact input (and, in the same commit, the §2.5 fzf/hyprland/sway
residue from unused-survey). That branch is untouched by this flow; it
is recorded here only because it bears on the same open question. It
was not merged, re-based onto, or altered.

### 3.2 unused-survey §2.5 — does importing `pi-models.nix` evaluate?

`modules/home/profiles/min/pi-models.nix` (326 lines) is not in
`modules/home/default.nix`'s `imports` list — confirmed by reading the
list. The file itself opens `# DEPRECATED — Pi is being phased out. Do
not add new models or configuration here.`, which the unused-survey did
not quote.

Test, on the `f6db8d-rust-relock` branch, **not committed**: added
`./profiles/min/pi-models.nix` to the `imports` list in
`modules/home/default.nix`, then built
`homeConfigurations.li.activationPackage` against the local `system`
stub above and a second local, non-committed `horizon` override built
from the live host's own real projection, `/tmp/horizon-ouranos.json`
(root-owned; readable as this user; the same file the unused-survey
noted it could not read as root but which matched the node's gates on
every testable axis). This is a real cluster projection, not a
hand-built fixture — `horizon.users` contains `bird` and `li` as found
on disk.

**Result: it evaluates and builds clean.** `nix build
.#homeConfigurations.li.activationPackage` with `pi-models.nix` imported
produced a `home-manager-generation` derivation, 10 derivations built,
exit 0. No evaluation error, no missing module argument, no assertion
failure. The only diagnostics were two pre-existing
`programs.ssh.matchBlocks`/`programs.ssh` deprecation warnings unrelated
to this module, and the usual `gemini-cli` removal and `stdenv.isLinux`
deprecation warnings seen on every build in this repo.

The import was then reverted (`jj diff --stat` shows only the two
rust-overlay files changed before the push in §2); no trace of the
experiment is on the pushed branch. Per the brief, this is recorded as
a determination, not a landing: **importing pi-models.nix evaluates**,
so the unused-survey's characterization of it as "a bug, not cruft" is
mechanically confirmed, but the file's own deprecation comment ("Pi is
being phased out. Do not add new models or configuration here.") is a
standing tension the main flow — not this determination — should
resolve before anyone actually adds the import.

## Table

| Item | Repository | Branch | Gate | Outcome |
| --- | --- | --- | --- | --- |
| unused-survey #5: two dead harness test binaries | harness | `main` | `nix flake check -L --builders ''` — all checks passed | Removed and landed, `8604a07305fe13b9d4de1b810e7863c247952ed7` |
| dependency-survey Tier 0 #3: rust-overlay relock, interactive Rust 1.96.0 → 1.97.1 | CriomOS-home | `f6db8d-rust-relock` | Local build of `checks.x86_64-linux.rust-toolchain` under a temporary `system` override — cargo/rustc/rustfmt/clippy/rust-analyzer all report 1.97.1 | Pushed, not landed: `37db5a8bb435fb4baa9d9b319c7b8e49f31d82c8`; CriomOS's own separate rust-overlay pin is unmoved (see landing note) |
| dependency-survey Tier 3 #13: `primary-generated-src` | CriomOS-home | (determination only; pre-existing sibling branch `f6db8d-removals` already removes it, untouched here) | Grep re-verification: one hit, its own declaration | Confirmed dead, unreferenced; not acted on by this flow |
| unused-survey §2.5: `pi-models.nix` (326 lines, not imported) | CriomOS-home | `f6db8d-rust-relock` (experiment reverted, not on the pushed commit) | Full `homeConfigurations.li.activationPackage` build with the import added, against the real ouranos horizon projection | Evaluates and builds clean; not landed; file carries its own "being phased out" deprecation notice |

## Sources

- `/home/li/primary/flows/f6db8d/reports/unused-survey.md` §2.3, §2.5 —
  the two harness binaries, `pi-models.nix`.
- `/home/li/primary/flows/f6db8d/reports/dependency-survey.md` §1.2,
  Tier 0 item 3, Tier 3 items 13 — the three Rust toolchains,
  `rust-overlay` lock age, `primary-generated-src`.
- `/home/li/primary/flows/f6db8d/reports/nota-pins.md` — harness's
  blocked `cargo update`.
- Witnessed, this flow, `/git/github.com/LiGoldragon/harness`: `git
  grep`/`grep` over `src/`, `Cargo.toml`; `jj log`, `jj status`, `jj
  diff`, `jj describe`, `jj bookmark`, `jj git push`; `nix flake check
  -L --builders ''` (background run, exit 0, full log at
  `/tmp/claude-1001/-home-li-primary/f6db8d14-1dfe-472d-914e-9c441f852834/tasks/b9rzyi00k.output`);
  `git ls-remote https://github.com/LiGoldragon/harness.git main`.
- Witnessed, this flow, `/git/github.com/LiGoldragon/CriomOS-home`:
  `grep` over `flake.nix`, `modules/home/default.nix`, `packages/`,
  `checks/`; `nix flake lock --update-input rust-overlay`; `nix build
  .#checks.x86_64-linux.rust-toolchain` and `nix build
  .#homeConfigurations.li.activationPackage`, both with a local
  `--override-input system` and (for the second) `--override-input
  horizon` pointing at scratch-directory stub flakes, `--builders ''`;
  `jj log`, `jj status`, `jj diff --stat`, `jj describe`, `jj bookmark`,
  `jj git push`; `git ls-remote
  https://github.com/LiGoldragon/CriomOS-home.git f6db8d-rust-relock`.
- `/tmp/horizon-ouranos.json` — the live host's own projected Horizon,
  used unmodified as the `horizon` override for the `pi-models.nix`
  build.
- `orchestrate 'Observe.Locks'` before any repository was touched; `Lock`
  1207 and 1208, `Release` of both after landing/pushing. Lock 1019
  (`CodexArtifactBrowserFlow`, flow f7941a) was observed and avoided by
  narrowing the CriomOS-home lock request. The 542442-flow lock set and
  the pre-existing `f6db8d-removals` branch were observed and left
  untouched.
- Skills loaded and applied: `subflow`, `spirit`, `behavior`,
  `orchestrate`, `file-editing`, `testing`, `nix-workflow`,
  `nix-input-upgrade`, `versioning`, `flow-evidence`.
