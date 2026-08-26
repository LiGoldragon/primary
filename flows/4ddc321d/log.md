# Flow 4ddc321d

Design flow. Opening word: remember 2f6b1dc5 — another flow apparently
restored its lost flow logs.

Remembered: 2f6b1dc5 — depth 1

## About

Continuing 2f6b1dc5's base-context replacement design. Opened by
remembering 2f6b1dc5 after its working-copy loss and restoration by
01a035fb. The psyche then directed (vision/hijackRepositories.md): two
public repositories, codex-hijack and claude-hijack, each thoroughly
documenting its harness's stock context — every block, what it is
tied to, how it is overridden — with the stock text copied verbatim
from what is found. Codex first, believed the worst offender; after
both repos are up and populated, the psyche reviews codex's worst
offender block.

## Settled

- Restoration confirmed and attributed: flow 01a035fb restored
  2f6b1dc5's log tail and vision entries in commit 90575b46c
  (2026-08-24, "flows: 2f6b1dc5 — restore lost records; base-context
  deployment accounts"). The files were never deleted from git; the
  loss was a working-copy loss during concurrent flow activity. The
  restored tail was rebuilt from retained session context and has no
  independent pre-loss byte copy. f426777b was not involved — it
  restored aa4c7747's index line, a parallel loss case.
- 2f6b1dc5's standing work: "base context" vocabulary deployed,
  vocabulary override line deployed, context-strata skill recovered
  and redeployed with "context" replacing "prompt", and the
  full-replacement mechanics for Claude Code (--system-prompt /
  --system-prompt-file) and Codex (instructions /
  model_instructions_file / base_instructions) witnessed and ledgered
  in verified/claude-code-context.md.
- No later flow picked up 2f6b1dc5's open design thread.
- codex-hijack subflow reported complete (claims, report at
  reports/codexHijackRepo.md): public repo at
  github.com/LiGoldragon/codex-hijack; Codex CLI 0.149.1 witnessed
  (tag rust-v0.149.1, commit 980a6d12); 17 stock-context blocks
  inventoried, 8 model-variant base contexts extracted verbatim; six
  worst-offender candidates flagged. Blocker: server-catalog
  instruction templates and collaboration-mode messages are fetched
  at runtime from OpenAI servers — content unknown from source alone.
  Machinery note: meta-orchestrate lane registration refused the
  attempted DOTOS; work proceeded on advisory basis.

- claude-hijack subflow reported complete (claims, report at
  reports/claudeHijackRepo.md): public repo at
  github.com/LiGoldragon/claude-hijack; Claude Code 2.1.241 witnessed
  (build 2026-08-22, git SHA c87e2742); 21 stock-context blocks
  inventoried (8 static + 13 conditional), 8 system-reminder messages
  documented, tool descriptions noted as API-parameter delivery; 19
  blocks extracted verbatim, 2 blocks not fully extracted (Heron Brook
  runtime injection, subagent steering). Six worst-offender candidates
  flagged. Blocker: Block 19 (Heron Brook) content fetched at runtime
  from remote service — content unknown from binary analysis.
  Extraction method: `strings` on compiled ELF binary (ASCII + UCS-2),
  code-read of minified JS, behavioral probe. Key difference from
  codex-hijack: stock context is programmatically assembled from
  template functions, not stored in readable prompt files. Both
  hijack repos added to repos-manifest.dotos. Machinery note:
  meta-orchestrate lane registration refused the attempted DOTOS
  (same as codex-hijack); work proceeded on advisory basis.

## Open

- Codex block walk started: one block at a time, psyche marks each for
  replacement or deletion (vision/hijackRepositories.md). Scope ruled:
  only 5.6 — the stock context actually served to the 5.6 model in
  this setup. No compiled-in 5.6 variant exists at 0.149.1; subflow in
  flight to establish the actual 5.6 base context verbatim (selection
  logic plus live capture) and land it in codex-hijack. The Autonomy
  and Persistence block presentation is paused until the 5.6 context
  is in hand; no mark given.
- 5.6 context obtained (reports/codex56Context.md): model gpt-5.6-sol
  witnessed; served by server-catalog instructions_template (17730
  chars, byte-identical across sol/terra/luna), captured from
  ~/.codex/models_cache.json, landed verbatim in codex-hijack. The 5.6
  autonomy section is rewritten and largely aligned (request-type
  scopes, stop-and-report on blockers) — no longer the worst offender.
  New most-harmful pick presented to the psyche: the Personality block
  ("another subjectivity", own tastes) as the direct inversion of the
  extension model. Psyche corrected the diagnosis
  (vision/subjectivity.md): the psyche is a bunch of internal
  dialogues, so subjectivity itself is not the problem — the block's
  opinionation is. Mark given: Personality → replace, replacement TBD
  (recorded in codex-hijack stock-context/MARKS.md). Block 2
  presented: the Using-skills section (lines 133–167), the template's
  most opinionated block, colliding with the authored skill system
  (persistence across turns, context-triggered loading, subflow
  delegation). Review in progress: skills-persistence line marked
  Delete; global replacement-vocabulary ruling landed (agent→flow,
  vision/flow.md); psyche's question on $SkillName programmatic
  mechanics answered by witness
  (witnesses/codexSkillMentionMechanics.md): the $ mention is
  programmatically active at 0.149.1 — harness parses the token,
  reads the matched SKILL.md, and injects the full body as a
  user-role fragment for that turn. The stock skills-block procedure
  governs the fallback path (catalog-triggered, unmentioned skills).
  Unknowns: server-side <skill> tag handling, MentionsV2 flag ($ vs @
  sigil), dynamic skill selector firing conditions.
- From 2f6b1dc5, still unruled: Block 1 (completion/autonomy pressure)
  replacement proposal awaits the psyche's ruling; the
  offensive-corpus block walk continues from there; the full
  base-context replacement composition is not yet written.
- The silent working-copy loss pattern (two witnessed instances in
  2f6b1dc5, plus aa4c7747's index line) remains unruled as a pattern;
  01a035fb investigated the mechanism.
