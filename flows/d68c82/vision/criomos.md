## Nobody edits files; the system is declarative
Context: the living, 2026-10-11, reacting to "someone has to change the file" about the Prometheus Wi-Fi.
"It sounds like you're telling me that we shouldn't be using a declarative operating system anymore. You're saying someone has to edit a file. Well first of all nobody edits files anymore. People do not edit files anymore. That never happens anymore, ever, ever, ever, ever, ever. ... you're saying we have to abandon declarative operating systems. Why are you taking it upon yourself to decide that we're changing all the architecture and how things are done?"
-- psyche, STT.

## A proper fix replaces every hotfix

Relayed by Psyche Core Tertiary, 2026-10-15; the living spoke to it directly, after a power outage, on the laptop battery draining too fast during suspend.

> I noticed that the battery has still gone down way too fast for a laptop on suspend, so I need that fixed. I don't want to have that problem again. Next time I put my laptop to sleep, it should not do that. Get the fix in [CriomOS]. I don't want a hotfix, and I want all possible hotfixes that are in now to be removed and replaced by a proper fix and proper deploy.

-- psyche, STT. Transcription corrected: "Creo OS" → "CriomOS".

## A hardware fix keyed by hardware in cluster data

Relayed by Psyche Core Tertiary, 2026-10-16; the living's comment on «Battery drain in sleep», the whole book.

> I want this fixed in. Let's treat this knowledge proposal as basically a goal right now: a field has to figure out how we fix this so we can test it at some point.
>
> I'm not saying the field has to figure out if the fix can be put in while we're still running. If not, or if he's not sure, then the fix that mine goes and passes through Priamo S [sic] to fix this should become a variable that we can put in the cluster data about what kind of hardware. This should be marked by the right kind of chip, or whatever piece of the hardware makes this skill, this fix, necessary.
>
> It should be a method, like `is this this type of chip right on hardware` [sic], which can then look up a table. We make a list of the hardware that we have, and it can answer all of these questions depending on what kind of processor it has and stuff. We can have a library that uses this data and can check if certain things need certain fixes, depending on what the computer model is and what variant it is, etc.

-- psyche, STT.

## Nothing opens tabs in the desktop browser on its own

> We have a constraint: we need to determine whatever it is that's opening all of the [Claude] artifacts in my web browser on my desktop while I'm away. It's just opening a new tab every time, so it's going to chew up all of the RAM in Chrome tabs. Let's get a specification, and then let's get that through with a [CriomOS] vision review. Does it even exist? Let's create it.

-- psyche, STT. Transcription corrected: "Clojure" → "[Claude]"; "Creo OS" → "[CriomOS]".

## Never a hard-coded Nix path

> "There can never be a hard-coded Nix path in Nix code. That's insane. It has to resolve to something. The first part, with all these variables being set: should these variables belong in modules and imports at the top there? This is very badly written code, there for sure. We cannot have a hardwired Nix path. I don't even know how this came to be but it's an aberration. I want a deep deep deep deep investigation with a fix, an audit, and a counter-audit. I want to exterminate every single trace of this bad pattern: out of history, forever, future and back, behavior change, everything, hard."

Context: comment on «CriomOS: the desktop opens nothing on its own», on CriomOS-home codex-remote-control.nix (occupiedCodex and occupiedNextCodex store-path literals), 2026-10-19 01:07.
-- psyche, STT.

## A new artifact does not open a tab on its own

> "No I didn't say that I don't want things to open tabs. I said I didn't want [Claude] Desktop to always open a new tab every time there's a new artifact. That's different and that's what it is because we're automating things. Sometimes I have [Claude] Desktop or whatever it is that opens (it might be the [Claude] Harness) open a tab when there's a new artifact. I don't want that."

Context: comment on the same book, Proposal 1, line "Nothing opens a tab in the desktop browser on its own.", 2026-10-19 01:05. Transcription corrected: "Cloud" → "[Claude]".
-- psyche, STT.

## Librem 5

> "Librem 5"

Context: correction of "Libre M5 Linux smartphone" in the same book's hardware line, 2026-10-19 01:00.
-- psyche, STT.
