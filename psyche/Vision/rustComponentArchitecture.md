# Rust component architecture

## 2026-08-08T11:28:10.420Z — all the components had the same overall architecture

Context (agent-authored, separate from the psyche's words): Direct typed human prompt. It repeated earlier text; only the newly added component-architecture words are quoted here. Transcript:
/home/li/.claude/projects/-home-li-primary/55d18f4f-ea0b-43d8-88ae-f8f4bd3027d2.jsonl:460

> And also, I can be blamed for a big part of this, which is I wiped, I completely demolished or significantly altered the workspace and the skills and everything, how the agents were being trained. And I think part of that was essentially this standard of how we create components. And all the components had the same overall architecture. They were a daemon that spoke signal. So you should send an agent to recover that. What's that architecture that we mistakenly thought was still understood by agents, but I never even really considered that my big, huge cleanup actually took that away. And now agents thought they were just writing like, they forgot that all my components have to be like this. So it's like, it's a bunch of signals speaking. And I want to actually be very clear about the terminology here so we don't fucking get lost again. So signal, right? Tell me what signal is. Let's start from the basics. What is SEMA? What is Nexus? I think everybody's completely fucking confused on what I'm actually meaning when I say these things because of how things have been brought up to me. The questions have shown me more and more confusion and I didn't actually clue in that everybody's totally fucking confused and lost on what I actually mean. So go dig in the past. Find out when that big, huge cutoff happened when I decided I need to clean all my skills and change everything and find everything before that. And I mean, spirit should show you how this works, right? It's a daemon. It should have two CLIs, which are just proof of concept. All those CLIs are short-term shims that we use to talk to the daemons. But eventually this is all just going to be a giant sort of cluster of components that exchange signal messages with each other. And there will be like a few different entry points. But yeah, the CLI is just like, it's a way to work ourselves up. Like eventually the LLM models will be trained not in text anymore, but in signal, in binary signal, which is way more dense and carries way more information per bits than any of that text crap. So that's what's going to give rise. This is why I'm going to have to head a multi-billion dollar AI company to show the world how you do this properly because everybody's still doing text like monkeys. And it's wrong. And this is how we're going to get there, bits by bits and component by component. So the daemon doesn't really speak string. Although for now they're records that will hold string fields, but it doesn't think in strings at all. And eventually even all of the string part of language will be replaced by a completely specified, fully typed binary system of enums and structs and scalar values.

— psyche, 2026-08-08T11:28:10.420Z (Designer session 55d18f4f)

## 2026-08-09T15:37:33.564Z — "I want to bring back the rust component architecture skill"

> I want to bring back the rust component architecture skill. I don't
> know if it was called that before, but I want to just throw
> everything in there for now. Just use the old version of everything
> and pack everything into there. Just get a file put together so that
> if we accept it, an agent doesn't have to copy it again or generate
> the tokens to make it again anywhere, just in a temporary folder or
> something, and then I'll review it.

— psyche, 2026-08-09T15:37:33.564Z (Designer session 98fbfa47; full
session UUID 98fbfa47-58a9-4a7b-8847-829443079d25)

Context, kept apart from the quote: no single skill by that name
existed pre-reset; the component-architecture doctrine was spread
across component-triad, contract-repo, actor-systems, micro-components,
the rust/ files, and related skills in the 2026-06-07 stratum. The
restoration is by packing the old versions verbatim into one draft
skill file for psyche review — old content, no regeneration.

## 2026-08-09T17:00:58.506Z — "find the parts that are skill"

> no thats too mindless. find the parts that are skill, take out the
> parts which act in any other way, like listing repos or other such
> non-skill content. also, your "this file was generated" has nothing
> to do with the skill. stick with the very universal stuff "how we
> design our components"

> this is documentation of a repo, not a skill

— psyche, 2026-08-09T17:00:58.506Z (Designer session 98fbfa47; full
session UUID 98fbfa47-58a9-4a7b-8847-829443079d25)

Context (agent-authored, separate from the psyche's words): reviewing
the raw 17-file pack. The second quote responds to the packed line
"Persona's correctness is maintained top-down". The skill keeps only
the universal how-we-design-our-components doctrine; repo
documentation, repo listings, workspace state, and assembly
provenance all go.

## 2026-08-09T18:23:09.678Z — "this is no high level explanation"

> its 8 thousand lines. If it was a thousand lines, I would still
> think its big. this is insane. this is no high level explanation.
> its full of hyper specific stuff. it should be about the daemon,
> the signal wire format, the cli's, the wire type repos, the traits
> first, etc

— psyche, 2026-08-09T18:23:09.678Z (Designer session 98fbfa47; full
session UUID 98fbfa47-58a9-4a7b-8847-829443079d25)

Context (agent-authored, separate from the psyche's words): reviewing
the curated 7,871-line version. The skill is a high-level explanation of the
component architecture — the daemon, the signal wire format, the
CLIs, the wire type repos, traits first — well under a thousand
lines. The hyper-specific doctrine does not belong in it.

## 2026-08-11 — all method calls in our rust code are part of a trait

> I even want to make the broad statement that I want *all* method
> calls in our rust code to be part of a trait, since I need to
> understand my systems through traits and main types, as I cannot
> possibly read all the code, and rust is the new assembly language;
> no serious engineer reads all the assembly code anymore, and the
> same is going to happen to rust, hence why we need a more concise,
> dense and congnitively concentrated language like ethos to write
> code with AI agents.

— psyche, 2026-08-11T19:53+02:00 (Designer session a5587095), typed,
during the protos context-parsing discussion
(protosIsTheSharedStyle.md). The comprehension surface is traits and
main types; Rust is the new assembly, read in full by no one; Ethos
is the concise, dense, cognitively concentrated language for
writing code with AI agents. The psyche called this a broad
statement — candidate Intent; proposal in progress this session.

## 2026-08-11 — traits constrain implementers to think in concepts; research first

> I meant traits constrain the implementers to think in a certain
> way, by forcing the implementation to fit within certain concepts.
> does that make sense? Do a trait-first development research,
> finding people who argue everything should go through traits (they
> do conceptually, if not explicitely; function names often betray
> the trait they would otherwise use in their name)

> Lets do the research first and think about this very deeply. It
> would probably go in skill. the intent aspect is more abstract
> (see 2)

— psyche, 2026-08-11T22:04+02:00 (Designer session a5587095), typed.
The sense of always-use-trait: traits are cognitive constraints —
they force implementations to fit within concepts. Function names
often betray the trait they would otherwise use. Trait-first
development research directed and dispatched; after it, deep
thought — the concrete all-methods rule probably lands in a skill;
the Intent carries the abstract aspect.

## 2026-08-12 — greenfield needs new traits; extraction is for porting

> well, on a greenfield we wouldnt extract; a new need would
> require a new trait (or extending an existing one if that looks
> more appropriate. Extraction would be for porting existing code
> to mandatory-trait standard

— psyche, 2026-08-12T01:26+02:00 (Designer session a5587095), typed,
correcting the Designer's extraction framing. Greenfield code is
trait-first natively: a new need gets a new trait, or extends an
existing one when that fits better. Extraction — lifting a latent
trait out of a method name — is the tool for porting existing code
to the mandatory-trait standard.
