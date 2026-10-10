# Mutex in ethos-zero c2653d: probe evidence

Origin: all observations below are witnessed in this flow. Build: `git archive c2653d` copied to Prometheus /tmp/mutexprobe/src, `nix build .#default` gave ethos-zero 16.0.0 (/nix/store/zayj9a-ethos-zero-16.0.0). Fixtures lived in Prometheus /tmp/mutexprobe/f, outside the ethos-zero tree. Nothing pushed.

## (a) What the import syntax accepts

Source read (c2653d):
- `Source::try_from` (src/lib.rs:100-127) accepts any syn path without leading colon, so `std::sync` is a valid Source value.
- `Conceiving<Import>` (src/conception.rs:~397-415) requires the protos node to be `Headed` with `Separator::Colon`, and the head text becomes the Source.
- The protos lexer (protos 15b41da, src/core.rs ~422-447) ends the head run at the first `.`, `!` or `:`. A head therefore never contains `::`; `std::sync:Mutex` is head `std`, body `:sync:Mutex`, which is not an import form. The multi-segment Source is unreachable through text.
- `Imported` (conception.rs:~370-395) takes a bare name or `Ethos.Source` with both sides a single Name (a Rust identifier, `Name::try_from`, src/lib.rs:70), so `sync::Mutex` is refused as a name.

Trials (command for each: `ethos-zero 'Generate.{ f.ethos out }'`; file text is the Library line shown):

| fixture | text | result |
|---|---|---|
| a1 | `Library [ std::sync:Mutex ] [ Holder.{ Mutex<String> } ] [] []` | `Conceptual.{ [ 1 0 0 ] Expected.Import }` |
| a2 | `... [ std::sync:[ Mutex ] ] ...` | same Expected.Import |
| b1/b2 | `std.sync:Mutex`, `crate::sync:Mutex` | same Expected.Import |
| c2 | `«std::sync»:Mutex` | same Expected.Import |
| c1 | `std:sync:Mutex` | `[ 1 0 0 1 ] Expected.Import` |
| a3 | `std:Mutex` | Generated: `pub string_mutex: std::Mutex<String>` |
| a6 | `std:[ Mutex ]` | Generated, same field |
| a4 | `std:sync` with field `sync<String>` | Generated: `std::sync<String>` |
| c3 | `std:Mutex.sync` (rename Mutex to emitted name `sync`) | Generated: `std::sync<String>` |
| c5 | `std:[ Mutex.sync::Mutex ]` | `Name.«Mutex.sync::Mutex»` |
| a7/a8 | inline `std::sync:Mutex<String>`, `std::sync::Mutex<String>` | `Name.«std::sync:Mutex»` / `Name.«std::sync::Mutex»` |
| c4 | inline `«std::sync»:Mutex<String>` | `Expected.Reference` |
| a9 | inline `std:sync:Mutex<String>` | Generated, but emits `std::Mutex<String>` (inner `sync:` head is overwritten by the outer `std`, conception.rs:~430-436) |
| c6 | `std:[ Sync.Mutex ]` | `Undeclared.Mutex` (rename makes the declared name `Sync`) |

## (b) Does any accepted form reach std::sync::Mutex

No. Every accepted form emits one of `std::Mutex`, `std::sync`, or `std::sync<..>`; each is the Source path joined to one identifier. Reaching `std::sync::Mutex` needs either a head containing `::` (the lexer cannot produce one) or a two-segment emitted name (Name is one identifier). Sources and names are both single segments in practice.

## (c) Do the generated derives compile on a Mutex field

Scratch crate /tmp/mutexprobe/scratch (Cargo.toml as in tests/flow_contract.rs: rkyv 0.8 plus optional datom-codec 4dff16, lock copied). `cargo check` inside `nix develop` of the archived source.

V1, a3 output as emitted:
```
error[E0425]: cannot find type `Mutex` in crate `std`
 --> src/generated.rs:6:28
```
V2, a3 output hand-edited to `std::sync::Mutex<String>` (a stand-in; ethos cannot emit it), no features, 11 errors:
```
E0277 `std::sync::Mutex<String>: Archive` is not satisfied   x4 (Archive, Serialize, Deserialize, CheckBytes derives)
E0277 `std::sync::Mutex<String>: Clone` is not satisfied
E0369 binary operation `==` cannot be applied to type `std::sync::Mutex<String>`
E0277 `std::sync::Mutex<String>: Eq` is not satisfied
E0277 `std::sync::Mutex<String>: Hash` is not satisfied
```
Debug has no error (Mutex implements Debug). V3, same file with `--features datom`, 13 errors: the above plus
```
E0277 `std::sync::Mutex<std::string::String>: Composing` is not satisfied
E0599 the method `datomize` exists for reference `&std::sync::Mutex<String>`, but its trait bounds were not satisfied
```

## Conclusion
(a) imports take only a single-segment Source head, or a single-identifier rename; `::` is unreachable. (b) No form reaches `std::sync::Mutex`. (c) Even with the correct path the derive set fails on Archive/Serialize/Deserialize, Clone, PartialEq, Eq, Hash and the datom kinds; only Debug passes. Not tested: a hand-written wrapper type, which would need ethos to omit derives for a declaration (none exists; an alias carries no derive).
