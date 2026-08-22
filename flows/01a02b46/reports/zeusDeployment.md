# Zeus deployment outcome

The requested immutable Zeus CompleteHost update did not activate. Evaluation
and realization succeeded, while TestActivation deployment 30 terminated at
the closure-copy stage with `BuilderUnreachable`. No live activation, boot
profile change, reboot, or separate Home Manager deployment occurred.

The target remains on its prior NixOS generation 63 in the persistent profile,
current runtime link, booted runtime link, and systemd-boot default/current
entry. SSH remained active, no failed systemd units appeared, and the activation
journal had no matching entries. The pre-existing absent `mpd.service` and
D-Bus duplicate-name messages remained. Bird and li's existing Home Manager
profiles were unchanged.

Lojix's durable state separates the successful earlier stages from the failed
test: deployment 28 Evaluate succeeded, deployment 29 Realize succeeded, and
deployment 30 TestActivation failed at `CopyClosure BuilderUnreachable`.
The attempted transfer did consume Nix-store space; the candidate system store
path was not present after failure. No retry is appropriate without an explicit
new ruling because the test had a partial copy failure.

## Sources

- [Zeus deployment witness](../witnesses/zeusDeployment.md)
- [Zeus update written-psyche record](../vision/zeusUpdate.md)
- [Lojix operating contract](../../../../.agents/skills/lojix/SKILL.md)
- [Zeus request inputs](../../01a02b6a/reports/zeusRequestInputs.md)
