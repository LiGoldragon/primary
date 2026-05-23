# 27 — NOTA mixed-enum support

Proposal for collapsing `NotaSum` and `NotaEnum` into one unified
derive that handles every enum variant shape per the three-case rule,
including enums that mix unit variants with data-carrying variants.
The current split is psyche-rejected (`intent/nota.nota` 2026-05-20
16:30) as a wrong-shape compromise: *"the current design is totally
fucking insane — making all code contort itself to save a little bit
of encode-decode computation for a format that doesn't even exist
inside the system (inter-component is all pure-binary signal)."*

## 0 · TL;DR

One derive — call it `NotaEnum` (subsuming `NotaSum`) — handles
every variant shape:

```rust
#[derive(NotaEnum)]
pub enum NodeService {
    TailnetClient,                        // unit          → wire: TailnetClient
    TailnetController,                    // unit          → wire: TailnetController
    NixBuilder { maximum_jobs: Option<u32> },   // struct  → wire: (NixBuilder None)
    NixCache,                             // unit          → wire: NixCache
    PersonaDevelopment { capabilities: Vec<PersonaDevelopmentCapability> },
                                          // struct        → wire: (PersonaDevelopment [...])
}
```

Encoder per variant: unit → bare `VariantName`; newtype/struct →
`(VariantName fields…)`. Decoder peeks the next token — if `(`,
dispatch to the data-carrying arm by tag; else dispatch to the
unit arm by bare tag. Total derive change: ~40 lines. Total codec
change: one new `peek_is_open_paren()` helper (~5 lines). Existing
`NotaSum`-only and `NotaEnum`-only code keeps working unchanged
because the new derive produces the same wire form for those
homogeneous cases.

## 1 · Why the current split is the wrong shape

NOTA's three-case rule already says all three cases coexist in
one grammar:

1. `(VariantName fields…)` — data-carrying variant.
2. `(fields…)` — struct (no leading PascalCase, schema position
   determines type).
3. Bare `VariantName` — unit variant.

The grammar is one rule with three cases. The derive split
artificially partitions Rust enums by which case they use —
NotaSum claims case 1 exclusively; NotaEnum claims case 3
exclusively. Mixed enums become impossible at the type system
level even though the grammar handles them fine.

The forcing function the split creates: an author who wants
`NodeService::TailnetClient` (no config) and `NodeService::NixBuilder { … }`
(with config) in one enum has three choices, all bad:

- **Use empty-struct variants** (`TailnetClient {}`) to satisfy
  NotaSum's all-data-carrying rule. Wire form: `(TailnetClient)`.
  Reads as "data-carrying variant with no data" — a contradiction
  the three-case rule rules out.
- **Split into two enums** (`NodeRoleUnit` + `NodeRoleConfigured`)
  plus a parent struct holding both vectors. The Rust shape now
  carries an artificial type-system boundary the domain doesn't
  have.
- **Make every variant data-carrying** by wrapping in newtypes
  (`TailnetClient(())`). Worse than option (a).

The cost-benefit per the psyche's framing: NOTA exists for human
authoring (cluster data, intent logs, skill files, configuration,
fixtures). Inter-component IPC inside the system is pure binary
signal — NOTA never crosses the wire between daemons. The codec
runs at the human-authoring boundary, infrequently. Optimising
codec simplicity at the expense of every Rust enum's natural shape
is the wrong direction. Pay the codec-complexity cost once,
inside the codec; let every author write the natural Rust enum.

## 2 · The unified derive — wire shape per variant

```rust
#[derive(NotaEnum)]
pub enum X {
    Unit,                          // wire: Unit
    Newtype(Inner),                // wire: (Newtype <inner>)
    Struct { f: u32, g: String },  // wire: (Struct 42 "hello")
}
```

Encoding per variant shape (matches the existing per-derive
behavior; just unified):

| Variant shape | Encode |
|---|---|
| `Foo` (unit) | `Foo` (bare PascalCase) |
| `Foo(Inner)` (newtype) | `(Foo <inner-encoded>)` |
| `Foo { a, b, c }` (struct) | `(Foo <a> <b> <c>)` (positional) |

Decoding by peek-then-dispatch:

```text
peek next token
├── Token::LParen        → data-carrying variant
│                          consume `(`
│                          read PascalCase variant tag
│                          dispatch to (newtype | struct) arm by tag
│                          expect `)`
└── Token::Ident(name)   → unit variant
    (name is PascalCase)   read bare PascalCase
                           dispatch to unit arm by tag
```

The decoder already has one-token lookahead via the `pushback`
queue (`decoder.rs:17`). No new lexer/parser primitives needed —
just one `peek_is_open_paren()` helper alongside the existing
`peek_is_record_end()`, `peek_is_explicit_none()`,
`peek_is_seq_end()`.

## 3 · Concrete codec change

### 3.1 · `nota-codec/src/decoder.rs` — one new helper

```rust
/// Returns true if the next token is `(` — used by enum
/// decoders to dispatch between unit-variant (no `(`) and
/// data-carrying-variant (with `(`) shapes.
pub fn peek_is_open_paren(&mut self) -> Result<bool> {
    let token = self.next_token()?;
    let is_paren = matches!(&token, Token::LParen);
    self.pushback.push_front(token);
    Ok(is_paren)
}
```

Mirrors the shape of the four existing peek helpers. ~5 lines.

### 3.2 · `nota-derive/src/nota_enum.rs` — replace with unified expand

```rust
pub fn expand(input: DeriveInput) -> TokenStream {
    let name = &input.ident;
    let name_string = name.to_string();

    let variants = match &input.data {
        Data::Enum(DataEnum { variants, .. }) => variants,
        _ => panic!("NotaEnum can only be derived for enums"),
    };

    let mut unit_encode_arms = Vec::new();
    let mut unit_decode_arms = Vec::new();
    let mut paren_encode_arms = Vec::new();
    let mut paren_decode_arms = Vec::new();

    for variant in variants {
        let variant_ident = &variant.ident;
        let variant_string = variant_ident.to_string();
        match &variant.fields {
            Fields::Unit => {
                unit_encode_arms.push(quote! {
                    Self::#variant_ident => encoder.write_pascal_identifier(#variant_string),
                });
                unit_decode_arms.push(quote! {
                    #variant_string => Ok(Self::#variant_ident),
                });
            }
            Fields::Unnamed(unnamed) if unnamed.unnamed.len() == 1 => {
                let payload_type = &unnamed.unnamed.first().unwrap().ty;
                paren_encode_arms.push(quote! {
                    Self::#variant_ident(value) => {
                        encoder.start_record(#variant_string)?;
                        value.encode(encoder)?;
                        encoder.end_record()
                    }
                });
                paren_decode_arms.push(quote! {
                    #variant_string => {
                        let value = <#payload_type as ::nota_codec::NotaDecode>::decode(decoder)?;
                        decoder.expect_record_end()?;
                        Ok(Self::#variant_ident(value))
                    }
                });
            }
            Fields::Named(named) => {
                /* same as today's NotaSum struct-variant path,
                   minus the inner expect_record_head call (the
                   unified decoder already consumed `(` + tag)   */
            }
            _ => panic!("..."),
        }
    }

    quote! {
        impl ::nota_codec::NotaEncode for #name {
            fn encode(&self, encoder: &mut ::nota_codec::Encoder) -> ::nota_codec::Result<()> {
                match self {
                    #(#unit_encode_arms)*
                    #(#paren_encode_arms)*
                }
            }
        }
        impl ::nota_codec::NotaDecode for #name {
            fn decode(decoder: &mut ::nota_codec::Decoder<'_>) -> ::nota_codec::Result<Self> {
                if decoder.peek_is_open_paren()? {
                    decoder.expect_record_start()?;
                    let tag = decoder.read_pascal_identifier()?;
                    match tag.as_str() {
                        #(#paren_decode_arms)*
                        other => Err(::nota_codec::Error::UnknownVariant {
                            enum_name: #name_string,
                            got: other.to_string(),
                        }),
                    }
                } else {
                    let tag = decoder.read_pascal_identifier()?;
                    match tag.as_str() {
                        #(#unit_decode_arms)*
                        other => Err(::nota_codec::Error::UnknownVariant {
                            enum_name: #name_string,
                            got: other.to_string(),
                        }),
                    }
                }
            }
        }
    }
}
```

Total: ~40 lines, structurally a merge of today's `nota_enum.rs`
(unit arm) and `nota_sum.rs` (data-carrying arm).

### 3.3 · Retirements

- `NotaSum` derive retires — `NotaEnum` covers its surface.
- `NotaSum`'s panic on unit variants retires.
- `nota-derive/src/nota_enum.rs:19` panic on data-carrying variants
  retires.
- All `#[derive(NotaSum)]` uses across the workspace become
  `#[derive(NotaEnum)]` in one mechanical pass (sed).

Per ESSENCE *"Backward compatibility is not a constraint"* — clean
break; no transitional shape. The `NotaSum` name disappears.

## 4 · What changes in the existing tree

### 4.1 · `horizon-rs/lib/src/proposal/services.rs` — natural rewrite

Current (forced into empty-struct variants by NotaSum):

```rust
#[derive(NotaSum)]
pub enum NodeService {
    TailnetClient {},
    TailnetController {},
    NixBuilder { maximum_jobs: Option<u32> },
    NixCache {},
    PersonaDevelopment { capabilities: Vec<PersonaDevelopmentCapability> },
}
```

After (natural Rust shape):

```rust
#[derive(NotaEnum)]
pub enum NodeService {
    TailnetClient,
    TailnetController,
    NixBuilder { maximum_jobs: Option<u32> },
    NixCache,
    PersonaDevelopment { capabilities: Vec<PersonaDevelopmentCapability> },
}
```

`{}` retire on the unit cases. Wire form for those cases changes
from `(TailnetClient)` to bare `TailnetClient`. Same change applies
to `PersonaDevelopmentCapability` if it has the same pattern.

### 4.2 · `goldragon/datom.nota` — migration sed

Existing data (`datom.nota:80-85, 121-124, 156-158`):

```nota
[
  (TailnetClient)
  (TailnetController)
  (NixBuilder None)
  (PersonaDevelopment [(GitoliteServer)])
]
```

After migration:

```nota
[
  TailnetClient
  TailnetController
  (NixBuilder None)
  (PersonaDevelopment [GitoliteServer])
]
```

`(TailnetClient)` → `TailnetClient`; `(NixCache)` → `NixCache`;
`(GitoliteServer)` → `GitoliteServer`; data-carrying variants
(`(NixBuilder None)`, `(PersonaDevelopment …)`) unchanged. Same
sed across any other NOTA file that wrote `(VariantName)` for a
unit-shaped variant.

### 4.3 · Cluster data also gets simpler for the four bare booleans

Tied to the §8.1 question in `reports/system-assistant/26`:
with mixed-enum support, the cleanest fold for `nordvpn`,
`wifi_cert`, `wants_printing`, `wants_hw_video_accel` becomes
"extend services" (option (a) from /26 §8.1) because nothing
forces the author to choose between unit-only services
(TailnetClient) and configured services (NixBuilder { … }) — both
shapes coexist in one enum:

```rust
#[derive(NotaEnum)]
pub enum NodeService {
    TailnetClient,
    TailnetController,
    NixBuilder { maximum_jobs: Option<u32> },
    NixCache,
    PersonaDevelopment { capabilities: Vec<PersonaDevelopmentCapability> },

    Nordvpn,                                       // unit
    WifiCert { cert_reference: SecretReference },  // struct
    Printing,                                      // unit
    HwVideoAccel { decoder: Option<DecoderHint> }, // struct
}
```

Cluster data reads naturally:

```nota
services: [
  TailnetClient
  (NixBuilder None)
  NixCache
  Nordvpn
  Printing
]
```

## 5 · Alternatives considered

| Alternative | Verdict |
|---|---|
| Keep current split; teach authors to "pick the right derive" | Wrong shape. The constraint is artificial; authors write contorted Rust to fit codec's preference. Psyche-rejected. |
| Detect empty-struct variants in NotaSum and emit bare form | Codec hides the unit-vs-struct distinction. Authors keep writing `TailnetClient {}` — the type system stays contorted. Half-fix. |
| Split into two enums per concern | Forces an artificial Rust-side boundary. Cluster data reads less naturally (two vectors instead of one). |
| **One unified derive** | Aligns Rust shape with grammar shape per the three-case rule. Codec change is small; derive change is mechanical merge of two existing paths. Wins. |

## 6 · What stays settled

The three-case rule from `intent/nota.nota` 2026-05-19 21:00 is
unchanged — and in fact reinforced. Mixed-enum support is the
straightforward application of that rule across one Rust enum
type. The grammar already supports it; only the derive partition
was blocking.

The `NotaRecord` derive (case 2: structs, no PascalCase tag) and
the `NotaTransparent` derive (newtype wrappers) keep their roles.
Only `NotaSum` collapses into `NotaEnum`.

## 7 · Open questions for the psyche

### 7.1 · Derive name

`NotaEnum` is the natural name once `NotaSum` retires (the type
is an enum; the derive says so). Alternatives:

- Keep `NotaEnum` (recommended — shortest, matches Rust vocabulary).
- Rename to `NotaVariant` (emphasises the variant-shape coverage).
- Keep both names as aliases during a transition (rejected per
  no-transitional-shapes).

### 7.2 · Migration sweep — automated or manual

Two known data files need the `(VariantName)` → `VariantName`
rewrite for unit cases:

- `goldragon/datom.nota` (lines 80-85, 121-124, 156-158)
- any other NOTA file using `(SomeUnitVariant)` form

A small Rust tool (read NOTA file, identify zero-field
parenthesized records whose tag matches a known unit variant,
rewrite to bare form) could automate it. Or a careful manual
sweep. The migration is small enough that manual is fine; the
question is whether the psyche wants a permanent migration tool.

### 7.3 · Bool / Option

`Bool` is `True | False` (NotaEnum-style, no data). Unchanged.

`Option<T>` is `None` (unit) + `Some(T)` (data-carrying) — which is
exactly the mixed-enum case the new derive supports. `Option<T>`
becomes the canonical example of mixed-enum NOTA. (Today
`Option<T>` is hand-coded in the codec; under the new shape it
could be derived if `Option` had `#[derive(NotaEnum)]`. Not
load-bearing — Option is fundamental enough to stay hand-coded —
but worth noting as semantic alignment.)

## 8 · Sequence to land

The work is small and self-contained; the only sequencing concern
is keeping existing users compiling while the derive change is in
flight. Two natural orderings:

- **Single-commit cutover**: add `peek_is_open_paren`, replace
  `nota_enum.rs` with unified expand, remove `nota_sum.rs`, sweep
  workspace `#[derive(NotaSum)]` → `#[derive(NotaEnum)]`, sweep
  data files in one PR. Risky for concurrent agents but clean.
- **Two-commit cutover**: (1) add `peek_is_open_paren` + the new
  unified `NotaEnum` expand alongside `NotaSum` (both work);
  (2) sweep callers + delete `NotaSum`. Easier to land
  concurrently with other in-flight work.

Operator-lane call; agent-territory per
`intent/workspace.nota` 2026-05-19T15:35Z (no bureaucratic
sequencing for the psyche).

## 9 · Reading list

- `intent/nota.nota` 2026-05-20 16:30 — the Correction +
  Principle that triggered this report.
- `intent/nota.nota` 2026-05-19 21:00 — the three-case rule (the
  grammar this proposal aligns the type system to).
- `nota-derive/src/nota_enum.rs` — current unit-only derive
  (62 lines).
- `nota-derive/src/nota_sum.rs` — current all-data-carrying
  derive (124 lines), including the panic at line 90 that this
  proposal retires.
- `nota-codec/src/decoder.rs` — `pushback` queue at line 17 and
  the four existing `peek_is_*` helpers (lines 240, 250, 287,
  301) — the codec already has the lookahead primitive this
  proposal builds on.
- `nota/README.md` lines 83-101 — the three-case rule in the
  spec.
- `reports/system-assistant/26-lean-rewrite-shape-analysis.md` §8.1
  — the boolean-field shape question that gets a cleaner answer
  under mixed-enum support.
- `horizon-rs/lib/src/proposal/services.rs` — the `NodeService`
  enum that retires its empty-struct workaround under this
  proposal.
