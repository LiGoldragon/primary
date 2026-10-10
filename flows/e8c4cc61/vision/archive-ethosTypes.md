# Ethos types

## Specifying a type inline

Context: the handwritten Ethos File Anatomy page,
`GenerationFailure.[SyntaxError.Vector<FilePath> ...]`.

> But one thing that I did do, and I have been doing, is to specify a type inline, so to speak. So you can see in the responses, we have, for example, generation failure, which is an enum because it then follows a bracket, right, which has all the variants in it, and the first variant being syntax error dot vector.
>
> So I'm specifying a new type inline. Instead of just saying syntax error and then importing syntax error from a library, I'm saying syntax error is a vector of file path. And that is something that I want to allow in ethos ... it's up to the writer really to decide if he wants to create a new type somewhere else or if he wants to just do it inline, then he can just do so.
>
> It's a syntactic sugar that allows him... So that these types will essentially become full types of their own and not something minor.

-- psyche, STT.

## A variant named as an already defined type is a data-carrying variant

> So the syntax error object, right, could just be by itself with no following dot. And in the import, it could say syntax error, and that object would be described in the library, and it could say syntax error dot vector file path.
>
> So there's another mechanism there also, which is when a variant is actually an already defined type somewhere else, we can just say syntax error, for example, and if it was specified somewhere else in the library, the same name, syntax error, then the ethos runtime has to make the leap and understand that syntax error is actually a data carrying variant.
>
> But there's no need to write syntax error dot syntax error data. We don't need that syntax. That's just repetitive, and from a logical point of view, there's actually no need to create that repetition. All that's needed is for the runtime to find out that syntax error is actually an already defined type, which means that this becomes a data carrying variant.
>
> And like I said, it can also be declared inline. It can declare the type of data that it carries inline by just saying syntax error dot vector, or it could be a full struct, or it could be another enum by using a bracket and then declaring the variants [STT: variance]. And then those variants [STT: variance] in turn could also be declared inline or refer to an already existing type by name, which would make them data carrying variants [STT: variance].

-- psyche, STT.
