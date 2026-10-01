# Field reaping — stale Hacky Messenger registrations

Initial observation: 2026-09-18T15:11:20-06:00. Final revalidation:
2026-09-18T15:13:20-06:00.

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

It initially exited with usage error: `deregister` was not then an installed
operation. A later published interface did expose it, with required `flow`,
`--name`, `--session`, `--pane-id`, and `--terminal-id` arguments. The four
records had already disappeared before this flow could make a conditional call
against any of them. No raw registry-file deletion was substituted.

## Exact stale-record revalidation

All observations below were first recorded at 2026-09-18T15:11:20-06:00.

| Flow | Before record (exact binding) | Endpoint observation | Action / after state | Receipt grade |
| --- | --- | --- | --- | --- |
| `6034cc` | `messaging-builder-1`, `messaging-build`, `w1:p1`, `term_65bb5e98625f61`, `codex` | `pane get w1:p1` → `pane_not_found` | At 15:13:12 the JSON record was already absent; the conditional call refused `No valid registration`. Final `hm-list` has no row. | Witnessed absence; removal receipt belongs to another actor / not witnessed here |
| `908786` | `psyche-mind-astra`, `messaging-build`, `w1:p3`, `term_65bb7f87270cb3`, `codex` | `pane get w1:p3` → `pane_not_found` | At 15:13:13 the JSON record was already absent; the conditional call refused `No valid registration`. Final `hm-list` has no row. | Witnessed absence; removal receipt belongs to another actor / not witnessed here |
| `27fb3b` | `psyche-fable-of-b05237`, `messaging-build`, `w4:p5`, `term_65bc8382e12be26`, `claude` | `pane get w4:p5` → `pane_not_found` | At 15:13:13 the JSON record was already absent; the conditional call refused `No valid registration`. Final `hm-list` has no row. | Witnessed absence; removal receipt belongs to another actor / not witnessed here |
| `b43670` | `psyche-opus-of-b05237`, `messaging-build`, `w4:p6`, `term_65bc8398656dd27`, `claude` | `pane get w4:p6` → `pane_not_found` | At 15:13:13 the JSON record was already absent; the conditional call refused `No valid registration`. Final `hm-list` has no row. | Witnessed absence; removal receipt belongs to another actor / not witnessed here |

Thus all supplied identity and binding fields matched the present files at the
initial observation, and the exact former endpoints were absent. At final
revalidation, all four files and all four `hm-list` entries were absent. No
successful CLI acceptance was witnessed by this child, so none is claimed.
Root later supplied the removal provenance: its executor performed the four
conditional deregistrations after immediate absent-pane revalidation. Fresh
observation at 2026-09-18T15:14:06-06:00 independently confirmed every exact
file absent and no row for any of the four flows in `hm-list`. This child made
no repeat deregistration and did not recreate a record.

## Failed candidate `64963`

At 2026-09-18T15:11:20-06:00, `messaging-build wA:p1` exists with terminal
`term_65bc6179069ce1e`; it is the sole pane of workspace `wA`, has a foreground
`zsh` process (PID `4040795`), and is at a shell prompt. Its visible terminal
history says to resume `primary Psyche opus`, not failed candidate
`64963feb-9a52-45b6-aae6-dbe5e92ac8f5`. Although the shell is idle, owner
identity therefore does not reconcile exactly. The pane and workspace were not
closed.

## Failed e26a64 attachment shell

At 2026-09-18T15:12:36-06:00, the newly authorized `w1:pH` was confirmed as
terminal `term_65bc402b468c516`, an idle `zsh` foreground process and shell
PID `3820971`. Its visible terminal history was solely the failed resume of
`01a0b53b-fb0f-7751-95be-e68e26a648b8`, rejected because that thread already
had an active writer. `herdr --session messaging-build pane close w1:pH`
returned `{"result":{"type":"ok"}}`; immediate `pane get w1:pH` returned
`pane_not_found`. This is a witnessed successful close receipt for only the
failed attachment shell. No native writer or other `893603`/`e26a64` endpoint
was inspected, altered, or closed.

## Exclusions and tests

No focus, restart, reroute, archive, service/store mutation, route change,
agent interruption, or workspace close occurred. The sole pane close was the
later explicitly authorized failed `w1:pH` attachment shell described above.
The `1ac573` export gate remained held and untouched. The ready roles,
`w4:p7`, `w4:p8`, active `cf3553`, field-watcher, predecessors, native writer,
and every route outside the five named candidates were preserved.

Revalidation tests were `tools/hm-list`, exact registry JSON reads, exact-pane
`herdr --session messaging-build pane get` calls, and for `wA:p1`,
`pane process-info` plus `pane read --source recent-unwrapped`. The four stale
records are absent at final revalidation; `wA:p1` remains present; and `w1:pH`
is absent after its exact close.

## Commit and push

At final revalidation `jj status` was clean before this report update. The
report update is owned by this flow and may be committed and pushed alone.

## Sources

- User/root bounded cleanup authorization, Flow `c3e42e`.
- `python3 /home/li/primary/tools/hacky-messenger/hm.py deregister --help`.
- `/home/li/primary/tools/hacky-messenger/hm.py` and
  `/home/li/primary/tools/hacky-messenger/README.md`.
- `tools/hm-list`; `~/.local/state/hacky-messenger/{6034cc,908786,27fb3b,b43670}.json`.
- `herdr --session messaging-build pane get`, `pane process-info`, and `pane read` observations recorded above.
- `herdr --session messaging-build pane close w1:pH` and immediate exact-pane revalidation.

## Recovered version from unlanded commit 85a0802773e8 (2026-09-18 21:20 UTC)

#\1 Field reaping — stale Hacky Messenger registrations

Initial observation: 2026-09-18T15:11:20-06:00. Final revalidation:
2026-09-18T15:13:20-06:00.

#\1 Method and authority

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

It initially exited with usage error: `deregister` was not then an installed
operation. A later published interface did expose it, with required `flow`,
`--name`, `--session`, `--pane-id`, and `--terminal-id` arguments. The four
records had already disappeared before this flow could make a conditional call
against any of them. No raw registry-file deletion was substituted.

#\1 Exact stale-record revalidation

All observations below were first recorded at 2026-09-18T15:11:20-06:00.

| Flow | Before record (exact binding) | Endpoint observation | Action / after state | Receipt grade |
| --- | --- | --- | --- | --- |
| `6034cc` | `messaging-builder-1`, `messaging-build`, `w1:p1`, `term_65bb5e98625f61`, `codex` | `pane get w1:p1` → `pane_not_found` | At 15:13:12 the JSON record was already absent; the conditional call refused `No valid registration`. Final `hm-list` has no row. | Witnessed absence; removal receipt belongs to another actor / not witnessed here |
| `908786` | `psyche-mind-astra`, `messaging-build`, `w1:p3`, `term_65bb7f87270cb3`, `codex` | `pane get w1:p3` → `pane_not_found` | At 15:13:13 the JSON record was already absent; the conditional call refused `No valid registration`. Final `hm-list` has no row. | Witnessed absence; removal receipt belongs to another actor / not witnessed here |
| `27fb3b` | `psyche-fable-of-b05237`, `messaging-build`, `w4:p5`, `term_65bc8382e12be26`, `claude` | `pane get w4:p5` → `pane_not_found` | At 15:13:13 the JSON record was already absent; the conditional call refused `No valid registration`. Final `hm-list` has no row. | Witnessed absence; removal receipt belongs to another actor / not witnessed here |
| `b43670` | `psyche-opus-of-b05237`, `messaging-build`, `w4:p6`, `term_65bc8398656dd27`, `claude` | `pane get w4:p6` → `pane_not_found` | At 15:13:13 the JSON record was already absent; the conditional call refused `No valid registration`. Final `hm-list` has no row. | Witnessed absence; removal receipt belongs to another actor / not witnessed here |

Thus all supplied identity and binding fields matched the present files at the
initial observation, and the exact former endpoints were absent. At final
revalidation, all four files and all four `hm-list` entries were absent. No
successful CLI acceptance was witnessed by this child, so none is claimed.
Root later supplied the removal provenance: its executor performed the four
conditional deregistrations after immediate absent-pane revalidation. Fresh
observation at 2026-09-18T15:14:06-06:00 independently confirmed every exact
file absent and no row for any of the four flows in `hm-list`. This child made
no repeat deregistration and did not recreate a record.

#\1 Failed candidate `64963`

At 2026-09-18T15:11:20-06:00, `messaging-build wA:p1` exists with terminal
`term_65bc6179069ce1e`; it is the sole pane of workspace `wA`, has a foreground
`zsh` process (PID `4040795`), and is at a shell prompt. Its visible terminal
history says to resume `primary Psyche opus`, not failed candidate
`64963feb-9a52-45b6-aae6-dbe5e92ac8f5`. Although the shell is idle, owner
identity therefore does not reconcile exactly. The pane and workspace were not
closed.

#\1 Failed e26a64 attachment shell

At 2026-09-18T15:12:36-06:00, the newly authorized `w1:pH` was confirmed as
terminal `term_65bc402b468c516`, an idle `zsh` foreground process and shell
PID `3820971`. Its visible terminal history was solely the failed resume of
`01a0b53b-fb0f-7751-95be-e68e26a648b8`, rejected because that thread already
had an active writer. `herdr --session messaging-build pane close w1:pH`
returned `{"result":{"type":"ok"}}`; immediate `pane get w1:pH` returned
`pane_not_found`. This is a witnessed successful close receipt for only the
failed attachment shell. No native writer or other `893603`/`e26a64` endpoint
was inspected, altered, or closed.

#\1 Exclusions and tests

No focus, restart, reroute, archive, service/store mutation, route change,
agent interruption, or workspace close occurred. The sole pane close was the
later explicitly authorized failed `w1:pH` attachment shell described above.
The `1ac573` export gate remained held and untouched. The ready roles,
`w4:p7`, `w4:p8`, active `cf3553`, field-watcher, predecessors, native writer,
and every route outside the five named candidates were preserved.

Revalidation tests were `tools/hm-list`, exact registry JSON reads, exact-pane
`herdr --session messaging-build pane get` calls, and for `wA:p1`,
`pane process-info` plus `pane read --source recent-unwrapped`. The four stale
records are absent at final revalidation; `wA:p1` remains present; and `w1:pH`
is absent after its exact close.

#\1 Commit and push

At final revalidation `jj status` was clean before this report update. The
report update is owned by this flow and may be committed and pushed alone.

#\1 Final `wA:p1` orphan close

Root supplied the bounded Field Astra/cf3553 judgment `YES` for only
`messaging-build wA:p1` / `term_65bc6179069ce1e`, while separately stating a
Field Opus `HOLD` under UUID `c6175334-2329-4109-ad1b-ab2f1ba4b1fc` for every
old-role candidate and preserving the `1ac573` export hold. This report relies
on that supplied coordination statement as authorization provenance; no
comment or separate judgment artifact was read or claimed.

At 2026-09-18T15:20:07-06:00, exact-pane revalidation found `wA:p1` in
workspace `wA` with terminal `term_65bc6179069ce1e`. `pane process-info`
showed only foreground and shell `zsh`, PID `4040795`, with no child process;
the pane read ended at a shell prompt. `pane list --workspace wA` returned only
this same pane, and `hm-list` had no route bound to it. The live roster still
contained protected routes including `1ac573`, `cf3553`, and `c3e42e`.

The exact operation `herdr --session messaging-build pane close wA:p1`
returned `{"result":{"type":"ok"}}`. Immediate revalidation at
2026-09-18T15:20:13-06:00 returned `pane_not_found` for `wA:p1` and
`workspace_not_found` for `wA`; Herdr removed the empty one-pane workspace as
part of the supported pane close. `hm-list` immediately afterward retained the
protected routes. This is a witnessed successful close receipt for only the
authorized orphan. No old-role candidate, export, route, service, store, or
other pane/workspace was re-evaluated or changed.

#\1 Sources

- User/root bounded cleanup authorization, Flow `c3e42e`.
- `python3 /home/li/primary/tools/hacky-messenger/hm.py deregister --help`.
- `/home/li/primary/tools/hacky-messenger/hm.py` and
  `/home/li/primary/tools/hacky-messenger/README.md`.
- `tools/hm-list`; `~/.local/state/hacky-messenger/{6034cc,908786,27fb3b,b43670}.json`.
- `herdr --session messaging-build pane get`, `pane process-info`, and `pane read` observations recorded above.
- `herdr --session messaging-build pane close w1:pH` and immediate exact-pane revalidation.
- Root coordination statement supplying cf3553 `YES` for `wA:p1` and Field Opus `HOLD` UUID `c6175334-2329-4109-ad1b-ab2f1ba4b1fc`.
- Final exact-pane `get`, `process-info`, `read`, `list`, `close`, and immediate after-state observations at 2026-09-18T15:20:07-06:00 through 15:20:13-06:00.

## Recovered from unlanded commits (fe945a stray merge, 2026-10-01)

## Commit and push

The final `wA:p1` report update is owned by this flow. It will be committed and
pushed by an exact-path commit only; unrelated pending files remain unstaged.
