# Witness — renovation rollback precondition: flow 542442 is live

Method: read-only observation only. No branch was pushed, no `main` was
rewritten, no cherry-pick was committed, no repository was mutated. Merge
feasibility was tested with `git merge-tree --write-tree`, which computes a
merge result without touching refs, index, or working tree. A single
`git fetch --prune` was run against CriomOS-home `origin` to refresh
remote-tracking refs before reading live tips.

Observed at 2026-09-06 ~18:25 +0200.

## Verdict

**STOPPED before step 1.** Flow `542442`'s root session is a running process,
resumed today, holding 28 unreleased Orchestrate locks — several of them on the
exact CriomOS-home and CriomOS paths this task would rewrite. The brief's hard
precondition applies: *"If 542442 appears live, STOP and report rather than
proceeding."*

Nothing was lost by stopping, and — see below — nothing would have been lost by
proceeding either: the seven commits are **already** preserved on a pushed
remote branch.

## Evidence that 542442 is live

### Its root session is a running process

```
$ ps aux | grep -iE 'claude|codex' | grep -v grep
li  1168478  0.0  1.3 2640868 114136 pts/5  Sl+  11:59  0:01 \
    /home/li/.nix-profile/bin/codex resume 01a07275-a9f1-7d03-8662-24b542442db3
```

Identified as 542442's root by its rollout transcript:

```
$ f=/home/li/.codex/sessions/2026/09/05/rollout-2026-09-05T18-45-08-01a07275-a9f1-7d03-8662-24b542442db3.jsonl
$ grep -o 'FLOW_ID[^,"]\{0,40\}' "$f" | sort -u | head
FLOW_ID: 542442\nFLOW_DIRECTORY: /home/li/prima
...
$ grep -o 'flows/[0-9a-f]\{6\}' "$f" | sort | uniq -c | sort -rn | head
    920 flows/542442
     24 flows/4a8046
      9 flows/0062e8
```

The process was `resume`d at 11:59 today and is still attached to pts/5. There
is no Claude-side session for this flow (`~/.claude/projects/**/542442*.jsonl`
does not exist); the root is this Codex session.

### It holds 28 unreleased Orchestrate locks

`orchestrate 'Observe.Locks'` returns locks owned by `542442` including, on the
very repositories this task targets:

```
{ 898 CriomosHomeChromaGate 542442
  [ .../CriomOS-home/home-horizon-shape-542442/flake.nix
    .../CriomOS-home/home-horizon-shape-542442/flake.lock ]
  “Validate Chroma Datom Home consumer and final producer pin” }
{ 910 CriomosHomeHorizonUserContract 542442
  [ .../CriomOS-home/home-horizon-shape-542442/lib/horizon-user.nix ] ... }
{ 911 C6FinalProducerPins 542442
  [ .../CriomOS-test-cluster/datomic-horizon/flake.nix
    .../CriomOS-test-cluster/datomic-horizon/flake.lock ]
  “Repin final CriomOS and CriomOS-home consumers” }
{ 900 CriomosLojixOwnershipAssertions 542442
  [ .../CriomOS/horizon-flake-integration-542442/checks/lojix-ownership/default.nix ]
  “Update ownership assertions for final Lojix and Home pins” }
```

Lock 911 in particular declares an *intent still outstanding* to repin CriomOS
and CriomOS-home consumers.

### Its own last checkpoint declares work active and mains held

`flows/542442/log.md`, final append (2026-09-06 07:21:49 UTC):

> "Attached remote C6 session 1132 is active, with no terminal result at this
> checkpoint. CriomOS de02 and Home e717 remain frozen"

and earlier:

> "Home/OS/test-cluster mains remain held for C6; the source migration, final
> evidence and record landing remain active."

## Evidence that it is nonetheless dormant

Kept separate from the above deliberately; this is why the call is a judgment
call and not a clean read.

- No process anywhere has a cwd inside any `*542442*` worktree (scanned
  `/proc/<pid>/cwd` for every `claude`/`codex` process).
- Last file write in any 542442 worktree: **08:21 today**
  (`.../CriomOS/horizon-flake-integration-542442/.jj/working_copy/checkout`;
  `flake.nix` 08:14:40, `flake.lock` 08:14:48). ~10 h ago.
- Last append to its rollout transcript: **10:11 today**. The 11:59 `resume`
  has produced no output in 6.5 h.
- No Codex rollout file anywhere was modified after 12:00 today.
- Last primary commit touching its records: `fee2000a1`, 02:14 today.
- Two later flows have since run and landed on primary `main`: `0384e0`
  (14:32–15:44) and `db267d`, this flow (16:22–now).
- Stale locks are demonstrably normal here: `Observe.Locks` also still holds
  `{ 440 WisprAuthWitness run_wispr_live_witness ... }`,
  `{ 441 WisprEdgeProxy implement_wispr_edge_proxy ... }` and
  `{ 639 DialectSkills 6329f1 ... }` from long-finished flows. Held locks alone
  are therefore weak evidence of liveness.

The honest reading: 542442 was **abandoned mid-flight this morning**, its
terminal left open and resumed at 11:59, and the psyche then moved on to other
flows and ordered its work branched and rolled back. It is not executing. It is
resumable, and its declared state assumes Home `main` is where it left it.

## Read-only verification of the rollback plan

Done so the decision can be acted on immediately if the main flow says proceed.

### CriomOS-home `main` layout (confirms the brief exactly)

```
$ cd /git/github.com/LiGoldragon/CriomOS-home && git log --format='%h %ad %s' --date=iso -10 main
fde8a2d 2026-09-06 17:05:54 Flow db267d: read the projected machine arch field Horizon actually emits
ceeaaf4 2026-09-06 16:55:28 Flow db267d: unpack Claude Desktop native modules and self-contain the local-binary override
1ae5da8 2026-09-06 16:31:42 Remove the Claude Remote Control server
654144d 2026-09-06 03:35:39 CriomOS-home: pin current Chroma Datom producer
0808afc 2026-09-06 01:08:15 CriomOS-home: repair Horizon isolation fixtures
a464fd7 2026-09-06 00:56:18 CriomOS-home: align Horizon test fixtures
8cda3ba 2026-09-06 00:54:53 CriomOS-home: read projected machine architecture
ad20d95 2026-09-06 00:28:20 Pin corrected Orchestrate migration
4bac7ce 2026-09-06 00:22:30 Read Horizon Home gates from projected capabilities
b12e3dc 2026-09-06 00:03:32 Consume Horizon user vectors in Home
08717ef 2026-09-05 23:55:17 Pin Orchestrate framed Datom Signals
```

### The seven commits are ALREADY preserved on a pushed branch

Live remote tips:

```
$ git fetch --prune origin
$ git ls-remote origin refs/heads/main refs/heads/home-horizon-shape-542442 refs/heads/home-horizon-users-vector-542442
e71729ec6ebccce9d853227aea549712344a743c	refs/heads/home-horizon-shape-542442
ad20d954041474acc9c1453fb18957e5341c931b	refs/heads/home-horizon-users-vector-542442
fde8a2d2bf743a6d5d990f85a86263b7125593de	refs/heads/main
```

Ancestry proof against the live branch tip:

```
$ B=e71729ec6ebccce9d853227aea549712344a743c
$ for c in b12e3dc 4bac7ce ad20d95 8cda3ba a464fd7 0808afc 654144d; do
    git merge-base --is-ancestor $(git rev-parse $c) $B && echo REACHABLE $(git rev-parse $c)
  done
REACHABLE  b12e3dc4855c1266b870c7f39b1c903144544600  Consume Horizon user vectors in Home
REACHABLE  4bac7ce559926ec1a91a6fe82eca5bc522231efa  Read Horizon Home gates from projected capabilities
REACHABLE  ad20d954041474acc9c1453fb18957e5341c931b  Pin corrected Orchestrate migration
REACHABLE  8cda3bab9d497b900ccd746e7a5abaf2fa81ebab  CriomOS-home: read projected machine architecture
REACHABLE  a464fd7d88195238ad08acba2dbd5400842e19c5  CriomOS-home: align Horizon test fixtures
REACHABLE  0808afc5cb5f875fc35618816d7e9b68f5584a8a  CriomOS-home: repair Horizon isolation fixtures
REACHABLE  654144d71a51f92bba56e405faab3243e2dce4ba  CriomOS-home: pin current Chroma Datom producer
```

All seven are reachable from `origin/home-horizon-shape-542442`, which is a
pushed remote ref. **Step 1's preservation goal is already satisfied** — no new
branch is strictly required to avoid loss. A branch pinned at exactly `654144d`
would still be worth creating as an explicit, self-describing record of "the
renovation as it stood on main", since `home-horizon-shape-542442` carries more
than those seven and is 542442's own working line.

`e71729ec` — the Home revision that CriomOS `de02…` pins — is **not** on `main`;
`git branch -r --contains e71729ec` returns only
`origin/home-horizon-shape-542442`. So rolling `main` back cannot orphan the
revision 542442's CriomOS half depends on.

### Both wanted fixes replay cleanly onto `08717ef8`

File-level overlap with the renovation does exist and the "disjoint file
regions" claim was **not** accurate at file granularity:

```
$ comm -12 <renovation files 08717ef8..654144d> <files of 1ae5da8 + ceeaaf4>
flake.nix
modules/home/default.nix
```

Both overlaps come from `1ae5da8`. Tested at content granularity anyway, and
both merge clean:

```
$ BASE=08717ef8950e514c346cbdfbc69143e4369056fb
$ git merge-tree --write-tree --merge-base 1ae5da8^ $BASE 1ae5da8
58a7af4f4941192d1b157dcb2f3fb610d1e24f59      # exit 0, no conflict
$ git merge-tree --write-tree --merge-base ceeaaf4^ $BASE ceeaaf4
d67c5d7fb75beeecfee9f0de6fc21255aba12559      # exit 0, no conflict
```

And the two fixes touch mutually disjoint files, so sequential replay
(`1ae5da8` then `ceeaaf4`) is equivalent to the two independent merges tested:

```
$ comm -12 <files of 1ae5da8> <files of ceeaaf4>
(empty)
```

Touched file sets:

- `1ae5da8` — `ARCHITECTURE.md`, `UPGRADES.md`,
  `checks/claude-remote-control/default.nix` (deleted), `flake.nix`,
  `modules/home/default.nix`,
  `modules/home/profiles/min/claude-remote-control.nix` (deleted).
- `ceeaaf4` — `checks/claude-desktop-declared-cli/default.nix`,
  `checks/claude-desktop-declared-cli/claude-desktop-asar-contract.cjs`,
  `checks/claude-desktop-declared-cli/claude-desktop-runtime-contract.cjs`,
  `owned-agents/claude-desktop/asar-unpack-pattern.mjs`,
  `owned-agents/claude-desktop/default.nix`,
  `owned-agents/claude-desktop/patch-runtime.mjs`.
- `fde8a2d` (NOT to be replayed) — `modules/home/profiles/min/default.nix`, one
  line.

## Not done

Steps 1–7 of the brief were not performed. Nothing was pushed, rewritten, or
built.
