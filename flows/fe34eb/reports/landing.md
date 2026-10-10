# Landing — the distilled-vision edits approved in flow fe34eb

Flow fe34eb, 2026-09-10. The living's final word was "yes, everything
is approved". The approved wording was taken from the main flow's
transcript, session `fe34eb91-2f5b-48bf-bc19-24d6b5fcc36e`, latest
version of each proposal. The raw records the edits distill are
`flows/fe34eb/vision/{nexus,signal,ethos,datom}.md`.

## Vision files changed

### Vision/nexus.md

- Heading **A kind of thing**: "A Nexus is not a thing; it is a kind
  of thing." replaced by "Nexus is our word for the style of component
  that speaks signal and uses a similar database. A Nexus is a daemon,
  amongst other things; the headings below say what else."
  Source: flows/fe34eb/vision/nexus.md, entries of 2026-09-10 on the
  word Nexus and on a nexus being a daemon amongst other things.
- Heading **The nexus core** dropped entirely (it carried the nexus
  core / nexus kernel and its input and output Ethos sections).
  Source: flows/fe34eb/vision/nexus.md, "the nexus-core runtime
  concept was overthinking".
- Heading **Library and daemon**: "Nexus is the universal library for
  all nexuses; the daemon lives in Ethos Zero." replaced by "Every
  component built from now on is a Nexus. The nexus repository is the
  library that defines the core of a Nexus component."
  Source: flows/fe34eb/vision/nexus.md, "a nexus is a daemon; the
  nexus repo is the library that defines the core of a nexus
  component".
- Heading **Routing**: "held in a universal signal repository every
  component depends on" became "held in the signal repository, which
  every component depends on". The sentence was reordered so the
  trailing "which wraps the objects" clause still reads: "The router
  tells signal types apart by an enum that wraps the objects, held in
  the signal repository, which every component depends on."
  Source: flows/fe34eb/vision/signal.md, "shouldnt it just be
  'signal'?".
- Heading **Processing is for the effect** left as it stands, as
  approved.

### Vision/signal.md

- Heading **Universal signal** ("Universal signal is a CapnProto
  implementation of Ethos. Not built.") replaced by heading
  **Protocol**: "Signal is portable rkyv plus whatever protocol is
  standardized on top of it. The protocol is to be decided."
  Source: flows/fe34eb/vision/signal.md, "portable rkyv + whatever
  protocol we decide to standardize".

### Vision/ethos.md

- Heading **Roots**: now "Library, Signal, Sema. No version in a file.
  Signal's sections are queries and responses, since there is
  communication; Sema's are record types, the rest to be decided.
  Signal gives a Nexus its main types and Sema its database types."
  Nexus is gone from the roots list and the input and output sections
  with it.
  Source: flows/fe34eb/vision/nexus.md, "the nexus-core runtime
  concept was overthinking".
- New heading **Zero**: "Ethos Zero was first named Ethos Monolith;
  the two are the same thing. Zero as in version 0: no daemon yet, no
  Nexus. The ethos repository is for the ethos nexus that follows."
  Source: flows/fe34eb/vision/ethos.md, "Ethos Monolith and Ethos Zero
  are the same thing".
- Heading **Generation**: now "By request to ethos-zero, which is not
  a daemon, hence its name; committed, held fresh by a test. The ethos
  repository is for the upcoming ethos nexus."
  Source: flows/fe34eb/vision/ethos.md, "ethos-zero is not a daemon,
  hence its name".

No example in Vision/ethos.md showed a Signal with a Nexus root, and
no Nexus root appears anywhere else in Vision/. The Roots edit was the
only change item 3 called for. Checked: Vision/{ethos,sema,datom,
protos}.md.

### Vision/datom.md

- Heading **Strings**: "its name is open, symbol being Lisp's" removed;
  the form is now named from the living's words — "The bare form, whose
  name is bare: ... It is a bare string, undelimited because it needs
  no delimiters."
  Source: flows/fe34eb/vision/datom.md, "only if it's a bare
  (undelimited because it doesnt need delimiters) string".

### Vision/ethosMonolith.md retired

Moved to `Vision/archive-ethosMonolith.md` with a note that the living
ruled Ethos Monolith and Ethos Zero the same thing and that what still
stands is carried by Vision/ethos.md, heading Zero. Every word kept.
`Vision/sources/ethosMonolith.md` is left in place as the trace of the
retired topic.

### Sources appended

One line each, per the distillation skill:

- Vision/sources/nexus.md — `fe34eb nexus`
- Vision/sources/signal.md — `fe34eb signal`
- Vision/sources/ethos.md — `fe34eb ethos`
- Vision/sources/datom.md — `fe34eb datom`

## Raw records swept

The living's instruction: no raw vision left around talking about a
Nexus runtime concept. Searched `flows/*/vision/`, `flows/*/notion/`
and `vision-raw/` for nexus core, nexus kernel, nexus-core, Nexus
runtime, Nexus root, "Nexus part", execution engine, input and output
as Nexus sections, and ethos-monolith. Nothing was deleted.

Moved into the archive:

- `flows/e06e4c07/vision/nexus.md` — the 2026-08-19 dictation whose
  words are "there's the Nexus part, which is the execution engine
  inside a Nexus". The whole record moved into
  `flows/e06e4c07/vision/archive-nexus.md`; the source file is gone,
  which is the archive practice and matches the `e06e4c07 nexus` line
  already standing in Vision/sources/nexus.md. A supersession note was
  written under it.

Already in archive files, annotated as superseded by the fe34eb
records (the nexus-core rulings):

- `flows/564f55/vision/archive-nexus.md` — "the nexus core, the nexus
  kernel ... input and output may be its words".
- `flows/564f55/vision/archive-ethos.md` — the two 2026-09-09 entries
  placing input and output in the nexus core and giving Nexus its own
  sections; the note sits after both.
- `flows/acbb6006/vision/archive-nexus.md` — "The engine inside a
  Nexus is Nexus Core"; the note sits after that entry.
- `flows/e06e4c07/vision/archive-nexus.md` — the entry proposing
  NexusCore as the execution heart.

Annotated as superseded by the Ethos Monolith = Ethos Zero ruling:

- `flows/aa4c7747/vision/archive-ethosMonolith.md`
- `flows/b675f3d9/vision/archive-ethosMonolith.md`
- `vision-raw/archive-threeStacks.md`
- `vision-raw/archive-rustComponentArchitecture.md`

(The last three plus aa4c7747 are exactly the sources listed in
Vision/sources/ethosMonolith.md.)

Found and left alone, since they name ethos-monolith only as a
repository or a stage in passing and carry no Nexus runtime concept:
`flows/01a02fd5/vision/interfaces.md`,
`flows/2b34fafa/vision/rustComponentArchitecture.md`,
`flows/aa4c7747/vision/orchestrate.md`,
`flows/acbb6006/vision/distillation.md`,
`vision-raw/mainFunction.md`.

## Item 8 — repositories

Repositories root is `/git` (SKILL_VARIABLES.md), the checkout root
`/git/github.com/LiGoldragon`, 192 repositories. Nothing was touched
there.

- **ethos-monolith**: no such repository, locally or remotely. Nothing
  under `/git` matches `*monolith*`. `gh api
  /repos/LiGoldragon/ethos-monolith` redirects and answers
  `LiGoldragon/ethos-zero`: the GitHub repository was renamed, which is
  the living's ruling witnessed in the forge.
- **signal**: a repository and crate named `signal` does exist —
  `/git/github.com/LiGoldragon/signal`, crate `signal` 0.1.0,
  described as "sema/criome record vocabulary with a local legacy wire
  envelope". Last commit 2026-08-13, and its recent commits are about
  dropping pointers to the deleted nexus repo. It belongs to the
  legacy stack: it depends on dotos, signal-sema and signal-derive,
  not on protos or datom-codec, and only `signal-forge` depends on it.
- **signal-standard**: `/git/github.com/LiGoldragon/signal-standard`,
  crate `signal-standard` 1.0.0, "Shared cross-component standards:
  the reconciled ComponentKind roster, the differentiator, and the
  authorized-object interest lattice". It carries an `ethos/`
  directory and generates its Rust through `ethos-zero` in `build.rs`,
  so it is on the current stack; last commit 2026-09-10. This is the
  shared taxonomy — the enum-and-common-payload role the Routing
  statement describes. Its dependents are the legacy meta-signal-*
  and component repositories.
- **signal-frame**: `/git/github.com/LiGoldragon/signal-frame`, crate
  `signal-frame` 0.4.0, "Signal frame mechanics: envelope,
  length-prefixed rkyv archives, handshake, exchange identifiers,
  async correlation, streams, reply plumbing". Last commit 2026-08-26.
  This is the wire kernel — the framing the living marked TBD today as
  "whatever protocol we decide to standardize".

So the two are not rivals for one name: signal-standard is the shared
vocabulary a router would tell types apart by, signal-frame is the
wire mechanics. The legacy `signal` repository holds the name today.
Note for the living's decision: lojix, the only realized Nexus,
depends on neither — its signal repositories are `signal-lojix` and
`meta-signal-lojix`, generated per socket, and no shared signal
repository is in its dependency graph. Nothing named `signal` is a
dependency of anything on the current stack.

## Not landed

- **Tension left standing in Vision/nexus.md.** The heading "A Nexus
  is the whole" still says "Daemon is retired as the name of the
  thing", while the approved "A kind of thing" now says "A Nexus is a
  daemon, amongst other things". No wording was approved for that
  heading, so it was left as it stands; it wants a ruling.
- **Repetition between Ethos's Zero and Generation headings.** Both
  approved wordings say the ethos repository is for the ethos nexus.
  Both were landed verbatim as approved; the duplicate line is worth
  a later trim.
