# Flow on ethos-zero 29.0.0 (branch ethos29-521d44)

Branch `ethos29-521d44` of LiGoldragon/flow, head `711b28ed3b82fc0a8146ae74587d7ebc583c3729`, one commit on origin/main eabddc8d29ddd30b4665065cec4bee57ea7410ce (Flow 0.56.2, verified). Pushed, not merged, nothing deployed. Worktree `/git/worktrees/flow-ethos29-521d44`.

meta-signal-flow: **no branch, no change**. Its refusals are wire types (see "Stopped"), so it stays at cdb4e7df3e52065c8c28c6f936e2f6f6fa285c9b on ethos-zero 27, as Flow pins it. The scratch worktree and local branch I made were removed.

## Changed in Flow

1. **Dead landing pipeline removed**: `crates/flow-nexus/ethos/landing.ethos`, `crates/flow-nexus/src/generated/landing.rs`, and the `"landing"` entry of `crates/flow-nexus/build.rs`. `LandingWatch` and `Start`'s `Option<LandingWatch>` stay (wire position). Nothing else referenced the ethos or its module.
2. **ethos-zero 27.0.0 8c95310 to 29.0.0 f23eacf** in flow-ethos, flow, flow-meta and flow-nexus (`Cargo.toml` of each). `Cargo.lock` (new 29.0.0 package, the four members move onto it; 22.0.0 and 27.0.0 stay, 27 for meta-signal-flow's own build dependency), `Cargo.nix` and `crate-hashes.json` (`ethos-zero?rev=f23eacf#29.0.0`) regenerated with the locked build-base's crate2nix.
3. **Refusals fixed** (all in-process types or one printed datom; none stored, none on a Signal):
   - flow-ethos `library.ethos` and flow-nexus `startup.ethos`: `StartRefusal.[ Store.StoreRefusal ]` removed; the startup refusal is the `StoreRefusal.{ Path Reason }` itself, used bare. `main.rs` builds and parses `flow_ethos::StoreRefusal`; the printed datom is now `{ <path> <reason> }` where it was `Store.{ <path> <reason> }`. Nothing in the repository reads that text (searched crates, capsule, launcher, nix, docs); its test is updated. Called out because it is printed output of a refused start, should anything outside the repository read it.
   - flow-nexus `emission.ethos` (all in-process Emission types):
     - `ShellLine.[ PrepareClaudeEnvironment.ClaudeEnvironment ]` is gone; `RunInPane` carries `ClaudeEnvironment` directly.
     - `MetadataSource.[ Flow ]`, `ScreenFormat.[ Ansi ]` and `CodexTitle.[ ThreadTitle ]` carried nothing, so the fields are gone; their words (`--source flow`, `--format ansi`, the Codex `tui.terminal_title` setting) are written in the translator `src/emission.rs`, same words and order.
     - `HerdrSocketRequest.[ PromptAgentByName.{ ... } ]` is `PromptAgentByName.{ LaunchRequestId HerdrAgentName PromptText }`, used by `HerdrSocketCall`.
   - Rust follows in `src/emission.rs`, `src/herdr/launch.rs`, `src/herdr/pane.rs`, `src/main.rs`. Not touched: `crates/flow-nexus/src/lib.rs`, the connection and call modules and their tests.
4. **Regenerated with ethos-zero 29** (binary `/nix/store/d9nv1n77gypi90h9jy9vqdb450xd6cgx-all-workspace-members/bin/ethos-zero`): every `.ethos` of Flow generates; only the files whose source changed differ (flow-ethos library, flow-nexus emission and startup). The other nine generated modules are byte-equal under 29. The build.rs freshness checks pass in the gate.

## Stopped: wire types, for Fable (meta-signal-flow ethos/signal.ethos, and tests/fixtures/meta-signal-flow-78.ethos at 366, 372, 591)

All three are Output variants of the meta Signal, so the plainest fix changes the datom and rkyv bytes of a wire type. None is stored in Memory. Not changed.

| enum | where sent | plainest fix | users in Flow |
|---|---|---|---|
| `ReadSendOutcomesRejected.[ StoreRefused ]` (line 380) | meta Output, answer to ReadSendOutcomes | the output variant carries nothing: `ReadSendOutcomesRejected` bare | `crates/flow-nexus/src/lib.rs` (2 uses; file owned elsewhere) |
| `InspectRejected.[ UnknownAddress ]` (line 383) | meta Output, answer to Inspect | the same: `InspectRejected` bare | `src/repairing.rs` (3) and `tests/unit/repairing.rs` (2) |
| `StoreRefusal.[ Store.String ]` (line 597, carried by `Refused` and `ObserveLegacyArchiveRejected`) | meta Output | `StoreRefusal.String`, used bare | `lib.rs` (4), `observe_configuration.rs`, `repairing.rs`; `lib.rs` is owned elsewhere |

Fixing them is a meta-signal-flow major version, and a Flow repin with it. Until then meta-signal-flow's build.rs stays on 27 (Flow's lock keeps ethos-zero 27.0.0 for it).

## build-base

The build-base main (1d75864, ethos-zero 22.0.0, 27.0.0, 28.0.0) carries **no 29.0.0 entry**; no branch carries one. Not changed. To take 29, build-base needs `ethos-zero "29.0.0": "f23eacf338a90ce4a6dea011554724fa6488fcc9"` in `crate-versions.json` and `"29.0.0": { "attaches": [], "features": [ "datom", "default" ] }` in `crate-features.json` (the same feature set as 27.0.0 and 28.0.0). Without it, `checks.crate-versions` and `checks.crate-features` refuse this branch's Cargo.lock and Cargo.nix.

Flow's flake.lock still pins build-base 9706bad (the ethos27-896bac commit); I left it. Flow's lock also holds signal-curriculum-nexus at 4358aa1, while build-base main now sets 4202d8b, so moving the lock onto main would need that lock move as well (the first gate run showed it).

## Gate

Builder prometheus, `nix-fast-build --remote li@prometheus.goldragon.criome --no-nom --no-download --eval-workers 1` on `github:LiGoldragon/flow/711b28ed3b82fc0a8146ae74587d7ebc583c3729#checks.x86_64-linux`, with the build-base input overridden to a scratch copy of 9706bad plus the 29.0.0 entries above (nothing pushed to build-base; the copy and its builder directory are deleted).

- **Exit 0, all 19 checks green**: capsule-witnesses, cargo-nix, configured-package, crate-features, crate-versions, curriculum-cargo-nix, default, doc, flow, flow-defaults, flow-ethos, flow-meta, flow-native, flow-nexus, flow-request-id-immutable-contract-pins, fmt, no-free-functions, no-inherent-methods, request-id-migration-process.
- **Counts equal 0.56.2's gate** (`flows/565bc8/release-0562/gate-eabddc8d.log`): flow-nexus 933 passed, 9 ignored (the brief's 920 passed, 8 ignored counts a different line of the same run; the 0.56.2 log reads 933 and 9 too), flow 32, flow-ethos 7, flow-meta 6, flow-native 3 and flow-defaults 1 passed, none ignored or failed.
- Logs: `/home/li/primary/flows/521d44/gate-711b28e.log` (first run, on build-base main with the entry: everything built and tested, `crate-versions` and so `default` refused it only for signal-curriculum-nexus 4358aa1 against 4202d8b) and `/home/li/primary/flows/521d44/gate-711b28e-base2.log` (second run, the locked base plus 29.0.0: exit 0, results cached from the first).

## Not done

- No Flow version bump and no UPGRADES entry (branch work only); the stored format and the Signal contracts are unchanged, and the one visible change is the printed startup refusal above.
- The pushed revision's own `flake.lock` does not pass `crate-versions` and `crate-features` until build-base carries 29.0.0.

## On build-base d58fa6f

Branch `ethos29-521d44`, new head `c183f26af864576494ff963fd21b4a3e3b8ea68c` (pushed; nothing merged).

- `flake.lock`: the `base` input (build-base) moves from 9706bad to exactly `d58fa6f9f7a509a26cbb383f5cee8a683858cb5a`; the flake input URL stays bare.
- signal-curriculum-nexus moves from 4358aa1 to `4202d8b` (`crates/flow-nexus/Cargo.toml`, `Cargo.lock`, `Cargo.nix`, `crate-hashes.json`). 4202d8b brings no source change, only its own move onto ethos-zero 28.0.0, so Flow's lock gains the `ethos-zero 28.0.0` package (rev 970459d) and signal-curriculum-nexus depends on it; 27.0.0 stays for meta-signal-flow and signal-flow. `crates/flow-nexus/src/lib.rs` and `connection_adapter.rs` are untouched; no source change was needed. meta-signal-flow stays at its current pin.
- `Cargo.nix` and `crate-hashes.json` were regenerated by build-base d58fa6f's crate2nix on the builder (the local cargo is disabled; run with the base toolchain on PATH).
- Gate: nix-fast-build `--remote li@prometheus.goldragon.criome` on `github:LiGoldragon/flow/c183f26a...#checks.x86_64-linux`, no override: exit 0, all checks green including `crate-versions` and `crate-features`. flow-nexus 933 passed, 9 ignored (920 + 10 + 3 passed, 8 + 1 ignored across its test binaries). Log: `/home/li/primary/flows/521d44/gate-c183f26a.log`.
