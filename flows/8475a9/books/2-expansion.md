<!-- to-the-living:start -->
Presentation.{ «Datom expansion» }

A reference in datom text that is replaced by the datom payload of a file, typed by the position it sits in. Ethos first, then the example, then the layers of correctness and six rulings.

## How it is now

Text reaches a typed value in three layers, none of which knows a file.

[drawing: Three boxes left to right: text → protos (untyped tree) → datom form (untyped) → compose (typed by position) → value. A note under compose: the expected type is known only here.]

```
protos        lexes text into a tree; reserves { } [ ] < > « » ( ) ; . ! :
datom form    Form.[ Struct Vector Variant Bare String Meaning ]
compose       walks the Form against the Rust type; a position's type is known only here
```

- No include, reference or reader syntax exists in protos or datom-codec 0.32.2.
- `@ # $ ~ % ^ & * = | ?` are free: the lexer reads them as bare text.
- A file-by-path convention exists as data only: curriculum-deploy 0.9.0 opens `roles.datom` itself in code; lojix passes two file paths as String positions and a program opens them later.
- `Budget` bounds compose steps, protos nodes and nesting depth; the caller builds it.

## The ethos

```
Library
[]                                          ; imports
[ FilePath.String                           ; types
  Locator.[ File.FilePath ]                 ;   where a payload lives; File is the only variant today
  Expansion.[ Forbidden                     ;   the reader was given no expander
              Missing.FilePath
              Unreadable.FilePath
              Cycle.Vector<FilePath>        ;   a file that reaches itself
              Depth.Integer ] ]             ;   nesting past the budget
[]                                          ; kinds: Expanding, below in Rust
[]                                          ; associations
```

## The syntax

One glyph, `@`, opens a reference; what follows is the locator, bare or in guillemets.

```
; a position expecting Request, for curriculum-deploy
Generate.{ @/git/github.com/LiGoldragon/Curriculum/curriculum.datom «/home/li/primary» }

; curriculum.datom, read against Configuration because that is the position it replaces
{ «/git/github.com/LiGoldragon/Curriculum»
  [ Psyche.@../psyche-skills/index.datom     ; a reference inside a file resolves beside that file
    Mind.@../mind-skills/index.datom
    Field.@../field-skills/index.datom ] }
```

The repo keeps `curriculum.datom`; no model composes it at deploy time. A reference may sit anywhere a value may sit, and the file is read as that position's type.

## The layers of correctness

[drawing: compose meets @ at a position expecting T; it asks the Expander for the file; the file's text goes through protos and datom form and is composed as T at the same path; the value drops into place. A locked box on the right labeled Nexus: no Expander, so @ is Forbidden there.]

1. **A node, not a bare string.** protos gains one node, `Reference`, opened by `@`; datom-codec gains `Form::Reference(Locator)`. A bare string that begins with `@` is written in guillemets. Nothing else in the grammar moves.
2. **Typed by position.** Expansion happens at compose, where the expected type is first known: the file is read as the type of the position holding the reference. A file that does not fit fails with the ordinary form error, at the reference's path, naming the file.
3. **A capability, not a default.** Reading a file is a kind the caller supplies. A `Budget` without an expander answers every reference `Forbidden`. A Nexus links no expander, so no text and no file ever enters it; expansion is the CLI's.
4. **Bounded.** The expanded file spends the same budget: its nodes, its compose steps, its depth. A file that reaches itself is `Cycle`.
5. **Located.** A reference inside a file resolves beside that file; a reference in the inline CLI argument resolves from the caller's working directory. An absolute path resolves as written.
6. **Errors are datom.** `Expansion` is a variant of the existing error vocabulary, carrying the path of the position and the file.

```rust
/// datom-codec: the caller's file access, supplied with the Budget. A Nexus never implements it.
pub trait Expanding {
    fn expand(&self, locator: &Locator, beside: &Origin) -> Result<String, Expansion>;
}

impl Datom {
    pub fn compose<T: Composing>(&self, budget: &mut Budget) -> Result<T, Error> {
        if let Form::Reference(locator) = &self.form {
            let expander = budget.expander().ok_or(Expansion::Forbidden)?;
            let text = expander.expand(locator, &self.origin)?;
            let origin = budget.enter_file(locator)?;               // Cycle, Depth
            let datom = Potential::<T>::from(text).form_at(&self.path, origin, budget)?;
            return datom.compose(budget);                            // the file read as T, at this path
        }
        budget.enter_composition(&self.path)?;
        let value = T::compose(self, budget);
        budget.leave_composition();
        value
    }
}
```

Illustration; not compiled. `Origin` is the file a datom came from, or the CLI argument.

## The other way

Output already is the expanded value: `datomize` writes every position in full, and a Nexus answers in signal, which never held a reference. Writing a value back into the files it was expanded from is a second design; nothing here needs it.

## What this touches

```
protos            one node, Reference, opened by @; its print
datom-codec       Form::Reference, Expanding, Budget.expander, Expansion errors
curriculum-deploy the roles.datom read in code goes; the request carries @roles.datom
the datom skill   the line "datom passes inline at a CLI boundary, never as a datom file" changes
```

## Two of your earlier words

Your notion on the same idea: "Using paths is very setup-dependent so it's not a very good idea for a system that wants to be correct", and the alternative, a compiled signal file beside the datom file. Layers 3 and 5 are the answer offered: the path is resolved only where text is already spoken, beside the file that names it, and never inside a Nexus.

Your ruling of 2026-08-21: "get rid of the manifest and generate whatever skills are present". curriculum-deploy does that today. The repo index you ask for now is a manifest again. Ruling 4 asks which stands.

## Rulings

1. The glyph: (a) `@`. (b) another (say which).
2. Where expansion happens: (a) at compose, typed by the position, only through a caller-supplied expander; a Nexus has none. (b) a text splice before parsing, untyped.
3. Resolution: (a) beside the file holding the reference; the inline argument from the caller's working directory. (b) absolute paths only.
4. The repo index: (a) each skill repository keeps its own index file, read by reference; this supersedes "get rid of the manifest". (b) keep directory discovery; references serve other inputs only.
5. A content pin, `@{ path checksum }`, so a deploy is reproducible: (a) not now. (b) design it with the glyph.
6. The other way: (a) not designed; output is the expanded value. (b) design contracting now.
<!-- to-the-living:end -->
