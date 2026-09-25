# Hacking Messenger repository and compensation skill

Receipt by a subflow of e51411, 2026-09-25, on the living's order to start with compensation, document the HM tools in a skill linked from the tool, and give HM its own repository, HackingMessenger.

## Repository

https://github.com/LiGoldragon/HackingMessenger, public, created with `gh`. Local clone `/git/github.com/LiGoldragon/HackingMessenger` (ghq, jj colocated).

History preserved: `git filter-repo` on a fresh clone of primary main (17ac2b3c) kept `tools/hacky-messenger/` (renamed to the repository root) and `tools/hm-*` (renamed to `bin/`): 16 commits, 8a510d5 to 1430fc5, content identical to primary's working copy at extraction (cmp of every file).

Landing commit 055d0574a17f527d7047c94f1118f310255bdf60 on main: wrappers call `../hm.py` through `readlink -f`; every command's `--help` ends with the note naming `compensation-hacking-messenger`; README (usage in the skill, installation, checks) and ARCHITECTURE added; `.gitignore` for `__pycache__/`. `git ls-remote git@github.com:LiGoldragon/HackingMessenger.git main` returned 055d0574a17f527d7047c94f1118f310255bdf60.

## Installation moved

HM was not a Nix package: `~/.local/bin/hm-{send,send-abrupt,list,register}` were links into `/home/li/primary/tools`. Each link was replaced atomically (new link, then `mv -T`) with a link into `/git/github.com/LiGoldragon/HackingMessenger/bin/`, and `hm-move`, `hm-rebind`, `hm-retire` were linked too. Registry state `~/.local/state/hacky-messenger` is unchanged.

primary's `tools/hacky-messenger/` and `tools/hm-*` were not changed or removed: `tools/field-luna-heartbeat.mjs` calls `tools/hacky-messenger/hm.py` by path, `tools/reap-flow` calls `tools/hm-list`, and `tools/msg` calls `tools/hm-send`.

## Skill

`skills/compensation-hacking-messenger.md` in Curriculum, landed at 3975783c7909840b4fb9bb027111a39f4657da0f from a fresh clone at `~/wt/github.com/LiGoldragon/Curriculum/compensation-hacking-messenger` (parent dd14ce7e). `git ls-remote git@github.com:LiGoldragon/Curriculum.git main` returned 3975783c7909840b4fb9bb027111a39f4657da0f.

Projection: `curriculum-deploy` 0.6.3 built from `git+ssh://git@github.com/LiGoldragon/curriculum-deploy?ref=main` (`/nix/store/6ym1xz0xqs3j43kxsilzdvxi0yk6047f-curriculum-deploy-0.6.3`), run as `Generate.{ «<fresh Curriculum clone>» «/home/li/primary» }`. Baseline run before the edit: clean status, no drift. After: only `.agents/skills/compensation-hacking-messenger/SKILL.md` and `.claude/skills/compensation-hacking-messenger/SKILL.md` appeared, committed in primary with this receipt. The harness then listed the skill.

## Tested

`python3 -m unittest discover -s .` in the new repository: 34 tests OK.
`hm-list` through the relinked `~/.local/bin`: exit 0, live agents and STALE registrations listed.
`hm-send --help`, `hm-send-abrupt --help`, `hm-register --help`: usage printed, ending with the skill note.
No message was sent.
