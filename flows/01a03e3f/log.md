# Flow 01a03e3f

Implemented the living-approved, package-local ChatGPT native-Wayland launch
override in CriomOS-home. `chatgptPackage` now overrides the llm-agents package
with `commandLineArgs = "--ozone-platform=wayland"`; the existing shared
`CODEX_CLI_PATH` wrapper remains the launcher boundary. X11 and XWayland were
not changed globally, and no generation was activated or app relaunched.

The focused graphical Home Manager evaluation and a remote Prometheus wrapper
contract passed. The historical package boundary produced the intended red
witness. The full graphical gate was blocked by an independently landed Claude
Desktop derivation that could not replace `app.asar`; the ChatGPT and Agent
Intercom derivations completed before that failure.

Open: repair or otherwise resolve that separate Claude Desktop derivation before
treating the complete graphical durable check as green.
