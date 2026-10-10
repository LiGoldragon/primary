# Flow 01a03f47

## About

Repair and verify Claude Desktop's EGL loader linkage after the declared Nix
Desktop package was updated and patched.

Remembered: 01a03e02 — depth 1

## Settled

- CriomOS-home producer `582607e59bd6e3799f2d086faed7abce105e9d96` and
  CriomOS consumer `89b207fbdca9f19353fd7a2a1577bbe7ee7ed01b` are pushed.
- The remote `claude-desktop-egl-linkage` check was red before the RPATH
  repair and green after it. Remote launcher-linkage and declared-CLI checks
  are green. The test-package and production-package derivations are distinct;
  both carry the patch.
- Lojix deployment 77 is terminal `Completed`/`Succeeded` and current at
  producer `582607e59bd6e3799f2d086faed7abce105e9d96`. Active Home Manager
  generation 986 uses output `vb37w2…`.
- The active `libGLESv2.so` DT_RUNPATH includes
  `dwc1…-libglvnd-1.7.0/lib`; a safe `dlinfo` witness resolves the exact
  `…/libEGL.so.1`; and the active ASAR embeds the exact Nix Claude Code
  `2.1.246` fail-closed path.
- The earlier blocked state came from inspecting raw upstream `04282…`, not
  the active output. No Desktop GUI process was restarted or launched.
- The Lojix query decoder/aggregate check is unrelated to this realization.

## Open

- A normal Desktop launch with hardware GPU enabled remains the next witness;
  no claim of that interactive process proof is made yet.

# Flow 01a03f47

Investigating why Claude Desktop continues to fail when a local prompt launches its downloaded Claude Code runtime on NixOS, after remembering flow 01a03e02.

Open: remember 01a03e02 at depth 1; establish the live causal chain behind the code-127 dynamic-linker failure; identify the proving witness and any authorized fix.

Relevant: the remembered design forces Claude Desktop to use the immutable Nix Claude Code and fail closed, with the interactive signed-in local-thread smoke still open. Current state confirms the declared `claude` is Nix `2.1.246` and `claude-desktop` is the declared wrapper for Desktop `1.37937.1`; however, a stateful `~/.config/Claude/claude-code/2.1.246/claude` now exists while the old `2.1.237` path is absent, and Desktop is running. No local-thread child was observed in this light check, so the live code-127 cause remains unresolved.

## About

Diagnose why Claude Desktop still launches its mutable Claude Code runtime
after the declared Nix Desktop package was updated and patched.

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

- An authorized repair must make the launched Electron process use the
  patched copied package and retain the declared, fail-closed Claude binary
  boundary.
- A wrapper-level launched-process witness and a fresh signed-in local-thread
  smoke are still required.
- No repair, mutable-state deletion, or stateful binary patching is authorized
  by this diagnosis.
