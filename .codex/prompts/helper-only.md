# Helper-Only

Run the deterministic brief generator and use its output as the complete helper
instruction:

```sh
tools/helper-only-brief --harness codex --task "$ARGUMENTS"
```

Use the generated packet unchanged unless the user supplied a narrower
authority, lane, source, or mode that must be passed to the command. The lead
stays in main-thread no-reading mode and learns only from the generated packet
and the helper return.
