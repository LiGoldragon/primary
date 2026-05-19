# 238 — Signal architecture redirection: contract-local verbs

*Broad direction report for any agent picking up signal-type
work. The psyche has redirected the architecture: public verbs
are now contract-local — they describe the client's domain
action — while the six former universal verbs (Assert / Mutate
/ Retract / Match / Subscribe / Validate) become Sema-engine
execution vocabulary in a new layer called `signal-sema`. This
is a substantive break that will touch signal-core, the
`signal_channel!` macro, and every existing contract crate.
The psyche has accepted that the implementation churn is real
and worth paying. Read this report first; the supporting
analysis lives in `reports/designer-assistant/125-v2-contract-local-verbs-vs-sema-core-verbs.md`.*

## 0 · TL;DR

The new model:

```
Layer 1 — Frame / exchange mechanics
    handshake, async ids, length-prefixed rkyv bytes
    (probably stays in signal-core, narrowed)

Layer 2 — Contract operations (PUBLIC)
    each signal-<component> defines its own verbs
    in domain-verb form — Query, Submit, Configure,
    Register, State, Observe, etc.

Layer 3 — Sema operations (INTERNAL)
    the daemon translates contract operations into
    sequences of Sema operations (Assert / Mutate /
    Retract / Match / Subscribe / Validate)
    against the daemon's typed state.
    A new crate signal-sema owns this vocabulary,
    and a component speaks signal-sema on the wire
    only when it is explicitly exposing typed-table
    operations (e.g. sema-engine introspection).
```

Concretely on a wire:

```
WAS:    (Match (RecentRepositoriesQuery None 20))
IS NOW: (Query (RecentRepositories None 20))

WAS:    (Assert (MessageSubmission ...))
IS NOW: (Submit (Message ...))

WAS:    (Mutate (Configure (DaemonConfiguration ...)))
IS NOW: (Configure (DaemonConfiguration ...))
```

The client sends what it's doing in domain terms. The daemon
internally decides what Sema operations that translates into,
or whether it translates into Sema operations at all (a Submit
might result in zero Sema ops if rejected, many Sema ops if
accepted, or a forwarded request).

## 1 · Why this is the right shape

Three failure modes have surfaced in the universal-six-verbs
model:

**Grammatical incoherence at the wire.** *"Mutate Configure"*
reads as "perform a mutation operation on a configure
operation." You mutate nouns, not verbs. *"Retract Retire"* has
the same problem. The current owner-contract precedent is not
a precedent — it's the same disease in a less obvious form.

**Mis-naming the client's action.** When an agent submits a
message, the public act is "submit"; whether the daemon writes
one row, many rows, mutates delivery state, forwards to
another daemon, or rejects without storing is downstream of
the public action. Forcing `Assert MessageSubmission` at the
wire pre-commits to a state-effect that may not happen.

**Repeated category words across siblings.** Five `Match
*Query(*Query)` siblings in `signal-repository-ledger` told us
that `Query` is a missing public layer. /124 proposed making
Query a parent payload enum *under* Match. The deeper
correction: Query IS the contract verb. Match is what the
database does internally; Query is what the agent asked for.

## 2 · The three layers in detail

### Layer 1 — Frame mechanics

Stays minimal and domain-free. What `signal-core` owns:

- The `Frame` envelope (length-prefixed rkyv archive).
- Handshake + protocol version + exchange identifiers.
- Async correlation, streams, reply mechanics.
- The `Operation<Payload>` and `Request<Payload>`
  shape — but `Operation` no longer carries a `SignalVerb`
  enum at the universal layer. The operation IS the contract
  verb directly.

What `signal-core` no longer owns:

- The `SignalVerb` enum (Assert / Mutate / etc.) — moves to
  `signal-sema`.
- The Sema-execution coupling that the current macro encodes.

### Layer 2 — Contract operations (public, per-contract)

Each `signal-<component>` defines its own operation roots. The
verbs are domain verbs in their **verb form** (not noun form):

| Contract | Public verbs (examples) |
|---|---|
| `signal-repository-ledger` | `Query`, `Observe`, `Receive` |
| `signal-persona-message` | `Submit`, `Deliver`, `Acknowledge` |
| `signal-persona-spirit` | `State` (psyche stating intent), `Record` (typed intent), `Observe` |
| `signal-persona-orchestrate` | `Assign`, `Revoke`, `Handoff` |
| `owner-signal-<X>` | `Configure`, `Register`, `Retire`, `Start`, `Stop` |

Naming rule (correction to the prior `Statement`/`Submission`
shape): the leading word is the **verb form**, never the noun
form derived from the verb. `State` not `Statement`. `Submit`
not `Submission`. `Observe` not `Observation`. `Register` not
`Registration`. The payload that follows the verb may be a
noun (e.g., `(Register (Registration name ...))`) — but the
operation root is always the verb.

### Layer 3 — Sema operations (internal, in `signal-sema`)

The six former universal verbs live here. `signal-sema` is the
contract for **speaking directly to the Sema engine**:
introspection, replay, debugging, multi-step queries. It is
itself a contract crate (one among many), not a privileged
universal layer.

Components consume `signal-sema` as a library when they need
to express their internal state effects in typed terms (for
logging, introspection, replay, transactional commit). A
component *speaks* `signal-sema` on the wire only when it
explicitly exposes Sema-shaped operations to peers — most
components don't.

## 3 · Cross-contract verb reuse

Same verb name across different contracts carries different
semantics. *"if you tell a cloud to fall, or if you tell a
bird to fall, they're going to have different reactions."* The
verb is contract-local; meaning is dispatched on the receiver.

Examples of legitimate reuse:

- `Observe` on `signal-repository-ledger` = "watch for ledger
  events"; on `signal-persona-spirit` = "query intent records."
- `Register` on `owner-signal-repository-ledger` = "register a
  repository"; on `owner-signal-persona-router` = "register a
  delivery lane."
- `Configure` is universal across every owner contract — same
  word, different effect per daemon.

Agent reasoning about an operation must include the receiver
context, not just the verb name. The macro and codec layer
should not pre-presume that a verb name means the same thing
across crates.

## 4 · Naming inside this model

Three rules, applied together:

1. **Spell every identifier as a full English word.** (Workspace
   rule; `ESSENCE.md` §"Naming".) Unchanged.
2. **Names don't carry their full ancestry.** (Workspace rule.)
   Unchanged. `signal-persona-spirit`'s domain is intent;
   types inside it do not prefix `Intent`.
3. **Contract verbs are verbs, in their verb form.** New rule.
   `State` not `Statement`. `Submit` not `Submission`. `Observe`
   not `Observation`. Apply this when an operation root names
   the client's action.

The fourth rule from skills/naming.md — *"repeated category
words across sibling names are schema smells"* — is now
sharpened: the repeated word is usually a missing **public
verb**, not just a missing parent payload enum. The prescription
changes accordingly: lift the repeated word up to the operation
root, not into a payload-enum tier.

## 5 · What every component needs to do (broad)

This direction touches every contract crate. The broad work
items per affected crate:

### `signal-core`

- Remove `SignalVerb` enum and its verb-tagged macro
  declarations.
- Redesign `signal_channel!` so request variants declare
  `operation` (contract-local), not `verb variant`.
- Retain frame mechanics, handshake, exchange identifiers,
  async correlation, streams, reply plumbing.

### `signal-sema` (new crate)

- Owns `SemaOperation` (the six former universal verbs).
- Owns the typed-table execution vocabulary.
- Becomes a contract crate like any other — components depend
  on it when they speak typed Sema operations internally
  (executor lowering, logging, introspection).

### `signal_channel!` macro

- New input shape: `operation <Verb>(<Payload>)`.
- Generates the contract's `Operation` enum, the `Request`
  wrapper, the codec, the frame plumbing — same outputs as
  before minus the verb-tagging machinery.
- Verb-to-Sema mapping (when static) is not encoded in the
  macro; if a contract publishes its Sema lowering, it does so
  in a separate declaration.

### Every `signal-<component>` and `owner-signal-<component>`

- Replace the verb-prefixed request variants with
  contract-local operation roots.
- Pick verb-form names per the naming rule.
- Audit for repeated category words; lift them to operation
  roots.
- Update consumers (the daemon, the CLI, any peer caller).

### Specific contracts in flight

- **`signal-repository-ledger`** — replace 5× `Match *Query`
  with `Query` operation root + nested read targets. Replace
  `*Listing` reply variants similarly.
- **`signal-persona-spirit`** — the operator's pending rename
  pass (drop `Intent*` prefixes) should now scale further:
  drop the `Assert PsycheStatement` / `Assert Entry` shape too.
  Use contract-local verbs: `State`, `Record`, `Observe`,
  `Watch` (subscriptions).
- **`signal-persona-message`** — when this lands, use
  `Submit` / `Deliver` / `Acknowledge`. Do not model message
  submission as `Assert`.
- **Owner contracts** — `Configure`, `Register`, `Retire`,
  `Start`, `Stop` become direct operation roots, not payloads
  under `Mutate`/`Retract`.

### `sema-engine` integration

- The engine still understands the six Sema operations
  (Assert/Mutate/Retract/Match/Subscribe/Validate) — that's
  unchanged at the typed-table level.
- The component daemon is the **lowering layer**: it accepts
  contract operations on its public socket and produces Sema
  operations against its `redb` tables internally.
- The lowering may be static (annotation: `Query lowers_to
  Match`) or dynamic (policy decides at runtime). Both shapes
  are valid.

## 6 · What gets superseded

The following prior decisions / reports / skill content is
now superseded by this redirection. Substance remains
recoverable via `jj` history.

- **`reports/designer-assistant/124-query-suffix-as-missing-schema-layer.md`**
  — proposed `Match Query(Query)` as a tree-shape fix. The
  parent-enum-under-Match move was correct as a stepping
  stone but is replaced by the contract-local-verb shape
  directly. The /124 analysis is still valuable as the
  diagnostic that surfaced the deeper question.
- **`reports/designer/237-signal-type-naming-and-schema-tree-investigation.md`**
  §"Are we underusing signal verbs?" — claimed verbs were not
  underused. Under the redirection, the question is reframed:
  verbs were **mis-located** at the public layer rather than
  the execution layer. Section needs revision.
- **`skills/naming.md` §"Anti-pattern: repeated category words
  across sibling names"** — uses `Match Query(Query)` as the
  worked example. The rule is still valid (repeated suffixes
  are still smells) but the prescription is now "lift to a
  contract verb," not "add a parent enum under the Sema
  verb." Worked example needs updating.
- **`skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb"** — the entire
  six-verb-spine framing at the public-contract layer is now
  wrong. Signal at the public layer speaks contract-local
  verbs; the database-language framing belongs in
  `signal-sema`-shaped docs. Major rewrite needed.
- **Intent records on "verb is state-effect label; variant is
  domain noun"** (the compromise I proposed earlier this
  session and was corrected on) — superseded by the records
  in `intent/component-shape.nota` 2026-05-19T19:30Z and
  2026-05-19T19:45Z.
- **Bead `primary-ojxq` (persona-spirit triad implementation)
  scope** — the operator's rename pass now extends further
  (drop `Assert`/`Match`/`Subscribe`/`Retract` wrapping;
  contract-local verbs throughout). The bead description
  should be updated to reflect the wider scope.
- **The planned signal-repository-ledger bead** (not yet
  filed) for /124's intermediate fix — called off. A new
  bead/report for the Candidate-C refactor is needed instead.

## 7 · Open architectural questions

These are the genuine open points the psyche should weigh in
on as implementation progresses. Surface them via direct
chat; not waiting on these blocks broad documentation.

1. **Does signal-core retain its name (narrowed to frame
   mechanics) or get renamed?** Current name conflates frame
   + Sema verbs; after the split, the frame-only kernel could
   still be called signal-core, or could be renamed to
   something like signal-frame, signal-kernel, or signal-wire.
2. **Does `signal_channel!` stay one macro, or split?** One
   macro that produces a contract-local operation root may be
   simpler than the current verb-tagged shape; alternatively,
   the macro could be split into a frame-mechanics macro and
   a contract-operation macro.
3. **Verb-to-Sema lowering: macro-declared or
   executor-resolved?** Some contract operations have
   straightforward Sema lowerings (Query → Match against
   indexes); others are runtime-policy decisions (Submit may
   Assert, Mutate, forward, or reject). The model needs a
   place to express both.
4. **Introspection across contracts** — without a universal
   verb spine at the public layer, what is the cross-component
   observation shape? `persona-introspect`'s subscription
   model already handles per-component event classes; the
   question is whether there's still a useful uniform
   introspection vocabulary at the Sema-effect layer.

## 8 · Implementation guidance for agents

If you're picking up signal-type work after this redirection:

1. Read this report first.
2. Read `reports/designer-assistant/125-v2-contract-local-verbs-vs-sema-core-verbs.md` for the architectural analysis behind the direction.
3. Query `intent/component-shape.nota` and `intent/naming.nota` for the underlying psyche statements.
4. Before designing a new contract's public verbs, ask: *what is the client doing in domain terms?* Pick the verb-form word for that action. The verb is the operation root; the payload is the noun.
5. Before reaching for `Assert` / `Mutate` / `Retract` / `Match` / `Subscribe` / `Validate` at the wire, ask: *am I describing what the client is asking, or what the daemon will do to state?* If the former, pick a contract-local verb. If the latter, the operation belongs in `signal-sema`, not in the component's public contract.
6. Cross-contract verb reuse is fine; verbs mean what the receiver does, not what the name presupposes universally.
7. When in doubt, surface to the psyche per `skills/intent-clarification.md`.

## 9 · References

- `reports/designer-assistant/125-v2-contract-local-verbs-vs-sema-core-verbs.md` — the architectural analysis that led to this redirection.
- `reports/designer-assistant/124-query-suffix-as-missing-schema-layer.md` — the diagnostic that surfaced the deeper question; the proposed intermediate fix is superseded but the analysis stands.
- `intent/component-shape.nota` — 2026-05-19T19:30Z and 2026-05-19T19:45Z records capture the psyche statements driving this redirection.
- `intent/naming.nota` — 2026-05-19T19:45Z record on verb-form-not-noun-form.
- `intent/workspace.nota` — 2026-05-19T19:45Z records on chat brevity, vague-question prohibition, agent-failure-as-guideline-failure, recent-intent-supersession, and bead-vs-report visibility.
- `ESSENCE.md` §"Backward compatibility is not a constraint" — applies; the cost of the wrong shape compounds.
- `skills/component-triad.md` §"The single argument rule" — unchanged; contract-local verbs still ride on the one-NOTA-argument-per-binary discipline.
- `skills/language-design.md` Rule 5 ("Names are meaningful") and Rule 6 ("Every value is structured") — apply directly; verb-form naming is downstream of these.
