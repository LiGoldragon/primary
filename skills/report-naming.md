# Skill — report naming

*The basic naming and supersession discipline for reports. Every
agent needs this, regardless of whether they write substantive
reports themselves. Companion to `skills/reporting.md`, which
carries the larger discipline (chat-vs-report, inline-summary,
visuals, soft caps).*

## Filename

`reports/<role>/<N>-<topic>.md`

- `<role>` is the writer's lane subdirectory (`designer`,
  `operator`, `system-specialist`, `poet`, plus the assistant
  lanes).
- `<N>` is the next integer after the highest-numbered report in
  this role's subdirectory. **Per-role numbering**, not workspace-
  wide — `reports/operator/97-…md` and `reports/designer/97-…md`
  can coexist; the role subdir is the disambiguator.
- `<topic>` is a kebab-case description of the report's subject.
- **No leading zeros. No date prefix.** Commit history records
  when a report landed; the filename does not repeat that.

To find the next number:

```sh
ls ~/primary/reports/<role>/ | grep -E '^[0-9]+-' \
  | sort -t- -k1,1n | tail -1
```

Then `N = (that number) + 1`. Numbers are not reused after deletion.

## Iteration with `-v2` / `-v3` suffix

When a report is being actively refined with feedback (back-and-
forth with the psyche or another agent), the edited version takes
a `-v2` / `-v3` suffix:

- v1 (implicit, no suffix): `225-workspace-redesign.md`
- v2: `225-v2-workspace-redesign.md`
- v3: `225-v3-workspace-redesign.md`

The current version is the canonical one; delete the predecessor
in the same commit that lands the successor. Don't accumulate
v1/v2/v3 side-by-side.

## Supersession with a new number

When the topic shifts enough that the *name after the number*
should change (concept → implementation; redirect of scope;
absorption of an audit's findings), write a new numbered report
and delete the predecessor:

```
write   reports/<role>/226-new-topic.md    (absorbs /225)
delete  reports/<role>/225-old-topic.md    (same commit)
```

The new report carries forward anything still relevant from the
predecessor. The predecessor's number is retired — number
sequences are gap-tolerant; the next report takes
next-highest-plus-one within the role's subdir, not the freed
number.

## Commit before delete

**Never delete an uncommitted report.** Commit first. Deletion of
a committed report only removes it from the work tree — git
history retains the substance and the report is recoverable.
Deletion of an uncommitted report is total loss.

For the rename/supersession protocol: the new report must be
committed (in the same commit as, or before, the predecessor's
deletion). The discipline:

```
write    reports/<role>/N-new-topic.md
git add  reports/<role>/N-new-topic.md
git rm   reports/<role>/M-old-topic.md
commit                                       (one commit; both visible)
push
```

(With `jj`: a single `jj commit reports/...` finalises the addition
+ deletion together.)

## See also

- `skills/reporting.md` — the larger reporting discipline
  (chat-vs-report, inline-summary rule, visuals, hygiene, soft
  caps).
- `skills/jj.md` — the version-control flow these commits use.
- `intent/reports.nota` — psyche statements driving this
  discipline.
