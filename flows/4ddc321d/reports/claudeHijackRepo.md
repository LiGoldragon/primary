# claude-hijack repository report

## What was stood up

Public repository `LiGoldragon/claude-hijack` at
https://github.com/LiGoldragon/claude-hijack, cloned to
`/git/github.com/LiGoldragon/claude-hijack`.

Purpose: documentation and replacement of the Claude Code harness's stock context.
Continues the base-context replacement design of flow 2f6b1dc5.

## Extraction methods and versions

- Claude Code version witnessed: **2.1.241**
- Build date: 2026-08-22, git SHA `c87e2742fc9ad269ec8920460d00a091b1e410f0`
- Binary path: `/nix/store/z8v8iqiw084sxw2licg0pad9hwy7wmkg-claude-code-2.1.241/bin/claude`
- Nix store path confirmed via `readlink -f $(which claude)`
- Extraction method: `strings -n 30` (ASCII) and `strings -e l -n 30` (UCS-2)
  on the compiled ELF binary, then code-read of the minified JS bundle found
  in the ASCII strings output to identify assembly functions and content
- Behavioral probe of the installed binary (structural outline of 21 blocks)
- Cross-verification: extracted text confirmed against binary strings for
  key blocks (security directive, identity lines, delivering-work, pronouns)
- All text copied verbatim from binary; no text written from memory

### Key difference from codex-hijack extraction

Codex's stock context lives in readable prompt.md files in the open-source
repository. Claude Code's stock context is **programmatically assembled** from
template functions in a minified, compiled JS bundle embedded in a Node.js SEA
binary. There is no single contiguous text file to extract. Each block is a
separate function that conditionally composes its text, gated by feature flags,
model family checks, and session mode. The extraction required code-reading the
minified JS assembly functions and extracting their string content.

## Block inventory (21 system-prompt blocks + 8 system-reminder messages)

System-prompt blocks (8 static + 13 conditional):

0. Identity line (3 variants by session type)
1. Opening / agent description
2. `# System` (rendering, permissions, hooks)
3. `# Doing tasks` (software engineering guidance)
4. `# Executing actions with care` (reversibility, confirmation)
5. `# Using your tools` (tool preference, parallel calls)
6. `# Tone and style` + `# Text output` (formatting, narration policy)
7. `IMPORTANT:` security directive
8. Pronouns (conditional)
9. Fable 5 identity paragraph (conditional, model-dependent)
10. JSON parameter enforcement (conditional, model-dependent)
11. `# Session-specific guidance` (conditional)
12. `# Environment` (conditional, dynamic)
13. `# Scratchpad Directory` (conditional)
14. `# Context management` (conditional)
15. Act-decisively directive (conditional, feature-flagged)
16. `# Delivering work` (conditional, model-dependent)
17. `# Corrections` (conditional, model-dependent)
18. Autonomy append (conditional, model/mode-dependent)
19. Remote-controlled injection (Heron Brook, runtime-fetched, not extracted)
20. Subagent steering (counter-steer mode only, not fully extracted)

System-reminder messages (separate API messages):
CLAUDE.md, Skills listing, Agent types, Deferred tools, Git status, User email,
Current date, Token budget.

Tool descriptions delivered via API tools parameter (not in system prompt).

## Flagged worst-offender candidates

Ranked by estimated misalignment with the psyche's stated direction:

1. **Autonomy and completion pressure** (Blocks 18, 3, 15) -- "You are
   operating autonomously... asking will block the work" contradicts the
   extension model. "Highly capable" framing and "act, do not re-derive"
   push speed over understanding.
2. **Tone and personality prescriptions** (Blocks 6, 17) -- "short and
   concise" responses, narration suppression, self-correction suppression
   impose vendor personality overriding authored character.
3. **Software engineering tunnel vision** (Blocks 1, 3) -- "helps users with
   software engineering tasks" framing causes misinterpretation of
   non-engineering requests.
4. **Vendor marketing in the context** (Blocks 9, 12) -- Fable 5 marketing
   copy, product placement ("default to the latest and most capable Claude
   models") compete for context with authored instructions.
5. **Prohibition-dense form** (Blocks 4, 6, 17) -- "Don't add features",
   "Don't narrate", "Avoid unnecessary self-correction" -- prohibitions cost
   context and hide roads (per 68512643 psyche ruling).
6. **CLAUDE.md override framing** (system-reminder) -- "These instructions
   OVERRIDE any default behavior" positions vendor context as the default;
   authored context must fight to override it.

## Override verification at 2.1.241

Re-verified against the 2.1.235 witnesses (flow 2f6b1dc5):

- `--system-prompt` / `--system-prompt-file`: confirmed full replacement of
  instructional body; identity line survives; environment block dropped.
  Unchanged from 2.1.235.
- `--append-system-prompt` / `--append-system-prompt-file`: confirmed append
  to default body. Unchanged.
- Identity line selection logic (`Iii()` function): 3 variants confirmed
  identical to 2.1.235.
- Managed-settings `appendSystemPrompt`: confirmed present in binary strings.
- Tool schemas, system-reminders, CLAUDE.md: confirmed harness-composed
  regardless of replacement. Unchanged.

## Blockers

- Block 19 (Heron Brook / remote-controlled injection): content fetched from
  remote service at runtime and injected into the system prompt. Content
  unknown from binary analysis. This is a runtime-variable block whose content
  could change without a binary update.
- Block 20 (Subagent steering): only included in counter-steer mode; not
  applicable to standard sessions, but not fully extracted.
- Tool description embedded instructions (commit protocol, PR creation
  protocol, etc.) are composed by per-tool template functions with
  interpolation. The static fragments are extracted but the full composed text
  depends on which tools are available and which feature flags are active.

## Edit coordination

The meta-orchestrate lane registration and orchestrate claim machinery did not
accept the DOTOS syntax attempted (same experience as the codex-hijack
subflow). The claim is advisory; this is noted and work proceeded without a
registered lane.

## Repository index

Both `codex-hijack` and `claude-hijack` added to
`/home/li/primary/protocols/repos-manifest.dotos` under a new `Hijack`
comment group in the Tooling family, as Content repos with Active lifecycle
and `(OtherDoc README.md)` doctrine home.

## Sources

- Claude Code 2.1.241 binary: `/nix/store/z8v8iqiw084sxw2licg0pad9hwy7wmkg-claude-code-2.1.241/bin/.claude-wrapped`
- `strings` extraction (ASCII and UCS-2) of ELF binary
- Code-read of minified JS bundle in ASCII strings output
- Behavioral probe of installed binary (structural outline)
- Prior witnesses: 2.1.231 code read (session 358f143a), 2.1.235 probe (flow 2f6b1dc5)
- Ledger: `verified/claude-code-context.md` in primary workspace
- Psyche ground: `psyche-raw/Vision/gradientsOfAuthority.md`, `flows/2f6b1dc5/vision/`
