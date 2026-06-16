# 669 — First e2e (offline full-chain): frame and method

The psyche opened the e2e-production phase, then resolved the two gating forks (report 668):

- **D1 — "vcs" = the mirror as spirit's version-control remote** (not git/Gitolite). spirit ships its
  versioned sema commit log (suffix + checkpoint) to the mirror; the mirror keeps its own versioned
  store and serves `Restore`.
- **D2 — finalize the OFFLINE full-chain e2e first** (stubbed crypto), per *"let's not worry about
  key encryption for now."* The live/gated cross-node tailnet bed is the second milestone.

Milestone intent: Spirit `d6he` (Decision, High) — [the first end-to-end production milestone is the
spirit → vcs → criome → router → mirror chain … finalize this full chain as the first real
multi-component e2e production deployment, with many designer lanes developing the parts in parallel].

## What the grounding (668) already established

- spirit healthy (0.13.0); versioned object model present (`versioned_log`/`checkpoint`/`import`).
- A complete tested `MirrorShipper` exists on `origin/store-decomposition`/`vc-followups`, dropped
  from main by merge `d2cf86f` (added by `a7b7d95`); re-land + pin reconcile, not from-scratch.
- mirror is a green commit-log VC (loopback ship+restore e2e); router milestone-1 (contract, pushed,
  green) + milestone-2 (networked forwarding daemon + passing two-router loopback e2e) are done on
  `router-network-transport`; §5 option (A) `RegisterActor.home` already taken.
- criome real BLS + admission gate green on the local `criome-auth-pilot` worktree (unpushed);
  signal-criome admission contract pushed. criome + router daemons deployed **nowhere**.
- Open: Tailscale (`0.0.0.0:7474`, deployed) vs Yggdrasil (`200::/7`, design docs) for the live bind.

## Method — four parallel designer slices

Prime-designer fan-out (the psyche asked for "many designers"). One BUILD slice on the critical path
plus three DESIGN slices that tee up the harness and the live track:

| # | Slice | Kind | Deliverable |
|---|---|---|---|
| 1 | **P1 — re-land the spirit→mirror shipper** | build | a spirit feature branch in `~/wt` with the dropped `MirrorShipper` re-landed against current main, pins reconciled, gated off-by-default, `tests/mirror_shipper.rs` green; report `669/1` |
| 2 | **P5 — offline full-chain e2e harness design** | design | blueprint composing spirit-ship → mirror A → router forward → mirror B restore into one offline harness + its assertions (the impl follows P1); report `669/2` |
| 3 | **criome integration + provisioning ceremony** | design | operator main-integration sequence + the cluster-root provisioning-ceremony design (for the live track); report `669/3` |
| 4 | **router m3 + deploy/interface plan** | design | router m3 (real criome attestation + replay/freshness window) spec + the deploy plan resolving Tailscale-vs-Yggdrasil and the two-node bed; report `669/4` |

Slices 1–2 finalize the offline first e2e (the priority green); slices 3–4 develop the live/gated
track in parallel so it's build-ready when the offline e2e lands. Synthesis is the highest-numbered
file in this directory; designers prepare feature branches (operator integrates to code-repo main).
