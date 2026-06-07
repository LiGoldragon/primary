# Cloud component core-crate context refresh

Date: 2026-06-06
Role: cloud-operator

## Request

The user asked to look into the latest development with the core crates, refresh intent, and contextualize it for the cloud component.

## Intent capture

Spirit record `fteq` captures the durable framing: refresh the cloud component intent and context against the latest core-crate development, so cloud-component work stays aligned with the current shared runtime and schema/crate direction.

## Core-crate development checked

The recent primary report `reports/cloud-designer/32-core-crate-refresh-for-lojix/` landed before this pass and gives the latest detailed survey. During this pass, `reports/cloud-designer/33-lojix-daemon-emitter-integration-design/0-frame-and-method.md` also appeared in the primary working copy, carrying the newer decision records `tj99` and `9v7h`: actively design the emitter evolution so lojix's needs integrate with the core crates, and fail closed on owner-auth uid mismatch.

The load-bearing development is that `schema-rust-next` now emits a component daemon spine and `triad-runtime` now carries the runtime primitives that spine consumes:

- `schema-rust-next` now emits a daemon module: `ComponentDaemon`, generated daemon runtime, listener tiering, command parsing, frame decode/execute/encode, and an exit tail.
- `triad-runtime` now carries additive primitives such as `ConnectionContext`, the `DaemonConfiguration` trait, and `ExitReport`.
- `ConnectionContext` supplies kernel-vouched peer credentials via the Unix stream, which is the primitive needed for owner/meta socket authority hardening.
- The emitted daemon spine is real, but currently serial/asymmetric relative to the newer component requirements identified in the lojix stack: it does not yet host worker offload, two typed wire contracts into one Nexus root as a first-class path, or per-request runtime over a shared store.

## Cloud context

`cloud` is structurally close to the same problem space:

- It has two authority-tiered public contracts: `signal-cloud` and `meta-signal-cloud`.
- It has daemon-local `cloud/schema/nexus.schema` and `cloud/schema/sema.schema` artifacts generated through `schema_rust_next::build`.
- It has a schema-engine witness in `src/schema_daemon.rs` that binds ordinary and owner sockets and routes both contracts into one `nexus::SignalInput` root.
- It keeps a per-request `SchemaRuntime` over a shared `Arc<SchemaStore>`.
- The production binary still runs `crate::daemon::Daemon`, the hand-written Cloudflare-IO path, until provider IO lands on the schema effect plane.

So the latest core-crate daemon emitter is an alignment target for cloud, not an automatic replacement in its current form. The refreshed direction is stronger than passive deferral: evolve the emitter/runtime to host the needed properties, then let cloud adopt the generated/common daemon path. Cloud should adopt common/generated daemon machinery only when it preserves:

- first-class ordinary + meta contract routing into one daemon-local Nexus/SEMA runtime;
- per-request runtime isolation over shared store state;
- bounded frame/read handling;
- non-blocking provider work;
- owner/meta socket authority hardening from peer credentials, with unauthorized uid mismatch rejected fail-closed;
- no credential bytes in source, logs, or ordinary records.

## Permanent context refreshed

Updated files:

- `/git/github.com/LiGoldragon/cloud/INTENT.md`
  - Added core-crate alignment intent.
  - Made explicit that generated/common daemon surfaces must not regress cloud authority, concurrency, provider-effect, or store boundaries.
  - Added fail-closed owner/meta peer-credential authorization context.
- `/git/github.com/LiGoldragon/cloud/ARCHITECTURE.md`
  - Added a core-crate refresh note to the schema-engine track.
  - Contextualized the emitted daemon spine as alignment target, not current production cutover.
- `/git/github.com/LiGoldragon/signal-cloud/INTENT.md`
  - Replaced stale “scheduled to convert” language with landed schema-authored contract language.
- `/git/github.com/LiGoldragon/signal-cloud/ARCHITECTURE.md`
  - Replaced stale pending-schema section with current `WireContract` schema-language status.
  - Removed ephemeral report references from the architecture body.
- `/git/github.com/LiGoldragon/meta-signal-cloud/INTENT.md`
  - Added landed schema-authored owner/meta contract context.
- `/git/github.com/LiGoldragon/meta-signal-cloud/ARCHITECTURE.md`
  - Added current `WireContract` schema-language status.
- `/home/li/primary/protocols/active-repositories.md`
  - Updated cloud from “documentation-only at birth” to current production/schema-engine split.
  - Corrected `signal-cloud`/`meta-signal-cloud` plan-preparation ownership in the active repo map.

## Operator note

No deploy, service restart, provider mutation, or live cloud daemon run was performed. This was a documentation/intent/context refresh only.
