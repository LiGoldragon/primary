# Claude Desktop callback registration is deployed

Deployment `62` completed successfully for `li` on Ouranos. The active Home
generation now exposes Claude Desktop's package-owned desktop entry in the
user XDG applications directory and resolves `x-scheme-handler/claude` to
`claude-desktop.desktop`.

This repairs the diagnosed missing discoverability/mapping condition that led
the desktop to show a chooser for Claude callbacks. It does not prove a full
OAuth exchange or browser focus behavior, which were intentionally not
replayed to avoid handling callback data. If sign-in still fails, the next
diagnostic scope is the browser-to-desktop handoff after this handler state is
confirmed live.

The change remains gated with the pre-existing medium graphical Claude Desktop
projection, reuses the already selected `llm-agents` package, and adds no
runtime override or stateful installer. Claude's embedded Code runtime remains
unobservable through this supported package interface.

## Evidence

- Home source and focused remote proof: `8d6e790c06e6`.
- CriomOS exact consumer pin and remote top-level proof: `1402eaa692ec`.
- Lojix terminal node-ledger result: deployment `62`, `Completed/Succeeded`,
  Current.
- Live XDG entry, cache mapping, and default query: see
  [deployment witness](../witnesses/claudeOAuthHandlerDeployment.md).

