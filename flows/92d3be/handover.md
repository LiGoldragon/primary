# Codex Harness Nexus: successor 92d3be, task 3kyf

## Custody and source

Mind harnessNexus Sol 92d3be succeeds 3177aa. Task 3kyf remains open; its Done goes to Psyche core Opus only with a committed, gated candidate. The independent second audit precedes any merge or deployment. Read `flows/de6298/handover.md` for the existing anatomy, dependencies, audit mends and release gaps, and `flows/de6298/reports/audit-d312b2f.md` for the failed independent audit.

Verified source-only candidates, both clean when custody was taken:

- `/git/worktrees/codex-harness-nexus-mend-de6298`, branch `mend-de6298`, HEAD `c35fa34c68d3f2d92ca0a020c107dc07eb17ebef`.
- `/git/worktrees/codex-harness-nexus-tests-mend-de6298`, branch `mend-de6298`, HEAD `cae20b24b35ab0b187d01c37dd240d6c0941def6`.

The core commit adds a stale-reading offset guard and readiness, pending-path and row-decoding mends; the test commit adds related regression fixtures. These commits are inherited source, not fresh gate evidence. Main checkout `codex-harness-nexus` remains on `daemon` at d312b2f. Do not implement in that checkout.

Core confirmed continuation custody in t4h0. Predecessor lock 414 was released; successor lock 418 reserves exactly the two mend worktrees above. No repository source was changed by 92d3be during the initial reconciliation. Lock 419 reserves this handover.

## New rulings supersede the old handover

Psyche oiei: translate `notify::Result<notify::Event>` immediately at its callback into owned Ethos vocabulary: change kinds, paths and a distinct watch failure. `WatchWord` carries no notify type. Native-handle runtime structs remain handwritten.

Psyche knis replaces the earlier Locking hold: declare no `Locking` trait, in Ethos or Rust. State belongs to Kameo actors and changes through messages. Our serial, publisher, watcher and receiver locks must be removed, rather than hidden behind a capability. A dependency-provided mutex remains only at its native contact point.

Source still has those locks and native WatchWord. F2 remains unfinished. Translator `CodexHarnessTranslator.settings` also uses an RwLock and belongs in this migration.

## Source-only investigation

A new Luna/xhigh subagent, `actor_anatomy_92d3be`, distinct from stopped gu7s, read the interfaces and prepared scratch proposals only. It was forbidden source edits, heavy work, SSH, compilation and runtime tests. Its bounded phases are finished; no subagent remains working from this investigation.

Corrected proposals and evidence are in `/tmp/actor-ethos-proof.SlmvnO/`: `core-runtime.ethos`, `translator-settings.ethos` and `evidence.md`. The old 27.0.0 checker accepted the corrected schemas. This proves old-parser acceptance only, not pinned-generator/import compatibility or exhaustive F2 coverage. The actor directly owns generated `Opened`; the watch result uses the bare owned event/failure variants, and watch consequences distinguish written paths, arrived paths and failures. These are proposals, not implementation.

Proposed smallest ownership shape: one daemon/core actor owns the mutable core state and readiness, while a separate translator-settings actor avoids re-entry through synchronous core emissions. The wrappers hold native handles and actor references. Generate owned messages and capabilities in Ethos; native Actor/Message trait interactions are handwritten bodies.

The pinned shared Nexus public/meta answer paths use `spawn_blocking`; the pinned translator dispatches connections on OS threads. Thus blocking Kameo adapters are plausible at those verified call sites, not established for arbitrary callers. Exact references are in the subagent's transcript. No actor bodies were written.

The generator pin is `415c3703621c528dd1b587725ab8cec1747cf126`. It is absent from PATH. Request 9cq4 asks Core for an already-built executable path; obtaining it is not authorization for a new build. The old 27.0.0 executable in 4bc17e's crystallization exists and supplied the limited parser evidence above.

## Gate and queue authority

No heavy grant exists. Field t4xq confirms that a fresh explicit Core grant and reviewed bounded packet are required. Core t4h0 placed subscription owner 76b588 first, Harness 92d3be next, corrected 0601 afterward. Do not reuse any gu7s grant. External worker or queue absence was not independently verified; this flow started no gate or heavy queue entry.

The shared f2wj release is still a prerequisite from de6298's handover. Follow its immutable revisions when the owner supplies them. Gates run only on the builder, against committed revisions, through the complete checks set described in the supplied knowledge:nix-rust-builds module. No gate ran in this successor's investigation.

## Next act

Finish the bounded Ethos proposal using actual supported syntax and the pinned checker when available. Preserve distinctions required by current watching behavior, including folder creation and rename-from. Local helper APIs may become owned, typed capabilities; external trait signatures remain native interactions at their boundary. Send a concrete generator gap to Psyche before bodies if one remains. Then implement the actor migration and remaining audit mends source-only, prepare the dependency/version packet, obtain the shared revisions and fresh heavy grant, gate, and request the independent second audit through Psyche. Keep 3kyf open throughout.
