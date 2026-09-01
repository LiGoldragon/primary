# Zeus copy-closure diagnosis

The leading cause of deployment 30 is an effect timeout while `nix copy` was still transferring the closure, not a proven unreachable builder. Zeus accepted the transfer SSH session at `00:15:28.002144` and closed it at `01:00:27.658288`: `2699.656144` seconds. The active Lojix unit is configured with a 2700-second effect timeout. Lojix then logged `effect failed at CopyClosure` at `01:00:27.674188`, 15.9 ms after the target session closed, and recorded `BuilderUnreachable`.

The word `BuilderUnreachable` is an error-mapping artifact here. Lojix constructs `nix copy --substitute-on-destination --to ssh-ng://root@192.168.18.95 <closure>`, captures the command's exit/stderr, and wraps failures in `EffectFailure.string`. The deployment failure path logs only the effect stage and maps every `CopyClosure` failure to `BuilderUnreachable`; it does not persist the captured string. No exact `nix copy` exit code or stderr is retained in the daemon journal or deployment record.

## Observations

- Both strict SSH routes currently reach `hostname=zeus`; both current `ssh-ng` store pings succeed with Nix 2.34.6 and `Trusted: 1`; both endpoints present the same Ed25519 fingerprint. This disproves a currently persistent endpoint outage, but not a transient failure during the long copy.
- The target direct Ethernet is currently up/carrier 1 at 1000/full with zero cumulative errors/drops. The local route to `192.168.18.95` currently uses Wi-Fi (`wlp0s20f3`); its cumulative errors are zero, with RX drop 1 and TX drops 249. Bounded target kernel logs contain no link or transport fault around the failure window.
- The candidate exists locally but is absent from Zeus. The local candidate's recursive closure is 34.5 GiB, while the parent flow measured at least 1,932,511,150 bytes transferred and about 13 GiB of target free-space consumption before failure. The candidate root was not registered on Zeus.
- Zeus has 66,240,503,808 bytes free and 28,191,543 free inodes now. These capacity observations do not identify the status of paths created during the failed transfer.
- The candidate has no local signatures; 1,203 of its 3,579 recursive paths are unsigned. Zeus requires signatures, has no configured secret-key-files, and trusts a finite set of cache/host keys. This is a credible secondary cause, especially if the copy reached path admission after substantial transfer, but the exact rejection text is unavailable.

## Possible causes

1. Effect timeout at 2700 seconds while transferring a large closure. The session-duration and daemon-failure timestamps are direct, independent witnesses and strongly support this cause.
2. A signature/trust rejection involving the unsigned candidate or other unsigned closure paths. Configuration and candidate metadata support this hypothesis, but no stderr proves it for deployment 30.
3. A transient SSH/network interruption or stalled transfer. Current probes and bounded journals disconfirm a continuing outage, while cumulative counters cannot disprove a short-lived incident in the earlier window.
4. Destination capacity or store/database behavior during partial transfer. Current free blocks/inodes are substantial, but no read-only integrity or registration inventory establishes what the 13 GiB footprint contains. The running Lojix store cannot be opened by the read-only inspector because the redb lock is held.

## Disconfirming evidence and unknowns

The successful current SSH/store probes and clean target direct-link counters weigh against a persistent reachability or physical-link failure. The exact command start is inferred from the long-lived target SSH session; the target journal does not record the remote command name. The exact `nix copy` exit status, stderr, path-by-path registration result, and whether the timeout sent TERM before Nix produced a final error are unknown. No witness establishes whether any partial objects are valid registered store paths, temporary files, or merely the effect of unrelated store activity.

## Retry assessment

The source describes copy as idempotent when the closure already exists on the target. An identical request would therefore let Nix reuse destination paths that completed and were validly registered, while re-sending missing paths. It does not establish that the roughly 13 GiB consumed by the failed attempt is reusable: the candidate root is absent, and incomplete transfer data must not be treated as valid store content without a path-level witness. A retry could also reproduce the same 2700-second timeout or hit the signature policy again.

Before any retry could be called safe, a new authority ruling and all of the following should gate it: preserve/obtain the exact copy failure detail; establish a signer trusted by Zeus for every transferred path or otherwise resolve the signature policy through approved source/configuration; confirm strict endpoint identity and a measured, adequate transfer path; inspect destination path registration and capacity without assuming partial data is valid; and choose an effect timeout/closure-transfer strategy that can complete within the configured bound. No retry, copy, signing, trust change, GC, deletion, build, activation, or reboot was performed here.

## Sources

- [copy failure mapping witness](../witnesses/copyFailureMapping.md)
- [transport and link witness](../witnesses/transportAndLink.md)
- [store health witness](../witnesses/storeHealth.md)
- [parent deployment witness](../../01a02b46/witnesses/zeusDeployment.md)
- [`schema_runtime.rs` copy and failure handling](/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:3689)
- [Lojix operating contract](../../.agents/skills/lojix/SKILL.md)
