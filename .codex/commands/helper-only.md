# Helper-Only

Compatibility shim for Codex surfaces that look for project commands under
`.codex/commands/`. The canonical repo-local Codex prompt lives at
`.codex/prompts/helper-only.md`.

Run:

```sh
tools/helper-only-brief --harness codex --task "$ARGUMENTS"
```

Use the generated packet unchanged as the helper instruction.
