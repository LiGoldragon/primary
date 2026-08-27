# Vision Impurities — Skill Change Proposal

## 1. Which skill carries the logging instruction

`psyche-interraction.md` owns the logging rule ("Log psyche rulings in the
flow's own `vision/<topic>.md`") and already carries the exclusion list
("conduct corrections, process events, and session narrative are not entries").
The differentiation between vision and working instructions belongs here
because this is the skill an agent holds when deciding what to log.
`psyche-distillation.md` receives the destruction rule only, since it is the
site of encounter. `flows.md` names the directory structure and need not change.

## 2. Proposed changes

### psyche-interraction.md — Logging section

```diff
-Record psyche rulings only; conduct corrections, process events, and
-session narrative are not entries. Supersede an entry by appending;
-never edit one.
+Record psyche rulings only; conduct corrections, process events, and
+session narrative are not entries. A working instruction — directing a
+flow's task (scope, priority, which project, what to do now) — goes to
+log.md, not to vision; a working instruction logged as vision is a vision
+impurity. Supersede an entry by appending; never edit one.
```

### psyche-distillation.md — end of file

```diff
 Distillation is proposed on encounter or done in dedicated
 passes.
+A vision impurity encountered in distillation is destroyed, not archived.
```

## 3. Vocabulary entry

Yes. Add to `vocabulary.md`:

> Vision impurity: a working instruction (scope, priority, which project,
> what to do now) logged as a vision record.

The term is defined once here per vocabulary skill convention; the skills
use it without re-defining it.

## 4. Regeneration and commit sequence on approval

Run `nix run /home/li/primary#generate-skills -- "CurriculumRequest.{Generate.{/git/github.com/LiGoldragon/Curriculum /home/li/primary}}"`, then commit and push Curriculum (`git push`), then commit and push primary (`git push origin HEAD:main`) per the file-editing skill.

## Sources

- flows/b675f3d9/vision/visionImpurities.md — psyche ruling (2026-08-27)
- /git/github.com/LiGoldragon/Curriculum/skills/psyche-interraction.md
- /git/github.com/LiGoldragon/Curriculum/skills/psyche-distillation.md
- /git/github.com/LiGoldragon/Curriculum/skills/flows.md
- /home/li/primary/.claude/skills/vocabulary/SKILL.md
- /home/li/primary/.claude/skills/skill-designing/SKILL.md


---

# Revision 2 (2026-08-27, after the living's ruling)

The living: conduct corrections can very well be vision — designing
model behavior is the work; be very clear on what does not qualify;
the impurity line in psyche-distillation is approved (applied).

## psyche-interraction.md — Logging section (revised)

```diff
-Record psyche rulings only; conduct corrections, process events, and
-session narrative are not entries. Supersede an entry by appending;
-never edit one.
+Record the psyche's rulings, corrections of an agent's conduct among
+them — designing model behavior is vision. Not vision, and not an
+entry: a working instruction (what to do now, in what order, at what
+scope, on which project, through which dispatch — it goes to
+log.md); a process event (a subflow finished, a commit landed, a file
+was read); session narrative; an acknowledgement that rules on
+nothing. A working instruction logged as vision is a vision impurity.
+Supersede an entry by appending; never edit one.
```

## psyche-distillation.md — one further sentence (new, for ruling)

```diff
 A vision impurity encountered in distillation is destroyed, not archived.
+A proposal names, for every statement, the Vision topic it lands in;
+a statement in the wrong topic cannot be approved.
```

## vocabulary.md — unchanged from §3

> Vision impurity: a working instruction (what to do now, in what
> order, at what scope, on which project, through which dispatch)
> logged as a vision record.


---

# Revision 3 (2026-08-27) — final edit set for ruling

The living: impurities are not hunted; they are eliminated only
through distillation, and a proposal points out the impurities it
discards. Distillation itself restarts in a new flow.

## psyche-interraction.md — Logging section

```diff
-Record psyche rulings only; conduct corrections, process events, and
-session narrative are not entries. Supersede an entry by appending;
-never edit one.
+Record the psyche's rulings, whatever they design — a machine, a
+syntax, a vocabulary, an agent's behavior, the way the work itself is
+done. Not vision, and not an entry: a working instruction (what to do
+now, in what order, at what scope, on which project, through which
+dispatch — it goes to log.md); a process event (a subflow finished, a
+commit landed, a file was read); session narrative; an
+acknowledgement that rules on nothing. A working instruction logged
+as vision is a vision impurity. Supersede an entry by appending;
+never edit one.
```
(Revision 4: the designing clause widened on the living's word —
"dont make the designing line narrow".)

## psyche-distillation.md — end of file

```diff
 A vision impurity encountered in distillation is destroyed, not archived.   (landed)
+Impurities are never hunted: they fall only through distillation, and
+a proposal points out the impurities it discards. A proposal names,
+for every statement, the Vision topic it lands in; a statement in the
+wrong topic cannot be approved.
```

## vocabulary.md — entry

> Vision impurity: a working instruction (what to do now, in what
> order, at what scope, on which project, through which dispatch)
> logged as a vision record.
