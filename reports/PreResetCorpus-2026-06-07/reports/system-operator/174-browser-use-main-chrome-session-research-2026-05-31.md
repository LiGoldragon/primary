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

## Browser-use versus Playwright extension mode

Browser-use is an agent framework. The caller gives it a task plus an LLM, and browser-use runs its own internal perceive/decide/act loop. It then drives the browser through Playwright/CDP-like browser control. In this workspace that was attractive because Gemma 4 could be the inner browser agent model through the Prometheus OpenAI-compatible endpoint, and browser-use had a ready-made browser agent loop including screenshots/vision.

Playwright MCP/CLI is a browser tool substrate. MCP/CLI itself does not contain the planning model. The outer harness agent sees snapshots, chooses `browser_click`/`browser_type`/CLI commands, and remains the only reasoning loop unless another wrapper adds one. That makes Playwright extension mode more direct and auditable for supervised account scouting.

CDP is not one thing operationally. External CDP means Chrome exposes a remote debugging endpoint such as `http://localhost:9222`; Chrome 136+ blocks that for the default data directory. Extension CDP means an installed extension with the `debugger` permission attaches to a selected tab from inside the real profile and relays DevTools-style commands to a local server. The Playwright extension uses the latter route, so it avoids the default-profile remote-debugging block while still speaking DevTools-like browser commands.

The practical distinction for the Digi/login use case:

- browser-use is best when the desired unit is "give this browser agent a task and let it solve it" using Gemma as the internal model;
- Playwright extension mode is best when the desired unit is "let the harness agent inspect and act in my real Chrome tab under supervision";
- browser-use can still be useful on a persistent automation profile or CDP endpoint, but it does not natively become the already-installed Playwright Extension unless we write an adapter.

## Live browser-use main-profile-copy test

After the user closed Chrome, browser-use was tested with `user_data_dir=/home/li/.config/google-chrome` and `profile_directory=Default`, headed mode, local Gemma Q4, and a harmless `https://example.com/` task. The agent returned success in two steps and reported the Example Domain heading, but the visible focused tab initially remained `about:blank`; CDP target inspection showed one `about:blank` target and one `https://example.com` target, and the example target had to be activated manually afterward. The smoke test therefore proves profile-copy launch and target creation, not a polished visible-session flow.

The important implementation detail: browser-use did **not** run Chrome directly against `/home/li/.config/google-chrome`. Process inspection showed Chrome launched with `--user-data-dir=/tmp/browser-use-user-data-dir-...`. The installed browser-use source explains why: `BrowserProfile._copy_profile()` copies the requested Chrome profile directory plus `Local State` into a temporary `browser-use-user-data-dir-*` directory before launch. That avoids both Chrome's profile lock and Chrome's default-data-dir remote-debugging block.

So browser-use's real-profile mode is better described as **main profile copy mode**: it can reuse profile data from the real profile after Chrome is closed, but it controls a temporary copied profile, not the live main browser session.

Observed caveats from the smoke test:

- Browser-use emitted a disallowed internal Chrome URL warning for `chrome://omnibox-popup.top-chrome/`; harmless for the test.
- The visible focused tab was `about:blank` even though an `https://example.com` target existed; the example target had to be activated manually via the browser's CDP endpoint.
- Screenshot capture timed out once and triggered CDP reconnect noise, while the task still returned successful.
- Since the profile is copied, account state may work if cookies/local storage decrypt under the same user, but live tabs/in-memory state are not the same as the killed Chrome session.

## Recommendation

Use two distinct modes deliberately:

- **browser-use main-profile-copy mode** for autonomous nested-agent work that can tolerate closing Chrome first and working from a copied profile snapshot;
- **Playwright Extension mode** for exact already-open main Chrome tab/session control via `npx @playwright/mcp@latest --extension` or `playwright-cli attach --extension`.

Security posture should stay supervised: user approves extension attachment or profile-copy use, login/2FA stays manual, the agent reports page state and proposed next actions, and consequential submissions require explicit approval.

## Sources

- Chrome Developers blog, March 2025: remote debugging switches no longer work against the default Chrome data directory from Chrome 136; use non-standard `--user-data-dir`; Chrome for Testing keeps the old automation behavior.
- browser-use documentation/code: `BrowserSession` / `Browser` supports `cdp_url` for existing browser instances.
- Chrome DevTools MCP documentation: supports `--autoConnect` for running Chrome with remote debugging enabled at `chrome://inspect/#remote-debugging`, and supports `--browserUrl`/`--wsEndpoint` for explicit CDP endpoints.
