# Stage-one 13s1 source implementation

## Immutable candidate

- Base: `544e63ca762fb8d9d7f882fabb8aeb60dfd7bde2`.
- Branch: `flow-1541ef-stage1-13s1`.
- Commit: `865b835cbd09e06c2857a254b21b7065bafdaccb`.
- Remote ref resolves to that exact commit.
- Worktree: `/git/worktrees/flow-1541ef-stage1-13s1`, clean after push.

## Source shape

`flake.nix` and `flake.lock` add one non-flake source input, `deployed-codex-source`, using the bare repository URL and locking Home revision `0b430341a594f1b1ee31e986c4dbd0d537e6ffe7` with its recorded NAR hash. No pre-existing input changed.

`modules/home/core-packages.nix` adds universal `codexServer` and `codexNextServer` package-set attributes. They rebuild the stable and next server packages from that pinned source in the consumer's package set. `codex-remote-control.nix` and `codex-next.nix` consume those selections for every user; no username branch exists. The next preparation is generated from the unchanged module body, so li retains `zxxd...` while each user's home remains correct.

`herdr.nix` rebuilds the stable Flow client from the pinned source's `stable-hashes.json`; the advanced `corePackages.codex` remains the PATH client. The exact deployed package universe reproduces client `1qc...`, leaving the Flow daemon's compiled default client unchanged.

`checks/bird-codex-selection/default.nix` independently injects distinct PATH, stable-server, and next-server selections and asserts both users receive the same server selections. `gates/codex-remote-control/default.nix` judges the server selection and completes its user fixtures with the already-required empty capability fact.

No owned version declaration, Codex next declaration, Flow input, harness input, main, consumer, profile, unit, or live runtime state changed.

## Reproduction and narrow builder proof

On `prometheus.goldragon.criome`, pinned Home `0b430...` evaluated in the deployed CriomOS package universe (`LiGoldragon/nixpkgs` `f4a03c...`) reproduced and built the exact occupied artifacts:

- `/nix/store/4p67nm261bqy549q2isd4ifydqrfqy48-codex-0.167.1`
- `/nix/store/g2sfx3dccpi3294i1p70vafpaa84jfb8-codex-next-0.158.0-alpha.9`
- `/nix/store/1qc6p7vncfd2vc5g74m3r0p0i7vjvzhg-codex-stable-flow-client`
- `/nix/store/zxxdr7rajm50pk46yk86qb6jaxxl3j69-codex-next-prepare`

The universal-selection check built as `/nix/store/9gs6kx62h1yq5s1f7r79y1y18f7c3jlx-bird-codex-matched-selection`. The stable remote-control gate built as `/nix/store/6pj5mmprl6g7f061s7v6xiz9gphc4h97-codex-remote-control-contract`.

Evidence logs are in `/home/li/primary/flows/1541ef/stage1-source-evidence/`.

## Held boundary

The exact consumer's three unit derivation/text comparisons, Flow daemon `fs53...` comparison, and full gate remain the next proof step under `/home/li/primary/flows/1541ef/proof-contract.md`. Both mains and every materialization, activation, replay, restart, profile switch, and publication remain held.
