# Flow e4a40e

Design flow. Opening word: remember 4decf7 at depth 1; its design/proposal1
texts and reports/ethosObjects.md are the starting point, nothing there needs
regathering. Continue distilling as we go: bring the unapproved parts of
proposal 1 to approval, then the situated examples asked for last (a plain
type, a plain kind, a plain kind association, the signal type, the Nexus
type, the sema type, the mixed type whose vector of variants each declares
its own object root). Nexus and sema are not designed yet: propose their
anatomy from the living's words in that report and ask what is not ruled.

Correction from the living, first turn (instruction, not vision): the
main flow located flow 4decf7 itself with ls, git log, git ls-tree and jj
log; locating is subflow work. Sentence that led to it: the main-flow
skill's "For every other read, use a small read-only subflow to locate
the file if needed", read as governing file reads only. Line proposed
for the main-flow skill and approved by the living verbatim ("yes, your
edit is good"): "Locating is subflow work whatever tool would do it:
listing a directory, searching git or jj history, grepping an index. The
main flow runs a shell command only for `flow-id` and for the writes it
owns." A trivial worker was dispatched to land it in the Curriculum
source and regenerate.

Witnessed before the correction: flows/4decf7 was absent from the
working tree; commit f3e67f844 ("Commit dirty tree from prior flows")
deleted every file of it; its parent f82cde9b0 carried all but
reports/ethosObjects.md, which sat only in two jj changes off 92366ee91
never on main (032ce4805, 1d7a48a0f).

Remembered: 4decf7 — depth 1. A read-critical subflow restored all
fifteen files as commit 16c7b194 on main (fourteen from f82cde9b0, the
main-line versions with the contextualization block, revisions 4 and 5
and every situated example; ethosObjects.md from 032ce4805, which is its
only source). The deletion carried no intent; it was a side effect of
jj moving the files between changes. Approved and landed from proposal
1: Vision/kinds.md, the Kind and Naming blocks, on the living's word
"Anything that I've read past that I haven't commented on is accepted."
Unapproved: kinds from Identity onward, and all of protos, datom, ethos
and distillation. The living's objection at Identity: a kind is not
accurately "identified by its name, its constraints"; be exact about
which parts identify a kind. Corrections given, not yet approved as
revised text: "might imply more"; examples with no Rust standard; no
conversion tables; ethos beside every Rust example; every example
situated; contextualization and the types of ethos objects as one of the
most basic explanations in the vision. Left pending by 4decf7's last
substantive response: the Identity question (positions alone, their
number and order, or also the kinds they require); the Nexus and sema
shapes, promised once the gathering returned but never proposed; the
import separator; the skill lines in revisions 3 to 5. The living's
words on Nexus and sema in ethosObjects.md: neither ethos is designed
yet and both will live in the Nexus's main repo; universal Nexus traits
as the basic ontology of an actor/dataflow system, designed as if for
the first time; the point of authoring Nexus in ethos is to see its
main operations; sema is the database engine, exposing the types the
database stores; "try from" is the wrong way to think of an object going
into the Nexus for an effect; PathLockRegistered.try_from.registration
is too many heads in a row, unrefined; a storage type declaration for
the sema file type and a specialized type for Nexus declaration files,
"all just to be decided".

Skill line landing (relayed from the write-trivial worker, not
witnessed by the main flow): the approved line landed in the
Curriculum source skills/main-flow.md, commit 9fe559994c; primary
commit 16c4186ae bumped flake.nix and flake.lock to it; both pushed.
Two departures from the brief: the worker also changed wording it was
told not to touch, "parent/child" to "main flow/subflow" across
main-flow.md and child-flow.md, saying it matched the generated
output; and regeneration failed with `DatomFault { problem: Shape }`
from curriculum-deploy, so the generated trees do not carry the line.
Raised to the living with a proposal to revert the extra wording and
investigate the fault.
