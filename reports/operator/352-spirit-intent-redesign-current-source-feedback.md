# Spirit Intent Redesign Third-Pass Feedback

Reviewed target: `reports/designer/578-intent-redesign-synthesis.md`

Current companion context:

- `reports/designer/577-intent-tool-state-and-the-real-flaw.md`
- `reports/designer/579-spirit-agglomeration-pass-2026-06-10.md`
- `/git/github.com/LiGoldragon/spirit/schema/signal.schema`
- `/git/github.com/LiGoldragon/spirit/src/store.rs`
- `/git/github.com/LiGoldragon/spirit/tests/collect_removal_candidates.rs`
- `/git/github.com/LiGoldragon/spirit/tests/process_boundary.rs`

This replaces the second-pass feedback after `578` changed §4a from a local
harness-library framing to an agent-daemon broker with warm per-component
harnesses.

## Current Read

The design is converging. The new §4a answers a real scaling problem: model
governance, rate limits, budget, warm pools, and harness lifecycle should not be
reimplemented inside every component. The vend-not-ferry rule is the right
preserving move: the agent daemon stays on the control path, while Spirit and
its guardian harness exchange Spirit signal directly.

I would treat `578` as a valid architecture target, with two caveats before
implementation starts:

- the certainty / magnitude / weight vocabulary still needs to be made exact;
- the new agent-daemon broker needs a small but precise lease/security/budget
  contract before Spirit depends on it.

The old complaint that "transport is just a diagram" is no longer fair. The
report now chooses the transport shape: lease a warm harness, then direct
component-to-harness signal. The remaining work is to make that shape executable.

## Remaining Attention Items

### 1. Settle the certainty / magnitude / weight axes before editing schema

This remains the strongest schema warning.

Current Spirit has `Entry.magnitude`. Current queries call filtering on that
axis `CertaintySelection`. Revised `578` says `Weight` is separate from
`magnitude` as "strength/importance," while removal-candidate behavior uses zero
on that same axis as currentness/live-state.

Those are three possible axes:

- `Certainty`: currentness / confidence / live-vs-retired filtering;
- `Weight`: reaffirmation count / repetition-derived ranking force;
- `Importance`: optional intrinsic priority, if the psyche truly wants it.

Recommendation: during the breaking schema pass, rename stored
`Entry.magnitude` to `Certainty`, add dedicated `Weight`, and do not keep a
third importance axis unless it is explicitly chosen as a real domain field.

### 2. Agent daemon ownership of model access needs a credential boundary

`578` says the agent daemon owns connections, keys, budget, and warm pools, while
the harness calls the model and the daemon never reads the payload. That can
work, but only if credential flow is explicit.

Implementation needs to decide whether the daemon:

- injects short-lived model grants into harnesses;
- proxies only credentials while never seeing prompt payloads;
- starts harnesses with restricted environment scoped to one lease;
- or keeps persistent warm harnesses that hold model access across leases.

The last option is fastest but hardest to reason about for revocation and
budget. The first option is cleaner but adds handshake cost.

Recommendation: make a `HarnessLease` carry a lease identifier, endpoint,
budget/grant, expiry, and component-role identity. The harness reports usage
against that lease, and the daemon can revoke or refuse future leases without
needing payload access.

### 3. Direct component-to-harness signal needs endpoint authentication

The daemon vends a ready harness endpoint to Spirit. Spirit then sends records
and a question directly to that endpoint. That direct channel carries intent
records, so endpoint authenticity matters even when payload privacy is not high.

Implementation needs:

- how Spirit knows the endpoint belongs to the leased harness;
- how the harness knows the caller owns the lease;
- whether the endpoint is a Unix socket path, inherited file descriptor, local
  service address, or signal runtime address;
- what happens if another process tries to use the endpoint before the lease
  ends.

Recommendation: the lease should include an unguessable lease token or
capability used only for that one call. A warm harness should reject payloads not
matching its active lease.

### 4. Budget accounting must survive daemon and harness failures

`578` says an agent-daemon blip leaves in-flight harnesses working and only new
leases wait. That is operationally attractive. It also means usage reporting can
arrive after daemon restart or fail to arrive at all.

Implementation needs a durable accounting story:

- lease issued;
- lease started;
- model call attempted;
- model call completed;
- usage reported;
- lease ended or expired.

Recommendation: agent daemon should journal lease issuance and completion. If a
harness dies or cannot report usage, the daemon should mark the lease unknown or
expired, not silently lose budget state.

### 5. Event/archive wording still needs implementation precision

`578` still says subscription events evaporate, while also saying retired arrows
and clarify prior wording are archived. The intended distinction is sound but
should be made explicit for implementers.

Recommended wording:

Subscription events are ephemeral delivery notifications; operation history,
retired arrows, and prior clarified wording are durable archive/journal data
outside the live intent query surface.

### 6. Category migration should precede guardian prompt work

The category plan is good: closed broad categories, agent proposal, psyche
approval, enlargement gate. It should still precede guardian prompts.

If guardian retrieval starts while the live field is still free-text `Topic`, it
will bake the old recall failure into the new gate. The first usable guardian
bundle should already be category + keyword + full-text, not old topic-only
matching.

### 7. Use exported fixture files for migration tests

The kind migration is now clear enough to test. Use exported record fixtures or
schema files checked into the repo, not inline Rust strings.

Fixture coverage should include:

- an old `Correction` folded into a forward record plus correction event/archive;
- an old `Clarification` converted into clarify history or a forward record;
- a removal-candidate record hidden from default query but visible to explicit
  candidate query;
- an old narrow topic becoming broad category plus keyword;
- a duplicate proposal refusing capture and bumping weight.

## Suggested Implementation Gate

Ready to implement substrate in this order:

1. identifier-bearing `RecordSnapshot` observations;
2. schema vocabulary cleanup for `Certainty` and `Weight`;
3. category catalog and migration fixtures;
4. durable operation journal/archive model;
5. `signal-agent` lease contract and meta-signal harness registry;
6. harness endpoint authentication and lease accounting;
7. guardian verdict integration for propose, clarify, and supersede.

Not ready to implement as "the guardian LLM loop" until those substrate pieces
are concrete.

## Net Feedback

The broker-daemon revision is a good move. It gives the workspace one place for
model governance without forcing the broker to understand every consumer signal.

The remaining implementation risk is mostly security and vocabulary, not the
high-level architecture. Do not start with prompts. Start with record snapshots,
axis naming, category migration, lease semantics, and failure/accounting tests.
