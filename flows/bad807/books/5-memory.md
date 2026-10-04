<!-- to-the-living:start -->
Presentation.{ «Memory» }

How it is now. `Vision/` has no file for memory. `Vision/sema.md` (15 lines) holds one heading, What sema is: "Sema is the database engine of a Nexus", with a Sema root of record types (`Lock.{ LockId LockName FlowId LockPaths LockReason }`). `Vision/nexus.md` speaks of the store under Configuration ("its Sema database at the default location"), First configuration (a standard metadata tree) and Documents ("The nexus and sema documents are undesigned"). `Vision/flowNexus.md` (59 lines, 8 headings) has no heading on what Flow keeps, and `Vision/ethos.md` Roots names Library, Signal, Sema. ethos-zero 16.0.0 (`/git/github.com/LiGoldragon/ethos-zero`, `c2653dd`, 2026-10-03) reads a Memory root with two sections, imports and record types, refuses a `Sema` head as `Renamed.Memory`, and generates the declared record types alone, each archiving with rkyv and datomizing under the `datom` feature; its `UPGRADES.md` says "No consumer generates from a Memory or Operation file", and the only Memory files are its fixtures `entry-memory.ethos` and `print/flow-memory.ethos`. The Flow Nexus 0.24.0 (`/git/github.com/LiGoldragon/flow`, `5e0b1bf`, 2026-10-03) keeps its memory in one file, `$HOME/.local/state/flow/flow.sema` (1,056,768 bytes, last written 2026-10-03), through sema-engine 0.18.0 (`9884905`, over redb 4 and rkyv) in 14 tables whose record types are written by hand in `crates/flow-nexus/src/store.rs`; its roles table holds a `Caller.{ FlowId FlowAspect PowerLevel ModelName }` per flow, no table holds context modules, it has `ethos/operation.ethos` and no `memory.ethos`, and it uses none of sema-engine's `Memorable`, `MemoryChanges` or `UpgradeFrom`. The Clojure messenger (`messenger-clj`, `85e71b1`, 2026-10-03) keeps its registry in Datalevin through the Babashka pod 0.8.25. On his order of today, vision statements migrate from Vision/ into the psyche repository as Vision-type skills; each [vision] proposal names its Vision/ file as its home today and travels with the migration.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 280" width="700" font-family="sans-serif" font-size="14">
<defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>
<rect width="700" height="280" fill="#fff"/>
<rect x="150" y="20" width="540" height="240" rx="10" fill="#f7f7f2" stroke="#333"/>
<text x="420" y="44" text-anchor="middle" fill="#111" font-weight="bold">flow-nexus</text>
<g fill="#eef2f7" stroke="#333">
<rect x="10" y="110" width="110" height="60" rx="6"/>
<rect x="175" y="90" width="130" height="100" rx="6"/>
<rect x="355" y="90" width="130" height="100" rx="6"/>
</g>
<rect x="535" y="90" width="135" height="100" rx="6" fill="#e3f0e3" stroke="#333" stroke-width="2"/>
<g fill="#111" text-anchor="middle">
<text x="65" y="136">flow-meta</text><text x="65" y="155" font-size="12">CLI, datom</text>
<text x="240" y="125" font-weight="bold">Signal</text><text x="240" y="145" font-size="12">rkyv on the</text><text x="240" y="161" font-size="12">meta socket</text>
<text x="420" y="125" font-weight="bold">Operation</text><text x="420" y="145" font-size="12">hand-written</text><text x="420" y="161" font-size="12">bodies</text>
<text x="602" y="125" font-weight="bold">Memory</text><text x="602" y="145" font-size="12">flow.sema</text><text x="602" y="161" font-size="12">record types</text>
<text x="160" y="96" font-size="11">in</text>
<text x="400" y="235" font-size="12" fill="#a33">no path: Signal never touches Memory</text>
</g>
<g stroke="#333" fill="none" marker-end="url(#m1)">
<path d="M120,125 H173"/><path d="M305,115 H353"/><path d="M485,115 H533"/>
<path d="M533,170 H487"/><path d="M353,170 H307"/><path d="M173,155 H122"/>
</g>
<path d="M240,190 V215 H602 V190" fill="none" stroke="#a33" stroke-dasharray="6 5"/>
<line x1="410" y1="207" x2="430" y2="223" stroke="#a33" stroke-width="2"/><line x1="430" y1="207" x2="410" y2="223" stroke="#a33" stroke-width="2"/>
<g fill="#111" font-size="11" text-anchor="middle">
<text x="330" y="108">1</text><text x="510" y="108">2</text><text x="510" y="185">3</text><text x="330" y="185">4</text><text x="148" y="170">5</text>
</g>
</svg>

The enforced path: a signal reaches memory only through operation (1, 2), and the change returns through operation as signal (3, 4, 5).

1. [vision] `Vision/memory.md`, heading What memory is. Assumes (b) of Ruling 1.
   Now: no such file.
   Proposed: "Memory is the keeping part of a Nexus: the typed records it remembers, declared in its ethos under the Memory root, so that reading the ethos shows everything the Nexus keeps. Every Nexus has its own memory and no other; there is no central store. Policy state and working state live in that one memory, and policy changes only over the meta socket."
   Ground: 2026-10-02, 91ea9f, "Yeah the memory is good".

2. [vision] `Vision/memory.md`, heading What memory never holds.
   Now: no such file.
   Proposed: "Memory holds only its own Nexus's records, each of a declared type. It never holds what another Nexus remembers, configuration kept in Markdown files, or state written into pane titles. A string is stored only where it is chosen on purpose, since text is the expensive form; where a type can stand, the type is stored. Memory's vocabulary never appears on the ordinary wire."
   Ground: 2026-10-03, edf227, "It lives in its own database and its memory."

3. [vision] `Vision/memory.md`, heading Memory is reached only through operation.
   Now: no such file.
   Proposed: "A signal reaches memory only through operation, and what memory answers leaves the Nexus only through operation and then signal: signal, operation, memory, operation, signal. Signal never touches memory. The Nexus's standard entry point enforces this path, so the ethos of the three parts names every object and process on it."
   Ground: 2026-10-04, 5ed94b, "go through the operation actor/system in order to reach the memory actor/system".

4. [vision] `Vision/memory.md`, heading A memory schema is written in ethos.
   Now: no such file.
   Proposed: "A memory schema is an ethos file headed Memory with two sections: imports, then record types. Each record type is a struct or enum named for what one record holds; a type the memory needs only for itself is declared in place. The memory kind gives every record type a standard change that succeeds or is refused with a typed reason, and the edit to the schema carries the upgrade that brings the stored records to the new format."
   Ground: 2026-10-02, 91ea9f, "a standard successful or unsuccessful change".

5. [vision] `Vision/memory.md`, heading The store. Assumes (b) of Ruling 3, the two engines by scope.
   Now: no such file.
   Proposed: "A Nexus keeps its memory in one file at its default location, written and read only through the memory engine. The Clojure prototypes are proofs of concept that emulate ethos on EDN and the Datomic libraries; they are not ported into the Nexus that follows them."
   Ground: 2026-09-25, e51411, "We're not porting one to the other."

6. [vision] `Vision/nexus.md`, heading Configuration. Assumes (b) of Ruling 1.
   Now: "A Nexus starts with no arguments and there is no bootstrap binary. / Its executable holds a default configuration as a constant. On start / it looks for its Sema database at the default location: a database / that exists holds the configuration; a database created new is / seeded with the defaults. The meta socket carries a Configure / interface, and changed values are accepted through it."
   Proposed: "A Nexus starts with no arguments and there is no bootstrap binary. Its executable holds a default configuration as a constant. On start it opens its memory at the default location: a memory that exists holds the configuration; a memory created new is seeded with the defaults. The meta socket carries a Configure interface, and changed values are accepted through it."
   Ground: 2026-08-26, 01a03d6e, "the default configuration when creating a new database".

7. [vision] `Vision/flowNexus.md`, new heading Flow's memory, after What it does. Assumes (b) of Ruling 4. The module-type and role vocabulary rests on flow 9fb0ad's notes and his 2026-10-03 words, not a ruled text.
   Now: no such section.
   Proposed: "Flow's configuration lives in Flow's memory. It holds the registry of context modules, one record per module: its type, its name, unique within that type, and its location, a local path for now. It holds one configuration per role: for each placement, the system prompt, the first prompt or loadable, the names it wants grouped by module type, and the model the role runs on. A name maps to its path only in the registry, so nothing is repeated. The registry and the role configurations change only over Flow's meta socket."
   Ground: 2026-10-03, edf227, "those module names correspond with the path".

8. [implementation] `/git/github.com/LiGoldragon/flow/crates/flow-nexus/ethos/memory.ethos`, generated into `src/generated/memory.rs` by `build.rs` beside `operation.ethos`. Assumes (b) of Ruling 4. The module-type and role vocabulary rests on flow 9fb0ad's notes and his 2026-10-03 words, not a ruled text; the schema is this flow's design.
   Now: no such file.
   Proposed:

```
; Flow's memory: the context-module registry and the role configurations
Memory
[ signal_flow:[ ModelName ] ]                          ; imports: the model's name, from Flow's wire
[ Module.{ ModuleType.[ Spirit Intent Vision Knowledge  ; one registry record per module
                        Compensation Trial Operation ]
           ModuleName.String                            ; unique within its type
           Location.[ Path.String ] }                   ; a local path for now
  RoleConfiguration.{ Role.[ Voice.{ Aspect.[ Psyche Mind Field ]  ; one record per role
                                     Layer.[ Primary Secondary Tertiary Quaternary ] }
                             LivingInteraction
                             Implementation
                             VisionAudit ]
                      Vector<Placed>                    ; where each selection goes
                      ModelName }
  Placed.{ Placement.[ SystemPrompt FirstPrompt Loadable ]
           Vector<Selection> }
  Selection.{ ModuleType                                ; one module type, the names it wants
              Vector<ModuleName> } ]
```

   Ground: 2026-10-03, 5578cc, "I don't see `role` as a kind here".

   Witnessed 2026-10-04 with ethos-zero 16.0.0 (`target/debug/ethos-zero`, built after `c2653dd`): `Check` answers `Checked`, `Generate` writes 93 lines. The Rust shape, derives and `#[rustfmt::skip]` omitted; every item derives rkyv's `Archive`, `Serialize`, `Deserialize` and, under `datom`, `Datomizable` and `Composing`:

```rust
pub enum ModuleType { Spirit, Intent, Vision, Knowledge, Compensation, Trial, Operation }
pub type ModuleName = String;
pub enum Location { Path(String) }
pub struct Module { pub module_type: ModuleType, pub module_name: ModuleName, pub location: Location }
pub enum Aspect { Psyche, Mind, Field }
pub enum Layer { Primary, Secondary, Tertiary, Quaternary }
pub struct Voice_Data { pub aspect: Aspect, pub layer: Layer }
pub enum Role { Voice(Voice_Data), LivingInteraction, Implementation, VisionAudit }
pub struct RoleConfiguration { pub role: Role, pub placed_vector: std::vec::Vec<Placed>, pub model_name: signal_flow::ModelName }
pub enum Placement { SystemPrompt, FirstPrompt, Loadable }
pub struct Placed { pub placement: Placement, pub selection_vector: std::vec::Vec<Selection> }
pub struct Selection { pub module_type: ModuleType, pub module_name_vector: std::vec::Vec<ModuleName> }
```

   A role is the record that selects a seat's modules; it is not a module type. Two stored records, read from datom into these types, written back and archived through rkyv (157 bytes for the role, equal after the round trip):

```
{ Vision nexus Path./home/li/primary/Vision/nexus.md }   ; a Module: type, name, location

{ Voice.{ Psyche Primary }                               ; a RoleConfiguration: the role
  [ { SystemPrompt
      [ { Spirit [ spirit ] }                            ; placed in the system prompt
        { Vision [ nexus memory ] } ] }
    { Loadable
      [ { Knowledge [ knowledge-ethos knowledge-flow ] } ] } ]  ; left loadable by name
  claude-opus-5-5 }                                      ; the model
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 300" width="700" font-family="sans-serif" font-size="13">
<defs><marker id="m2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>
<rect width="700" height="300" fill="#fff"/>
<g stroke="#333">
<rect x="10" y="20" width="250" height="130" rx="6" fill="#eef2f7"/>
<rect x="10" y="185" width="250" height="95" rx="6" fill="#eef2f7"/>
<rect x="320" y="20" width="370" height="260" rx="6" fill="#e3f0e3"/>
<rect x="340" y="70" width="330" height="40" fill="#fff"/>
<rect x="340" y="125" width="330" height="40" fill="#fff"/>
<rect x="340" y="180" width="330" height="80" fill="#fff"/>
</g>
<g fill="#111">
<text x="20" y="42" font-weight="bold">memory.ethos (the schema)</text>
<text x="20" y="66" font-family="monospace" font-size="12">Memory</text>
<text x="20" y="84" font-family="monospace" font-size="12">[ signal_flow:[ ModelName ] ]</text>
<text x="20" y="102" font-family="monospace" font-size="12">[ Module.{ ModuleType</text>
<text x="20" y="120" font-family="monospace" font-size="12">  ModuleName Location }</text>
<text x="20" y="138" font-family="monospace" font-size="12">  RoleConfiguration.{ … } … ]</text>
<text x="20" y="207" font-weight="bold">memory.rs (generated)</text>
<text x="20" y="231" font-family="monospace" font-size="12">pub struct Module</text>
<text x="20" y="249" font-family="monospace" font-size="12">pub struct RoleConfiguration</text>
<text x="20" y="267" font-size="12">rkyv always, datom in the CLI</text>
<text x="330" y="42" font-weight="bold">flow.sema, one file, through sema-engine</text>
<text x="330" y="60" font-size="12">a table per record type, each row an rkyv archive</text>
<text x="350" y="94" font-family="monospace" font-size="12">modules: { Vision nexus Path./home/li/… }</text>
<text x="350" y="149" font-family="monospace" font-size="12">modules: { Knowledge knowledge-ethos Path.… }</text>
<text x="350" y="204" font-family="monospace" font-size="12">role configurations:</text>
<text x="350" y="222" font-family="monospace" font-size="12">{ Voice.{ Psyche Primary }</text>
<text x="350" y="240" font-family="monospace" font-size="12">  [ { SystemPrompt [ … ] } … ] claude-opus-5-5 }</text>
</g>
<g stroke="#333" fill="none" marker-end="url(#m2)">
<path d="M135,150 V183"/><path d="M260,230 H318"/>
</g>
<text x="142" y="172" font-size="11" fill="#111">ethos-zero Generate</text>
<text x="266" y="222" font-size="11" fill="#111">stores</text>
</svg>

The store: the Memory root is the schema, ethos-zero generates its record types, and the memory engine keeps each record in Flow's one file; the records are shown here as datom.

9. [implementation] `/git/github.com/LiGoldragon/flow/crates/flow-nexus/src/store.rs`, the roles table.
   Now: "let roles = engine.register_table(TableDescriptor::new( / FLOW_ROLE_TABLE_NAME, / FamilyName::new("flow-nexus-role"), / SchemaHash::for_label("flow-nexus-role-v1"), / ))?;"
   Proposed: "let modules = engine.register_table(TableDescriptor::new( / FLOW_MODULE_TABLE_NAME, / FamilyName::new("flow-nexus-module"), / SchemaHash::for_label("flow-nexus-module-v1"), / ))?; / let role_configurations = engine.register_table(TableDescriptor::new( / FLOW_ROLE_CONFIGURATION_TABLE_NAME, / FamilyName::new("flow-nexus-role-configuration"), / SchemaHash::for_label("flow-nexus-role-configuration-v1"), / ))?;", the two tables holding `memory::Module` and `memory::RoleConfiguration`, each implementing sema-engine's `Memorable` so every change is admitted or refused by the record; the per-flow `Caller` rows stay in their own table. The store change is this flow's design, not his ruling.
   Ground: 2026-10-03, edf227, "That would be the meta."

10. [implementation] `/git/github.com/LiGoldragon/Curriculum/skills/vision-nexus.md`, second paragraph.
   Now: "Its Memory is its own typed store, reached only through the memory engine; there is no central store;"
   Proposed: "Its Memory is its own typed store, reached only from Operation and only through the memory engine, so a signal reaches memory through operation and returns through operation; there is no central store;"
   Ground: 2026-10-04, 5ed94b, "back through the operation system".

## Rulings

1. The keeping part's name.
   (a) Sema, the database engine, its root declaring record types: 2026-09-09, 564f55; 2026-09-10, fe34eb; `Vision/sema.md`.
   (b) Memory, Sema going to the meaning language and storage disliked: 2026-09-26, b7ba00; 2026-10-02, 91ea9f; ethos-zero since 15.0.0.
2. Whether each part of a Nexus has its own ethos root.
   (a) Signal and Sema give all the main types, the nexus-core concept dropped: 2026-09-10, fe34eb; `Vision/ethos.md` Roots.
   (b) The three layers, each described in ethos: 2026-09-13, 024bc7; 2026-10-02, 91ea9f.
3. The store engine.
   (a) Every Nexus opens its Sema database at the default location: 2026-08-26, 01a03d6e; `Vision/nexus.md` Configuration.
   (b) The Clojure tools keep a Datalevin database: 2026-09-25, e51411; 2026-09-26, e167d8.
4. Where Flow's memory lives.
   (a) In Mind, which grows the largest database: 2026-09-17, 9993b5.
   (b) In Flow's own database and memory: 2026-10-03, edf227.
5. The direction of a record type's upgrade.
   (a) Upgrade from the predecessor, upgrading the past (one record): 2026-10-02, 91ea9f; sema-engine 0.18.0 `UpgradeFrom`.
   (b) Possibly symmetrical, from and to (one record): 2026-10-02, 91ea9f.
<!-- to-the-living:end -->
