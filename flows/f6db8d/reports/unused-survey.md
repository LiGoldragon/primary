# Unused survey — what the estate is not using

Read-only survey delegated by main flow f6db8d. Nothing was removed,
disabled, built, or committed. Every daemon observation is passive.

Marking convention: **[W]** witnessed by this flow (I ran the command
or read the file), **[Wd]** witnessed by a delegated read-only subflow
and named as theirs, **[R]** relayed from a prior report without
re-verification.

## 0. What the psyche has already ruled, which narrows the survey

Three rulings were found before the mechanical work was interpreted,
and they overturn the largest apparent finding.

**The old stack is deliberately kept.** `vision-raw/archive-threeStacks.md`
(2026-08-10, dictated) — "I think we should just keep all of the code
that's been written on the incorrect stuff. I think we should just
leave it there and create new repositories for this like shortcut
ethos to rest." Carried forward in `Vision/archive-ethosMonolith.md`:
"the earlier stack's code is kept, left in place, frozen". **[W]**

The dependency graph flags ~57 repositories with no inbound flake or
Cargo edge (§1). Most of them are that frozen stack. Their orphanhood
is the ruling working as intended, not decay. This is the single most
important result of the survey: **repository-level removal is mostly
foreclosed by a standing ruling**, and the real "less code" surface is
inside the live repositories.

**Every component is owed two signal repositories.** `Vision/nexus.md`,
heading Repositories — "A component has three repositories: its main
repository, holding all its code, and two signal repositories — one for
the ordinary socket's contract, one for the meta socket's." **[W]**
So `signal-ethos-zero` / `meta-signal-ethos-zero` having no consumer is
forward scaffolding for a ruled shape, not dead weight. Same for the
`signal-psyche` / `meta-signal-psyche` pair.

**The nexus library is a standing commitment.** `Vision/nexus.md`,
heading Library and daemon — "The nexus repository is the library that
defines the core of a Nexus component." **[W]** See §2.1: the premise
that `nexus` is unused is false, and even the part that is true points
at building it out, not deleting it.

**The old signal repos were ruled archived.** `flows/fe34eb/vision/signal.md`,
2026-09-10 — "just archive the old Signal repo and then rename the
Signal Standard repo to it. We don't need the old Git history." **[W]**
That ruling is already executed (§1.2).

## 1. Repositories nothing depends on and nothing deploys

Method **[W]**: for all 192 directories under `/git/github.com/LiGoldragon/`
I extracted every `github:LiGoldragon/<repo>` and `/git/github.com/LiGoldragon/<repo>`
reference out of every `flake.nix` and every `Cargo.toml` (plus the same
over `/home/li/primary`), dropped self-edges, and subtracted. 57 repositories
have zero inbound edges. I then grepped each orphan's name across the whole
estate to separate "nothing references it at all" from "referenced by prose only".

Two systematic traps, both hit and both corrected:

- `/git/github.com/LiGoldragon/datom` is a **symlink** to `datom-codec`
  (`ls -ld` → `datom -> /git/github.com/LiGoldragon/datom-codec`). **[W]**
  It is not a repository and not a candidate.
- `/home/li/primary/protocols/repos-manifest.dotos` calls itself the
  "authoritative inventory" but is stale: 70 repositories on disk are
  absent from it, including `protos`, `datom-codec` and `ethos-zero`. **[W]**
  Its *absence* proves nothing; only its explicit `(Deprecated …)` entries
  are authoritative. Bead `primary-xqb.8.8` already tracks this.

### 1.1 Not candidates despite zero edges

- **`claude-hijack`, `codex-hijack`** — commissioned by the psyche on
  2026-08-25 and the block walk is recorded as still in progress
  (`flows/4ddc321d/vision/hijackRepositories.md`). **[W]**
- The frozen-stack cluster — `ethos-engine`, `logos-engine`, `logos-runtime`,
  `protos-engine`, `golden-bridge`, `tree-sitter-ethos`, `spirit-ethos`,
  `mind-judge*`, `orchestrator-judge*`, `domain-criome*`, `arca`, `chronos`,
  `lore`, `forge`, `library`, `cloud`, `standards`, and the `signal-*` /
  `meta-signal-*` contracts belonging to them. Covered by §0's freeze. **[W]**
  (`spirit-ethos` alone has a superseding path already tracked as bead
  `primary-xqb.8.12`, "Psyche component supersedes the separate spirit-ethos
  source repository" — that is a migration, not a deletion.)
- **`criomos-horizon-config`** — zero flake edges but pushed to the remote
  today, 2026-09-11T20:29Z. **[W]** Active.
- **`signal-ethos-zero`, `meta-signal-ethos-zero`** — `ethos-zero/Cargo.toml`
  depends on neither; its only git deps are `protos` and `datom-codec`. **[W]**
  Kept under §0's Repositories ruling.

### 1.2 Genuine residue — pure local leftovers, no code loss

| path | size | evidence | last commit |
|---|---|---|---|
| `/git/github.com/LiGoldragon/persona-role-general-code-implementer-reports` | 4.0K | **empty directory**, no `.git` | — |
| `/git/github.com/LiGoldragon/persona-role-SchemaTrainExpansion-reports` | 4.0K | **empty directory**, no `.git` | — |
| `/git/github.com/LiGoldragon/CriomOS-home-spirit-main-f53aacdd` | 5.2M | full clone of `CriomOS-home` at a July commit; HEAD `2888bc09` is contained in `origin/worktree-scaffold-path`; working tree clean; 0 unpushed | 2026-07-19 |
| `/git/github.com/LiGoldragon/signal-legacy` | 6.3M | remote `LiGoldragon/signal-legacy` is **`archived=true`**; the psyche's archive ruling already executed | 2026-09-11 |
| `/git/github.com/LiGoldragon/signal-derive-legacy` | 1.6M | remote **`archived=true`** | 2026-09-11 |

All five verified by me **[W]** (`git worktree list`, `git branch --contains`,
`git status --porcelain`, `gh repo view --json isArchived`). Removing any of
them deletes no unique history: the two `-legacy` clones exist intact and
frozen on the forge, and the stale `CriomOS-home` clone's HEAD is on a
pushed remote branch.

Note on motive: repository deletion reclaims almost nothing. The 57 orphans
total under 200 MB against 118 G in `/git`. The case for removing these five
is surface, not space. The space is in §5.

## 2. Dead crates, binaries, features and modules inside live repositories

### 2.1 Correction — the `nexus` crate is used

The brief names "the unused `nexus` crate". **That premise is false, and I
verified the refutation myself. [W]**

`nexus` is 131 lines exporting three items. All three are consumed:

- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/store.rs:5`
  — `use nexus::{Configurable, ConfigurationState, ConfigurationTransitionError};`
- `/git/github.com/LiGoldragon/lojix/src/lib.rs:40,1104,1156,1173,1188`

The trap that produces the false reading **[Wd]**: `lojix/src/daemon.rs:52`
and `lojix/src/schema_runtime.rs:27` both do
`use crate::runtime_flow::{self as nexus, NexusEngine};`, and
`lojix/src/runtime_flow.rs:417` declares `pub mod nexus`. A bare
`rg 'nexus::'` over lojix returns ~40 hits that are the local alias, not
the crate. A second trap of the same family: `datom-codec/Cargo.toml`
imports its derive crate renamed (`derive = { package = "datom-codec-derive", … }`),
so any dependency audit keyed on the TOML key rather than the `package =`
value manufactures false orphans. About 40 such renamed deps exist.

`runtime-audit.md` §3.3c is right that `nexus` is thin (131 lines, config
lifecycle only) and postdates the runtimes it was meant to found. Set against
`Vision/nexus.md` that is an **under-built commitment**, and the indicated
action is to build it out — not remove it.

### 2.2 Dead input — `primary-generated-src`

Declared `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:219-222`,
`flake = false`, pinned to `primary/fd049d90` (2026-08-22; primary is
1014 commits ahead **[R]**, `dependency-survey.md` §2.3).

Two independent sweeps found **zero consumers in the whole repo** — not
`modules/`, not `packages/`, not `checks/`. **[Wd]** ×2. The comment claims
"used by the harness compatibility check"; the check that used it
(`checks/pi-harness-profile/`) was deleted from live CriomOS-home and
survives only in the stale `CriomOS-home-spirit-main-f53aacdd` snapshot at
`checks/pi-harness-profile/default.nix:47`. The input was left behind. **[Wd]**

Touches: four lines of `flake.nix`, the `flake.lock` entry, and two
transitive lines in `CriomOS/flake.lock`.
Gate: `nix flake check` on CriomOS-home, then re-eval CriomOS.

### 2.3 Dead binaries

**`orchestrate-store-migrate`** —
`/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/bin/orchestrate_store_migrate.rs`,
26 lines, declared at `crates/orchestrate-nexus/Cargo.toml:19`.

Estate-wide the name appears only in its own source, its own `[[bin]]` line,
`orchestrate/README.md` + `UPGRADES.md` prose, and flow narrative. **[Wd]**
The decisive negative I confirmed myself **[W]**: `grep -rn 'store-migrate'`
over `CriomOS-home` and `CriomOS` returns **nothing**, while the check that
pins orchestrate's shipped binary set,
`CriomOS-home/checks/orchestrate-service-path/default.nix:72-77`, asserts
`orchestrate-nexus`, `orchestrate`, `meta-orchestrate` and
`orchestrate-upgrade-preflight` present and two retired names absent.
Its sibling is executed at line 87; store-migrate is named nowhere.
Corroborating: `runtime-audit.md` §4.2 witnessed that it "would fail
against the live store" because its `MigrationSourceInvariant` tables are
provably empty. **[R]**

Important scope limit **[Wd]**: the migration *capability* is not dead.
`PreviousSignalMigratable::migrate_previous_signal`
(`crates/orchestrate-nexus/src/store.rs:407,415`) is exercised by that
crate's own tests at `store.rs:959,1094,1096`. This removes a CLI wrapper.

Touches: the bin file, a 5-line `[[bin]]` block, two doc paragraphs.
Gate: `nix flake check` in orchestrate + `nix build` of the
`orchestrate-service-path` check in CriomOS-home.

**`harness-claude-session-stream-test`** (479 lines) and
**`harness-claude-artifact-observer-test`** (145 lines) —
`/git/github.com/LiGoldragon/harness/src/bin/`, declared
`harness/Cargo.toml:31-37`. **[Wd]** The first has a total estate hit count
of **two files** — its own source and its own declaration. The second has
three, the extra being an inventory listing in
`/home/li/primary/reports/field-readiness/12-run-and-assembly.md:319`,
not an invocation.

I confirmed the gate context myself **[W]**: `harness/flake.nix` exposes
four apps (`harness`, `harness-daemon`, `meta-harness`, `flow-id`) and
carries a large `cargoTest` check suite; neither binary appears in either.
The stream behaviour is already covered by the real check at
`harness/flake.nix:143`, `cargoTest "claude_session_stream"
"claude_session_observation_is_pushed_to_subscriber_without_polling"` —
that supersession is **inferred** by the delegate from the described
behaviour, not from a diff. 624 lines that crane compiles into every
harness package build and nothing ever runs.

Touches: two source files, two `[[bin]]` blocks. Check whether
`ClaudeArtifactObserver` retains other callers before touching the lib side.
Gate: `nix flake check` in harness.

### 2.4 A feature that cannot do anything

**`terminal-cell` / `dotos-text`**, `terminal-cell/Cargo.toml:32`,
declared `dotos-text = []`. **[Wd]** Two independent empties: the crate
contains **no `#[cfg(feature = "dotos-text")]` site at all** — the
declaration is the only occurrence of the string — and neither consumer
(`terminal/Cargo.toml:76`, `mentci/Cargo.toml:29`) enables it. Enabling it
would change nothing. Every other crate carrying that feature name has real
`cfg` sites; this looks like a copied manifest stanza whose implementation
never arrived.

Touches: one line. Gate: `nix flake check` in terminal-cell, `cargo check`
in terminal and mentci.

Two related findings that are **not** removals, recorded so they are not
mistaken for any: `triad-runtime/nota-text` is enabled by its own flake
check but by none of its 21 dependents **[Wd]**; `harness/message-router-e2e`
gates two four-process e2e tests that no flake, CI or script ever turns on
**[Wd]** — the feature is fine, the *gate* is missing.

### 2.5 Nix modules outside the import closure

**[Wd]**, reference counts re-verified by me **[W]**.

`CriomOS-home` — nine files under `modules/home/` are not in the closure of
`homeModules.default`. Of those, seven are removable and two must not be
touched:

- Removable, dead compositor/bar stack superseded by niri + noctalia:
  `modules/home/profiles/min/hyprland.nix` (250), `sway.nix` (62),
  `swayConf.nix` (217), `waybar.nix` (142). Caveat: `hyprland.nix` and
  `swayConf.nix` are read *as text* by
  `checks/keyboard-layout-policy/default.nix:32-33`, which asserts they do
  **not** contain colemak — a check that exists to prove they are stale.
  Removing the files means removing that check arm too.
- Removable, zero references anywhere **[W]**:
  `modules/home/profiles/min/fzfDark.nix` (18), `fzfLight.nix` (18),
  `fzfBase16map.nix` (14). Only `fzfColemak.nix` is reachable. **The
  cleanest removal in the survey** — 50 lines, no check, no reference.
- **Do not remove** `modules/home/profiles/min/pi-models.nix` (326 lines).
  It is a **bug, not cruft**: it declares `home.activation.mergePiModels`
  (`:237`) and is silently not imported, so the pi model-config merge does
  not run on this machine. `modules/home/default.nix:45-53` documents the
  identical failure mode having already happened to `niri.nix` and
  `sfwbar.nix`. The fix is to import it.
- **Do not remove** `modules/home/profiles/med/element.nix` — excluded on
  purpose with the reason inline at `modules/home/default.nix:84-87`.

`CriomOS` — the delegate reported six unimported NixOS modules. **I checked
each against the rest of the estate and two of the three "test" ones are
wrong [W]:**

- `modules/nixos/test-substrate.nix` — **is consumed**, from outside CriomOS:
  `CriomOS-test-cluster/lib/mkDeployTest.nix:160` and `lib/mkVmTest.nix:248`
  both `import "${inputs.criomos}/modules/nixos/test-substrate.nix"`. **Not
  a candidate.** The delegate's grep was scoped to CriomOS only.
- `modules/nixos/criome-node-test.nix`, `criome-auth-integrated-test.nix` —
  only prose references estate-wide. Genuinely unwired, but they are the
  only tests `criome` has, so removing them removes the only proof that a
  packaged component works. **Escalate, do not remove unattended.**
- `modules/nixos/disks/{default,liveiso,pod}.nix` — alternative install
  profiles, only `preinstalled.nix` is imported. Keep.

### 2.6 Dead pub items

**[Wd]**, method: word-matched estate-wide occurrence count of exactly one,
i.e. the definition itself, so no caller exists in production or in the
defining repo's own tests.

Eleven `pub fn`. Five are in lojix and form a group, not scattered cruft —
`src/lib.rs:2196,2449,2477` and `src/schema_runtime.rs:992,2172`
(`set_deployment_immutable_revision`, `record_deployment_phase`,
`append_live_generation`, `test_with_effect_barrier`,
`active_deployment_identifier`). Four of the five sit in the deployment-record
write path: this reads as a half-landed deployment ledger. Read them as a
group before deleting any one. Lojix is excluded from tonight regardless.

Four in `triad-runtime/src/process.rs:160,252,430,451`; two in
`core-logos/src/whole.rs:30,93`.

Eighteen `pub use` re-exports in `triad-runtime/src/lib.rs:27-66` have no
consumer outside the crate — but every one has 5–20 *internal* references.
**These are not deletable types.** The available change is narrowing the
public door, and each must be checked against the signatures that return it
(`RequestPermit` is returned by `RequestPermitPool::acquire`, so callers may
need to name it). Not a tonight item.

One genuine `#[allow(dead_code)]`: `message/src/engine.rs:165`,
`fn error_output`. The other three sites are legitimate (shared test-helper
modules, a generated contract artifact).

**Unused workspace crates: none found.** Every member of every in-scope
workspace is either depended on or is a binary-producing entry point. **[Wd]**

## 3. Daemons enabled but doing nothing

All observations passive, on host `ouranos`, uid 1001, 2026-09-11 ~20:25.
Nothing was started, stopped or reconfigured. **[Wd]**

The delegate was explicit about one discrimination that matters: the `ESTAB`
rows visible for these units are their own journal stdout pipes, not clients.
Those were not counted as traffic.

**Doing real work (4):** `orchestrate-nexus` (its
`orchestrate-nexus.sema` changed mtime twice inside 41 seconds under
observation), `listener` (11 concurrent peers on
`/run/user/1001/listener/status.sock`, 2.7 G of captures), `chroma-daemon`
(writing `state.redb` and `fzf-theme.sh` today), `codex-remote-control`
(live client, traffic through 19:31 today).

**Enabled and inert — the candidates:**

| daemon | socket peers | store | journal, 30 days | CPU / 31 h |
|---|---|---|---|---|
| `agent-daemon` | 0 on both | **contains nothing but its two 0-byte sockets** | **0 lines** | 24 ms |
| `spirit-judge` | 0 | — | **0 lines** | 21 ms |
| `aggregator-daemon` | 0 on both | 24 K; newest archive is `…smoke…2026-07-09T120157Z.rkyv`, a *test* artifact two months old | **0 lines** | 27 ms |
| `spirit-daemon` | 0 on both | `spirit.archive.sema` untouched since 2026-08-03 | 5 lines | 24 ms |
| `message-daemon` | 0 on both | startup write only; prior version is a 2026-07-18 premigration backup | 18 lines, all the startup banner | 20 ms |

`agent-daemon` is the strongest case: its state directory has never had a
data file written to it, and no peer has ever connected. Its repository was
last committed 2026-08-13 **[W]**, as was `aggregator`'s.

`message-daemon` is the weakest despite identical inertness: the `message`
repository was committed **today** **[W]** and `message` 0.11.1 is deployed.
It is being rebuilt, not abandoned.

`spirit-daemon` and `spirit-judge` are excluded by the brief.

Declared-but-off, for completeness **[Wd]**: `mirror.service` is hard-disabled
at `CriomOS/modules/nixos/mirror.nix:30` (`mirrorEnabled = false && mirrorEligible`,
a deliberate kill-switch over a redb crash-loop) — excluded by the brief.
`spirit.service` and `criome.service` are `mkEnableOption` defaults that
nothing outside `checks/` and `*-test.nix` ever sets. `codex-artifact-gateway`
is the one hard-disabled *user* unit, enabled only by its own check — which
is why its `plannotator-capability` input is check-only.

**A broken unit, which is a repair and not a removal [Wd]:**
`agent-intercom-fleet-cleanup.timer` / `.service`, fragment at
`/home/li/.config/systemd/user/` and **not Nix-managed**. It fires every 15
minutes and exits 1 immediately: **329 failures in 7 days**, `MODULE_NOT_FOUND`
on `/home/li/.pi/agent/packages/agent-intercom-orchestrator/src/agent-fleet-cleanup.mjs`
— that directory holds only `pi-mcp-adapter`. Expired Agent Intercom worker
cgroups are therefore not being reaped at all. It is the only failing unit
on the machine.

**Judgment.** Disabling any of these is a running-service change, which the
brief excludes from tonight and which the psyche should rule on. The evidence
supports *asking*, not acting: `agent-daemon` and `aggregator-daemon` are the
two to put to the living first.

## 4. Duplication one shared place could carry

### 4.1 The named lead: `projection.rs` re-derives protos' byte lengths

`datom-codec/src/projection.rs:22-91` (`Measure`/`Measuring`/`Meter`) against
`protos/src/core.rs:643-712` (`CanonicalizingTree::canonicalize_tree`).

I read both myself **[W]**. What is duplicated is *arithmetic, not a constant
table* — datom-codec computes in closed form what protos spends stepwise:

```rust
Form::Variant(head, body) => head.0.len() + 1 + lengths[&body]
Form::Struct(children) | Form::Vector(children) =>
    if children.is_empty() { 2 }
    else { children.map(|c| lengths[&c]).sum() + children.len() + 3 }
```

The `+1` is protos' separator glyph; the `+3` is `{`/`}` plus two inner
spaces. The opaque case is *not* duplicated — `opaque_length` delegates
through `protos::Boundary` **[W]**.

**They agree, and this is now witnessed rather than asserted [Wd]:** the
delegate built a scratch crate that projects a `Datom`, canonicalizes a
clone, and compares **every extent in the tree** — bare, string with `»`,
meaning with unbalanced parens, empty struct, empty vector, variant, nested
mixtures, non-ASCII bare text, and a 100 000-deep chain — under both pinned
protos 0.29.1 and the local 0.30.0. All match. `substrate-audit.md` §2.2 had
this as "agree today (verified by inspection)"; it is now verified by
execution.

**But the formula is already wrong for one arm [Wd]:**

```
Braced: protos=8  formula=8  text="{ ab c }"
Angled: protos=6  formula=8  text="<ab c>"
```

Off by two, because protos omits inner padding for `Angled`. Unreachable
only because `projection.rs:124-127` never emits `Angled` — while
`composition.rs:91` already *reads* it. Same class:
`separator: protos::Separator::Period` hardcoded at `:157` beside a bare
`+ 1`, and `constraints: None` at `:156` with no constraints term at all.

**Owner: protos, which already exports the capability.** `Canonicalizable`
is public and its doc comment states exactly this job. A sibling consumer
already does it right — `ethos-zero/src/protosization.rs:344-356` builds with
`Extent { start: 0, end: 0 }` then calls `canonical.canonicalize()`. **[Wd]**
datom-codec is the outlier.

Touches: delete `Measure`/`Measuring`/`Meter` and the `lengths` threading
(~83 lines of a 202-line file); `Builder::build` stays but stops carrying
offsets; `Projecting::project` becomes build-then-canonicalize;
`OpaqueProjecting::opaque_length` disappears. Nothing outside `projection.rs`
changes.
Gate: promote the differential into `datom-codec/tests/core.rs` — assert
**every** extent equal, not just the root, which is all
`wide_projection_keeps_canonical_extents` (`tests/core.rs:825-845`) checks
today; run over the existing corpus, the proptest alphabet, and at 100 000
deep. Keep `manually_built_hundred_thousand_deep_datom_projects_and_drops_iteratively`
(`tests/core.rs:760`) as the no-recursion guard.

### 4.2 Two live bugs found while looking for duplication

These are not removals. They are the most consequential things the survey
turned up and they should not be buried under it.

**Orchestrate frames little-endian; everything else is big-endian. [Wd]**
`signal/src/frame.rs:1-19` is the crate created to end exactly this, and its
header says so — Orchestrate hand-rolled the prefix, Lojix took
`triad-runtime`'s codec, the two disagreed, big-endian was kept
(`frame.rs:122` `from_be_bytes`, `:140` `to_be_bytes`). **Orchestrate never
migrated**, and is uniformly little-endian in production *and in its own
tests*, so its suite cannot catch it:
`orchestrate/crates/orchestrate-nexus/src/transport.rs:140,161`,
`crates/orchestrate/src/main.rs:164,169`,
`crates/orchestrate-meta/src/main.rs:164,169`, and five test sites.
Any `signal`-based client pointed at an Orchestrate socket reads a
byte-swapped length; a 1-byte body reads as 16 777 216 and trips
`FrameTooLarge`. Invisible only because Orchestrate talks solely to
Orchestrate. `MAXIMUM_SIGNAL_BYTES` is likewise redefined at five sites
(values agree). Owner: `signal`. A cross-crate test that writes with
`signal::frame` and reads with orchestrate's transport fails today.

**The estate is split across three `datom-codec` pins, and two of them
write different text. [Wd]** `f2cc068` 0.25.6 (ethos-zero, signal,
orchestrate); `99a9e8c` 0.25.7 (lojix ×4, signal-lojix, meta-signal-lojix,
horizon-rs); `196d0e2` 0.26.0 — **pinned by nobody**, so the released
substrate fix is unconsumed. The entire source difference between the two
live pins is one line in `impl Datomizable for String`: `| '.' | '!' | ':'`.
Half the estate writes `a:b:c` bare, half writes `«a:b:c»`. The reader
accepts both, so round-trips survive — but any two crates that compare,
hash, or golden-test canonical text disagree, and 0.26.0 changes the rule a
third time. Whoever reunifies should take 0.26.0 and move every pin at once.

Also surfaced **[Wd]**: `/git/github.com/LiGoldragon/protos` has a **dirty,
uncommitted 0.30.0 working tree** (`M Cargo.toml`, `M src/core.rs`,
`M README.md`, untracked `src/traversing.rs`). Pinned 0.29.1 derives `Clone`
recursively and **stack-overflows cloning a 100 000-deep tree**; the
untracked `traversing.rs` is the iterative fix. Real, and unlanded.

### 4.3 Further duplication, ranked by what it costs

- **`extent()` copied verbatim [Wd]** — `protos/src/core.rs:206-216`
  (private `trait Extenting`) and `datom-codec/src/core.rs:99-111`
  (`pub trait ProtosExtenting`), character-identical bodies. protos keeps
  the accessor private, so every consumer must re-open `Protos` by hand.
  Fix: make `Extenting` public and re-export. datom-codec's `at()` stays —
  it encodes datom path semantics.
- **The structural-glyph alphabet is open-coded twice [Wd]** —
  `'{' | '}' | '[' | ']' | '<' | '>' | '«' | '»' | '(' | ')' | ';'` at
  `protos/src/core.rs:368` (reader) and `datom-codec/src/composition.rs:186`
  (writer); separators `'.' | '!' | ':'` at `protos/src/core.rs:377,380,384,410`
  and `composition.rs:175`. They agree; the near-miss at `core.rs:405` is
  deliberate. This is the sharpest ownership case: protos decides which
  glyphs are structural and the writer that must avoid them has no way to
  ask. protos should export `delimits(char)` / `separates(char)`. This is
  the alphabet behind the 0.25.6/0.25.7 reversal in §4.2.
- **Orchestrate's two CLI clients are a 197-line copy-paste [R]** —
  `crates/orchestrate/src/main.rs` vs `crates/orchestrate-meta/src/main.rs`
  differ in six lines. This is the mechanism that doubled the endianness bug.
  `lojix` already solved it correctly by sharing
  `lojix::client::SocketExchange`. Owner: a shared `orchestrate-client` lib.
- **Symlink-escape guard duplicated inside lojix [R]** —
  `clients/meta/src/lib.rs:107-146` and
  `tools/src/lojix-write-configuration.rs:100-145`, line-for-line apart from
  the error type. Security-relevant: a patch to one silently misses the other.
- **`datom_codec::Budget` has no constructor [R]** — the four-field literal is
  written at 8 sites across 4 repos. Within a repo the values agree; across
  repos they are genuine policy. datom-codec should own a named constructor.
- **Byte-identical fixture files [R]** — `lojix/tests/common/mod.rs` ==
  `lojix/tools/tests/common/mod.rs`; orchestrate's two `build.rs` +
  `src/generated/client.rs` pairs.
- **Not duplication, recorded so nobody re-runs it [Wd]** — no hand-rolled
  varint, hex, base32, base64, retry or backoff exists in the thirteen repos
  surveyed; the three XDG-resolution sites encode three intentionally
  different policies; `lojix/src/runtime_model.rs`'s 77 types shadowing
  generated signal types are deliberate layering (nothing asserts the
  alignment, though — only `adapters.rs` failing to compile would catch
  divergence).

## 5. The space, since it was measured

Disk before, witnessed **[W]**: `/` is 916 G, **702 G used, 168 G free, 81%**.

- `/home/li/wt` holds **71 G**, of which **68 G is `target/` directories**
  inside worktrees of finished flows (`542442`, `6329f1`, `01a04e75`,
  `01a05588`, `857335`, `f7941a`). Of ~60 worktrees only **three** are still
  registered in their parent repo's `git worktree list`; the rest have no
  `.git` at all and are plain directories. Largest:
  `lojix/lojix-datom-horizon-542442` 12 G,
  `synchronizer/post-terminus-synchronizer-datom` 6.1 G,
  `chroma/chroma-current-datom-542442` 5.8 G.
- `/git/github.com/LiGoldragon/*/target` totals **94 G**, `lojix/target`
  alone 52 G — but that one is a live cache rebuilt today.

Deleting only the `target/` directories under `/home/li/wt` reclaims ~68 G
and destroys nothing: they are Cargo build output, rebuildable, and the
source beside them is untouched. Their `.jj/repo` files still point back at
the parent repositories' `.jj` stores **[W]**, so worktree *source* deletion
is a separate and later question.

## 6. What was not established

- Whether any of the inert daemons is wanted. Inertness is witnessed;
  intent is not. `lojix-daemon` and `repository-ledger` are also inert this
  boot, but a deployment orchestrator and a ledger idle between events are
  at rest, not broken — and `/var/lib/repository-ledger` was unreadable as
  this user, so its store freshness is unwitnessed. **[Wd]**
- Whether `harness/flake.nix:143`'s check truly supersedes
  `harness-claude-session-stream-test`. The delegate inferred it from
  described behaviour and did not diff the two. **[Wd]**
- Whether any candidate binary is invoked through a runtime-constructed
  string or a systemd unit outside CriomOS/CriomOS-home. No grep can see
  that, and none was attempted. **[Wd]**
- `/etc/horizon.json` was not read (root-only); the node's gates were
  matched against `/tmp/horizon-ouranos.json` and found consistent on every
  testable axis. **[Wd]**
- No build, check or test named as a gate anywhere in this report was run.
  Every gate is proposed, not executed.

## Sources

- `/home/li/primary/SKILL_VARIABLES.md` — estate paths.
- `/home/li/primary/flows/857335/reports/release-registry.json` — released revisions.
- `/home/li/primary/protocols/repos-manifest.dotos` — repository inventory; found stale.
- `/home/li/primary/Vision/nexus.md`, `Vision/signal.md`, `Vision/datom.md`,
  `Vision/archive-ethosMonolith.md`, `vision-raw/archive-threeStacks.md`,
  `flows/fe34eb/vision/nexus.md`, `flows/fe34eb/vision/signal.md`,
  `flows/4ddc321d/vision/hijackRepositories.md` — the rulings in §0.
- `/home/li/primary/flows/f6db8d/reports/runtime-audit.md`, `periphery-audit.md`,
  `dependency-survey.md`, `datom-codec-fix.md`, `protos-fix.md`,
  `substrate-audit.md`, `process-audit.md` — prior claims, extracted with
  provenance by a delegated read.
- `/git/github.com/LiGoldragon/` — 192 directories; flake and Cargo graph,
  `git log`, `git worktree list`, `du`, and `gh repo view --json isArchived`
  run by this flow.
- `/git/github.com/LiGoldragon/CriomOS/flake.nix`, `CriomOS-home/flake.nix`,
  their `flake.lock`s, `modules/` trees and `checks/` — deployed set and
  import closures, read by a delegated subflow.
- Live host `ouranos`: `systemctl`, `systemctl --user`, `ss -lxp`,
  `journalctl --user`, `du`, `df` — passive observation by a delegated subflow.
