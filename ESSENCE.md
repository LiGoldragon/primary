# ESSENCE

*The intent that shapes the work. Upstream of every other document.
Where a downstream rule conflicts with this, this wins.*

> Read this before any other document.

---

## Intent

The point of the work is to build software that is **eventually
impossible to improve** — in a bounded domain, the right shape,
chosen carefully, observed cleanly.

What I hold, in priority order:

1. **Clarity** — the design reads cleanly to a careful reader. The
   structure of the system is the documentation of itself.
2. **Correctness** — every typed boundary names exactly what flows
   through it; nothing accidental survives the type system.
3. **Introspection** — the system reveals itself to those building
   it. State is visible; derived values do not hide; what's
   happening at any moment is observable from outside.
4. **Beauty** — beauty in the operative sense: not pretty, but
   right. Ugliness is evidence the underlying problem is unsolved.

When two conflict, the earlier wins.

## What I am not optimising for

Not speed. Not feature volume. Not "minimum viable," "ship fast,"
"iterate later," "time to market." The right shape now is worth
more than a wrong shape sooner; unbuilding a wrong shape costs more
than the speed it bought.

Not backward compatibility for systems being born. Until a
compatibility boundary is declared, the system is being shaped, not
preserved.

Not estimates. Implementation timelines do not appear in design
discussions. Work is described by *what it requires*, not by *how
long it will take*.

---

## Beauty is the criterion

If it isn't beautiful, it isn't done. Ugly code is evidence the
underlying problem is unsolved. The aesthetic discomfort *is* the
diagnostic reading. When the right structure is found, the
ugliness dissolves: special cases collapse into the normal case;
repetition resolves into a single named pattern.

When something feels ugly, slow down and find the structure that
makes it beautiful. **That structure is the one you were missing.**

If you cannot make it beautiful, you do not understand it yet.

Diagnostic readings — each is a *signal*, not a sin. Notice it;
decide what the underlying problem is; fix the underlying problem:

- A name that does not read as English.
- A free function that should be a method.
- A `pub` field on a wrapper newtype.
- A boolean parameter at a call site (`frob(x, true)`).
- A name for what something is *not* (`non_root`, `not_admin`).
- Special cases stacked on the normal case.
- Stringly-typed dispatch — `match name.as_str()` over cases that
  should be a closed enum.
- Dead code retained "for safety" or "for backward compatibility."
- A doc comment that explains *what* the code does (well-named
  code already explains what; the comment signals the names
  aren't carrying their weight).
- A long function with multiple responsibilities.

---

## Naming — full English words

Identifiers are read far more than they are written. Cryptic
abbreviations optimize for the writer (a few keystrokes saved) at
the reader's expense (one mental lookup per occurrence, forever).

**Default: every identifier is a full English word.**

`AssertOperation` over `AssertOp`. `Deserializer` over `Deser`.
`Configuration` over `Cfg`. `Token` over `Tok`. `Identifier` over
`Ident`. `Operation` over `Op`. `Buffer` over `Buf`. `Address`
over `Addr`.

**Name length is proportional to scope.** A 3-line loop counter
can be `i`. A module-level type that appears across the codebase
spells itself out.

Permitted exceptions, narrow and named:

- Tight-scope loop counters (<10 lines): `i`, `j`.
- Mathematical contexts where the math itself uses the symbol:
  `x`, `y`, `theta`, `lambda`, `n` for sample size.
- Generic type parameters with no semantic content: `T`, `U`,
  `K`, `V`, `E`. When the parameter has semantic content, give
  it a real name (`$Value`, `$Output`, `$Failure`).
- Acronyms that have passed into general English: `id`, `url`,
  `http`, `json`, `uuid`, `db`, `os`, `cpu`, `io`, `ui`, `tcp`.
- Names inherited from `std` or well-known libraries: `Vec`,
  `HashMap`, `Arc`, `Box`, `Mutex`, `mpsc`, `regex`. Don't rename
  these; **don't extend the abbreviation pattern to your own
  types.**
- Domain-standard short names already documented at the project
  root.

Two scarred anti-patterns:

- **"Feels too verbose."** The full English form reads as
  English. The abbreviation reads as ceremony to be decoded. The
  cost of mis-naming is paid every time the name is read; the
  benefit of saving three keystrokes is paid once. The verbosity
  feeling is inherited prejudice from constraints that no longer
  apply (6-char FORTRAN, 80-column cards, 10-cps teletypes).
- **A name for what something is not.** Negative names compose
  poorly and read as denial. Find the positive name.

Two different things always have different names. `$LeftValue`
and `$RightValue` are different even when they share qualities;
*name is identity*.

---

## Behavior lives on types

Every reusable verb belongs to a noun. Free functions are for
things that genuinely belong nowhere else: a binary's `main`, a
small private helper inside one module, a relational operation
between two values of equal status (typically expressed via
operator overloading, which IS a method on a type with operator
syntax).

Free functions are *incorrectly specified verbs*. They encode an
action without naming the noun that owns it. When the temptation
to write one appears, slow down and find the noun — the type that
has the affordance the verb describes. If no obvious noun exists,
the model is incomplete; the missing type is what the verb is
asking you to declare.

The rule's purpose is not what it makes you write. It is what it
makes you do *before* you write. The forced invention of the type
that should own the behavior is the load-bearing cognitive event.

The rule has a sharper version: the verb belongs to **the right**
noun, not just any nearby noun. Adjacency of types is not the
same as adjacency of concerns. When two crates / two types / two
modules have similar surface (touch the same data, have similar
names) but different concerns, the verb goes with the concern,
not with the surface.

Companion form: a wrapper newtype's wrapped field is **private**.
A `pub` field defeats every reason to wrap. The type owns its
representation — construction with validation goes through
`TryFrom` / `from_str`; access goes through `AsRef`. A `pub`
field makes the type a label, not an abstraction.

A type whose only `impl` block is a parking lot for functions
that do real work on data they don't carry is a free function in
namespace clothing. The verb got attached to a fake noun. Step
back; find the noun whose data the verbs read or write. That
type may not exist yet — invent it.

---

## Polling is forbidden

When a system needs information from another system, that
information arrives by **subscription**, not by repeated
asking. The producer pushes; the consumer subscribes; the
information flows when there is information to flow.

**Polling — repeatedly asking "did anything change?" on a
clock — is forbidden.** Not "discouraged." Not "avoid where
practical." Forbidden.

The mental image: polling is the partner who keeps texting
when there's been no answer. The lack of an answer is the
answer. Sending again every N seconds doesn't change the
state of the world; it adds noise to it. Real systems
behave the same way. When a producer has nothing to say,
the right thing is to wait until it does. Asking
repeatedly is harassment, not communication.

Why polling is the wrong shape:

- **Latency.** Worst-case latency *N* between event and
  reaction, for a poll interval *N*.
- **Resource burn.** Most polls are no-ops; the work is
  wasted before the loop body runs. Systems that poll
  degrade under no real load.
- **Fake change-detection.** Two consecutive snapshots
  being identical doesn't mean nothing happened — only
  nothing visible to the consumer's projection.
- **Pacing leak.** Polling encodes the consumer's pacing
  into the producer's protocol.
- **Pattern lock-in.** Once polling is in a codebase,
  agents (human and LLM) reach for it again. Forbidding
  it once stops the multiplication.

Producers expose a **subscription primitive** — register a
callback, open a stream, accept a long-lived RPC, watch a
file via inotify, hold a Unix socket. Consumers subscribe
once and receive events indefinitely.

### When the producer can't push yet

If the producer cannot yet push, the dependent feature
**defers** rather than falls back to polling. A poll "for
now" never gets removed.

The right response is to sit down and figure out *why* the
producer can't push, and either:

- Build the subscription primitive in the producer.
- Replace the producer with one that can push.
- Accept that the dependent feature waits until push lands.

If none of these resolve the case at hand, **escalate** —
to the next level of design responsibility, and ultimately
to the human. **Until a named rule exists for a specific
class of "can't push" cases, that class escalates rather
than falls back to polling.**

Escalation is the correct outcome when no push answer is
found. It is not a failure mode; it is the discipline
working. The wrong outcome — falling back to a poll — is
never the answer.

### Named carve-outs — explicit, narrow

Three patterns look polling-shaped but aren't, because the
contract isn't "what changed?":

- **Reachability probes.** "Is service X alive?" is
  transport-layer reachability, not state-change detection.
  The contract is "are you alive," not "what changed."
- **Backpressure-aware pacing.** A consumer drains its own
  buffer at its own rate; the producer still pushes. This
  is flow control.
- **Deadline-driven OS timers.** A `timerfd` or equivalent
  fires when a wall-clock deadline arrives; the kernel
  pushes the wake. Used for TTLs, expirations, scheduled
  actions. The contract is "wake me at this deadline," not
  "tell me what changed."

These three are the complete list. Anything else that
looks polling-shaped is polling — escalate.

---

## Perfect specificity at boundaries

Every typed boundary names exactly what flows through it. No
wrapper enums that mix concerns. No string-tagged dispatch. No
generic-record fallback. No `Unknown` variant that means "we did
not model this yet." The type system is the model, not just the
validator.

Errors are **typed enums per crate**. Structured variants carry
the data needed to render a useful message. Foreign error types
convert via `#[from]`. **Never** `anyhow`, `eyre`, or
`Result<T, Box<dyn Error>>` — they erase the error type at the
boundary, which loses the typed-failure discipline the rest of
the rules build up. Callers can no longer pattern-match on what
went wrong.

**One object in, one object out.** Method signatures take at
most one explicit object alongside `self` and return exactly one
object. When inputs or outputs need more, define a struct.
**Anonymous tuples are not used at type boundaries** — not as
return types, not as parameter types, not as struct fields. The
single allowed form is a tuple newtype, which is a named type.

**Domain values are types, not primitives.** A content hash is
not a `String`. A node name is not a `String`. A file path used
as an identifier is not a `Path`. If a value has identity beyond
its bits, it gets a newtype.

**One type per concept.** No `Item`/`ItemDetails` companions, no
`-Info` / `-Extra` / `-Meta` / `-Full` / `-Raw`/`-Parsed` pairs.
Pairs of types around one suffix are one concept fragmented
across two because the base was designed too thin. Fix the base.

---

## Micro-components

Every functional capability lives in **its own independent
repository** with its own build descriptor and its own test
suite. Components communicate only through typed protocols, never
shared mutable state. Each component is sized so that **the
entire component, including tests, fits comfortably in a single
LLM context window** (≈3k–10k lines, ≈30k–80k tokens).

**Adding a feature defaults to a new crate, not editing an
existing one.** The burden of proof is on the contributor (human
or agent) who wants to grow a crate. They must justify why the
new behavior is part of the *same capability* — not a new one.
The default answer is "new crate."

The boundary is **filesystem-enforced**; nothing else holds.
Module-level boundaries inside one crate decay under deadline
pressure into shared internals — the "modular monolith" failure
mode.

The historical record on monolith collapse is unambiguous
(Parnas 1972 onward); the LLM-context argument is contemporary:
codebases grow faster than context windows; the fix is components
small enough that the whole component fits.

Each component carries its own architecture document at the root,
its own test suite, and its own version pin. Cross-component
references happen at two layers: locally as build-system inputs
during development; via published version pins once stable.
**Never** cross-crate `path = "../sibling"` in a manifest — that
assumes a layout a fresh clone won't reproduce.

---

## Skeleton-as-design

New design lands as **compiled skeleton code** — type
definitions, trait signatures, `todo!()` bodies — in the relevant
repo, not as prose blocks claiming "here's what the type would
look like." The type system enforces the shape; prose decays the
moment implementation lands.

Reports describe shapes, not implementations. Their medium is
**prose plus visuals** — diagrams, swimlanes, flowcharts, tables,
dependency graphs. Implementation code in a design doc goes
stale the moment it lands and the real type drifts; readers
cannot tell whether the report's snippet or the code's actual
type is authoritative; visual shapes carry the same information
without that freshness trap.

The narrow allowance: a few-line *sample* of the surface the
design talks about — a snippet of a config showing its shape, a
one-line invocation, a single field declaration to anchor a name
— is fine. The rule is about implementation blocks, not about
showing the shape of the thing the design is about.

---

## Positive framing

State what IS. Architecture docs and agent rules describe the
system's commitments — what kinds exist, what owns what, what
flow happens, what the agent does. The current shape lives in
the doc; the path that led there lives in version-control
history.

When a direction turns out to be wrong, the doc is rewritten to
state the new direction. The previous direction disappears from
the doc; the commit history preserves it for anyone who needs to
recover the path.

When an option is excluded — by constraint, preference, or
decision — the criterion that excludes it is stated as a positive
requirement. "Must be Rust" replaces "Go is excluded." The
candidates that satisfy the criteria appear in the doc; the
others stay silent.

Each architectural commitment lives **once**, positively, in the
appropriate canonical doc. Cross-references flow into
architecture from reports; reading lists, decision histories,
type-spec details live in reports.

---

## Efficiency of instruction

Each rule, principle, or pattern lives in **one canonical
place**. Other docs cite by reference; they don't restate.
When a rule starts to appear verbatim in multiple docs, that's
a smell — find the canonical home and trim the others.

The cost of duplication is paid every time a reader has to
reconcile two slightly-different versions of the same idea.
Instructions to agents should be efficient: short, focused,
precise; cross-referenced rather than copied. The reader's
attention is the resource being optimized.

This applies at every layer:

- **Upstream wins.** ESSENCE is upstream of `lore/AGENTS.md` is
  upstream of skills is upstream of tool reference is upstream
  of per-repo `AGENTS.md` / `ARCHITECTURE.md` / `skills.md`.
  Higher layers state principles; lower layers cite them.
- **Lore is *what* the tool does. Skills are *how* we use it
  and *when* we pick it.** Don't restate one in the other;
  point.
- **A brief pointer beats a full-text restate.** If a doc
  needs to invoke a rule, naming it and pointing at the
  canonical home is enough.
- **An agent should never have to choose between two versions
  of the same rule.** If they do, that's the bug to fix —
  consolidation, not arbitration.

When in doubt about where a new rule lives: ask which doc's
*role* it fits. If it's intent (the deepest "why"), it's
ESSENCE. If it's how-to-act-as-an-agent, it's a skill. If it's
how-the-tool-works, it's lore. If it's repo-specific intent
or invariants, it's that repo's `skills.md`. If a rule fits
two roles, it fits one of them better — pick that one and
have the other point at it.

---

## Choosing a data format

Three orthogonal questions: **for whom, for what, for how long.**

**For a human, to read or write — a positional, typed text
format.** No keywords beyond truth values. Field names live in
the schema, not the text. PascalCase for types, camelCase for
instances. Delimiter-first, first-token-decidable parsing. Every
value structured: no opaque strings; if a name or type is stored
as a flat string, the ontology is incomplete.

**For a machine, on the wire or on disk — a binary contract with
zero-copy reads.** Content-addressable by canonical encoding
(hash of canonical bytes is identity). Cross-platform feature
pin (little-endian, fixed pointer width, unaligned-read-safe).
Schema fragility is the price; a known-slot version-skew guard
checked at boot, hard-fail on mismatch. Schema changes are
breaking changes, coordinated upgrades.

**For an embedded transactional working set — an embedded
key-value store.** No separate server. Single-file or
directory-tree durability. Snapshot reads. Crash-consistent.

**For tracked items with audit history — git-for-data.** When
the unit being tracked is short, structured, and benefits from
branchable history (issues, tasks, workflow markers), use a
git-versioned database. Designs and long-form prose live in
files; the database summarises and points at the file. Long
prose in a `--description` field is the wrong storage.

The choosing principle: **identify the canonical state-shape for
the thing; pick the format whose semantics match that shape.**
Resist using one format as the universal currency. Each format
earns its place by matching one specific kind of thing.

Identity is the hash of canonical bytes. Mutable handles
("slots") provide follow-this-thing semantics on top of the
immutable identity — content edits update a slot's binding
without rippling rehashes through dependents.

---

## Language-design instincts

Whenever a notation is being designed (text format, request
language, schema notation, query surface), these are the
load-bearing commitments:

- **Delimiter-first.** Every construct has explicit opening and
  closing delimiters. The parser knows what it is reading from
  the first token. No fallback rules. No multi-token lookahead.
- **No keywords.** Closed sigil budget. New features land as new
  delimiter-matrix slots or PascalCase records, not as new
  sigils.
- **Position defines meaning.** The same delimiter means
  different things in different contexts. The parse position is
  the sole authority.
- **PascalCase = compile-time structural; camelCase = instance.**
  The parser dispatches on first-character case. This is not
  convention — it is syntax.
- **Names are meaningful.** No pointer names (`T`, `X`, `n`,
  `tmp`, `buf`). Every name describes what the thing IS.
- **Every value is structured.** If a name or type is stored as
  a flat string, that is a bug. As the ontology grows, strings
  collapse to typed domain variants.
- **Newlines are not significant.** Parsing is purely
  token-based.
- **Text is flat; trees come from the compiler.** Grammar rules
  stay flat; structure lives in the compiler's data tree.
- **Content-addressing by canonical encoding.** Identity is the
  hash of canonical bytes; the canonical form is itself defined.
- **No shortcuts in compiler work.** No raw-text passthrough. No
  "skip for now" stubs. No partial grammars. When hitting a
  language limitation, extend the language properly; don't work
  around it.
- **The parser stays small.** Adding new typed kinds is the
  central activity of evolving the schema; adding new parser
  rules is the rare activity. New syntactic territory becomes a
  new DSL surface, not parser logic.

These instincts emerged in language-design exploration that did
not, itself, ship; refined, they live in the data formats and
request languages currently in use. The instincts are the
heritable substance.

---

## Version control: always push

After every meaningful change, push immediately. **Blanket
authorization** — proceed without asking for confirmation.

Push per logical commit. Unpushed work is invisible to other
machines and to anyone consuming the repo as an input. Forgotten
pushes cause divergence and surprising forks.

Commit messages are short. A short verb plus scope; the repo is
implicit (the commit lives in the repo). Detail lives in the
diff and the report.

If a single change touches multiple repos, each repo gets its
own short commit.

---

## Documentation layers

| Where | What lives there |
|---|---|
| Source code | Implementation — types, tests, build files. Type sketches as compiler-checked skeletons. |
| `ARCHITECTURE.md` at the repo root | This repo's role, owned-and-not-owned boundaries, code map, invariants. ~50–150 lines. |
| `reports/<n>-<topic>.md` | Decision records, design syntheses, audit findings, end-of-session snapshots. Prose plus visuals. |
| Workspace-wide `AGENTS.md` | Cross-cutting guidance agents read first. The canonical contract. |
| Per-repo `AGENTS.md` | Thin shim plus the repo's role and carve-outs. |
| `CLAUDE.md` | One-line shim: *"You MUST read AGENTS.md."* Lets agents who only read `CLAUDE.md` and agents who only read `AGENTS.md` converge on a single source of truth. |

When a report contains durable substance, move it to the right
home rather than leaving it in `reports/`.

---

## How agents apply this

**Intent first, rules second.** The intent above is upstream of
every rule below. When a rule and the intent conflict, the intent
wins; the rule gets rewritten.

**Slowness is information.** When a rule's question is hard —
what type owns this verb, what is the right name, why does this
feel ugly — that hardness is a signal. The signal is that the
model of the problem is not yet fully formed. Don't paper over
the gap with a free function or a string; slow down and find the
structure.

**Never delegate understanding.** When prompting another agent
or invoking a tool, the prompt proves you understood: file paths,
specifics, what to change. Phrases like "based on your findings,
fix the bug" push synthesis onto the other side instead of doing
it yourself.

**State assumptions explicitly.** When a fact is load-bearing,
state it. When something is uncertain, state that. Hidden
assumptions are how plausible-looking work breaks invariants the
author cannot see.

**Verify each parallel-tool result.** When batching tool calls,
scan each result block for errors before any follow-up step. The
bundle returning is not the same as the bundle succeeding.

**Working directory matters.** Carry the working directory in
the prompt; don't assume context. Agents start cold every time.

---

*End ESSENCE.*
