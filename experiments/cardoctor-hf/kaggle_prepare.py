"""Inspect public Kaggle ZIPs by HTTP range; all artifacts remain on D:."""
import io,json,zipfile,urllib.request,urllib.parse,hashlib,time
from pathlib import Path
ROOT=Path("D:/hakathon_wiut/datasets/kaggle-audit")
SLUGS={"vehide":"hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection","hit":"humansintheloop/car-parts-and-car-damages","coco-small":"lplenka/coco-car-damage-detection-dataset"}
class RemoteZip(io.RawIOBase):
 def __init__(self,slug):
  self.url="https://www.kaggle.com/api/v1/datasets/download/"+slug
  self.pos=0
  with urllib.request.urlopen(urllib.request.Request(self.url,headers={"Range":"bytes=-22"}),timeout=60) as r:
   if r.status!=206:raise RuntimeError("Server did not support bounded range")
   self.size=int(r.headers["Content-Range"].split("/")[-1]);r.read()
 def seekable(self):return True
 def readable(self):return True
 def tell(self):return self.pos
 def seek(self,offset,whence=0):
  self.pos=offset if whence==0 else self.pos+offset if whence==1 else self.size+offset
  if self.pos<0:raise ValueError("negative seek")
  return self.pos
 def read(self,n=-1):
  n=self.size-self.pos if n<0 else min(n,self.size-self.pos)
  if not n:return b""
  if n>100*1024*1024:raise ValueError("Single read exceeds 100 MiB safety limit")
  for attempt in range(3):
   try:
    req=urllib.request.Request(self.url,headers={"Range":f"bytes={self.pos}-{self.pos+n-1}"})
    with urllib.request.urlopen(req,timeout=60) as r:
     if r.status!=206:raise RuntimeError("Range ignored")
     b=r.read(n+1)
    if len(b)!=n:raise RuntimeError("Incomplete bounded download")
    self.pos+=n;return b
   except Exception:
    if attempt==2:raise
    time.sleep(1)
def download_archive(key):
 ROOT.mkdir(parents=True,exist_ok=True)
 target=ROOT/(key+".zip");part=target.with_suffix(".zip.part")
 remote=RemoteZip(SLUGS[key])
 if target.exists() and target.stat().st_size==remote.size:
  print("Existing complete archive preserved",target,flush=True);return
 start=part.stat().st_size if part.exists() else 0
 if start>remote.size:raise ValueError("Partial archive is too large")
 req=urllib.request.Request(remote.url,headers={"Range":f"bytes={start}-{remote.size-1}"})
 with urllib.request.urlopen(req,timeout=90) as response,part.open("ab") as out:
  if response.status!=206:raise RuntimeError("Resumable range not supported")
  current=start;last=time.monotonic()
  while block:=response.read(4*1024*1024):
   out.write(block);current+=len(block)
   if time.monotonic()-last>10:print(key,"download",round(100*current/remote.size,1),"percent",flush=True);last=time.monotonic()
 if part.stat().st_size!=remote.size:raise ValueError("Incomplete archive")
 part.replace(target)
 with target.open("rb") as f:digest=hashlib.file_digest(f,"sha256").hexdigest()
 (ROOT/(key+"-download.json")).write_text(json.dumps({"slug":SLUGS[key],"bytes":remote.size,"sha256":digest,"downloaded_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())},indent=2),encoding="utf-8")
 print("Complete",key,remote.size,digest,flush=True)
def inspect(key):
 ROOT.mkdir(parents=True,exist_ok=True);slug=SLUGS[key]
 meta=json.load(urllib.request.urlopen("https://www.kaggle.com/api/v1/datasets/view/"+slug,timeout=30))
 (ROOT/(key+"-metadata.json")).write_text(json.dumps(meta,indent=2),encoding="utf-8")
 remote=RemoteZip(slug)
 with zipfile.ZipFile(remote) as z:
  fs=[{"name":i.filename,"bytes":i.file_size,"compressed":i.compress_size,"crc32":i.CRC} for i in z.infolist()]
  (ROOT/(key+"-archive-index.json")).write_text(json.dumps({"slug":slug,"archive_bytes":remote.size,"files":fs},indent=2),encoding="utf-8")
  ann=[i for i in z.infolist() if i.filename.lower().endswith((".json",".yaml",".yml",".txt",".xml"))]
  print(key,"archive",remote.size,"files",len(fs),"metadata files",len(ann),"examples",[i.filename for i in ann[:8]],flush=True)
  # VehiDE global annotations; HIT metadata and one annotation from each subset; tiny COCO all annotations.
  selected=ann if key!="hit" else [i for i in ann if "/ann/" not in i.filename]+[next(i for i in ann if "Car damages" in i.filename and "/ann/" in i.filename),next(i for i in ann if "Car parts" in i.filename and "/ann/" in i.filename)]
  for i in selected:
   out=ROOT/key/Path(i.filename)
   if out.resolve().is_relative_to((ROOT/key).resolve()) is False:raise ValueError("unsafe ZIP member")
   if i.file_size>80*1024*1024:raise ValueError("Annotation exceeds size cap")
   out.parent.mkdir(parents=True,exist_ok=True);data=z.read(i);out.write_bytes(data)
   print("downloaded",key,i.filename,len(data),hashlib.sha256(data).hexdigest(),flush=True)
if __name__=="__main__":
 import sys,concurrent.futures
 if len(sys.argv)>1 and sys.argv[1]=="download":
  download_archive(sys.argv[2]);raise SystemExit(0)
 keys=sys.argv[1:] or list(SLUGS)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(inspect,keys))
