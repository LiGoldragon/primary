# 660 — The whole vision, tested: pipe-delimiter schema → a generated complex component

The psyche asked to *see the whole vision, with schema syntax on complex, tested code —
implement further to make the tests impressive.* This is that demonstration: a complex
component authored entirely in the pipe-delimiter schema syntax, with **generics, traits/impls,
and code-is-data** all generating real Rust, proven green. Built on the proven `656` expansion
(designer worktrees `reaction-expand`, not pushed). Design reference: meta-report `659`.

## Verdict — every piece generates, compiles, round-trips, and the impls work

| Piece | Status |
|---|---|
| `(\| [params] body \|)` generic declaration (parse + lower) | **green** — lowers to the same parameterized `Declaration` the bare-paren head produces |
| Generic *use* `(Work …)` + expansion to a concrete enum | **green** — `Input`/`Output` expand leg-for-leg (the `656` path) |
| `{\| Trait Target \|}` marker impl | **green** — emits `impl Auditable for EntryHandle {}`; a trait-bounded fn accepts the type |
| `{\| Deref Target [body] \|}` **code-is-data** Deref | **green** — `(reference (field self payload))` → `fn deref(&self) -> &Self::Target { &self.0 }`; derefs at runtime |
| Payload struct / enum / newtype | **green** |
| rkyv + NOTA round-trip of the expanded enums (incl. recursive `Continue(Input)`) | **green** |
| Generic impl-header `impl<P..> Type<P..> where P: Bound` | **out of scope** — carried but `assert`-rejected at emission (honest, no silent wrong output) |

Tests (re-run and verified, not trusted): **`pipe_delimiter_demo` 10/10**; schema-rust-next
full suite **98/0**; schema-next **171/0**; `cargo clippy` clean on both. The shared `/git`
checkouts are clean.

## The schema — the whole component, in pipe-delimiter syntax

The frames, declared **once** (`reaction.schema`):

```
{
  Work (| [Event WriteDone ReadDone EffectDone]
    [(SignalArrived Event) (SemaWriteCompleted WriteDone) (SemaReadCompleted ReadDone) (EffectCompleted EffectDone)] |)
  Action (| [Reply Write Read Effect Continuation]
    [(ReplyToSignal Reply) (CommandSemaWrite Write) (CommandSemaRead Read) (CommandEffect Effect) (Continue Continuation)] |)
}
```

The component — bind + expand, payloads of each kind, a marker impl, a code-is-data Deref
(`ledger.schema`):

```
{ Work reaction:reaction:Work  Action reaction:reaction:Action }
(Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome)
(Action SignalOutput SemaWriteSet SemaReadInput EffectCommand (Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome))
{
  LedgerEntry { statement Statement sequence Integer }          ;; struct
  EntryHandle  Statement                                        ;; newtype
  SemaWriteSet [(Record) (Remove)]                              ;; enum
  …
  EntryHandleIsAuditable {| Auditable EntryHandle |}                                  ;; marker impl
  EntryHandleDeref       {| Deref EntryHandle [ (deref (reference (field self payload))) ] |}  ;; code-is-data Deref
}
```

## The generated Rust

```rust
// generic frame, expanded per binding (the 656 path):
pub enum Input  { SignalArrived(SignalInput), SemaWriteCompleted(SemaWriteOutput),
                  SemaReadCompleted(SemaReadOutput), EffectCompleted(EffectOutcome) }
pub enum Output { ReplyToSignal(SignalOutput), CommandSemaWrite(SemaWriteSet),
                  CommandSemaRead(SemaReadInput), CommandEffect(EffectCommand), Continue(Input) }
// + auto constructors (Input::signal_arrived(…)), From impls (incl. From<Input> for Output),
//   and the rkyv + nota-text codecs — all from the existing concrete-enum emitters.

pub struct LedgerEntry { pub statement: Statement, pub sequence: Integer }   // struct
pub struct EntryHandle(Statement);                                           // newtype
pub enum SemaWriteSet { Record(Record), Remove(Remove) }                     // enum

impl Auditable for EntryHandle {}                       // marker impl, from {| Auditable EntryHandle |}

impl std::ops::Deref for EntryHandle {                  // from {| Deref EntryHandle [ … ] |}
    type Target = Statement;
    fn deref(&self) -> &Self::Target { &self.0 }
}
```

## The code-is-data proof

The `Deref` body is **not** hand-written and **not** a hardcoded template — it is projected
from a data expression tree the schema carried. In schema-next `src/schema.rs`:

```rust
pub enum Expression {
    SelfReceiver,                                   // self
    Field(Box<Expression>, Name),                   // <base>.<field>  (payload → tuple .0)
    Reference(Box<Expression>),                      // &<inner>
}
impl Expression {
    pub fn to_rust(&self) -> String {                // the tiny generic interpreter over the body data
        match self {
            Self::SelfReceiver => "self".to_owned(),
            Self::Field(base, field) => format!("{}.{}", base.to_rust(),
                if field.as_str() == "payload" { "0".to_owned() } else { field.field_name() }),
            Self::Reference(inner) => format!("&{}", inner.to_rust()),
        }
    }
}
```

So `(reference (field self payload))` in the schema becomes `&self.0` in the emitted `deref`.
That is `4itr`/`7c71` made concrete at the smallest scale: a method body is a data object,
read by one tiny interpreter, not text-with-sigils. The test
`deref_impl_emits_from_code_is_data_body` asserts the emitted block, and
`deref_impl_returns_inner_payload` runs it.

## What the tests prove

`generic_declaration_expands_to_concrete_root_enums` (the `(| |)` declaration expands to
concrete `Input`/`Output`); `payload_types_of_each_kind_emit` (struct/enum/newtype);
`marker_impl_emits_empty_impl_block` + `marker_impl_admits_a_trait_bounded_function` (the
marker impl exists and a `fn audit<T: Auditable>` accepts `EntryHandle`);
`deref_impl_emits_from_code_is_data_body` + `deref_impl_returns_inner_payload` (the Deref
emits from the expression tree and derefs to the inner payload at runtime);
`expanded_input_round_trips_through_rkyv`, `expanded_output_recursive_continue_round_trips_through_rkyv`,
`expanded_enums_round_trip_through_nota` (both wire formats, incl. the recursive
`Continue(Input)` leg).

## Honest scope — what is proven vs deliberately deferred

Proven green: the generics leg (declaration + use + expansion), the `{| |}` trait/impl
construct for **markers** and a **`Deref`** with a code-is-data body, and the full
round-trip. Deliberately out of scope, and `assert`-rejected rather than faked:

- **Generic impl-header threading** `impl<P..> Type<P..> where P: Bound` — the genuinely-new
  codegen behind "bounds"; carried in the model, rejected at emission.
- **Method-bearing impls beyond `Deref`** — the fixed-signature `Deref` is the only
  method-bearing trait this slice emits; another method-bearing trait `assert`s. The
  expression family is the minimal `self` / `field` / `reference` set — exactly enough for the
  single-field Deref body.
- The Deref-target-not-a-newtype and unparseable-body cases `panic` at generation (a typed
  `SchemaError` would be cleaner if this lands).

These are the same frontiers `659`/`d3r2` flagged; nothing is silently wrong.

## What this means for the design

This moves the trait/impl leg from *designed-but-not-integrated* (the low-certainty record
`d3r2`) to *demonstrated-green-on-a-complex-component*. The whole vision — every construct
authored in pipe-delimiter syntax, generating real Rust, code-is-data and all — is now a
running, tested artifact, not a paper claim. The certainty on `d3r2` is a candidate to raise
once operator lands the leg on code-repo main (the worktrees `schema-next reaction-expand` /
`schema-rust-next reaction-expand` are the merge-ready material; not pushed). The schema-next
diff is +916/-30 (`ImplDeclaration`/`ImplBody`/`MethodDeclaration`/`Expression`, the `(| |)` /
`{| |}` lowering arms); schema-rust-next +248 (`RustImpl`/`emit_impl`/`RustImplTokens`).
