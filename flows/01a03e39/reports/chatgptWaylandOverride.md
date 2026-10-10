# ChatGPT native-Wayland package override

The accepted change is isolated to ChatGPT's package boundary: its llm-agents
derivation now receives `--ozone-platform=wayland`. The shared launcher still
sets `CODEX_CLI_PATH` to the pinned Codex CLI, so the desktop application and
terminal continue to use the same Codex executable.

No global X11 or XWayland setting changed. That broader direction remains
separate work. No live Home Manager activation or desktop application relaunch
was authorized or performed.

The current generated wrapper passed a remote Prometheus contract that checks
all three relevant properties: it targets an override rather than the original
ChatGPT package, its target contains the Wayland argument, and the outer
wrapper retains the shared Codex target. The corresponding historical wrapper
failed the no-original-package-reference condition before the implementation,
providing a red witness.

The complete graphical durable check remains blocked outside this change. Its
Claude Desktop dependency fails while replacing `app.asar`; therefore it cannot
yet prove the full desktop profile, despite the focused ChatGPT contract being
green.

## Sources

- `witnesses/chatgptWaylandOverride.md`
- Flow `01a03e39` — living-approved implementation request
- Flow `01a038be` — original X11/Wayland diagnosis and terminal proposal
