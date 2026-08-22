# Lojix deployment

Method: probe `lojix 'Query.ByNode.(goldragon ouranos None)'`

Observed: the controller reports CompleteHost generation 7 as Current while
its historical deployment 16 terminal record is Failed at Activate. It also
reports deployment 16's immutable source revision.

Method: probe `ssh root@ouranos.goldragon.criome 'readlink -f /nix/var/nix/profiles/system; readlink -f /run/current-system'`

Observed: both target links resolve to the same `jngjk328r5nd3xvkjw9wppb02ghm0jir`
NixOS closure. This directly confirms a live target closure distinct from the
controller's reported Current generation.

Method: probe `lojix 'Query.ByDeployment.16'`

Observed: the ordinary client rejects the request with `expected z2VLsn to be
a parenthesis block`. The historical unknown ByDeployment frame error is not
reproduced by this probe; its cause remains unknown.
