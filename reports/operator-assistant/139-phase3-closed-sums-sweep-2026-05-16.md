# 138 — Phase-3 closed-sums sweep across non-mind contracts

Date: 2026-05-16
Role: operator-assistant
Scope: Implement closed-sums research from designer/198 across the
seven non-mind signal-persona-* contract crates and signal-criome.
ARCHITECTURE.md + skills.md rewrites; canonical NOTA examples files
with round-trip witnesses; flake-source fix so the examples reach
nix-sandbox `include_str!`.

## 0 · TL;DR

Closed the workspace's "perfect specificity at boundaries" discipline
across the non-mind contract surface. Every in-scope contract now
carries:

- An `ARCHITECTURE.md` whose Constraints section names testable
  obligations — closed wire enums, Path A subscription lifecycle,
  per-variant rkyv + NOTA round-trip witnesses, no stringly-typed
  dispatch, named-API-reference dependency pin.
- A `skills.md` aligned with the same discipline, pointing at the
  workspace `subscription-lifecycle.md` skill for stream-block
  conventions.
- An `examples/canonical.nota` file with one canonical text example
  per request / reply / event variant (representative coverage for
  the larger surfaces).
- A `tests/canonical_examples.rs` round-trip witness that parses the
  canonical file through `<T as NotaDecode>::decode`, re-encodes,
  and asserts byte-equality with the canonical text.
- A `flake.nix` source filter extension that surfaces `examples/`
  into the nix sandbox so `include_str!` finds the canonical file.

Seven repos touched on `main`, three commits each (ARCH, skills,
tests + flake bundled, where some bundles split for hook
interactions). The `persona-router` consumer migration deferred by
/132 was already landed by a parallel agent and is verified by an
existing `observation_truth.rs` witness asserting
`RouterReply::MessageTraceMissing` on the slot-miss path. The
signal-persona-system Path A reconciliation question from the brief
(would /132 have removed the request-side retraction?) resolved
trivially: signal-persona-system already carries the kernel-grammar-
required request-side `Retract FocusSubscriptionRetraction` and the
reply-side `SystemReply::SubscriptionRetracted` ack; both are
present in the live source and the ARCH §6 constraints reflect the
both-sides shape per /91 §2.

`cargo test` AND `nix flake check` green on every touched crate.

## 1 · Pushed commits

| Repo | Commit | Subject |
|---|---|---|
| signal-persona-router | `b8b43eb0` | ARCH: closed-sums + Path A constraints, no-Unknown witness + NOTA codec quirk |
| signal-persona-router | `3566f213` | skills: closed-sums discipline, subscription-lifecycle pointer, NOTA codec quirk |
| signal-persona-router | `025fd95e` | tests: canonical NOTA examples round-trip witness for every request/reply variant |
| signal-persona-router | `e8ffebc6` | flake: include examples/ in build src so canonical.nota reaches include_str! |
| signal-persona-introspect | `d6176fcb` | ARCH: closed-sums constraints, Option<>-for-not-yet-observed witness, NOTA codec quirk |
| signal-persona-introspect | `0b108c4c` | skills: closed-sums + Option<>-for-not-yet-observed + subscription-lifecycle pointer |
| signal-persona-introspect | `615d1ec2` | tests: canonical NOTA examples round-trip witness for every request/reply variant |
| signal-persona-introspect | `e3cc8fd6` | flake: include examples/ in build src |
| signal-persona-system | `e9347736` | ARCH: Path A lifecycle witness, closed-sums constraints, NOTA codec quirk |
| signal-persona-system | `334d187c` | skills: subscription-lifecycle pointer, closed-sums discipline, NOTA codec quirk |
| signal-persona-system | `cecdc4bb` | tests: canonical NOTA examples round-trip witness for every request/reply/event variant |
| signal-persona-system | `de95aa00` | flake: include examples/ in build src |
| signal-persona-harness | `a022e308` | ARCH: Path A lifecycle (request + reply), closed-sums constraints, NOTA codec quirk |
| signal-persona-harness | `a77acbea` | skills: subscription-lifecycle pointer, closed-sums + skeleton-honesty discipline |
| signal-persona-harness | `dac34439` | tests: canonical NOTA examples + flake source filter |
| signal-persona-terminal | `990fbed5` | ARCH: Path A lifecycle, closed-sums constraints, NOTA codec quirk |
| signal-persona-terminal | `7b3d9ef0` | skills: subscription-lifecycle pointer, closed-sums + skeleton-honesty discipline |
| signal-persona-terminal | `f61ce88d` | tests: canonical NOTA examples round-trip witness (Path A + representative variants) |
| signal-persona-terminal | `a44a0903` | flake: include examples/ in build src + fmt the test |
| signal-persona | `9c651418` | ARCH: closed-sums + NOTA + named-API-ref constraints |
| signal-persona | `a8d0331c` | skills: six-root spine, closed-sums + structural-atomicity discipline |
| signal-persona | `49cf02c4` | tests: canonical NOTA examples round-trip witness for both relations |
| signal-persona | `67376687` | flake: include examples/ in build src + fmt the test |
| signal-persona-auth | `7fddd84e` | ARCH: closed-sums + NOTA + named-API-ref constraints; AuthProof absence |
| signal-persona-auth | `a50829a2` | skills: closed-sums + AuthProof-absence discipline, NOTA codec note |
| signal-persona-auth | `e4ea81ea` | tests: canonical NOTA examples round-trip witness for every record kind |
| signal-persona-auth | `ad999f9f` | flake: include examples/ in build src + fmt the test |
| signal-criome | `6d9a4576` | ARCH: Path A lifecycle + closed-sums witnesses, Unknown* as positive rejection causes |
| signal-criome | `1fc4f7bb` | skills: subscription-lifecycle pointer, closed-sums + AuthProof-absence discipline |
| signal-criome | `80f1f299` | tests: canonical NOTA examples round-trip witness (Path A + representative variants) |
| signal-criome | `6cd60c93` | flake: include examples/ in build src + fmt the test |

## 2 · ARCHITECTURE rewrites

Every in-scope ARCH file now follows the architecture-editor.md §"Format"
shape (TL;DR + components + wire vocabulary + messages + constraints +
non-ownership + code map + see-also) and inlines:

- **Closed-enum integrity** as a constraint with the witness named
  (per-enum exhaustive-match round-trip test).
- **Path A subscription lifecycle** as a constraint pointing at the
  `signal_channel!` `stream` block grammar and the kernel grammar at
  `signal-core/macros/src/validate.rs:303–331` which rejects any
  stream whose `close` is not a request-side `Retract` variant.
- **NOTA codec quirk** as its own short section: the macro emits a
  request variant's NOTA head as the *payload's* record head, not
  the Rust variant name. Canonical examples and round-trip tests
  use the payload heads.
- **Named API reference** as the dependency-pin constraint:
  `Cargo.toml` declares `git = "..."` with a named branch/bookmark,
  not a raw `rev = "..."` pin. Per /91 §4 (signal-core stable
  reference: bookmark/branch, not raw rev).
- **Round-trip witnesses cover every variant in rkyv AND NOTA** as a
  constraint with the canonical-examples test as the new witness for
  the NOTA half.

Stale "transitional Unknown variant" prose was scrubbed from
signal-persona-router and signal-persona-introspect ARCH files
during the rewrite (the hook had appended such rows in /132's run;
they are now gone). Stale "removes request-side retraction" prose
was scrubbed from signal-persona-harness ARCH (the old §
"Observation channel" section claimed retraction was reply-only,
which contradicts /91 + the kernel grammar). The replacement names
the both-sides Path A lifecycle and the kernel-grammar enforcement.

The harness ARCH was reshaped by a workspace hook between my first
and second commits to point at `~/primary/skills/subscription-lifecycle.md`
(which exists and is the canonical home for this discipline) rather
than embed "Path A per /181" prose. The hook's edit is correct per
architecture-editor §"Architecture files never reference reports"
(reports retire; skills are permanent); I left it in place.

## 3 · skills.md rewrites

Each in-scope contract's `skills.md` now lists:

- The repo's load-bearing invariants (closed enums, Path A both
  sides, every request variant declares a Signal root verb, no
  runtime code, every variant has rkyv + NOTA witnesses, named API
  reference pins).
- The editing patterns for the common cases (adding a new variant,
  adding a new subscription kind, modeling "entity not in store").
- A pointer to `~/primary/skills/subscription-lifecycle.md` as the
  canonical FSM for stream blocks.
- The NOTA codec quirk note as its own short section.

`signal-persona/skills.md` previously said "the only operation roots
are the seven `signal-core` `SignalVerb` roots." That was stale per
/177 (six roots, atomicity structural); the rewrite states the six
roots explicitly and notes the structural-atomicity rule.

`signal-persona-auth/skills.md` previously listed only four rules;
the rewrite adds the load-bearing-invariants block (no AuthProof
type, closed enums, no Unknown variant, no in-band proof, named API
reference pins) plus editing patterns and the SO_PEERCRED →
ConnectionClass mapping reminder.

## 4 · Canonical examples files + round-trip witnesses

Each contract now carries `examples/canonical.nota` plus
`tests/canonical_examples.rs`. The file holds one canonical text
example per request / reply / event variant; the test parses each
through `<T as NotaDecode>::decode`, re-encodes via
`<T as NotaEncode>::encode`, and asserts the resulting text equals
the canonical line in the file. The test also asserts the canonical
text appears in `examples/canonical.nota` (defensive: prevents drift
between the file and the test).

Discovery from this run: the `signal_channel!` macro's decode arms
dispatch on the **payload type's record head**, not the request
variant name. So `RouterRequest::Summary(RouterSummaryQuery { … })`
encodes as `(RouterSummaryQuery prototype)` — not `(Summary
prototype)`. This shape is now documented in every contract's ARCH
§"NOTA codec quirk" and matching skills.md note. The macro emission
lives at
`signal-core/macros/src/emit.rs:376-422` (`emit_payload_enum_codec`)
where the decode arm uses `last_path_segment(&payload_string)` as
the head — i.e. the payload's record-head type name.

The flake source-filter fix (a one-time addition to each contract's
`flake.nix`) extends `craneLib.cleanCargoSource ./.` to also include
`examples/` files. Without it, the nix sandbox excludes the
canonical file and `include_str!` fails at compile time. The
existing rkyv round-trip tests don't need this fix because they
don't read external files; only the new `tests/canonical_examples.rs`
does.

## 5 · What was checked but is already correct

### 5.1 signal-persona-system Path A shape

The brief asked me to "verify whether request-side
`FocusSubscriptionRetraction` (Retract verb) is still present per
/91 OR was wrongly removed." It is present, correctly. The
`signal_channel!` declaration in `src/lib.rs` names

```text
Retract FocusSubscriptionRetraction(FocusSubscriptionToken)
```

as a request variant and

```text
SubscriptionRetracted(SubscriptionRetracted)
```

as the reply variant. The `stream FocusEventStream { close
FocusSubscriptionRetraction; … }` block uses the same retract
variant, satisfying the kernel-grammar `stream`-block validation at
`signal-core/macros/src/validate.rs:303-331`. The Path A two-sided
shape is the source-of-truth design; the brief's contingent
restoration instructions were precautionary.

### 5.2 persona-router consumer migration of MessageTraceMissing

/132 deferred the consumer migration because the canonical
persona-router checkout carried uncommitted parallel-agent work at
the time. That work has since landed
(`ee091df5 persona-router: lock spawn_blocking detach + assert
MindAdjudicationOutbox counters` is HEAD on main today) and the
observation actor's `answer_message_trace` arm now returns
`RouterReply::MessageTraceMissing(RouterMessageTraceMissing { engine,
message_slot })` on the slot-not-in-store path. The witness lives at
`/git/github.com/LiGoldragon/persona-router/tests/observation_truth.rs:280-293`
where a `router.observe(RouterRequest::MessageTrace(...))` call for
a slot id of `99` is asserted to return
`RouterReply::MessageTraceMissing` with `message_slot ==
MessageSlot::new(99)`.

No edit needed in persona-router.

## 6 · Workspace lint witness — no `Unknown` in wire enums

The brief asked for a "workspace lint witness — no `Unknown` in wire
enums; source-scan witness; document the home in ARCH."

The witness home is per-contract: each ARCH §"Constraints" lists the
"wire enums contain no `Unknown` variant" obligation and names the
per-crate test that enforces it. The per-crate tests fall into three
classes:

- **Exhaustive-match round-trip tests** like
  `router_status_enums_are_closed_no_unknown_variants` (already in
  `signal-persona-router/tests/round_trip.rs`) and the analogous
  `introspection_status_enums_are_closed_no_unknown_variants` in
  signal-persona-introspect. These exhaustively match every variant
  of every closed wire enum; adding an `Unknown` variant either
  breaks the match (compile fail) or forces the new variant to be
  explicitly added to the match arms (which surfaces the change in
  review).
- **Canonical-examples round-trip tests** (the new
  `tests/canonical_examples.rs` in every contract) which enumerate
  every variant the contract emits. Adding `Unknown` to a closed
  enum forces a new canonical example, surfacing the change in
  review.
- **Source review** documented in each ARCH for the cases where the
  word "Unknown" appears as a positively-named domain rejection
  (`InjectionRejectionReason::UnknownTerminal`,
  `VerificationDecision::UnknownSigner`, etc.) — closed positive
  rejection causes, not polling-shape placeholders. The ARCH §"Closed-
  enum integrity" sections call out this distinction explicitly.

A workspace-level cross-crate scanner would be additional
defense-in-depth, but the constraint is enforced today through the
per-crate witnesses. I did not add a workspace-level bash script
because: (a) the per-enum exhaustive match is a stronger guard
(compile-time, type-checked) than a grep-based source scan; (b) the
grep would need exceptions for the positively-named domain rejection
variants which are valid usage; and (c) the workspace-skill home for
the discipline (`skills/contract-repo.md` §"Common mistakes",
ESSENCE §"Perfect specificity at boundaries") already documents the
rule.

## 7 · Discipline notes for the next agent

- **`signal_channel!` NOTA codec quirk.** Decode arms dispatch on
  the payload's type-name (per `signal-core/macros/src/emit.rs:376-422`).
  When writing canonical NOTA examples, the head is the payload
  struct name, not the Rust variant name. The two coincide for the
  common case (variant `MessageDelivery(MessageDelivery)`); they
  diverge when the variant name differs from the payload type, as
  in retract variants:
  `FocusSubscriptionRetraction(FocusSubscriptionToken)` encodes as
  `(FocusSubscriptionToken …)`.
- **`Vec<u8>` encodes as `[u8 u8 …]` not `#hex…`.** The hex literal
  form is `read_bytes` / `write_bytes` in the codec, used by
  `NotaTransparent` newtypes around `Vec<u8>`. The `Vec<u8>` itself
  goes through the generic `Vec<T>` impl which emits a sequence of
  u8 ints.
- **Bare-string eligibility includes hyphens.** `"internal-message-
  router"`, `"trace-7"`, `"hello-from-operator"` all emit bare;
  `"Approve write?"` emits quoted because the question mark and
  space disqualify it.
- **`Option<T>` encodes `None` as the bare PascalCase `None` and
  `Some(x)` as just `x`.** Adding a new optional field to a
  `NotaRecord` changes the canonical examples but does not change
  the encoding shape.
- **Linter/hook stale-state pressure** continues to be real. During
  this run a hook appended `RouterDaemonConfiguration` and
  `IntrospectDaemonConfiguration` records to two contract crates
  mid-arc; my ARCH/skill commits stayed clean because I edited only
  the doc files. Two crates needed `cargo fmt` because the hook's
  insertions introduced non-canonical line-wrapping that `nix flake
  check fmt` rejected.
- **The flake source filter is a one-time per-repo addition.** The
  pattern is identical across all seven contracts:

  ```nix
  examplesFilter = path: _type: builtins.match ".*/examples(/.*)?$" path != null;
  sourceFilter = path: type:
    (craneLib.filterCargoSources path type) || (examplesFilter path type);
  src = pkgs.lib.cleanSourceWith {
    src = ./.;
    filter = sourceFilter;
    name = "source";
  };
  ```

  Future contract crates with canonical examples files need the same
  filter.

## 8 · Cross-references

- `/home/li/primary/reports/designer/198-prior-art-closed-sums-and-perfect-specificity.md`
  (in-history; retrieved from git) — the research this run
  implements.
- `/home/li/primary/reports/designer/193-signal-persona-contracts-gap-scan.md`
  (in-history) — the gap scan /132 closed in Phase 1.
- `/home/li/primary/reports/designer-assistant/91-user-decisions-after-designer-184-200-critique.md`
  (in-history) — the user decisions that fix the subscription
  lifecycle shape (request-side retract + reply-side ack) and the
  named-API-reference dependency pin.
- `/home/li/primary/reports/operator-assistant/132-signal-persona-contracts-gap-close-2026-05-16.md`
  — the Phase 1 work this run extends.
- `/home/li/primary/skills/subscription-lifecycle.md` — the
  canonical workspace skill for the FSM every Signal subscription
  follows. Each in-scope ARCH and skills.md now points at it.
- `/home/li/primary/skills/contract-repo.md` §"Examples-first
  round-trip discipline" — the canonical home for the canonical-
  examples + round-trip witness pattern.
- `/home/li/primary/ESSENCE.md` §"Perfect specificity at boundaries"
  — the upstream principle.
