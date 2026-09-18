# Operational: cluster data specification — model table derives facts, Field verifies at boot, manual override for unknown hardware

## If we have a model table, it knows from the model what the CPU architecture is. Field could run a check after boot. Otherwise, set the architecture manually. Different form factors are variants for the interface style, with sections for audio, visual, interface

Context: spoken by the living to primary Psyche opus (Claude, medium, flow
b05237) on 2026-09-18, refining the hardware type system from Fable's
proposal. The living names this as cluster data specification. Three layers
of hardware knowledge: (a) a model data table that derives everything from
the model string — CPU architecture, display, form factor; (b) manual
override when the model is unknown but the architecture and form factor are
known; (c) Field Nexus verification at boot, checking what the hardware
actually is. Form factors are variants described by what they are: handheld,
laptop, paper-size tablet, high-DPI / low-DPI variants, large tablet.
The hardware record has sections: audio, visual, interface, and others not
yet named. These sections could be a vector of capabilities or a struct with
typed fields. Logged by the main flow before acting.

> Well, on the hardware, we're defining the cluster data here, the cluster data specification. What we could do is, sometimes we don't have the full model. If we have a model table, like a data table for each model, then it knows from the model what the CPU architecture is and everything else is. Eventually, we could even run a check after it starts, when it boots from field, right?
>
> Field is now the one we can open that up and draft the anatomy. Field is like our system interaction monitoring nexus. If we set the model, then it could get the CPU architecture and everything from the table. Otherwise, we could set the CPU architecture manually if it's something that we don't know the model of, but we know that it's, for example, an ARM64, a high DPI density handheld type, or a low pixel density handheld type, like a smartphone (i.e., a smartphone that's described by what they are: handheld, laptop, paper-size tablet, high DPI, high-density paper-size tablet, or high-density large tablet).
>
> All of these different formats would be some variants that we could pick from the interface style, if you will. It could be a vector of things, or it could have different sections like: audio section, visual section, interface, other interfaces that I haven't named.

-- psyche, direct to primary Psyche opus b05237.
