# Commits dropped from main — 2026-09-26

Read-only forensics in `/home/li/primary` (shared jj repo, one working copy, many
flows commit and push `main` concurrently). Evidence: `jj op log` (40285 ops, 1382
today), `git reflog show refs/remotes/origin/main` (247 pushes today), revset
`(::(pushed-tips)) ~ ::main`.

## Cause — six non-fast-forward pushes of `main` today

Consecutive `origin/main` reflog entries where the earlier hash is not an ancestor
of the later one:

| time (CST) | overwritten tip | replaced by | replacing tip's first line |
|---|---|---|---|
| 07:33:17 → 07:33:28 | c0de3f08ab58 | 4f92685f7c60 | b860be: log b7da5d proposal rejection and ruling |
| 08:11:31 → 08:13:00 | 0d00399a27ee | 95677dc1a233 | b860be: embedded-model question receipt |
| 08:13:04 → 08:14:00 | 4e96d43f817b | 8077b92493c7 | b860be: 31147a piper-tts ruling receipt |
| 08:28:47 → 08:29:15 | 933022460a54 | 1ccf71c8af81 | b860be: refresh-path ruling receipts |
| 08:30:41 → 08:30:53 | 8ba165027b17 | 42df07c2a593 | e167d8: log worktree cleanup |
| 08:33:17 → 08:33:28 | 2a5c075a218f | 018beb6e21f4 | 31147a: restore Piper relays |

The mechanism is not `--allow-backwards` and not a force push. Each replacing tip
was built by `jj commit` on top of a **stale** `@` in the shared working copy, so
`jj bookmark set main -r @-` moved `main` sideways onto a branch that never
contained the intervening flow's pushed commit; the push was a legal
fast-forward from jj's point of view only because the bookmark had been re-pointed
locally first. `jj op log` shows `reconcile divergent operations` several times
today (08:34:43, 08:34:44, 08:40:38), confirming concurrent jj processes in the
one working copy. The 08:30:53 case is a same-flow duplicate: `42df07c2a593` and
the dropped `8ba165027b17` carry the identical description
`e167d8: log worktree cleanup` on different parents.

The hypothesis in the repair brief — that an e167d8 subflow's
`main = 960908c0` push around 10:00–10:30 moved main backwards — is **not
supported**. The 08:41–08:43 e167d8 sequence (`b3f3baba7`, `960908c01`,
`7c433599e`, `d7d0b20a3`, `e270d306a`, `26630d3be`) is fast-forward throughout and
appears in no non-FF pair above.

## Dropped commits (pushed to origin/main today, not ancestors of main)

| commit | description |
|---|---|
| 4e96d43f817b | b860be: log 31147a piper-tts diagnosis and ruling |
| 45208af00873 | b860be: oracle-1 and main-roles relay receipts |
| 93494fecadf8 | e167d8: log oracle answer 1 |
| d533cb692259 | e167d8: log roles vision |
| 9bec75afa4a2 | b860be: log effort-vs-intent tension |
| 933022460a54 | b860be: Luna-effort tension receipt |
| 21098ca83bde | b860be: log oracle answer delivered |
| 8ba165027b17 | e167d8: log worktree cleanup |
| d3d20f26013f | b860be: 31147a status ask receipt |
| 635e4f759d12 | e167d8: log field API and OpenCode vision |
| b8405c28e99a | b860be: field-tool/OpenCode relay receipts |
| 2a5c075a218f | b860be: provenance refined on relayed vision; psyche envelopes received |

Earlier reflog non-FF pairs (07:33, 08:11) dropped no commit that is still
absent: their content returned to main by later pushes.

## Content already present on main (no restoration owed)

- `4e96d43f817b`, `93494fecadf8`, `d533cb692259`, `8ba165027b17`,
  `2a5c075a218f` — every added line present.
- All `vision/` payload files survived byte-identical:
  `flows/b860be/vision/{fieldTool,mainRoles,openCode}.md`,
  `flows/e167d8/vision/{fieldTool,openCode,roles}.md`.

## Content still absent from main

| commit | path | missing |
|---|---|---|
| 9bec75afa4a2 | flows/b860be/log.md | 1 line (Intent/models.md effort quote + tension) |
| 933022460a54 | flows/b860be/receipts/messages-2026-09-26.md | "Luna-effort tension" block (7 lines) |
| 21098ca83bde | flows/b860be/log.md | 1 line (oracle answer 1 / main-roles envelope Transported) |
| b8405c28e99a | flows/b860be/receipts/messages-2026-09-26.md | "Psyche envelope relay to e167d8 — 09:33 UTC" block (11 lines) |
| d3d20f26013f | flows/b7da5d/log.md | 1 line (stale b7 Codex rollout; OpenCode v2 finding) |
| d3d20f26013f | flows/b7da5d/reports/refresh-handoff-2026-09-26.md | "Raw-psyche provenance correction" + "OpenCode remote access read-only finding" (8 lines) |
| 635e4f759d12 | flows/e167d8/log.md | 1 line (relayed field-API / OpenCode psyche) |

## Conflicted — not overwritten

- `45208af00873` / `flows/b7da5d/vision/mainFlowRefreshAndRoles.md`: b7da5d has
  since rewritten the file with a richer structure and four further psyche
  records. The living's verbatim quote block survived intact; only an earlier
  wording of the `Context:` sentence is gone, superseded by an equivalent
  sentence. Not restored — a restore would clobber the owner flow's newer file.
- `9bec75afa4a2` / `flows/b860be/log.md`: an append attempt produced a jj rebase
  conflict against b860be's concurrent append to the same file. The attempt was
  abandoned; nothing was pushed, `main` was left equal to `origin/main`
  (`79bf3e87da76` at that moment) and the working copy was left free of it.

## Restored by this subflow

None. The coordinator stopped restoration mid-way: b860be is repairing its own
commit chain, and no restoration for any other flow was to be pushed. The seven
(commit, path) rows under "Content still absent from main" above are the
outstanding work, each owned by the flow named in its path.

## Standing hazard

`jj bookmark set main -r @-` in a shared working copy is unsafe whenever `@` was
snapshotted before another flow advanced `main`. Landing must rebase the new
commit onto the freshly fetched `main` before setting the bookmark, and must
verify `jj diff -r main --name-only` and the conflict flag before pushing.
