# Books of 28 to 30 September, and the living's words across them

Flow 7328f4 subflow. Read-only evidence; nothing distilled or ranked beyond counting. Times on comments are as the artifact service stamps them (no zone given). Times on transcript lines are UTC (Z).

## Part one: the books

The Artifact listing shows 12 artifacts updated 28 to 30 September (nothing newer than 29 September; the 30 September comments sit on books last updated on the 29th). Maker is taken from the page's own header or from the flow logs; where a page names none, it is marked "inferred".

### 1. Anatomy Correction
- URL: https://claude.ai/artifact/D6SqvvtHpi1JKwGWEDXnAb (updated 2026-09-29)
- Maker: Psyche Fable, flow c64ee3 (page cites transcript c64ee3f5, line 530, model claude-fable-5-1, 2026-09-29T18:55Z).
- Says: The two Ethos files of the first two anatomies written whole, each with its root (Signal root for the Curriculum Nexus wire vocabulary; Library root for a flow's "finished" declaration), after the living ruled a block lacking its type is not ethos.
- Comments (2 threads, 2 comments):
  - 2026-09-30T16:59, on "Ethos file 2 of 2 · Library root": "If you're only listing types then you can use the `types` type. We should make sure that that's in the code, in the spec, and in the vision anyway."
  - 2026-09-30T17:10, on "Ethos file 1 of 2 · Signal root":
    > This is something that goes deeper but the ethos syntax here is not what I envision still and I didn't address it before. Now I see that it's a bigger problem. We also want to work on other things and try to fix it. I feel like I've been fixing for days.
    >
    > On the syntax we don't want to do something like there's too much indirection. I already said, for example, if you have a skill type and one of the variants is psyche, that psyche object: the rule of ethos is that if there's another type called psyche with the same name, that's what data that variant carries. You don't need to write psyche type.
    >
    > We don't really need something like the collection because submit is too short. Using just an indirection to put a simple struct there, I think, is bad form. I think we can just have the definition of that struct be what comes right after the submit. The submit variant has, for data, a struct and its name will just be derived deterministically by ethos. I think that, for a variant, you can have a variant and a struct name be the same thing so I don't even think that's a problem.
    >
    > When we say stuff like skill name, I think it should just be name. Maybe not. Maybe that's appropriate. I haven't read everything. I don't know what deployed is. I'm trying to see where deployed actually happens. Oh vector deployed. Okay yeah, that's fair. The rest is all good.
    >
    > Like I said don't use psyche type. Just type psyche. I mean I'm not telling you to change. Obviously that's division so I want all of division to be edited to take that into account. Let's put a package together for this and give it to Fable on a new flow to help design this properly so he can send sub-agents to look at the current state and make his design proposition. Astra makes his and then we'll combine them. Fable and Astra Mind will agree after they've done their own design proposal on what it should actually look like.  And then Mindester will implement it on a fresh flow.

### 2. Anatomy One (skill deployment, first anatomy)
- URL: https://claude.ai/artifact/CTTfMGtjQoTH6q5SqXq6Lq (updated 2026-09-29)
- Maker: Psyche Fable, flow c64ee3 (transcript c64ee3f5 line 285, 2026-09-29T16:33Z).
- Says: What skill deployment is today (51 flat Curriculum files, a run-once Rust generator that knows no skill kind) and a pre-concept: three skill repos, a Curriculum Nexus, typed skills; nine questions, e.g. where a payload from several places comes from, where a skill's type is declared.
- Comments: 0 on this page. (Its text also sits inside For You, where the thread below landed.)

### 3. The Order of Work
- URL: https://claude.ai/artifact/LnGQc6q1GqVo8Rcm5red8S (updated 2026-09-29)
- Maker: Psyche, first person; flow not named on the page (c64ee3 log records "The order of work decided", 2026-09-29; inferred Psyche Fable c64ee3).
- Says: A count of what the living spoke of most on 28 and 29 September (skills about 22, the page about 18, Zeus and the cable about 13, seats about 11) and the frustrations, then a seven-item order: Zeus first, then Codex carrying Sol 6.1, seats that start whole and end closed, the page, commits colliding, skill deployment and session-finished wait on the living.
- Comments: 0.

### 4. Where the Design Is Going
- URL: https://claude.ai/artifact/4xykHZ7v47Xa2mKQjVwM2i (updated 2026-09-29)
- Maker: Psyche, first person; flow not named (inferred Psyche Fable c64ee3).
- Says: What the living's words of the day settled (skills in the Curriculum database, type from the skill itself, a registry with dependencies, Spirit a kind, version control a Nexus, "book not page") and a Signal-root skill registry with seven skill structs and seven dependency enums; asks the order within Mind and whether ethos should grow to state the repetition once.
- Comments (2 threads, 3 comments):
  - 2026-09-29T22:38, on "This is a Signal root. Its sections, in order, are imports, queries, responses, types.":
    > Now I see what you mean by root vocabulary. Yes I like that terminology. Let's put it in the vision, which means the skills, right? When I say vision I mean the vision part, the skills. When I say put it in the vision, then when I talk to Seki I like to have context because it's communication. I want to recontextualize all of that as having to do with that particular vision that already exists in the context of what we're changing, right? A comprehensive review of the vision and then how that part changes now changes the whole thing so I can approve it in one of its distillation proposals. Everybody can just do distillation so mine can do an operation. Right.
    >
    > Technically I think if psyche can tell mine that something is okay to use as an operation based on the psyche, then that's kind of like the psyche saying it's good enough and we can try that for now. I would like to see what happens and what you think of that.
  - 2026-09-29T22:41, on the Signal root block:
    > Okay we should edit the ethos design because this is a pattern that we need to train better for. When there is a repetition like that, a dependency, then the different variants become either the only payload or one of the payloads of that dependency field. We're not going to put spirit dependency, intent dependency. We're going to say dependency and then of the type: spirit, intent, blah, blah, blah, blah, blah, blah.
    >
    > Rethink everything and redo all of it. Let's get an audit, even on what already exists, to fix and reorganize it better anatomically because it's stronger that way. You have less change when you change a variant and you just add another variant. It's less confusing because now your code is just the same; it's matching on the same enum so you don't have to really change much.
  - 2026-09-29T22:41 (same thread): "Let's distill that into some vision."

### 5. Field — present cluster state  (cluster survey)
- URL: https://claude.ai/artifact/EH6m7CH4cLPYASTuodici1 (updated 2026-09-29)
- Maker: Field Sol, flow 1bc255 (source at flows/1bc255/books/field-state-2026-09-29/source.md; page says evidence is Field's, "later synthesized by Mind").
- Says: Read 15:36 on 29 September: Ouranos and Prometheus answer, Zeus has no current contact witness; carrier returned after the living's replug but no peer MAC or lease, so the likely boundary is the physical attachment after Ouranos's USB downlink (hypothesis, not diagnosis).
- Comments: 0.

### 6. Field state and independent seats — draft  (cluster survey)
- URL: https://claude.ai/artifact/Y3HBSuJHjH6bAG4ddxWF5a (updated 2026-09-29)
- Maker: Field Astra d5b96b (named on the page; flows/d5b96b/books).
- Says: Eight declared nodes, runtime evidence only for Prometheus, Ouranos and a strong Zeus candidate peer at 15:55; the 46-seat independent-seat ledger (2 successor mappings, 1 concluded, 43 unresolved) and that Fable ended the old-obligation chasing.
- Comments: 0.

### 7. For You
- URL: https://claude.ai/artifact/Afo898DtrDNPf82Q5aLi3H (updated 2026-09-29)
- Maker: Psyche Fable 8904b1 (the page of waiting questions and proposed distillations; the living's comments are quoted in flows/8904b1/vision/skills.md as "comments on the page 'For You'").
- Says: Questions waiting on the living (Markdown page skill, refresh paragraph, countdown rollback, command-versus-Nexus boundary, tests built by Nix) and proposed distillations (one Primary workspace, datom). Also carries the skill-deployment first anatomy.
- Comments (15 threads, 16 comments, all by the living, all open, none sent to Claude):
  - 2026-09-28T18:47, "The refresh paragraph": "Until we have a proper flow tool to respawn a flow easily, the skill is not very useful. Although that's the goal, I eventually don't want flows to compact because compacting is a short-term remedy to a problem that requires a much more refined approach to reorganize the context in a new flow. That will then be much more on point than just accumulating all this history.
    This ties into the distillation: we need to distill the psyche so that it's in a more perceptible form, ease of cognition, right? The way I talk is sort of all over the place and we need to put that back into a nice package and format, which is how I call it: distillation."
  - 2026-09-28T18:49, "The Markdown page skill": "Yeah what I want is actually a sub-agent, a programmed sub-agent. Where are we putting these? Are these also skills or are they deployed by curriculum?
    I want the call to cost the main flow that calls it as little as possible so that it knows everything. It doesn't even need the markdown. It should be able to get it from the transcript. That way the main flow doesn't have to output the token into the sub-agent. It just says, "In my transcript I said something that I want to make into a book."
    Or we could make an even more refined version of that with a smarter model that makes a book out of the transcript, eliminating suggestions that were overridden later on (sort of like recency wins first) and presenting everything that the psyche hasn't responded to (or that needs to be seen by the psyche or reviewed by the psyche or something). That would be cool.
    It would just be a single sub-agent with almost no arguments, no prompt made by the main flow, and then it would just make a book or a page, whatever, from the transcript."
  - 2026-09-28T18:50, "The countdown rollback": "This is more like an operation skill so give it to Astra. If there's something that you think needs to be fleshed out more carefully in there, let me know. I think Astra can make a good operation skill with that. Maybe Astra can also deploy the architecture that we've been drafting for how skills are deployed and then you can review what he's done."
  - 2026-09-28T18:52, "The boundary between a command and a nexus" (first of two): "Yeah this is important. We need to have this optional compilation with some parts of the code so that there's no datom logic in the nexus. The nexus only decodes known types using rkyv and some kind of whatever protocol we roll into it, such as the protocol that I've talked about, which I would like to push also. It identifies the process that causes the CLI and passes it into the message.
    Maybe eventually the CLI talks to one of the nexuses, like Flow or something, so that Flow can tell it which flow that process is. When the message comes into whatever nexus the CLI was calling, it tells it which flow called it, which flow this is coming from. Not by trusting that the flow put its ID in the message, but from the virtue of the process that called it"
  - 2026-09-28T18:52 (second, same thread): "But yeah it's really important that we don't put any extra logic for handling deserialization and serialization of text in the Nexus because the Nexus has to stay small. That's the whole point because they keep running and we might have a few so we want their runtime to be as small as we can make them."
  - 2026-09-28T18:53, "Check a push against the real remote": "I'm not sure I get this. A push is a push but whatever. If you think that there's a problem there, I guess fix it but pushing is pushing to me. I don't know what pushing is without pushing to a remote. I don't know if you're just hallucinating there, or you're making stuff up, or if there's something valid. You can let me know on the next page if there's something I'm missing."
  - 2026-09-28T18:53, "Stop a process by its number": "Again this sounds like an operation skill maybe."
  - 2026-09-28T18:54, "Tests built by Nix, Rust kept apart from data": "Yeah this is important. Also we don't want to be modifying things that are not Rust in a Rust executable repository. When we write a Rust runtime, it has its own repo and we don't put anything there except what needs to be there to compile the executable or the library."
  - 2026-09-28T18:55, "The Herdr skill": "What's your question here? You want to put a vocabulary that explains the spelling or something? I don't understand what you want from me here."
  - 2026-09-28T21:29, "Remove both, keeping the five functions.": "Sounds good."
  - 2026-09-28T21:31, "A skill's kind is the directory it sits…": "Yeah that's a good minimum viable product."
  - 2026-09-28T21:31, "First the types and the command, readin…": "We would have to flesh that out more. What you're saying is very, very vague so let's look at the anatomy, the structure of it. You should be making pages with ethos, syntax, and some visuals showing me the architecture.
    Another thing that I find missing (but this might be a bit too much for us to handle right now) is the Nexus and the rename of SEMA, the rename of the database. I think we should just call something simple because it's really just a simple concept and SEMA becomes the meaning language.
    We could have specialized pages too to look at the anatomy of what you're proposing here for example."
  - 2026-09-28T21:32, "Psyche Fable still works from a copy": "Yeah if you're still not working in the right workspace, we should restart your flow in the right workspace."
  - 2026-09-28T23:35, "Goes to the vision, on datom": "Good"
  - 2026-09-28T23:38, "Proposed distillations / All flows work in one Primary workspace": "This is good but we should specify that this is only until we have a different workflow where the workspace is generated per flow and how the logs are handled is all different.
    Either there's a central repository that is symlinked there. That would probably be the first step there and then we'll have a Nexus replace. Eventually all the data will go through Nexuses. Eventually everything will just be Datom. As far as the models are concerned they'll speak in a Datom specification and then they'll only see and talk to Nexuses through their CLIs or whatever, or maybe embedded in the menchi. There are going to be flows embedded in Nexuses themselves or calls for flows that will probably go to the flow Nexus.
    That's why I'm saying we're kind of doing the Unix philosophy of doing one thing well and then plugging these things together with their signal contract."
  - 2026-09-29T16:55, "Pre-concept: a typed skill": "We need to edit the skill that concerns this. Whenever ethos is written, this block is not ethos because it's lacking a type so it's invalid. Ethos always has to be correctly written; otherwise it's out of context, which means we don't know what it is. Actually you're telling me that it's ethos but still we should just write it correctly."

### 8. Who Contacts Whom
- URL: https://claude.ai/artifact/PW1i1qraz9ZjWcpxy7jzGV (updated 2026-09-29; page dated 2026-09-28)
- Maker: Psyche Opus 183ae0, with Psyche Fable c02c0d.
- Says: No psyche, mind or field role skill exists today (only psyche.md, which is not a role skill; mind.md never existed; field.md retired); three drafts, one per aspect, each teaching only its own contacts.
- Comments (1):
  - 2026-09-29T00:22, on "Codex / The line is left alone in the frontmatter…": "Well the line should still be removed because it's a cost. Anything we leave is a cost. If it's useless remove it. Anything else that's also useless should be taken out in all cases. We should just make it a trait, right? We can make something quite general about this. I don't know."

### 9. The Mentci-Criome Bridge
- URL: https://claude.ai/artifact/5PJiTz7AzuK1njSsDfNR2B (updated 2026-09-29)
- Maker: Psyche Fable, flow c02c0d (transcript lines 849 to 1094, 2026-09-28 23:55Z to 2026-09-29 00:16Z).
- Says: Mentci's stateless bridge holds one path to Criome's privileged socket; both ends are pinned to a contract nobody can compile against while the finished ethos contract sits unused on main. Six waiting questions, including who may speak to whom.
- Comments: 0 on the page. (The living spoke of it in the transcript: "a bunch of gap-filling with a poor understanding of my approach", 183ae001 line 813.)

### 10. Anatomy of the Base
- URL: https://claude.ai/artifact/6VBZ2GGQZWszkFze8nFMhV (updated 2026-09-28)
- Maker: Psyche Fable (page cites record c02c0d-1 and 8904b1-5; flow 8904b1 or c02c0d, not named).
- Says: The small components bigger tools will stand on (Curriculum, Describe, Forge, Reach, Key, Activate; the Nexus shape), each with inputs, outputs, what it must not do, its ethos types and an example call; marks separate the living's words, approved vision, proposals and the unsaid.
- Comments: 0.

### 11. Four Live Codex Seats
- URL: https://claude.ai/artifact/TR6EhLfLtPK1xLJCxSvx9P (updated 2026-09-28)
- Maker: not named on the page (read from the four seats' rollout transcripts; inferred a Psyche seat).
- Says: What Mind Astra, Field Astra, Mind Sol and Field Sol did on 28 September; "Zeus is updated" done; Home still failing at two Home Manager services; Forge paused.
- Comments: 0.

### 12. Where Your Page Lives
- URL: https://claude.ai/artifact/FEUNRWLtNs3Ch6ewMXShrY (updated 2026-09-28)
- Maker: Psyche Fable (page says "Psyche Fable now"; flow not named).
- Says: The page is a display over a small database held beside it at claude.ai; comments are the only channel, a Book sub-agent reads comments and the flow's transcript and writes rows; Codex seats have no way in. Weak points: comments get no reply, updates are not cheap, instructions have drifted.
- Comments: 0.

Not in the window: "Cluster Update 38de5b" (2026-09-25) and earlier. No other For You or Who Contacts Whom pages exist; both are single pages. Cluster-survey books found: two (#5 from Field Sol 1bc255, #6 from Field Astra d5b96b). No cluster-survey book from a Mind or Psyche primary was found in the Artifact listing.

Comment totals: Anatomy Correction 2; Where the Design Is Going 3; For You 16; Who Contacts Whom 1; every other book 0. Total 22 comments in 20 threads, all by the living.

## Part two: the living's words, 28 to 30 September

### Method and limits
- Corpus: (a) blockquotes of raw psyche records in the 55 files of flows/*/vision and flows/*/notion changed in git 28 to 30 September (165 distinct quote blocks after removing copies relayed between flows); (b) the 22 comments above, dropping those already quoted in (a); (c) non-relay user-typed messages in Claude transcripts 28 to 30 September, dropping any already in (a) (38 kept; the 30 September messages in flow 7328f4 are here). Total 212 units.
- A mention = a unit whose text matches the subject's keywords (regexes in the scratchpad, `count.py`, `S.json`). Keyword counting is crude: one unit can count for several subjects, and a long message counts once. Counts are comparable to each other, not exact.
- Not searched: Codex-seat transcripts; no `transcript` command exists on this host, so Claude JSONL under ~/.claude/projects was read directly. No vision files from 30 September exist yet (only the 7328f4 typed lines). The Order of Work's own tally (skills 22, page 18, Zeus 13, seats 11) used a different unit and dates 28 and 29 only.
- "Force" column: units of that subject holding profanity, "I want"/"I don't want", "important", "biggest", or words such as ridiculous, absurd, stupid, dirty, madness, unusable. The count of units containing profanity is given in brackets.

### Counts
| # | Subject | Mentions | Force units (profane) |
|---|---|---|---|
| 1 | Skills (kinds, repos, deployment, vision as skill) | 65 | 20 (3) |
| 2 | Who talks to whom / cost of Fable | 51 | 15 (1) |
| 3 | Books / pages / presentation / phone reading | 40 | 12 (0) |
| 4 | Seat and flow lifecycle (start, close, messenger, registration, probes) | 36 | 12 (2) |
| 5 | Workspace, commits, locks, version control | 31 | 10 (5) |
| 6 | Nexus architecture (signal, Sema, small daemons, Unity) | 29 | 7 (0) |
| 7 | Deployment and build (Forge, Lojix, Nix) | 24 | 8 (1) |
| 8 | Logging and recording psyche (distillation) | 22 | 12 (2) |
| 9 | Zeus, cable, network, cluster | 18 | 8 (0) |
| 10 | Ethos / datom syntax | 16 | 2 (0) |
| 11 | Trust and agents editing without approval | 16 | 10 (4) |
| 12 | Hooks and polling | 11 | 6 (0) |

Overlap note: subjects 1, 5, 7 and 11 share many of the same units (the skill and workspace arguments of 28 September, 16:00 to 17:20Z). Ethos is under-counted: the living's ethos words of 29 and 30 September are a few long comments, not many units.

### Strongest two lines per subject (verbatim)

**1. Skills**
- "I want everybody, and I want the skills to be fucking recommitted when they're changed and regenerated." (flows/8904b1/vision/anatomy.md, 8904b1-10, 2026-09-28)
- "It is too bad that changing any skill requires recompiling the entire Rust binary that we use to deploy it, which is ridiculous." (flows/183ae0/vision/skills.md, "Vision moves into skills")

**2. Who talks to whom / cost of Fable**
- "We should really minimize how much Fable is talked to because it's the most expensive model." (flows/6f51ad/vision/communication.md and c02c0d/vision/seats.md, 2026-09-28/29)
- "No we should try to avoid talking to Fable. What happened?" (transcript 7328f4ba line 420, 2026-09-30T16:21Z). Also line 442: "No we're going to limit the communication to Fable and Astra also."

**3. Books / pages**
- "It's basically unusable and I've talked about this. How do we deal with the mobile aspect?" (transcript 183ae001 line 715, 2026-09-29T00:26Z)
- "A lot of the books that were made in the last wave were actually overwhelming." and "I don't want to be showered with too much data. It's too much to deal with." (transcript 7328f4ba line 508, 2026-09-30T17:14Z)

**4. Seat and flow lifecycle**
- "My new flows are not getting a nice fat user prompt for context. They're told to read files, which yields lower-quality context." (transcript 183ae001 line 1280, 2026-09-29T17:13Z, after "This has been missed now for the last couple of days.")
- "The old one's still open and I bet if somebody tries to message people, they'll wake the old flow up. That's really bad." (transcript 183ae001 line 1088, 2026-09-29T16:44Z)

**5. Workspace, commits**
- "I don't understand why it's so fucking complicated to just get everybody to commit your changes immediately as soon as you fucking make it on primary and everything will be fine." (transcript 8904b10d line 5864, 2026-09-28T16:10Z)
- "So these 37 workspaces, what the fuck is going on with that?" (flows/8904b1/vision/anatomy.md, 8904b1-7, 2026-09-28)

**6. Nexus**
- "But yeah it's really important that we don't put any extra logic for handling deserialization and serialization of text in the Nexus because the Nexus has to stay small." (comment on For You, 2026-09-28T18:52)
- "My biggest concern is: starting to record things better; moving to a better workspace; developing, eventually, the nexuses that will take it to the next step, which is psyche, mind, and field" (flows/c64ee3/vision/priorities.md, c64ee3-10, 2026-09-29)

**7. Deployment and build**
- "I think logics is a big problem because it bottlenecks deployment and changing logic depends on reapplying it so we have this really slow process that this creates." (flows/8904b1/vision/anatomy.md, 8904b1-29, 2026-09-28)
- "The fact that they're not deployed is probably the real problem." (flows/6f51ad/vision/home.md, 2026-09-28)

**8. Logging and recording psyche**
- "I think the logging is absolutely excessive, incomparably excessive." (transcript 8904b10d line 6059, 2026-09-28T16:29Z)
- "It's almost like their log is bigger than their transcript, which is absurd, and we need to fix that." (same message)

**9. Zeus, cable, network**
- "So me asking the machine to update Zeus for days isn't enough to convey my intention that I want it to be updated?" (transcript 8904b10d line 6840, 2026-09-28T17:57Z; flows/6f51ad/vision/zeus.md)
- "It doesn't make any sense at all to me whatsoever. There was a problem but we just can't find it right now. It'll probably come back later and bite us in the face when we least expect it, unless we find the cause now and fix it." (transcript 8904b10d line 6038, 2026-09-28T16:28Z)

**10. Ethos / datom**
- "I feel like I've been fixing for days." (comment on Anatomy Correction, 2026-09-30T17:10)
- "Using just an indirection to put a simple struct there, I think, is bad form." (same comment)

**11. Trust and agents editing**
- "Well the madness is letting agents edit skills." (flows/8904b1/vision/skills.md, 8904b1-18, 2026-09-28)
- "I'm just trying to prevent another fucking mess from happening there. I have very little trust in you." (transcript 8904b10d line 6338, 2026-09-28T16:58Z)

**12. Hooks and polling**
- "I really want to plug into the hooks." (transcript 7328f4ba line 442, 2026-09-30T16:26Z)
- "Whenever you say something important, this is why I want the hook." (flows/6f51ad/vision/clusterSurvey.md, 2026-09-29)

### Also heard on 28 September, 16:13Z (the single hottest message, transcript 8904b10d line 5883)
"Wow you guys are fucking stupid. Fix this fucking mess and get us some agents to fucking kill everything, fucking wipe it out, wipe it the fuck out. ... Okay I don't want to talk to them anymore. They're all working in different copies and aggregating everything."

## Part three: later words that reverse earlier ones

- Skill kind from directory. 2026-09-28T21:31 (comment on For You): "Yeah that's a good minimum viable product." (the kind is the directory the skill sits in). Then 2026-09-29T16:11: "No the skills will be typed. Just copying the directory name is dirty."
- Rebuild claim. 28/29 September record: "changing any skill requires recompiling the entire Rust binary ... which is ridiculous." Then 2026-09-29T16:31 (c64ee3f5 line 260): "It's not. Those weren't my words. I was told that this is how it works by Opus so they're not my words."
- Ethos shape of the skill registry. Where the Design Is Going (29 September) carries SpiritDependency, IntentDependency and so on; 2026-09-29T22:41: "We're not going to put spirit dependency, intent dependency. We're going to say dependency and then of the type". Then 2026-09-30T17:10: drop the "Collection" indirection, "Just type psyche", not "psyche type"; "the ethos syntax here is not what I envision still and I didn't address it before". Also 2026-09-29T16:55: a block lacking its type is not ethos (led to Anatomy Correction), which 30 September says still is not right.
- Prometheus Wi-Fi. 2026-09-28T16:17Z: "...Prometheus's Wi-Fi, which does let the traffic through, but I don't want that." Then 2026-09-29T21:44Z: "I'd rather use Prometheus's Wi-Fi." and "I'd rather connect to my own Wi-Fi network and turn off this Mega."
- Talking to Fable. 2026-09-28 and 29: "We should really minimize how much Fable is talked to". 2026-09-30T16:21 and 16:26: avoid Fable and Astra. But the 2026-09-30T17:10 comment on Anatomy Correction says to "give it to Fable on a new flow" for the ethos design. Possible tension; not resolved by a later line.
- Workspaces. 2026-09-28T16:08Z: "we need to create a workspace for every main seat." 2026-09-28T16:10Z: everyone commits on the one primary workspace. 2026-09-28T23:38 comment: one workspace "only until" a per-flow workspace exists. 2026-09-29T17:12Z: "We're not using work trees."
- Volume of books. 2026-09-28T21:31: "You should be making pages with ethos, syntax, and some visuals showing me the architecture." and "We could have specialized pages too". 2026-09-30T17:14Z: the last wave of books was "overwhelming"; wants about 3, or 1 per aspect, few concepts. "Page" became "book" on 2026-09-29T21:38Z ("if I say 'page' then I mean a book").
- Buttons. 2026-09-28T23:35Z: pages without buttons; comments only. No later line reverses it.

## Sources
- Artifact list (scope all) and Artifact/ArtifactComments reads of the 12 URLs above; saved page copies under the scratchpad artifact-files directory.
- flows/*/vision and flows/*/notion files changed in git 2026-09-28 to 2026-09-30 (55 files); flows/c64ee3/log.md; flows/d5b96b/log.md and summary.md; flows/1bc255/books/field-state-2026-09-29/source.md.
- Claude transcripts under /home/li/.claude/projects (sessions 8904b10d, 183ae001, c02c0dd5, c64ee3f5, bd0019dd, 7328f4ba), user-typed lines only, relays and task notifications excluded.
- Scripts and intermediates: /tmp/claude-1001/-home-li-primary/7328f4ba-d5c4-440f-aa68-7e1d969deab8/scratchpad/ (count.py, S.json, units.json, typed2.json, ents.json, comments.py).
