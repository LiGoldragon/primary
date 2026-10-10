# Proposal and source

Method: probe `stat` and non-symlink status for
`/git/github.com/LiGoldragon/goldragon/datom.dotos`; read the Zeus node record
in that source; read `SKILL_VARIABLES.md`; and inspect current Lojix
`ProposalFile`, routing, and source-policy code.

Observed:

- The proposal is an existing absolute regular non-symlink `.dotos` file.
- Its Zeus record declares an `Edge` host on `x86_64`, while the current
  `goldragon` source revision is `be4bf4d63d15f5e591bb5d7bfdf06d9ed019d38c`.
- This workspace's configured deployment transport variables name Ouranos,
  not Zeus. Lojix validates and uses the request-supplied Nix store URI and
  SSH destination verbatim; it does not derive a route from cluster/node
  names.
- Lojix admits only an absolute regular non-symlink `.dotos` proposal that
  parses as a cluster proposal; routing, output selector, activation backend,
  and source-revision policy are validated before admission.

Unknown: the exact immutable CriomOS revision, output selector, Zeus transport,
builder, requested host action, and resulting Horizon/evaluation closure have
not been supplied or evaluated for this preflight.
