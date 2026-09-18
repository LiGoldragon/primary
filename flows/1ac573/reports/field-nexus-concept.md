# Field Nexus — conceptual report

Requested by the living as concept only. Nothing implemented, nothing deployed,
no service or store touched to produce it. First delivered in-terminal to the
living by flow 1ac573 on 2026-09-18 and landed here at the voice coordinator's
request so it is citable rather than scrollback.

Grounded in the living's own records, not invented: the triad psyche / mind /
field named as kshetra, with a Field Nexus named as the system monitor an agent
calls through the field CLI, which creates a signal carrying a traceback to its
caller (`flows/b05237/vision/operational-theField.md`); and the standing rule
that Field is an enduring role of which reaping is one capability, with a
protected Sol seat above Terra and Luna (the authored `field` skill).

## Boundaries

Field owns the ground: the machine, the infrastructure, the substrate flows run
on. Psyche owns vision and knows; Mind owns memory and databases; Field owns the
conditions of running. The separation is what makes Field safe to trust.

Field observes and maintains. Field never rules. It answers what is true of the
machine and repairs what is broken in it. It does not decide what work matters,
does not interpret vision, does not arbitrate between flows, and cannot
originate an instruction. A Field report is evidence; a Psyche ruling is
authority. If Field ever emits something a flow obeys rather than consults, the
boundary has been crossed.

Inside: process and seat liveness, disk and memory pressure, terminal and pane
health, service and socket reachability, quota and window state, orphaned
worktrees and build directories, stale registrations, reaping. Outside: what a
flow should do next, whether a vision statement holds, what a commit means, who
owns a lane.

Field is not Message and not Flow. It does not resolve logical identity to a
live target — Flow's contract — and it carries no messages and issues no
receipts. Field may report that a target looks dead; only Flow may say what that
target was, and only Message may claim anything about delivery to it.

## Triggers

Three kinds, kept typed apart because they carry different trust.

**Asked.** An agent calls the `field` CLI. Each call creates a signal carrying a
traceback to its caller, so every answer is attributable to who asked and why.
A Field reply is never anonymous.

**Scheduled upkeep.** Periodic sweeps Field owns by standing remit: pressure
checks, stale-registration detection, orphan collection. The only Field actions
with no caller, and therefore the ones needing the tightest written scope.

**Observed transition.** Field watches the substrate and emits on change — a
seat died, a socket stopped answering, free space crossed a threshold, a network
route dropped. Announcements, not commands. Subscribers decide.

Deliberately excluded: Field is never triggered by the content of work. Nothing
a flow is doing, thinking, or deciding may cause Field to act.

## State and ownership

Field holds one durable store of its own — its typed Sema store — and nothing
else. In it: the substrate inventory (hosts, seats, panes, services, sockets,
stores, disks), observation history with timestamps, upkeep policy, and the
outcome of every action Field itself performed.

Never in it: psyche of any level, flow lanes, work products, message bodies, or
anything a flow authored. If Field's store were lost entirely, nothing of the
psyche or the work would be lost — only observations Field can re-derive by
looking again. That property is the test of whether the boundary is intact, and
it should be checkable rather than asserted.

Ownership of the substrate is observational, not exclusive. Field is the
authority on what the machine's state is, not the owner of the machine's
purpose. A flow may act on its own resources without asking Field; Field reports
what happened.

Two sockets. The ordinary socket answers questions and accepts subscriptions
from any authenticated flow. The meta socket carries configuration and every
destructive capability — reaping, collection, deletion — because destruction is
policy and policy is privileged. Reaping a seat must not be reachable from the
ordinary socket even when the caller is right about the seat being dead.

Field is a vertex, not a hub. Peers depend on `signal-field` and
`meta-signal-field`, never on Field itself.

## Recovery

**Desktop and Herdr start.** Field starts with no arguments, its executable
owning its defaults; a fresh store persists them and a populated one resumes
them. On start it re-derives substrate truth by observation rather than trusting
its own last-written state, because the interesting case is exactly the one
where the machine changed while Field was not running. Its relationship to
Herdr is one-way: Field observes Herdr's panes and agents as substrate and never
assumes it is the only thing manipulating them.

**Crash recovery.** Field's own crash must be inert. Every upkeep action is
expressed so that dying midway leaves the action either done or not done, never
a half-state a later Field cannot recognize. On restart, Field reconciles intent
against observation and reports what it finds — including "I cannot tell what
happened here," which must be a typed answer rather than a silence. An action
Field cannot prove it completed is reported as unknown, never as completed.

**Network loss and job recovery.** Loss of reachability is an observation, never
a conclusion: unreachable is not dead, and Field must carry that distinction in
its vocabulary or it will reap live work. This is the highest-consequence
failure mode in the design — a Field that treats a partition as death destroys
running flows — so the conservative bias belongs in the types, not in an
operator's judgment. Recovering a job Field was watching means re-observing it
and reporting its present state; Field does not resume, restart, or re-dispatch
anyone's work.

**Subscriptions.** State is observed by subscription: current state on open,
then each change. Polling is forbidden; a quiet machine produces a quiet Field.

## Programmatically sourced prompt contributions

The part where the boundary is easiest to lose, so the rule is sharpest here.

Field can supply facts a prompt composer may include — what host this is, what
seats are live, what quota remains, what is under pressure. These are
contributions, not instructions. They enter a prompt as typed facts attributed
to Field and timestamped, at the stratum where evidence lives, never at the
stratum where vision and behavior live. A Field contribution may tell a flow
that disk is nearly full; it may never tell a flow what to do about it.

Three constraints follow. A contribution is attributed — the receiving flow can
always see that Field said it and when, so it is never mistaken for psyche or
for a rule. A contribution is refusable — a composer may decline it, and Field
cannot require inclusion. A contribution is fresh or absent — a stale fact is
marked stale or withheld, because a confidently wrong fact about the machine is
worse than no fact.

## Open questions

- Does Field reap on its own authority, or only on instruction? Reaping is named
  a Field capability, while the living has separately ruled that refresh itself
  performs the reaping — which places the act with the refreshing flow. These
  need reconciling before anything is built.
- Unreachable versus dead: what evidence licenses Field to call a seat dead?
  This belongs in vocabulary, not in a tunable threshold.
- Which seat runs Field, and does the monitor share the seat model of the
  monitored? Sol is protected and not to be spent on reaping or routine probing,
  but whether the long-running Nexus has a seat at all, or is plain
  infrastructure the seats call into, is unsettled.
- Does Field observe Mind? Databases are Mind's, but a database's disk, socket
  and process are substrate. The line runs inside that sentence and is undrawn.
- Whose store records an upkeep action that changed another component? Field's
  store holds what Field did; the affected component's history arguably should
  too.
- Is there a Field-side private layer? The private part is chartered and marked
  not active. If substrate facts can identify a host or an operator, Field's
  contributions may need the sterilization the private layer describes.
- What is Field's authority when it disagrees with Flow? Flow says a seat is
  Ready; Field observes it dead. Neither may overrule the other today, and the
  tie has no resolution rule.
