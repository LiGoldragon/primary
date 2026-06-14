# New-Moon Meta-Report Audit — Open Items / Loose Ends of the Day

## 1. Beads

| Bead | Title | Status | Owner | Tracks |
|---|---|---|---|---|
| `primary-bojw` | Self-host the macro-table type: generate the pattern family from `core.schema` | **OPEN · P2** | li · operator lane | The macro-table self-host POC (stage 1) |
| `primary-3rj9` | Operator integration fixes: schema-next reconciliation fold-ins + spirit testing-trace regression | **OPEN · P2** | li · operator lane | The two regressions from designer review 633 |

Both are OPEN, P2, owner `li`, labeled `operator`. Both created and last updated 2026-06-14.

`primary-bojw` (macro-table self-host POC) is the staged self-host work: generate the `MacroPattern` family + leaves (`MacroDelimiter`, `MacroPosition`, `MacroCaptureName`, `MacroAtom`, `MacroPatternObject`, `MacroPatternObjects`, `MacroPatternDelimited`, `MacroPattern`) from `schema-next/schemas/core.schema` via the `schema-rust-next` `RustEmitter`, swap them into `declarative.rs` (delete hand-written defs, re-home impls, `String`→newtype leaves), and prove `macro_exploration.rs` + `design_examples.rs` stay green decoding the generated types. It explicitly **stops before** `SchemaMacro`/`MacroTemplate`/`MacroLibrary` — the `MacroTemplate` structural-vs-typed-output model is a designer-gated fork. Its latest comment (10:55) confirms report 628 independently validated this as the one real self-host removal target, and surfaces the adjacent `MacroShape`/`MacroOutputKind` no-Rust gap as the next clearest case (see design items below).

`primary-3rj9` (operator integration fixes) tracks two real regressions on the `structural-forms-integration` branch (6/8 repos faithful; these two carry regressions):
- **schema-next `2bb0228e`** reverted three reconciliation fold-ins from 631/`17b4ebc7`: the hand-written `NotaDecode`/`NotaEncode` machine codec on `TypeReference` is back (should be thin delegators to the structural single source of truth), `SchemaError` reverted from `thiserror` to a plain enum (re-apply `thiserror` + `#[error]`/`#[from]`), and the `HeadedAtom` seam was dropped so `(Bytes N)` is hand-decoded (route through `#[shape(head="Bytes", atom)]`). Likely integrated from raw schema-generics rather than the reconciled `17b4ebc7`. These are quality regressions invisible to tests.
- **spirit `d2cf86fd`** fails 2 tests under `cargo test --all-features` (testing-trace): `instrumentation_logging` — the `SemaWriteApplied` trace no longer fires because the `Arc<SemaDatabase>` store-sharing edit (commit `37bafef`) bypasses the `SemaEngine::apply` trace hook. Route the shared-store write through the apply hook and verify with `--all-features`.

## 2. Pending operator work

Outstanding implementation queue, all operator-lane:

1. **Integrate the three branch stacks onto their mains** — reaction-frame stack, sema-engine stack, and nota-next leaf shapes, each onto their respective repo `main` (operator's rebase/integration ownership).
2. **Remerge `structural-forms-integration` to main + drop the cross-repo branch pins** — gated: this happens once the nota-next leaf derives land on nota-next main. The branch pins are the temporary cross-repo coupling to retire after that integration.
3. **Fix the two regressions** (`primary-3rj9`) — schema-next fold-in restoration (thin delegators / no hand codec; `thiserror`; `HeadedAtom` seam) and the spirit `SemaWriteApplied` trace-hook fix; both independently verified, after which the branch is clean to remerge toward main.
4. **Start the macro-table self-host POC** (`primary-bojw`) — stage-1 slice as specced above; stop at the template fork and the 103-shape boundary.

## 3. Open DESIGN items surfaced today

- **Full `TypeReference` self-host** needs a nota-next derive extension for named-field / sum-head variants (report 631). Stage-1 self-host removes the pattern family; the full `TypeReference` removal is blocked on this derive-shape capability.
- **`MacroShape` / `MacroOutputKind` schema-declared-but-no-Rust gap** (report 628, confirmed in `primary-bojw`'s 10:55 comment). `core.schema` declares both but there is no generated or hand-written Rust for them — the clearest "schema-declared-but-not-emitted" case to close next (out of scope for stage 1).
- **"Visuals-as-data"** (report 632) — generate architecture diagrams from schema rather than hand-drawing them; treat diagrams as a derived view over the typed schema.
- **Intent-digest layer over the raw Spirit corpus** (report 632) — a synthesized digest sitting over the raw Spirit records, feeding the per-repo `INTENT.md` / workspace intent surfaces.
- **The coming auditor role** (report 632) — shape decided (automated auditor auto-proposes intent refreshes; psyche confirms each source-record retirement; closes the loop back to designer), lane mechanics still open; no `skills/auditor.md` or `reports/auditor/` yet.

## 4. Worktree hygiene

Report 628's worktree audit flagged 5 cleanup candidates. **All 5 are now gone / cleaned** under `~/wt/github.com/LiGoldragon/`:

| Candidate | Status |
|---|---|
| `persona/realign-signal-introspect` (empty) | Gone — no `persona` top-level worktree dir exists at all |
| `spirit/operator-guardian-hardening` (empty) | Gone — `spirit/` now holds only active worktrees |
| `lojix/<triad-port>` (orphaned) | Gone — `lojix/` holds only `horizon-leaner-shape` |
| `meta-signal-lojix/<triad-port>` (orphaned) | Gone — no `meta-signal-lojix` top-level dir exists at all |
| `signal-lojix/<triad-port>` (orphaned) | Gone — `signal-lojix/` holds only `horizon-leaner-shape` |

Remaining worktrees are all legitimate active branches:
- `spirit/`: `mirror-shipper`, `store-decomposition`, `structural-forms-integration`, `vc-followups`
- `lojix/` and `signal-lojix/`: `horizon-leaner-shape` (each)
- Plus top-level repo worktrees: `schema-next`, `schema-rust-next`, `sema-engine`, `nota-next`, `triad-runtime`, `meta-signal-spirit`, `signal-spirit`, and others (chroma, CriomOS*, horizon-rs, mirror).

Worktree hygiene is clean; no cleanup action remains from the 628 audit.