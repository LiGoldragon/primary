# Skill — NOTA-as-comments

*Code comments use NOTA-formatted signal records. The comment lives
in code (which is text), so the signal is in text form. Each
meaningful edit carries a `(Why …)` record naming the rationale; the
accumulated whys become machine-readable design history that Mind
can index and agents can audit before making conflicting edits.*

## What this skill is for

A code comment can be free-form prose, or it can be a typed signal
record encoded in the workspace's typed text language.
The discipline says: when the comment names *why an edit was made*,
write it as a positional NOTA record opened with `(Why "…" …)`.

The frame: a signal record can be encoded as bytes (rkyv), as a
NOTA string, or as text inside a comment. The third form is **the
same signal**, just sitting where the surrounding context is source
code rather than a wire frame or a `.nota` file. CLI and comment
surfaces use NOTA because they are text edges. Daemon startup,
configuration, and peer traffic stay binary signal/rkyv (per
`skills/component-triad.md` §"The one argument rule"). The comment
uses NOTA-in-text because the file *is* text; NOTA is the encoding
that fits.

Two payoffs:

- **Mind reads code-as-signal.** Once persona-mind ships its
  code-indexing surface, a `(Why …)` comment is a queryable typed
  record — not a free-text blob that needs natural-language parsing.
  Auditor reads the same records to surface design-decision history;
  agents read prior whys before making conflicting edits.
- **The why lives next to the code.** A report says *"the recovery
  path now flips state"*; the report retires; the code outlives the
  report. A `(Why …)` comment on the function records the same
  decision where the code lives, so future agents see the rationale
  the moment they read the function — without chasing a report
  number that may have been deleted.

Pairs with: `skills/nota-design.md` (positional records, no labeled
fields), `skills/intent-log.md` (intent vs why — see §"`Why` vs
intent records" below), `skills/reporting.md` (why-in-comments
replaces some report content; the report names the bigger arc, the
comment names the per-edit rationale).

## The shape — `(Why …)` is the canonical opening

The comment opens with `(Why "<short summary>" …)`. After the
summary, positional fields name the surrounding context: what caused
the edit, what alternatives were considered, what the choice rests
on. The record is positional per `skills/nota-design.md` — type
first, fields in declared order, no labeled fields, no
`(key value)` pairs.

The exemplar:

```rust
// (Why "fix recovery path on transient failure"
//   (caused-by "operator/162 §Remaining Work item 4")
//   (alternatives-considered (RetryWithoutFlip ColdStart))
//   (chosen-because "preserves no-downtime precedent per intent 203"))
fn handle_completion_failure(&mut self) -> Reply {
    // ... implementation
}
```

The summary is a short one-line phrase — the rephrasing Mind will
index. The bracketed sub-records name structured context:

- `(caused-by "<trigger>")` — what occasioned the edit (a report, a
  bug, a peer's audit, a psyche intent).
- `(alternatives-considered (Variant1 Variant2 …))` — the closed set
  of approaches the editor weighed. PascalCase variants, named so
  later agents can search "did anyone consider `ColdStart` here?"
- `(chosen-because "<rationale>")` — the why-of-the-why; cites
  intent records or prior decisions when they are load-bearing.

The sub-records are themselves NOTA records — positional, typed.
The same grammar facts from `skills/nota-design.md` apply: bare
PascalCase tokens at variant positions, strings quoted, no labeled
fields.

## Multi-line comments aggregate into one record

A `(Why …)` record spans as many comment lines as it needs; the
parser concatenates the comment payload across consecutive `//`
lines (Rust) or `#` lines (shell, Nix, Python). Indentation inside
the comment block is whitespace and ignored by the NOTA reader.

Rust:

```rust
// (Why "rename signal-core to signal-frame"
//   (caused-by "intent record 142 — signal-core was confusing as a name")
//   (alternatives-considered (SignalCore SignalFrame SignalSpine))
//   (chosen-because "frame matches the wire shape vocabulary"))
pub struct Frame { /* ... */ }
```

Nix / shell (`#` comment style):

```nix
# (Why "pin persona-spirit before persona-mind in deploy order"
#   (caused-by "operator/161 §3 — mind queries spirit at startup")
#   (alternatives-considered (PinSpiritFirst PinMindFirst RunBoth))
#   (chosen-because "mind needs spirit's wire shape resolved first"))
persona-mind = { after = [ "persona-spirit.service" ]; };
```

Python (`#` comment style — identical shape):

```python
# (Why "early-return on empty payload"
#   (caused-by "designer/255 §audit finding 4")
#   (alternatives-considered (EarlyReturn DefaultZero LogAndContinue))
#   (chosen-because "downstream cannot distinguish zero from absence"))
def process(payload: bytes) -> Result:
    if not payload:
        return Reply.Empty
    # ...
```

The comment-prefix character (`//`, `#`) is language-syntax noise
the indexer strips; the NOTA record is what survives.

## Where the `(Why …)` goes

- **On a function** — opening lines above the `fn` signature. The
  rationale shapes the whole function; readers see the why before
  the implementation.
- **On a type** — opening lines above `struct` / `enum` / `trait`.
  The why explains the shape; readers see it before the field
  layout.
- **On a tricky line or block** — immediately above the relevant
  expression. The why explains the local choice; readers see it
  with the code it shapes.
- **On a module** — first lines of the file (after the file-header
  comment if any). The why explains the module's existence; readers
  see it before any of the module's items.

The discipline: the `(Why …)` sits where the next reader will see it
the moment they look at the code it describes. A function's why is
above the function, not at the top of the file; a struct's why is
above the struct, not next to the first field.

## `Why` vs intent records — the boundary

Both `(Why …)` comments and Spirit intent records carry "why-ness,"
but they live at different layers:

- **Intent records (Spirit)** — *what the psyche stated.* The
  author's voice on a topic, captured verbatim. Records are typed
  (Decision / Principle / Correction / Clarification / Constraint)
  and stored in the Spirit redb db. See `skills/intent-log.md`.
- **`(Why …)` comments** — *the editor's per-edit rationale.* An
  agent or operator made an edit; the comment records why this
  particular code shape was chosen. The why may *cite* an intent
  record (`(chosen-because "preserves no-downtime precedent per
  intent 203")`) but is not itself an intent record.

The psyche says intent and Why are related but not the same. The
boundary, working rule:

- A psyche statement that classifies as Decision / Principle /
  Correction / Clarification / Constraint goes to Spirit. The agent
  captures it with the spirit CLI. The intent record is the
  authoritative source.
- An editor's choice while making an edit — *why I picked this
  variant, what alternatives I considered, what prior decision I'm
  honoring* — goes in the `(Why …)` comment next to the code. The
  comment is the editor's witness, not the psyche's voice.

When the editor's choice rests on a psyche intent record, the
`(chosen-because …)` field cites the intent record by topic + record
number. The two layers are linked but separate; the cite is the
link.

A precise statement of the boundary is still being worked out — the
psyche says intent and why are related but not the same. Capture the
ones you're sure about; surface gaps to the psyche per
`skills/intent-clarification.md`.

## Mind integration — code-as-signal

Once persona-mind ships its code-indexing surface, the NOTA-comment
discipline pays off. The hooks:

- **A code-indexer tool walks repos and parses `(Why …)` records out
  of comments.** The parser is the same NOTA codec already used for
  wire frames and `.nota` files; the comment-prefix strip is the
  only difference.
- **Mind stores the records as typed memories.** Each `(Why …)`
  becomes a memory keyed by `(repo, file, line-range)`. Queries:
  "what whys cite intent record 203?", "what alternatives were
  considered for the recovery path?", "show me every function whose
  why mentions `RetryWithoutFlip`."
- **Auditor reads the indexed whys.** When the auditor (per
  `AGENTS.md` §"Possible additional role — auditor") sweeps a
  repo, it reads the whys to surface decision history before
  flagging a flaw. If a flagged shape has a `(Why …)` that names the
  exact reason, the audit either reverses the flag or refines its
  finding to address the recorded rationale.
- **Agents read prior whys before making conflicting edits.** Before
  an agent rewrites a function, it queries Mind for the function's
  prior whys. If a prior why says *"chosen-because preserves
  no-downtime precedent per intent 203"*, the agent knows not to
  break that precedent without justifying the change.

The forward direction is full automation. Until persona-mind's
code-indexer lands, the whys still serve a smaller purpose: future
human and agent readers see them when they open the file. The Mind
integration is the upside, not the prerequisite.

## When a `(Why …)` is worth writing

Not every edit warrants one. The bar:

- **Substantive choice** — the edit picked one variant from several
  plausible alternatives; the choice would not be obvious to a
  reader who didn't watch the deliberation.
- **Citation needed** — the choice rests on an intent record, a
  prior decision, or a report that future readers need to know
  about.
- **Surprising shape** — the code looks one way for a non-obvious
  reason; without the why, a future agent might "fix" the
  surprising shape and undo the precedent.

Not worth a `(Why …)`:

- Routine renames where the new name is plainly better.
- Mechanical translation (typo fixes, simple refactors with no
  alternatives weighed).
- Code whose shape is immediately obvious from the surrounding
  context.

The test: *would a future agent benefit from seeing the why before
touching this code?* If yes, write one. If no, the comment is noise.

## What this skill is NOT for

- **Documenting what the code does.** That's what the code itself
  carries; doc-comments (`///` in Rust) explain the API. `(Why …)`
  is the rationale layer above the API doc.
- **Replacing reports.** Reports name the bigger arc — the multi-
  function design pass, the cross-repo synthesis, the audit. The
  `(Why …)` comment names the per-edit rationale at the code line.
  See `skills/reporting.md` for the report's role.
- **Replacing Spirit intent records.** Spirit captures the psyche's
  voice; `(Why …)` captures the editor's choice. See §"`Why` vs
  intent records" above.
- **A free-form prose comment with parentheses around it.** The
  `(Why …)` is a positional NOTA record per
  `skills/nota-design.md`; the same grammar rules apply. If the
  prose doesn't fit positional NOTA, write it as an ordinary prose
  comment without the `(Why …)` wrapper — don't dress a free-text
  comment in fake NOTA.

## Forward — syntax-highlight integration

NOTA-syntax-highlighting inside code comments is a future
integration. The deployed editor highlighters understand the host
language's comment-prefix; making them also dispatch to the NOTA
highlighter for the comment body is a separate piece of work.
Tracked here as a deferred item — the discipline lands without the
highlight; the highlight is the polish.

## See also

- `skills/nota-design.md` — positional-record discipline. Every
  `(Why …)` follows the same rules: positional, no labeled fields,
  PascalCase enum variants, no tag on a single-shape struct.
- `skills/intent-log.md` — Spirit intent records (the psyche's
  voice). The `(chosen-because …)` field of a `(Why …)` can cite
  intent records; the boundary between why and intent lives here.
- `skills/reporting.md` — reports name the bigger arc; whys name
  the per-edit rationale. Comments and reports complement each
  other; whys do not replace reports.
- `skills/component-triad.md` §"The one argument rule" — where NOTA is
  the workspace text-edge argument language, while daemon startup and
  peer traffic remain binary.
- `AGENTS.md` §"Possible additional role — auditor" — the auditor
  reads accumulated whys; one of the integration hooks above.
</content>
</invoke>
