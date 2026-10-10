# Language web — item 39 review proposal

Status: proposed vocabulary relationships, not adopted names or wire identifiers. No installation or executable proof is claimed.

## Keep meanings attached to their sources

A node should hold a language, script, lemma, a particular sense, source reference and review status. An edge should say whether the senses overlap, are broader/narrower, or merely offer a useful metaphor. Sharing a translation does not make two words interchangeable. The source reference may be interned; repeated events need only its typed identifier. String storage is deliberate here because spelling and sense are the substance of the record.

| Language | Candidate | Grounded sense | Proposed use and limit |
| --- | --- | --- | --- |
| Latin | machina | Contrivance or machine; also figurative device or plan | Mechanical or constructed aspect; does not itself mean an intelligent person. |
| Latin | persona | Mask, dramatic role or character, and person | A role presented by an agent; no claim of personhood follows. |
| Spanish | persona | Person, with a dramatic-character sense | Human-facing role terminology requires care because its ordinary meaning is a person. |
| Spanish | personalidad | Distinguishing qualities of an individual | Candidate for behavior or character, distinct from the individual itself. |
| Sanskrit | yantra | Machine, instrument or contrivance in the indexed dictionary entry | Candidate lexical node only; a complete phrase for the proposed system remains unreviewed. |

Latin senses come from the digitized Lewis and Short entries for [machina](https://classics.andrewgadsden.com/lewisandshort/entry/n27468) and [persona](https://archli.com/dictionary/lewis-short-latin-dictionary/persona-166016). Spanish distinctions come from the RAE entries for [persona](https://dle.rae.es/persona) and [personalidad](https://dle.rae.es/personalidad). For Sanskrit, the search index points to the Cologne Monier-Williams [page 845 scan](https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/MWScanpdf/mw0845-yadIya.pdf); the PDF yielded no extracted text and the screenshot request timed out. This is an indexed-entry lead, not a visually verified Sanskrit scan.

## Review choices

Keep Persona, Flow and existing component identifiers unchanged. Offer the language web as explanatory material beside them. The model-proposed Spanish phrase “personalidad de la máquina” could describe behavior, but it is not a dictionary-attested technical term or an adopted project name. Do not assemble Sanskrit compounds from English glosses; obtain linguistic review first. Likewise, do not declare the user’s Latin-inspired wording an established grammatical expression without review.

A first acceptance review should choose the intended sense, then approve individual edges. A later executable proof can test that ambiguous senses remain separate and that every approved edge retains a source and reviewer reference. No such implementation or Nix check exists in this document.
