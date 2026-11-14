# synchronizer protos 0.33 checkpoint (923d14), NOT completed

- Worktree /git/worktrees/synchronizer-protos033-923d14, local branch protos033-923d14, WIP commit 1b4051c on base b42c9df (origin/main). Unpushed.
- WIP: Cargo.toml version 0.5.0, datom-codec 5cd6219, protos 3c7ade3, ethos-zero 5a5daca, Cargo.lock refreshed.
- Failure: nix flake check checks.x86_64-linux.build on prometheus, 565 errors: removed Datomic/Site/Locus/Situated/Fault/protos::Integer API in src/types.rs and others.
- Horizon blocker: synchronizer uses horizon_lib (src/role_resolution.rs, tests/role_resolution.rs) at horizon-rs 05879e7 (protos 0.26, datom-codec 0.21). horizon-rs origin/main 91abfd7 (horizon-lib 0.15.0) pins protos 15b41da (0.32.2), datom-codec 4dff16b, ethos-zero c2653dd: no published 0.33 Horizon. A 0.33 synchronizer cannot close one codec until Horizon is upgraded.
- Not tested: whether a mechanical 0.33 adaptation builds against a compatible Horizon.
agent worktree /git/worktrees/agent-protos033-923d14 branch protos033-923d14: triad-runtime c3391ee 0.11.0 repin builds fail: triad-runtime 0.11 dropped ComponentArgument::DotosFile (now DatomFile); agent speaks DOTOS text via signal-agent/meta-signal-agent dotos-text. Cloud same pin, nota-text. Blocked on those contracts moving to Datom.
relative-age-display: my candidate 35114f9 in /git/worktrees/relative-age-display-923d14 duplicates 7a00 claim 25801 (candidate c01e); preserved, not published. All checks passed incl freshness; Cargo.toml/ethos Library head/regenerated generated.rs/Decimal newtype/test API notes in UPGRADES.md.
