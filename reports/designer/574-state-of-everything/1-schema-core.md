# Schema/NOTA engine core

> A genuinely clean, well-disciplined cluster: zero free-function violations and zero fake-NOTA across all four repos, the terse-grammar migration is fully landed in the live schemas (no OLD verbose (Name Name) forms remain), and every type rides the real nota-next codec. The one real cross-cutting risk is dependency skew — schema-next/nota-config pin nota-next f0e435a6 while schema-rust-next pins ae5c25cd (4 commits apart, both below the d8862b6 string-encoding bump); no consumer actually pins d8862b6, so the prompt's d8862b6-consumer flag is empty, but the staggered pins are the live encoding-mismatch hazard.

## Cluster: Schema/NOTA engine core

**Verdict.** A genuinely clean, well-disciplined cluster. Zero free-function violations and zero fake-NOTA across all four repos; the terse-grammar migration is fully landed in the live schemas (no OLD `(Name Name)` verbose forms remain anywhere); every type rides the real `nota-next` codec. The one real cross-cutting risk is **dependency skew**: the schema engine and its Rust emitter pin different `nota-next` revisions. The prompt's "flag any consumer on d8862b6" yields an **empty list** — no consumer pins d8862b6; d8862b6 is `nota-next`'s own HEAD (the string-encoding bump).

### Per-repo summary

| Repo | Prod LOC | Test LOC | Gen LOC | Daemon shape | Intent fit | nota-next pin (vs HEAD d8862b6) | free-fn | fake-NOTA |
|---|---|---|---|---|---|---|---|---|
| schema-next | 8,273 | 4,194 | 0 | library | aligned | f0e435a6 — **8 behind** | 0 | 0 |
| schema-rust-next | 8,805 | 13,457 | 0 (10.5k golden fixtures in tests/) | contract-only emitter (emits 1 kameo `EngineActor`) | aligned | ae5c25cd — **4 behind** (deliberate) | 0 | 0 |
| nota-next | 4,253 (3,155 src + 1,098 derive) | 1,804 | 0 | library + proc-macro | aligned | — (is HEAD d8862b6) | 0 | 0 |
| nota-config | 279 | 229 | 0 | library-only | mixed (stale .concept.schema) | f0e435a6 — **8 behind** | 0 | 0 |

LOC verified: all four repos keep tests exclusively in `tests/` dirs — **zero inline `#[cfg(test)]` modules**, so production LOC is the full `src`(+`derive`) tree. Baselines refined slightly down (schema-next 8290→8273, schema-rust-next 8859→8805, nota-next 4395→4253). No `src/schema/*.rs` generated dirs exist in any repo; the 10,584 LOC of `*.generated.rs` in schema-rust-next are **test golden fixtures**, not production.

### Dependency state (the one real risk)

`flake.lock` carries **no foundation-crate pins** in any repo — only Nix tooling (crane/fenix/nixpkgs/rust-analyzer). The real pins live only in `Cargo.lock`, so there is no Cargo-vs-flake disagreement on foundation crates.

- `nota-next` HEAD `d8862b6` is the **encoding bump**: 3 commits above `ae5c25cd` change the NOTA string encode output (render bare-safe strings as atoms; escape pipe close markers; render bracket strings with lossless pipe fences).
- `schema-rust-next` pins `nota-next` `ae5c25cd` (the commit just below the bump) — **deliberate isolation, correct**. It also pins `schema-next` `c8ebb399` (HEAD), `signal-frame` `166bda84` (HEAD), and `triad-runtime` `bedbb1db` (**3 behind** HEAD `6ea8316` — missing the `DaemonConfiguration`→`BindingSurface` rename + kameo re-export its own INTENT already describes).
- `schema-next` and `nota-config` pin `nota-next` `f0e435a6` — **4 commits older than `ae5c25cd`**, 8 behind HEAD.

**The hazard:** the emitter (`schema-rust-next` @ `ae5c25cd`) derives `nota-next` codecs against a *newer* rev than the schema engine (`schema-next` @ `f0e435a6`) parses `.schema` with. Both still sit below the bare-safe-atom change, so they are mutually consistent **today**, but the encoding mismatch becomes live the moment `schema-rust-next` advances to `d8862b6` while `schema-next` stays back. Re-align both to one `nota-next` rev before adopting the bump.

### Schema / grammar state

The terse grammar is the live source of truth and the migration is **complete** in canonical files:

- `schema-next/schemas/{core,root,spirit-min,builtin-macros}.schema` use bare distinct newtypes (`MacroName String`), direct variants (`(Plain Name)`, `(Capture MacroCaptureName)`), and `*` markers. **Zero** old `(Name Name)` verbose self-references.
- `schema-rust-next/tests/fixtures/collections.schema` carries the newest forms: `Digest Bytes` (lm84 hash-id) and `Fingerprint (Bytes 4)` (yp29 fixed-size). `runner-triad.schema` uses direct `(Continue NexusWork)` (52ro, not old `(Continue Continue)`).
- `.concept` vs split-triad duality resolves cleanly: the **only** `.concept.schema` in the entire cluster is the stale `nota-config/schema/nota-config.concept.schema`; everything else is split `nexus.schema` / `sema.schema` / `signal.schema` ports.

### Free-function violations

**None — 0 across the cluster.** The only module-level `fn`s are the three `#[proc_macro_derive]` entry points in `nota-next/derive/src/lib.rs` (lines 12, 18, 24: `derive_nota_decode`, `derive_nota_encode`, `derive_structural_macro_node`). The Rust language *forces* proc-macro derive fns to be free functions at crate root, and each immediately delegates to a data-bearing type (`CodecDerive::new(input).expand_*()` / `StructuralDerive::new(input).expand()`). These are the sanctioned exception, not violations.

### Fake-NOTA violations

**None — 0 across the cluster.** Every `to_nota` falls into a legitimate bucket:

- `schema-next/src/schema.rs` (e.g. `Name` line 65, `SymbolPath` line 188, `TypeReference` line 869 emitting `(SymbolPath ...)`, `(Map ...)`, `(FixedBytes N)`) are **real `impl nota_next::NotaEncode for X`** that delegate to children's `.to_nota()`; decode goes through `NotaBlock`/`NotaSource`. Hand-written codec impls (rather than `#[derive]`) are correct here — these are the engine's own hand-authored semantic nouns implementing the real trait.
- `schema-next/src/declarative.rs:74,111` `to_nota_source` are thin aliases: `from_nota_source` → `NotaSource::new(...).parse()`, `to_nota_source` → `NotaEncode::to_nota(self)`.
- `schema-rust-next/src/lib.rs` `to_nota`/`to_nota_method` (lines 1583–3922) are **emitted `quote!{}` source**, including the `Bytes`/`FixedBytes` hex codec at `src/lib.rs:3780-3922` whose generated `to_nota` builds hex then delegates `nota_next::NotaEncode::to_nota(&hex)` — the delegation pattern the cluster note explicitly calls CORRECT.
- `nota-next/src/codec.rs` string-building is inside the encoder itself (sanctioned). `nota-config` does zero string-building and decodes through `nota_next::NotaSource`.

### Worth the psyche's attention

1. **`nota-config/schema/nota-config.concept.schema` is stale cruft** — an OLD-form, never-finished concept artifact (May 24) that directly contradicts the repo's own INTENT ("library-only; config records remain hand-declared; orthogonal to the schema engine"). Delete it; it is the last `.concept.schema` in the cluster.
2. **`schema-rust-next` ↔ `schema-next` pin different `nota-next` revs** (`ae5c25cd` vs `f0e435a6`, 4 apart). Align them onto one rev before the d8862b6 string bump is adopted, or the emitter's derived codecs and the engine's parser will project NOTA strings differently.
3. **`schema-rust-next`'s `triad-runtime` pin (`bedbb1db`) is 3 commits behind HEAD** and the missing commits (`BindingSurface` rename, kameo re-export, `upgrade_socket_path`) are already described as present in its INTENT.md — pin and intent have drifted.
4. **The d8862b6 encoding bump is staged but unconsumed** — no cluster consumer has adopted it yet; this is the deliberate isolation working as intended, but it means the bump's value isn't realized until the staggered pins are advanced together.
