# Head-start provenance

head-start.md, 1989 Unicode characters (python len), held for the living; no Fable Primary started or briefed.

## Psyche quoted
- "Let's rewrite it in idiomatic Nexus architecture and ethos ..." — 2026-10-14, STT; flows/d68c82/vision/nexus.md, full copy flows/7c89aa/vision/ethos-in-clojure.md; this flow vision/chronos.md.
- "Everything is tropical, even the [nakṣatras] ... the apogee." — 2026-10-14, STT, to da2038; flows/da2038/vision/spirit.md; this flow vision/chronos.md. Omission marked " ... ".
- "Showing me types in Rust is kind of silly. Like I said, we have Ethos" — 2026-10-07; flows/d4ae97/vision/ethos.md.

## Ruled lines summarized
- vision-nexus (authored psyche-context/skills/vision-nexus.md): Sockets, Default clients, Configuration, Three parts and one path, Observation by subscription, Polling is forbidden, Signal only (typed refusals), Repositories.
- vision-ethos (authored psyche-context/vision/ethos.md): four roots Library, Signal, Operation, Memory.

## Source facts (read-only subflow, not built or run)
/git/github.com/LiGoldragon/chronos at 500094596de495b81cf32b35e127905e7ab0fc42:
- requests: src/request.rs:68-76; daemon handles only SetLocation/GetLocation: src/daemon.rs:58-64,155
- wire rkyv, 4-byte BE length, 1 MiB cap: src/wire.rs:4-5,12; store redb state.redb, table location, key current: src/daemon.rs:100-123
- zodiac projection: src/zodiac.rs:60-78,290-309; solar event kinds: src/event.rs:30-40
- astronomy todo!(): src/sky.rs; anise, solar-positioning unused: Cargo.toml:78-93
- README/ARCHITECTURE claim DE440, NREL SPA, five output formats, Kameo topology, geoclue: not in code (claims).

## Tensions not carried in the head-start
- Raw nexus records beyond the skill: actor isolation (Signal and Memory talk only to Operation) and standard entry point, flows/aa887c, bad807, 5ed94b vision/nexus.md, 2026-10-04; config via successive Datom payloads on the meta socket, flows/445410, 73ada7, 0c85a3, 2026-10-09.
- vision-signal and vision-sema older than the four-root vision-ethos.
- Prior Chronos 0.3.0 scope (location) versus the living's astrological-time scope; nothing reconciles them.
