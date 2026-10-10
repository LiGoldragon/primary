# Codex remote connection: witness report

Flow 8f0f57, 2026-10-06 ~09:50 local (CST, -06:00), host ouranos. Read-only: nothing was changed, restarted, or logged in.
Trigger: the living's words "I'm having trouble connecting remotely to Codex."

## Summary

Two of the three Codex Remote Control app-servers can no longer authenticate.
`~/.codex-next` (0.158.0-alpha.9) and the candidate `~/.codex-next-8mkkxq293hk2` (0.161.0-alpha.2) have held the same ChatGPT refresh token since the candidate home was seeded on 09-30.
Since 2026-10-05 17:08 every refresh fails with `refresh_token_reused` ("refresh token was already used. Please log out and sign in again").
Their remote-control websockets loop on HTTP 401 and never connect.
The stable `~/.codex` server (0.153.4) and the ChatGPT desktop app's app-server both share a different, healthy token, and both are connected.
All ten running Codex seat TUIs attach to the broken candidate server.

## Observations

O1. Three systemd user services run `codex app-server --remote-control`, plus a fourth app-server inside the ChatGPT desktop app. None has restarted (NRestarts=0).
`systemctl --user status 'codex*'` and `systemctl --user show ... -p Environment -p ExecStart`:
- `codex-remote-control`: codex-0.153.4, pid 1936, default CODEX_HOME `~/.codex`, socket `~/.codex/app-server-control/app-server-control.sock`, active since 09-26 16:19.
- `codex-remote-control-next`: codex-next-0.158.0-alpha.9, pid 1960, `CODEX_HOME=/home/li/.codex-next`, socket symlinked to `/tmp/codex-daemon-1001/3b2c…`, active since 09-26 16:19.
- `codex-remote-control-next-8mkkxq293hk2`: codex-next-candidate-0.161.0-alpha.2, pid 1965146, `CODEX_HOME=/home/li/.codex-next-8mkkxq293hk2`, socket symlinked to `/tmp/codex-daemon-1001/340c…`, active since 09-30 09:53.
- The ChatGPT desktop app (chatgpt-unwrapped-26.901.51231) runs its own bundled `codex ... app-server` (pid 1134433), started about 1d19h ago.
- `ss -lx` shows all three control sockets listening, so the local listeners are up.

O2. The auth files have two token lineages. Compared by digest only; no token values were printed. `jq '{auth_mode,last_refresh}'` and file mtimes:
- `~/.codex/auth.json`: chatgpt mode, last_refresh 2026-10-05T23:30:31Z, mtime 10-05 17:30. Its token differs from the next homes.
- `~/.codex-next/auth.json`: chatgpt mode, last_refresh 2026-09-25T23:13:16.104290678Z, mtime 09-25 17:13.
- `~/.codex-next-8mkkxq293hk2/auth.json`: chatgpt mode, the same last_refresh to the nanosecond, mtime 09-30 09:53 (the candidate's start time). Its refresh token is identical to `.codex-next`'s.
- No other copy of that token lineage was found (`find / -xdev -name auth.json` outside /proc, /nix and /sys).

O3. The next homes have failed auth continuously since 10-05 17:08. From `journalctl --user -u <unit>`:
- The candidate's first failure was at `2026-10-05T17:08:21 ... Failed to refresh token status=401 ... error_code: Some("refresh_token_reused")`. The service has logged 17,528 such lines.
- The next server's first failure was at `2026-10-05T17:09:12`, same error. It has logged 7,211 such lines.
- The stable server has logged 0 such lines.
- At 10-06 09:44:53, next (pid 1960) logged `failed to refresh available models: unexpected status 401 ... token_expired`.
- From 10-06 09:05, the candidate (pid 1965146) logged `failed to connect to websocket: HTTP error: 401 Unauthorized, url: wss://chatgpt.com/backend-api/codex/responses`. This is the model channel, not only remote control.

O4. Remote-control status per home, from the `logs_2.sqlite` of each home (opened read-only with python sqlite3), target `...remote_control::{websocket,auth}`:
- `~/.codex`: pid 1936 and desktop pid 1134433 each show `status changed ... next_status=Connected` at 09:45:38 and 09:44:43, with installation_id 26de4fb0, server_name ouranos, and two distinct environment ids. Pid 1936 also showed `Connection reset without closing handshake` at 09:45:36 and reconnected in about 2 s. There were 32 such WARN lines since 10-04.
- `~/.codex-next` (installation 6b0f0ff6): `remote control auth recovery failed: mode=managed, step=refresh_token: ... refresh token was already used` and then `remote control server refresh failed at https://chatgpt.com/backend-api/wham/remote/control/server/refresh: HTTP 401`. It was at reconnect_attempt 9 and still looping.
- Candidate (installation 36a617ff): identical failure, reconnect_attempt 10, and `reset ... reconnect backoff after cap reconnect_backoff_cap=30s`.

O5. Every running Codex seat uses the broken candidate server. `/proc/<pid>/environ` and args for the 10 `codex` client processes holding TCP to chatgpt.com:443 show:
- All 10 are `codex-next-candidate-0.161.0-alpha.2/bin/codex --remote unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock` with `CODEX_HOME=/home/li/.codex-next-8mkkxq293hk2`.
- Models in use: gpt-6-astra, gpt-6-luna, gpt-6.1-sol.

O6. Refresh history, from `logs_2.sqlite` with target `codex_login::auth::manager` and body "Refreshing token":
- `.codex-next`: refresh attempts by pid 1998991 on 09-25 between 16:38 and 17:13 (that is the predecessor process; the current pid 1960 started 09-26). There are no more attempts until the failing loop on 10-06.
- Candidate: only the failing attempts on 10-06.
- `.codex`: one attempt, 10-05 17:30 by pid 1936, which succeeded (the file was rewritten).
- Caveat: sqlite retention differs from the journal. The 10-05 17:08 failures appear only in the journal.

O7. Network checks:
- `curl https://chatgpt.com/backend-api/codex/models` returned `401 0.27s`. The backend is reachable; 401 is expected without a token.
- The established TCP connections to chatgpt.com [2a06:98c1:...]:443 exist.
- sshd, tailscaled and headscale are `active`.
- `tailscale status` shows ouranos at 100.64.0.2 online and the peer prometheus "offline, last seen 207d ago".

O8. `codex --version` on PATH reports `codex-cli 0.158.0-alpha.9`. This differs from both the stable server (0.153.4) and the candidate the seats use (0.161.0-alpha.2). Source-verification receipt evidence for the installed Codex version is unavailable; no protocol claim rests on it.

## Hypotheses, ranked

H1 (strong). The next and candidate homes share one single-use refresh token, and it is now spent. The fix is a fresh login in those homes.
- Evidence: O2 shows identical tokens and last_refresh, and the candidate's auth.json was written at its start (a copy). O3 and O4 show a `refresh_token_reused` loop starting about 10 days after the 09-25 refresh, consistent with the access token expiring.
- Effect: any remote client connecting to the "ouranos" servers of installation 6b0f0ff6 or 36a617ff sees them offline. The seats on the candidate also cannot reach `codex/responses` (O3, O5).
- Unknown: who spent the token first. No successful refresh in either next home was found after 09-25. A plausible path is one process refreshing in memory, or an earlier process, without persisting the result. The cause of the 17:08 trigger is not settled.
- Disconfirming checks:
  - The stable `.codex` server has a different lineage and no errors (O2, O3). This rules out an account-wide logout or ban as the sole cause.
  - Backend reachability is fine (O7). This rules out network or firewall.
  - No third copy of the token was found on disk.

H2 (moderate, depends on what "remotely" means). The remote client may be choosing a dead "ouranos" entry.
- Evidence: four app-servers enroll for remote control under the same account and the same server_name "ouranos". There are three installation ids and four environment ids (O4).
- Effect: a remote client (ChatGPT/Codex app on another device) could list several "ouranos" entries, two of them permanently offline. If the living picks one of those, the connection fails even though the stable one is connected.
- Disconfirming check needed: which entry the living's client selects. This cannot be seen from this machine.

H3 (weak). Stable remote control drops intermittently.
- Evidence: pid 1936 logs occasional `Connection reset without closing handshake`, 32 times since 10-04, each reconnecting in about 2 s (O4).
- This could cause brief hiccups, but not persistent failure.

H4 (ruled out as primary).
- The local listener, socket, systemd crash, network, tailnet and firewall all look healthy (O1, O7).
- SSH-based remote access was not reported failing and sshd is active. If the living meant SSH or the tailnet rather than Codex Remote Control, that path is not shown broken here.

## Unknowns

- The exact client and path the living uses "remotely": the ChatGPT/Codex mobile or web remote control, SSH into a Codex seat, or something else.
- Which process first consumed the shared refresh token before 10-05 17:08.
- Whether the remote client shows the dead servers or hides them.

## What would resolve it (for the living or an authorized flow, not done here)

- Sign in again (`codex login`) under `CODEX_HOME=/home/li/.codex-next-8mkkxq293hk2` and, separately, `CODEX_HOME=/home/li/.codex-next`. Give each home its own login rather than copying auth.json, then confirm that the remote-control websocket reaches `Connected`.
- Stopping the stale next server, if it is superseded by the candidate, removes one offline "ouranos" entry and one token holder.

## Sources

- systemd user journals for units codex-remote-control, codex-remote-control-next, codex-remote-control-next-8mkkxq293hk2.
- `/home/li/.codex{,-next,-next-8mkkxq293hk2}/logs_2.sqlite`, opened read-only.
- `/home/li/.codex{,-next,-next-8mkkxq293hk2}/auth.json` metadata (`auth_mode`, `last_refresh`, mtime, token digest equality only).
- `ps`, `/proc/<pid>/environ`, `ss -lx`, `ss -tnp`, `tailscale status`, `curl` status code.
- Provenance receipt: unavailable (no receipt handoff exists for this flow).
