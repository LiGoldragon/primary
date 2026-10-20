<!-- to-the-living:start -->
Presentation.{ «Nothing is installed by hand» }

# Nothing is installed by hand

### Proposal 1: psyche-context › vision/criomos.md

**Comment** Under CriomOS, after the line that forbids editing a file on a host: every program and service comes from its declaration. The figure shows the single road to a host.

  CriomOS is a declarative operating system: nobody edits a file on a host.
+
+ Nothing is installed by hand: every program and service on a host comes from its declaration, deployed through CriomOS; no file is placed in ~/.local/bin or a nix profile.
  
  A problem in CriomOS is fixed in CriomOS by a proper fix and a proper deploy.

```
+------------------+    +------------------+
| declaration      |    | hand install:    |
| (CriomOS, Home)  |    | ~/.local/bin,    |
+------------------+    | nix profile,     |
        |               | hand-linked unit |
        | is deployed   +------------------+
        | by                    |
        v                       | is destroyed
+------------------+            | and replaced by
| lojix activation |<-----------+
+------------------+
        |
        | is the only source of
        v
+------------------+
| every program    |
| and service on   |
| a host           |
+------------------+
```

### Proposal 2: psyche-context › vision/criomos.md

**Comment** What is found on a host against the line above is not kept and not repaired in place: it is destroyed, and the declared deployment replaces it.

  CriomOS is a declarative operating system: nobody edits a file on a host.
+
+ A stateful installation found on a host is destroyed and replaced by its declared deployment.
  
  A problem in CriomOS is fixed in CriomOS by a proper fix and a proper deploy.

## psyche-context › vision/criomos.md

## CriomOS

CriomOS is a declarative operating system: nobody edits a file on a host.

A problem in CriomOS is fixed in CriomOS by a proper fix and a proper deploy.
Every hotfix in place is removed and replaced by that fix.

CriomOS is made more modular; an anatomy of it shows what should be taken out.

## Nix code

Every store path in Nix code is the output of evaluating a package, a flake input or an option; Nix code never names a store path.

## Hardware

CriomOS has a hardware type, so that it supports several kinds of hardware, the Librem 5 Linux smartphone among them; a module may be gated on it.
A fix that only some hardware needs is a value in the cluster data, marked by the chip or part that makes it necessary.
A library reads the cluster's list of its hardware and answers, by processor, model and variant, which fixes a computer needs.

## Harnesses

The harnesses and their desktop apps are kept stock in at least one version, under their ordinary executable names.

## Services

A new service lives in CriomOS.
A service is updated by bringing it up at its latest version.

## Desktop

A new artifact does not open a browser tab on its own.

## psyche-context › vision/deployment.md

## A proof of concept deploys on the flow's own host

A proof of concept is worked on and deployed on the host the flow is
running on. Another host is used only when the living names it.

## A stable node is not used for testing

Zeus is a stable node, and stable nodes are not where testing
happens.

## psyche-context › vision/nix-builds.md

## Nix builds

Nix builds live in the remote builder's store. A machine keeps links only to the profiles in use on it. A Nix build worth keeping is listed in one registry profile; every other Nix build is collected by how recently and how often it was used.

## Sources

d68c82 builds

## mind-context › knowledge/lojix.md

`lojix-nexus` owns durable state and two authority-tiered sockets. The ordinary contract is `signal-lojix`; the owner contract is `meta-signal-lojix`.

Use `lojix` on the ordinary socket for `Query`, `WatchDeployments`, `WatchCacheRetention`, and `Unwatch`.

Use `lojix-meta` on the owner socket for `Deploy`, `Pin`, `Unpin`, `Retire`, and `Test`. The owner contract is not optional.

Use `LOJIX_ORDINARY_SOCKET` and `LOJIX_OWNER_SOCKET`; neither socket has a default path.

## Request syntax

Each public client accepts exactly one inline datom value and rejects files, flags, subcommands, zero arguments, and extra arguments. A request root is one value.

A struct is brace-enclosed and positional, a vector is bracket-enclosed, a variant is a head with the period glued to both sides, and a variant carrying nothing is bare. `None` is bare and `Some` carries one glued payload. A string with a space or a delimiter is written in guillemets.

```text
Variant.{ field0 field1 field2 }
[ field0 field1 ]
Some.Value
«alpha beta»
```

Never name a field in a request; the position carries the data.

## Ordinary requests

`Query` carries `ByNode`, `ByGeneration`, `ByDeployment`, `ByEventLog`, or `ByTestRun`.

`ByNode` has, in order:

1. cluster name
2. node name
3. optional requested generation artifact

Exact witnessed form:

```sh
lojix 'Query.ByNode.{ alpha node-1 None }'
```

`ByGeneration` carries one generation identifier.

`ByDeployment` carries one deployment identifier.

`ByEventLog` has, in order:

1. first event-log position
2. last event-log position

`ByTestRun` has, in order:

1. cluster name
2. node name
3. optional test-run identifier

`WatchDeployments` has, in order:

1. optional deployment identifier
2. optional cluster name
3. optional node name

The all-target schema-derived form is:

```sh
lojix 'WatchDeployments.{ None None None }'
```

`WatchCacheRetention` has, in order:

1. optional cluster name
2. optional node name

The all-target schema-derived form is:

```sh
lojix 'WatchCacheRetention.{ None None }'
```

A successful watch request returns:

```text
Watching.{ subscription-token commit-sequence }
```

A rejection is `WatchRejected.MalformedWatch`, `WatchRejected.SubscriptionLimitReached`, or `WatchRejected.StreamUnavailable`.

The current `lojix` executable exchanges one request for one reply and exits. It cannot consume ongoing subscription events. Do not use it as a streaming terminal monitor; re-query with `Query.ByDeployment` or `Query.ByEventLog`.

`Unwatch` carries one subscription token.

## Owner requests

`Deploy.Host` has, in order:

1. cluster name
2. node name
3. host composition
4. proposal source
5. secrets input
6. flake reference
7. deployment transport
8. deployment input mode
9. deployment output selector
10. activation backend
11. host deploy action
12. source revision policy
13. optional Nix builder
14. extra substituters

`Deploy.UserEnvironment` has, in order:

1. cluster name
2. node name
3. user name
4. proposal source
5. secrets input
6. flake reference
7. deployment transport
8. deployment input mode
9. deployment output selector
10. activation backend
11. user-environment action
12. source revision policy
13. optional Nix builder
14. extra substituters

A deployment transport is the positional product of:

1. Nix store URI
2. SSH destination

A deployment output selector is a one-field positional product.

An optional builder is `None` or `Some` carrying its string.

Extra substituters are a vector of two-string positional products.

Host compositions are `CompleteHost` and `BaseHost`.

Host deploy actions are `Evaluate`, `Realize`, `SetBootProfile`, `ActivateNow`, `TestActivation`, and `ScheduleBootOnce`.

User-environment actions are `Realize`, `SetProfile`, and `ActivateNow`.

Deployment input modes are `Horizon` and `Direct`.

Activation backends are `NixosSystemdBootV1` and `HomeManagerNixProfileV1`.

Source revision policies are `RequireImmutable` and `ResolveAndRecord`.

`Pin` has, in order:

1. cluster name
2. node name
3. generation identifier
4. pin label

Exact witnessed form:

```sh
lojix-meta 'Pin.{ alpha node-1 42 keep }'
```

`Unpin` has, in order:

1. cluster name
2. node name
3. pin label

`Retire` has, in order:

1. cluster name
2. node name
3. generation identifier

`Test` carries `Run` or `Check`.

`Test.Run` has, in order:

1. cluster name
2. node selection
3. host selection
4. test execution profile

A node selection is bare `All` or `Nodes` carrying a node-name vector.

A host selection is bare `DefaultHost` or `OnHost` carrying a node name.

A test execution profile has, in order:

1. test mode
2. Nix system
3. deployment output selector
4. optional deployment transport

`Test.Check` carries a node-name vector.

## Replies and terminal state

Ordinary reply families are `Queried`, `DeploymentEventsQueried`, `TestRunsQueried`, `Watching`, `Unwatched`, `QueryRejected`, `WatchRejected`, and `UnwatchRejected`.

Owner reply families are `DeployAccepted`, `DeployRejected`, `DeployTerminal`, `Pinned`, `PinRejected`, `Unpinned`, `UnpinRejected`, `Retired`, `RetireRejected`, `Tested`, and `TestRejected`.

`DeployAccepted` has, in order:

1. deployment identifier
2. state marker

Exact witnessed reply:

```text
DeployAccepted.{ 13 { 263 263 } }
```

`DeployAccepted` is admission only. It does not prove evaluation, build, copy, activation, or completion.

`DeployTerminal` carries the terminal deployment record.

A deployment terminal is bare `Succeeded`, `Rejected` carrying a terminal reason, or `Failed` carrying failure stage and terminal reason.

Exact witnessed failed-activation form:

```text
Some.Failed.{ Activate ActivationFailed }
```

`Pinned` and `Unpinned` carry generation identifier, pin label, source slot, destination slot, and state marker.

`Retired` carries generation identifier, generation slot, and state marker.

`Tested` carries test-run identifier and state marker.

After `DeployAccepted`, re-query by deployment identifier or event-log position until a terminal deployment record exists.

## Deployment contract

Every deployment transport is explicit. Lojix uses the supplied Nix store URI and SSH destination verbatim; it never derives a route from cluster, node, or user names.

The logical node selects what is built; the activation destination selects which machine is changed. Before a state-changing deployment, verify that they identify the same node. If they do not, stop.

A `CompleteHost` deployment uses an explicit root-privileged Nix store URI and SSH destination.

A `UserEnvironment` deployment uses an explicit user-scoped Nix store URI and SSH destination.

When a deployment directly names a target pair, use it without asking for a second transport confirmation. Otherwise derive the canonical internal hostname as `<node>.<cluster>.<internal suffix>` from Horizon cluster data and use it as the host in the required `CompleteHost` or `UserEnvironment` Nix store URI and SSH destination. If the supplied or derived pair is invalid, report it rather than substituting another route.

A deployment proposal must be an existing absolute regular non-symlink `horizon-definition.datom` file.

Use `RequireImmutable` when production deployment must identify one exact source revision. Push producer revisions before pushing the consumer revision that pins them.

A `Current` generation is Lojix's committed state. It does not establish the target's live Nix profile or runtime links.

A terminal activation failure can follow a partial target change. Inspect the target profile, runtime links, and activation journal, then report Lojix state and live state separately.

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

## Placement

Keep Lojix configuration in the operating-system source. Do not add setup-specific deployment scripts to the user environment.

The supported deployment and observation interface is `lojix` and `lojix-meta`; setup-specific wrapper scripts are not an alternative interface.

### Proposal 3: field-context › compensation/operating-system.md

**Comment** Alternative to Proposal 4; the living lands one. The vision line that replaces this one is in psyche-context › vision/criomos.md: "Every hotfix in place is removed and replaced by that fix", with Proposals 1 and 2 above. This alternative removes the whole line: the approval for a reboot goes with the approval for a runtime mutation.

  Use existing deployment authorization once concrete artifact and execution prerequisites are satisfied; require separate release approval only if the living explicitly imposed it.
  
- Require explicit psyche approval before a reboot or emergency runtime mutation.

### Proposal 4: field-context › compensation/operating-system.md

**Comment** Alternative to Proposal 3; the living lands one. This alternative removes only the emergency runtime mutation, which the same vision line ("Every hotfix in place is removed and replaced by that fix") and Proposals 1 and 2 leave no place for, and keeps the approval for a reboot.

  Use existing deployment authorization once concrete artifact and execution prerequisites are satisfied; require separate release approval only if the living explicitly imposed it.
  
- Require explicit psyche approval before a reboot or emergency runtime mutation.
+ Require explicit psyche approval before a reboot.

### Proposal 5: field-context › compensation/update.md

**Comment** A service is updated by coming up at its latest version, so promotion no longer preserves the running process: the vision line that replaces this one is "A service is updated by bringing it up at its latest version" in psyche-context › vision/criomos.md, with Proposal 2. The rest of the module stays.

  Migrate every consumer in scope to the Next role through its declared configuration. Preserve the predecessor stable endpoint until migration is proved.
  
  Retain an exact migration artifact that identifies every native consumer in scope and its resolved role mapping. It must prove that none resolves predecessor stable. Source declarations, staged paths, successful evaluation, or intended configuration do not prove migration.
  
- After the migration gate, promote by mapping stable to the already-running Next endpoint. Preserve its process, service, socket, state root, client route, and running sessions. Do not restart, recreate, rename, move, copy, or share its mutable state as part of promotion.
+ After the migration gate, promote by mapping stable to the already-running Next endpoint.
  
  Create separate Next only after promotion. Give it a distinct process, state root, socket, and client route.

### Proposal 6: field-context › compensation/agent-harness-packaging.md

**Comment** Both lines are what Proposal 1 says: a program and its configuration come from their declaration, and nothing is placed on a host by an installer. The vision line that replaces them is Proposal 1, with "nobody edits a file on a host" in psyche-context › vision/criomos.md.

  Treat an external harness manager as distinct from the Claude or Codex harnesses it coordinates.
  
  Obtain current release, packaging, installation, and integration facts from authoritative upstream sources before choosing or changing an integration.
  
- Put durable packages and configuration in the declarative source that owns that environment.
  
  Put a distinct reusable package in its own public package repository; a home-environment source consumes a pinned package output.
  
  Give an agent manager a package and executable name that cannot collide with an unrelated existing package; StablyAI Orca is `orca-ide`, not GNOME `orca`.
  
- Do not run an upstream integration installer that mutates a configuration Nix owns; express the intended configuration in its declarative owner.
  
  Evaluation is not package proof: build the artifact and behavior-smoke every claimed CLI, GUI, and headless surface.

### Proposal 7: field-context › compensation/nix-workflow.md

**Comment** An environment part owned by CriomOS or CriomOS-home is maintained through its declaration: the vision line that replaces this one is Proposal 1, with "A problem in CriomOS is fixed in CriomOS by a proper fix and a proper deploy" in psyche-context › vision/criomos.md.

  Ask Nix or source, not the store filesystem.
- Any part of an environment already owned by Nix, CriomOS, or CriomOS-home is fixed, updated, and maintained through that owning declarative source.
  Keep local overrides transient.
  Run Nix evaluations and builds independently.

<!-- to-the-living:end -->
