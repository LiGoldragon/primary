<!-- to-the-living:start -->
Presentation.{ «A folder too full to index, 2nd edition» }

# A folder too full to index, 2nd edition

```
 a flow builds something
     |
     v
 +------------------------+
 | Nix leaves a link to   |
 | the result in a folder |
 +------------------------+
     |  the flow ends,
     |  the link stays
     v
 +------------------------+
 | the daily cleanup sees |
 | the link as "in use"   |
 | and keeps the build    |
 +------------------------+
     |  hundreds of these
     v
 +------------------------+
 | the store and its      |
 | link folder fill up    |
 +------------------------+
```

## Ouranos, before and after the cleanup

| | before | after |
|---|---|---|
| Nix store | 262 GB | 220 GB |
| entries in the link folder | 9.5 million | 4.9 million |
| warnings on a small import | 5,467 | 0 |
| time processes wait on IO | 79% | 36% |

The two measured minutes ran different workloads, so they compare loosely. The daily cleanup runs every night and removes old generations; it cannot remove a build that a leftover link still points to.

## What held the 42 GB

| left by | links |
|---|---|
| abandoned nested profiles | 57 |
| flows' scratch builds | 46 |
| superseded profile generations | 41 |
| deployment preparation | 25 |
| flows no longer running | 18 |
| test builds and result links | 11 |

Store optimisation stays on, on every host.

## Proposal 1: a build leaves no link behind

File: field-context/skills/compensation-nix-workflow.md, at the end

+ A build whose output is not kept builds without a link to it; a link made for a check or a deployment is removed when that work ends.

Ruling: land, amend, or reject.

## Proposal 2: let the folder grow past the limit

The disk's large-directory feature is switched on once, offline, from a recovery system. It cannot be switched off again; going back means restoring from a backup.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
