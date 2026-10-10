# Application updates

Flow `985ba2`; implementation thread `01a081a0-a02a-7810-b516-9e4b7ef3db8a`.

## Result

CriomOS-home `1f15866698d4` updates Codex from 0.153.3 to 0.153.4
and ChatGPT Desktop from 26.901.31953 to 26.901.51231. CriomOS
`b7dced0a58d1` pins that exact Home producer. Both commits were pushed to
`main` before evaluation and build.

The deployed Home profile directly reports `codex-cli 0.153.4` and Claude
Code `2.1.263`. Its launcher targets resolve ChatGPT `26.901.51231` and Claude
Desktop `1.46388.2`. Lojix reports deployment 235 as the Current
UserEnvironment generation at the same live Home profile and immutable CriomOS
revision `b7dced0a58d1`.

## Signed update evidence

The repository-owned Codex updater read OpenAI's official GitHub releases and,
after the update, reported 0.153.4 as both current and latest. Its initial run
could not discover the Cargo hash because a bare Home flake intentionally lacks
the Lojix-projected `system` input. No updater or input boundary was changed.
The flow reused published candidate `590bb08428a0`, whose only changes were the
official source hash and version; its Cargo and rusty-v8 pins were unchanged.
The later Lojix remote build witnessed that source and dependency hash together.

The ChatGPT updater verified pinned OpenAI archive-key fingerprint
`3BFA0E4AE8B8CC16A2D9BA684A3B4A566C4660E4`, verified the signed APT
`InRelease`, checked each architecture Packages index against its signed size
and SHA-256, required matching amd64 and arm64 versions, and generated the
26.901.51231 URLs and hashes.

The Claude Code updater read Anthropic's vendor release channel and reported
the existing 2.1.263 pin current. The Claude Desktop updater verified pinned
Anthropic archive-key fingerprint
`31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE`, independently verified both
`InRelease` and `Release.gpg`, required their bodies to match, verified both
architecture indexes, and reported the existing 1.46388.2 pin current.

## Build and deployment witness

Before mutation, hostname, name resolution, and the live Yggdrasil address
showed that logical node `goldragon/ouranos` and explicit destination
`li@ouranos.goldragon.criome` identify this machine. The proposal source was an
existing regular non-symlink. Both requests used the configured remote builder,
the explicit user-scoped store transport, Horizon inputs,
`HomeManagerNixProfileV1`, and `RequireImmutable`.

- Deployment 234, `UserEnvironment.Realize`, was accepted at `(6226 6226)`
  and completed at `(6242 6242)` with `Some.Succeeded`. While it ran, process
  observation showed Lojix owning one Nix build and Nix owning one SSH builder
  connection to Prometheus; no local or duplicate build ran.
- Deployment 235, `UserEnvironment.ActivateNow`, was accepted at `(6247 6247)`,
  progressed through Building and Copying, and completed at `(6280 6280)` with
  `Some.Succeeded`. `Query.ByNode` then reported 235 as `LiveActivation Current`.

Direct post-activation executable and launcher-target probes produced the four
versions above. No reboot or emergency runtime mutation occurred.

## Restart and remaining image check

Home activation restarted `codex-remote-control.service` because its executable
changed. Before activation it was PID 2217 on Codex 0.153.3. After activation,
systemd reported active PID 326495 on Codex 0.153.4, started at
2026-09-08 17:45:32 CEST with `NRestarts=0`. This planned service replacement
is the flow's likely cause of the conversation interruption at activation.

The later reconnection around 18:43 did not coincide with another service
restart: PID 326495 stayed live, while a new `codex-code-mode-host` process
started at 18:43:23. At 18:46:24 the service logged that custom tool output was
missing for the aborted call, consistent with the recovered connection's
uncertain-submission warning. Deployment 235 was queried rather than resubmitted.

The ChatGPT GUI was preserved. PID 297785 still runs 26.901.31953 from
16:28:29. The profile contains 26.901.51231, so a user relaunch is required to
run the update. The blank-image bug remains open until that new GUI visibly
renders an image; package installation does not witness renderer behavior.

Both isolated implementation workspaces were clean, forgotten from Jujutsu,
and removed after their commits landed. Orchestrate locks 972 and 973 were
released. The old Codex candidate is a published bookmark rather than a live
workspace or lock and remains as historical repository state.

## Sources

- CriomOS-home owned package sources and update programs at `1f15866698d4`.
- CriomOS `flake.nix` and `flake.lock` at `b7dced0a58d1`.
- OpenAI Codex releases: `https://api.github.com/repos/openai/codex/releases`.
- OpenAI signed ChatGPT repository:
  `https://persistent.oaistatic.com/codex-app-prod/linux/deb`.
- Anthropic Claude Code release channel:
  `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases`.
- Anthropic signed Claude Desktop repository:
  `https://downloads.claude.ai/claude-desktop/apt/stable`.
- Direct Lojix replies for deployments 234 and 235; direct profile executable,
  launcher symlink, systemd state, journal, and process observations made by
  implementation thread `01a081a0-a02a-7810-b516-9e4b7ef3db8a`.
