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

## 2026-08-17T17:34:10.507+02:00 — local user deployment does not loop through root SSH

> youre already user li, thats just adding ssh overhead to go in a complete circle right back to where you started. not that its a grave mistake, but its useless churn.

Context: an agent proposed deploying the local `li` user environment by connecting over SSH to the same host as root and then switching back to `li`. The psyche identified the route as circular overhead for a deployment whose target user is already the local caller.

## 2026-08-19T10:49:57+02:00 — same-host SSH should be improved, not rejected

> I didnt reject it, thats quackery. so there is no problem there. it should be improved but I didnt reject it.

Context: Source provenance is the current user's turn in local `/home/li/.codex/history.jsonl`, epoch `1787129397`, flow short-id `01a01450`. This corrects the agent's claim that the psyche rejected the available same-host SSH route: the route was not rejected, though it should be improved. This is a Vision entry, not Intent.
