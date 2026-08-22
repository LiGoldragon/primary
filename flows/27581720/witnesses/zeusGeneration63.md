# Zeus generation 63 source observability

Method: probe over strict noninteractive SSH with
`timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=8 -o ConnectionAttempts=1
-o StrictHostKeyChecking=yes -o LogLevel=ERROR
root@zeus.goldragon.criome`, running `nixos-version`, `nixos-version --json`,
`readlink -f /run/current-system`, `readlink -f
/nix/var/nix/profiles/system`, and `nix-env --list-generations --profile
/nix/var/nix/profiles/system`.

Observed:

- `nixos-version` reports `26.05.20260422.0726a0e (Yarara)`.
- `nixos-version --json` reports only
  `nixosVersion=26.05.20260422.0726a0e` and
  `nixpkgsRevision=0726a0ecb6d4e08f6adced58726b95db924cef57`.
- `/run/current-system` and the system profile both resolve to
  `/nix/store/6mjh02yv45nh0r0nr7gyd9rakrv79xdv-nixos-system-zeus-26.05.20260422.0726a0e`.
- The system profile lists generations 60, 61, 62, and 63; generation 63 is
  current (2026-08-09 16:21:29).

Inference: generation 63 is directly witnessed as the active NixOS profile,
and its NixOS/nixpkgs identity is known. The target's observable version JSON
contains no `configurationRevision`, CriomOS commit, CriomOS-home pin, or Lojix
pin. Therefore generation 63 cannot be matched to the public candidate
`d04f6dafce19b7b4f093c35716739f36d75973ba` from this probe.

Unknown: whether generation 63 was evaluated from the candidate, an older
CriomOS commit, or another source shape; whether any target-side daemon has a
separate source record; and whether its Home Manager outputs correspond to the
candidate's pinned home revision.
