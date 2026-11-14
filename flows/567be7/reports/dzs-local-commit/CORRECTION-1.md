# Correction 1 — owner rejection occurs after both spawns

This append-only correction supersedes one lifecycle description in the immutable local candidate evidence. It changes no candidate byte, commit, ref, prior report, or prior manifest.

## Correct source fact

In candidate commit `e6528df680e5a79de202b34e9b5ec3f6c5cac67e`, `run`:

1. successfully spawns the Nexus child;
2. successfully spawns the translator child;
3. places both children in the `PairedChildren` owner; and only then
4. validates `deployment.owner` against the launching login.

An owner mismatch is therefore a **post-spawn cleanup path with both children owned**. Returning the owner-validation error drops `PairedChildren`, which attempts termination and blocking reap of both owned children.

## Withdrawn wording

The following phrases are wrong and are withdrawn:

- immutable commit message `e6528df...`: “pre-spawn owner rejection”;
- `dzs-local-commit/REPORT.md`: “owner rejection, which is a pre-spawn path”;
- earlier `dzs-candidate-test-guard/child-process-test-inventory.md`: “owner rejection (no child reached)”.

Read each as: **owner rejection after both successful spawns exercises the paired owner’s cleanup path**.

The immutable commit message remains unchanged by order. This correction governs its evidence interpretation. No code, ref, build, test, publication, deployment, or bead state changed.
