# 663 — Standard generated impls + shape-derived capability resolution: the default policy

Co-signed psyche+operator direction (Spirit `d3r2`, Clarified): move from a method-NAME
allowlist to receiver-SHAPE-DERIVED capability resolution, and settle *which* shape-implied
methods become standard generated impls by default. This report grounds the policy in the live
emitter, the real `spirit`/`signal-spirit` source, and the census (661). It answers the four hard
questions concretely and gives one default-policy recommendation.

## TL;DR — the recommendation

| Decision | Answer |
|---|---|
| Capability resolution | Receiver-shape-derived `P(shape, inner)`, not a method-name list. Implemented as a typed `Capability` set computed from `RustNewtype`/`RustStruct`/`RustEnum` + the *kind* of the inner `TypeReference`. |
| Default-ON, unconditional | The **inherent constructor surface** every shape can guarantee from structure alone: newtype `new`/`payload`/`into_payload`/`From<Inner>`; enum `route` + per-variant `is_/as_`; struct field accessors. These need no inner-trait knowledge and can never be wrong. |
| Default-ON, *conditional on inner kind* | The **scalar-leaf delegations** — `Display`, `PartialEq<scalar>`, `PartialOrd<scalar>`, `AsRef<str>` — only when the inner is a known scalar (`String`/`Path`/`Integer`/`Boolean`). Already built (`StandardNewtypeImplTokens`); flip its gate ON. |
| Opt-in marker | `Deref` and the **nested-newtype scalar transitivity** (`payload().payload()`). These are *intent*, not structure — most schema-type newtypes must NOT deref. A `*deref` newtype marker. |
| Leave to `#[derive]` | `Clone`/`Debug`/`Eq`/`PartialEq<Self>`/`Hash`/`Default` — already standard derives on the schema-emitted types; do not re-emit by hand. |
| Avoid entirely | A broad std-leaf allowlist (`trim`/`to_lowercase`/`chars`/`wrapping_add`/`iter`). These appear ONLY inside business-logic validators in the real code, never as standalone delegating methods. `as_str` is covered by `AsRef<str>`; keep no separate `as_str` list. |

## The decisive new fact the census did not have

Counting the real schemas (`signal-spirit/src/schema/*.rs` + `spirit/src/schema/*.rs`):

- **18** newtypes wrap a scalar (`String`/`Path`/`u64`/`bool`).
- **189** newtypes wrap *another schema type* (`Statement(StatementText)`, `Recorded(SemaReceipt)`, …).
- Of those ~207 newtypes, only **~24 have a hand-written `Deref`** (12 in `engine.rs`, 12 in
  `signal-spirit/src/lib.rs`).

So the schema-type-wrapping newtype is the *dominant* shape (189), yet **~88% of them deliberately
do NOT deref.** That single ratio decides question (a): `Deref` is opinionated, not structural.
Generating it for every newtype would punch transparent holes in 165 abstraction boundaries the
authors intentionally kept opaque.

## State of the code today (what is already built)

The proposal is not greenfield — the `schema-rust-next` worktree already carries the committed
change `vrvvvuxlnpws` ("demonstrate schema-implied newtype trait impls"):

- `NewtypeInherentImplTokens` (`lib.rs:1985`) **already emits** `new`/`payload`/`into_payload`/
  `From<Inner>` for every newtype — unconditional, default-on. This is the inherent-constructor tier
  and it is already correct.
- `StandardNewtypeImplTokens` (`lib.rs:2058`) **already emits** `Display` + `AsRef<str>` +
  `PartialEq<&str>` (string-like), `PartialEq<u64>` + `PartialOrd<u64>` (integer), `PartialEq<bool>`
  (boolean) — gated by `scalar_like()`, and **explicitly skips** plain schema-type newtypes
  (`tests/standard_newtype_impls.rs:59` asserts `WrappedName` gets none). 3 tests green.
- It is gated behind an **opt-in** `RustEmissionOptions::with_standard_newtype_impls()`
  (`standard_newtype_impls: false` by default in all three constructors, `lib.rs:463/479/492`).
- `RouteMatchArm` (`lib.rs:1678`) **already emits** the `Self::Variant(_) => Route::Variant` /
  `Self::Variant => Route::Variant` shape — i.e. the 24-arm `OperationKind::from_input` is *already*
  a generated shape (the `route` method), handling both payload-discard and unit arms.
- **`Deref` is emitted nowhere.** All ~24 Deref impls are hand-written; the newtype path has no
  `deref` generation at all.

So three of the four tiers below are already implemented; the work is (1) decide the default flips,
(2) add the `Deref` marker, (3) lift name-only resolution to shape-derived resolution.

## Shape-derived capability resolution (the d3r2 core)

The shallow model (operator finding 2; 661/4 prototype) resolved a call by method name against a
3-entry alphabet `{payload, into_payload, as_str}`. The recorded direction is to compute the
receiver's shape and look the call up in *that shape's* capability set. Concretely:

```
Capability resolution = f(receiver shape, inner TypeReference kind)
  RustNewtype{inner: scalar}      → { new, payload, into_payload, From<Inner>,
                                      Display, PartialEq<scalar>, PartialOrd<scalar>?, AsRef<str>? }
  RustNewtype{inner: schema type} → { new, payload, into_payload, From<Inner> }   (no Deref unless marked)
  RustNewtype{inner: Vec/Map}     → { new, payload, into_payload, From<Inner> }
  RustStruct{fields}              → { new, <field accessors>, into_<field>, with_<optional>? }
  RustEnum{variants}              → { route, is_<v>, as_<v>, <v> constructor, From<unique payload> }
```

`payload` now resolves because the receiver **is** a newtype (the shape carries the capability),
not because `"payload"` is in a list. `as_str`/`Display` resolve only when `inner` is scalar.
The first call landing in no capability set is business logic → typed
`SchemaError::UnresolvedComposition { receiver_type, receiver_shape, method }` (extend the existing
variant with `receiver_shape` so the error names *why* it missed). This also subsumes operator
finding 1: the surrounding `assert!`/`panic!` for unsupported impl emission must become the same
typed `SchemaError` path — a schema author gets a typed error, never a generator panic.

## The four hard questions, answered

### (a) Is `Deref` safe to generate for EVERY newtype? — No. Opt-in marker.

`Deref` is the most-requested-by-d3r2 capability and the most dangerous to default-on. The data:
189 schema-type newtypes, only ~24 want `Deref`. The ~24 that do are a recognizable *kind* — the
**semantic-occasion wrapper**: `Recorded(SemaReceipt)`, `Found(FoundRecord)`, `Observed(ObservedRecords)`,
`SignalArrived(Input)`, `ReplyToSignal(Output)` — a newtype whose entire purpose is to *name a role*
for an existing payload type and forward to it. The other 165 are *distinct values* that happen to
be built on a base type and must stay opaque (a `RecordIdentifier` is not interchangeable with its
inner string for arbitrary `str` methods; deref would leak `.len()`, `.chars()`, slicing, etc.).

Auto-`Deref`-for-every-newtype is the textbook newtype anti-pattern: it destroys the abstraction the
newtype exists to create. There is no structural signal that separates the 24 from the 165 —
*it is author intent*. Therefore:

> **Recommendation: `Deref` is opt-in via a newtype marker (`*deref`), never default.** The schema
> declares `SignalArrived *deref Input`; the emitter emits the one-line `impl Deref { fn deref(&self)
> -> &Target { self.payload() } }` from a fixed template. This deletes the 24-impl wall *and*
> honestly records the transparent-wrapper intent in the schema, where it belongs. d3r2's "newtype
> Deref … by default" is the one line of the recorded direction this report recommends refining: the
> *capability* is standard and template-generated, but *applying* it is per-newtype intent, because
> the real code proves 88% of newtypes reject it.

### (b) Cross-type ergonomic impls (`PartialEq<&str>`, `Display`) — conditional on inner kind.

These need the *inner* type's trait (`String: Display`, `str: PartialEq`). They are safe and
desirable **exactly when the inner is a known scalar**, and unprovable otherwise. The emitter already
does precisely this: `StandardNewtypeImplTokens` gates every cross-type impl on `scalar_like()`. A
schema-type-wrapping newtype gets none, because the emitter cannot know the inner schema type
implements `Display` (it may not).

> **Recommendation: generate conditionally on inner kind — and flip the gate ON by default.** For
> scalar-backed newtypes, `Display` / `PartialEq<scalar>` / `PartialOrd<scalar>` / `AsRef<str>` are
> unambiguously safe (the inner scalar always implements them) and match hand-written code
> byte-for-byte. Skip them for every non-scalar inner. The conditionality is *structural* (the inner
> `TypeReference` discriminant), so this stays inside the shape-derived model — it is not a leaf
> allowlist. The single judgement call: `PartialEq<&str>` exposes the wrapper to string comparison —
> appropriate for identifier/name/path newtypes, which is what all 18 scalar newtypes are. Safe to
> default.

### (c) `as_str` / std-leaf methods — `AsRef<str>` template, NOT a leaf list. Avoid `as_str` entirely.

The adversarial pass (661/4) and operator finding 2 are right: a std-leaf method allowlist
(`as_str`, `trim`, `to_lowercase`, `chars`, `wrapping_add`) has an arbitrary boundary — `trim` is
structurally identical to `as_str` and only a human typing the list keeps it out. The real code
confirms the danger from the other side: `trim` appears **9 times** in `signal-spirit/src/lib.rs`,
every single one *inside* a business-logic validator (`self.payload().trim().is_empty()` at lines
206/218/239/243/274/286/317/326), **never** as a standalone delegating method. A leaf allowlist that
admitted `trim` would invite generating a method that should never exist as a primitive.

`as_str` itself: the three hand-written `as_str` methods (`ConfigurationPath`,
`SpiritGuardianProviderName`, `SpiritGuardianModelName`, lines 26-40) are all string-backed newtypes.
The standard-impl `AsRef<str>` already covers their use ergonomically (`.as_ref()` for `&str`), and
`Display` covers stringification. The remaining call sites that literally need `.as_str()`
(`self.agent_socket_path.payload().as_str()`) are *composition inside hand-written methods*, not
standalone `as_str` impls to generate.

> **Recommendation: per-trait newtype templates (route b), no std-leaf allowlist at all.** Provide
> `AsRef<str>` (string) and `AsRef<Path>` (path) from fixed templates — these *are* the principled
> way to reach a scalar leaf, because `AsRef` is the std contract for "view me as this leaf." Do NOT
> add a named `as_str` method (it duplicates `AsRef<str>` + `Display`). If a future case genuinely
> needs a free-standing `.as_str()` returning `&str` and `AsRef`/`Deref` won't serve, add it as a
> *single explicitly-named* exception keyed to string-backed newtypes — but the recommendation is to
> not need it. Pure-schema-first means scalar leaves are reached through std *traits* (`AsRef`,
> `Display`), never through a curated method-name registry.

One unsolved sub-case worth flagging: **nested-newtype scalar transitivity.** `Statement(StatementText)`
where `StatementText(String)` has a hand-written `PartialEq<&str>` body `self.payload().payload()`
(double hop, `lib.rs:1075`). `Statement`'s inner is a *schema type*, so the scalar gate skips it
today — yet it is transitively scalar. Two options: (1) compute the *transitive* scalar leaf by
following single-field newtype chains during lowering, so `Statement` is recognized as scalar-backed
at depth 2; or (2) require the `*deref`-style intent. Recommend option (1) — it is structural
(follow the chain, terminate at the first scalar or non-newtype) and deletes the remaining
hand-written scalar delegations without a marker.

### (d) The minimal DEFAULT standard-impl set per shape that is unambiguously safe.

"Unambiguously safe" = cannot produce wrong code, cannot leak an unintended capability, matches
hand-written output. Per shape:

| Shape | Unconditional default | Conditional default (on inner kind) |
|---|---|---|
| **Newtype** (any inner) | `new`, `payload`, `into_payload`, `From<Inner>` | — |
| **Newtype** (scalar inner, incl. transitive) | + | `Display`, `AsRef<str\|Path>`, `PartialEq<scalar>`, `PartialOrd<scalar>` (int/ord scalars) |
| **Enum** | `route` (already emitted), `is_<variant>`, `as_<variant>` (`Option<&payload>`) | `From<payload>` per *uniquely-typed* single-payload variant |
| **Struct** | per-field accessor `fn <field>(&self) -> &T`, `into_<field>` | `with_<field>` per `Optional` field; `From<T>` iff exactly one field |
| **All types** | `#[derive(Clone, Debug, Eq, PartialEq, Hash)]` (left to derive, see below) | — |

Everything in the "unconditional" column is provable from structure alone and can never be wrong.
The "conditional" column is gated on a structural discriminant (inner scalar kind, variant payload
uniqueness, field optionality) — still shape-derived, not a curated list.

## The four-bucket default policy (the answer to "conditionality + default")

### Bucket 1 — Default-ON, unconditional (the inherent surface)

`new`, `payload`, `into_payload`, `From<Inner>` (newtype); `route`, `is_/as_<variant>`, variant
constructors (enum); field accessors + `into_<field>` (struct). **Rationale:** derivable from shape
with zero knowledge of inner traits; the constructor/accessor surface every consumer needs; cannot be
wrong. Newtype + enum legs already emit. Add struct accessors and enum `is_/as_`. No marker, no flag.

### Bucket 2 — Default-ON, conditional on a structural discriminant

`Display`/`AsRef`/`PartialEq<scalar>`/`PartialOrd<scalar>` for scalar-backed (and transitively
scalar-backed) newtypes; `with_<optional>` withers; single-field `From`; unique-payload variant
`From`. **Rationale:** safe and matching hand-written code *whenever* the discriminant holds, skipped
otherwise — the condition is computed from the schema, not chosen by a human. **Action: flip
`standard_newtype_impls` to default-ON** (it is built and tested; the only reason it is off is that it
was landed as a demonstration). Add the transitive-scalar computation for nested newtypes.

### Bucket 3 — Opt-in marker (intent, not structure)

`Deref` (the `*deref` newtype marker). **Rationale:** 189 vs 24 proves it is per-newtype intent;
defaulting it on breaks 165 abstractions; defaulting it off and forcing hand-writing keeps the
24-impl wall. A marker is the honest middle: the *template* is standard, *applying* it is declared.
This is the one place a marker earns its keep.

### Bucket 4 — Leave to `#[derive]`, and Bucket 5 — Avoid

- **Leave to derive:** `Clone`, `Debug`, `Eq`, `PartialEq<Self>`, `Hash`, plus the `rkyv` +
  `NotaEncode`/`NotaDecode` derives the schema already attaches. Never hand-emit these as impl
  blocks — `#[derive]` is the standard, smaller, and correct path; emitting them by hand would
  duplicate and risk divergence.
- **Avoid entirely:** a broad std-leaf method allowlist (`trim`, `to_lowercase`, `chars`, `iter`,
  `wrapping_add`, bare `as_str`). The real code uses these *only* inside business-logic validators,
  never as delegating primitives; generating them invites methods that should not exist. Scalar
  leaves are reached via `AsRef`/`Display`/`Deref`(marked), which are principled std *traits*.

## Why this satisfies pure-schema-first and the discipline rules

- **Pure-schema-first:** every default capability is computed from `(shape, inner-kind)`; the only
  std reach is through std *traits* keyed to a structural discriminant (`AsRef<str>` iff scalar),
  which is shape-derived, not a method-name registry. No broad std allowlist exists.
- **Methods on data-bearing types only:** all generated impls are `impl <Type>` or trait impls on the
  emitted noun; the emitters (`NewtypeInherentImplTokens`, `RouteMatchArm`, the new struct/enum
  emitters) already obey this — no free functions, no ZST namespaces.
- **Typed errors not panics:** the unresolved-capability edge and the currently-`panic!`-ing
  unsupported-impl cases (operator finding 1) both become `SchemaError`.
- **Full-word identifiers:** `payload`/`into_payload`/`reference`/`receiver_shape` — no abbreviations.

## Open questions for the psyche

1. **The `*deref` marker, confirm the call (question a).** d3r2's recorded text says "newtype Deref …
   by default"; the 189-vs-24 data says default-on would break 165 abstractions. I recommend
   *refining* d3r2 to "Deref capability is standard and template-generated, applied per-newtype via a
   `*deref` marker." Is that the intended reading, or do you want Deref genuinely blanket-on (and the
   24→189 expansion of transparent wrappers accepted as a consequence)?

2. **Flip `standard_newtype_impls` to default-ON.** It is built, tested green, and skips non-scalar
   newtypes safely. Confirm I should change the default (and remove the opt-in flag), regenerate the
   spirit/signal-spirit artifacts, and delete the now-redundant hand-written scalar `Display`/
   `PartialEq`/`as_str` impls in the same slice.

3. **Nested-newtype transitive scalar (question c sub-case).** Recommend computing the transitive
   scalar leaf so `Statement(StatementText(String))` gets scalar standard impls automatically
   (deletes `self.payload().payload()` hand-impls). Agree, or keep depth-2 wrappers opaque by default?

4. **`as_str` exception.** I recommend *zero* named std-leaf methods — `AsRef<str>` + `Display`
   cover every current use. Confirm you do not want a generated `.as_str()` method (it would be the
   one named std-leaf exception d3r2 leaves open; I argue it is unnecessary).

## Landing slices (operator owns code-repo main)

1. Lift name-only resolution to shape-derived `Capability` resolution; extend
   `SchemaError::UnresolvedComposition` with `receiver_shape`; convert the unsupported-impl
   `panic!`/`assert!` to typed `SchemaError` (operator finding 1).
2. Flip `standard_newtype_impls` default-ON; add transitive-scalar; regenerate spirit/signal-spirit;
   delete redundant hand-written scalar impls. (Bucket 2.)
3. Add the `*deref` newtype marker + `Deref` template; mark the ~24 wrappers; delete the Deref wall.
   (Bucket 3.)
4. Add struct field-accessor + enum `is_/as_` emitters. (Bucket 1 completion.)
5. Then the composition-body slices (661 slices 3-5): `VariantMatch` with discard, ownership-aware
   projection — the variant-isomorphism class a template cannot express.
