# Scalar meter final review

## Verdict

Accepted. The independently checked, pushed provider tip
`033231a1255024447c6a4183c41f4ea9c1fa063f` satisfies the scalar-meter
contract under review. No counterexample was found in the packaged-payload
execution, bridge tests, or the inspected v2 source surface.

## Method

I created a disposable Jujutsu workspace at
`/home/li/wt/github.com/LiGoldragon/wispr-flow-linux/acf06f-scalar-final-review-acf06f`.
Its empty working-copy commit had parent `033231a12550`, and that commit was
also the pushed `feature/acf06f-scalar-meter@origin` bookmark. I did not edit
provider code, start the application, activate a microphone, use a production
socket, deploy, or run `bd`.

I read the full ancestry from the prior immutable review,
`0397f5abcada`, through `3119ea89` and the reviewed tip; the latter's parent
is `3119ea89f9118b8e5538734e45ab85a3e7f09bca`. I then inspected the actual
bridge, patch programs, package bootstrap witness, and relevant tests, seeking
violations of sample freshness, raw-data isolation, control/lifecycle behavior,
and socket ownership. Finally I performed syntax checks and independent Nix
evaluation/builds from the isolated exact source.

## Findings

- `publishMeter` is the sole meter mutator: it accepts only
  `{capture:"available", rms}` with finite `0..1` RMS, or an unavailable
  reset without an RMS field, and advances `microphone.sequence` only there.
  The generic heartbeat calls `publish(current)`, which preserves the nested
  sequence. The bridge witness proves invalid `Infinity` does not change either
  sequence, valid repeated `0` is fresh, and later heartbeats preserve the
  nested sequence. The documented v2 contract supports a Home consumer's
  five-second stale-RMS decay from that unchanged nested sequence; this is the
  review's inference from the stated nested-sequence and consumer-threshold
  rules, not a new status field.
- The actual packaged recorder worklet, not a substitute formula, is executed
  by the bootstrap witness with 640-sample nonconstant inputs. `[0,1]` expects
  `sqrt(0.5)`, which distinguishes RMS from mean absolute value; the further
  asymmetric, signed, non-finite, and over-range fixtures cover normalization
  and finite output. Its producer emits one meter per consumed raw transcription
  chunk (bounded to the 640-sample chunk cadence), not on a timer.
- The renderer checks the exact meter tag and scalar shape before returning
  ahead of `const t=e.data[0],a=Gm(t)`. Invalid tagged data is consumed rather
  than passed to that raw-audio handler. The main-process gate independently
  rejects bad RMS and forwards only the scalar `{capture,rms}` form to the
  bridge. Snapshot tests assert that `packet` and `samples` are absent; the
  documented v2 surface is only status fields plus `microphone`.
- The source exposes only `wispr-flow-status-v2.sock`,
  `wispr-flow-control-v2.sock`, and `com.criomos.wispr.status.v2`; the targeted
  v1/raw-surface search found no v1 runtime or socket use. The app-owned bridge
  binds private `0600` sockets, refuses a live competitor, clears its heartbeat,
  destroys incomplete control clients, closes both servers, and unlinks only
  the socket identities it owns. Those close and ownership cases are covered by
  the remote bridge gate.
- Lifecycle publication marks capture unavailable outside `Listening` and
  `Initializing`; the real lock mutator publishes the new mode. The exact
  packaged control slice is executed with the actual `_W` state vocabulary, not
  the previously invalid `c.B8` analogue: Idle/Dismissed starts, only locked
  Listening stops, and unlocked Listening plus Processing/Error reject. The
  package witness locates each paired marker exactly once and tests the tagged
  expression in a VM.

## Verification

Exact-source evaluation was run separately:

```
nix eval --raw .#checks.x86_64-linux.linux-patches.drvPath
# /nix/store/y20kc4xx2d0r196rg1jkp1s6d4qgxdgi-wispr-flow-linux-patches.drv
nix eval --raw .#checks.x86_64-linux.status-bootstrap.drvPath
# /nix/store/3rzxnd12bk8pwp8qvf3763z7mm4s2hw0-wispr-flow-status-bootstrap.drv
```

Configured-remote builds used only `prometheus`:

```
nix build .#checks.x86_64-linux.linux-patches --no-link -L \
  --option max-jobs 0 --option fallback false --builders @/etc/nix/machines
# remote prometheus; exit 0; Bats 46/46

nix build .#checks.x86_64-linux.status-bootstrap --no-link -L \
  --option max-jobs 0 --option fallback false --builders @/etc/nix/machines
# remote prometheus; terminal valid output:
# /nix/store/9wh5mzgdrxyn60r3hb3jl8ssikiydh5i-wispr-flow-status-bootstrap
```

The second command's tool stream ended during the remote package transfer, but
the original build process later exited and its expected output became valid;
that is the observed terminal result. No retry was used for this gate. Targeted
source checks also passed:

```
node --check scripts/wispr-status-bridge.cjs
node --check scripts/wispr-flow-status.cjs
bash -n scripts/patches/linux-status-bridge.sh \
  scripts/patches/linux-status-meter-worklet.sh \
  scripts/patches/linux-status-meter-renderer.sh scripts/verify-patches.sh
```

## Sources

- Pushed provider commit `033231a1255024447c6a4183c41f4ea9c1fa063f` and its
  branch ancestry from prior review `0397f5abcadaf812fed0ee7b50ca500d0ca16907`.
- `scripts/wispr-status-bridge.cjs`,
  `scripts/patches/linux-status-bridge.sh`,
  `scripts/patches/linux-status-meter-worklet.sh`, and
  `scripts/patches/linux-status-meter-renderer.sh` at the pinned tip.
- `nix/wispr-status-bootstrap-check.nix`, `tests/status-bridge.bats`, and the
  two remote Nix results above.
- `docs/reference/wispr-status-bridge.md` at the pinned tip.
