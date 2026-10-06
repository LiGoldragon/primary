<!-- to-the-living:start -->
Presentation.{ «Ethos: inline, layout, expansion» }

## 0. Why the Rust

Nothing in ethos is broken. Flows reach for the generated Rust because the ethos files on disk are unreadable: signal-flow's wire ethos is one line of 3,000 characters, Flow has no Memory root compiled, and the writer that prints ethos has no width and no comment column. The three proposals below make the ethos file the thing to read. The code book's next edition shows every type in ethos.

## 1. Inline declaration, and the algorithm

Rule: a type used once is declared where it is used, unless the declaration would reach past the third level. A type used twice is declared once, named. The generator refuses the other way round in either case: a named type that the rule inlines, or an inline type the rule names, is an error.

The algorithm, in ethos's own terms:

```
Depth.[ Leaf                 ; 0: String, Integer, a name
        Composite.Integer ]  ; 1 + the deepest element
Place.{ Type
        Level.Integer }      ; nesting from the root's element
Verdict.[ Inline             ; used once and
                             ;   level + depth ≤ 3
          Named              ; used twice, or too deep
          Error.[ NamedButInline
                  InlineButNamed ] ]
```

Bad, as signal-flow writes it today:

```
LaunchRequestId.String
SourcePath.String
SourceSha256.String
LaunchSource.{ SourcePath
               SourceSha256 }
LaunchProfile.{ LaunchRequestId
                Vector<LaunchSource>
                ... }
```

Good, by the rule:

```
LaunchProfile.{
  RequestId.String
  Sources.Vector<Source.{
    Path.String
    Sha256.String }>
  ... }
```

## 2. Layout: the new-line style and the comment column

Rule: a structure with a next layer opens on its line and its elements begin on the next line, indented two; elements align; the closer ends the last element's line. Comments in one block share one column, two past the widest element; when fewer than twenty columns remain, the comment goes on its own line above the element, at the element's indentation. A vector of leaves fills the width and wraps aligned with its first item. The width is the file's: 80 in a repository, 38 in a book.

Bad, the same-line style:

```
Launch.{ Voice.{ Aspect Layer }  ; who
         Brief.String }          ; what
```

Good:

```
Launch.{
  Voice.{          ; who runs it
    Aspect
    Layer }
  Brief.String }   ; what it does
```

Where it lands: protos `src/rendering.rs:111-128` decides a hanging layout only by whether an element is layered; it gains the width, the comment column and the wrap. `Check.src` of ethos-zero refuses a file with a line over its width, so the one-line files are rewritten once by `Generate` and never come back.

## 3. One position is a new type

`Name.Type` is a type of its own. ethos-zero `src/generation.rs:886` emits an alias:

```rust
quote! {
  #[rustfmt::skip]
  pub type #name #parameters
    = #aliased;
}
```

Replaced by a newtype with the derives every type has:

```rust
quote! {
  #[rustfmt::skip]
  #[derive(datom_codec::Datomizable,
           datom_codec::Composing)]
  pub struct #name #parameters(
    pub #aliased);
}
```

Its datom is its one position's datom, no braces: `FlowId.Integer` is written `918df4`.

## 4. Expansion: `@path` before structure

A datom text may hold `@path`; each is replaced by the text of the file it names before any structure is read; a file is checked balanced before it is spliced; a cycle is an error. datom-codec `src/core.rs:462-469` reads the text straight into protos:

```rust
let protos = self
  .text
  .protosize_with(&mut budget.reader)
  .map_err(|error| Error {
    layer: ErrorLayer::Protos,
    path: Path::new(),
    kind: ErrorKind::Structural(error),
  })?;
```

Replaced by the expansion first:

```rust
let expanded = self
  .text
  .expand(&self.origin,
          &mut budget.expansion)?;
let protos = expanded
  .protosize_with(&mut budget.reader)
  .map_err(|error| Error {
    layer: ErrorLayer::Protos,
    path: Path::new(),
    kind: ErrorKind::Structural(error),
  })?;
```

The kinds, in ethos:

```
Expanding.{ expand.{
  Self Origin Expansion } }
  ; text with @paths → text with none
Dereferencing.{ dereference.{
  Self ReferencePath Origin } }
  ; a path → the text it names,
  ; beside the file holding it
Balancing.{ balanced.Self }
  ; protos's delimiter check
```

`Resolving` is taken in ethos-zero for name resolution, so the path kind is `Dereferencing`.

## Rulings

1. The inline rule and its algorithm, section 1: yes, or amend.
2. The layout rule, section 2: yes, or amend. The file width: (a) 80. (b) your number.
3. One position is a newtype, its datom unbraced: yes, or amend.
4. Expansion before structure, each file checked balanced: yes, or amend.
5. Where a skill repository's contents come from: (a) its own `index.datom`, read by `@`. (b) directory discovery, as your 2026-08-21 word on the manifest.
6. Resolution: (a) beside the file holding the reference; the inline CLI argument from the caller's directory; an absolute path as written. (b) absolute only.
7. A content pin on a reference, for a reproducible deploy: (a) not now. (b) design it.
8. Writing an expanded value back into its files: (a) not designed; output is the expanded value. (b) design it.
9. The kinds, with `Dereferencing` for the path: yes, or amend.
<!-- to-the-living:end -->
