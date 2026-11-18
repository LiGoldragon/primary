# Proposal 2 kernel-owned cleanup controller — proposed final assembly shape

This replaces all numeric-PID/PGID cleanup instructions in bootstrap.md. It is
source-only, not an installed helper or runtime grant. Field's rr5e/dqmu accepts
this as a supported proposed boundary; exact source and actual witnesses remain
necessary. `herdr-containment-source.md` binds the examined installed launch
path. The native plan and its shared-auth race are accepted by Opus60hv.

## One private user service, one finite driver

Assemble the reviewed preparation/receipt/matrix blocks into ROOT/driver.sh;
its first act is to install EXIT/INT/TERM cleanup for private Flow/session state.
It launches all observers, supervisors, daemons, Herdr panes and native children
inside this service. It stops on every typed refusal, failed invariant or budget.
Do not run incomplete document blocks piecemeal. No bare-name kill is used.

The external Field operator reserves a unique unit name derived from the fresh
ROOT basename, with the complete name recorded before launch. It records the
reviewed Bash/Python/tool paths, exact ROOT and driver hash. It starts exactly:

```sh
UNIT="proposal2-${ROOT##*/}.service"
# Driver is the final immutable reviewed script, not an ambient shell profile.
systemd-run --user --unit="$UNIT" --service-type=exec --wait --pipe \
  --property=KillMode=control-group --property=SendSIGKILL=yes \
  --property=TimeoutStopSec=15s --property=RuntimeMaxSec=20m \
  "$REVIEWED_BASH" "$ROOT/driver.sh" "$ROOT"
```

The operator retains this foreground command through the terminal event. A
separate control tool may observe the owned service while it runs; it creates no
second native phase. The driver pauses before its first child on a private
ready/go FIFO so the operator can record InvocationID, ControlGroup, MainPID,
ExecMainStartTimestampMonotonic and exact service ExecStart. Required fields
must be nonempty and ExecStart must name this ROOT/driver.sh. Only then does the
operator release the one go receipt. The20-minute RuntimeMaxSec is the approved
whole native window, including preparation inside the driver; do not extend it.

The final driver may stage static files before the service starts, but creates
no child, auth link or native until its reviewed preflight/production witnesses
and cleanup owner are in place. Environment is private as in bootstrap.md.

## Identity and membership witnesses

Record the live unit identity once at the held startup cut:

```sh
systemctl --user show "$UNIT" -p Id -p InvocationID -p ControlGroup \
  -p MainPID -p ExecMainStartTimestampMonotonic -p ExecStart \
  > "$ROOT/evidence/unit-start.identity"
```

Capture the InvocationID and ControlGroup as exact parsed values, not shell
source text. Require unit Id exact-match and a nonempty cgroup under the user's
own slice; inspect no production cgroup. Retain its cgroup directory inode and
cgroup.events. This is a fresh uniquely reserved unit; no other work may create
or restart it during this test.

At server ready, each initial native ready and successor ready, record:
- each owned daemon/appserver and actual PTY/native PID with /proc startticks,
  executable and cgroup metadata (no full environment/prompt/credential dump);
- private Herdr agent list, then get for the exact pane, preserving native
  agent_session, terminal identity/title, revision and state_change_seq;
- correspondence of those actual processes to the saved ControlGroup, including
  any descendant subgroups, and the private Flow binding/native session.

Use the source-bound Herdr executable for list/get, under private environment
and the exact private session. PID metadata is evidence, not later kill authority.
A process outside the owned group fails containment. No whole-host membership
claim follows from a selected-process census. Since danger-full-access is used,
this is cleanup containment for the bounded commands, not a filesystem sandbox
or prevention of a deliberately escaping program.

## Graceful closure, then authoritative unit stop

The driver stores every confirmed FlowId immediately, plus pending launch
receipts when identity extraction fails. Before normal completion it captures
private Inspect for both synthetic addresses and private Herdr list/get. It
closes exactly the initial receiving identities or actual successor through
private flow-meta Close, captures typed Closed/refusal, and observes each exact
native/pane to its terminal event. A failed closure is retained, not relabelled
success. All such observers themselves remain inside the same unit.

Normal or interrupted completion returns through the unit's control-group stop:
remaining daemon, supervisor, PTY and native descendants are signalled by the
kernel-owned service boundary. A service-leader pidfd alone is not the witness.
If manual stop is required, the external owner first rereads InvocationID and
ControlGroup and compares them to the saved values. Any mismatch means STOP:
do not signal the name or a numeric PID; retain the slot and report custody.
For an exact match, the only operator stop is:

```sh
systemctl --user stop --job-mode=fail "$UNIT"
```

The foreground systemd-run --wait completion supplies the service terminal
receipt; it does not by itself prove every descendant exited. After that event,
require the exact saved cgroup (including descendants) to be absent, or its
cgroup.events to say populated0. Save that read. A live process or uncertain
external child retains the resource allocation and evidence. Never kill a
production unit, an executable-name match, or a saved numeric process group.

## Retention and production comparison

After owned-unit terminal/empty proof, run production-witness.md's exact after
capture and compare. Preserve ROOT/evidence, driver/hash, private transcripts,
receipts and model usage to a retained report directory outside disposable
source/native workload. Unlink only ROOT/codex/auth.json as a link; its approved
production target is never removed, read or hashed. Remove only the recorded
ROOT workloads after evidence retention and descendant reconciliation.

## Remaining assembly facts

The driver code, its go/ready pause, unit metadata parser and graceful pane
closure event commands must be written and independently reviewed as one
immutable executable artifact. This document names the supported stop boundary;
it is not a claim those commands already exist or have run. Concrete gated
package outputs, provider paths and whole-gate success remain prerequisites.
