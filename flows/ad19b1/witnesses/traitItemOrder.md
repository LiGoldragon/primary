# Rust trait items: declaration order and mutual reference

Witnessed 2026-09-04 by a write-trivial probe of flow ad19b1: six
programs compiled one by one with rustc 1.96.0 (ac68faa20
2026-05-25), `rustc --edition 2021 --crate-type bin`, in the flow's
scratchpad. Relayed to the main flow with full sources and output.

| case | trait body | result |
|---|---|---|
| 1 | `const DEFAULT: Self::Item;` before `type Item;` | compiles |
| 2 | `type Iter: Iterator<Item = Self::Item>;` before `type Item;` | compiles |
| 3 | `const A: usize = Self::B + 1;` before `const B: usize;` | compiles; `<S as T>::A` prints 2 with `B = 1` |
| 4 | `fn get(&self) -> Self::Item;` before `type Item;` | compiles |
| 5 | `const A: usize = Self::B; const B: usize = Self::A;` | refused: E0391 "cycle detected when simplifying constant for the type system `T::A`" |
| 6 | case 1 in the natural order, `type Item;` first | compiles, identically |

What this witnesses: inside a Rust trait, every item is in scope over
the whole body; associated constants, associated types and methods
may refer to items declared after them; only a cycle is refused. The
declaration order of trait items carries no meaning.
