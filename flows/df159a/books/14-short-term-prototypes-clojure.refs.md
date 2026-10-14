References for book 14 «Short-term prototypes: Clojure now?»
Plain text beside the book's source. Never passed to the page builder
(tools/book-build.clj reads only the source .md and tools/book-code.html).
Archived with the landing when some or all of a proposal is accepted.

## Records drawn from (his words; provenance STT)

flows/88475f/vision/cljTools.md — 2026-09-25, spoken to e51411, relayed
by e51411; section «Clojure prototypes, then Ethos and Rust»:
«You could kind of emulate the kind of code that you would write in Rust
and it's sort of faster to make one-off prototypes. Then you can rewrite
them in Ethos and in Rust from the [Malli] and the pseudo traits that you
wrote in [Clojure].» (Proposal 1)

flows/da2038/vision/prototypes.md — 2026-10-13, STT; also copied in
flows/d68c82/vision/flow.md «Short-term prototypes are written in
Clojure»: «I said before that I want the short-term prototypes to be
written in Clojure and I see .mjs and I don't recognize Clojure. I'm
pretty sure Clojure is .clj. In the proposal all the code that's being
proposed is the wrong stack. If any prototype doesn't use Clojure it's
going to have to be rewritten in Clojure and I don't understand.»
(Proposals 1–3)

flows/d68c82/vision/tools.md — 2026-10-14, STT, book comment on
«Communicating with the living»: «I don't want tools to accumulate in
the main workspace either so they should live in appropriate
repositories.» (Proposal 1, choices 4–5)

flows/33752b/vision/flow.md — 2026-10-13, STT: «the short-term solution,
which is [Clojure]» (the short-term solution is not the Nexus; context
for Proposal 1 choice 3).

flows/d68c82/vision/flow.md — 2026-10-13T17:47, STT, «Flow starting
configured in EDN, per aspect and per metaflow» (the EDN files
Proposals 2 and 3 move values into).

Proposal 4 rests on the living's word relayed 2026-10-14 by the
coordinating seat: a book carries no verbatim quote, record citation or
source path; references live beside the source. No raw record path for
it was given to this seat.

## Machine facts and their origin

Audit: flows/d68c82/reports/clojure-migration-2026-10-14.edn
(generated 2026-10-14). :totals :live-by-lang clj 10, mjs 19, py 1,
sh 4 (34 live files); :values-by-kind absolute-path 20, model 14,
prompt 13, skill-list 8, flow-id 2, hook-path 1 (58). Figure counts
recounted from the :files rows: messenger-clj live .clj 5 (data_readers,
core, legacy_import, main, typed_store) plus nix/launcher.sh; field-clj
live .clj 5; sh live 4 (the launcher and 3 home hooks).

Draft: flows/d68c82/reports/startup-prompt-draft.md named
config/main-flow/first-prompt.edn and tools/first_prompt.clj; neither
exists in the working tree (witnessed 2026-10-14).

Landed: commit 3f1cf6c40 (2026-10-14 09:26:58 -0600, «Start flows with
declarative topic proposals and current context»): config/main-flow/
shared.edn gained :first-prompt-template and
:first-response-timeout-seconds 900; tools/main-flow-mode/
launch-config.mjs gained firstPromptFromConfig;
tools/claude-main-flow-launch.mjs lost STARTUP_INSTRUCTION (present at
816253a0f). Removed lines quoted in Proposal 3 are the working-tree
lines of tools/native-worker-launch.mjs:9,
tools/claude-main-flow-launch.mjs:91 and tools/secondary-first.mjs:12.

## Skill texts struck or placed in Proposal 4

psyche-context/skills/vision-book.md, «Books», L8 (the landing point).
.claude/skills/compensation-book-crystallization/SKILL.md L14 (struck
sentence «A proposal may cite the record it crystallizes by path and
date.»; «A book does not restate the living's words.» kept, no
conflict). .claude/skills/compensation-psyche-interraction/SKILL.md L93
(«names the psyche module, the lines removed, and the lines that replace
them, verbatim») read; no conflict, not shown.

## Revision 2 (the Secondary's audit of Version 1, folded in)

tools/claude-native-seat-refresh.py:708–727 EDN_FIRST_PROMPT (added by
3f1cf6c40): a Clojure script in a Python raw string, run with
`bb -e` at :740 against config/main-flow/shared.edn and
metaflow/<Aspect>-<Topic>-<Layer>.edn; it carries the contract checks
(template is a string containing {{modules}}, {{handover}},
{{raw-psyche}}; sources non-empty). Proposal 2's first_prompt.clj is
that script moved to a file, with Malli for the checks and EDN on stdin.
The audit's live list does not include claude-native-seat-refresh.py.

Flow ids and native session ids (secondary-first.mjs:12–13) are run-time
registrations, not authored values; Proposal 3 offers choices 3–4
instead of showing them in EDN.

SKILL_VARIABLES.md names no variable for the Primary workspace;
the `workspace: '/home/li/primary'` value (claude-main-flow-launch.mjs:91)
is therefore not shown; a launcher's workspace is the repository its EDN
sits in.

Figure: the 4 live sh are messenger-clj nix/launcher.sh,
~/.claude/hooks/herdr-agent-state.sh, ~/.codex/herdr-agent-state.sh
(hooks) and ~/.claude/statusline.sh (the statusLine renderer).

Proposal 1 groups: group one (launch chain, 12 files) and group two
(hooks, committer, census, 8 files) are the 19 .mjs and 1 .py rows with
:live true in the audit.

## Revision 3 (the Secondary's re-audit of Version 3)

Lines moved out of the page: «Of 34 live files, 10 are Clojure, 19
.mjs, 1 .py, 4 sh.»; «The startup prompt is in EDN today; two readers
read it, one .mjs and one Clojure script embedded as a string in a
.py.»; «Of the 58 values: 20 absolute paths, 14 model names, 13
prompts, 8 skill lists, 2 flow ids, 1 hook path. Two kinds below; the
rest follow the same shape.»; «The three proposals above drew from
records and an audit; none is cited on this page.» All counts are the
audit's :totals (above).

The .py caller (tools/claude-native-seat-refresh.py:736–742) sends JSON
on stdin and two EDN paths as arguments; first_prompt.clj now takes
exactly that (cheshire, variadic paths through values/config).

Authored machine module: /git/github.com/LiGoldragon/field-context/
skills/compensation-book-crystallization.md L14 (the generated copy is
.claude/skills/compensation-book-crystallization/SKILL.md).
compensation-relaying-the-living L6 «Quote the living's words
verbatim.» is scoped to «Living words are passed to another flow»; a
book is not a relay; nothing added.

## Revision 4 (the Secondary's re-audit of Version 4)

Counts moved off the page as sentences: «the 20 non-Clojure live
files» (File: label), «the 58 values» (P3 heading), «The 13 prompts»,
«The 2 flow ids» (group headings). Counts inside the figure and the
choices stay. The caller's change (claude-native-seat-refresh.py:740)
is shown red/green; the installed-executable pattern is messenger-clj's
nix/launcher.sh (exec bb --config … ); malli 0.18.0 is the version in
field-clj/deps.edn and messenger-clj/bb.edn.
