# Remote title — Psyche Opus b87854 (pid 2360492, session b8785453-ff53-4e5a-9a74-e21edb554467)

## Where the remote title comes from

Claude Code 2.1.280 keeps a session's name in the **session registry record**
`~/.claude/sessions/<pid>.json` — fields `name`, `nameSource`, `nameSince`,
`formerNames`, `bridgeSessionId`. That record is what `/rename` writes and what
carries the name to the Remote Control bridge session (claude.ai/code card).
The transcript-side `~/.claude/projects/<project>/<session-id>/custom-title.json`
(what `tools/canonical-title-alignment.mjs` reads for Claude) is the second
store, written on the same path. The Herdr pane `terminal_title` is a third,
separate surface.

Live seats each have all three. Examples:

- `~/.claude/sessions/1716162.json` → `"name":"Psyche Opus e51411"`, `"nameSource":"user"`, `"bridgeSessionId":"session_0127ja4iAR4GHbboCmAv6YJB"`.
- `~/.claude/sessions/1714346.json` → `"name":"PsycheV2.{ Sonnet 9c7514 }"`, `"formerNames":[{"name":"Psyche Opus b87854", ...}]`, `"bridgeSessionId":"session_01DFpBqgVDMfEqcAF78GSSN5"`.

## Why b87854 shows Sonnet

b87854 has **none** of the three:

- `~/.claude/sessions/2360492.json` — absent (only the `.key` and the live
  `/run/user/1001/cc-socks/2360492.sock` exist).
- `~/.claude/projects/-home-li-primary/b8785453-.../custom-title.json` — absent.
- `~/.claude/projects/-home-li-primary/b8785453-....jsonl` — absent. No
  transcript exists for this session anywhere.

Root cause, from the 2.1.280 bundle:

    function R0e(){
      if(a.CLAUDE_CODE_FORCE_SESSION_PERSISTENCE) return !1;
      if(!(a.CLAUDE_CODE_CHILD_SESSION && id() && !ka())) return !1;
      return !n().isChildSessionMarkerAmbientInTmux()
    }
    function Wzt(){ ... if(R0e()) return "nested_marker"; return null }   // persistence disabled

`/proc/2360492/environ` carries `CLAUDE_CODE_CHILD_SESSION=1`,
`CLAUDE_CODE_SESSION_ID=108ab020-3394-4fe2-8ae3-304ea1d20843`,
`CLAUDE_PID=2883797` — i.e. `start-psyche-opus-refresh.sh` was exec'd from
inside another Claude Code session's Bash tool, and the child-session marker was
inherited. There is no `TMUX` in that environ, so the tmux escape does not
apply, and no team context. Persistence is therefore suppressed: reason
`nested_marker`.

The three sibling seats launched over Herdr (`1714346` / 9c7514,
`1716162` / e51411, `157498`) carry the same inherited `AI_AGENT`,
`CLAUDE_PID=2883797` and `CLAUDE_CODE_BRIDGE_SESSION_ID`, but **not**
`CLAUDE_CODE_CHILD_SESSION` — which is exactly why they persist and b87854 does
not.

The rename path in the same bundle explains the misleading local stdout:

    ...updatedAt:Date.now()},n)||!ou();
    if(!y) log(`[session-name] "${e}" applied locally but the session registry record was not updated ...`)
    function ou(){ return _E()==null && !R0e() }

With `R0e()` true, `ou()` is false, so the failure branch is skipped: `/rename`
prints "Session renamed to: Psyche Opus b87854" and applies the name **in
process only**. Nothing reaches the registry record, the transcript title, or
the bridge.

Consequence, visible now: the name "Psyche Opus b87854" was never held in the
registry by b87854. When companion session 9c7514 started in a pane whose
terminal title still read it, 9c7514 derived that name (its `formerNames` shows
`Psyche Opus b87854`), then was renamed to `PsycheV2.{ Sonnet 9c7514 }`. The
registry name-sync repainted b87854's terminal title with it:

    wD:pQ  term_65c40f03ab16676  tab wD:tF  "PsycheV2.{ Sonnet 9c7514 }"   <- b87854
    wD:pW  term_65c55829fcb1088  tab wD:tK  "PsycheV2.{ Sonnet 9c7514 }"   <- 9c7514

This is the same hazard `tools/canonical-title-alignment.mjs` already refuses to
apply for Claude ("Claude native /rename affects sibling sessions here; live
native-title apply disabled").

## Fix for the successor seat

Clear the inherited child-session marker at launch (and, belt and braces, force
persistence):

    #!/usr/bin/env bash
    set -euo pipefail
    exec env -u CLAUDE_CODE_CHILD_SESSION -u CLAUDE_CODE_SESSION_ID -u CLAUDE_PID \
      CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 \
      claude --session-id <UUID> --model claude-opus-5-5 --effort medium \
        --remote-control --dangerously-skip-permissions "$(< <PROMPT>)"

Verify after launch that `~/.claude/sessions/<pid>.json` exists before calling a
title set or readback meaningful.
