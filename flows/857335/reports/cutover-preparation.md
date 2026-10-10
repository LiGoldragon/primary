# Orchestrate cutover preparation

## Sequence and boundary

The living’s sequencing remains: complete and audit the Protos, Datom, and
Ethos stack first; only then port Orchestrate, signal-orchestrate, and
meta-signal-orchestrate from ethos-monolith and the old Datom. The live Nexus
continues serving until a replacement has been tested in isolation and deployed.
This record authorizes neither a live service write nor activation.

The deployment owner is CriomOS-home’s generated unit. It must be regenerated
through its owner, never patched in place.

## Witnessed live shape

The read-only review observed the user Nix service as PID 2323, executing
`orchestrate` version `0.30.0` with no arguments. Its ordinary and meta sockets
are respectively:

- `/run/user/1001/orchestrate-nexus/orchestrate.sock`
- `/run/user/1001/orchestrate-nexus/meta-orchestrate.sock`

Its active store is
`/home/li/.local/state/orchestrate-nexus/orchestrate-nexus.sema` (638,976
bytes). The retired-looking
`/home/li/.local/state/orchestrate/orchestrate.sema` also exists and is not a
cutover input.

These observations are a point-in-time review finding, not a claim that the
live service remains unchanged after the observation.

## Required pre-cutover evidence

Staging must use isolated `XDG_RUNTIME_DIR` and `XDG_STATE_HOME`; it must not
bind an active live socket. The existing store persists old `Configure` and
tuple `Lock` archives. Reuse is unproven. Before any cutover, an isolated-copy
probe must either demonstrate archive compatibility or exercise a one-shot
migration that preserves configuration, every lock, and allocator state.

The required deployment evidence is therefore a tested replacement using the
new stack and the isolated state copy, followed by the deployment owner’s
ordinary generated-unit path. No claim of a successful migration or replacement
deployment belongs in this preparation record.

## Protected paths and receipt provenance

The original path prohibition remains even though current live-lock observation
may no longer show those historic locks.

Receipt 981 was released at
`/home/li/.codex/sessions/2026/09/09/rollout-2026-09-09T21-58-24-01a087c0-0ad8-72d3-a8cd-200ebc041ca9.jsonl:556`.
It records ownership by flow `f7941a` of these CriomOS-home paths:

- `owned-agents/codex/remote.nix`
- `packages/codex-artifact-gateway`
- `modules/home/profiles/min/agent-intercom.nix`
- `modules/home/profiles/min/niri.nix`
- `modules/home/profiles/min/codex-artifact-gateway.nix`
- `modules/home/default.nix`
- `checks/codex-remote`
- `checks/codex-artifact-gateway`
- `checks/codex-artifact-gateway-module`
- `flake.nix`

Receipt 982 is at
`/home/li/.codex/sessions/2026/09/09/rollout-2026-09-09T20-23-19-01a08768-fa0c-71a1-9582-ba49d3ccdd46.jsonl:177`.
It records flow `f7941a`’s plannotator worktree
`/home/li/wt/github.com/LiGoldragon/plannotator/capability-history-f7941a`
and `/home/li/primary/flows/f7941a/reports/capability-implementation.md`; it
does not record a CriomOS-home path. The same distinction is corroborated by
`/home/li/primary/flows/564f55/reports/postOutage.md:27-35`.

`flake.lock` is not among the original protected paths. This does not broaden
any later change authorization: the original prohibition still controls the
listed paths.

## Sources

- Root and contract-review read-only findings supplied to this flow for this
  report.
- `/git/github.com/LiGoldragon/orchestrate/src/defaults.rs:12-41`
- `/git/github.com/LiGoldragon/orchestrate/src/transport.rs:35-52`
- `/git/github.com/LiGoldragon/orchestrate/src/store.rs:55-76`
- `/git/github.com/LiGoldragon/orchestrate/tests/live_nexus.rs:12-59`
- `/home/li/primary/AGENTS.md` (generated deployment-unit ownership)
- The two receipt and post-outage locations named above.
