# Stage 1 read-only tool inventory

Actor: Field browser Sol, flow 12b000. Authorization: Field core osuf. Tool executables were not invoked except the explicitly permitted shell/SSH/Python inventory machinery. No provisioning, mount, compiler/analyzer/version probe, browser action, or credential read.

## Ouranos

```text
ouranos
lspmux: ABSENT
rust-analyzer: /home/li/.nix-profile/bin/rust-analyzer
resolved: /nix/store/y3rnww8pqan19nddqc595kg7h775k3s5-rust-analyzer/bin/rust-analyzer
Text wrapper (bounded to 120 lines / 16 KiB):
#!/nix/store/hasnvc0j36gg6qrdsfcx7yivx3c2bpqr-bash-5.3p20/bin/bash
printf '%s\n' 'rust-analyzer: local compilation is disabled; use the repository Nix package/check selector on the configured remote builder. Use rustfmt for explicit formatting.' >&2
exit 126

cargo: /home/li/.nix-profile/bin/cargo
resolved: /nix/store/garzi81pb89lv8byh1zfsmsmss28ci71-cargo/bin/cargo
Text wrapper (bounded to 120 lines / 16 KiB):
#!/nix/store/hasnvc0j36gg6qrdsfcx7yivx3c2bpqr-bash-5.3p20/bin/bash
printf '%s\n' 'cargo: local compilation is disabled; use the repository Nix package/check selector on the configured remote builder. Use rustfmt for explicit formatting.' >&2
exit 126

rustc: /home/li/.nix-profile/bin/rustc
resolved: /nix/store/2np2jbdnkwhqcxsgkxa4cnlp9f68sqhq-rustc/bin/rustc
Text wrapper (bounded to 120 lines / 16 KiB):
#!/nix/store/hasnvc0j36gg6qrdsfcx7yivx3c2bpqr-bash-5.3p20/bin/bash
printf '%s\n' 'rustc: local compilation is disabled; use the repository Nix package/check selector on the configured remote builder. Use rustfmt for explicit formatting.' >&2
exit 126

nix: /run/current-system/sw/bin/nix
resolved: /nix/store/slbva5divbfvd1ns260ff6ppil8gg0b2-nix-2.35.3/bin/nix
Not a shebang text wrapper; executable not invoked.
python3: /home/li/.nix-profile/bin/python3
resolved: /nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14
Not a shebang text wrapper; executable not invoked.
ast-grep: /home/li/.nix-profile/bin/ast-grep
resolved: /nix/store/na8f7hyy8dfvh6cznymm88ngbrxb72lh-ast-grep-0.51.0/bin/ast-grep
Not a shebang text wrapper; executable not invoked.
sshfs: /home/li/.nix-profile/bin/sshfs
resolved: /nix/store/bmdfcbbfshlrs5rc34nqsa0v9yylrs0g-sshfs-fuse-3.7.6/bin/sshfs
Text wrapper (bounded to 120 lines / 16 KiB):
#! /nix/store/hasnvc0j36gg6qrdsfcx7yivx3c2bpqr-bash-5.3p20/bin/bash -e
PATH=${PATH:+':'$PATH':'}
PATH=${PATH/':''/nix/store/5wyaj1kvkxbbscz6innrh6yjjkdq4qmk-openssh-10.6p1/bin'':'/':'}
PATH='/nix/store/5wyaj1kvkxbbscz6innrh6yjjkdq4qmk-openssh-10.6p1/bin'$PATH
PATH=${PATH#':'}
PATH=${PATH%':'}
export PATH
exec -a "$0" "/nix/store/bmdfcbbfshlrs5rc34nqsa0v9yylrs0g-sshfs-fuse-3.7.6/bin/.sshfs-wrapped"  "$@" 
fusermount3: /run/wrappers/bin/fusermount3
resolved: /run/wrappers/wrappers.jCi4tZAn86/fusermount3
ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux /etc/ssh/ssh_host_ed25519_key 8 10 big-parallel,kvm,nixos-test - AAAAC3NzaC1lZDI1NTE5AAAAIAWX4CiSoep1+JuiYEpMzBj/H24eCYR+ZWaG3z2pg4Pk
crw-rw-rw- 1 root root 10, 229 Nov 11 13:20 /dev/fuse

```

## Prometheus

```text
prometheus
lspmux: ABSENT
rust-analyzer: /home/li/.nix-profile/bin/rust-analyzer
resolved: /nix/store/m1x8nj6nyim711lm0sv9s8w6a6xvmsc4-rust-analyzer/bin/rust-analyzer
Text wrapper (bounded to 120 lines / 16 KiB):
#!/nix/store/byi2zpy2bgcf3dr6y0l8m50rmjj8z7q1-bash-5.3p15/bin/bash
printf '%s\n' 'rust-analyzer: local compilation is disabled; use the repository Nix package/check selector on the configured remote builder. Use rustfmt for explicit formatting.' >&2
exit 126

cargo: /home/li/.nix-profile/bin/cargo
resolved: /nix/store/f395yg5fsyr0b76aig6q637qipblan9y-cargo/bin/cargo
Text wrapper (bounded to 120 lines / 16 KiB):
#!/nix/store/byi2zpy2bgcf3dr6y0l8m50rmjj8z7q1-bash-5.3p15/bin/bash
printf '%s\n' 'cargo: local compilation is disabled; use the repository Nix package/check selector on the configured remote builder. Use rustfmt for explicit formatting.' >&2
exit 126

rustc: /home/li/.nix-profile/bin/rustc
resolved: /nix/store/48l2adhg3vhadfgfnk5pbf2srw1cxmc5-rustc/bin/rustc
Text wrapper (bounded to 120 lines / 16 KiB):
#!/nix/store/byi2zpy2bgcf3dr6y0l8m50rmjj8z7q1-bash-5.3p15/bin/bash
printf '%s\n' 'rustc: local compilation is disabled; use the repository Nix package/check selector on the configured remote builder. Use rustfmt for explicit formatting.' >&2
exit 126

nix: /run/current-system/sw/bin/nix
resolved: /nix/store/slbva5divbfvd1ns260ff6ppil8gg0b2-nix-2.35.3/bin/nix
Not a shebang text wrapper; executable not invoked.
python3: /home/li/.nix-profile/bin/python3
resolved: /nix/store/0r6k8xa2kgqyp3r4v2w7yrb80ma2iawm-python3-3.13.12/bin/python3.13
Not a shebang text wrapper; executable not invoked.
ast-grep: /home/li/.nix-profile/bin/ast-grep
resolved: /nix/store/1g1pd0k42v7k6knx7k92fdfp45hd6n1d-ast-grep-0.42.1/bin/ast-grep
Not a shebang text wrapper; executable not invoked.
sshfs: /home/li/.nix-profile/bin/sshfs
resolved: /nix/store/rji8p3ylpxkzrsfq5bknrcbmg7nnycff-sshfs-fuse-3.7.5/bin/sshfs
Text wrapper (bounded to 120 lines / 16 KiB):
#! /nix/store/i27rhb3nr65rkrwz36bchkwmav6ggsmn-bash-5.3p9/bin/bash -e
PATH=${PATH:+':'$PATH':'}
PATH=${PATH/':''/nix/store/lj9iikldz29gc7nizgn4xh30cw33xvdl-openssh-10.3p1/bin'':'/':'}
PATH='/nix/store/lj9iikldz29gc7nizgn4xh30cw33xvdl-openssh-10.3p1/bin'$PATH
PATH=${PATH#':'}
PATH=${PATH%':'}
export PATH
exec -a "$0" "/nix/store/rji8p3ylpxkzrsfq5bknrcbmg7nnycff-sshfs-fuse-3.7.5/bin/.sshfs-wrapped"  "$@" 
fusermount3: /run/current-system/sw/bin/fusermount3
resolved: /nix/store/wvxq13lcabjmz3zcqvv19i343b1sabxg-fuse-3.18.2-bin/bin/fusermount3
Not a shebang text wrapper; executable not invoked.
crw-rw-rw- 1 root root 10, 229 Nov 13 16:28 /dev/fuse

```

## Gaps

No already-retained compatible vendor/toolchain artifact pointer was supplied: UNKNOWN. No store-wide or filesystem-wide search was made. Stage 2 allocation and exceptions remain separate.

Guard conclusion: both hosts expose unconditional exit-126 cargo/rustc/rust-analyzer wrappers; even version/probe calls are refused. Temporary Nix builds follow the stated repository Nix remote-builder route but are not authorized by this inventory; manual analyzers or observational compiler probes need a separate explicit exception/approved guarded executable. No bypass was attempted. Ouranos fusermount3 resolves but its wrapper file was not readable as the normal user.
