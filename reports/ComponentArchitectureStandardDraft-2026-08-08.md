# Component Architecture Standard — Draft

Designer draft, 2026-08-08, for psyche review. Written in vision
description mode — this states what components ARE, not how to build
them or migrate to them. Sources: the psyche's logged rulings
(psyche/Vision/), the pre-reset corpus (2026-06-07 stratum, synthesized
in reports/PreResetCorpusSynthesis-2026-08-08.md), and the 2026-08-08
signal-layer divergence audit.

Provenance marks, used throughout:

- **[psyche]** — backed by your verbatim words; the Vision entry or
  record is cited.
- **[doctrine]** — the pre-reset corpus teaches it; the source file is
  cited. You shaped that corpus, but these words are agent-written and
  the corpus predates the reset — treat as strong ancestry, not as
  your voice.
- **[audit]** — a fact about today's code, from the 08-08 audits.
- **[proposal]** — mine. A lean, not a verdict; you rule.

Names carried from the pre-reset corpus (Nexus, SemaPlane vocabulary,
archetype names, trait names) are agent coinage unless marked
**[psyche]**.

---

## 1. What a component is

**[psyche]** Every component is a daemon speaking Signal, with a CLI,
and a CLI for the meta socket:

> "They're all daemons. The same architecture as all my other
> components, right? There's the daemon, there's a CLI, there's a CLI
> for the metasocket. Everything is signal messages, meaning RKYV
> binary messages."
> — everythingIsInTheDaemon.md, 2026-08-08

A component's repo set:

| Repo | Holds | Provenance |
|---|---|---|
| `<component>` | The daemon and its logic | [psyche] majorRecoveryEffort.md |
| `signal-<component>` | The typed vocabulary of its public wire surface | [psyche] "they will each have a signal-XXX and meta-signal-XXX repo, which will hold the ethos describing the types of the messaging layer" |
| `meta-signal-<component>` | The owner/meta vocabulary (policy, configuration) | [psyche] same ruling |
| `core-<component>` | Optional library; a dependency OF the daemon, never the reverse | [psyche] "we can still have a core-XXX repo for each, if you think that wise or useful, otherwise all the logic can live in the main repo" — left to designer judgment; see fork F2 |

**[doctrine]** The contract split exists for two still-standing
reasons (component-triad.md, per your 2026-06-04 record 2605):
rebuild-churn isolation (peers recompile only on wire changes) and
security-sensitivity visibility (owner-only operations live in a
visibly distinct repo). The doctrine's third point — `meta-signal-`
optional where no owner relationship exists — is superseded
**[psyche]**: "the metasignal is not optional because otherwise
there's no way to configure the daemon" (metaSignalNotOptional.md,
2026-08-09). Every component carries both contract repos.

**[doctrine]** "The contract crates carry no runtime, no actors, no
`tokio` — they declare typed wire vocabulary and generated method
surfaces, and nothing else" (component-triad.md).

Binary naming **[doctrine]** (component-triad.md): the CLI binary is
`<component>` — what a human types; the daemon binary is
`<component>-daemon`. No `-cli`, `-server`, `-service` suffixes. The
meta-socket CLI is `<component>-meta` **[psyche]**
(metaCliIsComponentDashMeta.md, 2026-08-09).

## 2. Signal — the messaging layer

**[psyche]** The definition:

> "Signal is our messaging layer, and the CLI's role is to transform
> text into Signal."
> — signalIsOurMessagingLayer.md, 2026-08-08

> "Everything is signal messages, meaning RKYV binary messages. That's
> what signal means."
> — everythingIsInTheDaemon.md, 2026-08-08

**[psyche]** Signal is currently ad hoc and needs a clean reference
point: "I feel like all the demons like use a different approach...
let's like start defining all of this properly... a clean reference
point for everything" (signalIsOurMessagingLayer.md). The **[audit]**
confirms four divergent wire families in today's code; the Spirit
daemon's family (triad-runtime, dual sockets, full portable rkyv
feature set, signal-/meta-signal- contract pairs) is the closest to
standard-shaped.

**[doctrine]** The wire shape the pre-reset corpus settled on, which I
propose as the Signal standard's baseline **[proposal]**:

- Inner frame: the rkyv archive of the message **[psyche]**
  ("Everything is signal messages, meaning RKYV binary messages").
  The pre-reset `[u64 little-endian short header]` prefix —
  constant-time message discrimination before deserialization
  (cloud-designer/32/5) — is ruled a draft idea, not part of the
  present standard **[psyche]**: "a great idea, but it's quite low
  level, and right now we don't need to" (shortHeaderNotNow.md,
  2026-08-09). It lives on the draft-ideas surface — section 2a.
- Outer transport frame: `[u32 big-endian length][body]` with a
  maximum-frame-length guard (contract-repo.md, triad-runtime).
- Portable rkyv, full feature set — bytecheck-only builds are a
  portability defect [audit].
- Two sockets per daemon: the ordinary socket (any authenticated
  peer) and the meta socket (owner only) [doctrine, and your
  "a CLI for the metasocket" implies the meta socket] .
- A typed refusal envelope on every surface (Family A's
  EngineRefusal shape) [audit/doctrine].

**[psyche]** The long arc: "the daemon doesn't really speak string.
Although for now they're records that will hold string fields... 
eventually even all of the string part of language will be replaced by
a completely specified, fully typed binary system of enums and structs
and scalar values" (majorRecoveryEffort.md).

Unruled inside Signal — see forks F4, F5: whether connections open
with a handshake (today's language engines have one, the Spirit family
has none [audit]), and whether streaming/subscription is part of the
core Signal standard (only Spirit and the language engines have it
[audit]).

## 2a. Concept repos and draft ideas

**[psyche]** (everyConceptShouldHaveItsRepo.md, 2026-08-09): "every
concept should really have its repo, and if anything goes in there,
the traits can, since every concept deserves at least one trait, and
probably more." Signal is a concept, so Signal gets a concept repo
holding Signal's traits and reference definition — the "clean
reference point" you asked for in signalIsOurMessagingLayer.md.

**[psyche]** (draftIdeasForImprovement.md, 2026-08-09): design parts
that are good ideas but not decided for implementation need a marked
home — "a documentation file for the sort of thing that we haven't
really decided to implement, but that are drafted as good ideas for
future improvement of the particular component or logic."

**[doctrine]** The pre-reset corpus carried exactly this mechanism:
architecture-editor.md mandates a "Possible future design" section in
every ARCHITECTURE.md — "a standard part of every architecture file,
not something added only when uncertainty happens to exist" — sitting
after the cemented body, uncertainty named explicitly, never smuggled
into present-tense prose.

**[psyche]** (2026-08-09) Not ARCHITECTURE.md: "I dont like
architecture.md; it doesnt say 'possible future implementation ideas/
new features'" (draftIdeasForImprovement.md). The home is a dedicated
file per repo whose name says what it holds; a concept's draft ideas
live in its concept repo. First entry: the Signal short header, in the
signal concept repo's file. The file's name awaits your blessing —
proposed **[proposal]**, agent-coined: `FutureIdeas.md`, headed with
your phrase "possible future implementation ideas / new features".

## 3. Contract repos

**[doctrine]** (contract-repo.md) A contract crate owns: the frame
envelope and its encode/decode, the framing rule, protocol version, a
closed enum of request kinds with paired reply kinds, per-operation
typed payloads (no `Unknown` variant), version-skew guard, and
complete round-trip tests. It does not own daemon code, state, or any
logic that interprets records.

- Operation roots are verbs in verb form: `Submit`, not `Submission`.
  Replies are verb-past-tense: `Submitted`; rejections
  `SubmitRejected` [doctrine].
- The contract crate's semver IS the wire's semver; consumers pin the
  version [doctrine].
- **[psyche]** (2026-06-04, record 2612): "Sema classification
  vocabulary is forbidden on the public contract wire." The audit
  found pre-reset violations of exactly this; the standard keeps the
  rule.
- Examples-first: every record kind lands as a concrete text example
  plus a round-trip test before its Rust definition is final; "the
  text example is the falsifiable specification" [doctrine].

## 4. Inside the daemon — the three planes

The deepest pre-reset teaching about the daemon interior, absent from
everything post-reset:

**[doctrine]** Each daemon's interior is three schema-driven planes —
one primitive projected three ways:

> "Every plane is a REACTION LANGUAGE: an engine matches an input tree
> against runtime state and produces a corresponding output tree...
> the three planes are not three different kinds of thing, they are
> one primitive projected three ways, differing only by ownership and
> runtime semantics, never by authored shape."
> — pre-reset designer/548

| Plane | Role | Never does |
|---|---|---|
| Signal plane | Reactive external surface: framing, dispatch, admission, connection lifecycle | Decide acceptability, touch storage, interpret payloads |
| Nexus plane | Execution: owns in-flight work, translates Signal to Sema and back; the daemon's feature catalog — every internal feature is a declared verb+object in its schema, never hidden inline logic | Hold durable state |
| Sema plane | Durable single-writer state; concurrent reads queue through one writer | Call back up directly |

The flow [doctrine]: Signal in → Nexus accepts → Nexus translates to
Sema operation → Sema runs → Nexus translates the reply → Signal out.
Effects are data — the Nexus decision step returns typed actions
(reply / sema-write / sema-read / effect / continue), it never
performs them [doctrine, designer/553/2]. That property is what lets
the same logic run sync today and actor-native later (fork F6).

**Two triads, orthogonal — never conflate them.** Ethos, nomos, logos
are components (repos, daemons). Signal/Nexus/Sema are planes inside
every daemon — each of the three language daemons has all three
planes. The names ethos/nomos/logos appear nowhere in the pre-reset
corpus; the planes are their ancestry (Signal → communication, Nexus →
decisions, Sema → durable meaning), not their definition [audit of the
corpus]. Whether the plane vocabulary itself survives into the new
standard is fork F3 — my lean **[proposal]** is yes: nothing you have
said contradicts it, and "everything is in the daemon" composes
cleanly with it.

## 5. Sema — per-daemon storage

- **[psyche]** Each daemon owns its own sema database: "all three
  holding their language in their own sema database"
  (everythingIsInTheDaemon.md).
- **[psyche]** (2026-07-27 ruling, standing): no sema-storage daemon.
  A central storage daemon is forbidden; each daemon embeds its own
  store. Today's `sema-storage` daemon is a standing violation
  [audit].
- **[doctrine]** The embedded store goes through the sema-engine
  library exclusively — daemons never open redb directly, define raw
  tables, or run raw transactions (system-designer/63). Database
  files carry a `.sema` extension, not `.redb` — the name states what
  it is (system-designer/63).
- **[doctrine]** Policy state and working state live in the same
  per-daemon store; policy state changes only via meta-socket Mutate
  operations (component-triad.md invariant 5).
- **[doctrine]** The long arc: sema today is the typed storage kernel;
  eventually a universal medium for meaning. Two scopes, one word —
  the standard should always say which is meant (tension #5 in the
  synthesis).

## 6. The CLI — a shim

- **[psyche]** "The CLI's role is to transform text into Signal"
  (signalIsOurMessagingLayer.md). The CLI is a translator at the text
  edge; the daemon never thinks in text.
- **[doctrine]** A CLI has exactly one Signal peer — its own daemon.
  It cannot multiplex daemons, open any durable database, or speak a
  parallel protocol (component-triad.md invariant 1). Daemons, by
  contrast, may be Signal clients of any number of peer daemons.
- **[doctrine]** The one-argument rule: every component process takes
  exactly one argv argument, never a flag. The CLI accepts inline
  text, a text file path, or a signal-encoded file path; the daemon
  accepts only a path to a pre-generated signal-encoded startup
  message and rejects text in any form (component-triad.md).
- **[doctrine]** "The CLI is eventually obsolete machinery. Keep
  CLI-side logic thin accordingly" — held in tension with the rule
  that every stateful component exposes one (synthesis tension #2).
  The standard keeps both: required now, thin because doomed.
- **[psyche]** There is also a CLI for the meta socket
  (everythingIsInTheDaemon.md). Its naming is unsettled — fork F9.

The textual form the CLI translates is currently named Dotos, and
**[psyche]** that name "doesn't stick" and is open for renaming
(signalIsOurMessagingLayer.md) — this standard therefore says "the
textual form" and never depends on the name.

## 7. Daemon lifecycle

**[doctrine]** (designer/550-v2, component-triad.md):

- A daemon's single startup argument is a pre-generated signal-encoded
  Configure message. Bootstrap depends on no manager — a manager
  dependency is circular.
- A virgin daemon (empty store) applies the Configure as its first
  configuration; a daemon with a populated store self-resumes.
- The same Configure type is accepted live over the meta socket — two
  delivery channels, one schema. Configuration is a Mutate: integral
  durable state, changed through the same authority chain as any other
  state.
- On first start with no policy state, the daemon enters an
  Unconfigured semi-started state rather than dying or guessing.

**[psyche]** Bootstrap from the textual form is real for the language
components: "Nomos loads its transformer index from textual Nomos at
bootstrap" (everythingIsInTheDaemon.md) — the loading is performed by
reading the textual form through the translation edge, never by the
daemon parsing text itself [proposal — consistent with the daemon
text-rejection rule; the exact mechanism is unruled].

## 8. Authority and composition — how components fit together

- Contracts split by who-can-call, not by what-state-they-touch:
  `signal-` is the ordinary peer surface, `meta-signal-` is the
  owner's [doctrine, component-triad.md invariant 4].
- "Observation up, authority down": authority issues Mutate downward;
  state flows upward via push subscriptions [doctrine].
- Polling is forbidden; producers push, consumers subscribe; every
  subscription opens with a typed snapshot, then deltas [doctrine,
  push-not-pull.md, subscription-lifecycle.md].
- Peers depend on a component's contract crates, never on its daemon
  or internals [doctrine].
- There is no text on the wire between live components — the textual
  form exists at human edges only [doctrine, Spirit-1373-class rule;
  consistent with [psyche] "Everything is signal messages"].
- Partial failure: an issuer commits on first success and records
  divergence on failure; no two-phase all-or-nothing stalls
  [doctrine].
- Pure libraries are a named carve-out — they need no daemon (the
  frame codec, sema-engine itself) [doctrine].

## 9. The language components — ethos, nomos, logos

All three are instances of sections 1–8 [psyche]. What is specific to
them, all from everythingIsInTheDaemon.md **[psyche]** unless marked:

- The Ethos daemon loads the ethos and holds the whole thing — every
  object in its own specifically typed object, a specific type for
  every kind, including the Nomos object. Those Nomos types are shared
  with the Nomos daemon.
- Ethos holds the Nomos transformer input schemas — strictly typed
  objects per transformer.
- Nomos loads its transformer index from textual Nomos at bootstrap
  and stores it in its sema plane.
- Nomos communicates with Logos via Signal — "here's a new object" —
  operational editing.
- Each daemon holds its language in its own sema database.
- `core-<component>` (if kept — fork F2) is a dependency of the
  daemon, not the other way around.
- The translator seat is named protos-translator [psyche,
  itsATranslator.md]; it translates code into text. Its scope —
  encoded identities to readable names, or the whole program to
  textual form — is open with you (fork F7). Direction text-to-Signal
  belongs to the CLI, not the translator [psyche, read together with
  signalIsOurMessagingLayer.md].

## 10. Sizing, repos, naming

**[doctrine]** (micro-components.md, crate-layout.md, naming.md) — the
rules that still bind under this standard:

- One capability, one crate, one repo; a new feature defaults to a new
  crate, and the burden of proof is on growth.
- A component fits in a single LLM context window (~3k–10k lines);
  above the ceiling, split.
- Components communicate only through typed protocols; no shared
  mutable state; independently buildable, testable, replaceable.
- Cross-repo dependencies are pinned git references, never sibling
  paths.
- Identifiers are full English words; names don't carry their
  ancestry; no framework-category suffixes.

## 11. Concurrency stance — the open fork the corpus died on

The sharpest pre-reset contradiction (synthesis B.1) is also the one
the recovery must not repeat blind:

- actor-systems.md taught "actors all the way down" in the present
  tense while the entire component codebase had zero actor
  dependencies [doctrine + audit of the corpus].
- The reconciliation that was actually ruled: sync thread-per-request
  daemons driving the three plane traits now, actor-native as the
  eventual picture, two daemon archetypes selected by reply
  disposition — request/reply, or reply-then-subscribe [doctrine,
  cloud-designer/34/5].
- Because Nexus decisions return effects as data (section 4), the
  same plane logic serves both stances; only the driver changes
  [doctrine].

**[proposal]** The standard adopts the ruled reconciliation: the
daemon shell is sync thread-per-request today; the plane logic is
written effects-as-data so the actor-native shell remains a driver
swap, not a rewrite. Needs your confirmation — fork F6.

## 12. Forks for the psyche

Consolidated; F1–F4 overlap the recovery plan's stage-0 OPEN items.

- **F1** — Rename existing engine repos into ethos/nomos/logos, or
  start fresh (recovery OPEN-A; nomos especially).
- **F2** — Keep `core-<component>` repos, or fold logic into the main
  repo (recovery OPEN-B). My lean: keep a core- repo only where
  another daemon must consume the logic as a library (the shared
  Nomos types); fold otherwise.
- **F3** — Does the three-plane daemon interior (section 4) remain
  the standard? My lean: yes.
- **F4** — Handshake on connection open: the Spirit family has none,
  the language engines require one. One answer for Signal.
- **F5** — Is streaming/subscription part of core Signal, or an
  extension only some components carry?
- **F6** — Confirm the concurrency stance (section 11).
- **F7** — protos-translator scope: identities-to-names, or
  whole-program-to-text.
- **F8** — The textual form's name (Dotos doesn't stick) and the
  standards repo's name — both yours, both said to be no big deal.
- **F9** — RESOLVED 2026-08-09: the meta-socket CLI is
  `<component>-meta` [psyche].
- **F11** — PARTLY RESOLVED 2026-08-09: a dedicated file, not
  ARCHITECTURE.md [psyche]. Remaining: the file's name — proposed
  `FutureIdeas.md` [proposal], your phrase as its heading.
- **F10** — Which consolidated vision document rules (grounded
  questions Q8) — this standard cites only your logged rulings, but
  the two vision documents disagree on stream anatomy, which touches
  F5.

Q1–Q8 of reports/ProtosEngineGroundedQuestions-2026-08-08.md remain
open alongside these; nothing in this draft answers them for you.
