<!-- to-the-living:start -->
Presentation.{ «Clojure, the vision» }

## Proposal 1: The Clojure stack, as vision

`psyche-skills/skills/vision-clojure.md`, new

[Drawing: the stack, and where it runs]

Added, the whole skill:

```yaml
---
description: A tool or early component is begun,
  or how it is built, tested, deployed or paged
  is decided.
dependencies: [vision-datom, vision-ethos]
---
```

## Clojure for prototypes and early production

A tool or an early component is written in Clojure. Its data is EDN shaped like datom, and Malli schemas type its input and its output.

## Babashka first, a Nix-built image when deployed

Babashka runs the tool at its first use and in its Nix tests. When the tool is deployed, Nix makes the full build: a native image of the tool. Later, a pipeline reuses an image already built and available, and tests fall back to Babashka only when none is. Where disk space is tight, one Babashka serving many tools can take less room than an image for each.

## A tool pages its own output

A tool prints a short first page. When more remains, its last line says what to pass to get the next page. A caller runs the tool as the whole command and never trims its output itself.

```bash
$ status-clj '#flows []'
#flow ["d4ae97" :live]
#flow ["e51411" :live]
#flow ["88475f" :idle]
#next "#flows [3]"
$ status-clj '#flows [3]'
#flow ["b7da5d" :idle]
```

## Rust when it lasts

A prototype that becomes a lasting component is written in Ethos and generated into Rust, from its Malli schemas and its behaviour.

## Sources

d4ae97 tools
e51411 stack
88475f cljTools

Removed: the two lines proposed in «Tool Framework Study» for `mind-skills/skills/operation-system-tools.md`, which is no longer made.

- Write the tool in Clojure with a Malli schema for its input and its output; run it from source in Babashka while it is young, and build it through clj-build as a GraalVM native image once flows call it routinely.
- The tool keeps its own output small: it prints a default page and ends with `#more [offset]`, which the next call passes back as a plain number, so a caller runs the tool bare, as the whole command.

## Proposal 2: From Ethos vision to a Clojure prototype

`mind-skills/skills/operation-clojure-prototype.md`, new

[Drawing: from Ethos vision to a prototype, and on to Rust]

Added, the first lines:

```yaml
---
description: A prototype is made from an Ethos
  vision before its Rust exists.
dependencies: [vision-clojure, vision-ethos,
  knowledge-datom]
---
```

The prototype realizes what the component's vision skill and its ethos file rule, and nothing beyond them.

Each ethos type becomes a Malli schema of the same name: a struct a tuple of its positions, an enum a choice of tagged variants, a variant carrying nothing a keyword.

Each ethos kind becomes a Clojure protocol of the same name; its capabilities are the protocol's functions.

The input is one inline EDN value shaped as the root enum. The output is an enum, validated against its schema before it is printed.

The names stay the ethos names, so the Rust that ethos-zero later generates has the same types, and the prototype's recorded input and output pairs become its first tests.

```ethos
Library
[]                                   ; imports
[ LockId.Integer                     ; types
  LockName.String
  LockRequest.{ LockName Vector<String> }
  Query.[ Lock.LockRequest Release.LockId ] ]
[]                                   ; kinds
[]                                   ; associations
```

```clojure
(def LockId :int)
(def LockName :string)
(def LockRequest
  [:tuple LockName [:vector :string]])
(def Query            ; variant: a tag carrying data
  [:or (variant 'lock LockRequest)
       (variant 'release LockId)])
;; accepts  #lock ["build" ["/abs/path"]]
```

## Rulings

1. Proposal 1, the name:
   a. vision-clojure
   b. vision-tools
2. Proposal 1:
   a. land as written
   b. amend
3. Proposal 2:
   a. land as written
   b. amend
<!-- to-the-living:end -->
