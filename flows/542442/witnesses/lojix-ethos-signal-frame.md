# Generated Datom Signal-frame witness

The ordinary and privileged Lojix producers landed on main at
`signal-lojix@5ce3f11feac22a0ddbed028dec2a60385f77fa55` and
`meta-signal-lojix@55c1df20ddfa6ae99e0f4bca57b803bf366b781f`. Their checked-in
generated Datom Rust is verified during builds without regenerating source in a
dependency build; stale generated text fails the producer build. The ordinary
producer is pinned by the meta producer, and both are pinned by frozen Lojix
`d4404aad0d9418e29ebbbc8042c1684276bb3dcd`.

Each producer decodes the generated typed request, performs a structural rkyv
conversion, and carries it only in a `BoundExchangeFrame`. Frame validation
checks the contract binding, wire revision, and route before typed recovery.
Malformed archives and foreign binding/revision/route are rejected. This is not
a raw rkyv socket protocol.

The owner deployment contract carries `SecretsInput` directly with the typed
request. It is either `NoSecrets` or a caller-owned directory authority;
Horizon’s public `horizon-definition.datom` never carries secret contents or a
secret path. The Lojix adapter regression exercises the generated owner
`DeployRequest::Host` with `NoSecrets`, proves a structural bound-frame round
trip, and preserves strict typed conversion for non-string fields.

Remote producer/package gates and the frozen Lojix consumer package gate passed.
The behavior-complete consumer was
`d4404aad0d9418e29ebbbc8042c1684276bb3dcd`; final Lojix main
`59293764e02e0fb0ec9251f382e627787420f30d` is its documentation-only child.
It corrects the retained-v4 operator instructions without changing a producer,
generated contract, frame, or package input.

## Recovered version from unlanded commit 5245222d8067 (2026-09-06 12:33 UTC)

#\1 Generated Datom Signal-frame witness

The ordinary and privileged Lojix producers landed on main at
`signal-lojix@5ce3f11feac22a0ddbed028dec2a60385f77fa55` and
`meta-signal-lojix@55c1df20ddfa6ae99e0f4bca57b803bf366b781f`. Their checked-in
generated Datom Rust is verified during builds without regenerating source in a
dependency build; stale generated text fails the producer build. The ordinary
producer is pinned by the meta producer, and both are pinned by frozen Lojix
`d4404aad0d9418e29ebbbc8042c1684276bb3dcd`.

Each producer decodes the generated typed request, performs a structural rkyv
conversion, and carries it only in a `BoundExchangeFrame`. Frame validation
checks the contract binding, wire revision, and route before typed recovery.
Malformed archives and foreign binding/revision/route are rejected. This is not
a raw rkyv socket protocol.

The owner deployment contract carries `SecretsInput` directly with the typed
request. It is either `NoSecrets` or a caller-owned directory authority;
Horizon’s public `horizon-definition.datom` never carries secret contents or a
secret path. The Lojix adapter regression exercises the generated owner
`DeployRequest::Host` with `NoSecrets`, proves a structural bound-frame round
trip, and preserves strict typed conversion for non-string fields.

Remote producer/package gates and the frozen Lojix consumer package gate passed.
The behavior-complete consumer was
`d4404aad0d9418e29ebbbc8042c1684276bb3dcd`; `59293764e02e0fb0ec9251f382e627787420f30d`
is its documentation-only child. Final Lojix main
`7e29c37f51092e5a20abf88c670aabd2acee6e52` normally merges that child with
the retained legacy rollback `46585a2c8303bffe885b1722bfebd97d5353ca17`.
Both `59293764` and `7e29c37f` have root tree ID
`15e217d8a2b96625d7bb89d9d94b7b44479ef36a`; the exact tree diff is empty.
The merge changes no producer, generated contract, frame, package input, or
runtime behavior.
