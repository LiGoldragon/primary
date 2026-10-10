## 2026-08-22 — a toy is not a good example; the proposed toy replacement is quackery

Design session `bc05da32`, typed (captured 2026-08-22), on the logos
snippet in the software-design draft — a toy grammar
(`#[token("fast")] Fast`) lifted from logos's own README — and on
the Designer's proposed replacement, another invented toy grammar
(`let x`):

> a toy is not a good example

> your example is quackery

Context (agent-authored, separate from the psyche's words): both the
draft's logos README snippet and the Designer's invented substitute
are rejected. A demo grammar written to demonstrate a library is not
an example; an example is real, witnessed code from real software —
continuous with machineAnatomy.md 2026-08-21 (mine existing projects
for examples). The draft's snippet entered via
DesignExemplars-Rust-2026-08-21.md §10. Replacement to be drafted
from a witnessed production logos lexer, or the example dropped.

## 2026-08-22 — a skill is not a history book

Design session `bc05da32`, typed (captured 2026-08-22), on the
software-design draft's "Backwards from the want" passage
attributing the doctrine to SICP's wishful thinking and Kent Beck's
output tape:

> The content there can be good, but this is a skill not a history
> book

Context (agent-authored, separate from the psyche's words): the
content survives as instruction ("Write the core as if its coherent
inputs already existed; then ask what produces them"); the
attributions move to the draft's provenance file. Read together with
the approved example style: real machines cited as evidence (GCC,
bat, ruff, syn, serde, walrus) are examples; lineage and survey
narration are history. A skill-designing cut-list line is proposed,
approval-gated per 2026-08-19: "A line that tells where an idea came
from."

## 2026-08-22 — the taplo replacement isnt logos: quackery again; an example must be what it is presented as

Design session `bc05da32`, typed (captured 2026-08-22, after the
history-book ruling), on the taplo SyntaxKind excerpt that had
replaced the logos toy in the software-design draft:

> Well, that isnt logos, so it's quackery

Context (agent-authored, separate from the psyche's words): confirmed
by the witnessed source — taplo's SyntaxKind is a CST node vocabulary
(`repr(u16)`, unattributed KEY..ROOT variants the parser constructs)
with logos derived over a subset, and its callbacks carry grammar
outside the enum. The Designer's trim had cut the unattributed tail
and claimed "the grammar never leaves the enum" — presenting the
specimen as the pure form it is not. Replaced with protox-parse
Token (every variant attributed, witnessed at commit 8da89091), the
callback boundary stated honestly in the draft.

## 2026-08-22 — one crate per example block; syn File cut: logic may be good, naming is bad; a better example ordered

Design session `bc05da32`, typed (captured 2026-08-22), on the
draft's positive-model block holding syn and serde impls together,
and on syn's File after the emitting-misreading exchange:

> dont mix examples from two different crates in the same block.

> re syn File: seems to me they used the wrong name. Their logic may
> be good but their naming is bad. We need a better example.

Context (agent-authored, separate from the psyche's words): the
mixed block is split — serde Value stands alone as the positive
model. syn File is cut from the draft: the placement logic (no
parser service; each type declares its own creation) may be good;
the name File is not — it names the value's textual origin, not
what the value is at the moment it exists, and it misled the psyche
into reading emission. A replacement creation-side example with
truthful naming is hunted. Example rule carried forward: one crate
per code block.

## 2026-08-22 — cut the bad example: the lexer-crate example leaves the software-design draft

Design session `bc05da32`, typed (captured 2026-08-22), green on the
Designer's recommendation after the hunt returned both replacement
slots empty:

> cut the bad example and explain the macro options

Context (agent-authored, separate from the psyche's words): the
lexer-crate example (README toy → taplo → protox-parse) is cut from
the draft — the crate's name collides with our Logos and no
non-colliding machine-from-the-type's-shape specimen was found. The
witnessed trail stays in the exemplars report. Better examples to
come from our own software as it is built (machineAnatomy.md
2026-08-21).


