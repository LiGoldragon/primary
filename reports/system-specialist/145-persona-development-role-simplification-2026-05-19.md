# Persona Development Role Simplification

Date: 2026-05-19  
Role: system-specialist  
Status: correction after user review

## Correction

The first repository receive slice over-modeled the Horizon field as:

```nota
(Workstation (RepositoryReceiveRole true))
```

That was wrong for the production Horizon boundary. The only cluster fact
needed here is whether the node is a Persona development node. The specific
services implied by that role belong to CriomOS and the later component
implementation, not to a nested cluster-data capability tree.

The corrected production shape is now:

```nota
(NodeServices Client (Server 8443 "tailnet.goldragon.criome") true)
```

Projected JSON:

```json
{
  "personaDevelopment": true
}
```

CriomOS gates the local Gitolite receive module on that boolean.

## Commits

- `horizon-rs` `49a969c3` — replaces `Option<PersonaDevelopmentRole>` with
  `persona_development: bool`.
- `goldragon` `474734de` — changes `ouranos` to the boolean field and all
  other nodes to `false`.
- `lojix-cli` `70e1bcc5` — repins `horizon-lib` to the simplified schema.
- `CriomOS` `8ba7c296` — gates repository receive on the boolean field.
- `CriomOS-home` `67bd8177` — repins `lojix-cli`.
- `CriomOS` `bb31eb30` — repins `CriomOS-home`.

## Validation

Passed:

- `CARGO_BUILD_JOBS=2 cargo test -p horizon-lib`
- `CARGO_BUILD_JOBS=2 cargo test` in `lojix-cli`
- CriomOS repository receive Nix witness
- projected `goldragon/ouranos` and confirmed
  `horizon.node.services.personaDevelopment == true`
- full CriomOS module evaluation confirms `services.gitolite.enable == true`
  for projected `ouranos`

## Lesson

Do not make Horizon carry nested implementation detail when a single semantic
role bit is the actual cluster fact. Horizon should say "this node is for
Persona development"; CriomOS decides which development services that implies.

