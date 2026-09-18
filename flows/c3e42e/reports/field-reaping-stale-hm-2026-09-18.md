# Field reaping — stale Hacky Messenger registrations

Timestamp: 2026-09-18T15:11:20-06:00

## Method and authority

This bounded cleanup ran as Flow `c3e42e`. The user/root explicitly authorized
only explicit `herdr --session messaging-build` inspection while `HERDR_ENV`
was unset; no environment variable was spoofed and no focus operation was
used. Before a destructive step, the four specified registry JSON records were
read directly, `tools/hm-list` was run, and each specified pane was queried by
its exact opaque ID.

The requested deregistration boundary was then checked with:

```text
FLOW_ID=c3e42e python3 /home/li/primary/tools/hacky-messenger/hm.py deregister --help
```

It exited with usage error: `deregister` is not an installed operation; the
authoritative interface lists only `register`, `list`, `send`, and
`send-abrupt`. No raw registry-file deletion was substituted for that missing
conditional interface.

## Exact stale-record revalidation

All observations below were first recorded at 2026-09-18T15:11:20-06:00.

| Flow | Before record (exact binding) | Endpoint observation | Action / after state | Receipt grade |
| --- | --- | --- | --- | --- |
| `6034cc` | `messaging-builder-1`, `messaging-build`, `w1:p1`, `term_65bb5e98625f61`, `codex` | `pane get w1:p1` → `pane_not_found` | Refused: installed conditional `deregister` interface absent. `hm-list` immediately after still says `STALE`. | Witnessed read-only; no mutation receipt |
| `908786` | `psyche-mind-astra`, `messaging-build`, `w1:p3`, `term_65bb7f87270cb3`, `codex` | `pane get w1:p3` → `pane_not_found` | Refused: installed conditional `deregister` interface absent. `hm-list` immediately after still says `STALE`. | Witnessed read-only; no mutation receipt |
| `27fb3b` | `psyche-fable-of-b05237`, `messaging-build`, `w4:p5`, `term_65bc8382e12be26`, `claude` | `pane get w4:p5` → `pane_not_found` | Refused: installed conditional `deregister` interface absent. `hm-list` immediately after still says `STALE`. | Witnessed read-only; no mutation receipt |
| `b43670` | `psyche-opus-of-b05237`, `messaging-build`, `w4:p6`, `term_65bc8398656dd27`, `claude` | `pane get w4:p6` → `pane_not_found` | Refused: installed conditional `deregister` interface absent. `hm-list` immediately after still says `STALE`. | Witnessed read-only; no mutation receipt |

Thus all supplied identity and binding fields matched the present files, and
the exact former endpoints were absent. No successful CLI acceptance was
witnessed, so none is claimed.

## Failed candidate `64963`

At 2026-09-18T15:11:20-06:00, `messaging-build wA:p1` exists with terminal
`term_65bc6179069ce1e`; it is the sole pane of workspace `wA`, has a foreground
`zsh` process (PID `4040795`), and is at a shell prompt. Its visible terminal
history says to resume `primary Psyche opus`, not failed candidate
`64963feb-9a52-45b6-aae6-dbe5e92ac8f5`. Although the shell is idle, owner
identity therefore does not reconcile exactly. The pane and workspace were not
closed.

## Exclusions and tests

No focus, restart, reroute, archive, service/store mutation, route change,
agent interruption, workspace close, or pane close occurred. In particular,
the ready roles, `w1:pH`, `w4:p7`, `w4:p8`, active `cf3553`, field-watcher,
predecessors, and every route outside the five named candidates were preserved.

Revalidation tests were `tools/hm-list`, exact registry JSON reads, exact-pane
`herdr --session messaging-build pane get` calls, and for `wA:p1`,
`pane process-info` plus `pane read --source recent-unwrapped`. The four stale
records remain; `wA:p1` remains present.

## Commit and push

No commit or push was attempted. Before this owned report was written, `jj
status` showed unrelated pre-existing additions: `flows/4a2502/log.md` and
`flows/cf3553/vision/operational-fieldWorkersAreReapers.md`. Staging or
committing them would risk unrelated work. This report is intentionally left
uncommitted pending a clean safe boundary.

## Sources

- User/root bounded cleanup authorization, Flow `c3e42e`.
- `python3 /home/li/primary/tools/hacky-messenger/hm.py deregister --help`.
- `/home/li/primary/tools/hacky-messenger/hm.py` and
  `/home/li/primary/tools/hacky-messenger/README.md`.
- `tools/hm-list`; `~/.local/state/hacky-messenger/{6034cc,908786,27fb3b,b43670}.json`.
- `herdr --session messaging-build pane get`, `pane process-info`, and `pane read` observations recorded above.
