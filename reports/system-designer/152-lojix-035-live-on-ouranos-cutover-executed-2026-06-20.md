# lojix 0.3.5 live on ouranos — cutover executed

System-designer, ouranos, 2026-06-20. Executes the plan in report 151. Outcome:
**lojix 0.3.5 is live on ouranos**, daemon serving on a fresh layout-5 store, zero
failed units.

## Final live state

- `current-system` = `dcn80c1r…-nixos-system-ouranos` (generation 126).
- `lojix-daemon` = **lojix-0.3.5**, active, NRestarts=0 since 10:04:47, both sockets
  bound (`/run/lojix/ordinary.sock`, `/run/lojix/owner.sock`).
- `mirror`, `repository-ledger` active on fresh layout-5 stores.
- `/etc/criomOS/complex/publication.nota` written:
  `(ouranos [ssh-ed25519 …root@ouranos] None None)`.
- 0 failed units.

## What it took (the full chain)

1. **Rust → nightly** across the whole closure (fenix `complete`, no per-crate
   rolling-stable hash). The last hidden snag was repository-ledger's **dual remote**:
   `origin` = `gitolite@localhost` (a local mirror), `github` = github.com. Agent
   pushes landed on gitolite but never reached github (what nix fetches) — fixed by
   pushing to the `github` remote explicitly.
2. **SEMA store wipe** (psyche-authorized, overriding `29pb` for pre-production): no
   migration tool exists for the layout 4→5 / 3→5 transitions, so
   `/var/lib/lojix/lojix.sema` and `/var/lib/mirror/mirror.sema` were removed (keeping
   `bootstrap-datom.nota` + `generated-inputs/`); both daemons `StampFresh`-created
   clean layout-5 stores.
3. **repository-ledger binary-startup encoder**: new
   `repository-ledger-write-configuration` binary (github `48109483`) + the
   `repository-receive.nix` ExecStartPre-encoder / ExecStart-on-rkyv rework.
4. **clavifaber config**: two fixes in `complex.nix` — the enum body to 2 roots
   (`(Tag (payload))`), then the inner `OpenSshPublicKeyLocation` to a **no-tag struct
   body** `(${path})` (a named struct emits its fields, not its type name). Both
   verified against the live binary before landing (CriomOS `ebd7de29`).

## The two hazards, and the mechanisms that beat them

- **Switch self-restart deadlock.** A `Switch` whose target == daemon host runs
  `switch-to-configuration switch` over a foreground ssh the daemon awaits; activation
  restarts the daemon, killing the ssh + the switch together. Recovery and every
  subsequent activation used a **detached transient unit** (`ssh root` +
  `systemd-run --service-type=oneshot --wait <gen>/bin/switch-to-configuration switch`),
  which is PID-1-owned and survives. Confirmed deadlock-free across the rollback and
  the cutover. The daemon's own deadlock-free path is `BootOnce` (same systemd-run
  shape, deferred to reboot); 0.3.5 did **not** fix the in-place Switch case.
- **No clean way to read the built toplevel from a Build.** `Build` realizes the
  closure but creates no profile generation; only `Switch` stages a `system-NNN`.
  So the pattern was: `Build` to confirm green, then `Switch` to stage the gen (it
  deadlocks, expected), then detached-activate the staged gen.

## Access model correction

Root on hosts is reached via **ssh key, not sudo** (`ssh root@localhost` /
`ssh root@ouranos.goldragon.criome`). This is the standing deploy/admin access path.

## Residual / next

- `complex-init` on the live gen-126 still has the old broken baked script; the
  publication was written manually with the corrected invocation and the unit
  reset to inactive. The permanent fix is in main (`ebd7de29`) and activates on the
  next ouranos deploy — no special action needed.
- **Next milestone: prometheus.** The 0.3.5 daemon has build-on-target, so the
  durable vm-testing TestVm node on prometheus is now unblocked. prometheus is a live
  LargeAiRouter — deploy via **BootOnce + reboot** (Switch forbidden, Spirit `kx32`),
  build-on-target so models never transit ouranos. This is a live-router action +
  a reboot (brief connectivity drop) and should be psyche-timed.

## Deferred Spirit captures (Spirit daemon down — store schema v10 vs deployed binary)

To record when Spirit recovers: nightly-toolchain Correction; Switch-self-deadlock
Constraint (detached activation / BootOnce); ssh-not-sudo access model; the
pre-production store-wipe disposition vs `29pb`.
