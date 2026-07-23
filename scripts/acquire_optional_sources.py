#!/usr/bin/env python3
"""Download exact package distributions needed for local optional reconstruction."""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, sys
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--xenonpy-csv',type=Path,required=True);a=ap.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
 pkgs=['elementembeddings==0.8.0','matminer==0.10.1','mendeleev==1.1.0']
 subprocess.run([sys.executable,'-m','pip','download','--no-deps','--dest',str(a.output_dir),*pkgs],check=True)
 dest=a.output_dir/'xenonpy_element_data_original.csv';shutil.copy2(a.xenonpy_csv,dest)
 rec=[]
 for p in sorted(a.output_dir.iterdir()):
  if p.is_file():rec.append({'file':p.name,'size_bytes':p.stat().st_size,'sha256':sha(p)})
 (a.output_dir/'acquisition_receipt.json').write_text(json.dumps({'packages':pkgs,'files':rec,'notice':'Downloaded assets retain their upstream rights; do not commit locally rebuilt values.'},indent=2)+'\n')
 print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
