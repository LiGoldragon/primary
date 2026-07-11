Blocked by mandatory remote-test scheduling; no local fallback was used.

- Production services remain inactive; backup/marker untouched; no provider call, deployment, or activation.
- New `spiritJudgePinChain` Nix output passed remotely with `max-jobs=0`.
- Deployment lock corrected to pin Spirit `f9f5266a`.
- Required remote rebuild of Home CLI-contract test failed because Nix selected no remote builder when local slots were disabled. Deployment integration remains committed locally but unpushed.