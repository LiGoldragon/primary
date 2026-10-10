# Spirit Per-Record Access Classification — Research Across Traditions

## Frame

### Psyche directive

Per Spirit records 1447, 1448, and 1449 (psyche 2026-06-02), Spirit
records will gain a per-record access-classification field. The shape
is a graduated discrete enum (NOT a boolean), refining the existing
owner-socket / ordinary-socket privilege split — which is binary today.
The default level is the most-public. Candidate level vocabulary
mentioned in the directive includes "public", "personal", "sensitive",
"ultra-personal" — but the exact set is open. The psyche explicitly
invited research before deciding: *"You could do some research on
that. See what the thinkers are thinking in that field of thought.
We have access to books and stuff too."*

### What this report covers

Six research dimensions:

1. Government / military information classification
2. Modern privacy taxonomies (academic)
3. Legal / regulatory data classification
4. Computer-science access control models
5. Social and personal privacy practice
6. Contemplative / spiritual disclosure traditions

Then synthesis: cross-cutting patterns, Spirit's distinctive context,
2-4 candidate enum sets with tradeoffs, and open questions for the
psyche.

### What is out of scope

- Implementation: no schema edits, no source touches, no migration plan.
- The filter language (`AccessSelection` shape) — that's a separate
  design once the enum vocabulary settles.
- Cross-record relationships (e.g., one elevated record causing
  adjacent records to elevate) — out of scope.
- Authentication / cryptographic protection — Spirit's access field is
  metadata gating, not encryption. The model is appropriateness, not
  against-attacker security; the psyche's directive frames this as
  RESPECTFUL RESERVE rather than DEFENSIVE SECRECY.

### Method

WebSearch + WebFetch across six dimensions, eighteen primary searches
with targeted fetches to fill in specifics on canonical sources
(Solove's taxonomy, GDPR special categories, TLP 2.0, PaRDeS,
seal of confession, psychotherapy notes). The Magnitude enum's
existing vocabulary in `signal-sema/src/magnitude.rs` informs the
naming-style register the new enum should sit in.

## 1. Government / military information classification

The classical multi-tier confidentiality model — the deepest-rooted
graduated-classification tradition in modern bureaucracy. It originated
in military intelligence and propagates outward to civilian government,
defense contractors, and (via Bell-LaPadula) computer security.

### United States — Confidential / Secret / Top Secret + compartments

The US system uses three primary classification levels and layered
compartments:

- **Confidential (C)**: information whose unauthorized disclosure
  "reasonably could be expected to cause damage to the national
  security".
- **Secret (S)**: disclosure could be expected to cause "serious
  damage to national security". Requires a deeper background
  investigation; clearance renews every ten years.
- **Top Secret (TS)**: disclosure could cause "exceptionally grave
  damage". Strongest investigation; shortest renewal cycle.

Above Top Secret there are not higher levels but layered
COMPARTMENTS:

- **Sensitive Compartmented Information (SCI)**: classified
  intelligence concerning or derived from sensitive sources,
  methods, or analytical processes. Handled inside formal access
  control systems established by the Director of National
  Intelligence. Specific SCI compartments carry code words
  (e.g. TALENT KEYHOLE for satellite imagery; GAMMA for SIGINT
  derivative).
- **Special Access Programs (SAP)**: programs imposing need-to-know
  controls beyond those for any Collateral classification level.
  Often "black" programs whose existence is itself protected.

Beneath Confidential, there is no "Unclassified" classification per
se — but **Controlled Unclassified Information (CUI)** is a category
for material that is unclassified yet whose dissemination is
restricted. CUI replaces a previous patchwork of "For Official Use
Only", "Sensitive But Unclassified", etc.

The structural insight: three levels of TIERED severity + an
orthogonal axis of COMPARTMENTS that gate by need-to-know rather
than by clearance grade. A person with TS clearance still cannot
read a particular SCI compartment unless they are "read in" to that
compartment.

Sources: [Classified information in the United States — Wikipedia](https://en.wikipedia.org/wiki/Classified_information_in_the_United_States), [FAS Introduction to the Security and Classification System](https://sgp.fas.org/classdod.htm), [Electrospaces: The US Classification System](https://www.electrospaces.net/2013/09/the-us-classification-system.html).

### United Kingdom — Official / Secret / Top Secret

The UK's Government Security Classifications Policy (GSCP), issued
2018 by the Cabinet Office, collapses the older five-level system
(Unclassified / Restricted / Confidential / Secret / Top Secret) to
THREE levels:

- **OFFICIAL**: the vast majority of government information —
  general administration, public safety, criminal justice, law
  enforcement. Default classification for working government data.
- **SECRET**: very sensitive information justifying heightened
  protective measures against determined or highly capable threats;
  where compromise might seriously damage military capabilities,
  international relations, or serious-crime investigation.
- **TOP SECRET**: highest sensitivity — national security at the
  level of highly capable threat sources.

The clever wrinkle is **OFFICIAL-SENSITIVE** — not a separate
classification but a HANDLING MARKING applied to a subset of OFFICIAL
that warrants extra caution. OFFICIAL-SENSITIVE is "still
classification OFFICIAL but watch yourself". This is a useful pattern:
a primary tier ladder + a fine-grain sub-marking that doesn't break
the tier vocabulary.

The 2018 reform shifted the philosophical basis: classification is
NOT based on the consequence of compromise but on the CAPABILITY and
MOTIVATION of potential threat actors. This is a notable departure
from US doctrine and worth noting — but for Spirit's case
(no malicious adversary) the consequence-based model still applies.

Sources: [Government Security Classifications Policy — Wikipedia](https://en.wikipedia.org/wiki/Government_Security_Classifications_Policy), [GOV.UK — Government Security Classifications](https://www.gov.uk/government/publications/government-security-classifications), [Government Classification Scheme — Ministry of Justice](https://security-guidance.service.justice.gov.uk/government-classification-scheme/).

### NATO — four levels plus ATOMAL

NATO's system uses FOUR levels:

- **COSMIC TOP SECRET (CTS)**: disclosure could cause "exceptionally
  grave damage to NATO". The "COSMIC" prefix signifies subject to
  special security controls.
- **NATO SECRET (NS)**: disclosure would cause "serious damage".
- **NATO CONFIDENTIAL (NC)**: disclosure would be "damaging to
  NATO interests".
- **NATO RESTRICTED (NR)**: disclosure would be "disadvantageous"
  — note this language is materially weaker than US "Confidential".

Plus the **ATOMAL** compartment for US RESTRICTED DATA / FORMERLY
RESTRICTED DATA and UK Atomic Information released to NATO. ATOMAL
combines with the tier: COSMIC TOP SECRET ATOMAL (CTSA), NATO
SECRET ATOMAL (NSA), NATO CONFIDENTIAL ATOMAL (NCA).

The structural lesson: NATO uses FOUR levels because the RESTRICTED
tier ("disadvantageous") covers material that's sensitive enough to
not be public but not damaging enough to be CONFIDENTIAL. This
analogous-to-OFFICIAL-SENSITIVE gap exists in many real-world
information sets.

Sources: [NATO Security Briefing — US Marines](https://www.information.marines.mil/Portals/224/Docs/Newcomers/NATO-Security-Briefing.pdf), [Classified information — Wikipedia](https://en.wikipedia.org/wiki/Classified_information), [CUI Category: NATO Restricted — National Archives](https://www.archives.gov/cui/registry/category-detail/nota-restricted.html).

### Cross-cutting takeaway for Spirit

- 3 primary levels is the modal count (US, UK); 4 is common (NATO,
  corporate); 5 is rare (US pre-CUI-consolidation).
- Compartments / handling-markings (SCI, SAP, ATOMAL,
  OFFICIAL-SENSITIVE) are an ORTHOGONAL axis layered on top of the
  primary tier — they answer "who can see it" rather than "how
  severe is the elevation".
- Level names connote a graded danger continuum
  (CONFIDENTIAL < SECRET < TOP SECRET). The names form a clear
  ascending order even out of context — a useful linguistic property.

For Spirit's case there is no adversary, no need-to-know
compartments, no consequence-of-compromise calculus. But the TIERED
ENUM with ASCENDING GRAVITY pattern transfers cleanly.

## 2. Modern privacy taxonomies (academic)

### Daniel Solove — A Taxonomy of Privacy (2006)

Solove's *A Taxonomy of Privacy* (University of Pennsylvania Law
Review, 2006) is the most-cited contemporary attempt to give privacy
a systematic structure. Citation count: 1095+.

Solove rejects the project of defining privacy in a single sentence
("Privacy is a concept in disarray that nobody can articulate
clearly") and instead enumerates SIXTEEN HARMFUL ACTIVITIES grouped
into FOUR FAMILIES — the unit of analysis is the HARM, not the
information type. The taxonomy:

**Group 1 — Information Collection (2 categories)**

- **Surveillance**: continuous monitoring creating anxiety and a
  chilling effect on behavior.
- **Interrogation**: acquiring information through coercion or
  compulsion.

**Group 2 — Information Processing (5 categories)**

- **Aggregation**: combining isolated data points into a comprehensive
  profile; the whole becomes greater than the parts.
- **Identification**: linking aggregated data to a real individual;
  "reducing an individual to a list of traits".
- **Insecurity**: negligence creating vulnerability to future privacy
  harms.
- **Secondary Use**: employing data for purposes beyond original
  consent.
- **Exclusion**: denying individuals notice and input into how their
  records are used.

**Group 3 — Information Dissemination (6 categories)**

- **Breach of Confidentiality**: violating trust in a special
  relationship.
- **Disclosure**: revealing personal information causing reputational
  damage.
- **Exposure**: revealing physical or emotional attributes considered
  private — embarrassment, humiliation.
- **Increased Accessibility**: making dispersed information centrally
  available.
- **Appropriation**: using someone's identity for another's purposes.
- **Distortion**: manipulating perception through inaccurate
  information.

**Group 4 — Invasion (2 categories)**

- **Intrusion**: intruding upon solitude or seclusion.
- **Decisional Interference**: unwanted intrusion into life decisions
  / autonomy.

For Spirit's case, Solove's taxonomy is a USEFUL CHECK — the access
field controls Dissemination (Group 3) and to a lesser extent
Aggregation (Group 2, "the whole becomes greater than the parts" —
a public timeline of all Spirit records could leak more than any
single record). Solove's lesson: the harm is in the FLOW, not just
in the bit. Spirit's access enum is rightly attached to the record
because the record IS the unit of flow.

Solove's framework also suggests Spirit should not just gate
disclosure but consider whether elevated records should resist
AGGREGATION queries (e.g., "show me all records by topic" should
respect access levels even when the result is an aggregate).

Sources: [A Taxonomy of Privacy SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=667622), [Open Rights Group wiki — Solove taxonomy](https://wiki.openrightsgroup.org/wiki/A_Taxonomy_of_Privacy), [TeachPrivacy — Taxonomy of Privacy](https://teachprivacy.com/taxonomy-of-privacy/).

### Helen Nissenbaum — Contextual Integrity (2010)

Nissenbaum's *Privacy in Context* offers a fundamentally different
theory: privacy is NOT secrecy but APPROPRIATE FLOW OF INFORMATION
within a context. The famous quote: "people conflate privacy with
secrecy".

The theory defines privacy across FIVE PARAMETERS:

1. **Data subject** — whom the information is about
2. **Sender** — who is communicating it
3. **Recipient** — to whom it is being sent
4. **Information type** — what kind of information
5. **Transmission principle** — under what norm (consent, confidentiality, obligation, reciprocity, ...)

A privacy VIOLATION is a disruption of expected norms of information
flow — a change in any of the five parameters that breaks the
context's appropriate-flow rule. Telling a doctor about your
symptoms (subject=you, sender=you, recipient=doctor, type=health,
principle=clinical confidentiality) is fine. Telling the same to an
advertiser violates contextual integrity even though the data
content is identical.

For Spirit, contextual integrity is a CRITIQUE of access-tier
models. A tier label on a record is information-type centered;
Nissenbaum would say the question is not "how sensitive is the
information" but "to whom is it appropriate to flow under what
principle". A record about the psyche's emotional state shared with
Claude (close collaborator, contextually appropriate) is not
violating privacy even though it's elevated material; the same
record exfiltrated to an unrelated agent IS violating, regardless
of any label.

The practical implication: Spirit's tier label answers half the
question — the INFORMATION TYPE / SENSITIVITY half. The OTHER half
(recipient, transmission principle) is encoded in WHICH SOCKET the
query came from and which agent is requesting. Spirit's current
binary owner-socket / ordinary-socket split is contextual-integrity
work; the new tier enum is information-type work; together they
encode appropriate flow.

Sources: [Contextual integrity — Wikipedia](https://en.wikipedia.org/wiki/Contextual_integrity), [Privacy As Contextual Integrity — Washington Law Review](https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/), [Bridging Barriers interview](https://bridgingbarriers.utexas.edu/news/people-conflate-privacy-secrecy-interview-good-systems-symposium-keynote-speaker-helen).

### Alan Westin — Privacy and Freedom (1967)

Westin's *Privacy and Freedom* (1967) is the foundational
contemporary text. He defines privacy as "the claim of individuals
to determine for themselves when, how, and to what extent
information about them is shared with others".

Westin enumerates FOUR STATES of privacy:

- **Solitude**: being alone; no one perceiving you.
- **Intimacy**: small-group seclusion; close persons only.
- **Anonymity**: freedom from identification in public; the crowd
  hides you.
- **Reserve**: the ability to withhold communication even when
  others are present.

And FOUR FUNCTIONS of privacy:

- **Personal autonomy**: avoiding manipulation, domination, exposure.
- **Emotional release**: freedom from social roles to safely deviate.
- **Self-evaluation**: integrating experience into meaningful
  patterns; planning future actions.
- **Limited and protected communication**: opportunity to share
  personal information with TRUSTED OTHERS — the explicit graduated
  case.

For Spirit, Westin's four states map ONTO ACCESS LEVELS quite
naturally:

- **Solitude** ≈ records only the psyche-future-self sees
- **Intimacy** ≈ records shared with chosen collaborators
- **Reserve** ≈ records the psyche acknowledges exist but withholds
- **Anonymity** ≈ less directly relevant (Spirit records are not
  anonymous)

Westin's "limited and protected communication" function is the
CLEAREST psychological justification for graduated access:
self-realization REQUIRES the ability to share at chosen depth with
chosen partners. Spirit, by giving the psyche the ability to mark
records at their appropriate depth, supports this function.

Sources: [Westin's four states of privacy — Marcus Olsson](https://marcusolsson.dev/four-states-of-privacy/), [Alan Westin's Legacy — IAPP](https://iapp.org/news/a/alan-westins-legacy-of-privacy-and-freedom), [Psychological functions of privacy — Hacking with Care](https://hackingwithcare.in/2014/04/psychological-functions-of-privacy-one-academic-literature-review/).

### Irwin Altman — boundary regulation theory (1975)

Altman's *The Environment and Social Behavior* (1975) reframes
privacy as a DIALECTICAL DYNAMIC PROCESS: "a selective control of
access to the self or to one's group". Privacy is not a STATE but a
process of boundary REGULATION — sometimes opening, sometimes
closing. The desired level of privacy is the amount needed to serve
the person's needs; the actual level is what is achieved; the gap
between desired and actual is the central tension.

Altman's contribution sits uneasily with tier-based access models
because tiers are STATIC LABELS. Altman would argue that the same
record might be appropriately public at one moment and appropriately
sealed at another — depending on the psyche's current need.

For Spirit, the Altman lesson is RE-CLASSIFICATION matters: it must
be possible to ELEVATE or DOWNGRADE a record after creation. Spirit
records are append-only data, but the access level is METADATA that
should be mutable (or, more cleanly, additive — a later record can
re-classify an earlier one). Without this affordance, Spirit
violates Altman's dynamic-boundary insight.

Sources: [Privacy regulation theory — Wikipedia](https://en.wikipedia.org/wiki/Privacy_regulation_theory), [Unpacking Privacy for a Networked World — Palen](https://cmci.colorado.edu/~palen/palen_papers/palen-privacy.pdf), [A Critical Evaluation of Altman's Definition — academia.edu](https://www.academia.edu/58201352/A_Critical_Evaluation_of_Altmans_Definition_of_Privacy_as_a_Dialectical_Process).

## 3. Legal / regulatory data classification

### GDPR — Article 9 special categories + Article 10 criminal data

GDPR's structure is TWO TIERS plus an exclusive ELEVATED CATEGORY:

- **Personal data** (the baseline): "any information relating to an
  identified or identifiable natural person". Default treatment;
  Article 6 lawful-basis required.
- **Special categories** (Article 9, the elevated tier): processing
  PROHIBITED BY DEFAULT unless one of 10 exceptions applies. The
  categories:
  - racial or ethnic origin
  - political opinions
  - religious or philosophical beliefs
  - trade union membership
  - genetic data
  - biometric data (for unique identification)
  - health data
  - sex life / sexual orientation
- **Criminal convictions** (Article 10, parallel elevated tier):
  processed only under control of official authority or where
  authorised by Union/Member-State law with appropriate safeguards.

Notable: Article 9 categories are CONTENT-BASED — they enumerate
TYPES of information rather than degrees of severity. The elevation
is BINARY (special or not), not graduated. There's no "particularly
special" beyond Article 9.

For Spirit, the GDPR pattern is THE BASELINE-PLUS-ENUMERATED-ELEVATIONS
model: a default tier plus a list of categories that always elevate.
This is the simplest possible graduated model — 2 tiers — and works
because the categories are well-defined and culturally stable.

Sources: [Article 9 GDPR — GDPR-Text.com](https://gdpr-text.com/read/article-9/), [Special category data — ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/a-guide-to-lawful-basis/special-category-data/), [GDPR Article 10 explained — gdprinfo.eu](https://gdprinfo.eu/gdpr-article-10-explained-processing-personal-data-relating-to-criminal-convictions-and-offences).

### HIPAA — PHI as a unified category, with psychotherapy-notes subtier

HIPAA defines **Protected Health Information (PHI)** as a unified
category — health information held by a covered entity that
identifies an individual. The 18 identifier types (names, dates,
contact info, biometrics, etc.) determine WHEN information becomes
PHI; once classified as PHI, the protection is uniform.

The interesting subtlety: **psychotherapy notes** receive HIGHER
protection than other PHI. HIPAA defines them as "notes recorded
(in any medium) … documenting or analyzing the contents of
conversation during a private counseling session…that are separated
from the rest of the individual's medical record". Crucially:

- Psychotherapy notes are SEPARATELY STORED.
- Clients generally do NOT have automatic right to access them.
- They are NOT covered by routine release-of-records authorizations.
- They contain the therapist's personal impressions, theoretical
  analysis — material that could harm the client if shared
  uncritically.

This is the closest legal analog to Spirit's "ultra-personal" level:
material recorded by the practitioner for PROCESSING / SELF-USE,
held separately, accessed only with explicit elevated authorization.
The HIPAA design recognizes that some recordings exist for the
RECORDER'S processing, not for the record subject's medical
treatment — and protects them as a distinct class.

Sources: [HIPAA PHI: Definition and 18 Identifiers — Berkeley](https://cphs.berkeley.edu/hipaa/hipaa18.html), [Psychotherapy Notes and HIPAA — HIPAA Journal](https://www.hipaajournal.com/psychotherapy-notes-and-hipaa/), [Psychotherapy Notes & HIPAA — Accountable](https://www.accountablehq.com/post/psychotherapy-notes-hipaa).

### California CCPA / CPRA — personal information + sensitive personal information

California's CPRA amends the CCPA to add a SECOND TIER:

- **Personal information** (baseline)
- **Sensitive personal information** (elevated):
  - Social Security numbers, driver's license numbers, passport numbers
  - Account log-in credentials
  - Precise geolocation
  - Racial or ethnic origin
  - Religious or philosophical beliefs
  - Union membership
  - Private communications
  - Genetic data
  - Biometric data (for unique identification)
  - Health data
  - Sex life / sexual orientation
  - Citizenship / immigration status (added 2024 by AB 947)
  - Neural data (added 2025 by SB 1223)

Two-tier model, same shape as GDPR. The novel "neural data" addition
shows the model evolves: new sensitive categories emerge as
technology creates new disclosure modes. Spirit's enum should expect
SIMILAR EVOLUTION: what's "ultra-personal" today may be unremarkable
in five years.

Sources: [California Consumer Privacy Act — California AG](https://oag.ca.gov/privacy/ccpa), [California Expands Sensitive PI — Akin](https://www.akingump.com/en/insights/blogs/ag-data-dive/california-expands-definition-of-sensitive-personal-information-covered-under-ccpa), [Sensitive Personal Information — Bastion](https://bastion.tech/learn/ccpa/sensitive-personal-information).

### PII vs sensitive PII (NIST and general US practice)

NIST defines Personally Identifiable Information as "any
representation of information that permits the identity of an
individual to whom the information applies to be reasonably
inferred". US practice splits PII into TWO TIERS:

- **Non-sensitive PII**: zip code, race, gender, birth date,
  religion (note: not always non-sensitive elsewhere). Can be
  freely sent without securing.
- **Sensitive PII**: SSN, driver's license, credit cards, medical
  records, financial accounts. Must be secured at rest and in
  transit.

The NIST guidance is RISK-BASED: stricter controls cost more, so
match the control to the consequence-of-disclosure for that data
class.

Sources: [PII — NIST CSRC](https://csrc.nist.gov/glossary/term/PII), [Personally Identifiable Information — Lepide](https://www.lepide.com/cyber-learning/what-is-personally-identifiable-information-pii/), [Comparing SPII vs PHI and PII — Concentric](https://concentric.ai/comparing-spii-vs-phi-and-pii-a-sensitive-information-guide/).

### Cross-cutting regulatory observation

Across GDPR, HIPAA, CCPA/CPRA, NIST PII, the pattern is OVERWHELMINGLY
TWO-TIER: a baseline plus an elevated category enumerated by content.
None of these regulators uses a 5-level enum. The reason is
operational: regulators need EASY-TO-OBSERVE rules. Five tiers
introduces line-drawing problems at each boundary.

For Spirit, this argues that more tiers than ~4 will create
classification anxiety — the psyche will have to think harder about
each record. That's a real cost.

## 4. Computer-science access control models

### Bell-LaPadula — formal multi-level confidentiality

Bell-LaPadula (Bell & LaPadula, 1973-1976) is the formalization of
US DoD multilevel security into a state-machine model. The crucial
properties:

- **Simple Security Property** ("no read up"): a subject at level L
  cannot read an object at level > L.
- **Star Property** ("no write down"): a subject at level L cannot
  write to an object at level < L (preventing classified material
  from leaking into lower-classification stores).
- Plus the **Discretionary Security Property**: access subject to a
  conventional access matrix.

The model treats LEVELS as a POSET (typically a total order). A
subject's clearance and an object's classification are drawn from
the same lattice. The model proved that a system can remain in a
secure state across transitions.

For Spirit, the BLP lesson is the OBJECT LABEL / SUBJECT CLEARANCE
SEPARATION. The access field on the Spirit record is OBJECT LABEL
("this record is classified Sensitive"). The requester's CLEARANCE
comes from which socket they're on (owner socket = full clearance;
ordinary socket = Public-clearance-only by default). This separation
is what makes graduated classification implementable — the label is
data, the clearance is connection context.

Spirit's case is simpler than full BLP because Spirit doesn't worry
about WRITE operations leaking down (only the psyche writes; sub-agents
read). The "no write down" property doesn't apply — Spirit needs only
the "no read above clearance" property.

Sources: [Bell-LaPadula model — Wikipedia](https://en.wikipedia.org/wiki/Bell%E2%80%93LaPadula_model), [Bell-LaPadula Model: A MAC Model — Binaryte](https://binaryte.com/blog/post/bell-lapadula-model-a-mac-model-for-achieving-multi-level-security.md/), [Bell-LaPadula CISSP Guide](https://www.learnsecuritymanagement.com/cissp-bell-lapadula-model).

### Biba — formal integrity (the dual)

Biba (1975) is the integrity counterpart:

- **Simple Integrity Axiom** ("no read down"): subject at integrity
  level I cannot read object at integrity < I (preventing
  contamination by low-integrity data).
- **Star Integrity Axiom** ("no write up"): subject at integrity I
  cannot write to object at integrity > I (preventing low-integrity
  subject from corrupting high-integrity data).

For Spirit, Biba is mostly NOT RELEVANT (Spirit's concern is
confidentiality, not integrity), but it has one useful frame: if
some records have INTEGRITY classifications (e.g., "this is a
Maximum-magnitude principle, do not let it be silently contradicted
by Minimum-magnitude later records"), Biba's no-write-up principle
applies. Worth noting but separate from the access-classification
work.

Sources: [Biba Model — Wikipedia](https://en.wikipedia.org/wiki/Biba_Model), [Biba Integrity Model CISSP Guide](https://www.learnsecuritymanagement.com/cissp-biba-integrity-model).

### MAC / DAC / RBAC / ABAC

- **MAC (Mandatory Access Control)**: access enforced by
  predefined security labels and classifications, NOT by user
  discretion. Owner cannot override. Military / defense pattern.
- **DAC (Discretionary Access Control)**: owner decides who else
  can access. Filesystem unix permissions. Flexible, low-security.
- **RBAC (Role-Based Access Control)**: access tied to roles
  assigned to users, not users individually. Enterprise pattern.
- **ABAC (Attribute-Based Access Control)**: access decision is a
  policy function over arbitrary attributes (user, resource,
  environment, action). Flexible, fine-grained. Healthcare and
  cloud pattern.

For Spirit, the relevant model is closest to MAC: the access label
is set on the record (not by the requester); the daemon
enforces. The label cannot be overridden by the requester. The
psyche acts as the AUTHORITY who sets labels (analogous to a
classification authority in MAC), and the daemon is the REFERENCE
MONITOR that enforces.

But Spirit is NOT pure MAC because there's a discretionary element:
the psyche can change a record's label after creation (Altman's
dynamic-boundary insight). It is "MAC with owner override" — a
hybrid that's actually closer to LATTICE-BASED MAC + DAC layered.

Sources: [Access Control Models RBAC vs ABAC vs DAC vs MAC — SHK Corp](https://www.shkcorp.com/blog/access-control-models), [Types of Access Control — TechPrescient](https://www.techprescient.com/blogs/types-of-access-control/), [Access Control Models 2026 CISSP Guide](https://flashgenius.net/guides/access-control-models-explained-mac-vs-dac-vs-rbac-vs-abac-2026-cissp-guide).

### Object-capability model

Object-capability security is the alternative to LABEL-based access:
authority is communicated by UNFORGEABLE TOKENS (capabilities) that
combine designation and authority. Whoever holds the capability can
exercise it. The principle: **Principle of Least Authority (PoLA)**
— components receive only the capabilities they need.

For Spirit, capability-based design would mean: there's no "level"
on the record; instead, the daemon issues TOKENS to requesters
granting access to specific records. The ordinary socket has a token
granting access to all Public records; the owner socket has a token
granting access to all records.

This is NOT what the psyche directive describes. The directive
describes a STATIC LABEL on the record + a filter at query time.
That's MAC, not ocap. The ocap alternative is theoretically cleaner
(no labels to maintain, no level-vocabulary debate, finer-grained)
but operationally heavier and less ergonomic for the psyche.

Worth noting: capability-based design integrates well with TLP-style
SHARING markings ("share with these capability-holders only") and
could be a later evolution. For now, the static-label MAC pattern is
what the directive wants.

Sources: [Capability-based security — Wikipedia](https://en.wikipedia.org/wiki/Capability-based_security), [Object-capability model — Wikipedia](https://en.wikipedia.org/wiki/Object-capability_model).

### Traffic Light Protocol (TLP) 2.0 — the modern info-sharing tier ladder

TLP is a four-level information-sharing classification widely used
in incident response and cyber threat intelligence:

- **TLP:RED** — recipients may NOT share outside the specific
  conversation/meeting in which the information was disclosed.
- **TLP:AMBER+STRICT** — share only within the recipient's
  organization (added in TLP 2.0).
- **TLP:AMBER** — share with members of the recipient's organization
  AND its clients, on a need-to-know basis.
- **TLP:GREEN** — share with peers and partner organizations within
  the community, but not via public channels.
- **TLP:CLEAR** (formerly TLP:WHITE) — share without limit.

TLP is RELEVANT for Spirit because:

1. It's a SHARING-DIRECTIVE rather than a SEVERITY tier — it tells
   the recipient where THEY can pass it to. This is closer in spirit
   to Spirit's case than the threat-of-disclosure model.
2. The colors form a memorable ladder.
3. TLP 2.0 explicitly added a finer-grain tier (AMBER+STRICT)
   between two coarser ones — showing that real-world use surfaces
   gaps in tier vocabulary and refines incrementally.
4. The default TLP:CLEAR matches Spirit's "default is most-public"
   directive.

TLP is NOT directly adoptable (the colors don't fit Spirit's
naming-style register), but the FOUR-LEVELS + DEFAULT-OPEN pattern
transfers.

Sources: [Traffic Light Protocol — FIRST](https://www.first.org/tlp/), [CISA TLP definitions](https://www.cisa.gov/news-events/news/traffic-light-protocol-tlp-definitions-and-usage), [TLP 2.0 Going Softer on AMBER — Palo Alto Networks](https://live.paloaltonetworks.com/t5/community-blogs/tlp-update-2-0-going-softer-on-amber-and-adding-amber-strict/ba-p/530512).

### Corporate data classification — Public / Internal / Confidential / Restricted

The dominant industry pattern (Oracle, Microsoft, Drata, Palo Alto,
Fortra all converge here):

- **Public**: openly shareable; no harm if disclosed; marketing
  collateral, press releases.
- **Internal**: used within the organization; minor risk if leaked;
  internal communications, non-sensitive HR.
- **Confidential**: unauthorized disclosure damages the
  organization; intellectual property, financial records, strategy.
- **Restricted** (or Highly Confidential): severe damage if
  disclosed; SSNs, credit cards, regulated personal data, classified
  material.

The lesson: FOUR LEVELS strike "a balance between simplicity and
nuance" — phrasing used verbatim by multiple sources. Four is the
ENTERPRISE SWEET SPOT. Three is too coarse (no room for "default
work-in-progress"); five is too fine.

Sources: [Data Classification Levels — Fortra](https://www.fortra.com/blog/data-classification-levels-explained-enhance-data-security), [Data Classification & Sensitivity Labels — Microsoft](https://learn.microsoft.com/en-us/compliance/assurance/assurance-data-classification-and-labels), [Information and Assets Classification — Oracle](https://www.oracle.com/corporate/security-practices/corporate/information-assets-classification/).

## 5. Social and personal privacy practice

### Diary and journal traditions — three-layer pattern is recurrent

Across diary traditions, a THREE-LAYER pattern recurs:

- **Shareable** — letters, social diary entries, the public face;
  intended for circulation or eventual publication.
- **Private** — material the writer holds personally; sometimes
  shared with intimates, rarely with the world.
- **Sealed / posthumous** — material protected until death or
  beyond; sometimes destroyed by instruction.

**Samuel Pepys (1660-1669)**: wrote his diary in Thomas Shelton's
Tachygraphy shorthand to prevent casual reading. For sensitive
passages — specifically his sexual activity — he layered ADDITIONAL
encryption: first French (still in shorthand) in 1664, then Spanish
/ Latin / Greek by 1666, then dummy-letter ciphers by 1667. He used
this graduated encryption "in NO PASSAGES OTHER THAN those concerned
with his philandering" — a CONTENT-TRIGGERED elevation, very much
like GDPR Article 9.

**Anaïs Nin (1914-1977)**: kept her diary for 63 years, accumulating
~15,000 typewritten pages in ~150 volumes. The diaries exist in TWO
PUBLICATION LAYERS:
- **Expurgated** editions (1966 onwards) — the version Nin authorized
  during her life
- **Unexpurgated** editions (1986 onwards via Rupert Pole, her
  widower) — including the sexually frank material she had excluded
  from the expurgated edition

Nin's pattern is GRADUATED POSTHUMOUS DISCLOSURE: material she
wanted published, material she wanted withheld until after her
death, material that might never be published. Each diary entry
carried an implicit access level even when written.

**Franz Kafka (1883-1924)**: left two notes instructing Max Brod, his
literary executor, to BURN UNREAD all his unpublished papers
("everything in the way of notebooks, manuscripts, letters, sketches
and so on should be burned unread and to the last page"). Brod
refused and published the works — beginning a famous ethical-literary
debate about whether the EXECUTOR honors stated intent or aesthetic
value. The 2023 unexpurgated diary edition restored material Brod
had tidied for early publication.

The Kafka case demonstrates the LIMIT of access metadata: a
classification label says "do not share", but enforcement requires
TRUST IN THE READER. Spirit's case is mostly safer (the daemon
mechanically enforces what the label says), but the Kafka-Brod
problem reappears anywhere a human reader is in the loop.

Sources: [The Diary of Anaïs Nin — Wikipedia](https://en.wikipedia.org/wiki/The_Diary_of_Ana%C3%AFs_Nin), [The Hidden Diary of Samuel Pepys — History Today](https://www.historytoday.com/archive/feature/hidden-diary-samuel-pepys), [Kafka's Last Wish — Literary Hub](https://lithub.com/kafkas-last-wish-brods-first-betrayal/), [Franz Kafka's Diaries — Wikipedia](https://en.wikipedia.org/wiki/Franz_Kafka's_Diaries).

### Social media — five-tier modern default

Facebook (and analogues across Instagram, LinkedIn, etc.) settled on
FIVE LEVELS:

- **Public** — anyone on or off the platform
- **Friends** — accepted connections
- **Friends except [excluded]** — friends minus specific people
- **Specific friends** — only an explicit list
- **Only me** — visible only to the author

Plus the LIST-based extensions:

- **Close Friends** list — a hand-curated subset for higher-trust
  sharing
- **Restricted** list — nominal friends who only see Public posts

The five-tier model is interesting because it's been ITERATIVELY
TESTED on billions of users and converged to this shape. The
load-bearing levels are PUBLIC (default), FRIENDS (the social-graph
default), and ONLY ME (the journaling/self-only level). The
in-between tiers (Specific friends, Close Friends) handle "this is
for a smaller circle than friends-default".

For Spirit, the directly analogous structure is:

- Public ≈ ordinary-socket-accessible (workspace principles)
- Friends ≈ owner-socket-with-default-elevation (collaborators)
- Close Friends ≈ owner-socket-with-personal-elevation
- Only Me ≈ owner-socket-with-maximum-elevation (private)

The five-tier social-media model maps almost cleanly to a five-tier
Spirit enum.

Sources: [Controlling Your Privacy on Facebook — Thinglabs](https://thinglabs.io/facebook-only-me-post), [Facebook Privacy and Security 2026 — Brodneil](https://www.brodneil.com/facebook-privacy-and-security/), [Facebook's Audience Selector — Bobology](https://www.bobology.com/public/Facebooks-Audience-Selector-Choose-Who-Sees-a-Post.cfm).

### Therapy notes vs progress notes — the legal codification of "for the practitioner's own processing"

The HIPAA distinction between progress notes (clinical record,
shareable with insurance, part of medical chart) and psychotherapy
notes (therapist's personal impressions, separated from the chart,
not part of routine release) is the legal CODIFICATION of the same
distinction Spirit faces:

- Records intended for SHARED USE (workspace principles, technical
  decisions) ≈ progress notes
- Records intended for the WRITER'S OWN PROCESSING (emotional
  observations, vulnerability, in-progress thinking) ≈ psychotherapy
  notes

HIPAA recognizes that the latter requires SEPARATE STORAGE and
SEPARATE AUTHORIZATION to access. This is structurally identical to
what the psyche directive describes for Spirit: most records flow
freely; some require explicit elevation to reach.

The lesson: TWO categories alone (progress vs psychotherapy) is
enough to capture a real distinction the legal system bothers to
formalize. Spirit could be 2-tier and still serve the core use case;
more tiers add resolution but not necessarily new function.

Sources: [Psychotherapy Notes vs Progress Notes — ICANotes](https://www.icanotes.com/2018/06/08/the-differences-between-psychotherapy-notes-and-progress-notes/), [Psychotherapy notes vs progress notes — Upheal](https://www.upheal.io/documentation/psychotherapy-notes-vs-progress-notes), [Psychotherapy Notes & HIPAA — Accountable](https://www.accountablehq.com/post/psychotherapy-notes-hipaa).

## 6. Contemplative / spiritual disclosure traditions

### Buddhist Right Speech — the five filters

The Pali Canon (Anguttara Nikaya 5.198) gives FIVE qualities of
right speech:

1. **Timeliness** — spoken at the right time
2. **Truthfulness** — in accord with fact
3. **Kindness** — affectionately, with good will
4. **Benefit** — beneficial to the hearer
5. **Compassionate intention** — with a mind of good will

The Buddha is explicit that TRUE-AND-CORRECT-BUT-NOT-BENEFICIAL
speech should not be uttered; true-correct-beneficial-but-unwelcome
speech is to be timed. The framework is not about secrecy per se but
about a FILTER for what to disclose. Even what is TRUE doesn't
automatically warrant disclosure — there's a SECONDARY QUESTION of
whether disclosure is appropriate at this moment, to this hearer.

For Spirit, the Buddhist frame says: even Public records are not
"meant to be broadcast"; they're "available when appropriate".
Access classification is one piece of a larger appropriateness
question. The Spirit daemon enforces only the access label; the
psyche and downstream agents must still ask whether INVOKING the
record (in chat with a particular interlocutor, at a particular
moment) is right speech.

Sources: [Right Speech in the Pali Canon — Wannabe Poet](https://wannabepoet.com/2022/05/11/right-speech-in-the-pali-canon/), [Buddha's Teachings on Right Speech — Zen Studies](https://zenstudiespodcast.com/right-speech/), [Right Speech — Learn Religions](https://www.learnreligions.com/right-speech-450072).

### Sufi adab — etiquette of revelation

Sufi adab is the ETIQUETTE of spiritual conduct, including the
etiquette of WHAT IS DISCLOSED to whom. The framework is anchored in
ma'rifah (intuitive knowledge of God) reached THROUGH praxis, with
the etiquette of the student as the pivotal element. Adab connects
to maqamat (stations or assemblies) — disclosure that's appropriate
at one maqam may not be appropriate at another.

The structural insight: spiritual disclosure is GRADED by the
RECIPIENT'S READINESS. Material appropriate for an advanced student
may harm or mislead a beginner. This is the dual of access
classification: instead of labeling the OBJECT (the teaching) with a
level, the practice labels the SUBJECT (the student) with a level
and discloses what matches.

For Spirit, this maps to: if Spirit records were labeled per
recipient-readiness, a "Public" record might be safe to show any
agent, while a "Sensitive" record requires recipient (i.e., owner-
socket) authorization. The label is on the object; the recipient's
readiness is on the socket.

Sources: [Etiquette as Spiritual Nourishment — Yaqeen Institute](https://yaqeeninstitute.org/read/post/etiquette-as-spiritual-nourishment-the-adab-of-the-student-according-to-al-ghazali-and-al-isfahani), [The Sufi Practice of Adab — Spirituality and Practice](https://www.spiritualityandpractice.com/blogs/posts/civility-spirituality/132/the-sufi-practice-of-adab), [Adab — Sufi Etiquette in the Outer and Inner Worlds — Golden Sufi Center](https://goldensufi.org/article/adab-sufi-etiquette-in-the-outer-and-inner-worlds/).

### Kabbalah — PaRDeS as a four-tier interpretive depth model

The Jewish hermeneutic acronym **PaRDeS** ("orchard") names four
levels of textual / mystical interpretation:

- **Peshat** (פְּשָׁט, "plain") — the plain, literal meaning;
  surface reading
- **Remez** (רֶמֶז, "hint") — allegorical or symbolic meaning
  beyond the literal
- **Derash** (דְּרַשׁ, "inquire") — comparative / midrashic meaning;
  homiletic depth
- **Sod** (סוֹד, "secret") — the esoteric, mystical, Kabbalistic
  meaning

Sod is reserved teaching; it's not WITHHELD from all but available
only to those with sufficient preparation. The four-level model
corresponds in Kabbalistic theology to four spiritual Worlds and
four soul levels (Action / Emotion / Understanding / Wisdom).

This is the cleanest spiritual analog to Spirit's project: FOUR
GRADUATED LEVELS, each a deeper register of the same material, with
the deepest reserved. PaRDeS names BY DEPTH rather than by sensitivity
— note the linguistic difference. "Sod" doesn't mean "shameful" or
"dangerous"; it means "secret in the sense of esoteric, requiring
preparation".

For Spirit, the PaRDeS shape suggests names connoting DEPTH rather
than RISK. Compare: "Confidential" (risk) vs "Esoteric" (depth) — the
latter is more honest about what the elevated level actually is for
the psyche.

Sources: [Pardes (exegesis) — Wikipedia](https://en.wikipedia.org/wiki/Pardes_(exegesis)), [PaRDeS Jewish Hermeneutics — Hidden Orchard](https://www.thehiddenorchard.com/peshat-pardes/), [The Four Levels of Interpretation — Biblical Culture](https://biblicalculture.wordpress.com/2012/12/05/the-four-levels-of-interpretation/), [Introduction — Chabad.org](https://www.chabad.org/kabbalah/article_cdo/aid/1270231/jewish/Introduction.htm).

### Christian apophatic mysticism — reservation of the highest teaching

Pseudo-Dionysius the Areopagite (5th-6th century Syrian monk),
whose *Mystical Theology* shaped both Eastern and Western mystical
traditions, distinguishes:

- **Cataphatic theology** — what can be said of God affirmatively
- **Apophatic theology** — what God is NOT; the reserved tradition
  approached via unknowing

In *Mystical Theology* Dionysius explicitly warns against sharing
the treatise with the uninitiated — a classic "reserved for those
who can receive it without harm" disclosure principle. The Christian
mystical tradition (Eckhart, Cloud of Unknowing, John of the Cross)
inherits this reservation: certain teachings are protected not
because they're shameful but because they require preparation to
receive without distortion.

For Spirit, the apophatic model adds a nuance: the highest tier of
classification is not necessarily ABOUT THE PSYCHE's vulnerability
— it could be about COMPLEXITY OF MEANING. Some Spirit records may
encode psyche intent that's easily misread by an underprepared
agent; tagging them as elevated isn't just protecting the psyche
but protecting the AGENT from misinterpretation.

Sources: [Pseudo-Dionysius the Areopagite — Wikipedia](https://en.wikipedia.org/wiki/Pseudo-Dionysius_the_Areopagite), [Mystical Theology by Pseudo-Dionysius — EBSCO](https://www.ebsco.com/research-starters/literature-and-writing/mystical-theology-pseudo-dionysius-areopagite), [Pseudo-Dionysius the Areopagite — Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/pseudo-dionysius-areopagite/).

### Seal of confession — the absolute floor

The Catholic seal of confession (Canon 983, with roots in Lateran IV
1215) is the MOST RESTRICTIVE access classification in any human
tradition known to this research:

- The sacramental seal is INVIOLABLE.
- A priest cannot disclose what is confessed FOR ANY REASON —
  including to save his own life, protect his good name, save the
  life of another, aid justice, or avert public calamity.
- Recording or divulging confession material carries EXCOMMUNICATION
  *latae sententiae*.

This is "Sealed" in the most absolute sense: protection that admits
no exception. For Spirit, the seal-of-confession analog is the
deepest possible tier — material the psyche records for self-
understanding that has NO LEGITIMATE READER, not even another
authorized agent. The owner socket reaches it, but downstream
sharing is prohibited.

For Spirit, the lesson is the NAME for such a level should connote
ABSOLUTE NON-DISCLOSURE rather than mere elevation. "Sealed" works.
"Confidential" doesn't (too weak; the corporate world overloads
that word).

Sources: [Seal of confession in the Catholic Church — Wikipedia](https://en.wikipedia.org/wiki/Seal_of_confession_in_the_Catholic_Church), [Priests are bound to secrecy by seal of confessional — Catholic Times](https://catholictimescolumbus.org/news/priests-are-bound-to-secrecy-by-seal-of-confessional/), [Law of the Seal of Confession — Catholic Answers](https://www.catholic.com/encyclopedia/law-of-the-seal-of-confession).

### Mystery religions — initiation grades

Across mystery religions (Eleusinian, Mithraic, modern Rosicrucian,
Masonic), graduated INITIATION GRADES gate access to deepening
teaching:

- Lesser Mysteries — preliminary degrees
- Greater Mysteries — entered after preliminary completion
- Inner circle — esoteric core teaching reserved for advanced
  initiates

This is the structural ancestor of compartmented military
classification: ACCESS BY GRADE, with each grade a status the
recipient earns. For Spirit, this is interesting as a CONTRAST:
Spirit doesn't gate by recipient grade (other agents don't earn
clearance) — the gating is by the SOCKET they connect through, and
all sub-agents inherit the dispatcher's clearance level. The mystery-
religion model would be: each agent has its own classification level
and material flows down by clearance match. Spirit's model is
simpler — binary socket clearance + per-record label.

Sources: [Mystery Schools and Initiatic Orders — Sacred Ancestry](https://www.sacredancestry.com/blog/mystery-schools-amp-initiatic-orders), [Mystery Schools — Theosophical Society](https://www.theosociety.org/pasadena/mysterys/mystsch2.htm), [Esoteric Christianity — Wikipedia](https://en.wikipedia.org/wiki/Esoteric_Christianity).

## Cross-cutting patterns

After researching 6 dimensions across 18 distinct frameworks /
traditions, the following CROSS-CUTTING patterns emerge.

### Pattern 1 — three to five levels is the universal sweet spot

Counting actual levels across the surveyed traditions:

| Framework | Level count |
|---|---|
| US classification (Confidential / Secret / Top Secret) | 3 |
| UK GSCP (Official / Secret / Top Secret) | 3 |
| NATO | 4 |
| TLP 2.0 (Clear / Green / Amber / Amber+Strict / Red) | 5 |
| Corporate (Public / Internal / Confidential / Restricted) | 4 |
| GDPR (Personal / Special / Criminal) | 2-3 |
| HIPAA (PHI / Psychotherapy notes) | 2 |
| PII / Sensitive PII | 2 |
| Facebook / social media | 5 |
| PaRDeS | 4 |
| Westin four states | 4 |
| Buddhist Right Speech (five filters; not a tier system) | n/a |
| Pepys diary (plain / French / polyglot / cipher) | 4 |
| Solove taxonomy | 4 groups × 16 species (not a tier system) |

When traditions OFFER a tier ladder, the count clusters TIGHTLY at
3-5. Below 3 the resolution is too coarse; above 5 the line-drawing
overhead exceeds the benefit. The MODAL count is 4.

### Pattern 2 — default is usually the most-permissive (open)

In every tradition where there's a meaningful "default":

- TLP default is TLP:CLEAR (open)
- Facebook default depends on user but is most often Friends
- US classification default is unclassified
- UK GSCP default is OFFICIAL (the lowest)
- Corporate default is Public or Internal (low end)

The Spirit directive's "default is most-public" is the consensus
choice. The alternative (default-restricted, opt-in to public) is
seen ONLY in domains with adversarial settings (CIA, post-9/11
counterterrorism material) — and is operationally costly.

### Pattern 3 — elevation is usually a one-step verb

Across traditions the verb for raising classification is short and
declarative: "classify", "elevate", "compartment", "seal", "reserve".
The act is intentional, marked, and named. Records are NOT
"reclassified" in mass batches; each elevation is a deliberate act
applied to the record by the authority.

For Spirit, the lesson: the act of elevating a record's access level
should feel DELIBERATE in the recording UX. The psyche should think
"this record is personal" or "this record is sealed" as part of the
recording — not as a separate after-the-fact step.

### Pattern 4 — names connote either RISK or DEPTH

There's a fundamental linguistic split:

- **Risk-connoting** names: Confidential, Secret, Top Secret,
  Sensitive, Restricted, Classified
- **Depth-connoting** names: Peshat / Remez / Drash / Sod (PaRDeS),
  exoteric / esoteric, Solitude / Intimacy (Westin)
- **Audience-connoting** names: Public / Friends / Close Friends /
  Only Me (Facebook), Internal / External (corporate)

For Spirit, the choice is meaningful. Risk-connoting names
(Confidential, Sensitive) frame elevation as "this could harm if
disclosed". Depth-connoting names (Esoteric, Sealed) frame it as
"this is for inner-circle reception". Audience-connoting names
(Personal, Owner-only) frame it as "this is for these recipients".

The Spirit case — personal intent recorded for the psyche's own
use — fits BEST with audience-connoting names. There's no
adversary, so risk-connoting names overstate the threat. There's
no esoteric depth to most records, so depth-connoting names
overstate the substance. Audience-connoting names ("Personal",
"Sealed", "OwnerOnly") are honest about what the elevation actually
does: it narrows the audience.

### Pattern 5 — primary tier + handling marking is a common refinement

Several systems use a PRIMARY tier (the ordered enum) PLUS one or
more orthogonal MARKINGS:

- UK: OFFICIAL with optional -SENSITIVE marking
- US: TS with SCI / SAP compartments
- TLP 2.0: TLP:AMBER with optional +STRICT
- NATO: any tier with optional ATOMAL

The pattern is: keep the primary tier vocabulary small (3-5); when
finer granularity is needed, ADD A MARKING rather than ADD A TIER.
This keeps the ordered enum readable.

For Spirit, this argues against a 6+ tier vocabulary. If Spirit
wants finer-grain control, the right structural answer is a 4-tier
primary enum + an optional marking (e.g., "Sensitive+Health",
"Personal+Family") rather than 8 distinct tier names.

### Pattern 6 — graduated access supports the psyche's own work

Westin's "limited and protected communication" function, the
Buddhist filter of right speech, the Sufi etiquette of revelation,
the diary tradition of graduated layers — all converge on one point:
GRADUATED ACCESS IS NOT JUST DEFENSIVE. It's a positive support for
the self's processing. Material the psyche records at the deepest
level enables work that COULDN'T HAPPEN if the recording space were
public.

For Spirit, this reframes the access enum from "privacy controls"
to "self-respect controls": elevated levels exist not to keep
secrets but to give the psyche a space where vulnerable, in-progress,
or contradictory material can be recorded without performance.

## Spirit's distinctive context — what makes psyche-intent different

The traditions surveyed differ from Spirit's case on multiple axes.
Spirit's domain is:

### Personal-intent, not institutional

Most classification systems protect INSTITUTIONS (state, corporation,
hospital, NATO). The protected interest is the institution's
operations or its constituents. Spirit protects the PSYCHE'S OWN
RECORDING SPACE — a single human's intent log. The institution-
level concerns (chain of custody, audit, regulatory reporting,
adversary modeling) DO NOT APPLY.

The closest analogs are diary traditions (Nin, Pepys, Kafka) and
psychotherapy notes — both personal-not-institutional. The relevant
patterns come from these, not from BLP / NIST / corporate models.

### Self-and-collaborators, not adversarial

Government and corporate classification assumes ADVERSARIES (foreign
intelligence, competitors, fraudsters). Spirit has no adversary. The
audience is:

- The psyche-future-self (always allowed, no enforcement needed)
- Spirit's authorized agents (Claude, Codex, sub-agents) — trusted
  collaborators
- Possibly downstream readers if the workspace is opened to
  collaborators or open-sourced — but governed by intent, not
  defended against attack

The model is APPROPRIATENESS and SELF-RESPECT rather than DEFENSE.
The Buddhist Right Speech frame fits better than the Bell-LaPadula
frame.

### Append-only intent, not mutable data

Spirit records are immutable once stored. The access level is
metadata that may be the only mutable field (or, more cleanly,
later records may RE-CLASSIFY earlier ones). This is unlike
institutional data classification, where records get reviewed,
re-classified, and declassified over decades. Altman's
dynamic-boundary insight applies — the psyche may legitimately
re-classify their own material — but Spirit's mechanism for
re-classification should be additive (new records overlay old
classification) rather than mutating.

### Default-open is correct for THIS data shape

Most Spirit records ARE workspace principles, technical decisions,
architectural Constraints — exactly the material that benefits future
agents / collaborators / open-source contributors. The cost of
defaulting to elevated would be a graveyard of important principles
no future agent can read. Default-open matches the empirical shape
of the corpus.

In contrast, a personal diary might reasonably default to private;
a corporate planning document might reasonably default to internal.
The default choice tracks the DATA SHAPE, and Spirit's shape is
predominantly principle-like, hence default-open.

### Sub-agents inherit but don't escalate

The psyche directive 1448 implies (and the existing Spirit owner-
socket / ordinary-socket split confirms) that SUB-AGENTS inherit
their dispatcher's clearance. Sub-agents do not have independent
authority to access elevated records beyond what their dispatcher
has. This is unlike institutional MAC, where each subject has an
individually assigned clearance.

This simplification serves Spirit well: lane discipline already
encodes which agents do what; the access enum doesn't need to model
each agent's clearance independently.

### Linguistic register — fits with Magnitude + Kind family

The existing Spirit enums:

- **Kind**: Decision / Principle / Correction / Clarification /
  Constraint
- **Magnitude**: Zero / Minimum / VeryLow / Low / Medium / High /
  VeryHigh / Maximum

Kind uses NAMED CONCEPTUAL CATEGORIES (each name picks out a
distinct kind of intent statement). Magnitude uses ORDERED LEVEL
NAMES (each name picks a step on a graduated scale).

The new access enum is closer to Magnitude (ordered, graduated) but
must NOT BE NUMERIC. Naming should match Magnitude's register:
full English words, PascalCase, ordered, ascending, ideally with a
clear ceiling and floor.

## Candidate enum sets

Below are FOUR candidate enum vocabularies. Each names the levels,
defines each, identifies the default, maps to socket model, and lists
pros and cons. The psyche's directive named "public", "personal",
"sensitive", "ultra-personal" as candidate vocabulary — these
candidates RESPOND TO THAT VOCABULARY across different shapes.

### Candidate A — Three-tier minimum (Open / Personal / Sealed)

The minimum-viable model. Three levels matching the most-common
historic count (US, UK governmental, corporate baseline).

| Level | Definition | Triggers elevation | Who can see |
|---|---|---|---|
| **Open** | Default. Workspace principles, design Decisions, technical Constraints. Material intended to inform future agents and collaborators. | (None — the default.) | Ordinary socket + owner socket |
| **Personal** | Personal preferences, project context, work-in-progress thinking, anything the psyche shares with collaborators but not with the world. | The psyche marks it. | Owner socket only (or owner socket with `Personal` filter) |
| **Sealed** | Material the psyche records for self-understanding alone. Vulnerability, deeply personal reflection, work that no other agent should see. | The psyche marks it. | Owner socket with explicit `Sealed` filter only |

**Default**: Open

**Pros**:
- Lowest classification cost per record (only 2 choices beyond
  default).
- Matches the most-replicated tier count across traditions (US, UK,
  corporate baseline).
- Each name carries clear and distinct meaning; no overlap.
- "Sealed" connotes the absolute-floor character of the deepest tier
  in a way that "Confidential" or "Restricted" can't (those words
  are too institutional).
- "Personal" matches the psyche's vocabulary from the directive.

**Cons**:
- May force the psyche to either over-elevate or under-elevate; the
  middle tier carries a lot of weight.
- No room for a mid-tier between "Personal" and "Sealed" — the gap
  is large.
- No room for a sub-default tier like "Internal" (the corporate
  default for "share within team but not externally"). If Spirit
  ever opens to multi-collaborator use, this gap would be felt.

### Candidate B — Four-tier balanced (Open / Personal / Sensitive / Sealed)

The PsyChe's named vocabulary, faithfully. Four levels matching the
enterprise / corporate / NATO sweet spot.

| Level | Definition | Triggers elevation | Who can see |
|---|---|---|---|
| **Open** | Default. Workspace principles, design Decisions, technical Constraints. Material intended to inform future agents and collaborators. | (Default.) | Ordinary socket + owner socket |
| **Personal** | Personal preferences, project context, preferences and work patterns the psyche shares with close collaborators but not with the public. | The psyche marks it. | Owner socket only |
| **Sensitive** | Health observations, family matters, emotional reflections the psyche records for self-understanding and limited sharing with intimates. | The psyche marks it OR a topic-triggered policy elevates it (if Spirit supports per-topic policy — see Open Questions). | Owner socket with `Sensitive` filter |
| **Sealed** | Deeply personal psychological work, vulnerability, contradictions, in-progress thinking that should reach NO ONE except the psyche's own future self. | The psyche marks it. | Owner socket with explicit `Sealed` filter |

**Default**: Open

**Pros**:
- Faithful to the psyche's named vocabulary ("public", "personal",
  "sensitive", "ultra-personal").
- "Sealed" replaces "ultra-personal" with a more native enum-style
  name; "ultra-personal" feels prefix-style ("ultra-") rather than
  PascalCase-noun-style.
- Four tiers match the enterprise SWEET SPOT and NATO count.
- Middle "Sensitive" tier handles the health/emotional/family
  category that's distinct from generic "Personal" but not as
  reserved as "Sealed".
- Maps cleanly to the four-states Westin model (Open ≈ public
  identity, Personal ≈ social reserve, Sensitive ≈ intimacy,
  Sealed ≈ solitude).

**Cons**:
- More tiers means more classification cost per record.
- The Personal / Sensitive line will be fuzzy in practice; the
  psyche will spend cycles deciding which tier fits a given record.
- "Sensitive" is a heavily overloaded word in industry (GDPR
  sensitive categories, sensitive PII) — could create misleading
  associations.

**Spirit-naming-style register**: All names are full English words,
PascalCase, no abbreviations. Fits the Magnitude / Kind family.

### Candidate C — Five-tier graduated (Open / Reserved / Personal / Sensitive / Sealed)

A five-tier model adding a tier between Open and Personal for
material that's not public-by-default but also not really personal
— more like "the psyche's own working notes that aren't principles".

| Level | Definition | Triggers elevation | Who can see |
|---|---|---|---|
| **Open** | Default. Workspace principles, Decisions, Constraints; material designed to inform future agents and collaborators across time. | (Default.) | Ordinary socket + owner socket |
| **Reserved** | Working notes, in-progress thinking, exploratory observations, material that's not principle-like but isn't restricted to the psyche. The "internal-not-public" tier. | The psyche marks it. | Owner socket (default elevation) |
| **Personal** | Personal preferences, project context, work patterns. | The psyche marks it. | Owner socket with `Personal` filter |
| **Sensitive** | Health, family, emotional reflections. | The psyche marks it. | Owner socket with `Sensitive` filter |
| **Sealed** | Deeply personal psychological work, vulnerability, contradictions. | The psyche marks it. | Owner socket with explicit `Sealed` filter |

**Default**: Open

**Pros**:
- Matches the five-tier social media model (Public / Friends / Close
  Friends / Specific friends / Only me).
- Adds a tier ("Reserved") that handles the corporate "Internal"
  default — useful if Spirit ever opens to collaborators.
- Maximum resolution; the psyche can find a tier for almost any
  record.

**Cons**:
- Highest classification cost per record (5 choices).
- The Reserved / Personal line will be hard to draw in practice.
- More tiers = more places to make mistakes = more anxiety per
  record.
- Reserved is the WEAKEST-named tier; doesn't carry obvious meaning
  the way Open / Personal / Sealed do.

### Candidate D — Two-tier with marking (Open + Restricted, plus optional Marking)

A minimum-tier model inspired by GDPR / HIPAA / TLP-with-marking
pattern. Two primary tiers + an optional Marking that gives finer
control without expanding the primary enum.

```
enum Access { Open, Restricted }
enum Marking { Personal, Sensitive, Sealed }
```

Effectively: every record is Open OR Restricted; Restricted records
carry an additional Marking that names WHY they're restricted.

| Access value | Marking values | Definition | Who can see |
|---|---|---|---|
| Open | (none) | Default. Public-shareable material. | Ordinary + owner |
| Restricted | Personal | Project context, preferences. | Owner socket |
| Restricted | Sensitive | Health, family, emotional material. | Owner socket with `Sensitive` filter |
| Restricted | Sealed | Vulnerable, deeply personal. | Owner socket with explicit `Sealed` filter |

**Default**: Open (no marking)

**Pros**:
- Matches GDPR / HIPAA pattern (baseline + enumerated elevation
  categories).
- Two-axis design allows future markings without changing primary
  enum.
- Marking can be MULTIPLE per record (a record about a family
  member's health could carry both Personal and Sensitive).
- Lowest decision cost for most records (just "is this Open or
  Restricted?"); finer detail only when restricting.

**Cons**:
- Two axes means two enum types to design and version.
- Filter language is more complex (must specify access AND marking).
- Doesn't fit Spirit's existing single-enum-per-field pattern as
  cleanly.
- The orthogonal-axis pattern (BLP compartments, TLP markings) works
  well at institutional scale but may be overkill for the personal
  Spirit case.

### Comparison summary

| Aspect | A: 3-tier | B: 4-tier | C: 5-tier | D: 2-tier + marking |
|---|---|---|---|---|
| Levels | 3 | 4 | 5 | 2 (+3 markings) |
| Default | Open | Open | Open | Open (no marking) |
| Faithfulness to psyche vocabulary | Partial | Full | Full + extra | Reframed |
| Decision cost per record | Lowest | Medium | Highest | Lowest for most records |
| Resolution | Coarse | Balanced | Fine | Coarse + orthogonal detail |
| Linguistic style fit (Magnitude family) | Strong | Strong | Weak ("Reserved") | Two-enum complexity |
| Matches modal tradition count | Yes | Yes | Less common | Matches GDPR/HIPAA |
| Future evolution room | Limited | Good | Limited | Excellent |

## Open questions for psyche

The research surfaces these decisions the psyche should make before
implementation lands.

### Q1 — How many tiers? (3, 4, 5, or 2+marking)

The candidate enums above range from 3 (Candidate A) to 5
(Candidate C) plus a 2-tier-with-marking alternative (Candidate D).
The research suggests 4 is the modal count and the enterprise sweet
spot. The 5-tier model adds a "Reserved" tier that may be useful if
Spirit opens to multi-collaborator workflows but adds decision cost.
The 2-tier-with-marking is the most evolution-friendly but adds enum
complexity.

**Research recommendation**: Candidate B (four-tier). Matches the
psyche's named vocabulary, hits the modal count, and balances
decision cost against resolution. But the psyche is the authority on
how much classification overhead they're willing to absorb.

### Q2 — Default level confirmed open?

Per Spirit 1449, the default is the most-public. This is consistent
with every tradition surveyed where there's a meaningful default.
Confirmation: the default level is `Open` (or whatever the most-
public level ends up named). Records created without an explicit
access field get this level.

### Q3 — Level names — risk, depth, or audience register?

The candidate enums all use audience-register names ("Personal",
"Sealed") because Spirit's domain is personal-intent. The alternative
registers:

- **Risk register**: Confidential, Sensitive, Restricted — overstates
  threat; Spirit has no adversary
- **Depth register**: Esoteric, Reserved, Sealed — overstates
  esoteric content; most Spirit records are just principles or
  preferences
- **Audience register**: Open, Personal, Sensitive, Sealed —
  honest about what elevation does (narrows the audience)

**Research recommendation**: audience register. But the psyche
should verify the names FEEL RIGHT — they'll be in every record's
metadata for the life of the workspace.

### Q4 — Is the highest level "Sealed", "UltraPersonal", or
something else?

The psyche's directive named "ultra-personal". The research suggests
"Sealed" because:

- "Sealed" is one word; "UltraPersonal" requires a prefix.
- "Sealed" connotes absolute non-disclosure (seal of confession);
  "UltraPersonal" is graded ("more than Personal").
- "Sealed" fits naming-style register better (matches Magnitude
  enum's single-word PascalCase pattern: Minimum, Maximum, Medium).
- "UltraPersonal" is more accurate to the psyche's stated thought
  ("this is more personal than Personal") if the model is graduated
  depth.

If the psyche prefers graded-depth semantics, "UltraPersonal" is
fine. If the psyche prefers absolute-floor semantics, "Sealed" is
better. The research weakly recommends "Sealed".

### Q5 — Topic-triggered automatic elevation?

The directive doesn't say whether per-record access should be:

a. EXPLICIT ONLY — psyche specifies the field on every record; no
   automatic elevation
b. TOPIC-TRIGGERED — records on certain topics (e.g., "health",
   "family") automatically elevate to Sensitive unless explicitly
   marked Open

Option (a) is simpler but burdens the psyche to remember elevation
on every sensitive record. Option (b) is safer (forgetting to
classify a health record doesn't expose it) but requires a topic-to-
default-access mapping and may surprise the psyche when an Open
intent gets silently elevated.

**Research recommendation**: start with (a) — explicit-only — for
simplicity and predictability. Add (b) as a later evolution if the
explicit model proves error-prone.

### Q6 — Sub-agent clearance inheritance

Confirmed by Spirit 1448's framing: sub-agents inherit the
dispatcher's socket / clearance. A sub-agent dispatched by a
designer (typically running through the owner socket) inherits owner-
socket clearance. A sub-agent dispatched by an agent on the ordinary
socket inherits ordinary-socket clearance only. This matches the
existing lane-discipline rule (sub-agents inherit the dispatcher's
lane) and needs no special mechanism in the access enum itself.

But: the sub-agent's `AccessSelection` FILTER must be set
EXPLICITLY in their queries to reach elevated records, even if their
clearance allows it. Owner-clearance + default filter = Open records
only. To reach Personal records, the sub-agent must explicitly
request access to Personal. This default-conservative behavior
prevents accidental exposure when the sub-agent doesn't need
elevated material.

### Q7 — Reclassification after creation

Altman's dynamic-boundary insight argues that records should be
RECLASSIFIABLE. If Spirit records are append-only, the cleanest
mechanism is:

- A later record can RE-CLASSIFY an earlier one (a new Spirit record
  of Kind=Constraint pointing at the older record's ID and asserting
  a new access level).
- The daemon applies the latest re-classification when filtering.

This preserves Spirit's append-only character while supporting
re-classification. Alternative: the access field is the one mutable
field on the record. This is simpler operationally but breaks the
append-only invariant.

**Research recommendation**: support reclassification via new records
(append-only preserved). But this is a downstream mechanism design
question, not part of the enum vocabulary.

### Q8 — Multiple-marking semantics (Candidate D only)

If the psyche prefers Candidate D (two-tier + marking), then the
markings might be SINGLE (one marking per record) or MULTIPLE
(multiple markings per record). GDPR Article 9 allows multiple
categories per record (a record about a family member's health
genetic data carries Health + Genetic + Family categories
simultaneously). For Spirit, multiple-marking is more flexible but
the filter language is harder.

Only relevant if Candidate D is selected.

## Sources

### Government / military classification

- Wikipedia. "Classified information in the United States." https://en.wikipedia.org/wiki/Classified_information_in_the_United_States
- Federation of American Scientists. "An Introduction to the Security and Classification System." https://sgp.fas.org/classdod.htm
- Electrospaces. "The US Classification System." 2013. https://www.electrospaces.net/2013/09/the-us-classification-system.html
- Wikipedia. "Government Security Classifications Policy." https://en.wikipedia.org/wiki/Government_Security_Classifications_Policy
- GOV.UK. "Government Security Classifications." https://www.gov.uk/government/publications/government-security-classifications
- UK Ministry of Justice. "Government Classification Scheme." https://security-guidance.service.justice.gov.uk/government-classification-scheme/
- US Marines. "NATO Security Briefing." https://www.information.marines.mil/Portals/224/Docs/Newcomers/NATO-Security-Briefing.pdf
- Wikipedia. "Classified information." https://en.wikipedia.org/wiki/Classified_information
- US National Archives. "CUI Category: NATO Restricted." https://www.archives.gov/cui/registry/category-detail/nota-restricted.html

### Academic privacy taxonomies

- Solove, Daniel J. "A Taxonomy of Privacy." University of Pennsylvania Law Review 154 (2006): 477. SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=667622
- Open Rights Group Wiki. "A Taxonomy of Privacy." https://wiki.openrightsgroup.org/wiki/A_Taxonomy_of_Privacy
- TeachPrivacy. "A Taxonomy of Privacy." https://teachprivacy.com/taxonomy-of-privacy/
- Wikipedia. "Contextual integrity." https://en.wikipedia.org/wiki/Contextual_integrity
- Nissenbaum, Helen. "Privacy as Contextual Integrity." Washington Law Review. https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/
- Bridging Barriers. "Interview with Helen Nissenbaum." https://bridgingbarriers.utexas.edu/news/people-conflate-privacy-secrecy-interview-good-systems-symposium-keynote-speaker-helen
- Olsson, Marcus. "Westin's four states of privacy." https://marcusolsson.dev/four-states-of-privacy/
- IAPP. "Alan Westin's Legacy of Privacy and Freedom." https://iapp.org/news/a/alan-westins-legacy-of-privacy-and-freedom
- Hacking with Care. "Psychological functions of privacy." https://hackingwithcare.in/2014/04/psychological-functions-of-privacy-one-academic-literature-review/
- Wikipedia. "Privacy regulation theory." https://en.wikipedia.org/wiki/Privacy_regulation_theory
- Palen, Leysia. "Unpacking 'Privacy' for a Networked World." University of Colorado. https://cmci.colorado.edu/~palen/palen_papers/palen-privacy.pdf

### Legal / regulatory classification

- GDPR-Text.com. "Article 9 GDPR — Processing of special categories of personal data." https://gdpr-text.com/read/article-9/
- UK Information Commissioner's Office. "Special category data." https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/a-guide-to-lawful-basis/special-category-data/
- GDPRInfo. "GDPR Article 10 Explained: Criminal Convictions and Offences." https://gdprinfo.eu/gdpr-article-10-explained-processing-personal-data-relating-to-criminal-convictions-and-offences
- UC Berkeley. "HIPAA PHI: Definition of PHI and List of 18 Identifiers." https://cphs.berkeley.edu/hipaa/hipaa18.html
- HIPAA Journal. "Psychotherapy Notes and HIPAA." https://www.hipaajournal.com/psychotherapy-notes-and-hipaa/
- Accountable. "Psychotherapy Notes & HIPAA." https://www.accountablehq.com/post/psychotherapy-notes-hipaa
- California Office of the Attorney General. "California Consumer Privacy Act (CCPA)." https://oag.ca.gov/privacy/ccpa
- Akin. "California Expands Definition of Sensitive Personal Information." https://www.akingump.com/en/insights/blogs/ag-data-dive/california-expands-definition-of-sensitive-personal-information-covered-under-ccpa
- Bastion. "CCPA Sensitive Personal Information." https://bastion.tech/learn/ccpa/sensitive-personal-information
- NIST. "PII Glossary." https://csrc.nist.gov/glossary/term/PII
- Lepide. "What Is Personally Identifiable Information (PII)?" https://www.lepide.com/cyber-learning/what-is-personally-identifiable-information-pii/
- Concentric. "Comparing SPII vs PHI and PII." https://concentric.ai/comparing-spii-vs-phi-and-pii-a-sensitive-information-guide/

### Access control models

- Wikipedia. "Bell-LaPadula model." https://en.wikipedia.org/wiki/Bell%E2%80%93LaPadula_model
- Binaryte. "Bell-LaPadula Model: A MAC Model for Achieving Multi-level Security." https://binaryte.com/blog/post/bell-lapadula-model-a-mac-model-for-achieving-multi-level-security.md/
- Wikipedia. "Biba Model." https://en.wikipedia.org/wiki/Biba_Model
- SHK Corp. "Access Control Models: RBAC vs ABAC vs DAC vs MAC." https://www.shkcorp.com/blog/access-control-models
- TechPrescient. "Types of Access Control: DAC, MAC, RBAC, ABAC." https://www.techprescient.com/blogs/types-of-access-control/
- Wikipedia. "Capability-based security." https://en.wikipedia.org/wiki/Capability-based_security
- Wikipedia. "Object-capability model." https://en.wikipedia.org/wiki/Object-capability_model
- FIRST. "Traffic Light Protocol (TLP)." https://www.first.org/tlp/
- CISA. "Traffic Light Protocol (TLP) Definitions and Usage." https://www.cisa.gov/news-events/news/traffic-light-protocol-tlp-definitions-and-usage
- Palo Alto Networks. "TLP Update (2.0), Going Softer on AMBER and Adding AMBER+STRICT." https://live.paloaltonetworks.com/t5/community-blogs/tlp-update-2-0-going-softer-on-amber-and-adding-amber-strict/ba-p/530512
- Fortra. "Data Classification Levels Explained." https://www.fortra.com/blog/data-classification-levels-explained-enhance-data-security
- Microsoft. "Data classification & sensitivity label taxonomy." https://learn.microsoft.com/en-us/compliance/assurance/assurance-data-classification-and-labels

### Social / personal privacy practice

- Wikipedia. "The Diary of Anaïs Nin." https://en.wikipedia.org/wiki/The_Diary_of_Ana%C3%AFs_Nin
- History Today. "The Hidden Diary of Samuel Pepys." https://www.historytoday.com/archive/feature/hidden-diary-samuel-pepys
- Cambridge University Press. "The Strange History of Samuel Pepys's Diary: Shorthand and Secrecy." https://www.cambridge.org/core/books/strange-history-of-samuel-pepyss-diary/shorthand-and-secrecy/BDDE07A4B4646E1083E5A4E63ECAE32C
- Wikipedia. "Franz Kafka's Diaries." https://en.wikipedia.org/wiki/Franz_Kafka's_Diaries
- Literary Hub. "Kafka's Last Wish, Brod's First Betrayal." https://lithub.com/kafkas-last-wish-brods-first-betrayal/
- Thinglabs. "Controlling Your Privacy on Facebook: Only Me, Settings, FAQs." https://thinglabs.io/facebook-only-me-post
- Bobology. "Facebook's Audience Selector." https://www.bobology.com/public/Facebooks-Audience-Selector-Choose-Who-Sees-a-Post.cfm
- ICANotes. "Psychotherapy Notes vs Progress Notes." https://www.icanotes.com/2018/06/08/the-differences-between-psychotherapy-notes-and-progress-notes/
- Upheal. "Psychotherapy notes vs. progress notes." https://www.upheal.io/documentation/psychotherapy-notes-vs-progress-notes

### Contemplative / spiritual disclosure

- Wannabe Poet. "Right Speech in the Pali Canon." https://wannabepoet.com/2022/05/11/right-speech-in-the-pali-canon/
- Zen Studies Podcast. "Buddha's Teachings: Right Speech." https://zenstudiespodcast.com/right-speech/
- Yaqeen Institute. "Etiquette as Spiritual Nourishment: The Adab of the Student." https://yaqeeninstitute.org/read/post/etiquette-as-spiritual-nourishment-the-adab-of-the-student-according-to-al-ghazali-and-al-isfahani
- Golden Sufi Center. "Adab — Sufi Etiquette in the Outer and Inner Worlds." https://goldensufi.org/article/adab-sufi-etiquette-in-the-outer-and-inner-worlds/
- Wikipedia. "Pardes (exegesis)." https://en.wikipedia.org/wiki/Pardes_(exegesis)
- Hidden Orchard. "PaRDeS — Jewish Hermeneutics." https://www.thehiddenorchard.com/peshat-pardes/
- Wikipedia. "Pseudo-Dionysius the Areopagite." https://en.wikipedia.org/wiki/Pseudo-Dionysius_the_Areopagite
- Stanford Encyclopedia of Philosophy. "Pseudo-Dionysius the Areopagite." https://plato.stanford.edu/entries/pseudo-dionysius-areopagite/
- Wikipedia. "Seal of confession in the Catholic Church." https://en.wikipedia.org/wiki/Seal_of_confession_in_the_Catholic_Church
- Catholic Times. "Priests are bound to secrecy by seal of confessional." https://catholictimescolumbus.org/news/priests-are-bound-to-secrecy-by-seal-of-confessional/
- Sacred Ancestry. "Mystery Schools and Initiatic Orders." https://www.sacredancestry.com/blog/mystery-schools-amp-initiatic-orders
