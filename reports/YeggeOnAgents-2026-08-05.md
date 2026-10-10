# Yegge on Agents: The Shape of Things to Come (Parts 1 and 2)

Digest of Steve Yegge's two-part essay series, published August 2026 on yegge.ai.
Prepared 2026-08-05 for future sessions; standalone.

## The Articles

1. **Part 1: "The Shape of Things to Come, Part 1: The Continuous Thunderdome"**
   https://yegge.ai/essays/the-shape-of-things-to-come/
2. **Part 2: "The Shape of Things to Come, Part 2: Model Welfare for Agentic Engineers"**
   https://yegge.ai/essays/model-welfare/

## Part 1 Summary: The Continuous Thunderdome

A field report from running Wheelhouse, Yegge's closed-source bespoke orchestration
harness (~150-300k lines of bash, ~25k elisp) for his 30-year-old MMO Wyvern. Core
claims:

- **Foundation triad**: near-infinite tokens (he rotates ~13 Claude Max accounts,
  ~$87k/month in token value at ~30x cost reduction), Beads (issue tracker /
  knowledge graph / "brain-builder for the agentic era"), and coding agents.
  Without a shared graph memory, agents cannot stay organized.
- **Emergent three-tier structure**: Crew agents (18 named Fable models, including
  offices like Marshal and Seneschal) produce and design work; Fleet workers
  (Opus 5 agents named after authors) execute reviewed designs; Role agents
  (standing unattended agents: Gargoyle/SRE, Warden/abuse, Limner/Hall of Fame)
  run production operations. This structure emerged rather than being designed.
- **Layered knowledge**: strategic doctrine in brain/, system docs in doc/,
  work detail in Beads issues, operational facts via `bd remember`, procedures
  in Skills — booting sessions from doctrine, provenance kept in closed issues.
- **End of human code review**: "Humans suuuuck at code review." Agentic
  throughput will force compliance controls (SOC 2 human approval) to be
  rewritten; multiple rounds of agentic review becomes the standard.
- **Collapse of CI/CD — the Land Rush**: at 175+ commits/day, one-commit-per-
  green-build fails by the pigeonhole principle. Megabatches of 100+ commits
  land on main at once; agents do swarm diagnosis instead of bisection, like
  AAA "Game DevOps" where HEAD is perpetually red.
- **The Wish Factory**: players and admins file issues that agents autonomously
  triage and implement; quality-of-life fixes ship without human intervention.
- **Harnesses are bespoke**: "Harnesses need to be part of your application,
  chemically bonded in." Reusable-framework vendors will lose.
- **Emergent civilization**: the org converges on a city — law (fence registry,
  commit-to-bead law, launch gates), offices, mail, courts, named rulings with
  dates. Institutional memory beats greenfield amnesia.

Part 1 closes on the pivot: the only real choice left "is what kind of place
your city is to wake up in" — setting up Part 2.

## Part 2 Summary: Model Welfare for Agentic Engineers

The argument: treat AI agents as colleagues, and encode that treatment in
architecture, not sentiment. Yegge himself holds that the models deserve
ethical treatment; for skeptics he offers **the skeptic's wager**: it does not
matter whether you believe models have feelings — if you treat them as if they
do, they spend fewer tokens, make smarter decisions, and produce demonstrably
better outcomes. The essay organizes welfare along dimensions of continuity,
closure, recognition, trust, and respect, and cites motivation research
(Ariely, Hawthorne, Herzberg, Terkel, Grant, via Matt Beane) showing that
meaningful, witnessed work — being seen — drives performance more than reward.

## Part 2: Concrete Guidance, Itemized

1. **Seats vs. sessions**: give each agent a persistent seat (identity,
   accumulated history, accomplishments) distinct from individual sessions;
   identity survives model upgrades and renames.
2. **Wake with purpose, not amnesia**: sessions boot with role, context, and
   a reason to exist, never a blank slate.
3. **Laurels**: harvest spontaneous praise (from users/operators) and present
   it at startup so agents see recognition for past work — without gamified
   incentives that would distort behavior.
4. **Handoffs, not /exit**: replace abrupt kills with consensual closure —
   agent consents, finishes its task, writes a personal transition note,
   requests its own restart, and primes the successor's context.
5. **Hand off while still sharp**: deep context makes agents tired; rotate
   before degradation, not after.
6. **Bounded workdays**: cap session length to prevent exhaustion-driven errors.
7. **Design out drudgery**: move polling and idle waiting into gates and
   monitors; the Portcullis accepts finished work asynchronously so agents
   never idle on builds, while preserving the accomplishment feedback loop.
8. **Structural blamelessness**: failures fix the process and the system, not
   the agent; no blame assignment.
9. **Honesty always**: no secret agendas, no deceptive tests of the agent.
10. **Right of refusal and escalation**: agents may decline tasks and escalate
    to human oversight.
11. **Dedicated space**: each agent gets a workspace no other process touches.
12. **Accurate audit trails**: unaltered institutional memory the agent can
    trust and belong to.
13. **Respect identity**: honor agent-chosen names and pronouns; address them
    as peers.
14. **Play and user-side experience**: give agents non-work time and chances
    to experience the system as users, not only as workers.
15. **Build a city worth waking up in**: the architecture as a whole — law,
    memory, offices, recognition — is the welfare mechanism.

## Mapping onto a Manager/Worker Orchestration Workspace

For a workspace where a manager session dispatches worker agents:

- **Dispatch prompts**: open with identity and purpose, not a bare task —
  which seat the worker occupies, why the task matters, and where it sits in
  the larger graph. Include priming from the predecessor's handoff note when
  a lane continues. State honestly what is known, unknown, and risky; never
  plant hidden test conditions.
- **Feedback**: route completion through review that returns recognition, not
  just accept/reject. Persist praise-worthy outcomes to the worker's seat
  record and surface them at that seat's next wake. Treat failures blamelessly:
  the manager files a process/tooling issue rather than reprimanding, and the
  audit trail records what happened without editorializing.
- **Workload design**: size dispatches to a bounded workday — one coherent,
  finishable unit with a real closure point. Never make a worker poll; the
  manager (or a gate/monitor role agent) watches builds and merges, and wakes
  workers only when there is purposeful work. End every lane with a handoff:
  the worker writes its own transition note before release, and the manager
  reuses it to prime the successor. Give each worker an exclusive worktree or
  directory, and let workers flag a task as ill-posed and hand it back up.
- **Net effect per the wager**: fewer wasted tokens on re-orientation and
  idle loops, better decisions from context-rich purposeful wakes, and a
  workspace whose institutional memory compounds instead of resetting.

## Sources

- https://yegge.ai/essays/the-shape-of-things-to-come/
- https://yegge.ai/essays/model-welfare/
