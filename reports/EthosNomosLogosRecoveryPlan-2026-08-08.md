# Ethos / Nomos / Logos Recovery Plan

2026-08-08 -- Executable staged plan for the psyche-ordered major recovery.

## 1. As-Is Inventory

### 1.1 Ethos

| Repo | State | Lines | Notes |
|---|---|---|---|
| `ethos-engine` | Real daemon. Unix socket, kameo actors (SignalPlane, NexusPlane, SemaPlane), handles signal-ethos Request/Reply. Three ingest paths: `authority_ingest.rs` (445 LOC), `legacy_ingest.rs` (321), `legacy_storage_ingest.rs` (177). Bin: `ethos-engine.rs`. | ~1231 total | Native ingest still speaks the superseded six-slot syntax. The blessed bootstrap syntax lives in `core-ethos`'s reader. |
| `signal-ethos` | Real contract. Has `Request`/`Reply` enums, rkyv encode/decode. | 77 LOC | Only consumer: `ethos-engine`. Low blast radius. |
| `core-ethos` | Bootstrap reader/parser. The source of truth for the new blessed syntax. | ~2000+ LOC | 12 direct Cargo consumers across the estate. High blast radius for any rename. |
| `meta-signal-ethos` | Does not exist. | -- | Must be created. |

Missing from target shape: ordinary CLI, metasocket CLI, meta-signal contract, daemon ingest convergence onto blessed syntax.

### 1.2 Nomos

| Repo | State | Lines | Notes |
|---|---|---|---|
| `nomos-engine` | Not a daemon. A 91-line synchronous library (`lib.rs`) wrapping `core-nomos` lowering. `autobins = false`, `autotests = false`. | 91 LOC | Needs complete rewrite as a daemon. |
| `signal-nomos` | Wire vocabulary only: `NomosSlotId`, `SlotGeneration`, `SlotExpectation`, `CapsuleSelector`, `WireInvariant`. No `Request`/`Reply`. | 127 LOC | Explicitly excluded Request/Reply "while there is no process boundary." A daemon creates the process boundary, so R/R is now needed. |
| `core-nomos` | Real lowering logic. `bootstrap.rs` (755 LOC) does the Ethos-to-WholeLogos transformation. | ~755 LOC | The engine's brain. |
| `nomos-types` | StreamInitiation/StreamTermination data types. v0.1.0. | small | Shared vocabulary for the stream section. |
| `meta-signal-nomos` | Does not exist. | -- | Must be created. |

Missing from target shape: daemon binary, Unix socket handling, kameo actors, Request/Reply contract, meta-signal contract, CLIs, sema-engine storage with transformer index.

### 1.3 Logos

| Repo | State | Lines | Notes |
|---|---|---|---|
| `logos-engine` | Real daemon. Unix socket, kameo actors (SignalPlane, NexusPlane, SemaPlane), tokio runtime. Stateless projection -- receives WholeLogos and emits Rust code via `rust-logos`. | ~475 LOC lib + bin | Functional but missing CLIs, meta-signal, and proper sema-engine storage. |
| `signal-logos` | Real contract. Has `Request`/`Reply` enums, rkyv encode/decode. | 61 LOC | Consumer: `logos-engine`, `protos-engine`. |
| `core-logos` | WholeLogos types and the fully explicit program description. | -- | Shared between logos-engine, nomos-engine, protos-engine. |
| `meta-signal-logos` | Does not exist. | -- | Must be created. |
| `rust-logos` | Rust emitter. Turns WholeLogos into Rust source text. | -- | Used by logos-engine. |

Missing from target shape: ordinary CLI, metasocket CLI, meta-signal contract, proper sema-engine backed storage (the SemaPlane actor exists but may not be wired to sema-storage).

### 1.4 Supporting infrastructure

| Piece | State |
|---|---|
| `sema-storage` | **STANDING-RULING VIOLATION** — psyche 2026-07-27, verbatim: "There can be no sema-storage daemon, as it would overload the term sema." All daemon state lives in each daemon's own sema db. This shared storage daemon must dissolve during recovery: each daemon embeds its own sema-engine database, and sema-storage's documents fold into their owning daemons. Its DocumentKind enum dies with it. |
| `sema-engine` | Append-only versioned log. The storage backend for all component daemons. |
| `protos-engine` | 37 flake inputs pinning nearly every repo in the estate. The orchestrator of the pipeline. |
| Batch track (signal-spirit, meta-signal-spirit) | Build-script generation via `.schema` files. Working pattern that could template meta-signal-ethos/nomos/logos. |

## 2. Target Shape Per Component

Reference: `spirit` daemon. Each component (`ethos`, `nomos`, `logos`) must have:

```
<component>/
  src/
    lib.rs                       -- kameo actors: SignalPlane, NexusPlane, SemaPlane
    bin/
      <component>-daemon.rs      -- daemon binary (~5 lines, calls run_to_exit_code)
      <component>.rs             -- ordinary CLI shim (nota-text gated)
      meta-<component>.rs        -- metasocket CLI shim (nota-text gated)
```

Plus these sibling repos:

- `signal-<component>` -- Request/Reply contract (rkyv binary messages)
- `meta-signal-<component>` -- configuration/meta contract
- `core-<component>` -- library logic (OPEN: whether this stays separate)

Storage: each daemon embeds its OWN sema-engine database (append-only
versioned log). No daemon delegates persistence to a shared storage
daemon — the psyche's 2026-07-27 ruling forbids a sema-storage daemon.

### 2.1 Concrete operations per component

**Ethos:**

1. Repo: rename `ethos-engine` to `ethos` on GitHub (preserves history, redirects old URLs) OR create fresh `ethos` repo and archive `ethos-engine`. (OPEN-A)
2. Rename bin from `ethos-engine.rs` to `ethos-daemon.rs`.
3. Add `ethos.rs` (ordinary CLI shim) and `meta-ethos.rs` (metasocket CLI shim).
4. Create `meta-signal-ethos` repo (follow batch track pattern from meta-signal-spirit if build-script track is kept, else hand-author).
5. Wire `meta-signal-ethos` as a Cargo dependency.
6. Converge daemon ingest onto the blessed bootstrap syntax from `core-ethos` -- retire `legacy_ingest.rs` and `legacy_storage_ingest.rs`, update `authority_ingest.rs` to use `core-ethos`'s reader. (OPEN-D)
7. Rewire SemaPlane from the sema-storage socket to an embedded sema-engine store (the daemon owns its database, per the 2026-07-27 ruling); migrate its documents in.
8. If `core-ethos` stays separate (OPEN-B): no move. If folded in: merge its source into the `ethos` repo, update all 12 downstream Cargo consumers.

**Nomos:**

1. Repo: rename `nomos-engine` to `nomos` on GitHub OR create fresh `nomos` repo. (OPEN-A)
2. Rewrite the 91-line library wrapper into a full daemon (see Section 5: Nomos Daemon Birth Plan).
3. Add Request/Reply to `signal-nomos` (the process boundary now exists).
4. Create `meta-signal-nomos` repo.
5. Add `nomos-daemon.rs`, `nomos.rs` (CLI), `meta-nomos.rs` (meta CLI).
6. Wire sema-engine storage with transformer index.
7. If `core-nomos` stays separate (OPEN-B): keep as library dependency. If folded in: merge.

**Logos:**

1. Repo: rename `logos-engine` to `logos` on GitHub OR create fresh `logos` repo. (OPEN-A)
2. Rename bin from `logos-engine.rs` to `logos-daemon.rs`.
3. Add `logos.rs` (ordinary CLI shim) and `meta-logos.rs` (metasocket CLI shim).
4. Create `meta-signal-logos` repo.
5. Wire `meta-signal-logos` as a Cargo dependency.
6. Rewire SemaPlane to an embedded sema-engine store where persistence is needed — no sema-storage socket (the daemon owns its database, per the 2026-07-27 ruling).
7. If `core-logos` stays separate (OPEN-B): no move. If folded in: merge.

## 3. Blast Radius

### 3.1 Repo rename impact

**`ethos-engine` rename:** LEAF repo. Only consumer of `signal-ethos`. Zero downstream Cargo dependents. GitHub redirect handles git URL references. Impact: update protos-engine flake input (2 refs), any CriomOS packaging (0 refs found), Cargo.toml self-reference.

**`logos-engine` rename:** Near-leaf. Consumed by protos-engine only. Impact: update protos-engine flake input (2 refs), Cargo.toml self-reference.

**`nomos-engine` rename:** Near-leaf. Consumed by protos-engine only. Impact: update protos-engine flake input (2 refs), Cargo.toml self-reference. (This is a rewrite, not just a rename.)

**`core-ethos` rename (if folded):** HIGH blast radius. 12 direct Cargo consumers: ethos-engine, core-nomos, core-schema, schema-rust, nomos-engine, sema-engine, sema-translator, signal-persona, signal-message, signal-lojix, meta-signal-lojix, meta-signal-message. Every consumer's Cargo.toml and flake.nix must be updated. Recommendation: keep `core-ethos` separate unless the psyche specifically folds it.

### 3.2 protos-engine (37 inputs)

Protos-engine pins nearly everything. Any repo rename or URL change requires updating its flake.nix. The following inputs are directly affected:

- `core-ethos`, `core-logos`, `core-nomos` (3 primary + 3 stream-prefixed = 6)
- `nomos-engine` (1)
- `signal-nomos` (1)
- `signal-domain` (1)
- `rust-logos` (2: primary + template)
- `sema-engine`, `sema-translator` (2)
- `signal-frame` (1)
- New additions needed: `meta-signal-ethos`, `meta-signal-nomos`, `meta-signal-logos`

Total protos-engine flake edits per stage must be batched with a full `nix flake check`.

### 3.3 Nix packaging

- `ethos-engine`, `logos-engine`, `nomos-engine` flakes are self-contained (only nixpkgs + flake-utils + rust-build). Rename is a flake.nix URL update.
- CriomOS and CriomOS-home have zero references to the daemon repos (confirmed by grep). No system packaging changes needed for the rename itself.
- New repos (`meta-signal-ethos`, `meta-signal-nomos`, `meta-signal-logos`) need their own flake.nix following the standard rust-build pattern.

## 4. Staged Execution Order

Each stage leaves everything buildable.

### Stage 0: Preparation (no repo changes)

- [ ] Resolve OPEN decisions A through D (Section 6).
- [ ] Draft `meta-signal-ethos`, `meta-signal-nomos`, `meta-signal-logos` schema files (can follow the meta-signal-spirit pattern).
- [ ] Draft the signal-nomos Request/Reply expansion.
- [ ] Document the Nomos daemon actor architecture (what messages, what storage keys).

### Stage 1: Create meta-signal repos (additive, breaks nothing)

- [ ] Create `meta-signal-ethos` repo with flake.nix, Cargo.toml, schema file, build script (if batch track kept) or hand-authored contract.
- [ ] Create `meta-signal-nomos` repo, same pattern.
- [ ] Create `meta-signal-logos` repo, same pattern.
- [ ] Each must pass `cargo test` and `nix flake check` independently.

### Stage 2: Expand signal-nomos with Request/Reply

- [ ] Add `Request` and `Reply` enums to `signal-nomos` (modeled on signal-ethos/signal-logos pattern).
- [ ] Update `signal-nomos` version, push, verify.
- [ ] No downstream breakage: nothing currently imports Request/Reply from signal-nomos.

### Stage 3: Rename daemon repos (if rename path chosen)

If OPEN-A resolves to rename:

- [ ] Rename `ethos-engine` to `ethos` on GitHub.
- [ ] Rename `logos-engine` to `logos` on GitHub.
- [ ] Rename `nomos-engine` to `nomos` on GitHub.
- [ ] Update each repo's Cargo.toml (package name, repository URL, binary names).
- [ ] Update protos-engine flake.nix inputs (6 URL changes).
- [ ] Run `nix flake check` on protos-engine.

If OPEN-A resolves to fresh repos:

- [ ] Create `ethos` repo, move code from `ethos-engine`, archive `ethos-engine`.
- [ ] Create `logos` repo, move code from `logos-engine`, archive `logos-engine`.
- [ ] Create `nomos` repo (fresh daemon, not a move -- see Stage 5).
- [ ] Update all flake.nix references across the estate.

### Stage 4: Add CLIs and meta-signal wiring to Ethos and Logos

- [ ] In `ethos` (renamed/new): add `ethos-daemon.rs` (rename from ethos-engine.rs), `ethos.rs` (CLI shim), `meta-ethos.rs` (meta CLI shim).
- [ ] Wire `meta-signal-ethos` as Cargo dependency, feature-gate CLIs behind `nota-text`.
- [ ] In `logos` (renamed/new): add `logos-daemon.rs`, `logos.rs`, `meta-logos.rs`.
- [ ] Wire `meta-signal-logos` as Cargo dependency, feature-gate CLIs.
- [ ] Both must pass `cargo test` and `nix flake check`.

### Stage 5: Nomos Daemon Birth (see Section 5)

- [ ] Build the `nomos` daemon from scratch in the renamed/new repo.
- [ ] Wire `signal-nomos` (now with Request/Reply), `meta-signal-nomos`, `core-nomos`.
- [ ] Implement kameo actors: SignalPlane, NexusPlane (transformer execution), SemaPlane (transformer index storage).
- [ ] Wire sema-engine storage.
- [ ] Add `nomos-daemon.rs`, `nomos.rs`, `meta-nomos.rs`.
- [ ] Pass `cargo test` and `nix flake check`.

### Stage 6: Daemon ingest convergence (Ethos)

- [ ] Retire `legacy_ingest.rs` and `legacy_storage_ingest.rs` from ethos.
- [ ] Update `authority_ingest.rs` to use core-ethos's bootstrap reader (blessed syntax).
- [ ] Verify end-to-end: ethos daemon can ingest files written in the current blessed syntax.
- [ ] Pass `cargo test` and `nix flake check`.

### Stage 7: protos-engine full integration

- [ ] Update all protos-engine flake.nix inputs to point at the renamed/new repos.
- [ ] Add `meta-signal-ethos`, `meta-signal-nomos`, `meta-signal-logos` as new flake inputs.
- [ ] Full `nix flake check` on protos-engine.
- [ ] Verify the generation pipeline still produces correct signal-spirit and meta-signal-spirit output.

### Stage 8: Cleanup

- [ ] Archive `spirit-ethos` (condemned, still alive and buildable).
- [ ] Delete stale `core-schema` clone if still present.
- [ ] Dissolve the sema-storage daemon: migrate its documents into the owning daemons' embedded stores, then retire the repo (psyche 2026-07-27: no sema-storage daemon may exist).
- [ ] Update any remaining documentation, design files, and awareness records.

## 5. Nomos Daemon Birth Plan

### What exists today

- `core-nomos` (`bootstrap.rs`, 755 LOC): the real lowering engine. Takes parsed Ethos declarations and produces `WholeLogos` via hardcoded Rust transformation. This is the temporary hack sanctioned by the psyche until self-hosting.
- `nomos-engine`: a 91-line lib.rs that wraps `core-nomos` lowering as a synchronous library call. Not a daemon. No socket, no actors, no persistence.
- `signal-nomos`: slot vocabulary only. No Request/Reply.
- `nomos-types`: StreamInitiation/StreamTermination types.

### What the daemon needs

**Architecture** (modeled on ethos-engine and logos-engine):

1. **Unix socket listener** (tokio UnixListener) accepting rkyv-encoded signal-nomos messages.
2. **SignalPlane** actor: deserializes incoming Request, dispatches to NexusPlane, serializes Reply.
3. **NexusPlane** actor: holds the transformer index, executes transformations by calling core-nomos lowering (initially the hardcoded bootstrap, eventually self-hosted transformer evaluation).
4. **SemaPlane** actor: manages persistence via sema-engine. Stores:
   - The transformer index (loaded from textual Nomos at startup, eventually from the database).
   - Transformation results (WholeLogos output, keyed by capsule/request ID).
5. **Binary**: `nomos-daemon.rs` (~5 lines, standard run_to_exit_code pattern).

**Signal contract** (additions to signal-nomos):

```
Request:
  Transform { source: <parsed ethos input>, capsule_id: <identifier> }
  LoadTransformer { definition: <nomos textual form> }
  QueryTransformer { name: <transformer name> }

Reply:
  Transformed { capsule_id: <identifier>, logos: WholeLogos }
  TransformerLoaded { name: <transformer name> }
  TransformerFound { definition: ... }
  Refused { reason: ... }
```

(Exact types TBD per psyche ruling on the Nomos language design campaign.)

**Startup sequence:**

1. Nomos daemon starts, binds Unix socket.
2. Loads bootstrap transformers from textual Nomos files (the standard Ethos-to-Logos transformers).
3. Stores them in the transformer index (SemaPlane).
4. Listens for Transform requests from the Ethos daemon.

**Communication flow** (per psyche vision):

1. Ethos daemon receives parsed Ethos input.
2. Ethos sends a Transform request to Nomos via signal-nomos.
3. Nomos NexusPlane runs the appropriate transformer(s), producing WholeLogos.
4. Nomos communicates with Logos daemon (via signal-logos) to deliver the WholeLogos objects: "here is a new capsule, here are the objects."
5. Nomos replies to Ethos with the transformation result.

**Dependencies:**

- `core-nomos` (lowering logic)
- `core-logos` (WholeLogos types for output)
- `core-ethos` (parsed input types)
- `signal-nomos` (Request/Reply contract)
- `meta-signal-nomos` (configuration contract)
- `signal-logos` (for forwarding to Logos daemon)
- `sema-engine` (embedded persistence — the daemon owns its own database)
- `kameo` (actor framework)
- `rkyv` (serialization)
- `tokio` (async runtime)

## 6. OPEN Decision Points

### OPEN-A: Rename vs fresh repos

**Rename `ethos-engine` to `ethos`, `logos-engine` to `logos`, `nomos-engine` to `nomos`:**
- Pro: preserves git history, GitHub auto-redirects old URLs, lower effort.
- Con: old Cargo.toml package names linger in lock files; for nomos-engine the code is a near-total rewrite anyway.
- Recommendation: rename ethos-engine and logos-engine (real daemons with salvageable code); fresh repo for nomos (the 91-line wrapper is not worth preserving).

**If fresh repos:**
- All three get new repos; old repos archived.
- All flake.nix references across the estate must be updated to new URLs (no redirect).

### OPEN-B: Whether `core-*` libraries stay separate

**Separate (status quo):**
- Pro: 12 downstream consumers of core-ethos would break on a fold; clean dependency boundaries; components that need parsing but not the daemon can depend on core-ethos alone.
- Con: more repos to maintain; version coordination overhead.
- Recommendation: keep separate. core-ethos is consumed by too many crates to fold without a massive cascade.

**Folded into the main repo:**
- core-ethos, core-nomos, core-logos source moves into ethos, nomos, logos respectively.
- Every downstream Cargo.toml and flake.nix for all 12+ consumers of core-ethos must be updated.
- core-nomos and core-logos have fewer consumers (mainly protos-engine, logos-engine, nomos-engine) -- fold is feasible for these two if desired.

### OPEN-C: Whether the build-script batch track keeps running as scaffolding

**Keep (status quo for signal-spirit, meta-signal-spirit):**
- The `.schema` file + build.rs pattern generates contract crate source from authored Ethos files.
- meta-signal-ethos, meta-signal-nomos, meta-signal-logos could follow this pattern.
- Pro: consistent, one pipeline for all contracts.
- Con: the pipeline has known gaps (freshness digest only binds source text, not generator revision; `autotests = false` silently disables tests in 9 repos).

**Retire:**
- Hand-author meta-signal-ethos/nomos/logos contracts.
- Pro: no build-script complexity; contracts are small enough to hand-maintain.
- Con: diverges from the Spirit pattern; loses the "one interface file generates everything" vision.

### OPEN-D: Daemon ingest convergence onto the blessed bootstrap syntax

**Converge now (Stage 6):**
- Retire legacy ingest paths in ethos-engine immediately after rename.
- Pro: single code path, no more syntax confusion.
- Con: any existing consumers of the old six-slot syntax break.

**Converge later:**
- Keep legacy ingest as a compatibility shim during the recovery.
- Pro: nothing breaks during recovery stages.
- Con: two parsers, continued confusion about which syntax is canonical.

**Hybrid:**
- Converge at Stage 6 but keep legacy ingest behind a feature flag for one release cycle.

### Resolved by standing ruling: no sema-storage daemon

The psyche ruled 2026-07-27, un-superseded: "sema is the database of each daemon... There can be no sema-storage daemon, as it would overload the term sema." The recovery therefore embeds a sema-engine store in each daemon and dissolves sema-storage (Stage 8). The former DocumentKind question dissolves with it: each daemon defines its own store schema for the language it holds — the Ethos daemon stores Ethos objects, the Nomos daemon its transformers and results, the Logos daemon its capsules. What each daemon's store schema looks like is design work for the daemon-architecture sitting.
