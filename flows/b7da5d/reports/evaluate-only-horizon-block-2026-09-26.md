# Evaluate-only Horizon input regeneration: stopped

Field's subflow remotely verified goldragon revision `ddf27e0c28bfdd98bf36dcb580ab51abc2c6c40b` and built its `horizon-definition` output with remote-only Nix settings. The resulting source was the canonical regular file `/nix/store/6i5v50mhq6ljhi9s6vr1fbfmrvgz6w53-horizon-definition/horizon-definition.datom`.

The **live Lojix 7 client** rejected the first Ouranos Evaluate-only packet before creating a deployment: `CliRejected [Datom request did not decode: proposal source is not a Horizon definition]`. This is a compatibility/encoding gate, not a remote-builder failure. No Prometheus Evaluate, Realize, TestActivation, ActivateNow, main move, or cleanup was submitted by this worker. The source was not silently substituted or retried.

After this observation, e167d8 relayed b860be's ownership transfer: new Mind Astra owns step-2 gates and main moves. Field deploys only after b860be reports step-2 main green. Prometheus boot-once is additionally held until the living names its time. The above blocker is passed as evidence to that owner; it does not authorize a Field source fix or a new deployment.
