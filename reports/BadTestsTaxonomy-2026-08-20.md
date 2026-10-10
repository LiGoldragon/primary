# Bad Tests Taxonomy

Research date: 2026-08-20. All claims carry sources; uncertain attributions are marked [attribution uncertain] or [claim].

This report covers the full territory of bad tests beyond source-text-pinning and change-detector tests, which are treated in the companion report `SourceSearchingTests-2026-08-20.md`.

## 1. The Academic Test-Smell Canon

### 1a. Van Deursen, Moonen et al. — "Refactoring Test Code" (ICSM 2001)

Source: van Deursen, A., Moonen, L., van den Bergh, A., & Kok, G. (2001). "Refactoring Test Code." Proceedings of the 2nd International Conference on Extreme Programming. ACM: https://dl.acm.org/doi/10.5555/869201 | Semantic Scholar: https://www.semanticscholar.org/paper/Refactoring-test-code-Deursen-Moonen/a5b1308b13dd393176494e6ccd078533f943ce48

The paper introduced eleven test smells. All definitions below are drawn from the paper and from the tsDetect secondary documentation at https://testsmells.org/pages/testsmells.html.

**Mystery Guest**
A test depends on an external resource (file, database, network endpoint) that is created and managed outside the test method. Why bad: the resource's state is invisible to the reader; tests become environment-sensitive and non-reproducible. How detected: test methods that access the filesystem, a database, or a network without creating those resources in the same method body. Replacement: create and tear down resources inside the test, or use in-process fakes.

**Resource Optimism**
A test accesses an external resource without first verifying it exists or is in the expected state. Why bad: produces nondeterministic results — the test passes in one environment, fails silently in another. How detected: file or database access with no guard or setup step confirming availability. Replacement: assert resource preconditions explicitly, or eliminate the external resource dependency with fakes.

**Test Run War**
Multiple developers or CI agents running the same suite simultaneously share a resource (database row, file, network port), causing collisions. Why bad: tests pass in isolation and fail intermittently in shared environments with no deterministic cause. How detected: tests that fail more frequently in CI than locally; tests that contend on fixed database tables or fixed port numbers. Replacement: isolate resources per run via unique namespacing, transaction rollback, or in-memory stores.

**General Fixture**
The setup method initializes more state than any individual test needs. Why bad: readers cannot determine which parts of the setup each test actually depends on; changes to the fixture break unrelated tests. How detected: setup methods that construct objects or insert rows that only some tests use. Replacement: minimize setup to what each test strictly requires; inline rare fixtures into the test body itself.

**Eager Test**
One test method invokes and verifies multiple distinct methods of the production class. Why bad: when the test fails, the reader cannot tell which method is broken; coverage attribution is opaque. How detected: a single test method with multiple groups of act and assert phases, each targeting a different production method. Replacement: one tested behavior per test method.

**Lazy Test**
Multiple test methods exercise the same production method with overlapping inputs, adding no distinct coverage. Why bad: duplicated effort; neither test fully specifies the method's contract. How detected: several tests for one method with no variation in the condition being exercised. Replacement: consolidate or partition by distinct input class or boundary condition.

**Assertion Roulette**
Multiple assertions in one test with no identifying messages. Why bad: on failure the output names the test but not which assertion fired; diagnosis requires re-running under a debugger. How detected: multiple bare `assertEquals` or `assert` calls in sequence with no message argument. Replacement: add a descriptive message to each assertion, or split into single-assertion tests named for the condition.

**Indirect Testing**
A test for class A exercises class B through A, rather than testing B directly. Why bad: failures in B surface as failures in A; root cause is obscured. How detected: test class for A that exercises B's logic indirectly through A's interface. Replacement: write a dedicated test suite for B; use a test double for B when testing A.

**For Testers Only**
Production code contains methods added solely to enable testing — state-exposure hooks, package-private accessors, or methods that exist only to satisfy a mock setup. Why bad: pollutes the production API with test scaffolding; increases coupling; ships code that is never called in production. How detected: public or package-private methods with no production callers. Replacement: redesign the class to be testable through its natural interface using dependency injection.

**Sensitive Equality**
A test asserts equality by calling `toString()` on an object and comparing the resulting string. Why bad: any formatting change in `toString()` — whitespace, ordering, field addition — breaks the test even when behavior is unchanged; structurally identical to a source-text-pinning test for the object's representation. How detected: assertions of the form `assertEquals(expectedString, obj.toString())`. Replacement: compare fields directly, or use domain-specific assertion helpers that inspect the object's semantic properties.

**Test Code Duplication**
Setup, teardown, or assertion sequences are copy-pasted across test methods or classes. Why bad: every change must be made in N places; duplication drift causes tests to diverge silently, so some copies stop being correct specifications while remaining green. How detected: identical or near-identical code blocks across multiple test methods. Replacement: extract to shared helper methods; for fixtures, use a parameterized test or a factory method.

### 1b. tsDetect and Extended Empirical Studies

Tufano et al. (2016), "An Empirical Investigation into the Nature of Test Smells," ICSM 2016: https://www.semanticscholar.org/paper/An-empirical-investigation-into-the-nature-of-test-Tufano-Palomba/a9198481e7642be53501ff6dbfba6e10dd8ee511 — found test smells appear early (often in the first test commit) and persist for the lifetime of the project.

Spadini et al., tsDetect tool (2020): https://testsmells.org/pages/testsmellexamples.html — extends the van Deursen catalog to 19 statically-detected smells for Java/Android. Additions beyond the 11 above:

**Conditional Test Logic**
Control flow (`if`, `switch`, loops) appears inside a test method body. Why bad: success becomes path-dependent; some branches are never exercised by any run; a condition that always evaluates to `true` in CI silently skips assertions. Detected by: any branching keyword in a test method. Replacement: one test per scenario; parameterized tests for multiple inputs.

**Constructor Initialization**
Test fields are set in the test class constructor rather than in a `setUp` or `@Before` method. Why bad: JUnit lifecycle guarantees apply to `setUp`, not to constructors; state may leak between test objects depending on framework implementation. Detected by: field assignments in `TestCase` subclass constructors. Replacement: use `@Before` / `setUp()`.

**Default Test**
IDE-generated placeholder test method left in the suite unchanged (e.g., `assertTrue(true)` or a body that is empty or consists only of `fail("Not yet implemented")`). Why bad: always passes, misleads coverage reports, hides that no real test was written. Detected by: the literal strings `not yet implemented`, `assertTrue(true)`, or an empty body in a test method. Replacement: delete or replace with a real specification.

**Duplicate Assert**
The identical assertion expression appears more than once in the same test method. Why bad: wasted work; suggests confusion about what is being tested; the second assertion cannot produce different information than the first. Detected by: repeated `assertEquals(x, y)` with identical arguments. Replacement: assert once; if the second assertion checks a different condition, separate into two tests.

**Empty Test**
A test method with no executable statements. Why bad: always passes, covering nothing; CI treats it as a passing test. Detected by: a test method body with no statements other than comments. Replacement: either delete or implement.

**Exception Handling**
A test uses a `try/catch` block to catch an expected exception, with the `catch` body containing only assertions or — worse — being empty (so the exception is silently swallowed). Why bad: an empty catch makes the test incapable of failing on that exception; even a non-empty catch buries the intent. Detected by: `try { …; } catch (SomeException e) { }` in test methods. Replacement: use `@Test(expected=…)` or `assertThrows(…)`.

**Ignored Test**
A test marked `@Ignore` or `@Disabled` that has no stated expiry date or bug reference. Why bad: the test never runs; bugs accumulate invisibly behind the ignored tests; the ignored annotation is often forgotten permanently. Detected by: `@Ignore` or `@Disabled` without a linked issue. Replacement: fix the underlying issue and re-enable, or delete the test if the behavior is no longer specified.

**Magic Number Test**
A numeric literal appears in an assertion with no label explaining what it represents. Why bad: future readers cannot understand what value was expected or why; the test becomes documentation that documents nothing. Detected by: bare numeric literals in `assertEquals` or `assertThat` calls. Replacement: extract to a named constant; use a descriptive assertion message.

**Redundant Assertion**
An assertion that compares a value to itself — `assertEquals(x, x)` — or compares two literals. Why bad: mathematically always true; verifies nothing about production behavior. Detected by: identical expressions on both sides of an equality assertion. Replacement: delete and write an assertion that could actually fail.

**Sleepy Test**
`Thread.sleep()` or equivalent is used to wait for an asynchronous operation. Why bad: timing-dependent; fails on slower CI machines; slow regardless; is the proximate cause of one of the most common categories of flaky tests. Detected by: `Thread.sleep()`, `asyncio.sleep()`, or equivalent in test code. Replacement: use callbacks, futures, event-driven waiting, or polling with a timeout and a meaningful error.

**Unknown Test**
A test method with no assertion and no `expected` exception declaration — it passes if no exception is thrown. Why bad: cannot fail due to any regression in behavior; is in fact a subtype of Missing Assertion. Detected by: test methods with no assertion and no `@Test(expected=…)`. Replacement: add an assertion on the return value or observable state.

## 2. Meszaros — xUnit Test Patterns Smell Catalog (Beyond Fragile Test)

Source: Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007. Pattern index: http://xunitpatterns.com/ — site was partially unreachable at research time; definitions below come from the book via multiple secondary sources and slides.

The companion report covers *Fragile Test* and *Overspecified Software*. The additional Meszaros smells are:

**Obscure Test**
A test that cannot be understood at a glance — too long, too many setup steps, logic scattered across inherited helpers, or variable names that carry no semantic meaning. Why bad: Meszaros frames tests as *executable documentation*; a test that cannot be read is a specification that cannot be consulted. Subtypes: Long Test, Complex Test, Verbose Test. Detected by: test methods that require reading multiple files to understand, or that exceed ~20 lines of non-boilerplate code. Replacement: follow the Four-Phase structure (Arrange / Act / Assert / Teardown); inline all fixture that the reader needs to understand the intent; name variables after roles, not types.

**Hard-to-Test Code**
Production code is structured so that it cannot be exercised by a test without heroic effort — tightly coupled dependencies, global singletons, static methods with side effects, no injection points. Why bad: forces tests to either skip the code (leaving it untested) or become far more complex than the behavior warrants. Detected by: test setup that requires global state modification, process-level mocking, or significant reflection. Replacement: refactor production code toward dependency injection and clear seam points before writing the tests.

**Test Logic in Production**
Production code contains branches like `if (testing) { … }`, environment variable checks that alter behavior when `TEST=1`, or test-only methods baked into the shipping binary. Why bad: the production binary diverges from the tested binary; ships dead code; tests the harness, not the product. Detected by: grep for `ENV["TEST"]`, `#ifdef TEST`, or test-framework imports in non-test packages. Replacement: use dependency injection so test doubles replace production dependencies at the seam, without production code knowing it is under test.

**Buggy Tests**
Tests that themselves contain defects: they pass when production code is broken, or fail when it is correct, or are simply wrong about what behavior they specify. Why bad: destroys trust in the suite; developers begin ignoring red builds; a green suite with buggy tests is worse than no suite (it provides false confidence). Detected by: mutation testing — if a mutant that inverts production behavior is not caught by any test, at least one test is buggy with respect to that behavior. Replacement: treat test code with the same review rigor as production code; every new test must be seen failing before it is accepted.

**Erratic Test**
A test whose result varies across runs without changes to the code under test. Meszaros names eight subtypes:

- *Interacting Tests*: tests share mutable state, so one test's side effect determines another's outcome.
- *Interacting Test Suites*: suite-level shared state causes passes when run alone but failures in the full suite.
- *Lonely Test*: passes in the suite (relies on a prior test to have set up state) but fails in isolation.
- *Resource Leakage*: finite resources (threads, file handles, database connections) are allocated and not released; later tests in the run starve.
- *Resource Optimism*: the test assumes an external resource exists; passes on the developer machine, fails in CI.
- *Unrepeatable Test*: first run passes, second run fails because the test corrupts shared state it then depends on.
- *Test Run War*: parallel runs by different users collide on shared resources.
- *Nondeterministic Test*: fails randomly due to random input, timing, or thread scheduling.

Why bad (across all subtypes): the test cannot serve as a regression gate because its verdict is not repeatable; a red build that sometimes goes green trains developers to re-run rather than fix. Detected by: run the suite 10 times; any test whose result varies is erratic. Replacement: make every test fully self-contained — own setup, own teardown, no shared mutable fixtures, no external resource assumptions. See also Section 4 (flakiness) for the industry-scale treatment.

**Slow Tests**
The suite takes so long that developers stop running it before committing. Why bad: the feedback loop collapses; bugs accumulate between runs; the suite no longer functions as a fast regression net. Root causes: real database access, filesystem I/O, network calls, `Thread.sleep()`, test ordering effects that force serial execution. Detected by: measure wall-clock time per test; flag any test exceeding ~1 second for a unit test. Replacement: replace slow dependencies with fast in-process fakes; keep the unit suite under 30 seconds; separate integration tests that need real I/O into a slower tier.

**Manual Intervention**
A test requires a human step — clicking a button, entering credentials, approving a dialog — to complete. Why bad: not automatable; blocks CI; the suite cannot serve as an unattended regression gate. Detected by: documentation or comments in test code indicating human steps. Replacement: automate the interaction via headless browser or driver; mock the external actor; reclassify as an exploratory or acceptance test outside the automated suite.

## 3. The Self-Confirming Family

This family covers tests that are structurally incapable of detecting regressions, either because they contain no assertion, because their assertion is always true, or because their oracle — the expected value — is computed by replicating the production code.

### The Liar / Rotten Green Test / Always-Green Test

The name "The Liar" appears in the Meszaros catalog (xUnit Test Patterns, 2007) for a test that always passes even when the code is broken — it gives the false signal of passing tests while hiding real failures. The related term "Rotten Green Test" (used in the Python community) refers to a test that passes because its assertions are inside a branch that never executes, or inside a `try` block whose exception handler swallows the check. The "always-green test" framing also appears in mysoftwarequality.wordpress.com (2012) with the same definition.

[Note on attribution: The liar-test term is sometimes attributed to Ben Orenstein / thoughtbot; this was not confirmed by any source found at research time. The Meszaros usage is the earliest confirmed source.]

Why bad: gives green signal regardless of whether production behavior is correct; trains developers to trust the suite without justification. How detected: mutation testing — deliberately break the implementation; a liar test still passes. The `falsegreen` tool (https://github.com/vinicq/falsegreen, https://pypi.org/project/falsegreen/) scans Python ASTs for 47 known false-positive patterns: assertions that never execute, checks that are always true, swallowed exceptions, mock assertions with typos, dead-code checks. Replacement: every test must be seen failing before it is accepted into the suite.

### Missing Assertion (Assertion-Free Test)

A test method that executes code but asserts nothing. The tsDetect catalog calls this "Unknown Test" (see Section 1b). It passes unless an unexpected exception is thrown, which is a weak substitute for a real assertion.

Why bad: executes without verifying outcomes; provides false confidence; coverage tools count the executed lines as tested; mutation testing will show a near-zero kill rate. How detected: static analysis — scan for test methods with no `assert*`, `expect*`, or `verify*` calls. ESLint plugins (e.g., `eslint-plugin-ui-testing`) can enforce this at CI time. Source: https://test-smell-catalog.readthedocs.io/en/latest/Issues%20in%20test%20steps/Issues%20in%20assertions/Missing%20Assertions.html | https://www.effective-software-testing.com/tests-without-assertions-why-do-they-happen. Replacement: require at least one assertion verifying a concrete expected outcome; review every test in a suite to confirm it would fail if the code under test returned a constant or threw unconditionally.

### Tautological Test (TTDD)

Covered in the companion report's Section 2b; not repeated here.

### Testing the Framework / Testing the Language

A test exercises library or language behavior rather than application logic — for example, asserting that `list.append(x)` produces a list containing `x`, or that a standard library function returns a known result. No single canonical named smell with a primary source was found; the pattern appears across multiple antipattern catalogs under "Accidental Test Framework" or similar informal names.

Why bad: the test cannot fail due to any application regression; it only fails if the library changes behavior. How detected: ask "Would this test fail if I deleted all my application code and kept only the import?" If yes, it tests the framework, not the application. Source: https://medium.com/codex/anti-patterns-of-automated-software-testing-b396283a4cb6. Replacement: delete; if the test was added to gain confidence in a library's API, write a single integration test that exercises the application's use of the API, not the API itself.

## 4. Over-Mocking and Mockist Test Pathologies

### Mockist Brittleness (Fowler, "Mocks Aren't Stubs," 2007)

Martin Fowler distinguishes classical TDD (use real objects unless awkward) from mockist TDD (always mock collaborators). The pathology of the mockist style, in Fowler's words:

"Mockist tests are thus more coupled to the implementation of a method. Changing the nature of calls to collaborators usually cause a mockist test to break." And on correctness: "You also run the risk that expectations on mockist tests can be incorrect, resulting in unit tests that run green but mask inherent errors."

Source (read): https://martinfowler.com/articles/mocksArentStubs.html

Why bad: tests break on refactors that do not change observable behavior (implementation coupling); expectations can be wrong while the test is green; focuses verification on "how" the code does something rather than "what" it does. How detected: tests that break when code is reorganized without altering externally visible behavior; tests with more mock-setup lines than assertion lines. Replacement: prefer classical TDD; use test doubles only for genuinely awkward collaborators — I/O, time, randomness, external services. Test the observable output, not the call graph.

### Over-Mocking / Listening to Tests (Freeman & Pryce, GOOS, 2009)

Steve Freeman and Nat Pryce (*Growing Object-Oriented Software, Guided by Tests*, Addison-Wesley, 2009, https://growing-object-oriented-software.com/) use mock objects as a *design tool*. Their rule: mock "peers" (collaborators at the same architectural level) but not "internals" (implementation details within a class). When tests become painful to write because of excessive mock setup, they treat that pain as a design signal:

"Sensitise yourself to find the rough edges in your tests and use them for rapid feedback" — the roughness means the design has a weakness, not that more mocks are needed.

Chapter 20 of GOOS, "Listening to the Tests," adds this diagnosis step explicitly to the TDD cycle. Over-mocking surfaces as tests that are hard to set up because too many collaborators are being simulated — a sign the class under test has too many responsibilities.

Why bad: over-mocked tests are fragile, hard to read, test the wiring rather than the behavior, and permit the real collaborators to diverge from the mock's behavior silently (the mock drifts). How detected: mock setup that takes more code than the assertion; any mock that replicates production logic; tests that pass when the real collaborator is broken. Replacement: use contract tests (Pact, or hand-rolled provider tests) to verify that mocks match real implementations; simplify design to reduce the number of collaborators needing mocking.

Sources: https://growing-object-oriented-software.com/ | https://dev.to/trikitrok/listening-to-test-smells-3049

## 5. Flakiness and Environment

### Non-Deterministic Tests (Fowler, 2011)

Martin Fowler, "Eradicating Non-Determinism in Tests," 2011: https://martinfowler.com/articles/nonDeterminism.html (read at research time).

Core quote: "Non-deterministic tests have two problems, firstly they are useless, secondly they are a virulent infection that can completely ruin your entire test suite."

Fowler's taxonomy of non-determinism causes:

1. **Lack of isolation** — shared mutable state (databases, static fields, singletons) allows one test's side effects to corrupt another's preconditions. Fix: rebuild initial state from scratch, use transaction rollback, or properly isolate per-test.
2. **Asynchronous behavior** — timing issues when testing async operations. Fowler: "Never use bare sleeps to wait for asynchronous responses: use a callback or polling."
3. **Remote services** — unstable external dependencies. Fix: use test doubles, backed by contract tests that verify the double's behavior matches the real service.
4. **Time and clock dependencies** — `Date.now()` or `System.currentTimeMillis()` returns different values each run. Fowler: "Always wrap the system clock, so it can be easily substituted for testing." Fix: inject a clock stub set to a fixed value.
5. **Resource leaks** — exhausted database connections, file descriptors, or memory cause random failures in later tests. Fix: configure resource pools to size 1 during testing to surface leaks immediately rather than intermittently.

Quarantine strategy: place non-deterministic tests in a separate suite; enforce numeric and time limits (e.g., maximum 8 quarantined at once; maximum one week before forced resolution or deletion).

### Flaky Tests at Scale (Google, 2016–2017)

John Micco, "Flaky Tests at Google and How We Mitigate Them," Google Testing Blog, 2016: https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html

Jeff Listfield, "Where Do Our Flaky Tests Come From?", Google Testing Blog, 2017: https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html

Empirical findings from 4.2 million test runs at Google:

- Flakiness correlates linearly with binary size (larger test binaries are more flaky).
- Approximately 16% of flaky tests trace to actual production bugs — not test defects — meaning flaky tests occasionally surface real issues, but the signal is buried in noise.
- Android emulator tests show notably higher flakiness than other platforms.
- Causes ranked: (1) UI/GUI testing — highest flakiness rate; (2) timing and synchronization; (3) external dependencies; (4) test design flaws; (5) environmental variance; (6) global state and shared resources (temp files, fixed ports).

Micco's response framework: Identify, Notify, Triage, Prevent. New tests must be run repeatedly (Google uses 10 runs) before being added to a critical path suite. A test that is flaky on introduction is rejected. Stable failures are preferable to intermittent ones — a stable failure can be diagnosed and fixed; a flaky one trains developers to re-run.

### Test Order Dependence

A subtype of Interacting Tests (Meszaros) elevated to its own concern by the flakiness literature. Tests designed to be run in a fixed order become coupled: test B depends on state that test A leaves behind. When the runner randomizes order (JUnit 5, pytest-random-order), B fails. How detected: randomize test execution order and observe which tests break. Replacement: every test creates its own preconditions; no test depends on state from a prior test.

## 6. Coverage Worship

### Coverage Target Fixation

Martin Fowler, "TestCoverage," bliki: https://martinfowler.com/bliki/TestCoverage.html (read at research time).

Fowler: "If you make a certain level of coverage a target, people will try to attain it. The trouble is that high coverage numbers are too easy to reach with low quality testing." And: "Test coverage is a useful tool for finding untested parts of a codebase. Test coverage is of little use as a numeric statement of how good your tests are." He is explicitly suspicious of 100% targets: they suggest "someone writing tests to make the coverage numbers happy, but not thinking about what they are doing."

Brian Marick, "How to Misuse Code Coverage," 1999: https://www.exampler.com/testing-com/writings/coverage.pdf (the canonical primary source; Marick is Fowler's cited authority). Marick's key observation, quoted by Fowler: "If a part of your test suite is weak in a way that coverage can detect, it's likely also weak in a way coverage can't detect." This is the Goodhart's Law formulation applied to testing: the moment coverage becomes a target, it ceases to measure test quality.

Why bad: a suite that achieves a coverage target through assertion-free tests, tautological tests, or tests that exercise code without checking outcomes will score highly on coverage while providing near-zero regression protection. How detected: remove all assertions from the test suite; if coverage stays high, coverage is meaningless for this suite. Replacement: mutation testing.

### Mutation Testing as the Antidote

PIT (Java): https://pitest.org/ — introduces minimal mutations (flip `>=` to `>`, replace return values with constants, delete method bodies) and measures how many the test suite catches. A suite with 80% line coverage and 30% mutation score reveals hollow tests.

Stryker (JS/TS/C#): https://stryker-mutator.io/ — same principle for other languages.

The mutation testing literature is the sharpest formal indictment of hollow test suites: a test that passes after every behavioral mutation in the production code contributes nothing to the mutation score, regardless of its coverage contribution.

### The Pesticide Paradox (Beizer, 1990)

Boris Beizer, *Software Testing Techniques*, 2nd ed., 1990: "Every method you use to prevent or find bugs leaves a residue of subtler bugs against which those methods are ineffectual." Applied to test suites: a fixed test suite run repeatedly against evolving software finds no new bugs after a certain point. The tests that previously caught errors have already caught them; new code paths and new classes of bugs remain untested.

Why bad: the team accumulates false confidence from green builds while the defect escape rate rises. Sources: https://katalon.com/resources-center/blog/pesticide-paradox-in-software-testing | https://lawsofsoftwareengineering.com/laws/pesticide-paradox/ How detected: track the defect escape rate — bugs found in production vs. bugs caught by tests. A rising escape rate against a stable green suite is the paradox in operation. Replacement: continuously rotate and extend tests; use exploratory testing, fuzzing, and mutation testing to force the suite to evolve with the code.

## 7. Fixture and Golden-File Abuse

### Characterization Tests Left as Permanent Specification

Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall, 2004. Feathers coined characterization tests: tests written to document what the existing (possibly buggy) system actually does, as a prerequisite for safe refactoring. His own caveat at https://michaelfeathers.silvrback.com/characterization-testing: "A characterization test does not check whether the code is correct — it pins what the code actually does right now." And: "you may inadvertently lock in buggy behavior."

Feathers noted from practice: "After fixing a perceived bug, users complained because they depended on the behavior being removed — they didn't think it was a bug, they thought it was a feature."

Why bad: characterization tests are transitional tools. Left permanently in the suite, they assert implementation accidents as intended behavior; any deliberate correction produces test failures that appear to be regressions. The team then faces the choice of reverting the fix or deleting the test — at which point the test is revealed as not a specification at all. How detected: a test suite where fixing a real bug causes test failures, and where the team's response is to delete the test rather than update it. Replacement: replace characterization tests with intent-based specification tests as domain understanding develops; keep them only for the duration of the refactoring window that motivated them.

### Blessed Fixtures Re-Recorded Without Inspection

Snapshot or golden-file tests where the accepted output is regenerated automatically when tests fail — `jest --updateSnapshot`, `cargo insta review --accept-all` — committing the new snapshot without human review of whether the change was intended.

Why bad: the test stops being a specification of intent and becomes a change-detector with amnesia — it records whatever the code does now and calls it correct. It is the fixture equivalent of approving every code diff without reading it. How detected: grep git history for bulk snapshot updates committed together with behavior changes; any CI workflow where "update snapshots" is a reflex response to a failing test. Replacement: keep golden files small and reviewable; require explicit per-snapshot human sign-off; for complex output, prefer property-based assertions over whole-output comparison where possible.

Source: https://www.sitepen.com/blog/snapshot-testing-benefits-and-drawbacks (read at research time).

### Testing Against Production Data

Using a copy of a production database or production API responses as the test fixture. Why bad: (1) production data contains private information that should not exist in test environments; (2) production data changes, making tests that depend on specific records fragile; (3) the test passes when it happens to find the expected record, but the record may be cleaned up, migrated, or renamed; (4) the test does not specify what the data should be — it asserts against whatever the data happens to be. How detected: test configuration that points at a production or staging environment; tests that fail when production records are updated. Replacement: use generated, minimal, explicitly declared fixture data that is owned by the test suite and under version control.

## 8. LLM-Era Additions

[These are current claims from 2025–2026 sources. The academic literature on AI-generated test quality is still forming.]

### Tautological AI-Generated Tests

Tests generated by an LLM (GitHub Copilot, ChatGPT, Claude, etc.) by reading an existing implementation and asserting its current output — encoding bugs as intended behavior.

David Adamo Jr. (https://davidadamojr.com/ai-generated-tests-are-lying-to-you/): "We are replacing _validation_ with _transcription_." His canonical example: a `divide(a, b)` function that returns `0` on division by zero (a bug) instead of raising an exception. An LLM generates a test that asserts `divide(10, 0) == 0` — precisely because it mirrors the implementation. "We built the perfect machine for confirming our own mistakes faster than ever before."

Mark Seemann / ploeh.dk (https://blog.ploeh.dk/2026/01/26/ai-generated-tests-as-ceremony/): AI-generated tests for existing code are "tests as ceremony, rather than tests as an application of the scientific method." The scientific failure is skipping the red state: "Tests work best when you have seen them fail." A test generated from working code has never been red; it is cargo-cult testing — the motions of testing without the signal.

Academic research, arXiv 2607.22883v1 (2025), "Evaluating and Mitigating the Misguidance Effect": prompting an LLM with buggy code causes it to generate tests that validate the erroneous behavior and suppress bug-finding tests; "assertion errors account for over 85% of failures in some benchmarks." Source: https://arxiv.org/html/2607.22883v1

Why bad: the oracle is wrong. The test suite shows high line coverage and a low mutation score simultaneously — the most damning combination. How detected: mutation testing; ask whether the test could have been written before the implementation existed. Replacement: anchor AI assistance in TDD mode — write the failing test (specification) first, then use AI to implement against it; if generating tests after the fact, run mutation testing immediately and treat surviving mutants as test failures.

Source: https://getautonoma.com/blog/ai-generated-tests-pass-but-dont-assert

## Condensed Taxonomy Table

| Name | One-line definition | Detection question |
|---|---|---|
| Mystery Guest | Test depends on external resource managed outside the test | "Is there state this test needs that I cannot see in the test body?" |
| Resource Optimism | Test assumes external resource exists without checking | "Does this test fail differently depending on the environment?" |
| Test Run War | Parallel test runs collide on shared resources | "Does this test fail more in CI than locally?" |
| General Fixture | Setup initializes more than any single test needs | "Which setup lines does this test actually use?" |
| Eager Test | One test verifies multiple distinct behaviors | "If this test fails, do I know which behavior is broken?" |
| Lazy Test | Multiple tests overlap on the same method without distinct coverage | "Do these tests check distinct conditions?" |
| Assertion Roulette | Multiple assertions with no failure messages | "When this fails, will I know which assertion fired?" |
| Indirect Testing | Test for A exercises B through A | "Am I testing B here, or am I testing A's use of B?" |
| For Testers Only | Production methods exist only to enable test setup | "Is this method called in production?" |
| Sensitive Equality | Asserts equality via `toString()` | "Does this fail on formatting changes that don't affect behavior?" |
| Test Code Duplication | Copy-pasted setup or assertions across tests | "How many places must change if this logic changes?" |
| Conditional Test Logic | `if`/`switch`/loop inside a test method | "Are all branches of this test always executed?" |
| Default Test | IDE-generated placeholder left in the suite | "Does this test specify any actual behavior?" |
| Duplicate Assert | Identical assertion repeated in one method | "Does the second assertion add any new information?" |
| Empty Test | Test method with no statements | "Would this test catch any regression?" |
| Exception Handling | `try/catch` hides or swallows expected exception | "Could this test pass even if the code throws the wrong exception?" |
| Ignored Test | `@Ignore` with no expiry or bug reference | "Is this test ever run?" |
| Magic Number Test | Numeric literal in assertion with no label | "What does this expected value mean?" |
| Redundant Assertion | Asserts `x == x` or two identical literals | "Can this assertion ever fail?" |
| Sleepy Test | `Thread.sleep()` used for async synchronization | "Does this fail on a slow machine?" |
| Unknown Test | No assertion and no expected exception | "Would this test catch a regression that changes the return value?" |
| Obscure Test | Test cannot be understood at a glance | "Can I read this test and know what it specifies?" |
| Hard-to-Test Code | Production code requires heroic effort to reach in a test | "Is this test complexity caused by a production design problem?" |
| Test Logic in Production | Production code has `if (testing)` branches | "Does the production binary differ from the tested binary?" |
| Buggy Tests | Tests that pass when code is broken | "Has this test ever been seen failing?" |
| Erratic Test (umbrella) | Test result varies across runs | "Does this test pass 10 times in a row?" |
| Slow Tests | Suite is too slow to run before committing | "Does a developer skip running the suite because it takes too long?" |
| Manual Intervention | Test requires a human step to complete | "Can this test be run in a headless CI environment?" |
| The Liar / Rotten Green Test | Always passes even when production code is broken | "Does this test fail when I break the behavior it claims to verify?" |
| Missing Assertion | Test body executes code but asserts nothing | "Does this test contain any `assert*` call?" |
| Testing the Framework | Test exercises library behavior, not application logic | "Would this test fail if I deleted my application code?" |
| Mockist Brittleness | Tests break on safe refactors due to mock expectations | "Does this test fail when I reorganize code without changing behavior?" |
| Over-Mocking (GOOS) | Mock setup is more complex than the behavior under test | "Is the pain of setting up this test a design signal?" |
| Non-Deterministic Test | Fails randomly due to time, state, async, or remote services | "Does this test pass 10 times in a row in a clean environment?" |
| Test Order Dependence | Test depends on state left by a prior test | "Does this test pass when run in isolation?" |
| Coverage Target Fixation | Numeric coverage target drives test-writing behavior | "Do these tests actually specify behavior, or do they exercise lines?" |
| Pesticide Paradox | Fixed test suite finds no new bugs in evolving code | "Is the defect escape rate rising while the test suite stays green?" |
| Characterization Tests as Spec | Transitional tests left permanently, locking in bugs | "Does this test verify intent or does it verify what the code currently does?" |
| Blessed Fixtures Re-recorded | Snapshots approved without inspection of what changed | "Was each changed snapshot reviewed by a human?" |
| Testing Against Production Data | Test fixtures come from a production database or API | "Does this test fail when a production record is cleaned up?" |
| Tautological AI-Generated Test | LLM-generated test asserts current (possibly buggy) behavior | "Could this test have been written before the implementation existed?" |

## Five Sharpest Quotes

1. **Martin Fowler**, "Eradicating Non-Determinism in Tests" (2011): "Non-deterministic tests have two problems, firstly they are useless, secondly they are a virulent infection that can completely ruin your entire test suite." (https://martinfowler.com/articles/nonDeterminism.html)

2. **Martin Fowler**, "TestCoverage" bliki (quoting Brian Marick): "If a part of your test suite is weak in a way that coverage can detect, it's likely also weak in a way coverage can't detect." (https://martinfowler.com/bliki/TestCoverage.html)

3. **Martin Fowler**, "Mocks Aren't Stubs" (2007): "You also run the risk that expectations on mockist tests can be incorrect, resulting in unit tests that run green but mask inherent errors." (https://martinfowler.com/articles/mocksArentStubs.html)

4. **David Adamo Jr.**, "AI-Generated Tests Are Lying to You" (2025): "We are replacing _validation_ with _transcription_. We built the perfect machine for confirming our own mistakes faster than ever before." (https://davidadamojr.com/ai-generated-tests-are-lying-to-you/)

5. **Mark Seemann**, "AI-Generated Tests as Ceremony" (2026): "Tests work best when you have seen them fail. [AI-generated tests for existing code] are tests as ceremony, rather than tests as an application of the scientific method." (https://blog.ploeh.dk/2026/01/26/ai-generated-tests-as-ceremony/)

## Sources

- Van Deursen, Moonen et al., "Refactoring Test Code," ICSM 2001: https://dl.acm.org/doi/10.5555/869201
- Tufano et al., "An Empirical Investigation into the Nature of Test Smells," ICSM 2016: https://www.semanticscholar.org/paper/An-empirical-investigation-into-the-nature-of-test-Tufano-Palomba/a9198481e7642be53501ff6dbfba6e10dd8ee511
- tsDetect smell examples: https://testsmells.org/pages/testsmellexamples.html
- tsDetect smell list: https://testsmells.org/pages/testsmells.html
- Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007: http://xunitpatterns.com/
- Meszaros, Erratic Test: http://xunitpatterns.com/Erratic%20Test.html
- Meszaros, Obscure Test: http://xunitpatterns.com/Obscure%20Test.html
- Martin Fowler, "Mocks Aren't Stubs," 2007 (read): https://martinfowler.com/articles/mocksArentStubs.html
- Martin Fowler, "Eradicating Non-Determinism in Tests," 2011 (read): https://martinfowler.com/articles/nonDeterminism.html
- Martin Fowler, "TestCoverage" bliki (read): https://martinfowler.com/bliki/TestCoverage.html
- Brian Marick, "How to Misuse Code Coverage," 1999: https://www.exampler.com/testing-com/writings/coverage.pdf
- Steve Freeman & Nat Pryce, *Growing Object-Oriented Software, Guided by Tests*, Addison-Wesley, 2009: https://growing-object-oriented-software.com/
- Listening to Test Smells (GOOS-derived): https://dev.to/trikitrok/listening-to-test-smells-3049
- John Micco, "Flaky Tests at Google and How We Mitigate Them," Google Testing Blog, 2016: https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
- Jeff Listfield, "Where Do Our Flaky Tests Come From?", Google Testing Blog, 2017: https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall, 2004
- Michael Feathers, "Characterization Testing," silvrback: https://michaelfeathers.silvrback.com/characterization-testing
- SitePen, "Snapshot Testing: Benefits and Drawbacks" (read): https://www.sitepen.com/blog/snapshot-testing-benefits-and-drawbacks
- PIT Mutation Testing: https://pitest.org/
- Stryker Mutator: https://stryker-mutator.io/
- Boris Beizer, *Software Testing Techniques*, 2nd ed., Van Nostrand Reinhold, 1990
- Pesticide Paradox summary: https://katalon.com/resources-center/blog/pesticide-paradox-in-software-testing
- David Adamo Jr., "AI-Generated Tests Are Lying to You": https://davidadamojr.com/ai-generated-tests-are-lying-to-you/
- Mark Seemann, "AI-Generated Tests as Ceremony," ploeh.dk, 2026: https://blog.ploeh.dk/2026/01/26/ai-generated-tests-as-ceremony/
- arXiv 2607.22883v1, "Evaluating and Mitigating the Misguidance Effect": https://arxiv.org/html/2607.22883v1
- Autonoma, "AI-Generated Tests Pass But Don't Assert": https://getautonoma.com/blog/ai-generated-tests-pass-but-dont-assert
- falsegreen (Python AST-based liar-test detection): https://github.com/vinicq/falsegreen | https://pypi.org/project/falsegreen/
- Test Smell Catalog — Missing Assertions: https://test-smell-catalog.readthedocs.io/en/latest/Issues%20in%20test%20steps/Issues%20in%20assertions/Missing%20Assertions.html
- Anti-patterns of automated testing: https://medium.com/codex/anti-patterns-of-automated-software-testing-b396283a4cb6
