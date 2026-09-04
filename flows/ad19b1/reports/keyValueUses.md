# The uses of the key-value paradigm

Research delegated by the main flow: what key-value maps are actually
used for, across systems, and which of those uses survive when the data
is strictly typed and schema-driven.

The living's words, logged in `flows/ad19b1/vision/datom.md`:

> I think that will probably help us to see if key values are actually a
> thing that we want to have in data at all, because Datom [STT: Datum]
> is a revolutionary approach to data representation. It doesn't need to
> implement something simply because it has been so standard in the
> past.

This report answers only that question. It makes no recommendation
about datom; the main flow synthesizes and the living rules.

## Method

Six nested research subflows each took one slice of the survey, fetched
primary sources themselves — specifications, RFCs, official
documentation, papers, man pages on this machine, and source files from
the projects' own repositories — and returned verbatim quotes with the
URL fetched. I fetched a further set myself: RFC 7541, RFC 8446,
RFC 5280, RFC 4512, the OTLP `.proto` and the OpenTelemetry
specification and semantic conventions, the OCI image specification and
its annotation rules, Apache Arrow's `Schema.fbs`, Parquet's
`LogicalTypes.md`, the Cap'n Proto language reference, the Compose
specification, JSON Schema Core, the Kubernetes API conventions,
Kubernetes issues #2004 and #853 through the GitHub API, and the
Kubernetes server-side apply documentation.

Quotes marked with `>` were read in a document that was fetched, by me
or by a named subflow. Where a subflow rather than I fetched a source,
the section says so. Sections and paragraphs headed **Inference** are
not witnessed in any source; where an inference is a subflow's rather
than mine it is marked "(carried)". Anything a subflow could not verify
is carried through as **unverified** and collected in §13.

Three transcription caveats apply. The Thrift whitepaper, the ITU-T
X.680 PDF, Wirth's *Compiler Construction* and the 1991 Self paper were
read from PDF text layers; the subflows restored dropped `fi`/`fl`
ligatures and word spacing without changing words, and say so at each
quote. Several pages were read through a fetch tool that summarizes;
those are marked at the point of use. The ECMA-404 PDF could not be
read at all and nothing is quoted from it.

A prior report in this flow, `reports/mapMerit.md`, covers a different
question: who has argued that a key-value map is really a vector of
structs. Its ground — set theory, Codd, Date and Darwen, alists and
proplists, the array languages, the entries-array-plus-index
implementations, Dhall, protobuf's desugaring, YAML's tag grid, the
JSON/TOML/CBOR/MessagePack/XML comparison table, Castagna 2023 — is not
repeated here. Where this report touches those systems it adds new
material: Cap'n Proto's own generic-map example, protobuf's `Struct`
and `Any`, and the rationale statements the earlier report did not
seek.

---

## What the research found, in short

- **Most of what is called "key-value" is not a map.** Five of the most
  frequently cited cases fail the defining property outright. An HTTP
  header section permits repeats and makes their order significant
  (RFC 9110: "a proxy MUST NOT change the order of these field line
  values"). A query string is specified as "a list of tuples", with
  `getAll` returning values "in list order". A routing table's keys
  denote *overlapping sets*, so RFC 1812's forwarding algorithm "starts
  out with a set of candidate routes that consists of the entire
  contents of the FIB" and prunes. RDF is "a set of RDF triples" whose
  predicate is "a binary relation". EAV rows are time-stamped facts
  about the same `(entity, attribute)` pair. (§1.2, §1.9, §6.1, §7.1,
  §7.2)

- **The largest single use is an index that is never serialized.**
  Storage engines, symbol tables, interners, caches, hidden classes,
  adjacency structures, sparse-matrix build structures, the git object
  store, the Nix store, gettext's compiled MO file. Not one serializes
  its map as text — and where these systems *do* serialize, they emit a
  vector of records: ELF's `Elf64_Sym[]` plus a string table, the JVM's
  `constant_pool` "table of structures", LLVM bitcode v2 (which
  *moved* names out of the symbol table into a string table), SciPy's
  `(data, i, j)` triples, gettext MO's two parallel sorted arrays, git
  `packed-refs` lines, DNS zone-file lines, V7 Unix's 16-byte directory
  records. (§2, §3, §4)

- **The second largest is a record whose field set the notation
  declined to declare.** And in every language case the ecosystem later
  shipped a declaration mechanism to recover what was thrown away:
  Python `__dict__` → `__slots__` → dataclasses → `TypedDict`; Clojure
  maps → `defrecord` → `s/keys`; JavaScript objects → Web IDL's
  `maplike<DOMString, object>`; open telemetry attributes →
  namespaced registry → telemetry schemas with rename migrations.
  Python's docs state the payoff outright: "The space saved over using
  `__dict__` can be significant. Attribute lookup speed can be
  significantly improved as well." (§4.7, §5, §7.4)

- **The fastest implementations of key-value objects work by finding
  the struct inside.** V8: "**While JavaScript objects behave more or
  less like simple dictionaries from the outside, V8 tries to avoid
  dictionaries**"; HiddenClasses "are conceptually similar to classes".
  Self, 1991: "maps look much like classes"; "All constant slots and all
  format information are factored out into the map. Maps reduce the 10
  words per point to 3 words." The dictionary survives in both only as
  the *degraded* mode, entered when no struct was there to find. (§4.7)

- **The genuine map is real, and narrow.** The clearest instances found
  are gettext/Fluent string catalogues, Kubernetes labels and
  annotations, OCI/Docker labels, git refs, the Nix derivation
  environment, TOML's `[dependencies]`-shaped tables, Clojure's
  `s/map-of`, and OpenTelemetry attributes. Their shared profile is
  tighter than "key-value": keys are minted **outside any schema the
  reader holds**, **the value type is uniform**, order carries nothing,
  and uniqueness is required. **The axis that separates a real map from
  a record is value-type uniformity, not key openness.**

- **Open keys usually mark a place where the schema is elsewhere, not
  where there is none.** OpenFeature's evaluation context is open
  because the targeting rules that read it are authored in another
  system after the application ships. Kubernetes labels are open because
  third-party tools add them. TLS extension types, X.509 OIDs,
  OpenTelemetry attribute names and OCI annotation keys are all
  *registries* with namespace grammars, reservation rules and, in
  OpenTelemetry's case, a no-reuse rule and a schema-migration
  mechanism. (§1.8, §6.3, §7.4, §8)

- **Where a strictly typed protocol needs open-ended data, it reaches
  for a vector of structs — never a map.** TLS 1.3:
  `Extension extensions<8..2^16-1>` over
  `struct { ExtensionType extension_type; opaque extension_data<...>; }`.
  X.509: `SEQUENCE OF Extension` where `Extension` has **three**
  fields — `extnID`, `critical`, `extnValue`. HPACK's static table is a
  positionally addressed vector containing duplicate names.
  OpenTelemetry chose `repeated KeyValue` over protobuf's own
  `map<string, AnyValue>`. In each, uniqueness and unorderedness are
  written in prose because the vector cannot carry them, and the value
  is a *tag-dependent union*, not a uniform type. (§8)

- **Schema-first designers split three ways, and each states its
  criterion.** FlatBuffers excludes the map — "**this is a bad match for
  a strongly typed system like FlatBuffers, leading to relatively large
  binaries**" — and offers instead a sorted vector of tables with a
  designated `key` field and `LookupByKey`. GraphQL excludes it — Lee
  Byron: maps "are much more difficult to paginate", and map-in-API is
  "an API anti-pattern as indexing is an issue of storage and an issue
  of client caching but not an issue of transport" — with the
  list-of-tuples given as the sanctioned alternative. Thrift includes it
  on the opposite criterion: "focusing on the key types available in all
  programming languages". ASN.1, Cap'n Proto, XML Schema, RELAX NG and
  Kaitai Struct simply have none. (§9)

- **Two schema-first systems record what the map cost them.** Avro had
  to punch a hole in its own total order: "**map data may not be
  compared. It is an error to attempt to compare data containing maps**"
  — every other type gets an ordering rule. Thrift had to concede that
  its declared key type does not survive: "the key type for map should
  be a basic type ... the JSON protocol only supports key types that are
  base types." (§9.8, §9.9)

- **Six production formats already define the map as a vector of
  two-field structs.** Arrow: "A Map is a logical nested type that is
  represented as `List<entries: Struct<key: K, value: V>>`", with the
  candid rider "**we do not constrain the key and value types, so the
  application is responsible for ensuring that the keys are hashable and
  unique**". Parquet: "`MAP` must annotate a 3-level structure",
  and — omit the value half — "it can be represented ... as a set of
  keys". Plus protobuf's desugaring, Dhall's `Map`, FlatBuffers'
  sorted-vector idiom, and **Cap'n Proto's language reference, whose
  worked example of a generic type is the map itself**:
  `struct Map(Key, Value) { entries @0 :List(Entry); struct Entry { key @0 :Key; value @1 :Value; } }`.
  (§9.1, §9.2, §9.10)

- **Kubernetes forbade maps of subobjects outright, in writing, and
  said why.** "**There are no maps of subobjects in any API objects.
  Instead, the convention is to use a list of subobjects containing name
  fields.** ... This rule maintains the invariant that all JSON/YAML keys
  are fields in API objects. **The only exceptions are pure maps in the
  API (currently, labels, selectors, annotations, data)**". The reason
  is a reader's reason — Joe Beda: "**the novice user won't know what
  `www` is. Is this a magic value that they aren't supposed to change
  (like `ports`) or is it an input/naming thing that they should
  change?**" — and a parser's reason — Brian Grant: "**In JSON and YAML,
  structures and maps cannot be distinguished without a schema.**" The
  one cost they discovered, that "lists do not allow generic merging",
  was later paid off by declaring in the schema that a given vector of
  structs *is* a map: `x-kubernetes-list-type: map` with
  `x-kubernetes-list-map-keys`. (§10)

- **serde names the axis the whole question turns on, and it is not
  "keyed versus indexed".** serde calls both `map` and `struct`
  "heterogeneous". What separates them is whether the shape is known
  **without looking at the serialized data** — and that is exactly what
  buys compactness: "**Other formats may be able to omit the field names
  when serializing structs because the corresponding `Deserialize`
  implementation is required to know what the keys are without looking
  at the serialized data.**" FlatBuffers' "bad match for a strongly
  typed system", GraphQL's "shape of query should match shape of
  result", and serde's phrase are three names for one property. A map is
  the single construct where the schema cannot predict the value's
  shape, because the keys live in the data. (§9.7, §9.13)

- **When a real dictionary gets big enough to matter, nobody writes it
  in nested map syntax.** gettext PO puts `msgid`/`msgstr` on separate
  lines with a blank line between entries and comment lines carrying
  per-entry provenance; DNS zone files are "predominantly
  line-oriented"; git `packed-refs` is `<hash> SP <refname>` per line;
  Nix `.drv` writes `("k","v")` pairs in a list; V7 directories were an
  array of 16-byte records. Five independent designs, five flat record
  vectors. (§3.3, §3.4, §3.6, §3.7, §6.2)

---

## 1. Configuration and environment: key-value as text people write

### 1.1 POSIX environment variables

IEEE Std 1003.1-2024, XBD §8.1 "Environment Variable Definition"
(https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html,
fetched by a nested subflow):

> The value of an environment variable is an arbitrary sequence of
> bytes, except for the null byte. For a C-language program, an array
> of strings called the environment shall be made available when a
> process begins.

> These strings have the form name=value; names shall not contain any
> bytes that have the encoded value of the character '='. […] There is
> no meaning associated with the order of strings in the environment.
> **If more than one string in an environment of a process has the same
> name, the consequences are undefined.**

> The name space of environment variable names containing lowercase
> letters is reserved for applications.

And §8.3 on `PATH`:

> This variable shall represent the sequence of path prefixes that
> certain functions and utilities apply in searching for an executable
> file. The prefixes shall be separated by a <colon> (':').

> Since <colon> is a separator in this context, directory names that
> might be used in PATH should not include a <colon> character.

`ld.so(8)` on `LD_LIBRARY_PATH`
(https://man7.org/linux/man-pages/man7/environ.7.html and
https://man7.org/linux/man-pages/man8/ld.so.8.html):

> The items in the list are separated by either colons or semicolons,
> and **there is no support for escaping either separator**.

The subflow ran an experiment on this machine (Linux 7.1.8, glibc
2.42): a C program calling `execve` with
`envp = {"FOO=first", "FOO=second", "PATH=/usr/bin", NULL}` produced a
child in which `getenv("FOO")` returned `first` and `environ` still
held both strings; `env FOO=a FOO=b env` by contrast printed only
`FOO=b`. Duplicates survive the mechanism; the tools that build
environments collapse them.

- **Keys**: mixed. The POSIX-named variables are a de-facto record
  whose field names a standard fixes; the lowercase namespace is
  explicitly reserved for open-ended application use.
- **Value type**: uniform — every value is a byte string. Every richer
  type (`PATH`'s colon list, a locale name's
  `language[_territory][.codeset][@modifier]` grammar) is a per-key
  grammar hidden inside that string, with no escape mechanism.
- **Order**: explicitly meaningless.
- **Uniqueness**: not required; duplicates are *undefined*, not
  forbidden, and pass through `execve` intact.
- **Text or index**: text — a serialized `name=value` array handed
  across a process boundary.

### 1.2 HTTP header fields, and the retrofit of types onto them

RFC 9110 §5 (https://www.rfc-editor.org/rfc/rfc9110.txt, fetched):

> HTTP uses "fields" to provide data in the form of extensible
> name/value pairs with a **registered key namespace**.

> Field names are case-insensitive and ought to be registered within
> the "Hypertext Transfer Protocol (HTTP) Field Name Registry".

§5.2 and §5.3 settle order and duplication, and they settle them the
opposite way from a map:

> When a field name is repeated within a section, its combined field
> value consists of the list of corresponding field line values within
> that section, concatenated in order, with each field line value
> separated by a comma.

> **The order in which field lines with the same name are received is
> therefore significant to the interpretation of the field value; a
> proxy MUST NOT change the order of these field line values when
> forwarding a message.**

> The order in which field lines with differing field names are
> received in a section is not significant.

> *Note:* In practice, the "Set-Cookie" header field often appears in a
> response message across multiple field lines and does not use the
> list syntax, violating the above requirements […] recipients ought to
> handle "Set-Cookie" as a special case.

HPACK, RFC 7541 (https://www.rfc-editor.org/rfc/rfc7541.txt, fetched by
me), makes the same point in the binary encoding. Its terminology
section:

> Header Field:  A name-value pair.  Both the name and value are
> treated as opaque sequences of octets.

> Header List:  A header list is an **ordered collection** of header
> fields that are encoded jointly and **can contain duplicate header
> fields**.

> Static Table:  The static table […] is a table that statically
> associates header fields that occur frequently with index values.
> This table is ordered, read-only, always accessible, and it may be
> shared amongst all encoding or decoding contexts.

§2.1:

> HPACK preserves the ordering of header fields inside the header list.
> An encoder MUST order header field representations in the header
> block according to their ordering in the original header list.

And Appendix A's static table is a vector of two-field structs
addressed by ordinal, with duplicate names as separate entries:
index 2 is `:method GET`, index 3 is `:method POST`.

**RFC 9651, Structured Field Values for HTTP** (2024, obsoleting
RFC 8941; https://www.rfc-editor.org/rfc/rfc9651.txt, fetched by a
subflow) is the case of a standards body deliberately typing an
existing key-value text format. Its motivation:

> Specifying the syntax of new HTTP header (and trailer) fields is an
> onerous task […] Once a field is defined, bespoke parsers and
> serializers often need to be written, because each field value has a
> slightly different handling of what looks like common syntax.

What it asks a field author to do:

> **Specify the type of the field value; either List (Section 3.1),
> Dictionary (Section 3.2), or Item (Section 3.3).**

Its Dictionary:

> **Dictionaries are ordered maps of key-value pairs**, where the keys
> are short textual strings and the values are Items or arrays of
> Items, both of which can be Parameterized. There can be zero or more
> members, and their **keys are unique in the scope of the Dictionary**
> they occur within.

> **Implementations MUST provide access to Dictionaries both by index
> and by key.** Specifications MAY use either means of accessing the
> members.

> Typically, a field specification will define the semantics of
> Dictionaries by **specifying the allowed type(s) for individual
> members by their keys**, as well as whether their presence is
> required or optional. Recipients MUST ignore members whose keys are
> undefined or unknown, unless the field's specification specifically
> disallows them.

> Note that when duplicate Dictionary keys are encountered, all but the
> last instance are ignored.

Appendix A.1, "Why Not JSON?":

> For example, JSON has specification issues around large numbers and
> **objects with duplicate members**. Although advice for avoiding these
> issues is available (e.g., [RFC7493]), it cannot be relied upon.

The subflow counted the IANA HTTP Field Name Registry
(https://www.iana.org/assignments/http-fields/field-names.csv, fetched
2026-09-04): **259 registered field names; 221 with an empty Structured
Type; 18 `Item`, 11 `Dictionary`, 8 `List`, 1 `Token`.**

- **Keys**: registry-drawn, extensible; unknown fields must be
  forwarded and are otherwise ignored.
- **Value type**: per key. Each field name names its own grammar. The
  Structured Fields retrofit hoists that grammar into a declared type,
  recorded in the registry.
- **Order**: significant among equal names, insignificant among
  differing names. A Structured Fields Dictionary is *ordered by
  definition* and indexable by position.
- **Uniqueness**: not required in a header section — repeats are legal
  and combine. Required inside a Structured Fields Dictionary, enforced
  last-wins at parse time.
- **Text or index**: text on the wire; an index in every
  implementation.

**Note.** The Structured Fields Dictionary is a map that is *ordered*,
*unique-keyed*, *indexable by position*, and whose value types are
declared per key by an outside specification. Every one of those four
properties is a property of a vector of typed structs, not of a
hash map.

### 1.3 TOML

TOML v1.0.0 (https://toml.io/en/v1.0.0, fetched by a subflow):

> TOML is designed to map unambiguously to a hash table.

> The primary building block of a TOML document is the key/value pair.
> […] **Values must have one of the following types.** String / Integer
> / Float / Boolean / Offset Date-Time / Local Date-Time / Local Date /
> Local Time / Array / Inline Table. Unspecified values are invalid.

> Bare keys may only contain ASCII letters, ASCII digits, underscores,
> and dashes […] Note that bare keys are allowed to be composed of only
> ASCII digits, e.g. 1234, but are **always interpreted as strings**.

> Defining a key multiple times is invalid.

> Tables (also known as hash tables or dictionaries) are collections of
> key/value pairs.

> **Key/value pairs within tables are not guaranteed to be in any
> specific order.**

For contrast, the array-of-tables construct is where TOML does put
order into the model:

> The first instance of that header defines the array and its first
> table element, and each subsequent instance creates and defines a new
> table element in that array. **The tables are inserted into the array
> in the order encountered.**

- **Keys**: both uses, over one construct. Nothing in the syntax
  distinguishes `[server] port = 80` (a record) from
  `[dependencies] serde = "1.0"` (a map of user-chosen names).
- **Value type**: per key. TOML has no way to say that every value in
  a table has one type, and no way to constrain key names.
- **Order**: meaningless within a table.
- **Uniqueness**: essential and enforced at parse time.
- **Text or index**: text.

### 1.4 YAML mappings

YAML 1.2.2 §3.2.1.1 (https://yaml.org/spec/1.2.2/, fetched by a
subflow; the prior report quotes the same passage):

> The content of a mapping node is an unordered set of key/value node
> pairs, with the restriction that each of the keys is unique. […] In
> particular, keys may be arbitrary nodes.

§3.2.2.1, "Mapping Key Order", is the passage that matters here:

> In the representation model, mapping keys do not have an order. To
> serialize a mapping, it is necessary to impose an ordering on its
> keys. This order is a serialization detail and should not be used
> when composing the representation graph. **In every case where node
> order is significant, a sequence must be used. For example, an
> ordered mapping can be represented as a sequence of mappings, where
> each mapping is a single key/value pair.**

§3.2.1.3 records what key uniqueness costs a format whose scalars are
untyped:

> Since YAML mappings require key uniqueness, representations must
> include a mechanism for testing the equality of nodes. This is
> non-trivial since YAML allows various ways to format scalar content.
> For example, the integer eleven can be written as "0o13" (octal) or
> "0xB" (hexadecimal). If both notations are used as keys in the same
> mapping, **only a YAML processor which recognizes integer formats
> would correctly flag the duplicate key as an error**.

- **Keys**: open-ended and untyped; arbitrary nodes, not only strings.
- **Value type**: per key.
- **Order**: meaningless in the model; the spec's own answer for
  ordered key-value data is a sequence of single-pair mappings.
- **Uniqueness**: essential in the model, partial in enforcement.
- **Text or index**: text.

### 1.5 JSON objects, and the schema languages that must tell the two uses apart

The prior report settles JSON's ordering and duplicate rules. What
this survey adds is the evidence that the record use and the map use
are not a folk distinction: every schema language over JSON had to
build *separate machinery* for them, because the syntax does not carry
the difference.

JSON Schema draft 2020-12, Core §10.3.2
(https://json-schema.org/draft/2020-12/json-schema-core, fetched by me
and independently by a subflow):

> **properties** — The value of "properties" MUST be an object. Each
> value of this object MUST be a valid JSON Schema. Validation succeeds
> if, for each name that appears in both the instance and as a name
> within this keyword's value, the child instance for that name
> successfully validates against the corresponding schema.

> **patternProperties** — The value of "patternProperties" MUST be an
> object. Each property name of this object SHOULD be a valid regular
> expression […] Each property value of this object MUST be a valid
> JSON Schema.

> **additionalProperties** — The behavior of this keyword depends on
> the presence and annotation results of "properties" and
> "patternProperties" within the same schema object. Validation with
> "additionalProperties" applies only to the child values of instance
> names that do not appear in the annotation results of either
> "properties" or "patternProperties".

> **propertyNames** — If the instance is an object, this keyword
> validates if every property name in the instance validates against
> the provided schema. Note the property name that the schema is
> testing will always be a string.

The official learning documentation
(https://json-schema.org/understanding-json-schema/reference/object)
names the map use in its first line and the key-convention use plainly:

> Objects are the mapping type in JSON. They map "keys" to "values". In
> JSON, the "keys" must always be strings.

> Sometimes you want to say that, given a particular kind of property
> name, the value should match a particular schema. That's where
> patternProperties comes in: it maps regular expressions to schemas.

> [propertyNames] can be useful if you don't want to enforce specific
> properties, but you want to make sure that the names of those
> properties follow a specific convention.

OpenAPI v3.1.0 (https://spec.openapis.org/oas/v3.1.0.html, fetched by a
subflow) states the distinction as doctrine:

> **The schema exposes two types of fields: Fixed fields, which have a
> declared name, and Patterned fields, which declare a regex pattern
> for the field name.**

and uses a type constructor for the map case: Components Object
"schemas — `Map[string, Schema Object]`", Server Object "variables —
`Map[string, Server Variable Object]` — A map between a variable name
and its value"; while the genuinely open-ended keyed objects are
declared as Patterned Fields with the key's grammar spelled out — Paths
Object: "A relative path to an individual endpoint. **The field name
MUST begin with a forward slash (/).**"; Responses Object: "Any HTTP
status code can be used as the property name, but only one property per
code."

**Inference.** Everything a schema says about the *map* case is what a
typed language writes as `Map<K, V>`: a key type
(`propertyNames`/`Map[string, …]`), one value type
(`additionalProperties: <schema>`), and a cardinality
(`minProperties`/`maxProperties`, a constraint that is meaningless for
a record). Everything it says about the *record* case is a field list
with per-field types. The two are not variants of one thing in any
schema language examined; they are two different declarations that
happen to share a syntax.

### 1.6 INI, Java .properties, .env, systemd

`java.util.Properties`
(https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Properties.html,
fetched by a subflow):

> **Each key and its corresponding value in the property list is a
> string.**

> Because Properties inherits from Hashtable, the put and putAll
> methods can be applied to a Properties object. **Their use is strongly
> discouraged as they allow the caller to insert entries whose keys or
> values are not Strings.**

> The keys and elements are written in the natural sort order of the
> keys in the entrySet().

Windows INI, `GetPrivateProfileString`
(https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getprivateprofilestring):

> If lpKeyName is NULL, the function copies all key names in the
> specified section to the supplied buffer. An application can use this
> method to enumerate all of the sections and keys in a file.

systemd, `systemd.syntax(7)`
(https://manpages.debian.org/unstable/systemd/systemd.syntax.7.en.html
— freedesktop.org returned HTTP 418 to the subflow):

> The syntax is inspired by XDG Desktop Entry Specification .desktop
> files, which are in turn inspired by Microsoft Windows .ini files.

> **Various settings are allowed to be specified more than once, in
> which case the interpretation depends on the setting. Often, multiple
> settings form a list, and setting to an empty value "resets"** […]
> Note that using multiple assignments to the same value makes the file
> incompatible with parsers for the XDG .desktop file format.

Docker's `.env`
(https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/):

> Each line represents a key-value pair. Values can optionally be
> quoted. […] `VAR="{\"hello\": \"json\"}"` -> `{"hello": "json"}`

- **Keys**: fixed by an external, usually prose, schema — the
  program's documentation names them.
- **Value type**: uniformly string in all four. Numbers, booleans,
  lists and whole JSON documents are strings the consumer re-parses.
- **Order**: meaningless; Java's `store` proves it by rewriting the
  file in sorted key order. systemd is the exception, where repeated
  assignments to a list-valued setting accumulate in order.
- **Uniqueness**: conventional. systemd explicitly permits and defines
  repeats *per setting*.
- **Text or index**: text.

### 1.7 The two shapes offered side by side: Compose

The Compose Specification
(https://github.com/compose-spec/compose-spec/blob/main/05-services.md,
fetched by me) offers the *same data* in both shapes and says so:

> `environment` defines environment variables set in the container.
> **`environment` can use either an array or a map.**

with "Map syntax:" (`RACK_ENV: development`) and "Array syntax:"
(`- RACK_ENV=development`) given as two renderings of one thing.

The OCI Image Specification
(https://github.com/opencontainers/image-spec/blob/main/config.md,
fetched by me) picked the vector for the same data:

> **Env** *array of strings*, OPTIONAL — Entries are in the format of
> `VARNAME=VARVALUE`.

### 1.8 Kubernetes labels and annotations; Docker labels

These are the cases in the configuration slice where the key set is
genuinely not knowable by a schema author.

Kubernetes labels
(https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/,
fetched by a subflow):

> **Labels are key/value pairs that are attached to objects** […] Each
> object can have a set of key/value labels defined. **Each Key must be
> unique for a given object.**

> Valid label keys have two segments: an optional prefix and name,
> separated by a slash (/). […] The prefix is optional. If specified,
> the prefix must be a DNS subdomain.

> **If the prefix is omitted, the label Key is presumed to be private
> to the user.** Automated system components […] must specify a prefix.

Kubernetes annotations:

> You can use Kubernetes annotations to attach **arbitrary
> non-identifying metadata** to objects.

> Note: **The keys and the values in the map must be strings. In other
> words, you cannot use numeric, boolean, list or other types for
> either the keys or the values.**

Docker labels
(https://docs.docker.com/engine/manage-resources/labels/):

> A label is a key-value pair, stored as a string. […] **each key must
> be unique within an object. If the same key is given multiple values,
> the most-recently-written value overwrites all previous values.**

> Label values can contain any data type that can be represented as a
> string, including (but not limited to) JSON, XML, CSV, or YAML. The
> only requirement is that the value be serialized to a string first
> […] **Since Docker doesn't deserialize the value, you can't treat a
> JSON or XML document as a nested structure when querying or filtering
> by label value.**

The OCI Image Specification's annotation rules
(https://github.com/opencontainers/image-spec/blob/main/annotations.md,
fetched by me) are the same design written as a standard:

> Annotations MUST be a key-value map where both the key and value MUST
> be strings.
> While the value MUST be present, it MAY be an empty string.
> Keys MUST be unique within this map, and best practice is to
> namespace the keys.
> Keys SHOULD be named using a reverse domain notation.
> The prefix `org.opencontainers` is reserved […]
> Consumers MUST NOT generate an error if they encounter an unknown
> annotation key.

And then the same document lists the pre-defined keys, each with its
own value type in prose:
`org.opencontainers.image.created` "conforming to RFC 3339",
`org.opencontainers.image.licenses` an "SPDX License Expression",
`org.opencontainers.image.ref.name` with an EBNF grammar of its own.

- **Keys**: genuinely open-ended, supplied by users and third parties.
  The systems defend against collision with a *namespace grammar*
  rather than an enumeration, and reserve the unprefixed space for the
  user.
- **Value type**: uniform string, stated as a restriction, and the
  consequence named ("you can't treat a JSON or XML document as a
  nested structure").
- **Order**: meaningless.
- **Uniqueness**: essential, last-write-wins.
- **Text or index**: written and read as text in manifests; Kubernetes
  additionally builds a query index over labels, which is why
  annotations, which are not selectable, are a separate field.

**Inference.** This is the shape of a genuine map in configuration:
open-ended keys governed by a *key grammar with namespaces*, one
uniform value type, no order, unique keys. And the moment a
pre-defined key acquires a real type — an RFC 3339 date, an SPDX
expression — the uniform string type stops carrying it and prose takes
over. The record is still there, smuggled through the map.

### 1.9 Query strings: the most-written key-value text on the web is not a map

The WHATWG URL Standard §5 (https://url.spec.whatwg.org/, fetched by a
subflow):

> **The application/x-www-form-urlencoded format provides a way to
> encode a list of tuples, each consisting of a name and a value.**

> The application/x-www-form-urlencoded format is in many ways an
> aberrant monstrosity, the result of many years of implementation
> accidents and compromises […]

The parser and serializer are defined over a *list* with no
de-duplication step anywhere:

> Let output be an initially empty **list of name-value tuples** where
> both name and value hold a string. […] Append (nameString,
> valueString) to output.

> A URLSearchParams object has an associated **list: a list of tuples
> each consisting of a name and a value**, initially empty.

> The **getAll(name)** method steps are to return the values of all
> tuples whose name is name in this's list, **in list order**.

> The **set(name, value)** method steps are: If this's list contains any
> tuples whose name is name, then set the value of the first such tuple
> to value **and remove the others**.

> It can be useful to sort the name-value tuples in a URLSearchParams
> object, **in particular to increase cache hits**. This can be
> accomplished through invoking the sort() method.

- **Keys**: open-ended; empty names are legal.
- **Value type**: uniform string; a missing value is `""`, not absent.
- **Order**: preserved by construction and observable. Sorting is an
  explicit, opt-in normalization, done for cache hits.
- **Uniqueness**: explicitly not required. Duplicates are first-class,
  with `getAll`, a two-argument `has(name, value)` and a two-argument
  `delete(name, value)` built for them.
- **Text or index**: text, defined by a parse and a serialize algorithm
  over a list, with no map anywhere in the data model.

**Inference (carried from the subflow).** The most-written key-value
text on the web is specified, at the standards level, as an ordered
list of pairs. Every treatment of a query string as a map is a lossy
projection applied downstream, and the spec keeps the lossless form
available beside it.

---

## 2. Key-value stores: the paradigm as a storage interface

This is the use the phrase "key-value" most often names, and it is the
one furthest from a data notation. Gathered by a nested research
subflow which fetched each source itself; quotes carried unchanged.

### 2.1 LevelDB and RocksDB

LevelDB README
(https://github.com/google/leveldb/blob/main/README.md):

> LevelDB is a fast key-value storage library written at Google that
> provides an **ordered mapping** from string keys to string values.

>   * Keys and values are arbitrary byte arrays.
>   * **Data is stored sorted by key.**
>   * Callers can provide a custom comparison function to override the
>     sort order.

> This is not a SQL database. It does not have a relational data model,
> it does not support SQL queries, and it has no support for indexes.

`doc/index.md` shows what an application actually keys by:

> The preceding examples used the default ordering function for key,
> which orders bytes lexicographically. You can however supply a custom
> comparator when opening a database. For example, suppose **each
> database key consists of two numbers** and we should sort by the first
> number, breaking ties by the second number.

and, on key evolution:

> you could save some space by not encoding a version number in the
> key. Instead, ... reserve a bit of each key (one byte should suffice
> for most uses). When you wish to switch to a new key format ... (b)
> increment the version number for new keys (c) change the comparator
> function so it uses the version numbers found in the keys to decide
> how to interpret them.

RocksDB Overview
(https://github.com/facebook/rocksdb/wiki/RocksDB-Overview):

> RocksDB is a storage engine library of key-value store interface where
> keys and values are arbitrary byte streams. **RocksDB organizes all
> data in sorted order** and the common operations are `Get(key)`,
> `NewIterator()`, `Put(key, val)`, `Delete(key)`, and
> `SingleDelete(key)`.

> All data in the database is logically arranged in sorted order. An
> application can specify a key comparison method that specifies a total
> ordering of keys. An `Iterator` API allows an application to do a
> range scan on the database.

RocksDB Prefix-Seek — the store's admission that the key has internal
structure:

> "Prefix" is defined by options.prefix_extractor, which is a
> shared_pointer of a `SliceTransform` instance.

> A motivating use case for prefix seek is **representing multi-maps**,
> such as secondary indexes in MyRocks, where the RocksDB prefix is the
> key for the multimap and a RocksDB iterator finds all the entries
> associated with that prefix.

### 2.2 Redis

Redis data types
(https://redis.io/docs/latest/develop/data-types/ and
`.../data-types/hashes/`):

> Redis hashes are **record types** modeled as collections of
> field-value pairs. As such, Redis hashes resemble Python
> dictionaries, Java HashMaps, and Ruby hashes.

> Redis hashes are record types structured as collections of
> field-value pairs. **You can use hashes to represent basic objects**
> and to store groupings of counters, among other things.

The keyspace page
(https://redis.io/docs/latest/develop/using-commands/keyspace/) is the
strongest evidence anywhere of a schema hand-encoded into a key string:

> **Redis doesn't support namespaces or other categories for keys, so
> you must take care to avoid name collisions.** However, there is a
> convention for using the colon ":" character to split keys into
> sections (for example, "person:1", "person:2", "office:London",
> "office:NewYork:1").

> Very short keys are often not a good idea. There is little point in
> writing "u1000flw" as a key if you can instead write
> "user:1000:followers".

> **Try to stick with a schema.** For instance "object-type:id" is a
> good idea, as in "user:1000".

> Normally, the whole key is used to calculate the hash index, but there
> are some situations where you need to hash only a part of the key. You
> can select the section of the key you want to hash using a pair of
> curly braces {...} to create a hashtag. For example, the keys person:1
> and person:2 produce different hash indices but {person}:1 and
> {person}:2 produce the same index.

**Correction carried from the subflow.** The older Redis phrasing
"perfect to represent objects" is **not** in the live documentation.
The current text is quoted above; the older wording is marked
unverified.

### 2.3 memcached

Protocol documentation
(https://github.com/memcached/memcached/blob/master/doc/protocol.txt):

> Data stored by memcached is identified with the help of a key. A key
> is a text string which should uniquely identify the data for clients
> that are interested in storing and retrieving it.

> **The server will transmit back unstructured data in exactly the same
> way it received it, as a byte stream. The server doesn't care about
> byte order issues in unstructured data and isn't aware of them.**

> `<flags>` is an arbitrary 16-bit unsigned integer ... that the server
> stores along with the data and sends back when the item is retrieved.
> Clients may use this as a bit field to store data-specific
> information; **this field is opaque to the server.**

memcached.org, on what the key names:

> Memcached is an in-memory key-value store for small chunks of
> arbitrary data (strings, objects) **from results of database calls,
> API calls, or page rendering**.

with the site's own canonical example, in which the key is a function
name concatenated with its argument:

```
function get_foo(foo_id)
    foo = memcached_get("foo:" . foo_id)
    return foo if defined foo
    foo = fetch_foo_from_database(foo_id)
    memcached_set("foo:" . foo_id, foo)
    return foo
end
```

### 2.4 DynamoDB, and the original Dynamo paper

AWS DynamoDB Developer Guide, "Core components"
(https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html):

> **Items** – Each table contains zero or more items. An item is **a
> group of attributes** that is uniquely identifiable among all of the
> other items. ... Items in DynamoDB are similar in many ways to rows,
> records, or tuples in other database systems.

> **Other than the primary key, the People table is schemaless**, which
> means that neither the attributes nor their data types need to be
> defined beforehand. Each item can have its own distinct attributes.

> **Partition key and sort key** – Referred to as a composite primary
> key, this type of key is composed of two attributes. ... **All items
> with the same partition key value are stored together, in sorted order
> by sort key value.**

> **Each primary key attribute must be a scalar** (meaning that it can
> hold only a single value). **The only data types allowed for primary
> key attributes are string, number, or binary.** There are no such
> restrictions for other, non-key attributes.

DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store",
SOSP 2007 — read from the authors' own posting at
https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html
(the PDF could not be converted in the subflow's environment):

> **Query Model: simple read and write operations to a data item that is
> uniquely identified by a key. State is stored as binary objects (i.e.,
> blobs) identified by unique keys. No operations span multiple data
> items and there is no need for relational schema.**

> applications that use Dynamo do not require support for hierarchical
> namespaces (a norm in many file systems) or complex relational schema

### 2.5 etcd

etcd data model (https://etcd.io/docs/v3.5/learning/data_model/):

> **The store's logical view is a flat binary key space. The key space
> has a lexically sorted index on byte string keys so range queries are
> inexpensive.**

> etcd stores the physical data as key-value pairs in a persistent
> b+tree. ... **The key of key-value pair is a 3-tuple (major, sub,
> type).**

etcd API (https://etcd.io/docs/v3.5/learning/api/) — a hierarchy
explicitly removed:

> **The etcd data model indexes all keys over a flat binary key space.
> This differs from other key-value store systems that use a
> hierarchical system of organizing keys into directories. Instead of
> listing keys by directory, keys are listed by key intervals [a, b).**

> Like a hierarchical store, intervals support single key lookups via
> [a, a+1) ... and directory lookups by encoding keys by directory
> depth. In addition to those operations, intervals can also encode
> prefixes.

etcd "Why" page:

> In short, choose etcd for storing metadata or coordinating distributed
> applications. If storing more than a few GB of data or if full SQL
> queries are needed, choose a NewSQL database.

### 2.6 Bigtable

Chang et al., "Bigtable: A Distributed Storage System for Structured
Data", OSDI 2006, USENIX proceedings HTML
(https://www.usenix.org/legacy/event/osdi06/tech/chang/chang_html/index.html):

> **A Bigtable is a sparse, distributed, persistent multi-dimensional
> sorted map. The map is indexed by a row key, column key, and a
> timestamp; each value in the map is an uninterpreted array of bytes.**

> Bigtable maintains data in lexicographic order by row key.

> **Clients can exploit this property by selecting their row keys so
> that they get good locality for their data accesses. For example, in
> Webtable, pages in the same domain are grouped together into
> contiguous rows by reversing the hostname components of the URLs.**

> Column keys are grouped into sets called column families, which form
> the basic unit of access control. **All data stored in a column family
> is usually of the same type.**

> **A column key is named using the following syntax: family:qualifier.
> Column family names must be printable, but qualifiers may be arbitrary
> strings.**

and the authors' own summary:

> **The model we chose is richer than simple key-value pairs, and
> supports sparse semi-structured data.**

### 2.7 Berkeley DB and FoundationDB

Olson, Bostic, Seltzer, "Berkeley DB", USENIX 1999
(https://www.usenix.org/legacy/publications/library/proceedings/usenix99/full_papers/olson/olson_html/index.html):

> The software stores and retrieves records, which consist of key/value
> pairs. ... **Otherwise, Berkeley DB does not examine or interpret
> either keys or values in any way.**

> Berkeley DB supports three access methods: B+tree, Extended Linear
> Hashing (Hash), and Fixed- or Variable-length Records (Recno). ... **In
> the B+tree and Hash access methods, keys can have arbitrary structure.
> In the Recno access method, each record is assigned a record number,
> which serves as the key.**

FoundationDB, "Data Modeling"
(https://apple.github.io/foundationdb/data-modeling.html):

> **FoundationDB's core data model is an ordered key-value store.** Also
> known as an ordered associative array, map, or dictionary, this is a
> common data structure composed of a collection of key-value pairs in
> which all keys are unique. Starting with this simple model, an
> application can create higher-level data models by mapping their
> elements to individual keys and values.

> In FoundationDB, both keys and values are simple byte strings. Apart
> from storage and retrieval, the database does not interpret or depend
> on the content of values. **In contrast, keys are treated as members
> of a total order**, the lexicographic order over the underlying bytes.

> **Composite types.** An application's data is often represented using
> composite types, such as structures or records with multiple fields.
> **It's very useful for the application to use composite keys to store
> such data. In FoundationDB, composite keys can be conveniently
> represented as tuples that are mapped to individual keys for storage.**

> **FoundationDB provides a tuple layer** (available in each language
> binding) that encodes tuples into keys. ... **The layer works by
> preserving the natural ordering of the tuples.**

> The standard tuple layer provides an order-preserving, signed,
> variable length encoding [for integers].

"Layer Concept" (https://apple.github.io/foundationdb/layer-concept.html):

> Using indexing as an example, FoundationDB's core provides no indexing
> and never will. Instead, a layer provides indexing by storing two
> kinds of key-values, one for the data and one for the index. **For
> example, the `people/alice/eye_color = blue` key-value stores data
> about Alice's eye color and the `eye_color/blue/alice = true`
> key-value stores an index of people by eye color.**

### 2.8 What the storage slice shows

Per the five axes, and carrying the subflow's inferences:

- **Keys**: in every case a *composite flattened into bytes*. LevelDB's
  tutorial key "consists of two numbers"; RocksDB configures a
  `prefix_extractor` to re-derive the boundary; Redis instructs users
  to concatenate `object-type:id:field` because the server has no
  namespaces; Bigtable's key is literally a 3-tuple whose column half
  is itself `family:qualifier`; DynamoDB's is `(partition key, sort
  key)`, both of them *attributes of the record itself*; etcd's
  physical key is `(major, sub, type)`; FoundationDB names the practice
  and ships a tuple layer for it.
- **Value type**: opaque bytes in LevelDB, RocksDB, Berkeley DB,
  memcached, Bigtable cells, etcd, FoundationDB and Dynamo-2007. Typed
  in exactly two: Redis (per-key, a dozen server-known types) and
  DynamoDB (an item is a record of typed attributes). Those two are
  also the only two whose documentation stops saying "value" and starts
  saying **record** and **attributes**.
- **Order**: sorted, contractually, in six of eight — and the sort is
  the primary read operation beyond point lookup. The two unordered
  ones are the two that are not databases: memcached (a cache) and
  Redis's top-level keyspace.
- **Uniqueness**: essential everywhere, sometimes qualified by a
  namespace (RocksDB column family) or a version axis (etcd revisions,
  Bigtable timestamps).
- **Text or index**: **none of the eight serializes its map as text.**
  They are libraries, wire protocols and services. The only textual
  artifacts are the key strings, and those are text by accident of
  being byte strings people type.

**Inference (carried).** As soon as a key-value store is meant to
answer questions rather than merely remember answers, it becomes an
*ordered* structure. The word "map" is doing the wrong work: these are
sorted sequences with a lookup index. And the key is a struct that has
been serialized to make it sortable, which forces the application to
re-parse it on the way out — a workaround for an untyped interface, not
a feature.

---

## 3. Naming and content addressing: when the key is a name, and when it is the value

Gathered by a nested research subflow, which fetched web sources and
read local man pages and store files on this machine; quotes and marks
carried unchanged, with my own additions marked.

### 3.1 Git object database — the key is a function of the value

`gitformat-loose(5)`, local man page, git 2.55.0:

> The entire contents, prefix and data concatenated, is then compressed
> with zlib and the compressed data is stored in the file. **The object
> ID of the object is the SHA-1 or SHA-256 (as appropriate) hash of the
> uncompressed data.**

`gitglossary(7)`:

> **object** — The unit of storage in Git. It is uniquely identified by
> the SHA-1 of its contents. Consequently, an object cannot be changed.

Pro Git ch. 10
(https://git-scm.com/book/en/v2/Git-Internals-Git-Objects):

> Git is a content-addressable filesystem. Great. What does that mean?
> It means that at the core of Git is a simple key-value data store.
> What this means is that you can insert any kind of content into a Git
> repository, for which Git will hand you back a unique key you can use
> later to retrieve that content.

The subflow verified on this machine that the key is a pure function of
the value, computable with no store present:

```
$ printf 'what is up, doc?' | git hash-object --stdin
bd9dbf5aae1a3862dd1526723246b20206e5fc37
$ python3 -c "import hashlib; c=b'what is up, doc?'; print(hashlib.sha1(b'blob %d\0'%len(c)+c).hexdigest())"
bd9dbf5aae1a3862dd1526723246b20206e5fc37
```

- **Keys**: derived entirely from the value. Neither schema-fixed nor
  open-ended data — *computed*.
- **Value type**: uniform at the storage layer; the type tag lives
  inside the value, not in the key.
- **Order**: none.
- **Uniqueness**: automatic and definitional.
- **Text or index**: pure index. Delete it and it can be rebuilt by
  hashing every value.

**Inference (carried).** The object store's "map" carries zero
information the values do not already carry. Under a strict schema this
is not a map type at all: it is a set of values plus a derived lookup
function.

### 3.2 Git tree objects — a sorted vector of four-field records

`gitglossary(7)`:

> **tree object** — An object containing a list of file names and modes
> along with refs to the associated blob and/or tree objects. A tree is
> equivalent to a directory.

Pro Git ch. 10:

> A single tree object contains one or more entries, each of which is
> the SHA-1 hash of a blob or subtree with its associated mode, type,
> and filename.

The order and duplicate rules are enforced from outside the format, by
a checker. `git-fsck(1)`, local man page (I confirmed these two msg-ids
myself):

> **treeNotSorted** — (ERROR) A tree is not properly sorted.
> **duplicateEntries** — (ERROR) A tree contains duplicate file entries.

`git-mktree(1)`:

> Reads standard input in non-recursive ls-tree output format, and
> creates a tree object. **The order of the tree entries is normalized
> by mktree so pre-sorting the input is not required.**

The subflow demonstrated both halves on this machine: feeding `mktree`
the same entries in reverse produced the identical hash; and `mktree`
happily emitted a tree with two entries named `dup`, which `git fsck
--strict` then rejected with `duplicateEntries`.

- **Keys**: the `name` field is open-ended data, but structurally it is
  not a key — it is one field of a four-field record
  `(mode, type, hash, name)`.
- **Value type**: uniform; every entry is the same record shape, and
  `mode`, not the key, discriminates blob from tree from symlink.
- **Order**: carries no meaning and is fully canonicalized, because it
  is part of the hash.
- **Uniqueness**: essential, enforced by a *validator*, not by the
  format.
- **Text or index**: serialized data — a binary record vector.

**Inference (carried).** A git tree is literally a sorted vector of
structs, and every property people want from a map — unique keys,
canonical order — had to be re-imposed on top of the vector by an
external checker.

### 3.3 Git refs — a genuine name→hash map, serialized as lines

`gitglossary(7)`:

> **ref** — A name that points to an object name or another ref (the
> latter is called a symbolic ref) ... The ref namespace is
> hierarchical.

`git-pack-refs(1)`:

> Traditionally, tips of branches and tags (collectively known as refs)
> were stored one file per ref in a (sub)directory under `$GIT_DIR/refs`
> directory. ... **This command is used to solve the storage and
> performance problem by storing the refs in a single file,
> `$GIT_DIR/packed-refs`.**

`git-fsck(1)` msg-ids constrain the text format:

> **packedRefEntryNotTerminated** — (ERROR) The "packed-refs" file
> contains an entry that is not terminated by a newline.
> **packedRefUnsorted** — (ERROR) The "packed-refs" file is not sorted.

and the real file on this machine reads:

```
# pack-refs with: peeled fully-peeled sorted
2ab53a91cdba39cdaf0a8858541c9dbd01e67eff refs/heads/main
```

- **Keys**: open-ended, human-chosen, hierarchical names. Not derived
  from the value. This is a real map.
- **Value type**: uniform — one object name per ref (or, for a symref,
  another ref name, marked by the `ref: ` prefix inside the value).
- **Order**: no meaning, canonicalized anyway, for binary search.
- **Uniqueness**: essential; in the loose form the filesystem enforces
  it.
- **Text or index**: both. The authoritative loose form is the
  filesystem. The packed form is a **line-oriented text file**,
  `<hash> SP <refname> LF` — a record-per-line vector, not a nested map
  notation.

### 3.4 The Nix store and the `.drv` format

Nix manual, "Store Path" (local manual, Nix 2.35.1; same text at
https://nix.dev/manual/nix/2.28/store/store-path):

> Think of a store path base name as an opaque, unique identifier: The
> only way to obtain a store path base name is by adding or building
> store objects. A store path base name will always reference exactly
> one store object. **Store path base names are pairs of • A 20-byte
> digest for identification • A symbolic name for people to read**

> **fingerprint = type ":sha256:" inner-digest ":" store ":" name**

So the digest is a hash of a fingerprint that *includes the name and
the store directory*: the key is derived from value ⊕ name ⊕ location,
not from the value alone.

The `.drv` format is where Nix serializes what its own JSON schema
calls a map. `protocols/json/schema/derivation-v4.yaml`:

```yaml
      env:
        type: object
        title: Environment variables
        description: |
          Environment variables passed to the `builder`.
        additionalProperties:
          type: string
```

and the on-disk ATerm form of an actual derivation on this machine ends

```
...("mesonFlags",""),("name","vendor-cargo-deps"),("nativeBuildInputs",""),
("out","/nix/store/85nlgxlld2apjz59cwdizscm98r3imdb-vendor-cargo-deps"),
...("system","x86_64-linux")])
```

The subflow parsed all 33 keys and verified they are bytewise sorted.

**Inference (carried).** Nix's canonical on-disk form for a field its
own schema types as a homogeneous string map is *a sorted vector of
pairs*. Same conclusion as git trees, reached independently, for the
same reason: the serialization is hashed, so it must be canonical.

### 3.5 IPLD, DAG-CBOR and DAG-JSON — the map's freedom revoked to make it addressable

IPLD data model kinds
(https://github.com/ipld/ipld/blob/master/docs/data-model/kinds.md):

> #### Map kind
> Map is a recursive kind.
> Values in maps are accessed by their "key".
> Maps can also be iterated over, yielding key+value pairs.

That is the whole definition. The subflow grepped the page for
`sort|order|duplicat|uniq` and found nothing on the subject.

DAG-CBOR (https://ipld.io/specs/codecs/dag-cbor/spec/):

> The primary differences are: ... **Maps must only be keyed by
> strings.** Additional strictness requirements are applied to ensure
> canonical data encoding forms.

> **In DAG-CBOR, map keys must be strings. Other map keys, such as ints,
> are not supported and should be rejected when encountered.**

> **DAG-CBOR requires that there exist a single, canonical way of
> encoding any given set of data**, and that encoded forms contain no
> superfluous data that may be ignored or lost in a round-trip
> decode/encode.

> **The keys in every map must be sorted in (byte-wise) lexical order,
> including their major type 3 and length. Therefore, the keys are
> sorted by length first.**

and then the retreat:

> Due to the existence and active use of historical data, and the
> existence and active use of non-conforming encoders, DAG-CBOR decoders
> may relax strictness requirements by default ... **Map key ordering:
> map entries may be accepted in any order**

DAG-JSON (https://ipld.io/specs/codecs/dag-json/spec/) goes further and
makes key order *semantic*:

> **Maps are sorted by key.**

> Codec implementations **MUST** do the following when encoding data in
> order to ensure hashes consistently match for the same block data.
> — Sort object keys by their (UTF-8) encoded representation, i.e. with
> byte comparisons — Strip whitespace

> Maps with the first key of `"/"` are considered the **reserved
> namespace** in DAG-JSON as they are used to represent Bytes and Links.

> Data with the following forms are strictly not valid DAG-JSON ...
> *Maps with more than one key, where the first key is `"/"` and its
> value is a string.* e.g. `{"/":"foo","bar":"baz"}`
> **Where a key exists that sorts before `"/"`, the map is valid**, e.g.
> `{"0bar":"baz","/":"foo"}`.

CBOR itself supplies the uniqueness rule DAG-CBOR does not state.
RFC 8949 §5.3.1:

> **Duplicate keys in a map**: Generic decoders ... make data available
> to applications using the native CBOR data model. **That data model
> includes maps (key-value mappings with unique keys), not multimaps**
> (key-value mappings where multiple entries can have the same key).
> Thus, a generic decoder that gets a CBOR map item that has duplicate
> keys will decode to a map with only one instance of that key, or it
> might stop processing altogether.

**Inference (carried).** IPLD wanted a JSON-shaped, order-free,
string-keyed map. The moment the bytes had to hash reproducibly it had
to forbid non-string keys, mandate a total order on keys, forbid
indefinite-length encoding, and lean on CBOR for uniqueness — and even
then publish an escape hatch because real data did not comply. The
map's freedom was entirely revoked to make it addressable, and what
remains is a sorted vector of (string, value) pairs. In DAG-JSON the
canonical order then leaks into *meaning*: which key sorts first
decides whether the map is a Link, a Bytes, or an ordinary map.

### 3.6 POSIX directories

IEEE Std 1003.1-2024
(https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap03.html):

> **3.103 Directory** — A file that contains directory entries. **No two
> directory entries in the same directory have the same name.**

> **3.104 Directory Entry (or Hard Link)** — An object that associates a
> filename with a file. **Several directory entries can associate names
> with the same file.**

`<dirent.h>`:

> **The internal format of directories is unspecified.**

> It shall also define the structure `dirent` which shall include the
> following members:
> `ino_t d_ino` File serial number. `char d_name[]` Filename string of
> entry.

The V7 Unix directory was literally a vector of two-field structs. The
V7 `dir(5)` man page's body is a `.so` include of the header, so the
man page *is* the header
(https://github.com/dspinellis/unix-history-repo, `Research-V7`,
`usr/sys/h/dir.h`, complete file):

```c
#ifndef	DIRSIZ
#define	DIRSIZ	14
#endif
struct	direct
{
	ino_t	d_ino;
	char	d_name[DIRSIZ];
};
```

- **Keys**: open-ended data — filenames, preserved unaltered.
- **Value type**: uniform — one file reference per entry.
- **Order**: carries no meaning and is *not* canonicalized. POSIX never
  fixes it; `scandir`/`alphasort` and `ls`'s own collation exist to
  impose one at read time.
- **Uniqueness**: essential and definitional. Note the converse is not
  required — several names may denote one file.
- **Text or index**: index, explicitly ("The internal format of
  directories is unspecified"). Historically it *was* a serialized
  array of fixed-size two-field records.

**Note (carried, unverified).** The subflow could not find POSIX text
declaring `readdir` order unspecified; POSIX calls a directory stream
"an ordered sequence" and never constrains which order. That is an
omission, not a quoted guarantee.

### 3.7 DNS

RFC 1034 §3.1:

> **The domain name space is a tree structure.** ... **Brother nodes may
> not have the same label**, although the same label can be used for
> nodes which are not brothers.

RFC 1034 §3.6:

> The set of resource information associated with a particular name is
> composed of separate resource records (RRs). **The order of RRs in a
> set is not significant, and need not be preserved by name servers,
> resolvers, or other parts of the DNS.**

> The owner name is often implicit, rather than forming an integral part
> of the RR. ... **The remaining RR parts are the fixed header (type,
> class, TTL) which is consistent for all RRs, and a variable part
> (RDATA) that fits the needs of the resource being described.**

RFC 2181 §5:

> **It is meaningless for two records to ever have label, class, type
> and data all equal - servers should suppress such duplicates if
> encountered.** It is however possible for most record types to exist
> with the same label, class and type, but with different data. **Such a
> group of records is hereby defined to be a Resource Record Set
> (RRSet).**

RFC 1035 §4.1.2 gives the composite lookup key: `QNAME` / `QTYPE` /
`QCLASS`. And §5.1 gives the text format:

> **The format of these files is a sequence of entries. Entries are
> predominantly line-oriented**, though parentheses can be used to
> continue a list of items across a line boundary.

> **If an entry for an RR begins with a blank, then the RR is assumed to
> be owned by the last stated owner.**

> Omitted class and TTL values are default to the last explicitly stated
> values. **Since type and class mnemonics are disjoint, the parse is
> unique.**

- **Keys**: composite — `(QNAME, QCLASS, QTYPE)`. Names are open-ended,
  hierarchical, per-level unique. The `TYPE` component is a *closed,
  schema-fixed enumeration*.
- **Value type**: a fixed header plus a type-discriminated variable
  part — a tagged union, not a heterogeneous map. And the value at a
  key is a **set**, not a single value.
- **Order**: explicitly not significant, and not canonicalized in the
  base protocol.
- **Uniqueness**: essential at `(label, class, type, data)`.
  Multiplicity at `(label, class, type)` is the point.
- **Text or index**: both. The authored form is a line-oriented record
  format with no nesting at all, in which the tree is recovered from
  *string suffixes* (`$ORIGIN` plus relative names).

**Correction carried from the subflow.** The statement that RR order is
insignificant is in RFC 1034 §3.6, not RFC 2181 §5; RFC 2181 §5
contains no ordering statement.

### 3.8 The pattern across the naming slice

The subflow's own table, carried:

| system | order canonicalized? | witnessed by |
|---|---|---|
| git tree | yes, sorted; part of the hash | `treeNotSorted` (ERROR); `mktree` "order … is normalized" |
| git packed-refs | yes, sorted | `packedRefUnsorted` (ERROR); header `sorted` |
| Nix `.drv` env | yes, sorted (verified on a real file) | 33/33 keys bytewise sorted |
| DAG-CBOR | yes, mandated length-first bytewise | "keys in every map must be sorted…" |
| DAG-JSON | yes, mandated bytewise UTF-8 | "Maps are sorted by key"; MUST |
| POSIX directory | **no** | `scandir`/`alphasort` exist to impose it |
| DNS RRset | **no** | "order … is not significant" |

**Inference (carried).** The split is not about maps; it is about
whether the bytes are the identity. The two systems that do not
canonicalize are precisely the two that never serialize the mapping as
a document. Every system that writes a mapping down as content that
gets hashed had to strip the map of the one property that distinguishes
it from a sorted vector of pairs.

**Inference (carried).** Uniqueness is required by every item in the
slice, and in four of five it is enforced *outside the format*: git
needs `fsck`; POSIX pushes it into the filesystem; DAG-CBOR borrows it
from RFC 8949; DNS asks servers to suppress duplicates.

**Inference (carried).** When these systems had to write a name→value
mapping as text, none chose a nested map notation. git packed-refs is
one line per entry. DNS zone files are line-oriented records with
context inheritance. Nix `.drv` writes `[(k,v),(k,v),…]`. V7
directories were a fixed-size two-field record array. Four independent
designs, four flat record vectors.

---

## 4. Inside the program: the map as an implementation device

Gathered by a nested research subflow. Where a source was a PDF whose
extraction damaged spacing or ligatures, the subflow says so and I
carry the mark.

### 4.1 Symbol tables

The subflow could not reach a legitimate copy of the Dragon Book §2.7
(`dragonbook.stanford.edu` fails TLS; search returned only paraphrases
and pirate scans) and **refused to quote it from memory**. It
substituted Niklaus Wirth, *Compiler Construction* (Addison-Wesley
1996, revised 2017), author-hosted at ETH Zürich
(https://people.inf.ethz.ch/wirth/CompilerConstruction/CompilerConstruction1.pdf),
§8.1:

> The context is represented by a data structure which contains an
> entry for every declared identifier. This entry associates the
> identifier with the denoted object and its properties. The data
> structure is known by the name **symbol table**.

Wirth's declared structure is a **linked list of records**, not a hash
map:

```
Object = POINTER TO ObjDesc;
ObjDesc = RECORD name: Ident; class: INTEGER; type: Type;
                 next: Object; val: LONGINT END
```

> The new entry is appended at the end of the list, **so that the list
> mirrors the order of the declarations in the source text**.

> **Note that the linear ordering of entries must also be recorded,
> because it is significant in the case of procedure parameters.**

LLVM Programmer's Manual
(https://llvm.org/docs/ProgrammersManual.html):

> The ValueSymbolTable class provides a symbol table that the Function
> and Module classes use for naming value definitions. ... **Note that
> not all LLVM Values have names, and those without names (i.e., they
> have an empty name) do not exist in the symbol table.**

rustc dev guide (https://rustc-dev-guide.rust-lang.org/print.html):

> The name of every function, variable, module, etc. is not stored as a
> string, but rather as an opaque `Symbol` which is essentially an ID
> number for each identifier. **The compiler keeps a separate hashtable
> that allows us to recover the human-readable name of a Symbol when
> necessary** (such as when printing a syntax error).

- **Keys**: open-ended data — identifiers drawn from the source text.
- **Value type**: uniform per table, but the record is a **tagged
  union**; Wirth's `class` field discriminates constant, variable, type
  and procedure.
- **Order**: mostly irrelevant, **but not always** — Wirth states it is
  significant for procedure parameters, and record field offsets are
  computed by walking the scope list in declaration order.
- **Uniqueness**: essential within a scope; in rustc, unique *per
  namespace*, so a type and a value may share a name.
- **Text or index**: pure in-memory index, rebuilt from source on every
  compile. LLVM's textual `.ll` IR has no symbol-table section.

### 4.2 Interning, and what a *serialized* symbol table actually looks like

`rustc_span::symbol` module documentation
(https://doc.rust-lang.org/nightly/nightly-rustc/rustc_span/symbol/index.html):

> An 'interner' is a data structure that associates values with usize
> tags and allows bidirectional lookup.

> `pub struct Symbol(SymbolIndex);` … An interned UTF-8 string.
> **Internally, a Symbol is implemented as an index, and all operations
> (including hashing, equality, and ordering) operate on that index.**

The serialized forms are the point. The ELF gABI
(https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.symtab.html):

> An object file's symbol table holds information needed to locate and
> relocate a program's symbolic definitions and references. **A symbol
> table index is a subscript into this array.**

```c
typedef struct {
    Elf64_Word      st_name;
    unsigned char   st_info;
    unsigned char   st_other;
    Elf64_Half      st_shndx;
    Elf64_Addr      st_value;
    Elf64_Xword     st_size;
} Elf64_Sym;
```

> **st_name** — This member holds an index into the object file's symbol
> string table, which holds the character representations of the symbol
> names.

> **In each symbol table, all symbols with STB_LOCAL binding precede the
> weak and global symbols.**

And the string table (`.../ch4.strtab.html`) is not a map at all:

> a string table index may refer to any byte in the section. **A string
> may appear more than once; references to substrings may exist; and a
> single string may be referenced multiple times. Unreferenced strings
> also are allowed.**

The JVM specification §4.1 and §4.4
(https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html):

> **The constant_pool is a table of structures** representing various
> string constants, class and interface names, field names, and other
> constants ... The format of each constant_pool table entry is
> indicated by its first 'tag' byte.

> **The constant_pool table is indexed from 1 to constant_pool_count -
> 1.**

> All constant_pool table entries have the following general format:
> `cp_info { u1 tag; u1 info[]; }` ... **The format of the additional
> information depends on the tag byte.**

And LLVM bitcode moved in the same direction between versions
(https://llvm.org/docs/BitCodeFormat.html):

> In version 2, the meaning of module records FUNCTION, GLOBALVAR,
> ALIAS, IFUNC and COMDAT change such that **the first two operands
> specify an offset and size of a string in a string table**, the
> function name is removed from the FNENTRY record in the value symbol
> table.

**Inference (carried).** Every real, strictly typed, *serialized*
symbol table found — ELF, the JVM class file, LLVM bitcode v2 —
represents "name → info" as an array of fixed-shape records where the
name is an offset into a separate blob. The map exists only as a
transient index the reader rebuilds, and the direction of travel is
one-way: LLVM *moved* names out of the symbol-table block into a string
table.

### 4.3 Caches and memoization

Python `functools`
(https://docs.python.org/3/library/functools.html):

> `@functools.cache(user_function)` — Simple lightweight unbounded
> function cache. Sometimes called 'memoize'. ... **creating a thin
> wrapper around a dictionary lookup for the function arguments.**

> Distinct argument patterns may be considered to be distinct calls with
> separate cache entries. For example, `f(a=1, b=2)` and `f(b=2, a=1)`
> differ in their keyword argument order and may have two separate cache
> entries.

> **In general, the LRU cache should only be used when you want to reuse
> previously computed values.**

Guava `Cache`
(https://guava.dev/releases/33.0.0-jre/api/docs/com/google/common/cache/Cache.html)
and `CacheBuilder`:

> **A semi-persistent mapping from keys to values.** Cache entries ...
> are **stored in the cache until either evicted or manually
> invalidated.**

> **Note that the cache may evict an entry before this limit is
> exceeded.**

> If weakKeys, weakValues, or softValues are requested, **it is possible
> for a key or value present in the cache to be reclaimed by the garbage
> collector.**

memcached's protocol:

> `<exptime>` is expiration time. **If it's 0, the item never expires
> (although it may be deleted from the cache to make place for other
> items).**

- **Keys**: open-ended *and derived* — the argument tuple, not anything
  a schema names. Python's own note that `f(a=1,b=2)` and `f(b=2,a=1)`
  may be different keys shows key identity is not even semantic
  identity.
- **Value type**: uniform — the function's return type.
- **Order**: irrelevant. LRU recency is metadata about access, not
  content.
- **Uniqueness**: essential, but a duplicate key is not an error, it is
  a *hit*.
- **Text or index**: purely an index over data that lives elsewhere,
  never serialized as authoritative.

**Inference (carried).** A cache's contents are derived and disposable
*by specification*: memcached reserves the right to delete a
never-expiring item, Guava may evict before the stated limit,
`cache_clear()` is always available. This is the purest case of the map
as implementation device: it has no serialized form because it has no
meaning to serialize.

### 4.4 Counting, histograms and sparse arrays

Python `collections.Counter`
(https://docs.python.org/3/library/collections.html):

> **A Counter is a dict subclass for counting hashable objects.** ...
> **The Counter class is similar to bags or multisets in other
> languages.**

> `most_common(n=None)` — **Return a list** of the n most common
> elements and their counts.

> **Equality and inclusion compare corresponding counts.**

The sparse-matrix case is the decisive one. SciPy `dok_matrix`
(https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.dok_matrix.html):

> **Dictionary Of Keys based sparse matrix. This is an efficient
> structure for constructing sparse matrices incrementally.**

> - Allows for efficient O(1) access of individual elements.
> - **Duplicates are not allowed.**
> - **Can be efficiently converted to a coo_matrix once constructed.**

`coo_matrix`
(https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.html):

> **A sparse matrix in COOrdinate format.** Also known as the 'ijv' or
> 'triplet' format.

> `coo_matrix((data, (i, j)), [shape=(M, N)])` — **to construct from
> three arrays**

> **Advantages of the COO format** — facilitates fast conversion among
> sparse formats; **permits duplicate entries**

> **Intended Usage** — COO is a fast format for constructing sparse
> matrices. **Once a COO matrix has been constructed, convert to CSR or
> CSC format for fast arithmetic** ... **duplicate (i,j) entries will be
> summed together.** This facilitates efficient construction of finite
> element matrices and the like.

> **Canonical format** — Entries and coordinates sorted by row, then
> column. There are no duplicate entries.

**Inference (carried).** SciPy is the cleanest evidence that the map
form and the record-sequence form are the same object at different
phases. The dict-of-keys exists to answer "set A[i,j]" one element at a
time; when editing stops, SciPy's own docs say convert to parallel
arrays. And the two forms differ *semantically*, not only in speed: DOK
cannot express a duplicate, COO can and gives it a meaning
(summation). Here the map form is strictly **less** expressive — the
uniqueness constraint that makes it a map forbids the
accumulate-by-repetition idiom that finite-element assembly wants.

### 4.5 Sets as maps to unit

Rust `HashSet`
(https://doc.rust-lang.org/std/collections/struct.HashSet.html):

> **A hash set implemented as a `HashMap` where the value is `()`.**

Java `HashSet`:

> **This class implements the Set interface, backed by a hash table
> (actually a HashMap instance).**

The Go blog, "Go maps in action" (https://go.dev/blog/maps):

> It can be convenient that a map retrieval yields a zero value when the
> key is not present. **For instance, a map of boolean values can be
> used as a set-like data structure.**

> **When iterating over a map with a range loop, the iteration order is
> not specified and is not guaranteed to be the same from one iteration
> to the next.** If you require a stable iteration order you must
> maintain a separate data structure that specifies that order.

The idiom appears in Go's own standard library
(`src/mime/mediatype.go`, `FormatMediaType`):

```go
seenAttrs := make(map[string]struct{}, len(param))
for _, attribute := range slices.Sorted(maps.Keys(param)) {
    ...
    if _, ok := seenAttrs[attribute]; ok { return "" }
    seenAttrs[attribute] = struct{}{}
```

— note that the *input* map's keys are sorted before iteration,
precisely because Go map order is unspecified and the output is
serialized text.

C++ and Python do **not** do this. ISO C++ working draft
(https://eel.is/c++draft/set.overview,
https://eel.is/c++draft/map.overview):

> [map.overview] **A map is an associative container that supports
> unique keys** ... and provides for fast retrieval of values of another
> type T based on the keys.

> [set.overview] **A set is an associative container that supports
> unique keys** ... and provides for fast retrieval of **the keys
> themselves**.

CPython `Objects/setobject.c`, file header:

> set object implementation … **Derived from Objects/dictobject.c.**

> **Use cases for sets differ considerably from dictionaries where
> looked-up keys are more likely to be present. In contrast, sets are
> primarily about membership testing** where the presence of an element
> is not known in advance.

And a specification apologizing for the idiom in serialized form — the
OCI Image Specification's `ExposedPorts`:

> **NOTE:** This JSON structure value is unusual because it is a direct
> JSON serialization of the Go type `map[string]struct{}` and is
> represented in JSON as an object mapping its keys to an empty object.

Parquet says the same thing from the type side
(https://github.com/apache/parquet-format/blob/master/LogicalTypes.md):

> The `value` field encodes the map's value type and repetition. This
> field can be `required`, `optional`, or omitted. ... **If not present,
> it can be represented as a map with all null values or as a set of
> keys.**

- **Keys**: open-ended data — the members.
- **Value type**: **there is no value.** `()`, `struct{}`, always-true
  `bool`, an empty object. Zero information.
- **Order**: irrelevant, and the standards say so.
- **Uniqueness**: the entire content of the structure. A set is nothing
  but a uniqueness constraint.
- **Text or index**: in-memory; serializes as a *list* in every format
  examined, except where a Go type leaked into a JSON spec and the spec
  had to flag it.

**Inference (carried).** Where a language has a map and no set (Go),
programmers reach for map-to-unit at the *user* level. Where a language
ships a set, the map-to-unit is confined to the *implementation* and
the set gets its own type. CPython went further and forked the dict
code, with a comment saying the use cases differ. Map-to-unit is a
workaround for a missing set type, visible from both directions.

### 4.6 Graph adjacency

NetworkX
(https://networkx.org/documentation/stable/reference/introduction.html):

> **All graph classes allow any hashable object as a node.**

> The graph internal data structures are based on an adjacency list
> representation and implemented using Python dictionary datastructures.
> **The graph adjacency structure is implemented as a Python dictionary
> of dictionaries.**

> This design allows for **possible replacement of the
> 'dicts-of-dicts'-based datastructure with an alternative datastructure
> that implements the same methods.**

> For MultiGraph/MultiDiGraph we use a **dict-of-dicts-of-dicts-of-dicts**
> where the third dictionary is keyed by an edge key identifier.

Boost Graph Library
(https://www.boost.org/doc/libs/1_84_0/libs/graph/doc/adjacency_list.html,
`.../adjacency_matrix.html`) implements the same interface with no maps
at all:

> **An adjacency-list is basically a two-dimensional structure, where
> each element of the first dimension represents a vertex, and each of
> the vertices contains a one-dimensional structure that is its edge
> list.**

> For a graph with V vertices, a V x V matrix is used, where each
> element a_(ij) is a boolean flag.

- **Keys**: open-ended data — user-supplied node identity in NetworkX.
  Boost sidesteps it: vertices are integer indices into a vector, and
  the node's real name is a *property* attached to the vertex.
- **Value type**: uniform at each nesting level, except that the
  innermost edge-attribute dict is a genuinely heterogeneous **record**.
- **Order**: irrelevant.
- **Uniqueness**: essential for `Graph`, **deliberately abandoned** for
  `MultiGraph`, which synthesises a fourth key level purely to permit
  duplicates.
- **Text or index**: in-memory index, explicitly swappable.

### 4.7 Hidden classes: the fastest implementations of key-value objects find the struct inside

V8, "Fast properties in V8" (https://v8.dev/blog/fast-properties):

> In V8 every JavaScript object has a HiddenClass associated. **The
> HiddenClass stores information about the shape of an object, and among
> other things, a mapping from property names to indices into the
> properties.**

> **HiddenClasses are conceptually similar to classes in typical
> object-oriented programming languages.**

> **The basic assumption about HiddenClasses is that objects with the
> same structure — e.g. the same named properties in the same order —
> share the same HiddenClass.**

> **While JavaScript objects behave more or less like simple
> dictionaries from the outside, V8 tries to avoid dictionaries because
> they hamper certain optimizations such as inline caches.**

> **Fast properties are simply accessed by index in the properties
> store.**

> However, if many properties get added and deleted from an object, it
> can generate a lot of time and memory overhead ... Hence, V8 also
> supports so-called **slow properties**. An object with slow properties
> has a self-contained dictionary as a properties store. ... **Since
> inline caches don't work with dictionary properties, the latter are
> typically slower.**

Chambers, Ungar and Lee, "An Efficient Implementation of SELF, a
Dynamically-Typed Object-Oriented Language Based on Prototypes",
*Lisp and Symbolic Computation* 4(3), 1991, §3.1
(https://bibliography.selflanguage.org/_static/implementation.pdf; the
subflow extracted the PDF itself and restored word spacing and the `fi`
ligature without changing wording):

> **To compensate for the absence of classes, our system uses
> implementation-level maps to transparently group objects cloned from
> the same prototype, providing data type information and eliminating
> the apparent space overhead for prototype-based systems.**

> **We have invented maps as an implementation technique to efficiently
> represent members of a clone family.** In our SELF object storage
> system, objects are represented by the values of their assignable
> slots, if any, and a pointer to the object's map; **the map is shared
> by all members of the same clone family. For each slot in the object,
> the map contains the name of the slot, whether the slot is a parent
> slot, and either the offset within the object of the slot's contents
> ... or the slot's contents itself**

> **From the implementation point of view, maps look much like classes,
> and achieve the same sorts of space savings for shared data.**

> **All constant slots and all format information are factored out into
> the map. Maps reduce the 10 words per point to 3 words.**

**Inference (carried).** Two independent industrial efforts,
twenty-eight years apart, on the two most prominent dynamic object
languages, converged on the identical move: take the key-value object,
factor the keys and per-key metadata out into a shared immutable
descriptor, and leave behind a fixed-offset array of values — a struct.
The dictionary survives in both only as the *degraded* mode, entered
when an object is used in genuinely map-like fashion, and paying for it
with the loss of inline caching. The residual dictionary marks
precisely the cases where no struct was there to find.

---

## 5. Dynamic object systems: one construct doing two jobs

Gathered by a nested research subflow; quotes carried unchanged.

### 5.1 JavaScript

ECMA-262 §6.1.7 (https://tc39.es/ecma262/):

> Each instance of the Object type ... represents a collection of
> properties. ... **A property key is either a String or a Symbol.**

§10.1.11.1 `OrdinaryOwnPropertyKeys` — the property-order rule, in full:

> 1. Let keys be a new empty List.
> 2. For each own property key propertyKey of obj such that propertyKey
>    is **an array index, in ascending numeric index order**, do
>    a. Append propertyKey to keys.
> 3. For each own property key propertyKey of obj such that propertyKey
>    is a String and propertyKey is not an array index, **in ascending
>    chronological order of property creation**, do
>    a. Append propertyKey to keys.
> 4. For each own property key propertyKey of obj such that propertyKey
>    is a Symbol, **in ascending chronological order of property
>    creation**, do
>    a. Append propertyKey to keys.

but `for-in` is separately left unspecified, §14.7.5.9:

> **The mechanics and order of enumerating the properties is not
> specified** but must conform to the rules specified below.

MDN's "Objects vs. Maps" comparison
(https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
opens with the history:

> Object is similar to Map—both let you set keys to values, retrieve
> those values, delete keys, and detect whether something is stored at a
> key. **For this reason (and because there were no built-in
> alternatives), Object has been used as Map historically.**

and lists the differences. The rows that matter here:

> **Key Types** — Map: "A Map's keys can be any value (including
> functions, objects, or any primitive)." Object: "The keys of an Object
> must be either a String or a Symbol."

> **Key Order** — Map: "A Map object iterates entries, keys, and values
> in the order of entry insertion." Object: "**Although the keys of an
> ordinary Object are ordered now, this was not always the case, and the
> order is complex. As a result, it's best not to rely on property
> order.** ... note that no single mechanism iterates all of an object's
> properties; the various mechanisms each include different subsets of
> properties."

> **Serialization and parsing** — Map: "**No native support for
> serialization or parsing.**" Object: "Native support for serialization
> from Object to JSON, using JSON.stringify()."

That last row is directly load-bearing: **JavaScript's textual notation
covers only the Object, not the Map.** The map-shaped thing has no text
syntax at all.

MDN also records that the Web platform's "maplike" declarations
*re-impose* key and value types:

> unlike Map they only allow specific predefined types for the keys and
> values of each entry. The allowed types are set in the specification
> IDL definition. For example, RTCStatsReport is a Map-like object that
> must use strings for keys and objects for values:
> `readonly maplike<DOMString, object>;`

- **Keys**: both uses in one type. As a record, fixed by the program's
  convention with no enforcement; as a map, open-ended data.
- **Value type**: per key when used as a record; nominally uniform when
  used as a map, unenforced either way.
- **Order**: specified for `[[OwnPropertyKeys]]`, unspecified for
  `for-in`; MDN advises not relying on it.
- **Uniqueness**: essential and enforced.
- **Text or index**: Object is both; **Map is index only**.

**Note (carried, unverified).** The subflow found no TC39 prose
rationale arguing objects were inadequate as maps; the archived ES wiki
strawman is executable spec only. MDN's sentence is the best-sourced
statement of the rationale found. Incidentally, that strawman's
executable spec implements Map as **two parallel arrays**, `keys[]` and
`vals[]`.

### 5.2 Lua

Lua 5.4 Reference Manual §2.1
(https://www.lua.org/manual/5.4/manual.html), two consecutive
paragraphs:

> The type table implements associative arrays, that is, arrays that can
> have as indices not only numbers, but any Lua value except nil and
> NaN. ... **Tables can be heterogeneous; that is, they can contain
> values of all types (except nil).**

> **Tables are the sole data-structuring mechanism in Lua; they can be
> used to represent ordinary arrays, lists, symbol tables, sets,
> records, graphs, trees, etc. To represent records, Lua uses the field
> name as an index. The language supports this representation by
> providing `a.name` as syntactic sugar for `a["name"]`.**

§6.1 on `next`:

> **The order in which the indices are enumerated is not specified, even
> for numeric indices.**

**Inference (carried).** Lua is the clean extreme of the one-type
position, and its own manual documents the two dialects of use in
adjacent sentences. The sugar is the tell: the record use gets a
*different surface syntax* even inside a language that has only one
underlying type.

### 5.3 Python: `__dict__` versus `__slots__`

Python language reference §3.2.11 and §3.3.2
(https://docs.python.org/3/reference/datamodel.html):

> A class instance has a namespace implemented as a dictionary which is
> the first place in which attribute references are searched.

> The default behavior for attribute access is to get, set, or delete
> the attribute from an object's dictionary. For instance, `a.x` has a
> lookup chain starting with `a.__dict__['x']`.

§3.3.2.4:

> `__slots__` allow us to explicitly declare data members (like
> properties) and deny the creation of `__dict__` and `__weakref__`.
>
> **The space saved over using `__dict__` can be significant. Attribute
> lookup speed can be significantly improved as well.**

> **`__slots__` reserves space for the declared variables and prevents
> the automatic creation of `__dict__` and `__weakref__` for each
> instance.**

> Without a `__dict__` variable, instances cannot be assigned new
> variables not listed in the `__slots__` definition.

> `__slots__` are implemented at the class level by creating
> **descriptors** for each variable name.

`dataclasses` (https://docs.python.org/3/library/dataclasses.html):

> **A field is defined as a class variable that has a type annotation.**

> `slots`: If true ... `__slots__` attribute will be generated

`typing.TypedDict` (https://docs.python.org/3/library/typing.html):

> **TypedDict declares a dictionary type that expects all of its
> instances to have a certain set of keys, where each key is associated
> with a value of a consistent type.** This expectation is not checked
> at runtime but is only enforced by type checkers.

**Inference (carried).** Python's per-object key-value map exists only
because the field set is not declared. The moment it is declared —
`__slots__` — CPython replaces the map with descriptors over fixed
offsets, and the docs advertise both the space and the speed win. And
`__slots__` was not enough on its own: `dataclasses` and `NamedTuple`
add the *types* the slot declaration lacks. The trajectory is dict →
declared names → declared names + declared types. `TypedDict` is the
same trajectory applied to a value that stayed a dict for interchange
reasons.

### 5.4 Clojure: `defrecord`, and `s/keys` versus `s/map-of`

clojure.org/reference/datatypes, "Why have both deftype and
defrecord?":

> It has always been an unfortunate characteristic of using classes for
> application domain information that it resulted in information being
> hidden behind class-specific micro-languages, e.g. even the seemingly
> harmless `employee.getName()` is a custom interface to data. ... You
> can no longer take a generic approach to information processing.
>
> **This is why Clojure has always encouraged putting such information
> in maps, and that advice doesn't change with datatypes. By using
> `defrecord` you get generically manipulable information, plus the
> added benefits of type-driven polymorphism, and the structural
> efficiencies of fields.**

and on what `defrecord` supplies over `deftype`:

> **`defrecord` provides a complete implementation of a persistent
> map**, including: value-based equality and hashCode; metadata support;
> associative support; keyword accessors for fields; **extensible fields
> (you can assoc keys not supplied with the defrecord definition)**

A record also gets a *distinct textual notation* from a plain map:

> `defrecord` supports an additional reader form of
> `#my.record{:a 1, :b 2}` ... existing defrecord fields take the keyed
> values; defrecord fields without keyed values in the literal map are
> initialized to nil; **additional keyed values are allowed and added to
> the defrecord**

clojure.spec (https://clojure.org/guides/spec) then needed **two
separate primitives** for the two uses. For the record use:

> **Rather than define attribute (key+value) specifications in the scope
> of the entity (the map), specs assign meaning to individual
> attributes, then collect them into maps using set semantics (on the
> keys).**

> Entity maps in spec are defined with `keys`:
> `(s/def :acct/person (s/keys :req [:acct/first-name :acct/last-name :acct/email] :opt [:acct/phone]))`
> ... **The map spec never specifies the value spec for the attributes,
> only what attributes are required or optional.**

For the dictionary use:

> **In addition to the support for information maps via `keys`, spec
> also provides `map-of` for maps with homogenous key and value
> predicates.**
> `(s/def :game/scores (s/map-of string? int?))`
>
> By default `map-of` will validate but not conform keys **because
> conformed keys might create key duplicates that would cause entries in
> the map to be overridden.**

**Inference (carried).** Two independent confirmations in the
maps-maximalist language. `defrecord` was added because the record use
wanted "the structural efficiencies of fields" and "type-driven
polymorphism". And clojure.spec, the schema layer, could not describe
maps with one construct: it needed `keys` (fixed field set, per-key
value types) and `map-of` (open key domain, uniform value type) as
separate primitives. That is the record/dictionary distinction,
discovered from below, by the people most committed to not making it.

**Note (carried).** clojure.org still says of `defrecord` field type
hints: "a type hint of a non-primitive type will **not** be used to
constrain the field type nor the constructor arg ... **constraining the
field type and constructor arg is planned**."

---

## 6. Routing, string tables and feature flags

### 6.1 Routing tables are not maps

Go `net/http.ServeMux` (https://pkg.go.dev/net/http):

> ServeMux is an HTTP request multiplexer. **It matches the URL of each
> incoming request against a list of registered patterns and calls the
> handler for the pattern that most closely matches the URL.**

> **Precedence** — If two or more patterns match a request, then the
> most specific pattern takes precedence. **A pattern P1 is more
> specific than P2 if P1 matches a strict subset of P2's requests** ...
> **If a pattern passed to ServeMux.Handle or ServeMux.HandleFunc
> conflicts with another pattern that is already registered, those
> functions panic.**

The pre-1.22 wording (https://pkg.go.dev/net/http@go1.21.0) is the
syntactic version of the same rule:

> **Longer patterns take precedence over shorter ones**

RFC 1812 §2.2.5.1 and §5.2.4.3:

> By definition, CIDR comprises three elements: ... **consistent
> forwarding algorithm ("longest match").**

> **Conceptually, any route lookup algorithm starts out with a set of
> candidate routes that consists of the entire contents of the FIB. The
> algorithm consists of a series of steps that discard routes from the
> set. These steps are referred to as Pruning Rules.**

> **(2) Longest Match** — Longest Match is a refinement of Basic Match
> ... the algorithm examines the remaining routes to determine which
> among them have the largest `route.length` values. All except these
> are discarded.

- **Keys**: not keys at all — *patterns*, each denoting a **set** of
  requests or addresses, and the sets **overlap**.
- **Value type**: uniform (a handler, a next hop). This is the one axis
  where a routing table is genuinely map-like.
- **Order**: a **precedence** order, computed from the pattern's
  specificity, not from where the entry sits in the table.
- **Uniqueness**: of the pattern text, yes — Go *panics* on a
  conflicting registration. Of the *match*, emphatically no; breaking
  that tie is the structure's whole job.
- **Text or index**: index, over rules that live in code or in routing
  protocol state.

**Inference (carried).** If a routing table were a map, RFC 1812's
rules 2, 3 and 4 would not exist. What makes these not maps is that
keys denote overlapping *sets* rather than points, so there is no total
function from key to value.

### 6.2 Internationalization string tables

This is the cleanest genuine dictionary the survey found.

GNU gettext manual §3.1
(https://www.gnu.org/software/gettext/manual/gettext.html; the
per-node pages returned HTTP 403 to the subflow, which used the
single-page manual):

> **A PO file is made up of many entries, each entry holding the
> relation between an original untranslated string and its
> corresponding translation.**

```
#: lib/error.c:116
msgid "Unknown system error"
msgstr "Error desconegut del sistema"
```

§3.6, on uniqueness:

> **For a PO file to be valid, no two entries without `msgctxt` may have
> the same `untranslated-string` or `untranslated-string-singular`.**

§10:

> **the GNU gettext tools give an error when they encounter duplicate
> `msgid`s in the same file and in the same domain.** To merge
> duplicates, the `msguniq` program can be used.

§11.2, on where the key comes from:

> The main point about this solution is that it does not follow the
> method of normal file handling ... and that it does not burden the
> programmer with so many tasks, especially the unique key handling. **Of
> course here also a unique key is needed, but this key is the message
> itself (how long or short it is).**

And §11.3, the compiled MO format — the index that gettext builds from
the text:

> Then, at offset O and offset T in the picture, **two tables of string
> descriptors** can be found. In both tables, **each string descriptor
> uses two 32 bits integers, one for the string length, another for the
> offset of the string in the MO file** ... **The first table contains
> descriptors for the original strings, and is sorted so the original
> strings are in increasing lexicographical order. The second table
> contains descriptors for the translated strings, and is parallel to
> the first table.**
>
> **Having the original strings sorted enables the use of simple binary
> search.**

Contexts are folded into the key rather than modelled:

> **Contexts are stored by storing the concatenation of the context, a
> EOT byte, and the original string, instead of the original string.**

Fluent's normative grammar
(https://github.com/projectfluent/fluent/blob/master/spec/fluent.ebnf)
is a flat list of entries:

```
Resource  ::= (Entry | blank_block | Junk)*
Entry     ::= (Message line_end) | (Term line_end) | CommentLine
Message   ::= Identifier blank_inline? "=" blank_inline? ((Pattern Attribute*) | (Attribute+))
```

- **Keys**: open-ended data, minted wherever a developer writes a
  string. gettext's key *is the English source string*; Fluent's is an
  identifier. No schema can enumerate them.
- **Value type**: **uniform** — every value is a string, or in Fluent a
  Pattern.
- **Order**: irrelevant. PO order tracks source-scan order for the
  translator's convenience; `--sort-output` reorders at will; MO
  discards PO order and re-sorts lexicographically. The one exception is
  the reserved empty-`msgid` header entry, which "should be the first
  entry of the file."
- **Uniqueness**: essential and enforced.
- **Text or index**: **both, as two different artifacts with a compiler
  between them.** PO is the human-edited, order-preserving,
  comment-carrying text. MO is two parallel sorted arrays of
  (length, offset) pairs plus an optional hash table.

**Inference (carried).** Precisely because the i18n string table is a
*real* dictionary, gettext gives it a **dedicated line-oriented format
that is not a general key-value notation**: `msgid`/`msgstr` line pairs
separated by blank lines, with comment lines carrying provenance
(`#:` source references), workflow state (`#, fuzzy`) and translator
notes. Note what the text format carries that a bare map cannot:
per-entry metadata.

### 6.3 Feature flags

OpenFeature has **two** maps in one API, and they behave differently.

The flag store (https://openfeature.dev/specification/glossary,
`.../sections/flag-evaluation`):

> **Flag** — Flags represent a single pivot point of logic. **Flags have
> a type**, like string, boolean, json, etc.

> **The client MUST provide methods for typed flag evaluation, including
> boolean, numeric, string, and structure, with parameters flag key
> (string, required), default value (boolean | number | string |
> structure, required)**

The evaluation context (https://openfeature.dev/specification/sections/evaluation-context):

> The context might contain information about the end-user, the
> application, the host, or **any other ambient data that might be
> useful in flag evaluation**.

> **Requirement 3.1.2** — The evaluation context MUST support the
> inclusion of **custom fields, having keys of type string, and values
> of type `boolean | string | number | datetime | structure`.**

> **Requirement 3.1.4** — **The evaluation context fields MUST have a
> unique key.**

> **Requirement 3.2.3** — **Evaluation context MUST be merged in the
> order: API (global; lowest precedence) -> transaction -> client ->
> invocation -> before hooks (highest precedence), with duplicate values
> being overwritten.**

**Inference (carried).** The flag store is a heterogeneous map the type
system cannot see into, and OpenFeature's response is to make *every
read site* declare the expected type and a same-typed fallback — a
per-key type discipline pushed entirely onto the caller. The evaluation
context is a truer open map, and its openness is load-bearing for a
specific reason: the *consumer* of those attributes, the targeting
rules, is authored in a different system after the application ships.
Its keys are open because **the schema lives on the other side of a
deployment boundary**. That is a pattern worth naming: an open-ended
map often marks a place where the schema is *elsewhere*, not a place
where there is no schema.

---

## 7. Attribute-value facts: EAV, RDF, LDAP, OpenTelemetry

The prior report settles what a Datomic datom is. This section is about
the wider pattern: modelling an entity as a bag of (attribute, value)
facts because the attribute set is not knowable in advance.

### 7.1 EAV in the medical-informatics literature

Nadkarni, Marenco, Chen, Skoufos, Shepherd, Miller, "Organization of
Heterogeneous Scientific Data Using the EAV/CR Representation",
*J Am Med Inform Assoc.* 6(6):478–493, 1999
(https://pmc.ncbi.nlm.nih.gov/articles/PMC61391/):

> **Entity-attribute-value (EAV) representation is a means of organizing
> highly heterogeneous data using a relatively simple physical database
> schema.**

The lineage, which names most of this report's other sections:

> **Historically, attribute-value (A-V) pairs were first used in
> artificial intelligence applications in the form of LISP association
> lists. Attribute-value pairs are the basis of Web cookies, the
> Microsoft Windows Registry, and various tagged data interchange
> formats such as ASN.1.**

The definition, against the conventional design:

> **Conventional design** is defined ... as one in which **each parameter
> of interest is represented in a separate column in a table.**
>
> **An EAV design, in contrast, conceptually involves a table with three
> columns** — a column for entity/object identification (ID), one for
> attribute/parameter ..., and one for the value for the attribute. **The
> table has one row for each A-V pair.**

And the crucial concession — the logical schema does not go away:

> **EAV representation is primarily a means of simplifying the physical
> schema of a database** ... **However, regardless of the database's
> physical storage, its users naturally regard the data as
> conventionally structured — that is, segregated into tables and
> columns. Furthermore, external programs used for graphical
> presentation or data analysis always expect to receive data as one
> column per attribute.**

> **An EAV system must record the logical schema through metadata** —
> "dictionary" tables whose contents describe the rest of the system.
> **Well-designed metadata are critical to the proper functioning of an
> EAV system.**

The stated advantages are precisely the conditions under which the
pattern is legitimate:

> - **Flexibility.** There are no arbitrary limits on the number of
>   attributes per entity. The number of parameters can grow as the
>   database evolves, without schema redesign.
> - **Space-efficient storage for highly sparse data.** In an EPRS,
>   while thousands of parameters are applicable, only a few dozen
>   parameters are actually recorded for a typical patient.

and the stated drawbacks include the boundary:

> **Most production "EAV" databases also use conventional tables when it
> makes sense to do so. That is, their schema is heterogeneous.**

> **For schemas that are relatively static or simple (e.g., databases
> for business applications, such as inventory or accounting), the
> overhead of EAV design exceeds its advantages.**

The single most relevant passage in the whole survey is EAV/CR's
treatment of the per-key value type:

> **EAV/CR representation uses strong data typing, that is, when an
> attribute is defined, its data type is defined as well, and there is a
> separate EAV table for each data type.** (Many EPRSs, in contrast,
> store all data, even numbers and dates, as short strings.)

> **Seven data-type-specific tables record, respectively, integers,
> reals, short string, long string, date/time, binary (to handle
> BLOBS), and object IDs.**

The companion paper, Nadkarni and Brandt, "Data Extraction and Ad Hoc
Query of an Entity—Attribute—Value Database", *JAMIA* 5(6):511–527,
1998 (https://pmc.ncbi.nlm.nih.gov/articles/PMC61332/), gives the
reason again, independently:

> Some EPRSs use a single EAV table to store all values as strings ...
> **This is because ASCII strings representing numbers have a different
> sort order from true numbers (i.e., an index on the value field is
> essentially useless).**

> **Relational databases permit strong typing of columns in conventional
> tables** ... **Such power should not be discarded in the EAV context by
> converting data to least-common-denominator string form if the only
> expected benefit is simplification of the task of programming storage
> management.**

and the condition under which EAV is warranted:

> **Here, the nature and number of facts that will be stored for a given
> entity (the patient) cannot be predicted in advance — they depend on a
> particular patient's ailment. The problem of numerous and varying
> attributes per entity appears to be unique to databases that reflect
> rapidly evolving or highly heterogeneous domains.**

- **Keys**: open-ended, but **registered** — attributes live in a
  controlled-vocabulary metadata table. They are data rows, not schema
  columns, yet still declared before use.
- **Value type**: **per key, and declared**, with storage physically
  partitioned by type.
- **Order**: none; it is a relation.
- **Uniqueness**: **not essential.** EAV rows are time-stamped facts;
  the same (entity, attribute) pair recurs, and EAV/CR adds
  multi-instance attributes explicitly.
- **Text or index**: relational storage, not a text notation.

### 7.2 RDF

RDF 1.1 Concepts and Abstract Syntax
(https://www.w3.org/TR/rdf11-concepts/):

> **3. RDF Graphs — An RDF graph is a set of RDF triples.**

> **The predicate itself is an IRI and denotes a property, that is, a
> resource that can be thought of as a binary relation.** (Relations that
> involve more than two entities can only be indirectly expressed in
> RDF.)

> **Since RDF graphs are defined as mathematical sets, adding or
> removing triples from an RDF graph yields a different RDF graph.**

Nothing prevents `(s, p, o₁)` and `(s, p, o₂)` from both being in a
graph.

**Inference (carried).** RDF is not a map type and never was. It is a
set of triples, and the map reading — "subject as a record whose fields
are predicates" — is a derived view, valid only when a predicate
happens to be functional for that subject, which RDF does not guarantee
and OWL has to state separately as `owl:FunctionalProperty`. Same for
EAV. **The archetypal "everything is key-value" data models are
actually relations, and a map is the special case you get only by
adding a functional-dependency constraint the model itself does not
carry.**

### 7.3 LDAP: the same pattern, with a schema over it

RFC 4512 §2.2 (https://www.rfc-editor.org/rfc/rfc4512.txt, fetched by
me):

> An entry consists of **a set of attributes** that hold information
> about the object that the entry represents.

> **An attribute is an attribute description (a type and zero or more
> options) with one or more associated values.**

> **The attribute type governs whether the attribute can have multiple
> values, the syntax and matching rules used to construct and compare
> values of that attribute**, and other functions.

> **No two values of an attribute may be equivalent.**

and §2.4:

> Each object class identifies the set of attributes **required** to be
> present in entries belonging to the class and the set of attributes
> **allowed** to be present in entries of the class.

So: the value at a key is a **set**, not a single value; the value type
is **declared per attribute type**, with its own syntax and matching
rules; and object classes constitute a **schema of required and allowed
attributes** over the whole thing. This is a directory model that is
entirely a schema-first record system wearing key-value clothes.

### 7.4 OpenTelemetry: an open attribute map that reinvented schemas

OTLP `common.proto`
(https://github.com/open-telemetry/opentelemetry-proto/blob/main/opentelemetry/proto/common/v1/common.proto,
fetched by me) — note this is a modern, schema-first wire protocol that
needed open-ended attributes and **declined protobuf's own `map<K,V>`**:

```proto
message KeyValueList {
  // A collection of key/value pairs of key-value pairs. The list may be empty
  //
  // The keys MUST be unique (it is not allowed to have more than one
  // value with the same key).
  // The behavior of software that receives duplicated keys can be unpredictable.
  repeated KeyValue values = 1;
}

message KeyValue {
  string key = 1;
  AnyValue value = 2;
  int32 key_strindex = 3;   // Reference to the string key in ProfilesDictionary.string_table.
}
```

with the comment on `KeyValueList` explaining why:

> We need KeyValueList as a message since `oneof` in AnyValue does not
> allow repeated fields. **Everywhere else where we need a list of
> KeyValue messages (e.g. in Span) we use `repeated KeyValue` directly
> to avoid unnecessary extra wrapping (which slows down the protocol).
> The 2 approaches are semantically equivalent.**

The specification then supplies, in prose, every invariant the type
cannot carry
(https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/README.md):

> **An `Attribute` is a key-value pair, which MUST have the following
> properties:** The attribute key MUST be a non-`null` and non-empty
> string. ... The attribute value MUST be one of types defined in
> AnyValue.

> **Implementation MUST by default enforce that the exported attribute
> collections contain only unique keys.**

> **Collection of attributes are equal when they contain the same
> attributes, irrespective of the order in which those elements appear
> (unordered collection equality).**

> Note that they are distinct from `map<string, AnyValue>`, which is a
> type of AnyValue used to represent nested data structures.

The keys are then governed by a registry with the discipline of schema
field names
(https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/naming.md):

> **Use namespacing. Delimit the namespaces using a dot character.**

> **Two attributes, two metrics, or two events MUST NOT share the same
> name.**

> **Attributes, metrics, and events SHOULD NOT be removed from semantic
> conventions regardless of their maturity level. When the convention is
> renamed or no longer recommended, it SHOULD be deprecated.**

> it is recommended to prefix the new name by your company's reverse
> domain name, e.g. `com.acme.shopname`

And finally, the project had to invent schemas and schema migration
for its key space
(https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/schemas/README.md):

> Telemetry sources such as instrumented applications and consumers of
> telemetry such as observability backends sometimes make implicit
> assumptions about the emitted telemetry. **They assume that the
> telemetry will contain certain attributes or otherwise have a certain
> shape and composition of data (this is referred to as "telemetry
> schema" throughout this document).**

> For example **changing the name of an attribute of a span created by an
> instrumentation library can break the backend if the backend expects
> to find that attribute by its name.**

**Inference.** OpenTelemetry is the survey's clearest case of the whole
arc in one system: it needed genuinely open-ended attributes, it chose
a **vector of two-field structs** on the wire, it wrote uniqueness and
unordered equality into prose because the vector type cannot carry
them, it interned the keys into a string table for the one signal where
volume mattered, it governed the key space with a namespaced registry
and a no-reuse rule, and it then built a schema and a rename-migration
mechanism because the keys turned out to be field names after all.

---

## 8. Extension and annotation mechanisms in strictly typed protocols

This is a use the brief did not name and that the survey found
everywhere: **key-value as the escape hatch a strictly typed format
opens for data whose type the reader may not know.** Every instance
found is a *vector of structs with a designated key field* — never a
map — and in each the entry has more than two fields.

### 8.1 TLS 1.3

RFC 8446 §4.2 (https://www.rfc-editor.org/rfc/rfc8446.txt, fetched by
me):

> A number of TLS messages contain tag-length-value encoded extensions
> structures.

```
struct {
    ExtensionType extension_type;
    opaque extension_data<0..2^16-1>;
} Extension;
```

carried in every message as `Extension extensions<8..2^16-1>;` — a
vector. The key space is a registry:

> The list of extension types is maintained by IANA as described in
> Section 11.

And the two invariants are stated in prose, because the vector type
cannot carry them:

> **extensions MAY appear in any order, with the exception of
> "pre_shared_key" (Section 4.2.11) which MUST be the last extension in
> the ClientHello** (but can appear anywhere in the ServerHello
> extensions block). **There MUST NOT be more than one extension of the
> same type in a given extension block.**

Note the value type: `opaque extension_data` whose interpretation
depends on `extension_type`. That is a *dependent union keyed by the
tag* — a vector of variants, written as a vector of pairs because TLS's
presentation language has no open sum type.

### 8.2 X.509 certificate extensions

RFC 5280 §4.1 and §4.2 (https://www.rfc-editor.org/rfc/rfc5280.txt,
fetched by me):

```asn1
Extensions  ::=  SEQUENCE SIZE (1..MAX) OF Extension

Extension  ::=  SEQUENCE  {
     extnID      OBJECT IDENTIFIER,
     critical    BOOLEAN DEFAULT FALSE,
     extnValue   OCTET STRING
                 -- contains the DER encoding of an ASN.1 value
                 -- corresponding to the extension type identified
                 -- by extnID
     }
```

> **A certificate MUST NOT include more than one instance of a
> particular extension.**

> A certificate-using system MUST reject the certificate if it
> encounters a critical extension it does not recognize.

The entry is a **three-field struct** — key, criticality, value — which
a map type cannot express at all. And the value is again a
tag-dependent union: "the DER encoding of an ASN.1 value corresponding
to the extension type identified by extnID."

### 8.3 HTTP/2 header compression

Covered in §1.2. The static table is a vector of two-field structs
addressed by ordinal, containing duplicate names as separate entries,
and the header list is "an ordered collection ... [that] can contain
duplicate header fields."

### 8.4 Protocol Buffers' own escape hatches

google/protobuf well-known types
(https://protobuf.dev/reference/protobuf/google.protobuf/):

> **Struct** represents a structured data value, consisting of fields
> which map to dynamically typed values. — field `fields`,
> `map<string, Value>`. The JSON representation for `Struct` is JSON
> object.

> **Value** represents a dynamically typed value which can be either
> null, a number, a string, a boolean, a recursive struct value, or a
> list of values.

> **Any** contains an arbitrary serialized message along with a URL that
> describes the type of the serialized message.

**Inference.** Protobuf offers *two* escape hatches, and they answer
different questions. `Any` is for "a value whose schema exists but
which this message does not name" — a type URL plus bytes. `Struct` is
for "a value with no schema at all" — a recursive string→dynamic map
that is JSON in protobuf clothing. The map appears only in the second,
and it is explicitly the untyped case.

### 8.5 The OCI image configuration

Covered in §1.7 and §1.8. Three shapes in one document: `Env` is an
array of `VARNAME=VARVALUE` strings; `ExposedPorts` is a set encoded as
a map to unit, with the spec apologizing for it; `Labels` is a genuine
open string→string map governed by a namespaced key registry whose
pre-defined keys each carry their own value type in prose.

### 8.6 What the extension mechanisms show

Across TLS, X.509, HPACK, OTLP and OCI, the same shape recurs:

- The **key space is a registry** — IANA extension types, OIDs,
  namespaced attribute names, reverse-DNS label prefixes. Open-ended in
  the type system, governed in practice.
- The **entry is a struct with more than two fields** in two of five
  (X.509's `critical`, OTLP's `key_strindex`), which forecloses a map
  type outright.
- The **value is a tag-dependent union**, not a uniform type: what
  `extnValue` or `extension_data` means depends on the key.
- The **carrier is a vector**, and **uniqueness and unorderedness are
  written in prose** because the vector cannot carry them.
- The reason the type is not a record is always the same: the writer
  and the reader are **different programs on different release cycles**,
  and the reader must forward or ignore what it does not know
  ("Consumers MUST NOT generate an error if they encounter an unknown
  annotation key"; "A proxy MUST forward unrecognized header fields").

---

## 9. What schema-first designers did about a map type

The prior report covers Dhall, protobuf's `map<K,V>` desugaring,
Cap'n Proto's 2014 mailing-list position, CUE and Nix, YAML's tag grid,
JSON, TOML, CBOR, MessagePack and XML. This section is new ground and
is about the **rationale**.

### 9.1 FlatBuffers — no map type, and the reason stated outright

The complete `type` production of the schema grammar
(https://flatbuffers.dev/grammar/):

```
type = `bool` | `byte` | `ubyte` | `short` | `ushort` | `int` | `uint` |
       `float` | `long` | `ulong` | `double` | `int8` | `uint8` | `int16` |
       `uint16` | `int32` | `uint32` | `int64` | `uint64` | `float32` |
       `float64` | `string` | `[` type `]` | ident
```

No map. What it offers instead
(https://flatbuffers.dev/schema/):

> `key` (on a field): this field is meant to be used as a key when
> sorting a vector of the type of table it sits in. **Can be used for
> in-place binary search.**

and the rationale, under "Guidelines → Efficiency":

> **It is very common nowadays to represent any kind of data as
> dictionaries (as in e.g. JSON), because of its flexibility and
> extensibility. While it is possible to emulate this in FlatBuffers (as
> a vector of tables with key and value(s)), this is a bad match for a
> strongly typed system like FlatBuffers, leading to relatively large
> binaries. FlatBuffer tables are more flexible than classes/structs in
> most systems, since having a large number of fields only few of which
> are actually used is still efficient. You should thus try to organize
> your data as much as possible such that you can use tables where you
> might be tempted to use a dictionary.**
>
> **Similarly, strings as values should only be used when they are truly
> open-ended. If you can, always use an enum instead.**

The mechanism (https://flatbuffers.dev/languages/cpp/), under a heading
that names the use:

> **Storing maps / dictionaries in a FlatBuffer** — FlatBuffers doesn't
> support maps natively, but there is support to emulate their behavior
> with vectors and binary search, which means you can have fast lookups
> directly from a FlatBuffer without having to unpack your data into a
> `std::map` or similar.
>
> - Designate one of the fields in a table as they "key" field ...
>   **You may only have one key field, and it must be of string or
>   scalar type.**
> - Instead of `CreateVector`, call `CreateVectorOfSortedTables` ...
> - you can use `Vector::LookupByKey` instead of just `Vector::Get`
>
> **`LookupByKey` only works if the vector has been sorted, it will
> likely not find elements if it hasn't been sorted.**

**Inference (carried).** FlatBuffers' argument is that in a strongly
typed system the dictionary's flexibility is *already* provided by the
record, because absent fields are cheap. The dictionary is needed only
when the key set is genuinely unbounded, and then a sorted vector of a
declared element type serves.

### 9.2 Cap'n Proto — the map is the documentation's own example of a generic

The built-in types (https://capnproto.org/language.html, fetched by me)
are Void, Bool, the sized integers, Float32/64, Text, Data and
`List(T)`. There is no map. And the schema language's canonical
illustration of generics is the map, defined as a list of two-field
structs:

> **Generic Types** — A struct or interface type may be parameterized,
> making it "generic". For example, this is useful for defining
> type-safe containers:
>
> ```capnp
> struct Map(Key, Value) {
>   entries @0 :List(Entry);
>   struct Entry {
>     key @0 :Key;
>     value @1 :Value;
>   }
> }
>
> struct People {
>   byName @0 :Map(Text, Person);
>   # Maps names to Person instances.
> }
> ```

The same definition reappears in the backwards-compatibility section as
an example of a safe schema evolution.

### 9.3 ASN.1 — no map, and a four-cell grid instead

ITU-T X.680 (02/2021), fetched as PDF and text-extracted by the
subflow. The complete `BuiltinType` production:

> `BuiltinType ::= BitStringType | BooleanType | CharacterStringType |
> ChoiceType | DateType | DateTimeType | DurationType | EmbeddedPDVType |
> EnumeratedType | ExternalType | InstanceOfType | IntegerType | IRIType |
> NullType | ObjectClassFieldType | ObjectIdentifierType | OctetStringType |
> RealType | RelativeIRIType | RelativeOIDType | SequenceType |
> SequenceOfType | SetType | SetOfType | PrefixedType | TimeType |
> TimeOfDayType`

The subflow searched the whole 866 KB text layer: the word "map" occurs
six times, always as a verb or in "bit map", never as a type.

The definitions clause:

> **3.8.68 sequence-of types**: Types defined by referencing a single
> component type; each value in the sequence-of type is an **ordered
> list** of zero, one or more values of the component type.
>
> **3.8.72 set types**: Types defined by referencing a **fixed,
> unordered, list of types** (some of which may be declared to be
> optional); each value in the set type is an unordered list of values,
> one from each component type.
>
> **3.8.73 set-of types**: Types defined by referencing a single
> component type; each value in the set-of type is an **unordered list**
> of zero, one or more values of the component type.

and clause 28.3's three notes:

> NOTE 1 – Semantic significance should not be placed on the order of
> these values.
> NOTE 2 – Encoding rules are not required to preserve the order of
> these values.
> NOTE 3 – **The set-of type is not a mathematical set of values, thus,
> as an example, for `SET OF INTEGER` the values `{ 1 }` and `{ 1 1 }`
> are distinct.**

with clause 27.6 on `SET`:

> There shall be no semantics associated with the order of values in a
> set type.

**Inference (carried).** ASN.1's constructed types are exactly the
{ordered, unordered} × {heterogeneous-fixed, homogeneous-repeated}
cross-product, plus CHOICE. A map would be a fifth cell — unordered,
homogeneous, *keyed*. The grid is the design.

### 9.4 Nickel — a dictionary *type* over the same values as a record

Nickel user manual, typing chapter
(https://nickel-lang.org/user-manual/typing; the subflow cross-checked
it against `doc/manual/typing.md` in the repo):

> **Record**: `{field1: T1, .., fieldn: Tn}`. A record whose field names
> are known statically as `field1`, .., `fieldn`, respectively of type
> `T1`, .., `Tn`.
>
> **Dictionary**: `{_: T}`. A record whose field names are statically
> unknown but are all of the type `T`.

and the two are related by subtyping, not separated:

> **Record/Dictionary subtyping**: `{ field1 : T1, ..., fieldn : Tn } <:
> { _ : T }` if for each `i`, `Ti <: T`. That is, a record type is a
> subtype of a dictionary type if the type of each field is a subtype of
> the type of dictionary elements.

The rationale from the contracts side (`doc/manual/contracts.md`):

> The type constructor `{_ : Contract}` represents a record whose field
> names are not constrained but whose field values must satisfy
> `Contract`. ... **Such a contract is useful when using records as an
> extensible dictionary, that is a key/value store, where keys are
> strings and values satisfy `Contract`**

**Inference (carried).** Nickel did **not** introduce a second *value*
kind. Record and dictionary are two *types over the same values*,
related by subtyping. The distinction is entirely in the schema, not in
the notation: `{a = 1, b = 3}` is one syntactic form, and whether it is
a record or a dictionary is decided by the type ascribed to it.

**Note (carried, unverified).** No Tweag blog post giving a standalone
rationale for the split was found; the repo's `RATIONALE.md` discusses
language choice, not the dictionary type.

### 9.5 Pkl

Apple's Pkl (2024) has both, and its `Mapping` is defined as a
*sequence*. From the stdlib page
(https://pkl-lang.org/package-docs/pkl/current/base/Mapping.html,
fetched by me through WebFetch's extraction):

> **An object containing an ordered sequence of key-value pairs.**

> This class is the object equivalent of `Map`.

and from the language reference, on the two object kinds:

> **A Typed object has a fixed structure described by a class
> definition. When a typed object is amended, its properties can be
> overridden or amended, but new properties cannot be added.**

> A value of type `Mapping` is an ordered collection of values indexed
> by key.

### 9.6 Unison

The built-in types
(https://www.unison-lang.org/docs/language-reference/built-in-types/)
are `Nat`, `Int`, `Float`, `Boolean`, `Bytes`, `Text`, `Char` and `()`.
`Map` is absent; it is an ordinary library type in `base`, with no
literal syntax
(https://www.unison-lang.org/docs/fundamentals/values-and-functions/common-collection-types/):

> **Currently Unison does not have special `Map` construction syntax** so
> one easy way to create a multi-item map is from a `List` of tuples
> `Map.fromList [(1, "a"), (2, "b"), (3, "c")]`

**Note (carried, unverified).** No Unison design writing on why maps are
not primitive was found.

### 9.7 Rust's serde — the axis that everything turns on

serde's data model (https://serde.rs/data-model.html):

> The Serde data model is the API by which data structures and data
> formats interact. You can think of it as Serde's type system.

> **seq** — A variably sized heterogeneous sequence of values, for
> example `Vec<T>` or `HashSet<T>`. When serializing, the length may or
> may not be known before iterating through all the data. **When
> deserializing, the length is determined by looking at the serialized
> data.**
>
> **tuple** — A statically sized heterogeneous sequence of values **for
> which the length will be known at deserialization time without looking
> at the serialized data**, for example `(u8,)` or
> `(String, u64, Vec<T>)` or `[u64; 10]`.
>
> **map** — A variably sized heterogeneous key-value pairing, for
> example `BTreeMap<K, V>`. When serializing, the length may or may not
> be known before iterating through all the entries. **When
> deserializing, the length is determined by looking at the serialized
> data.**
>
> **struct** — A statically sized heterogeneous key-value pairing **in
> which the keys are compile-time constant strings and will be known at
> deserialization time without looking at the serialized data**, for
> example `struct S { r: u8, g: u8, b: u8 }`.

Both `map` and `struct` are called *heterogeneous*. The axis that
separates them — and identically `seq` from `tuple` — is **whether the
shape is known without looking at the serialized data.**

The same axis appears in the trait signatures
(https://docs.rs/serde/latest/serde/trait.Serializer.html):

```rust
fn serialize_map(self, len: Option<usize>) -> ...;
fn serialize_struct(self, name: &'static str, len: usize) -> ...;
```

> Begin to serialize a map. ... The argument is the number of elements
> in the map, **which may or may not be computable before the map is
> iterated.**

And the payoff, from serde's own annotated reference serializer
(https://serde.rs/impl-serializer.html):

```rust
// Structs look just like maps in JSON. In particular, JSON requires that we
// serialize the field names of the struct. Other formats may be able to
// omit the field names when serializing structs because the corresponding
// Deserialize implementation is required to know what the keys are without
// looking at the serialized data.
```

with the self-describing distinction spelled out
(https://docs.rs/serde/latest/serde/trait.Deserializer.html):

> **Self-describing data formats like JSON are able to look at the
> serialized data and tell what it represents.** For example the JSON
> deserializer may see an opening curly brace (`{`) and know that it is
> seeing a map. ...
>
> **Non-self-describing formats like Postcard need to be told what is in
> the input in order to deserialize it.** The `deserialize_*` methods are
> hints to the deserializer for how to interpret the next piece of
> input.

Finally, the key-type restriction is the *format's*, not the model's.
serde_json interposes a dedicated `MapKeySerializer` on every key whose
associated types are all `Impossible`, and whose errors read:

> `KeyMustBeAString` => "key must be a string"
> `ExpectedNumericKey` => "invalid value: expected key to be a number in quotes"
> `FloatKeyMustBeFinite` => "float key must be finite (got NaN or +/-inf)"

**Inference (carried).** This is the whole payoff of the map/struct
split for a schema-driven notation. Because `struct` is a *distinct
data-model type* from `map`, a format is free to drop the field names
entirely. If `struct` had merely been sugar for `map`, no format could
safely do so. The distinction exists precisely so that a schema-aware
format can be compact where a schema-less one cannot.

### 9.8 Avro — a genuine map, and the price stated in the spec

Avro specification
(https://avro.apache.org/docs/1.12.0/specification/):

> Avro supports six kinds of complex types: records, enums, arrays,
> maps, unions and fixed.

> Maps use the type name "map" and support one attribute:
> - `values`: the schema of the map's values.
>
> **Map keys are assumed to be strings.**

> Maps are encoded as a series of blocks. ... **The blocked
> representation permits one to read and write maps larger than can be
> buffered in memory, since one can start writing items without knowing
> the full length of the map.**

> Unions may not contain more than one schema with the same type, except
> for the named types record, fixed and enum. For example, unions
> containing two array types or two map types are not permitted.

And, from the "Sort Order" section, the price:

> Avro defines a standard sort order for data. This permits data written
> by one system to be efficiently sorted by another system. **This can be
> an important optimization, as sort order comparisons are sometimes the
> most frequent per-object operation.**

> **map data may not be compared. It is an error to attempt to compare
> data containing maps unless those maps are in an `"order":"ignore"`
> record field.**

Every other type gets an ordering rule — null, boolean, the numbers,
bytes, string, array ("compared lexicographically by element"), enum by
symbol position, union by branch, record lexicographically by field.
Map is the sole exception.

**Inference (carried).** Avro is a schema-first system that *did*
include a homogeneous map, and its own specification then had to carve
a hole in its total-order definition to accommodate it. Including the
map cost Avro the property that any two values of the same schema are
comparable. That is a concrete, spec-visible price, stated by the
designers themselves.

### 9.9 Thrift — a map because every target language has one

Thrift IDL grammar (https://thrift.apache.org/docs/idl):

```
[26] ContainerType  ::=  MapType | SetType | ListType
[27] MapType        ::=  'map' CppType? '<' FieldType ',' FieldType '>'
```

Thrift types page (https://thrift.apache.org/docs/types), which states
it "supersedes the information in the Thrift Whitepaper":

> - `list`: An ordered list of elements.
> - `set`: An unordered set of unique elements.
> - `map<type1,type2>`: **A map of strictly unique keys to values.**

> **N.B.: For maximal compatibility, the key type for map should be a
> basic type rather than a struct or container type. There are some
> languages which do not support more complex key types in their native
> map types. In addition the JSON protocol only supports key types that
> are base types.**

And the rationale, from Slee, Agarwal and Kwiatkowski, "Thrift: Scalable
Cross-Language Services Implementation", Facebook, 2007
(https://thrift.apache.org/static/files/thrift-20070401.pdf; the
subflow extracted the PDF text layer itself and **restored dropped
`fi`/`fl` ligatures and removed kerning-inserted intra-word spaces**;
words and order are the paper's):

> §2.1 — The type system rests upon a few base types. In considering
> which types to support, **we aimed for clarity and simplicity over
> abundance, focusing on the key types available in all programming
> languages, ommitting any niche types available only in specific
> languages.**

> §2.3 — Thrift containers are strongly typed containers that **map to
> the most commonly used containers in common programming languages.**
> ... `list<type>` ... **May contain duplicates.** ... `set<type>` An
> unordered set of unique elements. ... `map<type1,type2>` **A map of
> strictly unique keys to values.**

(The misspelling "ommitting" is the paper's.)

**Inference (carried).** Thrift's inclusion criterion is explicitly
*cross-language availability*, not type-system fit. FlatBuffers asks
"what does a strongly typed wire format want?" and answers "not a
dictionary". Thrift asks "what do all target languages already have?"
and answers "a map". Which question a notation is asking determines the
answer.

### 9.10 Arrow and Parquet — the map defined as a list of structs

Apache Arrow's `format/Schema.fbs`
(https://github.com/apache/arrow/blob/main/format/Schema.fbs, fetched
by me):

> **A Map is a logical nested type that is represented as**
>
> ```text
> List<entries: Struct<key: K, value: V>>
> ```
>
> In this layout, the keys and values are each respectively contiguous.
> **We do not constrain the key and value types, so the application is
> responsible for ensuring that the keys are hashable and unique.**
> Whether the keys are sorted may be set in the metadata for this field.

> Neither the "entries" field nor the "key" field may be nullable.

> **The metadata is structured so that Arrow systems without special
> handling for Map can make Map an alias for List.** The "layout"
> attribute for the Map field must have the same contents as a List.

```
table Map {
  /// Set to true if the keys within each value are sorted
  keysSorted: bool;
}
```

Apache Parquet's `LogicalTypes.md`
(https://github.com/apache/parquet-format/blob/master/LogicalTypes.md,
fetched by me):

> `MAP` is used to annotate types that should be interpreted as a map
> from keys to values. **`MAP` must annotate a 3-level structure:**
>
> ```
> <map-repetition> group <name> (MAP) {
>   repeated group key_value {
>     required <key-type> key;
>     <value-repetition> <value-type> value;
>   }
> }
> ```

> The `value` field ... can be `required`, `optional`, or omitted. ...
> **If not present, it can be represented as a map with all null values
> or as a set of keys.**

> **If there are multiple key-value pairs for the same key, then the
> final value for that key must be the last value.** Other values may be
> ignored or may be added with replacement to the map container in the
> order that they are encoded. **The `MAP` annotation should not be used
> to encode multi-maps using duplicate keys.**

**Inference.** In the two dominant columnar formats the map type *is* a
vector of two-field structs, plus an annotation and a `keysSorted`
flag. Arrow states outright that the uniqueness invariant is delegated
to the application, and that a system with no map support may treat it
as a plain List. Parquet states outright that the value half may be
omitted, in which case the same construct is a set. These are the two
clearest existing instances of exactly the design the brief asks about:
a vector of two-field structs whose *type* is declared a map.

### 9.11 GraphQL — no map, with a recorded rejection

The GraphQL specification (https://spec.graphql.org/October2021/) §3.4
lists six named type kinds — scalar, object, interface, union, enum,
input object — plus List and Non-Null wrappers. No map. The word "Map"
appears only as a required *serialization* primitive for responses
(§7.2), and the response map's order is normatively fixed by the query
(§7.2.2):

> Since the result of evaluating a selection set is ordered, the
> serialized Map of results should preserve this order by writing the
> map entries in the same order as those fields were requested.

> For example, if the request was `{ name, age }`, a GraphQL service
> responding in JSON should respond with `{ "name": "Mark", "age": 30 }`
> and should not respond with `{ "age": 30, "name": "Mark" }`.

**Mark: GitHub issue, not the specification.** graphql/graphql-spec
issue #101, "Map type", opened 2015-10-03, 79 comments, locked. Lee
Byron (GraphQL co-creator), 2016-01-09:

> **There are significant tradeoffs to a Map type vs a list of key/value
> pairs. One issue is paginating over the collection. Lists of values
> can have clear pagination rules while Maps which often have
> non-ordered key-value pairs are much more difficult to paginate.**
>
> **Another issue is usage. Most often Map is used within APIs where one
> field of the value is being indexed, which is in my opinion is an API
> anti-pattern as indexing is an issue of storage and an issue of client
> caching but not an issue of transport.** This anti-pattern concerns me.

with the sanctioned alternative given verbatim:

> Second is returning a list of tuples. This may be the right path if you
> don't know up front which you want, or if you specifically want them
> all.
> ```
> item {
>   titles {
>     language
>     text
>   }
> }
> ```

and Ivan Goncharov, spec maintainer, 2018-05-10, naming the structural
obstacle:

> I personaly think that this feature shouldn't brake current assumption
> that **shape of query should match shape of result**. ... I think it's
> one of the most critical parts of this proposal.

Byron locking the thread, 2019-09-16:

> I'm going to lock this issue since it has become non-actionable. For
> anyone arriving here looking for a Map type, I suggest first reading
> the comments on this thread about the API design tradeoffs and
> alternative approaches available.

### 9.12 XML Schema, RELAX NG, Kaitai Struct, Bencode

XML Schema 1.1 §3.8.1
(https://www.w3.org/TR/xmlschema11-1/):

> `{compositor}` One of {all, choice, sequence}.

The subflow searched all 814 KB: "dictionary" occurs zero times, and
every occurrence of "map" is a verb. `xs:all` is the closest analogue,
and it is a record with unordered fields — the same choice ASN.1 made
with `SET`. RELAX NG's pattern inventory
(https://relaxng.org/spec-20011203.html) is `choice`, `group`, `empty`,
`text`, `oneOrMore`, `interleave`, `element`, `attribute`, `data`,
`value`, `list`. No map.

Kaitai Struct's data model (https://doc.kaitai.io/user_guide.html) is
sequences of typed attributes, computed instances, enums and
user-defined types; every occurrence of "map" in the guide refers to
YAML mappings in the `.ksy` *source* syntax, never to a parsed data
type.

Bencode, BitTorrent BEP 3 (https://www.bittorrent.org/beps/bep_0003.html),
is the schema-less counter-example that pays the other price:

> Dictionaries are encoded as a 'd' followed by a list of alternating
> keys and their corresponding values followed by an 'e'. ... **Keys must
> be strings and appear in sorted order (sorted as raw strings, not
> alphanumerics).**

and the reason, downstream, under `info_hash`:

> The info-hash must be the hash of the encoded form as found in the
> .torrent file, which is identical to bdecoding the metainfo file,
> extracting the info dictionary and encoding it **if and only if the
> bdecoder fully validated the input (e.g. key ordering, absence of
> leading zeros).**

### 9.13 The three positions, in the designers' own words

**Exclude — the map is a bad fit for a typed wire format.**
FlatBuffers: "this is a bad match for a strongly typed system like
FlatBuffers, leading to relatively large binaries," with the positive
claim that a record with cheap absent fields already covers the
flexibility.

**Exclude — the map breaks a structural invariant.** GraphQL: it breaks
pagination, it breaks "the assumption that shape of query should match
shape of result", and its common use is an anti-pattern because
"indexing is an issue of storage ... but not an issue of transport."

**Include — because every target language has one.** Thrift: "focusing
on the key types available in all programming languages, ommitting any
niche types available only in specific languages."

And two systems record what including it cost, in their own specs:
Avro had to write "map data may not be compared", punching a hole in
its standard total order for the map alone; Thrift had to concede that
the declared key type does not survive contact with target languages or
its own JSON protocol.

**Inference (carried).** FlatBuffers, GraphQL and serde independently
identify one and the same property under three names: FlatBuffers'
"bad match for a strongly typed system", GraphQL's "shape of query
should match shape of result", and serde's "known at deserialization
time without looking at the serialized data". A map is the one
construct where the schema cannot predict the value's shape, because
the keys live in the data.

---

## 10. Kubernetes: a schema-first system that forbade maps of subobjects

This is the closest thing the survey found to a system that put the
brief's exact question to itself and answered it in writing.

The Kubernetes API conventions
(https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md),
section "Lists of named subobjects preferred over maps":

> Discussed in #2004 and elsewhere. **There are no maps of subobjects in
> any API objects. Instead, the convention is to use a list of subobjects
> containing name fields.**
>
> For example:
> ```yaml
> ports:
>   - name: www
>     containerPort: 80
> ```
> vs.
> ```yaml
> ports:
>   www:
>     containerPort: 80
> ```
>
> **This rule maintains the invariant that all JSON/YAML keys are fields
> in API objects. The only exceptions are pure maps in the API
> (currently, labels, selectors, annotations, data), as opposed to sets
> of subobjects.**

The referenced issue is kubernetes/kubernetes #2004, "Document why we
don't use maps in the API in api-conventions.md", opened by Brian Grant
on 2014-10-27 and closed on 2014-10-31. Grant opened it *proposing to
switch to maps*, and his own statement of the obstacle is:

> **Automatically translating maps into lists of named objects appears
> to be hard. In JSON and YAML, structures and maps cannot be
> distinguished without a schema.**

Joe Beda's reply the same day is the reader's argument:

> **The crux of this problem is that it isn't clear to the user what
> "left hand side strings" are "magic keywords" in the config
> system/API vs. which are user data.**

> While B is obviously shorter than A, I think it is more confusing for
> the novice user. When copy/pasting examples or reading unfamiliar
> configs, **the novice user won't know what `www` is. Is this a magic
> value that they aren't supposed to change (like `ports`) or is it an
> input/naming thing that they should change?**

and, on putting the name back inside the entry:

> Questions users'll be asking: **why is `www` there twice? What happens
> if I change one but not the other?**

His earlier statement of the same point, in issue #853
(comment 51851041, 2014-08-11):

> Even though the second one is shorter, **to the novice user it looks
> like `ports` and `www` are both magic system keywords when actually
> `www` is just a user provided token.**

and the schema argument:

> There are other things we want to avoid here -- significantly, **each
> key should have one and only one form for what it accepts -- this
> let's us have a strongly typed schema instead of forcing us to
> interpret the yaml parse tree with custom code.**

Grant abandoned the proposal four days later:

> Abandoning this idea. Converting it to a doc bug to document the
> reason for the way the API is.

The one cost of the decision was named months later, and it is the
cost that matters for this survey:

> **@ghodss has pointed out that lists do not allow generic merging for
> configuration updates.**

That cost was eventually paid off by **declaring the list's key in the
schema**. Kubernetes server-side apply
(https://github.com/kubernetes/website/blob/main/content/en/docs/reference/using-api/server-side-apply.md),
"Merge strategy":

> `//+listType` / `x-kubernetes-list-type` / `atomic`/`set`/`map` —
> Applicable to lists. **`set` applies to lists that include only scalar
> elements. These elements must be unique. `map` applies to lists of
> nested types only. The key values (see `listMapKey`) must be unique in
> the list.** `atomic` can apply to any list. If configured as `atomic`,
> the entire list is replaced during merge. At any point in time, a
> single manager owns the list. **If `set` or `map`, different managers
> can manage entries separately.**

> `//+listMapKey` / `x-kubernetes-list-map-keys` / List of field names,
> e.g. `["port", "protocol"]` — **Only applicable when `+listType=map`.
> A list of field names whose values uniquely identify entries in the
> list.** ... The key fields must be scalars.

> `//+mapType` / `x-kubernetes-map-type` / `atomic`/`granular` —
> Applicable to maps.
> `//+structType` / `x-kubernetes-map-type` — **Applicable to structs;
> otherwise same usage and OpenAPI annotation as `//+mapType`.**

**Inference.** Kubernetes is the survey's single most direct
precedent. It (a) banned maps of subobjects from a schema-driven
notation, (b) stated the reason as a *reader* problem — a map-shaped
text gives schema-fixed names and open-ended data the same syntactic
slot — (c) enumerated the four places where a genuine map survives:
labels, selectors, annotations, data, (d) discovered one real cost,
per-entry merging, and (e) paid it off by *declaring in the schema*
that a given vector of structs is a map, and which of the struct's own
fields are its key. The key is not a separate slot; it is one or more
of the entry's own fields, named by the schema.

---

## 11. Classification

The brief asks for four buckets: **(a)** a record with a fixed schema
wearing map clothing, which a positional struct expresses; **(b)** a
genuine map, keys open-ended data, one value type; **(c)** an index or
cache over data that lives elsewhere; **(d)** a set.

The survey found a fifth shape that none of the four fits, and
reporting it as one of the four would misreport it, so it is named
here as **(e)**: structures that are called maps but are not
functions from key to value at all — ordered multimaps, precedence
tables, and sets of facts.

### 11.1 The table

| Use | Class | Why |
|---|---|---|
| POSIX-named environment variables (`PATH`, `HOME`, `LC_*`) | **a** | key set fixed by a standard, per-key grammar hidden in a uniform string |
| The lowercase application environment namespace | **b** | keys reserved for applications, value uniformly a byte string |
| An HTTP header section | **e** | repeats legal and order-significant among equal names; an ordered multimap |
| A Structured Fields Dictionary | **a** | "specifying the allowed type(s) for individual members by their keys"; ordered; indexable by position |
| A TOML table used as `[server] port = 80` | **a** | keys are field names; value type per key |
| A TOML table used as `[dependencies] serde = "1.0"` | **b** | keys are package names; one value type |
| A JSON object under `properties`/OpenAPI Fixed Fields | **a** | the schema enumerates the names |
| A JSON object under `additionalProperties`/`Map[string,X]` | **b** | the schema gives a key type, one value type, and a cardinality |
| A JSON object under `patternProperties` (OpenAPI Paths, Responses) | **b** | key grammar declared, key set not enumerable |
| INI, `.properties`, `.env`, systemd settings | **a** | the program's documentation names the keys; value uniformly string |
| Kubernetes labels, selectors, annotations; Docker/OCI labels and annotations | **b** | keys minted by third parties, governed by a namespace grammar; value uniformly string |
| A query string / `application/x-www-form-urlencoded` | **e** | specified as "a list of tuples"; duplicates first-class, order observable |
| LevelDB, RocksDB, Berkeley DB, FoundationDB, etcd, Bigtable | **c** | sorted storage engines; the key is a struct flattened to make it sortable |
| The Redis keyspace | **c** | with a schema hand-encoded into the key string (`object-type:id:field`) |
| A Redis hash | **a** | the docs call it a "record type" used to "represent basic objects" |
| memcached | **c** | the purest cache: contents derived, disposable by specification |
| A DynamoDB table | **a** | an item is "a group of attributes"; the key is a designated subset of the item's own fields |
| The git object database | **c** | key is a function of the value; the index carries no information the values lack |
| A git tree object | **b**, expressed as a sorted vector of four-field structs | name→object is a genuine map; the format is a vector, and `fsck` re-imposes uniqueness and order |
| git refs / `packed-refs` | **b**, serialized as one line per entry | open-ended names, one uniform value type |
| The Nix store directory | **c** | key derived from value ⊕ name ⊕ store location |
| A Nix `.drv` `env` field | **b**, serialized as a sorted vector of pairs | schema says `additionalProperties: {type: string}` |
| IPLD maps under DAG-CBOR / DAG-JSON | **b**, forcibly canonicalized | string keys mandated, total key order mandated, uniqueness borrowed from CBOR |
| A POSIX directory | **b** in shape, **c** in medium | open-ended names, one uniform value; never serialized ("The internal format of directories is unspecified") |
| DNS | **e** | composite key `(name, class, type)`; the value at a key is a *set*; RDATA is a tag-discriminated union |
| A compiler symbol table | **c** | rebuilt from source every compile; never in the output |
| An interner / string table | **c** | and its serialized forms (ELF `.symtab`, JVM constant pool, LLVM bitcode v2) are vectors of fixed-shape records with offsets |
| A cache or memo table | **c** | derived and disposable by specification |
| `Counter`, histograms, frequency tables | **b** | keys are observed values, one uniform count type |
| A sparse array as DOK | **c** | a build structure; SciPy's own docs say convert to parallel arrays for computation |
| `HashSet`, `map[K]struct{}`, `ExposedPorts`, Parquet MAP with the value omitted | **d** | "there is no value"; a set is nothing but a uniqueness constraint |
| Graph adjacency as dict-of-dicts | **c** | NetworkX states the structure is replaceable; Boost implements the same interface over vectors and a matrix |
| Edge attribute dictionaries | **a** | `{'color': 'red', 'weight': 0.84}` — per-key types |
| V8 HiddenClasses, Self maps | **c**, over data that is really **a** | the runtime's whole strategy is to discover the struct hiding in the object |
| A JavaScript object used as a record | **a** | and it is the only half of the pair with a text syntax |
| A JavaScript `Map` | **b** | and it has "no native support for serialization or parsing" |
| A Lua table as a record (`a.name`) | **a** | the manual gives the record use its own sugar |
| Python `__dict__` | **a**, undeclared | `__slots__`, dataclasses and `NamedTuple` are the same record, declared |
| `TypedDict` | **a** | "expects all of its instances to have a certain set of keys, where each key is associated with a value of a consistent type" |
| Clojure `s/keys` | **a** | fixed `:req`/`:opt` key set, per-key value specs |
| Clojure `s/map-of`, `defrecord` extra keys | **b** | "maps with homogenous key and value predicates" |
| HTTP routing tables, IP FIBs | **e** | patterns denote overlapping *sets*; precedence, not lookup |
| gettext PO, Fluent FTL | **b** | the cleanest genuine dictionary found: open keys, one value type, order irrelevant, uniqueness enforced |
| gettext MO | **c** | two parallel sorted arrays of (length, offset) plus an optional hash table |
| An OpenFeature flag store | **a** with the types pushed to the call site | "Flags have a type", asserted per read with a same-typed default |
| An OpenFeature evaluation context | **b** | open because the schema lives on the other side of a deployment boundary |
| EAV / EAV-CR | **e** | a relation of time-stamped facts; `(entity, attribute)` recurs; uniqueness not required |
| RDF | **e** | "an RDF graph is a set of RDF triples"; a predicate is "a binary relation", not a function |
| An LDAP entry | **a** | object classes declare required and allowed attributes; each attribute type declares its own syntax; the value is a *set* |
| OpenTelemetry attribute collections | **b** with a registry-governed key space | carried on the wire as `repeated KeyValue`, with uniqueness and unordered equality in prose |
| TLS extensions, X.509 extensions, HPACK's static table, protobuf `Any` | **e** | a vector of tag-dependent *variants*; the entry has three fields in X.509 and OTLP |
| protobuf `Struct` | **b** with no value type at all | the explicitly schema-less escape hatch: `map<string, Value>` |
| OCI `Env` | **b**, flattened into `VARNAME=VARVALUE` strings | |
| Avro `map`, Thrift `map<K,V>`, Nickel `{_ : T}`, Arrow `Map`, Parquet `MAP`, Pkl `Mapping`, Cap'n Proto `Map(K,V)`, Dhall `Map` | **b** | genuine homogeneous map *types* — and six of the eight are defined as a vector of two-field structs |

### 11.2 What the classification comes to

**(a) dominates configuration and dominates languages.** Every use in
the survey where the keys are program vocabulary — environment
variables a program reads, INI settings, TOML `[server]` tables, JSON
objects under `properties`, Redis hashes, DynamoDB items, JS objects,
Python `__dict__`, Clojure `s/keys`, LDAP entries, edge attribute
dicts — is a record whose field set the notation declined to declare.
And in every single language case the ecosystem later shipped a
declaration mechanism to recover what the map threw away: `__slots__`
then dataclasses then `TypedDict`; `defrecord` then `s/keys`;
`maplike<DOMString, object>` in Web IDL; `x-kubernetes-map-type` on
`//+structType`; OpenTelemetry's telemetry schemas. **The record is
always rediscovered.**

**(b) is real, and it is narrow.** The genuine maps the survey found
share a profile that is much tighter than "key-value":

- keys are minted outside any schema the reader holds — a translator's
  source string, a user's label, a third party's annotation, a package
  name, a filename, a ref name, an attribute an unknown vendor adds;
- **the value type is uniform**, and where it is not, the thing turns
  out to be (a) or (e) on inspection;
- order carries nothing;
- uniqueness is required, and in most cases enforced from outside the
  format;
- and the reason the keys are open is usually specific and nameable:
  the key set is authored by a *different party on a different release
  cycle* than the reader.

The subflow on dynamic object systems put the discriminator plainly,
and the whole survey supports it: **the axis that separates (a) from
(b) is value-type uniformity, not key openness.** Both share open keys
in practice; only (b) has one value type.

**(c) is the largest bucket by count and the least relevant to a
notation.** Storage engines, symbol tables, interners, caches, hidden
classes, adjacency structures, sparse-matrix build structures, the git
object store, the Nix store, gettext's MO file, DNS's server-side
tree. Not one of them serializes its map as text. Where these systems
*do* serialize, they emit a vector of records with offsets or names —
ELF, the JVM constant pool, LLVM bitcode v2, COO triples, MO's parallel
arrays, packed-refs lines, zone-file lines, V7 directory entries.

**(d) is uniformly a workaround.** Where a language has a set type, the
map-to-unit lives in the implementation. Where it does not, it leaks
into serialized data, and specifications apologize for it when it does
(the OCI note on `ExposedPorts`). Parquet reads the same construct back
the other way: omit the value half and "it can be represented ... as a
set of keys".

**(e) is the trap.** Five of the most frequently cited "key-value"
things in computing are not maps: HTTP header sections, query strings,
routing tables, RDF, and EAV. Each is called a map in casual speech and
each fails the defining property — HTTP and urlencoded permit
duplicates and order matters; routing keys denote overlapping sets so
there is no total function; RDF's predicate is stated in the spec to be
"a binary relation"; EAV rows are time-stamped facts about the same
`(entity, attribute)` pair. The map reading of each requires adding a
functional-dependency constraint the model does not carry.

---

## 12. What is lost, for the (b) uses, if a genuine map is written as a vector of two-field structs whose type is declared a map

The question already grants the decisive half: **the type says "map".**
That places uniqueness, unorderedness, the key type, the value type and
the lookup operation in the type, where §10 of the prior report
established they need to live. What remains at issue is only what the
*text* carries. Six things were found, and the evidence on each is
uneven.

### 12.1 Almost nothing, on the evidence — six production formats already do this

This is not a hypothetical design. Six schema-first formats define
their map *exactly* this way:

- **Apache Arrow**: "A Map is a logical nested type that is represented
  as `List<entries: Struct<key: K, value: V>>`", with `keysSorted` as a
  flag.
- **Apache Parquet**: "`MAP` is used to annotate types that should be
  interpreted as a map from keys to values. `MAP` must annotate a
  3-level structure", the middle level being `repeated group key_value`.
- **Protocol Buffers**: `map<K,V>` desugars normatively to
  `repeated MapFieldEntry`, and "Any protocol buffers implementation
  that supports maps must both produce and accept data that can be
  accepted by the earlier definition."
- **Dhall**: `Map = λ(k) → λ(v) → List { mapKey : k, mapValue : v }`.
- **Cap'n Proto**: the map is the language reference's own worked
  example of a generic, `struct Map(Key, Value) { entries @0 :List(Entry); ... }`.
- **FlatBuffers**: a sorted vector of tables with a designated `key`
  field, plus `LookupByKey`.

And Kubernetes, which forbade map-shaped subobjects outright, later
added exactly the missing declaration —
`x-kubernetes-list-type: map` plus `x-kubernetes-list-map-keys` — so
that a vector of structs *is* a map to the schema, with per-entry
ownership restored.

### 12.2 The uniqueness invariant slips from the type to the application, unless the reader enforces it

This is the one loss the sources actually demonstrate, and it is a loss
of *discipline*, not of expressiveness. Arrow, having defined Map as a
List of Structs, has to write:

> **we do not constrain the key and value types, so the application is
> responsible for ensuring that the keys are hashable and unique**

and Parquet, having done the same, has to publish a tie-break rule:

> **If there are multiple key-value pairs for the same key, then the
> final value for that key must be the last value.** ... The `MAP`
> annotation should not be used to encode multi-maps using duplicate
> keys.

OpenTelemetry, which carries attributes as `repeated KeyValue`, states
the invariant three times in prose — in the `.proto` comment ("The keys
MUST be unique ... The behavior of software that receives duplicated
keys can be unpredictable"), in the specification ("Implementation MUST
by default enforce that the exported attribute collections contain only
unique keys"), and in the equality rule ("unordered collection
equality") — because the wire type cannot carry any of it. TLS 1.3
does the same for its extension vector ("There MUST NOT be more than
one extension of the same type in a given extension block"), as does
X.509 ("A certificate MUST NOT include more than one instance of a
particular extension"), as does git (`duplicateEntries` is an `fsck`
ERROR, and `git mktree` will happily emit a tree that violates it).

**Inference.** The pattern is exact: when the carrier is a vector, the
uniqueness rule migrates into prose and into a separate validator. That
is a loss only if the notation's reader does not enforce it. A reader
that walks a declared map type can reject a duplicate at read time,
which none of these formats' readers do — that is why they all had to
write the rule down.

### 12.3 The reader loses a syntactic signal that order does not matter

YAML states the convention as a rule: "**In every case where node order
is significant, a sequence must be used.**" A vector delimiter, in
every notation surveyed, signals ordered. A map delimiter signals
unordered. Writing an unordered thing inside an ordered delimiter
inverts the signal, and the type is the only thing correcting it.

Two witnesses on each side. Against the vector: the living's own
question, logged in this flow's vision records — "**In the key map, the
order is not guaranteed, right?**" — treats unorderedness as the
delimiter's meaning, and the ruling that key-value delimiters suit
"**sections that could not have the same key**" treats uniqueness the
same way. For the vector: Joe Beda's Kubernetes argument runs the other
direction, that a map-shaped text *hides* which strings are data — "the
novice user won't know what `www` is. Is this a magic value that they
aren't supposed to change (like `ports`) or is it an input/naming thing
that they should change?" — and Brian Grant's "**In JSON and YAML,
structures and maps cannot be distinguished without a schema**" is the
same observation from the parser's side.

### 12.4 Text density: two delimiters and their spacing per entry

FlatBuffers' stated objection to emulating dictionaries — "leading to
relatively large binaries" — is a size argument, and it transfers to
text. A map written `« home ADDR  work ADDR »` becomes
`[ { home ADDR } { work ADDR } ]`: one extra delimiter pair and its
spacing per entry. For the (b) uses that are actually large — an i18n
catalogue of thousands of entries, a label set, a `.drv` environment of
thirty-three pairs — that is the dominant textual cost.

Counter-witness from the same corpus: none of the systems that write a
large real dictionary as text uses a nested map notation *either*.
gettext writes `msgid`/`msgstr` on separate lines with a blank line
between entries; DNS zone files are "predominantly line-oriented"; git
`packed-refs` is one line per entry; Nix `.drv` writes `("k","v")`
pairs in a list. When a dictionary gets big enough to matter, the
formats that serve it reach for a flat per-entry record layout, not for
nesting of either kind.

### 12.5 What a two-field entry cannot hold, and a struct can

This is the one place the vector form is strictly *more* capable, and
it matters because the real dictionaries in this survey keep needing a
third field:

- X.509's `Extension` is `(extnID, critical, extnValue)`.
- OTLP's `KeyValue` is `(key, value, key_strindex)`.
- A git tree entry is `(mode, type, hash, name)`.
- A DNS resource record is `(owner, type, class, TTL, RDATA)`.
- A gettext PO entry carries `#:` source references, `#,` flags,
  `#|` previous msgid and `msgctxt` beside `msgid`/`msgstr`.
- Kubernetes' `listMapKey` is a *list* of field names,
  e.g. `["port", "protocol"]` — a composite key drawn from the entry's
  own fields.

A map construct admits exactly two slots. A vector of structs admits as
many as the type declares, and the key is then one or more of the
entry's own fields rather than a separate slot — which is precisely the
design Kubernetes and DynamoDB both arrived at independently.

### 12.6 Key types: the vector loses nothing and the map often does

Every map construct in the survey that restricted its key type did so
because the *map* forced it: Avro "Map keys are assumed to be strings";
DAG-CBOR "map keys must be strings"; JSON and serde_json "key must be a
string"; FlatBuffers "must be of string or scalar type"; Thrift's N.B.
that complex key types do not survive; protobuf's forbidding of message
and enum keys in `map<K,V>` even though its own desugaring permits
them. A vector of structs carries whatever the key field's declared
type is, with no such restriction. EDN and YAML, the two notations that
do permit arbitrary keys, are also the two with no schema to lean on.

### 12.7 Summary of the losses

| Loss | Strength of evidence |
|---|---|
| Uniqueness slips into prose and a separate validator | **Strong.** Arrow, Parquet, protobuf, OTLP, TLS, X.509 and git all had to write the rule down. Avoidable only if the notation's reader enforces the declared map type at read time. |
| The reader loses the delimiter's signal that order is immaterial | **Moderate.** YAML states the convention normatively; the living's own words treat the delimiter that way. Countered by Beda and Grant, who argue the map delimiter hides which strings are data. |
| Two extra delimiters and their spacing per entry | **Moderate, and it is the real cost at scale.** FlatBuffers' size argument transfers. Countered by the fact that no large real dictionary is written in nested map syntax either. |
| A distinct lookup notation, if the notation had one | **Not applicable** — no source in either report shows a textual notation whose map syntax carries a lookup operation; lookup is always an API. |
| Nothing else found | Six production formats already define the map as a vector of two-field structs, and Kubernetes forbade the map form outright in a schema-driven notation. |

---

## 13. What could not be verified, and corrections to the brief

### Corrections to premises in the brief

- **RFC 2181 §5 contains no statement about ordering within an RRset.**
  The sentence "The order of RRs in a set is not significant, and need
  not be preserved by name servers, resolvers, or other parts of the
  DNS" is in **RFC 1034 §3.6**. The subflow grepped RFC 2181 for
  `order|sorted|unordered|sequence|significan` and found nothing on the
  subject.
- **Redis's documentation no longer says hashes are "perfect to
  represent objects".** The live text is "Redis hashes are record types
  modeled as collections of field-value pairs" and "You can use hashes
  to represent basic objects". The older wording is **unverified**.
- **`rustc-dev-guide.rust-lang.org/symbol.html` returns HTTP 404.** No
  such chapter exists in the current guide. Substituted the official
  rustdoc for `rustc_span::symbol` and the guide's own chapters.
- **`docs.memcached.org/about/` returns 404.** Used `memcached.org/about`
  and the protocol spec in the memcached repository.
- **Go's `net/http.ServeMux` no longer says "longer patterns take
  precedence".** Since Go 1.22 the rule is stated semantically: "A
  pattern P1 is more specific than P2 if P1 matches a strict subset of
  P2's requests." The pre-1.22 wording is preserved at
  `pkg.go.dev/net/http@go1.21.0` and is quoted from there.
- **etcd's own landing page still advertises the v2 model** ("Store data
  in hierarchically organized directories, as in a standard
  filesystem"), which the v3 API documentation explicitly repudiates.
  The subflow marks the landing page as stale copy; the v3 documents are
  quoted.

### Not verified

- **ECMA-404.** Both editions' PDFs downloaded (HTTP 200) but their body
  text could not be extracted — no `pdftotext` or `pypdf` in the
  subflow's environment, subset fonts defeated raw stream
  decompression, and WebFetch returned "COULD NOT READ". **Nothing is
  quoted from it.**
- **The Dragon Book §2.7.** `dragonbook.stanford.edu` fails TLS
  certificate validation and search returned only paraphrases and
  pirated scans. The subflow **refused to quote it from memory** and
  substituted Wirth's *Compiler Construction*, author-hosted at ETH
  Zürich.
- **POSIX `readdir` ordering.** No POSIX text was found declaring the
  order unspecified. POSIX calls a directory stream "an ordered
  sequence" and never constrains which order. Stated here as an
  omission, not as a quoted guarantee.
- **Git's tree-entry sort rule.** Observed empirically on this machine
  (a blob `lib.txt` sorts before a subtree `lib`), consistent with the
  well-known "sort as if the name had `/` appended", but git ships no
  `gitformat-tree(5)` and no document stating the rule was found.
- **V7 Unix directory entry size.** `DIRSIZ 14` and the two-field struct
  are witnessed in the V7 source; the arithmetic to 16 bytes is the
  subflow's, from PDP-11 word size, not a quoted number.
- **Duplicate map keys in DAG-CBOR and DAG-JSON.** Zero occurrences of
  "duplicat" in either spec. Uniqueness comes from RFC 8949's data
  model, which DAG-CBOR adopts normatively via §4.2.
- **DNSSEC canonical RR ordering.** RFC 4034 was not fetched; no claim
  is made.
- **A TC39 rationale for adding `Map`.** The archived ES wiki strawman
  is executable spec only, with no rationale prose. MDN's sentence
  ("because there were no built-in alternatives, Object has been used as
  Map historically") is the best-sourced statement found, and it is
  MDN's, not TC39's.
- **Fluent's duplicate-identifier behaviour.** `spec/valid.md` contains
  no statement about unique message identifiers and the EBNF does not
  constrain it. No normative rule was found either way.
- **A Tweag rationale for Nickel's record/dictionary split.** The
  repository's `RATIONALE.md` discusses language choice, not the
  dictionary type. No blog post giving a standalone rationale was found.
- **Unison design writing on why maps are not primitive.** None found.
- **An ASN.1 design-rationale document** explaining the absence of a map
  type. X.680 is a normative notation, not a design document.
- **Berkeley DB duplicate-key support.** The 1999 paper contains no
  statement and the Oracle reference manual 404'd; no claim either way.
- **Redis top-level keyspace ordering.** No positive statement was found
  that it is unordered; the subflow inferred it from the absence of any
  ordering contract, and marks it as inference.
- **LLVM's `VALUE_SYMTAB_BLOCK` record layout.** The official bitcode
  format document contains only an unwritten stub for that section.
- **graphql-spec PR #888**, referred to in a search result as a later
  map RFC, was not fetched; no claim is made about it.
- **The Kenton Varda comparison** at
  `capnproto.org/news/2014-06-17-capnproto-flatbuffers-sbe.html` was
  fetched and contains nothing about maps or dictionaries.
- **Terraform's `count` versus `for_each` guidance** was sought as a
  witness that positional indices cause spurious replacement when a list
  changes. The current documentation says only "Use the `count` argument
  when you want to create nearly identical instances. Use `for_each`
  when some instance arguments must have distinct values that can't be
  directly derived from an integer index." The sharper statement was
  **not found** and nothing is claimed from it.
- **Quotes taken through a summarizing fetch tool** rather than raw
  text: Postgres `hstore`, Pkl's language reference and `Mapping` page,
  the protobuf well-known types page, and the serde pages I fetched
  myself (the serde quotes were independently confirmed by a subflow
  reading the same pages, and agree). Treat these as accurate in
  substance; a publication would want them re-read raw.

### A negative finding worth stating

**No source in either report shows a textual notation whose map syntax
carries a lookup operation.** Lookup is always an API over a parsed
value, never something the notation writes. Whatever a distinct map
delimiter buys, it is not that.

---

## Sources

Fetched by me in this flow, from raw text or source files unless noted:

- RFC 7541, *HPACK: Header Compression for HTTP/2*, Peon & Ruellan, May 2015 — https://www.rfc-editor.org/rfc/rfc7541.txt
- RFC 8446, *The Transport Layer Security (TLS) Protocol Version 1.3*, Rescorla, August 2018 — https://www.rfc-editor.org/rfc/rfc8446.txt
- RFC 5280, *Internet X.509 Public Key Infrastructure Certificate and CRL Profile*, Cooper et al., May 2008 — https://www.rfc-editor.org/rfc/rfc5280.txt
- RFC 4512, *LDAP: Directory Information Models*, Zeilenga, June 2006 — https://www.rfc-editor.org/rfc/rfc4512.txt
- OpenTelemetry, `opentelemetry/proto/common/v1/common.proto` — https://github.com/open-telemetry/opentelemetry-proto/blob/main/opentelemetry/proto/common/v1/common.proto
- OpenTelemetry Specification, `specification/common/README.md` — https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/README.md
- OpenTelemetry Specification, `specification/schemas/README.md` (Telemetry Schemas) — https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/schemas/README.md
- OpenTelemetry Semantic Conventions, `docs/general/naming.md` — https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/naming.md
- OCI Image Specification, `config.md` and `annotations.md` — https://github.com/opencontainers/image-spec/blob/main/config.md, `.../annotations.md`
- Apache Arrow, `format/Schema.fbs` — https://github.com/apache/arrow/blob/main/format/Schema.fbs
- Apache Parquet, `LogicalTypes.md` — https://github.com/apache/parquet-format/blob/master/LogicalTypes.md
- Cap'n Proto language reference — https://capnproto.org/language.html
- Compose Specification, `05-services.md` — https://github.com/compose-spec/compose-spec/blob/main/05-services.md
- JSON Schema draft 2020-12, Core — https://json-schema.org/draft/2020-12/json-schema-core.html
- Kubernetes API conventions — https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md
- kubernetes/kubernetes issue #2004 and issue comment 51851041, via the GitHub API — https://github.com/kubernetes/kubernetes/issues/2004
- Kubernetes server-side apply documentation — https://github.com/kubernetes/website/blob/main/content/en/docs/reference/using-api/server-side-apply.md
- protobuf well-known types (via a summarizing fetch) — https://protobuf.dev/reference/protobuf/google.protobuf/
- PostgreSQL `hstore` (via a summarizing fetch) — https://www.postgresql.org/docs/current/hstore.html
- Pkl language reference and `Mapping` (via a summarizing fetch) — https://pkl-lang.org/main/current/language-reference/index.html, https://pkl-lang.org/package-docs/pkl/current/base/Mapping.html
- serde: data model, `impl-serializer`, `impl-deserializer` (via a summarizing fetch; independently confirmed by a subflow) — https://serde.rs/data-model.html and siblings
- `man git-fsck`, git 2.55.0, on this machine
- `Vision/datom.md` and `flows/ad19b1/vision/` in this repository, for the living's words and the datom map syntax

Fetched by the configuration and environment subflow:

- IEEE Std 1003.1-2024 (POSIX), XBD §8 Environment Variables, `<dirent.h>`, `readdir`, `scandir`, `ls` — https://pubs.opengroup.org/onlinepubs/9799919799/
- `environ(7)`, `ld.so(8)` — https://man7.org/linux/man-pages/
- RFC 9110, *HTTP Semantics*, §5 — https://www.rfc-editor.org/rfc/rfc9110.txt
- RFC 6265, *HTTP State Management Mechanism* — https://www.rfc-editor.org/rfc/rfc6265.txt
- RFC 9651 and RFC 8941, *Structured Field Values for HTTP* — https://www.rfc-editor.org/rfc/rfc9651.txt
- IANA HTTP Field Name Registry — https://www.iana.org/assignments/http-fields/field-names.csv
- TOML v1.0.0 — https://toml.io/en/v1.0.0
- YAML 1.2.2 — https://yaml.org/spec/1.2.2/
- RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange Format* — https://www.rfc-editor.org/rfc/rfc8259.txt
- JSON Schema draft 2020-12 Core and Validation; the official learning documentation — https://json-schema.org/
- OpenAPI Specification v3.1.0 — https://spec.openapis.org/oas/v3.1.0.html
- `java.util.Properties` javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Properties.html
- `GetPrivateProfileString` — https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getprivateprofilestring
- `systemd.syntax(7)` — https://manpages.debian.org/unstable/systemd/systemd.syntax.7.en.html
- Docker Compose environment variables — https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/
- XDG Base Directory Specification — https://specifications.freedesktop.org/basedir-spec/latest/
- The Twelve-Factor App, III. Config — https://12factor.net/config
- Kubernetes labels and annotations — https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/, `.../annotations/`
- Docker object labels — https://docs.docker.com/engine/manage-resources/labels/
- RFC 3986 §3.4; WHATWG URL Standard §5 — https://url.spec.whatwg.org/

Fetched by the key-value stores subflow:

- LevelDB README and `doc/index.md` — https://github.com/google/leveldb
- RocksDB README, RocksDB-Overview, Column-Families, Basic-Operations, Prefix-Seek — https://github.com/facebook/rocksdb/wiki
- Redis data types, hashes, keyspace — https://redis.io/docs/latest/
- memcached `doc/protocol.txt`; memcached.org and `/about` — https://github.com/memcached/memcached
- Amazon DynamoDB Developer Guide, "Core components" — https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html
- DeCandia et al., *Dynamo: Amazon's Highly Available Key-value Store*, SOSP 2007, author's version — https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html
- etcd data model, API, "Why etcd" — https://etcd.io/docs/v3.5/
- Chang et al., *Bigtable: A Distributed Storage System for Structured Data*, OSDI 2006, USENIX proceedings — https://www.usenix.org/legacy/event/osdi06/tech/chang/chang_html/index.html
- Olson, Bostic, Seltzer, *Berkeley DB*, USENIX 1999 — https://www.usenix.org/legacy/publications/library/proceedings/usenix99/full_papers/olson/olson_html/index.html
- FoundationDB data modeling and layer concept — https://apple.github.io/foundationdb/

Fetched by the naming and content-addressing subflow:

- `gitformat-loose(5)`, `gitglossary(7)`, `git-fsck(1)`, `git-mktree(1)`, `git-pack-refs(1)`, `gitrepository-layout(5)` — local man pages, git 2.55.0
- Pro Git ch. 10, "Git Internals — Git Objects" and "Git References" — https://git-scm.com/book/en/v2/
- Nix manual, "Store Path", "Complete Store Path Calculation", `derivation-aterm`, `derivation-v4.yaml` — local Nix 2.35.1 manual; https://nix.dev/manual/nix/
- IPLD data model kinds; DAG-CBOR spec; DAG-JSON spec — https://ipld.io/, https://github.com/ipld/ipld
- RFC 8949, *Concise Binary Object Representation (CBOR)* — https://www.rfc-editor.org/rfc/rfc8949.txt
- IEEE Std 1003.1-2024, §3.103–3.105, `<dirent.h>`, `readdir`, `scandir` — https://pubs.opengroup.org/onlinepubs/9799919799/
- V7 Unix `usr/man/man5/dir.5`, `usr/sys/h/dir.h`, `usr/sys/h/types.h` — https://github.com/dspinellis/unix-history-repo, tag `Research-V7`
- RFC 1034 and RFC 1035, *Domain Names* — https://www.rfc-editor.org/rfc/rfc1034.txt, `.../rfc1035.txt`
- RFC 2181, *Clarifications to the DNS Specification* — https://www.rfc-editor.org/rfc/rfc2181.txt

Fetched by the in-program subflow:

- Niklaus Wirth, *Compiler Construction*, §8.1 — https://people.inf.ethz.ch/wirth/CompilerConstruction/CompilerConstruction1.pdf
- LLVM Programmer's Manual; LLVM Bitcode File Format — https://llvm.org/docs/
- rustc dev guide, name resolution and the full-book render — https://rustc-dev-guide.rust-lang.org/
- `rustc_span::symbol` rustdoc — https://doc.rust-lang.org/nightly/nightly-rustc/rustc_span/symbol/
- ELF gABI ch. 4, symbol table and string table — https://refspecs.linuxfoundation.org/elf/gabi4+/
- *The Java Virtual Machine Specification*, Java SE 21, §4.1 and §4.4 — https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html
- Python `functools`, `collections`, `datamodel`, `dataclasses`, `typing` — https://docs.python.org/3/
- Guava `Cache` and `CacheBuilder` javadocs — https://guava.dev/releases/33.0.0-jre/api/docs/
- SciPy sparse: `dok_matrix`, `coo_matrix`, and the `sparse` overview — https://docs.scipy.org/doc/scipy/reference/
- Rust `std::collections::HashSet`; Java `HashSet` javadoc — https://doc.rust-lang.org/std/, https://docs.oracle.com/en/java/javase/21/docs/api/
- The Go blog, "Go maps in action"; the Go specification; `src/mime/mediatype.go` — https://go.dev/
- ISO C++ working draft, `[map.overview]`, `[set.overview]`, `[associative.reqmts.general]`, `[unord.req.general]` — https://eel.is/c++draft/
- CPython `Objects/setobject.c` — https://github.com/python/cpython
- NetworkX introduction and data structure — https://networkx.org/documentation/stable/reference/introduction.html
- Boost Graph Library, `adjacency_list` and `adjacency_matrix` — https://www.boost.org/doc/libs/1_84_0/libs/graph/doc/
- V8 blog, "Fast properties in V8" — https://v8.dev/blog/fast-properties
- Chambers, Ungar & Lee, *An Efficient Implementation of SELF*, LaSC 4(3), 1991 — https://bibliography.selflanguage.org/_static/implementation.pdf

Fetched by the dynamic-objects subflow:

- ECMA-262, §6.1.7, §10.1.11, §14.7.5.9, §24.1 — https://tc39.es/ecma262/
- MDN, `Map` — https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map
- Lua 5.4 Reference Manual, §2.1 and §6.1 — https://www.lua.org/manual/5.4/manual.html
- clojure.org, "Datatypes: deftype, defrecord and reify"; "spec Guide" — https://clojure.org/reference/datatypes, https://clojure.org/guides/spec
- Go `net/http.ServeMux`, current and `@go1.21.0` — https://pkg.go.dev/net/http
- RFC 1812, *Requirements for IP Version 4 Routers*, §2.2.5.1 and §5.2.4.3 — https://www.rfc-editor.org/rfc/rfc1812.txt
- GNU gettext manual, §3.1, §3.6, §10, §11.2, §11.3 — https://www.gnu.org/software/gettext/manual/gettext.html
- Project Fluent, `spec/fluent.ebnf` and the guide — https://github.com/projectfluent/fluent, https://projectfluent.org/fluent/guide/hello.html
- OpenFeature specification: flag evaluation, evaluation context, glossary, types — https://openfeature.dev/specification/
- Nadkarni et al., *Organization of Heterogeneous Scientific Data Using the EAV/CR Representation*, JAMIA 6(6), 1999 — https://pmc.ncbi.nlm.nih.gov/articles/PMC61391/
- Nadkarni & Brandt, *Data Extraction and Ad Hoc Query of an Entity—Attribute—Value Database*, JAMIA 5(6), 1998 — https://pmc.ncbi.nlm.nih.gov/articles/PMC61332/
- W3C, *RDF 1.1 Concepts and Abstract Syntax* — https://www.w3.org/TR/rdf11-concepts/

Fetched by the schema-first-designers subflow:

- FlatBuffers grammar, "Writing a Schema", C++ guide — https://flatbuffers.dev/
- ITU-T X.680 (02/2021), *Abstract Syntax Notation One: Specification of basic notation* — https://www.itu.int/rec/T-REC-X.680
- Nickel user manual, typing and contracts chapters — https://nickel-lang.org/user-manual/typing, https://github.com/tweag/nickel/blob/master/doc/manual/
- Unison built-in types and common collection types — https://www.unison-lang.org/docs/
- serde data model, `Serializer` and `Deserializer` rustdoc, `impl-serializer`; serde_json `src/error.rs` and `src/ser.rs` — https://serde.rs/, https://docs.rs/serde/, https://github.com/serde-rs/json
- Apache Avro specification 1.12.0 — https://avro.apache.org/docs/1.12.0/specification/
- Apache Thrift IDL and types; Slee, Agarwal & Kwiatkowski, *Thrift: Scalable Cross-Language Services Implementation*, Facebook 2007 — https://thrift.apache.org/docs/idl, `.../types`, https://thrift.apache.org/static/files/thrift-20070401.pdf
- GraphQL specification, October 2021, §3.4, §3.6, §7.2 — https://spec.graphql.org/October2021/
- graphql/graphql-spec issue #101, "Map type" — https://github.com/graphql/graphql-spec/issues/101
- W3C XML Schema Definition Language 1.1 Part 1, §3.8.1 — https://www.w3.org/TR/xmlschema11-1/
- RELAX NG Specification — https://relaxng.org/spec-20011203.html
- Kaitai Struct user guide — https://doc.kaitai.io/user_guide.html
- BitTorrent BEP 3 — https://www.bittorrent.org/beps/bep_0003.html
