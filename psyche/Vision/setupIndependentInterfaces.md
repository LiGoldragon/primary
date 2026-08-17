## 2026-08-14 — no setup-specific scripts in general repos

> I don't want setup-specific scripts in general repos. Everything must be setup-independent with simple clear interfaces that agents can easily adapt to their needs.

Context: ouranos-activate.sh in LojixOsOnlyActivation bundles setup-specific deployment logic. The psyche rules this pattern out — deployment interfaces must be setup-independent.

## 2026-08-14 — the interface is lojix and meta-lojix CLI only

> Seems like letting agents "fix" it ended up abandoning my vision. The interface is lojix and meta-lojix CLI only.

Context: ouranos-activate.sh was an agent-created workaround that bundled deployment into a setup-specific script, bypassing the designed CLI interface. The psyche rules that all deployment goes through lojix and meta-lojix CLI — no parallel scripts.

## 2026-08-14 — CLIs cannot accept any argument other than the typed input object

> An agent broke the invariant. Get rid of the flag and expose the option through nota/dotos. Remove any and all flags from lojix, replace them all. CLIs cannot accept any other type of argument than the typed input object. I feel like I keep repeating myself.

Context: `--override-input horizon <path>` was being passed as a flag. The psyche rules that all input goes through the typed DOTOS/NOTA object — no flags on any component CLI. This invariant belongs in the rust-component-architecture skill.

## 2026-08-16 — sshcontrol keygrip comes from cluster data

> That should be set using cluster data in criomos-home.

Context: the GPG keygrip in ~/.gnupg/sshcontrol was missing from the new home-manager generation. The psyche rules it should come from the horizon/cluster data in CriomOS-home, not be hardcoded or manually managed.

## 2026-08-17 — lunar nixpkgs update pattern

> Update on the first commit exactly after the new moon every lunation.

Context: nixpkgs pin updates follow the lunar cycle — the first commit on the nixpkgs repo after each new moon becomes the pin for that lunation.
