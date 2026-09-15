# Session titles

The Claude remote session’s human-readable title is separate from its stable UUID. Official Claude Code documentation gives title precedence as explicit Remote Control name, `/rename` title, meaningful conversation message, then auto-generated title. Without an explicit name, the title can update after prompts; remote renaming propagates to the CLI on supported versions. The current local Claude transcript for session `942914a6-93d5-41ba-95bf-fa98ee557b09` contains `ai-title` values changing from `spirit skill initialization` to `spirit skill principles`, consistent with auto-title revision rather than UUID replacement.

The internal flow naming records support stable short identifiers independently of display names. [`flows/e1953c/vision/flowIdentity.md`](/home/li/primary/flows/e1953c/vision/flowIdentity.md) assigns cluster/pair identity to the first characters and a short session fragment; [`flows/7c3f0c1d/vision/sessionLog.md`](/home/li/primary/flows/7c3f0c1d/vision/sessionLog.md) says a session short ID is created at first prompt and never renamed.

Current Codex read-only state: root thread `01a0a5c3-82a5-79f3-a61a-e365f4fea54f` has persisted metadata `title: null`; this subflow thread `01a0617-dc7a-7b71-b630-5ee7a38a5787` also has `title: null`. `codex --help` exposes resume/archive/delete by ID or name and no start-time `--name` flag. The CLI supports `/rename` according to OpenAI’s public repository issue history, but no rename was issued and no claim is made about this current thread’s display surface.

## Sources

- [`flows/e1953c/vision/flowIdentity.md`](/home/li/primary/flows/e1953c/vision/flowIdentity.md).
- [`flows/7c3f0c1d/vision/sessionLog.md`](/home/li/primary/flows/7c3f0c1d/vision/sessionLog.md).
- [`flows/692df8/vision/sessionNames.md`](/home/li/primary/flows/692df8/vision/sessionNames.md).
- [Claude Code, Manage sessions](https://code.claude.com/docs/en/sessions).
- [Claude Code, Remote Control](https://code.claude.com/docs/en/remote-control).
- [OpenAI Codex issue #9471](https://github.com/openai/codex/issues/9471), CLI `/rename` status.
