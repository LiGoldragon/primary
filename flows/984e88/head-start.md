You design Chronos as an idiomatic Nexus: a full Ethos specification of its Library, Signal, Operation and Memory. Design only; questions go through Psyche Chronos Secondary 984e88.

The living, 2026-10-14, speech-to-text:
"Let's rewrite it in idiomatic Nexus architecture and ethos: full specification, just a simple thing, right?"
"Everything is tropical, even the [nakṣatras]. [Aśvinī] 0, and then 0° Aries is the first when we talk in ordinal notation ... reviving the Chronos [daemon] and then making it a [daemon] that does astrological times, either in pure solar or solely lunar format and maybe other things too, like with the lunar nodes. I really pay attention to the lunar nodes, the aphelion, the apogee."
And 2026-10-07: "Showing me types in Rust is kind of silly. Like I said, we have Ethos"

Ruled (vision-nexus, vision-ethos): four roots; a signal reaches memory only through operation; one operation for every effect; an ordinary and a meta socket; signal-chronos and meta-signal-chronos; the CLI takes one inline datom; starts with no arguments, defaults seeded into a new database; state observed by subscription, polling forbidden; refusals typed.

Current source, chronos 0.3.0 at 5000945, evidence only: Rust with .ethos/data/chronos.ethos. Requests GetTime, GetSchedule, GetLocation, SetLocation, UseGeoclue, Subscribe; only SetLocation and GetLocation work, rkyv over a Unix socket into redb. Zodiac projection from ecliptic longitude to sign, degree, minute, 0° = Aries. Solar event kinds CivilDawn, Sunrise, SolarNoon, Sunset, CivilDusk. All astronomy is todo!(); no moon, nodes or nakṣatras; anise and solar-positioning unused.

Open choices, for the living:
1. Which quantities the first spec holds: solar, lunar, nodes, apogee, aphelion, nakṣatras.
2. Ordinal notation: how 0° Aries and Aśvinī 0 are counted and shown.
3. Location: set on the meta socket, per request, or both.
4. What Memory holds beyond location and subscriptions.
5. The ephemeris source.
