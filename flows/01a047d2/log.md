# Flow 01a047d2

Audit the connected remote-control designs and realizations remembered from flows 01a03f49 and 01a04524, determine what went wrong from current evidence, and explain visually how to recover the envisioned design.

Remembered: 01a03f49 — depth 3. It established one persistent per-user Codex app-server owner shared by phone and attached terminal TUIs, with Home Manager ownership and strong local protocol proof. It did not establish a cross-vendor owner, phone enrollment surviving restart, or successful Desktop integration; its last response left the Desktop gate broken.

Remembered: 01a04524 — depth 3. It knowingly substituted two vendor-owned servers for Codex parity. Its last response admitted activation failure and no live Claude/Desktop witness. The deployed Claude service used `/home/li`, which Claude refuses to trust; it retried 175 times and stopped. Ordinary Claude sessions were never routed into a shared owner.

Remembered: e06e4c07 — depth 1. Nexus vision rejects a giant monolith: independently useful Nexuses gain value by communicating, while each Nexus remains a whole long-running component with ordinary and privileged interfaces.

Remembered: 01a0437d — depth 1. Its relevant ruling scopes canonical package ownership to Codex and Claude; it does not settle remote-control topology.

Current state:
- Phone access recovered without a local mutation. Preserve the active Codex owner; it is healthy, protocol-initializable, and has an attached terminal client.
- The living reports that Codex Desktop currently cannot start, while the Codex server works. The living suspects the earlier attempt to make Desktop use that server; this cause remains a hypothesis until a launch witness grounds it.
- The Codex service was explicitly stopped and started at 04:04:53–04:04:54, but the requester and its relationship to temporary phone invisibility remain unknown.
- Claude's separate live unit is inactive and its source/deployment ownership has drifted.
- The living ruled that the target is one server for everything across Claude and Codex.

Settled audit conclusion: the failure was architectural before it was operational. The work treated vendor parity as sufficient and landed a second server even though the envisioned shared ownership property was absent; its tests proved generated configuration, not the real Claude trust/relay/session lifecycle.

The living clarified the recovery boundary: do not introduce a Nexus or cross-vendor broker. Keep the native server capability running for Codex and Claude, and have their desktop apps use it locally.

Working instruction: Preserve the currently live Codex remote server while the living is away. If another server is started during investigation, leave this one running. Continue toward one server for everything across Claude and Codex.

Working instruction: Before realizing the Desktop proxy, land the latest base package updates in the owning repositories, especially the new Codex TUI release. Design and test the proxy only against those landed versions.

Open:
- Determine the smallest native topology that lets each desktop app use its matching persistent local server without disturbing the live Codex owner.
- Claude still needs an explicit trusted workspace/root and proof that its Desktop client can use the persistent local server as intended.
