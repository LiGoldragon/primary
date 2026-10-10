# Zeus Bird desktop-app diagnosis

Aim: Remember the latest Zeus deployment and determine why Bird on Zeus does not expose the Claude and Codex desktop applications.

Open: Reacquire the latest deployment flow, inspect the deployed and live application state on Zeus for Bird, identify the witnessed cause, and realize a correction if the existing design already rules it.

Remembered: 01a03f49 — depth 2 — latest Zeus host deployment identity, actions, final response, and Bird/li service witness.
Remembered: 01a0338f — depth 2 — Zeus/Bird application witness and node capability gates.
Remembered: 01a04524 — depth 1 — newer Claude/Desktop owner run; its final response explicitly says Zeus was not deployed.
Remembered: 01a047d2 — depth 1 — later audit; no newer Zeus activation and no cross-vendor desktop broker was authorized.

Settled: the latest actual Zeus host activation is deployment 76 (Evaluate 73, Realize 74, TestActivation 75, ActivateNow 76), with 76 Current. Its source is CriomOS 2fb323b0f2c7d0a06a28cc2c757c46799e4a9e0f, embedding CriomOS-home ba0de9f84130c47a927a04723db2cb6f33b6b103. The deployed Home profile's desktop gate requires both host capability AgentIntercomGraphical and a projected user size.medium. Goldragon's Zeus is Max/Edge with services [], while Bird has a Zeus user key/profile but no host Graphical capability. Therefore the deployed projection gives Bird CLI/remote-control facilities but does not enter the desktop package block; absence of Claude and native Codex desktop applications is explained by the capability gate, not by a witnessed failed host deployment. Historical Bird live evidence saw Codex as a Chrome PWA and no active Claude Desktop.

Open: current direct SSH to Zeus is unavailable (No route to host), so the post-76 launcher state cannot be freshly rechecked. The newer Desktop/Claude flow did not deploy Zeus. Whether Zeus should gain AgentIntercomGraphical and desktop apps is an unresolved psyche/authority decision; this investigation does not change that design.
