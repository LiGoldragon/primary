---
title: 3 — Dedicated Chrome automation profile
role: cloud-maintainer
variant: Handover
date: 2026-06-19
topics: [browser-use, chrome, digitalocean]
description: |
  Establishes the durable cloud-maintainer Chrome profile for browser automation,
  replacing the experimental real-profile CDP bridge as the default path for
  DigitalOcean and cloud-provider work.
---

# 3 — Dedicated Chrome automation profile

## Current state

The durable cloud-maintainer browser profile is running and exposing native Chrome DevTools Protocol.

- Profile: `/home/li/.local/state/cloud-maintainer/chrome-profile`
- Launcher: `/home/li/.local/bin/cloud-maintainer-chrome`
- CDP endpoint: `http://127.0.0.1:9223`
- Log: `/home/li/.local/state/cloud-maintainer/cloud-maintainer-chrome.log`
- Documentation: `protocols/cloud-maintainer-browser-profile.md`

The first attempted default port, `9222`, collided with an existing Chrome listener. The durable launcher therefore defaults to `9223`.

## Verification

`curl -fsS http://127.0.0.1:9223/json/version` returns Chrome version JSON with a browser-level `webSocketDebuggerUrl` on `127.0.0.1:9223`. That is the CDP shape browser automation tools expect natively.

## Operational decision

This profile is now the default browser automation path for cloud-maintainer work. The earlier real-profile CDP bridge is experimental and should not be used for account setup, billing, or provider token work until it is separately audited and fixed.

The dedicated profile keeps provider sessions isolated from the daily browser profile while avoiding the extension relay's token, attach, and browser-level-CDP emulation failures.

## Next step

Sign into Google/DigitalOcean in the dedicated Chrome window. After that, agent automation can attach to `http://127.0.0.1:9223`, create the DigitalOcean token, store it at `digitalocean/api-token`, and navigate to the billing/credit screen.
