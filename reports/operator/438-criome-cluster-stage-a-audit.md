# 438 — criome cluster Stage A audit and main-port status

## Verdict

Designer's Stage A claim is real: the `criome-cluster-1of1` NixOS VM test
boots a guest, starts a real `criome-daemon` systemd service from one binary
startup argument, and runs a witness over the daemon socket that proves both
authorization outcomes with real BLS material:

```text
authorized head -> Authorized
threshold-short head -> Rejected(QuorumShort{required:1, satisfied:0})
```

I independently ran the designer branch's VM check before integration:

```sh
nix build --builders '' --no-link --print-out-paths --log-format bar-with-logs .#checks.x86_64-linux.criome-cluster-1of1
```

It passed and produced:

```text
/nix/store/w4dr55dsldhnkv4shia6m7zkymwvbsml-vm-test-run-criome-cluster-1of1
```

This proves the criome half of the local spirit gate in a real sandbox. It does
not yet prove the full spirit -> criome -> router -> mirror propagation loop.

## What I Ported

I landed the reusable criome package half on `criome` main:

```text
criome main 1eaa783 — criome: land cluster witness test package
```

Changes:

- `cluster-witness` Cargo feature.
- `criome-write-configuration` deploy/build encoder for the rkyv daemon startup
  message.
- `criome-cluster-witness-test`, a test-only witness binary that:
  - mints real BLS key material,
  - registers the signer and timekeeper identities,
  - admits a 1-of-1 contract,
  - evaluates an authorized head as `Authorized`,
  - evaluates threshold-short evidence as rejected.
- `flake.nix` package `cluster-witness`.

I renamed the witness binary from designer's `criome-cluster-witness` to
`criome-cluster-witness-test`, because test-only binaries use the `-test`
suffix.

Verification on `criome` main:

```sh
cargo fmt --check
cargo test --features cluster-witness --bins
cargo test --features cluster-witness --lib
cargo clippy --features cluster-witness --all-targets -- -D warnings
nix build --builders '' --no-link --print-out-paths --log-format bar-with-logs \
  github:LiGoldragon/criome/1eaa78306ac23b63176e0ad5d75001ab617615e5#cluster-witness
```

The remote Nix build passed and produced:

```text
/nix/store/r35n88l6yw9khyknwpjf7481ps1qp23a-criome-0.1.1
```

That remote package installs:

- `criome-daemon`
- `criome-write-configuration`
- `criome-cluster-witness-test`

## What I Could Not Port Yet

I did not modify `CriomOS-test-cluster` main because `cloud-operator` currently
claims that repo for a pan-cluster domain configuration update, and the
canonical checkout is dirty with that lane's changes.

The unmerged designer branch is:

```text
CriomOS-test-cluster origin/criome-cluster-test 8247b293
```

It adds the reusable `mkCriomeClusterTest` NixOS test generator and the
`criome-cluster-1of1` check. It is structurally good, but now needs one small
main-port adjustment because the criome witness binary was renamed during
operator integration.

Required follow-up once the `CriomOS-test-cluster` lock clears:

```nix
criome.url = "github:LiGoldragon/criome/main";
```

and in `lib/mkCriomeClusterTest.nix`:

```nix
${machineName}.succeed("CRIOME_SOCKET=${socketPath} ${criomePackage}/bin/criome-cluster-witness-test")
```

Then build the check from the pushed remote, not by using a local `path:` flake
override.

## What Went Wrong

The main issue was coordination, not a fake green:

- The designer proof was valid but split across two feature branches.
- The criome branch could be ported immediately and is now on main.
- The harness branch depends on `CriomOS-test-cluster`, which another lane has
  locked and dirty.
- The harness branch still points at the feature-branch criome input and the
  pre-operator binary name, so it should not be merged blind.

The earlier "Spirit is down" note in designer report 704 is resolved in the
live environment: the `spirit` CLI responds, and the v10-store problem was a
stale systemd unit drift rather than data loss.

## Next

After `cloud-operator` releases `CriomOS-test-cluster`, integrate the harness
branch with the two mechanical edits above, push main, then run:

```sh
nix build --builders '' --no-link --print-out-paths --log-format bar-with-logs \
  github:LiGoldragon/CriomOS-test-cluster/<new-main-rev>#checks.x86_64-linux.criome-cluster-1of1
```

Stage B remains separate: wire `spirit` daemon configuration so the criome gate
can be armed from the meta-signal path and mint per-head evidence, then add the
spirit/mirror legs to the NixOS VM test.
