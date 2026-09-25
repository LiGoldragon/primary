# HackyMessenger: fresh repository under the right name

Receipt by a subflow of e51411, 2026-09-25, on the living's order that HM's repository was misnamed by speech-to-text and must restart, with no trace of the wrong name in its history, as HackyMessenger.

## New repository

https://github.com/LiGoldragon/HackyMessenger, public, created with `gh`. Local clone `/git/github.com/LiGoldragon/HackyMessenger` (jj colocated, origin `ssh://git@github.com/LiGoldragon/HackyMessenger.git`).

- `main` 405e718fe5bbf09fb3252c34abc5bbb98a29b73a: one commit holding the old main tree (f56027ad), renamed.
- `clojure` ff20b3538757ddd1e3a2a00c431bb3ca39d0e40c: one root commit holding the old `hm-clojure-00f95a` tree at 00ed9e3a (fetched after Mind's 15:58Z push), renamed. `src/` and `test/` namespace directories became `hacky_messenger`; namespaces became `hacky-messenger.*`. The old branch tracked four stale `__pycache__/*.pyc` files, which its own `.gitignore` excludes; they were not carried.

Both refs confirmed by `git ls-remote https://github.com/LiGoldragon/HackyMessenger.git`. A fresh mirror clone of the real remote shows 0 matches for "hacking" (case-insensitive) in commit messages, in paths, and in blob content (text and binary) across every commit. The repository description reads "Hacky Messenger (HM)".

The registry directory (`~/.local/state/hacky-messenger`) and the Orchestrate lock name (`HackyMessengerDelivery`) already carried the right name; only the skill note, the READMEs, `check.nix` and the Clojure namespaces changed.

## Repointing

- `~/.local/bin/hm-{list,move,rebind,register,retire,send,send-abrupt}`: each swapped atomically (`ln -s` to a temporary name, then `mv -T`) to `/git/github.com/LiGoldragon/HackyMessenger/bin/`. All resolve.
- primary `tools/field-luna-heartbeat.mjs`: hm.py path repointed, commit f0200b21 (on primary main).
- Every command's `--help` note now names `compensation-hacky-messenger`.
- Not rewritten: records in `flows/38de5b` and `flows/e51411` (log, receipts, reports, vision) that mention the old name; they are records, not users of the path.

## Skill

Curriculum, fresh clone of `git@github.com:LiGoldragon/Curriculum.git` (the local checkout sits on another flow's branch): `skills/compensation-hacking-messenger.md` renamed to `skills/compensation-hacky-messenger.md`, every "Hacking" replaced with "Hacky". Landed at bdb5764f492f6b36c0c09c682e50d76e60575bda, confirmed by `git ls-remote`.

Regenerator: `curriculum-deploy` 0.6.3, built from `github:LiGoldragon/curriculum-deploy/dc7f70ed`, run as `Generate.{ «<fresh Curriculum clone>» «/home/li/primary» }`. A baseline run on the unedited source (at Curriculum 8864d42e) moved nothing in the generated trees. After the edit it renamed `.agents/skills/compensation-hacking-messenger` and `.claude/skills/compensation-hacking-messenger` to `compensation-hacky-messenger`, removing the old folders; `Check.{ … }` then returned `Checked.{ 72 23 }`. Primary commit 1a0dd3a93102385fa7053b23b714d2cd04baaca9 holds just those two files and is confirmed on primary's remote.

The Curriculum commit message mentions the old name ("rename from the misheard Hacking name"); Curriculum's earlier history already names the old skill.

## Retirement

`gh repo delete LiGoldragon/HackingMessenger --yes` ran after the new repository was verified; `gh repo view` no longer resolves it. The old local clone had nothing unpushed (only an empty working-copy commit) and was removed.

## Tests

- `python3 -m unittest discover -s .` in the new clone: 38 tests, OK.
- `hm-list` runs and lists the registry.
- `hm-send --help` shows `compensation-hacky-messenger`.
- No message was sent.
