# Lojix Daemon Production Readiness

Variant: Refresh

## Context-maintenance action

This report refreshes the Lojix daemon production-readiness thread after the
system-maintainer installed-path validation completed on 2026-06-15.

It retires stale system-operator sources:

- `reports/system-operator/205-lojix-horizon-production-materialization-2026-06-10.md`
- `reports/system-operator/221-Update-lojix-daemon-production-situation.md`

It keeps `reports/system-operator/220-lojix-daemon-install-zeus-deploy-handoff-2026-06-14.md`
as historical provenance because the system-maintainer closeout explicitly
cites that handoff. This Refresh is the current status surface.

Primary current closeout source:

- `reports/system-maintainer/10-lojix-daemon-installed-zeus-deploy-parity-2026-06-15.md`

No Spirit capture: this was a context-maintenance work order.

## Current conclusion

The install-first Zeus parity task is no longer pending. System-maintainer
completed it:

- the three maintainer Beads from the handoff were closed;
- `lojix-daemon` was installed locally through the pushed CriomOS FullOS path;
- the installed `lojix-daemon.service` was active on Ouranos;
- installed `meta-lojix` drove Zeus Eval, Build, and Boot through the installed
  owner socket and got `Deployed` replies;
- Zeus host verification over root SSH showed the boot profile/default entry
  matching the deployed generation;
- one follow-up bug remains: ordinary query returned an empty generation listing
  after successful Boot.

The remaining Lojix parity caveat is now the state/query bug tracked as
`primary-htrk` ("lojix daemon post-Boot query returns empty generation
listing"), not installation.

## What landed

`lojix` main now has a Nix package/check surface:

- `packages.default` builds `lojix-daemon`, `lojix`, `meta-lojix`, and
  `lojix-write-configuration` with `nota-text` enabled for human-facing
  clients;
- `packages.daemon-binary` separately builds daemon-only pressure without
  `nota-text`;
- `checks.daemon-startup-rejects-nota` proves the daemon rejects inline NOTA
  startup and requires a signal/rkyv startup file.

`CriomOS` main now consumes `github:LiGoldragon/lojix` and installs
`lojix-daemon.service` on `PersonaDevelopment` nodes. The service:

- runs as `li:users`, matching the local owner-socket peer authorization
  requirement;
- generates `/run/lojix/startup.rkyv` with installed
  `lojix-write-configuration`;
- starts installed `lojix-daemon` with that rkyv startup argument;
- exposes `/run/lojix/ordinary.sock` and `/run/lojix/owner.sock`;
- stores durable state under `/var/lib/lojix`.

`CriomOS-home` main now pins the interactive Rust toolchain to exact Rust
`1.96.0` rather than `stable.latest`, avoiding the moving rust-overlay channel
hash failure encountered during FullOS evaluation.

Landed source commits named by the closeout:

- `lojix` `214acf53`: add Nix package surface.
- `CriomOS` `a45fc524`: install lojix daemon on operator hosts.
- `CriomOS` `74924fde`: update CriomOS rust-overlay pin.
- `CriomOS` `18e6ed95`: align CriomOS-home rust-overlay input to top-level pin.
- `CriomOS-home` `ce31cc21`: pin Home Rust toolchain version.
- `CriomOS` `57561a41`: pin CriomOS-home exact Rust toolchain.

Later local inspection saw `CriomOS-home` main at `d2f48a3a`
(`criomos-home: repin spirit typeref boundary`), after the Rust-toolchain pin.

## Installed state proven

Ouranos FullOS Eval, Build, and Switch from pushed `CriomOS/main` succeeded
through the production deploy path. The final installed validation did not use
`target/debug`.

Post-switch state from the maintainer closeout:

- `lojix-daemon.service`: active.
- `lojix-daemon`, `lojix`, `meta-lojix`, `lojix-write-configuration`: present
  in `/run/current-system/sw/bin`.
- `/run/lojix/ordinary.sock`: mode `0660`, owner `li:users`.
- `/run/lojix/owner.sock`: mode `0600`, owner `li:users`.
- `/run/lojix/startup.rkyv`: mode `0600`, owner `li:users`.
- `/var/lib/lojix`: mode `0750`, owner `li:users`.

Installed service/socket smoke:

- ordinary query before deploy validation: `(Queried ([] (0 0)))`;
- temporary startup with owner socket mode `0666` was rejected by installed
  `lojix-daemon`;
- installed `meta-lojix` Eval for Zeus through `/run/lojix/owner.sock` returned
  `(Deployed (1 (0 0)))`.

Zeus installed-daemon validation through installed `meta-lojix`:

- Eval: `(Deployed (1 (0 0)))`;
- Build with builder `prometheus`: `(Deployed (1 (2 2)))`;
- Boot with builder `prometheus`: `(Deployed (1 (4 4)))`.

After Boot, root SSH to `zeus.goldragon.criome` showed
`/nix/var/nix/profiles/system` and `/run/current-system` resolving to the same
Zeus system profile path, and `bootctl status` showed the default boot entry
for that generation.

## Current open bug

The required post-test ordinary query was captured:

```text
(Queried ([] (6 6)))
```

The database marker advanced through the deploy pipeline, but the ordinary
generation listing for `ByNode (goldragon zeus None)` was empty. Since the Zeus
boot profile verified, this is a Lojix state/query follow-up rather than proof
that the deploy failed.

Current bug task:

- `primary-htrk`: determine whether ordinary query excludes Boot-pending
  generations or the activation pipeline records phase markers without
  projecting the live generation into ordinary query results.

The next implementation pass should reproduce this in a `lojix` test before
changing state/query code.

## Current coordination state

During this context-maintenance pass, the operator lane was actively holding
the Spirit/domain-coarsening branch-family locks (`primary-fwe3`,
`primary-gm78`, and related Spirit/schema worktrees). Do not take those locks
for Lojix work.

`primary-htrk` was readable and marked in-progress for system-maintainer. The
general open-Beads list intermittently hit the known embedded-Dolt writer lock;
treat that as transient storage contention, not ownership.

## Retired framing

The 205-era frame is stale. It said Lojix production materialization had moved
closer to production but still lacked durable `sema-engine` backing and install
wiring. Current main has both durable backing and install wiring, and the
installed path has been validated through Zeus Boot.

The 221-era frame is stale because it described the daemon as not installed and
the three maintainer Beads as still open. That was true before
system-maintainer's pass; it is no longer current.

The older `horizon-leaner-shape` worktree remains historical evidence only. It
uses the old single-socket/text-startup daemon contract and should not be used
as the current install shape.
