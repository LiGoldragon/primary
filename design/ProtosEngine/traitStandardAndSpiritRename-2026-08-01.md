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
