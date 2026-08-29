# Flow 01a047d2

Audit the connected remote-control designs and realizations remembered from flows 01a03f49 and 01a04524, determine what went wrong from current evidence, and explain visually how to recover the envisioned design.

Remembered: 01a03f49 — depth 3. It established one persistent per-user Codex app-server owner shared by phone and attached terminal TUIs, with Home Manager ownership and strong local protocol proof. It did not establish a cross-vendor owner, phone enrollment surviving restart, or successful Desktop integration; its last response left the Desktop gate broken.

Remembered: 01a04524 — depth 3. It knowingly substituted two vendor-owned servers for Codex parity. Its last response admitted activation failure and no live Claude/Desktop witness. The deployed Claude service used `/home/li`, which Claude refuses to trust; it retried 175 times and stopped. Ordinary Claude sessions were never routed into a shared owner.

Remembered: e06e4c07 — depth 1. Nexus vision rejects a giant monolith: independently useful Nexuses gain value by communicating, while each Nexus remains a whole long-running component with ordinary and privileged interfaces.

Remembered: 01a0437d — depth 1. Its relevant ruling scopes canonical package ownership to Codex and Claude; it does not settle remote-control topology.

Remembered: 01a048a6 — depth 2, while still active. Its settled ruling removes the `AgentIntercom*` node-gating model: distinct wrapped Codex/Claude executables belong wherever canonical packages do, while graphical, edge, configuration, and service effects must justify themselves independently. Its implementation and exact desktop predicate remain in flight.

Current state:
- Phone access recovered without a local mutation. Preserve the active Codex owner; it is healthy, protocol-initializable, and has an attached terminal client.
- The living reports that Codex Desktop currently cannot start, while the Codex server works. The living suspects the earlier attempt to make Desktop use that server; this cause remains a hypothesis until a launch witness grounds it.
- The Codex service was explicitly stopped and started at 04:04:53–04:04:54, but the requester and its relationship to temporary phone invisibility remain unknown.
- Claude's separate live unit is inactive and its source/deployment ownership has drifted.
- The living ruled that the target is one server for everything across Claude and Codex.
- The Desktop failure is now witnessed: ChatGPT selects stdio `resources/codex app-server`; the packaged CriomOS gate exits 126 instead of proxying it to the live Unix owner.
- Latest stable owned bases landed in CriomOS-home commit `0de3c17ce4c0439f44ead79af0db8c43f3e62ac4`: Codex 0.150.1, Claude Code 2.1.250, ChatGPT 26.825.31414, Claude Desktop 1.37937.3, and current VSIXes. Package and affected Home contracts passed remote builds.
- Codex Desktop proxy landed in descendant CriomOS-home commit `799f8fd2d549241c323f84f6ff80fe9255a76615`. Its packaged bare `app-server` invocation now transparently proxies into the existing owner-owned 0600 Unix socket; lifecycle commands remain rejected. Red/green behavioral contract, actual ChatGPT closure, normal owner contract, and isolated VM restart/reconnect are green.
- The CriomOS consumer pin was deliberately restored and its Locks released after 01a048a6 revealed that the pinned Home shape still contains obsolete AgentIntercom gating. Consumer integration awaits that active flow's successor Home revision.
- No new Home generation was activated. The live owner carrying this flow remains untouched; deployment is a separate handoff.
- Claude 2.1.250/Claude Desktop 1.37937.3 retain the native topology: one local `claude remote-control --spawn=same-dir` owner, while Desktop discovers/steers it through Anthropic's outbound relay rather than local IPC. `remoteControlAtStartup` must remain unset because it creates separate per-process owners.
- The living confirmed `/home/li/primary` as the Claude owner's workspace root. The smallest Claude correction is to replace invalid `/home/li` ownership with that trusted root. In 2.1.250, `remote-control --help` performs eligibility work and is not a safe passive probe.
- Flow 01a048a6 completed its gate removal and layered integration. Home main `1274c581a51172d4fc53455e0c0cbd761215006b` and CriomOS main `45e83fbc29497208414ca5a08587d28a8e9617f2` landed; its unrelated eager MS2130 kernel-review gate remains independently non-green.
- Home `ed6832cf59b492601b3cdff4710751b8d1b02832` now requires an explicit non-home trusted Claude root. CriomOS `b617a56d4eeec18bca380f808186fc0b72a52e99` pins it and sets only li to `/home/li/primary`. The exact li Home activation closure remotely realized green.
- Full immutable Ouranos/li activation is authorized next. It will upgrade Codex 0.149.1 to 0.150.1 and necessarily stop/start the current owner; Lojix durable state must carry verification across the expected flow disconnect.
- Lojix deployment 83 was admitted at marker 2092 but reached terminal failure at Eval at 19:50:09. No new Home generation or service unit activated: Codex remains old PID 1048440/0.149.1 and Claude remains inactive with old `/home/li` root. The ordinary `Query.ByDeployment` reader itself panics with the known wire framing defect. A possibly unresolved general per-user profile link is under read-only causal audit; no retry is authorized before cause and live state are separated.

Settled audit conclusion: the failure was architectural before it was operational. The work treated vendor parity as sufficient and landed a second server even though the envisioned shared ownership property was absent; its tests proved generated configuration, not the real Claude trust/relay/session lifecycle.

The living clarified the recovery boundary: do not introduce a Nexus or cross-vendor broker. Keep the native server capability running for Codex and Claude, and have their desktop apps use it locally.

Working instruction: Preserve the currently live Codex remote server while the living is away. If another server is started during investigation, leave this one running. Continue toward one server for everything across Claude and Codex.

Working instruction: Before realizing the Desktop proxy, land the latest base package updates in the owning repositories, especially the new Codex TUI release. Design and test the proxy only against those landed versions.

Working instruction: The living is home and no longer needs phone access, but this flow itself is attached to the live Codex owner. Do not restart, replace, or activate over that server from this session; prepare deployment as a separate handoff.

Working instruction: Do not defer or stage around the Codex 0.150.1 owner upgrade. The final deployment includes the server upgrade and therefore its required restart; perform it only from outside this server-attached flow.

Working instruction: Before repairing or relying on any `AgentIntercom*` consumer gate, remember flow 01a048a6. The living identifies those variables as leftovers from an obsolete Agent Intercom gating approach.

Working instruction: Flow 01a048a6 is still active on a parallel problem. Do not land an intermediate consumer pin or modify/reinterpret its in-flight gating work; respect its Locks and integrate only after its settled result is available.

Open:
- Determine the smallest native topology that lets each desktop app use its matching persistent local server without disturbing the live Codex owner.
- Wait for active flow 01a048a6 to release/integrate its Home gating-removal work before setting the Claude owner root to `/home/li/primary`.
- Land the eventual Home successor in CriomOS and prepare a separate deployment session; do not activate from this owner-attached flow.

Deployment closure:
- Home `a1b9383561f54fc77fd201734f49d4beed9c2826` exported the canonical overlay-applied package set without forcing a placeholder Home configuration. CriomOS `ee0ae00dcdb1d809e8855faba6f8dc2f4afc0a72` consumed that materialized boundary, repairing deployment 83's `Eval FlakeReferenceMalformed` cause.
- Lojix deployment 84 for Ouranos/li at immutable CriomOS revision `ee0ae00dcdb1d809e8855faba6f8dc2f4afc0a72` reached terminal event 296, `Completed` / `Succeeded`, at 2026-08-28 20:32:32 CEST.
- The activation replaced the Codex owner. Live `codex-remote-control.service` is healthy at PID 1664164, Codex 0.150.1; its 0600 Unix control socket is listening and accepts connections. The old PID required SIGKILL after its stop timeout, but the replacement is healthy.
- Live `claude-remote-control.service` is healthy at PID 1664163, Claude Code 2.1.250, rooted at `/home/li/primary`.
- A later successful deployment 86 selected Home generation 989 (generation 988 was deployment 84). The remote-control processes remain the healthy instances started by deployment 84; no mutation was made while checking.
- The remaining acceptance witness is graphical: launch ChatGPT Desktop and confirm that its packaged bare `app-server` path attaches through the proxy to the existing Codex owner. Claude Desktop should discover the one native Claude owner through Anthropic's relay; it is not a direct local-socket client.

Desktop acceptance correction (2026-08-29):
- Live ChatGPT 26.825.31414 launches reached the embedded gate and failed 126. The managed Codex 0.150.1 owner and its 0600 socket were healthy; the failure is not server availability.
- The earlier bare-`app-server` model was wrong for this Desktop build. Its exact launch schema is `-c features.code_mode_host=true app-server --analytics-default-enabled -c mcp_servers.codex_app=<dynamic config>`. The final config includes a per-launch `CODEX_APP_TOOLS_PIPE_PATH` owned by Electron.
- ChatGPT contains a native local-daemon connection path, and the Home wrapper requests it. However, the Desktop code uses that path only when `getConfigOverrides()` is empty. Local Desktop always supplies the dynamic `codex_app` override (or a disabled fallback), so it deliberately falls back to a private stdio app-server before daemon compatibility is considered.
- The installed Linux ChatGPT package exposes no launch-at-login/autostart setting or unit. The separately enabled `codex-remote-control.service` is the login-session persistent owner (`Linger=no`); externally autostarting the GUI would only start the GUI and its private child.
- Widening the gate to accept the six arguments and then executing `app-server proxy --sock` would be a false green: Codex 0.150.1's proxy forwards bytes but discards startup `-c`, feature, and analytics options. It would silently remove Desktop's dynamic app-tools MCP surface and its Electron approval/result routing.
- Therefore the observed Desktop build cannot both preserve its native dynamic app-tools behavior and attach to the existing process-global owner through a simple gate. Correct options are: allow Desktop its private native Core while retaining the shared owner for TUI/phone; accept a reduced Desktop without app tools; or design an authenticated per-connection/per-thread bridge that injects and isolates dynamic MCP configuration. This is now an explicit psyche architecture decision; do not widen the matcher without it.
