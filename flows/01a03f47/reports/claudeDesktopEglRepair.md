# Claude Desktop EGL loader repair

## Conclusion

The Claude Desktop EGL linkage repair is landed and deployed. CriomOS-home
producer `582607e59bd6e3799f2d086faed7abce105e9d96` and CriomOS consumer
`89b207fbdca9f19353fd7a2a1577bbe7ee7ed01b` are pushed. The remote
`claude-desktop-egl-linkage` check was intentionally red before the RPATH
repair and green afterward; the remote launcher-linkage and declared-CLI
checks are green as well. The test-package and production-package derivations
are different outputs, and both received the overlay patch.

## Deployment and live proof

Lojix deployment 77 is terminal `Completed`/`Succeeded` and current at
producer `582607e59bd6e3799f2d086faed7abce105e9d96`. Active Home Manager
generation 986 uses output `vb37w2…`. In that active output, `libGLESv2.so`
has a DT_RUNPATH containing `dwc1…-libglvnd-1.7.0/lib`; a safe `dlinfo`
probe resolves the exact `…/libEGL.so.1`; and the ASAR contains the exact Nix
Claude Code `2.1.246` fail-closed path.

The earlier blocked status was based on raw upstream `04282…`, not the active
deployed output. No Desktop GUI process was restarted or launched during this
realization. A normal launch with hardware GPU enabled is the remaining
witness. The Lojix query decoder/aggregate check is unrelated and is not part
of this acceptance.

## Sources

- CriomOS-home commit `582607e59bd6e3799f2d086faed7abce105e9d96`, including `checks/claude-desktop-egl-linkage/default.nix` and `overlays/claude-desktop.nix`.
- CriomOS commit `89b207fbdca9f19353fd7a2a1577bbe7ee7ed01b`, including the Home pin and ownership expectation.
- `flows/01a03f47/witnesses/claudeDesktopRuntimeLinkage.md` and `flows/01a03f47/reports/claudeDesktopRuntimeDiagnosis.md` for the superseded raw-upstream diagnosis.
