---
title: 544 — Situation report (intent refresh + base-component stack sweep)
role: designer
variant: Survey
date: 2026-06-06
topics: [situation-report, intent-refresh, triad-main, component-triad, schema-rust-next, triad-runtime, spirit, cloud, domain-criome, auditor, archive, migration, orchestration]
description: |
  Designer-lane situation report from a six-agent sweep (live Spirit intent +
  base-component stack state + operator activity + designer frontier +
  workspace/orchestration). Headline: the triad_main! daemon-emit chain LANDED
  across triad-runtime/schema-rust-next/spirit and was extended by the operator
  (ConnectionContext). Live frontier: migrating the remaining components
  (message next) onto the schema-derived triad runtime. Surfaces open psyche
  decisions (archive semantics, Configure scope, schema field-ordering,
  Watch/SubscribeIntent unification, auditor firming, terminal-control unblock)
  and stale-doc reconciliation (component-triad.md, triad-runtime/INTENT.md,
  AGENTS.md auditor section).
---

# 544 — Situation report

## Executive summary

The base-component stack frontier is the **schema-derived triad runtime**, and its keystone just landed: the `triad_main!` daemon-emit chain (the uniform daemon skeleton emitted from schema) is **merged into `main` across all three repos** — triad-runtime, schema-rust-next, and spirit — verified green, and the operator has already extended it with a `ConnectionContext` (per-connection peer credentials) follow-on. Spirit is the proven pilot: its daemon bin is now a literal one-liner over emitted source. The most live thread is the **component migration onto this runtime** (mind/message/orchestrate/router/terminal-control/persona still hand-written; `message` is the chosen next pilot). The single most important open decision is the **archive-semantics call from report 541** (redirect vs migrate-forward), tied for urgency with the **schema field-ordering** choice that is currently blocking nothing but is silently being decided by default in design files.

A recurring honesty note runs through this report: several primary-surface and per-repo `INTENT.md`/skill docs (component-triad.md, triad-runtime/INTENT.md, AGENTS.md auditor section) are now **stale against landed reality** and need designer-lane reconciliation.

## Live intent state

Source: deployed `spirit` CLI (`~/.nix-profile/bin/spirit`, Spirit 0.5.2), live and responding. Window: `Since 2026-05-23` (1411 records) plus `Deep`/`VeryDeep` recency. Certainty mix in window: 1173 High, 125 Medium, 60 Maximum, 26 VeryHigh, plus a handful Low/Minimum/VeryLow. Dominant topic mass: schema (420), spirit (157), nota (138), workspace (81), signal (76), cloud (60). No blocker — Spirit was queried directly; no legacy `intent/*.nota` fallback was used.

### Recent dominant threads (record id + one-line gloss)

- **`vez8` (schema is a NOTA dialect, not a separate language; Maximum, 06-05)** — the schema / asschema / schema-next / schema-rust-next stack is the single biggest thread by mass; schema is a specialized NOTA dialect on structural macro nodes, and every schema must emit Rust (records `jypw`, `jr65`, `glr2`).
- **`lnhj` (triad_main is an EMITTED source-visible daemon module; High, 06-06)** — schema-rust-next emits `src/schema/daemon.rs` (the uniform daemon skeleton); streaming is Option B (emitter generates publish/subscribe wiring from declared schema streams); a component hand-writes only its `impl ComponentDaemon`. Full design in designer report 542.
- **`ocu7` (core components migrate onto the triad runtime; High, 06-06)** — mind, message, orchestrate, router, terminal-control, spirit, persona all port to the schema-derived triad runtime (triad_main + Signal/Nexus/SEMA engine traits); spirit is the landed pilot.
- **`tvbn` + `jxi9` (Horizon/lojix rewrite charter + buildable-and-evaluable milestone; VeryHigh/High, 06-04/06-06)** — the new lojix/horizon stack is a greenfield rewrite; the intermediate milestone is "can build node closures and be evaluated" (in-memory state OK); production-durable Stack-A parity is the later cutover bar. `o5rz`: new-stack repos push straight to main, no next/feature ceremony.
- **`2alg` + `k6w1` (lojix concurrent worker model; High, 06-06)** — the lojix daemon serves connections concurrently and never blocks on a nix build; the bounded thread-per-connection worker primitive belongs in the reusable `triad-runtime`, not per-component.
- **`ckhx` + `bcca` + `5fd6` (terminal-layer decomposition; High, 06-06)** — a new `terminal-control` component (working `signal-terminal-control`, policy `meta-signal-terminal-control`) owns the session surface; terminal-cell stays the abduco PTY primitive, forked via systemd to survive restart, with sema as the durable instance registry. `1g8y`: terminal-control migration targets the EXISTING terminal repo (no new repo) — this directly answers the operator's "blocked, repo doesn't exist" flag below.
- **`3nqt` / `8bea` / `tdsu` (agent retry resilience; VeryHigh/High, 06-06)** — newest workspace-discipline thread: agents (and their own tool calls, plus subagent/workflow dispatch) must retry transient/server-side errors (API 529, socket close, timeouts) with backoff until success; giving up on a transient error is a defect.
- **Spirit identity + privacy thread (`wm4r` / `y5m9` / `qtbd` / `xfc5`; Maximum/VeryHigh, 06-04)** — production Spirit moved to 96-bit CSPRNG random opaque identifiers rendered as lowercase base36 shortest-unique-prefix codes; numeric record lookup is retired.
- **`hnpo` (MetaSignal is the canonical policy-contract name; VeryHigh, 06-05)** — OwnerSignal deprecated; every component policy contract is `meta-signal-<component>`; `oszy` clarifies meta-signal carries owner CONFIGURATION ops (e.g. archive target), not a reclassification of working ops.
- **Primary version-control discipline (`p4sm` / `qqyg` / `lj8k`; Maximum/VeryHigh, 06-04)** — primary is always main, no branches; code repos use main + next.

### Notable recent decisions / corrections

- **`om3x` (Correction, Maximum, 06-04)** — agents must NOT default psyche statements to Maximum certainty; ordinary direct statements are not founding rules.
- **`own9` (Correction, High, 06-06)** — the ENTIRE at-binder surface (all `@`-binding) is ABANDONED; nota-next must remove all `@`-binding parser support; supersedes `n2z3` wholesale. The authored surface is the positional bracket/brace form.
- **`ug6i` (Principle, High, 06-06)** — generated Rust must ALWAYS be regenerated from schema (single source of truth, no ceremony); stale checked-in artifacts (meta-signal-cloud, meta-signal-lojix) were a failure that masked a real emitter bug; the per-crate write_or_check freshness gate must run fleet-wide.
- **`g3ax` (Decision, High, 06-06)** — the emitted daemon spine must thread per-connection peer credentials (SO_PEERCRED) into the `handle_working_input` hook; the prior spine regressed origin minting to a constant Owner tag. (This is the intent behind the `ConnectionContext` follow-on that has since landed.)
- **`lc2r` (Correction, VeryHigh, 06-04)** — the schema-derived triad is NOT one daemon schema file; the contract/daemon split holds per plane.
- **`vr32` / `tlaf` / `rvh4` / `kw1k` / `sg4o` (Maximum, 05-24/05-25)** — the NOTA-positional + bracket-string-only + shell-double-quote-wrap discipline cluster (all now Maximum).
- **`nqsb` (Principle, VeryHigh, 06-04)** — every repo must have an INTENT.md, the FIRST file to create.
- **`pkjl` (Correction, Maximum, 06-04)** — explain status to the psyche in plain English, not internal jargon.

### Open / uncertain intent awaiting the psyche

- **Auditor role — NOW FIRMED, no longer Medium.** AGENTS.md still describes it as a Medium-certainty proposal, but `ek8w` (Decision, High, 06-04) settles it: intent agglomeration / refresh is triggered by an automated auditor that auto-proposes refreshes; the psyche confirms the retire of source records (automated discovery, human-gated removal). The AGENTS.md §"Possible additional role — auditor" text is now stale against Spirit and should be updated to the High-certainty automated-auditor decision.
- **Schema field-ordering inside the root struct (`4y1h`, Decision, Medium)** — explicitly carried open: imports-first (let-style) vs input/output-first (function-signature style); the psyche named both, the decision is not locked, and design files currently use option A pending the pick.
- **Enum-vs-macro discriminator (`b0s4`, Clarification, Medium)** — the paren is doubly loaded (enum vs head-applied collection macro); three candidate discriminators (reserved operator-word set / sigil / move collections to suffix sigils); open which one, and whether bare-paren stays the enum default.
- **Schema component as separate triad vs absorbed into upgrade (`def2`, Principle, Medium)** — a dedicated schema-registry triad keyed by short header is named and concrete, but the daemon-shape decision (separate vs absorbed) is open.
- **Spirit privacy access tiers (`8ll8`, Decision, Low; `6gwz`, Medium)** — four tiers Open/Personal/Sensitive/Sealed proposed but at Low certainty; refined access categories still exploratory.
- **Spirit search richness (`699n`, Low; `73r4` / `g8ln`, Medium)** — weighted keyword/recency scoring possibly via Nexus, combined recency+topic filtering, and a separate `Weight` Magnitude axis are named but tentative.
- **Plane origin-route placement (`b559`, Clarification, Medium)** — tuple-leading-element vs named struct field for the origin route inside the data-carrying Plane enum, proposed by a subagent, pending psyche confirmation.
- **Browser automation path (`0zah` / `7o4q` / `ae2s`, Medium)** — Playwright CLI vs browser-use delegated-LLM path; design-level, not settled.

## Base-component stack

### Verdict — triad_main! daemon-emit chain: LANDED (all three repos), and extended past the named branch tips

The three `designer-daemon-emit-2026-06-06` branches were integrated into `main` (re-landed under new commit ids via the operator main/next flow, not as the literal pushed branch-tip ids). All three concrete checks pass, and a follow-on `ConnectionContext` feature landed on top.

- **triad-runtime — LANDED.** Commit `1bd383b` ("land daemon-emit — DaemonConfiguration + ExitReport for triad_main") explicitly states it integrates `designer-daemon-emit-2026-06-06 (4454952f)`. Evidence: the `DaemonConfiguration` trait + `ExitReport` live in `src/process.rs` (added by `1bd383b`; +87 lines src/process.rs, +123 tests/process.rs); `ExitReport::from_result` confirmed at `src/process.rs:142` (`pub fn from_result<Error>(&self, result: Result<(), Error>) -> ExitCode`). Caveat worth noting: the trait is in `src/process.rs`, not `src/daemon.rs` as the original task hint guessed. Extended further by `33b9531` (ConnectionContext).
- **schema-rust-next — LANDED.** The named branch tip `304d52e7` is not present under that id, but the substance landed via `33337d7` ("land triad_main daemon emitter — token-based + audit fixes") with `b75c7f5` and `6685e7b` follow-ons. Evidence: `src/daemon_emit.rs` present on origin/main (doc-comment: "the `triad_main!` emitter from designer report 542 … emits a per-component, source-visible `src/schema/daemon.rs`"); `ModuleEmission::daemon_module` confirmed at `src/build.rs:129`; tests `tests/daemon_emission.rs` + fixture `tests/fixtures/daemon-stream.schema` present.
- **spirit — LANDED.** Named tip `ad122e3e` IS on origin/main verbatim, plus `d406d19` / `bd04eac` on top. Evidence: emitted `src/schema/daemon.rs` present (carries `DaemonCommand<Daemon: ComponentDaemon>`); the hand-written `SpiritDaemonRuntime` / `DaemonCommand` / `SubscriptionHub` structs are GONE from hand-written source (grep finds them only in the emitted module); `src/daemon.rs` is now just `impl ComponentDaemon for SpiritDaemon`; the bin `src/bin/spirit-daemon.rs` is a true one-liner: `fn main() -> ExitCode { SpiritDaemon::run_to_exit_code() }`.

Implementation note vs. the original spec: `triad_main!` landed as a **source-visible emitted `src/schema/daemon.rs` module per component** (schema-rust-next's `daemon_emit.rs`), not as a literal invoked macro — consistent with the stack's source-visible-generation boundary.

**Stale-doc flag for follow-up:** `triad-runtime/INTENT.md` lines 80-91 still assert "triad_main! … is NOT YET BUILT — no triad_main! macro exists in triad-runtime, in schema-rust-next, or in any component crate" and describe spirit's daemon main as hand-written calling `DaemonCommand::from_environment().run()`. Both statements are now contradicted by landed main across all three repos and should be reconciled on the next triad-runtime branch.

### The rest of the base-component frontier

- **schema-next** (origin/main `77e71a4`) — schema macro engine + typed semantic schema data model; does NOT emit Rust. Recent: GAP-2 derive adoption, `Assembled`→`MacroExpansion` rename, full Asschema retirement (`6a12bcc` removed the compatibility surface; `5311f9a` / `a2123f8` source-field-naming through artifacts), stream lifecycle metadata + direct stream lowering (`c2b3546` / `30a88be`). Named frontier: built-in schema macros loading through a serialized macro-library artifact (hand-authored source kept as a freshness-checked bootstrap); structural macro-node codec machinery lives at the nota-next layer while schema-next owns positions/handlers.
- **schema-rust-next** (origin/main `6685e7b`) — emits Rust interface source from typed schema; owns the shared build-driver. Recent: the token-based string→token emission migration is **complete** (`4ac90de` GAP-1; god-struct `RustWriter` gone), the triad_main daemon emitter (`33337d7` token-based, `b75c7f5` E0284 fix, `6685e7b` emits `ConnectionContext` into the `handle_working_input` hook), Plane namespace family threaded through trace/engine traits. Named frontier: keeping NOTA-text projection opt-in per emission target (binary-only daemon closure carries no `nota_next`); cross-crate import aliasing; the emitter stays the home for `triad_main!`/daemon emission per the triad-runtime ownership boundary.
- **triad-runtime** (origin/main `33b9531`) — shared runtime mechanics for schema-derived Signal/Nexus/SEMA daemons. Recent: `DaemonConfiguration` trait + `ExitReport::from_result` (`1bd383b`), `ConnectionContext` per-connection peer credentials (`33b9531`), `BoundedWorkers` bounded-concurrency primitive (`fdfd183`, the reusable worker primitive intent `2alg`/`k6w1` named), bound-daemon socket cleanup, clean multi-listener stop. Named frontier: backpressure / deeper runtime-control machinery is deferred; INTENT.md needs the reconciliation noted above.
- **signal-frame** (origin/main `6f5a77f`) — shared Rust-to-Rust wire kernel (frames, exchange/stream ids, envelopes, streaming bodies, subscription-token inner values, length-prefixed rkyv helpers). Recent: intent + meta boundary wording (`6f5a77f`), constrained schema boxed NOTA codecs, compact schema-marker spelling routed through the schema reader. Named frontier: stays the low-level streaming wire kernel only (token issuance/registries/event publication belong to triad-runtime); the ordinary/meta split as a contract/rebuild boundary.
- **nota-next** (origin/main `f0e435a`) — the new NOTA implementation (delimiter predicates, root queries, structural macro nodes). Recent: `#[shape(keyword="...")]` structural-macro-node derive shape (`f0e435a`), removal of the abandoned `@` at-binder syntax (`d996a30`, executing correction `own9`), direct-decode structural macro nodes + `#[derive(StructuralMacroNode)]` enums (`fb600e3` / `f066805` / `a9a34f6`), `BlockShape` vocabulary. Named frontier: the typed structural-macro-node enum (declaration-order variant matching, recursive caption decode, encode-back to structural NOTA) is the derive surface; consumers like schema-next own the vocabulary attached to typed nodes.
- **sema-engine** (origin/main `e1aeef1`) — the exclusive database-operation boundary; a reusable redb-hiding engine over the `sema` kernel. Recent: identified mutation (`e1aeef1`) + identified record families (`817236a`) — assert/mutate/retract/match without retract-plus-assert shims; ARCHITECTURE notes on destructive retract / page reclaim, v0.1 concept schema. Named frontier: stays library-only (no daemon/socket/actor/NOTA parser); `IdentifiedTableDescriptor` for engine-assigned numeric identity; replay/subscription surfaces for handover.
- **spirit** (origin/main `bd04eac`) — proof that a running Spirit-like three-plane component is buildable from schema-derived interfaces; the landed triad_main pilot (evidence above). Named frontier: the meta slot in `Configuration` exists ahead of the meta listener; State/ChangeCertainty production-parity ops; the binary-rkyv daemon vs `nota-text` CLI boundary held by `cargo tree` assertions.

## Operator activity & pending handoffs

### What operator (Codex) recently FINISHED

The headline: the **triad_main! ordered cross-repo landing from designer handoff 543 is COMPLETE and verified green** — and operator has already built on top of it. The handoff (`/home/li/primary/reports/designer/543-triad-main-implementation-handoff.md`) asked for a dependency-ordered land of the three `designer-daemon-emit-2026-06-06` branches; operator executed it in `/home/li/primary/reports/operator/328-triad-main-audit-and-migration/`, captured on primary main as commit `cf1e5def` ("operator 328: triad_main audit + landed across triad-runtime/schema-rust-next/spirit; migration plan").

Operator did more than land — it **audited the branches first and caught a real flaw the handoff did not flag**: `daemon_emit.rs` (807 lines) was written in the OLD string-emission style (409 string-emit constructs, `quote!`=0) because the designer branch was built off pre-Gap-1 main. Since operator had landed the Gap-1 RustWriter→token rewrite earlier the same session, the daemon emitter directly re-violated psyche intent `4np2` (VeryHigh: emission must be `quote!`/proc-macro2/ToTokens, not a hand-rolled string generator). Operator **rewrote `daemon_emit.rs` to tokens as part of landing** (`self.line` 404→0, `quote!` 0→30, `ToTokens` 0→11) and caught a real E0284 regression (`SubscriptionWriters<Daemon>` unconstrained type param) that schema-rust-next's own goldens missed but spirit's actual compile surfaced — fixed via a disambiguated call.

Verified landed state (confirmed against live repo history, not just the report):
- **triad-runtime** main — `DaemonConfiguration` trait + `ExitReport::from_result` (44 tests, clippy -D); branch `4454952f` is now an ancestor of main.
- **schema-rust-next** main — token daemon emitter + audit fixes + E0284 disambiguation (61 tests incl. 6 daemon goldens, clippy -D); branch `304d52e7` is now an ancestor of main.
- **spirit** main — pilot regenerated against the token emitter; `--all-features` 77 pass / 9 nix-ignored; **process_boundary 8/8 over a real Unix socket**; freshness guard clean; branch `ad122e3e` is now an ancestor of main.

Also finished earlier in the same arc (report 327, six-agent study): the audit of the schema/NOTA/triad stack plus the four-gap fixes — Gap 1 (RustWriter god-struct eliminated), Gap 2 (StructuralMacroNode derive adopted in schema-next, the string-keyed `match macro_name()` ladder deleted), Gap 4 (the `@` at-binder removed from nota-next entirely per superseding Spirit `own9`). Gap 3 (triad_main!) was docs-only at 327 time, then actually built+landed via the 543 handoff in 328.

### What operator is MID-STREAM on

**Component migration onto the new schema-derived triad runtime** — the second half of the psyche's directive ("then start migrating all components: mind, message, orchestrate, router, terminal-control, spirit, persona"). Spirit is the done pilot; the rest are NOT yet migrated. Operator published a readiness survey and order in `/home/li/primary/reports/operator/328-triad-main-audit-and-migration/5-landing-complete-and-migration-plan.md`:
1. **message** — most ready (has the triad-runtime dep + daemon bin + `signal-message`); the cleanest single-tier pattern-setter, and the intended next step.
2. **persona, mind** — single-tier (persona has a daemon bin).
3. **router, orchestrate** — two-tier (working + owner-only meta listener); these exercise the meta-signal path.

Each migration is a real design+implement step (designing three plane schemas — `signal.schema` / `nexus.schema` / `sema.schema` — from each component's concept + wire contract, then wiring `NexusDaemonShape` + `impl ComponentDaemon`, verified green per repo), not a mechanical edit. As of the most recent commits, operator has NOT yet started message; instead it landed a follow-on triad-runtime feature first — `ConnectionContext` (per-connection peer credentials threaded through the daemon `handle_working_input` hook) across all three repos (triad-runtime `33b9531`, schema-rust-next `6685e7b` emitting it, spirit `bd04eac` threading it). This is operator continuing to extend the daemon emitter on top of the completed triad_main landing — and it directly discharges intent `g3ax`.

### Handoffs AWAITING operator (and reverse-direction flags)

1. **The 543 triad_main handoff is DISCHARGED** — no longer pending; it is the completed work above. (For the designer lane: the handoff was fully consumed, the daemon emitter was rewritten to tokens during landing, and the branches are merged into main.)
2. **Two items operator FLAGGED back for the psyche / designer (operator→designer/psyche, reverse direction):**
   - **terminal-control migration is BLOCKED** in operator's view — the triad repo does not exist (only `terminal` / `terminal-cell` plus a forming `signal-terminal-control`). **This is now answered by intent `1g8y`** (terminal-control migration targets the EXISTING terminal repo, no new repo) — so the block is resolvable: tell operator to use `terminal`.
   - **Gap 3 `component-triad.md` reconciliation** (a primary-surface item operator declined to edit unilaterally): the skill should now say triad_main! is an *emitted module* (not a literal macro) and re-anchor off dead records `1419` / `1486` to live `1488`. Designer 543 §"Follow-on" names this same primary-surface doc update as a designer-owned follow-on — so this is a designer-lane TODO, not operator's.
3. **Remaining schema-next / schema-rust-next doc-drift flags** raised in 327 for the code repos (want a work branch): schema-next docs still calling Asschema a "compatibility endpoint" (should read "retired"); the `Assembled*` family rename in schema-next to avoid confusion with the removed Asschema IR; `migration.rs` named as an untokenized residual surface. These are open code-repo cleanups in operator's lane.

Most recent operator reports (newest first): `/home/li/primary/reports/operator/328-triad-main-audit-and-migration/` (5 files, the landing+migration session), `/home/li/primary/reports/operator/327-schema-nota-triad-study/` (6 files, the audit), then single-file reports 326 (plane trace completion + doc fix), 325 (plane engine-trait followup), 324 (plane gated emitter + spirit production proof).

## Designer frontier

### Reports 534-543 — disposition

| # | Topic | State |
|---|---|---|
| 534 | Horizon RAW/PRETTY split (psyche record `9p8v`) | DECIDED + handed off. Split settled (RAW = typed cluster-data model; PRETTY = pre-derived Nix-consumed helpers); supersedes `m85j` "push to Nix"; remaining horizon forks handed to the in-project agent. |
| 535/536 | Base-component frontier + engine/spirit ground truth & plan | Ground-truth surveys; fed the work that landed in 541-543. |
| 537-540 | Plane type design + 3 audits (operator-plane integration, engine-trait follow-up, trace completion) | LANDED — spirit main shows `41d96e7` / `46daf37` / `bc28beb` (split planes on Plane-gated emitter, Plane-trait migration, Plane trace completion). |
| 541 | meta-signal-spirit owner-config contract + daemon meta-listener (`Configure ArchiveTarget`, MultiListenerDaemon, 0o600 meta socket) | IMPLEMENTED + LANDED on canonical `spirit` main as `0446697`. Two psyche design calls still OPEN (below). |
| 542 | triad_main! DESIGN (emitted module, not a literal macro; 6 forks) | DECIDED — psyche said "go with B." Re-anchors to live `1488`; flags `1419` / `1486` as dead. |
| 543 | triad_main! IMPLEMENTATION + ordered cross-repo landing handoff | IMPLEMENTED, verified green, and now LANDED past handoff (see Base-component stack). |

**Repo-identity caution:** the live spirit work is in `/git/github.com/LiGoldragon/spirit` (canonical main), NOT `/git/github.com/LiGoldragon/persona-spirit` — the latter is a stale older checkout (detached `5227741`, hand-written `DaemonRuntime`, no `src/schema/daemon.rs`) and should not be read as current. The 543 worktrees are under `~/wt/github.com/LiGoldragon/spirit-daemon-emit` / `spirit-meta-signal` / `spirit-archive-port`.

### Frontier item (a) — triad_main! follow-on (542 §forks 5/6)

triad_main! itself has LANDED on three of the four mains, AHEAD of where report 543's handoff left it (commits in Base-component stack). The named follow-on is NOT done: **cloud + domain-criome have NOT been generalized onto the emitter.**
- **cloud** STILL hand-writes `src/schema_daemon.rs` (199 lines) — the explicit generalization target. It is already a `MultiListenerDaemon` over two authority-tiered sockets driving the generated Nexus runner over `SchemaStore` (so it is the right shape for the multi-listener emitter pilot), but the skeleton is hand-written, not emitted. It also still carries a parallel legacy `src/daemon.rs` (201 lines, `signal_frame::ExchangeFrame` + hand-written `Store`) kept as the Cloudflare-IO runtime until that IO ports to the effect plane.
- **domain-criome** STILL hand-writes `src/daemon.rs` (272 lines) and has NOT even reached the multi-listener generated path — it is the older `Arc<Mutex<Store>>` + `signal_frame::ExchangeFrameBody` shape with hand-written `SocketBinding` / `ListenerRuntime`. It is the second (later) pilot and is further behind cloud.

### Frontier item (b) — archive / meta-signal open items

- **Watch/Unwatch-vs-SubscribeIntent boundary:** NOT reviewed as a designer report, but the boundary is now LIVE and distinct on spirit main. `Input` carries `Tap` / `Untap` (operator-stream observer), `Watch` / `Unwatch` (subscription, schema lines 7-8/25-26), AND a separate `SubscribeIntent(query)` variant (`nexus.rs:541`). Three distinct subscription-shaped surfaces coexist; whether Watch/Unwatch and SubscribeIntent should be unified or kept separate is unresolved — no designer report adjudicates it.
- **collect_removal_candidates partial-failure edge:** PARTIALLY addressed by `791bc23` ("fix Configure archive bug + port CollectRemovalCandidates"). The live `store.rs` is now per-record `match`: archive failure → per-record `ArchiveFailed` skip (no longer all-or-nothing into an empty reply); already-removed → `RecordAlreadyRemoved` skip. The all-records-swallowed-into-empty-reply edge the item named is FIXED. **Residual edge (unflagged in any report):** the mid-loop `self.remove(identifier)?` still propagates via `?`, so a remove error mid-loop aborts the whole method after some records are already archived AND removed — a partial commit with no divergence record, violating the component-triad "commit-first-success, record divergence" rule.
- **Observer push-stream deferral:** CONFIRMED still deferred on spirit main. `Tap` / `Untap` are ported as request/reply effects only — `ObserverTapTable.observe_operation` records every admitted op (`nexus.rs:500`, "the recording half"), and a later `Tap` reads what was recorded; `EffectsOnly` returns false / "observes none" (`nexus.rs:113-118`). No push stream to observers exists; the real-time observer push remains unbuilt. (The subscription push that DID land is the Watch/RecordSubscription streaming proven in 543's `process_boundary` test — distinct from the observer/Tap surface.)

### Frontier item (c) — skills/component-triad.md update

NOT done — the cleanest open documentation gap. `component-triad.md` lines 1078-1145 still assert:
- line 1093: "the **`triad_main!` macro itself is NOT yet built**" — now false; landed on all three mains.
- line 1099: cites `spirit/src/bin/spirit-daemon.rs` as a "hand-written near-one-line `DaemonCommand::from_environment().run()`" — now false; spirit's bin is the emitted one-liner.
- lines 1100/1122/1138: repeatedly anchor on the DEAD `1419` / `1486` ("named-but-unbuilt", "intended emission but is not yet built"). The live anchor `1488` is present (line 1140) but framed as future ("When `triad_main!` lands…"). The skill needs: (1) reframe to "triad_main! is an EMITTED `src/schema/daemon.rs` module, not a literal `macro_rules!`"; (2) flip the status note from named-but-unbuilt to landed-pilot; (3) re-anchor the live citation off `1419` / `1486` (dead) to `1488` (live) per reports 542/543.

### Two psyche design calls still OPEN (from 541, awaiting answer)

1. **Archive semantics = REDIRECT vs MIGRATE-FORWARD.** `set_archive_target` currently re-points future writes/reads only; existing records in the prior file are left in place (neither copied nor deleted). The psyche must confirm redirect is the intended meaning of "where to put archives," or request migrate-forward.
2. **Configure scope = archive-target-only vs broader.** `Configure` is built extensible but only carries `ArchiveTarget` today (`RetentionPolicy` etc. left as future non-breaking Optional additions). The psyche must confirm archive-only initial scope or name the other config wanted in.

Plus one schema-rust-next emitter follow-up flagged in 541: the meta `WireContract` needs a hand-written `src/meta_transport.rs` frame codec because `WireContract` emits per-root `short_header` but not `encode/decode_signal_frame` (gated to `emits_signal()` targets). The clean fix is for schema-rust-next to emit the frame codec for socket-transported wire contracts; `meta_transport.rs` is a correct bridge until then. (This also retroactively justifies keeping `short_header` in `WireContract` — audit 539 finding #4.)

### Production blockers still standing (per 541 handoff)

The Nix-built subscription-streaming witness and the `persona-spirit` → schema-derived Spirit cutover proof remain the two named standing production blockers.

## Workspace & orchestration

### Workspace intent essence (ESSENCE.md + INTENT.md)

The workspace is an **intent-and-design-driven engine** — a back-and-forth of intending and designing, where implementation crosses the threshold only when both halves of the readiness signal are met (intent clear AND design good enough). Designer and operator are the two halves of that dance, not a pipeline. Intent is primordial: when intent is unclear, absent, or contradicted, agents ask the psyche rather than infer — inferring intent is the single most-forbidden act ("the death sentence"). Logging psyche intent through the deployed `spirit` CLI is the first action of any psyche-prompt turn.

What the psyche is building: **software eventually impossible to improve**, priority order Clarity > Correctness > Introspection > Beauty (earlier wins on conflict). Key recently-synthesized themes:

- **The readability thesis** (promoted to ESSENCE 2026-06-05; was carried at `triad-runtime/INTENT.md`): the schema-derived stack reads cleanly because each layer names exactly one thing — types name the work, schema names the interface, generated Rust names objects/traits, and handwritten code is mostly the real algorithm (match typed input, decide, call the next typed interface, return typed output). When a daemon needs large handwritten plumbing to understand its own contract, that mechanism belongs in schema emission or shared runtime. This makes Clarity #1 concrete.
- **Strings only at the edges; the system is typed** — typed end-to-end; strings live only at the user-authored payload edge and the user-facing display edge (daemon edge: daemons receive binary signal-frame, never decode NOTA; trace edge: typed trace frames, strings rendered only at the display surface).
- **The two-deploy-stack discipline** — production today runs the monolithic `lojix-cli` stack on `main` in the canonical checkouts (`horizon-rs`, `lojix-cli`, `CriomOS`, `CriomOS-home`, `CriomOS-lib`, `goldragon`); the lean rewrite (new `lojix` daemon + thin CLI + lean horizon + pan-horizon config) lives on `horizon-leaner-shape` branches in `~/wt/...`. Do NOT fold one into the other piecemeal; cutover is a coordinated multi-repo merge after parity. (cloud-designer commit 26 records a fresh lojix engine refresh — Nexus completeness + runtime-state + raw/pretty boundary.)
- **Naming** — spell every identifier as a full English word (`Request` not `Req`) AND names don't carry their full ancestry (`Entry` not `IntentEntry`); the two rules pull opposite directions and only work as a pair.
- **NOTA as the only argument language / universal embedding-safe payload** — every component binary takes exactly one NOTA argument, no flags ever; NOTA strings come exclusively from bracket forms (never `"`), so a complete NOTA expression embeds escape-free inside any double-quote host (JSON, Rust, Nix, YAML, shell). NOTA is a typed text user interface; symbols are paths through the schema namespace (canonical SymbolPath, not per-design).
- **The component triad** — daemon + working signal + meta policy signal (`<component>`, `signal-<component>`, `meta-signal-<component>`); the CLI is the daemon's first client, not a triad leg. Runtime decomposes into three execution centers (Signal / Nexus / SEMA) over three planes; Nexus is the mail keeper. Schema IS the architecture; wire is REST-shaped; schema-emitted Rust mirrors the schema namespace.

### Active / claimed lanes (orchestrate/*.lock)

Two lanes currently hold claims; all other lock files are empty (idle):
- **designer** — `[primary-9hx0]` (the spirit plane-schema split exemplar) plus path `/home/li/wt/github.com/LiGoldragon/spirit/spirit-plane-split`, reason "spirit plane-schema split exemplar (9hx0)" (claimed Jun 4 14:59).
- **system-designer** — `[P3-introspect-realign]` (realign persona onto the renamed signal-introspect crate) plus path `/home/li/wt/github.com/LiGoldragon/persona/realign-signal-introspect`, reason "realign persona onto renamed signal-introspect crate" (claimed Jun 5 14:50; consistent with recent commit `30b94242` tracking the meta-signal repo rename).

Idle (empty) lock files: assistant, cloud-designer, cloud-operator, cluster-operator, counselor, nota-designer, operator, pi-operator, poet, second-designer, second-operator, system-operator. **Stale legacy lock files** from the retired `<role>-assistant` / `-specialist` suffix era still sit on disk but are empty and out of contract: `designer-assistant`, `operator-assistant`, `poet-assistant`, `second-designer-assistant`, `second-operator-assistant`, `second-system-assistant`, plus an orphan `primary-ngn8.lock`. Lock files are gitignored runtime state, so these are local cruft, not tracked drift — cleanup candidates but harmless.

### Standing open WORKSPACE-level question — auditor role

A third role beyond designer/operator that closes the loop back to designer — doubts, finds flaws, catches broken workspace rules; mostly mechanical (rules-and-flaws detection), suiting a smaller pattern-checking model. **DeepSeek** is named and the direction is to **automate** it. NOTE the live-intent finding above: AGENTS.md still carries this as Medium-certainty-proposed, but Spirit record `ek8w` (Decision, High, 06-04) has firmed the automated-auditor-with-human-gated-removal shape. Still open even after `ek8w`: (1) authority class — structural or support-tier? (2) lane mechanism — windows on a shared agent identity or external CI-style pipeline? (3) substrate for audit findings flowing back to designer — `reports/auditor/` subdir, bead comments, Spirit records from an auditor identity, or PR-style review on jj commits. No `skills/auditor.md` and no `reports/auditor/` yet; bootstrap entry point is INTENT.md §"When a new role appears without a skill".

### Recent role / process evolution (landed, not open)

- **Role renames (spirit record `920`, Maximum):** the `<role>-assistant` / `<role>-specialist` suffixes are RETIRED workspace-wide. Capacity is added via `second-<role>` / `third-<role>`; specialized scope is qualified by prefix (`cluster-operator`, `nota-designer`, `cloud-designer`, `system-designer`). Six main roles: operator, designer, system-operator, poet, assistant, counselor.
- **Whole-working-copy commit discipline (records `2589` / `2620`):** `jj commit` takes NO path arguments — it drains the entire shared working copy. Path-scoped commits strand peers' changes and cause sibling-commit forks. The resulting multi-lane / impersonal commit is accepted; committing is janitorial, not owned by a report's creator. Supersedes the prior "don't commit other lanes' files" guidance.
- **Primary-always-main (record `2585`, VeryHigh):** on primary everyone works on `main` directly — `jj commit` then `jj bookmark set main -r @-` then `jj git push --bookmark main`. No feature/`next`/`wip`/`push-*` branches and no rebase-onto-main choreography; the only divergence handler is the named `git fetch` + `git rebase origin/main` + push escape hatch. (Code repos under `/git` keep designers on `next`/feature branches in `~/wt` while operators own main + rebase — records `515` / `2561`.) Companion: lock selectively, never the whole space (record `2586`).

## Open questions for the psyche

- **Archive semantics — REDIRECT vs MIGRATE-FORWARD (from report 541; the single most urgent decision).** The landed `set_archive_target` only re-points future writes/reads; records already in the prior file stay put (not copied, not deleted). Confirm "redirect future only" is what you meant by "where to put archives," or say migrate-forward so existing records are moved. This is blocking the meta-signal-spirit archive feature from being declared complete.

- **Configure scope — archive-target-only vs broader now (from report 541).** `Configure` is extensibly built but today carries only `ArchiveTarget`. Confirm archive-only as the initial scope, or name the other owner config you want folded in now (e.g. `RetentionPolicy`) so it lands in the same contract rather than as a later addition.

- **Schema field-ordering inside the root struct (intent `4y1h`, Decision, Medium — carried open).** Imports-first (let-style) vs input/output-first (function-signature style). You named both; the decision is not locked, and every schema design file is currently defaulting to option A while it waits. This is silently being decided by default — worth a definitive pick.

- **Watch/Unwatch vs SubscribeIntent — unify or keep separate (judgment call, currently undocumented).** Spirit main now carries three subscription-shaped surfaces side by side: `Watch`/`Unwatch` (record subscription), `SubscribeIntent(query)` (a distinct variant), and `Tap`/`Untap` (observer). No report adjudicates whether the first two should be one mechanism. A direction from you tells the designer lane whether to write the unification or document the deliberate split.

- **AGENTS.md auditor text is stale against Spirit — confirm the update, and the three sub-decisions.** Record `ek8w` (Decision, High, 06-04) already firmed the auditor as "automated discovery, human-gated removal," but AGENTS.md still calls it a Medium-certainty proposal. May the designer lane update AGENTS.md to the High-certainty shape? And which way on: authority class (structural vs support-tier), lane mechanism (shared-agent windows vs external CI pipeline), and findings substrate (`reports/auditor/` vs bead comments vs auditor-identity Spirit records vs PR-style review)?

- **terminal-control block is resolvable — confirm operator should use the existing `terminal` repo.** Operator flagged terminal-control migration as blocked because no triad repo exists. Intent `1g8y` says the migration targets the EXISTING terminal repo (no new repo). Confirm so operator can unblock, rather than waiting for a repo creation that intent says should not happen.

- **Residual partial-commit edge in collect_removal_candidates (judgment call — should the designer lane fix it now?).** The empty-reply edge is fixed, but a mid-loop `self.remove(identifier)?` still aborts the whole method via `?` after some records are already archived-and-removed — a partial commit with no divergence record, which violates the component-triad "commit-first-success, record divergence" rule. It is currently unflagged in any report. Want this fixed on the next spirit branch, or accepted as a known edge for now?
