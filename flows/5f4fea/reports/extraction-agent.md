# Extraction agent proposal

The exact logging records distinguish direct transcript custody from later extraction. [`flows/692df8/vision/logging.md`](/home/li/primary/flows/692df8/vision/logging.md) says to “leave all of this detail extraction to a subflow” and asks for a “tiny little system prompt agent for a specialized case with just the minimum it needs to know,” “like a targeted program.” [`flows/692df8/notion/logging.md`](/home/li/primary/flows/692df8/notion/logging.md) explores a user-input hook that starts a small distilling subflow, but remains notion and authorizes no hook implementation.

The excluded draft is committed at `/home/li/wt/github.com/LiGoldragon/Curriculum/psyche-extractor-git/design/AgentOps/psyche-extractor.md`. It is not installed or activated. The current Curriculum generator reads role manifests and emits the generated role matrix; it has no standalone custom-agent source. Existing generated `.claude/agents/` packets and `skills/generated-role-outputs.dotos` remain untouched.

The candidate is deliberately targeted. The caller supplies the exact transcript selector, target flow/topic, provenance, and typed or speech-to-text modality. The agent reads only that passage and the existing target as data, preserves the living words verbatim, skips work orders/process/events/acknowledgments, uses Notion when the living frames exploration and otherwise captures stated design as Vision, and appends oldest-first while preserving existing destination content. `Read`, `Edit`, and `Write` are the requested native capability set; no `Skill` tool or skills are supplied.

The draft contains `omitClaudeMd: true` as an explicit future prerequisite. Claude Code 2.1.263 is installed locally; current official docs require 2.1.271 or later for that field. Local verified evidence reports that custom bodies do not eliminate all harness-composed context, so the candidate makes no runtime-isolation claim.

Token estimate: 157 words in the candidate body and frontmatter, approximately 215–245 tokens by word estimate. The surrounding design wrapper is additional prose. No tokenizer was available or invoked. No activation or runtime test was performed. The candidate uses `maxTurns: 4` to cover transcript read, target read, append edit, and completion.

## Sources

- [`flows/692df8/vision/logging.md`](/home/li/primary/flows/692df8/vision/logging.md), read in full.
- [`flows/692df8/notion/logging.md`](/home/li/primary/flows/692df8/notion/logging.md), read in full.
- [Anthropic, Create custom subagents](https://code.claude.com/docs/en/sub-agents), frontmatter, body, tools, skills, and `omitClaudeMd` behavior.
- [`verified/claude-code-context.md`](/home/li/primary/verified/claude-code-context.md), prior local runtime evidence.
- `/home/li/wt/github.com/LiGoldragon/Curriculum/FixNixSkills/AGENTS.md` and `src/assembly.rs`, authored generator boundary.
