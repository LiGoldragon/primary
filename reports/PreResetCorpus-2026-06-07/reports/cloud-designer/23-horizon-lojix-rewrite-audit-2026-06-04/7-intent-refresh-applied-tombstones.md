# Intent-refresh applied — tombstones for the removed originals

Cloud-designer, 2026-06-04. The psyche approved applying agglomeration
proposals 1, 2, 3, 5, 7 from file `2`. This file is the **tombstone
provenance** for the originals removed by that application, per
`skills/intent-maintenance.md` §"Removing a record — tombstone first". Each
removed record's full verbatim text + daemon-stamped provenance is preserved
here BEFORE removal, because Spirit removal is destructive and irreversible
(redb copy-on-write reuses the freed bytes within hours). This report IS the
provenance of what was removed.

## Fresh records that rehome the substance (captured first)

- `5ropw7qgw06oyyh3gw5` (Principle, VeryHigh) — Horizon minimalism, both axes
  (Proposal 1). Replaces `7ggswqdxqqz97za6o7w`, `10v4744869xt5spwnam`.
- `4go2t3ek2rcgvo3w0xx` (Decision, VeryHigh) — the Horizon/lojix rewrite charter
  (Proposal 2). Replaces `1bok2bxvu3beswif9mv`, `75auhtr308tgt4kaa9a`,
  `6pmeinb6tqtdotsgi4u`.
- `7n4gjopir5dyk4bfznr` (Clarification, High) — the surviving types-only-module
  nugget (Proposal 3). Replaces `1vymk533gmb43v78e46` (its open trichotomy is
  dead; the nugget re-captured at High).
- `29w2hwko8d7mr2jh943` (Correction, VeryHigh) — the plane-schema shape
  (Proposal 5). Replaces `7joz3dmegqiptqgra5p`, `1up1ufia24c2opn3mqn`,
  `2auv4uvj4cr71iy2emj`, `2bgatqufm9m0dktxkv5` (the last was Cert-Zero —
  folding it removes a misleading low-certainty artifact).
- `275awyobkhghbta326w` (Decision, High) — the meta-signal fleet rename
  (Proposal 7). Replaces `3lchri1gcxm3mc7ltm3`, `2hstvjvbxb8z0tp0xsp`,
  `1n5b0k32jjw75rhgkb6`; and `3i3hed0a6790r2clvo3` retired as stale/contradicted
  (it asserted owner-signal stays active; the three High records reverse it —
  not folded, just removed).

Three new session decisions were also captured (additive, not part of the
agglomeration): `1cfsmclkytl551wt5hn` (port-first sequencing),
`4pr9hz8q6phg3lb6awc` (Horizon partial collapse after cutover),
`11yimmwp4pueiudhl30` (lojix two-contract authority split, meta-signal-lojix
path-dep now).

## Removed records — verbatim text + provenance

### Proposal 1 cluster
- `7ggswqdxqqz97za6o7w` [horizon cluster-data nix-composition what-not-how minimal] Principle, High, 2026-06-04 15:04:42 — [Horizon and the cluster-data it carries should be elegant and minimal — they express only WHAT the psyche as cluster user wants the cluster to do, never HOW and never decision-making. Horizon emits simple typed facts that Nix consumes; Nix composes those facts into the more complex decisions, so complexity stays out of Horizon. This is the upstream design principle for the Horizon rewrite.]
- `10v4744869xt5spwnam` [horizon cluster-data type-design input-output-reuse minimal] Principle, High, 2026-06-04 15:04:47 — [Horizon data types should not repeat themselves across inputs and outputs — where the input type can also serve as the output type, reuse it rather than defining parallel in and out types. Fewer, reused types keep the rewritten Horizon model small.]

### Proposal 2 cluster
- `1bok2bxvu3beswif9mv` [horizon lojix runtime-shape triad-port hack-for-now] Clarification, High, 2026-06-04 15:04:49 — [Horizon is more of a hack for now and that is acceptable — it stays the simple projection surface, not a full triad component. Logix, the lojix component, is the more traditional component that receives the full triad-engine and schema-based-component port. This clarifies the earlier open runtime-shape question that left Horizon possibly-signal possibly-triad possibly-pure-projection: Horizon leans pure-and-simple, Logix carries the runtime triad.]
- `75auhtr308tgt4kaa9a` [horizon lojix rewrite cutover retire-dual-stack goal] Decision, High, 2026-06-04 15:04:51 — [Finish the Horizon and Logix lean rewrite to the point of cutover and retire the dual production-and-next deploy stacks. The standing burden of maintaining Stack A production and Stack B next in parallel should end; the rewrite is prioritized to reach parity and switch over.]
- `6pmeinb6tqtdotsgi4u` [criomos lojix horizon] Decision, High, 2026-05-27 09:19:34 — [Port high-confidence production CriomOS changes into the next Lojix and Horizon rewrite stack immediately where the correct change is clear, then test those builds.]

### Proposal 3 cluster
- `1vymk533gmb43v78e46` [horizon runtime-shape triad signal component] Clarification, Medium, 2026-05-28 08:23:39 — [Horizon runtime shape is open and the psyche is explicitly unsure: maybe Horizon has only a signal plane, maybe Horizon should be reconceived as a full triad component (signal plus nexus plus sema), maybe it stays a pure projection library. The datatype-generation concept should illuminate this rather than force it - the datatypes generate regardless of runtime shape; the runtime-shape decision is surfaced as open exploration. Note: a pure-projection-library Horizon would need the types-only-module schema shape (the report 39 finding that the 4-position document forces a signal plane); reconceiving Horizon as a triad component gives it Input/Output naturally.]

### Proposal 5 cluster
- `7joz3dmegqiptqgra5p` [schema component-triad daemon] Correction, VeryHigh, 2026-06-04 12:02:18 — [Each runtime plane has its own schema file inside the component daemon crate, for example cloud/schema/nexus.schema. Plane schemas are not separate crates; per-plane crate split is not the triad shape.]
- `1up1ufia24c2opn3mqn` [schema triad nexus sema daemon plane component-shape] Decision, High, 2026-06-04 12:03:05 — [The daemon owns its Nexus and Sema plane-schemas as separate schema files inside the daemon crate — for example cloud/schema/nexus.schema and cloud/schema/sema.schema — each importing the wire contract Signal Input and Output. Planes are separate SCHEMAS but NOT separate crates or repositories: there is no per-plane nexus-component or sema-component crate. One daemon crate carries its nexus.schema and sema.schema together, which requires schema-next to read more than one plane-schema per crate. Settles the placement left open by records 2597 and 2598.]
- `2auv4uvj4cr71iy2emj` [schema component-triad signal nexus sema contract-daemon-split] Correction, High, 2026-06-04 11:54:15 — [A schema-derived component triad is not one daemon schema file with Signal, Nexus, and SEMA sections. The triad has separate schema interfaces/files for the planes — at least Signal, Nexus, and SEMA schemas — with each plane declaring its own imports/exports, input, output, and namespace. Contract schemas remain wire-only Signal contracts; daemon runtime composition imports and connects the separate plane schemas instead of embedding Nexus and SEMA sections inside the contract or inside a single all-in-one daemon schema. The current all-in-one Spirit pilot is a bootstrap exception and must not be treated as the canonical contract/daemon split shape.]
- `2bgatqufm9m0dktxkv5` [schema triad signal nexus sema plane component-shape] Correction, Zero, 2026-06-04 11:56:11 — [Each runtime plane is its own schema. A triad component is three schemas minimum — a Signal schema for the wire contract, a Nexus schema for decisions, a Sema schema for durable state — not one all-in-one schema carrying Signal, Nexus, and Sema sections. There are no plane sections inside a single schema file: a Nexus interface has its own schema and a Sema interface has its own schema, which is what triad means. The schema-derived generator emits PER PLANE — a Signal schema emits wire types and codec only with zero engine traits, a Nexus schema emits the Nexus engine, a Sema schema emits the Sema engine — not a per-component contract-versus-daemon mode. The spirit pilot and the cloud port wrongly authored all three planes in one lib.schema and agents copied that all-in-one shape; that is the misunderstanding being corrected. Sharpens record 2593.]

### Proposal 7 cluster
- `3lchri1gcxm3mc7ltm3` [component-triad naming policy-signal meta-signal] Decision, High, 2026-06-03 18:55:00 — [The owner-signal to meta-signal rename is now active work, not tentative: run a deep rename pass that audits and updates the workspace guidance and affected contract repositories from owner-signal-* policy-contract naming to meta-signal-* where the policy-signal role is meant.]
- `2hstvjvbxb8z0tp0xsp` [workspace-wide rename owner-signal meta-signal fleet-rename naming-convention policy-contract designer-458-fleet-wide] Decision, High, 2026-06-02 11:25:36 — [Workspace-wide rename — all existing owner-signal-* contract repos rename to meta-signal-* as a fleet operation. The 13 affected repos: owner-signal-agent owner-signal-cloud owner-signal-domain-criome owner-signal-mind owner-signal-orchestrate owner-signal-persona owner-signal-persona-spirit owner-signal-repository-ledger owner-signal-router owner-signal-sema-upgrade owner-signal-terminal owner-signal-upgrade owner-signal-version-handover. Workspace standard policy-contract naming becomes meta-signal-<component> uniformly. Resolves designer 458 Option B at fleet scope. Future components follow meta-signal- convention from inception.]
- `1n5b0k32jjw75rhgkb6` [component-triad signal contract naming] Correction, High, 2026-06-04 13:34:54 — [Policy signal repositories use the meta-signal- prefix, not owner-signal-. The owner wording is stale; meta is the better canonical name for all policy-signal contract repos.]
- `3i3hed0a6790r2clvo3` [component-triad] Clarification, Medium, 2026-05-23 12:43:18 — [owner-signal remains the active policy-signal naming convention until an explicit rename lands] (RETIRED as stale/contradicted, not folded.)
