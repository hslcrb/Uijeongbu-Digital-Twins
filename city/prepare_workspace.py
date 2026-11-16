"""Restore a regeneration workspace without modifying the repository."""
import argparse,hashlib,json,shutil,tarfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('--elevation',type=Path,required=True,help='N37E127.hgt.gz from the documented source URL');a=p.parse_args();root=Path(__file__).resolve().parent
checks=json.loads((root/'data/source-checksums.json').read_text())
if hashlib.sha256(a.elevation.read_bytes()).hexdigest()!=checks['N37E127.hgt.gz']['sha256']:raise SystemExit('Elevation checksum mismatch')
a.output.mkdir(parents=True,exist_ok=True)
for f in (root/'scripts').glob('*.py'):shutil.copy2(f,a.output/f.name)
for name in ['boundary-search.json','download-index.json','source-checksums.json']:shutil.copy2(root/'data'/name,a.output/name)
shutil.copy2(a.elevation,a.output/'N37E127.hgt.gz')
with tarfile.open(root/'data/osm-source-tiles.tar.gz') as archive:archive.extractall(a.output,filter='data')
for name,entry in checks.items():
 file=a.output/name
 if file.exists() and hashlib.sha256(file.read_bytes()).hexdigest()!=entry['sha256']:raise SystemExit('Checksum mismatch: '+name)
print('Workspace restored:',a.output)
print('Set the system Python/Shapely path in build_city.py for your installation, then run Blender build_city.py and export_city.py.')
