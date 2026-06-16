# 659/2 — The settled design

The schema language's construct vocabulary and the code generation, as settled across
`654`–`658`. Detail lives in those reports; this is the consolidated specification.

## The delimiter family (six brackets)

The bracket **is** the kind (`3742`/`hh3z`) — the same move `{}`/`[]` already make:

| Delimiter | Holds | Meaning |
|---|---|---|
| `( … )` | objects | application / headed form / record |
| `[ … ]` | objects | enum body, vector, parameter list |
| `{ … }` | objects | struct body, strict key-value map, namespace |
| `[\| … \|]` | text | bracket-safe / multiline **string** (`3qjw`) |
| `(\| … \|)` | objects | **generic declaration** (`hh3z`) |
| `{\| … \|}` | objects | **trait / impl** construct (`bpyu`) |

Three base pairs + three pipe variants (`j9du`); pipes written *inside* the bracket to
mirror the string form. The pipe assignments supersede the legacy pipe-brace=struct /
pipe-paren=enum design (`own9` had already vacated it for positional `{}`/`[]`).

## Generics

**Declaration** — `Name (| [params] <body> |)`. The `(| |)` announces "generic" (kind
explicit, never guessed); `[params]` is the binder list; `<body>` is an ordinary struct/enum
body whose **inner** delimiter selects the kind (`[…]` = enum, `{…}` = struct). Params and
body live **together inside** the `(| |)` so the binders scope the body **structurally** —
no key/value side-channel threading (the "second object is outside the first" defect, fixed).

```
Work (| [Event WriteDone ReadDone EffectDone]
  [(SignalArrived Event) (SemaWriteCompleted WriteDone) (SemaReadCompleted ReadDone) (EffectCompleted EffectDone)] |)
Sema (| [Root] { origin_route.OriginRoute root.Root } |)      ;; generic struct
```

**Use / application** — the flat `(Head Arg…)` form, name-resolved (`wqdi`): `(Work
SignalInput SemaWriteOutput SemaReadOutput EffectOutcome)`. `Work` resolves by name exactly as
`(Vector X)`/`(Map K V)` do, because the `(| |)` declaration made it a *known* generic.
Use-site name resolution is legitimate, not guessing (`3742` clarified) — so no new use
delimiter, keeping `{| |}` free for traits. Arity-checked at lowering.

## Traits / impls — `{| |}`

A single positional, `for`-less object (no embedded keywords), with **optional ends**,
shape-discriminated structural-macro sugar:

```
{| Trait Target |}                       ;; marker impl (no params, no body)
{| [T] Trait Target |}                    ;; generic marker
{| Trait Target [ <body> ] |}             ;; impl with body
{| [T] Trait Target [ <body> ] |}         ;; generic impl with body
```

The reader discriminates by shape: a leading `[…]` = the param list; a trailing `[…]` =
the body; position settles which. The empty `[]` is never written — absence is "none." A
marker trait's impl is *legitimately* empty (it asserts membership); a method-bearing impl
**must** carry its methods (an empty impl of a real trait is pointless).

An impl is a single object so its `[T]` scopes the trait, target, and body together — the
same structural-scope rule as the generic declaration. The impl/trait leg is the
**least-designed**: `bpyu` records `{| |}` = trait/impl, but the optional-slot semantics,
where-clauses, and the trait-declaration `fn`/signature sub-construct are recognized but not
finally specified (`654` also sketched an alternative `(Impl …)` top-level-section form —
not finally reconciled with the `{| |}` object form).

## Code is data

A method/function body is a NOTA data object — an **expression tree** built from the same
recursive application form `(Head Arg…)` (`4itr`/`7c71`). The body recurses through the
application form the way a type reference does, e.g. `&self.payload` →
`(reference (field self payload))`. A `fn` is `name + [params] + return + body-expression`.

The load-bearing gradient (the `5hjv` boundary, ratified as deliberate):

1. **Marker** bodies — empty / blanket impls; fully data.
2. **Mechanical** bodies — a small **fixed, named** family (payload projection
   `self.payload()`, the auto-emitted constructor `Self::Variant(payload)`, `From` legs,
   accessors); datifiable as named directives.
3. **Business-logic** bodies — the Nexus decision plane, store, guardian, signal-query
   matchers — **never** modeled as data; stay hand-written on generated nouns.

The hard line (candidate Principle, `654`): generated impl bodies are capped at marker +
the fixed mechanical family; arbitrary Rust expression bodies are not data, because that
rebuilds an expression compiler inside NOTA (`4itr`/`2zed`).

## Code generation — EXPANSION, not generic-alias

A component root is **expanded** by positional binder→argument substitution into a
**concrete enum with empty parameters**, not left as `pub type Input = Work<…>`. Because the
expanded enum has empty params, the parameterized-decl suppression guards
(schema-rust-next `lib.rs:5104/5154`) don't fire, so the existing concrete-enum emitters
supply constructors / `From` / accessors / wire derives — **zero new codegen**. Alias was
rejected: wire-identical (Rust monomorphizes to the same layout), satisfies `zjmc` no better,
and would cost the generic-impl-header emission that doesn't exist. Generics are a
schema-authoring convenience + a thing for genuinely-polymorphic hand-written runtime code
(`triad-runtime`), not stamped into every component's surface (`657`).

**Proven** (`656`, re-verified green; designer worktrees `reaction-expand`, not pushed):
schema-next `RootApplication::expand_with` (promoted `FrameExpansion` method) +
`Schema::expand_application_root` (+ sibling-Continuation re-aim) + `ResolvedImport` carrying
params/variants; schema-rust-next applied-roots branch → concrete `RustEnum` into
`root_enums`. `cargo test --test spirit_frame_application` 5/5; full suites green (schema-next
18 binaries, schema-rust-next 88) — no regression. A two-line binding replaces ~2578 lines of
`nexus.rs` + ~1577 of `sema.rs` + 61 of `plane.rs`.

## The complete worked example (`658`)

```
;; reaction.schema — the frame, declared ONCE
Work (| [Event WriteDone ReadDone EffectDone] [(SignalArrived Event) …] |)
Action (| [Reply Write Read Effect Continuation] [(ReplyToSignal Reply) …] |)

;; spirit nexus — the whole reaction-core authored surface
{ Work reaction:reaction:Work  Action reaction:reaction:Action }
(Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome)
(Action SignalOutput SemaWriteSet SemaReadInput EffectCommand (Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome))
```

generates the concrete `pub enum Input { SignalArrived(SignalInput), … }`, `pub enum Output
{ …, Continue(Input) }`, their constructors and `From` impls, the payload structs/enums/
newtypes — flattening today's redundant double-newtype-wrap (`struct SignalArrived(SignalInput)`
*and* `NexusWork::SignalArrived(SignalArrived)`) to one layer.

## What operators implement (on top of the proven engine)

1. **`(| … |)` declare arm** — value-lowering path in `source.rs` (the name is the key,
   `(| [params] body |)` is the value): `child[0]` = params, `child[1]` = body (inner
   delimiter → enum/struct); lowers to the same parameterized `Declaration` as the bare-paren
   head form. Sub-work in nota-next: a `#[shape]` recognizing the `PipeParenthesis` delimiter
   (the parser already produces it; no seed change).
2. **Generic use** stays `(Head Arg…)` — no work.
3. **Expansion at applied-root lowering** — land the `656` prototype; delete the legacy alias
   path once accepted.
4. **Flatten** the per-leg newtype layer.

## Open frontiers

The `fn`/signature construct for trait *declarations* (signatures datify; default bodies are
real Rust); the `{| |}` optional-slot/where-clause semantics and the reconciliation with the
`(Impl …)` section form; the named mechanical-body family beyond payload-projection; generic
impl-header emission `impl<P..> Type<P..> where P: Bound` + a parameter-bound vocabulary (NEW
codegen, gated); role→trait binding (explicit table vs structural inference); the declare-once
consolidation deleting the triplicated `OriginRoute`/`Engine*Failure` + `plane.rs` bridges;
shape-vocabulary-as-data / the meta-schema fixpoint (aspirational).
