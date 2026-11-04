Landed: vision:nexus-v1 and its three sibling modules, psyche-belief commit 3ac8d7b

# Version one

## 2026-11-03 — raw, from the living, heard by { Psyche core Primary 04df39 }

> Our Flow Nexus is deeply broken in many ways and I'm not sure that we need to really fix it because I would rather make something quite different. Maybe there are a few things worth fixing, I'm not saying.

> We have a bit of Codex usage left, I think, until tomorrow morning or I'm not sure. Someone can check on that. We should maybe use that to try to get some fixes in the version 0. I'm going to refer to them as version 0 and version 1, right? The current version is version 0. Version 1 is going to, hopefully, do the translator-type Nexus. For the new type Nexus maybe we can also use the same numbering there. The version 0 type Nexus has no translator and the version 1 type Nexus has a translator and then potentially more things.

> Obviously I'm talking about the general Nexus arc architecture here too, right? Any Nexus in the version 1 format uses a translator so the version 1 Flow Nexus would. I would like to make the first version really simple, just so we can see it in action, see the translator working, and see some basic flows being launched.

> I'm going to change the vocabulary a bit in version 1. I think we're going to have the concept of a complex so the whole primary, secondary, and all that is, I think, going out the window. That's invented layering that's burnt into the logic and therefore opinionated. I want to take the opinion out and make the machine completely configurable.

> We'll have this domain-specific language, kind of like how Nix is a language to design operating systems, even though Nix as a language sucks. Datom, or a Datom-based language, is going to be used to configure this.


> Right what I'm saying is you could have just told the subagent to recover my words, right? Or that's kind of complicated but you can see how the complex solves this: even early on, even before we have an actual app (the Unity app, which I plan in the long term), it knows what to do with my words before they're passed to Fable. Meaning Fable wouldn't have to log anything because that would be taken care of by some other complex thinking machine logic, however many models are involved in that, right?

> We started working on this with the anatomy part and I don't want to get into the anatomy. The anatomy will be up to the user to define when we create this new nexus that essentially makes all of this configurable.

> In the short term, for example, you could spin up a cheap Haiku flow and I guess what you did was judge which part of what I said should be logged or something. There is, I guess, some kind of judgment there, am I right? Anyway if not, or maybe there's a way to do this properly.

> The goal is for you to be able to start a subagent or to spend as little. I'm not saying we can do this right now but the goal is for Fable. For example the model that discusses ideas did not have to take care of this bureaucracy: you used 500 words of your output, which were already in your transcript, so there's a total inefficiency there. Do you know what I mean? 

> No the part which is vision, which is notion, is the judgment so that is your job. Well maybe not. Maybe we don't need Fable to judge that or maybe it's several models together that can do a good job of that. It's okay, it's okay, I'm just saying. Anyway we don't need to spend so much time on that. Do you understand how I see this new Flow Nexus? 

> Well like I said, a bunch of what you said isn't for the first prototype, right? Obviously the first prototype has to be approached simply so it can't have all of the features that you just listed. That is the problem that we've been struggling with: how do we separate what the next implementation should have from what future implementations should have? It's easier to understand what the prototype should do by understanding what the eventual fully featured version wants to do.

> If we give everything to Opus or Astra, or even if we give a Fable Flow all of this information, what I've seen happen is that the implementation ends up being a Frankenstein of all these environments. That can't really be done all at once in one system, right? What I'm describing is a bunch of components. There's way more to the vision that you just described than just the flow nexus. Do you follow me? 

> Well the most important component is the flow nexus. This is, right now, the way we start flows, which is very suboptimal. There has to be a better way to customize which tools each flow has. Essentially I also think each flow should have its own working directory. Potentially that could even be done by some other sandboxing-type nexus and this brings up the problem of multi-nexus systems, which hasn't really been achieved yet.

> It would be cool to make the flow nexus simple: this is version 1, the new rewrite, and then couple it with maybe one or two other nexuses that do something simple. We could have another nexus that sets up a working directory. We are going to go in a sandbox-type thing although at first there could just be no sandbox. It could just be simple stuff like setting up a directory that will be cleaned up, maybe with just the repositories that I... No I don't want to get too complicated.

> The other simple nexus that we maybe have is one to handle the herder pane that Flow talks to, to do all of the herder stuff instead of putting all of the system herder system call logic in Flow or in its translator, right? The herder nexus would have its own translator that can take care of that. I see that maybe in the short term it might make things a bit more complicated to set up but then it would be easier to fix things. If herder has a problem or if there's a new version that changes things, then we don't have to rewrite the Flow nexus.

> I'm not saying we need to make a herder nexus and then obviously a better skill generator, which we were saying we were going to rewrite with a new name: belief. I think that is the right word to represent what a model actually believes when it starts, right? It's its beliefs.

> There's a lot to discuss here. Probably the best way is to just start suffixing all of this vision, in regard to version 1, with v1 on the modules that we would create for this design. That way it doesn't get confused and then we can start a flow, potentially even restart you, with just a concentration on version 1 of things and without the version 0 modules. Then we can start to focus on that particular vision. 
