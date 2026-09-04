# Witness: ethos-zero struct emission on origin/main

Flow: 6329f1
Witnessed rev: 31c5984c7fda (origin/main), ahead of previously reported 185f13a9
Method: detached worktree at origin/main; `cargo run` on fixtures/orchestrate.ethos; source reading of reader and emitter in src/lib.rs and committed src/generated.rs

## 1. Generated Rust for orchestrate signal types

Run: `cargo run -- "Generate.{ .../fixtures/orchestrate.ethos .../output }"`
Output file: signal.rs (rustfmt-formatted)

All structs are **positional tuple structs**. No named fields anywhere.

### Lock

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Clone, Debug, PartialEq, Eq)]
pub struct Lock(
    pub LockId,
    pub LockName,
    pub FlowId,
    pub LockPaths,
    pub LockReason,
);
```

### LockRequest

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Clone, Debug, PartialEq, Eq)]
pub struct LockRequest(pub LockName, pub FlowId, pub LockPaths, pub LockReason);
```

### Request (enum)

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Clone, Debug, PartialEq, Eq)]
pub enum Request {
    Lock(LockRequest),
    Release(LockId),
    Observe(ObserveSelection),
}
```

### Reply (enum)

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Clone, Debug, PartialEq, Eq)]
pub enum Reply {
    Locked(Lock),
    LockRejected(LockRejection),
    Released(Lock),
    ReleaseRejected(ReleaseRejection),
    Observed(Observation),
}
```

### Aliases

```rust
pub type LockId = protos::Integer;
pub type LockName = protos::Text;
pub type FlowId = protos::Text;
pub type LockPath = protos::Text;
pub type LockPaths = Vec<LockPath>;
pub type LockReason = protos::Text;
pub type DuplicateName = Lock;
pub type Locks = Vec<Lock>;
```

All field access in the generated Corporal/Datomic impls is positional: `self.0`, `self.1`, etc.

## 2. Reader: accepted declaration forms

The reader is `fn read_type_declaration` at src/lib.rs:747-790. It accepts exactly four forms for a type inside the types vector of a Library or Signal:

| syntax | internal representation | emitted Rust |
|---|---|---|
| `Name.{ T1 T2 }` (braced body) | `TypeDeclaration::Struct { name, fields }` | tuple struct |
| `Name.[ V1 V2 ]` (bracketed body) | `TypeDeclaration::Enum { name, variants }` | enum |
| `Name.<<< K V >>>` (guillemets body) | `TypeDeclaration::Map { name, key, value }` | type alias to BTreeMap |
| `Name.Type` (bare body / following) | `TypeDeclaration::Alias { name, target }` | type alias |

Match arms (src/lib.rs:757-790):

```rust
    // line 757: braced -> Struct
    if let Some(children) = pf_braced(body) {
        let fields = read_type_expression_list(children)?;
        return Ok((TypeDeclaration::Struct { name, fields }, false));
    }

    // line 762: bracketed -> Enum
    if let Some(children) = pf_bracketed(body) {
        let variants = read_variants(children)?;
        return Ok((TypeDeclaration::Enum { name, variants }, false));
    }

    // line 767: guillemets -> Map
    if let Some(children) = pf_guillemets(body) {
        ...
        return Ok((TypeDeclaration::Map { name, key, value }, false));
    }

    // line 788: fallthrough -> Alias
    let (target, consumed) = read_type_expression_with_following(body, following)?;
    Ok((TypeDeclaration::Alias { name, target }, consumed))
```

There is **no** `Struct.{ ... }` / `Tuple.[ ... ]` / `Record` form in the reader. The reader does not distinguish "Struct" or "Tuple" as head keywords; it dispatches purely on the delimiter (`{` vs `[` vs `<<` vs bare). The names "Struct", "Enum", "Alias", "Map" exist only in the internal Rust `TypeDeclaration` enum, not in the input syntax.

### ethos-zero.ethos (the self-description)

The self-description uses the same `Name.{ ... }` form for all its struct types:

```
; ethos-zero.ethos (lines 5-7 excerpted)
  Library.{ Version Vector<Import> Vector<TypeDeclaration> Vector<KindDeclaration> Vector<Association> }
  Signal.{ Version Vector<Import> Vector<SectionReference> Vector<SectionReference> Vector<TypeDeclaration> }
  Version.{ Integer Integer Integer }
```

And `Name.[ ... ]` for its enums:

```
  TypeDeclaration.[ Struct.{ Text Vector<TypeExpression> } Enum.{ Text Vector<Variant> } Alias.{ Text TypeExpression } Map.{ Text TypeExpression TypeExpression } ]
```

Here `Struct`, `Enum`, `Alias`, `Map` appear as variant names inside the `TypeDeclaration` enum declaration -- they are ordinary user-chosen variant names that happen to match the internal representation, not special syntax keywords.

### Committed src/generated.rs

The self-bootstrap generates the same tuple-struct form:

```rust
pub struct Library (pub Version , pub Vec < Import > , pub Vec < TypeDeclaration > , pub Vec < KindDeclaration > , pub Vec < Association > ,)
pub struct Signal (pub Version , pub Vec < Import > , pub Vec < SectionReference > , pub Vec < SectionReference > , pub Vec < TypeDeclaration > ,)
pub struct Version (pub protos :: Integer , pub protos :: Integer , pub protos :: Integer ,)
```

No named-field structs appear anywhere in generated.rs. The self-bootstrap is not a second syntax; it uses the same reader and emitter as any other .ethos file.

## 3. Emitter: struct emission and tuple path

### Struct emission (src/lib.rs:1213-1222):

```rust
        TypeDeclaration::Struct { name, fields } => {
            let name = ident(name)?;
            let field_tokens = fields
                .iter()
                .map(|ty| {
                    let ty = type_expression_tokens(ty, imports)?;
                    Ok(quote! { pub #ty })
                })
                .collect::<Result<Vec<_>, Fault>>()?;
            quote! { #derive pub struct #name ( #( #field_tokens, )* ); }
        }
```

This is the **only** struct emission path. It always emits `pub struct Name(pub T1, pub T2, ...);` -- a tuple struct. There is no named-field struct emission anywhere in lib.rs. The `#fields` variable in the quote contains type expressions only (no field names), yielding `pub T1, pub T2` inside parentheses.

### Lines 1310-1340 (type_expression_tokens):

```rust
fn type_expression_tokens(
    expr: &TypeExpression,
    imports: &HashMap<String, String>,
) -> Result<proc_macro2::TokenStream, Fault> {
    Ok(match expr {
        TypeExpression::Named(name) => match name.as_str() {
            "Text" => quote! { protos::Text },
            "Integer" => quote! { protos::Integer },
            "Decimal" => quote! { protos::Decimal },
            "Boolean" => quote! { protos::Boolean },
            "Meaning" => quote! { datomic::MeaningValue },
            "Symbol" => quote! { protos::Symbol },
            _ => {
                if let Some(module) = imports.get(name.as_str()) {
                    let module = ident(module)?;
                    let name = ident(name)?;
                    quote! { #module :: #name }
                } else {
                    let name = ident(name)?;
                    quote! { #name }
                }
            }
        },
```

This is not a "tuple path" -- it is the type-expression resolver. It fires for every type reference in fields, variants, aliases. The struct emission at line 1213 calls this for each field type.

**Decision point**: There is none. There is exactly one code path for `TypeDeclaration::Struct`, and it always emits a tuple struct. The reader always parses `Name.{ ... }` as `TypeDeclaration::Struct`. No branch or condition selects between named-field and tuple emission.

## 4. Commit history

```
31c5984 Import resolution in emitter, datom round-trip proptest, version 1.1.0
185f13a Pin datomic a27f9b8e: structural faults datomize without Debug
f2211ac Emit aliases as type aliases in Signal, add Corporal/Datomic for wire types
b869598 Full Protosizable, Corporal/Datomic split, e2e compile test, nix flake check pass
c85e9f7 Commit self-bootstrap module, freshness test, final protos/datomic pins
d42904e Pin final ProtoformStack revs, add Conceptual/Protosizable layer, drop splitting workaround
52c975e Integrate ProtoformStack: Protoform/Head/Qualified API, incorporate/datomize, single-; comments
907d015 Move entry points under Actualizing and Emitting kinds, fully qualify intrinsic names
```

One commit after 185f13a: 31c5984 ("Import resolution in emitter, datom round-trip proptest, version 1.1.0"). The diff of src/lib.rs between 185f13a and 31c5984 (115 insertions, 42 deletions) adds import resolution (a `HashMap<String, String>` threaded through the emitter so imported names resolve to `module::Name`) and a proptest. It does **not** change struct emission: the `quote! { #derive pub struct #name ( #( #field_tokens, )* ); }` line is identical before and after.

## Finding

On origin/main (31c5984), a user's `Name.{ T1 T2 }` declaration becomes a **positional tuple struct** `pub struct Name(pub T1, pub T2);` with no field names. This is the only struct form the emitter can produce. There is no named-field struct form in the accepted syntax, no `Struct.{ }` / `Tuple.[ ]` / `Record` reader dispatch, and no second syntax for the self-bootstrap. The earlier report that line 793 emits named-field structs via `quote! { #visibility struct #name #generics { #( #fields, )* } }` does not match the code at 31c5984: that line reads `quote! { #derive pub struct #name ( #( #field_tokens, )* ); }` -- tuple struct syntax. The discrepancy may reflect a different branch (the `horizon-named-fields` worktree exists) or an older rev; at origin/main it is tuple structs only.

## Unknowns

- A worktree named `horizon-named-fields` exists under the ethos-zero worktree root; its content was not examined. It may contain a branch where named-field structs are emitted.
- Another subflow may have pushed a newer main during this witness. The witness is valid for 31c5984.
- The earlier read subflow may have been looking at a different checkout (detached, or the working copy of a worktree) rather than origin/main.

## Sources

- ethos-zero origin/main 31c5984c7fda (fetched 2026-09-04)
- src/lib.rs lines 747-790 (reader), 1213-1222 (struct emitter)
- src/generated.rs (committed self-bootstrap output)
- fixtures/orchestrate.ethos (orchestrate lock signal declaration)
- `cargo run` output on fixtures/orchestrate.ethos -> signal.rs
