# Implementation evidence packet

## Item 11 — quota collector

Source branch: `git@github.com:LiGoldragon/primary.git`, `draft/5f4fea-g11g12-item11`, commit `a11b3b74ba8dc81097c2c0738dedbeed297353dc` (direct `ls-remote` verified). The isolated source paths copied here are `tools/codex-app-server-client.mjs`, `tools/quota-situation-report-cli.mjs`, `tools/quota-situation-report.mjs`, their tests, and `reports/read-only-account-inputs.json`. The client performs an injectable WebSocket JSON-RPC initialize handshake and exact read calls for `account/rateLimits/read` and `account/usage/read`; no live socket call was made. Eight Node tests and the pure remote Nix fixture derivation passed. The historical nixos-test scheduling failure remains report-only.

## Item 12 — first-prompt assembler

Source branch: `git@github.com:LiGoldragon/primary.git`, `group-17-5f4fea`, commit `72e9ee766a3c4ddf690cfa55ea944f4381ae2ac2` (directly verified). `tools/flow-prompt-assembler*` writes distinct system and user outputs, scans a predecessor lane, retains exact provenance, and refuses missing/ambiguous sources. Node and durable offline Nix checks passed.

## Item 13 — Persona Nexus draft

Source branch: `git@github.com:LiGoldragon/persona.git`, `flow/5f4fea-minimal-persona`, commit `56527105b41579657ea7b609bf4d0acdc3052bf9` (directly verified). The three-crate draft compiled against pinned `sema-engine`; five item13 tests passed. It is proposal-only and opens no sockets or services.

## Item 17 — fanout planner

Source branch: `git@github.com:LiGoldragon/primary.git`, `group-17-5f4fea`, commit `72e9ee766a3c4ddf690cfa55ea944f4381ae2ac2` (directly verified). `tools/prompt-fanout*` supports human and assistant-final exact source IDs, one source read and shared UTF-8 bytes, effective whole/receipt payloads, mocked Codex/Claude adapters, and failure fixtures. Node and durable Nix checks passed; no endpoint or hook was used.
