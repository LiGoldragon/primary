# lojix-daemon installed-path Zeús deploy validation — 2026-06-15

## Result

The three system-maintainer Beads from the system-operator handoff are closed:

- `primary-bplu` — package and install the lojix daemon stack first.
- `primary-4jtb` — smoke the installed service and socket contract.
- `primary-3eu2` — validate Zeús deploy through the installed daemon.

The validation used the installed `/run/current-system/sw/bin/*` binaries and the installed `lojix-daemon.service`; it did not use `target/debug` for final validation.

## Source changes landed

`lojix` now has a Nix flake package/check surface:

- `packages.default` builds the shipped `lojix-daemon`, `lojix`, `meta-lojix`, and `lojix-write-configuration` binaries with `nota-text` enabled for the human-facing clients.
- `packages.daemon-binary` separately builds the daemon binary without the `nota-text` feature for daemon-boundary pressure.
- `checks.daemon-startup-rejects-nota` proves the daemon rejects inline NOTA startup and requires a signal/rkyv startup file.

`CriomOS` now consumes `github:LiGoldragon/lojix` and installs `lojix-daemon.service` on `PersonaDevelopment` nodes. The service:

- runs as local operator user `li`, because `meta-lojix` owner-socket authorization requires the peer uid/gid to match the daemon uid/gid;
- generates `/run/lojix/startup.rkyv` with installed `lojix-write-configuration`;
- starts installed `lojix-daemon` with exactly that rkyv startup argument;
- exposes `/run/lojix/ordinary.sock` and `/run/lojix/owner.sock`;
- stores durable state under `/var/lib/lojix`.

`CriomOS-home` now pins the interactive Rust toolchain to exact Rust `1.96.0` instead of `stable.latest`, avoiding the moving rust-overlay channel hash failure seen during FullOS evaluation.

Commits:

- `lojix` `214acf53` — add Nix package surface.
- `CriomOS` `a45fc524` — install lojix daemon on operator hosts.
- `CriomOS` `74924fde` — update CriomOS rust-overlay pin.
- `CriomOS` `18e6ed95` — align CriomOS-home rust-overlay input to the top-level pin.
- `CriomOS-home` `ce31cc21` — pin Home Rust toolchain version.
- `CriomOS` `57561a41` — pin CriomOS-home exact Rust toolchain.

## Installed local deployment

Ouranos FullOS was deployed through the production deploy path from pushed `CriomOS/main`.

A remote-builder Eval with `builder = prometheus` initially failed before evaluation completed because the moving rust-overlay channel fixed-output hash had drifted. After the exact Home Rust toolchain pin, local Ouranos deployment used `builder = None` because Ouranos was the target host and no cross-host signed copy was needed.

Results:

- Ouranos FullOS Eval: success.
- Ouranos FullOS Build: success.
- Ouranos FullOS Switch: success.

Post-switch installed state:

- `lojix-daemon.service`: active.
- `lojix-daemon`, `lojix`, `meta-lojix`, `lojix-write-configuration`: present in `/run/current-system/sw/bin`.
- `/run/lojix/ordinary.sock`: mode `0660`, owner `li:users`.
- `/run/lojix/owner.sock`: mode `0600`, owner `li:users`.
- `/run/lojix/startup.rkyv`: mode `0600`, owner `li:users`.
- `/var/lib/lojix`: mode `0750`, owner `li:users`.

## Installed service/socket smoke

Smoke checks through the installed service:

- Ordinary query through installed `lojix` succeeded: `(Queried ([] (0 0)))` before deploy validation.
- A separate temporary startup with owner socket mode `0666` was rejected by installed `lojix-daemon` with `InsecureOwnerSocketMode`-class text.
- Installed `meta-lojix` Eval for Zeús through `/run/lojix/owner.sock` succeeded: `(Deployed (1 (0 0)))`.

## Zeús installed-daemon deploy validation

The final validation used installed `meta-lojix` talking to installed `lojix-daemon.service` on Ouranos.

Requests targeted:

- cluster: `goldragon`
- node: `zeus`
- deploy kind: `FullOs`
- proposal: `/git/github.com/LiGoldragon/goldragon/datom.nota`
- flake: `github:LiGoldragon/CriomOS/main`
- builder: `prometheus`

Results:

- Eval: `(Deployed (1 (0 0)))`
- Build: `(Deployed (1 (2 2)))`
- Boot: `(Deployed (1 (4 4)))`

After Boot, root SSH to `zeus.goldragon.criome` showed both `/nix/var/nix/profiles/system` and `/run/current-system` resolving to the same Zeús system profile path, and `bootctl status` showed the default boot entry matching that generation. No direct `bird@zeus` SSH was used.

## Caveat / follow-up

The post-test ordinary query required by the handoff was captured:

```text
(Queried ([] (6 6)))
```

That means the installed daemon advanced its database marker through the deploy pipeline, but the ordinary generation listing was empty for `ByNode (goldragon zeus None)`. The Zeús host-level boot profile did update/verify successfully, so the deploy path itself reached the target. The empty live-set listing should be treated as a lojix state/query follow-up: either the query shape does not expose the Boot-pending generation as expected, or the activation pipeline records phase markers without projecting the live generation into ordinary query results.
