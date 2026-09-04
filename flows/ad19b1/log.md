# Flow ad19b1

Design flow. Opening word: remember e4a40e at depth 1; continue
distilling as we go, showing the distillate and where it goes, in the
topic's own language, with elaborate examples and no single-field
structs. Datom landed. Still to approve: datom Meaning, kinds Identity
and Declaration, ethos, distillation; protos set aside. Then the
situated examples, and Nexus and sema anatomy from the living's words.
The opening restates rulings already logged in e4a40e (distillation,
newtypeWrappingAndSingleFieldStructs) as working instructions; nothing
new in it is vision.

Committed first, as its own commit: flows/78c93c/vision/witness-reuse.md,
found untracked in the tree (0cdd7aba0).

Remembered: e4a40e — depth 1. Witnessed on disk at this flow's start:
Vision/datom.md carries the approved blocks (Name, Nature, Repository
and migration, The interface shape, De/serialization, Relation to
Ethos, Syntax with the Person example and the Reply, map and vector
examples) and the Meaning block as it stood before, unapproved;
Vision/sources/datom.md lists thirty sources ending in e4a40e datom,
vocabulary, newtypeWrappingAndSingleFieldStructs; flows/e4a40e/vision
holds archive-datom.md and archive-vocabulary.md beside the live
distillation, kinds, newtypeWrappingAndSingleFieldStructs, protos and
witnesses records. Relayed from e4a40e's log: Vision/kinds.md Kind and
Naming approved and landed by 4decf7; unapproved from proposal 1:
kinds from Identity onward, ethos, distillation; protos set aside on
the living's offer to talk about it later, its ethos-bearing material
to be distilled with ethos. Rulings heard in e4a40e that govern this
flow's proposals: heads differing in a required kind are two kinds;
what identifies a trait in Rust identifies a kind, no decision
involved; a single-field struct is really bad design; elaborate
examples, explained properly; datom vision shows datom, never ethos
syntax; a proposal shows the distillate as it will stand and the topic
it goes to, no diff, no before text; fresh words keep being logged as
raw records; "block" is rejected, structure is the word; a head is a
qualifying subset of bare text, the rule unstated. Witnessed by
e4a40e's probe: Rust refuses two same-named traits in one module and
holds them as two traits in two modules, bounds never in the path.
Still pending from 4decf7: the situated examples (a plain type, a plain
kind, a plain kind association, the signal type, the Nexus type, the
sema type, the mixed type whose vector of variants each declares its
own object root); Nexus and sema anatomy, never proposed; the import
separator. e4a40e's last response graded its landing subflow: tier by
thinking needed, not by cost of a mistake. Seen in the tree during
this flow's setup, committed by another flow: the child-flow skill
renamed subflow (388f6fc29), and this flow's index entry committed as
dirty (070a4242b).

Gatherings for the four distillations (relayed from three read
subflows; the first two attempts on the default model were cut by
server overload, HTTP 529, and relaunched on another): 4decf7's
proposal1 texts for datom Meaning, kinds, ethos, distillation and
protos; the raw records on kinds, ethos and distillation named in the
composite's sources lists; every record on the structured string
across flows and vision-raw; e4a40e's last-presented Identity (line
290 of its transcript: identified by library and name, as a Rust
trait by its path) and Declaration (line 249, presented once, read
past without comment); the revision history of proposal 1. Read
directly by the main flow: a5587095 structuredStringType, whole.
Distillation order: datom Meaning, kinds Identity and Declaration,
ethos, distillation.

Meaning landed (relayed from the write-ordinary subflow, witnessed by
it by diff): commit 5c5f75977 replaces the Meaning block of
Vision/datom.md with the approved text and its three examples, appends
eight sources, archives a5587095 structuredStringType (its research
direction destroyed as an impurity), 01a03eda datomSyntax and this
flow's meaning record. The living's rulings on the way: no more
MeaningOrString, strings are strings and meaning is meaning; the
sentence on both languages seeing Meaning rejected; "Meaning is
datom". Commits of this flow before this point were made with raw
git; the file-editing skill, loaded now, rules jj from here.
Kinds Identity presented next, with the association form and the
Rust naming rule flagged as read past and witnessed respectively.

The living ruled kind an ethos concept, narrower than ethos: kinds
vision lives in Vision/ethos.md. Identity landed there (relayed from
the write-ordinary subflow, witnessed by it by diff): commit c2ac4cdb2
appends Kind, Naming and Identity to Vision/ethos.md, removes
Vision/kinds.md and Vision/sources/kinds.md, creates
Vision/sources/ethos.md carrying the kinds sources, the four sources of
the 68512643 ethos distillation reconstructed from archive headers,
and the Identity sources; e4a40e kinds and this flow's kinds record
archived. Rulings on the way: a Rust trait is identified by its name
and its constraints, not its path; "position" is a fuzzy word for a
constraint; an ethos example shows its target Rust; the universal
"never carry what you have not understood" line proposed for spirit,
its wording not yet ruled. A conversational remark logged as vision
was removed on the living's objection. Declaration presented next.

Declaration's example approved by the living ("that looks good. the
example that is"); its prose re-shown whole, the landing word not yet
given. Another flow's report, relayed by the living and witnessed by
grep: Vision/datom.md line 151 says "a map of Text to Integer" over a
map whose first value is a string. Three replacements failed in turn:
colon-faked keys, fixed keys that should be a struct, then "think of a
better example", "So you can't think of a credible example?". The
living then questioned the map's existence in datom and asked for
research into those who hold a key-value map to be a vector of
structs. Dispatched to a research subflow, report to
reports/mapMerit.md.

Map research returned (relayed from the research subflow, report in
reports/mapMerit.md, commit 88082a094, 2354 lines, every claim with
author, title, year, URL and quote): the reduction map = set of pairs
is set theory's definition of a function and Codd's footnote 8; the
reverse reduction, struct = map from name to value, is Date and
Darwen's tuple and Castagna 2023; Dhall and protobuf define the map
as a list of two-field records; CPython, indexmap, C++23 flat_map,
Zig ArrayHashMap and Erlang's EEP 43 all store a map as an array of
entries plus an index dropped below a small size; q and O'Keefe's
frames converge on keys vector plus values vector; the strongest case
for a distinct map is key uniqueness as an invariant and the
unordered guarantee; the strongest case for the vector is shadowing
of duplicate keys in alists and proplists; no canonical essay argues
the map away outright, Virding 2013 comes closest. The subflow
corrected premises in the brief: frames is O'Keefe's, not
Armstrong's; flat_map is Laine's; no PEP for the compact dict;
Muratori and Acton do not argue arrays versus maps. Another flow,
c34691, was seen writing in the tree concurrently.
