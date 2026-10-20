Presentation.{ «Chronos» }

# Chronos

Machine: a first edition. Chronos becomes an idiomatic Nexus with a full Ethos specification; this book proposes its psyche module and a basic anatomy for you to comment on and redesign.

## 1. Crystallization: the Chronos module

Machine: a new module; nothing is removed.

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
+ ## A simple, idiomatic Nexus
+
+ Chronos is an idiomatic Nexus with a full Ethos specification, and it stays simple.
+
+ ## The test of the Nexus
+
+ Short-term vision. Chronos is the simple component on which the Nexus architecture and Ethos are tested.
```

Every statement lands in vision-chronos.

**Archive, on approval:** the two earlier records this module replaces, each into its archive file. The tropical record stays raw; its other words are not crystallized here.

**Destroy, on approval:** an impurity, the order to start the rewrite now; this book carries it out.

## 2. Crystallization: the Ethos anatomy

Machine: Library, ordinary Signal, Operation and Memory in one file; the meta Signal in its own repository.

Machine: the Ethos of Chronos.

File: `chronos/chronos.ethos` (new)

```ethos
+ Library                        ; shared by all
+ []                             ; imports: none
+ [ Instant.Integer              ; types: Unix sec
+   Location.{ Latitude.Decimal  ;   on Earth, deg
+              Longitude.Decimal }
+   Moment.{ Instant Location }  ;   when and where
+   Body.[ Sun                   ;   a light or a
+          Moon                  ;   lunar point
+          NorthNode
+          SouthNode
+          Apogee ]
+   Sign.Integer                 ;   0 Aries .. 11
+   Naksatra.Integer             ;   0 Aśvinī .. 26
+   Position.{ Sign              ;   where it is
+              Naksatra
+              Arc.Decimal }     ;   deg into sign
+   Placement.{ Body Position }  ;   a body's place
+   Subscription.Integer         ;   a watch's id
+   Step.[ BySign                ;   what counts as
+          ByNaksatra            ;   a change
+          ByDegree ]
+   Configuration.{ Option<Location> } ] ; meta
+ []                             ; kinds
+ []                             ; associations
+
+ Signal                         ; ordinary socket
+ [ chronos:[ Moment             ; imports
+             Body
+             Placement
+             Step
+             Subscription ] ]
+ [ Tell.{ Vector<Body>          ; queries: places
+          Option<Moment> }      ;   None: now, here
+   Watch.{ Vector<Body> Step }  ;   subscribe
+   Unwatch.Subscription ]       ;   unsubscribe
+ [ Told.Vector<Placement>       ; responses
+   Watching.{ Subscription      ;   places now
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
+             Body
+             Placement
+             Step
+             Subscription
+             Configuration ] ]
+ [ Reckon.{ Vector<Body>        ; operations
+            Option<Moment> }    ;   compute places
+   Open.{ Vector<Body> Step }   ;   start a watch
+   Wake.Subscription            ;   at a crossing
+   Close.Subscription           ;   end a watch
+   Store.Configuration ]        ;   from meta
+ [ Reckoned.Vector<Placement>   ; outcomes
+   Opened.{ Subscription        ;   watch and now
+            Vector<Placement> }
+   Woke.{ Subscription          ;   the new places
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
+             Body
+             Step ] ]
+ [ Configuration                ; record types
+   Watcher.{ Subscription       ;   an open watch
+             Vector<Body>
+             Step } ]
```

Machine: the Ethos of the meta socket.

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
   +-- writes Watcher to ---> +--------+
   |                          | Memory |
   |                          +--------+
   |
   +-- answers Watching to -> +-------------+
   |                          | chronos CLI |
   |                          +-------------+
   |
   +-- sets the wake on ----> +-------+
                              | clock |
                              +-------+
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

Machine: the trace of one watch, end to end. Lands nowhere; the values are illustrative.

```datom
Watch.{ [ Sun ] BySign }        ; 1 query, CLI
Open.{ [ Sun ] BySign }         ; 2 operation
Watcher.{ 1 [ Sun ] BySign }    ; 3 to Memory
Succeeded                       ; 4 Memory's answer
Opened.{ 1                      ; 5 outcome: Libra,
  [ { Sun { 6 15 21.5 } } ] }   ;   Viśākhā, 21.5°
Watching.{ 1                    ; 6 response
  [ { Sun { 6 15 21.5 } } ] }
Wake.1                          ; 7 at the crossing
Woke.{ 1                        ; 8 outcome: Scorpio
  [ { Sun { 7 15 0.0 } } ] }
Moved.{ 1                       ; 9 response
  [ { Sun { 7 15 0.0 } } ] }
```


## 3. Choices

Machine: each choice states the shared text once, with the open words in braces; each option gives only those words. The default is marked; a choice you leave unruled lands its default.

### 3.1 The purely solar and purely lunar formats

File: `<Psyche context>/vision-chronos.md`, under Solar or lunar

```text
+ The purely solar format tells {the Sun's place}; the purely lunar format tells {the Moon's place}.
```

- a. Default: the Sun's place; the Moon's place. This is what the anatomy reckons.
- b. the solar month and its day; the lunation and its lunar day. Chronos then reckons time from the places, and the anatomy gains those types.

### 3.2 Mean or true nodes and apogee

File: `<Psyche context>/vision-chronos.md`, under Solar or lunar

```text
+ The lunar nodes and the apogee are {the true points}.
```

- a. Default: the true points.
- b. the mean points.
- c. both, the true and the mean, each its own body.

### 3.3 Where the count starts

File: `<Psyche context>/vision-chronos.md`, a new section

```text
+ ## Counting
+
+ Chronos shows {signs and nakṣatras counted from one, Aries and Aśvinī the first, and the arc as the degrees gone, from 0°}.
```

- a. Default: signs and nakṣatras counted from one, Aries and Aśvinī the first, and the arc as the degrees gone, from 0°.
- b. every count from zero, as the anatomy stores it.
- c. every count from one, the degree included: 21.5° into Libra is its twenty-second degree.

### 3.4 How a position prints

File: `<Psyche context>/vision-chronos.md`, under Counting

```text
+ A position prints {by name, the arc in degrees and minutes: Libra 21°30′, Viśākhā}.
```

- a. Default: by name, the arc in degrees and minutes: Libra 21°30′, Viśākhā.
- b. by number, the arc in decimal degrees: 7 21.5, 16.
- c. by name and number together.

### 3.5 Where the location comes from

File: `<Psyche context>/vision-chronos.md`, under Chronos tells astrological time

```text
+ The location is {the one a request carries, else the standing location set over the meta socket}.
```

- a. Default: the one a request carries, else the standing location set over the meta socket. This is what the anatomy does.
- b. only the one a request carries; the meta Configure and Configuration drop out.
- c. only the standing location; Tell carries a time and no location.

### 3.6 What Memory keeps

File: `chronos/chronos.ethos`, the Memory root

```ethos
  Memory                         ; what it keeps
  [ chronos:[ Configuration      ; imports
              Subscription
              Body
              Step ] ]
  [ Configuration                ; record types
    {records} ]
```

- a. `Watcher.{ Subscription Vector<Body> Step }`: a watch outlives a restart, as the anatomy has it.
- b. Default: nothing more, and `Watcher` with its imports is removed. A watch lives with its connection, and a restart ends both.
- c. as b, plus `Place.{ Name.String Location }`: named places kept for requests.

### 3.7 The ephemeris and its span

File: `<Psyche context>/vision-chronos.md`, a new section

```text
+ ## The ephemeris
+
+ Chronos reckons from {JPL's DE440 ephemeris, and answers for the years it covers, 1550 to 2650}.
```

- a. Default: JPL's DE440 ephemeris, and answers for the years it covers, 1550 to 2650. The Rust crate anise reads it.
- b. analytic series computed in its own code, and answers for some thousands of years around the present, less precisely.
- c. the Swiss Ephemeris, and answers for 13201 BC to 17191 AD.

### 3.8 The aphelion

File: `chronos/chronos.ethos`, the Library's Body

```ethos
  Body.[ Sun                     ;   a light or a
         Moon                    ;   lunar point
         NorthNode
         SouthNode
         {apogees} ]
```

- a. `Apogee`: no aphelion, as the anatomy has it.
- b. Default: `LunarApogee` and `SolarApogee`. Seen from the Earth on the ecliptic, the Earth's aphelion is the Sun's apogee, the Sun's place when it is farthest.
- c. as b, plus the heliocentric aphelia of the planets, which takes Chronos beyond the geocentric frame.

### 3.9 Where everything is tropical lands

File: `<Psyche context>/{modules}`

```text
+ Everything is tropical.
```

- a. Default: in vision-chronos only, as the module proposes; a wider statement waits for its own book.
- b. in vision-chronos and in spirit-core.
