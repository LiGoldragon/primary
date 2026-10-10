# Lunar nixpkgs Update Cycle

Psyche ruling (psyche/Vision/setupIndependentInterfaces.md, 2026-08-17):
"Update on the first commit exactly after the new moon every lunation."

## Rule

Each lunation, pin nixpkgs to the first commit on the NixOS/nixpkgs
first-parent master history whose committer timestamp (UTC) falls strictly
after the new-moon instant for that lunation. Apply once per lunation.

## Which pins it governs

| Repo | Pin location | Update method |
|---|---|---|
| Curriculum | `flake.nix` nixpkgs input | Set `github:NixOS/nixpkgs/<rev>`, run `nix flake update nixpkgs` |
| primary | follows Curriculum's nixpkgs | No separate action needed |
| CriomOS + CriomOS-pkgs | `github:LiGoldragon/nixpkgs?ref=main` | Rebase fork `LiGoldragon/nixpkgs` onto the target rev (preserving backports), then `nix flake update nixpkgs` in both repos. Must move in lockstep. |

## How to perform an update

### Curriculum (and primary by inheritance)

1. Determine the new-moon instant from the table below.
2. Find the target commit: the first merge commit (2-parent) on master whose
   committer date is strictly after the new-moon instant, and whose first
   parent's committer date is before it (confirming adjacency).
   ```
   gh api "repos/NixOS/nixpkgs/commits?sha=master&since=<NEW_MOON_ISO>&until=<+1h>&per_page=100" \
     --jq '[.[] | select(.parents | length > 1)] | sort_by(.commit.committer.date) | .[0]'
   ```
   Verify the first parent's committer date is before the new-moon instant.
3. Confirm the rev is an ancestor of `nixpkgs-unstable`:
   ```
   gh api "repos/NixOS/nixpkgs/compare/<REV>...nixpkgs-unstable" --jq '.status'
   ```
   "ahead" means it is an ancestor (nixpkgs-unstable is ahead of the rev).
4. In Curriculum `flake.nix`, change the nixpkgs input to:
   ```
   nixpkgs.url = "github:NixOS/nixpkgs/<REV>";  # lunation <YYYY-MM-DD>
   ```
5. Regenerate the lock: `nix flake update nixpkgs`
6. Verify: `nix flake metadata` shows the correct locked rev.

### CriomOS + CriomOS-pkgs (separate procedure)

Rebase `LiGoldragon/nixpkgs` (which carries backports such as GTK MR !10130)
onto the target rev, then update locks in both repos. This is a separate
coordinated operation.

## New-moon reference table

Sources: USNO (https://aa.usno.navy.mil/api/moon/phases/year?year=YYYY)
and lunaf.com, cross-checked to the minute.

| Lunation start (UTC) | Target rev | Applied? |
|---|---|---|
| 2026-06-15 02:54 | | |
| 2026-07-14 09:43 | | |
| 2026-08-12 17:37 | 2d1e72b652ee13fd1297641ce735e06416d22827 | pending |
| 2026-09-11 03:27 | | |
| 2026-10-10 15:50 | | |
| 2026-11-09 07:02 | | |
| 2026-12-09 00:52 | | |
| 2027-01-07 20:24 | | |
| 2027-02-06 15:56 | | |
| 2027-03-08 09:29 | | |
| 2027-04-06 23:51 | | |
| 2027-05-06 10:58 | | |
| 2027-06-04 19:40 | | |
| 2027-07-04 03:02 | | |
| 2027-08-02 10:05 | | |
| 2027-08-31 17:41 | | |
| 2027-09-30 02:36 | | |
| 2027-10-29 13:36 | | |
| 2027-11-28 03:24 | | |
| 2027-12-27 20:12 | | |

## Open questions for the psyche

### (a) Raw master commit vs. channel-tested commit

The literal rule selects the first commit on raw `master` after the new moon.
This commit may predate channel testing: `nixpkgs-unstable` is a branch that
advances only after Hydra CI evaluates and tests a given master commit. A raw
master pin may have poor binary-cache coverage and possible evaluation
breakage. The alternative reading is "the first commit that the
`nixpkgs-unstable` channel advances to after the new moon" -- which guarantees
CI-tested, cached packages but lands later (hours to days after the new moon).

Status: unknown, awaiting psyche ruling.

### (b) Table coverage

The new-moon table above covers through 2027-12-27. It must be extended from
USNO data (https://aa.usno.navy.mil/api/moon/phases/year?year=YYYY) before
that date.

Status: unknown, awaiting psyche ruling on whether to extend annually or
further ahead.
