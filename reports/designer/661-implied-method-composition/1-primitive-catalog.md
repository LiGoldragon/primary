# 661/1 — The implied-primitive catalog (the building blocks)

The methods *producible from a schema shape alone* — the building blocks a composed body may
call. Grounded in the live emitter (`schema-rust-next/src/lib.rs`) and real usage.

## The ground-truth finding (load-bearing)

Before cataloging what *could* be implied, the survey established what the emitter *actually
emits* today — and the answer reframes "implemented by default":

- **Named-field structs get NO inherent impl.** `RustStructTokens::to_tokens`
  (`schema-rust-next/src/lib.rs:3766`) emits only the struct definition with public fields.
  No `new`, no accessors, no withers, no `From`. "Reading a field" on an emitted struct is a
  direct `self.field` access, not a getter. So every struct primitive below is a *candidate*,
  hand-written today in spirit/triad-runtime/signal-spirit.
- **Newtypes are the one shape that already emits an inherent impl.**
  `NewtypeInherentImplTokens` (`lib.rs:1957-1995`) emits `new`, `payload(&self) -> &Inner`,
  `into_payload(self) -> Inner`, and `From<Inner>`. Plus the single `Deref` body the
  code-is-data interpreter already drives (`reaction-expand/src/schema.rs:1090`).

So "standardize and implement by default" is *partly already true* (newtypes), *mostly not
yet* (structs, enums beyond the variant tag). The composition idea rides on top of whichever
primitives the shape emits.

## The vocabulary, by shape

### Struct (named-field record)

| Primitive | Signature | Derivation | Emitted? |
|---|---|---|---|
| field accessor | `fn <field>(&self) -> &<T>` | one per field; `&self.<field>`; by-value for `Copy` | candidate |
| owned projection | `fn into_<field>(self) -> <T>` | by-value sibling; `self.<field>` | candidate |
| all-fields constructor | `fn new(<f0>: T0, …) -> Self` | one param per field in order; `Self { … }` | candidate |
| required+optional `new` | `fn new(<required…>) -> Self` | params = non-`Optional` fields; optionals → `None` | candidate |
| wither | `fn with_<field>(mut self, <T>) -> Self` | one per `Optional` field; `self.<f> = Some(arg); self` | candidate |
| `From<single-field>` | `impl From<T> for S` | only when exactly one field; `Self::new(payload)` | candidate |
| mutable accessor | `fn <field>_mut(&mut self) -> &mut <T>` | `&mut self.<field>` | candidate |

### Newtype (single-field tuple — the degenerate struct)

`payload(&self) -> &Inner`, `into_payload(self) -> Inner`, `new`, `From<Inner>`, `Deref`.
**All already emitted** — this is the only fully-standardized shape today.

### Enum

per-variant constructor (`Input::signal_arrived(x)`); `is_<variant>` predicate;
`as_<variant>`/`try_<variant>` projection (`Option<&payload>`); `From<payload>` per
single-payload variant; `into_<variant>`; a total variant `route`/re-wrap. These are
candidates — emitted enums today carry only the type definition + codec.

### Expanded reaction-frame enum (`Input`/`Output`)

The inter-enum lift `From<Input> for Output` via `Continue`; payload projection across legs;
the leg constructors; the recursive `Continue` leg. (The `656`/`660` expansion path.)

### Conversion / codec

rkyv encode/decode, nota encode/decode, the round-trip (already emitted); cross-type
`From`-chains (the `StoredRecord -> StampedEntry -> Entry` migration pattern).

## The key category: composed (not a new primitive)

The catalog's most important entry is **not** a primitive — it is the *composition* the whole
model targets. The most common hand-written struct method is a **field-projection accessor**:
read a field, then call that field type's own implied primitive, optionally lifted through
`Option`:

```
signal-spirit/src/lib.rs:72   self.agent_socket_path.payload().as_str()
                              ↑ field read   ↑ newtype payload()   ↑ String as_str()
signal-spirit/src/lib.rs:132  self.meta_socket_path.as_ref().map(ConfigurationPath::as_str)
                              ↑ Optional lift
```

Every call in the first line resolves to an implied primitive, so the whole body is — in
principle — generatable. This is the first proof that *composed* bodies stay inside the
closure, and it is the bridge from "implied primitives" to "compose them." It is also exactly
where the closure's boundary gets interesting (see `3` and `4`): `as_str` is a `String`
method, not a schema-shape method — the composition reaches *outside* the schema, and that is
the crack the adversarial pass found.
