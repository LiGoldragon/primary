# ethos-zero: a type with a special representation

Build host: `hostname` over ssh returned `prometheus` for every cargo and nix run. The scratch trees are on Prometheus in `/tmp`, with no remotes. Nothing was pushed, and nothing in Primary was committed.

## Bases

- **ethos-zero.** The base is 07714b0 plus item12-on-item5-ethos-zero.patch and item6-on-set-ethos-zero.patch. That tree is `/tmp/ez-i6` 77fc650. A fresh 07714b0 with both patches applied has an empty `git diff` against 77fc650. The scratch clone is `/tmp/ez-rep`:
  - branch `bare` is 31b346d;
  - branch `braced` is d781d4f, in the worktree `/tmp/ez-rep-braced`.
- **datom-codec.** Both variants are in `/tmp/dc-f3`:
  - braced is 776cf4b alone (branch `rep-braced`);
  - bare is d6191ff, which is 776cf4b plus item12-on-item5-datom-codec.patch, applied cleanly (branch `rep-bare`).
- **Pin.** In each variant, `Cargo.toml` and `Cargo.lock` pin datom-codec to `git+file:///tmp/dc-f3` at that variant's revision. The lock sources were checked.
- **Flake overrides.** Each flake check overrode protos with `path:/tmp/protos-i5` (the set's protos patch) and datom-codec with the variant's revision.

## The form

```
Library
[ datom:[ Represented ] ]
[ Ticket.Integer Digit.Integer ]
[]
[ Ticket.[ Represented.{ Representation.Vector<Digit> } ] ]
```

How each part reads:

- In the associations section, each element of a type's bracket is a borne trait.
  - `Name` alone is a trait reference, as before.
  - `Name.{ … }` is the trait together with the associated types it binds. Each binding is `Assoc.Type`, and the type's angle arguments sit beside it.
- The brace is read only as bindings. The associations bracket is never read as variants or as a struct.
- New model types in src/lib.rs:
  - `Association.traits` is now `Vec<Borne>`.
  - `Borne { bound: Reference, bindings: Vec<Binding> }`.
  - `Binding { name: Name, ty: Reference }`.
- Checking a borne trait:
  - A name that resolves to a declared type or an intrinsic type is refused with `Expected.Trait`. This holds with or without bindings.
  - Where the file itself declares the trait, a binding must name one of its associated types, or it is refused with `Undeclared`.
  - A binding named twice is refused with `Duplicate`.
  - A binding's type is checked as a type.
- The print reads back to the same File. The four fixtures that already had associations are unchanged.

## Emitted Rust (tests/generated/represented-types.rs, excerpt)

```rust
#[rustfmt::skip]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Represented))]
pub struct Ticket(pub i64);
#[rustfmt::skip]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
pub struct Digit(pub i64);
...
const _: () = {
    fn assert_ticket_represented<
        T: datom::Represented<Representation = std::vec::Vec<Digit>>,
    >() {}
    let _ = assert_ticket_represented::<Ticket>;
};
const _: () = {
    fn assert_digest_represented<T: datom::Represented<Representation = String>>() {}
    let _ = assert_digest_represented::<Digest>;
};
```

The derive swap applies to a type when two things hold:

- some association of the file names the type;
- that association bears a trait that resolves to `Represented`, imported or qualified from the source `datom` or `datom_codec`.

The generator emits no impl of `Represented`.

The fixture is `fixtures/represented-types.ethos`: `Ticket.Integer Digit.Integer Digest.Integer`, with the two associations shown above.

## Tests (tests/represented.rs, 8)

`represent` and `from_representation` are written by hand in the sibling module `representation`:

- A Ticket is its decimal Digits. A negative Ticket negates its first digit.
- A Digest is the 16 lowercase hex digits of its bits.

1. **`the_designed_form_is_accepted_and_reprints`.** The form above, word for word, reads and generates. The output contains:
   - `pub struct Ticket(pub i64);`
   - `T: datom::Represented<Representation = std::vec::Vec<Digit>>`
   - `let _ = assert_ticket_represented::<Ticket>;`

   Its print reads back to an equal File.
2. **`bindings_after_a_name_that_is_no_trait_are_refused_as_no_trait`.** Each case is refused with `Expected(Trait)`:

   | Case | Source excerpt | Path |
   |---|---|---|
   | A declared type | `Ticket.[ Digit.{ Representation.String } ]` | `[1 3 0 1 0 0]` |
   | A type named Represented, with an empty brace | `Represented.{ }` | `[1 3 0 1 0]` |
   | An intrinsic | `String.{ … }` | `[1 3 0 1 0 0]` |

   An extra test, `a_binding_names_an_associated_type_of_a_declared_trait_once`, uses a locally declared trait `Shown` with the associated type `Shape`:
   - `Shown.{ Shape.String }` generates `T: Shown<Shape = String>`.
   - `Form.String` is refused with `Undeclared("Form")` at `[1 3 0 1 0 1 0 0]`.
   - A second `Shape` is refused with `Duplicate("Shape")` at `[1 3 0 1 0 1 1 0]`.
3. **`a_representation_outside_the_trait_bounds_fails_to_compile`.** The association is `Representation.Opaque`, where `Opaque` is neither Datomizable nor Composing.
   - The generator accepts it and emits `T: datom::Represented<Representation = super::Opaque>`.
   - The test then compiles, with rustc, a crate made of the generated module plus a hand-written impl. It links against this test build's own datom-codec and rkyv rlibs, with `feature="datom"` set.
   - An impl with `Representation = String` fails with E0271 at `assert_ticket_represented`.
   - An impl with `Representation = Opaque` fails with E0277: "`Opaque: Composing` is not satisfied" and "`Opaque: Datomizable` …", required by the bound on `Represented::Representation`.
4. **`a_represented_type_derives_represented_in_place_of_the_datom_derives`.** In the committed golden:
   - The attributes of Ticket and Digest contain `derive(datom_codec::Represented)` and contain neither Datomizable nor Composing.
   - Digit keeps both datom derives and has no `Represented`.
5. **Round trips and the wrong impl.**
   - `a_ticket_is_written_as_its_digits_and_read_back`:
     - `Ticket(42)` prints exactly the text of its `Vec<Digit>`, and its datom equals the datom of `vec![Digit(4), Digit(2)]`.
     - The text reads back. 0, 7, 42, -42, `i64::MAX` and `i64::MIN` all round-trip.
     - `[]`, a leading zero, `12`, and a negative digit after the first are each refused.

     The observed text:

     | | braced | bare |
     |---|---|---|
     | `Ticket(42)` | `[ { 4 }\n  { 2 } ]` | `[ 4 2 ]` |

   - `a_hand_written_impl_with_another_representation_fails_to_compile`:
     - The control impl, `Vec<Digit>`, compiles.
     - An impl with `Representation = String` fails with E0271 "type mismatch resolving `<Ticket as Represented>::Representation == Vec<Digit>`", required by a bound in `assert_ticket_represented`.
6. **`a_digest_is_written_as_its_hex_string_and_read_back`.**
   - `Digest(42)` prints `000000000000002a` under both variants, and its datom equals that String's datom.
   - 0, 42, -1, `i64::MAX` and `i64::MIN` round-trip.
   - Too short, uppercase, non-hex and 17 digits are each refused.

Results by variant:

- **bare**: all 8 pass, under cargo and in the nix `test` check (`test result: ok. 8 passed`).
- **braced**: all 8 pass under `cargo test --test represented`. In nix, the run stops at an earlier test binary (see below), so the 8 did not run there.

## Checks

**bare**

- `cargo test`: all pass. lib 21, main 0, cli 17, ethos 33, flow_contract 1 (inner 2), freshness 4, generated 20, print 9, represented 8, signal_without_datom 2.
- `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings` and `cargo doc` with `-D warnings` are all clean.
- `nix flake check --keep-going`: "running 15 flake checks…", "all checks passed!", exit 0. The 8 check attributes are build, test, fmt, clippy, doc, dependency-ethos, no-free-functions and no-inherent-methods. `nix flake metadata` shows datom-codec at d6191ff and protos at `path:/tmp/protos-i5`.

**braced**

- `cargo test --no-fail-fast`:
  - pass: lib 21, ethos 33, flow_contract 1 (inner 2), freshness 4, print 9, represented 8, signal_without_datom 2;
  - fail: cli 9 pass / 8 fail; generated 19 pass / 1 fail (`a_new_type_has_its_value_size_and_reads_as_its_value_in_datom`, "`{ abc123 }`" against "`abc123`").
- **These 9 failures are not caused by Represented.** The base 77fc650, with only the pin moved to 776cf4b, fails the same 8 cli tests and the same generated test. The set's ethos-zero expects a newtype to print bare, which needs the set's datom-codec hunk.
- `nix flake check --keep-going`: "running 15 flake checks…", exit 1. Each check built alone gives:
  - pass: build, clippy, doc, fmt, no-free-functions, no-inherent-methods;
  - fail: test (cli fails first, so cargo stops there);
  - fail: dependency-ethos. The ethos-zero package derivation it consumes runs the same tests and fails with exit 101.

## Files touched

12 files changed, +810 / -29, against 77fc650. The two variants differ in 3 files: Cargo.toml, Cargo.lock and tests/represented.rs. The only difference in tests/represented.rs is the `TICKET_TEXT` line.

| Area | Files |
|---|---|
| src | lib.rs (`Borne`, `Binding`), conception.rs, checking.rs, generation.rs, protosization.rs |
| fixtures | represented-types.ethos (new) |
| tests | generated/represented-types.rs (new golden), represented.rs (new), freshness.rs (fixture count 18 → 19), print.rs (source count 20 → 21) |
| root | Cargo.toml (`[[test]] represented` and the datom-codec pin), Cargo.lock |

Patches, each a `git diff 77fc650 <branch>`:

- `ethos-represented-bare.patch`
- `ethos-represented-braced.patch`

## What did not hold, or holds with a condition

- **Conception cannot tell traits apart.** Conception does not know which names are traits. An import carries no role, so it reads every `Name.{ … }` in the associations section as a borne trait. Checking then refuses names declared as types. A name imported as a type (for example `datom:[ Digest ]`) is not refused, because an import carries no role.
- **The assertion does not check the trait's bounds.** rustc accepts `T: Represented<Representation = Opaque>` without checking Opaque against `Datomizable + Composing`. Test (3) fails at compile time because no impl can satisfy it: a valid impl fails the generated assertion with E0271, and an Opaque impl fails the trait's own bound with E0277 in the impl. The generator reads nothing about an imported trait's bounds.
- **`datom` is not a Rust crate.** The source `datom` is emitted as the path `datom::Represented`. That path compiles only where `datom` names datom-codec; the tests write `extern crate datom_codec as datom;`. The derive is always written `datom_codec::Represented`, like the other datom derives.
- **The derive is gated, the assertion is not.** The derive sits behind the `datom` feature, but the assertion does not. Without that feature, the hand-written impl still satisfies the assertion, since it needs datom-codec anyway.
- **Recognition is by name.** The derive swap is keyed on a borne trait named `Represented` from the source `datom` or `datom_codec`. Nothing else ties the generator to datom-codec's trait.
- **An empty brace is lost on reprint.** `Name.{ }` is read as a borne trait with no bindings, and it reprints as `Name`.
- **An existing error path changed.** The old plain-reference check placed an association's trait errors at `[… 1 0 at]`. The extra `0` came from passing section 0 to `refer_each`. Errors now sit at the element's Protos path `[… 1 at]`. No existing test pinned the old path.
- **Plain bornes now give a different error.** A plain borne name that resolves to a type is now refused with `Expected.Trait` instead of `Role`. No existing test pinned `Role`.
- **New names.** `Borne` and `Binding` are names this candidate introduces.
- **braced on this base.** The braced variant does not pass the set's own ethos-zero tests. Represented does not cause these failures; see the braced checks.

Provenance receipt: unavailable.
