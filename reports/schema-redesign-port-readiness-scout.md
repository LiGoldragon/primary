# Schema/NOTA Syntax Redesign — Base-State Scout

Read-only scout, 2026-07-11. Scope: `repos/` only (no `private-repos/` touched).
All findings below are separated into Observed (command output/file content) vs
Interpreted (my reading of what it means). Unknowns are named explicitly.

## 1. Core merge state — nota, schema-language, schema-rust, triad-runtime

**Observed:**
- All four repos' `main` bookmark tip is dated **2026-07-11** (today):
  - nota `f8de7a51` "add NotaOutputForm..."
  - schema-language `59d59aca` "reject duplicate declaration names..."
  - schema-rust `87de872d` "add --pretty readable NOTA output to the CLI"
  - triad-runtime `d323f902` "parse the shared --pretty CLI flag..."
- `jj bookmark list -a` in all four repos shows **no bookmark literally named
  `drop-next`**, locally or `@origin`.
- No `.git/refs/remotes/origin/drop-next` and no `drop-next` line in
  schema-rust's `packed-refs` (triad-runtime has no `packed-refs` file at all —
  refs are loose).
- `nota` main (`::main`) contains, as ancestors: `7dc0ab7e nota: remove
  retired structural pipe forms from grammar, parser, and codec`, `cf107deb
  nota: retire structural pipe forms from target grammar...`, `ce7c564d nota:
  remove next-family residue`. No commit or bookmark in the nota repo
  mentions "drop-next" anywhere in its full history.
- `schema-language` main (`::main`) contains: `13136d78 retire relations,
  streams, and families...`, `d452d549 retire relations, streams, and
  families from source, semantic model, substrate, identity, and view`,
  `4ead820c record six-block grammar rulings — no aliases, dotted imports,
  nested-namespace retirement`, `49edaab0 flip the general schema document to
  six per-kind blocks`, `c61fe157 dotted raw/reflection maps...`, `dc519502
  schema-language: repin nota to structural-pipe removal and drop pipe-form
  stragglers`, `6cfff304 reconcile ARCHITECTURE current-state to the landed
  six-block grammar`.
- `schema-rust` main contains `1821005f schema-rust: land the final
  six-block schema-language surface`, `7842acd7 migrate ARCHITECTURE and
  README to the dotted six-block schema surface`.
- `schema-language/ARCHITECTURE.md` (current, on main) explicitly documents
  the dotted-everywhere change: "import path colons become dots:
  `signal-spirit.signal.Entry` is a..." (line 242) and describes the
  six-block, no-alias, dotted-import grammar as landed.
- **Not yet merged to main**: two small unmerged branches exist —
  `schema-dotted-syntax-generic-builtin-slice` on schema-language
  (2 commits: "add positional generic definitions",
  "finish dotted generic source slice") and
  `schema-rust-generic-builtin-slice` on schema-rust (2 commits: "consume
  schema generic definitions", "consume dotted generic builtins"). Verified
  by `jj log -r '<branch> & ::main'` returning empty for both.
- Grepping **all 160+ repos** under `repos/` for `description(glob:"*drop-next*")`
  shows the string "drop-next" is heavily used as a **branch-name convention**
  in *downstream/component* repos (criome, CriomOS, CriomOS-home, orchestrate,
  router, signal-router, signal-spirit, meta-signal-router, skills, etc.),
  with commit messages like "integrate drop-next with current main",
  "integrate main into drop-next for landing", followed later by
  `rename-propagator: drop -next from family identity (nota-next->nota,
  schema-next->schema, schema-rust-next->schema-rust)` commits. No
  directory named `nota-next`, `schema-next`, or `schema-rust-next` exists
  on disk under `repos/` today.

**Interpretation:**
- The psyche's framing ("the drop-next branch was merged into main") maps
  onto the *component/downstream repos'* migration mechanics, not the core
  four repos. In the core repos, there was apparently no literal `drop-next`
  branch — those repos (nota, schema-language, schema-rust, triad-runtime)
  appear to have gone through a `-next`-suffixed identity themselves at some
  earlier point (`nota-next`, `schema-rust-next`) that was renamed onto
  `main` directly (the `rename-propagator` commits target *dependents*, not
  these repos' own histories — nota's own log never mentions "-next" at all).
  Given the redesign markers (pipe removal, families retirement, six-block,
  dotted imports) are present as ordinary linear ancestors of `main` in all
  four core repos, and dated today, **the full syntax-redesign work is
  observably on `main` for all four core repos**.
- The absence of any `drop-next` git ref anywhere in the core repos, combined
  with the presence of `rename-propagator: drop -next from family identity`
  commits in ~100+ downstream repos, is consistent with: downstream repos
  used a local `drop-next` bookmark/branch to track the still-in-flight
  redesign generation (pinning `nota-next`/`schema-rust-next`), merged it into
  their own `main`, then renamed their dependency package identities away
  from the `-next` suffix once the core repos completed their own rename.
  The branch was then deleted (consistent with no live ref surviving).
- The two unmerged generic-builtin-slice branches are small, additive,
  independent features (positional/dotted generic definitions) layered on
  top of an already-landed six-block/dotted base — they read as forward work,
  not unlanded redesign debris.

**Unknowns:**
- Whether a `drop-next` bookmark ever existed *inside* nota/schema-language/
  schema-rust/triad-runtime themselves and was simply deleted with no message
  trace (jj bookmark deletion doesn't necessarily leave a description). I did
  not inspect `jj op log` (op-log archaeology) in these four repos, which
  could confirm/deny this with certainty — flagged as not checked.
- Whether `schema-dotted-syntax-generic-builtin-slice` /
  `schema-rust-generic-builtin-slice` are still wanted, abandoned, or waiting
  on the same producer/consumer ordering as other component work.

## 2. Component pin map

**Observed** (`grep` of each repo's `Cargo.toml` for `nota`/`schema-language`/
`schema-rust`/`triad-runtime` dependency lines):

| Repo | nota | schema-language | schema-rust | triad-runtime |
|---|---|---|---|---|
| spirit | `branch = main` | `rev = 6aae825d668e3f607a2754afa6b7d94e9f246c41` | `rev = f3b4563163dd11ba1cbbcca8081701ab7830b8f5` | `branch = main` |
| message | `branch = main` | — | `branch = main` | `branch = main` |
| mind | `branch = main` | — | `branch = main` | `branch = main` |
| router | `branch = main` | — | `rev = 255823ab3d0d6c5cab26e26a8b1d60c63c52c7b4` | `branch = main` |
| orchestrate | `branch = main` | — | `rev = 255823ab3d0d6c5cab26e26a8b1d60c63c52c7b4` | `branch = main` |
| harness | `branch = main` | — | `branch = main` | `branch = main` |
| introspect | `branch = main` | — | **`branch = drop-next`** | **`branch = drop-next`** |
| system | `branch = main` | — | **`branch = drop-next`** | **`branch = drop-next`** |
| persona | `branch = main` | — | **`branch = drop-next`** | **`branch = drop-next`** |
| listener | `branch = main` (optional) | — | — | — |
| nexus-cli | — (thiserror only) | — | — | — |
| nexus | — (thiserror/tokio/kameo/signal) | — | — | — |

(`—` = no direct dependency line found; several of these repos depend on
schema-language/schema-rust only transitively through `schema-rust`'s own
dependency graph, which I did not fully expand.)

- `introspect`, `system`, and `persona` all pin `schema-rust` and
  `triad-runtime` to `branch = "drop-next"`. As established in §1, no
  `drop-next` ref currently exists in either the `schema-rust` or
  `triad-runtime` remotes on disk. **These are stale/broken pins** — a
  `cargo update`/fresh clone against `branch = "drop-next"` would fail to
  resolve unless an existing `Cargo.lock` still has a cached resolution.
- `spirit`'s `schema-language` pin (`rev = 6aae825d`) is a **pinned commit**,
  dated 2026-07-07 in schema-language's own history, and confirmed (via
  `jj log -r '6aae825d & ::dc5195022869'` returning non-empty) to be an
  **ancestor of** `dc519502 schema-language: repin nota to structural-pipe
  removal and drop pipe-form stragglers` — i.e. `6aae825d` **predates**
  schema-language's own adaptation to nota's pipe removal. Because
  `6aae825d`'s own `Cargo.toml` pins `nota = { branch = "main" }` (floating),
  rebuilding schema-language at that old rev today pulls current nota `main`
  (which has already dropped `PipeParenthesis`/`AtomClassification`), while
  schema-language's *code* at `6aae825d` still references those removed nota
  APIs. This is the exact mechanism behind the reported `E0432
  nota::AtomClassification` / `E0599 Delimiter::PipeParenthesis` build
  failures on spirit.
- `orchestrate`'s `Cargo.toml` is newer than its `Cargo.lock` on disk
  (mtime comparison), suggesting an unresolved/uncommitted dependency edit
  relative to the lockfile — worth a fresh `cargo generate-lockfile` check
  before treating orchestrate's current lock as authoritative.
- `nexus-cli` and `nexus` have **no dependency at all** on nota / schema-
  language / schema-rust / triad-runtime, so they are structurally unaffected
  by the redesign (see §4).

**Interpretation / porting order implied by pins:**
- Group A (already floating on `main` for all three schema-stack crates:
  message, mind, harness) — likely already tracking the redesign; still needs
  an actual `cargo build`/`cargo check` to confirm, not just pin inspection.
- Group B (`router`, `orchestrate` — schema-rust pinned to a specific rev
  `255823ab`) — needs checking whether `255823ab` postdates schema-rust's
  `1821005f land the final six-block schema-language surface` commit; not
  yet checked (unknown, flagged below).
- Group C (`introspect`, `system`, `persona` — pinned to the now-nonexistent
  `drop-next` branch) — blocked purely on **repinning to `main`** (or a
  fresh pinned rev); mechanically the simplest fix of the three groups, but
  needs verification since these were pinning `drop-next` specifically
  (possibly because `main` lagged `drop-next` at the time) — repinning to
  `main` should now carry everything `drop-next` had, per §1's finding that
  `drop-next` work is merged, but this is an inference, not confirmed by a
  diff.
- Group D (`spirit` — pinned to specific, stale revs on both schema-language
  and schema-rust) — the deepest port, discussed in §3.
- `nexus-cli`/`nexus` — no porting needed for the schema stack; unaffected.

**Unknowns:**
- Whether `router`/`orchestrate`'s pinned `schema-rust` rev `255823ab`
  predates or postdates the six-block landing — not checked.
- I did not run `cargo check`/`cargo build` anywhere (out of scope for a
  read-only, no-long-build scout per the brief) — every "resolves and
  builds" claim above is an inference from git ancestry and pin syntax, not
  a compiler-verified fact, except where I explicitly traced ancestor/
  descendant relationships via `jj log`.
- Did not enumerate `mentci`, `mentci-lib`, `mentci-egui`,
  `terminal`, `signal-*` wrapper crates, or `agent`/`aggregator` — the brief's
  named list was covered; the wider signal-stack was not exhaustively swept.

## 3. Spirit and "families"

**Observed:**
- `grep -rn "families\|Family"` across `spirit/src` returns **152 matches
  across 7 files**: `guardian_journal.rs`, `store/mod.rs` (2051 lines),
  `store/family_directory.rs` (71 lines), `shipper.rs`, `store/archive.rs`,
  `schema/sema.rs` (1781 lines, generated), `production_migration.rs`.
- `spirit/src/store/family_directory.rs` defines `StoreFamilyDirectory`
  implementing `sema_engine::FamilyDirectory` (trait defined at
  `sema-engine/src/fold.rs:347`), dispatching on `SchemaHash` per record
  family (`RECORDS_FAMILY`, `REFERENTS_FAMILY`, `MIGRATIONS_FAMILY` from a
  generated `family_identity` module) to route rows into typed tables
  (`entries`, `referents`, `migrations`).
- `spirit`'s `Cargo.toml` pins `sema-engine = { branch = "main" }` — floating,
  not stale. `sema-engine`'s own `main` history (recent, on `::main`) shows:
  `817236a7 add identified record families`, `53426b14 typed family identity
  in versioned log; storage kernel goes read-only; bump 0.3.0`, `22a08859
  settle storage-declaration surface on the sema.schema document kind`,
  `fa3a822f note pending successor stored-record identity basis` (latest).
- `spirit/schema/sema.schema` (the actual `.schema` source, 65 lines) uses
  **colon-separated cross-file references** throughout, e.g.
  `Entry signal-spirit:signal:Entry`, `Query signal-spirit:signal:Query`,
  `DomainScopes signal-domain:domain:DomainScopes` — no dotted paths anywhere
  in the file. The word "family"/"families" does **not** literally appear in
  `sema.schema`'s text.
- `schema-language/ARCHITECTURE.md:242` gives, as its own worked example,
  exactly this transformation: "import path colons become dots:
  `signal-spirit.signal.Entry` is a...". This is the literal spirit path.
- `spirit/schema/` contains an active-looking Emacs lock symlink
  `.#sema.schema -> li@ouranos.1797515:1783029461` and an autosave
  `#sema.schema#` (mtime `Jul 10 19:05`, one day before this scout), but a
  `diff` against the committed `sema.schema` shows only a single trivial
  leading `+` character difference — not a substantive in-progress edit.

**Interpretation:**
- There are **two distinct "families" concepts** in play, and they should
  not be conflated:
  1. The schema-language *document-kind* construct named `families` (along
     with `relations`/`streams`) that was **retired** on schema-language
     `main` (`d452d549`, `13136d78`) and is being succeeded by the "sema
     document-kind" design (`schema-language: record sema storage-declaration
     document kind`, `5d10d42e`).
  2. sema-engine's own runtime **`FamilyDirectory` trait / record-family**
     abstraction (storage-table dispatch by schema hash), which is **not**
     retired — it is actively developed on sema-engine `main` right now
     (most recent commit is about a "pending successor stored-record
     identity basis", i.e. mid-transition, not gone).
- Spirit's 152 "family" hits are almost entirely usage of concept (2), the
  still-live sema-engine storage abstraction, via a fully generated
  `schema/sema.rs` and a small hand-written `family_directory.rs` glue file.
  This usage is not, by itself, blocked on the schema-language `families`
  retirement.
- What **is** concretely gated on the schema-redesign is much narrower and
  mechanical: `spirit/schema/sema.schema`'s colon-path cross-file references
  need conversion to dotted paths (a direct, already-documented, one-for-one
  text transformation per schema-language's own ARCHITECTURE.md example),
  plus repinning `schema-language` off the stale `6aae825d` rev and
  `schema-rust` off its stale rev, then regenerating `schema/sema.rs` and
  `schema/nexus.schema`-derived code against the new toolchain.
- Whether this is a "stopgap-feasible port" or "genuinely gated on the sema
  document-kind successor design" is **not fully resolved by this scout**:
  the colon→dot text change looks mechanical and small, but I did not
  determine whether `sema-engine`'s in-flight "settle storage-declaration
  surface on the sema.schema document kind" work changes the *shape* spirit's
  `sema.schema` needs to take (i.e., whether the storage-declaration parts of
  spirit's schema need a document-kind rewrite, not just a dotted-path
  rename). That determination requires reading sema-engine's actual current
  document-kind design/commit content, which I did not do (out of the
  originally scoped four core repos + component pin map).

**Unknowns:**
- Whether `spirit`'s 152 family-hits include any usage of the *retired*
  schema-language families construct specifically (as opposed to
  sema-engine's still-live one) — I did not line-by-line classify all 152
  hits, only characterized the load-bearing files.
- Exact shape of the "pending sema document-kind design" and whether it
  requires a spirit schema rewrite beyond path-dotting — not read.
- Who/what is running `li@ouranos` Emacs on `spirit/schema/sema.schema`
  currently or as of yesterday, and whether that's relevant in-progress
  human work — flagged, not investigated further (out of scout scope; this
  is the psyche's own editing session, and the diff is trivial so it's not a
  blocker either way).

## 4. nexus-cli

> **Erratum — 2026-07-11.** Superseding this section's verdict: per a
> later psyche ruling, both `repos/nexus` and `repos/nexus-cli` were
> verified **agent-fabricated** and **deleted** on 2026-07-11. "Nexus"
> was only ever the psyche's concept name for a daemon's
> internal-operation IO types (the Signal/Nexus/SEMA plane triad), never
> a standalone daemon or executable. The scout's "nexus-cli exists as
> described, is not vaporware" conclusion below is therefore obsolete —
> a real repo on disk with plausible history is not the same as a
> psyche-sanctioned component. The section body is left intact as a
> historical record of what was on disk before the deletion; do not use
> it to plan a port.

**Observed:**
- `repos/nexus-cli` exists as a real, committed repo (`.git`, `.jj`, `.beads`
  all present) with substantive history: 24 commits from
  `2026-04-23` (`bd init`) through `2026-07-07` (latest, "docs: keep AGENTS
  guidance repo-local"). All commits are authored/committed as user `li`
  (per this workspace's global git-user convention — **not** a reliable
  signal of human vs. agent authorship; AGENTS.md states "Git user: li" is
  the fixed identity for all agents in this workspace, so authorship alone
  cannot distinguish who wrote it).
- `Cargo.toml`: `name = "nexus-cli"`, one binary `nexus` (`src/main.rs`), one
  lib `nexus_cli` (`src/lib.rs`), **dependencies: `thiserror = "2"` only**.
  Confirmed no clap, no nota, no schema-* dependency.
- `src/main.rs`: reads a file argument or stdin, connects to a Unix socket
  (`$NEXUS_SOCKET` or `/tmp/nexus.sock` default), writes the bytes via
  `Client::shuttle(&input)`, writes the raw reply bytes to stdout. No
  parsing of the reply — it is written back as raw text.
- `src/lib.rs`/`ARCHITECTURE.md`: describes itself explicitly as "the
  simplest possible shape of a text-in-text-out shuttle" / "reference
  client" — stateless, one connection per invocation, no protocol
  versioning on this leg. ARCHITECTURE.md's own "Status" section says "M0
  working. Shuttle implemented and verified end-to-end via
  mentci-integration through both `criome-daemon` and `nexus-daemon`" (per a
  2026-04-27 commit's smoke-test log recorded in the commit message).
- Confirmed by `grep -rl "nexus-cli\|nexus_cli"` across all of `repos/*/Cargo.toml`:
  **no other repo declares a dependency on nexus-cli**, and no
  `Command::new("nexus")`/shell invocation of the `nexus` binary was found
  outside `nexus-cli`/`nexus` themselves.
- Separately, `repos/nexus` (a *different* repo) exists and builds a
  `nexus-daemon` binary (`kameo`+`tokio`+`signal` deps) — the actual daemon
  nexus-cli's `Client` talks to over `/tmp/nexus.sock`.

**Interpretation:**
- The prior worker's description is accurate on every checkable point: real
  repo, `thiserror`-only deps, raw-NOTA-text shuttle (not parsed/rendered by
  the CLI itself), bespoke single-positional-arg parsing (no clap), and
  "shuttle relay" is a fair paraphrase of the CLI's own self-description.
- The psyche's skepticism ("nexus is an abstraction, not an executable... is
  there even a nexus-cli?") does not hold up against what's on disk: this is
  a real, historied, buildable (per its own commit-log smoke test),
  documented CLI binary named `nexus`, distinct from the `nexus` *library/
  vocabulary* repo and the `nexus-daemon` binary in the `nexus` repo. I am
  stating this plainly per the brief's instruction not to soften: **nexus-cli
  exists as described, is not vaporware, and its ARCHITECTURE.md claims it
  was verified working as of 2026-04-27.**
- However, **nothing in `repos/` currently consumes/invokes it** — no other
  repo shells out to the `nexus` binary or depends on `nexus-cli` as a
  library. Its only proven caller is its own historical commit-message smoke
  test. Whether it's exercised today (by a human directly, a script outside
  `repos/`, or not at all since April) is not established by this scout.

**Unknowns:**
- Whether anything outside `repos/` (e.g. a private script, a shell alias,
  `private-repos/`, or agent-harness tooling) invokes the `nexus` binary —
  out of this scout's authorized scope to check `private-repos/` beyond
  noting it exists (only `social-media` is present there per `ls`, unrelated).
- Whether nexus-cli/nexus-daemon still actually build and interoperate today
  (I did not run a build) — only the historical commit-log claim was
  checked, not re-verified.

## 5. listener

**Observed:**
- `repos/listener`, `Cargo.toml` `name = "listener"` version `0.9.0`.
  Binaries: `listener` (main CLI, `required-features = ["nota-text"]`),
  `listener-daemon`, `listener-recall`,
  `listener-transcription-customization`, `meta-listener`
  (`required-features = ["nota-text"]`). Depends on `nota` (optional, gated
  by the `nota-text` feature), `signal-frame`, `signal-listener`,
  `meta-signal-listener` (all `branch = "main"`).
- `src/main.rs` → `CommandLine::run()` (`src/command.rs`): builds a typed
  `ListenerCommand`/`Input`, sends it via `ListenerClient::call()` over a
  Unix socket using `ContractFrameCodec`, gets back a `signal_listener::
  Output`, and prints it via `writeln!(output, "{reply}")` — a plain Display
  format specifier.
- Traced `Output`'s `Display` impl to `signal-listener/src/schema/lib.rs:1484`
  (a generated file): `impl std::fmt::Display for Output { fn fmt(...) {
  formatter.write_str(&<Self as NotaEncode>::to_nota(self)) } }`, gated
  `#[cfg(feature = "nota-text")]`.
- **Answer: the printed reply is a genuine NOTA document** (via
  `NotaEncode::to_nota`), not ad hoc/Debug-style plain text — but only when
  the `nota-text` feature is enabled (which is `listener`'s default feature
  set, and is required by the `listener` binary's `required-features`).
- `src/meta.rs` (backing `meta-listener` binary via
  `src/bin/meta_listener.rs`): a 35-line file. `MetaCommandLine::run()`
  writes a fixed string `"meta-listener CLI scaffold: meta-signal-listener
  transport is not implemented"` and then unconditionally returns
  `Err(Error::NotImplemented { surface: "meta-listener CLI" })`. There is no
  branching logic, no partial implementation — every invocation always
  prints that message and fails.

**Interpretation:**
- The report that `meta.rs` is "an unimplemented scaffold" is confirmed
  precisely: it's a hard-coded stub that always errors, not a
  partially-working feature.
- The listener CLI proper (`listener` binary, not `meta-listener`) is a
  real, functioning NOTA client — its printed output round-trips through
  the same `nota`/schema-generated (`signal-listener`) machinery as the rest
  of the signal stack, and depends on `nota` at `branch = "main"` (floating,
  current).

**Unknowns:**
- Whether `listener` actually builds today against current `nota`/
  `signal-listener` main (not verified by build — pin inspection only, and
  `signal-listener`'s own generated `schema/lib.rs` derives were read but
  its own dependency pins on nota/schema-rust were not traced).

## Summary for the requesting agent

1. **Merge-state verdict**: The full syntax redesign (dotted-prefix imports,
   six-block schema-document shape, structural-pipe removal, families
   retirement) is on `main` for all four core repos (nota, schema-language,
   schema-rust, triad-runtime), each dated today (2026-07-11). There is no
   literal `drop-next` branch/bookmark surviving in any of the four core
   repos or their remotes — the "drop-next merged into main" framing applies
   to the ~100+ *downstream* repos, which used `drop-next` as their staging
   branch for the migration and later renamed their dependency identities
   away from the `-next` suffix. Two small, additive, unmerged branches
   remain (`schema-dotted-syntax-generic-builtin-slice` on schema-language,
   `schema-rust-generic-builtin-slice` on schema-rust) — forward feature
   work, not redesign debris.

2. **Proposed porting order / blocking dependencies**:
   - First, repin `introspect`, `system`, `persona` off the now-nonexistent
     `drop-next` branch pin for `schema-rust`/`triad-runtime` onto `main` —
     mechanically the cheapest fix, though unverified by an actual build.
   - Second, verify `router`/`orchestrate`'s pinned `schema-rust` rev
     `255823ab` against the six-block landing point (unchecked ancestry);
     likely a repin-only fix too.
   - Third, and most involved: `spirit` — repin `schema-language` off stale
     `6aae825d` (confirmed to predate schema-language's own pipe-removal
     repin) and `schema-rust` off its stale rev, convert `spirit/schema/
     sema.schema`'s colon-separated import paths to dotted paths (a
     documented, one-for-one schema-language transformation), then
     regenerate `spirit/src/schema/sema.rs`. This does **not** appear gated
     on sema-engine's in-flight "families" successor work by itself — that
     work affects a separate, still-live sema-engine runtime abstraction
     (`FamilyDirectory`) that spirit already depends on via `branch =
     "main"` — but I could not fully rule out that sema-engine's active
     "document-kind" transition changes the *shape* spirit's schema needs,
     so this should be revisited once sema-engine's document-kind design is
     read directly.
   - `message`, `mind`, `harness`, `listener` are already floating on `main`
     for all relevant crates and read as the least-blocked group, but this
     was not build-verified.
   - `nexus-cli`/`nexus` need no porting — no dependency on the redesigned
     crates at all.

3. **nexus-cli verdict**: It exists, plainly. Real repo, real history back to
   April 2026, deps limited to `thiserror`, bespoke argv parsing, raw
   NOTA-text shuttle over a Unix socket, self-described and historically
   smoke-tested as a working "reference client" for the `nexus-daemon`
   (in the separate `nexus` repo). Nothing in `repos/` currently invokes it,
   though — its only proven caller is its own historical commit-message
   smoke test.

4. **Spirit/families verdict**: Two different "families" exist. The retired
   one is schema-language's document-kind construct (gone from `main`,
   replaced by the pending sema document-kind design). The live one is
   sema-engine's `FamilyDirectory`/record-family storage abstraction, which
   spirit uses extensively (152 hits, 7 files) and which is **not** retired
   — spirit pins `sema-engine` at `branch = "main"`, currently mid-transition
   itself. What's concretely blocking a spirit port is narrower and looks
   mechanical: stale schema-language/schema-rust pins plus a colon→dot path
   rewrite in `spirit/schema/sema.schema`. Whether that's a safe stopgap or
   secretly requires the sema document-kind successor is not fully resolved
   here — flagged as the one open question worth a direct read of
   sema-engine's document-kind work before committing to a spirit port plan.

Report path: `/home/li/primary/reports/schema-redesign-port-readiness-scout.md`
