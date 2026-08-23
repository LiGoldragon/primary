# OpenAI skills review

The parent session exposes sixteen OpenAI-supplied skills: five system skills and eleven plugin-contributed skills. Physically installed or cached skills absent from the session catalog are outside this inventory.

## Recommendation

These verdicts are inferences from the written psyche, not rulings by the living.

Keep the narrow production and observation capabilities: `imagegen`, `browser:control-in-app-browser`, `documents:documents`, `pdf:pdf`, `presentations:Presentations`, `spreadsheets:Spreadsheets`, and `visualize:visualize`. They add bounded capabilities without choosing the system's authority, repository ownership, or deployment platform.

Disable the authority, installation, and platform-shaping skills: `openai-docs`, `plugin-creator`, `skill-creator`, `skill-installer`, `plugin-management:plugin-management`, `sites:sites-building`, `sites:sites-hosting`, and `template-creator:template-creator`. They can compete with local management and research discipline, bypass authored Curriculum/manifests, expand external capability, or prescribe an OpenAI-owned platform.

Disable `spreadsheets:excel-live-control` unless a connected live Excel workflow is deliberately wanted. The standalone spreadsheet capability remains available, while an unused external live-control path adds machinery without evidence of a need.

## Blanket control

The local probe verified that, in a new session, these controls remove the tested system and plugin representatives and the recommended-plugin block; the configuration semantics are class-level controls:

```toml
[features]
plugins = false

[skills.bundled]
enabled = false
```

The existing `[features]` table must be amended, not duplicated. `plugins = false` disables every plugin, including non-OpenAI integrations such as GitHub and Gmail. The bundled-skills setting disables all system skills. Neither control deletes caches, disconnects credentials, or changes an already-running session.

The session-only equivalent is:

```sh
codex --disable plugins -c 'skills.bundled.enabled=false'
```

Granular `[[skills.config]]` entries can disable named skills individually. No wildcard or OpenAI-publisher-only deny rule was verified. `include_instructions = false` only suppresses automatic prompt injection; it is not a disable/security boundary.

## Sources

- Witness: `flows/01a030df/witnesses/codexSkillDisableControls.md`
- OpenAI system skill sources under `/home/li/.codex/skills/.system/`
- OpenAI plugin manifests and skill sources under `/home/li/.codex/plugins/cache/openai-*`
- `/home/li/primary/psyche-raw/Vision/gradientsOfAuthority.md`
- `/home/li/primary/flows/e4be1c4a/vision/skillTypes.md`
- `/home/li/primary/psyche-raw/Vision/domainKnowledgePlacement.md`
- `/home/li/primary/flows/a60a9e85/vision/skillDesigning.md`
- OpenAI Codex configuration reference: https://developers.openai.com/codex/config-reference/
- OpenAI Codex skills configuration source: https://github.com/openai/codex/blob/main/codex-rs/config/src/skills_config.rs
- OpenAI plugin guide: https://learn.chatgpt.com/docs/plugins
- Remembered flow `01a02f74`
- Current-state follow-up flow `01a030a1`
