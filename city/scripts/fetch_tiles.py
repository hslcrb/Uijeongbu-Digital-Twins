import urllib.request,time,json,concurrent.futures,pathlib
D=pathlib.Path(__file__).parent; (D/'osm').mkdir(exist_ok=True)
a,b,c,d=127.00161,37.68593,127.14740,37.78037
jobs=[]
for x in range(5):
 for y in range(4):
  box=[a+(c-a)*x/5,b+(d-b)*y/4,a+(c-a)*(x+1)/5,b+(d-b)*(y+1)/4];jobs.append((f'{x}-{y}',box))
def get(job):
 n,box=job;p=D/'osm'/f'{n}.osm';u='https://api.openstreetmap.org/api/0.6/map?bbox='+','.join(map(str,box))
 if p.exists() and p.read_bytes().startswith(b'<?xml'):return n,p.stat().st_size
 for i in range(3):
  try:
   raw=urllib.request.urlopen(u,timeout=60).read();p.write_bytes(raw);print(n,len(raw),flush=True);return n,len(raw)
  except Exception as e:print(n,str(e),flush=True);time.sleep(3)
 return n,0
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(get,jobs))
(D/'download-index.json').write_text(json.dumps({'tiles':jobs,'results':results},indent=2))
