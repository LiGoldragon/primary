# 670 — Offline-e2e unblock: frame and method

Report 669 (the build round) showed the offline first green is not spirit-only: re-landing the
spirit→mirror shipper is blocked by two upstream gaps. This round clears them, in parallel, on
designer feature branches (operator integrates to code-repo main).

The two unblocks (669 §"corrected critical path", handoffs H1+H2):

| # | Slice | Repo | Goal |
|---|---|---|---|
| 1 | re-add the `MirrorTarget` schema noun | meta-signal-spirit | spirit's `mirror-shipper` `configure()` + test can name `MirrorTarget`/`MirrorAddress` + a `mirror_target` slot on the meta `ConfigureRequest`; author the schema, regenerate (no hand-written nouns) |
| 2 | forward-port the `Arc<Engine>` `ComponentShipper` onto mirror main | mirror | spirit (which holds `Arc<sema_engine::Engine>`) can construct a shipper sharing one engine; additive on the green/deployed nota-next-0.5 lineage, keeping `end_to_end_arc.rs` green |

Independent repos → parallel, no collision with each other or with system-designer's active
`criome-auth-pilot` / `router-network-transport` branches. After both land, the next round re-pins
spirit's `mirror-shipper-reland` to these branches, gets the feature + `tests/mirror_shipper.rs`
green (H3), and writes the option-(b) full-chain harness (P5) — that round also needs the operator
cross-branch pin unify (H4). Synthesis is the highest-numbered file here.
