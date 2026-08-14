# Psyche logs organized by topic, not aspect

> "psyche shouldnt be organized by aspect, but by topic and date"

— psyche, 2026-08-09, steward session

Context: psyche logs were previously at `psyche/Vision/<aspect>/<topic>.md`.
The psyche ruled they should be at `psyche/Vision/<topic>.md` with
dates and times in the content. Intent topics should be broader and
fewer than Vision.

## 2026-08-11 — the design log is now the psyche log

> that expression needs to be rooted out. it is now the psyche log.

— psyche, 2026-08-11T18:23+02:00 (Designer session 012fbf07), typed,
on the management skill's phrase "the design log": the expression is
rooted out everywhere; the thing is the psyche log.

## 2026-08-14 — statements are not topics; the swarm of tiny files

> encodedFormIsTheCode was a very poor choice of topic. thats not a
> topic, thats a statement. now im looking at those files, and
> theres so many bad topic; colonLegalInStringPosition
> colonConfusion flowsNotAgents genericParametersAreTraits
>
> why are the topics so specific? this will make it hard for agents
> to find something. are we afraid of having big files so much that
> we end up with a swarm of tiny files?

— psyche, 2026-08-14 (Designer session 06196cc7), typed, on seeing
the consistency audit (reports/PsycheConsistencyAudit-2026-08-14.md).
A statement is not a topic: statement-shaped file keys
(encodedFormIsTheCode, flowsNotAgents, genericParametersAreTraits,
colonLegalInStringPosition, colonConfusion named) hurt agent
findability; over-specific topics fragment the log into tiny
files. The psyche's questions answered and a consolidation
proposed by the Designer in-session; the roster ruling pending.

## 2026-08-14 — topic governance, the cleaning pass, a new psyche skill

> lets reframe that to make new topic a psyche blocked thing, and
> lets create a list of topic which are allowed for now. Or maybe
> we just do merging passes to make it easier to log "safely", so
> the flow doesnt have to overthing where to write something down
>
> I think this also brings the subject of keeping the psyche clean;
> after a while too many entries will exist, many of which will be
> overruled statements. The cleaning/merging pass is the way. But
> it needs to be psyche assisted to avoid mistakes. So an agent
> makes proposal statements which are aimed at replacing a bunch of
> psyche records and the psyche pronounces on them, then the old
> records are archived. it should even be archived to link back to
> the record(s) that replace them, ostensibly with a short hash.
> How does that sound?

> yes, that is better and should help slightly, get it deployed
> (through the skills repo of course)

> lets create a new psyche skill. find a name and make a first
> proposal.
>
> and some of the vision should be transferred into skills. we
> should have a manifest then that links some skills to psyche
> archives. see my discussion with claude d2bb5f5f

— psyche, 2026-08-14 (Designer session 06196cc7), typed. Status of
each piece: the topic definition ("a topic is a noun subject an
agent would guess before knowing any ruling; a statement is an
entry heading inside it" — Designer wording) is approved and
deploys through the skills repo. New-topic blocking with an
allowed list, versus free logging with merging passes, is floated
— a combination proposed by the Designer, pronouncement pending.
The psyche-assisted cleaning pass — an agent proposes replacement
statements, the psyche pronounces, old records are archived with
short-hash links to the records replacing them — is the psyche's
design, Designer assessment requested. A new psyche skill is
directed: name and first proposal owed by the Designer, informed
by the session d2bb5f5f discussion; some Vision transfers into
skills, with a manifest linking skills to psyche archives.

## 2026-08-14 — distillation corrections: re-articulation, many-to-many, 4-hex ids, psyche-archive/

> not necessarily. if the records being distilled cover many
> topics. the same input might be used as a reference for many
> outputs

> if we dont specify how, itll be chaos

> You didnt undestand the distillation meant we abandonned allowed
> topics?

> quotes them? that would create a mess. this is our opportunity to
> re-articulate everything, it would be foolish to miss on that.
> the referenced archives still contain the original quotes

> no way we are getting this complex. why would we do that? and
> 8!? Where did my short ID approach go? we use 4 and rarely have
> problems. and in this case, a collision wouldnt be a very big
> deal. cant the llm just produce 4 random hex?

> no, for two reasons; the records will be considered individually
> and whole topic files might not be distilled, and one
> distillation might come from two or more topics. also, it
> shouldnt be in psyche/ - lets use psyche-archive/

— psyche, 2026-08-14 (Designer session 06196cc7), typed, reviewing
the Designer's psyche-distillation skill draft v1 (read through
the archive-path section; the transfer-into-skills section
unread). Rulings: distillation is many-to-many — one archived
record may serve many pronounced outputs; the link mechanism must
be specified exactly or it will be chaos; distillation abandons
the allowed-topics idea — flows log freely, the cleaning pass
corrects; proposals re-articulate, never quote — the archive keeps
every original; record ids are four random hex produced by the
flow, no content hashing; the archive is psyche-archive/ at the
repository root, records archived individually, never by topic
file.
