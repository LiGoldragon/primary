# 169 — Candidate verb-spines in Rust pseudo-code

*Designer companion to `/168`, 2026-05-15. Translates all 23 candidate
verb-spines into concrete Rust pseudo-code with Sanskrit terms glossed
in parentheses (multiple English translations included where no single
word captures the term). Each candidate gives: the `SignalVerb` (or
equivalent) enum, a sample `signal_channel!` invocation showing how a
contract would declare its variants, and a sample wire frame in NOTA
syntax for at least one variant. This is the "what would I be
implementing" companion to `/168`'s brainstorm.*

**Retires when**: `/168` does (this is its concrete companion).

---

## 0 · How to read this report

Each candidate has the same three blocks:

1. **The verb enum** — the closed set, with one-line gloss per
   variant. Sanskrit terms always carry parenthetical translations.
2. **A signal_channel! sketch** — what a contract declaration looks
   like under this spine.
3. **One or two wire frames** in NOTA — what a human or agent would
   type to construct a request.

Sanskrit term conventions: `(term: translation1; translation2;
shade-of-meaning)`. Multiple translations are given when no single
English word captures the term — that's the user's request and the
honest way to render the philosophical vocabulary.

Code is **pseudo-code**, not currently compilable. The actual
`signal_channel!` macro (per `signal-core/src/channel.rs`) doesn't
yet support some of these shapes (kāraka role typing, multi-axis
declarations); they're sketched as what the macro *could* look like.

---

## 1 · Process-type spines (the "what kind of act" axis)

### 1.1 · Halliday-loop spine (six process types, topologically organized)

```rust
/// Six process types from M.A.K. Halliday's Systemic Functional Linguistics.
/// Three majors (corners of the triangle) + three boundaries (edges between).
/// Closed loop, not flat list.
pub enum SignalVerb {
    /// Major: outer-world doing — energy bringing about change.
    /// Exemplars in English: do, make, fall, create, destroy.
    Material,

    /// Major: inner consciousness — sensing, thinking, wanting.
    /// Exemplars: know, want, fear, believe, suppose.
    Mental,

    /// Major: abstract being or having — characterization, identity.
    /// Exemplars: be, have, seem, become, belong to.
    Relational,

    /// Boundary between Material and Mental: outer manifestation of
    /// inner state — physiological-psychological behavior.
    /// Exemplars: laugh, breathe, smile, sleep, dream.
    Behavioral,

    /// Boundary between Mental and Relational: saying — symbolic
    /// relations constructed in consciousness, enacted through language.
    /// Exemplars: say, tell, ask, reply.
    Verbal,

    /// Boundary between Relational and Material: simple existence —
    /// "there is", "it happens".
    /// Exemplars: be, exist, occur, happen.
    Existential,
}

// Adjacency constraint encoded by the loop:
impl SignalVerb {
    /// Returns the two verbs adjacent to this one in the loop topology.
    /// Atomic bundles of *adjacent* verbs are semantically clean;
    /// bundles of *diagonally-opposite* verbs are suspicious.
    pub fn adjacents(&self) -> (Self, Self) {
        match self {
            Self::Material =>    (Self::Behavioral, Self::Existential),
            Self::Behavioral =>  (Self::Material, Self::Mental),
            Self::Mental =>      (Self::Behavioral, Self::Verbal),
            Self::Verbal =>      (Self::Mental, Self::Relational),
            Self::Relational =>  (Self::Verbal, Self::Existential),
            Self::Existential => (Self::Relational, Self::Material),
        }
    }
}
```

Contract using it:

```rust
signal_channel! {
    request MindRequest {
        Material  SubmitThought(SubmitThought),   // writing a new thought
        Mental    ValidateProposal(ProposalCheck), // inner check
        Relational QueryThoughts(QueryThoughts),   // reading what is
        Behavioral StreamActivity(ActivityFilter), // ongoing observation
        Verbal    AnnounceClaim(RoleClaim),         // saying-into-record
        Existential AssertExistence(NewEntity),     // declaring existence
    }
    reply MindReply { /* ... */ }
}
```

Wire frame:

```sh
mind '(Material (SubmitThought (title "draft idea") (body "...")))'
mind '(Relational (QueryThoughts (kind ByStatus) (limit 100)))'
```

---

### 1.2 · Halliday-flat spine (six process types as peers, no topology)

Same enum as §1.1; drop the `adjacents()` method and the loop
constraint. Six peer verbs, no internal structure.

(Wire frames identical to §1.1.)

---

### 1.3 · Searle-illocutionary spine (five speech-act forces)

```rust
/// Five illocutionary forces from John Searle's *A Taxonomy of
/// Illocutionary Acts* (1975). Each carries a direction-of-fit
/// (word-to-world, world-to-word, both, or neither).
pub enum SignalVerb {
    /// Word-to-world: "this is the case."
    /// Direction: the words conform to how the world is.
    /// Psychological state: belief.
    /// Exemplars: state, claim, deny, predict, report, describe.
    Assertive,

    /// World-to-word: "make this be the case."
    /// Direction: the world should change to fit the words.
    /// Psychological state: want.
    /// Exemplars: request, command, ask, advise, suggest.
    Directive,

    /// World-to-word: "I commit myself to make this be the case."
    /// Direction: the world will change to fit the words (by speaker's act).
    /// Psychological state: intention.
    /// Exemplars: promise, vow, threaten, pledge, offer.
    Commissive,

    /// Null fit (presupposes truth of content; expresses attitude).
    /// Psychological state: various (regret, joy, gratitude, etc.).
    /// Exemplars: thank, apologize, congratulate, condole.
    Expressive,

    /// Both directions (bringing about correspondence by mere utterance).
    /// Psychological state: none required.
    /// Exemplars: "I pronounce you...", "you're fired", "I christen this..."
    Declaration,
}
```

Contract:

```rust
signal_channel! {
    request MindRequest {
        Assertive   PublishThought(Thought),       // word-to-world: stating
        Directive   RequestStateChange(StatusChange), // world-to-word: command
        Commissive  PromiseStream(SubscribeSpec),   // world-to-word by self-commit
        Expressive  AcknowledgeReceipt(Receipt),    // null-fit: feedback
        Declaration EngineLaunch(EngineSpec),       // both: performative creation
    }
}
```

Wire frame:

```sh
mind '(Assertive (PublishThought (...)))'
mind '(Directive (RequestStateChange (item id-42) (status Closed)))'
```

---

### 1.4 · Mīmāṃsā vidhi-centric spine (one verb + mode parameter)

The Mīmāṃsā philosophical school (Kumārila, Prabhākara, c. 6th–8th
c. CE) argued every Vedic sentence is fundamentally an injunction
(`vidhi`: injunction; cosmic-prescription; ought; command-with-
ritual-binding-force). The prototypical verb-form is `yajeta`
("one should sacrifice" — optative + reflexive, the canonical
vidhi shape).

```rust
/// Single verb following Mīmāṃsā's claim that every utterance is
/// fundamentally an injunction.
pub enum SignalVerb {
    /// (vidhi: injunction; command; cosmic-prescription; ought-utterance)
    /// Every Signal frame is an injection of meaning. The *kind* of
    /// injection — assertive, directive, retractive — lives in the mode
    /// parameter of the payload, not in a verb-tag.
    Inject,
}

pub struct InjectOp<Payload> {
    pub mode: InjectionMode,
    pub payload: Payload,
}

pub enum InjectionMode {
    Assert,       // declarative injection
    Direct,       // commanding injection
    Commit,       // promissory injection
    Retract,      // reversing injection
    Match,        // querying injection
    Subscribe,    // ongoing injection
    Validate,     // dry-run injection
}
```

Contract:

```rust
signal_channel! {
    request MindRequest {
        Inject SubmitThought(InjectOp<SubmitThought>),   // mode chosen at payload
        Inject QueryThoughts(InjectOp<QueryThoughts>),
        Inject RoleClaim(InjectOp<RoleClaim>),
        // ... every variant is Inject; mode in payload
    }
}
```

Wire frame:

```sh
mind '(Inject (mode Assert) (SubmitThought (...)))'
mind '(Inject (mode Match) (QueryThoughts (...)))'
```

Practical note: this collapses the verb dispatch entirely; mode-tags
take its place. Receiver-side verb validation per `/166` becomes
mode-validation. Mostly relabeling, not real structural change — but
philosophically committed to one fundamental utterance type.

---

## 2 · Aspectual spines (the "how the act unfolds in time" axis)

### 2.1 · Pāṇini lakāra spine (six tense/mood frames)

The Pāṇinian `lakāra` system (Sanskrit's ten tense/mood markers,
named after the abstract affix-letters `la-T`, `li-T`, etc., that
trigger them) classifies every verb by *the temporal-modal frame
of its uttering*. Pruning the ten down to the semantically distinct
six for a protocol use:

```rust
/// Six verbs derived from Pāṇini's lakāra (tense/mood) system.
/// Each lakāra is named after a Sanskrit affix-letter; the gloss
/// names the temporal-modal frame.
pub enum SignalVerb {
    /// (laṭ: "now-tense"; present-indicative; "happens-now")
    /// A declarative claim about present state.
    State,

    /// (loṭ: "imperative"; "do-it!"; command-form)
    /// A request that a state-transition happen.
    Command,

    /// (liṅ: "optative"; "should-tense"; "may-it-be-tense"; benedictive)
    /// A dry-run or wishful proposal.
    Propose,

    /// (lṛṭ: "future-tense"; "will"; "will-be")
    /// A commitment to a future stream of events.
    Schedule,

    /// (laṅ: "imperfect-past-tense"; "was-doing"; "had-been")
    /// A retraction — closing what was open.
    Retire,

    /// (lṛṅ: "conditional-tense"; "if-then"; "would-have-been")
    /// A hypothetical retraction — what would have followed had X.
    Counterfact,
}
```

(Three lakāras of the original ten don't get verb slots: `liṭ` —
witnessed-past-perfect — folds into `Retire`; `luṭ` —
periphrastic-future — folds into `Schedule`; `leṭ` — Vedic
subjunctive, lost in classical Sanskrit anyway — folds into
`Propose`; `luṅ` — aorist / "indefinite-past" — folds into
`Retire`.)

Contract:

```rust
signal_channel! {
    request MindRequest {
        State    PublishThought(Thought),          // present indicative: now-true
        Command  AssignRole(RoleAssignment),       // imperative: make-it-so
        Propose  ValidateGrant(GrantProposal),     // optative: should-this-work
        Schedule SubscribeStream(Subscription),    // future: will-deliver
        Retire   CloseClaim(ClaimRetraction),      // past-imperfect: was-open
        Counterfact RevertIf(ConditionalUndo),     // conditional: had-it-been-X
    }
}
```

Wire frame:

```sh
mind '(State (PublishThought (...)))'
mind '(Command (AssignRole (role Operator) (target user-42)))'
```

---

### 2.2 · Vendler aspectual spine (four aspectual classes)

```rust
/// Four aspectual classes from Zeno Vendler's *Verbs and Times* (1957).
/// Each class names how the event unfolds in time.
pub enum SignalVerb {
    /// Atelic, durative, non-dynamic. No goal-point, no end-point,
    /// no internal phases.
    /// Exemplars in English: know, love, own, be-tall.
    State,

    /// Atelic, durative, dynamic. Has phases but no goal-point.
    /// Exemplars: run, walk, push, swim.
    Activity,

    /// Telic, durative, dynamic. Has phases AND a goal-point.
    /// Exemplars: build-a-house, draw-a-circle, write-a-letter.
    Accomplishment,

    /// Telic, punctual, dynamic. Goal-point with no duration.
    /// Exemplars: recognize, find, arrive, die, win.
    Achievement,
}
```

Contract:

```rust
signal_channel! {
    request MindRequest {
        State          HoldRole(RoleClaim),           // ongoing being-claimed
        Activity       StreamThoughts(SubscribeSpec), // ongoing flow
        Accomplishment AtomicHandoff(HandoffPlan),    // multi-step toward goal
        Achievement    AssertThought(Thought),        // punctual write
        Achievement    RetractClaim(RoleRelease),     // punctual close
    }
}
```

Wire frame:

```sh
mind '(Achievement (AssertThought (...)))'
mind '(Activity (StreamThoughts (filter ...)))'
```

Note that this groups across what today are different verbs —
`Assert`/`Mutate`/`Retract` all fall under `Achievement`. Different
axis of classification.

---

## 3 · Argument-role spines (the "how it binds to participants" axis)

### 3.1 · Pāṇini kāraka spine (six syntactic-semantic roles)

The Pāṇinian `kāraka` system (case-relations; participant-functions;
roles-around-the-verb) is not really a *verb* spine — it's a
*payload-field* spine. Six roles tag every argument the verb takes.

```rust
/// Six kāraka roles from Pāṇini's Aṣṭādhyāyī (sūtras 1.4.23–1.4.51).
/// Each role names the semantic relation of a participant to the
/// verb (kriyā: action; verb-act; what-is-being-done).
pub enum KarakaRole {
    /// (kartṛ: agent; doer; the-one-who-does)
    /// The active source of the action.
    /// Default case (vibhakti): nominative.
    Agent,

    /// (karman: object; patient; what-is-most-affected; the-undergoer)
    /// What the action most-affects.
    /// Default case: accusative.
    Patient,

    /// (karaṇa: instrument; means; by-which; tool-or-method)
    /// The means by which the action is performed.
    /// Default case: instrumental.
    Instrument,

    /// (sampradāna: recipient; beneficiary; for-whose-sake; addressee)
    /// The one for whom the action is done.
    /// Default case: dative.
    Recipient,

    /// (apādāna: source; that-from-which; point-of-departure;
    /// origin-of-separation)
    /// That from which something separates or originates.
    /// Default case: ablative.
    Source,

    /// (adhikaraṇa: locus; substrate; place-or-time-of-action;
    /// "where/when")
    /// The place, time, or context in which the action occurs.
    /// Default case: locative.
    Locus,
}
```

Used as a payload-field annotation:

```rust
pub struct SignalRecord<Payload> {
    pub fields: Vec<(KarakaRole, Payload)>,
}

// Or, more typically, as field-level tagging on a record:
pub struct MessageDelivery {
    #[karaka(Agent)]   pub sender: ComponentName,
    #[karaka(Patient)] pub message: MessageBody,
    #[karaka(Recipient)] pub harness: HarnessName,
    #[karaka(Locus)]   pub message_slot: MessageSlot,
}
```

Contract using kāraka-typed payloads alongside Persona's current six
verbs:

```rust
signal_channel! {
    request HarnessRequest {
        Assert MessageDelivery(MessageDelivery),  // payload uses #[karaka(...)]
        Retract DeliveryCancellation(DeliveryCancellation),
        Match HarnessStatusQuery(HarnessStatusQuery),
    }
}
```

This isn't a competing verb-spine; it's a typed-payload-field
annotation system that could live *alongside* any of the verb-spine
candidates.

---

### 3.2 · Tesnière-valency spine (four verbs by argument arity)

```rust
/// Four verbs from Tesnière's *Elements of Structural Syntax* (1959),
/// classified by the number of obligatory actants (arguments) the
/// verb requires.
pub enum SignalVerb {
    /// Zero actants. Meteorological-style events with no participants.
    /// Tesnière's example: Latin "Pluit" ("it rains") — the process
    /// itself, no participants. Persona analog: heartbeat, tick.
    Avalent,

    /// One actant. Unary actions.
    /// Example: "Alfred falls" — one entity, the faller.
    Monovalent,

    /// Two actants. Subject + object.
    /// Example: "Alfred hits Bernard" — agent + patient.
    Divalent,

    /// Three actants. Subject + object + indirect object.
    /// Example: "Alfred gives the book to Charles" — giver + thing + recipient.
    Trivalent,
}

/// Plus five voice transformations (Tesnière's "diatheses") that any
/// verb can take without changing its valency:
pub enum Diathesis {
    Active,      // Alfred loves Bernard
    Passive,     // Bernard is loved by Alfred
    Reflexive,   // Alfred loves himself
    Reciprocal,  // Alfred and Bernard love each other
    Causative,   // Alfred makes Bernard love Charles
}
```

This too is more annotation than spine: most database operations are
divalent (caller + target), some trivalent (caller + target +
parameter). The arity is **already implicit** in payload-field
count today.

---

## 4 · Decompositional spines (the "what semantic atoms compose the verb" axis)

### 4.1 · Schank Conceptual-Dependency spine (eleven primitive ACTs)

```rust
/// Eleven primitive ACTs from Roger Schank's Conceptual Dependency
/// theory (1972, 1975). Claim: any verb in any language decomposes
/// to a combination of these.
pub enum SignalVerb {
    /// Physical transfer of an object's location.
    /// English exemplars: go, send, deliver, ship.
    PTrans,

    /// Abstract transfer of possession or relationship.
    /// English exemplars: give, take, sell, buy.
    ATrans,

    /// Mental transfer of information.
    /// English exemplars: tell, hear, read, listen.
    MTrans,

    /// Application of physical force to an object.
    /// English exemplars: push, kick, throw, hit.
    Propel,

    /// Movement of a body part by its owner.
    /// English exemplars: raise-hand, kick-foot.
    Move,

    /// Grasping of an object by an actor.
    /// English exemplars: hold, clutch, grab.
    Grasp,

    /// Taking into the body.
    /// English exemplars: eat, drink, breathe-in.
    Ingest,

    /// Expelling from the body.
    /// English exemplars: spit, cry, vomit.
    Expel,

    /// Mental construction or conclusion.
    /// English exemplars: think, conclude, decide.
    MBuild,

    /// Producing vocal sound.
    /// English exemplars: say, shout, whisper.
    Speak,

    /// Focusing a sense organ.
    /// English exemplars: see, hear, smell, look.
    Attend,
}
```

A pruned version (Schank's eleven minus the bodily-physical ones
that don't fit a daemon) gives a six-verb daemon-suitable subset:

```rust
pub enum SignalVerb {
    PTrans,  // routing records between components
    ATrans,  // possession-changes (Assert/Mutate)
    MTrans,  // information transfer (Match/Subscribe)
    MBuild,  // mental construction (Validate)
    Speak,   // utterance (Assert as publish)
    Attend,  // focusing (Subscribe as targeted observation)
}
```

Contract using the pruned six:

```rust
signal_channel! {
    request MindRequest {
        ATrans SubmitThought(SubmitThought),  // possession-change
        MTrans QueryThoughts(QueryThoughts),  // info-transfer
        MBuild ValidateGrant(ChannelGrant),   // mental-construction
        Speak  AssertClaim(RoleClaim),        // utterance
        Attend SubscribeThoughts(Subscribe),  // focus
    }
}
```

Wire frame:

```sh
mind '(ATrans (SubmitThought (...)))'
mind '(Attend (SubscribeThoughts (filter ...)))'
```

---

### 4.2 · NSM-derived spine (Wierzbicka's verbal primes, pruned to five)

```rust
/// Five core verbal primes from Anna Wierzbicka's Natural Semantic
/// Metalanguage. Selected from the ~17 verbal primes among NSM's 65;
/// the five chosen are the "action / event / utterance / consciousness
/// / retrieval" essentials that map onto daemon operation.
pub enum SignalVerb {
    /// The fundamental action verb.
    /// NSM exponent (English): "do"
    /// Cross-linguistic: translatable into every language NSM has tested.
    Do,

    /// The fundamental event verb.
    /// NSM exponent: "happen"
    Happen,

    /// The fundamental utterance verb.
    /// NSM exponent: "say"
    Say,

    /// The fundamental mental-construction verb.
    /// NSM exponent: "think"
    Think,

    /// The fundamental retrieval verb (knowing-what-is).
    /// NSM exponent: "know"
    Know,
}
```

Contract:

```rust
signal_channel! {
    request MindRequest {
        Do     PerformAction(Action),         // generic action
        Happen RecordEvent(Event),            // event occurred
        Say    PublishStatement(Statement),   // utterance
        Think  ValidateProposal(Proposal),    // mental construction
        Know   QueryState(StateQuery),        // retrieval
    }
}
```

The NSM family is academically strongest on cross-linguistic
universality grounds, weakest on database-operation-specificity.

---

### 4.3 · Jackendoff conceptual-primitive spine (five primitives)

```rust
/// Five conceptual-structure primitives from Ray Jackendoff's
/// *Semantic Structures* (1990).
pub enum SignalVerb {
    /// Motion through state-space.
    /// Persona analog: Subscribe (streaming through state changes).
    Go,

    /// State of being or identity.
    /// Persona analog: Match (one-shot state read).
    Be,

    /// Continuation of state.
    /// Persona analog: ongoing subscription.
    Stay,

    /// Causation of an event.
    /// Persona analog: Assert/Mutate (causing a state change).
    Cause,

    /// Permitting an event without forcing it.
    /// Persona analog: Validate (allowing without committing).
    Let,
}
```

Wire:

```sh
mind '(Cause (StateChange (item id-42) (new-status Closed)))'
mind '(Go (SubscriptionTransition (from open) (to streaming)))'
```

---

## 5 · Force-dynamic and minimalist spines

### 5.1 · Talmy force-dynamic spine (six force-pattern verbs)

```rust
/// Six force-dynamic patterns from Leonard Talmy's *Toward a Cognitive
/// Semantics* (2000). Each names a relation between two force-entities
/// (Agonist + Antagonist).
pub enum SignalVerb {
    /// Antagonist (caller) imposes change on Agonist (target).
    /// Maps to: extended causation. English modal: "made X happen."
    Extend,

    /// Antagonist prevents Agonist's tendency from manifesting.
    /// English modal: "kept X from happening."
    Block,

    /// Antagonist withdraws prior blocking.
    /// English modal: "let X happen."
    Release,

    /// Antagonist aids Agonist's tendency.
    /// English modal: "helped X happen."
    Help,

    /// Antagonist permits without forcing.
    /// English modal: "allowed X to happen."
    Permit,

    /// Antagonist resists but does not block.
    /// English modal: "hindered but did not stop X."
    Hinder,
}
```

This spine is **modal in flavor** — the verbs read like modal
auxiliaries (must, can, may) rather than database ops. Probably
better as an annotation than a primary spine.

---

### 5.2 · Aristotelian spine (two verbs)

```rust
/// Two verbs from Aristotle's *Categories*. The minimal coherent
/// classification: any verbal event is either doing-something or
/// having-something-done-to-you.
pub enum SignalVerb {
    /// (poiein: doing; making; producing; acting-on)
    /// The active mode. Subject acts on object.
    Do,

    /// (paskhein: suffering; undergoing; being-affected; receiving)
    /// The passive mode. Subject undergoes the action.
    Undergo,
}
```

Contract:

```rust
signal_channel! {
    request MindRequest {
        Do      SubmitThought(Thought),      // I do something to mind
        Do      QueryThoughts(QueryThoughts), // I act on mind to retrieve
        Undergo ReceiveStream(StreamRecord), // mind acts on me to deliver
    }
}
```

The Active/Passive distinction is roughly the request/reply split in
Signal today (the caller does, the daemon answers). Two verbs is
probably too coarse, but it's the philosophical-minimum case.

---

### 5.3 · Three-verb minimalist (action / state / process)

```rust
/// Three verbs partitioning verbal events by aspectual primary:
/// discrete event, persistent state, or ongoing process. Inspired by
/// Vendler reduced from four to three (collapsing achievement +
/// accomplishment into Act).
pub enum SignalVerb {
    /// Discrete telic event — happens at a point or over a bounded span.
    /// Includes: Assert, Mutate, Retract, Atomic, Validate.
    Act,

    /// Persistent state — being-a-certain-way.
    /// Includes: ongoing claim of state via Subscribe-to-state.
    State,

    /// Ongoing process — duration without bounded end.
    /// Includes: Subscribe-to-stream, Match-as-in-flight.
    Process,
}
```

---

## 6 · Topological spines

### 6.1 · Seven-planet octahedron (current spine + topology)

The seven-verb spine from `/162`, with classical-astrological aspects
encoded as adjacency / opposition rules.

```rust
/// Seven verbs from /162's planetary bijection, arranged as an
/// octahedron: six elementary on the equator, Atomic at the polar
/// binding point.
pub enum SignalVerb {
    Assert,      // Mars — the kleos-leaving strike that says "this happened"
    Mutate,      // Sun — re-manifest at identity (the Sun rises new each day)
    Retract,     // Saturn — impose-end (Cronus devouring his children)
    Match,       // Moon — reflect / show-stored (Luna returning the Sun's light)
    Subscribe,   // Mercury — relay / carry-between (Hermes the psychopomp)
    Validate,    // Venus — weigh / assay (Aphrodite-Urania's scales of judgment)
    Atomic,      // Jupiter — gather-many-into-one (Zeus the all-father, binder)
}

impl SignalVerb {
    /// Classical-astrological opposition (180°): semantic opposite.
    pub fn opposite(&self) -> Option<Self> {
        match self {
            Self::Assert => Some(Self::Retract),     // Mars ⇆ Saturn: write ⇆ end
            Self::Mutate => Some(Self::Match),       // Sun ⇆ Moon: change ⇆ reflect
            Self::Subscribe => Some(Self::Validate), // Mercury ⇆ Venus: stream ⇆ assay
            _ => None,                                // Jupiter has no opposite
        }
    }

    /// Classical sextile (60°): semantic compatibility.
    pub fn compatible(&self) -> Vec<Self> { /* ... */ todo!() }
}
```

Constraint: an `Atomic` bundle of opposite verbs is suspect (writing
+ retracting same record); same-sextile bundle is clean.

---

### 6.2 · Bhartṛhari speech-level spine (four levels of utterance)

The Sanskrit grammatical philosopher Bhartṛhari (c. 5th c. CE)
identified four levels at which speech exists:

```rust
/// Four levels of speech from Bhartṛhari's *Vākyapadīya*.
/// Not a peer-of-verbs spine; an *orthogonal pipeline stage*
/// classification — each Signal frame occupies one level.
pub enum SpeechLevel {
    /// (parā: transcendent; pre-formed; supreme; "the unmanifest")
    /// The unmanifested intent before articulation. In a daemon: the
    /// agent's internal state before any frame is constructed.
    Transcendent,

    /// (paśyantī: seeing; visioning; intuitive-stage; "vision-speech")
    /// The verb intuited as a whole, not yet formed. In a daemon:
    /// the type-checked Rust value before serialization.
    Intuitive,

    /// (madhyamā: middle; mental-form; intermediate; "thought-speech")
    /// The mentally-formed verb. In a daemon: the NOTA-encoded form
    /// in memory.
    Mental,

    /// (vaikharī: articulated; spoken-form; outer-speech; "voiced-speech")
    /// The fully-articulated wire-form. In a daemon: the
    /// length-prefixed rkyv bytes on the socket.
    Articulated,
}
```

Could be added as a typed pipeline annotation:

```rust
pub struct Op<P> {
    pub verb: SignalVerb,
    pub level: SpeechLevel,  // which stage of the pipeline this is at
    pub payload: P,
}
```

Not strictly a verb-spine; a stage-of-pipeline framework that could
coexist with any verb-spine.

---

## 7 · Multi-axis spines

### 7.1 · Full multi-axis (kinds × roles × aspect — the Pāṇinian pattern)

```rust
/// Three orthogonal closed sets simultaneously, following Pāṇini's
/// pattern of stating multiple axes explicitly.

pub enum SignalVerb {
    Material, Mental, Relational, Behavioral, Verbal, Existential,
    // OR: Assert, Mutate, Retract, Match, Subscribe, Validate
}

pub enum KarakaRole {
    Agent,      // (kartṛ: doer; one-who-acts)
    Patient,    // (karman: most-affected; undergoer)
    Instrument, // (karaṇa: means; by-which)
    Recipient,  // (sampradāna: beneficiary; for-whom)
    Source,     // (apādāna: that-from-which; origin)
    Locus,      // (adhikaraṇa: where/when; substrate)
}

pub enum AspectualContour {
    State,          // (Vendler atelic+durative+non-dynamic)
    Activity,       // (atelic+durative+dynamic)
    Accomplishment, // (telic+durative+dynamic)
    Achievement,    // (telic+punctual+dynamic)
}

pub struct Op<Payload> {
    pub verb:    SignalVerb,         // 1 of 6
    pub aspect:  AspectualContour,   // 1 of 4
    pub payload: Payload,            // each field tagged with KarakaRole
}
```

Contract with multi-axis declaration:

```rust
signal_channel! {
    request MindRequest {
        // Verb, aspect, then variant with kāraka-tagged fields.
        Material Achievement SubmitThought {
            #[karaka(Agent)]     submitter: ActorName,
            #[karaka(Patient)]   thought: Thought,
            #[karaka(Locus)]     timestamp: TimestampNanos,
        },
        Relational State QueryThoughts {
            #[karaka(Agent)]     querier: ActorName,
            #[karaka(Patient)]   query: QueryKind,
            #[karaka(Instrument)] limit: QueryLimit,
        },
        Behavioral Activity StreamThoughts {
            #[karaka(Recipient)] subscriber: ActorName,
            #[karaka(Patient)]   filter: SubscribeFilter,
        },
    }
}
```

Wire frame:

```sh
mind '(Material (Achievement (SubmitThought
  (agent persona-mind)
  (patient (Thought (title ...) (body ...)))
  (locus (now)))))'
```

This is the most ambitious shape. Every frame triply-classifies what
it is. The macro-generation work is significant; the introspection
power gain is also significant.

---

### 7.2 · Kāraka-only (current verbs + role-typed payload fields)

Subset of §7.1 keeping only the kāraka layer. Verbs stay as Persona's
current six; payload fields gain `#[karaka(...)]` annotations.

```rust
// Persona's current six (or §1.1's Halliday-loop six):
pub enum SignalVerb { Assert, Mutate, Retract, Match, Subscribe, Validate }

// Plus the kāraka role enum from §7.1 above, applied to fields.

signal_channel! {
    request HarnessRequest {
        Assert MessageDelivery {
            #[karaka(Agent)]     sender: MessageSender,
            #[karaka(Patient)]   body: MessageBody,
            #[karaka(Recipient)] harness: HarnessName,
            #[karaka(Locus)]     message_slot: MessageSlot,
        },
    }
}
```

Wire frame uses positional or named NOTA syntax (positional shown):

```sh
harness '(Assert (MessageDelivery
  alice                  ; agent
  "hello world"          ; patient
  harness-1              ; recipient
  slot-42))'             ; locus
```

The kāraka-tags make the field meanings semantically self-documenting
and allow generic dispatch (e.g., "for all messages where I am the
Recipient, ...").

---

### 7.3 · Verb × Vendler-aspect (two-axis spine)

```rust
pub enum SignalVerb { /* 6 verbs */ }
pub enum AspectualContour { State, Activity, Accomplishment, Achievement }

pub struct Op<P> {
    pub verb:   SignalVerb,
    pub aspect: AspectualContour,
    pub payload: P,
}
```

Contract:

```rust
signal_channel! {
    request MindRequest {
        Assert Achievement SubmitThought(SubmitThought),  // punctual write
        Match  Accomplishment QueryThoughts(QueryThoughts), // durative read with goal
        Subscribe Activity SubscribeThoughts(SubscribeSpec), // ongoing flow
        Subscribe State HoldClaim(RoleClaim),               // ongoing being-claimed
        Validate Achievement ValidateGrant(GrantProposal),  // dry-run point-act
    }
}
```

Wire:

```sh
mind '(Assert (Achievement (SubmitThought (...))))'
mind '(Subscribe (Activity (SubscribeThoughts (filter ...))))'
```

---

## 8 · Extreme cases

### 8.1 · Eight-verb extended (current six + Behave + Express)

```rust
pub enum SignalVerb {
    // Current six (per /166's collapse proposal):
    Assert, Mutate, Retract, Match, Subscribe, Validate,

    /// (Halliday's behavioral; an explicit ongoing-physiological-process verb)
    /// For: ongoing observations that aren't really subscriptions.
    Behave,

    /// (Searle's expressive; feedback, error, acknowledgment)
    /// For: out-of-band signals about other operations.
    Express,
}
```

(Probably overkill but documented for symmetry with the extreme cases.)

---

### 8.2 · Three-verb minimalist (Action / State / Process)

(Already shown in §5.3.)

---

### 8.3 · Single-verb (Mīmāṃsā limit)

(Already shown in §1.4.)

---

## 9 · Quick-reference comparison

| Candidate | Spine size | Other axes |
|---|---:|---|
| §1.1 Halliday-loop | 6 | adjacency topology |
| §1.2 Halliday-flat | 6 | — |
| §1.3 Searle-illocutionary | 5 | direction-of-fit |
| §1.4 Mīmāṃsā single | 1 | InjectionMode (size 7) |
| §2.1 Pāṇini-lakāra | 6 | — |
| §2.2 Vendler-aspectual | 4 | — |
| §3.1 Kāraka (annotation) | n/a | 6 roles on payload fields |
| §3.2 Tesnière-valency | 4 | + 5 diatheses |
| §4.1 Schank-CD | 11 (or 6 pruned) | — |
| §4.2 NSM-derived | 5 | universal-prime claim |
| §4.3 Jackendoff | 5 | conceptual-function |
| §5.1 Talmy force-dynamic | 6 | modal flavor |
| §5.2 Aristotelian | 2 | — |
| §5.3 Three-verb minimalist | 3 | aspect-flavored |
| §6.1 Seven-planet octahedron | 7 | aspect/opposition topology |
| §6.2 Bhartṛhari speech-level | n/a | 4 pipeline-stage levels |
| §7.1 Full multi-axis (Pāṇinian) | 6 × 6 × 4 | three closed sets |
| §7.2 Kāraka-only | 6 verbs + 6 roles | role-typed fields |
| §7.3 Verb × Vendler | 6 × 4 | two-axis |
| §8.1 Eight-verb extended | 8 | — |

---

## 10 · See also

- `~/primary/reports/designer/168-candidate-verb-spines-brainstorm.md`
  — the prose brainstorm this companion translates. Numbering of
  candidates differs because this report groups by family-of-spine
  rather than 1-23 enumeration.
- `~/primary/reports/designer/167-universal-verb-model-literature-survey.md`
  — the source-extraction for every term in this report. All
  Sanskrit translations follow Coward and Matilal's conventions.
- `/git/github.com/LiGoldragon/signal-core/src/channel.rs` — the
  current `signal_channel!` macro, which would need to grow to
  support the multi-axis (§7.1) and kāraka-annotated (§3.1, §7.2)
  declarations.
- `/git/github.com/LiGoldragon/signal-core/src/request.rs` — the
  current `SignalVerb` enum, which any of these candidates would
  replace.
