# 430 — Codec opt-in research: rkyv is the universal base; NOTA derive is opt-in per consumer

*Kind: Research + mechanism proposal · Topics: codec, nota-derive, rkyv, schema-emission, daemon-leanness, contract-crates, cargo-features, opt-in · 2026-05-30 · designer lane*

*Per psyche 2026-05-30 (after the @-sigil + newtype refinements landed): the
daemon should not carry the NOTA codec because (a) decoder cost — daemon must be
lean — and (b) the daemon should not even ACCEPT NOTA text on its wire (rkyv
only). Future binary-only clients face the same need. The CLI is the
"double" client — text in (NOTA), binary on the wire (rkyv). Research output:
where NOTA is read today, what mechanisms can split emission, recommended path.
Substrate: [[421-nota]] (codec lives in nota-next), schema layer
[[422-schema]], emission state [[427-schema-stack-as-implemented-now]].*

## 1. The ask, restated

- **rkyv is universal** — every client needs the binary representation to speak
  to the daemon at all; rkyv impls are always present on the wire types.
- **NOTA is opt-in** — only "double" clients (text + binary, e.g. the CLI) need
  `NotaDecode` / `NotaEncode`. Binary-only clients (the daemon, future
  binary-only consumers) carry neither the impls nor the `nota-next` dependency.
- **Same data types** across consumers — `Input`, `Output`, `Entry`, `Query`,
  etc. are byte-identical between daemon and CLI; what differs is the derive set
  on them. Wire compatibility comes from the shared rkyv layout.
- **Generation discipline** — schema-rust-next produces both forms from one
  `.asschema`. The build picks which the consumer needs.

## 2. Where NOTA is read in spirit-next today

```mermaid
flowchart LR
  user[user types `spirit (Observe …)`] -->|NOTA arg via env::args| cli["spirit-next CLI bin"]
  cli -->|FromStr → NotaDecode| input["Input (typed)"]
  input -->|rkyv::to_bytes| sock["unix socket"]
  sock -->|rkyv::from_bytes| daemon["spirit-next-daemon bin"]
  daemon -->|engine handle(Input)| reply["Output (typed)"]
  reply -->|rkyv::to_bytes| sock
  sock -->|rkyv::from_bytes| cli
  cli -->|Display → NotaEncode| stdout[stdout NOTA]

  systemd[systemd unit file] -->|NOTA config arg| daemon
  daemon -->|Configuration::from_single_argument| cfg["Configuration (typed)"]

  classDef nota fill:#fef3c7,stroke:#f59e0b
  classDef rkyv fill:#e0f2fe,stroke:#0284c7
  class cli,stdout,user,systemd nota
  class sock,input,reply rkyv
```

Files I verified:

| binary | NOTA codec usage | source |
| --- | --- | --- |
| `spirit-next` (CLI) | `source.parse::<Input>()` → `NotaDecode` via `FromStr`; `println!("{output}")` → `NotaEncode` via `Display` | `src/bin/spirit-next.rs` |
| `spirit-next-daemon` | None at wire; **but** `Configuration::from_single_argument` parses NOTA via `nota_next::{Block, Delimiter, Document}` for the systemd-passed config record | `src/bin/spirit-next-daemon.rs`, `src/config.rs:3` |
| `src/engine.rs` | imports schema-emitted `Input`, `Output`, `Entry`, etc. — uses them as Rust enums; never touches NOTA text | `src/engine.rs:4-7` |
| `src/transport.rs` | rkyv only on the socket | (grep clean) |

**So the daemon's current NOTA footprint = its systemd config parser, plus the
schema-emitted `NotaDecode`/`NotaEncode` impls on `Input`/`Output`/etc. that are
compiled in but never called.** Removing the latter is the main lean-down;
removing the former is a separate question (§6).

## 3. Schema-rust-next emits the derive line hardcoded

The relevant code path is `RustWriter::data_type_derive` (one method, two
return arms). Today every data-bearing emitted type gets the same derive set:

```rust
// schema-rust-next/src/lib.rs:234, 236
"#[derive(nota_next::NotaDecode, nota_next::NotaEncode, rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
 #[rkyv(derive(PartialEq, Eq, PartialOrd, Ord))]"
"#[derive(nota_next::NotaDecode, nota_next::NotaEncode, rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]"
```

The `nota_next::NotaDecode, nota_next::NotaEncode` pair is HARDCODED into both
arms. Also hardcoded in lines 363, 599-607 (plane envelope / ShortHeader /
OriginRoute), and in the emitted module's `use` line (line 313).

`nota-next` is therefore a non-optional dependency of every consumer of
schema-rust-next output today (including spirit-next, which has
`nota-next = { git = … }` directly in `[dependencies]`).

Single-emitter contract: schema-rust-next exposes `RustEmitter::default().emit_file(&asschema)`
(used by spirit-next's `build.rs`). To split the emission, the emitter needs a
configuration input.

## 4. The mechanisms — three options with tradeoffs

### Option A — Cargo feature on the emitted/contract crate (single crate, opt-in derive)

Schema-rust-next emits each derive line as a paired form:

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
#[cfg_attr(feature = "nota", derive(nota_next::NotaDecode, nota_next::NotaEncode))]
pub struct Entry { … }
```

Plus a feature-gated `use` of `nota_next::*` items where needed (FromStr/Display
impls go behind `#[cfg(feature = "nota")]`).

The emitted/contract crate's Cargo.toml carries:

```toml
[features]
default = []                            ; opt-in: NOT default, per psyche framing
                                        ; ("rkyv is universal, nota is opt-in")
nota = ["dep:nota-next"]

[dependencies]
rkyv = { version = "0.8", default-features = false, features = [...] }
nota-next = { git = "...", optional = true }
```

Consumers:

- **Daemon binary's crate**: `signal-spirit-next = { default-features = false }`
  — no nota, no nota-next compiled in.
- **CLI binary's crate**: `signal-spirit-next = { features = ["nota"] }` — gets
  the derives, depends on nota-next.

**Caveat — Cargo feature unification.** Features unify across a single
`cargo build`. If the daemon and CLI binaries live in the SAME crate (today's
spirit-next layout), they share one feature set and you cannot turn nota off
for the daemon while leaving it on for the CLI. **Fix is structural**: the
daemon binary and the CLI binary must live in SEPARATE crates so each chooses
its own dependency feature set.

| pros | cons |
| --- | --- |
| Standard Rust convention; single emitted crate; types are byte-identical because they're literally the same Rust types | Requires splitting spirit-next into ≥ 2 crates (daemon, CLI) so feature unification doesn't apply; build discipline (separate `cargo build -p` or Nix per-derivation) |
| One source of truth for the schema-emitted types | Mixing crates that enable + disable nota in one `cargo build` re-unifies — has to be enforced |

### Option B — Two crates: types + nota impls layered on top

`schema-emitted` = pure types + rkyv. `schema-emitted-nota` = a separate crate
that adds the NotaDecode / NotaEncode impls.

**Orphan rule blocks this**: NotaDecode / NotaEncode live in nota-next; the
types live in `schema-emitted`; the impl crate is neither. Rust forbids the
impls. You'd need a newtype wrapper (`pub struct EntryNota(pub Entry)`) which
defeats "same data types" — clients would have to convert.

| pros | cons |
| --- | --- |
| No feature flag — pure crate boundary | Orphan rule blocks the design; only ugly wrappers work |

Option B is **not viable** without uglier indirection. Discard.

### Option C — Per-target emission: schema-rust-next emits different .rs files for daemon vs CLI

Schema-rust-next CLI takes a NOTA argument specifying the target derives:

```nota
(EmitRust (Asschema [./spirit.asschema]) (Output [./out/types.rs]) (Codec [rkyv]))         ; daemon: rkyv only
(EmitRust (Asschema [./spirit.asschema]) (Output [./out/types-nota.rs]) (Codec [rkyv nota])) ; CLI: rkyv + nota
```

Build.rs in each consumer crate invokes the emitter with the appropriate codec
set. The daemon's emitted code is literally smaller; the CLI's is larger; no
`cfg_attr` shows up in the source.

**Wire-compatibility caveat**: daemon and CLI now have two SEPARATE Rust types
named `Input` (one in each crate's emitted module). Bytes from CLI's `rkyv::to_bytes(&cli::Input)`
deserialize as `daemon::Input` because the byte layout matches — but at the
Rust type level they are different types. Fine for separate binaries that only
share bytes; drift risk if schemas diverge across binary builds.

| pros | cons |
| --- | --- |
| No Cargo features; daemon's source is minimal | Two copies of the types compile (mostly fine for separate binaries); schema-version drift between binaries becomes possible if not managed |
| Emitter contract is explicit ("emit for THIS codec set") | More codegen complexity; requires per-binary build.rs |

### Option C' — Per-target emission, but into a SHARED contract crate

A hybrid: the contract crate has TWO modules — `rkyv_only` and `nota_added` —
both generated by schema-rust-next from the same `.asschema`. The `nota_added`
module re-exports `rkyv_only::*` and tacks on the NotaDecode/NotaEncode impls.

Same orphan-rule problem as Option B (you can't impl external trait on external
type from a different module if both are external to the module). So this
doesn't work either at the Rust language level.

## 5. Recommendation — **Option A + structural split**

The cleanest path is **Option A (Cargo feature on the contract crate) + a
structural split of spirit-next into separate binary crates**. Concretely:

```text
crate layout (proposed):
  signal-spirit-next        — the contract crate (schema-emitted Input/Output/Entry/…)
                              feature `nota` opt-in; default off
  spirit-next-engine        — shared library: Daemon/Configuration/SignalTransport
                              depends on signal-spirit-next (default-features=false)
                              IF the engine itself doesn't need nota text-parsing
  spirit-next-daemon        — daemon binary crate
                              depends on -engine, signal-spirit-next (no nota)
  spirit-next-cli           — CLI binary crate
                              depends on -engine, signal-spirit-next (with nota)
                              this is where Input::from_str (NotaDecode) lives
```

Why this is right:

1. **rkyv-base-nota-on-top is honored** at the crate level: the contract crate's
   default is rkyv only; consumers opt in to nota by enabling the feature.
2. **No feature-unification surprise**: daemon and CLI binaries are in different
   crates, so their feature choices don't merge under `cargo build -p X` or
   under Nix per-derivation.
3. **Same data types across consumers**: it's literally the same Rust crate;
   the NotaDecode/NotaEncode impls just compile away when the feature is off.
4. **Future binary-only clients** get the small-footprint contract crate for
   free.
5. **AGENTS.md component-triad alignment**: signal-spirit-next is already the
   intended working-signal contract crate; this just makes its default opt-out
   of NOTA.

Implementation in schema-rust-next:

- `RustEmitter` gains a `Codec` config (a `TypedEmit` knob, naming TBD): `{
  rkyv: true, nota: NotaFeatureMode }` where mode is one of `Always`,
  `FeatureGated("nota")`, `Never`. Default is `FeatureGated("nota")` (so the
  emitted source is feature-gated and downstream crates pick).
- The `data_type_derive` method (and lines 363, 599-607) split the derive
  attribute into two: an unconditional `#[derive(rkyv::*, …)]` and a
  `#[cfg_attr(feature = "nota", derive(nota_next::NotaDecode,
  nota_next::NotaEncode))]`.
- `use nota_next::{NotaDecode, NotaEncode, NotaSource, …}` items in the
  emitted module move under `#[cfg(feature = "nota")]` blocks.
- The emitter ALSO emits a recommended `Cargo.toml` snippet (or a sibling
  `Cargo.features.toml` for the contract crate) so the operator can paste in
  the feature stanza — single-source-of-truth.

The single-argument rule still holds: the emitter's input becomes a NOTA record
that specifies the codec mode, e.g. `(EmitRust (Asschema ./spirit.asschema)
(CodecMode FeatureGated))`.

## 6. Open question — daemon config: keep NOTA or drop it entirely?

The daemon currently parses NOTA for its systemd-passed Configuration record
(`Configuration::from_single_argument` uses `nota_next::{Block, Delimiter,
Document}`). That's a separate NOTA path from the schema-emitted wire types;
removing the wire-type derives doesn't remove this dependency.

Two paths to choose between:

- **(a) Keep daemon's config NOTA-readable.** Daemon binary still depends on
  nota-next, but ONLY for the small Configuration type. Other schema-emitted
  types (Input/Output/Entry/…) are nota-free. Net: nota-next still pulled in
  but only the parser, not the codec.
- **(b) Eliminate NOTA from daemon entirely.** Configuration comes in as rkyv
  bytes from a sidecar file the CriomOS-home module generates from a .nota
  source. Daemon has zero nota-next dependency. Net: fully lean, but adds a
  deploy-time pre-process step.

My read: **(a)** for the first slice — quick win, biggest wire-type derives
removed, simple to roll out. **(b)** as a follow-up if the operator confirms
the systemd-side rkyv-config pre-processing is worth it.

## 7. Operator implementation steps (one possible ordering)

1. **schema-rust-next** — add `EmitConfig` to the emitter, default
   `nota_mode: FeatureGated("nota")`. Refactor `data_type_derive` + the other
   inline derive strings (lines 363, 599-607, 622-637) to split the derive
   attribute and add `#[cfg_attr]`. Move FromStr/Display impls and the
   `nota_next::*` use-line under `#[cfg(feature = "nota")]`.
2. **The emitted contract crate's Cargo.toml** — operator updates spirit-next's
   schema-emitted module's Cargo (or moves it to a separate crate per the
   layout above) to declare:
   ```toml
   [features]
   nota = ["dep:nota-next"]
   [dependencies]
   nota-next = { git = "…", optional = true }
   ```
   No `default = ["nota"]` line — explicit opt-in.
3. **spirit-next split** — break the current single crate into the four crates
   above (`signal-spirit-next`, `-engine`, `-daemon`, `-cli`). Daemon depends
   on the contract crate with `default-features = false`; CLI depends with
   `features = ["nota"]`.
4. **Verify the daemon binary doesn't compile in nota-next**: under `cargo
   build -p spirit-next-daemon`, `cargo tree -p spirit-next-daemon` should
   show no `nota-next` in the dependency graph.
5. **(optional, deferred)** Daemon config moves to rkyv per §6(b) — the
   CriomOS-home module pre-generates the rkyv config file; daemon reads it via
   `rkyv::from_bytes`.

Tests / acceptance:

- A fixture schema lowers + emits with both `nota_mode: FeatureGated` and a
  hypothetical `nota_mode: Never`; the `Never` form has zero `nota_next::*`
  references in the emitted source.
- Daemon-only binary build under Nix produces no nota-next compiled artifact
  in the build closure (`nix path-info` introspection).
- Wire round-trip between CLI binary (nota enabled) and daemon binary (nota
  disabled) still works — confirming the rkyv layout is byte-identical between
  the two compilations.

## 8. The one-line summary

The emitter writes two derive attributes — an unconditional rkyv block and a
`#[cfg_attr(feature = "nota", …)]` block; the contract crate makes `nota` an
opt-in feature with `nota-next` an optional dependency; spirit-next splits so
the daemon and CLI binaries live in separate crates and choose independently —
daemon binary has zero `nota-next` in its closure, CLI binary has the full
text-parsing path. Wire stays rkyv-only.
