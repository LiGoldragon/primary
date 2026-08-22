# Orchestrate situation and skill review packet

## Finding

Flow `b7465e71` exposed a lane-registration contract gap while a worker was
editing Curriculum. The worker received `edit-coordination`, but neither a
concrete lane/discipline assignment nor syntax accepted by the deployed CLI.
It guessed fifteen registration forms; every one failed in Dotos parsing. It
then used the skill's fallback and completed the unrelated flows/vocabulary
work without a registered lane or claims.

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

## Skill ownership

No new skill is justified. `edit-coordination` already owns the exact
situation: another agent may write the same paths. A Dotos- or
Orchestrate-specific neighbor would duplicate its trigger. The authored source
is `/git/github.com/LiGoldragon/Curriculum/skills/edit-coordination.md`; the
generated `.agents/`, `.claude/`, `.codex/`, and `.pi/` copies are not edit
targets. No manifest or version change is implicated.

## Exact proposal for psyche review

Preserve the description and every lifecycle, recovery, reply-record,
advisory-claim, and closeout rule. Change only the four retired wire examples
and their delimiter sentence:

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

This preserves the owner and operating policy, changes the examples to syntax
accepted by the current `0.20.0` parser, and removes only stale wire syntax.

## Proof required after approval

1. Witness the old forms failing with their specific Dotos shape errors.
2. Add an independent parser/contract fixture and see it fail before changing
   the skill.
3. Witness the corrected forms pass parsing. A live daemon is required before
   claiming successful state transitions or reply contracts.
4. Regenerate consumer skills from Curriculum, run the durable skill gate, and
   expose any new durable test through a Nix check.
5. Pressure-test a fresh worker: the old skill should reproduce legacy forms;
   the proposed source should yield the brace/dotted forms and reply handling.

Orchestrate's own stale `AGENTS.md` examples are a separate authored-doc scope.
Leaving them unchanged preserves a second source for the same failure; changing
them should be ruled alongside, or explicitly separated from, the skill edit.

## Sources

- Witness: `flows/01a02a34/witnesses/laneRegistrationSyntax.md`.
- Witness: `flows/01a02a34/witnesses/orchestrateRepositoryState.md`.
- Flow `b7465e71`, especially its worker transcript and `log.md`.
- Flow `15b67974`, `log.md:167-172`.
- `orchestrate/AGENTS.md:51-73,188-227`.
- `/git/github.com/LiGoldragon/Curriculum/skills/edit-coordination.md:6-24`.
- `psyche-raw/Vision/entryFiles.md:75-89`.
- `psyche-raw/Vision/domainKnowledgePlacement.md`.
- `psyche-raw/Vision/gradientsOfAuthority.md`.
- `flows/01a01bac/vision/skillDesigning.md:25-33`.

