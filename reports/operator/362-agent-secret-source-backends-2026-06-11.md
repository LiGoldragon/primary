# Agent Secret Source Backends

## Scope

Implemented typed provider secret-source configuration for the `agent` component.

The meta socket now configures provider keys as a closed backend reference:

- `Environment(EnvironmentSecret)`
- `Gopass(GopassSecret)`
- `File(FileSecret)`

The secret value still never crosses the meta signal or startup archive.

## Landed Commits

- `meta-signal-agent` main: `04a9116c5293` — `meta-signal-agent: configure typed secret sources`
- `meta-signal-agent` main: `92bfc47867c8` — `meta-signal-agent: refresh secret-source docs`
- `agent` main: `df103ef72b00` — `agent: resolve provider secrets from configured backends`

All pushed; local `main` and `main@origin` match for both repos.

## Changes

- Replaced `ApiKeyHandle` in the meta contract with `SecretSource`.
- Updated `ProviderConfiguration` to carry `secret_source`.
- Updated canonical NOTA examples to use forms such as:
  - `(Gopass platform.deepseek.com/api-key)`
  - `(Environment MIMO_API_KEY)`
- Updated the agent registry so `ProviderEntry` stores a runtime `SecretSource`.
- Added `SystemKeySource`, which resolves:
  - environment variables through `std::env`,
  - gopass secrets through async `tokio::process::Command`,
  - secret files through async `tokio::fs`.
- Updated binary startup `ProviderSeed` and `agent-write-configuration` so startup archives use the same secret-source syntax as the meta socket.
- Updated the live DeepSeek test so the agent resolves the key from gopass itself.

## Verification

- `meta-signal-agent`: `cargo test`
- `meta-signal-agent`: `cargo clippy -- -D warnings`
- `agent`: `cargo test`
- `agent`: `cargo clippy --features live-provider -- -D warnings`
- `agent`: `cargo test --features live-provider live_deepseek_flash_returns_valid_nota_with_gopass_key -- --nocapture`

The real DeepSeek call passed with the key resolved by the agent through gopass.

## Note

I attempted to capture the durable design in Spirit first, but the deployed Spirit CLI rejected my old `Record` shape and also has no `Help` input. I did not keep guessing live record syntax.
