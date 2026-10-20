# Chronos source: location, ownership, naming (read-only research, 2026-10-16)

## 1. Repositories

Repository root is /git (SKILL_VARIABLES.md "Repository root: /git"). Only ONE Chronos repository exists.
Searched /git/github.com/*: there is NO signal-chronos and NO meta-signal-chronos. (Siblings exist for many other components, e.g. signal-flow, meta-signal-flow, signal-mind, meta-signal-psyche.) The 984e88 design proposes the meta Signal "in its own repository", not yet created.

### /git/github.com/LiGoldragon/chronos (v0.3.0, edition 2024)
- Default branch: main (origin/HEAD -> origin/main). Working copy is jj, checked out detached at the entry-point branch commit 5000945 (jj working-copy commit 56e6b1c0 is empty). Branches: main, entry-point, chronos-datom-542442 (+ origin/*). Clean.
- Last 5 commits on main:
  - a5cf51f 2026-09-06 Satisfy Chronos current codec Clippy gate
  - 9bbd558 2026-09-06 Finish Chronos current Datom boundary
  - 2daa26e 2026-09-06 Port Chronos request response and location Datom readers
  - 1159159 2026-09-06 Begin Chronos current Datom migration
  - 43703ad 2026-08-29 migrate chronos to Datomic and Ethos
- Last 5 on entry-point (HEAD, the unmerged Nexus entry-point experiment, claimed PASS by d66c26): 5000945 2026-10-04 Expose Chronos entry part types; 7899f0c 2026-10-04 Construct Chronos response errors; 68fa82c 2026-10-04 Route Chronos location through standard entry; a5cf51f 2026-09-06 Satisfy Chronos current codec Clippy gate; 9bbd558 2026-09-06 Finish Chronos current Datom boundary.
  NOTE: the source on disk (src/daemon.rs using `nexus::main!`, nexus rev ec097e3) is the entry-point branch, NOT main. Anyone targeting files must decide the base branch.
- Top two levels (excluding .git, .jj):
  - root files: AGENTS.md, ARCHITECTURE.md, CLAUDE.md, Cargo.lock, Cargo.toml, LICENSE.md, README.md, UPGRADES.md, flake.lock, flake.nix, rust-toolchain.toml, rustfmt.toml, skills.md, .gitignore
  - .ethos/data/: chronos.ethos, datomic_library.rs (486 lines, generated, byte-identical to the ethos per 01a04a30 log)
  - src/: calendar.rs client.rs daemon.rs error.rs event.rs lib.rs location.rs request.rs response.rs sky.rs wire.rs zodiac.rs, bin/ (chronos.rs, chronos_daemon.rs)
  - tests/: calendar.rs datomic_contract.rs entry.rs event.rs location.rs regenerate.rs request.rs response.rs zodiac.rs
- Dependencies of note: datom-codec, protos, rkyv 0.8, tokio, zbus, anise 0.10, hifitime 4, solar-positioning 0.5, redb 4, nexus (git rev ec097e3), dev: ethos-zero.

## 2. Ethos and Rust files

### Only .ethos file: /git/github.com/LiGoldragon/chronos/.ethos/data/chronos.ethos (full content)
```
Types
[ super:[ Latitude Longitude SolarEventKind SolarEvent EpochTaiNanos ZodiacalTime Location LocationSource ErrorMessage ] ]
[
 Request.[ GetTime GetSchedule GetLocation SetLocation.RequestSetLocation UseGeoclue Subscribe.RequestSubscribe ]
 RequestSetLocation.{ Latitude Longitude }
 RequestSubscribe.{ Vector<SolarEventKind> }
 Response.[ Acked Time.ResponseTime Schedule.ResponseSchedule Location.ResponseLocation Event.ResponseEvent Error.ResponseError ]
 ResponseTime.{ ZodiacalTime }
 ResponseSchedule.{ Vector<SolarEvent> }
 ResponseLocation.{ Location LocationSource }
 ResponseEvent.{ SolarEvent }
 ResponseError.{ ErrorMessage }
]
[]
```
(Header form is the old "Types / [ super:[...] ]" shape with the generated /git/github.com/LiGoldragon/chronos/.ethos/data/datomic_library.rs; it is not the new Library/Signal/Operation/Memory anatomy of the 984e88 proposal.)

### Rust files (one line each)
- src/lib.rs (34): module list and re-exports.
- src/bin/chronos.rs (21): CLI; embodies one Datomic value from argv, sends over UDS, prints reply.
- src/bin/chronos_daemon.rs (3): `nexus::main!(chronos::daemon::Chronos);` (entry-point branch).
- src/daemon.rs (181): the `Chronos` Nexus struct; Signaling/Operating/Remembering parts, redb LocationSource store (entry-point).
- src/client.rs (25): synchronous one-shot UDS client.
- src/wire.rs (91): u32-BE length-prefixed rkyv framing, 1 MiB cap, socket_path /run/chronos/<uid>.sock.
- src/request.rs (101): Request enum as Datomic (GetTime, GetSchedule, GetLocation, SetLocation, UseGeoclue, Subscribe).
- src/response.rs (126): Response enum (Acked, Time, Schedule, Location, Event, Error) and ErrorMessage.
- src/error.rs (42): thiserror Error and Result.
- src/location.rs (222): Latitude, Longitude (range-validated f64), Location, LocationSource; the only working domain logic.
- src/event.rs (141): SolarEvent, SolarEventKind, EpochTaiNanos for pushed subscription events.
- src/zodiac.rs (326): ZodiacSign, EclipticLongitude, ZodiacDegree, ZodiacMinute, ZodiacalTime (tropical sign projection).
- src/calendar.rs (141): AmYear, OrdinalSolarTime (equinox-anchored AM calendar).
- src/sky.rs (101): Sky, Observer, SkyState; astronomy bodies are `todo!()` stubs.
- tests/*.rs: integration tests per module (entry.rs incl. real socket Set/GetLocation).
- Status witnessed by e4b7d7 and 984e88: only SetLocation/GetLocation work; all astronomy is todo!(); no moon, nodes or nakshatras; no Chronos process or socket running.

## 3. Ownership: flows and locks

Repository owner of record: none established. 984e88 handoff: "Owners of the chronos repository: not established by this flow"; e4b7d7 (2026-10-14/15): "no current implementation/lock owner assumed". No flow currently holds a lock on /git/github.com/LiGoldragon/chronos.

### Orchestrate locks (`orchestrate 'Observe.Locks'`)
Only Chronos-path lock: 22243 ChronosTopicCanonical, holder 42265e, paths config/main-flow/metaflow/Psyche-Chronos-Primary.edn, Psyche-Chronos-Secondary.edn, and flows/504f11/continuation.json: "Align Chronos source data with the living lowercase-topic ruling". These are metaflow config, not code. No lock on the chronos repository or any chronos/signal-chronos path. (Other locks listed concern Flow, Message, Field, CriomOS; none Chronos.)

### Flows touching Chronos
- 984e88 | Psyche Chronos Secondary (Opus) | gathered the Chronos/Nexus/Ethos head-start (head-start.md, 1989 chars, held), vision/chronos.md, wrote Chronos book editions 1 and 2 (books/02-chronos.md, https://claude.ai/artifact/Fd1jGBnf2dcfkrSRShrE6w) and handoff-prototyping.md to Mind Prototyping Secondary (5b9075, secretary e4b7d7) "they build the Chronos MVP". Holds no lock, wrote nothing in the repo. Last entry: undated bullets, 2026-10-14/15 (second edition published fresh; handoff sent).
- 504f11 | Psyche chronos Secondary (this flow) | released 2026-10-16 12:59 by d68c82 to design Chronos as the golden Nexus example; deliverable a book of psyche proposals. Last entry 2026-10-16 12:59.
- e4b7d7 | Mind-side secretary to Mind Prototyping (Primary 5b9075) | read-only Chronos witness; asked Field to launch a bounded "Chronos Astra" lane; no implementation owner assumed. Last entries 2026-10-15/16 (undated bullets).
- d66c26 | Mind.{ Astra } | built the entry-point branch experiment (Chronos 68fa82c, Nexus ec097e3); unmerged; 66 tests pass per its claim. Last Chronos entry 2026-10-04.
- bad807 / 8475a9 / d4ae97 / aa887c | Fable and secretary Psyche seats | relayed the d66c26 branch claim, 2026-10-04/05. No code ownership.
- 01a04a30 | Portion-pivot realization | Chronos 0.2.0 (43703ad) migration and later "Chronos library-map correction" (M3 planned).
- 542442 | Datom codec migration | produced Chronos 0.3.0 a5cf51f (2026-09-06) and chronos-datom-542442 branch.
- da2038 | Psyche Flow Secondary | assigned the Chronos book to 984e88; logged the second edition 2026-10-15 and the Core-approved "code patterns (Chronos, ...)" 2026-10-16 awaiting packets.
- 65f93a | Psyche ethos Secondary | Ethos vision; "Chronos defaults held"; 2026-10-16 12:38.
- 23824a | Ethos Secondary predecessor | gathering file reports/ethos-nexus-chronos-psyche.md (6 Chronos records); last 2026-10-16.
- d68c82 | Psyche core Secondary (hub) | prepared Chronos metaflow 504f11 (36 modules) and approved lowercase "chronos" 2026-10-16 12:57; releases tasks.
- 23824a, 65f93a, 984e88, 058f16 (Nexus) are the neighbouring Psyche seats; no flow with aspect Mind/Prototyping has a log mentioning writes to chronos (47d946 mentions Prototyping only).
Metaflow config: /home/li/primary/config/main-flow/metaflow/Psyche-Chronos-Secondary.edn (aspect :Psyche, topic :chronos, layer :Secondary, 8 modules) and Psyche-Chronos-Primary.edn; both uncommitted-modified and locked by 42265e/22243.

## 4. How the sources name angle, apogee, watch, contextualizer

### Existing code in /git/github.com/LiGoldragon/chronos
- Angle: NO angle type. Angles are bare f64 degrees inside range-validated newtypes. src/zodiac.rs: `EclipticLongitude` strict to `[0, 360)`, normalised via `EclipticLongitude::from_unnormalized_degrees`; `ZodiacDegree`, `ZodiacMinute`. src/location.rs: `Latitude::try_new`, `Longitude::try_new`, `as_degrees`. src/sky.rs line 99-100:
  `/// Solar altitude above the local horizon, in degrees.`
  `pub solar_altitude_degrees: f64,`
  Sign naming: `ZodiacSign`, `ZodiacalTime`.
- Apogee/perigee/aphelion/nodes: ABSENT from all src, tests, ethos and *.md in the repo (grep for apogee, perigee, aphelion, node, culminat returned nothing).
- Watch: ABSENT. The existing equivalent is `Subscribe` (ethos: `RequestSubscribe.{ Vector<SolarEventKind> }`, `Response.Event`, `ResponseEvent.{ SolarEvent }`); sky.rs comment about twilight: `src/sky.rs:76: todo!("call solar_positioning twilight-at-angle / sunrise-sunset")`; AGENTS.md: "`solar-positioning` runs NREL SPA for sunrise / sunset / twilight at any solar elevation angle."
- Contextualizer: ABSENT from the Chronos repo (grep empty). The word appears only in unrelated psyche vision files (e.g. flows/d68c82/vision/context-modules.md, books.md, flows/564f55/vision/archive-ethos.md), not applied to Chronos.

### Design vocabulary (not code) in flows/984e88/books/02-chronos.md (second edition proposal, unruled)
- Angle: `Arc.Rational` (exact degrees), imported Rust type `num_rational::Rational64` through a hand-maintained vector (Proposal 4/5); `Location.{ Latitude.Arc Longitude.Arc }`; `Instant.Integer`; `Moment.{ Instant Location }`.
- Bodies, with apogee (lines 72-78):
  `Body.[ Sun  Moon  NorthNode  SouthNode  Apogee ]`
  Proposal 13 offers `Apogee` (no aphelion, default in anatomy) or default `LunarApogee` and `SolarApogee`; "the Earth's aphelion is the Sun's apogee". Handoff choice 9 nodes/apogee [true], 13 aphelion [LunarApogee, SolarApogee].
- Watch: `Watch.{ Vector<Reading> }`, `Unwatch.Subscription`, `Watching.{ Subscription ... }`, `Unwatched.Subscription`, `NoSuchWatch.Subscription`; Operation `Open.{ Vector<Reading> }`, `Close.Subscription`, `Opened`, `Watcher.{ Subscription ... }`; `Subscription.Integer` "a watch's id". Handoff choice 11: Memory [no watcher record].
- Reading: `Reading.[ Absolute.Body  Relative.{ Body Body } ]`, `Placement.{ Reading Arc }`; sign and nakshatra derived only by the `Zodiacal` trait on `Arc`; `Sign.[ Aries ... Pisces ]`, `Naksatra.[ Asvini Bharani Krttika Rohini Mrgasira Ardra ... ]`.
- Contextualizer: not named in 984e88 either.
