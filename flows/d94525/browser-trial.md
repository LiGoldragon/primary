# Browser bridge inventory

STATUS — STOPPED / TRANSFERRED: Opus0g0i, Fable89g1, moves handshake work to Field browserBridge Sol and dedicated-Chromium DevTools work to Field browser Sol. Deferred token-input research5hh0 transfers too. This flow performs no further browser work. Both installed-profile saved-token attempts timed out60s; cause unknown; no Billing rows read; no active trial relay remains, Chrome left running. Field core and Mind core know no verified working pairing/session provenance. Scratch pointer: /tmp/browser-bridge-d94525-path. Latest explicit72y7 allows saved-token wrapper local argv; no further Allow questions. Read the Main-flow execution/source corrections near the end before using earlier nominal commands.

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

## CLI output and bounded billing extraction

The installed CLI documentation says it provides a page snapshot after each command. `outputMode: "stdout"` (the default) emits that content to stdout; `outputMode: "file"` writes snapshots/logs under the configured output directory. There is no documented config field that disables automatic snapshots. The global `--raw` option is the relevant containment control: the installed skill documentation says it strips page status, generated code, and snapshot sections, returning only the command result. `eval --help` confirms `--filename` would persist a result, so do not use `--filename`.

Avoid `snapshot`, `tab-list`, or broad `eval(() => document.body.innerText)` commands. For the already-selected Billing tab, use `--raw` and return only rows matching the three requested fields, keeping the result in the shell pipe rather than writing a page dump:

```sh
playwright-cli --raw -s=d94525-billing eval \
  '() => { const rows = [...document.querySelectorAll("tr")].map(r => r.innerText.replace(/\\s+/g, " ").trim()).filter(Boolean); return rows.filter(r => /balance|remaining|credit|expir|valid until|renew/i.test(r)).slice(0, 8); }'
```

If the page is not table-based, use the same `--raw` envelope with a bounded line selector, never full body text:

```sh
playwright-cli --raw -s=d94525-billing eval \
  '() => { const lines = document.body.innerText.split(/\\n+/).map(x => x.trim()).filter(Boolean); return lines.filter(x => /balance|remaining|credit|expir|valid until|renew/i.test(x)).slice(0, 8); }'
```

The output is still account data and must stay in the private scratch channel; report only balance, expiry including timezone, and credit type. `goto` also normally emits a snapshot, so if navigation is required use `playwright-cli --raw -s=d94525-billing goto <known-billing-url>` and discard its empty/result output before the bounded `eval`. Do not use `--json` as a substitute for `--raw`, and do not retain output files containing page text.

## Saved-token attach wait and snapshot artifact risk

Source inspection shows extension attach creates a `ManualPromise` for the extension connection and `establishExtensionConnection()` awaits it without a visible timeout wrapper. If Chrome opens the connect page in a profile whose extension token does not match the saved token, the extension UI takes the invalid-token branch and the CLI can wait indefinitely for the relay handshake; the source provides no attach timeout or automatic fallback. The same symptom can occur if the connect page is opened in another Chrome profile/window or never reaches the extension relay.

Bounded cancellation should be applied by the owner before launch, for example an outer `timeout --signal=INT --kill-after=5s 60s ... playwright-chrome ... attach --extension=chrome`, with stdout/stderr discarded to a private scratch path. Do not kill the user's Chrome process; cancel only the CLI wrapper/session process. The owner currently owns the running process.

Observed in the first token-free attach: an automatic `page-*.yml` snapshot artifact was created even though the configured output mode was `stdout`; it was deleted without being read. Therefore `outputMode=stdout` is not sufficient evidence that page snapshots are never written. The installed CLI documentation says snapshots follow each command, while `--raw` strips snapshot sections from command output; it does not guarantee that internal snapshot artifact files are not created. Keep the CLI working directory and output directory in an isolated scratch directory, inspect no generated page files, and delete them after detach. `--raw eval` remains the narrowest result channel for the requested credit rows.

## Main-flow execution and revised ruling
The living's yes arrived via Opus reb3. Later Opus72y7 explicitly authorized the saved-token wrapper as it stands, accepting transient local Chrome URL argv and deferring stronger hiding. No further Allow click may be requested. The token was never printed or manually read by a model.
Token-free attachment exited0 but its sole controlled page was extension connect.html, not Billing; detached. Saved-token attachment did not complete its handshake; stopped only trial CLI/relay, leaving Chrome running. Two further60-second forced-profile trials, Default0.5.0 and Profile1 0.2.1, each exited124. Protocol versions match2 and extension disable_reasons metadata are empty. These observations do not establish the token is invalid or identify the cause. No account page or credit rows have been read.
Output correction: coreBundle.js around58760 has rawSections=[Error,Result,Snapshot], so raw is not a blanket snapshot suppressor. Around65300 CLI configuration explicitly overrides snapshotMode to full. One automatically generated page-*.yml from the token-free attach was deleted unread; no raw artifact was inspected. Filtered eval calls generated no further snapshot file. Main asked Mind core Sol for the existing pairing/working-session holder, not a duplicate producer or fresh human approval.
