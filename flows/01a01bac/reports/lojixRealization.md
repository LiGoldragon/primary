# Lojix realization

## Placement and proposal history

This flow resumed the root-deployment problem exposed by 01a01a93. The first
proposal placed the guidance in operating-system after the living rejected a
Lojix skill. The later ruling superseded that proposal: Lojix documents its
own typed mechanism and operating-system references it. The following ruling
required the strict Dotos/Datom syntax rather than pseudo-examples.

The proposal recovery kept the boundary explicit: one inline Dotos object,
positional products, exact request-family field orders, separate ordinary and
owner sockets, explicit transport, immutable source policy, and terminal
observation. No production `Deploy.Host` example was invented: the flow had no
complete production Host command with proven transport values. The proposed
claim that the thin client streams subscriptions was also rejected; it returns
one reply and exits, so terminal observation re-queries.

The final proposal was explicitly approved. Its scope included the Lojix and
operating-system instruction surfaces, deployment variables and activation,
generation, tests, commits, pushes, and declarative deployment. The approval
did not authorize reboot or emergency runtime mutation.

## Test doctrine recovery and cleanup

The target-template concern initially led to removal of the any-brace source
validator, brace-free generated-output checker, and their checker-specific
tests and documentation while retaining conditional rendering and the
published model assertion correction. The later ruling made the scope general:
all source-searching tests are forbidden. It explicitly pointed back to
e06e4c07, whose doctrine treats source-text assertions as change-detectors,
not machinery tests. No source-searching validation was added for this
migration.

## Completion and deployment outcome

The legacy completion claim records the Lojix skill realization, Curriculum
generation, durable checks, commits and pushes, and declarative deployment as
completed. Present authored-source reads show the resulting Lojix and
operating-system contract; primary history contains the recorded deployment
landing. Those are observations of the current artifacts, not a rerun of the
historic test suite.

The final landed revision chain is Curriculum
`bb700c50d99c1fc28039b6ff407b7a114e218e91` (`Add Lojix deployment skill`),
primary `665a6351d7e45339b1c5c74506d4cb304e3bdf0f` (`Deploy Lojix skill
surfaces`), CriomOS-home `1a6e22da155bb75a6362d10623301b13d0c24b34`, and
CriomOS `d04f6dafce19b7b4f093c35716739f36d75973ba` (`flake: update
CriomOS-home input`). The consumer lock at that CriomOS revision pins the
named CriomOS-home revision.

Curriculum cleanup removed the remaining skill-text-searching assertions in
`0769f1d2c1fe`; primary separately records the general prohibition at
`333999a1ff70` and the checker-removal approval at `2ca704ea8855`. The
resulting doctrine is not limited to template braces: source-searching tests
are removed rather than replaced by another source-searching check.

## UserEnvironment deployment 27

Deployment 27 is separate from CompleteHost deployment 16. The direct ordinary
query reports UserEnvironment deployment 27 terminal Succeeded, from `(588
588)` through `(621 621)`, Current at CriomOS
`d04f6dafce19b7b4f093c35716739f36d75973ba`, with Home artifact
`/nix/store/rlija745aqpq5p5dkf3s7082g42x1i4x-home-manager-generation`.
The read-only target profile probe resolves to that same artifact. This is a
successful UserEnvironment profile activation, not evidence about the
CompleteHost ledger.

The inherited deployment incident is preserved separately from the completion
claim. CompleteHost deployments 14 and 15 used target-user transport and could
not mutate system or boot profiles. Deployment 16 used the root store URI and
SSH destination. Lojix terminal bookkeeping recorded activation failure, while
the target system profile and `/run/current-system` advanced to the same live
closure. The direct current probes still show the same split: controller
generation 7 is Current, while target links resolve to the `jngjk…` closure.
This is evidence that controller state and target state must be reported
separately, not a claim that the controller is live-target evidence.

The historical report names an unknown ByDeployment frame-I/O error. A fresh
ordinary `Query.ByDeployment.16` instead fails client decoding with `expected
z2VLsn to be a parenthesis block`; it does not identify the historical
frame-I/O failure's cause. The unknown remains unknown.

## Final state

This flow's legacy record, global duplicates, proposal chronology, source-test
doctrine recovery, deployment result, and unknown are now represented here and
in the flow-local vision and witness records. No deployment, reboot, emergency
runtime mutation, or source-searching test occurred during migration.

## Sources

- `sessions/realization/2026-08-19T171403.md` — 01a01a93 deployment incident and approval boundary
- `sessions/design/2026-08-19T121952.md` — 7c3f0c1d test-travesty context
- `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T22-18-09-01a01bac-91d6-7161-80c3-6f9ca38c7cf5.jsonl` — targeted typed source events
- `/git/github.com/LiGoldragon/Curriculum/skills/lojix.md` and `operating-system.md` — current authored deployment instructions
- `/git/github.com/LiGoldragon/Curriculum` commit `bb700c50d99c1fc28039b6ff407b7a114e218e91` — final authored Lojix landing
- `flows/01a01bac/vision/skillDesigning.md` — verbatim placement, syntax, approval, cleanup, and deployment rulings
- `flows/01a01bac/vision/testTravesties.md` — verbatim general source-searching-test prohibition
- `flows/01a01bac/witnesses/lojixDeployment.md` — direct controller and live-profile observations
- `flows/01a01bac/witnesses/userEnvironmentDeployment.md` — direct UserEnvironment deployment 27 and target-profile observations
- `flows/01a01bac/witnesses/curriculumCompletion.md` — authored-source and primary-history observations
- `flows/e06e4c07/log.md` — source-searching-test doctrine
