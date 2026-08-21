# Import Resolution — World Map

Drafted for psyche review, design session `2b34fafa`, 2026-08-21.
Ordered: "of course" (worldModelBeforeCode.md 2026-08-21), after the
map framing — ontology, anatomy, an object/capability-oriented layout
— was confirmed as the Ethos interface file's role.

This is a map of the world, not of the process. It contains no steps.
Things, what each contains, what each can do. Resolution appears only
as a walk across the map, at the end. No signatures anywhere — the
signature is code, and code comes after the map is approved.

Every claim is grounded in a ruling or marked as proposal/open.

---

## 1. The Things

### AssembledSource (added in review, 2026-08-21)
The top-level world object — what the program goes for: "What you're
going for is not text. It's the assembled source, which would include
the manifest." (mainFunction.md 2026-08-21).

Contains:
- the **Manifest**
- the **Source(s)** reachable through it (and thereby the Files)

This names the world the resolution walk crosses: an ImportReference
resolves *within* an AssembledSource. The "thing plus its context"
pairing the walk needed is not an awkward helper — it is this obvious
world object. Built by the two-things rule: "if you build a thing
from two things... create a new type that can be created" (same
entry).

Capabilities: none beyond being creatable (its TryFrom origin is
undesigned — see open question 7).

### Source
The crate-unit. "source will be the name we use instead of crate"
(sourceNotCrate.md 2026-08-20).

Contains:
- **Files**, in a directory tree from the source root
- one distinguished File: **lib.es**, the default pull target —
  "`signal-pysche:Object` pulls Object from lib.es" (importResolution.md
  2026-08-20)

Capabilities: none on this map. A source is a container.

### File
The unit of source text. "What's wrong with File?" — File is the
type; "document" is dead (ethosSourceFiles.md 2026-08-20). One .es
file is one Rust module, for the monolith ("easy cognition is the
first safe bet", same entry). No namespace inside a file —
"ridiculous... foundation, not wallpaper" (ethosNamespaces.md
2026-08-20).

Contains:
- **type declarations** — where TypeNames denote something
- **import references** — imports are written in files; local
  references resolve from the containing File's directory
  (importResolution.md 2026-08-20)

Lives at: a FilePath within a Source's tree (or a plain directory,
for purely local work).

Capabilities: none on this map.

### ImportReference
What exists where an import is written. "I dont think Import is a
type; there are no Import's; what exists is an import reference"
(importResolution.md 2026-08-20).

Two forms (whether these are one universal thing whose form varies,
or two things, is OPEN — question 2):

**External pull** — the colon form. Contains:
- a **SourceName** (before the colon)
- a **FilePath** within that source, optional — absent means lib.es
- one **TypeName** or a list — `signal-pysche:stream.[Stream
  Termination]` (importResolution.md 2026-08-20)

**Local** — the bare path, no colon. Contains:
- a **FilePath** relative to the containing File's directory
- the TypeName(s)

The import reference contains every name it is about. That is why it
is the resolvable thing: "if the type needs a 'name' to resove the
import, then it's not resolvable" (importResolution.md 2026-08-20) —
the thing that already carries the name needs none handed in.

Capabilities: **Resolve** — the only behavior on this map. Placed
here by the placement law: the capability sits on the thing that
contains its subject.

### Manifest
Written in datom; to be specced ("which we must spec obviously",
importResolution.md 2026-08-20). Where it lives is OPEN — question 3.

Contains:
- associations **SourceName → Source** (an entry points a name at a
  source root)

Capabilities: **none — and this is the map's sharpest consequence.**
The manifest does not "resolve a name"; it *has* entries. Lookup is
containment traversed, not behavior performed. A table has; it does
not do. (See §3, non-things: Resolver.)

### The name things
- **SourceName** — the name before the colon; meaningful only
  through a Manifest association. Manifest miss = error, no fallback
  ("confirmed, kill the fallback", importResolution.md 2026-08-20).
- **FilePath** — path inside a source; `/` is the directory
  separator; `.` separates the file from the imported type or `[...]`
  list (importResolution.md 2026-08-20). The `.es` extension itself is
  an open side question, unruled.
- **TypeName** — what an import reference pulls; denotes a
  declaration in a File.

### The referent (proposed, unnamed)
What a TypeName denotes once the walk arrives: a type declaration in
a File. Whether this is its own thing on the map, and what its name
is, is OPEN — question 1. Not designed here.

---

## 2. The Map

```
Manifest
 └─ has: SourceName ──▸ Source
                         └─ has: File tree (root; lib.es default)
                                  └─ has: type declarations
                                  └─ has: ImportReferences
                                            │ contains: SourceName? FilePath? TypeNames
                                            ● Resolve   ← the map's only behavior
```

Every arrow is containment or reference — structure, not steps.
Textual/real twins: each thing here is drawn in its real form; its
textual twin carries Realize and the real thing carries Textualize,
per the ruled pair ("You dont textualize the text, and you dont
realize the realized data", traitsAsCapabilities.md 2026-08-18).
Drawn once as a law of the whole map, not as per-thing edges.

---

## 3. Non-Things

Dead by ruling, or never things at all. Listed so the next
implementer does not resurrect them.

| Non-thing | Why it is not on the map |
|---|---|
| Import | "there are no Import's" (importResolution.md 2026-08-20) |
| Document | File is the type (ethosSourceFiles.md 2026-08-20) |
| Namespace (in a file) | "ridiculous... wallpaper" (ethosNamespaces.md 2026-08-20) |
| Manifest-miss fallback | "kill the fallback" (importResolution.md 2026-08-20) |
| **Resolver** | Never a thing: a step of the walk dressed as a thing. The rejected sketch's `Resolving`/`FileYielding`/`ReferenceResolving` were the process view leaking into the ontology — two of the three drew *containment* (manifest entries, source files) as *behavior* (traitsAsCapabilities.md 2026-08-20; reports/CostumeTraitFingerprint-2026-08-20.md) |

---

## 4. Resolution — the Walk

The process falls out of the map; it is not on it. Resolve, the
ImportReference's capability, is this walk:

**External (colon form):**
its SourceName → through the Manifest's associations → a Source
→ its FilePath (or lib.es) → through the Source's tree → a File
→ its TypeNames → among the File's declarations → the referents.

**Local (bare path):**
its FilePath → from the containing File's directory → a File
→ its TypeNames → the referents.

Faults: the walk errors at the first missing edge — no manifest
entry (ruled: error, no fallback), no such file, no such declaration.
One walk, one fault family.

Note what dissolved: the "environment problem" (may the manifest be
an argument?) was an artifact of the service framing. On the map, the
walk *crosses other things' contents* — and the world it moves
through now has its name: the AssembledSource, which includes the
manifest (mainFunction.md 2026-08-21). How the world is reached at
implementation time is a code question, decided after this map is
approved, within the law: the subject is never handed in.

---

## 5. Open Questions

1. **What Resolve yields**: the File, the declarations, or both in
   stages (the morning entry staged source → file)? The referent
   thing is unnamed.
2. **One ImportReference or two**: is the local form the same
   universal thing as the external pull with absent SourceName
   (echoing Block: one type, form varies), or a different thing?
3. **The Manifest's spec and home**: per workspace? per source?
   Ordered specced; not yet designed.
4. **`.es` extension**: posed as an open side question, unruled.
5. **The colon tension**: 2026-08-07 moved imports off `:`; the
   2026-08-20 colon pull revises it; the noted reconciliation
   (placement law) is posed to the psyche, unanswered
   (importResolution.md 2026-08-20).
6. **The walk's implementation home**: at code time the walk may
   need a walk-state thing (as StructuralWalk is to the protos walk).
   That is implementation anatomy, decided after this map — flagged
   only so it does not get invented ad hoc as a "Resolver."
7. **AssembledSource's origin**: what it is TryFrom (a workspace
   root? a manifest path?) — undesigned; and whether assembly itself
   performs resolution of all import references, or resolution
   happens per-reference against the assembled world afterward.

---

## 6. Destination Form

This map's destination is the Ethos interface file — "yes, except
that it isnt ready to use yet, so the model writes the ethos but has
no way to run it (yet)" (worldModelBeforeCode.md 2026-08-21). The
Ethos rendering is deliberately not attempted in this draft: the
declaration-form syntax rulings are not reacquired in this session,
and guessed syntax would be false confidence. Once the map's content
is approved, rendering it as Ethos — unrunnable for now — is the
next act.
