# 5 — NOTA syntax exception audit

## 0 · Summary

The audit found two concrete codec exceptions that reused PascalCase
variant notation for non-enum data:

| Surface | Old form | Corrected form |
|---|---|---|
| `BTreeMap<K, V>` / `HashMap<K, V>` | `[(Entry key value)]` | `[(key value)]` |
| Rust tuples `(A, B, ...)` | `(Tuple a b ...)` | `[a b ...]` |

Both old forms were wrong for the same reason: `(Entry ...)` and
`(Tuple ...)` are data-carrying enum variants under the three-case
PascalCase rule. They cannot also mean map entry or tuple.

I changed `nota-codec` so maps use untagged pair records and tuples use
sequence form. `cargo test` and `nix flake check` pass.

## 1 · What The Audit Checked

The audit searched `nota-codec` for the protocol methods that introduce
syntax shapes:

| Method | Meaning |
|---|---|
| `start_record(name)` | Writes `(VariantName ... )`; legal only for data-carrying enum variants |
| `start_record_untagged()` | Writes `(fields...)`; legal for structs / schema-position records |
| `write_pascal_identifier(name)` | Writes bare unit variant |
| `start_seq()` | Writes `[elements...]`; legal for sequence-shaped containers |

The important question for every hard-coded PascalCase head was:

What enum owns this variant?

`Some`, `True`, and `False` have clean answers. `Entry` and `Tuple` did
not.

## 2 · Fixed Offenders

### Maps

The old map blanket impl encoded every entry with a fake `Entry` tag:

```nota
[(Entry alpha 1) (Entry beta 2)]
```

That is a vector of data-carrying enum values. It is not a map.

The corrected form is:

```nota
[(alpha 1) (beta 2)]
```

The element position supplies the pair schema: first field is key,
second field is value. No PascalCase head is introduced.

### Tuples

The old tuple blanket impl encoded tuples with a fake `Tuple` tag:

```nota
(Tuple 1 2)
```

That is a data-carrying enum variant named `Tuple`. It is not a tuple.

The corrected form is:

```nota
[1 2]
```

The schema position distinguishes fixed-length tuple decode from
variable-length vector decode.

## 3 · Surfaces That Are Not Offenders

`Option<T>` is clean:

```nota
None
(Some value)
```

`None` and `Some` are real variants of the `Option` enum.

`bool` is clean:

```nota
True
False
```

Those are the correct user-facing names for a two-member enum. Rust's
lowercase backend spelling is not a NOTA exception.

`NotaEnum` data-carrying variants are clean:

```nota
(NixBuilder (Some 8))
TailnetClient
```

The PascalCase heads are real variants of the surrounding Rust enum.

## 4 · Remaining Suspect

The one remaining surface worth a separate design decision is bare
`Path`.

Today `nota-codec::Path` accepts a wider bare token alphabet than
`String`, allowing values like:

```nota
skills/operator.md
./foo
/etc/hosts
```

That is not the same class of bug as `Entry` and `Tuple`: it does not
reuse enum notation. But it is explicitly documented as a carve-out in
`nota/README.md`, and the new rule is “no exceptions.” It needs a
designer-level answer:

| Option | Consequence |
|---|---|
| Keep bare `Path` | Treat it as a distinct lexical literal class, not an exception |
| Remove bare `Path` | Paths always quote as strings; less ergonomic, fewer token classes |
| Rename the concept | If bare path is first-class syntax, make the grammar say so directly |

I did not change `Path` in this pass because it is a grammar-level
question, not a clear hard-coded fake enum tag.

## 5 · Verification

`nota-codec`:

```text
cargo test
nix flake check
```

Both passed after the map and tuple changes.
