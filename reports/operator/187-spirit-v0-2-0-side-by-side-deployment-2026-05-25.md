# 187 — Spirit v0.2.0 Side-by-Side Deployment

## Summary

Deployed Spirit v0.2.0 as a side-by-side Home Manager service and CLI
wrapper on `ouranos`. The unversioned `spirit` command still resolves to
v0.1.0, so production intent capture remains on the existing database.
The new v0.2.0 daemon runs against its own segregated database under the
versioned state directory and is ready for explicit test usage through
`spirit-v0.2.0`.

## Landed Versions

- `persona-spirit` main: `ba1956d23217`
- `persona-spirit` tag: `v0.2.0 -> ba1956d23217`
- `CriomOS-home` main: `760c1a717506`

The GitHub remote for the Spirit daemon repo is still
`git@github.com:LiGoldragon/persona-spirit.git`. The repo/package rename
to `spirit` remains future work under the rename/cutover bead chain.

## CriomOS-home Changes

`CriomOS-home` now has a third versioned Spirit input:

- `persona-spirit-v0-2-0.url = github:LiGoldragon/persona-spirit?ref=v0.2.0`

The `criomosHome.personaSpirit` module now accepts:

- `v0.1.0`: production/current default, with upgrade socket
- `v0.1.1`: older side-by-side version, without upgrade socket
- `v0.2.0`: new description-only Spirit, with upgrade socket and the new
  nine-field daemon configuration shape

The versioned wrapper installed by the module is `spirit-v0.2.0`; it
points at:

- ordinary socket:
  `/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock`
- owner socket:
  `/home/li/.local/state/persona-spirit/v0.2.0/owner.sock`
- database:
  `/home/li/.local/state/persona-spirit/v0.2.0/persona-spirit.redb`

## Nix Witnesses

Passed:

```sh
nix build --option max-jobs 0 \
  .#checks.x86_64-linux.persona-spirit-versioned-deployment \
  --print-out-paths
```

Result:

```text
/nix/store/wxxpnqb0pb4rksa7gj2km9p7wny5ly3c-persona-spirit-versioned-deployment
```

The check asserts:

- v0.2.0 service exists
- `spirit-v0.2.0` wrapper exists
- v0.2.0 daemon `ExecStart` points at the versioned database
- v0.2.0 daemon `ExecStart` includes the versioned upgrade socket
- unversioned `spirit` remains v0.1.0

Home build passed:

```sh
lojix-cli '(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "path:/git/github.com/LiGoldragon/CriomOS-home" Build None None)'
```

Activation passed:

```sh
lojix-cli '(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "path:/git/github.com/LiGoldragon/CriomOS-home" Activate None None)'
```

The activation output included:

```text
Starting units: persona-spirit-daemon-v0.2.0.service
```

## Live State

`persona-spirit-daemon-v0.2.0.service` is active:

```text
Active: active (running)
ExecStart:
/nix/store/.../persona-spirit-daemon/bin/persona-spirit-daemon
("/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock"
 "/home/li/.local/state/persona-spirit/v0.2.0/owner.sock"
 "/home/li/.local/state/persona-spirit/v0.2.0/upgrade.sock"
 "/home/li/.local/state/persona-spirit/v0.2.0/persona-spirit.redb"
 384 None None None None)
```

The v0.1.0 production daemon remains active, and the profile still maps:

```text
spirit -> spirit-v0.1.0
spirit-v0.1.0 -> installed
spirit-v0.1.1 -> installed
spirit-v0.2.0 -> installed
spirit-next -> missing
```

That is intentional for this slice: explicit `spirit-v0.2.0` testing is
enabled, but the default production command remains v0.1.0.

## Live Usage Proof

Record into the v0.2.0 database:

```sh
spirit-v0.2.0 '(Record (spirit Clarification [deployed spirit v0.2.0 accepts description only records] Maximum))'
```

Reply:

```text
(RecordAccepted 1)
```

The reply is terse and does not echo the whole entry back.

Transferred the newest production summaries 690-697 into v0.2.0 as
description-only records, then queried:

```sh
spirit-v0.2.0 '(Observe Topics)'
spirit-v0.2.0 '(Observe (Records ((Some schema) None DescriptionOnly)))'
spirit-v0.2.0 '(Observe (Records (None (Some Decision) DescriptionOnly)))'
spirit-v0.2.0 '(Observe (Records ((Some spirit) (Some Constraint) DescriptionOnly)))'
```

Observed topic counts:

```text
(TopicsObserved ([(nota 1) (schema 3) (signal 1) (spirit 3) (workspace 1)]))
```

The topic and kind filters both returned the expected subsets.

## Notes

`lojix-cli` itself still uses the older quoted-string NOTA reader. The
deploy commands therefore used quoted strings for `lojix-cli` paths. The
new Spirit v0.2.0 usage proof used bracket strings.

This is not a production cutover. It is a side-by-side deployment of the
new Spirit substrate for explicit testing.
