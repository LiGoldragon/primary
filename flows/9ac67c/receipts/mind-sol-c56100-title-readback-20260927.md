# Mind Sol `c56100` title readback

Observed at `2026-09-27T02:33:45-06:00` by Field Sol `9ac67c`.

## Scope

This is a read-only identity and title witness.  It did not rename, repair,
rebind, route, prompt, or otherwise alter Mind Sol `c56100`.

The requested `testing-flow-titles` skill gate could not be loaded through a
skill interface in this worker context: no skill-interface tool was exposed.
The observations below therefore record the direct native and Herdr readbacks
without claiming that unavailable gate's additional procedures.

## Direct native-thread readback

The current native Codex catalog entry for native thread
`01a0e0a1-7075-7cc2-928d-13fc56100504` reported this exact `thread_name`:

```text
MindV2.{ Sol c56100 }
```

The live foreground Codex process was PID `318363`, whose command resumed that
same native thread through the current app-server control socket.  This binds
the title readback to the live native thread rather than to a historical
receipt.

The title itself displays aspect `Mind`, model display `Sol`, and Flow ID
`c56100`.  It exactly equals the required contract:

```text
MindV2.{ Sol c56100 }
```

Native-title comparison: **PASS**.

## Direct Herdr readback

The current `recovery-56ae53` Herdr agent lookup resolved native identity
`01a0e0a1-7075-7cc2-928d-13fc56100504` to:

```text
agent name:  mind_sol_c56100
workspace:   w1
tab:         w1:t1
pane:        w1:p3
terminal:    term_65c6d6c5c3aac3
status:      idle; interactive_ready=true
```

Both `herdr --session recovery-56ae53 agent get mind_sol_c56100` and
`herdr --session recovery-56ae53 pane get w1:p3` returned the same displayed
pane title, exactly as the API supplied it:

```text
MindV2.{ Sol c56100 } | mind-sol-successor-56...
```

Herdr has elided the suffix with `...`; this is an observed truncated display,
not a full-title readback.  Its visible title prefix is the required contract,
but the displayed Herdr pane title is a distinct value with a suffix.  The
complete suffix cannot be established from this readback.

Herdr comparison: **visible contract prefix PASS; full pane-title equality
UNVERIFIED (truncated display)**.

## Evidence grade

- Native title: direct current catalog readback, independently tied to the
  live process by exact native thread ID — **strong local runtime evidence**.
- Herdr title and binding: two current Herdr API readbacks, agent and pane,
  with matching native thread ID and terminal identity — **strong local
  runtime evidence**.
- Transport/remote message grade: **not applicable**. This witness sent no
  message and performed no external transport.
- Remote repository readback: after push and `jj git fetch --remote origin`,
  both local and `@origin` bookmark
  `field-title-readback-9ac67c` resolved to the same commit
  `c8ecd361708e3c0f180c43ed9110dec59f8e8d43`.  The receipt commit is therefore
  present on the real remote branch; the amended publication revision is
  recorded by the succeeding path-scoped commit.
