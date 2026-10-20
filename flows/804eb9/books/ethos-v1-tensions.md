Tensions on the Ethos basics, for volume 1 edition 2. Evidence for the assembler; not book text. Module: psyche-context › vision/ethos.md unless named. Records: R-numbers of gather-ethos-vision.md.

Missed records: flows/8e9e77/vision/single-field-structs.md:5,15; flows/cff271af/vision/tuples.md:64; flows/1c282d/vision/archive-protosizable.md:17; flows/6329f1/vision/archive-ethos.md:22; flows/e8c4cc61/vision/archive-ethosFileAnatomy.md:15; flows/564f55/vision/archive-ethos.md:23; flows/995a164e/vision/kinds.md:7; flows/e8c4cc61/vision/designPractice.md:26; flows/5578cc/vision/flow.md:35.

Draft flaws:
- v1 P5 line 1 calls Name.String "a struct of one unnamed position", contradicting its line 2 and 8e9e77:15.
- R41: a trait with one capability and one bearer is suspicious; v1 P1 Stored and old P1 Named.[ Prompt ] are such.
- Trait names are qualifier-named (crystallized § Naming; R37): Briefing, Prompting, Seating break it.

T1 Every file a vector? (§ Declaration: File)
 1a: - The unit is File: one file, one Rust module.  + Every file is a vector of roots; which roots share a file is file management only.
 1b: same removal; + A file is one root, or a vector of roots; which roots share a file is file management only.
T2 Outer braces (R16 later correction):
 - An ethos file is written in the sweet form: the root's head, then the sections as siblings, the outer braces omitted. The braced form — the root's head opening braces that hold every section — is the canonical form. The sweet form is kept out of the main logic run: before the text is read as ethos at all, the file is converted mechanically to the canonical form, so the ethos reader sees only proper ethos.
 + A root is its variant, the dot, and the braces holding its sections; no form drops the braces.
 (its code block goes too)
T3 Brace placement (§ Spacing):
 + A file's usual form is the root's variant, its dot and the brace on one line, then a break, its sections standing unindented one per line; this is good form, never a requirement.
 + A file that holds a single thing breaks nowhere.
 - Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line.
 + Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned, except a root, whose sections start on the line after its brace; the closing delimiter ends the last element's line.
T4 Sections in a vector of roots: 4a + In a vector of roots, each root's sections stand at its variant's column. / 4b + In a vector of roots, each root's sections are indented under its variant.
T5 Indent width (R62 three; examples two): 5a + An indent is three spaces. / 5b + An indent is two spaces.
T6 Type among roots: 6a - Four roots: Library, Signal, Operation, Memory. + Five roots: Library, Signal, Operation, Memory, Type; Type declares one type and what it needs, inline. / 6b + Type is not a root: it shows one type alone, outside a file. / 6c + Types declares several types, as a Library's types section does.
T7 Sema→Memory:
 - Library, Signal, Operation, Memory. No version in a file. Signal's sections are queries and responses, since there is communication; Sema's are record types, the rest to be decided. Signal gives a Nexus its main types and Sema its database types.
 + No version in a file. Signal's sections are queries and responses, since there is communication; Memory's are record types, the rest to be decided. Signal gives a Nexus its main types and Memory its database types.
T8 Implied associations: 8a - In the Signal and Sema roots the associations of the query, response and record types are implied and never written. + Every root ends with a traits section and an associations section, as a Library does. / 8b same removal + Every root ends with a traits section and an associations section, as a Library does; in Signal and Memory the associations of the query, response and record types are implied, and the section holds the rest.
T9 Every type bears a trait (R49 short-term without; R50): 9a + Every declared type bears at least one trait besides the datom traits; a type that bears none is refused, because it does nothing. / 9b + Short term: a type may bear only the datom traits. Long term: every declared type bears at least one trait besides them; a type that bears none is refused.
T10 All traits in ethos (R43, R48, R49): 10a + Every trait is declared in ethos and every implementation is of such a trait; code not generated from ethos declares no trait. / 10b same + Short term: a program may declare traits outside ethos.
T11 New type not alias:
 - An alias bears them through the type it names: an alias is not a new type and cannot carry a derive.
 - Head then symbol is a variant of `Query` or `Response` in a Signal's first two sections, an alias in the types section.
 + Head then symbol is a variant of `Query` or `Response` in a Signal's first two sections, a new type in the types section.
 + A type declared over one other type is a new type, never an alias: its name, the dot, the contained type, `Name.String`, `Age.Integer`.
 (replaces v1 P5 line 1; pub type blocks in the module become one-field tuple structs)
T12 New type over container: 12a + A new type may hold a container: `Counts.Vector<Integer>`. / 12b + A new type holds a type that is not a container; a container is written where it is used.
T13 Tuples: - No tuple in the code we design; if some parts require it (standard traits, dependencies), then it is allowed at that contact point only. + No tuple in the code we design, the new type excepted, which Rust writes as a tuple of one field; elsewhere a tuple is allowed only at a contact point that requires it (standard traits, dependencies).
T14 New type in datom (vision/datom.md; no living statement): 14a + A new type is written as the value it wraps: a `Name` reads `Ada`. / 14b + A new type is written as a struct of one position: a `Name` reads `{ Ada }`.
T15 Association direction: 15a no module change, v1 P1 example rewritten Type.[ Traits ] / 15b - An association declares that a type bears a trait: the type's name, a dot, a bracket of its traits. + An association declares that a trait is borne: the trait's name, a dot, a bracket of the types that bear it. / 15c + In associations, a trait borne by several types holds the vector of them; an association whose head is a type keeps the vector of traits that type bears.
T16 Capability case (R53): + A capability is named in lowercase camelCase, because it is not a type or a trait.
T17 "First": 17a + A name written in ethos says what it names; a word that means something only beside its neighbours, such as First, names nothing. / 17b old P1 wording plus - a repeated type as first and second

Blocking lines in main vision/ethos.md:
- P1: § Declaration: File "The unit is File: one file, one Rust module."; sweet-form sentences (T2) and code block.
- P3: § Associations implied sentence; § Shapes and placement Signal example without traits/associations.
- P4: § Every declared type bears both traits; examples with [] traits/associations (§ Declaration: File Record, § What a declaration turns into, § Inline types, § A variant named as a defined type, § A variant may declare its payload inline, § Shapes and placement); § Trait syntax SinkError/Fillable unassociated.
- P5: pub type lines in § What a declaration turns into, § Inline types, § A variant named as a defined type (incl. "; types: FilePath is an alias of String", SyntaxError), § A variant may declare its payload inline, § Every declared type bears both traits (alias sentence and "// an alias:" lines), § Shapes and placement ("an alias in the types section", three pub type lines); § Associations tuple sentence.
