# Nexus

## A standard entry point that enforces the nexus's three parts

> I want to talk more about how a nexus has three parts and make sure that it is effective and that we use maybe even some kind of standard main flow, like a macro in Rust, as some way for the whole machinery to enforce its own invariance so that the rest doesn't bypass it.

> That has been an idea of mine that I've been trying to put into practice: if we use something like a macro or a standard entry point for the main executable or the entry point of the library (or whatever it is), then we can control some properties of the system. For example the idea is that the signal has to go through the operation actor/system in order to reach the memory actor/system, then back through the operation system and back out through the signal. That way we can see the main objects and processes that are involved by just looking at the ethos code, which defines the types that are involved in this flow.

> If that can somehow be enforced in Rust through the way we write the Rust and then we leave the implementation side to be written by hand, then you can have effective compliance with ethos.

-- psyche, typed.
