# 191 — Spirit-next multi-topic deployment

## Scope

Implemented the v0.3 Spirit-next multi-topic record shape, deployed it beside
production v0.2.0, then cut production `spirit` over to v0.3.0 after the
psyche opened a no-writers migration window.

Repos changed:

- `/git/github.com/LiGoldragon/signal-persona-spirit`
- `/git/github.com/LiGoldragon/persona-spirit`
- `/git/github.com/LiGoldragon/CriomOS-home`

## What Changed

`signal-persona-spirit` now has `Topics(Vec<Topic>)` as the record topic
surface. `Entry` and `RecordDescription` carry `topics`, not a single
`topic`. NOTA shape is:

```text
(Record ([spirit deployment] Correction [description] High))
```

That is two topics, `spirit` and `deployment`. A migrated old v0.2 record
whose single topic contained a space remains one topic and prints as:

```text
(707 [[spirit deployment]] Decision [description] Maximum)
```

The contract decoder rejects invalid topic vectors before they become a
signal operation:

- empty topic vector
- duplicate topics inside one record

`persona-spirit` now runs store schema version 3, validates topic vectors at
store import/assert boundaries, filters records by topic membership, counts
topic memberships, and ships `spirit-migrate-0-2-to-next`.

`CriomOS-home` now deploys a `next` Spirit lane:

- wrapper: `spirit-next`
- service: `persona-spirit-daemon-next.service`
- state: `~/.local/state/persona-spirit/next/`
- sockets: `spirit.sock`, `owner.sock`, `upgrade.sock`

Production now has a stable v0.3.0 lane:

- wrapper: `spirit-v0.3.0`
- service: `persona-spirit-daemon-v0.3.0.service`
- state: `~/.local/state/persona-spirit/v0.3.0/`
- sockets: `spirit.sock`, `owner.sock`, `upgrade.sock`

The unsuffixed `spirit` wrapper now resolves to `spirit-v0.3.0`.

## Verification

Nix checks passed with remote-builder use:

```text
nix flake check --option max-jobs 0
nix build .#checks.x86_64-linux.persona-spirit-versioned-deployment --option max-jobs 0
```

Deployment was activated with:

```text
nix run /git/github.com/LiGoldragon/lojix-cli# --option max-jobs 0 -- "(HomeOnly ... Activate None None)"
```

The installed `lojix-cli` in the profile was too old for the current
bracket-string / curly-map proposal file, so the deployment used the local
`lojix-cli` checkout through Nix.

Pre-cutover next-lane runtime checks:

- `persona-spirit-daemon-v0.2.0.service` active.
- `persona-spirit-daemon-next.service` active.
- `spirit` resolved to `spirit-v0.2.0`.
- `spirit-next` resolves to the next wrapper and uses
  `PERSONA_SPIRIT_NEXT_SOCKET`.
- v0.2.0 database was snapshot-copied while the v0.2 daemon was briefly
  stopped, then migrated into next.
- Migration completed 707 records.
- A live multi-topic next record was accepted as record 708.
- Querying `deployment` through `spirit-next` returns record 708.
- Querying `deployment` through production `spirit` returns no records.
- Duplicate-topic input through `spirit-next` is rejected at request decode.

Post-cutover production runtime checks:

- `persona-spirit-daemon-v0.2.0.service` active.
- `persona-spirit-daemon-v0.3.0.service` active.
- `persona-spirit-daemon-next.service` active.
- `spirit` resolves to `spirit-v0.3.0`.

Production cutover version refs:

- `signal-persona-spirit` `v0.3.0` -> `026d38fb8be4`
- `persona-spirit` `v0.3.0` -> `b3b1ac0cef16`

Production cutover deployment:

- `CriomOS-home` commit: `c79ac52f`
- `nix build /git/github.com/LiGoldragon/CriomOS-home#checks.x86_64-linux.persona-spirit-versioned-deployment --option max-jobs 0`
- `nix run /git/github.com/LiGoldragon/lojix-cli# --option max-jobs 0 -- "(HomeOnly ... Activate None None)"`

Production cutover database migration:

- source: `~/.local/state/persona-spirit/v0.2.0/persona-spirit.redb`
- snapshot:
  `~/.local/state/persona-spirit/persona-spirit.redb.v0.2.0.production-cutover-20260525235707`
- target: `~/.local/state/persona-spirit/v0.3.0/persona-spirit.redb`
- result: `(MigrationCompleted 708)`

Live v0.3.0 verification:

- `readlink -f ~/.nix-profile/bin/spirit` resolves to the v0.3.0 wrapper.
- `systemctl --user is-active persona-spirit-daemon-v0.3.0.service` returns
  `active`.
- `spirit "(Observe (Records ((Some [spirit deployment]) None DescriptionOnly)))"`
  returns records 707 and 708 from the migrated database.
- The same query through
  `PERSONA_SPIRIT_SOCKET=~/.local/state/persona-spirit/v0.3.0/spirit.sock nix run /git/github.com/LiGoldragon/persona-spirit#spirit --option max-jobs 0 -- ...`
  also returns records 707 and 708.

Snapshot used:

```text
/home/li/.local/state/persona-spirit/persona-spirit.redb.v0.2.0.snapshot-20260525235013
```

Pre-migration empty next database backup:

```text
/home/li/.local/state/persona-spirit/next/persona-spirit.redb.empty-before-migration-20260525235013
```

## Open Follow-Up

The migration currently needs a source snapshot because redb refuses opening
the live v0.2 database while the production daemon holds the lock. That is
acceptable for this hard migration, but the durable upgrade path should use a
daemon-mediated snapshot/export or the full handover protocol rather than a
manual stop-copy-start step.
