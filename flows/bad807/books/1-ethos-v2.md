<!-- to-the-living:start -->
Presentation.{ «Ethos» }

Fourteen proposals and eight rulings on ethos, one change each.

## How it is now

### The vision files
- `Vision/ethos.md`, 442 lines. Its Roots: Library, Signal, Sema.
- Its headings: What Ethos is, Why Ethos, Roots, Non-repetition, Self-description, Horizon, Kind, Naming, Identity, Declaration: File, Imports, What a declaration turns into, Inline types, the two variant sections, the datom-kinds sections, Shapes and placement, Kinds are explicit, Kind syntax, Associations, Spacing, Zero, Generation.
- `Vision/sema.md`, 15 lines: Sema is the database engine, with a Sema root of record types.
- `Vision/archive-ethosMonolith.md` keeps the words behind Zero.

### ethos-zero 16.0.0
It reads four roots, Library, Signal, Operation, Memory. A `Sema` head is refused, as witnessed today:

```
Rejected.{ … { 1 1 } Conceptual.{ [ 0 ] Renamed.Memory } }
```

- It prints vertically, and drops comments from the print.
- It accepts one-field structs, and writes `Name.String` as `pub type`.
- It names a variant's inline payload `<Variant>_Data`.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 230" width="700" font-family="sans-serif" font-size="13" role="img" aria-label="ethos file to ethos-zero to Rust to the Nexus and the CLI">
<defs><marker id="p1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3d4654"/></marker></defs>
<rect width="700" height="230" rx="10" fill="#f7f8fb"/>
<rect x="12" y="55" width="140" height="64" rx="8" fill="#e6ecfa" stroke="#3b5bab"/><rect x="192" y="55" width="180" height="64" rx="8" fill="#fff1d6" stroke="#b07a12"/>
<rect x="412" y="55" width="128" height="64" rx="8" fill="#f4e4dc" stroke="#a5532e"/><rect x="578" y="20" width="110" height="56" rx="8" fill="#ddf1e4" stroke="#2f7d4a"/>
<rect x="578" y="100" width="110" height="56" rx="8" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="192" y="160" width="180" height="56" rx="8" fill="#fbe0e0" stroke="#b03a3a" stroke-dasharray="5 3"/>
<g fill="#1d2430" text-anchor="middle"><g font-weight="bold" font-size="15"><text x="82" y="82">flow.ethos</text><text x="282" y="82">ethos-zero</text><text x="476" y="82">flow.rs</text><text x="633" y="44">Nexus</text><text x="633" y="124">CLI</text><text x="282" y="185">Rejected.{ … }</text></g>
<text x="82" y="103">the ethos file</text><text x="282" y="103">canonicalize · check · generate</text><text x="476" y="103">one Rust module</text><text x="633" y="64">rkyv, no datom</text><text x="633" y="144">datom feature on</text><text x="282" y="205">the file refused</text></g>
<g stroke="#3d4654" stroke-width="1.6" fill="none" marker-end="url(#p1)"><path d="M152,87 H190"/><path d="M372,87 H410"/><path d="M540,80 L576,52"/><path d="M540,95 L576,124"/><path d="M282,119 V158"/></g>
</svg>

*How ethos-zero 16.0.0 runs today: one ethos file becomes one Rust module, which the Nexus and the CLI both compile.*

### The ethos files in the workspace
89 `*.ethos` files under `/git/github.com/LiGoldragon`, by the root they head:

| Signal | Library | Interface | Nexus | Sema | Memory | Operation |
|---:|---:|---:|---:|---:|---:|---:|
| 45 | 27 | 12 | 2 | 2 | 1 | 0 |

They hold 389 comment lines in 4,122, and 237 one-field structs in 42 files.

### Crates that pin ethos-zero
48 crates pin it: 21 at 9.0.0, 13 at 10.0.0, 3 at 16.0.0, the rest from 0.7.1 to 15.0.0.

### Where vision lives
On his order of today, vision statements migrate from Vision/ into the psyche repository as Vision-type skills.
Each [vision] proposal names its Vision/ file as its home today, and travels with the migration.

## Proposals

### 1. What Ethos is
[vision] `Vision/ethos.md`, heading What Ethos is. Ground: "effective compliance with ethos".

**Now:** "Ethos is the schema language. Of the two main syntaxes most agents will face, Ethos specifies the types and Datom fills them with data."

**Proposed:**
> "Ethos is the typed spec every Nexus is programmed from. Every runtime component is a Nexus, and every Nexus has an ethos; reading it shows the main objects and processes the component deals with.
>
> Ethos specifies the types and datom fills them with data. Ethos compiles to Rust: ethos-zero reads an ethos file and writes the Rust module the Nexus is built on."

### 2. Roots
[vision] `Vision/ethos.md`, heading Roots. Assumes (b) of Ruling 1. Ground: "signal, operation, and memory".

**Now:** "Library, Signal, Sema. No version in a file. Signal's sections are queries and responses, since there is communication; Sema's are record types, the rest to be decided. Signal gives a Nexus its main types and Sema its database types."

**Proposed:**
> "Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says: imports, queries, responses, types. Operation declares what it does, one operation for every effect: imports, operations, outcomes, types.
>
> Memory declares what it remembers: imports, record types. Library declares what they share: imports, types, kinds, associations. A signal reaches memory only through operation, and returns through operation."

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 270" width="700" font-family="sans-serif" font-size="13" role="img" aria-label="the four roots of one ethos">
<defs><marker id="p2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3d4654"/></marker></defs>
<rect width="700" height="270" rx="10" fill="#f7f8fb"/>
<rect x="15" y="25" width="190" height="96" rx="8" fill="#e6ecfa" stroke="#3b5bab"/><rect x="255" y="25" width="190" height="96" rx="8" fill="#fff1d6" stroke="#b07a12"/><rect x="495" y="25" width="190" height="96" rx="8" fill="#ddf1e4" stroke="#2f7d4a"/>
<rect x="160" y="190" width="380" height="64" rx="8" fill="#ece4f7" stroke="#6a4aa5"/>
<g fill="#1d2430" text-anchor="middle"><g font-weight="bold" font-size="15"><text x="110" y="50">Signal</text><text x="350" y="50">Operation</text><text x="590" y="50">Memory</text><text x="350" y="215">Library</text></g>
<text x="110" y="72">what a Nexus says</text><text x="350" y="72">what it does</text><text x="590" y="72">what it remembers</text><text x="350" y="236">what they share: types, kinds, associations</text>
<g font-size="12" fill="#4a5363"><text x="110" y="100">queries · responses · types</text><text x="350" y="100">operations · outcomes · types</text><text x="590" y="100">record types</text></g></g>
<g stroke="#3d4654" stroke-width="1.6" fill="none" marker-end="url(#p2)"><path d="M205,55 H253"/><path d="M445,55 H493"/><path d="M493,95 H447" stroke-dasharray="5 3"/><path d="M253,95 H207" stroke-dasharray="5 3"/>
<path d="M230,190 L130,123"/><path d="M350,190 V123"/><path d="M470,190 L570,123"/></g>
<g font-size="11" fill="#4a5363" text-anchor="middle"><text x="229" y="146">imported</text><text x="229" y="160">by each</text><text x="470" y="146">returns through</text><text x="470" y="160">operation</text></g>
</svg>

*The roots of one ethos: a signal reaches memory only through operation; Library feeds all three.*

```
Operation
[ lock:[ Lock LockName ] ]      ; imports: the types the lock Library shares
[ Take.Lock                     ; operations: one for every effect
  Free.LockName ]
[ Taken.Lock                    ; outcomes
  Failed.[ Held.Lock
           Unknown.LockName ] ]
[]                              ; types
```
ethos-zero 16.0.0 writes, derives left out:
```rust
pub enum Operation { Take(lock::Lock), Free(lock::LockName) }
pub enum Failed_Data { Held(lock::Lock), Unknown(lock::LockName) }
pub enum Outcome { Taken(lock::Lock), Failed(Failed_Data) }
```

### 3. What sema is
[vision] `Vision/sema.md`, heading What sema is. Assumes (b) of Ruling 1. Ground: "Yeah the memory is good".

**Now:** "Sema is the database engine of a Nexus, authored in Ethos so the stored types are visible; its root, Sema, declares record types. It matters more than nexus, because operational editing should yield the migration with the edit."

**Proposed:** "Sema is the database engine of a Nexus. What it stores is declared in the Memory root of the Nexus's ethos, so the stored types are visible, and an edit to that root yields the migration with the edit."

```
Memory
[ lock:[ LockId LockName FlowId ] ]   ; imports
[ Lock.{ LockId                       ; record types: one lock as stored
         LockName
         FlowId } ]
```

### 4. Everything is a type
[vision] `Vision/ethos.md`, new heading Everything is a type, after Non-repetition. Now: no such section. Ground: "everything is a variant of a set".

**Proposed:**
> "Everything is a type, because everything is a variant of a set; an instance is one member of a population. For engineering reasons not everything becomes an enum: the open-ended variants are names.
>
> Ethos has no key-value map, since a map is a poorly specified struct; a position is a type, never a key, and datom carries no field names."

```
Library
[]                                         ; imports
[ FilePath.String                          ; types: a path is its own type
  GenerationFailure.[ SyntaxError.Vector<FilePath>
                      Unwritable ] ]       ;   an enum, no keys anywhere
[]                                         ; kinds
[]                                         ; associations
```
The datom, a variant with no field names:
```
GenerationFailure.SyntaxError.[ /abs/orchestrate.ethos ]
```

### 5. An ethos edit is the data migration
[vision] `Vision/ethos.md`, new heading, after Declaration: File. Now: no such section. Ground: "which becomes the migration itself".
Assumes (b) of Ruling 6, versions held outside the file, and upgrade-from.

**Proposed:**
> "A change to ethos is operational: the edit to a Memory root is itself the operation that migrates the stored data into its new format. The Memory kind carries a standard successful or unsuccessful change on its record types, and each version carries the upgrade from the version before it.
>
> Versions are held by the Nexus that stores the records and by its manifest, never in the ethos file. Ethos is specified in its own ethos, so the same holds for ethos itself and for every proto family, datom included."

The upgrade-from choice follows a leaning he left open.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 260" width="700" font-family="sans-serif" font-size="13" role="img" aria-label="the upgrade mechanism">
<defs><marker id="p3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3d4654"/></marker></defs>
<rect width="700" height="260" rx="10" fill="#f7f8fb"/>
<rect x="10" y="20" width="200" height="56" rx="8" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="265" y="20" width="170" height="56" rx="8" fill="#fff1d6" stroke="#b07a12"/><rect x="490" y="20" width="200" height="56" rx="8" fill="#ddf1e4" stroke="#2f7d4a"/>
<rect x="250" y="110" width="200" height="56" rx="8" fill="#fff1d6" stroke="#b07a12"/>
<rect x="10" y="190" width="200" height="56" rx="8" fill="#e6ecfa" stroke="#3b5bab"/><rect x="490" y="190" width="200" height="56" rx="8" fill="#e6ecfa" stroke="#3b5bab"/>
<g fill="#1d2430" text-anchor="middle"><g font-weight="bold" font-size="15"><text x="110" y="44">Memory ethos, v1</text><text x="350" y="44">the edit</text><text x="590" y="44">Memory ethos, v2</text><text x="350" y="134">ethos-zero</text><text x="110" y="214">stored records, v1</text><text x="590" y="214">stored records, v2</text></g>
<text x="110" y="64">Lock.{ LockId LockName }</text><text x="350" y="64">adds FlowId</text><text x="590" y="64">Lock.{ LockId LockName FlowId }</text><text x="350" y="154">v2 records + upgrade from v1</text>
<text x="110" y="234">in the Nexus</text><text x="590" y="234">or the change refused</text>
<g font-size="12" fill="#4a5363"><text x="350" y="205">upgrade operation:</text><text x="350" y="242">successful or unsuccessful change</text></g></g>
<g stroke="#3d4654" stroke-width="1.6" fill="none" marker-end="url(#p3)"><path d="M210,48 H263"/><path d="M435,48 H488"/><path d="M350,76 V108"/><path d="M350,166 V196"/><path d="M210,218 H488"/></g>
</svg>

*The upgrade mechanism, not yet built: ethos-zero 16.0.0 generates no upgrade operation.*

### 6. Layout
[vision] `Vision/ethos.md`, heading Spacing, renamed Layout. Assumes (b) of Ruling 2. Ground: "a language that expands vertically".

**Now:** "Space the delimiters and the inner content. Ethos follows the canonical protos print: a space inside every bracket and brace at both ends when non-empty."

**Proposed:**
> "Ethos expands vertically. A structure with more than one element, one of which has a next layer, opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line and never takes a line of its own.
>
> Elements that are all leaves sit on one line. A space stands inside every non-empty bracket and brace. Inline nesting goes about three deep; past that, the type comes from a Library, where three more levels open."

```
Signal
[]                                   ; imports
[ Lock.{ LockName                    ; queries: take a lock by name for a flow
         FlowId }
  Release.LockId ]
[ Locked.Lock                        ; responses
  Refused.[ Held.Lock
            Unknown ] ]
[ LockId.Integer                     ; types
  LockName.String
  FlowId.Integer
  Lock.{ LockId LockName FlowId } ]
```

### 7. Comments
[vision] `Vision/ethos.md`, new heading Comments, after Layout. Assumes (a) of Ruling 5. Now: no such section. Ground: "so that I can see what the machine is seeing".

**Proposed:** "Ethos carries a comment on every section and on every line that has a next layer, saying in plain words what the machine reads there. A comment runs from ; to the end of the line, and it is kept wherever the ethos is printed."

### 8. ethos-zero prints comments
[implementation] `/git/github.com/LiGoldragon/ethos-zero/README.md`, section Print, line 156. Built on a yes to Ruling 5 (a). Ground: "what the machine is seeing".
Witness: `ethos-zero` with no argument prints `ethos-zero.ethos` without its 10 leading comment lines.

**Now:** "section on its own line; comments are not printed."

**Proposed:** "section on its own line; each comment is printed where it was written, at the end of its line or on the line above the structure it names."

### 9. Inline types
[vision] `Vision/ethos.md`, heading Inline types. Assumes (b) of Ruling 3. Ground: "a variant and a struct name be the same thing".

**Now:** "A type may be declared where it is used. The inline struct or enum is a full type whose derived name carries an underscore, non-idiomatic for a Rust type, so it never collides and reads at a glance as inferred from the sugar."

**Proposed:** "A type may be declared where it is used. A variant's inline payload is a full type that takes the variant's own name, as a struct position's inline type already does; a second declaration of that name in the file is refused as a duplicate."

```
Library
[]                                                        ; imports
[ FilePath.String                                         ; types
  GenerationFailure.[ SyntaxError.Vector<FilePath>        ;   the payload declared inline: a vector
                      Unwritable.{ FilePath String } ] ]  ;   a struct named Unwritable, after its variant
[]                                                        ; kinds
[]                                                        ; associations
```

### 10. One position is a new type
[vision] `Vision/ethos.md`, new heading, after What a declaration turns into. Assumes (a) of Ruling 4. Now: no such section. Ground: "This should be a new type".

**Proposed:** "A struct holds two or more positions. A type with one position is written as its name, a dot and the contained type, `HarnessName.String`; a struct of one position is refused. A variant with one payload carries it after the dot, with no braces."

```
Signal
[]                                         ; imports
[ HarnessStatusQuery.HarnessName ]         ; queries: the payload after the dot, no braces
[ HarnessStarted.HarnessName ]             ; responses
[ HarnessName.String ]                     ; types: one position, a new type
```

### 11. ethos-zero names payloads and refuses one-field structs
[implementation] `/git/github.com/LiGoldragon/ethos-zero/README.md`, lines 92 and 93. Built on a yes to Ruling 3 (b) and Ruling 4 (a). Ground: "refuse single-field struct types".
The refusal would meet 237 one-field structs in 42 of the 89 files.

**Now:** "capture those names. A variant `Name.{ T1 T2 }` carries a generated struct `Name_Data` with one field per position."

**Proposed:** "capture those names. A variant `Name.{ T1 T2 }` carries a generated struct `Name` with one field per position. A struct of one position, `Name.{ T }`, is refused as `Conceptual.{ [ path ] OnePosition.Name }`."

### 12. Kind
[vision] `Vision/ethos.md`, heading Kind. Assumes (b) of Ruling 7. Ground: "If I say traits I mean kinds".

**Now:**
> "Kind is the word for the bearer of capabilities: something that can run is a runner, Runnable is its kind, and run is its capability, a function the kind has. Trait is set aside as acoustically ambiguous.
>
> In ethos there are no generics, only kinds. Declaring a new kind declares a new trait in the Rust world and might imply more in the ethos world."

**Proposed:**
> "Kind is the word for the bearer of capabilities: something that can launch is launchable, Launchable is its kind, and launch is its capability. When trait is said, kind is meant; trait stays the Rust word for what a kind generates.
>
> In ethos there are no generics, only kinds: what a capability takes is another kind, never a type. Declaring a new kind declares a new trait in the Rust world."

```
Library
[ protos:Textualizable ]                   ; imports
[ LaunchError.[ Busy Unreadable ] ]        ; types
[ Launchable.[ launch!{ [ Textualizable ]  ; kinds: a launchable takes a textualizable brief
                        [ Result<Self LaunchError> ] } ] ]
[]                                         ; associations
```
ethos-zero 16.0.0 writes, derives left out:
```rust
pub trait Launchable {
    fn launch<N: protos::Textualizable>(&mut self, input: N) -> std::result::Result<Self, LaunchError>
    where Self: Sized;
}
```

### 13. Horizon
[vision] `Vision/ethos.md`, heading Horizon. Assumes (a) of Ruling 8 for today. Ground: "write the whole program directly in Ethos".

**Now:** "Ethos will eventually replace everything, Rustlang becoming its assembly layer. Designs are chosen for that horizon; what it enables — generator emission among it — comes in its time."

**Proposed:**
> "Ethos will eventually replace everything, Rust becoming its assembly layer. Today ethos declares the types and kinds and ethos-zero compiles them to Rust; the bodies are written by hand, in Rust shaped so that a signal reaches memory only through operation.
>
> The whole program written in ethos needs a function syntax, implementations on kinds, and a manifest for compiling and finding dependencies."

### 14. Move the 9.0.0 pins to 16.0.0
[implementation] `/git/github.com/LiGoldragon/signal-harness/Cargo.toml`, line 28, and the same line in the 20 other crates pinned to 9.0.0. Each crate is regenerated and its rkyv dependency added.
Rests on a witness, no record of his: 9.0.0 reads no Operation or Memory root.

```toml
# Now
ethos-zero = { git = "https://github.com/LiGoldragon/ethos-zero", rev = …the 9.0.0 commit }
# Proposed
ethos-zero = { git = "https://github.com/LiGoldragon/ethos-zero", rev = …the 16.0.0 commit }
```
The 20 other crates:
```
chroma                   claude-answers           meta-signal-aggregator
meta-signal-criome       meta-signal-harness      meta-signal-mentci
meta-signal-mirror       meta-signal-persona      meta-signal-repository-ledger
meta-signal-router       meta-signal-spirit       signal-aggregator
signal-criome            signal-introspect        signal-mentci
signal-mind              signal-repository-ledger signal-router
signal-spirit            signal-spirit-judge
```

## Rulings

| Ruling | (a) | (b) |
|---|---|---|
| **1. Roots** | Three roots, Library, Signal, Sema: `Vision/ethos.md` Roots; 2026-09-10. | Four roots, Library, Signal, Operation, Memory: 2026-10-02. |
| **2. Layout** | One declaration per line, delimiters spaced, as the protos print: `Vision/ethos.md` Spacing, as of 2026-09-11, dated by commit. | Vertical expansion about three deep, the closing delimiter ending the last line: 2026-10-02. |
| **3. The name of a variant's inline payload** | Derived with an underscore, `Unwritable_Data`, so it never collides: 2026-09-09; ethos-zero 16.0.0. | The variant's own name, shared by variant and struct: 2026-09-30. |
| **4. One-field structs, and what `Name.String` declares**<br>The flow reads the second as part of the first, a departure from the new-type form he asked for. | A one-field struct is refused, and `Name.String` is a new type of its own: 2026-09-08. | A one-field struct is accepted, and `Name.String` is a Rust alias, `pub type Name = String`, bearing no derive: `Vision/ethos.md`; ethos-zero since 2026-09-10, dated by commit; 42 files use it. |
| **5. Comments** | A comment on every section and next-layer line, kept: 2026-10-03. | Comments read and dropped from the print: ethos-zero README, 16.0.0, 2026-10-02, dated by commit. |
| **6. Versions** | No version in an ethos file: 2026-09-09. | Ethos versions, each with its upgrade: 2026-09-29; 2026-10-02. |
| **7. Trait or kind** | Trait set aside as acoustically ambiguous: 2026-08-26. | Kind meant when trait is said, trait still said for Rust: 2026-09-11; 2026-09-24. |
| **8. Bodies by hand, or the whole program in ethos** | Ethos types and kinds, implementations written by hand: 2026-10-04. | The whole program in ethos within a few months: 2026-09-25; 2026-09-29. |
<!-- to-the-living:end -->
