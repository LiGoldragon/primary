# Codex servers: stable and next are Nix variables

The living, his words: "My idea was that next and stable were just internal variable names in the Nix code. I wasn't saying that we should change the service derivation in any way. Essentially there should be no effect from the point of view of the running service: there would be nothing visible in terms of whether it's stable or next."

## Now (CriomOS-home, modules/home/profiles/min/)
- codex-remote-control.nix: service codex-remote-control, 0.153, home ~/.codex. No client. Being removed on his order.
- codex-next.nix: service codex-remote-control-next, 0.158, home ~/.codex-next. The `codex` command on PATH uses it. Carries an undeclared drop-in, override.conf (KillMode=process, Restart=no).
- codex-next-candidate.nix: service codex-remote-control-next-8mkkxq293hk2, 0.161.0-alpha.2, home ~/.codex-next-8mkkxq293hk2. Every Codex flow uses it.

The role, and for the candidate a build hash, is written into the service name, the home directory and the socket path.

## Proposed
1. Each running Codex server has a neutral, fixed service name, home and socket, which never carry stable, next, a version or a hash.
2. In Nix, `stable` and `next` are variables that name which server definition plays that role. Changing which one is stable is an edit of those variables. It changes no service, home, socket or derivation, so the running servers see nothing.
3. The PATH `codex` command and the Flow Nexus's Codex launch read the socket and home through the `stable` variable.
4. The undeclared override on the 0.158 server is traced to what added it. If KillMode=process is what keeps Codex threads alive across a unit stop, it is declared in Nix on the servers.

## What it costs once
- Renaming the current names to neutral ones is a one-time change. It means one announced stop of the flows' server (0.161), with no Codex flow mid-turn. Its home ~/.codex-next-8mkkxq293hk2 moves as a whole to the neutral home, so its threads, auth.json and sqlite come with it.
- In the same commit, every consumer changes: the Flow Nexus configuration's Codex socket and home, the PATH wrapper, and the checks bird-codex-selection, bird-home-isolation and gates/codex-remote-control-vm.

## Open
- After the 0.153 removal, whether the 0.158 server is kept as a second server or retired once PATH `codex` reads `stable`. The proposal works either way.
