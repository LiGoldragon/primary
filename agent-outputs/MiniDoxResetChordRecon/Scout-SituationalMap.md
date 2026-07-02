# MiniDox Reset Chord Recon Situational Map

## Task And Scope

Read-only reconnaissance for why the user's currently flashed MiniDox appears to remember a `[leader r e s e t]` reboot/reset behavior while the current `/git/github.com/LiGoldragon/kibord` MiniDox keymap reportedly lacks any bootloader/reset leader or chord.

Boundaries followed: no source edits, no flash, no reset, no device mutation, no commit, no push, and no `/nix/store` filesystem search. The only write was this report under `/home/li/primary/agent-outputs/MiniDoxResetChordRecon/`.

## Commands And Sources Consulted

- Local doctrine: `/home/li/primary/AGENTS.md` from the prompt, plus `spirit-query` and `version-control` skill files.
- Spirit query: `spirit "(PublicTextSearch [MiniDox firmware reset leader keyboard])"` returned `(Error [no matching record])`.
- Current repo: `jj status`, `jj log`, `jj bookmark list`, `jj file list`, `jj show`, `jj diff`, `rg`, `find`, `nl`, `sed` in `/git/github.com/LiGoldragon/kibord`.
- Adjacent binary repo: `jj status`, `jj log`, `jj bookmark list`, `jj show`, `jj file list`, `jj diff`, `rg`, `find` in `/git/github.com/LiGoldragon/qmkBinaries`.
- Local prior/nearby search: targeted `find`/`rg` under `/home/li`, `/home/li/primary`, `/home/li/git-archive`, `/git`, and `/git/github.com/LiGoldragon`, excluding `.git`, `.jj`, obvious caches where scoped, and not searching `/nix/store`.
- Remote GitHub: `gh repo list LiGoldragon`, `gh repo view LiGoldragon/kibord`, `gh repo view LiGoldragon/qmkBinaries`, `gh search code`, `gh search commits`, and web search for LiGoldragon/MiniDox/QMK reset terms.
- Upstream QMK at locked commit `b1093e9da5f27253f3db692352daf5cf4ad5b98d` via GitHub API for `keyboards/maple_computing/minidox/keymaps/default/keymap.c`, `readme.md`, and `rev1/keyboard.json`.
- Prior agent outputs: `MiniDoxModernization`, `MiniDoxColemakCorrection`, `MiniDoxFlashReadiness`, `MiniDoxModernTooling`, and `MiniDoxStackRecon`.

## Observed Facts

Current `/git/github.com/LiGoldragon/kibord` state:

- `jj status --no-pager` reports a clean working copy. Working copy `f76a117c` is an empty child of `c08bb77661ac24397cd53c432890280715c59fc2` on `main`, commit message `kibord: restore minidox firmware colemak`.
- `jj bookmark list --all` shows `main`, `main@git`, and `main@origin` at `c08bb776`; `mein@origin` remains at older `c89db1df`, message `(drafted minidox)`.
- Current file list includes only one MiniDox source keymap: `maple_computing/minidox/LiGoldragon/keymap.c`. It also includes `ergodone/coleremak/keymap.c` and tracked backup `ergodone/coleremak/#keymap.c#`.
- Current MiniDox keymap has layers `BASE`, `LOWER`, `RAISE`, and `ADJUST` at `maple_computing/minidox/LiGoldragon/keymap.c:3-8`; only `LOWER_KEY MO(LOWER)` and `RAISE_KEY MO(RAISE)` are defined at lines `10-11`.
- Current MiniDox `ADJUST` layer is all transparent placeholders at `maple_computing/minidox/LiGoldragon/keymap.c:39-43`; `layer_state_set_user` only calls `update_tri_layer_state` at lines `47-49`.
- Current MiniDox rules explicitly set `COMMAND_ENABLE = no` and `BOOTMAGIC_ENABLE = no` at `maple_computing/minidox/LiGoldragon/rules.mk:1-2`.
- Scoped current-repo search for `leader`, `combo`, tap dance, `QK_BOOT`, `RESET`, `reset_keyboard`, `bootloader`, and `r.*e.*s.*e.*t` found no MiniDox reset/leader/chord code.

Nearby non-MiniDox reset/leader evidence:

- `ergodone/coleremak/rules.mk:2` has `LEADER_ENABLE = yes`.
- `ergodone/coleremak/keymap.c:11-14` configures leader timing, including `LEADER_PER_KEY_TIMING`.
- `ergodone/coleremak/keymap.c:34`, `:56`, and `:77` place `KC_LEAD` in the ErgoDone layout.
- `ergodone/coleremak/keymap.c:82` contains a direct `RESET` key on the ErgoDone FN layer.
- `ergodone/coleremak/keymap.c:183-230` defines a `LEADER_DICTIONARY()` with several `SEQ_ONE_KEY(...)` entries, but no literal `r e s e t` leader sequence and no reset action inside the leader dictionary.
- The tracked backup `ergodone/coleremak/#keymap.c#` mirrors the same leader/reset material.

Repository history in `/git/github.com/LiGoldragon/kibord`:

- Commit `5343bc14635201bd860d7ec8b1a612fdf01c507c`, change `mrtutrquvmzsxwxuqqyrvsmrxpksvwsp`, message `kibord: modernize minidox qmk build`, added `maple_computing/minidox/LiGoldragon/{config.h,keymap.c,rules.mk}` and README MiniDox docs. Its added MiniDox keymap already had an all-transparent `ADJUST` layer and no `QK_BOOT` or `RESET`.
- Commit `c08bb77661ac24397cd53c432890280715c59fc2`, change `ltwkuwxotqyxmuwpwklklmprzutnpynu`, message `kibord: restore minidox firmware colemak`, changed only `README.md` and MiniDox base letter keycodes. It did not add or remove reset/bootloader behavior.
- Older commit `c89db1dfaf9b74ba9402b6f7e9c0452b9ba1af02`, change `vzkurumqmvpxzwqslktmvzxqumxlmqku`, bookmark `mein@origin`, message `(drafted minidox)`, changed only `flake.nix`.
- At `c89db1df`, `flake.nix:240-247` declares `LiGoldragon.minidox = mkQmkOS` but points `iuniksDir = ./maple_computing/minidox/one` while setting `keyboardModel = "ergodone"`. `jj file list -r c89db1df` shows no `maple_computing/minidox/one` directory and no MiniDox keymap source in that commit.
- Current `jj log` shows earlier ErgoDone-focused commits such as `45c03ded63bb (add leaderSeq)` and later leader edits, but the tracked source in those older states is `ergodone/coleremak/keymap.c`, not a MiniDox keymap.

Adjacent `/git/github.com/LiGoldragon/qmkBinaries` evidence:

- `jj status --no-pager` reports clean. `main`/`main@origin` are at `5f7fe00d62a920f1b5757b42eda4d479b5f26075`, message `qmkBinaries: refresh minidox firmware`.
- Current files are only `readme.md`, `minidox/left/maple_computing_minidox_rev1_LiGoldragon.hex`, and `minidox/right/maple_computing_minidox_rev1_LiGoldragon.hex`.
- Commit `15d50f4d94a3392ebd66dee8281ceb462a48c668`, message `(init qwertyVersion)`, added both left and right MiniDox hex files.
- Commit `f6e2093debe57ee15acedc88b3dd772cf4071fb5`, change `pmkrlzxkwvlloonmyywoswuprsslpsms`, message `(version basicLeaderChords)`, changed only `minidox/right/maple_computing_minidox_rev1_LiGoldragon.hex`.
- Commit `5f7fe00d62a920f1b5757b42eda4d479b5f26075`, message `qmkBinaries: refresh minidox firmware`, again changed only the right MiniDox hex file.
- `gh search commits --owner LiGoldragon 'basicLeaderChords'` finds the same remote commit at `https://github.com/LiGoldragon/qmkBinaries/commit/f6e2093debe57ee15acedc88b3dd772cf4071fb5`.
- No source code in `qmkBinaries` explains the binary behavior. The commit message is evidence that the right-half MiniDox hex was once built as a "basicLeaderChords" version, but not proof of the exact leader sequence.

Local prior/archived repository evidence:

- `/home/li/git-archive/Mentci-AI/Sources/kibord` exists and contains only the same old-style `ergodone/coleremak` files plus `flake.nix`/`flake.lock`; it has no MiniDox source directory.
- `/home/li/git-archive/Mentci-AI/Sources/kibord/flake.nix:241-245` also references `./maple_computing/minidox/one`, but that directory is absent in the archive.
- Broader targeted local search found repeated archived copies of the same ErgoDone leader/reset keymap under `/home/li/git-archive/Mentci-AI/Sources/mentci-ai/.../kibord/ergodone/coleremak`, but no local archived MiniDox source keymap with a reset leader sequence.
- `/home/li/Pictures/minidox` contains photos including `resetSwitch.jpeg` and `trrs.jpeg`; these were noted as physical-context files but not needed to prove firmware source behavior.

Remote GitHub evidence:

- `gh repo list LiGoldragon --limit 200` found only two clearly relevant LiGoldragon keyboard/QMK repos: `LiGoldragon/kibord` and `LiGoldragon/qmkBinaries`.
- `gh repo view LiGoldragon/kibord` reports default branch `mein`, not a fork, URL `https://github.com/LiGoldragon/kibord`, pushed `2026-07-02T12:37:19Z`.
- `gh repo view LiGoldragon/qmkBinaries` reports default branch `main`, not a fork, URL `https://github.com/LiGoldragon/qmkBinaries`, pushed `2026-05-30T05:28:36Z`.
- Remote code search for LiGoldragon `minidox` mostly found prior `primary` agent-output reports, not source. Remote code search for LiGoldragon `leader`/`RESET`/`QK_BOOT`/`KC_LEAD` produced no remote MiniDox source hit beyond those reports and noisy unrelated results.
- Web search did not surface another LiGoldragon MiniDox/QMK source repository or fork with a reset leader sequence.

Upstream/default QMK evidence at locked QMK commit:

- Upstream MiniDox `readme.md:7-8` says the hardware is `MiniDox PCB rev1 Pro Micro`.
- Upstream `rev1/keyboard.json:21-27` declares `development_board = "promicro"`, `bootmagic = false`, `mousekey = true`, `extrakey = true`, and `command = true`.
- Upstream default MiniDox keymap has no leader dictionary. It defines custom `LOWER`, `RAISE`, and `ADJUST` keycodes at `keyboards/maple_computing/minidox/keymaps/default/keymap.c:15-19`.
- Upstream default MiniDox keymap's Adjust layer comment labels a `Reset` key at line `100`, and the actual keycode is `QK_BOOT` at line `111`.
- The upstream default reset behavior is therefore a tri-layer `QK_BOOT` key, not `[leader r e s e t]`.

Prior agent-output evidence:

- `MiniDoxModernization/GeneralCodeImplementer-Evidence.md` says commit `5343bc14` added the current MiniDox source and "Leaves adjust layer without a bootloader/reset key because flashing is out of scope."
- `MiniDoxColemakCorrection/GeneralCodeImplementer-Evidence.md` says commit `c08bb77661ac24397cd53c432890280715c59fc2` changed only MiniDox base layer letter keycodes and README OS-layout wording.
- `MiniDoxFlashReadiness/Scout-SituationalMap.md` independently observed no programmed bootloader entry key/chord in current MiniDox files, and noted adjacent `qmkBinaries` hex files as reference artifacts only.

## Answers To Required Questions

1. Current or untracked/generated/alternate keymaps in `/git/github.com/LiGoldragon/kibord`:

- Current MiniDox files contain no leader, combo, tap dance, `QK_BOOT`, `RESET`, `reset_keyboard`, bootloader key, or `r/e/s/e/t` sequence.
- The current repo does contain non-MiniDox ErgoDone leader/reset code: `ergodone/coleremak/rules.mk:2`, `ergodone/coleremak/keymap.c:11-14`, `:34`, `:56`, `:77`, `:82`, and `:183-230`, plus the tracked backup `ergodone/coleremak/#keymap.c#`.
- No untracked MiniDox source file was found; `jj status` is clean.

2. Repository history evidence for prior MiniDox reset leader/chord:

- No `kibord` source-history commit found a MiniDox keymap with `[leader r e s e t]`.
- No `kibord` source-history commit found a MiniDox leader, combo, or tap dance reset behavior.
- `kibord` history does show older ErgoDone leader/reset behavior and the current MiniDox source added in `5343bc14` without reset behavior.
- The strongest MiniDox-specific prior artifact is in a separate repo: `LiGoldragon/qmkBinaries` commit `f6e2093debe57ee15acedc88b3dd772cf4071fb5` / change `pmkrlzxkwvlloonmyywoswuprsslpsms`, message `(version basicLeaderChords)`, changing only `minidox/right/maple_computing_minidox_rev1_LiGoldragon.hex`.

3. Could currently flashed firmware plausibly come from older local commit, uncommitted work, another branch/bookmark, another repo, or upstream/default QMK behavior?

Evidence:

- Older `kibord` bookmark `mein@origin` at `c89db1df` referenced a MiniDox output but did not include the MiniDox source directory it referenced.
- Local archive copies also reference `./maple_computing/minidox/one` but do not contain it.
- `qmkBinaries` contains MiniDox left/right hex artifacts, including a historical commit explicitly named `(version basicLeaderChords)`.
- Upstream QMK default MiniDox has a tri-layer `QK_BOOT` key at Adjust position line `111`.

Inference:

- The currently flashed reset behavior could plausibly come from a prior local source tree that existed when `c89db1df` referenced `./maple_computing/minidox/one`, but that source tree is not present in the checked local repos or archives inspected.
- It could plausibly come from the `qmkBinaries` right-half hex at `f6e2093d` because the commit message says `basicLeaderChords`, but the exact `[leader r e s e t]` sequence cannot be proven from the hex-only repository.
- It could plausibly be a remembered variant of upstream/default MiniDox behavior if the user is recalling a reset chord rather than a leader word; upstream default has `QK_BOOT` on Adjust, not a leader sequence.
- It is not supported by the current `kibord/main` MiniDox source and not by the old `kibord/mein@origin` source as currently available.

4. Did recent modernization/Colemak correction remove or overwrite the behavior?

Evidence:

- `5343bc14` added the current MiniDox source from scratch and intentionally left the Adjust layer blank; prior agent evidence explicitly says no bootloader/reset key was included because flashing was out of scope.
- `c08bb77661ac24397cd53c432890280715c59fc2` only restored firmware-level Colemak letters and README wording; it did not touch reset behavior.
- Because no prior MiniDox source keymap with reset behavior is present in `kibord` history, I cannot prove that modernization removed a tracked source behavior. It did overwrite the practical build source with a new MiniDox keymap that lacks upstream default `QK_BOOT` and any remembered leader behavior.

5. Shortest likely explanation and implementation recommendation:

- Shortest explanation: the flashed keyboard is probably running a prior MiniDox hex, most likely related to `qmkBinaries` commit `f6e2093d (version basicLeaderChords)` or a missing local MiniDox source tree once referenced by `kibord` as `./maple_computing/minidox/one`; the current `kibord` source is a modern rebuild and intentionally has no bootloader/reset path.
- Before reflashing, an implementation worker should restore an explicit bootloader-entry path in `maple_computing/minidox/LiGoldragon/keymap.c`.
- The lowest-risk source-backed restoration is to add `QK_BOOT` on the MiniDox tri-layer `ADJUST` layer, matching upstream MiniDox default semantics. Since the user's remembered action is `[leader r e s e t]`, the worker should decide whether to also enable QMK leader and implement a deliberate `leader r e s e t -> QK_BOOT` sequence. That second step is behavior restoration by memory/inference, not source-proven recovery.
- The worker should also document the exact chord/sequence in `README.md` before any flash so the recovery path is not lost again.

## Unknowns And Blockers

- The exact source code for `qmkBinaries` commit `f6e2093d (version basicLeaderChords)` was not found locally or remotely.
- I did not decode AVR machine code from the `.hex` artifacts; the binary repo does not carry C source, and proving a leader sequence from compiled firmware would require reverse engineering beyond this scout pass.
- No physical device reset/bootloader observation was performed by boundary.
- Remote GitHub search is limited to indexed/searchable content and accessible repositories; it found no additional LiGoldragon MiniDox source repo.

## Verification Summary

- Current `kibord` and `qmkBinaries` worktrees are clean by `jj status`.
- Important positive claims are backed by current file paths/lines, `jj` commit IDs/change IDs, `gh` repository/search output, or upstream QMK file content at the locked commit.
- Important negative claims are backed by scoped `rg`/`find` searches over current `kibord`, adjacent `qmkBinaries`, local git-archive copies, likely `/git` keyboard/QMK locations, and remote GitHub searches.
