# Review Of Designer 241 Signal Migration Guide

Date: 2026-05-19
Role: designer-assistant
Target: `reports/designer/241-signal-architecture-migration-guide.md`

## Verdict

`reports/designer/241-signal-architecture-migration-guide.md` is a much better
operator guide than `/239`. It correctly reflects the foundation state:

- `signal-frame` exists.
- `signal-sema` exists.
- `Operation<Payload>` has been collapsed.
- `Request::check()` has been removed.
- `signal_channel!` now accepts contract-local `operation <Verb>(<Payload>)`
  grammar.

I verified the foundation tests locally:

```text
/git/github.com/LiGoldragon/signal-frame
  CARGO_BUILD_JOBS=1 cargo test --all-targets
  22 tests passed

/git/github.com/LiGoldragon/signal-sema
  CARGO_BUILD_JOBS=1 cargo test --all-targets
  30 tests passed
```

The guide is therefore broadly implementation-ready. The remaining issues are
not foundation breakage; they are places where old semantics and stale
documentation still leak through.

## Finding 1: Observer Hook Still Conflicts With Psyche Intent

`/241 §3.E` still says:

```text
Every daemon publishes its inbound contract operations and outbound Sema effects
to optional observers.

The daemon defines an internal observer lane on its public socket (not the owner
socket — observation is not security-sensitive; no secrets cross the wire).
```

This remains the most important flaw.

The psyche's answer was subscription-driven introspection, not universal public
observation:

```text
possibly we don't log everything unless there's an introspection subscribe for
it. Right? So it depends if there's a subscription for that event. Unless it's
just normal operation to log that event, it's kind of like turning on debugging
mode.
```

The sentence "observation is not security-sensitive; no secrets cross the wire"
is especially wrong. Inbound contract operations and lower Sema effects may
contain user messages, private intent, daemon configuration, repository paths,
commit messages, prompts, or future credential-shaped mistakes.

### Recommended Correction

Replace "universal observer hook" with:

```text
Each daemon MAY expose typed observation classes.
Observation is subscription-driven.
Each observation class declares its authority surface:
  ordinary signal-<component> for safe peer-observable classes;
  owner-signal-<component> for privileged/sensitive classes;
  no surface for data that must not be introspected.
persona-introspect subscribes to the classes it is allowed to observe.
```

This preserves the development need for introspection without declaring all
operation/effect traces harmless.

## Finding 2: `signal-frame` Source Comments Still Say Atomic Commit

`signal-frame/ARCHITECTURE.md` has been corrected:

```text
Request<Payload>'s NonEmpty<Payload> sequence preserves order and aligns replies
positionally. Database atomicity belongs to signal-sema / sema-engine or to a
contract that explicitly promises it.
```

But `signal-frame/src/request.rs` still says:

```rust
/// One or more contract payloads that commit (or abort) as one unit.
///
/// ... Atomicity is structural — the `NonEmpty<Payload>` is the unit.
```

`signal-frame/src/reply.rs` also still says things like:

```rust
/// Every operation completed/committed in its own mode.
/// An operation at `failed_at` failed; the request aborted.
```

This is not just wording. It can pull implementers back into thinking
`signal-frame::Request` owns transactional commit semantics.

### Recommended Correction

Change source comments to match the architecture:

```text
Request<Payload> is an ordered non-empty sequence of contract payloads.
It is the unit of one exchange, not necessarily the unit of database atomicity.
Contracts or daemons may define all-or-abort semantics for their own requests.
Sema atomicity belongs below, in signal-sema / sema-engine.
```

Reply comments should say "operation completed" only if the component contract
defines completion for that payload. Avoid "committed" at the frame layer.

## Finding 3: `signal-sema` Dependency Guidance Is Still Too Broad

`/241 §3.A` says to add `signal-sema`:

```text
Only if the daemon speaks Sema directly (executor lowering, introspection,
sema-engine integration)
```

"sema-engine integration" makes this almost every triad daemon. That risks
turning `signal-sema` back into a universal dependency by habit.

Better distinction:

```text
Use sema-engine API directly for normal component state.
Depend on signal-sema only when the daemon constructs Sema operations as typed
data: explicit Sema plans, Sema-effect observations, signal-sema socket
traffic, replay/debug/introspection artifacts.
```

If sema-engine's ordinary API internally uses `signal-sema`, let sema-engine
depend on it. Do not make every component import `signal-sema` just because it
has a database.

## Finding 4: Permanent Docs Still Reference Reports

`/241` is a report, so it can cite reports. The problem is that the migration
has already pushed report references into permanent docs.

Examples found:

```text
skills/contract-repo.md
  references reports/designer/238...
  references reports/designer-assistant/125-v2...

/git/github.com/LiGoldragon/signal-sema/ARCHITECTURE.md
  references reports/designer/238...
  references reports/designer/239...

many signal-* ARCHITECTURE.md files
  MUST IMPLEMENT notes reference /238 and /239
```

This conflicts with:

```text
skills/skill-editor.md
  Skills do not cite reports.

skills/architecture-editor.md
  ARCHITECTURE.md files do not cite reports.
```

### Recommended Correction

`/241` should add a cleanup requirement:

```text
Migrate the substance of /238 / /239 / /241 into skills and architecture prose.
Remove report-path citations from skills and ARCHITECTURE.md files.
Temporary implementation notes may name the missing shape directly, but should
not rely on report paths for meaning.
```

For `MUST IMPLEMENT` notes, the shape should be self-contained:

```text
This contract still uses pre-migration SignalVerb wrappers.
Refactor to contract-local operation roots:
  Query(...)
  Submit(...)
  Configure(...)
```

No report path should be required to understand what must happen.

## Finding 5: "Use Reports As Documentation Substrate" Needs Rewording

`/241 §8` says:

```text
Use reports as the documentation substrate — beads are not psyche-visible.
```

The intent is good: do not hide decisions only in beads. But the wording can
fight the permanent-doc discipline. Reports are a working surface, not the
permanent documentation substrate.

Better wording:

```text
Use reports for migration coordination and user-visible synthesis. Once a
shape is settled, migrate its durable substance into skills, ARCHITECTURE.md,
or code comments, and retire or supersede the report.
```

## Finding 6: `RequestPayload` Marker Trait May Be Transitional Ceremony

`signal-frame::RequestPayload` is now a marker trait with only:

```rust
fn into_request(self) -> Request<Self>
```

This is not wrong, and the macro uses it ergonomically. But it is no longer
strictly a "payload contract" trait the way it was when it carried
`signal_verb()`.

The question is whether this convenience earns its trait:

- Keep it if the workspace wants every macro-generated request enum to have
  `operation.into_request()` as a standard ergonomic method.
- Collapse it later if it becomes another empty marker pattern.

This is not blocking, just worth tracking after the first real contract
migration.

## What `/241` Gets Right

- It names `/239` as superseded for practical migration. Good.
- It says the foundation is real, and local tests confirm that.
- It gives a clear new macro example and NOTA form.
- It correctly says `signal-repository-ledger` should be the pilot.
- It correctly says `signal-core` should be deprecated later, not patched into
  the new model.
- It captures the verb-form rule sharply: `Submit`, not `Submission`; `State`,
  not `Statement`.
- It keeps `ReadPlan` out of `signal-sema`; that belongs in sema-engine or
  contract read payloads.

## Questions To Bring Forward

### Q1. Observation Authority

Should `/241` keep saying observation lives on the ordinary public socket and
is not security-sensitive?

My recommendation: no. Observation must be event-class-specific and
permissioned. Some classes can be ordinary; sensitive classes belong behind
owner-signal or another explicit introspection authority.

### Q2. Frame Request Semantics

Should `signal-frame::Request` source comments keep using "commit", "abort",
and "atomicity" wording?

My recommendation: no. Use "ordered exchange sequence" at the frame layer.
Only contracts or sema-engine should speak about atomic commit.

### Q3. `signal-sema` Dependency Scope

Should every daemon that uses sema-engine import `signal-sema` directly?

My recommendation: no. Depend on `signal-sema` only when the daemon constructs
Sema operations as data. Normal sema-engine use should not automatically pull
the public operation vocabulary into every daemon.

## Bottom Line

`reports/designer/241-signal-architecture-migration-guide.md` is good enough to
use as the practical migration guide after two corrections: remove the unsafe
public-observer claim and clean up frame-layer atomicity language. The
foundation is real and tested; the remaining risk is agents implementing the
new design while preserving old semantics in comments, docs, and dependency
habits.
