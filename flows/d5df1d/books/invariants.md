<!-- to-the-living:start -->
Presentation.{ «Ethos invariants» }

# Ethos invariants

## Where things stand

Vision asks a good deal of an ethos file. The generator, Ethos Zero, holds some of it and lets the rest through. The audit read the generator's main line, the one in use; no development branch carries these invariants.

The picture: what vision asks of a file at the top, then the file's path through the generator, with what each stage holds and what it lets pass.

```
   what vision asks of an ethos file
   ---------------------------------
   one of four roots, sections in order
   a struct of two or more positions
   no new type wrapping a new type
   a comment on every layered line,
     beside it or above it, lined up
   each element on a new indented line
   inline until too deep
   every trait written in ethos
                 |
                 v
         +---------------+
         |  the reader   |
         +---------------+
   refuses: a wrong root, a version,
     a constraint on a data type,
     a concrete type in a trait input
   lets through: a one-position struct,
     a double wrap, any layout,
     a file with no comment
                 |
         +-------+--------+
         |                |
         v                v
   +-----------+    +-----------+
   | generation|    | the print |
   +-----------+    +-----------+
   Rust, datom      every comment
   derives,         dropped;
   assertions       elements hung
                    beside the opener
```

Two subjects sit outside this book. The special representation, a trait for a custom datom encoding, is the Core Secondary's work. Type, new type and alias have their own book.

## The invariants and the generator today

Origin of the grades: this flow's audit of the generator. "Probe" means the generator was run on a test file and its answer seen; "read" means the enforcing code was read. Its test suite passes (run on Prometheus by the Ethos Secondary, flows/1d0733/reports, 2026-10-09).

| Invariant | Record | Generator today |
|---|---|---|
| Four roots, sections in fixed order | vision-ethos | enforced (read, tests) |
| No version in a file | vision-ethos | enforced (read) |
| Sweet form made canonical before reading | vision-ethos | enforced (read, test) |
| Names fully qualified, no imports in Rust | vision-ethos | enforced (probe) |
| Fields named after their types | vision-ethos | enforced (probe) |
| Inline payload named with an underscore | vision-ethos | partly: a clash with a derived name is refused; an authored underscore name is accepted (probe) |
| Every struct and enum bears both datom traits | vision-ethos | enforced (read, probe) |
| Datom traits compiled only where text is spoken | vision-ethos | enforced (read, tests) |
| A trait input names a trait, not a concrete type | vision-ethos | enforced (read, tests) |
| A data type carries no constraint | vision-ethos | enforced (read, tests) |
| An association asserts at compile time | vision-ethos | enforced (probe) |
| A struct of one position is refused | flows/8e9e77/vision/single-field-structs.md, 2026-09-08; flows/ebbe30/vision/ethos.md, 2026-10-09 | not enforced (probe) |
| No double wrapping | flows/d4ae97/vision/ethos.md, 2026-10-06 | not enforced (probe) |
| A comment on every section and layered line | vision-ethos | not enforced (probe); the print drops every comment (read) |
| A comment beside or above, lined up | flows/e5a0bc/vision/ethos.md, 2026-10-06 and 2026-10-07 | not enforced; comments are dropped |
| Each element on a new indented line | flows/e5a0bc/vision/ethos.md, 2026-10-06 and 2026-10-07; flows/d4ae97/vision/ethos.md, 2026-10-06 | not enforced (probe); the print hangs elements beside the opener (read) |
| Inline until too deep; an algorithm decides | flows/d4ae97/vision/ethos.md, 2026-10-06 | not enforced; no algorithm stated (probe: six levels accepted) |
| Traits named as qualities | vision-ethos | not enforced (read) |
| Every trait written in ethos | flows/d4ae97/vision/ethos.md, 2026-10-07 | not met: the generator's own code holds about 95 hand-written traits (read) |
| The golden ethos is the ethos of ethos | flows/ebbe30/vision/ethos.md, 2026-10-09 | not met: the language's own anatomy is hand-written Rust (read) |
| A memory trait carries its upgrade per version | vision-ethos | not implemented (read) |
| A Mutex field | flows/ebbe30/vision/ethos.md, 2026-10-09 | not expressible (probe, flows/1d0733/reports/mutex-probe.md, 2026-10-09) |

Probes marked in the table above are witnessed on a Nix build of the audited revision on Prometheus: the generator runs were rerun and all matched the audit's initial readings (flows/1d0733/reports/probes-rerun.md, 2026-10-09).

## Proposal 1: a struct of one position is refused

For your ruling now. The proposals after it await their turn.

Target: psyche-skills/skills/vision-ethos.md. A new section lands between «Shapes and placement» and «Kinds are explicit; bodies are hand-written». The file as it stands around the landing:

Above — «Shapes and placement» ends with its Signal example, then its Rust; below — the heading «Kinds are explicit; bodies are hand-written» and its first paragraph: "A kind is declared, never inferred; an association asserts the type bears it."

Lines removed: none.

Lines added, a section heading and its text:

**## What ethos refuses**

The generator refuses a file that breaks one of these rules, and the refusal names the place.

A struct holds two or more positions; a struct of one is refused. A type that holds one other type is written as its name, a dot and that type.

In the example, Library is the root that holds shared types; its four brackets are imports, types, kinds and associations. `Age.{ Integer }` is a struct, Age, of one position, an Integer; `Age.Integer` is Age written as the Integer it holds.

```
; refused: a struct of one position
Library
[]                      ; imports
[ Age.{ Integer } ]     ; types
[]                      ; kinds
[]                      ; associations

; accepted: the type it holds, after a dot
Library
[]                      ; imports
[ Age.Integer ]         ; types
[]                      ; kinds
[]                      ; associations
```

Ruling: land, amend, or refuse.

## Proposal 2: no double wrapping (awaiting its turn)

Target: psyche-skills/skills/vision-ethos.md, in the section «What ethos refuses» that Proposal 1 makes, after its single-field rule.

Lines removed: none.

Lines added:

A type written as a name, a dot and one type never names another such type; it names what it holds. `FlowId.String` is a flow's id; a `Job.FlowId` beside it wraps a wrap, and is refused: where a job is a flow id, it is written FlowId.

```
; refused: Job wraps FlowId, which wraps String
Library
[]                    ; imports
[                     ; types
  FlowId.String       ; a flow's id
  Job.FlowId ]        ; a wrap of a wrap
[]                    ; kinds
[]                    ; associations

; accepted: a flow id is named a flow id
Library
[]                    ; imports
[ FlowId.String ]     ; types: a flow's id
[]                    ; kinds
[]                    ; associations
```

Ruling: land, amend, or refuse.

## Proposal 3: the print keeps every comment (awaiting its turn)

Target: psyche-skills/skills/vision-ethos.md, section «Spacing», which stands whole as:

Space the delimiters and the inner content. Ethos follows the canonical protos print: a space inside every bracket and brace at both ends when non-empty.

Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.

Ethos carries a comment on every section and on every line that has a next layer, saying in plain words what the machine reads there; a comment runs from ; to the end of the line.

Lines removed: none.

Line added, after the comment paragraph:

The canonical print keeps every comment, at the element it was written on.

Ruling: land, amend, or refuse.

## Proposal 4: each element on a new indented line (awaiting its turn)

Target: psyche-skills/skills/vision-ethos.md, section «Spacing», shown whole under Proposal 3.

Line removed:

Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.

Lines added:

Ethos expands vertically: a structure with more than one element opens its delimiter, and each element starts on a new line, indented one level beneath the line that opened it; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line. A vector of short items may hold several on a line up to a width, each wrapped line aligned with the first item.

A comment sits beside the element it is on, or on the line above it, lined up with that element.

In the example, Voice is a struct of two positions: Aspect, an enum declared in place, and Topic, a String.

```
Library
[]                      ; imports
[                       ; types
  Voice.{               ; where a flow speaks from
    Aspect.[            ; its aspect
      Psyche
      Mind
      Field ]
    Topic.String } ]    ; what it works on
[]                      ; kinds
[]                      ; associations
```

Ruling: land, amend, or refuse.

## Proposal 5: implementers report what ethos cannot express (awaiting its turn)

Target: field-skills/skills/compensation-behavior.md. The rule already stands there, a paragraph of its own after the rule that a design or report carries the thing as it now is:

An implementer who meets something hard to express in ethos — a mutex, an exception, any need the language seems not to carry — reports it to the living as its own finding rather than working around it.

Lines removed: none. Lines added: none.

Ruling: keep as it stands, or amend.

## Proposal 6: the derive's real name (awaiting its turn)

Target: psyche-skills/skills/vision-ethos.md. The generator derives `Composing`, the datom trait that reads a datom; `Compositional` is the trait beneath it, which that derive supplies. The skill names `Compositional` in its derives and in two sentences.

This lands after the trait rename of «The golden ethos», third edition, Ruling 2, since both touch the derive lines.

Each of the eleven derive lines, in «What a declaration turns into», «Inline types», «A variant named as a defined type carries that type», «A variant may declare its payload inline», «Kinds are explicit; bodies are hand-written» and «Kind syntax»:

```diff
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
```

In «Every declared type bears both kinds», its first sentence. Removed: "Ethos Zero emits `Datomizable` and `Compositional` on every struct and enum it generates". Added: "Ethos Zero emits `Datomizable` and `Composing` on every struct and enum it generates".

In the same section's example, the line under the two alias lines. Removed: `#[derive(Datomizable, Compositional)]        // a type: always derived`. Added:

```rust
// a type: always derived
#[derive(Datomizable, Composing)]
```

In «The datom kinds are compiled in only where text is spoken», its first sentence. Removed: "A generated signal library bears `Datomizable` and `Compositional` conditionally". Added: "A generated signal library bears `Datomizable` and `Composing` conditionally".

In the same section's example, under the comment "emitted by Ethos Zero into the signal crate". Removed: `#[cfg_attr(feature = "datom", derive(Datomizable, Compositional))]`. Added:

```rust
#[cfg_attr(feature = "datom",
    derive(Datomizable, Composing))]
```

Ruling: land, amend, or refuse.

## Forks for your ruling

### Fork 1: how deep a type is declared inline

The skill says inline nesting goes about three deep. The record of 2026-10-06 (flows/d4ae97/vision/ethos.md) makes inline mandatory unless a type is too deep, with an algorithm to decide. The generator checks neither: six levels pass. Example, a lock rejection whose payload nests four deep:

```
Library
[]                        ; imports
[                         ; types
  Rejection.[             ; why a lock is refused
    Overlap.{             ; a held lock and a claim
      Lock.{              ; the lock held
        Owner.{           ; who holds it
          FlowId.String
          Since.Integer }
        Path.String }
      Claim.String } ] ]  ; the path claimed
[]                        ; kinds
[]                        ; associations
```

Options: (a) a fixed depth, three, past which the type is named apart and the generator refuses it inline; (b) a width: a type is named apart when inline it would run past the line width; (c) a fixed depth as the rule and a width as the reason, both stated; (d) another rule.

### Fork 2: who holds layout and comments

The print can rewrite any layout into the canonical one and could keep comments; the reader could also refuse a file. Example: a file with `[ Lock.{ LockId LockName } ]` on one line and no comment on it.

Options: (a) the reader refuses it: the layout is wrong and the comment is missing; (b) the reader refuses the missing comment, and the print fixes the layout; (c) the reader accepts both, and the print fixes the layout and keeps what comments there are; (d) another split.

### Fork 3: a Mutex field in ethos

Example: a Nexus holding its live flows behind a lock, a struct with a field of `Mutex<Vector<Flow>>`. Measured on the generator (flows/1d0733/reports/mutex-probe.md, 2026-10-09): an import names one segment as its source, so no accepted form reaches the standard library's Mutex; the path it emits does not compile; with the path fixed by hand, every derive ethos attaches but Debug fails on a Mutex field, the datom traits among them; ethos has no way to give a declaration fewer derives.

Options: (a) ethos expresses a Mutex field: imports of more than one segment, and a declaration that carries fewer derives; (b) shared mutable state stays outside ethos, in hand-written Rust, and implementers report each case under Proposal 5; (c) another form.
<!-- to-the-living:end -->
