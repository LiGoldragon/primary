<!-- to-the-living:start -->
Presentation.{ «Flow today» }

## 1. `psyche-skills/skills/vision-flow.md`, before the section «Sources»

Lines removed: none. Lines added:

```
## Today

Witnessed 2026-10-07 to 09. Claude Code 2.1.294
(Home Manager generation 1057); Codex 0.158.0-alpha.9
and codex-next 0.161.0-alpha.2; Herdr exposes no
per-seat version. The Flow repository is 0.24.0, six
crates, most in flow-nexus; it composes the system
prompt and first prompt from caller-supplied paths,
has Replace, an events store on disk and hooks that
report Started, ToolUsed and Stopped; it has no
Memory root, no metaflow record, no lock, no module
registry and reads no context size. Main flows are
launched by the Primary scripts: the Claude launcher
passes a system prompt file and a first prompt that
opens with six slash skills from .claude/skills; the
Codex launcher reads .agents/skills SKILL.md files
into the first prompt; both take --topic, Core by
default, with continuation inheritance, since
897984 on main. The flow id is minted by flow-id as
six hex characters of the harness session id. The
authored skills live in psyche-skills, mind-skills
and field-skills under skills/. Messages go through
messenger-clj, which routes from its own store and
types into Herdr panes; the Orchestrate nexus runs
0.37.0 and Message's daemon is down.
```

Ruling 1: yes, or amend.
<!-- to-the-living:end -->
