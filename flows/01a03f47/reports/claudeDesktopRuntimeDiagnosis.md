# Claude Desktop runtime-linkage diagnosis

## Conclusion

The code-127 failure is still caused by Desktop invoking its mutable
stateful Claude Code executable, but the reason the intended override did not
take effect is now established: the patched ASAR is never used by the
launched Electron process.

The overlay copies the upstream Desktop tree and patches the copied
`app.asar`. Its generated outer launcher correctly exports the declared Nix
Claude `2.1.246` path. However, the nested `.claude-desktop-wrapped` launcher
execs the original absolute `claude-desktop` binary from the upstream package.
That binary's resource root contains the original `app.asar`. The running
Desktop process opened that original resource, so its manager never received
the patched local-binary initialization.

Desktop consequently selected
`/home/li/.config/Claude/claude-code/2.1.246/claude`, exactly as recorded in
`main.log`, and the generic Linux ELF exited 127 at NixOS's stub loader before
Claude Code initialized. The declared Nix `claude` command itself reports
`2.1.246` successfully.

## Proof boundary

The existing graphical check is insufficient for this failure. It extracts
the package ASAR directly, validates the patch markers, and executes the
manager functions from those extracted files. It does not launch the final
wrapper or inspect the Electron process's opened resource. Its success proves
the patch content and manager behavior in isolation; it does not prove that
the deployed launcher reaches that patched resource tree.

The direct code and process evidence closes that gap in the other direction:
the inner launcher has an absolute upstream exec target, and PIDs 219365 and
219644 held the upstream `resources/app.asar` open. The current mutable CLI
path and loader failure are therefore consistent with the launched process's
actual resource selection.

## Open boundary

The repair must make the launched Electron binary and its resource tree
resolve to the patched copied package while retaining the declared Claude
override and fail-closed behavior. No repair is authorized by this diagnosis.
A future repair needs a wrapper-level or equivalent launched-process witness,
then a fresh signed-in local-thread smoke; deleting or patching mutable user
state is not authorized.

## Sources

- `witnesses/claudeDesktopRuntimeLinkage.md`
- `/git/github.com/LiGoldragon/CriomOS-home/overlays/claude-desktop.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/overlays/patch-claude-desktop-runtime.mjs`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/agent-intercom-graphical-tui/default.nix`
- `/home/li/.config/Claude/logs/main.log`, lines 13563-13570
- Flow `01a03e02`, especially `log.md` and `reports/claudeDesktopDeclaredCliRealization.md`
