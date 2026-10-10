# Remembered UserEnvironment deployment procedure

Remembered flow: `01a02fe5` at depth 1.  This is the proper user-level
activation procedure recovered from its Lojix deployment records and the
successful immutable Home deployment witness.  It is a procedure record,
not an authorization to activate.

## Exact target and request

The intended logical target is `(goldragon ouranos li)`: cluster `goldragon`,
node `ouranos`, user `li`.  The physical copy and activation endpoint must be
proved independently and must resolve to Ouranos; the historical failure
installed a Zeus logical profile on Ouranos because Lojix accepted a mismatched
logical node and transport.  Use the explicit transport
`(ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome)`, direct
unprivileged SSH as `li`, and an exact endpoint-identity/host-key check before
submission.  Do not substitute Zeus, localhost, a controller, or a builder.

First evaluate the exact materialized target and its Horizon inputs, then do a
remote-only realization/build through the configured Prometheus builder (local
jobs disabled and no fallback) as proof.  Do not use a moving flake reference.
The current Home revision is:

`github:LiGoldragon/CriomOS-home?rev=f05a3639de72e4976c5ba87a932a39dc2f9ccf1c`

The owner submission shape, with that current revision substituted for the
historical revision, is:

```text
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.dotos github:LiGoldragon/CriomOS-home?rev=f05a3639de72e4976c5ba87a932a39dc2f9ccf1c (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

The positional fields are, in order: cluster, node, user, absolute proposal
source, immutable flake reference, `(Nix store URI, SSH destination)`
transport, input mode, output selector, activation backend, user-environment
action, source revision policy, optional builder, and extra substituters.
`Evaluate` is evaluation only; `Realize` evaluates and builds remotely but
does not copy or activate; `ActivateNow` builds, copies, and activates.  A
safer staged run is `Realize` followed by an explicitly authorized
`ActivateNow`, retaining the same immutable source and endpoint proof.

Submit only through the owner socket and typed `meta-lojix`; do not use
setup-specific scripts or an ad-hoc `home-manager switch`.  Admission
(`DeployAccepted`) is not completion.  Query the ordinary socket until a
terminal record, for example:

```text
lojix 'Query.ByNode.(goldragon ouranos Some.UserEnvironment)'
```

The accepted deployment must reach `Completed` with `Some.Succeeded`.  Keep
the Lojix ledger result separate from observations of the live target because
activation can fail after changing persistent links.

## Inputs, identity, and secrets

The proposal must be an absolute regular file and not an accidental symlink.
Lojix-generated materialized `system`, `horizon`, `deployment`, and `secrets`
trees are authoritative; do not fabricate, derive, or reuse an unspecified
input tree.  `Horizon` is the input mode and
`homeConfigurations.li.activationPackage` is the output.  The Home target is
the existing declarative profile, not a new secret or a manually assembled
package closure.

SSH/GPG material comes only from the source-declared
`user.pubKeys.${node.name}.keygrip`.  Never print private keys, secret values,
or generated secret trees in a report or chat.  If the agent has no identities,
the recovery established by `01a02fe5` is the only safe pattern: preserve the
managed `~/.gnupg/sshcontrol`, temporarily select the source-declared keygrip,
run the supported `gpgconf --reload gpg-agent`, prove strict BatchMode routes,
then declaratively converge and reattach the managed symlink.  Do not invent a
key or silently replace managed secret state.

Before admission, prove that the endpoint whose profile will change is
Ouranos: strict host-key material and hostname/route identity, SSH as `li`,
and the expected Lojix store destination must all agree.  This topology proof
is mandatory even when the controller or builder is elsewhere.

## Activation verification

After the terminal Lojix result, use strict BatchMode SSH to
`li@ouranos.goldragon.criome` and verify the Home Manager profile points at the
new generation/artifact, for example by resolving both
`~/.local/state/nix/profiles/home-manager` and `~/.nix-profile` as applicable.
Then verify the requested application surface on the target:

```text
codex --version
claude --version
readlink -f ~/.nix-profile/bin/codex
readlink -f ~/.nix-profile/bin/claude
```

Also inspect the medium-or-larger graphical projection, desktop entries and
processes, the `codex-remote-control` and Agent Intercom user services, and the
app-server socket where that integration is expected.  The current source
puts Claude Desktop behind `AgentIntercomGraphical && size.medium` and uses
one shared Codex derivation; the target projection must be checked rather than
assumed.

## Safety and rollback

Do not retry, hot-fix, manually activate, reboot, garbage-collect, or reset
after a failed copy or activation without an explicit new ruling.  A failed
Lojix request may have partially copied a closure or advanced persistent/live
links; inspect the target profile, runtime links, and activation journal and
record both the ledger state and live observations.  Preserve the prior Home
Manager generation.  Any rollback is an explicitly authorized declarative
Lojix/Home Manager operation, never an improvised `home-manager switch`.

## Relation to the current Home plan

There is no architectural conflict with Home commit `f05a3639de72` or
CriomOS pin `e1008e20abad`: both expose the expected immutable
`homeConfigurations.li.activationPackage`, retain the medium/graphical gate,
and use the shared Codex derivation while adding Claude Desktop.  A live
UserEnvironment activation is nevertheless a separate state change and still
needs the endpoint/topology proof and explicit authority above.  Current
`goldragon` data describes Ouranos as `Large` with
`AgentIntercomGraphical`, and user `li` as `Max`, so the profile should qualify;
the projected Horizon result must be the final check.  Claude Desktop's
embedded Code runtime remains unobservable through the supported package
interface, so deployment must not claim exact embedded-runtime parity.

No deployment was submitted or activated while recovering this procedure.
