# Reality-check — the Structural Forms epic against intent + implementation

The psyche asked, of their epic brain-dump: *"determine if what I'm saying is
what's happening now, and if it's not, tell me."* This grounds each load-bearing
claim against **two** sources: recorded intent (the Spirit corpus the guardian
surfaced when it rejected an over-stated epic record) and current implementation
(a 5-agent grounding workflow). Verdict up front: **the vision is sound and
largely already in motion; three specific current-state premises are stale.** The
map needed updating, not the destination.

## Claim 1 — "the signal schema was left in Spirit; move it to the signal repo"

**INACCURATE — already done.** The split the psyche proposes as future work has
already been performed, and it is both settled intent and built:

- `signal-spirit` owns the wire contract: `schema/{signal,domain}.schema` (source)
  + generated `src/schema/{signal.rs,domain.rs}` (Input/Output/Entry/RecordRequest…).
- `spirit` owns the genuinely daemon-local planes `schema/{nexus,sema}.schema`,
  which **import** the contract (`SignalInput signal-spirit:signal:Input`) rather
  than redefine it, and `spirit/src/lib.rs` re-exports via `pub use
  signal_spirit::schema::signal::*`. **(See the meta-signal correction below —
  `meta-signal` does *not* belong in this daemon-local list.)**
- Dependency edge is one-way: `signal-spirit` has **zero** dependency on `spirit`;
  consumers (`upgrade`, `meta-signal-spirit`) bind only to `signal-spirit`. So a
  contract consumer already does not recompile when `spirit`'s engine logic changes.
- This is recorded intent: [`y88n`: the ordinary public signal/domain contract
  lives in the signal-spirit contract crate; the daemon keeps crate-local
  nexus/sema/meta-signal] and [`u7tj`: wire-contract schemas live in
  `signal-<component>` as the canonical cross-component compile boundary].

Correction to the framing: **Nexus and SEMA are not contract** and must *not* move
into `signal-spirit` — they are correctly daemon-internal planes [`yjik`,`26e7`].
Only the Signal wire types belong in the contract crate, and they are already there.

**Correction (psyche caught this; verified) — `meta-signal` is NOT correctly
daemon-local.** Unlike nexus/sema, the meta-signal contract is one of a
component's *two wire contracts* [`7sx6`], so it belongs in `meta-signal-spirit`,
imported by the daemon — exactly as `signal` lives in `signal-spirit`. Current
state was **drift**: spirit defined `schema/meta-signal.schema` locally (verbs
`Configure`/`Import`), emitted it as a `wire_contract_module`, and had *zero*
dependency on `meta-signal-spirit`; meanwhile `meta-signal-spirit` was a stale,
hand-written, non-schema-derived orphan with a disjoint vocabulary
(`Start`/`Drain`/`Reload`/`Register`/`Retire`). So this report's Claim-1 grouping
of `meta-signal` with the internal planes was wrong.

**RESOLVED by operator (2026-06-14; cross-lane review target #7 / report 630).**
Operator rebuilt `meta-signal-spirit` as a schema-derived `Configure`/`Import`
contract (`d5b5dde`) and spirit imported it (`4ec746b`: deleted the local schema +
generated module, `pub use meta_signal_spirit::schema::meta_signal::*`) — contract
byte-identical to the rebuild, verdict CONSISTENT. The rule is settled intent
(`7sx6`/`u7tj`/`tb9h`) and now explicit in `skills/component-triad.md`. The
orphan's lifecycle verbs were *not* pulled in (correctly — stale, never wired; per
operator report 378). The only remaining vocabulary item is mirror-shipper's
`MirrorTarget`, kept branch-local until the mirror feature lands (then it joins the
meta contract's `Configure`), per report 630's 378 addendum.

## Claim 2 — "keep a generated-Rust reference copy in the contract; co-host at build time for the orphan rule"

**INACCURATE — the opposite of how it works.** No "reference copy" exists, and
there is no orphan-rule problem to solve:

- Each crate **regenerates and checks in its own** schema's Rust into its own
  `src/schema/*.rs` (via `build.rs` → `GenerationDriver…write_or_check`). That
  checked-in file *is* the artifact, not a reference beside a source of truth.
  `OUT_DIR` is explicitly rejected.
- Generated Rust is **not** co-hosted into consumers. `signal-spirit` owns its
  `Input`/`Output` enums and their impls; `spirit` takes `signal-spirit` as an
  ordinary dependency and `pub use`-re-exports — it does **not** regenerate the
  contract's types, so the orphan rule never bites.
- The contract crate publishes its `schema/` dir via Cargo `links` /
  `DEP_<LINKS>_SCHEMA_DIR` purely so a downstream daemon's `build.rs` can *resolve
  imports* at generation time — not to copy types. [`0678`: generated Rust may be
  checked in as reference; consumers avoid foreign-trait duplication and wrapper
  newtypes] is satisfied by per-owner generate-and-commit.

## Claim 3 — "the engine is a set of actors, the nexus engine; inputs/outputs predefined via schema"

**PARTLY.** Split cleanly:

- **Right and load-bearing:** every component declares its input/output roots in
  schema, schema-rust-next generates them as typed Rust, and *all* inter-stage
  messages (Signal Input/Output, NexusWork/NexusAction, SEMA WriteInput/ReadInput)
  are those generated objects. The daemon spine is decode → ask → encode over the
  typed roots [`xbc2`, `5hjv`, `a71r`]. Your schema-typed-IO model is exactly the
  architecture.
- **Stale:** it is **not** currently "a set of actors." The implementation emits
  **one** kameo `EngineActor` per daemon, whose single mailbox serialises all
  requests; the three engines (Signal/Nexus/SEMA) are plain `&mut` fields behind
  it, and Nexus is a single-flight Work→Action state machine. ("meta-agent"
  appears nowhere in code.)
- **But your model matches the *intent*:** [`zk6y`: the schema-emitted
  Signal/Nexus/SEMA engines *should be* kameo actors — "actors everywhere" — and
  the current synchronous, mutex-wrapped emission is **drift to correct, not a
  sanctioned end state**] and [`zjmc`: the Work/Action reaction-frame is
  workspace-universal]. So "set of actors" is your recorded **target**; the code
  sits at the one-actor synchronous state that `zk6y` itself flags as drift.

## Claim 4 — "feature branches strict about removing all legacy"

**PARTLY — one real target, not a sweep.** The single legitimate self-host
removal target is exactly the operator slice already in flight: schema-next's
hand-written macro-model types in `declarative.rs` / `macros.rs`
(`SchemaMacro`, `MacroPattern`/`-Object`/`-Delimited`, `MacroTemplate`/…,
`MacroDelimiter`, `MacroLibrary`, `MacroPosition`) duplicate what
`core.schema:9-22` already declares — replace them with generated types. **New
finding:** `MacroShape` and `MacroOutputKind` are schema-declared in `core.schema`
but have **no** Rust yet — proof the self-host is partial. The other "legacy"
candidates (duplicated signal schema, etc.) are already done or phantom; a strict
"remove everything" sweep over the stated list would over-remove.

## Worktree audit — 33 worktrees under `~/wt/.../LiGoldragon`

All are **designer-style** feature/next branches (operator owns main + rebases —
no operator worktrees found, which is why marking by lane will help). Classes:

- **Safe to remove (2):** `persona/realign-signal-introspect` and
  `spirit/operator-guardian-hardening` — bookmark already deleted, empty no-diff
  change on main, no work to lose.
- **Investigate then remove (3):** `lojix`, `meta-signal-lojix`, `signal-lojix`
  `/triad-port` — orphaned dirs with source files but **no VCS metadata** and no
  matching bookmark; content unreachable from version control (would be lost on
  removal), untouched 9 days. Look before deleting.
- **Redundant stacked siblings (REVIEW):** the sema-engine stack
  (engine-decomposition atop record-key-sum / rebuild-from-log /
  single-writer-internal-lock), the spirit VC stack (store-decomposition atop
  vc-followups), the schema-next stack (schema-generics atop typeref-structural-macro
  atop schema-next-polish) — several worktree dirs point into one branch stack;
  prune extra dirs without losing the stacked work.
- **Stale (2-4 wk) REVIEW:** lojix/signal-lojix `horizon-re-engineering`
  (superseded by `horizon-leaner-shape`), the `schema-deep` pair, the
  sema-engine `reusable-versioned-log-spike`.
- **Active KEEP:** the schema-next generics stack, schema-rust-next
  `reaction-frame-emission`, triad-runtime `generic-reaction-frame`, nota-next
  shape branches, sema-engine `engine-decomposition`, spirit `store-decomposition`,
  the design-47 TestVm trio, lojix `horizon-leaner-shape`.

## Corrected mental model (the one-paragraph version)

The schema-as-strict-interface, contract-in-the-signal-repo, per-owner
generate-and-commit, and stable-one-way-dependency properties you described as
goals are **already the built state** — verified, and matching settled intent
(`y88n`, `u7tj`, `0678`, `xbc2`). The "set of actors" is your **target** (`zk6y`),
not the current one-actor synchronous build. The genuinely-open self-host work is
the narrow macro-model duplication in schema-next (the operator slice
`primary-bojw`) plus the `MacroShape`/`MacroOutputKind` no-Rust gap. So: don't
write the "move the schema out of Spirit" bead — it's done; point the epic at the
one real target instead.
