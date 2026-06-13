# 102 — SEMA version-control audit: frame and method

*system-designer lane, 2026-06-13. Psyche commission: "Run an audit on the
work that you did on SEMA version control and the pilot project spirit for it
and the server component … make sure you train up … you wouldn't want to spawn
subagents with subpar understanding. There's no intent to log here." Subagent
dispatch explicitly authorized for this audit; no Spirit capture this session.*

## What is being audited

The SEMA version-control arc delivered across reports 98–101 — now **landed
and deployed**, not branches. Integrated `main` heads at audit time:

| Repo | `main` head | Role in the arc |
|---|---|---|
| spirit | `a4cc858` land versioned store pilot | the VC **pilot** (v9 versioned store, logged-fold migration, 0.12.0) |
| sema-engine | `909eaa0` distinguish domain keys from identifiers | the **engine** (versioned fold, checkpoint/import, tamper, family identity) |
| mirror | `69fe4e7` drop crate prefixes from daemon nouns | the **server component** (remote, payload-blind ingest daemon) |
| signal-mirror | `4fa767d` | working signal contract |
| meta-signal-mirror | `6a56fcb` | meta policy signal contract |
| schema-next | `f460e7b` | content identity + family declarations + typed macro library |
| schema-rust-next | `00763d6` | RecordFamily emission (generated identity) |
| nota-next | `3d6c2cd` | structural-shape derive extension |
| triad-runtime | `1b5d0f1` | tailnet TCP listener + PeerIdentity |
| mind | `334d445` | memory-graph family (consumer witness) |

## Corrected live state (verified before dispatch)

A relayed report claimed "the live spirit intent daemon is down (store is v8,
the deployed 0.12.0 upgrade tool expects v7)." The psyche corrected this
directly: `spirit Version → (VersionReported 0.12.0)`. **The daemon is up and
migrated** — v9 store, 0.12.0 binary, migration ran in production. The "down"
relay was stale or already resolved.

The decisive evidence for *why* the migration worked: deployed spirit 0.11.3
(`0a6f93a`) locked `sema-engine` to `branch=main#ebee6e44…` (0.2.3), and
`sema-engine-previous` is pinned to **exactly `ebee6e44`**. The migration reads
the live v8 store with the very engine generation that wrote it. The pin is
correct; the migration is faithful, not tautological.

A second live signal, relayed from the server lane: **the mirror daemon is up**
(working + meta sockets, TCP `0.0.0.0:7474`, `mirror.service` active), but
`ObserveHeads → (HeadsObserved [])` — **nothing ships to it yet.** The
data-loss-with-remote intent (`29pb`) is proven at the daemon level by the
end-to-end witness, but is not live, because the component-side shipper is
unbuilt. Retention enforcement and BLS attestation are deferred.

These two facts — daemon-up-but-migration-is-a-manual-step, and
server-up-but-idle — are the audit's load-bearing live context.

## Method

Adversarial fan-out across six dimensions (workflow `sema-vc-audit`). Each
dimension: a deep-read finder produces severity-ranked findings citing
`file:line` on `main`; each finding is then independently verified by a skeptic
prompted to refute it and to test significance against intent/ESSENCE
(High/Critical findings get a second, perspective-diverse skeptic). A synthesis
agent reconciles confirmed findings against the live state and writes the
numbered chapters plus the synthesis. The audit verb discipline holds
throughout: a claim states what the **production path does**, not what the code
**can do** in a test (`skills/designer.md` §Audit precision). Where the prior
phase-3 reviews already named a finding, the auditor re-verifies it
adversarially rather than trusting it.

Dimensions:

1. **Deployment & version-axis truth** — the manual-migration deploy
   fragility (root of the transient "down"), version-surface honesty
   (component vs store-schema vs wire), self-description (`h2oa`).
2. **Migration correctness** — the v1..v8→v9 logged fold, pin fidelity,
   single-rename crash safety, coverage gaps (v1–v6 type-only, mutation/
   retraction not log-covered, archive unversioned, guardian v2 not folded).
3. **sema-engine versioned fold** — fold/checkpoint/import-session/rebuild,
   tamper witnesses, storage-layout-3 guard, family-identity derivation.
4. **Mirror server** — daemon shape, payload-blind ingest, dedup/gap/fork,
   the two fixed wedges + self-heal, dogfooded ledger, and the live
   no-shipper / no-retention / no-attestation gap.
5. **Schema / identity / generation stack** — content identity, family
   declarations, RecordFamily emission, and whether the three hand-parsing
   sites the psyche named are genuinely structural macros now, plus the
   remaining tree-mirror hand-impl boundary.
6. **Cross-cutting discipline & beauty** — Rust rules, naming (incl. the
   `SpiritStoreV*` / double-`Store` warts and C-CRATE-PREFIX residue),
   positional NOTA, daemon-one-argument, file size, repetition-into-abstraction
   against the ESSENCE ladder (clarity → correctness → introspection → beauty).

The synthesis lands the numbered chapters here and a bead list (operator +
system-operator) — an audit that ends without operator-actionable beads is
incomplete (`skills/designer.md` §Audits feed into bead filing).
