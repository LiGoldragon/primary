---
title: 1 — Browser-use current situation
role: cloud-maintainer
variant: Handover
date: 2026-06-19
topics: [browser-use, chrome-cdp-bridge, cloud-maintenance]
description: |
  First cloud-maintainer report: registers the lane context and records the
  current browser-use / Chrome CDP bridge status, including what is verified,
  what remains human-consent-gated, and what should happen next.
---

# 1 — Browser-use current situation

## Scope

This is the first `cloud-maintainer` report. The lane is a specialized maintenance window under `system-maintainer` discipline: it handles cloud-host, provider-session, and browser-driven cloud account work without stealing the broader `cloud-operator` deploy lane or the `cloud-designer` design lane.

The immediate object is the `browser-use` path for driving the real Chrome profile through the new Chrome CDP bridge, so cloud work such as DigitalOcean account/token setup can be tested through the user's authenticated browser only after explicit per-tab consent.

## Orchestrate lane state

`cloud-maintainer` is now present in the orchestration registry and visible to the daemon-backed helper:

- `orchestrate/roles.list` contains `cloud-maintainer`.
- `tools/orchestrate claim cloud-maintainer '[self-test:cloud-maintainer-lane]' -- verify cloud-maintainer lane registration` succeeded.
- `tools/orchestrate release cloud-maintainer` succeeded.
- `tools/orchestrate status` now renders `cloud-maintainer.lock` as an idle lane.
- Reports have a dedicated lane at `reports/cloud-maintainer/`.

The registration docs now also name the lane in `AGENTS.md`, `orchestrate/AGENTS.md`, and `skills/role-lanes.md`.

## Browser-use bridge status

The deployed bridge surface is present in the active profile environment:

- `browser-use-attach` is on `PATH`.
- `chrome-cdp-bridge-relay` is on `PATH`.
- `chrome-cdp-bridge-extension-path` is on `PATH`.
- `chrome-cdp-bridge-extension-path` resolves to the Nix-built extension directory.
- That directory contains `manifest.json` and `background.js`.

The current chain described by CD remains the right mental model: a Manifest V3 Chrome extension attaches through Chrome's in-browser `chrome.debugger` API, while a local relay exposes the browser-level CDP shape expected by `browser-use` 0.13.1. That avoids the Chrome 136+ debug-port block against the real Default profile.

## Verified here

I verified the static deployment pieces only. I did not attach to the user's live browser tab, did not load or toggle the extension, and did not touch logged-in cloud-provider pages.

The safe checks show the bridge package is installed and discoverable. Attempting `--help` on `browser-use-attach` and `chrome-cdp-bridge-relay` is not a harmless introspection path in this package: both commands stayed active until the shell timeout, so future agents should treat them as operational commands rather than ordinary help surfaces.

## Consent-gated last mile

The remaining real-session test is still human-consent-gated:

1. Run `chrome-cdp-bridge-extension-path` and copy the printed extension directory.
2. Open `chrome://extensions` in the real Chrome profile.
3. Enable Developer mode.
4. Load unpacked extension from that directory.
5. Click the bridge toolbar icon on a fresh neutral tab, such as `https://example.com`.
6. Run `browser-use-attach` only against that consented tab.

A neutral smoke test should read `example.com` and report its heading. The DigitalOcean token path should wait until the browser path is proven and the user has created or approved the account/token flow.

## Risks and next actions

The main operational risk is model latency: Gemma vision calls can exceed `browser-use`'s step timeout under load. That is a serving/tuning issue, not evidence the extension bridge is wrong.

The next cloud-maintainer action is to wait for explicit consent to load and activate the extension on a real Chrome tab. After that, run the neutral `example.com` smoke test before any provider page is opened.
