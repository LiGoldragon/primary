---
title: 2 — Browser agent secret capture
role: cloud-maintainer
variant: Research
date: 2026-06-19
topics: [browser-use, secrets, digitalocean]
description: |
  Research on how an agent can complete a browser-only token creation flow
  without any human or LLM seeing the secret, focused on DigitalOcean PATs,
  Chrome native messaging, and gopass storage.
---

# 2 — Browser agent secret capture

## Finding

A fully agent-driven DigitalOcean PAT flow is possible only if the LLM is removed from the secret path. DigitalOcean's official path is browser-only: log in to the Control Panel, open Account → API, click Generate New Token, then save the displayed token; the page says the secret is shown once. The docs also explicitly say tokens function like passwords and should be kept secret.

That means the safe implementation is not “let browser-use see the page and promise not to log it.” The safe implementation is a local, trusted capture component that can read the once-shown token in the browser process and pipe it directly to `gopass`, while browser-use/LLM receives only non-secret status events such as `stored digitalocean/api-token length 71`.

## Shape that works

Use a dedicated Chrome extension plus native messaging host:

1. The LLM/browser agent drives non-secret UI only: open DigitalOcean, select Google sign-in, navigate to token creation, choose name/expiry/scopes.
2. When the token is generated, the content script detects the DigitalOcean token element, but does not send it to browser-use, console logs, screenshots, or the page clipboard.
3. The extension service worker sends the token through `chrome.runtime.sendNativeMessage()` to a registered native host.
4. The native host writes the token to `gopass insert -f digitalocean/api-token` over stdin.
5. The native host returns only a receipt: path, byte length, timestamp, and exit status.
6. The extension redacts or hides the token element immediately after capture.
7. Browser-use continues from the receipt and navigates to billing/credit.

Chrome supports this boundary directly: native messaging lets an extension talk to a local process over stdin/stdout, and the native host manifest whitelists the extension origin. Browserpass is the closest proof-of-pattern: a browser extension plus native messaging host talks to a local password store, performs origin-aware matching, and keeps secret handling in the native/password-store boundary rather than in the page automation layer.

## Why API-only is not the answer

DigitalOcean has API/CLI/SDK surfaces for using a token, but the official token-creation documentation routes creation through the Control Panel. The docs describe the UI flow and say the generated secret is displayed once. Public API references point users back to “Create an Access Token” before using `doctl`, PyDo, curl, billing APIs, droplets, databases, and other endpoints.

So the durable answer is not “find the token creation endpoint and call it.” If an undocumented control-panel endpoint exists, using it would still require an authenticated browser session cookie and CSRF state; that would just move the secret boundary from visible page text to private web-app internals. It would also be brittle and provider-hostile.

## Security requirements for the implementation

The extension/host must be stricter than a general browser automation bridge:

- Whitelist exact origins: `https://cloud.digitalocean.com/*` only for capture.
- Whitelist exact destination path: `digitalocean/api-token` by default.
- Never expose token bytes in messages visible to the LLM, stdout, stderr, logs, traces, exception text, screenshots, or browser-use observations.
- The native host writes secret bytes only to `gopass insert` stdin.
- Receipt validation is blind: byte length, prefix/class if checked locally, `gopass` exit code, and entry-name listing only.
- The extension requires explicit human per-run consent before capture, similar to the existing CDP bridge tab consent.
- The browser-use prompt never asks the model to read, summarize, copy, or verify the token.

## Near-term workaround

Until that component exists, the safe path remains human clipboard handoff:

```sh
wl-paste --no-newline | gopass insert -f digitalocean/api-token >/dev/null
```

The human copies the token because the token is already on their trusted display. The agent only runs the blind pipe and verifies the gopass entry by name/exit code.

## Recommendation

Build a tiny `secret-capture-bridge` rather than weakening the agent secret rule. It should be a separate extension/native-host pair from the CDP bridge because it has a different authority: CDP is page-control consent; secret-capture is one-shot secret exfiltration into the local encrypted store. Mixing them would make the high-risk path too easy to invoke accidentally.

Sources: DigitalOcean “How to Create a Personal Access Token” documents UI-only creation, one-time display, and password-like handling; Chrome Extensions “Native messaging” documents extension-to-native-host stdin/stdout messaging and extension-origin allowlists; Browserpass demonstrates a browser extension plus native messaging host integrating with a local password store.
