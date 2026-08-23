# SSH recovery report

## Result

SSH was restored for localhost and every configured remote endpoint tested.
The active `sshcontrol` now points to the current Home Manager generation's
managed file, which selects the source-declared Ouranos identity. Lojix user
environment deployment 52 completed successfully and is current.

## Observation

The local SSH server was healthy: it was running, listened on port 22, and
had recently accepted public-key sessions. The client reached authentication
on every endpoint but offered no identity. Its managed `sshcontrol` referenced
a keygrip belonging to another cluster-node identity and not to a local secret
key.

The declarative home source selects `user.pubKeys.${node.name}.keygrip`. For
the actual hostname `ouranos`, that selected key was locally available and
already part of the projected authorization set. The declarative source was
therefore correct; the live managed home state had drifted to a different
node's control entry.

## Repair

The first normal Lojix home activation could not copy its closure because the
same missing SSH identity blocked the remote-builder/copy path. Under explicit
recovery authority, the original `sshcontrol` symlink and content were kept
recoverably, and a temporary one-line control file selected only the declared
Ouranos key. Reloading GPG agent through `gpgconf --reload gpg-agent` made the
already-authorized key visible to OpenSSH.

That bootstrap restored strict SSH access, allowing the same typed Lojix user
environment activation to complete. Generation 52 is current. Its managed
control file was verified to contain the same entry, and the live path was
reattached to it. The recovery copies are intentionally retained for now.

## Unknowns

The direct evidence does not establish how the live managed `sshcontrol`
drifted to the other node's entry. The completed generation proves the source
and active deployment now agree; it does not by itself identify the prior
activation or projection event that caused the divergence.

## Coordination

At the final artifact write, both coordination binaries existed. The
current-form `meta-orchestrate` registration parsed but failed because its
socket was absent; ordinary `orchestrate` had the same transport failure.
Claims are advisory, so the requested isolated flow paths were written without
a claim. No commit was made, as directed.

## Sources

- `flows/01a02fe5/witnesses/sshRecovery.md`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/users.nix`
- `/git/github.com/LiGoldragon/goldragon/datom.dotos`
- `flows/01a01bac/witnesses/userEnvironmentDeployment.md`
- `flows/01a02b6a/reports/zeusRequestInputs.md`
