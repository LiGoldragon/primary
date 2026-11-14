Presentation.{ «The Meaning delimiter is the double angle bracket» Proposal }

# The Meaning delimiter is the double angle bracket

Created by Fable 5.1, on the living's words.

### Proposal 1: Parentheses are freed · psyche-belief › vision/datom.md

::: comment
A delimiter read by balance is safe only when its glyph is rare in content, and the parenthesis is the commonest glyph in prose and code: Markdown prose, Mermaid and every code block carry it, balanced or not. The double angle bracket appears in nothing we write. It is the guillemet's sibling, which is what a Meaning is: a string with structure. Parentheses are freed for whatever comes to need them.
:::

- Guillemets are the string delimiter, and parentheses are reserved for Meaning.
+ Guillemets are the string delimiter, and the double angle brackets, ⟪ ⟫, are the Meaning's.

- Meaning is the structured string: text that carries, besides its words, the emphasis and the other structural aspects a plain string simply lacks, an annotated string, meant to revolutionize the performance of thinking machines on text. The aim is the most advanced structured meaning system ever made. Parentheses are a major symbol of cognition, and in datom they have one duty: the parenthesis pair is the Meaning delimiter, as the guillemets are the plain string's. The seed of the design is that parentheses inside ordinary text are already markup, so a Meaning is read by balance: a parenthesis pair inside it is structure of its own, nesting to arbitrary depth, a graph of sorts, and the Meaning closes at the parenthesis that balances the one that opened it; an unbalanced parenthesis inside it is escaped. Opening a Meaning makes the whole delimiter and structure spectrum available inside it, until the closing parenthesis restores the outer context. Its annotations are enums used throughout the tree, Emphasis among them; its shape is still open. Meaning is datom. Strings are strings and Meaning is Meaning: a position of type String expects a plain string and nothing else, and a position of type Meaning expects a Meaning.
+ Meaning is the structured string: text that carries, besides its words, the emphasis and the other structural aspects a plain string simply lacks, an annotated string, meant to revolutionize the performance of thinking machines on text. The aim is the most advanced structured meaning system ever made. The double angle brackets, ⟪ ⟫, are the Meaning delimiter, as the guillemets are the plain string's: the string's sibling glyph, for the string with structure, and a glyph that appears in no prose and no code we write, so that balance alone closes it. A Meaning is read by balance: a ⟪ ⟫ pair inside it is a Meaning of its own, nesting to arbitrary depth, and the Meaning closes at the bracket that balances the one that opened it; an unbalanced one inside it, which is rare, is escaped with a backslash as a guillemet is. Opening a Meaning makes the whole delimiter and structure spectrum available inside it, until the closing bracket restores the outer context. Its annotations are enums used throughout the tree, Emphasis among them; its shape is still open. What stands inside the Meaning delimiter is Sema, the meaning language, and the version of Sema a position holds is the position's type: today SemaZero, version 0 of Sema, which is Markdown read into a typed tree. Strings are strings and Meaning is Meaning: a position of type String expects a plain string and nothing else, and a position of a Sema type expects a Meaning. Parentheses are free: datom gives them no duty.

```datom
- ; datom, in a position expecting Note: a struct of author String, body Meaning.
- ; The first position expects a string: Ada has no space and no delimiter, so it is bare.
- ; The second position expects a Meaning, so the parenthesis opens it and it is read by balance:
- ; the inner pair is structure inside the Meaning, and the parenthesis that balances the opening one ends it.
- ; Today the whole parenthesized text lands as a plain String; what the inner pair will mean is not yet designed.
- { Ada (The build passed on the third try (after two timeouts)) }
+ ; datom, in a position expecting Note: a struct of author String, body Meaning.
+ ; The first position expects a string: Ada has no space and no delimiter, so it is bare.
+ ; The second position expects a Meaning, so ⟪ opens it and it is read by balance:
+ ; the inner pair is a Meaning inside the Meaning, and the ⟫ that balances the opening one ends it.
+ ; Today the whole bracketed text lands as a plain String; what the inner pair will mean is not yet designed.
+ { Ada ⟪The build passed on the third try ⟪after two timeouts⟫⟫ }

- ; datom, in a position expecting Remark: a struct of author String, body String.
- ; The second position expects a plain string; it has spaces, so it is delimited,
- ; and the parentheses inside the guillemets are content, not a Meaning.
- { Ada «The build passed on the third try (after two timeouts)» }
+ ; datom, in a position expecting Remark: a struct of author String, body String.
+ ; The second position expects a plain string; it has spaces, so it is delimited,
+ ; and the brackets inside the guillemets are content, not a Meaning.
+ { Ada «The build passed on the third try ⟪after two timeouts⟫» }

- ; datom, in a position expecting Standup: a struct of team String, items Vector<Meaning>.
- ; Each component of the vector is one Meaning; each is read by balance on its own.
- { Backend
-   [ (Ada fixed the flaky test (the one with the timeout))
-     (Bo is out (back Monday)) ] }
+ ; datom, in a position expecting Standup: a struct of team String, items Vector<Meaning>.
+ ; Each component of the vector is one Meaning; each is read by balance on its own.
+ { Backend
+   [ ⟪Ada fixed the flaky test ⟪the one with the timeout⟫⟫
+     ⟪Bo is out ⟪back Monday⟫⟫ ] }
```

### Proposal 2: The protos delimiter set · psyche-belief › vision/protos.md

::: comment
The same change, at the layer that holds the glyphs.
:::

- Five pairs. `{ }`, `[ ]`, `< >` structural; `« »` opaque, every glyph content; `( )` reserved for meaning, its type unspecified, read by balance as opaque until it is.
+ Five pairs. `{ }`, `[ ]`, `< >` structural; `« »` opaque, every glyph content; `⟪ ⟫` meaning, read by balance as opaque, its type the conceptual layer's. Parentheses are not a delimiter.

### Proposal 3: The guillemet string is read by balance · psyche-belief › vision/protos.md

::: comment
The vision says balance; the codec closes at the first unescaped »; one of the two gives. This alternative keeps the datom vision as written and brings protos to it. Its cost is one rule more in the reader; its gain is that a datom quoted inside a string, as every example in these modules is, needs no escape.
:::

- A closing guillemet inside a string is escaped with a backslash, so the ascent never refuses.
+ A guillemet string is read by balance, as a Meaning is: a « » pair inside it is content, nesting to any depth, and the string closes at the guillemet that balances the one that opened it; an unbalanced guillemet inside it is escaped with a backslash, so the ascent never refuses.

### Proposal 4: The guillemet string closes at the first unescaped » · psyche-belief › vision/datom.md

::: comment
The other alternative: the vision says what the codec does. A plain string is opaque, and balance is a structure; the Meaning has it, the string need not. Its cost is that every » inside a string is escaped.
:::

- A guillemet string is read by balance, as a Meaning is: a « » pair inside it is content, nesting to any depth, and the string closes at the guillemet that balances the one that opened it; an unbalanced guillemet inside it is escaped with a backslash.
+ A guillemet string is opaque: every glyph inside it is content, and it closes at the first » that is not escaped; a » inside it, and a backslash, are escaped with a backslash.

```datom
- «Title «The Belief Nexus made small»»
- ; the inner pair is content
- «an unbalanced \» inside»
- ; escaped, since nothing balances it
+ «Title «The Belief Nexus made small\»»
+ ; every » inside is escaped
```
