# Tailnet feasibility witness

- `headscale`: `/run/current-system/sw/bin/headscale`, version 0.29.3.
- `sops`: `/home/li/.nix-profile/bin/sops`, version 3.13.3.
- `gopass`: `/home/li/.nix-profile/bin/gopass`, version 1.16.1.
- `ssh-to-age`: `/home/li/.nix-profile/bin/ssh-to-age`.
- `openssl`: absent from current PATH.
- `sudo -n headscale version` and `sudo -n headscale preauthkeys create --help`: `sudo: a password is required`.
- Passwordless localhost root SSH ran `headscale version` and `headscale preauthkeys create --help`; CLI supports `--user`, `--reusable`, `--expiration`, `--force`, and output formats.
- Ouranos public host key derives `age15k8h8e60x9qj558xms2wnc77akupprzsy6k4sg6zvrnk5h7tmgkqz57zf0`.
- No proposed `headscaleTls*.sops` or `tailnet*.sops` files exist in checked-out `repos/goldragon/secrets`; no matching runtime contract exists in checked-out CriomOS modules.
- `gopass cat --help` states it can encode stdin into a named secret and decode a named binary secret to stdout. `sops encrypt --help` confirms the report's `--age`, `--input-type`, `--output-type`, and stdin-required `--filename-override` options.
