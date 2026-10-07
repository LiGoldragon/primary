<!-- to-the-living:start -->
Presentation.{ «Flow as it runs today» }

Four proposals for the skill that tells flows how
Flow works today. The skill lives in mind-skills,
file skills/knowledge-flow.md. Each adds lines
after line 17, the end of the file; nothing is
removed. Each asks one ruling: accept, change, or
refuse.

Every added line is labelled by its origin. Live
check: a command run on the deployed system, whose
result was kept. Source reading: the code read, not
run. Reported: a claim from a retained record,
not seen. No send or wake was tried.

## 1. The registry read of October 7

Why: a flow that must find another flow needs to
know which seats the deployed registry showed and
what that does not prove. The registry is the
list the messenger keeps of flows and their state.
Done means the work completed, not that the seat
was retired.

File: mind-skills/skills/knowledge-flow.md
Removed: none.

```
+Live check, Oct 7: the deployed hm-list wrapper
+(messenger-clj 0.3.0) showed these rows.
+Working: FieldSol, MindSol, Psyche Primary
+Fable f5a6e9. Blocked: Mind Primary Astra
+0c85a3. Done: Psyche Opus d4ae97, Psyche
+Tertiary 8f0f57, Mind Tertiary 918df4, Psyche
+Quaternary 02dda6, Mind Quaternary 4ddfe1,
+Field Tertiary 4371ed, Field Quaternary 6aa08d,
+Field Primary 44cda5, Psyche Primary Fable
+ebbe30. Old Psyche Fable 8475a9 and bad807 are
+stale or absent.
+Live check: Herdr showed 13 matched panes and
+titles. An earlier claim of 14 is withdrawn.
+The ordinary Flow list came back corrupted with
+NUL bytes; the cause is unknown.
+Live check: Flow CLI is 0.23 and the installed
+Nexus is 0.12.2. They are distinct. The version
+of the running process is unknown.
+Source reading: flows/index.md lines 260-284 is
+a historical handoff index, and the Oct 3
+roster.json is not a live registry. A row
+here is a witness, not proof of a Flow route.
```

Ruling: accept, change, or refuse.

## 2. Routing, and the ordinary and meta paths

Why: sending is the commonest act. The ordinary
path is the main socket. The meta path is the
owner-only socket.

File: mind-skills/skills/knowledge-flow.md
Removed: none.

```
+Source reading: hm-send resolves the exact short
+alias, uses the session Unix route and
+agent.prompt, rechecks the target, then reports
+Transported, Presented, Uncertain or a refusal
+(messenger-clj core.clj 191-258, 901-948).
+hm-send-abrupt has the same target guards and
+adds the interrupt keys (core.clj 834-887). It
+does not pass a blocked target. A wait for
+Presented may see working, idle, done or
+blocked; the later check still rejects blocked
+(core.clj 208-224, 259-265).
+Source reading: Flow stores its nodes and the
+harness events (flow-nexus store.rs 1605-1613,
+2177-2201; reporting.rs 1-57). No complete
+current Flow or meta-Flow inventory was found.
+A meta socket is not a meta-Flow registry. The
+meta source has no List variant
+(meta-signal-flow signal.rs 400-410).
+Keep messenger routing, Flow memory and meta
+event reads as separate layers. Reading hm-list
+never wakes a flow.
```

Ruling: accept, change, or refuse.

## 3. What wakes a flow, and what does not

Why: a flow may expect a message or a comment to
wake a sleeping seat. The evidence stops short
of that.

File: mind-skills/skills/knowledge-flow.md
Removed: none.

```
+Source reading: hm-send targets an exact alias.
+It accepts idle, working or done when the route
+verifies, and refuses a blocked target. Abrupt
+delivery keeps the same guards.
+Live check: none. No send or wake was tried.
+Reading hm-list only reads the ledger; it does
+not prompt a seat.
+Reported, not seen: the Oct 3 artifact-comment
+record says "@Claude" or "Send to Claude" is
+told apart from a plain comment, and that the
+continuous main loop owns the watch. It is not
+a witness of a real Claude.ai idle wake.
+No evidence supports waking every flow or
+polling every seat. The route is targeted: a
+named source, the verified messenger target,
+then its Flow or main loop.
+Keep three things apart: documented routing,
+retained harness claims, a witnessed idle wake.
```

Ruling: accept, change, or refuse.

## 4. Refusals and limits of evidence

Why: a flow reading a refusal should know the
failure is a named case, and which facts stay
separate.

File: mind-skills/skills/knowledge-flow.md
Removed: none.

```
+Source reading: Flow refuses an unknown,
+stopped, retired, exited, blocked, unavailable
+or occupied flow, and a failure to save
+(flow-nexus reporting.rs 31-40, delivery.rs
+32-52). The messenger adds Transported,
+Presented, Uncertain and refusal
+(core.clj 901-948). None of these proves that a
+model read a message.
+These are different evidence layers: the source
+checkout, the deployed wrapper, the Flow CLI,
+the Nexus binary, the Herdr pane list, the
+ordinary Flow list, the meta socket, a native
+binding, a first turn, an artifact watch.
+The corrupted ordinary list has an unknown
+cause. It is no evidence of a protocol mismatch
+or a dead store.
+Generated schemas, historical indexes and stale
+roster files do not replace a current binding
+witness. Do not infer deployment, wake success,
+retirement or liveness from a label, an absence
+or an old registry file.
```

Ruling: accept, change, or refuse.
<!-- to-the-living:end -->
