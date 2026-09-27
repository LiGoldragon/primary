# Conditional resource grant: spirit-deployment check at 138c96

Issued by Field Sol 9ac67c on 2026-09-27 from the point-in-time resource census at 2026-09-27T08:35:19Z.

## Granted scope

This grants resources and execution clearance for exactly one local command: `checks.x86_64-linux.spirit-deployment` at immutable CriomOS-home revision `138c96b6fa56cbe4ea0958b2511bef1d5d205c1c`, with complete-host system and Horizon inputs frozen.

The executor is only the existing Sonnet-hosted author subagent `a055e7c7a698d88c0` (`claude-sonnet-5`) under Psyche Sonnet 38f337, for the owner Mind Astra 6fe957. No new worker is authorized.

The one run is bounded to 900 seconds, two jobs, two cores, empty builders, and public cache only. It uses `--impure --no-write-lock-file --no-link -L --max-jobs 2 --cores 2`. It must retain PTY start, end, exit, derivation, and log evidence.

## Preconditions and void condition

Immediately before start, the executor must directly witness all of the following:

1. Its own identity, availability, and actual `subflow`, `nix-workflow`, `testing`, `orchestrate`, `flow-evidence`, and `file-editing` receipts.
2. Lock 8189 remains held by 6fe957 over the exact spirit-deployment fixture scope.
3. The named source hash/revision is unchanged and complete-host inputs remain frozen.
4. A fresh host census finds no competing local Nix build or check and adequate memory.

Any failed or unknown precondition voids this grant. No run follows a void result. The command must start within five minutes of that immediate census; otherwise a fresh Field grant is required.

This Field grant is the only resource authorization. Sonnet and the named author record objective prestart facts; neither may issue a further or replacement clearance. If the same author's availability cannot be directly verified, this grant is inoperative. If the immediate census finds contention, stop without running, return the finding to Field, and do not retry automatically.

## Exclusions

No retry, full check, main movement, activation, service action, lock mutation, or model data movement is authorized. This is only a named diagnostic clearance.
