<!-- to-the-living:start -->
Presentation.{ «How long Flow's lock lasts» }

## The case

Before Message hands Flow a request for a metaflow, it asks Flow for a lock on that metaflow; with the lock it hands Flow the request, and Flow places it. Flow's buildable design stores the lock as a Lock record holding the Metaflow and Until, the moment it lapses in seconds since the epoch, and Flow judges a lapse when the next request arrives by comparing Until with now. What sets Until is open: no payload in either design names the lock's span, so nothing says whether a lock lasts one second or an hour. Message's design proposes 30 seconds, as a constant in Flow's built-in default configuration, and gives as its reason that a delivery into a flow's pane takes up to about 10 seconds today with its waits; that figure is Message's design's claim, not observed here. Flow already takes other values over its meta socket's Configure: in «The Nexus starts» each layer's Threshold, Handover and Refresh, arrives that way, with 20 and 40 percent shown as their values. Message and Flow as designed are in development, none of it in production. That the span is Flow's own and not part of the standard metadata tree every Nexus keeps is this flow's reading, since the span means nothing outside Flow's lock.

## Distillation

### D1. Where the lock's span is set, in vision-flow

Target: `psyche-skills/skills/vision-flow.md`, the paragraph at line 12 under «What it does». It stands as: Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows. The paragraph before it says the Flow Nexus sets up and starts a model flow; the paragraph after it introduces the Capsule. Nothing is removed; one sentence is added after "Flow holds the lock on flows."

**Option (a), a constant in Flow's built-in default configuration.**

Added: A lock lasts a fixed span, 30 seconds, held as a constant in Flow's built-in default configuration; no payload changes it, so no lock lasts beyond it.

Rests on: flows/f5a6e9/vision/flow.md:59 (logged 2026-10-07), on Message asking for a lock that is time-bound so that it does not lock forever; psyche-skills/skills/vision-nexus.md:89-90 «Configuration» (in the file at 2026-10-07), on the executable holding a default configuration as a constant. Message's design proposes this (flows/73ada7/reports/build/message-design.md:453-455), unruled. That «Configuration» goes on to accept changed values through Configure (line 93-94), which this option sets aside for the span, is this flow's reading.

**Option (b), Flow's configuration, changed over meta Configure.**

Added: A lock lasts the span Flow's configuration holds, 30 seconds from its built-in default, and the meta socket's Configure changes it like any other value.

Rests on: flows/f5a6e9/vision/flow.md:59 (logged 2026-10-07), on the time-bound lock; psyche-skills/skills/vision-nexus.md:89-94 «Configuration» (in the file at 2026-10-07), on the default constant seeding a new store and changed values being accepted through the meta Configure; psyche-skills/skills/vision-nexus.md:98-105 «First configuration» (in the file at 2026-10-07), on the metadata tree, written only on the meta socket once configured; flows/73ada7/vision/nexus.md:15 (2026-10-09, raw), on a Nexus's configuration living in datom payload files in different repositories, sent by the CLI in succession on the meta socket. «The Nexus starts» (https://claude.ai/artifact/49gSuEYkmo5dWkFmeNKHVb) carries Threshold this way, as a Configure payload with shown values; its ruling is not read here. That the span would then sit in a payload file beside Threshold is this flow's reading.

**Option (c), per request, chosen by Message.**

Added: Whoever asks for a lock names its span in the request; Message names it, and Flow holds the lock for that span.

Rests on: flows/f5a6e9/vision/flow.md:59 (logged 2026-10-07), on Message asking for the lock, which says Message asks and that the lock is time-bound, and does not say who picks the span. That a span named by the caller is bounded only by what the caller names, so a limit kept in Flow would still be needed for a lock never to last forever, is this flow's inference.

**Ruling D1.** (a) A constant. (b) Flow's configuration, changed over meta Configure. (c) Per request, chosen by Message. (d) Amend, by line.

## Voice

One choice. Flow's lock needs a length, and nothing sets it yet. Message's design suggests 30 seconds. In your comment on the Flow book you said the lock should be time-bound so it doesn't lock forever. A fixes 30 seconds in Flow's built-in defaults. B starts at 30 and lets the meta Configure change it, the way the Threshold values arrive in «The Nexus starts» and the way today's configuration files would load. C has Message name the span in each request. Which one? This flow's reading: C would still need a limit in Flow for no lock to last forever.
<!-- to-the-living:end -->
