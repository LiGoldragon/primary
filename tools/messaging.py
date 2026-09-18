#!/usr/bin/env python3
"""Typed Datom boundary and relay envelope for the shell messenger."""
from __future__ import annotations
import datetime as dt
import json
import pathlib
import re
import sys
import uuid
from dataclasses import dataclass

class ParseError(ValueError): pass
@dataclass(frozen=True)
class Bare: value: str
@dataclass(frozen=True)
class Text: value: str
@dataclass(frozen=True)
class Group: kind: str; values: tuple
@dataclass(frozen=True)
class Variant: head: str; body: object

class Reader:
 def __init__(self,s): self.s=s; self.i=0
 def ws(self):
  while self.i<len(self.s) and self.s[self.i].isspace(): self.i+=1
 def read(self):
  self.ws(); x=self.value(); self.ws()
  if self.i!=len(self.s): raise ParseError('trailing Datom input')
  return x
 def value(self):
  self.ws()
  if self.i>=len(self.s): raise ParseError('expected Datom value')
  c=self.s[self.i]
  if c in '{[':
   end='}' if c=='{' else ']'; self.i+=1; out=[]
   while True:
    self.ws()
    if self.i>=len(self.s): raise ParseError('unclosed Datom enclosure')
    if self.s[self.i]==end: self.i+=1; return Group(c,tuple(out))
    out.append(self.value())
  if c=='«':
   self.i+=1; out=[]
   while self.i<len(self.s):
    c=self.s[self.i]; self.i+=1
    if c=='»': return Text(''.join(out))
    if c=='\\':
     if self.i>=len(self.s): raise ParseError('unfinished string escape')
     escaped=self.s[self.i]; self.i+=1
     out.append(escaped if escaped in {'\\','»'} else '\\'+escaped)
    else: out.append(c)
   raise ParseError('unclosed Datom string')
  m=re.match(r'[A-Za-z][A-Za-z0-9_-]*',self.s[self.i:])
  if not m: raise ParseError('invalid Datom bare')
  head=m.group(); self.i+=len(head); self.ws()
  if self.s[self.i:self.i+1]=='.':
   self.i+=1; return Variant(head,self.value())
  return Bare(head)

def actualize(text): return Reader(text).read()
def _bare(x,name):
 if not isinstance(x,Bare) or not x.value: raise ParseError('expected '+name)
 return x.value
def relay(text):
 root=actualize(text)
 if not isinstance(root,Variant) or root.head not in {'MACHINE','LIVING'}: raise ParseError('producer must be MACHINE or LIVING')
 if root.head != 'MACHINE': raise ParseError('terminal ingress accepts MACHINE only')
 body=root.body
 if not isinstance(body,Variant) or body.head!='Relay' or not isinstance(body.body,Group) or body.body.kind!='{' or len(body.body.values)!=7: raise ParseError('expected MACHINE.Relay.{ from seat heard mode [recipients] quote context }')
 frm,seat,heard,mode,recips,quote,context=body.body.values
 frm,seat,mode=(_bare(frm,'from'),_bare(seat,'seat'),_bare(mode,'mode'))
 if not isinstance(heard,Text): raise ParseError('heard must be Datom string')
 heard=heard.value
 if mode not in {'typed','stt','unknown'}: raise ParseError('invalid mode')
 try: dt.datetime.fromisoformat(heard.replace('Z','+00:00'))
 except ValueError: raise ParseError('heard must be ISO timestamp')
 if not isinstance(recips,Group) or recips.kind!='[': raise ParseError('recipients must be vector')
 recipients=[_bare(x,'recipient') for x in recips.values]
 if not recipients or frm in recipients: raise ParseError('invalid recipients')
 if not isinstance(quote,Text) or not isinstance(context,Text): raise ParseError('quote and context must be Datom strings')
 return {'producer':'MACHINE','from':frm,'seat':seat,'heard':heard,'mode':mode,'recipients':recipients,'quote':quote.value,'context':context.value}
def q(s): return '«'+s.replace('\\','\\\\').replace('»','\\»')+'»'
def make_machine(frm,seat,recipient,payload):
 actualize(payload)
 heard=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
 # Datom bares cannot carry ISO punctuation; the timestamp is a string while
 # identity and routing positions remain structural bares.
 return f'MACHINE.Relay.{{ {frm} {seat} {q(heard)} unknown [ {recipient} ] {q(payload)} {q("")} }}'

# The ledger is an append-only local evidence file. Queue items are never
# rewritten into a different message; attempts reference the original event.
class Ledger:
 def __init__(self,path):
  self.path=pathlib.Path(path)
  try: self.data=json.loads(self.path.read_text())
  except FileNotFoundError: self.data={'version':1,'queue':[],'events':[],'attempts':[]}
 def _id(self): return str(uuid.uuid4())
 def _save(self):
  self.path.parent.mkdir(parents=True,exist_ok=True); tmp=self.path.with_suffix('.tmp'); tmp.write_text(json.dumps(self.data,sort_keys=True,separators=(',',':'))+'\n'); tmp.replace(self.path)
 def _event(self,kind,detail):
  e={'id':self._id(),'at':dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'kind':kind,'detail':detail}; self.data['events'].append(e); return e
 def enqueue(self,event):
  if len(self.data['queue']) >= 10:
   notice=self._event('backpressure',{'pending':len(self.data['queue'])}); self._save(); return {'accepted':False,'notice':notice}
  item={'id':self._id(),'event':event}; self.data['queue'].append(item); self._event('queued',{'queue_id':item['id'],'relay':event}); self._save(); return {'accepted':True,'queue_id':item['id']}
 def attempt(self,queue_id,binding,transport):
  item=next((x for x in self.data['queue'] if x['id']==queue_id),None)
  if item is None: raise KeyError(queue_id)
  a={'id':self._id(),'at':dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'queue_id':queue_id,'binding':binding,'grade':'Transported' if transport else 'Submitted','outcome':'transported' if transport else 'held'}
  self.data['attempts'].append(a); self._event('attempt',a); self._save(); return a
 def acknowledge(self,queue_id):
  # Explicit acknowledgement is the only dequeue. A failed delivery stays FIFO.
  if not self.data['queue'] or self.data['queue'][0]['id'] != queue_id: raise ValueError('only FIFO head may be acknowledged')
  self.data['queue'].pop(0); self._event('acknowledged',{'queue_id':queue_id}); self._save()
def main():
 if sys.argv[1]=='validate': print(json.dumps(relay(sys.stdin.read()),separators=(',',':')))
 elif sys.argv[1]=='machine': print(make_machine(*sys.argv[2:]))
 else: raise SystemExit(2)
if __name__=='__main__': main()
