# Zeus update shape

## Observations

The declared target is `goldragon/zeus`, an Edge/Max x86_64 ThinkPad T14 Gen2
Intel with no node services. Current CriomOS source owns the target system,
CriomOS-home supplies its Home Manager modules, and Lojix projects the
proposal into Horizon, system, deployment, and secrets inputs. The checked-in
source and its pinned inputs were read, but no current Zeus generation or
deployment record exists in the Ouranos Lojix view.

Zeus resolves through the local Yggdrasil route, but ICMP, TCP/22, and strict
noninteractive SSH probes timed out. Retained Zeus generated-input trees are
historical materialized output, not proof of the current target. No proposal,
evaluation, build, copy, activation, reboot, or runtime mutation occurred.

## Inference

The update boundary is an owner-only inline typed `meta-lojix` `Deploy.Host`
request. Its positional shape carries the cluster and node, host composition,
proposal source, immutable flake reference, explicit Nix-store/SSH transport,
input mode, output selector, NixOS activation backend and action, source
revision policy, optional builder, and extra substituters. Lojix then
materializes the proposal, evaluates and realizes the selected closure, copies
it to the explicit target store, performs the requested action, and records a
terminal result that must be checked with an ordinary query. Admission alone
does not prove completion.

The currently observed CriomOS revision is a possible immutable source
candidate, not an instruction to deploy it. A live switch, persistent boot
profile change, or one-shot boot scheduling would be a separate activation
mutation.

## Unknowns and authority gates

The exact Zeus transport pair, immutable source revision, output selector,
optional builder, extra substituters, and activation action are not established
by current variables or Zeus live records. Zeus target-side generations,
profiles, services, boot state, free space, cache/signing keys, activation
journal, and any safe rollback target remain unknown because the host was not
reachable. These values require caller supply or approval before any proposal
or deployment; this explanation-only request does not authorize mutation.

## Sources

- [written-psyche acquisition](./zeusPsyche.md)
- [Zeus update path subflow](../../d098fa2d/reports/zeusUpdatePath.md)
- [Zeus live preflight subflow](../../3cb84d07/reports/zeusLivePreflight.md)
