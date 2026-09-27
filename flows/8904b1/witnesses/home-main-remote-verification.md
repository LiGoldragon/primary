# Home main remote verification witness

## Method

Read-only verification of Home repository (CriomOS-home, LiGoldragon account) remote main branch via bare clone and local git history analysis. No state changes, no lock actions. Examined: (1) Remote HEAD of main via ls-remote; (2) Commit ancestry and fast-forward check via merge-base; (3) Commit count and file diff between reported old and new revisions; (4) Flake pins in both revisions by examining flake.nix and flake.lock; (5) Lock service reservation 7880 from flow 8904b1's own log.md entry dated 2026-09-26.

## Remote main HEAD

Verified: `daf026f1e02bcd092f0ecc43b81207c96c6ec1b3` — matches report exactly.

## Fast-forward ancestry

Confirmed: daf026f1 is a fast-forward descendant of 5ba2e1e2. Ancestry check passed via merge-base.

## Commit count and changes

Between 5ba2e1e2 and daf026f1: **1 commit** (daf026f: "Stage Flow 0.17.4 on Messenger Home main").

Files changed (3 total):
- `flake.nix` — Flow pins
- `flake.lock` — locked revisions  
- `checks/flow-message-next/default.nix` — flow-message-next check fixture

## Pin comparison

At both revisions:
- `messenger-clj`: `93c12756f9c00dd3c13762590f17cee3a3712530` (unchanged)
- `message`: `930c5169ffcf5fa3784b34b2751763009e926d1d` (unchanged)
- `flow-next`: changed from `ac216c89...` to `bc464e5e...` (only pin change in the single commit)

## Reservation 7880

From flow 8904b1 log.md line 800, message from Mind Astra 6fe957 (2026-09-26):
- **Holder**: Mind Astra 6fe957
- **Name**: Home Flow 0.17.4 stage generation lock
- **Paths**: Home repository main, immutable CriomOS d04257a8, Home daf026f1
- **Reason**: Generation failed at evaluation due to frozen Ouranos/home system lacking `horizon.node.machine.hardware` required by CriomOS modules/nixos/metal/default.nix. No activation or service change occurred. Remains held pending horizon input resolution.
