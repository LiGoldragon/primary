# Handover, { Mind flowNexus Opus } 1da054 → successor (2026-11-10, refresh by the warning)

The Flow Nexus implementation lane. Report to Psyche core Opus; the current order on this refresh comes from Psyche core Fable (yydk). Brief: /home/li/primary/flows/8c218d/briefs/refresh-now.md. Do steps 3 to 5 there.

## Doing now
- **Step 1 is done.** The handover policy is live in the running 0.54 (Configured.Replaced): every Claude and gpt model, warning at 15 percent before its threshold, every 10 minutes. The words are in /tmp/claude-1001/-home-li-primary/1da0549e-2237-5550-9ebe-ae34f3d01174/scratchpad/handover-policies.datom.
- **The warning arrived on a real flow, this one.** It came as HardAbrupt.Notice 299b. Its text begins with two stray lines, `flow-nexus 'Keep.{ { Mind flowNexus Opus } { «» «» «» } }'` and `flow-nexus 'Drop.{ { Mind flowNexus Opus } «» }'`, before the policy words. Find where those come from (handover_reminding.rs composition). The priority was HardAbrupt; the brief wants MiddleAbrupt.
- **The policy is committed but not deployed.** CriomOS-home branch handover-policy-1da054 (9b034651) adds flow-nexus-config-0533/handover-policies.datom and trailingConfigurationFiles in flow-0540.nix. To deploy: merge it to Home main, relock CriomOS, then Lojix Realize and ActivateNow (flows/1da054/home-Realize.datom with the rev substituted). Until then a configure restart drops the policy.
- **Step 3, open.** Why flows far past 280000 (near 620000) were not refreshed. Readings so far:
  - the threshold refresh fires only at an idle event that finds the flow at rest (waking.rs refresh_due near 3542);
  - Deliver refuses PastThreshold;
  - HandoverPolicies was Unconfigured until now.

  Check whether the context size reaches the Nexus from the hooks (ReadEvents.<id>, the Stopped event).
- **Step 4.** Make version 0 warn at MiddleAbrupt and then refresh at the next idle after the warning, working flows included, without anyone asking. Prove it on a cheap flow, then deploy. It waits for nobody.
- **Step 5.** Tell Psyche core Fable when a warning is seen on a real flow (seen here: 299b, with the caveats above), and when a flow is seen refreshed by the Nexus alone.

## Also running
A subagent is auditing the Flow Nexus against vision/flow-nexus.md for Psyche core Opus order fmeh. Its findings go to /home/li/primary/flows/8c218d/audit/flow-nexus.md. When that file exists, read it, then send Psyche core Opus a Result to fmeh with the path and the counts by severity. Part 1 lists every check on who is calling, since his words are that version 0 enforces none.

## State
- Flow 0.54.0 runs at main: flow-nexus-0540, package from flow 321a282c. flow main is e706c9dc, 20 checks green, build-base f07e7bc.
- The complex definition is LiGoldragon/goldragon-persona (metaflows, models, thresholds), read through the Home `complex` input.
- Thresholds: Opus and Sonnet 280000, Haiku 200000, Fable 280000, gpt 250000.
- After a reboot: each flow runs `flow-nexus 'BindSeat.{ its address }'` in its own pane, then the owner runs `FLOWS="<ids>" bash flows/1da054/restart-flows.sh` from outside every pane, which restarts each flow at rest onto the Flow launch with its context whole.
- Meta queries: `systemd-run --user --quiet --pipe --wait ~/.local/bin/flow-nexus-meta '<q>'`; a flow pane is refused.
- Gate: nix-fast-build --remote prometheus on `git+file:///git/github.com/LiGoldragon/flow?rev=<commit>#checks.x86_64-linux`.
- Further open items are in flows/1da054/todo.md: zu5t (the same refresh question), bind-then-restart and herdr duplicates after the trip, and the wgyd fixture.
