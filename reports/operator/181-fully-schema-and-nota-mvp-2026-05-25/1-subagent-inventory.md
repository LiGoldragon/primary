# Subagent Inventory

## Designer And Second-Designer Material

The strongest reusable design came from:

- `reports/second-designer/181-counter-ego-mvp-leans-2026-05-25.md`: P0/P1 ordering, with ShortHeader and schema-derived routing ahead of full upgrade emission.
- `reports/second-designer/182-schema-crate-state-and-version-projection-derivation-2026-05-25.md`: schema already has parser, reader, assembler, diff planner, and `Upgrade` feature support; missing part is generated `VersionProjection`.
- `reports/designer/334-v2-multi-pass-nota-first-schema-reader.md`: the six-pass model: lexer, generic tree, structural positions, macro identification, macro application, assembly.
- `reports/designer/329-schema-macro-component-extensibility.md`: builtin macros should be small typed macro variants whose inputs are data-carrying records at node-definition points.

The stable conclusion: the generic NOTA value tree belongs in `nota-codec`; schema-specific lowering belongs in `schema`; Rust emission belongs later in the signal/schema macro crates.

`reports/designer/336-designer-leans-on-27-psyche-questions-and-mvp-plan.md`
adds the current MVP posture: replace the old streaming reader with
one canonical NOTA-tree surface, keep schema as the source of truth,
and unblock later supervisor / upgrade ceremony work with test stubs
only after the schema shape layer is real.

## Second-Operator Material

`reports/second-operator/187-nota-shape-logic-and-schema-upgrade-macro-2026-05-25.md` had already landed the first foundation:

- `nota-codec` main had `NotaDocument`, `NotaValue`, `NotaMapEntry`, `NotaAtom`, `NotaString`, `NotaStringKind`.
- `schema` main had a proof test over `tests/fixtures/schema-e2e/spirit-v0-1-1.schema`.

The gap after /187 was not "does a generic tree exist"; it was "does the schema reader and macro-pipeline logic actually use it as the operating substrate?"

`reports/second-operator/188-real-schema-node-method-macro-situation-2026-05-25.md`
correctly found the rebase risk in the first operator branch:
`nota-codec` main already had `ByteRange`,
`Lexer::next_token_with_span`, and `parse_str`. The NOTA branch in
this slice was rebased onto main and reverified so those APIs are
preserved rather than regressed.

The async research lane for Spirit record `602` sharpened the code
boundary: `nota-codec` should expose `NotaValueKind` and shape helpers;
`schema` should expose relationship enums such as document position,
node-definition point, and builtin macro variant. The next refinement
is making those relationship enums more public and testable.

## Worktree State

The useful worktrees were:

- `/home/li/wt/github.com/LiGoldragon/schema/multi-pass-nota-reader`: earlier six-pass proof.
- `/home/li/wt/github.com/LiGoldragon/schema/fully-schema-and-nota-mvp`: chosen schema implementation lane.
- `/home/li/wt/github.com/LiGoldragon/nota-codec/fully-schema-and-nota-mvp`: chosen NOTA implementation lane.

Designer-owned nspawn and handover worktrees were relevant for the later Spirit cutover but were not edited in this slice.
