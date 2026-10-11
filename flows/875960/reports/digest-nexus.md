# Digest: what a Nexus is made of, for Flow's ethos

Source: flows/875960/reports/aggregate-nexus.md. Every line quotes the aggregate's quote of the living, trimmed (" … " joins spans); "distilled" lines are reviewed skill wording. Labels before a quote are headings, not quotes. A quote appears once; a later section points back by citation.

## 1. What a Nexus is made of

- Whole: "A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type." — vision-nexus Three parts and one path, distilled
- Whole: "All nexuses have to have all three." — d4ae97 nexus, 2026-10-07
- Sockets: "A Nexus opens at least two sockets. The ordinary socket serves ordinary peers. The meta socket is privileged — the root user of the Nexus — and configuration and privileged operations pass through it; every Nexus has one, since without it nothing could configure the Nexus." — vision-nexus Sockets, distilled
- Meta socket: "The meta signal is never optional: the daemon is configured only over its meta surface." — vision-signal Meta signal, distilled
- Meta socket: "A Nexus keeps a standard metadata tree. In it a type records whether the meta Configure was ever done; that record is reversed only on the meta socket, and while it is unset Configure is accessible on the ordinary socket." — vision-nexus First configuration, distilled
- Meta socket: "lets add to that metadata anything standard: socket paths (its own and the paths of all its other edge-sockets), and anything else that comes up as standard nexus configuration data." — acbb6006 archive-nexus, undated
- CLI: "A client is a separate program from the Nexus. For now the default clients are packaged with the Nexus as separate crates of its repository … one datom-converting CLI per socket, however many sockets the Nexus has, at least two." — vision-nexus Default clients, distilled
- CLI: "The textual form is datom; a CLI actualizes it and sends signal; a Nexus never textualizes." — vision-signal Text and signal, distilled
- CLI: "meta cli names is <component>-meta." — f6db8d metaCli, 2026-09-12
- CLI: "we make the library, and all the CLIs have to use the library to force them into this pattern. All of the CLIs just take a datom payload, all the options, all the help, and everything, which can be added on." — b81560 operational-flowDatomCLIAndSignalLibrary, undated
- CLI: "It identifies the process that causes the CLI and passes it into the message. … Not by trusting that the flow put its ID in the message, but from the virtue of the process that called it" — 8904b1 skills, 2026-09-28
- Start: "A Nexus starts with no arguments and there is no bootstrap binary. Its executable holds a default configuration as a constant." — vision-nexus Configuration, distilled
- Start: "first it should try to get its state from the default location for its Sema database. … Because the default configuration when creating a new database should set the configuration as the defaults in the database." — 01a03d6e archive-nexus, 2026-08-26
- Start: "on a never configured nexus, the ordinary socket could get a configure interface which works but rejects if already configured." — 01a03d6e archive-nexus, 2026-08-26
- Start: "this is independant of the builtin default configuration, which are needed since otherwise we wouldnt have a socket path to even fall back on to even allow the configure signal to come in." — acbb6006 archive-nexus, undated
- Configuration (latest): "We need to allow the Nexus to have its configuration loaded atomically so that it can live in separate files in different repositories. … (basically Datom payloads for configuring that particular Nexus that the CLI can use in succession to start up that Nexus with the right payload on the meta socket)." — 445410 nexus, 2026-10-09
- Signal: "Signal is the messaging layer: fully binary, portable rkyv fixed across endianness, fully typed with both sides knowing the full schema, nothing on the wire labeling itself." — vision-signal What signal is, distilled
- Signal: "A Signal declares queries and responses; input and output are too low-level for it." — vision-signal Query and response, distilled
- Signal: "Signal is portable rkyv plus whatever protocol is standardized on top of it. The protocol is to be decided." — vision-signal Protocol, distilled
- Signal: "Every client speaks to a Nexus in pure signal, fully binary. A Nexus speaks only the signal contracts it is compiled with; two of these are its own, one per socket." — vision-nexus Signal only, distilled
- Refusals: "When we're designing a signal interface, the input maybe should be even called commands or requests, because they could be refused. … And it should be an imperative voice, right, as in list." — 01a03d6e archive-ethosInterfaces, 2026-08-26
- Refusals: "when you have a start refused and then one of the variants is launching. How does that work? If it's refused how is it launching? That doesn't make sense to me." — 91ea9f ethos, 2026-10-02
- Refusals: "We can get very specific types of error messages just based on the way we parse and the way we generate the protos." — b81560 operational-nexusProcessObjectsAndEthosInDatom, undated
- No strings: "There should be no datom in any Nexus. It's going to be forbidden for string handling to be in the Nexus." — 8475a9 datom, 2026-10-05
- No strings: "The nexus only decodes known types using rkyv … it's really important that we don't put any extra logic for handling deserialization and serialization of text in the Nexus because the Nexus has to stay small." — 8904b1 skills, 2026-09-28
- Minimal forms: "You can have these shorthand types that are usually default, and then you have the more explicit longer name. Let's make this a design standard in the skill for specifying signal." — 692df8 signal, undated
- Operation: "An object enters a Nexus for the effect; the response follows as an effect of it. Conversion is the wrong frame for it." — vision-nexus Processing is for the effect, distilled
- Path: "Anything that can have an effect is going to have a corresponding operation … We're going to have to go through these types to go from signal to operation to memory and back into operation. If the memory has changed and there is a successful memory edit kind of return operation, that's going to end with a signal, probably sending a response back that the effect has taken place." — 91ea9f ethos, 2026-10-02
- Path: "the signal has to go through the operation actor/system in order to reach the memory actor/system, then back through the operation system and back out through the signal. … If that can somehow be enforced in Rust … then you can have effective compliance with ethos." — 5ed94b nexusEntryPoint, 2026-10-04
- Path: "Signal can only talk to operation. Memory can only talk to operation. That way we have to go through this operation process." — bad807 nexus, 2026-10-04
- Memory: "Its Memory is its own typed store, reached only through the memory engine; there is no central store; policy state and working state live in that one store, and policy changes only over the meta socket." — vision-nexus Signal only, distilled
- Memory: "Sema is the database engine of a Nexus, authored in Ethos so the stored types are visible; its root, Sema, declares record types. It matters more than nexus, because operational editing should yield the migration with the edit." — vision-sema What sema is, distilled
- Change kind: "It's going to be a kind that's going to have a standard successful or unsuccessful change implemented on these particular data types. Also each version is possibly going to have an implementation of an upgrade from or an upgrade to. … I guess an upgrade from makes more sense" — 91ea9f ethos, 2026-10-02
- Hashes: "The flow ID is not a string, it's a hash. … The Nexus just thinks of it as a hash, which is maybe an integer with certain kinds of traits." — edf227 identifiers, 2026-10-03
- Fingerprint: no line in the aggregate uses the word; nearest is "using the containing source with hash (blake3 I believe is what we use?)" — 73ada7 nexus, 2026-10-09
- Subscription: "State is observed by subscription: the subscriber receives the state on open, then each change as it happens." — vision-nexus Observation by subscription, distilled
- No polling: "Polling is forbidden; a correct system goes quiet when nothing changes." — vision-nexus Polling is forbidden, distilled
- Actors: "The engine inside a Nexus is driven by Kameo actors. The standards of their use are still to be designed. Arc-Mutex is permitted." — vision-nexus Actors, distilled
- Actors: "an actor, a main actor, which could have multiple sub-actors (like the signal actor), would only be able to talk to the operation actor, which could talk to both signal and memory." — bad807 nexus, 2026-10-04

## 2. Storage and memory

- Already in §1: vision-nexus Signal only; vision-sema; 01a03d6e 2026-08-26 default location; 91ea9f 2026-10-02 change kind; edf227 2026-10-03 hash; 73ada7 2026-10-09 blake3.
- "all of the daemons hold that language in memory, in their database. Not in memory, in their database. So they can fetch it back. … They can edit it." — 55d18f4f everythingIsInTheDaemon, 2026-08-08
- "to expose the types that the database stores … it would allow the agent to more easily understand how to upgrade, how to do a database migration." — vision-raw archive-rustComponentArchitecture, 2026-08-14
- "When we create the SEMA Ethos type for the root type, like we have library and signal, then we're going to be defining database record types." — 564f55 archive-sema, 2026-09-09
- "When we finally define the SEMA object type for Ethos, I want to take the version number out of Ethos." — 564f55 archive-ethos, 2026-09-09
- "a sema ethos type, which would have a storage type or a record type (whatever you want to call it) that would have associated kinds, implied associated kinds." — 6329f1 archive-ethos, 2026-09-04
- "every concept is going to go all the way through a process and somewhere where it's recorded in storage, where some things can be maybe made more efficient in storage." — 024bc7 storage, 2026-09-13
- "We're going to need to handle database upgrades or the database when the records change. We're going to need to specify a better way do that" — e51411 nexus, 2026-09-25
- "Nexus still doesn't have some kind of version control system for their data, which we're going to need." — 8904b1 presentation, 2026-09-28
- "data migration from the changes, it's using operational editing as an operation, which becomes the migration itself. … The ethos language will then have its structure for how it stores itself in the nexus, so those will be ethos versions." — c64ee3 ethos, 2026-09-29
- "No the configuration flow does not live in a Markdown file in every story. It lives in its own database and its memory." — edf227 flow, 2026-10-03
- "Let's look at what types people use for hashes in actual fast Rust code and that's the type we're going to use to store it." — d4ae97 datom, 2026-10-07
- "certain types in ethos, will have to have a different representation than how they're stored in the runtime. For example the SHA-256 is a good example." — d4ae97 datom, 2026-10-07
- "In the case of the memory, everything goes into the nexus but the CLI, I think, only uses the signal" — 0c85a3 memory, 2026-10-07, notion
- "the file location shouldnt matter from the nexus' pov; it must use a registry … those payloads live on the meta signal (to modify those registries)." — 73ada7 nexus, 2026-10-09
- "It can refer to a certain Git with a certain revision and we keep our own Blake3 hashes. … It would be the snapshot of that revision that we hash, kind of like how Nix does." — 058f16 source, 2026-10-10
- "The hash is there for us so that we can verify that the files are the right files when we use them. That's all. … This is not the priority lane." — 058f16 source, 2026-10-10
- "the name of the repo and the name in the registry, in our own memory, our own Nexus memory, doesn't have to be the same." — 058f16 source, 2026-10-10
- "Essentially, sema is storing Signal, so it's all Signal. The data itself, we're going to refer to it as Signal when it's binary and it's typed." — 692df8 identifiers, undated
- "Let's keep the storage layer thin. Let's be very specific about what we store as a string, which is expensive." — 840e42 logging, undated
- "if curriculum is a nexus, we can't have any data there because it's going to keep rebuilding it. We need curriculum data." — 108ab0 operational-curriculumAsModuleSystem, undated
- "But the Flow's memory will live in mind, and so mind will become our most bloated component in terms of the database quickly." — 9993b5 mindMemory, undated
- "We can just have a registry with paths to all of these context modules in the flow memory itself. … If we just feed the text in the memory, that would solve the problem." — e5a0bc flow, undated
- "you're going to have to manage storage on a system like this and how to store it to make links work, which is in a content-addressed way." — f38926 archive-meaningLanguage, undated

## 3. Traits of a Nexus

- Already in §1: 91ea9f 2026-10-02 change kind and upgrade from; edf227 2026-10-03 hash with traits; 5ed94b 2026-10-04 enforcement.
- "Every method lives in a trait; an inherent method is a trait not yet extracted." — vision-nexus Universal traits first, distilled
- "every concept should really have its repo, and if anything goes in there, the traits can, since every concept deserves at least one trait, and probably more." — vision-raw everyConceptShouldHaveItsRepo, 2026-08-09
- "We need to first design universal nexus traits, which would be the basic ontology of an actor/dataflow software system." — e06e4c07 archive-nexus, 2026-08-19
- "And then we need to isolate the traits, which is the ways in which these things, the ways these things interact, and put the proper names on them." — aa4c7747 archive-ethosMonolith, 2026-08-24
- "observe is more universal, and reuse is good, because there's going to be multiple nexuses … observe is the root variant, and then it has … another enum" — 01a03d6e archive-ethosInterfaces, 2026-08-26
- "When the CLI uses the signal library, it would derive Datomizable and composable, but when the Nexus compiles the same signal library, it would compile it without any of the textualization capability." — 564f55 archive-signal, 2026-09-09
- "potentially we're going to have Ethos create some default implementations for `query` and `response`, which is why we have this specialized Ethos file type." — 564f55 archive-ethos, 2026-09-09
- "We have this Nexus type, the sema type, and the signal type and they each have their own intrinsic kinds applied to the types so that they're of that specific actor. Only this kind of actor can react with this type of object. … an architecture guard basically." — 6cc91b nexus, 2026-09-14
- "how the trait enforces that it can only be used inside of a particular meta actor … We have the processes in the Nexus runtime that act as the only way to a Sema transformation." — e1953c nexus, undated
- "We have two standard signal handshakes. One checks the origin process of the call for the message to know where the message came from." — b05237 operational-signalOriginHandshake, undated
- "Let's do the name-based hash thing in the signal library." — fd0f97 identifiers, undated
- "I want to see traits also because all of the behavior, basically all of the traits. … we need to define all of the traits and all of the types in Ethos. Let's give this a shot on Flow." — 875960 flow, 2026-10-11
- Absent: no line in the aggregate names fingerprint, encode or apply as a trait.

## 4. Contradictions and later corrections

- Nexus repo: db97561c archive-nexus, undated ("Nexus should be the universal Nexus library … ethos-zero is where the daemon should be") is quoted as "this is wrong" by fe34eb nexus, 2026-09-10 — fe34eb is later.
- Nexus Core: e06e4c07 2026-08-19 and 564f55 2026-09-09 name a Nexus Core; fe34eb 2026-09-10 "overthinking"; 024bc7 2026-09-13 and 6cc91b 2026-09-14 reintroduce it; vision-nexus distilled "Nexus always names the whole" is the reviewed word.
- Input/output: 564f55 archive-nexus 2026-09-09 "input and output are actually good names for nexus" against 564f55 archive-ethos 2026-09-09 query and response; vision-signal distilled keeps query and response.
- Third part: 024bc7 2026-09-13 "The Sema: the storage part"; 91ea9f 2026-10-02 "process" and "storage", then "signal, operation, and memory" — 91ea9f memory is later and distilled.
- Sema's name: vision-sema distilled "database engine" and 564f55 2026-09-09; against 93ba9f 2026-09-26 and 8904b1 2026-09-28 "SEMA becomes the meaning language" — 8904b1 is the latest dated; the distilled skill's date is not in the aggregate.
- Messaging Nexus: e51411 2026-09-25 "Even the nexus should be called Messenger." against d4ae97 2026-10-09 "message should be called message." — d4ae97 is later.
- Datom in a Nexus: bad807 2026-10-04 (pull a value from a datom file) and b05237 undated (Nexus passing Datom) against 8475a9 2026-10-05 "There should be no datom in any Nexus." — 8475a9 is later than bad807.
- Configuration: 01a03d6e 2026-08-26 (configuration held in the Sema database at its default location) beside 445410 2026-10-09 (configuration files loaded atomically as Datom payloads on the meta socket) — 445410 is later; whether it replaces or adds is not settled.
- Arc-Mutex: fd301d9a 2026-08-21 "Re arc mutex ban: I dont like the approach anyway" against vision-nexus Actors distilled "Arc-Mutex is permitted."
- Signal's place: 564f55 archive-signal 2026-09-09 "the Signal layer between the concept and the in-memory rest value" against 564f55 archive-protos 2026-09-09 "That's a parallel structure"; vision-protos distilled keeps parallel.
- Encoded form: vision-raw 2026-08-06 "The encoded form is the code." against vision-raw 2026-08-13 "working form and signal form, drop code/encoded entirely" — 2026-08-13 is later.
- Locking: aa4c7747 2026-08-25 orchestrate nexus "that reserves paths" against 9993b5 orchestrateLocking undated "I really don't want to have it like we used to, where we just worked with orchestrate, and we can lock files."

## 5. The aggregator's tension paragraph (inference of flow 875960, not witnessed)

- Nexus Core / metaNexus as named parts (564f55, 6cc91b, e1953c, 024bc7) against "overthinking the whole nexus-core runtime concept" (fe34eb) and "Nexus always names the whole".
- Sema as database engine against renaming the database and keeping Sema for the meaning language (93ba9f/b7ba00, 8904b1).
- The third part named process, storage, or memory (91ea9f 2026-10-02).
- Messenger (e51411) against "message should be called message" (d4ae97).
- A Nexus with no datom against one that pulls a datom value from a file or passes datom messages (aa887c/bad807, b05237, 183ae0).
- Everything a Nexus against Clojure tools or no nexus for a given job (6f51ad, 01a047d2).
- Signal as a layer between concept and composition against Signal as a parallel structure (564f55, vision-protos).

## Sources

- /home/li/primary/flows/875960/reports/aggregate-nexus.md (read whole, 544 lines); original record files not re-read.
- Provenance receipt: unavailable; no PROVENANCE handoff was received.
