Presentation.{ «Identifiers and names» }

The ids that name a session, a commit or a page: what an id is, how it is written in words, and where it may appear. Small edits to the texts the machine starts its thinking with. Answer with the number, or "yes".

**1. Why words**
vision, vision-identifiers, create
> An id written in words is meant to be used: read, spoken and passed around. Words are cheaper for the machine to read and easier to say and think with.

Rests on: 3 Oct 2026, 15 Sep 2026.

**2. An id is a number**
vision, vision-ethos, edit (add)
> An id is a number of its own type, not a string. Inside a Nexus it stays a number. Turning it into letters or words, and back, happens at the edge, when it is written out or read in.

Rests on: 15 Sep 2026; 3 Oct 2026.

**3. How a word id is made**
vision, vision-identifiers, edit (add)
> A word id is the first 33 bits of the id the harness gives a session, written as three words from the 2,048-word wallet list, joined in camelCase with the first word in small letters, as in abandonAbilityAble. It can be turned back into the bits, so a tool can find the right transcript.

Rests on: 3 Oct 2026, 15 Sep 2026. Answer a number instead if you want a different list size.

**4. Collisions**
vision, vision-identifiers, edit (add)
> If two sessions share the same words, the tool returns every match and he is told. 33 bits is for local use; larger sizes are left for later.

Rests on: 3 Oct 2026, "I think it is enough entropy."

**5. Where the library lives**
vision, vision-ethos, edit (add)
Text 1:
> One generic word-id library for hashes of any size lives in an Ethos core library.

Text 2:
> It lives in an Ethos standard library.

Text 3:
> It lives in the Signal library.

Rests on: 15 Sep 2026 (Signal) against 3 Oct 2026 (a library all components reuse).

**6. What a title is**
knowledge, knowledge-flow, edit (replace the pane title line)
Text 1:
> A title is aspect, layer and six characters, as in psyche secondary 6f51ad. Words replace the six characters in a later version.

Text 2:
> A title is aspect, layer and word id, as in psyche secondary abandonAbilityAble. No name is changed until the word library exists.

Either way: a title holds no state, and the name is the same in the pane, on the remote and in the list.

Rests on: 3 Oct 2026 ("minimum viable product first") against 3 Oct 2026 ("This looks perfect"); 24 Sep, 26 Sep 2026.

**7. Addressing by lasting name**
knowledge, vocabulary, edit (flow identity)
> A voice is reached by its lasting name, aspect and layer, written psyche.primary, which carries over when one session hands over to the next. The flow id belongs to the ledger and the archive and to finding a transcript. A voice is a variant holding a variant, not a chained name.

Rests on: 2 Oct 2026, 3 Oct 2026. Yes also settles the dot against 6 Aug 2026 ("that is scrapped").

**8. Where a hash may appear**
operation, behavior, edit (add)
Text 1:
> A hash never appears in what voices send each other, in a launch prompt, or in anything shown to him. It is stored in full only in the ledger, the archive and the transcript stores. Six letters, or three words, may appear when a transcript must be found.

Text 2:
> The same, but only voice names appear, and the reader looks the session up itself.

Rests on: 1 Oct, 3 Oct 2026; 21 Sep 2026 ("only using shortened hashes where necessary") against 2 Oct 2026.

**9. Six characters for commits and artifacts**
operation, compensation-messenger-clj, edit (replace "at most six characters")
> Commits, published pages and other artifacts carry six characters as their name until the word library is in place, then three words. A commit names the larger piece of work it belongs to, and never carries the full id.

Rests on: 1 Oct 2026, 18 Sep 2026.

**10. A refreshed voice**
knowledge, knowledge-flow, edit (remove)
> Remove: a refreshed voice is named "of" its ancestor and the ancestor's id. The ancestor stays in the ledger only.

Rests on: 18 Sep 2026 against 2 Oct 2026 ("addressable by their continuous name").

**11. Subflow names**
knowledge, vocabulary, edit (subflow)
> A subflow is named by its job and a count, second, third, and has no word id of its own.

Rests on: 17 Sep 2026.
