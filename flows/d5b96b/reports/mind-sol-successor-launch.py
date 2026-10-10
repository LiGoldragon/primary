#!/usr/bin/env python3
import hashlib, os, sys
from pathlib import Path
SOURCE=Path('/tmp/mind-sol-successor-reparse.md')
SHA='f4bfb376339aa154496e6f66f939625efb648737c065d5bf00e01bc5575da46a'
WRAPPER='/nix/store/nmr4py6p0kwwza41l0gkhsa13k9971jb-codex-next-flow-client/bin/codex-next-flow-client'
REMOTE='unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock'
CONTEXT='''You are a fresh independent Mind Sol successor, not a native-session transfer. The entire immutable reparse follows. Use gpt-6.1-sol medium on the explicit candidate remote. Establish your own Flow lane, log, and index before registration. Your first task is a meaningful handoff reconciliation and concrete next-action plan from the supplied reparse. Preserve the old idle Mind Sol seat, all servers, and other seats until Field verifies your answer, lane/index, registration, model, and socket binding. Do not launch or migrate other seats, rename V2, or make host/source changes.\n\nCOMPLETE IMMUTABLE REPARSE FOLLOWS:\n'''
def prompt():
 b=SOURCE.read_bytes()
 if hashlib.sha256(b).hexdigest()!=SHA: raise SystemExit('reparse checksum mismatch')
 return CONTEXT+b.decode()
def argv(): return [WRAPPER,'-m','gpt-6.1-sol','-c','model_reasoning_effort="medium"','-s','danger-full-access','-a','never','--remote',REMOTE,'-C','/home/li/primary',prompt()]
if __name__=='__main__':
 a=argv()
 if sys.argv[1:]==['--verify']: print(f'verified bytes={SOURCE.stat().st_size} sha256={SHA} argv={len(a)} prompt_bytes={len(a[-1].encode())}')
 elif len(sys.argv)==1: os.execv(a[0],a)
 else: raise SystemExit('usage: --verify')
