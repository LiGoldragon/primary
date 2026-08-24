# Zeus Bird Codex launcher

Method: probe `ssh root@192.168.18.95 "sed -n '1,40p' /home/bird/.local/share/applications/chrome-ilpaeoofknldkmceepkoccjdocgbmbkj-Default.desktop; readlink -e /home/bird/.nix-profile/bin/{google-chrome-stable,codex}; ps -u bird -ww -o pid,comm,args"`

The probes were carried out through the `zeus_codex` subflow against `bird@zeus`.

Bird's `Codex` launcher is Chrome-created per-user PWA state:

```ini
Name=Codex
Exec=google-chrome-stable --profile-directory=Default --app-id=ilpaeoofknldkmceepkoccjdocgbmbkj
```

The launcher is `/home/bird/.local/share/applications/chrome-ilpaeoofknldkmceepkoccjdocgbmbkj-Default.desktop`. It was created or updated at 2026-08-24 13:29:44 CEST.

`google-chrome-stable` resolves to Nix package `google-chrome-151.0.7922.137`. Its wrapper adds no `--no-sandbox`; no native Codex/Electron process remained after the PWA window exited.

A read-only in-memory query of Bird's Chrome History found the launch-time URL `https://chatgpt.com/codex?add_source=github_connector&github_onboarding=configure-repos` and its slash-normalized form. No separate download URL was recorded. Whether that page rendered or redirected to other content is unknown.

Bird's separate CLI resolves to `/nix/store/a2hlxqhdyc642f8m6zhgkl5l2cbh2bks-codex-0.149.1/bin/codex`, with derivation `/nix/store/0ah93h653a74k1aghs99104gl61b0qb1-codex-0.149.1.drv`. The active embedded Home contains no native Codex Desktop package.

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix` and `/git/github.com/LiGoldragon/goldragon/datom.dotos`

`agent-intercom.nix` derives its graphical enablement from the `AgentIntercomGraphical` capability and only enables `programs.codexDesktopLinux` when that capability is present. The Ouranos node declares `AgentIntercomGraphical`; Zeus's services vector is empty. Thus the authored projection deliberately installs the native Codex Desktop package on Ouranos and omits it on Zeus. Bird's Chrome PWA is browser/user state outside that package projection.

Method: probe `ssh root@192.168.18.95 "find /home/bird/.local/share/applications -iname '*claude*' -type f; readlink -e /home/bird/.nix-profile/bin/claude"`

No active Claude Desktop package, launcher, or process was found. The active embedded Home resolves Claude Code 2.1.241. Bird's only Claude desktop entry is a non-display URL handler still pointing at Claude Code 2.1.226. Store paths named `claude-desktop-1.1.7714` exist but were not referenced by the active profile; store presence is not an installed application.

One purported version probe accidentally invoked `/home/bird/.nix-profile/bin/google-chrome`, the Hexis wrapper, rather than `google-chrome-stable`. Because Chrome was not running, its preflight may have reconciled `/home/bird/.config/google-chrome/Local State`; whether its contents or mtime changed is unknown. All other probes were read-only.
