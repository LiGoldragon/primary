# Intent Review #10 — Wider-Stack INTENT.md Presence Sweep

Part of the psyche-requested deep audit of the schema-derived stack
(`reports/designer/516-system-deep-audit/`). This review does not
deep-dive any single repo; it catalogues **breadth** — for every active
repository beyond the core schema stack, does an `INTENT.md` file exist,
and in one line, what is that repo for.

The psyche cares MOST about which repos are **MISSING** an `INTENT.md`,
because the per-repo `INTENT.md` is the canonical manifestation surface
for psyche intent into a repo (AGENTS.md §"Required reading", spirit
record 944). A missing `INTENT.md` means psyche intent for that repo
lives only in scattered reports and Spirit records, never synthesised
into the repo's own context surface.

## Method and honesty boundary

The active repo set comes from `/home/li/primary/protocols/active-repositories.md`
(read in full). Presence was checked with a real filesystem test per
repo, not guessed. The exact form run in `/git/github.com/LiGoldragon`:

```sh
for r in <repo...>; do
  if [ -f "$r/INTENT.md" ]; then echo "HAS    $r"; else echo "MISSING $r"; fi
done
```

Every HAS/MISSING line below is copied from the verbatim output of that
command. I separately confirmed (with `[ -d "$r" ]`) that every repo
flagged MISSING is an **actually-checked-out directory** — so "MISSING"
means "repo present, no INTENT.md", never "repo not checked out". I also
confirmed `[ -f signal-frame/INTENT.md ]` returns not-found while the
`signal-frame` directory itself exists with `ARCHITECTURE.md`,
`README.md`, and `skills.md` but no `INTENT.md`.

**One correction to naive reading:** the checkout at
`/git/github.com/LiGoldragon/primary` has **no** `INTENT.md`, but that is
a stale/secondary checkout. The live workspace `INTENT.md` is at
`/home/li/primary/INTENT.md` and exists (44488 bytes, verified). So the
primary *workspace* IS covered; the `/git/.../primary` checkout is not
the canonical one. `primary` is therefore NOT counted as a gap.

**`lore`** likewise has no `INTENT.md` — verified `ls` returns
no-such-file — but it carries `AGENTS.md`, `ARCHITECTURE.md`, `CLAUDE.md`,
`README.md`. Its role is cross-workspace agent discipline, not a
component, so whether it warrants an `INTENT.md` is a judgement call
flagged below rather than an obvious gap.

## Verbatim presence output

Three batched runs in `/git/github.com/LiGoldragon`. Pasted exactly.

Batch 1 (core stack, persona through upgrade family):

```
MISSING primary
MISSING lore
HAS    persona
MISSING mind
MISSING router
MISSING message
MISSING introspect
MISSING signal-introspect
MISSING system
MISSING harness
MISSING terminal
MISSING terminal-cell
MISSING sema
MISSING signal-sema
HAS    sema-engine
HAS    schema
HAS    schema-next
HAS    schema-rust-next
HAS    triad-runtime
HAS    persona-spirit
HAS    spirit
MISSING version-projection
MISSING signal-version-handover
MISSING owner-signal-version-handover
MISSING upgrade
MISSING signal-upgrade
MISSING meta-signal-upgrade
```

Batch 2 (signal-core through nota-config):

```
MISSING signal-core
MISSING signal
MISSING owner-signal-persona
MISSING signal-engine-management
MISSING signal-persona
MISSING signal-persona-origin
MISSING signal-agent
MISSING owner-signal-agent
MISSING signal-message
MISSING signal-router
MISSING owner-signal-router
MISSING signal-system
MISSING signal-harness
MISSING signal-terminal
MISSING owner-signal-terminal
MISSING signal-mind
MISSING owner-signal-mind
HAS    orchestrate
MISSING signal-orchestrate
MISSING owner-signal-orchestrate
MISSING signal-criome
MISSING repository-ledger
MISSING signal-repository-ledger
MISSING owner-signal-repository-ledger
MISSING nexus
MISSING nexus-cli
HAS    nota
HAS    nota-next
HAS    nota-codec
MISSING nota-derive
MISSING nota-config
```

Batch 3 (adjacent + replacement + signal-frame):

```
MISSING criome
HAS    cloud
MISSING signal-cloud
MISSING meta-signal-cloud
HAS    domain-criome
MISSING signal-domain-criome
MISSING meta-signal-domain-criome
MISSING chroma
MISSING CriomOS
MISSING CriomOS-home
MISSING mentci-lib
MISSING horizon-rs
MISSING lojix-cli
MISSING goldragon
MISSING chronos
MISSING TheBookOfSol
MISSING signal-lojix
MISSING lojix
MISSING criomos-horizon-config
MISSING signal-frame
```

## Presence table with one-line purpose

Purpose lines are drawn from `active-repositories.md` and (for the HAS
repos) the verbatim first lines of each `INTENT.md`, which I read.

### Core Persona / Sema / Signal / Nexus / NOTA stack

| Repo | INTENT.md | One-line purpose |
|---|---|---|
| `persona` | HAS | Persona meta-repo; wires the stack through Nix and apex architecture. |
| `mind` | MISSING | Central Persona state component; replaces lock-file orchestration over time. |
| `router` | MISSING | Message routing/delivery; binds internal `router.sock`. |
| `message` | MISSING | Engine message ingress: `message` CLI + supervised `message-daemon`. |
| `introspect` | MISSING | Supervised inspection-plane component; fans in typed observations, projects NOTA at the edge. |
| `signal-introspect` | MISSING | Central introspection envelope contract: query/reply selectors, correlation, projection wrappers. |
| `system` | MISSING | Deferred system observation component (OS/window facts such as focus). |
| `harness` | MISSING | Harness process/session control boundary. |
| `terminal` | MISSING | Persona-facing terminal owner: named sessions, Signal adapter, viewer-adapter policy. |
| `terminal-cell` | MISSING | Low-level daemon-owned PTY/transcript cell primitive consumed by `terminal`. |
| `sema` | MISSING | Today's typed storage kernel (redb + rkyv + schema guard). |
| `signal-sema` | MISSING | Sema operation vocabulary: Assert/Mutate/Retract/Match/Subscribe/Validate. |
| `sema-engine` | HAS | Full database engine over sema/signal-sema; the exclusive DB-operation boundary for state-bearing components. |
| `schema` | HAS | Typed schema-language substrate: resolved schema document model, validation, layout metadata. |
| `schema-next` | HAS | Replacement schema engine; runs position-aware macros, emits ordered macro-free `Asschema`. |
| `schema-rust-next` | HAS | Replacement Rust emission layer; consumes `Asschema`, emits Rust source text. |
| `triad-runtime` | HAS | Shared runtime mechanics for schema-derived Signal/Nexus/SEMA daemons. |
| `persona-spirit` | HAS | Production Spirit source until schema-derived cutover; deployed `spirit` CLI + daemon. |
| `spirit` | HAS | Public runnable pilot proving a Spirit-like component built from schema-derived interfaces. |
| `version-projection` | MISSING | Shared projection/compatibility-policy library for adjacent component versions. |
| `signal-version-handover` | MISSING | Private daemon-to-daemon version-handover signal contract. |
| `owner-signal-version-handover` | MISSING | Owner-only version-handover authority contract (force flip, rollback, quarantine). |
| `upgrade` | MISSING | Upgrade triad runtime scaffold; home for migration orchestration + `upgrade` CLI/daemon. |
| `signal-upgrade` | MISSING | Ordinary upgrade contract scaffold (inspection/planning/migration). |
| `meta-signal-upgrade` | MISSING | Owner-only upgrade meta-signal contract scaffold. |
| `signal-core` | MISSING | Signal wire kernel: typed frames, envelopes, channel macro. |
| `signal` | MISSING | Sema-ecosystem record vocabulary atop `signal-core`. |
| `owner-signal-persona` | MISSING | Owner-only Persona engine-manager contract: launch/retire/start/stop/status. |
| `signal-engine-management` | MISSING | Ordinary Persona manager-to-component lifecycle contract. |
| `signal-persona` | MISSING | Retired compatibility shim for the former combined Persona signal surface. |
| `signal-persona-origin` | MISSING | Persona origin-context vocabulary (engine/route/channel ids, origins). |
| `signal-agent` | MISSING | Ordinary agent front-door contract for pre-configured API agent calls. |
| `owner-signal-agent` | MISSING | Owner-only agent policy contract (backend/provider config + lifecycle). |
| `signal-message` | MISSING | Message-CLI-to-router channel contract. |
| `signal-router` | MISSING | Router-owned observation contract (accepted messages, route decisions, delivery status). |
| `owner-signal-router` | MISSING | Owner-only router policy contract. |
| `signal-system` | MISSING | System-observation-to-router channel contract. |
| `signal-harness` | MISSING | Router-to-harness delivery/observation channel contract. |
| `signal-terminal` | MISSING | Terminal transport control contract (prompt patterns, input gates, ack records). |
| `owner-signal-terminal` | MISSING | Owner-only terminal session lifecycle mutation (CreateSession/RetireSession). |
| `signal-mind` | MISSING | Mind/orchestration contract vocabulary. |
| `owner-signal-mind` | MISSING | Owner-only mind policy contract. |
| `orchestrate` | HAS | Orchestration component runtime. |
| `signal-orchestrate` | MISSING | Ordinary orchestration contract vocabulary. |
| `owner-signal-orchestrate` | MISSING | Owner-only orchestration policy contract. |
| `signal-criome` | MISSING | Criome trust/attestation contract (BLS envelopes, identity, delegation, releases). |
| `repository-ledger` | MISSING | Triad component recording pushed repo changes from Gitolite into a sema-engine DB. |
| `signal-repository-ledger` | MISSING | Ordinary repository-ledger contract (receive-hook event assertions + read queries). |
| `owner-signal-repository-ledger` | MISSING | Owner-only repository-ledger contract (registration, spool policy). |
| `nexus` | MISSING | Typed semantic text vocabulary written in NOTA syntax. |
| `nexus-cli` | MISSING | CLI surface for Nexus-shaped NOTA records. |
| `nota` | HAS | NOTA language home. |
| `nota-next` | HAS | Replacement NOTA implementation for the schema-derived stack (raw structural parsing, spans). |
| `nota-codec` | HAS | NOTA parser/encoder/decoder; no Nexus semantics. |
| `nota-derive` | MISSING | NOTA derive support. |
| `nota-config` | MISSING | Strict one-argument typed configuration input over NOTA/.nota/.rkyv. |

### Adjacent active work

| Repo | INTENT.md | One-line purpose |
|---|---|---|
| `criome` | MISSING | Minimal Spartan BLS12-381 authentication/attestation daemon. |
| `cloud` | HAS | Runtime repo for provider API management (documentation-only at birth). |
| `signal-cloud` | MISSING | Ordinary cloud contract (provider/capability observation, desired-state validation). |
| `meta-signal-cloud` | MISSING | Meta policy cloud contract (credential handles, provider account policy, plan approval). |
| `domain-criome` | HAS | Runtime repo for Criome-domain registry, intelligent resolution, provider-neutral projection. |
| `signal-domain-criome` | MISSING | Ordinary domain-criome contract (domain observation, resolution, projection). |
| `meta-signal-domain-criome` | MISSING | Meta policy domain-criome contract (registration, delegation, retirement). |
| `chroma` | MISSING | Active system-operator visual/scheduler work. |
| `CriomOS` | MISSING | Operating-system layer for the broader project. |
| `CriomOS-home` | MISSING | User/home-manager surface for the OS layer. |
| `mentci-lib` | MISSING | Future shell-state consumer of Sema patterns. |
| `horizon-rs` | MISSING | Active Rust codebase with NOTA/Rust discipline overlap. |
| `lojix-cli` | MISSING | Active CLI/Nix discipline reference (production Stack A horizon projection). |
| `goldragon` | MISSING | Active workspace-adjacent tooling. |
| `chronos` | MISSING | Active enough to keep visible, not Persona-core. |
| `TheBookOfSol` | MISSING | Poet/prose surface, not Persona-core. |

### Replacement stack and brief-named extras

| Repo | INTENT.md | One-line purpose |
|---|---|---|
| `signal-lojix` | MISSING | Wire surface for `lojix` daemon (skeleton + ARCHITECTURE.md). |
| `lojix` | MISSING | Lojix daemon + thin CLI client (lean horizon rewrite, Stack B). |
| `criomos-horizon-config` | MISSING | Pan-horizon constants repo (operator/suffixes/LAN pool/reserved labels). |
| `signal-frame` | MISSING | Wire kernel: frame envelope, length-prefixed rkyv archives (named in audit brief; NOT in active-repositories.md). |

## Tally

Counted across the active-repositories.md set plus brief-named
`signal-frame` (78 distinct repos; `primary` excluded from the gap count
because the canonical `/home/li/primary/INTENT.md` exists):

- **HAS INTENT.md: 14 repos** — `persona`, `sema-engine`, `schema`,
  `schema-next`, `schema-rust-next`, `triad-runtime`, `persona-spirit`,
  `spirit`, `orchestrate`, `nota`, `nota-next`, `nota-codec`, `cloud`,
  `domain-criome`.
- **MISSING INTENT.md: 64 repos** (full list in
  `missingIntentFiles` of this review's structured output, and in the
  tables above).

The HAS set is almost exactly the schema-derived core build chain plus
the two new doc-first runtime repos (`cloud`, `domain-criome`) and the
NOTA language repos. **Every `signal-*` / `owner-signal-*` /
`meta-signal-*` contract repo without exception is MISSING an
`INTENT.md`** — that is the single largest coherent gap. Every runtime
component daemon repo except those in the schema-pilot chain
(`mind`, `router`, `message`, `introspect`, `system`, `harness`,
`terminal`, `terminal-cell`, `repository-ledger`, `criome`) is also
MISSING.

## What the psyche should notice

The signal/contract families are the densest gap and also the most
self-describing repos (a `signal-*` repo IS its contract). One could
argue the contract schema is the intent — but per AGENTS.md the
per-repo `INTENT.md` is the canonical psyche-intent manifestation
surface, and these contracts carry real owner-vs-ordinary policy
decisions (the `owner-signal-*` / `meta-signal-*` split) that are pure
intent, not mechanism. Those are exactly the decisions an `INTENT.md`
should record.

The triad pattern makes the gap visible in threes: for `router`,
`message`, `terminal`, `mind`, `orchestrate`, `version-handover`,
`upgrade`, `repository-ledger`, `cloud`, `domain-criome`, each has a
daemon repo + a `signal-*` repo + an owner/meta repo, and in almost
every triad **zero or one** of the three carries an `INTENT.md`
(`orchestrate` and `cloud`/`domain-criome` being the only daemon repos
in their triads that do). No triad has its `signal-*` or `owner/meta`
leg covered.

`lore` and `signal-frame` are the two edge cases: `lore` is cross-cutting
discipline (may not need a component-style `INTENT.md`), and
`signal-frame` is named in the audit brief but absent from
`active-repositories.md` — worth confirming whether `signal-frame` is
still active or has been folded into `signal-core`/`triad-runtime`.

No code was edited and no INTENT.md was written; this is a presence
catalogue only, per the review's constraints.
