# «A Nexus reads a value from a datom file»: rulings

Summary of the proposals in `8-datom-file.md`:

- 1 `Vision/nexus.md` new "A value from a file": the Nexus answers `ReadFile` naming the wanted type and the path; the CLI reads, actualizes and sends `Supply`; only Nexuses that need it declare it.
- 2 `Curriculum/skills/datom.md` line 95: a CLI reads a datom file only when its Nexus answers `ReadFile`.
- 3 `Curriculum/skills/vision-nexus.md` line 14: one sentence on `ReadFile` and `Supply` over two exchanges.
- 4 `aggregator/src/daemon.rs` lines 35 to 38: the daemon stops reading `configuration.datom`; `meta-aggregator` sends it as `Configure`.

## Rulings

1. Which way a Nexus gets a value from a datom file.
   (a) It runs a reader subprocess named by a variant: 2026-10-04, his comment on «The Nexus», "a variant … that would tell it what type of CLI you would have to use".
   (b) It asks with `ReadFile`, the connected CLI supplies: 2026-10-04, his comment, "ostensibly the CLI that it's meant to work with"; the flow's proposal.
   (c) The caller reads and sends it, the Nexus unchanged: 2026-10-04, "unless all of that is, again, put into an external tool"; 2026-09-29, 183ae0 (a notion), "next to it would be the compiled signal file".
2. Whether the no-text rule admits a path string in a Nexus.
   (a) Yes, a path held and passed but never parsed: `Vision/nexus.md` "Signal only", "the string fields it still carries are records on the way to a fully typed form".
   (b) No, a path is first given a type of its own: 2026-09-15, 692df8, "in a way, it's a string when you print it, but it's not a string per se".
3. Whether every Nexus can ask for a file.
   (a) Only those that declare it in their Signal: 2026-10-04, his comment, "Maybe not all the Nexuses need this".
   (b) Every Nexus, through the shared nexus library: `Vision/nexus.md` "First configuration", "whatever else comes up as standard nexus configuration data".
