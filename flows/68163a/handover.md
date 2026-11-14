# Handover, Psyche audit Primary 68163a

Done: landed "a subflow's reply is a datom of a type its role declares; a failing subflow returns one variant and no report" in psyche-belief vision/subflows.md (63dc0ab), skills regenerated, item struck from flows/0c5b6e/undone.md Handovers, Secondary told by pane wKZ:p1.

Next: "Four v1 additions: harness as a definition (feature can add or remove); flow knows its metaflow by name; new metaflow told by replaying definitions; Rehearse in the v1 Signal" (source flows/383169/vision/handover.md line 47). Verify first: as of 2004e6b, vision:flow-nexus-v1 already holds the harness as a definition with Feature.Effect and Member.Features, Rehearse in its Signal, and a flow knowing itself by Identity; vision:metaflow-v1 holds the replay of definitions into a new place. What is likely still missing: a flow knowing its metaflow by name at launch (Identity carries Address and FlowId only), and vision:versioning's side-by-side-only line. Land only what the modules lack.

After it: per-metaflow environment-variable effect; then the items of the Handovers section in order that name a belief module.

Belief repos: /git/github.com/LiGoldragon/{psyche,mind,field}-belief, commit and push main, then context-skills-regenerate. Report each landing to Psyche core Secondary with herdr --session default agent prompt wKZ:p1. Use flow-0.50 for Send and Launch.
