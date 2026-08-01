# Three-Layer Naming, Capsules, Sugar Doctrine, Nomos Bootstrap — 2026-08-01

Psyche vision session continuing the review of the codex research agenda
(`reports/protosVisionReacquisition/2-Research-...`), answering the manager's
item-kind menu. Agent text answered: the sixteen-item enumeration of
programming-language item kinds and the observation that file kinds are
compositions from that menu. Grades follow the corpus vocabulary;
psyche-verbatim quotes are condensed from spoken dictation.

## 1. Three-layer naming — adopted

**[psyche-ruled]** "There's one design that keeps coming back... I think now
talking about it that we should just go for this." Reviewed against the
manager before Spirit capture, per his request. The three layers:

1. **True name** (absolute name, content address): "the true name is
   something that truly differentiates one object from another." Derived from
   content, so it changes on every edit; unusable as the working reference
   because an edit would cascade renames recursively through every referring
   object.
2. **Encoded name**: the stable identity minted when a new concept is
   introduced. The encoded form references objects through it, so an object
   can mutate without deep database-wide renaming. A table maps encoded name
   to current true name.
3. **Visible name** (symbolic, textual, human): natural-language pointers for
   capsule/textual views. Changeable freely without touching the encoded
   name's pointer to the true name.

**[psyche-ruled]** Open sub-choice, explicitly to be weighed: the encoded
name's minting scheme — (a) the true name of the object's first version
(typed, so no confusion with live true names; creates a traceability chain
for recovery/debugging), or (b) a random number (hash-map-style, balancing
benefit).

**[psyche-verbatim]** context: imports "are just something that we see in the
textual form... it's represented differently in encoded form. Because there
you address things absolutely."

## 2. Correctness-over-machinery principle (Spirit-grade candidate)

**[psyche-verbatim, condensed]**: "Another aspect of my psyche's spirit: when
more correctness is introduced in an engine, in a design, in an architecture,
the gain in correctness more than makes up for the added machinery. And as
the system expands, this layer of better correctness is going to make the
expansion much more simple and natural." He flagged this as Spirit material
to be captured after review with the manager. Capture pending psyche approval
of exact wording; Spirit daemon status must be checked (corpus records it
down since 2026-07-24; offline queue is `spiritbackup.nota`).

## 3. Spirit redefinition (doctrine correction, port pending approval)

**[psyche-verbatim, condensed]**: "I know I've been using the word intent
when it deals with spirit, but it's inappropriate. The thing that spirit
contains is spirit — the psyche's spirit. It's the computer representation of
the psyche's spirit. Like the vision: vision is a living thing which you
don't have access to. You have to use your limited inference ability to try
to infer what the vision is, just like you have to try to infer what the
spirit is." Also observed: Spirit has fallen by the wayside; agents have not
been consulting it. Doctrine surfaces (AGENTS.md Intent section, intent-log
skill naming) will need porting; skill edits require explicit approval and go
through the skills source repository.

## 4. Transactional editing horizon

**[psyche-vision]**: the aim is programmatic/transactional editing. Text
source files are bootstrap. Eventually the engine holds the source in
encoded form; a user pulls a representation ("we'll ask the engine to see
certain parts and it will just represent it to us in this textual form").
The source lives in the engine, not in files.

## 5. Capsule is a program, not a file

**[psyche-vision, lean]**: "an Ethos source file should not correspond with a
capsule. I think a capsule basically corresponds with the idea of a
program." With encoded/true names and a registry, capsules populate from
names without a file concept. Rendering a capsule to text is a **balanced
distribution** of content into reasonably and comparably sized files (known
balancing algorithms suffice); files in are not files out — no one-to-one
round trip at file granularity. Import and export sections are **derived
views**: "a function of what this file needs internally and what is needed
externally by other files from this file." Public/private is not a deep
concern; much of it is sugar. He also noted a possible naming gap: "maybe
there's a sub component here that deserves its own name" for the per-object
capsule-like unit.

## 6. Sugar doctrine: today's language surface is mostly sugar

**[psyche-vision]**:

- **main is sugar**: "the main function in a Rust program is sugar because it
  really is a trait on a particular object — the main execution thread —
  which has its own data: stdin, stdout, shell environment, argv."
- **Generics are Nomos objects**: "generics would be a certain kind of
  transformer object... a Nomos thing" whose strictly typed declaration has
  positions indicating the generic type slots and required contracts.
- **Attributes/metadata are Nomos objects**: "more complex objects created in
  Nomos to expose functionality that somebody wants in Ethos."
- **Per-need method**: "If we need a certain kind of object, we find the
  pattern it fits, we create the Nomos transformer for it that gives it the
  most elegant syntax — meaning it only lets us write the bits that change."
- **Implication**: the wire-type concept — composing a wire object implies
  rkyv serialization and friends automatically. "We get rid of a lot of the
  noise, the assembly feel of Rust, and create what a lot of people have been
  trying to do: a beautiful language that also compiles correctly."

## 7. FFI belongs in Logos

**[psyche-lean]**: foreign interfaces need a Logos facility (this is where
Logos could actually be authored), exposed through a specialized Nomos
object.

## 8. Nomos bootstrap and the self-hosting loop

**[psyche-vision, with an explicit bootstrap lean]**:

- **Bootstrap mandate (near-term option)**: "we could, for now, just mandate
  that every new Nomos object have a corresponding type created by hand in
  Rust, which would closely mirror its equivalent Logos type — similar
  structure, but different actual types for its fields," the fields holding
  promise/unknown values to be evaluated from the Ethos payload. "...which
  might be the way to bootstrap."
- **The closing of the loop (self-hosting moment)**: a specialized Nomos
  object takes Ethos type declarations and outputs **two** Logos types: (1)
  the final Logos object with its proper types, and (2) a similar-structure
  variant whose fields hold a "promise for something or possible something" —
  fixed fields known at Nomos parse time, varying fields filled by the Ethos
  payload. "So then the transformation trait from Ethos to Logos can be
  fulfilled properly without handwriting a bunch of Rust types and
  individually writing implementations for every Nomos object."
- [agent-inference] This answers the generation question left open by the
  mirror-types research (`reports/NomosLogosMirrorTypesResearch-2026-07-31.md`)
  and the codex hybrid's generation hinge: the mirror-pair generator is
  **Nomos itself**, not proc macros — consistent with the syn/quote ban.
  Handwritten mirrors are scaffolding for the bootstrap phase only, not
  architecture.

## Open sub-questions surfaced here

- Encoded-name minting scheme: first-version true name vs random (section 1).
- The name for the per-object capsule-like unit (section 5).
- Exact shape of the promise/unknown field types in the mirror variant
  (section 8; "there was a few ideas floating around").
- Spirit capture wording for the correctness principle (section 2) and the
  doctrine port of the Spirit redefinition (section 3), both pending
  approval.
