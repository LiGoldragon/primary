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
