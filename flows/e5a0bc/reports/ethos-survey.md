# Ethos survey: datom file expansion and three syntax changes

A read-only survey for implementing (a) datom file expansion (`@path` reference
splicing before structure is read) and (b) three ethos syntax changes:
mandatory inline type declaration up to an algorithm-decided depth; a one-position
`Name.Type` becoming a new type; and a line-breaking rule.

Each section keeps **Observed** (read in the source, with path, lines and
excerpt) apart from **Hypothesis** (where a change would go, not yet tried).
Nothing was built or run.

## 0. Where things live

Repository root (SKILL_VARIABLES.md): `/git`. All three crates are under
`/git/github.com/LiGoldragon/`. Each checkout is detached at the commit
`origin/main` points to (fetched 2026-10-06):

| crate | path | HEAD | Cargo version |
|---|---|---|---|
| ethos-zero | `/git/github.com/LiGoldragon/ethos-zero` | c2653dd (2026-10-03) | 16.0.0 |
| protos | `/git/github.com/LiGoldragon/protos` | 15b41da (2026-10-02) | 0.32.2 |
| datom-codec | `/git/github.com/LiGoldragon/datom-codec` | 4dff16b (2026-10-02) | 0.32.2 |

`/git/github.com/LiGoldragon/datom` is a second clone of the same
`git@github.com:LiGoldragon/datom-codec.git` remote at the same commit. It is not
a separate crate.

Related, not surveyed in depth: `tree-sitter-ethos` (a second ethos grammar,
`grammar.js`, last commit 7440ccf 2026-08-13), `ethos-engine`, `protos-engine`.

## 1. The ethos grammar as parsed today

The reading pipeline is documented at
`ethos-zero/src/lib.rs:8-13`:

```
| Text, as written (the sweet form) | `String` | [`Canonicalizable`] | [`Canonical`] |
| Text, canonical (the braced form) | [`Canonical`] | `protos::Protosizable` | `protos::Protos` |
| Structure | `protos::Protos` | [`Ethosizable`]<[`File`]> | [`File`], checked whole |
| Concept | [`File`] | [`Generating`] | Rust text, or a whole-file error |
```

The pipeline runs in `ethos-zero/src/actualization.rs:13-26` (canonicalize, then
`canonical.text.protosize()`, then `protos.ethosize()`).

### 1.1 The four roots

Observed. `ethos-zero/src/lib.rs:145-154` declares `pub enum File { Library(Library), Signal(Signal), Operation(Operation), Memory(Memory) }`.
Roots are identified in `conception.rs:84-96`. A retired head goes through
`Root::successor`, which maps `Sema` to `Memory` (`lib.rs:682-690`). The section
counts are read in `conception.rs`:

- Library: 4 sections, `[ imports ] [ types ] [ kinds ] [ associations ]` (`conception.rs:305-317`).
- Signal: 4, `[ imports ] [ queries ] [ responses ] [ types ]` (`:319-337`).
- Operation: 4, `[ imports ] [ operations ] [ outcomes ] [ types ]` (`:339-357`).
- Memory: 2, `[ imports ] [ types ]` (`:359-369`).

The sweet form (root head, then the sections as siblings) becomes the braced form
in `canonicalization.rs:14-68`. The conversion skips leading blank lines and `;`
lines, takes the first whitespace-delimited run as the head, and inserts `.{`
after it plus `\n}` at the end. It records a `seam`, and `Resituating` maps
extents back across that seam (`:71-98`).

### 1.2 How a type declaration is parsed

Observed. `conception.rs:445-477`:

```rust
let Protos::Headed { head, constraints, separator: Separator::Period, body, .. } = self
...
if constraints.is_some() { return Err(... Problem::Expected(Form::Declaration)) }
...
if let Some(p) = body.children(Enclosure::Braced) {
    Ok(TypeDeclaration::Struct(identity, p.positions().place(1)?))
} else if let Some(v) = body.children(Enclosure::Bracketed) {
    Ok(TypeDeclaration::Enum(identity, v.variants().place(1)?))
} else {
    Ok(TypeDeclaration::Alias(identity, body.conceive().place(1)?))
}
```

The concept is `TypeDeclaration { Struct(Identity, Vec<Position>), Enum(Identity, Vec<Variant>), Alias(Identity, Reference) }` (`lib.rs:277-286`).
Variants are `Bare | Typed(Name, Reference) | Struct(Name, Vec<Position>) | Enum(Name, Vec<Variant>)` (`lib.rs:288-299`), read in `conception.rs:479-501`.

### 1.3 Is an inline struct/enum inside a field accepted today?

Observed: yes. A struct position is `Position::Referenced(Reference) | Position::Declared(TypeDeclaration)` (`lib.rs:267-275`).
`conception.rs:189-217` treats any `Headed` node with a `Period` separator inside
a struct's braces as a declaration in place:

```rust
let declared = matches!(node, Protos::Headed { separator: Separator::Period, .. });
if declared {
    values.push(Position::Declared(node.declared(arguments, index)?));
```

Because `declared` recurses through `TypeDeclaration`, nested declarations in
place are accepted at any depth. Test `ethos-zero/tests/ethos.rs:104-125` reads
`Memory [] [ Flow.{ Integer Brief.String State.[ Running Ended ] Capsule.{ Home.String Login.Vector<String> } } ]`.
It asserts `pub enum State {`, `pub struct Capsule {`,
`pub type Login = std::vec::Vec<String>;` and `pub capsule: Capsule`.

A declaration in place is hoisted into the file namespace
(`sectioning.rs:530-629`, `Hoisting::declarations` and `inlined`). It is emitted
before the struct that holds it (`generation.rs:787-827`), and the position holds
it by name (`sectioning.rs:631-650`, `Referencing for Position`). Collisions
across the file namespace are refused (`tests/ethos.rs:127-139`).

An inline payload of an enum variant (`Variant::Struct`/`Variant::Enum`) is a
different mechanism. It generates a `<Variant>_Data` type, or
`<Owner>_<Variant>_Data` when the name collides (`checking.rs:738-858`,
`inline_name`).

Observed: nothing makes an inline declaration mandatory. No depth rule exists for
inline declarations. The only declaration limit is
`TYPE_DECLARATION_LIMIT = 512` on a Library's types section
(`checking.rs:25`, used at `:954-956` as `Problem::Depth`). Despite that name,
it limits a count, not a nesting depth. The protos reader caps nesting at
`MAXIMUM_READER_DEPTH = 256` (`protos/src/core.rs:254`).

Hypothesis. A mandatory-inline rule fits most naturally as a check pass
(`checking.rs`, alongside `Checkable for Library/Signal/...` at `:952-995`).
`Hoisting::declarations` already yields every declaration with its path, so
depth comes from `path.len()`. A new `Problem` variant would go in
`error.ethos:9-24`, and `src/error.rs` would be regenerated. The "algorithm"
that decides the depth is not present anywhere and is not specified in the code.

### 1.4 How `Name.Type` (one position) is handled

Observed: it is an alias. In the types section and as a struct position,
`Name.Type` reads as `TypeDeclaration::Alias` (`conception.rs:474-476`). It emits
a Rust type alias (`generation.rs:876-886`):

```rust
TypeDeclaration::Alias(identity, aliased) => { ...
    quote! { #[rustfmt::skip] pub type #name #parameters = #aliased; }
```

Generated evidence: `tests/generated/flow-signal.rs:3` is `pub type Brief = String;`.
`tests/generated/orchestrate.rs:3-13` has `pub type LockId = i64;` ... and
`pub type LockPaths = std::vec::Vec<LockPath>;`. Inline-collision evidence is
`tests/generated/inline-collision.rs:40` `pub type X_Data = String;`. The
knowledge-ethos skill states the same: "An alias carries no derive."

As an enum variant, `Name.Type` is not a declaration. It is
`Variant::Typed(name, reference)`, a variant carrying that type
(`conception.rs:495`; generated `#name(#archival #ty)`,
`generation.rs:697-702`).

Alias resolution is visible to the checker. It follows aliases for cycles and
reachability (`generation.rs:353`, `:445`). Any newtype change must also update
field naming (`field_names`, `generation.rs:~620-658`), archival/recursion, and
datom-codec composing for a one-field struct.

Hypothesis. Making `Name.Type` a new type means changing the `Alias` arm of
`Emitting for TypeDeclaration` to emit a one-field struct carrying the derive
block (`datom_derives`, `generation.rs:777-785`). It does not have to touch
conception, because the parse is already distinct. Whether the datom text of a
newtype stays the inner value's text (transparent) or becomes `{ value }` is a
datom-codec question. Its derive for one-field structs was not read in this
survey.

### 1.5 Comments

Observed. Comments begin with `;` and run to end of line, and only the protos
reader handles them (`protos/src/core.rs:519-531`):

```rust
fn space(&mut self) {
    loop {
        while self.glyph().is_some_and(char::is_whitespace) { self.step(); }
        if self.glyph() != Some(';') { return; }
        while self.glyph().is_some_and(|glyph| glyph != '\n') { self.step(); }
    }
}
```

`;` also ends a bare run (`core.rs:391`, `:428`). The sweet-form opener skips
`;` lines when it looks for the head (`canonicalization.rs:21-23`). Comments are
not kept in `Protos`, so a print drops them. `tests/print.rs:135-150` compares the
print against the source with `;` lines filtered out.

### 1.6 Generics and kinds accepted

Observed:

- A type declaration with angle constraints is refused (`conception.rs:460-465`). Declared types carry no generics, and `Identity.constraints` is always `vec![]` for types (`:466-469`).
- A kind accepts constraints: `Processable<[Clonable Sendable] Serializable>.[ ... ]` (`conception.rs:622-628`; test `lib.rs:847`). A constraint is `One(Reference)` or `Many(Vec<Reference>)` (`lib.rs:258-265`), with at most 26 per identity (`checking.rs:1000-1005`).
- Simple kind `Name.[ capabilities ]`; complex kind `Name.{ [ superkinds ] [ associated types ] [ CONSTANTS ] [ capabilities ] }` (`conception.rs:610-648`). Receivers: `.` Shared, `!` Mutable, `:` Static (`:512-520`). A capability is `name.[ Yield ]` or `name.{ [ inputs ] [ Yield ] }`, with exactly one yield (`:558-608`).
- Associated types: `Item<Serializable>` (`conception.rs:280-304`).
- Associations: `Type.[ Kind ... ]` (`:650-671`).
- Intrinsics: String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self, Sized (`lib.rs:418-441`, `:721-741`).
- Imports: `source:Name`, `source:[ A B ]`, with renaming `Ethos.Source` (`conception.rs:371-416`).

### 1.7 How `Vector<..>` / `Option<..>` are written

Observed. They are written tight, `Vector<Event>`, `Result<Integer SinkError>`.
Protos reads `Name<...>` with no following separator as two sibling nodes: a
`Bare` run, then an `Angled` enclosure. The reader rewinds to the bare run when
no separator follows the angle (`protos/src/core.rs:452-473`). Ethos pairs them
back up with `Constraining::constrained` (`conception.rs:132-172`; the doc
comment there says the re-join "is owed to protos"). On the writer side, an angle
stays tight to the preceding element (`protos/src/layout.rs:31-54`, `Grouping`,
`holds_tight` at `:78-88`). Ethos re-splits on ascent (`protosization.rs:55-79`,
`ReferencesProtosizing`).

Note. The doc comment at `conception.rs:146-147` still says the reprint spells
`Vector <Integer>`. Protos 0.32.1 ("Keep angles tight after a headed element")
and `tests/print.rs:69` (`leaves_stay_on_one_line_and_angles_stay_tight`) show
the current print is tight, so that comment is stale.

## 2. Writer / formatter side

Observed. There is one writer: `protos/src/rendering.rs`. It is an iterative step
machine with three renditions, `Printed` (canonical, vertical), `Compact` (one
line) and `Shown` (Debug) (`:38-46`). The vertical rule is at `:105-135`:

```rust
let elements = children.elements();
let hanging = elements.len() > 1 && elements.iter().any(|element| element.layered());
let mut steps = vec![ Step::Glyph(enclosure.opener()), Step::Glyph(' '), Step::Mark ];
for (index, element) in elements.into_iter().enumerate() {
    if index > 0 { steps.push(if hanging { Step::Hang } else { Step::Glyph(' ') }); }
```

`Mark` records the current column, and `Hang` writes `\n` plus spaces up to the
innermost mark (`:273-282`). The column tracker is `protos/src/layout.rs:7-29`
(`Column { glyphs }`, `Advancing`). It counts chars, not display width.
`Layered` (an element "has a next layer") is `layout.rs:57-77`.

Observed: there is **no width, no line-length limit and no right-margin
measurement** anywhere in the writer. A break is decided only by "more than one
element and any layered". Leaves always share one line however long they are
(protos test `tests/vertical.rs:28` `leaves_sit_on_one_line`). A single layered
element stays on its opener's line at any column
(`one_element_with_a_next_layer_stays_with_its_opener`, `vertical.rs:36`).

The same renderer computes extents. `Canonicalizable for Protos` measures the
`Printed` rendition (`rendering.rs:330-341`), and ethos's
`Protosizing for File` calls it (`ethos-zero/src/protosization.rs:421-425`). Any
layout change therefore moves the extents that error location depends on.

Ethos's own printing layer is `ethos-zero/src/printing.rs:10-45`. It prints the
root head, then each section from the first column via `section.textualize()`.
It owns no break decisions. The Rust side is printed by `prettyplease::unparse`,
followed by `collapse_derives` (`generation.rs:1197-1244`), which does not
concern ethos text.

Hypothesis. Both requested rules belong in `Rendition::Printed` steps
(`rendering.rs:105-135`):

1. A recursive block that would run too far right opens its first element on a new line, indented.
2. A vector wraps at a width, aligned with its first item.

Both need a width input, which nothing provides now. They also need a
measure-ahead: the `Compact` rendition of an element can give a width. The
column at `Mark` time is already known from `Column`. Every hand-written
expected text in `protos/tests/vertical.rs`, `deep.rs`, `textualization.rs` and
`ethos-zero/tests/print.rs`, plus the `fixtures/print/*.ethos` byte-identical
round trips, would need review.

## 3. datom-codec / protos: text→tree, pre-structure pass, `@`, CLI argument

### 3.1 Text→tree entry (protosize)

Observed:

- protos: `Protosizable for str`/`String` → `Reader::whole` with a 4096-node budget (`protos/src/core.rs:550-585`). `BoundedProtosizable::protosize_with(&mut ReaderBudget)` is the budgeted form.
- datom-codec: `Potential<T> { text, reader: Option<Protos>, marker }` (`datom-codec/src/core.rs:424-447`). `Actualizing for Potential<T>` (`:459-473`):

```rust
let protos = self.text.protosize_with(&mut budget.reader).map_err(|error| Error {
    layer: ErrorLayer::Protos, path: Path::new(), kind: ErrorKind::Structural(error) })?;
self.reader = Some(protos.clone());
let datom = crate::DatomForming::datom_form(&protos, Path::new())?;
datom.compose(budget)
```

- Ascent: `Datom::protosize` → `project` (`datom-codec/src/projection.rs:87-100`).
- ethos-zero has its own separate text entry, `Potential<File>` (`ethos-zero/src/lib.rs:400-412`), via `actualization.rs`.

### 3.2 Where a pre-structure text pass would go

Observed: there is a precedent. Ethos already has one text→text pass ahead of
structure, `Canonicalizable for String` (`canonicalization.rs`). It carries a
`seam` so that structural error extents can be resituated onto the source text
(`actualization.rs:14-25`).

Hypothesis. For datom, the pass would go in `Actualizing for Potential<T>`
(`datom-codec/src/core.rs:460-464`), before `protosize_with`. The pass would
replace `self.text` or produce a mapped text. Error extents
(`PotentialExtenting::reader_extent`, `:451-458`) would then refer to the
expanded text unless a seam map like ethos's `Canonical.seam` is kept. Splicing
can insert many seams, while ethos's `Shifting` handles exactly one (`canonicalization.rs:71-89`), so a list of seams would be needed. For ethos files, the
pass would go before or inside `Potential<File>::actualize`, ahead of
`canonicalize`. Expanding reads files, which datom-codec's pure core does not do
today. Where the file read lives (core vs the CLI) is an open choice.

### 3.3 Anything named Expanding / Resolving / ReferencePath / `@`

Observed. A grep over protos, datom-codec, ethos-zero and datom for
`Expand|Resolv|ReferencePath|@[a-z/.]|splic` (`.rs`, `.md`, `.ethos`) found:

- Nothing in protos or datom-codec.
- `Resolving` **already exists in ethos-zero** with a different meaning: name resolution, `pub trait Resolving { fn resolve(&self, name: &Name) -> Resolution; }` (`ethos-zero/src/lib.rs:533-537`), implemented throughout `checking.rs:31-169`. A new pass named `Resolving` would collide with it.
- No `@` handling. In protos `@` is an ordinary glyph inside a bare run (the run breakers at `core.rs:388-392` do not include `@`). Hypothesis on how `@/abs/x.datom` would read today: its segments split on `.` are non-empty (`core.rs:402-404`), so it reads as a `Headed` node `@/abs/x` `.` `datom`. In a `String` position, datom-codec re-joins headed runs into a dotted string (`composition.rs:200-238`, `compose_bare_string`). This matches how the CLI accepts `Check./abs/flow.ethos` unquoted.
- `$@xs` splice syntax appears only in protos-engine design notes (`protos-engine/design/ProtosEngine/ProtosEngineDesign-2026-07-29.md:661-669`), a different, unimplemented engine.

### 3.4 How the CLI takes its one inline datom argument

Observed. `ethos-zero/src/main.rs:184-210`:

```rust
[] => { /* print own ethos canonically */ }
[argument] => {
    let mut potential = Potential::<Query>::from(argument.as_str());
    potential.serve()
}
many => Response::Arguments(many.len() as datom_codec::Integer),
```

The argument is actualized with a fixed budget
(`Budget { remaining: 4_096, reader: ReaderBudget { remaining: 4_096 }, depth: 0, maximum_depth: 4_096 }`,
`main.rs:156-169`). A malformed argument answers `Response::Malformed(error)`.
The reply is printed by `datomize(...).protosize().compact()`, one line
(`main.rs:48-53`). The contract is `ethos-zero.ethos` (a Library:
`Query.[ Generate.Generation Check.String ]`), generated into
`src/ethos-zero.rs`. Paths are passed bare or in guillemets: the checks use
`"Generate.{ «$declaration» «$temporary» }"` (`protos/checks/generated-kinds.sh:13`).

Hypothesis. For `@path` to work on the CLI, the expansion has to run on
`argument` before `Potential::<Query>::from`, or inside datom-codec's
`actualize`.

## 4. Versions, and whether a manifest carries ethos versions

Observed:

- ethos-zero `Cargo.toml:3` `version = "16.0.0"`. It pins `protos` rev 15b41da (features rkyv) and `datom-codec` rev 4dff16b (features rkyv) (`Cargo.toml:27-28`). Its flake pins the same two revs as inputs, for the dependency-ethos check (`flake.nix:12-23`).
- protos `Cargo.toml:3` `version = "0.32.2"`.
- datom-codec `Cargo.toml:3` `version = "0.32.2"`. It pins protos rev 15b41da (`Cargo.toml:24`).
- protos and datom-codec pin the generator by **flake input**, `github:LiGoldragon/ethos-zero/06d73e07...` (`protos/flake.nix:11-12`, `datom-codec/flake.nix:11-12`). That commit is ethos-zero **14.2.0**, not 16.0.0. The pin is used by the `generated-kinds` and `checked-anatomy` checks (`protos/flake.nix:58-66`, `datom-codec/flake.nix:66-72`).
- Consumers pin ethos-zero by git rev as a **build-dependency**, and the revs vary. Examples: `signal/Cargo.toml` rev c2653dd (current); `signal-system`/`signal-persona` rev 4bf73ca; `signal-router`/`meta-signal-spirit` rev b232d35.
- No manifest field carrying an "ethos version" was found. A grep for `ethos[-_ ]?version|ethosVersion` in `.toml`/`.nix`/`.json`/`.ethos`/`.datom` under `/git/github.com/LiGoldragon` matched nothing. The only version linkage is the Cargo/flake rev pin of the generator crate. Ethos files carry no version.

## 5. Generator entry point and how a repository runs it

Observed. There are two entry points.

1. **CLI binary** `ethos-zero` (`src/main.rs`). Per the knowledge-ethos skill and `tests/cli.rs`:
   ```
   ethos-zero 'Generate.{ /abs/flow.ethos /abs/out }'   -> Generated.[ /abs/out/flow.rs ]
   ethos-zero 'Check./abs/flow.ethos'                    -> Checked./abs/flow.ethos
   ```
   Output lands at `<directory>/<stem>.rs` (`main.rs:109-113`); the directory is created (`:118`). A rejected file writes nothing. This is the form the Nix checks run (`protos/checks/generated-kinds.sh:13` then `cmp` against the committed `generated/protos-kinds.rs`; `ethos-zero/checks/dependency-ethos.sh:8`).
2. **Library**, `ethos_zero::{Potential, File, Actualizing, Generating}`. Consumers call it from `build.rs` as a build-dependency and **assert freshness** against committed Rust, rather than writing to OUT_DIR. `signal/build.rs:1-13`:
   ```rust
   let source = std::fs::read_to_string(root.join("ethos/signal.ethos")).expect("source");
   let file = Potential::<File>::from(source).actualize().unwrap_or_else(|_| panic!("read"));
   let generated = file.generate().unwrap_or_else(|_| panic!("generate"));
   assert_eq!(generated, std::fs::read_to_string(root.join("src/generated/signal.rs")).expect("generated"));
   ```
   Generated Rust is committed. Locations vary by repository: `signal` uses `src/generated/<stem>.rs`, protos and datom-codec use `generated/<stem>.rs`, and ethos-zero itself uses `src/ethos-zero.rs`, `src/error.rs` and `tests/generated/*.rs`. Inside ethos-zero, regeneration is done by `#[test] regenerate_cli_contract` / `regenerate_library_fixtures` (`src/lib.rs:868-931`). `tests/freshness.rs` asserts that the committed files are fresh and that there are exactly 18 fixtures (`:55`).

Hypothesis on the blast radius of the syntax changes. Every consumer `build.rs`
equality assert and every Nix `cmp` check fails until its committed Rust is
regenerated with the new generator. A change from alias to newtype changes the
generated Rust of every file that uses `Name.Type`, and so changes consumer Rust
code that relies on the alias being the underlying type (for example
`LockId = i64`). Consumers pinned to older revs are unaffected until they are
repinned.

## Not found

- No width or line-length concept in any writer (protos, ethos printing).
- No `@`, file-reference, include or expansion mechanism in protos, datom-codec or ethos-zero.
- No algorithm for deciding a mandatory inline-declaration depth, and no inline-declaration requirement.
- No manifest field carrying ethos versions.
- Not read: the datom-codec derive for one-field structs (`crates/datom-codec-derive/src/lib.rs`), which bears on how a newtype's datom text would look; `tree-sitter-ethos/grammar.js`, which is a second grammar that the syntax changes may also have to update.

## Sources

- `/git/github.com/LiGoldragon/ethos-zero` @ c2653dd: `Cargo.toml`, `flake.nix`, `src/{lib,main,actualization,canonicalization,conception,protosization,sectioning,printing,generation,checking}.rs`, `error.ethos`, `ethos-zero.ethos`, `fixtures/`, `tests/{ethos,print,freshness,cli}.rs`, `tests/generated/`, `checks/dependency-ethos.sh`.
- `/git/github.com/LiGoldragon/protos` @ 15b41da: `Cargo.toml`, `flake.nix`, `src/{lib,core,layout,rendering}.rs`, `checks/{generated-kinds,checked-anatomy}.sh`, `tests/vertical.rs` (names only).
- `/git/github.com/LiGoldragon/datom-codec` @ 4dff16b: `Cargo.toml`, `flake.nix`, `src/{lib,core,composition,projection}.rs`, `README.md`.
- `/git/github.com/LiGoldragon/signal` @ 0cad1d1: `Cargo.toml`, `build.rs`.
- knowledge-ethos skill (loaded through the Skill tool).
- Provenance receipt: unavailable (no PROVENANCE handoff received).
