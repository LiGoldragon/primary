<!-- to-the-living:start -->
Presentation.{ «Ethos» }

How it is now. `Vision/ethos.md` (442 lines) holds What Ethos is, Why Ethos, Roots, Non-repetition, Self-description, Horizon, Kind, Naming, Identity, Declaration: File, Imports, What a declaration turns into, Inline types, the two variant sections, the datom-kinds sections, Shapes and placement, Kinds are explicit, Kind syntax, Associations, Spacing, Zero, Generation; its Roots are Library, Signal, Sema. `Vision/sema.md` (15 lines) names Sema the database engine with a Sema root of record types; `Vision/archive-ethosMonolith.md` keeps the words behind Zero. ethos-zero 16.0.0 (`/git/github.com/LiGoldragon/ethos-zero`, `c2653dd`, 2026-10-03) reads four roots, Library, Signal, Operation, Memory, and refuses a `Sema` head (witnessed 2026-10-04: `Rejected.{ … { 1 1 } Conceptual.{ [ 0 ] Renamed.Memory } }`); it prints vertically, drops comments from the print, accepts one-field structs, writes `Name.String` as `pub type`, and names a variant's inline payload `<Variant>_Data`. The 89 `*.ethos` files under `/git/github.com/LiGoldragon` head 45 Signal, 27 Library, 12 Interface, 2 Nexus, 2 Sema, 1 Memory, none Operation; they hold 389 comment lines in 4,122 and 237 one-field structs in 42 files. Of the 48 crates that pin ethos-zero, 21 pin `b232d35e` (9.0.0), 13 `4bf73cae` (10.0.0), 3 `c2653dd8` (16.0.0), the rest 0.7.1 to 15.0.0. On his order of today, vision statements migrate from Vision/ into the psyche repository as Vision-type skills; each [vision] proposal names its Vision/ file as its home today and travels with the migration.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 300" width="700" font-family="sans-serif" font-size="14">
<defs><marker id="a1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>
<rect width="700" height="300" fill="#fff"/>
<g fill="#eef2f7" stroke="#333">
<rect x="10" y="20" width="140" height="50" rx="6"/><rect x="190" y="20" width="140" height="50" rx="6"/><rect x="370" y="20" width="140" height="50" rx="6"/><rect x="550" y="20" width="140" height="50" rx="6"/>
<rect x="10" y="120" width="160" height="40" rx="6"/><rect x="185" y="120" width="160" height="40" rx="6"/><rect x="360" y="120" width="160" height="40" rx="6"/><rect x="535" y="120" width="155" height="40" rx="6"/>
<rect x="230" y="200" width="240" height="40" rx="6"/><rect x="60" y="255" width="230" height="36" rx="6"/><rect x="410" y="255" width="230" height="36" rx="6"/>
</g>
<g fill="#111" text-anchor="middle">
<text x="80" y="42">flow.ethos</text><text x="80" y="60" font-size="12">sweet form</text>
<text x="260" y="42">canonicalize</text><text x="260" y="60" font-size="12">sweet → braced</text>
<text x="440" y="42">check</text><text x="440" y="60" font-size="12">or Rejected.{ … }</text>
<text x="620" y="42">generate</text><text x="620" y="60" font-size="12">one Rust module</text>
<g font-size="12"><text x="90" y="138">Library →</text><text x="90" y="154">types, traits</text><text x="265" y="138">Signal →</text><text x="265" y="154">Query, Response</text>
<text x="440" y="138">Operation →</text><text x="440" y="154">Operation, Outcome</text><text x="612" y="138">Memory →</text><text x="612" y="154">records</text></g>
<text x="350" y="225">flow.rs, committed, held fresh by a test</text>
<text x="175" y="278">Nexus: rkyv, no datom</text><text x="525" y="278">CLI: datom feature on</text>
</g>
<g stroke="#333" marker-end="url(#a1)" fill="none">
<path d="M150,45 H188"/><path d="M330,45 H368"/><path d="M510,45 H548"/>
<path d="M620,70 L90,118"/><path d="M620,70 L265,118"/><path d="M620,70 L440,118"/><path d="M620,70 L612,118"/>
<path d="M90,160 L330,198"/><path d="M265,160 L340,198"/><path d="M440,160 L360,198"/><path d="M612,160 L380,198"/>
<path d="M300,240 L190,253"/><path d="M400,240 L510,253"/>
</g>
</svg>

Figure: how ethos-zero 16.0.0 runs today. One ethos file becomes one Rust module: each root yields its enums, and the Nexus and the CLI compile the same types, the CLI with datom.

1. [vision] `Vision/ethos.md`, heading What Ethos is.
   Now: "Ethos is the schema language. Of the two main syntaxes most agents / will face, Ethos specifies the types and Datom fills them with data."
   Proposed: "Ethos is the typed spec every Nexus is programmed from. Every runtime component is a Nexus, and every Nexus has an ethos; reading it shows the main objects and processes the component deals with. Ethos specifies the types and datom fills them with data. Ethos compiles to Rust: ethos-zero reads an ethos file and writes the Rust module the Nexus is built on."
   Ground: 2026-10-04, 5ed94b, "effective compliance with ethos".

2. [vision] `Vision/ethos.md`, heading Roots. Assumes (b) of Ruling 1.
   Now: "Library, Signal, Sema. No version in a file. Signal's sections are / queries and responses, since there is communication; Sema's are record / types, the rest to be decided. Signal gives a Nexus its main types and / Sema its database types."
   Proposed: "Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says: imports, queries, responses, types. Operation declares what it does, one operation for every effect: imports, operations, outcomes, types. Memory declares what it remembers: imports, record types. Library declares what they share: imports, types, kinds, associations. A signal reaches memory only through operation, and returns through operation."
   Ground: 2026-10-02, 91ea9f, "signal, operation, and memory".

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
```rust
// generated by ethos-zero 16.0.0; derives and #[rustfmt::skip] left out here
pub enum Operation { Take(lock::Lock), Free(lock::LockName) }
pub enum Failed_Data { Held(lock::Lock), Unknown(lock::LockName) }
pub enum Outcome { Taken(lock::Lock), Failed(Failed_Data) }
```

3. [vision] `Vision/sema.md`, heading What sema is. Assumes (b) of Ruling 1.
   Now: "Sema is the database engine of a Nexus, authored in Ethos so the / stored types are visible; its root, Sema, declares record types. It / matters more than nexus, because operational editing should yield the / migration with the edit."
   Proposed: "Sema is the database engine of a Nexus. What it stores is declared in the Memory root of the Nexus's ethos, so the stored types are visible, and an edit to that root yields the migration with the edit."
   Ground: 2026-10-02, 91ea9f, "Yeah the memory is good".

```
Memory
[ lock:[ LockId LockName FlowId ] ]   ; imports
[ Lock.{ LockId                       ; record types: one lock as stored
         LockName
         FlowId } ]
```

4. [vision] `Vision/ethos.md`, new heading Everything is a type, after Non-repetition.
   Now: no such section.
   Proposed: "Everything is a type, because everything is a variant of a set; an instance is one member of a population. For engineering reasons not everything becomes an enum: the open-ended variants are names. Ethos has no key-value map, since a map is a poorly specified struct; a position is a type, never a key, and datom carries no field names."
   Ground: 2026-09-26, 93ba9f, "everything is a variant of a set".

```
Library
[]                                         ; imports
[ FilePath.String                          ; types: a path is its own type
  GenerationFailure.[ SyntaxError.Vector<FilePath>
                      Unwritable ] ]       ;   an enum, no keys anywhere
[]                                         ; kinds
[]                                         ; associations
```
```
GenerationFailure.SyntaxError.[ /abs/orchestrate.ethos ]     ; the datom: a variant, no field names
```

5. [vision] `Vision/ethos.md`, new heading An ethos edit is the data migration, after Declaration: File. Assumes (b) of Ruling 6, versions held outside the file, and upgrade-from.
   Now: no such section.
   Proposed: "A change to ethos is operational: the edit to a Memory root is itself the operation that migrates the stored data into its new format. The Memory kind carries a standard successful or unsuccessful change on its record types, and each version carries the upgrade from the version before it. Versions are held by the Nexus that stores the records and by its manifest, never in the ethos file. Ethos is specified in its own ethos, so the same holds for ethos itself and for every proto family, datom included."
   Ground: 2026-09-29, c64ee3, "which becomes the migration itself".
   The upgrade-from choice (each version carries the upgrade from the one before) follows a leaning he left open.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 260" width="700" font-family="sans-serif" font-size="14">
<defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>
<rect width="700" height="260" fill="#fff"/>
<g fill="#eef2f7" stroke="#333">
<rect x="5" y="20" width="200" height="50" rx="6"/><rect x="265" y="20" width="170" height="50" rx="6"/><rect x="495" y="20" width="200" height="50" rx="6"/>
<rect x="265" y="110" width="170" height="50" rx="6"/>
<rect x="5" y="195" width="200" height="50" rx="6"/><rect x="495" y="195" width="200" height="50" rx="6"/>
</g>
<g fill="#111" text-anchor="middle">
<text x="105" y="42">Memory ethos, v1</text><text x="105" y="60" font-size="12">Lock.{ LockId LockName }</text>
<text x="350" y="42">the edit</text><text x="350" y="60" font-size="12">adds FlowId</text>
<text x="595" y="42">Memory ethos, v2</text><text x="595" y="60" font-size="12">Lock.{ LockId LockName FlowId }</text>
<text x="350" y="132">ethos-zero</text><text x="350" y="150" font-size="12">v2 records + upgrade from v1</text>
<text x="105" y="217">stored records, v1</text><text x="105" y="235" font-size="12">in the Nexus</text>
<text x="595" y="217">stored records, v2</text><text x="595" y="235" font-size="12">or the change refused</text>
<text x="350" y="208" font-size="12">upgrade operation:</text><text x="350" y="242" font-size="12">successful or unsuccessful change</text>
</g>
<g stroke="#333" marker-end="url(#a2)" fill="none">
<path d="M205,45 H263"/><path d="M435,45 H493"/><path d="M350,70 V108"/>
<path d="M205,220 H493"/><path d="M350,160 V196"/>
</g>
</svg>

Figure: a mechanism that does not yet exist; ethos-zero 16.0.0 generates no upgrade operation. The edit to the Memory ethos would be compiled into the upgrade that carries each stored record from the old format to the new.

6. [vision] `Vision/ethos.md`, heading Spacing, renamed Layout. Assumes (b) of Ruling 2.
   Now: "Space the delimiters and the inner content. Ethos follows the / canonical protos print: a space inside every bracket and brace / at both ends when non-empty."
   Proposed: "Ethos expands vertically. A structure with more than one element, one of which has a next layer, opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line and never takes a line of its own. Elements that are all leaves sit on one line. A space stands inside every non-empty bracket and brace. Inline nesting goes about three deep; past that, the type comes from a Library, where three more levels open."
   Ground: 2026-10-02, 91ea9f, "a language that expands vertically".

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

7. [vision] `Vision/ethos.md`, new heading Comments, after Layout. Assumes (a) of Ruling 5.
   Now: no such section.
   Proposed: "Ethos carries a comment on every section and on every line that has a next layer, saying in plain words what the machine reads there. A comment runs from ; to the end of the line, and it is kept wherever the ethos is printed."
   Ground: 2026-10-03, edf227, "so that I can see what the machine is seeing".

8. [implementation] `/git/github.com/LiGoldragon/ethos-zero/README.md`, section Print, line 156; built on a yes to Ruling 5 (a); witness: `ethos-zero` with no argument prints `ethos-zero.ethos` without its 10 leading comment lines.
   Now: "section on its own line; comments are not printed."
   Proposed: "section on its own line; each comment is printed where it was written, at the end of its line or on the line above the structure it names."
   Ground: 2026-10-03, edf227, "what the machine is seeing".

9. [vision] `Vision/ethos.md`, heading Inline types. Assumes (b) of Ruling 3.
   Now: "A type may be declared where it is used. The inline struct or enum is / a full type whose derived name carries an underscore, non-idiomatic / for a Rust type, so it never collides and reads at a glance as / inferred from the sugar."
   Proposed: "A type may be declared where it is used. A variant's inline payload is a full type that takes the variant's own name, as a struct position's inline type already does; a second declaration of that name in the file is refused as a duplicate."
   Ground: 2026-09-30, 7328f4, "a variant and a struct name be the same thing".

```
Library
[]                                                        ; imports
[ FilePath.String                                         ; types
  GenerationFailure.[ SyntaxError.Vector<FilePath>        ;   the payload declared inline: a vector
                      Unwritable.{ FilePath String } ] ]  ;   a struct named Unwritable, after its variant
[]                                                        ; kinds
[]                                                        ; associations
```

10. [vision] `Vision/ethos.md`, new heading One position is a new type, after What a declaration turns into. Assumes (a) of Ruling 4.
   Now: no such section.
   Proposed: "A struct holds two or more positions. A type with one position is written as its name, a dot and the contained type, `HarnessName.String`; a struct of one position is refused. A variant with one payload carries it after the dot, with no braces."
   Ground: 2026-09-08, 8e9e77, "This should be a new type".

```
Signal
[]                                         ; imports
[ HarnessStatusQuery.HarnessName ]         ; queries: the payload after the dot, no braces
[ HarnessStarted.HarnessName ]             ; responses
[ HarnessName.String ]                     ; types: one position, a new type
```

11. [implementation] `/git/github.com/LiGoldragon/ethos-zero/README.md`, lines 92 and 93; built on a yes to Ruling 3 (b) and Ruling 4 (a). The refusal would meet 237 one-field structs in 42 of the 89 files.
   Now: "capture those names. A variant `Name.{ T1 T2 }` carries a generated / struct `Name_Data` with one field per position."
   Proposed: "capture those names. A variant `Name.{ T1 T2 }` carries a generated struct `Name` with one field per position. A struct of one position, `Name.{ T }`, is refused as `Conceptual.{ [ path ] OnePosition.Name }`."
   Ground: 2026-09-08, 8e9e77, "refuse single-field struct types".

12. [vision] `Vision/ethos.md`, heading Kind. Assumes (b) of Ruling 7.
   Now: "Kind is the word for the bearer of capabilities: something that can / run is a runner, Runnable is its kind, and run is its capability, a / function the kind has. Trait is set aside as acoustically ambiguous. / In ethos there are no generics, only kinds. Declaring a new kind / declares a new trait in the Rust world and might imply more in the / ethos world."
   Proposed: "Kind is the word for the bearer of capabilities: something that can launch is launchable, Launchable is its kind, and launch is its capability. When trait is said, kind is meant; trait stays the Rust word for what a kind generates. In ethos there are no generics, only kinds: what a capability takes is another kind, never a type. Declaring a new kind declares a new trait in the Rust world."
   Ground: 2026-09-24, 26c50c, "If I say traits I mean kinds".

```
Library
[ protos:Textualizable ]                   ; imports
[ LaunchError.[ Busy Unreadable ] ]        ; types
[ Launchable.[ launch!{ [ Textualizable ]  ; kinds: a launchable takes a textualizable brief
                        [ Result<Self LaunchError> ] } ] ]
[]                                         ; associations
```
```rust
// generated by ethos-zero 16.0.0; derives and #[rustfmt::skip] left out here
pub trait Launchable {
    fn launch<N: protos::Textualizable>(&mut self, input: N) -> std::result::Result<Self, LaunchError>
    where Self: Sized;
}
```

13. [vision] `Vision/ethos.md`, heading Horizon. Assumes (a) of Ruling 8 for today.
   Now: "Ethos will eventually replace everything, Rustlang becoming its / assembly layer. Designs are chosen for that horizon; what it / enables — generator emission among it — comes in its time."
   Proposed: "Ethos will eventually replace everything, Rust becoming its assembly layer. Today ethos declares the types and kinds and ethos-zero compiles them to Rust; the bodies are written by hand, in Rust shaped so that a signal reaches memory only through operation. The whole program written in ethos needs a function syntax, implementations on kinds, and a manifest for compiling and finding dependencies."
   Ground: 2026-09-25, e51411, "write the whole program directly in Ethos".

14. [implementation] `/git/github.com/LiGoldragon/signal-harness/Cargo.toml`, line 28, and the same line in the 20 other crates pinned to 9.0.0 (chroma, claude-answers, meta-signal-aggregator, meta-signal-criome, meta-signal-harness, meta-signal-mentci, meta-signal-mirror, meta-signal-persona, meta-signal-repository-ledger, meta-signal-router, meta-signal-spirit, signal-aggregator, signal-criome, signal-introspect, signal-mentci, signal-mind, signal-repository-ledger, signal-router, signal-spirit, signal-spirit-judge); each crate regenerated and its rkyv dependency added. Rests on a witness, no record of his.
   Now: `ethos-zero = { git = "https://github.com/LiGoldragon/ethos-zero", rev = "b232d35e03011161fe7ec9129ad99a9914413348" }`
   Proposed: `ethos-zero = { git = "https://github.com/LiGoldragon/ethos-zero", rev = "c2653dd82adbdb1f1f2f654405c6620e0d06fd58" }`
   Ground: 2026-10-04, bad807, witness only: 9.0.0 reads no Operation or Memory root.

## Rulings

1. Roots.
   (a) Three roots, Library, Signal, Sema: `Vision/ethos.md` Roots; 2026-09-10, fe34eb.
   (b) Four roots, Library, Signal, Operation, Memory: 2026-10-02, 91ea9f.
2. Layout.
   (a) One declaration per line, delimiters spaced, as the protos print: `Vision/ethos.md` Spacing, as of 2026-09-11, dated by commit.
   (b) Vertical expansion about three deep, the closing delimiter ending the last line: 2026-10-02, 91ea9f.
3. The name of a variant's inline payload.
   (a) Derived with an underscore, `Unwritable_Data`, so it never collides: 2026-09-09, 564f55; ethos-zero 16.0.0.
   (b) The variant's own name, shared by variant and struct: 2026-09-30, 7328f4.
4. One-field structs and what `Name.String` declares. The flow reads the second as part of the first, a departure from the new-type form he asked for.
   (a) A one-field struct is refused, and `Name.String` is a new type of its own: 2026-09-08, 8e9e77.
   (b) A one-field struct is accepted, and `Name.String` is a Rust alias, `pub type Name = String`, bearing no derive: `Vision/ethos.md`; ethos-zero since 2026-09-10 (`9e2e327`, `79e51c0`), dated by commit; 42 files use it.
5. Comments.
   (a) A comment on every section and next-layer line, kept: 2026-10-03, edf227.
   (b) Comments read and dropped from the print: ethos-zero README, 16.0.0, 2026-10-02, dated by commit.
6. Versions.
   (a) No version in an ethos file: 2026-09-09, 564f55.
   (b) Ethos versions, each with its upgrade: 2026-09-29, c64ee3; 2026-10-02, 91ea9f.
7. Trait or kind.
   (a) Trait set aside as acoustically ambiguous: 2026-08-26, f426777b.
   (b) Kind meant when trait is said, trait still said for Rust: 2026-09-11, fe34eb; 2026-09-24, 26c50c.
8. Bodies by hand, or the whole program in ethos.
   (a) Ethos types and kinds, implementations written by hand: 2026-10-04, 5ed94b.
   (b) The whole program in ethos within a few months: 2026-09-25, e51411; 2026-09-29, c64ee3.
<!-- to-the-living:end -->
