# Independent Protos fixture-closure gate

**PASS** for exact immutable commit `2c76ccf1ed7ba646a62962131bd60f8886daac54`, tree `b6551eb8afb2d4089c84e93c0bb411e3534d1b0a`, versus2672f833 fixture delta; whole source base15b41 was already independently reviewed without functional defect. This closes the prior fixture-only GAP, not a staging/push grant.

Fresh nonauthor reviewer `/root/review_protos_slice`, native `01a1adff-cafa-77a1-aa73-aa98b4dd4794`, sequential rereview23:23:28–23:23:56UTC, read-only/no writes/ref/remote effects. Parent lands reviewer report.

Extended construction test and5new tests in tests/protos.rs cover both fields' Negative/width attribution, largest native/i64 shared value, each x86_64 OutsideIntegerWidth, exact depth boundary, usize::MAX refusal, one→zero spend/max preservation, Unicode whitespace/comment/newline, UTF-8 offsets/error extent, six enclosure delimiters, representative refused non-enclosure/opaque/comment/separator glyphs and every cursor token boundary. Six named tests total (one extended/five new).

Platform qualification: cfg32 OutsideNativeWidth cases use u32::MAX+1 represented in i64 and independently test both fields in source. They were NOT compiled/run by the x86_64 receipt; this is platform-conditional source coverage, not claimed32-bit execution.

Independent `nix build --no-link .#checks.x86_64-linux.test` PASS, log tests/protos25/25 plus full suite/scale/doc-tests. Exact drv `/nix/store/g21avdmf7w8h642kzv5zszw30j0rwhkb-protos-test-0.33.0.drv`, result `/nix/store/7psrj3v59gs2sg54iljz18pkscjsr213-protos-test-0.33.0`.

Before/after clean detachedHEAD2c76ccf1/treeb6551eb8; frozen gate6e1cb5a31fe7f4646fdb97ca3df2e0eaef963a1e1c8e11b8c72d00dfbcc23b6f, finalconsumers3b4d85a9f88dd65fd2de9d67edcc06b37e9c607c5d14dabc59c2d812f1f16511, codec-boundarycec16610c0d8eccde53321751df7e28f5487c96b978e1f48ad29fda7b68e1759 unchanged. Staging effect remains Core-held.
