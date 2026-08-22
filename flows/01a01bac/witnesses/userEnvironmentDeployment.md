# UserEnvironment deployment

Method: probe `lojix 'Query.ByNode.(goldragon ouranos Some.UserEnvironment)'`

Observed: UserEnvironment deployment 27 reached terminal Succeeded from marker
`(588 588)` to `(621 621)`. It is Current at CriomOS revision
`d04f6dafce19b7b4f093c35716739f36d75973ba` with artifact
`/nix/store/rlija745aqpq5p5dkf3s7082g42x1i4x-home-manager-generation`.

Method: probe `ssh li@ouranos 'readlink -f /home/li/.local/state/nix/profiles/home-manager'`

Observed: the target Home Manager profile resolves to
`/nix/store/rlija745aqpq5p5dkf3s7082g42x1i4x-home-manager-generation`.
