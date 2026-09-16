# Codex successor package v5

Unlaunched proposal for a successor of cf7879 at depth 1, paired with efa157.
`baseInstructions` is the replacement field established by the supported
app-server schema. The dry-run script imports the repository's supported
`tools/codex-app-server-client.mjs`; it has no socket path, creates no thread,
and makes no RPC request unless a later authorized launcher supplies one.

First order: develop the Cloud Nexus DNS capability for
`xmpp.goldragon.criome.net`, keeping Cloudflare credentials in gopass-to-program
flow. Prosody/accounts/bot and production deployment belong to secondary.
