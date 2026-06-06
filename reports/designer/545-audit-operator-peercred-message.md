---
title: 545 — Audit: operator peer-cred cascade + message migration
role: designer
variant: Audit
date: 2026-06-06
topics: [audit, operator, peer-credentials, connection-context, message, migration, triad-runtime, schema-rust-next, spirit, continuous-manifestation, intent]
description: |
  Adversarial designer audit (5 dimensions → per-finding skeptics → synthesis,
  13 agents) of the operator's peer-cred cascade (ConnectionContext via
  SO_PEERCRED) + the message component migration onto the emitted triad runtime.
  Verdict: SOUND + green, no blockers, fix-then-fine. All four commits
  independently re-verified on origin/main; suites re-run green. The worth-acting
  items are all doc/commit-message truthfulness on the trust-boundary feature
  (two self-contradicting INTENT.md files, a process.rs doc overclaim, a dead
  Option<i32> pid, a missing ARCHITECTURE.md trust-boundary entry). Continuing
  to router is endorsed with the precondition that the doc contradictions are
  fixed first so router inherits an accurate template.
---

# 545 — Audit: operator peer-cred cascade + message migration

## Verdict

The operator's work is sound and shippable. All four headline commits are genuinely on origin/main and green: triad-runtime `33b9531a` (ConnectionContext via SO_PEERCRED), schema-rust-next `6685e7b3` (emitter threads the context), spirit `bd04eac7` (threads-but-ignores), and message `8fa99105` (first real migration onto the emitted runtime). I independently re-ran the suites — process_boundary is 8/8 under `--all-features`, message's two owner-vs-non-owner origin tests pass, schema-rust-next is 61 green, triad-runtime is 6/6 plus clippy `-D warnings` clean across all four. No blocker. Net: **fix-then-fine** — the code is correct, but several stale doc/commit-message claims about peer-cred wiring are factually wrong and should be corrected before this is held up as the migration template.

### Editor's note (designer, post-audit)

Finding **#5** below (triad-runtime/INTENT.md still says `triad_main` "NOT YET BUILT") was **already fixed** in the same session, before this audit landed, on the pushed designer branch **`designer-intent-triad-main-2026-06-06`** (`45188bd3`) — it rewrites the stale block to the landed-emitted-module reality and records what triad-runtime still owns. That branch awaits operator integration into triad-runtime main; integrating it discharges #5. The branch does NOT yet cover the ARCHITECTURE.md trust-boundary gap (#3), the `process.rs` doc overclaim (#1), the `Option<i32>` pid (#2), or message/INTENT.md (#4).

## Claims independently verified

| Operator claim | Verdict | Evidence (re-run / inspection) |
|---|---|---|
| Four commits on origin/main | CONFIRMED | `git rev-parse HEAD == origin/main` after fetch for all four: triad-runtime `33b9531a`, schema-rust-next `6685e7b38a49…`, spirit `bd04eac7f015…`, message `8fa9910523db…`. Working trees clean. |
| forbid(unsafe_code) kept, no unsafe added | CONFIRMED | triad-runtime `src/lib.rs:8` `#![forbid(unsafe_code)]` + `Cargo.toml:21` `unsafe_code = "forbid"`; `grep -rn unsafe src/ tests/` finds only doc-comment mentions. SO_PEERCRED read via rustix's safe `socket_peercred` wrapper, not the unstable std path. |
| Emitter is token-based (no string-emission regression) | CONFIRMED | schema-rust-next `daemon_emit.rs`: 30 `quote!` uses, 11–14 `impl ToTokens`, routed through `syn::parse2::<syn::File>` + `prettyplease::unparse` at `render()` (180–188). No `write!`/`String` code-builder. (See refuted finding below: the specific `self.line=0` evidence the operator cited does not exist, but the conclusion holds.) |
| process_boundary 8/8 (spirit) | CONFIRMED (with qualifier) | `cargo test --all-features` → `8 passed; 0 failed`. Under `--features nota-text` alone it is 7/7 — the 8th test is `testing-trace`-gated. The operator's commit message correctly scoped the claim to `--all-features`, so 8/8 is accurate for the suite named. |
| message uid-based origin tests (owner vs non-owner) | CONFIRMED | `tests/forward_to_router.rs` both pass: uid 1000 → `MessageOrigin::External(ConnectionClass::Owner)`; uid 4242 → `NonOwnerUser(UnixUserIdentifier::new(4242))`. Drive the real `MessageEngine::handle` through a `StubRouter` UnixListener and assert the actual forwarded wire origin — not a stub. Hardcoded constant Owner is gone. |
| Emitter threads &ConnectionContext into handle_working_input | CONFIRMED | `daemon_emit.rs:412` emits the hook with `connection: &triad_runtime::ConnectionContext`; spine captures `ConnectionContext::from_stream(&stream)` at `:843` before the stream moves into `WorkingTransport::new` (`:844`) — correct borrow-before-move. message `src/schema/daemon.rs:154` calls it for real. |
| triad-runtime commit message: "emitted daemon spine threads &ConnectionContext into handle_working_input" | REFUTED (within triad-runtime) | The emitted spine lives in schema-rust-next, not triad-runtime; `33b9531a` defines+exports the type only. `handle_working_input` does not exist in triad-runtime, and `daemon.rs` `handle_stream` still takes a bare `UnixStream`. The cross-repo wiring is real (in `6685e7b3`); the triad-runtime commit message overclaims for that one repo. See first verified finding. |
| Each touched repo's INTENT.md reconciled on the same change | REFUTED | triad-runtime and message INTENT.md both ship stale/contradictory peer-cred prose (see Verified findings). |
| Migration is genuinely deep (readability thesis) | CONFIRMED | message deleted `src/supervision.rs` (380 hand-written kameo-actor lines) + ~845 test lines; daemon is now one `impl ComponentDaemon` (3 methods) + a one-liner bin. Stateless sema verified honest (no Store/DB opened). |

## Verified findings

All findings below returned `standsUp=true` from the independent skeptic. Ordered blocker → concern → nit. There are no blockers.

### Concerns

**1. triad-runtime commit message + process.rs doc overstate the work: ConnectionContext is defined+exported but never wired into the daemon spine *within triad-runtime*.** The commit message says "The emitted daemon spine threads &ConnectionContext into handle_working_input so components mint origin tags," and `src/process.rs:14-19` doc asserts "The emitted daemon spine reads these once per accepted working connection." Neither is true *in this crate*: `handle_working_input` does not exist in triad-runtime, ConnectionContext appears only in `process.rs` (def), `lib.rs` (re-export), and tests, and `daemon.rs:23,40-44` `handle_stream` still takes a bare `UnixStream`. The repo's own `ARCHITECTURE.md:78` and `INTENT.md:80-89` say the emitted spine does not live here. The wiring genuinely lands in schema-rust-next `6685e7b3` — so the cross-repo feature is real, but a future agent reading the triad-runtime doc-comment will believe origin-minting is live in this crate when it is not. Location: `/git/.../triad-runtime/src/process.rs:14-19`, `src/daemon.rs:23,40-44,371,413`; commit `33b9531a`. Recommendation: soften the commit message / `process.rs` doc to "type introduced ahead of wiring," or note the wiring is owned by schema-rust-next.

**2. triad-runtime `Option<i32>` pid is dead optionality and the doc mischaracterizes rustix.** `from_stream` (`process.rs:61`) always produces `Some(credentials.pid.as_raw_pid())` — it can never return `None`. rustix 1.1.4 `Pid` wraps a `NonZeroI32` (`src/pid.rs:19`, `as_raw_pid` = `self.0.get()`), so the pid is structurally non-zero and no accessor lifts to `None`. Yet the doc at `process.rs:26-30` claims "SO_PEERCRED can report a zero pid … the accessor lifts an absent identifier to None" — both halves are false. The only `None` comes from the test-only `new()` path. Location: `/git/.../triad-runtime/src/process.rs:26-30,61`; `rustix-1.1.4/src/pid.rs`. Recommendation: drop the `Option` (use plain `i32` or a typed `ProcessId(NonZeroI32)` newtype) and fix the doc, so callers don't write `None`-handling production never triggers.

**3. triad-runtime INTENT.md / ARCHITECTURE.md not updated for the new security-relevant surface (continuous-manifestation gap).** A public peer-credential trust boundary landed with zero doc manifestation: grep of both files for `ConnectionContext` / `SO_PEERCRED` / `peercred` returns nothing. Commit `33b9531a` touched only `Cargo.toml/lock`, `lib.rs`, `process.rs`, `tests/process.rs`. `ARCHITECTURE.md` has a `## Process Runtime` section documenting `process.rs`'s prior contents but not the type that landed in that very file. AGENTS.md mandates same-branch manifestation when intent affecting a repo lands; a kernel-vouched trust boundary qualifies. Location: `/git/.../triad-runtime/INTENT.md`, `ARCHITECTURE.md`; commit `33b9531a`. Recommendation: add the trust-boundary concept to ARCHITECTURE.md's process-edge section (and INTENT.md if durable) on the same change as the pending wiring/doc fix.

**4. message INTENT.md §Residuals contradicts its own landed peer-cred code (same-commit self-contradiction).** Commit `8fa99105` ADDED an INTENT.md residual saying peer-cred origin is "carried, not yet resolved" — that "the spine discards the connection stream, so SO_PEERCRED is not available" and "the daemon stamps `External(Owner)` from configured owner identity." Every clause is false in that same commit: `src/schema/daemon.rs:154` calls `ConnectionContext::from_stream`, threads it into `handle_working_input`; `src/router.rs:310` `origin_for_connection` mints `Owner` on uid-match else `NonOwnerUser(peer_user_id)`; two tests prove it; the commit message itself says "Peer-cred origin RESTORED." The "Wire translation to router" paragraph is also stale (still says provenance is minted "from configured owner identity"). A future agent reading INTENT.md would re-attempt done work or distrust the green code. Location: `/git/.../message/INTENT.md` (Residuals → Peer-credential-derived origin; Wire translation to router), vs `src/router.rs` + `src/schema/daemon.rs:154`. Recommendation: delete the peer-cred residual, fix the wire paragraph to say provenance is minted from the accepted connection's SO_PEERCRED peer uid; leave only the genuine CLI-wire residual.

**5. triad-runtime INTENT.md says `triad_main` "NOT YET BUILT" but the daemon emission landed.** `INTENT.md:80-91` reads "It is NOT YET BUILT — no `triad_main!` macro exists … Today the daemon `main` is hand-written: spirit's `spirit-daemon.rs` calls `DaemonCommand::from_environment().run()`." Both clauses are stale: the emission is schema-rust-next `daemon_emit.rs` (its own header calls it "the `triad_main!` emitter from designer report 542"); spirit and message both ship generated `src/schema/daemon.rs`; both bins are now `*Daemon::run_to_exit_code()` one-liners. Note the verifier's two honest caveats: (a) the auditor's chronology sub-claim ("obsolete the moment it was committed") is WRONG — the doc commit `08b624a` (12:54) predates the daemon-emit commit `1bd383b` (14:55) by two hours, so it was accurate when written and only went stale after; (b) there is no *literal* `triad_main!` macro (the design chose a source-visible emitted module instead), so that narrow phrasing is technically true. The central code-confirmed contradiction (the hand-written-main example is false) stands; severity stays concern. Location: `/git/.../triad-runtime/INTENT.md:80-91`. Recommendation: drop the NOT-YET-BUILT framing and the stale hand-written-main example; the "triad-runtime does not itself own the emitter" nuance can stay. **(Already fixed on branch `designer-intent-triad-main-2026-06-06` / `45188bd3`, pending operator integration — see Editor's note.)**

### Nits

**6. Operator's `self.line=0` evidence for token-based emission does not exist.** No `self.line` field or line counter exists anywhere in `daemon_emit.rs` (the only "line" is a doc comment). The conclusion (token-based) is correct; the cited signal is not real. Recommendation: cite `quote!`/`ToTokens` routing through `syn::parse2`+`prettyplease` instead. Location: `/git/.../schema-rust-next/src/daemon_emit.rs`.

**7. Report 5's `ToTokens 0->11` count is off — actual landed count is 14.** Harmless and conservative-direction, but the report's other falsifiable counts are exact, so the one mismatch is worth a correction if the report is revised. Location: `reports/operator/328-.../5-landing-complete-and-migration-plan.md:26`.

**8. uid/gid/pid exposed as raw `u32`/`i32` rather than typed domain newtypes.** For a trust-boundary type where confusing uid and gid is a security bug, the raw-int edge is a real (minor) loss of type safety. rustix hands back typed `Uid`/`Gid`/`Pid` that are immediately stripped. Recommendation: consider `UserId`/`GroupId`/`ProcessId` newtypes (or re-export rustix's types). Not blocking. Location: `/git/.../triad-runtime/src/process.rs:31-78`.

**9. Stateless message still carries a phantom `database_path` (upstream trait-shape smell).** `triad_runtime::DaemonConfiguration::database_path()` forces message to carry an unused path and pass a bogus `message.unused` in tests. message documents this honestly; the fix belongs upstream. Recommendation (designer): make `database_path` return `Option<&Path>` (default `None`) so stateless components need not carry a phantom path. Location: `/git/.../message/src/config.rs:30`; `DaemonConfiguration` in triad-runtime.

**10. Pre-existing free-function discipline violation in message `src/surface.rs:23`.** `pub fn expect_end(...)` is a free function outside `#[cfg(test)]`/`main`, violating the method-only override. Pre-existing (commit `3f5ecff`), NOT touched or worsened by the migration. Recommendation: move onto an owning noun on a future cleanup pass. Location: `/git/.../message/src/surface.rs:23`.

**11. Minor emitted-message-shape and substring-golden nits (schema-rust-next).** `DaemonError::Component` emits `#[error("component error: {0}")]` where audit m1 suggested the `daemon ` prefix the sibling arms carry (m1's actual requirement — self-describing — is satisfied). daemon_emission goldens are substring assertions (`assert_code_contains`) not full-file snapshots, so they would miss unrelated emission drift; adequate for this change. Recommendations are optional. Locations: `daemon_emit.rs:950`; `tests/daemon_emission.rs`.

### Praise (verified sound)

- **Peer-cred restoration is exemplary and refutes the constant-Owner-regression worry.** rustix's safe `socket_peercred` keeps `forbid(unsafe_code)`; the emitted spine threads the context; spirit legitimately ignores it (its OriginRoute is a monotonic per-request routing counter minted internally in `issue_origin_route`, never peer-derived — confirmed via history commit `962be96`, so there is no prior peer-cred origin to regress from); message restores real uid-based classification with owner sourced from configuration, never payload, and proves both branches.
- **message migration is genuinely deep**, not a headline: 380 lines of supervision + ~845 test lines deleted, replaced by an emitted spine; one-liner bin; honestly-stateless sema with a build-time guard script.
- **spirit's freshness guard was verified to actually run in check mode** (forced build.rs rerun with no UPDATE env), proving the checked-in `src/schema/daemon.rs` matches the emitter — not assumed.

## Findings that did NOT survive verification

To keep the record honest, one auditor finding was refuted by the skeptic (`standsUp=false`) and is dropped from the verified set:

- **"Session report 328 stops before the peer-cred + message-migration commits it should cover" — REFUTED, downgraded concern → nit.** All the report's mechanical sub-claims are true (file-5's SHAs are two-per-repo stale; main advanced). But the auditor missed `reports/operator/329-session-summary-schema-stack-and-triad-main-2026-06-06.md`, a separate session summary that documents ALL of it: the peer-cred cascade narrative, a commit-ledger table listing every advanced SHA (`33b9531a`, `6685e7b3`, `bd04eac7`, `8fa99105`), the g3ax/ocu7 intent records, and the CLI-wire residual. The "undocumented / deserves the session log" framing is a missing-thing-that-exists-elsewhere false positive. The only residue is a tidiness nit: the 328 directory's frame reads as final while the migration phase landed afterward in 329.

## Recommendation to the psyche / operator

The cascade is correct and green; nothing blocks shipping. The worth-acting-on items are all **doc/message truthfulness** on a trust-boundary feature — cheap to fix and high-value because future agents will lean on these docs as the migration template:

1. **Fix the two contradictory INTENT.md files** (message §Residuals + triad-runtime `triad_main`/ConnectionContext gaps). These are same-branch continuous-manifestation violations on the headline feature; an agent reading them today would either re-do finished peer-cred work or distrust green code. Highest-value fix. (triad-runtime/INTENT.md `triad_main` half is already done on branch `45188bd3`; the ConnectionContext addition + message/INTENT.md remain.)
2. **Soften the triad-runtime commit message + `process.rs` doc** so they don't claim in-crate wiring that lives in schema-rust-next, and **resolve the `Option<i32>` pid dead-optionality** (drop the Option or fix the doc).
3. **Add the triad-runtime ARCHITECTURE.md/INTENT.md trust-boundary entry** for ConnectionContext on the same change.

Everything else (typed-uid newtypes, `database_path` → `Option`, the pre-existing `expect_end` free function, report-count corrections, golden-snapshot upgrade) is optional polish, not a gate.

**On continuing straight to router:** yes, with one precondition. message is a sound reference pattern, and router/orchestrate carry owner tiers that will exercise the same peer-cred path on the meta listener — so they are the right next migrations. But the message **CLI↔daemon path is NOT yet end-to-end** (the CLI still speaks the old signal-message `MessageChannel` wire, bypassing the migrated daemon — confirmed real, documented in INTENT.md). Before router is held up as "done," decide whether that CLI-wire migration is finished for message first or explicitly deferred; proceeding to router with message's CLI residual open is fine as long as it is tracked, not forgotten. Recommend fixing the doc contradictions (item 1) before the next migration so router inherits an accurate template.
