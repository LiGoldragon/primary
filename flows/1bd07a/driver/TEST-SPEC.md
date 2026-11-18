# Source fixtures and current boundary

`test_controller.py`, `test_bootstrap.py`, `test_orchestration.py`, and
`test_wiring.py` are synthetic unittest sources. They are **unrun**. Syntax
parsing only has been performed. No build, provider, service, credential, native
or fixture execution has occurred.

The executable entrypoint binds the manifest and all three Python artifacts to
an admission record, then wires the production-before and held service cut to
private staging, auth metadata/link, daemon readiness, configuration and
reviewed rehearsals. The native matrix is not assembled: the workload returns
failure after rehearsals and cannot report a completed run. The template has
pending admission and runtime values. Independent review and Field admission
are required before any execution; this source and the package gate confer
neither. Test and review the admission authority, immutable artifact storage,
FIFO and service identity races, exact configuration/rehearsal contracts, and
terminal cgroup custody before using the entrypoint.
