# Default effort provenance

## Living direction

The exact living direction is preserved in
`/home/li/primary/flows/908786/vision/default-effort.md`: medium is the default
effort for every model and every subflow. This work did not restart a running
session.

## Claude

`/home/li/.claude/settings.json` is a regular user-owned file, not a symlink or
Nix store path. Searches of the actual Home source, user configuration, and
managed-file declarations found no owner for this file or its `effortLevel`
key. The file is mutable Claude user state.

Flow 908786 acquired Orchestrate lock 1989 for that exact path. It replaced
the single exact top-level scalar `effortLevel: xhigh` with `medium`, then
verified:

- the resulting document is valid JSON;
- the top-level value is `medium`;
- the existing `claude-opus-5` and `claude-fable-5-1` model overrides remain
  `medium`;
- the canonical JSON with `effortLevel` removed has the same SHA-256 before
  and after; and
- the file remains owned by user 1001, group 100, with mode 0644.

Lock 1989 was released after verification. No other field was changed and no
Claude process was restarted.

## Pi and Pi testing

The live `/home/li/.pi-testing/agent/settings.json` is a regular mode-0600 file
whose `defaultThinkingLevel` remains `high` pending the Home candidate and a
future authorized activation. It was not edited directly because the actual
authoring source owns that key in `always` mode.

The exact owning source is
`/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/pi-models.nix`.
Actual GitHub main was
`528b951b7bd946532eb2246f12faac8a7850d428` when inspected. At that revision:

- `piSettingsConfig.defaultThinkingLevel` is `high`;
- `piTestingSettingsConfig` aliases `piSettingsConfig`;
- `mergePiSettings` owns `/defaultThinkingLevel` in `always` mode; and
- `mergePiTestingSettings` targets
  `$HOME/.pi-testing/agent/settings.json` and owns
  `/defaultThinkingLevel` in `always` mode.

The exact path, revision, current value, and required `medium` correction were
queued to the existing primary Home owner under message receipt
`01a0b261-e04a-7051-af4a-c1644677abeb`. Root later relayed that the Home owner
explicitly accepted the authored Codex and Pi default corrections and checks,
preserving model identifiers and overrides, in its isolated integration. This
is an acknowledged pending source candidate, not a claim that Home main or the
live managed Pi file has already changed.

## Published Home proposal and remaining activation

A later read-only audit verified the actual published proposal
`proposal/6852f4-default-effort-medium` at
`bfea9669aa4ce33c09111430d5935ea33ed6182f`. Home main still named
`528b951b7bd946532eb2246f12faac8a7850d428` at that observation.

The proposal sets medium for authored Codex root and plan reasoning effort,
the default subagent effort, and the default/explorer/worker role efforts.
It also sets the shared ordinary/testing Pi `defaultThinkingLevel` to
medium. Model identifiers are preserved.

Two checks changed with the source:

- `checks.x86_64-linux.ai-agent-launch-orchestration` asserts medium in the
  generated root configuration and role TOMLs.
- `checks.x86_64-linux.bird-home-isolation` executes both Pi settings merges
  against seeded settings, checks medium alongside the intended provider and
  model, and checks preservation of unrelated fields.

No durable execution receipt for those proposal checks was found in the
owner's worktree or lane at this observation. Final integration must supply
those receipts. The live Codex and Claude settings already conform; both
ordinary Pi and Pi-testing still select high. This proposal therefore closes
the authored-source gap but does not establish activation.

Canonical Curriculum `roles.datom` and generated role packets already use
medium. Supported-effort lists containing high or xhigh are capabilities,
not defaults. No DeepSeek/dsh configuration is installed; the observed
OpenCode configuration declares plugins without a model or effort default.
No generated agent tree was edited during this audit.

## Sources

- `/home/li/primary/flows/908786/vision/default-effort.md`
- `/home/li/.claude/settings.json`, exact-key and metadata inspection
- `/home/li/.pi-testing/agent/settings.json`, exact-key and metadata inspection
- CriomOS-home main
  `528b951b7bd946532eb2246f12faac8a7850d428`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/pi-models.nix`
- Orchestrate `Locked` and `Released` receipts for lock 1989
- Root relay of the primary Home owner acknowledgement, 2026-09-17
