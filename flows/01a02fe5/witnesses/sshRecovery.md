# SSH recovery witness

Method: direct probes of the OpenSSH client and GPG SSH agent; `systemctl`,
`ss`, and `journalctl` reads of local `sshd`; strict `BatchMode` SSH probes;
source reads of CriomOS-home and goldragon cluster data; and ordinary/owner
Lojix requests.

Observed before repair:

- `sshd.service` was active and listening on TCP port 22; localhost reached
  public-key authentication but was denied.
- `SSH_AUTH_SOCK` pointed at the expected GPG SSH socket, but `ssh-add -l`
  and `ssh-add -L` reported zero identities. There were no local `id_*`
  private-key files.
- The only `sshcontrol` keygrip agreed with GPG agent configuration but had
  no matching locally listed secret-key keygrip. It was not the cluster
  declaration for `li` on the running `ouranos` node.
- The source-declared `ouranos` keygrip did match a locally available,
  authentication-capable secret key; its public SSH fingerprint matched the
  local `li` authorization and the cluster's current-node public key.
- Strict, key-only probes of localhost, Prometheus aliases, Ouranos, and both
  Zeus routes all failed at authentication. This established a shared client
  identity failure rather than independently offline targets.

Authorized reversible bootstrap:

- Preserved the original managed `sshcontrol` symlink and its one-line
  content under `~/.gnupg/sshcontrol.ssh-recovery-01a02fe5.*`.
- Temporarily selected only the source-declared, locally available Ouranos
  keygrip and ran the supported narrow `gpgconf --reload gpg-agent` reload.
- OpenSSH then exposed one ED25519 identity and every strict probe succeeded.

Declarative convergence:

- Owner request 51 was admitted but failed before activation at
  `CopyClosure/BuilderUnreachable` while the identity remained unavailable.
- After bootstrap, owner request 52 completed successfully and became the
  current Ouranos user-environment generation.
- The temporary control file was verified byte-for-byte equal to generation
  52's managed control file, then replaced with a symlink to that managed
  file. The recovery copies remain retained.

Final strict key-only `BatchMode` probes with `StrictHostKeyChecking=yes`
exited zero for: `localhost`, `prometheus`,
`prometheus.goldragon.criome`, `li@ouranos`, `root@192.168.18.95`,
`root@zeus.goldragon.criome`, and `root@ouranos.goldragon.criome`.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/users.nix`
- `/git/github.com/LiGoldragon/goldragon/datom.dotos`
- `flows/01a01bac/witnesses/userEnvironmentDeployment.md`
- `flows/01a02b6a/reports/zeusRequestInputs.md`
- direct local SSH/GPG/systemd/Lojix probes in flow `01a02fe5`
