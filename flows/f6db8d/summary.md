# Flow f6db8d — summary

Claude Code main flow, 2026-09-11 evening through 2026-09-12 morning. Two orders from the living: first "remember 857335. Audit everything - even auditing the very idea of even having bothered to touch some of those repos"; then, going to bed, an overnight brief to find and prioritize by recent vision, implement, audit, move dependencies up, review skills as proposals, reduce code, remove unused things on test branches, and finish what earlier sessions left undone on Lojix, asking no questions.

Every report named below is in `reports/`; witnesses in `witnesses/`. Every subflow's claim is the subflow's; what this flow verified itself is said so. Nothing was deployed all night; no running service was reconfigured. One live service was killed for 21 seconds by a subflow (see Incidents).

## Part one — remembering and auditing 857335

1. **Remember (read-demanding)** — depth one over 857335's eighteen reports, its last model response ("the whole-stack audit is incomplete"), and parent 564f55's psyche records. Found Intent/mandatoryTraits.md in the audit digest but not in 564f55's landing, and Vision/flowNexus.md the reverse.
2. **Dirt commit (write-trivial)** — pre-existing dirt committed as 90f567b9; swept in this flow's log and an fe34eb report; the two submodule deletions under flows/da223f were never staged by jj and remain in the tree.
3. **Warrant audit** (`warrant-audit.md`) — three repositories were named in an order, twenty-two were changed; the clause "update every consumer" was 564f55's, and its object "of these" was dropped before the prompt was sent; spirit/mirror work was invented scope by 857335's own admission; every stated boundary held.
4. **Substrate audit** (`substrate-audit.md`) — protos writer did not escape backslashes (27,657 failures in 300,000 leaves); four of five protos test files never compiled; derived enums bypassed the budget; panics on public surfaces; datom-codec 0.25.7 reversed bare strings against Vision.
5. **Runtime audit** (`runtime-audit.md`) — orchestrate-nexus linked Datom as built; the migration targeted a store generation that did not exist; seven Nexus authority failures; Lojix gaps three-fifths closed; deployment patch would break a CriomOS check.
6. **Periphery audit** (`periphery-audit.md`) — no harness v0.4.0 existed; signal-standard's head committed stale result symlinks; ten consumers behind; spirit daemons still running under the deprecation.
7. **Process audit** (`process-audit.md`) — no lock left held, no protected path touched; the Sol auditor had found real defects that 857335 never harvested; the read-only sandbox crippled that audit.

Presented to the living with six questions. Then the overnight order arrived.

## Part two — overnight

Wave 1 (parallel): protos fix, datom-codec fix, ethos-zero fix, skill proposals, Lojix history, dependency survey.

8. **protos 0.30.0** e8701521 (`protos-fix.md`) — one escape rule per boundary; all tests registered; Clone/PartialEq/Debug iterative after a 20k-depth overflow.
9. **datom-codec 0.26.0** 196d0e29 (`datom-codec-fix.md`) — bare-string writer per Vision/datom.md; decimal by position; budget, NaN, sixteen unreachable!() and ARITY removed; +4 and Meaning-in-String refused.
10. **ethos-zero 7.0.0** c8a68369 (`ethos-zero-fix.md`) — Query per Vision; Sema reserves nothing; Self boxed; four scanners folded to one; Sema generation tests.
11. **Skill proposals** (`skill-proposals.md`, proposals only) — replacement bodies for ethos, datom, protos; lojix's syntax witnessed rejected by the binary; the claude/codex wrappers pass no permission flag; ten more proposals appended later (testing: kill by PID; file-editing: clone from the real remote; subflow: release locks before finishing).
12. **Lojix history** (`lojix-history.md`) — nothing built for Lojix since 09-05 has run; CriomOS's unit calls a binary the pinned revision does not build; eleven ranked work items.
13. **Dependency survey** (`dependency-survey.md`) — tiered plan; kameo fork, chroma redb, nixpkgs fork, lojix deploy, spirit marked never unattended.

Wave 2: Tier 0 lockfile updates; recent-vision backlog; unused survey; Lojix W3/W8/W9/W10; Lojix W1/W4 on CriomOS test branches; substrate repin; Orchestrate fixes; removals; skill-tree regeneration.

14. **Tier 0** (`cargo-update-tier0.md`) — message, agent, clavifaber landed; five repositories fail on a floating `nota` dependency.
15. **Recent vision** (`recent-vision.md`) — ranked unrealized vision; 186 undated flow vision files; corrected its own Opus-5 misreading.
16. **Unused survey** (`unused-survey.md`) — nexus crate is used; repository removal foreclosed by the 08-10 "just leave it there" ruling; found Orchestrate's little-endian frame against signal's big-endian.
17. **Substrate repin** (`substrate-repin.md`) — datom-codec 0.26.1, ethos-zero 7.0.1.
18. **Orchestrate 0.32.0** 054ce581 with signal 3.0.1 and both contracts (`orchestrate-work.md`) — frame via signal; Datom-free as built; wrong migration deleted; Configure record, ordinary Configure with reversal, Observe subscription, socket modes and peer check.
19. **Removals** (`removals.md`) — CriomOS-home `f6db8d-removals` 4cb132ec (fzf orphans, dead compositor stack, dead flake input; derivation hash unchanged), terminal-cell `f6db8d-removals`; 57 GiB of orphaned build output deleted.
20. **Skill regeneration** (`skill-regeneration.md`) — blocked: roles.datom's typographic quotes under the pinned protos; curriculum-deploy migration held by flow 542442's lock 851.
21. **Lojix CriomOS** (`lojix-criomos.md`) — CriomOS `f6db8d-lojix-start` c4c830c1 (unit execs pinned lojix-nexus; VM test answers a Query); CriomOS-home 0176de5f (arch→architecture; fixtures from the real producer). Stops: the pinned lojix does not compile; `modelIsThinkpad` was deliberately deleted from horizon-rs at f1a5eca (design choice for the living).

Wave 3: substrate review; drift fix; producer settle; consumer migration; sweep; Orchestrate review and follow-up; nota pins.

22. **Substrate review** (`substrate-review.md`) — fixes hold, ~12,000 adversarial cases pass; committed contracts were not the generator's output; ARITY removal contradicts Vision by the letter (question for the living).
23. **Drift fix** (`substrate-drift.md`) — protos 0.30.1, datom-codec 0.26.2; contract drift checks; six traversals to one; −50 lines.
24. **Datom migration** (`datom-migration.md`) — ethos-zero 8.0.0 (error, not fault); fourteen consumers moved; mirror contracts left on branches.
25. **Producer settle** (`producer-settle.md`) — final heads: protos 0.30.1 171b21f6, datom-codec 0.26.3 627db67f, ethos-zero 8.0.1 de3d9928, signal 3.0.2 8f9a0deb.
26. **Consumer sweep** (`consumer-sweep.md`) — nineteen consumers on final heads including orchestrate 0.33.1 and claude-answers; a `git clone --shared` mistake caught by ls-remote and redone.
27. **Orchestrate review** (`orchestrate-review.md`) — six of seven closures hold against a real 0.30.0 store; peer refusal witnessed via user namespace; cutover left ordinary Configure open (high).
28. **Orchestrate follow-up** (`orchestrate-followup.md`) — 0.33.0: carried stores seed Configure through the meta path; durable peer-refusal tests; UPGRADES.md corrected.
29. **Nota pins** (`nota-pins.md`) — nota was renamed dotos; Cargo cannot override a producer's floating pin; aggregator group landed on dotos; harness 0.4.0.
30. **Stack membership** (`stack-membership.md`) — the dotos landing was the wrong direction (Vision/datom.md: everything moves to Datom, Dotos is frozen). Corrected by:
31. **Aggregator migration** (`aggregator-migration.md`) — signal-aggregator 0.8.0, meta-signal-aggregator 0.6.0, aggregator 0.6.0 on the Datom stack; router needs six producers first.

Wave 4: verification and closure.

32. **Push verification** (`push-verification.md`) — every claimed landing is on GitHub main or an ancestor, except one branch that reached only the gitolite mirror; signal-repository-ledger's mirror main had been moved sideways.
33. **Mirror restore** (`mirror-restore.md`) — mirror main restored; branches on both remotes.
34. **Lojix work** (`lojix-work.md`) — horizon-rs 0.10.0, signal-lojix 4.1.0, meta-signal-lojix 5.1.0, lojix 4.0.0 8cb12b8d; failure evidence durable (bead primary-cod closed); no-free-functions enforced in both; no-inherent-methods in lojix needs the Store/SchemaRuntime decomposition.
35. **Lojix settle** (`lojix-settle.md`) — repin of the Lojix group to final heads, VM fixture regeneration, real cluster proposal parse: see that report for its outcome (its VM gate was still running when this summary was written).
36. **Open items and Beads** (`open-items.md`, `beads-created.md`) — epic primary-ciw with 100 children: 55 decisions, 13 landings, 32 work items.

## Incidents and errors of this flow

- A review subflow's `pkill -f` matched the live orchestrate-nexus user service and stopped it for 21 seconds (21:35:48–21:36:09); restarted; store intact.
- This flow read `lojix-work.md` mid-flight and treated locks 1111/1112 as leaked; the subflow was alive. The settle subflow was corrected to rebase onto lojix 4.0.0.
- The nota-pins direction (onto dotos) contradicted standing Vision; corrected the same night for the aggregator group.
- One subflow's `git clone --shared` pointed origin at a local checkout; caught and redone.
- Five pushed commit messages label ethos-zero da585049 as 7.0.1; it is 8.0.0.

## Lessons

- A subflow's report can exist before the subflow is done; only its return closes it.
- Kill a scratch daemon by PID, never by pattern that a production instance also matches.
- Verify pushes with ls-remote against the real remote; some checkouts have a gitolite `origin` and a `github` remote.
- The skills for protos, datom, ethos, lojix, and orchestrate teach the abandoned syntax; agents following them get refusals.
- Contracts must be checked against their generator or they drift silently.

## Unfinished and for the living

Everything is in `reports/open-items.md` and the beads under primary-ciw. The largest: the meta CLI name, the ARITY/Compositional split, hardware classification after horizon-rs f1a5eca, the schema-rust emitter wall behind listener/router/repository-ledger, curriculum-deploy's migration under flow 542442, the CriomOS `f6db8d-lojix-start` and CriomOS-home `f6db8d-removals` landings, and the skill proposals awaiting approval.
