#!/usr/bin/env python3
"""Typed Datom boundary and relay envelope for the shell messenger."""
from __future__ import annotations
import datetime as dt
import hashlib
import os
import fcntl
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
  start=self.i
  while self.i<len(self.s) and not self.s[self.i].isspace() and self.s[self.i] not in '{}[]«».' : self.i+=1
  bare=self.s[start:self.i]
  if not bare: raise ParseError('invalid Datom bare')
  if self.s[self.i:self.i+1]=='.':
   if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',bare): raise ParseError('invalid Datom variant head')
   self.i+=1; return Variant(bare,self.value())
  return Bare(bare)

def actualize(text): return Reader(text).read()
def _bare(x,name):
 if not isinstance(x,Bare) or not x.value: raise ParseError('expected '+name)
 return x.value
def relay(text):
 root=actualize(text)
 if not isinstance(root,Variant) or root.head not in {'Machine','Living'}: raise ParseError('producer must be Machine or Living')
 if root.head != 'Machine': raise ParseError('terminal ingress accepts Machine only')
 body=root.body
 if not isinstance(body,Variant) or body.head!='Relay' or not isinstance(body.body,Group) or body.body.kind!='{' or len(body.body.values)!=8: raise ParseError('expected Machine.Relay.{ ingress from seat heard mode [recipients] quote context }')
 ingress,frm,seat,heard,mode,recips,quote,context=body.body.values
 ingress=_bare(ingress,'ingress_id')
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
 return {'producer':'Machine','ingress_id':ingress,'from':frm,'seat':seat,'heard':heard,'mode':mode,'recipients':recipients,'quote':quote.value,'context':context.value}
def q(s): return '«'+s.replace('\\','\\\\').replace('»','\\»')+'»'
def make_machine(frm,seat,recipient,payload,ingress_id=None):
 heard=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
 # Datom bares cannot carry ISO punctuation; the timestamp is a string while
 # identity and routing positions remain structural bares.
 ingress_id=ingress_id or ('e'+uuid.uuid4().hex)
 return f'Machine.Relay.{{ {ingress_id} {frm} {seat} {q(heard)} unknown [ {recipient} ] {q(payload)} {q("")} }}'
def make_psyche_poc(request_id, flow_id, recipient, verbatim, ingress_id=None):
 heard=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
 ingress_id=ingress_id or ('p'+uuid.uuid4().hex)
 # This is a source-accepted POC statement, not a browser or human identity.
 return f'Mentci.PsycheIngress.{{ {ingress_id} {request_id} {flow_id} {q(heard)} [ {recipient} ] {q(verbatim)} }}'

# The ledger is an append-only local evidence file. Queue items are never
# rewritten into a different message; attempts reference the original event.
class Ledger:
 def __init__(self,path):
  self.path=pathlib.Path(path)
  self.path.parent.mkdir(parents=True,exist_ok=True)
  # Each CLI ledger operation holds this advisory lock for its complete
  # read/modify/write transaction.  This prevents two messenger processes from
  # producing conflicting snapshots of immutable ingress evidence.
  self._lock=open(self.path.with_suffix(self.path.suffix+'.lock'),'a+')
  fcntl.flock(self._lock.fileno(), fcntl.LOCK_EX)
  try: self.data=json.loads(self.path.read_text())
  except FileNotFoundError: self.data={'version':1,'queue':[],'events':[],'attempts':[],'ingress':{}}
  self.data.setdefault('ingress',{})
 def close(self):
  if not self._lock.closed: fcntl.flock(self._lock.fileno(), fcntl.LOCK_UN); self._lock.close()
 def __del__(self):
  try: self.close()
  except Exception: pass
 def _id(self): return str(uuid.uuid4())
 def _save(self):
  self.path.parent.mkdir(parents=True,exist_ok=True)
  tmp=self.path.with_suffix('.tmp')
  payload=json.dumps(self.data,sort_keys=True,separators=(',',':'))+'\n'
  with open(tmp,'w') as out:
   out.write(payload); out.flush(); os.fsync(out.fileno())
  os.replace(tmp,self.path)
  # Persist the rename itself, rather than merely the replacement file.
  directory=os.open(str(self.path.parent),os.O_RDONLY)
  try: os.fsync(directory)
  finally: os.close(directory)
 def _event(self,kind,detail):
  e={'id':self._id(),'at':dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'kind':kind,'detail':detail}; self.data['events'].append(e); return e
 def _fingerprint(self,event): return hashlib.sha256(json.dumps(event,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 def lookup(self,event):
  ingress=event.get('ingress_id')
  if not ingress: return {'accepted':False,'unidentified':True}
  known=self.data['ingress'].get(ingress)
  if not known: return {'accepted':True}
  if known['fingerprint'] != self._fingerprint(event):
   self._event('ingress-conflict',{'ingress_id':ingress,'existing_queue_id':known['queue_id']}); self._save()
   return {'accepted':False,'conflict':True,'queue_id':known['queue_id']}
  return {'accepted':False,'duplicate':True,'queue_id':known['queue_id'],'state':known.get('state','queued')}
 def enqueue(self,event):
  status=self.lookup(event)
  if not status.get('accepted'): return status
  ingress=event['ingress_id']; fingerprint=self._fingerprint(event)
  if len(self.data['queue']) >= 10:
   notice=self._event('held-backpressure',{'pending':len(self.data['queue']),'relay':event}); self._save(); return {'accepted':False,'notice':notice}
  item={'id':self._id(),'ingress_id':ingress,'fingerprint':fingerprint,'event':event}; self.data['queue'].append(item)
  self.data['ingress'][ingress]={'fingerprint':fingerprint,'queue_id':item['id'],'state':'queued'}
  self._event('queued',{'queue_id':item['id'],'relay':event}); self._save(); return {'accepted':True,'queue_id':item['id']}
 def attempt(self,queue_id,binding,transport):
  item=next((x for x in self.data['queue'] if x['id']==queue_id),None)
  if item is None: raise KeyError(queue_id)
  a=next((x for x in reversed(self.data['attempts']) if x['queue_id']==queue_id and x['outcome']=='attempt_started'),None)
  if a is None: a={'id':self._id(),'at':dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'queue_id':queue_id,'binding':binding}; self.data['attempts'].append(a)
  a.update({'binding':binding,'grade':'Transported' if transport else None,'outcome':'transported' if transport else 'transport_failed'})
  self._event('attempt',a); self._save(); return a
 def attempt_started(self,queue_id,binding):
  a={'id':self._id(),'at':dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'queue_id':queue_id,'binding':binding,'grade':None,'outcome':'attempt_started'}; self.data['attempts'].append(a); self._event('attempt_started',a); self._save(); return a
 def recover(self):
  for a in self.data['attempts']:
   if a['outcome']=='attempt_started':
    a['outcome']='uncertain_crash'; self._event('uncertain_crash',a)
    item=next((x for x in self.data['queue'] if x['id']==a['queue_id']),None)
    if item and item['ingress_id'] in self.data['ingress']: self.data['ingress'][item['ingress_id']]['state']='uncertain_crash'
  self._save()
 def acknowledge(self,queue_id):
  # Explicit acknowledgement is the only dequeue. A failed delivery stays FIFO.
  if not self.data['queue'] or self.data['queue'][0]['id'] != queue_id: raise ValueError('only FIFO head may be acknowledged')
  item=self.data['queue'].pop(0)
  if item['ingress_id'] in self.data['ingress']: self.data['ingress'][item['ingress_id']]['state']='acknowledged'
  self._event('acknowledged',{'queue_id':queue_id}); self._save()

def main():
 if sys.argv[1]=='validate': print(json.dumps(relay(sys.stdin.read()),separators=(',',':')))
 elif sys.argv[1]=='machine': print(make_machine(*sys.argv[2:]))
 elif sys.argv[1]=='psyche-poc': print(make_psyche_poc(*sys.argv[2:]))
 elif sys.argv[1]=='ledger-lookup': print(json.dumps(Ledger(sys.argv[2]).lookup(json.loads(sys.argv[3])),separators=(',',':')))
 elif sys.argv[1]=='ledger-enqueue': print(json.dumps(Ledger(sys.argv[2]).enqueue(json.loads(sys.argv[3])),separators=(',',':')))
 elif sys.argv[1]=='ledger-attempt': print(json.dumps(Ledger(sys.argv[2]).attempt(sys.argv[3],json.loads(sys.argv[4]),sys.argv[5]=='transported'),separators=(',',':')))
 elif sys.argv[1]=='ledger-start': print(json.dumps(Ledger(sys.argv[2]).attempt_started(sys.argv[3],json.loads(sys.argv[4])),separators=(',',':')))
 elif sys.argv[1]=='ledger-recover': Ledger(sys.argv[2]).recover()
 elif sys.argv[1]=='ledger-ack': Ledger(sys.argv[2]).acknowledge(sys.argv[3])
 elif sys.argv[1]=='ledger-pending': print(len(Ledger(sys.argv[2]).data['queue']))
 else: raise SystemExit(2)
if __name__=='__main__': main()
