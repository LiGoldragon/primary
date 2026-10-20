# References: The memory type and its traits

## Context

- flows/d68c82/notion/ethos.md, "The memory type and its traits" (the living, typed): the memory type implies each type in it bears the traits that make it storable; explore the pros and cons of explicit declaration, every trait explicit, or special objects
- flows/d68c82/vision/ethos.md, "Sema is the meaning language; the database is Memory" (2026-10-18): the naming used throughout
- flows/d68c82/vision/ethos.md, "One Ethos file holds one main object": registry addressing, one name one object
- flows/d68c82/vision/ethos.md, "Every file is a vector of variants; signal, memory and operation carry traits": withdrawn in its multi-object part; traits on the three aspects stand
- flows/d68c82/vision/ethos.md, "Traits in Ethos: long term" (2026-10-16): long term all traits in ethos, short term without
- flows/d68c82/vision/ethos.md, "White square brackets as sugar; layers; traits as capabilities" (2026-10-16): all traits declared in ethos, every implementation uses one
- field-context skills/compensation-design.md lines 24-25: "Every trait is written in ethos; hand-written code that is not ethos-generated declares no trait."
- psyche-context vision/ethos.md lines 62, 86-94, 308-314 (datom traits on every type), 370-374 (a trait is declared, never inferred), 450-455 (associations of the Signal and database roots implied, a Library's written)
- psyche-context vision/nexus.md line 152: a Nexus has three parts, each its own ethos specification

## Code, as read (not built)

- ethos-zero origin/main 07714b0: src/generation.rs 759-786 one fixed derive set (rkyv Archive, Serialize, Deserialize, Clone, Debug, PartialEq, Eq, Hash; datom Datomizable, Composing) for every type of every root; 1096-1137 associations emit only compile-time assertions; src/lib.rs 145-167 and 213-218 the Memory root has imports and record types only, no traits, associations, key, version or table section; fixtures/sink-associations.ethos the Library form; fixtures/entry-memory.ethos the Memory form
- ethos-zero src/main.rs 108-113 output named after the input file; src/lib.rs 143 "one file, one Rust module"; no registry in ethos-zero
- sema-engine 988490: src/record.rs EngineRecord (record_key, by hand), EngineStoredValue (blanket from rkyv), EngineStoredRecord (blanket); src/memory/mod.rs MemoryDefinition (memory_version, schema_hash, by hand), Memorable (optional), UpgradeFrom
- flow origin/main 67b80b3: crates/flow-nexus/src/store.rs and store/*.rs 39 impl EngineRecord and 13 impl MemoryDefinition, by hand; flow's seven .ethos files are six Library and one Operation, none a Memory root

## Unknowns

- whether the target traits are sema-engine's current ones or a later design
- how a source-registry address maps onto a stored type (no code carries a registry)
- whether the count of 209 hand-written Flow traits is a different measure from the 264 trait-declaration lines read outside generated/
- whether ethos-v1-3 proposals 14-17 (flows/804eb9/books/ethos-v1-3.md) were ruled

## Proposals 1-3 (psyche-context vision/ethos.md)

- the line after line 62 in each proposal is the lines proposed; the three are alternatives, one to be chosen
