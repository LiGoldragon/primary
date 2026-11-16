# Browser trial report

Flow: 12b000. Observed 16 November 2026, approximately 17:35 UTC. Instruction: Psyche core Opus wnd5, `instructions.md` beside this report.

## Result

The saved-token extension bridge worked. The trial read Billing through his own Chrome with existing login, without human interaction, sign-in input, profile copying, or site changes. The console URL redirected to `https://platform.claude.com/settings/billing`. The page was in Spanish.

Only the requested credit facts:

| Credit type | Remaining balance | Expiry |
| --- | --- | --- |
| Promotional — API credit (Ultra) | US$193.54 of US$200.00 | 19 November 2026, 00:00 UTC |
| Promotional — API credit (Ultra) | US$200.00 of US$200.00 | 19 December 2026, 00:00 UTC |

Promotional balance: US$393.54. Purchased credit balance: US$0.00. The navigation badge briefly showed US$393.55; the credit section and two grant rows above agreed on US$393.54 at the final read.

## Each step and instruction clarity

1. **Done, after restoring the desktop display environment.** `pgrep -a chrome` initially matched only unrelated Electron crash handlers, not Chrome. A plain `google-chrome-stable` failed with these exact errors:

   ```text
   Missing X server or $DISPLAY
   The platform failed to initialize.  Exiting.
   ```

   `systemctl --user show-environment` supplied `DISPLAY=:0` and `WAYLAND_DISPLAY=wayland-1`. With those environment values, the same unflagged Chrome command started. Chrome 157.0.8103.78 was observed with no alternate user-data-directory or explicit profile argument. A foreground tool session kept the browser alive; detached launches had not left a running browser. **Clearer instruction:** distinguish Chrome from crash handlers, import the desktop display variables when absent, and keep the launched GUI process alive. No profile-selection flag was added. The runtime-selected profile name was not independently verified.

2. **Done.** The specified gopass entry supplied a nonempty token directly to the wrapper environment as `PLAYWRIGHT_MCP_EXTENSION_TOKEN`. Its value was never printed or written to a report/log. The installed wrapper has a different automatic lookup path; setting the specified environment variable explicitly bypassed that lookup. **Clearer instruction:** retain the explicit environment assignment; do not rely on the wrapper lookup. Existing bridge implementation puts its connection token in a transient extension URL/Chrome argument, as previously authorized; this trial does not prove stronger token confinement.

3. **Done, with corrected CLI syntax.** The installed wrapper delegates to playwright-cli 0.1.13. Bare `--extension` produced this exact error:

   ```text
   Error: no target specified for attach command; use one of [name], --cdp, --endpoint, or --extension to specify the target to attach to.
   ```

   The working form was `playwright-chrome --raw -s=browser-12b000 attach --extension=chrome --config=<scratch>/config.json`, under the desktop display environment and token environment from step 2. Configuration selected a private temporary output directory, stdout output, and no code generation. A 60-second outer timeout bounded this trial; attach completed in under one second. The sole controlled page was initially the extension connection page, titled Welcome. `playwright-cli --raw -s=browser-12b000 goto https://console.anthropic.com/settings/billing` navigated that same tab to Billing; no second trial tab was opened. **Clearer instruction:** include the `attach` subcommand, `--extension=chrome`, session selection, and same-tab `goto`; attachment itself does not open Billing.

4. **Done.** Read-only DOM evaluation extracted the credit section and both promotional grant rows. English-only labels initially missed the Spanish UI; localized labels (`Saldo de créditos`, `Caduca el`, `crédito promocional`) found the requested fields. **Clearer instruction:** allow localized labels and read every grant row; expiry belongs to each grant, not necessarily one account-wide date.

5. **Done.** `playwright-cli --raw -s=browser-12b000 tab-close` returned exit 0, then `playwright-cli --raw -s=browser-12b000 detach` returned exit 0. Chrome remains running. Generated page artifacts were deleted without opening them. **Clearer instruction:** close the controlled trial tab, detach the bridge, and remove temporary snapshots. `--raw` did not prevent an automatic snapshot artifact at attach.

## Sanitized reproducibility contract

Wrapper: `/home/li/.nix-profile/bin/playwright-chrome`. Delegated installed CLI: `/nix/store/29jvfww5dd4682wvqliqdrrdaqzibir4-playwright-cli-0.1.13/bin/playwright-cli`. Ordinary installed wrapper source was inspected. The supported token consumer is its environment variable `PLAYWRIGHT_MCP_EXTENSION_TOKEN`; no token argument is supplied by the flow. No new helper, bridge installation, Allow click, or sign-in was needed. Existing extension inventory and implementation caveats: `flows/d94525/browser-trial.md`.

Scratch configuration used `outputDir`, `outputMode: "stdout"`, and `codegen: "none"`; commands ran from a private temporary directory. `--raw` is an output formatter, not a guarantee against snapshot files. Reuse one named session for attach, goto, eval, tab-close, and detach; close only its controlled trial tab, leaving external Chrome running. This report records one successful invocation, not the cause of previous handshake failures.

## Second trial — OpenAI API credit grants

Authorization: Psyche core Opus oerw/ar62. Observed 16 November 2026, approximately 17:44–17:47 UTC. The instruction corrections were first folded into `instructions.md`, including display inheritance, exact attach syntax, structural/positional field selection, second page, and cleanup (commit f602cdd0a).

**Requested balance:** US$183.88 remaining, calculated from the two available grant balances (US$120.00 + US$63.88). Independently, the summary tooltip explicitly said US$156.12 used of US$340.00 total granted, giving the same US$183.88 remaining. The displayed summary fraction is used/total, not remaining/total.

| Grant amount | Remaining | Expiry shown | Credit type |
| --- | --- | --- | --- |
| US$120.00 | US$120.00 | 3 December 2026; time and timezone not displayed | API credit grant; subtype not displayed |
| US$100.00 | US$63.88 | 31 March 2027; time and timezone not displayed | API credit grant; subtype not displayed |
| US$10.00 | US$0.00 | Not displayed (`-`); inactive | API credit grant; subtype not displayed |
| US$100.00 | US$0.00 | Not displayed (`-`); inactive | API credit grant; subtype not displayed |
| US$10.00 | US$0.00 | Not displayed (`-`); inactive | API credit grant; subtype not displayed |

The table exposes received date, state, balance and expires columns, not a type column. Available/inactive are states, not credit types. No expiry cell supplied title, datetime or accessible-label metadata containing a time zone. Time, timezone and grant subtype remain **unknown**, rather than inferred from the Anthropic page or local timezone.

### Step outcomes

1. **Done:** reused the external Chrome already running from the earlier trial; no profile copy, new browser launch or profile-selection flag.
2. **Done:** a new private temporary CLI working/output directory and explicit named session were used. The saved token went directly from the authorized gopass entry to the wrapper environment; no value was printed or logged.
3. **Done:** `playwright-chrome --raw -s=openai-12b000 attach --extension=chrome --config=<scratch>/config.json` attached in under one second. The initial controlled page was Welcome. Navigated that same trial tab to `https://platform.openai.com/settings/organization/billing/credit-grants`; navigation returned exit 0. No additional trial tab, Allow click, sign-in, organization switch or site change.
4. **Done, with explicit gaps above:** initial navigation completed before the client-rendered table appeared, so the first structural read returned no headings or tables. A subsequent read found one native table. Read its header/cell structure and four column positions, rather than matching translated credit labels. Extracted all five grants. Read-only inspection of expiry-cell metadata found no hidden timestamp/timezone. Hovering the summary amount revealed the used/total tooltip, resolving its meaning without changing account state. No table row exposed a type field or details control. **Instruction improvement:** wait for the credit table's visible DOM event before extraction; inspect the summary tooltip before interpreting a fraction. An absent type/timezone is a reportable gap, not permission to invent one.
5. **Done:** same-session `tab-close` and `detach` both returned exit 0. Generated scratch files were deleted unread. External Chrome remains running. No site mutation or sign-in was performed.
