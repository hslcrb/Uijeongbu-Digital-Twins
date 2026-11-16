"""Lossless Blender Zstd recompression. pip install zstandard; source target arguments."""
import sys,hashlib,zstandard as z
from pathlib import Path
src,dst=map(Path,sys.argv[1:3])
assert src.resolve()!=dst.resolve(),'Write a separate output, never overwrite source while reading'
with src.open('rb') as f,z.ZstdDecompressor().stream_reader(f) as r,dst.open('wb') as o,z.ZstdCompressor(level=19,threads=4).stream_writer(o) as w:
 while b:=r.read(1024*1024):w.write(b)
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f,z.ZstdDecompressor().stream_reader(f) as r:
  while b:=r.read(1024*1024):h.update(b)
 return h.hexdigest()
assert digest(src)==digest(dst),'Uncompressed bytes changed'
print(dst.stat().st_size,digest(dst))
