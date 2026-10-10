# Claude Desktop runtime linkage

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/overlays/claude-desktop.nix` lines 18-29 and the generated wrapper at `/nix/store/hk040dz0xc9kj17slrbzmrbr414gqvgf-claude-desktop-with-declared-claude-code-1.37937.1/bin`.

Observed:

- The overlay copies the upstream Desktop tree, extracts and patches the copied `app.asar`, repacks it, and then applies `wrapProgram` to the copied launcher.
- The outer wrapper exports `CLAUDE_CODE_LOCAL_BINARY=/nix/store/wv6jxc43nkr2c9zv4y6hjr6m8isdqmdh-claude-code-2.1.246/bin/claude` and execs `.claude-desktop-wrapped`.
- `.claude-desktop-wrapped` line 51 execs the original absolute package binary `/nix/store/04282s5hsdnj1080vm77k9k7vnv57m80-claude-desktop-1.37937.1/lib/claude-desktop/claude-desktop`.

Method: probe `readlink -f`, `/proc/219365/{exe,fd}`, and `/proc/219644/{exe,fd}` while the deployed Desktop was running.

Observed:

- Both PIDs executed the original package binary and held the original package `resources/app.asar` open, not the copied patched output tree.

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/checks/agent-intercom-graphical-tui/default.nix` lines 113-200.

Observed:

- The check extracts `${claudeDesktopPackage}/lib/claude-desktop/resources/app.asar` directly, checks wrapper text for `CLAUDE_CODE_LOCAL_BINARY`, and runs JavaScript against the extracted files.
- It does not launch the generated wrapper or observe which `app.asar` Electron opens. Its green result therefore proves patch content and manager behavior in isolation, not launched-resource linkage.

Method: probe `nl -ba /home/li/.config/Claude/logs/main.log | sed -n '13563,13570p'`, `readelf -l`, direct execution, and `claude --version`.

Observed:

- Desktop logged `Using Claude Code binary at: /home/li/.config/Claude/claude-code/2.1.246/claude` and then exited 127.
- The mutable ELF requests `/lib64/ld-linux-x86-64.so.2`; that path resolves to NixOS `stub-ld`, `NIX_LD` is unset, and direct execution exits 127.
- The declared Nix CLI exits successfully and reports `2.1.246 (Claude Code)`.

Inference: the patched ASAR is not the resource tree used by the launched Electron process. The nested wrapper's absolute exec target bypasses the copied package tree, so the runtime patch cannot govern the live Desktop process. The exact repair remains open and unauthorized.
