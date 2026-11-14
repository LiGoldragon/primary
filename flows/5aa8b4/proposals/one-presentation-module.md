Presentation.{ «One presentation module» }

# One presentation module

Created by Fable on his words of 2026-11-05: fifteen modules on one thing is far too many; a vision module holds his broad concept and stays short, since his time went into it; a knowledge module is the machine's working notes, cheap to make and cheap to delete. Five vision modules become one short one. The fine rules of a source, a figure, a build and a publication go to knowledge:book and the role modules, landed without review.

### Proposal 1: vision:presentation, rewritten · psyche-belief › vision/presentation.md

**Comment** The module as it stands is removed whole and the new text added whole; its description becomes "What a presentation is to the living: a proposal, a review or an account, and how a change reads." Modules that depended on vision-proposal, vision-review, vision-account or vision-book depend on vision-presentation after this; the lander renames them.

- ## A presentation
-
- A presentation's source opens with its title and is handed to the publisher as made.
-
- ## A presentation is signed
-
- A presentation names the model that created it and, for each model that helped, what that help was, on a subtitle line under the title.
-
- ## Figures
-
- A figure shows one thing, where the idea has a shape, and its colours and marks mean the same in every presentation.
-
- Every flowchart, in a presentation or in a belief module, is Mermaid, in the figure grammar; a presentation shows the SVG drawn from it.
-
- A figure shows how a thing moves, one question per figure, readable in seconds. Its grammar: a box is a thing or a collection; an arrow is a one-way relation carrying a verb, so that box, verb, box reads as a sentence; nearness and enclosure are kinship; top to bottom is order; colour carries a role or is absent. A figure is boxes joined by verbed arrows, drawn so a phone shows it. A sizable presentation carries several figures.
-
- ## Prose and code
-
- Prose is shown as rendered text.
-
- Code is shown as code, labelled with its language and highlighted in that language's colours.
-
- ## Change marks
-
- A presentation shows belief modules, each under its repo › path; its headings, naming the module and the kind of change, are the only words it has of its own.
-
- Colour is the sign of a change and lies in the margin alone: text keeps the page's colour, and code its language's colours, highlighted.
-
- A line added shows a green margin. A line removed shows a red margin. A line moved between modules shows once, under a margin of a third colour, headed by the module it leaves and the module it enters.
-
- A proposed change shows the light shade of its colour; a landed change shows the dark shade: darker is more.
-
- ```mermaid
- flowchart TB
-     p["a presentation"] -- "is one kind of" --> pr["a proposal: changes he rules on, light"]
-     p -- "is one kind of" --> rv["a review: changes already landed, dark"]
-     p -- "is one kind of" --> ac["an account: what happened"]
-     p -- "handed as made to" --> b["the publisher"]
-     b -- "publishes, for" --> l["the living"]
- ```

+ # A presentation
+
+ A presentation is a page the living reads: a proposal, a review or an account. It names the model that made it and what each other model did for it.
+
+ A proposal shows the system as it will be: the lines added to and removed from belief modules, for him to rule on, line by line. It has one subject, states what is wanted, and documents nothing. What can be said in code is said in code, complete; a figure draws what is wanted and nothing of what goes; prose carries only what neither can.
+
+ A review shows lines that landed without his review, so he sees at a glance that they are already in and checks them for a line that would make a flow misbehave.
+
+ An account tells him what happened and how a thing works, the gist first, the rest as long as two sips of coffee allow.
+
+ A change is shown in the margin, never in the text: an added, a removed and a moved line are told apart there, and a proposed change from a landed one.
+
+ Fable writes a proposal, reading the belief modules itself; the flows below publish and land it. Every word of his on a book redoes it; words that open a topic of their own get a proposal of their own.
+
+ A book is one publication of a presentation, at one link. A book he has commented on stays as he saw it; the next publication is a new book at a new link.

### Proposal 2: vision:proposal · psyche-belief › vision/proposal.md, a deleted file

**Destroy** Its concept is in Proposal 1; its fine rules are in knowledge:book.

- ## A proposal
-
- A proposal is a presentation: the prose and the code that describe the system as it will be, shown as changes to belief modules, in the light shades, for the living to rule on.
-
- A proposal lives in its source file and is edited on his comments.
-
- A proposal states what is wanted of the system; it documents nothing.
-
- A proposal is the vision as it will be. A removed line is shown as the text it was, under a red margin, so the edit can be seen, and nothing else is made of it: it is not drawn, not summarised and not shown as a state of anything. A proof, a test, a milestone or a sequence of work is an order, and goes to a bead; written into a proposal it is a vision impurity.
-
- A versioned module is self-contained: everything true of that version is in it, and the version is named once, in its description. Another version is not mentioned.
-
- A proposal is a proposal into belief modules, and the whole of it is its crystallization: what it removes and what it adds.
-
- A proposal has one subject, and small changes that belong together are one subject: one proposal per subject he would judge as one.
-
- A proposal that touches a code component shows the code it changes or adds.
-
- A code block in a proposal stands on its own. It carries the code, why it is important, and what its function is.
-
- A proposal is usually drawn as well as written, and always when it has a shape; a figure draws what is wanted, and nothing of what goes. A flowchart in a proposal is a proposed line like any other: it stands under the addition margin of the proposal it belongs to, which names the module it goes to.
-
- The records a proposal draws from live in an unrendered reference file, one per book, in a references/ directory beside the books; they are archived with the landing when some or all of the proposal is accepted.
-
- The proposal is the center of development: it is the evolution of an idea.
-
- A line removed from a module is shown beside the line that makes it unnecessary.
-
- A question between alternative lines shows each alternative as its own proposal, with the exact lines it lands; the living rules land, amend or reject.
-
- Every word of his redoes the proposal it bears on, unless it closes the topic; words that open a topic of their own get a proposal of their own.
-
- Every type a proposal names is in the proposal: added to the module it lands in, added to another module, or shown as it already stands in its vision module, its definition in full; naming a type is not showing it.
-
- What can be expressed in code is shown as code, with a comment where the code needs one; prose is the comment on the code. A method is shown with the trait it belongs to and that trait's ethos, so its inputs and its yield are read. Code not yet settled is marked tentative. A "never" or an "always" is code: the rule is shown as the code that enforces it.
-
- A shape is a flowchart. Prose carries only what neither code nor chart can. Ethos is the first chart: its types are the nodes and its traits the actions between them.
-
- Code shown is complete: every name it uses is declared in the proposal, a method with its trait in ethos. A type wraps nothing without purpose: a variant carries a type bare when the wrapping would name nothing the type does not.
-
- ```ethos
- Text.String                                   ; what herdr types; made from Waking, held by no struct
- ```
-
- ```rust
- let text = Text(self.waking.datomize(Path::root()).protosize().textualize());   // only the waking becomes text
- ```
-
- ```mermaid
- flowchart TB
-     a["his vision"] -- "is made into" --> b["a proposal (the proposal module's rules)"]
-     b -- "is rendered as" --> c["a book (the book module's rules)"]
-     c -- "is shown to" --> d["him"]
- ```
-
- ## What a proposal shows
-
- A module shown whole, as it stands, situates the landing.
-
- A module shown beside another, both as they stand, serves comparison: psyche with knowledge.
-
- A line replaced shows its removal and its addition together, and only the changed words are marked.
-
- A new module shows whole under a green margin, under the path it will have.
-
- A module deleted shows whole under a red margin, with a Destroy or Archive mark.
-
- A dependency changed shows in the module's front matter: the dependency removed under a red margin, the dependency added under a green margin.
-
- A figure proposed for a module shows under that module's path with a green margin, as an added line does; a fence it replaces, in the module, shows as its lines under a red margin.
-
- ```mermaid
- flowchart TB
-     a["belief module"] -- "stays" --> b["shown whole or beside another"]
-     a -- "changes" --> c["line added with a green margin, removed with a red margin, moved with the third"]
-     a -- "is born or is deleted" --> d["shown whole, under a green or a red margin"]
-     c -- "proposed as" --> e["a proposal: land, amend or reject"]
-     d -- "proposed as" --> e
- ```
-
- ## Who writes a proposal
-
- Fable writes a proposal: the wanted lines and where they go, reading the belief modules itself. Opus publishes it and lands it.

### Proposal 3: vision:review · psyche-belief › vision/review.md, a deleted file

**Destroy** Its concept is in Proposal 1; its fine rules are in knowledge:book.

- ## A review
-
- Spirit, intent and vision land on the living's review: he approves every crystallization. A knowledge or role module may be landed by the machine so the work goes on.
-
- Whatever lands without his review is shown to him afterward, as a review: each line under its repo › path, under the dark shade of green for a line landed added and of red for a line landed removed, so he sees at a glance that it has already landed and checks it for a line that would make a flow misbehave.

### Proposal 4: vision:account · psyche-belief › vision/account.md, a deleted file

**Destroy** Its concept is in Proposal 1; its fine rules are in knowledge:book.

- ## Account
-
- An account tells the living what happened and how a thing works: how a fault was found, what it was, how it was fixed. He reads it to understand, trusting the machine to know how things work; it explains, and where a vision proposal truly arises in it, that part is marked as one.
-
- An account is read between two sips of coffee: its first lines give the gist, we found a bug and we fixed it, and the explanation of how is as long as that leaves.

### Proposal 5: vision:book · psyche-belief › vision/book.md, a deleted file

**Destroy** Its concept is in Proposal 1; its fine rules are in knowledge:book.

- ## Publishing
-
- The publisher builds the source as it was handed and publishes the page; it authors nothing and enforces nothing, and the book is as correct as its author made it.
-
- ## A commented book stays
-
- A book is one publication of a presentation, at one link. A book the living has commented on stays as he saw it; what his comments change goes into the source, and the next publication is a new book at a new link.
