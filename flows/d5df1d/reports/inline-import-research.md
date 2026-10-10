# Inline import `core:Name`: research

Research for d5df1d. Every quote below is verbatim from the named record. Each code fact names the file and line read, or the command run. The research flow's own inferences are marked **Inference**.

## 1. Psyche records

The rule applied: the most recent vision, and vision repeated often, unless something overrides it. Dates are the record's own date. Where a record carries no date, the date given is the day it was logged (from git).

### 1.1 The opening statement (2026-10-09)

`flows/d5df1d/vision/ethos.md` (typed), also kept in `flows/1d0733/vision/ethos.md` (marked STT there, with "Etho" corrected to "[Ethos]"), in `flows/73ada7/vision/nexus.md` (the Nexus half only) and in `flows/f5a6e9/vision/contextModules.md`. The comment was on «The golden ethos», 3rd edition, thread babade, 20:07:

> the file location shouldnt matter from the nexus' pov; it must use a registry which uses the `{ Subaspect.[Vision Knowledge ...] Topic:Name }` to store the location of each, using the containing source with hash (blake3 I believe is what we use?) and relative path of each. those payloads live on the meta signal (to modify those registries). curriculum can have the capacity to get/check the hash when the query come in, according to the operation (write or read).

> Notice I used a new syntax there that I also want to bring into the table of ethos design. I want to talk about how this will be implemented, but I also have more ideas for more ethos improvements.
>
> This is another form where a type can be declared, and it means that we're doing an inline import. If it starts with a capital letter, then it means it's pulling directly from the core built-ins. `name` would be one of the built-ins in the core of the language, which would be declared in the core library. We need a whole registry for all this: all of the manifests for where all the different libraries live.
>
> Otherwise, if it starts with a small letter, then that means it's pulling in from the registry name. This sort of depends on the isos environment that's loaded, right? There's going to be a registry for those as well.
>
> This is a rather big improvement or change in Etho, so I want to make sure it's done well with a full Opus and Fable topic flow on that.

### 1.2 `core:Name`, camelCaseExpression, checked at runtime (2026-10-09)

This one sentence is repeated in four records: `flows/445410/vision/flow.md` (typed, the original), `flows/1d0733/vision/ethos.md`, `flows/9fed42/vision/flow.md` and `flows/f5a6e9/vision/flow.md`. 445410 had written a title as `{ Psyche Core Secondary 445410 }`:

> but technically it should be uncapitalized core and ethos since theyre the core:Name type which is "camelCaseExpression" type with runtime checks when creating a new one

**Overrides** `flows/f5a6e9/vision/flow.md` (2026-10-08, STT):

> The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably.

The change of case from PascalCase to camelCase is overridden. The checker, the dense short expression, and the open "certain number of words" still stand.

Also `flows/f5a6e9/vision/flow.md` (2026-10-09, STT), which shows that `core` is itself a value of this type:

> the topic for the current metaflows that we have that essentially are [topicless] is core.

### 1.3 Case conventions and identifiers (logged 2026-09-15 to 2026-09-26)

`flows/05c604/vision/identifiers.md` (typed, logged 2026-09-15):

> If your typed objects are whatever is Pascal case, I think it is the first capital, right? That would be how we write our symbols for our objects. They're all capitalized, and then camel case could be easily recognized as probably a hash or an idea of some sort.

`flows/692df8/vision/identifiers.md` (typed, logged 2026-09-15):

> What would be a legal symbol, or I don't know, what do we mean by that? An ethos object identifier, right? What we can use as an identifier for an object. What is legal there as a symbol, basically, or what I call a symbol in ethos, something that symbolizes an object, like a data variant or whatever. That would probably live in ethos core or ethos standard, or I guess Signal could have it

`flows/93ba9f/vision/ethosNames.md` (typed, 2026-09-26):

> There are these open-ended variants, which we call names.

`flows/f5a6e9/vision/flow.md` (2026-10-07, STT):

> maybe some kind of short camelcase expression, a string

This was said of a role.

### 1.4 A core library, manifest and registry (2026-10-03)

`flows/9fb0ad/vision/ethosLibrary.md` and `flows/5578cc/vision/identifiers.md` (typed, 2026-10-03):

> This should go into a library that all components can reuse, so maybe some kind of Ethos core library or Ethos standard or something. This might mean needing to develop the way ethos is put together, like manifest, registry, index: where do dependencies, libraries, etc., come from? Let's get Fable to ask me some questions about that and then with the answers he can start on a new flow and design something.

`flows/f5a6e9/vision/ethos.md` (STT, logged 2026-10-07), on `curriculum:[ Name Sha256 ]`:

> I don't see how a [SHA-256] type belongs in the curriculum library.

`flows/e51411/vision/ethos.md` (2026-09-25):

> Maybe the manifest needs to be fleshed out better for compiling and finding dependencies and so on.

`flows/e996e8/vision/archive-ethos.md` (typed, 2026-09-04; archived, and landed in vision-ethos):

> if we version stuff it should be in a manifest of some kind. Lets drop the versionning everywhere for now. I guess any type would need an import section.

### 1.5 The colon import and manifest resolution (2026-08-20 and after)

All from `flows/2b34fafa/vision/importResolution.md` (typed, 2026-08-20), in order:

> signal in signal/domain must be resolved from a manifest (which we must spec obviously), which uses datom. if signal has no entry, it will look in the directory of the document where the import takes place.

The fallback in that statement is **overridden** the same day: "confirmed, kill the fallback." A colon resolves from the manifest or is an error. A bare path is local only.

> actually, I think the syntax should be explicit when pulling an external source.
> `signal-pysche:Object` pulls Object from lib.es in signal-psyche source
> `signal-pysche:[Object Thing]` multiple imports
> `signal-pysche:stream.[Stream Termination]` from stream.es in signal-psyche source

> hmmm. my worry was if the manifest contains signal and the source has a signal module

> I dont think Import is a type; there are no Import's; what exists is an import reference.

`vision-raw/importResolution.md` (2026-08-20):

> if the type needs a 'name' to resove the import, then it's not resolvable.

`vision-raw/importResolution.md` (2026-08-21, from mainFunction.md):

> The manifest should have everything you need. Like maybe we don't have the same idea of a manifest, maybe we need another type, kind of like how the cargo file works, but more specific, where it doesn't have more than one possible output. So it's a kind of an assembly file, if you will.

`flows/2b34fafa/vision/sourceNotCrate.md` (logged 2026-08-22):

> source will be the name we use instead of crate

`flows/752e0f/psyche-block/all.md:2969` (2026-08-07) said "I would rather not create confusion with :". This was **overridden** by the colon for external pulls (2026-08-20). It is archived as colonConfusion.

`flows/b675f3d9/vision/archive-structuralParsing.md:43` (dictated, 2026-08-27):

> If the, uh, colon is used in imports, it doesn't at all keep us from using it in another context. [...] ethos parsing is always dependent on the current context in which the parsing is taking place.

### 1.6 Registries, the meta socket and Curriculum (2026-10-03 to 2026-10-09)

`flows/edf227/vision/contextModules.md` (STT, 2026-10-03):

> Every flow call, or the flow database, has a registry of where each context module is located. [...] the third field would be the location of where it is, either just a local file path for now. Maybe later we can support Git repos and stuff like that. [...] We can make it the meta socket.

The "local file path" part is **overridden** by 1.1 (2026-10-09): file location no longer matters to the Nexus; the entry holds the containing source with its hash and the relative path.

The same file, typed, 2026-10-03:

> It could be a vector with the variant, like vision, and each of the variants contains all of the names of the modules that it wants. Somewhere else in the database, those module names correspond with the path

The same file, typed, 2026-10-03 (also in `flows/5578cc/vision/ethos.md`):

> I don't see `role` as a kind here, and I don't like `kind` because it collides with our use for `kind`, which is more basic.

**Inference:** `Subaspect` in 1.1 names what that registry called `Kind`.

`flows/d4ae97/vision/curriculum.md` (STT, 2026-10-07):

> the curriculum nexus will have its memory registry populated with these registry editing messages, which can contain a vector of new entries and/or a vector of edits (to say that a certain skill has been removed)

The same file, the same day:

> We're going to make this really dirty just so that it works. Right now we're going to use the path of the skill where it is

**Tension, not resolved here:** the 10-07 "dirty first" path stage, against the 10-09 registry keyed by hash and relative path. It is unclear whether 10-09 replaces the stage or is its successor.

`flows/183ae0/notion/datom.md` (Notion, logged 2026-09-29):

> Using paths is very setup-dependent so it's not a very good idea for a system that wants to be correct. [...] you would have the datom file there and next to it would be the compiled signal file so that then the Nexus could load it because it's already signal.

The vision-nexus skill (distilled, part of the base context) says:

> Identity is trait-borne: an encoded form fingerprints itself, by default the hash of its rkyv archive

It also says policy changes only over the meta socket. No hash algorithm is ruled.

### 1.7 Nothing found

- "isos" appears in no record, report or skill except the 1.1 comment and its copies; 1d0733 marks it `[sic]`. **Unknown.**
- No record defines the anatomy of the core library, of a registry entry, or of an isos environment.
- No other record speaks of runtime checks on names.

## 2. The code today

Witnessed in ethos-zero 16.0.0 at `c2653dd`, which equals `origin/main` after a fetch. The binary was built with `cargo build --offline --locked` into the scratchpad.

### 2.1 Imports

- `src/lib.rs:220-236`: `Import::One(Source, Imported)` or `Import::Many(Source, Vec<Imported>)`. `Imported{name, emitted}` allows the `Ethos.Source` rename.
- `src/lib.rs:62-70, 106-138`: `Source` is "a Rust path prefix such as `protos`, `crate` or `std::clone`". It is checked by `syn::parse_str::<syn::Path>`.
- `src/conception.rs:397-415`: an import is a protos `Headed` with `Separator::Colon`.
- `src/checking.rs:31-56`: resolution is file-local. A name resolves to `Resolution::Imported(source, emitted)` from the file's own imports section. There is no manifest or registry in ethos-zero: grep finds only `CARGO_MANIFEST_DIR`. Resolution therefore needs nothing outside the file, and the Rust crate named by the source must already be a Cargo dependency.
- `src/generation.rs:49-55`: the source is emitted as a Rust path, fully qualified, with no `use`.
- `src/lib.rs:418-441, 704-737`: `Intrinsic` is String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self and Sized. These are hard-coded, and `generation.rs:57-75` maps them to `String`, `i64`, `datom_codec::Decimal`, `bool`, `datom_codec::Meaning`, `std::vec::Vec` and so on. **Observation:** vision-ethos lists nine intrinsics. The code adds `Sized`.

### 2.2 Inline sourced references already exist

- `src/lib.rs:238-247`: `Reference { source: Option<Source>, name, arguments }`, with the doc "An inline source qualifying the name: `protos:Error`".
- `src/conception.rs:416-440`: a `Headed` with a colon in a reference position becomes a `Reference` with `source = Some(head)`.
- `src/conception.rs:189-216`: in a struct position, a period means a type declared in place (`Position::Declared`). Any other form is a reference (`Position::Referenced`).
- `checking.rs:1101-1125` checks an inline source only when it is `protos` and the name is a Protos intrinsic. Every other source goes unchecked.
- In use today: `ethos-zero.ethos` writes `Structural.protos:Error` and `ethos_zero:Problem` inline.

### 2.3 What `Name` is today

`src/lib.rs:56-60, 72-84`: `pub struct Name(String)`, built through `TryFrom<&str>`. It accepts `Self` or any text that `syn` parses as a Rust `Ident` and that is not raw (`r#`). `Topic`, `core`, `fooBar`, `snake_case` and `ALLCAPS` all pass. It is the generator's own validated identifier for types, kinds, variants, capabilities and constants, and runs no case check at all. It is not the living's camelCase `core:Name`. A camelCase check would refuse every PascalCase type name ethos-zero handles.

### 2.4 Protos and datom on `a:B` and `a.B`

- protos `src/core.rs:18-22`: `Separator` is Period, Exclamation or Colon.
- protos `src/core.rs:383-497`: in a run, the first `.`, `!` or `:` ends the head, and the rest is the body: `a:B`, `A:B`, `a.B` and `A.B` are all `Headed`. A chain nests (`a:b.C` is `Headed(a, Colon, Headed(b, Period, C))`). A run with an empty segment or a doubled separator stays `Bare`. Protos ignores case entirely.
- datom-codec `src/composition.rs:103-132`: `Headed` with a period becomes `Form::Variant(head, body)`. `Headed` with a colon or exclamation becomes `Form::Bare` of the whole text. In datom, `Topic:Name` is a bare string, and `a.B` is a variant named `a`. datom-codec has no case check.

### 2.5 Is `{ Subaspect.[ Vision Knowledge ] Topic:Name }` parseable today?

Probes ran against the scratchpad build:

| text in a struct | Check | Rust emitted |
|---|---|---|
| `Topic:Name` | Checked | `pub name: Topic::Name` |
| `core:Name` | Checked | `pub name: core::Name` |
| `[ core:Name ]` import + `Topic.Name` | Checked | `pub type Topic = core::Name;` `pub topic: Topic` |
| `Topic.Name`, no import | `Undeclared.Name` | — |
| `Topic:Name` as a type declaration | `Expected.Declaration` | — |

It parses, but means something else: `Topic` is read as a Rust *source path*. The field is named `name`, not `topic`. The Rust would not compile because no `Topic` module exists.

**Collisions:**

1. With the existing inline sourced reference. Under protos, the head of `Topic:Name` is a source. The capital-letter rule must change how the conception reads a colon head.
2. With Rust's `core` crate. `rustc` on `pub type Topic = core::Name;` gives `error[E0425]: cannot find type 'Name' in crate 'core'`. A core library cannot be emitted as `core::`. The source name must be mapped to a real crate path, which is a registry's job.
3. With the kinds section: `create:[ Self ]` (a lowercase head with a colon) means a capability with no self. Context separates them, as ruled 2026-08-27.
4. With import sources today, which are Rust crate names (`signal_flow:[ … ]` in meta-signal-flow; `std:Serializable` in vision-ethos). A registry name and a crate name are not the same thing.
5. In datom, `x:Y` is a bare string, so it cannot appear as a datom head.

Prior code: core-ethos (last touched 2026-10-07; commits from August) carries the commit "resolve catalog-registered builtin vocabulary in bootstrap reader". This is a claim from its git log, not read further. That stage is earlier than Ethos Zero.

## 3. Draft examples, and the questions to rule

**Reading A (Inference, which the coordinator also relayed):** "it" in "if it starts with a capital letter" is the part before the colon. A capitalised head declares a type of that name from a core built-in (`Topic:Name`, a type Topic that is core's Name). A lowercase head is a source name resolved through the loaded environment's registry (`flow:Voice`). `core:Name` is then the lowercase form, with `core` as one registry entry. The 2026-08-20 colon mechanism is kept.

What "inline" adds:
- A capitalised head names and declares a type in the position, where today an import plus `Topic.Name` is needed.
- The source resolves through a registry, not a Rust path.

The sourced reference itself is not new to the generator (2.2).

**Reading B:** the case of the imported name decides. It is weaker, since an ethos type name is never lowercase. It still needs a ruling.

Capitalised, from the core built-ins:

```
Library
[]                         ; imports: none
[ Entry.{ Subaspect.[ Vision      ; a registry key
                      Knowledge ]
          Topic:Name } ]   ; Topic, core's Name
[]                         ; kinds
[]                         ; associations
```

The wrong forms beside it:

```
[ core:Name ]              ; imports: a step
[ Entry.{ Subaspect.[ Vision      ; types
                      Knowledge ]
          Topic.Name } ]   ; Name said twice
```
```
[ Entry.{ topic:Name } ]   ; reads a library
                           ;   named topic
```

Lowercase, from the environment's registry:

```
Signal
[]                         ; imports: none
[ Launch.{ flow:Voice      ; queries: Voice,
           Brief.String } ]  ;   from library flow
[ Launched ]               ; responses
[]                         ; types
```

The wrong forms beside it:

```
[ Launch.{ Flow:Voice } ]  ; declares a type
                           ;   Flow from a core
                           ;   built-in Voice
```
```
[ Launch.{ signal_flow:Voice } ]
                           ; a Rust crate name,
                           ;   not a registry name
```

### The questions to rule

1. **Which part's case decides.** In `Topic:Name`, Reading A (the head) or Reading B (the name)?
2. **What `Topic:Name` declares.** An alias, `pub type Topic = ethos_core::Name;`, which keeps Name's runtime check? Or a new type, `pub struct Topic(ethos_core::Name)`? A new type is a tuple, which is forbidden; the 2026-09-08 record calls a new type `Name.Contained`.
3. **Core built-ins against intrinsics.** If `Name` joins the intrinsics, `Topic.Name` already works. Does `:` earn its place only because core built-ins are not in scope? And does core absorb String, Integer, Vector and the rest, so that intrinsics are core built-ins known without import?
4. **What `core:Name` accepts.** `core`, `ethos` and `flowNexus` pass. Do `Core`, `flow_nexus`, `flow-nexus`, `x9` or `""` pass? Is there a word bound, given "a certain number of words" (10-08)? Is ethos-zero's own `Name` (PascalCase `Topic`, `Self`) a different core type, say `core:Symbol`? See 2.3.
5. **The registry entry.** The key `{ Vision ethos }` maps to what? Something like `{ psyche-skills «blake3…» vision/ethos.md }`? Is the "containing source" a repository, or a Source in the 2026-08-22 sense? Is the hash over the source tree, the commit, or the file? Is blake3 ruled? It is a dependency of content-identity, sema-engine and 11 other LiGoldragon crates, but not of ethos-zero, protos, datom-codec or Curriculum.
6. **One registry or two.** Is the ethos library registry (resolving `flow:`) the same type as the context-module registry (`{ Subaspect Topic }`)? Which Nexus's Memory holds each, given there is no central store? Ethos-zero is not a Nexus: where does it read the registry from? A datom manifest (2026-08-20)? An assembly file (2026-08-21)? The `Generate` request?
7. **What a lookup returns.** For `flow:Voice`: the source location, then the ethos file, then Voice's declaration and arity? And the Rust crate path to emit, such as `signal_flow::Voice`, together with the Cargo dependency it needs?
8. **What the generator emits for core.** `core::` collides with Rust (2.5). Is the emission `ethos_core::Name`? Which crate holds core's Rust?
9. **What the isos environment is.** No record names it.
10. **The meta signal payloads.** Something like `Register.[ … ]`, `Edit.[ … ]`, `Remove.[ … ]`, each a vector, as on 2026-10-07? Does Curriculum's per-operation hash check refuse a read on a mismatch, or report it?
11. **Whether the imports section survives.** A type used twice inline (`flow:Voice` twice) repeats itself. Does the rule "used once inline, more than once named" move it into an imports section?
12. **Whether a declaration can pull from a registry source.** No drafted form declares a capitalised name over a registry source, such as `Speaker:flow:Voice`. Is one wanted?
