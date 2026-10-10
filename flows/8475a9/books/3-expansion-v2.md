<!-- to-the-living:start -->
Presentation.{ «Datom expansion» }

Second edition, after your nine comments. Each is quoted, then answered; the design follows, rewritten in plain words.

## Your comments

**"Well with the new vision we wouldn't involve this curriculum repo. We would just directly invoke the particular repositories like mind, psyche, and field."**
The example now invokes the three skill repositories directly; the Curriculum repository is gone from it.

**"Well the Nexus has no datom so expand [it]. It doesn't even have datom. There should be no datom in any Nexus. It's going to be forbidden for string handling to be in the Nexus."**
The Nexus box and the word Forbidden are gone. Expansion lives in datom-codec, which is compiled only into CLIs; a Nexus has no datom and so no expansion. Nothing has to forbid it.

**"No it wouldn't use [guillemets] because that would make it a string, which it's not. It's a path. It's an expanding path or whatever the right term is here. Yeah it's a reference path so it's not a string so it's not going to have the string delimiter."**
Agreed. The term here is reference path. It is written bare after `@` and is its own type, never a String.

**"So compose would be a step before the protos structure step, like finding the structure. There would be a step before that, kind of like how we have a step, or we should have a step in ethos to rearrange an ethos file so that it's a variant with a struct."**
Yes. Expansion is now the first step, before any structure is read: every `@path` is replaced by the text of its file, and only then does the reader look for structure.

**"I don't understand that: a budget without an expander, answers every reference forbidden. What the hell does that mean?"**
That sentence is gone with the Nexus box.

**"I again don't understand what this spend budget is. What the hell are you talking about, spending budget?"**
Budget is datom-codec's own name for its limits: the reader refuses text past a size, a nesting depth and a node count. The point was only that an included file counts toward those same limits. Said so below, without the word.

**"The trait is missing here. Everything should be done with a trait, right? Don't we have that rule? How we code in Rust: everything is a trait. Everything must fall under a trait. If the trait design is wrong then there's something wrong with the anatomy of the design of the system."**
The code was wrong: `compose` sat as a method on a struct. Every step is now a trait, and the four steps form one chain.

**"Yeah I think that's the right symbol."**
`@` stands.

**"What do you mean, 'typed by the position'? That doesn't make sense to me."**
The phrase is gone. With expansion first, the file's data simply sits where `@path` was, and is checked like anything written there by hand.

## The four steps

[drawing: Four boxes in a column: 1 expand (text with @paths becomes text without them), 2 structure (protos reads the tree), 3 form (datom form), 4 compose (the typed value). Expand is highlighted as the new, first step; the other three are unchanged.]

```
1 expand     every @path replaced by its file's text, which is itself expanded first
2 structure  protos reads the expanded text into a tree          (unchanged)
3 form       the tree becomes a datom form                        (unchanged)
4 compose    the form becomes the typed value                     (unchanged)
```

## The syntax

`@` followed by a bare reference path. The path is its own type, not a string.

```
; the deploy request, typed at the CLI: each skill repository is named directly
Generate.{ [ Psyche.@/git/github.com/LiGoldragon/psyche-skills/index.datom
             Mind.@/git/github.com/LiGoldragon/mind-skills/index.datom
             Field.@/git/github.com/LiGoldragon/field-skills/index.datom ]
           /home/li/primary }

; psyche-skills/index.datom: the repository describing itself, kept in the repository
{ [ { Spirit spirit spirit/spirit.md }
    { Vision contextModules vision/contextModules.md }
    { Vision psyche vision/psyche.md } ] }
```

After step 1 the request reads as if the three index files had been typed in place. No model composes an index at deploy time; each repository keeps its own.

## The ethos

```
Library
[]                                            ; imports
[ ReferencePath                               ; types: a path to a datom file; its own type, never a String
  Expansion.[ Missing.ReferencePath           ;   why an expansion failed
              Unreadable.ReferencePath
              Unbalanced.ReferencePath        ;   the file's delimiters do not close
              Cycle.Vector<ReferencePath>     ;   a file that reaches itself
              Depth.Integer ]                 ;   nesting past the reader's limit
  Index.Vector<Module>                        ;   what a skill repository says of itself
  Module.{ ModuleType Name.String ModulePath.String }
  ModuleType.[ Spirit Intent Vision Notion Knowledge Operation ]
  Source.[ Psyche.Index Mind.Index Field.Index ]
  Request.[ Generate.{ Vector<Source> Workspace.String } ] ]
[]                                            ; kinds: Expanding and Resolving, below in Rust
[]                                            ; associations
```

`Index`, `Module`, `ModuleType` and `Request` are the deploy's types reshaped for this example; `ModuleType` is the list from «Context modules», Proposal 3.

## The layers of correctness

[drawing: The expand step as a walk along the text: it skips «…» strings and ; comments, meets @path, resolves it beside the file that holds it, checks the file is balanced, splices its expanded text in, and continues. Side notes: a file reaching itself stops as Cycle; the whole expanded text is measured against the reader's limits.]

1. **Before structure.** Expansion is the first step; steps 2 to 4 never see a reference.
2. **A path, not a string.** `@` opens a reference path in the text; an `@` inside guillemets or after `;` is content, because the walk skips strings and comments.
3. **Located.** A reference inside a file resolves beside that file; one in the inline CLI argument resolves from the caller's working directory; an absolute path as written.
4. **Checked before splicing.** Each file is checked balanced on its own before its text goes in, so a broken file is reported by its own name, never as a broken request.
5. **Measured as one text.** The expanded text is held to the reader's existing limits on size, depth and node count, as if written in place; a file that reaches itself is refused as a cycle.
6. **Nowhere near a Nexus.** All of this is datom-codec, compiled only into CLIs.
7. **Errors are datom.** `Expansion` joins the existing error vocabulary and names the file.

## The traits

```rust
/// Step 1. Text that may hold reference paths becomes text that holds none.
pub trait Expanding {
    fn expand(&self, resolver: &impl Resolving, within: &mut Within) -> Result<Expanded, Expansion>;
}
impl Expanding for Text { /* one walk: skip « » and ; … \n, replace each @path */ }

/// Turns a reference path into the text it names, beside the file that holds the reference.
pub trait Resolving {
    fn resolve(&self, path: &ReferencePath, beside: &Origin) -> Result<Text, Expansion>;
}
impl Resolving for Files { /* the CLI's resolver: the filesystem */ }

/// A file is balanced before it is spliced.
pub trait Balancing { fn balanced(&self) -> Result<(), Expansion>; }
impl Balancing for Text { /* protos's delimiter check, nothing more */ }

/// Within: the files already open, for cycles, and the depth so far.
pub struct Within { open: Vec<ReferencePath>, depth: Integer }

/// The chain. Steps 2 to 4 are the traits datom-codec already has.
pub trait Actualizing<T: Composing> {
    fn actualize(&self, resolver: &impl Resolving, limits: &mut Limits) -> Result<T, Error>;
}
impl<T: Composing> Actualizing<T> for Potential<T> {
    fn actualize(&self, resolver: &impl Resolving, limits: &mut Limits) -> Result<T, Error> {
        let expanded = self.text.expand(resolver, &mut Within::at(&self.origin))?;   // 1
        let tree = expanded.protosize(limits)?;                                       // 2
        let form = tree.datom_form()?;                                                // 3
        form.compose(limits)                                                          // 4
    }
}
```

Illustration; not compiled. `Limits` is datom-codec's existing `Budget`, renamed here only to say what it is.

## The other way

Output already is the expanded value: a value written out gives every position in full, and a Nexus answers in signal, which never held a reference. Writing a value back into the files it came from is a second design; nothing here needs it.

## What this touches

```
datom-codec       the expand step, Expanding, Resolving, Balancing, Within, the Expansion errors
protos            the delimiter check exposed as Balancing; no new node
curriculum-deploy takes Vector<Source> of indexes; the directory walk and the roles.datom read in code go
the datom skill   the line "datom passes inline at a CLI boundary, never as a datom file" changes
```

## Your earlier words

Your notion: "Using paths is very setup-dependent so it's not a very good idea for a system that wants to be correct." Layers 3 and 6 answer it: a path is resolved beside the file that names it, by a CLI, never by a Nexus.

Your ruling of 2026-08-21: "get rid of the manifest and generate whatever skills are present". A repository's own index is a manifest again, kept by the repository. Ruling 3 asks which stands.

## Rulings

1. Settled by your comment: the glyph is `@`.
2. Expansion as the first step, a text splice with each file checked balanced before it goes in: yes, or amend.
3. Each skill repository keeps its own `index.datom`, read by reference; this supersedes "get rid of the manifest": (a) yes. (b) no, keep directory discovery.
4. Resolution: (a) beside the file holding the reference; the inline argument from the caller's working directory. (b) absolute paths only.
5. A content pin on a reference, so a deploy is reproducible: (a) not now. (b) design it.
6. The other way: (a) not designed; output is the expanded value. (b) design it now.
7. The traits above: yes, or amend.
<!-- to-the-living:end -->
