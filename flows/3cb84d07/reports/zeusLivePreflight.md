# Zeus live preflight

## Result

Zeus is not reachable from the current Ouranos session: name resolution and
the Yggdrasil route succeed, but ICMP, TCP/22, and strict noninteractive SSH
all time out. The local Ouranos Lojix daemon is running and answers
ordinary queries, but its durable state has no committed Zeus generation or
deployment. No cluster proposal, evaluation, deployment, activation, reboot,
or runtime mutation occurred.

## What is established

### Current controller

Lojix 0.17.5 is active on Ouranos. It owns ordinary read-only queries on
`/run/lojix/ordinary.sock` and owner mutations on `/run/lojix/owner.sock`; the
service is configured for daemon host `ouranos`, state `/var/lib/lojix`, a
2700-second effect timeout, and production `NoTestDefaults`.

`Query.ByNode.(goldragon zeus None)` returned an empty generation/deployment
listing at marker 625. The same query for Ouranos returned current CompleteHost
generation 7 and UserEnvironment generation 27. This proves only the local
controller view; it does not prove what a separate Zeus daemon or target
profile contains.

The read-only key-material request returned an empty report for Zeus. The
current implementation constructs that empty report without inspecting target
keys, so it is not a host-key or reachability proof.

### Source and retained artifacts

`/git/github.com/LiGoldragon/goldragon/datom.dotos` is an existing regular
non-symlink `.dotos` proposal source. It declares Zeus as an Edge host on
`x86_64`. Retained Zeus materializations exist under
`/var/lib/lojix/generated-inputs`, with latest observed shapes dated July 2,
July 25, and July 29. They are managed-output evidence from earlier runs, not
current target state. Encrypted files in those trees were not read.

### Update interface

The supported update surface is the owner-only inline typed `meta-lojix` request
`Deploy.Host`; ordinary `lojix` is for queries, watches, and key-material
checks. A host request must carry, positionally, the cluster and node, host
composition, proposal source, immutable or resolvable flake reference, explicit
Nix-store/SSH transport, input mode, output selector, NixOS activation backend,
host action, source-revision policy, optional builder, and extra substituters.

For a Horizon-mode Zeus host deployment, Lojix first materializes the supplied
proposal for `(goldragon, zeus)`, then evaluates/builds the requested output,
copies the exact closure to the explicit target store, and performs the chosen
activation action. `DeployAccepted` only means the durable request was
admitted; terminal completion requires ordinary re-query.

The current workspace has explicit transport variables for Ouranos only. A
Zeus request therefore cannot safely inherit or derive a route; the exact Zeus
transport, immutable CriomOS revision, output selector, builder, and requested
host action remain caller decisions.

## Preconditions and safety checks

Before any actual Zeus proposal, evaluation, or deployment, the caller must
establish:

- Zeus reachability and strict known-host SSH access for the exact explicit
  transport.
- A pushed immutable CriomOS revision and the intended pinned CriomOS-home
  input, plus a valid proposal source revision.
- The exact Horizon input mode, host composition, output selector, Nix system,
  activation backend/action, builder and substituter configuration.
- Remote-only Nix evaluation/build placement where required by the owning Nix
  workflow, with no silent local fallback.
- Independent target-side free-space, cache/signing-key, profile, boot-entry,
  and activation-journal checks before live activation.

The current probes establish none of the Zeus target-side checks because the
host is unreachable. The materialized inputs do not establish a current
proposal evaluation or closure.

## Failure and rollback

Lojix records typed failure stages and terminal reasons for source, evaluation,
build, copy, and activation failures. It does not automatically roll back an
`ActivateNow` failure. Because host activation may set the target profile before
`switch-to-configuration` completes, a terminal activation failure can leave
partial target state; inspect the target profile, runtime links, boot state, and
activation journal before any retry. The committed Lojix generation set and the
live target links must be reported separately.

`ScheduleBootOnce` is a separate action with explicit old-entry/new-entry
boot-once handling; it must not be conflated with normal live activation.

## Unknown until proposal/evaluation or target access

- Zeus's current NixOS generation, Home Manager generation, runtime services,
  boot default, and target-side Lojix state.
- Whether the retained July materializations correspond to any deployed or
  booted state.
- The exact immutable source revision and resulting Horizon projection.
- The evaluated derivation, realized closure, target copy result, activation
  journal, and whether any partial state would remain after failure.
- A safe rollback target for Zeus.

No mutation is authorized by this preflight.

## Sources

- `flows/3cb84d07/witnesses/zeusConnectivity.md`
- `flows/3cb84d07/witnesses/lojixController.md`
- `flows/3cb84d07/witnesses/zeusInputs.md`
- `flows/3cb84d07/witnesses/proposalAndSource.md`
- `flows/3cb84d07/witnesses/failureBehavior.md`
- `/home/li/primary/SKILL_VARIABLES.md`
- `/git/github.com/LiGoldragon/goldragon/datom.dotos`
- `/git/github.com/LiGoldragon/goldragon/AGENTS.md`
- `/git/github.com/LiGoldragon/goldragon/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS/NON_IDEAL_AGENTS.md`
- `/git/github.com/LiGoldragon/lojix/README.md`
- `/git/github.com/LiGoldragon/lojix/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`
- `/git/github.com/LiGoldragon/lojix/src/daemon.rs`
- `/home/li/primary/.agents/skills/lojix/SKILL.md`
