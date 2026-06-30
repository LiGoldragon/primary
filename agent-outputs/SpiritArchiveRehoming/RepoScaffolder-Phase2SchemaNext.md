# Phase 2 Append — schema-next ARCHITECTURE Integration

## Task and scope

Integrate the durable direction of the 110 archived Spirit records routed to
`repos/schema-next/ARCHITECTURE.md` into that single surface. Not a raw dump:
records were grouped thematically, synthesized into coherent prose, woven into
the existing direction surface, and deduped against substance already present.
Target repo is `/git/github.com/LiGoldragon/schema-next` (own git+jj).

## Inputs consulted

- Routing manifest: `agent-outputs/SpiritArchiveRehoming/RoutingManifest.md`
  (the schema-next section lists the 110 record ids; none in that section is
  `[SECRET]`).
- Record dump: `/tmp/spirit-archive-extract/archived-spirit-records.dump.md`
  (id -> full description). All 110 blocks extracted and read in full.
- Existing target: `schema-next/ARCHITECTURE.md` (already a rich direction +
  mechanics surface before this change).
- `schema-next/flake.nix` (to identify the narrow scaffold check).

## Secret redactions

None. The three `[SECRET]` ids in the manifest (`go41`, `wn7q`, `2qhw`) route to
CriomOS-home and lojix-cli, not schema-next. No secret value was read or written
for this surface; a post-edit grep for those ids and for SECRET/REDACT markers in
the file returned empty.

## Records integrated (count)

All 110 accounted for:

- 80 integrated as new, cited prose.
- 30 consciously deduped — their substance is already fully carried by the
  existing doc (e.g. SpecifiedSchema IR, Asschema removal, TypeReference/
  TypeDeclaration sums, struct brace map, scalar pass-through, header resolution,
  duplicate rejection, multi-pass NOTA-first reader, package/import resolution,
  forward references, generics/pipe-brace traits). Two of these (`dqmc`, `ymq8`)
  describe the older `@`-binder form that the existing doc explicitly marks
  abandoned (`own9`); integrating them as current would have contradicted the
  settled design, so only their still-live substance (already present) stands.

Deduped ids: `3742 6cfr 6grf bkzd oxgh lf7y esn1 hrte tbff 3don mcuk 9uje p8sq
qv4q kfqa 1sa2 2i75 c8lc 6jdv uujd i8wt 20id ymq8 dqmc 31nz h053 ppuk d3r2 ba6d
7c71`.

## Sections touched

Existing `## Direction` was restructured from a flat bullet list into grouped
subsections and substantially expanded; four new top-level sections were added at
the end; two existing mechanics sections gained a few woven paragraphs. File grew
from ~639 to 1077 lines and remains a readable direction surface, not an appended
bullet wall.

- `## Direction` -> new subsections:
  - `### What schema is` — `1aam ycmd er9w g2xr khbv sanf tace ospz`.
  - `### Foundational model` — `umsv 2cuo b05y a5tg wvpg 2f04 gjr1`.
  - `### Authored-syntax direction` (states the positional-list / no-star future
    direction explicitly distinct from the implemented brace+star surface) —
    `6wwf a5tg 5jac iypq yp29 94sj izib mn3k tw15`.
  - `### Settled architecture choices` (absorbed the original Direction bullets +
    new ones) — `hl1z i9xk bw9v b0v3 9yxh uuh7 yngr 58bv 5mxn ddlv t5wx neib mqlb
    brgo`.
- `## Runtime Planes the Schema Describes` (new) — `2v9u rmv8 7118 ugig z9kv mimk
  l1ip rmqo m76h w6y1 oe6s`; `### Engines and the request pipeline` — `o8x5 str0
  ooxy`; `### Effect table and the match-matrix surface` — `udjq xiqa ujb2`.
- `## Contracts, Channels, and the Component Triad` (new) — `26e7 nm97 f8ds l6zw
  c8b3 xbc2 fhe8 8u1o fry8`.
- `## Schema as a System` (new) — `xbu8 uzxp cbtg wx5c xqkv hckx h9xd`.
- `## Macro Dispatch and Composition` (new) — `506w pul9 rfg9 d6if qe84 xprx sd7x
  e8iu b0s4`.
- `## Semantic Schema` (existing, +1 paragraph) — `3itj` (deep type trees + type
  index).

## Changed files

- `schema-next/ARCHITECTURE.md` — the only content change.

## Checks run and exact result

- `nix flake show --no-write-lock-file` -> exit 0 (flake evaluates; "dirty tree"
  warning expected for the uncommitted edit at the time, now committed). No flake
  check inspects `ARCHITECTURE.md`, so the documentation edit cannot break the
  Rust build/test or the source-discipline guards; flake evaluation is the
  correct narrow scaffold check for a doc-only change and it passes.
- Markdown hygiene: no `---` horizontal rules; coherent `##`/`###` section tree;
  secret-id grep empty.

## Pre-flight gate and publish

- Before editing: `@` was an empty change with `main` as parent; `main` ==
  `main@origin` (not behind); working copy clean. Re-fetched immediately before
  commit — still in sync, no divergence.
- Claimed `schema-next/ARCHITECTURE.md` via Orchestrate (lane `repo-scaffolder`);
  released after push.
- Commit: `357eac0e4562` (jj change `unvxmttw`), message
  `rehome: integrate archived intent records into ARCHITECTURE` with the
  `Co-Authored-By: Claude Opus 4.8 (1M context)` trailer.
- `jj bookmark set main -r @-` then `jj git push --bookmark main` ->
  `Move forward bookmark main from 184516e21237 to 357eac0e4562`, exit 0
  (fast-forward, never a sibling-of-main). `main` and `main@origin` now both at
  `357eac0e`.

## Blockers, unknowns, follow-up

- None blocking. The integration is published.
- Provisional note for the psyche (recommendation, not new authority): several
  integrated records describe a future authored syntax (bare positional struct
  field lists with a dot differentiator; retirement of the `*` star shorthand and
  the name-value struct form) that the current implemented surface in the same
  file has not adopted. This tension is deliberately preserved: the implemented
  surface stays described as-is, and the future shape lives only under
  `### Authored-syntax direction`. When the codebase migrates to the positional
  form, the implemented-surface sections (Strict Key/Value Schema Syntax,
  Constraints) will need a follow-up reconciliation pass.
