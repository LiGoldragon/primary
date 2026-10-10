# Live ChatGPT desktop new-chat diagnosis

Observed read-only on 2026-09-02. The running desktop process is ChatGPT 26.825.51511, PID 1440540. The parent flow's ownership witness identifies this running process as generation 991; generation 992 is reported to contain the repair. Consequently, the witness below establishes the failure still present in the live 991 process, but does not evaluate generation 992.

## Smallest meaningful witness

The direct UI/Composer path reaches `thread/start`, and the local app-server returns JSON-RPC `-32600` before creating a conversation:

```text
2026-09-02T12:43:49.950Z ... thread-start config resolved ... threadStartConfig=true
2026-09-02T12:43:49.957Z ... response_routed ... errorCode=-32600 ... method=thread/start
2026-09-02T12:43:49.959Z ... Request failed ... error={"code":-32600,"message":"failed to load configuration: invalid transport\nin `mcp_servers.codex_app`\n"} failureReason=invalid_config ... method=thread/start
2026-09-02T12:43:49.965Z ... [Composer] submit failed ... errorMessage="failed to load configuration: invalid transport\nin `mcp_servers.codex_app`\n" ... mode=local
```

The same failure repeats at 12:47:22.644Z (prewarm), 12:47:30.473Z (Composer), and 12:47:40.728Z (prewarm), with earlier occurrences at 10:04:59.916Z and 11:02:20.542Z. There are six observed failed `thread/start` responses in this log; the repeated error/handler lines are not six different faults. A read-only reproduction of the witness is:

```sh
rg -n -a 'errorCode=-32600.*method=thread/start|Composer\\] submit failed|Failed to prewarm conversation' \
  /home/li/.local/state/codex/logs/2026/09/02/codex-desktop-db4b2188-3588-4b45-8b87-3245dd49a547-1440540-t0-i1-100451-0.log
```

## Observations

- Desktop startup itself succeeds. The log records the native dynamic-app-tools pipe listening, starts the local app-server transport, upgrades from stdio to WebSocket, completes the initialize handshake with `transportKind=websocket`, reports app-server version 0.151.0, and reaches `connected` state.
- The sole persistent owner is PID 4013983, `codex app-server --remote-control --listen unix://`, active under `codex-remote-control.service` since 2026-08-31. Its Unix socket `/home/li/.codex/app-server-control/app-server-control.sock` is listening with mode 600. ChatGPT has its own `/home/li/.codex/ipc/ipc.sock`; it does not open the owner's control socket directly, consistent with the desktop client using the app-server transport layer.
- No second `codex app-server` owner is present under ChatGPT. The owner journal shows no owner startup, transport, or socket failure associated with these attempts.
- The static `/home/li/.codex/config.toml` contains no `mcp_servers.codex_app` section. The current runtime marketplace definition `/home/li/.codex/.tmp/bundled-marketplaces/openai-bundled/plugins/codex-app-tools/desktop-mcp.json` does contain a valid `codex_app` stdio definition (`command` plus `args`). This means the malformed value is not an obvious durable entry in the ordinary config or the currently installed definition.
- After failed starts, the desktop log reports `mcp_server_startup_status_updated ... server=codex_apps status=ready`. This is an independent app-tools readiness signal and does not prove that the per-thread `mcp_servers.codex_app` config object is valid.
- The current ASAR's main bundle contains a separate codex-app-tools config producer. It reads `CODEX_APP_TOOLS_PIPE_PATH`, resolves the bundled `desktop-mcp.json`, and normally emits a `mcp_servers.codex_app` stdio object. Its unavailable fallback is the exact text `mcp_servers.codex_app={command="",enabled=false}`, which has neither a usable stdio command nor an HTTP URL and would produce the observed `invalid transport` parser error. The current desktop log contains no `Codex app tools unavailable`/`missing-*` warning, so this source is a plausible mechanism, not a proven payload for this launch.

## Failure boundary

```text
ChatGPT process starts
  -> bundled native pipe starts
  -> local app-server transport initializes (WebSocket, connected)
  -> UI/Composer resolves a new-thread start config
  -> app-server config loader rejects runtime mcp_servers.codex_app
  -> thread/start returns -32600; prewarm/Composer submission stops
```

The boundary is after desktop bootstrap and owner handshake, at per-thread configuration loading. It is not currently bounded to the persistent owner, its Unix socket, authentication, or the static `config.toml` entry set.

## Hypotheses (not settled)

1. The running generation 991 may still be injecting the malformed fallback from its codex-app-tools path; the static bundle contains that fallback, but no producer warning or emitted override was captured.
2. A stale or independent runtime override may be surviving outside the ordinary config file. Prior flow 01a05e53 identified the same separate `codex-app-tools-mcp` producer as the fault source and disabled it in a pushed repair; the still-running generation 991 would not contain that repair.
3. The valid current marketplace definition makes a simple “plugin file is absent” explanation insufficient for this exact machine state. The producer selection result and the final merged per-thread config are not exposed in the desktop log.

## Unknowns and limits

- The live GUI was not driven or mutated by this diagnostic. The log is the available UI witness; it shows repeated new-chat/prewarm attempts and the exact boundary, but not a screenshot or a fresh click generated by this flow.
- The final merged runtime config passed to the failing `thread/start` is not logged. Therefore the exact malformed field shape and which producer supplied it remain unknown.
- Today’s log has successful app-server activity for other existing/externally created threads after the failed UI starts. This confirms the failure is path/attempt-specific rather than proof that every app-server request fails.
- The parent flow should treat generation 992 as a separate acceptance target: reopen/restart into that generation and repeat the smallest witness, then require a successful `thread/start` with no `invalid transport` result.

## Comparison with prior fault

This is the same fault recorded in `/home/li/primary/flows/01a05e53/log.md`: the exact `invalid transport in mcp_servers.codex_app` parser rejection was previously observed as a runtime/per-thread injection despite no durable config entry. Today’s witness confirms that the prior malformed-runtime path persists in the live generation 991 process after the shared-daemon startup repair. The startup portion is now healthy (WebSocket handshake and connected state); the remaining live fault is the new-thread configuration path.

## Sources

- [Current ChatGPT desktop log](/home/li/.local/state/codex/logs/2026/09/02/codex-desktop-db4b2188-3588-4b45-8b87-3245dd49a547-1440540-t0-i1-100451-0.log:1)
- [Current static Codex config](/home/li/.codex/config.toml)
- [Current runtime codex-app-tools definition](/home/li/.codex/.tmp/bundled-marketplaces/openai-bundled/plugins/codex-app-tools/desktop-mcp.json)
- [Current codex-app-tools launcher](/home/li/.codex/plugins/cache/openai-bundled/codex-app-tools/0.1.3/scripts/launch_codex_app_tools_mcp)
- [Current desktop ASAR containing the producer/fallback code](/nix/store/swaqqi5jqc09v66hij95niqjv1bzmbpx-chatgpt-unwrapped-26.825.51511/lib/chatgpt/resources/app.asar)
- [Prior fault record](/home/li/primary/flows/01a05e53/log.md)
- [Psyche's requested full-access desktop behavior](/home/li/primary/flows/01a05d17/vision/fullAccessPermission.md)
