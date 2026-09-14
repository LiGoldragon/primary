# Work left off main across the estate

Survey of every repo under `/git/github.com/LiGoldragon/` (188 repos, all jj) and
every worktree under `/home/li/wt/` (94 directories, mostly jj workspaces). For
each: non-main bookmarks and dirty working copies. ~450 non-main bookmarks exist;
most are single-repo, some cluster into fleet-wide sweeps repeated across dozens
of repos. Below: substantive unmerged work, then stale/mechanical clusters, then
dirty working copies.

## (a) Unmerged branches with substantive work

- **message** / `messenger-fixture-34d94e` (also **meta-signal-message**, **signal-message**), 1 commit each, 2026-09-13
  A fixture workspace proving a v4 ledger migration preserves catalog identity, repinning signal-message, and adding a typed prompt-envelope contract. Built to test an Orchestrate Lock call, which failed (`Unreachable`/`failed to fill whole buffer`) — no lock granted, no implementation edits made.
  Flow log: flows/34d94e/log.md (the flow that made it), flows/6cc91b/log.md (this survey).
  Psyche: idea not reviewed by the living — flow 34d94e's own record says root was informed and instructed no editing/bypass; this is a live diagnostic artifact, not a proposal awaiting review.

- **ethos-zero-e3-nexus-runtime / ethos-zero-e3-wire-root-envelope / signal-ethos-zero-e3-contract / meta-signal-ethos-zero-e3-contract / orchestrate-e4-wire-integration / signal-orchestrate-e4-wire-contract / meta-signal-orchestrate-e4-wire-contract** (7 worktrees under /home/li/wt), dates 2026-07 through 2026-08
  A cross-repo Nexus/WireContract migration in progress: WIP commits extend the Orchestrate Nexus lifecycle contract and map imported structural wire faults into generated contract faults, layered on datom path-lock work. Working copies are clean (no uncommitted edits), but the branch tips sit ahead of main.
  Flow log: flows/01a04a30, flows/6329f1, flows/4d5fc7da/log.md.
  Psyche: idea not reviewed by the living — no Vision/flows-vision hit on "WireContract" or "Nexus lifecycle" specifically.

- **CriomOS-wispr-runtime / CriomOS-wispr-system-consumer / CriomOS-wispr-integration / CriomOS-verification-4a8046 / CriomOS-home-wispr-overlay / CriomOS-home-wispr-integration** (6 worktrees) plus repo-level `wispr-*` bookmarks in **CriomOS-home** (listener080recovery, wispr-noctalia-startup-*, wispr-provider-fetch-81c0dc, wispr-recovery-4e296a, wispr-status-*), dates 2026-07 through 2026-08
  Wispr Flow (dictation) integration across the home/CriomOS fleet: private package additions, Home Wispr status consumer wiring, Noctalia plugin preload/reconciliation, provider-owned installer fetch, meter freshness reset after reconnect. Working copies clean; commits ahead of main.
  Flow log: not found by exact branch name; repo-level flows for CriomOS-home commonly touch Wispr (grep on "Wispr" returns dozens of flow logs, too broad to attribute one-to-one).
  Psyche: idea not reviewed by the living.

- **lojix** — 20 non-main bookmarks, dominated by `lojix-canonical-*-milestone-{2..9}` (schema, external-adapters, routed-contact, runner-daemon, persistence-recovery, integration-tests, schema-one reconstruction), plus `finish-lojix-rewrite`, `lojix-bounded-lifecycle-release-milestone-9`, `lojix-lifecycle-completion`, `deployment-compatibility-preflight` (divergent vs @origin), `bounded-lifecycle-remediation`. Dates cluster mid-2026.
  A large staged rewrite of Lojix onto a "canonical six-slot schema" — migrating persistence, routing, runner/daemon fields, and integration tests through eight numbered milestones, with a release/lifecycle-completion branch on top. This reads as the bulk of an in-progress Lojix rewrite that never landed on main.
  Flow log: not found under these exact branch names in flows/*/log.md.
  Psyche: Vision/datom.md line 240 — "Everything moves to Datom: all of the stack, Horizon, Lojix, everything" — states the direction but does not address this specific milestone branch set. Treat as: idea not reviewed by the living at this level of detail.

- **core-ethos** — 13 non-main bookmarks: `SpiritV14Implementation`, `SpiritLineageBTrain`, `SpiritSourceIntegration`, `ProtosSourceFormsProposal`, `AliasAdmissionProposal`, `NoAliasesProducers`, `identifier-slicing-contracts`, `hqu30-resolution` (+`-v30`), `FirstTrancheProducerTrain`, `SlicingCoreSchema`, `acceptance-builtin-priors`. Dates mid-2026.
  Design-stage schema work: sliced/streaming relation and contract foundations, manifest-backed textual schema views, accepted "source surface" installs, and resolving catalog-registered builtin vocabulary in the bootstrap reader (explicitly tied to bead primary-hqu.30). `SpiritLineageBTrain` fans out into 11 other repos (ethos-engine, protos, rust-logos, sema-storage, signal-ethos/logos/nomos/spirit, meta-signal-spirit) each repinning the same encoded-schema-pipeline wave.
  Flow log: not found under these exact names.
  Psyche: idea not reviewed by the living.

- **criome** — 15 non-main bookmarks: `criome-auto-approve` (auto-approve verdict mode + meta Configure impl, cites report 704/Spirit t00s·da5i), `criome-client-approval-witness` (report 705), `cluster-root-admission-ceremony` (offline mint for ClusterRoot::admits), `attested-moment-majority-guard-139` (fork-safe strict-majority time-attestation guard), `criome-nixos-module-142`, `criome-peer-transport` (E1 increment 3 hardening), `criome-spirit-log-object-auth`, `CriomeElevenCompatibility(Final)`, `CriomeElevenFamilyComplete`, `CriomeRuntimeCompatibility`, `language-content-addressed-bls`. Dates June–August 2026.
  A cluster of authorization/attestation features: auto-approve policy, client-approval witnesses, cluster-root admission ceremonies, majority-guarded time attestation, and a NixOS deploy module — each cites a numbered report, suggesting these were written up but not landed.
  Flow log: not found under these exact bookmark names.
  Psyche: idea not reviewed by the living.

- **CriomOS / CriomOS-home** — beyond the Wispr cluster above, ~35 more non-main bookmarks each: hardware/host features such as `bluetooth-microphone-reliability`, `home-kernel-supervisor`, `enable-vm-hosting-prometheus`, `disk-retention-2e28d8`, `bounded-state-production-{os,home}`, `solar-location-*` (solar clock/tooltip, IP-location disable), `spirit-judge-source-ready-{deploy,home}-20260710`, `AdaptiveWindowWrapping`, `repair-pi-package-and-activate`, `pi-child-intercom-injection-{os,home}`. Dates March–August 2026, several tagged "recovery" or "preserve" (safe-saved dirty worktrees from 2026-07-16).
  Grouped rather than itemized individually given volume; these read as one-off host/deploy fixes queued but never merged, several explicitly named as GPT-authored ("GPT-5.4", "GPT-5.6") recovery or hardening passes.
  Flow log: not systematically checked per-branch given count; spot checks on `bluetooth-microphone-reliability` and `home-kernel-supervisor` found no hits.
  Psyche: idea not reviewed by the living.

- **datom** / **datom-codec** / (also touches meta-signal-orchestrate) `epic-datom-path-locks-20260822`, 1+ commits, 2026-08-23
  Adds Datom path-lock replies — infrastructure for the path-locking scheme referenced by the Orchestrate Lock protocol used (and failing) in the messenger-fixture-34d94e item above.
  Flow log: flows/01a02a34/log.md, flows/01a04a30/log.md.
  Psyche: idea not reviewed by the living directly, though it underlies the Orchestrate Lock mechanism the living has used (see messenger-fixture-34d94e).

## (b) Stale or abandoned

Mechanical fleet-wide sweeps where the same commit landed as an unmerged bookmark
across many repos, generally because main already carries an equivalent commit or
the sweep was superseded — collapsed to one line each:

- `realizer-three-stack-status` — 23 repos, all "docs: mark Protos estate status"; main already has this commit in each repo's history, so these are stale duplicate pointers, not unlanded work.
- `SpiritLineageBTrain` — 11 repos (see item above under core-ethos; several are `(empty) no description set` stubs with no real diff).
- `recovery/old-worktree-20260813/*` — 21 bookmarks across CriomOS, meta-signal-criome, meta-signal-mentci, meta-signal-mind, meta-signal-orchestrate; auto-generated worktree-recovery snapshots from 2026-08-13, mostly `(no description set)`.
- `f6db8d-cargo-update` — 4 repos (aggregator, harness, listener, repository-ledger), each tagged "FAILED"; lockfile-only bumps that did not complete, left by flow f6db8d's dependency sweep (flows/f6db8d/log.md wave 1).
- `f6db8d-found-dirt` — 4 repos (chroma, introspect, meta-signal-introspect, terminal); flow f6db8d's "found dirt at wind-down" preservation branches for stale pre-rename working trees.
- `f6db8d-datom-migration` — 3 repos (criome, mentci, message-family); repin branches from the same flow's Datom port, superseded once the port landed on main.
- `CoherentLegacyPins` / `RegistryRemovalIntegration` — 5 and 4 repos respectively, all `(empty) no description set` stubs.
- `mirror/deprecation-857335` and `spirit/deprecation-857335` worktrees — WIP ports (mirror: "port mirror runtime to current signal contracts"; spirit: isolated migration acceptance harness) on components flow f6db8d explicitly marked deprecated on main, after noting mirror WIP does not compile and spirit/mirror were left for the living deliberately. This is reviewed: flow f6db8d's log records the deprecation decision and names spirit/lojix/kameo/chroma-redb/nixpkgs-fork as "never unattended, left for the living."
- Numerous `(empty) (no description set)` single-commit stubs with no diff (dozens more, one or two per repo) — not itemized; these carry no content to review.

## (c) Dirty working copies (uncommitted changes, no branch)

- **CriomOS-home** — `flake.lock`, `packages/rust-toolchain/default.nix` modified on top of the divergent `f6db8d-rust-relock` bookmark (rust-overlay/interactive-Rust relock, itself divergent from @origin).
- **Curriculum** — `result` symlink deleted (build artifact cleanup, trivial).
- **mind** — `ARCHITECTURE.md`, `Cargo.toml`, `flake.nix`, `scripts/live-knowledge-judge-eval.py` modified; no bookmark, no commit made.
- **mind-judge** — `Cargo.toml`, `src/lib.rs`, `src/main.rs` modified, uncommitted.
- **pi-subagents** — `AGENTS.md` modified on top of "Harden subagent terminal result classification."
- **protos-engine** — new file `ideas/guardedObjects-2026-08-07.md` added but uncommitted — an idea note, not yet reviewed.
- **signal-mind-judge**, **signal-orchestrate**, **signal-orchestrator-judge** — each has `ARCHITECTURE.md`, `Cargo.lock`/`Cargo.toml`, `README.md` modified uncommitted; likely a batched contract-regen sweep left mid-way.
- **signal-sema** — `ARCHITECTURE.md`, `Cargo.lock`, `Cargo.toml` modified plus `examples/canonical.nota` renamed to `canonical.dotos`, uncommitted.
- **spirit** — `flake.lock`, two scripts, `src/bin/spirit-migrate-store.rs` modified uncommitted (on the deprecated component).
- **spirit-ethos** — `Cargo.lock`, `Cargo.toml` modified, two new files (`meta-allocation-manifest.nota`, `meta-batch-config.json`) added uncommitted.
- **wispr-flow-linux** — `.beads/issues.jsonl` modified on top of "Track Wispr Status-window re-show repair," on the tracked bookmark `wispr-flow-linux-bjn`.

None of the dirty working copies above are mentioned as reviewed in Vision/, vision-raw/, or any flows/*/vision record found by keyword search; treat all as **idea not reviewed by the living** except where noted (protos-engine's ideas file is explicitly an unreviewed idea note by its own filename).
