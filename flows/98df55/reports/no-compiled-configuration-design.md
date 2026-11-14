# Flow with no compiled-in configuration: design (bn7s, Fable 5pl2)

Its own release, after the release carrying pko0, w0f8 and k7jy. The inventory it rests on: flows/98df55/reports/compiled-config-inventory.md (58 rows, at flow pko0-90d453 291b73e6; classes A from the place, B meta-settable but defaulted in code, C no meta value yet, D fixed).

## What the release does
1. The crate flow-defaults goes, with every caller: `HerdrCli::default` and its environment read (HOME, /etc/passwd, XDG_RUNTIME_DIR, CLAUDE_CONFIG_DIR), the seeding path (`SeedsConfiguration`, `open_seeded`, `OpensFlowStore::open`, `ConfigurationOnlyStore::configuration(&defaults)`). The daemon builds its Herdr and Codex clients from Memory alone. Tests construct their configuration explicitly, as a replayed datom does.
2. Every B fallback goes (hook path beside the daemon, harness profiles in code, request-id draws and announcement tries written at open, default Minutes 30, publication deadline 60 s, counter seeds, flows root `~/primary/flows`, Codex placeholders). A missing value is not filled.
3. Every C value becomes meta configuration: a Configure variant in a new meta-signal-flow, kept in Memory, replayed from datom by the definitions.
4. A Nexus lacking a value answers that it is unconfigured for it: the Input that needs it is refused naming the missing value (signal-flow, new version), never a fallback, a relative path or a PATH lookup. The daemon starts and serves its meta socket unconfigured.
5. The A names stay derived from the place: `<Runtime>/flow.sock`, `<Runtime>/flow-meta.sock`, `<State>/flow.sema`; the place file found at `$XDG_CONFIG_HOME/nexus/<place>/flow-nexus.signal`, the CLI's place name in `$XDG_CONFIG_HOME/nexus/flow-nexus.datom`, as vision nexus 1 states.
6. Home: the configure unit's datom gains the new values; the Flow module states what it sets.
7. The flake's 0.53.2 `mkFlowPackage { defaultConfiguration }` stays: it builds a historical predecessor for a migration test, not this daemon.

## Proposed new configuration (C), one value at a time
- Executables: herdr, flow-id, git, and the Claude client path beside Codex's ClientPath (C1-C4).
- ClaudeHome, also passed to the hook in its HookConfiguration so the hook reads no environment (C5, C6).
- HerdrWaits: title, rest, submission, render, agent start, pane output, reply (C7, C8, C12); PaneWriter: interrupt presses and their wait, composer lines, rest wait (C9).
- CodexEndpoint gains its timeout and history paging (C10, C21); Curriculum exchange wait and answer-frame bound (C11).
- Restart: automatic reopens and spawned-exit wait (C13); CompactionMargin (C14); ConnectionTimeout read/write (C16); SendSettlementWait (C17).
- TaskReminders (C15), LeftOutTools (C18), FlowsDirectory (C20), the prompt and notice texts (C19): see the questions.

## Answers (Psyche rv6w)
2 XDG_CONFIG_HOME else HOME/.config stays, the one environment read. 3 one Unconfigured refusal naming the missing value. 4 configured absolute paths, no PATH lookup; Claude gets a ClientPath. 5 one Configure value per component, each changed alone. 6 texts and left-out tools: configuration, on a bead after this release. 7 reminder count and flows directory (a path) are configuration. 8 protocol seeds fixed; first delivery number is a default and goes. 1 with Fable.
Build held: a hard cut of Flow is being shaped by Fable; this release may fold into it.
