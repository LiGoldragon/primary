# 052 exact recovery appendix

Read-only recovery by native thread `01a1addb-db3d-7bb2-9bf8-0494b543d810`, started 2026-11-05 22:41:42 UTC under the one-time bounded assignment. This appendix supplements the frozen packet; it grants no body, source, lock, preparation, or independent-gate authority. The reader is its author and cannot independently certify it.

## Frozen inputs and reconciliation

- Frozen packet: `/home/li/primary/flows/e60c75/reports/final-packet-052`; `MANIFEST.sha256` SHA-256 before this read `e545c6c2d378be1a1c86eed9ea688096c8fd259e3e7059ce58f7a31e5e01d38c`; `packet.json` SHA-256 `789d2fe063fc17e8f3cc80deb1f1fcd301a7488234d64aabee0a57b71205b904`.
- Approved reminder correction: `/home/li/primary/flows/4f3cb8/reports/052-review-supplement-stop-poll.md`, SHA-256 `ae49678d642160ee312ddf30f55ed41f079f9daf742b4833ad8328dc8d352ce6`. It owns the correction: `PollingPolicy.AgentStop` is `observe_agent.rs:217`; `ReminderPolicy.Scan` is `REMINDER_TICK` at `reminding.rs:15-16`; both the sleep and spent increment at `reminding.rs:95-97` use one captured `StopPoll`, with the current wait retaining its snapshot and the next wait reading the newly committed snapshot.
- `current-owner-index.md` records that the predecessor recovery status is UNKNOWN, its partial semantic supplement is unaccepted, and this thread produced no durable file before its interruption. This file is the only output of the new one-time assignment; it makes no continuity claim.

## Exact named runtime rows

### `FramePolicy.Nexus`

Current production owner is `CarriesSignalFrames for UnixStream`, `crates/flow-nexus/src/lib.rs:1386-1445`. The literal is `FRAME_LIMIT = 1024 * 1024` at `:1389`. `read_frame` reads the u32 prefix at `:1408-1412`, rejects only inbound `length > FRAME_LIMIT` at `:1412-1414`, then allocates at `:1415`. `write_frame` at `:1402-1405` casts `bytes.len()` to u32 and writes prefix and payload without either the configured frame bound or checked u32 conversion. Ordinary query/response and meta query/response all pass through those two methods at `:1420-1445`.

Exact replacement required by the frozen proposals: one resolved `FramePolicy.Nexus.ByteCount`, validated positive and representable as both usize and u32, is captured for the Nexus frame carrier. The same captured allowance gates outbound serialized length, with checked usize-to-u32 conversion before any prefix or payload write, and inbound announced length before allocation. Activation is the committed RuntimePolicy snapshot used by both ordinary and meta Unix-stream operations; a trait-wide associated literal cannot express independently captured policy. Oracle: exact-bound and one-over in both directions; outbound refusal writes zero bytes, inbound refusal allocates no payload; ordinary and meta paths observe the same captured snapshot, and a later operation observes a later committed snapshot. This is an affected production consumer, not a fixture.

### `LaunchPolicy.FlowIdentity`

Current production constructor is `HerdrCli::default`, `crates/flow-nexus/src/herdr.rs:143-198`: `flow_id_executable: PathBuf::from("flow-id")` at `:158`. Actual execution is `ClaimsNativeIdentity::claim_flow_identity`, `herdr/launch.rs:689-710`, specifically `Command::new(&self.flow_id_executable)` at `:695`. Exact replacement is validated `LaunchPolicy.FlowIdentity.ExecutablePath`, an explicit absolute path passed unchanged into `flow_id_executable`; PATH lookup disappears. It activates for future identity-claim operations. Validation covers nonempty absolute/no-NUL spelling; existence, regular-file/access and start failure remain typed operation observations. Oracle: configured helper receives the existing harness/`--flows-root` arguments; absent/nonfile/unexecutable helper refuses at the operation boundary with no sibling/PATH substitution. Fixture-only `ConfiguresHerdrCli::at` sets a fixture helper at `herdr.rs:358-367` and remains fixture data.

### `LaunchPolicy.ClaudeHome`

Current production branch is `HerdrCli::default`, `herdr.rs:146-153`: read `CLAUDE_CONFIG_DIR`, else `home.join(".claude")`. That result fans out to `claude_transcript_root = claude_home.join("projects")`, `ClaudeDaemon::under(&claude_home)`, and `ClaudeSessions::under(&claude_home)` at `:188-190`; transcript consumption is `herdr/launch.rs:820-840` (`Claude => &self.claude_transcript_root` at `:832`). Exact replacement is validated `LaunchPolicy.ClaudeHome.DirectoryPath`, passed unchanged as the base for those three existing projections; the environment/home fallback is removed. It activates when constructing the Herdr adapter for later Claude launch/readiness/session operations, without moving existing seats. Oracle: configured base yields exactly its `projects` transcript child and daemon/session bases; relative/empty/NUL validation refuses the whole configuration; unavailable/wrong-kind/access failure is observed at the existing operation boundary with no environment fallback. Fixture-only `ConfiguresHerdrCli::at` uses `fixture_root/claude-home` at `herdr.rs:358-391`.

### `LaunchPolicy.FlowDirectory`

Current production branches are `workspace_root.join("flows")` in `HerdrCli::default`, `herdr.rs:154-159`, and the configuration overlay `self.flows_root = source_root.join("flows")` in `ConfiguresHerdrCli::with_source_root`, `herdr.rs:332-356`. The result is used for workspace validation at `herdr/launch.rs:651-665`, marker paths at `:668-686`, and the identity-helper `--flows-root` argument at `:689-699`; reservation and launched-flow paths use the same `flows_root`. Exact replacement is the validated one-component `LaunchPolicy.FlowDirectory.DirectoryName`, appended once to existing configured `SourceRoot` in both construction and overlay. The current hard-coded filename check `== Some("flows")` at `herdr/launch.rs:652-655` must compare the configured component/derived root rather than reinstate the literal. It activates for future workspace/marker/reservation/launch operations and does not move existing seats. Oracle: a valid non-`flows` normal component is retained through derived root, marker, helper argument and launch directory; empty, dot, parent, separator or NUL refuses configuration; SourceRoot and child remain distinct facts. Fixture-only `ConfiguresHerdrCli::at` accepts an explicit fixture `flows_root` at `herdr.rs:358-367`.

## Held codec-query classification

This classification is bounded to the already-held `codec-full-query-results.txt` (92 rows) and `final-independent-codec-query.log`; it is not a new inventory and does not infer whole-world exhaustiveness.

### The 92 direct `protosize`/`datom_form` rows

- Rows 1-35 are all under prepared/cached Datom `tests/{hygiene,core,composition}.rs`: fixture/oracle only. Direct-forming affected fixtures are `tests/core.rs:226` (round-trip former) and `:989` (manual 100,000-deep headed-tree refusal); both must pass explicit forming depth after the signature change. Other rows are output structural projections or text-convenience fixture calls; every text `String/str.protosize()` fixture migrates to `protosize_with` with an explicit `ReaderBudget`, while structural `Datom.protosize()` output stays.
- Rows 36-60 are all under prepared/cached Protos `tests/{delineation,vertical,protos,textualization}.rs`: fixture/oracle only. They exercise the text convenience slated for removal and therefore migrate to explicit `protosize_with`; none is a production receiver.
- Flow rows 61, 67-69, 80-82, and 90-92 are fixture-only at their cited locations (`store/queue_delivery.rs:2785`; `tests/counters.rs:40`; `tests/configuring.rs:819,880`; `main.rs:426,521,641`; `flow-meta/main.rs:153,189,303,312`). Rows 61/80-82/90-92 pair output projection with fixture readback elsewhere; the cited `protosize` expression itself is output-only.
- Flow rows 62-66, 70-79, and 83-89 are production output-only structural projection: `store/send_v32.rs:39`, `metaflow.rs:174`, `delivery/body.rs:158-159`, `sending.rs:215`, `send_tool.rs:367`, `herdr/launch.rs:490`, `composition.rs:158,604`, `bin/flow-store-check.rs:42`, `title.rs:42,66`, `main.rs:357-358,369`, `flow/compose_invocation.rs:34`, `flow/hook.rs:175,187`, `flow/main.rs:94`, `flow-meta/compose_invocation.rs:34`, and `flow-meta/main.rs:91`. They retain structural `Protosizable`; rows `main.rs:357-358` create text later read by the separate production receiver below, but are themselves writers.

### Every held Flow `Budget`/`ReaderBudget` receiver

| Location/symbol | Classification | Exact disposition / owner |
|---|---|---|
| `flow-meta/src/main.rs:39-59`, `FlowMetaClient::parse_command` | production affected | Meta `Invocation` outer codec settings from the approved adapter envelope. |
| `flow-meta/src/main.rs:19-36`, `ParsesMetaDatom::parse_datom` | fixture affected | Test helper; explicit fixture limits. |
| `flow-meta/src/compose_invocation.rs:8-31`, `main`/budget closure | production affected | Approved Meta `ComposerInput` outer settings; emitted target `Invocation` owns separate target settings. |
| `flow/src/main.rs:30-50`, `FlowClient::parse_command` | production affected | Ordinary `Invocation` outer codec settings. |
| `flow/src/compose_invocation.rs:8-31`, `main`/budget closure | production affected | Approved ordinary `ComposerInput` outer settings; target settings remain distinct. |
| `flow/src/hook.rs:78-98`, `HarnessHook::from_environment` | production affected | Approved `HookConfiguration` outer settings; native stdin JSON stays separate. |
| `flow/src/hook.rs:219-236`, test `report` | fixture affected | Explicit fixture limits. |
| `flow-nexus/src/main.rs:43-64`, `ParsesStart::parse_start` | production affected | Bootstrap `Start`/`BootstrapTextBudget`; fixed-position intrinsic obtains five limits, then same envelope full-decodes with them. |
| `flow-nexus/src/main.rs:356-370`, `ConfigurationStartup::start_store_refusal_datom` | production affected, **literal unresolved policy owner** | It constructs text then actualizes `StartRefusal` before a committed RuntimePolicy is available. Frozen prose does not explicitly assign this internal error-path decoder a supplied five-limit record. Core must choose an existing bootstrap budget passed into this function or replace the text round-trip with typed construction; no hidden constants survive. |
| `flow-nexus/src/main.rs:501-521,612-641` | fixture affected | Two `#[cfg(test)]` startup/config-only readback fixtures; explicit fixture limits. |
| `flow-nexus/src/bin/flow-store-check.rs:15-29`, `ReadsStoreCheckRequest::store_check_request` | production affected, **literal unresolved configuration envelope** | Standalone `flow-store-check` parses text, but the approved adapter envelopes enumerate ordinary/meta clients, composers and hook, not this binary. Core must assign an explicit supplied codec envelope/producer (or declare it part of an already-authored startup envelope) before body work. |
| `flow-nexus/src/delivery/body.rs:367-374`, test `budget`; `tests/waking.rs:520-528`; `store/queue_delivery.rs:2786-2795` | fixture affected | Test/readback helpers only; explicit fixture limits. |

### Codec-owned production and fixture effects exposed by the held query

- Production definitions: `protos/src/core.rs:550-575` are the two text convenience implementations with hidden `ReaderBudget { remaining: 4_096 }`; the approved replacement removes both and keeps `BoundedProtosizable::protosize_with`. `datom-codec/src/core.rs:25-30` adds `forming_maximum_depth` to `Budget`. `datom-codec/src/composition.rs:564-581` is the production Datom writer/reader for `ReaderBudget`; because the type gains `maximum_depth`, this scalar projection must become the generated/structural two-field representation (or an explicitly approved equivalent), preserving both supplied values. `generated/datom-codec-kinds.rs:10` and `datom-codec-kinds.ethos` receive the second `DatomForming` input as already authored.
- All Datom budget constructors found in the held prepared-root query outside `src/core.rs` are under `tests/{composition,hygiene,core}.rs`; all Protos `ReaderBudget` constructors outside `src/core.rs:553,571` are under `tests/`. They are fixture/oracle changes. Direct `datom_form` callers are exactly `datom-codec/tests/core.rs:226,989`, both fixture-only.

## Cargo checkout to prepared-root identity

| Source | HEAD | tree | tracked status | untracked |
|---|---|---|---|---|
| cached Datom `/home/li/.cargo/git/checkouts/datom-codec-9f95a6bbf327d45b/4dff16b` | `4dff16b4f7412febc3b71aac8b49680cd20988cb` | `3880b212180d3997d4dc400f9bd3d4b35f6908b5` | clean | `.cargo-ok` only |
| prepared Datom `/git/worktrees/datom-codec-config-d05351-independent` | same | same | clean | none |
| cached Protos `/home/li/.cargo/git/checkouts/protos-src-9157a2de36441878/15b41da` | `15b41da8f2579e73ead59bc0c2b97529b8ac32d3` | `2d1dce1ab6afdb41dc90934a0beae3e7e41377d2` | clean | `.cargo-ok` only |
| prepared Protos `/git/worktrees/protos-config-d05351-independent` | same | same | clean | none |

`diff -qr`, excluding `.git` and `.cargo-ok`, returned no differences for either pair. All seven cached files named by the 92-row receipt are tracked: Datom `tests/composition.rs`, `tests/core.rs`, `tests/hygiene.rs`; Protos `tests/delineation.rs`, `tests/protos.rs`, `tests/textualization.rs`, `tests/vertical.rs`. The receipt contains zero `.cargo-ok` hits. Thus cached and prepared receipts identify the same committed source trees; `.cargo-ok` is excluded as one untracked marker per cached root, not source evidence.

## Literal remaining questions

1. `flow-nexus/src/main.rs:356-370`, `ConfigurationStartup::start_store_refusal_datom`: choose its already-authored supplied budget owner or typed-construction removal of the parse round-trip.
2. `flow-nexus/src/bin/flow-store-check.rs:15-29`, `ReadsStoreCheckRequest::store_check_request`: assign an explicit supplied five-limit configuration envelope/producer or explicitly place it under an existing authored envelope.
3. Independent review must re-pin this appendix and the approved StopPoll supplement and gate the exact rows. This author supplies evidence, not PASS.

No other production codec receiver remains unclassified **within the two held query artifacts**. That bounded statement is not an assertion that the held query was exhaustive beyond its recorded expressions and roots.
