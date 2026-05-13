# 08 — Autonomous session status

Date: 2026-05-12
Role: system-assistant
Tracks: reports 02–07; the loop iterations after `<<autonomous-loop-dynamic>>`
        wake-ups across this session.
Builds on: `reports/system-specialist/118-criomos-state-and-sandbox-audit.md`
        for the cross-role state snapshot.

## What this report is

The user is stepping out and asked me to keep working unattended. This
report consolidates what landed during the autonomous loop iterations
so a returning reviewer can see the cumulative state without paging
through eight push bookmarks.

## What landed this session

Eight commits across four repos. All pushed to auto-named bookmarks;
none have been merged to a `main` line by me — that is the operator /
system-specialist / user's call.

| # | Repo | Bookmark | Description | Test delta |
|---|---|---|---|---|
| 1 | horizon-rs | `push-pkzmxxsolntv` | Audit-07 quick wins: `Cluster.tld` typed field + `tests/projection_purity.rs` | 107 → 109 |
| 2 | primary | `push-mpotsrmlsplt` | `skills/actor-systems.md` ZST-actor anti-pattern section + new `skills/typed-records-over-flags.md`; also bundles reports 06, 07 | n/a |
| 3 | lojix-cli | `push-qmxupxzkpqnz` | `tests/network_neutrality.rs` (literal-name regression scan) | +1 |
| 4 | horizon-rs | `push-knztnowkrtln` | P1 slice 2a: derive `Node.placement` in projection (Metal & Pod migration) | 109 → 111 |
| 5 | horizon-rs | `push-nsypqrwypsyo` | P1 slice 2b: `placement` on `NodeProposal`, `NexusVerb`+`NotaRecord` wire derives, `Metal`/`Contained` rename to match variant names | 111 → 115 |
| 6 | horizon-rs | `push-touxqnoympto` | P1 slice 2c: containment validation rules (`ContainedHostNotFound`, `NestedContainment`) | 115 → 117 |
| 7 | horizon-rs | `push-xzrxuvroxskv` | P1 slice 3a: derive `Node.capabilities.build_host` from `is_remote_nix_builder` | 117 → 119 |
| 8 | primary | (this report) | Session-status report 08 | n/a |

Also earlier in this conversation, before the autonomous loop began:
- `push-ovulwxnnpykv` in lojix-cli (kameo collapse, bead `primary-q3y`)
- `push-oowpqtrszouq` in horizon-rs (P1 slice 1, typed placement /
  capability / secret modules)
- `push-wtqynszxzlul`, `push-kvxxrpnluyrq` in primary (reports 05,
  06, 07)

## Cumulative P1 plan status

The cloud-host-and-contained-node plan from
`reports/system-assistant/04-dedicated-cloud-host-plan-second-revision.md`
is broken into slices in `reports/system-assistant/06-implementation-status-after-slice-1.md`.
Where they stand:

| Slice | State |
|---|---|
| 1 — types exist (`placement.rs`, `capability.rs`, `secret.rs`) | Shipped this conversation |
| 2a — derive `Node.placement` in projection | Shipped this session |
| 2b — `placement` on `NodeProposal` + sum-type wire derives | Shipped this session |
| 2c — containment validation (host exists, no nesting) | Shipped this session |
| 3a — derive `Node.capabilities.build_host` | Shipped this session |
| 3b — derive `Node.capabilities.binary_cache` | Pending: needs `SecretReference` defaults + `BinaryCacheEndpoint` scheme/port defaults to be settled. Speculative without an operator/designer pass. |
| 3c — `container_host`, `public_endpoint` derivations | Pending: same reason. Defer until proposals start authoring them. |
| 4 — `Horizon.contained_nodes` + `ProjectedNodeView` | Pending: per report 04 §P1.4 this is recursive-projection territory; do it when a contained node actually needs its own viewpoint (i.e. when CriomOS container-host module starts being implemented). |
| Pod-direct-author migration | Will follow once `ContainerNetwork` / `ContainerState` typed shapes settle. Today legacy Pods project with `network: None, state: None`. |

The pieces I deliberately did **not** touch this session, despite being
in the audit's recommendations:

- **Wi-Fi PKI / `WifiNetwork`** — designer/139 names the shape; system-specialist's
  audit 118 §3 lists it as the next horizon-rs step. The designer/139 task
  table designates `operator` as the owner, and the user is actively
  reshaping the broader PKI direction (designer/141 BLS substrate just
  landed). Adding `WifiNetwork` unilaterally risks rework.
- **`literal-tld-policy` check in CriomOS** — premature. The
  TLD literal `"criome"` is still in `router/default.nix:95`, `network/wifi-eap.nix:*`,
  `router/wifi-pki.nix:34`. Those will be removed alongside Wi-Fi PKI
  migration (separate concern: SSID, not TLD). System-specialist's
  CriomOS-test-cluster has a `source-constraints` check that does some
  of this from the other end.
- **`metal/default.nix` and `profiles/min/default.nix` splits** — system-specialist
  primary; my report 07 §3.3 named them as debt rather than urgent.
- **Cluster-trust runtime naming** — system-specialist's call (per
  designer/139 task E).
- **CriomOS-home flake input audit** — tedious enumeration without a
  strong frame for "dead consumer."
- **`signal-persona-mind` NOTA round-trip coverage** — operator is on it
  per recent locks.

## What's right that wasn't this morning

A short list of things the session demonstrably moved:

1. **Typed records over flag soup** is now both a skill
   (`skills/typed-records-over-flags.md`) AND has further concrete witnesses:
   `Node.placement: NodePlacement`, `Node.capabilities.build_host`,
   `ContainerHost.bridge_policy`, the `Cluster.tld` newtype. The pattern
   is no longer ambient lore — it's a workspace skill with named
   precedents.
2. **The ZST-actor anti-pattern** is named in `skills/actor-systems.md`
   §"Zero-sized actors are not actors" with the lojix-cli kameo collapse
   as the worked example. Future agents won't reinvent the discovery.
3. **`projection_purity.rs`** (horizon-rs) and `network_neutrality.rs`
   (lojix-cli) lock in two implicit-but-unwritten architectural rules
   as failing-test witnesses. If a future change reaches for env/fs/clock
   in horizon-rs, or names `"prometheus"` / `"goldragon"` / `"criome"`
   in lojix-cli source, the next CI run fails loud.
4. **`Cluster.tld`** is the data-neutrality move that system-specialist
   immediately consumed (commit `bcd1e9f` derived tailnet DNS from
   horizon node domain; CriomOS-test-cluster gained an alternate-domain
   fixture). The literal `"criome"` exiting horizon-rs has unblocked
   CriomOS module migration.
5. **Containment is type-safe**. Authored placement overrides legacy
   derivation; nested containment is rejected at projection time;
   missing hosts are rejected at projection time. `Node.placement`
   is the new gate consumers should read.

## Where the locks are right now

| Lock | State |
|---|---|
| `operator.lock` | empty |
| `designer.lock` / `designer-assistant.lock` | empty |
| `system-specialist.lock` / `system-assistant.lock` | empty |
| `poet*.lock` | empty |

The system is fully idle. The eight pushed bookmarks are waiting for
review.

## What I'd suggest doing first when you're back

In rough priority order:

1. **Read `reports/system-specialist/118-criomos-state-and-sandbox-audit.md`**
   for the system-specialist's cross-cutting state snapshot (it
   covers CriomOS, CriomOS-test-cluster, ClaviFaber, and notes the
   booted-service-test gap).
2. **Decide on the eight pushed bookmarks**. The least-risky path is
   probably to fast-forward `main` in each repo over the bookmarks in
   the order they shipped, since each slice is self-contained and tests
   pass on every commit.
3. **Decide whether to drive Wi-Fi PKI implementation next**. The
   design is detailed (designer/139, designer-assistant/29, the user's
   pushes on 141). The system-specialist's audit names it as the
   biggest remaining architectural violation. Who owns the
   horizon-rs `WifiNetwork` addition (operator vs system-assistant)?
4. **Decide on the cluster-trust runtime naming** — task E from
   designer/139 §6.

The autonomous session can resume on any of those if directed.

## Sources

- Push bookmarks listed above are the canonical artifacts. Each carries
  its own commit message with the rationale; this report is a pointer.
- `reports/system-specialist/118-criomos-state-and-sandbox-audit.md`
  is the parallel state report from the system-specialist side.
- `reports/system-assistant/04` and `06` are the slice plan and prior
  status snapshot.
- `reports/system-assistant/07` is the deep audit that drove most of
  this session's work.
