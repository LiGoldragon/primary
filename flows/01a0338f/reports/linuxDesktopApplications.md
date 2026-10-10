# Linux ChatGPT, Codex, and Claude applications

## What is installed

On `li@ouranos`, the launcher labelled **ChatGPT** is not OpenAI's official Linux package. It is a Nix build from the third-party `ilysenko/codex-desktop-linux` project:

```text
Desktop label: ChatGPT
Executable:    codex-desktop
Package:       codex-desktop-computer-use-ui-remote-mobile-control-26.721.41059
Runtime:       Electron 42.3.0 + loopback Python webview server
Source:        ilysenko/codex-desktop-linux 0.10.3, commit c6d76231…
Security:      Chromium and GPU sandboxes explicitly disabled
Codex CLI:     profile 0.149.0; resident GUI process still 0.148.0
```

On `bird@zeus`, the launcher labelled **Codex** is not any native Codex Desktop package. It is a Chrome PWA generated in Bird's browser profile. It launches Chrome 151 with app ID `ilpaeoofknldkmceepkoccjdocgbmbkj` and opens the Codex-in-ChatGPT web URL. The separate Nix-installed Codex CLI is 0.149.1.

```text
shared agent-intercom module
├── Ouranos has AgentIntercomGraphical
│   └── third-party native Codex Desktop Nix package → menu label “ChatGPT”
└── Zeus lacks AgentIntercomGraphical
    └── no native desktop package
        └── Bird's independent Chrome PWA → chatgpt.com/codex
```

This is why equal base machinery does not yield equal graphical applications: the shared module contains an explicit per-node capability gate, and the Zeus PWA is independent user/browser state. There is no witnessed deployment failure behind this difference.

Neither host has Claude Desktop actively installed. Both have Claude Code. Ouranos's current package is 2.1.241; Zeus's active embedded Home also resolves 2.1.241. Local URL-handler files and resident processes can lag those profile packages.

## Current upstream and Nix packaging

OpenAI's current documentation claims an official **ChatGPT desktop app for Linux** preview, distributed as signed `.deb` and `.rpm` packages for supported Debian, Ubuntu, and Fedora systems. The GUI includes Codex, while the open-source **Codex CLI** remains a separate Linux product. The generic ChatGPT download page may not present Linux as clearly as the Linux-specific documentation.

Anthropic's current documentation claims an official **Claude Desktop for Linux** beta, with signed APT packages/direct `.deb` downloads for supported Ubuntu and Debian on x86_64 and ARM64. This is distinct from **Claude Code**, the terminal agent already installed here.

At the inspected nixpkgs master state:

- `codex` packages the official Codex CLI, not a desktop application.
- `chatgpt` packages the macOS `.app` and is Darwin-only.
- `claude-code` packages the Claude Code CLI, not Claude Desktop.
- No canonical nixpkgs Linux package for either vendor's desktop GUI was found.

`numtide/llm-agents.nix` currently provides third-party Nix derivations named `chatgpt` and `claude-desktop` which repackage the vendors' official Linux `.deb` files. It also packages the two CLIs. These derivations are not vendor-maintained or nixpkgs, even though their payloads originate from vendor downloads. `aaddrick/claude-desktop-debian` is another explicitly unofficial repackaging project covering additional formats, including Nix.

Older projects which extract or patch macOS desktop bundles are now a worse trust and maintenance shape than packaging the official Linux payloads. The clean target for this environment would be a reviewed, pinned Nix derivation of each vendor's official Linux package, with the graphical capability decision made explicitly per node. In particular, the current Ouranos port disables Chromium sandboxing, so it should not be mistaken for an equivalent security/update path to OpenAI's official Linux build.

## Unknowns and probe side effect

Chrome History proves that Zeus launched the Codex web URL, but not the exact content the site rendered or any transient client-side redirect. Therefore the observed “download Codex for Linux” page is consistent with the PWA opening the website, but its page behavior was not independently reproduced.

During the Zeus inspection, one version command accidentally invoked Bird's Hexis-wrapped `google-chrome` path. It may have reconciled Bird's Chrome `Local State`; no before/after witness exists, so whether anything changed remains unknown. No package, profile, authored configuration, or other system state was changed by this investigation.

## Sources

- [Ouranos installation witness](../witnesses/ouranosChatgpt.md)
- [Zeus installation witness](../witnesses/zeusCodex.md)
- [OpenAI Linux app documentation](https://learn.chatgpt.com/docs/linux/linux-app)
- [OpenAI Codex app documentation](https://developers.openai.com/codex/app)
- [OpenAI Codex repository](https://github.com/openai/codex)
- [nixpkgs Codex derivation](https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/co/codex/package.nix)
- [nixpkgs ChatGPT derivation](https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ch/chatgpt/package.nix)
- [nixpkgs Claude Code derivation](https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/cl/claude-code/package.nix)
- [Anthropic Claude download page](https://claude.com/download)
- [Anthropic Claude Desktop installation guide](https://support.claude.com/en/articles/10065433-install-claude-desktop)
- [numtide llm-agents.nix](https://github.com/numtide/llm-agents.nix)
- [aaddrick claude-desktop-debian](https://github.com/aaddrick/claude-desktop-debian)
- Prior flows `01a032e5` and `01a03345`
