# Audit21 item13 — held for next owner

Core disposition: HELD, separate from the declaration commit. No diagnostic installation/build or clipboard probe authorized. Resume only with a supported diagnostic and verified committed-base custody.

Scope: four ranger mappings, CriomOS-home modules/home/profiles/med/colemak.conf:116-119. Audit /home/li/primary/flows/44b9b8/audits/criomos-git-server-x11.md finds xsel reliance despite shipped wl-clipboard and vision:x11's desktop without reliance on X11. Claude desktop X gates are outside this narrow scope; installed Xwayland fallback stays.

Contract: each mapping delivers identical bytes to PRIMARY and CLIPBOARD; jo/js/jk omit newline, jr retains exact newline bytes. Either delivery failure must propagate; no pipeline masking or automatic X fallback. Exact four-mapping design and nonclipboard byte-capture tests are required before edit approval. No replacement was chosen or proposed.

Sole evidence reader was 72e1eb's /root/review_refactor, coordinated by Field core Secondary2885c5; stopped/idle. No parallel reader or writer from80c6e8.

Read-only target witness: loginctl session3 li/seat0, Wayland, active, local; leader niri, compositor PID2354 niri26.04 --session. Compositor filtered environment: XDG_SESSION_TYPE=wayland and XDG_RUNTIME_DIR=/run/user/1001; WAYLAND_DISPLAY/DISPLAY/XDG_CURRENT_DESKTOP unset. Existing sockets /run/user/1001/wayland-1 and /run/user/1001/niri.wayland-1.2354.sock. Declaration retains Xwayland-satellite and niri:GNOME. This witnesses session identity, not clipboard protocol support.

Open gates:
- Clipboard and PRIMARY protocol globals UNWITNESSED. Bounded existing inventory found no wayland-info/weston-info. Existing niri msg help offers compositor commands, not registry/global enumeration. No supported registry-only diagnostic found within authorized scope.
- Installed wl-copy/wl-paste2.3.0 help/man supports default clipboard/--primary and byte/newline retention; installed-tool support does not prove actual-session capability.
- Actual ranger execution shell and macro-source semantics remain incompletely witnessed; examples are insufficient.
- Implementation base/custody unavailable: await eventual COMMITTED Home after declaration-owner change, verify exact HEAD and explicit custody. Local-only origin/main b18ab8e3e0f26f6c1f02dcd167dc45dfc2ceea80 (tree dab80f8aa64f9935e2b7b6775d99a2a37da1d313, colemak blob379d015a9ebde94c15dba170d7ae6805d63416a8) was potentially stale planning evidence, never an approved base. No branch from staged/dirty25318. Seat adoption is not writing custody.

No clipboard contents read, clipboard writes, ownership/source/offer operations, application launches, installs, edits to Home, worktree/ref allocations, fetches, evaluations or builds were performed in this item13 lane. No broader search or workaround is inferred.
