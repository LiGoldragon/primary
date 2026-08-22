# Orchestrate situation and skill review packet

## Finding

Flow `b7465e71` exposed two lane-registration contract gaps while a worker was
editing Curriculum. The worker received `edit-coordination`, but neither a
concrete lane/discipline assignment nor syntax accepted by the deployed CLI.
It guessed fifteen registration forms; every one failed in Dotos parsing. It
then used the skill's fallback and completed the unrelated flows/vocabulary
work without a registered lane or claims.

The syntax fault is not sufficient to explain the failure. Local Orchestrate
instructions say the harness supplies lane and discipline, while the observed
registration, identity-mint, and harness-launch contracts transmit only
identity, mission, harness, and continuation. The b7465e71 worker's dispatch
also carried no concrete assignment. The operational contract is therefore
underdetermined before it reaches the parser.

The daemon was never reached, so this was not witnessed as a daemon refusal,
collision, or connectivity failure. The narrower witnessed failure is stale,
underdetermined operational documentation.

## Current shape

```text
remote main ─┐
local main  ─┼─ b1435557  clean, Orchestrate 0.20.0
checkout    ─┘
                 │
                 ├─ live JJ workspace: repair…  11d, clean, empty tip
                 ├─ live JJ workspace: schema…  12d, clean, empty tip
                 └─ 6 dangling JJ records        62–78d, missing roots,
                                                    empty tips, no unique files
```

There is no Git lag from current remote main. There is contract/version lag:
the repository and current CLI are `0.20.0`, while `orchestrate/AGENTS.md`
still describes a deployed `0.16.0` contract and gives lifecycle forms rejected
by the current parser.

```text
AGENTS.md / edit-coordination old forms
                  │
                  ▼
             Dotos parser ✕

proposed brace/dotted forms
                  │
                  ▼
             Dotos parser ✓ ──► transport ✕ (daemon socket absent)
```

Parser acceptance is witnessed. Live daemon semantics and reply records remain
unknown.

## Skill ownership and assignment boundary

No new skill is justified. `subflows` owns an editing-capable dispatch and
`edit-coordination` owns the resulting registration and claims; a
Dotos-, Orchestrate-, or session-lanes-specific neighbor would duplicate those
triggers. Current Curriculum has no `session-lanes` source. The authored
sources are `/git/github.com/LiGoldragon/Curriculum/skills/subflows.md` and
`/git/github.com/LiGoldragon/Curriculum/skills/edit-coordination.md`; the
generated `.agents/`, `.claude/`, `.codex/`, and `.pi/` copies are not edit
targets. No manifest or version change is implicated.

## Provisional two-skill patch

The prior syntax-only proposal is insufficient: corrected wire examples still
leave an editing worker without the values required to fill them. Preserve the
existing descriptions and all lifecycle, recovery, reply-record, advisory-
claim, and closeout rules. The provisional boundary is:

- `subflows` supplies a concrete Session, Lane, Discipline, and
  Fresh-or-Recovery value to every editing-capable dispatch, and does not
  dispatch when any is missing.
- `edit-coordination` consumes those dispatched values for registration and
  claims. It never invents them or derives them from provider identities.

Within `edit-coordination`, replace only the retired wire examples and their
delimiter sentence with the parser-accepted v0.20 forms:

```diff
-      meta-orchestrate "(Register ((SessionName laneName ([SessionName Discipline] Structural) [why this lane exists]) Fresh))"
-      orchestrate      "(Claim (laneName [(Path /absolute/path)] [why you are editing]))"
-      orchestrate      "(Release laneName)"
-      meta-orchestrate "(Retire (Lane laneName))"
+      meta-orchestrate "(Register {{SessionName laneName {{[SessionName Discipline]} Structural} (why this lane exists)} Fresh})"
+      orchestrate      "(Claim {laneName [Path./absolute/path] (why you are editing)})"
+      orchestrate      "(Release {laneName})"
+      meta-orchestrate "(Retire Lane.laneName)"

-A bracketed reason needs two or more tokens; a one-word reason goes bare.
+A parenthesized reason needs two or more tokens; a one-word reason goes bare.
```

This preserves ownership and operating policy, adds the missing dispatch-to-
registration handoff, changes the examples to syntax accepted by the current
`0.20.0` parser, and removes only stale wire syntax. It does not add a skill.

This is not yet approval-ready. The living must rule who assigns Session, Lane,
Discipline, and Fresh-or-Recovery; their semantics and valid disciplines;
whether `Structural` is universal; and whether this V2 identity remains
desired.

## Proof required after approval

1. Obtain the living's rulings on the four unresolved assignment questions.
2. Witness the old forms failing with their specific Dotos shape errors.
3. Add an independent dispatch-to-registration contract fixture and see it
   fail before changing either source.
4. Witness corrected assignment-bearing dispatches and v0.20 forms pass
   parsing. A live daemon is required before claiming successful state
   transitions or reply contracts.
5. Regenerate consumer skills from Curriculum, run the durable skill gate, and
   expose any new durable test through a Nix check.
6. Pressure-test a fresh editing worker: the old sources should reproduce the
   missing assignment or legacy forms; the proposed sources should supply the
   concrete values, yield brace/dotted forms, and handle replies.

Orchestrate's own stale `AGENTS.md` examples are a separate authored-doc scope.
Leaving them unchanged preserves a second source for the same failure; changing
them should be ruled alongside, or explicitly separated from, the skill edit.

## Sources

- Witness: `flows/01a02a34/witnesses/laneRegistrationSyntax.md`.
- Witness: `flows/01a02a34/witnesses/orchestrateRepositoryState.md`.
- Witness: `flows/01a02a34/witnesses/coordinationAssignment.md`.
- Flow `b7465e71`, especially its worker transcript and `log.md`.
- Flow `15b67974`, `log.md:167-172`.
- `orchestrate/AGENTS.md:51-73,188-227`.
- `/git/github.com/LiGoldragon/Curriculum/skills/edit-coordination.md:6-24`.
- `psyche-raw/Vision/entryFiles.md:75-89`.
- `psyche-raw/Vision/domainKnowledgePlacement.md`.
- `psyche-raw/Vision/gradientsOfAuthority.md`.
- `flows/01a01bac/vision/skillDesigning.md:25-33`.
