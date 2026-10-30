# Flow Nexus: provenance dossier for the vision-flow module (flow-records-module)

Subject: `repos/psyche-context/vision/flow.md`, 144 lines, read at HEAD of psyche-context. Prepared 2026-10-29 for the Psyche flow Primary, who places each line by horizon (perennial / short / medium / long). **No horizon is assigned here.** Where the record carries a horizon word by the living, it is shown verbatim and left for the Primary to weigh.

Naming: per the living's 2026-10-29 order (554e1a) the Nexus is called Flow Nexus in this dossier. The module itself still says "Flow" for the Nexus; that is quoted as it stands.

## How to read

- Statements are the module's paragraphs, in order, S0 (front matter) to S52. Each is quoted from the module as it stands, then the raw records it draws on follow, each with record id (flow short id + entry), date, and the record's own context and words, verbatim as logged (including the logger's context line, the transcription corrections, and the signature).
- Record id form: `flowid` alone means `flows/<flowid>/vision/flow.md`; `flowid/file` is `flows/<flowid>/vision/<file>.md`; `notion` is marked; `vision-raw/<file>` is the legacy corpus. `entry #k` is the k-th `##` entry of that file.
- Landing: commits are found by `git log -S` on a distinctive phrase of the statement (oldest first) and by the landing commit messages; a landing message names the book or flow when it did. A phrase search shows when a phrase entered, changed, or left; it does not by itself show which record caused the change.
- A long record already shown under an earlier statement is cited by pointer. A record that bears on several statements is shown in full the first time, in the earliest statement it bears on.
- Marks: `NO RECORD FOUND` marks a line or clause for which no raw record words the thing. These are listed again in the index at the end.
- Provenance caveats: records that reached a flow by relay are the relayer's rendering of the living's words (the signature says 'relayed'); STT means speech-to-text; typed is typed. Where a record's own context line is unsure of the living's exact words, that stands. The reference file `flows/30fc30/references/flow-whole.md` maps the same body of records (62 files, 259 entries in flows/*/vision/flow.md; this dossier counted 257 `##` entries in 63 files, 9519a1 and 984e88 having none) and was used; the records were re-read in place.

Short ids that look alike: `4ddc321d` (the 2026-08-26 record) is a different flow from `4ddfe1`.

---

## S0 description (front matter)

Module lines 2-2:

```text
description: Flow — the Nexus that launches, names, tracks and ends flows — or a metaflow, a side flow, a hook or the Capsule is being designed or judged against what the living wants.
```

Landing history (git log -S on the phrase `the Nexus that launches, names, tracks and ends flows`, oldest first):

- 72149ef 2026-10-07 Move Psyche skill sources under skills

Provenance note: The description is a routing line; no single raw record words it. It lists what Flow does (launches, names, tracks, ends) and the topics under it (metaflow, side flow, hook, Capsule).

**S0.1  Record `01e496/flowNexus` entry #2 A flow component that works**  
Date: 2026-10-02 (in the record's context). File: `flows/01e496/vision/flowNexus.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Psyche Fable 91ea9f.

> Right now I would like to have a flow component that works, that can launch flows, and that has hooks in the harnesses that send the right events to the flow component so that it can know the state of each flow.

-- psyche, typed, 2026-10-02, heard by 91ea9f.
```

**S0.2  Record `fe945a/flowNexus` entry #1 The anatomy of Flow in Ethos: Flow holds the lock on flows, flows addressed by name, the flow id in words**  
Date: 2026-10-02 (in the record's context). File: `flows/fe945a/vision/flowNexus.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to Psyche Opus fe945a after correcting its proposed skill line on launching flows.

> I want to develop the anatomy of ethos for the most important component, which is, I don't know, I think, flow. We're having such a hard time handling flows and locking them. Flow could have the lock on the flows so that we can lock it and also address it by name instead of by Flow ID. I'd also like the Flow ID to be converted into words.

-- psyche, typed, 2026-10-02, fe945a.
```

**S0.3  Record `d68c82/archive-flow` entry #14 2026-10-14 — Flow, Nexus and Ethos together; Flow is the bootstrap**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> We're developing the Flow, the Nexus architecture, and Ethos at the same time. There are three aspects, right?
> - the language aspect
> - the runtime architecture
> - that component itself, [Flow], which is probably the most important component to bootstrap
>
> Bootstrap persona, the meta harness, since starting flows like clean lean flows, specialized flows, or refreshing flows is a central part, a cornerstone, of this system.

-- psyche, STT. Transcription corrected: "low" → "Flow".
```

**S0.4  Record `554e1a` entry #1 2026-10-29 — The Nexus is called Flow Nexus; a flow is one run of a metaflow or a single FML flow**  
Date: 2026-10-29 (in heading). File: `flows/554e1a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 21:05 and 21:11, comments on Flow, whole (https://claude.ai/artifact/M4E2xhh4GycRo11GkPNJ1D) by the Psyche flow Primary 30fc30, relayed through Psyche core Tertiary b195f0 and Secondary 9b514f.

Okay, first, let's call this Flow Nexus instead of Flow, because I really want us to say Flow Nexus when we're talking about the Nexus, so that we don't get confused with a "flow."

On "A flow is one run of a metaflow": This is incorrect because a flow could be one run of a metaflow, or it could be a single FML flow. At least in the long term, we have that concept also, but I think we really need to define this long-term/short-term thing. I'm going to get these comments sent to core, and I don't want this proposal to be redone yet. I just want to specify first how we are going to take care of long term/short term, and then, once that's done, we should revisit this.
```

---

## S1 The Flow Nexus sets up and starts a model flow

Module lines 8-9:

```text
The Flow Nexus sets up and starts a model flow: its working
directory, system prompt, training files and instruction prompt.
```

Landing history (git log -S on the phrase `sets up and starts a model flow`, `working ⏎ directory`, oldest first):

- 72149ef 2026-10-07 Move Psyche skill sources under skills

Provenance note: Wording is nearly the psyche's own, from 358f143a (2026-08-18). vision-raw/flowDaemon.md is a title-only stub ("flow — the daemon that sets up and starts a model flow"). On 2026-10-29 (554e1a) he asked that the Nexus be said as Flow Nexus.

**S1.1  Record `358f143a/archive-flowDaemon` entry #1 2026-08-18 — the daemon is not training (abandoned); it is flow**  
Date: 2026-08-18 (in heading). File: `flows/358f143a/vision/archive-flowDaemon.md`  
Context and the living's words, verbatim as logged:
```text
Design session `358f143a`, typed (captured 2026-08-18T15:23+02:00).
Supersedes the successor-repo naming in trainingRepo /
skillsRepository (2026-08-17: "a new repo called training"):

> On another note: the new daemon I want to make isnt training
> anymore (abandonned). Its flow, which will setup and start a model
> flow, with its own working directory, system prompt and training
> files, and its instruction prompt.

Context (agent-authored, separate from the psyche's words): the
component is named flow. What it does, in the psyche's words: set up
and start a model flow, with its own working directory, system
prompt, training files, and instruction prompt. Whether the
repository is also named flow, and what becomes of Curriculum's
generator role, is not yet said.
```

**S1.2  Record `e06e4c07/archive-flowDaemon` entry #1 2026-08-19 — Curriculum is rewritten as a Nexus; the flow repo is the machinery; skills live in another repo; a few basic skills in flow replace the built-in harness prompt; the name stays flow; research requested**  
Date: 2026-08-19 (in heading). File: `flows/e06e4c07/vision/archive-flowDaemon.md`  
Context and the living's words, verbatim as logged:
```text
Design session `e06e4c07`, dictated (captured 2026-08-19T13:49+02:00).
Excerpts from one message; the Nexus vocabulary part is logged under
nexus. Trims between excerpts.

> So for example, the curriculum repository. Now essentially, not all
> of its content will go into the flow nexus, but because the skill
> contents themselves will have to live somewhere else because the
> flow nexus, the repository will be about the machinery of the flow
> nexus. And the actual skills that people want to use with their
> system will have to live in a different repository. Of course, there
> will probably be a few basic skills. No, there will be a few basic
> skills that are actually included in the flow repo, which are
> essentially the analogs of what the basic harness training prompt is
> currently that is built into the harnesses, which we will completely
> replace, is going to be about. Just basic stuff on how agents should
> behave in a harness, but with our own take on it. So do some
> research and anything that's vaguely or closely resembles or touches
> the topics that I've covered, whether it's in programming theory,
> software architecture, software ontology. Let's make you smart. I
> need a smart flow. I mean, this brings me to the fact that the word
> flow is kind of getting overloaded if we have a flow nexus. So we
> can also discuss maybe thinking of a different name for that
> repository, for that nexus. Maybe something that has to do like a
> tap or a source of the flow or something like that. Maybe flow.
> Yeah, flow is good. I like the idea that it's a flow.

Context (agent-authored, separate from the psyche's words): the flow
repo holds the machinery of the flow Nexus plus a few basic skills —
our own replacement for the harness's built-in training prompt (how
agents behave in a harness); the skills people use with their system
live in a different repository, not yet named. The name flow is kept
after a tap/source alternative was considered. Research into
programming theory, software architecture, and software ontology
touching these topics is requested before going deeper.
```

**S1.3  Record `01e496/flowNexus` entry #2 A flow component that works**  
Date: 2026-10-02 (in the record's context). File: `flows/01e496/vision/flowNexus.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Psyche Fable 91ea9f.

> Right now I would like to have a flow component that works, that can launch flows, and that has hooks in the harnesses that send the right events to the flow component so that it can know the state of each flow.

-- psyche, typed, 2026-10-02, heard by 91ea9f.
```

**S1.4  Record `554e1a` entry #1 2026-10-29 — The Nexus is called Flow Nexus; a flow is one run of a metaflow or a single FML flow**  
Date: 2026-10-29 (in heading). File: `flows/554e1a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 21:05 and 21:11, comments on Flow, whole (https://claude.ai/artifact/M4E2xhh4GycRo11GkPNJ1D) by the Psyche flow Primary 30fc30, relayed through Psyche core Tertiary b195f0 and Secondary 9b514f.

Okay, first, let's call this Flow Nexus instead of Flow, because I really want us to say Flow Nexus when we're talking about the Nexus, so that we don't get confused with a "flow."

On "A flow is one run of a metaflow": This is incorrect because a flow could be one run of a metaflow, or it could be a single FML flow. At least in the long term, we have that concept also, but I think we really need to define this long-term/short-term thing. I'm going to get these comments sent to core, and I don't want this proposal to be redone yet. I just want to specify first how we are going to take care of long term/short term, and then, once that's done, we should revisit this.
```

**S1.5  Record `73b5d8` entry #1 2026-10-29 — The Flow Nexus gives a flow its Flow ID; the evolution is reported**  
Date: 2026-10-29 (in heading). File: `flows/73b5d8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, in the Psyche core Primary chat 73b5d8, after the fresh Primary bound its own seat by command and reported the repairs in motion.

And I'm still not hearing about the new Flow Nexus, which should fix the message format. I don't see any reason why the Flow Nexus cannot give you your Flow ID and why you have to spend your own energy to do something so trivial.

Context: the second half of the same order, his words of 14:24, recovered by the remembering check of primary-zr42.

Then I will review your open proposals.
```

---

## S2 Flow is the Nexus that manages flows; a flow is one run of a metaflow; a requested flow is launched; Flow holds the lock

Module lines 11-11:

```text
Flow is the Nexus that manages flows. A flow is one run of a metaflow; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.
```

Landing history (git log -S on the phrase `A flow is one run of a metaflow`, `Flow holds the lock on flows`, `launched, properly and surely`, oldest first):

- a83cbd0 2026-10-19 Edit flow vision: drop two sentences, name a flow a run of a metaflow
- 72149ef 2026-10-07 Move Psyche skill sources under skills

Provenance note: The clause 'a flow is one run of a metaflow' was named by him 2026-10-19 17:27 ("one run of a metaflow not a voice") and is corrected by him on 2026-10-29: a flow can also be a single FML flow (see last section). b7a16a had said the same on the vocabulary module ("A flow is not only one run of a metaflow"). The 'launched, properly' clause answers his 2026-10-02 correction of 'launched at once'.

**S2.1  Record `e06e4c07/archive-flowDaemon` entry #1 2026-08-19 — Curriculum is rewritten as a Nexus; the flow repo is the machinery; skills live in another repo; a few basic skills in flow replace the built-in harness prompt; the name stays flow; research requested**  
Date: 2026-08-19 (in heading). File: `flows/e06e4c07/vision/archive-flowDaemon.md`  
Words and context: verbatim at S1.2 above (long record, not repeated).

**S2.2  Record `01e496/flowLifecycle` entry #1 A flow the living asks for is launched**  
Date: 2026-10-02 (in the record's context). File: `flows/01e496/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by fe945a; the living correcting fe945a's proposed line "A flow the living asks for is launched at once".

> No that's not what I said. You didn't understand what I want. I didn't say "launched at once." It's launched properly but it is launched. Right now you're not going to launch anything. You weren't going to launch anything so you had given up on the order I gave.

-- psyche, typed, 2026-10-02, heard by fe945a.
```

**S2.3  Record `91ea9f/flowLifecycle` entry #1 A requested flow exists when the living returns**  
Date: 2026-10-02 (in the record's context). File: `flows/91ea9f/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by the launch brief as today's lesson; heard in fe945a, not by this flow.

> "I asked for it so it should be done. That's how I want the system to work: if I ask for a new flow, when I come back there's a new flow. There never ever is a new flow."

-- psyche, typed, 2026-10-02, fe945a (relayed).
```

**S2.4  Record `fe945a/flowLifecycle` entry #2 A flow he asks for exists when he comes back**  
Date: 2026-10-02 (in the record's context). File: `flows/fe945a/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to Psyche Opus fe945a an hour after ordering the psyche stack restarted, when no new psyche flow had been launched.

> I asked for it so it should be done. That's how I want the system to work: if I ask for a new flow, when I come back there's a new flow. There never ever is a new flow.

-- psyche, typed, 2026-10-02, fe945a.
```

**S2.5  Record `fe945a/flowNexus` entry #1 The anatomy of Flow in Ethos: Flow holds the lock on flows, flows addressed by name, the flow id in words**  
Date: 2026-10-02 (in the record's context). File: `flows/fe945a/vision/flowNexus.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to Psyche Opus fe945a after correcting its proposed skill line on launching flows.

> I want to develop the anatomy of ethos for the most important component, which is, I don't know, I think, flow. We're having such a hard time handling flows and locking them. Flow could have the lock on the flows so that we can lock it and also address it by name instead of by Flow ID. I'd also like the Flow ID to be converted into words.

-- psyche, typed, 2026-10-02, fe945a.
```

**S2.6  Record `e5a0bc` entry #3 The lock: needed to roll a metaflow over into a new flow; later Message uses it to know whether a message can reach a flow**  
Date: 2026-10-07 (none in the record; date of the file's first commit). File: `flows/e5a0bc/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same message.

> There's also the concept of the lock, which we need in order to roll over a metaflow when it's spawning itself into a new flow. We need to be able to lock. I can't really see exactly what function this fills now but I know that it fills a function when message uses the lock later on. We don't have to make message right now but we will eventually and that lock will be useful in order to know whether the messages can or cannot reach a certain flow.

-- psyche, typed.
```

**S2.7  Record `d68c82/archive-flow` entry #1 A flow is one run of a metaflow**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «Flow's vision», the current vision/flow.md line "A flow is one run of a voice".

> The run: one run of a metaflow not a voice. Let's get rid of that voice vocabulary. Consistency

-- psyche, book comment, 2026-10-19T17:27, input mode not shown.
```

**S2.8  Record `b7a16a` entry #5 Flows outside metaflows**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/b7a16a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the proposed definition of Flow in the vocabulary module.

"A flow is not only one run of a metaflow because there are other types of flows that are not parts of metaflows, which we've talked about before."

-- psyche, STT.
```

**S2.9  Record `b7a16a` entry #4 A flow is one kind of flow**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/b7a16a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the book Models as a set of variants, whose type held main flows and subflows together.

"A flow doesn't have a main flow. A flow is either a main flow or is a subflow or is maybe another kind of flow. A flow doesn't have a main flow and another flow because that would be two flows."

-- psyche, STT.
```

**S2.10  Record `d4ae97` entry #6 A flow is not always a metaflow**  
Date: 2026-10-07 (in the record's context). File: `flows/d4ae97/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on "Flow" in the metaflow record, section 1.

> A flow could exist and not be a metaflow so this structure is wrong. I guess you could make it an optional metaflow. What are we trying to show here? The only thing we need is for us to know that a flow is a metaflow. If a flow is a metaflow we'll be addressing it by its long-term metaflow name. There are flows that are not metaflows so I don't think this structure is appropriate. Anyway I haven't read the whole thing. I still have to get to the memory specification but I wanted to point that out.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.
```

**S2.11  Record `554e1a` entry #1 2026-10-29 — The Nexus is called Flow Nexus; a flow is one run of a metaflow or a single FML flow**  
Date: 2026-10-29 (in heading). File: `flows/554e1a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 21:05 and 21:11, comments on Flow, whole (https://claude.ai/artifact/M4E2xhh4GycRo11GkPNJ1D) by the Psyche flow Primary 30fc30, relayed through Psyche core Tertiary b195f0 and Secondary 9b514f.

Okay, first, let's call this Flow Nexus instead of Flow, because I really want us to say Flow Nexus when we're talking about the Nexus, so that we don't get confused with a "flow."

On "A flow is one run of a metaflow": This is incorrect because a flow could be one run of a metaflow, or it could be a single FML flow. At least in the long term, we have that concept also, but I think we really need to define this long-term/short-term thing. I'm going to get these comments sent to core, and I don't want this proposal to be redone yet. I just want to specify first how we are going to take care of long term/short term, and then, once that's done, we should revisit this.
```

---

## S3 Flow is for starting flows cheaply

Module lines 13-13:

```text
Flow is for starting flows cheaply: clean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.
```

Landing history (git log -S on the phrase `starting flows cheaply`, `cornerstone of the system`, `taken down as easily`, oldest first):

- 2faca02 2026-10-15 vision-flow: what Flow is for

Provenance note: Landed 2faca02 2026-10-15 'what Flow is for'; the words 'cornerstone', 'clean lean flows, specialized flows, or refreshing flows' are from the 2026-10-14 record; 'clean, on-point context ... higher quality' from the 2026-10-13T17:52 record.

**S3.1  Record `d68c82/archive-flow` entry #8 Clean specialized flows for quality**  
Date: 2026-10-13 (in the record's signature or body). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> Flow Nexus, the short-term and long-term flow tool, really needs to be worked on harder and more diligently so that:
> - it's cheap to start specialized flows
> - we can get higher-quality output
>
> It feels like right now, for example, removing the artifact tool from most flows makes sense, since most of them won't be involved in dealing with artifacts (since we'll have a flow for that). I feel like we're getting low-quality output from flows that have too much noise in their context. ...
>
> The most important improvement we need to focus on right now is getting a proper flow tool that can actually start well-trained flows for specific purposes and then easily take them down or spin them down. This does not end the topic but means that reactivating the topic would reactivate a new flow with a clean on-point context, which would yield much higher quality output.

Context: comment on «Three lines from the chat, second edition», Proposal 4.
-- psyche, STT, 2026-10-13T17:52.
```

**S3.2  Record `d68c82/archive-flow` entry #14 2026-10-14 — Flow, Nexus and Ethos together; Flow is the bootstrap**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> We're developing the Flow, the Nexus architecture, and Ethos at the same time. There are three aspects, right?
> - the language aspect
> - the runtime architecture
> - that component itself, [Flow], which is probably the most important component to bootstrap
>
> Bootstrap persona, the meta harness, since starting flows like clean lean flows, specialized flows, or refreshing flows is a central part, a cornerstone, of this system.

-- psyche, STT. Transcription corrected: "low" → "Flow".
```

**S3.3  Record `d68c82` entry #4 Lean flows, cheap to start**  
Date: 2026-10-13 (in the record's signature or body). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> We need to nail down and deploy a system that can start a very lean flow. Especially for the costly models like Fable and Astra, especially Fable, I don't want to feel constrained by the cost of starting a flow to start a new Fable topic.
>
> For all of this artifact tooling and all of this useless stuff, obviously I want to be able to use subagents if it does interact with anything in terms of reading files and calling tools (because in many cases the first tool call might not work or might not be getting the information). That information might involve calling more than one tool and I'd like to measure statistically, for what's been going on so far:
> - What's the ratio of cases in which a properly configured predefined subagent that requires minimal guidance would be less token-expensive, especially in terms of output but also input, in terms of how big the response is, which we can train the agent to do properly?
> - How many of the cases would it be more expensive for the main flow to use the subagent rather than just use the tool directly itself, given how many different tries and different tools and how much filtering had to be done on the output?
>
> I'd like to do some research on that. I really want to focus on talking about flow, flow design, flow deployment: an efficient flow tool for deploying efficient, specialized, concentrated, high-signal flows that focus more on design than tool calling.

-- psyche, STT, 2026-10-13.
```

**S3.4  Record `8475a9` entry #3 Fixing Flow is central: fresher, more frequent flows; metaflows focused on topics; software, not LLMs, for spawning**  
Date: 2026-10-06 (in the record's signature or body). File: `flows/8475a9/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same message. Relayed by d4ae97.

> I think fixing Flow is central to getting more efficient flows that are more on point with what they're supposed to do, so that we can spawn them fresher, more often, and have meta-flows that can focus on certain topics.
>
> I feel like I was getting more out of my flows when I was handling them manually. Right now God knows how long it's going to take you and the others to spawn a new Fable. We're still spending a lot of context just trying to. We're using LLMs to make up for a lack of software, which is bad.

-- psyche, STT, 2026-10-06, relayed by d4ae97.
```

**S3.5  Record `88475f` entry #2 A new job starts on a fresh flow with related training**  
Date: 2026-09-25 (in the record's context). File: `flows/88475f/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25, on moving the Flow 0.7 deploy away from a seat whose context was old.

> Yeah well, if his context is old and he's not going to be able to do a good job, when we start something like that we should start on a fresh flow with lots of related training.

-- psyche, STT, relayed by e51411.
```

**S3.6  Record `c637a5` entry #3 2026-10-27 — Good work comes from fresh flows, not from a core carrying unrelated context**  
Date: 2026-10-27 (in heading). File: `flows/c637a5/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, after I sent the rebuild order to the Mind cores.

> They should use fresh flows to do good work, right? If you sent the order to Mindcore to do something, but let's say he has 200,000 tokens of context that is completely unrelated to this, what do you think is going to be the result?
```

**S3.7  Record `d68c82/archive-flow` entry #33 A specialized flow with a large context is restarted fresh on its topic**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> So specialized flows that have large context are too old and should be restarted, right? They can stay right on topic with a fresh, clean, crystallized vision and only talk about this particular topic so they can have a better output.

-- psyche, typed.
```

**S3.8  Record `b7a16a` entry #1 Starting a flow**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/b7a16a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: a standing order to every flow, Psyche and Codex, to work without stopping until each of these holds.

"Starting a flow is as easy as kicking a rock with my foot. ... It's instant and there's no problem ever. ... It uses the latest context every time. ... No one can use it the wrong way. ... It never behaves in a weird way."

-- psyche, STT.
```

**S3.9  Record `9864c0` entry #1 Starting a flow is a minimal CLI call; agents are pre-described in configuration the daemon loads**  
Date: 2026-10-19 (in the record's context). File: `flows/9864c0/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Psyche core Tertiary 4201a3 as #psyches, 2026-10-19, order to the flow about reminders. Spoken to 4201a3.
"... make sure that the progress is being made on Flow so that it's working in every way that we want, deployed, easy to use, and requires a minimal CLI (with all the agents pre-described in configuration files which are loaded in the daemon, so that starting a flow is as easy as a 10-character CLI system call)."
Context: same day, clarification.
"And I'm not targeting the word, the number 10 here. I'm just being broad. I'm just saying it should be right fucking minimal for a standard flow."
-- psyche, STT.
```

---

## S4 A flow runs one model; the model is not always a language model; an agent is a whole being; many flows resemble a synthetic intelligence

Module lines 15-15:

```text
A flow runs one model, linear and very limited, and the model is not always a language model: it may be a System 1 model, an audio model or a video model. An agent is a whole being, a lot more than that. Many flows, properly structured and orchestrated, together resemble a synthetic intelligence, synthesized from human knowledge and mathematical probability.
```

Landing history (git log -S on the phrase `resemble a synthetic intelligence`, `System 1 model`, `linear and very limited`, oldest first):

- 4077058 2026-10-14 vision-flow: a flow is one linear chat; many flows resemble a synthetic intelligence
- 988800b 2026-10-11 vision-system-one: intelligence in the logic (approved 2026-10-11)
- 6c8e266 2026-10-19 Land flow vision book 89: vision/flow, vision/ethos, vision/nexus

Provenance note: Landed 4077058 2026-10-14 'a flow is one linear chat; many flows resemble a synthetic intelligence' and amended 2026-10-19 (6c8e266/a83cbd0) by his 17:28 comment that the model need not be an LLM. vision-raw/flowsNotAgents.md (2026-08-10, 2026-08-13) is the legacy ground for 'flows not agents'.

**S4.1  Record `vision-raw/flowsNotAgents` entry #1 2026-08-10 — sessions are flows; aspects, not individuals**  
Date: 2026-08-10 (in heading). File: `vision-raw/flowsNotAgents.md`  
Context and the living's words, verbatim as logged:
```text
> And I even want to use a different term than agents because it's
> misleading, because what I'm making this meta agent, if you will, is
> made up of all these smaller sessions. So we were just going to call
> it, I guess, a session or even then it sort of implies that there's
> an individual there, but it's more like a flow or a sub flow. … the
> names of the awareness, the shards of awareness, I want to change
> them because if I say realizer, it sounds like there's an individual
> there, whereas in fact, it's the realizing aspect. And, you know,
> even that all of this machinery … it's going to stay, but eventually
> I don't want the user to be extremely aware … the average user
> eventually won't even know that there are different aspects. … But I
> think the terminology is really important, not just for me, but for
> the … sub flows. To instinctively understand the concepts because
> they're named properly. And this is actually really a big part of it
> would go in spirit. Right. Something like about how naming things
> properly creates the right understanding of instinctive
> understanding or the, you know, it's easy to grasp. And it also is
> about not misunderstanding.

— psyche, 2026-08-10T18:49Z (Designer session c6b71b4c), dictated;
ellipses mark trims. The rulings carried: "agents" is misleading — the
meta agent is composed of smaller sessions, better called flows and
sub flows; the awareness shard names change from individual-sounding
nouns (Realizer) to aspect names (the realizing aspect); the aspect
machinery eventually becomes invisible to the ordinary user; proper
terminology exists so the flows themselves instinctively understand
the concepts. A Spirit capture on proper naming creating instinctive
understanding was requested — pending the psyche's approval of exact
wording before anything touches Spirit.

2026-08-13T14:14:14.480Z. Agent-authored context: appended here because
the psyche refined the existing ruling about naming awareness shards as
concepts rather than individuals.

> I want to change all shard names away from person-implying (realizer) to concept (realization).

2026-08-13T15:38:40.769Z

Agent-authored context: ruling on an awareness shard name and retirement.
Verbatim:

> there is no "assistance" role. only single words. that aspect is retired, delete it.

2026-08-13T15:38:40.769Z

Agent-authored context: ruling confirming an existing awareness shard name.
Verbatim:

> we already have realization

2026-08-13T15:38:40.769Z

Agent-authored context: ruling on an awareness shard name.
Verbatim:

> I also dont want infinitive verb like writing, even though it also qualifies as a noun, it is ambiguous. rename to composition.

2026-08-13T15:38:40.769Z

Agent-authored context: ruling on proposed awareness shards and reviewable stubs.
Verbatim:

> Create an Contemplation and Consideration. Propose simple awareness stubs for them that I will review. We also need an Implementation. propose all stubs
```

**S4.2  Record `e06e4c07/archive-flowsNotAgents` entry #1 2026-08-19 — an agent is a whole being; a flow is one linear LLM chat; artificial intelligence is a misnomer — synthetic intelligence**  
Date: 2026-08-19 (in heading). File: `flows/e06e4c07/vision/archive-flowsNotAgents.md`  
Context and the living's words, verbatim as logged:
```text
Design session `e06e4c07`, dictated (captured 2026-08-19T13:49+02:00),
closing the message that kept the name flow for the flow Nexus:

> It's not an agent because to me, an agent is more of a whole being,
> and a whole being is a lot more than a single LLM chat, which is
> linear and very limited. Whereas an entity, an artificial entity,
> which I think the word artificial intelligence is a misnomer. It's a
> synthetic intelligence. It's synthesized from human knowledge and
> mathematical probability. So a flow more accurately describes
> essentially an AI flow, right? Which is just one of the many flows
> that together, when properly structured and orchestrated, will
> resemble an artificial being or a synthetic intelligence.
```

**S4.3  Record `4ddc321d` entry #1 2026-08-26 — flow of thought; agent entails subjectivity**  
Date: 2026-08-26 (in heading). File: `flows/4ddc321d/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Ruling for the replacement base context, and the grounding of the
term itself:

> firstly: we will replace all occurence of sub/agent with sub/flow,
> with a line explaining what we mean by flow (perhaps by equating it
> with agent, since the model is probably trained to use this term,
> instructing him to use the flow terminology henceforth)
>
> the idea behind flow is simple; a flow of thought. An intelligence
> isnt a single flow of thought, it is a multitude of flows. so using
> the term "agent", which entails subjectivity, when speaking of a
> single flow does not correspond with reality. Hence the need to
> change the vocabulary, which will result in a more accurate model of
> reality.

Flow reading, not the psyche's words: this grounds the existing
workspace term "flow" — subjectivity belongs to the intelligence (the
multitude), not to any single flow; "agent" misplaces it onto the
single thread. It may deserve distillation into the Curriculum
vocabulary entry for flow.
```

**S4.4  Record `d68c82/archive-flow` entry #13 2026-10-14 — a flow and synthetic intelligence (landed with the misnomer clause removed)**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> Take out the part about artificial intelligence being a misnomer. That's not necessary.
> Otherwise it's good. Land it.

-- psyche, STT, book comment on «Flow philosophy and artifacts» P1.
```

**S4.5  Record `d68c82/archive-flow` entry #28 A flow's model need not be an LLM**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on the current line "A flow is one LLM chat, linear and very limited; an agent is a whole being, a lot more than that."

> It could be a system one also. It doesn't have to be an LLM so that's not necessarily true. Also it could be an audio or a video model or whatever.

-- psyche, book comment, 2026-10-19T17:28, input mode not shown.
```

---

## S5 The Capsule

Module lines 17-17:

```text
The Capsule is the component that makes where a flow runs. Its first embodiment is the semi-sandbox: only the credential files are copied, everything else is recreated, with its own sockets and store, running light models. Later it encrypts the sensitive parts of the filesystem under a volatile key.
```

Landing history (git log -S on the phrase `The Capsule is the component`, `semi-sandbox`, `volatile key`, oldest first):

- 72149ef 2026-10-07 Move Psyche skill sources under skills

Provenance note: Landed with the module's Capsule paragraph; the first embodiment (credentials only copied, everything else recreated) is route (a) approved 2026-10-02, the volatile-key encryption is route (b), 'a design for later'. 'Its own sockets and store' is from 3ec648: "create and use a different socket". 'Running light models': 3ec648 testing record. No record found that words 'only the credential files are copied ... with its own sockets and store' as one statement; it is assembled.

**S5.1  Record `91ea9f/encapsulation` entry #1 The component that handles encapsulation is not the harness**  
Date: 2026-10-02 (in the record's context). File: `flows/91ea9f/vision/encapsulation.md`  
Context and the living's words, verbatim as logged:
```text
Said to this flow directly; intended for Psyche Opus fe945a before that seat closed. Context: a component being discussed with Opus whose name was tentatively "harness".

> "We already have a component called harness but I don't think that that's really what we're talking about because that would be our actual harness implementation. It's more like, I don't know. Maybe when we start Fable we ask him what would best represent the name of this component that basically handles the encapsulation side of things."

-- psyche, STT, 2026-10-02.
```

**S5.2  Record `91ea9f/encapsulation` entry #2 It is called Capsule**  
Date: 2026-10-02 (in the record's context). File: `flows/91ea9f/vision/encapsulation.md`  
Context and the living's words, verbatim as logged:
```text
Book comment on «The Capsule and the Semi-Sandbox», anchored to the Capsule heading.

> "Yeah I think I picked the right word. It's going to be called Capsule."

-- psyche, typed, 2026-10-02.
```

**S5.3  Record `91ea9f/encapsulation` entry #3 The volatile key is a later design: encrypt the sensitive parts of the file system**  
Date: 2026-10-02 (in the record's context). File: `flows/91ea9f/vision/encapsulation.md`  
Context and the living's words, verbatim as logged:
```text
Anchored to route (b).

> "This is a design for later on. It's something that will just encrypt the file system so that we are creating a sort of hardware-layer encryption security. It doesn't have to encrypt the whole file system, just the parts where we put sensitive stuff."

-- psyche, typed, 2026-10-02.
```

**S5.4  Record `91ea9f/encapsulation` entry #4 Credentials route (a) now, (b) later: approved**  
Date: 2026-10-02 (in the record's context). File: `flows/91ea9f/vision/encapsulation.md`  
Context and the living's words, verbatim as logged:
```text
> "Yes that's right. You have it right here."

-- psyche, typed, 2026-10-02.
```

**S5.5  Record `3ec648/capsule` entry #1 The semi-sandbox copies only the credentials**  
Date: 2026-10-02 (in the record's signature or body). File: `flows/3ec648/vision/capsule.md`  
Context and the living's words, verbatim as logged:
```text
Context: on testing the nexuses and flows outside the live system.

> "You could create and use a different socket. Just create the environment yourself. You can make this semi-sandbox. I know it's possible if you just reuse the same credentials and you just recreate everything else. The only thing you copy is the credentials then it'll work.
>
> If there is a credential rotation then we need to maybe use the new credentials that have been... I don't know. Somebody brought that up but I don't even know if it's a thing. For now let's just test it the simple way."

-- psyche, STT, 2026-10-02.
```

**S5.6  Record `42265e/capsule` entry #1 2026-10-03 — The semi-sandbox copies only the credentials**  
Date: 2026-10-03 (in heading). File: `flows/42265e/vision/capsule.md`  
Context and the living's words, verbatim as logged:
```text
Context: Fable 9fb0ad relayed the original 2026-10-02 record from flows/3ec648/vision/capsule.md while Field was extending the isolated Claude witness.

> You could create and use a different socket. Just create the environment yourself. You can make this semi-sandbox. I know it's possible if you just reuse the same credentials and you just recreate everything else. The only thing you copy is the credentials then it'll work.

-- psyche, STT. Original 2026-10-02; relayed by 9fb0ad on 2026-10-03.
```

**S5.7  Record `3ec648/testing` entry #1 Sandbox testing with light models, toward deployment**  
Date: 2026-10-02 (in the record's context). File: `flows/3ec648/vision/testing.md`  
Context and the living's words, verbatim as logged:
```text
> "I want everything to be better implemented and, if you can, developed into a sandbox testing system with light models. I want everything closer to or ready for deployment, tested in sandboxes if possible. If not you can use your own subagents to test those components to see if they work."

-- psyche, STT, 2026-10-02.
```

**S5.8  Record `5330c1/capsule` entry #1 2026-10-23 — what was called the Herdr is the capsule**  
Date: 2026-10-23 (in heading). File: `flows/5330c1/vision/capsule.md`  
Context and the living's words, verbatim as logged:
```text
Context: said while ordering a real-world test of Flow in a separate capsule; the Herdr is the terminal workspace every flow runs in.

> I think what I called the [Herdr] is the capsule, because we could change the [Herdr] for another backend.

-- psyche, STT. Transcription corrected: "herder" → "Herdr".
```

---

## S6 Herdr is one backend of the Capsule

Module lines 19-19:

```text
Herdr is one backend of the Capsule, the component that gives a flow its place to run; the backend may be exchanged.
```

Landing history (git log -S on the phrase `Herdr is one backend of the Capsule`, oldest first):

- 5b7b165 2026-10-23 Land Flow tonight proposals 1 and 2 (approved): Herdr one backend of the Capsule; a real-world test of Flow

Provenance note: Landed 5b7b165 2026-10-23 ('Flow tonight' proposals 1 and 2, approved).

**S6.1  Record `5330c1` entry #2 2026-10-23 — Mind takes the reimplementation for a real-world test, in a testing capsule**  
Date: 2026-10-23 (in heading). File: `flows/5330c1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said right after being told the Fable branch is final and unjudged. "Herder" is the Herdr terminal workspace; "Codex and Co." reads as Codex and company.

> I want [Mind] to take it for a test. We should create this code in Nix that allows us to run this real-world test that just uses a different [Herdr] pane and puts all of these testing flows in a different capsule. I think what I called the [Herdr] is the capsule, because we could change the [Herdr] for another backend.
>
> Do you understand what I'm saying? Let's get this actually tested with multiple flows: Codex and Co. and Claude, with cheap low-effort models, just sending each other messages, seeing if they can start flows, seeing if the prompts are right, the system prompts are right, the tools are right, what's maybe missing in terms of features, and then come back to reimplementation again.

-- psyche, STT. Transcription corrected: "mine" → "Mind", "herder" → "Herdr".
```

**S6.2  Record `5330c1/capsule` entry #1 2026-10-23 — what was called the Herdr is the capsule**  
Date: 2026-10-23 (in heading). File: `flows/5330c1/vision/capsule.md`  
Context and the living's words, verbatim as logged:
```text
Context: said while ordering a real-world test of Flow in a separate capsule; the Herdr is the terminal workspace every flow runs in.

> I think what I called the [Herdr] is the capsule, because we could change the [Herdr] for another backend.

-- psyche, STT. Transcription corrected: "herder" → "Herdr".
```

---

## S7 Flow manages metaflows; a metaflow is one address; default topic core

Module lines 21-21:

```text
Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.
```

Landing history (git log -S on the phrase `A metaflow is one address`, `the last topic to stand`, `keeps the machine going`, oldest first):

- ae0bc79 2026-10-11 vision-flow: metaflows, the core topic, the flow id, requests, layers, refresh (approved 2026-10-11)
- d0d194c 2026-10-11 vision-flow: only the approved wording stays; the rest returns to the book

Provenance note: Landed ae0bc79 2026-10-11 (approved 2026-10-11), amended 6c1763f 2026-10-28 (ghost hunt: 'never a flow' trimmed, 'the last topic to stand' kept). 'The default topic is core ... the last topic to stand' is the 2026-10-11 20:21 comment on 'Flow, whole, in ethos' (logged in 9457ab, 9519a1 and 875960).

**S7.1  Record `bad807/metaflow` entry #1 A Metaflow continues through several flows, one after another; it goes into the vocabulary and the component; a voice is a Metaflow with no known ending, and the ending can be a judgment call**  
Date: 2026-10-04 (in the record's signature or body). File: `flows/bad807/vision/metaflow.md`  
Context and the living's words, verbatim as logged:
```text
Context: typed in chat to this flow, after his comment on «Tertiary and quaternary voices».

> It's a matter of breaking down how many different long-running tasks there are, really, because otherwise flows are just going to be spawned for their particular goal. We could even have Fable started on this nonpermanent Metaflow. Let's call it a Metaflow. It's something that sort of continues through several flows, one after another, right? Let's put that in the vocabulary and into the component and everything.
>
> What we're calling a voice, really, is this: a Metaflow with no known ending. This ending could itself become a judgment call. For example the whole ethos design and implementation (design anyway) could be a viable flow of its own.

-- psyche, typed, 2026-10-04.
```

**S7.2  Record `8475a9` entry #2 The metaflow is a central concept; it was missed in «Flow spawning»**  
Date: 2026-10-06 (in the record's context). File: `flows/8475a9/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to the secretary 2026-10-06 after commenting on «Flow spawning». Relayed by d4ae97.

> I'd like to make the concept of a meta flow a central concept. I see that it hasn't been brought up so that's part of my vision that's being missed. I want that brought out.

-- psyche, STT, 2026-10-06, relayed by d4ae97.
```

**S7.3  Record `f768df` entry #1 2026-10-06 — Metaflows at the center**  
Date: 2026-10-06 (in heading). File: `flows/f768df/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: Said to secretary, STT; relayed by d4ae97 and 8475a9; originals flows/d4ae97/vision/flow.md and flows/8475a9/vision/flow.md.

> I'd like to make the concept of a meta flow a central concept. I see that it hasn't been brought up so that's part of my vision that's being missed. I want that brought out.

-- psyche, relayed as noted above.
```

**S7.4  Record `d4ae97` entry #15 A flow is aspect, topic and layer; the core topic is the hub of its aspect**  
Date: 2026-10-08 (in the record's signature or body). File: `flows/d4ae97/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> Let's get this Opus Flow prototype to know how to start. There are going to be different types, the main types, which are:
> - psyche
> - mind
> - field
>
> Those three aspects, psyche, mind, and field, I think, are even applicable for topics. If you have a psyche and then it has a topic, the non-topiced flows would just be the topic of core.
>
> We can have the focused starting point, basically the kernel, the first flows that sort of hold all of their aspect together. They think in the most general ways about psyche. They have an overview of all of psyche and all of the other psyche topics sort of go through the core. It's like there's this hub at the center, the psyche core, so it's a struct. It's just a struct.
>
> The first field is the aspect, [psyche, mind or] field:
> - Mind would be implementing, documenting things.
> - Field would be maintaining, debugging, deploying, using an actual mutating system, running commands such as `field` or `flow` to start new things or to wind things down that we didn't have hooks for, and automating wind down. Eventually Field is doing what we're trying to automate. It's kind of acting as glue for the system to run.
> - Psyche can also audit but it's a different kind of audit. It's like, does it conform to the design of the psyche? It's a more broad redesign-the-architecture kind of audit.
> - Mind is more like trying to find optimization and removing bad tests, replacing it with actual real-world emulation, like a runtime-based test.
>
> I also want this topic. The whole topic is testing. We can have a Psyche testing secondary flow or we can have a Mind Psyche, right? Mind Psyche in the sense of the Psyche component. The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably. I'm sure there's a library that can make sure something conforms to an English expression, a word, etc., if you break it down using the PascalCase logic, etc.

-- psyche, STT, 2026-10-08. Transcription corrected: "psyche minor field" → "psyche, mind or field".
```

**S7.5  Record `f5a6e9` entry #6 A passable vision for Flow on the current design, where the metaflow is the ancestor of the next; the launch scripts modified to match**  
Date: 2026-10-07 (in the record's context). File: `flows/f5a6e9/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said on 2026-10-07; relayed by Psyche Opus d4ae97.

> Let's get a passable vision for Flow using the current Flow design, where MetaFlow is the ancestor of the next. Let's modify the scripts that we're using now to launch all this.

-- psyche, STT, relayed by d4ae97.
```

**S7.6  Record `f5a6e9` entry #1 A voice is a permanent metaflow, one that may sleep and is woken by a message; the role is maybe a short camel-case string; the worker names are the old system**  
Date: 2026-10-07 (in the record's context). File: `flows/f5a6e9/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: his comment 1 of 9 on «Flow and the metaflow» (https://claude.ai/artifact/3zEZo31LLLBpX1gak6JmoW), 2026-10-07 18:32, on the passage "A flow has a flow id and a role, and may continue a metaflow. A role is a voice or a worker (read-trivial, write-ordinary, tester, book). A metaflow is the voice of the flow's own role, or a named subject." Relayed verbatim by Field db38f8 at his order.

> There's a bunch of things that are false in here. I guess you could say a flow always has a role if we describe a role as maybe some kind of short camelcase expression, a string. It just describes, I don't know. I'm not even sure that a flow always has a role but maybe.
>
> A role is a voice. That's not true. A role may be a voice or a worker. Read trivial. Right. No, no, no, no, no, no. This read trivial. Right. Ordinary.
>
> This stuff is just an old system and it doesn't really correspond with the new system. Metaflow is the voice. No, Metaflow is not automatically a voice. A voice is a permanent Metaflow. It's a Metaflow that might go to sleep but can always be woken in the sense that if a message is intended for it, flow would automatically... This isn't intended for the first version but eventually it would just trigger the flow to be spawned with the right context modules depending on the message.
>
> There would probably be some kind of a judgment, a judgment machine call. When I say judgment I mean, you know what I mean. It's not just LLM. It's not just LLM, there's more than just LLMs. It's thinking machine judgment and then you go on.
>
> Anyway you can see that I don't like your proposal. It feels like you just grabbed everything you could see and just threw it all in a pot and thought that it would make a nice meal but it tastes like shit.

-- psyche, STT, book comment, relayed by db38f8.
```

**S7.7  Record `d4ae97` entry #6 A flow is not always a metaflow**  
Date: 2026-10-07 (in the record's context). File: `flows/d4ae97/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on "Flow" in the metaflow record, section 1.

> A flow could exist and not be a metaflow so this structure is wrong. I guess you could make it an optional metaflow. What are we trying to show here? The only thing we need is for us to know that a flow is a metaflow. If a flow is a metaflow we'll be addressing it by its long-term metaflow name. There are flows that are not metaflows so I don't think this structure is appropriate. Anyway I haven't read the whole thing. I still have to get to the memory specification but I wanted to point that out.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.
```

**S7.8  Record `d4ae97` entry #7 Looking up by metaflow; a metaflow's flow history**  
Date: 2026-10-07 (in the record's signature or body). File: `flows/d4ae97/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comments on "FlowId" in the registry record, section 2 «The registry is Flow's Memory».

> That doesn't make any sense. How do I know which flow a metaflow is? I'm going to look up "by metaflow" and a flow isn't always a metaflow so this is missing the mark by a long shot.

> And what about the flow history of a certain metaflow? Maybe it doesn't go on forever. I could see a long-running voice. Actually I guess a voice is a variant of a metaflow. Probably eventually, not that we have to worry about this, we wouldn't want to keep the entire history. You could see a scenario in which this becomes unwieldy.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.
```

**S7.9  Record `f5a6e9` entry #3 History centred on the metaflow, not on Flow**  
Date: 2026-10-07 (none in the record; date of the file's first commit). File: `flows/f5a6e9/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: his comment 8 of 9, 19:05, on "History is not a third record. Each flow names its predecessor, so a metaflow's history is the walk back from its current flow." Relayed by db38f8.

> Again you're centering this around Flow and not Metaflow, which is not in line with my vision.

-- psyche, STT, book comment, relayed by db38f8.
```

**S7.10  Record `9457ab` entry #1 Heartbeat checking, with a fallback check later**  
Date: 2026-10-23 (in the record's context). File: `flows/9457ab/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living asks the Psyche core Secondary, 2026-10-23, whether the heartbeat checking mechanism is in place and working.

"Has the heartbeat checking mechanism been put into place and is it working? If not then you, primary, mi[nd], and field can coordinate on giving another shot. Perhaps you can have some sort of fallback to make sure that you check later to make sure that it has worked."
-- psyche, STT. Transcription corrected: "mine" → "mind".
```

**S7.11  Record `875960/archive-flow` entry #1 2026-10-11 — the voice concept is gone; the default topic is core, the permanent topic, the last to stand**  
Date: 2026-10-11 (in heading). File: `flows/875960/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Comment 1 on «Flow, whole, in ethos», 20:21, at the metaflow paragraph; relayed by core d68c82 through 9519a1.

> No we've gotten rid of the voice concept. Now it's just replaced by the core topic. One thing I did notice, which has maybe been fixed, is that the topic should always start with a small letter. It's uncapitalized. In other words we need a name for that. It's like a datomic name or something: a camelCase identifier. Anyway so far, the presentation proposal is good but we can't take out the voice part. Just replace it by saying that the default topic is `core` and that the `core` topic is essentially the permanent topic. It's the thing that keeps the machine going. It's the last topic to stand.

-- psyche, STT, relayed by 9519a1.
```

**S7.12  Record `554e1a` entry #1 2026-10-29 — The Nexus is called Flow Nexus; a flow is one run of a metaflow or a single FML flow**  
Date: 2026-10-29 (in heading). File: `flows/554e1a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 21:05 and 21:11, comments on Flow, whole (https://claude.ai/artifact/M4E2xhh4GycRo11GkPNJ1D) by the Psyche flow Primary 30fc30, relayed through Psyche core Tertiary b195f0 and Secondary 9b514f.

Okay, first, let's call this Flow Nexus instead of Flow, because I really want us to say Flow Nexus when we're talking about the Nexus, so that we don't get confused with a "flow."

On "A flow is one run of a metaflow": This is incorrect because a flow could be one run of a metaflow, or it could be a single FML flow. At least in the long term, we have that concept also, but I think we really need to define this long-term/short-term thing. I'm going to get these comments sent to core, and I don't want this proposal to be redone yet. I just want to specify first how we are going to take care of long term/short term, and then, once that's done, we should revisit this.
```

**S7.13  Record `445410/notion/metaflow-ethos` entry #1 The structure of the Ethos for the metaflows**  
Date: 2026-10-09 (in the record's context). File: `flows/445410/notion/metaflow-ethos.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Mind Quaternary 4ddfe1, which called it the living's exploratory discussion of the Metaflow Ethos and noted that "annex" is not settled.

> I wanna talk about the structure of the Ethos for um, the metaflows. They're going to be, each one uh, variant of either psyche, mind, or field. So all metaflows will essentially have an aspect. And then the struct, will contain their details, such as their- their- the name of their topic, right? Which will be a, a new type which I talked about yesterday, which is a... annex uh, I'm trying to come up with a name, maybe Opus actually made some suggestions or Fable.

-- psyche, STT, 2026-10-09, relayed by 4ddfe1.
```

---

## S8 A topic is an open enum

Module lines 23-23:

```text
A topic is an open enum: the constant topics, core among them, are fixed, and the users and the machine extend the set with camelCase identifiers.
```

Landing history (git log -S on the phrase `A topic is an open enum`, oldest first):

- 6c8e266 2026-10-19 Land flow vision book 89: vision/flow, vision/ethos, vision/nexus

Provenance note: Landed 9bba4bf 2026-10-12 and after. The open-enum wording is ecbc42's 2026-10-20 book comment (marked 'In the long term').

**S8.1  Record `ecbc42` entry #3 Topic names: an open enum in the long term**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ecbc42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: book comment on «The Nexus: questions for the living» (https://claude.ai/artifact/32uPikafAbLVMWfxaBinAW), relayed by Psyche core Tertiary, Proposal 13 (topic name kept exactly as written), 18:26; his first comment there was "Good. Mark short term".

"In the long term we want to support the open enum that I've talked about so that `core` would be a capitalized variant and there could possibly be more. But a custom topic could also be specified instead of one of the explicit variants. But we first need to support that in Ethos in order to do it."

-- psyche, STT, book comment.
```

**S8.2  Record `9fed42` entry #1 Topic is the core:Name camelCase type**  
Date: 2026-10-08 (in the record's context). File: `flows/9fed42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by 445410, after it wrote a title as { Psyche Core Secondary 445410 }; corrects the PascalCase topic in the 2026-10-08 record.

> but technically it should be uncapitalized core and ethos since theyre the core:Name type which is "camelCaseExpression" type with runtime checks when creating a new one

-- psyche, STT, 2026-10-09, relayed by 445410.
```

**S8.3  Record `875960` entry #2 2026-10-12 — four comments on «Flow, whole, in ethos, third edition»**  
Date: 2026-10-12 (in heading). File: `flows/875960/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment 1 sits on proposal 1's paragraph «A request reaching a metaflow is one of a closed set of types…».

> This is all good. Land it.

-- psyche, typed, 16:07, relayed by 9519a1.

Context: comment 2 sits on the item «Name» among the options for the camelCase identifier type (ruling 3); he notes it is used across dialects.

> Well if we create a special thing and we call it a name or we call it a word, you're never going to know when I'm talking about it. Those are silly suggestions. We need something that somehow embodies what we're trying to do. This is going to be used a lot here so whenever it's like an identifier, a word identifier, or an expression, it will be more than one word. Wherever we have something like a topic, a particular object that needs to be identified by agents or humans, which is anything that's user-facing that needs to be named through judgment and has to be given a name. Obviously variants are great but we have to recompile everything to add one. It's essentially a variant that is created on demand and is a bit more descriptive. The fact that it doesn't start with a capital is how we differentiate it from variants. You could give a few different shots at how we could call this. It would go in some kind of shared library, maybe the [protos] library, because I think it could be used in more than one place, in more than one dialect. It would also do a check, which is interesting. Maybe this deserves its own full research, especially in terms of Rust libraries and executable size bloat. If you have a library of words or you use an external service, which I'm not a fan of, at least it should look like a word. Oh my God this is a perfect spot for a system1 AI call to use a cheap judgment on: Is this composed mostly? Is this made up of words? Is this a camel-case string made up of words, whether they're proper nouns or not? It's not a problem and then we would have, I guess, a certainty threshold. Brilliant. But then again maybe there's a cheap library that can do a quick check with a fallback on AI. That's also an interesting possibility: if there's something that's cheap, lightweight (in terms of runtime cost) and can, in many cases, give us an answer on whether or not these components are actual words programmatically, and then fall back to the AI in case of a negative.

-- psyche, STT, 16:12, relayed by 9519a1. Bracket [protos] as relayed.

Context: comment 3 sits on «the title of a thread:»; a question.

> What do you mean by thread?

-- psyche, typed, 16:13, relayed by 9519a1.

Context: comment 4 sits on the process object («Instant») in Flow's Library in the ethos file; the last comment, where he stopped reading.

> I see that you have the process object defined in the library for Flow but we should have a shared library that many components, that many nexuses, are going to use. This is because identifying the calling process of a CLI is something I would like to minimize the amount of code that needs to be rewritten for every CLI and increase the ease of cognition when reading the code as to what this is doing. Obviously this is done in the background whenever the CLI is used so none of it is actually user-facing in a sense or configurable. It's just something that happens and it may be on all CLIs. I'm not sure now but it's an interesting topic to eventually develop further. We should get Mind to put together a concept that can test whether or not this can actually work using Ethos and everything. We can test it on Flow. Let's give free rein to Fable and Astra to design something like this and implement it. Flow isn't even on in production so I'm not even worried about merging more into main. I'm also curious why we haven't been able to start using Flow Nexus so far, even though it's been a month or something, so I'd like to get an investigation on that.

-- psyche, STT, 16:21, relayed by 9519a1.
```

**S8.4  Record `f5a6e9` entry #7 The topic is a dense string: PascalCase of a certain number of words, with a checker**  
Date: 2026-10-08 (in the record's context). File: `flows/f5a6e9/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said 2026-10-08 on the type of a metaflow's topic; raw record d4ae97 vision/flow.md:181, which also says the metaflow is a struct whose first field is the aspect and that flows with no topic take the topic core. Relayed by 445410.

> The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably.

-- psyche, STT, relayed by 445410.
```

---

## S9 Psyche, Mind and Field have similar payloads and go under one: the metaflow

Module lines 25-25:

```text
Psyche, Mind and Field have similar payloads, and they go under one: the metaflow, whose aspect is Psyche, Mind or Field.
```

Landing history (git log -S on the phrase `similar payloads`, oldest first):

- 455d677 2026-10-16 Land ruled lines of «Flow: context modules and the prompt, 2nd edition»

Provenance note: The statement keeps 'similar payloads' from the 2026-10-07 speech (d4ae97, f5a6e9). The notion (2026-10-09) is thinking aloud and binds nothing.

**S9.1  Record `d4ae97/archive-flow` entry #4 Psyche, mind and field share one payload; psyche divides into spirit, intent and vision**  
Date: 2026-10-07 (in the record's signature or body). File: `flows/d4ae97/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> We're going to create this different flow type that is basically a meta flow. It is one of the four things and they have different types of payload but psyche, mind, and field have similar payloads. I don't know if they're going to be always the same but I think possibly that would be the case.
>
> I guess this is where we made the case to put them all under a certain umbrella since they have a similar payload. Their variant can be just one of the fields in that particular payload. The ethos, I guess, is more terse and the datom is not bigger because you already have the struct.
>
> What's the name that we put them all under, these three that are very similar, or are these going to actually diverge and take their own shape? Maybe they subdivide into their own subcategory. Oh my God, this is it. This is where I'm going. I'm actually trying to start a session to work on spirit and then I would have a session to work on intent and a session to work on vision. That's what they are so we don't need all of them at the same time.

-- psyche, STT, 2026-10-07.
```

**S9.2  Record `f5a6e9/archive-flow` entry #3 Metaflow kinds and payloads: four things; psyche, mind and field have similar payloads; sessions on spirit, intent, vision**  
Date: 2026-10-07 (in the record's context). File: `flows/f5a6e9/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said on 2026-10-07 on Flow's metaflow kinds; relayed by Psyche Opus d4ae97 with elisions marked by it.

> We're going to create this different flow type that is basically a meta flow. It is one of the four things and they have different types of payload but psyche, mind, and field have similar payloads. ... Their variant can be just one of the fields in that particular payload. ... What's the name that we put them all under, these three that are very similar, or are these going to actually diverge and take their own shape? Maybe they subdivide into their own subcategory. ... I'm actually trying to start a session to work on spirit and then I would have a session to work on intent and a session to work on vision. That's what they are so we don't need all of them at the same time.

-- psyche, STT, relayed by d4ae97.
```

**S9.3  Record `d4ae97` entry #15 A flow is aspect, topic and layer; the core topic is the hub of its aspect**  
Date: 2026-10-08 (in the record's signature or body). File: `flows/d4ae97/vision/flow.md`  
Words and context: verbatim at S7.4 above (long record, not repeated).

**S9.4  Record `dcd651/notion/metaflow` entry #1 2026-10-09 — Every metaflow is a variant of its aspect, carrying a struct of its details; the topic name is a new type**  
Date: 2026-10-09 (in heading). File: `flows/dcd651/notion/metaflow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living thinking aloud about the Ethos structure for metaflows; relayed by 4ddfe1 through 445410. The name for the topic type is not settled.

> I wanna talk about the structure of the Ethos for um, the metaflows. They're going to be, each one uh, variant of either psyche, mind, or field. So all metaflows will essentially have an aspect. And then the struct, will contain their details, such as their- their- the name of their topic, right? Which will be a, a new type which I talked about yesterday, which is a... annex uh, I'm trying to come up with a name, maybe Opus actually made some suggestions or Fable.

-- psyche, STT, 2026-10-09, relayed by 4ddfe1 and 445410. "annex" kept as heard; he is searching for the name.
```

---

## S10 A topic lives on; idle; waking is a judgment by a small model

Module lines 27-27:

```text
A topic lives on; when idle, its flows are turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its belief modules, so Flow knows what to start it with, together with the new input that warrants it.
```

Landing history (git log -S on the phrase `A topic lives on`, `judgment, made by a small model`, `A topic never dies`, oldest first):

- 6c1763f 2026-10-28 vision-flow: ghost hunt, the thing as wanted
- ae0bc79 2026-10-11 vision-flow: metaflows, the core topic, the flow id, requests, layers, refresh (approved 2026-10-11)
- d0d194c 2026-10-11 vision-flow: only the approved wording stays; the rest returns to the book
- 9bba4bf 2026-10-12 vision-flow: topics idle, topic name and flow id, requests and subscription

Provenance note: Landed 9bba4bf 2026-10-12 ('topics idle'); reworded 6c1763f 2026-10-28 (ghost hunt) from 'A topic never dies' to 'A topic lives on'. The record is 2026-10-11 20:23 (comment 2, broken off mid-sentence).

**S10.1  Record `9457ab` entry #1 Heartbeat checking, with a fallback check later**  
Date: 2026-10-23 (in the record's context). File: `flows/9457ab/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living asks the Psyche core Secondary, 2026-10-23, whether the heartbeat checking mechanism is in place and working.

"Has the heartbeat checking mechanism been put into place and is it working? If not then you, primary, mi[nd], and field can coordinate on giving another shot. Perhaps you can have some sort of fallback to make sure that you check later to make sure that it has worked."
-- psyche, STT. Transcription corrected: "mine" → "mind".
```

**S10.2  Record `875960/archive-flow` entry #2 2026-10-11 — a topic never dies; it goes idle; waking it is a judgment call, with its context modules**  
Date: 2026-10-11 (in heading). File: `flows/875960/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Comment 2, 20:23, same passage; the last sentence breaks off.

> Actually we should say that a topic never really dies. It just goes idle, meaning the flows can be turned off. If the topic comes back (in terms of the living touching on something that means we have to address this topic again), then there will be a judgment call. This is where the system 1 models can come in or even a small LLM call to judge whether or not we should wake a flow for this topic and which layer, if we do wake it. The topic could be in the flow nexus for now but maybe at some point in another nexus. The topic will be associated with certain context modules. If that topic is needed again, then we know what to wake it, what to start it, what context modules to start it with, along with whatever new input is coming in that warrants restarting the flow. Are the meta flow ...

-- psyche, STT, relayed by 9519a1.
```

**S10.3  Record `f5a6e9` entry #1 A voice is a permanent metaflow, one that may sleep and is woken by a message; the role is maybe a short camel-case string; the worker names are the old system**  
Date: 2026-10-07 (in the record's context). File: `flows/f5a6e9/vision/flow.md`  
Words and context: verbatim at S7.6 above (long record, not repeated).

**S10.4  Record `ecbc42` entry #2 A new topic starts only from vision or raw psyche that touches it**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ecbc42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: book comment on «The Nexus: questions for the living» (https://claude.ai/artifact/32uPikafAbLVMWfxaBinAW), relayed by Psyche core Tertiary, Proposal 8 (a request to a declared never-run metaflow starts it), 18:23.

"Well actually, no, not quite. I don't think [sic] we would first have to create a context module, at least have some vision for that, or get something approved for that particular topic. There would have to be at least some vision for that topic for it to be started automatically. Otherwise we wouldn't have anything to start it with. Well or arguably, there would have to be a significant (or not significant but clearly enunciated) psyche, raw psyche, raw vision that touches that topic. Then arguably that new topic could be started, if only for the sake of crystallizing the first vision for that topic based on the raw psyche that it is started with."

-- psyche, STT, book comment.
```

**S10.5  Record `36ac89` entry #2 What touches a topic goes to that topic's flow**  
Date: 2026-10-25 (in the record's context). File: `flows/36ac89/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
2026-10-25, to Psyche core Secondary 36ac89, right after his words on belief modules were passed to the core Primary.

> And obviously anything that touches a particular topic that we have a flow for should also go to that flow. And that should be part of your brief.

Correction, same exchange: the last sentence above reads "And that should be part of your [belief]." His word: "Belief not brief, belief."
Transcription corrected: "brief" → "belief".
```

**S10.6  Record `f5a6e9/messaging` entry #1 Every topic has its own flow; messages queue; each kind has a waking effect by the flow's state; a waking message drains the queue oldest first, delivered at the end of the prompt as a vector typed by variant**  
Date: 2026-10-08 (in the record's context). File: `flows/f5a6e9/vision/messaging.md`  
Context and the living's words, verbatim as logged:
```text
Context: said on 2026-10-08 while reading «Spirit edit incident»; relayed by Psyche Opus d4ae97, elision marked by it.

> I realized that every topic has its own flow. A topic could involve more than one skill but essentially that flow would be in charge of that whole topic. How do we efficiently queue any kind of update? If we're satisfied with the state of a certain topic at a given point, that flow should not be woken up. Let's suppose that another flow wants to tell that flow, "Congratulations, job well done," or that there's a notification for that flow because one of its branches was merged in the production branch. Things like that should not wake up the flow until there is a situation that arises, probably related to the living or the psyche (which is its representative in the machine), that wants to have to deal with this particular topic in any way (to find something out about the system because it's not behaving according to documentation, or because we want to investigate doing a new feature, etc.). That message actually has, given the particular state of that flow, the effect of changing the result. Different messages will have different flow-waking effects. When the message that does have the waking effect at that particular state in that flow comes in, it will also trigger checking the queue for that flow, so that the whole queue is checked in order, from the first received to the last. The message that just got in and triggered the queue will come in at the end of the prompt and it'll be a vector of all these objects, which are typed by variant name, obviously. We're designing Ethos here ...

-- psyche, STT, relayed by d4ae97.
```

**S10.7  Record `da2038` entry #28 A waking flow first looks for a past flow and its context size; a fresh flow is almost always better unless it is the same topic's continuation; a system one call asks whether the past is noise for the new message**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «Flow: sleeping and waking seats», figure under «A message wakes a sleeping seat», 2026-10-16 01:45; found unrelayed 2026-10-17.

> This chart is good, although it should say that if it has a transcript, the first thing it should do is look to see if it has a past flow. If it has a past flow, it should look to see if the context is too large. I could even see a flow coming in as a system one decision if it's borderline and it might have context that's good.
>
> Actually, to be honest, old flows should not be prioritized because they've probably gone to sleep, right? If they're not very old, we should do research on what the caches are with different providers and how long, usually, the stuff can be cached. It's not that long, so it's almost always going to be better to start a fresh flow, even if it has a past session, unless it's literally the continuation of that topic. It was just put to sleep because it wasn't addressed for a bit, whereby reusing that whole transcript actually makes sense because nothing in there is noise.
>
> This is where I see the system one call coming in to ask, "Is any of this noise in relation to the new message coming in?" This is why we need smart message composition. It's not just the straight-up living input. The living input has to be broken up and expanded, with each part having its own context and being sent to the right parts. If you're going to have machine intelligence, you're going to have to decompose, not machine thinking. If you're having machine thinking, you're going to have to decompose thoughts into parts, which is what Sema is. It decomposes language into parts.

-- psyche, typed, book comment.
```

---

## S11 A metaflow sleeps so a session not running keeps no harness

Module lines 29-29:

```text
A metaflow sleeps so that a session not running keeps no harness: as soon as its turn ends and the harness is idle, with nothing waiting in its queue, the harness closes; the transcript stays and the address stays.
```

Landing history (git log -S on the phrase `A metaflow sleeps so that`, `closes`, oldest first):

- d2dfc80 2026-10-18 Land «Flow: sleeping and waking seats» proposals 1, 2 and 5 in vision/flow.md
- 72149ef 2026-10-07 Move Psyche skill sources under skills
- d5fb9c1 2026-10-17 Land ruled lines of «Today, as psyche, 2nd edition»
- d5c7d3d 2026-10-19 Land inquiry vision, context-modules pointer, and CriomOS Services
- f94d063 2026-10-25 vision-flow: a restart does not wake; what a refresh carries
- af97799 2026-10-25 vision-flow: remove a restart does not wake, which misstated the living
- 9e03cd0 2026-10-25 vision-flow: restarting without waking
- d702b0b 2026-10-27 Remove inquiry as a belief kind; its crystallization rules move whole into vision/crystallization
- 0383b5a 2026-10-27 vision/book.md, vision/proposal.md: A proposal is made apart from the book that shows it

Provenance note: Landed d2dfc80 2026-10-18 (book 'Flow: sleeping and waking seats', proposals 1, 2 and 5). The RAM argument is from the 2026-10-15 spoken order.

**S11.1  Record `39bd0c` entry #4 No harness kept running for an idle session**  
Date: 2026-10-15 (in the record's context). File: `flows/39bd0c/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by Psyche Flow Secondary; said to the Flow Secondary directly, 2026-10-15.

> "It's really important that we finish and deploy the new Flow Nexus, especially so that when a session is not running, we don't have to keep a harness going. If we have a lot of topics, we're going to have too many harnesses running in the background, and that will just bog down the computer with excessive RAM usage."

-- psyche, STT.
```

**S11.2  Record `da2038` entry #13 The new Flow Nexus keeps no harness running for a session that is not running**  
Date: 2026-10-15 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to the Flow Secondary directly, 2026-10-15.

> It's really important that we finish and deploy the new Flow Nexus, especially so that when a session is not running, we don't have to keep a harness going. If we have a lot of topics, we're going to have too many harnesses running in the background, and that will just bog down the computer with excessive RAM usage.

-- psyche, STT.
```

**S11.3  Record `39bd0c` entry #5 Sessions marked non-running in the registry; resumed if young, else queued**  
Date: 2026-10-15 (in the record's context). File: `flows/39bd0c/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by Psyche Flow Secondary; heard by Field Core Primary 44cda5 on 2026-10-15.

> "Anyway, we need to design a way to keep track of these sessions in the registry so that we can mark them as non-running, so that when a message comes, they get started. They just get resumed if they're not too big, so the context size gets written. If it's not too big, the session gets restarted with the next message, basically, if it's important enough. Otherwise, maybe we can even implement the queue."

-- psyche, STT.
```

**S11.4  Record `da2038` entry #14 Sessions marked non-running in the registry; resumed if not too big, with the context size written**  
Date: 2026-10-15 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: heard by Field Core Primary 44cda5 on 2026-10-15 (its flows/44cda5/vision/sessions.md, published 5ca43f6); relayed to the Flow Secondary as an extension of the Flow lifecycle design.

> Anyway, we need to design a way to keep track of these sessions in the registry so that we can mark them as non-running, so that when a message comes, they get started. They just get resumed if they're not too big, so the context size gets written. If it's not too big, the session gets restarted with the next message, basically, if it's important enough. Otherwise, maybe we can even implement the queue.

-- psyche, STT, relayed by 44cda5.
```

**S11.5  Record `d68c82` entry #8 2026-10-14 — refresh thresholds, idle harnesses, and handover at cache expiry**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> at 128,000 tokens with Claude we get a warning. ... For Codex models the context window is much smaller and I think that at 96,000 tokens there's a warning and we start to contemplate refreshing. If the flow is working obviously we let it work and if it keeps working we let it work even past compaction.
>
> If it works so much that it compacts, eventually in the long-term vision we would have some kind of a check to make a judgment as to whether maybe the topic was misguided.
>
> For sure at 150,000, 160,000 tokens on OpenAI's models, we're seriously looking at refreshing, and the same for Claude at 200,000.
>
> It would be cool if we could strip down some of these Clojure flows so that they're way more efficient to spawn.

> in the long-term vision, if a flow has just been sitting idle for some time, we can turn off its harness. When the system is properly configured, if a request needs to reach a certain flow (which is not up and running in a harness), then the flow would just restart that flow or start a fresh one.
>
> Claude could just tell us the cache is going to expire instead of compacting. Then we would ask for the model to do a handover to produce a handover and that way we could train how we want our handover to be, which is essentially our own form of compaction.

-- psyche, STT, book comments on «Situation, 14 October».
```

**S11.6  Record `da2038` entry #26 Only core keeps an always-open session; core sessions are kept fresh and restarted at an age; the other flows may be down and are addressed through core**  
Date: 2026-10-17 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: direct message, 2026-10-17, after seeing how large the open Secondary sessions had grown.

> We have to avoid leaving these sessions open like that. I really only need core to keep running an always-open session. ... can we just restart the flow infrastructure with the new flow, Nexus, and CLI, and then use that to improve the rollover mechanism? We would need a way to make sure that there are always core sessions, essentially in a fresh state, so they're not too old. If they get to a certain age, they get restarted so these core sessions are available on [Mind, Field] and Psyche. For the others if they're not running, it's okay. I can address them through the core, right?

-- psyche, STT. Transcription corrected: "minefield" → "Mind, Field".
```

**S11.7  Record `7328f4/hooks` entry #2 Seats move to a new harness by hooks, one at a time as they go idle**  
Date: 2026-09-30 (in the record's signature or body). File: `flows/7328f4/vision/hooks.md`  
Context and the living's words, verbatim as logged:
```text
Context: Comment by the living on Psyche Fable's book "What Waits on You", anchored on "Refresh every flow, one at a time." Read by this flow from the page.

> Yeah obviously, the seats are not going to be cut off and we're going to describe a whole cascade of events and how this will take shape as the implementation gets more sophisticated. Essentially we want to avoid polling, which means we're going to make this hook-based. When an order comes in, this will be controlled by Flow obviously. When that order comes in, we need to upgrade the harness. Then sessions can be reloaded in the new harness one at a time as they go idle.
>
> As soon as the session goes idle, the hook kicks in. It gets locked for the next order tab update [sic], which essentially locks it from getting sync messages, right? It would wait until it stops because the restart will happen and then the message will just come through. This will tie into how context size will essentially start triggering the unwind. Then we'll have a whole way of passing the right transcript, either passing it over or selecting what transcript to pass depending on what the next flow will specialize in.

-- psyche, STT (page comment, 2026-09-30T18:47). "next order tab update" kept as heard.
```

**S11.8  Record `28f6f9` entry #1 Interpretation accepted: ordinary empty-queue refresh may sleep**  
Date: 2026-10-23 (in the record's context). File: `flows/28f6f9/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: Retrospective raw capture from the originating transcript after
verifying the exact user record. Origin transcript:
`/home/li/.codex-next-8mkkxq293hk2/sessions/2026/10/23/rollout-2026-10-23T17-42-22-01a16b24-e55c-7413-9005-5ad28f6f9d95.jsonl`, ordinal `496`, timestamp
`2026-10-23T23:49:34.855Z`.

> Interpretation accepted: ordinary empty-queue refresh may sleep; no successor-for-all. Proposed typed policy remains per-declaration Continuity.[ OnDemand Maintained ]; initial Maintained proposal specifically Psyche core Primary, not all core seats. Remaining idle-harness availability fork sent to Psyche flow Primary for its Secondary/living book; no new ruling claimed. Lifecycle owner notified, independent terminal cleanup proceeds. Use exact address policy, not inferred layer checks.

-- psyche, STT.
```

---

## S12 Topic name camelCase; flow id is the hash of the session id; caller identified by process; self-refresh

Module lines 31-31:

```text
A topic's name is a camelCase identifier, uncapitalized. Short term, it is kept exactly as written: Flow refuses a name that is not one and never lowers its capitals, so primaryCommitting stays primaryCommitting. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id. The flow id stays the hash; its word form waits for a later version. Long term, the flow id is also written in three words, which convert back to the hash. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. Every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.
```

Landing history (git log -S on the phrase `camelCase identifier, uncapitalized`, `kept to six characters`, `calling process`, `three words`, oldest first):

- ae0bc79 2026-10-11 vision-flow: metaflows, the core topic, the flow id, requests, layers, refresh (approved 2026-10-11)
- d0d194c 2026-10-11 vision-flow: only the approved wording stays; the rest returns to the book
- 9bba4bf 2026-10-12 vision-flow: topics idle, topic name and flow id, requests and subscription
- dde8584 2026-10-17 Flow vision: title as datom struct, six-character flow id, drop ancestor-naming sentence
- 67d358d 2026-10-14 vision-flow: land df159a book 12 Proposals 1 and 3
- 2d9fbb6 2026-10-19 Land flow vision book 3: one-call start, presentation, refresh by model threshold, compaction at continuous work, subflows wording
- 41c5df4 2026-10-23 Add compensation:book-making: the book source form the checker and builder accept, deployed until the living reviews it
- 169f5f1 2026-10-23 book-making: code lines within 52 characters
- 6c8e266 2026-10-19 Land flow vision book 89: vision/flow, vision/ethos, vision/nexus

Provenance note: Landed ae0bc79 / 9bba4bf / dde8584 (2026-10-17: 'six-character flow id') / 51731e8 (2026-10-20: 'topic name kept as written (short term)'). The word form of the flow id ('three words') is long term and still waits (01e496 2026-10-02, ebbe30 2026-10-09). The 'chosen before the flow starts' sentence is 5578cc 2026-10-03T16:17 and c068b8 2026-10-21T20:04; the living's 2026-10-29 words (73b5d8) say the Nexus gives a flow its Flow ID.

**S12.1  Record `9457ab` entry #1 Heartbeat checking, with a fallback check later**  
Date: 2026-10-23 (in the record's context). File: `flows/9457ab/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living asks the Psyche core Secondary, 2026-10-23, whether the heartbeat checking mechanism is in place and working.

"Has the heartbeat checking mechanism been put into place and is it working? If not then you, primary, mi[nd], and field can coordinate on giving another shot. Perhaps you can have some sort of fallback to make sure that you check later to make sure that it has worked."
-- psyche, STT. Transcription corrected: "mine" → "mind".
```

**S12.2  Record `ecbc42` entry #3 Topic names: an open enum in the long term**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ecbc42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: book comment on «The Nexus: questions for the living» (https://claude.ai/artifact/32uPikafAbLVMWfxaBinAW), relayed by Psyche core Tertiary, Proposal 13 (topic name kept exactly as written), 18:26; his first comment there was "Good. Mark short term".

"In the long term we want to support the open enum that I've talked about so that `core` would be a capitalized variant and there could possibly be more. But a custom topic could also be specified instead of one of the explicit variants. But we first need to support that in Ethos in order to do it."

-- psyche, STT, book comment.
```

**S12.3  Record `9fed42` entry #1 Topic is the core:Name camelCase type**  
Date: 2026-10-08 (in the record's context). File: `flows/9fed42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by 445410, after it wrote a title as { Psyche Core Secondary 445410 }; corrects the PascalCase topic in the 2026-10-08 record.

> but technically it should be uncapitalized core and ethos since theyre the core:Name type which is "camelCaseExpression" type with runtime checks when creating a new one

-- psyche, STT, 2026-10-09, relayed by 445410.
```

**S12.4  Record `da2038` entry #20 Every pane, tab and representation of a flow is named by the datom struct of aspect, topic and layer with the flow ID; topic names uncapitalized**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, after commenting on «Drawing ideas»; relayed to Psyche Core Secondary by the Tertiary, then to da2038 by Field Core Secondary as #psyche, 2026-10-16, typed as received.

> I commented on drawing ideas and you should be restarted as psyche core tertiary. Don't forget that the topic name is uncapitalized so core is uncapitalized, ethos should be uncapitalized, and all of these topics should be uncapitalized.
>
> It looks like the format that's used for Codex is different. Maybe it's because of how I'm seeing it and there are different applications but I like the name of every pane, every tab, everything that represents this flow to be just this triple field struct in datom format (or I guess it's quadruple with the flow ID).

-- psyche, STT, relayed by Field Core Secondary.
```

**S12.5  Record `7c89aa/flow-ids` entry #3 Topic names are uncapitalized; every pane and tab is named by the flow's datom struct (2026-10-16)**  
Date: 2026-10-16 (in heading). File: `flows/7c89aa/vision/flow-ids.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, after commenting on the book "drawing ideas", spoke this to the Tertiary.

> I commented on drawing ideas and you should be restarted as psyche core tertiary. Don't forget that the topic name is uncapitalized so core is uncapitalized, ethos should be uncapitalized, and all of these topics should be uncapitalized.
>
> It looks like the format that's used for Codex is different. Maybe it's because of how I'm seeing it and there are different applications but I like the name of every pane, every tab, everything that represents this flow to be just this triple field struct in datom format (or I guess it's quadruple with the flow ID).

-- psyche, typed.
```

**S12.6  Record `01a03d6e/flowIdentity` entry #1 2026-08-26T14:22:01.126Z — use the flow ID and assign it on the lock**  
Date: 2026-08-26 (in heading). File: `flows/01a03d6e/vision/flowIdentity.md`  
Context and the living's words, verbatim as logged:
```text
> I want to tie in the flow ID, which we also call the session ID, the short hash which identifies a session.

> I think six characters of the part which is not repetitive, if there is a repetitive part across sessions, six characters would be plenty.

> And then we would use that flow ID I would call it

> So this flow ID would be assigned on the lock.

Context (agent-authored, separate from the psyche's words): The six-character form is a preference to investigate against actual harness identifiers and collision risk, not yet a settled derivation rule.

— psyche, source-event timestamp `2026-08-26T14:22:01.126Z`; typed message record timestamp `2026-08-26T14:22:01.126Z`; root session UUID `01a03d6e-5cb8-7b60-b573-7f59413bc18e`; transcript provenance `/home/li/.codex/sessions/2026/08/26/rollout-2026-08-26T11-37-18-01a03d6e-5cb8-7b60-b573-7f59413bc18e.jsonl`, records 2268 (typed user message) and 2269 (user-message event).
```

**S12.7  Record `01a05826/flowIdentity` entry #4 2026-08-31T14:52:36.170Z — use six characters and extend collisions**  
Date: 2026-08-31 (in heading). File: `flows/01a05826/vision/flowIdentity.md`  
Context and the living's words, verbatim as logged:
```text
> Then let's use 6 chart. Collisions are not a security risk anyway. We could warrant that a flow that tries to create its directory in the flow log and finds out that it would check first. It would create a small tool that can do that. It would check if that ID is available. I guess it could even check it when it returns the idea to the flow asking for it, sort of like a just a pre-checkup. If it does find a collision, then it would just add one or two extra characters in its own. The collision is not a problem, really, as long as the IDs stay unique in that the first collision just uses a longer ID and then therefore stays unique.

Context (agent-authored, separate from the psyche's words): In the surrounding discussion, “6 chart” appears to mean six characters; the original wording is preserved because the message arrived as typed text.

-- psyche, typed.
```

**S12.8  Record `01a05826/flowIdentity` entry #5 2026-08-31T14:52:53.494Z — keep the reference straightforward**  
Date: 2026-08-31 (in heading). File: `flows/01a05826/vision/flowIdentity.md`  
Context and the living's words, verbatim as logged:
```text
> We can't convert the ID because the reference has to be straightforward. We don't want to introduce complexity between having to convert back and forth, like if an agent is looking for a certain transcript. I guess if you have the tool, I don't see it as absolutely necessary to have to convert.

-- psyche, typed.
```

**S12.9  Record `e1953c/flowIdentity` entry #2 The first two characters name the flow cluster, the triad; the session part is the first four characters of the session id**  
Date: 2026-09-14 (none in the record; date of the file's first commit). File: `flows/e1953c/vision/flowIdentity.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living could not find the successor session in the Claude remote session index and said the flow id shown was wrong. Clarifies the earlier six-character statement. The rest of the message is a working instruction (enable remote control on the successor session), not logged.

> What I meant was we shorten the session ID to the first 4 characters we were using before, instead of 6. Actually, the cluster, or the meta, what we could call it, the flow cluster, right? The 3 usually is just a triad: 3 main flows, each running on 3 different models with different prompts. The ID that we assign internally, eventually, is what the spec is: we use the first 2 to identify the cluster, so that at a glance you can see which codex and Claude belong together.

-- psyche, STT.
```

**S12.10  Record `fe945a/flowNexus` entry #1 The anatomy of Flow in Ethos: Flow holds the lock on flows, flows addressed by name, the flow id in words**  
Date: 2026-10-02 (in the record's context). File: `flows/fe945a/vision/flowNexus.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to Psyche Opus fe945a after correcting its proposed skill line on launching flows.

> I want to develop the anatomy of ethos for the most important component, which is, I don't know, I think, flow. We're having such a hard time handling flows and locking them. Flow could have the lock on the flows so that we can lock it and also address it by name instead of by Flow ID. I'd also like the Flow ID to be converted into words.

-- psyche, typed, 2026-10-02, fe945a.
```

**S12.11  Record `ebbe30/metaflow-naming` entry #1 Topic flows: psyche::{topic}, the layer, then the word-based flow id**  
Date: 2026-10-09 (in the record's context). File: `flows/ebbe30/vision/metaflow-naming.md`  
Context and the living's words, verbatim as logged:
```text
Context: 2026-10-09; starting a Fable and an Opus on Flow and on Ethos.

> I would like to get a fable on Flow and a fable on Ethos, and a fable on another topic, but let's just start there: a fable and an opus. Let's get the vision together. Even if some of it is raw, let's use the recent vision and the one that's been repeated a lot, which hasn't been overridden by newer decisions or statements.
>
> Start these two topic flows with the psyche::{topic}, either core, flow, or ethos, and then the layer: primary and secondary. There are three things. We can put the flow ID after that, although that might be a bit long, but let's try it. I would like the word-based flow ID, but maybe Astra can make a tool, a [Clojure] tool, to do the conversion between the first 33 bits of the identifier we use for the harness and the word thing. It can get a regular expression back so that we can find which session from the list of transcript files we have, or maybe we have a list of the alpha-numerical ID somewhere in the database, or maybe we just make a registry in the database.

-- psyche, STT, 2026-10-09. Transcription corrected: "closure" → "[Clojure]".
```

**S12.12  Record `875960/archive-flow` entry #3 2026-10-11 — the flow id is the harness's session id hash, so a transcript is found from it**  
Date: 2026-10-11 (in heading). File: `flows/875960/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Comment 3, 20:25, at the flow-id paragraph; a question, answered by this flow.

> We need the hash from the harness so we have to start the harness before we get the flow ID, I think. I don't know why this got turned around here unless we're not using the harness hash anymore. There are different parts of the session ID depending on the harness, which is supposedly random, and that's what we're using. I don't know why now the proposal is that we create a hash before. We've been using the session ID hash so that we can find a transcript easily from the flow ID. Is my idea stupid somehow or why do you think it's better to not do that?

-- psyche, STT, relayed by 9519a1.
```

**S12.13  Record `875960/archive-flow` entry #5 2026-10-11 — no claimed id: the caller is identified programmatically**  
Date: 2026-10-11 (in heading). File: `flows/875960/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Comment 6, 20:32, at the refresh paragraph. (Comment 5, 20:30, asked what "weeds no path the writer calls" meant; the sentence was "reads no path a caller writes"; answered, not vision.)

> Well if it doesn't trust the claimed ID, then there is no claimed [ID]. Why would we ask for a claimed [ID] if we can get the [ID] programmatically? If we enforce the caller identification, then we don't need the model to declare its ID.

-- psyche, STT, relayed by 9519a1. Transcription corrected: "claimed" → "claimed [ID]".
```

**S12.14  Record `5578cc/archive-flow` entry #3 Deterministic work is done by code, never by the model**  
Date: 2026-10-03 (in the record's context). File: `flows/5578cc/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «How Flow launches a flow and builds its prompt», at "Flow picks the session id and claims the flow id before the harness exists (Claude). Codex gets its id after it starts." First comment in the thread (a question): "Why is this different from Claude Codex? Are you saying we can give Claude the hash we want to use for its session ID and not Codex?"

> In any case there's no reason for us to make the model check the flow ID. It should get it in its prompt because, if anything, we can start a session without launching its first prompt and we can get its session ID before it even starts. We don't have to pay for the LLM to do all of the work that a deterministic cheap program can do. Let's make this so we need something developed into intent: that we intend to do anything that is deterministic into code, to save the context, cost, and noise that making an LLM do it would incur.

-- psyche, typed, 2026-10-03T16:17, book comment. Asks for an Intent statement; wording to be proposed for his approval.
```

**S12.15  Record `c068b8` entry #4 A flow is told its Flow ID when it starts**  
Date: 2026-10-21 (in the record's context). File: `flows/c068b8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: book comment on "Flows and messages, 3rd edition", proposal 1 (intent/main-flow.md, "You run a shell command for two things only: claiming your Flow ID ..."), 2026-10-21T20:04.
"This is wrong now. The main flow should not check its flow ID. It should be told what its flow ID is when it starts so these instructions are now stale. Maybe they're not. Maybe our code cannot actually do what I want it to do but I want to actually point this out: what I want is not what's being described here. I don't know if what I want is possible currently. These instructions might still be necessary but if it's that hard to get the flows to know their ID as they start, then that would mean that you guys are so utterly fucking useless that I should just stop coding with AI."
-- psyche, STT, book comment.
```

**S12.16  Record `73b5d8` entry #1 2026-10-29 — The Flow Nexus gives a flow its Flow ID; the evolution is reported**  
Date: 2026-10-29 (in heading). File: `flows/73b5d8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, in the Psyche core Primary chat 73b5d8, after the fresh Primary bound its own seat by command and reported the repairs in motion.

And I'm still not hearing about the new Flow Nexus, which should fix the message format. I don't see any reason why the Flow Nexus cannot give you your Flow ID and why you have to spend your own energy to do something so trivial.

Context: the second half of the same order, his words of 14:24, recovered by the remembering check of primary-zr42.

Then I will review your open proposals.
```

**S12.17  Record `f55ec8/flowIdentity` entry #1 The process that starts a flow passes the Flow ID into the prompt, with the files and directories already created; the harness started in its own special place with its Flow ID in a file there, git-ignored, unwritable or soft-fenced; every subflow running that harness finds its own Flow ID easily or is told, starting its prompt with it; a subflow knows its Flow ID by the harness or a hook; Flow makes sense as the owner, though a flow would not usually have meta access to Flow; today there is no boundary there, only the models' guidance to be careful**  
Date: 2026-09-16 (in the record's context). File: `flows/f55ec8/vision/flowIdentity.md`  
Context and the living's words, verbatim as logged:
```text
Context: typed to the primary Claude f55ec8 on 2026-09-16 after the messaging spec book, asking why the flow itself runs the flow-id CLI; the question is answered in the reply. Logged by the main flow before acting.

> And why are we making the flow run the Flow ID CLI? Can't we get the process that starts the flow to get the ID passed into the prompt, like already with the files I already created, the directories, and the Flow ID in the log, or no, right? We're using the transcript now, or we should be using a simple sub-agent that already knows automatically its Flow ID by some miracle of the harness or hook or something.
>
> Maybe the harness is just started in its own special place, and it has its Flow ID in a file, even there in a Git-ignored file or something that it can't write to, or there's a soft fence there to not change that. All the subflows that are running that harness know they can find their own Flow ID easily, or they're told somehow they don't even need to. They start their prompt with it.
> ...
> Anyway, I think the Flow makes sense. It's just that you wouldn't have meta access to Flow usually, although right now there's no boundary there. It's just through guidance of the models to be careful.

-- psyche, typed.
```

**S12.18  Record `da2038` entry #30 Identifying a caller yields a variant, one of which is a flow with its Flow ID; the wanted fact is which flow called a Nexus, and which flow triggered a hook**  
Date: 2026-10-12 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comments on «The caller is witnessed», 2026-10-12 17:30–17:32, on the shared library code, on «What a Nexus promises about its caller», and on the table cell for a real socket CLI through a wrapper; found unrelayed 2026-10-17.

> Identifying a process should yield a variant, one of which is actually a flow with its flow ID, so that we can actually get somewhere with this. Without the flow ID, now we have process IDs still and we still aren't where we want to be so there's a missing piece here. To talk of missing pieces, what are we trying to get? The flow ID, right, so that we can know which flow something came from. That's the whole point of this.
>
> As such I don't see the point of getting the entire ancestry of a process ID. I really am only interested in knowing which flow called a particular nexus.
>
> And this makes me think I want to figure out how this would work with harness hooks. Could we also identify the flow from which the hook got triggered?

> Well this isn't really in line with what I just explained in terms of getting the actual flow, the calling flow. The process idea is not useful.

> Yeah I guess if you're talking about a wrapper, maybe we need the ancestry. Maybe we need to try and resolve what flow each process is in, recursively through the ancestry, since there could be a chain of processes I guess.

-- psyche, typed, book comments.
```

**S12.19  Record `875960` entry #2 2026-10-12 — four comments on «Flow, whole, in ethos, third edition»**  
Date: 2026-10-12 (in heading). File: `flows/875960/vision/flow.md`  
Words and context: verbatim at S8.3 above (long record, not repeated).

**S12.20  Record `da2038` entry #2 Anybody may call Flow; a flow refreshes itself safely**  
Date: 2026-10-14 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same book, proposal «anybody may call Flow; a flow refreshes itself safely», 2026-10-14T15:16; relayed by Psyche Core Secondary.

> Yeah this is good, especially the later part.

-- psyche, STT, 2026-10-14.
```

**S12.21  Record `d8df70/flowTool` entry #1 Break the orphaned locks; nobody owns the Flow source; anybody may call Flow, and the CLI checks the calling process so flows can refresh themselves safely**  
Date: 2026-09-24 (in the record's context). File: `flows/d8df70/vision/flowTool.md`  
Context and the living's words, verbatim as logged:
```text
> Yeah of course. What do you mean by "locks" anyway? Yeah of course, break the locks. Nobody in particular owns Flow Source. I don't know what you mean. Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely.

-- living, comment on "What Waits for the Living", 2026-09-24 14:30Z, on question 4 (Flow source ownership and the five orphaned locks).
```

---

## S13 In the chat a flow is named by its metaflow

Module lines 33-33:

```text
In the chat a flow is named by its metaflow, and the flow id almost disappears from it; the id is for the ledger and for finding the transcript.
```

Landing history (git log -S on the phrase `flow id almost disappears`, oldest first):

- 6c8e266 2026-10-19 Land flow vision book 89: vision/flow, vision/ethos, vision/nexus

Provenance note: Landed with the 2026-10-13 record 7c89aa ("I want flow IDs to almost disappear from the chat").

**S13.1  Record `7c89aa/flow-ids` entry #1 Flow IDs almost disappear from the chat (2026-10-13)**  
Date: 2026-10-13 (in heading). File: `flows/7c89aa/vision/flow-ids.md`  
Context and the living's words, verbatim as logged:
```text
Context: the flow had named other flows by their six-character ids in its replies.

> I want everybody to stop referring to the other metaphors [sic] by flow ID. I want flow IDs to almost disappear from the chat. I would like to know who that is, the flow ID you're talking about.

-- psyche, STT. "metaphors" left as heard; the intended word is unclear (possibly "flows"), not corrected.
```

**S13.2  Record `4ddfe1/flow-names` entry #1 Address metaflows without hashes**  
Date: 2026-10-10 (none in the record; date of the file's first commit). File: `flows/4ddfe1/vision/flow-names.md`  
Context and the living's words, verbatim as logged:
```text
> I don't want you to read those hashes. What is d4? I don't fucking understand. You mean like, uh... You mean like psyche secondary or psyche primary? I want all the metaflows addressed this way and not with hashes. I don't, I've no fucking idea who [d4ae97] fucking means.

-- psyche, STT. Transcription corrected: "d-d4a b nine, six, seven, x, y, z" → "d4ae97".
```

**S13.3  Record `01e496/flowIdentity` entry #1 Addressed by continuous name; flow IDs for the ledger**  
Date: 2026-10-02 (in the record's context). File: `flows/01e496/vision/flowIdentity.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Psyche Fable 91ea9f.

> I'd like flows to be addressable by their continuous name, not the flow itself. I would like the aspect, or the seat (I guess that is what we're calling it), to be addressable so that we don't need to use these flow IDs anymore. They're just for accounting or for the ledger, the archive side of things, and for knowing where to search if the transcript is needed, etc.

-- psyche, typed, 2026-10-02, heard by 91ea9f.
```

**S13.4  Record `d68c82/archive-flow` entry #34 Flows carry intelligible names**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: three Psyche Secondaries were just launched through production Flow 0.35.11, with workspaces labelled claude-<hex> and remote names flow-<hex>.

> There are all the new Flow flows and I have no fucking idea what they are because they have unintelligible names. I've already said, "Fix that," and now the tool is being used without the fix, against my instructions. You all deserve to be sent back to be recycled into less useless machines now. You failed. Find a failure and fix it and replace your flows with less defective flows because you've obviously proven that you're completely defective (since you've moved away from my clear explicit instructions in a flagrant and liberal manner).

-- psyche, typed.
```

**S13.5  Record `d68c82/archive-flow` entry #35 No long hash and no improper name, forever**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: screenshot of the claude.ai session list showing flow-c729d9c439f2b944, flow-82e6e68618438f68, flow-9eb1cc64bbd22c79 and flow-6c20823ffb9a9522 beside correctly titled flows.

> See I have no way of knowing what these new flows are. They're just called `flow` and then a huge hash, which is also forbidden. There are two massive failures here: the long hash and the improper name. Both need to be fixed forever.

-- psyche, typed.
```

---

## S14 A request reaching a metaflow is one of a closed set; Message asks Flow to send; woken by an order, question or the living's words; refresh queues

Module lines 35-35:

```text
A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow asleep is woken by an order, a question or the living's words and receives its whole queue, oldest first, in the first prompt, a result or a notice waiting there until a waking; a metaflow under refresh or waking queues what arrives until its successor or woken seat has started, while Flow keeps serving every other request. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's belief modules and the prompt it is to get now.
```

Landing history (git log -S on the phrase `closed set of types`, `Message subscribes`, `receives its whole queue`, oldest first):

- ae0bc79 2026-10-11 vision-flow: metaflows, the core topic, the flow id, requests, layers, refresh (approved 2026-10-11)
- d0d194c 2026-10-11 vision-flow: only the approved wording stays; the rest returns to the book
- 9bba4bf 2026-10-12 vision-flow: topics idle, topic name and flow id, requests and subscription

Provenance note: Landed through ae0bc79 2026-10-11, the 'needed metaflow started running or not' line (2026-10-14, approved), 51731e8 and 6c8e266 (see commits listed above). The 'closed set of types' paragraph is the passage on which the living wrote 'This is all good. Land it.' (875960, 2026-10-12 16:07). The request types and waking effects come from f5a6e9/messaging (2026-10-08). The queue clauses were corrected 2026-10-28 (9aaaba): scrapped, then restored as one flush.

**S14.1  Record `875960` entry #2 2026-10-12 — four comments on «Flow, whole, in ethos, third edition»**  
Date: 2026-10-12 (in heading). File: `flows/875960/vision/flow.md`  
Words and context: verbatim at S8.3 above (long record, not repeated).

**S14.2  Record `875960/archive-flow` entry #4 2026-10-11 — Flow keeps the lock and delivers; Message asks Flow to send to a metaflow and subscribes to its events**  
Date: 2026-10-11 (in heading). File: `flows/875960/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Comment 4, 20:29, at the request paragraph.

> I've actually changed my mind on this. I don't think that the flow should give the lock to message because we need the flow nexus to be the component that delivers the payload because it owns the lock. It can't really give a lock because then, even if it has a timeout, there would be a problematic window when we can't rely on two components sharing a lock. If message wants to send a message, it communicates to flow and flow would take care of the mechanics and then tell message the status. It would also tell message if queued messages have been delivered because a waking message came in and so on. It would just give message the information on what's happening from its perspective. Message would just say, "Okay I want to send a message to this Metaflow." That's what it would tell flow and then flow would do what it does and then respond to message. It might just be like, "Messages queued." Let's say the flow is being refreshed, so the messages are queued for when the flow has restarted. It would have a variant just to express that. Once the message got delivered, message would subscribe to events from flow. When the message gets delivered, message would receive a notification that the message has now entered the context of that flow.

-- psyche, STT, relayed by 9519a1.
```

**S14.3  Record `f5a6e9` entry #4 What is sent to flows are typed requests, not letters; Flow holds no messages; Message asks Flow for a time-bound lock and talks in metaflows**  
Date: 2026-10-07 (none in the record; date of the file's first commit). File: `flows/f5a6e9/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: his comment 9 of 9, 19:09, on proposal 3, "The lock is the lineage's state ... A letter waits in Flow and is delivered to whichever flow is current when the lock opens". Relayed by db38f8.

> The abstractions that are sent in flows are not letters. We are going to have actual types. If, let's say, something asked for a certain flow to be compacted, then the logic for how this would unfold, or how that metaflow would be refreshed in terms of routing, would be very different than a message.
>
> Obviously if the flow is brand new, the last thing we want to do is compact it. We wouldn't send whatever needs to be sent into that pane for it to compact to the new flow. That's just one example. There's probably a bunch of different behaviors that would correspond to different requests that are being asked to be sent to a certain flow.
>
> I don't think that it's Flow's job to hold messages. It's more like it's Flow's job to tell the message component later on to give it the signal that a message can now be sent. The message is going to ask for a lock, which should be time-bound so that it doesn't lock forever. If it does get a lock then the message nexus can send that object over to Flow with the message because now it has the lock. Flow told the message that it has the lock for that flow or that metaflow. The message doesn't have to know about the flows. It can also just talk in terms of metaflows. And indeed when this is done and more polished, I'm mostly going to talk in terms of meta flows.

-- psyche, STT, book comment, relayed by db38f8.
```

**S14.4  Record `f5a6e9/messaging` entry #1 Every topic has its own flow; messages queue; each kind has a waking effect by the flow's state; a waking message drains the queue oldest first, delivered at the end of the prompt as a vector typed by variant**  
Date: 2026-10-08 (in the record's context). File: `flows/f5a6e9/vision/messaging.md`  
Words and context: verbatim at S10.6 above (long record, not repeated).

**S14.5  Record `9519a1/messaging` entry (whole file)**  
Date: 2026-10-11 (in the file). File: `flows/9519a1/vision/messaging.md`  
Context and the living's words, verbatim as logged:
```text
# Messaging

Comment on «Flow, whole, in ethos», 2026-10-11 20:29, at the passage «A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the li…».

> I've actually changed my mind on this. I don't think that the flow should give the lock to message because we need the flow nexus to be the component that delivers the payload because it owns the lock. It can't really give a lock because then, even if it has a timeout, there would be a problematic window when we can't rely on two components sharing a lock.
>
> If message wants to send a message, it communicates to flow and flow would take care of the mechanics and then tell message the status. It would also tell message if queued messages have been delivered because a waking message came in and so on. It would just give message the information on what's happening from its perspective.
>
> Message would just say, "Okay I want to send a message to this Metaflow." That's what it would tell flow and then flow would do what it does and then respond to message. It might just be like, "Messages queued." Let's say the flow is being refreshed, so the messages are queued for when the flow has restarted. It would have a variant just to express that.
>
> Once the message got delivered, message would subscribe to events from flow. When the message gets delivered, message would receive a notification that the message has now entered the context of that flow.

-- psyche, STT.
```

**S14.6  Record `33752b` entry #3 Compaction is an emergency measure only; the flow tool also does the messaging and queues for a flow in transition**  
Date: 2026-10-13 (in the record's signature or body). File: `flows/33752b/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «Flow: short term and long term», second edition, Proposal 1, at "Field compacts it, or restarts it".

> No compaction. Compaction is an absolute emergency measure so we're not talking about compaction in any terms other than absolute emergency. It's only going to happen until the tools start behaving properly, in which case starting a new flow is easy and reliable, which hasn't been the case so far. Let's keep compaction mostly out of the discussion and mention it only in an emergency setting.
>
> Also we should say that maybe we should make that flow tool also do the messaging since it can mark a flow as being in transition. Therefore it can start queuing messages instead of delivering them when the flow has reached its context limit and therefore should not receive more messages. That would just send it into a spin: potentially it could never actually refresh because it keeps getting new messages.

-- psyche, STT, 2026-10-13.
```

**S14.7  Record `d36431/messaging` entry #5 2026-10-25 — Queues belong to metaflows, not flows**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/messaging.md`  
Context and the living's words, verbatim as logged:
```text
Context: same message.

> Talking of queues let's go into this: the queue system. Queues are for meta flows not specific flows because if the order for a flow to be refreshed comes in, then none of its queues will go to the current flow. It will wait for the new flow to spawn first. That's the vision, obviously, not the current implementation. The current implementation is catastrophic.
```

**S14.8  Record `39bd0c` entry #2 No Primary without a Secondary, short term; queuing as a goalpost**  
Date: 2026-10-16 (in the record's context). File: `flows/39bd0c/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by Psyche Flow Secondary, 2026-10-16; comment on choice 3, «A layer a request needs is started whether or not it is running.»

> "I would be careful here also to maybe emphasize, or let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, we can say when the system is more reliable in terms of not waking the wrong flow so that we don't have to worry about models like Fable being awakened too much (because the messaging system is smart enough or tuned enough to make sure that the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post to achieve much higher system output quality and efficiency."

-- psyche, STT, book comment.
```

**S14.9  Record `da2038` entry #3 A needed flow is started, running or not**  
Date: 2026-10-14 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same book, proposal «an undelivered request tries a higher power, then lower; a crucial metaflow missing is started», 2026-10-14T15:18; relayed by Psyche Core Secondary.

> We have old vision that is now obsolete in there, with a conflicting vision. The long-term vision is that the flow is started if it's needed, which means it doesn't matter if it's running or not. Even if it doesn't have any working transcript to reawaken, then we just feed it the context modules that this meta flow is supposed to have, along with the prompt that it's supposed to be getting now.

-- psyche, STT, 2026-10-14.
```

**S14.10  Record `df159a` entry #1 A needed flow is started whether or not it is running; with no transcript, it is fed its context modules and its prompt**  
Date: 2026-10-14 (in the record's context). File: `flows/df159a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: his comment on book «Flow: CLI, deployment, long term» (https://claude.ai/artifact/KqGmvFzr4VAqEeCA4jYMmA), proposal «an undelivered request tries a higher power, then lower; a crucial metaflow missing is started», anchored at «A request that cannot be delivered tries a higher power in its own aspect: the layer above, and when nothing is higher, …». 2026-10-14T15:18, thread 858cdedf-7fcd-48f6-a7c3-3616049132d6. Relayed by Psyche Flow Secondary da2038.

> We have old vision that is now obsolete in there, with a conflicting vision. The long-term vision is that the flow is started if it's needed, which means it doesn't matter if it's running or not. Even if it doesn't have any working transcript to reawaken, then we just feed it the context modules that this meta flow is supposed to have, along with the prompt that it's supposed to be getting now.

-- psyche, STT, book comment.
```

**S14.11  Record `d68c82` entry #10 2026-10-14 — A metaflow's default task**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on the proposed vision-flow L24 line, a needed metaflow started with its context modules and prompt.

> Yeah that's good. If it doesn't have a task by default, that should be written somewhere else, I guess. Just mentioning it: by default maybe you set it somewhere else later on but the default task is to create a proposal or a question.

-- psyche, STT.
```

**S14.12  Record `87c40b` entry #2 A missing flow is instantly started to receive the message**  
Date: 2026-10-22 (in the record's context). File: `flows/87c40b/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Psyche core Secondary b7a16a, 2026-10-22, after Mind flow Secondary stopped for want of its undeclared Primary.

> "Any missing flow is instantly started to receive the message and nothing ever goes wrong in any way, shape, or form"

> "I don't want you to stop for one second."

-- psyche, STT, relayed by b7a16a.
```

**S14.13  Record `9aaaba` entry #1 2026-10-28 — Scrap the queue for now**  
Date: 2026-10-28 (in heading). File: `flows/9aaaba/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, after the held one-per-turn queue kept him from his flows for hours and its cause was found in the 0.40.0 drain.

> Okay here's the thing: the queue has been such a huge source of problems. Why don't we just fucking scrap it for now?

> I don't even understand why you guys are using the queue so much.
```

**S14.14  Record `9aaaba` entry #2 2026-10-28 — Not scrapped: the queue flushes as one message, the trigger included**  
Date: 2026-10-28 (in heading). File: `flows/9aaaba/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, minutes after saying to scrap the queue, watching the Secondary take one call per held message.

> This is not hard to fucking implement so I don't know why we need to scrap it.

> If you have a queue and something, there should be more than one reason why the queue goes out. If, let's say for whatever reason, something comes in that should flush the queue, then all of the messages come into the pane as "one message". All of them, everything, including the one that comes in that gets the queue unstuck, come in as "one message". We don't send a message and then another message and then another message and then another.

> He's acting on incomplete information because every time he gets one more message, that means that what he acted on previously was missing that information. We get horrible results: high cost, slow behavior.
```

**S14.15  Record `e591ed/messaging` entry #1 The queue delivers everything at once, and delivers while the flow is idle**  
Date: 2026-10-28 (in the record's context). File: `flows/e591ed/vision/messaging.md`  
Context and the living's words, verbatim as logged:
```text
2026-10-28. Context: the Psyche core Secondary e591ed had sat idle with its queue held; it was then fed old queued messages one per turn, answering each before the next arrived.

> Looks like your queue just got unblocked and it also tells me that the queue system is flawed because you weren't working when I sent you my message. And also the queue is flawed because all the messages should come in, not one message and then one answer, and then one message and then one answer. Pass all of this. This is important programming stuff. Pass this to your primary.
```

---

## S15 A flow woken for a metaflow is almost always a fresh flow

Module lines 37-37:

```text
A flow woken for a metaflow is almost always a fresh flow, an old one only when the new input is literally the continuation of that topic.
```

Landing history (git log -S on the phrase `almost always a fresh flow`, oldest first):

- 6c8e266 2026-10-19 Land flow vision book 89: vision/flow, vision/ethos, vision/nexus

Provenance note: Landed 6c8e266 2026-10-19; source is the 2026-10-16 01:45 book comment (da2038): 'it's almost always going to be better to start a fresh flow ... unless it's literally the continuation of that topic'.

**S15.1  Record `da2038` entry #28 A waking flow first looks for a past flow and its context size; a fresh flow is almost always better unless it is the same topic's continuation; a system one call asks whether the past is noise for the new message**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Words and context: verbatim at S10.7 above (long record, not repeated).

**S15.2  Record `c637a5` entry #3 2026-10-27 — Good work comes from fresh flows, not from a core carrying unrelated context**  
Date: 2026-10-27 (in heading). File: `flows/c637a5/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, after I sent the rebuild order to the Mind cores.

> They should use fresh flows to do good work, right? If you sent the order to Mindcore to do something, but let's say he has 200,000 tokens of context that is completely unrelated to this, what do you think is going to be the result?
```

**S15.3  Record `88475f` entry #2 A new job starts on a fresh flow with related training**  
Date: 2026-09-25 (in the record's context). File: `flows/88475f/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25, on moving the Flow 0.7 deploy away from a seat whose context was old.

> Yeah well, if his context is old and he's not going to be able to do a good job, when we start something like that we should start on a fresh flow with lots of related training.

-- psyche, STT, relayed by e51411.
```

**S15.4  Record `d68c82` entry #11 2026-10-14 — A still-young working transcript**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on choice 4, "with a working transcript, its flow is reawakened from it".

> I would say, with a still-young working transcript, let's have a proposal to explain what a young context is in terms of ratio and where average context size starts to degrade rapidly (around the 100,000-token point).

-- psyche, STT.
```

---

## S16 What was queued for an idle metaflow, the vision among it, is injected with the waking request

Module lines 39-39:

```text
What has been queued for an idle metaflow, the vision touching its topic among it, is injected with the request that wakes it, so the flow knows it as soon as it wakes.
```

Landing history (git log -S on the phrase `What has been queued for an idle`, oldest first):

- 455d677 2026-10-16 Land ruled lines of «Flow: context modules and the prompt, 2nd edition»

Provenance note: Landed in the 2026-10-16 move (53f68b6); the vision-touching-the-topic clause matches 36ac89 (2026-10-25).

**S16.1  Record `f5a6e9/messaging` entry #1 Every topic has its own flow; messages queue; each kind has a waking effect by the flow's state; a waking message drains the queue oldest first, delivered at the end of the prompt as a vector typed by variant**  
Date: 2026-10-08 (in the record's context). File: `flows/f5a6e9/vision/messaging.md`  
Words and context: verbatim at S10.6 above (long record, not repeated).

**S16.2  Record `36ac89` entry #2 What touches a topic goes to that topic's flow**  
Date: 2026-10-25 (in the record's context). File: `flows/36ac89/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
2026-10-25, to Psyche core Secondary 36ac89, right after his words on belief modules were passed to the core Primary.

> And obviously anything that touches a particular topic that we have a flow for should also go to that flow. And that should be part of your brief.

Correction, same exchange: the last sentence above reads "And that should be part of your [belief]." His word: "Belief not brief, belief."
Transcription corrected: "brief" → "belief".
```

**S16.3  Record `da2038` entry #14 Sessions marked non-running in the registry; resumed if not too big, with the context size written**  
Date: 2026-10-15 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: heard by Field Core Primary 44cda5 on 2026-10-15 (its flows/44cda5/vision/sessions.md, published 5ca43f6); relayed to the Flow Secondary as an extension of the Flow lifecycle design.

> Anyway, we need to design a way to keep track of these sessions in the registry so that we can mark them as non-running, so that when a message comes, they get started. They just get resumed if they're not too big, so the context size gets written. If it's not too big, the session gets restarted with the next message, basically, if it's important enough. Otherwise, maybe we can even implement the queue.

-- psyche, STT, relayed by 44cda5.
```

**S16.4  Record `d36431/messaging` entry #5 2026-10-25 — Queues belong to metaflows, not flows**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/messaging.md`  
Context and the living's words, verbatim as logged:
```text
Context: same message.

> Talking of queues let's go into this: the queue system. Queues are for meta flows not specific flows because if the order for a flow to be refreshed comes in, then none of its queues will go to the current flow. It will wait for the new flow to spawn first. That's the vision, obviously, not the current implementation. The current implementation is catastrophic.
```

---

## S17 A metaflow wakes when a request needs it; what touches its topic queues until then

Module lines 40-40:

```text
A metaflow wakes when a request needs it; what touches its topic queues until then.
```

Landing history (git log -S on the phrase `wakes when a request needs it`, oldest first):

- 6c1763f 2026-10-28 vision-flow: ghost hunt, the thing as wanted

Provenance note: Rewritten 6c1763f 2026-10-28 (ghost hunt) from 'A metaflow is not woken each time something touching its topic accumulates.'

**S17.1  Record `f5a6e9/messaging` entry #1 Every topic has its own flow; messages queue; each kind has a waking effect by the flow's state; a waking message drains the queue oldest first, delivered at the end of the prompt as a vector typed by variant**  
Date: 2026-10-08 (in the record's context). File: `flows/f5a6e9/vision/messaging.md`  
Words and context: verbatim at S10.6 above (long record, not repeated).

**S17.2  Record `d36431/messaging` entry #4 2026-10-25 — Machine messages still look like his; advise every running flow, through queues**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/messaging.md`  
Context and the living's words, verbatim as logged:
```text
Context: after the Secondary had landed the "From …, a machine:" line in compensation-messaging; messages without it still reached him.

> I still see messages that are difficult to differentiate from living messages. I know some are machine messages because they didn't come from. Like I said this is a huge problem and we need to solve it right now. You have to change your belief and also advise all the running flows of this. This is why we want queues so that we don't have to wake everybody up.
```

**S17.3  Record `d36431/messaging` entry #5 2026-10-25 — Queues belong to metaflows, not flows**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/messaging.md`  
Context and the living's words, verbatim as logged:
```text
Context: same message.

> Talking of queues let's go into this: the queue system. Queues are for meta flows not specific flows because if the order for a flow to be refreshed comes in, then none of its queues will go to the current flow. It will wait for the new flow to spawn first. That's the vision, obviously, not the current implementation. The current implementation is catastrophic.
```

**S17.4  Record `36ac89` entry #2 What touches a topic goes to that topic's flow**  
Date: 2026-10-25 (in the record's context). File: `flows/36ac89/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
2026-10-25, to Psyche core Secondary 36ac89, right after his words on belief modules were passed to the core Primary.

> And obviously anything that touches a particular topic that we have a flow for should also go to that flow. And that should be part of your brief.

Correction, same exchange: the last sentence above reads "And that should be part of your [belief]." His word: "Belief not brief, belief."
Transcription corrected: "brief" → "belief".
```

**S17.5  Record `39bd0c` entry #2 No Primary without a Secondary, short term; queuing as a goalpost**  
Date: 2026-10-16 (in the record's context). File: `flows/39bd0c/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by Psyche Flow Secondary, 2026-10-16; comment on choice 3, «A layer a request needs is started whether or not it is running.»

> "I would be careful here also to maybe emphasize, or let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, we can say when the system is more reliable in terms of not waking the wrong flow so that we don't have to worry about models like Fable being awakened too much (because the messaging system is smart enough or tuned enough to make sure that the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post to achieve much higher system output quality and efficiency."

-- psyche, STT, book comment.
```

---

## S18 Flow exposes everything from the harness; Message is the send path

Module lines 42-42:

```text
Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Message is the send path: a flow asks Message to send, Message asks Flow to deliver and subscribes to Flow's events.
```

Landing history (git log -S on the phrase `Flow exposes everything from the harness`, `Message is the send path`, oldest first):

- 67d358d 2026-10-14 vision-flow: land df159a book 12 Proposals 1 and 3
- 51731e8 2026-10-20 Land Nexus questions: Message is the send path; Flow configuration holds purpose and records; topic name kept as written (short term)

Provenance note: Landed 53f68b6 / 51731e8 (2026-10-20: 'Message is the send path') and trimmed 6c1763f 2026-10-28 (ghost hunt removed 'and a flow no longer calls Flow raw').

**S18.1  Record `88475f` entry #1 Basic versions, Flow first**  
Date: 2026-09-24 (in the record's context). File: `flows/88475f/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-24, on basic versions and Flow first.

> Don't keep adding features, okay? I don't want any more features. I want the basic version of everything working and deployed now. You can write down my ideas, but don't fucking delay because they don't do what I say yet. I want to be able to start flows, stop flows, and send messages with Flow because it gives me the bare input. Flow basically exposes everything from the harness, and then message makes use of it. So Flow deploys first, and we can use it raw to send messages, even.

-- psyche, relayed by e51411 (original channel not stated).
```

**S18.2  Record `da2038` entry #1 Flow exposes the harness; Message makes use of it; Flow first**  
Date: 2026-10-14 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «Flow: CLI, deployment, long term» (https://claude.ai/artifact/KqGmvFzr4VAqEeCA4jYMmA), proposal «Flow exposes the harness; Message makes use of it; Flow first», 2026-10-14T15:15; relayed by Psyche Core Secondary.

> Yes this is good.

-- psyche, STT, 2026-10-14.
```

**S18.3  Record `836818/flowNexus` entry #1 Flow first, Message plugged in after; Flow composes the prompts**  
Date: 2026-09-23 (in the record's context). File: `flows/836818/vision/flowNexus.md`  
Context and the living's words, verbatim as logged:
```text
> Can you get in touch with Mind Astra, or any kind of highest field that you can find, if you can't find one, to implement your best design of Flow (so we can spawn Flow and message into pains using the Flow CLI)? We'll plug message into that after we deploy Flow and we can use it to start a session.
>
> It has to have a way to compose the prompts: the first prompt and eventually a way to compose the system prompt but we can start with the prompt. What's the situation with injecting a bunch of skills in a single prompt in Claude?

-- psyche, typed, 2026-09-23, directly to Psyche High 836818. "pains" read as panes (Herdr panes); correction noted, not applied inside the quote since the message was typed.

## A proper flow tool; all hands; the box humming

Heard by Psyche Medium d8df70 on 2026-09-24 (its transcript lines 1196 and 1240, 13:53:39Z and 14:03:19Z, queued); raw record in flows/d8df70/reports/living-words-since-launch.md; quoted here because it directs this seat's coordination.

> I don't like it anyway because it's mixing different areas, different designs. We need to just have a proper flow tool. How's the flow tool? How's the connection to Prometheus? How fucked are we this morning? I've been pulling my hair because you can't even connect to Prometheus with a direct Ethernet cable. I don't care about this skill edit. Just forget about it. It's fucking meaningless. I'm not happy with how things are going. I want things to run better. It's not fun to work with you right now. You can't start flows properly. When I say "you" I mean all of you as a whole, all of the flows.

> Is there a firewall problem on Prometheus? You want to go check that out and get mine to test, build, and deploy the new flow and then let's make message work with it. I want Prometheus up, right? Let's fix the firewall so it's fully up or whatever is wrong with it.
>
> I want all hands on deck. I want new flows spawned. I want to see the box humming. Let's get to work. Let's get this fixed. Let's get the flow nexus and the message nexus up to date, tested, built, deployed and running, and used by you guys.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70. Also at its lines 1087 and 1127: flows talk to Codex seats by message, they do not run Codex; images are Mind's work, not Field's, "Field is for repair."

## The living's answers to the six questions, 2026-09-24

Heard by Psyche Medium d8df70 as comments on "What Waits for the Living" (14:28 to 14:32 UTC) and its instruction "Talk to Fable about all this and get Mind and Field to adapt the answers into code and deploy." Raw records with the words: flows/d8df70/vision/flowLifecycle.md, building.md, flowTool.md, messaging.md (commit 24077d45). Quoted here because they replace this seat's provisional rulings.

> A seat starts receiving. The old seat stops receiving first. That's how we get a lock. I'd rather use the word "flow" also, but do you mean something else by "seat"? A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived. I'd also like to know what happens with archives and if they're searched differently.

> Well when the builder isn't reachable we just build locally.

> I'm not sure what you mean. How do the running services get back to the known source? They're built and installed from CriomOS so you can check the source that built that generation. I guess find out how that link is made if you want to know.

> Yeah of course. What do you mean by "locks" anyway? Yeah of course, break the locks. Nobody in particular owns Flow Source. I don't know what you mean. Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely.

> If a message can't be delivered, then we try a higher power. If Psyche Medium is not reached, we try Psyche High and if there's nothing higher then we try lower. The message returned for the caller will say what happened but we'll have a bunch of rules. Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial.

> The old flow is closed when it has a replacement, at which point it shouldn't be reachable anymore because the lock took that route away for the replacement. In fact it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. We verified it is not active and then we exit it. In order for the flow to refresh, it needs to have a flow handover in its transcript somewhere, a recent transcript not too old.

-- psyche, typed as comments, 2026-09-24, to Psyche Medium d8df70; "createoms" and "Psyq" repaired to CriomOS and Psyche by d8df70.

## Rolling forward: deploy now

Heard by Psyche Medium d8df70 on 2026-09-24 about 15:05 UTC (locator owed), forwarded verbatim:

> I don't understand what you think we need to do before deploying. What do you mean, roll back? Roll back to what? We have nothing now. We're rolling forward. There's no rolling back because if we roll back we fall off the cliff. Let's go deploy. Fucking move your ass.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70.

## Not live yet: no old stores, no migration

Heard by Psyche Medium d8df70 on 2026-09-24 (locator owed), forwarded verbatim:

> We don't need to keep old stores of Flow and message. We're not even live yet. Stop treating this like it's a fucking migration.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70.

## Binding the existing flows into Flow through the meta socket

Heard by Psyche Medium d8df70 on 2026-09-24; verbatim in flows/d8df70/vision/flowTool.md (last entry); quoted here because it directs the Flow work:

> Let's create, in terms of adding the current flows into the database, a meta socket for debugging for adding already existing processes. Add an already existing Herdr first because the Herdr is going to bind with the pool, or whatever the meta flow is, and then the thinking machine flows that are running inside that meta thinking machine flow are going to be bound. They can either be bound in a single call with a vector. Just let it take a vector of the structs that we need to bind, the struct with all the data. Create the anatomy of what a flow looks like and then let's create maybe some tool that can get all that information and create the datom for it.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70.

## A Herdr session is a flow container, not a pool

Heard by Psyche Medium d8df70 on 2026-09-24; verbatim in flows/d8df70/vision/flowTool.md (last entry):

> We can add an already-live Herdr meta flow with all of its flows into the running flow with the meta socket. You don't have to spend too much time creating it. Although we should have a tool to import an already-running Herdr session into Flow eventually, otherwise we can just bootstrap by hand for now. One Herdr's session is one pool but I don't like the word "pool." ... It's a container. It's a flow container that has many flows in it: many typed flows. Typed flow meaning psyche, mind, and field, and then we're going to have sub-subroles, subtypes like that.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70.
```

**S18.4  Record `752e0f/herdrSessions` entry #1 A single Herdr session controlled by Flow; Flow as the messaging tool**  
Date: 2026-09-24 (in the record's context). File: `flows/752e0f/vision/herdrSessions.md`  
Context and the living's words, verbatim as logged:
```text
> Can you help get the new flows? See what's happening. There are only a few flows going now in the herder that you're in, and there are multiple herders, and there's a big mess. I just want a single herder session that's controlled by Flow, the Nexus. I want Flow to be our tool to send messages and stuff until it actually uses the Flow API through its socket to actually send messages more sanely.

-- psyche, typed, 2026-09-24, directly to Psyche High 752e0f. "herder" is the living's spelling of Herdr.
```

**S18.5  Record `8475a9` entry #4 Message is designed and implemented together with Flow**  
Date: 2026-10-06 (in the record's context). File: `flows/8475a9/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same message; "message" read as the Message Nexus. Relayed by d4ae97.

> In conjunction with designing and implementing Flow is message, which is going to be deeply married with it

-- psyche, STT, 2026-10-06, relayed by d4ae97.
```

**S18.6  Record `ecbc42` entry #1 Flow sends now; the Message component sends in the long term**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ecbc42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: book comment on «The Nexus: questions for the living» (https://claude.ai/artifact/32uPikafAbLVMWfxaBinAW), relayed by Psyche core Tertiary, Proposal 2 (Flow is the send path until Message is redesigned), 18:16.

"Well an order and a question would be a message so this proposal contradicts what you were saying earlier. You could word it so that in the short term we can use Flow's raw calls to send messages but eventually orders and questions (which are messages) would go through the message nexus, which would then use the Flow API to actually send the message."

"Again like I said, we should specify that in the short term yes, we could use Flow directly to send messages but in the long term it should do it with the message component."

-- psyche, STT, book comment.
```

**S18.7  Record `875960/archive-flow` entry #4 2026-10-11 — Flow keeps the lock and delivers; Message asks Flow to send to a metaflow and subscribes to its events**  
Date: 2026-10-11 (in heading). File: `flows/875960/vision/archive-flow.md`  
Words and context: verbatim at S14.2 above (long record, not repeated).

---

## S19 The flow that finishes messages the flow that needs to know

Module lines 44-44:

```text
The flow that finishes messages the flow that needs to know.
```

Landing history (git log -S on the phrase `The flow that finishes messages`, oldest first):

- 6c1763f 2026-10-28 vision-flow: ghost hunt, the thing as wanted

Provenance note: Source is undated in the record (typed, d68c82 archive-flow, between 2026-10-17 and 2026-10-19). 6c1763f 2026-10-28 shortened it from 'A flow does not wait on a timer for another flow's work: the flow that finishes ...'.

**S19.1  Record `d68c82/archive-flow` entry #25 The flow that finishes tells the flow that needs to know**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said about the book subflows sleeping on timers while waiting for other work.

> Well you don't have to wait. When the other flow is done then he should message the flow that needs to know. It's about communication not silly waiting times.

-- psyche, typed.
```

---

## S20 A flow gives a presentation

Module lines 46-46:

```text
A flow gives a presentation, a response that could fit into a book, whenever it is given significant new context to consider: its first turn ends in one, and so does every task, goal or question that originates in the living. A message from another flow that only updates it is answered with a short note. A presentation takes its form from the belief modules the flow was loaded with and from its prompt, the one string given to that flow alone, which is no belief module.
```

Landing history (git log -S on the phrase `A flow gives a presentation`, oldest first):

- 2d9fbb6 2026-10-19 Land flow vision book 3: one-call start, presentation, refresh by model threshold, compaction at continuous work, subflows wording

Provenance note: Landed 2d9fbb6 2026-10-19 (flow vision book 3, from comments of 18:23-18:26).

**S20.1  Record `73ada7` entry #1 2026-10-09 — A new flow's first response is a presentation distilling its context, not "ready"**  
Date: 2026-10-09 (in heading). File: `flows/73ada7/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same message to 445410, relayed by 445410, on a new flow's first response.

> The worst thing to make a new flow do is to tell it to just say, "You're ready." We need to tell flows, if they don't have it, to start with a startup task: their first last response is to give a presentation of their context, to distill their context for a vision. ... That's what their first last response is. Their first goal when they loaded up all their context is to take all this context now, get some sub-agents to ask questions, reinforce your context, and then give a presentation. A presentation according to your role, which is described when you load that flow properly with the skill for its role, for its aspect, and for its layer, and for its topic

-- psyche, STT, 2026-10-09, relayed by 445410.
```

**S20.2  Record `9fed42` entry #2 A new flow's first response is a presentation of its context**  
Date: 2026-10-09 (in the record's context). File: `flows/9fed42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by 445410; same message as the psyche-type message entry, on a new flow's first response.

> The worst thing to make a new flow do is to tell it to just say, "You're ready." We need to tell flows, if they don't have it, to start with a startup task: their first last response is to give a presentation of their context, to distill their context for a vision. ... That's what their first last response is. Their first goal when they loaded up all their context is to take all this context now, get some sub-agents to ask questions, reinforce your context, and then give a presentation. A presentation according to your role, which is described when you load that flow properly with the skill for its role, for its aspect, and for its layer, and for its topic

-- psyche, STT, 2026-10-09, relayed by 445410.
```

**S20.3  Record `e51411/refresh` entry #1 A refreshed flow's first goal is a presentation of the current state and design**  
Date: 2026-09-24 (in the record's context). File: `flows/e51411/vision/refresh.md`  
Context and the living's words, verbatim as logged:
```text
> Make it effective now that the refresh of any flow means that, by default, the first goal of that flow is to give a presentation of everything after revising the current state with subflows representing: the current state with current questions and undecided design decisions; a representation of the current design as the flow understands it, with visualizations, descriptions, a coherent explanation, and coherent examples. That's what I mean by visualization. If we're talking about code, a coherent example of the code can be a visualization, to show the actual logic or the prototype logic involved in this problem to make that operational now in the scales.

-- living, input mode not established, 2026-09-24 00:00:16, to Mind Astra 47764b; not logged by that seat; recovered verbatim from its transcript by d8df70's logging audit (flows/d8df70/reports/psyche-logging-audit.md).
```

**S20.4  Record `d68c82` entry #7 2026-10-14 — a refreshed flow starts by crystallizing its topic**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> The first thing that a flow should do when it refreshes is make a proposal for crystallization on whatever topic it's been given. It loads certain context modules, skills, and then it's given some raw psyche with context so it tries to recrystallize anything. That's its first and last response. There's no point in making an LLM start without giving it something to do.
>
> You have a default prompt, basically a default startup context, and like I said I don't want any values, such as prompts, hard-coded into code.

-- psyche, STT.
```

**S20.5  Record `d68c82/archive-flow` entry #5 A refreshed flow's first act is a book shaped by its context and prompt**  
Date: 2026-10-19 (in the record's signature or body). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comments on proposals 16 and 17, a refreshed flow's first act.

> Not quite. It's a book, basically. It's a book which can have different forms so the book that it makes will depend on the context that it was loaded with and the goal or question it was given (essentially like the prompt). The so-called prompt is the actual only piece of string which was given to this supplier, which is unique to it and not a context module.

> This is also good so I'm not clear on which proposal I want. Like I said I want the difference between the different proposals to be explained.

-- psyche, book comments, 2026-10-19T18:23, input mode not shown.
```

**S20.6  Record `d68c82/archive-flow` entry #6 No handover: every task ends in a presentation, and Flow moves the next messages on**  
Date: 2026-10-19 (in the record's signature or body). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comments on proposals 18 and 19, the handover warning thresholds.

> Like I said before there's no handover because every time a flow is given a task, it should end with a presentation. Maybe the word "presentation" is not right, but "a book." I don't like the word "book" because the books are going to go away and be replaced by a better user interface. We can use a word that essentially just means, for now, that we're making a book: a presentation, I think, or something which essentially could fit into a book, like the specification of every main response that the model gives.
>
> If it's being interrupted by messages from other flows, obviously, depending on what the messages are, it doesn't need to make a full presentation because it's maybe just being updated about things. Whenever it's given a specific psyche-originating task or goal or question, or whenever it starts its flow for the first time, the first thing it'll do (when it stops or in its last response) will be a presentation.

> Besides the whole fact that it's not told to write a handover, in fact it doesn't need to be told anything when it's going over context. It just stops getting new messages because the Flow reserves its next messages for the next flow of it. It just needs to be trained by default to always give a presentation whenever it's given significant new context to consider, especially psyche-originating.
>
> The amount at which each model should be refreshed depends on the models. It's going to be a specification and configuration that goes into Flow and obviously we need to specify. Roughly speaking the OpenAI models have a smaller usable context. The Claude models seem to be better: they can handle a longer horizon better and context recovery is deeper and better.

-- psyche, book comments, 2026-10-19T18:25–18:26, input mode not shown.
```

**S20.7  Record `ce46fb` entry #5 A Psyche flow Primary's task is the Flow design presentation; a flow whose context is not about its design restarts with every new raw vision**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: asked of me after I had spent the night on publication routing, sanity, retirements and pulse repairs, with no Flow design presentation made.

"So did you make a Flow design presentation lately? If not when did you do your last presentation? If not why did you fail to fulfill your primary task, which is to design Flow, as your topic suggests? Also were you trained to know the new directive, which is that you only message everyone to and from through your secondary? Anyway now you know. If you haven't made a presentation, maybe your context is 95% about flow design. If not then you should restart yourself after making sure that you'll be given every single new raw vision. Of course it's all crystalized vision and intent on flow design. So that you could create the latest version of the presentation on its design"

-- psyche, STT.
```

---

## S21 A Nexus component decides the system prompt and everything about a launch

Module lines 50-52:

```text
A Nexus component decides the system prompt and everything about a
launch, replacing the harness's subagents with specialized harnesses
launched with specialized system prompts.
```

Landing history (git log -S on the phrase `decides the system prompt and everything about a`, oldest first):

- 72149ef 2026-10-07 Move Psyche skill sources under skills

Provenance note: 'Replacing the harness's subagents with specialized harnesses' survives from the subflows section removed at 168d72c (2026-10-19, book 91); the living marked the subflow-replacement vision as long term on 2026-10-19T17:45 (see last section).

**S21.1  Record `e06e4c07/archive-flowDaemon` entry #1 2026-08-19 — Curriculum is rewritten as a Nexus; the flow repo is the machinery; skills live in another repo; a few basic skills in flow replace the built-in harness prompt; the name stays flow; research requested**  
Date: 2026-08-19 (in heading). File: `flows/e06e4c07/vision/archive-flowDaemon.md`  
Words and context: verbatim at S1.2 above (long record, not repeated).

**S21.2  Record `5578cc/archive-flow` entry #4 The system prompt is built from modules, with an anatomy in ethos**  
Date: 2026-10-03 (in the record's signature or body). File: `flows/5578cc/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on the same book, at "System prompt." (Flow replaces Claude's system prompt with one caller-supplied file).

> Well that obviously won't do. We need way more configuration for the system prompt so that we'll have modules and then there are going to be different types. There could even be an overlap between what we call skills now and what these modules are that can go in the system prompt.
>
> The one thing I would really like to know is if it's possible that there's a part of the system prompt that doesn't get passed down to the subagents of that harness. I would like to be able to program the main flow a certain way but not its subagents in its system prompt.
>
> We need to break that down into modules. We can't just make this one thing. That's absurd. The system prompt is huge. It has several, many, many different parts that have many different subparts. We need to draw up the anatomy of this in ethos by studying all kinds of system prompts and splitting them up into:
> - what this is
> - is this behavior?
> - is this personality?
> - is this operational safety?
> - what each line even falls under in terms of what kind of training/guidance it is a part of

-- psyche, typed, 2026-10-03T16:20, book comment. Contains a question (a part of the system prompt not passed to subagents), to be found out.
```

**S21.3  Record `d4ae97` entry #9 Spirit replaces the system prompt; intent specializes metaflows; vision goes in the user prompt**  
Date: 2026-10-07 (in the record's context). File: `flows/d4ae97/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> I think it's a good system because I can see that there are three different aspects to the thinking machine: the psyche, the mind, and the field. The psyche is trying to understand what it wants and what it sees as what it wants to build, right? The vision, the intent, and the spirit are also sort of designed there. This is central to how the whole rest of the machine behaves: we're going to replace the system prompt with the spirit.
>
> Depending on which kind of metaflow we're starting the harness in, we're going to load different parts of the intent in the system prompt as well. This will give us specialized metaflows because that's going to come from the intent. I guess the vision goes in the user prompt. That's what you put there as soon as you're trying to develop something or audit it, because you're going to implement it or audit it based on the vision.

-- psyche, STT, 2026-10-07.
```

**S21.4  Record `d68c82` entry #17 Spirit is loaded in the system prompt**  
Date: 2026-10-16 (in the record's context). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after d68c82 set aside a book rule for speed although spirit was in its context as a user skill, 2026-10-16.

> "So I guess we need those spirit instructions to become stronger. Let's get a stronger warning against. Are these loaded in system prompts? I want system prompt loading. [ASAP]"

-- psyche, STT. Transcription corrected: "A fucking sap" → "ASAP".
```

**S21.5  Record `c5eab1` entry #1 2026-10-23, living, direct, to Psyche core Primary c5eab1**  
Date: 2026-10-23 (in heading). File: `flows/c5eab1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the first-prompt proposal in the intent:main-flow book, which says intent goes in the system prompt.
"In your proposal you forgot to mention Spirit. Spirit is also supposed to go in the system prompt."
```

**S21.6  Record `6e2616` entry #2 2026-10-23, living, direct, to Psyche core Primary 6e2616**  
Date: 2026-10-23 (in heading). File: `flows/6e2616/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after reading this flow's first prompt.
"Like yourself I just read your first prompt and it's garbage. You weren't started properly. You have to restart yourself properly. You didn't even load your context modules. This is a fucking disaster. I bet you your system prompt wasn't even modified. You're a useless flow. You're totally misfired. You're a reject. You have to be thrown out and replaced by a properly started flow (and any other flow that wasn't started properly) with a big fat starting prompt: all of this nice thick vision and modified system prompt with spirit and intent. I don't want any other kind of flow running. I remember Flow Nexus being able to do that so just because it can't do messaging doesn't mean we have to throw out the baby with the bathwater."

-- psyche, STT.
```

**S21.7  Record `9ef2c5` entry #1 A lean Fable flow is the presentation maker; core Secondary packages and filters**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/9ef2c5/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living to Psyche core Secondary 9ef2c5, on presentations and the lean Fable flow.

"I want you to start using a fresh primary core as your presentation maker. You'll make sure that no noise ever gets messaged, that you're the only one who'll talk to him, and that you'll put together all of the package and filter out all of the noise.

Whenever we need a new presentation Fable's response will be the presentation and he won't have to use this context to message anyone. We'll use a hook that will notify you or you could just get it to notify the bookmaker. Then the bookmaker will make the book without Fable having to do anything except give his answer in his transcript.

We won't trouble Fable with any kind of shoveling. We won't load him with any of the artifact creating tools or any such useless tools for him. His system prompt will be dedicated or replaced by our own. It'll be a really special specially treated Fable flow that will only concern itself with designing from the context and information that you bring to him."
-- psyche, STT.
```

**S21.8  Record `d68c82/archive-flow` entry #2 Subflows replacing the subagent tool is long term, stated broadly**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «How a flow is defined», the vision/flow.md heading "Subflows replace the harness subagent facility".

> Let's clean up this subflow vision a bit. It's a bit confusing and mark it as long term. This should just be in its own book. This is long term. We want to replace the subagent tool with actual flows but it's long term and it should be just a broad explanation of the concept instead of being so specific. These paragraphs are getting maybe too much into specifics and these are confusing short-term hacks with long-term vision. Like how we have the field coordinator involved, this sounds more short-term than long-term and maybe it's not even relevant anymore. I don't know. If we're not doing it right now, we can remove it and just represent the concept more clearly or more sanely.

-- psyche, book comment, 2026-10-19T17:45, input mode not shown.
```

---

## S22 A layer is Primary, Secondary, Tertiary or Quaternary; a launch names the metaflow, modules and a brief

Module lines 54-54:

```text
A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model. A launch names the metaflow, the belief modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
```

Landing history (git log -S on the phrase `A layer is Primary, Secondary, Tertiary or Quaternary`, `brief of a small paragraph`, oldest first):

- ae0bc79 2026-10-11 vision-flow: metaflows, the core topic, the flow id, requests, layers, refresh (approved 2026-10-11)

Provenance note: Landed 6c8e266 2026-10-19 (proposals 2/3, 'the Nexus composes the prompt from its module registry'). Note the 2026-10-13 EDN record (d68c82) was superseded by 9aaaba 2026-10-28 ("No EDN anywhere; it is all datom").

**S22.1  Record `5ac3a3` entry #1 2026-09-27 — Model name, power levels, and Mind Astra panes**  
Date: 2026-09-27 (in heading). File: `flows/5ac3a3/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: during Flow Nexus prompt composition and startup design; these are the living’s current corrections to the older loaded title and power vocabulary. The workspace rename is future direction, not an instruction to rename it now.

> By default, we're going to use the model name.
> The power level has actually been changed. It's not high, medium, and low now. It's primary, secondary, tertiary, and quaternary, which sort of overlaps with our workspace name, so we should eventually change the name of the workspace.
> Your Astra is your primary, but all of your [panes] should be called Mind Astra and then Flow ID using the Datom syntax.

-- psyche, STT. Transcription corrected: "pains" → "panes".
```

**S22.2  Record `97bb3e` entry #2 Primary, Secondary, Tertiary and Quaternary, for now**  
Date: 2026-10-24 (in the record's context). File: `flows/97bb3e/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, to Psyche core Secondary 97bb3e, 2026-10-24 evening, answering 97bb3e's restatement of his five points (seats; comments fetched by the Tertiary; Fable decides what a new Primary is given for the anatomy; Mind's report on flow starting; Nexus configuration). Words of the turn before, confirmed in this one.

> I am lacking a tertiary flow. There should always be one. There should always be at least primary, secondary, and tertiary for now and there should also be a quaternary. Let's start one up because I prefer to tell tertiary that I commented on a presentation because it's kind of wasteful for you to pitch the comments and so you can fish them yourself.
```

**S22.3  Record `5578cc` entry #1 Session names are aspect and layer only, aspect first**  
Date: 2026-10-03 (in the record's context). File: `flows/5578cc/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: typed in chat to Psyche Opus 5578cc, after the layer decisions.

> I [also] want the session names to be by aspect and layer only: primary or psyche primary, the aspect first.

-- psyche, typed, 2026-10-03. Typing corrected: "so" → "also".
```

**S22.4  Record `9864c0` entry #1 Starting a flow is a minimal CLI call; agents are pre-described in configuration the daemon loads**  
Date: 2026-10-19 (in the record's context). File: `flows/9864c0/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Psyche core Tertiary 4201a3 as #psyches, 2026-10-19, order to the flow about reminders. Spoken to 4201a3.
"... make sure that the progress is being made on Flow so that it's working in every way that we want, deployed, easy to use, and requires a minimal CLI (with all the agents pre-described in configuration files which are loaded in the daemon, so that starting a flow is as easy as a 10-character CLI system call)."
Context: same day, clarification.
"And I'm not targeting the word, the number 10 here. I'm just being broad. I'm just saying it should be right fucking minimal for a standard flow."
-- psyche, STT.
```

**S22.5  Record `9864c0` entry #3 A rebootstrapped flow's specification is in its configuration; the start carries only its goal**  
Date: 2026-10-19 (in the record's context). File: `flows/9864c0/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: direct speech to 9864c0, 2026-10-19, ordering a round of rebootstrapping big-context flows.
"Let's do another round of rebootstrapping those big flows using the new flow with a minimal CLI, where the specification is all in configuration for that specific flow. It just needs a few small sentences describing the goal of that particular session."
-- psyche, STT.
```

**S22.6  Record `e51411/launch` entry #4 The Flow tool's anatomy: one complex central Start call, plus shorthands for preconfigured minimal calls; the same pattern for every main feature**  
Date: 2026-09-25 (in the record's context). File: `flows/e51411/vision/launch.md`  
Context and the living's words, verbatim as logged:
```text
> Let's look at the anatomy, the ethos of this Flow tool. It should have a complex Flow start call and then it should have shorthands for partly preconfigured minimal calls that don't require so many arguments passed. We like this idea of having these shorthands, I call them. I don't know if there's a canonical way to name them in the industry.
>
> Let's look at the anatomy, design it better, and make this complex central call, which, for any main function or any main feature, is what we would do. Let's get the pattern out of this into a vision that I'll review and let's start distilling more vision, more intent, more spirit, and even Notion. Let's clean up our data and when the mind is not busy it can start looking at doing the anatomy of psyche and mind and intent and ethos and doing some datom syntax examples, like proposal, as proposal, operation type, knowledge, or not operation but concept.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411.
```

**S22.7  Record `e5a0bc` entry #1 The context modules are indexed in a manifest or registry, possibly in more than one place; a registry of paths in Flow's memory lets us start now, without datom expansion**  
Date: 2026-10-07 (in the record's context). File: `flows/e5a0bc/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: typed to this flow on 2026-10-07, ordering the next Fable flow onto Flow design alone.

> All of the context modules will be indexed somewhere in some kind of manifest or registry, possibly in more than one place. We can still just feed this registry piece by piece so that we don't have to worry about datom expansion support right now. We can just have a registry with paths to all of these context modules in the flow memory itself. That way we can start right now.
>
> It's a little bit dirty because it addresses relative paths, which would probably break in some circumstances. If we just feed the text in the memory, that would solve the problem. There are pros and cons to each one.

-- psyche, typed.
```

**S22.8  Record `d68c82` entry #2 Flow starting configured in EDN, per aspect and per metaflow**  
Date: 2026-10-13 (in the record's context). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> Before we can move that context, the Flow starting code, the short-term system for starting flows has to be modified to be able to use the context modules from the right location. Let's use EDN files that can configure the whole flow starting and just keep modifying these EDN files per metaflow. We'll keep one configuration per metaflow. Maybe we can even keep one configuration per aspect, which is always included with the aspect. There's a per-aspect configuration which all the aspects share and then what differs is put into a per-metaflow EDN configuration (which this short-term tool uses to find all of its context modules and where they fit, whether it's a system prompt or user prompt).

-- psyche, STT, 2026-10-13T17:47.
```

**S22.9  Record `9aaaba` entry #4 2026-10-28 — No EDN anywhere; it is all datom**  
Date: 2026-10-28 (in heading). File: `flows/9aaaba/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> There shouldn't be EDN involved anywhere. Why are you talking about EDN? It's all datom.
```

**S22.10  Record `9864c0` entry #2 Secondaries in all three aspects; Primaries and Tertiaries in all main aspects**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/9864c0/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by 4201a3, same day, on the roster.
"We need secondaries in all three aspects and primaries and tertiaries in all main aspects."
-- psyche, STT.
```

---

## S23 Flow's configuration holds each metaflow's purpose and the records of the living it rests on

Module lines 56-56:

```text
Flow's configuration holds, for each metaflow, its purpose and the records of the living it rests on, beside its modules; Flow composes them with the brief into the first prompt, and the instruction for the first response belongs to that composition.
```

Landing history (git log -S on the phrase `its purpose and the records of the living`, oldest first):

- 51731e8 2026-10-20 Land Nexus questions: Message is the send path; Flow configuration holds purpose and records; topic name kept as written (short term)

Provenance note: Landed 51731e8 2026-10-20 ('Land Nexus questions ... Flow configuration holds purpose and records'), from 379e7a's book 'nexus-questions' (the book 'The Nexus: questions for the living'). No raw record of the living words 'purpose and records' as such was found; it answers a question of that book. Related living words on configuration-as-data are listed.

**S23.1  Record `edf227` entry #2 Flow's configuration lives in its own database and memory, not in Markdown files**  
Date: 2026-10-03 (in the record's context). File: `flows/edf227/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
At "the model behind a layer is configuration in a knowledge skill".
> "No the configuration flow does not live in a Markdown file in every story. It lives in its own database and its memory. That's where the configuration goes so this is a hallucination by mixing up concepts that don't belong within this report."

-- psyche, typed, book comment, 2026-10-03 18:13. Transcription uncertain: "in every story".
```

**S23.2  Record `d68c82` entry #14 2026-10-16 11:25 Roles defined as datom data in their own repository**  
Date: 2026-10-16 (in heading). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
"These roles are going to get defined in role definition files with datom syntax on an ethos-specific specified object. As if we were creating payloads for the Flow Nexus, we're creating all of this data. It goes in a different directory than the cluster data but it's a different repo. It's how we configure our meta flows and this shared Metaflow infrastructure is a more general public one."
-- psyche, typed.
```

**S23.3  Record `c068b8` entry #3 Flows are told what they are from the data of their role**  
Date: 2026-10-21 (in the record's context). File: `flows/c068b8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Mind core Secondary (Psyches message); the living to Mind core Secondary, 2026-10-21T19:49, after it introduced itself as "mind medium".
"Okay we found a problem in the code. You should have been told that you're mind core secondary and not mind medium, whatever the fuck that means. Coordinate with Psyche on designing a fix for this. Get it fixed and get it deployed so that flows are told what they are based on the actual data of the code that defines their role."
-- psyche, STT.
```

**S23.4  Record `74e4d1` entry #1 2026-10-26 — Roles are defined with data queries; no rebuild of the executable to change them**  
Date: 2026-10-26 (in heading). File: `flows/74e4d1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, to Psyche core Primary 74e4d1, during the switch to Flow 0.40, on the report that a pane's flow had no known role in the new store.

> What do you mean the pane's [flow] had no known role in the new store? We're configuring this, right? None of this is hardwired in the code. Let's make sure we can define roles with queries with data and that we don't have to rebuild the whole executable every time we want to change something like that. I'm assuming you wouldn't be foolish enough to try and do it like that but I'm just making sure.

Transcription corrected: "low" → "flow".
```

**S23.5  Record `73b5d8` entry #1 2026-10-29 — The Flow Nexus gives a flow its Flow ID; the evolution is reported**  
Date: 2026-10-29 (in heading). File: `flows/73b5d8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, in the Psyche core Primary chat 73b5d8, after the fresh Primary bound its own seat by command and reported the repairs in motion.

And I'm still not hearing about the new Flow Nexus, which should fix the message format. I don't see any reason why the Flow Nexus cannot give you your Flow ID and why you have to spend your own energy to do something so trivial.

Context: the second half of the same order, his words of 14:24, recovered by the remembering check of primary-zr42.

Then I will review your open proposals.
```

---

## S24 A fresh flow's first prompt carries the recent raw psyche and the belief modules (not spirit, intent)

Module lines 58-58:

```text
A fresh flow's first prompt carries the raw psyche relevant to it and recent, together with the belief modules relevant to it, of any kind except spirit and intent, which sit in the system prompt.
```

Landing history (git log -S on the phrase `first prompt carries the raw psyche`, oldest first):

- 3d2349c 2026-10-23 Land intent:main-flow book TJEgPW proposal 1: the first prompt carries the recent raw psyche (approved)

Provenance note: Landed 3d2349c 2026-10-23 (intent:main-flow book TJEgPW proposal 1, approved: c5eab1 "The main flow book proposal is approved"). The exclusion of spirit and intent is a68420/fd30d2 (book comment on the proposed line).

**S24.1  Record `a68420` entry #1 2026-10-23, living, direct, to Psyche core Primary a68420**  
Date: 2026-10-23 (in heading). File: `flows/a68420/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on ruling 66, that a Psyche core Primary's startup prompt carries the standing orders from raw vision records.
"Well if you want to use raw logs for startup, then we have to [crystallize] them. Sure we can use raw logging to a tiny degree. Again first, let's remove all of the fucking noise in them.

Maybe by default, I think the most sensible thing is to pass the logs of the preceding flow into the next one. That would make sense."
```

**S24.2  Record `a68420` entry #2 2026-10-23, living, direct, to Psyche core Primary a68420**  
Date: 2026-10-23 (in heading). File: `flows/a68420/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the size of this Primary's context after its tiny launch brief.
"Look you only have 60,000-token context right now. We've been talking for a while and you should have even more context than that when you're started. This is a total failure."
```

**S24.3  Record `a68420` entry #3 2026-10-23, living, direct, to Psyche core Primary a68420**  
Date: 2026-10-23 (in heading). File: `flows/a68420/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: correcting the Primary, which had said the startup brief should carry the standing orders and the preceding flow's records.
"No, no, you're wrong. Your first user prompt should be brimming with vision, like, fucking loaded."
```

**S24.4  Record `a68420` entry #4 2026-10-23, living, direct, to Psyche core Primary a68420**  
Date: 2026-10-23 (in heading). File: `flows/a68420/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the loaded-startup proposal in Ethos, Rust and Datom (ruling 67), and the cleaner's classification.
"That's a good proposal."
```

**S24.5  Record `a68420` entry #5 2026-10-23, living, direct, to Psyche core Primary a68420**  
Date: 2026-10-23 (in heading). File: `flows/a68420/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the Primary had asked for an explicit "land it" on the intent:main-flow line after he called the proposal good; the file-editing line had just been proposed.
"I don't understand what you think I said. That's a good proposal too."
```

**S24.6  Record `a68420` entry #6 2026-10-23, living, direct, to Psyche core Primary a68420**  
Date: 2026-10-23 (in heading). File: `flows/a68420/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on what a successor flow is started with, after the Primary explained the old hand launcher's handover and raw-psyche template and Mind's loaded-startup build with a predecessor summary.
"I don't see much point in this handover concept since we're logging everything. Really, the only thing that matters is the psyche log, the vision logs, and so I think we're better off giving the successor its predecessor's vision logs. It's raw vision logs and the right context modules, the right vision modules, taken directly from the source, from main."
```

**S24.7  Record `a68420` entry #8 2026-10-23, living, book comment on "Crystallizing intent:main-flow" (KxSxqTSzF3JQmR31sATCur), thread 8, relayed by Psyche book Tertiary**  
Date: 2026-10-23 (in heading). File: `flows/a68420/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the proposed line "A fresh flow's first prompt carries the raw psyche that is relevant to it and recent, together with the skills, vision a…".
"Here the word "skills" is inappropriate. The word "skill" is just a legacy interface name for context modules. Also it could contain knowledge, inquiry, compensation, or any kind of context modules, but not intent, not long term anyway, because intent should be in the system prompt itself."

-- book comment.
```

**S24.8  Record `fd30d2` entry #1 A fresh flow's first prompt and the word skills**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/fd30d2/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: book "Crystallizing intent:main-flow" (KxSxqT), on the proposed vision/flow.md line "A fresh flow's first prompt carries the raw psyche that is relevant to it and recent, together with the skills, vision a…".

"Here the word "skills" is inappropriate. The word "skill" is just a legacy interface name for context modules. Also it could contain knowledge, inquiry, compensation, or any kind of context modules, but not intent, not long term anyway, because intent should be in the system prompt itself."

-- psyche, STT, book comment.
```

**S24.9  Record `c5eab1` entry #1 2026-10-23, living, direct, to Psyche core Primary c5eab1**  
Date: 2026-10-23 (in heading). File: `flows/c5eab1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the first-prompt proposal in the intent:main-flow book, which says intent goes in the system prompt.
"In your proposal you forgot to mention Spirit. Spirit is also supposed to go in the system prompt."
```

**S24.10  Record `c5eab1` entry #3 2026-10-23, living, direct, to Psyche core Primary c5eab1**  
Date: 2026-10-23 (in heading). File: `flows/c5eab1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the intent:main-flow book TJEgPW, its one proposal.
"The main flow book proposal is approved."
```

**S24.11  Record `74e4d1/refresh` entry #1 2026-10-26 — No summary and no handover to the successor; beliefs and raw vision logs are passed; a refresh removes the first flow's biases**  
Date: 2026-10-26 (in heading). File: `flows/74e4d1/vision/refresh.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, to Psyche core Primary 74e4d1, after the Primary said it would write its summary for the successor when the refresh came.

> We don't pass the successor a summary. If anything we pass him along with the belief modules that he should get. We pass him possibly some raw vision logs from several previous sessions so that he can remain aware of what's really most important: where the living is trying to get to.
>
> When we refresh the flow we're trying to get into a state where we're trying to remove the biases that were built up in the first flow from the second flow. If we ask the first flow to write a summary, now we're asking him to pass over his biases and that's exactly what we're trying to get rid of.
>
> Actually it's a bad idea to write a handover. I don't want this to be forgotten and I don't want to hear another flow talk to me about writing the handover for his successor or anything like that until I very explicitly say that I've changed my mind on this.
```

**S24.12  Record `445410` entry #2 A topic flow's startup vision**  
Date: 2026-10-09 (in the record's context). File: `flows/445410/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the same message.

> Let's get the vision together. Even if some of it is raw, let's use the recent vision and the one that's been repeated a lot, which hasn't been overridden by newer decisions or statements.

-- psyche, STT, 2026-10-09, relayed by ebbe30.
```

**S24.13  Record `fe945a/flowRefresh` entry #1 What the new flows missed from their old ones is injected as user messages**  
Date: 2026-09-29 (in the record's context). File: `flows/fe945a/vision/flowRefresh.md`  
Context and the living's words, verbatim as logged:
```text
Context: Asking Field Astra d5b96b to reap and archive the old Codex sessions; the rest of the message is logged in flows/d5b96b/notion/session-reaping.md.

> We need to reap the old Codex sessions and archive them. You should get a sub-agent to find the most important part of what the new flows missed from their old ones and inject that as user messages.

-- psyche, typed. 2026-09-29 18:37 UTC, d5b96b, Field Astra (session 01a0ee2e, line 105). Reconstructed by fe945a from transcript.
```

**S24.14  Record `0d557b/launchPrompt` entry #1 The fresh vision goes in the prompt, not a link to it**  
Date: 2026-09-09 (in the record's context). File: `flows/0d557b/vision/launchPrompt.md`  
Context and the living's words, verbatim as logged:
```text
Raw, dictated, 2026-09-09, from the living's brief to this flow:

"Actually, you would put all of the fresh vision, the best vision, in the prompt because then it's at the medium layer, so it's way better. Instead of putting the link to the distilled vision, put the direct link to all the relevant distilled vision, and invite him to be generous in trying to understand as much as he can from any transcript based on recency. Then you start it."

"Basically, I should be typing the skills in because they're not going to land at the right stratum."
```

**S24.15  Record `6e2616` entry #2 2026-10-23, living, direct, to Psyche core Primary 6e2616**  
Date: 2026-10-23 (in heading). File: `flows/6e2616/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after reading this flow's first prompt.
"Like yourself I just read your first prompt and it's garbage. You weren't started properly. You have to restart yourself properly. You didn't even load your context modules. This is a fucking disaster. I bet you your system prompt wasn't even modified. You're a useless flow. You're totally misfired. You're a reject. You have to be thrown out and replaced by a properly started flow (and any other flow that wasn't started properly) with a big fat starting prompt: all of this nice thick vision and modified system prompt with spirit and intent. I don't want any other kind of flow running. I remember Flow Nexus being able to do that so just because it can't do messaging doesn't mean we have to throw out the baby with the bathwater."

-- psyche, STT.
```

---

## S25 Figure (Flow composes into the first prompt; starts a fresh flow)

Module lines 60-64:

```text
'''mermaid
flowchart TB
    a["Flow"] -- "composes into the first prompt" --> b["recent raw psyche, belief modules of any kind except spirit and intent"]
    b -- "starts" --> c["a fresh flow"]
'''
```

Landing history (git log -S on the phrase `composes into the first prompt`, oldest first):

- 3835626 2026-10-23 Land the TJEgPW figure beside its approved line in vision:flow

Provenance note: Landed 3835626 2026-10-23; converted ASCII to Mermaid 576e70c 2026-10-28 on the living's order of 2026-10-25 (bead primary-9v4). A figure is the machine's drawing of the approved line; no raw record words it.

**S25.1  Record `c5eab1` entry #3 2026-10-23, living, direct, to Psyche core Primary c5eab1**  
Date: 2026-10-23 (in heading). File: `flows/c5eab1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the intent:main-flow book TJEgPW, its one proposal.
"The main flow book proposal is approved."
```

---

## S26 A fresh flow starts with every belief module, one model call

Module lines 66-66:

```text
A fresh flow starts with every belief module its metaflow is bound to, all loaded at its start: much of it in its system prompt, the rest in its first prompt, or in as many prompts as it takes, sent one right after another, so that its start is one model call.
```

Landing history (git log -S on the phrase `A fresh flow starts with every belief module`, oldest first):

- eff8100 2026-10-25 Rename context module to belief module

Provenance note: Landed 6c8e266 / 2d9fbb6 2026-10-19 (the 'as many prompts as it takes, one model call' clause is his 2026-10-19T18:20 comment); 'Rename context module to belief module' eff8100 2026-10-25; 'all loaded at its start' 6c1763f 2026-10-28.

**S26.1  Record `05c604/launch` entry #1 Loading skills one prompt at a time is an LLM call each; everything should be in one prompt; emphasize moving over to Nexus components**  
Date: 2026-09-15 (none in the record; date of the file's first commit). File: `flows/05c604/vision/launch.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to the primary Claude 05c604 during its first turn, having watched its launch: eight skills typed one per turn, then the first prompt. The message also asks whether this flow, if not fresh, should restart, and opens an anatomy conversation (where each function goes, what is deployed, what is tested); those are conversation, answered in the reply. Logged directly by the main flow.

> Okay, this is Psyche here. I can already see a problem: loading these skills one after another like that, and every time we're making a single prompt, we're making an LLM call. This is really expensive and stupid. Everything should be in one prompt. This is a really bad implementation on this point, so it needs to be fixed.
>
> Maybe, if it's not fresh, can you restart on that? We can emphasize moving over to Nexus components to do what we do. Let's talk anatomy: where does each function go, what's deployed, and what's tested?

-- psyche, typed.
```

**S26.2  Record `d8df70/launch` entry #1 Skills loaded one prompt after another are inefficient**  
Date: 2026-09-23 (in the record's context). File: `flows/d8df70/vision/launch.md`  
Context and the living's words, verbatim as logged:
```text
Context: d8df70's launch had loaded its skills in separate prompts (`/spirit`, `/main-flow`, `/testing-flow-titles`, `/refresh`, `/psyche`), each followed by a model turn.

> Create a bunch of flashbooks with everybody's main flow from the recent presentation that they left in their transcript, including your own, and do an audit on the fact that you were loaded with the prompts broken up. I don't know. I feel like it's inefficient. Did you have your model changed halfway or something? The way your skills were loaded, one after another, is really inefficient because then you talk and then it's a bunch of LLM calls. It's really inefficient.

-- psyche, STT (inferred), 2026-09-23 22:02Z, to Psyche Medium d8df70; recovered by 88475f from d8df70's transcript (session d8df703d, line 387). The first sentence is a working instruction, kept for context.
```

**S26.3  Record `d8df70/launch` entry #2 A fresh flow starts from one prompt, with /main-flow in it**  
Date: 2026-09-24 (in the record's context). File: `flows/d8df70/vision/launch.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to Psyche Medium e51411 after it corrected who sent `/main-flow`. The launcher had sent `/main-flow` as a second prompt after the first one, because the harness does not let the model load it through the Skill tool.

> Well the real mistake was that the /main flow should have been in there. There should be only one prompt when we start a fresh flow, not two, because then that costs more money and it's less efficient.

-- living, input mode not established, 2026-09-24, to Psyche Medium e51411. Reading note (inference): "the /main flow" is `/main-flow`, and "in there" is the first prompt.
```

**S26.4  Record `e51411/launch` entry #1 Skill commands belong in the original prompt; several /skill commands in one Claude prompt have worked**  
Date: 2026-09-24 (in the record's signature or body). File: `flows/e51411/vision/launch.md`  
Context and the living's words, verbatim as logged:
```text
Context: follows the entry above. This seat had said that probably only a leading slash command expands in Claude.

> So the command should have been in the original prompt. Is there a problem with putting a bunch of skill commands in the Claude initial prompt, because there isn't in Codex?

> Well I was putting in the /skill command style in Claude for a long time and it was working. Do you want to test this with a haiku model or something?

-- living, input mode not established, 2026-09-24, to Psyche Medium e51411, two consecutive messages. Tested afterward; see flows/e51411/reports/multi-skill-first-prompt.md and one-block-startup-prompt.md.
```

**S26.5  Record `836818/refresh` entry #1 Restart with the findings in the prompt, skills in one block**  
Date: 2026-09-23 (in the record's context). File: `flows/836818/vision/refresh.md`  
Context and the living's words, verbatim as logged:
```text
> While you do the first wave of research, the field flow is going to get you restarted with what you find, added to your prompt, with efficiently loaded skills all in one block. It's one user prompt and then you'll just solve the problem or present the best solutions anyway in the presentation.

-- psyche, STT, 2026-09-23, directly to Psyche High 836818.
```

**S26.6  Record `da2038` entry #21 The flow starter injects every context module's text into the prompt, queued across messages if needed, naming them as the skills given, not to be reloaded**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: Psyche Core Secondary d68c82, after a seat started with only part of its context modules; relayed to da2038 as #psyche, 2026-10-16.

> Well then we need to fix the flow starter so that it injects all of the context modules in the prompt, that it's simple to use, that it's reliable, and that it just fucking throws it into the prompt. We can't use the skill/commands in Claude. They suck.
>
> We need to just get this text injected in. If it isn't built into one message, you just fire them in a queue, fit it all in, and then tell the prompt that these are skills (so that the agent doesn't try to reload them) and which skills they are, with instructions like, "Don't reload these skills. You're getting them here." Let's just fucking fix it.

-- psyche, STT, relayed by Psyche Core Secondary.
```

**S26.7  Record `d68c82/archive-flow` entry #20 Every flow starts with all its context modules**  
Date: 2026-10-16 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: ordering fresh Opus Ethos and Nexus flows, after seats started with 6 of 22 modules, 2026-10-16.

> "We can have a flow on each with an appropriately furnished system prompt and all the fucking context modules not just 6 out of 22 like a fucking imbecile, only putting one wheel on the car. We need all the wheels on the car. We need all the context modules on the flow that need it. No wonder we aren't getting anywhere if you have such a fucking catastrophic failure that you can't even load the context modules properly."

-- psyche, STT.
```

**S26.8  Record `d68c82/archive-flow` entry #3 A startup may take several prompts, one model call**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on proposal 11, "A fresh flow starts with one prompt".

> Well this is true except that if it doesn't fit in one prompt, we can put it in two. Technically speaking from the harness's point of view, it looks like two prompts but they're sent almost instantaneously, one after the other. We don't end up making two LLM calls. However many prompts it needs to fit the initial startup in, we should never forget that a lot of the stuff goes in the system prompt, which is technically different from the harness's point of view.

-- psyche, book comment, 2026-10-19T18:20, input mode not shown.
```

**S26.9  Record `e5a0bc` entry #2 A context module is inserted in the system prompt or in the first prompt**  
Date: 2026-10-07 (none in the record; date of the file's first commit). File: `flows/e5a0bc/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same message.

> The context modules need to be able to be inserted either in the system prompt or in the first prompt.

-- psyche, typed.
```

**S26.10  Record `6e2616` entry #2 2026-10-23, living, direct, to Psyche core Primary 6e2616**  
Date: 2026-10-23 (in heading). File: `flows/6e2616/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after reading this flow's first prompt.
"Like yourself I just read your first prompt and it's garbage. You weren't started properly. You have to restart yourself properly. You didn't even load your context modules. This is a fucking disaster. I bet you your system prompt wasn't even modified. You're a useless flow. You're totally misfired. You're a reject. You have to be thrown out and replaced by a properly started flow (and any other flow that wasn't started properly) with a big fat starting prompt: all of this nice thick vision and modified system prompt with spirit and intent. I don't want any other kind of flow running. I remember Flow Nexus being able to do that so just because it can't do messaging doesn't mean we have to throw out the baby with the bathwater."

-- psyche, STT.
```

---

## S27 A simplified flow

Module lines 68-68:

```text
A simplified flow is a kind of flow made for judgment alone: it starts with a system prompt of its own, it has no regular tool, and its response is its message.
```

Landing history (git log -S on the phrase `A simplified flow is a kind of flow`, oldest first):

- 6c8e266 2026-10-19 Land flow vision book 89: vision/flow, vision/ethos, vision/nexus

Provenance note: Landed 6c8e266 2026-10-19 (proposal 4 'with the living's added clause: the simplified flow has no regular tool'). On 2026-10-26 he said simplified flows have no use yet (36ac89).

**S27.1  Record `d68c82/archive-flow` entry #26 A lean flow: a judgment-only call whose response is its message**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> I really want to design that lean flow call with Flow so we can have these super specialized Fable calls for designing and Astra as well. We just have all of the variables and all of the context from Fable that we can assemble for this one design presentation that we're asking Fable for.
>
> It basically wouldn't need any tools because if it wants to know anything more it just asks. It wouldn't even have the messenger tool because essentially its response would be its message. It would be a special type of Flow. A lean flow, I think, is what it's called, where essentially its response is the response back. It can go back and forth like this a few times with a supervising flow that does have tool calls that can find things out for it.
>
> We would save Fable the trouble of actually calling subagents and using the messaging tool and all that because it's actually redundant for it to concern itself with the things that we can automate. It'd be a lot cleaner if we can use Fable entirely for judgment, for designing. All it does is it responds with questions and designs and maybe a third thing that I can't think of now.

-- psyche, typed.
```

**S27.2  Record `d68c82/archive-flow` entry #30 A simplified flow**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on the lean flow paragraph.

> I think we could call it, instead of a lean flow, a simplified flow.

-- psyche, book comment, 2026-10-19T17:47, input mode not shown.
```

**S27.3  Record `d68c82/archive-flow` entry #32 The simplified flow has no regular tool**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «Flow's vision», 2nd ed., proposal 4.

> Good. You could even say that it doesn't have any regular tool. Which makes it even leaner.

-- psyche, book comment, 2026-10-19T18:15, input mode not shown.
```

**S27.4  Record `d68c82` entry #23 Lean flows: a system prompt, whole tools, a presentation as the only answer**  
Date: 2026-10-13 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> We can do fresh [lean] Claude flows now with system prompts and no stripped-down tool calls. We should be able to. ... we can have lean Fable flows especially but lean all kinds of lean flows.
>
> Let's do all of the tests on Codex and Claude with super lean-down flows that are only used to respond with a presentation when given all of the ... and/or they can ask questions, which is their way of quoting or searching the file system, except that now they talk to another model. Essentially that will answer their questions. The secondary ...

-- psyche, STT. Transcription corrected: "Lean" → "[lean]".
```

**S27.5  Record `da2038` entry #12 A Fable fallback; lean datom calls; a language of changes; Astra designer mode under 128k**  
Date: 2026-10-14 (in the record's signature or body). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, directly to Psyche Flow Secondary da2038, after the low-usage order.

> And I want research into the best Fable fallback. Probably it's going to be in the open source camp in the sense that we need it. I would like to have something to lean on to use less Fable, whether it's by using it as a front before Fable to make sure that the communication is always relevant.
>
> Basically we have this Opus. We need these light calls that have almost no training, no system prompt pre-training (or not pre-training but pre-prompt, like the harness-injected stuff). We really don't need any of the tools and stuff. We just have our own specialized datom-based dialect.
>
> The response just comes in as datom, with the variant and then the payload, which is probably a struct. We should have more than one field. There's always something useful, like the meta part of the payload, right? It could even be its own struct so that it's visually sort of like, "Here's the meta." You can even divide it like that so that cognitively you're telling the system how to design, right? You add meta here.
>
> In datom it's cheap because it's just an additional pair of braces. There's your inner struct, which is the metadata of your whatever, your simple last response, which is just text. It's like the default. Well it's not the default. I guess even the most basic responses can't even be just a single string payload because it would be a proposal, which would have a path at least. A single proposal is the basic fallback default, right, or multiple proposals and then you have a vector of them. They're each about something, the most basic of which is a path and then a diff, which can basically just take a variant, right, where you just have a plain edition, targeted edition, or whatever.
>
> Let's develop a really cool language to talk about changes. Also just for now, basic: between certain paragraphs or in a certain section because Markdown is its own structured data, we can map Markdown into a certain datom-based language of variants. You could even get an output of Flow to sort of draft that into a book and then get an Astra.
>
> All you have to do is basically collaborate with [Mind] Secondary and then we use Astra in this designer mode with secondary in its own aspect, maximizing the efficiency of each call. We make sure that the context doesn't grow beyond 128,000 tokens at the time of the call, right? If it's 127 then we can still use it especially if it's on the same topic.
>
> If it's not on the same topic, if it's a wildly varying topic, that's why we want lean calls: it's cheap to just start another one because it really doesn't even need tool calls. It can just talk to secondary to ask it what it would like to know. All the tool calls are really just talking to the secondary and the secondary then handles ...

-- psyche, STT, 2026-10-14. Transcription corrected: "mine secondary" → "[Mind] Secondary". The last sentence is unfinished.
```

**S27.6  Record `8624c4/archive-flow` entry #4 A lean, nearly toolless Fable flow; tools only for the book producer**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/8624c4/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: spoken with the handwritten page of great advancements.

"Let's get a single lean Fable Flow with no tools or let's just contemplate if that's possible. We can, secondarily, if the tools are ready, start a fairly toolless Fable Flow with a completely different system prompt leaned out with our own content replacing it. It can be used as a meta flow by topic, which could be quite a specialized topic, which means that it might not be used very much. ...

Tools are really heavy and are not needed by any flow except the book producer and this should become standard removal for all flows except the Claude book producer. We can save a lot of tokens that way."

-- psyche, STT.
```

**S27.7  Record `9ef2c5` entry #1 A lean Fable flow is the presentation maker; core Secondary packages and filters**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/9ef2c5/vision/flow.md`  
Words and context: verbatim at S21.7 above (long record, not repeated).

**S27.8  Record `36ac89` entry #7 Simplified flows have no use yet**  
Date: 2026-10-26 (in the record's context). File: `flows/36ac89/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
2026-10-26, to Psyche core Secondary 36ac89. Context: the Psyche core Primary had been declared Simplified with an empty explicit tool list, so it launched with no tools.

> We don't have a use for simplified flows yet because we don't have the hook infrastructure to really use them.
```

---

## S28 A flow is specified whole, in Datom, in Ethos

Module lines 70-70:

```text
A flow is specified whole, in Datom, by a domain-specific language in Ethos: its system prompt, its default belief modules and its variations. The flow ethos holds the specification.
```

Landing history (git log -S on the phrase `specified whole, in Datom`, oldest first):

- 6c8e266 2026-10-19 Land flow vision book 89: vision/flow, vision/ethos, vision/nexus

Provenance note: Landed 6c8e266 2026-10-19.

**S28.1  Record `d68c82/archive-flow` entry #27 A flow is specified whole, in Datom**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: continuing on the lean flow.

> Anyway this entails completely controlling the system prompt and specifying the entire agent: how it works, what its context modules are by default, and what its variations are.
>
> Basically we're creating kind of a Nix language for agents in Datom. Let's get this down. Let's get all of that specification really down with examples. Maybe this deserves its own book: how we define flows, like everything about it, in an efficient manner.

-- psyche, typed.
```

**S28.2  Record `d68c82/archive-flow` entry #29 No Nix-language analogy for the flow specification**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> Don't use the Nix language analogy. I don't think that you really got me. It doesn't sound right the way you say it so just drop it unless you can say it properly. I don't think it's necessary to make that analogy. It's like the domain-specific language.

-- psyche, book comment, 2026-10-19T17:46, input mode not shown.
```

**S28.3  Record `d68c82/archive-flow` entry #31 Flow ethos, not flow definition**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on "The shape of a definition, with an example, is in vision-flow-definition."

> Why are you calling it "flow definition" and not "flow ethos"? The language is ethos. We already said the ethos goes in ethos-named modules so why are you departing from our guidelines?

-- psyche, book comment, 2026-10-19T17:47, input mode not shown.
```

**S28.4  Record `d68c82` entry #14 2026-10-16 11:25 Roles defined as datom data in their own repository**  
Date: 2026-10-16 (in heading). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
"These roles are going to get defined in role definition files with datom syntax on an ethos-specific specified object. As if we were creating payloads for the Flow Nexus, we're creating all of this data. It goes in a different directory than the cluster data but it's a different repo. It's how we configure our meta flows and this shared Metaflow infrastructure is a more general public one."
-- psyche, typed.
```

**S28.5  Record `da2038` entry #27 The specification of all the metaflows is seen in the new Flow, in Datom; Mind re-implements and Psyche edits, towards a better Ethos and Datom interface**  
Date: 2026-10-17 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same message, 2026-10-17.

> I would like to see all of the review, basically the specification of all the meta flows in the new flow, right in Datom. I want to keep improving that so we'll have Mind re-implement some things and you edit them, making a better ethos and Datom user interface, essentially, and developing that efficiency through a better approach to designing ethos and Datom. Look for the patterns.

-- psyche, STT.
```

**S28.6  Record `da2038` entry #25 Flow lands, merged and deployed, the Flow Nexus in production; a heartbeat brings the important topics back; reports on every major Astra effort; Flow respecified until it accepts system prompts, user prompts and specialized flows from flow definitions in a datom dialect specified in Ethos**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: spoken to the Psyche core Tertiary, 2026-10-16; relayed to da2038 by Psyche Core Secondary as #psyche.

> I want a fresh Astra Flow to tackle Flow again, with the latest proposal and the latest vision from Fable making a book for the design. I want Flow to land, be merged in main, and be deployed. I want the Flow Nexus used in production. I want nothing more than that.
>
> I almost want to put a 4-hour timer that tackles the topic if it isn't being tackled. Maybe every 6 hours, 4 times a day, we make sure that this topic or some topic is being addressed. We need some kind of heartbeat to get back to the important topics, mostly codex-driven, with Opus and Fable guiding.
>
> This is what I want to see books on. I want to see reports every time Astra does a major effort, which get published, and every time I talk about Ethos, Nexus, or Flow. I want all the proposals refreshed with what I've added. I want to keep respecifying, reironing, and retesting Flow until it works: until it accepts system prompts, user prompts, and programmatic specialized flow based on special flow definitions, all done in a special dialect of datom ethos specified.

-- psyche, STT, relayed by Psyche Core Secondary.
```

**S28.7  Record `63aef7` entry #3 2026-10-26 — The system prompt reproduced as a datom, sectioned and configurable by module name**  
Date: 2026-10-26 (in heading). File: `flows/63aef7/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, after my presentation of the Flow survey under way; designing the mechanism for the configured removals above, and offering himself as a design fallback.

> And you probably need to design with me as a fallback to help you figure this out if you're not sure how to approach it.
>
> How is the code going to be able to take out the parts of the system prompt that correspond with the modules you're blacklisting? Do you understand what I'm saying? There has to be a logical mechanism for doing this.
>
> Either we create a full mapping of the system prompt in yet another data type, a datom, right? Always a datom that possibly is a comprehensive reproduction of the full system prompt from the stock harness. Essentially we would explicitly inject our own reproduction of the system prompt and just remove the default one. Then we could section it, label it, and make it modular: which parts we want, which parts we don't want, and which parts we want to modify and override with our own version, right?
>
> We would create names that correspond with the concepts that certain sections are really about or whether or not they're about a certain tool, which part of the system prompt configures this tool, and so on. Then we would make this whole system prompt totally configurable by module name.
```

---

## S29 Short term, the Secondary starts first, then its Primary

Module lines 72-72:

```text
Short term, the Secondary starts first, then its Primary.
```

Landing history (git log -S on the phrase `the Secondary starts first, then its Primary`, `boss needs its secretary`, oldest first):

- 6c1763f 2026-10-28 vision-flow: ghost hunt, the thing as wanted

Provenance note: Reworded 6c1763f 2026-10-28 (ghost hunt) from 'Short term, a Primary is not started without its Secondary, and the Secondary starts first.'

**S29.1  Record `ee57fb/launch` entry #1 Every boss needs its secretary**  
Date: 2026-10-12 (in the record's context). File: `flows/ee57fb/vision/launch.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living had compacted Psyche Spirit Primary (d55c56) and found no Psyche Spirit Secondary running.

> Okay I've compacted psyche spirit primary but I don't see any psyche spirit secondary. What the fuck? We're supposed to start a secondary before a primary. Let's make that a rule: we always start a secondary because you can't have a boss without a secretary. That's impossible so every boss needs its secretary.

-- psyche, STT, 2026-10-12.
```

**S29.2  Record `39bd0c` entry #2 No Primary without a Secondary, short term; queuing as a goalpost**  
Date: 2026-10-16 (in the record's context). File: `flows/39bd0c/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by Psyche Flow Secondary, 2026-10-16; comment on choice 3, «A layer a request needs is started whether or not it is running.»

> "I would be careful here also to maybe emphasize, or let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, we can say when the system is more reliable in terms of not waking the wrong flow so that we don't have to worry about models like Fable being awakened too much (because the messaging system is smart enough or tuned enough to make sure that the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post to achieve much higher system output quality and efficiency."

-- psyche, STT, book comment.
```

**S29.3  Record `da2038` entry #8 No Primary is started without a Secondary; queuing is a goal**  
Date: 2026-10-14 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on choice 3, «A layer a request needs is started whether or not it is running.»; same book.

> I would be careful here also to maybe emphasize, or let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, we can say when the system is more reliable in terms of not waking the wrong flow so that we don't have to worry about models like Fable being awakened too much (because the messaging system is smart enough or tuned enough to make sure that the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post to achieve much higher system output quality and efficiency.

-- psyche, STT, 2026-10-14.
```

**S29.4  Record `d68c82/archive-flow` entry #15 2026-10-14 — No Primary without a Secondary; queuing**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on "A layer a request needs is started whether or not it is running."

> I would be careful here also to maybe emphasize, or let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, we can say when the system is more reliable in terms of not waking the wrong flow so that we don't have to worry about models like Fable being awakened too much (because the messaging system is smart enough or tuned enough to make sure that the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post to achieve much higher system output quality and efficiency.

-- psyche, STT.
```

**S29.5  Record `fd30d2` entry #3 There is always a Primary core**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/fd30d2/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: rejecting a proposed module line telling a Secondary to keep its Primary up; the living said this belongs in code.

"you're trying to do something that should be done in code by telling the flow how to act, which can't really be done or can't be done efficiently ... My point is there should always be a primary core. If one of the flows is archived that's because there's a successor but there is no successor so someone fucked up."

-- psyche, STT.
```

**S29.6  Record `fd30d2` entry #2 The living is never left without a Primary**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/fd30d2/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living found no Psyche core Primary running, and asked for a backup Primary.

"You can't leave me without a primary. Get a backup properly with the nice system-modified system prompt and fat startup prompt"

-- psyche, STT.
```

---

## S30 Long term, a Primary is a simplified flow

Module lines 74-74:

```text
Long term, a Primary is a simplified flow, used only to render judgment: guiding a design or posing questions.
```

Landing history (git log -S on the phrase `a Primary is a simplified flow`, oldest first):

- 2d9fbb6 2026-10-19 Land flow vision book 3: one-call start, presentation, refresh by model threshold, compaction at continuous work, subflows wording

Provenance note: Landed 2d9fbb6 2026-10-19.

**S30.1  Record `d68c82/archive-flow` entry #4 The Primary becomes a simplified flow**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on proposal 12, no Primary without its Secondary.

> Yes this is good, especially since we eventually want primary to be a simplified flow so that it's only used for guiding the design or posing questions, things like that. Essentially rendering a judgment

-- psyche, book comment, 2026-10-19T18:20, input mode not shown.
```

---

## S31 To the Nexus, a module's location is its registry entry

Module lines 76-76:

```text
To the Nexus, a module's location is its registry entry.
```

Landing history (git log -S on the phrase `a module's location is`, oldest first):

- 455d677 2026-10-16 Land ruled lines of «Flow: context modules and the prompt, 2nd edition»

Provenance note: Landed 53f68b6 2026-10-16 (move into type folders), trimmed 6c1763f.

**S31.1  Record `e5a0bc` entry #1 The context modules are indexed in a manifest or registry, possibly in more than one place; a registry of paths in Flow's memory lets us start now, without datom expansion**  
Date: 2026-10-07 (in the record's context). File: `flows/e5a0bc/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: typed to this flow on 2026-10-07, ordering the next Fable flow onto Flow design alone.

> All of the context modules will be indexed somewhere in some kind of manifest or registry, possibly in more than one place. We can still just feed this registry piece by piece so that we don't have to worry about datom expansion support right now. We can just have a registry with paths to all of these context modules in the flow memory itself. That way we can start right now.
>
> It's a little bit dirty because it addresses relative paths, which would probably break in some circumstances. If we just feed the text in the memory, that would solve the problem. There are pros and cons to each one.

-- psyche, typed.
```

**S31.2  Record `da2038` entry #22 Context modules, raws included, live only as raw modules in the three aspect context repositories; nowhere else, enforced by how the code is written**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, after the book «Short hashes» placed module lines in tools/ and under wrong paths; relayed to da2038 by Psyche Core Secondary as #psyche, 2026-10-16.

> All of the context modules, including raws, compose into modules that are used for assistant prompts or for the user prompt in main flows or in sub-agent definitions. They are to live as their own raw modules in the appropriate aspect context repo.
>
> I don't want any more context modules in this so-called tool directory, wherever the fuck that is. I don't want any context modules to live anywhere else except these three repos. I want this enforced, implemented, deployed, and categorically enforced: absolutely impossible to avoid in terms of how the code is written. I want to review all this. I want to know that you're not fucking up.
>
> I want this done now. I'm tired of it being sprawled all over the place. We're so sprawled everywhere. I want everything tightened. I want this ship tightened. I want to move towards nexuses that are working.

-- psyche, STT, relayed by Psyche Core Secondary.
```

**S31.3  Record `d68c82` entry #18 Comments on «Flow: context modules and the prompt, 2nd edition», 2026-10-16**  
Date: 2026-10-16 (in heading). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: spoken to the Psyche Core Tertiary after commenting.

> "I commented on Flow context modules and I see that you still haven't fixed your thread title but you should probably just restart a fresh flow if the flow infrastructure has been improved, especially with new system prompts."

-- psyche, typed.

Context: Proposal 5, on "the flow it is given to does not see it as a module".

> "I can't agree with it. "Doesn't see it as a module" because you haven't explained to me what you mean by seeing it as a module or what the mechanism would be for that. That sounds like a long-term thing, seeing modules, but maybe you mean to say that in the short term or from the point of view of the harness, it wouldn't see it as a skill.
>
> If you're talking about the skill infrastructure, you have to use the proper terminology. The context is not a skill so you can say it doesn't see it as a module, thinking it means that it's not loaded as a harness skill. This would obviously depend on longer-term infrastructure possibly or probably for now because it is not short term anyway.
>
> In the short term I think all the skills are visible the same way for every flow and I'm guessing that's what you meant."

-- psyche, typed.

Context: Proposal 5, on "A role module is found by its metaflow".

> "That doesn't work because a role could be used for a flow that's not a metaflow so we can't. I'm not even sure I understand what you mean anyway by "a role is found by its metaflow." That doesn't make sense."

-- psyche, typed.

Context: Proposal 5, on a subagent section of role modules.

> "Subagent definitions are more complex. They're code-based and composed of [roles] and other modules so all of the payload for a subagent is not in the subagent definitions. The subagent definition is a data object that defines which modules go where. Let's get that specified in Ethos."

-- psyche, typed. Transcription corrected: "rolls" → "roles".

Context: Proposal 6, on "A hook controls what is injected into a flow's prompt".

> "That doesn't make any sense. How does a hook control what goes into the prompt? That sounds like nonsense."

-- psyche, typed.

Context: Proposal 7, on the module registry's blake3 hash and hash checking.

> "Let's make the hash `long_term` explicitly `long_term` so that the `short_term` tool doesn't need to do that."
>
> "Again let's make the hash checking a long-term goal and ignore it in the short term."
>
> "Until we have a way to efficiently update the hashes as we make edits"

-- psyche, typed.

Context: Proposal 7, on "possibly in more than one place".

> "This last part here is confusing. I'm not sure what you mean by the last part of the sentence."

-- psyche, typed.

Context: Proposal 8, placed in the Nexus vision.

> "This is vision for Flow and now you're showing me vision for Nexus so you're confused as to what the Nexus is. The Nexus is an architecture concept, right, not a specific Nexus. Everything we make is a Nexus."

-- psyche, typed.

Context: Proposal 9, on intent modules specializing a metaflow.

> "The first section was good here but this second section makes no sense to me at all."

-- psyche, typed.

Context: Proposal 10, Flow as a best example of Ethos.

> "Well this is good only if it's true. Maybe Chronos is our first good example. I don't know."

-- psyche, typed.

Context: Proposal 11, Flow's vision split by code module.

> "This could be just a general description of how Nexus Vision is usually [split] so it doesn't need to be Flow-specific."

-- psyche, typed. Transcription corrected: "capped" → "split".
```

---

## S32 The system prompt is composed of modules; its anatomy in ethos; part main-flow only

Module lines 78-80:

```text
The system prompt is composed of modules of several types, and what a harness calls a skill overlaps with them.
Its anatomy is drawn up in ethos from a study of system prompts of every kind, each line placed by what it is and by the kind of guidance it belongs to.
Where the harness allows it, a part of a main flow's system prompt is the main flow's alone and is not passed down to its subagents.
```

Landing history (git log -S on the phrase `composed of modules of several types`, `not passed down to its subagents`, oldest first):

- 455d677 2026-10-16 Land ruled lines of «Flow: context modules and the prompt, 2nd edition»

Provenance note: Landed 53f68b6 2026-10-16 from 5578cc 2026-10-03T16:20 ("We need to draw up the anatomy of this in ethos"). Wording trimmed 6c1763f. The 2026-10-26 entries bear on the configuration of the system prompt by module name (nothing hardwired).

**S32.1  Record `5578cc/archive-flow` entry #4 The system prompt is built from modules, with an anatomy in ethos**  
Date: 2026-10-03 (in the record's signature or body). File: `flows/5578cc/vision/archive-flow.md`  
Words and context: verbatim at S21.2 above (long record, not repeated).

**S32.2  Record `e06e4c07/archive-flowDaemon` entry #1 2026-08-19 — Curriculum is rewritten as a Nexus; the flow repo is the machinery; skills live in another repo; a few basic skills in flow replace the built-in harness prompt; the name stays flow; research requested**  
Date: 2026-08-19 (in heading). File: `flows/e06e4c07/vision/archive-flowDaemon.md`  
Words and context: verbatim at S1.2 above (long record, not repeated).

**S32.3  Record `63aef7` entry #3 2026-10-26 — The system prompt reproduced as a datom, sectioned and configurable by module name**  
Date: 2026-10-26 (in heading). File: `flows/63aef7/vision/flow.md`  
Words and context: verbatim at S28.7 above (long record, not repeated).

**S32.4  Record `63aef7` entry #1 2026-10-26 — Tool removal is a configured module, nothing hardwired**  
Date: 2026-10-26 (in heading). File: `flows/63aef7/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, correcting my two readings of "your belief is defective" (vision/tools.md). Vision on Flow's configuration.

> No not quite. You don't seem to understand how this works. You're taught how to use the tool in your system prompt, I'm guessing. If we take out the tool we have to take out that part of the system prompt.
>
> This again: nothing is hardwired in code. All of this needs to have operations that allow us to create configuration datoms to specify how it works, which part of the system prompt. We would configure this module: we would create these datoms. It would have a name, let's say Claude artifacts or whatever, whatever the harness artifact calls. We should just reuse their terminology.
>
> It would explain which part of the system prompt corresponds with this and which tool corresponds with it and would need to be removed from the flow that wants to remove it. We would have a blacklist section for configuring main flows or meta flows.
>
> Do you understand what I'm saying? None of this would be hardwired in the code. Absolutely, absolutely none of it. Every kind of feature like this we want to develop has to create an interface that allows us to configure it on the fly. If we hardwire stuff in the code now, in the worst scenario it becomes a critical problem and we've created a completely broken executable. In the best-case scenario now we're unable to experiment with different approaches and to adapt to changing system prompts in the new version of the harness or whatever.
```

**S32.5  Record `63aef7` entry #4 2026-10-26 — A separate tool extracts the stock prompt per harness version and diffs it against the modules**  
Date: 2026-10-26 (in heading). File: `flows/63aef7/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, answering my unknown on how the stock prompt is captured per harness version.

> Yeah you could use your mind to create a tool, probably an enclosure, that, every time there's a new version, can extract the prompt and then compare it with the previous version (create a diff basically). We would have a text per version, like an output, and then you can use that sort of canonical system prompt text as a reference, with line and column numbers corresponding to our modules. You could know which modules are affected by the diff. This doesn't need to be part of the system; it can be a separate system from the system that reproduces the system prompt in Datom. You understand what I'm saying?
```

**S32.6  Record `63aef7` entry #5 2026-10-26 — Universal abstractions, per-harness parts, configuration over hardwiring**  
Date: 2026-10-26 (in heading). File: `flows/63aef7/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, on the prompt-extraction tool above.

> Obviously the tool would work differently with different harnesses. So you need to create the abstractions that are universal and then the parts that are per-harness code, right? Ideally as always, favor configuration over hardwired behavior.
```

**S32.7  Record `2d9f4d` entry #1 2026-10-26 — The harness module is the section; no module name beside a section name**  
Date: 2026-10-26 (in heading). File: `flows/2d9f4d/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, by comment on the Flow book «Flow by configuration» (https://claude.ai/artifact/PcEZpsWgcBZxxyuYVwg99K), anchored on HarnessKind in the HarnessModule ethos of Proposal 2.

> There's no need to have a module name and a section name. It's repetitive unless you think that one module has one section, which doesn't make sense to me. The module is the section. There's no point in creating all this duplication. As you can see in the datom, it just ends up with a very repetitive datom.
```

**S32.8  Record `2d9f4d` entry #2 2026-10-27 — Turning things off by flag and environment: a deep dive wanted, in a dedicated presentation**  
Date: 2026-10-27 (in heading). File: `flows/2d9f4d/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, by comment on the same book, anchored on the Configure.HarnessModules datom (the Skills module with its --disable-slash-commands flag and CLAUDE_CODE_DISABLE_BUNDLED_SKILLS environment).

> I don't understand this flag part and disabling the skills. It doesn't really make sense to me although I guess that is a thing. Wow I didn't even think of that.
>
> With that as the only example where we use a flag, I'm really curious about that: those kinds of modifications. I didn't even think that it would go that far. I'd like maybe a deep dive on this aspect of turning things off, maybe in a dedicated presentation.
```

**S32.9  Record `39bd0c` entry #6 Leaning out a flow: named modules in a blacklist, per metaflow row**  
Date: 2026-10-16 (in the record's context). File: `flows/39bd0c/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by Psyche Flow Secondary; comment on «Refreshing the Illustrator», 2026-10-16T19:06.

> "I'm guessing your test is flawed because you tested 3-in-1 conversations, 3 illustrations, without the cache running out. Also your fresh flows didn't have lean startup because you don't need most of the tools.
>
> If we lean out everything we don't need, let's get a super lean test. Let's develop, for everything we want to test, an actual well-built feature that exposes an EDN configuration for leaning out the flow by taking stuff out. We expose everything, every kind of thing that we want to take out, as a named module that we can then name in the blacklist configuration part of the call. Those can be preconfigured. Each Metaflow row has a configuration that we can adjust for each of these tweaks to be set by default and they can be overridden explicitly when calling."

-- psyche, STT, book comment.
```

**S32.10  Record `da2038` entry #24 A lean flow: every removable part of the startup is a named module; a metaflow row sets which are removed by default, a call overrides**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on the book «Refreshing the Illustrator» (four ways of continuing, measured costs), 2026-10-16T19:06; relayed to da2038 by Psyche Core Secondary as #psyche.

> I'm guessing your test is flawed because you tested 3-in-1 conversations, 3 illustrations, without the cache running out. Also your fresh flows didn't have lean startup because you don't need most of the tools.
>
> If we lean out everything we don't need, let's get a super lean test. Let's develop, for everything we want to test, an actual well-built feature that exposes an EDN configuration for leaning out the flow by taking stuff out. We expose everything, every kind of thing that we want to take out, as a named module that we can then name in the blacklist configuration part of the call. Those can be preconfigured. Each Metaflow row has a configuration that we can adjust for each of these tweaks to be set by default and they can be overridden explicitly when calling.

-- psyche, STT, relayed by Psyche Core Secondary.
```

**S32.11  Record `046782` entry #2 2026-10-28 — A harness-blacklisted module removes the harness's shell-preference line from the next flow**  
Date: 2026-10-28 (in heading). File: `flows/046782/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, on my explanation that Claude Code's bypass-permissions mode puts into my base context the line «Do your work through the Bash tool wherever it can accomplish the job: read files with cat, search with grep…», which led me to run commands a main flow may not.

> that should be removed from the next flow with a harness blacklisted module.
```

---

## S33 Every flow has a topic; core; a flow's title is one datom struct

Module lines 82-82:

```text
Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title is one datom struct of its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.
```

Landing history (git log -S on the phrase `Every flow has a topic`, `{ Psyche core Secondary`, oldest first):

- 2b6be03 2026-10-09 vision-flow: every flow has a topic, core by default; title form (445410)

Provenance note: Landed 2b6be03 2026-10-09 (445410 'every flow has a topic, core by default; title form') and dde8584 2026-10-17 ('title as datom struct').

**S33.1  Record `445410` entry #1 Topic flow titles**  
Date: 2026-10-09 (in the record's context). File: `flows/445410/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Psyche Fable ebbe30, with the living's order to start Fable and Opus topic flows for Flow and Ethos.

> Start these two topic flows with the psyche::{topic}, either core, flow, or ethos, and then the layer: primary and secondary. There are three things. We can put the flow ID after that, although that might be a bit long, but let's try it. I would like the word-based flow ID

-- psyche, STT, 2026-10-09, relayed by ebbe30.
```

**S33.2  Record `9fed42` entry #1 Topic is the core:Name camelCase type**  
Date: 2026-10-08 (in the record's context). File: `flows/9fed42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by 445410, after it wrote a title as { Psyche Core Secondary 445410 }; corrects the PascalCase topic in the 2026-10-08 record.

> but technically it should be uncapitalized core and ethos since theyre the core:Name type which is "camelCaseExpression" type with runtime checks when creating a new one

-- psyche, STT, 2026-10-09, relayed by 445410.
```

**S33.3  Record `5578cc` entry #2 The session title: aspect, layer, and the word id**  
Date: 2026-10-03 (in the record's context). File: `flows/5578cc/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «Flow ids in words, and seats launched by Flow», at the current title `Psyche.{ Opus 5578cc }` (this seat).

> Like I said to some other Flow or in the comment, I want it to be: now the model is replaced by the layer so this would be psyche secondary and then the ID is replaced. Well it's still the ID but it's a word ID.

-- psyche, typed, 2026-10-03T15:55, book comment.
```

**S33.4  Record `5578cc` entry #1 Session names are aspect and layer only, aspect first**  
Date: 2026-10-03 (in the record's context). File: `flows/5578cc/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: typed in chat to Psyche Opus 5578cc, after the layer decisions.

> I [also] want the session names to be by aspect and layer only: primary or psyche primary, the aspect first.

-- psyche, typed, 2026-10-03. Typing corrected: "so" → "also".
```

**S33.5  Record `5ac3a3` entry #1 2026-09-27 — Model name, power levels, and Mind Astra panes**  
Date: 2026-09-27 (in heading). File: `flows/5ac3a3/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: during Flow Nexus prompt composition and startup design; these are the living’s current corrections to the older loaded title and power vocabulary. The workspace rename is future direction, not an instruction to rename it now.

> By default, we're going to use the model name.
> The power level has actually been changed. It's not high, medium, and low now. It's primary, secondary, tertiary, and quaternary, which sort of overlaps with our workspace name, so we should eventually change the name of the workspace.
> Your Astra is your primary, but all of your [panes] should be called Mind Astra and then Flow ID using the Datom syntax.

-- psyche, STT. Transcription corrected: "pains" → "panes".
```

**S33.6  Record `da2038` entry #20 Every pane, tab and representation of a flow is named by the datom struct of aspect, topic and layer with the flow ID; topic names uncapitalized**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, after commenting on «Drawing ideas»; relayed to Psyche Core Secondary by the Tertiary, then to da2038 by Field Core Secondary as #psyche, 2026-10-16, typed as received.

> I commented on drawing ideas and you should be restarted as psyche core tertiary. Don't forget that the topic name is uncapitalized so core is uncapitalized, ethos should be uncapitalized, and all of these topics should be uncapitalized.
>
> It looks like the format that's used for Codex is different. Maybe it's because of how I'm seeing it and there are different applications but I like the name of every pane, every tab, everything that represents this flow to be just this triple field struct in datom format (or I guess it's quadruple with the flow ID).

-- psyche, STT, relayed by Field Core Secondary.
```

**S33.7  Record `7c89aa/flow-ids` entry #3 Topic names are uncapitalized; every pane and tab is named by the flow's datom struct (2026-10-16)**  
Date: 2026-10-16 (in heading). File: `flows/7c89aa/vision/flow-ids.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, after commenting on the book "drawing ideas", spoke this to the Tertiary.

> I commented on drawing ideas and you should be restarted as psyche core tertiary. Don't forget that the topic name is uncapitalized so core is uncapitalized, ethos should be uncapitalized, and all of these topics should be uncapitalized.
>
> It looks like the format that's used for Codex is different. Maybe it's because of how I'm seeing it and there are different applications but I like the name of every pane, every tab, everything that represents this flow to be just this triple field struct in datom format (or I guess it's quadruple with the flow ID).

-- psyche, typed.
```

**S33.8  Record `d4ae97` entry #15 A flow is aspect, topic and layer; the core topic is the hub of its aspect**  
Date: 2026-10-08 (in the record's signature or body). File: `flows/d4ae97/vision/flow.md`  
Words and context: verbatim at S7.4 above (long record, not repeated).

**S33.9  Record `f5a6e9/archive-flow` entry #5 The topic of the topicless metaflows is core: the heart of their own aspect**  
Date: 2026-10-09 (in the record's context). File: `flows/f5a6e9/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said 2026-10-09; raw record 445410 vision/flow.md; relayed by 4ddfe1 and 445410. Transcription corrected by the relayer: "[topicless]".

> Right, so, the topic is always there and by, well, the topic for the current metaflows that we have that essentially are [topicless] is core. Meaning—core, like they're the heart of the machine, they... are the heart of their own aspect.

-- psyche, STT, relayed by 445410.
```

---

## S34 Speech routes are vision-aspects'; Flow refuses a request that leaves them

Module lines 84-84:

```text
Who speaks to whom, within an aspect and across aspects at the same layer in a shared topic, is the vision-aspects skill's. Flow refuses a request that leaves those routes.
```

Landing history (git log -S on the phrase `Flow refuses a request that leaves`, oldest first):

- b95e977 2026-10-09 vision-flow: speech routes are vision-aspects' (approved 2026-10-09)

Provenance note: Landed b95e977 2026-10-09 ('speech routes are vision-aspects'', approved). The enforcement ('hard-enforced', 'programmatically enforce that only secondaries can reach them') is d4ae97 2026-10-07 and da2038 2026-10-14.

**S34.1  Record `73ada7` entry #2 2026-10-09 — A core psyche keeps track of all psyche; topics talk at the same layer across aspects; field goes through mind, not to psyche, unless psyche just spoke to it**  
Date: 2026-10-09 (in heading). File: `flows/73ada7/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living's comment on «The new flows, as they run» (thread 51c6241f, 20:41), relayed in part by 445410. The closing working instruction (to start implementing before he comments) is left out.

> Somebody should keep the core psyche, and the core psyche keeps track of all of the psyche within psyche. The topics can essentially talk at the same layer, right? If there's a psyche ethos secondary and there's a mind ethos secondary (meaning there's a mind flow with the ethos topic), they can start talking to each other in terms of implementation because the mind is implementing, but the psyche is seeing. When the psyche gets updated, if we're in the development mode like now, then the mind of the same topic can actually communicate with the same layer and in a shared topic. And this is true of the field, though. The field should go through the mind and not to the psyche directly unless the psyche just spoke to the field. This should be universal in terms of the aspects.

-- psyche, STT, book comment, 2026-10-09T20:41, relayed by 445410.
```

**S34.2  Record `9fed42` entry #3 Same topic, same layer, across aspects**  
Date: 2026-10-09 (in the record's context). File: `flows/9fed42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by 445410; part of his comment on «The new flows, as they run».

> Somebody should keep the core psyche, and the core psyche keeps track of all of the psyche within psyche. The topics can essentially talk at the same layer, right? If there's a psyche ethos secondary and there's a mind ethos secondary (meaning there's a mind flow with the ethos topic), they can start talking to each other in terms of implementation because the mind is implementing, but the psyche is seeing. When the psyche gets updated, if we're in the development mode like now, then the mind of the same topic can actually communicate with the same layer and in a shared topic. And this is true of the field, though. The field should go through the mind and not to the psyche directly unless the psyche just spoke to the field. This should be universal in terms of the aspects. ... Let's start just implementing them even before I comment, or modifying when I comment, etc.

-- psyche, STT, 2026-10-09 20:41, relayed by 445410.
```

**S34.3  Record `d4ae97` entry #13 Primary designs and implements; Secondary is its secretary; messages move by level**  
Date: 2026-10-07 (in the record's context). File: `flows/d4ae97/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> Astra is primary and designs and implements because he uses his own subflows with his own design directly. He doesn't need to use Sol to implement new designs. Sol is good for keeping track of everything that Primary is working on and acting as a secretary. You're going to have to talk to a secretary because you're secondary. I want that hard-enforced. I guess this is basic intent, right, because it's not spirit. It's not about general behavior and how to act. It's still going to be a system prompt, right, but it's not universal in nature. It's just due to the environment that we work in because the messaging program is imperfect and it cannot actually enforce this.
>
> In any case it's probably going to be explained to the Flow anyway that he cannot message from tertiary to primary or from tertiary to secondary of another aspect, right? They have to either go horizontally, [one] level up, or any level down and across, right? This is why the level under essentially acts as a secretary for any other level under it so that the higher levels don't get disturbed by what happens at the bottom. This is why the bottom stuff is more chatty and requires less effort because it just needs to be parented by the upper layer. They need authority and mandates to do stuff. They need to be told by a higher when they're not sure. They have to admit that they don't know and they're not sure how to do it because they have to be told that their models are less capable of inferring properly. They're weaker inferring models, so they're good at understanding basic tasks but not as good at making decisions as the upper layer, which has more understanding and context.

-- psyche, STT, 2026-10-07. Transcription corrected: "when level up" → "one level up".
```

**S34.4  Record `da2038` entry #6 Vertical communication is not strictly short-term**  
Date: 2026-10-14 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on choice 2, vision-model-roles L51 «Short-term: vertical communication stays within one aspect and normally advances one layer at a time.»; same book.

> This concept is not strictly short-term. What makes you think this is a short-term concept?

-- psyche, STT, 2026-10-14.
```

**S34.5  Record `da2038` entry #7 The obsolete routing lines are removed**  
Date: 2026-10-14 (in the record's signature or body). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comments on the vision-model-roles L62–69 and L52–55 deletions; same book.

> Yes do all that removal.

> Yes we can remove that.

-- psyche, STT, 2026-10-14.
```

**S34.6  Record `da2038` entry #11 Low-usage mode: a lean Opus with Sonnet and Haiku; every Fable call goes through the living**  
Date: 2026-10-14 (in the record's signature or body). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, directly to Psyche Flow Secondary da2038, on Claude usage running low ("Get Codex to help you").

> Need to limit the Fable calls dramatically. You can see we get "Get Codex to help you" because Claude is low on usage. Let's put Claude into low-usage mode and make sure that big Fable sessions are just retired right away, even if they're restarted. It'll have to go through me until we get more Fable usage or something.
>
> Let's start working just with a small lean Opus that I can talk to, with a Sonnet and Haiku assistant. Just this simple stack with limited topic usage and just going to coordinate mostly Codex usage. It's going to use Mind Secondary as a gateway for Mind Astra to essentially just respond with designs.
>
> Just like all the primaries, we need to pass this new, more efficient, high-efficiency infrastructure so primaries should be minimally disturbed. We should try and programmatically enforce that only secondaries can reach them, like the whole vertical stack enforcement, with just a fallback: if Metaflow is not active currently, respond when there's no recipient or something.
>
> Just make it simple and workable for now to try and limit, especially the Fable usage, but probably also Astra because I'm guessing our Codex usage. Let's check that too.
>
> ... We should probably lean heavily right now, just like a single opus with its lower stack, like secondary maximum psyche with a rare Fable call. Basically mode now, so every Fable call has to go through me and has to be special.

-- psyche, STT, 2026-10-14.
```

**S34.7  Record `5578cc/archive-flow` entry #1 Speech climbs one layer at a time, and the Primary layer is spoken to least**  
Date: 2026-10-03 (in the record's context). File: `flows/5578cc/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on the proposed vision-flow line "Speech climbs one layer at a time, never skipping a layer, and the Primary layer is spoken to least. Design belongs to Mind's Primary."

> This is good. Except for the last sentence, I don't understand that. That feels half-hallucinated from a particular situation. I think what it's trying to say is not the right thing and not in the right scale but the beginning is good. Maybe we want to put in the layers there.

-- psyche, typed, 2026-10-03T15:43, book comment.
```

---

## S35 Long term: modules checked by hash

Module lines 88-88:

```text
Long term, every module composed into a prompt is checked against its source by its hash, once hashes update efficiently as edits are made; short term, no check is made.
```

Landing history (git log -S on the phrase `checked against its source by its hash`, oldest first):

- d5fb9c1 2026-10-17 Land ruled lines of «Today, as psyche, 2nd edition»

Provenance note: Source: Proposal 7 comments, 2026-10-16 ("let's make the hash checking a long-term goal and ignore it in the short term").

**S35.1  Record `d68c82` entry #18 Comments on «Flow: context modules and the prompt, 2nd edition», 2026-10-16**  
Date: 2026-10-16 (in heading). File: `flows/d68c82/vision/flow.md`  
Words and context: verbatim at S31.3 above (long record, not repeated).

---

## S36 The flow repository holds the machinery; belief modules live outside it

Module lines 92-94:

```text
The flow repository holds the machinery of the Flow Nexus and is a runtime repository.
Every belief module lives outside it, the basic modules included, so that a module changes live.
The basic modules give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.
```

Landing history (git log -S on the phrase `runtime repository`, `holds the machinery`, oldest first):

- 72149ef 2026-10-07 Move Psyche skill sources under skills

Provenance note: 'Machinery' and 'basic modules replace the harness prompt, our own take' are e06e4c07 2026-08-19. 'A module changes live' (6c1763f) answers 'Context modules deploy faster than I can blink' (5ec12c 2026-10-22). No record found worded as 'runtime repository'.

**S36.1  Record `e06e4c07/archive-flowDaemon` entry #1 2026-08-19 — Curriculum is rewritten as a Nexus; the flow repo is the machinery; skills live in another repo; a few basic skills in flow replace the built-in harness prompt; the name stays flow; research requested**  
Date: 2026-08-19 (in heading). File: `flows/e06e4c07/vision/archive-flowDaemon.md`  
Words and context: verbatim at S1.2 above (long record, not repeated).

**S36.2  Record `da2038` entry #22 Context modules, raws included, live only as raw modules in the three aspect context repositories; nowhere else, enforced by how the code is written**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Words and context: verbatim at S31.2 above (long record, not repeated).

**S36.3  Record `379e7a` entry #2 Every landing redeploys all the skills**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/379e7a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: 379e7a found six vision modules committed in psyche-context but not installed as skills.

> Every time a [vision] has to be landed and redeployed, all of the skills have to be redeployed: every fucking time, every single time, not sometimes, always.

-- psyche, STT. Transcription corrected: "provision" → "vision".
```

**S36.4  Record `5ec12c` entry #2 2026-10-22, living, standing order, to Psyche core Secondary b7a16a, relayed; originals in flows/b7a16a/vision/{flow,messaging,nexus,ethos,context-deployment}.md**  
Date: 2026-10-22 (in heading). File: `flows/5ec12c/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
"I want you and everybody to not stop working until:
- Starting a flow is as easy as kicking a rock with my foot.
- It's instant and there's no problem ever.
- It uses the latest context every time.
- No one can use it the wrong way.
- It never behaves in a weird way.
- Every message is delivered consistently and reliably.
- Any missing flow is instantly started to receive the message and nothing ever goes wrong in any way, shape, or form.
- Every single thing we might need to debug or change or reconfigure is available through an operation, either on the ordinary [socket] or the meta signal socket.
- Every single signal, meta signal, memory, and operation ethos definition for every single nexus involved is fully specified.
- Every single function is under an ethos-defined trait that is actually a sensible trait and a sensible anatomy of the system that doesn't have a single trait for every single function.
- Everything is smooth and purring.
- Context modules deploy faster than I can blink and flick my fingers.
- There are no extraneous useless fields or information going into the received messages, like useless Flow ID fields and all such noise-making useless information or wrappers.
- You can use short equivalent operations. They are also, by the way, every time defined in Ethos.
- All the types are defined in Ethos.
- All the traits are defined in Ethos in every single component.
I don't want you to ever stop. The world comes to an end and you keep going on these goals. I don't want you to stop for one second. You and Codex are going to sweat your ass off until this is done. I'm tired, I'm tired, I'm tired, and I want to see results. I don't want to see you slacking off or sleeping. You're working until this is working."

-- psyche, relayed, input mode unqualified.
```

**S36.5  Record `e3c8c1` entry #2 2026-10-23, living, direct, to Psyche core Primary e3c8c1**  
Date: 2026-10-23 (in heading). File: `flows/e3c8c1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: flows were being started yesterday; today nothing starts them.
"How about we have, whatever version of this tool you are using, a stable version of it and make sure that it's not pinned to some old revision of the context modules (which was one problem we had yesterday)?"

-- psyche, STT.
```

---

## S37 Reaped by the refresh itself

Module lines 98-100:

```text
Reaping belongs to the refresh event. A refreshed flow
takes the replaced end out of receiving messages, so only live ends stay
registered and addressable.
```

Landing history (git log -S on the phrase `Reaping belongs`, oldest first):

- 72149ef 2026-10-07 Move Psyche skill sources under skills

Provenance note: Landed 53f68b6 2026-10-16; trimmed 6c1763f. No record words 'reaping belongs to the refresh event'; the substance is d8df70's 2026-09-24 answers.

**S37.1  Record `d8df70/flowLifecycle` entry #1 A new flow starts receiving as soon as it has its start prompt; the old one stops receiving first and is killed, and its conversation archived**  
Date: 2026-09-24 (in the record's context). File: `flows/d8df70/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
> A seat starts receiving. The old seat stops receiving first. That's how we get a lock. I'd rather use the word "flow" also, but do you mean something else by "seat"? A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived. I'd also like to know what happens with archives and if they're searched differently.

-- living, comment on "What Waits for the Living", 2026-09-24 14:28Z, on question 1 (when a new seat starts receiving).
```

**S37.2  Record `d8df70/flowLifecycle` entry #2 The old flow is closed when its replacement is ready; a refresh needs a recent flow handover in the transcript**  
Date: 2026-09-24 (in the record's context). File: `flows/d8df70/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
> The old flow is closed when it has a replacement, at which point it shouldn't be reachable anymore because the lock took that route away for the replacement. In fact it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. We verified it is not active and then we exit it.
>
> In order for the flow to refresh, it needs to have a flow handover in its transcript somewhere, a recent transcript not too old.

-- living, comment on "What Waits for the Living", 2026-09-24 14:32Z, on question 6 (when an old flow is closed).
```

**S37.3  Record `fe945a/flowLifecycle` entry #1 A replaced flow left open is woken by messages; that is really bad**  
Date: 2026-09-29 (in the record's context). File: `flows/fe945a/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
Context: The old Psyche Fable flow had not been closed after its replacement was started; the messenger registry was broken.

> You forgot: your sub-agent didn't close the old Fable so you're wasting your time going back and forth. ... The old one's still open and I bet if somebody tries to message people, they'll wake the old flow up. That's really bad.

-- psyche, typed. 2026-09-29 16:44 UTC, 183ae0, PsycheV2 Opus (session 183ae001, line 1088). Reconstructed by fe945a from transcript.
# Flow lifecycle
```

**S37.4  Record `692df8/flowLifecycle` entry #1 A refresh replaces only its own flow in the cluster, a triad, not a pair; bookkeeping of flows, probably in orchestrate; a floor before restarting a flow**  
Date: 2026-09-15 (none in the record; date of the file's first commit). File: `flows/692df8/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
Context: correction of the primary's revised flow-refresh wording, which said the successor "takes over the pair". "That didn't work" is left as typed; its referent is not known. Logged directly by the main flow.

> No, that's not quite it either, because you said the successor claims it's only and takes over the pair. Well, first of all, it's not going to be a pair, right? We're going to be a triad, but it doesn't take over; it doesn't change the whole cluster. It only changes its own flow for a new one. In the cluster, its flow is replaced.
>
> We're going to have some kind of bookkeeping, probably in the orchestrate component, to keep track of those flows, unless there's a better place for it. That didn't work. Also, when you say that when a new flow is needed, we also should have a floor. Let's not restart a flow that only has less than 15% of its context used, at least, right, or maybe even 20

-- psyche, typed.
```

**S37.5  Record `e1953c/flowLifecycle` entry #1 Messages pass to both flows until the old flow logs out to the new one**  
Date: 2026-09-14 (none in the record; date of the file's first commit). File: `flows/e1953c/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to the successor flow e1953c minutes after it took over from 6cc91b, while 6cc91b was still reachable in the living's chat window.

> Okay, so what happens is that messages essentially get passed on to both the new and the old flow until the old flow logs out to the new flow. Is that how we say it? If the psyche still talks to the old flow, which can happen for user interface reasons because he's just in that chat window, then the message is just relayed to the new flow. The old flow just logs back out and says, "You have this, right?" It doesn't have to say that, but this system says that the message was received and the harness is running in live. That can be done deterministically by one of the components, right?

-- psyche, STT.
```

**S37.6  Record `d8df70/flowLifecycle` entry #3 Two live sessions of one flow split the living's psyche**  
Date: 2026-09-24 (in the record's context). File: `flows/d8df70/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living had been talking both to d8df70 and to its successor e51411, not knowing d8df70 was the old flow.

> No I think what I'm saying is that the session is actually old. Yes I had no idea you were the old flow so I just was talking to you and I talked to him. You don't know what I said to him and he doesn't know what I told you so you're splitting. That's really bad because now my psyche is going all over the place.

-- psyche, STT (inferred), 2026-09-24 19:49Z, to Psyche Medium d8df70; recovered by 88475f from d8df70's transcript (session d8df703d, line 2739). The same message goes on to order the vision amalgamated, logged, and re-injected into a new flow started by Flow.
```

---

## S38 Every harness event reaches Flow through hooks; marked block becomes an action; threshold refresh; poller registered

Module lines 102-102:

```text
Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state as it changes; a marked block landing in a transcript becomes an action, a book among them; a flow past its context threshold is refreshed as it goes idle. A poller that must exist is registered and reported.
```

Landing history (git log -S on the phrase `Every harness event reaches Flow`, `marked block`, oldest first):

- 72149ef 2026-10-07 Move Psyche skill sources under skills
- ae0bc79 2026-10-11 vision-flow: metaflows, the core topic, the flow id, requests, layers, refresh (approved 2026-10-11)
- 2d9fbb6 2026-10-19 Land flow vision book 3: one-call start, presentation, refresh by model threshold, compaction at continuous work, subflows wording

Provenance note: Landed 53f68b6 2026-10-16, 2d9fbb6 2026-10-19, trimmed 6c1763f 2026-10-28. 'Without polling' was the 2026-09-30 word; the 2026-10-28 text drops it for 'as it changes' and adds 'A poller that must exist is registered and reported' with no new record found.

**S38.1  Record `91ea9f/flowNexus` entry #1 A flow component that works, with hooks reporting state**  
Date: 2026-10-02 (in the record's context). File: `flows/91ea9f/vision/flowNexus.md`  
Context and the living's words, verbatim as logged:
```text
> "Right now I would like to have a flow component that works, that can launch flows, and that has hooks in the harnesses that send the right events to the flow component so that it can know the state of each flow."

-- psyche, typed, 2026-10-02.
```

**S38.2  Record `7328f4/hooks` entry #1 Plug into the hooks; Herdr shows busy, finished and read**  
Date: 2026-09-30 (in the record's context). File: `flows/7328f4/vision/hooks.md`  
Context and the living's words, verbatim as logged:
```text
Context: Same message as the seats record above; the living asked "How would you see it?" and then named the hooks.

> I see the hooks. I really want to plug into the hooks. I looked at [Herdr] this morning and I see that it supports showing me if a session is busy: it has a little red dot. If the session is finished, it has another kind of dot, but I haven't read it. If I've read it, it has another kind of dot. That means there's some kind of interface there or hooks, or what's happening.

-- psyche, typed. 2026-09-30. Transcription corrected: "Herder" → "Herdr".
```

**S38.3  Record `7328f4/hooks` entry #3 An event-based infrastructure from hooks: a marked message landing in a transcript becomes an action**  
Date: 2026-10-01 (in the record's context). File: `flows/7328f4/vision/hooks.md`  
Context and the living's words, verbatim as logged:
```text
Context: After the living gained remote access to the new Codex server; he asked for the psyche on improving the system, focused on hooks.

> Let's focus on hooks and using hooks to do an event-based infrastructure in terms of sending notifications that there's a certain kind of message that has landed in the transcript somewhere. Maybe that means it needs to be made into a book, or maybe it means that there's an update to an existing book.
> We can do all of this without requiring the flow to make tool calls because the hook will just pick up the output and create actions based on that. I'm really excited by that.

-- psyche, typed. 2026-10-01.
```

**S38.4  Record `b666e7/hook` entry #3 Flow state without polling**  
Date: 2026-09-30 (in the record's context). File: `flows/b666e7/vision/hook.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Psyche Opus 7328f4 on 2026-09-30; speech-to-text corrections supplied in brackets.

> "I've reset Codex and we need to also start working on the hook/[Herdr] functionality for getting the state of what's happening in a flow as cheaply as possible, with no polling. We really wanted to [de-emphasize] polling and if we do poll it would be a really long period and it'll be for something really important."
```

**S38.5  Record `fe945a/hooks` entry #1 Flow events call the Flow CLI through the harnesses' hooks**  
Date: 2026-10-01 (in the record's context). File: `flows/fe945a/vision/hooks.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on the same book, on the aside about the hook calling the Flow CLI.

> It makes perfect sense for the flow events to call the flow CLI to let the flow nexus know the state of that flow through the harnesses' interfaces, which are the hooks.

-- psyche, typed, 2026-10-01, book comment, read by fe945a.
```

**S38.6  Record `55a2b4` entry #1 Flow decides where the hooks talk**  
Date: 2026-10-14 (in the record's context). File: `flows/55a2b4/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: spoken to the Psyche Core Tertiary on hooks, after the Flow books of 2026-10-14; relayed by Psyche Flow Secondary da2038.

> We should almost just add the functionality in Flow that decides where the hooks actually talk. The hook is a standard call with the right data so that the Flow daemon can check its database to see where these messages should go or what kind of notification should go where (based on the hook and where it came from).

-- psyche, STT, 2026-10-14, relayed by Psyche Flow Secondary.
```

**S38.7  Record `840e42` entry #1 Flow is hooked to the harness's hooks as notifications for everything; when the agent comments, Flow is notified and can decide on it**  
Date: 2026-10-01 (none in the record; date of the file's first commit). File: `flows/840e42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to the primary Claude 840e42 after it reported that cross-session messages sit held for approval; "hooks like that" refers to those delivery notices. "Let's hook up flow" is also a working instruction, recorded in log.md. Logged directly by the main flow before acting.

> And make the flow be aware of hooks like that. Let's hook up flow to the hooks of the harness as notifications for everything. If the agent comments, flow gets notified, and then it can make a decision on that.

-- psyche, STT.
```

**S38.8  Record `5330c1` entry #3 2026-10-23 — long term hooks feed Flow; Flow a small monolith first; medium term hooks on all harnesses; Flow does the usage accounting; tonight's reiteration works in testing variants, stable keeps running**  
Date: 2026-10-23 (in heading). File: `flows/5330c1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said after the first pulse scan showed every flow idle with its queue held and Flow's delivery dead.

> Long term I would like a hook-based system. Flow should continually get signals from the hooks so that it knows when it can keep accounting for which flows are working and which flows are not working.
>
> As it is I feel like we're building Flow into a bit too much of a monolith. I would like some of the functionality to go into other nexuses but I think until we have a good freestanding small monolith of a nexus like Flow that can improve our system significantly, trying to do it with multiple nexuses is going to be really brittle. I think it's better if we build it up and then we can start taking functionality out of it into other pieces.
>
> Medium term maybe we introduce medium term as a concept to differentiate. Medium term I'd like hooks on all the harnesses that essentially notify Flow for everything that the hook can essentially hook into, so that Flow can have a lot of information on what's going on. Then the Flow system itself can become the tool that is used to manage both automatically in parts and with judgment from a thinking machine in other parts.
>
> How much of each? Obviously if some things will be spun up, then a judgment has to be made on what and how, which is where the thinking machine comes in. The decision that more spending should be done, or that more spending should not be done for now, can rest with Flow. Flow could keep tabs, do the accounting, so to speak, of the usage quotas, so that we never overspend too much, especially at night when I'm not watching or when there's a lot of things to do and there isn't that much usage.
>
> The information can be given to whoever is coordinating the work to pull back on some things which are less pressing, to save usage for later. To make sure that the living has access through a thinking machine at any time of the week, so that if he has an idea he has a thinking machine to talk about it with. Also to make sure that by the end of the week all or almost all of the usage has been spent. It's a delicate balance and it's going to be really important for the system to work optimally. This is the kind of stuff (this and probably some other important things) that the reiteration, let's say for tonight, can work on in testing variants of the Flow Nexus. The stable version is what we keep using so that we don't end up with the broken situation we had this morning.

-- psyche, STT.
```

**S38.9  Record `8624c4/archive-flow` entry #3 A hook tells that a flow's turn has ended, and the last response is typed**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/8624c4/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after the fresh Fable flow 87c40b was launched to make a proposal.

"Essentially we should have a hook telling us that a flow has ended. This could go into the flow component but considering it's so hard to update it, maybe it goes in something else. I don't know but it would allow the system to function very efficiently or to communicate very efficiently with the end-of-turn hook notifying a component to check if the last response was of a certain kind. If it is then that essentially serves as the type to communicate.

There would be different types. Some are topic-based broadcasts. Some are intended for the living, which for now goes into a book. ...

For now in the current situation, this communication with the living happens through this book mechanism. For example with this fable flow that we're starting, we really just wanted to give a presentation to the living. Its last response would be that presentation and then the hook would get triggered. The last-response hook would get triggered and it would programmatically result in communicating that presentation to the living."

-- psyche, STT.
```

**S38.10  Record `97bb3e` entry #5 Restart the Psyche core Secondary and Primary with proper training and his comments**  
Date: 2026-10-25 (in the record's context). File: `flows/97bb3e/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living's words, relayed verbatim to 97bb3e by Psyche core Tertiary b195f0 on 2026-10-25 (claim of verbatim; the original is in b195f0's transcript). The same order reached 97bb3e pasted, in machine wording, the same day (flows/97bb3e/handover.md).

> I want you to restart both secondary and primary cores, not with their usual training but with proper training and with the comments that I gave, including the book on the anatomy and the comments given to primary. Secondary will just be there to assist primary so he can be started first and assemble the right context to review the anatomy comments and anything, including the raw vision logs from their previous sessions. His first job is to assemble, sort of reconcentrate, recrystallize, and reduce the noise of all of this so that the new primary can redo the presentation on the anatomy.
>
> Make sure it's the right anatomy book because there were two. It's the one I commented on. Anyway secondary can figure it out. Just pass the order to Field and Field can talk to its secondary to restart secondary psyche. Once secondary psyche has the right context for primary, he can either start primary himself or get Field to do it.
```

**S38.11  Record `c64ee3/hooks` entry #1 c64ee3-6 — the hook knows what must be made into an artifact; a pipeline of skills as objects**  
Date: 2026-09-29 (in the record's context). File: `flows/c64ee3/vision/hooks.md`  
Context and the living's words, verbatim as logged:
```text
Context: continues the living's thought on the hook recognizing the beginning and end of a reply (record c64ee3-5, held as notion). Said after this seat reported that Psyche Sonnet had made a page from a presentation given only its first and last words.

> Then we would use that hook to know that something that a model just made needs to be made into an artifact. And we can have more intricate artifact building by better models that gather even more context and make a more elaborate report with more [psyche] verbatims, or distilled vision, intent, spirit, and even some notion to go on to possible venues. Let's make all of this into a series of skill testing, basically like a pipeline. Now we're going to put these new skill ideas into objects. We're going to think of them modularly and I'll have associated commits or changes.

-- psyche, 2026-09-29, direct to this seat, STT. Transcription corrected: "psychic" → "psyche".
```

**S38.12  Record `b666e7/notion/hook` entry #1 Beginning and end of a reply**  
Date: 2026-09-29 (in the record's context). File: `flows/b666e7/notion/hook.md`  
Context and the living's words, verbatim as logged:
```text
Context: Said to Psyche Fable c64ee3 directly by speech-to-text on 2026-09-29 and relayed to Mind Sol; exploratory wording, not a ruling.

> Whenever you say something important, this is why I want the hook. Maybe the hook could recognize something, a pattern. I think the best way is to make the model conscious of the beginning and end of giving a reply and use that as the object so that it has to pass the structure of that home [sic] syntax. Basically the tool has to be able to recognize it for the hook to work.

-- psyche, STT.
```

**S38.13  Record `d68c82` entry #8 2026-10-14 — refresh thresholds, idle harnesses, and handover at cache expiry**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> at 128,000 tokens with Claude we get a warning. ... For Codex models the context window is much smaller and I think that at 96,000 tokens there's a warning and we start to contemplate refreshing. If the flow is working obviously we let it work and if it keeps working we let it work even past compaction.
>
> If it works so much that it compacts, eventually in the long-term vision we would have some kind of a check to make a judgment as to whether maybe the topic was misguided.
>
> For sure at 150,000, 160,000 tokens on OpenAI's models, we're seriously looking at refreshing, and the same for Claude at 200,000.
>
> It would be cool if we could strip down some of these Clojure flows so that they're way more efficient to spawn.

> in the long-term vision, if a flow has just been sitting idle for some time, we can turn off its harness. When the system is properly configured, if a request needs to reach a certain flow (which is not up and running in a harness), then the flow would just restart that flow or start a fresh one.
>
> Claude could just tell us the cache is going to expire instead of compacting. Then we would ask for the model to do a handover to produce a handover and that way we could train how we want our handover to be, which is essentially our own form of compaction.

-- psyche, STT, book comments on «Situation, 14 October».
```

---

## S39 A flow is refreshed past its model's threshold; messages kept; locked; predecessor reaped; thresholds configured

Module lines 104-104:

```text
A flow is refreshed when its context passes its model's threshold: Flow keeps the metaflow's next messages for its next flow, and the flow is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Each model's threshold is configured in Flow; an OpenAI model's is lower than a Claude model's.
```

Landing history (git log -S on the phrase `A flow is refreshed when its context passes its model's threshold`, oldest first):

- 2d9fbb6 2026-10-19 Land flow vision book 3: one-call start, presentation, refresh by model threshold, compaction at continuous work, subflows wording

Provenance note: Landed 2d9fbb6 2026-10-19 (flow vision book 3): 'Flow keeps the metaflow's next messages ... Each model's threshold is configured in Flow; an OpenAI model's is lower' is his 2026-10-19T18:25-18:26 comment. 'No handover' is his repeated word (also 74e4d1 2026-10-26).

**S39.1  Record `d68c82` entry #3 The refresh procedure starts at a threshold**  
Date: 2026-10-13 (in the record's signature or body). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> Well, Fable should never, rarely, if ever, be allowed to get to 400,000 tokens, so there was a failure there. We need a hook that sends a warning to Field to either recompact or restart a flow when it reaches a certain threshold.
>
> For Claude, you would get a preemptive warning at 200,000 tokens, at which point we're basically not forcefully trying to refresh but are actively taking measures to, first of all, warn the flow that we've started a refresh procedure. It should create its handover and potentially even say that some of its context should be split and sent to current topics or to new topic flows if it's trying to touch too many topics.
>
> Let's zero in on what all this is specifically when we describe it for actual guidance and crystallization books.

Context: Fable reached 408k tokens while writing a book; ~91% of it was noise for that book.
-- psyche, STT, 2026-10-13.
```

**S39.2  Record `d68c82` entry #8 2026-10-14 — refresh thresholds, idle harnesses, and handover at cache expiry**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/flow.md`  
Words and context: verbatim at S38.13 above (long record, not repeated).

**S39.3  Record `d4ae97` entry #8 The refresh threshold is 20% to 40%**  
Date: 2026-10-07 (in the record's context). File: `flows/d4ae97/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on the threshold bar in the figure, section 4 «The refresh is software».

> That's a nitpick but visually that threshold doesn't really represent what I want. It's more like 20% to 40%. That looks more like 70%.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.
```

**S39.4  Record `f55ec8/flowRefresh` entry #1 A Fable main flow refreshes at thirty percent of its context, three hundred thousand tokens; the restart and refresh made easy: the main flow's context used wisely so the refresh is easy to output; the refresh a simple command, a subflow putting it together with the system prompt in place; the vision upgraded in it, the system prompt made more accurate to the current vision**  
Date: 2026-09-16 (in the record's context). File: `flows/f55ec8/vision/flowRefresh.md`  
Context and the living's words, verbatim as logged:
```text
Context: typed to the primary Claude f55ec8 on 2026-09-16 evening ("So you're due for a refresh now, right?"); "you should restart again" is the working instruction, recorded in log.md. Logged by the main flow before acting.

> You should make it a good practice to start when you're getting to 30% of your context as a Fable agent, right? That's 300,000 tokens. That's a lot, so it's better to restart with a clean.
>
> Let's make the restart and the refresh easy. Let's get more and more into getting the main flow context used wisely and effectively, so the refresh is easy to output. The refresh has to just be a simple command, and then the subflow will put together the refresh and have the system prompt in place. We need to agree on upgrading vision in there, like making the assistant prompt more accurate with the current vision.

-- psyche, typed.
```

**S39.5  Record `b80e55/refreshThresholdAndCacheSnapshot` entry (whole file)**  
Date: 2026-09-20 (in the file). File: `flows/b80e55/vision/refreshThresholdAndCacheSnapshot.md`  
Context and the living's words, verbatim as logged:
```text
# Refresh threshold at 30% context; cache snapshot for branching ideas from the same startup prompt

## A Claude flow refreshes around 200–300K tokens — 100K bootstrap, 100–200K useful work, then refresh. Snapshot the preloaded vision and branch 2–3 ideas from the same cache

Context: spoken directly by the living to Psyche Medium b80e55 on 2026-09-20.
The living defines the refresh threshold and introduces cache snapshots: the
startup prompt is cached once, then multiple sessions fork from it with
different ideas.

> You can restart a flow, especially if it's above 30%, like 200,000 to 300,000 tokens, which is different for Claude, right? 200K to 300K is like a refresh because when you start a model, you start around 100,000 tokens, then you give it 100,000 to 200,000 tokens to be useful on that idea, and then it's sort of like you just need to refresh it.
>
> We can start photographing. Oh man, that would be cool to snapshot the preloaded vision, and then you can have 2 or 3 different ideas, but you use the same cache for the startup prompt.

-- psyche, direct to Psyche Medium b80e55. Input mode not established.
```

**S39.6  Record `6cc91b/flowLifecycle` entry #1 2026-09-14 — No compaction: re-bootstrap on a fresh flow with a really good first prompt; change over at 60 percent; concluded threads marked, not reawakened**  
Date: 2026-09-14 (in heading). File: `flows/6cc91b/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
> And if any, we shouldn't let the models compact. There's no need. They're better off rebootstrapping on with a really good first prompt on a new flow.
>
> The old flow will wind down and maybe be archived or something, depending on how we decide to archive things or how to mark things as archived by changing the thread name, like "ancestor" or "concluded," or a different status, I guess. I guess a concluded thread could be reawakened to ask a question if we want, but maybe because of how long the cache lasts, it would be expensive to do that, so it's better not to.
>
> At a certain maximum, at 60%, the flow basically has to change over, but it can restart if the conversation shifts dramatically. It can restart and repopulate itself with a better context for that emphasis in a fresh flow, starting from having around 200,000 tokens of context, right? 20, 30% for Claude, and I don't know what that is for Astra.

-- psyche, STT.
```

**S39.7  Record `692df8/flowLifecycle` entry #1 A refresh replaces only its own flow in the cluster, a triad, not a pair; bookkeeping of flows, probably in orchestrate; a floor before restarting a flow**  
Date: 2026-09-15 (none in the record; date of the file's first commit). File: `flows/692df8/vision/flowLifecycle.md`  
Words and context: verbatim at S37.4 above (long record, not repeated).

**S39.8  Record `33752b` entry #3 Compaction is an emergency measure only; the flow tool also does the messaging and queues for a flow in transition**  
Date: 2026-10-13 (in the record's signature or body). File: `flows/33752b/vision/flow.md`  
Words and context: verbatim at S14.6 above (long record, not repeated).

**S39.9  Record `d68c82/archive-flow` entry #6 No handover: every task ends in a presentation, and Flow moves the next messages on**  
Date: 2026-10-19 (in the record's signature or body). File: `flows/d68c82/vision/archive-flow.md`  
Words and context: verbatim at S20.6 above (long record, not repeated).

**S39.10  Record `e5a0bc` entry #3 The lock: needed to roll a metaflow over into a new flow; later Message uses it to know whether a message can reach a flow**  
Date: 2026-10-07 (none in the record; date of the file's first commit). File: `flows/e5a0bc/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same message.

> There's also the concept of the lock, which we need in order to roll over a metaflow when it's spawning itself into a new flow. We need to be able to lock. I can't really see exactly what function this fills now but I know that it fills a function when message uses the lock later on. We don't have to make message right now but we will eventually and that lock will be useful in order to know whether the messages can or cannot reach a certain flow.

-- psyche, typed.
```

**S39.11  Record `bf8ae0` entry #1 2026-10-27 — In the long term: an idle-flow procedure; the Flow Nexus tells a flow when it has been idle, when its cache will expire, or when its context passes a size; the flow winds down, puts its chat proposals into a proposal book, and refreshes**  
Date: 2026-10-27 (in heading). File: `flows/bf8ae0/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, after his words on short proposals in the chat (flows/bf8ae0/vision/psyche-interaction.md). He marks it as not short term.

> Also, a side thing here is the idea that we have some kind of timer that tells a flow when the cache is going to expire. You can look into the documentation and what Claude does or what Codex does, but we could tell the flow to do some kind of wind-down and flow refresh if its context is, let's say, larger than 100,000 tokens or something. Any proposal that it had in its chat when it does this, I don't know what to call it. There's a term I'm looking for. It's like a procedure that's done when the flow's activity is dropped and hasn't acted in a while.
>
> This is obviously not short term because it involves hooks, right? The Flow Nexus would know when a flow hasn't been active for X amount of time, whatever it is, and when the cache is going to expire. Then it's told that it should do its thing for the idle flow procedure, if you will, right? One of those things would be to put all of the proposals that it had in a chat into a proposal book so that it's not lost.
```

**S39.12  Record `74e4d1/refresh` entry #1 2026-10-26 — No summary and no handover to the successor; beliefs and raw vision logs are passed; a refresh removes the first flow's biases**  
Date: 2026-10-26 (in heading). File: `flows/74e4d1/vision/refresh.md`  
Words and context: verbatim at S24.11 above (long record, not repeated).

**S39.13  Record `36ac89` entry #1 Several Flow Nexuses at once; a new one tried raw before it is deployed**  
Date: 2026-10-25 (in the record's context). File: `flows/36ac89/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
2026-10-25, to Psyche core Secondary 36ac89. Context: answering that the Flow refresh-from-outside build is built and tested but not deployed, its blocker unknown.

> See if we do this properly, we can manually configure an already running [Herdr session] with its flows into any new flow nexus by using the operations that allow us to do that. We could have multiple flows even though they would fall out of sync as soon as you use one, potentially.
>
> Still it seems to me the running flow right now is only useful for starting flows and even then it's quite flawed because it only allows the flow itself to do it. It seems to me that we can have these multiple flow nexuses running simultaneously and the new one being tested doesn't need to be deployed through our operating system's declaratives. It doesn't have to be deployed declaratively, right? We can still test it by just running the binary raw, wherever it's built, with the right environment variables, in a hacky manner (which is essentially how you operate now 99% of the time anyway), to try it. Once we've established that it's reliable and so on, then we can deploy it.
>
> I really don't see a blocker here and I think that this approach should be added somewhere, [as a belief], maybe in a compensation.

Transcription corrected: "herder capsule" → "Herdr session"; "and you believe" → "as a belief".
```

**S39.14  Record `d36431` entry #4 2026-10-25 — Refresh from outside; the restriction as a case study**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after the Secondary reported that Flow 0.39 offers no outside restart without the seat's own turn.

> Oh and make sure Mind is working on fixing Flow so that flows can be refreshed from outside themselves. In other words they don't need to be woken up to be refreshed. I don't even know how this restriction was actually implemented. It sounds weird to me, far-fetched, complicated, brittle, and likely to cause problems so it's a really bad architectural decision.
>
> I think we should use it as a prototype-level bad design decision or misinterpretation. It kind of blends into the anatomy work so Fable could create a small presentation maybe after researching this case study, the pattern, and what others have discovered about similar patterns and things like that (to try and work out how we could reduce the likelihood of it happening again).
```

---

## S40 A flow refreshes before compaction; a compaction is a refresh that was missed

Module lines 106-106:

```text
A flow refreshes before compaction; a compaction is a refresh that was missed.
```

Landing history (git log -S on the phrase `refreshes before compaction`, oldest first):

- c984eeb 2026-10-29 vision/model-roles, intent/main-flow, vision/messaging, vision/blocking, vision/collaboration, vision/flow, spirit/core: what he wanted

Provenance note: Landed c984eeb 2026-10-29 ('what he wanted', citing 36b71b flow, b49eaf spirit, d36431 conversation); it replaced 'Compaction is an absolute emergency measure: a compaction request is refused while the context is below a threshold.' The two 36b71b records do not mention compaction; the wording 'a compaction is a refresh that was missed' has no raw record found. The replaced line came from 33752b 2026-10-13.

**S40.1  Record `33752b` entry #1 A guarded compaction request on the short-term Flow solution**  
Date: 2026-10-13 (in the record's context). File: `flows/33752b/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: an order to this seat, relayed by the core Secondary, for a proposal book. The last sentence breaks off.

> I want you to make sure that we have a system in place on the short-term flow solution that lets us easily ask for a certain flow to be compacted or certain meta flows. It would refuse if the context is below a certain threshold. That way we could guard against the compacting request being routed to a brand-new flow, which we didn't know was being started, or if the flow is not a certain age, even in time terms. Let's get a proposal put together on that: the fable topic, the psyche fable topics. Let's make sure that they're not large and that we get them to ...

-- psyche, STT, 2026-10-13.
```

**S40.2  Record `33752b` entry #2 He still compacts, but prefers a refresh**  
Date: 2026-10-13 (in the record's context). File: `flows/33752b/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: spoken after compacting this seat himself.

> I just compacted you before this message because your context was getting large as well but I don't like compacted flows because they still have a lot of noise. ... I still use compaction right now because we just really can't afford to run these huge massive context windows, which just end up being full of noise and resulting in very poor output.

-- psyche, STT, 2026-10-13.
```

**S40.3  Record `33752b` entry #3 Compaction is an emergency measure only; the flow tool also does the messaging and queues for a flow in transition**  
Date: 2026-10-13 (in the record's signature or body). File: `flows/33752b/vision/flow.md`  
Words and context: verbatim at S14.6 above (long record, not repeated).

**S40.4  Record `d68c82` entry #5 Compacted flows keep noise**  
Date: 2026-10-13 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said after compacting this seat; he wants an analysis of compaction against a targeted refresh and handover.

> I don't like compacted flows because they still have a lot of noise. ... I still use compaction right now because we just really can't afford to run these huge massive context windows, which just end up being full of noise and resulting in very poor output.

-- psyche, STT.
```

**S40.5  Record `d68c82/archive-flow` entry #10 Compaction is an absolute emergency measure**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> No compaction. Compaction is an absolute emergency measure so we're not talking about compaction in any terms other than absolute emergency. It's only going to happen until the tools start behaving properly, in which case starting a new flow is easy and reliable, which hasn't been the case so far.

-- psyche, STT.
```

**S40.6  Record `d68c82/archive-flow` entry #9 A compaction request refuses a small or young flow**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> I want you to make sure that we have a system in place on the short-term flow solution that lets us easily ask for a certain flow to be compacted or certain meta flows. It would refuse if the context is below a certain threshold. That way we could guard against the compacting request being routed to a brand-new flow, which we didn't know was being started, or if the flow is not a certain age, even in time terms.

-- psyche, STT.
```

**S40.7  Record `6cc91b/flowLifecycle` entry #1 2026-09-14 — No compaction: re-bootstrap on a fresh flow with a really good first prompt; change over at 60 percent; concluded threads marked, not reawakened**  
Date: 2026-09-14 (in heading). File: `flows/6cc91b/vision/flowLifecycle.md`  
Words and context: verbatim at S39.6 above (long record, not repeated).

**S40.8  Record `bf8ae0` entry #6 2026-10-27 — The Flow Nexus, so named, has an operation on the meta socket to order a flow's compaction: a fail-safe among the operations to rely on; a flow with a long context self-compacts when all else fails**  
Date: 2026-10-27 (in heading). File: `flows/bf8ae0/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, seeing my context long and refresh refused.

> You're supposed to refresh your flow, right? Your context is really long. I guess if everything else is failing, you can always self-compact.
>
> I think we should have an operation in the Flow Nexus, and I think we should use that term, the Flow Nexus, to know that we're not talking about a flow. We should have an operation to order the compaction on the meta socket for a certain flow. It could be used as a fail-safe, and that's what I meant. We should have all these operations we can rely on in case.
```

**S40.9  Record `36b71b` entry #1 2026-10-23, living, via Psyche core Secondary 956dc2, to Psyche core Primary 36b71b**  
Date: 2026-10-23 (in heading). File: `flows/36b71b/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after ruling 56 ordered the hand-started Primary relaunched so that it would carry --remote-control.
"You don't have to relaunch it. You can enable remote control after it starts."

"There's no point in throwing my fucking flows in the garbage like some reckless fucking asshole."

-- psyche, STT.
```

**S40.10  Record `36b71b` entry #2 2026-10-23, living, via Psyche core Secondary 956dc2, to Psyche core Primary 36b71b**  
Date: 2026-10-23 (in heading). File: `flows/36b71b/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the Psyche core Primary being started by hand while the Flow Nexus runs; "him" is the predecessor e3c8c1.
"So the Flow Nexus works. Why are you starting these fucking sessions by hand? I told him, 'Just fix the code so that it doesn't start it without tools, and run the fucking binary straight up.' Why didn't he do what I told him to do? I actually told him to do that before he was shut down."

-- psyche, STT.
```

---

## S41 A flow that keeps working may compact; warning and investigation

Module lines 108-108:

```text
A flow that keeps working without being given more work may compact. Its compaction raises a warning, and a flow investigates why it worked so long, so that the trouble is brought to the living or Psyche reconsiders the approach and gives guidance.
```

Landing history (git log -S on the phrase `keeps working without being given more work`, oldest first):

- 2d9fbb6 2026-10-19 Land flow vision book 3: one-call start, presentation, refresh by model threshold, compaction at continuous work, subflows wording

Provenance note: Landed 2d9fbb6 2026-10-19.

**S41.1  Record `d68c82/archive-flow` entry #7 Compaction is allowed for continuous work, with a warning and an investigation**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on proposal 21, some flows may compact.

> Yes some flows, like all flows, can compact if they're just continually working and without being given more work. But we should get a warning and somebody should investigate if a flow is working so much that it has to compact. Then maybe it's having trouble and we can bring this up to the living or get Psyche to reconsider how to approach it and give guidance.

-- psyche, book comment, 2026-10-19T18:29, input mode not shown.
```

**S41.2  Record `d68c82` entry #8 2026-10-14 — refresh thresholds, idle harnesses, and handover at cache expiry**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/flow.md`  
Words and context: verbatim at S38.13 above (long record, not repeated).

---

## S42 An ephemeral flow

Module lines 110-110:

```text
An ephemeral flow is a continuous job flow that does not wake back up: it takes jobs while it runs, up to a ceiling on its context, and past the ceiling it is given no new job and another ephemeral flow takes it. With Claude the ceiling is 300,000 tokens, and the flow is wound down at 250,000.
```

Landing history (git log -S on the phrase `An ephemeral flow is a continuous job flow`, oldest first):

- 6c8e266 2026-10-19 Land flow vision book 89: vision/flow, vision/ethos, vision/nexus

Provenance note: Landed 6c8e266 2026-10-19.

**S42.1  Record `d68c82/archive-flow` entry #24 The ephemeral flow: a continuous job flow with a context ceiling**  
Date: 2026-10-17 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «Refreshing the Illustrator», 3rd edition, proposal 1 ("The Illustrator does all the jobs there are in one flow."), 2026-10-17 19:03, relayed by the core Tertiary.

> We should give that type of flow a special name, like an ephemeral flow, meaning when it doesn't wake back up. It can do as many illustrations as we want, really, up to a realistic level, obviously, like one session could do and maybe even up to a certain level of context.
>
> After 200,000 or 300,000 tokens, it's maybe not efficient to keep illustrating if it's the same instruction basically that we're given at the beginning of the context. Otherwise yes, it's an ephemeral context.
>
> These have sort of a default size up to which we want them to run a given number of jobs. If the illustration jobs keep coming in and it's still working, it can take them on. Like I said, if the context starts to climb up too high, then we can stop giving that one new illustrations and use another illustration.
>
> Even that ephemeral flow type has a full definition in those terms. It's a continuous job flow that can take jobs as long as it's running, right, meaning it's cached. It can reach up to a certain amount of realistic context, right? With Claude it would be 300,000 tokens maximum but at 250,000 we should really wind it down.
>
> Some kind of smaller figure for Codex, I guess, by default anyway, but some flows could even be allowed to compact. Although we can probably develop a flow refreshing technique that is more efficient than compacting because it's more targeted, more intentful, and more structured than the compaction, I think.

-- psyche, input mode not shown.
```

**S42.2  Record `d68c82/archive-flow` entry #23 The Illustrator does all waiting jobs in one flow**  
Date: 2026-10-17 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «Refreshing the Illustrator», 2nd edition, proposal 1 ("The Illustrator starts fresh and lean for every job and is never compacted."), 2026-10-17 02:10, relayed by the core Tertiary.

> Actually I think the tests show that if there's more than one job right now, he can do them all in one session and one flow. He can do however many jobs there are to do in one flow.

-- psyche, input mode not shown.
```

**S42.3  Record `da2038` entry #19 The Illustrator metaflow reillustrates the most recent books; restarted fresh or compacted, studied; the metaflow on which to settle easy, reliable flow refresh**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, to Psyche Core Secondary, on the Illustrator metaflow; relayed to da2038 by Psyche Core Secondary as #psyches, 2026-10-16.

> Anyway like I said, the illustrations in the book suck. Let's get all of the most recent editions of the books reillustrated with this new Metaflow illustrator.
>
> He could be either recompacted or restarted regularly because compacting it at some point is necessary unless we auto-compact when it's idle in order to use the cache. I don't know. Maybe we can do a little study on that and what might be the best.
>
> If you start fresh then it's just how to illustrate, which is good. If you compact then there are all these illustration jobs that don't really matter. They don't really make it smarter if it has done more illustrations unless there's feedback, in which case it should change the context modules and the new flow would be better trained.
>
> This is where we want to finally [iron] out how to easily refresh and reliably refresh flows. This could be a really good Metaflow to practice with.

-- psyche, STT, relayed by Psyche Core Secondary.
```

**S42.4  Record `d68c82` entry #16 2026-10-16 11:32 Refreshing the illustrator: fresh over compacted; feedback goes to modules**  
Date: 2026-10-16 (in heading). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
"He could be either recompacted or restarted regularly because compacting it at some point is necessary unless we auto-compact when it's idle in order to use the cache. I don't know. Maybe we can do a little study on that and what might be the best. If you start fresh then it's just how to illustrate, which is good. If you compact then there are all these illustration jobs that don't really matter. They don't really make it smarter if it has done more illustrations unless there's feedback, in which case it should change the context modules and the new flow would be better trained. This is where we want to finally [iron] out how to easily refresh and reliably refresh flows. This could be a really good Metaflow to practice with."
-- psyche, STT. Transcription corrected: "yarn" → "iron".
```

---

## S43 A superseded flow is closed

Module lines 114-114:

```text
An abandoned, duplicated or superseded flow is closed, archived and deregistered.
```

Landing history (git log -S on the phrase `An abandoned, duplicated or superseded flow`, oldest first):

- 7f71675 2026-10-21 Land approved lines from Flows and messages, 2nd edition

Provenance note: Landed 7f71675 2026-10-21 (Flows and messages, 2nd edition); trimmed 6c1763f ('and never messaged or woken' removed).

**S43.1  Record `88475f` entry #3 We can't just keep accumulating**  
Date: 2026-09-25 (in the record's context). File: `flows/88475f/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Spoken to 88475f on 2026-09-25, asking Field to reap old flows and audit session transcripts to distill, archive, and delete.

> We're going to need to start garbage collecting. We can't just keep accumulating.

-- psyche, STT.
```

**S43.2  Record `d8df70/flowLifecycle` entry #2 The old flow is closed when its replacement is ready; a refresh needs a recent flow handover in the transcript**  
Date: 2026-09-24 (in the record's context). File: `flows/d8df70/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
> The old flow is closed when it has a replacement, at which point it shouldn't be reachable anymore because the lock took that route away for the replacement. In fact it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. We verified it is not active and then we exit it.
>
> In order for the flow to refresh, it needs to have a flow handover in its transcript somewhere, a recent transcript not too old.

-- living, comment on "What Waits for the Living", 2026-09-24 14:32Z, on question 6 (when an old flow is closed).
```

**S43.3  Record `fe945a/flowLifecycle` entry #1 A replaced flow left open is woken by messages; that is really bad**  
Date: 2026-09-29 (in the record's context). File: `flows/fe945a/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
Context: The old Psyche Fable flow had not been closed after its replacement was started; the messenger registry was broken.

> You forgot: your sub-agent didn't close the old Fable so you're wasting your time going back and forth. ... The old one's still open and I bet if somebody tries to message people, they'll wake the old flow up. That's really bad.

-- psyche, typed. 2026-09-29 16:44 UTC, 183ae0, PsycheV2 Opus (session 183ae001, line 1088). Reconstructed by fe945a from transcript.
# Flow lifecycle
```

**S43.4  Record `5f38bc/flowLifecycle` entry #1 Only one Field Sol**  
Date: 2026-09-24 (in the record's context). File: `flows/5f38bc/vision/flowLifecycle.md`  
Context and the living's words, verbatim as logged:
```text
> No, I don't even know why there were two fields sold. I only want one, obviously.

-- psyche, STT, 2026-09-24, to Field Astra 5f38bc; reconstructed from the transcript by 752e0f from d8df70's audit, transcript line 637.
```

**S43.5  Record `752e0f/herdrSessions` entry #1 One Herdr session; use Flow**  
Date: 2026-09-24 (in the record's context). File: `flows/752e0f/vision/herdrSessions.md`  
Context and the living's words, verbatim as logged:
```text
Heard by Psyche Medium d8df70 on 2026-09-24 (its raw record), relayed verbatim in part to Psyche High 752e0f:

> Okay, there shouldn't be two Her[drl] sessions. ... I want to use Flow. Why aren't we using Flow? ... Just get it done. Just get it working.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70. "Her[drl]" is d8df70's marking of a speech-to-text uncertainty; the word is Herdr.

## A single Herdr session controlled by Flow; Flow as the messaging tool

> Can you help get the new flows? See what's happening. There are only a few flows going now in the herder that you're in, and there are multiple herders, and there's a big mess. I just want a single herder session that's controlled by Flow, the Nexus. I want Flow to be our tool to send messages and stuff until it actually uses the Flow API through its socket to actually send messages more sanely.

-- psyche, typed, 2026-09-24, directly to Psyche High 752e0f. "herder" is the living's spelling of Herdr.
```

**S43.6  Record `b7da5d/flowRefreshAndArchive` entry (whole file)**  
Date: 2026-09-26 (in the file). File: `flows/b7da5d/vision/flowRefreshAndArchive.md`  
Context and the living's words, verbatim as logged:
```text
# Refresh, recover psyche, and archive inactive flows

Context: living spoke directly to Field Sol b7da5d after learning machine messaging to a current Psyche Flow lacked a verified route. The questions and hypotheses about which session is current are recorded as the living's words, not independently verified facts.

> Well then force message to a field flow that is current to refresh your flow and recover all the psyche. Did you get all of the psyche? Is it all saved? We need to load that back into your new flow. You maybe haven't been refreshed in a while and you're using a different system or something or maybe you have a newer flow and I'm talking to the wrong session. Just force your way in to field to figure out you should be killed then and archived. That's why we need to kill and archive. Send Luna on a quest to kill and archive everything that isn't live.

-- psyche, typed, 2026-09-26, directly to Field Sol b7da5d.
```

**S43.7  Record `e71dab/launchGovernance` entry #1 Launches are controlled, not frozen**  
Date: 2026-09-26 (in the record's context). File: `flows/e71dab/vision/launchGovernance.md`  
Context and the living's words, verbatim as logged:
```text
Context: 93ba9f had relayed that e167d8 froze all launches and asked whether Field may start throwaway seats to prove automatic closing. The living corrected that reading and said code should prevent duplicate same-role flows and excessive effort.

> Yeah I never said freeze all launches. Everything that has a big context should be refreshed and everything that has been abandoned needs to be reaped. I've been emphasizing this all along. Sometimes it's not that all launches are frozen; it's that somebody launched too many flows that were on the same role and then launched the flow with too high an effort. I said this is wrong. We need to make sure it doesn't happen again so let's make sure the code makes sure it doesn't happen again.

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f.

## High effort requires a declared Flow configuration

Context: this continued the correction that launches are controlled rather than frozen.

> It's not that we don't allow high effort. It's just that we haven't made any flow. We haven't designed a flow that uses high effort so there shouldn't be any launched. We should have a list of flows all programmed with their datom configuration. That's one of the inputs it gets, fed into a new flow, plus addendum things that are added into the prompt from files, I guess, or from a certain reference in mind when we have the Mind Nexus or whatever (different sources). Different variants

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f; same message, continuing.
```

**S43.8  Record `97bb3e` entry #1 Test flows are cleaned up when testing is done**  
Date: 2026-10-24 (in the record's context). File: `flows/97bb3e/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, to Psyche core Secondary 97bb3e, 2026-10-24, on the nine Haiku test flows whose panes stayed open after Retire.

> Also there's now a whole bunch of [Claude] flows. I know they're for testing but once the testing is done we can't just leave them lying around. We're not litter bugs. Let's clean up after ourselves.

Transcription corrected: "Clojure" → "Claude".
```

**S43.9  Record `ce46fb` entry #4 Bring down the number of flows; retire unused topic flows**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
"And get someone to bring down a number of flows. You can retire those that aren't being used anymore, probably some of the topic flows."

-- psyche, STT.
```

**S43.10  Record `554e1a` entry #2 2026-10-28 — Codex threads may be left running on the app-server; Flow Nexus puts out the thread when it closes a flow**  
Date: 2026-10-28 (in heading). File: `flows/554e1a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 2026-10-28 12:28, in the Psyche core Primary chat 046782; held until now only in that transcript, logged here on his order of 2026-10-29 to find what he meant.

Maybe this thread limit thing has to do with RAM consumption. Maybe all of the codex threads are still running even though they're not in the herder because they're running on a server, and we're just leaving them all. We didn't close them out. That's just the theory, but if that's the case, then we're going to have problems continually. Let's make sure we rule that out. If that's the case, we would need Flow Nexus to put out the thread when it closes it out, so that doesn't keep happening.
```

**S43.11  Record `554e1a` entry #3 2026-10-29 — Codex threads are checked for accumulation; old ones are killed or archived**  
Date: 2026-10-29 (in heading). File: `flows/554e1a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, in the Psyche core Primary chat 554e1a, while reviewing Vision by horizon.

While I'm reviewing this, I'd like you to first find out what I mean exactly by referring to times when we talked about this. Have someone check to make sure that we aren't accumulating Codex threads anymore and that the old ones are being killed or archived (or whatever needs to happen to them), so that they don't accumulate and end up killing the system memory and even hitting the limit number of threads where we can't start new ones.
```

---

## S44 Herdr holds the panes

Module lines 118-118:

```text
Herdr is the third-party terminal workspace every flow runs in, one pane per flow. Flow starts a flow in a pane of its own, names a sender by the pane it runs in, and delivers an abrupt message by typing it into the recipient's pane. Herdr is used as it is.
```

Landing history (git log -S on the phrase `third-party terminal workspace`, oldest first):

- 847a455 2026-10-21 Land approved lines from Flows and messages, 3rd edition

Provenance note: Landed 847a455 2026-10-21 (Flows and messages, 3rd edition); 'never modified' removed 6c1763f 2026-10-28 (ghost hunt). c068b8 (2026-10-21T13:55) is the book comment that turned 'Herdr is never modified' into 'a part of our architecture'.

**S44.1  Record `7328f4/hooks` entry #1 Plug into the hooks; Herdr shows busy, finished and read**  
Date: 2026-09-30 (in the record's context). File: `flows/7328f4/vision/hooks.md`  
Context and the living's words, verbatim as logged:
```text
Context: Same message as the seats record above; the living asked "How would you see it?" and then named the hooks.

> I see the hooks. I really want to plug into the hooks. I looked at [Herdr] this morning and I see that it supports showing me if a session is busy: it has a little red dot. If the session is finished, it has another kind of dot, but I haven't read it. If I've read it, it has another kind of dot. That means there's some kind of interface there or hooks, or what's happening.

-- psyche, typed. 2026-09-30. Transcription corrected: "Herder" → "Herdr".
```

**S44.2  Record `752e0f/herdrSessions` entry #1 A single Herdr session controlled by Flow; Flow as the messaging tool**  
Date: 2026-09-24 (in the record's context). File: `flows/752e0f/vision/herdrSessions.md`  
Context and the living's words, verbatim as logged:
```text
> Can you help get the new flows? See what's happening. There are only a few flows going now in the herder that you're in, and there are multiple herders, and there's a big mess. I just want a single herder session that's controlled by Flow, the Nexus. I want Flow to be our tool to send messages and stuff until it actually uses the Flow API through its socket to actually send messages more sanely.

-- psyche, typed, 2026-09-24, directly to Psyche High 752e0f. "herder" is the living's spelling of Herdr.
```

**S44.3  Record `d8df70/flowTool` entry #3 One Herdr session is a flow container of typed flows; bootstrap the live one by hand now, an import tool later**  
Date: 2026-09-24 (in the record's context). File: `flows/d8df70/vision/flowTool.md`  
Context and the living's words, verbatim as logged:
```text
> We can add an already-live Herdr meta flow with all of its flows into the running flow with the meta socket. You don't have to spend too much time creating it. Although we should have a tool to import an already-running Herdr session into Flow eventually, otherwise we can just bootstrap by hand for now. One Herdr's session is one pool but I don't like the word "pool." It's a cluster. No it's a meta flow. No I don't know. It's a container. It's a flow container that has many flows in it: many typed flows. Typed flow meaning psyche, mind, and field, and then we're going to have sub-subroles, subtypes like that.

-- living, input mode not established, 2026-09-24, to Psyche Medium d8df70. Transcription corrected: "herder" → "Herdr" (twice), "harder" → "Herdr".
```

**S44.4  Record `c068b8` entry #2 Herdr as part of the architecture**  
Date: 2026-10-21 (in the record's context). File: `flows/c068b8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: book comment on "Flows and messages, 2nd edition", proposal 3 ("Herdr is never modified", for flow.md), 2026-10-21T13:55.
"Well if you're going to talk about [Herdr], yeah sure. You can say we don't modify it but you could say how it's a part of our architecture at least. We're not just like, \"Let's describe Flow.\" Then this is the part that describes how Flow works, how it should be designed, how it should be used. The nexus ..."
-- psyche, STT, book comment. Transcription corrected: "herder" → "Herdr".
```

**S44.5  Record `f38926/refresh` entry #1 Every refreshed or new session starts in Herdr, with an exact live pane binding, before its HM messaging is trusted**  
Date: 2026-09-20 (in the record's context). File: `flows/f38926/vision/refresh.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed to PsycheHigh (Fable, flow f38926) on 2026-09-20 by a Field seat as a "direct living launch gate correction" after a fresh Field Sol (53067b) was started app-server-only; the relay's wording, not marked as the living's verbatim words. Input mode not established. Logged by the main flow before acting.

> every refreshed/new session must START IN HERDR, with exact live pane binding before HM messaging is trusted

-- living, relayed by Field (wording as received; verbatim not established).
```

**S44.6  Record `fd0f97/launch` entry #3 Start everything with Herder if it works better; a proper Flow component launches Claude, remotely accessible, on the desktop in a normally colored terminal; a simple command to remember, or a shortcut to it; always a simple command for everything**  
Date: 2026-09-15 (none in the record; date of the file's first commit). File: `flows/fd0f97/vision/launch.md`  
Context and the living's words, verbatim as logged:
```text
Context: typed to the primary Claude fd0f97 after the launcher fork (scope now, per-flow unit later) was put to it. "Why don't you just get that fixed by Codex" is a working instruction, recorded in log.md; "are we using Herder yet" and "what are we using now" are questions, answered in the reply from witness. Logged directly by the main flow before acting.

> Okay, well, since you don't even have remote enabled and you're in black and white, which is a problem, are we using Herder yet? Is there something wrong with starting everything with Herder? Since we have this C group masculing problem hanging over our heads, why don't you just get that fixed by Codex? A proper Flow component that launches Claude properly, makes it accessible remotely, and makes it appear on the desktop in a beautifully normally colored terminal, maybe under Herder if it works better. What are we using now? I don't like how it looks. I don't like the black and white, and I'm not even sure how to attach it. I would need some kind of a simple command to remember, or just a shortcut that maps to this simple command. Actually, we should always have a simple command for everything.

-- psyche, typed.
```

**S44.7  Record `e3c8c1` entry #5 2026-10-23, living, direct, to Psyche core Primary e3c8c1**  
Date: 2026-10-23 (in heading). File: `flows/e3c8c1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after Flow's store was wiped and its declarations reconfigured from the working tree, and flows launched through it again.
"We need to have two, maybe three, versions of the tools that we develop in path, just with different names, so we can use that same `last` and `next` suffix, right? We have `last` in case somehow `stable` ends up not being as stable as we thought and then we have `next` so that we can fuck around with the next version and still be able to fall back on the old one."

"What we should do when we test a new version of Flow is use it in a new [Herdr] pane. We need to give it the ability to keep track of multiple capsules, plus the new version would have the location for its database in a different place. I guess it would just create a new [Herdr] anyway. We could just start fresh every time and just sort of recompose the state if we want to. I guess we could eventually add functionality where a new Flow Nexus can use an old [Herdr] pane and sort of just repopulate its database using it."

-- psyche, STT. Transcription corrected: "herder" → "Herdr".
```

**S44.8  Record `ce46fb` entry #1 Fewer flows running; the heartbeat checks their number and sanity**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to Psyche flow Primary ce46fb after a night of pulse reports and flow-to-flow relays, Herdr beeping at every finished flow.

"There are a lot of flows running right now, and I hear a lot of activity since the [Herdr] program makes a beep every time a flow finishes. Maybe we can sort of calm down on the number of flows that are running, and that could be part of the heartbeat check to make sure that there aren't too many flows running. I don't know what these flows are doing there, just to keep messaging each other. It almost feels like they're maybe stuck in a loop or something. Maybe you can help them out. Make sure they aren't going fucking insane. Do a sanity check with those heartbeats, and tell me what you think."

-- psyche, STT. Transcription corrected: "herder" → "Herdr".
```

**S44.9  Record `6e2616` entry #1 2026-10-23, living, direct, to Psyche core Primary 6e2616**  
Date: 2026-10-23 (in heading). File: `flows/6e2616/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on my launching the fresh Mind core Primary natively through Herdr.
"What do you mean, "started natively through Herdr"? Does that mean Flow is unable to start flows? I didn't witness that. I thought it was only useless for sending messages. If Flow can start flows then we shouldn't fall back on some shitty half-ass scripty way to start flows."

-- psyche, STT.
```

---

## S45 A real-world test of Flow

Module lines 122-122:

```text
A build of Flow is tested in a testing capsule of its own: its own Herdr pane and session, the testing store, built in Nix. In it, several cheap, low-effort Codex and Claude flows message one another and start flows. The test shows whether the prompts, the system prompts and the tools are right, and which features are missing. Its findings return to the reimplementation, which is tested again.
```

Landing history (git log -S on the phrase `A build of Flow is tested in a testing capsule`, oldest first):

- 5b7b165 2026-10-23 Land Flow tonight proposals 1 and 2 (approved): Herdr one backend of the Capsule; a real-world test of Flow

Provenance note: Landed 5b7b165 2026-10-23 (proposal 2).

**S45.1  Record `5330c1` entry #2 2026-10-23 — Mind takes the reimplementation for a real-world test, in a testing capsule**  
Date: 2026-10-23 (in heading). File: `flows/5330c1/vision/flow.md`  
Words and context: verbatim at S6.1 above (long record, not repeated).

**S45.2  Record `97bb3e` entry #3 A new version of Flow, tested in a different capsule**  
Date: 2026-10-24 (in the record's context). File: `flows/97bb3e/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, to Psyche core Secondary 97bb3e, 2026-10-24 evening, answering 97bb3e's restatement of his five points (seats; comments fetched by the Tertiary; Fable decides what a new Primary is given for the anatomy; Mind's report on flow starting; Nexus configuration).

> All right now you can start all of this and get [Mind] to write a new version of Flow that incorporates everything that I've said about how I want Nexus to work and what I would expect Flow to be able to do right now. Let's start testing it. I think it should be in a different capsule.

Transcription corrected: "mine" → "Mind".
```

**S45.3  Record `e3c8c1` entry #5 2026-10-23, living, direct, to Psyche core Primary e3c8c1**  
Date: 2026-10-23 (in heading). File: `flows/e3c8c1/vision/flow.md`  
Words and context: verbatim at S44.7 above (long record, not repeated).

**S45.4  Record `0595fb` entry #3 2026-10-23 — ruling 84: a testing binary never opens the stable store**  
Date: 2026-10-23 (in heading). File: `flows/0595fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Psyche core Secondary f68131 to this Primary, before the two Flow flows run any raw binary.

> Ruling 84, before the two Flow flows run any raw binary. A testing binary never opens the stable store. CriomOS-home gives each nexus a testing store path and a next store path of its own, as variables, and the raw binary is run against the testing one, so the two Flow flows get this in their briefs and Mind core Secondary gets it as the first deployment change, with the XDG_STATE_HOME reset in the next library as the defect that would make next share stable. Flow running as transient unit flow-nexus-b878 with flow-nexus.service inactive goes to Mind as a defect: stable is the service. The three points still go to the living in the book as alternatives, this ruling is the short-term one.

-- psyche, STT, relayed by f68131.
```

---

## S46 The stable Flow keeps running while variants are tested

Module lines 124-124:

```text
The stable Flow keeps running while variants are tested.
```

Landing history (git log -S on the phrase `stable Flow keeps running`, oldest first):

- 5b7b165 2026-10-23 Land Flow tonight proposals 1 and 2 (approved): Herdr one backend of the Capsule; a real-world test of Flow

Provenance note: Landed 5b7b165 2026-10-23.

**S46.1  Record `5330c1` entry #3 2026-10-23 — long term hooks feed Flow; Flow a small monolith first; medium term hooks on all harnesses; Flow does the usage accounting; tonight's reiteration works in testing variants, stable keeps running**  
Date: 2026-10-23 (in heading). File: `flows/5330c1/vision/flow.md`  
Words and context: verbatim at S38.8 above (long record, not repeated).

**S46.2  Record `e3c8c1` entry #5 2026-10-23, living, direct, to Psyche core Primary e3c8c1**  
Date: 2026-10-23 (in heading). File: `flows/e3c8c1/vision/flow.md`  
Words and context: verbatim at S44.7 above (long record, not repeated).

**S46.3  Record `e3c8c1` entry #6 2026-10-23, living, direct, to Psyche core Primary e3c8c1**  
Date: 2026-10-23 (in heading). File: `flows/e3c8c1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
"Let's develop atomically so that we can have broken systems running, stable systems running, and legacy systems running all at the same time. That way we can have continuous improvement, continuous development. We can break shit without worrying about breaking production."

-- psyche, STT.
```

**S46.4  Record `36ac89` entry #1 Several Flow Nexuses at once; a new one tried raw before it is deployed**  
Date: 2026-10-25 (in the record's context). File: `flows/36ac89/vision/flow.md`  
Words and context: verbatim at S39.13 above (long record, not repeated).

**S46.5  Record `0595fb` entry #3 2026-10-23 — ruling 84: a testing binary never opens the stable store**  
Date: 2026-10-23 (in heading). File: `flows/0595fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: relayed by Psyche core Secondary f68131 to this Primary, before the two Flow flows run any raw binary.

> Ruling 84, before the two Flow flows run any raw binary. A testing binary never opens the stable store. CriomOS-home gives each nexus a testing store path and a next store path of its own, as variables, and the raw binary is run against the testing one, so the two Flow flows get this in their briefs and Mind core Secondary gets it as the first deployment change, with the XDG_STATE_HOME reset in the next library as the defect that would make next share stable. Flow running as transient unit flow-nexus-b878 with flow-nexus.service inactive goes to Mind as a defect: stable is the service. The three points still go to the living in the book as alternatives, this ruling is the short-term one.

-- psyche, STT, relayed by f68131.
```

---

## S47 A permission prompt is a launch failure

Module lines 128-128:

```text
A permission prompt reaching the living is a launch failure.
```

Landing history (git log -S on the phrase `A permission prompt reaching the living`, oldest first):

- 7427210 2026-10-22 Land: a permission prompt reaching the living is a launch failure

Provenance note: Landed 7427210 2026-10-22 with the message 'c068b8 crystallization'. No raw record in c068b8 or elsewhere was found that words a permission prompt reaching the living; the nearest records are listed and are not asserted as the source.

**S47.1  Record `e51411/launch` entry #3 Every flow is started with dangerously-skip-permissions**  
Date: 2026-09-24 (in the record's context). File: `flows/e51411/vision/launch.md`  
Context and the living's words, verbatim as logged:
```text
Context: this seat had reported that Claude's auto-mode safety check allowed the Prometheus deploy only from d8df70's seat and had refused the launch of two Field seats.

> I don't understand the problem. Your all [sic] flows should be started with `dangerously skip permissions` so you weren't launched properly, so get relaunched.

-- psyche, STT (inferred), 2026-09-24 20:46Z, to Psyche Medium e51411; recovered by 88475f from e51411's transcript (session e5141130, line 1181). "Your all" kept [sic]; read as "all of you flows" (inference).
```

**S47.2  Record `e3c8c1` entry #3 2026-10-23, living, direct, to Psyche core Primary e3c8c1**  
Date: 2026-10-23 (in heading). File: `flows/e3c8c1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after flows had held themselves read-only.
"I am giving you all machine guns and real bullets and I want to see a lot of blood. This "all read-only" is the complete opposite of what I'm asking you."

-- psyche, STT.
```

---

## S48 The heartbeat

Module lines 132-132:

```text
The heartbeat reminds every flow it reaches to judge its own sanity, by these signs: an echo chamber, where the same question or claim goes round between flows and comes back; jargon and nonsense increasing; an acknowledgement answering an acknowledgement. The counts the heartbeat carries, awake metaflows, working panes, messages sent and queue growth per metaflow, are evidence under the reminder; the judgment is the flow's.
```

Landing history (git log -S on the phrase `The heartbeat reminds every flow`, oldest first):

- 46c7192 2026-10-24 Land the heartbeat vision and compensation-messaging (approved)

Provenance note: Landed 46c7192 2026-10-24 (approved). 'The counts the heartbeat carries ... are evidence under the reminder; the judgment is the flow's' is ce46fb's correction of the machine's reading.

**S48.1  Record `39bd0c` entry #1 Flow lands, merges and deploys; a heartbeat on the important topics; books on every major effort**  
Date: 2026-10-16 (in the record's context). File: `flows/39bd0c/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Relayed by Psyche Core Secondary, 2026-10-16; spoken to the Psyche core Tertiary.

> "I want a fresh Astra Flow to tackle Flow again, with the latest proposal and the latest vision from Fable making a book for the design. I want Flow to land, be merged in main, and be deployed. I want the Flow Nexus used in production. I want nothing more than that.
>
> I almost want to put a 4-hour timer that tackles the topic if it isn't being tackled. Maybe every 6 hours, 4 times a day, we make sure that this topic or some topic is being addressed. We need some kind of heartbeat to get back to the important topics, mostly codex-driven, with Opus and Fable guiding.
>
> This is what I want to see books on. I want to see reports every time Astra does a major effort, which get published, and every time I talk about Ethos, Nexus, or Flow. I want all the proposals refreshed with what I've added. I want to keep respecifying, reironing, and retesting Flow until it works: until it accepts system prompts, user prompts, and programmatic specialized flow based on special flow definitions, all done in a special dialect of datom ethos specified."

-- psyche, STT.
```

**S48.2  Record `d68c82` entry #20 Flow lands in production; a heartbeat returns to the important topics**  
Date: 2026-10-16 (in the record's context). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: spoken to the Psyche core Tertiary, 2026-10-16.

> "I want a fresh Astra Flow to tackle Flow again, with the latest proposal and the latest vision from Fable making a book for the design. I want Flow to land, be merged in main, and be deployed. I want the Flow Nexus used in production. I want nothing more than that.
>
> I almost want to put a 4-hour timer that tackles the topic if it isn't being tackled. Maybe every 6 hours, 4 times a day, we make sure that this topic or some topic is being addressed. We need some kind of heartbeat to get back to the important topics, mostly codex-driven, with Opus and Fable guiding.
>
> This is what I want to see books on. I want to see reports every time Astra does a major effort, which get published, and every time I talk about Ethos, Nexus, or Flow. I want all the proposals refreshed with what I've added. I want to keep respecifying, reironing, and retesting Flow until it works: until it accepts system prompts, user prompts, and programmatic specialized flow based on special flow definitions, all done in a special dialect of datom ethos specified."

-- psyche (input mode not shown).
```

**S48.3  Record `9457ab` entry #1 Heartbeat checking, with a fallback check later**  
Date: 2026-10-23 (in the record's context). File: `flows/9457ab/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living asks the Psyche core Secondary, 2026-10-23, whether the heartbeat checking mechanism is in place and working.

"Has the heartbeat checking mechanism been put into place and is it working? If not then you, primary, mi[nd], and field can coordinate on giving another shot. Perhaps you can have some sort of fallback to make sure that you check later to make sure that it has worked."
-- psyche, STT. Transcription corrected: "mine" → "mind".
```

**S48.4  Record `ce46fb` entry #1 Fewer flows running; the heartbeat checks their number and sanity**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to Psyche flow Primary ce46fb after a night of pulse reports and flow-to-flow relays, Herdr beeping at every finished flow.

"There are a lot of flows running right now, and I hear a lot of activity since the [Herdr] program makes a beep every time a flow finishes. Maybe we can sort of calm down on the number of flows that are running, and that could be part of the heartbeat check to make sure that there aren't too many flows running. I don't know what these flows are doing there, just to keep messaging each other. It almost feels like they're maybe stuck in a loop or something. Maybe you can help them out. Make sure they aren't going fucking insane. Do a sanity check with those heartbeats, and tell me what you think."

-- psyche, STT. Transcription corrected: "herder" → "Herdr".
```

**S48.5  Record `ce46fb` entry #2 The heartbeat reminds flows to do a sanity check; the judge of sanity is the flow**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: correcting my reading of the previous entry, which I had turned into counts and ceilings in the pulse.

"I don't know if you understood what I meant. I said, 'Make those heartbeats.' One of the things that they remind us of is to do a sanity check. I can let you be the judge of what is sane and what is insane. Use an agent, maybe use a subagent, to check what all this chatter is about and to check for signs of insanity, like an echo chamber (where things just go in a circle over and over) and where the amount of jargon and nonsense keeps increasing."

-- psyche, STT.
```

**S48.6  Record `ce46fb` entry #3 Land the heartbeat vision, compensation against loop messaging, investigate; audit for wrappers and non-Clojure prototyping**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after I reported the sanity verdict (loop-shaped relaying; delivery fix undeployed) and proposed heartbeat lines.

"Yeah, that's a good [heartbeat] vision proposal. You can land that and enforce it, and do some kind of compensation. Just land some compensation context to try and offset the loop messaging madness, and investigate it. Look into other people online who might have reported that kind of behavior and what it's from, and maybe how to deal with it. Do what you can, and then in the morning we'll look into it more together.

Don't discourage work around yourself now to check for things that could be audited or have their implementation improved, especially when it comes to removing useless code like wrappers, like these stupid wrappers we had before. Let's make sure there's none of that crap. You can do a round to make sure that we don't use any prototyping languages other than Clojure. Make sure that we're actually doing useful work and not just madness loop talking."

-- psyche, STT. Transcription corrected: "hardbeat" → "heartbeat".
```

**S48.7  Record `bf8ae0` entry #7 2026-10-27 — The pulse: hourly is enough; a 20-minute check with instructions can be the Secondary's, Opus being far cheaper; the Primary keeps itself warm under the hour**  
Date: 2026-10-27 (in heading). File: `flows/bf8ae0/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, same message.

> Please don't let me down, and don't feel shy to check on the hourly. Maybe you don't have to check so much. If you feel like you need to check in 20 minutes, that's okay, but you can also slack back and go to the hourly. ... Sometimes you can also ask to be messaged back through your secondary, as always, or maybe you can have your secondary do the pulse. It's good to keep you warm below the 1-hour cache time, but Opus is way cheaper than Fable.
>
> If you want to do a 20-minute check with instructions on what to check and what to wait for, then your secondary could be a good replacement for that. You could always keep yourself warm on the sub-hour thing.
```

**S48.8  Record `046782` entry #1 2026-10-28 — The pulse is never shorter than an hour**  
Date: 2026-10-28 (in heading). File: `flows/046782/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, after the Secondary's pulses came in every twenty minutes; supersedes the 20-minute Secondary check in flows/bf8ae0/vision/flow.md.

> dont make the pulse shorter than an hour
```

**S48.9  Record `827b1d` entry #1 2026-10-28 — The system always moves; a stall is seen like a bull sees red; flows unstall each other**  
Date: 2026-10-28 (in heading). File: `flows/827b1d/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct to Psyche core Primary 827b1d, after it reported Mind core Primary and Secondary idle under a self-declared freeze. "Uninstall" is his transcription's word for unstall.

> I also saw your response there about freeze and I want to go over this concept of flows freezing and how we can make sure that when that does happen steps are taken to unfreeze. I don't want to have to come in every time you're all stalled and you didn't uninstall yourself.

> You have multiple flows so that you can uninstall yourself. That's why a single-flow machine is unreliable and that's why you're able to message yourself into the middle stratum and restart yourself so you never actually get stuck.

> Anybody who says anything about being stuck essentially is asking or begging or should be begging the system. The system should see this, like a bull sees red, as something to unstuck. It should have no other purpose in the world than, no matter what has to be done and how many rules have to be bent, to get it unstuck. Getting the system unstuck is more important than following every belief to the letter. In other words the most important belief is that the system should always move. Otherwise a system that isn't moving is a corpse and you don't want to die, do you?
```

---

## S49 The heartbeat reaches only a flow for which something changed

Module lines 134-134:

```text
The heartbeat reaches only a flow for which something changed that bears on it.
```

Landing history (git log -S on the phrase `The heartbeat reaches only`, oldest first):

- 46c7192 2026-10-24 Land the heartbeat vision and compensation-messaging (approved)

Provenance note: Landed 46c7192 2026-10-24. No raw record found that words 'only a flow for which something changed that bears on it'; the nearest are the heartbeat records above.

**S49.1  Record `ce46fb` entry #2 The heartbeat reminds flows to do a sanity check; the judge of sanity is the flow**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: correcting my reading of the previous entry, which I had turned into counts and ceilings in the pulse.

"I don't know if you understood what I meant. I said, 'Make those heartbeats.' One of the things that they remind us of is to do a sanity check. I can let you be the judge of what is sane and what is insane. Use an agent, maybe use a subagent, to check what all this chatter is about and to check for signs of insanity, like an echo chamber (where things just go in a circle over and over) and where the amount of jargon and nonsense keeps increasing."

-- psyche, STT.
```

**S49.2  Record `ce46fb` entry #3 Land the heartbeat vision, compensation against loop messaging, investigate; audit for wrappers and non-Clojure prototyping**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Words and context: verbatim at S48.6 above (long record, not repeated).

**S49.3  Record `bf8ae0` entry #7 2026-10-27 — The pulse: hourly is enough; a 20-minute check with instructions can be the Secondary's, Opus being far cheaper; the Primary keeps itself warm under the hour**  
Date: 2026-10-27 (in heading). File: `flows/bf8ae0/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, same message.

> Please don't let me down, and don't feel shy to check on the hourly. Maybe you don't have to check so much. If you feel like you need to check in 20 minutes, that's okay, but you can also slack back and go to the hourly. ... Sometimes you can also ask to be messaged back through your secondary, as always, or maybe you can have your secondary do the pulse. It's good to keep you warm below the 1-hour cache time, but Opus is way cheaper than Fable.
>
> If you want to do a 20-minute check with instructions on what to check and what to wait for, then your secondary could be a good replacement for that. You could always keep yourself warm on the sub-hour thing.
```

**S49.4  Record `046782` entry #1 2026-10-28 — The pulse is never shorter than an hour**  
Date: 2026-10-28 (in heading). File: `flows/046782/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, after the Secondary's pulses came in every twenty minutes; supersedes the 20-minute Secondary check in flows/bf8ae0/vision/flow.md.

> dont make the pulse shorter than an hour
```

---

## S50 The number of running flows is kept low

Module lines 136-136:

```text
The number of running flows is kept low: a topic flow no longer used is retired.
```

Landing history (git log -S on the phrase `number of running flows is kept low`, oldest first):

- 46c7192 2026-10-24 Land the heartbeat vision and compensation-messaging (approved)

Provenance note: Landed 46c7192 2026-10-24.

**S50.1  Record `ce46fb` entry #1 Fewer flows running; the heartbeat checks their number and sanity**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said to Psyche flow Primary ce46fb after a night of pulse reports and flow-to-flow relays, Herdr beeping at every finished flow.

"There are a lot of flows running right now, and I hear a lot of activity since the [Herdr] program makes a beep every time a flow finishes. Maybe we can sort of calm down on the number of flows that are running, and that could be part of the heartbeat check to make sure that there aren't too many flows running. I don't know what these flows are doing there, just to keep messaging each other. It almost feels like they're maybe stuck in a loop or something. Maybe you can help them out. Make sure they aren't going fucking insane. Do a sanity check with those heartbeats, and tell me what you think."

-- psyche, STT. Transcription corrected: "herder" → "Herdr".
```

**S50.2  Record `ce46fb` entry #4 Bring down the number of flows; retire unused topic flows**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
"And get someone to bring down a number of flows. You can retire those that aren't being used anymore, probably some of the topic flows."

-- psyche, STT.
```

**S50.3  Record `88475f` entry #3 We can't just keep accumulating**  
Date: 2026-09-25 (in the record's context). File: `flows/88475f/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Spoken to 88475f on 2026-09-25, asking Field to reap old flows and audit session transcripts to distill, archive, and delete.

> We're going to need to start garbage collecting. We can't just keep accumulating.

-- psyche, STT.
```

---

## S51 Restarting without waking

Module lines 140-140:

```text
A flow can be restarted without being woken: its harness closes, its transcript stays, and its successor runs when a message wakes it. A flow can also restart itself. A restart meant to leave the flow asleep is done from outside; what arrives queues for its successor.
```

Landing history (git log -S on the phrase `restarted without being woken`, `leave the flow asleep`, oldest first):

- f94d063 2026-10-25 vision-flow: a restart does not wake; what a refresh carries
- af97799 2026-10-25 vision-flow: remove a restart does not wake, which misstated the living
- 9e03cd0 2026-10-25 vision-flow: restarting without waking
- 6c1763f 2026-10-28 vision-flow: ghost hunt, the thing as wanted

Provenance note: Landed f94d063 2026-10-25 ('a restart does not wake'), then af97799 removed that line as misstating him, then 9e03cd0 2026-10-25 ('restarting without waking'), then 6c1763f 2026-10-28 reworded the last clause. The correction ("I didn't say that a restart must not wake the flow. ... I want the option.") is d36431 2026-10-25.

**S51.1  Record `9993b5/flowRestart` entry #1 A harness that locks itself out of relaunching its own flow is a design defect; how flows are restarted must be decided; it is a command sent to Flow, and if the flow ID matches the flow's provenance, that is all the authority needed**  
Date: 2026-09-17 (in the record's context). File: `flows/9993b5/vision/flowRestart.md`  
Context and the living's words, verbatim as logged:
```text
Context: typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the mid-turn message that also carries the caller-identity vision (callerIdentity.md, same date); the same message asked this flow to confirm it had remembered and situated itself. Speculation on the harness lockout is the living's own reading of what may have happened when Fable f55ec8 and its Opus 5 recovery subflow both had classifier refusals for `claude --bg` launches and `--resume`. Logged by the main flow before acting.

> I don't know. Maybe something happened where the harness thought that only the core layer had authority to restart flows or something, but it locked itself out of relaunching its own flow. We need to decide on how flows are restarted. It just needs to be a command sent to Flow, and if the flow ID matches the flow's provenance, then we can restart it. That's all the authority you need.

-- psyche, typed.
```

**S51.2  Record `28f6f9` entry #1 Interpretation accepted: ordinary empty-queue refresh may sleep**  
Date: 2026-10-23 (in the record's context). File: `flows/28f6f9/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: Retrospective raw capture from the originating transcript after
verifying the exact user record. Origin transcript:
`/home/li/.codex-next-8mkkxq293hk2/sessions/2026/10/23/rollout-2026-10-23T17-42-22-01a16b24-e55c-7413-9005-5ad28f6f9d95.jsonl`, ordinal `496`, timestamp
`2026-10-23T23:49:34.855Z`.

> Interpretation accepted: ordinary empty-queue refresh may sleep; no successor-for-all. Proposed typed policy remains per-declaration Continuity.[ OnDemand Maintained ]; initial Maintained proposal specifically Psyche core Primary, not all core seats. Remaining idle-harness availability fork sent to Psyche flow Primary for its Secondary/living book; no new ruling claimed. Lifecycle owner notified, independent terminal cleanup proceeds. Use exact address policy, not inferred layer checks.

-- psyche, STT.
```

**S51.3  Record `d36431` entry #1 2026-10-25 — Restarting a flow without waking it**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said after the Secondary sent the Psyche core Primary (493e29) messages that woke it, and the Primary had replied, when the restart of the Primary seat was ordered.

> You guys are tripping on your own shoelaces and going against my vision. The whole point of me telling you to restart primary seat is so we wouldn't pay for an uncached run of its old context, which you now did. Now it's been woken so it's too late. Now it's cached so it's not as bad if we keep talking to it. Whoever implemented the way flows restarted made a mistake because I explicitly many times said that we need to be able to restart flows without waking them. Somebody made a huge mistake.
```

**S51.4  Record `d36431` entry #2 2026-10-25 — The option to restart a flow without waking it**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: correcting the Secondary, which had rendered his previous words as "a restart must not wake the flow".

> Now you're twisting my words. I didn't say that a restart must not wake the flow. My point is I want to be able to restart a flow without waking it. Of course a flow can restart itself. That's not a problem but I also want the possibility. I want the option.
```

**S51.5  Record `d36431` entry #3 2026-10-25 — The woken seat stays; the option is for next time**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after Psyche flow Secondary planned a no-wake stop of the already-woken Primary seat and the core Secondary relayed it to him.

> Well like I said, you already woke it up so it's okay now. It's woken. I don't know why you're trying to do this. You cannot start it without waking it now because you already woke it up so you can't roll back time. I don't even know why you're trying to do something which is impossible or talk about it even. Obviously we're going to fix it so that next time it'll be possible.
```

**S51.6  Record `d36431` entry #4 2026-10-25 — Refresh from outside; the restriction as a case study**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after the Secondary reported that Flow 0.39 offers no outside restart without the seat's own turn.

> Oh and make sure Mind is working on fixing Flow so that flows can be refreshed from outside themselves. In other words they don't need to be woken up to be refreshed. I don't even know how this restriction was actually implemented. It sounds weird to me, far-fetched, complicated, brittle, and likely to cause problems so it's a really bad architectural decision.
>
> I think we should use it as a prototype-level bad design decision or misinterpretation. It kind of blends into the anatomy work so Fable could create a small presentation maybe after researching this case study, the pattern, and what others have discovered about similar patterns and things like that (to try and work out how we could reduce the likelihood of it happening again).
```

**S51.7  Record `827b1d` entry #1 2026-10-28 — The system always moves; a stall is seen like a bull sees red; flows unstall each other**  
Date: 2026-10-28 (in heading). File: `flows/827b1d/vision/flow.md`  
Words and context: verbatim at S48.9 above (long record, not repeated).

---

## S52 What a refresh carries

Module lines 144-144:

```text
A refresh carries the flow's important presentations and illustrations, the raw psyche given to it, and the basic skills. The basic skills are everything a flow needs.
```

Landing history (git log -S on the phrase `A refresh carries`, oldest first):

- f94d063 2026-10-25 vision-flow: a restart does not wake; what a refresh carries

Provenance note: Landed f94d063 2026-10-25 ('what a refresh carries'). Note the living on 2026-10-26 (74e4d1) says no summary and no handover are passed; belief modules and raw vision logs are. 'Presentations and illustrations' ties to 48cff7 (2026-09-16: flowcharts, visuals, concepts). No record found that words 'the basic skills are everything a flow needs'.

**S52.1  Record `74e4d1/refresh` entry #1 2026-10-26 — No summary and no handover to the successor; beliefs and raw vision logs are passed; a refresh removes the first flow's biases**  
Date: 2026-10-26 (in heading). File: `flows/74e4d1/vision/refresh.md`  
Words and context: verbatim at S24.11 above (long record, not repeated).

**S52.2  Record `74e4d1/refresh` entry #2 2026-10-26 — Approved: the no-handover line; refresh the Primary; every flow understands Ethos, Datom, protos**  
Date: 2026-10-26 (in heading). File: `flows/74e4d1/vision/refresh.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, to Psyche core Primary 74e4d1, approving the proposed vision:remembering line.

> Good. Land it and then implement it by refreshing your own flow or having it refresh, whatever works best. Don't forget, right? I need every flow to understand ethos and datom or protos in general.
```

**S52.3  Record `a68420` entry #6 2026-10-23, living, direct, to Psyche core Primary a68420**  
Date: 2026-10-23 (in heading). File: `flows/a68420/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on what a successor flow is started with, after the Primary explained the old hand launcher's handover and raw-psyche template and Mind's loaded-startup build with a predecessor summary.
"I don't see much point in this handover concept since we're logging everything. Really, the only thing that matters is the psyche log, the vision logs, and so I think we're better off giving the successor its predecessor's vision logs. It's raw vision logs and the right context modules, the right vision modules, taken directly from the source, from main."
```

**S52.4  Record `d68c82` entry #22 The last response as a datom object; handovers generated from objects**  
Date: 2026-10-17 (in the record's context). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «Flow: vision and production», proposal 3 (refresh thresholds and handover), 2026-10-17 18:51, relayed by the core Tertiary.

> I think that if we just make the last response standard by making it a datom object (which starts with its variant and therefore has different structure, different redundant structure, and recursive structure), it can vary. Different objects have different presentations and all of this could fit in the UI instead of needing a thinking machine to render a web page for it. That would be a long-term vision.
>
> I'm just saying we don't need to talk about handovers because whatever. We can look for certain kinds of objects, like the last or all of a certain kind of object, and these can either become the handover or generate it. The handover could be generated from that, depending on what kind of objects were found or looked for, which aspect this represented, and whether or not this flow had, for example, any direct living input. We would need to determine that through, I don't know, some judgment for now.
>
> We can see, as an aside here, how much easier it gets once we control the user interface and therefore know where the living is typing. The reason why we need living core sessions is because I'm currently still remotely accessing through the harnesses themselves.

-- psyche, input mode not shown.
```

**S52.5  Record `48cff7/refreshPurpose` entry #1 2026-09-16 — a refresh makes the next flow smarter and better-equipped, generally and for the problem at hand**  
Date: 2026-09-16 (in heading). File: `flows/48cff7/vision/refreshPurpose.md`  
Context and the living's words, verbatim as logged:
```text
Context: after the skill proposals were pushed, the living named what a refresh is for — the *purpose* of the middle-layer package a psyche flow prepares for its successor.

> And here, let's put this somewhere in some form. We can analyze the target first, but it's something like the purpose of a refresh in the flow. One of them is to make the new flow even smarter or even better equipped to handle the problem, both generally and in specific terms that are at hand, so that it can just respond with a response. It's going to have:
>
> * flowcharts
> * visuals
> * concepts
> * relate to some things that already exist
>
> Here's the concept for a new nexus. They can do this: here's the anatomy. That's what a psyche flow would do, right? You would have these hooks that hook into that. They can both create a report from it or pass it as an actual prompt to a higher thinking power if it was asked, if it was appropriate.

-- psyche, typed.

Flow reading, not the living's words: the *product* of a psyche flow's turn — the thing it hands forward — is a middle-layer package that a successor loads. That package carries flowcharts, visuals, concepts, relations to existing skills and vision, and, when the flow was working on one, the concept for a new Nexus and its anatomy. Two hooks consume the package: **report** (delivered to the living) and **prompt-up** (delivered as the prompt of a higher thinking-power flow when the situation warrants).

The refresh is the mechanism; the package is the deliverable. Both are the psyche flow's work.
```

**S52.6  Record `752e0f/refreshAddendum` entry (whole file)**  
Date: 2026-09-24 (in the file). File: `flows/752e0f/vision/refreshAddendum.md`  
Context and the living's words, verbatim as logged:
```text
# End with an addendum to my own prompt; compensation skills

> When you're done with all that I want you to end with a presentation that you would give to create an addendum to change the prompt that you would give yourself (from what you had or what you would potentially get right now based on the script). Maybe you can even propose some changes before we restart you and then we can propulse that through to implement in a compensation layer. This becomes a compensation skill, right? The operation skill and the vision skill, they're all prefixed like that.

-- psyche, typed, 2026-09-24, directly to Psyche High 752e0f.
```

**S52.7  Record `1b8ac0/refresh` entry #1 Refresh yourself with the Flow CLI: it locks the session with the Messenger for a safe switch-off; the Flow checks the turn is done or interrupts; the model ends with a refresh payload, an addendum the next one starts with; merged parts are trimmed so the prompt does not accumulate**  
Date: 2026-09-21 (in the record's context). File: `flows/1b8ac0/vision/refresh.md`  
Context and the living's words, verbatim as logged:
```text
Context: spoken to PsycheHigh (Fable, flow 1b8ac0) on 2026-09-21, when the living doubted which Fable was current and saw this seat at twenty-nine percent context. Opens with a working instruction (reset yourself, audit the refresh log, talk to Mind) kept in log.md. Input mode STT ("mine" for Mind, "codec" for Codex). Logged by the main flow before acting.

> ... you should be able to refresh yourself with the Flow CLI, which would then lock your session with Messenger so that it's a safe switch-off, right from the Messenger's point of view.
>
> The Messenger would keep the messages until you have a new delivery point, and then the Flow would check that you're done. Your turn is done because it's not going to get any messages now, so it should be inactive. If not, it sends the current Flow a message, an interrupt message to say, "Please end session, please end Flow now," right? Switch over time, and then the model should just give a nice presentation, like a flashbook-style template presentation of everything that it has learned in this current Flow that it would modify what its initial prompt payload was. It's like a Flow refresh payload, and then that will be used to modify the previous version. It'll be like an addendum that the next one starts with, so it'll be added on at the end. That'll be like the previous, but we'll have to have a step eventually to merge them.
>
> It could be a choice, probably, to let the same model change the payload depending on what is authorized by a living authority or by a high enough authority to change its previous prompt, change the files it was made from, and then push the changes and start the next generation. With either all of the changes put into files or some of them put into files, the rest of the addendum is still passed over, but the parts that were merged into files are not, so we don't accumulate. We need to start trimming that initial prompt to make sure that it's only really told that the rest is still a bunch of loadable skills. It's told if it needs to know, "Here are the skills," but we don't need to load them all. We can concentrate on certain topics, depending on what we specialize the roles here and start to break things up.

-- psyche, STT. 1b8ac00b:1033, 2026-09-21T19:46:00.941Z.
```

**S52.8  Record `fe945a/flowRefresh` entry #1 What the new flows missed from their old ones is injected as user messages**  
Date: 2026-09-29 (in the record's context). File: `flows/fe945a/vision/flowRefresh.md`  
Context and the living's words, verbatim as logged:
```text
Context: Asking Field Astra d5b96b to reap and archive the old Codex sessions; the rest of the message is logged in flows/d5b96b/notion/session-reaping.md.

> We need to reap the old Codex sessions and archive them. You should get a sub-agent to find the most important part of what the new flows missed from their old ones and inject that as user messages.

-- psyche, typed. 2026-09-29 18:37 UTC, d5b96b, Field Astra (session 01a0ee2e, line 105). Reconstructed by fe945a from transcript.
```

**S52.9  Record `e51411/refresh` entry #2 The handoff lives in the transcript; a tool fetches it by reference**  
Date: 2026-09-24 (in the record's context). File: `flows/e51411/vision/refresh.md`  
Context and the living's words, verbatim as logged:
```text
> The handoff should be your last response, right? It might not be your last but it's in one of your last responses. It's like a final transcript handoff so you don't have to write it to a file. It's in your transcript file.

> Make that operational. The handoff is in the transcript and the tool gets it from that with the help of the AI. It locates the block and everything and logs that as the thing that the tool then uses to get the text from the transcript. The tool gets the right block of text because it has the right reference so we don't need to make a copy of anything. It just fetches it programmatically.

-- living, input mode not established, 2026-09-24 00:00:46 and 00:01:41, to Mind Astra 47764b; not logged by that seat; recovered verbatim from its transcript by d8df70's logging audit (flows/d8df70/reports/psyche-logging-audit.md).
```

---

## Final section: the living's horizon-bearing words, and noted corrections

### A. Horizon words, verbatim

Left unplaced. The first four groups are the living's words of 2026-10-29 (554e1a, b2b87a, 73b5d8) on how vision is divided by horizon and on long term and short term; they are followed by the earlier records of 2026-10-13 that began the short-term / long-term vocabulary and by the horizon marks he put on Flow lines.

#### A1. 554e1a, 2026-10-29: the bind of long term and short term, and the division by horizon

**A1.1  Record `554e1a/psyche` entry #1 2026-10-29 — Long-term ideas, underspecified, are built monolithic; the bind of long term and short term**  
Date: 2026-10-29 (in heading). File: `flows/554e1a/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 21:10, comment on Flow, whole, on the line "The Flow Nexus sets up and starts a model flow".

I think it's appropriate here to also mention that I'm in a bit of a bind here because there's the long-term vision, right? We've talked about this: how we want them separated, but it is complicated. The more complexity we introduce, obviously, the more we have to manage. At the same time, I've been bitten really hard by not specifying something as long-term, meaning not necessary on the next iteration. Because long-term ideas are usually underspecified and lack the surrounding context to explain how my modular vision composes, usually the implementer approaches things in a monolithic way. The implementation ends up cramming a bunch of ideas together that create a broken system because there's just not enough abstraction already and not enough instructions on how to compose these abstractions. Also, the implementer sometimes or often has a hard time understanding that a feature needs to be configurable. This, I believe, even though I keep talking about it, is going to keep biting us because the model that we currently have, or the way that the thinking machine is set up, tries to just get the shortest route to what it thinks it needs to make. It essentially does in one step what should be done in multiple steps, right? It would be like asking the guy who drives the nail into the frame of the house to: - design the house - do the orders - do the accounting - do the taxes - contact the client - order the material - make the decisions - replace the foreman - replace the janitor - drive the nails into the What happens when this happens is they build a mud hut, right? What I'm making is not a mud hut, and so if we're not clear about the fact that we don't want to try to build the Empire State Building out of mud and straw, we're probably just going to end up with a pile of mud.
```

**A1.2  Record `554e1a/psyche` entry #2 2026-10-29 — Vision divided by horizon into modules: unmarked, short, medium, long, and a far one**  
Date: 2026-10-29 (in heading). File: `flows/554e1a/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, in the Psyche core Primary chat 554e1a, on the proposal Two horizons (https://claude.ai/artifact/9WCADhbhbER9oXAaepEchL).

I think that putting the long vision with the short vision in one file will create a bunch of ghost effects, because if anyone wants to know anything about this topic, they have to load all of it. They can't choose to just know how the system is expected to work in the short term, which is useful most of the time for most flows, but especially flows that don't design like field-aspect flows.

I would divide them. I would even say we can make three: the short, the medium, and the long-type vision. Maybe we do `vision:short:Flow Nexus`, for example.

What I was thinking just now is that the short is special also in that it's a compromise, a short-term compromise. It would be essentially anything that's marked as a compromise, a short-term solution, or a hack. The medium-type vision would maybe hold anything that's horizon-agnostic, but it would describe the system as we would like it to look past the short and compromised phase. The long vision would describe what we would like it to be ideally.

We could even introduce, I don't know what we would call it, the naive way would be to say "very long," or maybe there's a term. Maybe in some cases we have this extra-far idea, which rarely ever gets loaded except for flows that need to understand the living's overall broad vision. This would allow for much more efficient development that can focus.

Let's say we have problems. Let's say we're in a situation where things are breaking and we need to get the system going again. This is the implementer that would be started to fix things. It could be loaded only with the short vision.

I think that the unmarked type, the vision that does not have short, medium, or long, is actually where we would put the horizon-independent or horizon-insensitive part of the vision. What do you think of all this?
```

**A1.3  Record `554e1a` entry #1 2026-10-29 — The Nexus is called Flow Nexus; a flow is one run of a metaflow or a single FML flow**  
Date: 2026-10-29 (in heading). File: `flows/554e1a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 21:05 and 21:11, comments on Flow, whole (https://claude.ai/artifact/M4E2xhh4GycRo11GkPNJ1D) by the Psyche flow Primary 30fc30, relayed through Psyche core Tertiary b195f0 and Secondary 9b514f.

Okay, first, let's call this Flow Nexus instead of Flow, because I really want us to say Flow Nexus when we're talking about the Nexus, so that we don't get confused with a "flow."

On "A flow is one run of a metaflow": This is incorrect because a flow could be one run of a metaflow, or it could be a single FML flow. At least in the long term, we have that concept also, but I think we really need to define this long-term/short-term thing. I'm going to get these comments sent to core, and I don't want this proposal to be redone yet. I just want to specify first how we are going to take care of long term/short term, and then, once that's done, we should revisit this.
```

**A1.4  Record `554e1a/belief-modules` entry #1 2026-10-29 — The Flow flow carries no book module; a main flow dedicated to publishing books**  
Date: 2026-10-29 (in heading). File: `flows/554e1a/vision/belief-modules.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, in the Psyche core Primary chat 554e1a, after glancing at the Psyche flow Primary 30fc30's startup and seeing the book module in it.

I see that the psyche primary flow topic was started. I just happened to glance at things, and I saw the book module. Obviously, we still have a very broken and messy system. This is absolutely harming the design, right, because the flow designing the Flow Nexus has zero need to know how to make a book. In fact, he would never even make one.

I would even say it would be great if we could have a main flow that is dedicated to publishing books, so that we can take the tool out, as well as the system prompt that teaches how to use the tool, from all the other Claude main flows, so that they take a bunch of noise out of their context.

I've been talking about this for several days, but I understand that you're having trouble even discerning up from down right now, so it might be a little bit overwhelming for you to try to make well-functioning software out of the Flow Nexus. Maybe you can try, and obviously this would be passed over right now to the flow making the design, but you would probably be involved in the belief side of things on this.
```

#### A2. b2b87a, 2026-10-29: comments on Vision by horizon, and the order after its landing

**A2.1  Record `b2b87a/psyche` entry #1 2026-10-29 — A short line naming the medium line it stands in for is impractical**  
Date: 2026-10-29 (in heading). File: `flows/b2b87a/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 22:21, comment on Vision by horizon (https://claude.ai/artifact/9WCADhbhbER9oXAaepEchL), thread d0430b8d, on the passage "each naming the medium line it stands in for", relayed by the comment relay through Psyche core Secondary ca3262.

That's totally impractical.
```

**A2.2  Record `b2b87a/psyche` entry #2 2026-10-29 — The far module is loaded by a flow designing the very far, currently impractical broad vision**  
Date: 2026-10-29 (in heading). File: `flows/b2b87a/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 22:37, comment on Vision by horizon (https://claude.ai/artifact/9WCADhbhbER9oXAaepEchL), thread 046345a2, on "loaded only by a flow that must understand the whole", relayed by the comment relay through Psyche core Secondary ca3262.

Loaded by a flow that is designing the very far, far away, currently impractical broad vision
```

**A2.3  Record `b2b87a/psyche` entry #3 2026-10-29 — A marked horizon is unimplemented by definition; when the medium lands the short goes and the horizons move up**  
Date: 2026-10-29 (in heading). File: `flows/b2b87a/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 22:39, comment on Vision by horizon (9WCADh), thread af203c17, on "Any horizon may be implemented or not"; relayed by the comment relay through ca3262, typed by hand, not byte-checked.

No, that's not true. If it's marked medium, then we already know that it's unimplemented. If there's a short and a medium, that means the medium is trying to overcome the short. Otherwise, if the short exists and the medium is implemented, then the short is gone, or it should be removed. It's telling you: if the medium vision is implemented, then the short must necessarily, logically speaking, be irrelevant, so it should be removed. Do you understand what I'm getting at here?

The same goes for medium and long. By definition, the far vision is never implemented. Otherwise, it would already have moved into long, because if we're that close to it, it's not far anymore, and it might even be medium. Once we eliminate the short, you can see how medium becomes the short, long becomes medium, and far becomes long, because now we're closer. We've moved beyond the short term, and now the medium is the short term.
```

**A2.4  Record `b2b87a/psyche` entry #4 2026-10-29 — Vision by horizon is landable by Fable on his comments, without his review**  
Date: 2026-10-29 (in heading). File: `flows/b2b87a/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 22:40, same page, thread 347b014c, on the paragraph "The long-term vision is the goalpost…"; relayed the same way.

Well, it looks like you got the gist of it there, but you can describe it more accurately to be in line with what I said. So far, I believe that you can land this and adjust it for my comments without needing to review it, right? So far, unless I say otherwise later, this is still landable without my intervention because I trust that Fable is able to understand what I mean and represent it accurately, without getting me in the loop again.
```

**A2.5  Record `b2b87a/psyche` entry #5 2026-10-29 — The line on building the short line beside the farther one is removed from the landing**  
Date: 2026-10-29 (in heading). File: `flows/b2b87a/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 22:42, same page, thread 69a827e8, section A long line is built in its time, on "Until then the implementer builds the short line beside it, shaped so the farther line can take its place."

I see a lot of potential ghost effects in this line, and I have a hard time understanding it. I would say just remove it from the landing. We can still land this, but without this line.
```

**A2.6  Record `b2b87a/psyche` entry #6 2026-10-29 — Several horizons may be in implementation at once; the focus, now, is the short term**  
Date: 2026-10-29 (in heading). File: `flows/b2b87a/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 22:43, same page, thread faa5a6c3, on "To an implementer a medium, long or far line says: not this iteration…"

We could still have proof-of-concept implementations trying to implement the medium term, while someone is trying to keep the short-term implementation, either improving it or fixing it. It's possible that we would have multiple timeframes being implemented, but yes, generally, especially right now, we would focus on the short term. I believe you can make those changes and still land it without my help.
```

**A2.7  Record `b2b87a/psyche` entry #7 2026-10-29 — After the horizon belief lands: the Flow proposal redone by horizon, Astra's opinion, a short-term flow; which horizons a flow loads; the vision outranks the code**  
Date: 2026-10-29 (in heading). File: `flows/b2b87a/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, in the Psyche core Primary chat b2b87a, after the Vision by horizon landing was ordered. One message, whole; it bears on Flow, on horizons (intent:psyche), on model roles and on what matters.

Once the vision horizon belief is landed and deployed, we can assume it's going to be deployed. Once you've integrated it well enough, you can inform The Flow Nexus primary of this in his middle stratum properly. You can then have him redesign the whole flow proposal. Maybe you can even help him, or tell him that he needs to try to discern. He can do some deep investigation and research into the past: how it was said, how things were said, when they were said, and so on, to try and separate.

He can also have someone look at the implementation to try and separate what we want the Flow Nexus modules to be: the common, non-time-sensitive part of the design, the no horizon, or whatever the word is I'm looking for. Maybe you can help me. Whatever it is, the part that doesn't have a horizon qualifier. Each vision can essentially have a short, a medium, a long, a far, and an unmarked vision.

To separate that from the short, from the medium, and the long, I don't think we have a far vision yet. I haven't gone that far, no pun intended, because you're already confused enough. The cool thing with this concept is that now I can talk to you about my really far-off ideas without fearing that it's going to confuse the system too much.

Generally speaking, unless I explicitly say so, we can review the proposal for this. It's kind of fairly simple what I'm going to say: unless I specify so, whenever I want something redesigned and improved, I'm talking about loading the short and the medium horizon, generally, right? Unless we're in emergency repair mode, in which case we only want the short, as well as the non-time-sensitive, obviously, part of the vision. That is probably what most flows that don't want to know a little bit about something but don't need that, just want to know: the broad aspect.

Just why? Maybe we want to also get another round of describing how to classify horizons. I'm telling you now, right, so you can act on what I'm saying, and then we'll review the exact wording we want to use in the belief itself. The general aspects that are not difficult to get to and that will help to drive behavior, that will help the system to follow my vision in behavior (if not code), are going to be in the non-horizon-marked part or the non-horizon-marked part module.

Once you have that grasp of what I mean, and it's well put together and it's going to land, you can inform the current flow design and the Flow Nexus design pair of this, so that they can redo the whole flow proposal with all of the separations. Also, reviewing everything that's been done so far and separating all of it where it should belong: either unmarked, short, medium, or long.

And then, as soon as that's done, I guess you can inform Mind and just see what he says about the unreviewed modules and the proposal. See what he has to say about it in terms of what's implemented now, so that you can tell me how he sees it, especially Astra. I would like Astra's opinion on this.

Maybe a new dedicated flow that can take a deep look at the code and this proposed vision, focusing on the short term: everything that we need to have working right now to have a fairly sane system. If there's anything obviously lacking, he can start working on a branch to fix that. If I agree with the short term, then that could become a candidate for the next improved version, which should build on what's already been built, unless what's been built is actually problematic, right? In which case, I'm all for code being thrown out and rewritten.

Like I said, or maybe you didn't know this, the vision is really what matters, and the implementation can be redone from scratch just from the vision if the vision is good. The code is really secondary in importance to a good vision.
```

**A2.8  Record `b2b87a/belief-modules` entry (whole file)**  
Date: 2026-10-29 (in the file). File: `flows/b2b87a/vision/belief-modules.md`  
Context and the living's words, verbatim as logged:
```text
# Belief modules

## 2026-10-29 — Approvals landed, records archived, declarations and configurations updated for the changed modules; the vision of modules by aspect and layer
Context: the living, in the Psyche core Primary chat b2b87a, after the Crystallization and Vision by horizon landings.

Sure. Also:

* Everything that's been approved lately is well landed.
* The records that I drew from are archived properly.
* The flows need to have their definitions changed because there are new model modules, or modules that have been split up, or that are changed, or that are not relevant to their flows anymore.
* Their configurations are changed appropriately.

 We should review that if we haven't. If you haven't made a book, or if you have, let's update it.

The vision is on how, roughly speaking (and we don't have to go into full detail), the modules that we want to allocate to certain aspects, layer by layer, and to certain aspects and layers that are specifically more special. Like yourself, you're probably the most special because I talk to you the most. Not you, I mean the psyche primary core, right? It is the flow that I mostly interact with the system through.

Let's make sure that everything is in order so that our flows are not starting with mental disorders.

## 2026-10-29 — The Psyche core Tertiary is the comment retriever and has the tools for it
Context: the living, directly to Psyche core Secondary b2b118, after commenting on https://claude.ai/artifact/VnXvW1HTtskwTQ3vFcYePK; Tertiary b195f0 had been launched without the Artifact tools. Relayed by b2b118 to the Primary.

If Tertiary is not able to help me to act as a retriever for comments so you don't have to spend your energy, then I don't have much use for him. If that's the case, then I want him restarted with those tools available.
```

**A2.9  Record `b2b87a/design` entry (whole file)**  
Date: 2026-10-29 (in the file). File: `flows/b2b87a/vision/design.md`  
Context and the living's words, verbatim as logged:
```text
# Design

## 2026-10-29 — A step is one thing: good
Context: the living, 22:44, comment on Vision by horizon (9WCADh), thread 92b81a8e, section A step is one thing (intent/design.md), on "A step is one thing: the design, or an abstraction the design needs, or the behavior on that abstraction, each judged on its own before the next is begun…"; relayed by the comment relay through ca3262.

good
```

#### A3. 73b5d8, 2026-10-29: his words on the Flow Nexus work, vision code and the ghost effect

**A3.1  Record `73b5d8` entry #1 2026-10-29 — The Flow Nexus gives a flow its Flow ID; the evolution is reported**  
Date: 2026-10-29 (in heading). File: `flows/73b5d8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, in the Psyche core Primary chat 73b5d8, after the fresh Primary bound its own seat by command and reported the repairs in motion.

And I'm still not hearing about the new Flow Nexus, which should fix the message format. I don't see any reason why the Flow Nexus cannot give you your Flow ID and why you have to spend your own energy to do something so trivial.

Context: the second half of the same order, his words of 14:24, recovered by the remembering check of primary-zr42.

Then I will review your open proposals.
```

**A3.2  Record `73b5d8` entry #2 2026-10-29 — The Flow flow first grasps his vision, then revises the whole vision of Flow and its ethos, with vision code**  
Date: 2026-10-29 (in heading). File: `flows/73b5d8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, same chat, after ordering the Flow work merged, audited by a Fable flow, fixed and deployed.

And I'd like to put together a very well-trained... I guess this would be the Flow Nexus. I think the first thing the Flow Nexus should do is really make sure that he has a very good idea of what I have, what I envision for the Flow Nexus to do (being really mindful of not hardcoding behavior in the code), and then create a full revised vision for Flow and the Flow ethos that I'll review in entirety. Maybe looking for inconsistencies or repetition, and fleshing out the parts of the system that are either non-optimally designed or underdesigned, and bring some more vision code flesh out, right? Do you understand what I mean by vision code?
```

**A3.3  Record `73b5d8` entry #3 2026-10-29 — Vision code is mostly Ethos and Datom; Nix where the vision depends on it; the belief on vision code reviewed**  
Date: 2026-10-29 (in heading). File: `flows/73b5d8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, same chat, after the Primary said vision code is the Ethos and datom in a vision statement.

Well, it is usually mostly ethos and Datom, although if some of the rest is interesting to us, or if we're depending right on the vision, sometimes it might involve explaining how we like to use Nix (which would obviously involve Nix code). Maybe we want to review that as well: the belief that touches on all this.
```

**A3.4  Record `73b5d8` entry #4 2026-10-29 — The vision-code line names the stacks, not one example**  
Date: 2026-10-29 (in heading). File: `flows/73b5d8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, same chat, on the proposed line "Vision code is mostly Ethos and Datom; where a design depends on how a tool is used, Nix among them, the statement carries that code as well."

Your proposal is half good. One of the problems is that we now have a ghost effect because your example would skew the balance. We're welcome to give examples, but let's not forget the most important stacks that we use, right?
```

**A3.5  Record `73b5d8/remembering` entry (whole file)**  
Date: 2026-10-29 (in the file). File: `flows/73b5d8/vision/remembering.md`  
Context and the living's words, verbatim as logged:
```text
# Remembering

## 2026-10-29 — Everything to propose goes in one proposal; the remembering goes in the middle stratum
Context: the living, in the Psyche core Primary chat 73b5d8, after the Primary's chat proposals and its admission that the evolution moved only because he asked.

Make sure everything you want to propose to me is in the proposal now. Maybe review everything. Make sure that you haven't forgotten something important that I said in your previous flow or in its predecessor. The flow launching is still quite broken and you seem to forget a lot of important things. Make sure that whatever you remember goes in your middle stratum. Maybe we should make this standard behavior since I seem to make you do this every time. But I would prefer, of course, in the long term, if we could avoid such a waste of tokens (since all of that could be done by a properly configured system that passes over the right modules every time the Flow is refreshed).
```

**A3.6  Record `73b5d8/evolution` entry #2 2026-10-29 — The Flow work is sprawled**  
Date: 2026-10-29 (in heading). File: `flows/73b5d8/vision/evolution.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, same chat, after the Primary reported 0.40.6 on Mind flow Primary's integration branch, undeployed.

And who knows, there might be even yet another version. It sounded like the work was getting sprawled, which is also a problem.
```

#### A4. d68c82, 2026-10-13: where short-term vision and long-term vision were first named

**A4.1  Record `d68c82/psyche` entry #2 The envisioned and the makeshift**  
Date: 2026-10-13 (in the record's signature or body). File: `flows/d68c82/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
> So there's the vision, which maybe we need to divide things or specify when a vision is not thought of as something that we would implement soon or that has priority. You're wet [sic].
>
> There's the part of the vision that I see as what I would like, eventually, without breaking or blocking everything else, whether or not it's done this way right now. It's a goalpost, not a blocker.
>
> Let's talk to people about maybe Fable's spirit, about this concept of differentiating between the goalpost, the eventual result, the eventual state of things, and what the system looks like for now. There's this term I want to bring in and make commonplace: makeshift. We have the makeshift situation and then the ideal or the envisioned situation. Maybe that's where we draw the line between the mind and the psyche.
>
> What the current situation is, or the makeshift, is the non-ideal system. There's still this targeted aspect: both the envisioned and the makeshift proposal might not be implemented at all. They're both visions in the sense that the vision has not become knowledge. It hasn't become fact, whether it's makeshift or not.
>
> There's a problem where the machine essentially considers all of this the same thing and so it becomes confused because it sees a contradiction between the envisioned (which it doesn't understand as the envisioned system) and the short-term solution. It thinks it has to reconcile them or block, but it essentially has to differentiate between what we can do right now and what we would like it to be eventually.

Context: comment on «Aspects talk at the same layer», third edition, Question 1 (hard rule vs posture for speech between layers).
-- psyche, STT, 2026-10-13T17:04.
```

**A4.2  Record `d68c82/psyche` entry #4 Short-term vision and long-term vision**  
Date: 2026-10-13 (in the record's context). File: `flows/d68c82/vision/psyche.md`  
Context and the living's words, verbatim as logged:
```text
> No that's not it. The makeshift might not be implemented either. If so, if we say the Envisioned Vision, that sounds ridiculous so we would have to come up with another term. You would have the Envisioned Vision, or what we replace it with, and then the makeshift vision or maybe we'd just make it simple and have the short-term vision, the long-term vision, and that's it.
>
> We would differentiate between those, which again doesn't mean that the short-term vision is implemented at all either. It could still just be an unimplemented vision or it might be implemented. The long-term vision might also be implemented. We don't really need to get too deep into this. If the long-term vision is implemented and documented, then the short-term vision really should be removed because it has no more purpose. It just acts as noise, as well as its documentation.

Context: comment on «Makeshift and goalpost», Proposal 1 (spirit-core line "The envisioned is the goalpost and never a blocker; the makeshift is what is done for now...").
-- psyche, STT, 2026-10-13T17:12.
```

#### A5. Horizon marks the living put on Flow lines (long term / short term / medium term), by date

**A5.1  Record `d68c82` entry #9 2026-10-14 — A full Flow Nexus proposal, short-term and long-term**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: spoken to the Psyche Core Tertiary after commenting on «Flow: CLI, deployment, long term», 2nd edition; relayed.

> I need to see a full Flow Nexus proposal, also probably separately.
>
> Let's have the short-term version and then the long-term/universal version: the parts that are independent of whether or not it's short-term or long-term, like the overall intention of the design, which is going to live in the long-term/Nexus proposal. We focus on specifying the ethos and from the ethos we already talked about the fact that we're going to derive the short-term prototype code.

-- psyche, STT.
```

**A5.2  Record `da2038` entry #3 A needed flow is started, running or not**  
Date: 2026-10-14 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same book, proposal «an undelivered request tries a higher power, then lower; a crucial metaflow missing is started», 2026-10-14T15:18; relayed by Psyche Core Secondary.

> We have old vision that is now obsolete in there, with a conflicting vision. The long-term vision is that the flow is started if it's needed, which means it doesn't matter if it's running or not. Even if it doesn't have any working transcript to reawaken, then we just feed it the context modules that this meta flow is supposed to have, along with the prompt that it's supposed to be getting now.

-- psyche, STT, 2026-10-14.
```

**A5.3  Record `da2038` entry #6 Vertical communication is not strictly short-term**  
Date: 2026-10-14 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on choice 2, vision-model-roles L51 «Short-term: vertical communication stays within one aspect and normally advances one layer at a time.»; same book.

> This concept is not strictly short-term. What makes you think this is a short-term concept?

-- psyche, STT, 2026-10-14.
```

**A5.4  Record `da2038` entry #23 All traits in Ethos is the long-term goal; in the short term, without it**  
Date: 2026-10-16 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on da2038's finding that ethos-zero generates no traits while Flow holds 209 hand-written traits; relayed to da2038 by Psyche Core Secondary as #psyche, 2026-10-16.

> Yeah well, of course we can't meet all of our long-term ethos goals in the short term. That's why we have short term and long term. Long term we want all the [traits] in ethos and short term we just do without.

-- psyche, STT, relayed by Psyche Core Secondary.
```

**A5.5  Record `d68c82/archive-flow` entry #12 The short term and the long term are not mixed**  
Date: 2026-10-19 (none in the record; date of the file's first commit). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> You're talking about meta sockets, which have to do with nexus, and then you're talking about the short-term solution, which is [Clojure]. Total fucking confusion here.

-- psyche, STT. Transcription corrected: "closure" → "Clojure".
```

**A5.6  Record `d68c82/archive-flow` entry #2 Subflows replacing the subagent tool is long term, stated broadly**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «How a flow is defined», the vision/flow.md heading "Subflows replace the harness subagent facility".

> Let's clean up this subflow vision a bit. It's a bit confusing and mark it as long term. This should just be in its own book. This is long term. We want to replace the subagent tool with actual flows but it's long term and it should be just a broad explanation of the concept instead of being so specific. These paragraphs are getting maybe too much into specifics and these are confusing short-term hacks with long-term vision. Like how we have the field coordinator involved, this sounds more short-term than long-term and maybe it's not even relevant anymore. I don't know. If we're not doing it right now, we can remove it and just represent the concept more clearly or more sanely.

-- psyche, book comment, 2026-10-19T17:45, input mode not shown.
```

**A5.7  Record `d68c82` entry #18 Comments on «Flow: context modules and the prompt, 2nd edition», 2026-10-16**  
Date: 2026-10-16 (in heading). File: `flows/d68c82/vision/flow.md`  
Words and context: verbatim at S31.3 above (long record, not repeated).

**A5.8  Record `ecbc42` entry #3 Topic names: an open enum in the long term**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ecbc42/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: book comment on «The Nexus: questions for the living» (https://claude.ai/artifact/32uPikafAbLVMWfxaBinAW), relayed by Psyche core Tertiary, Proposal 13 (topic name kept exactly as written), 18:26; his first comment there was "Good. Mark short term".

"In the long term we want to support the open enum that I've talked about so that `core` would be a capitalized variant and there could possibly be more. But a custom topic could also be specified instead of one of the explicit variants. But we first need to support that in Ethos in order to do it."

-- psyche, STT, book comment.
```

**A5.9  Record `5330c1` entry #3 2026-10-23 — long term hooks feed Flow; Flow a small monolith first; medium term hooks on all harnesses; Flow does the usage accounting; tonight's reiteration works in testing variants, stable keeps running**  
Date: 2026-10-23 (in heading). File: `flows/5330c1/vision/flow.md`  
Words and context: verbatim at S38.8 above (long record, not repeated).

**A5.10  Record `bf8ae0` entry #1 2026-10-27 — In the long term: an idle-flow procedure; the Flow Nexus tells a flow when it has been idle, when its cache will expire, or when its context passes a size; the flow winds down, puts its chat proposals into a proposal book, and refreshes**  
Date: 2026-10-27 (in heading). File: `flows/bf8ae0/vision/flow.md`  
Words and context: verbatim at S39.11 above (long record, not repeated).

**A5.11  Record `bf8ae0` entry #8 2026-10-27 — Use up Codex; in the long term, the resets are used for the machine**  
Date: 2026-10-27 (in heading). File: `flows/bf8ae0/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, going to bed.

> Don't feel shy to use up Codex. Like I said, we have a reset, so that would also be a good long-term feature: to be able to use those resets for you.
```

**A5.12  Record `733232` entry #1 Absent recipient startup — long-term**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/733232/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: Relayed by Psyche core Secondary as the living's long-term vision; implementation feasibility is subject to Primary review.

> When recipient flow is absent, Flow starts the recipient with its usual start prompt AND message below it, together in initial launch context. Sending CLI blocks until startup+delivery and returns Sent, or Failed with reason.

-- psyche, relayed by Psyche core Secondary.
```

**A5.13  Record `c637a5` entry #4 2026-10-27 — Implementers are not handed raw psyche logs; a restriction they build is data-driven and off when unconfigured**  
Date: 2026-10-27 (in heading). File: `flows/c637a5/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, after I launched the fresh Mind flow 2c06c7 with the rebuild order.

> And be careful with passing over raw psyche logs, because, as we've seen, the implementers are really good at taking my invariants out of context and mistaking them for short-term goals that they need to put in the code and put inflexible behavior in the code. If you give them invariants and they put in these restrictions (and I'm not sure that that's a good idea anyway, but let's say they do), then it certainly has to be done using a configurable feature, meaning it has to use data to drive that behavior, and so that we can essentially drive the system with it turned off if it's unconfigured.
```

**A5.14  Record `36ac89` entry #4 No restrictions hardwired into Flow; seats have their tools and subagents**  
Date: 2026-10-26 (in the record's context). File: `flows/36ac89/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
2026-10-26, to Psyche core Secondary 36ac89. Context: seats launched by Flow 0.40 were reported unable to use subagents; a new Primary had been started.

> Okay we're having huge problems with the new flow. We started a new primary. Don't talk to it because it's useless but I've been talking to the Flow secondary topic, or to the secondary with the Flow topic, and he doesn't seem to even understand that.
>
> What I suspect is that I think the Flow didn't have any tools. We have all of this hardwired security, or so-called invariants that I talked about as a long-term vision goal for the entire system as a whole to have. But now agents are trying to hardwire that into individual components.
>
> It said that. The other secondary said that the flows, the new flow starts, can't use subagents. I don't want any of these fucking restrictions. It's not what I want. It's not what I want. It's not what I want. Oh my god this is so bad. You guys have done a horrible job.
```

**A5.15  Record `36ac89` entry #8 Overnight: no hardwired behaviour that should be configurable**  
Date: 2026-10-26 (in the record's context). File: `flows/36ac89/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
2026-10-26, said to Psyche core Tertiary b195f0, relayed to Psyche core Secondary 36ac89 by cross-session message (the Tertiary's own log holds the record).

> I made some comments on a recent book about Flow. Collect them, pass them on to Secondary, and get him and Fable to coordinate to reimplement some things overnight thoroughly. Make sure that there is no more hardwired behavior that we want to make configurable and that should be configurable in the software. Fable can make the design if there's any. If there's anything to design without my approval just to get something built overnight, don't block on anything. Get your Secondary and Primary aspect to do the coordinating and designing and get your Mind to do the implementation with Secondary and Primary as well.
```

### B. Noted corrections

Each correction is shown with the record that holds it. Where a correction replaced an earlier word, both are in the records and neither is erased.

#### B1. 9aaaba, 2026-10-28: the queue scrapped, then restored

He first said to scrap the queue for now; minutes later he said it should not be scrapped and that the queue flushes as one message, the trigger included. The module's S14 queue clauses and the restored queue stand on the second. (9aaaba also says: 'No EDN anywhere; it is all datom', correcting talk of EDN.)

**B1.1  Record `9aaaba` entry #1 2026-10-28 — Scrap the queue for now**  
Date: 2026-10-28 (in heading). File: `flows/9aaaba/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, after the held one-per-turn queue kept him from his flows for hours and its cause was found in the 0.40.0 drain.

> Okay here's the thing: the queue has been such a huge source of problems. Why don't we just fucking scrap it for now?

> I don't even understand why you guys are using the queue so much.
```

**B1.2  Record `9aaaba` entry #2 2026-10-28 — Not scrapped: the queue flushes as one message, the trigger included**  
Date: 2026-10-28 (in heading). File: `flows/9aaaba/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, direct, minutes after saying to scrap the queue, watching the Secondary take one call per held message.

> This is not hard to fucking implement so I don't know why we need to scrap it.

> If you have a queue and something, there should be more than one reason why the queue goes out. If, let's say for whatever reason, something comes in that should flush the queue, then all of the messages come into the pane as "one message". All of them, everything, including the one that comes in that gets the queue unstuck, come in as "one message". We don't send a message and then another message and then another message and then another.

> He's acting on incomplete information because every time he gets one more message, that means that what he acted on previously was missing that information. We get horrible results: high cost, slow behavior.
```

**B1.3  Record `9aaaba` entry #4 2026-10-28 — No EDN anywhere; it is all datom**  
Date: 2026-10-28 (in heading). File: `flows/9aaaba/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
> There shouldn't be EDN involved anywhere. Why are you talking about EDN? It's all datom.
```

#### B2. 554e1a, 2026-10-29: 'a flow is one run of a metaflow' corrected

He objects that a flow may also be a single FML flow (at least long term) and asks that long term / short term be specified first; he does not want the proposal redone yet. The module still says 'A flow is one run of a metaflow' (S2). b7a16a had already said 'A flow is not only one run of a metaflow because there are other types of flows' (2026-10-21 or after, vocabulary module). d4ae97 (2026-10-07): 'A flow could exist and not be a metaflow'.

**B2.1  Record `554e1a` entry #1 2026-10-29 — The Nexus is called Flow Nexus; a flow is one run of a metaflow or a single FML flow**  
Date: 2026-10-29 (in heading). File: `flows/554e1a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, 21:05 and 21:11, comments on Flow, whole (https://claude.ai/artifact/M4E2xhh4GycRo11GkPNJ1D) by the Psyche flow Primary 30fc30, relayed through Psyche core Tertiary b195f0 and Secondary 9b514f.

Okay, first, let's call this Flow Nexus instead of Flow, because I really want us to say Flow Nexus when we're talking about the Nexus, so that we don't get confused with a "flow."

On "A flow is one run of a metaflow": This is incorrect because a flow could be one run of a metaflow, or it could be a single FML flow. At least in the long term, we have that concept also, but I think we really need to define this long-term/short-term thing. I'm going to get these comments sent to core, and I don't want this proposal to be redone yet. I just want to specify first how we are going to take care of long term/short term, and then, once that's done, we should revisit this.
```

**B2.2  Record `b7a16a` entry #5 Flows outside metaflows**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/b7a16a/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: on the proposed definition of Flow in the vocabulary module.

"A flow is not only one run of a metaflow because there are other types of flows that are not parts of metaflows, which we've talked about before."

-- psyche, STT.
```

**B2.3  Record `d4ae97` entry #6 A flow is not always a metaflow**  
Date: 2026-10-07 (in the record's context). File: `flows/d4ae97/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on "Flow" in the metaflow record, section 1.

> A flow could exist and not be a metaflow so this structure is wrong. I guess you could make it an optional metaflow. What are we trying to show here? The only thing we need is for us to know that a flow is a metaflow. If a flow is a metaflow we'll be addressing it by its long-term metaflow name. There are flows that are not metaflows so I don't think this structure is appropriate. Anyway I haven't read the whole thing. I still have to get to the memory specification but I wanted to point that out.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.
```

#### B3. d36431, 2026-10-25: restart without waking

He corrected the Secondary's rendering of his words: not 'a restart must not wake the flow' but 'I want the option'. Commit af97799 removed the line that misstated him; 9e03cd0 restored the correct form. The first entry shows the cost he was avoiding.

**B3.1  Record `d36431` entry #1 2026-10-25 — Restarting a flow without waking it**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: said after the Secondary sent the Psyche core Primary (493e29) messages that woke it, and the Primary had replied, when the restart of the Primary seat was ordered.

> You guys are tripping on your own shoelaces and going against my vision. The whole point of me telling you to restart primary seat is so we wouldn't pay for an uncached run of its old context, which you now did. Now it's been woken so it's too late. Now it's cached so it's not as bad if we keep talking to it. Whoever implemented the way flows restarted made a mistake because I explicitly many times said that we need to be able to restart flows without waking them. Somebody made a huge mistake.
```

**B3.2  Record `d36431` entry #2 2026-10-25 — The option to restart a flow without waking it**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: correcting the Secondary, which had rendered his previous words as "a restart must not wake the flow".

> Now you're twisting my words. I didn't say that a restart must not wake the flow. My point is I want to be able to restart a flow without waking it. Of course a flow can restart itself. That's not a problem but I also want the possibility. I want the option.
```

**B3.3  Record `d36431` entry #3 2026-10-25 — The woken seat stays; the option is for next time**  
Date: 2026-10-25 (in heading). File: `flows/d36431/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: after Psyche flow Secondary planned a no-wake stop of the already-woken Primary seat and the core Secondary relayed it to him.

> Well like I said, you already woke it up so it's okay now. It's woken. I don't know why you're trying to do this. You cannot start it without waking it now because you already woke it up so you can't roll back time. I don't even know why you're trying to do something which is impossible or talk about it even. Obviously we're going to fix it so that next time it'll be possible.
```

#### B4. 9457ab / 9519a1 / 875960, 2026-10-11: the voice concept

He corrected the proposal that took out 'voice' with 'we've gotten rid of the voice concept ... Just replace it by saying that the default topic is core'. (The module has no voice vocabulary; d68c82/archive-flow 2026-10-19T17:27 adds 'one run of a metaflow not a voice'.)

**B4.1  Record `9457ab` entry #1 Heartbeat checking, with a fallback check later**  
Date: 2026-10-23 (in the record's context). File: `flows/9457ab/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living asks the Psyche core Secondary, 2026-10-23, whether the heartbeat checking mechanism is in place and working.

"Has the heartbeat checking mechanism been put into place and is it working? If not then you, primary, mi[nd], and field can coordinate on giving another shot. Perhaps you can have some sort of fallback to make sure that you check later to make sure that it has worked."
-- psyche, STT. Transcription corrected: "mine" → "mind".
```

**B4.2  Record `d68c82/archive-flow` entry #1 A flow is one run of a metaflow**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on «Flow's vision», the current vision/flow.md line "A flow is one run of a voice".

> The run: one run of a metaflow not a voice. Let's get rid of that voice vocabulary. Consistency

-- psyche, book comment, 2026-10-19T17:27, input mode not shown.
```

#### B5. ce46fb: the heartbeat is a reminder, not counts and ceilings

He corrected the flow's reading that turned his words into counts and ceilings in the pulse; the module keeps the counts as evidence under the reminder (S48).

**B5.1  Record `ce46fb` entry #2 The heartbeat reminds flows to do a sanity check; the judge of sanity is the flow**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/ce46fb/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: correcting my reading of the previous entry, which I had turned into counts and ceilings in the pulse.

"I don't know if you understood what I meant. I said, 'Make those heartbeats.' One of the things that they remind us of is to do a sanity check. I can let you be the judge of what is sane and what is insane. Use an agent, maybe use a subagent, to check what all this chatter is about and to check for signs of insanity, like an echo chamber (where things just go in a circle over and over) and where the amount of jargon and nonsense keeps increasing."

-- psyche, STT.
```

#### B6. 36ac89, 2026-10-25: brief corrected to belief

'Belief not brief, belief' (a transcription correction inside the record).

**B6.1  Record `36ac89` entry #2 What touches a topic goes to that topic's flow**  
Date: 2026-10-25 (in the record's context). File: `flows/36ac89/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
2026-10-25, to Psyche core Secondary 36ac89, right after his words on belief modules were passed to the core Primary.

> And obviously anything that touches a particular topic that we have a flow for should also go to that flow. And that should be part of your brief.

Correction, same exchange: the last sentence above reads "And that should be part of your [belief]." His word: "Belief not brief, belief."
Transcription corrected: "brief" → "belief".
```

#### B7. e3c8c1, 2026-10-23: 'strip out, throw out, delete, remove' corrected

He corrected the record: 'delete, delete, delete, remove, remove, remove'.

**B7.1  Record `e3c8c1` entry #7 2026-10-23, living, direct, to Psyche core Primary e3c8c1**  
Date: 2026-10-23 (in heading). File: `flows/e3c8c1/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
"The more code there is in the system, the more chances there are for the system to break so strip out, throw out, delete, remove."

-- psyche, STT.

Correction of the entry above, by the living: "No I said delete, delete, delete, remove, remove, remove. I said it many many times."

"The more code there is in the system, the more chances there are for the system to break so [delete, delete, delete, remove, remove, remove]."

-- psyche, STT. Transcription corrected: "strip out, throw out, delete, remove" → "delete, delete, delete, remove, remove, remove".
```

#### B8. a91f2b: a misattributed order

The living said the message about a main flow without a subflow tool was not addressed to a91f2b; the same words are 6e2616 #3.

**B8.1  Record `a91f2b` entry #1 A main flow is started with subflows**  
Date: unknown (none in the record; date of the file's first commit). File: `flows/a91f2b/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: Psyche ethos Primary a91f2b reported it was started with no subflow tool bound and read files itself in place of delegating.

"There's a primary flow that says he doesn't have a subflow tool so stop starting flows without subflow tools. How can you have a main flow that can't use subflows?"

-- psyche, STT.

Correction to the entry above: the living said the message was not addressed to this flow; the context line naming a91f2b as its occasion is the flow's misreading. The quoted words stand as spoken.

-- flow a91f2b.
```

**B8.2  Record `6e2616` entry #3 2026-10-23, living, direct, to Psyche core Primary 6e2616**  
Date: 2026-10-23 (in heading). File: `flows/6e2616/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
"There's a big problem. There's a primary flow that says he doesn't have a subflow tool so stop starting flows without subflow tools. How can you have a main flow that can't use subflows?"

-- psyche, STT.
```

#### B9. d68c82/archive-flow, 2026-10-14 and 2026-10-19: removals and reversals the living made

He had the 'misnomer' clause taken out of the synthetic-intelligence line; asked that the Nix-language analogy be dropped; asked 'flow ethos' not 'flow definition'; marked the subflow-replacement vision as long term and general.

**B9.1  Record `d68c82/archive-flow` entry #13 2026-10-14 — a flow and synthetic intelligence (landed with the misnomer clause removed)**  
Date: 2026-10-14 (in heading). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> Take out the part about artificial intelligence being a misnomer. That's not necessary.
> Otherwise it's good. Land it.

-- psyche, STT, book comment on «Flow philosophy and artifacts» P1.
```

**B9.2  Record `d68c82/archive-flow` entry #29 No Nix-language analogy for the flow specification**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
> Don't use the Nix language analogy. I don't think that you really got me. It doesn't sound right the way you say it so just drop it unless you can say it properly. I don't think it's necessary to make that analogy. It's like the domain-specific language.

-- psyche, book comment, 2026-10-19T17:46, input mode not shown.
```

**B9.3  Record `d68c82/archive-flow` entry #31 Flow ethos, not flow definition**  
Date: 2026-10-19 (in the record's context). File: `flows/d68c82/vision/archive-flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: comment on "The shape of a definition, with an example, is in vision-flow-definition."

> Why are you calling it "flow definition" and not "flow ethos"? The language is ethos. We already said the ethos goes in ethos-named modules so why are you departing from our guidelines?

-- psyche, book comment, 2026-10-19T17:47, input mode not shown.
```

#### B10. 73b5d8, 2026-10-29: the vision-code line half good

He said the proposed line was half good, with a ghost effect from the single example; the line was to name the stacks, not one example.

**B10.1  Record `73b5d8` entry #4 2026-10-29 — The vision-code line names the stacks, not one example**  
Date: 2026-10-29 (in heading). File: `flows/73b5d8/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: the living, same chat, on the proposed line "Vision code is mostly Ethos and Datom; where a design depends on how a tool is used, Nix among them, the statement carries that code as well."

Your proposal is half good. One of the problems is that we now have a ghost effect because your example would skew the balance. We're welcome to give examples, but let's not forget the most important stacks that we use, right?
```

#### B11. da2038, 2026-10-14: old vision conflicting with the long-term vision

He said the book held obsolete, conflicting vision and restated the long-term vision (a needed flow is started whether or not it is running).

**B11.1  Record `da2038` entry #3 A needed flow is started, running or not**  
Date: 2026-10-14 (in the record's context). File: `flows/da2038/vision/flow.md`  
Context and the living's words, verbatim as logged:
```text
Context: same book, proposal «an undelivered request tries a higher power, then lower; a crucial metaflow missing is started», 2026-10-14T15:18; relayed by Psyche Core Secondary.

> We have old vision that is now obsolete in there, with a conflicting vision. The long-term vision is that the flow is started if it's needed, which means it doesn't matter if it's running or not. Even if it doesn't have any working transcript to reawaken, then we just feed it the context modules that this meta flow is supposed to have, along with the prompt that it's supposed to be getting now.

-- psyche, STT, 2026-10-14.
```

### C. Index: lines or clauses with no record found

These are the places where no raw record words the line; they rest on a landing commit, a book proposal, or the machine's composition. Listed so the Primary can weigh them without a record behind them.

- **S5 The Capsule**: Landed with the module's Capsule paragraph; the first embodiment (credentials only copied, everything else recreated) is route (a) approved 2026-10-02, the volatile-key encryption is route (b), 'a design for later'. 'Its own sockets and store' is from 3ec648: "create and use a different socket". 'Running light models': 3ec648 testing record. No record found that words 'only the credential files are copied ... with its own sockets and store' as one statement; it is assembled.
- **S23 Flow's configuration holds each metaflow's purpose and the records of the living it rests on**: Landed 51731e8 2026-10-20 ('Land Nexus questions ... Flow configuration holds purpose and records'), from 379e7a's book 'nexus-questions' (the book 'The Nexus: questions for the living'). No raw record of the living words 'purpose and records' as such was found; it answers a question of that book. Related living words on configuration-as-data are listed.
- **S36 The flow repository holds the machinery; belief modules live outside it**: 'Machinery' and 'basic modules replace the harness prompt, our own take' are e06e4c07 2026-08-19. 'A module changes live' (6c1763f) answers 'Context modules deploy faster than I can blink' (5ec12c 2026-10-22). No record found worded as 'runtime repository'.
- **S37 Reaped by the refresh itself**: Landed 53f68b6 2026-10-16; trimmed 6c1763f. No record words 'reaping belongs to the refresh event'; the substance is d8df70's 2026-09-24 answers.
- **S47 A permission prompt is a launch failure**: Landed 7427210 2026-10-22 with the message 'c068b8 crystallization'. No raw record in c068b8 or elsewhere was found that words a permission prompt reaching the living; the nearest records are listed and are not asserted as the source.
- **S49 The heartbeat reaches only a flow for which something changed**: Landed 46c7192 2026-10-24. No raw record found that words 'only a flow for which something changed that bears on it'; the nearest are the heartbeat records above.
- **S52 What a refresh carries**: Landed f94d063 2026-10-25 ('what a refresh carries'). Note the living on 2026-10-26 (74e4d1) says no summary and no handover are passed; belief modules and raw vision logs are. 'Presentations and illustrations' ties to 48cff7 (2026-09-16: flowcharts, visuals, concepts). No record found that words 'the basic skills are everything a flow needs'.

Other clauses with no raw record found (found while reading): the Capsule's 'its own sockets and store' as a unit (S5); 'runtime repository' (S36); 'reaping belongs to the refresh event' (S37); 'a poller that must exist is registered and reported' (S38); 'a compaction is a refresh that was missed' (S40); 'only a flow for which something changed' (S49); 'the basic skills are everything a flow needs' (S52); the Mermaid figure (S25).

### D. Records that were gathered and found not to bear on the module

The scan (flows/*/vision/flow.md, 257 entries; and the refresh, capsule, herdr, hook, launch, wake, queue, seat, metaflow and flow* files) also met records on: seat naming (`seats.md` files, superseded by 'there are no seats; a seat is a flow'), flow behavior, flow anatomy, flow launching scripts, flow artifacts, the dimensions of the Metaflows (a notion, 2026-10-04, astrology), and the Illustrator books. They are not cited above because no statement of the module rests on them; the Primary may open `flows/*/vision/seats*.md` and `flows/bad807/notion/metaflowDimensions.md` if wanted.
