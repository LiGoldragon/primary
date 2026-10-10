# Psyche inventory — Protos family topics

Origin marks: **[read]** = I read the file myself in this thread. **[sub]** = relayed from a subagent audit, path/line cited, not re-verified by me except where noted. **[inferred]** = my reading, not the living's words.

Dates in §1–2 are the psyche entry dates carried in the text. Git dates for files under `flows/` and `vision-raw/` are mostly 2026-09-01 (a repository reorganisation) and are **not** evidence of when the living spoke — I note them only where they are the file's real last touch. **[read]**

---

## 1. Vision/ and Intent/ on these topics

Everything in `Vision/` and `Intent/` is approved by definition — a statement lands only on the living's explicit approval (psyche-distillation skill). No Vision file carries per-statement approval markers; only `Intent/mandatoryTraits.md` and `Intent/protosParsing.md` and `Intent/data.md` carry their approval quote inline. **[read]**

| File | Statements (headings) | Last change |
|---|---|---|
| `/home/li/primary/Vision/datom.md` | Name; Nature; A datom is a form at a path; Strings; Syntax; The datom composes, the type states its positions; Any Rust type; From text and back; Containers; Errors; Omittable fields; The interface shape; De/serialization; Relation to Ethos; Repository; Map; Meaning | 2026-09-11 |
| `/home/li/primary/Vision/protos.md` | What Protos is; What Protos knows; Layers; Every layer carries its own context; Kinds are borne by the type converted and named for the layer it becomes; Signal is parallel; Delimiters; Structure; String, escape, error; Multi-pass; Canonical print | 2026-09-09 |
| `/home/li/primary/Vision/ethos.md` | What Ethos is; Why Ethos; Roots; Non-repetition; Self-description; Horizon; Kind; Naming; Identity; Declaration: File; Imports; What a declaration turns into; Inline types; A variant named as a defined type carries that type; A variant may declare its payload inline; Every declared type bears both kinds; The datom kinds are compiled in only where text is spoken; Shapes and placement; Kinds are explicit, bodies are hand-written; Kind syntax; Associations; Spacing; Zero; Generation | 2026-09-11 |
| `/home/li/primary/Vision/sema.md` | What sema is | 2026-09-09 |
| `/home/li/primary/Vision/signal.md` | Name; What signal is; Query and response; Text and signal; Meta signal; Protocol | 2026-09-10 |
| `/home/li/primary/Vision/nexus.md` | A Nexus is the whole; A kind of thing; Library and daemon; Universal traits first; Processing is for the effect; Documents; Sockets; Default clients; Signal only; The graph; Routing; Configuration; First configuration; Repositories; Why everything is a Nexus; Actors; Splitting a Nexus; Observation by subscription; Polling is forbidden | 2026-09-11 |
| `/home/li/primary/Vision/orchestrate.md` | Deployment; The skill | 2026-08-27 |
| `/home/li/primary/Vision/highLevelView.md` | The very high-level view is looked at routinely; A view takes room | 2026-08-27 |
| `/home/li/primary/Vision/flowNexus.md` | What it does; Starting flows; Repository and skills | 2026-09-09 |
| `/home/li/primary/Vision/archive-ethosMonolith.md` | (retired 2026-09-10 into Vision/ethos.md "Zero") | 2026-09-10 |
| `/home/li/primary/Intent/anatomy.md` | Code is written anatomically | 2026-09-09 |
| `/home/li/primary/Intent/context.md` | Every layer carries its own context | 2026-09-09 |
| `/home/li/primary/Intent/conversion.md` | A kind names one conversion | 2026-09-09 |
| `/home/li/primary/Intent/data.md` | (single body) Everything is data — approval quoted: *"make that intent, not spirit"*, 2026-09-02 | 2026-09-01 |
| `/home/li/primary/Intent/mandatoryTraits.md` | 2026-08-13 — approved; approval quoted: *"otherwise its good, implement commit and deploy."* | 2026-09-01 |
| `/home/li/primary/Intent/protosParsing.md` | (single body) Protos parsing; approval quoted: *"the intent is good"*, 2026-08-13T00:19+02:00 | 2026-09-01 |

**Topics with no Vision file at all**: Ethos Zero (carried inside `Vision/ethos.md` "Zero"), code-is-language, parser-is-the-parser, rust component architecture, traits-as-capabilities (only via `Intent/mandatoryTraits.md`), generic parameters, newtype wrapping / single-field structs, colon-form transformer syntax (carried inside `Vision/datom.md` Syntax), structured string (carried inside `Vision/datom.md` Meaning). **[read]**

---

## 2. Raw sources — what is distilled, superseded, or still undistilled

### 2a. Already distilled (archived, and cited in `Vision/sources/`)

`Vision/sources/*.md` names 150-odd raw records across `datom`, `protos`, `ethos`, `nexus`, `signal`, `sema`, `flowNexus`, `orchestrate`, `highLevelView`, `distillation`, `remembering`. I checked every line against the filesystem: all resolve to an `archive-` file except four. **[read]**

**Hygiene gap — four records cited as sources but never archived:**

```
flows/fe34eb/vision/datom.md    (cited in Vision/sources/datom.md)
flows/fe34eb/vision/ethos.md    (cited in Vision/sources/ethos.md)
flows/fe34eb/vision/nexus.md    (cited in Vision/sources/nexus.md)
flows/fe34eb/vision/signal.md   (cited in Vision/sources/signal.md)
```

I read all four; their content **is** carried in Vision (e.g. Vision/datom.md:240 carries "Horizon, Lojix"; Vision/nexus.md:5 carries the reconciled daemon wording the living approved with *"yes, good"*). They are distilled, they just still sit raw. **[read]**

**Second hygiene gap**: `Vision/sema.md` states *"it matters more than nexus, because operational editing should yield the migration with the edit."* Its raw support is `vision-raw/archive-rustComponentArchitecture.md:71-73,145`, which is **not** listed in `Vision/sources/sema.md`. **[read]**

**Third gap — a source archived as a title-only stub, the words lost**: `vision-raw/archive-highLevelView.md` reads in full:

```
# High-level view — archived

## I think the biggest lesson from this is that we need to routinely look at the very high-level view of what we're building

(title-only record; no body text)
```

`flows/b675f3d9/vision/highLevelView.md` (the other cited source) is likewise a bare heading. The living's actual words survive only in `flows/55d18f4f/vision/highLevelView.md`, which is **not** cited as a source and **not** archived. Consequently `Vision/highLevelView.md`'s second statement — "A high-level view takes room and breaks everything down in-line." — has **no surviving raw support anywhere in the corpus**. **[read]**

### 2b. Drained shells (topic named, no psyche words left)

These `vision-raw/` files hold a heading and nothing else. Their entries were split out to per-flow files and archived there. They can be deleted. **[read]**

- `/home/li/primary/vision-raw/codeIsLanguage.md` — `# Code is language`, nothing more. **The topic "code-is-language" has no psyche words anywhere in the corpus** (grepped `Vision/`, `Intent/`, `vision-raw/`, `flows/*/vision/`, `flows/*/notion/` for "code is language", "language is code"; one hit, this heading).
- `/home/li/primary/vision-raw/highLevelView.md`
- `/home/li/primary/vision-raw/protosIsTheSharedStyle.md`
- `/home/li/primary/vision-raw/newtypeWrappingAndSingleFieldStructs.md`
- `/home/li/primary/vision-raw/structuredStringType.md` — holds only a 2026-08-14 agent-authored cross-reference annotation, no psyche words.

### 2c. Still undistilled — `vision-raw/` (legacy)

**`/home/li/primary/vision-raw/parserIsTheParser.md`** — 2026-08-11, steward session. No archive counterpart, cited in no sources file. Fully undistilled; nothing in Vision on this.

> "assembly.rs reimplements its own parser, which is forbidden.
> the parser is the parser, nothing implements its own parsing logic."

**`/home/li/primary/vision-raw/genericParametersAreTraits.md`** — 2026-08-01. Partly carried by `Vision/ethos.md:48` ("In ethos there are no generics, only kinds"), but the *"rust is assembly"* clause and the multiple-trait-adjusts-emitted-Rust clause are not.

> youre right; and the answer is the mandatory trait! so T would be a trait!
> and multiple trait in the declaration would just adjust the emitted rust -
> remember for us rust is assembly

**`/home/li/primary/vision-raw/traitsAsCapabilities.md`** — 2026-08-20, session `2b34fafa`. Sibling archives exist (`flows/06196cc7`, `flows/2b34fafa`, `flows/6863ef19`), this entry is not among them. Nothing in Vision carries it.

> "You misunderstood the trait based approach. your trait methods are
> just regular functions pretending to be traits. if the type needs a
> 'name' to resove the import, then it's not resolvable. So we found
> one of the cornerstone of models not understand my vision. Do a
> research in this"

**`/home/li/primary/vision-raw/rustComponentArchitecture.md`** — 2026-08-18, session `2b34fafa`.

> "grep isnt the right way to do this testing anyway; there are much
> better tools to analyze code than grep nowadays"

**`/home/li/primary/vision-raw/signalIsOurMessagingLayer.md`** — 2026-08-14T20:17+02:00, session `ba906ae2`. Explicitly floated, not ruled.

> why not Input Output Refuse, like Write and Read?

> but actually, it might be better to have a shared Process trait?

> because input.input() is a bit weird? input.process() feels more
> appropriate. but process is overloaded. lets look at some word
> choices

> we need to clarify the skill. get the miner to dig in the old
> skill set (we have a file somewhere with that)

**`/home/li/primary/vision-raw/colonFormTransformerSyntax.md`** — 2026-08-06T17:25:39Z, session `5abf3be8`. **Superseded** by `flows/a5587095/vision/archive-colonFormTransformerSyntax.md` (2026-08-11, `.[` / `.{` payloads, parentheses freed), which is distilled into `Vision/datom.md` Syntax. The residue can be archived with it.

> unrelated first. I think Name:TransformerName.( ... ) is the better
> syntax for named transformers. The other syntax will create
> difficult parsing and reasoning. Do you agree?

**`/home/li/primary/vision-raw/assembly.md`**, **`/home/li/primary/vision-raw/mainFunction.md`**, **`/home/li/primary/vision-raw/importResolution.md`**, **`/home/li/primary/vision-raw/machineAnatomy.md`** — large 2026-08-21/22 dictations on the program's shape (registry + assembly file, ResolvedAssembly, `From` over `Into`, the 3-part machine, AssembledRust). None of this reaches any `Vision/` file. Too long to quote whole here; each file's `##` headings and quotes are intact at those paths. The internal supersessions are already recorded inside them (Create trait → *"it would just be TryFrom, not create, so theres nothing to make."*; four-part → *"agglomerate multiple types -> create a coherent type -> convert it to another type"*).

**`/home/li/primary/vision-raw/itsATranslator.md`** — 2026-08-08T11:48:31.390Z.

> right now, I dont really give a fuck what anything is built as. Im 100% in vision description mode. Consider all the implementation half garbage for now.

### 2d. Still undistilled — `flows/*/vision/` and `flows/*/notion/`

**Datom / kinds / layers — flow `04db2fd2`**, all three uncited in any sources file:

`/home/li/primary/flows/04db2fd2/vision/delineate.md`
> Re Delineate: Yes! That's what I was looking for. So a Prospective&lt;Datom&gt; is Delineatable (however this is spelled, or however you think we could word that kind)

> delineation is protos.

`/home/li/primary/flows/04db2fd2/vision/decomposable.md`
> here's a kind. A kind decomposable. ... if something is decomposable, it's decomposable into composable kinds. And then we get the reverse behavior, where if all of the composing parts, the composable parts of a decomposable kind, are put together in the right order, then we can re-obtain... We can regenerate the actual instance of this decomposable kind from the composable parts.

(the second entry, "Maybe not decompose/compose but finding the keyframes", is at the same path and reads as the living turning the idea over, not ruling)

`/home/li/primary/flows/04db2fd2/vision/softwareAnatomySkill.md` — the two entries direct a skill on software/nexus anatomy. None of `Delineatable`, `Decomposable`, `Prospective`, `Composable` appears anywhere in `Vision/` or `Intent/` (grepped). **[read]**

**Kinds / concept / contexts / Rust — flow `995a164e`**, 2026-08-30/31 artifact comments, none cited in sources:

`/home/li/primary/flows/995a164e/vision/rust.md`
> 2. You've used an implementation block that is not implementing a trait, and that is forbidden. We forbid freestanding implementations. All implementations must be of a trait.

> I really despise free functions, and I despise these inlined lambdas even more. Whenever I see that, to me, that smells of bullshit and ugly design.

(The fully-qualified-generated-Rust entry in the same file **is** carried, at `Vision/ethos.md:144-145`.)

`/home/li/primary/flows/995a164e/vision/kinds.md` — three entries, all open questions the living posed: `name could perhaps be a capability of Conceptual`; *"What's an associated kind? Russ doesn't have associated traits, so did you mean associated types?"* / *"Why values? What's wrong with constants?"*; and the Protoformed naming problem:
> I think we need different terms here because the adjective "protoformed" is difficult to distinguish in speech from the noun "protoform". Maybe the kind is "protosic" or "protoformal", or maybe something else.

`/home/li/primary/flows/995a164e/vision/contexts.md`, `/home/li/primary/flows/995a164e/vision/concept.md`, `/home/li/primary/flows/995a164e/vision/explodedForm.md`, `/home/li/primary/flows/995a164e/vision/layerMatching.md` — likewise undistilled. `explodedForm.md` is an open naming request:
> We should have a name explicitly for this form where the ethos text can appear. I was thinking "exploded form," but it sounds a bit violent, although it kind of works. I would like you to offer some alternatives as well on how we could name that.

`/home/li/primary/flows/62022e8f/notion/layerMatching.md` — the largest single undistilled body on this topic, and the living marked it a notion himself: *"this is sort of a notion that we need to crystallize before it really becomes a vision. So brainstorm with me on this and on the terminology as well."* Four entries: the embodiments and the single enumerator, the roster match on context + structure, the compile-time no-conflict check and multi-form going up, and the ethos roster. **Notion level — must not be built on.** **[read]**

`/home/li/primary/flows/62022e8f/vision/multiFormConcepts.md` — vision, not notion, and not in `Vision/`:
> You would have this multi-form concept where it's struct with a different number of a different arity. It would just be the same concept, but some of the fields can be omitted depending on which arity is being used. That way, we have a simple form and a complex form without having to always write out all the fields, even if they're empty.

**Single-field structs / newtypes — flow `8e9e77`**, 2026-09-08, uncited:
> Also, there's another recent flow which you might want to look into, where we talked about single-field structs, which are an aberration and which we need to sort of train against, or possibly even refuse. I think we should possibly even refuse single-field struct types and ethos, and instruct against them even in Rust, because those should be new types.

> Which, as I was talking in the other flow, is something that I want to make illegal now because it's absurd. This should be a new type and not a struct with just a single element in it.
>
> Then the implementation is wrong because a new type should be just the name of the type and then the separator, which is a period, and then the name of the contained type. If it's an inline type declaration, then it's just that: a type declaration. Never mind that. That's what it is. It would be absurd to make a new type that contains another complex type. A new type generally is like `name.string`, `age.integer`, or whatever we use: `int`.

`Vision/ethos.md:421-422` rules only on tuples, not on single-field structs. This is the freshest and sharpest undistilled ruling in the set. **[read]**

**Tuples — `/home/li/primary/flows/cff271af/vision/tuples.md`**, 2026-08-22, six entries, most explicitly unruled; the one ruling:
> the newtype is allowed. the fact that its a tuple is unfortunate
> for us, so it would have to be mentionned in case.
>
> > A multi-field tuple struct, struct Pair(A, B), also passes the
> > rule's letter
>
> do we have to allow those? I really dont like tuples, they're a
> form of un-specification

`Vision/ethos.md:421` carries the tuple rule but not the newtype-is-allowed-and-must-be-mentioned clause. **[read]**

**Arity and meta CLI — flow `f6db8d`, 2026-09-12** (the most recent psyche words in this whole set), uncited and unarchived:

`/home/li/primary/flows/f6db8d/vision/arity.md`
> reintroduce arity where it makes most sense (sounds like it should be in compositional).

`/home/li/primary/flows/f6db8d/vision/metaCli.md`
> meta cli names is &lt;component&gt;-meta.

**Datom value layer — flow `564f55`, 2026-09-09** — resolved in place by the living:
`/home/li/primary/flows/564f55/vision/datom.md` holds the value-layer entries and then this, which supersedes them as vision:
> Well, I'm not sure anymore about the value layer. None of what I was saying about the value layer was vision. It was a notion. I was brainstorming with you, so none of what I said about the value layer has any authority in the vision. I think you have a hard time differentiating. I guess I should be more explicit when I'm bouncing ideas with you and when I'm actually making pronouncements. I was not making pronouncements. I was trying to brainstorm the code with you.

The words are held at `/home/li/primary/flows/564f55/notion/datom.md`. The composed/composable entry there is notion.

**Ethos strings — flow `564f55`, 2026-09-08** — same self-correction:
`/home/li/primary/flows/564f55/vision/ethos.md`
> "ethos isnt about strings" is bad vision. youre confusing something I said to help you understand vision with vision

The first entry in that file (nomos and logos as layers of a fuller programming language) is thereby disqualified as vision. **Note**: `Vision/ethos.md:8-14` ("Why Ethos") and `Vision/protos.md:8-12` (nomos/logos in the multi-pass engine) still stand on other sources. **[read]**

**Design practice — `/home/li/primary/flows/564f55/vision/designPractice.md`, 2026-09-08** — governs distillation itself, already partly encoded in the psyche-distillation skill's "A statement about code carries the code":
> Machines think in code, and I don't know why you would talk to a machine about code without giving him the code.

> The code they don't know is Ethos and datom, what this Ethos should turn into in Rust, and how to use datom in Rust.

`/home/li/primary/flows/62022e8f/vision/distilledVision.md` (undistilled) carries the same direction at length, plus a second ruling not in any skill:
> And it would make it obvious whenever if I said something that contradicted that, that we need to change the vision. And then we could sort of, we don't necessarily always have to work on raw vision when I speak. If what I'm talking about is something in the distilled vision, like obviously you can log what I say, but then you can also just apply what I say directly to the distilled vision, if you understand what I'm saying.

`/home/li/primary/flows/e8c4cc61/vision/designExamples.md` (undistilled):
> lock is an extremely poor example when we are designing ethos. why not do the structure of an ethos Library and an ethos Signal Request?

This one is directly violated by the current skills — `skills/ethos.md` and `skills/datom.md` both use Lock as the worked example throughout. **[read]**

**Rust component architecture — five flows, none distilled into any Vision file.** `Intent/mandatoryTraits.md` carries the 2026-08-13 approved wording; everything after it is raw:
- `/home/li/primary/flows/e4be1c4a/vision/rustComponentArchitecture.md` — 2026-08-16 *"if it implements any other related trait, we have a trait design training problem"*; 2026-08-17 *"the problem isnt that it only has one implementor, but that many of those traits should be one."*
- `/home/li/primary/flows/a5587095/vision/rustComponentArchitecture.md` — 2026-08-11 *"all method calls in our rust code to be part of a trait … rust is the new assembly language"* (this one **is** carried, in `Intent/mandatoryTraits.md`); 2026-08-11 *"traits constrain the implementers to think in a certain way"*; 2026-08-12 *"on a greenfield we wouldnt extract; a new need would require a new trait"* — the last two are not.
- `/home/li/primary/flows/2b34fafa/vision/rustComponentArchitecture.md` — 2026-08-18, four entries against the architecture guard: *"thats so stupid. I want to get rid of that, and train against this level of expert foolishness."*; *"Using mechanical tests isnt going to create good ontology; trait/types design is ontology in code."*; *"its stupid because it writes a tool for this single repo, instead of a universal tool being created to test this for any repo"*; *"Do an othological study of the code, and create the most unified map of traits and types you can."*
- `/home/li/primary/flows/e06e4c07/vision/rustComponentArchitecture.md` — 2026-08-19; the Nexus half **is** distilled into `Vision/nexus.md`, the ontology-training half is not.
- `/home/li/primary/flows/2b34fafa/vision/importResolution.md` — 2026-08-20, five entries on the colon import syntax. `Vision/ethos.md:130-145` carries `protos:String` and the fully-qualified rule; it does **not** carry the manifest resolution, `lib.es`, the `.es` extension, *"confirmed, kill the fallback."*, or *"I dont think Import is a type; there are no Import's; what exists is an import reference."*

**Nexus / signal / actors — `/home/li/primary/flows/fd301d9a/vision/actorLibrary.md`** (undistilled; sources cite `15b67974 actorLibrary`, a different, archived record): *"we are definitely using kameo actors in nexus. I just havent designed the standards of use"* — this **is** carried at `Vision/nexus.md:107-110`. The rest (distrust the fork, no Arc mutex ban, hexis not trusted, persona-spirit abandoned) is not.

`/home/li/primary/flows/98fbfa47/vision/shortHeaderNotNow.md` — 2026-08-09, a deliberate deferral not carried anywhere:
> Yeah, the signal header idea, the short header, is a great idea, but
> it's quite low level, and right now we don't need to really... I
> feel like if I let agents implement it, it's going to be kind of
> useless, because they don't really understand what I want to do with
> it and what's possible with it, and it would take me too much effort
> to explain that one small part, and the benefits aren't great
> enough.

`/home/li/primary/flows/6863ef19/vision/theBestShape.md` — 2026-08-13, flagged by the living as possibly Intent (*"Maybe there's some intent in here"*), never graduated:
> If we see from a high level here, if we express things properly,
> we will minimize the amount of code. The minimum amount of code
> for the most elegant machinery, which can be easily understood by
> an engineer and easily extended and easily introspected, is the
> best shape.

`/home/li/primary/flows/6863ef19/vision/signalIsOurMessagingLayer.md` — 2026-08-13 *"routable signal then"*. Not in `Vision/signal.md`.

`/home/li/primary/flows/bc05da32/vision/mainFunction.md` — 2026-08-22. The horizon half **is** carried at `Vision/ethos.md:37-41`; the macro entry is not.

**Ethos interfaces — `/home/li/primary/flows/01a02fd5/vision/interfaces.md`**, 2026-08-24, four entries, the last two superseding the first two:
> we'll just say ethos, which will motivate everyone to get ethos working.

Not carried in `Vision/ethos.md` or `Vision/signal.md`. **[read]**

---

## 3. Same-time conflicts and entries sitting oddly

**A live contradiction inside approved Vision itself.** `Vision/orchestrate.md:6-7` (2026-08-27):

> Orchestrate is deployed unconditionally, in the home, for every user. Its meta binary is part of it; a deployment without **meta-orchestrate** is wrong.

against `Vision/nexus.md:48-49` (2026-09-11):

> The meta CLI is named **component-meta**.

and the living's typed ruling of 2026-09-12, `/home/li/primary/flows/f6db8d/vision/metaCli.md`:

> meta cli names is &lt;component&gt;-meta.

Two approved statements name the same binary two ways. The later ruling settles it; `Vision/orchestrate.md` was never corrected. **[read]**

**The ARITY reversal.** `Vision/protos.md:85` and `Vision/datom.md:120,141` put `const ARITY: Integer` on `Compositional`. The shipped `datom-codec` 0.26.x removed it, and the living ruled on 2026-09-12 that it be reintroduced. `skills/datom.md:43` encodes the removal. Three surfaces, two of them against the living's word. **[read]** + **[sub]**

**Entries sitting oddly against the larger direction:**

`/home/li/primary/flows/fe34eb/vision/nexus.md`, 2026-09-10 — the living asking, not ruling, and the record correctly marks it so:
> 4. I want to discuss nexus actually. am I overcomplicating things? the idea was to expose the types used in core of the program (in ethos)

and, same day:
> I think I was overthinking the whole "nexus-core" runtime concept. As you said, signal defines the requests and the replies, and that sort of gives us all of the main types that we want to be concerned with, other than the database types, which would be the sema types.

A moment of retreat logged as vision, later the same day as a firm ruling (*"a nexus is a daemon. every component we will build will be a nexus."*). `Vision/nexus.md` carried the firm one forward. **[read]** I flag it because the second quote reads as the living doubting the Nexus root, and `Vision/nexus.md` does not record that doubt. **[inferred]**

`/home/li/primary/flows/995a164e/vision/contexts.md` — the living refusing the flow's whole Context enum:
> I'm not sure I vibe with all of these ... I think we need to look at what this looks like in practice when it's applied to an actual engine to better understand what we're trying to do here, because some of it feels unnecessary.

against `Intent/protosParsing.md`, which is approved Intent resting on context as the ruling mechanism. Not a contradiction — the Intent is about parsing-in-context, the comment is about enumerating context *values* — but a flow reading only the Intent would build the enum the living rejected. **[inferred]**

`/home/li/primary/flows/2b34fafa/vision/importResolution.md` records its own tension, agent-authored:
> Tension noted for review: 2026-08-07 moved imports off `:` ("I would rather not create confusion with :"); placement law may resolve it — question posed to the psyche.

`Vision/ethos.md:130` now uses the colon for imports and `Vision/protos.md:118` lists colon among the three head separators. The tension was never put to the living; Vision simply chose. **[read]**

---

## 4. The three skills

Skill sources: `/git/github.com/LiGoldragon/Curriculum/skills/{protos,datom,ethos}.md`, all last changed **2026-09-12**, commit `2ef2b53` "Apply the approved skill proposals from flow f6db8d". `roles.datom` (2026-09-10) names none of the three; `ARCHITECTURE.md` and `README.md` mention Datom only as the format of `roles.datom`. `AGENTS.md:3` — "Curriculum owns only `skills/*.md`, `roles.datom`, and repository documentation." **[read]**

I verified two findings myself; the rest is relayed.

### 4a. protos **[sub]**

Unsupported by any Vision or raw entry:
- `:6` "It owns the only character reader and the only character writer." — nothing in the corpus; nearest is `Vision/protos.md:6-7` on *shareability*.
- `:57` the `constraints: Option<Box<Protos>>` field on `Headed` — contradicts `Vision/protos.md:116-119` and `flows/04db2fd2/vision/archive-anatomy.md:19` ("*So the headed object is a struct with three parts.*"), and contradicts the skill's own prose at `:35`.
- `:71` `pub trait Canonicalizable` — zero hits for "canonicaliz" outside the skill; also breaks `Intent/conversion.md:5` (a kind names one conversion) since it converts nothing.
- `:67` `ReaderBudget { remaining: usize }` — Vision's type is `Budget` (`Vision/protos.md:83`, `Vision/datom.md:114`); the declared type is never used in the skill.
- `:66` `Error { extent, problem: Problem }` — `Problem` appears nowhere, and the `extent` field reinstates exactly the situated pair `Vision/protos.md:59-61` abolishes.
- `:63` `enum Boundary { Guillemets, Parentheses }` — against `flows/564f55/vision/archive-protos.md:33` "*() isnt opaque; its still unspecified, so treated as opaque until it get specified.*"
- `:86` "comments are not printed" and "to end of line" and "`Head.body` with nothing around the separator" — none stated anywhere.
- `:10` "a single pass is not an option" — Vision's words are "Multiple passes are wanted over a single pass" (`Vision/protos.md:138`).

Approved statements dropped or contradicted: the whole of `Intent/protosParsing.md` (the context-switching parse is named once at `:6` and never explained — the largest omission); `Intent/anatomy.md`; `Intent/conversion.md:5`; `Vision/protos.md:8-12` (Datom's place, the protos engine); `:90-94` (Signal is parallel); `:49-52` (the context principle); `:137-143` (the multi-pass rationale); `:18-23` (a head is anatomy not interpretation; protos examples are non-dialect-specific — which the skill's own `Datom` examples violate); `:78-85` (four of seven kind signatures, so `ARITY`, `from_positions`, `Positions`, and budget threading are all lost); `Path::root()` → `Path::new()` at `:73`.

### 4b. datom **[sub]**, ARITY item verified **[read]**

Unsupported:
- `:19` "A decimal is finite and point-mandatory." — the only psyche words are a *question* (`flows/4decf7/vision/archive-datomSyntax.md:15`). Three prior flow reports already flagged this as invented; `flows/f6db8d/reports/skill-proposals.md:612` kept it on the false ground that it is in `Vision/datom.md`. It is not.
- `:44` `type Output` on `Datomizable` — Vision's signature is monomorphic (`Vision/datom.md:145`, `Vision/protos.md:84`).
- `:57` `budget.spend(&datom.path)?` with a comment claiming to ask the type's arity while the arity is hardcoded `2` on the next line.
- `:83` `Value.{ Integer x }` — Vision's form is `Corporate.{ [ 1 ] Value.x }` (`Vision/datom.md:179`).
- `:74` `Path::new()` — same drift as protos.
- `:91-92` the orchestrate Lock example — matches the shipped tool, not any psyche record, and diverges from `Vision/signal.md:22-27`.

Contradictions: **`Compositional` loses `const ARITY`** (`:43`, `:58`) against `Vision/datom.md:141`, `Vision/protos.md:85`, and the living's 2026-09-12 word; `Composable`'s body and its arity check are dropped (`Vision/datom.md:118-123`); the potential no longer owns the budget (`:73` vs `Vision/datom.md:152-153`).

Dropped: the whole Name section (including "Datomic … is not a term of the code", a live naming hazard); "Datom is signal's form at the edge"; the today's-division-of-labor guard; the bare-form name and the guillemet rationale; "`Pending`, never an empty structure"; the Containers rule ("bear the kinds once, generically", Box dropped); nearly the whole Repository section; nearly the whole Map section, keeping the rule and discarding every reason for it; and **essentially the whole Meaning section** — a reader of the skill alone cannot tell a Meaning from a parenthesized string. Also `Intent/data.md` and `Intent/anatomy.md`, the latter naming datom directly.

### 4c. ethos **[sub]**, `Ethos.Rust` item verified **[read]**

Unsupported:
- `:63` "Written `Ethos.Rust`, the part after the period is what the generated Rust writes, and nothing checks that the resulting path exists." — I grepped `Vision/`, `Intent/`, `vision-raw/`, `flows/*/vision/`, `flows/*/notion/` for "Ethos.Rust" and "nothing checks": **zero hits**. The notation is then used throughout the worked example at `:73`, where `Vision/ethos.md:78` writes the same imports as `[ std:[ Clonable Sendable Serializable ] ]`.
- `:105` the `#![allow(...)]` / `#[rustfmt::skip]` rule — zero hits for rustfmt/lint/allow anywhere.
- `:24`, `:49` the `Clone, Debug, PartialEq` and `rkyv::*` derives — Vision says only that Ethos Zero emits the two datom kinds.
- `:25,46,51,87` `i64` for `Integer` — every approved example writes `Integer`.
- `:88` `where Self: Sized` — Vision generates plain `fn create() -> Self;` (`Vision/ethos.md:361,381`).
- `:109` `Generated.[ … ]` — the psyche's own page writes `Generated.{ … }` (`flows/e8c4cc61/vision/archive-ethosFileAnatomy.md:33`).

Contradiction: `:30` "`Name.Type` is an alias" stated flatly, against `Vision/ethos.md:287-291` — "**placement carries the meaning**. Head then symbol is a variant of `Query` or `Response` in a Signal's first two sections, an alias in the types section." The skill's own example at `:36` breaks its own rule. Second contradiction: `:12` states a Sema's sections as settled, where `Vision/ethos.md:19-20` and `Vision/sema.md:14` both say the rest is to be decided.

Dropped, on the topics named in the brief: **Non-repetition** loses its aim clause ("the most terse, non-repetitive syntax ever made"). **The ethos/datom division** loses its "in today's division of labor" guard. **Ethos Zero** — the entire "Zero" section is absent; the skill names `ethos-zero` three times and never says it is the former Monolith, that Zero means version 0, that there is no daemon and no Nexus yet, or (at `:105`) the living's own correction *"which is not a daemon, hence its name"*. **Kind syntax** — the identity/definition distinction, "a constraint is a kind, or a bracket of kinds", "two heads that differ in a constraint are two kinds", the angle-bracket recycling, and the legacy tolerance for `Write`/`Read` are all gone; "Run is not a kind" is left as an unqualified law that would reject what Vision explicitly tolerates. **The two mandatory kinds** — neither `Datomizable` nor `Compositional` appears in the skill's prose, only inside code, and "no declared type can exist without them" is dropped. **Generation** — the not-a-daemon clause, as above. Plus `Intent/mandatoryTraits.md` and `Intent/conversion.md` in full, and the definitions of "interaction" and "association", both words the skill uses without teaching.

One tension for the living, not for a flow to settle: `skills/ethos.md:67` lists `Embodied`, faithfully following `Vision/ethos.md:55`, but at `flows/6329f1/vision/archive-protos.md:36-40` (2026-09-04) the living said *"I think I want to drop 'embodied' and just stick with … 'sized'"*. That was about the `Sized` bound, not the naming example — worth asking. **[sub]**

---

## 5. Ranked — what most needs distilling or purifying

1. **`Vision/orchestrate.md` "meta-orchestrate"** — an approved statement contradicting another approved statement and a 2026-09-12 ruling. Correct Vision, then the orchestrate skill. Cheapest, highest-certainty fix in the set.
2. **ARITY on `Compositional`** — `skills/datom.md:43,58` encodes a removal the living explicitly asked to be undone on 2026-09-12. Distil `flows/f6db8d/vision/arity.md` and regenerate the skill.
3. **Single-field structs and newtypes** — `flows/8e9e77/vision/single-field-structs.md` (2026-09-08) carries a sharp, recent, twice-stated ruling with a syntax example (`name.string`, `age.integer`) that `Vision/ethos.md` does not carry at all. Pair with `flows/cff271af/vision/tuples.md`'s newtype-is-allowed clause and `flows/d63804f2/vision/archive-newtypeWrappingAndSingleFieldStructs.md`.
4. **Purify the three skills of the invented Rust.** `Canonicalizable`, `ReaderBudget`, `Problem`, `Boundary`, the `constraints` field on `Headed`, `type Output`, `budget.spend(path)`, `Path::new()`, `i64`, the derive lists, `#![allow]`, `Ethos.Rust`, "A decimal is finite and point-mandatory." These are not distillation gaps — they are fabrication in the highest-read documents in the estate, and at least one (`Ethos.Rust`) is then used as the skill's own worked example. This is what the living named at `vision-raw/traitsAsCapabilities.md`: *"we found one of the cornerstone of models not understand my vision."*
5. **The Meaning section and the Map rationale** — the datom skill keeps the rules and discards every reason for them, which is precisely the failure mode the living described at `flows/62022e8f/vision/distilledVision.md`. A machine that cannot defend a rule will trade it away.
6. **Ethos Zero in the ethos skill** — the living corrected "is a daemon" twice (`flows/fe34eb/vision/ethos.md`, `flows/fe34eb/vision/nexus.md`). The skill still leaves it open.
7. **Rust component architecture** — five flows, zero Vision statements. `Intent/mandatoryTraits.md` alone is not enough: the trait-fusion ruling (2026-08-17), the greenfield/extraction split (2026-08-12), the anti-guard rulings (2026-08-18), and the "regular functions pretending to be traits" cornerstone (2026-08-20) are all raw and all repeatedly re-learned.
8. **The machine anatomy lane** — `vision-raw/{assembly,mainFunction,machineAnatomy,importResolution}.md`. Large, coherent, self-superseded already, and entirely absent from Vision. `From` over `Into`, the 3-part machine, AssembledRust, the registry/assembly-file split.
9. **`flows/62022e8f/vision/distilledVision.md`** — a ruling about distillation itself that the psyche-distillation skill only half carries. The missing half: when the living speaks on something already distilled, apply it to the distilled vision directly, not only as a raw log.
10. **Import resolution and the colon** — `flows/2b34fafa/vision/importResolution.md`. Vision chose the colon without the living resolving the flagged tension. Ask before distilling.
11. **Housekeeping**: archive the four `flows/fe34eb/vision/*.md`; add the missing sema source line; delete the five drained `vision-raw/` shells; fold `vision-raw/colonFormTransformerSyntax.md` into its superseding archive; recover `flows/55d18f4f/vision/highLevelView.md` as the real source for `Vision/highLevelView.md`, whose second statement currently has no surviving support.

### Vision impurity — working instructions logged as vision

Per the psyche-distillation skill these are destroyed in distillation, not archived, and the proposal names them. Candidates found, verbatim. **[read]**

- `/home/li/primary/flows/01a03eda/vision/orchestrateRealization.md` — pure dispatch: order, parallelism, scope.
  > actually, first mine the session designing datom; we have changed direction on the string delimiters. So youll have datom modified again. You can do all the work in parallel, and re-adapt orchestrate to the new datom once its done.
- `/home/li/primary/flows/01a03d6e/vision/orchestrateSkill.md` — a deployment instruction. (`Vision/orchestrate.md`'s "The skill" statement was distilled from it; the residue is impurity.)
  > just deploy the proposal without any meta material
- `/home/li/primary/flows/aa4c7747/vision/dispatches.md`, 2026-08-25 — quota management and bedtime, logged as vision.
  > I dont like this. Id rather get a POC, then we can just write a new version to change the bits we dont like later. Im going to bed so lets get codex working; IV been losing tons of unused quotas lately because im not making the agents work.
- `/home/li/primary/flows/aa4c7747/vision/orchestrate.md`, 2026-08-25 — what to build first, i.e. order of work.
  > our first work will be a simple orchestrate nexus that reserves paths to make dead-simple datom-syntax path reservation possible for edit coordination.
- `/home/li/primary/flows/fe34eb/vision/signal.md`, 2026-09-10 — which repos to merge, in what order, whether to keep git history. **This one is cited as a distillation source in `Vision/sources/signal.md`.** The first two entries in that file are vision; this third is not.
  > Yeah, I think you understand the Signal repository, so we could merge all of that there, but let's not just throw a bunch of code that no one's using in there. Start with the code that was written recently ... Let's make sure that whatever depends on Signal standard is then depending on it, or just archive the old Signal repo and then rename the Signal Standard repo to it.
- `/home/li/primary/flows/98fbfa47/vision/rustComponentArchitecture.md`, 2026-08-09 — a task with a delivery format.
  > I want to bring back the rust component architecture skill. ... Just get a file put together so that if we accept it, an agent doesn't have to copy it again or generate the tokens to make it again anywhere, just in a temporary folder or something, and then I'll review it.
- `/home/li/primary/vision-raw/itsATranslator.md` — a momentary working stance.
  > right now, I dont really give a fuck what anything is built as. Im 100% in vision description mode.
- `/home/li/primary/vision-raw/machineAnatomy.md` — the entry is substantially vision, but ends in budget instruction: *"don't skimp on the tokens. I really don't give a shit. ... so like go crazy."* Impure tail on a sound record; the tail goes, the body distils.

Borderline, and not to be destroyed without asking: `/home/li/primary/flows/62022e8f/vision/designPractice.md`'s "Do not spend Fable output on HTML" and "The converting subflow can also pick the colors" read as durable practice rather than one-time dispatch. **[inferred]**

---

## Sources

Read directly in this thread by the reporting subflow:

- `/home/li/primary/Vision/*.md`, `/home/li/primary/Vision/sources/*.md`, `/home/li/primary/Intent/*.md`
- `/home/li/primary/vision-raw/` — the topic files and archive files named throughout §2
- `/home/li/primary/flows/*/vision/*.md` and `/home/li/primary/flows/*/notion/*.md` — the files named throughout §2
- `/git/github.com/LiGoldragon/Curriculum/skills/{protos,datom,ethos}.md`, `roles.datom`, `AGENTS.md`, `ARCHITECTURE.md`, `README.md`; last-change dates from `git log` and `jj log` in that repository

Relayed from three read-only subagent audits launched by this subflow (§4, marked **[sub]**): one per skill, each comparing the skill source against the named `Vision/` and `Intent/` files and grepping the raw corpus for support. Their path and line citations are reproduced as given; the `Ethos.Rust` and ARITY findings were re-verified directly.

Not witnessed: the shipped behaviour of `datom-codec` 0.26.x and of the `orchestrate` binary. Both are claims taken from psyche records and skill text, not from running code.
