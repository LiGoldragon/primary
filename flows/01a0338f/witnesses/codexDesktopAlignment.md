# Codex desktop and terminal alignment

Method: probe official OpenAI documentation, `openai/codex` source, and the current official Linux `chatgpt_amd64.deb` through the delegated `codex_code_alignment` subflow on 2026-08-25.

OpenAI's current Linux package is `chatgpt` 26.818.61809. Its payload contains `/usr/lib/chatgpt/resources/codex`, which reports `codex-cli 0.149.0-alpha.4.3`, and an Electron `app.asar` frontend. The frontend resolves that bundled executable, honors `CODEX_CLI_PATH`, and spawns the selected executable as `codex app-server`; local-daemon mode instead connects to the app-server Unix socket.

The desktop and Codex runtime therefore have independent version schemes:

```text
Desktop: 26.818.61809
Codex runtime: 0.149.0-alpha.4.3
Current stable Codex release at inspection: 0.149.1
```

The Codex CLI, TUI, app-server, app-server client, daemon, and protocol crates share the public `openai/codex` Rust workspace and one workspace version. The Electron desktop frontend is a separate artifact and process which speaks the app-server protocol. OpenAI's app-server documentation says generated schemas are version-specific and must match the exact Codex version used.

An enforceable Nix invariant is therefore:

```text
CODEX_CLI_PATH --version
  == app-server initialize/user-agent version
  == expected pinned Codex release/revision/hash
```

The official desktop build number must remain a separate field. The package can either retain the exact bundled runtime or replace it through the supported `CODEX_CLI_PATH` selection with the same Codex derivation exposed to the terminal. An external runtime whose reported version differs must fail the check.

## Sources

- [OpenAI Linux app](https://learn.chatgpt.com/docs/linux/linux-app)
- [Codex CLI](https://developers.openai.com/codex/cli)
- [Codex App Server](https://developers.openai.com/codex/app-server)
- [Codex release rust-v0.149.0-alpha.4.3](https://github.com/openai/codex/releases/tag/rust-v0.149.0-alpha.4.3)
- [Codex workspace Cargo.toml](https://raw.githubusercontent.com/openai/codex/rust-v0.149.0-alpha.4.3/codex-rs/Cargo.toml)
- [App Server README](https://raw.githubusercontent.com/openai/codex/rust-v0.149.0-alpha.4.3/codex-rs/app-server/README.md)
- [ilysenko/codex-desktop-linux](https://github.com/ilysenko/codex-desktop-linux)
