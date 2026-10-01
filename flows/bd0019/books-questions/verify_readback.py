# Read-back check: the published page must contain book.html byte-for-byte; reports both sha256 values.
import sys,hashlib
b=open('/home/li/primary/flows/bd0019/books-questions/book.html').read(); r=open(sys.argv[1]).read()
i=r.find(b.strip()[:200])
seg=r[i:i+len(b.strip())] if i>=0 else ''
print('local sha256   ',hashlib.sha256(b.strip().encode()).hexdigest())
print('readback sha256',hashlib.sha256(seg.encode()).hexdigest())
print('READBACK IDENTICAL' if seg==b.strip() else 'READBACK DIFFERS'); sys.exit(0 if seg==b.strip() else 1)
