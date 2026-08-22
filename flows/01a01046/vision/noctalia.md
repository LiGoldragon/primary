## 2026-08-17T17:58:28.765+02:00 — use helix to statefully override any value that deviates from declared value

> then we should use helix to statefully override any value that deviates from declared value.

Context: Noctalia stores GUI-selected preferences in mutable `~/.local/state/noctalia/settings.toml`, which overrides its Nix-generated configuration. The psyche rules that declared values are reconciled statefully through Helix when the mutable value deviates, rather than by deleting or overwriting the whole application state file at activation.

