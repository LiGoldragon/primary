# protos

## 2026-09-08 — the guillemet, freed by abandoning maps, should delimit strings; the curly quotes look too much like the usual double quote

Said fresh, while a distillation of datom, ethos, nexus, sema, and signal was being composed:

> I just had a really interesting thought, which is that, because the curly quotes look so much like whatever the usual symbol is that almost all programming languages use for strings (is it the double quote?), and because the guillemet looks like a double angle bracket, it has been freed by [STT: from] abandoning maps. I think we should use the guillemet for strings. Bounce that back to me if you understand it, and what do you think of it?

-- psyche, STT.

## 2026-09-08 — the guillemet keeps the doubleness of the double quote but cannot be mistyped for it, and its direction shows where a string begins and ends

Answering the flow's read that the guillemet resembles nothing in mainstream languages:

> Well, the reason I was saying to switch for the guillemet is not that it does not look like you say it resembles nothing in mainstream language. Actually, that's not true, because if anything, there is that doubleness there, which actually does look like the double quotes, but it's not. That way, somebody would not, by mistake, use the wrong character. You see what I mean? It would be harder to make a typo and use the wrong delimiter for a string with the guillemet, and it also is visually easier to see where it begins and where it ends.
>
> The curly quotes are very hard to differentiate, especially if the font is small, where the beginning, the opening half, and the closing half are. This is what happened when I was on my phone, which has really small fonts, and I couldn't see the beginning. I had a hard time seeing which one is the beginning one and the ending one. Actually, I couldn't even tell the difference, whereas the guillemet looks more like a delimiter. It has the direction that's way more clear, so that's essentially why. It still kind of looks like a string delimiter from that cognitive reusage. It's still kind of there with the doubleness of it, but it has more of a direction. I think it's perfect. It's exactly what we need for the string.

-- psyche, STT.

## 2026-09-08 — protos has no types, only structure; the change to protos is that the curly quote is no longer a delimiter, and that is as far as it goes

Answering the flow's question whether the string change is protos-level:

> So, you're asking if that's Protos level? That's a misunderstanding of what Protos is, because Protos does not have types, yet it only has structure. In the sense that, yet, do we abandon the curly quotes? Yes. In the sense that it does change Protos because now the curly quote is not a delimiter anymore, but that's as far as it goes, essentially, for Protos.

-- psyche, STT.

## 2026-09-08 — parentheses are not opaque; they are unspecified, treated as opaque until specified

Answering the proposed delimiter table that listed `( )` as opaque:

> () isnt opaque; its still unspecified, so treated as opaque until it get specified.

-- psyche, typed.

## 2026-09-08 — parentheses are reserved for meaning; the meaning type is what has not been specified

Answering the proposed row "( ) is unspecified":

> Well, it's not exactly that the parentheses are completely unspecified. We know what we want to use it for, but that `for` has not been specified. The meaning structure, the meaning type, has not been specified, but it is reserved for that.

-- psyche, STT.

## 2026-09-09 — textualization is a chain of conversion: corpus to concept to structure to text; does the structure hold all the data

Thinking out loud, asking the flow to verify:

> Okay, I'm thinking out loud here, and I want you to verify if what I'm saying makes sense. If we have a Datomizable kind, then that's not what implements textualizable, because the textualization comes from the structure. No, wait, this is interesting: you need every type successively. You need the concept and the structure to get the text, or do you have all of the data in the structure, meaning you only have to implement this structure? It would have to be textualizable, like you have a chain of conversion: you go from the corpus to the concept (which, in this case, is the datom) to the structure to the text.

-- psyche, STT.

## 2026-09-09 — the protoform is what implements Textualizable, not the datom; a conversion chain changes type, so the original type cannot be said to implement Textualizable

Answering the flow's account that Textualizable lands on the corpus type through a protos blanket:

> No, I think we're not understanding each other here. There is a type, the proto type, which is the structural layer, and that's the type that is Datomizable. For a Datomizable type to become text, it has to first be converted into a prototype which implements Textualizable, and not the datom itself.
>
> I know you push back here, but the way I see it, it's not the datom that implements Textualizable. It's the prototype, which is another type. There's a conversion chain. That's what I said earlier: we have a chain of conversions so that we change type. If we change type, we can't say that the original type implements Textualizable, because what gets converted into text is the prototype, not the datom type.

Context: "prototype" here is the protoform, the structural layer's type. The flow reads the first sentence's "that's the type that is Datomizable" as naming the Datomizable type's counterpart in the chain: the corpus type is Datomizable, the protoform is Textualizable.

-- psyche, STT.

## 2026-09-09 — text is above, the Rust value below; down is density, up is visibility; the textual form can be written on sand, the binary form is stricter and denser

> Well, in my mind, I was putting text above and then a Rust value at the bottom. Is that not the canonical way to think about serialization and deserialization? Did I have it backwards? Should I say the text is at the bottom because, to me, the text is the least dense, and then down is density? Down is the earth, up is the sky. When you go up, you lose density, so it becomes easier to read. It's more visible. It's more large, right? The sky is easier to read because you can see way more of it than the earth.
>
> The Datom textual form can be written with a pen on sand, but if you try and write the binary form, it's a lot more strict, so it's more dense. It even takes less space.

-- psyche, STT.
