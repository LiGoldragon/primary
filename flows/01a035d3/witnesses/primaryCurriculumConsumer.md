# Primary Curriculum consumer

Method: code read `/home/li/primary/flake.nix`

Primary pins `github:LiGoldragon/Curriculum` through its lock file. Its wrapper and `generated-skills-current` check use the locked Curriculum source as the generator's source root and Primary as the workspace root. The wrapper depends on the locked compiled `skills` package.

A local edit in `/git/github.com/LiGoldragon/Curriculum` therefore does not by itself invalidate Primary's package or check. Primary sees that edit only after its lock is updated or the input is explicitly overridden. Editing only Primary's generated output changes the workspace/check input, not the locked Curriculum engine derivation.

Primary's own `manifests/active-outputs.dotos` is not selected by the normal wrapper and differs from the current Curriculum copy. No active invocation using it as the source-root manifest was found. Its intended status is unknown.

Only Primary and copies of its worktrees were witnessed as checked-out consumers. Uncloned or external consumers were not enumerable.
