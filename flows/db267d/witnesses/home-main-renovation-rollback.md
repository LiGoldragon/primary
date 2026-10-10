# Witness — rolling CriomOS-home main back off the 542442 renovation

Method: `jj` in the two main checkouts (`/git/github.com/LiGoldragon/CriomOS-home`
and `/git/github.com/LiGoldragon/CriomOS`). Producer before consumer: Home
first, then CriomOS. Preservation branch pushed and fetched back **before** any
`main` was moved. Evaluations run with `nix eval`; the two check builds went to
the configured remote builder. No deploy, no activation, no Zeus access. Flow
542442's session, worktrees and Orchestrate locks were not touched.

Authority for the rewrite: the psyche's ruling ("put all the changes that belong
to this giant epic work onto a branch and roll back `main` to before that") and
the main flow's go decision recorded in
`flows/db267d/witnesses/renovation-rollback-precondition.md`.

Executed 2026-09-06, 18:25–18:45 +0200.

## Revisions

| | before | after |
|---|---|---|
| CriomOS-home `main` | `fde8a2d2bf743a6d5d990f85a86263b7125593de` | `ed958211e8bfaa4384aca6622d92bc9bdb429fa1` |
| CriomOS `main` | `37149c316ad1` | `bc3c4917b5df` |

Branches created and pushed on CriomOS-home `origin`:

- **`home-datom-renovation-from-main-542442`** = `654144d71a51f92bba56e405faab3243e2dce4ba`
  — the renovation exactly as it stood on `main`.
- **`main-before-rollback-db267d`** = `fde8a2d2bf743a6d5d990f85a86263b7125593de`
  — the pre-rollback `main` tip, so the force-push is fully reversible. Not
  asked for; taken as free insurance.

Untouched: `origin/home-horizon-shape-542442` (`e71729ec`),
`origin/home-horizon-users-vector-542442` (`ad20d954`), and
`origin/horizon-flake-integration-542442` on CriomOS.

## Step 1 — preservation branch, pushed and verified

```
$ jj bookmark create home-datom-renovation-from-main-542442 -r 654144d71a51f92bba56e405faab3243e2dce4ba
Created 1 bookmarks pointing to pllsxykl 654144d7 ... CriomOS-home: pin current Chroma Datom producer
$ jj git push --bookmark home-datom-renovation-from-main-542442
Changes to push to origin:
  bookmark: home-datom-renovation-from-main-542442 [add to 654144d71a51]
```

Fetched back and checked against the **live remote tip**, not local state:

```
$ git ls-remote origin refs/heads/home-datom-renovation-from-main-542442
654144d71a51f92bba56e405faab3243e2dce4ba	refs/heads/home-datom-renovation-from-main-542442
$ git fetch --prune origin
$ B=654144d71a51f92bba56e405faab3243e2dce4ba
$ for c in b12e3dc 4bac7ce ad20d95 8cda3ba a464fd7 0808afc 654144d; do
    git merge-base --is-ancestor $(git rev-parse $c) $B && echo REACHABLE ...
  done
REACHABLE  b12e3dc4855c1266b870c7f39b1c903144544600  Consume Horizon user vectors in Home
REACHABLE  4bac7ce559926ec1a91a6fe82eca5bc522231efa  Read Horizon Home gates from projected capabilities
REACHABLE  ad20d954041474acc9c1453fb18957e5341c931b  Pin corrected Orchestrate migration
REACHABLE  8cda3bab9d497b900ccd746e7a5abaf2fa81ebab  CriomOS-home: read projected machine architecture
REACHABLE  a464fd7d88195238ad08acba2dbd5400842e19c5  CriomOS-home: align Horizon test fixtures
REACHABLE  0808afc5cb5f875fc35618816d7e9b68f5584a8a  CriomOS-home: repair Horizon isolation fixtures
REACHABLE  654144d71a51f92bba56e405faab3243e2dce4ba  CriomOS-home: pin current Chroma Datom producer
```

All seven verified reachable from a pushed remote ref before `main` moved.

## Steps 2–3 — roll back and replay

`jj rebase` refused (`Commit 1ae5da86099e is immutable` — the commits are
reachable from a remote bookmark). Used `jj duplicate`, which copies rather than
rewrites and so also leaves the originals intact on
`main-before-rollback-db267d`:

```
$ jj duplicate 1ae5da86099e323cda8f79ab239ca4efaa12ce47 ceeaaf4272ea \
      --onto 08717ef8950e514c346cbdfbc69143e4369056fb
Duplicated 1ae5da86099e as uvwtxzym 08d66b81 Remove the Claude Remote Control server
Duplicated ceeaaf4272ea as qvzpkwsn 539f7059 Flow db267d: unpack Claude Desktop native modules and self-contain the local-binary override
```

Resulting chain, no conflicts:

```
539f70593f5a  parent=08d66b81dbb4  Flow db267d: unpack Claude Desktop native modules ...
08d66b81dbb4  parent=08717ef8950e  Remove the Claude Remote Control server
08717ef8950e  parent=75b6eba0d207  Pin Orchestrate framed Datom Signals
```

`fde8a2d2` (the architecture fix) was **not** replayed, as instructed.

### Separability — the earlier claim corrected

The earlier subflow reported the two fixes were separable because their file
regions were disjoint. That is **not true at file granularity**: `1ae5da8` and
the renovation both touch `flake.nix` and `modules/home/default.nix`.

```
$ comm -12 <renovation files 08717ef8..654144d> <files of 1ae5da8 + ceeaaf4>
flake.nix
modules/home/default.nix
```

Verified at content granularity instead, before touching anything, with
`git merge-tree --write-tree` (computes a merge without moving refs):

```
$ git merge-tree --write-tree --merge-base 1ae5da8^ 08717ef8 1ae5da8
58a7af4f4941192d1b157dcb2f3fb610d1e24f59      # exit 0, no conflict
$ git merge-tree --write-tree --merge-base ceeaaf4^ 08717ef8 ceeaaf4
d67c5d7fb75beeecfee9f0de6fc21255aba12559      # exit 0, no conflict
```

The two fixes touch mutually disjoint file sets, so sequential replay is
equivalent to those two independent merges.

Replayed patches compared against the originals:

```
1ae5da8 -> 08d66b81: DIFFERS
ceeaaf4  -> 539f7059: IDENTICAL patch
```

The `1ae5da8` difference is **only** the blob index lines for the two
overlapping files:

```
253c253
< index fb8a3ff..3ec3a09 100644          # flake.nix
> index f0d6f3a..242bbc1 100644
275c275
< index 0130fd0..dfc9d64 100644          # modules/home/default.nix
> index bd9fd65..36222f6 100644
```

Same six files, same add/modify/delete operations, identical hunks — the change
simply applied to the pre-renovation versions of those two files.

## Step 4 — the architecture comparison

Ground truth first. The **deployed** producer's materialized output emits the
field `arch` with an upper-case value; the renovation branch's producer emits
`architecture` with a lower-case one:

```
$ grep -o '"arch"[^,}]*' /nix/store/902py25yp2jmrihbdaszis6xb8fvfgaa-horizon.json
"arch":"Arm64"
"arch":"X86_64"
$ grep -o '"architecture"[^,}]*' /nix/store/ajs2jvi932d850gh86wy1nmxdzpwnzsa-horizon.json
"architecture":"x86_64"
```

`horizon-rs` `main` (`6f8e680`, last moved 2026-08-13) defines
`pub enum Arch { X86_64, Arm64 }` in `lib/src/species.rs`, serialized with no
`rename_all`, which is what produces `"X86_64"`.

On the rolled-back line all three sites read `"x86-64"` — right field name,
value that matches nothing:

```
modules/home/profiles/min/default.nix:240:    ++ (optionals (node.machine.arch == "x86-64") [ i7z ]);
checks/ai-agent-launch-orchestration/default.nix:25:    horizon.node.machine.arch = "x86-64";
checks/yt-dlp/default.nix:47:    horizon.node.machine.arch = "x86-64";
```

**Note for the record:** the pre-renovation consumer line read `"x86-64"`, which
the producer never emitted either. This comparison has therefore been *silently
false* on every node, for as long as it has been in this form. This change fixes
it; it does not restore prior behaviour. The two check fixtures set the same
never-matching value, so they were asserting against a shape the producer does
not emit; they are corrected with it, per "make the fixtures agree with the
producer."

Corrected to `"X86_64"` at all three sites, committed as `ed958211`:

```
modules/home/profiles/min/default.nix:240:    ++ (optionals (node.machine.arch == "X86_64") [ i7z ]);
checks/ai-agent-launch-orchestration/default.nix:25:    horizon.node.machine.arch = "X86_64";
checks/yt-dlp/default.nix:47:    horizon.node.machine.arch = "X86_64";
```

A repo-wide `grep -rn 'machine\.arch\|machine\.architecture' --include='*.nix'`
confirms these are the only three sites.

Home `main` then moved (a sideways move — `jj` required
`jj bookmark set --allow-backwards`):

```
$ jj git push --bookmark main
Changes to push to origin:
  bookmark: main [move sideways from fde8a2d2bf74 to ed958211e8bf]
$ git ls-remote origin refs/heads/main
ed958211e8bfaa4384aca6622d92bc9bdb429fa1	refs/heads/main
```

## Step 5 — CriomOS repin

`flake.nix`, `flake.lock` and `expectedHomeRevision` moved together:

```
flake.nix:36: criomos-home.url = "github:LiGoldragon/CriomOS-home/ed958211e8bfaa4384aca6622d92bc9bdb429fa1";
checks/lojix-ownership/default.nix:10: expectedHomeRevision = "ed958211e8bfaa4384aca6622d92bc9bdb429fa1";
$ nix flake update criomos-home
• Updated input 'criomos-home':
    '...fde8a2d2...' → '...ed958211...?narHash=sha256-YRuX/4DP5eI7FGWVTTMBWpTa06n6NmHhPXtdLKuJrKI='
• Updated input 'criomos-home/chroma':
    'github:LiGoldragon/chroma/c9c11a5b...' (2026-09-05)
  → 'github:LiGoldragon/chroma/1b626d9d...' (2026-08-29)
```

The `chroma` movement is renovation commit `654144d` ("pin current Chroma Datom
producer") being undone, as expected. `grep -rn fde8a2d2… --include='*.nix'`
returns nothing. The `./stubs/no-horizon` `horizon.follows` override was left
alone. `origin/horizon-flake-integration-542442` was not touched.

Committed and pushed as `bc3c4917b5df` (fast-forward from `37149c316ad1`).

## Step 6 — the lojix-ownership three-way lock state

The check requires one Orchestrate revision to hold in three places: a hardcoded
expectation, CriomOS's own lock, and Home's lock.

```
checks/lojix-ownership/default.nix:11: expectedOrchestrateRevision = "9585484738ce0748d0cf23f0431285f9693ca2ec";
:199 assert rootLock.nodes.orchestrate.locked.rev == expectedOrchestrateRevision;
:200 assert homeLock.nodes.orchestrate.locked.rev == expectedOrchestrateRevision;
```

| | before rollback | after rollback |
|---|---|---|
| expectation (hardcoded) | `9585484738ce…` | `9585484738ce…` |
| CriomOS root lock | `5f016531e765…` | `5f016531e765…` |
| Home lock | `ac8a92666f4a…` | `5f016531e765…` |

**The mismatch changed but persists.** It was a genuine three-way disagreement —
three distinct values. It is now a two-way disagreement: **root and Home agree
with each other**, and the hardcoded expectation matches neither. The rollback
resolved the producer/consumer divergence and nothing else.

The check is still red. Confirmed by evaluating it rather than reasoning about
it:

```
$ nix eval .#checks.x86_64-linux.lojix-ownership.drvPath --override-input horizon ... --show-trace
… while evaluating the condition of the assertion
  '((rootLock).nodes.orchestrate.locked.rev == expectedOrchestrateRevision)'
  at /git/github.com/LiGoldragon/CriomOS/checks/lojix-ownership/default.nix:199:1
error: string '"5f016531e765d9b679a86cc47a2d75eaca43d624"'
   is not equal to string '"9585484738ce0748d0cf23f0431285f9693ca2ec"'
```

Line 200 fails the same way. `schema-rust-source` (`f3b45631…`) matches in both
locks; `lojix` root pin `d3c0ac90…` matches; Home carries no `lojix` node.

**Cause, and it is neither the renovation nor the rollback.** Bisecting the root
lock across CriomOS history:

```
840ed01  2026-09-04  root-orchestrate=9585484738ce…  CriomOS: advance Home Wispr recovery inputs
f3d8b2c  2026-09-05  root-orchestrate=9585484738ce…  Update Home ownership pin invariant
57ec013  2026-09-05  root-orchestrate=5f016531e765…  Pin Orchestrate framed Datom Signals
a48f9cb  2026-09-06  root-orchestrate=5f016531e765…  Drop Claude Remote Control from the OS contract
```

`57ec013` (2026-09-05 23:55:17) moved the root lock to `5f016531` **without**
updating `expectedOrchestrateRevision`. That commit is flow 542442's paired
Orchestrate bump — its Home-side twin is `08717ef8` "Pin Orchestrate framed
Datom Signals" at the same 23:55:17, which is the rollback target itself. It
landed eight minutes before the renovation's first commit (`b12e3dc`, 00:03).

`57ec013` is also the CriomOS revision currently deployed to Zeus (flow 0384e0,
"Zeus on CriomOS 57ec0138, generation 207"), so `5f016531` is the Orchestrate
revision actually running. The expectation `9585484738ce` is stale against
deployed reality.

**Not repinned and not edited**, per instruction. The check is satisfiable only
by moving the expectation to `5f016531` (which would be editing a red check
green) or by repinning Orchestrate backwards to `9585484` (which would regress
the deployed line). Both were declined. This is a real, pre-existing drift that
needs a deliberate decision by whoever owns the Orchestrate pin — it is not a
consequence of this work and this work cannot legitimately close it.

## Step 7 — evaluation proofs

### The user-environment evaluation that failed this morning now succeeds

Same materialized Lojix inputs this flow used for the failing run
(`/var/lib/lojix/generated-inputs/goldragon/zeus/user-environment`), same
attribute:

```
$ G=/var/lib/lojix/generated-inputs/goldragon/zeus/user-environment
$ nix eval --no-write-lock-file --raw .#homeConfigurations.bird.activationPackage.drvPath \
    --override-input horizon "path:$G/horizon" \
    --override-input system  "path:$G/system" \
    --override-input secrets "path:$G/secrets"
/nix/store/c99v0bygd9g8dkiq7js9gf2iy7nk3a0n-home-manager-generation.drv

$ ... .#homeConfigurations.li.activationPackage.drvPath ...
/nix/store/jk3391v76mf5d514cd2mpp9fnzc5mfks-home-manager-generation.drv
```

This morning the identical evaluation died with:

```
… while evaluating the option `home-manager.users.bird.home.packages':
error: attribute 'architecture' missing
at «github:LiGoldragon/CriomOS-home/ceeaaf4272ea…»/modules/home/profiles/min/default.nix:240:20
```

Both users now evaluate to a derivation. Evaluation only — nothing was built or
activated from these.

### The claude-desktop checks are green

Built through the configured remote builder, with the same synthesized `system`
stub this flow used before (`{ outputs = _: { system = "x86_64-linux"; }; }`;
`--impure` + `NIXPKGS_ALLOW_UNFREE=1` are needed only because an unrelated
blueprint check in the same attrset pulls `unrar`):

```
$ nix build -L --impure --no-write-lock-file --override-input system "path:$S/sys-x86" \
    --no-link --print-out-paths \
    .#checks.x86_64-linux.claude-desktop-declared-cli \
    .#checks.x86_64-linux.desktop-app-support
/nix/store/4baapzl3dadjj551ynmydlf04hcn692q-claude-desktop-declared-cli-contract
/nix/store/58jjjmnzldpn6c7njwji09v6kzycambv-desktop-app-support-contract
[exited with code 0]
```

These are the **same two store paths** recorded in
`flows/db267d/witnesses/claude-desktop-asar-and-local-binary.md` before the
rollback. Identical output paths mean identical derivations: the rollback did
not perturb the claude-desktop work at all.

### The two check fixtures changed in step 4 still pass

```
$ nix build -L --impure --no-write-lock-file --override-input system "path:$S/sys-x86" \
    --no-link --print-out-paths \
    .#checks.x86_64-linux.ai-agent-launch-orchestration \
    .#checks.x86_64-linux.yt-dlp
/nix/store/j0vi5n9i2g5052ygwchcxxscnf0lgh0j-ai-agent-launch-orchestration
/nix/store/blwpyqj31avhn3yj8w8sffg4g60pm5df-yt-dlp-current-source
[exited with code 0]
```

Both fixtures now set the value the producer actually emits, and both checks
build green against the corrected consumer.

The full VM suite was not run, as instructed.

## Not done / open

- `checks/lojix-ownership` remains red on the stale `expectedOrchestrateRevision`
  (see step 6). Deliberately left failing.
- No deploy and no Zeus contact. bird's app continues to run off the previously
  deployed generation; a separate subflow owns her redeployment.
- Flow 542442's 28 Orchestrate locks were left held — they are not this flow's
  to release.
