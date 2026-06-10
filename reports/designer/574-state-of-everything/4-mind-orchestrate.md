# Mind + Orchestrate

> Two genuinely-built triad components with clean codecs (zero fake-NOTA cluster-wide) but real free-function debt in orchestrate (12) and divergent daemon architectures: mind runs a 14-actor hand-written kameo mesh, orchestrate rides a single generated EngineActor. The cruft is concentrated — orchestrate carries 5 dead versioned/.concept schema files and the oldest nota-next pin (f0e435a, 8 behind), and every consumer emits from a schema-rust-next that is 8 commits stale (pre-Bytes-prelude). No consumer pins nota-next d8862b6, so the encoding-bump flag does NOT fire here.

## Cluster: Mind + Orchestrate

**Verdict.** Two genuinely-built triad components, not scaffolds. Codec hygiene is excellent — **zero fake-NOTA across all six repos**. The interesting structural fact is that the two daemons are built oppositely: `mind` runs a **14-actor hand-written kameo mesh** (`MindRoot` tree, component-decoded `MindFrame` working tier), while `orchestrate` rides a **single generated `EngineActor<OrchestrateDaemon>`** whose mailbox serialises every request onto one `OrchestrateService` engine. Both are legitimate; they reflect different problems (mind's choreography/subscription concurrency vs orchestrate's serial claim-ledger).

The debt is concentrated, not diffuse: `orchestrate` carries **12 free-function violations** and **5 dead schema files**, and holds the **oldest nota-next pin** in the cluster. Every codegen consumer emits from a **schema-rust-next that is 8 commits stale** (pre-Bytes-prelude). **No consumer pins nota-next `d8862b6`** — the encoding-bump flag does not fire here; the codegen repos all sit on `ae5c25c`, which is exactly schema-rust-next's deliberate isolation rev.

### Per-repo summary

| Repo | Role | Prod LOC (gen) | Test | Daemon shape | Intent | Free-fn | Fake-NOTA | nota-next pin |
|---|---|---|---|---|---|---|---|---|
| mind | central control-plane daemon | 9921 (2569) | 3356 | real 14-actor kameo mesh | aligned | 2 | 0 | ae5c25c (−4) |
| signal-mind | ordinary mind wire contract | 2712 (0) | 1315 | contract-only, hand-written | aligned | 0 | 0 | ae5c25c (−4) |
| meta-signal-mind | meta mind policy contract | 241 (0) | 122 | contract-only, hand-written | aligned | 0 | 0 | ae5c25c (−4) |
| orchestrate | machinery daemon (claims/lanes/roles) | 7201 (2234) | 1888 | real, single generated EngineActor | mixed | 12 | 0 | **f0e435a (−8)** |
| signal-orchestrate | ordinary orchestrate contract | 2803 (1702) | 725 | contract-only, schema-emitted | aligned | 0 | 0 | ae5c25c (−4) |
| meta-signal-orchestrate | meta orchestrate contract | 1291 (1047) | 286 | contract-only, schema-emitted | aligned | 0 | 0 | ae5c25c (−4) |

Prod LOC = `src` + generated `src/schema`, minus inline `#[cfg(test)]` and `tests/`. Inline test modules are negligible (mind 211, orchestrate 9, rest 0), so the refined figures track the baseline closely; the meaningful correction is splitting out **generated** LOC, which is large (mind 2569, orchestrate 2234, signal-orchestrate 1702, meta-signal-orchestrate 1047).

### Dependency status

Every `flake.lock` in the cluster carries **only the Nix toolchain** (crane/fenix/nixpkgs/flake-utils) — foundation crates are resolved by Cargo from git, so the real pins live solely in `Cargo.lock` and **no Cargo-vs-flake disagreement is possible** on foundation revs.

The codegen consumers (mind, orchestrate, signal-orchestrate, meta-signal-orchestrate) all pin **schema-next `77e71a4` (5 behind `c8ebb39`)** and **schema-rust-next `7282446` (8 behind `eca4028`)** — so all checked-in `src/schema/*.rs` predates the Bytes prelude / FixedBytes work and carries no `Bytes` leaf.

nota-next pins split: **mind / signal-mind / signal-orchestrate / meta-signal-orchestrate → `ae5c25c` (4 behind HEAD)** — exactly schema-rust-next's isolation rev. **orchestrate alone → `f0e435a`, which is 8 behind HEAD and 4 behind even `ae5c25c`** (it predates the numeric codecs). orchestrate is the laggard across the board: also sema-engine `5cee993` (−2) and signal-frame `904bb2f` (−4). One outlier elsewhere: **meta-signal-mind pins signal-frame `8b128d3` (−1)**, the only repo behind the cluster's `166bda8`.

### Free functions (14 total: mind 2, orchestrate 12)

mind:
- `/git/github.com/LiGoldragon/mind/src/supervision.rs:28` `supervision_synthetic_exchange` — builds a constant `ExchangeIdentifier`; self-labeled wave-1 placeholder. → `ExchangeIdentifier::synthetic()`.
- `/git/github.com/LiGoldragon/mind/src/actors/choreography.rs:336` `exchange` — identical body, duplicated. Same fix, shared.

orchestrate:
- `src/lock_projection.rs:39` `lock_line` / `:43` `scope_text` — claim/scope → text; want `impl Display`.
- `src/service.rs:326` `reject_handover` — constructs `UpgradeReply::HandoverRejected`; want associated fn.
- `src/service.rs:330` `first_committed_payload` — unwraps `Reply<Payload>`; want a method on `Reply`.
- `src/lane.rs:106` `pascal_to_kebab` / `:117` `ordinal_word` — string/ordinal conversions floating at module level.
- `src/handover.rs:160` `civil_date_from_unix_days` — calendar math returning a bare `(i32,u32,u32)` tuple; want `TryFrom` on a date newtype (also a typed-value smell).
- `src/activity.rs:86` `path_matches_prefix` — predicate over `&str`; belongs on the path type.
- `src/layout.rs:65` `wire_path` (pub) — `&Path → WirePath`; this is `TryFrom<&Path> for WirePath`.
- `src/repository.rs:49` and `:57` `create_repository_link` — two `cfg(unix)`/`cfg(not(unix))` fs-symlink fns; one logical violation across two arms.

### Fake-NOTA — none

All `to_nota` impls in this cluster are correct manual codecs: they delegate to nota-next's `Delimiter::Parenthesis.wrap(...)` and to child `NotaEncode`, and every decode path goes through `NotaBlock::new(block).expect_delimited(...)` / `demote_to_string`, never paren-splitting or char-indexing. `mind/src/text.rs` (11 `to_nota`), `signal-mind/src/graph.rs`, and the contract crates were all inspected and are clean — these are deliberate hand-written codec layers (e.g. `TextVariantEncoding`/`TextVariantRecord` in mind), not paren-string assembly. No `format!("(...)")` or `push_str("(")` record-building exists in any non-generated source.

### Schema state and the concept/triad duality

Every repo still carries an OLD `<name>.concept.schema` that is **no longer the source of truth**. Live sources are the split triad-port schemas: `nexus.schema`+`sema.schema` (mind, orchestrate), `signal.schema` too for mind, and `lib.schema` for the orchestrate contracts. `orchestrate` is the worst offender with **5 dead, unreferenced schema files** (`orchestrate.concept.schema`, `orchestrate-v0-1.schema`, `orchestrate-v0-1-1.schema`, `orchestrate-types-v0-1.schema`, `orchestrate-storage-v0-1.schema`) — confirmed against `build.rs`, which reads only `nexus.schema`/`sema.schema`. The two `signal-mind`/`meta-signal-mind` contracts are hand-written (no `build.rs`, no codegen), so their `.concept.schema` files are purely documentary and stale; `meta-signal-mind`'s even still self-labels `(Status Concept)` while its Rust is real and tested.

Terse-form (2026-06-10 grammar) adoption is **partial**: distinct-newtype variants are already modern (`(Claim RoleClaim)`, `(CommandSemaRead SemaReadInput)`), but pure self-tags still repeat the name — `(SignalArrived SignalArrived)`, `(Continue Continue)`, `(ClaimAcceptance ClaimAcceptance)` — which is the pre-**52ro** verbose form (should collapse to arity-1 `(Name)`). The **yp29** (`Bytes` leaf) and **lm84** (hash-id newtype) forms are simply **N/A** here — neither concept appears in this cluster's domain, so their absence is correctness, not debt. The cheap migration is the self-tag collapse, and it should ride on the same regeneration that bumps schema-rust-next off the 8-behind pin.
