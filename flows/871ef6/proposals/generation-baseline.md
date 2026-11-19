# Messenger core generation baseline — approval requested

No generation or gate is authorized or running. Orchestrate 455 holds both
repositories. Flow releases retain builder priority.

## Published source

- messenger-nexus, research/d69736:
  f0be766da8758eb1b4e2267ac9709dfe694f2690.
- messenger-nexus-tests, research/d69736:
  0beeeb5b5c9475514cf36a5359429aeea88136b2.
- The test manifest pins that published core. Both remote branch tips were
  read back with git ls-remote and matched these revisions.
- Opus exis confirms the retained explicit Open opener and configured
  room-level Communicator. Twelve operation tests are authored, none run.

## Baseline authority gap

Neither source repository has an accepted flake.lock or Cargo.lock. The
handover identifies 7fca4d583adfd2354903c59cbc7f5e928e1baa76 only as a
historical build-base registry anchor. No accepted Messenger toolchain/base
cohort has been found. That anchor is a candidate for approval, not a grant.
The working build-base HEAD was inspected but is not selected.

## Static candidate inventory

At build-base 7fca4d583adfd2354903c59cbc7f5e928e1baa76:

- flow-ethos 0.54.0 is registered at
  5c61d66648a17a218147f3ec11dd995847c8303d, matching both manifests.
- datom-codec 0.33.1 is registered at
  09a0526949b043f921b6d3ce115b7f455291f2e2. The core and Flow write
  rev-string 09a0526, so Cargo retains one source identity.
- Flow build-depends on ethos-zero 22.0.0, rev-string 1976e45, registered
  revision 1976e45fe1edfd5676cb33919dba1ec20c785a02.
- Its protos 0.33.0 uses rev-string c93b598, registered revision
  c93b598025984f8a73e70aa18b8e8a6fdfdfdfd8.
- Registry rkyv 0.8.18 and tokio 1.53.1 match manifest lower bounds.
- The base lock pins nixpkgs 0e251e24a4f24e036a084b6b4b2d2491af4167f4
  and fenix f7d416b5073152c7f2e4de1a28d1a4330dd30a26.
- Its crate2nix is 0.15.0 with the base's git-hash-by-rev patch.
- Registry-file SHA256s: versions
  0411cd33543e995367f40be4cc3826590b5271dfc51a18f983b8e269c2dc4f89;
  features 83ed70ad8456dba4771f74fe9d6c990cf81b2f8b2efdde32af4140932e033eb5.

## Mismatches requiring coordinated approval

The separate test repository introduces messenger-core 0.1.0 as a git crate;
the candidate base does not register it. The candidate tokio union attaches
more dependencies than the test manifest's macros/rt/io-util resolution;
generation must inventory the missing edges before a gate can be proposed.
The core flake's ethos-zero input has no lock. Its previously used compiler
is 30.1.0, store /nix/store/dfz5drcy3c2afy5558ccr03iz3998zzr-rust_ethos-zero-30.1.0-bin,
but that version is absent from this candidate's git registry. Registered
30.0.1 (2999292dc67c8608e54d32c333c550b29153cbff) is a possible generator
baseline; identical output and compatible toolchain are not yet proved.

## Publication audit limitation

The required whole-history secret check was performed after publication,
which missed the prescribed order. A local, non-compiling regex audit of
all reachable historical blobs found zero matches in 34 core and 8 test
blobs for private keys, GitHub/Matrix/AWS token forms, quoted credential
assignments and credential-bearing HTTP URLs. It is a bounded heuristic
check, not a comprehensive secret-scanner result. Evidence:
/tmp/messenger-871ef6.yNgfbi/history-secret-audit.json.

## Requested decision and next boundary

Approve an explicit base/compiler cohort, or name its existing accepted
lock. Name the coordinator for the new messenger-core registry entry and
any required tokio attachment edges. After that approval, I will submit
one exact metadata-only generation command, pinned tools and input-change
allowlist, 600-second limit, one job/two cores, private workspace, no Rust
compilation, and owned cleanup evidence. Generation outputs are reviewed
before source commits and a separately granted immutable whole-check gate.
