# "Field name = type name": how far it goes, where it breaks, why it's sound

Your aski instinct — use the type's name as the field's name everywhere, for
extreme type-strictness — maps directly onto a mechanism already in these
schemas (`*`), and the codebase already holds both the win and the one genuine
counterexample. Here is exactly where it works, where it can't, and what it
really is.

## You're already doing it — that's what `*` is

In `spirit-min.schema`:

```
Entry { Topics * Kind * Description * Magnitude * }
```

Every field there is `<TypeName> *`, and `*` lowers to *"the type of the same
name as the field"* (`TypeReference::from_name(field_name)`). So `Topics *` is a
field named `topics` of type `Topics`. **That is field-name = type-name.** It
already works for the four fields of `Entry` because their four types
(`Topics`, `Kind`, `Description`, `Magnitude`) are all distinct.

So the question "would it be a problem to do `TypeReference *` everywhere" is
really: *when can a field's name be left implicit as its type?*

## The one hard rule

A record's field names must be distinct. If field name = type name, then:

> **A record may use `Type *` for a field only if no other field in that record
> has the same type.**

It breaks exactly when a record needs **two fields of the same type**.

## The counterexample is live in `root.schema`

```
TypeReferencePair { key TypeReference value TypeReference }
```

`key` and `value` are **both** `TypeReference`. You cannot write
`{ TypeReference TypeReference }` — two fields named `typeReference` collide. The
role-names `key` / `value` are doing real work: they distinguish two values of
the *same type* by their *position/meaning*. This is the irreducible case.

So for the four declarations you quoted:

| Declaration | `Type *` work? | Why |
|---|---|---|
| `FieldDeclaration { Name * reference TypeReference }` | **Yes** → `{ Name TypeReference }` | `Name` and `TypeReference` are distinct types |
| `NewtypeDeclaration { Name * reference TypeReference }` | **Yes** | distinct types |
| `ImportDeclaration { Name * source TypeReference }` | **Yes, but…** | works mechanically, but `source` *means* "where the import comes from" — a role the bare type doesn't carry |
| `Payload [Unit (Carries TypeReference)]` | n/a | it's a variant payload, not a struct field — already nameless |

## Two tiers: must-name vs may-name

The `source` row shows there are actually two reasons to keep a role-name:

1. **Must name (hard):** two fields share a type → collision (`key`/`value`).
2. **May name (soft):** the field's *role* carries meaning its *type* doesn't.
   `source: TypeReference` tells you "origin of the import"; `typeReference`
   would lose that. No collision, but a real readability/intent call.

Field-name = type-name is ideal precisely when **the type fully captures the
role** — which, under a newtype discipline, is most of the time.

## Why it's sound: role = type (the newtype discipline makes it compose)

The deep reason your aski idea holds up: in this workspace **every distinct
domain value is already its own newtype** (a hard rule). `Topic`, `Description`,
`RecordIdentifier` are all `String`/`Integer` underneath but are *distinct
types*. So "two fields of the same type" almost never arises legitimately — if
two fields are truly the same type they're the same role; if they're different
roles they should be different types:

```
;; not this — two String fields would collide and lose meaning
Person { firstName String lastName String }
;; this — roles ARE types, and field-name = type-name falls out for free
FirstName String
LastName  String
Person { FirstName * LastName * }
```

So "I had to invent a field name" becomes a signal: *you were probably missing a
newtype.* The discipline you reached for in aski and the newtype discipline here
are the same discipline seen from two ends — and they reinforce each other.

The only case that survives the newtype defense is the **symmetric homogeneous
pair**: `key`/`value`, `x`/`y`, `from`/`to`, `min`/`max`. There the two roles
are the *same kind of thing in symmetric positions*; newtyping them
(`MapKey(TypeReference)`, `MapValue(TypeReference)`) is real ceremony, so naming
the positions — or having a dedicated `Pair` primitive — is the honest choice.

## What it really is

A record where every field is named by its type is a **type-indexed product**:
an (at most) one-of-each-type set, projected *by type* rather than by an
arbitrary label. Almost no mainstream language commits to this — records
everywhere allow many fields of one type and lean on labels. Making the label a
*function of the type* is genuinely stricter, and it has real payoffs:

- no naming decisions, no `profileSize`-vs-`size` bikeshedding;
- the schema collapses to a pure graph of types;
- a rename propagates by type;
- "can I even name this?" becomes a type-design question, caught early.

One honest nuance against full type-indexed semantics: **NOTA records are
positional**, so today this is "a positional list of types whose names are
derived," not order-independent projection-by-type. Order still drives decode.
That's a smaller simplification than the full idea, but it points the same way.

## The mechanism's own limit

`*` specifically only expresses a **single declared name** — it becomes
`from_name(field_name)`. It cannot stand in for a composite type like
`(Vector Topic)` or `(Optional T)` (there is no single type-name to borrow). The
discipline handles this the way `spirit-min` does: **alias the composite first**,
then `*` it —

```
Topics (Vector Topic)        ;; name the composite
Entry  { Topics * … }        ;; now the field can borrow that name
```

So composites don't break the idea; they just ask you to name the shape once.

## Recommendation

The idea is sound and already half-adopted. A coherent direction:

- **Default to `Type *`** wherever the type's name fully captures the field's role
  (which the newtype discipline makes the common case).
- **Keep an explicit role-name only for** (a) two fields of the same type
  (`key`/`value` — forced), or (b) a role whose meaning the type genuinely
  doesn't carry (`source`).
- **Treat "I need a field name" as a prompt** to ask whether a newtype is
  missing.

If you want this as a standing principle for the workspace's languages, it's a
clean, recordable one — say the word and I'll capture it in the intent log
(it would sharpen, not duplicate, the existing newtype rule).
