# Spirit New-Design Implementation Frontier

## Scope

The psyche asked for the new Spirit designs to be reviewed with an operator eye:
what can be implemented now, what can at least be demonstrated, and what should
wait. I grounded this against the recent designer/system-designer reports and the
current repo state, especially:

- `reports/system-designer/110-psyche-answers-spirit-concept-2026-06-15.md`
- `reports/system-designer/112-criome-spirit-auth-concept/2-concept-decisions.md`
- `reports/designer/647-universal-positional-prototype-and-operator-plan.md`
- `reports/designer/648-spirit-positional-integration-analysis.md`
- `reports/designer/649-family-stream-positional-syntax-pin.md`
- `reports/designer/652-schema-cc-design-and-leans.md`
- `reports/designer/653-schema-cc-integration-merge-ready.md`
- `reports/operator/388-schema-cc-main-landing-and-structural-repin.md`

I also checked current source in `spirit`, `signal-spirit`, `schema-next`, and
`schema-rust-next`, and ran focused tests listed at the end.

## Current baseline

Production Spirit is healthy on the deployed mainline build:

- `spirit-daemon.service`: active
- startup preflight: `(Current (1275 0))`
- `spirit Version`: `(VersionReported 0.13.0)`
- `spirit Marker`: `(MarkerReported (1312 12541975979470193249))`

The store-version skew that broke the edit path has been fixed. Spirit main now
also contains a public intent render client, `spirit-render`, which is a first
practical piece of the "Spirit as intent substrate" rollout.

## Implementation frontier

| Design | Current state | Operator call |
|---|---|---|
| Clarification as edit, not additive record | Future-facing `Clarify` already edits the target record in place, archives the previous arrow, and preserves the record identifier. There is no `ResolveClarification` cleanup root on main for old standalone `Kind::Clarification` records. | Implement now. This is the highest-value Spirit operation because it fixes the bad-use pattern directly. |
| Named private capture | Stored record remains uniform; report 110 says the private path should be a named short-form. No `RecordPrivate` / `RecordSealed` root exists. | Implement now or demo first. Low schema blast radius and high safety value. Needs one naming/default privacy call. |
| Intent substrate in Spirit | `spirit-render` exists on main and renders public records by referent to a generated `spirit.nota`. Contract/docs rollout is still unfinished. | Demonstrate now; then implement gradual rollout. This is the clean bridge from per-repo `INTENT.md` to Spirit. |
| Domain coarsening | Domain schema is coarsened in `signal-spirit`; production migration maps older software leaves into terminal values plus keywords. Focused migration test passes. | Treat the core as implemented. Remaining work is acceptance/gate polish and guardian/query behavior verification, not a new design. |
| Collect removal candidates | Implemented in `signal-spirit` and `spirit`: archive-first into a separate archive database, then remove exact Zero/Zero candidates. Tests pass. | Already implemented. Any open bead for the base operation should be reconciled/closed after checking its exact text. |
| Schema-cc | Landed on `schema-next` main: parenthesis-reference dispatch is generated from `schemas/reference-grammar.nota`. Spirit consumers are byte-transparent. | Done for this slice. Next demo is datafying another compiler surface, not more Spirit integration. |
| Universal positional family/stream syntax | Design is pinned, but the mainline schema still uses brace forms for `Family` and `Stream`. Branches exist. | Build as a branch demo next, then integrate through the normal schema cascade. Do not deploy halfway. |
| Criome caller attestation | Design is sound but production is blocked on real criome BLS sign/verify, signed identity registration, and key lifecycle. | Demo only until `primary-kr40` lands. Spirit-side scaffolding can be built behind a fake/local attester. |
| Mirror shipper | Mirror work exists, but production enablement is blocked by unauthenticated `0.0.0.0` ingress. | Keep blocked for production. Local demo only after auth posture is explicit. |
| Fast/full Spirit verification gates | Open bead says the local stack check is too slow/monolithic. Recent outages show the need. | Implement now. This is pure operator hygiene and reduces deploy risk for every other slice. |

## Best immediate implementation

The next production-grade Spirit feature should be `ResolveClarification`.

The important distinction is:

- `Clarify` is for a correctly shaped future operation: target identifier plus
  sharper description. It already exists and is tested.
- `ResolveClarification` is maintenance for the bad historical shape: a standalone
  record whose kind is `Clarification`, which should never have been added as a
  new durable arrow. Resolution means edit the clarified target or targets, then
  archive/remove the standalone clarification record as one guarded operation.

I would make the first implementation explicit rather than clever:

```
ResolveClarification {
  clarification RecordIdentifier
  target_changes (Vec RecordChange)
  justification Justification
}

ClarificationResolved {
  clarification RecordIdentifier
  changed RecordIdentifiers
}
```

The daemon should not guess the targets in the authoritative operation. A helper
can suggest targets by searching testimony, antecedents, referents, and nearby
records, but the committed operation should name the standalone clarification and
the exact target edits. That keeps the destructive part auditable.

Store behavior:

- validate the clarification record exists and has `Kind::Clarification`
- validate every target exists before any write
- archive the old target records and the standalone clarification record
- apply all target record changes
- remove the standalone clarification record
- emit one receipt and one observer/intent event

The acceptance test should seed one bad standalone clarification plus one or more
targets, call `ResolveClarification`, assert the target descriptions changed,
assert the clarification no longer observes, assert archives contain the prior
state, and assert rollback if any target is missing.

## Best demonstration implementations

`RecordPrivate` is the safest visible demo. It proves the "uniform storage,
named creation shorthand" design without destabilizing the store. The operation
would lower to `Record` with an explicit privacy value and otherwise reuse the
existing guardian/write path. The only open call is name and default privacy:
`RecordPrivate` is plain; `RecordSealed` is stronger but more ambiguous. My lean
is `RecordPrivate` with a default of `Privacy Minimum`, unless the psyche wants
the named form to mean a higher privacy rung.

Spirit intent-render is already a partial demo. Next step is to make it useful:
render by repo referent into a generated `INTENT.md`-like document or sidecar,
then update the workspace skills to say "read Spirit first, render summary when
needed" only after the rollout is real. The current `spirit-render` implementation
is public-only, which is correct for generated repo guidance.

Criome attestation can be demonstrated but should not ship as production trust
until criome has real crypto. The Spirit-side demo should introduce the nouns now:
`CriomeAuthority`, a committed-operation digest accessor, and an out-of-band
attestation family. Use a fake attester in tests to prove the flow and failure
posture. Do not embed proofs into intent records.

Universal positional family/stream syntax is a compiler-stack demo, not a Spirit
feature in isolation. The pinned source forms are:

```
RecordsFamily (Family StoredRecord records Domain)
IntentEventStream (Stream SubscriptionToken SubscriptionStarted IntentEvent SubscriptionToken)
```

That should land only as a coherent schema cascade after the `symbol_atom` derive
support and Nix gate are green.

## What I would not implement first

I would not start with mirror shipper production enablement. It is blocked on
transport/auth posture, and its failure mode is external exposure, not just local
schema churn.

I would not make `ResolveClarification` auto-discover and mutate targets as its
first form. Auto-discovery is useful as a CLI assistant, but the committed
operation should be explicit.

I would not expand schema-cc directly into Spirit. The first schema-cc slice is
already on `schema-next` main and byte-transparent to Spirit. The next schema-cc
work belongs in compiler surfaces, then flows downstream naturally.

## Verification run during this audit

Focused checks:

- `cargo test --features nota-text --test spirit_render -- --nocapture`: 3 passed
- `cargo test --features nota-text --test collect_removal_candidates -- --nocapture`: 3 passed
- `cargo test --features nota-text --test runtime_triad signal_write_operations_propose_clarify_supersede_and_retire -- --nocapture`: 1 passed
- `cargo test --features production-migration production_migration::tests::migrates_version_nine_current_layout_domains_to_terminal_values_and_keywords -- --nocapture`: 1 passed

Live checks:

- `systemctl --user is-active spirit-daemon.service`: active
- `spirit Version`: `(VersionReported 0.13.0)`
- `spirit Marker`: `(MarkerReported (1312 12541975979470193249))`
