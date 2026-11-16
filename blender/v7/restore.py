"""Restore the exact Blender file using only Python's standard library."""
from pathlib import Path
import hashlib,json,os
root=Path(__file__).resolve().parent;m=json.loads((root/'manifest.json').read_text());out=root/m['output'];tmp=out.with_suffix('.blend.tmp');h=hashlib.sha256();size=0
try:
 with tmp.open('wb') as w:
  for part in m['parts']:
   b=(root/part['name']).read_bytes()
   assert len(b)==part['bytes'] and hashlib.sha256(b).hexdigest()==part['sha256'],part['name']+' checksum mismatch'
   w.write(b);h.update(b);size+=len(b)
 assert size==m['bytes'] and h.hexdigest()==m['sha256'],'Output checksum mismatch'
 os.replace(tmp,out);print(out, size, h.hexdigest())
finally:
 if tmp.exists():tmp.unlink()
