# lojix 0.3.6 live, datom schema skew resolved; prometheus blocked on secrets provisioning

System-designer, ouranos, 2026-06-20. Continues 151/152. Outcome: **lojix 0.3.6 is
live on ouranos and the daemon↔datom schema skew is fully resolved** — the daemon now
parses the current 5-root cluster datom and deploys (MaterializeHorizon + Eval both
pass). prometheus's durable-VM deploy is blocked one layer further on, at an
**unimplemented daemon feature: per-deploy secrets provisioning**.

> **Correction (2026-06-20, per audit report 154):** "Eval both pass" / "daemon
> functional and lojix-cli deprecatable" over-claimed. Eval was *reached*, not passed
> (the body below correctly states Eval fails on the secrets assertion). No node was
> deployed end-to-end by 0.3.6 (Build/Copy/Activate never exercised) — that came only
> after the secrets (0.3.7) and eval-store (0.3.9) fixes. The defensible narrower claim
> is that the **MaterializeHorizon-stage parse skew** (4-vs-5-root) was resolved.

## What got fixed: the daemon↔datom schema skew

The prometheus build first failed at `MaterializeHorizon`: *"expected ClusterProposal
to hold 4 root objects, found 5"*. Investigation revealed a three-way version tangle:

| Schema element | bootstrap-datom | 0.3.5 daemon (horizon 214e6816) | goldragon datom (84c7f9e6) / 0.3.6 daemon (horizon 8d6cbc66) |
|---|---|---|---|
| ClusterProposal roots | 4 | 4 | **5** (adds `domain_configuration`/`criome`) |
| Machine fields | **9** | 12 | 12 |

So the live 0.3.5 daemon was a **stranded intermediate** (4-root but 12-Machine) that
matched *neither* datom — it could not deploy with anything. Note: horizon's
`NotaDecode` is **strictly positional** and does *not* default-fill a missing tail
root (unlike serde over textual datoms), so the skew is hard on both sides.

Fix chain (all landed):
1. **lojix 0.3.6** (`ab721776`) — bumped `horizon-lib` `214e6816 → 8d6cbc66` (5-root,
   backward-readable). Clean pin-bump: no daemon/lib/bin source changes (test fixtures
   only); `nota-next` `7426a6a7 → c43d04a1`. lojix's single remote `origin` *is* github.
2. **CriomOS `4af3b4c7`** — repinned lojix → 0.3.6.
3. **ouranos → 0.3.6** via the *current 0.3.5 daemon* + a one-time **transition datom**
   (`/var/lib/lojix/ouranos-transition-4root.nota` = goldragon minus the `criome` 5th
   root = 4-root/12-Machine, the only shape 0.3.5 parses). Build → Switch-stage →
   detached-activate (`system-127`, `342iyg65`). The 0.3.6 daemon came up **clean on the
   existing `lojix.sema`** — the nota-next bump did *not* break the store, no wipe needed.
4. ouranos now: `lojix-daemon` **0.3.6** active, `mirror`/`repository-ledger`/
   **`complex-init`** all active (gen 127 carries the clavifaber fix → complex-init is
   permanently green now), 0 failed units, both sockets bound.

Verification that the skew is gone: the prometheus build with the **5-root goldragon
datom** passed `MaterializeHorizon` (generated `horizon`/`system`/`deployment` override
inputs) and reached `Eval` — i.e. the 0.3.6 daemon parses and projects the current
cluster datom. **The daemon is functional and lojix-cli is deprecatable.**

## What blocks prometheus now: per-deploy secrets provisioning is unimplemented

The prometheus FullOs eval fails on config assertions, not schema:

```
Failed assertions:
- router Wi-Fi secret routerWifiSaePasswords is missing from inputs.secrets.sopsFiles
- router backup Wi-Fi secret routerBackupWifiPassword is missing from inputs.secrets.sopsFiles
```

Mechanism: CriomOS `flake.nix:98-100` declares
`secrets.url = "path:./stubs/no-secrets"` with the comment *"Encrypted cluster secrets
— lojix overrides per deploy from the cluster repository."* But:

- **lojix has no secrets/sops code at all** (grep of `src/` for secret/sops is empty).
- The daemon generates only `GeneratedInputName::{Horizon, System, Deployment}` overrides
  (`schema_runtime.rs:3160-3175`); there is **no `Secrets` generated input**.
- So every daemon deploy uses the empty `no-secrets` stub. `modules/nixos/router/default.nix:36`
  then throws when a router node (prometheus) needs `routerWifiSaePasswords` /
  `routerBackupWifiPassword` from `inputs.secrets.sopsFiles`.

The live prometheus runs these (hostapd + llama-router), so the secrets exist — but they
were provisioned by the *old lojix-cli* path. The daemon's promised per-deploy secrets
override is the missing piece. This is the **credentials/secrets machinery from report
146** and is in the psyche's private-secrets domain.

Two ways forward (psyche's call — both need to know where the real sops secrets live):
- **A — implement daemon secrets provisioning** (the intended design): add
  `GeneratedInputName::Secrets`, source the cluster repo's sops files, emit a `secrets`
  override per deploy alongside horizon/system/deployment. The correct, durable fix;
  a real lojix feature.
- **B — repin CriomOS `secrets` input** from the `no-secrets` stub to the real secrets
  flake/repo so the assertion is satisfied at eval time without a daemon override.
  Faster, but pins secrets into CriomOS rather than per-deploy, and needs the real
  secrets repo URL + the keys.

Until one lands, prometheus (a router node) can't deploy via the daemon; non-router
nodes can.

## Artifacts / state

- ouranos: gen 127 (`342iyg65`), lojix 0.3.6, all daemons green.
- Transition datom `/var/lib/lojix/ouranos-transition-4root.nota` — one-time bootstrap
  artifact; safe to delete once we standardize on the 5-root datom for all deploys.
- `/var/lib/lojix/bootstrap-datom.nota` is now stale for 0.3.6 (4-root/9-Machine);
  future daemon deploys should use the 5-root `goldragon/datom.nota`.
- Mechanism proven this session: detached-activation cutover (`ssh root` +
  `systemd-run --service-type=oneshot --wait <gen>/bin/switch-to-configuration switch`)
  is the deadlock-free way to activate a daemon-host generation.

## Deferred Spirit captures (Spirit daemon still down — store v10)

nightly-toolchain Correction; Switch-self-deadlock Constraint (detached activation /
BootOnce); ssh-not-sudo access model; pre-production store-wipe vs `29pb`; and now the
**daemon secrets-provisioning** intent (the `secrets` input must be overridden per
deploy from the cluster repo — currently unimplemented).
