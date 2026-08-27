# Kinds

## Qualifier form; Kind is the word; a kind is a trait; no generics in Ethos

2026-08-26, the psyche, typed (answering the surfaced tension "infinitive vs qualifier trait names"):

> 1. qualifier. Write isnt a kind. we say kind now, not trait. declare a new kind = declare a new trait, in Ethos world, which will imply some things which arent in rust world (tbd). so in Ethos there are no generics, only kinds.

## Capability is a function a kind has

2026-08-26, the psyche, typed (answering the surfaced tension "'trait' disliked, no replacement sealed"):

> 4. capability will refer to the actual functions a kind has (Runnable would be the Kind, run would be a capability)

## The kind syntax proposal is inappropriate; start from the anatomy of a Rust trait

2026-08-26, the psyche, dictated, on the four-section kinds/capabilities proposal f426777b had shown:

> Your kind syntax proposal is very... is completely inappropriate. So start by looking at a rust trait, which is what our kind essentially becomes, and in its most complex form, and doing the anatomy of a rust trait. And then you'll see how many different kinds, how many different types of things are in a trait. Which means you're almost, I'm like, I can guarantee you that you're going to need a struct to fit it all in. Or maybe even a root enum to differentiate between different kinds of kinds or different types of kinds or maybe an enum in the struct or like we'll look at different possibilities for essentially to maximize elegance, the elegance of the syntax and yet achieve the level of expression required to express any different kinds that we might want to express.

## A kind's identity must mirror Rust's: name and constraints

2026-08-26, the psyche, typed, on the Rust-trait anatomy presentation (reports/rustTraitAnatomy.md):

> important: in rust, a trait is identified by its name *and* constraints. How would we want to mirror that?

## Identity head preferred; existing Rust traits perhaps kept as-is; capabilities need real thought

2026-08-26, the psyche, typed, on the identity mirrors and the (d) shape presentation:

> I prefer
>
> Processable<[Clonable Sendable]  Serializable>
>
> what did I say about the <> syntax in ethos?

On `[Output.Serializable  Ref]   associated kinds`:

> do you mean associated types? What is Ref? If we want to refer to existing rust traits in the non-verbal way, we'll have to maintain a table for conversion. but that will incure a cost. it might be better to keep the existing trait as-is

On `[process.Output  fetch.Output  validate.Boolean]   capabilities`:

> You havent actually thought about this I can tell. Give it a serious shot. Maybe you need to start with the anatomy of a trait function signature (a capability)

On the section "Where the interaction fills the position":

> I dont understand that section. look like quackery

On the question whether "constraints" meant positions or also superkinds:

> dont worry, you understood what I meant; the identity parts of the data.

> We'll come back to what I havent addressed.

## A struct always has the same fields in the same order; a capability struct is one type

2026-08-27, the psyche, typed, on the capability shape presentation (reports/capabilityAnatomy.md):

> lots of quackery there.
>
> you seem really confused about ethos design.
>
> a struct {} always has the same fields, in the same order. the struct definition declares the field types, so they can be anything; there are no restriction in which type a field can hold!

> so if we use a struct for the capability, it's always the same struct type! it cannot change in number of fields!
