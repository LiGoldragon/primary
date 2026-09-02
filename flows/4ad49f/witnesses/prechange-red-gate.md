# Immutable pre-change desktop-app-support red gate

Method: ran the immutable Home check in one foreground `exec` session, first
with a short yield to obtain the session ID, then polled that exact session
until it returned `exit_code`. The run used the materialized Ouranos
user-environment `system` and `horizon` inputs and the configured
`/etc/nix/machines` remote builder. After the gate returned, I read the
immutable derivation's `buildCommand` and performed read-only `cmp` and hash
diagnostics against its independently fetched vendor archive. No product or
system source, deployment, runtime, GUI, or service state was changed.

Exact gate command:

```sh
nix build --refresh --no-link --print-build-logs --option max-jobs 0 --option fallback false --builders '@/etc/nix/machines' --override-input system /var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system --override-input horizon /var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/horizon 'github:LiGoldragon/CriomOS-home/af7c67746dda#checks.x86_64-linux.desktop-app-support'
```

Exit code: `1`.

Smallest gate excerpt:

```text
building '/nix/store/q1r2dz946cvvwqh426yz7pyfb6jlgg17-desktop-app-support-contract.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
Reason: builder failed with exit code 1.
```

The immutable derivation's first `set -eu` contract assertion is an exact
`cmp -s` between the independently fetched vendor
`usr/lib/chatgpt/resources/app.asar` and the packaged
`chatgpt-unwrapped-26.831.21537/lib/chatgpt/resources/app.asar`. A direct
read-only reproduction returned `ASAR_cmp_exit=1`; both files are
292435829 bytes, with vendor SHA-256
`9745ec1195897c019533d08e8415ab81a3c4e59e845403fdfea42ce1272fe954` and
packaged SHA-256
`5fe72e5ab9c58dc9d786c41e0928a7a0a46adde5f39b8d962a8677466173f84e`.
The subsequent bundled `resources/codex` exact comparison also returned `1`
(vendor regular file versus packaged symbolic link). Thus the nonzero result
is the intended stock ASAR/resource contract red, not unrelated
infrastructure.

## Sources

- Immutable Nix gate command and terminal output from the foreground session
  on 2026-09-02.
- `nix derivation show /nix/store/q1r2dz946cvvwqh426yz7pyfb6jlgg17-desktop-app-support-contract.drv`
  (read-only build-command inspection).
- Read-only extraction of the derivation's pinned vendor archive and `cmp`,
  `sha256sum`, and `stat` diagnostics against the packaged output.
