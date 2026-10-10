# datomic-situated: Datomic for Situated<F> and impl_datomic_box!

Subflow of 6329f1.

## What was done

On datomic main at `a27f9b8e`, `protos::Situated<F>` had no `Corporal<Datom>` or
`Datomic` implementation. Orchestrate 0.28.0 had to declare its own `Situated` in
client ethos because the generic impl was missing.

### impl<F: Datomic> Corporal<Datom> for Situated<F>

Added to `src/lib.rs` in the datomic crate. `Situated<F>(pub Option<Extent>, pub F)`
is defined in protos; the impl lives in datomic under the orphan rule (Datom is local).

Datom encoding — `{ Option<Extent> <F's datom> }`:
- `Situated(Some(Extent(5, 13)), f)` → `{ Some.{ 5 13 } <f's datom> }`
- `Situated(None, f)` → `{ None <f's datom> }`

This matches orchestrate's stderr exactly:
`Unreadable.{ Some.{ 5 13 } Structural.{ { 5 13 } Unclosed.Braced } }`
where `{ Some.{ 5 13 } Structural.{…} }` is the Situated datom.

### impl_datomic_box! macro

Rust's orphan rule prevents `impl<T: Datomic> Corporal<Datom> for Box<T>` because
`Corporal` is a foreign trait from protos, and with `Box` being `#[fundamental]` the
check looks through Box to T — an uncovered type parameter that appears before the
local type `Datom` in the trait-parameter ordering (E0210).

`impl_datomic_box!(TheirType)` is exported as a `#[macro_export]` macro that generates:
- `impl protos::Corporal<datomic::Datom> for Box<TheirType>` — transparent delegation
- `impl datomic::Datomic for Box<TheirType>` — transparent delegation

The orphan rule is satisfied because the impl is generated in the crate that defines
`TheirType`. Claude-answers can replace its manual `impl Corporal<Datom> for Box<Query>`
with `datomic::impl_datomic_box!(Query)`.

### datomic.ethos

Version bumped `{0 8 0}` → `{0 9 0}`. `Situated<Datomic>.[ Datomic ]` added to the
association list. `Box<Datomic>.[ Datomic ]` was not added (it is macro-generated, not
a blanket impl; the ethos describes blanket associations only).

### Version

`0.8.0` → `0.9.0` (new Datomic impls; backward-compatible feature addition).

### Tests

Three new tests:
- `situated_fault_datomizes_as_struct` — verifies the exact datom text
  `{ Some.{ 5 13 } Structural.{ { 5 13 } Unclosed.Braced } }` and round-trips via
  incorporate.
- `situated_fault_none_extent_round_trips` — verifies the None variant
  `{ None Structural.{…} }` and round-trips.
- `box_query_recursive_round_trips` — defines a local recursive `Query` enum, applies
  `impl_datomic_box!(Query)`, and round-trips `Nested.Nested.Literal.7`.

## Witnessed results

```
cargo test: 37 passed (34 existing + 3 new)
cargo clippy --all-targets -- -D warnings: clean
cargo fmt --check: clean
nix flake check -L --builders 'ssh://prometheus': all checks passed
```

## Outcome

datomic main is now at `e4430bfe`. Orchestrate can import `datomic:[ Situated Fault ]`
and use `Situated<Fault>` directly. The `api-deviations.md` entry "datomic: no Datomic
for Box<T>" is partially resolved: the macro replaces the manual impls in consumers.

## Sources

- flows/6329f1/reports/keep-going-ethos-orchestrate.md (starting point; described the gap)
- flows/6329f1/reports/api-deviations.md (Box<T> deviation entry; orphan rule analysis)
- flows/6329f1/log.md (Design section; Situated definition)
- protos rev 56c683ec (Situated<F> struct; Corporal trait definition)
- datomic main a27f9b8e (starting state)
