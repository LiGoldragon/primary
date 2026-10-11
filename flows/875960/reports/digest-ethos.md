# Ethos digest for Flow's ethos

Drawn only from flows/875960/reports/aggregate-ethos.md; every quoted line is the aggregate's, trimmed with "…". Lines marked "Digest note" are this digest's own inference.

## Load-bearing statements
- "Ethos is the schema language. … Ethos specifies the types and Datom fills them with data. Ethos is central. The anatomy of the system, every type and every trait it uses, is read in its ethos; an implementation is mostly the hand-written bodies." — vision-ethos «What Ethos is», distilled vision-ethos
- "we need to define all of the traits and all of the types in Ethos." — 875960 flow, 2026-10-11, vision
- "The unit is File: one file, one Rust module. No namespace inside a file. An ethos file is written in the sweet form: the root's head, then the sections as siblings, the outer braces omitted. … A Library's sections, in order, are imports, types, traits and associations." — vision-ethos «Declaration: File», distilled vision-ethos
- "An ethos file carries no version; datom has no versions. What is versioned is versioned in a manifest of some kind, never in the file." — vision-ethos «Declaration: File», distilled vision-ethos
- "An import names a source and a type: `protos:String` or `protos:[ String Integer ]`. … Intrinsic names known without import: String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self. … `Topic.custom:Name` declares `Topic` over the type `Name` from the source `custom`." — vision-ethos «Imports», distilled vision-ethos
- "If it starts with a capital letter, then it means it's pulling directly from the core built-ins." — 1d0733 ethos, 2026-10-09, vision
- "Otherwise, if it starts with a small letter, then that means it's pulling in from the registry name." — 1d0733 ethos, 2026-10-09, vision
- "The generated code carries no `use` statements; each imported name is written fully qualified" — vision-ethos «Imports», distilled vision-ethos
- "Each section has its own parsing context; placement carries the meaning. … Where types are defined a bracket is an enum, never a vector." — vision-ethos «Shapes and placement», distilled vision-ethos
- "A type used once is declared inline where it is used; a type used in more than one place is declared once and named. A variant's payload is written in the variant and bears the variant's name; no second type is invented to hold it. Inline nesting goes about three deep; past that, the type comes from a Library." — vision-ethos «Inline types», distilled vision-ethos
- "The inline struct or enum is a full type whose derived name carries an underscore" — vision-ethos «Inline types», distilled vision-ethos
- "When a variant's name is a type already defined in the library, that type is the data the variant carries. Nothing further is written." — vision-ethos «A variant named as a defined type carries that type», distilled vision-ethos
- "Instead of naming a defined type, a variant may declare what it carries in place: a vector, a struct, or an enum, each a full type with a derived name, recursively." — vision-ethos «A variant may declare its payload inline», distilled vision-ethos
- "You can use a type, `type ethos`. It just starts with `type` and it defines a single type and you can define everything inline" — 081064 ethos, 2026-10-10, vision
- "Everything is a type." — 91ea9f ethos, 2026-10-02, vision
- "Anything that can have an effect is going to have a corresponding operation, which is going to be the type that we have to use." — 91ea9f ethos, 2026-10-02, vision
- "single-field structs are forbidden. If it was a string, it would be just a new type, and I want the new types not to be type aliases." — ebbe30 ethos, 2026-10-09, vision
- "Why are you going to wrap a new type with another new type? Don't double-wrap types." — d4ae97 ethos, 2026-10-06, vision
- "We don't have key-value in Ethos anymore." — 91ea9f ethos, 2026-10-02, vision
- "No tuple in the code we design; if some parts require it (standard traits, dependencies), then it is allowed at that contact point only." — vision-ethos «Associations», distilled vision-ethos
- "We can start leaning more on [structs] than on chaining up [variants], which ends up in an ugly Ethos pattern." — bad807 ethos, 2026-10-04, vision
- "I think rather the voice is a struct that contains the aspect and the layer, and the flow has a role, one of which is a voice." — bad807 ethos, 2026-10-04, vision
- "whenever you have a variant in ethos you need to position the variants hierarchically. There's an implied hierarchy: the first one is most senior." — d4ae97 ethos, 2026-10-07, vision
- "In Protos languages like datom and [Ethos] for things that are not types or traits, we are going to use uncapitalized. It's going to be camel case because we do PascalCase for defined objects in the language and we do variants." — 058f16 identifier, 2026-10-10, vision
- "technically it should be uncapitalized core and ethos since theyre the core:Name type which is "camelCaseExpression" type with runtime checks when creating a new one" — 1d0733 ethos, 2026-10-09, vision
- "In Ethos, we're going to describe the real type, the real Rust type that it has, and then the special representation is going to implement the representation type." — ebbe30 ethos, 2026-10-09, vision
- "A declaration turns into the Rust type with named fields, bearing the datom traits through the derive … A field is named after its type in snake case; a constructed type type-first, `string_vector`, `lock_option`; a repeated type as first and second." — vision-ethos «What a declaration turns into», distilled vision-ethos
- "Ethos Zero emits `Datomizable` and `Compositional` on every struct and enum it generates … An alias bears them through the type it names: an alias is not a new type and cannot carry a derive." — vision-ethos «Every declared type bears both traits», distilled vision-ethos
- "A generated signal library bears `Datomizable` and `Compositional` conditionally, under a feature the CLI and client enable and the Nexus does not." — vision-ethos «The datom traits are compiled in only where text is spoken», distilled vision-ethos
- "Any repetition in ethos syntax is an implementation failure. … Terseness is in the low amount of noise, never in shortened words." — vision-ethos «Non-repetition», distilled vision-ethos
- "Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. … Ethos carries a comment on every section and on every line that has a next layer" — vision-ethos «Spacing», distilled vision-ethos
- "maybe we can try three. I like the number three so I think we should give it a shot." (indentation) — f5a6e9 ethos, 2026-10-07, vision
- "You need to always specify your object type in Ethos." — 692df8 ethos, vision
- "Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code." — vision-ethos «Flow, a current best example», distilled vision-ethos

## Roots
- "Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs." — vision-ethos «Roots», distilled vision-ethos
- "In the Signal and Sema roots the associations of the query, response and record types are implied and never written. In a Library they are the fourth section, after the traits." — vision-ethos «Associations», distilled vision-ethos
- "Ethos may generate default implementations for Query and Response, which is why Signal is its own root." — vision-ethos «Shapes and placement», distilled vision-ethos
- "In Ethos I want to specify the three aspects: - the signal - the memory - the operation" — 081064 ethos, 2026-10-10, vision
- "All nexuses have to have all three." (signal, operation, memory) — d4ae97 nexus, 2026-10-07, vision
- "When we write a nexus, essentially all of the types, because we have three layers, are going to be in one of the three layers or in the library." — 0c85a3 ethos, 2026-10-07, vision
- "Yeah the memory is good. That's what it is I guess: signal, operation, and memory." — 91ea9f ethos, 2026-10-02, vision
- "so we can have the signal, the process, and the storage." — 91ea9f ethos, 2026-10-02, vision
- "describing the signal, process, and storage parts in ethos of Flow" — 91ea9f flowNexus, 2026-10-02, vision
- "I'm not a big fan of storage but something that emphasizes the kinds of things that are memorized, as in a database, but maybe with a better concept vocabulary." — 91ea9f ethos, 2026-10-02, vision
- "I don't know what yet storage is." — 91ea9f ethos, 2026-10-02, vision
- "It's going to be a kind that's going to have a standard successful or unsuccessful change implemented on these particular data types." — 91ea9f ethos, 2026-10-02, vision
- "Also each version is possibly going to have an implementation of an upgrade from or an upgrade to. I'm not sure." — 91ea9f ethos, 2026-10-02, vision
- "You have the library, which combines them, and signal, which is more specialized." — b05237 operational-ethosTypeRoot, 2026-09-19, vision
- "So for a signal type, it would have an import vector, a request vector, and a response vector" — e8c4cc61 archive-ethosFileAnatomy, vision
- "the signal's root-level enums are `query` and `response`." — 564f55 archive-ethos, 2026-09-09, vision
- "When we create the SEMA Ethos type for the root type, like we have library and signal, then we're going to be defining database record types." — 564f55 archive-ethos, 2026-09-09, vision
- "You have the signal, sema, and nexus type." — 564f55 archive-ethos, 2026-09-09, vision
- "Well, Nexus's sections are input and output, so it's kind of similar to Signal." — 564f55 archive-ethos, 2026-09-09, vision
- "you have the signal layer, the nexus layer, and the sema layer, and these are described in ethos. That's what that database is: it stores that namespace." — 024bc7 nexus, 2026-09-13, vision
- Digest note: the aggregate holds no "storage ethos" and no "store" as a root name before 2026-10-11; "storage" appears only in the three 91ea9f lines of 2026-10-02 above, each with "signal" and "process", and the same record settles "memory". "stores" appears once, of the Sema database (024bc7).

## Traits
- "Trait is the word for the bearer of capabilities, the same word in ethos and in Rust; kind might be used to also mean traits. In ethos there are no generics, only traits. … A capability speaks in Self, the trait's own parameters and other traits; a concrete type in an input is a trait not yet named." — vision-ethos «Trait», distilled vision-ethos
- "Traits are qualifier-named: Runnable, Textualizable, Structural, Embodied. Run is not a trait. The verbs Rust imposes, Write and Read among them, are tolerated as legacy" — vision-ethos «Naming», distilled vision-ethos
- "A trait is identified as a Rust trait is, by its name and its constraints, written as one head: Processable<[Clonable Sendable] Serializable>. … its supertraits, its associated types and constants, its capabilities, is its definition." — vision-ethos «Identity», distilled vision-ethos
- "A trait is declared, never inferred; an association asserts the type bears it. The generated Rust carries a compile-time assertion that the type bears the trait; the interaction body is hand-written Rust." — vision-ethos «Traits are explicit; bodies are hand-written», distilled vision-ethos
- "A simple trait opens with a bracket after the dot. … `.` takes self, `!` takes mutable self, `:` takes no self. … A yield bracket holds one type. A complex trait opens with a brace after the dot. Inside: supertraits …, associated types …, associated constants … — upper case, each the name, a dot, and its type — and capabilities in a bracket." — vision-ethos «Trait syntax», distilled vision-ethos
- "An association declares that a type bears a trait: the type's name, a dot, a bracket of its traits. … Interactions — the term for trait implementations — use the type itself in all cases." — vision-ethos «Associations», distilled vision-ethos
- "Every method call in our Rust code lives under a trait, because traits are the comprehension surface" — intent-mandatory-traits «2026-08-13 — approved», 2026-08-13, distilled intent-mandatory-traits
- "We forbid freestanding implementations. All implementations must be of a trait." — 995a164e rust, 2026-08-31, vision
- "Everything must fall under a trait. If the trait design is wrong then there's something wrong with the anatomy of the design of the system." — 8475a9 datom, 2026-10-05, vision
- "I was saying we can mechanically make sure there's no trait in the non-ethos-generated part of the code" — d4ae97 ethos, 2026-10-07, vision
- "A trait that only has one function is suspicious and a trait that's only implemented by one type is doubly suspicious." — d4ae97 ethos, 2026-10-06, vision
- "There's probably a bunch of other capabilities that we could agglomerate under an appropriately named trait, like a Claude host trait. I guess we can use either a qualifier or a name for traits." — d4ae97 ethos, 2026-10-06, vision
- "the machine is just inventing a whole bunch of silly traits that are not really load-bearing" — d4ae97 ethos, 2026-10-06, vision
- "the traits are something that the types implement. We don't look for traits and then think of types for that." — vision-raw archive-traitsAsCapabilities, 2026-08-13, vision
- "we want to have as many common traits as possible, because then we're creating the right abstraction." — vision-raw archive-traitsAsCapabilities, 2026-08-13, vision
- "I think we went more towards the qualifier `launchable`. I think that makes more sense because that then cognitively translates as a kind." — 91ea9f ethos, 2026-10-02, vision
- "A kind names one conversion and is borne by the type that undergoes it, named for the layer it becomes. Each step yields a wholly new type." — intent-conversion «A kind names one conversion», distilled intent-conversion
- "It would be a trait, a special representation, like a custom Datom conversion, basically." — ebbe30 ethos, 2026-10-09, vision
- "There is going to be an associated constant, possibly in each kind, to hold the value of its forms" — 995a164e layerMatching, vision
- "Essentially, an implementation would be mostly a bunch of implementation blocks, whereas the traits would be generated by ethos kinds" — 8325c1 ethos, 2026-09-13, vision
- "If there is a Nix closure, the action of copying the closure is an implementation on the type of the Nix closure." — 8325c1 ethos, 2026-09-13, vision

## Contradictions and later corrections
- "If I say traits I mean kinds." — 26c50c ethos, 2026-09-24 / "I guess we can use traits." — ebbe30 ethos, 2026-10-09. Later: ebbe30.
- "all traits will be qualifiers." — 6863ef19 archive-traitsAsCapabilities, 2026-08-13 / "Yes, I accept verbs." — 06196cc7 archive-traitsAsCapabilities, 2026-08-14. Later: 06196cc7.
- "Yes, I accept verbs." — 06196cc7, 2026-08-14 / "I also want to lean back to writable > write" — f426777b archive-spokenVocabulary, 2026-08-26. Later: f426777b.
- "Traits are qualifier-named" — vision-ethos «Naming», undated / "I guess we can use either a qualifier or a name for traits." — d4ae97 ethos, 2026-10-06. Order undated.
- "So I dont see a trait syntax" — aa4c7747 archive-ethosTraitSyntax, 2026-08-24 / "we need to define what the trait syntax for Ethos is" — aa4c7747, 2026-08-24, and vision-ethos «Trait syntax». Same day.
- "Ethos doesn't generate implementations" — 564f55 archive-ethos, 2026-09-08 / "I never said that Ethos Zero should not generate implementations." — 564f55, 2026-09-08. Same day; the second corrects.
- "the interaction body is hand-written Rust" — vision-ethos «Traits are explicit…» / "I want you to reconsider if we exclude expanding ethos to do implementations (i.e., functions)" — e51411 ethos, 2026-09-25. Order undated.
- "all the traits should not now [sic] have to be written in the ethos" — d4ae97 ethos, 2026-10-07 / "I was saying we can mechanically make sure there's no trait in the non-ethos-generated part of the code and my speech detect got me off." — d4ae97, 2026-10-07. Second corrects.
- "the signal, the process, and the storage." — 91ea9f ethos, 2026-10-02 / "signal, operation, and memory." — 91ea9f ethos, 2026-10-02. Same record.
- "You have the signal, sema, and nexus type." — 564f55 archive-ethos, 2026-09-09 / "In Ethos I want to specify the three aspects: - the signal - the memory - the operation" — 081064 ethos, 2026-10-10. Later: 081064.
- "Four roots: Library, Signal, Operation, Memory." — vision-ethos «Roots» / "In the Signal and Sema roots the associations … are implied" — vision-ethos «Associations». Both distilled, same skill.
- "Head then symbol is … an alias in the types section." and "an alias is not a new type" — vision-ethos «Shapes and placement», «Every declared type bears both traits» / "I want the new types not to be type aliases." — ebbe30 ethos, 2026-10-09. Order undated.
- "`Topic.custom:Name` declares `Topic` over the type `Name`" — vision-ethos «Imports» / "Topic:custom.Name is what I had in mind, but there is a problem with that now that I see it. Maybe it's Topic:custom:Name" — d5df1d ethos, 2026-10-09, notion. Order undated.
- "basically PascalCase of a certain number of words" — f5a6e9 flow, 2026-10-08 / "the core:Name type which is "camelCaseExpression" type" — 1d0733 ethos, 2026-10-09. Later: 1d0733.
- "it should be CAPACITY. and use a key-value map delimiter" — ad19b1 archive-ethos, 2026-09-04 / "We don't have key-value in Ethos anymore." — 91ea9f ethos, 2026-10-02. Later: 91ea9f.
- "That's why I was thinking we limit it to three depths" — 91ea9f ethos, 2026-10-02 / "We don't have to make it a hard limit." — 91ea9f ethos, 2026-10-02. Same record.
- "I think we're going to abandon this idea that we wouldn't have an enum where each data-carrying variant carries the same type" — bad807 ethos, 2026-10-04 / "a pattern in Ethos that I would like to develop … a series of variants one after another." — aa887c ethos, undated; aa887c also: "We can start leaning more on [structs] than on chaining up [variants]". Order undated.
- "ethos-zero is where the daemon should be." — db97561c archive-nexus, undated / "no, ethos-zero is not a daemon, hence its name." — fe34eb ethos, 2026-09-10. Order undated; vision-ethos «Zero» follows fe34eb.
- "ethos isnt datom-expressible." — 1c282d archive-protosizable, undated / "Basically, ethos becomes a payload in datom" — b81560 operational-nexusProcessObjectsAndEthosInDatom, 2026-09-19; vision-datom «Relation to Ethos» leaves "ethos might be read as datom in one pass" unsettled.
- "Ethos is not really about strings yet" — 564f55 ethos, 2026-09-08 / ""ethos isnt about strings" is bad vision." — 564f55 ethos, 2026-09-08. Second corrects.

## Not yet expressible
- "Zero as in version 0: no daemon yet, no Nexus." — vision-ethos «Zero», distilled vision-ethos
- "In Ethos do we have an Ethos Nexus or is Ethos Zero a non-Nexus? We need to migrate the Ethos Nexus version so that we can do this." — 081064 ethos, 2026-10-10, vision
- "Let's get a fable on Ethos to make sure that we got the vision right, because there have been some changes, and I think the implementation doesn't follow them." — ebbe30 ethos, 2026-10-09, vision
- "I guess we would need the datom file expansion and also all of the things that I've been talking about modifying ethos syntax to be implemented in ethos." — d4ae97 ethos, 2026-10-06, vision
- "Ethos will eventually replace everything, Rustlang becoming its assembly layer. … what it enables — generator emission among it — comes in its time." — vision-ethos «Horizon», distilled vision-ethos
- "we should spec everything in Ethos and then have a standard, maybe even eventually code, from which Ethos code creates the types, the functions, and the logic" — d4ae97 flow, 2026-10-08, vision
- "The step to change the data is the same as the edit that's made to the source code because, in ethos, we're going to specify ethos in its own ethos language." — c64ee3 ethos, 2026-09-29, vision
- "The help menu can be generated from the ethos but not by copying the string of the source code programmatically" — 752e0f helpMenu, 2026-09-24, vision
- "Datom, the data dialect of the Protos family, may gain an inline place in authored Ethos … That road is reached, or even floated, only with explicit context" — vision-datom «Nature», distilled vision-datom
- Digest note: the next four come from the aggregate's other sections, not "Ethos-zero today".
- "Is it because we don't support mutexes in Ethos, so the machine feels obligated to define that type in Rust directly?" — d4ae97 ethos, 2026-10-06, vision; "can we support mutex?" — ebbe30 ethos, 2026-10-09, vision
- "We need a way to essentially refer to Rust types from Ethos, which I guess we already do. Maybe it's just a special import syntax" — 058f16 ethos, 2026-10-10, notion
- "That would mean fleshing out the function syntax in Ethos, implementations … Maybe the manifest needs to be fleshed out better for compiling and finding dependencies" — e51411 ethos, 2026-09-25, vision
- "Like I said it's only a subset because it doesn't have all the types yet." — d4ae97 ethos, 2026-10-08, vision

## Sources
- flows/875960/reports/aggregate-ethos.md, read whole at its current working-tree state.
- Provenance receipt: unavailable; no PROVENANCE handoff was given.
