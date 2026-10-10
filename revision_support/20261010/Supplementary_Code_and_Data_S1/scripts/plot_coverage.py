#!/usr/bin/env python3
"""Recreate Fig. 2(a-c): all 118 elements, 34 unchanged block/Tier groups.
Optional dependencies: numpy, matplotlib, Pillow. No prediction model is used.
"""
from pathlib import Path
import csv,argparse,json
import numpy as np
import matplotlib.pyplot as plt

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--out',type=Path)
 a=p.parse_args();root=a.root;out=a.out or root/'outputs/figures';out.mkdir(parents=True,exist_ok=True)
 def read(path):
  with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
 meta=read(root/'data/element_feature_metadata.csv');values={};els=None
 for name in ['element_data_interpretable.csv','element_data_others.csv']:
  rows=read(root/'data'/name);order=[r[''] for r in rows]
  if els is not None and els!=order:raise ValueError('Mismatched element order')
  els=order
  for r in rows:values.setdefault(r[''],{}).update(r)
 groups=sorted({(r['interpretability_tier'],r['feature_block']) for r in meta});data=[];keys=[]
 for j,(tier,block) in enumerate(groups,1):
  cols=[r['feature_name'] for r in meta if (r['interpretability_tier'],r['feature_block'])==(tier,block)]
  data.append([sum(values[e][c].strip()!='' for c in cols)/len(cols) for e in els]);keys.append(f'G{j:02d}')
 assert len(els)==118 and len(groups)==34
 data=np.asarray(data);plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10.5,'svg.fonttype':'none'})
 shown=[]
 for label,lo,hi in [('a',0,40),('b',40,80),('c',80,118)]:
  fig,ax=plt.subplots(figsize=(6.9,7.1));fig.subplots_adjust(left=.11,right=.98,bottom=.205,top=.90)
  im=ax.imshow(data[:,lo:hi],aspect='auto',interpolation='nearest',vmin=0,vmax=1)
  ax.set_xticks(range(hi-lo),els[lo:hi],rotation=90);ax.tick_params(axis='x',labelsize=10.5,length=2,pad=2)
  ax.set_yticks(range(len(groups)),keys);ax.tick_params(axis='y',labelsize=10.5,length=2)
  ax.set_xlabel(f'Element (atomic numbers {lo+1}-{hi})');ax.set_ylabel('Feature-block/Tier group (Table S1)')
  ax.set_title(f'({label}) All elements shown: {els[lo]}-{els[hi-1]}',fontsize=10.5,pad=12,loc='left')
  cax=fig.add_axes([.25,.058,.66,.018]);cb=fig.colorbar(im,cax=cax,orientation='horizontal',ticks=[0,.25,.5,.75,1]);cb.ax.tick_params(labelsize=9.5);cb.set_label('Fraction with a reported value',fontsize=10.5,labelpad=2)
  ticks=[t.get_text() for t in ax.get_xticklabels()];assert ticks==els[lo:hi];shown+=ticks
  for ext in ['png','svg','pdf']:fig.savefig(out/f'Figure2{label}_all_elements.{ext}',dpi=400)
  plt.close(fig)
 assert shown==els and len(set(shown))==118
 print('PASS: all 118 element columns occur once and all have explicit labels.')
if __name__=='__main__':main()
