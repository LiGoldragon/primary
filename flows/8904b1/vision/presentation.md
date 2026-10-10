# presentation

## 8904b1-27 — 2026-09-28, the living, direct to this pane

Raw. Mode of entry not stated; "Clojure artifact" reads as speech-to-text for "Claude artifact".

> Yeah your lock edit suggestion is good.
>
> I don't know what the set-aside skills are. I can't search all of this chat for everything. This is the chat UI problem that I've brought up before. If there's something for me, you should just make a Clojure artifact for it then I know where to find it. What do you think?

## 8904b1-30 — 2026-09-28, the living, direct to this pane

Raw. Mode of entry not stated. "The book" and "the page" are the standing page "For You".

> I've made several comments on the page you made and we can use this. I've also made an important comment in respect to this. I think this will be the flow with Psyche, where I'll be interacting with the book instead of the answers, because agents talk to each other so I can't keep track of everything you're saying.
>
> We could even make a skill that minimizes unnecessary comments the model makes and only focuses on this: every response will be a sort of presentation. I even have the idea that in the future it won't even be necessary for the main flow to call a sub-agent to make the page from his transcript. It'll just be done automatically. It won't be a page. Obviously it'll be an app. We're going to make our own user interface in Unity.
>
> Whenever an agent returns some kind of mechanism will be thrown into gear and maybe some other LLM calls will be used in order to make changes in the user interface in Unity. We can use the concept of using pages for now that I can comment on, which Claude has an interface for, but eventually I would like to use the application itself.

## 8904b1-32 — 2026-09-28, the living, direct to this pane

Raw. Speech to text by its look. "Menchi" is Mentci. The whole message, one record; the Mentci ruling, the page sub-agent, hooks and events, and where sub-agent files live are all in it.

> I think the Menchi you're referring to is obsolete now. Menchi is just a nexus and we're calling the user interface Unity. If there's a GUI called Menchi there, we should just archive and mark as stale and abandoned.
>
> I've contacted you because I'm trying to save tokens and I would like to design this subagent with you. It's a subagent that you call with almost no argument, with almost no prompt, and it knows how to find your transcript and create a page from it that I can use so that it knows to prioritize. I think Opus would be good for this and then it can maybe use Sonnet as a subagent. I don't know but I would like to design something efficient and then eventually we'll turn that into some kind of hook that just gets triggered when some kind of event comes out of the harness. What kind of events?
>
> Also let's get somebody to look at what we can hook into the harness instead. I see a world where everything is a hook and an event and triggers something so that it's not really the decision of "Do I spawn a subagent?" It's like, "I would like a subagent." Here's the vision, right? Or here's how it would look. The flow would just give its final answer and eventually everything will be datom-specified, like an ethos. It'll come out with this final answer that implies that some subagents could be called on certain things. It'll be up to some other mechanism, probably some kind of token accounting mechanism, to decide if subagents are launched, which ones, and how much, which model, and how much effort they're each going to be.
>
> For now I wanted to just develop the concept in the normal subagent file that we'll put in, that Claude can use anyway. Let's talk about how subagent files get put in. Do we create a subagent section in each of the skill repos so each aspect can create its own types of subagents?

## 8904b1-33 — 2026-09-28, the living, direct to this pane

Raw. Sent while this seat was working on 8904b1-32.

> You could also get a small sub-agent to go around and fill your user prompt context with the right vision for what I just talked about and what I just covered.

## 8904b1-34 — 2026-09-28, the living, direct to this pane

Raw. A correction of this seat's design of the page sub-agent, which had fed the page from the living's words and the seat's final answers only.

> No but I'm not saying we don't get a tool to get the transcript. There could be several parts involved in the page. It's not a final answer. That's what I'm saying. The problem is you're missing the whole point. My whole point is that, with the chat's vertical scrolling, I miss everything. The thing I need is not in the final answer. That's my whole point. We need to make a page from everything, where contradiction is won by the most recent output or input or whatever.

## 8904b1-35 — 2026-09-28, the living, direct to this pane

Raw. On this seat's table saying all of the living's words go into the page.

> I wouldn't say that all my words need to go in. I think this is a good opportunity to trim out my words, trim out the fat, trim out the unnecessary bits.

## 8904b1-36 — 2026-09-28, the living, direct to this pane

Raw. Speech to text by its look; "a mine aspect" is a Mind aspect.

> Well the concept is that a sub-agent is being called by the flow that wants its transcript in a page so that the living can interact with that flow (even though it's talking to a bunch of different agents). It would be really hard to do that by reading the chat. It would be hard to interact. Yeah like you said, this is a perfect opportunity to start distilling the psyche's words into a more assimilatable form and a more coherent form.  And by trimming my words I mean taking out the parts that aren't necessary, not rewording it. We don't need my words in there because I said what I said. I know what I said. The page is for me. Really you're right: we should just distill my words and then if I approve, everything will be like, "Here's a proposed distillation." Every proposed distillation should have a proposed destination: which skill would hold it? Even when we're able to do this with OpenAI Codex, even a field or a mine aspect could get stuff from me when they're able to make these pages, to tell them if they get my words right in terms of making a skill with it. Which is its own form of distillation. You can distill psyche into psyche or, arguably, if they run it by me and I approve it, then it can become vision or intent. Unless all I say is, "Yes this is a good compensation skill, a good trial skill, a good operation skill, or a good documentation skill," if I just say that then it can just go in. We're just concerned with Claude right now because Claude is the only product that can put together these artifacts that I can comment on right now.

## 8904b1-37 — 2026-09-28, the living, direct to this pane

Raw. Speech to text by its look; "herder" is Herdr.

> Well tell Astra to spawn a Sol Flow and then when we have very, very well-specified stuff, Astra can do it. There's no reason why. Let's just start a Sol Flow. Tell Astra to do it and load him with what's necessary to review maybe the generator or what?
>
> I feel like I don't have a lot of Claude usage for this week because of that dreaded night and I have a Codex reset so I could lean on Codex more or maybe just start the Astra field.
>
> Ask one of your Opus subagents to start an Astra field aspect in the same herder and make him all reachable with the messenger. Let's design this subagent thing so you can use it right now. Maybe let's just write it in the primary so you can do that. You say you want to inject skills. I guess if it's Claude, Claude can load skills on its own, actually, because it ends up in its middle stratum. We can tell the subagent what skills to load or, like you said, you could just have the skills injected in the prompt.
>
> I guess let's just weigh the pros and cons of each approach. For now we could just tell him which skills to load and give him the instructions on how to turn the transcript into a page, and which subagents, if we use subagents, to use and how it's defined that subagent as well so that it's already well trained.

## 8904b1-40 — 2026-09-28, the living, direct to this pane

Raw. Sent while this seat was working.

> So where are we? Let's look at the design of the page or the book subagent. I think book is better but yeah whatever, it doesn't matter. Just call it a page.

## 8904b1-43 — 2026-09-28, the living, direct to this pane

Raw. On this seat's remark that the page's own code lives only on the page and should be held in Primary.

> No I don't think the page goes in primary because the page was made. Primary is mostly to hold skills and subagent definitions and to let the flows log in a very technologically obsolete manner (because we don't have a nexus for them to store their things in properly). Nexus still doesn't have some kind of version control system for their data, which we're going to need. No I don't think the page goes in primary. The primary is already overloaded. The transcripts and the logs are there. The page is there somewhere. I don't want to duplicate. This is a form of duplication.

## 8904b1-44 — 2026-09-28, the living, direct to this pane

Raw.

> Would there be a way to resume a book update sub-agent so that it would know from where, which part of the transcript to consider to modify the page? Giving someone an HTML for context is really bad. You're saying you're going to give the page for handover, isn't that HTML? That sounds like a really bad idea. That's what I think it is.

## 8904b1-46 — 2026-09-28, the living, direct to this pane

Raw.

> So you're saying the successor reads the rows in a database. Where is that database? Where? How does this page thing work? You can get your successor to explain that.
