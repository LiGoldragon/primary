<!-- to-the-living:start -->
Presentation.{ «Ethos: a set» }

# Ethos: a set

### Proposal 1: psyche-context › vision/ethos.md

```
+-------------+
| Flow spec   |
+-------------+
      |
   declares
      v
+-------------+
| Models      |
| Set<Model>  |
+-------------+
      |
  written as
      v
+-----------------------+
| [ Fable Opus Sonnet ] |
+-----------------------+
      |
 read by datom as
      v
+-----------------------+
| each member once,     |
| in no order           |
+-----------------------+
```

  In Imports, the paragraph that starts "An import starts with a colon".

- An import starts with a colon, followed by uncapitalized namespace segments separated by colons, ending in the type: `:namespace:sub:Type`. It is usable inline in a type declaration or a field, and the import section uses the same syntax: `:protos:String`, or `:protos:[ String Integer ]` for several. An explicit import and an intrinsic name mean the same thing. The names known without import depend on the Ethos object type; a Library, the standard library, knows String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self and Sized.
+ An import starts with a colon, followed by uncapitalized namespace segments separated by colons, ending in the type: `:namespace:sub:Type`. It is usable inline in a type declaration or a field, and the import section uses the same syntax: `:protos:String`, or `:protos:[ String Integer ]` for several. An explicit import and an intrinsic name mean the same thing. The names known without import depend on the Ethos object type; a Library, the standard library, knows String, Integer, Decimal, Boolean, Meaning, Vector, Set, Option, Result, Self and Sized.

### Proposal 2: psyche-context › vision/ethos.md

  After the Imports section, before What a declaration turns into.

```proposed
  +-------------------+  +---------------------+
  | the import        |  | a declaration or    |
  | section           |  | a field, inline     |
  +-------------------+  +---------------------+
```

+ ## A set is a set
+
+ A set holds each member once, in no order. A value that is a set has a set type: `Set<Model>`.
+
```proposed
+ Library
+ []
+ [ Model.String
+   Models.Set<Model>
+   Effort.[ Low Medium High ]
+   Main.{ Models Effort }
+   Flows.{ Vector<Main> } ]
+ []
+ []
```

### Proposal 3: mind-context › skills/knowledge-datom.md

  In Syntax, after the paragraph on the map.

  There is no map. What a map would hold is a struct when its keys are fixed, and a vector of structs when they are not.

+ A set is written as a bracket structure in a position expecting `Set<T>`. The reader refuses a repeated member; the canonical print orders members by their canonical text.
+
```proposed
+ ; in a position expecting Set<Model>
+ [ Fable Opus Sonnet ]
```
+
Ruling: land, amend, or reject.
<!-- to-the-living:end -->
