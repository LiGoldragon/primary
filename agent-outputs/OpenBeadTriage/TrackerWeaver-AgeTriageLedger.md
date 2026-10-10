# Open Bead Age-Triage Ledger — `primary-` tracker

## Task and scope
Age-based triage of all OPEN beads in the `primary-` bd tracker. Age is the
staleness signal: older beads are more likely superseded by a moved design
frontier. Reference date 2026-07-02. Authorized action: close stale/suspicious
beads with a specific reversible reason. No reopens, no Spirit intent changes,
no code/doc edits.

Buckets (by bead creation date):
- **> 1 month** — created on/before 2026-06-02 ("almost guaranteed nonsense") → CLOSE by default, fast skim.
- **2 weeks – 1 month** — created 2026-06-03 … 2026-06-18 ("very suspicious") → close unless clearly still-live.
- **< 2 weeks** — created 2026-06-19 onward → keep, list only.

## Commands / sources consulted
- `bd count --status open` and per-status counts.
- `bd export -o …` (JSONL) for authoritative created_at/status/title/priority, parsed with `jq`.
- `git log --since=2026-06-10` to gauge which lines of work are live (liveness signal for spare/keep decisions).
- `bd close <id...> -r "<reason>"` for mutations; `bd show` / re-export for verification.

## Authoritative counts

| Status | Count (before) |
|---|---|
| open | **222** |
| in_progress | 6 (spared by default) |
| blocked | 2 (spared) |
| deferred | 1 (spared) |
| closed (pre-existing) | 771 |

Open-bucket distribution (of the 222):

| Bucket | Created | Count | Closed | Kept/Spared |
|---|---|---|---|---|
| A: >1mo | ≤ 2026-06-02 | 45 | **45** | 0 spared |
| B: 2wk–1mo | 2026-06-03 … 2026-06-18 | 33 | **24** | 9 kept |
| C: <2wk | ≥ 2026-06-19 | 144 | 0 | 144 kept |

**Total closed this pass: 69.  Open before: 222 → Open after: 153.**  (Verified: `bd count --status open` = 153; the only open beads created ≤ 2026-06-18 are the 9 bucket-B keeps.)

## Liveness signals used (recent commit volume since 2026-06-10)
criome/criome-auth ~102 · router/networking ~31 · sema ~24 · positional & schema-next ~17 each · mirror ~11 · intent-substrate/Listener/strict-positional store-migration landing 2026-07-01/02. Beads clearly mapping to these active frontiers were spared/kept; predecessor design threads that the frontier passed were closed.

## Landmine note status
**primary-1y56** ("spirit: drop dead meta-signal-criome [patch]…") was created **2026-06-29** → it falls in the **<2wk keep bucket**, so it was NOT touched and remains OPEN. The flake.nix-unsafe warning is preserved by leaving the bead open; no close reason needed to carry it. Verified open.

## Spared non-open beads (status ≠ open; spared by default per policy)
- in_progress: primary-2y5, primary-a18, primary-a61, primary-devn.1.4, primary-vhb6, primary-at7x
- blocked: primary-6obv.4, primary-jwx0
- deferred: primary-t5vj.3

These are outside the 222 open set and were not modified.

## Bucket A — >1mo (45 closed, 0 spared)
Close reason (uniform, per-bead date substituted): *"Stale by age (>1mo, created <date>); presumed superseded/abandoned per age-triage. Reversible — reopen if still wanted."*

Rationale for zero spares: none of these 2026-05 beads map to a currently-active frontier. Their lines of work are predecessors the frontier moved past — spirit-next cycle-2 followups predate the strict-positional store migration; whisrs RecordingSession predates the live Listener STT line; Horizon rewrite, CriomOS/prometheus/atlas deploys, cluster-registry, and clavifaber items show no recent commits. The lone epic (primary-ipjx, whisrs) has no recent repo activity. The near-uniform 2026-06-19 updated_at is a prior bulk age-refresh, not real activity.

| Created | ID | Title |
|---|---|---|
| 2026-05-08 | primary-obm | lore: audit current doc boundaries and stale agent-path shims |
| 2026-05-09 | primary-fgk | chronos: replace Sky TODOs and Subscribe stub with Phase 1 solar engine |
| 2026-05-09 | primary-npd | horizon-rs: shrink serde to the JSON projection boundary, not proposal parsing |
| 2026-05-09 | primary-oil | whisrs: refresh old feature-gap list into durable RecordingSession follow-ups |
| 2026-05-10 | primary-e3c | cluster registry: choose the long-lived publication registry component, not clavifaber |
| 2026-05-10 | primary-mm0 | clavifaber: decide whether a Prometheus e2e remains beyond existing rootless sandbox |
| 2026-05-11 | primary-8b3 | CriomOS: finish Yggdrasil key ownership handoff from network seed to clavifaber projection |
| 2026-05-11 | primary-da7 | cluster registry mismatch handling: keep lojix read-only until registry/runtime exists |
| 2026-05-11 | primary-tpd | CriomOS: decide overlay roles for Headscale, Tailscale, and Yggdrasil from current modules |
| 2026-05-12 | primary-1ha | CriomOS-test-cluster: add negative Horizon fixtures only after production diagnostics exist |
| 2026-05-12 | primary-58l | CriomOS-test-cluster: add booted DNS/tailnet assertions to existing VM/nspawn suite |
| 2026-05-12 | primary-5u9 | CriomOS: Ghost publication node after container-host substrate exists |
| 2026-05-12 | primary-7ay8 | CriomOS-test-cluster: persist Prometheus runner artifacts outside mktemp sandboxes |
| 2026-05-12 | primary-9wi | CriomOS: add mkCriomOSNode/container-host now that nix role split is done |
| 2026-05-12 | primary-hpx | lojix: materialize GC-root symlinks and retention policy from durable daemon state |
| 2026-05-12 | primary-nvs8 | CriomOS-test-cluster: add synthetic Wi-Fi PKI fixtures after clavifaber/Ygg handoff is wired |
| 2026-05-15 | primary-gfc0 | CriomOS: split metal/default.nix hardware concerns into focused modules |
| 2026-05-15 | primary-k9kj | CriomOS-home: add an unused-input/static-grep check for flake/module drift |
| 2026-05-17 | primary-f6cc | CriomOS: move large-AI model downloads/materialization out of normal system closure |
| 2026-05-17 | primary-ipjx | whisrs: design durable RecordingSession capture after repo-intent repair (epic) |
| 2026-05-17 | primary-izze | tui-criome: long-running meta-signal-criome client after encrypted meta session exists |
| 2026-05-18 | primary-ihee | Horizon rewrite: combine leaner shape with re-engineering |
| 2026-05-23 | primary-0xn7 | arca-daemon: add schema_header redb table + read-on-boot |
| 2026-05-23 | primary-54ti | horizon-rs: migrate to current nota/signal/sema/spirit foundations (per Spirit record 303) |
| 2026-05-23 | primary-srmq | lojix-daemon: authenticated Nix flake resolution via nix-auth crate |
| 2026-05-25 | primary-h1vl | Programmatic extractor for legacy intent files that preserves psyche timestamps |
| 2026-05-27 | primary-1tdr | Multi-connection daemon concurrency — process-boundary witness needed |
| 2026-05-27 | primary-1ubd | Add Gemma 4 E4B multimodal GGUF to atlas (largeAI node) inventory |
| 2026-05-27 | primary-2n1r | Implement schema-diff upgrade trait surface per record 950 |
| 2026-05-27 | primary-6d5n | Exercise 1-byte tag-space partition for Input/Output per record 934 |
| 2026-05-27 | primary-a1px | spirit-next cycle-2 followup: emit OutputNexus client-side dispatcher |
| 2026-05-27 | primary-gxmj | spirit-next cycle-2 followup: schema-diff upgrade trait check |
| 2026-05-27 | primary-jqkq | spirit-next cycle-2 followup: schema-emit observer registration trait |
| 2026-05-27 | primary-lrf8 | Promote mail handling to explicit queue + fanout observers per record 963+970 |
| 2026-05-27 | primary-lrgj | Nix integration tests should run automatically — CI or pre-commit hook |
| 2026-05-27 | primary-pjbp | Wire StructureHeader into spirit-next routing per record 933 |
| 2026-05-27 | primary-y3is | Deploy atlas node + end-to-end smoke through browser-use |
| 2026-05-28 | primary-1xor | Shared schema-core floor imported via cross-crate (de-duplicate emitter-hardcoded runtime floor) |
| 2026-05-28 | primary-a6m0 | Spirit: query intent records by numeric identifier |
| 2026-05-28 | primary-fq9l | prometheus: complete Gemma + sops-auth deploy via BootOnce (never Switch) |
| 2026-05-28 | primary-ia60 | prometheus: confirm router-wifi-projection + possible wifi password change |
| 2026-05-28 | primary-lome | prometheus: establish console/out-of-band access before router deploys |
| 2026-05-28 | primary-si42 | Types-only schema module shape (Input/Output optional) |
| 2026-05-28 | primary-u0by | Wire a live three-engine chain for Horizon (gated on runtime-shape decision) |
| 2026-05-28 | primary-ytdj | prometheus: verify Gemma multimodal (mmproj) works, iterate wiring if needed |

Note: primary-5u9 was silently skipped by its batch `bd close` (batch reported success but the ID stayed open); it was re-closed individually and verified CLOSED.

## Bucket B — 2wk–1mo (24 closed, 9 kept)
Close reason format: *"Suspicious by age (2wk–1mo, created <date>); <why>. Reversible."*

### Closed (24)
| Created | ID | Title | Why closed |
|---|---|---|---|
| 2026-06-03 | primary-am9d | Spirit: named shorthand operation ladder | Not the current Spirit frontier (moved to strict-positional store migration). |
| 2026-06-03 | primary-flwg | Spirit: design true stream archive targets | Early design thread; superseded by later archive/GC direction. |
| 2026-06-04 | primary-dn1e | spirit: add ChangePrivacy operation | Feature-add not evidenced as current frontier; privacy path already exists. |
| 2026-06-04 | primary-es8u | Extract daemon listener/startup runner beyond Nexus loop | Daemon refactor with no recent activity; not a current deliverable. |
| 2026-06-04 | primary-myku | Build RustItem emission token model in schema-rust-next | Likely superseded by the universal-positional schema-next migration. |
| 2026-06-04 | primary-n1ao | Migrate chroma config.rs off removed nota-codec lexer | Tech-debt with no recent activity; frontier moved on. |
| 2026-06-04 | primary-nres | Apply 18 constraint manifestations (designer 504-508) | Those reports are far superseded (designer now past 720). |
| 2026-06-04 | primary-oq0n | Prune ~54 superseded concept branches | Stale branch-prune chore; count outdated; no recent activity. |
| 2026-06-04 | primary-tcg0 | Fix spirit pilot doc/discipline (INTENT.md:206 …) | Premise gone: workspace INTENT.md eliminated/rehomed into ARCHITECTURE.md 2026-06-30. |
| 2026-06-04 | primary-tiyo | New-Spirit concept thread (archive/privacy/feedback/ladder) | Concept thread superseded by the shipped Spirit direction. |
| 2026-06-04 | primary-u4tl | Integrate 3 persona-spirit cleanup commits | Stale integration task, presumed landed/superseded. |
| 2026-06-04 | primary-ukzf | Eliminate shared jj working-copy + shared-main race | Edit-coordination doctrine now governs this; no active bead-driven work. |
| 2026-06-04 | primary-uwo0 | Spirit: removal-candidate archive retrieval/restore | Feature not evidenced as current frontier. |
| 2026-06-04 | primary-vjl5 | Split slow spirit local-stack verification | Testing-infra task with no recent activity. |
| 2026-06-04 | primary-wvey | Redo VmTesting as a TYPED node-service | Superseded by the lojix typed test-authoring design line. |
| 2026-06-04 | primary-y0ec | Peripheral sema-engine boundary strays | Boundary cleanup; not a current deliverable. |
| 2026-06-12 | primary-s22j | Sema VC follow-ups after integration | Vague, no concrete live scope. |
| 2026-06-13 | primary-8dcn | Delete into_next_step shim + reaction-frame migration | No recent activity. |
| 2026-06-13 | primary-x178 | Split engine.rs god-impl and store.rs | Crate-layout refactor chore; no recent activity. |
| 2026-06-14 | primary-3rj9 | Operator integration fixes (schema-next / spirit trace) | Stale integration task. |
| 2026-06-14 | primary-bojw | Self-host macro-table type from core.schema | schema-next design likely superseded by positional migration. |
| 2026-06-15 | primary-v1w7 | Spirit: named private-capture short-form | Feature-add not evidenced as current frontier. |
| 2026-06-15 | primary-xslx | message: direct-delivery fast path (l3k4 clause 2) | message subsystem is not an active frontier. |
| 2026-06-15 | primary-ydfh | message: existence-fact durable / SEMA existence-log (l3k4 clause 1) | message subsystem is not an active frontier. |

### Kept (9) — clearly still-live
| Created | ID | Title | Why kept |
|---|---|---|---|
| 2026-06-04 | primary-ohpk | Add a prominent production marker to persona-spirit | Recently touched (updated 2026-07-01); persona-spirit is production-relevant. |
| 2026-06-13 | primary-4civ | Add failure escalation around spirit migrate-store ExecStartPre | Directly hardens the store-migration path that landed evidence 2026-07-02 (v10→v11). |
| 2026-06-13 | primary-85hv | Build the production mirror shipper driver in spirit | P1 on the active mirror line (~11 recent commits). |
| 2026-06-13 | primary-x3l7 | Rebind mirror TCP ingress off 0.0.0.0; auth before shipping | P1 security-relevant item on the active mirror line. |
| 2026-06-15 | primary-hhp0 | Universal-positional: migrate schema-next streams/families to positional typed-body structs | Maps directly to the strict-positional frontier active 2026-07-01/02. |
| 2026-06-16 | primary-5zur | spirit: criome-auth pilot — out-of-band caller-attestation | criome-auth is the most active frontier (~102 recent commits). |
| 2026-06-16 | primary-9x9f | Networking through the router: signal-router forwarding contract + router daemon transport | P1 on the active router/networking line (~31 recent commits). |
| 2026-06-16 | primary-ebev | workspace: intent-substrate rollout — Spirit as single intent source | The current live workspace direction (intent-substrate / Spirit-as-source). |
| 2026-06-16 | primary-kr40 | criome: real blst Sign/Verify + signed RegisterIdentity + master key lifecycle | P1 on the active criome-auth frontier. |

## Bucket C — <2wk (144 kept, no action)
Full list (created ≥ 2026-06-19), sorted by date:

```
2026-06-19  primary-dw95   P1  Stand up durable VM-host test node on prometheus: VmHost service + TestVm node, BootOnce, Yggdrasil-reachable
2026-06-19  primary-x8by   P1  Act on cloud-engine-audit 68: spine, wire cutover, Hetzner-lead, ad53 CloudNode
2026-06-19  primary-ymww   P2  Deploy cross-host router/criome transport: L1 CI -> L2 Yggdrasil -> L3 ouranos/prometheus
2026-06-20  primary-exzf   P1  De-branch criome cluster test → CriomOS-test-cluster main
2026-06-20  primary-n98t   P1  Land cloud-node feature branches: doris declaration + TypeIs deletion
2026-06-20  primary-unig   P1  CriomOS website-hosting node service (doris's role)
2026-06-22  primary-0bab   P1  Port the Immich agentic media mirror into the CriomOS web-host system
2026-06-24  primary-64s3   P2  Land generated spirit-manual.md in primary; split intent-log into intent-capture
2026-06-24  primary-7d8m.1 P2  Intent-alignment: nota-next -> SpecifiedSchema era
2026-06-24  primary-7d8m.2 P2  Intent-alignment: schema-next -> SpecifiedSchema era
2026-06-24  primary-7d8m.3 P2  Intent-alignment: schema-rust-next -> SpecifiedSchema era
2026-06-24  primary-7d8m.4 P2  Intent-alignment: signal-spirit -> SpecifiedSchema era
2026-06-24  primary-7d8m.5 P2  Intent-alignment: spirit -> SpecifiedSchema era
2026-06-24  primary-7d8m   P2  Intent-layer alignment: schema stack -> SpecifiedSchema era (epic)
2026-06-24  primary-80cw.1 P1  schema-next: define schema-owned rkyv help catalog over SpecifiedSchema
2026-06-24  primary-80cw.2 P1  schema-rust-next: emit embedded help catalogs and type-attached accessors
2026-06-24  primary-80cw.3 P1  schema-daemon: design registry/query contract for schema catalogs
2026-06-24  primary-80cw.4 P1  schema-daemon: implement persisted catalog registry and type-help lookup
2026-06-24  primary-80cw.5 P1  mentci pilot: display schema type specs from the schema-daemon registry
2026-06-24  primary-80cw.6 P1  signal-spirit canary: consume schema-owned help catalog
2026-06-24  primary-80cw.7 P1  production cutover gate: schema help daemon pilot acceptance
2026-06-24  primary-80cw.8 P2  schema help intent/report maintenance for Spirit 6th4
2026-06-24  primary-80cw   P1  Schema help daemon pilot: embedded catalogs plus registry (epic)
2026-06-24  primary-dixg   P2  Create skills/videographer.md (discipline lacks a skill file)
2026-06-24  primary-dt1s   P1  Use failed system-operator refresh as context-maintenance negative example
2026-06-24  primary-e4o9   P2  Author the spirit-repo manual generator + ManualNarration + staleness check
2026-06-24  primary-fdd7   P2  Round-trip and ancestor-All fold tests across record, store, observe, deploy
2026-06-24  primary-fos7   P2  Wire DomainRecords/SpecificRecords daemon dispatch + review guardian-retrieval fold
2026-06-24  primary-kooj   P2  Cut orchestrate roles.list / daemon seed to the dynamic-lane model
2026-06-24  primary-lwc6   P2  schema triad vertical slice: manifest environment to canonical schema and Rust regeneration
2026-06-24  primary-mlck   P1  Storage migration 10 to 11 and version bumps for the All recut
2026-06-24  primary-ptvb.2 P1  W2 Cut intent-log the same way
2026-06-24  primary-ptvb.3 P1  W3 Cut spirit-cli to the capture-side reference
2026-06-24  primary-ptvb.4 P1  W4 Cut session-lanes
2026-06-24  primary-ptvb.6 P1  W6 Shrink AGENTS.md to a thin spine
2026-06-24  primary-ptvb.7 P1  W7 Sharpen every skills.nota description into the selection list
2026-06-24  primary-ptvb   P1  preciousMainContext: precious-main-context standard + skill-ladder dedup (epic)
2026-06-24  primary-sfn5   P1  Ancestor-All scope-set transform + DomainRecords/SpecificRecords shorthand verbs
2026-06-24  primary-w0v4   P2  Teach the guardian that All is a legitimate terminal domain
2026-06-24  primary-w0xf   P1  Recut domain.schema + generator: delete Optional, inject All at every domain-tree node
2026-06-24  primary-xgcr   P1  Record the founding All maxim under top-level All at Maximum importance
2026-06-24  primary-yluj   P1  Rebuild spirit-daemon, update CriomOS-home pin, redeploy with migration
2026-06-25  primary-0bax   P2  Sandboxed work proof in ephemeral jj repo after live Claude round trip
2026-06-25  primary-2wj8.1 P1  Create signal-standard shared library and migrate the three signal- consumers
2026-06-25  primary-2wj8.2 P2  Retire local ComponentKind forks by importing signal-standard
2026-06-25  primary-2wj8.3 P2  Drop signal-orchestrate's mirror decision/outcome types; cross-import signal-criome nouns
2026-06-25  primary-2wj8   P1  signal-standard roster + router m3 contract convergence (epic)
2026-06-25  primary-4ddb.1 P2  Add ComponentTrace query + config-encode binary to the introspect CLI
2026-06-25  primary-4ddb.2 P1  Fix the dead trace plane: align producer/consumer, key, sequence, label, faults
2026-06-25  primary-4ddb.3 P1  Make criome the durable canonical substrate: persist configuration_generation + commit
2026-06-25  primary-4ddb   P1  Make the component trace/observability plane work end-to-end (epic)
2026-06-25  primary-7e7a   P2  Failure-mode shakeout after Claude live proof and lifecycle policy
2026-06-25  primary-8jzu   P2  Cloud: hard max-N droplet cap as enforced cost-safety invariant for DigitalOcean
2026-06-25  primary-9ppu.1 P2  Verify mirror routed-object-notice against the REAL router/spirit loop (700 C2)
2026-06-25  primary-9ppu.2 P2  signal-mirror fetch-by-digest restore: HeadMark + HeadNotHeld + locate-by-digest
2026-06-25  primary-9ppu.3 P2  Production MirrorObjectNotify: router EndpointKind::Mirror + auto-fetch reactor
2026-06-25  primary-9ppu   P1  Mirror: production chain-endpoint — audit, fetch-by-digest, live object-notify (epic)
2026-06-25  primary-c4dz.1 P2  Reconcile per-repo INTENT.md/ARCHITECTURE.md presenting scaffold as live
2026-06-25  primary-c4dz.2 P2  spirit: implement live in-place Store::adopt_head
2026-06-25  primary-c4dz.4 P2  spirit: build corpus-agglomeration Supersede pipeline + three pilot clusters
2026-06-25  primary-c4dz.5 P2  Add interim off-host backup of spirit.sema
2026-06-25  primary-c4dz.6 P2  spirit: decouple every-boot migration from daemon liveness (forward-skew degrade)
2026-06-25  primary-c4dz.7 P2  sema-engine/spirit: delete v1-v6 migration readers + crash-injection tests
2026-06-25  primary-c4dz.8 P2  sema-engine: seal kernel write surface + single SchemaHash construction path
2026-06-25  primary-c4dz   P1  Spirit substrate hardening + intent-doc reconciliation (epic)
2026-06-25  primary-fzwd.1 P1  Build the orchestrate workflow-execution engine to production depth
2026-06-25  primary-fzwd.2 P2  Land guard-substrate downstream daemon behavior in mind and criome
2026-06-25  primary-fzwd.3 P1  Integrate the real workflow engine to main, replacing the fixture stub
2026-06-25  primary-fzwd.5 P2  Migrate the live orchestrate redb store 2->3 and restart the daemon
2026-06-25  primary-fzwd.6 P2  Build a cross-lane recently-landed push feed
2026-06-25  primary-fzwd   P1  Orchestrate workflow-execution engine + worktree registry (epic)
2026-06-25  primary-iy51.10 P2 mentci CLI all-paths completeness: render generic path + retract:/propose: atoms
2026-06-25  primary-iy51.12 P1 criome+mentci two-daemon nixosTest keystone on Prometheus
2026-06-25  primary-iy51.3 P1  mentci daemon: persist SEMA state / reconcile from criome on restart
2026-06-25  primary-iy51.5 P1  mentci correctness/security cluster: rollback, Defer delivery, remote-answer guard
2026-06-25  primary-iy51.6 P2  mentci-lib: make Error surface load-bearing + clear slot on RetractObservation
2026-06-25  primary-iy51.7 P2  mentci post-answer refresh: Observe-on-VerdictAccepted now, daemon-pushed deltas later
2026-06-25  primary-iy51.8 P1  Create signal-mentci-egui + meta-signal-mentci-egui triad; rework mentci-egui
2026-06-25  primary-iy51.9 P2  mentci-egui: per-client view-state + DriveOrigin double-write attribution
2026-06-25  primary-iy51   P1  Realize mentci as a live component: daemon, egui, two-daemon keystone (epic)
2026-06-25  primary-nlx5.1 P2  Activate referents: register recurring instances + model-tag aboutness at write-time
2026-06-25  primary-nlx5.2 P2  Capture guardian prompt-cache telemetry + add a verdict cache
2026-06-25  primary-nlx5.3 P3  Rewrite guardian rejection-reason glosses to lead with the operable test
2026-06-25  primary-nlx5.4 P2  Verbatim quote authentication + idiolect-aware modality learned from the journal
2026-06-25  primary-nlx5   P1  Activate the guardian's dormant signals: referents, cache, glosses, auth (epic)
2026-06-25  primary-o2lr   P2  Emit architecture/flow/dependency mermaid diagrams from the typed schema
2026-06-25  primary-o7j2.1 P2  Finish schema-rust-next emission: scalar/newtype impls, accessors, VariantMatch, errors
2026-06-25  primary-o7j2.2 P2  Decide and create the neutral importable home for reaction.schema
2026-06-25  primary-o7j2.3 P2  schema-next: route Family-body parsing through a typed structural-macro node
2026-06-25  primary-o7j2.4 P2  schema-next: build real RustSurface crate-parse populator + method-call resolver
2026-06-25  primary-o7j2.5 P2  schema-rust-next: emit guardian verdict-type triad as a reusable schema macro
2026-06-25  primary-o7j2.7 P2  Regenerate signal-agent artifacts against current schema-rust-next pin
2026-06-25  primary-o7j2.8 P2  router: live authorized-object fan-out (Attend/Withdraw + durable attendance table)
2026-06-25  primary-o7j2   P1  Finish schema-rust-next codegen back-half and clear wire-contract debt (epic)
2026-06-25  primary-om4g.10 P2 Run consumer-build sweep across ~12 unaudited consumer daemons
2026-06-25  primary-om4g.11 P1 Wire single-host criome-gated typed propagation loop to LoopProvenGreen
2026-06-25  primary-om4g.12 P2 Build criome adjudicator / escalation ladder beyond EscalateToPsyche
2026-06-25  primary-om4g.13 P2 Add verb-scoped quorums, meta-plane amend-contract verb, full replay quad
2026-06-25  primary-om4g.15 P1 Finish direct criome peer lane: serve-loop + nonce-bound tally + two-node test
2026-06-25  primary-om4g.17 P2 Decide and encode where the AuthorizationGrant lives
2026-06-25  primary-om4g.1 P2  Add criome-authorization trace event so auth watch rides tracing surface
2026-06-25  primary-om4g.2 P1  Arm the criome gate in the shipped spirit daemon from authenticated meta-signal config
2026-06-25  primary-om4g.3 P1  Make criome SubmitAuthorizationApproval idempotent: status-guard, honest replies, TTL
2026-06-25  primary-om4g.4 P2  Add double-signature + missing-co-signature watcher to second Prometheus criome
2026-06-25  primary-om4g.5 P2  Implement BLS12-381 aggregate verification (FastAggregateVerify + PoP-on-admission)
2026-06-25  primary-om4g.6 P1  Build cluster-root AdmitRegistration minting ceremony / CLI
2026-06-25  primary-om4g.7 P2  Enforce three-layer auth boundary in criome peer-responder with distinct reasons
2026-06-25  primary-om4g.8 P3  Collapse criome decline reasons to coarse PolicyRefused; document coauthority trust
2026-06-25  primary-om4g.9 P1  Build encrypted multi-key KeyStore replacing the bare MasterKey
2026-06-25  primary-om4g   P1  criome auth core: production gate, quorum plane, key custody, proven loop (epic)
2026-06-25  primary-pl60   P2  Unify actor runtime across daemon fleet + Nix flake-check source-equals-binary witness
2026-06-25  primary-tdtl   P3  Next harness and generalization after Claude proof and shakeout
2026-06-26  primary-57ce   P2  Initial lifecycle policy for persistent harness sessions
2026-06-26  primary-b99l   P2  Promote slice-local harness behavior into final owners
2026-06-26  primary-q4uk   P3  Fix terminal viewer color fidelity for live Claude TUI
2026-06-26  primary-xj1y   P2  Classify Claude-first proof failures by owning layer
2026-06-27  primary-2ne2   P2  Mind technical subscriptions expose overflow/outbox policy
2026-06-27  primary-pm7l.10 P1 Final reconciliation for Mind technical memory review hardening
2026-06-27  primary-pm7l.11 P2 Mind Signal caller identity uses real auth proof
2026-06-27  primary-pm7l   P1  Mind technical dependency memory review hardening (epic)
2026-06-29  primary-1y56   P2  spirit: drop dead meta-signal-criome [patch] so full nix flake check is green  [LANDMINE: flake.nix fix as described is UNSAFE — would break mirror-shipper Nix builds]
2026-06-29  primary-9s3j   P2  Teach speech-to-text tool workspace vocabulary
2026-06-30  primary-6obv   P1  Legacy Spirit-tracks disposition + ESSENCE/INTENT elimination doctrine (epic)
2026-06-30  primary-7wld   P2  DEFERRED T5: Build human-facing Spirit usage manual
2026-07-01  primary-0jxo   P2  nota-strict-positional: Spirit intent record — strict-positional + canonical-codec intent
2026-07-01  primary-2f7j   P2  Track CriomOS-test-cluster architecture-md worktree
2026-07-01  primary-4tx1   P1  nota-strict-positional: signal-spirit migration — 12 variants + tests
2026-07-01  primary-53pz   P2  Track lojix-holistic-test-cluster worktree
2026-07-01  primary-5k8z   P2  nota-strict-positional: nota-design doctrine manifestation
2026-07-01  primary-6kst   P1  nota-strict-positional: wire/storage compat + spirit deployment decision
2026-07-01  primary-6obv.11 P3 Follow-up: goldragon AGENTS.md commit-format doctrine vs practice divergence
2026-07-01  primary-6obv.13 P4 Follow-up: audit F6 traceability note — cited Spirit design-record IDs no longer resolve
2026-07-01  primary-6obv.14 P3 Follow-up: ESSENCE subsection-precision — F1 repoint collapsed anchors
2026-07-01  primary-aae5   P1  nota-strict-positional: signal-mentci migration — 1 variant + consumers
2026-07-01  primary-c8w0   P1  Listener: close usable production trial readiness
2026-07-01  primary-dym1   P3  parked: ListenerTier lowercase Display divergence (#2)
2026-07-01  primary-gm05   P2  Listener: decide orphan and capture-store trust policy (decision)
2026-07-01  primary-lf12   P1  nota-strict-positional: downstream consumer migration — spirit + mentci/mentci-lib
2026-07-01  primary-llep   P2  Listener: validate crash durability on disposable storage
2026-07-01  primary-sjot   P2  nota-strict-positional: Phase-3 independent audit
2026-07-01  primary-ta2q   P2  nota-strict-positional: scope-enum #1 second-inconsistency verification
2026-07-01  primary-ugc8   P3  parked: query/selection newtype style (#3)
2026-07-01  primary-wibo   P1  nota-strict-positional: machinery fix — schema-next guard + schema-rust-next codegen deletion
2026-07-01  primary-z2xg   P2  Recover preserved spirit-guardian-config WIP bookmark
```

## Verification performed
- `bd count --status open` = **153** after the pass (222 − 69).
- Re-export + `jq`: the only open beads created ≤ 2026-06-18 are exactly the 9 bucket-B keeps (primary-4civ, 5zur, 85hv, 9x9f, ebev, hhp0, kr40, ohpk, x3l7) — zero bucket-A stragglers.
- Spot-checked close_reason strings on primary-y3is (bucket A) and primary-tcg0 (bucket B): correct format and content.
- primary-1y56 confirmed OPEN (kept; landmine preserved).
- primary-5u9 confirmed CLOSED after individual re-close.

## Blockers / notes
- No blockers. No Dolt lock retries were needed (all closes succeeded first attempt).
- One integrity note: multi-ID `bd close` silently skipped **primary-5u9** while reporting overall success; caught by count reconciliation and re-closed individually. Recommend preferring per-ID closes (or post-close verification) when batching.
- All closes are reversible tracker state; every close carries a specific reason. No Spirit records touched, no reopens, no code/doc edits.
