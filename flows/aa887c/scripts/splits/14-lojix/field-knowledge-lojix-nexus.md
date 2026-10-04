---
description: The deployed Lojix Nexus must be configured, started, inspected, reset or bootstrapped: its sockets, startup archive, or store.
dependencies: [nix-workflow]
---

Use `LOJIX_ORDINARY_SOCKET` and `LOJIX_OWNER_SOCKET`; neither socket has a default path.

## Startup configuration

The Nexus does not accept operator requests. `lojix-write-configuration` is the datom-to-startup boundary and writes the archive consumed by `lojix-nexus`.

Its single request is the `ConfigurationWriteRequest` struct with:

1. ordinary socket path
2. ordinary socket mode
3. owner socket path
4. owner socket mode
5. state directory
6. store path
7. Nexus host
8. test-default choice
9. output path

Exact tested form:

```text
ConfigurationWriteRequest.{ /run/fixture-lojix/ordinary.sock 432 /run/fixture-lojix/owner.sock 384 /var/lib/fixture-lojix /var/lib/fixture-lojix/configured-lojix-store.db fixture-nexus NoTestDefaults /tmp/startup.rkyv }
```

Production uses bare `NoTestDefaults`.

The nested development form is `TestDefaults` with, in order:

1. cluster name
2. VM host
3. mode
4. flake
5. Nix system
6. output selector
7. proposal source

Success prints:

```text
ConfigurationWritten.[ path ]
```

## Store inspection and reset

Inspect a store read-only with exactly:

```sh
lojix-inspect-store 'InspectStore.{ /tmp/lojix.sema }'
```

Inspection does not create or register missing tables.

Reset accepts only:

```sh
lojix-reset-store 'ResetStore'
```

It takes no path. Store selection comes from the service-owned `LOJIX_CONFIGURATION` archive.

Stop the Nexus before reset.

The Nexus accepts schema v5 and refuses earlier schemas. Reset removes and recreates recognized v2/v3/v4 stores as v5. An existing v5 store is left intact.

Successful reset replies are:

```text
LojixStoreReset.{ path 5 count }
LojixStoreAlreadyCurrent.{ path 5 }
```

Reset is destructive for a recognized v2/v3/v4 store.

## Bootstrap

`lojix-bootstrap` is a separate Nexus-free ingress. It accepts exactly one inline `BootstrapRun` value and does not read Nexus sockets, configuration, or store state.

`BootstrapRun` is a struct with:

1. request identifier
2. bootstrap mode

`BuildOnly` carries:

1. direct immutable build request
2. optional builder
3. journal parent
4. GC root
5. terminal-evidence path

The direct immutable build request carries:

1. immutable flake
2. Nix system
3. output selector

`BootOnce` additionally carries a test plan and either `RemoteNixosSystemdBootV1` or `LocalBootstrapV1`.

`RemoteNixosSystemdBootV1` carries:

1. Nix store URI
2. SSH destination
3. SSH policy
4. system profile
5. boot entries

Its SSH policy carries caller-owned identity, caller-owned known-hosts, and bare `RequireKnownHost`. Ambient SSH configuration is not accepted.

`LocalBootstrapV1` carries:

1. system profile
2. boot entries

Bootstrap immutable flakes use:

```text
github:owner/repository/40-lowercase-hex-revision
```

This differs from Nexus deployment flake syntax.

Terminal output is bare `BootstrapTerminal.Succeeded` or `BootstrapTerminal.Failed`. Parse or validation failure prints a redacted `BootstrapRejected.[ … ]`.
