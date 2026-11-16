# Browser trial: two billing pages through his own Chrome

Goal: read the requested credit facts through his existing browser login, without human interaction.

Rules:
- Use his own Chrome and its normal profile. Never copy profiles or cookies.
- Use at most one trial tab at a time; reuse it for both pages and close it after.
- Type no sign-in and change nothing on any site. He is away; ask him nothing.
- Keep the saved bridge token out of model output and logs. The existing bridge implementation places it in a transient local connection URL/Chrome argument, as already authorized.

## Preparation and attachment

1. Check actual Chrome processes, distinguishing Chrome itself from Electron crash handlers. If the shell lacks display variables, obtain only DISPLAY, WAYLAND_DISPLAY and, if present, XAUTHORITY from `systemctl --user show-environment`, and pass them to Chrome and the wrapper. Do not print the whole environment. If Chrome is absent, launch `google-chrome-stable` with no flags in that desktop environment. Keep the GUI process alive in the tool session; do not assume a detached launch survived. Use no alternate user-data-directory or profile-selection flags.
2. Create a private temporary working/output directory. Write configuration there with `outputDir` pointing inside it, `outputMode: "stdout"`, and `codegen: "none"`. Run all CLI commands from that directory. Automatic snapshots can still be generated even with `--raw`; keep them private and delete them unread after cleanup.
3. Obtain `gopass show -o playwright.dev/mcp-extension-token` directly into `PLAYWRIGHT_MCP_EXTENSION_TOKEN` for the wrapper environment only. Suppress credential-producer diagnostics; stop if the producer fails or returns empty. Do not rely on the wrapper automatic lookup, whose stored-entry path differs. Never echo the token or retain raw connection output. Discard attach output or redact the exact token and entire extension connection URL before it reaches any log/model.
4. Attach using `playwright-chrome --raw -s=<trial-session> attach --extension=chrome --config=<scratch>/config.json`. Use the same explicit session on every later command. The `attach` subcommand and `=chrome` value are required by the installed CLI; bare `--extension` failed. Bound the attach with an outer timeout (the successful trial used 60 seconds). Stop on failure; do not request an Allow click or create another bridge.
5. Attachment initially controls a Welcome extension-connection tab. Navigate that same controlled tab with `playwright-cli --raw -s=<trial-session> goto <page-url>`; do not open an additional tab. Discard navigation snapshots/output. If attachment controls an existing personal tab instead, stop rather than navigate that personal tab.

## Page 1 — Anthropic Console Billing

Navigate to `https://console.anthropic.com/settings/billing` (it may redirect to `https://platform.claude.com/settings/billing`). Read only the purchased/promotional balance and each grant's remaining amount, expiry including time zone, and credit type.

Use read-only DOM evaluation. Find the credit table/section by semantic structure: heading and adjacent amount, table header and column positions, or accessible row/cell roles. Determine amount/type/expiry from those positions, not a fixed English or Spanish label match. Keep returned text bounded to the credit section and requested fields; do not dump the entire page. If the timezone is not shown, report it as unknown rather than inferring it.

## Page 2 — OpenAI Platform credit grants

Reuse the same trial tab; navigate to `https://platform.openai.com/settings/organization/billing/credit-grants`. Wait for the visible credit table DOM event before extraction; navigation completion alone can precede client rendering. Read only the balance and each API credit grant's amount, expiry including time zone, and type. If a summary fraction has no label, read its tooltip before deciding whether it means used or remaining; retain an explicitly calculated remaining balance as a calculation. Match by table/row/cell structure and column position rather than language. Inspect only credit-section structure when necessary. If a different billing tab must be selected, a read-only navigation link within Billing is permitted; do not purchase credits, change billing settings, change organizations, or enter authentication. If signed out, access denied, or no grant data is visible, report that observation and stop. Report an absent timezone as unknown.

## Cleanup and report

Close only the controlled trial tab: `playwright-cli --raw -s=<trial-session> tab-close`. Then `playwright-cli --raw -s=<trial-session> detach`. Check both exit statuses. Leave external Chrome running. Delete the trial's generated snapshots and private temporary artifacts without opening them. On failure, still close the owned trial tab and detach when possible; do not kill the user's browser.

Write observations to `flows/5e646f/browser/report.md`. For each step state done or the exact error/visible condition and the instruction improvement needed. Record only the requested balance/grant facts as account content; retain earlier trial evidence. Answer the ordering flow in two lines with the report path and result.
