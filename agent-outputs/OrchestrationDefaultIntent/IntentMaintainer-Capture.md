# Intent Maintainer Capture

## Task and scope

Capture durable psyche intent from the latest message if it met Spirit criteria. Candidate areas were orchestration-by-default, orchestrator non-action, orchestration skill shape, skill/agent composition, and commit-message model provenance.

## Files and commands consulted

- `AGENTS.md` workspace instructions from the provided context.
- Existing Spirit neighborhood through `PublicTextSearch` and `Observe`.
- `.agents/skills/intent-led-orchestration/SKILL.md` for orchestration manifestation.
- `.agents/skills/jj/SKILL.md` for commit-message manifestation.
- Spirit schema and skill docs were consulted where operation shapes mattered.

## Existing intent neighborhood observed

Relevant existing records before capture:

- `n9fl`: agent systems maximize best-quality output by maximizing early context and using extremely specific agents/skills.
- `346n`: quality is primary for agent work.
- `jys2`: design at the post-agent capability frontier.
- `w312`: deterministic routing/dispatch/lookup belongs in mechanism, while agents do substantive cognition.
- No existing active public record was found for orchestration as the default for all sessions or for commit messages naming the model.

## Classification and Spirit results

Accepted:

- `dhqe` — new `Constraint`: all agent work sessions should be orchestration sessions; an orchestrator should not perform task work directly; it reads psyche chat, pasted content, and agent outputs, then spawns subagents even when asked to do, look up, or research; the orchestration skill should not provide a direct-action exception window.
- `n9fl` — clarified existing `Principle`: agent-system composition now explicitly favors orchestration with extremely specific subagents/skills. This used the psyche wording `skill/agent composition should favor orchestration and specific subagents` and did not create a duplicate record.
- `em04` — new `Constraint`: when feasible, commit messages should indicate the LLM model that created the changes.

Rejected or adjusted before acceptance:

- First orchestration `Record` attempt was rejected as `EmptyReferents`.
- High-certainty/high-importance orchestration attempts were rejected as overstated or unsupported; accepted at `Medium` certainty and `Medium` importance.
- First commit-message attempt was rejected because `LLM-model-provenance` was not a valid concrete referent; accepted with `commit-message-policy` only.

## Manifestation changes

Changed guidance surfaces:

- `.agents/skills/intent-led-orchestration/SKILL.md`
  - Removed the fresh-context-only/direct-action escape-window wording.
  - Added that every orchestration-capable session is an orchestration session.
  - Added `look it up` and `research it` to the examples that must become worker dispatch rather than direct orchestrator action.
  - Replaced the ordinary-immediate-implementation exit with a worker-dispatch requirement.
- `.agents/skills/jj/SKILL.md`
  - Added that commit messages should include the LLM model that created the changes when feasible.

## Verification

- Each changed guidance statement traces to accepted Spirit records `dhqe`, `n9fl`, or `em04`.
- No supersession was needed; `n9fl` was clarified in place and no duplicate standalone clarification was left active.
- Public searches after capture returned `dhqe`, clarified `n9fl`, and `em04` with the intended wording.

## Checks run

- `spirit '(PublicTextSearch [orchestration sessions])'` — passed after capture; returned `dhqe` and clarified `n9fl`.
- `spirit '(PublicTextSearch [LLM model commit messages])'` — passed after capture; returned `em04`.
- `spirit '(PublicTextSearch [favor orchestration specific subagents])'` — passed after clarification; returned `n9fl` and `dhqe`.
- `jj diff --no-pager -- .agents/skills/intent-led-orchestration/SKILL.md .agents/skills/jj/SKILL.md` — passed; showed only the intended guidance edits in those files.
- `jj status --no-pager` — passed; showed this task's two skill edits and output file plus unrelated pre-existing dirty files; jj has no staged-file area.

## Residual risks and follow-up

- The working copy already contained unrelated dirty files from other sessions. I did not touch or normalize them.
- No tests were added; this was intent capture and markdown guidance maintenance.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Spirit accepted dhqe and em04, clarified n9fl, and guidance edits were limited to the orchestration and jj skill surfaces needed to manifest those accepted intents."
    }
  ],
  "changedFiles": [
    ".agents/skills/intent-led-orchestration/SKILL.md",
    ".agents/skills/jj/SKILL.md",
    "agent-outputs/OrchestrationDefaultIntent/IntentMaintainer-Capture.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "spirit '(PublicTextSearch [orchestration sessions])'",
      "result": "passed",
      "summary": "Verified dhqe and clarified n9fl are visible."
    },
    {
      "command": "spirit '(PublicTextSearch [LLM model commit messages])'",
      "result": "passed",
      "summary": "Verified em04 is visible."
    },
    {
      "command": "spirit '(PublicTextSearch [favor orchestration specific subagents])'",
      "result": "passed",
      "summary": "Verified n9fl clarification is visible."
    },
    {
      "command": "jj diff --no-pager -- .agents/skills/intent-led-orchestration/SKILL.md .agents/skills/jj/SKILL.md",
      "result": "passed",
      "summary": "Showed only intended skill guidance edits in the two manifested files."
    },
    {
      "command": "jj status --no-pager",
      "result": "passed",
      "summary": "Showed this task's edits plus unrelated pre-existing dirty files; jj has no staged-file area."
    }
  ],
  "validationOutput": [
    "Accepted Spirit records: dhqe, em04; clarified existing record: n9fl.",
    "No tests were applicable to Spirit/guidance maintenance."
  ],
  "residualRisks": [
    "Working copy has unrelated pre-existing dirty files from other sessions; not touched."
  ],
  "noStagedFiles": true,
  "diffSummary": "Captured orchestration-default and commit-message model intent in Spirit; clarified n9fl; manifested accepted intent in the orchestration and jj skills.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "Spirit rejected earlier overstated or invalid-referent attempts; accepted records use lower certainty/importance and concrete referents."
}
```
