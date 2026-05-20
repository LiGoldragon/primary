# 25 — handover

System-assistant handover after the signal-architecture convergence
arc settled into `reports/designer/247-radical-rethink-or-converge.md`
+ `reports/operator/143-signal-infrastructure-convergence-and-pilot-pivot.md`.
Drops three predecessor reports whose substance has migrated; carries
forward only what isn't already on disk somewhere durable.

## What landed (this lane's recent commits)

- **signal-lojix contract-local-verbs migration** —
  `/home/li/wt/github.com/LiGoldragon/signal-lojix/horizon-leaner-shape/`
  commit `ef98dc0a`. SignalVerb tags dropped; `Deploy`,
  `Pin`/`Unpin`/`Retire`, `Query`, `WatchDeployments` +
  `UnwatchDeployments`, `WatchCacheRetention` +
  `UnwatchCacheRetention` as contract-local operation roots.
  `DeploymentSubmission` → `DeploymentRequest`. Dep
  `signal-core` → `signal-frame`. All checks green via
  `nix --max-jobs 0 flake check -L` against the remote builder.
  ARCH gains a Migration history section.
- **STT canonical normalisations in `/home/li/primary/intent/`** —
  `intent/deploy.nota` + `intent/arca.nota` use `lojix` /
  `Nix` / `Arca` per `skills/stt-interpreter.md` (the canonical is
  the filesystem name; both "lojix" and "logix" are STT-heard
  forms of the same repo).
- **Workspace-wide `max-jobs 0` directive captured** in
  `intent/workspace.nota` (lock-free shell append) — all Nix
  builds delegate to the remote builder.
- **Earlier context-maintenance sweep** retired six of my earlier
  reports (16/17/18/19/20/21) per
  `reports/designer/215-workspace-state-of-art-2026-05-18.md`
  §4.6; substance had already migrated to
  `protocols/active-repositories.md`,
  `reports/system-specialist/136/138/141/139`, and D/213/214.

## Where the arc actually is (per /143 + /247 + /248)

The signal-frame/signal-executor architecture **is not being torn
up**. The current split holds: `signal-frame` owns the wire +
fanout primitives + macro; `signal-executor` owns lowering
orchestration + batch planning + abort semantics + projection
bridge; `sema-engine` owns durable state mechanics;
`signal-<component>` contracts own domain vocabulary; daemons
implement policy + lowering + projection.

The convergence bundle (per `reports/designer/246-v4-bundled-fix-deep-design-with-examples.md`
+ `reports/operator/142-signal-frame-executor-bundled-fix-logic-probe.md`
+ `reports/designer/248-three-layer-changes-for-operators.md`) crystallises
the three-layer model (psyche-affirmed 2026-05-20T02:00Z):

- **Layer 1 — Contract Operation** — external request language; owned by `signal-<component>` contracts (e.g. `LojixOperation::Deploy(DeploymentRequest)`).
- **Layer 2 — Component Command** — internal executable language, per-daemon; owned by each daemon (e.g. `LojixCommand::*` would live in the lojix-daemon crate).
- **Layer 3 — Sema Operation** — payloadless universal classification for observation; owned by `signal-sema` (just the six variants: Assert / Mutate / Retract / Match / Subscribe / Validate).

Concretely on the wire and in the trait shapes:

1. `Lowering` returns typed `OperationPlan<Command>` not
   `Vec<SemaOperation>` — adds `type Command` + `type ComponentEffect`
   associated types; structural ownership (one OperationPlan per source
   op) — no `sema_op_owners` sidecar.
2. `signal-sema::SemaOperation` becomes **payloadless** — pure
   classification. `PatternField<T>`, `Slot<T>`, `Revision` stay as
   workspace-shared primitives that components use inside their typed
   Commands. Component Commands impl `ToSemaOperation` for
   cross-component observation.
3. `AcceptedOutcome` splits into `Committed` /
   `OperationAborted { failed_at, reason }` /
   `BatchAborted { reason, retry, commit }`. Domain rejection rides as
   `SubReply::Failed { detail }` inside `OperationAborted`; engine
   atomic failure rides as `BatchAborted` with all-`Invalidated`
   per-operation slots; kernel `Reply::Rejected` narrows to true
   frame-level failures.
4. Each daemon defines its own `CommandExecutor` (engine adapter that
   knows the daemon's tables/indexes and executes its Commands
   atomically). The executor framework provides atomic boundaries +
   snapshots + redb transaction handling + failure classification.
5. Observation projection is opt-in via an extension trait
   (`ObservedLowering: Lowering`) with projection inputs taking typed
   component-local values (`Self::Operation`, `Self::ComponentEffect`)
   — not raw `SemaEffect`.
6. **Observable grammar simplified per v4**: the `observable` block
   drops `open <Verb>(Filter); close <Verb>;` lines. For persona
   components the macro hard-codes `Tap` / `Untap` (no author
   override). Non-persona small utilities don't declare an observable
   block. Domain contracts that need the verb `Tap` rename their
   domain verb.
7. After the bundle, the pilot is `signal-repository-ledger` +
   `repository-ledger` proving the end-to-end flow.

**Package 1** of the bundle (typed lowering rejection) is
**already landed** on `/git/github.com/LiGoldragon/signal-executor/`
`main` — `Lowering::lower()` returns
`Result<Vec<Self::Command>, Self::Reply>`; `Executor` builds
`Reply::Accepted { outcome: Aborted, per_operation }` with
Invalidated/Failed{detail}/Skipped via `domain_rejection_reply()`.
The current shape is slightly cleaner than what /141 sketched
(generalizes `SemaOperation` → typed `Command`).

**Package 2** as `reports/operator/141-...` defined it (contract-named
open/close verbs) is **stale under v4**. /246-v4 + /248 deleted the
author-named open/close grammar entirely; macro now hard-codes
`Tap`/`Untap` for persona components and contracts without a need for
observability drop the block. My in-flight attempt on `/git/.../signal-frame`
got wiped during a parallel agent's work — see "Discipline lesson"
below — but is moot regardless because the v4 grammar supersedes the
/141 shape.

## What's open — lojix-mesh-side residuals not absorbed anywhere

These were carried forward from `reports/system-assistant/23-most-relevant-questions-after-d214-op149-op150-2026-05-17.md`
§4 (now retired). None of them are absorbed in
`reports/designer/216-criome-routed-authorization-state-2026-05-18.md`,
`reports/designer/221-lojix-arca-horizon-leaner-shape-state-2026-05-18.md`,
or the convergence bundle reports — they're lojix-mesh-specific.

| Old ID | Live residual | Lean / suggested resolution |
|---|---|---|
| G3 | **Peer-daemon discovery for `peer_daemons` runtime population.** | v1: static configuration. v2: dynamic via clavifaber's node registry. Cross-link to `reports/designer/221-...` Q15 (`owned_cluster` shape). |
| G8 | **GC-root lifetime across participating daemons.** Builder pins build outputs; cache pins received outputs; target pins activated outputs. The "let go" event needs a wire signal. | Add `DeploymentReleased { request_id }` to `signal-lojix`. Issued by caller on observed activation; each role-daemon releases its pin on receipt. |
| G9 (partial) | **Concurrent-deploy + network-partition failure modes** not in `reports/system-specialist/137-lojix-self-deploy-cache-coordination-architecture-2026-05-17.md` §"Failure behavior". | Spec needed: behaviour when (a) two concurrent deploys to same target arrive; (b) network partitions builder↔cache mid-transfer. |
| G10 | **Cancellation wire shape.** | `CancelDeployment { request_id, scope: CancellationScope }` where `CancellationScope ∈ { PreBuild, MidBuild, PreActivate, MidActivate(force_rollback) }`. Activation is intrinsically uncancellable once `nixos-rebuild switch` is invoked — wire must reflect this. |
| G13 | **Per-deploy observability granularity.** | Per-phase events default; per-derivation events opt-in via subscription filter. Per-derivation could be tens of thousands per build; not a default. |
| G16 | **Concurrent deploys to same target.** | Per-target activation lock (already in `reports/system-specialist/137-...`). On lock contention: reject second with typed reason (caller decides retry). FIFO-with-rejection rather than queue. |
| G18 | **Idempotency.** `wire::DeploymentSubmission` has no idempotency key. | Add `idempotency_key: IdempotencyKey` field. Daemon dedupes by `(caller_identity, idempotency_key)` for a configurable window. Cheap now; hard later. The signal-lojix migration already pivoted the type to `DeploymentRequest` — adding `idempotency_key` to that record is a small follow-up. |

These will need an absorption sweep once the convergence bundle
settles enough that the lojix daemon migration starts.

## What's open — criome-side residuals not closed by /246 or /247

Most criome-side questions from `reports/system-assistant/22-...` and
`23-...` are now in
`reports/designer/216-criome-routed-authorization-state-2026-05-18.md`
§5. Three are still genuinely open and worth carrying forward:

- **Unattended-system-daemon bootstrap.** A `lojix-system` user's
  criome has no human at boot. v1 lean: master key unencrypted +
  filesystem permissions. v2: TPM-sealed with PCR-bound policy.
  Blocks cluster-side criome ship.
- **D/214 §1 mermaid drift.** Draws the peer socket as
  `mode 0660, group criome-peers`; `reports/system-specialist/142-criome-public-socket-and-deploy-approval-clarification-2026-05-17.md`
  corrected to "public + unencrypted; security via signatures +
  receiving daemon policy." Designer-lane to reconcile; concrete
  edit list lived in my earlier chat brief and is now lost — needs
  reproducing if the designer wants it as a report.
- **`owner-signal-criome` contract design pass.** ECDH cipher
  choice (Noise XX vs hand-rolled X25519 + HKDF-blake3 +
  ChaCha20-Poly1305/AES-GCM). Blocks tui-criome + CLI passphrase.

## Side notes

- **note: workspace canonical for the deploy CLI repo is `lojix`**
  (directory name; `skills/stt-interpreter.md` table). Both "lojix"
  and "logix" are STT-heard forms; the canonical for verbatim
  records and ARCH/code is the directory-derived form. My earlier
  attempt to apply the psyche's spelling correction L-O-G-I-X
  workspace-wide was wrong per the canonical-from-filesystem rule
  and got reverted.
- **note: criome IS a PKI** (D/214 §13). ClaviFaber registers
  nodes, criome masters anchor identity, peer routing is intrinsic.
  Makes TLS for cross-host transport much cheaper; unifies
  cross-component trust resolution. Worth keeping visible as
  cross-host transport gets designed.
- **possibly useful: Package 1 of the convergence bundle landed
  beyond what /141 sketched** — `signal-executor` now has a
  separate `Command` associated type (not just `SemaOperation`).
  The /246 v4 three-layer model (Contract Operation / Component
  Command / Sema Operation classification) crystallises this; any
  downstream Lowering impl picks its own typed Command type.
- **possibly useful: signal-lojix on `horizon-leaner-shape` is
  already partly aligned with /246's three-layer model** because
  the migration moved the contract-local verbs but did not yet
  introduce a typed Command type for the daemon side. When the
  lojix daemon migration starts, the daemon's `Lowering` impl
  picks `LojixCommand` + `LojixEffect`, impls `ToSemaOperation` on
  `LojixCommand`, impls `CommandExecutor`. If lojix is treated as
  a non-persona component, the observable block is optional —
  decide explicitly whether the deploy daemon wants Tap/Untap
  observability or not.
- **note: `reports/designer/249-component-intent-gap-analysis.md`**
  is persona-side gap audit. Two cross-cutting items relevant to my
  arc indirectly: (a) "`Tap`/`Untap` vs universal observer-hook
  consistency" is open — applies to lojix observability if/when it
  ships; (b) "skeleton honesty for ordinary + owner contracts" —
  the lojix daemon's `Lowering` impl should return typed
  `Unimplemented`-shaped replies for any unbuilt-but-decodable
  variants during the migration, not panic.

## Discipline lesson (mine)

Per `skills/feature-development.md`, foundation-crate work
belongs in a feature-branch worktree under
`~/wt/github.com/LiGoldragon/<repo>/<branch>/`, not in the
canonical `/git/...` checkout. The peer that has the Package 2
work did it correctly (in
`~/wt/github.com/LiGoldragon/signal-executor/signal-frame-executor-report-141/`);
I edited `/git/.../signal-frame` directly and got wiped. Future
foundation-crate edits in this lane start with `jj new` in a
worktree.

## Next-session pickup points

When the next system-assistant session opens:

1. Read this report + `reports/designer/247-radical-rethink-or-converge.md`
   + `reports/operator/143-signal-infrastructure-convergence-and-pilot-pivot.md`
   + `reports/designer/248-three-layer-changes-for-operators.md`
   (the operator-facing v3→v4 diff) to re-orient on the converged
   arc shape.
2. Check whether Package 2 (observable open/close grammar) landed
   in `/git/.../signal-frame/main`. If yes, the lojix daemon's
   future migration can use the new shape.
3. Check whether the pilot `signal-repository-ledger` +
   `repository-ledger` end-to-end work has progressed
   (`reports/operator/143-...` §"The Pivot"). The lojix arc
   migration tracks behind that pilot.
4. If `reports/designer/215-workspace-state-of-art-2026-05-18.md`
   has been refreshed for a later state-of-art, fold accordingly.
5. The unattended-bootstrap question is still the single biggest
   gating decision for cluster-side criome ship — surface to
   psyche if a deploy-stack cutover gets scheduled.

This handover retires once the lojix daemon migration starts (at
which point the §"What's open" residuals get absorbed into the
daemon's design / implementation reports) or when /143's "cognitive
pivot" (move pattern to persona-spirit / persona-mind) reshapes
the priority list.
