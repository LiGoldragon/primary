# Verification

## schema-next

Commit: `30a88bee607ac1d590c24152483a994f14c27d07`

Verified:

- `cargo test`
- `cargo clippy --all-targets -- -D warnings`

## triad-runtime

Commit: `de332266ff795f651619cecfb83f97bf3a9a5ea8`

Verified:

- `cargo test`
- `cargo clippy --all-targets -- -D warnings`

## signal-frame

Commit: `6f5a77f11115c043b93d005086cda8cbec349cd4`

Only docs/intent were changed.

## signal-sema

Commit: `c132e9a06431617055bad2a9bae7bbecdeacd4b0`

Verified:

- `cargo test`
- `cargo clippy --all-targets -- -D warnings`

## schema-rust-next

Commits:

- `4ee2c8986fa6`: stream support emission
- `d8e0a37a3d50`: streaming support token wrapper + docs
- `fd84aae25cad`: trace object emission tokenization

Verified:

- `SCHEMA_RUST_NEXT_UPDATE_FIXTURES=1 cargo test --test emission`
- `cargo test --test emission`
- `SCHEMA_RUST_NEXT_UPDATE_BIG_EXAMPLES=1 cargo test --test big_emission`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`

## spirit

Commits:

- `a2df81768d5a`: stack pins + exemplar documentation
- `885aa9325e17`: complete Nix local override proof + regenerated schema

Verified:

- `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo test`
- `cargo test`
- `cargo test --all-features`
- `cargo clippy --all-targets --all-features -- -D warnings`
- direct `nix build --print-out-paths --no-link ... path:/git/github.com/LiGoldragon/spirit#default` with the complete local override set
- `SPIRIT_NIX_BUILD_RESULT=/nix/store/zy4ffjpp4rfvl35ny67xab1k4cq0wgs4-spirit cargo test --all-features --test nix_integration -- --ignored --test-threads=1`
- `scripts/run-nix-integration-tests --test-threads=1`

The final script proof built `/nix/store/dyp1r5mm68dlqq801r5kkfdcg1fzaxd2-spirit`
and passed all 9 ignored Nix-built binary integration tests.

## Remote state

Remote `main` was verified for every touched code repo:

- `schema-next`: `30a88bee607ac1d590c24152483a994f14c27d07`
- `schema-rust-next`: `fd84aae25cad15f79d9945b0ba2cd3d5ef5dd72a`
- `triad-runtime`: `de332266ff795f651619cecfb83f97bf3a9a5ea8`
- `signal-frame`: `6f5a77f11115c043b93d005086cda8cbec349cd4`
- `signal-sema`: `c132e9a06431617055bad2a9bae7bbecdeacd4b0`
- `spirit`: `885aa9325e17e4b8d058ff14af2e0793d3e48fda`
