# Lojix client ENOENT diagnosis

- Installed `lojix-meta` resolves to `lojix-7.0.0`; live `/run/lojix/meta.sock` listener is `lojix-nexus` 7.0.0.
- The checked source at the installed client revision `a67f5773` actualizes every Horizon deployment before `SocketExchange`: it calls `checked_path`, then `std::fs::read_to_string` on `proposal_source`; only afterwards does it open the owner socket.
- `SecretsDirectory` is carried as a string in that client path; it is not statted, opened, or copied before socket exchange.
- The cited Horizon artifact `/nix/store/p61bn3w1qgl3lhx5gm96crw1f1qlr0gg-horizon-definition/horizon-definition.datom` is absent.
- `/git/github.com/LiGoldragon/goldragon/secrets` is an existing directory owned by `li:users`.
- Therefore an `io error: No such file or directory` from this client is before server receipt and identifies the submitted Horizon proposal path (or an ancestor), not the owner socket or the secrets directory.
