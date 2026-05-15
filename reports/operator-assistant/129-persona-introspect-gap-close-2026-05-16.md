# 129 — persona-introspect gap close

Date: 2026-05-16
Role: operator-assistant
Scope: Close the implementable gaps named in `designer/190-persona-introspect-gap-scan.md` for current-slice paths in `/git/github.com/LiGoldragon/persona-introspect`.

---

## TL;DR

Two commits on `persona-introspect:main`:

- `ca74dc5` — drop the redundant `let _ = (...)` placeholder in `IntrospectionRoot::prototype_witness`.
- `934ee7d` — add two architectural-truth tests in `tests/store.rs`: one source-scan witness that the daemon does not depend on peer contract crates, and one actor-density witness that every `IntrospectionRequest` variant flows through the Kameo root and persists via the sema-engine commit log.

No router observation wiring landed. Router daemon still does not serve `RouterRequest::Summary`; `RouterClient` stays scaffolded. The `DeliveryTraceStatus::Unknown` retire-work is owned by the contract-side agent (signal-persona-router landed a parallel `drop Unknown from wire status enums` commit on its own contract; signal-persona-introspect has not seen the equivalent yet).

---

## What landed

### 1. Drop the placeholder in `prototype_witness`

Before:

```rust
fn prototype_witness(&mut self, query: PrototypeWitnessQuery) -> IntrospectionReply {
    self.handled_queries = self.handled_queries.saturating_add(1);
    let _ = (
        &self.target_directory,
        &self.query_planner,
        &self.manager_client,
        &self.router_client,
        &self.terminal_client,
        &self.store,
        &self.projection,
    );
    IntrospectionReply::PrototypeWitness(PrototypeWitness { /* Unknown */ })
}
```

After:

```rust
fn prototype_witness(&mut self, query: PrototypeWitnessQuery) -> IntrospectionReply {
    self.handled_queries = self.handled_queries.saturating_add(1);
    IntrospectionReply::PrototypeWitness(PrototypeWitness { /* Unknown */ })
}
```

**Why the placeholder was wrong.** Every field on `IntrospectionRoot` is already referenced in `stop_children` (each child is asked to stop and waited on at shutdown). The placeholder didn't actually prevent dead-code warnings — it just hid the truth that `prototype_witness` ignores its children. Clippy is clean without it. The honest shape is: `IntrospectionRoot` supervises the client actors, and `prototype_witness` is honest about which planes it asks (none, today). When Slice 2 wires `RouterClient`, the new field references appear naturally in the method body. No need to keep ceremony that lies about who's read.

The /190 §12.Q1 suggestion to use `#[allow(dead_code)]` was an alternative — but the fields aren't dead, so the attribute would itself be a lie. Removing the placeholder is the right move; it leaves the code stating what is true (held, supervised, not yet asked).

### 2. Architectural-truth tests

`tests/store.rs` (the existing source-scan home) now has two new tests.

**`introspect_daemon_does_not_depend_on_peer_component_contract_crates`** — opens `Cargo.toml` and asserts the dependency list contains none of:

- `signal-persona-router`
- `signal-persona-terminal`
- `signal-persona-message`
- `signal-persona-mind`
- `signal-persona-harness`
- `signal-persona-system`

This witnesses ARCHITECTURE.md §4's "Component observations remain component-owned" constraint at the strongest layer: the daemon literally cannot redefine a `RouterSummary` or `TerminalEvent` row because it doesn't pull in any peer contract crate. The existing source-scan test only covered redb paths and `redb::Database::open` calls; this test catches the next-layer failure of copying observation row types into the daemon's own crate.

When Slice 2 lands, this test will need to be relaxed for the per-peer contracts the daemon does call (almost certainly `signal-persona-router`, `signal-persona-terminal`). At that point the test would change to assert "depends on these per-peer contracts and only these," not "depends on no peer contract." That migration is mechanical when the wiring lands.

**`every_introspection_request_variant_persists_through_actor_root_and_sema_engine`** — for each of the four variants (`EngineSnapshot`, `ComponentSnapshot`, `DeliveryTrace`, `PrototypeWitness`), sends `HandleIntrospectionRequest` to the Kameo root, then reopens the store and verifies:

- exactly four observations in the table
- exactly four entries in the commit log
- each observation's `sequence`, `request`, and `reply` match
- each commit-log entry's head operation is `SignalVerb::Assert` against `introspection_observations`

This generalises the existing single-variant truth test to all four variants. It witnesses /190 §10's "Prototype witness travels through Kameo actors" constraint at full coverage, not just for PrototypeWitness; and it witnesses "Daemon opens introspect.redb through sema-engine" by inspecting the commit log's verb tags.

---

## What did not land, and why

### Router observation wiring

`RouterClient` cannot yet ask `RouterRequest::Summary`: the persona-router daemon does not serve the observation contract. As of this session's end:

- `/git/github.com/LiGoldragon/signal-persona-router/src/lib.rs` declares `RouterRequest::Summary`, `RouterRequest::MessageTrace`, `RouterRequest::ChannelState` — the contract is in place.
- `/git/github.com/LiGoldragon/persona-router/src/*.rs` contains no handler for these requests. The router daemon's source has no reference to `RouterSummaryQuery` / `RouterRequest` / `signal_persona_router`.

Per the prompt's coordination rule ("if it hasn't landed yet, don't speculate — leave the scaffolding"), I left the `ManagerClient`, `RouterClient`, `TerminalClient` actors in their current scaffolded form. They're held by `IntrospectionRoot`, supervised at shutdown, and not asked. When the router daemon gains an observation handler (paired agent 186's work), wiring `RouterClient` becomes a focused follow-up:

1. Add a `QueryRouterSummary` message type on `RouterClient`.
2. Implement the handler: connect to the router socket, send a length-prefixed `RouterRequest::Summary` frame, await the typed reply.
3. In `prototype_witness`, ask `RouterClient` and compose the result.
4. Add an end-to-end witness test (`prototype_witness_returns_router_status_when_router_observation_landed`) using `CARGO_BIN_EXE_persona_router_daemon` as a real peer.

### Closed-enum cleanup

A parallel `signal-persona-router` commit (`e2f9033`, `drop Unknown from wire status enums`) landed during this session. The introspect contract still has `ComponentReadiness::Unknown` and `DeliveryTraceStatus::Unknown`. Per the prompt's scope ("may be paired work with agent 193; if those need to retire, coordinate; otherwise leave them"), I left them — the contract-side retire belongs to whoever owns signal-persona-introspect contract changes, and the introspect daemon currently returns those variants as honest "not yet implemented" sentinels (will become typed `IntrospectionUnimplemented` reply variants per ARCH §0.6 once Slice 2 lands).

---

## Tests & build

Pre-change baseline: `nix flake check` green.

Post-change verification (`/git/github.com/LiGoldragon/persona-introspect`):

- `cargo test`: 11 passing (was 9; +2 new tests)
- `cargo clippy --all-targets -- -D warnings`: clean
- `nix flake check`: green

All eight named flake checks pass:

- `build`
- `test`
- `test-actor-runtime-truth`
- `test-daemon-socket`
- `test-daemon-applies-spawn-envelope-socket-mode`
- `test-daemon-answers-component-supervision-relation`
- `test-introspection-store-uses-sema-engine` (now exercises the two new tests as well)
- `fmt`, `clippy`

---

## Files touched

- `/git/github.com/LiGoldragon/persona-introspect/src/runtime.rs` — drop placeholder
- `/git/github.com/LiGoldragon/persona-introspect/tests/store.rs` — add two architectural-truth tests

No changes to `ARCHITECTURE.md`, `Cargo.toml`, `flake.nix`, or peer crates.

---

## Commits

- `ca74dc5 persona-introspect: drop redundant prototype_witness placeholder`
- `934ee7d persona-introspect: add architectural-truth tests for contract scoping and per-variant actor flow`

Both pushed to `persona-introspect:main`.

---

## See also

- `/home/li/primary/reports/designer/190-persona-introspect-gap-scan.md` — the gap scan this report closes against.
- `/home/li/primary/reports/designer/186-persona-router-gap-scan.md` — the parallel router observation contract work (gating Slice 2 wiring).
- `/git/github.com/LiGoldragon/persona-introspect/ARCHITECTURE.md` §4 — constraint table with witnesses (now stronger).
- `/home/li/primary/skills/architectural-truth-tests.md` — the witness discipline this work applies.
