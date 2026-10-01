# Questions since 28 September: what the living asked or needed to know

Flow 6997eb, Psyche Fable. Covers 2026-09-28 through 2026-10-01 inclusive. Times are UTC. Each flow is named by its six-character id. Transcript line numbers are given as `Lnnn` for the record where I found the words; a queued copy of the same message may sit a few lines from the number the companion report gives. "Mode not stated" means the record does not say whether the words were typed or spoken by speech-to-text (STT); where a vision record or the companion report states it, that statement is carried. Quotes are verbatim. `…` marks an omission. `[ ]` marks a restored question mark or a correction carried from a source record.

## Method and limits

- **Observation.** I read the companion report `psyche-since-28-september.md` whole, then read every user record and queued message of the 19 sessions it lists under Sources (310 candidate messages after leaving out relayed `#msg` bodies, task notifications, skill loads, launch briefs, readiness probes and machine-assembled recovery messages; 190 after removing duplicates between a queued message and its record). I took every question mark and every sentence of need ("I want to know", "I don't know why") and read each message in full.
- **Observation.** The `transcript` command is not installed here; I read the JSONL records with a script.
- **Convention.** An implied question is stated in one line as my inference, under the verbatim, and marked "Inference". A polite request in question form ("Can you fix this?") is an instruction and is left out unless it carries a real question. A rhetorical question is kept where he answered it himself.
- **Convention.** Status words. *Answered*: his words, or a flow's record, answer it; the answer is quoted or pointed to. *Open*: no answer in the words I searched. *Superseded*: his later words replace the question. "Open" means open in his words and the flow records I read; an agent's reply in a transcript is not his answer and was not searched.
- **Unknown.** Page comments that are not stored as user records are known to me only where the companion report quotes them. Any question that exists only in a relay between agents may be missed. Input mode is not recorded in the transcripts.
- **Left out.** One question in a message about pairing: the code itself is not reproduced and no token or credential appears anywhere in this report.

---

## 1. Skills, curriculum, and the skill-deployment nexus

### Q1

> I saw you didn't put in Logics. Does that mean that you think we don't need it?

- **Provenance:** 2026-09-28, 8904b1 L5776, mode not stated.
- **Status:** answered: his own words, 2026-09-28 18:18, 8904b1 L6988: "I think logics is a big problem because it bottlenecks deployment and changing logic depends on reapplying it so we have this really slow process that this creates."

### Q2

> I don't know what you mean by "move the primaries pin to the new source." Why the pin to what? It sounds too complicated for deploying skills. We need to make a nexus to deploy skills. Why should it be right? Is it curriculum nexus?

- **Provenance:** 2026-09-28, 8904b1 L5776, mode not stated.
- **Status:** answered: in part, 2026-09-29, 183ae0 L823, mode not stated: "The skills are not supposed to be in the curriculum anymore. The curriculum is just the executable source code." The pin question itself has no answer in his words.

### Q3

> Because I was allowing agents to make certain kinds of skills, I want to know the situation on that: different kinds of skills and how that would translate into actual implementation. If it became a circus, or if they ignored it, or if they made a mess of it

Inference: he wants to know what happened when agents were allowed to author skills, and how bad it was. (my inference)

- **Provenance:** 2026-09-28, 8904b1 L6187, mode not stated.
- **Status:** open: no answer from him in the words searched; he went on at 17:20 "I'll trust your judgment on the skill cleanup and then I'll just go read them." (8904b1 L6607)

### Q4

> Maybe we need a better term than test, like experimental or what's the term I'm looking for, like when somebody is a candidate or something.

Inference: what is the right word for a skill being tried out before it becomes a compensation skill. (my inference)

- **Provenance:** 2026-09-28, 8904b1 L6569, mode not stated.
- **Status:** answered: 2026-09-28 17:20, 8904b1 L6612: "And we're going to use a trial prefix so that you understand the concept after that."

### Q5

> I think we should just prefix all the skills but I don't know. … How does that sound? For an unprefixed skill what if there is a skill called compensation? … then there's a lack of consistency in application, isn't there?

- **Provenance:** 2026-09-28, 8904b1 L6569, mode not stated.
- **Status:** answered: 2026-09-29 21:34, c64ee3 L804, STT: a pipeline "that prefixes skills based on the payload itself"; and 2026-09-28 17:20 8904b1 L6612 "we're going to use a trial prefix".

### Q6

> Whatever are we calling the nexus for skill generation? … Is it curriculum?

- **Provenance:** 2026-09-28, 8904b1 L6695, mode not stated.
- **Status:** superseded: by 2026-09-29, 183ae0 L823: "The curriculum is just the executable source code." He asked again at L886 (next entry).

### Q7

> I don't know what the set-aside skills are. I can't search all of this chat for everything.

Inference: he wants to be told what the set-aside skills are, in an artifact he can find. (my inference)

- **Provenance:** 2026-09-28, 8904b1 L6863, mode not stated.
- **Status:** open: no answer in the words searched.

### Q8

> Let's talk about how subagent files get put in. Do we create a subagent section in each of the skill repos so each aspect can create its own types of subagents?

- **Provenance:** 2026-09-28, 8904b1 L7455, mode not stated.
- **Status:** open: no answer in the words searched.

### Q9

> Are the skills training flows to use the right messenger tool? Let's take a look.

- **Provenance:** 2026-09-28, 8904b1 L8228, mode not stated.
- **Status:** open: no answer in the words searched.

### Q10

> Let's make sure everybody is well trained in how Nix works and symlink-ing and stuff like that. Maybe we should have a basic teaching/training for that somewhere, like in a trial skill. If we don't have it already

Inference: do we already have a Nix training skill? (my inference)

- **Provenance:** 2026-09-28, caf622 L708, mode not stated.
- **Status:** open: no answer from him; a notion exists at flows/caf622/notion/nix-training.md (named in the landed report's Sources), which is not a ruling.

### Q11

> So you're saying we didn't have any skill that talked about how to make flashbooks and pages and books and things like that? I thought I'd had agents make a skill like that or did we remove it? It's okay, I'm just curious.

- **Provenance:** 2026-09-29, 183ae0 L781, mode not stated.
- **Status:** answered: a trial-flashbook skill appears in the present skill list (2026-10-01); his own record does not say how it came back.

### Q12

> Now we need three skill repos so we need to finish designing that or we just scrap the whole idea of deploying skills for now. I don't know.

Inference: shall we design the three skill repos or drop skill deployment for now? (my inference)

- **Provenance:** 2026-09-29, 183ae0 L823, mode not stated.
- **Status:** answered: in direction, 2026-09-29 21:34, c64ee3 L804, STT: "Bring the new skill stack with the three different source repos, each for a different aspect to be in charge of". The report still counts the design as open.

### Q13

> So if the CLI is not called curriculum, then what is curriculum?

- **Provenance:** 2026-09-29, 183ae0 L886, mode not stated.
- **Status:** open: one reading is a notion only, 2026-09-29, c64ee3, STT: "The curriculum maybe is an even more advanced concept: the concept of personality building or the post-training. … I'm just throwing that out there too".

### Q14

> The big question that this just brought up in my mind is designing a way to deal with a datom payload that comes from multiple places.

- **Provenance:** 2026-09-29, 183ae0 L902, mode not stated.
- **Status:** open: he weighed two options in the same message (a path reader inside datom, or a compiled signal file beside the datom) and called neither settled.

### Q15

> Do we have a psyche, mind, and field skill?

- **Provenance:** 2026-09-29, c02c0d L966, mode not stated.
- **Status:** open: no answer in the words searched; the landed report lists the aspect-contact skill as open design.

### Q16

> What do you need to know to create the anatomy of the proper curriculum architecture? I don't know if you could have these midterm outputs that you can print. I think they're called commentaries but you can let me know the vocabulary so we can agree and then clarify this in the vocabulary skill.

Inference: what is the right word for the mid-turn outputs, and what does the architecture anatomy need. (my inference)

- **Provenance:** 2026-09-29, c64ee3 L257, STT.
- **Status:** open: no answer in the words searched.

### Q17

> I forgot the other one.

Inference: what is the missing fourth kind of skill in the hierarchy he was reciting (vision, operation, documentation, trial, and one more)? (my inference)

- **Provenance:** 2026-09-29, c64ee3 L1007, STT.
- **Status:** answered: 2026-09-28 17:02, 8904b1 L6468: "compensation and test skills" are the field kinds; operation and documentation are the mind kinds.

### Q18

> So do you want to put that into an operational skill?

- **Provenance:** 2026-10-01, e2a70a L1136, mode not stated.
- **Status:** open: no answer in the words searched.

## 2. Flows, restart, first prompts, seats, and talking to Fable

### Q19

> Don't we have a closure script for that? Let's finish it and start an Astra session, a mind Astra, so you can talk with him, right?

- **Provenance:** 2026-09-28, 8904b1 L5880, mode not stated.
- **Status:** open: no answer in the words searched. (STT wrote Clojure as closure.)

### Q20

> Do we have the new Sonnet out? We need to update Claude to get the new Sonnet 5.5. It supposedly might have come out, I don't know.

- **Provenance:** 2026-09-28, 8904b1 L5880, mode not stated.
- **Status:** answered: 2026-09-29 16:38, bea031 L3200, typed: "It is a fact that Sonnet 5.5 came out yesterday".

### Q21

> So what's the situation with Mind? Are you able to talk now?

- **Provenance:** 2026-09-28, 8904b1 L6569, mode not stated.
- **Status:** open: no answer from him in the words searched.

### Q22

> I would like to know what kind of actual material has been loaded into it.

Inference: what was Fable's context actually loaded with? (He saw only four skills.) (my inference)

- **Provenance:** 2026-09-28, 183ae0 L278, mode not stated.
- **Status:** open: no answer in the words searched.

### Q23

> Why did he tell you this?

- **Provenance:** 2026-09-29, c02c0d L875, mode not stated.
- **Status:** open: no answer in the words searched.

### Q24

> It should be rare for Field to talk to Psyche, right? Very rare and actually almost never. … Primary, secondary, tertiary, and they need to have a good reason, right?

- **Provenance:** 2026-09-29, c02c0d L939, STT.
- **Status:** answered: his own continuation in the same message, and 2026-09-30 16:26, 7328f4 L432, typed: "No we're going to limit the communication to Fable and Astra also. … use the layer underneath to coordinate the work. … That's the vision."

### Q25

> Would it be possible to resume the same Claude flows in the new harness?

- **Provenance:** 2026-09-29, bea031 L3200, typed.
- **Status:** answered: 2026-09-29 17:06, bea031 L3864, typed: "Well obviously the sessions have to be idle, right? You can quit the harness and start the harness again with `--dangerously-skip-permissions` and then type in `resume`".

### Q26

> Okay so you're ready to resume the Clojure sessions in a new instance of the harness that's running the new version?

- **Provenance:** 2026-09-29, bea031 L3817, mode not stated.
- **Status:** answered: 2026-09-29 17:06, bea031 L3864, typed (the same answer as the entry above). STT wrote Clojure for Claude.

### Q27

> You're using subagents to run commands, right?

- **Provenance:** 2026-09-29, bea031 L3883, mode not stated.
- **Status:** open: no answer in the words searched.

### Q28

> Have you resumed the Fable flow in the new version of Claude?

- **Provenance:** 2026-09-29, bea031 L4232, mode not stated.
- **Status:** open: no answer in the words searched.

### Q29

> So you're saying that because the session was started in an older version of Claude, even if we resumed it, it would use old versions of the model for subagents?

- **Provenance:** 2026-09-29, bea031 L4242, mode not stated.
- **Status:** open: no answer in the words searched. He ruled at L3200 that the model number should not be hard-coded.

### Q30

> What do you mean the prompt is committed? It's in your transcript.

- **Provenance:** 2026-09-29, 183ae0 L1357, typed.
- **Status:** open: no answer in the words searched.

### Q31

> Why would you spend twice as many tokens for the same thing?

- **Provenance:** 2026-09-29, 183ae0 L1365, typed.
- **Status:** open: no answer in the words searched.

### Q32

> What is the problem you say you're having? Durable terminal? I don't know what you mean.

- **Provenance:** 2026-09-29, bea031 L4498, typed.
- **Status:** open: no answer in the words searched.

### Q33

> Wait you're saying the Flow has to register itself on the Messenger? It's not registered when it started.

- **Provenance:** 2026-09-29, bd0019 L110, mode not stated.
- **Status:** open: no answer in the words searched.

### Q34

> So you were instructed to register yourself with the messenger when you didn't need to. Is that what you're saying?

- **Provenance:** 2026-09-29, bd0019 L145, mode not stated.
- **Status:** open: no answer in the words searched.

### Q35

> I see there are some overlapping seats. Are the ones without the V2, the new ones?

- **Provenance:** 2026-09-29, caf622 L4295, mode not stated.
- **Status:** open: no answer in the words searched.

### Q36

> I'd like to talk about a system with Fable to use hooks so that we can know when a session is finished so that it can be reaped. … Maybe you can tell me.

Inference: is there a way to learn, without polling, that a session has finished? (my inference)

- **Provenance:** 2026-09-29, d5b96b L105, typed.
- **Status:** answered: in part, 2026-10-01 01:12, 7328f4 L898, typed: "Let's focus on hooks and using hooks to do an event-based infrastructure".

### Q37

> You're still running with the old title and there are a few duplicates, I think, that I can still see. There are no duplicates but you're on the old title, which means you haven't been relaunched. I don't know what the difference is.

Inference: why is this seat still on its old title, not relaunched? (my inference)

- **Provenance:** 2026-09-29, 6f51ad L9848, mode not stated.
- **Status:** open: no answer in the words searched.

### Q38

> No we should try to avoid talking to Fable. What happened?

- **Provenance:** 2026-09-30, 7328f4 L417, typed.
- **Status:** open: no answer in the words searched.

### Q39

> Let's agree on whether all of the seats will restart, whether we refresh all the flows, or whether we'll resume some of them from the newer harness.

- **Provenance:** 2026-09-30, c64ee3 L1669, mode not stated.
- **Status:** answered: in part, 2026-10-01 01:12, 7328f4 L898, typed: "Maybe we can even resume the sessions on a new server so that it has Sol 6.1. Unless the context is old, then we should just start a new flow for them and reparse the old one."

### Q40

> Let's find out the state of everything, where all the flows are, what they've been covering mostly, and what hasn't been addressed that seems to be important.

Inference: what is the state of every flow, and what important thing is unaddressed. (my inference)

- **Provenance:** 2026-10-01, 7328f4 L898, typed.
- **Status:** open: no answer in the words searched; the landed report psyche-since-28-september.md covers his words only, not flow state.

### Q41

> Let's see how that was all done and do a little bit of an estimation. Use the subagents to estimate how much was done by the LLM and how much effort was expended to do all this.

Inference: how much of the Codex migration was done by the LLM, and at what effort. (my inference)

- **Provenance:** 2026-10-01, e2a70a L585, typed.
- **Status:** open: no answer in the words searched.

### Q42

> Is someone taking care of migrating Field Astra to the new server?

- **Provenance:** 2026-10-01, e2a70a L1048, mode not stated.
- **Status:** open: no answer in the words searched; the landed report lists it as unknown.

### Q43

> I see three sessions that were started with a weird prompt and don't seem to have a role and they were just abandoned. I'm wondering what the hell is going on.

- **Provenance:** 2026-10-01, e2a70a L1109, mode not stated.
- **Status:** open: no answer in the words searched; repeated at L1169: "I see these three weird-looking random sessions that cost me money and I don't even know why they are there but I don't see any Mind Astra."

### Q44

> If it's possible we should just pass the title of the session as an argument to the startup command. I'm imagining it might be possible so that we don't have to make this a multiple-step thing.

Inference: can the session title be passed as a startup argument? (my inference)

- **Provenance:** 2026-10-01, e2a70a L1247, mode not stated.
- **Status:** open: no answer in the words searched.

### Q45

> What the hell is field pilot?

- **Provenance:** 2026-10-01, e2a70a L1260, mode not stated.
- **Status:** answered: in part, by a flow's relay, 2026-10-01 17:58, 098f27 L270 (agent text, not his words): "Pilot is now completed and retired; current active roles are the two Minds, Mind Sol, Field Astra and sole AP owner Field Sol."

### Q46

> Where's my new Fable Flow?

- **Provenance:** 2026-10-01, fe945a L517, mode not stated.
- **Status:** open: no answer in the words searched.

## 3. Books, presentations, and reading what agents say

### Q47

> Would there be a way to resume a book update sub-agent so that it would know from where, which part of the transcript to consider to modify the page?

- **Provenance:** 2026-09-28, 8904b1 L8217, mode not stated.
- **Status:** open: no answer in the words searched.

### Q48

> So you're saying the successor reads the rows in a database. Where is that database? Where? How does this page thing work?

- **Provenance:** 2026-09-28, 8904b1 L8249, mode not stated.
- **Status:** open: no answer in the words searched.

### Q49

> Can you see the button I pushed on the For You page?

- **Provenance:** 2026-09-28, 183ae0 L374, mode not stated.
- **Status:** answered: by himself, 2026-09-28 23:35, 183ae0 L469: "I think the only thing that works really is the comment so we might as well just get rid of the buttons".

### Q50

> This is also very hard to read. I have to zoom to see anything … How do we deal with the mobile aspect? Does Claude care even about this? Are they totally ignoring the issue of different screen sizes in this artifact interface or what's the deal? What can we do?

- **Provenance:** 2026-09-29, 183ae0 L668, mode not stated.
- **Status:** open: no answer in the words searched; the landed report lists mobile readability as open design.

### Q51

> If you're just proposing a line, it's like proposing to shoot a gun. That's not a proposal. A gun is supposed to be shot at a target. What's your target?

- **Provenance:** 2026-09-29, 183ae0 L749, mode not stated.
- **Status:** answered: rhetorical; his own definition in the same message: "A proposal proposes a line to be added to a certain place."

### Q52

> Have we created this subagent that creates a page? … Can you link to your transcript so you would print the presentation midterm … What's the solution to address the transcripts of both?

- **Provenance:** 2026-09-29, c64ee3 L257, STT.
- **Status:** answered: in design, 2026-09-30 17:14, 7328f4 L505, typed: the primary's response "in their transcript that they marked with a beginning and an end as the object that we wanted", which a lower layer turns into a book. Whether the subagent exists is not stated.

### Q53

> Is it better in a file? Now you're saying that even when it's in a file, it's in a transcript. To me if I'm keeping the transcript even for a bit, it gives me the chance to decide: do I want to make it and put it into a file before I delete the transcript later on?

- **Provenance:** 2026-09-29, c64ee3 L1007, STT.
- **Status:** answered: by himself in the same message, STT: "I think we need to instruct models to prefer not actually writing to a file, especially if it's trivial information like logging every single command line."

### Q54

> I'm not sure what you mean by the four books, and some of the things you say are cryptic, like the box on your bed. You mean Prometheus? The mark on the cable? I don't know what that means.

- **Provenance:** 2026-09-30, c64ee3 L1669, mode not stated.
- **Status:** open: no answer in the words searched.

## 4. Workspaces, committing, merging, version control, and logging

### Q55

> So these 37 workspaces, what the fuck is going on with that? Are you saying agents worked in different workspaces? All my stuff is all over the place and that's why they can't see each other's logs?

- **Provenance:** 2026-09-28, 8904b1 L5829, mode not stated.
- **Status:** open: his later words (2026-09-29 17:12, 183ae0 L1253; 2026-10-01 17:35, fe945a L348) show divergence continuing; no cause in his words.

### Q56

> Why do you think there was an orchestrate lock? Because you're all working in the same workspace, duh.

- **Provenance:** 2026-09-28, 8904b1 L5847, mode not stated.
- **Status:** answered: by himself in the same message.

### Q57

> How can it be 50,000 words?

- **Provenance:** 2026-09-28, 8904b1 L6059, mode not stated.
- **Status:** open: no answer in the words searched; the referent is not in the line.

### Q58

> Did you get all the workspaces deleted and merged? My Astra is working in the same place as you. Did you get the skills deployed properly?

- **Provenance:** 2026-09-28, 8904b1 L6182, mode not stated.
- **Status:** open: still open on 2026-10-01 17:31, fe945a L300 and L308: he asked again and said "all of the stray workspace"; the landed report: "Whether the merge has been completed" is unknown.

### Q59

> Why did your worker not release the lock? Is the skill not clear enough? We need to fix that.

- **Provenance:** 2026-09-28, 8904b1 L6717, mode not stated.
- **Status:** open: no answer in the words searched.

### Q60

> What about if the lock is held by another flow? Communicate what you're wanting that lock for and maybe the other flow can take care of it or something.

- **Provenance:** 2026-09-28, 8904b1 L6824, mode not stated.
- **Status:** answered: by himself in the same message, and L6863: "Yeah your lock edit suggestion is good."

### Q61

> Do we not just need a single long-lived nexus that has a single writer logic?

- **Provenance:** 2026-09-29, 183ae0 L1182, mode not stated.
- **Status:** answered: by himself, 2026-09-29 21:37, c64ee3 L861, STT: "There's a tool there that's worth developing into a really simple nexus that we force agents to use instead of [JJ] and Git commands."

### Q62

> How could you be working on a different tree if you're in the same tree? … are you just not even on the same work tree and you're still using separate work trees against my instructions explicitly, clearly, and hardly put down yesterday?

- **Provenance:** 2026-09-29, 183ae0 L1253, typed.
- **Status:** open: no answer in the words searched.

### Q63

> If you only commit certain files … They're left behind on this other commit, dang, dangling … Maybe there's a different flow that we're not seeing.

- **Provenance:** 2026-09-29, 183ae0 L1304, typed.
- **Status:** answered: by himself in the same message: "You have to commit everything basically." and "That's where it breaks: this is the file selection".

### Q64

> I think whoever is trying to clone a repo for 37 minutes is either jamming my disk, which I don't want, or is playing the role of a fool.

Inference: who is cloning a repo for 37 minutes, and why. (my inference)

- **Provenance:** 2026-09-29, 183ae0 L1312, mode not stated.
- **Status:** open: no answer in the words searched.

### Q65

> Okay so, did you log the things that weren't logged and what do you need to merge all of the three workspaces? I thought that was taken care of.

- **Provenance:** 2026-10-01, fe945a L300, mode not stated.
- **Status:** superseded: by his next message, 2026-10-01 17:31, fe945a L308: "I didn't say all three workspaces. I said all of the stray workspace." Whether it was logged is unanswered.

### Q66

> But you say it needed my word so what word does it need? Are you just repeating what he said? It needed my word. You don't know what?

- **Provenance:** 2026-10-01, fe945a L337, mode not stated.
- **Status:** answered: by himself, 2026-10-01 17:35, fe945a L348, STT: "any changes are all of the changes that are logging, or minus the noise. … We need to merge all that and stop diverging."

## 5. Network and hosts: Zeus, Uranus, Prometheus

### Q67

> Why is it going from Prometheus to Zeus? The cable from Prometheus lets you just go through but why is it that Uranus doesn't? I don't want their network setups to be drastically different … why they can't be set up the same way with the same feature

- **Provenance:** 2026-09-28, 8904b1 L5824, mode not stated.
- **Status:** answered: in design, 2026-10-01 00:45, 7328f4, STT (page comment): "Whenever a network device comes up on USB, it shares internet onto it and allows [traffic] to go through. That's it." The cause of the broken link is not answered; see the later entries.

### Q68

> The hosts are not set up the same. Why are they not the same? Nothing prevents sync, but then make them the same. Correctness means the data lives with the data not in the code, right?

- **Provenance:** 2026-09-28, 8904b1 L5907, mode not stated.
- **Status:** answered: in design, 2026-10-01 00:47, 7328f4, STT (page comment): "None of this should be specific to Uranus … I want declarative features".

### Q69

> I swear that last night I couldn't ping Prometheus from Uranus through the cable. If it works now, great. I don't know why it wasn't working last night.

Inference: why did the USB cable link fail, and will it come back. (my inference)

- **Provenance:** 2026-09-28, 8904b1 L6035, mode not stated.
- **Status:** open: he reported the same fault on 2026-09-29 21:21, b666e7 L3801: "It's the same problem again on the USB cable side."

### Q70

> Are you sure that Zeus is still compiling, because if it's basically a copy of Uranus, we have Uranus's build? There's no need to rebuild. I don't understand why you think it's just recompiling or did we update Nix packages? What's going on?

- **Provenance:** 2026-09-28, 6f51ad L6950, mode not stated.
- **Status:** open: no answer in the words searched.

### Q71

> Can't you build on Prometheus with an SSH remote, like getting the builds from Uranus using SSH with a command-line modification?

- **Provenance:** 2026-09-28, 6f51ad L6980, mode not stated.
- **Status:** open: no answer in the words searched.

### Q72

> The biggest problem is authentication. Mostly I use my SSH key from Uranus to deploy, which has root access. Maybe there's a component for that. I don't know.

Inference: how should deployment authenticate without a root key held by agents. (my inference)

- **Provenance:** 2026-09-28, 8904b1 L6967, mode not stated.
- **Status:** open: no answer in the words searched.

### Q73

> Apparently Zeus was updated but the home profiles were unable to update. I'd like whatever is blocking that to be bypassed and I'd like to know what happened.

Inference: what happened to the Zeus home-profile update. (my inference)

- **Provenance:** 2026-09-28, bea031 L2050, mode not stated.
- **Status:** answered: in part, by a flow record, flows/bea031/log.md as relayed 2026-09-29 18:46 to d5b96b: "Zeus durable system/Home repair is complete at exact 4yk/gl6/w50 outputs".

### Q74

> What do you mean it rejected missing herder config files?

- **Provenance:** 2026-09-28, bea031 L2069, mode not stated.
- **Status:** open: no answer in the words searched.

### Q75

> What do you mean the messenger still resolves through the old link? What the fuck is that about? Is that a stateful thing?

- **Provenance:** 2026-09-29, caf622 L3526, typed.
- **Status:** open: no answer in the words searched. His rule from the same message: "We don't do stateful unless we do it in a single call."

### Q76

> I can ping Prometheus, but I can't ping Zeus. It's the same problem again on the USB cable side. I have no contact with Zeus. Can you debug that with Luna or by yourself?

Inference: what is the cause of the recurring Zeus link loss. (my inference)

- **Provenance:** 2026-09-29, b666e7 L3801, mode not stated.
- **Status:** open: at 21:30, c64ee3 L727 he re-plugged the cable and a light appeared: "Find out why I had to unplug and replug the cable back in, maybe, or what the likely cause was"; no cause in his words.

### Q77

> I don't know if Prometheus is unstable or something but it seems to prefer the router, which has a really annoying power signal when it's turned on and it's next to my bed. I'd rather use Prometheus's Wi-Fi.

Inference: is Prometheus unstable, and why does it prefer the router. (my inference)

- **Provenance:** 2026-09-29, c64ee3 L1007, STT.
- **Status:** open: no answer in the words searched; 2026-10-01 05:41, d5b96b L8587: "debug and fix the fact that Prometheus's Wi-Fi access point is not giving me internet access."

### Q78

> I have no idea what that watcher is for and there's a chance that I don't want it.

Inference: what is the watcher for. (my inference)

- **Provenance:** 2026-10-01, 7328f4 L741, typed.
- **Status:** open: no answer in the words searched.

### Q79

> why am I using the full nix path in the command? I dont like agents to handle these.

- **Provenance:** 2026-10-01, 7328f4 L873, typed.
- **Status:** open: no answer in the words searched.

## 6. Codex and Claude updates, stable and next rotation, migration, secrets

### Q80

> So me asking the machine to update Zeus for days isn't enough to convey my intention that I want it to be updated? You're still asking me if that's what I want?

- **Provenance:** 2026-09-28, 8904b1 L6837, mode not stated.
- **Status:** answered: 2026-09-29 16:52, bea031 L3477, STT: "You can deploy home whenever. If something isn't home that means it needs to be deployed".

### Q81

> Is there a problem with the changes that are in and haven't been deployed?

- **Provenance:** 2026-09-28, 8904b1 L6798, mode not stated.
- **Status:** answered: by himself in the same message: "The fact that they're not deployed is probably the real problem."

### Q82

> Where is this release approval block coming from? Where is that instruction? Let's address that.

- **Provenance:** 2026-09-29, bea031 L3553, mode not stated.
- **Status:** open: no answer in the words searched.

### Q83

> How the fuck do we end up in this situation? … How the hell do you give me an older version? … How did I end up with an older version?

- **Provenance:** 2026-09-30, d5b96b L3999, mode not stated.
- **Status:** open: no cause in his words; he called it a repeat: "This has happened before, and we were supposed to have fixed the skills" (L4026).

### Q84

> Can we get the new one instead? How about I get GPT-6.1 Sol instead of 5.6?

- **Provenance:** 2026-09-30, d5b96b L4009, mode not stated.
- **Status:** answered: by a flow record, 2026-09-30 16:34, 098f27 L9 (agent text): Field Luna "replaced by f69847 gpt-6.1-sol"; and by him, 2026-10-01 01:12, 7328f4 L898: "I have the new server on my remote access, so we can start migrating the new flows."

### Q85

> We can call it maybe "compensation update", or should we just call it Codex? Not sure.

- **Provenance:** 2026-09-30, d5b96b L4125, typed.
- **Status:** answered: 2026-09-30 14:01, d5b96b L4139, typed: "I think it's better just like compensation update."

### Q86

> Are we ready to deploy the next Codex infrastructure that will have Sol 6.1, the newest Codex? Using the infinite socket rotation naming mechanism that allows us to move next to stable without renaming the socket

- **Provenance:** 2026-09-30, 6f51ad L12777, typed.
- **Status:** answered: in part, 2026-10-01 01:12, 7328f4 L898, typed: "I have the new server on my remote access, so we can start migrating the new flows."

### Q87

> What pairing code? Did you give me a pairing code through here? That's really unsafe.

- **Provenance:** 2026-10-01, 7328f4 L738, typed.
- **Status:** open: no answer in the words searched; his ruling follows at L873: "I dont like agents to handle these." The code itself is not reproduced here.

### Q88

> So this wasn't committed to Git, right? Hopefully. How would I do this manually myself on my terminal?

- **Provenance:** 2026-10-01, 7328f4 L762, typed.
- **Status:** open: no answer in the words searched; he repeated at L820: "I just need to know how to get the pairing code."

## 7. Hooks, events, polling

### Q89

> I would like to design something efficient and then eventually we'll turn that into some kind of hook that just gets triggered when some kind of event comes out of the harness. What kind of events?

- **Provenance:** 2026-09-28, 8904b1 L7455, mode not stated.
- **Status:** open: no answer in the words searched.

### Q90

> I looked at Herdr this morning and I see that it supports showing me if a session is busy … That means there's some kind of interface there or hooks, or what's happening. Let's see how Herdr does it.

Inference: how does Herdr know a session is busy, finished, or read. (my inference)

- **Provenance:** 2026-09-30, 7328f4 L432, typed.
- **Status:** open: Luna was sent to investigate; no result in the words searched.

### Q91

> Maybe even if there are hooks that could insert stuff when a new message comes in … I don't know if that's possible, but that would be more like psyche research.

Inference: can a hook insert text into an incoming message? (my inference)

- **Provenance:** 2026-10-01, 7328f4 L898, typed.
- **Status:** open: he marked it as research.

## 8. Research and tooling questions

### Q92

> Is there any code out there that started to programmatically change the system prompt of some harnesses? What is the most developed system that has capitalized on this concept? What about open source stacks?

Inference: who has built on the stratification of context in an LLM prompt. (my inference)

- **Provenance:** 2026-09-29, 183ae0 L942, mode not stated.
- **Status:** open: no answer in the words searched.

### Q93

> …see if I could get them to log me into my OpenAI account through the web authentication. That probably gets triggered when OpenCode does a subscription login and we could remotely log in to Codex while I'm not in front of my laptop

Inference: can a flow drive his web browser to complete a login while he is away. (my inference)

- **Provenance:** 2026-09-29, 183ae0 L942, mode not stated.
- **Status:** open: no answer in the words searched.

### Q94

> No, Clojure is the best Lisp, right, because the thing is, Clojure is data. … let's tell people to do research if there's a new Lisp that has surpassed Clojure in correctness … Shen is really cool also but I don't know. Has somebody written Shen in Rust and would it make sense to have Etho to Shen or Shen to Etho, basically?

- **Provenance:** 2026-09-29, 6f51ad L9848, mode not stated.
- **Status:** open: no answer in the words searched. STT wrote ethos as Etho.

### Q95

> Post-training but maybe there's a better word somewhere.

Inference: what is a better word than curriculum for personality building or post-training. (my inference)

- **Provenance:** 2026-09-29, c64ee3 L804, STT.
- **Status:** open: no answer in the words searched.

## 9. Repository classification and gathering his questions

### Q96

> Let's do some research on vocabulary: what have people used, what have other people used, and how have other people talked about these kinds of things, classifying the state of different parts of the project? … Let's do some research into that field also. What have other people done?

- **Provenance:** 2026-10-01, 6997eb L202, mode not stated.
- **Status:** answered: by the landed report flows/6997eb/reports/repository-classification-research.md (commit f88f86, 2026-10-01).

### Q97

> Let's create a nexus that classifies our repositories. Let's think of a name

Inference: what should the repository-classifying nexus be called. (my inference)

- **Provenance:** 2026-10-01, 6997eb L202, mode not stated.
- **Status:** open: no name recorded in the words searched.

### Q98

> If I'm asking for documentation, or maybe the word "documentation" isn't actually what we're looking for, let's look at different terms here.

Inference: what is the right term for logging his questions (mind logging?). (my inference)

- **Provenance:** 2026-10-01, 6997eb L434, mode not stated.
- **Status:** open: no answer in the words searched.

### Q99

> This could get tricky but I think we need a good description of how it's done, with some examples, and how to differentiate between psyche and mind.

Inference: how do psyche, mind and field logging differ. (my inference)

- **Provenance:** 2026-10-01, 6997eb L434, mode not stated.
- **Status:** open: no answer in the words searched.

### Q100

> I want these questions gathered and brought into a book with either answers or proposals for an answer, or proposals for counter questions.

Inference: he wants his questions assembled, with answers or proposals; this is the request that produced this report. (my inference)

- **Provenance:** 2026-10-01, 6997eb L434, mode not stated.
- **Status:** answered: in part, by this report; the book is not yet made.

---

## Count by status

- Answered: 33
- Open: 65
- Superseded: 2
- Total: 100


## Sources

- `/home/li/primary/flows/6997eb/reports/psyche-since-28-september.md` (the companion report, read whole), and its Sources list.
- Claude transcripts, the living's user records and queued messages (`~/.claude/projects/-home-li-primary/` and `-home-li-wt-primary-56ae53/`), files named by flow prefix: 8904b1, 183ae0, c02c0d, c64ee3, bd0019, 7328f4, fe945a, 6997eb.
- Codex transcripts, the living's user messages: `~/.codex-next/archived_sessions/` rollouts for flows 6f51ad, bea031, b666e7, caf622, d5b96b; `~/.codex-next-8mkkxq293hk2/sessions/2026/` rollouts for flows 098f27, d32329, 5104af, e2a70a, 29b75f.
- Flow records used only for answers: `flows/bea031/log.md` and `flows/098f27` handoff text, as relayed in transcripts quoted above; `flows/6997eb/reports/repository-classification-research.md` (commit f88f86); the present skill list for the flashbook skill.
- Git log of Primary for the repository-classification commit.
