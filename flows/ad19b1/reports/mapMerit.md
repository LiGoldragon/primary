# The existential merit of the key-value map

Research delegated by the main flow: who has questioned whether the
key-value map deserves to exist as a data structure distinct from a
vector of two-field structs, and what the strongest counter-arguments
are.

Method: web search and direct fetch of primary sources. Every claim
below carries author, title, year and URL. Quotes marked with `>` were
read in a document I fetched in this flow. Where a source was fetched
by a nested research subflow rather than by me, the section says so;
those subflows were instructed to fetch primaries and to mark what
they could not verify, and their marks are carried through unchanged.
Sections headed **Inference** are mine and were not witnessed in any
source.

One transcription caveat applies throughout. Several primaries exist
only as scanned or two-column PDFs. Where text was extracted from such
a PDF, subscripts, mathematical symbols and column order come out
mangled, and I have normalised them (for example Codd's "X1, S, , . . .
, S," back to "S1, S2, ..., Sn", and the Third Manifesto's "n  0" back
to "n ≥ 0"). The words are as read; the notation is reconstructed.
Sources affected are named as such at the point of use and in §12.

The living's notation is also named `datom`. Section 6 reports only
what Rich Hickey's `datom` is in Datomic. No connection is assumed and
none was found.

---

## What the research found, in short

- The reduction is old and mainstream. Set theory defines a function as
  a set of ordered pairs with a uniqueness condition (§1). Codd's own
  footnote 8 in the 1970 paper says "A function is a binary relation,
  which is one-one or many-one, but not one-many" (§2.1).
- The reduction runs both ways, and the *reverse* is at least as well
  attested. Date and Darwen define a tuple — the struct — as a set of
  ⟨attribute, type, value⟩ triples, i.e. as a map (§2.2). The Alice book
  says a tuple "is a total mapping from U to dom" (§7). Nix and CUE have
  one construct serving as both record and map (§8.5). Castagna's ICFP
  2023 paper opens "Records are finite functions from keys to values"
  and argues the two should share one type, not that either should go
  (§9).
- Several real notations already define the map as a vector of
  two-field structs, not as an argument but as a definition: Dhall's
  `Map = λ(k) → λ(v) → List { mapKey : k, mapValue : v }` (§8.1) and
  protobuf's `map<K,V>` desugaring normatively to
  `repeated MapFieldEntry { key = 1; value = 2; }` (§8.2). YAML's
  ordered-map and duplicate-pairs types are Kind: Sequence, not Kind:
  Mapping (§8.3).
- Every serious implementation of a map is already an array of entries
  plus an index, and drops the index below a small threshold: CPython
  and PyPy's compact dict (§5.1), Rust's indexmap (§5.2), C++23's
  `flat_map` (§5.3), Zig's `ArrayHashMap`, which literally linear-scans
  until the entries outgrow a cache line (§5.4). Erlang's own EEP 43
  chose the same two-tier design (§3.4).
- Two independent traditions converged on the *same* representation:
  keys in one vector, values in another. Whitney's q ("Dictionaries are
  maps of lists to lists"; "a table is a list of similar dicts"; the
  flip "is never carried out") — §4 — and O'Keefe's Erlang frames (a
  shared key tuple plus a value vector) — §3.3.
- The strongest arguments for keeping a distinct map are: key
  uniqueness is a real invariant and the vector→map conversion is lossy,
  which is why every notation has to publish a duplicate-key rule
  (§10.1); unorderedness is a guarantee, not an omission (§10.2); lookup
  semantics need somewhere to live (§10.3); and keys are often not
  strings (§10.4).
- The strongest argument *for the vector* that the research turned up is
  one the brief did not anticipate: alists, plists and Erlang proplists
  permit duplicate keys and give them a **shadowing** rule, and both the
  Common Lisp standard and the Erlang proplists documentation name that
  as the use rather than the defect (§3.1, §3.2). Leijen's scoped labels
  is the type-theoretic form of the same idea (§9).
- The closest thing to a person arguing outright that the distinct map
  type is unnecessary is Robert Virding on erlang-questions in 2013:
  "this fascination with *NATIVE* implementations. Why *native*? … I see
  it as a solution to a problem which is at worst only very small."
  (§3.5). Richard O'Keefe, on the other side of the same thread, gives
  the cleanest statement of why the two should stay apart:
  "Clearly distinguishing between record-like data structures and
  dictionary-like data structures is the core of good design in this
  area."
- No single canonical essay arguing "the map is a degenerate relation"
  or "a language needs only structs and vectors" was found. The claim
  exists piecemeal and is usually made by doing rather than by arguing
  (§12).

---

## 1. The set-theoretic thread: a function *is* a set of ordered pairs

This is the oldest form of the claim, and it is not a critique — it is
the standard definition. In classical set theory a map is not a
structure at all; it is a set of pairs carrying one extra condition.

Herbert B. Enderton, *Elements of Set Theory*, Academic Press, 1977,
Chapter 3 "Relations and Functions" (fetched as PDF):

> You have probably guessed that for us a relation will be a set of
> ordered pairs. And there will be no further restrictions; any set of
> ordered pairs is some relation, even if a peculiar one.
>
> **Definition** A relation is a set of ordered pairs.

and, a few pages later:

> But the simplest procedure is to take this set of ordered pairs to be
> the function. Thus a function is a set of ordered pairs (i.e., a
> relation). But it has a special property: It is "single-valued," i.e.,
> for each x in its domain there is a unique y such that x↦y. We build
> these ideas into the following definition.
>
> **Definition** A function is a relation F such that for each x in
> dom F there is only one y such that xFy.

Wikipedia's "Function (mathematics)" article states the same thing in
the modern formulation (fetched):

> A function with domain X and codomain Y is a binary relation R
> between X and Y that satisfies the two following conditions: For
> every x in X there exists y in Y such that (x, y) ∈ R. If (x, y) ∈ R
> and (x, z) ∈ R, then y = z.

**What this supports.** A finite map is exactly a finite set of pairs
plus single-valuedness. It supports the reduction, but note the two
things the definition insists on that a *vector* of pairs does not
give: the collection is a **set** (unordered, duplicate-free at the
pair level) and it is **single-valued** (duplicate-free at the key
level). The mathematical reduction is to a *set* of pairs, never to a
*sequence* of pairs.

**Inference.** The set-theoretic tradition therefore argues for
"map = relation + uniqueness", not for "map = vector of structs". The
step from set to vector is a separate step, and it is the step that
introduces order and permits duplicates.

---

## 2. The relational thread: Codd, Date & Darwen, Stonebraker

### 2.1 Codd, 1970

E. F. Codd, "A Relational Model of Data for Large Shared Data Banks",
*Communications of the ACM* 13(6), June 1970 (fetched as PDF).

Codd defines a relation as the mathematics does:

> The term relation is used here in its accepted mathematical sense.
> Given sets S1, S2, ..., Sn (not necessarily distinct), R is a relation
> on these n sets if it is a set of n-tuples each of which has its first
> element from S1, its second element from S2, and so on. […] More
> concisely, R is a subset of the Cartesian product S1 × S2 × ... × Sn.

And in footnote 8, on the same page as his discussion of joins, he
states the identification directly:

> A function is a binary relation, which is one-one or many-one, but
> not one-many.

(The PDF's two-column OCR scatters this footnote across three
fragments; all three were located and reassembled in reading order.)

That is Codd himself saying a map is a two-column relation with a
uniqueness constraint on the first column.

Codd goes further and models what a modern programmer would call a
nested map as a nested binary relation:

> For example, one of the domains on which the relation employee is
> defined might be salary history. An element of the salary history
> domain is a binary relation defined on the domain date and the domain
> salary. The salary history domain is the set of all such binary
> relations.

He then argues these nested (non-simple) domains should be normalised
away.

Two Codd passages cut the *other* way, against a purely key-value view:

- The removal of **ordering dependence** is his first stated goal.

  > Three of the principal kinds of data dependencies which still need
  > to be removed are: ordering dependence, indexing dependence, and
  > access path dependence.

  His array picture of a relation is explicitly labelled non-essential:
  "(2) The ordering of rows is immaterial."

- He argues *against* reducing everything to binary relations, which is
  what a pure key-value model does:

  > To support symmetric exploitation of a single binary relation, two
  > directed paths are needed. For a relation of degree n, the number of
  > paths to be named and controlled is n factorial.
  >
  > Again, if a relational view is adopted in which every n-ary relation
  > (n > 2) has to be expressed by the user as a nested expression
  > involving only binary relations (see Feldman's LEAP System [10], for
  > example) then 2n − 1 names have to be coined instead of only n + 1
  > with direct n-ary notation.

  "Symmetric exploitation" is Codd's term for being able to query by
  any column:

  > Once a user is aware that a certain relation is stored, he will
  > expect to be able to exploit it using any combination of its
  > arguments as "knowns" and the remaining arguments as "unknowns,"
  > because the information (like Everest) is there.

  A map gives you one direction only.

### 2.2 Date & Darwen: the struct *is* a map

C. J. Date and Hugh Darwen, *Databases, Types, and the Relational
Model: The Third Manifesto* (the TTM text at Warwick, copyright 2014;
fetched as PDF from https://www.dcs.warwick.ac.uk/~hugh/TTM/DTATRM.pdf).

This is the sharpest reversal found anywhere in the research. Date and
Darwen define a **tuple** — the struct — as a **set of ordered
triples**, i.e. as a map from attribute name to (type, value):

> Given a collection of types Ti (i = 1, 2, ..., n, where n ≥ 0), not
> necessarily all distinct, a tuple value (tuple for short) over those
> types — t, say — is a set of n ordered triples of the form
> ⟨Ai,Ti,vi⟩, where Ai is an attribute name, Ti is a type name, and vi
> is a value of type Ti.

RM Prescription 9 (Tuples) states it prescriptively:

> A heading H is a set of ordered pairs or attributes of the form
> ⟨A,T⟩, where: a. A is the name of an attribute of H. No two distinct
> pairs in H shall have the same attribute name. […]
>
> Now let t be a set of ordered triples ⟨A,T,v⟩, obtained from H by
> extending each ordered pair ⟨A,T⟩ to include an arbitrary value v of
> type T […]. Then t is a tuple value (tuple for short) that conforms
> to heading H

and RM Prescription 10 (Relations) makes the relation a set of those:

> A relation value r (relation for short) consists of a heading and a
> body, where: a. The heading of r shall be a heading H as defined in
> RM Prescription 9 […] b. The body of r shall be a set B of tuples,
> all having that same heading H.

Consequences they draw explicitly:

> There is no left-to-right ordering to the components of a tuple. This
> property follows because a tuple has a set of components, and sets in
> mathematics have no ordering to their elements.

> Relations have no top-to-bottom ordering to their tuples and no
> left-to-right ordering to their attributes

and RM Proscription 1:

> D shall include no concept of a "relation" whose attributes are
> distinguishable by ordinal position. Instead, for every relation r
> expressible in D, the attributes of r shall be distinguishable by
> name.

On the key: a candidate key is precisely the uniqueness condition, and
they connect it to functional dependency:

> Because of the uniqueness property, the functional dependency (FD)
> K → A holds for every attribute A of R.

**Inference.** In TTM the containment runs the opposite way to the
proposition being researched. A struct is a map (attribute name →
value, names unique, no order); a table is a *set* of structs. If one
takes TTM seriously, "a map is a vector of structs" and "a struct is a
map" are both true, and the pair of them says the two notions are
mutually definable rather than that one is redundant.

### 2.3 Stonebraker: the key-value store as a two-column table with no query language

Michael Stonebraker, "Why Enterprises Are Uninterested in NoSQL",
BLOG@CACM, September 30, 2010. The live URL is behind Cloudflare and
returned 403; text fetched from the Internet Archive snapshot of
`cacm.acm.org/blogs/blog-cacm/99512-why-enterprises-are-uninterested-in-nosql/fulltext`.

> **A Low-Level Query Language is Death**
>
> Data warehouses are subject to frequent ad-hoc queries like "Tell me
> whether pet rocks are selling better than Barbie dolls in the south?"
> Ted Codd's pioneering paper, "A Relational Model of Data for Large
> Shared Data Banks," in 1970 advocated a user interface whereby one
> stated what is required and not how to fetch it from disk. In the
> subsequent 40 years of DBMS activity, high-level languages, like SQL,
> have been shown to offer ease of programming for such ad-hoc data
> warehouse inquiries. My enterprise guru's company is rarely interested
> in the algorithmic record-at-a-time interfaces seen in most NoSQL
> products, as they are seen as a throwback to the days of IMS and
> CODASYL.

> Most have a data model, which is unique to that system, along with a
> one-off, record-at-a-time user interface.

He closes:

> "Those who do not understand the lessons from previous generation
> systems are doomed to repeat their mistakes."

The explicit "two columns and nothing else" characterisation is in
Michael Stonebraker and Rick Cattell, "Ten Rules for Scalable
Performance in 'Simple Operation' Datastores", *Communications of the
ACM* 54(6), June 2011 (fetched as PDF from
http://www.cattell.net/datastores/CACM-Paper.pdf):

> 1. Key-value stores, including Dynamo, Voldemort, Tokyo Cabinet,
> Scalaris, and Riak. These systems have the simplest data model: a
> collection of objects, each with a key and a payload. They provide
> little or no ability to interpret the payload as a multi-attribute
> object, and there is no query mechanism for non-primary attributes.

Their Rule #2 is the general form of the critique:

> **Rule #2: High-level languages are good and need not hurt
> performance**
>
> In the 1960's and 1970's, hierarchical and network systems were the
> dominant DBMS solutions, offering a low-level procedural interface to
> data. The high-level language of RDBMSs were instrumental in
> displacing these DBMSs because: A high-level language system requires
> the programmer to write less code that is easier to understand. A user
> states what he wants instead of writing a disk-oriented algorithm on
> how to access the data he needs. […] A high-level language system has
> a better chance of allowing a program to survive a change in the
> schema without maintenance or recoding.

**Note.** Stonebraker's target is the key-value *database*, not the
key-value type in a programming language. The transferable part of the
argument is that a two-column keyed structure gives up query by
anything but the key, which is Codd's "symmetric exploitation" point.

### 2.4 The relational-model-as-programming argument

Ben Moseley and Peter Marks, "Out of the Tar Pit", 2006 (fetched as PDF
from https://curtclifton.net/papers/MoseleyMarks06a.pdf). Section 8:

> The relational model [Cod70] has — despite its origins — nothing
> intrinsically to do with databases. Rather it is an elegant approach
> to structuring data, a means for manipulating such data, and a
> mechanism for maintaining integrity and consistency of state. These
> features are applicable to state and data in any context.

> As mentioned above, relations provide the sole means for structuring
> data in the relational model. A relation is best seen as a homogeneous
> set of records, each record itself consisting of a heterogeneous set
> of uniquely named attributes […]
>
> Implications of this definition include the fact that — by virtue of
> being a set — a relation can contain no duplicates, and it has no
> ordering.

> The idea of structuring data using relations is appealing because no
> subjective, up-front decisions need to be made about the access paths
> that will later be used to query and process the data.

A modern instance: Molham Aref et al., "Rel: A Programming Language for
Relational Data", arXiv:2504.10323, 2025 (fetched as PDF). Rel enforces
sixth normal form, which reduces every relation to one of exactly two
shapes:

> Indeed, GNF requires each relation to be in 6NF, which means that:
> • the set of all its columns is its unique key, or
> • the set of all its columns except one is its unique key.
> We can view such a relation as either a set of distinct composite keys
> k̄, or a set of key-value pairs (k̄, v) representing a function that
> maps keys k̄ to atomic values v.

That is a working language in which every structure is either a set of
keys or a set of key-value pairs, and there is no separate map type
because everything already is one.

D. Richard Hipp / SQLite, "SQLite As An Application File Format"
(https://www.sqlite.org/appfileformat.html, no date on page) argues the
same direction for file formats:

> Any application state that can be recorded in a pile-of-files can also
> be recorded in an SQLite database with a simple key/value schema like
> this:
>
>     CREATE TABLE files(filename TEXT PRIMARY KEY, content BLOB);
>
> […] But an SQLite database is not limited to a simple key/value
> structure like a pile-of-files database.


---

## 3. Lisp and Erlang: the map that was a list of pairs for fifty years

Gathered partly by me and partly by a nested research subflow; both
fetched primaries and the two sets of quotes agree where they overlap.

### 3.1 Common Lisp: an alist *is* a list of conses, and duplicates shadow

ANSI Common Lisp HyperSpec, §14.1.2.1 "Lists as Association Lists"
(http://www.lispworks.com/documentation/HyperSpec/Body/14_aba.htm), and
the identical glossary entry
(http://www.lispworks.com/documentation/HyperSpec/Body/26_glo_a.htm):

> An association list is a list of conses representing an association of
> keys with values, where the car of each cons is the key and the cdr is
> the value associated with that key.

Glossary, "property list"
(http://www.lispworks.com/documentation/HyperSpec/Body/26_glo_p.htm):

> **property list** n. 1. a list containing an even number of elements
> that are alternating names (sometimes called indicators or keys) and
> values (sometimes called properties). When there is more than one name
> and value pair with the identical name in a property list, the first
> such pair determines the property.

Note where this sits in the standard: under "Conses as Lists". The
standard does not define a map and then implement it as a list; it
defines the list and then describes a *use* of lists.

Guy L. Steele Jr., *Common Lisp the Language*, 2nd edition, §15.6
(https://www.cs.cmu.edu/Groups/AI/html/cltl/clm/node153.html), states
the shadowing property as an advantage:

> An association list, or a-list, is a data structure used very
> frequently in Lisp. An a-list is a list of pairs (conses); each pair is
> an association. The car of a pair is called the key, and the cdr is
> called the datum.

> An advantage of the a-list representation is that an a-list can be
> incrementally augmented simply by adding new entries to the front.
> Moreover, because the searching function assoc searches the a-list in
> order, new entries can "shadow" old entries.

and makes `acons` a triviality over `cons`:

> (acons x y a) == (cons (cons x y) a)

The construction goes back to the beginning. McCarthy, Abrahams,
Edwards, Hart and Levin, *LISP 1.5 Programmer's Manual*, MIT Press,
1962, §7.3 (PDF fetched from
https://www.softwarepreservation.org/projects/LISP/book/LISP%201.5%20Programmers%20Manual.pdf;
text is OCR-extracted and the sentinel is printed with a subscript 8):

> Every atomic symbol has a property list. When an atomic symbol is read
> in for the first time, a property list is created for it.
>
> A property list is characterized by having the special constant 77777_8
> (i.e., minus 1) as the first element of the list. The rest of the list
> contains various properties of the atomic symbol. Each property is
> preceded by an atomic symbol which is called its indicator.

Peter Norvig, *Paradigms of Artificial Intelligence Programming*, 1992,
ch. 3 (https://github.com/norvig/paip-lisp/blob/main/docs/chapter3.md)
states the equivalence directly:

> Property lists (sometimes called p-lists or plists) and association
> lists (sometimes called a-lists or alists) are similar:
>
>     a-list: ((key1 . val1) (key2 . val2) ... (keyn . valn))
>     p-list: (key1 val1 key2 val2 ... keyn valn)
>
> Given this representation, there is little to choose between a-lists
> and p-lists. They are slightly different permutations of the same
> information. The difference is in how they are normally used.

He is not a partisan of them, and says why:

> Property lists have a long history in Lisp, but they are falling out of
> favor as new alternatives such as hash tables are introduced. There are
> two main reasons why property lists are avoided. First, because symbols
> and their property lists are global, it is easy to get conflicts when
> trying to put together two programs that use property lists. … Second,
> property lists are messy.

and in ch. 10 gives the size threshold that §5 finds everywhere:

> An association list is perhaps the simplest: it is just a list of
> key/value pairs. It is appropriate for small tables, up to a few dozen
> pairs. The hash table is designed to be efficient for large tables, but
> may have significant overhead for small ones.

Peter Seibel, *Practical Common Lisp*, 2005, ch. 13, "Lookup Tables:
Alists and Plists"
(https://gigamonkeys.com/book/beyond-lists-other-uses-for-cons-cells.html):

> Under the covers, an alist is essentially a list whose elements are
> themselves cons cells. Each element can be thought of as a key/value
> pair with the key in the cons cell's CAR and the value in the CDR.

> Structurally a plist is just a regular list with the keys and values as
> alternating values.

> While you wouldn't use either alists or plists for large tables--for
> that you'd use a hash table--it's worth knowing how to work with them
> both because for small tables they can be more efficient than hash
> tables and because they have some useful properties of their own.

> However, since the basic mechanism for alists is so lightweight, for
> small tables an alist can outperform a hash table.

### 3.2 Erlang proplists: the same design, with shadowing named as the point

Erlang/OTP `stdlib`, `proplists` module documentation
(https://www.erlang.org/doc/apps/stdlib/proplists.html):

> Property lists are ordinary lists containing entries in the form of
> either tuples, whose first elements are keys used for lookup and
> insertion, or atoms, which work as shorthand for tuples {Atom, true}.
> (Other terms are allowed in the lists, but are ignored by this module.)
> If there is more than one entry in a list for a certain key, the first
> occurrence normally overrides any later (irrespective of the arity of
> the tuples).

> Property lists are useful for representing inherited properties, such
> as options passed to a function where a user can specify options
> overriding the default settings, object properties, annotations, and so
> on.

The first words are "ordinary lists". There is no proplist *type* in
Erlang, only a module of functions over lists.

**Inference.** This is the sharpest *pro*-vector argument found
anywhere. Both the Common Lisp standard and the Erlang documentation
name the duplicate-key case as the use, not the defect: a list of pairs
is a stack of scopes. Convert it to a map and the override history is
gone.

### 3.3 Frames — by Richard O'Keefe, not Joe Armstrong

**Correction to the brief.** The frames proposal is Richard A.
O'Keefe's. EEP 43 says so in as many words; the document is O'Keefe's;
and the erlang-questions thread "Frames proposal" (29 December 2012,
http://erlang.org/pipermail/erlang-questions/2012-December/071395.html)
quotes O'Keefe defending it. There is also **no EEP for frames** — the
subflow grepped the raw erlang.org EEP index for "frame" and "struct"
and found zero hits. Frames remained a standalone PDF.

Joe Armstrong's counterpart idea is called **"proper structs"** and is
dated to 2001 by O'Keefe. Armstrong's own write-up of it could not be
located and is **unverified**; O'Keefe's §8.3 is the only sourced
description.

Richard A. O'Keefe, "No more need for records", Computer Science,
University of Otago, November 2003, fifth draft May 2012 (54-page PDF
fetched from https://www.cs.otago.ac.nz/staffpriv/ok/frames.pdf):

> In this report I propose a new compound data type, with a long history
> in other programming languages, which can be used as a replacement for
> the -record construct. This data type has the same storage requirements
> as records, but does not require textual coupling between Erlang
> modules, and is more robust against change, and provides full run-time
> access to field names for printing and version change.

§5, "So what are 'frames'?":

> Frames are semantically immutable association lists: finite partial
> functions from the space of Erlang atoms to the space of Erlang terms.
> In other words, a frame is a finite set of (key,value) pairs such that
> values are any Erlang terms, keys are all atoms, and no two keys are
> equal.

> Similar but mutable (or further instantiable for LIFE and IBM PROLOG)
> data structures have been known by various names in various languages:
> "tables" in SNOBOL, "Dictionaries" in Smalltalk, "associative arrays"
> in AWK, "hashes" in Perl, "psi-terms" in LIFE, "items" in IBM PROLOG,
> "feature structures" in linguistics, and who knows what elsewhere.

and, in the same section, the attribution to Armstrong:

> The idea of this data type occurred to me a day after I first read
> about Erlang records, but I did not write it up until September 2003.
> It turns out that Joe Armstrong had also thought of this data type, and
> wrote something about it in 2001. I had not then seen what he wrote. He
> uses the name "proper structs" and slightly different syntax. I do not
> know how he intended them to be implemented.

§13, "Implementation" — first the naive representation, which is a
sorted plist inside a tuple:

> An obvious way is to use a representation identical to tuples except
> for the tag on the pointer. Keys and values would be stored with the
> keys in strictly ascending order. In effect, ⟨n,K1,V1,...,Kn,Vn⟩.

then the one he proposes: a **shared key tuple** plus a **value
vector**:

> A frame F = ⟨{k1 ∼ V1, . . . , kn ∼ Vn}⟩ is represented by a tagged
> pointer to a vector ⟨P, V1, . . . , Vn⟩ where P points to a tuple
> {k1, . . . , kn}.

> The key tuple literal is part of the module's constant pool. All the
> frame-making expressions in a module with the same set of keys could
> and should share the same key tuple.

with the consequence that reading the key set is free:

> In particular, the tuple of keys is sorted. Cost: O(1). […] with the
> implementation I have in mind, this is an O(1) operation because the
> key tuple is already there

§10, "Why not use the dict module?", records the "existing structures
suffice" position and O'Keefe's rebuttal. He attributes the position to
Chris Pressey (whose original posts were not retrieved — **unverified**):

> Chris Pressey has forcibly argued in the Erlang mailing list that the
> dict module should be used. … His view is that the compiler could
> support such syntax on top of whatever concrete implementation dict
> uses; and if that implementation is not satisfactory, then dict could
> have a new implementation, that being the point of using abstract data
> types.

> The basic answer is that dict and frames are designed to do different
> jobs. They have different implementation tradeoffs. You can't make dict
> good for the record-like uses that frames are meant for without making
> it bad for its existing uses.

> Frames are supposed to be small, cheap, fast, immutable. You are
> supposed to be able to have millions of them.

He also quotes the Erlson library's own documentation, which states the
identity outright:

> At runtime, Erlson dictionaries are represented as a list of {Name,
> Value} tuples ordered by Name. This way, each Erlson dictionary is a
> valid proplist and orddict in terms of the corresponding stdlib
> modules.

**Inference.** O'Keefe's frame is exactly the array-language dictionary
of §4 and the struct-of-arrays of §5, arrived at independently: keys in
one vector, values in another, the key vector shared across every
instance of the same shape. It is what a "vector of two-field structs"
becomes once the repeated key column is factored out.

### 3.4 EEP 43: why Erlang added maps anyway

Björn-Egil Dahlberg, "EEP 43: Maps", created 4 April 2013, Final,
implemented in OTP 17.0 (https://www.erlang.org/eeps/eep-0043.html).

The abstract acknowledges frames and states the disagreement:

> From the community there has been many wishes of a Map like data-type
> and a few suggestions. The one suggestion that stands out is of course
> the Frames proposal from Richard O'Keefe. It is the most complete
> proposal I've seen and is very well thought out. Its goal is to be a
> record replacement and the proposal satisfies this goal very well.
>
> If Frames are that good, why a separate EEP?
>
> It boils down to goals and constraints. A record replacement is just
> that, a replacement. It's like asking the question, "What do we have?"
> instead of "What can we get?" The instant rebuttal would be "What do we
> need?" I say Maps.

The Motivation section is the direct answer to "why a map when a list
of pairs will do":

> Why would we need maps when we have records, dicts, gb_trees, ets and
> proplists?
>
> Maps are envisioned to be an easy to use, lightweight yet powerful
> key-value association store.
>
> Maps utilizes one of Erlang's major strengths, pattern matching, to
> enrich user experience and provide a powerful tool to simplify code
> development. Pattern matching gives Maps a clear edge over dicts,
> gb_trees or proplists in usability.
>
> Maps provides the possibility to associate arbitrary terms as keys, not
> only atoms, with arbitrary terms as values in a matching capable
> data-type.
>
> Maps does not claim to be an replacement to records as the frames
> proposal does. Instead maps targets a larger usage domain and wishes to
> be a complement to records and supersede them where suitable.

Its assessment of records is worth having whole:

> Records are powerful under the right circumstances: fast lookups, O(1),
> due to compile time indexing of keys, and fast stores for small record
> sizes (~50 values), no memory overhead to store keys, only values and a
> name: 2 + N words consumption, ease of use in function head matching.
>
> However some of the drawbacks are: compile-time dependency and forces
> header file inclusions for inter-module usage, only atoms as keys, keys
> are not accessible in runtime, no dynamic access of values, i.e. we
> cannot use variables to access values, it is not a data-type and cannot
> be distinguished from tuples.

> Being faster than direct-indexing array, where indices and possibly the
> resulting value are determined at compile time, is hard. In fact it is
> impossible.

EEP 43 concedes the frames representation is the efficient one and
rejects it for a stated reason:

> A memory model for Maps where the efficiency was near that of records
> could be achieved by essentially using two tuples, one for keys and one
> for values as demonstrated in Frames. This would be impact performance
> of updates on Maps with a large number of entries and thus constrain
> the capability of a dictionary approach.

> Maps would then stores keys together with its values whereas frames
> stores keys outside its value structure and records generates key
> indexes at compile-time. This would indicate a memory overhead for Maps
> over Frames and records for each instance.

Its resolution is the two-tier design §5 finds everywhere:

> Proposal: Two tier approach, similar to binaries. Use flat compact,
> key-sharing approach for few associations (~50 associations). Use
> sorted tree approach and store keys with values beyond first tier
> limit. The rationale being it is more likely to have multiple instance
> where we have few keys.

### 3.5 The 2013 mailing-list debate

Richard O'Keefe, erlang-questions, 9 May 2013
(http://erlang.org/pipermail/erlang-questions/2013-May/073667.html),
replying to "map is just new name for frames":

> ABSOLUTELY *NOT*!
> The desire for O(lg N) update forces some crucial implementation
> differences.
> For record-like uses, frames would be smaller, faster, and safer than
> maps.
> For dictionary-like uses, maps would be superior to frames.
> Clearly distinguishing between record-like data structures and
> dictionary-like data structures is the core of good design in this
> area.

> The Maps proposal is about *breadth* (a jack of all trades data
> structure) and *expressiveness*.

Robert Virding, erlang-questions, 14 May 2013
(http://erlang.org/pipermail/erlang-questions/2013-May/073724.html), is
the closest thing found in the whole research to a direct statement of
the position the brief asks about — that the distinct built-in map type
is unnecessary:

> One thing that has always puzzled me in these discussions is this
> fascination with *NATIVE* implementations. Why *native*? What is it
> with *native* that makes people want it? Is it the speed? Or is it the
> special syntax? Or what? Why care HOW things are done just as long as
> it fulfils my requirements. … People complain that you need a special
> data type or else you can get them mixed up. I don't buy that. I work
> with lists, tuples, proplists, orddicts, dicts, gb_trees, records, etc
> together in one application and one problem I don't have is getting
> them mixed up. I see it as a solution to a problem which is at worst
> only very small.

> One of the ideas behind dicts/orddicts was to provide a standardised
> API which would allow you to choose and easily change which
> implementation you need/want. … One of the bad things of having a
> built-in type is that you don't have think, but you won't always get
> the most suitable. And seriously thinking about your data structures is
> always a Good Thing.

Loïc Hoguin, erlang-questions, 10 May 2013
(http://erlang.org/pipermail/erlang-questions/2013-May/073674.html):

> Records work good enough for most purposes, with the exception of
> upgrades, which few people do anyway.

> Maps have the potential to replace proplists, dicts, and also some
> record misuses, where an interface requires you to include a file to
> have the records definition (the file example found in the EEP is one).

Joe Armstrong, erlang-questions, 13 May 2013
(http://erlang.org/pipermail/erlang-questions/2013-May/073700.html),
argues *for* maps, and twice credits O'Keefe's key-sharing idea:

> ':=' means "update an existing key - crash if they key is not present"
> '=>' means "update an existing key OR add a new key"
>
> This is good idea (ROK suggested this in his frames paper) since we
> don't want too accidentally create a new key due to a spelling error.

> Will succeed, but more importantly the new map has exactly the same
> keys as the old map (since all the updates are ':=' updates) - and so
> can *share* the same key descriptor. So if we have a very long list of
> maps they can be stored in a space efficient manner. (Again this idea
> comes from ROKs frames paper).

**Inference.** Erlang ran this exact argument out in public for a
decade and settled it by keeping both: a map type in the language,
implemented as a flat key-sharing vector below about 32–50 entries and
as a tree above it. The reasons given for wanting a distinct type were
pattern matching, arbitrary terms as keys, and being distinguishable
from a tuple at runtime — none of which a bare vector of two-field
structs supplies. O'Keefe's line is the one that separates the two
questions most cleanly: distinguishing record-like from
dictionary-like structure is "the core of good design in this area".

---

## 4. The array languages: APL, J, K and q

This section was gathered by a nested research subflow, which fetched
each source and marked what it could not verify.

### 4.1 Arthur Whitney's own manual

Arthur Whitney, "Abridged Q Language Manual", Kx Systems, listed by KX
as 2009 (https://github.com/KxSystems/kdb/blob/master/d/a/q.htm). Its
whole section 5, "Dict and Table", is two sentences:

> Dictionaries are maps of lists to lists. A table is a list of similar
> dicts(records).

with the annotated lines:

> d:`x`y!(`a;2)              / a dict is a map from a list to a list
> f:(d;`x`y!(`b;3))          / a table is a list of dictionaries
> f:flip`x`y!(`a`b;2 3)      / same table as flip of dict of lists
> A keyed table is a dict whose key and value are both tables.

and the type shorthand:

> l list
> L list of l(matrix)
> r record/row (S!l)
> R list of r(table)
> K R!R(keyed table)

### 4.2 Kx's reference manual

Don Orth, "Q Language Reference Manual", Kx Systems, listed by KX as
2006 (https://github.com/KxSystems/kdb/blob/master/d/a/q1.htm):

> Associations are the only primitive datatype that has no syntactic
> form; associations are created with the primitive dyadic function
> denoted by ! and called Xkey. Associations are associative lists; the
> items of the left argument to Xkey are the indices, or keys, and the
> items of the right argument are the values. The left and right
> arguments must have the same length.

Its section headings are the claim itself:

> 12.1.1 A Table is a List of Dictionaries
> 12.1.2 A Table is the Flip of a Dictionary
> 12.2 A Key Table is a Dictionary

> One last point: even though a table is the flip of a dictionary, the
> flip is never carried out.

> A key table is not a table, but a pair of tables instead. The primary
> key columns form one table and the data columns the other.

### 4.3 Current kdb+/q documentation and Q for Mortals

"Dictionaries & tables", kdb+ and q documentation, KX
(https://code.kx.com/q/basics/dictsandtables/):

> A list is a mapping from its indexes to its items.
>
> A dictionary is a mapping from a list of keys to a list of values.

"flip" reference (https://code.kx.com/q/ref/flip/):

> The flip of a dictionary is a table, and vice versa.

Jeffry A. Borror, *Q for Mortals* (hosted by KX), §5 Dictionaries
(https://code.kx.com/q4m3/5_Dictionaries/):

> A dictionary is an association between a list of keys and a list of
> values. Logically it can also be considered as key-value pairs but it
> is stored physically as a pair of lists.

§8 Tables (https://code.kx.com/q4m3/8_Tables/):

> Is a table a flipped column dictionary or a list of records? Logically
> it is both, but physically it is stored as a column dictionary.

> The only effect of flipping the column dictionary is to reverse the
> order of its indices; no data is rearranged under the covers.

**Inference.** In q the two candidate structures — "vector of records"
and "dictionary of columns" — are the same value under a free
transposition, and the notation exposes both readings. The primitive
underneath is neither; it is a pair of lists.

### 4.4 K2 (1998) and K9

K Reference Manual, Kx Systems, Version 2.0, 1998 (PDF; the subflow
decoded the PDF's compressed text streams itself, so spacing in these
quotes is approximate). The monadic `.` verb, "Make / Unmake
Dictionary":

> Create a dictionary from a list x of a special form, or create a list
> of that form from a dictionary x.

> If x is a list as described above then .x is a dictionary whose
> entries are the first items of the items of x

That is a dictionary defined as an involution on a nested list of
(name; value; attributes) triples — a different construction from the
K4/q two-vector one, same principle.

The community-maintained K9 reference card (https://kparc.github.io/ref;
authorship not established as Whitney's):

> A table is a list of dicts where each dict has the same keys in the
> same order.
>
> A table can also be considered as a flipped dict of lists, where each
> list is of equal length.
>
> Key tables are dictionaries where the rows of one table map to the
> rows of another table.

### 4.5 APL and J: no dictionary type at all

Dyalog Ltd., dfns workspace documentation, "association lists"
(https://dfns.dyalog.com/n_alists.htm):

> An association list (AKA: dictionary, symbol table, look-up table) is
> a classic and generally useful structure. It is implemented here as a
> pair of vectors of keys and values.

with the implementation being index-of into the key vector:

> alget←{keys vals←⍺ ⋄ (keys⍳⊂⍵)⊃vals}

J Wiki, "Vocabulary/Nouns" (https://code.jsoftware.com/wiki/Vocabulary/Nouns):
the complete J type table lists Boolean, integer, extended integer,
rational, float, integer2, integer4, long float, complex, byte,
unicode, unicode4, boxed, symbol and the sparse variants. There is no
dictionary, map or associative type.

J Wiki, "Essays/DataStructures"
(https://code.jsoftware.com/wiki/Essays/DataStructures):

> J's default data structure is array. However, you might want to use
> other data structures that are common to other languages.
>
> AA provides O(1), i.e. constant time, lookup. You can emulate AA in J
> in several ways.

The three emulations given are `m&i.` (index-of against a key array),
sparse arrays, and names in a locale.

**Unverified.** The subflow could not fetch docs.dyalog.com or
aplwiki.com (both 403), so Dyalog's formal array-type roster is not
witnessed; the "Dyalog has no dictionary type" reading rests on the
dfns page's framing. A search result claiming dzaima/APL adds
dictionaries natively is unverified. No paper by Whitney titled "A
Business Oriented Language" or "An APL Machine" was found on KX's own
archive page; "An APL Machine" is likely Philip Abrams' 1970 Stanford
thesis and should not be cited to Whitney without checking.


---

## 5. The implementation thread: the map is an array of entries plus an index

This section was gathered by a nested research subflow, which fetched
each source and marked what it could not verify. Its corrections to the
brief's own premises are carried through in §12.

### 5.1 Python's compact dict

Raymond Hettinger, "[Python-Dev] More compact dictionaries with faster
iteration", python-dev, 10 December 2012
(https://mail.python.org/pipermail/python-dev/2012-December/123028.html):

> The current memory layout for dictionaries is unnecessarily
> inefficient. It has a sparse table of 24-byte entries containing the
> hash value, key pointer, and value pointer.
>
> Instead, the 24-byte entries should be stored in a dense table
> referenced by a sparse table of indices.

His worked example:

>     indices =  [None, 1, None, None, None, 0, None, 2]
>     entries =  [[-9092791511155847987, 'timmy', 'red'],
>                 [-8522787127447073495, 'barry', 'green'],
>                 [-6480567542315338377, 'guido', 'blue']]

> Only the data layout needs to change. The hash table algorithms would
> stay the same.

> In addition to space savings, the new memory layout makes iteration
> faster. […] Now, keys/values/items can loop directly over the dense
> table, using fewer memory accesses.

CPython `Objects/dictobject.c` (fetched from `main` and from the
`v3.6.0` tag; https://github.com/python/cpython/blob/main/Objects/dictobject.c):

> As of Python 3.6, this is compact and ordered.

> dk_indices is actual hashtable. It holds index in entries, or
> DKIX_EMPTY(-1) or DKIX_DUMMY(-2).

> It's simple for combined table. Since dk_entries is mostly append
> only, we can get insertion order by just iterating dk_entries.

PyPy shipped the layout a year earlier — Maciej Fijałkowski, "Faster,
more memory efficient and more ordered dictionaries on PyPy", PyPy
Status Blog, 22 January 2015
(https://morepypy.blogspot.com/2015/01/faster-more-memory-efficient-and-more.html):

> The new PyPy dictionary is split in two arrays […] Here,
> compact_array stores all the items in order of insertion, while
> sparse_array is a 1/2 to 2/3 full array of integers.

> The obvious benefit of having more compact dictionaries is an
> increased cache friendliness.

The ordering was an implementation detail in 3.6 and a language
guarantee in 3.7. `Doc/whatsnew/3.6.rst`:

> The order-preserving aspect of this new implementation is considered
> an implementation detail and should not be relied upon

Guido van Rossum, python-dev, 15 December 2017
(https://mail.python.org/pipermail/python-dev/2017-December/151283.html):

> Make it so. "Dict keeps insertion order" is the ruling. Thanks!

Python docs, `stdtypes`:

> Dictionaries preserve insertion order. Note that updating a key does
> not affect the order. Keys added after deletion are inserted at the
> end.

**Inference.** CPython's dict since 3.6 *is* a vector of `{hash, key,
value}` structs with a separate index array bolted on for lookup, and
the language subsequently promoted the vector's order to a semantic
guarantee. That is the reduction happening inside a language that has
a map as its most prominent type.

### 5.2 Rust: indexmap, linear-map, litemap

`indexmap` README
(https://github.com/indexmap-rs/indexmap/blob/main/README.md):

> This was inspired by Python 3.6's new dict implementation (which
> remembers the insertion order and is fast to iterate, and is compact
> in memory).

> `IndexMap` derives a couple of performance facts directly from how it
> is constructed, which is roughly:
> > A raw hash table of key-value indices, and a vector of key-value
> > pairs.

The core, from `src/inner.rs` and `src/lib.rs`:

```rust
type Indices = hash_table::HashTable<usize>;
type Entries<K, V> = Vec<Bucket<K, V>>;

pub(crate) struct Core<K, V> {
    indices: Indices,
    entries: Entries<K, V>,
}

struct Bucket<K, V> {
    hash: HashValue,
    key: K,
    value: V,
}
```

`linear-map` (https://github.com/contain-rs/linear-map), first line of
both README and `src/lib.rs`:

> A map implemented by searching linearly in a vector.

and its doc comment:

> All search operations (`contains_key`, `get`, `get_mut`, `insert`,
> and `remove`) run in `O(n)` time, making this implementation suitable
> only for small numbers of keys.

`vec_map` (https://github.com/contain-rs/vec-map) turns out to be a
different idea — a direct-indexed sparse array, not an array of pairs:

> A simple map based on a vector for small integer keys. Space
> requirements are O(highest integer key).

`litemap` (ICU4X,
https://github.com/unicode-org/icu4x/blob/main/utils/litemap/src/lib.rs):

> `litemap` is a crate providing [`LiteMap`], a highly simplistic "flat"
> key-value map based off of a single sorted vector.
>
> The main goal of this crate is to provide a map that is good enough
> for small sizes, and does not carry the binary size impact of
> `HashMap` or `BTreeMap`.

Benchmarks give a real but **unstable** crossover point. `micromap`
(Yegor Bugayenko, https://github.com/yegor256/micromap) claims linear
scan is 26–32× faster at N=2 and loses above N≈32; the counter-test
`wezm/hashmap-vs-vec` (https://github.com/wezm/hashmap-vs-vec) found:

> The results on my machine showed that `FxHashMap` was pretty much
> always the best option.

with the Vec ahead only at N≈5. The subflow's conclusion, which I
carry: the "array beats hash map for small N" claim is real but the
crossover ranges from about 5 to about 32 depending on key type,
hasher and access pattern.

### 5.3 C++: sorted vectors of pairs

Boost.Container documentation, "Non-standard containers", Boost 1.86.0
(https://www.boost.org/doc/libs/1_86_0/doc/html/container/non_standard_containers.html):

> Using sorted vectors instead of tree-based associative containers is a
> well-known technique in C++ world.

quoting Matt Austern, "Why You Shouldn't Use set, and What You Should
Use Instead", *C++ Report* 12:4, April 2000 (read second-hand, via
Boost's page):

> Using a sorted vector instead of a set gives you faster lookup and
> much faster iteration, but at the cost of slower insertion.

Standardisation: **Zach Laine** (not Zhihao Yuan — see §12), "A Standard
flat_map", P0429R0, 2016-08-31
(https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0429r0.pdf)
through P0429R9, 2022-06-17:

> There has been a strong desire for a more space- and/or
> runtime-efficient representation for map among C++ users for some time
> now.

> Iteration is vastly cheaper for contiguous-storage variants. Any
> node-based associative container will always be slower than a
> flattened one for iteration.

Directly on the "two-field struct" question, R0 benchmarked a
hand-written pair struct against `std::pair` and found the struct
fastest:

> The 'custom pair' version of the sorted vector uses a simple struct
> instead of pair for its value type.
>
> The curve for sorted vector using a custom struct is dramatically
> flatter in its growth in the `<int,int>` runs.

The version adopted into C++23 is **struct-of-arrays**, not
array-of-structs — from P0429R9 and cppreference
(https://en.cppreference.com/w/cpp/container/flat_map.html):

```cpp
template<class Key, class T, class Compare = less<Key>,
         class KeyContainer = vector<Key>, class MappedContainer = vector<T>>
class flat_map {
```

> A flat_map maintains the following invariants: (5.1) it contains the
> same number of keys and values; (5.2) the keys are sorted with respect
> to the comparison object; and (5.3) the value at offset off within the
> value container is the value associated with the key at offset off
> within the key container.

Chandler Carruth, "Efficiency with Algorithms, Performance with Data
Structures", CppCon 2014 (slides fetched from the CppCon2014 repo;
transcript not found):

> DISCONTIGUOUS DATA STRUCTURES ARE THE ROOT OF ALL (PERFORMANCE) EVIL

> STACKS? QUEUES? MAPS? / Just use std::vector. Really.

> USING STD::MAP IS AN EXERCISE IN SLOWING DOWN CODE

> A GOOD HASH TABLE DESIGN / No buckets! Use open addressing into a
> table of the key-value pairs. / Table stored as contiguous range of
> memory

### 5.4 Zig

`std/array_hash_map.zig`, current master
(https://github.com/ziglang/zig/blob/master/lib/std/array_hash_map.zig):

> A hash table of keys and values, each stored sequentially.
>
> Insertion order is preserved. In general, this data structure supports
> the same operations as `std.ArrayList`.

> This type is designed to have low overhead for small numbers of
> entries. When `store_hash` is `false` and the number of entries in the
> map is less than 9, the overhead cost of using
> `ArrayHashMapUnmanaged` rather than `std.ArrayList` is only a single
> pointer-sized integer.

The two fields, and the entry type:

```zig
entries: DataList = .{},

/// When entries length is less than `linear_scan_max`, this remains `null`.
index_header: ?*IndexHeader = null,

pub const Data = struct {
    hash: Hash,
    key: K,
    value: V,
};
pub const DataList = std.MultiArrayList(Data);
```

and the lookup path below the threshold is literally a `for` loop over
the array — `getIndexAdapted` begins:

```zig
const header = self.index_header orelse {
    // Linear scan.
```

with the threshold derived from the cache line:

```zig
const linear_scan_max = @max(1, @min(
    std.atomic.cache_line / @max(1, @sizeOf(Hash)),
    std.atomic.cache_line / @max(1, @sizeOf(K))));
```

`std/multi_array_list.zig`:

> A MultiArrayList stores a list of a struct or tagged union type.
> Instead of storing a single list of items, MultiArrayList stores
> separate lists for each field of the struct […]

**Inference.** Zig's ordered map is the cleanest existing artefact of
the thesis: an array of `{hash, key, value}` structs that acquires a
hash index only when it outgrows a cache line, and linear-scans until
then.

### 5.5 Data-oriented design

Mike Acton, "Data-Oriented Design and C++", CppCon 2014 (deck fetched
from the CppCon2014 repository), slide 40:

> Rule of thumb: Where there is one, there are many. Try looking on the
> time axis.

> If you don't understand the data you don't understand the problem.

**Correction, carried from the subflow:** searching the full extracted
text of all 201 slides for `hash` and `map` found no arrays-versus-maps
argument. "Where there is one, there are many" is a general layout
principle. Do not attribute a maps claim to this talk.

**Correction:** Casey Muratori, "Semantic Compression", 28 May 2014
(https://caseymuratori.com/blog_0015) — the subflow fetched the full
page and reports it contains **no** discussion of hash maps or
arrays-versus-maps. It is an argument against speculative class
hierarchies. Citing it for a hash-map claim would be a misattribution.
A Muratori source on hash maps specifically was not found.

Richard Fabian, *Data-Oriented Design*, online edition dated
2018-10-08 (https://www.dataorienteddesign.com/dodbook/), chapter
"Relational Databases":

> there are many places where you will wish you had a simple array to
> work with, and this chapter will help you by giving you an example of
> how you can migrate from a web of connected complex objects to a
> simpler to reason about relational model of arrays.

> For many programmers brought up on object-oriented design, the idea of
> reducing the types of structure available down to just simple arrays,
> is virtually unthinkable.

> Edgar F. Codd introduced the fundamental terms of normalisation we use
> to this day in a systematic approach to reducing the most complex of
> interconnected state information to linear lists of unique independent
> tuples.

and chapter "Searching", which treats the index as an addition to a
table rather than a structure in its own right:

> You can manually add searching helpers such as binary trees, hash
> tables, or just keep your table sorted by using ordered insertion
> whenever you add to the table.

> Database management systems have long held the concept of an index.
> […] We can use this idea and implement a just-in-time indexing system
> in our games


---

## 6. Datomic and Rich Hickey's datom

Reported as found. No connection to the living's notation is assumed
and none was found.

### 6.1 What a datom is

"Datomic Data Model", docs.datomic.com (no publication year on the
page; retrieved 2026-09-04;
https://docs.datomic.com/whatis/data-model.html). I fetched this page
myself and a nested subflow fetched it independently; the quotes agree.

> A Datomic database is a set of immutable atomic facts called datoms.
> It has no tables; instead it has a universal schema of user-defined
> attributes, in which any entity can possess any attribute.

> A datom is an immutable atomic fact that represents the addition or
> retraction of a relation between an entity, an attribute, a value, and
> a transaction. A datom is expressed as a five-tuple:
>  - an entity id (E)
>  - an attribute (A)
>  - a value for the attribute (V)
>  - a transaction id (Tx)
>  - a boolean (Op) indicating whether the datom is being added or
>    retracted

> An entity is a set of datoms that are all about the same E.

> Because all datoms are part of a single relation, this is called a
> universal schema.

Datomic glossary (https://docs.datomic.com/glossary.html):

> **Datom**: An atomic fact in a database, composed of
> entity/attribute/value/transaction/added. Pronounced like "datum",
> but pluralized as datoms.
>
> **Database**: A database is a set of datoms.
>
> **Index**: Sorted collection of datoms. Indexes are named by the order
> in which datom components are used for sort, e.g. An index that sorts
> first by entity, then attribute, then value, then tx is called EAVT.

### 6.2 The map is a view, not the storage

Same Data Model page, under "Map View Example":

> It is often convenient to consider a point-in-time view as only a
> three-tuple with Tx and Op elided

> This three-tuple view is very similar to a programming language object
> where the E is analogous to this or self. The map view of an entity at
> a particular point in time captures this information more compactly,
> using the reserved pseudo-attribute name :db/id for E

"Entities" (https://docs.datomic.com/reference/entities.html):

> A Datomic entity provides a lazy, associative view of all the
> information that can be reached from a Datomic entity id.
>
> Entities are not a mapping layer between databases and application
> code. Entities are a direct, mechanical translation from database
> information to associative application access.

Hickey said the same in talks. The following are **volunteer community
transcripts**, not text Hickey published; wording is the transcriber's
rendering of speech. "Writing Datomic in Clojure", GOTO Copenhagen, May
2012 (transcript at
https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/WritingDatomicInClojure.md):

> So we call this thing a datom. Entity, attribute, value, and
> transaction. And the only schema that is associated with a Datomic
> database is the definition of attributes. There is no other structural
> construct. There are no records. There are no types. There are no
> classes. There are no document schemas, or anything like that.

"Deconstructing the Database", QCon SF, November 2012 (same repository):

> it is important if you are going to build a system that is about the
> accretion of facts, that you have a representation that your
> structural representation is minimized. You do not want to have this
> big composite thing and say, "I need to add a fact to it, like in the
> middle here." And store this whole thing to get that new piece of
> novelty in. You need to actually boil down your data representation to
> be that primitive thing.

"The Functional Database", QCon New York, June 2013 (same repository):

> So I am going to make an entity, which is sort of a lazy map, from the
> value of the database.

### 6.3 Etymology

The only first-party statement found is the glossary's "Pronounced like
'datum', but pluralized as datoms." A community-transcribed remark from
JaxConf 2012, in an AI-assisted gist whose title attribution the
transcriber himself flags as unreliable
(https://gist.github.com/HerbCaudill/acf2294dac8e87e24f550715b6991035),
has Hickey saying:

> We call them "datoms" and we just spell it differently, so we can say
> "datoms" because if we spelled it "datum", the plural would be "data",
> and then people wouldn't know what we mean. So we have "datom", which
> is an atomic fact, and "datoms" are more than one fact.

The widely repeated gloss "datom = data atom" was **not** found in any
first-party source; treat it as unverified.

### 6.4 Hickey arguing *for* maps

The same man makes the strongest available case for the map. "Maybe
Not", Clojure/conj, November 2018 (community transcript). Slide text:

> Maps vs Records / Fields
> + maps are (mathematical) functions!
> + simplest functions in programming
>   + keyset -> vals
>   + no code, no categories

Spoken:

> We have an even more primitive way to get from a mapping of one set to
> another. And it is the literal map. It is saying: if you give me this,
> I will give you that. ... I am saying specifically, declaratively,
> with no executable code, no functions being run, nothing, a definition
> of a function. A mathematical function. A mapping between a set and
> another set. It is a concrete thing.

> Maps are the most fundamental functions in programming. They should
> not be denigrated. They should be exalted. This is the first place to
> start. This is the simplest thing that you can do.

> in addition to the maps being functions, maps are also self
> descriptive. You can call "keys" on a map, unlike a function.

> So this enumerability is super important, which is why you do not want
> junk empty keys in your maps. You want to leave it out. That way the
> map can tell you: I do not *know* the last name, or the address. I do
> not know that. The maps know what they know.

He states the objection himself:

> at least these records, classes, whatever, they enumerate what is
> possible. We are passing maps around, it is the wild West. It could be
> anything. How do you know what it is? ... Maps are too open. There is
> no guidance.

"Effective Programs — 10 Years of Clojure", Clojure/Conj, October 2017
(community transcript; I fetched this one myself) is where "just use
maps" comes from:

> So, you know, we know in practice, Clojure says, "just use maps". What
> this meant actually was, "Clojure didn't give you anything else",
> right? ... So working with these associative data structures was
> tangible, well-supported, functional, high-performance activity. And
> they're generic. ... I can combine anything that I like, there's an
> algebra associated with associative data. The names are first-class

> we can associate the semantics with the attributes and not with the
> aggregates, right?

> we elevate the containership of information to become the semantic
> driver. Okay, we say, "this is a person, and a person has a name, and
> a person has an email, and a person has a social security number", and
> there's no semantics for those three things except in the context of
> the person class or type

> the most important thing is that the aggregates determine the
> semantics, which is dead wrong

And "The Value of Values", JaxConf 2012 (community transcript; I
fetched it) on how few aggregate kinds are needed:

> There is a logical notion of a list. There is a logical notion of a
> map, and a logical notion of a set, and strings and numbers and
> whatever. But you can probably exhaust what you need to use in the
> value space with fewer than 20 of these things.

**Inference (from the subflow, which I agree with and mark as
inference).** Hickey is not on two sides. Both arguments are the same
argument — that meaning belongs to the attribute, not to the aggregate.
At the storage layer that means decomposing to E-A-V so the granularity
of a fact matches the granularity of change. At the program layer it
means open maps keyed by namespaced attributes rather than closed
records. The map he exalts is the open, attribute-keyed, enumerable
map. The thing he removes from Datomic's storage is the *record* — the
fixed composite that must be rewritten whole to record one new fact.


---

## 7. Datalog and Prolog: facts are tuples, and there is no map type

Serge Abiteboul, Richard Hull, Victor Vianu, *Foundations of Databases:
The Logical Level*, Addison-Wesley, 1995 (the "Alice book"). The
authors' own site was unreachable; the subflow fetched a university
mirror PDF and extracted text itself, so the notation below is
flattened and reconstructed while the wording is as read.

§3.2, the named perspective — a *row* is a map:

> In the named perspective, it is natural to view tuples as functions.
> More precisely, a tuple over a (possibly empty) finite set U of
> attributes (or over a relation schema R[U]) is a total mapping from U
> to dom.

§3.2, the unnamed perspective:

> With the unnamed perspective, it is more natural to view a tuple as an
> element of a Cartesian product. More precisely, a tuple is an ordered
> n-tuple (n ≥ 0) of constants

and the book's own statement that the two readings are interchangeable:

> This correspondence will allow us to blur the distinction between the
> two perspectives and move freely from one to the other when
> convenient.

§3.3, the logic-programming perspective:

> A fact over R is an expression of the form R(a1,...,an), where ai ∈
> dom for i ∈ [1..n].
>
> Under the logic-programming perspective, a relation (instance) over R
> is a finite set of facts over R. For a database schema R, a database
> instance is a finite set I that is the union of relation instances
> over R.

Soufflé (a modern Datalog engine), "Relations"
(https://souffle-lang.github.io/relations):

> Soufflé requires the declaration of relations. A relation is a set of
> ordered tuples (x1, …, xk) where each element xi is a member of a data
> domain denoted by an attribute type.

"Program" (https://souffle-lang.github.io/program):

> A fact is a rule that holds unconditionally, i.e., a fact is a Horn
> Clause A(1,2) ⇐ true.

"Types" (https://souffle-lang.github.io/types) lists four primitive
types — symbol, number, unsigned, float — plus record types, which are
tuples:

> A record-type is defined as follows, .type <new-record> = [ <name_1>:
> <type_1>, ..., <name_k>: <type_k> ]

No map or dictionary type appears in Soufflé's type system on the pages
fetched.

Prolog is the interesting case, because the one mainstream
implementation that added a map built it out of a compound term. SWI-Prolog
Manual §5.4 (https://www.swi-prolog.org/pldoc/man?section=bidicts):

> SWI-Prolog version 7 introduces dicts as an abstract object with a
> concrete modern syntax and functional notation for accessing members

> Compound terms with positional arguments form the traditional way to
> package data in Prolog.

§5.4.6, "Implementation notes about dicts":

> Dicts are currently represented as a compound term using the functor
> `dict`. The first argument is the tag. The remaining arguments create
> an array of sorted key-value pairs. This representation is compact and
> guarantees good locality. Lookup is order log(N), while adding values,
> deleting values and merging with other dicts has order N.

**Unverified.** The subflow searched the Alice book's extracted text and
the Datomic and Soufflé docs for a statement of the form "a relation
with a functional dependency on one column is what a map is" and found
none. Treat that equation as unattested in these sources; the nearest
witnessed statements are the Alice book's "a tuple over U is a total
mapping from U to dom" (a *tuple*, not a relation, is the map) and
Datomic's ":db.cardinality/one – the attribute is single-valued".


---

## 8. Notations that define the map *as* a vector of two-field structs

These are the cases where the reduction is not an argument but a
published definition.

### 8.1 Dhall — the strongest instance found

Dhall has no map type. Its Prelude defines `Map` as a `List` of a
two-field record. From the Dhall Language Tour
(https://docs.dhall-lang.org/tutorials/Language-Tour.html), quoting the
Prelude's `Map/Type`:

> Several Dhall features, tools, packages use Maps, where a Map is
> defined as a list of key-value pairs

```dhall
{- This is the canonical way to encode a dynamic list of key-value pairs.

   Tools (such as `dhall-to-json`/`dhall-to-yaml` will recognize values of this
   type and convert them to maps/dictionaries/hashes in the target language

   For example, `dhall-to-json` converts a Dhall value like this:

   [ { mapKey = "foo", mapValue = 1 }
   , { mapKey = "bar", mapValue = 2 }
   ] : ./Map Text Natural

   ... to a JSON value like this:

   { "foo": 1, "bar": 2 }
-}
let Map
    : Type → Type → Type
    = λ(k : Type) → λ(v : Type) → List { mapKey : k, mapValue : v }
```

The tour's own gloss:

> Map is a function that takes two function arguments (the type of each
> key and the type of each value), and returns a new type (a List of
> key-value pairs).

Dhall's `toMap` keyword goes the other direction, turning a record into
that list — from "Built-in types, functions, and operators"
(https://docs.dhall-lang.org/references/Built-in-types.html):

> The `toMap` keyword converts a record literal to a List of key-value
> pairs:
>
>     ⊢ toMap { foo = 2, bar = 3 }
>
>     [ { mapKey = "bar", mapValue = 3 }, { mapKey = "foo", mapValue = 2 } ]

Note that the output is sorted by key: Dhall's records are unordered,
so the list it produces has to pick an order, and it picks a canonical
one.

### 8.2 Protocol Buffers

Google, "Language Guide (proto3)"
(https://protobuf.dev/programming-guides/proto3/#maps), fetched by a
nested subflow. Under "Backwards Compatibility":

> The map syntax is equivalent to the following on the wire, so protocol
> buffers implementations that do not support maps can still handle your
> data:
>
>     message MapFieldEntry {
>       key_type key = 1;
>       value_type value = 2;
>     }
>
>     repeated MapFieldEntry map_field = N;

and, immediately after (I verified this passage myself by fetching the
page independently of the subflow):

> Any protocol buffers implementation that supports maps must both
> produce and accept data that can be accepted by the earlier
> definition.

with:

> Wire format ordering and map iteration ordering of map values is
> undefined, so you cannot rely on your map items being in a particular
> order.

> When parsing from the wire or when merging, if there are duplicate map
> keys the last key seen is used.

The generated entry type leaks into the namespace as `FooEntry` for a
map field `foo`, which is the sugar showing through.

**Inference (from the subflow, carried).** Protobuf's map is strictly
*less* expressive than the `repeated MapFieldEntry` it desugars to: the
map forbids message and enum keys, forbids `repeated`, and abandons
ordering, all of which the raw repeated entry retains.

### 8.3 YAML's `!!omap` and `!!pairs`

From the YAML type repository (https://yaml.org/type/), fetched by a
nested subflow — three tags forming an exact grid on ordering ×
duplicates:

> **map:** "Unordered set of key: value pairs without duplicates."
> **omap:** "Ordered sequence of key: value pairs without duplicates."
> **pairs:** "Ordered sequence of key: value pairs allowing duplicates."

The structurally telling detail: `!!omap` and `!!pairs` have **Kind:
Sequence**, not Kind: Mapping. YAML builds its ordered map out of a
sequence of single-entry mappings — a vector of two-field records —
rather than out of its map type. The omap page notes that where a
language has no such native type an application may load the structure
"into a native array of hash tables containing one key each".

### 8.4 Cap'n Proto: no map type

Kenton Varda, capnproto Google Group thread "Serializing a hash/map?",
2014–2015 (https://groups.google.com/g/capnproto/c/6eT7pBx4_Mc):

> this is something I want to have, it just hasn't reached the top of
> the priority queue.

> You can, of course, roll your own using a list.

**Note.** This is a "no map type in practice" case, not an argument
that the map should not exist; Varda says he wants one. Weight it
accordingly.

### 8.5 CUE and Nix: the struct subsumes the map

The opposite reduction also exists in practice, and it is worth
recording because it is the reverse of the proposition.

CUE specification (https://cuelang.org/docs/reference/spec/):

> A _struct_ is a set of elements called _fields_, each of which has a
> name, called a _label_, and value.

> A _dynamic field_ is a field whose label is determined by an
> expression wrapped in parentheses.

CUE has no separate map or dictionary type; structs with pattern
constraints and dynamic fields do the work.

Nix (https://nix.dev/manual/nix/2.24/language/syntax), fetched by a
nested subflow:

> An attribute set is a collection of name-value-pairs called
> _attributes_.
>
> An attribute name may only occur once in each attribute set.
>
> Attributes can appear in any order.

Nix's attribute set is simultaneously its record type and its map type.

---

## 9. Type theory: records, maps and structs as one construct

Giuseppe Castagna, "Typing Records, Maps, and Structs", *Proc. ACM
Program. Lang.* 7, ICFP, Article 196, August 2023
(https://www.irif.fr/~gc/papers/icfp23.pdf, fetched as PDF). This is
the most precise treatment found of exactly the question at hand.

Opening line of the abstract:

> Records are finite functions from keys to values. In this work we
> focus on two main distinct usages of records: structs and maps.

His enumeration of the differences (verbatim, abridged):

> **Maps:**
> - All keys of a single map have the same type and so do the values
>   they are mapped to.
> - It is not necessary to know all the keys at compile time: they can
>   be dynamically discovered.
> - It is sensible to give a default value.
> - Keys may be indexed: it is possible to iterate over them.
> - Keys are values: keys used for map selection can be results of
>   expressions.
> - Accessing a key that is not defined does not yield an error
>
> **Structs:**
> - Different keys in the same structure can be mapped to values of
>   different types.
> - Keys may be restricted to a specific set (e.g., strings, atoms,
>   identifiers, ...).
> - It is necessary to know all the different keys at compile time.
> - Keys do not support indexing.
> - Keys are not necessarily values, they may form a separate set of
>   names.
> - Accessing a key that is not defined yields an error.

and his ruling:

> Besides these linguistic differences, maps and structs may have
> different implementations, typically, hashes or search trees for maps;
> arrays or contiguous locations for structs.

> While it is sensible to have different implementations for maps and
> structs, it is less justified to have different types for them,
> especially in languages in which the two data structures share the
> same or similar syntax for expressions and the same set of operations
> (as a matter of fact, both are finite functions from keys to values).

He also surveys who does what:

> Some languages do not make any syntactic distinction for defining maps
> and structs (e.g., Lua, Ballerina), in other languages they are
> distinct but tightly related (e.g., in Elixir, structs are wrappers
> around maps […]), others make them completely disjoint (e.g., Go
> Language, Erlang, Swift)

Daan Leijen, "Extensible records with scoped labels", *Trends in
Functional Programming* 2005 (draft revision 23 July 2005; fetched as
PDF) makes the record a *sequence* rather than a set, which is the
type-theoretic form of "a record is a vector of label-value pairs":

> A novel aspect of this work is that records can contain duplicate
> labels, effectively introducing a form of scoping over the labels.

> The records support scoped labels since fields with duplicate labels
> are allowed and retained. As records are equivalent up to permutation
> of distinct labels, all basic operations are still well-defined.

The equality relation is explicitly a permutation-up-to-distinct-labels
relation on a list:

> Rule (eq-swap) is the most interesting: it states that the first two
> fields of a row can be swapped if (and only if) their labels are
> different.

and his implementation discussion names the association list outright:

> **Association lists.** A naïve implementation of records uses a simple
> association list of label-value pairs. Selection is implemented as a
> linear search over this list, where the type system ensures that such
> label is always found.

**Inference.** Leijen's system is the exact midpoint: a record whose
value is a list of pairs, whose type equality quotients only by
swapping *distinct* labels, so duplicates survive and shadow. That is
the vector of two-field structs, given a type system that makes lookup
total.

Martin Fowler, "List And Hash", 3 December 2015
(https://martinfowler.com/bliki/ListAndHash.html), states the reduction
in passing while arguing the opposite case:

> In most cases there are separate data types for the list and hash,
> since their access operations differ. However, as any lisper can tell
> you, it's easy to represent a hash as a list of key-value pairs.
> Similarly you can treat a hash with numeric indexes as a list (which
> is what Lua's tables do).


---

## 10. The case for keeping a distinct map

Gathered as asked. These are the strongest arguments found, each with a
witnessed source.

### 10.1 Key uniqueness is a real invariant, and the conversion is lossy

The clearest demonstration is that going from a vector of pairs to a
map destroys information, and every language has to state a rule for
what it destroys.

Haskell `containers`, `Data.Map.Strict.fromList`
(https://hackage.haskell.org/package/containers/docs/Data-Map-Strict.html):

> If the list contains more than one value for the same key, the last
> value for the key is retained.

Protocol Buffers (https://protobuf.dev/programming-guides/proto3/):

> When parsing from the wire or when merging, if there are duplicate map
> keys the last key seen is used.

TOML v1.0.0 (https://toml.io/en/v1.0.0):

> Defining a key multiple times is invalid.

CBOR, RFC 8949 §3.1:

> A map that has duplicate keys may be well-formed, but it is not valid,
> and thus it causes indeterminate decoding.

Nix (https://nix.dev/manual/nix/2.24/language/syntax):

> An attribute name may only occur once in each attribute set.

**Inference.** A map is the quotient of a vector of pairs by
"same key". A type that is the quotient carries a proof the raw vector
does not: that lookup is a total function on the present keys, with no
tie-break rule to publish, no last-wins convention to document, and no
divergence between readers. Every notation above had to publish such a
rule precisely because it declined to make the type carry it.

### 10.2 Unorderedness is a semantic guarantee, not an omission

The Go specification (https://go.dev/ref/spec):

> A map is an unordered group of elements of one type, called the
> element type, indexed by a set of unique keys of another type, called
> the key type.

and:

> The iteration order over maps is not specified and is not guaranteed
> to be the same from one iteration to the next.

Go's runtime randomises iteration order deliberately, so that programs
cannot come to depend on an order the type does not promise.

Codd made the same point as his first design goal in 1970 — ordering
dependence is a data dependency to be removed, not a feature — and Date
and Darwen made it a proscription:

> D shall include no concept of a "relation" whose attributes are
> distinguishable by ordinal position.

Rich Hickey, "Maybe Not" (community transcript), makes the positive
case: an unordered, enumerable map *is* a mathematical function given
directly, with no code.

### 10.3 Lookup semantics need a place to live

Castagna's enumeration (§9) is the sharpest statement of what "map" and
"struct" mean *as usage*, and both his lists turn on lookup: whether
the key is known at compile time, whether it may be computed, whether a
miss is an error or a default. A vector of two-field structs has no
lookup operation at all until someone defines one, and defining it is
defining a map.

Boost's own summary of what a sorted vector of pairs costs
(https://www.boost.org/doc/libs/1_86_0/doc/html/container/non_standard_containers.html):

> Slower insertion and erasure than standard associative containers
> (specially for non-movable types)

### 10.4 Keys need not be strings, and often are not

EDN (https://github.com/edn-format/edn):

> Note that keys and values can be elements of any type.

with the spec's own example `{:a 1, "foo" :bar, [1 2 3] four}` — a
vector used as a key.

YAML 1.2.2 §3.2.1.1 (https://yaml.org/spec/1.2.2/):

> The content of a mapping node is an unordered set of key/value node
> pairs, with the restriction that each of the keys is unique. YAML
> places no further restrictions on the nodes. In particular, keys may
> be arbitrary nodes, the same node may be used as the value of several
> key/value pairs and a mapping could even contain itself as a key or a
> value.

**Inference.** A record type whose labels are names cannot express
these; a map type whose keys are values can. Where a notation restricts
keys to strings, the distinction narrows and the reduction gets easier
— which is precisely why protobuf, having reduced the map to a repeated
entry, then had to *forbid* message and enum keys.

### 10.5 The counterweight: one construct can do both

The reverse reduction has as much practice behind it as the forward
one. Nix and CUE have one construct (attribute set / struct) serving as
both record and map. Date and Darwen define the tuple *as* a set of
name-value triples. Castagna's paper exists to argue that having two
*types* for one thing is unjustified even where two implementations
are:

> While it is sensible to have different implementations for maps and
> structs, it is less justified to have different types for them

Martin Fowler, "List And Hash" (2015), reports the list-and-hash pair
as the working universal pair in practice, and notes both that the hash
is easy to represent as a list of pairs and that most languages keep
them as separate types "since their access operations differ".


---

## 11. How the notations define the map

Gathered by a nested research subflow, which fetched each specification
directly. Its summary table, carried unchanged:

| Format | Spec's own word for the structure | Ordered? | Duplicate keys? |
|---|---|---|---|
| JSON (RFC 8259) | "unordered collection of zero or more name/value pairs" | No | SHOULD be unique; not forbidden; behavior "unpredictable" |
| JSON (ECMA-404) | "zero or more name/value pairs" | "does not assign any significance to the ordering" | "does not require that name strings be unique" |
| EDN | "collection of associations between keys and values" | "No semantics should be associated with the order" | "Each key should appear at most once" |
| TOML | "collections of key/value pairs" | "not guaranteed to be in any specific order" | "Defining a key multiple times is invalid." |
| Nix attrsets | "collection of name-value-pairs called attributes" | "Attributes can appear in any order." | "may only occur once" |
| YAML `!!map` | "Unordered set of key: value pairs without duplicates." | No | Error |
| YAML `!!omap` | "Ordered sequence of key: value pairs without duplicates." | Yes | No |
| YAML `!!pairs` | "Ordered sequence of key: value pairs allowing duplicates." | Yes | Yes |
| XML | *(no map type)* | children: ordered list | attribute names must be unique |
| CBOR (RFC 8949) | "pairs of data items" | encoding order free; deterministic profile sorts | well-formed but "not valid" |
| MessagePack | "key-value pairs of objects", stored as `N*2 objects` | (no statement found) | (no statement found) |
| Protobuf `map<K,V>` | sugar for `repeated MapFieldEntry` | "undefined" | "last key seen is used" |

Points worth having in full.

**JSON has two normative specs and they disagree.** RFC 8259 (Bray ed.,
December 2017, https://www.rfc-editor.org/rfc/rfc8259.html) §1:

> An object is an unordered collection of zero or more name/value pairs,
> where a name is a string and a value is a string, number, boolean,
> null, object, or array. An array is an ordered sequence of zero or
> more values.

but §4's grammar is a comma-separated sequence of members, and the RFC
concedes:

> When the names within an object are not unique, the behavior of
> software that receives such an object is unpredictable. Many
> implementations report the last name/value pair only. Other
> implementations report an error or fail to parse the object, and some
> implementations report all of the name/value pairs, including
> duplicates.

ECMA-404 2nd edition (December 2017) §6 declines to assert map
semantics at all (the subflow decompressed the PDF's content streams to
read this):

> The JSON syntax does not impose any restrictions on the strings used
> as names, does not require that name strings be unique, and does not
> assign any significance to the ordering of name/value pairs. These are
> all semantic considerations that may be defined by JSON processors or
> in specifications defining specific uses of JSON for data interchange.

and its Introduction puts the whole family in one bag:

> Most programming languages will have some feature for representing
> such collections, which can go by names like record, struct, dict,
> map, hash, or object.

**CBOR's map is a flat alternating run.** RFC 8949 §3.1, major type 5:

> A map of pairs of data items. Maps are also called tables,
> dictionaries, hashes, or objects (in JSON). A map is comprised of
> pairs of data items, each pair consisting of a key that is immediately
> followed by a value.

§4.2.1, which exists because the encoding order is otherwise free and
observable:

> The keys in every map MUST be sorted in the bytewise lexicographic
> order of their deterministic encodings.

**MessagePack is the barest case.** Its spec
(https://github.com/msgpack/msgpack/blob/master/spec.md) defines a map
as a header plus `N*2 objects`, with "odd elements in objects are keys
of a map"; the subflow reports finding no statement in the spec about
ordering or duplicates, and marks that absence as a fetch finding
rather than a verified negative.

**XML has no map.** W3C XML Information Set §2.2: `[children]` is "An
ordered list of child information items, in document order";
`[attributes]` is "An unordered set of attribute information items". XML
1.0's well-formedness constraint Unique Att Spec: "An attribute name
MUST NOT appear more than once in the same start-tag or empty-element
tag." The `!!pairs` type in YAML exists, per yaml.org, precisely to
carry XML-shaped data where names repeat and order matters.

**Correction carried from the subflow.** EDN does *not* say duplicate
keys are an error. Its text is "Each key should appear at most once."
The brief's premise on that point is not confirmed by the spec.


---

## 12. What could not be verified, and corrections to the brief

Corrections to premises in the brief itself, each established by a
fetched source:

- **P0429 `std::flat_map` is by Zach Laine, not Zhihao Yuan.** Verified
  in the headers of both P0429R0 (2016-08-31) and P0429R9 (2022-06-17).
  The SG14 predecessor P0038R0 "Flat Containers" (2015-09-25) is by
  Sean Middleditch.
- **There is no PEP for Python's compact dict.** PEP 468 (Eric Snow,
  2014) is about `**kwargs` ordering and mentions the compact dict only
  as an alternate approach. The 3.7 ordering guarantee came from
  Guido van Rossum's "Make it so" ruling on python-dev, 15 December 2017.
- **Casey Muratori's "Semantic Compression" does not discuss hash maps.**
  The full page was fetched and searched. It argues against speculative
  class hierarchies. No Muratori source on hash maps specifically was
  found.
- **Mike Acton's CppCon 2014 deck does not argue arrays versus maps.**
  All 201 slides were extracted and searched for `hash` and `map`.
  "Where there is one, there are many" is verified but is a general
  layout principle.
- **The `std::flat_map` that shipped is struct-of-arrays**
  (`KeyContainer = vector<Key>` plus `MappedContainer = vector<T>`), as
  is Zig's `ArrayHashMap` via `MultiArrayList`. Only indexmap, Boost's
  `flat_map` and CPython/PyPy keep an actual array of key-value structs.
- **The frames proposal is Richard O'Keefe's, not Joe Armstrong's.**
  EEP 43 names it "the Frames proposal from Richard O'Keefe", the
  document is O'Keefe's "No more need for records" (Otago, 2003, fifth
  draft 2012), and the erlang-questions thread quotes O'Keefe defending
  it. No frames proposal by Joe Armstrong was found.
- **There is no EEP for frames.** The raw erlang.org EEP index was
  grepped for "frame" and "struct"; zero hits. Frames remained a
  standalone PDF.
- **EDN does not say duplicate keys are an error.** Its text is "Each
  key should appear at most once."
- **The small-N crossover where an array beats a hash map is not a
  fixed number.** Verified data points: Zig derives it from
  `cache_line / max(sizeof(Hash), sizeof(K))`; `micromap`'s own
  benchmark puts it near 32; `wezm/hashmap-vs-vec` puts it near 5–10
  against `FxHashMap`; `litemap` says "< 20 items".

Unverified or unreachable:

- **"A relation with a functional dependency on one column is what a map
  is"** — searched for in the Alice book, the Datomic docs and the
  Soufflé docs; **not attested** in any of them. The nearest witnessed
  statements are Codd's footnote 8 ("A function is a binary relation,
  which is one-one or many-one, but not one-many") and the Alice book's
  "a tuple over U is a total mapping from U to dom".
- **"datom = data atom"** — repeated widely, found in **no** first-party
  source. Datomic's glossary gives only the pronunciation note.
- **Rich Hickey's "A History of Clojure" (HOPL IV, 2020)** — the PDF is
  behind Cloudflare on download.clojure.org and behind a 403 on
  dl.acm.org. Not fetched; nothing is quoted from it.
- **All Hickey talk quotations** are from volunteer community
  transcripts (github.com/matthiasn/talk-transcripts) and one
  AI-assisted gist, not from text Hickey published. The Datomic
  documentation quotations *are* first-party.
- **Joe Armstrong's own 2001 "proper structs" write-up** — not found.
  O'Keefe's §8.3 is the only sourced description of it.
- **Chris Pressey's erlang-questions posts** arguing that the `dict`
  module suffices — not retrieved; only O'Keefe's characterisation of
  them was read.
- **A complete sweep of erlang-questions** — erlang.org's pipermail
  rate-limited the subflow; roughly 113 of ~145 May 2013 messages were
  retrieved. Stronger "proplists suffice" statements may exist in the
  remainder.
- **docs.dyalog.com and aplwiki.com** — 403. Dyalog's formal array-type
  roster is not witnessed; "Dyalog has no dictionary type" rests on the
  dfns association-lists page's framing.
- **Whitney papers "A Business Oriented Language" / "An APL Machine"** —
  neither appears on KX's own archive page. "An APL Machine" is likely
  Philip Abrams' 1970 Stanford thesis; do not attribute it to Whitney.
- **Matt Austern's "Why You Shouldn't Use set" (C++ Report, 2000) and
  Alexandrescu's *Modern C++ Design*** — read second-hand through
  Boost's documentation, not in the originals.
- **Transcripts of the Acton and Carruth CppCon 2014 talks** — slides
  verified, transcripts not found.
- **The 1998 K Reference Manual quotations** come from a hand-decoded
  PDF stream; word spacing may be imperfect though the words are right.
- **The Alice book quotations** come from a university mirror PDF with
  self-extracted text; notation is flattened and reconstructed.
- **Hettinger's PyCon 2017 "Modern Python Dictionaries" slides** — the
  schedule page 404s; slides not fetched. The San Francisco Python
  "Modern Dictionaries" talk (8 December 2016) *is* verified on pyvideo.
- **CACM live pages** are behind Cloudflare; the Stonebraker blog post
  was read from an Internet Archive snapshot, and "SQL Databases v.
  NoSQL Databases" (CACM 53(4), April 2010) could not be fetched at all
  — nothing is quoted from it.

A negative finding worth stating plainly: **no single canonical essay
or talk was found whose thesis is "the map is a degenerate relation" or
"a language needs only structs and vectors".** Repeated searches on
those framings returned nothing. What exists instead is the same claim
made piecemeal, and usually made by *doing* rather than by arguing:

- as a definition — Dhall's `Map = λ(k) → λ(v) → List { mapKey : k, mapValue : v }`;
- as a wire format — protobuf's `map<K,V>` desugaring to
  `repeated MapFieldEntry`;
- as a normal form — Rel's 6NF, where every relation is a set of keys
  or a set of key-value pairs;
- as an implementation — CPython's, PyPy's, indexmap's and Zig's
  entries-array-plus-index;
- as advice — Carruth's "STACKS? QUEUES? MAPS? Just use std::vector.
  Really."; Fabian's "reducing the types of structure available down to
  just simple arrays";
- as a type-theoretic result — Castagna's "it is less justified to have
  different types for them".

The nearest thing to a direct argument is Castagna's ICFP 2023 paper,
and its conclusion is not that the map should go but that the map and
the struct should share one type.

---

## Sources

Set theory

- Herbert B. Enderton, *Elements of Set Theory*, Academic Press, 1977,
  ch. 3 "Relations and Functions". PDF fetched from
  http://lib.ysu.am/disciplines_bk/d082ae34f719d34061304625be32601c.pdf
- "Function (mathematics)", Wikipedia, fetched 2026-09-04.
  https://en.wikipedia.org/wiki/Function_(mathematics)

Relational model

- E. F. Codd, "A Relational Model of Data for Large Shared Data Banks",
  *CACM* 13(6), June 1970.
  https://web.eecs.umich.edu/~michjc/eecs584/Papers/codd_1970.pdf
- C. J. Date and Hugh Darwen, *Databases, Types, and the Relational
  Model: The Third Manifesto*, copyright 2014 text.
  https://www.dcs.warwick.ac.uk/~hugh/TTM/DTATRM.pdf
- Michael Stonebraker, "Why Enterprises Are Uninterested in NoSQL",
  BLOG@CACM, 30 September 2010. Live page 403; read via Internet Archive
  snapshot of
  http://cacm.acm.org/blogs/blog-cacm/99512-why-enterprises-are-uninterested-in-nosql/fulltext
- Michael Stonebraker and Rick Cattell, "Ten Rules for Scalable
  Performance in 'Simple Operation' Datastores", *CACM* 54(6), June 2011.
  http://www.cattell.net/datastores/CACM-Paper.pdf
- Ben Moseley and Peter Marks, "Out of the Tar Pit", 2006.
  https://curtclifton.net/papers/MoseleyMarks06a.pdf
- Molham Aref et al., "Rel: A Programming Language for Relational Data",
  arXiv:2504.10323v2, 24 April 2025. https://arxiv.org/pdf/2504.10323
- D. Richard Hipp / SQLite, "SQLite As An Application File Format".
  https://www.sqlite.org/appfileformat.html

Lisp and Erlang

- ANSI Common Lisp HyperSpec, §14.1.2.1 "Lists as Association Lists" and
  the glossary entries "association list" and "property list".
  http://www.lispworks.com/documentation/HyperSpec/Body/14_aba.htm ;
  http://www.lispworks.com/documentation/HyperSpec/Body/26_glo_a.htm ;
  http://www.lispworks.com/documentation/HyperSpec/Body/26_glo_p.htm
- Guy L. Steele Jr., *Common Lisp the Language*, 2nd ed., §15.6.
  https://www.cs.cmu.edu/Groups/AI/html/cltl/clm/node153.html
- John McCarthy et al., *LISP 1.5 Programmer's Manual*, MIT Press, 1962,
  §7.3.
  https://www.softwarepreservation.org/projects/LISP/book/LISP%201.5%20Programmers%20Manual.pdf
- Peter Norvig, *Paradigms of Artificial Intelligence Programming*,
  1992, chs. 3 and 10.
  https://github.com/norvig/paip-lisp/blob/main/docs/chapter3.md ;
  https://github.com/norvig/paip-lisp/blob/main/docs/chapter10.md
- Peter Seibel, *Practical Common Lisp*, 2005, ch. 13.
  https://gigamonkeys.com/book/beyond-lists-other-uses-for-cons-cells.html
- Erlang/OTP stdlib, `proplists` module documentation.
  https://www.erlang.org/doc/apps/stdlib/proplists.html
- Richard A. O'Keefe, "No more need for records", University of Otago,
  November 2003, fifth draft May 2012.
  https://www.cs.otago.ac.nz/staffpriv/ok/frames.pdf
- erlang-questions, "Frames proposal", 29 December 2012 (quoting
  O'Keefe, 3 May 2012).
  http://erlang.org/pipermail/erlang-questions/2012-December/071395.html
- Björn-Egil Dahlberg, "EEP 43: Maps", created 4 April 2013, Final,
  OTP 17.0. https://www.erlang.org/eeps/eep-0043.html
- erlang-questions, May 2013: Richard O'Keefe (9 May), Loïc Hoguin
  (10 May), Joe Armstrong (13 May), Robert Virding (14 May).
  http://erlang.org/pipermail/erlang-questions/2013-May/073667.html ;
  http://erlang.org/pipermail/erlang-questions/2013-May/073674.html ;
  http://erlang.org/pipermail/erlang-questions/2013-May/073700.html ;
  http://erlang.org/pipermail/erlang-questions/2013-May/073724.html

Array languages

- Arthur Whitney, "Abridged Q Language Manual", Kx Systems, 2009.
  https://github.com/KxSystems/kdb/blob/master/d/a/q.htm
- Don Orth, "Q Language Reference Manual", Kx Systems, 2006.
  https://github.com/KxSystems/kdb/blob/master/d/a/q1.htm
- "Dictionaries & tables", kdb+/q documentation, KX.
  https://code.kx.com/q/basics/dictsandtables/ ;
  https://code.kx.com/q/ref/dict/ ; https://code.kx.com/q/ref/flip/
- Jeffry A. Borror, *Q for Mortals*, chs. 5 and 8.
  https://code.kx.com/q4m3/5_Dictionaries/ ;
  https://code.kx.com/q4m3/8_Tables/
- "K Reference Manual", Kx Systems, Version 2.0, 1998 (PDF, text
  self-extracted).
  https://github.com/pyzh/kPARC/blob/master/else.related/k%20reference%20manual%201998%20-%20kreflite.pdf
- "+/kei | K reference card", kparc.github.io/ref, 2019 (authorship not
  established). https://kparc.github.io/ref
- Dyalog Ltd., dfns workspace, "association lists".
  https://dfns.dyalog.com/n_alists.htm
- J Wiki, "Vocabulary/Nouns" and "Essays/DataStructures".
  https://code.jsoftware.com/wiki/Vocabulary/Nouns ;
  https://code.jsoftware.com/wiki/Essays/DataStructures

Implementation

- Raymond Hettinger, "More compact dictionaries with faster iteration",
  python-dev, 10 December 2012.
  https://mail.python.org/pipermail/python-dev/2012-December/123028.html
- CPython `Objects/dictobject.c` (main and v3.6.0 tags);
  `Doc/whatsnew/3.6.rst`, `Doc/whatsnew/3.7.rst`, `Doc/library/stdtypes.rst`.
  https://github.com/python/cpython/blob/main/Objects/dictobject.c
- Guido van Rossum, python-dev, 15 December 2017.
  https://mail.python.org/pipermail/python-dev/2017-December/151283.html
- Maciej Fijałkowski, "Faster, more memory efficient and more ordered
  dictionaries on PyPy", PyPy Status Blog, 22 January 2015.
  https://morepypy.blogspot.com/2015/01/faster-more-memory-efficient-and-more.html
- indexmap (README, `src/inner.rs`, `src/lib.rs`, `RELEASES.md`).
  https://github.com/indexmap-rs/indexmap
- linear-map. https://github.com/contain-rs/linear-map
- vec-map. https://github.com/contain-rs/vec-map
- litemap (ICU4X).
  https://github.com/unicode-org/icu4x/blob/main/utils/litemap/src/lib.rs
- micromap. https://github.com/yegor256/micromap
- wezm/hashmap-vs-vec. https://github.com/wezm/hashmap-vs-vec
- Boost.Container, "Non-standard containers", Boost 1.86.0.
  https://www.boost.org/doc/libs/1_86_0/doc/html/container/non_standard_containers.html
- Zach Laine, "A Standard flat_map", P0429R0 (2016-08-31) and P0429R9
  (2022-06-17).
  https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0429r0.pdf ;
  https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p0429r9.pdf
- Sean Middleditch, "Flat Containers", P0038R0, 2015-09-25.
  https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0038r0.html
- cppreference, `std::flat_map`.
  https://en.cppreference.com/w/cpp/container/flat_map.html
- Chandler Carruth, "Efficiency with Algorithms, Performance with Data
  Structures", CppCon 2014 (slides). https://github.com/CppCon/CppCon2014
- Zig standard library, `lib/std/array_hash_map.zig` and
  `lib/std/multi_array_list.zig` (master, November 2025).
  https://github.com/ziglang/zig
- Mike Acton, "Data-Oriented Design and C++", CppCon 2014 (slides).
  https://github.com/CppCon/CppCon2014
- Casey Muratori, "Semantic Compression", 28 May 2014.
  https://caseymuratori.com/blog_0015
- Richard Fabian, *Data-Oriented Design*, online edition 2018-10-08.
  https://www.dataorienteddesign.com/dodbook/

Datomic, Datalog, Prolog

- "Datomic Data Model", "Glossary", "Entities", "Schema Reference",
  docs.datomic.com. https://docs.datomic.com/whatis/data-model.html ;
  https://docs.datomic.com/glossary.html ;
  https://docs.datomic.com/reference/entities.html
- Rich Hickey talk transcripts (volunteer, not author-published):
  "Writing Datomic in Clojure" (GOTO CPH, May 2012),
  "Deconstructing the Database" (QCon SF, November 2012),
  "The Functional Database" (QCon NY, June 2013),
  "The Value of Values" (JaxConf, July 2012),
  "Effective Programs — 10 Years of Clojure" (Clojure/Conj, October 2017),
  "Maybe Not" (Clojure/conj, November 2018).
  https://github.com/matthiasn/talk-transcripts/tree/master/Hickey_Rich
- Herb Caudill, AI-assisted transcript gist of a Hickey 2012 talk
  (title attribution flagged unreliable by the transcriber).
  https://gist.github.com/HerbCaudill/acf2294dac8e87e24f550715b6991035
- Serge Abiteboul, Richard Hull, Victor Vianu, *Foundations of
  Databases*, Addison-Wesley, 1995 (mirror PDF, self-extracted text).
  https://wiki.epfl.ch/provenance2011/documents/foundations+of+databases-abiteboul-1995.pdf
- Soufflé documentation, "Relations", "Program", "Types".
  https://souffle-lang.github.io/relations ;
  https://souffle-lang.github.io/program ;
  https://souffle-lang.github.io/types
- SWI-Prolog Manual §5.4, "Dicts: structures with named arguments".
  https://www.swi-prolog.org/pldoc/man?section=bidicts

Notations and type theory

- Dhall, "Language Tour" and "Built-in types, functions, and operators".
  https://docs.dhall-lang.org/tutorials/Language-Tour.html ;
  https://docs.dhall-lang.org/references/Built-in-types.html
- Google, "Language Guide (proto3)", §Maps.
  https://protobuf.dev/programming-guides/proto3/
- YAML type repository and YAML 1.2.2 specification.
  https://yaml.org/type/ ; https://yaml.org/type/omap.html ;
  https://yaml.org/type/pairs.html ; https://yaml.org/spec/1.2.2/
- Kenton Varda et al., capnproto group, "Serializing a hash/map?",
  2014–2015. https://groups.google.com/g/capnproto/c/6eT7pBx4_Mc
- CUE language specification. https://cuelang.org/docs/reference/spec/
- Nix language syntax. https://nix.dev/manual/nix/2.24/language/syntax
- Giuseppe Castagna, "Typing Records, Maps, and Structs", *PACMPL* 7,
  ICFP, Article 196, August 2023. https://www.irif.fr/~gc/papers/icfp23.pdf
- Daan Leijen, "Extensible records with scoped labels", *Trends in
  Functional Programming* 2005 (draft rev. 23 July 2005).
  https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/scopedlabels.pdf
- Martin Fowler, "List And Hash", 3 December 2015.
  https://martinfowler.com/bliki/ListAndHash.html
- Go programming language specification. https://go.dev/ref/spec
- Haskell `containers`, `Data.Map.Strict`.
  https://hackage.haskell.org/package/containers/docs/Data-Map-Strict.html
- IETF RFC 8259 (JSON, December 2017) and ECMA-404 2nd edition.
  https://www.rfc-editor.org/rfc/rfc8259.html ;
  https://ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf
- edn-format/edn. https://github.com/edn-format/edn
- TOML v1.0.0. https://toml.io/en/v1.0.0
- IETF RFC 8949 (CBOR, 2020). https://www.rfc-editor.org/rfc/rfc8949.html
- MessagePack specification.
  https://github.com/msgpack/msgpack/blob/master/spec.md
- W3C XML Information Set and XML 1.0.
  https://www.w3.org/TR/xml-infoset/ ; https://www.w3.org/TR/xml/
