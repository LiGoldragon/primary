# Spirit Record Privacy And Access Design

## Frame

The psyche asked for privacy built into Spirit without reducing the model to
`private: bool`. The durable intent was captured as Spirit records `1445`
and `1446`: Spirit records need a typed access/classification field, `Public`
is the default, and non-public records need more refined categories such as
personal and sensitive.

This is a design report, not an implementation change. No private personal
material was inspected.

## Current Spirit Shape

Production Spirit's record shape is still public by structure:

```text
Entry [Topic Kind Description Magnitude]
Observation [(Option Topic) (Option Kind) ObservationMode]
```

`spirit-next` currently has the same core shape in generated Rust:

```rust
pub struct Entry {
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub magnitude: Magnitude,
}

pub struct Query {
    pub topic_match: TopicMatch,
    pub kind: Option<Kind>,
}
```

Persona-spirit has ordinary, owner, and upgrade sockets. Those sockets are
authority/control surfaces. They do not yet label records, filter observation
by privacy, or prevent high-sensitivity records from being exported into
lower-sensitivity reports.

## Research Signal

NIST SP 800-60 is useful because it treats classification as a consequence
of information type and risk, not as a single private/public switch. For
Spirit, this means the record's content type and expected harm from
disclosure should determine the label.

NIST SP 800-122 is useful because personally identifiable or personal
information is context-sensitive. The right protection level depends on the
specific instance and inappropriate access, use, or disclosure risk.

NIST SP 800-162 is useful because the access decision should evaluate
attributes of subject, object, operation, and environment. For Spirit, the
record label is an object attribute; the caller role/socket, requested
operation, target output surface, and purpose are decision inputs.

Helen Nissenbaum's contextual integrity is the strongest privacy-theory fit.
It rejects the simple public/private dichotomy: privacy is about appropriate
information flow inside a context. Spirit's danger is context collapse: a
private counselor note getting observed by an implementation agent, quoted in
a public report, or mined into a public skill.

Daniel Solove's privacy taxonomy reinforces that Spirit must guard not only
collection but also processing and dissemination. The database can store a
private record correctly and still violate privacy later by summarizing,
searching, exporting, or training context from it in the wrong place.

## Recommended Model

Add an access/classification field to every Spirit entry. Keep it concrete
and ordinal for the first implementation:

```text
Access (Public Workspace Personal Sensitive Sealed)
Entry [Topic Kind Description Magnitude Access]
```

Suggested semantics:

- `Public` — ordinary workspace intent; safe for ordinary Spirit,
  public reports, repo `INTENT.md`, skills, and cross-agent search.
- `Workspace` — safe for trusted workspace agents, but not for public
  repository publication or broad external export.
- `Personal` — private personal-affairs material; visible only to the
  owning psyche and private assistant/counselor lanes.
- `Sensitive` — private material whose disclosure could cause meaningful
  harm or embarrassment; requires explicit owner-purpose approval for
  observation or summarization.
- `Sealed` — owner-only or envelope-only; ordinary queries can reveal at
  most that a sealed record exists, and perhaps not even topics.

This is intentionally a typed enum, not a boolean. It can later grow into a
record if the "yes" branch starts carrying data:

```text
Access (Public Workspace (Private PrivateAccess))
PrivateAccess (Personal Sensitive Sealed)
```

or eventually:

```text
AccessPolicy [Classification Audience FlowRestriction]
```

Do not start with that heavier shape unless implementation pressure proves
the single enum inadequate.

## Enforcement Consequences

Observation must become caller-aware. A query cannot mean "return matching
records" without knowing who asks and where the answer is going. The default
public/ordinary observation should behave as `maxAccess = Public`.

Owner/private observation can raise `maxAccess`, but should still require
operation-specific policy. A caller allowed to read `Personal` records may
not be allowed to export them into a public report.

Every output-producing path needs an access decision:

- `Observe`
- `Lookup`
- topic search
- recent/depth search
- `WithProvenance`
- export/report generation
- context-maintenance sweeps
- intent manifestation into `AGENTS.md`, skills, and repo `INTENT.md`

Information-flow discipline matters as much as read discipline. A higher
access record must not be summarized into a lower access surface. In
Bell-LaPadula language, Spirit needs the practical version of "no write down":
do not move protected material into public outputs.

## Migration Shape

Production records without an access field migrate to `Public`.

The ordinary `spirit "(Record (...))"` CLI should default to `Public`.
Private capture should require a distinct typed operation or explicit access
field, not an ambient shell flag. Because every component binary takes one
NOTA argument, this should be modeled in the signal schema, for example:

```text
Record [Entry]
RecordPrivate [Entry PrivateAccess]
```

or by adding `Access` to `Entry` and making the CLI constructor explicit.

The private substrate remains open. Current `skills/privacy.md` correctly says
private personal substance must not go into ordinary Spirit until a private
Spirit substrate exists. This design should be treated as the path to that
substrate, not as permission to start recording private personal details in
the current public database.

## Tests Needed

Architecture tests should be named after constraints:

- `public_observation_cannot_return_personal_records`
- `public_topic_search_cannot_match_sensitive_descriptions`
- `private_record_cannot_manifest_into_public_skill`
- `with_provenance_cannot_bypass_access_filter`
- `sealed_lookup_returns_only_allowed_envelope`
- `legacy_records_migrate_to_public`

The strongest witness is a two-step Nix test: write records at multiple
access levels, then run observation/export commands through different caller
surfaces and prove only allowed records appear.

## Sources

- NIST SP 800-60 Vol. 1 Rev. 1: https://csrc.nist.gov/pubs/sp/800/60/v1/r1/final
- NIST SP 800-122: https://csrc.nist.gov/pubs/sp/800/122/final
- NIST SP 800-162: https://csrc.nist.gov/pubs/sp/800/162/upd2/final
- Helen Nissenbaum, "Privacy as Contextual Integrity": https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/
- Daniel J. Solove, "A Taxonomy of Privacy": https://papers.ssrn.com/sol3/papers.cfm?abstract_id=667622
