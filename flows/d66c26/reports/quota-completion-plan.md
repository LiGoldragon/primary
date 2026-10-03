# Quota snapshot completion plan

## Decision

Complete the one-shot quota snapshot as an ordinary Harness operation. The
implementation route is:

```text
harness CLI → migrated Harness working socket → daemon-level usage reader → UsageSnapshot reply
```

The reader remains one request/one reply. It adds no watch, store, timer, or
new daemon type. The existing `harness-daemon` is the process to deploy as a
Home user service; this is not a direct-collector CLI bypass.

## Contract-family migration

`harness` must consume one current `signal-harness` revision only. Remove the
temporary `usage-contract` package aliases and use the current contract types
throughout the crate. The current source has both the legacy working contract
and the new usage contract in one build graph, so the CLI and daemon cannot
carry `UsageSnapshotQuery` today.

Port the ordinary client and daemon framing to the current Signal contract,
then handle the query at daemon scope before any configured-instance lookup.
The query therefore reads subscriptions and live context without launching a
model session or requiring an interactive Harness instance. It replies with
the current contract's `UsageSnapshot` value.

Port `meta-signal-harness` as a coordinated contract-owner change. Its current
legacy Signal-frame dependency is not an acceptable compatibility side path.
After that contract migration, migrate Harness's meta client, daemon meta
surface, launch path, and their witnesses. No old-wire client may remain
deployed beside the new ordinary or meta server.

The authored ordinary vocabulary remains owned by
`signal-harness/ethos/signal.ethos`; regenerate its checked-in projection from
that source. Do not hand-edit generated contract code. `meta-signal-harness`
owns its own migration and must be coordinated rather than changed as an
incidental Harness patch.

## Coordinated consumers

The same landing must include the actual ordinary wire peers:

- Harness CLI and daemon: `harness/src/client.rs`, `harness/src/daemon.rs`,
  their ordinary socket tests, and the new usage snapshot route.
- Router: `router/src/harness_delivery.rs` and its Harness frame witnesses.
- Meta Harness contract and Harness's meta CLI/daemon/launch path.

Persona configuration producers are not ordinary socket peers, but they write
the binary startup configuration consumed by `harness-daemon`. Migrate and
rebuild the one that the deployed Home configuration actually selects; assess
the lowercase `persona` and uppercase `Persona` checkouts rather than changing
both by name. Their generated configuration fields must follow the migrated
contract shape, not copied legacy names.

Mentci is an inspected source consumer that constructs Harness adapter events,
without an observed Harness socket exchange in its source. Assess and rebuild
it against the single contract revision before release when its host needs
those events; it is not a reason to keep legacy framing alive.

## Home deployment

CriomOS-home currently pins Harness through the `flowId` core package option.
The inspected minimum-profile source declares no Harness user service. Add a
Home user service following the existing `orchestrate-nexus` pattern, using
one immutable migrated Harness package revision for the service and CLI.

The service needs a deterministic configuration emitter/launcher because
`harness-daemon` accepts one binary rkyv configuration-file argument. The
emitter must write the migrated typed configuration, give the user private
ordinary and supervision sockets, use the owning user's identity, and start
with an empty instance set. It must not rely on an old configuration field
layout or invent a text/argv configuration ABI. The service needs no store,
watch, or periodic collection.

The precise new Home module location and emitted configuration mechanism remain
implementation work. The available source establishes the service pattern and
the daemon's binary-configuration boundary, not a ready Harness service.

## Acceptance and release sequence

1. Land the contract-family migration and update every deployed wire peer to
   the same revision; rebuild the client, daemon, Router peer, and migrated
   configuration producer together.
2. Add and enable the Home user service from the same immutable package
   revision. A stale daemon/client pair is not releaseable.
3. Secondary performs the fixed collector review recorded in its sibling
   `quota-contract-review.md`, plus independent negative tests. Those results
   are Secondary's evidence, not claimed by this plan.
4. Release only after the installed native one-call command returns a bounded,
   normalized, credential-safe live result, and existing message delivery plus
   meta/lifecycle regression checks still pass.

The live result must preserve provider source and freshness, enumerate every
reported quota limit/window, deduplicate same-account Codex homes, represent
unknown absolute limits and stale/superseded context explicitly, and avoid raw
credentials, paths, responses, argv, environment values, or error echoes.

## Sources

- `flows/28d847/reports/quota-sources.md`
- `flows/d66c26/reports/quota-component-design.md`
- `/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos`
- `/git/github.com/LiGoldragon/harness/Cargo.toml`
- `/git/github.com/LiGoldragon/harness/src/usage/mod.rs`
- `/git/github.com/LiGoldragon/harness/src/daemon.rs`
- `/git/github.com/LiGoldragon/harness/src/schema/daemon.rs`
- `/git/github.com/LiGoldragon/harness/src/configuration.rs`
- `/git/github.com/LiGoldragon/harness/tests/component_cli.rs`
- `/git/github.com/LiGoldragon/router/src/harness_delivery.rs`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/orchestrate.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/core-packages.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix` (the requested `profiles/min/default.nix` path was not present)
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
