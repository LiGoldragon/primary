# New Spirit Production OS Cutover Investigation — 2026-06-09

## Question

The question was how to switch the production Spirit used by the OS from the deployed `persona-spirit` stack to the new schema-derived `spirit`, with tests backing the claims.

This is an investigation report, not a live cutover. I did not change the OS service or stop the production daemon.

## Current Production Shape

The installed `spirit` command is still the versioned `persona-spirit` profile:

- `command -v spirit` -> `/home/li/.nix-profile/bin/spirit`
- resolved target -> `/nix/store/...-spirit-v0.5.2/bin/spirit-v0.5.2`

The user session currently runs side-by-side versioned daemons:

- `persona-spirit-daemon-v0.1.0.service`
- `persona-spirit-daemon-v0.1.1.service`
- `persona-spirit-daemon-v0.2.0.service`
- `persona-spirit-daemon-v0.3.0.service`
- `persona-spirit-daemon-v0.4.0.service`
- `persona-spirit-daemon-v0.4.1.service`
- `persona-spirit-daemon-v0.4.2.service`
- `persona-spirit-daemon-v0.5.0.service`
- `persona-spirit-daemon-v0.5.1.service`
- `persona-spirit-daemon-v0.5.2.service`
- `persona-spirit-daemon-next.service`

The relevant Home Manager module is:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`

That module is built around the old repo shape:

- flake inputs are named `persona-spirit-v0-*` and `persona-spirit-next`
- daemon package is `packages.${system}.persona-spirit-daemon`
- daemon binary is `persona-spirit-daemon`
- unsuffixed `spirit` is a symlink to the selected version wrapper
- current default is `v0.5.2`
- state lives under `~/.local/state/persona-spirit/<version>/`
- production database is `persona-spirit.redb`
- daemon startup argument is inline NOTA text

The current state path for production is:

- `~/.local/state/persona-spirit/v0.5.2/persona-spirit.redb`
- `~/.local/state/persona-spirit/v0.5.2/spirit.sock`
- `~/.local/state/persona-spirit/v0.5.2/owner.sock`
- `~/.local/state/persona-spirit/v0.5.2/upgrade.sock`

## New Spirit Package Shape

The new repo is:

- `/git/github.com/LiGoldragon/spirit`

The flake exposes:

- `packages.default`: combined package with `bin/spirit` and `bin/spirit-daemon`
- `packages.cli`: CLI only
- `packages.daemon`: daemon only
- `packages.trace`: trace-capable combined package
- `apps.nix-integration-tests`

The daemon binary is `spirit-daemon`, not `persona-spirit-daemon`.

The new daemon startup contract is deliberately different from old production:

- the daemon accepts exactly one argument
- that argument is a path to a signal-encoded rkyv `Configuration`
- the daemon does not parse NOTA at startup
- the configuration carries working socket, meta socket, database path, and optional trace socket

The new production database type is `.sema`, not `.redb`.

## Important Cutover Decision

The psyche clarified during this investigation:

> just prebuild the configuration.rkyv

Captured as Spirit record `u4st`: new Spirit production deployment should prebuild `configuration.rkyv` and pass that binary configuration path to the daemon; the daemon remains binary-only and does not parse NOTA at startup.

That is the correct shape. The Home Manager module should materialize `configuration.rkyv` ahead of daemon start, then `ExecStart` should call:

```sh
spirit-daemon /path/to/configuration.rkyv
```

Nix should not hand-encode rkyv bytes itself. The deployment should use a tiny package-provided writer binary or build-time helper linked against the `spirit` library to create the binary file from Nix-known paths.

## Tested

### Current OS Deployment Check

Command:

```sh
nix build /git/github.com/LiGoldragon/CriomOS-home#checks.x86_64-linux.persona-spirit-versioned-deployment -L
```

Result: passed.

Meaning: the current `persona-spirit` Home Manager versioned service/profile shape still evaluates and builds.

### New Spirit Flake Surface

Command:

```sh
nix flake show /git/github.com/LiGoldragon/spirit --allow-import-from-derivation
```

Result: passed.

Meaning: the new flake exposes the expected package/check/app surface.

### New Spirit Package Build

Command:

```sh
nix build /git/github.com/LiGoldragon/spirit#default -L
```

Result: failed.

The failure is not the earlier “builder unreachable” failure. The remote builder was reached and began compiling. The failure is that the Nix build is not fully closed over the Cargo Git dependency graph:

```text
failed to get `signal-frame` as a dependency of package `signal-spirit`
unable to update https://github.com/LiGoldragon/signal-frame.git?branch=main
failed to resolve address for github.com
```

The immediate source is `signal-spirit` as an optional Git dependency for the `production-migration` feature. Even without building the migration binary, Cargo still tries to resolve enough of that Git dependency path during the derivation. The flake vendors several local workspace repos, but not `signal-spirit`, so the package can still hit the network inside the build.

This blocks OS cutover until fixed. Production deployment should not rely on GitHub DNS from inside a derivation.

### Binary Configuration Contract

Command:

```sh
cargo test --all-features --test daemon_command -- --nocapture
```

Result: passed, 3 tests.

Coverage:

- daemon accepts exactly one binary configuration file argument
- daemon rejects missing/extra arguments
- configuration carries the required meta socket slot

### Production Database Sandbox

Command:

```sh
SPIRIT_PRODUCTION_DATABASE="$HOME/.local/state/persona-spirit/v0.5.2/persona-spirit.redb" \
  cargo test --all-features --test production_database_sandbox -- --ignored --test-threads=1
```

Result: passed, 3 tests.

Coverage:

- copied production database is not directly usable as the new store without explicit migration
- production migration binary preserves production record identifiers
- migrated production records remain queryable in new Spirit

This proves the data side is ready enough for a sandboxed migration test. It does not by itself prove the OS cutover module is ready.

## How I Would Switch Production

### Step 1 — Fix New Spirit Nix Closure

Before touching Home Manager, make `nix build .#default` pass in `/git/github.com/LiGoldragon/spirit`.

Required fix:

- add `signal-spirit-source` as a flake input or remove the optional Git dependency from the default build closure
- vendor/patch `signal-spirit` the same way the flake already vendors `nota-next`, `schema-next`, `schema-rust-next`, `sema`, `sema-engine`, `signal-frame`, `signal-sema`, and `triad-runtime`
- patch nested `signal-spirit` dependencies so it uses the vendored `signal-frame` rather than fetching GitHub during the derivation
- include a Nix check that catches remaining Git fetches

Acceptance test:

```sh
nix build /git/github.com/LiGoldragon/spirit#default -L
```

### Step 2 — Add a Config Archive Writer

Add a small installed helper to the `spirit` package, for example:

- `spirit-write-configuration`

Inputs should be paths already known to the deployment:

- working socket path
- meta socket path
- database path
- optional trace socket path
- output path

Output:

- binary rkyv `Configuration`

The daemon still receives no NOTA and no flags. This helper is a deployment/build helper, not the daemon.

Acceptance test:

- helper writes `configuration.rkyv`
- `spirit-daemon configuration.rkyv` starts and binds both sockets
- missing meta socket is rejected

### Step 3 — Add New Spirit as a Home Manager Deployment Family

The current `spirit.nix` module can either be replaced or extended.

I would not overload `persona-spirit-next`. The new repo is no longer “persona-spirit next”; it is `spirit`. Add a new deployment family:

- input: `spirit`
- service: `spirit-daemon`
- working socket: `~/.local/state/spirit/current/spirit.sock` or a versioned equivalent
- meta socket: `~/.local/state/spirit/current/meta-spirit.sock`
- database: `~/.local/state/spirit/current/spirit.sema`
- config archive: `~/.local/state/spirit/current/configuration.rkyv`

If retaining side-by-side rollback, use a versioned directory:

- `~/.local/state/spirit/v0.3.0/spirit.sema`
- `~/.local/state/spirit/v0.3.0/configuration.rkyv`

The unsuffixed `spirit` wrapper should export:

```sh
SPIRIT_SOCKET=/home/li/.local/state/spirit/<version>/spirit.sock
```

Then call:

```sh
spirit "$@"
```

The wrapper should not export `PERSONA_SPIRIT_SOCKET`; new Spirit uses `SPIRIT_SOCKET`.

### Step 4 — Migrate Data Once

The deployment should not directly point the new daemon at `persona-spirit.redb`.

On first activation, if the new `.sema` store does not exist and the selected production `persona-spirit.redb` exists, run:

```sh
spirit-migrate-production "([/home/li/.local/state/persona-spirit/v0.5.2/persona-spirit.redb] [/home/li/.local/state/spirit/<version>/spirit.sema])"
```

The migration helper is a CLI/human-edge tool and may parse NOTA. The daemon still may not.

The current sandbox test proves this migration can preserve record identifiers and query migrated records.

### Step 5 — Run New Daemon Side By Side

Do not replace the unsuffixed `spirit` command first.

Start the new daemon under a separate service and socket:

- `spirit-daemon-current.service`, or
- `spirit-daemon-v0.3.0.service`

Keep old `persona-spirit-daemon-v0.5.2.service` running until the new one passes live smoke tests.

Smoke tests:

- `Record`
- `Observe`
- `PublicRecords`
- `PrivateRecords`
- `ChangeRecord`
- `ChangeCertainty`
- `RemoveRecord`
- `SubscribeIntent`
- meta `Configure`
- `CollectRemovalCandidates` against a separate archive `.sema`

### Step 6 — Flip Unsuffixed `spirit`

Only after side-by-side smoke passes:

- change Home Manager’s unsuffixed `spirit` symlink/wrapper to the new package
- keep `spirit-v0.5.2` available for rollback
- leave old versioned daemons running until confidence is high enough to disable them

## Not Ready Yet

The new Spirit runtime/data path is close, but OS production cutover is not yet ready because:

1. `nix build /git/github.com/LiGoldragon/spirit#default` currently fails due an unclosed Git dependency path through `signal-spirit`.
2. The package does not yet expose a production config-archive writer, so Home Manager has no clean way to prebuild `configuration.rkyv`.
3. `CriomOS-home` still models Spirit as `persona-spirit` versions only; it needs a new `spirit` deployment family or a deliberate replacement of the profile.
4. The service name, binary name, environment variable, state directory, database suffix, and startup argument all change.

## Recommendation

Do the switch in two implementation commits before live cutover:

1. `spirit`: make the flake closed/reproducible and ship `spirit-write-configuration`; prove `nix build .#default`.
2. `CriomOS-home`: add a new side-by-side `spirit` deployment that prebuilds `configuration.rkyv`, migrates `persona-spirit.redb` to `spirit.sema` if needed, starts `spirit-daemon`, and exposes an opt-in wrapper before changing the unsuffixed `spirit`.

After those land, run the side-by-side service against a copied/migrated production database and only then flip the unsuffixed command.
