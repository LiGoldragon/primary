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

## Outcome

The interface slice and all four architecture guards landed, were pushed to canonical `main`, passed their repository Cargo and Nix gates on the configured remote builder, and passed independent adversarial source audits.

- Protos: `bfea114c96eb548ceae17ab05da9c231a6412ba1`
- Datom: `26a58e0c88d1cf66daa0590ecff0231348be27a2`, pinned to Protos `bfea114c96eb548ceae17ab05da9c231a6412ba1`
- Ethos Monolith: `165183abde6e072715a70b8e5020a2a2ad7b6cec`, version `0.2.0`, pinned to the same Protos revision

All three working copies were clean and their `main`, local Git, and `origin` identities agreed at closeout.

### Protos guards

Protos now exposes the four required durable Nix checks plus an aggregate architecture check:

- `no-production-free-functions`
- `no-production-inherent-methods`
- `no-zst-behavior`
- `no-forbidden-vocabulary`
- `architecture-guards`

The substantial checker lives outside `flake.nix` under `checks/architecture-guards/`. It parses Rust syntax, follows source-module namespaces, aliases, re-exports, glob imports, visibility and path forms, and uses Rust XID boundaries for vocabulary. Good and bad fixtures falsify each rule, and every named check executes its own fixtures as well as the production scan. No universal `HeadAndSymbol` shape was added; placement-specific interface parsing was sufficient.

### Ethos interface slice

The public interface model lives under `ethos_monolith::fixture` and contains `Interface { version, imports, inputs, outputs, refusals, streams, types }`. Imports and all five content sections have distinct carriers and contexts. Root, section, operation, declaration, enum-body, and scalar acceptance all pass through the placement type's `ShapeDefined` implementation before semantic validation.

Realization and textualization close at the top through Protos. Tests prove canonical realize → textualize → equal-realize behavior, both-direction Close→Resume transitions, parent identity and one-position resumption, exact fixture anatomy, rejected forms, and full generated-type consumption.

The committed source and output are:

- `fixtures/psyche/interface.ethos`
- `src/fixture/generated.rs`

The generated module contains the four role-less roots `Input`, `Output`, `Refusal`, and `Stream`, plus distinct `Layer`, `Description`, `EntryIdentifier`, `SubscriptionHandle`, `Entry`, `AdmissionRefusal`, and `RecordEvent` types. `Description` is a newtype over `String`. A real consumer compiles and constructs all root families and declared payload forms. The existing artifact comparison is now trait-borne and makes stale generated Rust fail the registered tests.

Ethos also moved its pre-existing production operations behind data-bearing traits and added a syntax-aware `binding-law` Nix check. Its fixtures cover free functions, inherent methods, behavioral zero-sized layouts including aliases and generic/const/lifetime compositions, macro surfaces, and forbidden vocabulary.

## Landed commits

### Protos

1. `884f9334a658415053da277973df38549b82994a` — add durable architecture guards
2. `ac22e233a56badb6025641feb1f3267702a493ca` — harden architecture guard checks
3. `72cee605fd5b40c879ebd5ee32d1408feaeefc7a` — close remaining lexical guard bypasses
4. `8a056423e4b69011b17c460d2eb7e668c3b04af7` — replace heuristic guards with a Rust AST checker
5. `d7dd22cdfac4b02b4fb7f975271448cadb8bd557` — resolve aliases in zero-sized type guards
6. `c2093363c64b1b7700f4e20768e93554ea0925ad` — harden namespace alias resolution
7. `76dab09a3c087f1295555d340e263ff663e4d609` — close transitive module-alias gaps
8. `b81a911aa865f0f6341e79ba2be6e54aa840ece3` — resolve glob-exported modules
9. `bf7cc7048a44fcb145d42c12dfb6828c415214b7` — normalize restricted-visibility paths
10. `74a8bcfc68f71bcd2541633d3167995c2ad01a12` — share relative-path normalization
11. `bfea114c96eb548ceae17ab05da9c231a6412ba1` — resolve grouped bare-`self` imports

### Datom

1. `1feacc56fb4c8656e5e306b314c7137b29e38e68` — update Protos dependency revision
2. `306aa88145e7b4bb9cd35a02a6f4266a4eaad63d` — advance Protos dependency revision
3. `c3d63786427af615b2914a5817d949855d5c42a1` — pin the then-final guard revision
4. `4117654bdfbc6fa81e27665932227ff887c42ac7` — converge the dependency revision
5. `4bad19fb66a3d7adbff44aaef9f17c56bf0a2c25` — converge the alias-aware revision
6. `26a58e0c88d1cf66daa0590ecff0231348be27a2` — converge the independently accepted revision

### Ethos Monolith

1. `213e51e5d4a4ef9de1e6e7af5b76577e2fa85076` — realize and project the psyche Interface fixture
2. `3ada81dd90678825aad6faaca4bec408f1b5f6c3` — reject lowercase declared type heads
3. `f0f2509ae420bcb88154ca11b9d9ec14de1de6ce` — validate declaration symbols
4. `e10e69af2fb5318fec276d74000787090901fa90` — witness complete Protos transitions
5. `f804d2572a093e36ede02cc0f19d4105fe9c634f` — preserve Ethos fixture sources in Nix checks
6. `f245a793792a30e5230c19259cc39342f23baa30` — move production operations behind traits
7. `5b3a2b0d65d2316c853eb9f6ce154e3d8f78ed70` — enforce shape selection and two-way walk evidence
8. `e48fe4960ba624cdfc81d6a63957aad2221b9b64` — add the binding-law Nix guard
9. `4e4609136f69320984105271143fe3ffbbb7c6b4` — correct the first guard expressions
10. `8102b1469d4bdc984fdfb468a6c06b8d00f16aa4` — replace heuristic binding checks with AST checks
11. `1cb4c094bc9266f632138f27d61967dc540cc6e9` — reuse Cargo artifacts for the binding-law check
12. `71f0d3a63ed21d72fd6872d61e306e1a703776a1` — converge on the canonical Protos revision
13. `b1cac92ab01c6b824280378a0ddaf1ec91f645b7` — converge on the alias-aware Protos revision
14. `1cadb26608d5f0067ea34174bdf828d8a641fdcd` — converge on the accepted Protos revision
15. `5fd0da0d2664dee94de7d113447702d0961c785e` — guard namespace layouts and macro surfaces
16. `88b40369aca72ce737f7d905e1a2ff55f218549e` — complete generic zero-sized layout analysis
17. `30acc3577be334bf4929a9c000d36fcf95ecc048` — complete generic substitution and nested-item guards
18. `8d4a41c65e7acc2fe957ea92ac311a5a5166a3e9` — extend the guard for const and lifetime generics
19. `d1f6c74d8566af39e0571b2d8214315b0210eefe` — resolve const expressions in array-layout guards
20. `165183abde6e072715a70b8e5020a2a2ad7b6cec` — bump `ethos_monolith` to `0.2.0`

## Self-made decisions

- Kept head-and-symbol placement-specific instead of expanding universal `protos::Shape`; the section carrier splits a bare dotted symbol after `ShapeDefined` discrimination.
- Put the vertical slice in a dedicated `fixture` module and committed its generated Rust beside its real consumer.
- Kept Ethos directly dependent on Protos only; Datom is a separately proven dialect consumer, not an Ethos product or build dependency.
- Used `String` for the `String` scalar and `i64` for `Integer`; every typedef remains a distinct newtype.
- Made generated tuple payloads and struct fields public so the compiled fixture consumer can construct and destructure the actual boundary types.
- Lowercased only the first ASCII character when projecting declared struct field type names into Rust field identifiers.
- Canonical Ethos text is structural, space-separated, and has no trailing newline.
- Kept the Interface wire version at `0 1 0`; bumped the Rust crate to `0.2.0` because the round added a substantial public API.
- Used syntax-aware checks rather than lexical regular expressions once adversarial fixtures demonstrated that formatting, aliases, namespaces, Unicode boundaries, and generic layout affect the law.
- In Ethos, unknown array lengths are conservatively treated as potentially zero-sized unless they can be proven nonzero; this prevents layout-dependent behavior namespaces from evading the guard.
- Ethos rejects item-producing macro/include surfaces and foreign free-function declarations in production; its current implementation uses neither.

## Verification

- Protos: Cargo format, workspace tests, Clippy, docs, direct aggregate and four individual guard runs, Nix evaluation, and all 10 remote flake checks passed. An independent critical audit returned PASS with no in-scope source-AST bypass.
- Datom: seven tests and all 15 remote flake checks passed against the final pushed Protos revision.
- Ethos Monolith: Cargo format/check/all-target tests/Clippy/docs, direct architecture and interface fixtures, Nix evaluation, and all eight remote flake checks passed. An independent critical audit returned PASS after adversarial namespace, generic-layout, const-expression, macro-surface, exact-interface, generated-consumer, and freshness review.

## Stopped forks and morning questions

- Should the Protos architecture guard inspect expanded macro and `include!` output, or should item-producing macro surfaces be forbidden or allowlisted as Ethos does? Protos production contains no relevant macro/include surface, so the round did not choose a universal policy.
- Do foreign declarations count as forbidden production free functions for the universal Protos guard? Protos production contains none. Ethos conservatively rejects them locally; no universal ruling is claimed.
- Role-capability names, inline shorthand and derived-name law, trait/generic grammar, universal Signal anatomy/repository/routing, Meaning, long-term `Head`, walk-trait naming, and a dialect constant remain exactly as listed in the acquired-ground open forks; none was crossed.
