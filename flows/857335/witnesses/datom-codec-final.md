# Datom codec final witness

Method: ran `cargo test --test core`, `cargo clippy --all-targets -- -D warnings`,
and `nix flake check -L` in `/git/github.com/LiGoldragon/datom-codec` after
pinning Protos `1bf659e5489cf1ac05cc293ee2e8068774fb48bd`.

Observation: all 10 core tests passed locally. The remote Nix gate built on
`prometheus.goldragon.criome` and passed build, test, generated contract,
documentation, formatting, clippy, and policy checks.
