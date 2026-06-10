# Persona engine + Agent component

> A mature, two-actor-system cluster: persona is a near-complete 9.4k-LOC privileged supervisor daemon (8 hand-written kameo actors), agent is the clean newer split-schema LLM-call daemon whose ~1.5k hand-written LOC sits behind ~1.8k of fresh-verified generated code. Both daemons are real. The standout risks are agent's lone nota-next d8862b6 pin (the isolated encoding bump) against codegen from 8-commit-behind schema-rust-next, hand-rolled NOTA brackets in signal-persona/origin.rs, and a cluster-wide pre-52ro verbose-schema / stale-concept-schema debt; persona-pi is a genuine but 17-day-dormant concept-only seed.

## Cluster: Persona engine + Agent component

Two real component daemons anchor this cluster, each following the generated-skeleton + hand-written-hooks pattern, plus their working/meta signal contract crates and one dormant seed. Both daemons are genuine (not scaffolds): **persona** is a heavyweight privileged supervisor with eight hand-written kameo actors; **agent** is the cleaner newer LLM-call daemon whose actor and daemon spine are schema-emitted. The cluster's discipline is strong — five of six code repos are spotless on both the free-function and fake-NOTA rules — so the findings concentrate in a handful of named sites plus a uniform toolchain-lag and stale-concept-schema debt.

### Per-repo table

| Repo | Role | Prod / Test / Gen LOC | Intent | Daemon shape | Complete | nota-next pin | Free-fn | Fake-NOTA |
|---|---|---|---|---|---|---|---|---|
| persona | Privileged engine-manager daemon | 9439 / 4962 / 558 | aligned | real (8 kameo actors) | ~90% | ae5c25c (4 behind, safe) | 3 lib + ~20 bin | 0 |
| signal-persona | Working-signal + origin contract | 798 / 262 / 0 | mixed | library | ~95% | ae5c25c (4 behind, safe) | 0 | 6 |
| meta-signal-persona | Meta policy Frame contract | 325 / 216 / 0 | aligned | library | ~95% | ae5c25c (4 behind, safe) | 0 | 0 |
| agent | LLM-API-call daemon (report 569) | 1472 / 151 / 1807 | aligned | real (1 generated EngineActor) | ~85% | **d8862b6 (HEAD — the bump)** | 0 | 0 |
| signal-agent | Working-signal Call/Completion contract | 456 / 330 / 0 | mixed | library | ~90% | ae5c25c (4 behind, safe) | 0 | 0 |
| meta-signal-agent | Meta provider-policy contract | 484 / 280 / 0 | aligned | library | ~95% | ae5c25c (4 behind, safe) | 0 | 0 |
| persona-pi | Concept seed (Pi surface) | 0 / 0 / 0 | scaffold | concept-only | ~5% | n/a (not a crate) | 0 | 0 |

LOC notes: no inline `#[cfg(test)]` modules exist anywhere in this cluster — all test code lives in `tests/`. Production = total `src/*.rs` minus checked-in generated `src/schema/*.rs`. The baseline overcounted two repos: **agent's** apparent 3425 is really 1472 hand-written + 1807 generated; **persona's** 10044 is 9439 + 558 generated.

### Foundation-crate status (Cargo.lock is the sole truth)

Every flake.lock in this cluster locks only the Nix toolchain (crane/fenix/nixpkgs) — the foundation crates flow purely through Cargo git deps, so there is no Cargo.lock-vs-flake.lock disagreement to reconcile, and **agent has no flake.lock at all**. Uniform lag against HEAD:

- **schema-next** 77e71a4 → c8ebb39: **5 behind** (persona, agent, signal-agent).
- **schema-rust-next** 7282446 → eca4028: **8 behind** (persona, agent, signal-agent). Today's `FixedBytes<N>` grammar (c8ebb399 + eca40280) has reached none of them.
- **triad-runtime** ae2e817 → 6ea8316: **1 behind** (persona, agent) — HEAD renames `DaemonConfiguration` to `BindingSurface`.
- **version-projection** e40fd14 → f00b239: **1 behind** (persona).
- **nota-next**: persona and all four signal/meta-signal crates pin **ae5c25c (4 behind, safe — not the encoding bump)**; **agent alone pins d8862b6**, the bump.

### Finding: agent's nota-next d8862b6 against isolated codegen (FLAG)

`agent/Cargo.lock` pins **nota-next d8862b6** — the encoding bump — while pinning **schema-rust-next 7282446** (8 commits behind). Per the brief, schema-rust-next HEAD deliberately still pins nota-next `ae5c25cd` to isolate that bump. Agent therefore links the new encoding while its generated `NotaEncode`/`NotaDecode` came from the older emitter, and `default = ["nota-text"]` makes that codec live (not feature-gated off). This is the precise isolation-violating combination flagged — a plausible, unverified NOTA encoding-format mismatch. It is also an intra-triad disagreement: agent's own contract crate `signal-agent` is on ae5c25c. Resolve before this ships.

### Finding: hand-rolled NOTA brackets in signal-persona/origin.rs

`signal-persona/src/origin.rs` is the only fake-NOTA offender in the cluster: three hand-written `NotaEncode` impls assemble paren-records with `format!("(Tag {})")` string interpolation across six sites, while **13 sibling types in the same file use `#[derive(NotaEncode)]`**. The child `.to_nota()` delegation is fine; the hand-built brackets around it are the anti-pattern.

- `/git/github.com/LiGoldragon/signal-persona/src/origin.rs:251-272` — `impl NotaEncode for ConnectionClass`: `format!("(NonOwnerUser {})" …)`, `(System …)`, `(OtherPersona … …)`, `(Network …)`.
- `/git/github.com/LiGoldragon/signal-persona/src/origin.rs:331-335` — `impl NotaEncode for InternalComponentInstanceOrigin`: `format!("({} {})", self.component.to_nota(), self.instance.to_nota())`.
- `/git/github.com/LiGoldragon/signal-persona/src/origin.rs:394-397` — `impl NotaEncode for IngressContext`: `format!("({})", self.origin.to_nota())`.

Contrast — these are **correct** and were not flagged: `signal-agent` `TranscriptToken::to_nota` uses `Delimiter::Parenthesis.wrap([…])` (the nota-next block API); persona/agent `to_nota` methods all delegate to `<Self as NotaEncode>::to_nota`; agent's generated `src/schema/*.rs` `to_nota` delegate to the derive.

### Finding: free functions concentrate in persona

The library-proper violations (3):

- `/git/github.com/LiGoldragon/persona/src/transport.rs:24` `unlink_existing_socket_path` — belongs on `PersonaEndpoint` (defined at `transport.rs:44`).
- `/git/github.com/LiGoldragon/persona/src/transport.rs:38` `prepare_socket_parent` — same owner.
- `/git/github.com/LiGoldragon/persona/src/unit.rs:924` `systemd_manager_method` — a `UnitAction → &'static str` conversion that should be `impl UnitAction`.

Plus ~20 helper free fns across the six `src/bin/wire_*` test-harness binaries and `persona_component_fixture.rs` (each a `[[bin]]` with `fn main`): `parse_variant`, `parse_origin`, `build_reply_frame`, `write_nota`, `connect_with_retry`, `read_length_prefixed_frame`, etc. These violate the rule but live in dedicated wire-protocol test tooling, a lesser concern. **agent, signal-persona, meta-signal-persona, signal-agent, meta-signal-agent are completely clean (0 free fns).**

### Finding: schema duality — concept cruft vs live split schemas

Two distinct states coexist:

- **Leaf contract crates (signal-persona, signal-agent, meta-signal-persona, meta-signal-agent):** the `.concept.schema` files are **stale cruft** — verbose pre-52ro, stamped `(Status Concept)`, and they do not match the hand-written Rust. The starkest case is `signal-agent.concept.schema` (names `Call/Session/Transcript`, `Prompt/Tool/Cancel`) versus its lib (`AgentIdentifier`, `MessageDelivery`, `TranscriptToken`, `AgentLifecycle`). The Rust is the live source of truth; the schema is dead documentation. `meta-signal-agent`'s file even keeps an outdated `owner-signal-agent.concept.schema` filename.
- **agent:** the only repo on the modern **split triad-port** form (`schema/nexus.schema` + `schema/sema.schema`, no concept file), and here the schemas ARE the live truth — `build.rs` regenerates `src/schema/{nexus,sema,daemon}.rs` via schema-rust-next and asserts the checked-in copy is fresh. Their bodies are still pre-52ro verbose (`(SignalArrived SignalArrived)`, `(Completed Completed)`), so 52ro self-tag adoption is the migration debt; the sema plane is honestly `Stateless` (durable projection deferred).
- **persona:** carries a verbose monolithic `persona.concept.schema` plus a near-empty `daemon.schema` (`{} [] [] {}`); neither is live (the daemon is generated from the `NexusDaemonShape` in `build.rs`).

### Finding: persona-pi is a real but dormant seed

`persona-pi` has **zero code** — a coherent v0.1 concept schema (Session/Agent/Extension roots, Configure Model/Provider meta) plus deliberate Pi/criomos Nix packaging (`pi-linkup`, `pi-subagents`). Last commit 2026-05-24, 17 days before this audit. Judgment: a **genuine seed gone quiet**, not stale cruft — but it is not a Rust crate (no Cargo.toml), has no triad legs, and has no `INTENT.md`. Decide explicitly whether it is active (then it needs a crate + triad) or parked (then say so), and add the missing `INTENT.md` either way.
