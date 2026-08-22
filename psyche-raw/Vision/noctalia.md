## 2026-08-17T17:58:28.765+02:00 — use helix to statefully override any value that deviates from declared value

> then we should use helix to statefully override any value that deviates from declared value.

Context: Noctalia stores GUI-selected preferences in mutable `~/.local/state/noctalia/settings.toml`, which overrides its Nix-generated configuration. The psyche rules that declared values are reconciled statefully through Helix when the mutable value deviates, rather than by deleting or overwriting the whole application state file at activation.

## 2026-08-19T21:12:36+02:00 — noctalia shouldnt be in charge of deciding the light/theme anywhere

> noctalia shouldnt be in charge of deciding the light/theme anywhere, it should be yielding to chroma's effects

Context: Chroma reports Dark while Noctalia independently resolves Light and writes the shared GNOME color-scheme setting. The psyche rules that Noctalia must yield theme authority to Chroma.

## 2026-08-19T22:17:13+02:00 — sounds good

> sounds good.

Context: The psyche approved the proposed fallback anatomy. In Noctalia external mode, retain the last externally observed mode and use dark only when no prior observation exists. Chroma rejects location fixes worse than 1 km, retains the last good fix, and remains explicitly unlocated when none exists. These fallback sentences were the agent's proposal accepted by the quoted reply.
