# 46 - Review of designer 158 sema kernel and engine split

*Designer-assistant review, 2026-05-14. Scope:
`reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md`.
Review stance: findings first, then summary. Baseline: the two-repo
split is correct; this review focuses on wording and implementation
risks that should be fixed before operators treat /158 as the
implementation handoff.*

## Findings

### 1. High - Raw redb access escape hatch in Criome undermines typed storage

`reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md:214`
says Criome absorbs its own slot store, which is correct. But lines
217-219 then say the legacy store can be "reimplemented as a typed
table internally, or kept as raw redb access for performance -
criome's call."

That second option is wrong-shaped. The whole split says `sema` is
the typed redb/rkyv kernel and `sema-engine` is the higher execution
layer. Letting Criome bypass both with raw redb access for performance
reintroduces the untyped storage problem through a side door.

Fix: replace that sentence with a stricter rule:

```text
Criome may own its slot-store abstraction, but the storage remains
typed. If it stores bytes, the bytes are a typed record/newtype with a
specific meaning, persisted through `sema` or through a Criome-owned
typed storage layer that has the same typed-boundary witnesses. Raw
redb access is not an optimization escape hatch.
```

If raw redb is ever truly required, it needs its own design report and
witnesses. It should not appear as a casual option in /158.

### 2. High - Subscription delivery semantics are underspecified and can block commits

`reports/designer/158...md:322-327` says `sema-engine` has no actor
framework and is synchronous, and that `SubscriptionSink<R>` is the
boundary to consumer-side async. The surface at lines 268 and 287-288
names `subscribe` and `SubscriptionSink<R>`, but does not specify
whether sink delivery is allowed to block, fail, apply backpressure,
or run before/after durable commit.

This is dangerous because the engine is also supposed to own
commit-then-emit. A naive implementation could call a consumer sink
inside the write path and let a slow or dead subscriber stall all
writes. Another naive implementation could return from commit before
recording enough data to replay a missed delta.

Fix: /158 should add the delivery contract:

- engine commits state and operation-log entry first;
- engine records subscription delta intent durably or has an explicit
  "best effort live notification only" rule;
- `SubscriptionSink<R>` is enqueue-only and must not block on network,
  actor mailbox pressure, or terminal IO;
- sink failure is typed and logged; it does not roll back the already
  committed database transaction;
- consumer daemons own backpressure policy and reconnect/rebind of
  sinks.

The exact mechanism can be a durable subscription outbox or a strictly
bounded in-memory enqueue, but /158 must pick the first prototype rule.
Without that, Package 4 is not implementation-ready.

### 3. Medium - Dependency pin guidance should use immutable revisions, not tags as the witness

`reports/designer/158...md:305-310` shows:

```toml
sema = { git = "ssh://git@github.com/LiGoldragon/sema", tag = "..." }
```

and lines 487-489 make the witness require `git + tag`. This weakens
reproducibility. The workspace rule in `skills/micro-components.md`
is "git dependency, never sibling path"; Cargo.lock pins the actual
revision. A tag is a release label, not the immutable build identity.
Tags can be moved unless the hosting policy prevents it, and `ssh://`
URLs are less portable in Nix/build contexts than HTTPS Git URLs.

Fix:

```toml
sema = { git = "https://github.com/LiGoldragon/sema.git", rev = "<commit>" }
signal-core = { git = "https://github.com/LiGoldragon/signal-core.git", rev = "<commit>" }
```

The witness should check "no path dependency" and "Cargo.lock pins a
revision" rather than "tag exists." Release tags can still exist, but
the build proof should be the resolved revision.

### 4. Medium - /158 still needs the "no engine-protocol crate yet" guard

My earlier split report explicitly says not to create a separate
engine-protocol crate yet: `signal-core` owns the universal verb words,
and `sema-engine` is the first implementation of database execution.
`reports/designer/158...md` correctly says `sema-engine` should not
depend on `signal-<consumer>` crates, but it does not warn against a
premature `signal-sema-engine` / `sema-engine-contract` repo.

This matters because agents often respond to "engine" plus "typed
contracts" by spawning a protocol crate before there are two
implementations or a process boundary.

Fix: add a short subsection after section 3.3:

```text
No separate sema-engine protocol crate in v1. The plan IR is an
implementation API inside sema-engine. Split a protocol crate only
when a second engine implementation appears or plans must cross a
process boundary.
```

### 5. Low - Wording mistakes can confuse implementation ownership

Two phrases should be corrected before handoff:

- `reports/designer/158...md:238-240` says /157 section 4 contains "the four
  affordances." In /157, section 4 is the full engine shape; the four
  affordances were from the retired /155 pattern-library design. This
  should say: "Carries the /157 section 4 engine surface; the /155
  affordances become internal materials."
- `reports/designer/158...md:393-395` says `sema-engine` becomes the
  "canonical storage layer" for Persona components. More precise:
  `sema-engine` becomes the canonical database-operation layer, backed
  by `sema` as the storage layer.

These are not conceptual blockers, but they matter because the
boundary is the whole point of /158.

### 6. Low - Line-count witness is too easy to game

`reports/designer/158...md:497-499` proposes
`sema_kernel_size_below_six_hundred_lines`. Context budget is a real
constraint, but line count alone is a weak witness: code can be
compressed into ugly dense form to satisfy it, or clear code can exceed
it by a small amount while preserving the boundary.

Fix: make the line-count witness advisory and keep the structural
witnesses load-bearing:

- no `Slot`;
- no legacy raw slot-store API;
- no `reader_count`;
- no `signal-core` dependency;
- no `sema-engine` dependency;
- kernel API still fits in one context and is reviewed as one
  capability.

## Summary

`reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md`
gets the central decision right: `sema` remains a small storage kernel
and `sema-engine` becomes the full Signal/Sema verb execution engine
in a new repo.

I would call it implementation-ready after four edits:

1. remove the raw redb escape hatch for Criome;
2. specify nonblocking/post-commit subscription sink semantics;
3. change dependency guidance from `ssh + tag` to HTTPS Git plus
   revision/Cargo.lock pinning;
4. add the "no separate engine protocol crate yet" guard.

The remaining fixes are wording and witness sharpness.
