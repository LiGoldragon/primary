# Operator comparison — meta-signal split vs Designer

## Scope

Compared the landed operator implementation against Designer's current durable
surface:

- `reports/designer/628-reality-check-structural-forms-epic.md`
- Designer Spirit worktrees under `~/wt/github.com/LiGoldragon/spirit/*`
- current `meta-signal-spirit` main
- current `spirit` main

I did not find a separate Designer `meta-signal-spirit` implementation
worktree. The executable Designer evidence is older Spirit feature-branch
state where `schema/meta-signal.schema` remains daemon-local. The report is
therefore a comparison of the operator split against Designer's stated target
and the older local-contract branch shapes.

## Verdict

The operator implementation matches Designer's correction in report 628: the
owner-only meta contract is now a real schema-derived `meta-signal-spirit`
contract crate, and `spirit` imports it instead of emitting its own local
meta-signal module.

The landed shape is narrower and cleaner than the older Designer worktree
shape:

- `meta-signal-spirit` owns `schema/meta-signal.schema`,
  `src/schema/meta_signal.rs`, examples, and contract tests.
- `spirit` removed `schema/meta-signal.schema` and
  `src/schema/meta_signal.rs`.
- `spirit::schema::meta_signal` remains available as a re-export, so existing
  Spirit runtime/tests do not need local generated ownership.
- `spirit/build.rs` imports dependency schema from both `signal-spirit` and
  `meta-signal-spirit`, then emits only daemon-local Nexus, SEMA, and daemon
  modules.

This is the correct ownership boundary. Designer's stated drift is fixed on
main.

## Designer branch comparison

`operator-guardian-hardening` has a daemon-local meta schema with only
`Configure`.

`mirror-shipper` has the same daemon-local schema promoted to `Configure` and
`Import`.

`vc-followups` has daemon-local `Configure` and `Import`, plus mirror-specific
`MirrorTarget` fields folded into `ConfigureRequest` / `ConfigureReceipt`.

The operator implementation takes the middle vocabulary, not the latest
branch-specific extension: `Configure` and `Import` are split into
`meta-signal-spirit`, while `MirrorTarget` stays out. That is the right call
for this slice because mirror shipping is a separate feature branch concern,
not part of the stable Spirit meta-policy contract split.

## Implementation quality

Positive:

- The stale hand-written `Start` / `Drain` / `Reload` / `Register` / `Retire`
  placeholder surface is gone from the contract code.
- The new contract imports shared Spirit nouns from `signal-spirit` instead of
  duplicating `Entry`, `RecordIdentifier`, `RecordCount`, or `DatabaseMarker`.
- The default contract build is binary-first; NOTA text is feature-gated.
- The split has actual witnesses: frame tests in `meta-signal-spirit`,
  public-surface/dependency-surface tests in `spirit`, and the existing
  `meta_configure` behavior tests still pass against the imported type.

Residuals found and fixed during this comparison:

- `spirit/ARCHITECTURE.md` still listed `src/schema/meta_signal.rs` as a
  daemon-local generated module. It now lists only `nexus`, `sema`, and
  `daemon` as daemon-local generated modules.
- `meta-signal-spirit/skills.md` still said request variants were declared
  through `signal_channel!`. It now points at schema roots in
  `schema/meta-signal.schema`.

## Open pressure

There is no functional gap in the split itself. The next comparison point is
branch integration: any Spirit feature branch derived before this split that
still edits local `schema/meta-signal.schema` must be rebased by moving stable
meta contract vocabulary into `meta-signal-spirit` and leaving daemon-local
behavior in `spirit`.

The one known vocabulary choice is `MirrorTarget`: keep it branch-local until
the mirror shipper design lands as a committed Spirit meta-policy feature. Do
not smuggle it into the contract merely because the VC follow-up branch has it.
