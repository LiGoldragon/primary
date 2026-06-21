# Deploy-readiness gate for schema-help (+ Stream/Family follow-up)

*schema-designer · report 4 · the design/audit lane's view of what
"ready to deploy into spirit with all the full production-db sandbox
tests passing" means for this feature, and the Stream/Family follow-up
spec.*

## Why this deploy is unusually low-risk

Because Help is **client-side**, three things that normally make a spirit
deploy risky are **unchanged**:

- **The daemon binary** — `schema-next` and `nota-next` are both
  `optional` and gated to `nota-text`; `help` is `#[cfg(feature =
  "nota-text")]`. The daemon's default build pulls in **neither the
  parser nor the help module**. The daemon is byte-for-byte the same
  shape it was.
- **The wire contract** — there is no `Input::Help` / `Output::HelpReported`
  root. The daemon-facing contract is identical, so **no daemon redeploy
  or SEMA migration is forced** by this feature. (`spirit` bumped to
  0.16.0; `signal-spirit` staying at 0.8.0 on the wire is *correct* — the
  wire did not change. Confirm that stance is deliberate.)
- **The database** — Help never connects to the socket, so it reads and
  writes nothing. The production store cannot be perturbed by a Help call.

So "deploy" here is effectively a **CLI/text-client-only ship**. That
should frame the test gate.

## The gate — what the prod-db sandbox run should prove

| # | Gate | Status |
|---|---|---|
| 1 | **Daemon boundary clean** — default build excludes `nota-next` **and** `schema-next` and the help module. | Mostly done. The binary-only "no-nota-next dependency surface" test passes; **extend it to assert no `schema-next` in the daemon build too** (the new gated dep). |
| 2 | **Help is a live view of the one decoded schema** — the gate drives Help built from the canonical schema through the decode path (`from_signal_schema_source()` → `from_schema_text(SIGNAL_SCHEMA_SOURCE)`), so the test exercises **decode → project → render** over the real contract. `(Help)` renders **every** Input+Output root and `(Help X)` works for every declared type — including the recursive `Domain` tree and `IntentEventStream`. | Already real (the golden tests call `from_signal_schema_source()`). **Add an explicit "every root renders, no error" assertion.** The virtue we want: because Help reads the same schema that defines the types, it always *is* the real contract — complete and current, by construction, with zero upkeep. The schema is the single source of truth; Help is its self-description, decoded live. |
| 3 | **Prod-db side-effect-free** — copy the production store into the sandbox, run a batch of Help invocations, assert the copy is **byte-identical** afterward, and a daemon pointed at the copy is unperturbed. This is the real point of the prod-db test for a client-side feature: prove Help touches nothing. | This is the test to make sure passes. Help-without-socket already passes; add the **db-untouched assertion** against a real prod-db copy. |
| 4 | **Nix-built CLI renders Help** — the actual deployed binary, built from the pushed remotes in the sandbox, renders `(Help …)` offline. | Done — the ignored nix-integration Help test passed (143.70s). |
| 5 | **Versioning / pins** — `CriomOS-home/flake.lock` pins the `schema-help` revs for the CLI ship; daemon slot unchanged. | Confirm the flake pins target the integrated `main` (post-merge), not the feature branch. |

The honest summary: **the feature is functionally ready**; the gap between
"green on operator's branch" and "deploy-ready" is items 2–3 (an explicit
full-schema render assertion + the db-untouched proof on a real prod-db
copy) and item 1's `schema-next` boundary extension. None are large.

## Stream/Family follow-up — the spec (the "explain")

**What streams/families are.** Most schema types are structs, enums, or
newtypes. A few are *positional special forms* (`skills/structural-forms.md`):
a **Stream** and a **Family**. Spirit has one stream and no working-contract
families:

```
IntentEventStream (Stream { token SubscriptionToken opened SubscriptionStarted
                            event IntentEvent close SubscriptionToken })
```

A stream is four **role-named slots** (`token` / `opened` / `event` /
`close`), each a type. A family is `record` / `table` / `key` slots.

**Current handling.** `help.rs`'s `HelpBody` has variants `Unit`,
`Reference`, `Struct`, `Enumeration`, `Text`. Streams/families have **no
dedicated variant** — they map to `HelpBody::Text(value.to_schema_text())`,
stuffing the whole declaration's raw schema text into a `String`. So
`(Help IntentEventStream)` renders the stream's text inline rather than a
typed node whose slots are navigable references.

**Why it's a (minor) gap.**

- **Not typed in the rkyv tree.** Every other node is a typed `HelpBody`
  a consumer can walk; the stream is an opaque `String`. A tool reading
  the rkyv `HelpModel` can't introspect the stream's slots without
  re-parsing that string.
- **Not typed-linked.** The slot types (`SubscriptionToken`, `IntentEvent`)
  are inside the text, not surfaced as the references that
  `(Help IntentEvent)` resolves. (You can still Help those types directly;
  the stream node just doesn't link to them.)
- **One-level-uniformity break.** It is the single place the typed tree
  degrades to a string.

**The fix.** Add a typed `HelpBody::Frame { kind: FrameKind, slots:
Vec<(HelpName, HelpTypeExpression)> }` (slots are role-named, like a
labeled struct, since stream/family slots carry role names). Project it
from `SourceDeclarationValue::Stream | Family`, and render it the same
shape it reads — but from typed data, each slot a navigable reference, no
`String` escape hatch.

**Priority: low.** One stream, zero working families; the text rendering
is already human-readable. It matters only if a programmatic consumer
walks the rkyv help tree, or for full one-level uniformity. Spec is here
if the psyche wants it; otherwise leaving streams as text is acceptable.
