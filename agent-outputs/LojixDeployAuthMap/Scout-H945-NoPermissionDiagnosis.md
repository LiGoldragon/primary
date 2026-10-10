# Scout — primary-h945 System-Deploy "NOPERMISSION" Root-Cause Diagnosis

Read-only diagnosis of the blocked live **System** deploy to `ouranos`
(`primary-h945`). No state changed: only `lojix` queries, `systemctl show`,
`journalctl` reads, `/run` symlink reads, and repo/flake.lock reads. No `ssh`,
no deploy, no activate, no privileged host op. `OBSERVATION` and `INTERP`
(interpretation) are labelled; `UNKNOWN`s named at the end.

## Verdict (one line)

The "NOPERMISSION" is a triple mislabel of a plain application crash: a failing
`mirror.service` makes `switch-to-configuration switch` exit **4**, which systemd
cosmetically names `NOPERMISSION` and lojix 0.3.10 further mis-names
`BuilderUnreachable`. No privilege, credential, or store permission is denied
anywhere. **Clearing it needs psyche/operator action** (see Remediation).

## The verbatim failing operation and error

OBSERVATION — last System Switch attempt (deploy id 38, 2026-07-02 16:55:09,
from `journalctl -u lojix-daemon.service`). The daemon (as `li`) ran:

```
ssh -o BatchMode=yes root@ouranos.goldragon.criome systemd-run \
  --unit=lojix-self-switch-deploy-38 --collect --wait --service-type=oneshot \
  /bin/sh -c 'export PATH=/run/current-system/sw/bin:/run/wrappers/bin:$PATH
set -eu
nix-env -p /nix/var/nix/profiles/system --set /nix/store/c4kfjxxvb269...-nixos-system-ouranos-26.05...
/nix/store/c4kfjxxvb269...-nixos-system-ouranos-26.05.../bin/switch-to-configuration switch
... bootctl set-default / set-oneshot ...'
  exited with exit status: 4: Running as unit: lojix-self-switch-deploy-38.service
          Finished with result: exit-code
Main processes terminated with: code=exited, status=4/NOPERMISSION
lojix deploy pipeline terminal output: DeployRejected(... deploy_rejection_reason: BuilderUnreachable ...)
```

OBSERVATION — the transient unit's own journal
(`journalctl -u lojix-self-switch-deploy-38.service`) shows the switch ran to the
very end as root, doing all real work, and failed only on one started unit:

```
Checking switch inhibitors... done
switching to system configuration /nix/store/c4kfjxxvb269...
stopping the following units: keyd.service
activating the configuration...
setting up /etc...
reloading user units for li... / for root...
restarting sysinit-reactivation.target
restarting the following units: home-manager-bird.service, home-manager-li.service, nix-daemon.service
starting the following units: keyd.service
the following new units were started: NetworkManager-dispatcher.service
warning: the following units failed: mirror.service        <-- the only failure
  ● mirror.service - SEMA version-control mirror daemon
    ExecStart=.../mirror-0.1.2/bin/mirror-daemon ...  (code=exited, status=1/FAILURE)
switching to system configuration /nix/store/c4kfjxxvb269... failed (status 4)   <-- exit 4
```

The identical pattern occurs for deploy id 25 (2026-06-29 16:23:31): same script,
same `warning: the following units failed: mirror.service`, same `failed (status 4)`.

## Where it originates in the deploy path

OBSERVATION — decomposing the pipeline, each earlier stage **succeeded**:

- SSH to `root@ouranos` succeeded — the unit printed `Running as unit: ...` and
  ran for 13.1 s (id 38) / 6.9 s (id 25). No `Permission denied (publickey...)`
  on this path.
- `systemd-run` created and ran the unit as **root** (system manager, PID 1).
- `nix-env -p /nix/var/nix/profiles/system --set` succeeded — it created
  `/nix/var/nix/profiles/system-136-link -> c4kfjxxvb269...` (mtime Jul 2 16:54).
- `switch-to-configuration switch` executed fully as root: stopped/started/reloaded
  units, set up `/etc`, restarted `home-manager-*`, `nix-daemon`. The bootloader
  install runs in this phase (INSTALL_BOOTLOADER in the wrapper) and evidently
  applied (see "current live state").

INTERP — the failure originates **at the very last activation step**:
`switch-to-configuration`'s post-start health check. It found one unit it started
(`mirror.service`) had failed, so it returned exit code **4**. Exit-4 semantics
are self-evidenced by the log: the line `the following units failed: mirror.service`
is immediately followed by `failed (status 4)`. It is *not* a bootloader,
profile, ssh, or nix-copy failure.

The three misleading labels, in order:

1. `switch-to-configuration` returns **4** to signal "one or more units failed to
   start during the switch."
2. systemd's `systemd-run --wait` reports that numeric exit as
   `code=exited, status=4/NOPERMISSION` — `NOPERMISSION` is systemd's fixed LSB
   cosmetic name for exit code 4, **not** an EPERM/EACCES.
3. lojix 0.3.10 `fail_pipeline` maps any `Activate`-stage failure to
   `DeployRejectionReason::BuilderUnreachable` (the prior scout pinned this at
   `src/schema_runtime.rs:2610-2611`; 0.4.x renames it `ActivationFailed`).

## The true cause (ruled IN, with evidence)

OBSERVATION — `mirror.service` is failing **live right now** (not just during the
switch). `systemctl status mirror.service`:

```
● mirror.service - SEMA version-control mirror daemon
   Active: activating (auto-restart) (Result: exit-code)
   ExecStart=.../mirror-0.1.2/bin/mirror-daemon /run/mirror/mirror-daemon.rkyv
            (code=exited, status=1/FAILURE)
```

`Restart=on-failure`, `RestartSec=5s` (from `modules/nixos/mirror.nix`) → it
crash-loops continuously.

OBSERVATION — the exact daemon error (`journalctl -u mirror.service -o cat`,
repeated every restart):

```
mirror-daemon: component error: ledger storage: table store-heads is registered as
HeadFamily@52af5f99ad1dec0f688deaf4a89a8bf4e91b75b752f3a60d9bcf9405b6913999 (table store-heads),
not as the declared
HeadFamily@df02e0f568beec2191368d3ed50dc27a880d04e1fa597ac4c0990ea01d92f9ec (table store-heads)
```

INTERP — this is a **persistent-storage schema/type-signature mismatch**. The
SEMA ledger (`/var/lib/mirror/mirror.sema`, a redb store per `mirror.nix:19`) has
its `store-heads` table stamped with the `HeadFamily` type fingerprint
`52af5f99…` written by an **older** mirror binary. The current binary
(mirror-0.1.2) declares `HeadFamily` (value type `StoredHead`, see
`mirror/src/schema/sema.rs:1097,1113-1114`) with fingerprint `df02e0f5…`. The
sema engine enforces family-fingerprint equality on table open (a safety gate
against reading data under the wrong type) and refuses → `mirror-daemon` exits 1.
There is **no migration or reset-on-mismatch path** in the mirror source (grep
for migrat/reset/recreate/drop_table in `*.rs` returned nothing).

INTERP — so the on-disk **data** is stale relative to the binary; the binary and
the CriomOS pin agree (both 0.1.2). The mirror ledger owner is user `mirror`,
group `nixdev`, dir mode `2770` — `li` cannot even `ls /var/lib/mirror`
(Permission denied), confirming the fix target is a privileged path.

### Ruled OUT (with evidence)

- (a) **Privilege the deploying user lacks to switch the system profile /
  activate** — RULED OUT. The self-switch ran as root via `systemd-run`; every
  privileged step (`nix-env --set`, `/etc`, unit restarts, bootloader) succeeded.
  No EPERM/EACCES appears anywhere in the unit journal.
- (b) **Auth / credential issue** — RULED OUT. `ssh -o BatchMode=yes
  root@ouranos` authenticated (the remote unit ran). The only
  `Permission denied (publickey,keyboard-interactive)` lines in the journal are
  **older, unrelated** deploys to *other* nodes (`zeus`, `prometheus`, user
  `bird`), not this ouranos self-switch.
- (c) **Nix store / builder permission** — RULED OUT. The closure was present,
  `nix-env --set` wrote the system profile, and the switch read the toplevel
  freely. No store/copy permission error on the failing path.

## Current live-vs-repo state (Q4)

OBSERVATION:

- **Live/booted system**: `/run/current-system` == `/run/booted-system` ==
  `c4kfjxxvb269...-nixos-system-ouranos-26.05...` (= `system-136-link`, created by
  the failed id-38 `nix-env --set`). INTERP: the switch **partially applied** —
  the toplevel/bootloader took effect and the machine has since booted it — but
  `mirror.service` never came up, so lojix marked the deploy rejected.
- **lojix's own view is stale/diverged**: `lojix "(Query (ByNode (goldragon
  ouranos None)))"` shows the last recorded `FullOs Switch` as gen 20
  (`dfp8lba…`) and a gen 33 `FullOs BootOnce` (`5wv10ns…`); **none** equal the
  actually-booted `c4kfjxxvb269…`. lojix has no `Current` record for the running
  system toplevel because the deploy that produced it was rejected.
- **lojix daemon on host**: **0.3.10** (`/nix/store/2a719h33…-lojix-0.3.10`),
  a `User=li` system unit, active (PID 3488, since Jul 2 23:58). lojix 0.4.x is
  **absent from the live host** — confirms the brief. (The 0.3.10 CLI has no
  `(Version)` variant; version read from the resolved store path.)
- **spirit / guardian prompt**: `spirit "(Version)"` → `(VersionReported 0.21.0)`,
  matching the landing evidence (rev `7b0770642ab1`, home gen 39 `z26qd5…`,
  activated live via the **home** path on Jul 3). INTERP: the guardian prompt is
  live through the user/home profile, but the booted **system** generation
  (`c4kfjxxvb269…`, built Jul 2) pins an **older home input**. Because CriomOS
  activates home via system-level `home-manager-li.service`, a reboot re-activates
  the system-pinned (older) home → the guardian prompt reverts. Making it
  reboot-persistent requires a successful **System Switch** pinning the new home
  input — the exact blocked path.
- **A fresh System deploy would hit the same wall**: CriomOS main
  (`0be40ba`) `flake.lock` pins the `mirror` input at rev `5102f5e` = the same
  **mirror-0.1.2** binary now crash-looping, and `mirror.nix` enables
  `mirror.service` on ouranos (`mirrorEnabled = has "TailnetClient" && has
  "PersonaDevelopment"`, both present). So any System Switch built from current
  main restarts the same failing unit against the same stale `/var/lib/mirror`
  ledger and exits 4 again — **independent of the lojix 0.3.10→0.4.x change**.
  No bead tracks this specific `store-heads`/`HeadFamily` storage crash.

## Remediation (Q5) — what it takes to clear the blocker

The switch fails solely because `mirror.service` fails to start. Two routes:

### Route A — immediate host unblock — REQUIRES PSYCHE / OPERATOR ACTION
Clear (or migrate) the stale ledger on ouranos: stop `mirror.service`, back up
and remove `/var/lib/mirror/mirror.sema`, restart. mirror-0.1.2 then recreates
the table with the new `df02e0f5…` fingerprint, the service goes green, and the
next System Switch's `mirror.service` restart succeeds.
- **Requires psyche/operator**: `/var/lib/mirror` is owned by `mirror:nixdev`,
  mode 2770 — `li` cannot read it, let alone modify it. This needs root (or the
  `mirror` user) on the host, and it **discards accumulated mirror ledger state**
  (SEMA heads) — a data-affecting decision the psyche should own (the ledger is
  intended to be reconcilable from criome per `primary-iy51.3`, but that path is
  not yet built).

### Route B — durable in-repo fix — WORKER-LANDABLE (with a caveat)
Teach the mirror component to survive its own storage-schema evolution: on a
`store-heads` family-fingerprint mismatch, either migrate the table or explicitly
reset/recreate it (drop-and-rebuild), rather than erroring out. Land in `mirror`,
bump the version, bump CriomOS's `mirror` pin. A new system generation then
carries a mirror-daemon that starts cleanly against the stale ledger, so the
System Switch's restart succeeds and self-heals the host state on first start (no
manual host op needed).
- **Worker-landable in-repo** — no host privilege to author.
- **Caveats**: (1) a "reset" flavor discards existing heads → same data-loss
  decision as Route A, worth psyche confirmation on acceptability; (2) the fixed
  daemon must start within `switch-to-configuration`'s health-check window; (3)
  **landing the fix still needs a live System deploy to take effect**, and that
  privileged `meta-lojix` System Switch is itself the operator-gated act — the
  `primary-h945` bead already pauses it for host safety (the 0.3.10→0.4.x jump).

### Route C — not recommended
Make `mirror.service` non-fatal to the switch (drop from `multi-user.target` /
change failure posture). Masks a real service failure; against the mirror epics'
direction (`primary-9ppu`, `primary-nbmq`). Note only.

### Net answer to "does clearing it require psyche action?"
**Yes.** The minimal unblock (Route A) is a privileged, data-discarding host op
`li` cannot perform. The durable fix (Route B) is worker-landable in source, but
(i) may still require psyche sign-off on discarding mirror ledger state, and
(ii) cannot clear `h945` by itself — the live **System Switch** that finally
lands it (and jumps lojix 0.3.10→0.4.x) is an operator-authorized privileged
deploy the bead has intentionally paused. A worker can land the code; only the
psyche/operator can run the deploy (and/or clear host state) that proves it
cleared.

### What would prove it cleared
`systemctl is-active mirror.service` → `active` on ouranos; a subsequent
`meta-lojix "(Deploy (System (goldragon ouranos FullOs ... Switch ...)))"` returns
accepted **and** `lojix "(Query (ByNode (goldragon ouranos None)))"` shows a new
`FullOs Switch Current` record whose store path equals the newly-built toplevel;
`/run/booted-system` matches it after reboot; and the guardian prompt survives
the reboot.

## Unknowns

- Which earlier mirror version wrote the on-disk `52af5f99…` fingerprint (git
  archaeology not done; not needed for the diagnosis). UNKNOWN.
- Whether a mirror migration is feasible vs a reset being the only realistic fix
  — a mirror-component design question for the implementer. UNKNOWN.
- Whether the psyche accepts discarding the ouranos mirror ledger state. UNKNOWN
  — needs a psyche decision.
- Exact `switch-to-configuration-ng` exit-code table not read from source (the
  `.switch-to-configuration-wrapped` is a compiled binary; `/nix/store` search is
  barred). Exit-4 = "units failed to start" is taken from the direct journal
  correlation, which is unambiguous.

## Evidence pointers

- `journalctl -u lojix-daemon.service` — id 38 (Jul 2 16:55) and id 25 (Jun 29
  16:23) full blocks; `journalctl -u lojix-self-switch-deploy-38.service` /
  `-25.service` — the switch's own output incl. `mirror.service` failure.
- `systemctl status mirror.service`, `journalctl -u mirror.service -o cat` — live
  crash-loop + `ledger storage ... store-heads ... HeadFamily@…` error.
- `/run/current-system` == `/run/booted-system` == `c4kfjxxvb269…`;
  `/nix/var/nix/profiles/system-136-link` (Jul 2 16:54).
- `lojix "(Query (ByNode (goldragon ouranos None)))"` (stale system view);
  live lojix store path `2a719h33…-lojix-0.3.10`; `spirit "(Version)"` → 0.21.0.
- `CriomOS/modules/nixos/mirror.nix` (enable cond, storePath, Restart);
  `CriomOS` `flake.lock` `mirror` → `5102f5e` (0.1.2); `mirror` repo main
  `b8cf8ec` (0.2.0), `src/schema/sema.rs:1097,1113-1151` (HeadFamily table).
- Companion prior recon: `Scout-SituationalMap.md`,
  `OperatingSystemImplementer-LandingEvidence.md`.
