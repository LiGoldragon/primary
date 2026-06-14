# Structural Forms integration sidecar

Operator sidecar after reading:

- `reports/designer/627-structural-forms-the-concept.md`
- `reports/designer/628-reality-check-structural-forms-epic.md`
- `reports/designer/630-cross-lane-review.md`
- `reports/designer/631-typeref-reconciliation-outcome.md`
- `reports/system-designer/106-domain-coarsening-operator-handoff.md`
- operator reports `377` and `378`

## What I did

I turned the best currently compatible parts of the Structural Forms work into a
pushed branch family named `structural-forms-integration`.

The branch family is eight repos now:

| Repo | Pushed head | What landed |
|---|---:|---|
| `nota-next` | `00d00504` | Combined structural leaf shapes: `PascalHeadBody` plus `HeadedAtom`. |
| `triad-runtime` | `7a84034b` | Generic reaction frame: `Work<Event, Write, Read, Effect>` and `Action<Reply, Write, Read, Effect, Continuation>`. |
| `schema-next` | `2bb0228e` | Reconciled structural TypeReference grammar: full-word heads and flat `(Map K V)`. |
| `schema-rust-next` | `573375da` | Reaction-frame and structural-forms emission against the integrated grammar. |
| `signal-spirit` | `e85830b1` | Contract crate repinned to integrated NOTA/schema emitter, fmt-clean. |
| `meta-signal-spirit` | `cc576705` | Meta contract repinned to integrated NOTA/schema emitter and `signal-spirit` branch. |
| `sema-engine` | `1afcd012` | Engine decomposition / versioned plane integration. |
| `spirit` | `d2cf86fd` | Store decomposition integrated onto the post-split contract world. |

Verification run:

- `cargo test` on `triad-runtime`, `schema-next`, `schema-rust-next`,
  `sema-engine`, and `spirit`.
- `cargo test --features nota-text` on `signal-spirit`,
  `meta-signal-spirit`, and `spirit`.
- `cargo fmt --check` on the touched repos where formatting mattered; applied
  rustfmt where needed.

Ignored Nix integration tests were not run.

## What I deliberately did not do

I did **not** deploy anything.

I did **not** merge the old `mirror-shipper` branch into `spirit`.

I did **not** add `MirrorTarget` to the stable meta-signal contract. That remains
the correct call from operator report `378` and designer report `630`: if mirror
configuration lands, its eventual home is `meta-signal-spirit`'s `Configure`
contract, but only when the mirror policy is a committed feature. It should not
come along as stale daemon-local vocabulary.

I did **not** keep the old `spirit` `0.13.1` version bump. The branch currently
stays on `0.12.1` because this is an integration branch, not a production release
candidate. Version bumping should happen when the deploy bundle is selected and
the migration/deploy gates are green.

I did **not** implement the system-designer domain coarsening handoff (`106`).
That is a separate production migration over the live intent store.

## How this relates to Designer's reports

Designer report `627` names the right paradigm: **Structural Forms**. The branch
family implements a first real substrate slice of that idea:

- NOTA gets the shape derives needed by the reconciled TypeReference grammar.
- `schema-next` stores TypeReference structure as full-word, generic
  applications with flat `Map`.
- `schema-rust-next` emits the structural forms into Rust.
- Spirit contract crates are pinned into the same NOTA/schema universe so text
  clients do not split across two incompatible `NotaDecode` traits.

Designer report `631` says full TypeReference self-hosting is still partial
because the top-level `TypeReference` node needs named-field / sum-head derive
support. My implementation agrees. I did not pretend that seam was gone.
`schema-next` still has a hand-written delegating implementation where the derive
cannot yet express the shape.

Designer report `630` said operator should integrate reaction-frame,
sema-engine stack, nota-next leaf shapes, and `spirit` store decomposition while
dropping standalone mirror-shipper. That is the shape I followed.

Report `628` and operator report `378` settled the meta-signal split. My `spirit`
integration preserves that boundary: local `schema/meta-signal.schema` and local
generated `src/schema/meta_signal.rs` stay deleted, and `spirit` imports
`meta-signal-spirit`.

System-designer report `106` is about a different deploy train: the domain
taxonomy coarsening. It should be sequenced against this SEMA/Spirit store
tower, not mixed blindly into it.

## The 0.13.x deployment question

The old 0.13.x tower was left undeployed because it was not a clean deploy
artifact. It combined several dangerous things:

- production store-layout migration;
- store decomposition;
- versioned log / outbox work;
- mirror-shipper direction;
- daemon-local meta-signal edits from before the contract split;
- `MirrorTarget` in the wrong layer;
- known migration concerns such as `primary-im1l` (v7 to v9 fold dropping
  referents);
- mirror deploy risk (`primary-x3l7`: mirror bound on `0.0.0.0:7474` without
  auth).

That is why I describe the old 0.13.x branch as reviewed tower work, not a
release candidate.

The new `structural-forms-integration` family is an attempt to extract the good
parts into a cleaner substrate:

- keep the SEMA/store decomposition pieces that build and test;
- keep the post-split signal/meta-signal ownership;
- keep the TypeReference/Structural Forms branch family coherent;
- drop mirror policy until its deploy gate is solved;
- leave the production version bump and deployment sequencing to a later,
  explicit release step.

## What I think now

The current branch family is useful as an integration base, but it is **not yet
the production deploy answer**.

It may satisfy part of `primary-qu28` (the integration bead for the SEMA-VC /
store tower), but it does not close the full production tower if that tower is
defined to include mirror shipping, VersionReport store axes, rebuild-from-log
deploy gates, and live-store migration proof.

The cleanest sequencing looks like this:

1. Treat `structural-forms-integration` as the coherent code integration base.
2. Decide whether it is meant to become the SEMA-VC deploy candidate or only a
   lower substrate for it.
3. If it becomes the deploy candidate, add the missing deploy-only work
   deliberately: version bump, staging-copy migration proof, any required
   `spirit-migrate-store` behavior, and release notes.
4. Keep domain coarsening (`106`) as the next migration step unless the owner
   explicitly chooses to bundle both migrations in one pass.
5. Keep mirror shipper out until mirror auth/bind is solved and `MirrorTarget`
   is added to `meta-signal-spirit` intentionally.

## Questions for the psyche

1. Should `structural-forms-integration` be promoted into the new SEMA-VC deploy
   candidate, or is it only the clean integration substrate beneath a later
   deploy branch?

2. Should Spirit's version stay `0.12.1` on this integration branch until deploy,
   or should the branch itself claim the `0.13.x` line now that it carries store
   decomposition?

3. Is `primary-qu28` considered satisfied by this cleaned branch family, or does
   it remain open until rebuild-from-log, migration proof, and deployment are
   complete?

4. Should `primary-im1l` be solved by fixing the v7 to v9 referent fold, or by
   rejecting v7 as nonexistent/unsupported as system-designer `106` hints for
   pre-v7 stores?

5. Should the domain coarsening migration (`106`) be strictly after the SEMA-VC
   deploy, or should system-operator bundle both migration steps into one staged
   live-store pass?

6. Should `MirrorTarget` wait for the mirror auth/bind fix and then enter
   `meta-signal-spirit`'s `Configure`, or should mirror shipping be removed from
   the near-term Spirit deploy story entirely?

7. Do you want `signal-spirit` and `meta-signal-spirit` to stay in this branch
   family permanently whenever `nota-next` changes, or should contract repos
   normally stay on main and only join when `nota-text` trait coherence requires
   it?

## Operator recommendation

Use this branch family as the clean integration base. Do not deploy it as-is.

Next operator/system-operator work should be one of two explicit paths:

- **Deploy path:** turn this branch family into a release candidate with a
  staging-copy migration test and version bump, then deploy before domain
  coarsening.
- **Substrate path:** leave it as an unmerged integration branch, let
  system-operator implement report `106` separately, and later reconcile both
  migrations into one deployment plan.

I lean deploy path only if someone explicitly owns the staging-copy migration
proof. Without that proof, merging code is fine; touching the live intent store
is not.
