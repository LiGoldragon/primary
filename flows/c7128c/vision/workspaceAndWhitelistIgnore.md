# Workspace and whitelist ignore

## 2026-09-18 — A workspace for everybody, merged into main; heavy data directories shared by mount under the lock; lightweight clones; primary stays super lightweight with a whitelist-only gitignore stated in AGENTS.md

Context: spoken directly by the living to Fable (Claude, medium, flow c7128c), in the same message as the commit subflow script. "Jiu-jitsu system" is a speech-to-text rendering of jj, the version-control system layered over Git; corrected inside the quote.

> We want to create a workspace for everybody, but anything that gets committed has to be merged into `main`, right? We don't want to duplicate a heavy repository, so we just share the data directories. We just mount them, and we use the lock. Other than that, everybody can have their own lightweight clone, like lightweight worktrees. Primary is going to stay super lightweight, and it just tells you how to mount the rest, and it has a default `gitignore` of all of it. It's a whitelist-only `gitignore` kind of thing, so it won't pick up messiness from agents. That's in the agents.md: anything outside of this is going to be ignored by the Git system, which is underneath the jj system, so it'll be ignored by version control.

-- psyche, direct to Fable c7128c; input mode not stated. ("jiu-jitsu system" reads "jj system"; corrected.)
