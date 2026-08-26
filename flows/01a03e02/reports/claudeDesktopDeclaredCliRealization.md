# Claude Desktop uses the declared Claude Code

## Outcome

CriomOS-home `origin/main` commit `656afcdd1f56ea135ab0b0aaec084a215ba5a4b6` makes Claude Desktop local sessions use the exact `claudeCodePackage` already selected for the terminal. Desktop no longer has an allowed path to download, invalidate, copy, or otherwise materialize a second Claude Code executable when the declared override is configured. If the declared executable is absent or non-executable, the override terminates rather than falling back.

The shared `llm-agents.nix` input advance changes Claude Desktop from `1.34493.1` to `1.37937.1`, Claude Code from `2.1.241` to `2.1.246`, and ChatGPT Desktop from `26.818.61809` to `26.820.60940`; Codex remains `0.149.1`. The separately pinned VSCodium Claude extension remains outside this package relationship.

## Runtime anatomy

The hash-verified current Anthropic payload still reads `CLAUDE_CODE_LOCAL_BINARY` without invoking `initLocalBinary`. The package patch activates that dormant initializer, changes invalid declared-binary handling from log-and-fallback to a terminal error, prevents host invalidation while the override is configured, and rejects the VM path before it can copy the Nix executable into mutable user state. It leaves the vendor resolver in place, using its existing `local_override` branch.

This is narrower than rewriting the resolver or enabling `nix-ld`: the Nix package supplies one immutable executable, and the application retains no successful stateful fallback. Exact minified markers are fail-on-drift package inputs, so a future Desktop update must be re-audited rather than silently bypassing the patch.

## Proof

The durable `claude-desktop-declared-cli` Nix check extracts the final patched ASAR into a test copy, boots the package's production Electron runtime with a test entrypoint under declared DBus and Xvfb facilities, exports the actual closure-bound manager class, and drives its real valid/missing override, resolution, preparation, invalidation, VM, and update paths.

The test was witnessed failing on Prometheus after its expected terminal error was deliberately made wrong. The corrected derivation `/nix/store/5al3mj2jwjp9ijawv8cj3zajjdzs5r42-claude-desktop-declared-cli-contract.drv` then built on the configured Prometheus builder with `max-jobs 0` and `fallback false`; the client exited `0`. Its phase log records the actual manager loading, exact resolution to `/nix/store/...-claude-code-2.1.246/bin/claude`, and the missing-override terminal branch. Persistent witnesses make the test fail if any downloader, copy, removal, or cleanup fallback is invoked even when application code swallows the helper error. The manager-owned executable roots `Claude/claude-code` and `Claude/claude-code-vm` remain absent.

The built wrapped Desktop launcher also returned `1.37937.1` with exit `0` in fresh HOME/XDG state. This smoke did not open the GUI or touch an account. Independent review of the final correction found no remaining contract-test blocker.

## Deployment boundary

The change is on GitHub `origin/main`, proven at its Home repository boundary, and not deployed. A separate authorized realization must advance the layered CriomOS consumer, build and deploy that immutable target, then start one fresh local Desktop thread to witness the live account/GUI path and absence of manager-owned executable state.

## Sources

- [CriomOS-home Claude Desktop overlay](/git/github.com/LiGoldragon/CriomOS-home/overlays/claude-desktop.nix).
- [Current-payload patcher](/git/github.com/LiGoldragon/CriomOS-home/overlays/patch-claude-desktop-runtime.mjs).
- [Claude Desktop runtime contract](/git/github.com/LiGoldragon/CriomOS-home/checks/agent-intercom-graphical-tui/claude-desktop-runtime-contract.cjs).
- [Agent Intercom package projection](/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix).
- [CriomOS-home architecture](/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md).
- [Anthropic Linux APT package index](https://downloads.claude.ai/claude-desktop/apt/stable/dists/stable/main/binary-amd64/Packages).
- [`llm-agents.nix` Claude Desktop package](https://github.com/numtide/llm-agents.nix/blob/76b78a399417964e9133aed0c0a9493616c3508e/packages/claude-desktop/package.nix).
- [Dormant-override upstream report](https://github.com/anthropics/claude-code/issues/84371).
- [Prior Nix ASAR activation patch](https://github.com/diwangs/nixos-config/blob/e032a41f78829ced7f9d4245fddd088fad64a7d5/package/overlay/claude-desktop/patch/cli-path.nix).
- [Environment-only Nix wrapper prior art](https://github.com/tiborpilz/NixOS/blob/717726dfbab2bb29938ec415a7e1486776364a6c/packages/claude-desktop/claude-desktop.nix).
- [Environment-only counterexample](https://github.com/BeatLink/TechNet/blob/d73a9b8625b7bf4fbe4e7060765c14c7e299936c/nix/3-laptop/4-apps/programming/claude-desktop.nix).
- Flow `01a038be`, especially its deployment log and stateful-installation ruling.
- Flow `01a03e02` local probes, current-payload inspection, remote build reports, and independent review subflows.

