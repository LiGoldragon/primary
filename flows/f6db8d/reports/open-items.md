# Open items left for the living — flow f6db8d

Compiled from `flows/f6db8d/log.md` and all 31 files in `flows/f6db8d/reports/*.md`
(five read-only audits: warrant, substrate, runtime, periphery, process; and the
overnight work reports that followed them). Assembled by five parallel research
passes over disjoint report sets, cross-checked against each other, plus a live
`git ls-remote --heads` sweep of all 188 repositories under
`/git/github.com/LiGoldragon/` and a check of `bd search` for beads already open
on these subjects. Every item below is a **claim relayed from a report**, not a
fact this compiling subflow independently witnessed, except where a report's own
witness text is quoted.

Existing beads found to touch these subjects (none closes any item below; noted
for cross-reference, not as resolution): `primary-cod` (closed, Lojix activation
failure evidence — matches W3, already done); `primary-2d7`/`primary-746` (closed
spikes on the Kameo fork's causal anatomy — background to A16 below, the rebase-
or-drop decision itself is still open); `primary-83s` (open, "Rename NOTA to
Dotos" — adjacent to A21/A22); `primary-hqu.14` (open, migrate spirit's schema
car off the deleted emitter — one repo in the schema-rust wall, C1); `primary-xqj`
and its subtasks (in_progress/closed, "Datom consumers use the current codec
contract" — the consumer-migration effort this flow's Wave 3/4 continued);
`primary-mjl.6` and `primary-akw` (in_progress, Lojix deployment truth /
Lojix+VSCodium deploy — background to A9–A14, C25–C27); `primary-ahk.1` (open,
"pure-read, state-only Orchestrate coordination boundary" — adjacent to A6).
No bead exists yet for the great majority of items below; the main flow creates
beads, not this subflow.

---

## (A) Design questions only the living can answer — 59 items

### Substrate: protos / datom-codec / ethos-zero

**A1. Does `Datomizable` name one conversion or two?**
`substrate-audit.md` §2.2 + §8; `datom-codec-fix.md` "Contradictions left standing" item 1. Repo: datom-codec. `Vision/protos.md`'s table and snippet give `Datomizable` two different signatures for `Protos` and a composition, while `Intent/conversion.md` says "A kind names one conversion and is borne by the type that undergoes it." Witness: code carries two associated-`Output` shapes (`Result<Datom, Error>` for descent, `Datom` for ascent) — "Vision as written is not literally implementable; the shape is unchanged."

**A2. Which bare-string rule, and what is its name?**
`substrate-audit.md` §3.1/§8; `datom-codec-fix.md`; `log.md` Wave 1. Repo: datom-codec. `Vision/datom.md` (2026-09-10) says a bare run may hold a colon; datom-codec 0.25.7 (committed after) already narrows it. Datom-codec 0.26.x's exhaustive "break only where protos reads the run back as something else" rule is now witnessed consistent with Vision (substrate-review.md), but the bare-string form still has no settled name — 564f55's own summary lists it open.

**A3. May the ethos canonical print differ from the Vision notation?**
`substrate-audit.md` §4.4/§10; `ethos-zero-fix.md` §6; `substrate-repin.md`. Repos: ethos-zero, protos. `LockPaths.Vector<LockPath>` must reprint with a space (`LockPaths.Vector <LockPath>`) because protos has no unseparated qualified head — "the clearest statement in the whole substrate that this is a compromise forced from below." Still open after every substrate release; protos 0.30.0/0.30.1 do not make the rejected shape readable.

**A4. Three protos changes needed for the "right shape" of `Vector<Integer>`/`Vector<Text>` (and whether it should exist at all).**
`ethos-zero-fix.md` §3; `protos-fix.md` "Left standing, deliberately"; `substrate-repin.md`; `substrate-review.md` "Hypotheses formed and disconfirmed". Repos: protos, ethos-zero. Verbatim, the three changes: a node for a name bearing constraints and no body; a reader that keeps the constraints instead of rewinding past them; a writer that prints constraints against the name with no space. Confirmed still unmet at 0.30.1 by diffing `src/core.rs` across releases. Coupled to A3 (same tension).

**A5. `Problem::MissingHead` looks unreachable — remove it or make it reachable?**
`protos-fix.md` "Left standing, deliberately". Repo: protos (`protos.ethos`). The reader only raises it inside the run loop, which no leading `.` or `<` ever reaches; every probed case reads as a bare run or dispatches to the angled enclosure first. It is declared in `protos.ethos`, so removing it changes the generated contract.

**A6. ARITY removal vs Vision — should `Compositional` split into a positional kind and a scalar kind?**
`datom-codec-fix.md` "Decisions taken on the living's behalf" item 3; `substrate-review.md` §2/§5 (flagship item). Repo: datom-codec, with Vision as contested authority. Both the `ARITY` constant and the `from_positions` capability are named in `Vision/protos.md` and `Vision/datom.md:120,141`; a full search of `flows/*/vision/`, `flows/*/notion/`, `vision-raw/` for `from_positions`/`Compositional`/`positions(` found nothing that supersedes them. Witness: `unreachable!()` count in datom-codec fell 19→2; the whole suite composes through the new trait. "That split is the thing to put to the living. Until then the released substrate contradicts two Vision files that have not been amended."

**A7. Non-finite `f64` writes text no `Decimal` reads (D4) — the terminal fix is an ethos-zero change first.**
`substrate-review.md` §5 D4; `datom-codec-fix.md` decision 4. Repos: datom-codec (symptom), ethos-zero (`Vision/ethos.md:133` makes Decimal an intrinsic; `generation.rs:58` lowers it to `f64`). Witness: `{ NaN }` → `Value { expected: "Decimal", value: "NaN" }` — the writer now accepts silently what the reader refuses, where it previously panicked. "The terminal fix is a finite-decimal type, which is an ethos-zero change first." `substrate-drift.md` explicitly left this and A6 for the living.

**A8. `protos::Error` datomizes under head `ProtosError` while its variant is `Structural` — one naming ruling owed.**
`datom-codec-fix.md` "Contradictions left standing" item 2. Repo: datom-codec. Text reads `Structural.ProtosError.{ … }`, two names for one thing; Vision names neither.

**A9. Single-field structs — alias or newtype?**
`recent-vision.md` item 12. Repos: ethos-zero, protos, datom-codec. Psyche (`flows/8e9e77/vision/single-field-structs.md:5,13-15`): a single-field struct "should be a new type" and single-field structs should possibly be refused. But the form named for it (`X.T`) generates `pub type X = T;`, a Rust *alias*, and `Vision/ethos.md` itself says "an alias is not a new type and cannot carry a derive" — so the psyche's own ruling and Vision's own alias rule contradict each other. Load-bearing today: `ReaderBudget.{ Integer }` at `protos.ethos:16` generates exactly this alias, and protos's own `dependency-ethos` Nix check runs over that file — refusing arity-1 products today **breaks protos's own gate**. Five-step remediation named, step (a) is the ruling. "Safe unattended: NO."

**A10. Is `Sized` a tenth intrinsic, and are unconditional `rkyv`/`Clone,Debug,PartialEq` derives, `where Self: Sized`, the import-rename form, and `TYPE_DECLARATION_LIMIT` wanted?**
`ethos-zero-fix.md` §6; `substrate-audit.md` §4.3/§8. Repo: ethos-zero. Vision lists exactly nine intrinsics; each emission is defensible and none is written down. Now baked into every committed contract (`substrate-drift.md`).

**A11. Is `Processable<[ Clonable Sendable ] Serializable>`'s ordering a Vision correction rather than a code defect?**
`substrate-audit.md` §4.4 closing. Repo: ethos-zero. "One place where the code is arguably righter than Vision… worth putting to the living as a Vision correction rather than a code one."

**A12. §4.3 qualification leak — `Option<std::boxed::Box<Self>>` vs "no `use` statements" (borderline A/C).**
`ethos-zero-fix.md` §6. Repo: ethos-zero. Compiles only because `Option` is in the prelude, against Vision's stated no-`use`-statements rule. Sits under the same §4.3 group whose siblings are explicitly the living's.

**A13. Is `Vector<Integer>` splitting into two protos structures accepted design or unnoticed defect?**
`substrate-audit.md` §8. Repos: protos, ethos-zero. No psyche record found either way across `Vision/`, `vision-raw/`, `flows/*/vision/`. "Either protos gains an unseparated qualified head, or ethos stops delegating its writer."

**A14. Should `Boundary::Parentheses` eventually move off `Opaque`?**
`recent-vision.md` item 11. Repos: protos, datom-codec. `protos/README.md:65` still calls guillemets and parentheses both opaque — "exactly what the psyche corrected." The distilled sentence may now be behind the code (a distillation-edit question, not just a code one).

**A15. datom-codec's dirty working tree is mid-deleting the `Compositional` design — whose change, and is it sanctioned?**
`skill-proposals.md` §5. Repo: datom-codec. `Vision/datom.md` writes `from_positions(p: Positions<'_>)`; the released crate writes `from_positions(positions: Positions<'_>, budget: &mut Budget)`. Separately, an **uncommitted** working-tree change reduces the trait to `fn compose(datom, budget)`, deleting `ARITY` and `from_positions`, while `src/composition.rs` still references them — "the tree does not currently compile as it stands… This flow does not know whose change this is or whether it is sanctioned."

### Substrate-adjacent: unfinished quality items surfaced as if design (now resolved — listed so they aren't reopened)

- Query vs Request enum naming — **resolved**, ethos-zero 7.0.0 chose `Query` per Vision (`substrate-audit.md` §4.2a; `log.md` Wave 1).
- D1 (protos-kinds.ethos contract not its generator's output), D2 (no drift check anywhere), D5 (PrintStep/ShowStep duplication), D6 (unreachable Arity refusal) — all **closed** by `substrate-drift.md`.

### Orchestrate / Nexus

**A16. The meta CLI's name: `orchestrate-meta`, `meta-orchestrate`, or `component-meta`?**
`orchestrate-work.md` §6; `orchestrate-review.md` §3.2/D-3; `orchestrate-followup.md` §6; `lojix-history.md` (parallel `lojix-meta` naming). Repos: orchestrate, CriomOS-home, nexus. `Vision/orchestrate.md:7` says a deployment without `meta-orchestrate` is wrong; `Vision/nexus.md` and the `nexus` skill say the meta CLI is `component-meta`; the package has built `orchestrate-meta` since 0.31.0. `CriomOS-home/modules/home/profiles/min/orchestrate.nix` wraps `meta-orchestrate` and **fails at build time** in `makeWrapper`; `checks/orchestrate-service-path/default.nix:74` asserts the same wrong name. A relayed, unverified decision ledger (`flows/01a03603/reports/decisionLedger.md:39`) sides with `meta-orchestrate`. "Nothing here should be deployed until the living settles the name." Also unsettled: whether `lojix-meta` (shipped unilaterally by flow 857335) fits whatever convention is chosen.

**A17. Socket binding: does the built-in default win, or the persisted store?**
`orchestrate-followup.md` §6; `orchestrate-review.md` §3.4/D-6. Repo: orchestrate. `Vision/nexus.md` reads as if the built-in default should win for binding; the implementation lets the store win. Witnessed: a copy of a real store opened by 0.32.0 tried to bind the live socket path and was refused only because the live Nexus already held it; a durable test relies on exactly this behavior.

**A18. Is Orchestrate's engine supposed to be Kameo actors, and by what standard?**
`orchestrate-work.md` §4.4/§6; `orchestrate-review.md` §4. Repos: orchestrate, nexus. Vision: "The engine inside a Nexus is driven by Kameo actors. The standards of their use are still to be designed." No `kameo` dependency exists in the released code; a prior WIP branch declared it and used it nowhere. "Remains open. It needs the Kameo standards first." (Same open question recurs in lojix — see A19.)

**A19. Kameo fork: rebase onto upstream 0.22.2, or drop the fork for crates.io?**
`dependency-survey.md` §6 Tier 2 item 8/§5. Repo: kameo (fork) + 14 consumers. Fork at 0.20.0 (last commit 2026-08-13) vs crates.io 0.22.2; what the fork changes relative to upstream was never established — "the principal unknown blocking a kameo bump… the choice is the living's." Marked never-unattended. (Lojix's own duplicate copy was already collapsed to one crates.io reference via `[patch]`; the estate-wide fork question stands.) Related closed background: beads `primary-2d7`, `primary-746` (fork causal-anatomy spikes, closed) establish only that the fork is understood, not what to do about it.

**A20. Does the subscription/streaming design belong in a CLI at all?**
`orchestrate-followup.md` §6; `orchestrate-review.md` §1.6/D-5; `orchestrate-work.md` §6. Repos: orchestrate, Curriculum. Both CLIs read one frame and exit; the `orchestrate` skill tells agents to re-poll `Observe.Locks`, which Vision forbids. "A streaming CLI needs an output protocol for a sequence of typed values, which has not been designed; so does the question of whether the CLI is the right consumer at all, or whether the estate's followers should be Nexuses with an edge."

**A21. Discard or finish the dirty shared `orchestrate` WIP checkout?**
`orchestrate-work.md` §3/§6; `orchestrate-review.md` D-11; `orchestrate-followup.md` §5. Repo: orchestrate (`/git/github.com/LiGoldragon/orchestrate`). `HEAD` detached at 1bc55af1 (0.31.0) with ten modified files byte-identical to uncompiled WIP commit `cf0dfef2`; the working tree still builds the WIP, not the release. Now four releases behind main. "Discarding it discards whatever that flow intended to finish." Also unresolved for the sibling WIP bookmarks: `signal-orchestrate` `e3ea414c`, `meta-signal-orchestrate` `eb6df08e`, `wip-flow857335-spirit-port`/`-signal-port`, `mirror` `783be4b8`.

**A22. Should a carried (pre-0.30) store keep its ordinary bootstrap window?**
`orchestrate-followup.md` §6 item 4/§2. Repo: orchestrate. Shipped in 0.33.0 with three tests each seen failing first, but "the reading of Vision that supports it is a reading, and the living may prefer the literal record with a different remedy (e.g. a deployment that configures through the meta socket at first start)."

**A23. Is `signal-frame`'s envelope layer *the* protocol — absorbed into `signal`, or kept separate?**
`datom-migration.md` §5; `recent-vision.md` item 7; `aggregator-migration.md` ("router — not migrated, and why"). Repos: signal-frame, signal, plus ~50 dependents. Neither `signal-frame` nor `dotos` depends on protos/datom-codec/ethos-zero at all. The merge decision is explicitly deferred at `flows/fe34eb/vision/signal.md:23`. Blocks: signal-mirror/meta-signal-mirror repin (B13/B14 below), router's entire migration (B10), and ~28 repositories still floating `branch = "main"` on it.

**A24. Retiring or renaming the repositories still named for the frozen (dotos) notation.**
`datom-migration.md` §5; `aggregator-migration.md`; `stack-membership.md`. Repos: dotos, dotos-config, dotos-text-query, tree-sitter-dotos. `Vision/datom.md`: "Everything moves to Datom… no Dotos file remains… that old notation stays behind, frozen." Surviving `.dotos` files enumerated (signal-sema, message, spirit's forbidden fixture, criomos-horizon-config, CriomOS-test-cluster, tree-sitter-dotos fixtures). "Retiring those is a `repository-lifecycle` decision, not a migration step."

**A25. Do the nine schema-rust `build.rs` consumers count as "the incorrect stack" (and so frozen), or do they need active migration?**
`stack-membership.md`. Repos: harness, repository-ledger, terminal, introspect, mind, system, terminal-cell, spirit, persona. No entry in `Vision/`, `Intent/`, or `flows/*/vision/` names any of them frozen or scheduled. "This flow's inference, not a ruling I can quote." (This is the design half of C1's mechanical wall below.)

**A26. Should the Signal text projection go straight to Datom instead of resting on `dotos`?**
`stack-membership.md` per-repository table. Repos: aggregator, signal-aggregator, meta-signal-aggregator, router, dotos-text-query, signal-repository-ledger, meta-signal-repository-ledger. Grounded in the same "no Dotos file remains" ruling as A24; verdict on aggregator specifically: "Unwarranted [to keep migrating toward dotos]; raise to the psyche whether the Signal text projection should go straight to Datom instead."

**A27. Does `nexus` need to depend on `signal` and `sema`, and where does the universal actor/dataflow ontology belong?**
`recent-vision.md` item 6; `orchestrate-work.md` §4.4 #6; `orchestrate-review.md` §4 row 6. Repo: nexus. `nexus/Cargo.toml` depends on `rkyv`/`thiserror` only; 0.1.1 is 131 lines covering configuration lifecycle only, no effect/`Apply` trait, no actor or dataflow ontology, no socket/signal surface — and it postdates the runtimes it was meant to found by four and a half hours. "Whether it should [depend on signal/sema] is not settled by any vision text this flow read."

**A28. No router, no wrapping enum, no handshake payload — whose design work is this, and when?**
`orchestrate-work.md` §4.4 #7/§6; `orchestrate-review.md` §4 row 7; `warrant-audit.md` §3.3(d). Repo: signal. `signal` holds the frame, `Signal<T>`, and a `ComponentKind`/`AuthorizedObjectInterest` taxonomy, but the dispatch enum and handshake payload a router would need are absent, and Orchestrate does not depend on the taxonomy at all — "Orchestrate has no edges to any other Nexus today, so it could not have driven the design of either."

**A29. Chroma's redb 2.6.3 → 4.x: needs a storage-format migration answer, not a `cargo update`.**
`dependency-survey.md` §1.4/§6 Tier 2 item 9. Repo: chroma (a running daemon with its own on-disk state). Marked never-unattended.

**A30. The nixpkgs fork chain bump, and the fate of the GTK MR !10130 backport patch.**
`dependency-survey.md` §2.5/§6 Tier 2 item 10. Repos: LiGoldragon/nixpkgs, CriomOS-pkgs, CriomOS, CriomOS-home. Deployed fork evaluates `gtk4 = "4.22.4"`, exactly the version the nix-input-upgrade skill records as *not* containing the fix — "the backport is therefore live, not historical." Decision: drop the patch if the new revision brings ≥4.23.3, else rebase. Also unknown: the local fork clone is a broken `git` checkout, so its distance from upstream is unestablished.

### Lojix / Horizon / CriomOS

**A31. Hardware classification after horizon-rs `f1a5eca` deleted `KnownModel`/`ComputerIs`/`TypeIs`/`LidSwitchPolicy` with no replacement.**
`lojix-criomos.md` §5. Repos: horizon-rs, CriomOS. `git diff f1a5eca~1 f1a5eca` shows the deletion is "a design judgement against per-model closed-enum flags, not an oversight." `CriomOS/modules/nixos/metal/default.nix:37` still reads `modelIsThinkpad`, stopping `complete-system BuildOnly`. Three named options: reintroduce typed hardware classification, match the raw `machine.hardware.model` string, or relocate the ThinkPad/RPi behaviors elsewhere. Consequences at eleven more `metal/default.nix` lines and five checks that currently pass only by hand-writing the retired fields into fixtures (the same false-green shape already found and closed for `arch`, see B4). "Inventing a default here would silently disable every real ThinkPad's battery/thermal/lid handling."

**A32. Three more unrepaired CriomOS-home / Horizon-projection divergences.**
`lojix-criomos.md` §2.4. Repo: CriomOS-home. `min/spirit.nix:32` — `node.services` absent, silently `[]`; `min/pi-models.nix:37` + `max/browser-use.nix:56` — `node.typeIs.largeAiRouter` absent, silently `false`; `flake.nix:710` + `min/agent-intercom.nix:11` — an attrset operation (`mapAttrs`) on `horizon.users`, which is now a list. "Each changes behaviour rather than restoring it… the living has not been asked."

**A33. Should CriomOS-home check in a generated horizon fixture, or take horizon-rs as a flake input and project at check time?**
`lojix-criomos.md` §4.1 item 4. Repo: CriomOS-home. Current fixture proved byte-identical to deploy-time materialization; "a larger change and was not made unasked" if the living wants the alternative.

**A34. Unit rename `lojix-daemon.service` → `lojix.service` — keep or revert?**
`lojix-criomos.md` §4.1 item 2. Repo: CriomOS. Branch renames it "because it is a Nexus, not a daemon" (`Vision/nexus.md:5`); means an extra service stop/start on the live host at cutover. "Say if you would rather keep the name."

**A35. Should socket paths/modes/store file be `readOnly` Nix options restating the Nexus's own built-in choices?**
`lojix-criomos.md` §4.1 item 1. Repo: CriomOS. The Nexus offers no setting for any of them; agreement between the restatement and real behavior is witnessed only at runtime, not at evaluation.

**A36. Does the 2026-08-13 "I don't care about any past lojix database" ruling still hold, given the v5 cutover discards deployment history?**
`lojix-criomos.md` §4.2 step 4; `lojix-history.md` §3. Repo: lojix. The retained v4 store (`lojix.sema`) holds 100 live-set rows, 98 GC roots, 895 event-log rows, 245 deployment records that the v5 Nexus will never open (fixed basename). "If it does not [still hold], the change is in lojix (make the store file selectable, or migrate)."

**A37. The `lojix` skill's parenthesised-query syntax vs the brace form the shipped binary actually accepts — approval to edit is owed, not a technical decision.**
`lojix-history.md` §4.2/§5 W2; `lojix-criomos.md` §3.4. Repo: Curriculum. Technically settled: the deployed binary rejects the parenthesised form and accepts `Query.ByNode.{goldragon ouranos None}`; `Vision/datom.md:274` reserves parentheses for Meaning. What's owed is the standing approval for a skill edit — the proposal already exists in `skill-proposals.md`.

**A38. The `lojix` skill's `CheckHostKeyMaterial` row — the verb and its vocabulary were deleted; skill still documents it.**
`lojix-work.md` §W8. Repos: lojix, signal-lojix, Curriculum. The stub returned an empty mismatch vector unconditionally; a real implementation needs an SSH read of the live host key (an effect, not a store read) that was never designed. Proposal drafted at `skill-proposals.md` §A4.

**A39. A ninth false statement in the `lojix` skill: `proposal.datom` vs the actually-required `horizon-definition.datom`.**
`lojix-criomos.md` §3.4. Repo: Curriculum. "This flow lost two attempts to it" before discovering the correct filename.

**A40. The standing set of unanswered Lojix questions (W11).**
`lojix-history.md` §5 W11. Repos: lojix, horizon-rs, Curriculum, Vision/. Contents: 674a4dab's three questions (what criomos-core is, where Horizon's line is, how much Lojix and where a deployment request lives); 4d5fc7da's three asks (the action set, route as rule vs per-deployment choice, the Sema anatomy); whether `Vision/lojix.md` and `Vision/horizon.md` should be distilled at all ("Lojix is the most-discussed component in the corpus and has no distilled vision"); the Zeus signing/trust boundary (A41). "Looks reasonable," from the living on 2026-08-xx, is witnessed as agreement in direction, not as a ruling on each.

**A41. The Zeus signing/trust boundary, unruled since 2026-07-29.**
`lojix-history.md` §1.1. Cluster hosts / lojix. "A psyche decision is required before adding or changing any signing/trust capability… Never ruled. It is still the most likely latent cause of CopyClosure failures to Zeus." No flow has re-tested the signature gate since.

**A42. Does the living want flow 542442's `Deploy.Host` redesign at all?**
`lojix-history.md` §1.7. Repos: lojix, meta-signal-lojix. Blocked structurally on Datom having no omittable fields ("just remember datom doesnt support omittable fields yet" — psyche, `flows/4d5fc7da/vision/archive-datom.md:9`); the request has grown 13→14 fields regardless. "Unruled."

**A43. WatchDeployments: implement the subscription, or delete the whole vocabulary?**
`lojix-history.md` §4.5/§5 W7; `runtime-audit.md` §9.6 (independent confirmation). Repos: lojix, signal-lojix. `open_subscription` allocates a token inserted into nothing; `close_subscription` cannot fail so two error variants are unreachable; an exhaustive search for `broadcast`/`mpsc`/`watch::`/`Sender`/`subscriber` returns zero hits; `ARCHITECTURE.md` falsely claims the CLI streams events. "The living has never asked for `WatchDeployments`… deleting the whole subscription vocabulary and its two orphaned tables (`deployment-outbox`, `pending-transition-intent`) is as faithful as implementing it. Put both to him; do not choose silently."

**A44. `criomos-core` and `extended-horizon`: shape, and whether to build them at all.**
`lojix-history.md` §1.5/§4.7. Neither repository exists. Four open shape questions recorded at `flows/01a030a1/reports/extendedHorizonReacquisition.md:124-131`; the one strong justification named is duplicated Horizon service-variant interpretation between OS and Home.

**A45. Fate of the 26 unmerged Lojix remote bookmarks, and the three orphaned flow-542442 branches.**
`lojix-work.md` §W10; `lojix-history.md` Unknown 13. Repos: lojix, horizon-rs, CriomOS-home. Nine spent (ancestor) bookmarks were deleted; the other 26 were deliberately not, because "the remote branch is the only copy of that work" — a living's-call, not an omission. The three 542442 branches (`horizon-datom-node-542442`, `horizon-flake-integration-542442`, `home-datom-renovation-from-main-542442`) "no longer a coherent unit."

**A46. Where should the NixOS lojix module live?**
`lojix-history.md` Unknown 9/§5 W1. Repos: lojix, CriomOS. `lojix/flake.nix` exposes no `nixosModules`, which is why CriomOS's copy drifted into calling a binary that does not exist.

**A47. The "calling it lojix is bad" naming objection was never withdrawn, and the meta-CLI naming was resolved unilaterally.**
`lojix-history.md` Unknown 8/§1.7. The living objected to the name (2026-08-16), approved the skill five days later without ever saying the objection was withdrawn; flow 857335 separately shipped `lojix-meta` without the naming question ever being raised to the living. Connects to A16.

**A48. Does the release registry (`flows/857335/reports/release-registry.json`) remain the release authority?**
`dependency-survey.md` §3.1/§6 Tier 3 item 14. It lists datom-codec 0.25.6 (head is far ahead), lojix 1.0.1 (head 2.0.0/3.0.0 since), and omits `signal` entirely. "Anything reading it as the release authority is reading a month-old snapshot."

**A49. Lojix's own upgrade path is marked never-unattended — it is the deploy mechanism itself.**
`dependency-survey.md` §6 Tier 1 item 7. "A broken lojix means no way to deploy the fix." Wire compatibility across the 1.0.1→2.0.0 breaking bump is claimed by the producer commit body, not witnessed by this survey.

### Naming / authority / repository lifecycle

**A50. Which remote is authoritative for `repository-ledger` and `signal-repository-ledger`: the gitolite mirror (`origin`) or GitHub?**
`mirror-restore.md`; `push-verification.md` D1. No skill variable and no Vision/Intent/flow-vision entry rules on it. Witness: `repository-ledger` main diverges — mirror `4153fd848c69` vs GitHub `0580eff46139` — left exactly as found, both heads recorded. `push-verification.md` further found the two reports before it had the direction backwards: "what the two reports treated as the pushed authority is the local mirror, and GitHub already carries the commit they called local-only."

**A51. Naming and shape of a dedicated flows repository, and of a "static workspace" repository.**
`recent-vision.md` items 15–16. The psyche's own naming question ("Maybe you have some suggestions there") is unanswered in any file; 1510 tracked files sit under `flows/` in `/home/li/primary` with no matching GitHub repository. Separately: broaden Curriculum into the workspace repository, build a new one beside it, or revive the dormant `LiGoldragon/workspace` (created 2026-04-22, last pushed 2026-05-02, predating the statement by four months — "This flow does not know whether the psyche had it in mind").

### Skill / documentation corpus

**A52. Four skill-corpus contradictions the corpus cannot resolve itself.**
`skill-proposals.md` §18. Repo: Curriculum. (a) `vocabulary.md`'s "machine, not AI; flow, not agent" rule is violated by roughly fifteen files including `spirit.md` itself — "the rule as written condemns the highest-authority text in the corpus." (b) `documentation-placement` ("point to the document, don't restate") directly contradicts `skill-designing` ("do not add a line telling them where to look") for the same line. (c) `testing.md`'s "infrastructure reports are ground" vs `behavior.md`'s "a thing is verified only by a witness" — "if the carve-out is deliberate, one sentence… settles it." (d) "Lane" appears in `main-flow`/`subflow` descriptions but is undefined in `vocabulary.md`, which conflicts with `subflow`'s own "do not create a lane."

**A53. The Sol contradiction: `AGENTS.md` forbids what `roles.datom` and the generated `.codex/agents/*.toml` mandate.**
`skill-proposals.md` §14a; `recent-vision.md` item 13. Repos: primary (`AGENTS.md`), Curriculum (`roles.datom`). `roles.datom` assigns `gpt-5.6-sol` to the demanding depths and the generated `worker.toml`/`write-demanding.toml`/`read-demanding.toml` carry `model = "gpt-5.6-sol"`, while an `AGENTS.md` section (absent from `CLAUDE.md`) forbids Sol for subagents outright. "One of the two is wrong and only the living can say which."

**A54. Whether `skill-proposals.md`'s body (~60 deletions, three whole-skill replacements, ten addendum proposals) is approved.**
`skill-proposals.md` (entire file); `log.md` Wave 1/4. Repo: Curriculum. Nothing in it was applied — "skill edits require the living's explicit approval after proposal," per standing order. This is not a design question in the ordinary sense (the audit-agent's synthesis calls it "neither A nor C: a class of complete work sitting behind a standing yes/no gate") but is listed here because only the living can supply that word. Two rows (`spirit.md`, both in §16b) are flagged for wording review even where the ground is clear, because spirit is philosophy.

**A55. Where should the `Intent/mandatoryTraits.md` traits-first-for-Rust rule live: a new `rust` skill, a line in `spirit`, or an entry-file line?**
`skill-proposals.md` §9e. "Creating a new skill is a larger decision than a line edit and the living should choose."

**A56. Should the harness itself be reconfigured to wake only on "Send to Claude," making a proposed skill line unnecessary?**
`skill-proposals.md` §2. "If the harness itself can be configured [that way], that is the better fix and the line is unnecessary — that question is for the living."

**A57. Should the entry files keep the `psyche`-search duplication, or defer entirely to the skill?**
`skill-proposals.md` §14b. "The entry file is middle stratum and always present, while the skill is loaded only when the flow loads it… This flow does not know which was intended."

**A58. Is the `Vector<Integer>` adjacency-scanner split (ethos-zero's four-scanner workaround) a design to document, or a defect to fix at the source?**
`skill-proposals.md` §6 "Known trap, deliberately left out." Cross-reference to A4/A13. "If the living rules that the split stands, one line belongs in the protos skill and the ethos skill's spacing section."

**A59. A bare enum variant spelling a declared type name becomes a payload variant — intended or not?**
`aggregator-migration.md` "Two findings the generator forced." Repo: ethos-zero. `OperationKind.[ Configure ObserveConfiguration ValidateConfiguration ]` generated `ObserveConfiguration(ObserveConfiguration)` because a type of that name was also declared. "Whether that is intended is unknown to this flow; it is recorded as observed behavior, not as a defect."

---

## (B) Pushed `f6db8d-*` test branches awaiting the living's word — 22 items

All revisions independently verified against real GitHub in `push-verification.md` via `git ls-remote https://github.com/LiGoldragon/<name>.git` (URL derived from the repository name, never from a checkout's `origin`, after a `git clone --shared` mistake had repointed some checkouts' origins at local paths), plus a further live sweep across all 188 repos that found six additional branches no report tables.

**B1. CriomOS-home — `f6db8d-removals`, `4cb132ec04ecf550bfc9a6b0d14a71cf6806889f`.**
Removes fzf orphans, the dead `primary-generated-src` flake input, the dead compositor stack (hyprland/sway/waybar), two dead assert arms in `checks/keyboard-layout-policy`. Landing note (`removals.md`): "Not landed — the brief for CriomOS-home items is explicit: test branch only, never land, never deploy. Ready for a human or a deploy-authorized flow to open a PR whenever wanted." Witness: home-generation activation derivation byte-identical before/after.

**B2. terminal-cell — `f6db8d-removals`, `f572839e1d152936238c009a2552a079f2cef1a6`.**
Drops the dead `dotos-text` feature (zero `#[cfg(...)]` sites reference it); removes seven stray `result-N` symlinks. Landing note: gate partially blocked by pre-existing, unrelated breakage in sibling repos `terminal` (self-contradictory `[patch]` block, 17 uncommitted files) and `mentci` (unresolved `schema_rust::bootstrap::BootstrapInterfaceGeneration` import — same family as C1). `nix flake check` in terminal-cell itself is green. "A version bump was withheld along with the landing — bump when this lands."

**B3. CriomOS — `f6db8d-lojix-start`, `c4c830c10d32e15c6afc055383ca49fef95963fd`.**
Rewrites `modules/nixos/lojix.nix`: `ExecStart` becomes the pinned package's `lojix-nexus` with no argument; socket paths/modes/store file become `readOnly` options; unit renamed `lojix.service`; new VM test `checks/lojix-nexus-start`. Landing note (`lojix-criomos.md` §4.2): needs the lojix repin first (the declared pin, `23f09f28`, does not compile — see C-item on the dup `meta-signal-lojix` lock entries) and was blocked behind Orchestrate lock 1123 on `CriomOS/flake.lock`. Design questions A34/A35 attach to this branch. Witness: red-green on the argument change; VM test boots, both sockets bind, one live `Query.ByNode` answers `Queried.{ [] [] { 2 2 } }`, built only via a transient `--override-input` to a buildable lojix revision because the declared pin does not compile.

**B4. CriomOS-home — `f6db8d-lojix-start`, `0176de5f6d9a4a9111adebbff5e2480d31a6dd06`.**
Fixes `min/default.nix:240`'s `machine.arch == "X86_64"` against the producer's actual `machine.architecture` (lowercase); adds a checked-in `fixtures/horizon-projection.json` regenerated from the real producer, closing a false-green on two dependent checks. Landing order: land CriomOS-home before CriomOS (CriomOS pins Home by revision). Blocked downstream by A31's `modelIsThinkpad` stop. Witness: evaluation error → 127 packages resolved; fixture proved byte-identical to deploy-time materialization; both dependent checks proven red on the old field.

**B5–B9. Five `f6db8d-cargo-update` branches, all FAILED-and-parked on the same `nota` cause.**
`cargo-update-tier0.md`; `nota-pins.md`. Repos and revisions: aggregator `7ef8d506e1390726b6d321c5ec2da5bd176e0e34` (now stale — aggregator landed 0.4.0 on main separately, `nota-pins.md`); harness `d28634c26cd56b1b8c701d7c7f830923a56d9b57` (still valid — blocked on C1); router `f15220b0d4bcd83356e6f1e2e3667e0f51689045` (still valid, blocked on C1); listener `04137484445b80ac2c36f419750685b7856a04cf` (still valid, blocked on C1); repository-ledger `0c9bd81bde7bdf7628c03c96a46217033620a653` (was GitHub-absent per `push-verification.md` D2, **since restored to GitHub** by `mirror-restore.md`; still depends on A50). All five are empty commits recording `error: no matching package named 'nota' found` against a mutable `branch = "main"` git dependency whose current HEAD no longer defines that package.

**B10. router — `f6db8d-nota-pins`, `5fa990dc7f62629cafe08998691b5851f0f0a5e3`.**
Completes router's full Dotos migration (nine `branch = "main"` pins converted to `rev =`). Landing note: `aggregator-migration.md` ran `cargo metadata` on it directly and found it cannot resolve (a `links = "signal-persona"` conflict) — "router's main resolves cleanly. **The Dotos branch is strictly worse than main and must not land.**" Also the wrong direction per A24/A26 (Dotos is the frozen notation). Checkout was moved back to main so nobody builds on it by accident.

**B11. signal-repository-ledger — `f6db8d-nota-pins`, `9d267c275df7d2f9db800196465a7dd50ec38623`.**
Found-in-tree Dotos migration finished and gated fully green (fmt, clippy `-D warnings`, test, doc, `nix flake check`); 0.1.0→0.2.0. Landing note: blocked on A50 (main divergence). Mirror-side corruption from an earlier push (D3 in `push-verification.md`) has since been repaired by `mirror-restore.md` — both remotes now agree on `main` and both carry this branch.

**B12. meta-signal-repository-ledger — `f6db8d-nota-pins`, `0c2da541ccb65217cb5b112b85e3790bac0e9293`.**
Same migration, same full-green gate, 0.1.0→0.2.0. Held for B11's blocker (A50).

**B13. signal-mirror — `f6db8d-datom-migration`, `4c6765fa6310cec7cf57a7b6b067371ae6ddd456` (2.0.0).**
Repins to the substrate/Ethos-Zero heads of that night. Landing note: test RED, clippy RED (fmt/doc/`nix flake check` green) because its one Signal dependency, `signal-standard`, renamed its own package to `signal` on main in the same window, leaving two `datom-codec` versions in the graph — blocked on A23 (`signal` is under a sibling lock). **Likely superseded**: `signal-mirror` main has since landed 2.0.1 at `e60b7667` via the consumer sweep; this branch may be stale residue rather than a live pending item — worth a fresh check before acting.

**B14. meta-signal-mirror — `f6db8d-datom-migration`, `b269cedab413ece432dcf1922397118e2dbe65fe` (2.0.0).**
Same repin, same cause, same blocker (A23). **Likely superseded** by main 2.0.1 `adf6be61`.

**B15–B16. signal-spirit-judge and meta-signal-spirit — `f6db8d-sweep`.**
`cb9f0a790896bf0eda2db71ff8c0a74c8488e8a2` and `ab23db0b0ca8c784cc7728251cae6bf4982d2bad`. Partial repin work parked mid-sweep on a cross-consumer version conflict, then re-dispatched once blockers cleared. **Both are now residue**: `push-verification.md` confirms both branches exist on GitHub, but main for both has since landed correctly (signal-spirit-judge at `5e7764ea`; meta-signal-spirit at `7ba0f82`, 3.0.1, after a version-label mismatch was separately corrected). Safe to delete, not pending a ruling.

**B17. signal-introspect — `f6db8d-sweep` — claimed in a report but does not exist.**
`push-verification.md` D6: "signal-introspect's complete GitHub ref list carries no such branch… the claim is wrong for one of the three." Not a live item; noted as a correction to an earlier report's own record.

**B18–B21. Four further `f6db8d-datom-migration` branches found only by a live `git ls-remote` sweep, not tabled in any report.**
signal-introspect `5b36271698ee1a40347d63b96790afaa22dd30b8` (superseded — this is the pre-migration state; main has since landed 2.0.1 `8de16e3`); signal-spirit `bd95898e655671dc3174da24b698f6dddefa075d` (main landed separately at `c1d78e85`→`d13ddcea`, this branch not narrated in any report); signal-spirit-judge `74e713f9bee0333c7fb119cf5bcbaf8d32d9282d` (main landed `f9da94e3`→`5e7764ea`, not narrated); meta-signal-terminal `a2bb6e55a78bc7fb937381f6b54c840519548f7d` (main landed `3d0eafa1`→`a9b18ee8`, not narrated). All four appear to be residue from landed work rather than pending decisions, but nobody has swept or deleted them, and their exact relationship to what landed on main was not independently re-verified by this compiling subflow.

**B22. Not test branches, but WIP the living has never been asked to discard: the three-plus pre-flow-f6db8d bookmarks from flow 857335.**
orchestrate `cf0dfef2` (= A21's dirty checkout target), signal-orchestrate `e3ea414c`, meta-signal-orchestrate `eb6df08e`, `wip-flow857335-spirit-port`, `wip-flow857335-signal-port`, mirror `783be4b8` (does not compile as of the periphery audit — see C-item on mirror WIP below). "It needs the living's word, since discarding it discards whatever that flow intended to finish" (`orchestrate-work.md`).

---

## (C) Unfinished work needing no ruling, just doing — 46 items

### Blocked on mechanics, not judgment

**C1. The schema-rust emitter wall blocks nine repositories.**
`nota-pins.md`. Repos: listener, repository-ledger, terminal, introspect, harness, mind, system, terminal-cell, spirit, persona. The Nexus daemon emitter and the contract-crate emitter (`ContractCrateBuild`, `CargoSchemaMetadata`, `DependencySchema`) were removed from `schema-rust`'s main on 2026-08-06; every revision that still exports them pins the unresolvable `nota` at `branch = "main"`. `Cargo`'s `[patch]` cannot redirect a git source to a different revision of the same source (tried on harness, refused). Unblock order given: (1) restore/replace the two emitters on schema-rust's main against `dotos`; (2) regenerate `signal-mind` against `signal-persona` 0.3.1 (a bare repin produced 195 compile errors — this is contract regeneration, not a repin); (3) migrate `signal-listener`/`meta-signal-listener`; (4) resolve the repository-ledger main divergence (A50) and land B11/B12. Sibling f6db8d subflows already hold Orchestrate locks 1126–1131 on this — known, owned work in flight, not an unresolved discovery. Bead `primary-hqu.14` (open) already tracks the spirit slice of this wall.

**C2. `curriculum-deploy`'s Datom migration is held under flow 542442's Lock 851.**
`skill-regeneration.md`. Repos: curriculum-deploy, Curriculum. Held over worktree `/home/li/wt/…/curriculum-deploy/datom-codec-542442`, not the main checkout. `curriculum-deploy`'s `Cargo.lock` still resolves datom-codec 0.25.6 / protos 0.29.1.

**C3. Skill regeneration is blocked behind C2 — `main-flow`, `design`, and `realization` remain agent-loadable on Claude.**
`skill-regeneration.md`; `recent-vision.md` item 3. Repos: primary, Curriculum, curriculum-deploy. `roles.datom`'s typographic quotes plus a mid-sentence `;` make it unparseable by the pinned protos (`Error.{ … Unclosed.«{» }`, reproduced and isolated to the semicolon). The fix itself is already pinned and waiting: `curriculum-deploy`'s generator already emits `disable-model-invocation: true` at a commit `flake.nix` already pins; regenerating "applies only the generator's frontmatter change." One open sub-question that is not a ruling, just unanswered: whether Codex's `allow_implicit_invocation: false` also blocks *explicit* invocation of a skill by name, or only description-matched auto-invocation — untested.

**C4. `terminal` and `mentci` are independently broken, unrelated to any of tonight's changes.**
`removals.md` §4. `terminal`: 17 uncommitted files plus a self-contradictory `[patch."…signal-terminal.git"]` block. `mentci`: fails in a transitive `build.rs` on an import the schema-rust wall (C1) already removed. This is what keeps B2 from landing cleanly and blocked C1's `terminal-cell` cargo-update attempt (Orchestrate lock 1124, since released).

**C5. `CriomOS/checks/orchestrate-service-path` fails on the `Configured` reply shape independent of the binary-name question.**
`orchestrate-review.md` §3.2/D-3; `orchestrate-followup.md` §5. Repo: CriomOS-home. The check asserts a literal string for the old reply shape; the meta reply is now a `ConfigurationReceipt` with a different shape entirely. "Fixing the binary name alone [A16] leaves the check red." A separate, purely mechanical correction once A16 is settled.

**C6. `Curriculum/skills/orchestrate.md` and its four generated copies still teach curly quotes; the installed binary requires guillemets.**
`orchestrate-review.md` D-2; `orchestrate-followup.md` §4. Repo: Curriculum. Witnessed both directions (0.32.0 refuses `"curly quoted"` with `Unreadable.Error…`, requires `«guillemets»`). "Every agent in the estate taking a multi-word-reason Lock breaks on deploy day." Fix already drafted in `skill-proposals.md` §7; purely mechanical once approved (needs no ruling — code is already the decided authority here, only the skill text is stale). The `datom` skill has the identical defect (`datom-migration.md` §2).

**C7. Two leaked Orchestrate locks (1111 `LojixNexusHardening`, 1112 `HorizonRsNoFreeFunctions`) blocked two consumer sweeps all night.**
`push-verification.md` D5. `lojix-work.md` reports all four of its repositories released and verified, yet never records acquiring or releasing either lock. Release was subsequently authorized to a lojix-settle subflow, which was to repin lojix/horizon-rs to final heads.

**C8. The aggregator correction is half-landed — contracts moved to Datom, consumer's own final revision unverified.**
`push-verification.md` D4; `aggregator-migration.md`. Repo: aggregator (+ signal-aggregator, meta-signal-aggregator, both fully migrated and gated green). Lock 1193 is recorded released and the report is no longer a stub, but `aggregator-migration.md` carries no revision table for `aggregator` itself and its gate is relayed from another subflow rather than witnessed directly here. What remains: obtain and verify aggregator's landed `main` revision against GitHub the way `push-verification.md` did for everything else.

**C9. `unreachable!()` sites and orphaned traversal duplication.**
Fifteen production `unreachable!()` sites remain in lojix's `schema_runtime.rs`/`lib.rs`, several of which panic the Nexus on a store-write error (`lojix-work.md`). Sixteen equivalent sites in datom-codec were already closed (`log.md` Wave 1). `src/projection.rs` in datom-codec still duplicates protos's canonical byte-length formulas keyed by a `HashMap` of raw pointer addresses, with "nothing keeping them agreeing" (`substrate-review.md` §4.3) — and `unused-survey.md` §4.1 found the formula is **already wrong for one arm** (`Angled: protos=6, formula=8`), with a concrete gate proposed (promote the differential test to assert every extent, not just the root).

**C10. `DeploymentPipeline::phase_event`'s `_detail: Option<String>` is discarded for non-terminal transitions.**
`lojix-work.md`. Repo: lojix. Only the terminal transition carries detail through `optional_deployment_terminal`.

**C11. `CopyClosure` still maps to the generic `BuilderUnreachable` reason.**
`lojix-work.md`; `lojix-history.md` §1.8/§4.3. Repo: lojix. Historically produced misleading diagnosis (deployments 158/162: "No route to host" reported as builder-unreachable when Prometheus was never unreachable). Evidence is now attached to mitigate, but the reason itself is still generic. Connects to A41 (Zeus trust).

**C12. lojix's `same-host-test-activation` VM fixture is stale against the `NodeDefinition` shape horizon-rs itself now requires.**
`lojix-criomos.md` §3.3/§4.3. Repo: lojix. The embedded proposal has 10 fields; horizon-rs `8f4240ef` requires 11 (`fixed_location_option` added) and refuses with `Arity { expected: 11, found: 10 }`. "That check cannot be green at the revision lojix itself pins. Recorded, not fixed — it is a lojix change." Not mentioned as resolved in `lojix-work.md`.

**C13. The real cluster proposal's parse failure is only partly re-verified as fixed.**
`lojix-criomos.md` §3.3. Repos: protos, goldragon, criomos-horizon-config. The guillemet-escape writer defect that caused the original failure is fixed and released (protos 0.30.0), but no report re-parses `goldragon/proposal.datom` at the new protos version, and horizon-rs would need repinning first. Separately, `criomos-horizon-config/horizon.dotos` is refused for an unrelated reason (still pre-Datom parenthesised form) and the local checkout is stale relative to its own `origin/main` (C14).

**C14. `criomos-horizon-config`'s local checkout is stale and holds a retired file.**
`lojix-history.md` §4.9. Local `e222d3a` still holds `horizon.dotos`; `origin/main` `74a4ad3` holds `horizon-configuration.datom`. "Any agent reading the checkout reads a retired file."

**C15. `CriomOS` complete-system `BuildOnly` still does not reach `BootstrapTerminal.Succeeded`.**
`lojix-criomos.md` §3/§5.3. One stop is a fixture inadequacy (a `Live`-node run fails on `boot.loader.systemd-boot.enable`); the other is A31 (`modelIsThinkpad`). "The materialization path itself works end to end," which is the one clean positive result.

**C16. The CriomOS lojix pin (`23f09f28`) does not compile; the cause is understood and fixed upstream, only the repin is unlanded.**
`lojix-criomos.md` §1.4/§4.2. Repo: CriomOS. Duplicate `meta-signal-lojix 2.3.0` `Cargo.lock` entries resolving to two different datom-codec versions; lojix `main` `fab60e58…` (and the later released 3.0.0 `48f637e8…`) carries a single, correct entry and builds clean with all checks green. The repin was blocked on Orchestrate lock 1123, not on judgment.

**C17. `terminal-cell`'s `cargo update` never ran.**
`cargo-update-tier0.md`. Blocked by `LockRejected.PathOverlap` against lock 1124 (`f6db8dRemovalsTerminalCell`), since released per `removals.md`. Outstanding for a future attempt.

### Bookkeeping / residue, no ruling required

**C18. `meta-signal-spirit`'s version label came apart from its revision for one commit — corrected, but the intermediate commit is permanent on GitHub.**
`consumer-sweep.md` §7/§8; `push-verification.md` D8. Corrected 3.0.0→3.0.1 at `7ba0f82`; no push problem, just a permanent record of the gap.

**C19. `signal-standard`/`signal` package-name collision — recorded, deliberately untouched.**
`consumer-sweep.md` §7. A known architectural collision (a repository rename that turned out to be a rename of the repository, not merely the package) that this sweep repinned through exactly as an earlier flow left it.

**C20. Three `orchestrate`-family commit messages mislabel ethos-zero `da585049` as "7.0.1" (it is 8.0.0).**
`push-verification.md` D9. Pinned revisions are correct and on GitHub; only pushed commit-message prose is wrong, deliberately not rewritten (rewriting pushed history is worse than the label error).

**C21. `harness`, `message`, and `clavifaber` each carry two "landed on main" revisions from two different subflows, neither naming the other.**
`push-verification.md` D7. All verify as ancestors of each other, so nothing is false — "recorded so a reader of any one report does not take its revision for the current head."

**C22. `signal-mirror`/`meta-signal-mirror` `f6db8d-datom-migration` branches (B13/B14) and the two `f6db8d-sweep` branches (B15/B16) plus the four newly-found `f6db8d-datom-migration` branches (B18–B21) are likely stale residue from landed work and could be deleted after a fresh check.**
Synthesized from `push-verification.md` and the live `git ls-remote` sweep; see B13–B21 above for detail. No ruling needed, just a sweep-and-delete pass once someone confirms each corresponding `main` is ahead.

**C23. `datom-codec` 0.26.0's commit is missing its `Co-Authored-By`/`Claude-Session` trailer.**
`datom-codec-fix.md`; flagged again in `substrate-review.md` §6 as "worth the main flow's eye." Pushed before the omission was noticed; rewriting pushed history was judged worse than leaving it. Record-only.

**C24. `#[rustfmt::skip]` lands inconsistently across multi-item generated groups.**
`ethos-zero-fix.md` §6; re-confirmed present in committed contract evidence by `substrate-drift.md` (four consecutive un-skipped items in `protos.rs`). "Bites only when rustfmt is first run over a generated file" — latent, not yet active.

**C25. `repos-manifest.dotos` is stale: 70 on-disk repositories (including protos, datom-codec, ethos-zero) are absent from the "authoritative inventory."**
`unused-survey.md` §1. Already tracked by bead `primary-xqb.8.8`.

### Removal / hygiene items already identified, some already actioned, some pending a sibling lock

**C26. Dead binaries and dead test code flagged but not removed (items 5–6 skipped in the removals pass because a sibling held the lock).**
`unused-survey.md` §2. `orchestrate-store-migrate` CLI wrapper (no consumer greps to it anywhere in CriomOS/CriomOS-home); `harness-claude-session-stream-test` (479 lines) and `harness-claude-artifact-observer-test` (145 lines), "624 lines that crane compiles into every harness package build and nothing ever runs" — one open sub-question, whether an existing flake check already supersedes the first of the two, was not verified.

**C27. `CriomOS-home/modules/home/profiles/min/pi-models.nix` is a real bug, not cruft — do not remove.**
`unused-survey.md` §2.5. It declares `home.activation.mergePiModels` and is silently not imported, so the pi model-config merge does not run on this machine. "The fix is to import it," not delete it.

**C28. `agent-intercom-fleet-cleanup.timer` has failed 329 times in 7 days.**
`unused-survey.md` §3. Not Nix-managed. Fires every 15 minutes, exits 1 immediately on a `MODULE_NOT_FOUND`; expired Agent Intercom worker cgroups are not being reaped at all. "It is the only failing unit on the machine." A straightforward repair.

**C29. Two live bugs found in the periphery, each with an owner named.**
`unused-survey.md` §4.2. (a) Orchestrate frames little-endian while everything else built on `signal` is big-endian — any `signal`-based client pointed at an Orchestrate socket misreads frame length. A cross-crate test is proposed. This appears to be **fixed** by `orchestrate-work.md` ("Framing now through the shared signal crate (big-endian)") — worth a one-line re-check that the fix actually reached the byte order the audit flagged. (b) Three coexisting `datom-codec` pins across the estate wrote different text (bare vs guillemet-quoted); largely resolved by the consumer sweep landing 0.26.3 broadly, but not verified as fully unified.

**C30. `mirror` WIP (`783be4b8`) does not compile.**
`periphery-audit.md` §2/§3. 23 errors reproducing an earlier capture; references old schema-rust generator identifiers the pinned producers no longer export; introduces a forbidden compatibility-path feature flag (`dotos-text = ["datom-cli"]`). Marked deprecated on main; this WIP sits alongside B22.

**C31. `spirit` WIP (`5c53df2a`) is a large (+7253/-4682) unmerged branch of a deprecated repository.**
`periphery-audit.md` §2. A workspace split, a typed signal migration, a v15 store migration, a zero-argument daemon, and new fixtures — "the single largest investment in the slice," parked, not an ancestor of main.

**C32. `spirit` and `spirit-judge` are running services, 33/14/3/11 commits behind their own contract producers, while marked deprecated on main.**
`dependency-survey.md` §3.5. "That tension belongs to the main flow, not to this survey." Bead `primary-mo6` (closed) only established that spirit binds as a skill / tenets is retired — the operational tension itself is untouched.

**C33. Two unconcluded `jj` workspaces and orphaned build cache.**
`process-audit.md` §7. `/home/li/wt/{spirit,mirror}/deprecation-857335` remain live jj workspaces reporting their colocated git main "behind by 1 commit"; `/home/li/.cache/flow857335-audit-builds` holds 201 MB with no owner. (Separately, this flow's own removals pass freed 57 GiB of orphaned worktree `target/` output and 13 MB of other residue — already done, `log.md` Wave 2.)

**C34. `AGENTS.md` and `CLAUDE.md` have diverged on the skill-loading authority rule.**
`process-audit.md` §8. The rule was added to `CLAUDE.md` (commit `ff89e5575`) and never added to `AGENTS.md`; Codex reads `AGENTS.md` only, so every Codex flow is currently exempt without knowing it.

**C35. Six green claims across various reports carry no witness of any kind; several reports have evidence-shape lapses (missing `## Sources`, sections appended past it, a 0-byte log cited from `/tmp`).**
`process-audit.md` §3/§9. Listed for whoever audits process quality next; not this flow's to fix retroactively, but nothing here needs the living either.

**C36. The Sol auditor's (a prior "skeptical shutdown") findings sat unharvested in a transcript, though independently re-confirmed by the substrate audit.**
`process-audit.md` §4. "This is the most consequential process failure in the flow… A defect the flow's own gates missed, which the audit the living ordered actually caught, was discarded." All three findings were independently re-confirmed elsewhere (substrate-audit.md §1.2/§1.3/§1.5) so no defect is currently unaddressed — this is a process note, not open work.

### Dependency tiers (ordering already specified; no ruling needed to execute)

**C37. Tier 0/1 dependency updates specified but not yet executed.**
`dependency-survey.md` §6. Remaining: datom-codec re-pin sweep for claude-answers/signal-terminal/signal-upgrade/meta-signal-terminal/meta-signal-upgrade; fenix toolchain bump to 2026-09-09 (gate by building the lojix group and chroma first); repository-ledger 0.2.0→0.4.1; orchestrate and lojix pin bumps in CriomOS. "Tier 1 — do next, attended, one at a time."

**C38. 205 mutable `branch = "main"` pins across 43 repositories — the root cause behind several of the B-branch failures and the periphery's stale-consumer findings.**
`dependency-survey.md` §3.4; connects to B5–B9, A19 (kameo), and `periphery-audit.md` §6. "Converting them to immutable revs is the precondition for ever surveying this estate cheaply again."

**C39. `niri-flake`'s 14-month-old module schema against a running 26.04 compositor — untested, not yet a known defect.**
`dependency-survey.md` §2.5/§6 Tier 2 item 11. "Whether the 2025-07 module schema still covers everything 26.04 accepts was not checked."

**C40. Several uncommitted / unclaimed dirty trees noticed in passing, none touched by this flow.**
`recent-vision.md` Part F. `mind` (21 modified files, HEAD six weeks stale); `signal-forge` (modified `ARCHITECTURE.md`/`Cargo.lock`); `Curriculum` (a deleted `result` symlink); `/home/li/primary` itself carries two uncommitted submodule deletions under `flows/da223f/joint.0jZ7PT` (visible in this session's own git status at the top of this flow). "None of these belongs to this flow and none was touched."

### Substrate/wire quality items, closed but worth confirming stayed closed

**C41. D1/D2 (no drift check on committed contracts vs. their generator) and D5/D6 (traversal duplication; unreachable Arity refusal) — closed by `substrate-drift.md`.** Listed so they are not reopened by mistake.

**C42. The recursive-type limitation Ethos Zero's Signal root has for rkyv — consequence already shipped, root cause not fixed.**
`aggregator-migration.md`. Repo: ethos-zero. A minimal recursive Signal fails to compile under rkyv 0.8 (`overflow evaluating the requirement Vec<T>: Archive`); `dotos-text-query` works around it by hand with `#[rkyv(omit_bounds)]`, which Ethos Zero emits for nothing. The consequence already shipped without a ruling: `TranscriptBlockTextQuery`/`TranscriptBlockSearchEvidence` were redesigned from trees into flat node arenas because the tree form cannot cross this wire at all. Fixing the generator itself (emitting the needed rkyv attributes) is unfinished work, not a design question.

**C43. `sema-engine`'s real subscription surface (`subscribe`, `SubscriptionSink`, `SubscriptionDelta`) is unused; Orchestrate announces over a bare `tokio::sync::broadcast` instead.**
`orchestrate-work.md` §6. "Worth revisiting when the actor design lands" (i.e., after A18/A19 are settled) — until then it needs no ruling, just noticing it exists.

**C44. Two client `main.rs` files in orchestrate remain near-duplicates (~190 lines each).**
`orchestrate-work.md` §6; `orchestrate-review.md` §2. The defect this mattered most for (framing double-application) is already gone since framing now comes from `signal`. A shared client library would be a fourth crate, out of scope for any brief so far.

**C45. Three low-severity Orchestrate defects, open, no ruling needed.**
`orchestrate-followup.md` §5. D-8: `ConfigurationRejection`/`ConfigurationRejectionReason` declared redundantly in both `signal-orchestrate` and `meta-signal-orchestrate` despite the meta contract already importing shared types. D-9: `Admitting::admitted` answers from a socket-agnostic trait, correct today only because `SocketAuthority::Ordinary::admits` is unconditionally true — a third authority would break it silently. D-10: `ConfigurationRejection` no longer names which configuration it refused, a loss of diagnosability.

**C46. The INCIDENT (21-second live-service outage from a `pkill -f` collision) is already remedied operationally; a generalized fix is drafted but not landed.**
`orchestrate-review.md`. Service restarted, store and locks intact, no data loss. A `testing`-skill proposal ("kill by PID, never by pattern") already exists in `skill-proposals.md` and needs only the standing approval (folds into A54), not a fresh ruling. Separately, the incident's own root-cause observation — nothing distinguishes a production Nexus process from a scratch copy at the same store path — has no dedicated remediation task open anywhere in the reports; it was carried forward only as part of A17 (socket binding).

---

## Cross-cutting notes

- **Group B is entirely absent from the five original read-only audits** (warrant/substrate/runtime/periphery/process) — those pushed no branches. All of Group B comes from the overnight work reports that followed the audits, in the same flow.
- **Several A- and C-items from the original five audits were closed during the overnight wave**: Query-vs-Request naming (A-item, closed), the artefact-Datom-freedom check (closed), protos's orphaned test files (closed, 49 tests now run), sixteen `unreachable!()` sites in datom-codec (closed), the drift-check gap D1/D2 (closed), traversal duplication D5/D6 (closed). Each is marked above rather than dropped, so the delta from the original audits is visible.
- **One unresolved discrepancy this compiling subflow did not adjudicate**: whether Lojix's own half of W9 (no-free-functions / no-inherent-methods) is done. `log.md` Wave 4 states "W3 failure evidence, W8, W9, W10 done" against lojix 3.0.0 `48f637e8` with all gates green (including two NixOS VM tests, run against the exact landed revision). But `lojix-work.md`'s own §W9 section ends with the line "### lojix — delegated, outcome below" and nothing follows it — no closing statement confirms lojix's own completion, only horizon-rs's (0.10.0, confirmed green). `runtime-audit.md` independently counted ~112 module-level functions and 19 identity-ZSTs in lojix at the pre-fix revision. Treat this as unconfirmed pending one `grep` over the current lojix `main`, not as settled either way.
- **A class that is neither A nor C**: the whole of `skill-proposals.md` (full replacement bodies for the ethos/datom/protos skills, ~60 deletions across ~20 skills, ten further addendum proposals) and any Vision distillation this flow drafted are complete work sitting behind the standing rule that skill edits and Vision edits need the living's approval before landing. They need no further design ruling and no further labor — only a yes, itemized as A54 above.

## Sources

- `/home/li/primary/flows/f6db8d/log.md`
- `/home/li/primary/flows/f6db8d/reports/warrant-audit.md`
- `/home/li/primary/flows/f6db8d/reports/substrate-audit.md`
- `/home/li/primary/flows/f6db8d/reports/runtime-audit.md`
- `/home/li/primary/flows/f6db8d/reports/periphery-audit.md`
- `/home/li/primary/flows/f6db8d/reports/process-audit.md`
- `/home/li/primary/flows/f6db8d/reports/protos-fix.md`
- `/home/li/primary/flows/f6db8d/reports/datom-codec-fix.md`
- `/home/li/primary/flows/f6db8d/reports/ethos-zero-fix.md`
- `/home/li/primary/flows/f6db8d/reports/substrate-repin.md`
- `/home/li/primary/flows/f6db8d/reports/substrate-drift.md`
- `/home/li/primary/flows/f6db8d/reports/substrate-review.md`
- `/home/li/primary/flows/f6db8d/reports/producer-settle.md`
- `/home/li/primary/flows/f6db8d/reports/datom-migration.md`
- `/home/li/primary/flows/f6db8d/reports/orchestrate-work.md`
- `/home/li/primary/flows/f6db8d/reports/orchestrate-review.md`
- `/home/li/primary/flows/f6db8d/reports/orchestrate-followup.md`
- `/home/li/primary/flows/f6db8d/reports/stack-membership.md`
- `/home/li/primary/flows/f6db8d/reports/lojix-history.md`
- `/home/li/primary/flows/f6db8d/reports/lojix-criomos.md`
- `/home/li/primary/flows/f6db8d/reports/lojix-work.md`
- `/home/li/primary/flows/f6db8d/reports/dependency-survey.md`
- `/home/li/primary/flows/f6db8d/reports/nota-pins.md`
- `/home/li/primary/flows/f6db8d/reports/cargo-update-tier0.md`
- `/home/li/primary/flows/f6db8d/reports/consumer-sweep.md`
- `/home/li/primary/flows/f6db8d/reports/aggregator-migration.md`
- `/home/li/primary/flows/f6db8d/reports/mirror-restore.md`
- `/home/li/primary/flows/f6db8d/reports/push-verification.md`
- `/home/li/primary/flows/f6db8d/reports/removals.md`
- `/home/li/primary/flows/f6db8d/reports/unused-survey.md`
- `/home/li/primary/flows/f6db8d/reports/recent-vision.md`
- `/home/li/primary/flows/f6db8d/reports/skill-proposals.md`
- `/home/li/primary/flows/f6db8d/reports/skill-regeneration.md`
- `bd search` over the primary Beads database (30+ term queries), run 2026-09-11, for cross-reference only — no bead was found to close or duplicate any item above.
- Five parallel `read-demanding` research passes over the above files (this session), each independently reading its assigned subset in full; one pass (covering the five original audits) was resumed once to obtain its complete list after its first reply arrived as a diff against unseen prior context.
