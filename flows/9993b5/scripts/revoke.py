import pathlib, sys
p = pathlib.Path("/tmp/9993b5-work/base.md")
s = p.read_text()
anchor = "The embedded efa157 log's 08:2xZ correction describes the former stock base,\nwhich this base replaces; it is historical evidence, not a contrary rule."
insert = (
    "\n\nRevocation, on the living's direct order of 2026-09-17: the "
    "'a concluded flow is not reawakened' line in the main-flow skill body "
    "below (Flow refresh section), and any wording anywhere in this base "
    "that holds a flow back from restarting itself, are revoked. A flow "
    "may restart itself, and Fable may restart flows in its lineage, with "
    "authority. This revocation is in the base header and outranks the skill "
    "body per the precedence rule immediately above."
)
if anchor not in s:
    print("ANCHOR NOT FOUND"); sys.exit(1)
p.write_text(s.replace(anchor, anchor + insert))
print("REVOKED, new size", p.stat().st_size)
