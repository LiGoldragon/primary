# Refresh payload — Psyche Medium b80e55 (Opus 4.6, 1M context)

Successor is Psyche Medium Opus (the sole Opus model now served).
Predecessor b81560 remembered at depth one. This flow's predecessor
chain: b80e55 ← b81560 ← 1ac573.

---

## What this flow learned

### Flashbook design is a three-stage pipeline

Psyche designs the specification (sections with imagery, flowcharts, text).
Fable audits with corrections. A low-power seat illustrates and renders as
a Claude artifact. This is an operational mind-level skill.

Illustrations are pure inline SVG — organic, artistic, curved paths and
gradients, not box-and-arrow diagrams. Two SVG variants per illustration:
portrait (phone, top-to-bottom) and landscape (desktop, left-to-right).
Container queries, not media queries, inside artifact iframes. CSS Grid,
not flexbox. `dvh` viewport units. Headless Chrome screenshots at 390×844
before publishing.

The exportable skill is at `flows/b80e55/reports/flashbook-skill-exportable.md`
(206 lines, self-contained, portable to any agent system).

### The 12-seat cluster is 4 power levels × 3 aspects

```
         High    Medium   Low      Ultra Low
Psyche   Fable   Opus     Sonnet   Haiku
Mind     Astra   Sol?     Terra    Luna
Field    Astra   Sol      Terra    Luna
```

The system checkup agent verifies this grid: 12 panes, each with a working
harness, proportionally assigned. If nobody in an aspect is active, the
ultra-low wakes, gets a status report, notifies its superior or refreshes
itself, assembles the picture for a higher echelon.

### Ultra-low is Luna everywhere except Psyche

Luna's hallucination rate (92.6% on AA-Omniscience) is too high for psyche
work. Haiku's refusal calibration and doubt disposition make it the right
Psyche ultra-low. Mind and Field ultra-low stay Luna — their work is
mechanical and bounded.

### The living's words are not typed on keyboards anymore

No gate, receipt, title, skill load, permission, or launch step may be
framed as cleared by a human typing into a pane. The machine clears it or
the design changes. `user-only` stays — its purpose is that models and
subagents cannot load these skills, not that a human types a command. The
launcher composes startup skills into one block; injection repairs omissions.

### Triad branches per repository

Every repo gets three branches: field, mind, psyche. One worktree per
aspect. Sub-branches for specific work. Field operates and releases skills
without permission. Mind integrates finished epics. Psyche-reviewed means
the whole idea is shown working and approved — that is a Vision.

### Skill authority prefixes

- `testing-` = machine-generated, field-level
- `operational-` = psyche-reviewed, mind-level
- unprefixed = living-approved

Curriculum must only delete the types of skills it's overwriting (type-scoped
deletion). Testing-prefix skills authored ad-hoc survive regeneration.

### Ethos spec skill

All machine-to-machine language is ethos. Every skill teaches how to make an
ethos spec. A new ethos-spec skill is loaded whenever creating or modifying
messaging. The messaging system is the main spec agents iterate on.

### System census runs in ~5 seconds

Full observability chain: flow ID → HM registry → Herdr agent/pane →
transcript path. 19 data sources, all programmatic. The census script
becomes Field Nexus signal contract queries.

### WiFi roaming research — partially reviewed

Phase 1 (802.11r/k/v on existing SAE) sent to Mind. Phases 2–3 need rework:
Ouranos is on a different subnet, AP trigger is operator-toggled not auto,
phones should be on EAP-TLS. CriomOS already has clavifaber, wifi-pki.nix,
wifi-eap.nix — the infrastructure exists. Report at
`flows/b80e55/reports/wifi-roaming-research.md`, Fable review at
`flows/752e0f/reports/wifi-roaming-review.md`.

### Prometheus builder recovered

Full chain proven: Ouranos → USB share → Prometheus → USB bridge → Zeus.
Firewall was the root cause (nixos-fw dropped DHCP/DNS on USB interface).
Runtime fix persisted via systemd drop-in. Declarative CriomOS source needs
a typed `NodeCapability` in Horizon for USB Internet sharing.

### Refresh threshold

A Claude flow refreshes around 200–300K tokens. 100K bootstrap, 100–200K
useful work, then refresh. Cache snapshots: the startup prompt is cached
once, then multiple sessions fork from it with different ideas.

---

## Artifacts published

- Orchestrate (dd53e0fc) — responsive prototype
- Living to Mind (acc98d12) — five exchanges
- How We Make Flashbooks (913bd1b2)
- Skill Situation (c6c668af)

## Vision records

12 entries at `flows/b80e55/vision/`:
flashbookDesignAndFormat, refreshThresholdAndCacheSnapshot,
nexusComponentDeploymentAndTriadRoles, ghostCollectionAndFlowMaintenance,
ethosInlineTypeDeclaration, visualizationPipelineAndFlowLifecycle,
flashbookResponsiveDesign, curriculumAndTriadSkillGeneration,
fieldNexusSystemQuery, systemCheckupAgentAndAutoWake,
twelveMainsProportionalAssignment, lunaForUltraLowEverywhere,
haikuForPsycheUltraLow, flashbookStylingAndCurriculum,
autonomousClusterOperation, flashbookIllustrationStyle,
noHumanTypingOnKeyboards, userOnlyFlagPurpose,
unifiedWifiRoamingAndCertAuth.

## Reports

refresh-owner-addendum, ethos-flashbook-spec, system-census-capabilities,
haiku-vs-luna-comparison, artifact-styling-research, skill-situation-audit,
codex-quota-analysis, flashbook-skill-exportable,
flashbook-claude-agents-source, wifi-roaming-research, refresh-payload.

## Current roster at end

- Psyche High: 752e0f (Fable, working)
- Psyche Medium: b80e55 (this flow, ending)
- Psyche Low: 0625c3 (Sonnet, pane missing)
- Psyche Ultra Low: psyche-haiku-of-b80e55 (idle, wD:p8)
- Mind: 6288d1 (Sol, working), 47764b (High, done)
- Field: 9ddcbc (medium, working), cf3553 (Astra), c3e42e (Sol)
