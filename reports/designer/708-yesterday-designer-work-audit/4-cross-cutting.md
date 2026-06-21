# 708-4 — Cross-cutting analyses

Three cross-repo passes. Architecture coherence (with mermaid) lives in `1-size-and-architecture.md`.

I now have everything needed. `replace_repositories` and `replace_worktrees` share an identical "collect existing keys -> remove each -> upsert each" skeleton (the only difference is the key derivation), confirming the registry/storage mirroring with extractable common shape. Let me write up the audit.

## Cross-repo repetition

This audit covers yesterday's designer work plus the surrounding contract/runtime repos it touches. The headline is one large, real, and now-fixable schema duplication that the per-repo maps flagged only as "deferred"; the smaller findings are hand-written boilerplate and storage-layer mirroring. The two reuse goals — single-sourcing the criome decision mapping and reusing `ObservationModel`/`RenderNota` in the GUI — were both **achieved correctly**, so they are confirmations, not problems.

### (a) Same type defined in more than one place — the `signal-standard` regression

`signal-standard` **already exists as a built crate** (`/git/github.com/LiGoldragon/signal-standard/src/schema/lib.rs`, with `tests/round_trip.rs` exercising it). Its whole purpose (Spirit eeeo) is to be the one home for cross-component vocabulary. Yet every consumer still carries a local copy, and yesterday's `meta-signal-mentci` work re-declared two of these types fresh rather than importing them. The schema comments call these "deferred cross-imports … while signal-standard is not yet a crate" — that premise is now false.

`ComponentKind` — the closed 14-variant roster — exists verbatim in **four** schemas:

- `/git/github.com/LiGoldragon/signal-standard/schema/lib.schema:31` (the intended canonical, zone-partitioned)
- `/git/github.com/LiGoldragon/meta-signal-mentci/schema/lib.schema:130` (re-declared, comment admits "Declared local here PENDING the signal-standard crate")
- `/git/github.com/LiGoldragon/signal-persona/schema/lib.schema`
- `/git/github.com/LiGoldragon/signal-criome/schema/lib.schema`

`AuthorizedObjectKind` / `ComponentObjectInterest` / `AuthorizedObjectInterest` — the four-rung interest lattice — are duplicated between `signal-standard` (which says it "Lifted from signal-criome") and the still-live original in `signal-criome/schema/lib.schema:220-231`. signal-standard lifted them but signal-criome never retired its copy.

`SocketPath` / `StandardSocket` is the worst spread — **eight** schemas declare a `SocketPath`/`StandardSocket`: signal-standard, meta-signal-mentci, signal-mentci, signal-criome, signal-persona, signal-terminal, signal-router, signal-message. And the modeling has already silently forked:

```
;; signal-standard/schema/lib.schema:120  (the rich, intended shape)
StandardSocket [ UnixSocket(SocketPath)  NetworkSocket(NetworkEndpoint) ]

;; meta-signal-mentci/schema/lib.schema:98  (yesterday's narrowed struct copy)
StandardSocket { path.SocketPath }
```

These are the same name with **different shapes** (an enum with a network case vs. a single-field struct), which is exactly how a "deferred import" silently becomes a contract fork. Zero repos currently `use signal_standard` (`grep -rln signal_standard` over all the contract `src/` returns nothing but doc/comment hits).

### (b) Same hand-written pattern in each signal-* / meta-signal-* repo

The hand-written `src/lib.rs` ergonomics layer is copy-pasted. `signal-mentci/src/lib.rs:1-38` and `signal-criome/src/lib.rs:1-39` are byte-identical across:

- the mod attribute block `#[rustfmt::skip] #[allow(clippy::large_enum_variant, dead_code, private_interfaces)] pub mod schema;` + `pub use schema::lib::*;`
- the alias septet `<Name>Request/Reply/Frame/FrameBody/ReplyEnvelope/RequestBuilder/OperationKind` (the only delta is the `Mentci`/`Criome` prefix word)
- `impl Input { pub fn operation_kind(&self) -> InputRoute { self.route() } }` — identical in both
- the `string_accessor!` macro definition itself:

```rust
macro_rules! string_accessor {
    ($($type:ident),* $(,)?) => {
        $( impl $type { pub fn as_str(&self) -> &str { self.payload().as_str() } } )*
    };
}
```

This macro is **re-defined privately in each repo** (confirmed in signal-mentci and signal-criome; meta-signal-mentci hand-writes the same `as_str` body inline at `src/lib.rs:19`). This is a generator gap: `as_str()` over string newtypes, `value()` over integer newtypes, the `operation_kind` route shim, and the channel-alias septet are mechanical and should be schema-emitted (or live in one shared `signal-derive`/`signal-frame` macro), not hand-copied per contract.

Naming note surfaced while reading: `signal-criome/src/lib.rs:43-44` declares `PrincipalId` and `PrincipalName` side by side — `PrincipalId` violates the spell-identifiers-as-full-words override (`Identifier`, not `Id`).

### (c) orchestrate worktree registry vs. StoredRepository

The two registries mirror structurally but have **diverged in elaboration**, not in contract — there is no wrong type here, just an unextracted common skeleton. `WorktreeRegistry` (`/git/github.com/LiGoldragon/orchestrate/src/worktree.rs:30-156`) and `RepositoryRegistry` (`/git/github.com/LiGoldragon/orchestrate/src/repository.rs:5-45`) both:

- hold the identical `{ tables: &'tables OrchestrateTables, layout: &'tables OrchestrateLayout }` pair with an identical `new`
- `refresh()`: `create_dir_all` a root, `read_dir`, skip non-dirs, skip `.`-prefixed names, push to a Vec, `sort_by`, then `replace_*`

The worktree `refresh` even documents the parallel in its own comment ("Mirrors `crate::RepositoryRegistry::refresh`"). The shared "scan a directory of dirs, skip dotfiles, parse the name into a typed token, collect+sort+replace" loop is duplicated; worktree just nests one level deeper (`<repo>/<branch>`) and derives jj facts. At the storage layer the mirroring is tighter still — `replace_repositories` (`tables.rs:251`) and `replace_worktrees` (`tables.rs:287`) are the **same algorithm**: collect existing keys, `remove_if_present` each, then upsert each; the only difference is `.name` vs. `StoredWorktree::key()`. That "diff old keys against new, replace the table" body is begging for a single generic `replace_table_by_key(table, items, key_fn)`.

### (d) ObservationModel / RenderNota re-implementation — none (confirmed reused)

`mentci-egui` correctly **consumes** the shared model rather than re-implementing it. `src/app.rs:13` imports `ObservationModel, RenderNota, RenderOrigin, RenderedObject, EngineEvent, ...` from `mentci_lib`; it holds `model: ObservationModel` (`app.rs:32,48`), routes gestures through `self.model.on_user_event(...)` and `self.model.on_engine_event(...)`, and renders every payload via `reply.render_nota(RenderOrigin::Reply)`. No approval state machine, no per-socket slot map, no NOTA projection is reimplemented in the shell — its only approval references are read-only display of `view.approval.pending_count/answered_count` (`app.rs:166-167`). This is the intended thin-client shape; report 707-1's "orphaned mentci-lib" finding is genuinely closed.

One narrow related observation (not in mentci-lib's scope): the criome **decision** projection is now single-sourced — `mentci/src/criome_bridge.rs:40` delegates to `mentci_lib::CriomeVerdict::from_decision` and the only `ApprovalDecision -> AuthorizationApprovalDecision` match lives at `mentci-lib/src/decision.rs:65`. But the daemon CLI keeps a **parallel verdict vocabulary** at `mentci/src/client.rs:146-150`, mapping `criome:approve|reject|defer` strings straight to `AuthorizationApprovalDecision`. That is a different concern (CLI atom parsing, not the closed-decision projection), so it is not a duplicate of `from_decision` — but it is a second hand-maintained approve/reject/defer table that will drift if the verdict set ever grows.

## Three highest-value consolidation opportunities

1. **Adopt `signal-standard` and retire the local copies — the deferral is over.** signal-standard is a real crate today, so the "deferred cross-import" comments in meta-signal-mentci, signal-criome, and signal-persona are stale. Replace the local `ComponentKind`, `AuthorizedObjectKind`, `AuthorizedObjectInterest`/`ComponentObjectInterest`, and `SocketPath`/`StandardSocket` declarations with `{ ComponentKind signal-standard:lib:ComponentKind }`-style imports. Do this **before** the meta-signal-mentci `StandardSocket { path }` struct and signal-standard's `StandardSocket [UnixSocket | NetworkSocket]` enum diverge further — they already disagree on shape, which is a live contract fork hiding behind a shared name. Highest value because it eliminates a 4-way and an 8-way duplication and stops an active drift.

2. **Emit the per-contract `src/lib.rs` ergonomics from the generator instead of hand-copying.** The `string_accessor!` macro, the integer-newtype `value()`, `impl Input { operation_kind }`, and the `<Name>Request/Reply/Frame/FrameBody/ReplyEnvelope/RequestBuilder/OperationKind` alias septet are mechanical and currently re-typed in every signal-*/meta-signal- repo. Have schema-rust-next emit `as_str()`/`value()` directly on the newtypes (the schema already knows which are string- vs integer-backed) and provide the channel aliases from one shared place. This removes the largest body of true copy-paste across the whole contract fleet and closes the gap that forces each repo to hand-write the same macro. (Fold in the `PrincipalId -> PrincipalIdentifier` rename while touching signal-criome.)

3. **Extract orchestrate's "replace table by key" and "scan dir of typed-named dirs" skeletons.** Add one generic `OrchestrateTables` helper — `replace_table_by_key(table, items, key_fn)` — and collapse `replace_repositories`/`replace_worktrees` (and any future `replace_*`) onto it; the bodies are identical but for the key function. Then lift the shared `refresh` scan shape (create root, read_dir, skip non-dirs and dotfiles, parse typed name, collect+sort+replace) so `RepositoryRegistry` and `WorktreeRegistry` differ only in their per-entry derivation. Lower blast radius than 1–2 but removes the registry/storage mirroring the prompt flagged and makes the next registry trivial to add.

Relevant files: `/git/github.com/LiGoldragon/signal-standard/schema/lib.schema`, `/git/github.com/LiGoldragon/meta-signal-mentci/schema/lib.schema` (lines 80-145), `/git/github.com/LiGoldragon/signal-criome/schema/lib.schema` (lines 220-231), `/git/github.com/LiGoldragon/signal-mentci/src/lib.rs` (lines 8-57), `/git/github.com/LiGoldragon/signal-criome/src/lib.rs` (lines 8-56), `/git/github.com/LiGoldragon/orchestrate/src/worktree.rs`, `/git/github.com/LiGoldragon/orchestrate/src/repository.rs`, `/git/github.com/LiGoldragon/orchestrate/src/tables.rs` (lines 247-300), `/git/github.com/LiGoldragon/mentci/src/client.rs` (lines 146-150), `/git/github.com/LiGoldragon/mentci-egui/src/app.rs` (reuse confirmation, no action needed).

Two more confirmations: the egui still does one-shot observe (`daemon_client` even says "mentci-daemon does not expose a live meta socket yet" — meta mode is still a placeholder, confirming the daemon meta-socket bind enabler is NOT done), and the criome park pickup is one-shot on observe (`a62c59e`), not the continuous subscription synthesis 4 described.

## Report-vs-reality

| Claim (from reports) | Reality on main / disk | Status |
|---|---|---|
| mentci-lib re-founded on live contracts: `0731c374`, depends on `signal-mentci` not `signal`, no `DaemonRole::Criome/Nexus`, no duplicate approval vocab (447, 707-9) | True. `mentci-lib` HEAD=main=origin `0731c37`; Cargo.toml deps are all branch=main (no `signal`, no local `[patch]`); `ObservationModel`/`ApprovalModel`/`RenderNota`/`CriomeVerdict` all present | Accurate |
| signal-mentci public readers `58dd5a26` landed, prototype `[patch]` removed (447) | True. HEAD=main=origin `58dd5a2`, clean | Accurate |
| mentci-egui `8c8b426e` consumes `mentci-lib::ObservationModel` + `RenderNota`, patches removed (447) | True. HEAD=main=origin `8c8b426`, consumes shared model | Accurate |
| mentci daemon `ada04788` bridge uses `mentci_lib::CriomeVerdict` for closed-decision→criome mapping (447); 707-9 framed this as "when convenient" | True and done. `criome_bridge.rs:40` calls `CriomeVerdict::from_decision(...)`; `use mentci_lib::CriomeVerdict` present | Accurate (the "when convenient" handoff is closed) |
| Orchestrate triad landed: signal `a785cc77`, meta `135c2e7a`, daemon `0cd09045`; worktrees table, scanner, projection, schema bump 2→3 (447, 707-9) | True on main. All three HEAD=main=origin at those SHAs; `worktree.rs`/`worktree_projection.rs`/`StoredWorktree` present; `tables.rs:44` `SCHEMA_VERSION = 3` with the 2→3 comment | Accurate (source only — see migration row) |
| Codegen pin skew resolved; all orchestrate repos resolve schema-next `4b7e830a` + schema-rust-next `90d853c3` (447, 707-9) | True. All three Cargo.lock files pin exactly those two SHAs | Accurate |
| Tests green: mentci 9/9 model + clippy; orchestrate signal 33 / meta 5 / daemon 38 (707-9) | Plausible but unverified by me; reports cite TEMP-store runs. Code is present and self-consistent. Operator 447 re-ran `cargo test`/`clippy` per repo | Likely accurate (claim is "tested against TEMP stores", not against live redb) |
| Preservation bookmarks pushed for both schema-rust-next trees; unique-unpushed revset now empty (707-9, 445, 446) | True. `origin/operator/preserve-schema-rust-next-reaction-expand` (`8b147fac`) and `...-structural-forms-integration` (`a0138ce1`) exist; plus two schema-next preserve refs; tip commits present on origin | Accurate |
| Merged feature bookmarks retired (`re-found-on-live-contracts` ×3, `*-worktree-registry` ×3) (447) | True. Zero matching refs in all six repos | Accurate |
| "Schema-version bump needs a sema-upgrade migration on the live store at integration" — flagged as integration concern (707-9 #1) | NOT done. Live daemon binary is dated **Jun 18 10:33** = the old schema-2 build, still running (PID 653243); `orchestrate.redb` not migrated; no live `worktrees.nota` exists. Source landed; live runtime never rebuilt/restarted | Open follow-up — claimed-as-flagged, still owed |
| egui gains "live subscription + per-component panes + the approval card" (synthesis 707-4 plan) | Partial. egui has per-component panes + an approval **summary** (pending/answered counts) only. No interactive approval card, no verdict submission — only an "observe" button. `daemon_client.rs:114` literally says "mentci-daemon does not expose a live meta socket yet" → still one-shot observe, no live subscription, meta mode still placeholder | Open follow-up (707-9 itself defers the card to "next slices"; reports do NOT claim it as done) |
| Daemon enablers: "bind the meta socket" + "continuous criome park subscription" (synthesis 707-4 plan) | Not delivered. Daemon has no live meta socket (egui client confirms); criome park pickup is one-shot on observe (`a62c59e`/`criome_bridge.rs`), not continuous | Open follow-up (plan item, never claimed done in wave-2 results) |
| GC pass gated on `worktrees.nota` landing live + re-verify (707-9) | Not run, correctly. `nota-next/` and `upgrade/` empty parent dirs still present under `~/wt/github.com/LiGoldragon/`; merged/archive worktree set still on disk; the gate (live manifest) is itself unmet | Open (correctly gated) |
| "designer lock still advertises the old mentci-lib feature worktree… should be released by the designer lane" (447) | Still true. `designer.lock` still contains `.../mentci-lib/re-found-on-live-contracts` + `[mentci-lib-refound]`; the worktree dir still exists on disk | Open follow-up — accurately flagged, still owed |
| CLI `orchestrate worktree list/register/refresh` adapter "deferred… follow-up once contracts land" (707-9, 447) | Confirmed absent. `orchestrate-cli/src/bin/orchestrate.rs` handles only `claim/release/status/verify-jj`; no `worktree` verb | Open follow-up — accurately deferred, still owed |
| CLI read+answer atom roster + criome+mentci `runNixOSTest` "next slices" (707-9, 447) | Absent. mentci bins: daemon, write-configuration, pickup-witness-test — no observe/answer atom CLI. No criome nix referencing mentci; `criome-nixos-module-142` worktree still un-recycled | Open follow-up — accurately deferred, still owed |

No place where a report claims something is on main that is actually missing. Every "landed" SHA is verified at `HEAD = main = origin/main`, clean. The one genuine report-vs-reality tension is the **live orchestrate daemon**: 447 says "all touched code checkouts are clean and aligned with origin main," which is true for source, but the report does not flag that the **running daemon is still the old schema-2 binary** — the schema-3 migration it itself listed as an integration concern (707-9 #1) is unaddressed, so the registry is on main but dead in production.

## Open follow-ups still owed

- [ ] **Live orchestrate redb schema migration 2→3 + daemon rebuild/restart.** Source landed (`SCHEMA_VERSION=3`), but PID 653243 runs the Jun-18 schema-2 binary and `orchestrate.redb` is unmigrated; no live `worktrees.nota`. The registry is inert until the daemon is rebuilt and the sema-upgrade runs. (707-9 integration concern #1; owner: operator/maintainer)
- [ ] **`orchestrate worktree list/register/refresh` CLI adapter** in primary `orchestrate-cli` — does not exist; only `claim/release/status/verify-jj`. (707-9 / 447 deferred)
- [ ] **mentci CLI read+answer atom roster** (grep-assertable, prints shared `RenderNota`) — no observe/answer bin exists. (707-9 / 447 next slice)
- [ ] **egui interactive approval card** — only a pending/answered summary + observe button today; cannot submit a verdict. This is the still-inert `gc0n` psyche-escalation surface. (707-4 plan / 707-9 next slice)
- [ ] **egui live subscription + daemon meta-socket bind** — egui still one-shot observe; `daemon_client.rs` says the daemon "does not expose a live meta socket yet"; meta mode still placeholder. (707-4 daemon enablers + egui plan)
- [ ] **Continuous criome park subscription in the daemon** — park pickup is one-shot on observe (`a62c59e`), not the continuous subscription synthesis described. (707-4 daemon enabler)
- [ ] **criome+mentci `runNixOSTest` on Prometheus** — does not exist; `criome-nixos-module-142` template worktree still un-recycled. (707-9 / 447 next slice)
- [ ] **schema-rust-next capability-resolution port + worktree GC.** Preservation bookmarks exist (done), but per 445 the design choice (catalog-vs-resolver) is routed to nota-designer/system-designer and not actioned; the `reaction-expand` `Cargo.toml` `[patch]` to non-existent `../../schema-next/reaction-expand` still needs repointing before it builds elsewhere. (445 §recommended actions, 707-8 #3)
- [ ] **Gated destructive GC pass** — merged/archive worktree set still on disk; empty parent dirs `~/wt/github.com/LiGoldragon/nota-next` and `.../upgrade` still present. Gate (live `worktrees.nota` + re-verify) unmet because of the migration item above. (707-9)
- [ ] **Designer lane: release the stale `mentci-lib` lock + remove the dead worktree.** `designer.lock` still advertises `.../mentci-lib/re-found-on-live-contracts`; the worktree dir still exists on disk though the branch is merged and deleted on origin. (447 closing note — designer's to do, not operator's)

Orchestrate builds clean. I have all the evidence needed across the four intent records. Let me compile the final audit.

## Intent fidelity

Audit of yesterday's (2026-06-19/20) work against the four governing Spirit records. Note: the codes in the prompt are paraphrases; the live records resolve to **7x5z** (mentci-lib shared model), **p43g** (criome owns keys + decides; references t00s for the quorum mode), **pviw** (the EscalateToPsyche dead-letter, prompt's "gc0n"), and **eh5a** (worktree registry + lifecycle). All evidence is on `main`.

### 7x5z — mentci-lib is the shared model reused by daemon and clients — REALIZED

Faithful. The record demands a five-shape MVU library reused by both the `mentci` daemon and thin clients.

- `mentci-lib/src/lib.rs` exports the full MVU surface: `ObservationModel`, `UserEvent`/`EngineEvent`, `Cmd`, `CriomeDecision`/`CriomeVerdict`, and the NOTA-fallback `render` module. Typed records only, no GUI-library types in the crate (intent's "holds typed records, never GUI-library types").
- Genuine dual reuse, the load-bearing claim: the **daemon** `mentci/Cargo.toml` depends on `mentci-lib` (`branch=main`) and consumes `CriomeVerdict` in `src/criome_bridge.rs`; the **client** `mentci-egui/Cargo.toml` depends on the same crate and `src/app.rs` holds a `mentci_lib::ObservationModel` and renders through mentci-lib's renderer as a thin shell.
- "Closed verdicts; edits are proposals" is modeled (`meta-signal-criome` `AuthorizationApprovalDecision [Approve Reject Defer]`; mentci-lib `decision` module).

INTENT.md: `mentci-lib/INTENT.md` was updated yesterday (commit `b94320b`) and accurately records the re-founding on live `signal-mentci` contracts, including the honest retraction of the earlier "nexus-daemon dual pair" framing. Exemplary.

### p43g (+ t00s) — criome owns keys + decides; mentci lists+decides parked approvals by slot — REALIZED (one loose seam)

The core contradiction p43g settles — **criome is the decider, not a mere signature-verifier** — is correctly realized. `criome/src/actors/root.rs::evaluate_authorization` branches on a daemon-wide `AuthorizationMode`: `AutoApprove` decides immediately, `ClientApproval` parks, and the default (Quorum, per t00s) evaluates the admitted contract against evidence via `ContractStore::evaluate`. The requester submits a content-addressed object and criome decides; there is no requester request-signing key in the path.

The parked client-approval flow exactly matches "mentci lists+decides parked approvals by `AuthorizationRequestSlot`":
- criome owns the queue: `park_authorization` stores a `parked` state keyed by `request_slot`; `read_parked_authorization_snapshot` filters to `AuthorizationStatus::Parked`.
- mentci lists via `ObserveParkedAuthorizations` and decides via `SubmitAuthorizationApproval(request_slot, decision)`; `record_authorization_approval` → `apply_authorization_approval` looks up the criome-held evaluation by slot and applies approve/reject/defer (vote-on-existing-object, not re-supply-by-value). `RejectAuthorization` is correctly blocked in ClientApproval mode (root.rs:241) so the verdict path is single-sourced.

The one seam (partial within an otherwise-realized record): p43g says criome "decides the verdict **and signs it**." On the decision path, criome publishes the outcome as an `AuthorizedObjectUpdate` pulse (`publish_authorized_object_update`) but does **not** route the verdict through `AttestationSigner` to mint a signed verdict object. Signing lives in separate explicit CLI verbs (`Sign`/`AttestAuthorization` in `signer.rs`), not bound to the authorization decision. The "decides" half is solid; the "signs the verdict it decided" coupling is not wired.

INTENT.md: `criome/INTENT.md` (commit `56547cc`) describes client-approval mode, `ParkedAuthorizationId`, the meta-socket list/observe/approve loop, and quotes t00s. Faithful and current.

### pviw — EscalateToPsyche approval surface (inert dead-letter) — REALIZED

pviw states EscalateToPsyche is "an inert dead-letter until the psyche UI exists." That is precisely what the code does, and faithfully:
- It is a closed typed variant of `EvaluationDecision [Authorized (Rejected ...) EscalateToPsyche]` in `signal-criome` (lib.schema:206), not an open string or hidden side effect.
- A contract can produce it: `criome/src/language.rs:318` returns `EvaluationDecision::EscalateToPsyche`.
- It is inert: `record_evaluation_decision` (root.rs:386) only publishes an authorized-object update when `decision == Authorized`; an `EscalateToPsyche` decision is returned as a typed `AuthorizationEvaluated` reply and otherwise acted on by nothing — exactly a dead-letter awaiting the psyche UI.

`criome/INTENT.md` describes it correctly ("a typed outcome, not a hidden side effect"). Realized.

### eh5a — register worktrees in orchestrate; lifecycle merge/archive(manifest for GC)/recycle — PARTIAL

The registry skeleton landed and builds clean (`orchestrate` v0.4.1 compiles), but the lifecycle eh5a calls for is only half-built.

Realized:
- Registry table + scanner + projection + handlers landed yesterday (`orchestrate` `0cd0904`/`ba8866d`). `WorktreeRegistry` (`src/worktree.rs`) serves `RegisterWorktree` and `RefreshWorktreeIndex` meta orders plus the `Observe(Worktrees)` read; infrastructure-minted facts (`last_activity`, `PushedState`) are re-derived from `jj`, never agent-supplied — a good fidelity touch.
- The lifecycle vocabulary exists in the wire: `signal-orchestrate` schema `WorktreeStatus [Active Merged Archived Recycled]` — the three eh5a outcomes are named and round-trip through the daemon (`execution.rs:1188`).
- A manifest is rendered: `WorktreeProjection` writes `orchestrate/worktrees.nota`, the GC-manifest sibling of the `.lock` projection.

Gaps against the captured intent:
1. **No lifecycle transition order.** Every code path sets `WorktreeStatus::Active` (`worktree.rs:144`); there is no `Archive`/`Recycle`/`Merge` order. `MetaOperationKind` adds only `RegisterWorktree`/`RefreshWorktreeIndex`. The Merged/Archived/Recycled states are reachable in the type system but unreachable in operation — an agent cannot drive the lifecycle eh5a specifies.
2. **The "manifest that drives later garbage collection" doesn't drive GC.** `worktrees.nota` is a passive projection; nothing reads it to garbage-collect a branch or dismantle a tree. The GC half of eh5a's archive contract is unrealized.
3. **INTENT.md not updated — the clearest documentation gap of the session.** `orchestrate/INTENT.md` last changed at `ecd81e3` (before yesterday) and says nothing about the worktree registry, the merge/archive/recycle lifecycle, or the GC manifest. AGENTS.md requires per-repo INTENT.md to be refreshed on the same branch as landing intent; the eh5a work shipped to main without it. (By contrast mentci-lib, mentci, and criome all updated their INTENT.md the same day.)

Verdict: registration + observe + manifest-rendering realized; lifecycle transitions and GC are stubs; INTENT.md is stale.

Relevant files: `/git/github.com/LiGoldragon/orchestrate/src/worktree.rs`, `/git/github.com/LiGoldragon/orchestrate/src/worktree_projection.rs`, `/git/github.com/LiGoldragon/orchestrate/INTENT.md`, `/git/github.com/LiGoldragon/signal-orchestrate/schema/lib.schema`, `/git/github.com/LiGoldragon/criome/src/actors/root.rs`, `/git/github.com/LiGoldragon/criome/src/actors/authorization.rs`, `/git/github.com/LiGoldragon/criome/src/actors/signer.rs`, `/git/github.com/LiGoldragon/criome/src/language.rs`, `/git/github.com/LiGoldragon/criome/INTENT.md`, `/git/github.com/LiGoldragon/mentci-lib/src/lib.rs`, `/git/github.com/LiGoldragon/mentci-lib/INTENT.md`, `/git/github.com/LiGoldragon/mentci/src/criome_bridge.rs`, `/git/github.com/LiGoldragon/mentci-egui/src/app.rs`.
