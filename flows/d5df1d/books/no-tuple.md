<!-- to-the-living:start -->
Presentation.{ «No tuple, and FlowId» }

## The new type meets the tuple rule

In ethos the declaration is `FlowId.String`: a
new type named `FlowId` over the plain value
`String`. That line is what you see, and it stays
as it is whichever way this is ruled.

```
FlowId.String  ; FlowId, a new type over String
```

The vision of ethos says, in lines 467–468: no
tuple in the code we design, save at a contact
point that requires one. The new type you ruled
for a plain value is emitted, in the development
set that turns ethos-zero's aliases into new
types (not in production), as one Rust line:

```rust
pub struct FlowId(pub String);
```

That is a tuple struct of one position. The rule
and the emission meet, and one of them gives way.
Whether the value inside is public is the open
Fork 4 of «Types»; reading (2) below settles it
in the same ruling.

```
+------------------------------------+
| ethos: FlowId.String               |
| (unchanged in either reading)      |
+------------------------------------+
                  |
                  v
+------------------------------------+
| Rust today, development set:       |
| pub struct FlowId(pub String);     |
| a tuple of one position            |
+------------------------------------+
                  |
                  v
+------------------------------------+
| vision lines 467-468:              |
| no tuple in the code we design     |
+------------------------------------+
          |                 |
          v                 v
+-----------------+ +-----------------+
| (1) rule gains  | | (2) emission    |
| one exception:  | | gains a named   |
| the new type    | | field:          |
| stays a tuple   | | { pub string }  |
+-----------------+ +-----------------+
```

## Distillation

### D1. No tuple, and the new type

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill, lines 467–468, after the
Interactions paragraph and before "## Spacing".

Above, unchanged:

```text
Interactions — the term for trait implementations — use the type
itself in all cases.
```

**Reading (1).** A new type over a plain value is
the one tuple the rule allows; the lines gain that
sentence. Fork 4 of «Types» stays open.

Removed:

```text
No tuple in the code we design; if some parts require it (standard
traits, dependencies), then it is allowed at that contact point only.
```

Added, prose:

```text
No tuple in the code we design, save the new type: a new type over a
plain value, `FlowId.String`, is the one-position tuple struct
`FlowId(String)`. Where other parts require a tuple (standard traits,
dependencies), it is allowed at that contact point only.
```

**Reading (2).** A new type is emitted with a
named field, and the rule stands as it is. The set
changes its emission from the tuple to:

```rust
pub struct FlowId { pub string: String }
```

The lines stay, unchanged:

```text
No tuple in the code we design; if some parts require it (standard
traits, dependencies), then it is allowed at that contact point only.
```

Reading (2) also answers Fork 4 of «Types»: the
inner value is a named public field, so one ruling
settles both.

Below, unchanged:

```text
## Spacing
```

Distils flows/d4ae97/vision/ethos.md, 2026-10-06
(the new type of «Types» Proposal 1),
and the tension found in
flows/d5df1d/reports/ethos-test-judgement.md.

**Ruling D1.** (1) The new type is the allowed
tuple. (2) The new type takes a named field.
Or amend, by line.
<!-- to-the-living:end -->
