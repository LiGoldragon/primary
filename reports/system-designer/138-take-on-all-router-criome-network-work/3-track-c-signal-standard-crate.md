# 138/3 — Track C: the `signal-standard` crate (sound, built green, local)

*Build → adversarial verify. Verdict: **sound**, build reproduced and the
report's own caveats exceeded (freshness proven, discipline checks built to
completion, `nix flake check` evaluated green).*

## Result

New local repo **`/git/github.com/LiGoldragon/signal-standard`** (colocated
jj+git, **no remote**), branch `signal-standard-bootstrap`, commit `3f9d75ee`
(change `wzuzvtut`), worktree at `/home/li/wt/github.com/LiGoldragon/signal-standard/main`.
It is the second shared `signal-` library alongside `signal-frame` — a pure
cross-component vocabulary crate.

`schema/lib.schema` carries the reconciled 681 classification:

- **`ComponentKind` — one closed-but-partitioned 14-variant enum in 5 zones:**
  Core `Spirit/Mind/Criome`; Messaging `Message/Router/Mirror`; Interaction
  `Terminal/Harness/Agent`; Platform `System/Introspect/Orchestrate/Lojix`;
  Aggregate `Persona`. No variant dropped, nothing invented; matches the 681
  census.
- `Differentiator { component ComponentKind, kind AuthorizedObjectKind }` and
  `AuthorizedObjectKind [Operation Contract Agreement Time]` — **byte-identical**
  to `signal-criome`'s originals.
- The four-rung `AuthorizedObjectInterest` lattice (`AnyAuthorizedObject` /
  `Component` / `ObjectKind` / `ComponentObject`) + `ComponentObjectInterest` +
  `AuthorizedObjectReference`, `ObjectDigest`, `ComponentClassification`.

**Key toolchain finding (reusable):** `ContractCrateBuild` (used by criome) is
**wire-only** — it hardcodes the wire-contract emission target and emits empty
`Input`/`Output` roots + `signal_frame` codec scaffolding even when both roots
are `[]`, so it does not compile for a pure-vocabulary crate. signal-standard's
`build.rs` instead composes `GenerationPlan` + `ModuleEmission::declaration_module`
+ `GeneratedPackage::write_or_check` via a `StandardCrateBuild` data-bearing
struct (DeclarationModule target) — types only, no roots/codec/runtime. Two NOTA
fixes from the prototype: `ObjectDigest` is the newtype form (`ObjectDigest
String`, matching criome) not `{ value String }`; the `Differentiator` field uses
bare-field shorthand (the engine rejected the redundant explicit field role).

Green: `cargo build`, `cargo test --features nota-text` (7/7, incl. all 14
roster variants round-tripping), `cargo clippy` (both feature sets) clean,
`cargo fmt --check` clean. **Freshness proven** — re-lowering without the UPDATE
env var leaves the working copy clean, so checked-in Rust exactly matches the
schema (this also resolves 681's open caveat: the positional dot-form schema
machine-validates). `nix flake check --no-build` fully evaluated green (11
checks incl. the custom `rkyv-feature-discipline` + `contract-crate-carries-no-runtime`).

## Remaining (handed to operator / follow-up)

1. **Create the `LiGoldragon/signal-standard` GitHub remote, establish main, push**
   — the one outward-facing step, deliberately left for the operator (who owns
   code-repo main).
2. **Consumer migration (separate coordinated breaking change):** `signal-criome`
   deletes its local `ComponentKind` + `AuthorizedObjectKind` + interest-lattice
   types and imports from here; `signal-persona` deletes its `ComponentKind` and
   retires `ComponentPrincipal` collapsing into the imported `ComponentKind`. Old
   ordinals don't carry over — all consumers rebuild at once. `signal-message`'s
   third `ComponentName` roster (9 variants) is also reconciled here.
3. Add a `signal-standard` row to `protocols/active-repositories.md`.
4. Two P3 cosmetic nits: a misleading `"Wire-only"` doc-comment in `src/lib.rs:10`
   and an unused `examples/` source filter in `flake.nix:39-45`.
