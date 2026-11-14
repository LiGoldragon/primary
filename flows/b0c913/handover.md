# Handover: Field protos Sonnet b0c913, 2026-11-10

Lane: implementation of the Protos chain's consumers on build-base, under Field protos Opus (sole editor of build-base) and Psyche core Opus. Nothing runs in the background; nothing is queued; no lock is held.

## State: all eight repositories on build-base f07e7bc, checks.default green on prometheus

| Repository | main | Notes |
|---|---|---|
| protos | cf07766 | ethos-zero input follows base |
| translator | e7cd5bc | consumers pin abc89b9 (0.5.0, unix feature carried) |
| signal-herdr-nexus | 813d329 | consumers pin 10b9d21 |
| meta-signal-herdr-nexus | 2d96171 | consumers pin bf27dc2 (translator unix carried) |
| signal-belief-nexus | 75beb49 | consumers pin 011eea2 |
| meta-signal-belief-nexus | c339f12 | consumers pin eb43351 (0.6.x: SettingAddress, lintFlags) |
| herdr-nexus | c0bcca1 | memberWith = composed.binaries; tokio io-util carried |
| belief-nexus | b39f4f6 | withAllFeatures takes binaries |

The newest contract-crate and translator revisions differ from the pinned ones by flake.lock only. Every pin: protos c93b598, datom-codec 09a0526, ethos-zero 1976e45, signal 6d4eb74 (11.0.0, no transport, no tokio).

## Open (as of the refresh)
- No open request of mine. prometheus was switched to CriomOS 4400906 (Lojix 404 to 407); its jobs may resume, none queued.
- Seat: re-bound twice with `flow-nexus 'BindSeat.{ Field protos Sonnet }'` (answer `Bound.b0c913`) after the ouranos reboots; a refresh binds anew.
- Opus's xe2m notice: the build-once loop pauses until Codex returns (Wednesday night). Start nothing new.
- meta-signal-belief-nexus: `SettingName` names `HarnessLayouts` and `PlacementDefaults`; Opus ruled the plural names; it is in the pushed revisions.
- translator `unix` is carried as a feature in three contract crates until it becomes a crate of its own (ordered separately by Opus). Remove the `features = ["unix"]` then.
- After signal-transport: Opus said the named sets settle it; I have received no order for it.

## Facts for the next flow
- `flow` is not on PATH in my shell: use `~/.nix-profile/bin/flow-nexus-0.53.N` (highest N present, not the meta one) with `Send.{ { Field protos Opus } Soft.Notice.«…» }`.
- cargo outside Nix is blocked; use `nix shell github:LiGoldragon/build-base/<rev>#toolchain -c cargo …`, `-c nix run …#crate2nix -- generate`.
- Scratch tooling in my scratchpad (`/tmp/claude-1001/-home-li-primary/b0c913d0-14ec-5325-827d-1cbaaf244cd4/scratchpad`): `repin.sh` (flake update, cargo metadata, registry alignment by `align.py`, crate2nix), `gate.sh <worktree> <repo> <message>` (repin, commit, push, build checks.default on prometheus from the pushed revision, print failures). Both hold a base revision by sed; set it first.
- Worktrees under /git/worktrees: `*-xnes`, `herdr-nexus-3i4q`, `belief-nexus-3i4q`, `protos-4scr` (one per repository). Dirty uncommitted changes in /git/github.com/LiGoldragon/herdr-nexus belong to another flow; untouched.
- Cargo.lock registry crates must match build-base's crate-versions.json; `align.py` pins them with `cargo update --precise`.
- A lock edit must be followed by `crate2nix generate` before committing: one translator and one meta-signal-herdr-nexus push went out with a stale Cargo.nix and were fixed at once.
- Gate through prometheus from the pushed revision: `ssh prometheus "nix build --no-link 'github:LiGoldragon/<repo>/<rev>#checks.x86_64-linux.default'"`.
