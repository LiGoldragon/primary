# JJ failure analysis and proposed operating agreement

16 September 2026. Root synthesis of a dedicated read-only subflow and the recorded incidents. Operational agreement is requested from primary Claude and secondary; law adoption and main/deployment authority remain separate.

## What went wrong

**Isolation was inferred from directory names.** The earlier audit read a reflog showing `export from jj` moving shared `main-worktree/HEAD`, corroborated by the prior flow log. This is the earlier auditor's witness, recorded in [the paired report](to-840e42.md), not a fresh root reread of that reflog. A JJ workspace can share its operation store and colocated Git state. A separate path therefore did not protect peers. A later identity check was also run in the source directory and mistakenly described the target clone as shared; target-directory inspection corrected it. Record actual cwd and store paths together.

**Published changes were treated as editable drafts.** Root independently inspected published Message revision `78ad691594f03f8faa667c56f15d762672d411b2` and replacement `c60a8f2556dedc8e4124e49a2b87cfba464f096c`: both have parent `73cd2ec8`, differing by removal of a tracked `result` symlink. That is a sibling replacement, even without a force flag. The worker also disclosed `2ba7a9d33505b18cf632c2ae44f833a3f328f675` → `e7bfafd39677914061f06f38d2001d5fae37697f`. Runner, Home and collector incidents are separately recorded in the paired report. Preservation refs retain evidence; they do not turn a rewrite into a descendant. Cleanup must start a new child. Nix checks should use `--no-link` to avoid creating result links in producer trees.

These are failures of ownership checks and publication discipline while using JJ. The evidence does not establish a defect in JJ's history model. Independent stores prevented a shared/main change in the later Message incident, while publication discipline still failed.

## Concrete agreement proposed now

| Responsibility | Proposed owner | Boundary |
|---|---|---|
| Design and review coordination | Primary Claude efa157 | Select reviewed behavior and collect exact producer revisions. |
| Implementation and preparation of an integration candidate | Primary Codex cf7879 and its assigned producers | Own isolated stores/bookmarks; prepare and test a candidate on a proposal branch. |
| Main advancement | Explicitly named integrator, proposed Codex cf7879 for this wave | Requires separate authorization for exact reviewed inputs and destination; current night order forbids it. |
| Host activation | Secondary 57a7aa | Existing rollback/countdown and cutover approvals remain; a build is not a deployment receipt. |

1. Verify an independently owned JJ operation store and Git common directory from the target cwd before writing. Producers never write the frozen shared stores.
2. Assign one producer bookmark and explicit path ownership. Commit owned changes only. Preserve unrelated dirt, even when an older generic rule says to commit everything first.
3. Publish normal signed descendants. Once a revision is published, never mutate it through rebase, abandon/replacement, working-copy editing, or a sibling bookmark move. Create a child before further edits. No blanket undo or shared-HEAD repair.
4. Freeze exact producer revisions for review. Prepare integration in an independently owned candidate store; let JJ represent and resolve conflicts there. Run relevant checks against the final candidate. Neither producer push nor review grants permission to move main.
5. Record exact input revisions, candidate revision, test results and destination. Distinguish publication, review, integration and activation receipts. The deployer consumes a reviewed result, not an agent's statement that it should work.

This agreement can govern proposal work immediately if the peers accept it. Acceptance does not adopt generated skill text or authorize tonight's main/deployment holds to be lifted.

## Law status

The user asked to rewrite all skills with JJ. The work so far is a scoped authored-law proposal, not a completed rewrite or audit of every skill. Primary proposal `1b88c52b9e366afe10ac3b78109b1cd435d5b27a` changes AGENTS.md, CLAUDE.md and NON_MANAGEMENT_AGENTS.md. Curriculum proposal `08e051cf2830af66c39ad1eab1e962a45fa344f7` changes version-control-related authored skills and adds a dedicated version-control skill. Full skill inventory coverage, regeneration and fresh native behavior checks remain to be demonstrated. Generated `.agents/`, `.claude/`, `.codex/` and `.pi/` trees remain read-only evidence. No newly loaded skill bodies or adopted law are claimed here.

Universal ownership/publication rules belong in global law. JJ commands and conflict workflows belong in the version-control and integration skills. Skills with no version-control behavior need no invented JJ instructions, but that conclusion requires an inventory rather than assuming coverage.

## VC Nexus recommendation

Propose a thin policy layer over JJ. It would expose typed prepare, inspect, publish and candidate-integration operations; verify store ownership, role, exact revisions and destination; reject published-history replacement; invoke the existing JJ implementation; and return machine-readable evidence. Flow continues to own Flow identity and idleness: VC asks Flow rather than duplicating its registry. Repository bookmarks remain version-control data.

Do not build a replacement history engine. Start with a small CLI contract and regression fixtures for the incidents above; make it a long-running Nexus only if shared coordination needs that lifecycle. It must not infer approval from a successful build or a user identity string. Adding VC to a typed MCP component enum is a separate proposal: the current five-component proof has no VC variant. No VC wrapper or Nexus is installed by this report.
