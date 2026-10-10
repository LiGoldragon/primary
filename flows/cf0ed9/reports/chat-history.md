# Remembered ChatGPT Desktop new-chat history

## Conclusion

The prior work separates two failures that were easy to conflate:

1. ChatGPT Desktop initially could not bootstrap because the package did not expose the executable candidate its resolver requires. Flow `01a05c80` added the candidate, deployed it, and witnessed a fresh Desktop process completing a WebSocket `initialize` through the already-running persistent Codex owner.
2. After that startup repair, flow `01a05e53` investigated the reported inability to create a new conversation or resume an existing one. It attributed the rejection to a separate Desktop `codex-app-tools-mcp` synchronizer writing a malformed runtime `mcp_servers.codex_app` object through `config/batchWrite`; the object had neither accepted `command` nor `url` transport data. The persistent Codex owner and static config were healthy. The proposed producer-disabling fix was pushed as Home commit `51676f4eed1c2356faef799ebe8f0d12b933384c`, but that flow explicitly records that the durable Nix check, deployment, and activation had not yet happened.

Therefore, the healthy-start witness from `01a05c80` does not contradict the later new-chat failure: startup and per-thread configuration loading are different stages. The present flow must establish which generation is active before treating `51676f4e` as live, and must witness both a fresh thread and a resumed thread after any authorized realization.

## Recovered chain

### 01a03f49 — persistent Codex owner

The Nix-owned topology was a persistent per-user Codex app-server daemon with phone Remote Control and terminal TUIs as clients. The retained report says an ordinary TUI cannot be converted or attached after it has created its own embedded app-server; the daemon-backed TUI and phone instead share one daemon writer. Its live proof observed a phone message arrive in the same daemon-backed terminal conversation (`flows/01a03f49/reports/codexPhoneRemoteControl.md:5-10,40-55`). This is the server-side foundation for Desktop integration; it does not itself prove Desktop's private App Tools path.

### 01a047d2 — Desktop gate and topology decision

The flow log first recorded a witnessed Desktop launch failure in which ChatGPT selected stdio `resources/codex app-server` and the packaged gate exited `126`, while the managed owner/socket remained healthy (`flows/01a047d2/log.md:21-23`). Later analysis in that same record found the refreshed Desktop launch shape includes dynamic `mcp_servers.codex_app` configuration and that a simple bare `app-server proxy --sock` matcher would silently discard Desktop startup options and App Tools behavior (`flows/01a047d2/log.md:64-68`).

The relevant psyche vision is narrower and authoritative for topology: keep one server for Claude and Codex, rooted in `primary`, with the desktop apps using it locally; do not introduce a Nexus (`flows/01a047d2/vision/remoteControl.md:1-20`). The later App Tools bridge was an implementation option, not a settled requirement.

### 01a05487 — what “messaging Desktop threads” meant

The exact typed request asked whether Desktop created “a messaging system between threads” (`/home/li/.codex/sessions/2026/08/30/rollout-2026-08-30T23-15-56-01a05487-6e13-7092-ad16-5acb27438b7f.jsonl:10`). The flow’s answer was that `create_thread` and `send_message_to_thread` were a private Electron-host callback surface: work in one thread could ask the host to create or insert a turn into another, but threads were not autonomous peers with mailboxes or subscriptions (`flows/01a05487/log.md:7-9`; transcript claim at the same session `:201`).

The living chose Option 2: Desktop should be an ordinary client of the persistent Codex server, with the private Desktop App Tools channel removed (`flows/01a05487/log.md:7-14`). The final response claimed that the ASAR patch made `getConfigOverrides` empty and removed the bundled CLI override, while also stating that no authenticated GUI activation had yet been attempted (transcript claim at `/home/li/.codex/sessions/2026/08/30/rollout-2026-08-30T23-15-56-01a05487-6e13-7092-ad16-5acb27438b7f.jsonl:1320`). That absence of GUI proof matters: the later startup failure was a real disconfirmation of the static “native shared-daemon transport” claim.

### 01a05c80 — startup repair, then a healthy connection witness

The next user message said, “the skill edit is good. but my chatgpt desktop app still doesnt start” (`/home/li/.codex/sessions/2026/09/01/rollout-2026-09-01T12-25-03-01a05c80-3f85-7c83-9d44-094cf7d53582.jsonl:1134`). The flow identified that the wrapper selected local-daemon mode but the package supplied no recognized `resources/codex` candidate, so the app died before initialization even though the service/socket were healthy (`flows/01a05c80/log.md:7-13`).

Home commit `b04edb442f52` added `resources/codex` backed by the managed package; consumer CriomOS commit `69a946b1d0e5…` pinned it. The flow log records successful Realize and ActivateNow deployments and a fresh ChatGPT process completing a WebSocket `initialize` through the sole pre-existing persistent Codex owner (`flows/01a05c80/log.md:13-23`). The transcript’s final claim says the same: “Fresh ChatGPT connected via WebSocket to the existing persistent Codex server” and did not start a second server (`/home/li/.codex/sessions/2026/09/01/rollout-2026-09-01T12-25-03-01a05c80-3f85-7c83-9d44-094cf7d53582.jsonl:1473`). This proves startup and connection, not successful `thread/start` after Desktop synchronizes per-thread config.

### 01a05e53 — malformed runtime `codex_app` on start/resume

The current prior flow was explicitly opened for “new chats and existing threads” failing with `invalid transport in mcp_servers.codex_app` (`flows/01a05e53/log.md:1-5`). Its settled account says:

- The persistent Codex `0.151.0` owner and Unix socket were healthy.
- Static `/home/li/.codex/config.toml` contained no `mcp_servers.codex_app`.
- Desktop supplied a runtime/per-thread `codex_app` object with neither accepted transport discriminator: no `command` for stdio and no `url` for HTTP.
- The separate `codex-app-tools-mcp` generator bypassed `getConfigOverrides` and wrote the object through `config/batchWrite`; its disabled fallback `{ command = "", enabled = false }` still parsed as an invalid transport.
- An audit found no durable `codex_app` entry in global config, 1,977 inspected session metadata records, or Desktop atom state, so no data migration was needed (`flows/01a05e53/log.md:7-9`).

The exact transcript claim is: “Desktop has a separate ‘Codex App Tools’ synchronizer that bypasses `getConfigOverrides` and writes `mcp_servers.codex_app` through `config/batchWrite` for each local thread” (`/home/li/.codex/sessions/2026/09/01/rollout-2026-09-01T20-55-28-01a05e53-8c4a-7503-b3c5-a04384d4dc20.jsonl:312`). The flow’s first decisive transcript claim separately says both thread creation and resume are rejected before they start, while the owner/socket is healthy (`…01a05e53…jsonl:178`).

The flow then wrote and pushed `CriomOS-home` commit `51676f4eed1c2356faef799ebe8f0d12b933384c`, disabling that exact producer and adding a disposable app-server start/rollout/resume check. Its final transcript explicitly says the source-fit, Nix parse, and direct Codex `0.151.0` probe passed, but the durable Nix check had not run and nothing had been deployed or activated (`…01a05e53…jsonl:562`; `flows/01a05e53/log.md:11`). Treat this as a pushed candidate, not as active product state.

### 01a05d17 — separate Bird full-access request

This is related by product surface but separate by failure mechanism. The raw psyche record preserves the request: “her chatgpt desktop app doesnt start a new codex session with \"full access\" permission, as I want it to be” (`flows/01a05d17/vision/fullAccessPermission.md:3-5`; typed transcript at `/home/li/.codex/sessions/2026/09/01/rollout-2026-09-01T15-10-02-01a05d17-4904-71a1-bbe5-d92577b61e5d.jsonl:312`). That flow declaratively set Codex `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`, and its live probe says a fresh ephemeral Bird app-server thread resolved `never` and `dangerFullAccess` (`flows/01a05d17/log.md:5-9`). It left a UI-only witness open (`flows/01a05d17/log.md:13`).

The full-access policy does not explain a `codex_app` transport parse error: the former concerns session permission defaults, while the latter occurs during runtime MCP configuration loading before a thread can start or resume. Keep them as two acceptance axes.

## Evidence boundaries

The flow files above are written records from prior flows. Records under `witnesses/` and `reports/` identify the underlying method and are the strongest retained artifacts; `log.md` entries summarize what those flows believed they had established. The transcript line quotations are exact prior user/model text, but the model text is a claim from that prior flow, not a fresh witness in this flow. In particular, do not promote the pushed `51676f4e` candidate to deployed state without a current profile/deployment witness.

## Open questions returned to the caller

- Which Home/CriomOS generation is active for the currently failing Desktop, and does it contain `51676f4e` or only the earlier startup repair?
- Has the producer-disabling candidate passed the durable package check and an authorized deployment since `01a05e53` ended? That prior record says no.
- After activation, can a fresh Desktop `thread/start` and an existing `thread/resume` both complete, with no malformed runtime `codex_app` injection? This is the needed live acceptance witness.
- If Desktop App Tools are intentionally removed under Option 2, confirm that the desired scope is ordinary conversations through the persistent owner rather than the unruled Option 3 bridge that preserves Electron callbacks.

## Sources

- [Flow 01a03f49 report](/home/li/primary/flows/01a03f49/reports/codexPhoneRemoteControl.md:5)
- [Flow 01a047d2 log](/home/li/primary/flows/01a047d2/log.md:21)
- [Flow 01a047d2 topology vision](/home/li/primary/flows/01a047d2/vision/remoteControl.md:1)
- [Flow 01a05487 log](/home/li/primary/flows/01a05487/log.md:7)
- [Flow 01a05c80 log](/home/li/primary/flows/01a05c80/log.md:7)
- [Flow 01a05e53 log](/home/li/primary/flows/01a05e53/log.md:5)
- [Flow 01a05d17 log](/home/li/primary/flows/01a05d17/log.md:5)
- [Flow 01a05d17 raw vision](/home/li/primary/flows/01a05d17/vision/fullAccessPermission.md:3)
- [01a05e53 transcript, initial request](/home/li/.codex/sessions/2026/09/01/rollout-2026-09-01T20-55-28-01a05e53-8c4a-7503-b3c5-a04384d4dc20.jsonl:10)
- [01a05e53 transcript, diagnosis](/home/li/.codex/sessions/2026/09/01/rollout-2026-09-01T20-55-28-01a05e53-8c4a-7503-b3c5-a04384d4dc20.jsonl:178)
- [01a05e53 transcript, producer path](/home/li/.codex/sessions/2026/09/01/rollout-2026-09-01T20-55-28-01a05e53-8c4a-7503-b3c5-a04384d4dc20.jsonl:312)
- [01a05e53 transcript, final status](/home/li/.codex/sessions/2026/09/01/rollout-2026-09-01T20-55-28-01a05e53-8c4a-7503-b3c5-a04384d4dc20.jsonl:562)
- [01a05c80 transcript, healthy WebSocket claim](/home/li/.codex/sessions/2026/09/01/rollout-2026-09-01T12-25-03-01a05c80-3f85-7c83-9d44-094cf7d53582.jsonl:1473)
- [01a05d17 transcript, full-access request](/home/li/.codex/sessions/2026/09/01/rollout-2026-09-01T15-10-02-01a05d17-4904-71a1-bbe5-d92577b61e5d.jsonl:312)
