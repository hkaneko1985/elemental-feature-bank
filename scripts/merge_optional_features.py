#!/usr/bin/env python3
"""Merge public and locally rebuilt optional matrices for private/local analysis only."""
from __future__ import annotations
import argparse,csv
from pathlib import Path

def read(p):
 with p.open(newline='',encoding='utf-8-sig') as f:r=csv.reader(f);h=next(r);return h,list(r)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-dir',type=Path,required=True);ap.add_argument('--optional-dir',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
 for pub,opt,out in [('element_data_interpretable.csv','optional_element_data_interpretable.csv','element_data_interpretable_with_optional_local.csv'),('element_data_others.csv','optional_element_data_others.csv','element_data_others_with_optional_local.csv')]:
  hp,rp=read(a.public_dir/pub);ho,ro=read(a.optional_dir/opt);assert [x[0] for x in rp]==[x[0] for x in ro]
  with (a.output_dir/out).open('w',newline='',encoding='utf-8-sig') as f:
   w=csv.writer(f);w.writerow(hp+ho[1:]);[w.writerow(x+y[1:]) for x,y in zip(rp,ro)]
 print('Local-only merged matrices written to',a.output_dir)
if __name__=='__main__':main()
