# Help as a dual-codec value — the schema-codec spec for operator

*schema-designer · report 5 · closes the help-shape thread: make the help
data a truly-typed value with **two** codecs — rkyv (binary) and schema
(text, via `schema-next`) — that both **encode and decode**, like every
other signal type. (Filename keeps the `-nota-` slug; the codec is
schema-next's, with NOTA as the block substrate beneath it.)*

## What we want (affirmative)

The help is **one truly-typed value carrying two serializations**, not a
string the client prints:

- **rkyv** — binary, present everywhere, encode↔decode.
- **schema** — text, on the text clients, encode↔decode through the
  **schema declaration codec** (`schema-next`). NOTA is the block
  substrate beneath schema-next; the help round-trips at the **schema**
  layer, not the raw-NOTA layer.

Both directions, round-trippable. And the text codec is the **same
schema-decode that generated the model** — the help is schema, so it is
encoded and decoded as schema, end to end.

## Where it stands

| Codec | State |
|---|---|
| rkyv | **Done.** `HelpModel`/`HelpResponse`/`HelpEntry`/`HelpBody`/`HelpTypeExpression` derive `Archive/Serialize/Deserialize`; operator's test round-trips both the model and the rendered response in binary. |
| schema (text) | **A discipline violation to remove.** The text is built by a hand-written `impl Display` (`render_with_name` → `format!`) — a **hand-rolled encoder**, forbidden by the same rule as hand-rolled parsers: serialization goes through the typed codec, never by hand. It must be replaced by the schema codec, not improved. (A `Display` is legitimate only if it delegates to the codec.) |

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

The hand-written `Display` happens to produce this shape (it switches on
the `HelpBody` variant and picks the delimiter) — useful only as a
*specification* of what the schema encoder must emit. Doing it by hand-
rolled `format!` is itself forbidden; producing the declaration form is
the schema encoder's job, and there is no inverse at all.

And the right codec is **schema-next**, not a hand-rolled `nota_next`
one: the `{ }` / `[ ]` / `(Vec X)` body grammar is the schema declaration
grammar `schema-next` already decodes (`from_schema_text`).
Re-implementing it as a bespoke `nota_next` `NotaDecode` would duplicate
the schema decoder. **Decode the help as schema.**

## (b) The spec — make it a true dual-codec type (rkyv + schema)

1. **Encode through `schema-next`'s declaration encoder.** The help node
   is a (re-headed) schema declaration; render it with schema-next's
   declaration encoding (`to_schema_text`, already used for the
   Stream/Family fallback — extend it to every body), so the help text
   **is** the canonical schema declaration form. **Delete the hand-`format!`
   `Display`** — it is a forbidden hand-rolled encoder; the only allowed
   `Display` delegates to the schema codec.
2. **Decode through `schema-next`'s declaration decoder** — the same
   grammar `from_schema_text` uses to build the model. The `{ }` / `[ ]`
   / `(Vec X)` body is schema, so schema-next parses it straight back into
   the typed help node — no hand-rolled delimiter dispatch, no parallel
   codec. This likely needs a small public entry point in `schema-next`
   for decoding a single (re-headed) declaration; that is the one new
   surface to add.
3. **Keep the rkyv derives** unchanged — the binary codec.
4. **Stream/Family (report 4 follow-up)** round-trips through the same
   schema codec — a stream is already a schema form (`Stream { … }`), so
   schema-decode handles it and the last `Text(String)` escape hatch
   closes; *every* node becomes a true typed value.

Net: the help is a genuine **dual-codec value — rkyv (binary) + schema
(text)** — encode and decode both ways, with NOTA as the shared block
substrate beneath the schema layer. `(Help X)` output parses back into the
typed help node via the *same schema decoder that generated it*. That is
the "truly-typed representation, encoded/decoded in rkyv or schema" we
want, made concrete.

## Why schema, not a raw-NOTA codec

The help node is, structurally, a **re-headed schema declaration**
(`Record` re-headed over `RecordRequest`'s `{ Entry Justification }`
body). Its text form is the grammar `schema-next` already encodes
(`to_schema_text`) and decodes (`from_schema_text`) — so the codec is
**schema-next's, not a bespoke `nota_next` `NotaEncode`/`NotaDecode`**.
This keeps the whole feature **schema end to end**: the model is generated
by schema-decoding the contract, and the help output is itself schema,
decoded by the same schema decoder. NOTA stays the block substrate
beneath; nothing re-implements the declaration grammar. (Per psyche:
decode in schema, not nota.)
