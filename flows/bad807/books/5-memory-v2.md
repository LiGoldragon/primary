<!-- to-the-living:start -->
Presentation.{ «Memory» }

## How it is now

### The vision
`Vision/` has no file for memory.
`Vision/sema.md` has one heading, What sema is: "Sema is the database engine of a Nexus".
`Vision/nexus.md` names the store under Configuration and calls the sema document undesigned.
`Vision/flowNexus.md` says nothing of what Flow keeps; `Vision/ethos.md` Roots names Library, Signal, Sema.

### The generator
ethos-zero 16.0.0 reads a Memory root: imports, then record types.
It refuses a `Sema` head as `Renamed.Memory` and generates the record types alone (rkyv always, datom under the `datom` feature).
No consumer generates from a Memory file yet; the only ones are its own fixtures.

### Flow today
Flow Nexus 0.24.0 keeps its memory in one file, `flow.sema` (about 1 MB), through sema-engine 0.18.0 over redb and rkyv.
Its 14 tables have record types written by hand in `store.rs`.
The roles table holds one `Caller.{ FlowId FlowAspect PowerLevel ModelName }` per flow; no table holds context modules.
It has `operation.ethos`, no `memory.ethos`, and uses none of `Memorable`, `MemoryChanges`, `UpgradeFrom`.

### Elsewhere
The Clojure messenger keeps its registry in Datalevin through the Babashka pod 0.8.25.
Vision statements now migrate into the psyche repository as Vision-type skills; each [vision] proposal names its `Vision/` file and travels with them.

## The enforced path

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 250" width="700" font-family="sans-serif" font-size="15">
<defs><marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2a5db0"/></marker>
<marker id="pb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2e7d4f"/></marker></defs>
<rect width="700" height="250" rx="10" fill="#ffffff"/>
<rect x="150" y="14" width="536" height="222" rx="12" fill="#f6f4ee" stroke="#8a8270"/>
<text x="418" y="38" text-anchor="middle" font-weight="bold" fill="#3a3528">flow-nexus</text>
<rect x="12" y="92" width="112" height="66" rx="8" fill="#fff4d6" stroke="#a07800"/>
<text x="68" y="120" text-anchor="middle" fill="#111">flow-meta</text><text x="68" y="140" text-anchor="middle" font-size="12" fill="#555">the CLI</text>
<rect x="172" y="76" width="140" height="98" rx="8" fill="#dcebff" stroke="#2a5db0"/>
<text x="242" y="118" text-anchor="middle" font-weight="bold" fill="#111">Signal</text><text x="242" y="140" text-anchor="middle" font-size="12" fill="#333">the wire</text>
<rect x="356" y="76" width="140" height="98" rx="8" fill="#ece3fb" stroke="#6b44b0"/>
<text x="426" y="118" text-anchor="middle" font-weight="bold" fill="#111">Operation</text><text x="426" y="140" text-anchor="middle" font-size="12" fill="#333">the work</text>
<rect x="540" y="76" width="134" height="98" rx="8" fill="#dff1e4" stroke="#2e7d4f" stroke-width="2"/>
<text x="607" y="118" text-anchor="middle" font-weight="bold" fill="#111">Memory</text><text x="607" y="140" text-anchor="middle" font-size="12" fill="#333">flow.sema</text>
<g stroke="#2a5db0" stroke-width="2" marker-end="url(#pa)"><path d="M124,108 H170"/><path d="M312,100 H354"/><path d="M496,100 H538"/></g>
<g stroke="#2e7d4f" stroke-width="2" marker-end="url(#pb)"><path d="M538,150 H498"/><path d="M354,150 H314"/><path d="M170,142 H126"/></g>
<g font-size="13"><path d="M14,196 H40" stroke="#2a5db0" stroke-width="3"/><text x="46" y="201" fill="#2a5db0">ask</text><path d="M14,222 H40" stroke="#2e7d4f" stroke-width="3"/><text x="46" y="227" fill="#2e7d4f">answer</text></g>
<path d="M242,174 V206 H607 V174" fill="none" stroke="#b3261e" stroke-width="2" stroke-dasharray="6 5"/>
<path d="M414,198 l16,16 M430,198 l-16,16" stroke="#b3261e" stroke-width="3"/>
<text x="424" y="230" text-anchor="middle" font-size="13" fill="#b3261e">no path: Signal never touches Memory</text>
</svg>

*Signal, operation, memory, operation, signal: memory is reached only through operation.*

## Proposals: Vision/memory.md

### 1. What memory is
[vision] `Vision/memory.md`. Assumes Ruling 1 (b). Now: no such file.

> Memory is the keeping part of a Nexus: the typed records it remembers, declared in its ethos under the Memory root, so that reading the ethos shows everything the Nexus keeps.
>
> Every Nexus has its own memory and no other; there is no central store. Policy state and working state live in that one memory, and policy changes only over the meta socket.

Ground: "Yeah the memory is good".

### 2. What memory never holds
[vision] `Vision/memory.md`. Now: no such file.

> Memory holds only its own Nexus's records, each of a declared type. It never holds what another Nexus remembers, configuration kept in Markdown files, or state written into pane titles.
>
> A string is stored only where it is chosen on purpose, since text is the expensive form; where a type can stand, the type is stored. Memory's vocabulary never appears on the ordinary wire.

Ground: "It lives in its own database and its memory."

### 3. Memory is reached only through operation
[vision] `Vision/memory.md`. Now: no such file.

> A signal reaches memory only through operation, and what memory answers leaves the Nexus only through operation and then signal: signal, operation, memory, operation, signal.
>
> Signal never touches memory. The Nexus's standard entry point enforces this path, so the ethos of the three parts names every object and process on it.

Ground: "go through the operation actor/system in order to reach the memory actor/system".

### 4. A memory schema is written in ethos
[vision] `Vision/memory.md`. Now: no such file.

> A memory schema is an ethos file headed Memory with two sections: imports, then record types. Each record type is a struct or enum named for what one record holds; a type the memory needs only for itself is declared in place.
>
> The memory kind gives every record type a standard change that succeeds or is refused with a typed reason, and the edit to the schema carries the upgrade that brings the stored records to the new format.

Ground: "a standard successful or unsuccessful change".

### 5. The store
[vision] `Vision/memory.md`. Assumes Ruling 3 (b), the two engines by scope. Now: no such file.

> A Nexus keeps its memory in one file at its default location, written and read only through the memory engine. The Clojure prototypes are proofs of concept that emulate ethos on EDN and the Datomic libraries; they are not ported into the Nexus that follows them.

Ground: "We're not porting one to the other."

## Proposals: other vision files

### 6. Vision/nexus.md, Configuration
[vision] Assumes Ruling 1 (b). Only the store's name changes.

```diff
- On start it looks for its Sema database at the default location: a database
- that exists holds the configuration; a database created new is seeded with the defaults.
+ On start it opens its memory at the default location: a memory
+ that exists holds the configuration; a memory created new is seeded with the defaults.
```

The sentences before and after stay: no arguments, no bootstrap binary, a default configuration as a constant, a Configure interface on the meta socket.
Ground: "the default configuration when creating a new database".

### 7. Vision/flowNexus.md, new heading Flow's memory
[vision] After What it does. Assumes Ruling 4 (b). The module-type and role vocabulary rests on notes and his words, not a ruled text. Now: no such section.

> Flow's configuration lives in Flow's memory. It holds the registry of context modules, one record per module: its type, its name, unique within that type, and its location, a local path for now.
>
> It holds one configuration per role: for each placement, the system prompt, the first prompt or loadable, the names it wants grouped by module type, and the model the role runs on.
>
> A name maps to its path only in the registry, so nothing is repeated. The registry and the role configurations change only over Flow's meta socket.

Ground: "those module names correspond with the path".

## Proposal 8: Flow's memory schema

[implementation] `flow/crates/flow-nexus/ethos/memory.ethos`, generated into `src/generated/memory.rs` by `build.rs`. Assumes Ruling 4 (b). The vocabulary rests on notes and his words, not a ruled text; the schema is this flow's design. Now: no such file.

```
; Flow's memory: the context-module registry and the role configurations
Memory
[ signal_flow:[ ModelName ]                  ; the model's name, from Flow's wire
  curriculum_deploy:[ ModuleType ] ]         ; the module types, declared once in the generator's ethos
[ Module.{ ModuleType                        ; one registry record per module
           ModuleName.String                 ; unique within its type
           Location.[ Path.String ] }        ; a local path for now
  RoleConfiguration.{ Role.[ Voice.{ Aspect.[ Psyche Mind Field ]
                                     Layer.[ Primary Secondary Tertiary Quaternary ] }
                             LivingInteraction Implementation VisionAudit ]
                      Vector<Placed>         ; where each selection goes
                      ModelName }
  Placed.{ Placement.[ SystemPrompt FirstPrompt Loadable ] Vector<Selection> }  ; Queued is proposed, not ruled
  Selection.{ ModuleType Vector<ModuleName> } ]  ; one module type, the names it wants
```

The module types are not listed here: they are declared once, in `curriculum-deploy.ethos`, which does not declare them yet.
Ground: "I don't see `role` as a kind here".

### The generated Rust
Witnessed with ethos-zero 16.0.0 with the types declared in place: `Check` answers `Checked`, `Generate` writes 93 lines. The import form is not yet checked.

```rust
pub struct Module { pub module_type: curriculum_deploy::ModuleType, pub module_name: ModuleName, pub location: Location }
pub enum Aspect { Psyche, Mind, Field }
pub enum Layer { Primary, Secondary, Tertiary, Quaternary }
pub struct Voice_Data { pub aspect: Aspect, pub layer: Layer }
pub enum Role { Voice(Voice_Data), LivingInteraction, Implementation, VisionAudit }
pub struct RoleConfiguration { pub role: Role, pub placed_vector: Vec<Placed>, pub model_name: signal_flow::ModelName }
pub struct Placed { pub placement: Placement, pub selection_vector: Vec<Selection> }
pub struct Selection { pub module_type: curriculum_deploy::ModuleType, pub module_name_vector: Vec<ModuleName> }
```

Every item archives with rkyv and, under `datom`, datomizes. A role is the record that selects a seat's modules; it is not a module type.

### Two records
Read from datom, written back, archived through rkyv: 157 bytes for the role, equal after the round trip.

```
{ Vision nexus Path./home/li/primary/Vision/nexus.md }        ; a Module

{ Voice.{ Psyche Primary }                                    ; a RoleConfiguration
  [ { SystemPrompt [ { Spirit [ spirit ] } { Vision [ nexus memory ] } ] }
    { Loadable [ { Knowledge [ knowledge-ethos knowledge-flow ] } ] } ]
  claude-opus-5-5 }                                           ; the model
```

## The store

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 300" width="700" font-family="sans-serif" font-size="14">
<defs><marker id="sa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#444"/></marker></defs>
<rect width="700" height="300" rx="10" fill="#ffffff"/>
<rect x="12" y="14" width="250" height="122" rx="8" fill="#ece3fb" stroke="#6b44b0"/>
<text x="24" y="38" font-weight="bold" fill="#111">memory.ethos</text>
<g font-family="monospace" font-size="13" fill="#222"><text x="24" y="62">Memory</text><text x="24" y="82">[ imports ]</text><text x="24" y="102">[ Module.{ … }</text><text x="24" y="122">  RoleConfiguration.{ … } ]</text></g>
<rect x="12" y="178" width="250" height="108" rx="8" fill="#dcebff" stroke="#2a5db0"/>
<text x="24" y="202" font-weight="bold" fill="#111">memory.rs, generated</text>
<g font-family="monospace" font-size="13" fill="#222"><text x="24" y="228">struct Module</text><text x="24" y="248">struct RoleConfiguration</text></g>
<text x="24" y="272" font-size="12" fill="#444">rkyv always, datom in the CLI</text>
<path d="M137,136 V176" stroke="#444" stroke-width="2" marker-end="url(#sa)"/>
<text x="146" y="162" font-size="12" fill="#444">ethos-zero Generate</text>
<rect x="318" y="14" width="370" height="272" rx="8" fill="#dff1e4" stroke="#2e7d4f" stroke-width="2"/>
<text x="332" y="38" font-weight="bold" fill="#111">flow.sema, one file</text>
<text x="332" y="58" font-size="12" fill="#333">a table per record type, each row an rkyv archive</text>
<rect x="332" y="72" width="342" height="62" rx="6" fill="#ffffff" stroke="#2e7d4f"/>
<text x="342" y="92" font-size="12" font-weight="bold" fill="#2e7d4f">modules</text>
<text x="342" y="118" font-family="monospace" font-size="13" fill="#222">{ Vision nexus Path.… }</text>
<rect x="332" y="146" width="342" height="126" rx="6" fill="#ffffff" stroke="#2e7d4f"/>
<text x="342" y="166" font-size="12" font-weight="bold" fill="#2e7d4f">role configurations</text>
<g font-family="monospace" font-size="13" fill="#222"><text x="342" y="192">{ Voice.{ Psyche Primary }</text><text x="342" y="214">  [ { SystemPrompt [ … ] }</text><text x="342" y="236">    { Loadable [ … ] } ]</text><text x="342" y="258">  claude-opus-5-5 }</text></g>
<path d="M262,232 H316" stroke="#444" stroke-width="2" marker-end="url(#sa)"/>
<text x="268" y="224" font-size="12" fill="#444">stores</text>
</svg>

*The schema generates the types; the memory engine keeps each record in Flow's one file (records shown as datom).*

## Proposal 9: the roles table

[implementation] `flow/crates/flow-nexus/src/store.rs`. This flow's design, not his ruling.

```rust
// Now
let roles = engine.register_table(TableDescriptor::new(
    FLOW_ROLE_TABLE_NAME,
    FamilyName::new("flow-nexus-role"),
    SchemaHash::for_label("flow-nexus-role-v1"),
))?;
```

```rust
// Proposed
let modules = engine.register_table(TableDescriptor::new(
    FLOW_MODULE_TABLE_NAME,
    FamilyName::new("flow-nexus-module"),
    SchemaHash::for_label("flow-nexus-module-v1"),
))?;
let role_configurations = engine.register_table(TableDescriptor::new(
    FLOW_ROLE_CONFIGURATION_TABLE_NAME,
    FamilyName::new("flow-nexus-role-configuration"),
    SchemaHash::for_label("flow-nexus-role-configuration-v1"),
))?;
```

The tables hold `memory::Module` and `memory::RoleConfiguration`, each `Memorable`, so the record admits or refuses every change.
The per-flow `Caller` rows stay in their own table. Ground: "That would be the meta."

## Proposal 10: the vision-nexus skill

[implementation] `Curriculum/skills/vision-nexus.md`, second paragraph.

```diff
- Its Memory is its own typed store, reached only through the memory engine;
+ Its Memory is its own typed store, reached only from Operation and only through the memory engine,
+ so a signal reaches memory through operation and returns through operation;
  there is no central store;
```

Ground: "back through the operation system".

## The upgrade path

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 272" width="700" font-family="sans-serif" font-size="14">
<defs><marker id="ua" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#444"/></marker>
<marker id="ub" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#b06a00"/></marker></defs>
<rect width="700" height="272" rx="10" fill="#ffffff"/>
<rect x="12" y="20" width="190" height="66" rx="8" fill="#ece3fb" stroke="#6b44b0"/>
<text x="107" y="48" text-anchor="middle" font-weight="bold" fill="#111">schema, old</text><text x="107" y="70" text-anchor="middle" font-size="12" fill="#333">Module.{ … }</text>
<rect x="498" y="20" width="190" height="66" rx="8" fill="#ece3fb" stroke="#6b44b0"/>
<text x="593" y="48" text-anchor="middle" font-weight="bold" fill="#111">schema, new</text><text x="593" y="70" text-anchor="middle" font-size="12" fill="#333">Module.{ … edited }</text>
<path d="M202,53 H496" stroke="#6b44b0" stroke-width="2" marker-end="url(#ua)"/>
<text x="350" y="44" text-anchor="middle" font-size="13" fill="#6b44b0">the edit carries the upgrade</text>
<rect x="12" y="150" width="190" height="66" rx="8" fill="#dff1e4" stroke="#2e7d4f"/>
<text x="107" y="178" text-anchor="middle" font-weight="bold" fill="#111">stored records</text><text x="107" y="200" text-anchor="middle" font-size="12" fill="#333">old format</text>
<rect x="255" y="150" width="190" height="66" rx="8" fill="#fff4d6" stroke="#a07800"/>
<text x="350" y="178" text-anchor="middle" font-weight="bold" fill="#111">UpgradeFrom</text><text x="350" y="200" text-anchor="middle" font-size="12" fill="#333">one record at a time</text>
<rect x="498" y="150" width="190" height="66" rx="8" fill="#dff1e4" stroke="#2e7d4f" stroke-width="2"/>
<text x="593" y="178" text-anchor="middle" font-weight="bold" fill="#111">stored records</text><text x="593" y="200" text-anchor="middle" font-size="12" fill="#333">new format</text>
<g stroke="#444" stroke-width="2" marker-end="url(#ua)"><path d="M202,174 H253"/><path d="M445,174 H496"/></g>
<path d="M593,216 V236 H107 V219" fill="none" stroke="#b06a00" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#ub)"/>
<text x="350" y="258" text-anchor="middle" font-size="13" fill="#b06a00">(b) only: back to the old format</text>
<path d="M107,86 V148 M593,86 V148" stroke="#999" stroke-dasharray="3 4"/>
</svg>

*Ruling 5: (a) upgrades forward from the predecessor; (b) would also go back.*

## Rulings

### 1. The keeping part's name
(a) Sema, the database engine, its root declaring record types: 2026-09-09; 2026-09-10; `Vision/sema.md`.
(b) Memory, Sema going to the meaning language and storage disliked: 2026-09-26; 2026-10-02; ethos-zero since 15.0.0.

### 2. Whether each part of a Nexus has its own ethos root
(a) Signal and Sema give all the main types, the nexus-core concept dropped: 2026-09-10; `Vision/ethos.md` Roots.
(b) The three layers, each described in ethos: 2026-09-13; 2026-10-02.

### 3. The store engine
(a) Every Nexus opens its Sema database at the default location: 2026-08-26; `Vision/nexus.md` Configuration.
(b) The Clojure tools keep a Datalevin database: 2026-09-25; 2026-09-26.

### 4. Where Flow's memory lives
(a) In Mind, which grows the largest database: 2026-09-17.
(b) In Flow's own database and memory: 2026-10-03.

### 5. The direction of a record type's upgrade
(a) Upgrade from the predecessor, upgrading the past (one record): 2026-10-02; sema-engine 0.18.0 `UpgradeFrom`.
(b) Possibly symmetrical, from and to (one record): 2026-10-02.
<!-- to-the-living:end -->
