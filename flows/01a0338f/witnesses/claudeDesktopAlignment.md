# Claude desktop and terminal alignment

Method: probe official Anthropic documentation, APT metadata, release metadata, and the current official amd64 `.deb` through the delegated `claude_code_alignment` subflow on 2026-08-25.

Anthropic documents Claude Desktop and Claude Code as using the same underlying engine and sharing `CLAUDE.md`, settings, MCP configuration, hooks, skills, and project memory. They keep separate session histories. Desktop includes and manages its own Claude Code runtime; installing the standalone CLI is only required for terminal use.

The inspected official payload exposed four independent identities:

```text
Desktop:                    1.34493.1
Desktop-embedded Code:      2.1.237
Standalone current Code:    2.1.241
Desktop Agent SDK wrapper:  0.3.237
```

The official `.deb` contains no standalone `/usr/bin/claude`. Static bundle code holds the embedded Code manifest, platform checksums, download logic, and a user-data runtime location. Anthropic publishes no supported contract that makes Desktop invoke the separately Nix-packaged `claude` executable.

A Nix derivation can assert the vendor `.deb` version/hash, payload identity, embedded Code version/checksum, and an independently pinned standalone Code version/checksum. It cannot honestly claim parity unless the embedded and standalone Code versions actually match, and it cannot force them to match without delaying one release stream or relying on unsupported Desktop internals.

The audit tuple is:

```text
Desktop = (desktopVersion, debHash, embeddedCodeVersion, embeddedCodeChecksum)
CLI     = (cliVersion, platform, cliChecksum)
```

Any difference must be reported as skew rather than hidden by the unrelated Desktop version.

## Sources

- [Claude Desktop Linux](https://code.claude.com/docs/en/desktop-linux)
- [Claude Desktop reference](https://code.claude.com/docs/en/desktop)
- [Claude Desktop installation](https://support.claude.com/en/articles/10065433-install-claude-desktop)
- [Anthropic APT Release](https://downloads.claude.ai/claude-desktop/apt/stable/dists/stable/Release)
- [Anthropic amd64 package metadata](https://downloads.claude.ai/claude-desktop/apt/stable/dists/stable/main/binary-amd64/Packages)
- [Claude Code 2.1.241 manifest](https://downloads.claude.ai/claude-code-releases/2.1.241/manifest.json)
- [Claude Code 2.1.241 release](https://github.com/anthropics/claude-code/releases/tag/v2.1.241)
