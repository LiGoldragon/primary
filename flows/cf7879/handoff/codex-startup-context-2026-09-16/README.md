# Startup-context sandbox proposal

This is a reviewable proposal for a Codex startup packet. It does not change
Codex defaults, install a skill, launch a refreshed primary, or publish any
private source material.

## Supported surfaces

The installed `codex-cli 0.153.4` generated app-server schema exposed:

* `thread/start.baseInstructions` and `thread/start.developerInstructions`.
* `thread/name/set` with `{ threadId, name }`.

`baseInstructions` replaces the model's normal base instructions. The proposal
therefore uses only `developerInstructions`; it is explicitly a developer-role
stand-in and must never be described as a system prompt or as a native skill
load. `additionalInstructions` was not present in the generated schema.

## Source packet

`manifest.json` pins the intended private source inputs by logical path, byte
count, and SHA-256. `assemble_startup_developer_prompt.py` checks every digest
before producing the full developer packet. It needs two source roots:

```text
python3 docs/startup-context-sandbox/assemble_startup_developer_prompt.py \
  --workspace-root /path/to/private-primary \
  --curriculum-root /path/to/Curriculum \
  --output /tmp/startup-developer-prompt.md
```

The generated file intentionally contains complete `<skill ...>...</skill>`
body copies for the selected authored skills. Each wrapper says that the body
was copied into developer-role text. A path or a `<skill>` wrapper is not proof
of a harness-native skill load.

The selected sources are: the four core skill bodies, correction, vocabulary,
testing, psyche-interraction, subflow, edit-coordination, codex-harness,
prompt-crafting, the top-level Vision corpus, all current Intent files, and
one design-Spirit reference. The design reference is labeled unadopted and is
not converted into an instruction or a native law.

## De-duplication rule

Omit a body only after the startup receiver has a receipt that the exact
SHA-256 body is already present in its context. The known pasted-skill rule is
valid for a structurally complete pasted block; this proposal has no evidence
that a path alone or a same-named native skill is already loaded.

## Bounded receipt probe

`sandbox-receipt.json` records two harmless, read-only Luna runs. The
persistent parent received the exact sentinels in a developer-role message.
Both child-spawn attempts were rejected with `agent type is currently not
available`; no child thread, model, or inherited-body receipt exists. Do not
use this evidence to claim subagent inheritance.

`run_probe.sh` is intentionally opt-in: it prints the command unless called
with `--execute`. It creates a named sandbox thread and asks for one child. It
does not rename a primary thread or change model configuration.

## Title receipt

The named primary thread was read, renamed through `thread/name/set`, and read
back as `Primary Codex cf7879 · paired Claude efa157`. That is an app-server
receipt only; no independent remote-client reflection was observed.

## Root review note

The retained persistent test thread was named separately through the supported API. `run_probe.sh` itself does not issue a naming call. Its synthetic skill marker lacks a location; it tests developer-body presence, not the complete-pasted-skill loader rule. The assembled startup packet does contain complete named/location skill blocks. Root verified all12 embedded skill hashes in root-verification.json. No new model run or root refresh is included in this artifact copy.
