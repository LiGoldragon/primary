# Knowledge refresh: knowledge-ethos and knowledge-nexus

Curriculum commit 982929 (982929dbf7f5) on main, pushed; carries 920f5eb and 87aa0f3 with it.
Generate `Generated.{ 68 24 }`; Check `Checked.{ 68 24 }` (curriculum-deploy 0.6.3 built from its main fb171e3).
Primary: own commit 83f463fa, COPY 2ffa89d0bc810f5d3065b2f575f5ad6a01a2b574 (no conflict) on main@origin 7a7170e; main set to the copy and pushed.
Locks: KnowledgeRefresh 11634 (the two Curriculum skill files), PrimaryPublish 11636 (the four generated SKILL.md paths); both Released.

## knowledge-ethos

- "As of 14.2.0 ... three roots: Library, Signal, Sema" -> 16.0.0, four roots Library, Signal, Operation, Memory.
- Section orders -> adds Operation imports, operations, outcomes, types, marked proposed pending the living's word; Sema -> Memory imports, record types.
- "associations of query, response and record types are implied" -> Signal generates `Query`/`Response`, Operation `Operation`/`Outcome` from the two sections after imports.
- New: a `Sema` head is refused as `Conceptual.{ [ 0 ] Renamed.Memory }`.
- New (in the field-naming paragraph): a struct position may declare its type in place (`Brief.String`), held by name (`brief: Brief`).
- "Library or Sema derive Datomizable and Composing unconditionally; Signal archives" -> every root derives rkyv Archive/Serialize/Deserialize, Clone, Debug, PartialEq, Eq, Hash, with Datomizable/Composing behind `datom`.
- New: consumer depends on rkyv 0.8 always, datom-codec only under `datom`; a `Decimal`/`Meaning`/datom-codec `Error` position needs datom-codec 0.32.2's `rkyv` feature (which enables protos's).

## knowledge-nexus

Running-state paragraph, guillemet paragraph and the live_nexus.rs line unchanged (sockets and binaries re-witnessed live).

- "orchestrate 0.35.0 pins ... 3.0.2" -> kept, as the running orchestrate-nexus 0.35.0.
- New: orchestrate main 0.36.1 pins signal-orchestrate and meta-signal-orchestrate 4.0.0 on signal 7.0.0, sema-engine 0.17.0.
- "signal 7.0.0 consumed only by contract repositories" -> no running Nexus speaks signal 7.0.0.
- "signal-frame 0.4.0 superseded and still locked ... ethos-zero contracts 0.5.0 pin signal-frame 0.3.2" -> signal-ethos-zero and meta-signal-ethos-zero 1.0.0 on signal 7.0.0, no signal-frame.
- "flow-nexus 0.17.4 ... from s1-e167d8 branches; message-nexus 0.17.0 from s2-e167d8 ... until the branches land" -> both run what is now on main; flow 0.18.0 still pins signal-flow 7.0.0 (1c9e4b3) while signal-flow main is 7.1.0; meta-signal-flow 11.0.0; message 0.17.1 pins signal-message 8.0.0, meta-signal-message 0.8.0; all on signal 5.0.0.
- "sema-engine 0.16.0 is the store engine of flow and message ..." -> flow and message pin 0.16.0 (same limits); 0.17.0 executes Filter and lands an open as one write transaction; main 0.18.0 adds Memorable.
- New: every flow, message and orchestrate contract and orchestrate's clients generate with ethos-zero 13.0.0 and protos 0.31.0; orchestrate-test and flow-test inherit through flake inputs; only the ethos-zero contracts are on ethos-zero 15.0.0.

## Divergences from the brief

- The brief named four repositories on ethos-zero 13/protos 0.31. The Cargo locks show it is wider: signal-message, meta-signal-message, signal-orchestrate, meta-signal-orchestrate and orchestrate's workspace are on it too. The skill states the wider set.
- flow, message and their four contracts are on signal 5.0.0. The brief did not say this, and the skill now states it.
- signal-ethos-zero and meta-signal-ethos-zero lock ethos-zero 15.0.0, not 16.0.0.
- Generate also rewrote `.claude/agents/book.md` (+264 lines, the authored Book procedure). That change comes from curriculum-deploy fb171e3, not from a Curriculum commit. It is outside this flow's own paths, so it is left dirty and unpublished in Primary. Check passes with it written.
- The PrimaryPublish lock named the four generated Primary paths. The brief's "never a Primary path" was read as applying only to the Curriculum edit lock.

## Sources

- ethos-zero main 0edfc0c: Cargo.toml, README.md, UPGRADES.md (16.0.0, 15.0.0), ethos-zero.ethos, fixtures/print/flow-*.ethos, tests/generated/flow-*.rs, src/lib.rs `Intrinsic`.
- protos 15b41da8 and datom-codec 4dff16b4 Cargo.toml (0.32.2, `rkyv` feature).
- Cargo.toml and Cargo.lock at main@origin: orchestrate bc5cd36, signal-orchestrate 4e68345, meta-signal-orchestrate 972a3b0, signal-ethos-zero d2a98d3, meta-signal-ethos-zero d61bb37, flow ae05027, signal-flow 5860383, meta-signal-flow 2ac045c, message 7ffd4a2, signal-message d574200, meta-signal-message 14f5759, sema-engine 9884905 (log 692aa5e, 928f017, 489d290, c94f31c).
- flake.nix/flake.lock: orchestrate-test 5f0d568 (orchestrate bc5cd36), flow-test 67e1f0a (flow ae05027).
- s1-e167d8/s2-e167d8 bookmarks are ancestors of main in flow, signal-flow, meta-signal-flow, message, signal-message, meta-signal-message.
- Live: sockets under $XDG_RUNTIME_DIR and /run/lojix; running binaries orchestrate-nexus 0.35.0, flow 0.12.2 and 0.17.4, message 0.17.0, message-daemon 0.14.0, lojix 8.1.0.
