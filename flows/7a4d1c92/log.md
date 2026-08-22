# Read-only CriomOS-home Chroma–Emacs audit — 7a4d1c92

Audit of CriomOS-home revision `002e521a625cd8a8fa3c4fd7de2a533084e48634` against the accepted Chroma–Emacs slices and exact upstream revisions. Product repositories, deployment, and runtime state were not changed by this flow.

2026-08-23 — Read `NON_MANAGEMENT_AGENTS.md`, the governing spirit, flows, psyche, behavior, vocabulary, testing, nix-workflow, and repository-lifecycle skills, plus Home, CriomOS, Chroma, and chroma-emacs repository instructions. Reacquired the accepted Chroma–Emacs contract and prior Home reconnaissance.

2026-08-23 — Read the Home parent revision and exact Chroma/chroma-emacs revisions. Confirmed lock pins, same-Emacs-package-set construction, Home-owned Ignis symbols/path, mode enablement, Chroma concern removal, and the remaining generic Emacsclient surface.

2026-08-23 — Inspected the exact resident check. Its derivation evaluates independently and wires the built PGTK Emacs, chroma-emacs package, built Chroma daemon, fake Gamma peer, and private session bus. The script uses event barriers and runtime D-Bus/Emacs queries, but manually creates theme fixtures and does not itself cover all protocol statuses or Home's compiled/native-init artifact.

2026-08-23 — Reproduced the canonical flake blocker against the exact commit using a `git+file` revision: `checks/yt-dlp/default.nix:62` accesses `.home` after importing the min profile, whose direct shape is `{ config = mkIf ...; imports = ...; }`. The defect predates `002e…` and is absent from its diff. A separate evaluation against the concurrently modified working copy succeeded; that result is not evidence for the audited revision.

2026-08-23 — Wrote the sourced audit report and three witnesses. The working copy of CriomOS-home became dirty through an outside implementation flow; all exact-revision conclusions use `jj file show` or `git+file?...rev=002e…`, and no product files were edited here.

2026-08-23 — Correction audit of Home `a61b02d0cf69de757bdf8b5fa0f336f78f5054ee`: exact pins now use Chroma `6a8e4c6a…` and chroma-emacs `119a2313…`; the yt-dlp shape helper passes canonical evaluation; the resident witness consumes Home's shared Ignis generator, proves `.elc`/`.eln` and package closure identity, and explicitly checks target/opposite/overlay/rendered faces and both daemon restart paths. Canonical no-build checks and forced remote rebuilds pass. A direct host invocation exposed only a duplicate-GUID `/etc/dbus` caveat; the canonical remote sandbox passed. Home is safe to pin under the stated gates.
2026-08-23 — Qualification: `.elc`/`.eln` proof is artifact-level and closure-matched; the daemon uses `--quick --load test-init.el`, so normal activation-path loading of Home early-init is not claimed. This bounded distinction does not block pinning under the stated gates.
