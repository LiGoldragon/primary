# Duplicate fan-out prototypes — read-only comparison

Witness: persona_read, 2026-09-15. No implementation was merged, removed, activated, or selected as the surviving implementation. The living owns that decision.

| Property | Codex prototype 72e9ee7 | Peer main a983f1699 |
|---|---|---|
| Source reads | One | One |
| Lookup | Exact ID plus Unicode head/tail; ambiguous matches refused | Requested ID; first match wins |
| Assistant final support | Codex and Claude | Not supported |
| Whole / receipt | Effective distinct payloads | Whole only |
| Same bytes for N endpoints | Shared UTF-8 buffer | Per-endpoint native delivery |
| Transport | Injected Codex/Claude mocks | Unix WebSocket Codex and Claude control attachment |
| Tests | Source/provenance/modes/mock delivery | Fake sockets exercising real framing |
| Hooks installed | None | No installation established by this review |

Codex paths: tools/prompt-fanout-core.mjs, tools/prompt-fanout, tools/prompt-fanout.test.mjs on group-17-5f4fea at72e9ee766a3c4ddf690cfa55ea944f4381ae2ac2. Peer paths: tools/fan-out.mjs and tools/fan-out.test.mjs at a983f1699; its flake check is fan-out-fixtures.

The peer implementation uses initialize/thread-resume/turn-start for Codex and claude agents discovery, idle check, control-key socket attachment and bracketed paste for Claude. This is source evidence, not a live-delivery test by this flow. Its control-key handling needs the existing secret-safe authority boundary before use.

Recommendation: retain the Codex prototype as the behavioral base because it covers assistant completion records, minimal receipts, and ambiguous-ID refusal. Treat the peer implementation as a candidate transport reference for a separately reviewed adapter. Neither has been chosen by the living, and this recommendation authorizes no merge, deletion, hook or live delivery.

## Attribution of main report commit12f3f7277

Subject: “Log the identifier-tokenizers and persona-stranded-branch reports found in the tree”. Author/committer metadata: li <li@goldragon.criome.net>. Parent: fef4e858d77a92ad7ac8ce9707bedce5b2a5ec43. It is not descended from our report commit59394d6a375b73fb27ae92b86d0e9f35176d799c.

It adds exactly flows/5f4fea/reports/identifier-tokenizers.md and flows/5f4fea/reports/persona-stranded-branch.md, byte-identical to our flow branch files. The contents came from this flow's delegated reports. This flow's recorded report push is59394d6 on flow/5f4fea; this witness does not identify who ran the main commit operation or prove a copy/cherry-pick mechanism. No main push is claimed as this flow's action.
