# Effective-library equivalence audit

Audited 2026-07-17 by `NewEngineCompletion` / `CompleteEffectiveLibrary` against the public `language-engine-witness` main revision `b938d7400da4742c3873e9203a92c3c628f3bcc4` and the pinned `schema-rust` revision `79a9e5c98a5db226d88fb9bb1934f95e4d6090c9`.

## Verdict

The current shipped-daemon witness is a real and passing process-level witness for the narrow declaration subset. It does **not** meet the accepted complete-effective-library equivalence threshold. The blocker is source-visible, not a flaky test result: the witness deliberately selects twelve declarations from the reference output, while `core-logos` deliberately models only four declaration kinds and no Rust body vocabulary.

Do not close `primary-56d1.35` from the existing green check. It proves the narrow bridge only.

## Fresh commands and results

| Command | Result | Evidence |
| --- | --- | --- |
| `jj git clone --branch main https://github.com/LiGoldragon/language-engine-witness.git /home/li/wt/github.com/LiGoldragon/language-engine-witness/complete-effective-library` | passed | Fresh public clone placed `main` at `b938d7400da4742c3873e9203a92c3c628f3bcc4`. |
| `nix build .#checks.x86_64-linux.test --no-link` | passed | The Nix test ran `one_document_pushes_through_four_processes_and_recovers`; its process-level body completed in 12.62 seconds. |
| `nix flake check --no-write-lock-file` | passed | Evaluated package plus build, test, doc, fmt, and clippy derivations for x86_64-linux. The command reported that incompatible non-Linux systems were omitted. |
| `jj git clone --branch main https://github.com/LiGoldragon/schema-rust.git /home/li/wt/github.com/LiGoldragon/schema-rust/complete-effective-library` followed by `jj new 79a9e5c98a5db226d88fb9bb1934f95e4d6090c9` | passed | Fresh isolated checkout at the witness's pinned legacy-reference revision. |
| `cargo run --example generate_spirit_fixture --locked` | passed | Live `SchemaEngine` then `RustEmitter` generation of `spirit-min.schema` emitted 1,023 lines / 26,267 bytes. |

The Nix test log shows the test launched the Nix-built `sema-storage`, `schema-engine`, `nomos-engine`, and `logos-engine` executables rather than substitutes.

## Gate status

| Equivalence gate | Status | Concrete evidence |
| --- | --- | --- |
| Real NOTA -> Schema -> Nomos -> Logos -> TextualRust process pipeline | partial | `tests/e2e.rs` launches the four shipped binaries, frames the handshake and requests through `signal_frame`, subscribes at Logos before ingress, and receives a pushed projection event. The live reference is generated through pinned `schema-language` and `schema-rust`. Its final equality target is filtered, so this is not full-library evidence. |
| Shared signal-frame and event-driven progression | satisfied for the witnessed path | The test uses `signal_sema_storage::Wire` for the handshake, all request frames, and replies. It rejects protocol `99.0.0`; `nomos-engine` and `logos-engine` public-main revisions are respectively `458104b89a407b30715f264f023fc045109443cd` and `43d8f279938e5c52ca1032a3467947095695cd1d`, both labelled as framed upstream supervision without polling. Source inspection found only two `tokio::time::timeout` calls, each an event deadline; there is no sleep, interval, or retry loop. |
| Four-process restart and durable push recovery | satisfied for the witnessed path | The test terminates and respawns all four binaries against the same Sema database, fetches the stored Logos document and all four document roots, subscribes again, reinserts TypeSchema, and receives a resumed Logos event. |
| Fresh legacy reference | satisfied | The fresh `schema-rust` command above generated the reference at the exact revision named by the witness. The E2E source independently calls `SchemaEngine::lower_source` followed by `RustEmitter::emit_code_from_true_schema`. |
| Truthful locked generated/reference crates | not satisfied | `write_crate` writes the same locked manifest for generated and reference crates, but that manifest contains only `rkyv`, `signal-frame`, and optional `nota`. It cannot truthfully cover the full reference output's runtime traits, route enums, codecs, helpers, and module surface because the E2E filters those constructs away. |
| Supported feature matrix | not satisfied | The passing test runs `default`, `--no-default-features`, and `--all-features`. Its generated manifest defines `nota-text`, but the required NOTA-only command `cargo test --locked --features nota-text` is absent. |
| Complete public, wire, runtime, and helper behavior | not satisfied | The generated test imports only `Topic`, `Topics`, `Description`, `Summary`, `RecordIdentifier`, `Entry`, `Query`, `RecordSet`, `Kind`, `Magnitude`, `Input`, and `Output`. It checks archive bounds and a few fields/enum values. No full wire codec, route, runtime wrapper, hook, trait, method, or helper behavior is shared between independently compiled complete libraries. |
| Complete CoreLogos algebra | not satisfied | `core-logos/src/item.rs` has only `Newtype`, `Struct`, `Enumeration`, and `Alias`. Its own architecture says `TraitDefinition`, `ImplBlock`, and `FreeMethod` are deliberately out of scope because it has no body vocabulary. It has no typed module, const/static, function/method, associated item, statement, or expression data. Therefore TextualRust cannot faithfully transcribe the remaining effective Rust library from Core data. |
| Exact public revisions and dependency closure | partial | The witness lock pins the expected public revisions for `core-logos` `17cbd7596df203e0717fe079b7688cc60ec05e4b`, `core-nomos` `d2f705808ed555cae0ead6a9181970ef1fdc0430`, `textual-rust` `571b76f5eedd47c5cdedbd1b00cbe5bb7bef3c7d`, `schema-language` `4270fbdad5318518291829c2f08b22090e833182`, `schema-rust` `79a9e5c98a5db226d88fb9bb1934f95e4d6090c9`, `nota` `7d0651a0e098efea5fe2578cb06d88e009d40ff0`, and `signal-sema-storage` `bd6cd6c4f2f020ad04427fc8ca86ca22d9cf4e6c`. The lock also retains branch-qualified package source URLs for the patched `kameo` and `signal-frame` source identities, although each resolved entry ends in a commit hash. A complete-library closure audit must be repeated after the omitted constructs land. |

## The concrete full-library boundary

The freshly generated reference contains 39 public type/trait heads and these additional construct counts:

- 3 modules;
- 46 `impl` blocks;
- 89 functions and methods;
- 4 public traits;
- 1 constant/static declaration;
- 9 aliases;
- 16 structs;
- 10 enums.

The E2E function `expected_generated_rust` instead retains only these twelve declaration names:

```text
Topic Topics Description Summary RecordIdentifier Entry
Query RecordSet Kind Magnitude Input Output
```

Reproducing the filter over the freshly generated reference yields 142 lines / 3,473 bytes, only 13.22 percent of the 26,267-byte reference. The green equality therefore proves that the daemon result equals this selected declaration-only projection; it cannot prove equality of the effective library.

## Remaining implementation work

1. Complete `core-logos` with stringless typed data for modules, const/static items, functions and methods, traits and implementations, associated items, paths, attributes, visibility, generics, where clauses, route/conversion/codecs/errors/aliases, runtime wrappers/hooks, and explicit statements and expressions. Do not add raw Rust strings or opaque token blobs.
2. Extend Nomos lowering and TextualRust transcription for every added data variant. Maintain Core identity over canonical archive bytes with NameTables and formatting excluded.
3. Replace the E2E declaration-name filter with the complete daemon-produced output. Compile generated and freshly generated legacy reference crates with identical truthful locked manifests.
4. Run exactly this feature matrix for both crates: default, `--no-default-features`, `--features nota-text`, and `--all-features` (plus any newly declared supported feature combinations).
5. Add shared public API compile witnesses and behavior tests for every full-output category, especially codecs, route enums, conversions, runtime wrappers, hooks, error formatting, aliases, traits, and methods.
6. Re-run the live four-process restart/recovery witness after the full surface is in the daemon path, then re-audit every resolved dependency as a public exact revision.

## Authority and safety

No production Spirit state was activated or mutated. The required work is implementation, not a decision on any reserved authority question: it does not require deciding permanent allocation authority, lineage/merge semantics, String-versus-Text spelling, or detailed future document-kind design.
