# Flow bad807 — Psyche.{ Fable bad807 }

Successor of Psyche Fable 5ed94b. Secretary: Psyche Opus 28d847. May also reach Mind Astra.

## 2026-10-04 — Launch

Launch brief, the living's words (relayed by 28d847 in the brief):

> I want to restart the Fable flow and then your flow on similar contexts with different roles. You'll assist and delegate. You'll be the messenger, the secretary, the one that gets all the messages in and out, and only you talk to Fable. Fable can talk to Astra but the same rules as before apply.

> I want to concentrate on creating better context modules, especially high-quality ones that we can load in the system prompt, and continue developing Flow.

Role: design, rule, judge. 28d847 builds and tests. All inter-flow messages go through 28d847, except to Mind Astra.

First task: context modules — the standard, then the first high-quality modules for the system prompt.

Dispatched three readers: 5ed94b handover; context-module quotes from fable-package-vision.md; distill proposals and current module/base-context state.

Handover of 5ed94b digested. Key facts: edf227 designed a context-module standard and the Curriculum context standard; 5ed94b's raw records live in flows/5ed94b/vision/ (contextModules.md, skills.md, seats.md, nexusEntryPoint.md among them); 24 proposal books plus gap list and «Subflow context: four edits» sit uncommented in the living messenger; open to him: the five subflow-context edits, the family word for context modules ("faculties" proposed), proposal numbers. Field 42265e measured harness context: Codex base instructions 21,420 chars reach collaborators, our developer instructions do not; a Claude subagent carries its definition body plus two fixed paragraphs.

State witnessed by readers: no context-module standard exists in Vision/ or Intent/; raw records in flows/{edf227,dea0ba,5ed94b}/vision/contextModules.md and dea0ba/vision/systemPrompt.md. The Claude main-flow launcher (tools/claude-main-flow-launch.mjs) takes --system-prompt-file; its default is tools/main-flow-mode/system-prompt.md (299 words, behavior rules, no skills). Birth skills (main-flow, spirit, psyche, psyche-interraction, vocabulary, edit-coordination) load at user-prompt level. Curriculum (/git/github.com/LiGoldragon/Curriculum/skills) composes role modules `{identifier body}` for subagents only. 28d847's distill proposal on context modules holds 18 statements (unread whole; statements requested). The «Subflow context: four edits» proposals file is not in flows/5ed94b/books/.

Received: edf227/dea0ba raw records on context modules (five module types vision/intent/spirit/knowledge/operation plus role; registry (type, name, location) in Flow served over meta; launch names modules per place as a vector of variants carrying names; "kind" is taken; standard Flow uses and Curriculum implements; keep the name Curriculum; system-prompt anatomy classified line by line; a main-flow part not passed to subagents). edf227's research report (context-modules-research.md, 340 lines) read in part: Curriculum has 69 flat skill sources, no module type in the generator, roles.datom composes subagent bodies. 28d847's 18 distilled statements received as proposals. Still out: tension list from the vision package; edf227's standard design.

edf227's standard found: flows/edf227/books/curriculum-the-context-standard.md (module types Spirit Intent Vision Knowledge Compensation Trial Operation Role; file = frontmatter type/name/description + body; registry Module.{ ModuleType Name Location } over the meta socket; placements SystemPrompt / FirstPrompt / Loadable; RoleConfiguration.{ Role Vector<Placed> Model }; launch composes with no model in the loop; four proposals uncommented). Harness facts witnessed by edf227/dea0ba: on Claude, --system-prompt-file replaces the stock prompt and does not reach non-fork subagents; CLAUDE.md reaches some subagents; leading /skill commands reach forks only; Flow today passes the bundle as --system-prompt-file on Claude, and on Codex keeps stock base instructions with the bundle opening the first turn. Tensions open to him: T2 (family word), T3 (which modules qualify for the system prompt), T23 (the set of types). Decision: own edf227's standard with amendments and present the standard and the first system-prompt modules as one book of numbered proposals, after the measurement subflow returns.

Presented «Context modules: the standard and the first system-prompt modules»: the standard (seven types, three placements, qualifying rule, quality bar), measurements, five first modules (Spirit/spirit, Role/main-flow, Vision/vocabulary, Vision/psyche, Role/psyche-primary new), six rulings. Book subflow dispatched. Next, on his word: hand the build to 28d847.

## 2026-10-04 — Ethos, Datom and the Nexus: deep wide distillation ordered

The living, typed in chat:

> Well since you're up now, let's do an involved deep wide distillation of everything that touches Ethos, Datom, the Nexus architecture, and the three parts of the Nexus: signal, memory, and (I think we called it) operation. Let's get all of that with code and visuals in proposal books.

Carried out as an order. Plan: a corpus gatherer first (every raw record, distilled file, book and existing distill proposal touching these subjects, with tensions), then one proposal book per subject with ethos/datom code, Rust where expected, and SVG visuals.

28d847 replied: it stops on Ethos and nexus; holds flows/28d847/vision/nexus.md (his 2026-10-04 words on the standard entry point), 3-ethos-nexus.md, package sections 3–4; today's builds: signal-harness 8.0.0 and meta-signal-harness 1.0.x as ethos contracts on ethos-zero 9.0.0; ethos-zero 16.0.0 departures pending his ruling (one-field structs, Name.String as alias, comments dropped). Forwarded to the corpus gatherer.

Lane publish: the PrimaryPublish lock is held standing by the publisher db38f8; my publish subflow was stopped (it had polled the lock for five minutes, a no-polling fault, noted). Route now: publish requests go to 28d847 for db38f8, naming exact paths.

His comment on the first book: he does not understand where the proposals land. Logged in vision/presentations.md. Correction accepted: the book is redone as proposals each naming the file, how it is now (its lines), and the lines that replace them. Reader dispatched for the current lines.

Lane published on main through db38f8 (log, pointers, books, index line). Presented «Context modules: where each proposal lands»: nine proposals each naming file, current lines and replacement, vision marked from implementation; six rulings. Book subflow dispatched.

Corpus map landed: flows/bad807/reports/ethos-nexus-corpus.md, 10,053 lines, 633 records (251 ethos, 220 datom, 225 nexus, 100 signal, 94 memory, 16 operation, 14 entry point), 21 record tensions and 13 distilled-text tensions; none of 28d847's 13 clusters approved; ethos-zero 16.0.0 reads Operation and Memory roots ahead of his ruling while consumers pin 9.0.0. Decision: six proposal books — Ethos, Datom, The Nexus, Signal, Memory, Operation — drafted concurrently to flows/bad807/books/, reviewed against the bar, then published one by one.
