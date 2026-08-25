# Remembered Desktop deployment

Flow `01a0338f` investigated what the Linux ChatGPT/Codex and Claude entries actually installed and how official and unofficial Nix packaging related.

It settled that Ouranos's `ChatGPT` launcher was an unofficial Nix-built Electron port from `ilysenko/codex-desktop-linux`, with Chromium/GPU sandboxing disabled and a resident GUI app-server on an older Codex CLI than the profile. Zeus's `Codex` launcher was a Chrome-created PWA opening `chatgpt.com/codex`; Zeus had no native Codex Desktop package. Neither host had Claude Desktop, although both had Claude Code. The flow also found official Linux vendor payloads and third-party Nix routes, but did not authorize a package or deployment change.

Its remembered psyche rulings require three constraints: Desktop applications target medium-size graphical nodes; a third-party flake must pass a repeatable source/install audit on every update; and terminal/Desktop engine versions must line up or their skew must be explicit. The flow's alignment evidence makes the vendor distinction material: Codex Desktop supports `CODEX_CLI_PATH`, so the same pinned Codex derivation can serve terminal and Desktop app-server checks. Claude Desktop embeds/manages its own Code runtime and offers no supported external CLI override, so exact equality is not enforceable through the standalone package.

The light current-state check finds the Home consumer clean but still carrying the unofficial Codex Desktop input and no Claude Desktop projection. The direct Codex and Claude Code packages are projected in the local Agent Intercom profile; Codex Desktop is gated by `AgentIntercomGraphical`. Current cluster data marks Ouranos and Tiger as `Max` plus graphical and Zeus as `Max` without graphical; no exact Medium graphical node is present. CriomOS currently has unrelated dirty edits, so it is not a clean deployment baseline.

The parent realization may implement only after the sibling external-flake audit returns a source-safety conclusion. This memory does not conclude that the flake is safe, select a provider, settle Claude's release-skew policy, or authorize any deployment mutation.

## Sources

- [Remembered flow log](../../01a0338f/log.md)
- [Desktop packaging anatomy](../../01a0338f/reports/desktopPackagingAnatomy.md)
- [Installed Linux applications](../../01a0338f/reports/linuxDesktopApplications.md)
- [Codex alignment witness](../../01a0338f/witnesses/codexDesktopAlignment.md)
- [Claude alignment witness](../../01a0338f/witnesses/claudeDesktopAlignment.md)
- [Medium graphical node ruling](../../01a0338f/vision/mediumGraphicalNodes.md)
- [Package audit ruling](../../01a0338f/vision/packageAuditProtocol.md)
- [TUI/Desktop version ruling](../../01a0338f/vision/tuiAndDesktopVersions.md)
- [Current Desktop deployment witness](../witnesses/currentDesktopDeploymentState.md)
- [Setup-independent interfaces](../../../psyche-raw/Vision/setupIndependentInterfaces.md)
