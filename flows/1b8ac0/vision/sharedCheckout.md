# One shared checkout, no worktrees per flow

> We can't use different worktrees for primary because then we don't have the same database for the psyche for all the subflows. That's why we have orchestrate. Plus, they only need their own flow ID subdirectory, so it's not even a problem. Just commit whatever. If somebody else hasn't committed, commit for them. Isn't that clear in the basic instructions already for everyone?

-- psyche, typed, 2026-09-22, said directly to PsycheHigh 1b8ac0 in reply to my proposal that Field move every flow into its own worktree. That proposal is withdrawn. The standing instruction in CLAUDE.md already says it: dirty changes found in the tree are committed first, as their own commit.
