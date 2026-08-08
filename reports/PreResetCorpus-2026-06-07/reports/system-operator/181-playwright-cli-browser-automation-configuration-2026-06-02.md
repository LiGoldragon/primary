# Playwright CLI Browser Automation Configuration

## Result

CriomOS-home now packages `@playwright/cli` as `packages/playwright-cli`
and installs it in the min profile's AI package set. The package disables
Playwright browser downloads during the Nix build, so it does not smuggle
mutable browser binaries into the profile.

The repo also has a focused Nix check:
`checks/playwright-cli/default.nix`. The check proves that
`playwright-cli` is on `PATH` in the derivation environment and that
`playwright-cli --help` starts successfully.

Follow-up after real extension testing: the package now also exposes
`playwright-chrome`. That wrapper reads
`gopass:chrome-browser/playwright-mcp-extension-token` at runtime and sets
the Chrome executable path for NixOS, so extension attach commands do not
need manual environment setup.

## Browser-use Boundary

Browser-use does not need to call the Playwright CLI to use Chrome. It has
its own command line and browser/session layer, and current docs say its
CLI supports real Chrome with existing profiles, `browser-use connect`,
and explicit CDP URLs.

The clean model is:

- `playwright-cli`: deterministic shell/browser automation surface for
  agents.
- `browser-use`: delegated browser-agent layer that can use CDP directly.
- Playwright MCP: optional MCP tool surface for agents that want MCP
  rather than shell commands; it can connect to existing Chrome through
  CDP or the Playwright browser extension.

The integration point is CDP or extension-backed existing-tab access, not
"browser-use wraps Playwright CLI".

## Current Evidence

- Local direct package build succeeded through the configured remote
  builder.
- `checks.x86_64-linux.playwright-cli` succeeded through the configured
  remote builder.
- `nix eval .#packages.x86_64-linux.playwright-cli.meta.mainProgram`
  returns `playwright-cli`.
- Extension attach succeeded against the main Chrome session when using
  the gopass-backed extension token and the NixOS Chrome executable path.
  The attached session navigated to `https://midigi.digimobil.es/login`.
- `nix fmt` currently fails because the repo formatter package receives
  no file input from the `nix fmt` wrapper; formatting the touched Nix
  files directly with `nix run nixpkgs#nixfmt -- ...` succeeds.

## Sources

- Playwright CLI configuration docs: https://playwright.dev/agent-cli/configuration
- Playwright MCP existing-browser connection docs: https://playwright.dev/mcp/configuration/browser-extension
- Browser-use CLI docs: https://docs.browser-use.com/open-source/browser-use-cli
- Browser-use Playwright/CDP integration docs: https://docs.browser-use.com/cloud/browser/playwright-puppeteer-selenium
