# Datom migration — the substrate moved, and who moved with it

Subflow of main flow f6db8d, 2026-09-11/12. Brief: realize "error, not
fault" in ethos-zero, then move every consumer of protos, datom-codec and
ethos-zero — and their signal and meta-signal contracts — onto tonight's
heads, deleting every compatibility path met on the way.

Everything below marked **witnessed** was read or run by this flow on this
machine. **Relayed** means a named subflow of this flow ran it and reported
it; every per-repository gate result in the tables is relayed from the
subflow that held that repository's Orchestrate lock, except ethos-zero,
signal-message and signal-domain, whose gates this flow ran itself.

---

## 1. The producer: "error, not fault"

Vision (2026-09-09, relayed through
`flows/f6db8d/reports/recent-vision.md` item 9, itself quoting
`flows/564f55/vision/archive-datom.md:47`): *"error, not fault"*.

Witnessed: ethos-zero was the last holdout. `pub trait ConceptualFaulting`
stood in its public API at `src/lib.rs:530`, with the noun through its
module docs, its checking and conception modules, three local bindings and
a test fixture directory named `faulty`.

Done, witnessed, in one commit at
`/git/github.com/LiGoldragon/ethos-zero` `da585049`:

- `ConceptualFaulting` → **`ConceptualErroring`**, and its capability's doc
  now says "Construct the error from its path and problem".
- Every remaining `fault` in prose, locals and fixture names became `error`
  or `err`: `src/lib.rs`, `src/checking.rs`, `src/conception.rs`,
  `src/generation.rs`, `tests/cli.rs` (`faulty` → `erroneous`), and
  `error.ethos`'s heading comment.
- The Delineation/Protoform sweep (item 10) landed in the same commit. The
  module-doc layer table and the README pass table had been describing
  types and kinds that **do not exist**: they named `protos::Delineation`,
  `protos::Protoform`, `protos::Text`, `Conceivable<File>`,
  `Actualizable<File>`, `Situated<Error>` and `protos::Pathed`. Witnessed
  against the code, the real chain is `String` → `Canonical` →
  `protos::Protos` → `File` → Rust text, carried by `Canonicalizable`,
  `protos::Protosizable`, `Ethosizable<File>` and `Generating`, with
  `Actualizing<File>` on `Potential<File>` for the whole descent and
  ethos-zero's own `Pathed` for the path convention. Both tables were
  rewritten to that.

Witnessed, and it decided the risk: `grep -rl ConceptualFaulting` over
every repository under `/git/github.com/LiGoldragon/`, excluding `target/`,
returns **nothing outside ethos-zero itself**. The rename breaks no
consumer.

A public trait rename is major: **7.0.1 → 8.0.0**.

---

## 2. What "the new heads" means, and why every bump is major

| producer | version | rev |
|---|---|---|
| protos | 0.30.0 | `e8701521a37c698d6a2eb933618b9d5d1c6f6ffb` |
| datom-codec | 0.26.1 | `18129314966c5043ee659de452b6f976fa319b21` |
| ethos-zero | **8.0.0** (this flow) | `da58504926dabe4680bb7863d812846b0f845d86` |

datom-codec 0.26 changed the canonical datom wire text. Per `versioning`, a
wire-text change is breaking, so every crate whose declared types carry the
datom derives took a **major** bump on repin even where its own Rust did
not change and its regenerated module was byte-identical.

Two producer-side changes bit consumers, both witnessed by the subflow that
hit them and relayed here:

- **protos 0.30.0 changed opaque-string round-tripping.** An unpunctuated,
  space-free string now textualizes **bare** rather than delimited:
  claude-answers' path expectation moved from `File.«/home/li/x.jsonl»` to
  `File./home/li/x.jsonl` (relayed; the subflow verified by scratch test
  that punctuated, multi-word and empty strings still delimit).
- **The string delimiter is now guillemets, not curly quotes** — `«Cluster
  CA»`, not `“Cluster CA”` (relayed from the clavifaber subflow, which
  checked protos' own `Boundary`/`Escaping` source before rewriting
  anything). **This flow's own `datom` skill still documents curly quotes.**
  The brief warned that the `datom` and `ethos` skills describe an older
  design and that code is the authority; this is the concrete instance, and
  the skill is wrong where it stands.
- **ethos-zero 8.0.0 renamed the intrinsic `Text` to `String`** and changed
  the Library file root, which for clavifaber turned every declared type
  from a tuple struct with a hand-written `Datomic` impl into a named-field
  struct deriving `Datomizable`/`Compositional` — so every construction and
  field access in its `src/` and `tests/` changed shape (relayed).

---

## 3. The table

"Before" and "after" are the repository's own version and the `origin/main`
commit it sat on before this flow, and the commit this flow landed. "Gate"
is the full local gate: `cargo test --all-features`, `cargo fmt --check`,
`cargo clippy --all-targets --all-features -- -D warnings`, `cargo doc
--no-deps --all-features`, and `nix flake check -L --builders ''`.

### Landed on main, full gate green

| repository | before | after | gate |
|---|---|---|---|
| ethos-zero | 7.0.1 `212b3590` | **8.0.0** `da585049` | green |
| signal-message | 1.0.0 `178a5ef7` | **2.0.0** `f03a147c` | green |
| signal-domain | 1.0.1 `da553c95` | **2.0.0** `01c73e78` | green |
| signal-persona | 1.0.0 `740eb20f` | **2.0.0** `07494bb2` | green |
| signal-terminal | 1.0.1 `ddbd3237` | **2.0.0** `b0523f77` | green |
| signal-introspect | 1.1.0 `910b1e37` | **2.0.0** `5b362716` | green |
| signal-upgrade | 1.0.0 `8e73d740` | **2.0.0** `e9bffc57` | green |
| signal-spirit | 2.0.0 `e4ab1062` | **3.0.0** `c1d78e85` | green |
| signal-spirit-judge | 1.0.0 `064d23d1` | **2.0.0** `f9da94e3` | green |
| meta-signal-spirit | 2.0.1 `a4b8cdde` | **3.0.0** `9f6c648e` | green |
| meta-signal-upgrade | 1.0.0 `ce82dfa1` | **2.0.0** `83c6cead` | green |
| meta-signal-terminal | 1.0.1 `d3289568` | **2.0.0** `3d0eafa1` | green |
| claude-answers | 0.6.0 `2f281e39` | **0.7.0** `cf124370` | green |
| clavifaber | 0.3.0 `2aaf293f` | **0.4.0** `8fa6dc44` | green |

### Landed on the pushed test branch `f6db8d-datom-migration`

Per the brief: a consumer whose gate stays red for a reason outside its own
code leaves a pushed branch rather than main.

| repository | before | after (branch) | gate | why red |
|---|---|---|---|---|
| signal-mirror | 1.0.0 `e6c565ca` | **2.0.0** `4c6765fa` | test RED, clippy RED; fmt, doc, `nix flake check` green | Its one Signal dependency is `signal-standard`. That repository's main has moved to tonight's heads but in the same move **renamed its package to `signal`**, so no pin exists that keeps the old crate name at the new revs; two `datom-codec` versions coexist and `Option<StandardSocket>` fails `Datomizable`/`Compositional`. Repinning means rewriting every `signal_standard::` reference — the item-7 dependents migration, and `signal` is under a sibling lock. |
| meta-signal-mirror | 1.0.0 `bdc76bcd` | **2.0.0** `b269ceda` | test RED, clippy RED; fmt, doc, `nix flake check` green | Second in the same chain: `signal-mirror`'s main is not yet migrated, so `NetworkEndpoint`'s derives resolve against two `datom-codec` versions. The subflow tried repinning `signal-standard` to its new head, hit `no matching package named signal-standard`, and reverted. |

Both branches are pushed and carry the complete migration; each needs only
its blocker to land, then a re-gate and a push to main.

### Skipped, and the lock that held them

| repository | lock |
|---|---|
| lojix | 1111 `LojixNexusHardening` (f6db8d) |
| horizon-rs | 1112 `HorizonRsNoFreeFunctions` (f6db8d) |
| orchestrate | 1126 `OrchestrateFrameAndAuthority` (f6db8d) |
| signal-orchestrate | 1127 `SignalOrchestrateEthosSevenRepin` (f6db8d) |
| meta-signal-orchestrate | 1128 `MetaSignalOrchestrateEthosSevenRepin` (f6db8d) |
| signal | 1129 `SignalSharedFrameRepin` (f6db8d) |
| signal-lojix, meta-signal-lojix | 1130 `SignalLojixEvidenceShape` (f6db8d) |
| terminal-cell, terminal, mentci (`Cargo.toml` only) | 1124 `F6db8dRemovalsTerminalCell` (f6db8d) |
| curriculum-deploy | 851 `CurriculumDeployDatomMigration` (**flow 542442**) |

Witnessed: the f6db8d locks above were held by sibling subflows at the
moment this flow observed them, exactly as the brief anticipated. Three of
them — 1127, 1128, 1129 — are named for the same work this flow was doing
("Repin substrate to newest mains and regenerate from Ethos Zero 7.x"), so
`signal`, `signal-orchestrate` and `meta-signal-orchestrate` were another
subflow's to move.

Witnessed and worth flagging: **curriculum-deploy's lock 851 reserves a
worktree** (`/home/li/wt/.../curriculum-deploy/datom-codec-542442`), not the
main checkout at `/git/github.com/LiGoldragon/curriculum-deploy`. The
delegate skipped on the strength of the lock's subject rather than its
paths — a different flow migrating the same repository for the same reason.
This flow judges that the right call and records it as a skip, not an
omission. Its head is 0.6.2, still on datom-codec 0.25.6 / protos 0.29.1 /
ethos-zero 6.1.4.

### Excluded by the brief, untouched

`spirit`, `mirror`, `chroma`, the kameo fork, and every running service.
`signal-spirit`, `signal-spirit-judge`, `meta-signal-spirit`,
`signal-mirror` and `meta-signal-mirror` were treated as in scope: they are
separate contract repositories, not the daemons the brief named, and moving
them touches neither `spirit` nor `mirror`.

---

## 4. Compatibility paths deleted

The brief said to delete any compatibility path met. What was met, relayed
from the subflow that found it:

- **`examples/canonical.dotos` → `examples/canonical.datom`**, converted to
  current datom text against each repository's own `.ethos` contract, old
  file deleted, and every document naming the old path corrected:
  signal-persona, signal-upgrade, meta-signal-upgrade, meta-signal-terminal,
  signal-mirror, meta-signal-mirror. The signal-upgrade subflow additionally
  **round-tripped all eight converted lines** through
  `Potential::<Query>/<Response>::actualize` in a throwaway example before
  deleting it — the strongest witness in this set.
- **An orphaned legacy dotos decode tree deleted outright**:
  `meta-signal-mirror/src/schema/**` — never `mod`-declared, referencing an
  undeclared `dotos-text` feature and an undeclared `dotos` crate — together
  with the dead `test-dotos-text` and `clippy-dotos-text` Nix checks that
  named it. signal-mirror carried the same two dead Nix checks; both went.
- **Stale Dotos prose rewritten, not patched**: signal-introspect's
  `ARCHITECTURE.md` and `skills.md` (which described a
  `signal_channel!`/Dotos architecture the crate no longer has) plus a dead
  `examplesFilter` in its `flake.nix` naming a nonexistent path;
  signal-spirit's `README.md`, `ARCHITECTURE.md` and `skills.md` (which
  described a retired Dotos/schema-projection pipeline); clavifaber's whole
  "Operator surface — DOTOS only" section in `skills.md`, plus
  `publication.dotos` prose in its `README.md` and `ARCHITECTURE.md`.
- **One real upstream break fixed rather than worked around**:
  signal-spirit-judge's `tests/scaffold.rs` — upstream `Justification`
  changed from an enum to a struct `{ testimony, reasoning }`.

No compatibility shim, feature alias, dual decode path or version
negotiation was added anywhere.

---

## 5. What this flow did not reach, and why

**The `dotos-text` estate is not downstream of the substrate.** Witnessed:
`signal-frame` 0.4.0 declares `dotos-text = ["dep:dotos"]` over the separate
`dotos` crate, and **neither `signal-frame` nor `dotos` depends on protos,
datom-codec or ethos-zero at all** (`grep -rlE
'LiGoldragon/(protos|datom-codec|ethos-zero)' --include=Cargo.toml` over
both returns nothing). Every one of the roughly fifty repositories still
carrying a `dotos-text` feature reaches it through `signal-frame`, not
through anything this flow moved. Converting that estate is a distinct
migration, and it is gated on the question the psyche deferred at
`flows/fe34eb/vision/signal.md:23` — whether signal-frame's envelope layer
*is* the protocol, and so whether signal-frame is absorbed into `signal` or
stays separate. That is item 7's unresolved merge decision, and it belongs
to the living, not to a repin.

**`.dotos` files outside the substrate consumers remain.** Witnessed:
`signal-sema/magnitude.schema.dotos`, `message/.message/agents.dotos`,
`spirit/tests/fixtures/spirit_judge_live_eval.dotos` (forbidden),
`criomos-horizon-config/horizon.dotos` and three under
`CriomOS-test-cluster/clusters/` (deploy-adjacent, and flow 542442 holds
locks across that tree), the `tree-sitter-dotos` fixtures, and the
`examples/canonical.dotos` of every signal contract this flow did not hold.
Four repositories are still named for the format: `dotos`, `dotos-config`,
`dotos-text-query`, `tree-sitter-dotos` — retiring those is a
`repository-lifecycle` decision, not a migration step.

**One old `datom-codec` survives transitively, and it is `signal`'s to
remove.** Relayed, independently, from the signal-spirit, signal-spirit-judge
and meta-signal-spirit subflows: those three now carry a single direct
`datom-codec` 0.26.1 pin each, but their lockfiles still resolve one
`datom-codec` 0.25.6 through `signal-spirit → signal@626e407b →
ethos-zero (build-dependency)`. It blocked no gate. It clears when
`signal-spirit` repins the `signal` crate — which waits on `signal` itself,
held tonight under lock 1129. The same chain is what leaves signal-mirror
and meta-signal-mirror on branches. **`signal` is the one remaining knot in
this migration**, and it was another subflow's to untie.

**One untidy landing, recorded rather than rewritten.** On signal-domain the
delegate had already committed and advanced main to `d33cbc70` while this
flow was running the same repository's gate; this flow's own commit landed
on top as an **empty** commit `01c73e78` with a duplicate description.
Rewriting pushed main history that sibling subflows may already have fetched
is worse than one empty commit, so it stands. signal-domain's content at
`01c73e78` is correct and witnessed.

**The Nix daemon crashed twice under the concurrent load** — `error: Nix
daemon disconnected unexpectedly`, with `daemon worker … crashed` in the
journal, on a machine with 22 GB available. Witnessed by this flow on
signal-domain. Each retry resumed further along because completed
derivations are cached, and the third attempt reported `all checks passed!`.
Reported as an observation; the cause is unknown and this flow did not
investigate it.

---

## Sources

- Brief of main flow f6db8d to this subflow (2026-09-11).
- `/home/li/primary/flows/f6db8d/reports/recent-vision.md` — items 2, 7, 8,
  9, 10 (relayed; itself relaying `flows/fe34eb/vision/datom.md:11`,
  `flows/fe34eb/vision/signal.md:23`, `flows/fe34eb/vision/ethos.md:7`,
  `flows/564f55/vision/archive-datom.md:47`,
  `flows/564f55/vision/archive-protos.md:109,121,153`).
- `/home/li/primary/flows/f6db8d/reports/dependency-survey.md` §3 — the pin
  graph (relayed).
- `/home/li/primary/flows/f6db8d/reports/periphery-audit.md` §§5–7 — the
  consumer findings (relayed).
- `/home/li/primary/Vision/datom.md:238-241` (relayed).
- `orchestrate 'Observe.Locks'`, run by this flow before each repository and
  again at the close (witnessed).
- Per-repository gate results: relayed from the subflow holding that
  repository's lock, named in the tables above; ethos-zero, signal-message
  and signal-domain witnessed by this flow.
- `/git/github.com/LiGoldragon/` working trees and `origin/main` refs, read
  by this flow (witnessed).
