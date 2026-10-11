# Distillation candidates, flow d68c82 vision, 2026-10-11

Gathered for the main flow; no statement is composed here.

Scope: every `## ` entry in flows/d68c82/vision/*.md as the working tree held it (11 committed files plus the uncommitted additions to distillation.md and the untracked flow.md and jev.md). Landed status was read from psyche-skills origin/main at 82c92fa (fetched 2026-10-11); mind-skills origin/main was also read where a record landed outside psyche skills. Book status was read from flows/*/books/*.md sources. Whether each (b) book has since been ruled on was not checked against comment reports, except where a landing commit shows it.

## Counts

- (a) landed in a vision-/intent-/spirit skill: 1
- landed only outside psyche skills (mind-skills), and not as a vision line: 1 (temporaryConditions); two (b) entries are also partly landed in mind-skills
- (b) proposed in a book: 18
- (c) undistilled and unproposed: 5

## Entries

### books.md — What is to be ruled sits in the proposal

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/d68c82/books/3-what-you-rule-on.md, Proposal 1 (targets field-skills compensation-book-distillation, not a psyche skill).

Verbatim record:

    Context: comment on «The Source nexus», on a design point carried in the book's context rather than a proposal.

    > Also this should be in the proposal. I basically almost don't read anything that's not in the proposal. It feels like most of the books are going to waste because I don't see the point of me reading something if I'm not reading it to approve or disapprove it with a comment.

    -- psyche, STT.

### commitMessage.md — Commit messages written in datom, specified in ethos as variants

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/081064/books/type-ethos.md, «The type file» in vision-ethos (commit.type.ethos example).

Verbatim record:

    Context: comment on «Sources in the commit message», ruling 1, approving the commit-message rule.

    > We could also improve the format so that it essentially fits a datom, which would mean creating an ethos specification, but we wouldn't need to make an implementation that uses it yet. It would just be the ethos that shows. You can use a type, `type ethos`. It just starts with `type` and it defines a single type and you can define everything inline, like these quick type definitions, where you can use the inline import syntax.
    >
    > ... We won't need to backport the new syntax to the [commits]. We can do that later. We can improve the syntax so that it's eventually compatible with Datom message. We could even define a specification and ethos for different variants of commit messages so our commit messages would start to be written in a Datom syntax with different variants.
    >
    > I guess you could use vectors when there's more than one type of thing in a commit. It would be good to support that just in case we can't force the commit to be split up or something but we would encourage only one variant per commit message.

    -- psyche, STT. Transcription corrected: "commands" → "commits".

### commitMessage.md — A distillation's sources as a variant: topic and flow id pairs

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/081064/books/type-ethos.md, the `VisionDistillation.Vector<Reference.{ Topic FlowId }>` variant.

Verbatim record:

    Context: comment on the same book, at the example commit-message list for vision-distillation.

    > So you can see how you could easily turn this into a variant with a struct in Elm [sic] syntax, right? Your variant would be `vision distillation` and then it would just be a vector of a name to flow ID.
    >
    > I mean topic and Flow ID.

    -- psyche, STT.

### distillation.md — Source references are not vision

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/d68c82/books/1-sources-outside-the-skill.md and 2-sources-in-the-commit-message.md, Proposal 2 (remove the lists). Partly carried out: psyche-skills 82c92fa removed «Sources» from vision-persona; origin/main vision-distillation.md still ends in «## Sources». Not landed as a line in any vision-/intent-/spirit skill.

Verbatim record:

    Context: on finding a «Sources» section (lines such as `058f16 source`, `081064 ethos`) in a proposed vision skill.

    > To me that looks like noise. There's nothing about this that I want to load into it. ... That's not vision; that's noise. If there is a technical reason to have that data, it does not belong in the vision. I can almost be certain of that.

    -- psyche, STT.

### distillation.md — The source reference goes in the commit message

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/d68c82/books/2-sources-in-the-commit-message.md, Proposal 1. Landed outside psyche skills: mind-skills origin/main operation-psyche-distillation.md:20 «Every distillation refers to the raw psyche it was distilled from, in the message of the commit that lands it» (mind-skills 3e56108, 2026-10-10). No vision-/intent-/spirit line.

Verbatim record:

    Context: on «Sources outside the skill», which proposed a separate sources file per topic.

    > Well we should just put that source reference in the commit message that makes the change.

    -- psyche, STT.

### distillation.md — Books distil psyche only

Date: 2026-10-11 (first commit of the heading by git blame, or as the record states).

Status: (c) undistilled, unproposed. Uncommitted in the tree at this report's writing.

Verbatim record:

    Context: the living opened a book that proposed compensation-skill lines (2026-10-11).
    "So I opened another book and it was proposing compensation skills. I don't give a fuck about compensation skills. These are not my thing. These are for machines to make. When I distill we distill psyche only. God. I mean I could review knowledge skill but it's really just a matter of verifying, testing something, and seeing that it works in a certain way. There's nothing for me to review except psyche so yeah the machine is misguided."
    -- psyche, STT.

### distillation.md — Taking the whole picture, not the one sentence

Date: 2026-10-11 (first commit of the heading by git blame, or as the record states).

Status: (c) undistilled, unproposed. Uncommitted in the tree at this report's writing.

Verbatim record:

    Context: right after the books-distil-psyche-only statement and the seats' immediate relays of it (2026-10-11).
    "And then I feel like I say stuff like that and then you'd turn around and everybody runs like an idiot to quickly get to the one thing I just mentioned. Everybody just acts mindlessly and doesn't try to get the whole picture of what I'm trying to say. They're tripping in their own shoelaces trying to run for the one thing I actually put into words but the one thing I put into words implies a million other things."
    -- psyche, STT.

### ethos.md — An Ethos Nexus whose signal, memory and operation are specified in ethos

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/081064/books/ethos-nexus.md, D1 «The Ethos Nexus, a new section of vision-ethos».

Verbatim record:

    Context: comment on «Sources and the registry», proposal 2, 15:22.

    > In Ethos do we have an Ethos Nexus or is Ethos Zero a non-Nexus? We need to migrate the Ethos Nexus version so that we can do this. In Ethos I want to specify the three aspects:
    > - the signal
    > - the memory
    > - the operation
    >
    > For one or another we can do Ethos now so that would go with the Ethos flow, the eco psyche flow [sic] design to design the ethos of all three parts of the Ethos Nexus.

    -- psyche, typed.

### flow.md — Start flows with the new Flow Nexus

Date: 2026-10-11 (first commit of the heading by git blame, or as the record states).

Status: (c) undistilled, unproposed. Overlaps the landed vision-flow line «The Flow Nexus sets up and starts a model flow» (psyche-skills origin/main vision-flow.md); the record reads as a working instruction (use it now) more than a new ruling — this flow's inference. Untracked in the tree at this report's writing.

Verbatim record:

    Context: the living naming the topics in focus, 2026-10-11.
    "We have certain topics that we're focused on. I really want to use the new Flow, the Flow Nexus, to start flows."
    -- psyche, STT.

### jev.md — Jev puts intelligence into our logic

Date: 2026-10-11 (first commit of the heading by git blame, or as the record states).

Status: (c) undistilled, unproposed. No Jev line in psyche-skills origin/main. flows/33752b/books/1-psyche-honesty.md statement 4 proposes Jev only as judge of precedence; flows/bad807/books/9-jev-use.md and 18-jev.md are Jev design books with rulings, not proposals of this record. Untracked in the tree at this report's writing.

Verbatim record:

    Context: same message, 2026-10-11; the living corrected "Java" to "Jev" in a follow-up line.
    "I really want to start using [Jev] in our logic to put intelligence in. There are so many things to do with [Jev]. It's crazy."
    -- psyche, STT. Transcription corrected: "Java" → "[Jev]" (the living's own correction).

### metaHarness.md — A proper base, redeployable, tested through an API

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/875960/books/1-meta-harness-base.md, Proposal 1 (vision-flow); test-on-API also in flows/875960/books/2-meta-harness-persona.md section «Tests». vision-flow on origin/main has no meta-harness line.

Verbatim record:

    Context: said while asking for packages to the topic Secondaries, on a new-moon day.

    > Let's flesh these out and let's also make a conviction of getting a proper base for the meta harness to work smoothly and to be redeployable. Right now it's kind of like a one-off that only exists on my computer. Creating full tests somehow will probably require that we rely on an API for testing since it's easier to deal with the key management than the subscription. We're going to figure out a way to handle subscriptions.

    -- psyche, STT, 2026-10-10.

### naming.md — Registry names are independent of repository names; uncapitalized camelCase names made of words

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/058f16/books/source-nexus.md («A source's registry name need not be its repository's name. Repository names stay kebab-case.»); flows/081064/books/prototype-name.md (casing rule); flows/058f16/books/word-names.md (word check, dedicated nexus, runtime cost).

Verbatim record:

    Context: «Sources and the registry», proposal 3, "What the key reaches", 15:25.

    > Well the name of the repo and the name in the registry, in our own memory, our own Nexus memory, doesn't have to be the same. Even I would say it seems we've gone with a hyphenated kebab case (I think it's called) for repo names, which maybe is more canonical or standard, and it's fine. I don't have any problem with it.
    >
    > In Protos languages like datom and [Ethos] for things that are not types or traits, we are going to use uncapitalized. It's going to be camel case because we do PascalCase for defined objects in the language and we do variants. If there's a string position in datom and it starts with a capital, that's okay because we have a different type that's kind of like a string but it has to be checked whenever we create a new one. This is the Prototypic name or whatever, the prototype name, which is an uncapitalized identifier. It's going to have to be composed of words so we need to put together some kind of fancy check. Well not that fancy, I guess.
    >
    > That would need a dedicated Nexus because it would need to have a database of words. If we're going to do the word-based identifiers, I'd like to get a book on the runtime size cost of having these things in a certain runtime and how it might be smarter to create a dedicated Nexus for that functionality. We could still just build it into whatever we're compiling into, whatever we're doing for now.

    -- psyche, typed. Transcription corrected: "Esos" → "Ethos".

### persona.md — Persona is the root component of the meta harness; credentials come by encrypted deployment

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/875960/books/2-meta-harness-persona.md, sections «The root of the meta harness» and «Credentials». Only the frontmatter description of origin/main vision-persona.md carries «Persona, the root of the meta harness»; no root or credentials section landed.

Verbatim record:

    Context: comment on «The meta harness has a base», proposal 1 (the base, in vision-flow).

    > The umbrella component, or the root component for the meta harness, is persona. This would go in the persona vision. I guess persona should have everything it needs in the environment. We're assuming an installation of [CriomOS] for now, which is fine. It would need credentials, which obviously we can't just include. These would be deployed from an encrypted deployment through Nix, I guess: Sops, Nix, through the cluster data, ostensibly.

    -- psyche, STT. Transcription corrected: "CreoleOS" → "CriomOS".

### persona.md — The old Persona designs are rewritten

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (c) undistilled, unproposed (no book line found).

Verbatim record:

    Context: comment on «Persona's root and what it does», at the figure of the existing Persona design.

    > Yeah obviously these designs are old so we basically need to rewrite it. There might not be anything, or not much, worth saving there.

    -- psyche, STT.

### persona.md — Which part of the triad Persona spawns is not Persona's vision

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (a) vision-persona, «What the root does» (psyche-skills 7a6b130, approved 2026-10-10): «It keeps a harness instance of each of the triad running: Psyche, Mind and Field.» The landed line drops the proposed «always core, and usually primary» but still names the triad; whether that matches his comment is open.

Verbatim record:

    Context: same book, «What the root does».

    > This is good except I don't know what you mean by triad. Oh I see: psyche, mind, and field. Yeah but we don't need to specify so much which part of the triad it spawns. That could live, I think, somewhere else and we can just not duplicate all the vision because this isn't really specific to persona. The rest of the description is pretty good. That's a rough vision.

    -- psyche, STT.

### psycheCore.md — A Psyche core Primary reviews the core Secondary's designs against the psyche data they rest on

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/33752b/books/1-psyche-honesty.md, Proposal 1 statement 5, Ruling 4.

Verbatim record:

    Context: spoken to the core Secondary during the evening's book work.

    > We should have a psyche core primary for you to get a second opinion on everything before you send a design off. He would review your designs and you would give him the sources that you used and the skills or visions or raw psyche that you follow. You're backing your proposal with as much psyche data as possible, but well-interpreted not twisted.

    -- psyche, STT.

### psycheHonesty.md — Judging whether psyche data has been abused

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/33752b/books/1-psyche-honesty.md, Proposal 1 statement 1 and Proposal 2 (mind-skills operation-psyche-abuse-judging).

Verbatim record:

    > It's a very important skill that we have to define: how to judge if psyche data has been abused by an agent, by a machine, to try and mean something that it doesn't, because it was taken out of context or it was exaggerated.

    -- psyche, STT.

### psycheHonesty.md — Every psyche agent is honest about psyche data; newer, more coherent and emphasized statements take precedence

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/33752b/books/1-psyche-honesty.md, Proposal 1 statements 2-4, Rulings 1-3.

Verbatim record:

    > That's something we should teach all of the psyche agents: how to be honest about the psyche data and understand that the living changes its mind so the psyche changes direction. The newer and/or more coherent and emphasized statements take precedence, which is why we should also really integrate with jev [sic] the System 1 model.

    -- psyche, STT. "jev" is kept as heard; its referent is not known to this flow.

### source.md — A nexus called Source

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/058f16/books/source-nexus.md, D1 (new skill vision-source).

Verbatim record:

    Context: said after commenting on the «Sources and the registry» book in «Open books»; the concepts themselves are in his comments there.

    > I did advance some concepts on how we can get sources from a particular nexus called Source that we would design.

    -- psyche, STT, 2026-10-10.

### source.md — The registry: its anatomy, populated from datom files in each repository

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/058f16/books/source-nexus.md, D2 and D6; flows/081064/books/ethos-nexus.md (Meta Signal: the registry).

Verbatim record:

    Context: comment on «Sources and the registry», proposal 2 (a lowercase source names a registry entry), 15:22.

    > Yes this is good and now we need to define the anatomy of that registry and use the same atomically updatable approach. The registry can be populated from multiple sources using the datom files that can be in the repositories that essentially wrap all of the data in that particular repository and can be updated by whoever updates that repo. It can then be loaded along with other repositories to create a full registry.
    > ... This will be used to put together a registry and it'll just keep it. Every time we update some Ethos source, add one, or edit its name or something, we need to change the registry.

    -- psyche, typed.

### source.md — The hash verifies the files; a smart store comes later

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/058f16/books/source-nexus.md, D1 («A store for hash-addressed files ... is a later lane.»).

Verbatim record:

    Context: same thread, 15:22.

    > Also we could use the content hashes maybe. Maybe we need this hash-based storage. I think I had a thing called Logic Store but we could just move it to something more straightforward like a file store, an archive, or a file archive or something. It would be a nexus where we can put these hash-addressed files. Actually never mind all this. The hash is there for us so that we can verify that the files are the right files when we use them. That's all.

    > For now we can just check the files. Later on we can have a store dedicated for this that will be smart enough to know what to store and what not to store, and how or where to get it (if it has to just use a Git backend to fetch a particular request) so that we don't double-store if we're already storing it in Git (like some kind of smart system). This is not the first lane. This is not the priority lane.

    -- psyche, typed.

### source.md — The hash covers the whole repository; one shared sources library for ethos and curriculum

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/058f16/books/source-nexus.md, D3, D7, D8.

Verbatim record:

    Context: «Sources and the registry», proposal 3, "What the hash covers", 15:27.

    > Since we're going to use repos, we're going to hash the whole thing. It's got lights like Nix [sic], right? When the source changes, the source changes. That's why we don't put non-Rust things in the Rust repo, because if we want to change any of it, then Nix has to recompile.
    >
    > Since the skills are in repos, if we're talking about curriculum, we should have a list of sources. ... It's the same concept for curriculum.
    >
    > We can create a shared library between them, which is about sources, and it can even have objects for memory to store a registry of sources. That way the skill doesn't have a registry for each skill that doesn't need to be updated because it refers by name to the source. Only the source content addressing registry needs to be updated.

    -- psyche, typed.

### source.md — A Source nexus: Git at a revision, own Blake3 hashes, several registries, backend fetchers

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/058f16/books/source-nexus.md, D1, D4, D5.

Verbatim record:

    Context: «Sources and the registry», proposal 3, "How many", 15:30.

    > This is actually really interesting. We could just make a registry [of] sources. We could make a Nexus called sources and we just put it all there. It can refer to a certain Git with a certain revision and we keep our own Blake3 hashes. We have different registries in fact. Eventually when we cut off Git, we don't need to keep the Git equivalence registry because it's different and some sources don't necessarily need to have it, right?
    >
    > We can have different types of backend fetchers. Basically we have this concept: we can get it from Git or we can get it from a local path on a certain host and we have the hash, right? Even the local path on the host is not dangerous. We would use a technique similar to Nix in that we wouldn't, obviously, include the Git subdirectory in the data, right? It would be the snapshot of that revision that we hash, kind of like how Nix does.

    -- psyche, typed. Transcription corrected: "registry or sources" → "registry of sources".

### source.md — One Source nexus for all components; "get a source" means a source request to it

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: (b) flows/058f16/books/source-nexus.md, D1.

Verbatim record:

    Context: «Sources and the registry», proposal 3, "How many", choice b, 15:31.

    > There's some mix-up here: vision and knowledge. I guess you mean skills or context modules for the curriculum.
    >
    > ... we can have a source. Essentially we're adapting to the language. If I say, "Go get a source," then eventually you'll automatically know that I mean: use the source nexus and send it a source request and then you'll get a source. It's called the source nexus ...
    >
    > I think it's easier to just make the nexus for all the sources and reuse it for all components, then we only have one place to fix the sources aspect.

    -- psyche, typed.

### temporaryConditions.md — A temporary-conditions compensation skill every flow loads by default

Date: 2026-10-10 (first commit of the heading by git blame, or as the record states).

Status: Landed outside psyche skills: mind-skills origin/main compensation-temporary.md exists. Its being in a default module list was not checked. A working instruction rather than vision; flows/d68c82/books/6-back-on-the-grid.md Proposal 1 concerns the conditions after arrival, not this skill.

Verbatim record:

    Context: on Prometheus and Ouranos being powered off for travel.

    > I don't know how we do temporary things. I guess we should have a temporary condition skill that every agent reads. I guess it's a good compensation skill. Temporary compensation, temporary, that's pretty good. That sounds perfect. ... It's a skill to meet temporary conditions that all agents will load so we'll put it in the list of default modules that we load when we start a flow. We should have a list of the default modules.

    > We're going to change the temporary flow [sic], the temporary conditions, when they're over, or the network topology and all that stuff can go in there.

    -- psyche, STT.

## Related raw records for the (c) entries

### Books distil psyche only

- flows/01e496/vision/skills.md and flows/91ea9f/vision/skills.md, 2026-10-02, «Trial and compensation skills without going through the living» — consistent with the (c) record:

    > Give yourself trial and compensational skills to help yourself function the way I've been asking without having to go through me for the skill edit. I'm sure that you can make the proposal and then field can implement it and deploy it.

- flows/d4ae97/vision/skills.md, 2026-10-07, «Every distillation is a skill writing»:

    > So vision is a type of skill, right? Is this vision/directory all stuff that's going into skills? Otherwise we're still fucking around like fucking idiots. Every form of distillation is a skill writing. Every single fucking one of them.

- flows/d4ae97/vision/skills.md, 2026-10-07, «Compensation skills are reviewed for upgrade» — possible tension, this flow's reading: it does not say the review goes through the living.

    > Then we have to start creating this: essentially all the compensation skills are the things that need to be reviewed so that they can be upgraded potentially into an operation skill, a knowledge skill, vision, or whatever.

- Not raw, a current skill line that the 2026-10-11 record contradicts: the book rule loaded in this flow's context, «Every distillation is written into a skill: a proposal names its authored source under psyche-skills/skills, mind-skills/skills, or field-skills/skills.» The 2026-10-11 record is the later explicit correction; flows/d68c82/books/3-what-you-rule-on.md and 4-five-landed-lines.md propose compensation lines to him.

### Taking the whole picture, not the one sentence

- No raw record on the same subject was found in flows/*/vision/ (searched for whole picture, implies, one thing I, mindless, run for). The nearest written line is in knowledge-psyche (psyche-skills origin/main, line 16): «Agents must read between the lines — using written psyche to infer the living psyche». This is a knowledge skill, not a raw record.

### The old Persona designs are rewritten

- flows/9519a1/vision/persona.md and flows/875960/vision/persona.md, 2026-10-10: the same words relayed, not separate records:

    > Yeah obviously these designs are old so we basically need to rewrite it. There might not be anything, or not much, worth saving there.

- No contradicting or superseding record was found. The landed vision-persona «What the root does» (approved 2026-10-10) is the rewrite so far.

### Start flows with the new Flow Nexus

- flows/108ab0/vision/operational-flowStartsFlows.md, 2026-09-17:

    > We need an easy way to start Flow also, for the Flow to start a new flow by just calling Flow, right? It starts it in that Herder server.

- flows/28d847/vision/skills.md (also 5ed94b), 2026-10-03:

    > Let's start. I want to modify the system prompt. I want to use the new flow. I want skills that do skill edits. I want a constant flow of small skill edit proposals, not huge ones, so that I can say yes quickly.

- flows/445410/vision/nexus.md, 2026-10-09:

    > Well, the Flow Nexus will be called directly with the right Datom command, and it might need a few. We need to allow the Nexus to have its configuration loaded atomically so that it can live in separate files in different repositories. [...]

- flows/aa887c/vision/jev.md, 2026-10-05: «Also, using the new Flow, better messages, and Datom syntax for basic commands for a lot of things».

### Jev puts intelligence into our logic

- flows/93ba9f/vision/jev.md, 2026-09-26:

    > [...] this makes me think of Jev [sic], the new AI model. I want to integrate that and start using it because I think it's perfect for us to use Jev [sic] with an approach like this, where we have our own specified language that we could even translate into JSON [...]

- flows/aa887c/vision/jev.md, 2026-10-05:

    > I'm very interested in [Jev], and I think there's huge value there. [...] using [Jev] to automate things like committing and judging if certain items can enter a database and things like that.
    > [...] [Jev] is perfect for judging if something should be edited or if it should be merged with some other text because it's kind of overlapping, so that the database doesn't grow too fast and there are no conflicting views on anything. It would be really useful to do the commit messages, check that the system is running, and check that there are no conflicting main flows.

- flows/bad807/vision/jev.md, 2026-10-04:

    > Extend the proposals for how we can use it now, maybe for different parts of what we're trying to design in our communication/flow handling system. How this [Jev] could be used to make decisions, or to guide decisions, or to give data that will maybe make another [Jev] call put out data that will eventually come out as a decision somewhere

- flows/d68c82/vision/psycheHonesty.md, 2026-10-10: «which is why we should also really integrate with jev [sic] the System 1 model» (already (b) in 33752b).

- No contradicting record found; the 2026-10-11 record widens the earlier ones.

## Tensions found in (a)/(b) entries

- Source references are not vision: psyche-skills origin/main vision-distillation.md still ends in a «## Sources» section listing `b675f3d9 visionImpurities` and three more.
- Triad: the landed vision-persona line names the triad (Psyche, Mind and Field) after his comment that which part Persona spawns need not be specified in Persona's vision.

## Sources

- flows/d68c82/vision/*.md (working tree, 2026-10-11)
- psyche-skills origin/main 82c92fa: skills/vision-persona.md, vision-flow.md, vision-distillation.md, vision-book.md, knowledge-psyche.md; commits 7a6b130, 82c92fa
- mind-skills origin/main: skills/operation-psyche-distillation.md (3e56108), skills/compensation-temporary.md
- Books: flows/d68c82/books/1..6, flows/081064/books/type-ethos.md, ethos-nexus.md, prototype-name.md, flows/058f16/books/source-nexus.md, word-names.md, flows/875960/books/1..3, flows/33752b/books/1-psyche-honesty.md, flows/bad807/books/9-jev-use.md, 18-jev.md
- Raw records named above under flows/*/vision/
- Provenance receipt: unavailable
