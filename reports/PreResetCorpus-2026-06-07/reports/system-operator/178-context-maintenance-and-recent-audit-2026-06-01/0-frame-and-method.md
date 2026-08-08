# Context maintenance and recent audit — frame

## Trigger

The psyche asked for two non-blocking subagents: one to do context maintenance for this session, and one to audit recent work against fresh intent and recent reports. After the subagents returned, the parent would decide which findings needed immediate attention and implement the safe fixes.

## Fresh intent captured first

Spirit record `1354` captures the durable workflow clarification: operator integration remains on main; designer work for anything new proceeds in worktrees rebased on main, reusing past work where appropriate, and continuing one design/prototype at a time around what the prototype is meant to prove.

## Current local topic

This session researched and tested browser automation choices for controlling the user's real/main Chrome profile:

- browser-use can use real-profile data only by copying the profile into a temporary controlled profile in the installed version tested here;
- the visible headed browser-use test was unreliable: the user saw `about:blank` while browser-use internally reported `Example Domain` on another target;
- the installed main-profile extension likely relevant to prior working control is Playwright Extension `mmlmfjhmonkocbjadbfplnigmagldckm`;
- Playwright Extension mode is currently the better candidate for supervised already-open main Chrome tab/session control.

Primary report for the topic: `reports/system-operator/174-browser-use-main-chrome-session-research-2026-05-31.md`.

## Method result

The first subagent run failed because the harness injected missing read files. The second produced useful reports but paused/failed during wrap-up. The parent recovered the useful outputs, consolidated them into this canonical meta-report directory, cleaned sensitive temporary browser profile copies, restored an accidental report deletion, and wrote the synthesis.
