# Producer chain settle: protos, datom-codec, ethos-zero, signal

## Task

Settle the producer chain so each producer pins the final head of its
producers: (1) datom-codec → protos 0.30.1; (2) ethos-zero → protos 0.30.1
and the new datom-codec; (3) signal → all three. Each repository was
claimed with an Orchestrate lock before editing and released once its
gate passed and the commit was pushed. No consumer repositories were
touched.

## What was read

- `orchestrate 'Observe.Locks'` before each claim, to confirm no other
  f6db8d (or any) subflow held the target repository.
- `/git/github.com/LiGoldragon/protos` `Cargo.toml` and `jj log -r main`:
  confirmed main at `171b21f65337983ab624b7b906397a4f1f92c5a3`, version
  0.30.1, matching the brief's stated final protos head.
- `/git/github.com/LiGoldragon/datom-codec` `Cargo.toml`, `Cargo.lock`,
  and `jj log -r main`: confirmed main at
  `5eefe829243399d82eddf3c76204f770e9943f91`, version 0.26.2, pinning
  protos `e8701521a37c698d6a2eb933618b9d5d1c6f6ffb` (0.30.0), matching
  the brief.
- `/git/github.com/LiGoldragon/ethos-zero` `Cargo.toml` and `flake.nix`:
  confirmed main at `da58504926dabe4680bb7863d812846b0f845d86`, version
  8.0.0, pinning protos `e8701521...` and datom-codec
  `18129314966c5043ee659de452b6f976fa319b21` (0.26.1) both in Cargo.toml
  and as flake inputs.
- `/git/github.com/LiGoldragon/signal` `Cargo.toml`: confirmed main at
  `2276ec4227a08526cb667f475827368d02accc72`, version 3.0.1, pinning
  protos `e8701521...`, datom-codec `18129314...`, and ethos-zero
  `da585049...` (build-dependency).

## What was written

Per repository, under an Orchestrate lock (`F6db8dProducerSettle*`,
released immediately after push):

1. **datom-codec** (`/git/github.com/LiGoldragon/datom-codec`): repinned
   `protos` to `171b21f65337983ab624b7b906397a4f1f92c5a3`, ran
   `cargo update -p protos` to refresh `Cargo.lock`, bumped
   `version` `0.26.2` → `0.26.3`. `cargo test --all`,
   `cargo fmt --all -- --check`, `cargo clippy --all-targets
   --all-features -- -D warnings`, `cargo doc --no-deps --all-features`,
   and `nix flake check -L --builders ''` all passed with no fixture
   changes required. Committed and pushed to `main`:
   `627db67f2655efd9f786864009955005fd8ab2ad`.

2. **ethos-zero** (`/git/github.com/LiGoldragon/ethos-zero`): repinned
   `protos` to `171b21f65337983ab624b7b906397a4f1f92c5a3` and
   `datom-codec` to `627db67f2655efd9f786864009955005fd8ab2ad` in both
   `Cargo.toml` (dependency) and `flake.nix` (flake inputs), ran
   `cargo update -p protos -p datom-codec` and `nix flake lock
   --update-input protos --update-input datom-codec` to refresh
   `Cargo.lock`/`flake.lock`, bumped `version` `8.0.0` → `8.0.1`.
   `cargo test --all` (including the `freshness.rs` generation-freshness
   tests) passed with no regenerated fixtures — generation is
   byte-identical against the new producer heads. `cargo fmt`,
   `cargo clippy -D warnings`, `cargo doc`, and `nix flake check -L
   --builders ''` all passed. Committed and pushed to `main`:
   `de3d9928b156f2e1a92d060b7817af201abfdbef`.

3. **signal** (`/git/github.com/LiGoldragon/signal`): repinned `protos`
   to `171b21f65337983ab624b7b906397a4f1f92c5a3`, `datom-codec` to
   `627db67f2655efd9f786864009955005fd8ab2ad`, and `ethos-zero`
   (build-dependency) to `de3d9928b156f2e1a92d060b7817af201abfdbef`, ran
   `cargo update -p protos -p datom-codec -p ethos-zero` to refresh
   `Cargo.lock`, bumped `version` `3.0.1` → `3.0.2`. `cargo test
   --all-features` (including `interface_contract.rs`, which checks the
   generated contract against the authored one) passed with no
   regenerated fixtures. `cargo fmt`, `cargo clippy --all-features -D
   warnings`, `cargo doc`, and `nix flake check -L --builders ''` all
   passed. Committed and pushed to `main`:
   `8f9a0deb701cebbea518679548df4a795affc918`.

No consumer repository was touched.

## Method

Each step: `orchestrate 'Observe.Locks'` to check for a conflicting
claim, `orchestrate 'Lock.{ ... }'` naming the repository path under
`FLOW_ID` f6db8d, edit `Cargo.toml` (and `flake.nix`/`flake.lock` for
ethos-zero) by hand, `cargo update -p <producer>` to move `Cargo.lock`,
then the full local gate (`cargo test`, `cargo fmt --check`, `cargo
clippy --all-targets --all-features -- -D warnings`, `cargo doc
--no-deps --all-features`, `nix flake check -L --builders ''`), `jj
commit -m ...`, `jj bookmark set main -r @-`, `jj git push --bookmark
main`, then `orchestrate 'Release.<lock-id>'`.

## Unknowns

None.

## Sources

- Direct action: this subflow ran every command above on primary,
  under `FLOW_ID` f6db8d. All claims in this report are witnessed by
  this subflow's own tool output (`jj log`, `cargo test`/`fmt`/`clippy`/
  `doc`, `nix flake check -L`, `orchestrate` replies) in this session.
