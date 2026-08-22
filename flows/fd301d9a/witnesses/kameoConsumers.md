# Kameo consumers

Method: probe `for repo in /git/github.com/LiGoldragon/*; do rg -n '^kameo\s*=' "$repo/Cargo.toml"; done`

Method: code read `/git/github.com/LiGoldragon/*/Cargo.toml` and matching `Cargo.lock` package blocks.

Method: probe `rg -l --hidden -i 'kameo|use kameo::|impl Actor for|impl Message<'` over `/git/github.com/LiGoldragon` while excluding `.git` and `target`.

## Manifest observations

Twenty-one repository manifests mention Kameo, excluding the Kameo fork itself:

- Direct fork declarations on `branch = "main"`: `chroma`, `clavifaber`, `criome`, `harness`, `introspect`, `mentci`, `mind`, `persona`, `repository-ledger`, `router`, `system`, `terminal`, `terminal-cell`.
- Direct fork declarations pinned to `rev = "f491b45d7dcb55e5837eddde3d5d7ca8ceaa9f01"`: `ethos-engine`, `logos-engine`, `sema-storage`, `triad-runtime`.
- Feature branch declaration: `persona-spirit`, branch `persona-lifecycle-terminal-outcome`.
- Testbed: `kameo-testing`, fork `branch = "main"`, feature `macros`.
- Upstream direct declaration: `lojix`, crates.io `kameo = "0.20"`.
- Patch-only declaration: `upgrade`, with no direct Kameo source usage; its `triad-runtime` dependency carries the fork transitively.

Feature choices observed in direct declarations:

- `macros,tracing`, with `default-features = false`: `chroma`, `criome`, `harness`, `mentci`, `mind`, `repository-ledger`, `router`, `system`, `triad-runtime`, and `persona-spirit`.
- `macros`, with `default-features = false`: `ethos-engine`, `introspect`, `logos-engine`, `sema-storage`.
- `tracing`, with `default-features = false`: `terminal`.
- `macros`, with defaults retained: `kameo-testing` and `terminal-cell`.
- Defaults retained without an explicit feature list: `clavifaber`.
- Defaults disabled without extra features: `persona`.

`Cargo.lock` observations:

- The `branch = "main"` declarations currently resolve to fork commit `f491b45d7dcb55e5837eddde3d5d7ca8ceaa9f01` in the checked lockfiles.
- Explicit `rev = f491b45...` declarations resolve to the same commit.
- `persona-spirit/Cargo.lock` contains both the feature-branch fork package at `22514f7c6900da00703a4a0ef096f21a45c95a99` and a registry Kameo package used by its locked `persona` dev dependency.
- `lojix/Cargo.lock` contains registry Kameo for its direct dependency and fork Kameo through `triad-runtime`; these are distinct package sources despite both reporting version `0.20.0`.

## Runtime observations

Textual source inventory (`^impl Actor for` and `^impl Message<` under `src/`) found:

- `ethos-engine`, `logos-engine`, and `sema-storage` each implement `SignalPlane`, `NexusPlane`, and `SemaPlane` with typed messages.
- `persona` has eight actor implementations and uses manual shutdown; its source does not contain an explicit Kameo `.supervise` call.
- `persona-spirit` has thirteen actor implementations and twelve explicit `::supervise` call sites beneath `SpiritRoot`.
- `mind` has sixteen actor implementations and fifteen explicit `::supervise` call sites in its root/store topology.
- `criome` has seven actor implementations and six explicit `::supervise` call sites beneath `CriomeRoot`.
- `chroma`, `clavifaber`, `harness`, `introspect`, `lojix`, `mentci`, `repository-ledger`, `router`, `system`, `terminal`, `terminal-cell`, and `triad-runtime` all use data-bearing Kameo actors, typed `Message` implementations, `ActorRef`, and `Spawn` in production source.

The recurring API surface is `Actor`/`ActorRef`/`Spawn`, `Message`/`Context`, `ask`, and graceful lifecycle through `stop_gracefully` followed by `wait_for_shutdown`. `DelegatedReply`, `ReplySender`, `WeakActorRef`, `ActorStopReason`, `spawn_in_thread`, and `ChildActor::supervise` appear in selected consumers.

`wait_for_shutdown()` is widely called but its returned value is generally ignored. Direct `ActorTerminalOutcome`/`ActorTerminalReason` usage was found in `kameo-testing/tests/links.rs` and Persona’s `tests/manager_store.rs`; no production consumer overrides `on_link_died`. The only `on_link_died` implementation found in the consumer set is the Kameo testbed’s link witness.

## Transitive boundary observation

`triad-runtime` is directly declared by: `Curriculum`, `agent`, `cloud`, `criome`, `harness`, `introspect`, `lojix`, `mentci-egui`, `mentci`, `message`, `mind`, `mirror`, `orchestrate`, `persona-spirit`, `persona`, `repository-ledger`, `router`, `signal-introspect`, `spirit-judge`, `spirit`, `system`, `terminal-cell`, `terminal`, and `upgrade`. These manifests therefore name a transitive path to the fork wherever their locked graph uses `triad-runtime`; lock freshness differs between repositories.
