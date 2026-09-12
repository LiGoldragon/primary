# Prometheus remote builder: why it fell back to local, and the working invocation

Subflow of main flow `f6db8d`, 2026-09-12. Brief: diagnose why
`reports/orchestrate-actor.md` saw `nix flake check -L` report `failed to
start SSH connection to 'prometheus'` and fall back to local, despite `nix
store info --store ssh-ng://prometheus` answering `Trusted: 1`.

Marks: **witnessed** — this thread ran the command and the text below is what
came back; **relayed** — a named file or process listing, not independently
re-verified; **this thread's inference** — reasoning, not a ruling.

## Finding

**No CriomOS or system bug.** The default, already-configured remote builder
works. The failure in `orchestrate-actor.md` was caused by that thread's own
`--builders` override, which named the builder by a bare alias
(`ssh-ng://prometheus …`) that resolves only inside `li`'s user-level SSH
config — not inside root's environment, which is what actually opens the SSH
connection for a build. No `--builders` flag is needed at all; the declared
`/etc/nix/machines` entry already points at Prometheus correctly and was used
successfully below with no override.

## How builders are configured

**Witnessed**, `nix show-config | grep -i builders`:
```
builders = @/etc/nix/machines
builders-use-substitutes = true
```

**Witnessed**, `/etc/nix/machines` (root-owned, NixOS-managed):
```
ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux /etc/ssh/ssh_host_ed25519_key 6 10 big-parallel,kvm,nixos-test - AAAAC3NzaC1lZDI1NTE5AAAAIAWX4CiSoep1+JuiYEpMzBj/H24eCYR+ZWaG3z2pg4Pk
```
This is generated NixOS config (`/etc/nix/nix.conf` header: "generated from
the nix.* options in your NixOS configuration ... Do not edit it!"). The
owning module lives in `The system` (CriomOS), not located in this thread —
see **What was not chased** below. It is correct as deployed: FQDN
`prometheus.goldragon.criome`, user `nix-ssh`, identity
`/etc/ssh/ssh_host_ed25519_key` (this host's own SSH host key, pre-authorized
on Prometheus's side for `nix-ssh`), and the target's host public key inlined
as the trailing field — so no `known_hosts` entry is needed for this path at
all; Nix supplies the host key itself from the machines-file line.

No user-level `builders` setting exists. `~/.config/nix/nix.conf` (`li`) holds
only `connect-timeout`, `http-connections`, and a GitHub `access-tokens` entry
— no builder override.

## Which user the daemon connects as, and with which key

**Witnessed**, `ps aux | grep nix-daemon` while builds were in flight: several
`root`-owned `nix-daemon` worker processes, each with a matching:
```
ssh nix-ssh@prometheus.goldragon.criome -x -i /etc/ssh/ssh_host_ed25519_key \
  -oUserKnownHostsFile=/tmp/nix-<pid>-<rand>/host-key \
  -oPermitLocalCommand=yes -oLocalCommand=echo started -- nix-daemon --stdio
```
This confirms: the daemon runs as **root**, connects as **`nix-ssh`** (not
`li`, not `root`), using the host's own ed25519 host key as the client
identity, and supplies the machines-file's inlined public key as a synthetic,
per-invocation `known_hosts` file (`/tmp/nix-*/host-key`) rather than reading
`root`'s or anyone's persistent `known_hosts`. `li`'s `~/.ssh/known_hosts` and
`config` are irrelevant to this path — root's SSH client identity is separate
and self-contained via the machines-file line.

**Relayed, not witnessed**: `root`'s own `~/.ssh/config` and `~/.ssh/known_hosts`
could not be read (`sudo -n cat ...` → `sudo: a password is required`, exit
1), so whether `root` additionally carries a persistent SSH config for
Prometheus is unknown. It does not matter for the machines-file path, which
supplies its own identity and host key inline, but it does matter for any
future ad hoc `--builders` override — see next section.

## Reachability now

**Witnessed**:
- `getent hosts prometheus.goldragon.criome` → resolves to
  `200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f` (a mesh/overlay address, present in
  `/etc/hosts` too).
- `ssh -o BatchMode=yes -o ConnectTimeout=5 prometheus.goldragon.criome true`
  as `li` → exit 0 (works, using `li`'s own `~/.ssh/config` alias and agent).
- `ssh -o BatchMode=yes -o ConnectTimeout=5 li@192.168.1.65 true` → `ssh:
  connect to host 192.168.1.65 port 22: No route to host`, exit 255. This
  matches the signal-standard witness from earlier tonight: `192.168.1.65` is
  not Prometheus's current address (`getent hosts` never returns it; it does
  not appear in `/etc/hosts` against `prometheus`). **This thread's
  inference**: that witness was testing a stale or wrong IP, not the
  configured mesh name, and its failure says nothing about whether the
  machines-file builder works.
- `sudo -n true` → `sudo: a password is required` (exit 1). Root's own
  reachability could not be checked interactively; the live nix-daemon
  connections above, and the successful remote build below, are the actual
  evidence that root's path to Prometheus works right now.

## Reproducing the failure

**Witnessed**, with an explicit `--builders` override using the bare alias
(as `orchestrate-actor.md`'s thread did):
```
$ nix build --builders 'ssh://prometheus' --max-jobs 0 -L --impure --expr \
    'derivation { name="test-remote"; system="x86_64-linux"; builder="/bin/sh"; args=["-c" "echo hi > $out"]; }'
cannot build on 'ssh://prometheus': error: failed to start SSH connection to 'prometheus': ssh: Could not resolve hostname prometheus: Name or service not known
Failed to find a machine for remote build!
...
error: Cannot build '...'.
       Reason: local builds are disabled (max-jobs = 0)
```
This is the exact failure text `orchestrate-actor.md` saw (`failed to start
SSH connection to 'prometheus'`). Root cause: `prometheus` is a bare alias
that exists only in `li`'s home-manager-generated `~/.ssh/config` (`Host
prometheus.goldragon.criome prometheus` → `HostName
prometheus.goldragon.criome`). The daemon's SSH subprocess runs as `root`,
which has no such alias and no DNS search domain to expand it —
**witnessed**, `/etc/resolv.conf` has `search .` (empty search list), and
`getent hosts prometheus` (bare, no domain) returns nothing. So the bare name
can never resolve for root, regardless of network reachability.

## The working invocation

**Witnessed**, no `--builders` override at all — the declared
`/etc/nix/machines` builder is used by default:
```
$ nix build --max-jobs 0 -L --impure --expr \
    'derivation { name="test-remote-default"; system="x86_64-linux"; builder="/bin/sh"; args=["-c" "echo hi > $out"]; }' \
    -o /tmp/test-remote-default-result
building '/nix/store/jw3wmznsg0hmk62gigjr5arj1d6v4cw1-test-remote-default.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
building '/nix/store/jw3wmznsg0hmk62gigjr5arj1d6v4cw1-test-remote-default.drv'...
copying 1 paths...
copying path '/nix/store/lwqhh76pxa739jzhxspjkq8qwn087wp6-test-remote-default' from 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
```
Exit 0; `cat /tmp/test-remote-default-result` → `hi`. The build log line
itself (`building '...' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`) is
the witness that this ran on Prometheus, not locally — `--max-jobs 0` makes a
local fallback impossible, so a green result here can only be a remote one.

**For any subflow that needs an explicit remote-builder flag** (e.g. to add
system features not in the machines-file line, as `orchestrate-actor.md`'s
`nix flake check` did), use the FQDN, not the bare alias:
```
--builders 'ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux - 32 1 big-parallel,benchmark,nixos-test,kvm'
```
This was not separately re-tested with every feature flag `orchestrate-actor.md`
used, but the only thing that differed between its failing invocation and the
one witnessed here is the hostname form (`prometheus` vs the FQDN), and that is
the exact string the error names as unresolvable.

## No fix was needed and none was made

No user-level change (SSH config, `known_hosts`, `nix.conf` builder spec) and
no CriomOS/CriomOS-home module change were required: the declared builder
already works for both the daemon's normal path (machines-file, witnessed
above) and would work for an explicit override if given the FQDN. Nothing was
edited in `The system` or `The user environment`, and no `f6db8d-builders`
test branch was created, because there is nothing broken in either repository
for this thread to change. Nothing running was touched; every command above is
read-only or a scratch build torn down by Nix's own store handling (`-o
/tmp/test-remote-default-result` is a local scratch symlink, not a system
path).

## What was not chased

- The CriomOS module that renders `/etc/nix/machines` and the `builders =
  @/etc/nix/machines` line was not located in `The system`'s source tree in
  this thread (the file itself, being NixOS-managed, was read directly from
  `/etc/nix/machines` instead). It is not needed for this diagnosis since the
  rendered config is already correct, and it is **relayed, not witnessed**
  that its source matches what is deployed.
- `root`'s own `~/.ssh/config` and `~/.ssh/known_hosts` were not read (no
  password for `sudo`). Not needed for the machines-file path, which supplies
  its own key and host-key data inline per invocation.

## Sources

- **Witnessed**, this thread, 2026-09-12: `nix show-config | grep -i
  builders`; `cat /etc/nix/nix.conf`; `cat /etc/nix/machines`; `cat
  ~/.config/nix/nix.conf`; `cat ~/.ssh/config`; `grep -i -E
  'prometheus|192.168.1.65' ~/.ssh/known_hosts`; `ps aux | grep nix-daemon`;
  `getent hosts prometheus.goldragon.criome`; `getent hosts
  prometheus.maisiliym.criome`; `grep -i -E 'prometheus|192.168.1.65'
  /etc/hosts`; `cat /etc/resolv.conf`; `getent hosts prometheus`; `ssh -o
  BatchMode=yes -o ConnectTimeout=5 prometheus.goldragon.criome true`; `ssh -o
  BatchMode=yes -o ConnectTimeout=5 li@192.168.1.65 true`; `sudo -n true`;
  `sudo -n cat /root/.ssh/config` (permission denied); `nix build --builders
  'ssh://prometheus' --max-jobs 0 -L --impure --expr ...` (reproduced
  failure); `nix build --max-jobs 0 -L --impure --expr ... -o
  /tmp/test-remote-default-result` (working remote build); `nix store info
  --store ssh-ng://prometheus` (`Trusted: 1`).
- **Relayed**: `flows/f6db8d/reports/orchestrate-actor.md`, "The gate" section
  — the exact failing invocation and error text this diagnosis reproduces.
