# Browser-use and the main Chrome session

## Frame

The user wants browser-use/Gemma to control the already-open main Chrome session, not a temporary guest profile, for supervised account-page scouting such as Mi DIGI.

## Findings

Chrome itself blocks the old direct approach. Starting with Chrome 136, `--remote-debugging-port` and `--remote-debugging-pipe` are ignored for the default Chrome data directory. Chrome requires `--user-data-dir` pointing to a non-standard directory. The local reproduction matched the policy: launching main Chrome with `--remote-debugging-port=9222 --profile-directory=Default` opened Chrome, but no DevTools endpoint appeared and Chrome logged that DevTools remote debugging requires a non-default data directory.

Browser-use can attach to any existing browser that exposes a CDP URL, using `BrowserSession(cdp_url="http://localhost:9222")` or the newer CLI `--cdp-url` support. That does not bypass Chrome. It only works if Chrome exposes CDP.

User correction after the initial report: the psyche has previously controlled their main browser session through a browser extension. Extension-mediated control is therefore a known viable precedent for this workspace, not merely a hypothetical route.

Follow-up inspection found the likely extension already installed in the main Chrome profile: **Playwright Extension** (`mmlmfjhmonkocbjadbfplnigmagldckm`), version `0.2.1`. Its manifest says: "Connect your browser to AI agents through Playwright MCP server and CLI. Enables AI-driven web testing, debugging, and automation." It has `debugger`, `activeTab`, `tabs`, and `tabGroups` permissions, plus `<all_urls>` host permissions. Its service worker opens a WebSocket relay connection and uses `chrome.debugger.attach` / `chrome.debugger.sendCommand` to forward CDP-style commands for selected tabs. This matches the user's memory: control comes from an extension inside the real profile, not from external CDP against the profile directory.

Microsoft Playwright documents this path directly: install the Playwright Extension and configure Playwright MCP with `npx @playwright/mcp@latest --extension`. The CLI path is `playwright-cli attach --extension`. The documented use cases are SSO/2FA, browser extensions, and already-open tabs — exactly the main-session problem here.

## Viable paths

### Path A — persistent automation profile

This is the currently robust path. Launch Chrome with a dedicated non-default `--user-data-dir`, log into Digi once there, and attach browser-use via CDP. It is visible, persistent, and supported by Chrome 136+.

Trade-off: it is not the same main Chrome profile. It is a separate supervised automation profile.

### Path B — Chrome DevTools MCP autoConnect

Chrome DevTools MCP documents an `--autoConnect` mode for Chrome 144+ that connects to a running browser after remote debugging is enabled at `chrome://inspect/#remote-debugging` and the user approves the connection. This is the only current-looking path that claims access to the actual running Chrome session with existing login state.

Trade-off: this is Chrome DevTools MCP, not browser-use directly. To use it with Gemma/browser-use we would need either:

- a bridge from browser-use to an existing autoConnect CDP endpoint if one is discoverable; or
- use Chrome DevTools MCP as the browser tool substrate instead of browser-use for main-session work.

It also carries the highest security risk because the agent can observe/control the real browser session after approval.

### Path C — extension or relay model

A browser extension installed in the main Chrome profile can mediate control over a selected tab. This avoids CDP against the default profile and can scope access to a chosen tab.

Trade-off: browser-use does not natively use this path. It would mean packaging or writing a relay extension plus a small local server/tool adapter.

### Path D — profile copy

Browser-use can copy the main profile into a temporary Chrome profile and control that copy. It may carry some cookies/state, depending on Chrome encryption and live profile locks.

Trade-off: it is not the real main session, it is fragile while Chrome is running, and it creates sensitive duplicated browser state. Not recommended for account work.

## Recommendation

Do not fight Chrome's default-profile CDP block. For immediate use, create a persistent Digi automation profile and log into it once. For the user's desired exact main-session control, research/implement a Chrome DevTools MCP `--autoConnect` path and decide whether to bridge it into browser-use or treat Chrome DevTools MCP as a separate main-session scout tool.

Security posture should stay supervised: user approves connection, login/2FA stays manual, the agent reports page state and proposed next actions, and consequential submissions require explicit approval.

## Sources

- Chrome Developers blog, March 2025: remote debugging switches no longer work against the default Chrome data directory from Chrome 136; use non-standard `--user-data-dir`; Chrome for Testing keeps the old automation behavior.
- browser-use documentation/code: `BrowserSession` / `Browser` supports `cdp_url` for existing browser instances.
- Chrome DevTools MCP documentation: supports `--autoConnect` for running Chrome with remote debugging enabled at `chrome://inspect/#remote-debugging`, and supports `--browserUrl`/`--wsEndpoint` for explicit CDP endpoints.
