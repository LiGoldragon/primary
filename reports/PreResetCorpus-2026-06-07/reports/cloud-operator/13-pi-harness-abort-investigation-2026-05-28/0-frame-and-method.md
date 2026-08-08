# Pi harness abort investigation — frame and method

## Frame

The psyche showed a Pi screenshot where a failing `nix flake check github:LiGoldragon/schema-next/collections-horizon-2026-05-28 --print-build-logs` ended with `Command exited with code 1`, then Pi displayed `Operation aborted`, then compaction happened. The psyche asked this cloud-operator lane to investigate the Pi harness failure with a subagent and continue the Horizon / Lojix / CriomOS audit.

## Method

- Dispatch one read-only Pi-focused subagent in the background.
- Ask it to inspect the screenshot, Pi docs/code/log surfaces available locally, and distinguish ordinary command failure from an actual harness bug.
- Continue the main audit work in parallel instead of waiting for the subagent.
- Synthesize the subagent result into this directory after it completes.
