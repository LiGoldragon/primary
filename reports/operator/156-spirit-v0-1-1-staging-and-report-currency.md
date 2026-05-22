# Spirit v0.1.1 staging and report currency

Report kind: implementation status
Topic: Spirit v0.1.1 database staging, operator report currency, remaining cutover gap
Date: 2026-05-22
Lane: operator

## Result

Spirit v0.1.1 is no longer an empty staged daemon. The v0.1.1 state path now
contains a migrated copy of the v0.1.0 Spirit database, and the v0.1.1 daemon
is running against it.

Current state:

- `persona-spirit-daemon-v0.1.0.service` is active.
- `persona-spirit-daemon-v0.1.1.service` is active.
- unsuffixed `spirit` still resolves to `spirit-v0.1.0`.
- `spirit-v0.1.1` sees migrated records through record 146.
- the v0.1.1 staged database was installed at
  `/home/li/.local/state/persona-spirit/v0.1.1/persona-spirit.redb`.
- backups were left beside it:
  `/home/li/.local/state/persona-spirit/v0.1.1/persona-spirit.redb.backup-20260522100213`
  and
  `/home/li/.local/state/persona-spirit/v0.1.1/persona-spirit.redb.backup-20260522100422`.

The migration was done through a Nix-owned app, not an ad hoc shell migration.

## Intent captured first

The prompt's durable intent was logged into production Spirit before the work:

- 135: operator watches new designer reports.
- 136: operator and second operator are one identity.
- 137: agent checkout should drive commits.
- 138: claims start from clean checkout.
- 139: unversioned spirit should dual-write during migration.
- 140: old spirit should redirect after safe dual write.
- 141: Spirit CLI should be one inline NOTA call.
- 142: NOTA CLI syntax must stay shell safe.
- 143: operators read peer operator reports first.
- 144: track which reports were read.
- 145: start using Spirit v0.1.1 after database update.

Record 146 appeared after the first staging pass from another live writer:
`ItemPriority in signal-persona-mind collapses onto signal_sema::Magnitude`.
That live write forced a second staging pass and demonstrated the remaining
write-synchronization problem.

## Reports read in this pass

Operator-side first, per the new intent:

- `reports/operator/155-spirit-double-daemon-deployment-check.md`
- `reports/second-operator/165-current-situation-2026-05-22.md`
- `reports/second-operator/166-review-persona-orchestrate-migration-2026-05-22.md`
- `reports/second-operator-assistant/8-141-migration-coordination-audit.md`

Designer-side next:

- `reports/designer/280-session-handover-2026-05-22.md`
- `reports/designer/279-nota-schema-language-and-version-hash.md`
- `reports/designer/273-schema-migration-synthesis-post-operator-151.md`
- `reports/designer/270-sema-upgrade-component-design.md`

I also checked the current report listings for `reports/operator/`,
`reports/second-operator/`, `reports/designer/`, and `reports/second-designer/`
to identify the latest report surface.

## Code landed

Repo: `/git/github.com/LiGoldragon/sema-upgrade`

Commit on `main`:

```text
8434c438 sema-upgrade: add Spirit migration staging app
```

Files:

- `flake.nix`
- `README.md`
- `ARCHITECTURE.md`

New flake app:

```sh
nix run --max-jobs 0 .#spirit-migration-stage -- \
  /home/li/.local/state/persona-spirit/v0.1.0/persona-spirit.redb \
  /home/li/.local/state/persona-spirit/v0.1.1/persona-spirit.redb
```

The app:

- copies the v0.1.0 source database into a same-directory staging area;
- runs `sema-upgrade-temporary` from `(0 1 0)` to `(0 1 1)`;
- copies the migrated target into a probe database;
- starts the tagged v0.1.1 `persona-spirit-daemon` against the probe;
- verifies migrated reads;
- verifies `High` can be written and queried on the probe;
- leaves the unmodified migrated database as the persistent target;
- backs up any existing target database before the atomic rename.

The first version of the staging script wrote the `High` probe record into the
staged target itself. I fixed that before the real install: the write probe now
runs only against a copy, so the installed v0.1.1 database contains migrated
production records, not a synthetic staging record.

## Verification

Nix checks:

```sh
nix flake check --max-jobs 0 -L
```

passed in `sema-upgrade`.

Nix staging dry run:

```sh
temporary_directory=$(mktemp -d)
nix run --max-jobs 0 .#spirit-migration-stage -- \
  /home/li/.local/state/persona-spirit/v0.1.0/persona-spirit.redb \
  "$temporary_directory/persona-spirit.redb"
```

passed and printed:

```text
(UpgradeCompleted (persona-spirit (0 1 0) (0 1 1) persona-spirit-0-1-0-to-0-1-1 146))
(StageReadProbeSucceeded)
(StageWriteProbeSucceeded)
(StageInstalled (...))
```

Live staged state after restart:

- `spirit-v0.1.1 '(Observe (Records ((Some component-shape) (Some Decision) SummaryOnly)))'`
  includes record 146.
- `spirit-v0.1.1 '(Observe (Records ((Some testing) (Some Constraint) SummaryOnly)))'`
  includes only the real migrated record 127, not the synthetic staging `High`
  probe record.

## Remaining problem

The system is not atomically cut over.

Unsuffixed `spirit` still writes to v0.1.0. During this slice, another process
added record 146 to v0.1.0 after v0.1.1 had already been staged. I had to rerun
the staging app. That is acceptable as a temporary manual catch-up, but it is
not a transition protocol.

The next design/implementation decision is the user-proposed migration-aware
default:

- either the unsuffixed `spirit` wrapper dual-writes accepted write operations
  to both v0.1.0 and v0.1.1 during the migration window;
- or the default flips to v0.1.1 and v0.1.0 becomes a read-only fallback;
- or sema-upgrade gains a high-water-mark replay path before any further write
  traffic is allowed through the old default.

The prompt's latest intent leans toward dual-write plus old-version redirect:
the old path should confirm the new daemon accepted the write and then tell the
agent to stop using the old version. That is not implemented yet.

## Operational note

`tools/orchestrate status` is currently broken because the registry contains
`second-operator` but the shell helper's closed lane enum has not been updated.
I used the documented manual lock-file path for this slice:

```text
/git/github.com/LiGoldragon/sema-upgrade
[primary-x3ci]
```

This is another concrete reason to move lock/checkout state into the typed
persona-orchestrate lane registry.
