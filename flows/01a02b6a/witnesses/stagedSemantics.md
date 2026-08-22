# Zeus staged deployment semantics

Method: code read `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`
and `/git/github.com/LiGoldragon/lojix/src/lib.rs`.

Observed:

- `DeployAction::produces_closure` is false only for host `Evaluate`; host
  `Realize`, `TestActivation`, and `ActivateNow` all evaluate and realize a
  closure.
- `DeployAction::activates` is true for host `TestActivation` and
  `ActivateNow`, and false for host `Evaluate` and `Realize`.
- `Evaluate` finishes after `nix eval` with the derivation path; it does not
  run a build, closure copy, or activation.
- `Realize` finishes after remote `nix build`; it does not copy or activate.
- `TestActivation` and `ActivateNow` build, copy the exact closure using the
  request transport, then run target activation. Test uses
  `switch-to-configuration test`; ActivateNow uses `switch`.
- `record_deploy_submitted` calls the durable allocator. Each accepted request
  receives a new deployment identifier and generation identifier. There is no
  request field that links a later stage to a prior stage's closure.
- A later identical request may reuse the already-realized Nix store path or a
  configured substitute, but that is Nix store/cache reuse, not Lojix deployment
  identity reuse. The staged requests remain separate durable deployments.

## Sources

- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:1125-1158` — action closure/copy/activation predicates
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:3470-3528` — effect continuation behavior
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:3779-3815` — per-request durable admission
- `/git/github.com/LiGoldragon/lojix/src/lib.rs:1498-1565` — fresh deployment/generation allocation
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:5320-5355` — host activation command mapping
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:5630-5645` — user/host activation behavior
- `flows/01a02b6a` — this flow
