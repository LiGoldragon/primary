Presentation.{ «Chronos» }

# Chronos, second edition

Machine: the second edition, after your two comments on the Ethos anatomy. Coordinates and arcs take a type imported from Rust, listed in a hand-kept vector that ethos-zero links against. A position is now an absolute arc on the ecliptic; sign and nakṣatra are derived from any arc, absolute or relative. The choices on count origin and print are settled or re-posed accordingly; the rest are carried unruled.

## Crystallization

### Proposal 1: the Chronos module

Machine: a new module; nothing is removed. Changed since the first edition: the section Positions are arcs, from your comment on signs and nakṣatras.

File: `<Psyche context>/vision-chronos.md` (new)

```text
+ ---
+ description: Chronos, the Nexus that tells astrological time, is being designed or judged against what the living wants it to be.
+ dependencies: [vision-nexus, vision-ethos]
+ ---
+
+ ## Chronos tells astrological time
+
+ Chronos tells astrological time for the present moment, or for a given time and location.
+
+ ## Solar or lunar
+
+ Chronos tells the time in a purely solar or a purely lunar format, and may tell more, the lunar nodes among them.
+
+ ## Tropical, on the ecliptic
+
+ Chronos is tropical throughout, the nakṣatras included: Aśvinī begins at 0° Aries. Every position is reckoned on the ecliptic.
+
+ ## Positions are arcs
+
+ A position is an absolute arc on the ecliptic. Sign, nakṣatra and the like are derived from an arc, absolute or relative; a relative arc is one body's arc less another's. The lunation is the Moon's arc less the Sun's, and a lunation of 31° reads as Taurus.
+
+ ## A simple, idiomatic Nexus
+
+ Chronos is an idiomatic Nexus with a full Ethos specification, and it stays simple.
+
+ ## The test of the Nexus
+
+ Short-term vision. Chronos is the simple component on which the Nexus architecture and Ethos are tested.
```

Every statement lands in vision-chronos.

**Archive, on approval:** the two earlier records this module replaces, and your comment on signs and nakṣatras, each into its archive file. The tropical record stays raw; its other words are not crystallized here.

**Destroy, on approval:** an impurity, the order to start the rewrite now; this book carries it out.

Ruling:

1. Land the module, the archives and the destruction.
2. Land the module; the records stay as they are.
3. Neither.

### Proposal 2: the Ethos anatomy

Machine: Library, ordinary Signal, Operation and Memory in one file; the meta Signal in its own repository. Changed since the first edition: `Arc` is the imported `Rational` of Proposal 5, in degrees; `Location` is two arcs; `Position` and its stored sign and nakṣatra are gone; a `Reading` asks for a body's absolute arc or one body's arc relative to another; `Sign` and `Naksatra` are named enums, yielded only by the `Zodiacal` trait on `Arc`.

Machine: the Ethos of Chronos.

File: `chronos/chronos.ethos` (new)

```ethos
+ Library                        ; shared by all
+ []                             ; imports: none
+ [ Instant.Integer              ; types: Unix sec
+   Arc.Rational                 ;   degrees, exact
+   Location.{ Latitude.Arc      ;   on Earth
+              Longitude.Arc }
+   Moment.{ Instant Location }  ;   when and where
+   Body.[ Sun                   ;   a light or a
+          Moon                  ;   lunar point
+          NorthNode
+          SouthNode
+          Apogee ]
+   Reading.[ Absolute.Body      ;   what is asked:
+             Relative.{ Body    ;   second's arc
+                        Body } ] ; less first's
+   Placement.{ Reading Arc }    ;   a reading's arc
+   Sign.[ Aries                 ;   derived, never
+          Taurus                ;   stored or
+          Gemini                ;   answered
+          Cancer
+          Leo
+          Virgo
+          Libra
+          Scorpio
+          Sagittarius
+          Capricorn
+          Aquarius
+          Pisces ]
+   Naksatra.[ Asvini            ;   derived: the 27
+              Bharani           ;   from 0° Aries
+              Krttika
+              Rohini
+              Mrgasira
+              Ardra
+              Punarvasu
+              Pusya
+              Aslesa
+              Magha
+              PurvaPhalguni
+              UttaraPhalguni
+              Hasta
+              Citra
+              Svati
+              Visakha
+              Anuradha
+              Jyestha
+              Mula
+              PurvaAsadha
+              UttaraAsadha
+              Sravana
+              Dhanistha
+              Satabhisaj
+              PurvaBhadrapada
+              UttaraBhadrapada
+              Revati ]
+   InSign.{ Sign Arc }          ;   arc gone in
+   InNaksatra.{ Naksatra Arc }
+   Subscription.Integer         ;   a watch's id
+   Step.[ BySign                ;   what counts as
+          ByNaksatra            ;   a change
+          ByDegree ]
+   Configuration.{ Option<Location> } ] ; meta
+ [ Zodiacal.[ sign.[ InSign ]   ; kinds: derived
+              naksatra.[ InNaksatra ] ] ]
+ [ Arc.[ Zodiacal ] ]           ; associations
+
+ Signal                         ; ordinary socket
+ [ chronos:[ Moment             ; imports
+             Reading
+             Placement
+             Step
+             Subscription ] ]
+ [ Tell.{ Vector<Reading>       ; queries: arcs
+          Option<Moment> }      ;   None: now, here
+   Watch.{ Vector<Reading>      ;   subscribe
+           Step }
+   Unwatch.Subscription ]       ;   unsubscribe
+ [ Told.Vector<Placement>       ; responses
+   Watching.{ Subscription      ;   arcs now
+              Vector<Placement> }
+   Moved.{ Subscription         ;   at each step
+           Vector<Placement> }
+   Unwatched.Subscription
+   Refused.[ NoLocation         ;   typed refusals
+             BeyondEphemeris.Instant
+             NoSuchWatch.Subscription ] ]
+ []                             ; types
+
+ Operation                      ; one per effect
+ [ chronos:[ Moment             ; imports
+             Reading
+             Placement
+             Step
+             Subscription
+             Configuration ] ]
+ [ Reckon.{ Vector<Reading>     ; operations
+            Option<Moment> }    ;   compute arcs
+   Open.{ Vector<Reading>       ;   start a watch
+          Step }
+   Wake.Subscription            ;   at a crossing
+   Close.Subscription           ;   end a watch
+   Store.Configuration ]        ;   from meta
+ [ Reckoned.Vector<Placement>   ; outcomes
+   Opened.{ Subscription        ;   watch and now
+            Vector<Placement> }
+   Woke.{ Subscription          ;   the new arcs
+          Vector<Placement> }
+   Closed.Subscription
+   Stored.Configuration
+   Failed.[ NoLocation          ;   each refusal
+            BeyondEphemeris.Instant
+            NoSuchWatch.Subscription
+            StoreRefused ] ]
+ []                             ; types
+
+ Memory                         ; what it keeps
+ [ chronos:[ Configuration      ; imports
+             Subscription
+             Reading
+             Step ] ]
+ [ Configuration                ; record types
+   Watcher.{ Subscription       ;   an open watch
+             Vector<Reading>
+             Step } ]
```

Machine: `Rational` needs no import line; it is known from the vector of Proposal 4, as a built-in is. A relative arc is reduced to 0° up to 360°, so the Sun at 350° and the Moon at 21° make a lunation of 31°. `Zodiacal` is a Chronos trait borne by a Rust type from another crate, which Rust allows because the trait is Chronos's own. Sign and nakṣatra are taken the same way on an absolute and a relative arc.

Machine: the Ethos of the meta socket, unchanged.

File: `meta-signal-chronos/meta-signal-chronos.ethos` (new)

```ethos
+ Signal                         ; meta socket
+ [ chronos:[ Location           ; imports
+             Configuration ] ]
+ [ Configure.Configuration ]    ; queries
+ [ Configured.Configuration     ; responses
+   Refused.[ OutOfRange.Location ] ] ; refusal
+ []                             ; types
```

Machine: the trait as the generator would write it.

```rust
pub trait Zodiacal {
    fn sign(&self) -> InSign;
    fn naksatra(&self) -> InNaksatra;
}
```

Machine: how one relative arc yields its derivations.

```text
+---------------------------+
| Moon at 151°, Sun at 120° |
+---------------------------+
              |
              | subtracts into
              v
     +-------------------+
     | lunation arc, 31° |
     +-------------------+
              |
     +--------+--------+
     | reads as        | reads as
     | sign            | nakṣatra
     v                 v
+------------+  +----------------+
| Taurus, 1° |  | Kṛttikā, 4°20′ |
+------------+  +----------------+
```

Machine: `Wake` is the operation the Nexus gives itself at the next crossing it has reckoned; nothing polls, and between crossings Chronos is quiet.

```text
     +-------------+
     | chronos CLI |
     +-------------+
            |
            | sends Watch to
            v
       +---------+
       | Chronos |
       +---------+
            |
  +---------+---------------+
  | writes  | answers       | sets the
  | Watcher | Watching to   | wake on
  v         v               v
+--------+ +-------------+ +-------+
| Memory | | chronos CLI | | clock |
+--------+ +-------------+ +-------+
                              |
                              | wakes
                              v
                         +---------+
                         | Chronos |
                         +---------+
                              |
                              | sends Moved to
                              v
                       +-------------+
                       | chronos CLI |
                       +-------------+
```

Machine: the trace of one watch on the lunation, end to end, its arcs written as in option 1 of Proposal 6. Lands nowhere; the values are illustrative.

```datom
Watch.{ [ Relative.{ Sun Moon } ] ; 1 query, CLI
        BySign }
Open.{ [ Relative.{ Sun Moon } ]  ; 2 operation
       BySign }
Watcher.{ 1                       ; 3 to Memory
          [ Relative.{ Sun Moon } ]
          BySign }
Succeeded                         ; 4 Memory answers
Opened.{ 1                        ; 5 outcome: 31°,
  [ { Relative.{ Sun Moon } 31 } ] } ; Taurus
Watching.{ 1                      ; 6 response
  [ { Relative.{ Sun Moon } 31 } ] }
Wake.1                            ; 7 at crossing
Woke.{ 1                          ; 8 outcome: 60°,
  [ { Relative.{ Sun Moon } 60 } ] } ; Gemini
Moved.{ 1                         ; 9 response
  [ { Relative.{ Sun Moon } 60 } ] }
```

Ruling:

1. Land the anatomy as shown, the choices below filling its open places.
2. Neither; it is redesigned.

### Proposal 3: types imported from Rust

Machine: two paragraphs added to vision-ethos, after the intrinsic names; nothing is removed.

File: `<Psyche context>/vision-ethos.md`, under Imports

```text
  An import names a source and a type: `protos:String` or
  `protos:[ String Integer ]`. An explicit import and an intrinsic name
  mean the same thing. Intrinsic names known without import: String,
  Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.
+
+ Types taken directly from Rust are listed in a vector, specified and kept by hand; the Ethos-to-Rust compiler reads it to know what each links to. A listed type is known without import, as a built-in is.
+
+ In time, the feedback on code says where each type comes from.
```

Both statements land in vision-ethos.

**Archive, on approval:** your comment on fraction and angle types, into its archive file.

Ruling:

1. Land both paragraphs and the archive.
2. Land the first paragraph only.
3. Neither.

### Proposal 4: the import vector's shape

Machine: a proposal for the vector itself, in ethos-zero's repository; it lands no vision. Each entry names the type as Ethos reads it, the Rust path the generator writes, and the rkyv adapter for it. None of the candidates in Proposal 5 archives with rkyv, and every generated type derives the rkyv archive, Eq and Hash; so the generator writes the adapter on each field of an imported type, and the adapters live in a small crate of their own, since the Nexus compiles without datom-codec; the datom impl of an imported type is hand-written beside the intrinsics in datom-codec. The crate the path names is a dependency in the generated crate's manifest, never versioned in the vector.

File: `ethos-zero/ethos-zero.ethos`, its Library

```ethos
+ [ Import.{ Name.String         ; types: as read
+            Path.String         ;   Rust path
+            Adapter.String } ]  ;   rkyv adapter
```

File: `ethos-zero/imports.datom` (new)

```datom
+ [ { Rational                   ; the vector of
+     «num_rational::Rational64» ;   Proposal 5's
+     «ethos_imports::Ratio» } ] ;   default
```

Ruling:

1. Land the shape and the file: ethos-zero reads the vector when it is built.
2. Land the shape; the vector is a constant in ethos-zero's code instead of a file.
3. Neither; the shape is redesigned.

## Choices

Machine: each choice states the shared text once, with the open words in braces; each option gives only those words. The default is marked; a choice you leave unruled lands its default. Of the first edition's choices, where the count starts is gone: signs and nakṣatras are named, and an arc is degrees gone from 0°. How a position prints is re-posed as Proposal 6.

### Proposal 5: the imported angle type

Machine: no crate Chronos depends on, anise, hifitime or solar-positioning, has an angle type; anise and solar-positioning carry angles as bare floating-point degrees, which bear neither Eq nor Hash. The options are the crates found that do; each takes its own adapter.

File: `ethos-zero/imports.datom`

```text
+ [ { {name} {path} {adapter} } ]
```

Ruling:

1. Default: `Rational`, `«num_rational::Rational64»`. num-rational 0.4.2, already in Chronos's lock: an exact fraction, here of degrees, bearing Eq and Hash; a float from the ephemeris is rounded into it once.
2. `Angle`, `«turns::Angle64»`. turns 0.1.2: an angle as a wrapping unsigned integer, one full range one turn, bearing Eq and Hash; very new and little used, and latitude is read off a full circle.
3. `PlaneAngle`, uom 0.38.0's plane angle over its rational storage: an angle with its unit in the type; the heaviest of the three.
4. None; `Decimal` stays, and no vector is kept yet.

### Proposal 6: how an arc is written

Machine: the datom of the imported type, hand-written in datom-codec; shown for 21°30′ into the lunation.

File: `datom-codec`, the datom of `Rational`

```text
+ Told.[ { Relative.{ Sun Moon } {arc} } ]
```

Ruling:

1. Default: `43/2`: a bare fraction of degrees, a whole number when whole.
2. `{ 43 2 }`: numerator and denominator as a struct.
3. `21°30′`: bare degrees, minutes and seconds, the seconds shown when not zero.

### Proposal 7: how a derivation is reached

File: `<Psyche context>/vision-chronos.md`, under Positions are arcs

```text
+ A derivation is reached {by the trait methods of the Library, which any client calls on an arc it holds}.
```

Ruling:

1. Default: by the trait methods of the Library, which any client calls on an arc it holds. Chronos answers arcs only.
2. by the trait methods, and by a request carrying an arc and what to derive, `Derive.{ Arc Derivation.[ ToSign ToNaksatra ] }` answered `Derived.[ InSign InNaksatra ]`.

### Proposal 8: the purely solar and purely lunar formats

Machine: re-posed for arcs. The lunar day is the lunation in twelfths of 12°, a derivation like the sign.

File: `<Psyche context>/vision-chronos.md`, under Solar or lunar

```text
+ The purely solar format tells {the Sun's arc}; the purely lunar format tells {the lunation, the Moon's arc less the Sun's}.
```

Ruling:

1. Default: the Sun's arc; the lunation, the Moon's arc less the Sun's.
2. the Sun's arc; the Moon's arc.
3. the solar month and its day; the lunation and its lunar day. Chronos then derives time from the arcs, and the Library gains those derivations.

### Proposal 9: mean or true nodes and apogee

File: `<Psyche context>/vision-chronos.md`, under Solar or lunar

```text
+ The lunar nodes and the apogee are {the true points}.
```

Ruling:

1. Default: the true points.
2. the mean points.
3. both, the true and the mean, each its own body.

### Proposal 10: where the location comes from

File: `<Psyche context>/vision-chronos.md`, under Chronos tells astrological time

```text
+ The location is {the one a request carries, else the standing location set over the meta socket}.
```

Ruling:

1. Default: the one a request carries, else the standing location set over the meta socket. This is what the anatomy does.
2. only the one a request carries; the meta Configure and Configuration drop out.
3. only the standing location; Tell carries a time and no location.

### Proposal 11: what Memory keeps

File: `chronos/chronos.ethos`, the Memory root

```ethos
  Memory                         ; what it keeps
  [ chronos:[ Configuration      ; imports
              Subscription
              Reading
              Step ] ]
  [ Configuration                ; record types
    {records} ]
```

Ruling:

1. `Watcher.{ Subscription Vector<Reading> Step }`: a watch outlives a restart, as the anatomy has it.
2. Default: nothing more, and `Watcher` with its imports is removed. A watch lives with its connection, and a restart ends both.
3. as 2, plus `Place.{ Name.String Location }`: named places kept for requests.

### Proposal 12: the ephemeris and its span

File: `<Psyche context>/vision-chronos.md`, a new section

```text
+ ## The ephemeris
+
+ Chronos reckons from {JPL's DE440 ephemeris, and answers for the years it covers, 1550 to 2650}.
```

Ruling:

1. Default: JPL's DE440 ephemeris, and answers for the years it covers, 1550 to 2650. The Rust crate anise reads it.
2. analytic series computed in its own code, and answers for some thousands of years around the present, less precisely.
3. the Swiss Ephemeris, and answers for 13201 BC to 17191 AD.

### Proposal 13: the aphelion

File: `chronos/chronos.ethos`, the Library's Body

```ethos
  Body.[ Sun                     ;   a light or a
         Moon                    ;   lunar point
         NorthNode
         SouthNode
         {apogees} ]
```

Ruling:

1. `Apogee`: no aphelion, as the anatomy has it.
2. Default: `LunarApogee` and `SolarApogee`. Seen from the Earth on the ecliptic, the Earth's aphelion is the Sun's apogee, the Sun's place when it is farthest.
3. as 2, plus the heliocentric aphelia of the planets, which takes Chronos beyond the geocentric frame.

### Proposal 14: where everything is tropical lands

File: `<Psyche context>/{modules}`

```text
+ Everything is tropical.
```

Ruling:

1. Default: in vision-chronos only, as the module proposes; a wider statement waits for its own book.
2. in vision-chronos and in spirit-core.
