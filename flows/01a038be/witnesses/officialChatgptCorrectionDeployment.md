# Official ChatGPT Linux correction deployment witness

Scope: the authorized declarative replacement of the obsolete converted
Codex-Desktop integration. No ChatGPT window was launched, no OAuth flow was
replayed, and no authentication or callback data was read.

## Source and proof

CriomOS-home commit `2fb9f089fafb08fe3396e938a9a5ca5de34c6845`
(`home: use official ChatGPT Linux package`) pins `llm-agents` to audited
revision `ed38c11e34e72199025ab70dc0042d78ef4c64cd`, removes the old
`ilysenko/codex-desktop-linux` input/module/service wiring, and reuses the
existing declared `packages/codex` derivation everywhere Codex is needed.

At the existing medium graphical gate it packages the official ChatGPT Linux
`26.818.61809` executable behind a small wrapper that exports its exact shared
Codex CLI path. It declares `chatgpt.desktop` in the active XDG applications
directory and makes it the `x-scheme-handler/codex` default. The existing
Claude Desktop package, XDG desktop entry, and `claude` URI default remain
unchanged.

The focused graphical-TUI contract was evaluated from the clean GitHub Home
revision with materialized Ouranos system/Horizon inputs. The contract then
built with local jobs disabled, fallback disabled, and `/etc/nix/machines`.
Prometheus remotely built official ChatGPT, the shared Codex CLI, the wrapper,
Agent Intercom, its profile, and the contract. The contract verified:

- ChatGPT `26.818.61809`, `Exec=chatgpt %U`, and its `codex` URI MIME type;
- `CODEX_CLI_PATH` in the wrapper is the exact shared Codex executable;
- Claude Desktop still has `Exec=claude-desktop %U` and its `claude` URI MIME
  type; and
- both generated default mappings resolve to their declared desktop entries.

The remotely built Codex package successfully version-checked as `0.149.1`.

CriomOS commit `e8b3e8e9951b10585f7de8b32a512dd395564ba1`
(`criomos: pin official ChatGPT Linux package`) pins the exact Home revision.
Its materialized and clean-GitHub-source NixOS target evaluations completed
with only pre-existing deprecation warnings. Its final top-level build ran on
Prometheus with the same remote-only settings and completed successfully.

## Activation and live evidence

Before admission, Lojix checked host-key material for logical
`goldragon/ouranos`; the immutable proposal was an absolute regular,
non-symlink `.dotos` file; and strict BatchMode SSH to the explicit endpoint
reported host `ouranos`.

Lojix owner request `Deploy.UserEnvironment` used user `li`, immutable Home
revision `2fb9f089fafb`, output `homeConfigurations.li.activationPackage`,
`HomeManagerNixProfileV1`, `ActivateNow`, `RequireImmutable`, `Horizon`, and
the configured builder list. It returned deployment `63`. The ordinary
deployment-ID reader again had its established frame-read error, but ordinary
node-ledger observation showed terminal record `1489` as `Completed` and
`Succeeded`; the active UserEnvironment record marks deployment `63` Current
for the exact Home revision.

```text
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.dotos github:LiGoldragon/CriomOS-home?rev=2fb9f089fafb08fe3396e938a9a5ca5de34c6845 (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
DeployAccepted.(63 (1489 1489))
```

Post-terminal strict SSH showed a changed Home-generation fingerprint. The
active Home path contains executable `chatgpt`, does not contain the old
`codex-desktop` wrapper, and its ChatGPT wrapper resolves to official
ChatGPT `26.818.61809` with the exact active shared Codex target. The shared
Codex reports `codex-cli 0.149.1`.

Live desktop checks returned:

```text
x-scheme-handler/codex=chatgpt.desktop
x-scheme-handler/claude=claude-desktop.desktop
desktop-entries=present-and-URI-capable
```

No manual Home Manager switch, retry, rollback, reboot, garbage collection,
stateful installer, ChatGPT launch, or OAuth interaction occurred.
