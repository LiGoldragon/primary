# Obsidian as the medium for proposals, research of 2026-10-29

By a read-demanding subflow (Sonnet) of Psyche obsidian Primary 11b7c0. "gh" marks a version read with `gh api .../releases/latest`; desktop-only flags come from each plugin's manifest.json; everything else is cited by URL. Nothing was run on a device.

## Obsidian itself
- Version 1.15.0, desktop and mobile, 2026-10-22; installer releases show v1.14.5 (gh). https://obsidian.md/changelog/
- The app needs no account. Sync and Publish need one: the headless Sync client starts with `ob login`. https://obsidian.md/pricing · https://obsidian.md/help/sync/headless
- Free for any purpose; optional Commercial licence $50/user/year; code proprietary. https://obsidian.md/license
- Platforms: Windows, macOS, Linux, Android, iOS. Publish: $8/site/month yearly. https://obsidian.md/pricing

## Obsidian Sync
- Standard $4/user/month yearly ($5 monthly): 1 vault, 5 MB/file, 1 GB, 1 month history. Plus $8 ($10): 10 vaults, 200 MB/file, 10–100 GB, 12 months. Unlimited devices. AES-256 end-to-end. https://obsidian.md/help/sync/plans
- Official headless client: npm `obsidian-headless`, command `ob`, open beta, announced 2026-02-27, npm 0.0.14 of 2026-07-30. `ob login`, `ob sync-setup`, `ob sync --continuous`, `ob sync-config`. Runs on Linux; needs a Sync subscription; must not share a device with the desktop app's Sync; `--configs` syncs app, appearance, hotkeys, core and community plugin settings. https://obsidian.md/help/sync/headless
- No public Sync API beyond `ob`.
- Full app under Xvfb is community practice: `ppatlabs/obsidian` Docker image with Local REST API; a forum systemd write-up on Obsidian 1.12.7. A plugin listed in community-plugins.json is not guaranteed to load. https://hub.docker.com/r/ppatlabs/obsidian · https://forum.obsidian.md/t/running-obsidian-headlessly-on-ubuntu-for-ai-agent-workflows-xvfb-systemd-setup/112741
- With `ob sync --continuous` on the server, the agent writes a plain file into the vault folder and it reaches his devices.

## Self-hosted alternatives
- Self-hosted LiveSync (vrtmrz) 1.0.42, 2026-10-27 (gh); desktop and mobile; Obsidian ≥ 1.7.2. Backends CouchDB, S3/MinIO/R2, WebRTC (needs a signalling relay). Optional E2E. Must not run beside Obsidian Sync. Mobile needs HTTPS and CORS for app://obsidian.md and capacitor://localhost. Server side: LiveSync CLI, Docker `ghcr.io/vrtmrz/livesync-cli`, `daemon` mirrors a folder to CouchDB both ways; `mirror` carries no deletions; `put`, `cat`, `ls`, `rm`. https://github.com/vrtmrz/obsidian-livesync
- Syncthing: Linux native; the official Android app archived 2024-12-03, maintained forks Syncthing-Fork and BasicSync; iOS only via Möbius Sync or SyncTrain, background sync unreliable, listed unsupported by Obsidian's iOS help.
- Git vault, obsidian-git 2.42.0, 2026-10-18 (gh): desktop auto commit/pull/push, diff and history views; mobile "very unstable", isomorphic-git, no SSH, may crash on clone or pull. The agent commits and pushes; his comments come back as commits: the cleanest data path. https://github.com/Vinzent03/obsidian-git
- Remotely Save 0.5.25 of 2024-10-20, last push 2024-11-10, dormant; S3/WebDAV/Dropbox/OneDrive; source-available, merging paid; unknown whether files written straight to the backend are picked up.

## Comments inside Obsidian
- Built-in `%% %%`: hidden in Reading view, sits where typed, not anchored; mobile 1.15.0 restored the comment button on the toolbar; regex-parseable. https://obsidian.md/help/syntax · https://obsidian.md/changelog/2026-10-22-mobile-v1.15.0/
- Commentator (Fevol/obsidian-criticmarkup) 0.2.7, 2026-08-07 (gh), mobile allowed; CriticMarkup `{++ ++}` `{-- --}` `{== ==}` `{>> <<}`; README calls it beta and warns text may be removed; threads on the roadmap.
- Review Comments 2.1.1 (Shota Shirai), desktop and mobile: `{==text==}{>>id|author|date|TYPE: comment<<}`, replies as further `{>> <<}` with the same id; anchor, author and date as structured fields. Best match found for comment-on-passage from a phone with parseable output; mobile ease unverified. https://community.obsidian.md/plugins/review-comments
- Others: Review & Critic (mobile, CriticMarkup pane); Inline Review Comments (`%% %%` as cards, Obsidian ≥ 1.13.0); Margin Comments (JSON sidecars in `.margin-comments/`); Side Comments (desktop only, sidecars); Document Comments and Notion-style Comments (HTML comments in the note; the latter mobile).
- Footnotes `[^1]` and inline `^[…]`: anchored at a point, easy to parse; footnotes view since 1.9.0. Callouts `> [!info]` not anchored. Highlights with emoji colours `==🔴…==` since 1.14.0. Properties suit status fields. Bases (core since 1.9.10, kanban 1.14.0) could list proposals by properties.
- Diffing every edit works under any sync layer, since each delivers the plain file.

## Programmatic access
- Official Obsidian CLI, since 1.12.4, native binary from 1.12.7; desktop only, needs the running app; create, read, append, prepend, search, property:set, base:query, diff, history, sync:*, publish:*, eval; 1.15.0 appends under a heading. https://obsidian.md/help/cli
- URI scheme obsidian://open|new|daily|unique|search with content/append/prepend/overwrite/silent; needs the app. https://obsidian.md/help/uri
- Local REST API (coddingtonbear) 5.5.2, 2026-10-17, desktop only, Obsidian ≥ 1.13.1; HTTPS 127.0.0.1:27124; PATCH by heading, block or frontmatter key with If-Match/ETag; search, commands, event streams, built-in MCP at /mcp/. https://github.com/coddingtonbear/obsidian-local-rest-api
- mcp-obsidian 0.2.3 on PyPI, 2026-08-20, over the Local REST API.
- Every route here needs a desktop app running, on a server under Xvfb; plain files plus a sync layer need no app.

## Rendering
- Mermaid built in; since 1.15.0 drawn by Obsidian's own "Pele", Mermaid 12.1.0 syntax claimed; coverage unknown. https://obsidian.md/changelog/2026-10-22-desktop-v1.15.0/
- SVG embeds with `![[x.svg]]`. Code blocks by Prism.
- Red/green diff: none found in core; Shiki Highlighter colours +/- in ```diff; also Code Diff, Show Diff, Inplace Diff View; indented diff blocks reported to break editing view.
- Phone: Reading view hides `%%`; how a long proposal reads on a phone, wide code block scrolling, and CriticMarkup display there are untested.

## Alternatives not tied to a proprietary product
- SilverBullet 2.12.1, 2026-10-12 (gh): open-source self-hosted Markdown wiki in the browser; files on disk. https://github.com/silverbulletmd/silverbullet
- Logseq 2.0.2, 2026-10-07: DB version early beta; markdown edition in maintenance.
- Plain git with any markdown viewer; phone editing needs a git client app, not evaluated.

## Unknowns
- Whether any comment plugin is low-friction on a phone; none tested.
- Pele's Mermaid coverage.
- Whether Remotely Save picks up files written straight to its backend.
- Stability of LiveSync CLI and obsidian-headless, both recent or beta.
- How Obsidian Sync or LiveSync resolve a conflict when the agent and the phone edit the same file.
