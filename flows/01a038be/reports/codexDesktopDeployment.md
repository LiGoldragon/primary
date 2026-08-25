# Codex and Claude Desktop deployment

Home commit `f05a3639de72` declares the Codex derivation once in
`packages/codex`, sourced from the audited `llm-agents` pin. Terminal,
Codex Desktop's CLI and remote-control package, Agent Intercom, VSCodium, and
their checks use that package. The obsolete standalone Codex input and its
lock graph are removed together.

Claude Desktop is added only when the projected user has the medium profile
and the node has the graphical Agent Intercom capability. Claude Desktop's
embedded Code runtime remains package-managed. The published package identity
is observable, but the embedded runtime version is not exposed by this
integration, so no unsupported equality assertion or override was added.

Direct evaluation proves the Codex terminal/Desktop/remote package equality
and the Desktop gate. Syntax parsing and Nix formatting passed. The complete
durable check build has not run because no configured remote builder is
available; consequently the CriomOS consumer pin was deliberately not updated.

## Sources

- [Current-flow deployment witness](../witnesses/codexDesktopDeployment.md)
- [Remembered Desktop deployment](rememberedDesktopDeployment.md)
- [Codex derivation ruling](../vision/codexDerivation.md)
- [Medium graphical nodes ruling](../../01a0338f/vision/mediumGraphicalNodes.md)
- [TUI and Desktop versions ruling](../../01a0338f/vision/tuiAndDesktopVersions.md)
