# Terminal estate migration — the branch-pinned consumers onto the Datom heads

Subflow of main flow f6db8d, 2026-09-11/12, thread
`f6db8d14-1dfe-472d-914e-9c441f852834`.

Brief: move `terminal`, `mentci`, `introspect`, `persona` and every sibling
consumer of the contracts released tonight — excluding spirit, mirror,
harness, listener, router, repository-ledger, chroma and any running daemon's
repository whose wire a deploy would need — onto the final producer heads,
following `reports/datom-migration.md`'s method; and deal with the dirty files
found in `terminal` without discarding them.

**Witnessed** means this flow read or ran it on this machine. **Relayed**
means a dispatched subflow of this flow ran it and reported it back. Where a
gate result is relayed, the table says so.

## 1. The dirty files — what they actually were

The brief asked whether `terminal`'s uncommitted files were flow 857335's
preliminary consumer edits, and said to build on them if so and otherwise set
them aside on `f6db8d-found-dirt`. They were not 857335's edits. Three
findings, all witnessed:

**They move backward, not forward.** `git diff` in `terminal` changes
`nota-text` to `dotos-text`, the `nota` dependency to `dotos`, and three
`branch = "main"` pins (`signal-frame`, `meta-signal-terminal`,
`signal-terminal`, `schema-rust`) to older immutable revisions — it also adds
a `[patch."https://github.com/LiGoldragon/signal-terminal.git"]` block
pointing at the same source it patches, which is the self-contradictory patch
`reports/removals.md` §4 recorded as blocking `cargo check` there. The
committed HEAD carries the *newer* `nota` naming; the working tree carries the
*older* `dotos` naming. No migration onto tonight's heads looks like that.

**The same reversal sits in two more repositories.** `introspect` (14 files)
and `meta-signal-introspect` (6 files) carried the identical `nota` → `dotos`
reversal with old immutable pins restored. The brief named only `terminal`'s
ten files; the condition was wider — `terminal` itself had seventeen dirty
files by the time this flow observed it, not ten.

**The timestamps settle it.** Every dirty file's mtime is **2026-07-31**.
Flow 857335 ran on 2026-09-10. The content is six weeks older than the flow it
was attributed to, and older than the `dotos` → `nota` rename commits that
landed on each repository's main in June 2026. `jj`'s reflog in all three
shows only `export from jj` entries and no stash. The most economical reading
is a working tree written from a pre-rename state on 2026-07-31 and never
updated when the rename landed; a second possible cause is a deliberate
restoration of old pins abandoned mid-way. This flow did not determine which,
and leaves the cause unknown.

Set aside, not discarded, and verified on the real remotes with
`git ls-remote https://github.com/LiGoldragon/<repo>.git f6db8d-found-dirt`:

| repository | files | `f6db8d-found-dirt` |
|---|---|---|
| terminal | 17 | `71c1e72134b575061d8a2cd1e4d0f27a1c156d09` |
| introspect | 14 | `03767b417aa9f6af19f6d6ad7e28fd78410e814d` |
| meta-signal-introspect | 6 | `56a6e8e799b11f1f81408ff86b420142fb2246a7` |

Each working copy was then returned to its own `main` with `jj new main`.

## 2. The psyche's warrant for deleting, not shimming

Distilled Vision, `Vision/datom.md:239-243` (witnessed):

> Everything moves to Datom: all of the stack, Horizon, Lojix, everything; no
> Dotos file remains. Datom's own line of descent is NOTA, which also passed
> through the temporary name Dotos; that old notation stays behind, frozen,
> and may be called legacy.

Raw vision behind it, `flows/01a03d6e/vision/archive-dotosFiles.md:9`
(witnessed): *"There should be no Dodos files anymore"* — with the
speech-to-text correction `Dodos` → `Dotos` recorded beside the quote. And
`flows/019feb93/vision/threeStacks.md:9` (witnessed), the psyche naming the
condition for retirement: the generated Rust for signal, nexus and sema types
is what must exist *"before the old Schema + NOTA stack can be retired"*.

So `nota-text` and `dotos-text` features, `signal-frame` envelopes,
`schema-rust` build-time codegen and the `nota`/`dotos` crates are deleted
where this flow touched them, never aliased and never kept behind a feature.

## 3. The real diagnosis — mutable branch pins, not staleness

`reports/periphery-audit.md` §6 relayed six branch-pinned consumers as
*broken now*. This flow re-derived that set directly rather than inheriting
it, by grepping every `Cargo.toml` under `/git/github.com/LiGoldragon/` for a
`branch = "main"` pin on a contract that moved tonight (witnessed). The result
corrects the inherited list in three ways:

- **`kin` does not exist.** `git ls-remote https://github.com/LiGoldragon/kin.git`
  returns `Repository not found`; no directory under
  `/git/github.com/LiGoldragon/` matches `*kin*`; and
  `reports/periphery-audit.md` itself never uses the word — grepped, no hit,
  there or in `removals.md`, `consumer-sweep.md` or `open-items.md`. The name
  reached this flow through its own brief's summary of the audit, not from the
  audit. One of the six named consumers names no repository, and this flow
  found nothing it could plausibly be a shorthand for. Recorded as an
  observation against the brief's premise rather than silently dropped.
- **Rev-pinned siblings are not broken.** `signal-harness`, `signal-mind`,
  `signal-system`, `meta-signal-harness` and `meta-signal-persona` all pin
  `signal-persona` by *immutable rev* at an old revision. They still resolve
  and still build. They are stale, on the retired stack, and will need moving
  — but they are not part of tonight's breakage, and this flow did not move
  them.
- **Two siblings the audit did not name are broken.** `meta-signal-system`
  and `system` both branch-pin `signal-persona`, and `persona-spirit`
  branch-pins `signal-persona` and `meta-signal-upgrade`.

The genuinely broken, in-scope set is therefore: `terminal`, `introspect`,
`mentci`, `persona`, `meta-signal-introspect`, `meta-signal-system`, `system`,
`persona-spirit`. `terminal-cell` is rev-pinned and not broken, but is
`terminal`'s own dependency and was moved with it. `harness`, `router` and
`spirit` carry the same branch-pin breakage and were left untouched because
the brief excludes them.

**The disease is the mutable pin itself**, and a repin that lands another
`branch = "main"` re-arms it. Every dispatch in this flow was instructed to
convert *every* LiGoldragon branch pin it met to an immutable rev, not only
the ones that had moved.

## 4. Not a repin — a port

`reports/datom-migration.md`'s method was written for consumers that were
already on the Datom stack and needed their pins refreshed. It does not
describe this estate. Witnessed by reading each `Cargo.toml` and `src/`:
`terminal`, `introspect`, `persona`, `mentci`, `system`, `terminal-cell`,
`meta-signal-introspect` and `meta-signal-system` sit on the **retired**
stack — `signal-frame` envelopes with `signal_channel!`, the `nota`/`dotos`
text crates and their cargo features, `schema-rust` build-time codegen,
`triad-runtime` and `sema-engine`. The contracts they consume have been
rewritten into ethos-generated, protos/datom-codec, rkyv-framed crates.

Moving them is a port of each consumer's Rust onto a different generated
surface, not a version bump. `meta-signal-terminal` at
`a9b18ee853a449709fd908bb4c2d16c8f7fd15ff` (2.0.1) was used as the exemplar
target shape throughout — `ethos/signal.ethos`, a `build.rs` asserting the
committed `src/generated/signal.rs` against a fresh `ethos-zero` generation,
`examples/canonical.datom`, and the rkyv `Signal`/`Signalizable`/
`ByteViewable`/`Restorable` surface in `src/lib.rs`.

## 5. Deployment safety

Witnessed: every `systemd.user.services.*` declared anywhere in
`/git/github.com/LiGoldragon/CriomOS-home` is one of `active-network-widget`,
`aggregator-daemon`, `chroma-daemon`, `codex-artifact-gateway`,
`codex-remote-control`, `criomos-ui-priority`, `listener`, `message-daemon`,
`orchestrate-nexus`, plus `spirit-daemon` and `spirit-judge` in
`modules/home/profiles/min/spirit.nix`. **None** of the repositories this flow
moved has a deployed unit. Nothing was deployed, no running service was
touched, and no process was killed.

## 6. The table

