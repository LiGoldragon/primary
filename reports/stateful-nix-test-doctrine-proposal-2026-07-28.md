# Stateful Nix test doctrine proposal

Observation: Orchestrate's durable state boundary is meaningful only when a packaged daemon and its actual NOTA clients survive a restart in temporary state without touching a checkout, VCS, or live socket. A unit test of the service alone cannot witness the command, socket, codec, and package boundary together.

Proposal: add this one universal testing-skill line:

> Expose every durable test through a Nix check.

Placement decision:

| Surface | Keep / add | Reason |
|---|---|---|
| `testing` skill | add the proposed line | This is the cross-repository proof obligation: a durable-state test needs a durable gate, not merely local test discovery. |
| `nix-workflow` skill | no change | It already says substantial check/build implementation and long shell programs stay out of `flake.nix`; repeating it would duplicate a settled instruction. |
| standards repository | no change now | This is repository workflow and verification placement, not a Rust, Nix language, wire-contract, or domain standard. |

Application in this task: `flake.nix` remains an index; the substantial implementation is `checks/stateful-nix-scenario.sh`; the check consumes the packaged daemon, both packaged clients, a schema-parser assertion helper, and a typed upgrade-socket client. The scenario's temporary store and sockets isolate it from live state. Ordinary and meta replies are parsed as their published output enums rather than matched as text; upgrade replies are decoded as the version-handover contract frames.

The check deliberately avoids wall-clock label assertions. Its restart proof is typed route/state observation, while direct table tests prove the existing count-bounded diagnostic windows (activity 256, divergence 128, triage 256). Those windows are separate from the removed age/path reapers.

No skill or standard is edited by this task. The proposed sentence is returned for psyche approval before a generated-skill source change.
