# Flow workbench verifier

Owner: flow `5f4fea`.

`check-handoff.py` reviews the two prompt files emitted by the existing
`flow-prompt-assembler` primary profile. It does not assemble prompts, launch a
successor, send a message, or edit a handoff.

## Input

The script reads only the explicitly supplied `--system-prompt`, `--user-prompt`
and `--primary-root` paths. It requires `--expected-successor`; that value is
checked against both prompt headings, so the verifier does not infer an identity.
It reads the user-prompt's exact source-coverage JSON and checks each listed
source's path, byte count, and SHA-256 against disk. It also requires every
regular file beneath `Vision/` and `Intent/`, and the nine selected skill bodies,
to occur in that manifest and as complete text in the system prompt.

## Output and cleanup

It writes one JSON review result to the caller-specified `--output` path. The
parent directory must already exist. It creates no output directory and leaves
no state outside that one result. The fixture test uses an automatically removed
temporary directory.

## Scope

The result is a review artifact. The demonstrated 05c604→fd0f97 output is an
old-predecessor prototype only; it is not the next successor handoff. A real
handoff must be assembled from the current predecessor after the separate
cheap-proof gate.

Promotion of this verifier into the flow assembler, and tokenizer/report work
into Signal research or quota/persona work, are proposals only. This workbench
does not activate either proposal.
