# 563 — old-code audit after the archival pass

designer, 2026-06-08. Fleet-wide audit (workflow `wiwh04zfz`, four read-only
cluster sweeps) for **old code still referenced/used** and **old design
patterns still present**, run right after the deprecated-repo archival (report
`562`). The remediation work-list this produces is the concrete shape of "no old
design left anywhere" for the persona engine.

## Headline

The fleet is **cleaner on patterns than on references**. Fleet-wide there is
**no** `capnp`, **no** `ractor`, **no** `OwnerSignal`/`owner-signal-*` naming,
**no** live `Asschema` type, **no** `signal-core` import, and `serde_json` only
at legitimate external boundaries (niri IPC, Pi-RPC, Cloudflare CLI) — never on
the inter-component wire. The **signal-executor four** (orchestrate, upgrade,
repository-ledger, persona-spirit) are **clean of signal-executor** — the
executor→nexus retirement (`gb87`) landed, each with a guard test.

The debt is concentrated in three places: (1) the dangling references the
archival just created, (2) the `signal_channel!` contract backlog, (3) the
daemon-shell + actor-shell migration.

## A. Build-breaking dangling references (created by the archival — fix first)

Deleting `signal-persona-origin` + `signal-engine-management` (production-pinned,
per your "delete now") broke the builds that depend on them.

- **`signal-engine-management` + `signal-persona-origin` — 16 active repos**:
  router, terminal, system, signal-system, signal-introspect, introspect,
  harness, signal-harness, mind, signal-mind, signal-agent, persona,
  **persona-spirit (PRODUCTION — won't `cargo build`/`nix build`)**,
  signal-persona, meta-signal-persona, meta-signal-terminal. Each has the
  Cargo.toml git-dep **and** live `use signal_engine_management::` /
  `use signal_persona_origin::` imports (heaviest in `persona`, ~100 refs).
  **Fix = the migration**: fold both vocabularies (SocketMode, WirePath,
  ComponentName, EngineIdentifier, OwnerIdentity, ConnectionClass, the
  EngineManagement lifecycle types) into the canonical `signal-persona` /
  `meta-signal-persona` pair — this is the `n0ss` third-contract fold, and the
  deletion is its forcing function.
- **`nota-codec` — 4 active crates**: `lojix/triad-port`, `signal-lojix/triad-port`,
  `meta-signal-lojix/triad-port`, `signal-sema-upgrade`. Pure dep+import swap to
  `nota-next` (StructuralMacroNode codec).
- **`spirit/flake.nix`** vendors four deleted repos (`nota-codec`, `nota-derive`,
  `schema`, `signal-core`) through a full input → cp → `substituteInPlace` →
  `[patch]` → Cargo.lock-sed pipeline (`flake.nix:16-253`, `flake.lock`,
  `tests/nix_integration.rs:220`). None are in spirit's Cargo build graph — pure
  vendoring cruft. Cached builds still work; `nix flake update` fails. Rip the
  four out wholesale (exact lines enumerated in the audit output).
- **`workspace/flake.nix`** inputs `nota-codec`/`nota-derive` — but `workspace`
  is itself archived; retire the flake rather than repair.

## B. The `signal_channel!` contract backlog (the biggest pattern debt)

Only `signal-message` and `signal-terminal` are schema-derived. **~24 contract
repos still invoke the legacy `signal_channel!` macro** and must migrate to the
`schema/lib.schema` + `build.rs` + schema-rust-next shape (the template proven
in `signal-terminal`, report `561`-era work): signal-agent, signal-cloud,
signal-criome, signal-domain-criome, signal-forge, signal-harness,
signal-introspect, signal-mind, signal-orchestrate, signal-persona,
signal-repository-ledger, signal-spirit, signal-system, signal-version-handover,
plus meta-signal-{agent, cloud, domain-criome, mind, orchestrate, persona,
repository-ledger, spirit, terminal, version-handover}, plus signal-sema-upgrade.
`signal-frame/macros` is the macro's definition home — it retires when the last
consumer migrates, not before.

## C. Daemon-shell + actor-shell migration (partial)

Three coexisting states:

- **Migrated** (schema-emitted `Async*ListenerDaemon` + `GeneratedDaemonRuntime`,
  real kameo actor engines): `message`, `router`, `terminal`, `repository-ledger`.
  These are the reference shape.
- **Hand-written accept loops** around real kameo actors (pattern #3 — spine
  needs the schema shell, engine is fine): `introspect`, `system`, `harness`,
  `persona-spirit`, `persona`, `mind`, `terminal-cell`.
- **Fully old sync spine** (worst): `orchestrate` — `triad_runtime::{MultiListenerDaemon,
  BoundedWorkers}` + a `Mutex`-wrapped `OrchestrateService` synchronous engine +
  an `OperationLowering` ZST namespace. A migrated `src/schema/daemon.rs` already
  exists but `main` doesn't use it. Delete `src/daemon.rs`, wire `main` to the
  schema shell, make the engine a real actor.

**Root cause of the non-actor shell — the emitter.** `schema-rust-next` emits a
`tokio::sync::Mutex<SubscriptionState>` daemon (`daemon_emit.rs:922,937`), which
is why `spirit` (no `kameo` dep at all; `engine.rs:36 nexus: Mutex<Nexus>`;
`SignalActor` carrying "actor" wording for a non-actor) is a synchronous shell.
Per `zk6y`/`96mi`/`ilxh` the emitter must generate **real Kameo actor engines**.
This is a `schema-rust-next` + `triad-runtime` foundation change that unblocks
the actor-shell axis fleet-wide — and `triad-runtime` already has the pieces
(`RequestGate` is a real `impl Actor`, `Runner::drive` exists).

## D. Workspace-surface stale references (mine to fix — doing now)

- `protocols/active-repositories.md`: 7 table rows for deleted repos
  (`schema:36`, `signal-core:50`, `signal-engine-management:53`,
  `signal-persona-origin:55`, `nota:76`, `nota-codec:78`, `nota-derive:79`) +
  3 prose `signal-core` seams (`sema-engine:35`, `signal:51`, `lojix:115`).
- `RECENT-REPOSITORIES.md`: 5 dead rows (nota, nota-codec, nota-derive, prism,
  signal-core).
- `skills/`: ~11 files with stale `signal-core`→`signal-frame`/`signal-sema` and
  `nota-codec`/`nota-derive`→`nota-next` references (storage-and-wire,
  nix-discipline, micro-components, contract-repo, subscription-lifecycle,
  language-design, operator, system-operator). Mostly examples; agent-misleading,
  so worth a sweep.
- `repository-management.md`: should document the archival procedure
  (delete remote + `mv ~/git-archive/` + prune `active-repositories.md`).

## E. Open program-level questions (n0ss two-contract rule)

- **Missing `meta-signal-<c>`**: `message` (has `signal-message`, no meta),
  and `meta-signal-sema`/`meta-signal-nexus` don't exist. Confirm whether
  `message` gets a meta tier and whether `sema`/`nexus` are components (needing
  the pair) or kernel libraries (exempt).

## Remediation priority

1. **Unbreak production**: `persona-spirit` — fold engine-management +
   origin vocab onto `signal-spirit`/`meta-signal-spirit`, drop the two deleted
   deps. (Highest stakes; it's the deployed Spirit's source.)
2. **Unbreak the active fleet**: the other 15 repos' dangling deps → fold into
   `signal-persona`/`meta-signal-persona`; the 4 `nota-codec` crates → `nota-next`.
3. **Clean `spirit/flake.nix`** (rip the 4-repo vendor pipeline).
4. **Workspace docs** (D — doing now).
5. **Emitter actor-shell** (`schema-rust-next` → real kameo actors) — the
   foundation change that unblocks the daemon-shell axis.
6. **`signal_channel!` contract migrations** (B) — the long tail, fan-out using
   the `signal-terminal` template.
7. **orchestrate** sync-spine deletion; missing-meta confirmations (E).
