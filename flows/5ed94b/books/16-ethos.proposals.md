Presentation.{ «Ethos» }

Ethos is the language the system's types and kinds are written in, still being designed. Reading it is how he understands the system's anatomy; the kinds become Rust traits, and the hand-written code is mostly bodies.

**1. What Ethos is**
Module: vision, vision-ethos. Action: edit.
Text: "Ethos is the language the system's types and kinds are written in. Every machine-to-machine language invented as we go is Ethos."
Rests on: 8 Sep, 20 Sep.

**2. Everything is a type, nothing repeats**
Module: vision, vision-ethos. Action: edit.
Text: "There are no loose values and no key-value maps; every value is a type. Design the types first; kinds follow from what the types can do. Ethos never repeats itself, carries no version number (versions go in a manifest), and has no generics: where Rust has a parameter, Ethos names a kind."
Rests on: 2 Oct, 13 Aug, 2 Oct, 4 Sep, 1 Aug.

**3. How a type is written**
Module: vision, vision-ethos. Action: edit.
Text: "A variant named like an existing type carries that type. A variant may declare what it carries in place; Ethos derives the new type's name. A type used in one place is declared inline. Struct fields have no names in Ethos; Rust names them after their types."
Rests on: 30 Sep, 2 Oct, 8 Sep.

**4. Newtypes**
Module: vision, vision-ethos. Action: edit.
Text: "A type that wraps exactly one other type is a newtype, never a one-field struct. The generator refuses a one-field struct. Name becomes a type of its own."
Rests on: 8 Sep, 7 Aug.

**5. Kinds and capabilities**
Module: vision, vision-ethos. Action: edit.
Text: "A kind is a quality a type has, named like Launchable, not Launch. A capability is one function of a kind. A capability's inputs are kinds, never specific types."
Rests on: 26 Aug, 2 Oct.

**6. How it looks**
Module: vision, vision-ethos. Action: edit.
Text: "Ethos grows downward: anything with a layer inside opens onto new lines. A closing bracket ends the last line. Every section, and every line with a layer inside, carries a comment saying in plain words what the machine reads there."
Rests on: 2 Oct, 3 Oct.

**7. Comments reach the Rust**
Module: vision, vision-ethos. Action: edit.
Text: "The generator carries each Ethos comment into the Rust above its type."
Rests on: 3 Oct. Today the generator drops every comment.

**8. Ethos in a book is a whole file**
Module: vision, vision-ethos. Action: edit.
Text: "Ethos shown anywhere is a whole root with its sections; a fragment is not ethos. Beside it goes a datom example in use."
Rests on: 15 Sep, 29 Sep, 2 Oct.

**9. The registry's list**
Module: vision, vision-ethos. Action: edit.
Text: "The context-module registry's list is named ModuleType, and Role is one of its entries."
Rests on: 3 Oct.

**10. Topics**
Module: vision, vision-ethos. Action: edit.
Text 1: "Every topic is a variant inside Mind, rebuilt whenever one is added."
Text 2: "Topics are open names, not variants."
Rests on: 3 Oct against 26 Sep. Name 1 or 2.

**11. Inline depth**
Module: vision, vision-ethos. Action: edit.
Text 1: "The generator refuses a type nested four levels inline; deeper types come from a library."
Text 2: "The generator warns at the fourth level."
Text 3: "Inline depth is left to the writer."
Rests on: 2 Oct. Name 1, 2 or 3.

**12. Update what the generator does**
Module: knowledge, knowledge-ethos. Action: edit.
Text: "The generator accepts a one-field struct and writes a one-part type as a plain alias. It drops every comment. No word-id library and no core Ethos library exist yet."
Rests on: witnessed today.
