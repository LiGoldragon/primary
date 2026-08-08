# Fresh intent sweep — lojix/horizon engine rewrite (2026-06-05)

A CURRENT Spirit sweep across `lojix horizon nexus sema schema engine
cutover triad cluster-data deploy streaming`, agglomerated into today's
intent picture, verified against the GREEN triad-port schemas. This is a
fresh pass — it does NOT assume report 23's earlier agglomeration still
holds; the today-dated records (`9p8v`, `avvh`, `242o`, `z6qu`, plus the
streaming pair `brgo`/`2tfa`) re-anchor the picture.

## Method

Read-only. Spirit queried by ten topics (`SummaryOnly Deep`). Schemas
read direct from `/home/li/wt/.../lojix/triad-port/schema/{nexus,sema}.schema`
and the two wire contracts. Legacy parity measured against
`/git/github.com/LiGoldragon/lojix-cli/src/{build,activate,copy,check,deploy,cluster,request,stage}.rs`.
No build, no `jj`, no `cargo` (parallel workflow holds the working copy).

## (a) The settled charter and sequencing

| id | kind | cert | gist |
|---|---|---|---|
| `tvbn` | Decision | VeryHigh | The rewrite charter. Horizon stays a hack / simple projection surface, NOT a full triad. lojix is the traditional component that receives the full triad-engine + schema-component port and carries the runtime triad. Goal: finish the lean rewrite to cutover and retire the dual deploy stacks (Stack A production + Stack B next). Reach parity, then switch per node. Port high-confidence production CriomOS changes into the next stack immediately. |
| `fe2j` | Decision | High | Ordering is PORT-FIRST: complete the lojix triad-engine + schema-component port BEFORE cutting CriomOS over, then cut onto the ported daemon. Stack A is never retired onto a non-triad deployer. |
| `mkvb` | Decision | High | lojix is built on the triad engine + schema substrate (same schema-derived shape the other components converge on), not a hand-written hack. |
| `munq` | Constraint | High | Prototype audits must require the prototype to USE the designed components fully; when a component is too incomplete, develop it further rather than bypass it. |
| `v5d4` | Constraint | High | Passing sandbox testing is a precondition for the lean-stack cutover to main deployment. |
| `5au6` | Decision | (legacy) | The lean lojix/horizon stack becomes the main deployment after MVP. |
| `j9ba` | Decision | High | lojix-horizon logics work is a schema-deep rewrite on nota-next + schema-next; deep actor system, schema-defined interfaces AND data shapes, method-only Rust; psyche authorizes modifying schema-next itself if depth demands. Almost a full rewrite. |

The charter and sequencing are SETTLED and mutually consistent. No fork
remains on whether lojix is a triad (it is) or whether horizon is
(it is not — see (d)).

## (b) Nexus-as-feature-catalog — the governing principle for this work

| id | kind | cert | gist |
|---|---|---|---|
| `z6qu` | Principle | VeryHigh | **The Nexus interface is the engine's INTERNAL FEATURE INTERFACE; its MAIN reason for existing is VISIBILITY of internal features.** EVERY engine feature — any computation, any filtering/condition on results, any conditional write, any internal logic-feature — MUST be a declared Nexus verb+object in the schema. Internal features must NOT live as inline hand-written logic hidden from the schema. The nexus schema is the readable catalog of everything the engine can do. Per psyche 2026-06-05. |
| `3d5z` | Constraint | VeryHigh | Triad separation is strict and absolute: SEMA owns ALL durable-state code, Nexus owns ALL decision-making, Signal owns ALL communication. A daemon contains NO db boilerplate, NO decision-making, NO comms outside its engine. |
| `xq4z` | Correction | High | Nexus input and output are NOT symmetric lists of the same categories. Input = facts/replies/events to decide FROM; output = what Nexus commands/emits next. |
| `a71r` | Principle | VeryHigh | Every component conducts core logic through schema-emitted traits whose methods take/return root types of the planes. Trait surface uniform across components. |
| `l6zw` / `bodd` | Correction / Clarification | High | Contracts carry ONLY wire messaging vocabulary; Nexus and SEMA are daemon-internal and must NOT appear in any contract schema. Every contract repo must be audited for this leak. |
| `lc2r` | Correction | VeryHigh | A component is at least THREE separate plane schema files: wire Signal in the contract repos; Nexus and SEMA as separate `.schema` files INSIDE the daemon crate (e.g. `lojix/schema/nexus.schema`, `lojix/schema/sema.schema`), each importing the wire Signal IO. Not separate crates/repos. |
| `4vi4` / `iq57` | Clarification / Decision | High | Nexus may host a recursive computation engine (next object is a Nexus object, not a final reply) — a future runtime control substrate for prioritizing actor work and backpressure. |
| `9ypt` | Clarification | Medium | Nexus sits between two worlds: Signal = OUTER (clients), SEMA = INNER (durable state). Nexus is the center making decisions. |
| `k4d9` | Clarification | Medium | Generated internal Nexus nouns should not be promoted to the daemon crate root or public contract; keep internal Nexus vocabulary separate from wire-facing Signal APIs. |
| `de8i` | Principle | High | Schema→Rust lowering is methods-on-nouns (each Rust-model noun renders itself), not a god-struct emitter. (Touches generation, not the lojix schema directly, but governs how the catalog becomes code.) |

`z6qu` (VeryHigh, today) is the LENS for the completeness audit: the
nexus schema must be the COMPLETE, visible catalog of every internal
feature. The deploy pipeline's `EffectCommand` catalog and every
conditional/filter the daemon performs must be a declared Nexus verb —
nothing inline.

## (c) Runtime-state expectations (SEMA plane)

The SEMA plane is the four durable tables (ARCHITECTURE.md:44-65):
live generation set, GC-roots retention tree, append-only event log,
container-lifecycle mirror. Supporting intent:

| id | kind | cert | gist |
|---|---|---|---|
| `0fdy` | Decision | (firm) | Component databases use a `.sema` file extension (hiding redb), declaring the architectural role in the filename. |
| `qvyc` | Decision | (firm) | A daemon can run two databases concurrently — the transitory-database pattern is part of the SEMA interface (for live upgrades). |
| `1wn5` / `py4h` | Decision / Principle | High | Upgrade is realized AS SEMA operations on the Asschema; schema-changing ops are the same kind of operation on different objects. |
| `7l7l` | Decision | High | The six Sema classification words (Assert/Mutate/Retract/Match/Subscribe/Validate) are FORBIDDEN as request-root tags on any contract wire and must not be mirrored as an `AuthorizedSignalVerb` enum. Sema class is daemon-derived, never peer-sent. |
| `en7k` | Clarification | Medium | Splitting SEMA out of the daemon is a distant-future consideration only; not the current per-plane-crate design. |
| `ox7e` | Principle | High | Don't port storage needs onto a mismatched sema-engine API; improve the shared engine so generated SEMA expresses its real storage identity. |
| `jkkq` | Constraint | High | Production-candidate testing must include a production-copy handover test (seed prod-like .sema, copy, exercise candidate against copy, verify original untouched). |

The lojix `sema.schema` IS consistent with this: four table records
(`LiveSetTable`, `GcRootsTable`, `EventLogTable`,
`ContainerLifecycleTable`), typed `StateMarker` (CommitSequence +
StateDigest), and no Sema-classification words on the wire (the contracts
use domain verbs `Query`/`Deploy`/`Pin`, never `Assert`/`Mutate`).

## (d) The raw/pretty horizon decision (TODAY)

| id | kind | cert | gist |
|---|---|---|---|
| `9p8v` | Decision | High | Horizon splits into two clearly separated parts. RAW horizon = core typed cluster-data model (NodeService enum, typed facts, arch resolution, typed name/key-line newtypes, cross-node fan-in, typed validation, secret-binding resolution map). PRETTY horizon = separate layer adding pre-computed pre-derived helper variables Nix consumes (behaves-as / gating booleans like is-dispatcher / is-large-edge / enable-network-manager, resolved magnitudes, lid-switch policy, trust-gated extra-groups). Pretty helpers computed in typed Rust, NOT pushed into Nix; Nix only uses already-derived variables. Refines+supersedes m85j's mechanism: derive seam is the typed pretty layer, not a CriomOS Nix derive module; magnitudes pre-resolved not raw ordinals. Timing from m85j stands — pretty lands after cutover, parity is the bar, collapse does not gate cutover. Typed-source-first preserved end to end. |
| `avvh` | Clarification | High | The raw/pretty split is ALSO a forward-integration seam, not only anti-tangling. RAW horizon kept as a clean minimal typed cluster-data model keeps the door open to promote raw horizon into a real component later, while pretty stays the typed derive layer Nix consumes. Connects to the open `x8iv` fork (does horizon become a full triad?) and to `tvbn` (horizon is a projection hack for now): the split makes the later promotion a clean step rather than a rewrite. |
| `a2t4` | Principle | VeryHigh | Horizon + cluster-data minimal on TWO axes: (1) semantic boundary — Horizon expresses only WHAT the psyche wants the cluster to do (simple typed facts), never HOW / never decision-making; Nix composes the decisions downstream. (2) type-count — data types do NOT repeat across inputs and outputs; reuse the input type as output where possible. Minimal at the boundary AND minimal in type count. |
| `vu2k` | Clarification | High | A pure-projection Horizon needs the types-only-module schema shape: a 4-position schema forces a signal plane, so Horizon (pure library, no runtime triad) needs a types-only-module variant so datatypes generate WITHOUT forcing an Input/Output plane. Surviving mechanical constraint from the now-closed Horizon-runtime-shape trichotomy. |
| `qkvx` | Correction | High | Cluster-data node-service features MUST be typed end-to-end, never string-keyed. Order is typed-source-first: extend the horizon model → author the fact → project typed → consume typed. The string-keyed VmTesting work was garbage. |
| `242o` | Constraint | VeryHigh (TODAY) | Ouranos swap and zram config expressed through cluster-data + Horizon projection, NOT a host-local CriomOS override. The first concrete typed-cluster-data feature the rewritten horizon must carry. |
| `6njo` | Correction | High | Name the ROLE not the host: `NodeService::LargeAi` (large-ai-node), not "Prometheus". Refresh existing host-named references. |

The raw/pretty split is SETTLED as of today (9p8v High + avvh High). The
ordering — pretty lands after cutover, parity is the cutover bar — is
explicit and does NOT gate cutover. `242o` is the new VeryHigh concrete
demand: swap/zram via cluster-data is the next typed-source-first feature.

## (e) Minimalism / type-reuse principles

`a2t4` (VeryHigh) is the upstream minimalism principle: minimal at the
semantic boundary (WHAT not HOW) AND minimal in type count (no in/out
repetition; reuse input type as output). `qkvx` enforces typed-source-
first. These govern BOTH horizon's model AND — by `a71r` uniformity —
the lojix plane schemas. Note: the lojix contracts already practice this
(shared record types defined ONCE in signal-lojix, cross-imported by
meta-signal-lojix; the nexus/sema schemas import rather than redeclare).

## (f) Streaming substrate (TODAY's pair) and OPEN forks

### Streaming — now DECIDED in direction, but the substrate is a platform project

| id | kind | cert | gist |
|---|---|---|---|
| `brgo` | Decision | High (TODAY) | Chosen direction is FULL schema-derived streaming — not poll-as-permanent, not a lojix-only hand-wired carve-out. Teach schema-next to express an event/stream root with opens+belongs; teach schema-rust-next to emit the event frame reaching signal-frame's existing-but-unused `StreamingFrameBody` + `ObservableSet` pub/sub; add a push action + subscriber registry to the triad-runtime runner. Platform project across the shared engine, cheaper because the substrate already exists in signal-frame. lojix Watch gets real push once it lands; UNTIL then handshake+poll suffices and does NOT block cutover. **Open question carried:** was the existing signal-frame streaming substrate deliberate scaffolding or leftover — which most changes the effort estimate. |
| `2tfa` | Decision | High (TODAY) | signal-lojix carries WatchDeployments + WatchCacheRetention from day one, NOT deferred. The port accepts being the first component to prove schema-derived streaming-subscription emission; if the generator can't yet emit streams, that enhancement is on the lojix port path rather than dropping streaming from the contract. Deploy phase events + cache-retention transitions are pushed not polled. |
| `vudl` | Decision | High | lojix uses the two-contract authority split. Deploy/Pin/Unpin/Retire = owner-only policy → meta-signal-lojix. Query + the two Watch subscriptions + Unwatch = peer-callable → ordinary signal-lojix. Born meta-signal-lojix, never owner-signal-. Until cutover, carry meta-signal-lojix as a local path-dependency package inside the lojix tree; create the standalone repo AT cutover. |
| `3chp` | Decision | High | The policy/control socket is the META socket, not the owner socket. |

The contracts are CONSISTENT with brgo/2tfa: signal-lojix already carries
`WatchDeployments`/`WatchCacheRetention` as the request→`SubscriptionToken`
handshake form (the emittable shape), with `DeploymentPhaseEvent` /
`CacheRetentionTransitionEvent` defined once as namespace records. The
nexus/sema schemas carry both event payloads. So the day-one decision is
HONORED at the schema level; only the generator's event-frame emission is
the named follow-on (matches report 25's three-layer streaming analysis).

### OPEN forks still unresolved

1. **`x8iv` — horizon-rs vs horizon-next, and does horizon become a full
   triad.** `avvh` (today) explicitly references this fork as still open:
   the raw/pretty split is *designed so* a later promotion of raw horizon
   into a real component is a clean step — but WHETHER that promotion
   happens, and which checkout (`horizon-rs` the hack vs `horizon-next`
   the schema-derived successor) is the forward base, is NOT decided.
   Today's records make the split, not the promotion. STILL OPEN.

2. **Parity scope for cutover.** `tvbn`/`fe2j` say "reach parity then
   switch", `v5d4` makes sandbox-pass a precondition — but the EXACT
   parity surface that gates cutover is not enumerated in intent. The
   legacy Stack A surface (build.rs SystemAction Eval/Build/Boot/Switch/
   Test/BootOnce; activate.rs EFI reconcile + boot-once two-reboot
   semantics + home activation; check.rs key-material diff; copy.rs
   closure copy; stage.rs remote-input staging) is the de-facto parity
   bar, but intent does not say which of these MUST be at-parity before
   cutover vs may-follow. This is a designer/operator judgment gap, not a
   contradiction. OPEN.

3. **meta-signal-lojix standalone timing.** `vudl` decides the repo is
   "born meta-signal-lojix" and "created AT cutover", carried until then
   as a local path-dependency. The trigger ("at cutover") is named but
   the mechanical sequencing (when in the cutover does the repo split)
   is unstated. Minor open seam.

4. **Streaming substrate provenance.** `brgo` explicitly CARRIES the open
   question: was signal-frame's `StreamingFrameBody`/`ObservableSet`
   deliberate scaffolding ahead of this work, or leftover? This most
   changes the streaming effort estimate. OPEN (and named as carried).

5. **schema-next event/stream grammar + schema-rust-next emission.**
   Implied open by `brgo`/`2tfa`: the generator cannot yet emit a
   daemon-pushed event frame (no event/stream root, no opens/belongs).
   This is the named follow-on enhancement on the lojix path, not a
   contradiction. OPEN as a platform task.

## STALE / contradicted records to flag (NOT an instruction to remove)

These should be REFRESHED or tombstoned by an intent-maintenance pass;
flagging only, per the carry-uncertainty discipline.

| id | issue |
|---|---|
| `m85j` (referenced by 9p8v) | Its MECHANISM is explicitly superseded by `9p8v` — the derive seam is the typed pretty-horizon layer, NOT a CriomOS Nix derive module; magnitudes are pre-resolved, not raw ordinals. Only m85j's TIMING survives. Flag for refresh so the record's mechanism half doesn't mislead. |
| lojix `ARCHITECTURE.md` (the FILE, not a Spirit record) | Stale vs current intent: dated 2026-05-15; describes a SINGLE socket `/run/lojix/daemon.sock` (contradicts the two-contract / two-socket / meta-socket split of `vudl`+`3chp`); frames storage as `sema-engine`/`signal-core` (the triad-port is on `schema_runtime` + signal-frame + the `.sema` engine); code map lists `live_set.rs`/`gc_roots.rs` Kameo actors that the schema-runtime composition supersedes; says "push never poll" as an invariant while `2tfa`/`brgo` accept handshake+poll until the streaming substrate lands. NOT a Spirit record — flag for the same-branch INTENT/ARCHITECTURE manifestation pass (AGENTS.md continuous-manifestation rule). |
| `6njo` (host-vs-role naming) | Still LIVE intent, but names a refresh chore ("refresh existing references to Prometheus that should be role-level") that the lojix ARCHITECTURE.md and nexus schema comments do NOT yet honor (the nexus.schema header comment still references prometheus). Flag the chore as outstanding, not the record as stale. |
| Older spirit-cutover deploy records (`y35z`, `bo17`, `6px0`, `a5u7`, `zcga`, `px6d`, `s5dz`) | These are persona-spirit cutover mechanics, surfacing under the `deploy` topic but UNRELATED to the lojix/horizon engine rewrite. Not stale per se; flag as topic-noise so a future lojix sweep doesn't conflate spirit-daemon cutover with the deploy-stack cutover. |

## Nexus-completeness finding (the audit z6qu demands)

Measured the lojix `nexus.schema` EffectCommand catalog against the legacy
Stack A deploy pipeline. The catalog is GOOD but has identifiable GAPS vs
parity — each a feature that today would be inline-or-absent rather than a
declared Nexus verb (a `z6qu` violation if it lands as hidden logic):

**Covered well.** `EffectCommand` = ResolveFlakeAuth, NixEval, NixBuild,
CopyClosure, ActivateGeneration, PathInfoGc. `NixBuild` carries a
`BuildTarget [Local (Remote BuilderNode)]` — correctly modeling the
local-dispatcher-vs-remote-builder split (legacy build.rs `BuildLocation
{ Dispatcher, Builder(SshTarget) }`) AND honoring the dropped
hallucinated local-build guard (`783n`). `ExtraSubstituter` carried.
`EffectStage`/`EffectFailure` give typed per-stage failure. The
`NexusWork`/`NexusAction` model correctly follows `xq4z` (input = arrived
facts/completions; output = commands/replies/continue).

**Gaps vs legacy parity (each a candidate Nexus verb/object, flagged for
the designer who completes the catalog — NOT edited by this read-only
pass):**

1. **Remote-input staging is absent.** Legacy `stage.rs`
   (`RemoteInputStage`, `GeneratedInput` for horizon/system/deployment/
   secrets, MakeDirectory + Synchronize commands) materializes override
   flake inputs and rsyncs them to the target before the build. There is
   NO `StageInputs`/`MaterializeFlakeInputs` EffectCommand. Either this is
   subsumed by `ResolveFlakeAuth`+`NixEval` (unlikely — staging is a
   distinct rsync-to-host IO step) or it is a missing catalog entry.

2. **EFI / bootloader reconcile is not a declared effect.** Legacy
   `activate.rs` has `requires_efi_reconcile`, `step_set_efi_default`,
   `step_clear_efi_oneshot`, and the BootOnce two-reboot one-shot
   semantics (set new gen as one-shot, default stays on current). The
   nexus `ActivateGenerationCommand` carries only `ActivationKind`
   (Switch/Boot/Test/BootOnce) — the EFI-reconcile sub-steps and the
   one-shot/clear-oneshot logic are conditional internal features that
   `z6qu` says must be VISIBLE as Nexus verbs/objects, not inline inside
   an activate handler. Candidate: a typed `ActivationPlan` /
   `EfiReconcileStep` object, or an effect-result that exposes the
   reconcile decision.

3. **Home activation is collapsed into the OS path.** Legacy carries a
   distinct `HomeActivation` (profile_invocation / activate_invocation /
   remote variants) and `HomeMode [Build Profile Activate]`. The wire
   `meta-signal-lojix` carries `HomeDeployment`+`HomeMode`, but the nexus
   `EffectCommand` catalog has no Home-specific activate/profile effect —
   the home path's profile-set + activate steps are not visible as Nexus
   verbs. Candidate: a `ProfileHomeGeneration` / `ActivateHomeGeneration`
   effect, or an explicit branch in ActivateGeneration keyed on
   DeploymentKind.

4. **Key-material check is a SEMA read only; the DIFF is invisible.**
   `CheckKeyMaterial` is a SemaReadInput and the wire has
   `CheckHostKeyMaterial`, but the legacy `check.rs::diff` (comparing
   horizon-declared SecureShell/Yggdrasil public keys + Yggdrasil address
   against the host publication, producing typed `Mismatch`/`Report`) is a
   COMPUTATION — exactly the "any filtering or condition on results"
   `z6qu` says must be a Nexus verb. Today it would be inline in a read
   handler. Candidate: a `DiffKeyMaterial` NexusWork/Action object so the
   comparison is a declared feature.

5. **GC retention slot transitions are not declared as Nexus decisions.**
   The wire `CacheRetentionTransition [Pinned Unpinned Promoted Demoted
   Retired Evicted]` names the transitions, and SEMA has the
   `GcRootsTable`, but the DECISION logic — promote/demote/evict based on
   slot policy (current/boot-pending/rollback-N/pinned/recent, narinfo TTL
   two-phase deletion per ARCHITECTURE.md:47-55) — has no Nexus verb.
   `PathInfoGc` runs the GC, but the conditional retention-policy
   reasoning that decides WHAT to collect is a `z6qu` internal feature
   that must be a declared Nexus object, not inline.

These five are the concrete completeness gaps. Each is a place where, if
implemented as inline handler logic, the engine would violate `z6qu`
(VeryHigh, today). The recommendation for the catalog-completion designer:
model staging, EFI-reconcile, home-activate, key-material-diff, and
retention-policy decision as declared Nexus verbs/objects before the
handlers are written, so the nexus schema stays the complete visible
feature catalog.

## Bottom line

The charter (a), the Nexus-catalog principle (b), the SEMA expectations
(c), the raw/pretty split (d), and minimalism (e) are SETTLED and mutually
consistent as of today's records. The current triad-port schemas are
faithful to all of them. The live open forks are (f): x8iv horizon
promotion, parity-scope enumeration, meta-signal-lojix split timing,
streaming-substrate provenance, and the schema-next/schema-rust-next
event-frame emission task. The actionable NEW finding is the Nexus
feature-catalog completeness audit: five legacy-parity features (remote-
input staging, EFI reconcile, home activation, key-material diff, GC
retention-policy decision) are not yet declared Nexus verbs/objects and
must become them per `z6qu` before they are implemented inline.
