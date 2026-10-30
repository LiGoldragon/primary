# Flow

## 2026-10-23 — long term hooks feed Flow; Flow a small monolith first; medium term hooks on all harnesses; Flow does the usage accounting; tonight's reiteration works in testing variants, stable keeps running

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
