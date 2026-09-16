# CORE writer handoff

CORE `e43002` owns the clean Jujutsu producer workspace `/home/li/wt/github.com/LiGoldragon/primary/core-e43002`, published as `proposal/cf7879-core-e43002` from revision `3b0750634058`. It is the future scoped writer workspace; it does not move `main` or authorize repairs.

On 2026-09-16, supported app-server `thread/resume` for existing CORE thread `01a0a792-2d0e-7a53-ac0b-9b3e43002941` was called with this workspace as `cwd`. The returned thread remained at `/home/li/wt/github.com/LiGoldragon/primary/core-bootstrap-cf7879`. Thus resume treats the supplied cwd as a consistency check for a running thread, not a working-directory update. CORE remains read-only until a supported thread-cwd transition or a new explicitly authorized runtime is available.

The separate core-checkup producer may provide bounded facts for CORE to consider. Its transient timer and Luna analysis are not a production scheduler; approval-wait is not idle and restart policy remains with that producer.
