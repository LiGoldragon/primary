# Protos parsing

Protos parsing always happens inside a context, and only the
current context gives shapes their meaning: it defines which
shapes can appear next and which shape completes it. A met shape
announces a type, and that type's context takes over completely
until its completing shape; then the parent context resumes
exactly where it left off. Reading and writing are one walk in
two directions — text lands in typed values, and typed values
project back into the same text.

---

Provenance: wording Designer-drafted through the two-way
structural transcoding flesh-out
(design/ProtosEngine/twoWayStructuralTranscoding-2026-08-11.md);
approved as Intent by the psyche 2026-08-13T00:19+02:00 ("the
intent is good", Designer session a5587095). The ruling trail —
context-switching parse, the stack keeping the parent's position,
a child context taking the shapes' meaning — is in
psyche/Vision/protosIsTheSharedStyle.md.
