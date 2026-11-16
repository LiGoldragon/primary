# Browser bridge inventory

Date: 2026-11-15. Scope: read-only process, extension, and installed CLI inspection. No gopass read, attach invocation, page read, login action, screenshot, site mutation, cookie read, profile database read, or MCP server installation was performed.

## Tested

* Google Chrome `157.0.8103.78` is running from the Nix store. The top-level Chrome process has no alternate `--user-data-dir`, so this is the default Chrome data directory path. Chrome has an extension-process. This establishes a running Chrome and an installed extension process, not a selected-tab attachment.
* Playwright Extension ID `mmlmfjhmonkocbjadbfplnigmagldckm` is installed in `~/.config/google-chrome/Default` at version `0.5.0` and in `~/.config/google-chrome/Profile 1` at version `0.2.1`. Both manifests say `Playwright Extension`, Manifest V3, permissions `debugger`, `activeTab`, `tabs`, `tabGroups`, host permission `<all_urls>`, and background service worker `lib/background.mjs`. Preferences contain settings for the ID in both profiles.
* Installed CLI: `/home/li/.nix-profile/bin/playwright-cli`, Nix package `playwright-cli-0.1.13`. `playwright-cli attach --help` exposes `--extension` (optionally `--extension=chrome`), `--cdp`, `--endpoint`, `--config`, and `--session`. Official interface: [`playwright-cli attach`](https://playwright.dev/agent-cli/commands/attach).
* A local debug-port listener was seen during process inventory, but requests to its local HTTP metadata endpoint returned unavailable. No CDP attachment is claimed.

## Secret-safety finding

The existing `playwright-chrome` wrapper obtains `PLAYWRIGHT_MCP_EXTENSION_TOKEN` from gopass only when the environment variable is absent, then `exec`s `playwright-cli`; it does not print the value. The installed Playwright core's extension attach implementation then constructs `chrome-extension://.../connect.html` with the token as a `token` query parameter and spawns Chrome with that URL as an argument. Thus `PLAYWRIGHT_MCP_EXTENSION_TOKEN` is absent from the initial wrapper command line and ordinary CLI output, but the token is placed in the spawned Chrome argv and the connect URL. A same-user process observer could read it through process metadata while the connect page is being opened. No invocation was made because this violates the supplied secrets rule that a secret must not be placed in argv.

The exact nominal command is `playwright-cli attach --extension=chrome` (or the wrapper's equivalent), and the CLI's supported input is the environment variable named above. The current installed implementation has no inspected stdin or file-descriptor token input. Token auto-approval would need an implementation that keeps the token out of URL/argv. The token-free manual-consent path below is separate and remains available, subject to the living's prior approval.

## Unknown

Extension files and an extension process prove installation/loading, not that the extension is enabled for the profile currently holding the user's desired tab, nor that the bridge relay is connected. No account page was opened and no Anthropic Billing credit rows were read. No token was handled. No Claude or Codex MCP trial was run.

## Official references

* Playwright CLI attach: https://playwright.dev/agent-cli/commands/attach
* Playwright MCP browser extension configuration: https://playwright.dev/mcp/configuration/browser-extension

## Follow-up: token-free interactive approval path

The installed extension's no-token branch is explicit and bounded. With no `token` query parameter, `connect.html` validates that the relay URL is loopback, shows a warning and the current tab list, and renders `Allow & select` controls. The living can choose the intended tab in Chrome; the extension then sends `connectToTab` for only that selected tab. This is a supported manual-consent path, distinct from token auto-approval. The extension warning says the approved client can expose signed-in sessions and other tabs, so consent must be deliberate.

The nominal token-free invocation below remains ON HOLD until the living approves through Fable; it has not been run:

```sh
mkdir -p /tmp/browser-trial/output
printf '%s\n' '{"outputDir":"/tmp/browser-trial/output","outputMode":"stdout","codegen":"none"}' > /tmp/browser-trial/config.json
env -u PLAYWRIGHT_MCP_EXTENSION_TOKEN \
  PLAYWRIGHT_MCP_OUTPUT_DIR=/tmp/browser-trial/output \
  playwright-cli --config=/tmp/browser-trial/config.json \
  -s=browser-bridge attach --extension=chrome \
  > /dev/null 2>&1
```

The command has no token in argv, environment, URL, or file. The generated connect URL contains only a loopback relay endpoint, random relay UUID, client metadata, and protocol version. It causes Chrome to open the extension's consent page; the living must select a tab. `detach` is the supported teardown and leaves the external Chrome running:

```sh
playwright-cli -s=browser-bridge detach > /dev/null 2>&1
```

The CLI documentation states that attached sessions use in-memory browser state by default and that `detach` tears down the attached session without affecting the external browser. The CLI has no documented switch to disable automatic snapshots. Its documented default `outputMode` is `stdout`; redirecting stdout only moves any emitted snapshot/page text into a file and is not a privacy control. Suppress attach output entirely and inspect only the command exit status. Do not run `snapshot`, `state-save`, cookie, storage, network, screenshot, or page-read commands until the living has selected the intended tab and the main flow has imposed a page-specific read boundary. Do not retain raw attach logs or automatic snapshot text; discard command stdout/stderr until an explicitly filtered credit-row extraction.

No invocation was made by this flow.

## Installed consent UI and enforced scope

Source was inspected in both installed copies, without opening Chrome:

* Default `0.5.0` and Profile 1 `0.2.1` display the same exact strings: `⚠️ Warning: Allowing this connection exposes the entire browser to the client, including any signed-in sessions, cookies, and content in other tabs and windows. Once approved, the client may also be able to reconnect later without showing this dialog again, unless you regenerate the token below and then restart the browser.` The page then says `You can drag tabs into the Playwright group later to make them accessible to the client. Optionally, select a tab to allow and immediately switch to it:` and each tab button is `Allow & select`. After approval it displays `"<client>" connected.`
* In both copies, the initial no-token page enumerates all debuggable tabs. Selecting one sends `connectToTab`; the extension calls `chrome.debugger.attach` for that selected tab and focuses it. This is not a read-only grant: the attached debugger relay can issue supported CDP commands against the tab, including page inspection and actions. The UI warning explicitly claims browser-wide exposure, signed-in sessions, cookies, and other-tab content; treat that as the consent scope rather than assuming page text only.
* Default `0.5.0` enforces a Playwright tab group named `Playwright` or `Playwright · <client>`. The selected tab is placed into that group; tabs dragged into that group are attached, and tabs removed from it are detached. Navigations of grouped tabs are reattached when debuggable. Thus the initial click is one tab, with a continuing group-based scope that can expand when the user drags tabs into the group. New tabs are not automatically added merely because they are opened; they become controlled when entering the Playwright group. Closing the relay detaches/cleans up and ungroups controlled tabs.
* Profile 1 `0.2.1` is legacy single-active-group behavior: its `ConnectedTabGroup` attaches the selected tab and has no group-style argument in `_connectTab`; it does not implement the 0.5.0 client-named tab-group expansion. It still holds a debugger connection to the selected tab until relay disconnect, tab close, or extension cleanup. This is source behavior, not a claim that the active user tab is in Profile 1.
* Revocation/lifetime: the source closes the debugger connection on relay close and removes listeners; 0.5.0 ungroups its controlled tabs. The connect page's warning says token-approved connections may reconnect without the dialog until token regeneration plus browser restart. For no-token interactive approval, the source provides no persistent approval record: each new CLI relay opens the consent page and requires selection. The extension's own action/status UI can disconnect active connections. `playwright-cli detach` tears down the relay while leaving Chrome running; it does not revoke the extension installation or alter account sessions.

These are source observations for the installed versions. They do not establish which profile owns the desired account tab until the living sees the consent page's tab list.
