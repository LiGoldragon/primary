# Mind Component Situational Map

## Task and Scope

Read-only scout map of the current Mind component in `/home/li/primary` and the local source-truth it points to. Scope included Mind repositories, contracts, docs, architecture, storage assumptions, tests, tracker/TODO surfaces, and adjacent naming. I did not edit source files, commit, start daemons, or run build/test commands.

The user supplied current alignment during the task: Mind, not Mine, is the non-Spirit knowledge substrate for non-intent system knowledge such as reports, architecture, specs, rationale, and eventually many comments. Spirit remains only psyche intent. The user also clarified that the first implementation priority should be making existing architecture/report knowledge queryable; full multi-component code/spec synchronization with Orchestrate and version-control is important but later.

## Commands and Files Consulted

Local workspace guidance:

- `/home/li/primary/AGENTS.md` from the prompt.
- `/home/li/primary/ARCHITECTURE.md`.
- `/home/li/primary/protocols/active-repositories.md`.
- `/home/li/primary/RECENT-REPOSITORIES.md`.
- `/home/li/primary/orchestrate/AGENTS.md`.
- `/home/li/primary/orchestrate/ARCHITECTURE.md`.

Mind family repositories:

- `/git/github.com/LiGoldragon/mind/AGENTS.md`, `README.md`, `ARCHITECTURE.md`, `skills.md`, `Cargo.toml`, `flake.nix`, `build.rs`.
- `/git/github.com/LiGoldragon/mind/schema/*.schema`.
- `/git/github.com/LiGoldragon/mind/src/**`.
- `/git/github.com/LiGoldragon/mind/tests/**`.
- `/git/github.com/LiGoldragon/signal-mind/AGENTS.md`, `README.md`, `ARCHITECTURE.md`, `skills.md`, `Cargo.toml`, `flake.nix`, `schema/signal-mind.concept.schema`, `src/**`, `tests/**`.
- `/git/github.com/LiGoldragon/meta-signal-mind/AGENTS.md`, `README.md`, `ARCHITECTURE.md`, `skills.md`, `INTENT.md`, `Cargo.toml`, `flake.nix`, `schema/lib.schema`, `src/**`, `tests/**`.

Commands run:

- `spirit "(PublicTextSearch [Mind knowledge substrate Spirit intent reports architecture specs rationale Orchestrate version-control])"` returned public intent records including `qjrf`, which says intent belongs in the intent layer and information/belief is not intent.
- `rg --files`, `rg -n`, `find`, `ls -la`, and `sed -n` were used for local inspection.
- `jj status` in `mind`, `signal-mind`, and `meta-signal-mind`.
- `pgrep -af 'mind-daemon|/bin/mind|meta-mind|mind-write-configuration' || true`.
- `ls -la /tmp/mind.sock /tmp/meta-mind.sock /home/li/.local/state/mind 2>/dev/null || true`.
- `bd list` / `bd show` read-only tracker inspection. Some later `bd show` calls hit an embedded backend exclusive-lock error.

Not checked:

- I did not run `nix flake check`, `cargo test`, or any daemon.
- I did not inspect `/nix/store`.
- I did not inspect private reports substantively. A narrow name search found private report mentions of older Mind-like concepts, but I did not use or quote them because public component source was sufficient.

## Observed Facts

Workspace source of truth names Mind as active:

- `/home/li/primary/protocols/active-repositories.md` lists `mind` at `/git/github.com/LiGoldragon/mind` as "Central Persona state component; replaces lock-file orchestration over time."
- The same file lists `signal-mind` as "Mind/orchestration contract vocabulary" and `meta-signal-mind` as "Mind meta policy contract."
- `/home/li/primary/RECENT-REPOSITORIES.md` lists `mind`, `signal-mind`, and `meta-signal-mind` with last local commit date `2026-06-08`.
- `/home/li/primary/orchestrate/AGENTS.md` says blocked work's typed target is `signal-mind`, with notes as append-only mind graph events, and says new design work should target `signal-mind` rather than new BEADS integrations.

Repository presence and status:

- `/git/github.com/LiGoldragon/mind` exists. `jj status` reported no working-copy changes. Parent commit: `a10983d9 main | rehome: integrate archived intent records into ARCHITECTURE`.
- `/git/github.com/LiGoldragon/signal-mind` exists. `jj status` reported no working-copy changes. Parent commit: `2d31e96b main | signal-mind: fold INTENT direction into ARCHITECTURE, drop per-repo INTENT.md`.
- `/git/github.com/LiGoldragon/meta-signal-mind` exists. `jj status` reported no working-copy changes. Parent commit: `0ac8f093 main | meta-signal-mind: port to strict schema syntax`.

Repo-local guidance:

- `/git/github.com/LiGoldragon/mind/AGENTS.md` says `mind` is Persona's central state machine for memory/work items, typed thoughts, relations, notes, dependencies, aliases, subscriptions, and ready-work views. It says ordinary role claims, handoffs, and activity belong to `orchestrate`.
- `/git/github.com/LiGoldragon/mind/skills.md` says Mind owns its own `mind.sema` through `sema-engine`; typed Thought/Relation graph records use `sema-engine`; graph mutations append immutable records; memory/work mutations append typed events; the CLI accepts exactly one NOTA record or file path.
- `/git/github.com/LiGoldragon/signal-mind/skills.md` says the contract owns `ThoughtKind`, `ThoughtBody`, `RelationKind`, typed technical dependency nodes/relations, the closed `MindRequest` and `MindReply` enums, work/memory vocabulary, frame alias, and round-trip tests. It explicitly does not own state actor/database/CLI parsing/runtime tables.
- `/git/github.com/LiGoldragon/meta-signal-mind/skills.md` says the repo owns only meta PersonaMind policy signal vocabulary and contains no daemon, database, actor runtime, CLI parser, or policy evaluation logic.

Current Mind implementation:

- `/git/github.com/LiGoldragon/mind/Cargo.toml` defines library `mind`, binary `mind`, daemon binary `mind-daemon`, meta CLI `meta-mind`, and configuration writer `mind-write-configuration`.
- `/git/github.com/LiGoldragon/mind/src/lib.rs` exports `MindRoot`, `MindClient`, `MindDaemon`, `MetaMindClient`, `MindTables`, `MemoryState`, `TechnicalSeedDataset`, text projection types, supervision, and generated schema modules.
- `/git/github.com/LiGoldragon/mind/src/actors/root.rs` defines a real Kameo `MindRoot` supervising ingress, dispatch, domain, view, store, reply, subscription, supervision, and optional choreography actors.
- `/git/github.com/LiGoldragon/mind/src/actors/store/kernel.rs` defines `StoreKernel` as the actor owning `MindTables`; it handles memory graph commit/load, typed thought/relation writes and reads, technical node/relation writes and reads, subscriptions, and shutdown.
- `/git/github.com/LiGoldragon/mind/src/tables.rs` sets `MIND_SCHEMA_VERSION` to 10 and registers `memory_graph`, `thoughts`, `relations`, `technical_nodes`, `technical_relations`, and four subscription tables through `sema-engine`.
- `/git/github.com/LiGoldragon/mind/src/configuration.rs` says the daemon accepts exactly one binary rkyv startup configuration file naming working socket, meta socket, and store path; daemons do not parse NOTA.
- Runtime probe found no active `mind-daemon`/`mind`/`meta-mind` process and no default `/tmp/mind.sock` or `/tmp/meta-mind.sock` socket at inspection time.

Contracts:

- `/git/github.com/LiGoldragon/signal-mind/src/lib.rs` uses one `signal_channel!` declaration and aliases `MindRequest = Operation`.
- `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema` says it is hand-maintained concept source for `signal-mind 0.5.0`, documents current Rust contract, and is not yet the generator source for `src/*.rs`.
- `signal-mind` current operation families include typed mind graph, work/memory graph, typed technical dependency graph, subscriptions, and channel choreography observation.
- `/git/github.com/LiGoldragon/meta-signal-mind/schema/lib.schema` defines `Configure`, `Inspect`, policy modes, `PolicySnapshot`, `ConfigurationRejected`, and `RequestUnimplemented`.
- `/git/github.com/LiGoldragon/mind/src/meta.rs` currently replies to meta-policy operations with typed `RequestUnimplemented { reason: NotBuiltYet }`.

Tests and check surfaces:

- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`, `daemon_wire.rs`, `cli.rs`, `memory.rs`, `orchestrate_caller.rs`, and `weird_actor_truth.rs` contain many targeted tests for actor topology, daemon wire, CLI, durable storage, technical memory, subscriptions, and architecture guards.
- `/git/github.com/LiGoldragon/mind/flake.nix` exposes `checks.default`, `build`, `test`, `cli`, `cli-binary`, daemon checks, subscription checks, technical-memory checks, doc, fmt, and clippy.
- `/git/github.com/LiGoldragon/signal-mind/flake.nix` exposes cargo tests, round-trip tests, schema drift tests, doc, fmt, and clippy.
- `/git/github.com/LiGoldragon/meta-signal-mind/flake.nix` exposes build, tests, round-trip, doc, fmt, and clippy.
- I did not run these checks.

Tracker/TODO surfaces:

- `bd list --status open --limit 100 | rg -i ...` showed open `primary-pm7l` "[epic] Mind technical dependency memory review hardening", open `primary-pm7l.10` final reconciliation, open `primary-pm7l.11` "Mind Signal caller identity uses real auth proof", and open `primary-2ne2` "Mind technical subscriptions expose overflow/outbox policy."
- `bd show primary-pm7l` says the first `primary-irfi` epic shipped the initial public technical memory path but review found issues across durable write truthfulness, caller identity, subscription lifecycle, schema drift, key/vocabulary shape, seed coverage, and graph/provenance query ergonomics. It reports 9/11 children complete.
- `bd show primary-pm7l.11` says current caller identity is claimed frame context, not cryptographic/socket-credential/policy-backed proof, and calls for real Signal auth proof or socket credential policy while keeping request payloads identity-free.
- Later `bd show primary-2ne2` and `bd show primary-ptvb.8` failed with `.beads/embeddeddolt` exclusive-lock contention; this is a read blocker for those details, not evidence the tasks are absent.

## Current State of Mind

Confirmed current component:

- `mind` is an implemented Rust component with a real actor runtime, daemon, ordinary CLI, meta CLI, configuration writer, Sema-backed durable store, and tests.
- `signal-mind` is an implemented contract crate for Mind's public ordinary channel.
- `meta-signal-mind` is an implemented contract crate for Mind's meta policy channel, but the `mind` daemon currently returns typed `NotBuiltYet` for meta policy operations.

Mind already models more than work items:

- Typed `Thought` / `Relation` records cover observations, memories, beliefs, goals, claims, decisions, and references.
- Typed technical dependency memory covers components, repositories, crates, contracts, work items, source artifacts, reports, technical claims, witnesses, storage resources, schema families, and tables.
- Existing implementation and tests cover technical append/query, provenance/dependency queries, technical subscriptions, public seed data, and durable restart behavior.

Mind is not currently active as a live local daemon on the default sockets. The inspected state is source and tracker truth, not a live service state.

## Existing Contracts, Storage, and Runtime Assumptions

Ordinary signal:

- `signal-mind` owns the public ordinary request/reply vocabulary. It is closed-enum contract-local operation vocabulary, not public Sema wrappers.
- The CLI text surface is NOTA, but Rust-to-Rust component traffic is `signal-frame` carrying rkyv archives.
- The contract still has relation-specific operation heads such as `SubmitTechnicalNode` and `QueryTechnicalNodes`; its concept schema says those are transitional toward a future unified `Submit` / `Query` / `Tap` surface.

Meta signal:

- `meta-signal-mind` owns `Configure` and `Inspect`.
- The meta channel names policy shape: `AuthorityMode`, `ChoreographyMode`, and `IntentSynchronizationMode`.
- Runtime policy storage and policy evaluation are not implemented yet; `mind/src/meta.rs` returns `RequestUnimplemented(NotBuiltYet)`.

Storage:

- Mind owns one component-local store path supplied at daemon startup.
- Architecture and repo skills call the durable store `mind.sema`.
- `mind/src/tables.rs` uses `sema-engine` with versioning policy store name `mind`; direct redb is behind the Sema/sema-engine layer.
- `StoreLocation` is currently a generic path wrapper and does not enforce `.sema`.
- Several test scripts still use temporary `mind.redb` file names even though architecture and skills say `mind.sema`.
- `/home/li/primary/orchestrate/AGENTS.md` also says the destination is `mind.redb`, which conflicts with Mind's current `mind.sema` direction.

Runtime:

- `MindRoot` is Kameo-backed.
- The daemon accepts binary rkyv configuration as its single startup argument.
- Ordinary CLI defaults are `/tmp/mind.sock` and actor `operator`, controlled by `MIND_SOCKET` and `MIND_ACTOR`.
- Meta CLI default is `/tmp/meta-mind.sock`, controlled by `MIND_META_SOCKET`.
- The current caller identity is required in Signal frame context and propagated into `MindEnvelope`, but tracker item `primary-pm7l.11` confirms it is not yet a real auth proof.

Orchestrate adjacency:

- `mind` depends on `meta-signal-orchestrate` and contains `MindOrchestrateCaller`.
- `mind/src/actors/choreography.rs` can send `Create`, `Retire`, and `Refresh` decisions to Orchestrate's meta socket.
- Tests in `mind/tests/orchestrate_caller.rs` manually inject choreography decisions and prove the outbound meta-orchestrate transport.
- `mind/ARCHITECTURE.md` says policy derivation from observations remains unbuilt.

## Gaps and Risks

Architecture/report queryability is close but not yet the obvious first-class product surface:

- `signal-mind` and `mind` already have typed `Report`, `SourceArtifact`, `TechnicalClaim`, `Witness`, `StorageResource`, `SchemaFamily`, and `Table` nodes.
- The first public seed dataset is hard-coded in `mind/src/technical_seed.rs`.
- There is no observed crawler/importer/indexer that ingests existing `ARCHITECTURE.md`, reports, specs, or rationale comments into Mind as queryable records.
- There is no observed CLI workflow focused on querying existing architecture/report knowledge by natural component-local keys such as component, repo, file path, report path, claim, witness, or dependency closure beyond the existing contract-level technical queries.

Source/provenance gaps:

- `mind/src/technical_seed.rs` embeds two public report paths under `/home/li/primary/reports/system-operator/`; both paths were missing during inspection.
- This does not prove the seed is invalid, but it weakens report provenance for a queryable knowledge substrate until the report references are restored, rehomed, or represented as external/missing references.

Documentation drift:

- `mind/README.md` says ordinary role claims live in `persona-orchestrate`; current architecture and active repos say `orchestrate` / `signal-orchestrate`.
- `signal-mind/README.md` says ordinary role operations belong to `signal-persona-orchestrate`; current architecture says `signal-orchestrate`.
- `meta-signal-mind/INTENT.md` still exists even though current workspace direction says durable repo direction belongs in `ARCHITECTURE.md` or code stubs, not per-repo `INTENT.md`. This may be stale, especially because `signal-mind` recently removed its per-repo INTENT.
- `mind/ARCHITECTURE.md` references `~/primary/ESSENCE.md`, which is absent in the current primary workspace layout where `ARCHITECTURE.md` absorbed workspace vision/intent.

Naming/storage drift:

- Mind architecture and skills say `mind.sema`.
- Orchestrate guidance and Mind test scripts still say/use `mind.redb`.
- Current `StoreLocation` accepts arbitrary paths, so naming is a convention rather than a type-enforced storage invariant.

Policy/choreography gaps:

- Full channel choreography policy plane is destination work.
- Ordinary inbound choreography requests route to typed unimplemented replies until policy derivation is built.
- The outbound `MindOrchestrateCaller` works for manually injected decisions, but there is no observed implementation that derives decisions from architecture/report knowledge, channel misses, or spec/implementation drift.

Auth gap:

- The current Signal caller identity is not a real proof. Tracker `primary-pm7l.11` explicitly leaves real auth proof/socket credential policy open.

Subscription/outbox gap:

- `signal-mind` contract documents bounded demand and says it does not promise a durable outbox.
- Tracker list shows open `primary-2ne2` for "Mind technical subscriptions expose overflow/outbox policy", but detailed read hit `.beads` backend lock contention.

Schema/generation gap:

- `signal-mind/schema/signal-mind.concept.schema` is not the generator source for `signal-mind/src/*.rs`; it documents current Rust.
- `mind/schema/mind.concept.schema` is older concept material and not a reliable current contract map.
- `mind/build.rs` generates daemon/runtime-plane modules, while ordinary `signal-mind` decoding remains component-side and hand-written.

Private boundary:

- Private reports may contain older Mind design discussion, but public source and tracker evidence are enough for component-local planning. Do not use private report contents as public source truth without explicit scope.

## Interpretation

Mind is present and substantially implemented. It is no longer just a concept or placeholder. The core technical-memory substrate for non-Spirit system knowledge exists at the contract and storage/runtime layers.

The current useful boundary is narrower than the eventual multi-component vision. Mind can already hold typed technical facts and provenance, but it does not yet appear to ingest and query the existing architecture/report corpus as a normal workflow. The source-to-spec and spec-to-implementation synchronization loop with Orchestrate, repository-ledger, and version-control is still an integration problem across multiple components.

The storage and docs drift is not fatal to implementation, but it will confuse the next worker if left implicit: `mind.sema` is the architectural name, while `mind.redb` still appears in Orchestrate guidance and test scripts.

## Recommended First Implementation Slice

Prioritize a component-local "architecture/report knowledge import and query" slice inside the existing Mind surfaces.

Smallest coherent slice:

1. Define the import target in `signal-mind` using existing technical-memory vocabulary if possible: `Report`, `SourceArtifact`, `TechnicalClaim`, `Witness`, `Documents`, `ClaimsAbout`, `ProvenBy`, `LocatedAt`, `ProvenanceDependency`, and storage/schema/table nodes. Avoid broad code/spec sync semantics in this slice.
2. Add a `mind` importer or seed command that reads a bounded public corpus first: repo `ARCHITECTURE.md` files for `mind`, `signal-mind`, `meta-signal-mind`, and selected public reports already referenced by source or active protocols. It should create append-only technical nodes/relations and preserve source path, heading/symbol if available, summary, and evidence locator.
3. Add query paths oriented around existing knowledge: query by repo/component, report path, source artifact path, claim/witness, and dependency/provenance neighborhood. Reuse existing `QueryTechnicalNodes`/`QueryTechnicalRelations` if sufficient; add contract variants only where existing query shapes cannot express the needed retrieval.
4. Add CLI text projection for those queries so an agent can ask Mind for "what does architecture/report knowledge say about component X" without hand-writing full contract records.
5. Prove it with Nix checks: import a tiny fixture corpus, query it back through the daemon/Signal-frame path, verify append-only correction behavior, and verify missing report paths are represented explicitly rather than silently accepted.

Out of first slice:

- Do not implement full Orchestrate/version-control bidirectional code/spec synchronization yet.
- Do not derive policy decisions from the imported knowledge yet.
- Do not ingest private reports.
- Do not redesign `signal-mind` operation heads unless the existing query/import shapes genuinely cannot carry the first slice.

Follow-on integration after the queryable-knowledge slice:

- Connect repository-ledger/version-control events into Mind technical memory.
- Let Orchestrate consult Mind for spec/implementation drift and file work items.
- Add policy derivation from Mind observations into `MindOrchestrateCaller`.
- Replace claimed caller identity with real auth proof or socket credential policy before trusting Mind as an authority root.

## Verification Summary

- Source inspection completed for `mind`, `signal-mind`, `meta-signal-mind`, primary architecture/protocols, and Orchestrate docs.
- No builds or tests were run.
- No daemon was running on the default local sockets during inspection.
- Three Mind-family repositories were clean by `jj status`.
- Tracker inspection partially succeeded; `.beads` backend contention blocked details for two open items.
