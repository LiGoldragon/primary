# Ethos: rulings

Summary of the proposals in `1-ethos.md`:

- 1 `Vision/ethos.md` What Ethos is: ethos as the typed spec every Nexus is programmed from, compiled to Rust.
- 2 `Vision/ethos.md` Roots: four roots, Library, Signal, Operation, Memory, with their sections.
- 3 `Vision/sema.md` What sema is: Sema stores what the Memory root declares.
- 4 `Vision/ethos.md` new Everything is a type: no key-value, positions are types, open-ended variants are names.
- 5 `Vision/ethos.md` new An ethos edit is the data migration: the Memory edit is the upgrade; versions outside the file.
- 6, 7 `Vision/ethos.md` Spacing becomes Layout (vertical, about three deep, closer on the last line); new Comments.
- 8, 11 `ethos-zero/README.md`: comments printed where written; inline payload named after its variant; one-position struct refused.
- 9 `Vision/ethos.md` Inline types: a variant's inline payload takes the variant's own name.
- 10 `Vision/ethos.md` new One position is a new type: `Name.Type`, never `Name.{ T }`.
- 12 `Vision/ethos.md` Kind: kind meant when trait is said; a capability takes kinds, never types.
- 13 `Vision/ethos.md` Horizon: bodies by hand today; what the whole program in ethos needs.
- 14 `signal-harness/Cargo.toml` and 20 others: repin ethos-zero from 9.0.0 (`b232d35e`) to the ruled release.

## Rulings

1. Roots.
   (a) Three roots, Library, Signal, Sema: `Vision/ethos.md` Roots; 2026-09-10, fe34eb.
   (b) Four roots, Library, Signal, Operation, Memory: 2026-10-02, 91ea9f; ethos-zero since 15.0.0.
2. Layout.
   (a) One declaration per line, delimiters spaced, as the protos print: `Vision/ethos.md` Spacing, as of 2026-09-11.
   (b) Vertical expansion about three deep, the closing delimiter ending the last line: 2026-10-02, 91ea9f.
3. The name of a variant's inline payload.
   (a) Derived with an underscore, `Unwritable_Data`, so it never collides: 2026-09-09, 564f55; ethos-zero 16.0.0.
   (b) The variant's own name, shared by variant and struct: 2026-09-30, 7328f4.
4. One-field structs.
   (a) Refused, written as a new type: 2026-09-08, 8e9e77.
   (b) Accepted, as ethos-zero does since 2026-09-10 (`9e2e327`) and 42 files use.
5. What `Name.String` declares.
   (a) A Rust alias, `pub type Name = String`, bearing no derive: `Vision/ethos.md`; ethos-zero since 2026-09-10 (`79e51c0`).
   (b) A new type of its own: 2026-09-08, 8e9e77.
6. Comments.
   (a) A comment on every section and next-layer line, kept: 2026-10-03, edf227.
   (b) Comments read and dropped from the print: ethos-zero README, 16.0.0, 2026-10-02.
7. Versions.
   (a) No version in an ethos file: 2026-09-09, 564f55.
   (b) Ethos versions, each with its upgrade: 2026-09-29, c64ee3; 2026-10-02, 91ea9f.
8. Trait or kind.
   (a) Trait set aside as acoustically ambiguous: 2026-08-26, f426777b.
   (b) Kind meant when trait is said, trait still said for Rust: 2026-09-11, fe34eb; 2026-09-24, 26c50c.
9. Bodies by hand, or the whole program in ethos.
   (a) Ethos types and kinds, implementations written by hand: 2026-10-04, 5ed94b.
   (b) The whole program in ethos within a few months: 2026-09-25, e51411; 2026-09-29, c64ee3.
