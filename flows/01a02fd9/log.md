# Design flow

Investigating Codex live light/dark theme propagation and stale component contrast under Chroma changes.

## 2026-08-23

- Flow opened from the living's report that Codex does not follow Chroma light/dark changes and that manual theme changes leave some UI components unreadable until quit and resume.
- Skills loaded: design, spirit, subflows, psyche-interraction, flows, psyche, OpenAI Docs, behavior, vocabulary.
- Three read-only subflows were dispatched: official OpenAI documentation, first-party Codex issue and change history, and local mechanism plus written-psyche investigation.
- No Codex-specific terminal-theme ruling was found in the written psyche. The relevant existing authority is that Chroma owns theme state and applications consume its projection without Chroma scanning PTYs.
- Both failures have multiple open first-party reports. Codex's former focus-time palette refresh was removed in 0.147.0 because it could block or discard queued input; current main redraws with the startup-cached palette.
- Local Chroma reloads Ghostty's palette over D-Bus. Ghostty 1.3.1 contains DECSET 2031 notification support, while Codex 0.148.0 does not subscribe and the local config's explicit `dracula` syntax theme disables adaptive theme selection.
- `reports/codexThemeSwitching.md` records the evidence, current workaround boundary, and the preferred terminal-notification plus replay-safe palette-refresh design.
- An independent source audit corrected the report's evidence boundaries: the explicit syntax theme is configured behavior, the live semantic-palette defect is upstream, and safe runtime probing remains a design requiring a single input owner and queued-input proof.
