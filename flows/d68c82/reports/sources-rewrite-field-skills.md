# Sources rewrite: field-skills

Main `51920edfe6b29ca83ae39ea13766b167da7b02ec` (25 commits, no merges) carries no distillation Sources section in any commit, so it was not rewritten, no backup branch was pushed, and main did not move. The only `Sources:` line in any commit is in `skills/compensation-nix-rationale.md`: a list of external web citations (numtide blueprint, flake.parts, NixOS RFCs and manuals), not distillation references; it is left in place.

## Method

Every commit reachable from any ref was searched with `git grep -i` for `Sources` headings and lines, reference-form lines (`<hex id> <topic>`), `flows/<id>/vision` paths and `vision-raw <topic>` lines. The same result came from the read-only audit of flow 0c85a3.

## Sources

- `/home/li/private-repos/flow-evidence/0c85a3/skills-history-rewrite-20261011/`
