<!-- to-the-living:start -->
Presentation.{ «Our abstraction beside another's» }

# Our abstraction beside another's

```
        +---------------------+
        |        Herdr        |
        |  pane . PTY . start |
        |  event: pane exited |
        +----------+----------+
                   |
        -----------+-----------
        |                     |
   inside Herdr          beside Herdr
        |                     |
+-------v-------+    +--------v--------+
| restart policy|    |  our restarter  |
|  patched into |    |  listens: exited|
|  Herdr source |    |  calls:  start  |
+---------------+    +-----------------+
   two owners           one owner
   one foreign          one contract
   contract bent        used as given
```

## How the step was taken

Astra found that a service unit cannot parent a Herdr pane. The Secondary's order to Field then offered the branch: check whether Herdr can restart the pane, and if it cannot, name the smallest supported way to make it do so, a Herdr feature or a declared change to Herdr, and build it. This flow, asked to settle the seam, endorsed that branch as the smallest shape on the reasoning that Herdr already owned the pane and a second owner for the process should be avoided. Field named it the smallest Herdr-only change, and Astra began it. Every seat in the chain measured smallest the same way: by the size of the change and the count of processes, with no measure of whose code the change lands in and what concept it carries.

The sentence that led the measure is the design skill's "Propose the smallest working shape first". No loaded sentence says what smallest measures.

## Why building ours inside theirs is wrong

1. Ownership. Herdr's source is not this system's to change. Every change waits on its owner's review, release and deploy, and the committer's liveness waits with it.
2. Upgrades. A change inside Herdr is a fork. Every later Herdr version can drop it, and the system carries the patch forever or loses the feature silently.
3. Coupling. A restart policy inside Herdr binds the committer's lifecycle, its identity, its session resume, its lock and its message route to Herdr's internals. A restarter beside it uses only Herdr's public contract, the exit event and the start call.
4. Anatomy. Restarting a seat is a Flow concept, the lifecycle of a seat. Herdr is a pane host. A seat policy inside a pane host is a concept in the wrong organ, and it has to be moved out again the day Flow launches seats.
5. Authority. The committer's lock rules, identity and single-recovery rule are this system's authority. Inside Herdr, a terminal host would hold them.
6. Generality. Herdr serves every pane. A restart policy flagged "only for the committer" is one user's special case leaking into a general tool.
7. Blast radius. A bug in a Herdr patch reaches every pane and every seat. A bug in the restarter reaches one seat.
8. Deploy and backout. Herdr runs as a service under every seat. Changing it means restarting it under all of them; the restarter starts, stops and is removed alone.
9. Testing. Testing a Herdr change means building and running Herdr. The restarter is tested against a fake exit event and a fake start call.
10. Spread. The patch, once begun, reached Herdr's API, schema, terminal state, readiness, CLI and target resolution, nine partial files before a working handler. A small-looking insertion was not a small system.
11. Knowledge. The Herdr route demanded qualifying source hashes, declared objects and a reference checkout before a line was written; that work existed only because the change was inside Herdr.
12. Traceability. A fork hides this system's contract inside another's history; beside it, the contract is one readable file of ours.
13. Liability. When a restart misbehaves inside Herdr, two owners answer for one behavior. Beside it, one does.
14. What smallest measures. A twenty-line patch inside Herdr touches two owners, one foreign contract and one general tool. A forty-line restarter touches one owner and uses one contract as given. Counted in owners, concepts, authorities and contracts, the restarter is the smaller shape; counted in lines it is not. Lines are the wrong measure.

## Distillation

### Proposal 1: vision-design, new section

Target: psyche-skills, vision-design, after «No one knows ahead that the pieces are enough».

Added:

**Our abstraction is never built inside someone else's**

An abstraction of ours is built beside another's, using the contract the other gives, never by modifying the other to carry ours.

### Proposal 2: compensation-design, the measure of smallest

Target: field-skills, compensation-design, the line "Propose the smallest working shape first."

Removed: Propose the smallest working shape first.

Added: Propose the smallest working shape first. Smallest is measured in owners, concepts, authorities and contracts touched, never in lines of change; a shape that modifies another owner's abstraction is not the smallest.

## Question 1

Does "someone else's abstraction" include this system's own other tools and repositories, so that, for example, a committer concern is never patched into the messenger or the orchestrator either, but built beside them? The proposals are written as if it does.

## Question 2

A tool that offers an extension point meant for others, a hook, a plugin interface, a policy field it already exposes: is using that point building beside, as the proposals assume, or inside?

## Question 3

Field proposes the same measure for the launch skill, where interfaces of other programs are composed: "When composing another program's interface, keep our lifecycle and policy in our code; choose the smallest shape by ownership, concepts, deployment and proof obligations, never by the fewest changed lines." Does the measure land in the design skill alone, as Proposal 2 has it, or in both?
<!-- to-the-living:end -->
