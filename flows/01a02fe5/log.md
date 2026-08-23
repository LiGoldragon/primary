# SSH access recovery

2026-08-23

Restored SSH access to localhost and all tested configured hosts. The live managed GPG SSH control had drifted to a foreign-node keygrip with no local secret key; a reversible bootstrap restored the already-declared Ouranos identity, Lojix deployment 52 converged it into current Home generation 52, and strict probes plus `jj status` passed.

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
