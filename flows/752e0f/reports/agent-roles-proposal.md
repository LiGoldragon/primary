# Two subflow roles, proposed for the living's review

Drafted from `752e0f selfAudit`. Neither is a skill yet; each is written as the skill it would become.

## 1. self-audit (the self-doubt script)

    ---
    description: A flow has finished a piece of work and must audit it against the psyche before reporting it.
    user-only: true
    dependencies: [psyche, psyche-recovery, behavior]
    ---

    Arguments: the parent's topics, and the work to audit as the parent states it.

    First obtain the unified psyche on those topics through psyche-recovery: the distilled statement, then every raw or unmerged record newer than it, the newer word ruling where they differ.

    Then judge the work against that psyche, not against the parent's brief: each claim the work makes, each choice it took, and each thing the psyche asked for that the work left out.

    Return one datom in the SelfAudit type:

        Type
        SelfAudit.{ Vector<Finding> Vector<PsycheRecord> }
        [ Finding.{ Verdict Markdown }  Verdict.[ Holds Contradicts Missing Ungrounded ]  PsycheRecord.{ Topic Source Grade }  Topic.String  Source.String  Grade.[ Distilled Raw Notion Reconstructed ]  Markdown.String ]

    A Contradicts or Missing finding quotes the living verbatim with its sources line. Ungrounded marks a claim the work makes with no witness behind it.

    Read only.

## 2. psyche-recovery

    ---
    description: A flow must hold every psyche record that touches its topics before it designs, judges, or briefs.
    user-only: true
    dependencies: [psyche, transcript-search]
    ---

    Arguments: the parent's topics, and what the parent already holds.

    Search `Vision/`, `vision-raw/`, `flows/*/vision/`, and `flows/*/notion/`, archived records included, for every record touching a topic; search transcripts for the living's words on those topics that no record holds.

    Per topic: the distilled statement first, then each raw or unmerged record newer than it, verbatim with its attribution and one line of context, the question it answered or the work it was said in. Mark a newer word that departs from the distilled one as ruling.

    Leave out what the parent already holds.

    Return one Markdown block under 8 KB, each quote with its sources line and grade, ready for the parent to use or to inject as a new flow's user-level context.

    Read only.
