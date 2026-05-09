# Architecture Truth Pass

Reviewed current `ARCHITECTURE.md` files across the active workspace and used
recent reports plus commit recency to prefer the newer architecture. This pass
only changed high-certainty drift.

## Basis

- `reports/designer/79-architecture-files-audit.md` identified stale
  `persona-store`, store-actor, and `NexusVerb` / `NexusPattern` references.
- `reports/designer/78-convergence-with-operator-77.md` retired
  `signal-persona-store` and the shared store actor.
- `reports/operator/77-first-stack-channel-boundary-audit.md` confirmed that
  state belongs to the owning component actor, with `persona-sema` used as a
  library.
- Current `signal` / `signal-core` architecture says Nexus text is NOTA syntax
  projected outside the rkyv wire.

## Current Shape

```mermaid
flowchart LR
    "Nexus text" -->|"uses"| "NOTA syntax"
    "signal-core" -->|"frame kernel"| "signal-persona-*"
    "signal-persona-*" -->|"typed channel records"| "component actor"
    "component actor" -->|"owns write ordering"| "persona-sema"
    "persona-sema" -->|"typed tables over"| "sema"
```

## Edits Landed

| File | High-certainty correction |
|---|---|
| `/git/github.com/LiGoldragon/persona-harness/ARCHITECTURE.md` | Replaced `persona-store` with harness-owned state using `persona-sema`; added `signal-persona-harness` as the harness contract boundary. |
| `/git/github.com/LiGoldragon/persona-orchestrate/ARCHITECTURE.md` | Replaced `persona-store` with orchestrate-owned state using `persona-sema`. |
| `/git/github.com/LiGoldragon/persona-system/ARCHITECTURE.md` | Replaced `persona-store` with `signal-persona-system` observations and consumer-owned durable state. |
| `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md` | Removed store-actor framing; named `signal-persona-message` as the message channel contract and router-owned durable message state as the destination. |
| `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md` | Removed the last store/caller wording; router owns its database, not a shared database actor. |
| `/git/github.com/LiGoldragon/persona-sema/ARCHITECTURE.md` | Clarified that component actors own runtime write sequencing; `persona-sema` owns schema/table layout. |
| `/git/github.com/LiGoldragon/sema/ARCHITECTURE.md` | Clarified Sema as kernel; consumer runtime actors own mailboxes and external effects. |
| `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md` | Reworded non-ownership from store actors to consumer runtime actors. |
| `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md` | Clarified Nexus text as a NOTA-syntax projection outside the binary frame kernel. |
| `/git/github.com/LiGoldragon/signal/ARCHITECTURE.md` | Removed old sigil-pair reply wording; replies are typed records by position. |
| `/git/github.com/LiGoldragon/nexus-cli/ARCHITECTURE.md` | Replaced `Decoder::nexus`, `NexusPattern`, `NexusVerb`, and old sigil grammar with Tier 0 explicit verb records plus `NotaSum`. |

## Not Changed

- Historical reports keep their original claims unless a later report supersedes
  them. I did not rewrite report history.
- `nexus-spec-archive/ARCHITECTURE.md` still contains archived delimiter
  grammar. It is an archive, not current architecture.
- Repos whose `ARCHITECTURE.md` files only contained false-positive strings such
  as `todo!()` were not touched.

## Residual Known Work

- `primary-b7i`: migrate message body strings to typed Nexus records.
- `primary-28v`: naming sweep from verb-form command names to noun-form channel
  records.
- `primary-3fa`: converge focus and input-buffer observation contracts.
