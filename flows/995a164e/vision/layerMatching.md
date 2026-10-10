# Matching structure to concept

## The constant roster misses the whole point: no separate data table; go through the enum, variant by variant

Context: artifact comment on the recap's `const ROSTER` block
(2026-08-31 11:49). The psyche stopped reading the report here.

> Somehow, you didn't understand what I meant at all here. By merely putting a constant roster, you're showing that you didn't understand what I meant when I said that the whole point of doing this capability-based structure matching logic is to not have a separate data table. It just becomes like a parallel data structure to the data which actually lives in the capabilities of the kinds, so you're showing that you've missed my whole point and you somehow didn't understand. This means it's telling me that we need to have a further discussion on how this would actually look, even just at a high level, without necessarily thinking too specifically about this particular way or this particular implementation of the concept that I'm talking about, which is to go through the enum.
>
> Essentially, it would just take the top-level enum that contains all of the embodiments of that layer, and it would go through the variants one by one. In that way, it would get all of the data. I don't know if what I'm trying to say is not possible in Rust, or if we have to maybe go deeper in understanding how Rust works to make this possible. The mere fact of presenting a constant in relation to this shows that the concept hasn't actually been understood.

-- psyche, typed (artifact comment).

## "The data is in the capabilities" means the trait implementations, and only them; no constant

Context: terminal, after the comment above.

> When I say the data is in the capabilities, you don't really understand that I just mean the trait implementations, right? That is the only thing that is involved in obtaining that data. There's no constant. There's not gonna be a constant. You're completely missing my point. You're actually making the parallel data structure that essentially repeats the data that would already be, or that must be, in the capabilities. It's specific to these embodiments, and therefore it must live in their capabilities.

-- psyche, STT.

## Unstable Rust is fine; the check is at compilation, not generation; an associated constant in each kind holds its forms; think in an actual type, even a throwaway instance

Context: terminal, after the flow claimed stable Rust cannot call trait
methods in const evaluation and moved the no-conflict check to
generation time.

> Okay, you say that stable Rust doesn't allow calling trait methods during constant evaluation. Well, I don't really care about stable Rust, so we can use unstable Rust if that fixes it, but I'm not sure I even believe you. Maybe you don't really understand what I want.
>
> Obviously, you can't call traits directly. You need a type to call the methods on. You need to think about it in terms of using an actual type and an actual instance of a type, I guess. Even if it's just a temporary throwaway instance to run this check during compilation, we're going to find a way. I know we're going to find a way, even if it's from generating the rest [STT; Rust] from ethos, where we had a kind of check somewhere in the logic there, but I would leave that for last resort.
>
> No conflict should be done at compilation, not at generation. There's no reason to do it at generation. It's kind of ridiculous because we have a limited set. This conflict can be checked without actually feeding any ethos to generate from. It's going to be in the logic of the length of the runtime [transcription uncertain] whether or not there's a conflict, so we shouldn't postpone the conflict check until we're running the execute code. That's absurd.
>
> There is going to be an associated constant, possibly in each kind, to hold the value of its forms or whatever it is.

-- psyche, STT.
