# Terminal + Terminal-cell + Harness

> Three real component triads in good health: terminal, terminal-cell, and harness are all genuine kameo daemons (3 / 1 / 6 actors) with real ComponentDaemon impls, the contracts are clean of fake-NOTA, and nota-next pins are safe (no consumer on the d8862b6 encoding bump). The two real liabilities are a uniform foundation lag (schema-rust-next 8 behind, schema-next 5 behind) that leaves every live triad schema on the OLD verbose pre-52ro grammar (74 verbose self-tags across the live split schemas, plus Vec-Integer byte payloads instead of the yp29 Bytes leaf), and a small free-function debt in terminal (8 synthetic-exchange/default helpers that should be associated fns).

## Cluster: Terminal + Terminal-cell + Harness

Three real component triads in good health. `terminal`, `terminal-cell`, and `harness` are all genuine kameo daemons with real `ComponentDaemon` impls (3 / 1 / 6 actors respectively); the six contract/daemon crates are clean of fake-NOTA and free-function debt is confined to `terminal` (8) and one library-src fn in `terminal-cell`. The two real liabilities are a uniform foundation lag (schema-rust-next 8 behind, schema-next 5 behind) that strands every live triad schema on the OLD pre-52ro verbose grammar, and a contract-layer methodology split (one generated, three hand-written). No consumer is on the dangerous nota-next `d8862b6` encoding bump.

### Per-repo summary

| Repo | Role | Prod / Test / Gen LOC | Daemon shape | IntentFit | Foundation pins (behind HEAD) | Free-fn / Fake-NOTA |
|---|---|---|---|---|---|---|
| terminal | Persona terminal session owner | 5435 / 1640 / 3632 | real-kameo-daemon, 3 actors | aligned | schema-next −5, schema-rust-next −8, nota-next ae5c25cd −4, triad-runtime −1, signal-frame current | 8 / 0 |
| terminal-cell | Low-level PTY/transcript cell | 4780 / 1610 / 262 | real-kameo-daemon, 1 actor | aligned | same as terminal | 1 / 0 |
| signal-terminal | Working terminal wire contract | 631 / 946 / 3032 | contract-only (generated) | aligned | schema-rust-next −9, signal-frame −1 (lags cluster) | 0 / 0 |
| meta-signal-terminal | Meta terminal session lifecycle | 263 / 217 / 0 | contract-only (hand-written) | aligned | nota-next −4, signal-frame current | 0 / 0 |
| harness | AI-harness runtime objects | 2667 / 2521 / 262 | real-kameo-daemon, 6 actors | aligned | same as terminal | 0 / 0 |
| signal-harness | Working router↔harness contract | 672 / 706 / 0 | contract-only (hand-written) | aligned | nota-next −4, signal-frame current | 0 / 0 |
| meta-signal-harness | Meta harness daemon-config contract | 118 / 0 / 0 | contract-only (hand-written) | aligned | nota-next 16493c8 −3 (ahead of cluster), signal-frame current | 0 / 0 |

LOC method: production = `src` minus generated `src/schema/*.rs`; there are zero inline `#[cfg(test)]` modules anywhere in this cluster (all tests live in `tests/`), so no inline-test subtraction was needed. The pre-computed baselines were close; refined prod numbers above strip the generated schema modules out as a separate `Gen` column.

### Daemon reality (read from entrypoints, not READMEs)

- **terminal** — real. `src/daemon.rs` implements `ComponentDaemon for TerminalProcessDaemon` with `handle_working_connection` + `handle_meta_connection`, routing into the `TerminalSupervisor` actor. Three `impl Actor`: `TerminalSupervisor` (`supervisor.rs:642`), `TerminalSignalControl` (`signal_control.rs:520`), `SupervisionPhase` (`supervision.rs:144`). Bins are thin (`terminal-supervisor.rs` is 5 lines delegating to `run_to_exit_code`).
- **terminal-cell** — real. `ComponentDaemon for TerminalCellProcessDaemon`; one `impl Actor` (`TerminalCell`, `session.rs:1333`) plus heavy non-actor worker threads (fanout/scriber/reader) that are intentionally off the mailbox per INTENT.
- **harness** — real and the richest. `ComponentDaemon for HarnessProcessDaemon`; six `impl Actor`: `Harness`, `HarnessInstance`, `SupervisionPhase`, `TranscriptSubscriptionManager`, `TranscriptStreamingReplyHandler`, `TranscriptDeltaPublisher`. `HarnessProcessDaemon` is a legitimate ZST type-level selector, not a namespace-as-free-fn dodge.
- **signal-terminal / meta-signal-terminal / signal-harness / meta-signal-harness** — contract-only library crates (no `main`, no actors).

### Schema state: live vs stale, and grammar age

Every triad-bearing repo carries a stale `*.concept.schema` — the OLD single-file verbose concept form — alongside the LIVE split triad schemas. The concept files are **not** in any `build.rs` rerun list and generate nothing; they are dead cruft in all five that carry them (`terminal`, `terminal-cell`, `harness`, `signal-harness`, `meta-signal-terminal`). The live schemas (`signal/nexus/sema/daemon.schema`, and `signal-terminal`'s `lib.schema`) are freshness-gated by `build.rs … write_or_check`, so the checked-in `src/schema/*.rs` must track them.

Because schema-rust-next is pinned 8–9 commits behind `eca4028`, those live schemas are all on the **pre-52ro** grammar: 74 verbose `(X X)` self-tags across the live split schemas (nexus 27, sema 11, `signal-terminal/lib` 33, `harness/nexus` 3) that 52ro would collapse to `(X)`, plus **pre-yp29** byte payloads — `terminal/signal.schema` has `TerminalBytes (Vec TerminalByte)` and `signal-terminal/lib.schema` declares `{ value (Vec Integer) }` newtypes instead of the reserved `Bytes` leaf. Migrating is a three-step: bump the foundation, rewrite the schema files to terse/Bytes forms, regenerate. `harness`'s `nexus.schema` is additionally near-vestigial (its entire content is `HarnessToken Integer`) because harness drives its runtime from hand-written actors, not the generated nexus/sema runtime — its triad-port schema is decorative scaffold worth an explicit adopt-or-opt-out decision.

### Dependency posture

Pins are a **uniform lag, not drift**. Every consumer sits at schema-next `77e71a4` (−5), schema-rust-next `7282446` (−8, except `signal-terminal` at `0a845c3` / −9), nota-next `ae5c25cd` (−4, except `meta-signal-harness` at `16493c8` / −3), triad-runtime `ae2e817` (−1), signal-frame `166bda8` (current, except `signal-terminal` at `8b128d3` / −1). The nota-next/schema-rust-next pins are deliberately co-located at the `ae5c25cd` isolation point. **The d8862b6 encoding-bump flag does not fire for this cluster** — no consumer pins it; `meta-signal-harness` is the closest at one step ahead (`16493c8`, the bracket-string pipe-fence render) but still pre-bump. `flake.lock` in every repo pins only nixpkgs/crane/fenix (the Rust toolchain), so there is no Cargo.lock-vs-flake.lock disagreement on foundation crates. Action: `signal-terminal` should be re-locked up to the cluster baseline, and `meta-signal-harness` re-locked back to `ae5c25cd`, before any coordinated bump.

### Contract-layer methodology split

`signal-terminal` is schema-**generated** (`schema/lib.schema` → 3032-LOC `src/schema/lib.rs` via `ContractCrateBuild`, with 631 hand-written prod lines of accessor/introspection impls on top). Its three siblings — `signal-harness`, `meta-signal-terminal`, `meta-signal-harness` — are **hand-written** `signal_channel!` crates with no `build.rs` and no generated code. Same triad role, two authoring methods. `signal-terminal` also declares socket/owner helper types locally while the hand-written contracts import `SocketMode`/`WirePath` from `signal-persona`. Worth a deliberate standard.

### Free-function violations

Confirmed by reading each candidate (all are production, none under `#[cfg(test)]`, none `fn main`):

- `terminal/src/supervisor.rs:30` `synthetic_exchange` — fabricates a degenerate `ExchangeIdentifier`; should be `ExchangeIdentifier::synthetic()`.
- `terminal/src/supervisor.rs:38` `synthetic_stream_event` — fabricates a `StreamEventIdentifier`; belongs on the identifier type.
- `terminal/src/signal_cli.rs:27` `synthetic_exchange` — duplicate of the supervisor helper in a second module.
- `terminal/src/supervision.rs:324` `io_error` — error-constructor free fn; should be a `From`/associated fn.
- `terminal/src/pty.rs:1150` `default_control_socket`, `:1154` `default_data_socket`, `:1158` `default_command`, `:1162` `control_socket_and_text_from_environment` — four default/env free helpers that should hang off the owning socket/command/config types.
- `terminal-cell/src/socket.rs:13` `synthetic_exchange` — sole library-src free fn; the in-code comment already flags it as a placeholder for a future handshake cutover.
- `terminal-cell/src/bin/terminal-cell-session-select.rs:171/176` `process_is_alive` — cfg-gated free fn doing real OS work (`/proc` / `kill -0`) inside a CLI bin (not `main`); violates the rule even in a binary. Secondary to the library count.

`harness`, `signal-terminal`, `meta-signal-terminal`, `signal-harness`, `meta-signal-harness`: **zero** free-function violations (harness has only `fn main`).

### Fake-NOTA

**Zero across the whole cluster.** Every `to_nota` / `from_nota_block` in `src/schema/*.rs` delegates to `<Self as NotaEncode>::to_nota` / `NotaDecode` — generated, correct. The only hand-written codec, `meta-signal-harness`'s `ConfigurationGeneration` (`src/lib.rs:39`), delegates to `self.0.to_string()` for a `u64` scalar leaf — legitimate, not paren-building. No hand-assembled paren records, no `push_str("(")` accumulation, no hand-rolled NOTA parsing anywhere in `src`.
