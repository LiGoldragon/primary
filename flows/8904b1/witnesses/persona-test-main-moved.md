# Persona-test: main moved, and who made it

Read-only look, dispatched by main flow 8904b1 after Mind Sol 56ae53's
unwitnessed claim that persona-test origin main advanced to c1a2370 while
this flow's worker (lock 8200) still shows dirty at e3505bfd. Scope: the
real remote only; the worker's clone at
`/home/li/wt/github.com/LiGoldragon/persona-test/message-flow-8904b1` was
never touched, fetched into, or run against — only its lock-request text
was read from the witness file below, by pattern search.

## 1. The remote's main and every other branch

Method: `git ls-remote git@github.com:LiGoldragon/persona-test.git`
(direct query of the real remote, no local clone).

```
c1a23704537813764bf2c416544b87ec337d86d3	HEAD
c1a23704537813764bf2c416544b87ec337d86d3	refs/heads/main
```

Observation: the remote has exactly one branch, `main`, at
`c1a23704537813764bf2c416544b87ec337d86d3`. This matches Mind Sol's
"c1a2370" in full. No other branch exists on the remote.

## 2. Fresh scratch clone; commits between e3505bfd and the new main

Method: fresh clone from the real URL into this session's scratchpad
(`/tmp/claude-1001/-home-li-wt-primary-56ae53/8904b10d-7f06-4e44-9342-3a8a2d7e17bd/scratchpad/persona-test-scratch`),
never from a local path and never inside the worker's or any existing
checkout. Then `git merge-base --is-ancestor` and `git log`/`git show`
inside that scratch clone only.

`git merge-base --is-ancestor e3505bfd6732990e84f867a8850ae09ff6ae0d65 c1a2370...` succeeds:
e3505bfd is a direct ancestor of the new main, and `c1a2370...^` (the new
commit's sole parent) is `e3505bf message-flow: copy only credentials,
generate the rest of a seat's identity`. So exactly **one** commit sits
between the two revisions:

- Full revision: `c1a23704537813764bf2c416544b87ec337d86d3`
- Author: `li <li@goldragon.criome.net>`
- AuthorDate: `2026-09-27T00:21:53-06:00`
- Committer: `li <li@goldragon.criome.net>`
- CommitDate: `2026-09-27T00:25:36-06:00`
- Subject: `message-flow: pin Flow 0.17.4 and isolate Herdr`
- Body: **empty** — no trailers of any kind (no `Flow:` line, no
  `Co-Authored-By:`, no `Claude-Session:` link).
- Paths changed (`git show --stat`):
  - `README.md`
  - `flake.lock`
  - `flake.nix`
  - `lib/components/herdr.nix` (new file)
  - `lib/default.nix`
  - `packages/message-flow.nix`

For contrast, method: `git log` on the four commits at and before
e3505bfd in the same scratch clone. All four (`e3505bf`, `f7a7ab2`,
`58e263b`, `5997e2e`) carry the same author (`li
<li@goldragon.criome.net>`) but each also carries a
`Co-Authored-By: Claude ... <noreply@anthropic.com>` and a
`Claude-Session: https://claude.ai/code/session_...` trailer. c1a2370 is
the first commit in this repository's visible history with neither
trailer. Observation, not inference: the trailer pattern this repository
otherwise carries is absent from c1a2370.

## 3. What the new work does (from the diff, read in the scratch clone)

- `flake.lock` / `flake.nix`: the `flow` input's pinned revision moves
  from `9aa9bf88e3ff6f3b68864eb300ee009897162ef4` to
  `bc464e5e1b94fcc179af73111f43b69db1f69fc5` (`README.md`'s table now
  reads "Flow 0.17.4" where it read "Flow 0.16"). `message` stays pinned
  at `f1843dbaa63f38634dc10d3b28df2f4a482d6d35` ("Message 0.16"),
  unchanged.
- `lib/components/herdr.nix` (new): defines a `herdr` library component
  — the `nixpkgs` `herdr` package, its client binary path, and an
  `isolatedConfig` function that writes a generated
  `$stateRoot/herdr/config/herdr/config.toml` under a fresh
  `XDG_CONFIG_HOME`, whose `[agents] codex_executables = [...]` allowlist
  names only the one Codex executable the runner is given. This is the
  isolation: Herdr gets its own generated, single-entry allowlist and
  config home per run rather than sharing the living's own Herdr config.
- `lib/default.nix`: registers the new `herdr` component beside the
  existing `flow` and `message` ones.
- `packages/message-flow.nix`: rewritten from a skeleton runner (no
  Herdr, an `echo` placeholder where a scenario would go, and a
  credential-copying `seatCredentialEnv`) into a runner that: requires
  three externally-supplied, already-isolated Codex parameters
  (`PERSONA_TEST_CODEX_CLIENT`, `PERSONA_TEST_CODEX_HOME`,
  `PERSONA_TEST_CODEX_CONTROL_SOCKET` — the runner errors out if unset,
  and copies no credential itself); brings up an isolated Herdr session
  (`herdr session attach message-flow` under a generated `$herdrHome`)
  and asserts the generated allowlist is the one in effect; writes a
  `brief.md` fixture and its sha256; starts Flow and Message each on
  isolated state; sends Flow a real `Configure.{...}` meta request
  naming the supplied Codex endpoint and model, restarts Flow, then
  drives a real `Start.{...}` / `List.{}` / `Stop.<id>` / `List.{}`
  round-trip against Flow's ordinary client socket, asserting each
  reply's shape (`Started.*`, the row present, `Stopped.*`, the row
  showing `Stopped`); tears everything down (Message stop, Flow stop,
  Herdr server stop, killing the background `herdr session attach`
  process) on the way out.

Observation: this is not a stand-in/skeleton scenario — it is a runner
that would start real Flow and Message Nexuses, bring up a real Herdr
session, and issue live Start/List/Stop protocol messages to Flow, if
run. It does not itself perform any login: it explicitly requires its
caller to hand it an already-isolated, already-authenticated Codex
client/home/socket triple ("The supplied endpoint owns any
authentication, outside this runner" — from the diff's own comment) and
refuses to run (`:?` parameter expansion) without them. So invoking it
still needs an outside actor to supply live, authenticated Codex
material; the file alone does not embed or fetch a login.

## 4. Who made it

- Commit trailers: none. No `Flow:` line, no `Co-Authored-By:`, no
  `Claude-Session:` link — see point 2. The trailer convention this
  repository otherwise follows (Claude co-author + session link on every
  prior commit back to the repository's creation) does not name an
  author on this one.
- Author/committer identity `li <li@goldragon.criome.net>`: the human
  user's own git identity, the same one every prior commit in this
  repository (including ones plainly made through a Claude Code session,
  by their trailers) carries. It does not by itself distinguish a flow
  from the living committing directly.
- Search of Primary's flow directories (`/home/li/wt/primary/56ae53/flows/*/`,
  by pattern, never a whole-file read) for anything claiming persona-test
  or message-flow work: `grep -rl "persona-test\|message-flow"` across
  `reports/`, `witnesses/`, and `log.md` under every flow directory
  matches `893603`, `908786`, `da88cf`, `dc53b4`, `e167d8`, `857335`,
  `8904b1`, `93ba9f`. None of those hits, on inspection by further
  pattern search, names c1a2370, "pin Flow 0.17.4", or "isolate Herdr"
  except this flow's own (8904b1) log and witness/report files — i.e.
  this flow's own record of receiving and acting on Mind Sol's claim,
  and of authorizing/dispatching its own worker's implementation of the
  very same scenario. No other flow's log or report claims authorship of
  c1a2370.
- 8904b1's own log (`flows/8904b1/log.md`, lines ~2456-2477) records,
  by its own subflow's read-only search of the worker's own transcript
  record up to 06:43 UTC: the worker had made **no commit and no push**
  as of that record, and its brief forbids moving main. So the worker
  this flow hosts is, by that witness, not the source of c1a2370 either
  — though that search predates the worker's full return and cannot
  rule out a later action by it.
- Orchestrate lock listing (`Observe.Locks`, read-only; see point 6):
  the only lock naming any persona-test path is 8200, held by 8904b1
  itself (this flow), scoped to the worker's own thirteen paths in its
  own clone directory, not to the upstream repository's main branch at
  all. No lock anywhere names an act of pushing to persona-test's `main`.
- Conclusion: **unknown**. No commit trailer, no flow's log or report,
  and no Orchestrate lock names an author for c1a2370. What is
  established is only who it was *not*, by witness: not this flow's
  worker (as of its 06:43 UTC record), and not attributed to any other
  flow's own record.

## 5. Overlap with the worker's locked paths

Method: the worker's thirteen locked paths were read from two sources —
the live Orchestrate lock listing itself (`Observe.Locks`, lock 8200,
read-only) and, per the brief, a pattern search (not a whole-file read)
of the witness file
`/home/li/wt/primary/56ae53/flows/8904b1/witnesses/persona-test-worker-receipts.md`
(lines 80-99, matched via `grep -n "8200\|PersonaTestMessageFlowScenario8904b1\|lock request\|paths"`
then a bounded `Read` of lines 80-99 only). Both sources agree on the
same thirteen paths (repository-root-relative, stripping the worker's
`$W=/home/li/wt/github.com/LiGoldragon/persona-test/message-flow-8904b1`
prefix):

```
flake.nix
flake.lock
README.md
AGENTS.md
lib/default.nix
lib/components/flow.nix
lib/components/message.nix
lib/components/herdr.nix
lib/components/flow-id.nix
lib/components/claude-stand-in.nix
packages/message-flow.nix
checks/message-flow-binaries.nix
fixtures/message-flow
```

c1a2370's six changed paths (point 2), compared to this list by name:

| c1a2370 path | in worker's locked paths? |
| --- | --- |
| `README.md` | yes |
| `flake.lock` | yes |
| `flake.nix` | yes |
| `lib/components/herdr.nix` | yes |
| `lib/default.nix` | yes |
| `packages/message-flow.nix` | yes |

Observation: all six paths c1a2370 touched are among the worker's
thirteen locked paths. Every file the new main-branch commit changed is
one the worker holds a lock on. `AGENTS.md`, `lib/components/flow.nix`,
`lib/components/message.nix`, `lib/components/flow-id.nix`,
`lib/components/claude-stand-in.nix`, `checks/message-flow-binaries.nix`,
and `fixtures/message-flow` are locked by the worker but untouched by
c1a2370.

## 6. Other locks covering a persona-test path

Method: `/home/li/.nix-profile/bin/orchestrate 'Observe.Locks'`
(read-only; the one Orchestrate request this task permits).

Full listing returned 20 locks. Read by scanning each entry's path list
for `persona-test`: only one entry names any persona-test path —

```
{ 8200 PersonaTestMessageFlowScenario8904b1 8904b1
  [ 13 paths under /home/li/wt/github.com/LiGoldragon/persona-test/message-flow-8904b1/... ]
  «Write the Flow 0.17.4 live-start witness scenario in persona-test on branch message-flow-0174-8904b1» }
```

Holder: `8904b1` (this flow). Reason: as quoted. No other lock in the
listing (all 20 read) names a persona-test path, this repository, or
this scenario.

## Findings summary (plain sentences)

1. The remote's main is `c1a23704537813764bf2c416544b87ec337d86d3`,
   matching the claim's "c1a2370" exactly; it is the only branch on the
   remote. Witnessed directly (`git ls-remote`).
2. Exactly one commit separates it from `e3505bfd`: c1a2370 itself,
   authored and committed by `li <li@goldragon.criome.net>` about four
   minutes apart, with an empty body carrying none of this repository's
   usual `Co-Authored-By`/`Claude-Session` trailers, changing six files.
   Witnessed directly (fresh scratch clone, `git log`/`git show`).
3. The commit pins Flow to 0.17.4 (via `flake.lock`/`flake.nix`), adds a
   `herdr` library component that generates an isolated, single-entry
   Codex-executable allowlist and config home per run, and rewrites the
   `message-flow` runner from an inert skeleton into one that would
   really start Flow and Message, really bring up an isolated Herdr
   session, and really drive Flow's Start/List/Stop protocol — but only
   given an already-authenticated Codex endpoint supplied from outside;
   it embeds no login itself. Read directly from the diff (inference
   about "what it would do if run" flagged as such; the diff's content
   itself is witnessed).
4. Who made it is unknown by any evidence found: the commit carries no
   authorship trailer, no flow's own log or report claims it, and no
   Orchestrate lock names an act on persona-test's main. What is
   witnessed is only that this flow's own worker had made no commit and
   no push as of its last-read record (06:43 UTC) and that its brief
   forbids moving main — so the worker is not shown to be the source,
   without ruling out a later action by it that postdates that record.
5. All six paths the new commit changed are among the worker's thirteen
   locked paths — full overlap on the changed set, direct collision.
6. No lock besides the worker's own (8200) covers any persona-test path,
   by a full read of the current Orchestrate lock listing.
