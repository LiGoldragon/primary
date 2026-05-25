# 189 — Spirit v0.2 live cutover

## What changed

The live Spirit default was cut over from v0.1.0 to v0.2.0.

Production database handling:

- stopped `persona-spirit-daemon-v0.1.0.service`,
  `persona-spirit-daemon-v0.1.1.service`, and
  `persona-spirit-daemon-v0.2.0.service`
- copied the stopped v0.1.0 database as the migration source
- ran `spirit-migrate-0-1-to-0-2`
- replaced only the v0.2.0 database
- restarted `persona-spirit-daemon-v0.2.0.service`
- left v0.1.0 and v0.1.1 stopped after verification

Backups:

- source copy:
  `/home/li/.local/state/persona-spirit/v0.1.0/persona-spirit.redb.cutover-source-20260525222821`
- previous v0.2.0 database backup:
  `/home/li/.local/state/persona-spirit/v0.2.0/persona-spirit.redb.pre-cutover-20260525222821`

## Deployment change

`CriomOS-home` now defaults the unversioned `spirit` command to v0.2.0:

- commit `51df5573`
- file: `modules/home/profiles/min/spirit.nix`
- change: `criomosHome.personaSpirit.currentDefault` default
  `v0.1.0` -> `v0.2.0`

I built and activated the home generation with the lojix-projected inputs for
ouranos:

- `system`: `~/.cache/lojix/system/x86_64-linux`
- `horizon`: `~/.cache/lojix/horizon/goldragon/ouranos`
- `deployment`: `~/.cache/lojix/deployment/home-on`
- local `CriomOS-home` override

## Verification

Nix/module check:

```sh
nix build --option max-jobs 0 \
  .#checks.x86_64-linux.persona-spirit-versioned-deployment \
  --print-out-paths
```

Migration output:

```nota
(MigrationCompleted 699)
```

Live service state after cutover:

- `persona-spirit-daemon-v0.2.0.service`: active
- `persona-spirit-daemon-v0.1.0.service`: inactive
- `persona-spirit-daemon-v0.1.1.service`: inactive

Unversioned `spirit` now resolves to the v0.2.0 wrapper and returns 699
records.

Representative live checks:

- `spirit '(Observe (Records (None None WithProvenance)))'` -> 699 records
- `spirit '(Observe Topics)'` -> v0.2 topic catalog returned
- `spirit '(Observe (Records (None (Some Decision) WithProvenance)))'` -> 303
  Decision records

## Note

I incorrectly captured an operational migration instruction as a Spirit intent
record before the psyche corrected me. I did not add another record for that
correction during the cutover. The incorrect record is now part of the migrated
database because it had already been written to the v0.1.0 source before the
final migration run.
