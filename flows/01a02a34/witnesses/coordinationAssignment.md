# Coordination assignment contract

Method: code read `orchestrate/AGENTS.md:115-117`,
`/git/github.com/LiGoldragon/orchestrate/src/execution.rs:255-312,453-513`,
`/git/github.com/LiGoldragon/signal-orchestrate/src/lib.rs:2670-2701`, and
`/git/github.com/LiGoldragon/signal-harness/src/lib.rs:399-475`; typed-message
lookup of the b7465e71 worker transcript line 1; current Curriculum skill-list
inspection; and historical Curriculum revision `kpnwrxpoqyms/full.md:95-97`.

`orchestrate/AGENTS.md:115-117` says that the harness names a session lane and
that an agent learns both lane and discipline from the harness. The contract
observations do not carry either value. `OrchestratorAgentRegistration` and
`AgentIdentityMintRequest` contain session, mission, harness, and identity
selection only. The execution path registers and mints those fields, then
builds a harness launch with only harness kind, minted identity, an initial
prompt containing identity plus mission, and `Fresh` continuation. The harness
`SessionLaunchRequest` has exactly those four fields.

The b7465e71 editing worker's transcript line 1 likewise has no concrete
session, lane, discipline, or Fresh-or-Recovery assignment. Current Curriculum
has no `session-lanes` skill. The historical Curriculum record
`kpnwrxpoqyms/full.md:95-97` instead placed concrete editing-worker assignment
at dispatch.

The resulting gap is witnessed: the local instruction attributes assignment to
the harness, but the observed V2 registration and launch boundary neither
transmits nor types the assigned lane or discipline. The evidence does not
identify who should assign them, what their values mean, which disciplines are
valid, whether `Structural` is universal, or whether this V2 identity shape is
still wanted.
