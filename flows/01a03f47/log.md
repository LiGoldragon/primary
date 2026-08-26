# Flow 01a03f47

## About

Diagnose why Claude Desktop still launches its mutable Claude Code runtime
after the declared Nix Desktop package was updated and patched.

Remembered: 01a03e02 — depth 1

## Settled

- The declared `claude` is Nix Claude Code `2.1.246`; the declared Desktop
  launcher is the `1.37937.1` wrapper.
- The overlay patches a copied `app.asar`, but the generated inner
  `.claude-desktop-wrapped` launcher line 51 execs the original absolute
  upstream Desktop binary.
- Live Desktop PIDs 219365 and 219644 opened the upstream package's original
  `resources/app.asar`, not the patched copied tree.
- The existing check inspects extracted ASAR contents and manager functions
  directly. It never launches the generated wrapper or observes Electron's
  resource file, so its green result did not prove the launcher linkage.
- The live Desktop log records the mutable
  `~/.config/Claude/claude-code/2.1.246/claude`; that ELF requests
  `/lib64/ld-linux-x86-64.so.2`, reaches NixOS `stub-ld`, and exits 127. The
  declared Nix CLI exits 0.
- The immediate causal chain is therefore established: the patched ASAR is
  bypassed, Desktop uses its mutable downloaded CLI, and that generic ELF
  cannot start on this NixOS session.

## Open

- An authorized repair must make the launched Electron process use the
  patched copied package and retain the declared, fail-closed Claude binary
  boundary.
- A wrapper-level launched-process witness and a fresh signed-in local-thread
  smoke are still required.
- No repair, mutable-state deletion, or stateful binary patching is authorized
  by this diagnosis.
