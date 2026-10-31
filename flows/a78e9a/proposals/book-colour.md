Presentation.{ «Colour in the margin» }

# Colour in the margin

Created by Fable. The builder and the Ethos and Datom grammars made by Opus.

His words, 2026-10-31: “Making all of the code blocks green or red destroys syntax highlighting so we only need that. Making all the text green or all the text red when we're using a block also is not necessary. We could just have a green margin. I understand if we're directly adding or removing, like in a block where we only mark red and green the parts that are being added or removed. Arguably they could even just be underlined if we were looking at code. That could be problematic though, because the syntax styling might all be screwed up by the fact that it's not valid code anymore (because you have the added parts and the removed parts). I don't know but at least when it's a block we could get syntax highlighting. Maybe even someone could write a very basic ethos tree sitter, syntax, and whatever all the other stuff is that is used with treesitter to create syntax highlighting.”

The builder now colours only the margin. A block added or removed whole has one green or red edge, and its text stays in the page's colour or in its language's colours. A code block changed in part is highlighted twice, once as it stands and once as proposed, each side whole and valid, and its lines are then interleaved, each signed in the gutter. Highlighting runs at build time with tree-sitter, for Rust, shell, Ethos and Datom. Before, every line of such a block was tinted green or red, and the code lost its colours. Now it shows like this:

```rust
  fn emit(&self) -> Result<Done, Error> {
-     let text = self.message.to_string();
+     let text = self.message
+         .datomize(Path::root());
      self.pane.send(text)
  }
```

### Proposal 1: Colour in the margin · psyche-belief › vision/book.md

**Comment** Green and red stay the signs; they move to the margin, and the text keeps its own colour.

- A line added shows in green.
+ A line added shows a green margin.

- A line removed shows in red.
+ A line removed shows a red margin.

+ Colour is the sign of a change and lies in the margin alone: text keeps the page's colour, and code its language's colours.

+ A code block changed in part shows each side highlighted whole as valid code, its lines interleaved, each signed in the gutter.

  A line replaced shows its removal and its addition together, and only the changed words are marked.
