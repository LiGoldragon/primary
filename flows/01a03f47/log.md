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
