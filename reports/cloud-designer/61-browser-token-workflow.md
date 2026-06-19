# 61 · Supervised browser workflow — DigitalOcean token to gopass + funding (2026-06-19)

A concrete, runnable supervised procedure that drives the psyche's own
visible browser to: **(a)** sign in to DigitalOcean, **(b)** mint a
personal access token with write scope and land it in gopass at
`digitalocean/api-token`, **(c)** reach the billing page so the human can
add a payment method / funds. End goal: unblock the cloud daemon's live
DigitalOcean test from report 60 (the daemon reads the token by-handle as
`DIGITALOCEAN_ACCESS_TOKEN`).

**This report DESIGNS and HANDS BACK the workflow. Nothing here was
executed.** No browser was driven, no account accessed, no money moved.
The probes below only checked which binaries exist on this host and the
*names* (never values) of existing gopass entries.

## 0 · Governing intent (the workflow must embody these)

| Spirit | Verbatim substance | Workflow consequence |
|---|---|---|
| `7hmc` (Clarification) | "A browser agent should be usable in supervised scout mode: it scans visible account pages, reports the UI state and possible next steps step by step, and waits for human decisions before taking consequential actions." | Every AGENT step is scan + report + WAIT. No consequential click without an explicit human go-ahead. |
| `5g4d` (Clarification) | "the preferred browser surface is the human's main Chrome profile rather than a temporary guest automation profile, so logged-in state and familiar browser context are available when safe." | We try to reuse the human's logged-in Chrome — but a Chrome-136+ security rule blocks this on the default profile (see §1.3). This is the central tension and an open question. |
| `7o4q` (Clarification) | "two paths: an optional Playwright MCP server for direct agent browser tooling, and a browser-use-style delegated smaller/faster LLM path." | We pick the Playwright-CDP path now; the MCP server is the heavier alternative (§1.4). |
| `s8lq` (cited by the directive) + `nsi2` (Decision) | secrets are env-var-populated by the password manager, "never echoed"; no human-driven leakage. | Token value never enters a prompt, chat, report, or log. Funding is real money and human-only. |

`s8lq` is cited by the task as the supervised-scout / human-driven-money
intent; `7hmc`, `5g4d`, `7o4q` were read verbatim from the live Spirit
store and govern the mechanism. `nsi2` is the proven Cloudflare secrets
pattern this reuses.

## 1 · Tooling recommendation

### 1.1 The gap, stated honestly

**This environment has NO browser-automation capability wired right now.**
ToolSearch surfaces only `WebFetch` (fails on authenticated/private URLs
— it cannot see an account page) and `WebSearch`. There is no browser MCP
server, no Playwright/Puppeteer/Selenium skill, no CDP-attach mechanism in
the session. So a driver must be stood up before any of §2 can run, and
that requires the psyche's approval (it launches a browser and installs an
npm package).

### 1.2 What the host already has (probed, read-only)

- **Google Chrome 147** at `~/.nix-profile/bin/google-chrome`
  (`/nix/store/...google-chrome-with-hexis/...`). No relaunch-with-driver
  binary needed beyond a flag.
- **Node v24.14.1** + **npx** in the nix profile — so Playwright can be
  fetched with `npx` with no global install.
- **gopass** present; store unlocked enough to list names. It already
  holds `cloudflare.com/` entries (proof the store + pinentry work) and
  **no `digitalocean/` entry yet** — consistent with this task.
- **nix** present. No Chrome currently running; nothing on debug port 9222.
- Playwright is **not** installed (no global package).

### 1.3 Recommended mechanism: Playwright `connectOverCDP` attaching to a visible Chrome

Playwright as a **CDP client** (not a browser launcher) attaching to a
Chrome the human started with `--remote-debugging-port`. The human sees
the exact same window and can grab the mouse at any moment — this is what
makes "supervised scout mode" real rather than nominal.

Because the host already ships Chrome, we do **not** need
`playwright-driver.browsers` / `PLAYWRIGHT_BROWSERS_PATH` (that nixpkgs
dance is only for Playwright *launching* its own bundled Chromium). We
attach to the existing Chrome, so we only need the Playwright npm client
as a CDP speaker. Minimal, lowest-friction.

**The Chrome-136+ security rule — the load-bearing constraint.** Since
Chrome 136 (host is 147), `--remote-debugging-port` is **ignored / refused
on the default `--user-data-dir`** profile, to stop a local process
reading your full browsing state. Remote debugging now *requires* a
**non-default** `--user-data-dir`. Two consequences:

1. We cannot attach to the human's normal, already-open Chrome window.
2. This collides with Spirit `5g4d` (prefer the main profile for its
   logged-in state). The honest resolution: use a **dedicated automation
   profile dir** (`~/.cache/do-token-scout-profile`). It is empty on first
   run, so the human logs in fresh **once** inside it (that login is a
   HUMAN step anyway, §2). It is a real persistent profile the human
   watches — not a hidden guest context — which honours the *spirit* of
   `5g4d` (familiar, persistent, human-visible surface) within the
   security rule. Confirm with the psyche (§5, Q2).

**Setup the psyche must do / approve before §2 can run:**

1. **Approve launching Chrome with a debug port and a scratch profile.**
   Close other Chrome windows first (the port attaches to one Chrome
   process). Launch:
   ```sh
   google-chrome \
     --remote-debugging-port=9222 \
     --user-data-dir="$HOME/.cache/do-token-scout-profile" \
     "https://cloud.digitalocean.com/"
   ```
   Verify the port is live (returns JSON, no secret):
   `curl -s http://127.0.0.1:9222/json/version`.
2. **Approve fetching the Playwright client** (one npm package via npx; no
   global install, no bundled-browser download since we attach):
   ```sh
   cd "$HOME/.cache/do-token-scout"        # scratch dir for the driver
   npm init -y >/dev/null
   npm install playwright-core             # CDP client only; no browsers
   ```
   `playwright-core` is deliberate — it ships the CDP client without
   downloading Chromium, since we attach to the host Chrome.
3. **gopass must be unlockable** by the human's key (pinentry) at token
   time — already true on this host.

All three need explicit psyche approval: #1 opens a browser and #2
installs a package. The agent proposes; the psyche runs (or authorises the
agent to run) these.

### 1.4 Alternatives considered

- **Browser-use / a browser MCP server** (e.g. Chrome DevTools MCP,
  Playwright MCP) added to session config. Heavier: edits harness config,
  pulls a server, and most variants hit the *same* Chrome-136 profile
  rule. Better as a durable capability (matches `7o4q`'s "optional
  Playwright MCP server" path) but overkill for this one-shot token errand.
  Recommend deferring; if the psyche wants browser automation as a
  standing tool, stand up the MCP server as a follow-up.
- **nixpkgs `playwright` + `playwright-driver.browsers`** launching its own
  Chromium. Rejected: needs `PLAYWRIGHT_BROWSERS_PATH`,
  `PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS`, version-matching gymnastics
  on NixOS, and a fresh browser with no familiar context — strictly worse
  than attaching to the Chrome already on the box.

**Pick: Playwright `connectOverCDP` against the host's Chrome (§1.3).**

## 2 · The supervised workflow

Legend: **[AGENT]** = automated navigate / scan / report, ends at a WAIT.
**[HUMAN]** = the psyche acts in the visible window; the agent does not.
**[WAIT]** = the agent blocks on an explicit human go-ahead in chat.

The agent connects with `connectOverCDP('http://127.0.0.1:9222')` and
operates on the existing page. It **closes only its own context on exit**,
never the browser, so the human's session survives.

### Phase A — Attach and sign in

- **A1 [AGENT]** Connect over CDP, locate the DigitalOcean tab, report the
  current URL + visible page state (login form? already signed in?
  dashboard?). List the possible next steps. **[WAIT]**
- **A2 [HUMAN]** If not signed in: the human types email/password and
  completes **2FA** directly in the window. The agent **never** types
  credentials or 2FA codes and does not read the password field. The human
  says "signed in" when the dashboard is up.
- **A3 [AGENT]** Re-scan: confirm a signed-in dashboard (look for account
  chrome / the team name region, no value capture). Report. **[WAIT]**

### Phase B — Create the write-scope personal access token

Public click-path confirmed from DigitalOcean docs (§ Sources):

- **B1 [AGENT]** Navigate to the API tokens page:
  `https://cloud.digitalocean.com/account/api/tokens`
  (Control Panel path: **Account → API → Tokens** / "Applications & API").
  Scan and report the "Personal access tokens" section and the **"Generate
  New Token"** button. **[WAIT]**
- **B2 [HUMAN or AGENT-with-go-ahead]** Open the Generate-New-Token form.
  Filling **Token name** (suggest `criome-cloud-livetest`), **Expiration**,
  and **Scopes** is safe non-secret config. Recommended: the **HUMAN**
  selects the scope to keep the consequential choice human-owned;
  alternatively the agent fills the form on an explicit go-ahead and the
  human reviews before submit. Scope = **Full Access** (the `api:write`
  alias — write scope, what the live test needs to create/destroy
  droplets). The docs warn the **secret is shown only once**.
- **B3 [HUMAN]** The human clicks the final **Generate Token** button
  (this is the consequential action that mints the secret — human-owned per
  `7hmc`). The new token string appears **once** on screen.
- **B4** Hand the token to gopass — **see §3. The token value never enters
  chat, a report, a prompt, or a log.**
- **B5 [AGENT]** After §3 confirms the entry exists, report success by
  **name only** (`digitalocean/api-token` present) — never the value.
  **[WAIT]** for the human to dismiss the one-time token panel.

### Phase C — Billing / payment method / funds (human-only money)

- **C1 [AGENT]** Navigate to `https://cloud.digitalocean.com/account/billing`.
  Scan and report: current balance region, the **"Payment Methods"**
  section, and whether an **"Add payment method"** button is present.
  Report the possible next steps. **[WAIT]**
- **C2 [HUMAN]** The human clicks **"Add payment method"**, which opens the
  **"Add a new payment method"** window, and **enters all card / PayPal /
  wallet details themselves**. The agent never reads or types payment
  fields.
- **C3 [HUMAN]** To add funds: the human opens the **"Make a payment"**
  page (`https://cloud.digitalocean.com/pay-now`), chooses the **Payment
  Amount** (past-due / current-period / **custom amount**), and clicks the
  final **"Submit Payment"** button. **This is real money and is
  human-driven and human-confirmed — the agent NEVER clicks Submit Payment
  / Pay / Add funds.** See §4.
- **C4 [AGENT]** After the human says funding is done, optionally re-scan
  the billing page to confirm a payment method now shows as present
  (boolean state only, no card numbers). Report. Done.

### 2.1 Runnable artifact — AGENT-AUTOMATED parts only (Playwright/CDP)

Scan-and-report only. **No login, no payment, no token-mint, no
submit-payment click lives in this script.** Each consequential action is a
human step in §2.

```js
// do-token-scout.js  —  AGENT-AUTOMATED scout only (Node + playwright-core)
// Run AFTER the human launched Chrome with:
//   google-chrome --remote-debugging-port=9222 \
//     --user-data-dir="$HOME/.cache/do-token-scout-profile" \
//     https://cloud.digitalocean.com/
// Usage: node do-token-scout.js <a1|b1|c1>   (one scout step per call)
const { chromium } = require('playwright-core');

const PAGES = {
  tokens:  'https://cloud.digitalocean.com/account/api/tokens',
  billing: 'https://cloud.digitalocean.com/account/billing',
};

// Report only structural UI facts — labels, URLs, presence of buttons.
// NEVER read input values, the one-time token panel text, or card fields.
async function scan(page) {
  const url = page.url();
  const buttons = await page.getByRole('button')
    .all().then(bs => Promise.all(bs.map(b => b.innerText().catch(() => ''))))
    .then(ts => ts.map(t => t.trim()).filter(Boolean).slice(0, 40));
  const signedIn = await page.locator('[data-testid="topbar"], nav')
    .first().isVisible().catch(() => false);
  return { url, signedIn, buttons };
}

(async () => {
  const step = process.argv[2] || 'a1';
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  try {
    const ctx = browser.contexts()[0];           // the human's live context
    const page = ctx.pages()[0] || await ctx.newPage();
    if (step === 'b1') await page.goto(PAGES.tokens,  { waitUntil: 'domcontentloaded' });
    if (step === 'c1') await page.goto(PAGES.billing, { waitUntil: 'domcontentloaded' });
    const state = await scan(page);
    // Structural report to chat — contains no secrets, no field values.
    console.log(JSON.stringify(state, null, 2));
    console.log('\nWAIT: report the above, list next steps, await human go-ahead.');
  } finally {
    // Detach only — do NOT browser.close(); the human keeps their session.
    await browser.close.call({ _connection: browser._connection });  // detach CDP
  }
})();
```

The detach line is intentional: on a `connectOverCDP` session, the
Playwright `browser` handle owns only the CDP connection, so releasing it
leaves the human's Chrome untouched. (If a Playwright version makes
`browser.close()` tear down the remote browser, replace with dropping the
connection / process exit; never call any `context.close()` on the human's
context.)

## 3 · Token → gopass, privacy-safe

**Recommended path (privacy-safest): the HUMAN pastes into a local
`gopass insert` prompt. The token string never touches the agent, the
Playwright script, chat, a report, or any log.**

When the one-time token is on screen (B3), the human runs, in their own
terminal:

```sh
gopass insert digitalocean/api-token
# gopass prompts; the human pastes the token; it is written encrypted.
# The value is never echoed and never passed as argv.
```

Then verify **blind** — names and exit code only, never the value (per
`skills/secrets.md`):

```sh
gopass ls | grep -F digitalocean/api-token   # presence by name only
```

Why human-paste over script-reads-DOM: it keeps the secret on a path the
agent literally cannot observe (terminal stdin → gopass), needs no
DOM-scraping of the one-time panel, and matches the `nsi2` "never echoed"
discipline. The Playwright scout is explicitly forbidden from reading the
token panel's text.

**If (and only if) the psyche prefers a hands-off capture**, the *fallback*
is a zero-echo pipe — but it must never surface the value:

```sh
# FALLBACK ONLY, on explicit psyche request. The script must write the
# token to stdout ONCE and pipe straight into gopass; nothing else reads it,
# nothing prints it, and it never returns to the agent's chat/report/logs.
node read-do-token.js | gopass insert -f digitalocean/api-token >/dev/null
```

The agent does **not** see that stdout (it is consumed by the pipe), must
not log it, and must not echo it back. Recommendation: **prefer the
human-paste path**; only use the pipe if the psyche asks, because it is the
only way the secret never lives in any process the agent spawned.

The daemon consumes this exactly as report 60 specifies: the cloud flake's
gopass shim exports `gopass show -o digitalocean/api-token` as
`DIGITALOCEAN_ACCESS_TOKEN` at exec, by-handle, never echoed — the same
`wrapProgram` pattern proven for Cloudflare (`nsi2`).

## 4 · Funding is explicitly human-only

Adding a payment method and adding funds (Phase C) is **real money and the
psyche's private financial affairs.** The agent:

- never reads or types card / PayPal / wallet fields;
- never clicks **"Add payment method"** submit, **"Submit Payment"**,
  "Pay now", or any final charge/add-funds control;
- only navigates to the billing URL, reports the UI state (button presence,
  balance region — no card data), and WAITS.

The human performs and confirms every money action in their own visible
window. This is `7hmc` (no consequential action without human decision)
applied at its strictest, plus the privacy discipline on financial
substance. Card numbers, amounts, and balances are private substance and
stay out of this report, chat, and any log.

## 5 · Open questions for the psyche

1. **Approve the tooling setup?** May the agent (or will the psyche) run
   the §1.3 setup — launch Chrome with `--remote-debugging-port=9222` and a
   scratch `--user-data-dir`, and `npm install playwright-core` in a
   scratch dir? Nothing is installed yet; this is the gate before §2.
2. **Profile choice (the `5g4d` tension).** Chrome 136+ refuses remote
   debugging on the default profile, so we must use a dedicated
   `--user-data-dir`. That means a **one-time fresh DigitalOcean login** in
   that automation profile rather than reusing the main profile's existing
   session. Acceptable? (The alternative — the heavier MCP path — mostly
   hits the same rule.)
3. **Which browser / is Chrome the right surface?** Host has Google Chrome
   147 only (no Firefox/Chromium/Brave). Confirm Chrome is the intended
   surface.
4. **Token-capture path:** human-paste into `gopass insert` (recommended,
   §3) — or the hands-off zero-echo pipe fallback? Default to human-paste
   unless you say otherwise.
5. **Scope confirmation:** Full Access (`api:write`) is what the live test
   needs (create/destroy droplets). Confirm you want write, not a narrower
   custom scope. Also choose an expiration (the form requires one).
6. **Standing capability?** Want browser automation as a durable tool (the
   `7o4q` Playwright-MCP path) as a follow-up, or just this one-shot errand?

## Sources

- DigitalOcean — Create a Personal Access Token:
  https://docs.digitalocean.com/reference/api/create-personal-access-token/
  (Account → API → Tokens; **Generate New Token**; Token name / Expiration /
  Scopes with **Full Access** = `api:write`; secret shown **once**).
- DigitalOcean — Scopes for API Tokens:
  https://docs.digitalocean.com/reference/api/scopes/
- DigitalOcean — Manage Payment Methods (`https://cloud.digitalocean.com/account/billing`,
  **"Add payment method"** → **"Add a new payment method"**):
  https://docs.digitalocean.com/platform/billing/manage-payment-methods/
- DigitalOcean — Pay Your Bill (`https://cloud.digitalocean.com/pay-now`,
  **Payment Amount**, **Submit Payment**):
  https://docs.digitalocean.com/platform/billing/pay-bills/
- Playwright `connectOverCDP` attach-to-existing-Chrome:
  https://playwright.dev/docs/api/class-browsertype#browser-type-connect-over-cdp
- Chrome 136 remote-debugging change (default profile blocked; requires
  non-default `--user-data-dir`):
  https://developer.chrome.com/blog/remote-debugging-port
- Cross-references: report 60 (DO provider landed, live-test runbook),
  `skills/secrets.md` (gopass / pipe-source-to-sink / verify-blind),
  Spirit `7hmc`, `5g4d`, `7o4q`, `nsi2`.
