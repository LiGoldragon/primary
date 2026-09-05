# Provider fix review

## Verdict

The initial provider commit corrected the observed hands-free guard but did not
yet witness it against the packaged payload. The review update below supersedes
that provisional verdict.

## Review update — exact pushed tip `0397f5abcada`

`0397f5abcadaf812fed0ee7b50ca500d0ca16907` resolves the prior material
verification gap. Its `status-bootstrap` check extracts paired-marker-delimited
control and lock-publication expressions from the built package's `app.asar`,
executes those exact expressions in a VM with no `B8` export, and proves
Idle/Dismissed start, locked Listening stop, unlocked Listening rejection, busy
Processing rejection, Error rejection, and lock-mode publication. The
fail-closed paired-marker guard added after the earlier reported green run was
included in this review's independent remote builds.

Verdict: accepted for the stated hands-free contract. A non-blocking coverage
gap remains: Initializing, Stopping, and Retrying share the same fallback
branch but are not individually enumerated by the VM matrix.

Exact-tip verification was evaluated before building:

```
nix eval --raw .#checks.x86_64-linux.linux-patches.drvPath
# /nix/store/hvw3ryyzav46nx8d2kjlkq88943pjqwn-wispr-flow-linux-patches.drv
nix eval --raw .#checks.x86_64-linux.status-bootstrap.drvPath
# /nix/store/cnpi3fj4pw2294kg3jch9hgkx3wc07wm-wispr-flow-status-bootstrap.drv
nix build .#checks.x86_64-linux.linux-patches --no-link -L \
  --option max-jobs 0 --option fallback false --builders @/etc/nix/machines
# exit 0; remote prometheus; Bats 45/45
nix build .#checks.x86_64-linux.status-bootstrap --no-link -L \
  --option max-jobs 0 --option fallback false --builders @/etc/nix/machines
# exit 0; remote prometheus
```

## Method

Read the clean isolated worktree at
`/home/li/wt/github.com/LiGoldragon/wispr-flow-linux/acf06f-producer-integration`
at the pushed bookmark `fix/acf06f-producer-integration`, then compared the
commit with its parent. I also used the earlier static extraction of the
pinned signed installer in this flow: the state-vocabulary module exports
`_W` but not `B8`; upstream starts hands-free through `Qw`, and stops only
when `Listening && isLocked` through `US`. No application, microphone, or
production control socket was invoked.

I evaluated each check separately, then built it only on the configured remote
builder:

```
nix eval --raw .#checks.x86_64-linux.linux-patches.name
# wispr-flow-linux-patches
nix build .#checks.x86_64-linux.linux-patches --no-link -L \
  --option max-jobs 0 --option fallback false --builders @/etc/nix/machines
# exit 0; remote prometheus; Bats 45/45 passed

nix eval --raw .#checks.x86_64-linux.status-bootstrap.name
# wispr-flow-status-bootstrap
nix build .#checks.x86_64-linux.status-bootstrap --no-link -L \
  --option max-jobs 0 --option fallback false --builders @/etc/nix/machines
# exit 0; remote prometheus; built wispr-flow-1.6.774+criomos.6 and check
```

## Findings

- The control hook now uses `e === c._W.Listening && S.ZZ.isLocked`, matching
  the proven contract: Idle/Dismissed starts; only locked Listening stops;
  unlocked Listening preserves held PTT; initializing, processing, and error
  states are not toggleable. This removes the invalid `c.B8.includes(e)`
  access.
- The patch additionally publishes immediately after the exact one matched
  `S.ZZ.isLocked` mutation. This supplies the fresh mode publication required
  by bridge acknowledgement instead of relying on a later lifecycle change.
- The bridge heartbeats the current snapshot every second and clears its timer
  on close. The focused gate behaviorally observed a later recording packet
  with a greater sequence.
- `tests/signed-payload-patches.bats` does apply the complete suite to the
  real audited payload, but only checks syntax/idempotence. Its new behavioral
  test writes `status-control.js` itself and provides
  `c.B8: ["Listening", "Processing"]`. Pre-fix code therefore stops in that
  fixture; the test does not disconfirm the original production failure.
- The same fixture proves only the analogue lock-publication splice. It does
  not execute the corresponding function extracted from the signed bundle.

## Required follow-up

Replace that analogue with a VM harness which extracts the marked hook and
lock mutator from the patched signed payload, supplies only the real exported
state vocabulary plus spies for `Qw` and `US`, and exercises
Idle/Dismissed, locked/unlocked Listening, and each non-toggleable state. Run
it red against the parent before accepting it as the behavioral proof.

## Sources

- Provider tip `0397f5abcadaf812fed0ee7b50ca500d0ca16907`, compared with
  `29ff08e28a25` in the isolated worktree.
- The exact-tip checks: `nix/wispr-status-bootstrap-check.nix` and
  `scripts/patches/linux-status-bridge.sh`; the remote Nix results are recorded
  below.
- Provider commit `29ff08e28a252678f8810730cb413ba6cf68f4de`, compared with
  its parent in the isolated worktree.
- `scripts/patches/linux-status-bridge.sh`, `scripts/wispr-status-bridge.cjs`,
  `tests/signed-payload-patches.bats`, `tests/status-bridge.bats`, and
  `nix/wispr-status-bootstrap-check.nix` in that commit.
- Remote Nix outputs recorded above.
