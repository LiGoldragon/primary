# Zeus resume capacity

The bounded capacity assessment cannot establish a current reusable-byte or reusable-path count. The realized candidate `jz6mg0qlm3w2h2h5jxwldccncjgcz22j-nixos-system-zeus-26.11.20260813.0e251e2` is no longer valid in the expected local store, so its exact recursive closure cannot be enumerated for a remote `ssh-ng` validity comparison. The remote batch query consequently has no rows; that does not prove that Zeus has no valid dependencies from the failed copy.

The only available size witness is earlier same-flow metadata: 3,579 recursive paths and a coarse human-readable NAR closure size of 34.5 GiB while the candidate was locally present. The exact byte total, current source closure, destination-valid path count, destination-valid byte total, and missing byte total are unknown. The parent flow's approximately 13 GiB free-space loss and 1.93 GB transfer counter cannot be classified as reusable store data without path-level registration evidence.

Nix/Lojix semantics support reuse only for paths already validly registered at the destination. The copy invocation is documented as idempotent when the closure already exists, so a future copy could skip valid destination paths and resend missing paths. It must not assume that incomplete transfer residue is valid or reusable.

On the evidence available, a 2700-second retry is not shown likely to finish: the prior copy consumed essentially the full 2700-second bound, and the remaining byte count is unmeasured. A retry would need a restored/queryable candidate, exact closure accounting, remote valid/missing comparison, and an authorized resolution of the timeout/signature conditions before any safety or completion claim.

## Sources

- [resume-capacity witness](../witnesses/resumeCapacity.md)
- [earlier store-health witness](../witnesses/storeHealth.md)
- [earlier copy diagnosis](copyClosureDiagnosis.md)
- [`schema_runtime.rs` ClosureCopy invocation](/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:5209)
