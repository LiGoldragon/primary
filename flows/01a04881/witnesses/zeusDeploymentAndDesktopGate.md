# Zeus deployment and Bird desktop gate

This witness records read-only reacquisition for the question why Bird on Zeus may lack Claude and Codex desktop applications. It does not authorize or perform a deployment change.

## Direct observations

### Latest Zeus deployment

`lojix 'Query.ByNode.(goldragon zeus None)'` returned the host chain:

- deployment 73: `Host.Evaluate`, `RequireImmutable`, completed, `Succeeded`;
- deployment 74: `Host.Realize`, completed, `Succeeded`;
- deployment 75: `Host.TestActivation`, `TestActivation`, completed, `Succeeded`;
- deployment 76: `Host.ActivateNow`, `LiveActivation`, completed, `Succeeded`.

The host tuple for 76 is `CompleteHost LiveActivation Current`, with NixOS system closure `m978snxl8ac5147z47iy930cm91vx5yc-nixos-system-zeus-26.11.20260813.0e251e2` and source CriomOS revision `2fb323b0f2c7d0a06a28cc2c757c46799e4a9e0f`. Source inspection of that CriomOS revision shows it pins Home revision `ba0de9f84130c47a927a04723db2cb6f33b6b103`. The current Lojix query therefore identifies 76 as the latest actual Zeus host activation and current state.

Flow `01a03f49`'s log/report and final response additionally claim that 75 and 76 succeeded and that li's and Bird's Zeus per-user remote-control services, sockets, and WebSocket initialization were live-verified. Those are that flow's witnesses, not a fresh SSH observation in this flow.

### Package gate in the deployed Home source

In Home revision `ba0de9f...`, `modules/home/profiles/min/agent-intercom.nix` derives:

```nix
graphicalEnabled = hasCapability "AgentIntercomGraphical";
mediumEnabled = profileUser.size.medium or false;
desktopEnabled = graphicalEnabled && mediumEnabled;
```

The `desktopEnabled` package block installs both `claudeDesktopPackage` and `chatgptWithSharedCodex`, and writes their desktop launchers/mime defaults. Thus user size alone is insufficient: the host capability is also required.

The authored `goldragon/datom.dotos` witness (current source, and unchanged in the deployed datom shape) defines Zeus as `Max`/`Edge` with its final services vector `[]`. Bird has a Zeus per-node public-key entry and a user projection, but that does not add `AgentIntercomGraphical` to Zeus. The earlier exact node-gate witness records `AgentIntercomGraphical` only on Ouranos and Tiger; Zeus has no such capability.

### Historical Bird application state

Flow `01a0338f`'s `witnesses/zeusCodex.md` records a direct-IP SSH inspection of `bird@zeus`: the visible Codex launcher was a Chrome PWA with `Exec=google-chrome-stable ... --app-id=...`, while a separate Nix Codex CLI resolved to 0.149.1. The same witness found no active Claude Desktop package/launcher/process, only Claude Code 2.1.241 (and an older Claude URL handler). Its final model response says Bird's Codex was a Chrome PWA, no native desktop was present, and neither inspected host had Claude Desktop.

## Interpretation boundaries

**Witnessed:** host deployment 76 is Current and succeeded through all four recorded actions; the deployed Home desktop gate requires `AgentIntercomGraphical && size.medium`; Zeus's node definition has no Graphical service; historical Bird state had Chrome-PWA Codex and no active Claude Desktop.

**Relayed claims:** `01a03f49` claims live post-76 Bird/li remote-control service and protocol verification. `01a04524`'s later final response says its newer canonical Desktop/Claude revisions were deployed only to Ouranos and explicitly that Zeus was not deployed in that run.

**Best-supported explanation:** Bird lacks both desktop applications because Zeus is not projected with `AgentIntercomGraphical`, so the Home desktop package block is false even where Bird's user projection is large/medium enough. The deployed Zeus action was a successful host activation, but it was not a Graphical-desktop enablement action.

**Unknown:** a fresh post-76 Bird launcher/process check could not be made here because `ssh root@192.168.18.95` currently fails with `No route to host`. The exact per-user Home generation for Bird is not separately identified by the host query. Whether the psyche now authorizes adding Graphical capability/desktops to Zeus remains open; no change is made. An earlier `01a0338f` probe may have reconciled Chrome Local State, an unrelated possible side effect that does not alter the package-gate conclusion.

## Sources

- `flows/01a03f49/log.md`, `flows/01a03f49/reports/codexPhoneRemoteControl.md`, and its retained session JSONL under `/home/li/.codex/sessions/2026/08/26/`.
- `flows/01a0338f/log.md`, `flows/01a0338f/witnesses/zeusCodex.md`, `flows/01a0338f/witnesses/currentNodeGates.md`, and `flows/01a0338f/reports/nodeConfigurationGates.md`.
- `flows/01a04524/log.md` and its retained session JSONL under `/home/li/.codex/sessions/2026/08/27/`.
- Deployed source revisions: CriomOS `2fb323b0f2c7d0a06a28cc2c757c46799e4a9e0f`; CriomOS-home `ba0de9f84130c47a927a04723db2cb6f33b6b103`; authored datom `goldragon/datom.dotos`.
