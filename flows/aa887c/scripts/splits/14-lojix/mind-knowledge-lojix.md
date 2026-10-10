---
description: A Lojix request must be constructed, submitted, observed, or interpreted.
dependencies: [nix-workflow]
---

`lojix-nexus` owns durable state and two authority-tiered sockets. The ordinary contract is `signal-lojix`; the owner contract is `meta-signal-lojix`.

Use `lojix` on the ordinary socket for `Query`, `WatchDeployments`, `WatchCacheRetention`, and `Unwatch`.

Use `lojix-meta` on the owner socket for `Deploy`, `Pin`, `Unpin`, `Retire`, and `Test`. The owner contract is not optional.

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

## Placement

Keep Lojix configuration in the operating-system source. Do not add setup-specific deployment scripts to the user environment.

The supported deployment and observation interface is `lojix` and `lojix-meta`; setup-specific wrapper scripts are not an alternative interface.
