# Recursive Domain Scope Deploy

## Scope

Implemented and deployed the correction that `DomainScope` is a typed recursive enum over `Domain`, not a `Vec String`/`DomainPath` wrapper.

The public NOTA scope surface is now:

- `Technology`
- `(Technology Software)`
- `(Technology (Software Security))`
- `(Technology (Software (Security AdmissionControl)))`

The old bracket-string path form, for example `[[Technology Software]]`, is rejected.

## Landed Commits

- `schema-next` `2397d5b2` — adds `ScopeOf` as a schema type reference.
- `schema-rust-next` `86fa189a` — emits typed recursive scope families, path projection, typed `from_path`, NOTA codec, and relation expansion support.
- `spirit` `b3735827` — changes `DomainScope` to `(ScopeOf Domain)`, removes `DomainPath`, regenerates checked-in schema Rust, updates tests, and bumps Spirit to `0.9.1`.
- `CriOMOS-home` `da34fb6b` — pins Spirit to `b3735827`.

## Verification

- `schema-next`: `cargo test`
- `schema-rust-next`: `cargo fmt`; `cargo test`
- `spirit`: `cargo test --features nota-text`
- `spirit`: `cargo test --no-default-features`
- `spirit`: `cargo test --features production-migration`
- `spirit`: `cargo test --features agent-guardian`
- `spirit`: `cargo clippy --all-targets --features agent-guardian,production-migration,testing-trace -- -D warnings`
- `spirit`: `nix build .#default`
- `CriOMOS-home`: `nix build .#checks.x86_64-linux.spirit-deployment`
- `CriOMOS-home`: `lojix-run '(HomeOnly goldragon ouranos li [/git/github.com/LiGoldragon/goldragon/datom.nota] [github:LiGoldragon/CriomOS-home/main] Activate None None)'`

## Live Checks

After activation:

- `agent-daemon.service`: active/running, `NRestarts=0`, `ExecMainStatus=0`
- `spirit-daemon.service`: active/running, `NRestarts=0`, `ExecMainStatus=0`
- `spirit Version`: `(VersionReported (0.9.1 (1456 6119361712800042049)))`
- `spirit '(Count ((Full [(Technology Software)]) Any Any Any None (Exact Zero) (AtLeastCertainty Minimum) Any))'`: `(RecordsCounted (11 (1456 6119361712800042049)))`
- `spirit '(Count ((Full [(Technology (Software (Engineering SoftwareArchitecture)))]) Any Any Any None (Exact Zero) (AtLeastCertainty Minimum) Any))'`: `(RecordsCounted (5 (1456 6119361712800042049)))`
- Old syntax rejection: `[[Technology Software]]` fails with `expected DomainScope to be a parenthesis block`.
- Guardian smoke: transient proposal rejected as `NonIntent`, proving the deployed daemon still gates through the agent.

## Store Version Note

The live SEMA store version did not need a bump for this change. The stored record payload uses `Entry` with `Domains`; `DomainScope` is query/wire surface and is not stored in the live record table. The deployed startup reported `(Current (1456))`, and live count/queries succeeded after activation.
