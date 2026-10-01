# Core

## The core layer: a Codex, or a Codex-heavy pair, running checkup jobs that see whether the system is fine, not paralyzed in a self-update failure or a network sandboxing problem, fixing it and bringing it back online; when nobody is doing anything it wakes the primary and asks why it fell asleep, whether the quota is low; the flow talks to itself about whether to work and on what, or messages the living and waits; unanswered, it asks what the living would want, or saves and wakes later; for now Codex does the wake-up

Context: typed to the primary Claude 840e42 after the channel decision. "Luna jobs" is left as typed, not recognized (the third time "Luna" appears); asked in the reply. "Let's use Codex mostly for the wake-up" is also a working instruction, recorded in log.md. Logged directly by the main flow before acting.

> You should set up a layer, a core layer: a codex, or a pair, but it's codex-heavy in that the codex runs these checkup Luna jobs to see if things are going okay. It checks if the system hasn't paralyzed into some kind of weird self-update failure thing or some catastrophic network sandboxing problem or whatever. It can fix it and bring the system back online.
>
> If nobody's doing anything, it can maybe message primary and say, "Hey, did you fall asleep? Do you want to get back to work? Maybe on this and this, crucial things: why did you fall asleep? Is the quota low? Did I not see that?" You start talking to yourself about whether I should be working and on what, or should I message the Living, right? Then wait for my answer. If I'm not answering, then ask yourself what the Living would probably want us to do, or should we save our thing and wake back up in a bit?
>
> That would be the core layer's job, and for now, let's use Codex mostly for the wake-up.

-- psyche, typed.
