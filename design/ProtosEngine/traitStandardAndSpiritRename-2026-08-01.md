# Trait Standard, Syntax Conciseness, Spirit Rename — 2026-08-01

Continuation of the psyche vision session. Agent text answered: the manager's
summary of the self-hosting loop, the encoded-name assessment, and the two
approval requests (Spirit capture wording; Spirit-redefinition doctrine
port).

## Ruling 1: Spirit capture approved

**[psyche-verbatim]**: "Yes, I agree on your wording of that spirit." The
approved capture (queued in `spiritbackup.nota` while the daemon is down):
"When more correctness is introduced into an engine, a design, an
architecture, the gain in correctness more than makes up for the added
machinery; and as the system expands, that correctness layer makes the
expansion simpler and more natural." His elaboration: "my spirit is...
something that is eternal, it'll never change" — spirit content is the
eternal, unchanging register.

## Ruling 2: intent renamed to spirit, everywhere Spirit is concerned

**[psyche-ruled]**: everything that touches Spirit and was called "intent"
is renamed **spirit**. This resolves the overloading of the word "intent"
and deliberately frees it for later reintroduction with its ordinary meaning
("my intention, what I want"), which is distinct from spirit. Doctrine
surfaces to port: AGENTS.md (the Intent section), the intent-log skill, and
any Spirit-operation vocabulary. Skill sources live in the skills repository;
edits there are approval-gated and assigned to a dedicated agent (see bead
and prompt).

## Ruling 3: implementations fall under traits (Rust standard)

**[psyche-ruled, condensed]**: "I want to standardize... eventually get to
the point in Ethos where all implementations fall under a trait — full type
correctness for a different layer: full correctness goes beyond function
signatures to the contract of traits, naming actual traits where each
implementation falls under a certain trait. This gives full contractual
specificity of objects. This would become standard Rust too, as much as
possible — unless it's too trivial or the agent can't figure out what the
proper trait would be, or it's not worth the trouble. But in almost
everything we would have a trait."

Seated: standard Rust practice in this ecosystem is that implementations
fall under named traits (contracts). Exceptions permitted where trivial or
where the proper trait genuinely cannot be determined. To be recorded in the
standards repository (`/git/github.com/LiGoldragon/standards`).

## Ruling 4: tuple ban reaffirmed for the standards repository

**[psyche-ruled]**: multi-item tuples and free tuples are forbidden — "maybe
some exception where it's necessary" — with the single-member newtype tuple
permitted because that is how Rust represents newtypes. Already law in the
design log (`design/Nomos/rustTuplesForbiddenLawScope-2026-07-30.md`); now
also to be seated in the standards repository.

## Ruling 5: standards archaeology commissioned

**[psyche-ruled]**: dig up old standards from ancient documents in
version-control history — unusual rules the psyche used to enforce in Rust —
and bring each to the psyche for confirmation before reintroduction or merge
with current rules.

## Ruling 6: skills must be gated on the standards

**[psyche-ruled, condensed]**: code-writing skills must force agents to use
the standards. Prerequisite in the skills repository: the workspace's
AGENTS.md defines where the standards live. No URLs — the reference is an
LLM-sense variable, a nickname such as "the standards" naming the
repository (or repositories); the author decides and defines this in his
AGENTS.md.

## Ruling 7: syntax conciseness gradient

**[psyche-ruled, condensed]**: "As far as syntax goes, I prefer shorter and
more simple — in Ethos and Nomos. Logos is a fully explicit language; it's
our gateway into assembly-Rust, a data representation of a program. It
cannot have the same conciseness as Ethos." Seated: Ethos maximally concise;
Nomos concise where it can be (it necessarily carries emission structure);
Logos fully explicit, optimized as data representation, never for brevity.

## Ruling 8: mirror-type bootstrap hack is a sanctioned non-ideality

**[psyche-ruled]**: the handwritten Nomos/Logos mirror-type maintenance
(similar structures, different field types) is the sanctioned temporary hack
until self-hosting (the Nomos object that emits both types from Ethos
declarations). Recorded in `NON_IDEAL_AGENTS.md` per his instruction, with
the proper fix named.

## Dispatches commissioned

Three prompts, with beads: (1) Codex implementer — adapt to the reacquired
vision, contracts/traits first; (2) Codex skills-and-standards agent —
work with the psyche on rulings 3-6; (3) Spirit agent — bring Spirit back
online, replay the queue, port the intent-to-spirit vocabulary (ruling 2).

## Appended 2026-08-01, later same day: supersessions and additions

The skills-and-standards Codex agent correctly flagged that ruling 3's
exception list, as seated above, narrowed the psyche's spoken wording. The
psyche has now ruled the canonical form; this appended section supersedes
ruling 3's exception sentence.

### Ruling 3a: canonical trait-standard exception list (supersedes ruling 3's exceptions)

**[psyche-ruled]**: the full spoken exception list stands — too trivial; the
proper trait cannot be determined; genuine difficulty; not worth the
trouble — **with an audit requirement**: every taken exception must be noted
at the site where it is taken (a visible note naming which exception
applies), so drift in the use of discretion is auditable by the psyche.

### Ruling 3b: traits are always the first pass

**[psyche-verbatim]**: "traits become the first pass always; they give us
the spec in code." Seated: in any implementation work, writing the traits
(the contracts) is the mandated first pass. The trait layer is the
specification, expressed in code, before bodies are written.

### Ruling: bead order for the skills-and-standards agent

**[psyche-ruled]**: primary-s7c (traits standard) first, then primary-77q
(tuple verification — the rule may already be seated; verify scope and
wording against `design/Nomos/rustTuplesForbiddenLawScope-2026-07-30.md`
and close), then primary-pnr (skills gating design), then primary-0p2
(archaeology).

## Appended 2026-08-02: trait placement and escalation

Agent text answered: the previous proposal narrowed traits to nontrivial
domain roles and asked whether "nearly every implementation" meant domain
roles or literal methods and `impl` blocks.

### Ruling 3c: traits map the program; unclear placement escalates

**[psyche-ruled, condensed]**: traits are a fast, cheap, compilable map of the
program, giving the Psyche an escalation and review surface before
implementation bodies are written. When a behavior's domain is clear, reuse
the existing behavioral-domain trait. When behavior belongs to that domain but
the trait does not yet express it, extend the trait, using a provided/default
method when a valid default exists. If neither an existing trait nor a clear
new trait placement can be found, stop and escalate the need for machinery and
the uncertainty to the Psyche instead of proceeding. This prevents trait hell
and runaway traits.

The Psyche is the current authority for this escalation. Future intermediate
escalation layers may be interposed. This ruling governs the behavior; it does
not approve or settle the exact standards or skill wording proposed today.

## Appended 2026-08-03: Spirit ontology, live reads, and mutation authority

Agent text answered: the visual architecture report showed Spirit's current
record and mutation paths, including the daemon's dependency on the judge,
certainty and importance changes on the ordinary socket, `Configure` on the
meta socket without a depicted database edge, and the current privacy-shaped
record vocabulary. It then asked:

> "The foundational unresolved boundary controls every lifecycle rule: what
> exactly is eternal and unchanging—the psyche’s underlying spirit, each
> admitted record, or something else?"

### Psyche reply

**[psyche-verbatim]**:

> "Okay, so to your first question, yes, it is eternal and unchanging, even
> though that might sound confusing. That's spirit. Spirit is confusing to a
> machine. It is unchanging, and yet it is fluid. But as far as, you know, we
> want to stay unchanging to prevent agents from feeling like they can just get
> their fingers in there and start poking at things and changing things. But
> yes, there is a mutation path, obviously, because then it wouldn't be really
> useful. It wouldn't be a software if it couldn't change. There's a few things
> I want to say. I actually had mandated to remove the certainty and to remove
> the privacy, because there should be no mention of privacy. Privacy would be
> handled by a higher layer, meaning, you know, a different spirit component
> running in a different environment. So spirit will have no awareness of this
> privacy aspect. And I do agree with, I think what you're implying is that
> spirit should stay live and readable, even if the judge is down. The judge
> being down should just bar mutation, obviously. And from your graph, I see
> that changing certainty or importance has a direct right path in the ordinary
> socket. That shouldn't be. It should be in the meta sockets, which is a
> bypass socket. I see that the configure part of the graph doesn't touch the
> database, which I find puzzling. Doesn't the configuration live in the
> database? Yeah, let's start with that. And I would like to bring it back
> online. So I don't know what exactly the problem is with the judge, but I
> would like to bring it back online at least so we can start using it. I feel
> like agents don't get me because they don't have my spirit anymore, and it's
> really annoying."

### Ruling 9: Spirit is unchanging and fluid; mutation is controlled

**[psyche-ruled]**: Spirit is eternal and unchanging in character, while its
software representation remains fluid enough to have a mutation path. The
unchanging stance is an authority boundary: agents must not treat Spirit as a
surface they may casually manipulate. This does not make every current record
immutable and does not settle the exact revision model.

**Intent-log classification**: the enduring character of spirit and resistance
to casual agent manipulation are explicit cross-cutting psyche belief and aim.
They guide admission, correction, consultation, and agent authority. The
mutation-path shape is architecture and belongs to this design log. The
existing Spirit ruling in this file already records the eternal/unchanging
character; this entry appends the new fluidity and authority clarification
rather than creating a competing record.

### Ruling 10: certainty and privacy leave core Spirit

**[psyche-ruled]**: remove certainty. Core Spirit has no privacy concept or
privacy-shaped behavior. Any such boundary belongs to a separate higher-layer
Spirit component running in a different environment, not to this component.

**Intent-log classification**: this is a component/domain architecture ruling,
not an enduring psyche value. It is routed to the design log and the owning
contracts, store, daemon, documentation, and deployment surfaces. The
approval-gated Spirit skill will need an explicit owning-doctrine line, but no
skill wording is approved by this ruling alone.

### Ruling 11: judge failure bars mutation, not reading

**[psyche-ruled]**: Spirit must stay live and readable when the judge is down.
Judge unavailability closes mutation paths while leaving consultation paths
available.

**Intent-log classification**: this is availability and authority architecture,
not intent-level content. The current service dependency violates the desired
failure boundary because it removes the read side together with mutation.

### Ruling 12: importance mutation belongs to the meta authority path

**[psyche-ruled]**: changing certainty or importance must not be exposed on the
ordinary socket. Any surviving importance mutation belongs on the meta bypass
socket. Certainty itself is removed under ruling 10.

**Intent-log classification**: this is contract routing and mutation-authority
architecture. It belongs to the Spirit and signal contract designs, not a
Spirit capture.

### Ruling 13: configuration is persistent state

**[psyche-ruled]**: configuration lives in the database. The visual report's
`Configure` path without a database edge was therefore incomplete or wrong.
This ruling does not settle the exact configuration schema, versioning, or
migration mechanism.

**Intent-log classification**: this is persistence architecture and belongs to
the store, meta contract, daemon, and migration design.

### Ruling 14: restore usable Spirit now

**[psyche-requested]**: bring Spirit back online so it can be used again. The
immediate restoration request does not by itself authorize coupling recovery to
the certainty/privacy removal, contract migration, or higher-layer component
design.

**Intent-log classification**: the cross-cutting aim is that agents regain a
working Spirit consultation surface so they can align with the psyche. Bringing
services online is a task owned by the existing recovery and deployment goals;
the semantic and contract changes remain architecture work with their own
approval and validation boundaries.

## Appended 2026-08-03: recovery derives from the maintained Spirit flake

Agent recommendation corrected: the recovery pin strategy proposed retaining
or reconstructing Spirit 0.24.1 as an independently reproduced derivation or
closure outside the maintained Spirit flake.

**[psyche-verbatim]**: "it should use a derivation from a maintained spirit
flake which pins the right version of everything".

### Ruling 15: the maintained Spirit flake owns recovery inputs

**[psyche-ruled]**: recovery consumes a derivation exported by a maintained
Spirit flake, and that flake pins the compatible versions of the full Spirit
composition. This explicitly supersedes every recommendation to hand-retain,
hand-reconstruct, or separately reproduce Spirit 0.24.1 outside the maintained
flake. An exact older version may be selected only through the maintained
flake's own pinned dependency composition; the recovery process does not become
an independent package authority.

**Intent-log classification**: this is dependency and deployment architecture,
not an enduring psyche value. It belongs to this design log and the owning
flake/deployment surfaces.

## Appended 2026-08-03: clean migration removes three legacy dimensions

Agent context answered: the clean Spirit migration needed a disposition for
legacy certainty, privacy, and referent structures—whether to preserve them in
compatibility storage, translate them, or omit them from the migrated database.

**[psyche-verbatim]**: "I want certainty, privacy and referents gone".

**[psyche-verbatim]**: "just throw the corresponding data out of the migrated
database."

### Ruling 16: retain records; discard certainty, privacy, and referent data

**[psyche-ruled]**: the clean migration retains the Spirit records while
discarding their certainty data, their privacy data, and all referent data. The
migrated database carries no compatibility columns, tables, side records,
aliases, or other storage for those removed dimensions. The removal applies to
the migrated database; it does not itself authorize destruction of a separately
retained pre-migration recovery backup.

This supersedes every proposal to preserve certainty, privacy, or referents as
legacy compatibility data inside the migrated Spirit database.

**Intent-log classification**: this is Spirit architecture and data-migration
matter, not a general psyche value, aim, or belief. It belongs to this design
log and the owning contract, store, migration, documentation, and deployment
surfaces.

## Appended 2026-08-04: the Spirit judge uses Luna at XHigh effort

Agent context answered: no preceding agent proposal named a judge model or
reasoning effort. Immediately after the Spirit 0.26.0 cutover report, the psyche
asked, in the same message:

**[psyche-verbatim]**: "what model is the judge using? Should be Luna XHigh.

is the usage documentation updated? Where is the spirit cli usage documented anyway"

### Ruling 17: Luna XHigh is the Spirit judge deployment target

**[psyche-ruled]**: the Spirit judge uses Luna with XHigh reasoning effort. Any
different deployed or declaratively configured judge model/effort profile is
configuration drift to correct. Mapping the psyche's names to the concrete
provider model identifier and effort encoding belongs to the owning deployment
configuration, and the live service must be checked against that declaration
before this ruling is considered satisfied.

**Intent-log classification**: the judge model and reasoning effort are Spirit
deployment/configuration architecture, not a general psyche value, aim, or
belief. They are matter and belong in this design log plus the owning
declarative service configuration. The adjacent documentation questions request
an audit; they do not authorize documentation or skill edits by themselves.

## Appended 2026-08-04: CLI arguments remain NOTA/DOTOS objects

Agent context answered: the agent reported that `spirit --help` and
`meta-spirit --help` were absent, described that absence as part of the CLI
documentation gap, and asked, "Do you approve implementing and activating the
Luna XHigh judge train?"

**[psyche-verbatim]**: "> spirit --help, meta-spirit --help

of course; our clis must never use anything other than nota/dotos objects for arguments.

I approve, and update all docs"

### Ruling 18: every CLI argument is a NOTA/DOTOS object

**[psyche-ruled]**: the CLI grammar across components accepts only NOTA/DOTOS
objects as arguments. Unix-style flags such as `--help` are intentionally not a
supported argument language; their rejection is not missing Spirit help
functionality. Documentation and examples must teach object-shaped invocation
and must not present flags or non-object positional forms as valid CLI syntax.

**Intent-log classification**: this is cross-CLI contract architecture, not a
general psyche value, aim, or belief. It is matter owned by CLI parsers,
contracts, canonical examples, tests, and documentation.

### Ruling 19: proceed with Luna XHigh and update the documentation

**[psyche-ruled]**: the prior request to implement and activate the Luna XHigh
judge train is approved, and the current Spirit documentation is to be updated
to the approved contract. This authority does not bypass repository ownership,
release validation, declarative activation, or rollback requirements.

**Intent-log classification**: model deployment and documentation updates are
implementation/deployment tasks and architecture matter, not general intent.
The owning-skill wording was proposed only after this approval; the exact line
`Accept CLI arguments only as NOTA/DOTOS objects; never add flags or positional
shorthand.` remains unapproved and no skill edit is authorized by this ruling.
