from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
m=json.loads((p/'ARCHIVE_PARTS.json').read_text())
out=p/m['archive_name']
if out.exists():
 assert hashlib.sha256(out.read_bytes()).hexdigest()==m['archive_sha256'],'Existing archive does not match; move it before retrying'
 print('Archive already present and verified:',out.name)
else:
 tmp=out.with_suffix(out.suffix+'.assembling')
 digest=hashlib.sha256();total=0
 with tmp.open('wb') as stream:
  for item in m['parts']:
   part=p/item['name'];assert part.resolve().is_relative_to(p.resolve())
   data=part.read_bytes()
   assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],item['name']
   stream.write(data);digest.update(data);total+=len(data)
 assert total==m['archive_bytes'] and digest.hexdigest()==m['archive_sha256'],'Archive verification failed'
 tmp.replace(out)
 print('Assembled and verified:',out.name)
