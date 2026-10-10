# CriomOS forge pins

Method: probe `gh api repos/LiGoldragon/CriomOS`, `gh api
repos/LiGoldragon/CriomOS/git/ref/heads/main`, the corresponding repository
metadata/ref endpoints for `CriomOS-home`, `lojix`, and `goldragon`, immutable
commit endpoints for each pinned revision, and `gh api
'repos/LiGoldragon/CriomOS/contents/flake.lock?ref=d04f6dafce19b7b4f093c35716739f36d75973ba'`
with JSON/base64 decoding and `jq`.

Observed from the public forge on 2026-08-22:

- `LiGoldragon/CriomOS` is public, non-archived, defaults to `main`, and
  `refs/heads/main` points exactly to
  `d04f6dafce19b7b4f093c35716739f36d75973ba`.
- The CriomOS commit is publicly addressable and is titled `flake: update
  CriomOS-home input`. Its `flake.lock` is public at that immutable revision
  (content SHA `18160f993c8652093944aeceec293da0faed1af4`).
- The `criomos-home` lock node has both `original.rev` and `locked.rev`
  `1a6e22da155bb75a6362d10623301b13d0c24b34`, owner `LiGoldragon`, repo
  `CriomOS-home`, type `github`, and narHash
  `sha256-RDdAjNlnAw7kBsh+aoatYYU2mP/RoiGr+J3NXNpCdfw=`.
- The `lojix` lock node has both `original.rev` and `locked.rev`
  `0d968da44bc0be8ed875b8546bebf52c3de53a81`, owner `LiGoldragon`, repo
  `lojix`, type `github`, and narHash
  `sha256-gMVIWbjQdCy2nMvDwSv7jnDFzkon5OpU7Px13IwQUcY=`.
- Public `CriomOS-home/main` is exactly
  `1a6e22da155bb75a6362d10623301b13d0c24b34`; public `lojix/main` is exactly
  `0d968da44bc0be8ed875b8546bebf52c3de53a81`. Each immutable commit endpoint
  returned successfully.
- Public `goldragon/main` is
  `be4bf4d63d15f5e591bb5d7bfdf06d9ed019d38c`; its public `datom.dotos` at that
  revision exists (content SHA `e0fac23293ce8b64ebd091550b16d16baf680fa8`).
  This is proposal-source evidence, not a claim that Lojix has used that
  revision.

Inference: the candidate producer chain is pushed, public, and represented by
immutable GitHub owner/repository/revision references with content hashes. The
lock entries are portable references rather than local checkout paths or
branch-only inputs. This does not prove every transitive input, cache route, or
target-side deployment state.
