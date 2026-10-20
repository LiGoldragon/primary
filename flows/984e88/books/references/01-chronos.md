# References: Chronos

Source: flows/984e88/books/01-chronos.md. Not rendered.

## Provenance of the Chronos module

- flows/984e88/vision/chronos.md, 2026-10-14, both records.
- flows/d68c82/vision/nexus.md, 2026-10-14, «Chronos as the Nexus test».
- flows/da2038/vision/spirit.md, 2026-10-14, «Everything is tropical».

## Archive, on approval

- flows/d68c82/vision/nexus.md «Chronos as the Nexus test», into its archive- file.
- The first record of flows/984e88/vision/chronos.md, into its archive- file.
- The tropical record (flows/da2038/vision/spirit.md) stays raw: its firmament and Sun-as-energetic-centre words are not crystallized here.

## Destroy, on approval

- The impurity in flows/984e88/vision/chronos.md: «Maybe we re-adapt Chronos ... Let's rewrite it», the order to start the rewrite now; the book carries it out.

## Chronos 0.3.0 as it stands

Read by a read-only subflow at commit 500094 of the chronos repository; not built or run. Evidence for the redesign, not part of it.

- Rust, with an Ethos file `.ethos/data/chronos.ethos`.
- Requests GetTime, GetSchedule, GetLocation, SetLocation, UseGeoclue, Subscribe; the daemon answers only SetLocation and GetLocation.
- Wire: rkyv over a Unix socket, 4-byte length prefix, 1 MiB cap. Store: redb, one table holding the current location.
- A zodiac projection from ecliptic longitude to sign, degree and minute, 0° = Aries; solar event kinds CivilDawn, Sunrise, SolarNoon, Sunset, CivilDusk.
- All astronomy is `todo!()`: no Sun, Moon, nodes or nakṣatras are computed. The anise and solar-positioning crates are listed and unused.
- The README and ARCHITECTURE name DE440, NREL SPA, five output formats, Kameo actors and geoclue; none of it is in the code.

## The choices, from the earlier questions

- Q1 (quantities, formats, mean or true) became 3.1 and 3.2; whether the body set is the first set is folded into 3.8.
- Q2 (ordinal notation) became 3.3 and 3.4.
- Q3 (location) became 3.5.
- Q4 (Memory) became 3.6; past readings were dropped, as there is no proposal behind them.
- Q5 (ephemeris) became 3.7. The spans are machine knowledge, not checked against the providers in this edition: DE440 1550 to 2650; the Swiss Ephemeris 13201 BC to 17191 AD; analytic series (such as VSOP87 and ELP) degrade over some thousands of years. The default follows the anise crate already listed in 0.3.0.
- Q6 (aphelion) became 3.8. The living named the aphelion beside the apogee and the lunar nodes, and describes a frame in which the Sun's eye goes around with the firmament on the ecliptic; that frame is why the default takes the Earth's aphelion as the Sun's geocentric apogee.
- Q7 (tropical beyond Chronos) became 3.9. The living said everything is tropical and that the spirit might specify it.
