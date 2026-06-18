# 138 — Take on all the router + criome-network work (session frame & method)

*The psyche, after report 137, said: "take on all the work yourself with
subagents." This meta-report directory is that session. This file is the
orchestrator's frame; numbered sub-reports hold each track's outcome; the
highest-numbered file is the synthesis.*

## Authorization & lane discipline

The psyche's directive is explicit per-task authorization for the designer
subagent protocol. Lane rules still bind: **system-designer lands code on
feature branches under `~/wt`; operator owns the merge to code-repo main.** So
every code track below commits + pushes a *feature branch* and never touches a
code repo's main. Design deliverables land as primary reports (committed to main
per the primary convention). No code-repo main is moved by this session.

## The work, from report 137 §5/§7

Two tracks at very different maturity, plus this lane's own unbuilt design, plus
a correctness bug:

| Track | What | Kind | Repo / surface |
|---|---|---|---|
| A | Clear the router transport P1 blockers + fence the offline test identity out of the production daemon path | code | `router` (+ `signal-router`), branch off `router-network-transport` |
| B | Recommend criome's cross-host wire-crypto layer (the deferred "open design slot") | design | primary report |
| C | Promote `signal-standard` from `/tmp` design (681) to a real crate that lowers green | code | new `signal-standard` repo |
| D | Fix the cross-machine quorum majority guard (`> count` → fork-safe `> n/2`) — investigate first, fix only if genuinely the 685 bug | code | `criome`, feature branch |

Deferred to **Phase 2** (depend on Track C landing `signal-standard`):

| Track | What | Depends on |
|---|---|---|
| E | The router `Attend`/`Withdraw` subscribe/fan-out surface, keyed by the `signal-standard` differentiator (134/135 design) | C |
| F | The L1 two-kernel `runNixOSTest` exercising the router transport with real criome BLS (136's ladder, rung 1) | A |

## Method

Phase 1 is a background `Workflow`: four tracks fan out in parallel, each a
pipeline. Code tracks are **build → adversarial verify** (the reviewer re-checks
out the branch, rebuilds offline, and confirms each specific fix + no
regression). Track B is a **3-advocate judge panel → synthesis**. Every code
agent works in its own `~/wt` worktree on a distinct repo (no cross-track file
collision), uses `jj` with inline `-m` only (never an editor), and pushes only
its feature branch.

Phase 2 launches after I read Phase 1's results and write the Track B report +
the Phase-1 synthesis here.

## Honesty constraints carried into the prompts

- Track D: do **not** force a "fix" if the guard is actually correct or the
  intent is ambiguous — report findings instead. A wrong fix to a quorum
  invariant is worse than none.
- Track C: create `signal-standard` **locally** (repo + crate + worktree, green
  if possible); the GitHub remote creation is an outward-facing step left for the
  psyche/operator. Do **not** yet rip the types out of `signal-criome` /
  `signal-persona` — that consumer migration is a separate, many-repo change.
- All tracks report `build_status` honestly (green / partial / red) with the
  exact command output as evidence; no green claims without a reproduced build.
