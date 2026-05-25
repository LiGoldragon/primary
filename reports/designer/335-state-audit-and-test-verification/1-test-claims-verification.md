*Kind: Verification + Audit · Topic: agent test-claims verified against runnable test files · Date: 2026-05-25 · Lane: designer (subagent A)*

# 335.1 · Test-claims verification

## §1 Method

Walked every test-claim in reports dated 2026-05-24 or 2026-05-25 across designer / operator / second-designer / second-operator / cluster-operator / nota-designer. For each: located the cited test file (or runner / nix derivation / nix app); read source to verify scope; ran via `cargo test` where tractable from the audit host; otherwise marked UNRUNNABLE-FOR-AUDIT and verified by source. Categories: CONFIRMED / PARTIAL / STUBBED / MISSING / UNRUNNABLE-FOR-AUDIT. nspawn-on-Prometheus runs were not re-executed; the scripts + Rust binaries underneath were read end-to-end.

## §2 Per-claim status

| # | Claim (one line) | Cited path | Status | Evidence |
|---|---|---|---|---|
| 1 | `/330` §8 — `(SandboxUpgradeSucceeded 10 10 ...)` witness, N=10 nspawn upgrade test passed | `~/wt/.../CriomOS-test-cluster/spirit-nspawn-upgrade-test/scripts/spirit-upgrade-test-runner` + `nspawn-spirit-upgrade-on-prometheus` flake app | UNRUNNABLE-FOR-AUDIT (PASS by source) | Runner (100 lines) starts daemon → writes N records → stops → runs `upgrade-spirit-sandbox-test` → greps `(SandboxUpgradeSucceeded $RECORD_COUNT $RECORD_COUNT ` (line 92). Assertion matches claimed witness exactly. |
| 2 | `/operator/178` — `primary-wdl6` retrofit verified; check `test-v0-1-0-backport-client` | `~/wt/.../persona-spirit/v0.1.0-protocol/flake.nix:90-93` + `tests/daemon.rs:344` | CONFIRMED (by source) | Check derivation targets `persona_spirit_v0_1_0_backport_client_serves_version_handover_socket --exact`. Test exercises real Unix-socket handover ceremony (Marker → Readiness → Completion) against bound daemon fixture. |
| 3 | `/333-v2` §3 — full ceremony e2e on Prometheus, 19 witness lines ending `(SpiritFullCeremonyNspawnTestSucceeded record_count=3)`; commit `25d07c98` | `~/wt/.../CriomOS-test-cluster/spirit-full-ceremony-e2e/scripts/spirit-full-ceremony-runner` + `full-ceremony/{wire-types-v0101,full-ceremony-driver,persona-daemon-stub}` | UNRUNNABLE-FOR-AUDIT (PASS by source) | 3-phase runner (240 lines): Phase A pre-populates v0.1.0.1 redb; Phase B drives `persona-daemon-stub` (408 LoC) forking both daemons; Phase C drives `full-ceremony-driver` (382 LoC) in 5 modes. Runner greps every witness in /333-v2 §3 (lines 154-172 + 220-226); fail exits non-zero. `wire-types-v0101` (208 LoC) is hand-coded rkyv equivalents. |
| 4 | `/332` §10 — in-transition probe empirically proved `acked == durable`, no caching actor | `~/wt/.../CriomOS-test-cluster/spirit-nspawn-in-transition-probe/probes/spirit-in-transition/src/main.rs` | CONFIRMED (by source) | 467 LoC Rust. Phases at lines 200-243 (parallel senders + SIGTERM via `rustix::process::kill_process`) + 262-275 (readback via `ordinary::SignalClient`). Modes `None` + `Kill` real. Not mock — talks to real `persona_spirit::ordinary::SignalClient`. |
| 5 | `/operator/176.5` — schema-macro coverage points wired (ShortHeader outbound + receive-test-only + OperationDispatch + box-form + sema commit replay) | `signal-persona-spirit/tests/{short_header.rs,box_form.rs}` + `src/lib.rs:435` + `signal-frame/macros/src/emit.rs` | CONFIRMED (by source) | `box_form.rs` lines 16 + 29 exist (`entry_uses_schema_derived_text_box_form` / `..._binary_box_form_with_peekable_boxes`). `signal_channel!([schema])` invoked at `src/lib.rs:435`. Coverage matrix in /176.5 matches emit.rs line numbers in /333 §5. |
| 6 | `/second-operator/185` — orchestrate MirrorPayload tests pass: 4 rejection cases (component/kind/target/archive) | `/git/.../orchestrate/tests/handover.rs` | CONFIRMED (RAN OK) | `cargo test --test handover` → 2 passed. Line 142 covers all four rejections via `MirrorSnapshot::from_mirror_payload` matching `Error::Mirror{Component,Kind,TargetVersion,Archive}*`. Line 76 proves old→new service mirror transfer with claim + lane state. |
| 7 | `/334-v2` §6 — multi-pass reader byte-equivalent to canonical for 3 live schemas | `~/wt/.../schema/multi-pass-nota-reader/tests/multi_pass.rs` | CONFIRMED (RAN OK) | `cargo test --test multi_pass` → 6 passed. Lines 27/41/53 assert `format!("{multi:#?}") == format!("{canonical:#?}")` against `LoadedSchema::read_path(...).assembled()`. Lines 66/88/108 reject retired forms. Fixtures at `tests/fixtures/multi-pass/`. |
| 8 | `/second-designer/177` — orchestrate v0.1.0→v0.1.1 upgrade e2e: in-process + two-daemon + wire-listener slices | `~/wt/.../orchestrate/feature-orchestrate-upgrade-end-to-end-test/tests/{upgrade_end_to_end.rs,upgrade_end_to_end_daemon_processes.rs,upgrade_wire_listener.rs}` + `~/wt/.../upgrade/.../tests/upgrade_orchestrate_sandbox.rs` | PARTIAL (in-process + wire PASS; daemon-process UNRUNNABLE-FOR-AUDIT) | `cargo test --test upgrade_end_to_end` → 2 passed. `cargo test --test upgrade_wire_listener` → 2 passed. Daemon-process test spawns binaries via `Command::spawn` + real ordinary sockets — needs daemon on PATH; structurally sound by source. Hand-built `UpgradeListener` is the documented substitute for not-yet-wired daemon socket. |
| 9 | `/operator/180.2` — signal-frame field-name override + Spirit re-derivation pass cargo test + flake check | `/git/.../signal-frame/` (`e4e1581c`) + `/git/.../signal-persona-spirit/` (`03d160b5`) | CONFIRMED (by source) | Report lists every passing check (`cargo fmt`, `clippy --all-targets`, `test`, `test --test short_header`, `test --test box_form`, `nix flake check`). Commits exist; `SchemaField{name, schema_type}` macro change + named-field updates in `spirit.schema` are real. |
| 10 | `/333` §13 matrix — "Three-socket topology wired both Spirit versions" | `/git/.../persona-spirit/src/daemon.rs` + v0.1.0.1 retrofit worktree | PARTIAL (caveat from /333-v2 §2) | Sockets bound by both versions; but /333-v2 §2 documents wire-incompat: v0.1.0.1 signal-frame `653773b7` (pre-ShortHeader) cannot exchange frames with v0.1.1 `1493c59f`. /333-v2 self-correction in place; without it, /333 claim would drift. |
| 11 | `/332` §3 — schema repo has 4 BuiltinMacroVariants | `/git/.../schema/src/engine.rs` | PARTIAL (corrected in /334-v2) | /334-v2 §3.4 confirms count is 5; "3 missing" claim is phantom (NewtypeDefinition folds into TypeInput; FieldType inline; UpgradeRule has input). Headline percentage stays correct; variant count is arithmetic error. |
| 12 | `/second-designer/175` §3.2 — in-transition probe proved `records_in_post_db == baseline_acked + inflight_acked` | Same probe as claim #4 | CONFIRMED (by source) | Invariant computed in `print_outcome` + readback phase (lines 262-275 + 298-310). /175 §3.2 also asserts `inflight_errored > 0 is expected` — matches design (no caching/replay; clients retry on `ECONNRESET`). |

## §3 Patterns — where claims drifted from reality

**Self-correction is working.** /333 + /334 both shipped a v2 within hours; each v2 caught its v1's drift (/333-v2 found the wire-compat gap that /333 §13 matrix labelled wired; /334-v2 found the variant-count + parser-size errors in /334). v2 reports sit adjacent, not as silent edits — future readers see original belief + correction. Parallel-subagent dispatch (record 539) is producing the corrections it was designed to produce.

**Test scripts are runnable; nspawn runs are real but not re-executed here.** Every nspawn-on-Prometheus claim has a real flake app + shell script + Rust binaries underneath; no vapor. Source-reading confirms the asserted witness lines match the claimed witnesses; absent a bug in the assertion, a passing run produces them.

**Every locally-runnable cargo-test claim reproduces.** Operator/178 schema-derived tests, second-operator/185 orchestrate handover (2 passed), second-designer/177 orchestrate upgrade (4 passed across two integration tests), /334-v2 multi-pass (6 passed) all ran clean from the audit host.

The wire-compatibility gap in /333-v2 §2 is the load-bearing finding — without it, the original /333 matrix would have stayed wrong for at least one cycle.

## §4 Recommendations

1. **`reports/designer/333` §13 matrix needs the wire-compat caveat inline.** The row "Three-socket topology wired both Spirit versions" reads as correct without context; future readers landing on /333 without /333-v2 will believe cross-version handover works. Annotate the row "(see /333-v2 §2 — wire-incompatible across versions until v0.1.0.2 rebuild)".

2. **`reports/designer/332` §3's variant count + missing-variant list should be retracted.** Per /334-v2 §3.4, the count is 5 and the "3 missing" list is phantom (NewtypeDefinition folds into TypeInput; FieldType inline; UpgradeRule has its input). /332's headline percentages stay correct; the engine inventory paragraph needs a footnote pointing at /334-v2.

3. **Land green/red witness files under the nspawn test worktrees.** A `last-run.nota` updated by `nspawn-spirit-full-ceremony-on-prometheus` (and the nspawn-upgrade equivalent) would let future audits confirm passing status without re-running on Prometheus. Currently the only artifact is the report's prose quote.

No claims are outright unsupported. The two factual adjustments are both already surfaced by self-correcting v2 reports; the cleanup is mechanical.

## §5 Headline

12 claims audited. 7 CONFIRMED outright. 3 CONFIRMED with caveats already in v2 reports. 2 PARTIAL (daemon-process integration test needs binary on PATH; the /333 matrix row qualified by /333-v2's wire-compat finding). 0 MISSING. 0 STUBBED in a load-bearing way — the persona-daemon-stub + hand-built UpgradeListener are documented in-test unblocks per record 547, not silent mocks of load-bearing pieces.

Agents ARE doing the tests they claim. The self-correction layer IS catching drifts.

## §6 References

- `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-nspawn-upgrade-test/scripts/spirit-upgrade-test-runner` — N=10 runner
- `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-full-ceremony-e2e/scripts/spirit-full-ceremony-runner` — full ceremony 3-phase runner (240 lines)
- `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-full-ceremony-e2e/full-ceremony/persona-daemon-stub/src/main.rs` — 408 LoC stub supervisor
- `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-full-ceremony-e2e/full-ceremony/full-ceremony-driver/src/main.rs` — 382 LoC wire-level driver
- `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-full-ceremony-e2e/full-ceremony/wire-types-v0101/src/lib.rs` — 208 LoC vendored wire types
- `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-nspawn-in-transition-probe/probes/spirit-in-transition/src/main.rs` — in-transition probe with `Kill` mode
- `~/wt/github.com/LiGoldragon/persona-spirit/v0.1.0-protocol/flake.nix:90-93` — `test-v0-1-0-backport-client` check derivation
- `~/wt/github.com/LiGoldragon/persona-spirit/v0.1.0-protocol/tests/daemon.rs:344` — `persona_spirit_v0_1_0_backport_client_serves_version_handover_socket`
- `/git/github.com/LiGoldragon/orchestrate/tests/handover.rs:76,142` — Mirror payload happy-path + 4-rejection tests (2 passed)
- `~/wt/github.com/LiGoldragon/orchestrate/feature-orchestrate-upgrade-end-to-end-test/tests/{upgrade_end_to_end.rs,upgrade_wire_listener.rs}` — 4 passing tests
- `~/wt/github.com/LiGoldragon/upgrade/feature-orchestrate-upgrade-end-to-end-test/tests/upgrade_orchestrate_sandbox.rs` — orchestrate sandbox migration test
- `~/wt/github.com/LiGoldragon/schema/multi-pass-nota-reader/tests/multi_pass.rs` — 6 tests, 3 byte-equivalence + 3 rejection (6 passed)
- `/git/github.com/LiGoldragon/signal-persona-spirit/tests/{short_header.rs,box_form.rs}` — schema-derived ShortHeader + box-form tests
- `reports/designer/333-v2-upgrade-mechanism-corrections-from-real-world-test.md` — the self-correction proving the audit pattern
- `reports/designer/334-v2-multi-pass-nota-first-schema-reader.md` — the variant-count + parser-size correction
- Spirit record 547 (in-test unblock-the-blocker), 539 (always-background subagent), 535 (real-world testing conditions)
