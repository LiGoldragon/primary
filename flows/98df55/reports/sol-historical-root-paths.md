# Historical provenance and root call paths — Astra Order mgmg

Read-only source/history investigation of candidate 47e9b1b6fb446f2a76bacd95b86b87ce49d2b5e9 by flow 72d107. No builds, archive generation, fixture edits, source/worktree changes, or lock changes.

## Published original V1 producer located

- Repository: https://github.com/LiGoldragon/flow
- Original producer: **4b8134040b2dfc1ecabb333c098042aa07a115f1**, “Add dedicated handover configuration Memory family”. Retrieved through a new filtered bare remote clone on Prometheus, and `merge-base --is-ancestor <producer> refs/heads/main` exited 0. This supersedes the original audit's history-unavailable limitation.
- Exact original source: `crates/flow-nexus/src/store/handover_configuration.rs`, lines 5–10 in that revision. Its StoredHandoverConfiguration has policies, archive, count in that order; rkyv Archive/Serialize/Deserialize derives; record key `handover`; memory version 1; schema hash `SchemaHash::for_label("flow-nexus-handover-configuration-v1")`; table `flow_nexus_meta_handover_configuration`; family `flow-nexus-handover-configuration`.
- A later still-V1 producer is **b0331a849fc214c1072e1c7a60c7c2a679db958c**, the parent of c7d92b4f4f6fafc76d28643ab6c2b1f22ba077fd (publication-deadline addition). It too is an ancestor of published main. It has the same top-level V1 fields/schema, but pins meta68 at 91e1f45adced679a006638f1cec1b6456e5a4dc0. Do not assume all constituent histories under a schema label are the same without checking.

## Exact original constituent closure

Producer 4b813404 Cargo.lock pins:

- meta-signal-flow **66.0.0**, **2f0a8de1e767929e2c8e1191a8e5a8a67492ae8e**.
- signal-flow **52.0.0**, **32902052a31745f0ddb6c35c8013146d0dfca4d6**.
- sema-engine **0.18.0**, **9884905ff9c660ad97a35c524e42532d5c7bac90**.
- rkyv **0.8.18**, registry checksum d9776093b7ca170454ab1406954f7b7d97a57c51dc6c0642957fb2ef25c2d399. Candidate also locks rkyv0.8.18; feature/target settings still belong to any execution proof.

Meta66's `src/generated/signal.rs` records:

- :36 WarningShareLeft = i64; :38 ReminderText = String; :40 EveryMinutes = i64.
- :44–49 HandoverPolicy fields are ModelName, WarningShareLeft, ReminderText, EveryMinutes, in that order.
- :53 Path = String.
- :57–60 HandoverPoliciesConfiguration variant order Configured(Vec<HandoverPolicy>), Unconfigured.
- :64–67 HandoverArchiveConfiguration variant order Configured(Path), Unconfigured.
- :71–74 HandoverCountConfiguration variant order Configured(i64), Unconfigured.
- `signal-flow` reexports ModelName from flow-ethos (`src/lib.rs:6`); both its lock and meta66's lock pin flow-ethos0.53.1 at **5ea2aa474a27bc2f233d189f1295d311c69c6ec8**. That revision's `crates/flow-ethos/src/generated/library.rs:267` declares ModelName = String.

**Important qualification:** candidate frozen V1 uses *current* meta82 constituent types, not these exact old constituent definitions. Meta82 `570b173cbd943001b611439606a439d194a3b824` has WarningShareLeft/ReminderText/EveryMinutes newtypes (:66/:70/:74) and Path newtype (:207). Thus top-level field agreement does not establish a fully frozen historical type graph. The newtype-versus-alias difference is observed; whether its rkyv archived bytes remain compatible is unknown without old-producer evidence. It is not established data corruption. Existing new-build frozen-type fixtures cannot decide it.

## Bounded old-producer fixture plan — proposed, unexecuted

1. After authorization, use a dedicated scratch checkout of the published original producer4b813404 with its own committed dependency lock. Add a test-only producer at that package's private-module boundary so it uses the actual StoredHandoverConfiguration and descriptor, rather than copying a schema and silently taking current dependencies. Preserve its old pinned engine and archive settings. Build only on Prometheus through the approved committed-revision gate path; this step is not authorized or started here.
2. Have that test create a persisted sema-engine store with configured, nonempty policies (distinct model/reminder strings and nonzero integer values), configured archive path and nondefault count. Include separate Unconfigured and empty-configured cases. Persist a manifest naming producer/dependency revisions, schema/family/table, target/archive features, exact logical expectations and archive digest. No harness, sockets, native flow or live store is needed.
3. Hand the immutable produced bytes to the *new consumer process*, open using its real family descriptor/upgrader, assert every predecessor field plus exact independently stored approved recovery text and default deadline, change text through configuration, close and reopen, and assert no reseeding. Never have the new test generate its own supposedly historical input.
4. Repeat at the later still-V1 b0331a84/meta68 boundary if its constituent closure differs; this catches two producers using the same V1 schema label. If compatibility fails, freeze the actual old graph in a reviewed migration release rather than changing test expectations. A V2→V3 producer boundary and a real V1→V2→V3 chain can follow as bounded additional cases; they are not already proved.

## HandoverRoot call-path conclusion

**Unread is not rehearsal-only. It is the no-root composition API mode, and production also selects it when there is no predecessor. No observed production predecessor path selects Unread.**

Exact candidate paths:

- `composition.rs:769–775`: ComposesLaunch::compose delegates to compose_in_root(..., Unread, []). Its repository callers in composition.rs, codex.rs and lib.rs are tests (codex test module begins :1950, lib test module :3036). The trait remains public, so this says what the repository calls, not what all hypothetical downstream callers do.
- `performing.rs:263–270`: Operation::Compose sets launch_root=None only when profile.flow_id_option=None; with a predecessor it attempts self.launch_root(address).
- `performing.rs:294–297`: None→Unread, successful root→At, failed predecessor root→Unresolved. Thus ordinary production no-predecessor composition can use Unread, and production predecessor root failure uses Unresolved.
- `sending.rs:630–638`: Rehearse constructs its declared profile and calls the same Operation::Compose. It does not call the no-root compose API directly. Root behavior is therefore determined by the profile, not by the Rehearse verb.
- `launching.rs:393` and `waking.rs:2210/:3717` also call Operation::Compose. `waking.rs:3704–3705` explicitly puts the predecessor id in successor profiles; they therefore take At/Unresolved, not Unread.
- `lib.rs:1705–1715`: ConfiguredRunner supplies one MemoryHandoverSource to both composer capabilities. Its `requires_launch_root` returns false (:201–204).
- `composition.rs:345–351`: Unresolved with that source becomes the empty Path, instead of RootUnresolved. `lib.rs:212–228`: a matching memory handover yields text; no matching handover with empty root yields Absent, without trying a file. `composition.rs:358–375`: Absent with validated emergency provenance reads current recovery text and renders the typed provenance, for either flow kind.

Therefore production Unresolved **can statically reach recovery** and does not require transcript-path or filesystem-root resolution to do so. This is a traced code path, not executed proof. A store read fault still yields HandoverUnreadable or RecoveryUnavailable as applicable; a real memory handover takes precedence. Add the previously requested Unresolved+real-source negative-root fixture during integration acceptance. Unread suppression is not by itself an observed production emergency defect under these callers.

## Evidence retained outside all source worktrees

Remote scratch: `prometheus.goldragon.criome:/tmp/flow-72d107-history-uMDpje/` holds filtered bare flow.git, meta.git, signal.git and evidence/ original source/lock/generated snapshots. Evidence SHA256:

- original-v1.rs: dfcc20be4bc6d411e7fd25fff6941e9873b221ac69878c7b86a2669727981d91
- original-Cargo.lock: b9c814b8481d912c2c3311b780d40f58957a3dc2987d73b5854b7875e5e6779d
- meta66-generated.rs: 974a44868f1ccd8a7c0207066455100ad6c047732a8545091f1a198ba1d4ac30
- old-flow-ethos-generated.rs: 56360fd0fec3e47d9c26d5cafdf9208c8c60efa539f8729e9b4368cf914612bd

All earlier locks/source holds preserved. ttkb/6k78/kick remain open.
