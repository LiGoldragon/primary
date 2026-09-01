# Const traits in Rust — verified state, 2026-09-01

Relayed from primary sources via research subflow (nightly 1.100.0-nightly 2026-08-31 docs, RFC 3762, tracking issue #143874, libcore master). Nothing here is witnessed on this machine; no nightly toolchain is installed locally.

## Status
- Nightly-only, feature gate `const_trait_impl`. Nothing stabilized. RFC 3762 ("Make trait methods callable in const contexts") is still an open, unmerged PR; tracking issue #143874 (~1/61 items). A 2026 blog claim of stabilization is wrong.

## Current spellings (nightly)
- Trait declaration: `const trait Foo { … }` (`#[const_trait]` removed).
- Impl: libcore master writes `const impl Foo for T`; the Unstable Book still writes `impl const Foo for T` — keyword order is an unsettled bikeshed, `const impl` currently winning in-tree (PR #139858, #148434).
- Bounds: maybe-const `T: [const] Foo` (replaced `~const`); always-const `T: const Foo` (required for calls in const/static initializers).

## Semantics
- A const trait impl is a checked promise: every method body must pass const-fn checking. It stays a fully ordinary runtime impl; const evaluation happens only where a const context demands it (const items, const blocks, array lengths, const generics). A license, not a mode switch.
- Generic const construction and chained generic const calls work: RFC example `const fn default<T: [const] Default>() -> T { T::default() }`; live in libcore: `const impl<T, U> Into<U> for T where U: [const] From<T>`.

## Const-world restrictions that bite
- Heap allocation: separate unstable gate `const_heap` (#79597; `const_allocate`, `const_make_global` to escape into a final value). Stable: only `Vec::new` etc. Design consequence: const-path data is allocation-free — associated consts, inline arrays, borrowed slices.
- `for` loops/iterators: `Iterator` is not a const trait; write `while` loops over slices in const fns.
- Panics: `panic!("literal")` and `assert!(cond)` are const-legal; formatted `panic!("{}", x)` is not (`const_format_args` unresolved; const_panic crate exists). A coherence fault's message must be literal or preassembled.
- `dyn` method calls in const: out of scope for the RFC. Generic drops need `T: [const] Destruct`.

## Consequence for the layer machinery
The compile-time coherence check is expressible as const trait capabilities on nightly: forms data in each kind's associated constant (allocation-free), the walk a while-loop over the enum's members' constants inside a const evaluation, the build failing by const panic (literal message). Bringing a nightly toolchain into the Nix setup is the prerequisite to witness it.

## Sources
- https://doc.rust-lang.org/nightly/unstable-book/language-features/const-trait-impl.html
- https://github.com/rust-lang/rust/issues/143874 · https://github.com/rust-lang/rfcs/pull/3762
- https://github.com/rust-lang/rust/pull/139858 · https://github.com/rust-lang/rust/pull/148434
- https://rustc-dev-guide.rust-lang.org/effects.html
- https://doc.rust-lang.org/nightly/src/core/convert/mod.rs.html (const impl Into via [const] From)
- https://github.com/rust-lang/rust/issues/79597 (const_heap) · #92476 (const_iter) · #133214 (const_destruct) · #140585 / #108595 (const formatted panics)
- https://rust-lang.github.io/rust-project-goals/2026/const-traits.html
- Flow 995a164e; witness witnesses/rustConstEvaluation.md (stable-side probes on this machine)
