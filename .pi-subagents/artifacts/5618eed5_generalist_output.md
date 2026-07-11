Not SOURCE READY. Stopped after the required Nix validation failures; no retries started.

- Production services remain inactive; backup/marker untouched; no provider call or activation.
- `spirit-judge` witness producer is pushed: `c2303a30ff88fea527a8075b22f1d598a80fdb80`.
- Home consumer is pushed: `3391ee776da7c0d2d09b0609a58177009e1236b0`.
- Deployment integration is staged atop current `43d9234f`, with Nix-generated Home/witness lock updates and runbook changes, but is uncommitted pending valid deployment-chain validation.
- Deployment root `nix flake check` requires Lojix materialization because its default `system` input is intentionally a stub. The first Nix pin assertion also used a nonexistent top-level `signal-spirit-judge` lock node.