# SSH access recovery

2026-08-23

Restored SSH access to localhost and all tested configured hosts. Lojix deployment 49 had installed the Zeus Home environment on Ouranos, leaving a GPG SSH keygrip with no local secret key; a reversible bootstrap restored the already-declared Ouranos identity, Lojix deployment 52 converged it into current Home Manager generation 974, and strict probes plus `jj status` passed.

Remembered: 01a0193f, 01a01959 — depth 1

The 2026-08-19 incident was a Lojix-daemon authentication-agent boundary failure: the interactive user manager had the GPG SSH-agent socket, the daemon did not. It is a lead only because the current report includes interactive SSH and localhost.

2026-08-24 — Direct recovery found the managed `sshcontrol` selecting a
different cluster node's keygrip: it had no local secret key, so OpenSSH saw
no identities. The source-declared Ouranos keygrip was locally available and
already authorized. The normal activation first failed before activation while
the SSH identity was unavailable; an authorized, reversible bootstrap exposed
the source-declared identity and restored every strict SSH probe. Deployment
52 then completed and became current; `sshcontrol` was reattached to that
generation's managed file. Recovery copies remain in `~/.gnupg/`.

Coordination: the current grammar for `meta-orchestrate` parsed, but its
socket was absent; `orchestrate` had the same transport failure. The required
flow artifacts were therefore written without a claim under the advisory
safe-continuation rule. No repository commit was made.

2026-08-24 — Follow-up investigation opened to determine whether an agent
actually deployed a foreign-node Home environment, or whether the stale
managed keygrip arose from target projection, activation, or profile-state
drift. Transcript attribution, runtime provenance, and selection mechanism are
being investigated independently.

2026-08-24 — Follow-up attribution established. Deployment 49 requested the
logical user environment for `goldragon zeus li` while separately routing copy
and activation through `li@ouranos`. Lojix preserved both requested values:
Horizon evaluation selected Zeus's identity, and activation installed that
closure on Ouranos as Home generation 973. The submitting
`lojix_daemon_deploy_plan` agent constructed the mismatched pair. The surviving
record does not establish whether Zeus was intentionally approved or was stale
request context; the absent node/transport consistency invariant allowed the
mismatch to activate successfully.

2026-08-24 — The living ruled: “We need better skill training.” The exact
agent context and the owning skill invariant are being reconstructed before any
skill wording is proposed or edited.

2026-08-24 — Training-gap anatomy established. Visible user approvals did not
name Zeus. Shared variables encoded `DeploymentNode: zeus` alongside an
Ouranos store, SSH destination, and controller; the agent reused that mixed
template. Existing Lojix training explicitly preserved node and transport as
independent but did not distinguish build/evaluation from profile-changing
activation. The needed invariant is operation-specific: controllers, builders,
and textual routes may differ, but `SetProfile`/`ActivateNow` must prove that
the logical node and physical activation target are the same host before
submission. No skill was edited pending exact psyche approval.

2026-08-24 — The living rejected hardwiring a node through setup variables and
ruled that correctness should come from good training. The variable-origin
investigation was stopped; the proposed correction is confined to teaching
agents to understand and reconcile each request's logical node, controller,
builder, copy route, and state-changing activation target.

2026-08-24 — The living directly requested removal of the hardwired deployment
variables and a proposal for cluster-aware training: what the cluster and nodes
are, and how an agent verifies the node it is on, builds on, builds for, copies
to, and activates. Removal and proposal research were separated so authored
sources can be corrected without prematurely installing unapproved training.

2026-08-24 — All twelve `Deployment*` variables and their authored Lojix
bindings were removed, regenerated, validated, committed, and pushed. The
training proposal keeps topology facts in the current proposal/Horizon and adds
a compact Lojix request-topology model: controller, logical viewpoint,
evaluator, builder, copy target, and activation target are derived and witnessed
per request; state-changing endpoints must be proven to be the logical node.
The proposed wording and behavioral pressure tests are recorded without yet
editing the authored training.
