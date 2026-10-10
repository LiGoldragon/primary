# Other signal witnesses

Terminal Cell v1.0.0 `e44c41a39866f645853364e85eff2f8e2256e722`:

- `cargo test --all-targets`: passed, including 12 `daemon_witness` spawned socket/component cases.
- configured-builder Nix explicit current-system check attributes: `build`, `default`, `ownership`, `control-socket-mode`, `fmt`, `clippy`.
- `nix build -L` for all six exited `0`; captured exit record `/tmp/terminal-cell-e44-gates.exit` and log `/tmp/terminal-cell-e44-gates.log`.

Harness v0.4.0 `722b68b3579b0235120ca098a0cddefa379d9945`: full local all-target tests and strict clippy passed. Every declared current-system Nix check was explicitly built; `harness-722b-nix.exit` is `0`. `harness-check-attributes.json` records the selected attributes. The prior guessed-attribute invocation failed before running checks and is not release evidence.
