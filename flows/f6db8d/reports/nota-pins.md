# `nota` — what it was, what replaced it, and what each consumer could reach

Subflow of main flow f6db8d. Task: establish what the package `nota` was
and what replaced it; then, per consumer (aggregator, listener, harness,
router, repository-ledger), either move to the replacement at an
immutable rev or pin `nota` to its last defining revision; convert every
other mutable `branch = "main"` git dependency in those five manifests to
`rev =`; bump harness properly for the breaking wire change in 722b68b3;
gate and land.

Everything below is witnessed by this flow on this host on 2026-09-11
unless marked relayed.

## What `nota` was

`nota` was the hand-authored structural reader and codec at the recursion
floor of the schema-derived stack — the crate that recognized delimiters,
spans, atoms and block structure before any schema could load, and that
owned the text value shapes (`NotaEncode` / `NotaDecode` / `NotaSource`)
for every Signal contract's text projection.

It lived in **one** GitHub repository that has been renamed twice. The
three URLs the estate pins — `nota.git`, `nota-next.git` and `dotos.git`
— all resolve to the same repository: `git ls-remote` on each returns the
identical HEAD (`d97dd5c17688a49ed41b12d3c20ef51fe3c692ae` at the time of
this flow). Cargo, however, treats each URL as a distinct source, which
is why one dependency graph could hold `nota 0.5.1` from `nota.git` and
`nota 0.8.0` from `nota-next.git` at once (harness's committed lockfile
does exactly that).

## What replaced it

**`dotos`, in the same repository, at commit
`1facca44fbcb37633f71fcf6f73bd693fbe56a5e`** — "dotos: rename the NOTA
language and API surface", 2026-07-31. The rename is total and purely
lexical at the API surface: `nota` → `dotos`, `Nota` → `Dotos`, `NOTA` →
`DOTOS`. `NotaEncode::to_nota` became `DotosEncode::to_dotos`,
`NotaDecodeError` became `DotosDecodeError`, `nota_derive` became
`dotos_derive`, and the crate's own `name` moved from `nota 0.9.0` to
`dotos 0.10.0`. The optional-feature name on every contract crate moved
with it: `nota-text` → `dotos-text`. The sibling query crate was renamed
in the same pass: `nota-text-query.git` → `dotos-text-query.git`
(`acf6b4b935443602f0bf575adfb22e974c5dde53`, same day).

**The last revision that still defined the package `nota` is
`89dc3c85a9ff96d4e4d53accfd867df672cae5a8`** ("nota: remove the retired
MacroRegistry/MacroNodeDefinition dispatch pair", 2026-07-17), the parent
of the rename.

The estate's already-migrated crates converged on **`dotos` at
`80c7b17f7ad3cf547d2624c6a243e5de5f85c9f3`**, not at the repository's
head: signal-frame (at the revision its consumers pin), signal-harness,
meta-signal-harness, signal-router, meta-signal-router, signal-mind,
triad-runtime and message all pin that exact revision. Grammar changed
again after it (curly strings and bare angle applications at `2db2eb9`,
bare atom map keys at `b3c2c76`), so head is not interchangeable with
`80c7b17`. This flow used `80c7b17` wherever it introduced a `dotos` pin.

### Psyche

`Vision/`, `vision-raw/`, `Intent/` and `flows/*/vision/` were searched
for `nota` and `dotos`. The corpus carries the language's design (three
stacks, structured string type, `Intent/protosParsing.md`,
`Vision/sources/datom.md`) but **no entry rules on the rename itself and
none names any of the five consumers as frozen or deprecated**. The
brief's fallback condition ("Vision says the consumer is frozen or
deprecated") is therefore not met for any of them; where a consumer could
not be moved, this report says so as a mechanical finding, not as a
licence to freeze.

## The condition that actually blocks the estate

Pinning a consumer's own dependencies does not stop its producers'
dependencies from floating. Every `branch = "main"` pin inside a producer
now resolves to a post-rename head, and Cargo offers no way to correct
that from the consumer: `[patch]` refuses to redirect a git source to a
different revision of the same source ("patch for `X` points to the same
source, but patches must point to different sources"), and Cargo
canonicalizes `…/foo` and `…/foo.git` to one source, so the URL-spelling
trick does not buy an override either. This flow tried both, on harness,
and was refused. A consumer is therefore reachable only when **every**
producer in its graph has already crossed to `dotos`.

Two further walls sit behind that one:

1. **The Nexus daemon emitter is gone from `schema-rust`'s main.**
   harness's and repository-ledger's `build.rs` import
   `schema_rust::{NexusDaemonShape, WorkingListenerTier, MetaListenerTier,
   SocketModeBits, build::{GenerationDriver, GenerationPlan,
   ModuleEmission}}`. No revision on `schema-rust`'s main exports those
   (they were removed on 2026-08-06); the revisions that still do
   (`f3b45631` and earlier, and every side branch carrying them:
   `lojix-release-schema-rust-immutable`,
   `lojix-canonical-nota-pin-schema-rust`, `train/unified-green-owner-fix`,
   `record-family-emission`, …) all pin `nota` at `branch = "main"` and
   are themselves unresolvable. Nine repositories are in this position —
   terminal, introspect, harness, mind, system, terminal-cell, spirit,
   repository-ledger, persona. The same holds for the contract-crate
   emitter (`ContractCrateBuild`, `CargoSchemaMetadata`,
   `DependencySchema`) that signal-listener and meta-signal-listener
   build against.
2. **signal-mind has not crossed the signal-persona generation.**
   signal-mind's head pins signal-persona `51ee97b1` (0.2.1); every
   dotos-era signal-harness pins `0baf90c8` (0.3.1); signal-persona
   declares `links = "signal-persona"`, so Cargo admits only one copy.
   Repinning signal-mind to `0baf90c8` was attempted and produced 195
   compile errors — its source is written against the older generated
   schema, so this is contract regeneration, not a repin.

Sibling f6db8d subflows hold Orchestrate locks (1126–1131) on exactly
this work — "Repin substrate to newest mains and regenerate from Ethos
Zero 7.x" on signal, signal-orchestrate and meta-signal-orchestrate — so
the walls above are known, owned work in flight, not discoveries this
flow should have resolved alone.

## Per repository

### aggregator — migrated to `dotos`, landed, `cargo update` now resolves

The one consumer of the five whose whole graph was reachable: it has no
`build.rs`, and its two producers were already half-migrated in their
working trees.

- Source moved wholesale from `nota` to `dotos` (`nota`→`dotos`,
  `Nota`→`Dotos`, `NOTA`→`DOTOS`; `nota_text_query`→`dotos_text_query`);
  `examples/*.nota` renamed to `*.dotos` and their contents converted
  from the paren grammar to the brace grammar `dotos 80c7b17` requires.
- Every `branch = "main"` pin replaced by a rev: meta-signal-aggregator
  `98cc36fc`, dotos `80c7b17f`, dotos-text-query `aee1a446`,
  signal-aggregator `5d2b80e2`, signal-frame `8aa0bcae`.
- `signal_frame::BoundExchangeFrame::new` now takes a `WireRoute`. The
  route's meaning is contract-local, so the derivation was put in the
  contract crates (`AggregatorRequest::wire_route`,
  `MetaAggregatorRequest::wire_route`: root 0 for requests, variant byte
  = the operation's position in the contract's heads) and the daemon
  echoes the incoming frame's route onto its reply.
- Version `0.3.1` → **`0.4.0`**: the wire changed (a bound contract
  header and a different text grammar), which is exactly what the
  `versioning` skill names.
- Gate: `cargo fmt --check`, `cargo clippy --all-targets -D warnings`,
  `cargo test --all` (14 suites green, 62 boundary tests), `cargo doc
  --no-deps`, `nix flake check -L --builders ''` — all green.
- `cargo update` after landing: **"Locking 0 packages"**, no error. The
  Tier 0 item 1 goal is met here.
- Landed on main at `87c48f8169c94c5eb49936895cb7a0852520c11f`.

### harness — version bumped and landed; `cargo update` still blocked

- `harness 0.3.4` → **`0.4.0`**, landed. Commit `722b68b3` ("Port Harness
  terminal delivery to generated Signal contract") changed the terminal
  delivery wire — it repinned signal-terminal and rewrote
  `src/terminal.rs`, `src/claude.rs`, `src/delivery.rs`,
  `src/subscription.rs` and their tests — while leaving the version at
  `0.3.4`. A breaking wire change with no prior release at `0.3.4` is a
  minor bump on a 0.x line.
- Gate on the landed state: fmt, clippy, `cargo test --all` (21 suites
  green), `cargo doc`, `nix flake check -L --builders ''` — all green.
- The dotos migration of harness was **prepared and then abandoned as
  unreachable**: harness's `build.rs` needs the deleted `schema-rust`
  Nexus emitter (wall 1), its checked-in `src/schema/daemon.rs` matches a
  `triad-runtime` generation that still spells `ComponentArgument::
  InlineNota`/`NotaFile` (head spells `InlineDotos`/`DotosFile`), and the
  freeze alternative was refused by Cargo's patch rules (above). No
  half-migration was left on main.
- Landed on main at `9a4d3375b02250ce724099bd9111c3ae6384d64e`.
  `cargo update` still fails on `nota`; the tier-0 test branch
  `f6db8d-cargo-update` (`d28634c26cd5`) stands unchanged.

### message — repinned to the coherent producer front, landed

Not one of the five, but harness's graph could not even be resolved
while message pinned an older signal-harness. message pinned
signal-harness `c05eacf1` (→ signal-persona `2802259f`) against the rest
of the estate's `0baf90c8`; with `links = "signal-persona"` that is an
outright resolution failure, not a duplicate.

- signal-harness `c05eacf1` → `cdfd4e3c`, triad-runtime `7d10bb9d` →
  `02cdd49d`. Both ranges are docs-only or a dependency-pin change; the
  signal-persona delta is a single build-dependency feature flag, so no
  public behaviour, wire or storage of message changed and its version
  stays `0.11.1`.
- Gate: fmt, clippy, `cargo test --all`, `cargo doc`, `nix flake check -L
  --builders ''` — all green. `cargo update` resolves.
- Landed on main at `38345dae42ac04caad0204ddbb94daf8f92c3367`.

### signal-aggregator, meta-signal-aggregator, dotos-text-query — landed

These three were the precondition for aggregator.

- **dotos-text-query** `aee1a446bb3236858d7157bad88dd63550abc25b`: its
  only mutable pin (`dotos`, `branch = "main"`) fixed at `80c7b17f`.
  Version unchanged — no surface moved. Full gate green.
- **signal-aggregator** `5d2b80e21f1a79b1025731d269ceb03c64f26d5b`: a
  dotos migration was **found uncommitted in the working tree** and
  committed first as its own commit, per the hard boundary. It was
  unfinished — its `signal_channel!` block still used the pre-contract
  form and its canonical example file was still in the old grammar. This
  flow bound the ordinary contract seat (`AggregatorWire`, contract id 1,
  wire revision 1, matching signal-harness's and signal-mind's
  convention), pinned dotos `80c7b17`, dotos-text-query `aee1a446` and
  signal-frame `8aa0bcae`, regenerated `examples/canonical.dotos` from
  the encoders, derived the frame-required traits on the wire marker, and
  exposed `wire_route`. Version `0.5.0` → **`0.6.0`** (wire change). Full
  gate green.
- **meta-signal-aggregator**
  `98cc36fc7cbf9d0ae18d976a19c5c1a626d165d5`: same shape — found-in-tree
  migration committed first, then the meta seat (`MetaAggregatorWire`,
  contract id 2), the same pins, a regenerated canonical file, and
  `wire_route`. Version `0.3.0` → **`0.4.0`**. Full gate green.

### router — prepared, gated red at resolution, left on a test branch

router was already half-migrated on main: its features are spelled
`dotos-text`, it already carried `dotos` at `80c7b17` as an optional
dependency, and `src/meta.rs`, `src/client.rs` and `src/lib.rs` were on
the `dotos` API — while `src/router.rs`, `src/message.rs` and
`src/error.rs` still used `nota::` unconditionally through a second,
mutable `nota` pin. This flow finished that: removed the `nota`
dependency, made `dotos` non-optional (the codec use is unconditional),
collapsed the duplicate `Error::Dotos` variant, renamed the remaining
sources, and converted nine `branch = "main"` pins to revs.

It cannot resolve. signal-criome's head requires signal-standard
`f12d0cb9` while meta-signal-router requires `d5a4a545`, and
signal-standard declares `links`; the older signal-criome revisions that
use `d5a4a545` depend on a `schema-rust` that pins `nota`. Working
around that lands on wall 2 (signal-mind vs signal-persona). Left on
`f6db8d-nota-pins` at `5fa990dc7f62629cafe08998691b5851f0f0a5e3`;
main untouched at `f60d4e33d0d0`.

### listener — not attempted; blocked upstream

Both of its producers, signal-listener and meta-signal-listener, still
declare `nota-text` and pin `nota` at `branch = "main"`, and both build
against the deleted `schema-rust` contract-crate emitter
(`ContractCrateBuild`, `GenerationDriver`, `CargoSchemaMetadata`,
`DependencySchema`). Migrating listener means regenerating those two
contracts first, which is wall 1. main untouched; the tier-0 test branch
`f6db8d-cargo-update` (`04137484445b`) stands.

### repository-ledger — not attempted; contracts prepared on test branches

repository-ledger's own `build.rs` uses the deleted Nexus emitter
(through the alias `schema-rust-next`, pinned at `0f306826`, which itself
pins `nota` at `branch = "main"`), so the consumer is behind wall 1.

Its two contract crates did hold uncommitted dotos migrations, which were
committed and finished rather than left dirty:

- **signal-repository-ledger**: found-in-tree migration committed, then
  the ordinary `LedgerWire` seat bound, dotos `80c7b17` and signal-frame
  `8aa0bcae` pinned, two canonical text expectations updated to the brace
  grammar, version `0.1.0` → `0.2.0`. Full gate green.
- **meta-signal-repository-ledger**: found-in-tree migration and a
  deleted `result` build symlink committed, then the `MetaLedgerWire`
  seat (contract id 2), the same pins, `WireRoute` threaded through the
  round-trip test, version `0.1.0` → `0.2.0`. Full gate green.

Neither was landed on main. signal-repository-ledger's GitHub `main`
(`894335a074f3`, "docs: restore Protos estate status") has **diverged**
from the base this work sits on (`1a83dc31`, "docs: mark Protos estate
status") in the same shape the tier-0 report recorded for
repository-ledger, and the brief forbids resolving that divergence. Both
are pushed to GitHub as `f6db8d-nota-pins`.

**Method note**: signal-repository-ledger has two git remotes — `github`
(GitHub) and `origin` (`gitolite@localhost`, a local mirror). jj's
default push target there is the mirror, so a first `jj git push
--bookmark main` moved the *mirror's* main sideways onto the local-only
divergent commit; it was immediately repointed to the intended revision
and GitHub was never touched by it. Every other repository in this report
has GitHub as `origin`. Landed revisions were re-verified with `git
ls-remote` after each push, because `jj bookmark set` can silently refuse
a sideways move.

### repository-ledger's local/origin divergence — recorded, not resolved

As the tier-0 report found and this flow re-confirmed: local `main`
`0580eff46139` ("docs: restore Protos estate status", also carrying
`realizer-three-stack-status`) against `main@origin` `4153fd848c69`
("docs: integrate Protos estate status"). Unchanged by this flow. The
same sibling-commit divergence exists in signal-repository-ledger
(`894335a074f3` vs `1a83dc31dd17`) and is the reason its finished
migration is on a branch.

## What would unblock the rest

In order, and all of it in the territory the sibling "repin substrate to
newest mains and regenerate from Ethos Zero 7.x" subflows already hold:

1. Restore or replace `schema-rust`'s Nexus daemon and contract-crate
   emitters on main, against `dotos`. Nine `build.rs` consumers wait on
   it, harness and repository-ledger among them.
2. Regenerate signal-mind against signal-persona 0.3.1. router waits on
   it.
3. Migrate signal-listener and meta-signal-listener to `dotos` once (1)
   exists. listener waits on them.
4. Resolve the `repository-ledger` / `signal-repository-ledger` main
   divergences, then land the two branches this flow left.

## Table

| Repository | What `nota` became | Outcome | Revision |
| --- | --- | --- | --- |
| aggregator | `dotos` @ `80c7b17f` (+ `dotos-text-query`) | migrated, gated green, landed; `cargo update` resolves | `87c48f8169c94c5eb49936895cb7a0852520c11f` (main) |
| listener | `dotos` — unreachable: both Signal producers still on `nota` and on the deleted `schema-rust` emitter | not attempted; blocked upstream | main unchanged `471b0d598f4e`; tier-0 branch `04137484445b` |
| harness | `dotos` — unreachable: `build.rs` needs the deleted `schema-rust` Nexus emitter | version bumped 0.3.4 → 0.4.0 for 722b68b3, gated green, landed; `cargo update` still blocked | `9a4d3375b02250ce724099bd9111c3ae6384d64e` (main) |
| router | `dotos` @ `80c7b17f` | migration completed but graph unresolvable (signal-standard `links` conflict, then signal-mind); left on test branch | `5fa990dc7f62629cafe08998691b5851f0f0a5e3` (`f6db8d-nota-pins`); main `f60d4e33d0d0` |
| repository-ledger | `dotos` — unreachable: `build.rs` needs the deleted `schema-rust` Nexus emitter | not attempted; both contract crates finished and left on test branches; local/origin main divergence recorded, not resolved | main unchanged `4153fd848c69` (origin) |
| message *(producer, required for harness)* | already `dotos` | repinned to the coherent producer front, gated green, landed | `38345dae42ac04caad0204ddbb94daf8f92c3367` (main) |
| dotos-text-query *(producer)* | is the renamed `nota-text-query` | mutable `dotos` pin fixed, gated green, landed | `aee1a446bb3236858d7157bad88dd63550abc25b` (main) |
| signal-aggregator *(producer)* | `dotos` @ `80c7b17f` | found-in-tree migration committed and finished, 0.5.0 → 0.6.0, gated green, landed | `5d2b80e21f1a79b1025731d269ceb03c64f26d5b` (main) |
| meta-signal-aggregator *(producer)* | `dotos` @ `80c7b17f` | found-in-tree migration committed and finished, 0.3.0 → 0.4.0, gated green, landed | `98cc36fc7cbf9d0ae18d976a19c5c1a626d165d5` (main) |
| signal-repository-ledger *(producer)* | `dotos` @ `80c7b17f` | found-in-tree migration committed and finished, 0.1.0 → 0.2.0, gated green; main diverged, so left on a branch | `9d267c275df7d2f9db800196465a7dd50ec38623` (`f6db8d-nota-pins`) |
| meta-signal-repository-ledger *(producer)* | `dotos` @ `80c7b17f` | found-in-tree migration committed and finished, 0.1.0 → 0.2.0, gated green; held with its ordinary contract | `0c2da541ccb65217cb5b112b85e3790bac0e9293` (`f6db8d-nota-pins`) |
| *(the package itself)* | `nota` → `dotos` at `1facca44fbcb37633f71fcf6f73bd693fbe56a5e`; last `nota`-defining revision `89dc3c85a9ff96d4e4d53accfd867df672cae5a8` | — | — |

## Sources

- Witnessed on this host, 2026-09-11: `git log`, `git show`, `git
  ls-remote`, `git grep`, `jj status`, `jj log`, `jj diff`, `jj describe`,
  `jj new`, `jj restore`, `jj abandon`, `jj bookmark`, `jj git push`,
  `cargo check`, `cargo update`, `cargo fmt --check`, `cargo clippy
  --all-targets -- -D warnings`, `cargo test --all`, `cargo doc
  --no-deps`, and `nix flake check -L --builders ''` in
  `/git/github.com/LiGoldragon/{nota,dotos,dotos-text-query,message,harness,router,aggregator,listener,repository-ledger,signal-frame,signal-harness,meta-signal-harness,signal-persona,signal-mind,signal-standard,signal-criome,signal-aggregator,meta-signal-aggregator,signal-repository-ledger,meta-signal-repository-ledger,signal-listener,meta-signal-listener,schema-rust,triad-runtime}`.
- Witnessed: `orchestrate 'Observe.Locks'` before any repository was
  touched, and `Lock`/`Release` for every repository this flow wrote in
  (1134, 1136, 1143, 1154, 1155, 1156, 1158, 1167, 1168, 1170, 1184). No
  repository this flow touched was held by another flow; locks 1113,
  1114, 1123, 1124, 1126–1131 (sibling f6db8d subflows) and the 542442
  set were observed and avoided.
- Read: `/home/li/primary/flows/f6db8d/reports/cargo-update-tier0.md` for
  the five failing repositories, their test branches, and the
  repository-ledger divergence it recorded.
- Searched: `Vision/`, `Intent/`, `vision-raw/`, `flows/*/vision/` and
  `flows/*/notion/` for `nota` and `dotos`; no ruling on the rename and
  no freeze or deprecation of any of the five consumers was found.
- Skills loaded and applied: `subflow`, `spirit`, `behavior`,
  `orchestrate`, `file-editing`, `testing`, `versioning`,
  `flow-evidence`, `psyche`.
