# Witness: orchestrate 0.29.2 — import datomic::Situated<datomic::Fault>

Subflow of 6329f1. Worktree: orchestrate-situated-6329f1.

## Method

In worktree `/home/li/wt/github.com/LiGoldragon/orchestrate/orchestrate-situated-6329f1`
(from main ef10df213b45, 0.29.1), under Orchestrate Lock 671 (flow 6329f1):

1. Edited `ethos/client.ethos`: changed `datomic:[ Fault ]` to
   `datomic:[ Situated Fault ]`, removed `Situated.{ Option<Extent> Fault }`
   local declaration, changed `Unreadable.Situated` to
   `Unreadable.Situated<Fault>`.
2. Edited `ethos/meta_client.ethos`: same changes.
3. Regenerated `src/generated/client.rs` and `src/generated/meta_client.rs`
   via ethos-zero 0f198968d208 (1.3.1).
4. Updated `src/bin/orchestrate.rs` and `src/bin/meta_orchestrate.rs`:
   replaced `client::Situated(...)` / `meta_client::Situated(...)` with
   `datomic::Situated(...)` at the two construction sites in each file.
5. Bumped Cargo.toml version 0.29.1 → 0.29.2. Added UPGRADES.md entry.

## Emitter output witnessed

```
// src/generated/client.rs (line 6)
Unreadable(datomic::Situated<datomic::Fault>),
// src/generated/client.rs (line 18)
Self::Unreadable(<datomic::Situated<datomic::Fault> as datomic::Corporal<
```

`datomic::Situated<datomic::Fault>` appears in both generated modules.
The local `Situated` struct is gone.

## Tests

```
cargo test: 14 passed (2 lib + 2 client_freshness + 6 live_nexus + 4 ordinary_lock_contract)
cargo clippy --all-targets -- -D warnings: clean
cargo fmt --check: clean
nix flake check -L --builders 'ssh://prometheus': all checks passed
```

## Commit

885f6e3e67ac Import datomic::Situated<datomic::Fault>; remove local Situated; bump 0.29.2

origin/main: 885f6e3e67ac (fast-forward from ef10df213b45)
