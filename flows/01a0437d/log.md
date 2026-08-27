# Flow 01a0437d

Investigate how updating the packaged Codex and Claude TUIs affects their desktop applications: whether desktop derivations rebuild automatically against the updated TUIs, how to make them do so if not, and what terminal end-shape prevents two independently versioned stacks.

Realize and deploy the approved narrow CriomOS-owned Codex/Claude package collection in CriomOS-home, including the derived ChatGPT and Claude Desktop packages and their single-stack contracts. Before choosing an implementation checkout, find and integrate any relevant recent unmerged worktree so no work is abandoned.

Remembered: 01a038be — depth 1 — the official ChatGPT package retained one declared Codex derivation for terminal and wrapper consumers; Desktop and CLI have separate product versions.
Remembered: 01a03e02 — depth 1 — Claude Desktop was patched fail-closed to consume the exact declared Nix Claude Code package instead of downloading or copying a second runtime.
Remembered: 01a03f47 — depth 1 — the declared Claude Code path remained embedded through the later EGL repair and deployment.

## Settled

- Updating the shared Codex CLI derivation changes the terminal wrapper and the ChatGPT wrapper because both depend on `codexCliPackage`; a TUI-wrapper-only edit does not change Desktop because Desktop consumes the CLI package, not the terminal UI wrapper.
- Updating the Claude Code derivation changes the locally patched Claude Desktop derivation because the exact CLI store path is embedded in its ASAR; a substitute-package evaluation changed the Desktop derivation with no Desktop-version change.
- Nix invalidation is automatic only once the changed Home graph is evaluated/built. Propagation into CriomOS additionally requires publishing Home, advancing the locked `criomos-home` input, building the host toplevel, deploying, and restarting existing GUI processes.
- Claude's selected local runtime is fail-closed. ChatGPT normally uses the shared CLI through `CODEX_CLI_PATH`, but its vendor payload still contains a bundled Codex fallback reachable when the wrapper is bypassed.
- Desktop product release numbers are independent of CLI release numbers; the alignment contract is executable-derivation identity, not numeric equality.
- The living approved CriomOS-home owning the canonical Codex and Claude packages plus the derived ChatGPT and Claude Desktop package expressions, with direct consumer exposure to `llm-agents` removed.

## Open

- Audit recent worktrees and integrate any relevant unmerged work before implementation.
- Implement the owned package collection, update every consumer, strengthen the ChatGPT fallback to the canonical Codex derivation, and retain Claude's fail-closed canonical runtime.
- Prove producer packages/checks and the layered complete-host consumer, publish both revisions, deploy, and witness the realized runtime paths.
