Blocked before source-ready completion.

- Producer witness committed/pushed: `spirit-judge` `c2303a30ff88fea527a8075b22f1d598a80fdb80`.
- Retired confirmed task-created unlocked `/tmp/spirit-luna-witness`.
- Services remain inactive; backup and marker untouched; no Luna/Terra call or activation occurred.
- Rebase onto current CriomOS `main` `43d9234f` exposed `flake.lock` conflicts across the old candidate stack. Lockfiles were not hand-edited.
- Required lock regeneration/package validation is blocked by unrelated active Nix/Cargo work still running after 15 minutes. Smallest next step: wait for it to finish, regenerate only declared locks with one-job limits, then validate `.#witness`.