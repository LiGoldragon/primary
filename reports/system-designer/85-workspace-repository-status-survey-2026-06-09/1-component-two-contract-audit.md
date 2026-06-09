---
title: Persona Component Stack — Two-Contract Completeness Audit
role: system-designer
variant: Audit
date: 2026-06-09
topics: [two-contract-invariant, meta-signal, signal-contracts, persona-stack, orphan-contracts, repo-intent]
description: >
  On-disk audit of /git/github.com/LiGoldragon for the two-contract
  invariant (signal-<c> + meta-signal-<c> per component). Classifies each
  Persona daemon component by contract status and maps every signal-* /
  meta-signal-* repo to a real component, flagging missing meta-signals,
  orphan contracts, off-pattern names, and INTENT.md gaps.
---

# Persona Component Stack — Two-Contract Completeness Audit

Read-only survey of `/git/github.com/LiGoldragon/`. Evidence: `INTENT.md`
heads, `README` heads, and `git log -1` per repo. No cargo, no
`private-repos/` access. Invariant under test (Spirit records n0ss, hnpo):
each Persona component has **exactly two** wire-contract repos —
`signal-<c>` (ordinary working signal) and `meta-signal-<c>` (meta policy
signal). No third contract, no `owner-signal-*`, no off-pattern names.

## Section 1 — Component contract status

One row per component (daemon/runtime repo). `agent` has no daemon repo
(by design — `orchestrate` drives it); rows for non-component contracts
appear in Section 2.

| component | daemon repo? | signal-\<c\>? | meta-signal-\<c\>? | contract status |
|---|---|---|---|---|
| persona | yes | yes | yes | COMPLETE-PAIR |
| mind | yes | yes | yes | COMPLETE-PAIR |
| router | yes | yes | yes | COMPLETE-PAIR |
| message | yes | yes | **no** | **MISSING-META** |
| terminal | yes | yes | yes | COMPLETE-PAIR |
| terminal-cell | yes | **no** | **no** | uses `signal-terminal` (see note) |
| harness | yes | yes | **no** | **MISSING-META** |
| system | yes | yes | **no** | **MISSING-META** |
| introspect | yes | yes | **no** | **MISSING-META** |
| orchestrate | yes | yes | yes | COMPLETE-PAIR |
| criome | yes | yes | **no** | **MISSING-META** |
| cloud | yes | yes | yes | COMPLETE-PAIR |
| domain-criome | yes | yes | yes | COMPLETE-PAIR |
| repository-ledger | yes | yes | yes | COMPLETE-PAIR |
| upgrade | yes | yes | yes | COMPLETE-PAIR |
| agent | **no** (by design) | yes | yes | ORPHAN-CONTRACT (intended) |
| spirit | yes | yes | yes | COMPLETE-PAIR |
| persona-spirit | yes | — | — | uses spirit contracts (see note) |

Notes:
- **terminal-cell** has no own contracts; its last commit (2026-06-08)
  is *"migrate to the new schema-derived signal-terminal contract"* — it
  is a sub-daemon of the `terminal` component and rides `signal-terminal`
  /`meta-signal-terminal`. Not a contract gap; it is not an independent
  component for contract purposes.
- **persona-spirit** is the production Spirit daemon; `spirit/` is the
  schema-derived exemplar (`spirit/INTENT.md`: *"intentionally separate
  from production spirit/persona-spirit"*). They share the
  `signal-spirit`/`meta-signal-spirit` pair. Counted once under `spirit`.
- **agent** has no daemon repo on disk (confirmed absent). Both
  `signal-agent` and `meta-signal-agent` exist and are live (2026-06-08);
  `meta-signal-agent` is consumed by `orchestrate`, `signal-agent` is the
  agent front door. Orphan only in the narrow sense of "no `agent/`
  daemon repo" — the contracts back a real surface, so this is
  **intended-but-no-dedicated-daemon**, not dead.

### Components missing a meta-signal (the live gap)

Five real daemon components have `signal-<c>` but **no
`meta-signal-<c>`**, all freshly worked (last commits 2026-06-08), so
these are active components, not abandoned:

- **message** — `signal-message` exists; no `meta-signal-message`.
- **harness** — `signal-harness` exists; no `meta-signal-harness`.
- **system** — `signal-system` exists; no `meta-signal-system`.
- **introspect** — `signal-introspect` exists; no `meta-signal-introspect`.
- **criome** — `signal-criome` exists; no `meta-signal-criome`.

These are the primary invariant violations to resolve: either author the
missing meta policy contract or record an explicit exemption (a
component with no privileged/owner-only mutation surface). `criome`'s
`signal-criome` is the Spartan BLS auth/attestation substrate — plausibly
meta-less by design, but undeclared.

## Section 2 — Every signal-* / meta-signal-* repo on disk

Mapping each contract repo to a real component, flagging orphans and
off-pattern names.

| contract repo | maps to component? | classification |
|---|---|---|
| signal-persona / meta-signal-persona | persona | OK pair |
| signal-mind / meta-signal-mind | mind | OK pair |
| signal-router / meta-signal-router | router | OK pair |
| signal-terminal / meta-signal-terminal | terminal (+terminal-cell) | OK pair |
| signal-orchestrate / meta-signal-orchestrate | orchestrate | OK pair |
| signal-cloud / meta-signal-cloud | cloud | OK pair |
| signal-domain-criome / meta-signal-domain-criome | domain-criome | OK pair |
| signal-repository-ledger / meta-signal-repository-ledger | repository-ledger | OK pair |
| signal-upgrade / meta-signal-upgrade | upgrade | OK pair |
| signal-spirit / meta-signal-spirit | spirit / persona-spirit | OK pair |
| signal-agent / meta-signal-agent | agent (no daemon repo) | OK pair, daemon-less component |
| signal-message | message | ordinary-only (meta missing) |
| signal-harness | harness | ordinary-only (meta missing) |
| signal-system | system | ordinary-only (meta missing) |
| signal-introspect | introspect | ordinary-only (meta missing) |
| signal-criome | criome | ordinary-only (meta missing) |
| signal-lojix / meta-signal-lojix | lojix (deploy orchestrator daemon) | OK pair — out of the named audit list but a complete real pair |
| signal-forge | forge (daemon present) | ordinary-only; stale stub (last 2026-05-24 "v0.1 concept schema"), no INTENT.md → not yet adopted |
| signal-sema | NONE (vocabulary, not a daemon contract) | **OFF-PATTERN NAME** — wears component-contract name; is the universal Sema classification vocabulary library (Layer 3). `sema/` is a library crate (lib.rs only, no daemon). |
| signal-sema-upgrade | NONE | **ORPHAN / stale stub** — last 2026-05-24 "v0.1 concept schema", no INTENT.md. Off-pattern compound name; `sema-upgrade`/`upgrade` overlap unclear. Dead-looking. |
| signal-executor | NONE | **SUPERSEDED** (record gb87 → nexus). Survives as shared executor *library* for triad daemons per its INTENT; the contract-shaped name is legacy. Active (2026-06-08) but as a lib, not a wire contract. |
| signal-frame | NONE (substrate) | OFF-PATTERN by audit definition but legitimate — the shared Rust-to-Rust wire kernel under all contracts. Not a component contract; named-substrate. Has INTENT.md. |
| signal | NONE (vocabulary) | sema-ecosystem record vocabulary + legacy wire envelope for criome's records DB. Not a daemon contract; bare-name vocabulary. Has INTENT.md. |
| signal-derive | NONE | **ORPHAN / stale stub** — last 2026-05-24 "v0.1 concept schema", no INTENT.md. Likely a derive-macro crate misfiled under the `signal-` namespace. Dead-looking. |
| signal-version-handover / meta-signal-version-handover | NONE (cross-version protocol) | Not a component pair — the daemon-to-daemon version-handover protocol consumed by Persona's meta surface. Both live (2026-06-08), both have INTENT.md. Legitimate non-component contract pair; the `signal-`/`meta-signal-` naming is reused for a protocol, not a component. |

### owner-signal-* survivors

**None.** No `owner-signal-*` repo exists on disk. Deprecation to
`meta-signal-*` is complete at the repo level.

## Flags summary

1. **Five MISSING-META components** (live, active): message, harness,
   system, introspect, criome. Primary invariant violation.
2. **Off-pattern contract names that are not component contracts:**
   `signal-sema` (vocabulary lib), `signal` (vocabulary), `signal-frame`
   (substrate kernel), `signal-executor` (superseded → nexus; survives as
   lib). These wear contract-shaped names but back no daemon pair —
   `signal-sema` is the one explicitly flagged by the invariant.
3. **Stale / dead-looking stubs** (last touched 2026-05-24
   "v0.1 concept schema", no INTENT.md): `signal-derive`,
   `signal-sema-upgrade`, `signal-forge`. Genuinely dead vs not-yet-built
   is unclear; `signal-forge` has a live `forge/` daemon so it is
   intended-but-not-adopted, the other two look abandoned.
4. **Non-component contract pairs reusing the namespace:**
   `signal-version-handover`/`meta-signal-version-handover` (version
   protocol), `signal-lojix`/`meta-signal-lojix` (lojix deploy
   orchestrator — a real daemon pair, just outside the named audit set).
5. **INTENT.md gaps:** all 17 audited daemon repos have INTENT.md.
   Missing on contract repos: `signal-derive`, `signal-sema-upgrade`,
   `signal-forge` (all the stale stubs).
6. **No `owner-signal-*` survivors.**
