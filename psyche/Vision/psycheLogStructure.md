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

## 2026-08-14 — distillation is ongoing; the chain of origin

> We don't need to think of it only as something that is done in a
> pass. If a flow comes across records that he feels could use
> distillation, then he can make the proposal right there and then.
> So the distillation can be an ongoing process, and we can have a
> list of clues or explain situations where a proposal for
> distillation is appropriate. So we can do distillation passes,
> but it doesn't need to only always happen that way.

> I also want to start considering something which we can develop
> further on the next session, but which you can already have in
> your context for perspective, which is I think Psyche logging
> could be done with the short session ID besides every records,
> which would let a later agent verify the entire conversation if
> the session file is still there and would allow that flow to
> possibly get an actually better understanding of what the Psyche
> was saying because he has different perspective and a better
> focus. So like this chain of origin is essentially the concept
> that is appearing out of all of this approach. And I'd like us to
> just keep it in mind and maybe start, maybe we can do some, yeah,
> maybe we can start logging the Psyche that way. And yeah.

— psyche, 2026-08-14 (Designer session 06196cc7), the second part
dictated. Distillation is ongoing: any flow meeting records that
could use it may propose right there; dedicated passes remain one
form, and the skill carries the situations where proposing is
appropriate. The chain of origin named: the short session ID
beside every record would let a later flow verify the whole
conversation from the session file and re-read the psyche with a
different perspective and better focus — to develop next session.
Entries this round already carry session ids inside their context
lines; the tentative start is making that per-record and
systematic.

## 2026-08-14 — "agent annotations are not records" was never ratified

Reconstructed 2026-08-22 by design session `15b67974` from transcript
06196cc7 L716 (2026-08-14T11:20Z) — the opening of the same message
whose remainder is captured in the entry above. On the distillation
draft line "Agent annotations and context notes are not records; a
proposal may cite them but never treat them as psyche ground.":

> I dont understand

Context (agent-authored): the Designer explained the two kinds of
text in a psyche file (the psyche's quoted words; the agent's context
lines); the psyche's next message moved to the id scheme without
approving or rejecting the principle. It stands unratified — not to
be assumed accepted by any later skill draft.

## 2026-08-14 — ids are increasing numerics; archives are date-based append-only files

> Actually I've changed my mind on hashing the IDs. We should just
> create archives based on dates and append-only files, and give
> each new entry an increasing numeric ID.

— psyche, 2026-08-14 (Designer session 06196cc7), typed.
Supersedes the same-day four-random-hex ruling above: entries
carry increasing numeric ids, and the archive is date-based
append-only files (psyche-archive/<date>.md). Designer mechanics
proposed in the skill draft: the next id is one more than the
highest found anywhere in the log or archive; a record predating
ids gets its number when distillation first touches it; a
distilled record is appended to the archive file of the day it was
archived, its header keeping the origin topic and date.

## 2026-08-14 — the id scheme is unresolved: global counter versus compound references

> I don't understand how you think the numeric ID is going to work.
> Right. If you're saying that we're using an increasing number all
> the time for all the files, then how do we know what the latest
> number is to add another entry? Otherwise, each file has its own
> numbering, which means that a reference needs to know. Like for
> example, if we archive by date, then a reference would be the
> date and the number. And if the raw logs are by topic, then to
> reference a raw psyche log, we need the topic and the ID, unless
> there's something I'm missing here.

— psyche, 2026-08-14 (Designer session 06196cc7), dictated, ending
the session's skill-draft round. The id mechanics are unresolved: a
single increasing id needs a source of truth for the latest number
(the Designer's highest-found-anywhere proposal unratified);
per-file numbering makes every reference compound — date plus
number into the archive, topic plus number into the live log. The
distillation-skill design restarts in a fresh flow from this
trail; the chain-of-origin concept above is marked for that
session too.

## fb1008c0-1 — 2026-08-14 — session-scoped ids; retrofit by origin hunt

> I see your C now; the agents knows his own counter. thats clever.
> and we could hunt for the origin of every existing record to
> retrofit them. I like that idea

— psyche, 2026-08-14T14:03+02:00 (Designer session fb1008c0),
typed, closing the id fork: a record's id is its originating
session's short id plus that session's own count. The flow knows
its own counter, so there is no global source of truth and no
cross-flow race; the id names the record, not its location, so it
survives topic merges and archiving. Date-based append-only
archive files stand unchanged. The retrofit is the psyche's
extension: hunt the origin session of every existing record and
assign its id retroactively. Supersedes the increasing-numerics id
mechanics above. This entry carries the first session-scoped id in
its header — Designer placement, veto open.

## 1030529c-1 — 2026-08-14 — agents generate psyche data or delegate from it; distilled psyche seeks a skill home

> right. psyche data is anchored in the psyche skills
>
> actually, what should happend with the data youre trying to move
> is you should make a psyche proposal.
>
> In fact, this is a really good idea. So when agents want to write
> something down that they've sort of semi-synthesized from whatever
> they're doing, either it agrees with Psyche, and therefore it
> could really just be a Psyche record, but in that case, obviously,
> it would have to be approved by the living Psyche. Or it's not
> Psyche, or it doesn't align with Psyche, in which case it's
> garbage. So really, an agent that's interacting with the Psyche is
> really only trying to generate Psyche data, or is using Psyche
> data to delegate implementation. And I think this is really
> important. This is a fundamental principle, I think. And we could
> probably distill the spirit or intent out of this, at least. I
> know I've been neglecting intent because, you know, at least for
> me when it's logged as vision, it's logged somewhere. So I can
> always later on, you know. But yeah, I see intent as essentially
> data that needs to become a skill. Because now it's so true that
> it has enough authority to just be read by anyone who deals with
> anything that's related to that. So it's not that all of intent
> becomes a skill called intent. But it's that we really want to
> sort of generate skills from intent. But this also brings me to
> another aspect of all this, which is traceability or ancestry or
> whatever we want to call it. I mean, technically, because of how
> I've instructed skills to be designed, any skill edit needs to be
> approved by Psyche. So in a sense, all skills, if they're done
> properly at this point, are as good as Psyche. And, you know,
> there's the higher layer, the top layer, which we haven't reached
> yet. But until then, right, the highest authority is other than
> typing in the user prompt are skills. So really, what we're trying
> to do by accumulating all this Psyche is first to give references,
> right, for agents that can look at the vision and see what should
> be done. But it would give more reliable results if this data was
> loaded through a skill, because the context then would have a
> higher LLM authority. So what I was trying to get at is that I
> think that we could have a system whereby edits that are done on
> skills refer back to a Psyche record or more than a Psyche record.
> Because once we've distilled Psyche, which is we've reformulated
> it in a more understandable and or more just like a terser,
> direct, well-written form, which is what AI LLMs are good at, then
> we've made it, we've created a line that is really looking for a
> home in the skill. So there's a whole lot of skill editing to, and
> obviously Psyche logging, to get out of all this.

— psyche, 2026-08-14T15:45+02:00 (Design sibling flow 1030529c),
first two lines typed, the rest dictated, answering the anchor
principle and the question of where evicted awareness synthesis
goes: make a psyche proposal. Generalizes the distillation trail
above into the principle that a flow interacting with the psyche
only generates psyche data or delegates implementation from it;
semi-synthesis either agrees with psyche (a record, on living
approval) or is garbage; intent is data that needs to become a
skill — skills are generated from intent, per topic; properly made
skills are as good as psyche and are the highest authority below
the typed prompt until the top layer is reached; skill edits refer
back to the psyche records they distill.

## 2026-08-19 — duplicate topics: distill the psyche instead; review that protocol, we've never done it

Design session `7c3f0c1d`, typed (captured 2026-08-19T13:05+02:00). On the
Designer's proposal to fold the duplicate topic `sessionLogging.md` into
`session-log.md` by appending its entries verbatim:

> the right thing to do is to distill this psyche instead. lets review that
> protocol since we've never done it

## 2026-08-19 — propose the distillation skill; one unified statement for one subject

Design session `7c3f0c1d`, typed (captured 2026-08-19T13:40+02:00). On the
protocol review:

> re distillation: propose the skill

On the Designer's five re-articulated statements for the session-log topic:

> your distillation proposal: why are you not making one unified statement
> from all of it? Isnt it all the same subject?

## 2026-08-19 — the distillation skill draft mixes the particular with universals; one statement is a falsehood

Design session `7c3f0c1d`, typed (captured 2026-08-19T14:45+02:00), on the
draft description "Psyche records repeat, overlap, or stand superseded, and
their subject can be said once." and the body's first line "Distillation
replaces a set of psyche records with one re-articulated statement":

> > and their subject can be said once.
>
> thats clumsy. your mixing your particular with universals
>
> > Distillation replaces a set of psyche records with one re-articulated
> > statement
>
> again, same falsehood. not reading the rest. ask if you dont understand what
> I mean

## 2026-08-22 — considering: psyche logging into the flow protocol; more frequent distillation; a distilled file in the flow's directory

Design session `15b67974`, typed (captured 2026-08-22T13:39+02:00),
stated as a consideration, after the flows/ protocol landed:

> now im considering moving psyche logging into the flow protocol as
> well, and emphasizing more frequent psyche distillation, with
> distilled entries kept in their flow's directory but moved into a
> "distilled" file or something similar.

## 2026-08-22 — psyche/Vision becomes the home of distilled psyche; raw psyche lives in flows/*/psyche/; archives are archive- prefixed files in the same directory

Design session `15b67974`, typed (captured 2026-08-22T15:19+02:00),
answering the anatomy questions on the flow-protocol move.

On whether psyche/Vision/<topic>.md remains the live merged view
while flow directories hold the raw records:

> yes and that would now become the home of distilled psyche going
> forward. so finding raw psyche would search flows/*/psyche/

On whether psyche-archive/ stands unchanged as the destination for
distilled-away raw records:

> no, distilled logs are moved into an archive- prefixed file in the
> same directory

## 2026-08-22 — distillation defined: self-standing records, clarified and purified by the model, always explicitly reviewed by the living psyche; agglomerate across flows, favor recency and certainty

Design session `15b67974`, typed (captured 2026-08-22T16:28+02:00),
answering the unratified "agent annotations are not records" flag
(06196cc7 L716, reconstructed above):

> context is crucial to understand any statement. a distilled record
> is self-standing; clarified and purified by the model, which do
> this very well, but *always reviewed explicitely by the living
> psyche*

> so essentially, psyche distillation is the model attempting to
> articulate the psyche in a more coherent form, agglomerating
> records made across several flows that touch the same topic,
> favoring more recent statements, and favouring statements made
> with more certainty, when overlapping or contradictory readings
> surface.

## 2026-08-22 — a skill is still a file; rename the undistilled corpus; log vision: flows/<id>/vision/; top-level psyche/ maybe unnecessary — Vision/ and Intent/ as typed directories

Design session `15b67974`, typed (captured 2026-08-22T16:47+02:00),
on the proposed psyche-skill wording ("psyche/Vision/<topic>.md —
distilled psyche"; the existing line "The spirit skill — Spirit
lives there, not in a file"):

> 1. a skill is still a file. and untill the entire psyche/ corpus is
> distilled, that proposal isnt true. we could rename the current
> corpus's main directory to make this clear, and encourage
> distillation into the new location
>
> and I just noticed something; we are loggin psyche, yes, but more
> specifically we are logging psyche *vision*. so we should make it
> flows/<id>/vision/...
>
> this could even make the top level psyche/ unecessary. distillation
> could happen in vision/ and intent/ (maybe Vision/ and Intent/
> carry more cognitive weight, and the caps imply a typed directory),
> with spirit being treated in a special way for technical reasons.

The same message continues on spirit and entry files; that part is
logged in spirit.md (2026-08-22).
