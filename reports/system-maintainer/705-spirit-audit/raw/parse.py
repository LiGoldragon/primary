#!/usr/bin/env python3
"""Parse a spirit `RecordsStashed` NOTA dump into per-record JSON.

NOTA `[...]` is overloaded: a VECTOR of values, or a delimited STRING.
Disambiguation is by schema position, so this parser is type-directed for
the known positional Entry schema:
  stash  = (RecordsStashed (handle count records))
  records= [ record* ]
  record = (id entry)
  entry  = (domains Kind desc Certainty Importance Privacy referents)
Only `desc` is a free-text string; domains/referents are vectors; the
ladder fields are atoms. `[|...|]` is a bracket-safe string anywhere.
"""
import json, sys
from collections import Counter

class P:
    def __init__(self, s):
        self.s = s; self.i = 0; self.n = len(s)
    def ws(self):
        while self.i < self.n and self.s[self.i] in ' \t\n\r':
            self.i += 1
    def expect(self, c):
        self.ws()
        if self.s[self.i] != c:
            raise ValueError(f"want {c!r} at {self.i}: {self.s[self.i:self.i+40]!r}")
        self.i += 1
    def peek(self):
        self.ws(); return self.s[self.i]
    def atom(self):
        self.ws(); start = self.i
        while self.i < self.n and self.s[self.i] not in ' \t\n\r()[]':
            self.i += 1
        return self.s[start:self.i]
    def string(self):
        """free-text string at a known string position: [text] or [|text|].
        Bracket-safe form ends at the first UNescaped |] ; \\ escapes next char."""
        self.ws()
        assert self.s[self.i] == '[', self.s[self.i:self.i+10]
        if self.s[self.i+1] == '|':
            self.i += 2; start = self.i
            while self.i < self.n:
                c = self.s[self.i]
                if c == '\\':
                    self.i += 2; continue
                if c == '|' and self.s[self.i+1:self.i+2] == ']':
                    val = self.s[start:self.i]; self.i += 2; return val
                self.i += 1
            raise ValueError("unterminated [|")
        # plain [text]: no brackets inside by NOTA rule
        self.i += 1; j = self.s.find(']', self.i)
        val = self.s[self.i:j]; self.i = j+1; return val
    def value(self):
        """generic NOTA value: ( list ), [ vector ], [|string|], or atom"""
        c = self.peek()
        if c == '(':
            self.i += 1; out = []
            while self.peek() != ')':
                out.append(self.value())
            self.i += 1; return out
        if c == '[':
            if self.s[self.i+1] == '|':
                return {'s': self.string()}
            self.i += 1; out = []
            while self.peek() != ']':
                out.append(self.value())
            self.i += 1; return out
        return self.atom()
    def domain(self, node):
        parts = []
        def walk(x):
            if isinstance(x, list):
                for e in x: walk(e)
            else: parts.append(x)
        walk(node); return '.'.join(parts)
    def parse(self):
        self.expect('('); head = self.atom(); assert head == 'RecordsStashed', head
        self.expect('('); handle = self.atom(); count = self.atom()
        # records vector
        self.expect('[')
        recs = []
        while self.peek() != ']':
            self.expect('('); rid = self.atom()
            self.expect('(')
            domains = self.value()              # vector
            kind = self.atom()
            desc = self.string()                # free text
            certainty = self.atom()
            importance = self.atom()
            privacy = self.atom()
            referents = self.value()            # vector
            self.expect(')')                    # close entry
            self.expect(')')                    # close record
            recs.append({
                'id': rid,
                'domains': [self.domain(d) for d in domains],
                'kind': kind, 'desc': desc,
                'certainty': certainty, 'importance': importance,
                'privacy': privacy,
                'referents': [r if isinstance(r,str) else r.get('s','?') for r in referents],
            })
        return int(count), recs

count, recs = P(open(sys.argv[1]).read()).parse()
json.dump(recs, open(sys.argv[2], 'w'), indent=0)
print(f"declared={count} parsed={len(recs)}  MATCH={count==len(recs)}")
print("kinds:", dict(Counter(r['kind'] for r in recs)))
print("certainty:", dict(Counter(r['certainty'] for r in recs)))
print("importance:", dict(Counter(r['importance'] for r in recs)))
dl = [len(r['desc']) for r in recs]
print(f"desc chars: total={sum(dl)} avg={sum(dl)//len(dl)} max={max(dl)} min={min(dl)}")
refless = sum(1 for r in recs if not r['referents'])
print(f"records with NO referents: {refless} ({100*refless//len(recs)}%)")
