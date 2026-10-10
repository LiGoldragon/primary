# Comments on "The meta harness has a base"

## Proposal 1 — the base, in vision-flow

**Anchored text:** The meta harness is the tooling that st…

**Comment (2026-10-10T15:55):**

The umbrella component, or the root component for the meta harness, is persona. This would go in the persona vision. I guess persona should have everything it needs in the environment. We're assuming an installation of CreoleOS for now, which is fine. It would need credentials, which obviously we can't just include. These would be deployed from an encrypted deployment through Nix, I guess: Sops, Nix, through the cluster data, ostensibly.
