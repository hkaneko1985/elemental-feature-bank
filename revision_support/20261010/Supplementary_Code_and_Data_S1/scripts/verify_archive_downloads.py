#!/usr/bin/env python3
"""Optional user-side fresh download check for TV-040. Not needed for offline S1.

Downloads the named v1.0.1 asset separately from GitHub and Zenodo, records
byte counts and SHA-256, and succeeds only if both match the pinned ZIP digest.
An HTTP/network failure is inconclusive; it is not evidence of a service outage.
"""
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
import argparse,csv,hashlib
EXPECTED='6c2403e88b5c4a8f63cd01d5788f3012bbe077b34c51ccca3886d4d12cde15c3'
URLS={'github':'https://github.com/hkaneko1985/elemental-feature-bank/releases/download/v1.0.1/elemental-feature-bank-v1.0.1-data.zip','zenodo':'https://zenodo.org/records/21509504/files/elemental-feature-bank-v1.0.1-data.zip?download=1'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('archive_download_check'));p.add_argument('--timeout',type=int,default=60);a=p.parse_args();a.out.mkdir(exist_ok=True,parents=True);rows=[]
 for source,url in URLS.items():
  r=dict(source=source,url=url,checked_at_utc=datetime.now(timezone.utc).isoformat(),bytes=0,sha256='',expected_sha256=EXPECTED,status='INCONCLUSIVE',detail='')
  try:
   with urlopen(Request(url,headers={'User-Agent':'ElementalFeatureBank-validation/1.0'}),timeout=a.timeout) as resp:
    h=hashlib.sha256();size=0;prefix=b''
    with (a.out/(source+'_v1.0.1.zip')).open('wb') as f:
     while True:
      b=resp.read(1024*1024)
      if not b:break
      if not prefix:prefix=b[:4]
      f.write(b);h.update(b);size+=len(b)
    r.update(bytes=size,sha256=h.hexdigest(),status='PASS' if prefix==b'PK\x03\x04' and h.hexdigest()==EXPECTED else 'FAIL',detail='Fresh authenticated-free download; ZIP signature and digest checked.')
  except Exception as e:r['detail']=type(e).__name__+': '+str(e)
  rows.append(r)
 with (a.out/'archive_equivalence.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 print('\n'.join(x['source']+': '+x['status'] for x in rows))
 if not all(r['status']=='PASS' for r in rows):raise SystemExit(2)
 print('TV-040: both independent downloads match the pinned v1.0.1 ZIP.')
if __name__=='__main__':main()
