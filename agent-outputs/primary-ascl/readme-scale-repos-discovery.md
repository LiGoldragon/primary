# README Scale Repos Discovery

Task: work bead `primary-ascl.6`, discovery only. Scope was local public project/tracker/agent-output history for existing public skill-repo comparison, scale/serious repo list, influence/reference notes, or README draft material. I did not edit README or source files and did not inspect `private-repos/`.

## Commands and files consulted

- `read /home/li/primary/AGENTS.md`
- `spirit "(PublicTextSearch [README scale repos influence reference skill comparison])"`
- `pwd && ls -la && find agent-outputs -maxdepth 3 -type f ...`
- `bd show primary-ascl.6`
- `bd search README -n 20 --long`, `bd search "scale repos" -n 20 --long`, `bd search influence -n 20 --long`
- `rg -n --hidden --glob '!private-repos/**' --glob '!**/.git/**' --glob '!**/.jj/**' --glob '!result/**' -i ...`
- `find agent-outputs/primary-ascl -maxdepth 1 -type f ...`
- `find agent-outputs/SkillBenchmark -maxdepth 1 -type f -exec wc -l ...`
- `find . ... -iname '*readme*' -type f`, excluding `private-repos`, `.git`, `.jj`, and `result`
- `rg` over public README files for `influence|reference|similar|scale|serious|Claude Skills|Cursor|Windsurf|Continue|Aider|OpenAI|Google|AutoGen|Semantic|Simon|Total TypeScript`
- `read` / `nl -ba` on:
  - `/home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md`
  - `/home/li/primary/agent-outputs/SkillBenchmark/Researcher-PublicPatterns.md`
  - `/home/li/primary/agent-outputs/SkillBenchmark/Reviewer-LocalPatterns.md`
  - `/home/li/primary/agent-outputs/orchestration-weave/naming-orchestration-spirit-bundle-retry.md`
  - `/home/li/primary/repos/skills/README.md`
  - `/home/li/primary/repos/skills-primary-ascl-doctrine/README.md`
- `jj status --no-pager`

One exploratory `bd search ... --no-pager` command failed because `bd search` has no `--no-pager` flag; I reran the tracker searches successfully without that flag.

## Observed facts

### Tracker and intent context

- `bd show primary-ascl.6` says the task is `Investigate README scale repos and actual influence labels`; definition of done is to investigate whether a comparison/list exists, report scale repositories and which are actual influences, and propose README update scope or no-change rationale. It explicitly says discovery first, do not invent influence claims, avoid private leakage, and no README edits.
- `agent-outputs/orchestration-weave/naming-orchestration-spirit-bundle-retry.md:16-18` defines the parent bundle as including a README scale-repo influence backlog. Lines `43-45` define `primary-ascl.6` as first investigating whether comparison/list exists, listing scale repos, and labeling only actual influences. Line `75` says to dispatch it as lower-priority README backlog work or before final audit.
- `bd search README -n 20 --long` found four README-related beads: `primary-ascl`, `primary-ascl.6`, `primary-ascl.7`, and unrelated `primary-iy51.11`. `bd search "scale repos"` and `bd search influence` each found only `primary-ascl.6`.
- Spirit public text search returned records `k09z` and `n9fl`. `k09z` is a privacy constraint; `n9fl` is an agent-systems principle. Neither is a README-specific approval or direct influence-label source. This supports privacy caution but does not answer actual influence labeling.

### Existing comparison/list output exists

Yes. The direct prior output is `/home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md`.

Important content:

- Lines `3-6`: summary says public AI instruction systems favor task/domain nouns for reusable capabilities and role nouns for agents; local direction is strong on operational doctrine, privacy boundaries, output discipline, and VCS/worktree rules; limitation says no live web search, clone, or public repo inspection was available in that run.
- Lines `8-23`: findings compare local direction to Claude Skills, Cursor, Windsurf, Continue, Aider, OpenAI Agents SDK, Google ADK, AutoGen, Semantic Kernel, Simon Willison `llm`, Cursor community rules, and Total TypeScript/Matt Pocock.
- Lines `25-34`: comparison table maps public/acclaimed patterns to local observed patterns and README recommendations.
- Lines `48-56`: list of categories public repos have that local may lack or could expose better: language/framework rule packs, security checklists, evaluation/benchmark recipes, prompt templates, tool config examples, skill package examples, and learning/study modes.
- Lines `58-67`: list of local differentiators ready to advertise: explicit private/public boundary, output/report discipline, doctrine loading economy, `jj` VCS policy, intent capture safeguards, and no `/nix/store` search.
- Lines `69-91`: concrete README wording/pattern recommendations: compact glossary, package convention, naming guidance, progressive-disclosure sentence, and only examples for categories actually present.
- Lines `93-109`: a draft README section headed `Similar repositories and influences` with suggested entries.
- Lines `111-128`: source list and dropped-source rationale.
- Lines `130-135`: gaps, including no live web search/clone/current GitHub inspection and a note that Matt Pocock/Total TypeScript phrasing needs targeted verification before direct influence claims.

Supporting outputs also exist:

- `/home/li/primary/agent-outputs/SkillBenchmark/Researcher-PublicPatterns.md` is a public-pattern research brief. Lines `3-5` summarize the strongest models as Anthropic Claude Skills, Cursor/Windsurf/Continue, Aider, and OpenAI/Google/Microsoft guidance. Lines `7-23` list influential examples and their roles. Lines `47-57` give concrete local recommendations. Lines `68-86` list sources. Lines `88-91` explicitly say no live web search was available, star counts/acclaim were not verified, and a live pass over GitHub star counts/current docs remains a next step.
- `/home/li/primary/agent-outputs/SkillBenchmark/Reviewer-LocalPatterns.md` is the local-side benchmark/audit. Lines `5-11` summarize inspected generated skill/role surfaces. Lines `13-20` give a comparison-ready local strength summary. Lines `22-29` list local weaknesses with severity. Lines `43-50` classify worker doctrine that should move to role composition. Lines `78-82` disclose residual risks and say private repositories were not inspected.

Other references found:

- `/home/li/primary/agent-outputs/ContextHandoverRedesign/SkillEditor-Acceptance.md:70` and `/home/li/primary/agent-outputs/OrchestrationRename/SkillEditor-Result.md:77` reference `agent-outputs/SkillBenchmark/PublicRepoComparison.md`, but targeted search did not show additional README scale/influence content in those files.

### Existing README draft material

A draft exists only as report text, not in a README:

- `/home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md:93-109` proposes heading `Similar repositories and influences` and lists entries.
- Public README files found by `find`, excluding private paths, were `.beads/README.md`, `.claude/worktrees/nota-codec-mockup-2/README.md`, `.claude/worktrees/nota-codec-mockup-2/.beads/README.md`, `repos/skills-primary-ascl-doctrine/README.md`, `repos/skills/README.md`, and `repos/spirit-guardian-config/README.md`.
- Targeted README search for influence/reference/similar/scale/serious and named external systems produced no matches in `repos/skills/README.md` or `repos/skills-primary-ascl-doctrine/README.md`.
- `repos/skills/README.md:1-49` and `repos/skills-primary-ascl-doctrine/README.md:1-49` are currently the same short generator overview: regeneration/check commands, manifest/module paths, source module kinds, role output paths, and pruning/staleness behavior. They contain no similar-repositories, references, or influences section.

## Interpretation

- Existing comparison/list output does exist and is likely the intended pickup surface for later README work: `agent-outputs/SkillBenchmark/PublicRepoComparison.md` plus its two supporting SkillBenchmark reports.
- The existing draft heading `Similar repositories and influences` is not fully aligned with the clarified psyche direction. Because the psyche now says README should eventually list scale/serious repos as references and only call repos influences if they actually influenced the work, the safer implementation heading is likely `Similar repositories and references` or `References and related systems`, with an optional smaller `Influences` subsection only for verified direct influences.
- Most entries in `PublicRepoComparison.md:99-108` are ready as references or comparisons, not as direct influences. The report itself uses wording such as closest packaging analogy, useful distinction, parallel model, good precedent, reinforces, useful terminology, strong example, broad examples, and useful comparison. Those phrases support neutral reference labels.
- `PublicRepoComparison.md:19` and `:109` treat Total TypeScript/Matt Pocock docs-grounded learning style as a useful influence, but `:134` and acceptance residual risk `:178` say it requires targeted verification before being framed as direct influence. So it is not ready for an unqualified README influence claim.
- `Researcher-PublicPatterns.md:23` says awesome lists are discovery indexes, not design authority. They should not be elevated into README influence language.

## Ready for later README/reference implementation

Ready with neutral reference wording:

- Anthropic Claude Skills: packaging analogy for `SKILL.md`, optional support files, noun/task names, progressive disclosure. Evidence: `PublicRepoComparison.md:99`, `Researcher-PublicPatterns.md:7`, `:31`, `:69`.
- Cursor Rules and Memories: reference for scoped/project/user rules and remembered context boundaries. Evidence: `PublicRepoComparison.md:100`, `Researcher-PublicPatterns.md:9`, `:71`.
- Windsurf rules/memories: reference/parallel for persistent rules and memories. Evidence: `PublicRepoComparison.md:101`, `Researcher-PublicPatterns.md:11`, `:72`.
- Continue: reference for declarative config, context providers, slash commands, and model/tool config separate from prose rules. Evidence: `PublicRepoComparison.md:102`, `Researcher-PublicPatterns.md:13`, `:73-74`.
- Aider conventions: reference for terse repo-level coding-agent conventions and examples. Evidence: `PublicRepoComparison.md:103`, `Researcher-PublicPatterns.md:15`, `:75-76`.
- OpenAI Agents SDK/Codex guidance: reference for tool clarity, sandboxing, environment contracts, agents/tools/handoffs/guardrails/tracing separation. Evidence: `PublicRepoComparison.md:104`, `Researcher-PublicPatterns.md:17`, `:77-78`.
- Google ADK: reference for agent/tool/session/artifact/memory/eval vocabulary. Evidence: `PublicRepoComparison.md:105`, `Researcher-PublicPatterns.md:19`, `:79`.
- Microsoft AutoGen and Semantic Kernel: references for multi-agent role/capability boundaries and plugins/tools/functions. Evidence: `PublicRepoComparison.md:106`, `Researcher-PublicPatterns.md:19`, `:80-81`.
- Simon Willison `llm` templates: reference for named reusable prompt templates with arguments. Evidence: `PublicRepoComparison.md:107`, `Researcher-PublicPatterns.md:21`, `:82-83`.
- Cursor community rule repositories and `awesome-cursorrules`: reference/discovery examples only, not quality baseline or influence. Evidence: `PublicRepoComparison.md:108`; caution at `PublicRepoComparison.md:23` and `Researcher-PublicPatterns.md:23`.

Ready local differentiator content:

- `PublicRepoComparison.md:58-67` gives concise local differentiators suitable for a README paragraph.
- `PublicRepoComparison.md:69-91` gives implementation-ready wording patterns: glossary, package convention, naming guidance, progressive disclosure sentence, and warning to avoid empty taxonomy.
- `Reviewer-LocalPatterns.md:13-20` gives local strength phrasing against external patterns.

Not ready as influence without more evidence:

- Total TypeScript/Matt Pocock docs-grounded learning. Prior output suggests it may be an influence, but also explicitly says targeted verification is required before claiming direct influence. Treat as `possible influence, unverified` or omit from an `Influences` subsection until verified.
- All other listed systems should be treated as references, similar systems, or design comparisons unless the psyche or a durable source identifies actual causal influence.

## Open questions and missing evidence

- Which public projects actually influenced this work? Local public history searched here does not answer that beyond the weak/unverified Total TypeScript/Matt Pocock note.
- Which README is the implementation target? The likely source README is `repos/skills/README.md`; `repos/skills-primary-ascl-doctrine/README.md` is an additional public worktree with an identical README. The bead does not explicitly name the target path.
- No current star counts, current GitHub file trees, or live public repository states were verified in the prior SkillBenchmark outputs. This scout did not perform web verification because the assigned scope was local history discovery.
- Private paths were not inspected. If the only direct influence evidence lives in private chat/repo material, it remains unavailable for public README wording unless the psyche explicitly authorizes a public-safe summary.
- The prior comparison report did not inspect the full local source tree in its own run; the supporting local audit partially fills that gap for generated runtime skills/roles, but source-side README implementation still needs source-of-truth review before editing.

## Blockers and review findings

- blocker: none for this discovery task; the requested comparison/list output was found.
- high: direct influence labels are not supported by local public evidence for most listed systems. Later README implementation must use reference/comparison language unless actual influence evidence is supplied.
- medium: `PublicRepoComparison.md:93-109` draft heading includes `influences`; update wording before use to avoid overstating causality.
- medium: prior external comparison outputs lacked live web/search/clone verification (`PublicRepoComparison.md:6`, `:130-135`; `Researcher-PublicPatterns.md:88-91`). Current popularity, star counts, and exact current repo structures are residual risks if README needs "scale/serious" proof.
- low: target README path is ambiguous between `repos/skills/README.md` and the duplicate `repos/skills-primary-ascl-doctrine/README.md`; implementation should confirm source-of-truth before editing.

## Not checked

- I did not inspect `private-repos/` or private chat/session scopes.
- I did not edit source files, README files, tracker state, or generated runtime surfaces.
- I did not run tests or generators.
- I did not fetch live web pages, clone public repos, or verify current GitHub popularity metrics.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Found existing comparison/list output at /home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md, plus supporting reports /home/li/primary/agent-outputs/SkillBenchmark/Researcher-PublicPatterns.md and /home/li/primary/agent-outputs/SkillBenchmark/Reviewer-LocalPatterns.md; review findings include severity-labeled blockers/risks."
    }
  ],
  "changedFiles": [
    "/home/li/primary/agent-outputs/primary-ascl/readme-scale-repos-discovery.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "read /home/li/primary/AGENTS.md",
      "result": "passed",
      "summary": "Read local workspace instructions."
    },
    {
      "command": "spirit \"(PublicTextSearch [README scale repos influence reference skill comparison])\"",
      "result": "passed",
      "summary": "Returned public records k09z and n9fl; neither was README-specific influence approval."
    },
    {
      "command": "bd show primary-ascl.6",
      "result": "passed",
      "summary": "Confirmed discovery-only scope and no-invented-influence constraint."
    },
    {
      "command": "bd search README -n 20 --long; bd search \"scale repos\" -n 20 --long; bd search influence -n 20 --long",
      "result": "passed",
      "summary": "Found primary-ascl.6 as the only scale/influence tracker hit; README search also found parent/audit and unrelated primary-iy51.11."
    },
    {
      "command": "rg searches excluding private-repos, .git, .jj, and result for scale/serious/readme/influence/reference/public-skill terms",
      "result": "passed",
      "summary": "Located SkillBenchmark comparison reports and primary-ascl tracker-weave references."
    },
    {
      "command": "find public README files excluding private-repos/.git/.jj/result and rg README influence/reference terms",
      "result": "passed",
      "summary": "Found public README files; no influence/reference/similar/scale section in repos/skills README copies."
    },
    {
      "command": "read/nl selected SkillBenchmark reports and README files",
      "result": "passed",
      "summary": "Collected line-backed summaries of existing comparison, reference list, README draft, and gaps."
    },
    {
      "command": "jj status --no-pager",
      "result": "passed",
      "summary": "Observed pre-existing unrelated agent-output working-copy changes before writing this report."
    },
    {
      "command": "jj status --no-pager",
      "result": "passed",
      "summary": "Post-write status showed this report added plus pre-existing unrelated agent-output changes; no README/source edits."
    }
  ],
  "validationOutput": [
    "Report written to /home/li/primary/agent-outputs/primary-ascl/readme-scale-repos-discovery.md.",
    "Discovery found prior comparison/list output; no README/source edits were made.",
    "Post-write jj status lists agent-outputs/primary-ascl/readme-scale-repos-discovery.md as added; other listed changes pre-existed this scout."
  ],
  "residualRisks": [
    "high: actual direct influence evidence remains missing for most listed systems; later README work should use reference/comparison language unless new evidence is supplied.",
    "medium: prior external reports lacked live web/clone/current-star verification, so 'scale/serious' claims may need a live pass before publication.",
    "medium: target README source-of-truth path is not explicitly named in the bead.",
    "low: private evidence was intentionally not inspected."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added discovery report only; no README or source changes.",
  "reviewFindings": [
    "no blockers for discovery: comparison/list output exists at /home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md",
    "high: direct influence labels are unsupported for most listed systems; use references/comparisons unless actual influence evidence is supplied",
    "medium: /home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md:93-109 uses an influences-inclusive heading that should be revised before README use",
    "medium: /home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md:6,130-135 and /home/li/primary/agent-outputs/SkillBenchmark/Researcher-PublicPatterns.md:88-91 disclose no live web/clone/star-count verification",
    "low: likely README target is /home/li/primary/repos/skills/README.md, but the bead does not explicitly confirm it"
  ],
  "manualNotes": "Private paths were not inspected. Later implementation can reuse the SkillBenchmark reference list, but should change the section framing to references/similar systems and only create an Influences subsection for verified causal influences."
}
```
