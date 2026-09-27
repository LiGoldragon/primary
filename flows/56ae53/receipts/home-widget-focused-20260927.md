# Focused Home widget witness — 2026-09-27

This is an independent read of retained evidence; it did not rerun Nix or
change Home source.

## Exact focused run

- **Home source:** `f368ed706e47b61495324142e60219a518b5b8a2`
  (`Home: register solar and active network Noctalia plugins`).
- **Scope:** the combined focused build selected only
  `checks.x86_64-linux.active-network-widget` and
  `checks.x86_64-linux.solar-time-widget`, using `--impure`, frozen complete-
  host system and horizon overrides, public cache, and two jobs/cores.
- **Retained metadata:**
  `/var/tmp/flow-widget-focused-6fe957-20260927-002/metadata`, mode `0600`;
  start `2026-09-27T00:08:12-06:00`, finish `2026-09-27T00:12:05-06:00`,
  source as above, and `exit=0`.
- **Retained PTY:**
  `/var/tmp/flow-widget-focused-6fe957-20260927-002/pty.log`, mode `0600`,
  SHA-256 `dba3e9543f60cdcae302dc5d10c5bb7fda0b9b15adbe05c459fb79132618296d`.
  Its footer names and shows builds for
  `/nix/store/ifr30rrx5abr31llhxqlqgzgas8ijbn5-active-network-widget.drv` and
  `/nix/store/inp6kmwd6p3s3blsgkh8z7w9yn4qd9ns-solar-time-widget.drv`, then
  `COMMAND_EXIT_CODE="0"`.

Evidence grade: strong retained terminal, metadata, and content-hash witness
that both named focused checks realized successfully on `f368ed70`.

## Limit

This is not a full Home check.  The retained full IFD terminal on prior Home
`daf026f1e02bcd092f0ecc43b81207c96c6ec1b3` remains red, and this witness does
not test or clear `agent-daemon-configuration`, `mentci-deps`,
`cluster-relay-package`, `session-variables`, or `listener-level-widget`.
It does not establish activation readiness.
