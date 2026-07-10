SOURCE APPROVE

## Review
- Correct: `spirit-judge@6af6ed7c` changes only `ARCHITECTURE.md` (3 insertions, 2 deletions).
- Correct: `spirit-judge/ARCHITECTURE.md:25-27` assigns bounded single-attempt provider mechanics to `judge` and safe domain-specific retry policy to `spirit-judge`.
- Correct: This matches `judge@dfba388b/README.md:5-8` (“Calls are single-attempt; adapters own any domain-specific retry”) and `signal-spirit-judge@7c25b71a/ARCHITECTURE.md:22-26`.
- Correct: `CriomOS-home@0005123a` changes only `flake.lock`, advancing `spirit-judge` to `6af6ed7c`; immutable blob witness: `flake.lock:3320-3326`.
- Correct: `deployment@229d9e45` changes only `docs/spirit-judge-cutover.md` and `flake.lock`. Its lock pins Home at `flake.lock:821-827` and `spirit-judge` at `flake.lock:4066-4072`.
- Correct: Deployment documentation records the exact successor chain at `docs/spirit-judge-cutover.md:27-33`.
- Correct: Blob assertions reconstructed:
  - deployment `229d9e45` → Home `0005123a`
  - deployment/Home → spirit-judge `6af6ed7c`
  - spirit-judge `Cargo.toml:24,28` and `Cargo.lock:602-604,1234-1236` → judge `dfba388b` and signal-spirit-judge `7c25b71a`
  - deployment/Home → Spirit `f9f5266a` and signal-spirit-judge `7c25b71a`
  - Spirit `Cargo.toml:194` → signal-spirit-judge `7c25b71a`
- Blocker: none.

## Remaining live gates
These do not block source approval:

- Bound the authorized ambient Codex session through the approved non-secret status interface.
- Record the minimal Luna/Terra provider witnesses.
- Create and verify the private byte-preserving backup and logical marker.
- Activate immutable deployment `229d9e45`; verify generation, services, argv, restart behavior, and fail-closed rejection paths.
- Retain the documented rollback path.

No Nix, builds, deployments, services, providers, secrets, records, or backups were accessed. Existing unrelated working-copy modifications were observed in CriomOS-home and Spirit; all findings above came exclusively from the named immutable revision blobs.