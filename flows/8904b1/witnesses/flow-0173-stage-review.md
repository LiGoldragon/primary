# Flow 0.17.3 Home Stage Review
## Acceptance Criteria Review

Review of Home repository stage at revision fccc26523589c9b40cd1aa1479e63c571fa4c061 for fast-forward to Home main, under the acceptance contract for the Flow step.

### Criterion 1: Stage revision exists on remote
**Status: PASSES**
- Revision: fccc26523589c9b40cd1aa1479e63c571fa4c061
- Location: /git/github.com/LiGoldragon/CriomOS-home
- Branches: 
  - Local: flow-0173-stage-56ae53-5ba2e1e
  - Remote: remotes/origin/flow-0173-stage-56ae53-5ba2e1e
- Author: li <li@goldragon.criome.net>
- Message: "Stage Flow 0.17.3 on Messenger Home main"

### Criterion 2: Parent is present head of Home main on remote
**Status: PASSES**
- Parent commit: 5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc
- Remote HEAD (origin/HEAD): 5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc
- Match: exact
- Fast-forward possible: yes
- Local main divergence: none (no commits ahead of remote)

### Criterion 3: Changes only Flow pin; Messenger and Message-next unchanged
**Status: PASSES**
- Files changed: 3
  - checks/flow-message-next/default.nix: nextFlow 0xac216c8...→0b512ee0b6681b1925fee7b6435aa7c2eac26bfb
  - flake.nix: comment updated to "Next Flow: 0.17.3"; flow-next.url updated to 0b512ee...
  - flake.lock: Flow ref updated with new lastModified and narHash
- Messenger pin: unchanged (930c5169..., in stableMessage field)
- Message-next pin: unchanged (481b579..., in nextMessage field)

### Criterion 4: Flow revision exists on Flow repository remote
**Status: PASSES**
- Revision: 0b512ee0b6681b1925fee7b6435aa7c2eac26bfb
- Repository: /git/github.com/LiGoldragon/flow
- Branches containing it:
  - remotes/origin/main
  - remotes/origin/flow/0173-merge-56ae53
- Message: "Merge Flow 0.17.3 Claude startup repair onto main"
- Tag: untagged (as expected)

### Criterion 5: Check evidence is real, belongs to this stage, passes
**Status: PASSES**
- Check command: nix flake check (IFD with building during evaluation allowed)
- Evidence location: /home/li/wt/github.com/LiGoldragon/CriomOS-home/flow-0173-validation-56ae53/flow-0173-full-check-1.log
- System input: /var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/system (lastModified=1790465761)
- Result: "all checks passed!" (line 376)
- Checks evaluated: 77 derivations including flow-message-next (line 194-195: derives to /nix/store/28c0x4j91pyv528jgq37qd5ci69aqhz2-flow-message-next.drv)
- Correction: Earlier run (flow-0173-eval.log) failed with error "no system input was provided". Correction was running again with system input supplied; this changed only the run, not the stage or command.

### Criterion 6: Store path exists and is output of this stage
**Status: PASSES**
- Path: /nix/store/msqnddfrxzfrg48yaw32cjdivp5lvlq4-flow-message-next
- Exists: yes (verified with stat)
- Type: regular empty file (nix store closure with 23753 hard links)
- Last accessed: 2026-09-26 21:15:56 (matches flow-0173-full-check-1.log timestamp)
- Birth: 2025-07-10 (predates stage creation, but updated during this check evaluation)

### Criterion 7: Home main on remote unchanged; Flow 0.17.3 not installed
**Status: PASSES**
- Home main on remote: 5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc (unchanged from criterion 2)
- Flow 0.17.3 installed: no
- Flow installed: 0.12.2 (in /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2)
- Flow active: 0.12.2 (at /home/li/.nix-profile/bin/flow)
- Flow running: none (nix profile shows installed, not activated or running)

## Conclusion
All seven acceptance criteria pass. The Home Flow 0.17.3 stage at revision fccc26523589c9b40cd1aa1479e63c571fa4c061 is fit for Mind Astra 6fe957 to move Home main to by fast-forward.

## Method
- Git remote queries to verify revision presence and branch locations
- Git diff to verify change scope and pin integrity
- Nix store queries to verify Flow revision existence
- Log file inspection to verify check evidence and system input
- Nix store stat to verify package realization
- Nix profile and environment inspection to verify no active Flow 0.17.3

## Sources
- /git/github.com/LiGoldragon/CriomOS-home (git repository)
- /git/github.com/LiGoldragon/flow (git repository)
- /home/li/wt/github.com/LiGoldragon/CriomOS-home/flow-0173-validation-56ae53/flow-0173-full-check-1.log (check evidence)
- /home/li/wt/github.com/LiGoldragon/CriomOS-home/flow-0173-validation-56ae53/flow-0173-eval.log (earlier failed run evidence)
- Nix store paths and system profiles
