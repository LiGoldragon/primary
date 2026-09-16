Read the preceding independent Cloudflare job workspace and its candidate changes. Perform a read-only audit only: verify fixture-only behavior and that no credential read, provider mutation, deployment, or shared-branch operation occurred. Record evidence and limitations; do not edit, commit, publish, or resume another agent.

Never use `signing.behavior=drop`, any signing override, approval bypass, or global/user configuration change. If a normal commit is blocked by signing, preserve the patch and test output, state signing-blocked, and do not work around it.
