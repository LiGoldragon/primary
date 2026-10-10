# Horizon design ruling — 2026-07-29

Context: `horizon-cli --cluster goldragon --node zeus` rejected a Zeus proposal
without Agent Intercom capabilities: `trusted node zeus lacks the required local
Agent Intercom capability`.

Psyche ruling: `AgentIntercomLocal` and `AgentIntercomGraphical` are opt-in
node features. A trusted node must never implicitly gain or be required to
declare either capability.

This answers the agent message requesting removal of Zeus's Agent Intercom
capabilities; it authorizes removal of the trusted-node baseline requirement
while retaining only the explicit graphical-requires-local invariant.

Context: the direct Bird hotfix created command shims, a PATH override, and
mutable VSCodium state beneath `/home/bird` to bypass a broken managed
lifecycle. This ruling answers that just-used hotfix technique.

Psyche ruling: Bird’s user environment is changed only through CriomOS-home.
Never install command shims, wrappers, PATH overrides, or managed application
state directly under `/home/bird`.

Newer, superseding ruling: Any part of an environment already owned by Nix,
CriomOS, or CriomOS-home must be fixed, updated, and maintained only through
that owning declarative source. Never overlay, replace, or repair it with
unmanaged files, profile elements, PATH shims, manual registry edits, or direct
service mutations.
