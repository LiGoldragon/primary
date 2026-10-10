# Chroma Pi Theme Cleanup Evidence

Task: remove Pi-specific Chroma code and stale CriomOS-home package/check surfaces for the former Pi theme-switcher extension. Preserve Chroma terminal/desktop/Ghostty/Emacs behavior.

Changed files:

Chroma `/git/github.com/LiGoldragon/chroma`:
- `src/theme.rs` — removed the `tokio::fs::write(state_dir.join("current-mode"), format!("{mode}\n"))` sidecar write from `TerminalThemeConcern::apply`; the terminal concern still creates `$XDG_STATE_HOME/chroma` and writes `fzf-theme.sh`.
- `tests/hard_constraints.rs` — extended the terminal reload hard constraint to assert Chroma source does not contain the old `current-mode` sidecar.

CriomOS-home `/git/github.com/LiGoldragon/CriomOS-home`:
- `packages/pi-criomos/default.nix` — kept `criomos-dark` and `criomos-light` themes, removed the packaged `theme-switcher.ts` extension from package metadata and install output.
- `packages/pi-criomos/src/extensions/theme-switcher.ts` — deleted the old extension that watched `$XDG_STATE_HOME/chroma/current-mode` and called Pi UI theme APIs.
- `modules/home/profiles/min/chroma.nix` — stopped seeding `$XDG_STATE_HOME/chroma/current-mode` during activation.
- `checks/pi-harness-profile/default.nix` — now asserts `pi-criomos` has no Pi extensions and the old theme-switcher file is absent while preserving theme JSON checks.
- `checks/pi-criomos-extension-load/default.nix` renamed to `checks/pi-criomos-package-load/default.nix` — no longer fabricates `current-mode` or loads the old extension; still verifies Pi can list models and the continuation extension check still works.
- `flake.nix` — renamed the check attribute to `pi-criomos-package-load`.
- `docs/pi-extensions.md` — documents that Pi uses built-in automatic theme mode with `criomos-dark`/`criomos-light` and no Chroma sidecar extension.
- `flake.lock` — bumped `chroma` input to `b5313b6b915d1f8de527810c9afa9ae825d8d849` so home deployments consume the cleanup.

Exact old Pi signal removed:
- Chroma no longer writes `${XDG_STATE_HOME:-$HOME/.local/state}/chroma/current-mode`.
- CriomOS-home no longer packages or checks the Pi `theme-switcher.ts` watcher that mapped `dark|light` from that file to `criomos-dark|criomos-light`.

Validation:
- `cd /git/github.com/LiGoldragon/chroma && cargo test --test hard_constraints hc_chroma_006_daemon_does_not_trigger_global_terminal_reload_files_or_pi_mode_sidecar` — pass.
- `cd /git/github.com/LiGoldragon/chroma && cargo test` — pass.
- `cd /git/github.com/LiGoldragon/chroma && nix build .#checks.x86_64-linux.default` — pass.
- `cd /git/github.com/LiGoldragon/CriomOS-home && nix build .#checks.x86_64-linux.chroma-nota-config` — pass.
- `cd /git/github.com/LiGoldragon/CriomOS-home && nix build .#checks.x86_64-linux.pi-harness-profile` — pass.
- `cd /git/github.com/LiGoldragon/CriomOS-home && nix build .#checks.x86_64-linux.pi-criomos-package-load` — pass.
- Initial discovery command `nix flake show --all-systems --no-pager` in Chroma failed because this Nix does not recognize `--no-pager`; reran as `nix flake show --all-systems` successfully.

Commit and push status:
- Chroma committed and pushed on `main`: `b5313b6b915d1f8de527810c9afa9ae825d8d849` (`chroma: stop writing Pi theme sidecar`).
- CriomOS-home committed and pushed on `main`: `e319468fe6202e5a6474a8ef2047ebd3032310c8` (`Pi: drop Chroma theme-switcher sidecar`).
- Both working copies were clean after push.

No blockers.
