# h6zj Home publication and deployments

## Published source
- CriomOS-home main: `0c294523f71d9bbb4a9d6b6c59f4da8d75032b76`.
- CriomOS main and immutable consumer: `da9b38bd0f6989b96b31f63e96502f00f92b20b1`.
- The consumer locks that Home and persona `e1ebf473fb100489a52cab4ec6e982e09095feea`; explicit HTTPS main readback matched.

## Ouranos
- Identity preflight: logical and SSH node `ouranos`, user `li`; proposal was an absolute regular non-symlink and the secrets directory existed.
- Watch token 72/marker 13021 preceded Realize 544. It completed `Some.Succeeded` at marker 13037.
- Watch token 73/marker 13041 preceded ActivateNow 545. It completed `Some.Succeeded` at marker 13072.
- Lojix Current and live Home Manager profile both resolve to `/nix/store/j8i9hsrsms50pn63nw4009cab6alvdq7-home-manager-generation`.
- Declared/live launched Claude Desktop is `/nix/store/bjczvz8rjxhcr8i3iyjynx5g9iqx3kaj-claude-desktop-5.11492.2`; main PID 2724381. Declared Codex is `/nix/store/xnxjrb02pqq33khnss013651pkmr85jw-codex-0.169.0`.
- Flow stayed at `/nix/store/fs53xwvgp9kbam4sbc25671hdrvnl37q-flow-configured-0.54.7`; Curriculum stayed at the existing runtime. This Home operation did not restart them.

## Other hosts
- Zeus: the one authorized SSH attempt to `192.168.1.80` with canonical HostKeyAlias returned `No route to host`; no Lojix request was submitted.
- Prometheus identity succeeded. Watch token 74 preceded Realize 546. It failed terminally at evaluation because its generated projection has no `homeConfigurations.li`; no activation or retry followed.
- Prometheus generated references from Lojix evidence: horizon `sha256-UqMFShw27ocfs+Ko0pQ3W9ir9PGQI3LZ5X5WzbNvQME=`, system `sha256-KW3DUTifDJ6m2JuYiTVtJz+9ieAgqjCb46wgrMqxJJU=`, secrets `sha256-UXfrzp0B+uwSwvYhoW8v9Hg9tTtsJire8YmSf4h8SDQ=`. Secret contents were suppressed.

Raw requests, watch transcripts, terminal queries, and live readbacks are in the host subdirectories beside this report.
