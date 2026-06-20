# Durable VM-test node live on prometheus — daemon-based deploy complete

System-designer, ouranos, 2026-06-20. Culmination of reports 145–154. **The durable
`vm-testing` TestVm node is deployed on prometheus, built-but-not-booted, via the
lojix daemon's build-on-target — with the live LargeAiRouter intact and zero models
ever transiting ouranos.** This was the original goal.

## Final verified state

**prometheus** (booted gen 49, persistent default):
- Running gen `2j08dj66` (the new FullOs gen); `bootctl` Default Entry =
  `nixos-generation-49`, one-shot cleared — durable across reboots.
- **`vm-testing` TestVm: defined but NOT booted** — every `microvm-*@vm-testing` +
  `install-microvm-vm-testing` unit is `loaded inactive dead`; microvm autostart does
  not include it (autostart=false). Bootable on demand for continual dev.
- Live router intact: `prometheus-llama-router`, `yggdrasil`, `hostapd` active after
  the reboot. Home profiles (`home-manager-li`) active. **Zero failed units.**
- VmHost capability present (pod net `169.254.100.0/22`, capacity 4).

**ouranos** (daemon host): `lojix-daemon` = **0.3.10**, self-Switch-capable, healthy.

**Model safety** (the psyche's explicit concern, verified): ouranos holds only the
2 KB model `.drv` metadata, zero GGUF data; prometheus holds the 114 model paths and
ran the build. The eval-store + build-store fixes keep the entire model closure on the
target.

## The full arc (0.3.4 → 0.3.10)

The deploy pipeline was deeply rotted; each layer was repaired and verified:
1. **Rust → nightly** cluster-wide (fenix `complete`, no rolling-stable hash); fixed a
   dual-remote trap (repository-ledger pushing to gitolite, not github).
2. **lojix 0.3.5 cutover** (SEMA stores wiped — no migration tool exists, psyche-approved
   pre-prod) + config-contract fixes (repository-ledger binary startup, clavifaber 2-root).
3. **lojix 0.3.6** horizon bump (5-root ClusterProposal) — resolved the daemon↔datom
   schema skew (the daemon had been a stranded 4-root/12-Machine intermediate).
4. **lojix 0.3.7** per-deploy secrets provisioning (the `secrets` override CriomOS's
   stub promised but the daemon never generated).
5. **Self-audit** (54-agent adversarial workflow, report 154): caught a real critical
   error — I had claimed the 0.3.8 eval-store fix worked when it didn't.
6. **Batched audit fixes (lojix 0.3.9)**: real eval-store fix (verified), deadlock-free
   self-Switch, write_secrets cleanup, drop the lossy sops-name transform (verbatim
   stems + goldragon secrets renamed to camelCase), typed errors; + clavifaber
   golden-string test + horizon comment corrections.
7. **lojix 0.3.10**: the eval-store fix's missing half — the BUILD step must also use
   `--store` target (not `--eval-store auto`); eval and build now consistently realize
   on the target store. (Found by running the build, not just the eval — the audit's
   whack-a-mole lesson, owned.)
8. **spirit recovery (0.15.0)**: root cause was generator-version skew — spirit pins
   `schema-rust-next 90d853c3` (moved per-struct impls into the `{| |}` catalog) while
   the signal-* crates' checked-in `.rs` were generated against older revs. Regenerated
   the 5 build-blocking crates; `nix build .#default` green. The Spirit daemon is now
   buildable again (it had been down all session).

## Two fixes proven in production this session

- **Deadlock-free self-Switch (0.3.9)**: the daemon redeployed ouranos to 0.3.10 with
  **zero manual intervention** via a detached `systemd-run` self-switch unit — the
  deliberate-deadlock workaround is retired. (Audit CRITICAL B.)
- **build-on-target end-to-end**: eval + build both `--store` the target; prometheus's
  full FullOs closure (incl. the 122B model derivations + vm-testing) realized on
  prometheus, nothing on ouranos. (The build-on-target design intent, now complete.)

## Follow-ups (honest remaining work)

- **Spirit daemon**: it now *builds* (0.15.0), but the running daemon still needs
  deploying/restarting on its host before it accepts records again. Until then the
  deferred captures stay queued.
- **Deferred Spirit captures**: nightly-toolchain Correction, the (now-fixed)
  Switch-self-deadlock Constraint, ssh-not-sudo access model, the store-wipe-vs-`29pb`
  disposition, the secrets-provisioning Decision — to append to `spiritbackup.nota`
  and replay when the daemon is back.
- **Daemon default-source smell**: `lojix.nix` `WriterTestDefaults` still points at the
  test cluster + an absent `cluster.nota`; deploys pass the source explicitly so it's
  not blocking, but it should point at the production cluster (design: how the cluster
  datom reaches the daemon's state dir).
- **router source lag**: `router` fails to compile against the new `{| |}` generator —
  pre-existing application-source work, gated out of all deploys.
- **vm-testing**: deployed built-but-not-booted; boot it on demand to validate the VM
  for continual development.
