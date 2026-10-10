# Testing

## Never search production code for a string; test by trace in normal running
> There should be a test that makes sure somehow, not by wrapping the code: do not just fucking search ever. Do not ever search the code, the actual code, the production code, for a string.
>
> You have to test. This is basic testing skill: how to write tests. You never actually search the code, the actual code, the production code, for anything string-wise. You can trace. You can use trace systems with a developer build that has tracing built in to know that this function gets called if you use the system in a normal condition. You can't just run it with a dummy nonsensical load or just run build, compile, and run just a small part of the code.
>
> You have to run the whole system in the normal condition and if you get the trace that you expect to be running this function, maybe even in a particular order, then your test passes. We need complex trace, not complex tracing, but we need to know how it's running in a normal way and not just search the code. That's how we know.

-- psyche, STT, 2026-10-07.
