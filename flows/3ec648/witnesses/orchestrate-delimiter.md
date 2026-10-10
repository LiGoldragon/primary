# Orchestrate client string delimiter

## Method
Client: /home/li/.nix-profile/bin/orchestrate. Lock name Probe3ec648, FlowId 3ec648,
path /home/li/primary/flows/3ec648/witnesses. Each obtained lock released at once
(11422, 11423 released; none held now). Source read at /git/github.com/LiGoldragon/
orchestrate (rev 9070cbb), protos, datom-codec.

Note: the bare probe was first run while the guillemet lock was still held, so it
was rejected as a duplicate name; I released and reran it. Both replies are given.

## Replies (verbatim)
1. Guillemets, `Lock.{ Probe3ec648 3ec648 [ P ] «two words» }`:
   `Locked.{ 11422 Probe3ec648 3ec648 [ /home/li/primary/flows/3ec648/witnesses ] «two words» }` (exit 0)
2. Curly quotes, `“two words”`:
   `Unreadable.Error.{ Composition [ 1 ] Arity.{ 4 5 } }` (exit 1)
3. Bare, `oneword`:
   first run (guillemet lock still held): `LockRejected.DuplicateName.{ 11422 Probe3ec648 3ec648 [ /home/li/primary/flows/3ec648/witnesses ] «two words» }` (exit 0)
   rerun after release: `Locked.{ 11423 Probe3ec648 3ec648 [ /home/li/primary/flows/3ec648/witnesses ] oneword }` (exit 0)
4. ASCII double quotes, `"two words"`:
   `Unreadable.Error.{ Composition [ 1 ] Arity.{ 4 5 } }` (exit 1)
Releases: `Released.{ 11422 ... «two words» }`, `Released.{ 11423 ... oneword }`.

## Source
- protos/src/core.rs: `Boundary` has only Guillemets («») and Parentheses (()); the
  parser opens an opaque only at `«` or `(`. No curly-quote glyph anywhere.
- orchestrate/AGENTS.md lines 29-34: strings with space or delimiter go in guillemets;
  curly quotes belonged to an earlier Protos generation and are refused; the curly
  Lock reason yields exactly `Unreadable.Error.{ Composition [ 1 ] Arity.{ 4 5 } }`.
- orchestrate/UPGRADES.md lines 245-256: since 0.31.0 guillemets; deployed 0.30.0
  accepted curly; says the `orchestrate` skill outside the repo needs the same fix.
- The error is an arity error because the unrecognised quotes split the reason into
  two bare words (fifth position).

## Contradiction
The orchestrate skill (`.claude/skills/orchestrate/SKILL.md`: "written in Datom curly
quotes, “like this”; ASCII double quotes are not Datom string delimiters" and its
`“Clarify Lock fields”` example) is contradicted by the running client. The datom
and protos skills agree with the client.
