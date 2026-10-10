# cf7879 prompt-relay parser receipt

Source base: `e38dd1239859` (`relay-parser-cf7879`).

- Claude delivery filters matching roster records by a verified live PID before testing uniqueness and remains restricted to `idle` status. It does not delete daemon records.
- Plain files require explicit `--source-format peer-file` and may omit `--match`; they receive `peer-file` provenance, a content-hash source ID, and a null timestamp. They are not represented as human transcripts.
- HEAD remains exact. TAIL accepts only trailing whitespace or punctuation beyond its six characters, while relay payload bytes remain unchanged. Multiple matching candidates still refuse.
- The PTY path validates liveness again after attach approval and sends only one bracketed paste.

Local validation: `node tools/prompt-relay.test.mjs` passed (fixture suite; 1 process). Remote focused Nix validation is pending.

Remote validation: `nix build --max-jobs 0 --no-link --option substituters https://cache.nixos.org/ --option connect-timeout 5 '.#checks.x86_64-linux.prompt-relay-fixtures'` completed on Prometheus with exit 0. The final terminal transfer returned `primary-prompt-relay-fixtures` from the remote builder.
