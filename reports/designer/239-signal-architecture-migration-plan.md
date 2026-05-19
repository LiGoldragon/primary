# 239 — Signal architecture migration plan

*The agent-consumable migration playbook. Companion to
`reports/designer/238-signal-architecture-redirection-contract-local-verbs.md`
(the why and the what). This report carries the how: new repos
to depend on, per-component checklists, order of operations,
coordination points. If you maintain a signal-<component>,
owner-signal-<component>, or component daemon, this is your
guide.*

## 0 · TL;DR

Two new repos are being created at `github.com/LiGoldragon`:

| Repo | Role |
|---|---|
| `signal-frame` | Renamed from signal-core. Frame envelope, length-prefixed rkyv archives, handshake, exchange identifiers, async correlation, streams, reply plumbing. **No SignalVerb. No Sema verbs.** |
| `signal-sema` | New. Owns the six Sema operations: `Assert / Mutate / Retract / Match / Subscribe / Validate`. Consumed by daemons that need to express their internal state effects in typed terms. Speakable on the wire when a component explicitly exposes typed-table operations. |

Every `signal-<component>` and `owner-signal-<component>`
contract gets refactored:

- **Drop the SignalVerb tag** from every request variant.
- **Lift operation roots to contract-local verbs** in
  verb-form (English verb spelling, not noun-form).
- **Move verb-to-Sema lowering** into the daemon executor —
  not into the contract, not into the macro.
- **Add the universal observer hook** to enable
  introspection (subscription on the public socket).

The `signal_channel!` macro stays one macro but is modified:
input shape becomes `operation <Verb>(<Payload>)` without a
verb tag.

`signal-core` is deprecated. The old verb-tagged contract
shape is retired; the universal six-verb spine no longer
sits at the public-contract layer.

## 1 · What's changing — the model in one paragraph

The six former universal verbs (Assert / Mutate / Retract /
Match / Subscribe / Validate) describe what a Sema engine
does to durable state. They are database vocabulary. They
move down a layer: into `signal-sema`, consumed by daemons
when they express their internal state effects. The public
contract layer — what a caller speaks to a daemon — now
carries the **caller's domain action** in domain-verb form:
`Query`, `Submit`, `Configure`, `Register`, `State`,
`Observe`, etc. The daemon internally translates contract
verbs into Sema operations against its `redb` tables; that
lowering is daemon-executor work, not macro-static.

The full rationale lives in
`reports/designer/238-signal-architecture-redirection-contract-local-verbs.md`.

## 2 · New repos — what they contain

### `signal-frame` (renamed `signal-core`)

Owns:
- `Frame` envelope + length-prefix framing rule.
- Handshake + protocol version + version-skew guard.
- Exchange identifiers + async correlation primitives.
- `Operation<Payload>` and `Request<Payload>` (without
  SignalVerb).
- `NonEmpty<T>` for atomic operation sequences.
- Stream / subscription lifecycle primitives.
- Reply plumbing.
- The `signal_channel!` macro (modified for contract-local
  operations).

Does NOT own:
- The six Sema verbs.
- `PatternField<T>` if the read-algebra patterns belong with
  the verbs (likely).

### `signal-sema` (new)

Owns:
- `SemaOperation` enum: `Assert / Mutate / Retract / Match /
  Subscribe / Validate`.
- The typed-table execution vocabulary.
- `PatternField<T>: Wildcard | Bind | Match(T)` (the
  read-algebra primitives that pair with Match/Subscribe).
- ReadPlan<R> operators (`Constrain`, `Project`, `Aggregate`,
  `Infer`, `Recurse`) — these live inside `Match` /
  `Subscribe` / `Validate` payloads.

A component depends on `signal-sema` when it speaks Sema
operations internally (for executor lowering, logging,
introspection). A component *exposes* `signal-sema` on a wire
only when it explicitly publishes typed-table operations —
most components don't.

## 3 · Per-component migration checklist

For each `signal-<component>` / `owner-signal-<component>` /
daemon repo you maintain:

### A. Update Cargo dependencies

```toml
# OLD
signal-core = { git = "https://github.com/LiGoldragon/signal-core.git", branch = "main" }

# NEW
signal-frame = { git = "https://github.com/LiGoldragon/signal-frame.git", branch = "main" }
# Add signal-sema only if you speak Sema operations on the wire
# or use Sema operations internally for executor lowering / introspection:
signal-sema = { git = "https://github.com/LiGoldragon/signal-sema.git", branch = "main" }
```

### B. Update `signal_channel!` invocation

The macro's input shape changes — no more `SignalVerb`
prefixes on variants. Each variant declares `operation`
directly:

```rust
// OLD (verb-tagged variants)
signal_channel! {
    channel Ledger {
        request Request {
            Assert ReceiveHookNotification(ReceiveHookNotification),
            Match RecentRepositoriesQuery(RecentRepositoriesQuery),
            ...
        }
    }
}

// NEW (contract-local verbs)
signal_channel! {
    channel Ledger {
        operation Receive(HookNotification),
        operation Observe(Push),
        operation Query(Query),
    }
}
```

The macro generates the same outputs (`Operation` enum,
`Request` wrapper, `Frame`, `RequestBuilder`, codec impls)
minus the verb-tagging machinery.

### C. Audit operation root names — verb-form rule

Every operation root names the caller's action in **verb
form**. Not the noun derived from the verb.

| Wrong (noun-form) | Right (verb-form) |
|---|---|
| `Statement` | `State` |
| `Submission` | `Submit` |
| `Observation` | `Observe` |
| `Registration` | `Register` |
| `Configuration` | `Configure` |
| `Retirement` | `Retire` |

The payload that follows the verb is the noun the action
takes: `(Register (Registration name ...))` — Register is the
verb; Registration is the noun.

### D. Lift repeated category words to operation roots

If you have several variants that share a suffix or prefix,
the repeated word is your contract verb. Lift it up.

```rust
// Wrong — Query repeated as suffix across five variants
operation EventQuery(EventQuery),
operation RecentRepositoriesQuery(RecentRepositoriesQuery),
operation ChangedFileQuery(ChangedFileQuery),
operation CommitMessageQuery(CommitMessageQuery),
operation CatalogQuery(CatalogQuery),

// Right — Query is the contract verb; siblings name read targets
operation Query(Query),

pub enum Query {
    Events(EventSelection),
    RecentRepositories(RecentRepositorySelection),
    ChangedFiles(ChangedFileSelection),
    CommitMessages(CommitMessageSelection),
    Catalog(CatalogSelection),
}
```

### E. Move verb-to-Sema lowering into the daemon executor

The contract no longer declares which Sema verbs its
operations lower to. The daemon's executor decides at runtime
based on the operation, the payload, the daemon's policy
state, and any routing decisions.

> *"For a bird to lower itself, it changes the angle of its
> wings. But for a cloud to lower itself, it changes its
> temperature."* Same verb, different effect per receiver.

Concrete: an operation handler in the daemon takes the
contract operation, computes the Sema-operation sequence (or
the policy decision that no Sema operations are needed —
rejection, forwarding, deferred), executes against the
`redb` tables via `sema-engine`, and produces a reply.

### F. Add the universal observer hook

Every daemon publishes its operations and Sema effects to
optional observers. The pattern:

- The daemon defines an internal "observer lane" on its
  public socket.
- A subscriber (typically `persona-introspect`) subscribes
  via the public socket to one of:
  - Inbound contract operations.
  - Outbound Sema effects.
  - Both, by event class.
- When a message arrives or a Sema effect happens, the daemon
  checks the subscriber set and sends a copy to each.

Subscription lives on the **public socket** (not the owner
socket). Observation is not a security concern — no secrets
cross the wire — and putting it on the owner socket creates
ambiguity about which owner the subscription belongs to.

The contract crate declares the observation types; the daemon
implements the emission logic.

### G. Update ARCHITECTURE.md

Each affected crate's ARCHITECTURE.md should:
- Note the migration in a `## Migration to contract-local
  verbs` section.
- Name the new operation roots.
- Reference this report and `/238`.
- List what's still TODO (`MUST IMPLEMENT` annotations are
  fine).

### H. Update tests

- Round-trip tests should exercise the new operation shape.
- Verb-mapping tests (the old `signal_verb()` impl tests)
  are retired — there's no SignalVerb to map.
- Add tests for the daemon-executor lowering where the
  Sema-effect sequence is deterministic.

## 4 · The per-contract migration is a real refactor

This isn't a rename pass. The schema-shape changes:
- Some variants collapse into operation roots (the `*Query`
  → `Query` lift).
- Some variants change names (Assert MessageSubmission →
  Submit Message).
- The reply / event surfaces may simplify (reply variants
  often follow the operation root structure).
- The daemon code that dispatched on `request.signal_verb()`
  changes to dispatch on contract operation directly.
- The CLI may need shorter human-typing shapes — the public
  daemon frame must be the contract operation.

Expect each component refactor to touch:
- The contract crate (`signal-<component>` and / or
  `owner-signal-<component>`).
- The daemon implementation.
- The CLI binary.
- Tests in all three.
- Component-triad witness tests if any reference the verb
  spine.

## 5 · Order of operations across the workspace

Migration order across components — coordinated to minimize
blocked downstream work:

### Phase 1 — Foundation (in flight now)

1. **`signal-frame` repo created** — extracted from
   signal-core. (See companion dispatch report when this
   lands.)
2. **`signal-sema` repo created** — the six Sema verbs +
   read-algebra primitives. (Same.)
3. **The `signal_channel!` macro is updated** in
   `signal-frame/macros/`.
4. **Skill edits land** — `skills/contract-repo.md`,
   `skills/naming.md`, `skills/language-design.md` updated
   for the new direction.

### Phase 2 — Pilot contract refactor

One contract goes first as a worked example:

1. **`signal-repository-ledger`** is a strong pilot — flat
   `*Query` siblings, clear domain (Query / Observe / Receive
   for the read side; Push observation on the assertion
   side), already has the `/124` analysis describing the
   refactor.
2. Refactor produces the canonical example that subsequent
   migrations follow.

### Phase 3 — Persona contracts

Once the pilot lands:

- `signal-persona-spirit` (operator pickup in flight; expand
  bead `primary-ojxq` to include the broader refactor).
- `signal-persona-mind`.
- `signal-persona-orchestrate`.
- `signal-persona-router`.
- `signal-persona-harness`.
- `signal-persona-message`.
- `signal-persona-terminal`.
- `signal-persona-auth`.
- All `owner-signal-persona-*` counterparts.

These can refactor in parallel once Phase 1 is stable; each
agent picks up their assigned component.

### Phase 4 — Cleanup

- `signal-core` deprecated. Archive the repo with a README
  pointing at `signal-frame` + `signal-sema`.
- Any cross-references in skills, reports, lore are updated
  to the new repo names.
- Universal observer hook lands in each daemon (Phase 3 may
  defer this to Phase 4).

## 6 · Coordination points

These are the places where parallel agents need to coordinate:

- **`signal_channel!` macro shape.** Until the macro is
  finalized, contract crates can't fully migrate. The Phase
  1 macro work is gating.
- **`signal-sema` type shapes.** If multiple daemons use
  the same Sema-operation shape (e.g., `Match` payload
  patterns), they share types in `signal-sema`. Avoid
  per-daemon redefinitions.
- **Operation root naming consistency.** Cross-contract
  verb reuse is fine and expected (Observe, Configure,
  Register are common). Reuse the verb name; the receiver
  determines the effect. Don't invent new verbs when an
  existing one fits.

## 7 · References

- `reports/designer/238-signal-architecture-redirection-contract-local-verbs.md`
  — the why and the what.
- `reports/designer-assistant/125-v2-contract-local-verbs-vs-sema-core-verbs.md`
  — the architectural analysis.
- `intent/component-shape.nota` — the psyche statements
  driving the redirection (records from 2026-05-19T19:30Z
  through 2026-05-19T20:00Z).
- `intent/naming.nota` — verb-form-not-noun-form rule.
- `intent/workspace.nota` — chat-brevity, no-vague-questions,
  reports-over-beads, recent-intent-supersession.
- `ESSENCE.md` §"Backward compatibility is not a constraint"
  — applies; the migration is worth the churn.
- `skills/component-triad.md` §"The single argument rule"
  — unchanged; contract-local verbs still ride on the
  one-NOTA-argument-per-binary discipline.
- `skills/language-design.md` — apply directly; verb-form
  naming is downstream.

## 8 · MUST IMPLEMENT notes for affected components

Agents working on the listed components — add a
`## MUST IMPLEMENT — signal architecture migration` section
to your ARCHITECTURE.md pointing back at this report (`/239`)
and the direction report (`/238`). Use the per-component
checklist above. When the refactor lands, remove the MUST
IMPLEMENT note.

Components affected (non-exhaustive — audit your repo if you
maintain a signal-* or component-daemon outside this list):

| Component | Status |
|---|---|
| signal-repository-ledger | Pilot. Refactor first. |
| signal-persona-spirit | In flight; expand bead `primary-ojxq`. |
| signal-persona-mind | Pending. |
| signal-persona-orchestrate | Pending. |
| signal-persona-router | Pending. |
| signal-persona-harness | Pending. |
| signal-persona-message | Pending. |
| signal-persona-terminal | Pending. |
| signal-persona-auth | Pending. |
| owner-signal-* | Each gets its own pass. |
| persona-introspect | Add subscriber side of observer-hook. |
| repository-ledger (daemon) | Move lowering into executor. |
| persona-* daemons | Same — per-component. |

## 9 · How to pick this up

If you're a designer or operator picking up component work
after this migration:

1. Read `/238` and `/239` (this report) in full.
2. Query `intent/component-shape.nota` for the psyche
   statements behind the direction.
3. Check `signal-frame` and `signal-sema` repos on GitHub
   for the current state of the foundation crates.
4. Pick up your component's MUST IMPLEMENT note from its
   ARCHITECTURE.md, OR audit if no note exists yet.
5. Apply the per-component checklist (§3).
6. Update the component's ARCHITECTURE.md to remove the
   MUST IMPLEMENT note once the refactor is done; add a
   `## Migration history — contract-local verbs (2026-05-XX)`
   section noting the shape change for future readers.
7. When the daemon code changes, the migration is done.
