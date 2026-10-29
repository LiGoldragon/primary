Archived on landing: distilled into Vision/ethos.md (Declaration), flow 6329f1, 2026-09-04. The content is carried there; the words are kept here.
# Ethos

## 2026-09-04 — the file is the sweet form; the braced form is canonical; the sweet form is converted before the text is read

On the proposed Declaration's File section, which called the braced `Library.{ … }` the sweet form:

> You didn't understand that the ethos file is the sweet form, and the second version, where it's `library.` and then it opens `{}`, is the canonical form, the non-sweet form. You have them backwards, and in order to keep the pipe clean, the suite [STT: sweet] file form of ethos should be kept out of the main logic run. It should be done as a pre-step before we even get to text, so that, essentially, an ethos file, we just do not consider it text yet. It should be converted mechanically to the proper text form before we proceed.

-- psyche, STT.

## 2026-09-04 — proper ethos is variant-headed, a struct with its version and fields: kinds, types, signal, sema variants with implied kind associations

> That way, the ethos parser uses proper ethos, which is variant-headed and is a properly defined struct with its version and all of its different fields. There would be:
>
> * a `kinds` variant, which only holds kinds
> * a `types` variant, which only holds types
> * a `signal` variant, which holds certain specialized types that automatically have kind associations
>
> You would have a query type and a response type, and these would each have their own respective implied associations, implied kind associations. The same would be true of a sema ethos type, which would have a storage type or a record type (whatever you want to call it) that would have associated kinds, implied associated kinds.
>
> It's sort of just a shorthand syntax. Instead of just manually always adding the associations, it's just implied because these types always need to implement those kinds in these ethos variants, essentially different kinds of structs.

-- psyche, STT.
