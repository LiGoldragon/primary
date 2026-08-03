# Spirit surface-removal design rulings

## 2026-08-03 — destructive live-schema migration

Agent text answered: design the clean breaking removal of certainty, privacy,
and referents from Spirit, including exact replacement semantics, live storage
migration, compatibility, ordering, testing, activation, and rollback.

Psyche ruling: the migrated database discards the corresponding data. Retain
record identity and substance while dropping certainty and privacy fields and
indexes; delete all referent data. Do not retain a compatibility shadow or
archive inside the new database. Keep only a private pre-migration backup for
rollback.

## 2026-08-03 — remove the concepts

Agent text answered: no verbatim agent text accompanied this ruling in the
dispatch. The design context was whether certainty, privacy, and referents
remain anywhere in Spirit's active architecture.

Exact psyche ruling: “I want certainty, privacy and referents gone”.

## 2026-08-03 — discard their migrated data

Agent text answered: define what happens to the corresponding certainty,
privacy, and referent data while migrating the live database to the new schema.

Exact psyche ruling: “just throw the corresponding data out of the migrated
database.”

Clean discard semantics: the new database preserves each surviving record's
identity and substance, omits certainty and privacy fields and indexes, and
contains no referent rows, indexes, aliases, compatibility tables, or embedded
archive. A private pre-migration database backup is rollback material only and
is not part of the new schema or runtime compatibility surface.
