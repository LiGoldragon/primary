# Scoped main-flow projection plan and receipt

## Rendered plan before installation

The Primary flake remains pinned to Curriculum `99409107f4e62d67644612164db069643d4774fe` and `curriculum-deploy` `dc7f70edce087ac4157d7b48af954177ce454491`. Authored Curriculum main `c5e33e351f2aad73059c6496e51789b83fafec68` is clean; only its accepted `skills/main-flow.md` change is selected for this scoped installation. The existing generated outputs are regular files, not symlinks. Lock 4332 covers exactly the three target files.

Using the pinned Primary `nix run .#generate-skills` wrapper and existing deploy runtime, I rendered the pinned Curriculum archive and the accepted Curriculum archive into separate empty disposable workspace roots under `/tmp/mainflow-projection.AlBMY6/`. Each Generate returned `Generated.{ 66 21 }`. No Generate or Check ran against Primary. The pinned render matches all three existing preimages byte-for-byte, establishing legacy generator ownership for these exact outputs only:

| Target under `/home/li/primary` | Existing/pinned SHA-256 | Accepted render SHA-256 | Action |
| --- | --- | --- | --- |
| `.agents/skills/main-flow/SKILL.md` | `dc1f25c072a54856c246f819bd047c980c3275addb31aebac0a39d935c173ecc` | `8abaeae311818a48e7480cd88dc19e5f327b4c7c76cc8b511d4f1fcc6e4479dd` | Replace after exact preimage CAS. |
| `.claude/skills/main-flow/SKILL.md` | `fa2c3139036f63fa558b30bbcad7f7c48a8e46bb514b7a3ca78e7ad2af9e0505` | `e753d1330d69c0e34398300bfb9efb7b0a417cfe2bb691edaf8c1d9c20660110` | Replace after exact preimage CAS. |
| `.agents/skills/main-flow/agents/openai.yaml` | `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` | Same digest. | Preserve; user-only sidecar still disables implicit invocation. |

The two Markdown replacements change the main-flow delegation/inspection instructions. Frontmatter dependencies and the sidecar remain the same. This is a narrow replacement of known existing generator outputs under the user's authorization. It is **not** the proposed typed `SkillKey` source/type ledger, complete namespace snapshot, CAS inventory generation, durable journal, or safe whole-tree reconciliation in `flows/4b0f60/reports/curriculum-skill-namespace-ownership.md`. Those mechanisms are absent from the current runtime. No other skill namespace, role projection, source pin, or inventory is selected.

## Installation receipt

Under lock 4332, a scoped installer rechecked both pinned preimage digests immediately before each atomic replacement, rejected symlink/non-regular targets and ancestors, and copied only the two accepted rendered Markdown files. It staged each replacement in the target directory and used `os.replace`; on a detected mid-install failure it would restore an already replaced file only if that file still matched the expected new digest. The actual run completed without rollback.

Post-install SHA-256 and `cmp` agree byte-for-byte with the accepted render: Codex `8abaeae311818a48e7480cd88dc19e5f327b4c7c76cc8b511d4f1fcc6e4479dd`, Claude `e753d1330d69c0e34398300bfb9efb7b0a417cfe2bb691edaf8c1d9c20660110`. The sidecar remains byte-for-byte equal to the pinned render at `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94`. Primary's Curriculum pin remains `99409107`; the authored accepted source remains `c5e33e35`. Scoped working-copy status showed only these two modified outputs and this new report before commit. This verifies installed bytes, not global mixed-source Check or active-session native injection.

Push and remote readback will be recorded below after the scoped installation commit is published.

## Sources

- `flows/4b0f60/reports/curriculum-skill-namespace-ownership.md`: accepted architecture and current generator cleanup/overwrite limitations.
- Primary `flake.nix` and `flake.lock`: pinned Curriculum and deploy runtime; `nix run .#generate-skills` wrapper.
- `/git/github.com/LiGoldragon/Curriculum` archives at pinned `99409107` and accepted `c5e33e35`, each rendered with the supported Generate request into its own empty disposable root.
- The three current Primary target files, pinned-render files, and accepted-render files: regular-file checks, SHA-256 digests, exact `cmp` preimage equality, and sidecar equality.
