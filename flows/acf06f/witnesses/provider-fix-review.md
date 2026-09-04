# Provider fix review

## Verdict

`29ff08e28a252678f8810730cb413ba6cf68f4de` corrects the observed
hands-free control guard and packages successfully. Its behavior claim is not
fully witnessed: the added test called `signed-payload control hook` executes
a hand-authored analogue, not the signed payload, and its analogue defines the
previously absent `c.B8`. It therefore cannot have been the required red
witness for the real-payload failure. The production change is suitable for
integration after that test is made payload-derived and seen red once.

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

- Provider commit `29ff08e28a252678f8810730cb413ba6cf68f4de`, compared with
  its parent in the isolated worktree.
- `scripts/patches/linux-status-bridge.sh`, `scripts/wispr-status-bridge.cjs`,
  `tests/signed-payload-patches.bats`, `tests/status-bridge.bats`, and
  `nix/wispr-status-bootstrap-check.nix` in that commit.
- Remote Nix outputs recorded above.
