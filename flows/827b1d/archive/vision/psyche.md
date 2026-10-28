# Psyche

## 2026-10-28 — Raw records carry their state; landed records move out of the open file, perhaps to an archive directory

Landed: vision/psyche.md, 3a12dc
Context: the living, direct to Psyche core Primary 827b1d, after the startup that remembered settled records and missed open ones; before reading the book Record state.

> We need to design a system that allows us to better pick. Probably we need to design a way to mark. I don't think we have any emphasis on marking or archiving or I don't know how we want to say this. Maybe the archiving language is the wrong language but some way for the things that have either been landed, changed, or refuted to not be passed over.

> Not only were you given things that were already settled but you weren't giving the things that were not settled.

> First I want to say: rename the file. If we rename the file then we don't need to write anything in it. That's the first thing I would say to that. Even if we do keep that system, we should at least be explicit about it. But actually that doesn't do because a file is not a thing. A file contains things so things in the files might be done and some other things in the file might not be done. We use the file to pass over the context.

> If only parts of the file are landed and if we do keep this file-based system, then the parts that are landed are moved into the otherwise fixed file. If keeping it in the same directory makes recovery more problematic for filtering out what was done and what wasn't, then maybe the archive lives in a different directory. That way it's easy to query for what has landed and what is believed to have not landed.

## 2026-10-28 — Long term, the records live in the psyche nexus

Landed: vision/psyche.md, 3a12dc
Context: the living, direct to Psyche core Primary 827b1d, agreeing that landed records move to an archive directory with a state line, open records carrying nothing.

> Yeah I think we're starting to agree on stuff and the long term is the psyche nexus obviously.

## 2026-10-28 — The archive directory is named explicitly, for predictable behavior

Landed: vision/psyche.md, 3a12dc
Context: the living, as a comment on Proposal 1 of the presentation Record state, on the words "in a separate directory".

> This is good but we need to be explicit about what directory we're talking about so that we can get predictable behavior, so that scripts and tools can work reliably to find archived data. Do you know what I mean?
