# CORE flow e43002

Identity claimed after the completed bootstrap: `CODEX_SESSION_ID=01a0a792-2d0e-7a53-ac0b-9b3e43002941 flow-id codex --flows-root /home/li/wt/github.com/LiGoldragon/primary/core-bootstrap-cf7879/flows` returned `e43002` before this lane was written. The CORE thread and its bootstrap turn existed first; this log does not retroactively claim the bootstrap had a flow ID.

Role: distinct CORE main, not a successor and not root primary `cf7879`. Its authoritative sources and byte/hash manifest are at `../cf7879-core-bootstrap-manifest.json`. Its initial Astra-medium response is witnessed in the CORE rollout, and it is read-only and finite.

Checkup association: the separate `core-checkup-cf7879` producer owns the checkup runner and timer wiring. Its `checkup(config, adapters)` remains a source-backed read-only adapter boundary for this CORE thread; it does not create a production scheduler, authority to restart, or an idle equivalence for approval wait.
