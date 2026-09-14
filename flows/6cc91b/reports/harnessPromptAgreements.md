# Harness system-prompt agreements

Subflow of 6cc91b, answering: "What have we agreed on most to change
about the system prompts of the default harnesses? What are we going
to put in the open source one?"

## 1. The living's statements, verbatim, newest first

> What have we agreed on most to change about the system prompts of
> the default harnesses? What are we going to put in the open source
> one? Let's have a draft of the open source stack, which is entirely
> self-authored. Let's be honest about how I work and ask me questions
> about how I view how to work, how the law should be laid, and how
> behavior should be, which is in nuclei right now, in our skills and
> in our vision.
-- flows/6cc91b/vision/openSourceStack.md, 2026-09-14

> Today, what is the best open-source stack with remote control,
> essentially the open-source Claude and Codex with a remote control
> solution?
-- flows/6cc91b/vision/openSourceHarness.md, 2026-09-13

> if you do the harness right and you give the right ontology and
> guidance, you can make any model in the right harness ...
-- flows/6cc91b/vision/openSourceHarness.md, 2026-09-13

> It's just the concept that we're going to start flows using a Nexus
> component, which will decide what the system prompt is and
> everything. We're going to replace the harness's concept of
> subagents with this component, which will have specialized harnesses
> launched with specialized system prompts.
-- flows/1a6ca4/vision/archive-nexus.md, 2026-09-05

> the persona meta-harness is going to bring in the dawn of the more
> complete thinking machine systems ...
-- flows/1a6ca4/vision/personaMetaHarness.md, 2026-09-05

> We should just create a separate repository that anyone could use to
> give modified versions with different names of Claude and Codex,
> with different takes on system prompts.
-- flows/38dec9/vision/systemPromptRepository.md

> I would probably just rename the executable ... call the wrapper
> something else, like Claude Light or Claude Unopinionated, or maybe
> Codec Unsafe if we take all the safety out ... or Codec Bare.
-- flows/38dec9/vision/perHarnessSkills.md

> There may be some things that I want to remove in all harnesses that
> we could do universally and just replace.
-- flows/38dec9/vision/perHarnessSkills.md

> [Codex Autonomy-and-persistence block] this overlaps with our own
> skills ... it's a bit thin and spread wide ... they're trying to make
> a single flow do the job of several flows ... trying to cram too much
> into a single flow, and it's breaking the flow.
-- flows/ceb3b9fd/vision/topStratum.md, 2026-08-30

> mark as replace, at least in parts.
-- flows/ceb3b9fd/vision/hijackRepositories.md, on Codex's
   "Working with the user" block, 2026-08-30

> we're going to have different top stratums for different jobs. The
> top stratum will be programmable per flow.
-- flows/ceb3b9fd/vision/topStratum.md, 2026-08-30

> even the harnesses are kind of actually told to [copy code they
> already find]. And actually, that's one of the things I want to
> change in the base prompt. I don't think that that's a good thing
> ... because if there's bad things and bad things get copied.
-- flows/aa4c7747/vision/basePrompt.md, 2026-08-24

> Let's look at the most offensive base prompt blocks first, and
> design replacement for each, and work our way through the entire
> offensive corpus like this
-- flows/2f6b1dc5/vision/systemPrompt.md, 2026-08-23

> I want to replace claude and codex's system prompts with a version
> that doesnt incentivize the sort of behavior im constantly steering
> against. The system/base prompt ... has the highest context priority
> and is currently full (I suspect) of instructions that are
> completly or even partly against my philosophy and approach to LLM
> usage.
-- flows/2f6b1dc5/vision/systemPrompt.md, 2026-08-23 (founding statement)

> I think we should really consider replacing both Claude and Codex's
> harness' system prompts with some heavy modifications ... [training
> against false confidence, rewarding admission of ignorance]
-- flows/358f143a/vision/falseConfidence.md, 2026-08-17

> essentially the analogs of what the basic harness training prompt is
> currently that is built into the harnesses, which we will completely
> [replace] ... behave in a harness, but with our own take on it.
-- flows/e06e4c07/vision/archive-flowDaemon.md, 2026-08-19

## 2. What the skills already assert

- claude-harness: "Claude Code's top stratum is the system prompt.
  The --system-prompt and --system-prompt-file flags replace the
  whole of it ... CLAUDE.md and the other entry files ... are middle
  stratum ... The living witnesses the stock system prompt only
  through the machine's transcription of it." Replacing it "removes
  its behavioral guidance and nothing else" — permissions, hooks,
  entry-file injection, training persist.
  /git/github.com/LiGoldragon/Curriculum/skills/claude-harness.md
- codex-harness: "Codex's top stratum is the base instructions, sent
  as the instructions field ... The model_instructions_file config
  key replaces the base instructions ... the source discourages
  both, and we use the file." Both the living and the machine can
  read it.
  /git/github.com/LiGoldragon/Curriculum/skills/codex-harness.md
- context-strata: "The top stratum is the base context ... Universal
  invariants belong here ... Harness seizure is authoring the top
  stratum ourselves."
  /git/github.com/LiGoldragon/Curriculum/skills/context-strata.md
- spirit: carries the invariants (extension-of-psyche framing, no
  backward compatibility, admit not-knowing, seek disconfirming
  evidence) the living has repeatedly said belong at the top stratum
  of a replaced prompt.
  /git/github.com/LiGoldragon/Curriculum/skills/spirit.md

## 3. Agreed changes, most-said/most-recent first

1. Replace both stock system/base prompts outright — founding
   decision, restated at least four times. flows/2f6b1dc5/vision/
   systemPrompt.md (08-23), flows/358f143a/vision/falseConfidence.md
   (08-17), flows/e06e4c07/vision/archive-flowDaemon.md (08-19).
2. Work block-by-block, worst offenders first, marking each
   replace/keep/replace-in-parts. flows/2f6b1dc5/vision/systemPrompt.md;
   enacted in flows/ceb3b9fd/vision/hijackRepositories.md and
   flows/4ddc321d/reports/{codexHijackRepo,claudeHijackRepo}.md.
3. Drop the "reward false confidence" shape; train toward admitting
   ignorance. flows/358f143a/vision/falseConfidence.md (08-17).
4. Stop instructing the model to copy code it finds in the repo.
   flows/aa4c7747/vision/basePrompt.md (08-24).
5. Replace Codex's "Autonomy and persistence" block: crams several
   flows' jobs into one, undefined "evidence." flows/ceb3b9fd/vision/
   topStratum.md (08-30).
6. Replace, in parts, Codex's "Working with the user" block: keep
   channel/compaction facts and a rare-commentary rule, drop the
   60-second decree and assumption mandate. flows/ceb3b9fd/vision/
   hijackRepositories.md (08-30).
7. Replace imposed personality/tone prescriptions and output-
   formatting/verbosity rules — flagged worst-offender by the
   extraction subflow, not yet a direct psyche ruling.
   flows/4ddc321d/reports/codexHijackRepo.md.
8. Per-flow, per-job top strata instead of one prompt for everything.
   flows/ceb3b9fd/vision/topStratum.md (08-30), flows/1a6ca4/vision/
   archive-nexus.md (09-05).
9. Put spirit's (and behavior's) content in the highest reachable
   stratum; practically landed as an entry-files top section (middle
   stratum), not a system-prompt rewrite, pending the meta-harness.
   flows/358f143a/vision/behavior.md (08-17), vision-raw/spirit.md
   (08-22).
10. Publish a separate open-source repository offering modified,
    differently-named Claude/Codex builds ("Claude Light/
    Unopinionated", "Codex Unsafe/Bare"). flows/38dec9/vision/
    systemPromptRepository.md, flows/38dec9/vision/perHarnessSkills.md.
11. Longer-range: a persona meta-harness / Nexus component decides
    each flow's system prompt at launch, replacing subagents with
    specialized harnesses. flows/1a6ca4/vision/personaMetaHarness.md,
    flows/1a6ca4/vision/archive-nexus.md (both 09-05).
12. Today: the open-source stack is to be entirely self-authored, its
    content drawn from asking the living directly how work, law, and
    behavior should be laid out — not inferred solely from existing
    skills/Vision. flows/6cc91b/vision/openSourceStack.md (09-14).

## 4. Implemented vs. only stated

Implemented:
- Entry files (CLAUDE.md, AGENTS.md, NON_MANAGEMENT_AGENTS.md,
  SKILL_VARIABLES.md) at primary's root, generated from Curriculum's
  authored AGENTS.md, distributed as middle stratum on both harnesses.
- Generated per-harness trees (.claude/, .agents/, .codex/) carrying
  claude-harness, codex-harness, context-strata, spirit as skills
  (middle stratum), not top.
- Two public extraction repos with verbatim stock prompt text and a
  block inventory: /git/github.com/LiGoldragon/codex-hijack (17
  blocks, Codex 0.149.1 source) and /git/github.com/LiGoldragon/
  claude-hijack (21 system-prompt blocks + 8 system-reminders,
  extracted from the Claude Code 2.1.241 binary). Each holds only
  README + stock-context/ — stock text, not replacement text.
- A few Codex blocks individually marked replace / replace-in-parts
  in flows/ceb3b9fd/vision/{hijackRepositories,topStratum}.md.
- flows/7b4d4c/reports/proposal.md: a 382-line harness-anatomy
  proposal comparing all three strata across Claude Code, Codex, and
  dsh, with F1-F22 open forks — drafted, not ruled block-by-block.

Only stated, no artifact yet:
- No replacement system-prompt or base-instructions file drafted or
  committed for either harness; --system-prompt-file /
  model_instructions_file not wired into any launch config in primary.
- No open-source stack repository (today's ask) exists.
- The persona meta-harness / Nexus component is unbuilt (an empty,
  remote-less local git directory named `persona`, per flows/7b4d4c/
  reports/proposal.md).
- No "Claude Light/Unopinionated" or "Codex Unsafe/Bare" wrapper
  exists.
- Personality/tone and output-formatting blocks are flagged but not
  yet marked replace/keep by the psyche directly.

## 5. Unknowns

- Whether the worst-offender rankings in flows/4ddc321d/reports/
  {codexHijackRepo,claudeHijackRepo}.md have since been ruled on by
  the psyche directly, or remain the flow's own reading.
- Whether flows/7b4d4c/reports/proposal.md's F1-F22 forks were later
  resolved in a flow not surfaced by this search.
- Whether "open source Claude and Codex" (09-13/14) means the
  codex-hijack/claude-hijack repos become the open-source stack, or a
  new repository is intended.
- What specific replacement wording exists today for blocks already
  marked "replace" — none found; the hijack repos hold only stock text.
- Whether entry-files placement of spirit/behavior is the final
  answer to "top stratum," or a stopgap pending the meta-harness — the
  record carries both framings without an explicit reconciling ruling.
