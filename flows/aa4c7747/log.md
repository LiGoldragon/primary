# aa4c7747 — software-design and Ethos zero design

Ethos zero: version zero of the ethos nexus, bootstrapping ethos in the
nexus trinity stack (ethos, nomos, logos), written straight as a Nexus,
bootstrapped by ethos-cc (the renamed ethos-monolith; the literal
compiler-that-compiles-the-compiler reading holds). High-level anatomy
round shown: demand chain SourceLocations/EthosFiles → SourceIndex →
ResolvedComponent → AssembledRust → RustGeneration, interactions table,
example interface.ethos in the witnessed fixture dialect.

Settled this flow: tuple rule stamped — no tuples in the code we design,
contact points only; the software-design skill splits into High level
design / Implementation invariants / Standard Nexus architecture, with a
real design as the example; Ethos trait implementations are
"interactions" and use the qualified type; Ethos trait syntax is
declarations only — body syntax and its generation are not MVP; agreed
design rounds print dispatches referencing psyche records to Codex flows
for vertical-slice implementation on a new repository.

Settled also: carrying declarations name the real trait — TryFrom is
written TryFrom, no Create alias; the carrying check is the plain
const fn-pointer idiom plus #[diagnostic::on_unimplemented] on
generated traits (probe-witnessed, no dependency). Flows-skill
main-points wording approved; Curriculum edit and regeneration
dispatched.

Under consideration: carrying declarations (b) — generated Rust holds
types, trait definitions, and build-failing carrying checks, bodies
hand-written; whether generated traits are concrete by default, the
associated type introduced only when one verb has carriers with
different yields.

Incident, resolved: a concurrent session's commits left the shared
jj working copy checked out behind main, deleting this flow's vision/
files from disk and reverting the deployed flows skill; everything
was safe in commit e9dbab8c on main; flow records restored from it;
working copy advanced to main and pushed (f8b4b238 — swept-up
changes committed first, two log conflicts resolved as supersets). Edit-coordination lane CLI
rejects its own skill template (as cff271af also found) — continued
unclaimed.

Open: newtype under the tuple rule; type-first vs verb-first carrying
form; the "every interaction involves its qualified type" line;
concrete-traits-by-default proposal; entry-file
commit-what-you-touch line (approved, landing dispatched);
5abf3be8 syntax triage; software-design concept walk continuation;
vocabulary shortlist ruling.

Remembered: cff271af, 68512643, a60a9e85 — depth 1

Rulings verbatim in vision/: tuples, skillDesigning, interactions, ethos,
spokenVocabulary, ethosMonolith, ethosTraitSyntax, dispatches,
basePrompt, sessionLog.
