# Overnight Realization Round — 2026-08-15

## Acquired ground

The psyche record below governs this round. Later entries supersede earlier entries only where they conflict; questions, candidates, and agent-authored proposals are not rulings.

### Ruled ground

- Every Rust method call lives under a trait. (`psyche/Intent/mandatoryTraits.md`, 2026-08-13)
- Parsing always occurs inside a current context; only that context gives a shape meaning, a met child owns the walk until completion, and the parent then resumes at its saved position. (`psyche/Intent/protosParsing.md`, 2026-08-13)
- Reading and writing are the same structural walk in opposite directions. (`psyche/Intent/protosParsing.md`, 2026-08-13)
- `ShapeDefined` discriminates a standard shape; the matched data-bearing type owns its parsing context. (`psyche/Vision/protosIsTheSharedStyle.md`, 2026-08-12; `psyche/Vision/traitsAsCapabilities.md`, 2026-08-14)
- Shape discrimination occurs at every nesting depth, with child delimiters opaque to the parent and parent position preserved across descent. (`psyche/Vision/protosIsTheSharedStyle.md`, 2026-08-13)
- Protos owns the universal substrate: walk machinery, shapes, `ShapeDefined`, `Head`, `Realize`, `Textualize`, block scanning, and string carriers. (`psyche/Vision/threeStacks.md`, 2026-08-14)
- Datom and Ethos are distinct languages sharing Protos as substrate; Datom is typed data without generics and sits outside the Ethos-to-Rust generation engine. (`psyche/Vision/threeStacks.md`, 2026-08-11; `psyche/Vision/protosIsTheSharedStyle.md`, 2026-08-14; `psyche/Vision/datomSyntax.md`, 2026-08-11)
- The quick-new bootstrap stack is isolated from the legacy, frozen incorrect-new, and terminal correct-new stacks. (`psyche/Vision/threeStacks.md`, 2026-08-13)
- The shortcut daemon is `ethos-monolith`; it compiles Ethos directly to Rust while Nomos and Logos remain outside this bootstrap phase. (`psyche/Vision/threeStacks.md`, 2026-08-14; `psyche/Vision/rustComponentArchitecture.md`, 2026-08-14)
- Signal is the fully typed serialized messaging form; both endpoints know the complete schema. (`psyche/Vision/signalIsOurMessagingLayer.md`, 2026-08-14)
- The serialized form is named Signal, never by rkyv's archive vocabulary, and code/encoded/codec/transcode vocabulary has been dropped. (`psyche/Vision/signalIsOurMessagingLayer.md`, 2026-08-14; `psyche/Vision/encodedFormIsTheCode.md`, 2026-08-13–14)
- Ethos operation names generate Rust types, never runtime labels or self-describing wrappers. (`psyche/Vision/signalIsOurMessagingLayer.md`, 2026-08-14)
- Interface versions begin at `0 1 0`; version 1 is reserved for the first stable release. (`psyche/Vision/signalIsOurMessagingLayer.md`, 2026-08-14)
- Each interface section is a distinct type with its own parsing context; different fields are different things even when their accepted shape tables overlap. (`psyche/Vision/signalIsOurMessagingLayer.md`, 2026-08-14)
- A shape's meaning belongs to its placement; each section field's element type implements `ShapeDefined` and supplies that section's parsing law. (`psyche/Vision/signalIsOurMessagingLayer.md`, 2026-08-14)
- A head followed by a symbol in a variant section is a data-carrying variant whose payload is the named type; a bare symbol is the distinct unit-variant form authorized for this round. (`psyche/Vision/signalIsOurMessagingLayer.md`, 2026-08-14; overnight realization prompt, 2026-08-15)
- Interface roots, especially Input and Output, are branching enumerators carrying typed data. (`psyche/Vision/interfaceRootEnumerators.md`, 2026-08-07)
- Inline struct and enum forms define types rather than instances, but their derived-name scheme is not ruled and is outside this round. (`psyche/Vision/signalIsOurMessagingLayer.md`, 2026-08-14)
- Types are determined first and traits follow; role-capability naming for interface sections remains open. (`psyche/Vision/traitsAsCapabilities.md`, 2026-08-13–14; `psyche/Vision/signalIsOurMessagingLayer.md`, 2026-08-14)
- Traits live on data-bearing types; production free functions and zero-sized behavior namespaces are forbidden. (`psyche/Intent/mandatoryTraits.md`, 2026-08-13; `psyche/Vision/rustComponentArchitecture.md`, 2026-08-08–11)
- `Head` is the official name for the dotted prefix, and variants textualize with their heads. (`psyche/Vision/datomSyntax.md`, 2026-08-14)
- Parentheses are balance-delimited strings; structural symbols are content in string position, and strings that do not require quoting remain bare in canonical text. (`psyche/Vision/datomSyntax.md`, 2026-08-14)
- Generated Rust is committed, and a real consumer must expose lineage/freshness rather than a self-contained imitation. (`psyche/Vision/threeStacks.md`, 2026-08-11)
- Tests must provide observable witnesses, including negative guards; recreating the implementation inside a test is not evidence. (`psyche/Vision/testTravesties.md`, 2026-08-14)
- Every durable test is exposed through a Nix check. (`testing` skill, loaded 2026-08-15)

### Designer defaults, morning review pending

- Fixture operation vocabulary: Input — `Record.Entry`, `Subscribe.Layer`, `Unsubscribe.SubscriptionHandle`; Output — `Recorded.EntryIdentifier`, `Subscribed.SubscriptionHandle`, `Unsubscribed.SubscriptionHandle`; Refusal — `AdmissionRejected.AdmissionRefusal`, `UnknownSubscription.SubscriptionHandle`; Stream — `RecordChange.RecordEvent`. (overnight realization prompt, 2026-08-15)
- `Entry` remains `Entry.{ Layer Description }`; `Description` is a distinct identity-granting Rust type over `String`. (overnight realization prompt, 2026-08-15)
- Variant sections admit exactly head-and-symbol and bare-symbol shapes tonight. (overnight realization prompt, 2026-08-15)
- Generated root enums are role-less tonight: no Input, Output, Refusal, or Stream capability traits. (overnight realization prompt, 2026-08-15)
- All generated output stays inside `ethos-monolith`. (overnight realization prompt, 2026-08-15)

### Open forks not crossed

- The role-capability vocabulary for interface sections remains open; no role traits are generated tonight.
- Inline `.{ ... }` and `.[ ... ]` shorthand, derived payload names, and their naming law remain open and out of scope.
- Generic instantiation, trait-declaration grammar, lowercase bindings, Signal-Psyche, meta-Signal, a new Signal repository, and daemon work remain out of scope.
- The exact future universal-Signal representation, repository name, envelope anatomy, and routing identity remain open.
- Meaning's final type, shape, annotation model, and name remain open; current string behavior is not promoted into that design.
- The exact long-term `Head` representation and any expansion of the universal shape vocabulary beyond what this slice proves remain open.
- `Walk`, `RealizeWalk`, and `TextualizeWalk` naming may still change; this round does not rename them.
- A dialect constant on `Realize`/`Textualize` remains an unruled possibility.
- Shared parsing behavior may be expressed through traits and shared implementations, never by collapsing distinct field or declaration-body types.
- The prior `design/ProtosEngine/psycheEthosFixtureStage2-2026-08-14.md` is proposal evidence only and yields wherever it disagrees with the psyche log or this round's ruled constraints.

