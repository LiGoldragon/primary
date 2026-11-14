# 052 proposed allocation — explicit authority requested

Prepared 2026-11-05; source evidence is immutable916 and previously captured local refs. Capture timestamp of the342-ref namespace inventory is UNKNOWN (not replaced with filesystem mtime or this report time). No current remote fetch, unpublished-owner ledger or registry reservation witness is held. Every candidate below is a QUESTION to Core, not a free-name or allocated claim. Core must confirm its authoritative reservation boundary or name the owner who does.

Final packet index: `/home/li/primary/flows/e60c75/reports/final-ledger-checkpoint.md` (seven proposal hashes); current custody `/home/li/primary/flows/e60c75/reports/custody-handoff.md`, receipt hash db9c64e8e442e96e4a68b82ba8843b62a7201d4b2c2c77466888186ab17037da. New prep locks25611/25612/25613/25614 owner e60c75. No body/publish grant requested by allocation alone.

## Crates/contracts/libraries

| Exact package(s) | Immutable base / current version | Observed namespace and collisions | Candidate requested | Final direct consumers |
|---|---|---|---|---|
| flow-defaults | Flow916b54574ae0024b893a9f4252f2e97704db48c1 /0.51.0 workspace | Flow155 heldrefs in342-ref capture; authoritative unpublished allocations unknown | Retire executable-default source; allocate0.52.0 ONLY if retained as changed package, otherwise remove package and update all consumers; no empty compatibility shim | old startup/Nix/Flow consumers replaced by explicit startup input |
| flow-ethos | same Flow916 /0.51.0; standalone contract edges currently pin Flowb92b9689190c62db4f4c66a2b39cafe356cec1e4 | Same Flow heldrefs, no current remote clearance | 0.52.0, SAME one real shared revision for contracts and workspace | ordinary/meta contracts; native/Nexus/clients; moved exact4ProcessIdentity declarations |
| flow-meta | Flow916 /0.51.0 | Same Flow boundary | 0.52.0 | flow-meta and flow-meta-compose-invocation binaries; Nix/wrapper/invocation callers |
| flow-native | Flow916 /0.51.0 | Same Flow boundary | 0.52.0 | Nexus/native adapters and same-session Resume |
| flow-nexus | Flow916 /0.51.0 | Same Flow boundary | 0.52.0 | runtime service, configured Nix package/capsule, ordinary/meta peers |
| flow | Flow916 /0.51.0 | Same Flow boundary | 0.52.0 | flow, flow-hook, flow-compose-invocation binaries and their Nix/invocation producers |
| signal-flow | ce083f2ba9cc0bd928735ba4cc09e59965982e30 /42.0.0 |73heldrefs;43.0.0 exists refs/remotes/origin/next/a8f7-70a111 at d3a5fbc5beb595b53a739f8f75e768f16c21e20e | 44.0.0? | meta,Flow ordinary/native/Nexus,generated codecs/projections/Resume/Observe |
| meta-signal-flow |281f5aa1b88cd43609c127cdf6f3c12645faf58b /54.0.0 |97heldrefs;59.0.0 at origin/next/a8f7-70a111 8fcbf8468bd61d0e78b4a3f7e43386a66431f84b;57/58 also occupied;55 previously held collision |60.0.0? | Flow meta/Nexus/startup/configuration; ProcessIdentity old-path reexports |
| sema |51d7927c872f0df12791bad8d39a4db6433b01a1 /0.1.1 |5heldrefs;0.2.0 absent ONLY that capture |0.2.0? | Engine retained-backend/opening/transaction surfaces |
| sema-engine |9884905ff9c660ad97a35c524e42532d5c7bac90 /0.18.0 |12heldrefs;0.19.0 absent ONLY that capture |0.19.0? | Flow opening/config/Resume stores, all commit_atomic callers |
| datom-codec |4dff16b4f7412febc3b71aac8b49680cd20988cb /0.32.2 | Exact pinned tree; held codec-ref namespace appendix pending, no free claim |0.33.0? | Flow/contract codec features, adapters, generated forming/composition consumers |
| datom-codec-derive (conditional actual source delta) | same Datom4dff16b4f7412febc3b71aac8b49680cd20988cb workspace /0.32.0 | Exact companion manifest witnessed; ref/namespace authority same unknown codec boundary |0.33.0 IF changed generated trait implementations require it; otherwise retain0.32.0 and do not publish an empty bump | generated datom trait implementations in contracts/Flow; actual changed expansion obligation must be demonstrated |
| protos |15b41da8f2579e73ead59bc0c2b97529b8ac32d3 /0.32.2 |Exact26-file tree; depth1 history, parent unavailable; namespace appendix pending |0.33.0? | Datom, Flow prefix scanner, all explicit bounded reader consumers |
| redb (owned Git fork, NOT crates.io release) | registry4.3.0 archive SHA256 fb338a6c67830a61bed824b78c2bb034ab1ff401a20616bd7957524f4fdc2f22; explicit import1e985fb3c51126676047f295c8630b17229ef11d, manifest commit4936637de6faf266d02f479141c01c55190f4759 | Independent local repo no upstream Git identity/owned remote; registry4.3.0 occupied by exact source; fork namespace unallocated | Retain package4.3.0 for Cargo version compatibility, allocate owned fork ref `flow-052-opening` and authoritative owned remote; immutable resulting Git rev is release identity. Core must approve fork coordinates before publishing. | Sema/Engine and Flow direct admission consumer, explicit Cargo override/lock+fixed Nix source; never incidental local path/cache |

All six Flow package names/versions are witnessed manifest fields, not six independently divergent releases. Their workspace version is one fact. Retirement of flow-defaults is an explicit consumer replacement, not an unreviewed published package shim. A separately changed derive/codegen package requires its own row; Datom companion datom-codec-derive0.32.0 is now witnessed and listed conditionally; Protos has no separate companion observed. Narrow reader still confirms actual ref names and whether any derive expansion changes, not merely use of new input types. `ethos-zero` build input is pinned07714b0171802787bea1eefe4caa2d826d9c4030: no generator-source change currently evidenced/authorized; regenerating projections alone does not allocate a new generator version. Any actual generator API edit must be surfaced before bodies.

## Memory coordinates

Base for every row is Flow916 and its exact existing catalog. Local label search across held five-repository refs is observation only; its timestamp is unrecorded. No remote/unpublished schema ledger is held.

| Family | Existing identity | Requested exact coordinates | Known collision / consumer reach |
|---|---|---|---|
| flow-nexus-runtime-policy | absent in916 | table flow_nexus_runtime_policy; MemoryVersion1; schema flow-nexus-runtime-policy-v1; singleton key policy | locally unseen labels; new validated config snapshot/read/write/open/catalog/meta |
| flow-nexus-resume-head | absent in916 | table flow_nexus_resume_heads; MemoryVersion1; schema flow-nexus-resume-head-v1; exact FlowId key | locally unseen labels; Resume admission/head/readback/terminal transaction |
| flow-nexus-resume-attempt | absent in916 | table flow_nexus_resume_attempts; MemoryVersion1; schema flow-nexus-resume-attempt-v1; declared length-prefixed FlowId/generation key | locally unseen labels; durable Resume phases/evidence/readback/history |
| flow-nexus-meta-metaflow-configuration | table flow_nexus_meta_metaflow_configuration, version5/schema flow-nexus-meta-metaflow-configuration-v5 | same table/family/address key; version6/schema flow-nexus-meta-metaflow-configuration-v6 | locally unseen candidate; exact frozenV5, legacydirectV1–V4→V5→V6, declaration/config/launch consumers |

Retain Nexus-configuration-v4,AddressHold-v5,main lifecycleMetaflow-v6 and unchanged send archives. Known current-delivery-v6/send-call-v7 collisions are NOT requested: dedicated Resume changes do not justify those migrations. Any proven changed reachable persisted type is an additional explicit row before implementation, never an unnoticed enum extension.

## Specific decisions requested

1. Allocate or replace each candidate above against Core's authoritative current reservations; cite that authority/time. Locally absent does not satisfy this.
2. Confirm common Flow/shared0.52.0 and ordinary44/meta60 real-revision dependency publication order, with default+datom graphs checked independently; no root patch masking nominal identity.
3. Allocate Sema0.2/Engine0.19/codec0.33 coordinates and owned redb remote/ref, or provide exact alternatives. The fork retains4.3.0 package compatibility deliberately, while immutable fork revision differentiates modified source; no masquerade as upstream source.
4. Allocate all four Memory identities as exact typed catalog entries above. Retained families receive compatibility fixtures, not speculative successors.
5. Companion-package/ref appendix remains a named input, not blanket authorization for an unseen package. Final consumer ledger and independent review remain separate body gates.

## Core judgment and current evidence update

Core conditionally approved the proposed version/schema choices for this composition, NOT allocation: common Flow0.52, ordinary44/meta60, Sema0.2/Engine0.19, codec pair0.33 and the four listed Memory coordinates. Core holds no authoritative reservation ledger beyond supplied evidence. The verified current owner is authorized one timestamped current remote/local reservation check; collisions return for a new number, unpublished claims remain explicit. No bodies/publication follow from conditional choice.

Exact local codec/ref appendix: `/home/li/primary/flows/e60c75/reports/codec-redb-local-refs.txt`, SHA a5c3b9c07566125440ae20ea5c6ab398d22a4b7362d79c60dfde9fb93cf47293. Independent Datom/Protos clones have no refs; their read-only Cargo caches have origin/HEAD and origin/main at their exact pinned commits. Independent redb has only refs/heads/main4936637de6faf266d02f479141c01c55190f4759, local import, not an owned remote namespace. No remote freshness or free-name inference follows.

Redb package4.3.0 is conditionally acceptable only as explicitly identified owned Git fork; actual owned repository/ref is unallocated and must be established read-only without creating/pushing. Publication order: one immutable shared flow-ethos revision available first, ordinary/meta revisions using it next, then coherent final workspace pins. Root patch success is not that dependency witness.

Companion source check: pinned datom-codec-derive/src/lib.rs62,116 generates compose with `&mut datom_codec::Budget`; that type/signature remains unchanged. Inspected expansion delegates compose/compose_positions/position, contains neither Budget construction nor datom_form call. Current approved DatomForming changes therefore provide no evidenced derive-source delta. Retain derive0.32.0; no derive0.33 allocation requested on the present plan. A later concrete expansion incompatibility must be surfaced separately.

Current remote/local reservation packet returned: `/home/li/primary/flows/e60c75/reports/current-reservation-packet.md`, observation window2026-11-05 22:13:19–22:16:46UTC, raw receipt/hash index alongside. Authenticated catalogue confirms owned LiGoldragon/redb and permission evidence; desired fork ref remains unallocated. Current sema/sema-engine remote main package names are memory/memory-engine, distinct from exact prepared sema/sema-engine baselines. Proposed coordinate remains the pinned package name for scoped052; no rename or repin is inferred. Core must rule that boundary explicitly. Private/unpublished claims and authoritative Memory reservations remain unknown; current remote absence is not clearance.

Reservation packet final SHA256: `0acbbc6a1515ecaafe7fb9d36c3a5e8cf8439a53c3198d1e38a6496730c90527`; receipt-hash index SHA256 `921a95247439f7116e56256b7ecc8f6d68c3365cf5df25db93882fc226c1e2f0`. No further namespace conclusion follows from pinning the evidence.

## Binding Core reservation — NEW allocation

Core Primary's delivered message reserves these names for this sole independent052 composition. This is NEW allocation authority, not certification that unknown private reservations are absent:

- Common retained Flow workspace0.52.0; signal-flow44.0.0; meta-signal-flow60.0.0.
- sema0.2.0 and sema-engine0.19.0, preserving exact prepared package names and bases. No remote-main memory rename adoption/reversal or main landing authority.
- datom-codec0.33.0 and protos0.33.0; datom-codec-derive remains0.32.0.
- All FOUR exact Memory table/family/version/schema/key coordinates in this table, including meta-metaflow-configurationV6. Frozen predecessor/unchanged-family obligations remain.
- https://github.com/LiGoldragon/redb.git refs/heads/flow-052-opening reserved for the explicitly registry-derived fork, package4.3.0. Preserve master and every existing ref.

Authority provenance: Mind core Primary, MiddleAbrupt.Notice beginning “Read the current reservation packet. I now reserve these coordinates…”; observation packet SHA0acbbc6a1515ecaafe7fb9d36c3a5e8cf8439a53c3198d1e38a6496730c90527, bounded timestamp/scope/unknowns above. This authorizes names ONLY: no body, push, tag, main landing or release. A later conflicting claim/ref stops publication for reconciliation; never overwrite. Final independent consumer/API/schema checks and Core Secondary's sole-writer clearance still precede bodies. Further universal-ledger search is closed.
