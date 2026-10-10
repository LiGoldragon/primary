# Home Flow 0.17.3 stage validation

- **Stage:** `fccc26523589c9b40cd1aa1479e63c571fa4c061`; Flow-next `0b512ee0b6681b1925fee7b6435aa7c2eac26bfb`, Messenger `93c12756f9c00dd3c13762590f17cee3a3712530`, Message-next `481b579fcf72797ffa9ccf8ce4e2283a58cdff97`.
- **OS inputs:** Ouranos complete-host system and horizon, both `lastModified=1790465761`; system nar hash `sha256-KW3DUTifDJ6m2JuYiTVtJz+9ieAgqjCb46wgrMqxJJU=` and horizon nar hash `sha256-+2TlZvji1dU4IL89k1CpsC+7kpVtD1M37Zgsw2CKG10=`.
- **Full evaluation:** bounded `nix flake check --no-build --keep-going --impure --no-write-lock-file`, local builders only, max-jobs/cores 2, cache.nixos.org only, completed with `all checks passed!`; it evaluated `flow-message-next` to drv `28c0x4j91pyv528jgq37qd5ci69aqhz2`.
- **Dedicated realization:** one bounded local build of that check produced valid `/nix/store/msqnddfrxzfrg48yaw32cjdivp5lvlq4-flow-message-next`. Its Nix log records `Configured.{...}` and all four next client probes. The terminal wrapper did not return a numeric exit code, so this receipt does not claim one.
- **Coordination:** one HM notice each: Astra `Presented.{ 6fe957 done }`, Fable `Presented.{ 8904b1 done }`, Field Sol `Presented.{ 9ac67c idle }`. Presentation is transport evidence only.
- **Boundary:** no Home main move, activation, or Zeus deployment was performed by this validation.
