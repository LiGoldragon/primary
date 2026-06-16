# 659/4 — Synthesis: the language, its constraints, and the generate-not-hand-wire goal

The agglomeration. One thesis, one delimiter vocabulary, one pipeline, one boundary — woven
from the constraint catalog (`1`), the settled design (`2`), and the e2e goals (`3`).

## The thesis

A programming language **is** a set of structural macros kept as data (`7c71`); everything,
the macro most of all, is a serializable data object read by one tiny generic interpreter,
round-tripping through NOTA text and rkyv bytes (`4itr`). The schema is a NOTA dialect
(`6grf`), not a separate language lowered into NOTA; reading it is type-directed structural
matching by shape, not data-tag or string dispatch (`xai7`/`kchq`/`v0n6`); there is no
separate IR — resolution is methods on schema-in-rust, the emitter only projects to Rust
(`6cfr`/`813q`); and the compiler is build-time only — shipped binaries carry strict rkyv
contracts (`9rjq`), with the compiler's own definition increasingly data (`vpbx`/`549v`).

Everything below is that thesis made concrete for the two constructs `654` found missing:
**generics** and **traits/impls**.

## The construct vocabulary — the bracket is the kind

A type's kind is explicit on its declaration form, never inferred from position (`3742`); the
six-delimiter closed set (`j9du`) carries every construct:

```
   BASE                          PIPE FAMILY (pipes inside, mirroring the string form)
   ( … )  application / record   [| … |]  STRING            (3qjw)
   [ … ]  enum / vector / params (| … |)  GENERIC decl      (hh3z)   ← assigned this arc
   { … }  struct / map / ns      {| … |}  TRAIT / IMPL      (bpyu)   ← assigned this arc

   Name { … }   = struct          Name (| [P…] body |) = generic (inner []/{} → enum/struct)
   Name [ … ]   = enum            {| [P…]? Trait Target [body]? |} = impl (optional ends)
   Name <ref>   = newtype         (Head Arg…)          = generic USE (name-resolved)
```

The two pipe assignments **supersede** the legacy pipe-brace=struct / pipe-paren=enum design
(`own9` had vacated it for the positional forms; this arc retired/superseded the stale records
— see `1`). The binders of a generic declaration and of an impl scope their body
**structurally** — params and body live together inside the one pipe form — retiring the
old key/value side-channel (the "second object is outside the first" defect). Use sites stay
bare `(Work A B)` and resolve by name exactly as `(Vector X)` does, because the declaration
made the head a *known* construct — legitimate resolution, not guessing (`3742` clarified).

## The pipeline — declare once, bind per component, expand

```
  reaction.schema              spirit nexus (the WHOLE authored surface)
  ┌────────────────────┐       ┌──────────────────────────────────────────┐
  │ Work  (| [E W R Ef] │       │ { Work reaction:reaction:Work … }          │
  │       [legs] |)      │  ───▶ │ (Work SignalInput SemaWriteOutput …)       │  Input
  │ Action(| […] [legs])│       │ (Action SignalOutput … (Work …))           │  Output
  └────────────────────┘       └──────────────────────────────────────────┘
        declared ONCE                    bind per component (zjmc)
                                              │  EXPANSION (binder→argument), build-time (9rjq)
                                              ▼
  ┌──────────────────────────────────────────────────────────────────────────┐
  │ pub enum Input  { SignalArrived(SignalInput), … }                          │
  │ pub enum Output { …, Continue(Input) }                                     │
  │ impl Input { signal_arrived(…) … }   impl From<SignalInput> for Input …    │  ← existing
  │ + payload structs / enums / newtypes, constructors, From, rkyv+NOTA codecs │    emitters,
  └──────────────────────────────────────────────────────────────────────────┘    ZERO new
        a concrete OWNED interface — not  pub type Input = Work<…>                  machinery
```

**Expansion, not generic-alias** (`656`/`657`): the expanded enum has empty parameters, so
the existing concrete-enum emitters supply constructors/`From`/accessors/codecs and the
parameterized-decl suppression guards never fire — zero new codegen. Alias is wire-identical
(Rust monomorphizes to the same bytes), satisfies `zjmc` no better, and would cost the
generic-impl-header emission that doesn't exist. Genericity is a *schema-authoring*
convenience and a thing for genuinely-polymorphic hand-written runtime code (`triad-runtime`);
it is not stamped into every component's output. **Proven green** (`656`): a two-line binding
replaces ~4,200 lines of hand-spelled Rust.

## The boundary — what is data, what stays hand-written

```
  marker / empty body      ─┐
  mechanical body (fixed,   ├─  DATA → generated   (the {| |} construct, code-is-data,
   named: payload-proj,     │                        expression trees via the application form)
   constructor, From, …)   ─┘
  ─────────────────────────────────────────────────────────────────────────────────
  business logic            ──  HAND-WRITTEN on generated nouns   (5hjv — deliberate, not debt:
  (Nexus decide, store,                                            Nexus plane, store, guardian,
   guardian, query matches)                                        signal-query matchers)
```

The hard line (candidate Principle, `654`): generated impl bodies are capped at marker +
the small fixed mechanical family; arbitrary Rust expression bodies are never modeled as
data, because that rebuilds an expression compiler inside NOTA (`4itr`/`2zed`). A method body
*is* data (an expression tree over `(Head Arg…)`), but only for the generatable tiers.

## Settled / open / operator ledger

**Settled (recorded in Spirit, verified active):** kind-explicit-on-the-form (`3742`);
`(| |)` = generic declaration, inner `[]`/`{}` = enum/struct, binders scope body structurally
(`hh3z`); generic use stays `(Head Arg…)` name-resolved (`wqdi`/`3742`); `{| |}` = trait/impl
(`bpyu`); pipe forms are generics/traits, not declaration forms, positional forms declare
(`n1px`/`own9`); expansion-not-alias codegen (`656`, proven); declare-once-bind-per-component
(`zjmc`); the hand-written-behavior boundary (`5hjv`). The deprecated pipe-struct/enum cluster
is retired/superseded; the store is internally consistent.

**Open frontiers (`2`/`3`):** the `fn`/signature construct for trait *declarations*
(signatures datify; default bodies are real Rust); the `{| |}` optional-slot/where-clause
semantics and reconciliation with the alternative `(Impl …)` section form; the named
mechanical-body family beyond payload-projection; **generic impl-header emission**
`impl<P..> Type<P..> where P: Bound` + a parameter-bound vocabulary (genuinely NEW codegen,
not free from generics-as-data — until it lands, the suppressed parameterized-decl impls stay
suppressed); role→trait binding (explicit table vs structural inference in `nexus_runner_shape`);
the declare-once consolidation deleting the triplicated `OriginRoute`/`Engine*Failure` +
`plane.rs` bridges; shape-vocabulary-as-data / the meta-schema fixpoint (aspirational).

**Candidate intent worth recording** (not yet in Spirit): the concrete `{| [params]? Trait
Target [body]? |}` impl shape rule with optional-ends sugar (`bpyu` records the delimiter, not
the shape detail); the concrete-owned-interface principle (genericity is schema-authoring
convenience, not a generated-output abstraction — `657`); the generated-body cap (marker +
fixed mechanical family). Hold for the psyche.

**What operators build** (on top of the proven expansion engine, `2`): the `(| … |)` declare
arm (value-lowering path in `source.rs`; a `PipeParenthesis` `#[shape]` in nota-next — parser
already produces it); land the `656` expansion prototype (delete the legacy alias path); keep
`(Head Arg…)` for use; flatten the per-leg newtype layer. Then down `654`'s inventory: the
single-payload `Deref` directive (cleanest first proof), leaf shapes in the derive (to delete
schema-cc's own newtypes), the `ImplDeclaration` section, generic impl-header threading.
Code-repo main is operator's lane; the designer prototype + this spec are the build target.

## The through-line, in one sentence

Make the schema language express every construct a component needs as data, with each
construct's kind explicit on its form; declare the universal frames once and bind them per
component; expand the bindings into concrete owned interfaces with their impls generated
build-time; and keep only genuine behavior hand-written on the generated nouns — turning
~4,200 lines of hand-wired component Rust into a handful of declarations.
