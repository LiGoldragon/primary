# Signal

## 2026-09-10 — signal is portable rkyv plus whatever protocol is standardized; the protocol is TBD for now

Context: the flow asked whether "universal signal is a CapnProto implementation of Ethos" stood beside "portable rkyv".

> signal: portable rkyv + whatever protocol we decide to standardize (talked about before but just mark as TBD for now)

-- psyche, typed.

## 2026-09-10 — the universal signal repository: shouldn't it just be "signal"?

Context: the flow asked whether the agent-named crate signal-standard is the "universal signal repository every component depends on" of the Nexus vision's Routing statement.

> 3. shouldnt it just be "signal"?

-- psyche, typed.

## 2026-09-10 — merge the signal repositories into signal, starting with the recently written code, not unused code; archive the old signal repo, rename signal-standard to it; old git history not needed

Context: the flow presented the legacy signal repo, signal-standard, and signal-frame as candidates for "the signal repository" and proposed merging standard and frame into signal.

> Yeah, I think you understand the Signal repository, so we could merge all of that there, but let's not just throw a bunch of code that no one's using in there. Start with the code that was written recently ... Let's make sure that whatever depends on Signal standard is then depending on it, or just archive the old Signal repo and then rename the Signal Standard repo to it. We don't need the old Git history unless you think there's something useful there. I don't know. Maybe let's talk about this further, or give me a better view of everything.

-- psyche, STT.
