# Beads created from flow f6db8d's open-items report

Compiled by a subflow of f6db8d, working from `reports/open-items.md`. Store
verified before writing (`/home/li/primary/.beads`, plus the target
repository's own store wherever an item belonged squarely to it and that
store existed and was usable). All primary-store beads are parented to the
epic below; cross-store beads carry their primary/epic reference as a note
(links cannot cross bead databases), and the epic itself carries a note
listing every cross-store companion id. `blocks`/`related` dependencies were
added wherever `open-items.md` stated one; the rest are cross-referenced in
text only.

## Epic

- **primary-ciw** — Overnight flow f6db8d: land, decide, finish (epic). Points at `flows/f6db8d/summary.md` (to be written) and `flows/f6db8d/reports/open-items.md`.

## Group B — pushed branches (13 beads: 12 landing/decision beads + 1 prune chore)

| id | title | note |
|---|---|---|
| home-awa | CriomOS-home sheds fzf orphans, dead compositor stack, and the dead primary-generated-src input | B1, own store (CriomOS-home) |
| primary-ciw.1 | terminal-cell drops the dead dotos-text feature and stray result-N symlinks | B2, blocked by primary-ciw.14 (C4) |
| CriomOS-gw2 | CriomOS starts the Lojix it pins via a clean lojix-nexus unit | B3, own store (CriomOS) |
| home-aly | CriomOS-home fixes the arch field mismatch and checks in a real horizon-projection fixture | B4, own store (CriomOS-home) |
| primary-ciw.2 | harness cargo update is ready once the schema-rust emitter wall clears | B6, blocked by primary-ciw.11 (C1) |
| primary-ciw.3 | router cargo update is ready once the schema-rust emitter wall clears | B7, blocked by primary-ciw.11 (C1) |
| primary-ciw.4 | listener cargo update is ready once the schema-rust emitter wall clears | B8, blocked by primary-ciw.11 (C1) |
| primary-ciw.5 | repository-ledger cargo update awaits the schema-rust wall and the remote-authority ruling | B9, blocked by primary-ciw.11 (C1) and primary-ciw.82 (A50) |
| primary-ciw.6 | router keeps its clean main; the Dotos-migration branch stays unlanded | B10, **closed** (already resolved, must-not-land) |
| primary-ciw.7 | signal-repository-ledger's Dotos migration is fully green, blocked only on the remote-authority ruling | B11, blocked by primary-ciw.82 (A50) |
| primary-ciw.8 | meta-signal-repository-ledger's Dotos migration is fully green, held for signal-repository-ledger's blocker | B12, blocked by primary-ciw.7 and primary-ciw.82 |
| primary-ciw.9 | Discard-or-finish decision owed on flow-857335's pre-f6db8d WIP bookmarks | B22, related to primary-ciw.54 (A21) |
| primary-ciw.10 | Prune stale f6db8d test branches superseded by landed main | chore folding B13-B21's likely-stale branches (9 branches listed) |

## Group C — mechanical work (32 beads: 31 substantive items + 1 hygiene chore)

Priority 1 (deploy would hit): primary-ciw.11 (C1, schema-rust emitter wall), primary-ciw.12 (C2, curriculum-deploy migration), home-vem (C5, CriomOS-home service-path check). Priority 2 otherwise.

| id | title | note |
|---|---|---|
| primary-ciw.11 | The schema-rust emitter wall blocks nine repositories | C1, P1, related primary-hqu.14 |
| primary-ciw.12 | curriculum-deploy's Datom migration is unstuck once flow 542442's Lock 851 clears | C2, P1 |
| primary-ciw.13 | Skill regeneration: main-flow, design, and realization remain agent-loadable on Claude | C3, blocks primary-ciw.12 |
| primary-ciw.14 | terminal and mentci are independently broken, unrelated to flow f6db8d | C4 |
| home-vem | CriomOS-home's orchestrate-service-path check fails on the reply shape | C5, P1, own store, notes primary-ciw.49 (A16) |
| skills-68r | Curriculum's orchestrate.md and datom skills still teach curly quotes | C6, own store, notes primary-ciw.86 (A54) |
| primary-ciw.15 | Verify aggregator's landed main revision against GitHub | C8 |
| primary-ciw.32 | Remove lojix's unreachable!() sites | C9a — lojix's own `.beads` store scaffold exists but its Dolt database failed to init (`bd bootstrap` did not repair it); filed in primary instead |
| primary-ciw.16 | datom-codec's byte-length formula duplication has a confirmed-wrong arm | C9b, related primary-ciw.40 (A6) |
| primary-ciw.33 | DeploymentPipeline::phase_event discards _detail for non-terminal transitions | C10 — lojix store unusable, filed in primary |
| primary-ciw.34 | CopyClosure still maps to the generic BuilderUnreachable reason | C11 — lojix store unusable, filed in primary |
| primary-ciw.35 | lojix's same-host-test-activation VM fixture is stale | C12 — lojix store unusable, filed in primary |
| primary-ciw.17 | Re-verify the real cluster proposal's parse fix at current protos | C13 |
| primary-ciw.18 | criomos-horizon-config's local checkout is stale and holds a retired file | C14 |
| CriomOS-zwv | CriomOS complete-system BuildOnly does not reach BootstrapTerminal.Succeeded | C15, own store |
| CriomOS-4pi | Land the CriomOS lojix repin | C16, own store |
| primary-ciw.19 | terminal-cell's cargo update has not yet run | C17, related primary-ciw.14 (C4) |
| primary-ciw.20 | Remove flagged dead binaries and dead test code | C26 |
| home-3sq | Import CriomOS-home's pi-models.nix | C27, own store |
| primary-ciw.21 | Repair the failing agent-intercom-fleet-cleanup.timer | C28 |
| primary-ciw.22 | Re-check the Orchestrate endianness fix and the datom-codec pin unification | C29 |
| primary-ciw.23 | Assess disposal of the large unmerged spirit WIP branch | C31 |
| primary-ciw.24 | spirit and spirit-judge run in production while marked deprecated | C32, related primary-mo6 |
| primary-ciw.25 | AGENTS.md and CLAUDE.md have diverged on the skill-loading authority rule | C34 |
| primary-ciw.26 | Execute the specified Tier 0/1 dependency updates | C37 |
| primary-ciw.27 | Convert 205 mutable branch="main" pins to immutable revs | C38 |
| primary-ciw.28 | Check niri-flake's module schema against 26.04 | C39 |
| primary-ciw.29 | Sweep uncommitted/unclaimed dirty trees | C40 |
| primary-ciw.30 | Fix ethos-zero's generator to emit rkyv attributes recursive Signal types need | C42 |
| orchestrate-ykd | Fix three low-severity Orchestrate defects (D-8/D-9/D-10) | C45, own store |
| orchestrate-clf | Give the live-vs-scratch Nexus process distinction a dedicated remediation | C46, own store, notes primary-ciw.50 (A17) |
| primary-ciw.31 | Record-only residue from flow f6db8d needing no further action | hygiene chore folding C7, C18-C21, C23, C24, C33, C35, C43, C44 |

C25 (repos-manifest.dotos staleness) was **not** duplicated — already tracked by `primary-xqb.8.8`; linked instead via `bd dep add primary-ciw primary-xqb.8.8 -t related`. C7, C18-C21, C23-C24, C30, C33, C35-C36, C41, C43-C44, C46's proposal-half are folded/referenced rather than separately beaded, per the report's own "no ruling, just noticing/record-only/closed" framing.

## Group A — design decisions (55 beads covering all 59 numbered items)

Priority 1: primary-ciw.40 (A6, ARITY/Compositional split), primary-ciw.49 (A16, meta CLI name) + primary-ciw.79 (A47, same naming cluster), primary-ciw.51 (A18, Kameo actors standard), primary-ciw.63 (A31, hardware classification), primary-ciw.36 (A1, Datomizable one-or-two). Priority 2 otherwise.

| id | title | covers |
|---|---|---|
| primary-ciw.36 | Does Datomizable name one conversion or two? | A1, P1 |
| primary-ciw.37 | Which bare-string rule, and what is its name? | A2 |
| primary-ciw.38 | Vector<Integer>/space-in-print shape across protos and ethos-zero | A3, A4, A13, A58 (grouped) |
| primary-ciw.39 | Problem::MissingHead reachability | A5 |
| primary-ciw.40 | ARITY removal vs Vision — Compositional split | A6, P1 |
| primary-ciw.41 | Non-finite f64 / Decimal intrinsic | A7 |
| primary-ciw.42 | protos::Error naming | A8 |
| primary-ciw.43 | Single-field structs — alias or newtype? | A9 |
| primary-ciw.44 | Is Sized a tenth intrinsic? | A10 |
| primary-ciw.45 | Processable ordering | A11 |
| primary-ciw.46 | sec4.3 qualification leak | A12 |
| primary-ciw.47 | Boundary::Parentheses / Opaque | A14 |
| primary-ciw.48 | datom-codec dirty tree, sanctioned? | A15, related primary-ciw.40 |
| primary-ciw.49 | Meta CLI name | A16, P1, related primary-ciw.79 |
| primary-ciw.50 | Socket binding default vs store | A17 |
| primary-ciw.51 | Kameo actors standard for Orchestrate | A18, P1 |
| primary-ciw.52 | Kameo fork: rebase or drop | A19, related primary-ciw.51, primary-2d7, primary-746 |
| primary-ciw.53 | Streaming CLI design | A20 |
| primary-ciw.54 | Discard/finish orchestrate WIP checkout | A21 |
| primary-ciw.55 | Carried-store bootstrap window | A22 |
| primary-ciw.56 | signal-frame absorption | A23 |
| primary-ciw.57 | Retire dotos-named repos / Signal-text-to-Datom | A24, A26 (grouped) |
| primary-ciw.58 | schema-rust build.rs stack membership | A25, related primary-ciw.11 |
| primary-ciw.59 | nexus / signal / sema ontology | A27 |
| primary-ciw.60 | router / wrapping enum / handshake | A28 |
| primary-ciw.61 | Chroma redb migration | A29 |
| primary-ciw.62 | nixpkgs / GTK backport | A30 |
| primary-ciw.63 | Hardware classification | A31, P1 |
| primary-ciw.64 | CriomOS-home / Horizon divergences | A32 |
| primary-ciw.65 | Fixture vs flake-input projection | A33 |
| primary-ciw.66 | lojix.service rename | A34 |
| primary-ciw.67 | readOnly Nix options | A35 |
| primary-ciw.68 | lojix v4 database ruling | A36 |
| primary-ciw.69 | lojix skill query-syntax approval | A37 |
| primary-ciw.70 | CheckHostKeyMaterial vocabulary | A38 |
| primary-ciw.71 | lojix skill wrong filename | A39, related primary-ciw.69 |
| primary-ciw.72 | Standing Lojix questions (W11) | A40 |
| primary-ciw.73 | Zeus signing/trust boundary | A41 |
| primary-ciw.74 | Deploy.Host redesign | A42 |
| primary-ciw.75 | WatchDeployments implement-or-delete | A43 |
| primary-ciw.76 | criomos-core / extended-horizon shape | A44 |
| primary-ciw.77 | Unmerged Lojix bookmarks fate | A45 |
| primary-ciw.78 | NixOS lojix module location | A46 |
| primary-ciw.79 | lojix naming objection / unilateral lojix-meta | A47, P1, related primary-ciw.49 |
| primary-ciw.80 | Release registry authority | A48 |
| primary-ciw.81 | Lojix never-unattended upgrade | A49 |
| primary-ciw.82 | repository-ledger remote authority | A50 |
| primary-ciw.83 | flows / static workspace repo naming | A51 |
| primary-ciw.84 | Skill-corpus contradictions | A52 |
| primary-ciw.85 | Sol contradiction | A53 |
| primary-ciw.86 | skill-proposals.md approval | A54, related primary-ciw.69/70/71 |
| primary-ciw.87 | mandatoryTraits placement | A55 |
| primary-ciw.88 | Harness wake-on-send-to-claude | A56 |
| primary-ciw.89 | Entry-file psyche-search duplication | A57 |
| primary-ciw.90 | Bare enum variant becomes payload variant | A59 |

## Counts

- Epic: 1 (primary-ciw)
- Group A (decisions): 55 beads, covering all 59 numbered design questions
- Group B (landings/branches): 13 beads (12 live + 1 prune-stale chore; 1 of the 12, primary-ciw.6, closed on creation as already-resolved)
- Group C (mechanical work): 32 beads (31 substantive items + 1 hygiene-residue chore)
- **Total beads created: 101**
- Cross-store companions: 10 (home-awa, home-aly, home-vem, home-3sq, CriomOS-gw2, CriomOS-zwv, CriomOS-4pi, orchestrate-ykd, orchestrate-clf, skills-68r)
- Existing beads linked (not duplicated): primary-hqu.14, primary-xqb.8.8, primary-mo6, primary-2d7, primary-746

## Sources

- `/home/li/primary/flows/f6db8d/reports/open-items.md`
- `bd show`/`bd create`/`bd dep add`/`bd note` output from this session against `/home/li/primary/.beads` and the `.beads` stores of CriomOS, CriomOS-home, orchestrate, Curriculum, and chroma-repo-adjacent checkouts under `/git/github.com/LiGoldragon/`
