# State of Everything — Synthesis

The fleet is in strong, coherent health. Across ~75 Persona-core crates
(~200k lines of production Rust, ~80k test) the audit found **no
architectural rot**: daemons are real, contracts are clean, NOTA mostly
rides genuine typed codecs, and intent-fit is "aligned" for the large
majority of repos. The work is not *broken* anywhere — it is **mid-
migration**, and almost every issue is one of two shapes: (a) the
consumer fleet is frozen 5–20 commits behind a schema toolchain that
moved decisively this week, and (b) a thin, well-localized layer of
discipline debt (free functions, a handful of hand-rolled NOTA sites,
stale `.concept.schema` cruft).

The single most important fact: **the structural-macro grammar overhaul
is DONE and beautiful on the engine side, and almost entirely UNADOPTED
on the consumer side.** That gap — not any defect — is the dominant
theme of everything below.

## 1. Scale and code volume

| Tier | Repos | Production LOC | Test LOC | Notes |
|---|---:|---:|---:|---|
| Schema/NOTA engine | 4 | ~21.6k | ~19.7k | schema-next, schema-rust-next, nota-next, nota-config |
| Storage + wire foundation | 8 | ~14.8k | ~8.1k | sema, sema-engine, signal*, signal-frame, triad-runtime, version-projection |
| Component daemons + triads | ~50 | ~150k | ~50k | spirit, mind, persona, router, terminal, etc. + signal/meta-signal legs |
| Lojix/CriomOS stack | ~10 | ~15k | ~5k | lojix daemon, horizon-rs, lojix-cli, CriomOS* |
| **Persona core total** | **~75** | **~200k** | **~80k** | excludes vendored `kameo` (23k) and adjacents |

**Production ≠ hand-written.** A large and growing share of the
"production" surface (code that runs if the component is used) is
schema-*emitted*, not hand-authored. Examples: spirit is 9.2k generated
of 13.2k; the upgrade/criome/cloud contract crates are 70–95% generated
(`signal-criome` 3037/3142, `meta-signal-domain-criome` 961/1135,
`meta-signal-cloud` 1217/1465); agent is 1807 generated of 3279. Roughly
**a quarter of the core production LOC is checked-in generated code**.
This is by design and aligned with intent — but it means "how much code"
splits three ways: hand-written logic, generated interface code, and
tests. The generated share is exactly why the contract crates show zero
free functions and zero hand-rolled codecs: they are pure derive
surfaces.

One baseline correction worth noting: `triad-runtime` is ~3148 prod, not
3800 — it is the *only* foundation crate with substantial inline
`#[cfg(test)]` (652 lines). Every other core crate keeps tests in
`tests/` dirs, so production LOC = full `src` tree minus generated.

## 2. The dependency situation — the central story

Foundation crates are tracked by `branch = "main"` in every `Cargo.toml`;
the real pin lives in each consumer's `Cargo.lock`. `flake.lock` **never**
pins foundation crates anywhere in the fleet — it carries only Nix
toolchain inputs (crane/fenix/nixpkgs), and the Nix build defers to
Cargo's git resolution. So there is **no Cargo-vs-flake disagreement** to
chase; `Cargo.lock` is the sole source of truth, and a stale lock is the
only staleness.

The schema toolchain moved this week (schema-next `c8ebb39`,
schema-rust-next `eca4028`, both 2026-06-10). The consumer fleet is
frozen behind it in a tight band:

- **schema-next**: every consumer pins `77e71a4` = **5 behind**.
- **schema-rust-next**: daemons pin `7282446` (**8 behind**), contracts
  `0a845c3` (**9 behind**); cloud/domain-criome are `a35eff7`
  (**20 behind**); the lojix stack is **~43 behind**.

Two consequences follow, and they are the two things most worth the
psyche's attention.

### 2a. The qz6j alias debt is checked-in everywhere — the next regen is BREAKING

The schema-rust-next commits between the fleet's pin and HEAD include
`a259139` (qz6j: drop transparent aliases) and `44e472b` (private-wrapped
newtype fields). Every consumer's checked-in `src/schema/*.rs` therefore
still emits transparent `pub type X = Y` aliases that HEAD no longer
produces — **router 57, message 46, meta-signal-router 28, signal-router
17, signal-message 9**, and so on. The instant any consumer regenerates
against current schema-rust-next, those aliases become **distinct
newtypes** and every former-alias access site breaks. This is the qz6j
fleet-forcing sweep (the work I flagged at the end of report 573): it is
a deliberate, coordinated breaking bump, not a byte-stable refresh, and
it must be sequenced component-by-component by the operator.

### 2b. The nota-next d8862b6 encoding bump — real, bounded, decode-safe

`nota-next` HEAD `d8862b6` carries an encoding change (commit `027e18a`:
render bare-safe strings as bare atoms instead of `[bracket]` form).
schema-rust-next deliberately pins `ae5c25cd`, the rev *just before* the
bump, to isolate it. The audit found **five consumers actually on the
bump**: `spirit`, `criome`, `signal-criome`, `meta-signal-criome`,
`agent`. Their emitted `to_nota` resolves at compile time to *their own*
nota-next pin, so they emit bare atoms where their ae5c25cd-pinned
siblings emit `[brackets]`.

The reassuring part — verified by the engine agent reading the diff:
`027e18a` touched only `format()` (the *emit* path) plus a codec test,
**not the parser**, and `parse_string` already accepts both bare atoms
and bracket strings. So this is **emit-divergence, not a decode break**.
A `d8862b6` producer talking to an `ae5c25cd` consumer decodes fine. The
real exposure is byte-equality: regenerated fixtures and content hashes
will not be byte-identical across the fork. **It must be unified to a
single nota-next pin before any byte-stable wire contract is declared**,
but it is the lowest-severity of the migration risks today. The sharpest
case is the Criome triad, which pairs the post-bump runtime with a
*pre-bump* emitter (schema-rust-next `c0f76c2`).

There is also a quieter skew: schema-next and several contract crates pin
nota-next `f0e435a6` (8 behind), which is 4 commits *older* than the
emitter's `ae5c25cd` — so the schema engine and its emitter sit on
different nota-next revs. Harmless today (both pre-bump), but it should
be unified in the same sweep.

### Recommended pin sweep (one coordinated operation)

Unify the whole fleet on one schema-next / schema-rust-next / nota-next
triple, regenerate, and absorb the qz6j break — per component, operator-
owned. The contract crates (small, fully generated) are the cheapest
first movers; the Criome triad is the most urgent (resolve the pre/post-
bump split-brain); the lojix stack (~43 behind) is the heaviest.

## 3. Schema engine + the grammar overhaul

**Engine: essentially done and well-shaped.** schema-next HEAD builds
clean, 107+ tests green. The AST is genuinely beautiful: `TypeReference`
carries `Bytes` + `FixedBytes(u64)`; `TypeDeclaration` is exactly
`Struct | Enum | Newtype` with the `Alias` variant fully **deleted** (not
disabled); the three reference-parsing paths agree on every new form.
schema-rust-next emits `quote!{Bytes}`, `quote!{FixedBytes<#width>}`, and
the hex codecs as token streams. All four terse forms are implemented and
round-trip-tested:

| Form | Engine | Fleet adoption |
|---|---|---|
| 52ro `(X)` self-tag | DONE | **~0** — old `(X X)` form appears **787 times across 85 files** |
| yp29 `Bytes` / `(Bytes N)` | DONE | 1 partial (signal-frame `(Bytes)`); rest fixtures-only |
| qz6j no-aliases | DONE (Alias deleted) | **~191 bare alias re-tags still checked in** |
| lm84 hash-id (`Digest Bytes`) | DONE | **0** consumer adoption (fixtures only) |

**Consumer schema debt: ~85 of ~102 schema files need migration.** Two
debt classes: 787 old `(X X)` self-tags that collapse to `(X)`, and ~191
bare `Name Synonym` re-tag aliases (`Record Entry`, `Prompt
signal-agent:lib:Prompt`) that post-qz6j are distinct newtypes — the
correctness-affecting sites. Even agent/nexus.schema, the *most*-migrated
consumer, is only half-migrated.

**The `.concept.schema` dialect should be retired wholesale.** There are
~50 `<name>.concept.schema` files vs ~48 live split triad-port files
(`nexus`/`sema`/`signal`/`meta-signal`/`daemon`/`lib.schema`). The
concept files are not merely old-grammar schema-next — they are a
*different, older dialect* (parenthesized single-type newtypes like
`Text (String)`, `Identifier (u64)` — `(u64)` is not even valid
schema-next grammar), `(Status Concept)`-stamped, dated mostly 2026-05-24,
and **read by no build.rs anywhere**. 7 repos carry both a stale concept
file and live split schemas (harness, mind, orchestrate, repository-
ledger, router, system, terminal). The right move is deletion, not
form-by-form migration. (signal-criome and meta-signal-domain-criome
already deleted theirs — the model.)

**One transitional cruft in the emitter:** a residual string-based
`rust_type()` renderer (schema-rust-next/src/lib.rs:5623) builds Rust
type *source* as strings (`format!("FixedBytes<{width}>")`,
`format!("Vec<{}>")`) and duplicates the proper `ToTokens` path
(`TypeRenderer` in migration.rs). It is still wired live into enum-
constructor payload emission via string→`syn::parse` round-trips.
Finishing the quote!/ToTokens migration per ESSENCE means replacing
`rust_type()` at its ~3 call sites with the `TypeRenderer`. It is
already Bytes/FixedBytes-aware, so this is purely string-vs-tokens form,
not missing capability.

## 4. Engine analysis — daemon shapes

The fleet divides cleanly into real daemons, schema-emitted daemons,
contract-only libraries, and scaffolds:

**Real hand-written kameo actor meshes:** persona-spirit (13 actors),
persona (8), router (8), criome (7), harness (6), terminal (3), system
(3), nexus (3), repository-ledger (2), mind (14). These are the genuine
engines — full supervision trees, durable sema-engine storage, honest
typed `Unimplemented` replies for unbuilt paths (no `todo!`/`panic`
stubs anywhere).

**Schema-emitted single-actor daemons:** spirit, orchestrate, message,
agent, cloud, domain-criome ride the schema-rust-next-emitted
`EngineActor` / `ComponentDaemon` spine over triad-runtime, hand-writing
only the component hooks. This is the target architecture.

**The cutover gap, made concrete:** the schema-derived *pilot* (spirit)
has exactly **one** generated actor; the *production* daemon it must
eventually replace (persona-spirit) has **13 hand-written** actors and
zero generated code. Same for mind (14 hand-written) vs the emitted
single-EngineActor pattern. Cutover is not a pin bump — it is
regenerating a 13-actor tree from schema. That is the real distance
between "pilot proves the emitter" and "production runs on it".

**Scaffolds / honest holds:** upgrade has a real ~2.3k-LOC
migration/handover engine behind a *placeholder* daemon
(`daemon_placeholder_response`) — the largest completeness gap in the
fleet. system is a deliberately-paused 60% skeleton (FocusTracker ready,
Niri stream unbuilt by intent). persona-pi is a genuine but 17-day-
dormant concept-only seed (0 code, no INTENT.md — its absence is the
first gap to fill).

## 5. Free functions — 73 flagged, stratified by severity

The method-only rule has real but **localized and mostly low-severity**
debt. Stratification matters:

- **Proc-macro idiom (lowest severity, ~43):** signal-frame/macros (36)
  and signal-derive (7) are token-builder fns over data-bearing model
  types (`ChannelSpec`, `DataStruct`). Violations by the letter; the
  conventional compile-time idiom. Fold onto model methods only when
  tightening.
- **Test-harness bins (~21):** persona's six `wire_*` protocol-test bins.
  Real work outside `#[cfg(test)]`, but in dedicated test tooling, not
  shipped library.
- **Genuine library-proper violations (~25 — the ones worth fixing):**
  concentrated in persona-spirit (the worst single offender:
  `serve_ordinary_stream` at daemon.rs:1469 — a full read/admit/reply/
  write exchange as a loose fn in a file with no test gate), orchestrate
  (12 — several `Display`/`From`/`TryFrom` in disguise:
  `wire_path`, `scope_text`, `civil_date_from_unix_days`,
  `pascal_to_kebab`), upgrade (migration module is free-fn-structured),
  introspect (6), criome (5), terminal (8), signal-frame/src (11 wire
  codec helpers).

**Three recurring single-fix patterns** that would erase a third of the
list at once:
- `synthetic_exchange() -> ExchangeIdentifier` is copy-pasted as a free
  fn in **~6 repos** (mind, router, terminal ×2, terminal-cell, criome,
  introspect). It wants to be one associated fn `ExchangeIdentifier::
  synthetic()` on the type in signal-frame.
- `io_error(impl Display) -> std::io::Error` is duplicated in persona-
  spirit, router, terminal — a `From` impl in disguise.
- `encode_reply`/`encode_nota` (a bare `.to_nota()` wrapper) appears in
  cloud, repository-ledger, upgrade — pointless indirection; inline it.

## 6. Fake-NOTA — small, concentrated, ~6 genuine of 8 flagged

The psyche's specific worry — ad-hoc string-printing of a fake NOTA shape
instead of encoding a real type — is **largely absent**. The fleet
overwhelmingly uses the real `nota-next` codec (`Delimiter::wrap` + child
`.to_nota()`, or `#[derive(NotaEncode)]`). Genuine offenders:

- **signal-persona/origin.rs (the worst):** 3 `NotaEncode` impls
  (`ConnectionClass`, `InternalComponentInstanceOrigin`, `IngressContext`)
  hand-assemble paren-records with `format!("(Tag {})")` — while **13
  sibling types in the same file** use `#[derive(NotaEncode)]`. Delete
  the hand-rolled impls and derive.
- **cloud bins (hard-override breach):** `cloud-daemon.rs:5` and
  `cloud.rs:5` emit `(DaemonRejected "{error}")` / `(CliRejected
  "{error}")` — **literal quotation marks**, which the hard override says
  NOTA structurally cannot emit. domain-criome's sibling bin already does
  it right with `[{error}]`. Fix to bracket form (ideally a typed node
  through the codec).
- **persona-spirit/migration.rs:410:** `format!("(MigrationCompleted
  ({}))")` — sole genuine fake-NOTA in its cluster.
- **signal-system/lib.rs:78:** `SystemTarget::to_nota` hand-wraps
  `format!("(NiriWindow {})")` — a single-variant enum that should derive.

Two flagged sites are **not** the author's fault: introspect's
`surface.rs` hand-wraps reply heads because the `signal_channel!`-
generated reply enum lacks `NotaEncode` — that is a **derive gap to fix
in the emitter**, and it recurs (nexus's renderer buckets ~15
`Reply->String` transforms statically for the same reason). Worth a
deliberate emitter fix: make generated reply enums carry the codec so
consumers never hand-wrap.

The cleanest reference for correct hand-written NOTA is
`signal-version-handover` (derives the record codec, hand-writes only
scalar leaves via `Delimiter::Parenthesis.wrap`).

## 7. Lojix → CriomOS migration

**Daemon ~80% built; stack-level cutover parity LOW.** The shape pivoted
from the documented "horizon-leaner-shape lean stack" to a **triad-port**
that is now `lojix` main (`f9be5df`): lojix is a real ~5k-LOC daemon —
two authority-tiered Unix sockets via triad-runtime, generated Nexus
routing, actor-native async deploy pipeline doing real `nix
eval/build/copy/ssh-switch/gc`, plus a thin CLI. The signal-lojix /
meta-signal-lojix contract ports are landed and clean.

Six blockers stand between here and cutover:
1. **Durable storage unwired** — lojix uses an in-memory `Mutex` Store;
   no sema-engine/redb, no daemon self-resume on restart. A hard blocker
   for an operator-owned deploy ledger (violates the daemon-resume rule).
2. **CriomOS not wired to the daemon** — its HLS flake still takes
   `lojix-cli`, not lojix-daemon or criomos-horizon-config, on *both*
   branches.
3. **No node cut over** — the old zeus/prometheus smoke artifact predates
   the triad-port + actor-async rewrite.
4. **Horizon shape predates the psyche's variants-first cluster-data
   correction** (report 193) — `NodeServices`, `TailnetControllerRole`,
   `ClusterProposal` still carry how-not-what fields. The psyche wants a
   typed-end-to-end pass *before* cutover.
5. **criomos-horizon-config is paper only** — data repo exists, not
   consumed by horizon-rs.
6. **Foundation pins ~43 commits behind** — re-pin must be one
   coordinated regenerate-and-smoke across all three lojix-stack repos.

**Stack A advanced past its own docs:** lojix-cli production pin is now
`fc2ff02` (not the `4c66b8a6` documented in active-repositories.md), and
both lojix-cli and horizon-rs landed their nota-next migration on main.
`protocols/active-repositories.md` has three stale claims (the lojix-cli
pin, the lean-stack shape, the smoke-build claim) that should be
corrected.

## 8. Skills corpus

No contradictions with landed intent — the psyche's worry about "intent
files that sound contradictory now" did not materialize. The issue is
length and overlap, concentrated in a few files:

- **Too long:** `reporting.md` (811 ln — three psyche-report subsections
  say the same thing three ways; absorbs and should fold in
  `report-naming.md`), `designer.md` (582 — ~200 lines of sub-agent
  orchestration restating reporting/feature-development/main-next),
  `component-triad.md` (1123 — genuinely *two* skills: repo-triad and
  runtime-triad; split it).
- **Merge-and-delete:** `report-naming.md` ⊂ `reporting.md`;
  `engine-analysis.md` + `engine-report.md` are one discipline; the
  meta-report-directory pattern is defined in three places
  (context-maintenance, context-maintenance-deep, reporting) and should
  be defined once.
- **The exemplars to imitate:** `beauty.md` (a complete discipline in 83
  lines) and `rust-discipline.md` (an index delegating to 5 focused
  sub-files) are the model for how short a skill can be while carrying
  its weight.

## 9. Prioritized recommendations

1. **Coordinated foundation-pin sweep** (operator, per-component): unify
   schema-next / schema-rust-next / nota-next, regenerate, absorb the
   qz6j alias break. Start with the small fully-generated contract crates;
   make the **Criome triad** urgent (resolve the pre/post-bump split-
   brain); the lojix stack is heaviest. This is the qz6j fleet-forcing
   sweep from report 573, now quantified.
2. **Retire the `.concept.schema` dialect wholesale** (~50 files) — it is
   a dead older grammar, not migratable old-form source. Delete, don't
   port.
3. **Migrate live schemas to the terse grammar** (787 `(X X)` → `(X)`;
   ~191 aliases → direct newtypes) as part of each component's regen.
4. **Fix the emitter derive gap** so generated reply enums carry
   `NotaEncode` — eliminates introspect/nexus hand-wrapping at the source.
5. **Sweep the three recurring free-fn patterns** (`ExchangeIdentifier::
   synthetic`, `io_error`→`From`, `encode_reply` inlining) — one fix each,
   fleet-wide.
6. **Fix the hard-override breach** in cloud's two bins (quotation-mark
   NOTA → bracket form) and derive signal-persona/origin.rs.
7. **Finish the quote!/ToTokens migration** — replace `rust_type()` with
   `TypeRenderer` at its ~3 call sites.
8. **Lojix→CriomOS:** wire sema-engine storage + daemon self-resume, then
   the variants-first horizon pass, then CriomOS flake wiring; correct
   the three doc-drift items in active-repositories.md.
9. **Skills:** merge report-naming→reporting, engine-analysis→engine-
   report, split component-triad; trim reporting.md and designer.md.

None of this is rework of a wrong shape — it is the consumer fleet
catching up to a foundation that got *more* right this week. The shapes
are sound; the lag is the work.
