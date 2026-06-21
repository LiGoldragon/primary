# Help as a dual-codec value — the NOTA spec for operator

*schema-designer · report 5 · closes the help-shape thread: make the help
data a truly-typed value with **two** codecs — rkyv (binary) and NOTA
(text) — that both **encode and decode**, like every other signal type.*

## What we want (affirmative)

The help is **one truly-typed value carrying two serializations**, not a
string the client prints:

- **rkyv** — binary, present everywhere, encode↔decode.
- **NOTA** — text, on the nota-text clients, encode↔decode.

Both directions, round-trippable, the same dual-codec shape every signal
type already has. The help isn't special-cased; it's a normal contract
value that happens to describe the contract.

## Where it stands

| Codec | State |
|---|---|
| rkyv | **Done.** `HelpModel`/`HelpResponse`/`HelpEntry`/`HelpBody`/`HelpTypeExpression` derive `Archive/Serialize/Deserialize`; operator's test round-trips both the model and the rendered response in binary. |
| NOTA | **Half.** The text comes from a hand-written `impl Display` (`render_with_name` → `format!`) — a one-way projection. No `NotaEncode`/`NotaDecode`, so nothing parses the help text back, and the canonical-NOTA guarantees come from getting `format!` right by hand rather than from the codec. |

## (a) Verification — does deriving the NOTA codec reproduce the syntax?

**No.** Proven empirically (`/tmp/nota-help-probe`, `nota-next` derive on
help-shaped types):

```
want:          (Record { Entry Justification })
naive derive:  (Record (Struct [Entry Justification]))      round-trips = true
want:          (RecordAccepted RecordIdentifier)
naive derive:  (RecordAccepted (Reference RecordIdentifier))
```

The standard `nota_next` derive encodes a **struct as an untagged
positional record** `(a b)` and an **enum variant as a tagged paren form**
`(Variant payload)`. So a `HelpEntry { name, body: HelpBody::Struct(..) }`
becomes `(Record (Struct [Entry Justification]))` — it **leaks the
`HelpBody` discriminant** (`Struct`/`Reference`/`Enumeration`) and parens-
wraps it. It is a valid round-tripping codec — just the wrong surface.

The help syntax is the schema **declaration grammar**
(`skills/structural-forms.md`), where the **delimiter is the
discriminant**, no tag:

| HelpBody kind | help syntax | discriminant |
|---|---|---|
| `Struct` | `(Head { A B })` | brace `{ }` |
| `Enumeration` | `(Head [A B])` | bracket `[ ]` |
| `Reference` / newtype | `(Head Ref)` | bare atom / application |
| `Unit` | `(Head)` | empty |

The hand-written `Display` already produces exactly this (it switches on
the `HelpBody` variant and picks the delimiter). So the encode logic is
right; it just isn't wired to the codec, and there is no inverse.

## (b) The spec — make it a true dual-codec type

1. **`NotaEncode` for the help node = the current `render` logic,
   promoted to the canonical encoder.** Move `render_with_name` /
   `HelpTypeExpression::render` into `impl NotaEncode for HelpEntry` (and
   the sub-types), so `to_nota()` *is* the help text. Keep a `Display`
   that delegates to `to_nota()`. No behavior change to the output.
2. **Add the inverse `NotaDecode`** — recover the `HelpBody` kind from the
   **delimiter** of the body block, using the `nota_next` `Block` /
   `Delimiter` API the request recognizer already uses
   (`as_delimited(Delimiter::Brace | Bracket | Parenthesis)`,
   `demote_to_string`): brace → `Struct`, bracket → `Enumeration`,
   atom/application → `Reference`, empty → `Unit`. The leaf
   `HelpTypeExpression` parses the container heads (`Vec`/`Optional`/`Map`)
   back to its kinds. Now `(Record { Entry Justification })` **parses back**
   into the typed `HelpEntry`.
3. **Keep the rkyv derives** unchanged. The value now has both codecs.
4. **Stream/Family (report 4 follow-up)** gets the same treatment: the
   typed `Frame` variant encodes its named slots as a brace body and
   decodes back — so the one remaining `Text(String)` escape hatch closes
   and *every* node is a true typed value.

Net: `(Help X)` output becomes a genuine NOTA value — `to_nota()` emits
`(Record { Entry Justification })`, `from_nota` parses it back — and the
help travels as rkyv binary anywhere and as NOTA text on the nota clients,
encode and decode both ways. That is the "truly-typed representation,
encodable/decodable in rkyv or nota" we want, made concrete.

## Note — relation to schema-next's declaration codec

The help node is, structurally, a **re-headed schema declaration** (`Record`
re-headed over `RecordRequest`'s `{ Entry Justification }` body). So its
NOTA form is the same grammar `schema-next` already encodes
(`to_schema_text`) and decodes (`from_schema_text`). Two ways to realize
the codec: (1) a self-contained `NotaEncode`/`NotaDecode` on the help types
(above — fewest moving parts, no new cross-crate coupling), or (2) reuse
`schema-next`'s declaration codec directly. Recommend (1) for the pilot;
(2) is the deeper unification if the help node is later expressed as an
actual declaration value. Operator's call.
