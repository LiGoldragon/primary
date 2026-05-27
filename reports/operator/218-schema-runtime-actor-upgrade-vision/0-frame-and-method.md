# 218 — schema runtime actor upgrade vision

Kind: Synthesis
Topics: schema runtime actor upgrade spirit nota

## Frame

The psyche's current direction tightens the schema stack around one
runtime principle: schema-authored objects become the Rust nouns that
actors exchange, match, store, upgrade, and implement behavior on.

This session splits three report lanes from the implementation work:

- `1-designer-prototype-and-intent-synthesis.md` surveys fresh design
  reports and prototype branches.
- `2-skill-manifestation-targets.md` identifies workspace-skill edits.
- `3-repo-manifestation-targets.md` identifies repo-specific
  architecture and intent edits.

The operator path in parallel is to keep the current `nota-next`,
`schema-next`, `schema-rust-next`, and `spirit-next` implementation
closer to that rule with Nix-visible witnesses.

## Method

The implementation pass is constrained to surfaces already in flight:

- Manifest durable psyche intent in the relevant repo `INTENT.md` and
  `ARCHITECTURE.md` files.
- Keep generated Rust under `src/schema/`, where agents can implement
  methods against the visible generated nouns.
- Keep source tests in Nix checks, including structural witnesses for
  schema macro lowering and generated source paths.
- Avoid legacy macro fallback surfaces in the new schema-derived stack.
