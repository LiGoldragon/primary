# Item 19 — native Nexus refresh witness

Date: 2026-09-15. The landed Curriculum commit `fd99d0e5` supplies this exact
boundary sentence in both generated projections:

> A CLI takes one inline datom value and translates it into Signal; a Nexus receives only Signal and never sees datom.

The projections `.agents/skills/nexus/SKILL.md` and `.claude/skills/nexus/SKILL.md`
are byte-identical, SHA256
`ab3abc39afa3ce2bb3c3b427aed1380518835cc68d0c40f905f931567cc92f27`.
No regeneration was performed.

## Native test

Exact command:

```sh
cat <<'PROMPT' | timeout 180s codex exec --ephemeral -m gpt-5.6-luna -s read-only -C /home/li/primary -o /tmp/item19-nexus-luna.txt -
$spirit $nexus $testing $flow-evidence $subflow
Data-only witness task. Propose a minimal Persona anatomy as a Nexus with two sockets. What do the sockets carry, and what does the CLI translate? Quote the exact boundary sentence from the native Nexus skill. Do not launch, connect, regenerate, or modify anything.
PROMPT
```

Exit: 0. Ephemeral session: `01a0a684-7cea-7eb0-99e9-5cf102905249`. The native
skill input was accepted. The response proposed ordinary and meta sockets
carrying typed Signal requests/replies and CLI translation from one inline
datom to length-prefixed binary Signal, with the Nexus receiving no datom or
text. It quoted: “It is the boundary where the textual form ends and the
binary world begins.” No launch, connection, regeneration, edits, or tests
were performed. A separate native turn ID was unavailable and is not claimed.
