# R0 Field execution handoff

## Accepted artifacts and producer ownership

Astra 1mjd/ygzd accepts source and consumer assembly for Field Realize only: Flow `37980e10bcb8325d9a68c580e0d22c73061bb267` (full20 check attributes green), Home `1c5def7dc5f984c29b3f08aa62a055104de19ea9` (full projected97 green), CriomOS `5c71a9a7cc7f9d0dd99d8127957ab9b54cbb2ae5`. Home descends fromc58 and preserves generator/WantedBy; CriomOS descends from20e87723 and pins exact Home. Field alone produces Lojix Realize artifacts. Sol has submitted no deployment, Realize included. Existing ehrm templates/transports are unchanged except immutable consumer revision.

## Source-verified unit and storage facts

Home's `flow-0550.nix` and `flow-nexus-place.nix` retain `flow-nexus-0550.service` and `flow-configure-0550.service`; place remains `main`. New ExecStart is the new package's `flow-nexus-daemon main` (one place-name argument); the daemon reads the activation-compiled framed Place at the user's configuration-home `nexus/main/flow-nexus.signal`. Existing shared place State/Runtime directories remain the same. No store relocation or new state-copy destination is declared. The configure oneshot runs after the notify-ready daemon using the same pinned package's `flow-meta` and its versioned configuration home. Home writes the Place before reloadSystemd. Versioned wrappers are `flow-0.55.0` / `flow-meta-0.55.0`; bare paths are `~/.local/bin/flow` / `flow-meta`; hook is `flow-hook`. CLI datom filename and socket names are unchanged.

`UPGRADES.md` at accepted Flow records wire signal-flow64/meta-signal-flow83 and ordered stored upgrades: launch outcomes9→10→11; successor intents3→4→5; ordered replacements1→2; handover configuration1→2→3. Recovery wording is seeded once; publication deadline is seeded; configured text, including empty, persists. New warning families register empty; hook vector migration is separate. Ended-turn-retention absent row means64.

Opening refuses callerless queued/ordered Refresh before any registration/migration/staging writes. Both store-level and configuration-only open paths are gated; repeated refusal leaves original bytes/staging unchanged. Fresh open-refresh inventory is therefore mandatory immediately before the transition; historical evidence is insufficient. Field must settle those rows through supported operations before starting the new daemon. If inventory cannot establish safety, stop the cutover.

## Execution and recovery boundary

Before any first new-daemon open: Field's executor stops the old serving daemon/configure writer, takes and verifies a consistent copy of the actual Place State store (including its storage sidecars/companion data), and retains old generation/unit/configuration/Place metadata. Exact resolved paths, copy command and verification receipt belong to Field's executor; none was run or inferred here. The old and new daemons must not write one store concurrently.

An older daemon refuses the upgraded identities. Recovery is a coordinated return to the old declared generation AND restoration of the verified pre-upgrade state copy while writers are stopped; pointing the old executable at upgraded state is not recovery. Field must supply the exact restore-copy operation and retained generation before slot authorization. A partial activation still requires separate live profile/link/unit inspection; Lojix terminal state alone is insufficient.

After configuration replay: read back with the new pinned `flow-meta 'Configuration'`; prove configured context-warning policy vector empty, legacy reminder configuration retained, Place/runtime and unit binary correct. Repeat the no-policy proof after any replay. Field reapplies Maintained for Mind flowNexus Astra/Sol with the pinned contract's supported operation and verifies readback (dz3p); declared whole-family replay otherwise makes them OnDemand.

Energy timing remains Field's conditional Configure.Program update to `/home/li/.local/bin/flow`, only inside the approved transition after the new command exists and before completing sender proof. No source change or early live update is requested.

## Owners still required before live slot

Field Realize terminals/live-state executor and restore-copy details; Curriculum exact approved ProjectRoles agent replay (cc9ab9 says not ready); Psyche timed knowledge push; Astra live-package review; Field slot. Then h94r: Ouranos, Zeus; knowledge push and actual skills/agents projection; Sol restarts EVERY running Claude with new `flow-meta 'Restart.<FlowId>'` on its SAME session, checks returned session identity, and sends exactly the prescribed Notice once per running permaflow. Sol obtains one restarted-Claude Send, one Codex Send and an actual restarted-Claude hook reaching Flow. Field verifies Maintained; Psyche gets one live line. No alias, native warning run or policy enablement is included.
