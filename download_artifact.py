from pathlib import Path
import urllib.request,urllib.parse,json,hashlib,concurrent.futures,sys,argparse,os,time
parser=argparse.ArgumentParser(description='Retrieve the anonymous R6 artifact with verified, resumable 512-KiB parts. No model/API credentials are used.')
parser.add_argument('--url',default='https://anonymous.4open.science/r/task-availability-evaluation-records-03F5/')
parser.add_argument('--output',default='artifact_download')
parser.add_argument('--jobs',type=int,default=2)
a=parser.parse_args();u=urllib.parse.urlsplit(a.url)
assert u.scheme=='https' and u.netloc=='anonymous.4open.science' and u.path.startswith('/r/')
repo=u.path.split('/')[2];base='https://anonymous.4open.science/api/repo/'+urllib.parse.quote(repo,safe='')+'/file/'
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
def retrieve(name):
 assert Path(name).name==name
 req=urllib.request.Request(base+urllib.parse.quote(name)+'?download=true',headers={'User-Agent':'artifact-review-download'})
 with urllib.request.urlopen(req,timeout=60) as response:
  assert response.status==200 and urllib.parse.urlsplit(response.url).netloc=='anonymous.4open.science'
  start=time.monotonic();data=bytearray()
  while True:
   block=response.read1(65536)
   if not block:break
   data.extend(block)
   assert len(data)<=1024*1024,'Unexpected oversized response'
   if time.monotonic()-start>90:raise TimeoutError('Per-file transfer deadline exceeded')
  return bytes(data)
raw_manifest=retrieve('ARCHIVE_PARTS.json');m=json.loads(raw_manifest)
assert m['archive_name']=='anonymous_artifact_R6.zip' and len(m['parts'])<=128
assert all(Path(x['name']).name==x['name'] and 0<x['bytes']<=512*1024 for x in m['parts'])
(out/'ARCHIVE_PARTS.json').write_bytes(raw_manifest)
def part(item):
 name=item['name'];p=out/name
 if p.exists() and p.stat().st_size==item['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']:return name+' cached'
 last=None
 for attempt in range(2):
  try:
   data=retrieve(name)
   assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],'Length or hash mismatch: '+name
   tmp=p.with_name(p.name+'.downloading');tmp.write_bytes(data);tmp.replace(p);return name+' verified'
  except Exception as e:
   last=e
   if attempt==0:time.sleep(2)
 raise RuntimeError('Download incomplete for '+name+'; rerun to keep already verified parts') from last
pool=concurrent.futures.ThreadPoolExecutor(max_workers=max(1,min(a.jobs,4)))
futures=[pool.submit(part,item) for item in m['parts']]
try:
 for future in concurrent.futures.as_completed(futures):print(future.result(),flush=True)
except BaseException:
 for future in futures:future.cancel()
 pool.shutdown(wait=True,cancel_futures=True)
 raise
else:pool.shutdown(wait=True)
archive=out/m['archive_name'];tmp=archive.with_name(archive.name+'.assembling');digest=hashlib.sha256();size=0
with tmp.open('wb') as stream:
 for item in m['parts']:
  data=(out/item['name']).read_bytes();stream.write(data);digest.update(data);size+=len(data)
assert size==m['archive_bytes'] and digest.hexdigest()==m['archive_sha256']
tmp.replace(archive);print('Complete original archive verified:',archive)
print('Next: python3 -m zipfile -e '+str(archive)+' unpacked')
print('Then: cd unpacked/anonymous_artifact_R6 && python3 verify_all.py')
