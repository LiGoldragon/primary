# 413 — Schema strict positional open questions

## Short Answer

The strict parser patch is mechanically green. The biggest remaining
risks are design edges it intentionally exposed:

- how much syntax expressivity belongs in `field.Type`
- whether metadata structural macros also leave key/value syntax
- how to sequence the downstream repo break
- whether schema should keep any hidden/private helper concept
- whether source-codec and macro-engine diagnostics should be unified

## Biggest Concerns

### 1. Composite Field Roles Are Awkward

The strict grammar currently supports:

```nota
Entry { marker.DatabaseMarker }
Entry { Topic }
Entry { (Vector Topic) }
Topics (Vector Topic)
Entry { Topics }
```

It does not support a direct role name over a composite reference:

```nota
Entry { topics.(Vector Topic) }
Entry { by_topic.(Map Topic RecordIdentifier) }
```

So a component author must either accept a derived field name from the
reference shape, or declare a named wrapper type first.

Spirit record `i3p0` closes one edge: it does not support redundant
explicit roles:

```nota
Entry { topic.Topic }
```

That is now an error because the role `topic` is exactly the derived
field name for `Topic`; the author should write:

```nota
Entry { Topic }
```

Best question:

Should the schema language have a direct explicit-role form for
composite references, or is the intended style always to name the
domain type first?

### 2. Scalar Field Policy Is a Real Design Decision

I rejected bare scalar fields inside struct bodies:

```nota
Entry { String }
Entry { Integer }
```

That was necessary to make `Record { Topic String }` reject reliably.
The accepted forms are now:

```nota
Text String
Entry { Text }

Entry { text.String }
```

Best question:

Do we want scalar fields to always have semantic names, or should there
be a different unambiguous scalar shorthand?

### 3. Metadata Macros Still Use Key/Value Bodies

These are still accepted because they are not ordinary struct bodies:

```nota
Family { record Entry table entries key Domain }
Stream { token SubscriptionToken opened Receipt event Event close SubscriptionToken }
```

That may be fine: they are structural macro configuration objects, not
schema structs. But it is also a visible exception to "NOTA records are
positional, not labeled."

Best question:

Is the key/value retirement limited to schema struct bodies, or should
metadata macro payloads also become positional/schema-defined records?

### 4. Inline Private Helpers Are Gone

The old syntax could invent private helper types from inside a struct
field. The strict grammar removes that. Helpers must now be declared in
the namespace.

This is simpler and more visible, but it loses compactness and changes
the public/private story.

Best question:

Do we need explicit visibility in schema source, or is every declared
helper now public until a later module/export system exists?

### 5. Two Parser Front Doors Must Stay Locked Together

I closed both:

- source-codec path: `src/source.rs`
- macro expansion path: `src/declarative.rs`

The tests prove both are strict now. But this is an ongoing risk: future
macro work could accidentally reintroduce pair acceptance through a new
struct-field macro.

Best question:

Should strict positional struct-field parsing become one shared parser
object used by both front doors, instead of mirrored logic?

### 6. Diagnostics Are Not Yet Beautiful

Direct parser failures return `RetiredStructFieldSyntax`.

Source structural variant decode failures can wrap that as:

```text
MalformedSchemaNode { found: "... retired struct field syntax ..." }
```

That is acceptable for tests, but not ideal for a language users will
write directly.

Best question:

Should retired syntax errors preserve typed structure through
source-codec decoding, instead of being wrapped in a generic malformed
node error?

### 7. Rollout Will Break Many Repos At Once

The scan found 52 likely `.schema` files still using old patterns across
the workspace. That is expected under the no-backcompat rule, but it
means strict `schema-next` mainline will force a coordinated port of
contract repos and codegen consumers.

Best question:

Do we land strict schema-next first and let consumers fail loudly, or do
we make a coordinated stack branch that ports schema-next,
schema-rust-next, and the major component contracts together?

## My Lean

My lean is:

1. Keep the current strict parser behavior.
2. Decide composite explicit-role syntax before porting every contract.
3. Treat metadata macros as a separate design question, not silently as
   an exception.
4. Port `schema-rust-next` next, because it is the generator consumer
   and has the highest fixture count.
5. Then port signal/meta-signal contracts component by component.

The one decision I would ask for first is the composite-role form. If
you want `topics.(Vector Topic)` or another delimiter form, it should be
settled before we rewrite all the component schemas.
