# Mainline Architecture

I have everything I need. All reading was done directly in this run. Here are my complete structured findings.

# Persona / Criome — Reconstructed System Map

Read-only architecture analysis, 2026-07-01. Every claim is grounded in a file path; FACT = stated in a doc, INFERENCE = my synthesis. Repos live at `/git/github.com/LiGoldragon/<name>/`.

## 1 · One-paragraph system definition

Persona is a **meta-AI system that organizes models into a structure emulating human intelligence**, built on the **Criome stack** — a multi-repo Rust-on-Linux system where the "thinking" is done by agent LLMs and the software is deliberately **dumb mechanism** that no component runs without an LLM on the other end of the wire (FACT: `/home/li/primary/ARCHITECTURE.md` §0.5 "What the workspace is building", lines 46–55). Concretely today it is a fleet of **micro-component daemons** (each a long-lived daemon + a thin CLI + one or two typed `signal-*` wire contracts) coordinated by a privileged `persona-daemon` engine manager, persisting typed records in per-component `.sema` databases, communicating over binary rkyv Unix-socket frames, with NOTA text used only at the human/agent edge (FACT: `persona/ARCHITECTURE.md` §0 lines 18–58; §0.6 "Shared component architecture patterns" of the workspace file). Persona is positioned explicitly as **"the durable agent"** — a long-lived, inspectable agent runtime rejecting one-shot agent CLIs, tmux-as-runtime, and polling-based reconciliation (FACT: `persona/ARCHITECTURE.md` §0.5 table, lines 79–92). The whole thing is a "realization step" toward an eventual self-hosting `Sema`-on-`Sema` substrate; today's pieces are built rightly for today's scope (FACT: `persona/ARCHITECTURE.md` lines 102–113; `sema/ARCHITECTURE.md` §Scope lines 21–31).

## 2 · Component / layer map

ASCII layering from storage up. Confirmed against the docs; the prompt's proposed layering is essentially correct, with two corrections noted below.

```
                     ┌─────────────────────────────────────────────┐
 PLATFORM            │ CriomOS / CriomOS-home / CriomOS-lib / lojix │  NixOS host, deploy
                     │ horizon-rs (cluster projection), forge       │
                     └─────────────────────────────────────────────┘
                     ┌─────────────────────────────────────────────┐
 APEX / MANAGER      │ persona (persona-daemon: engine manager)     │  supervises N engines
                     │  spirit(intent) mind message router harness  │  each engine = full
                     │  terminal/-cell system introspect orchestrate│  component federation
                     │  upgrade agent listener mentci ...           │
                     └─────────────────────────────────────────────┘
                     ┌─────────────────────────────────────────────┐
 TRUST / AUTH        │ criome (BLS12-381 sign/verify/attest daemon) │  "Criome verifies;
                     │  clavifaber (per-host key publication)       │   Persona decides"
                     └─────────────────────────────────────────────┘
                     ┌─────────────────────────────────────────────┐
 CONTRACTS / WIRE    │ signal-frame (frame kernel) + signal-<comp>  │  rkyv binary contracts
   + VOCABULARY      │ + meta-signal-<comp> ; signal-sema (6 verbs) │  two contracts/component
                     │ signal-standard, signal-derive               │
                     │ nexus (typed semantic TEXT vocab in NOTA)    │  human/agent text edge
                     └─────────────────────────────────────────────┘
                     ┌─────────────────────────────────────────────┐
 STORAGE ENGINE      │ sema-engine (full DB engine: verb exec,      │  per-component redb,
                     │  query/mutation plans, op-log, snapshots,    │  no shared store daemon
                     │  subscriptions, versioned commit log)        │
                     └─────────────────────────────────────────────┘
                     ┌─────────────────────────────────────────────┐
 STORAGE KERNEL      │ sema (redb + rkyv + schema-version guard,    │  "signal-core is to wire
                     │  closure-scoped txns, Table<K,V>)            │   as sema is to state"
                     └─────────────────────────────────────────────┘

 CROSS-CUTTING (build-time only, never linked into runtime binaries):
   nota-next  →  schema-next  →  schema-rust-next     [the schema-derived stack]
   triad-runtime (shared Signal/Nexus/SEMA daemon runtime), rust-build, version-projection
```

Corrections to the prompt's proposed layering:
- **sema is NOT one layer** — it is split into `sema` (kernel: redb/rkyv/schema-guard) and `sema-engine` (the full database engine: verb execution, plans, op-log, snapshots, subscriptions). The kernel must not depend on the engine (FACT: `sema/ARCHITECTURE.md` §Boundary lines 62–83; §Status line 239; `active-repositories.md` lines 37–39).
- **signal vs nexus are different kinds of thing.** `signal-*` = binary rkyv **wire** contracts. `nexus` (the repo) = a typed semantic **text** vocabulary written in NOTA + a translator daemon; it is NOT a wire layer parallel to signal (FACT: `nexus/ARCHITECTURE.md` lines 1–15, "Two messaging surfaces" table lines 119–130). Note the naming overlap: "Nexus the plane" (decision/execution engine in the runtime triad) ≠ "nexus the translator" (this repo) — the doc calls this out explicitly (`nexus/ARCHITECTURE.md` "Nexus the plane vs. nexus the translator", lines 14–56).

### Per-repo role (what each does / how it connects)

Component daemons in the Persona federation (FACT: `persona/ARCHITECTURE.md` §1 Component Map lines 191–214; `active-repositories.md`):
- **persona** — host-level `persona-daemon` engine manager; supervises N engines, each owning a full component federation; allocates per-engine sockets/`.sema` dirs; owns manager state (engine catalog, health, active-version snapshots), upgrade process-lifecycle, and the SCM_RIGHTS public-socket handoff. Talks via `meta-signal-persona` (management) and `signal-persona` (manager↔component lifecycle).
- **mind** — central Persona state component: work graph, typed thoughts/relations, subscriptions, choreography policy, channel adjudication ("mind decides; router enforces"). Contracts `signal-mind`/`meta-signal-mind`. Intended to replace lock-file/BEADS orchestration over time.
- **message** — engine-owner ingress: `message` CLI + `message-daemon`; binds `message.sock` (0660, engine-owner group), stamps `MessageOrigin::External` via SO_PEERCRED, forwards typed frames to router.
- **router** — routing/delivery/gate state; holds live `authorized-channel` state keyed by (source,destination,kind); parks unknown-channel messages for mind adjudication. Binds `router.sock` (0600). Contracts `signal-router`/`meta-signal-router`.
- **harness** — harness identity/lifecycle/transcripts, delivery adapter boundary.
- **terminal / terminal-cell** — `terminal` = durable PTY/session owner (currently archived/inactive); `terminal-cell` = the active low-level PTY/transcript daemon used directly for V1 harness / Claude/Codex tests (FACT: `active-repositories.md` lines 36, 93).
- **system** — OS/window focus observation; `FocusTracker` Niri actor is real but the component is **paused** (no live consumer) (FACT: `persona/ARCHITECTURE.md` §0.7 lines 156–174).
- **introspect** — supervised inspection-plane component; asks each component daemon for typed inspectable records over Signal and projects NOTA at the edge; NOT in the delivery path, does not open peers' `.sema` (FACT: `persona/ARCHITECTURE.md` §0.6 lines 116–155).
- **orchestrate** — orchestration machinery under mind authority: role claims, handoffs, activity, spawn/supervise/schedule/escalate (FACT: `persona/ARCHITECTURE.md` §0.8 lines 176–187).
- **upgrade** — upgrade triad runtime (owner of schema/version migration, handover driver); Persona is now only a process-lifecycle participant (FACT: `persona/ARCHITECTURE.md` §1.6.7 lines 471–531).
- **spirit** — the intent-store daemon AND the copyable exemplar of the schema-derived triad stack (see §4).
- **agent** — front-door for pre-configured API agent calls (`signal-agent`/`meta-signal-agent`); newest cognitive-edge component (first commit 2026-06-09).
- **listener** — STT/listener component (first commit 2026-07-01, 5 commits — the newest thing in the tree; contracts `signal-listener`/`meta-signal-listener` exist).
- **mentci** — programmable human-approval daemon for the local per-Unix-user criome; `mentci-daemon` owns UI state + a socket endpoint, `mentci` is the thin client (FACT: `active-repositories.md` line 75; first commit 2026-06-18). Spelling note: "Menchie" was an STT error, migrated to mentci (FACT: workspace `ARCHITECTURE.md` §0.7 lines 266–267).

Foundational / cross-cutting:
- **criome** — today's minimal Spartan BLS12-381 auth/attestation daemon (identity registry, sign/verify, attestations, routed authorization); "Criome verifies, Persona decides" (FACT: `criome/ARCHITECTURE.md` §0 lines 30–81).
- **sema / sema-engine** — storage kernel / full engine (above).
- **nexus / nexus-cli** — NOTA↔Signal translator daemon + typed text vocabulary.
- **nota-next / schema-next / schema-rust-next** — the schema-derived stack (see §4).
- **triad-runtime** — shared runtime for schema-derived Signal/Nexus/SEMA daemons: trace logging, rkyv frame transport, Unix listeners, the bounded thread-per-connection worker model, subscription registry (FACT: `active-repositories.md` line 42; workspace `ARCHITECTURE.md` §0.6 lines 137–141).
- **CriomOS family + lojix + horizon-rs + forge** — the NixOS platform and deploy layer (FACT: `CriomOS/ARCHITECTURE.md`; `active-repositories.md` "Replacement Stack" lines 119–202).

### How components talk (the two triads)

This is the central pattern; the prompt asked specifically about it.

**Runtime LOGIC triad — Signal / Nexus / SEMA** (FACT: workspace `ARCHITECTURE.md` §0.6 lines 121–141; `spirit/ARCHITECTURE.md` "Runtime triad" lines 133–169; `schema-next/ARCHITECTURE.md` "Engines and the request pipeline" lines 898–920):
- **SEMA** owns durable state/storage (the body at rest).
- **Nexus** owns decision-making + request execution (the execution engine + the keeper of in-flight mail between Signal ingress and SEMA reply).
- **Signal** owns communication (movement across channels; admission, dispatch, identity-stamping, wire-frame handling — nothing heavy).
- Request flow: `Signal in → Nexus → SEMA → Nexus → Signal → client`. Trait method counts encode order: `SignalEngine` has 2 (triage, reply), `NexusEngine` has 1 (execute), `SemaEngine` has 2 (apply, observe). Push only on success. Async throughout, with a rolling **origin route** threaded through every layer for reply correlation.

**Packaging triad — two contracts per component** (FACT: workspace `ARCHITECTURE.md` §0.6 lines 144–171):
- `signal-<component>` — ordinary working/peer-callable signal.
- `meta-signal-<component>` — meta policy/authority (config, owner-only ops). `MetaSignal` is canonical; `OwnerSignal` is deprecated.
- Each contract → one thin CLI (`<component>` and `meta-<component>`). Every daemon binds its meta socket even if its only op is `Configure`. The meta socket is the authority lane (mode 0600, owner-only). Splitting into separate repos buys rebuild-churn isolation, security visibility, and optionality — NOT where state/logic lives.

**Wire discipline** (FACT: workspace `ARCHITECTURE.md` §0.6 "Wire and identity discipline" lines 195–229; `signal/ARCHITECTURE.md` "Target Signal direction" lines 273–422):
- **No NOTA between components.** Daemons exchange binary rkyv frames over Unix sockets via `signal-frame` (4-byte length-prefix, bytecheck on read). The CLI is the only translation/text-debug surface.
- **rkyv**, not capnp. capnp/Cap'n-Proto is referenced only as a *comparison* ("superset of Cap'n-Proto-style spec languages"; "Cap'n-Proto-style structural-compatibility discipline lives at the rkyv layer") — it is not a wire format in use (FACT: `schema-next/ARCHITECTURE.md` line 55; `sema/ARCHITECTURE.md` line 317).
- Every message carries an un-schema-declared **origin route** (short return address) + a **short header** (64-bit, 8 enums, constant-time namespace discrimination).
- **NOTA's role:** NOTA is the *only* text syntax; it is the human/agent projection at the edge (CLI parse/print, agent-authored records). Schema is a specialized NOTA dialect. Binary-only daemon builds structurally reject NOTA at the wire (FACT: `spirit/ARCHITECTURE.md` "Layers" lines 20–47 and `tests/socket_negative.rs` reference lines 254–258; workspace `ARCHITECTURE.md` §0.7 "The three-part vocabulary" lines 279–286: SCHEMA specifies / SIGNAL moves / SEMA is the body).

## 3 · Design principles (each tagged)

All are FACT unless marked INFERENCE. Path given per principle.

- **Typed records over flags / no `Unknown` escape at closed boundaries.** Prefer closed typed enums; the variant set lives in the type system; unmatched cells return typed errors (`Unavailable`/`Unauthorized`/`NotImplemented`), and "the error surface IS part of the trait surface." FACT: `schema-next/ARCHITECTURE.md` "Effect table and the match-matrix surface" lines 924–933; `signal/ARCHITECTURE.md` lines 168–172.
- **Every function is a method on a data-bearing type; async mail modeled as object flow.** No free helpers where a method fits; module-level routing helpers are forbidden in favor of typed envelopes moving between objects. FACT: `spirit/ARCHITECTURE.md` "Implementation methods" lines 650–693 ("the code must not replace that movement with module-level routing helpers").
- **Micro-components: one capability per component.** Distinct nouns split into independently-buildable typed components sized for fresh-agent context. FACT: workspace `ARCHITECTURE.md` §0.6 "Component binary naming"; `criome/ARCHITECTURE.md` See-also line 684 (micro-components); the 90+ repos in `repos-manifest.nota` are the evidence.
- **Push, not poll.** Producers push, consumers subscribe; escalate deeper rather than tune sleep intervals. Bounded reachability probes (e.g. "is the child listening yet") are an explicit carve-out, not polling. FACT: workspace `ARCHITECTURE.md` §"Push, not poll" lines 94–100; `persona/ARCHITECTURE.md` "Bounded reachability probe vs ongoing polling" lines 833–855; `criome/ARCHITECTURE.md` line 158.
- **NOTA as human projection; state in typed stores; Rust-to-Rust wire is binary.** FACT: workspace `ARCHITECTURE.md` §0.6 "No NOTA between components" lines 197–201; `signal/ARCHITECTURE.md` "Signal is binary only" lines 284–292.
- **Schema is the source of truth.** One `.schema` file generates data types, wire, storage, and upgrade behavior; hand-written Rust implements *only behavior* on generated nouns. FACT: `schema-next/ARCHITECTURE.md` "What schema is" lines 17–24; "The data / hand-written boundary" lines 807–815.
- **Clarity > correctness > introspection > beauty; NOT optimizing speed / feature volume / MVP / backward-compat / time estimates.** Priority order, earlier wins on conflict. FACT: workspace `ARCHITECTURE.md` §0.5 lines 58–67.
- **No backward-compat for systems being born.** Break the system if it makes it more beautiful; compatibility binds only at explicitly declared versioned boundaries. FACT: workspace `ARCHITECTURE.md` §0.5 lines 70–77.
- **Today vs eventually — different things, different names.** `sema`/`sema-engine` vs eventual `Sema`; `criome` daemon vs eventual `Criome`. A scope discipline, not a license to cut corners. FACT: workspace `ARCHITECTURE.md` §"Today and eventually" lines 103–112; enforced in every repo's Scope callout.
- **Engines are match-matrices over enums (enum × enum → outcome per cell).** FACT: workspace `ARCHITECTURE.md` §"Engines are match-matrices" lines 180–193; `schema-next/ARCHITECTURE.md` lines 924–933.
- **Everything is a struct; schema handles only the workspace Rust subset (no tuples); a field's role is its type (no two fields share a type).** FACT: `schema-next/ARCHITECTURE.md` "Foundational model" lines 62–93.
- **Full-English-word naming; single-colon symbol paths as universal identity; shortest-reliable-identifier first-class.** FACT: workspace `ARCHITECTURE.md` §5 line 451, §0.6 lines 213–220.
- **Components must prove themselves on the live path** (no dead scaffolding beside an older code path; wrapping an old path is not migration). FACT: workspace `ARCHITECTURE.md` §"Components must prove themselves" lines 242–250.
- **Local trust = OS boundary (Unix-user + filesystem ACL + SO_PEERCRED), not in-band crypto proof.** The crypto-first alternative was explicitly rejected for local components. FACT: `persona/ARCHITECTURE.md` §1.6.1 lines 308–330; `criome/ARCHITECTURE.md` §"Security model" lines 166–212.
- **Content/data daemon privilege = can-ingest-and-serve-content, not can-read-anything; store unwritable by anything but the daemon.** FACT: workspace `ARCHITECTURE.md` §"Privilege and authentication boundaries" lines 233–241.
- INFERENCE: **Intent-primacy is architecturally load-bearing, not just process.** The spawn order puts `spirit` (intent) *last* as the "cognitive apex that animates the system," and the guardian rejects non-intent "matter" at admission — i.e. the intent layer is treated as the top of the authority graph in running code, mirroring the workspace's "intent precedes structure" invariant. Basis: `persona/ARCHITECTURE.md` §1.7.1 lines 680–699; `spirit/ARCHITECTURE.md` "Guardian admission" lines 474–485; workspace `ARCHITECTURE.md` §6 lines 469–471.

## 4 · The schema-derived stack (schema-next / nota-next / schema-rust-next)

Created 2026-05-26 (git: all three first-commit 2026-05-26). **Problem it solves / how it relates to older schema+NOTA** (FACT: `active-repositories.md` "Current Truth Pins" lines 236–241; `schema-next/ARCHITECTURE.md`; `nota-next` row lines 83):

- The `-next` repos are the **canonical replacements** for the deprecated `nota` / `schema` repos; the `-next` suffix is vestigial and slated to drop (Spirit `4ups`). FACT: `active-repositories.md` lines 236–241.
- **nota-next** — replacement NOTA implementation: raw structural block parsing, source spans, `qualifies_as_*`, and the **StructuralMacroNode** codec (`#[derive(StructuralMacroNode)]`) decoded by SHAPE (type-directed, structural match in declaration order, first-match-wins, recursive) with bidirectional encode. NOTA is "a thin structure-sensing library carrying no meaning" (FACT: `schema-next/ARCHITECTURE.md` line 27; `active-repositories.md` line 83).
- **schema-next** — the schema **macro engine + typed semantic data model**. It turns NOTA structure into typed schema-in-Rust source data (`SchemaSource` → semantic `Schema`), but **does not emit Rust itself**. A `.schema` file IS full NOTA (a specialized dialect), not a separate language. The old **Asschema** assemble step was *removed* (record `6cfr`); resolution now lives as methods on the source types. FACT: `schema-next/ARCHITECTURE.md` lines 1–7, "Semantic Schema" lines 354–381; `active-repositories.md` line 40.
- **schema-rust-next** — the Rust **emission** layer: LOWERS schema-in-Rust to Rust using real macro infra (`quote!` / `proc-macro2` `TokenStream` / `ToTokens`), NOT a string generator (records `4np2`, `e6v5`); the old 52-method `RustWriter` string emitter is mid-migration out. FACT: `active-repositories.md` line 41.
- **What it buys:** one `.schema` file emits *both* a binary-only daemon build and an optional NOTA+rkyv CLI build without hand-written parallel type mirrors; content-addressable schema identity (blake3 hash of the semantic value = the version the version-control layer consumes); reducer-based migration; and "the compiler is itself data" self-hosting (Spirit `vpbx`, `g2xr`). FACT: `schema-next/ARCHITECTURE.md` "Direction" lines 30–60, "Settled architecture choices" lines 150–166; `spirit/ARCHITECTURE.md` "Layers" and "Local stack testing" lines 710–760.
- **spirit** is the running proof and copyable exemplar of this stack (FACT: `spirit/ARCHITECTURE.md` Purpose lines 3–17).

## 5 · Three-wave evolution narrative (dated)

Context: the canonical rewrite / reset landed 2026-04-23 (per the brief). Git first-commit dates confirm three clean waves. Note that `criome` (first commit 2024-05-28) and `sema` (2019-11-06) are **old repos reset/rewritten in place** — `criome/ARCHITECTURE.md` "Archaeology note" (lines 19–27) records the pre-rewrite sema-records-validator skeleton at commit `a3f4173`, deferred to eventual Criome.

**Wave (a): Reset week — 2026-04-23 to ~04-28. Foundations laid.** (git first-commits: `nexus` 04-23, `CriomOS` 04-23, `signal` 04-25; `criome`/`sema` reset in place around then.)
- Accomplished: re-established the storage kernel (`sema`), the sema-ecosystem record vocabulary + local wire envelope (`signal`), the NOTA↔Signal translator (`nexus`), the auth/records daemon (`criome`), and the NixOS platform (`CriomOS`). This is the "criome stack" seed: text-in-NOTA → translator → Signal → criome+sema. Evidence: `signal/ARCHITECTURE.md` (still-legacy envelope, "Per Li 2026-04-25" quote line 243); `nexus/ARCHITECTURE.md`; `sema/ARCHITECTURE.md` §Status.

**Wave (b): Persona component-daemon burst — 2026-05-06 to ~05-23.** (git: `message` 05-06, `persona` 05-06, `mind`/`router`/`harness`/`system` 05-07, `terminal-cell` 05-10, `introspect` 05-13, `lojix` 05-13, `sema-engine` 05-14, `orchestrate` 05-18, `repository-ledger` 05-19, `cloud`/`domain-criome` 05-23, `upgrade` 05-24.)
- Accomplished: the Persona federation as a set of micro-component daemons with the two-contract packaging triad. The engine-manager model (one `persona-daemon`, N engines, per-engine sockets/`.sema`), channel choreography ("mind decides, router enforces"), filesystem-ACL local trust, and the `sema`→`sema-engine` split all land here. Evidence: `persona/ARCHITECTURE.md` §1.5–§1.6; `sema/ARCHITECTURE.md` §Status (sema-engine "created as a sibling library-only repo," first consumer persona-mind in flight).

**Wave (c): Schema-derived wave — 2026-05-26 to ~06-13 (extending into July).** (git: `spirit` 05-26, `schema-next` 05-26, `nota-next` 05-26, `schema-rust-next` 05-26; `triad-runtime` 06-02.)
- Accomplished: the schema-as-source-of-truth stack (§4) and its first running exemplar, `spirit` — the intent-store daemon proving `.schema` → binary daemon + NOTA CLI, guardian LLM admission, versioned SEMA commit log, meta-socket owner-only deletion. `spirit` is the single most actively developed repo (265 commits May–Jul, confirmed). `triad-runtime` extracts the shared daemon runtime. Evidence: `spirit/ARCHITECTURE.md` in full; `schema-next/ARCHITECTURE.md`.

## 6 · Current-state snapshot (as of 2026-07-01)

**Production / running today:**
- **CriomOS deploy stack A** — running on every node; `lojix-cli` monolith projecting `horizon-rs` over `goldragon/datom.nota`; already migrated to nota-next (FACT: `active-repositories.md` "Stack A" lines 157–169).
- **criome** — real BLS12-381 (min-pk) sign/verify/attest with registry, revocation, replay guard, expiry live; still skeleton for master-key signing of authorization grants, pushed observation events, quorum aggregation (FACT: `criome/ARCHITECTURE.md` §9 lines 590–668).
- **spirit** — "active production Spirit implementation" (FACT: `active-repositories.md` line 43); durable versioned SEMA store, guardian admission, migration path. Known-in-progress: mail ledger still in-memory, schema diff/upgrade traits unimplemented, `Store` still under a mutex not a kameo actor (FACT: `spirit/ARCHITECTURE.md` "Known limits" lines 796–823).
- **cloud** — DigitalOcean adapter witnessed end-to-end **once** (droplets 578866840, 578873541); behavioral axis closed but the artifact axis (committed re-runnable socket-apply test) is **open** (FACT: `active-repositories.md` line 103).
- **domain-criome** — daemon + CLI ship with persisted registry; birth bead closed (FACT: `active-repositories.md` line 106).

**In-progress / not yet cut over:**
- **persona engine federation** — the manager, spawn order, and dev-stack smoke path (router→harness→terminal) work; but mind adjudication, live harness login, terminal-cell live-agent delivery, and multi-engine ops are separate unfinished lanes; cross-engine is "minimal-mode" (FACT: `persona/ARCHITECTURE.md` lines 899–903, 440–448).
- **schema-derived stack** — `schema-rust-next` mid-migration off the string emitter; `schema-next` generics leg proven, trait/impl leg designed-but-not-integrated (FACT: `schema-next/ARCHITECTURE.md` lines 816–836; `active-repositories.md` line 41).
- **upgrade triad** — scaffold; target home for migration orchestration (FACT: `active-repositories.md` lines 49–51).
- **lojix daemon reshape (Stack B)** — the `lojix`/`signal-lojix` daemon rewrite on branch `horizon-leaner-shape`; smoke-built `zeus` but NOT cut over to any node (FACT: `active-repositories.md` lines 138–202).
- **system** — paused (FocusTracker real, no consumer); **terminal** — archived/inactive, use `terminal-cell` directly (FACT: `persona/ARCHITECTURE.md` §0.7; `active-repositories.md` line 93).

**Newest pieces:**
- **listener** — STT/listener component, first commit **2026-07-01** (5 commits; contracts `signal-listener`/`meta-signal-listener` exist). Newest repo in the tree.
- **mentci** — approval daemon, first commit **2026-06-18** (47 commits); SEMA in-memory, durable storage + criome verdict egress are integration work (FACT: `active-repositories.md` line 75).
- **agent** — API-agent front-door daemon, first commit **2026-06-09** (22 commits).
- (Note: `mentci-egui`/`mentci-lib` predate the daemon — first commit 2026-04-29 — likely the earlier "Menchie" approval-UI effort later folded into the mentci family.)

## 7 · Explicit UNKNOWNS / not checked

- **Only ARCHITECTURE.md/manifest surfaces were read** — I did not read source (`src/*.rs`), tests, or flake outputs. Claims about "what runs" reflect what the docs assert, not live verification. In particular, "production" for spirit/criome/cloud is the docs' word; I ran no daemon and executed no test.
- **Git dates are commit dates on the current default branch**, read via `git log`; the primary workspace uses jj and these are clones. First-commit dates for `criome` (2024) and `sema` (2019) reflect pre-reset history retained in the repo, so "first commit" ≠ "first commit of the current rewrite." I did not walk the reset commit for each repo to pin the exact rewrite date beyond criome's cited `a3f4173`.
- **Spawn-order / federation liveness:** `persona/ARCHITECTURE.md` describes a spawn order including `spirit` last and `sema-upgrade` first, but I did not verify which of these are implemented vs designed. The doc itself flags much as "minimal-mode" / "future work."
- **I did not read** the second half of `persona/ARCHITECTURE.md` (lines 964–1814; the file is 1814 lines total and I read 1–963). Sections beyond line 963 (deeper manager/upgrade/sandbox detail) are unread — flagging in case the synthesis worker needs them.
- **mentci-lib / mentci-egui early-history (2026-04-29)** and the exact relationship to the Jun-18 `mentci` daemon is inferred, not confirmed from a doc.
- **INTENT.md files:** `criome/ARCHITECTURE.md` references an `INTENT.md §"Why this repo exists"`, but the manifest lists criome's doctrine-home as `Architecture`, and the workspace forbids per-repo `INTENT.md`. I did not resolve whether criome's `INTENT.md` still exists — a possible stale reference.
- **Spirit record IDs** (e.g. `gvaz`, `4ups`, `6cfr`, and the many `schema-next` records) are cited from docs; I did not query the live Spirit store to confirm them (a `spirit` CLI query was out of scope for this read-only doc pass).