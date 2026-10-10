# Source-Searching Tests: What the Testing Literature Says

Research date: 2026-08-20. All claims are sourced; inferred content is marked [inferred].

---

## 1. The Failure Family and Its Named Authorities

### The Central Concept: Behavior vs. Structure Coupling

The testing literature has a well-developed vocabulary for the failure family the designer is condemning. The core distinction is between tests coupled to *behavior* (what the system does) and tests coupled to *structure* (how it is expressed in source text).

**Kent Beck** articulated this most directly in *Programmer Test Principles* (Medium, 2019). Beck writes that programmer tests should be "sensitive to behavior changes" and "insensitive to structure changes." A test that pins the literal text of source code is maximally sensitive to structure and yields zero behavioral signal — exactly inverting the desideratum. Beck's formulation: "Tests should be coupled to the behavior of code and decoupled from the structure of code." (Source: search result summary of the Medium article; the article is at https://medium.com/@kentbeck_7670/programmer-test-principles-d01c064d7934 and is paywalled.)

**Ian Cooper**, in the widely-viewed NDC talk "TDD, Where Did It All Go Wrong" (InfoQ, https://www.infoq.com/presentations/tdd-original/), argues that TDD went wrong precisely because practitioners began testing *every class and method* rather than *behaviors and contracts*. His direct statement: "Your API is your contract, your tests should test the API, not the implementation details. Coupling is the first problem in software." He further identifies the trigger for writing a test: "Adding a new class is not the trigger for writing tests. The trigger is implementing a requirement." A test that scans source prose for verbatim text is triggered by source-structure events, not requirement events — Cooper's exact anti-pattern. (Source: https://keyvanakbary.github.io/learning-notes/talks/tdd-where-did-it-all-go-wrong/, read directly.)

**Google Testing Blog / "Software Engineering at Google"**: The canonical named article is "Testing on the Toilet: Change-Detector Tests Considered Harmful" by Alex Eagle (January 27, 2015, https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html). The article defines *change-detector tests* as tests that fail in response to any change to production code even when the behavior is unchanged. It argues such tests provide false confidence, prevent safe refactoring, and fail as documentation. A second piece, "Testing on the Toilet: Test Behavior, Not Implementation" by Andrew Trenk (August 5, 2013, https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html), states: "test setup may need to change if the implementation changes... but the actual test itself typically shouldn't need to change if the code's user-facing behavior doesn't change." A third, "Testing on the Toilet: Test Behaviors, Not Methods" by Erik Kuefler (April 2014, https://testing.googleblog.com/2014/04/testing-on-toilet-test-behaviors-not.html), advocates naming and structuring tests around behaviors — specific outcomes — rather than around the methods or classes they happen to exercise.

**Martin Fowler** (https://martinfowler.com/bliki/UnitTest.html): categorizes unit tests as *sociable* (interacting with real collaborators) versus *solitary* (isolating with doubles). The terminology originates with **Jay Fields**. Fowler's position is that the choice between the two is a practical concern — speed, stability, non-determinism — not ideological purity; but in either case, tests verify *behavior* of a unit, not its text.

**Sandi Metz**, "The Magic Tricks of Testing" (RailsConf 2013, Speaker Deck: https://speakerdeck.com/skmetz/magic-tricks-of-testing-railsconf), produces the most concise grid: for incoming query messages, "make assertions about what they send back" — not about what methods were called internally, and certainly not about the text that produces the return. Her rule for not testing implementation: it "allows you to change the implementation without causing your tests to break."

**Gerard Meszaros**, *xUnit Test Patterns: Refactoring Test Code* (Addison-Wesley, 2007, http://xunitpatterns.com/Fragile%20Test.html — note: site was unreachable at time of research; content inferred from multiple secondary sources that cite the book directly): defines the *Fragile Test* as a test that "fails to compile or run when the system under test is changed in ways that don't affect the part the test is exercising." He enumerates subtypes including *Behavior Sensitivity* (tests that are too tightly coupled to internal behavior) and *Overspecified Software* (tests that specify more about the implementation than necessary). The Fragile Test is the umbrella; change-detector tests are the acute form.

**Fabio Pereira**, "TTDD — Tautological Test Driven Development Anti-Pattern" (2010, http://fabiopereira.me/blog/2010/05/27/ttdd-tautological-test-driven-development-anti-pattern/): defines *tautological tests* as those in which "test setup and assertions nearly duplicate the code being tested, creating a situation where implementation changes automatically satisfy test expectations without validating actual behavior." The anti-pattern is: assert interactions with collaborators rather than outputs; test implementation instead of class behavior; include excessive mock setup that obscures intent.

**Randy Coulman**, "Tautological Tests" (2016, https://randycoulman.com/blog/2016/12/20/tautological-tests/): "Never calculate an expected value to check against within your test. Logic driving the assertions in your test code is always a smell. Never write test code that assumes it knows how the method under test should be implemented." An assertion that a string appears verbatim in source code is the logical limit of this smell: the "expected value" is the source text itself.

---

## 2. Specific Degenerate Forms and Their Names

### 2a. Change-Detector Tests

Named by Google (Eagle, 2015, cited above). Tests that fail whenever production code is touched, regardless of behavioral effect. A grep-style assertion that prose appears in a source file is the purest possible change-detector: it fails the moment any character in the file moves, whether or not the system's behavior changed at all.

### 2b. Tautological Tests

Named by Fabio Pereira (TTDD, 2010) and independently described by Randy Coulman (2016), Mark Sands ("Mocking is Tautological," 2014, http://marksands.github.io/2014/05/14/mocking-is-tautological.html), and the ploeh blog ("Tautological assertion," 2019, https://blog.ploeh.dk/2019/10/14/tautological-assertion/). A tautological test restates the source: the expected value is derived by the same logic as the production code, making the test true by construction and meaningless as a check.

### 2c. Snapshot Tests / Golden-Master Tests Done Badly

Jest snapshot tests capture the serialized representation of a component and fail when it changes. The legitimate use — revealing regressions in output — degrades into *snapshot blindness* when developers routinely run `jest --updateSnapshot` without examining what changed. SitePen (https://www.sitepen.com/blog/snapshot-testing-benefits-and-drawbacks): "snapshot tests don't contain focused, meaningful assertions or expectations. They verify output hasn't changed, but reveal nothing about whether that output is actually correct." Brains & Beards (https://brainsandbeards.com/blog/snapshot-testing/): "There is no place where you can define what you expect in Jest's snapshot approach." When snapshots grow large, they become textual pins against representation rather than assertions about behavior. The literature distinguishes this from *deliberate* golden-master/characterization testing (see §4 below).

### 2d. Mock-Verification Tests / Overspecified Tests

Testing that a specific internal method was called a specific number of times with specific arguments is, structurally, a grep of the call graph rather than a behavioral assertion. Sandi Metz's grid (cited above) explicitly excludes this: for incoming query messages, assert the return value, not the call chain. Meszaros names this *Overspecified Software*. Fabio Pereira's TTDD category covers the same form.

---

## 3. What Respected Practice Does Instead

### Test Through the Public Boundary

Ian Cooper: test behaviors at the public surface; during refactoring, write no new tests for extracted classes. Martin Fowler (sociable tests), Google (test behaviors not methods): cross the boundary with real or realistic inputs, assert real or realistic outputs.

### Characterization Tests for Legacy (Feathers)

Michael Feathers, *Working Effectively with Legacy Code* (Prentice Hall, 2004): a *characterization test* documents what the system currently does, not what it ought to do. This is how coverage is established before refactoring legacy code. Feathers defined legacy code as "simply code without tests." The characterization test is intentionally a behavioral snapshot — not a text snapshot — that is meant to be replaced by proper behavioral tests once the system is understood. (Source: https://www.fabrizioduroni.it/blog/post/2018/03/20/golden-master-test-characterization-test-legacy-code, read summary; Wikipedia characterization test entry https://en.wikipedia.org/wiki/Characterization_test.)

### Property-Based Testing (QuickCheck lineage)

Property-based testing (Claessen & Hughes, QuickCheck, ICFP 2000; Hypothesis in Python; fast-check in JS) replaces "this specific string appears in source" with "this law holds over generated inputs." Laws are behavioral: `reverse(reverse(xs)) == xs`. No source text is pinned. The literature notes that "if the functions of an API satisfy elegant laws, that in itself is a sign of good design." (Source: https://softwarepatternslexicon.com/haskell/testing-and-design-patterns/property-based-testing-with-quickcheck/.)

### Mutation Testing as the Measure

Stryker (JS/TS), PIT (Java), and mutmut (Python) introduce minimal code mutations (e.g., flipping `>=` to `>`), then run the test suite. Tests that do not detect the mutation are functionally equivalent to no test. A text-pinning test that asserts a line of prose appears in the source file will *survive* any mutation to the system's behavioral logic, scoring zero against the mutation suite. The mutation testing literature is therefore the sharpest formal indictment of source-searching tests: they contribute nothing to the mutation score. (Source: https://stryker-mutator.io/docs/, read directly.)

### DAMP over DRY; Behavior-Named Tests

Google Testing Blog, "Tests Too DRY? Make Them DAMP!" (December 2019, https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html): Tests should be Descriptive and Meaningful Phrases, not minimal DRY abstractions. The behavior named in the test title and body is the specification.

---

## 4. Where a Text Assertion IS Defended by Serious People

### Compiler and Code-Generator Output (Rustc UI Tests, insta)

The Rust compiler test suite uses *UI tests*: each test case is a snippet of Rust source; the expected compiler output (diagnostics, error messages) is stored in a `.stderr` golden file checked into git. The `trybuild` crate (https://github.com/dtolnay/trybuild) and `ui_test` framework (https://github.com/oli-obk/ui_test) formalize this. The `insta` crate (https://insta.rs; https://www.mutorium.com/blog/cargo-insta-snapshot-testing/) generalizes it for any Rust project.

The advocates' justification: the *output being pinned is itself the behavior under test*. A compiler's diagnostic message is not an internal representation detail; it is the user-facing surface — what the user reads. Pinning it is therefore a behavioral assertion about the compiler's output, not a structural assertion about the compiler's source. The distinction the advocates draw: "the output is the artifact" (compiler messages, rendered reports, serialized JSON from a formatter). The disqualifying case is asserting that a *prose string appears inside the source file that produces the output* — there the source is the representation, not the artifact.

The insta project explicitly notes that golden-file tests are appropriate when "the output is large (think multi-line JSON)" and "the structure changes often and you want a nice diff." The implicit limit is that a human reviewer must *inspect and intentionally approve* each change; blind approval (`--update-snapshots` in CI without human review) collapses the practice back into snapshot blindness.

### ArchUnit-Style Dependency Rules

ArchUnit (Java, https://www.archunit.org/) and NetArchTest (.NET) allow writing tests that enforce structural rules: "no class in `domain` may import from `infrastructure`." The *Building Evolutionary Architectures* book (Ford, Parsons, Kua; O'Reilly, 2017/2022) calls these *architectural fitness functions*: "not a new framework — a new perspective on existing tools; JDepend, ArchUnit, NetArchTest all pre-existed the term." (Source: https://synchronium.github.io/software-architecture-wiki/concepts/fitness-functions.html, read summary; https://medium.com/yonder-techblog/architectural-fitness-functions-an-intro-to-building-evolutionary-architectures-dc529ac76351.)

The advocates' justification: these tests encode *architectural decisions* — decisions with cross-cutting behavioral consequences that cannot be enforced by any single behavioral test. The rule "domain must not import infrastructure" is not a prose pin; it is a machine-checkable statement of a design invariant. It is tested structurally *by necessity*, not *by laziness*. The line between this and prose-pinning: architectural fitness functions encode deliberate, documented architectural decisions and survive refactoring of any implementation that respects the invariant. A test that asserts "the string `def authenticate` appears in `auth.py`" is not a fitness function; it encodes no architectural decision and is invalidated by any rename.

### Lint Rules as Tests

Lint rules (ESLint, Clippy, Rubocop) are structural checks, and some projects run them as part of the test suite. Advocates treat them as fitness functions: they encode stylistic or safety decisions that cannot be exercised by behavioral tests (e.g., "no `eval`"). They are distinguished from prose-pinning by being rule-based — they check for the *presence or absence of a structural pattern* that is itself prohibited — rather than asserting that a specific string of prose exists.

---

## Synthesis

### The Vocabulary the Literature Offers

| Term | Coined By | Core Meaning |
|---|---|---|
| Change-detector test | Alex Eagle / Google (2015) | Fails on any code change regardless of behavioral effect |
| Tautological test (TTDD) | Fabio Pereira (2010) | Restates the implementation; true by construction |
| Fragile test | Meszaros, *xUnit Test Patterns* (2007) | Fails when SUT changes in irrelevant ways |
| Overspecified software | Meszaros | Test specifies more about internals than necessary |
| Snapshot blindness | Jest community (informal) | Snapshots routinely approved without inspection |
| Behavior sensitivity / Structure sensitivity | Kent Beck (2019) | The axis: good tests are behavior-sensitive, structure-insensitive |

### Three Strongest Quotes from Named, Respected People

1. **Kent Beck** (Programmer Test Principles, 2019): "Tests should be coupled to the behavior of code and decoupled from the structure of code."

2. **Ian Cooper** ("TDD, Where Did It All Go Wrong"): "Your API is your contract, your tests should test the API, not the implementation details. Coupling is the first problem in software."

3. **Google Testing Blog, Alex Eagle** ("Change-Detector Tests Considered Harmful," 2015): Change-detector tests "validate implementation details rather than actual behavior... break easily during refactoring even when functionality remains intact... provide false confidence in code correctness... don't serve as effective documentation."

### Where the Literature Draws the Line the Designer Is Drawing

The designer's line — tests that "search or compare the source code itself" rather than "running actual machinery" — maps precisely onto the *behavior-sensitivity* axis Kent Beck names. Every major authority agrees: tests couple to the *observable output* of a running system, not to the *text that produces the system*. An assertion that prose appears verbatim in a source file is:

- A change-detector test in Eagle's taxonomy (it detects edits to a file, not misbehavior).
- A tautological test in Pereira's taxonomy (the expected value is part of the implementation).
- An overspecified test in Meszaros's taxonomy (it specifies far more about the representation than about any behavior).
- A test that scores zero against any mutation testing suite, because no behavioral mutation in the system's logic can make it fail.

The carve-outs the literature recognizes — compiler UI tests (rustc, insta), architectural fitness functions (ArchUnit), lint-as-test — all share one property: *the structure being asserted is the artifact* (compiler output is the product) *or encodes a documented architectural invariant*. None of these cases assert that a specific prose string lives inside the source file implementing a feature.

The designer's intuition is confirmed as mainstream, named, and held by the field's most respected voices.

---

## Sources

- Kent Beck, "Programmer Test Principles," Medium, 2019: https://medium.com/@kentbeck_7670/programmer-test-principles-d01c064d7934 (paywalled; content from secondary sources)
- Kent Beck, "Test Desiderata," Medium: https://medium.com/@kentbeck_7670/test-desiderata-94150638a4b3
- Ian Cooper, "TDD, Where Did It All Go Wrong," NDC/InfoQ: https://www.infoq.com/presentations/tdd-original/
- Ian Cooper talk notes (read): https://keyvanakbary.github.io/learning-notes/talks/tdd-where-did-it-all-go-wrong/
- Alex Eagle / Google, "Change-Detector Tests Considered Harmful," 2015 (read): https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html
- Andrew Trenk / Google, "Test Behavior, Not Implementation," 2013: https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html
- Erik Kuefler / Google, "Test Behaviors, Not Methods," 2014 (read): https://testing.googleblog.com/2014/04/testing-on-toilet-test-behaviors-not.html
- Google, "Tests Too DRY? Make Them DAMP!," 2019: https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html
- Sandi Metz, "The Magic Tricks of Testing," RailsConf 2013: https://speakerdeck.com/skmetz/magic-tricks-of-testing-railsconf
- Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007; Fragile Test entry: http://xunitpatterns.com/Fragile%20Test.html (unreachable at research time; content from multiple secondaries)
- Fabio Pereira, "TTDD — Tautological Test Driven Development Anti-Pattern," 2010 (read): http://fabiopereira.me/blog/2010/05/27/ttdd-tautological-test-driven-development-anti-pattern/
- Randy Coulman, "Tautological Tests," 2016 (read): https://randycoulman.com/blog/2016/12/20/tautological-tests/
- Mark Sands, "Mocking is Tautological," 2014: http://marksands.github.io/2014/05/14/mocking-is-tautological.html
- Martin Fowler, "Unit Test," bliki (read): https://martinfowler.com/bliki/UnitTest.html
- Martin Fowler, Software Testing Guide: https://martinfowler.com/testing/
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall, 2004; characterization test entry (Wikipedia): https://en.wikipedia.org/wiki/Characterization_test
- Fabrizio Duroni, "Golden master testing aka Characterization test" (read summary): https://www.fabrizioduroni.it/blog/post/2018/03/20/golden-master-test-characterization-test-legacy-code
- SitePen, "Snapshot Testing: Benefits and Drawbacks" (read): https://www.sitepen.com/blog/snapshot-testing-benefits-and-drawbacks
- Stryker Mutator, "What is mutation testing?" (read): https://stryker-mutator.io/docs/
- Mutorium, "Snapshot Testing Rust Code with cargo-insta" (read): https://www.mutorium.com/blog/cargo-insta-snapshot-testing/
- dtolnay, trybuild: https://github.com/dtolnay/trybuild
- oli-obk, ui_test: https://github.com/oli-obk/ui_test
- Neal Ford, Rebecca Parsons, Patrick Kua, *Building Evolutionary Architectures*, O'Reilly, 2nd ed. 2022; fitness functions summary (read): https://synchronium.github.io/software-architecture-wiki/concepts/fitness-functions.html
- ArchUnit fitness functions overview (read): https://medium.com/yonder-techblog/architectural-fitness-functions-an-intro-to-building-evolutionary-architectures-dc529ac76351
- QuickCheck / property-based testing (read): https://softwarepatternslexicon.com/haskell/testing-and-design-patterns/property-based-testing-with-quickcheck/
