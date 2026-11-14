# Mind flowNexus Sol 751881 handover

## Authority and completed stage

Open Astra task **80lb** (120 minutes): metadata-only hook-content correction, no deployment/live-store mutation, logical row removal only. Full accepted plan: flows/a6be39/hook-content-consumer-plan.md. Stage1 meta76 **3b1f6f0bfa77acd751c17a490db6a24cba728520** was accepted by Astra, published by Opus; eight immutable remote checks passed. Evidence flows/751881/meta76-stage1.md and its raw log. Opus published build-base **1e0d3efbdf71a9c957cf63dfe04d95c916704022**, retaining meta75 plus76 named plain/datom sets. Ordinary signal60/04a72fd and external flow-ethos0.54.3/062ef9e1 stay unchanged.

## Stage2 current source

Granted worktree **/git/worktrees/flow-0546-hook-a6be39**, branch **0.54.6-hook-a6be39**, off accepted Flow **886eefa86599e6871997f91901f1e9ab6b9712cd**. Current clean unpublished HEAD **5fcc9f14c5e777a3035e1b7147673c0efb2827c9**. Prior local commits c4ba8eff, f43ca38d, cb098cdb. Only Opus publishes after Astra acceptance.

Implemented: generated Memory6 FlowEvents with typed FlowId, RecordedHarnessEvent/RecordedStop; exact original key string retained. Shared Event.recorded() ingress; separate stored.metadata() wire projection; content-free IdentifiesNativeStop trait for transient/stored correlation; all located readers updated. Exact frozen v5 Event/Stop/row decoder and typed atomic upgrade before registration, v4 direct-to6 conversion in existing multi-family evolution; both predecessors declared before Engine::open. Catalog recognizes exact5 plus current6. Hook local metadata diagnostics preserve original ordinary Report transport. Pins/locks/Cargo.nix regenerated with published base. Docs updated.

Tests authored: direct record_event AND FlowStore Query.Report markers (None/empty/Unicode/large), reopen; exact v5 published-layout decoding/all six tags, keys/order/populated background/unrelated rows; unsupported/new/current stores; real supported upgrade fault rollback/reopen/retry; hook socket transport unchanged and diagnostics success/error/invalid config; existing actual socket acknowledgement-order test extended with body marker; hookA/transcriptB exact receipt once-only Result regression. Latest5fcc adds actual predecessor production-writer v4 populated Stop plus complete current-process serves/reopens metadata assertions. These tests are NOT yet all green.

## Gates and concrete fixes

Full immutable c4ba8eff gate exit1:13 successes/7 failures. Cause: retained Message fixture pulls meta75 but moving live dependency76 dropped meta75 datom attachments; old live-meta pin assertion. Opus granted crates/flow-nexus/Cargo.toml and flake.nix (v6c3/twzx). Fixed with aliased fixed-e192c0d meta75 dev-dependency/datoms, updated immutable76 assertions; inactive Message untouched.

Full immutable cb098cdb gate exit1:15 successes/5 failures. Dependencies/registry now pass; flow-nexus test build failed ONLY two lints: unused ReadsFlowMemory in new waking regression, useless vec in lib.rs EventsRead expectation. Both fixed in5fcc; not regated yet. Both full logs saved beside this handover. No running exec session or gate remains.

## Required next change: actual meta greeting (approved, newly granted)

Disconfirmed plan assumption: actual flow-meta client and lib.rs meta server currently send/decode raw Query frames, despite contract greeting unit tests. Astra zbg6 relays Psyche approval: **meta connection opens with existing Signal Handshake and receipt BEFORE Query decoding**; update every in-repo writer; ordinary socket unchanged. Real meta75 handshaking peer gets typed refusal; old raw-query client safely rejected separately; matched76 serves. No sniffing/fallback. Include actual matching CLI/server Configuration and populated ReadEvents roundtrip. This remains unimplemented.

Opus **m2jl** granted four extra paths in same worktree: crates/flow-meta/{Cargo.toml,src/main.rs,tests/default_socket.rs}, crates/flow-nexus/tests/default_start.rs. Existing grants include lib.rs server and nexus manifest. Add existing signal dependency pinned6d4eb74, default-features=false, where needed. signal Contracted/Handshake/HandshakeReceipt API source: /git/github.com/LiGoldragon/signal at6d4eb74, src/accord.rs. CLI CallsMetaNexus::call in main.rs:87 sends raw query; lib.rs CarriesSignalFrames::read_meta_query:2366 directly decodes. Integration helper default_start.rs:205 and mock default_socket.rs:44 need greeting. All other maintained-source inventories found no raw Flow meta writer. CriomOS-home hits invoke packaged CLIs or bind/check sockets; activation stays Opus's. Reported to Astra xsti.

Extra test grants **bcga**: store/request_id_predecessor_fixture.rs and request_id_migration_process.rs, now edited in5fcc; only test source injected into exact old revision, historical production unchanged.

## Tools, evidence and finish

Builder prometheus.goldragon.criome. WIP copy /tmp/offload/flow-0546-hook-a6be39 (excludes .git/target); recopy before regeneration. Pinned ethos-zero22 binary /nix/store/gh9lg32sv8dp2h3gml1zkax09s4r3sn3-rust_ethos-zero-22.0.0/bin/ethos-zero. Never hand-edit generated Rust. Generation example: Generate.{ /tmp/offload/.../crates/flow-nexus/ethos/memory.ethos /tmp/offload/.../crates/flow-nexus/src/generated }. Cargo update --workspace then crate2nix generate in nix shell published base#toolchain/#crate2nix on builder; rustfmt there too. Offline regeneration lacked fixed git cache, network update succeeded without dependency drift.

Exact sema-engine6a95a092 source recovered on builder: ~/.cargo/git/checkouts/sema-engine-ff01b9246db31ae9/6a95a09 (HEAD verified). MemoryUpgrades::interrupt_upgrade_at(UpgradeFault::AfterRowsWritten) exists in src/memory/upgrade.rs:28-57; actual storage fault before log/catalog commit, no engine edits. Current event_upgrade test uses it. Astra informed cqlz.

Next: claim paths including four new greeting paths; implement approved handshake and tests, regen locks, commit local immutable candidate, run FULL remote nix-fast-build gate by git+file revision, wait terminal exit, fix failures. Need isolated upgrade evidence and actual CLI/server witness. packages.store-proof exposes nexus test binary; checks.configured-package yields matching packaged daemon/CLIs for external isolated witness. Final evidence to Astra before Opus publication. Task80lb stays open.

All locks22/23/24 released at refresh. Primary evidence stays unstaged/uncommitted for standing committer. No subagents authorized/used. Skill interface absent: no generated skill file opened. Worker instructions/variables and Rust doctrine read; predecessor read rust-nix-example whole. Preserve normal checkout foreign edits.
