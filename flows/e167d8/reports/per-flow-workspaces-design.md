# Safe landing on primary: field-clj `#commit`, per-flow workspaces, Field Nexus

Design subflow of Psyche Opus e167d8, 2026-09-26. Proposal only: no skill,
launcher, or field-clj source was edited. field-clj belongs to Mind Sol a676b3;
section 3 is the spec for a676b3. Skill text in section 7 awaits the living's
approval.

## 1. Problem

Every flow writes the one jj working copy `/home/li/primary`. Today's
forensics (`flows/e167d8/reports/main-dropped-commits-2026-09-26.md`): six
non-fast-forward moves of `origin/main`, twelve pushed commits dropped. Each
replacing tip was a `jj commit` on a stale `@` in the shared copy, then
`jj bookmark set main -r @-`; `jj op log` shows `reconcile divergent
operations` from concurrent jj processes. Other losses today: pathless
commits sweeping others' edits, `jj new` / checkout dropping uncommitted
receipts, a workspace-forget through a nested git worktree removing the
default working-copy commit. At the time of writing the default `@` change id
`untxslqo` was itself divergent (two visible commits).

## 2. Psyche on record

> Well I thought we wanted to make the field tool do the committing the right way so that this problem doesn't happen. Can we do that?

-- the living, 2026-09-26, relayed by e167d8.

> Well if the CLJ tool is going to have a database (all our CLJ tool has the [Datalevin] database), then it would have a lock in the database so it would know.

-- psyche, STT, 2026-09-26, `flows/e167d8/vision/landing.md`.

> We need that field tool, either Field Nexus or the Field CLJ, whichever is most ready, to be able to interact with all of the system

-- psyche, typed, 2026-09-26, `flows/e167d8/vision/fieldTool.md`.

Earlier, still standing: "you all just need to go back onto one shared primary
for now and use the Orchestrate tool to lock files"
(`flows/9993b5/vision/oneSharedPrimary.md`, 2026-09-17) and "from henceforth
we launch all the primary flows directly on main"
(`flows/9993b5/vision/launchOnMain.md`). Today the living also said jj
workspaces of the one repo are fine, while only one clone may exist on disk.

Tension to surface, not resolve: per-flow workspaces (section 5) depart from
"one shared primary" of 09-17. The safe `#commit` below keeps that shared
primary and makes it safe, so it fits both records; per-flow workspaces need
the living's word to supersede 09-17.

## 3. field-clj `#commit` today, and the gaps

Source: `/git/github.com/LiGoldragon/field-clj`, main `a2c278d3`. Deployment:
packaged in CriomOS-home (`modules/home/profiles/med/cli-tools.nix:51`), but
`field-clj` is not on PATH on ouranos; the smoke runs recorded in
`flows/b7da5d/log.md:98` and `flows/e167d8/log.md:156` ran a built copy.

What it does (`src/field_clj/commit.clj:108-141` steps, `src/field_clj/jj.clj`
traits): `jj root` in the caller's directory; resolve push URL, refusing a
local/mirror URL; read local main; `jj diff --name-only` must contain every
named path; mark `jj op log -n1`; `jj commit -m <msg+Flow trailer>
root-file:"<path>"...`; `jj diff -r @- --name-only` must equal the set;
`jj bookmark set main -r <commit>`; `jj git push --remote <r> --bookmark
main`; `git ls-remote <url> refs/heads/main` must equal the commit. On any
refusal after the mark it runs `jj op restore <mark>`.

What is already right: exact filesets (`jj.clj:24-29`) so a directory or
pattern never widens the set; the scope check; the `Flow:` trailer; the
real-remote verification with `ls-remote`; typed `#success`/`#refused`.

Gaps:

- G1 `jj.clj:52` (`admit`), and every later jj call: runs in the caller's
  working copy, so each call snapshots the shared `/home/li/primary`. Two jj
  processes snapshotting the one copy is the source of "Concurrent checkout",
  divergent `@`, and `reconcile divergent operations`.
- G2 `jj.clj:73` (`commit`): the commit's parent is the shared copy's `@-`,
  never freshly fetched main. No `jj git fetch` exists anywhere in `src/`.
  This is exactly the stale-`@` mechanism behind today's six non-FF moves.
- G3 `jj.clj:59-60` (`confirm` ignores its `_commit` argument and reads
  `@-`) and `jj.clj:76` (commit id read back from `@-`): a concurrent jj
  process that moves `@` makes both read the wrong commit.
- G4 `jj.clj:96-97` (`advance`): `bookmark set` without `-B` refuses a
  backwards or sideways move only relative to the local view of main; there
  is no check that the commit descends from the real remote's main.
- G5 `jj.clj:99-100` (`publish`) and `commit.clj:137-139`: when the remote
  moved, jj's lease refuses the push and the pipeline ends. No fetch, rebase,
  or bounded retry.
- G6 `commit.clj:69-75` with `jj.clj:78-80` (`restore`): `jj op restore` is
  repository-wide. It undoes every other flow's jj operation since the mark
  (their commits, bookmark moves, snapshots) and re-checks-out the working
  copy to the restored `@`, which can drop other flows' uncommitted edits
  snapshotted in between. This is a loss path of its own and must go.
- G7 `commit.clj:108-141`: no serialization. Two `#commit` runs interleave
  freely.
- G8 `jj.clj:109-112` (`verify`): equality with the new commit only; it does
  not record that the pre-push remote main is an ancestor of the new main.

## 4. Spec for a676b3: `#commit` that lands safely

Input and output keep their shape: `FLOW_ID=<id> field-clj '#commit
["message" ["path" ...]]'` → `#success [flow commit [path ...] :main :pushed
:present]` or `#refused #<stage> [...]`.

Required behaviour:

1. Never snapshot, check out, or restore the caller's working copy. Every jj
   call against the caller's workspace uses `--ignore-working-copy` and only
   reads: `jj --ignore-working-copy root`, and the base content
   `jj --ignore-working-copy file show -r @- <path>` for each named path.
   The named paths' new bytes are read from disk directly.
2. Build the commit in a landing workspace that field-clj owns: one jj
   workspace of the same repository per repo, e.g.
   `/home/li/wt/primary/field-land`, name `field-land`, created once with
   `jj workspace add`. No flow works there.
3. Serialize with the Datalevin landing lock (section 4a), acquired before
   step 4 and released after step 9, per repository.
4. In the landing workspace: `jj git fetch --remote origin --branch main`;
   `R0 = main@origin`; `git ls-remote <real-url> refs/heads/main` must equal
   R0, else `#refused #remote [...]`. `jj new R0`.
5. For each named path, with base B (step 1), ours O (disk), theirs T (at
   R0): T = B → write O; T = O → nothing to write; otherwise three-way merge
   (`git merge-file -p O B T`); a merge conflict refuses `#conflict [paths]`.
   O = B for a path refuses `#clean [path]` (today's clean-path refusal).
   A missing O is a deletion.
6. `jj commit -m <message + Flow trailer> root-file:"<path>"...`; read the
   new commit id C by `jj log -r @- ` in the landing workspace (field-clj is
   the only process there); confirm `jj diff -r C --name-only` equals the
   named set (fixes G3).
7. Require `R0` to be C's only parent. `jj bookmark set main -r C` (never
   `-B`). `jj git push --remote origin --bookmark main`.
8. When the push is refused because the remote moved: `jj git fetch`,
   `jj rebase -r C -d main@origin`; a conflicted C refuses `#conflict`;
   retry step 7 at most 3 times with 1-3 s jitter, then `#refused
   #race-exhausted [...]`.
9. Verify: `git ls-remote <real-url>` equals C, and the R0 of the final
   attempt is an ancestor of C. Release the lock.

Refusal cleanup touches only what this run created: `jj abandon C` in the
landing workspace; if local main equals C and the remote does not, set main
back to `main@origin` (a compare-and-set on the tool's own unpushed move, the
only backwards move allowed). Never `jj op restore` (fixes G6).

Optional `#sync []`: under the same lock, in the caller's workspace,
`jj rebase -b @ -d main` so the landed paths stop showing as modified; refuses
when the rebased `@` has conflicts, and restores nothing. It is the only
operation that snapshots the caller's copy, and runs only when the caller asks.

### 4a. The landing lock in Datalevin

field-clj has no store today: `deps.edn` carries only `metosin/malli`.
messenger-clj opens Datalevin through the babashka pod
(`messenger-clj/src/messenger_clj/typed_store.clj:12-13,108-116`); field-clj
is JVM Clojure built by clj-build, so it takes `datalevin/datalevin` as a
Maven dependency. Store: `$XDG_STATE_HOME/field-clj/datalevin`, one per host.

Datalevin sits on LMDB, which admits one write transaction at a time across
all processes that open the same environment, so a read-then-write inside one
write transaction is atomic between field-clj processes. Unverified here:
that the chosen Datalevin API (`with-transaction`, or a `:db/cas` datom)
holds that guarantee across two JVMs; a676b3's test must race two processes
on one lock and show exactly one acquire.

Records:

    {:land-lock/repo       "<absolute git common dir>"   ; :db.unique/identity
     :land-lock/holder     "<FLOW_ID>"
     :land-lock/token      #uuid "..."
     :land-lock/host       "ouranos"
     :land-lock/pid        12345
     :land-lock/acquired   #inst "..."
     :land-lock/expires    #inst "..."}                 ; acquired + 120 s

    {:landing/id :landing/flow :landing/paths :landing/base-remote
     :landing/commit :landing/final-remote :landing/outcome :landing/at}

Acquire: in one write transaction, read the repo's lock; free, expired, or
held by a dead pid on this host → write holder, token, expiry; otherwise
report the holder. Wait by polling up to 60 s, then `#refused #busy [holder
acquired]`. Renew `expires` every 30 s while landing. Release: retract the
lock only when its token is ours. Breaking a stale lock writes a
`:landing/outcome :broke-stale-lock` record naming the old holder. Every
landing appends a `:landing` record: the history of who landed what.

The lock binds only landings that go through field-clj. A manual
`jj git push` bypasses it; jj's push lease and step 9 still keep the remote
from moving backwards.

## 5. Per-flow workspaces: needed?

Once section 4 is live and flows land only through it, they are not needed to
stop commit loss: field-clj never snapshots, commits in, or restores the
shared copy, and every landing is a serialized fast-forward. What remains in
the shared copy is flows running other writing jj commands there (`jj new`,
pathless `jj commit`, `jj workspace forget`), and reads that snapshot it.
Section 7's rule closes that: in `/home/li/primary`, no jj command writes
except through field-clj, and reads use `--ignore-working-copy`.

They stay useful as isolation for a flow doing long or conflicting edits in
shared files. If adopted, the shape witnessed here:

- One workspace per writing main flow: `jj workspace add
  /home/li/wt/primary/<seat>-of-<ancestor> --name <same> -r main`, created by
  the launcher before launch (the FLOW_ID is claimed after launch, so the
  name comes from the seat). Subflows inherit the main flow's cwd and never
  get their own. `native-seat-launch.mjs` already takes `--cwd`
  (`tools/native-seat-launch.mjs:18`) and passes it to Codex `thread/start`
  and `skills/list` (lines 382, 431, 439); Claude takes the pane's cwd.
- CLAUDE.md, AGENTS.md, `.claude/skills` (72 files), `.codex`, `.agents` are
  tracked, so they appear in every workspace at checkout. Witnessed: the
  e167d8 workspace holds all of them.
- Other flows' records are read from the shared store:
  `jj --ignore-working-copy file show -r main <path>`, or `jj git fetch` then
  `jj rebase -b @ -d main` in one's own workspace.
- Landing is the same `#commit`; `#sync` keeps the workspace current.
- Ending: `jj workspace forget <name>` run from `/home/li/primary`, naming the
  workspace explicitly, then remove its directory. Never forget from inside a
  nested git worktree.

Costs, all witnessed or read: 291 MB per workspace checkout; no `.git` in a
secondary workspace (tools that look for `.git` — Codex project-root markers,
raw git — see none; `jj git root` still works); untracked `repos/`,
`private-repos/`, and the Beads database are absent unless linked; Claude
transcripts land under a per-cwd project directory
(`~/.claude/projects/-home-li-wt-primary-<name>`); `native-seat-launch.mjs`
claims FLOW_IDs under `<cwd>/flows` (lines 442, 461, 484, 502), so two
workspaces could claim the same id unless the claim root stays
`/home/li/primary/flows` (the profile guard at lines 88-90 allows only a
relative root or the authorized Field root).

## 6. Field Nexus, facts only

- No `field-nexus`, `signal-field`, or `meta-signal-field` repo, binary, unit,
  or socket exists. Running nexuses: `flow-nexus.service`,
  `orchestrate-nexus.service`.
- `flows/1ac573/reports/field-nexus-concept.md`: concept only, "Nothing
  implemented, nothing deployed": ordinary and meta sockets, a typed Sema
  store, subscriptions.
- `/git/github.com/LiGoldragon/field`: read-only JS inventory scripts and a
  timer; no request types, no commit vocabulary.
- A Land in a Field Nexus would be a typed `Land` request on the ordinary
  socket, answered `Landed` or a typed refusal; the one long-running process
  serializes landings per repo by construction, with no lock records.
  Everything else in section 4 (landing workspace, fetch, three-way, FF-only
  push, retry, verify) is the same work in either home.
- field-clj: exists, typed commit vocabulary, 34 tests / 167 assertions
  passed (`flows/b860be/log.md:30`), packaged, not on PATH; section 4 is a
  change to its existing pipeline plus a new Datalevin dependency.

## 7. Proposed skill and entry-file text (for approval)

`file-editing` (Curriculum `skills/file-editing.md`): replace from "The
sequence for landing work:" through the `FLOW_ID=<id> field-clj '#commit ...`
paragraph with:

    Land every change with
    `FLOW_ID=<id> field-clj '#commit ["message" ["path" ...]]'`,
    naming exactly the files this flow edited. It commits them onto freshly
    fetched `main` in its own landing workspace, pushes a fast-forward, and
    confirms it on the real remote; it never snapshots or changes your working
    copy. On `#refused #conflict`, bring your edits onto current `main` and
    land again; report any other refusal.

    In `/home/li/primary` run no jj command that writes; read with
    `jj --ignore-working-copy`.

Preserves: path-only commits, Flow trailer, real-remote check. Removes: the
manual `jj commit` / `bookmark set` / `push` sequence, which is today's loss
path. Until section 4 is deployed the manual sequence must stay, amended to
fetch first:

    jj git fetch
    jj commit -m 'message' path ...
    jj rebase -s @- -d main@origin
    jj bookmark set main -r @-
    jj git push --bookmark main

`testing-commit-scope`: replace `jj diff -r @- --name-only` with
`jj diff -r <commit> --name-only`, `<commit>` being the id `#success`
returned. `@-` moves under concurrent jj runs.

`CLAUDE.md` "Committing" and `NON_MANAGEMENT_AGENTS.md` "Leave no uncommitted
changes behind" both say to commit dirty changes found in the tree first. In
a shared tree that line sweeps other flows' in-progress edits. Replace with:

    Land what you edited before going idle. Dirty paths you did not edit
    belong to the flows editing them; leave them.

`subflow`, `main-flow`, `refresh`: no change needed for section 4. Only if
section 5 is adopted, `refresh` gains, after "Each launch profile declares
...":

    Launch each main seat with `--cwd` at its own jj workspace
    `/home/li/wt/primary/<seat>-of-<ancestor>`, added from `/home/li/primary`;
    FLOW_IDs are still claimed under `/home/li/primary/flows`.

and `subflow` gains nothing: a subflow inherits its main flow's cwd.

## 8. Migration

1. a676b3 implements section 4 with a two-process lock race test and a
   concurrent-landing test on a scratch repo; deploy field-clj onto PATH.
2. The living approves section 7; skills regenerate from Curriculum.
3. Existing flows switch at their next landing; nothing else is moved.
4. The default `@` is brought current once, by `#sync`, under the lock.
5. Per-flow workspaces only on the living's word (section 2 tension).

## 9. Prototype evidence

Workspace `e167d8` at `/home/li/wt/primary/e167d8` (added from
`/home/li/primary` with `--ignore-working-copy`, then `jj new main@origin`
inside it). Land by path: `jj git fetch`; `jj rebase -b @ -d main@origin`;
`jj commit -m 'e167d8: per-flow workspace land-by-path probe'
flows/e167d8/reports/per-flow-workspace-probe.md`; `jj diff -r @- --name-only`
returned only that path; `main@origin` 0c733174 was its ancestor;
`jj bookmark set main -r @-`; push reported "move forward from 0c7331746cf3
to 02153ee6972f"; `git ls-remote git@github.com:LiGoldragon/primary.git`
returned `02153ee6972f4b17b8c71a5503dee4e1ba2a4d29`. The default working
copy's dirty set (`flows/b7da5d/log.md`, `flows/e167d8/log.md`,
`flows/e167d8/vision/landing.md`) was identical before and after.
