# nota-next parser OOM + agent memory-containment

A single malformed NOTA string drove a process to **23.6 GiB RAM + 9.6 GiB
swap**, killing the desktop UI for ~a minute. Root-caused, fixed at the
parser, and below: the pattern and how to constrain agents from ever doing
this again.

## Incident

During the Spirit big-trim (report 705), `spirit-bigtrim.service` (a bash
loop calling `meta-spirit` to import records) ballooned to 23.6 GiB + 9.6 GiB
swap and stalled the machine. It happened repeatedly — every run died at the
same batch (009), and harness/terminal sessions kept dying with it.

## Root cause — an unbounded parser loop on malformed input

Two layers:

1. **Trigger (my bug):** the audit's NOTA encoder double-escaped block-string
   delimiters in descriptions that are *about* NOTA syntax (e.g. record
   `f8m3`, "NOTA has two bracket-string forms: `[content]` … `[|content\|]`
   …"). The malformed escape produced an early-terminated block-string with
   stray `|]` sequences in the trailing tokens. (Fixed in report 705:
   `enc_str` / parser now match nota-next `escape_pipe_text`.)

2. **The real defect (nota-next):** `Parser::parse_atom` (parser.rs:781)
   breaks **without advancing** when the first character is a pipe-close
   (`|]`, `|)`, `|}`) at an object position (the `at_pipe_delimiter_close`
   guard). It returns a **zero-width atom**, so the enclosing
   `parse_document` / `parse_delimited` loop never advances — it spins
   forever, pushing empty blocks into a `Vec` until memory is exhausted.

   **Any** malformed or adversarial NOTA containing a misplaced `|]` OOMs the
   parsing process — a denial-of-service on every nota-next consumer (every
   component CLI and daemon that parses NOTA from agent/human/external input).

Confirmed: parsing `(a |])` under an 800 MiB cgroup cap is OOM-killed at the
cap (without the cap it reaches 23 GiB). `tests/parser_progress.rs` is a
watchdog-threaded regression.

## Fix (done) — parser guarantees progress

nota-next `parse_object` now rejects a stray pipe-close with
`NotaError::UnexpectedClose` instead of routing it to a non-advancing
`parse_atom`. The parser therefore always makes progress on malformed input;
bad NOTA fails fast instead of OOMing. Branch `parser-progress-fix`
(nota-next 0.5.1); full suite (70 tests) green. **Takes effect for consumers
on their next build against the fixed nota-next** — the currently-deployed
daemons still carry the vulnerable parser until rebuilt.

## The pattern, and how to constrain agents

The pattern is general: **unbounded resource use triggered by untrusted /
malformed input, run without a resource ceiling.** An agent that produces a
bad string (a typo, a bug, an adversarial payload) can take down the whole
machine. Defense must be layered:

1. **Input-robust parsers (root).** A parser over untrusted input must be
   bounded — guaranteed termination/progress (done), and ideally explicit
   limits on nesting depth, total blocks, and input length. No single bad
   input should be able to exhaust memory or stack. This protects every
   consumer.

2. **Memory-capped agent execution (the agent constraint).** Agent-spawned
   bulk / long-running jobs must run inside a cgroup with a hard memory
   ceiling so a runaway is contained, never machine-fatal:

   ```sh
   systemd-run --user --collect \
     --property=MemoryMax=2G --property=MemorySwapMax=0 \
     --unit=<job> bash <script>
   ```

   This is also the right detachment for long jobs — a `systemd-run --user`
   transient unit survives terminal/harness death (the harness kept killing
   session-tied jobs during the trim). The deepest version is **harness-level**:
   the agent harness should run *all* agent-spawned processes under a cgroup
   memory cap by default, so no agent action — bad NOTA, runaway loop, fork
   bomb — can ever OOM the workstation. That is a settings/harness change the
   psyche controls; absent it, the `systemd-run --property=MemoryMax` practice
   above is the per-job guard.

3. **Validate generated NOTA before feeding a daemon.** Encoders that emit
   NOTA should round-trip-validate (encode → parse → compare) before sending,
   catching malformed output before it reaches a parser.

## Recommended durable rules (for the intent layer)

- Parsers over untrusted input guarantee bounded resource use (termination +
  depth/size limits); malformed input fails fast, never exhausts memory.
- Agent-spawned bulk/long jobs run under a cgroup memory cap (and detached via
  `systemd-run --user`), so no agent action can OOM the host.

## Follow-ups

- Land `parser-progress-fix` to nota-next main + rebuild/redeploy consumers
  (esp. spirit) so production carries the bounded parser.
- Consider parser depth/length limits in nota-next (deep nesting still
  recurses → stack overflow is a separate, smaller DoS).
- Add the memory-cap practice to `skills/system-maintainer.md` (and consider a
  `tools/bounded-run` helper) so every lane uses it for bulk work.
- Avoid long bash wait-loops (`until … sleep` / `for … sleep`) and `timeout`
  in the harness — these correlated with terminal crashes this session; prefer
  detached units + short non-blocking status reads.
