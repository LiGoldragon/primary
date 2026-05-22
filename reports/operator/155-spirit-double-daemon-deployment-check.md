# Spirit double-daemon deployment check

## Result

The double-daemon deployment is present and mostly matches the intended shape.
Both versioned daemons are active, the unsuffixed `spirit` command resolves to
`spirit-v0.1.0`, and versioned state directories/sockets exist.

The deployment is **not ready to flip** yet because `v0.1.1` is currently
serving an empty database, not a migrated copy of the live `v0.1.0` database.

## What is running

`systemctl --user list-units 'persona-spirit*'` shows:

```text
persona-spirit-daemon-v0.1.0.service  active running
persona-spirit-daemon-v0.1.1.service  active running
persona-spirit-daemon.service         not-found inactive dead
```

The running daemon commands are:

```text
persona-spirit-daemon (.../v0.1.0/spirit.sock .../v0.1.0/owner.sock .../v0.1.0/persona-spirit.redb 384 None)
persona-spirit-daemon (.../v0.1.1/spirit.sock .../v0.1.1/owner.sock .../v0.1.1/persona-spirit.redb 384 None)
```

The command resolution is:

```text
spirit        -> spirit-v0.1.0
spirit-v0.1.0 -> versioned v0.1.0 wrapper
spirit-v0.1.1 -> versioned v0.1.1 wrapper
```

That matches the intended initial deployment: old version remains default while
new version is staged.

## Database state

Current state paths:

```text
~/.local/state/persona-spirit/v0.1.0/persona-spirit.redb
~/.local/state/persona-spirit/v0.1.1/persona-spirit.redb
```

The old version is live and receiving writes. I logged record 128 through the
unsuffixed `spirit`, and it appears in `spirit-v0.1.0` queries.

The new version is reachable, but its query surface shows no migrated records:

```text
spirit-v0.1.1 '(Observe Topics)'
# => (TopicsObserved ([]))

spirit-v0.1.1 '(Observe (Records ((Some deploy) None SummaryOnly)))'
# => (RecordsObserved ([]))
```

So `v0.1.1` is alive, but its database is not the migrated production state.

## Nix migration sandbox

I reran the Nix-owned live sandbox against the versioned production database:

```sh
nix run --max-jobs 0 /git/github.com/LiGoldragon/sema-upgrade#spirit-migration-sandbox -- \
  /home/li/.local/state/persona-spirit/v0.1.0/persona-spirit.redb
```

It succeeded:

```text
(UpgradeCompleted (persona-spirit (0 1 0) (0 1 1) persona-spirit-0-1-0-to-0-1-1 128))
(SandboxMigrationSucceeded ("/home/li/.local/state/persona-spirit/v0.1.0/persona-spirit.redb"))
```

The sandbox also started a temporary v0.1.1 daemon, queried migrated topics,
wrote a sandbox-only `High` record, and queried it back.

This proves the latest `v0.1.0` database can still be migrated cleanly. It does
not change the staged `v0.1.1` production database.

## Transition Readiness

Not ready to flip the default yet.

Safe next transition shape:

1. Temporarily freeze writes to v0.1.0, or accept a short stop-old/start-new
   window.
2. Stop `persona-spirit-daemon-v0.1.1.service`.
3. Run the sema-upgrade migration from
   `v0.1.0/persona-spirit.redb` to a fresh temporary v0.1.1 database path.
4. Atomically move the migrated database into
   `v0.1.1/persona-spirit.redb`.
5. Start `persona-spirit-daemon-v0.1.1.service`.
6. Verify with explicit `spirit-v0.1.1` queries.
7. Switch the Home Manager default from `v0.1.0` to `v0.1.1`.

Without a freeze or high-water-mark replay, a migration copied while v0.1.0 is
still accepting writes can miss late records. The current sema-upgrade prototype
has copy-migrate-verify, not delta replay.
