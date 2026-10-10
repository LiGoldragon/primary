# Codex and Claude Home activation

The living-authorized Home activation is complete.  Lojix deployment `61`
installed immutable CriomOS-home revision `f05a3639de72` for user `li` on
Ouranos through the existing `HomeManagerNixProfileV1` path.  Topology was
proved first: Lojix accepted the proposal's Ouranos host-key material and
strict user SSH reached a host reporting Ouranos.  This avoids the historical
logical-node/activation-endpoint mismatch recorded in flow `01a02fe5`.

The exact package separately evaluated and remote-built on Prometheus with
local jobs disabled and fallback forbidden.  The projected graphical,
medium-or-larger gate was true, so both Codex Desktop and Claude Desktop are
present in the activated profile.  The remote builder proof and Lojix
activation are separate evidence.

Lojix accepted deployment `61` and its ordinary node ledger later recorded a
successful terminal state and Current generation.  The direct ordinary
deployment-ID reader produced a frame I/O error during observation; this is a
client/read-path limitation, not a terminal failure claim.  The successful
node ledger and strict live-profile check independently establish completion.

The live profile changed generation, uses Codex `0.149.0` from the shared
llm-agents derivation, and retains Claude Code `2.1.241`.  Both Codex Desktop
and Claude Desktop launchers are present, while the Codex remote-control and
Agent Intercom Codex bridge services are active.  Claude Desktop's embedded
runtime remains intentionally unasserted because the supported integration
does not expose it.

## Sources

- [Activation witness](../witnesses/codexHomeActivation.md)
- [Remote deployment proof](../witnesses/codexDesktopDeployment.md)
- [Recovered deployment procedure](rememberedUserDeployment.md)
- [Historical topology incident](../../01a02fe5/reports/wrongHomeDeployment.md)
