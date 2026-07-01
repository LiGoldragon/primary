# Scout — Open Bead Triage: Situational Map

## Task and Scope

Read-only survey and triage of EVERY open bead in the primary workspace bead
tracker. No mutations were made: nothing was closed, edited, advanced, or
implemented. This file is the durable, machine-readable inventory; the chat
return carries the decision buckets.

## Interface and sources consulted

- Work tracker: `bd` (beads) CLI at `/home/li/.nix-profile/bin/bd`; DB under
  `/home/li/primary/.beads/`. There is one workspace database (prefix `primary-`).
  `repos/` and `private-repos/` are EMPTY; the actual code repos live under
  `/git/github.com/LiGoldragon/<name>` (authoritative list:
  `/home/li/primary/protocols/repos-manifest.nota`). No per-repo bead databases
  were found — all work items are in the single primary tracker.
- Export used: `bd export --no-memories` -> 991 total issues; 262 open, 720
  closed, 6 in_progress, 2 blocked(stored), 1 deferred. Infra beads
  (agent/rig/role/message), gates, and templates are excluded by default and are
  NOT counted here.
- `bd status` separately reports 53 "Blocked" (dependency-derived) and 209
  "Ready to Work"; those 53 are stored-status `open` but have active blockers.
- Spirit intent grounding: read-only `PublicTextSearch` + `Lookup` queries only.

## Observed-fact vs interpretation boundary

- FACT: bead ids, ages, titles, labels, descriptions (from `bd export`).
- FACT: which target repos exist under `/git` and their manifest lifecycle.
- FACT: which Spirit records resolve / do not resolve (query outputs).
- INTERPRETATION: the `target-repo` column (inferred from title+labels, `?` when
  ambiguous), the `size` estimate, and every disposition. Per-repo git
  merge-state was NOT verified for the bulk engineering beads (see Unknowns).

## Disposition summary

- Total open beads: **262**
- `implement`: **251** (still-wanted, not proven done). Rows tagged
  `implement*` (17) are merge/integration beads whose branch-merge state was not
  git-verified — they may already be landed (see Unknowns).
- `stale-close`: **2**
- `possible-contradiction`: **9** (psyche must personally adjudicate — full list
  in chat return and below).

Default rule applied: an open bead was left `implement` unless there was positive
evidence of staleness (target repo gone / self-declared no-op) or genuine doubt
about alignment with current psyche intent. Per the brief, doubt was NOT resolved
by the scout — it was routed to `possible-contradiction`.

## Implement bucket — grouped (full per-bead rows in the table below)

MULTI-CHILD EPIC CLUSTERS (implement):
- **primary-om4g** (n=18) criome auth core: production gate, quorum plane, key custody, and the   [repos: criome:12, ?:6]
- **primary-iy51** (n=14) Realize mentci as a live component: daemon, driveable egui, and the tw  [repos: mentci:12, mentci-egui:2]
- **primary-80cw** (n=9) Schema help daemon pilot: embedded catalogs plus registry for producti  [repos: mentci:7, schema-next:1, schema-rust-next:1]
- **primary-c4dz** (n=9) Spirit substrate hardening + intent-doc reconciliation  [repos: spirit:6, sema-engine:2, ?:1]
- **primary-o7j2** (n=9) Finish the schema-rust-next codegen back-half and clear the wire-contr  [repos: schema-rust-next:4, schema-next:3, orchestrate:1, signal-router:1]
- **primary-fzwd** (n=7) Orchestrate workflow-execution engine + worktree registry to productio  [repos: orchestrate:4, ?:2, criome:1]
- **primary-36iq** (n=6) Coordinate NOTA bracket-string merge and consumer migration  [repos: nota-next:4, spirit:1, horizon-rs:1]
- **primary-7d8m** (n=6) Intent-layer alignment: schema stack -> SpecifiedSchema era  [repos: nota-next:2, spirit:2, schema-next:1, schema-rust-next:1]
- **primary-ptvb** (n=6) preciousMainContext: precious-main-context standard + skill-ladder ded  [repos: ?:3, spirit:1, skills/primary:1, nota-next:1]
- **primary-nlx5** (n=5) Activate the guardian's dormant signals: referents, cache, glosses, au  [repos: spirit:3, ?:2]
- **primary-2wj8** (n=4) signal-standard roster + router m3 contract convergence  [repos: signal-standard:3, mirror:1]
- **primary-4ddb** (n=4) Make the component trace/observability plane work end-to-end  [repos: ?:3, criome:1]
- **primary-6obv** (n=4) Legacy Spirit-tracks disposition + ESSENCE/INTENT elimination doctrine  [repos: spirit:2, skills/primary:1, ?:1]
- **primary-9ppu** (n=4) Mirror: production chain-endpoint — audit, fetch-by-digest, and live o  [repos: mirror:4]
- **primary-pm7l** (n=3) Mind technical dependency memory review hardening  [repos: mind:3]

SINGLE-BEAD implement items: 143
IMPLEMENT by size: {'normal': 202, 'substantial': 32, 'mechanical': 17}
IMPLEMENT by repo: {'spirit': 51, '?': 33, 'mentci': 22, 'schema-next': 20, 'criome': 20, 'cloud': 12, 'CriomOS': 10, 'nota-next': 10, 'schema-rust-next': 10, 'mirror': 7, 'sema-engine': 6, 'CriomOS-test-cluster': 6, 'orchestrate': 6, 'horizon-rs': 5, 'mind': 4, 'lojix': 4, 'listener': 4, 'signal-standard': 3, 'CriomOS-home': 3, 'skills/primary': 2, 'signal-router': 2, 'whisrs': 2, 'mentci-egui': 2, 'triad-runtime': 1, 'persona-pi': 1, 'skills': 1, 'chronos': 1, 'CriomOS/prometheus': 1, 'orchestrator': 1, 'sema': 1}


## stale-close bucket

- **primary-b7qc** — "lojix-cli: review + merge branch cloud-designer-llm-api-token
  to main". Target repo `lojix-cli` is ABSENT from `/git` and NOT present in
  `protocols/repos-manifest.nota`; `RECENT-REPOSITORIES.md` explicitly names
  lojix-cli as a retired/absent checkout. The merge target no longer exists as
  written. The underlying need (localLlmApiToken in the generated secrets flake)
  likely rehomed to `lojix` or `cloud` — verify before final close.
- **primary-g28b** — "DEFERRED T6: Certainty-vs-importance two-axis model". The
  bead's own description states it is OBSERVATION-ONLY with "NO change recommended
  or scheduled." There is no work to implement; it is a note, not a task.

## possible-contradiction bucket (psyche adjudicates — self-contained)

Each entry names the bead, what it may contradict, and the Spirit record id or
repo fact behind the judgment.

1. **primary-bvsd** — "DEFERRED T2: Telos-trio merge decision — jys2 / sj2c / cam8".
   Proposes deciding whether three near-restatement "aim at the ideal design"
   records should be merged/superseded. MAY CONTRADICT: sj2c and cam8 are LIVE
   current intent (both surfaced as active in grounding; jys2 too). Consolidating
   or superseding live intent is a psyche-only decision and the bead itself gates
   on raw-psyche-testimony. Behind judgment: live records jys2, sj2c, cam8.

2. **primary-smwa** — "DEFERRED T1: Fused-source dispositions — o7zt c5nq hv5f k09z
   qjrf gni3". Proposes re-capture / split / REMOVE across six Spirit records.
   MAY CONTRADICT: hv5f, k09z, qjrf are CONFIRMED-LIVE current intent (returned by
   Spirit query during this scout). Removing or splitting live intent records is a
   psyche-only, testimony-gated action. Behind judgment: live records hv5f, k09z,
   qjrf (o7zt/c5nq/gni3 asserted live by the bead).

3. **primary-e191** — "DEFERRED T8: Two uncaptured intents — psyche-acknowledgment
   gate + ask-when-incomplete". Proposes CAPTURING two new intents into Spirit.
   MAY CONTRADICT: intent-capture principle qjrf ("agents ask the psyche rather
   than generating plausible synthesis and capturing it as psyche-authorized;
   inferring to close the loop produces fake records"). New capture needs psyche's
   verbatim testimony. Behind judgment: record qjrf + the bead's own testimony gate.

4. **primary-zpgw** — "DEFERRED T7: Appeals architecture + whole-cleanup audit".
   Two UNBUILT forward-design surfaces, "scope-first". MAY CONTRADICT: nothing
   specific yet, but the shape/scope is undecided and the bead flags it needs
   psyche scoping before any build. Routed here because "still wanted now?" is
   genuinely open. Behind judgment: bead states both surfaces are unbuilt design
   language with no psyche-scoped spec.

5. **primary-ptvb.9** — "S1 Spirit sweep: retire beads vocabulary -> Mind/memory/
   weave across its record cluster" (targets ypg9, el7z, krez, j028, mi6m, pm1b,
   3w61, wgii). MAY CONTRADICT current reality: `PublicTextSearch [retire beads
   vocabulary Mind memory weave]` returned NO matching Spirit record — the rename
   has no durable intent backing that this scout could find — while the ENTIRE
   live tracker is `bd`/beads and the shipped `work-tracking` skill uses that word.
   The "Psyche-authorized" note is only an in-bead claim (unverifiable; qjrf warns
   against fabricated authorization). Behind judgment: absence of any Spirit record
   for the rename + entrenched live `bd`/beads usage.

6. **primary-ptvb.8** — "W8 Roll out the Mind/memory/weave vocabulary; retire the
   word beads" (docs/AGENTS.md/skills side). Same rename as ptvb.9, applied to
   documentation. Same doubt: no Spirit record backs it; contradicts the live
   `bd`/beads vocabulary. Behind judgment: same as ptvb.9; rides on ptvb.9's
   outcome.

7. **primary-ptvb.10** — "S2 Spirit sweep: retire designer/operator distinction
   across its record cluster" (targets ahop, kxzh, zjop, irmw, jq8w, ty8z). The
   bead is itself UNRESOLVED: "Decide per record whether the distinction is
   genuinely retired or merely dormant-for-routing (still meaningful for
   who-does-what)." MAY CONTRADICT: modifies/supersedes live Spirit intent records
   on a question the bead admits is unsettled. Behind judgment: the six named live
   records + the undecided per-record call the bead defers.

8. **primary-ptvb.11** — "S3 Reconcile ky10 then land the minimize-AGENTS.md
   principle". PREMISE BROKEN: `Lookup ky10` returns "record not found" in live
   Spirit, yet the bead's whole plan is to ChangeRecord/Supersede ky10 first and
   land a minimize-AGENTS.md record on top. MAY CONTRADICT / is blocked by: the
   unblock target no longer resolves; the psyche must clarify whether ky10 was
   already retired (making this partly moot) or the id is wrong. Behind judgment:
   dead Spirit reference ky10.

9. **primary-4wvl** — "Rename CriomOS-home to CriomOS-user". Fresh (created today)
   but labeled `future` and the description says "(or equivalent final name)" — the
   final name is EXPLICITLY UNDECIDED in-bead, and `repos-manifest.nota` still
   lists `CriomOS-home` as Active. Routed here because implementation needs a
   psyche decision on the final name and timing before any rename. Behind judgment:
   repo fact (manifest lifecycle Active, no CriomOS-user checkout) + in-bead
   "name not finalized".

## Unknowns and blockers

- **Per-repo merge-state NOT verified** for the 17 `implement*` merge/integration
  beads (e.g. primary-36iq, -60xf, -9gkn, -cxyf, -6eog, -u4tl, -hpkj, -n98t,
  -qu28, -64s3, -3dqf, -exzf, -omis, -bhox, -z2xg, -fzwd.2, -fzwd.3). Their design
  branches may already be landed; each needs a `git log`/branch check in its target
  repo before it is worked or closed.
- **Absent target repos** sharpen a few dispositions but were not fully chased:
  `lojix-cli` (primary-b7qc, stale), `orchestrator` (primary-mt02 — local checkout
  already gone, retirement may be partly done), `nota-codec` (referenced by
  primary-36iq; likely folded into `nota-next`), `persona-spirit` (primary-u4tl,
  -oq0n — manifest says Active but no local checkout under `/git`). These merge
  beads could be closer to done or moot than `implement` implies.
- **Bulk engineering beads (~230)** were classified `implement` from title/label/
  description + alignment with current design-frontier intent (sj2c, cam8, jys2,
  zn2l, w312, j8g6). Their individual done-state in-repo was NOT inspected. This is
  a breadth-over-depth pass; a per-epic deep verification is the recommended
  follow-up before any is picked up.
- **`target-repo` column is inferred** (title+labels heuristic); 33 rows resolve
  to `?`. Treat it as a routing hint, not ground truth.
- **"Psyche-authorized" stamps** appear in several ptvb Spirit-sweep bead bodies.
  They are agent-written claims in the bead, not independently verifiable Spirit
  evidence; per qjrf they cannot be taken as proof of current intent.

## Full inventory (all 262 open beads)

`implement*` = merge/integration bead, branch-merge state unverified.

| id | age_d | upd_d | pri | type | target-repo | size | disposition | title |
|----|-------|-------|-----|------|-------------|------|-------------|-------|
| primary-0bab | 9 | 9 | P1 | task | CriomOS | normal | implement | Port the Immich agentic media mirror into the CriomOS web-host system |
| primary-0bax | 6 | 4 | P2 | task | ? | normal | implement | Sandboxed work proof in ephemeral jj repo after live Claude round trip |
| primary-0v2 | 51 | 12 | P2 | decision | CriomOS | substantial | implement | clavifaber/CriomOS: document SSH host key as sshd-owned cluster publication input |
| primary-0xn7 | 39 | 39 | P2 | task | sema-engine | normal | implement | arca-daemon: add schema_header redb table + read-on-boot |
| primary-1ha | 50 | 12 | P2 | task | CriomOS-test-cluster | normal | implement | CriomOS-test-cluster: add negative Horizon fixtures only after production diagnostics exis |
| primary-1tdr | 35 | 35 | P2 | task | schema-next | normal | implement | Multi-connection daemon concurrency — process-boundary witness needed |
| primary-1ubd | 35 | 35 | P2 | task | cloud | normal | implement | Add Gemma 4 E4B multimodal GGUF to atlas (largeAI node) inventory |
| primary-1xor | 34 | 34 | P2 | task | schema-next | normal | implement | Shared schema-core floor imported via cross-crate (de-duplicate emitter-hardcoded runtime  |
| primary-1y56 | 2 | 2 | P2 | chore | criome | mechanical | implement | spirit: drop dead meta-signal-criome [patch] so full nix flake check is green |
| primary-2f7j | 0 | 0 | P2 | task | CriomOS-test-cluster | mechanical | implement | Track CriomOS-test-cluster architecture-md worktree |
| primary-2n1r | 35 | 35 | P2 | task | schema-next | normal | implement | Implement schema-diff upgrade trait surface per record 950 |
| primary-2ne2 | 4 | 4 | P2 | task | mind | normal | implement | Mind technical subscriptions expose overflow/outbox policy |
| primary-2wj8 | 6 | 6 | P1 | epic | signal-standard | substantial | implement | signal-standard roster + router m3 contract convergence |
| primary-2wj8.1 | 6 | 6 | P1 | task | signal-standard | normal | implement | Create signal-standard shared library and migrate the three signal- consumers |
| primary-2wj8.2 | 6 | 6 | P2 | task | signal-standard | normal | implement | Retire local ComponentKind forks by importing signal-standard |
| primary-2wj8.3 | 6 | 6 | P2 | task | mirror | normal | implement | Drop signal-orchestrate's mirror decision/outcome types; cross-import signal-criome nouns |
| primary-36iq | 40 | 40 | P1 | epic | nota-next | substantial | implement* | Coordinate NOTA bracket-string merge and consumer migration |
| primary-36iq.3 | 40 | 40 | P1 | task | spirit | normal | implement | Update nota-config and Spirit CLI examples for bracket-string NOTA |
| primary-36iq.6 | 40 | 40 | P2 | task | nota-next | normal | implement | Refresh adjacent NOTA consumers and deploy-stack examples |
| primary-36iq.7 | 40 | 40 | P2 | task | nota-next | normal | implement | Sweep authored NOTA examples away from quotation-mark strings |
| primary-36iq.7.1 | 38 | 38 | P2 | task | nota-next | mechanical | implement | Persona/signal: migrate remaining quote-delimited NOTA examples after rename lock clears |
| primary-36iq.7.2 | 38 | 38 | P2 | task | horizon-rs | normal | implement | Horizon/lojix docs: finish bracket-string example cleanup with active migration |
| primary-3dqf | 35 | 35 | P2 | task | CriomOS | normal | implement* | Land fetchHfModel + nix-prefetch-huggingface from cloud-designer prototype branch |
| primary-3rj9 | 17 | 17 | P2 | task | schema-next | normal | implement | Operator integration fixes: schema-next reconciliation fold-ins + spirit testing-trace reg |
| primary-4civ | 18 | 18 | P2 | task | spirit | normal | implement | Add failure escalation around spirit migrate-store ExecStartPre |
| primary-4ddb | 6 | 6 | P1 | epic | ? | substantial | implement | Make the component trace/observability plane work end-to-end |
| primary-4ddb.1 | 6 | 6 | P2 | task | ? | normal | implement | Add ComponentTrace query + config-encode binary to the introspect CLI |
| primary-4ddb.2 | 6 | 6 | P1 | task | ? | normal | implement | Fix the dead trace plane: align producer/consumer, key, sequence, label, faults |
| primary-4ddb.3 | 6 | 6 | P1 | task | criome | normal | implement | Make criome the durable canonical substrate: persist configuration_generation + commit bef |
| primary-4itq | 15 | 15 | P2 | task | spirit | normal | implement | spirit: add ResolveClarification maintenance operation |
| primary-4wvl | 0 | 0 | P2 | task | CriomOS-home | mechanical | possible-contradiction | Rename CriomOS-home to CriomOS-user |
| primary-53pz | 0 | 0 | P2 | task | lojix | mechanical | implement | Track lojix-holistic-test-cluster worktree |
| primary-54ti | 39 | 39 | P1 | task | sema-engine | normal | implement | horizon-rs: migrate to current nota/signal/sema/spirit foundations (per Spirit record 303) |
| primary-57ce | 5 | 5 | P2 | task | mentci | normal | implement | Initial lifecycle policy for persistent harness sessions |
| primary-58l | 50 | 12 | P2 | task | CriomOS-test-cluster | normal | implement | CriomOS-test-cluster: add booted DNS/tailnet assertions to existing VM/nspawn suite |
| primary-5u9 | 50 | 12 | P2 | task | CriomOS | normal | implement | CriomOS: Ghost publication node after container-host substrate exists |
| primary-5zur | 15 | 15 | P2 | task | criome | normal | implement | spirit: criome-auth pilot — out-of-band caller-attestation over per-operation digest |
| primary-60xf | 27 | 27 | P2 | task | triad-runtime | normal | implement* | Integrate triad-runtime designer-strings-at-edges-2026-06-04 onto main |
| primary-64s3 | 7 | 7 | P2 | feature | spirit | substantial | implement* | Land generated spirit-manual.md in primary; split intent-log into intent-capture |
| primary-6d5n | 35 | 35 | P2 | task | ? | normal | implement | Exercise 1-byte tag-space partition for Input/Output per record 934 |
| primary-6eog | 16 | 16 | P2 | task | schema-next | normal | implement* | Integrate family-identity SchemaHash named-newtype emission + regenerate consumers |
| primary-6obv | 1 | 0 | P1 | epic | spirit | substantial | implement | Legacy Spirit-tracks disposition + ESSENCE/INTENT elimination doctrine |
| primary-6obv.11 | 0 | 0 | P3 | task | skills/primary | normal | implement | Follow-up: goldragon AGENTS.md commit-format doctrine vs practice divergence (psyche call) |
| primary-6obv.13 | 0 | 0 | P4 | task | spirit | normal | implement | Follow-up: audit F6 traceability note — cited Spirit design-record IDs no longer resolve i |
| primary-6obv.14 | 0 | 0 | P3 | task | ? | normal | implement | Follow-up: ESSENCE subsection-precision — F1 repoint collapsed fine-grained ESSENCE subsec |
| primary-7ay8 | 50 | 12 | P3 | task | CriomOS-test-cluster | normal | implement | CriomOS-test-cluster: persist Prometheus runner artifacts outside mktemp sandboxes |
| primary-7d8m | 7 | 7 | P2 | epic | nota-next | substantial | implement | Intent-layer alignment: schema stack -> SpecifiedSchema era |
| primary-7d8m.1 | 7 | 7 | P2 | task | nota-next | normal | implement | Intent-alignment: nota-next -> SpecifiedSchema era |
| primary-7d8m.2 | 7 | 7 | P2 | task | schema-next | normal | implement | Intent-alignment: schema-next -> SpecifiedSchema era |
| primary-7d8m.3 | 7 | 7 | P2 | task | schema-rust-next | normal | implement | Intent-alignment: schema-rust-next -> SpecifiedSchema era |
| primary-7d8m.4 | 7 | 7 | P2 | task | spirit | normal | implement | Intent-alignment: signal-spirit -> SpecifiedSchema era |
| primary-7d8m.5 | 7 | 7 | P2 | task | spirit | normal | implement | Intent-alignment: spirit -> SpecifiedSchema era |
| primary-7e7a | 6 | 5 | P2 | task | ? | normal | implement | Failure-mode shakeout after Claude live proof and lifecycle policy |
| primary-7wld | 1 | 1 | P2 | task | spirit | normal | implement | DEFERRED T5: Build human-facing Spirit usage manual (psyche wants to use Spirit himself) |
| primary-7xr4 | 18 | 18 | P2 | bug | nota-next | normal | implement | signal-version-handover: repair Nota derives against current version-projection |
| primary-80cw | 7 | 7 | P1 | epic | mentci | substantial | implement | Schema help daemon pilot: embedded catalogs plus registry for production cutover |
| primary-80cw.1 | 7 | 7 | P1 | task | schema-next | normal | implement | schema-next: define schema-owned rkyv help catalog over SpecifiedSchema |
| primary-80cw.2 | 7 | 7 | P1 | task | schema-rust-next | normal | implement | schema-rust-next: emit embedded help catalogs and type-attached accessors |
| primary-80cw.3 | 7 | 7 | P1 | task | mentci | normal | implement | schema-daemon: design registry/query contract for schema catalogs |
| primary-80cw.4 | 7 | 7 | P1 | task | mentci | normal | implement | schema-daemon: implement persisted catalog registry and type-help lookup |
| primary-80cw.5 | 7 | 7 | P1 | task | mentci | normal | implement | mentci pilot: display schema type specs from the schema-daemon registry |
| primary-80cw.6 | 7 | 7 | P1 | task | mentci | normal | implement | signal-spirit canary: consume schema-owned help catalog instead of local generic HelpBody |
| primary-80cw.7 | 7 | 7 | P1 | task | mentci | normal | implement | production cutover gate: schema help daemon pilot acceptance |
| primary-80cw.8 | 7 | 7 | P2 | task | mentci | normal | implement | schema help intent/report maintenance for Spirit 6th4 |
| primary-85hv | 18 | 18 | P1 | task | mirror | normal | implement | Build the production mirror shipper driver in spirit |
| primary-8b3 | 51 | 12 | P2 | task | CriomOS | normal | implement | CriomOS: finish Yggdrasil key ownership handoff from network seed to clavifaber projection |
| primary-8dcn | 18 | 18 | P2 | feature | ? | mechanical | implement | Delete into_next_step shim + migrate all 14 components to the reaction frame |
| primary-8jpa | 39 | 39 | P2 | task | persona-pi | normal | implement | [Constraint test] persona-pi Nix module hides /nix/store paths from Pi-visible filesystem  |
| primary-8jzu | 6 | 6 | P2 | task | cloud | normal | implement | Cloud: hard max-N droplet cap as enforced cost-safety invariant for DigitalOcean runs |
| primary-9gkn | 18 | 18 | P2 | feature | schema-next | substantial | implement* | Integrate schema-generics + reaction-frame design branches to main |
| primary-9ppu | 6 | 6 | P1 | epic | mirror | substantial | implement | Mirror: production chain-endpoint — audit, fetch-by-digest, and live object-notify |
| primary-9ppu.1 | 6 | 6 | P2 | task | mirror | normal | implement | Verify mirror routed-object-notice against the REAL router/spirit loop (700 C2) |
| primary-9ppu.2 | 6 | 6 | P2 | task | mirror | normal | implement | signal-mirror fetch-by-digest restore: target HeadMark + HeadNotHeld + locate-by-digest |
| primary-9ppu.3 | 6 | 6 | P2 | task | mirror | normal | implement | Production MirrorObjectNotify: router EndpointKind::Mirror + mirror auto-fetch reactor |
| primary-9s3j | 2 | 2 | P2 | task | ? | normal | implement | Teach speech-to-text tool workspace vocabulary |
| primary-9wi | 50 | 12 | P2 | task | CriomOS | normal | implement | CriomOS: add mkCriomOSNode/container-host now that nix role split is done |
| primary-9x9f | 15 | 13 | P1 | task | signal-router | normal | implement | Networking through the router: signal-router forwarding contract + router daemon transport |
| primary-a1px | 35 | 30 | P1 | task | spirit | normal | implement | spirit-next cycle-2 followup: emit OutputNexus client-side dispatcher |
| primary-a6m0 | 34 | 34 | P2 | task | spirit | normal | implement | Spirit: query intent records by numeric identifier |
| primary-am9d | 28 | 16 | P2 | task | spirit | normal | implement | Spirit: implement named shorthand operation ladder |
| primary-b7qc | 34 | 34 | P2 | task | lojix | normal | stale-close | lojix-cli: review + merge branch cloud-designer-llm-api-token-2026-05-28 to main |
| primary-b99l | 5 | 5 | P2 | task | mentci | normal | implement | Promote slice-local harness behavior into final owners |
| primary-bhox | 0 | 0 | P3 | task | criome | mechanical | implement* | Merge criome essence-repoint doc branch to main |
| primary-bojw | 17 | 17 | P2 | task | schema-next | normal | implement | Self-host the macro-table type: generate the pattern family from core.schema |
| primary-bvsd | 1 | 1 | P2 | task | ? | normal | possible-contradiction | DEFERRED T2: Telos-trio merge decision — jys2 / sj2c / cam8 (+ zn2l relation) |
| primary-c4dz | 6 | 6 | P1 | epic | spirit | substantial | implement | Spirit substrate hardening + intent-doc reconciliation |
| primary-c4dz.1 | 6 | 6 | P2 | task | ? | normal | implement | Reconcile per-repo INTENT.md/ARCHITECTURE.md presenting scaffold as live |
| primary-c4dz.2 | 6 | 6 | P2 | task | spirit | normal | implement | spirit: implement live in-place Store::adopt_head |
| primary-c4dz.3 | 6 | 6 | P2 | task | spirit | normal | implement | spirit: single-source meta types from meta-signal-spirit, drop local schema/meta-signal.sc |
| primary-c4dz.4 | 6 | 6 | P2 | task | spirit | normal | implement | spirit: build the corpus-agglomeration Supersede pipeline + run three pilot clusters |
| primary-c4dz.5 | 6 | 6 | P2 | task | spirit | normal | implement | Add interim off-host backup of spirit.sema |
| primary-c4dz.6 | 6 | 6 | P2 | task | spirit | normal | implement | spirit: decouple every-boot migration from daemon liveness (forward-skew degrade) |
| primary-c4dz.7 | 6 | 6 | P2 | task | sema-engine | mechanical | implement | sema-engine/spirit: delete v1-v6 migration readers + add crash-injection tests for the mig |
| primary-c4dz.8 | 6 | 6 | P2 | task | sema-engine | normal | implement | sema-engine: seal the kernel write surface + single SchemaHash construction path |
| primary-c8w0 | 0 | 0 | P1 | task | listener | normal | implement | Listener: close usable production trial readiness |
| primary-cxyf | 16 | 16 | P2 | task | ? | normal | implement* | Integrate structural-forms epic (positional struct syntax + retired-syntax reject) to main |
| primary-da7 | 51 | 12 | P3 | feature | lojix | substantial | implement | cluster registry mismatch handling: keep lojix read-only until registry/runtime exists |
| primary-dixg | 7 | 7 | P2 | task | skills | normal | implement | Create skills/videographer.md (discipline lacks a skill file) |
| primary-dn1e | 27 | 27 | P2 | feature | spirit | substantial | implement | spirit: add ChangePrivacy operation (in-place privacy change) |
| primary-dt1s | 7 | 7 | P1 | task | ? | normal | implement | Use failed system-operator refresh as context-maintenance negative example |
| primary-dw95 | 12 | 12 | P1 | task | nota-next | normal | implement | Stand up durable VM-host test node on prometheus: add VmHost service + TestVm node to dato |
| primary-e191 | 1 | 1 | P2 | task | ? | normal | possible-contradiction | DEFERRED T8: Two uncaptured intents — psyche-acknowledgment gate + ask-when-incomplete |
| primary-e3c | 52 | 12 | P2 | task | ? | normal | implement | cluster registry: choose the long-lived publication registry component, not clavifaber |
| primary-e4o9 | 7 | 7 | P2 | feature | spirit | substantial | implement | Author the spirit-repo manual generator + ManualNarration + staleness check |
| primary-ebev | 15 | 14 | P2 | task | spirit | normal | implement | workspace: intent-substrate rollout — Spirit as the single intent source |
| primary-es8u | 27 | 26 | P1 | task | listener | normal | implement | Extract daemon listener/startup runner beyond Nexus loop |
| primary-exzf | 11 | 11 | P1 | task | CriomOS-test-cluster | normal | implement* | De-branch criome cluster test → CriomOS-test-cluster main |
| primary-f6cc | 45 | 12 | P2 | task | CriomOS | normal | implement | CriomOS: move large-AI model downloads/materialization out of normal system closure |
| primary-fdd7 | 7 | 7 | P2 | task | spirit | normal | implement | Round-trip and ancestor-All fold tests across record, store, observe, deploy |
| primary-fgk | 53 | 12 | P3 | task | chronos | normal | implement | chronos: replace Sky TODOs and Subscribe stub with Phase 1 solar engine |
| primary-flwg | 28 | 28 | P3 | task | spirit | normal | implement | Spirit: design true stream archive targets |
| primary-fos7 | 7 | 7 | P2 | feature | spirit | substantial | implement | Wire DomainRecords/SpecificRecords daemon dispatch + review guardian-retrieval fold |
| primary-fq9l | 34 | 34 | P2 | task | cloud | normal | implement | prometheus: complete Gemma + sops-auth deploy via BootOnce (never Switch) |
| primary-fzwd | 6 | 6 | P1 | epic | orchestrate | substantial | implement | Orchestrate workflow-execution engine + worktree registry to production depth |
| primary-fzwd.1 | 6 | 6 | P1 | task | orchestrate | normal | implement | Build the orchestrate workflow-execution engine to production depth |
| primary-fzwd.2 | 6 | 6 | P2 | task | criome | normal | implement* | Land guard-substrate downstream daemon behavior in mind and criome |
| primary-fzwd.3 | 6 | 6 | P1 | task | ? | normal | implement* | Integrate the real workflow engine to main, replacing the fixture stub |
| primary-fzwd.4 | 6 | 6 | P2 | task | orchestrate | mechanical | implement | Implement orchestrate worktree lifecycle + GC reader + refresh INTENT.md |
| primary-fzwd.5 | 6 | 6 | P2 | task | orchestrate | normal | implement | Migrate the live orchestrate redb store 2->3 and restart the daemon |
| primary-fzwd.6 | 6 | 6 | P2 | task | ? | normal | implement | Build a cross-lane recently-landed push feed |
| primary-g28b | 1 | 1 | P3 | task | ? | normal | stale-close | DEFERRED T6: Certainty-vs-importance two-axis model — observation-only, no change |
| primary-gdb7 | 35 | 35 | P2 | task | cloud | normal | implement | Mint + wire prometheus llama-server API token via gopass |
| primary-gfc0 | 47 | 12 | P3 | task | CriomOS | normal | implement | CriomOS: split metal/default.nix hardware concerns into focused modules |
| primary-gm05 | 0 | 0 | P2 | decision | listener | substantial | implement | Listener: decide orphan and capture-store trust policy |
| primary-gxmj | 35 | 35 | P2 | task | spirit | normal | implement | spirit-next cycle-2 followup: schema-diff upgrade trait check |
| primary-h1vl | 37 | 37 | P2 | task | nota-next | normal | implement | Programmatic extractor for legacy intent files that preserves psyche timestamps |
| primary-hhp0 | 16 | 16 | P2 | task | schema-next | normal | implement | Universal-positional: migrate schema-next streams/families to positional typed-body struct |
| primary-hpkj | 12 | 12 | P2 | task | cloud | normal | implement* | Land DigitalOcean Phase-1 live on cloud main + harden (Tier 1/2) |
| primary-hpx | 50 | 12 | P2 | task | lojix | normal | implement | lojix: materialize GC-root symlinks and retention policy from durable daemon state |
| primary-ia60 | 34 | 34 | P2 | task | cloud | normal | implement | prometheus: confirm router-wifi-projection + possible wifi password change (system-operato |
| primary-ihee | 44 | 44 | P2 | feature | CriomOS-home | substantial | implement | Horizon rewrite: combine leaner shape with re-engineering |
| primary-ipjx | 45 | 12 | P1 | epic | whisrs | substantial | implement | whisrs: design durable RecordingSession capture after repo-intent repair |
| primary-iy51 | 6 | 6 | P1 | epic | mentci | substantial | implement | Realize mentci as a live component: daemon, driveable egui, and the two-daemon keystone |
| primary-iy51.1 | 6 | 6 | P1 | task | mentci | normal | implement | Build the real mentci daemon over mentci-lib |
| primary-iy51.10 | 6 | 6 | P2 | task | mentci | normal | implement | mentci CLI all-paths completeness: render generic path + retract:/propose: atoms |
| primary-iy51.11 | 6 | 6 | P3 | task | mentci | normal | implement | mentci README.md: remove stale criome:* CLI atoms |
| primary-iy51.12 | 6 | 6 | P1 | task | mentci | normal | implement | criome+mentci two-daemon nixosTest keystone on Prometheus |
| primary-iy51.13 | 5 | 5 | P1 | epic | mentci | substantial | implement | Mentci/criome/Spirit intercept-policy MVP weave |
| primary-iy51.2 | 6 | 6 | P1 | task | mentci | normal | implement | Resolve LiGoldragon/mentci remote-name collision + push the four component repos |
| primary-iy51.3 | 6 | 6 | P1 | task | mentci | normal | implement | mentci daemon: persist SEMA state / reconcile from criome on restart |
| primary-iy51.4 | 6 | 6 | P1 | task | mentci | normal | implement | mentci daemon: surface criome rejection instead of unconditional VerdictAccepted |
| primary-iy51.5 | 6 | 6 | P1 | task | mentci | normal | implement | mentci correctness/security cluster: rollback, Defer delivery, remote-answer guard, subscr |
| primary-iy51.6 | 6 | 6 | P2 | task | mentci | normal | implement | mentci-lib: make the Error surface load-bearing + clear slot on RetractObservation |
| primary-iy51.7 | 6 | 6 | P2 | task | mentci | normal | implement | mentci post-answer refresh: Observe-on-VerdictAccepted now, daemon-pushed deltas later |
| primary-iy51.8 | 6 | 6 | P1 | task | mentci-egui | normal | implement | Create signal-mentci-egui + meta-signal-mentci-egui triad and rework mentci-egui off hand- |
| primary-iy51.9 | 6 | 6 | P2 | task | mentci-egui | normal | implement | mentci-egui: per-client view-state + DriveOrigin double-write attribution |
| primary-izze | 45 | 12 | P1 | task | criome | normal | implement | tui-criome: long-running meta-signal-criome client after encrypted meta session exists |
| primary-jqkq | 35 | 35 | P2 | task | spirit | normal | implement | spirit-next cycle-2 followup: schema-emit observer registration trait |
| primary-k5fz | 26 | 26 | P2 | task | schema-rust-next | normal | implement | schema-next + schema-rust-next: streaming event-frame emission for wire contracts |
| primary-k9kj | 47 | 12 | P3 | task | CriomOS-home | normal | implement | CriomOS-home: add an unused-input/static-grep check for flake/module drift |
| primary-kooj | 7 | 7 | P2 | task | orchestrate | normal | implement | Cut orchestrate roles.list / daemon seed to the dynamic-lane model |
| primary-kr40 | 15 | 13 | P1 | task | criome | normal | implement | criome: real blst Sign/Verify + signed RegisterIdentity + master key lifecycle |
| primary-kwm2 | 27 | 27 | P3 | chore | spirit | mechanical | implement | Convert the four spirit error enums to thiserror |
| primary-l35n | 18 | 18 | P2 | task | schema-next | normal | implement | Enforce imported-head arity in schema-next (Local to Imported head rewrite) |
| primary-llep | 0 | 0 | P2 | task | listener | normal | implement | Listener: validate crash durability on disposable storage |
| primary-lome | 34 | 34 | P2 | task | cloud | normal | implement | prometheus: establish console/out-of-band access before router deploys |
| primary-lrf8 | 35 | 35 | P1 | task | ? | normal | implement | Promote mail handling to explicit queue + fanout observers per record 963+970 |
| primary-lrgj | 35 | 35 | P2 | task | schema-next | normal | implement | Nix integration tests should run automatically — CI or pre-commit hook |
| primary-lwc6 | 7 | 7 | P2 | task | schema-next | normal | implement | schema triad vertical slice: manifest environment to canonical schema and Rust regeneratio |
| primary-mlck | 7 | 7 | P1 | feature | spirit | substantial | implement | Storage migration 10 to 11 and version bumps for the All recut |
| primary-mm0 | 52 | 12 | P2 | task | CriomOS/prometheus | normal | implement | clavifaber: decide whether a Prometheus e2e remains beyond existing rootless sandbox |
| primary-mt02 | 27 | 27 | P2 | task | orchestrator | normal | implement | Retire orchestrator (legacy Criopolis/Gas City cascade dispatcher) |
| primary-myku | 27 | 27 | P2 | feature | schema-rust-next | substantial | implement | Build the RustItem emission token model in schema-rust-next |
| primary-n1ao | 27 | 27 | P2 | task | sema-engine | normal | implement | Migrate chroma config.rs off removed nota-codec lexer, then adopt sema-engine |
| primary-n98t | 11 | 10 | P1 | task | horizon-rs | normal | implement* | Land cloud-node feature branches: doris declaration + TypeIs deletion |
| primary-nlx5 | 6 | 6 | P1 | epic | spirit | substantial | implement | Activate the guardian's dormant signals: referents, cache, glosses, authentication |
| primary-nlx5.1 | 6 | 6 | P2 | task | ? | normal | implement | Activate referents: register recurring instances + model-tag aboutness at write-time |
| primary-nlx5.2 | 6 | 6 | P2 | task | spirit | normal | implement | Capture guardian prompt-cache telemetry + add a verdict cache |
| primary-nlx5.3 | 6 | 6 | P3 | task | spirit | normal | implement | Rewrite guardian rejection-reason glosses to lead with the operable test |
| primary-nlx5.4 | 6 | 6 | P2 | task | ? | normal | implement | Verbatim quote authentication + idiolect-aware modality learned from the journal |
| primary-npd | 53 | 12 | P2 | task | horizon-rs | normal | implement | horizon-rs: shrink serde to the JSON projection boundary, not proposal parsing |
| primary-nres | 27 | 27 | P2 | chore | ? | mechanical | implement | Apply 18 architecture/skill constraint manifestations from the report agglomeration (desig |
| primary-nvs8 | 50 | 12 | P2 | task | CriomOS-test-cluster | normal | implement | CriomOS-test-cluster: add synthetic Wi-Fi PKI fixtures after clavifaber/Ygg handoff is wir |
| primary-o2kc | 27 | 27 | P2 | task | spirit | mechanical | implement | Rename spirit repo internal names (spirit-next -> spirit) + cross-repo refs |
| primary-o2lr | 6 | 6 | P2 | task | schema-next | normal | implement | Emit architecture/flow/dependency mermaid diagrams from the typed schema (visuals-as-data) |
| primary-o7j2 | 6 | 6 | P1 | epic | schema-rust-next | substantial | implement | Finish the schema-rust-next codegen back-half and clear the wire-contract debt |
| primary-o7j2.1 | 6 | 6 | P2 | task | schema-rust-next | normal | implement | Finish schema-rust-next emission: default-on scalar/newtype impls, accessors, VariantMatch |
| primary-o7j2.2 | 6 | 6 | P2 | task | schema-next | normal | implement | Decide and create the neutral importable home for reaction.schema |
| primary-o7j2.3 | 6 | 6 | P2 | task | schema-next | normal | implement | schema-next: route Family-body parsing through a typed structural-macro node (retire chunk |
| primary-o7j2.4 | 6 | 6 | P2 | task | schema-next | normal | implement | schema-next: build the real RustSurface crate-parse populator + impl-reference method-call |
| primary-o7j2.5 | 6 | 6 | P2 | task | schema-rust-next | normal | implement | schema-rust-next: emit the guardian verdict-type triad as a reusable schema macro |
| primary-o7j2.6 | 6 | 6 | P2 | task | orchestrate | normal | implement | Fix orchestrate contract-fidelity bugs + add wire round-trip tests to every contract delta |
| primary-o7j2.7 | 6 | 6 | P2 | task | schema-rust-next | normal | implement | Regenerate signal-agent artifacts against current schema-rust-next pin |
| primary-o7j2.8 | 6 | 6 | P2 | task | signal-router | normal | implement | router: live authorized-object fan-out (Attend/Withdraw + durable attendance table) |
| primary-obm | 54 | 12 | P2 | task | ? | mechanical | implement | lore: audit current doc boundaries and stale agent-path shims |
| primary-ohpk | 27 | 27 | P2 | chore | spirit | mechanical | implement | Add a prominent production marker to persona-spirit |
| primary-oil | 53 | 12 | P3 | task | whisrs | normal | implement | whisrs: refresh old feature-gap list into durable RecordingSession follow-ups |
| primary-om4g | 6 | 6 | P1 | epic | criome | substantial | implement | criome auth core: production gate, quorum plane, key custody, and the proven propagation l |
| primary-om4g.1 | 6 | 6 | P2 | task | criome | normal | implement | Add a criome-authorization trace event so the auth watch rides the tracing surface |
| primary-om4g.10 | 6 | 6 | P2 | task | ? | normal | implement | Run the consumer-build sweep across the ~12 unaudited consumer daemons |
| primary-om4g.11 | 6 | 6 | P1 | task | criome | normal | implement | Wire the single-host criome-gated typed propagation loop to LoopProvenGreen |
| primary-om4g.12 | 6 | 6 | P2 | task | criome | normal | implement | Build the criome adjudicator / escalation ladder beyond EscalateToPsyche |
| primary-om4g.13 | 6 | 6 | P2 | task | ? | normal | implement | Add verb-scoped quorums, a meta-plane amend-contract verb, and the full replay quad |
| primary-om4g.14 | 6 | 6 | P1 | task | criome | normal | implement | Migrate signal-criome / signal-persona / signal-message bodies to positional schema syntax |
| primary-om4g.15 | 6 | 6 | P1 | task | criome | normal | implement | Finish the direct criome peer lane: daemon serve-loop + nonce-bound tally + two-node test |
| primary-om4g.16 | 6 | 6 | P2 | task | criome | normal | implement | Add SO_PEERCRED owner-auth on the criome meta socket / distinct Unix users |
| primary-om4g.17 | 6 | 6 | P2 | task | ? | normal | implement | Decide and encode where the AuthorizationGrant lives |
| primary-om4g.2 | 6 | 6 | P1 | task | criome | normal | implement | Arm the criome gate in the shipped spirit daemon from authenticated meta-signal config |
| primary-om4g.3 | 6 | 6 | P1 | task | criome | normal | implement | Make criome SubmitAuthorizationApproval idempotent: status-guard, honest replies, parked T |
| primary-om4g.4 | 6 | 6 | P2 | task | criome | normal | implement | Add double-signature + missing-co-signature watcher to the second Prometheus criome |
| primary-om4g.5 | 6 | 6 | P2 | task | ? | normal | implement | Implement BLS12-381 aggregate verification (FastAggregateVerify + PoP-on-admission) |
| primary-om4g.6 | 6 | 6 | P1 | task | ? | normal | implement | Build the cluster-root AdmitRegistration minting ceremony / CLI |
| primary-om4g.7 | 6 | 6 | P2 | task | criome | normal | implement | Enforce the three-layer auth boundary in the criome peer-responder with distinct reasons |
| primary-om4g.8 | 6 | 6 | P3 | task | criome | normal | implement | Collapse criome decline reasons to coarse PolicyRefused and document coauthority trust |
| primary-om4g.9 | 6 | 6 | P1 | task | ? | normal | implement | Build the encrypted multi-key KeyStore replacing the bare MasterKey |
| primary-omis | 0 | 0 | P2 | task | cloud | normal | implement* | Merge cloud intent-curator-fold into main |
| primary-ooh1 | 35 | 35 | P2 | task | cloud | normal | implement | Package browser-use with OPENAI_API_BASE wrapped to atlas |
| primary-oq0n | 27 | 27 | P3 | chore | spirit | mechanical | implement | Prune ~54 superseded concept branches across engine repos and the spirit pilot |
| primary-pibt | 39 | 39 | P2 | feature | spirit | substantial | implement | persona-pi: Nix packaging that hides Nix paths from harness internal view (per Spirit reco |
| primary-pjbp | 35 | 35 | P2 | task | spirit | normal | implement | Wire StructureHeader into spirit-next routing per record 933 |
| primary-pl60 | 6 | 6 | P2 | task | ? | normal | implement | Unify the actor runtime across the daemon fleet + add Nix flake-check source-equals-binary |
| primary-pm7l | 4 | 4 | P1 | epic | mind | substantial | implement | Mind technical dependency memory review hardening |
| primary-pm7l.10 | 4 | 4 | P1 | task | mind | normal | implement | Final reconciliation for Mind technical memory review hardening |
| primary-pm7l.11 | 4 | 4 | P2 | task | mind | normal | implement | Mind Signal caller identity uses real auth proof |
| primary-ptvb | 7 | 7 | P1 | epic | ? | substantial | implement | preciousMainContext: precious-main-context standard + skill-ladder dedup |
| primary-ptvb.10 | 7 | 7 | P1 | task | spirit | normal | possible-contradiction | S2 Spirit sweep: retire designer/operator distinction across its record cluster |
| primary-ptvb.11 | 7 | 7 | P1 | task | skills/primary | normal | possible-contradiction | S3 Reconcile ky10 then land the minimize-AGENTS.md principle |
| primary-ptvb.2 | 7 | 7 | P1 | task | ? | normal | implement | W2 Cut intent-log the same way |
| primary-ptvb.3 | 7 | 7 | P1 | task | spirit | normal | implement | W3 Cut spirit-cli to the capture-side reference |
| primary-ptvb.4 | 7 | 7 | P1 | task | ? | normal | implement | W4 Cut session-lanes |
| primary-ptvb.6 | 7 | 7 | P1 | task | skills/primary | normal | implement | W6 Shrink AGENTS.md to a thin spine |
| primary-ptvb.7 | 7 | 7 | P1 | task | nota-next | normal | implement | W7 Sharpen every skills.nota description into the selection list |
| primary-ptvb.8 | 7 | 7 | P1 | task | mind | normal | possible-contradiction | W8 Roll out the Mind/memory/weave vocabulary; retire the word beads |
| primary-ptvb.9 | 7 | 7 | P1 | task | spirit | normal | possible-contradiction | S1 Spirit sweep: retire beads vocabulary -> Mind/memory/weave across its record cluster |
| primary-q4uk | 5 | 5 | P3 | task | ? | normal | implement | Fix terminal viewer color fidelity for live Claude TUI |
| primary-qu28 | 18 | 18 | P1 | task | sema-engine | normal | implement* | Integrate the sema-engine VC-hardening stack (rebuild-from-log @ e5e38e8e, v0.6.0) to main |
| primary-s22j | 19 | 19 | P2 | task | sema | normal | implement | Sema VC follow-ups after integration |
| primary-sfn5 | 7 | 7 | P1 | feature | spirit | substantial | implement | Ancestor-All scope-set transform + DomainRecords/SpecificRecords shorthand verbs |
| primary-si42 | 34 | 34 | P2 | task | schema-next | normal | implement | Types-only schema module shape (Input/Output optional) |
| primary-smwa | 1 | 1 | P2 | task | ? | normal | possible-contradiction | DEFERRED T1: Fused-source dispositions — o7zt c5nq hv5f k09z qjrf gni3 |
| primary-srmq | 39 | 39 | P1 | feature | lojix | substantial | implement | lojix-daemon: authenticated Nix flake resolution via nix-auth crate |
| primary-tcg0 | 27 | 27 | P3 | chore | spirit | mechanical | implement | Fix spirit pilot doc/discipline: INTENT.md:206 parity claim, dead concept.schema, CLI Box- |
| primary-tdtl | 6 | 5 | P3 | task | ? | normal | implement | Next harness and generalization after Claude proof and shakeout |
| primary-tiyo | 27 | 27 | P2 | task | spirit | normal | implement | New-Spirit concept thread: archive, privacy split, typed feedback, lifecycle ladder |
| primary-tpd | 51 | 12 | P2 | task | CriomOS | normal | implement | CriomOS: decide overlay roles for Headscale, Tailscale, and Yggdrasil from current modules |
| primary-u0by | 34 | 34 | P3 | task | horizon-rs | normal | implement | Wire a live three-engine chain for Horizon (gated on runtime-shape decision) |
| primary-u4tl | 27 | 27 | P2 | task | spirit | normal | implement* | Integrate persona-spirit spirit-repetition-cleanups (ALL 3 commits) |
| primary-ukzf | 27 | 27 | P2 | task | ? | normal | implement | Eliminate the shared jj working-copy + shared-main race (per-agent workspaces + single-wri |
| primary-unig | 11 | 9 | P1 | task | CriomOS | normal | implement | CriomOS website-hosting node service (doris's role) |
| primary-uwo0 | 27 | 27 | P2 | feature | spirit | substantial | implement | Spirit: implement removal-candidate archive retrieval and restore |
| primary-v1w7 | 16 | 16 | P2 | task | spirit | normal | implement | Spirit: add named private-capture short-form (RecordPrivate/RecordSealed) |
| primary-vjl5 | 27 | 27 | P1 | task | spirit | normal | implement | Split slow spirit local-stack verification into fast and full checks |
| primary-vllc | 27 | 27 | P1 | bug | schema-next | normal | implement | Fix schema-next dual-lowering bare-header bug + both-paths witness |
| primary-w0v4 | 7 | 7 | P2 | task | spirit | normal | implement | Teach the guardian that All is a legitimate terminal domain |
| primary-w0xf | 7 | 7 | P1 | feature | schema-rust-next | mechanical | implement | Recut domain.schema + generator: delete Optional, inject All at every domain-tree node and |
| primary-wk88 | 16 | 16 | P2 | task | spirit | normal | implement | Spirit: implement CollectRemovalCandidates as combined archive-then-retract guarded op |
| primary-wvey | 27 | 27 | P2 | task | horizon-rs | normal | implement | Redo VmTesting as a TYPED node-service end-to-end (discard the string-keyed hack) |
| primary-x178 | 18 | 18 | P2 | chore | spirit | mechanical | implement | Split engine.rs god-impl and store.rs to honor crate-layout bar |
| primary-x3l7 | 18 | 18 | P1 | task | mirror | normal | implement | Rebind mirror TCP ingress off 0.0.0.0; auth before shipping |
| primary-x8by | 12 | 12 | P1 | task | cloud | normal | implement | Act on cloud-engine-audit 68: spine, wire cutover, Hetzner-lead, ad53 CloudNode |
| primary-xgcr | 7 | 7 | P1 | task | spirit | normal | implement | Record the founding All maxim under top-level All at Maximum importance |
| primary-xj1y | 5 | 5 | P2 | task | mentci | normal | implement | Classify Claude-first proof failures by owning layer |
| primary-xslx | 16 | 16 | P3 | task | spirit | normal | implement | message: direct-delivery fast path (supersedes l3k4 clause 2 + 17ss) — public+local-by-uid |
| primary-y0ec | 27 | 27 | P2 | task | schema-next | normal | implement | Peripheral sema-engine boundary strays: chroma, orchestrator, schema-next, .sema |
| primary-y3is | 35 | 35 | P2 | task | cloud | normal | implement | Deploy atlas node + end-to-end smoke through browser-use |
| primary-ydfh | 16 | 16 | P2 | task | spirit | normal | implement | message: own the existence-fact durably (SEMA existence-log) — realize l3k4 clause 1 |
| primary-yeom | 7 | 7 | P2 | task | schema-rust-next | normal | implement | schema-rust-next: repair generated legacy-helper Nix witness |
| primary-yluj | 7 | 7 | P1 | task | CriomOS-home | normal | implement | Rebuild spirit-daemon, update CriomOS-home pin, redeploy with migration |
| primary-ymww | 12 | 12 | P2 | task | criome | normal | implement | Deploy cross-host router/criome transport: L1 CI host -> L2 Yggdrasil -> L3 ouranos/promet |
| primary-ytdj | 34 | 34 | P2 | task | cloud | normal | implement | prometheus: verify Gemma multimodal (mmproj) works, iterate wiring if needed |
| primary-z2xg | 0 | 0 | P2 | task | spirit | normal | implement* | Recover preserved spirit-guardian-config WIP bookmark |
| primary-zpgw | 1 | 1 | P3 | task | ? | normal | possible-contradiction | DEFERRED T7: Appeals architecture + whole-cleanup audit — both unbuilt, scope-first |
