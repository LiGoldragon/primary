# 347 — schema-rust-next Plane emitter follow-ups + Spirit production-readiness

Agglomerates operator reports 322-326 (2026-06-05 to 2026-06-06): the sequence of `schema-rust-next` Plane-emitter slices that gated signal-frame support to the signal plane, carried `Plane` through engine-trait and trace object-name emission, added the streaming/subscription runtime substrate, and reproved Spirit (Nix-built, real-socket) after each slice. Each slice was a response to a designer audit (538/539) and each carried the same forward production-blocker list. This report is the landing witness for the five sources; the per-commit detail lives in git history.

## What landed (commit ledger, all on main, all cargo+clippy verified)

| Repo | Commit | What |
|---|---|---|
| schema-rust-next | `7f59b395` | `Plane { Signal, Nexus, Sema }` owns plane-intrinsic names; `RuntimePlaneSet::active_planes()`; plane namespace/origin-route emission moved to token nouns (`PlaneNamespaceAlias`, `PlaneNamespaceTokens`, `PlaneOriginRouteConstructorTokens`, `PlaneWrapperPath`). Signal-frame support gated by `writer.emits_signal()`: only `SignalRuntime`/`ComponentRuntime` keep `InputRoute`+frame encode/decode+`SignalFrameError`; `WireContract`/`NexusRuntime`/`SemaRuntime` do not. |
| schema-rust-next | `3ebeeda2` | carry `Plane` through engine traits: `Plane::{engine_trait_name, trace_enum_name, trace_activation_method_name}`; Signal/Nexus/SEMA engine-trait token nouns consult those instead of hardcoding. Added `RustWriter::emits_short_headers()` — NexusRuntime/SemaRuntime stop emitting orphaned `short_header` modules. ARCHITECTURE.md records the three-tier rule: `Plane` owns intrinsic names; `RuntimePlaneSet`/`RustEmissionTarget` own which planes emit; emitter nouns that inspect declarations/roots own schema-presence checks. |
| schema-rust-next | `9ca87549` | carry `Plane` through trace object names: `TraceObjectNameEnumTokens` + `TraceSupportTokens` derive enum names and match arms from each plane (was hardcoded `SignalObjectName`/`NexusObjectName`/`SemaObjectName`). ARCHITECTURE.md: wire contracts emit schema nouns, derives, NOTA/rkyv codecs, short-header route constants — not runtime envelopes, engine traits, mail/trace support, or signal-frame helpers. |
| triad-runtime | `de332266` | subscription runtime support: `SubscriptionToken`/`SubscriptionTokenIssuer`, `SubscriptionRegistry<Token, Filter>`, `SubscriptionEventSequence` (mints `StreamEventIdentifier`), `SubscriptionEventPublisher<Input,Output,Event>` (builds real `signal_frame::StreamingFrame`). Also: shared role traits (`NexusWork`, `NexusAction`, `SemaWriteInput`, `SemaReadInput`, effect roles) and a multi-listener daemon shell (many listeners → one runtime owner, not threads racing one engine). |
| schema-next | `30a88bee` | stream metadata + direct-lowering alignment for the streaming substrate. |
| signal-frame | `6f5a77f` | local INTENT + meta boundary wording; short-header exports the runtime now needs. |
| spirit | `41d96e70` → `186d97b1` → `46daf37b` → `bc28feb8` | regenerated against each emitter slice. Effects proven: `nexus.rs`/`sema.rs` lost ~159/~139 lines of misplaced signal-frame support (gating); lost dead `pub mod short_header`; intent subscription streaming pilot (`SubscribeIntent(Query)` opens `IntentEventStream`, hub in `src/subscription.rs`, tokens via `SubscriptionTokenIssuer`); meta socket slot reserved in `Configuration` (`meta_socket_path: Option`). Generated roots live under `spirit::schema::{signal,nexus,sema}`; crate root does not flatten them (witness present). Cleared a zero-byte `src/main.rs` residue so it can't be swept into a whole-working-copy commit. |

## Design contention carried forward

Reusable role names belong in shared `triad-runtime` traits/runner roles; component-specific variants stay generated in the component's schema modules. `NexusWork`/`NexusAction`/`SemaWriteInput`/`SemaReadInput` are traits/fixed runner roles in triad-runtime; Spirit's variants implementing them remain under `spirit::schema::{nexus,sema}` — keeping both no-boilerplate and the internal-feature catalog visible in `schema/nexus.schema` (z6qu).

## Spirit verification baseline reached

The new Spirit proof no longer stops at `cargo test`. Green across: normal + all-features Rust tests, process-boundary CLI/daemon (incl. subscription + trace), clippy `--all-targets --all-features -D`, and the ignored Nix-built binary integration suite (9 tests via `scripts/run-nix-integration-tests`, with local-builder fallback when the Prometheus cache/SSH builder times out — infrastructure noise, not product failure). `Observe` returns `RecordsStashed`, then `LookupStash` returns `RecordsObserved` (the slim-output flow); the Nix tests were corrected to prove that real behavior.

## Remaining production blockers (the forward list these slices kept reissuing)

1. **Full meta-signal Spirit listener/contract path** — meta is still only an optional daemon configuration socket slot; no full `meta-signal-spirit` contract/listener yet.
2. **Subscription-specific Nix-built streaming witness** — process-boundary subscription tests pass locally and in the Nix release matrix, but the ignored Nix integration suite has no subscription-specific streaming test. The shared schema/emission/runtime substrate is in place; the remaining slice is a component pilot that declares a real stream and wires long-lived socket delivery through the daemon.
3. **Two-listener ordinary/meta daemon runner** — the single engine-owner loop for the ordinary+meta shape still needs implementing and testing as shared triad-runtime code; Spirit currently proves only the single-listener path.
4. **Runtime emitter migration still incomplete** — large `format!`/`self.line` clusters remained in generated runner glue, engine traits, mail/envelope/namespaces, and signal-frame routing/short-header support (this is the Gap-1 tail later closed by the 327/329 token-emitter work).
5. **Deployed `persona-spirit` cutover / migration proof** — a real deployment cutover still needs live database/interface compatibility decisions and an operator-managed release path (continued in reports 341-345).

## Next operator moves named at the time

1. Continue tokenizing schema-rust-next runtime emission (runner glue, then engine traits). 2. Implement the two-listener daemon runner as shared triad-runtime code. 3. Build the first real streaming component path end to end. 4. Use Spirit's green Nix proof as the exemplar test shape before porting other components.
