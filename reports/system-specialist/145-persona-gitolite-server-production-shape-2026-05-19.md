# Persona Gitolite Server Production Shape

Date: 2026-05-19  
Role: system-specialist  
Status: corrected report; supersedes the stale boolean-role report

## Correction

The previous version of this report is superseded. It described the
Persona development gate as a plain boolean:

```json
{ "personaDevelopment": true }
```

That was an intermediate shape and is no longer the production
architecture. The current production shape is variant-first:

```nota
(PersonaDevelopment [(GitoliteServer)])
```

This matters because the cluster data should carry meaningful role
selection, not positional booleans or implementation records. The
cluster owner selects that this node hosts Persona development
infrastructure and, within that role, that it hosts the Gitolite
receive surface. CriomOS owns how that capability is implemented.

## Boundary

The cluster data may say:

```nota
[
  (PersonaDevelopment [(GitoliteServer)])
]
```

The cluster data must not say:

```nota
(Workstation (RepositoryReceiveRole true))
```

and must not carry:

- Gitolite data directories
- hook paths
- socket paths
- SSH command wiring
- daemon implementation names
- ports or domain names

`GitoliteServer` is acceptable cluster data because it is a semantic
capability selection. It names the role a node should play. It does not
configure the Gitolite implementation.

## Current Production Flow

`goldragon/datom.nota` selects the role on `ouranos`:

```nota
(PersonaDevelopment [(GitoliteServer)])
```

`horizon-rs` models this as:

```rust
NodeService::PersonaDevelopment {
    capabilities: Vec<PersonaDevelopmentCapability>,
}

PersonaDevelopmentCapability::GitoliteServer {}
```

The projected Horizon JSON carries the service vector through to
CriomOS as externally tagged variants. `CriomOS` consumes that vector
through:

```text
modules/nixos/node-services.nix
```

The repository receive module gates Gitolite on:

```nix
nodeServices.personaDevelopmentHas (horizon.node.services or [ ]) "GitoliteServer"
```

When present, `modules/nixos/repository-receive.nix` enables:

- `services.gitolite.enable = true`
- `services.gitolite.dataDir = "/var/lib/gitolite"`
- `services.gitolite.adminPubkey` from `horizon.node.adminSshPubKeys`
- a Gitolite `post-receive` hook
- tmpfiles entries for `/var/lib/repository-ledger` and its spool

## Hook Behavior

The current hook is a durable spool witness, not the final repository
ledger daemon integration.

On Git receive, the hook writes a Nota record:

```nota
(RepositoryReceiveHookNotification ...)
```

into:

```text
/var/lib/repository-ledger/spool
```

The record includes repository name, Gitolite user, receive timestamp,
ref updates, and whether the expected repository ledger daemon socket
exists. It does not yet deliver an actor message to a daemon.

This is the right early production behavior: Git receive should not
block on a daemon that may be absent or evolving. The hook records an
event durably and exits successfully.

## Tests

The production stack has tests for the shape at three layers:

- `horizon-rs` decodes `[(PersonaDevelopment [(GitoliteServer)])]` as
  the nested capability vector.
- `horizon-rs` projects Persona development roles from proposal data,
  not from node names.
- `CriomOS` `repository-receive-role-policy` verifies that Gitolite is
  disabled with no service variants and enabled only when
  `PersonaDevelopment` contains `GitoliteServer`.

The CriomOS check also verifies:

- the configured Gitolite data directory
- that the admin key comes from projected Horizon data
- that test fixtures do not smuggle a real-looking SSH key
- that the post-receive hook contains the repository ledger spool path
- that tmpfiles creates the spool directory

## Deployed State

The production service-variant stack has been deployed to `ouranos`
through a `FullOs Switch` pinned to `CriomOS` `fcf6f09a`.

The current deployed generation includes the Gitolite receive module
through the `PersonaDevelopment [(GitoliteServer)]` role selection on
`ouranos`.

## What Is Still Missing

The current implementation is not the complete Persona repository
receive architecture.

Missing or still provisional:

- A real repository ledger daemon consuming the spool or socket.
- A typed signal contract for repository receive events.
- A clear ownership decision for whether repository-ledger paths stay
  local to the module or move into `CriomOS-lib` once reused.
- End-to-end tests that perform an actual Git push through Gitolite and
  assert the resulting ledger event.
- Authorization rules for who may create or mutate repositories.

The implemented slice is still valuable: it establishes the correct
Horizon boundary, enables Gitolite from a semantic role selection, and
records receive events durably without adding cluster-specific
implementation data to the proposal.

## Rule To Keep

Persona infrastructure in cluster data should be a vector of role
variants and nested capability variants. CriomOS turns those variants
into concrete services.

Do not regress to:

- booleans whose meaning is only known by position
- node-name predicates
- cluster-authored ports or paths
- Horizon records that merely mirror CriomOS module options
