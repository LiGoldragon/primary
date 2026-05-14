# 168 — Candidate verb-spines: a brainstorm

*Designer brainstorm report, 2026-05-15. Generates candidate verb-spine
designs by following each theoretical tradition surveyed in `/167` to
its natural protocol form, then combining traditions. Twenty-three
candidates from minimal (one verb) through pure-tradition (4–11
verbs) through multi-axis (the deep Sanskrit pattern). No
recommendation; the goal is to widen the design space so a chosen
spine can be evaluated against alternatives.*

**Retires when**: the workspace selects one candidate (or hybrid) and
absorbs the substance into ARCH; this report has done its job as a
generation surface.

---

## 0 · TL;DR

The literature in `/167` gives many possible verb-spines, organized
by **which axis** the spine is supposed to classify. Each candidate
below is a complete-enough sketch that we could implement it; none is
*the* answer. Six families of candidates:

| Family | Source axis | Cardinality range |
|---|---|---|
| **Process-type spines** | "what kind of act" (Halliday, Searle, Mīmāṃsā) | 1–6 |
| **Aspectual spines** | "how the act unfolds in time" (Vendler, lakāra) | 4–10 |
| **Argument-role spines** | "how the act binds to participants" (kāraka, Tesnière) | 3–6 roles |
| **Decompositional spines** | "what semantic atoms compose the verb" (Schank, NSM, Jackendoff) | 5–17 |
| **Force-dynamic spines** | "what forces interact" (Talmy) | small closed set |
| **Multi-axis spines** | several closed sets simultaneously (Pāṇinian pattern) | (product) |

Persona's current `SignalVerb` (six per `/166`'s collapse proposal) is
on the process-type axis. The brainstorm explores what else is
possible if we follow each tradition cleanly, then combine them.

**Chat-surfaced finalists** — the four candidates I'd push to the
front of any decision conversation, with full context in the chat
reply:

1. **The Halliday-loop spine** (§2.1) — six verbs arranged as
   three majors (write / read / think) plus three boundaries (stream,
   declare, observe), in a closed topological loop. Matches Persona's
   current six but gives it a *structural* organization rather than a
   flat list.
2. **The multi-axis Pāṇinian spine** (§5.1) — one closed set for
   *kinds of act* (the current `SignalVerb`), a second for
   *participant roles* (kāraka-style — six closed roles every payload
   uses), a third for *aspectual contour* (Vendler-style — four
   classes). Three orthogonal closed-set declarations per
   variant. Most ambitious.
3. **The Searle-illocutionary spine** (§2.3) — five verbs from speech
   act theory: Assert / Direct / Commit / Express / Declare.
   Lines up with workspace-internal command-and-control more
   naturally than database-op verbs do; carries the direction-of-fit
   semantics that database ops only implicitly have.
4. **The Vedānta / Mīmāṃsā minimal spine** (§7.1) — *one* verb
   (Inject) with all other distinctions carried as payload
   parameters. Maximally honest about the "all frames are
   injunctions" reading. Probably too minimal but worth comparing
   against.

The other 19 candidates are interesting in their own right and the
report develops each in enough detail to evaluate.

---

## 1 · What "deriving a spine" means

A "verb-spine" here means **a closed enum that every Signal frame
declares one variant of, plus the rule for how variants compose into
operations**. The literature gives many candidate closure cardinalities
along several orthogonal axes. Different traditions answer different
questions:

- *"What kind of act is happening?"* → process-type spines.
- *"How does the act unfold in time?"* → aspectual spines.
- *"How does the act bind to participants?"* → role spines.
- *"What semantic atoms compose the act?"* → decompositional spines.
- *"What forces interact?"* → force-dynamic spines.

A spine could pick *one* axis (today's `SignalVerb`) or *several*
(the Pāṇinian pattern of multiple orthogonal closed sets).

Each candidate below is sized to be evaluated, not implemented yet.
Cardinality, semantics, and rough mapping to today's persona-domain
operations are sketched; the full payload designs aren't. Where a
candidate clearly fails a workspace requirement (e.g., can't classify
streaming subscriptions), the report says so.

---

## 2 · Single-tradition spines

### 2.1 · The Halliday-loop spine (six process types, topologically organized)

Source: M.A.K. Halliday's *Introduction to Functional Grammar*, Ch 5
(per `/167 §4.1`). The most direct theoretical neighbour to Persona's
current six.

Six verbs in a closed loop, three majors + three boundaries:

```text
        Mutate (material)
       /                 \
      /                   \
  Subscribe              Atomic
  (behavioral —          (verbal —
   mediating              mediating
   write-and-think)       think-and-read)
      \                   /
       \                 /
        Validate (mental)
       /                 \
      /                   \
  Retract                Match
  (existential —         (relational —
   modifying being)       being/having)
      \                   /
       \                 /
        Assert (material — second pole)
```

*Or* the cleaner version:

| Position | Halliday name | Persona verb | Boundary act |
|---|---|---|---|
| Major 1 | material (doing) | `Assert` / `Mutate` / `Retract` | durable write |
| Major 2 | mental (sensing) | `Validate` | dry-run consciousness |
| Major 3 | relational (being) | `Match` | one-shot read |
| Boundary mat↔mental | behavioral | (new) `Behave` — or absorbed into `Subscribe` | physiological process-stream |
| Boundary mental↔rel | verbal | `Subscribe` | saying-into-stream |
| Boundary rel↔mat | existential | `Atomic` | declaring-into-existence |

This is six verbs with **structural organization**. The loop tells you
what's adjacent (and therefore composable) and what's diagonally
opposite (and therefore semantically distant). Halliday's claim is
that the three majors are universal; the three boundaries vary by
language. Persona's spine inherits this: the three "core" acts
(write/read/think) plus three "boundary" acts (stream/declare/observe).

**Tradeoff**: gains structural meaning over a flat list; costs
explicit topology metadata.

**Maps to current Persona spine**: 5 of 6 line up cleanly. The
remaining slot (`material`-write) has three Persona verbs (Assert,
Mutate, Retract) collapsed into it — which actually argues for
re-naming Assert/Mutate/Retract as sub-modes of one *material* verb.

### 2.2 · The Halliday-flat spine (six process types as peers)

Same six categories without the loop topology:

```
material   |   mental   |   relational   |
behavioral |   verbal   |   existential
```

Six peer verbs, no internal structure. Closer to today's flat
`SignalVerb`. Reads honestly as "six kinds of clause."

**Tradeoff**: simpler than the loop; loses Halliday's universality
claim (which depends on the loop topology to distinguish majors from
boundaries).

### 2.3 · The Searle-illocutionary spine (five forces)

Source: Searle 1975 (per `/167 §4.3`). Five verbs by direction of fit:

| Verb | Direction of fit | Persona analog | Exemplar payload |
|---|---|---|---|
| `Assert` | word-to-world | already in spine | "this record exists" |
| `Direct` | world-to-word | ≈ `Mutate` | "make X true" (command) |
| `Commit` | world-to-word | ≈ `Subscribe` | "I will keep telling you about X" |
| `Express` | null (presupposes) | (no Persona analog) | error/feedback/acknowledgment |
| `Declare` | bidirectional | ≈ `Atomic` (performative bundle) | "this is now in force" |

Five verbs. Each carries an illocutionary-force semantics richer than
"what kind of database op": each says what the *speech act between
daemons* is. Today's Persona inherits some of this implicitly (a
`Mutate` is a directive; a `Subscribe` is a commissive) but not in
its naming.

**Tradeoff**: gains principled speech-act framing; costs the
direct-database-op naming.

**Gap**: no clean analog for `Match`, `Retract`, or `Validate`.
Match-as-query is a directive ("tell me"); Retract-as-undo is a
declarative-via-reversal; Validate-as-dry-run is a hypothetical
assertive. All forced.

### 2.4 · The Pāṇini-lakāra spine (six tense-mood frames)

Source: Pāṇini's ten lakāra (per `/167 §2.1`), pruned to the
semantically distinct cases for a database protocol.

Six verbs by tense-mood:

| Lakāra | Sanskrit form | Verb | Use |
|---|---|---|---|
| `laṭ` (present indicative) | gacchati ("goes") | `State` | declarative read or write — present-tense fact |
| `loṭ` (imperative) | gaccha ("go!") | `Command` | request a state transition |
| `liṅ` (optative) | gacchet ("should go") | `Propose` | dry-run / what-if |
| `lṛṭ` (future) | gamiṣyati ("will go") | `Schedule` | commit to future delivery |
| `laṅ` (past imperfect) | agacchat ("was going") | `Retire` | close an open state |
| `lṛṅ` (conditional) | agamiṣyat ("would have gone") | `Counterfact` | hypothetical retraction |

Six verbs derived from grammatical tense-mood. The mapping is
**aspectual rather than process-shaped**: it asks not "what kind of
act" but "in what mode of time is the act being uttered."

**Tradeoff**: gains the Indo-European grammatical lineage; aspect is
first-class. Loses the action/state symmetry (everything is a verbal
act-of-uttering, even reads).

### 2.5 · The Mīmāṃsā vidhi-centric spine (one verb + parameters)

Source: Mīmāṃsā's claim (Kumārila, Prabhākara per `/167 §2.3`) that
every Vedic sentence is fundamentally an injunction (vidhi).

**One verb**: `Inject`. Everything is a kind of injection of meaning.
Variants are payload parameters:

```
Inject {
    mode: Mode,     // assertion | command | promise | dry-run | retraction
    target: Noun,   // what's being injected onto
    body: Payload,
}
enum Mode {
    Assert, Direct, Commit, Propose, Retract, Match, Subscribe, …
}
```

This is **maximally minimalist**. Pushes all structure into the
payload. The verb spine has size 1; the *mode* enum has size N.

**Tradeoff**: dramatically reduces the verb spine; gains the Mīmāṃsā
philosophical lineage; loses the per-verb match-exhaustiveness benefit
the macro-generated witness gives today (you can no longer dispatch on
verb alone).

**Probably wrong for the workspace** because the verb tag is what
makes receive-path validation cheap; collapsing to one verb defeats
this. But interesting as the *limit case* of the spine.

### 2.6 · The Vendler aspectual spine (four classes)

Source: Vendler 1957 (per `/167 §4.4`). Four verbs by aspectual contour:

| Vendler class | Verb | Persona analog | Aspect |
|---|---|---|---|
| state | `Hold` | ≈ `Subscribe` (ongoing) | atelic, durative, non-dynamic |
| activity | `Process` | ≈ `Match` (in-flight read) | atelic, durative, dynamic |
| accomplishment | `Achieve` | ≈ `Atomic` (multi-step commit) | telic, durative, dynamic |
| achievement | `Event` | ≈ `Assert`/`Mutate`/`Retract` (punctual write) | telic, punctual, dynamic |

Four verbs by aspect. Each carries a temporal-contour claim:
`Event` is what happens at a moment; `Achieve` is what happens
over a span with a goal; `Process` is what happens over a span
without a goal; `Hold` is what *is* over a span.

**Tradeoff**: aspect first-class; loses the act-kind distinction
(Assert and Retract are both `Event`).

**Could combine with another axis** for full coverage.

### 2.7 · The Schank-CD spine (eleven primitive ACTs)

Source: Schank 1972 (per `/167 §5.1`). Eleven verbs by decomposition
primitive:

| ACT | Persona analog | Database-op gloss |
|---|---|---|
| `PTRANS` | (new) physical move | record-moves-between-tables |
| `ATRANS` | ≈ `Assert`/`Mutate` | possession-changes (record-becomes-yours) |
| `MTRANS` | ≈ `Match`/`Subscribe` | information transfer between processes |
| `PROPEL` | (no analog) | force application |
| `MOVE` | (no analog) | body-part movement |
| `GRASP` | (no analog) | holding |
| `INGEST` | (no analog) | taking-in (consume a record?) |
| `EXPEL` | (no analog) | excretion |
| `MBUILD` | ≈ `Validate` | mental construction / conclusion |
| `SPEAK` | ≈ `Assert` (output) | vocal utterance |
| `ATTEND` | ≈ `Subscribe` | focusing attention |

Eleven verbs by Schank's decomposition. **Roughly seven of eleven map**
onto something Persona does (ATRANS, MTRANS, MBUILD, SPEAK, ATTEND,
plus loosely PTRANS for record-routing). Four (PROPEL, MOVE, GRASP,
INGEST, EXPEL) don't have natural daemon analogs — they're physical
verbs.

**Tradeoff**: gains the Schank decomposition lineage (the universal
AI verb-prime literature); costs the physical-body verbs that don't
fit daemons.

A workspace-bounded subset (the seven that fit) would be:
`Transfer / PossessionChange / InformationFlow / Conclude / Utter /
Focus` — six verbs derived from Schank with the bodily ones pruned.

### 2.8 · The NSM-derived spine (Wierzbicka's verbal primes, pruned)

Source: Wierzbicka NSM (per `/167 §5.2`). Seventeen verbal primes,
pruned to those that fit a daemon:

| NSM prime | Persona analog | Use |
|---|---|---|
| DO | ≈ `Mutate` / `Assert` | the action verb in general |
| HAPPEN | ≈ `Subscribe` (event stream) | the event verb |
| SAY | ≈ `Assert` (publishing) | utterance |
| THINK | ≈ `Validate` | mental construction |
| KNOW | ≈ `Match` | retrieval of known state |
| WANT | ≈ `Subscribe` (intent) | desire-for-future |
| SEE | ≈ `Match` (observe) | perception-now |
| HEAR | ≈ `Subscribe` | perception-stream |
| BE-(somewhere) | ≈ `Match` (locative) | located existence |
| THERE-IS | ≈ `Assert` (existential) | declaration of existence |

Ten verbs derived from NSM's verbal-prime subset. The mapping
suggests **DO/HAPPEN/SAY/THINK/KNOW** as a compact five-verb spine —
the action / event / utterance / consciousness / retrieval verbs.

**Tradeoff**: strongly defensible cross-linguistic universality
(NSM is the most empirically tested universal-verb claim); loses
the database-op specificity.

### 2.9 · The Aristotelian spine (action + passion)

Source: Aristotle's *Categories* (per `/167 §3.1`). Two verbs:

| Verb | Greek | Use |
|---|---|---|
| `Do` (poiein) | active form | I act on the world |
| `Undergo` (paskhein) | passive form | the world acts on me |

Two verbs. Everything else is voice / aspect / role on top.

**Tradeoff**: maximally minimal in the act-kind dimension; pushes
all complexity into payload-shape and voice.

**Probably too coarse for the workspace** — the Assert/Mutate/Retract
distinction collapses to "Do." But comparable to the Mīmāṃsā
extreme (§2.5): they're both *single-verb* spines from different
philosophical angles.

### 2.10 · The Jackendoff conceptual-primitive spine (five primitives)

Source: Jackendoff 1990 (per `/167 §5.3`). Five primitives:

| Primitive | Persona analog | Conceptual function |
|---|---|---|
| `GO` | ≈ `Subscribe` (motion through state space) | motion |
| `BE` | ≈ `Match` (state of being) | location / identity |
| `STAY` | ≈ subscription-ongoing | continuation |
| `CAUSE` | ≈ `Mutate` / `Atomic` (causal write) | causation |
| `LET` | ≈ `Validate` (permitting without forcing) | permission |

Five verbs. Each is a conceptual function over states/events.

**Tradeoff**: highly compositional; pairs well with payload-shape
classification (a payload says *what GO is moving*, etc.). Loses the
direct act-classification.

### 2.11 · The Talmy force-dynamics spine (six force patterns)

Source: Talmy 2000 (per `/167 §5.4`). Six force-dynamic patterns:

| Pattern | Persona analog | Force structure |
|---|---|---|
| `Extend` | `Assert` / `Mutate` | antagonist (caller) imposes change |
| `Block` | (no analog) | preventing change |
| `Release` | `Retract` | removing prior block |
| `Help` | `Subscribe` (continuous support) | aiding ongoing process |
| `Permit` | `Validate` | letting-be |
| `Hinder` | (no analog) | resisting change |

Six verbs in force-dynamic terms. Compactly classifies *the modal
structure* of the act (what gets pushed, blocked, allowed).

**Tradeoff**: gains modal-semantic richness; loses
ontological-act-kind framing. The six pattern-categories don't all
have daemon analogs.

### 2.12 · The Tesnière-valency spine (verbs classified by arity)

Source: Tesnière 1959 (per `/167 §4.2`). Verbs classified not by
*kind* but by *number of actants*:

| Valency | Verb | Use |
|---|---|---|
| avalent (0 actants) | `Pulse` | meta-events: heartbeat, time-tick — no real actants |
| monovalent (1 actant) | `OneActor` | unary actions on self |
| divalent (2 actants) | `BinaryOp` | typical request: subject + object |
| trivalent (3 actants) | `Triadic` | requests with three roles: caller + target + parameter |

Four verbs by arity. Most database ops are divalent (caller +
target). Some are trivalent (caller + target + recipient — like
`MessageDelivery`'s harness + sender + receiver).

**Tradeoff**: orthogonal to act-kind. The arity is **already
implicit** in payload-field count today; making it a verb axis would
surface what's already there.

**Probably better as an annotation** than as the primary spine.

---

## 3 · Two-axis combinations

Two closed sets simultaneously. Each variant declares two tags.

### 3.1 · Halliday-process × Vendler-aspect (6 × 4 = 24-cell matrix)

Each variant tagged with one process type and one aspectual class.
Most cells are empty; the populated cells are the meaningful
combinations:

|  | state | activity | accomplishment | achievement |
|---|---|---|---|---|
| material | — | (rare) | `Atomic` build | `Assert`/`Mutate`/`Retract` |
| mental | (own beliefs?) | reasoning | conclude | `Validate` |
| relational | being-stored | — | — | identifying-once |
| behavioral | (not modeled) | streaming | (rare) | (rare) |
| verbal | published | broadcasting | declare-once | `Assert`/utter |
| existential | (rare) | — | — | declare-existence |

A variant carries `(process, aspect)`. The receiver knows immediately
both *what kind of act* and *how it unfolds*.

**Tradeoff**: doubles the per-variant metadata; covers two axes
explicitly. The 24-cell matrix is sparse, which is honest (most
combinations don't occur).

### 3.2 · Searle × Vendler (5 × 4 = 20-cell matrix)

Same shape, different axes:

|  | state | activity | accomplishment | achievement |
|---|---|---|---|---|
| assertive | "X is true (ongoing)" | "X is being asserted (in progress)" | "X is asserted (completed)" | `Assert` |
| directive | (waiting on response) | "requesting X (in progress)" | "command completed" | `Mutate` request |
| commissive | "I will keep doing X" | `Subscribe` | "promise fulfilled" | "promise made" |
| expressive | (continuous mood) | "thanking continuously" | (rare) | "thanks" (event) |
| declarative | (declared state) | (rare) | `Atomic` declaration | "declared" |

Same tradeoffs as §3.1.

### 3.3 · Verb × kāraka (6 verbs × 6 roles for participants)

Source: Pāṇini's kāraka system applied to payload structure.

Six verbs (Persona's spine), and **every payload field is tagged with
one of six kāraka roles**:

| Kāraka | Sanskrit | Role | Persona analog |
|---|---|---|---|
| `kartṛ` | agent | "the doer of the action" | the originating component (often implicit) |
| `karman` | object/patient | "what is most-affected" | the typed record being asserted/mutated |
| `karaṇa` | instrument | "the means by which" | the engine/sema layer |
| `sampradāna` | recipient | "for whom" | the addressee daemon |
| `apādāna` | source | "from which" | the originator (for forwarded records) |
| `adhikaraṇa` | locus | "where/when" | the table/slot/timestamp |

Six verbs × six roles per payload = a deeply structured spine. Every
record field is tagged with its kāraka role; receivers can dispatch
on both the verb and the field's role.

**Tradeoff**: significant per-variant ceremony; gains principled
participant-role classification. The kāraka system is **one of the
most defensible cross-linguistic role inventories** in the
literature (Cardona, Kiparsky).

### 3.4 · Verb × Tesnière-valency

Same six verbs × four valencies. The valency tag classifies how many
actants the request takes:

```
SignalFrame {
    verb: SignalVerb,       // one of 6
    valency: Valency,       // 0..3
    ops: Vec<Op>,
}
enum Valency { Avalent, Monovalent, Divalent, Trivalent }
```

Most operations are divalent (caller + target). Valency lets the
type system reject malformed requests at frame-parse time.

**Tradeoff**: small ceremony; gains a typed arity check.

---

## 4 · Topological spines

Same verbs, but structurally organized.

### 4.1 · The Halliday-loop spine, formally

Source: §2.1 above, with explicit topology.

```
                  Material (write)
                 /                \
                /                  \
       Existential               Behavioral
       (declare-being)           (process-flow)
              |                          |
              |                          |
       Relational                   Mental
       (read)                      (think)
                \                  /
                 \                /
                       Verbal
                       (say)
```

Six verbs in a hexagonal closure. Each verb has two *adjacencies*
(neighbors in the loop) and three *non-adjacencies* (diagonals).
Adjacency rules can constrain what `Atomic` may bundle.

### 4.2 · The seven-planet octahedron (current spine + structure)

Source: `/162`'s planetary bijection, taken seriously as topology.

Seven verbs arranged as an octahedron (not flat). Jupiter (Atomic)
sits at one pole; the six elementary verbs sit on a hexagonal middle
band. The planets' classical astrological aspects (sextile, trine,
square, opposition) become structural relations:

- Mars (Assert) and Saturn (Retract): opposition → semantically
  opposite; can't co-occur in same Atomic
- Sun (Mutate) and Moon (Match): opposition → write vs read
- Mercury (Subscribe) and Venus (Validate): opposition → streaming
  vs dry-run
- Jupiter (Atomic): the polar point that binds them all

**Tradeoff**: gains narrative-mnemonic structure; the
adjacency/opposition rules become validatable constraints. Some
romantic; some load-bearing.

### 4.3 · The Bhartṛhari four-level speech-spine

Source: Bhartṛhari's parā/paśyantī/madhyamā/vaikharī (per `/167 §2.2`).
Verbs classified by *which level* of speech they occur at:

| Level | Verb | Use |
|---|---|---|
| `parā` (transcendent) | the unformed verb | the intent before articulation |
| `paśyantī` (intuitive) | `Propose` | a thought taking shape |
| `madhyamā` (mental/internal) | `Validate` | dry-run in the mind |
| `vaikharī` (articulated/wire) | `Assert` etc. | the spoken/sent verb |

Four levels. This isn't a competing six-verb spine — it's an
*orthogonal annotation* saying *how realized* the act is. A
`Validate` is at level madhyamā (internal); an `Assert` is at level
vaikharī (sent). Could be a stage in the wire pipeline.

**Tradeoff**: gives a typed-state-machine of the message lifecycle
(pre-propose → propose → validate → commit). Most useful for
processing pipelines, less useful for the wire itself.

---

## 5 · Multi-axis Pāṇinian spines

Following Pāṇini's three-closed-sets-simultaneously pattern.

### 5.1 · The full multi-axis spine (kinds × roles × aspect)

Three closed sets:

1. **Verb-kind** (6, Halliday-shaped): material/mental/relational/
   behavioral/verbal/existential, OR Persona's current Assert/Mutate/
   Retract/Match/Subscribe/Validate.
2. **Participant role** (6, kāraka-shaped): kartṛ/karman/karaṇa/
   sampradāna/apādāna/adhikaraṇa, per field of the payload.
3. **Aspectual contour** (4, Vendler-shaped): state/activity/
   accomplishment/achievement.

Every variant declares all three. Receivers dispatch on any combination.

```text
Op {
    verb: SignalVerb,        // 6
    aspect: AspectualContour, // 4
    payload: TypedRecord {
        fields: Vec<(KarakaRole, Value)>,
    }
}
```

**Tradeoff**: most ambitious; matches the Sanskrit tradition's pattern
of multi-axis closure. Every message is *triply* classified.
Significant macro-generation work; significant per-contract
declaration ceremony; significant gain in introspection and dispatch
power.

### 5.2 · The kāraka-only spine

Just one closed set: the six kāraka roles, applied to every payload
field. Verb-kind stays as it is (Persona's six); aspectual contour
stays implicit.

Smaller than 5.1; still gains the participant-role typing.

### 5.3 · The aspect-only spine

Just one new closed set: the four Vendler classes, applied to every
variant. Verb-kind stays; role typing stays implicit.

Smaller than 5.1; gains aspectual contour at the wire level.

---

## 6 · Hybrid sketches I find compelling

These are subjective brainstorm-favorites, not recommendations.

### 6.1 · The Halliday-loop with kāraka-typed payloads

Six verbs in the loop topology (§2.1), with payload fields tagged
kāraka-style (§3.3). Combines the strongest *act-kind* classification
in the literature (Halliday) with the strongest *role* classification
(Pāṇini). Aspect stays implicit.

```text
[Persona Frame]
└─ Op
   ├─ Verb: one of 6 Halliday-loop process types
   └─ Payload
      ├─ kartṛ-field: ...
      ├─ karman-field: ...
      ├─ karaṇa-field: ...
      ├─ sampradāna-field: ...
      ├─ apādāna-field: ...
      └─ adhikaraṇa-field: ...
```

**Tradeoff**: gains both the loop structure and the role typing;
costs the macro-generation complexity.

### 6.2 · The Searle-illocutionary spine with Vendler-aspect

Five Searle illocutionary forces with one aspectual tag each:

```text
SignalFrame {
    force: IllocutionaryForce,  // Assertive, Directive, Commissive, Expressive, Declarative
    aspect: AspectualContour,   // State, Activity, Accomplishment, Achievement
    payload: P,
}
```

Five × four = twenty cells. Each variant says **what speech act
this is** (Searle) and **how it unfolds** (Vendler). Together they
give a much richer per-frame semantics than today's spine.

**Tradeoff**: gains principled speech-act classification; costs the
direct database-op naming.

### 6.3 · The minimalist 3-verb spine (action / state / process)

A coarse partition matching the most uncontroversial divisions in
linguistic literature:

| Verb | Use | Vendler equivalent |
|---|---|---|
| `Act` | discrete, telic events (writes, retractions, validates) | achievement |
| `State` | being-a-certain-way (Match: I read your state) | state |
| `Process` | ongoing flow (Subscribe: the stream) | activity |

Three verbs. Every Persona variant fits one. Payload carries the
specifics.

**Tradeoff**: maximally compact; loses fine-grained dispatch on the
act-kind. Roughly the level Aristotle works at, or Vendler reduced
from four to three by collapsing achievement+accomplishment.

### 6.4 · The Vedānta-inspired single-verb spine

Source: §2.5 (Mīmāṃsā vidhi). One verb (`Inject`) plus a
parameter-enum for the mode.

Every frame is structurally identical. The wire shape is the
minimal possible: one verb, one record, one reply.

**Tradeoff**: extremely simple wire; pushes all complexity into the
mode-parameter. The mode-parameter then *is* the spine, just at a
different syntactic level — a verb-spine in disguise.

---

## 7 · Extreme cases

These are the limit cases that make the design space's shape
visible.

### 7.1 · One-verb minimal (Mīmāṃsā limit)

§2.5. Smallest possible spine.

### 7.2 · Two-verb minimal (Aristotelian limit)

§2.9. Do / Undergo.

### 7.3 · Multi-axis maximal (Pāṇinian full)

§5.1. Three closed sets simultaneously.

### 7.4 · Sevenfold extended (current + new)

Current six + one new for what's not covered. Candidates:

- `Stream`/`Behave` — Halliday's behavioral type, for explicitly
  ongoing physiological-style processes
- `Defer`/`Hold` — Vendler's state, for explicitly "hold this
  pending"
- `Express`/`Acknowledge` — Searle's expressive, for feedback/error
  acknowledgments
- `Negotiate` — for the channel-grant adjudication dance

Seven verbs. Picking the right seventh would require concrete
workspace pressure not yet present.

### 7.5 · Eight-verb extended

Six current + two new. E.g., `Behave` + `Express`. Eight is the
cardinality of the eight directions; matches some traditions' octave
structures.

---

## 8 · Evaluation criteria

How to choose among these candidates:

| Criterion | What to look at |
|---|---|
| **Cross-linguistic universality** | Halliday and NSM are the strongest. Spines derived from them are most defensible academically. |
| **Workspace fit** | Database-op coverage. Halliday/Searle map cleanly; Schank/NSM partially (physical-body verbs don't fit); Aristotle is too coarse. |
| **Receiver-validation enforceability** | Every spine should be `match`-exhaustive. Mīmāṃsā single-verb fails this; multi-axis spines double the surface. |
| **Composability** | Halliday's loop adjacency suggests rules for what `Atomic` may bundle. Flat spines have no such constraints. |
| **Aspectual completeness** | Vendler/lakāra-shaped spines surface aspect; process-type spines leave it implicit. |
| **Participant-role explicitness** | Kāraka-shaped role-typing makes payload fields semantically explicit. |
| **Beauty / elegance** | The Halliday loop is the most beautiful structure in the literature. Mīmāṃsā single-verb is the most minimal. Persona's current flat-six is between. |
| **Migration cost from current** | Halliday-loop is small (re-organize, no rename). Searle is medium (some renames). Schank/NSM are large (different verb-names). Multi-axis is largest (new metadata). |

The choice depends on **what Persona is trying to be**: a
database-operation protocol (favors `/166`'s collapsed-six), a
universal-act-of-language protocol (favors Halliday-loop or
Searle-illocutionary), or a deeply-typed Sanskrit-style multi-axis
declaration (favors §5.1).

---

## 9 · Summary table — twenty-three candidates

| # | Candidate | Cardinality | Source | Family |
|---|---|---:|---|---|
| 2.1 | Halliday-loop | 6 | Halliday SFL | process-type |
| 2.2 | Halliday-flat | 6 | Halliday SFL | process-type |
| 2.3 | Searle-illocutionary | 5 | Searle 1975 | process-type |
| 2.4 | Pāṇini-lakāra | 6 | Pāṇini | aspectual / mood |
| 2.5 | Mīmāṃsā-single | 1 | Mīmāṃsā | minimal |
| 2.6 | Vendler-aspectual | 4 | Vendler 1957 | aspectual |
| 2.7 | Schank-CD | 11 (or 6 pruned) | Schank 1972 | decompositional |
| 2.8 | NSM-derived | 10 (or 5 essentials) | Wierzbicka NSM | decompositional |
| 2.9 | Aristotelian | 2 | Aristotle | minimal |
| 2.10 | Jackendoff-primitives | 5 | Jackendoff 1990 | decompositional |
| 2.11 | Talmy-force-dynamic | 6 | Talmy 2000 | force-dynamic |
| 2.12 | Tesnière-valency | 4 | Tesnière 1959 | argument-role |
| 3.1 | Halliday × Vendler | 6 × 4 | combined | two-axis |
| 3.2 | Searle × Vendler | 5 × 4 | combined | two-axis |
| 3.3 | Verb × kāraka | 6 × 6 | combined | two-axis |
| 3.4 | Verb × valency | 6 × 4 | combined | two-axis |
| 4.1 | Halliday-loop formal | 6 + topology | Halliday | topological |
| 4.2 | Seven-planet octahedron | 7 + topology | `/162` astrology | topological |
| 4.3 | Bhartṛhari speech-levels | 4 levels | Bhartṛhari | topological |
| 5.1 | Full multi-axis | (6 × 6 × 4) | Pāṇini | multi-axis |
| 5.2 | Kāraka-only | 6 + roles | Pāṇini | multi-axis-partial |
| 5.3 | Aspect-only | 6 + aspect | Vendler | multi-axis-partial |
| 6.3 | Action/state/process | 3 | hybrid | minimal+ |

Twenty-three. Each is a complete spine. The design space is wide.

---

## 10 · Open questions

These are research-and-decision questions, not implementation
questions:

### Q1 — Which axis is primary?

The choice between process-type / aspectual / decompositional /
role-shaped spines is *what kind of question* the spine answers.
Persona's current spine answers "what kind of boundary act." Other
spines answer different questions. Which is what Persona's protocol
should classify?

### Q2 — One axis or several?

The Pāṇinian pattern argues for multi-axis closure. The Western
linguistic tradition usually picks one axis. Persona's current spine
is single-axis. Does the workspace benefit from multi-axis explicit
declaration, or is single-axis sufficient?

### Q3 — Loop structure or flat list?

The Halliday-loop topology gives semantic structure (adjacency,
opposition) that a flat list doesn't. Does Persona's spine benefit
from explicit topology, or is the seven-planet narrative correspondence
in `/162` enough?

### Q4 — Cross-linguistic ambitions?

Persona's spine could aim for cross-linguistic universality
(Halliday-loop, NSM-derived) or stay deliberately workspace-bounded
(database ops only). The astrological correspondence in `/162` reaches
for universality; the database-op framing stays bounded. Which?

---

## 11 · See also

- `~/primary/reports/designer/167-universal-verb-model-literature-survey.md`
  — the source for every candidate in this report. All sources cited
  there.
- `~/primary/reports/designer/166-atomic-collapses-into-frame-shape.md`
  — the pending decision on 7→6 collapse. Most candidates here
  assume the collapse; some (the seven-planet octahedron in §4.2)
  keep seven.
- `~/primary/reports/designer/162-signal-verb-roots-synthesis.md` —
  the original seven-verb synthesis. The planetary bijection there
  becomes the seven-planet octahedron (§4.2) when topology is taken
  seriously.
- `~/primary/reports/designer/163-seven-verbs-no-structure-eighth.md`
  — schema-as-data containment, still load-bearing under any of the
  candidates above.
