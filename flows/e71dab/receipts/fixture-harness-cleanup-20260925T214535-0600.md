# Fixture harness cleanup receipt

Timestamp: 2026-09-25 21:45:35 -0600 (ouranos)

Scope examined: `app-ghostty-surface-transient-2908029.scope`.

## Verification before action

- The inventory reported 67 `fixture_harness.py` processes. At verification time,
  the transient scope contained 66 members; the historical sixty-seventh process
  was no longer present.
- `systemctl --user status <pid>` was run for every one of the 66 current member
  PIDs. Every status resolved to this same transient scope. The scope had no
  current Flow ownership: `hm-list` had no working Flow named `fixture_harness`
  or `flow-cli-poc`.
- Each member ran
  `/home/li/.nix-profile/bin/python3 /home/li/primary/tools/flow-cli-poc/fixture_harness.py`
  and had PPID 2067 (`systemd --user`). Under the corrected criterion this is
  consistent with reparented test fixtures.
- The scope was transient and active, under `app.slice`, rather than a live
  session scope. The active graphical session was `session-3.scope`; it did not
  contain these processes.
- `lsof` found zero IPv4, IPv6, or Unix socket rows for the 66 PIDs. `ss` found
  no listener or Unix socket associated with `fixture_harness.py`.

The group was therefore confirmed orphaned under the corrected criterion.

## Action and outcome

- Sent `TERM` to all 66 members through
  `systemctl --user kill --kill-who=all --signal=TERM
  app-ghostty-surface-transient-2908029.scope` at 2026-09-25 21:45:35 -0600.
- Waited exactly 10 seconds.
- Survivors at the ten-second check: 0.
- `KILL` actions: 0.
- Final scope member count: 0.

Exit state: complete. No other process, service, configuration, build, or test
was changed.

## Exact pre-action members

`2927072, 2927150, 2927308, 2927466, 2927525, 2927567, 2927661, 2927715,
2930456, 2930458, 2930498, 2930511, 2930513, 2930515, 2930547, 2930549,
2930774, 2930780, 2930829, 2930833, 2930859, 2930869, 2930878, 2930884,
2938432, 2938597, 2939193, 2939249, 2939254, 2939256, 2939262, 2939264,
2939775, 2939777, 2939803, 2939807, 2939819, 2939838, 2939845, 2939848,
2941571, 2941573, 2941581, 2941587, 2941589, 2941594, 2941618, 2941620,
2943429, 2943443, 2943461, 2943520, 2943526, 2943528, 2943530, 2943534,
2943536, 2945136, 2945145, 2945150, 2945187, 2945191, 2945193, 2945195,
2945202, 2945206`.
