# Research: Persistent terminal-based AI coding sessions and Niri workspace recovery

## Summary

The most robust practical design is to make the AI process independent of the terminal emulator (tmux, Zellij, or a user systemd service), persist the tool’s own conversation/session identifier, and treat terminal windows as disposable views. tmux is the strongest general-purpose choice when scripted input is required; Zellij is attractive for declarative layouts and resurrection; abduco/dvtm is simpler but has much less orchestration surface. Niri can enumerate windows/workspaces and move newly opened terminal windows into one workspace through its IPC, but it does not preserve terminal processes itself.

There is an important distinction between **reopening/resuming a conversation** and **attaching to the same live TUI**. Codex CLI and Claude Code document conversation resume and noninteractive/SDK interfaces. No primary documentation reviewed establishes a supported public API that injects a new user prompt into an already-running interactive TUI. PTY writes, `tmux send-keys`, and terminal remote-control typing can work as UI automation, but are inherently state-dependent and should not be treated as a reliable message API.

## Findings

1. **tmux provides the broadest confirmed persistence and control primitives.** A tmux server owns sessions, windows, panes, and their child PTYs independently of clients; clients can detach and later attach. `list-sessions`, `list-panes`, `display-message -p`, control mode (`-C`), hooks, `pipe-pane`, `capture-pane`, `send-keys`, and `paste-buffer` give an external supervisor both discovery and automation surfaces. `send-keys` sends key events to a pane rather than invoking an application API; literal mode (`-l`) avoids key-name interpretation, while `paste-buffer -p` requests bracketed-paste wrapping. This makes tmux suitable for supervised UI automation but does not make such automation semantically safe. [tmux manual](https://man.openbsd.org/tmux)

2. **Zellij confirms session persistence, discovery, layouts, and resurrection, but scripted TUI injection is a weaker contract.** Zellij supports named sessions, `list-sessions`, attach, session-manager UI, layouts, plugins, and session resurrection. Its CLI also exposes pane actions such as writing bytes/characters to the focused pane. Resurrection restores layout and, where configured/supported, commands and pane state; it cannot reconstruct arbitrary in-memory state of a dead AI process. Use live sessions for process continuity and Codex/Claude resume IDs for crash/reboot recovery. [Sessions](https://zellij.dev/documentation/sessions.html) [Session resurrection](https://zellij.dev/documentation/session-resurrection.html) [CLI actions](https://zellij.dev/documentation/cli-actions.html)

3. **abduco/dvtm is a small, composable persistence option, not a rich fleet manager.** abduco detaches a program from its controlling terminal, lists sessions with `abduco`, and reattaches by name; dvtm supplies terminal multiplexing. This cleanly survives terminal-emulator restarts, but compared with tmux it offers fewer documented pane metadata, hooks, output capture, and targeted key-injection primitives. It is viable when each coding agent is one named process and orchestration remains outside the multiplexer. [abduco README/man page](https://www.brain-dump.org/projects/abduco/) [dvtm](https://www.brain-dump.org/projects/dvtm/)

4. **systemd user services are the best lifecycle authority, but an interactive TUI still needs a PTY owner.** User units offer restart policy, dependencies, environment, logging, stable names, and enumeration via `systemctl --user`. `systemd-run --user`, templated units, and lingering can keep services alive beyond a login session. A service alone does not provide a reconnectable terminal: run tmux/Zellij as the service-managed server, or use a purpose-built PTY bridge. `StandardInput=tty` requires a TTY path and is not a general attach protocol. Lingering also changes security/resource behavior and must be explicitly enabled. [systemd user manager](https://www.freedesktop.org/software/systemd/man/latest/systemd.html#User%20Manager) [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) [loginctl enable-linger](https://www.freedesktop.org/software/systemd/man/latest/loginctl.html)

5. **Terminal-emulator remote control should recreate views, not own persistence.** Kitty’s remote-control protocol can list OS windows/tabs and launch, focus, or send text; WezTerm’s CLI/multiplexer can list and activate panes/tabs and spawn commands. These facilities disappear or vary when the emulator/server exits, and “send text” still targets a foreground terminal application with unknown UI state. They are useful for opening one client window per persistent session after restart, not as the persistence boundary or preferred agent-message bus. [kitty remote control](https://sw.kovidgoyal.net/kitty/remote-control/) [WezTerm CLI](https://wezterm.org/cli/cli/index.html) [WezTerm multiplexing](https://wezterm.org/multiplexing.html)

6. **Codex CLI has supported resume and automation paths, but they are not documented as live-TUI injection.** Official Codex CLI documentation exposes interactive session resume (`codex resume`, including selection/last-session forms) and noninteractive execution through `codex exec`; the open-source repository documents configuration and CLI behavior. Codex also has an app-server protocol used by clients, with thread/turn concepts, but it should be treated as a separate supported/experimental client interface according to the versioned protocol documentation—not as permission to write into an arbitrary already-running TUI process. A safe controller should either (a) let the human attach to the live TUI, (b) start a new resumed interactive process only after the old one has exited, or (c) own the conversation through the documented noninteractive/app-server interface from the outset. [Codex CLI](https://developers.openai.com/codex/cli/) [CLI features](https://developers.openai.com/codex/cli/features/) [Non-interactive mode](https://developers.openai.com/codex/noninteractive/) [Codex repository](https://github.com/openai/codex) [App server README](https://github.com/openai/codex/tree/main/codex-rs/app-server)

7. **Claude Code similarly documents resume, print/streaming, SDK, and hooks—not a public “inject into this live TUI” endpoint.** Claude Code supports continuing/resuming conversations from its CLI and noninteractive `-p` operation; structured streaming input/output belongs to print-mode/SDK automation rather than an attached interactive prompt. Hooks receive lifecycle events and can run commands or return documented decisions/context, but they are not a general asynchronous user-message channel into the current TUI. A controller needing dependable messaging should create and own a headless Claude Code/Agent SDK session rather than type into an independently operated TUI. [CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference) [Interactive mode](https://docs.anthropic.com/en/docs/claude-code/interactive-mode) [Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) [Headless/programmatic use](https://docs.anthropic.com/en/docs/claude-code/sdk)

8. **PTY/key injection is possible but unsupported at the application-semantic layer.** Writing to the PTY master, `tmux send-keys`, Zellij write actions, kitty `send-text`, or desktop keyboard automation all imitate user input. Failure modes include: the TUI is on a confirmation/permission dialog; a modal selector or slash-command UI is active; focus is in another pane; the application is generating and queues/ignores input; terminal dimensions changed; text contains control characters; bracketed-paste markers are absent, doubled, or interpreted differently; multiline paste triggers a confirmation or submit behavior; and Enter is sent before rendering/input processing settles. Never inject secrets or destructive approval answers. If unavoidable, target a stable pane ID, verify the foreground command and captured prompt marker, send literal text via a paste buffer, send Enter separately, serialize writers, capture output, enforce timeouts, and fail closed on any unexpected state. These mitigations reduce risk but do not turn automation into a supported API. [tmux `send-keys`/`paste-buffer`](https://man.openbsd.org/tmux#send-keys) [Bracketed paste mode specification](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html)

9. **Niri provides the required discovery and placement layer.** `niri msg` exposes outputs, workspaces, windows, focused-window information, actions, and JSON output; actions include focusing a workspace/window and moving a window to a workspace. Niri’s IPC socket (`NIRI_SOCKET`) and event stream allow a supervisor to discover newly created windows and react without polling. Window rules can match app ID/title and open windows on a named workspace, which is preferable when terminal instances can be launched with distinct, stable app IDs/titles. Exact action flags are version-sensitive, so automation should feature-detect with the installed `niri msg action --help` and consume JSON rather than human-formatted output. [Niri IPC](https://yalter.github.io/niri/IPC.html) [Niri configuration: window rules](https://yalter.github.io/niri/Configuration%3A-Window-Rules.html) [Niri wiki](https://github.com/YaLTeR/niri/wiki)

10. **Recommended architecture A: tmux + manifest + Niri reconciler.** Create one named tmux session per repository/agent (or one fleet session with one window per agent), save a manifest containing stable logical ID, cwd, tool, tool-native conversation ID, tmux session/window/pane ID, and desired Niri workspace. Optionally let a systemd user unit supervise the tmux server/reconciler. On terminal restart, enumerate tmux, launch a terminal client attaching to each selected session, then use Niri window rules or IPC events to move all client windows to a named workspace and focus it. Use native resume after process death. Reserve `send-keys` for explicitly opted-in, state-checked best-effort automation.

11. **Recommended architecture B: API/headless agents + replaceable monitoring TUIs.** For unattended dispatch, start Codex noninteractive/app-server or Claude Code headless/SDK sessions under systemd user services, persist events and conversation IDs, and expose logs/status in tmux/Zellij panes. This separates reliable message transport from terminal rendering and is safer than injecting into interactive TUIs. The tradeoff is that it may not reproduce every interactive approval flow; the supervisor must implement an explicit approval policy and never silently downgrade sandbox/permission protections.

12. **Recommended architecture C: Zellij layouts for human-first recovery.** Use named Zellij sessions and checked-in/local layouts to restore tabs/panes, plus tool-native resume IDs for process loss. This gives a polished “reopen the workspace” experience with less custom code. Prefer tmux instead if precise pane targeting, mature control-mode integration, or extensive capture/injection tooling is a hard requirement. abduco/dvtm is the minimal variant for users who value small components over orchestration features.

## Confirmed capabilities vs. inference

### Confirmed in cited primary documentation

- Multiplexer sessions can outlive emulator clients and be enumerated/reattached.
- tmux exposes targeted pane input, capture, hooks, and machine-oriented control mode.
- Codex and Claude Code expose conversation continuation/resume and separate programmatic modes.
- Niri exposes IPC-based window/workspace discovery and placement actions/rules.
- systemd user managers can supervise named long-running processes.

### Inference or operational recommendation

- A tmux pane containing a live Codex/Claude TUI will normally survive an emulator restart because tmux remains the PTY owner; this follows from tmux’s process model, not an AI-tool guarantee.
- Prompt-marker/foreground-process checks can make key injection less dangerous, but no cited Codex or Claude contract guarantees that these checks identify a safe input state.
- Combining terminal launch, Niri event discovery, and move actions can reconstruct a multiwindow workspace; the reconciler and race handling are custom integration work.
- Any July 2026 product feature not present in the versioned pages/repositories at deployment time must be feature-detected. Documentation URLs are rolling and may describe newer behavior than an installed binary.

## Sources

- Kept: [tmux manual](https://man.openbsd.org/tmux) — authoritative lifecycle, control mode, pane discovery, input, and capture semantics.
- Kept: [Zellij documentation](https://zellij.dev/documentation/) — official sessions, resurrection, layouts, and CLI behavior.
- Kept: [abduco](https://www.brain-dump.org/projects/abduco/) and [dvtm](https://www.brain-dump.org/projects/dvtm/) — upstream project documentation.
- Kept: [systemd manuals](https://www.freedesktop.org/software/systemd/man/latest/) — authoritative user-service lifecycle semantics.
- Kept: [OpenAI Codex docs](https://developers.openai.com/codex/cli/) and [source repository](https://github.com/openai/codex) — primary CLI/programmatic-interface evidence.
- Kept: [Anthropic Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/overview) — primary CLI, SDK, and hook evidence.
- Kept: [Niri IPC docs](https://yalter.github.io/niri/IPC.html) and [repository](https://github.com/YaLTeR/niri) — primary compositor integration evidence.
- Kept: [kitty](https://sw.kovidgoyal.net/kitty/remote-control/) and [WezTerm](https://wezterm.org/cli/cli/index.html) official docs — representative emulator remote-control capabilities.
- Dropped: blog posts and “best terminal multiplexer” comparisons — secondary, often stale, and unnecessary for capability claims.
- Dropped: Expect/xdotool recipes — examples demonstrate feasibility but cannot establish Codex/Claude support or Wayland/Niri reliability.

## Gaps

- This runtime exposed no web-search/fetch tool, so the brief could not snapshot and quote the exact July 2026 revisions of rolling documentation. The linked primary pages and installed versions should be rechecked during implementation, especially Codex app-server stability, Claude Code’s current programmatic/remote features, and Niri action argument names.
- Neither vendor documentation cited here establishes a supported asynchronous injection channel into an already-running interactive TUI. Absence of documentation is not proof no private/internal mechanism exists; vendor confirmation or source-level review at the pinned release is the next step.
- Persistence across a machine reboot depends on multiplexer resurrection or tool-native resume, not merely detach/reattach. Exact fidelity (pending approvals, unsubmitted editor text, streamed response state) needs destructive testing against pinned tool versions.

## Practical validation plan

Pin versions, then test: emulator kill/restart; user logout and reboot; session enumeration; simultaneous terminal reopening; Niri placement races; Codex/Claude process crash followed by native resume; input during generation, permission confirmation, modal selection, multiline/bracketed paste, and focus loss. Record whether injection fails closed. Do not enable automated confirmations until these cases are proven and an explicit security policy exists.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Created only the requested research brief at the authoritative output path; no product or repository files were modified."
    },
    {
      "id": "criterion-2",
      "status": "satisfied",
      "evidence": "Brief provides primary-source links, separates confirmed capabilities from inference, compares all requested architectures, covers TUI injection risks, Niri IPC, recommendations, and explicit research gaps."
    }
  ],
  "changedFiles": [
    "/home/li/primary/research-session-harnesses.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "Output file was written successfully by the file tool.",
    "No web-search tool was available; rolling July 2026 documentation could not be independently fetched or revision-pinned in this runtime."
  ],
  "residualRisks": [
    "Primary documentation URLs are rolling and require version-pinned revalidation before implementation.",
    "No supported live-TUI prompt injection API was confirmed; PTY/key injection remains state-dependent UI automation.",
    "Independent reviewer gate remains to be performed by the parent/reviewer."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added one research report comparing persistence, control, AI CLI messaging, and Niri workspace-restoration options.",
  "reviewFindings": [
    "no self-review blockers; independent review required",
    "caveat: web retrieval was unavailable, so exact July 2026 documentation state is not revision-pinned"
  ],
  "manualNotes": "Recommended default is tmux plus a manifest and Niri IPC reconciler; use Codex/Claude native programmatic interfaces for dependable unattended dispatch rather than typing into live TUIs."
}
```
