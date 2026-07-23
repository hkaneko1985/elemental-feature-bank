#!/usr/bin/env python3
"""Rebuild AMBER/HOLD feature blocks locally from pinned source assets.

The script writes two local-only matrices matching the columns listed in
``excluded_features.csv``. It does not grant or imply redistribution rights.

Required vendor assets (created by acquire_optional_sources.py):
- elementembeddings==0.8.0 wheel
- matminer==0.10.1 wheel
- mendeleev==1.1.0 installed in the execution environment
- exact original XenonPy-derived element_data.csv supplied by the user
"""
from __future__ import annotations
import argparse, csv, importlib.util, json, math, re, statistics, sys, tempfile, zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any


def blank(v: Any) -> str:
    if v is None: return ""
    if isinstance(v, bool): return "1" if v else "0"
    if isinstance(v, (int,float)):
        x=float(v)
        if not math.isfinite(x): return ""
        if x==0: return "0"
        return f"{x:.15g}"
    s=str(v).strip()
    if s.lower() in {"","none","nan","na","missing","inf","-inf"} or s.lower().startswith('missing['): return ""
    return s

def fnum(v):
    try:
        x=float(v); return x if math.isfinite(x) else None
    except Exception:return None

def pstdev(a): return statistics.pstdev(a) if len(a)>=2 else (0.0 if len(a)==1 else None)
def stat(a,name):
    if not a:return None
    if name=='count':return len(a)
    if name=='mean':return statistics.fmean(a)
    if name=='std':return pstdev(a)
    if name=='min':return min(a)
    if name=='max':return max(a)
    if name=='median':return statistics.median(a)
    if name=='range':return max(a)-min(a)
    raise KeyError(name)

def read_csv_matrix(p):
    with p.open(newline='',encoding='utf-8-sig') as f:
        r=csv.reader(f); h=next(r); return h[0],h[1:],list(r)

def read_dicts(p):
    with p.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))

def write_matrix(p,elements,features,vals):
    with p.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['']+features)
        for e in elements:w.writerow([e]+[blank(vals[e].get(x)) for x in features])

def wheel(vendor,pattern):
    xs=sorted(vendor.glob(pattern))
    if not xs: raise FileNotFoundError(f"Missing vendor wheel: {pattern}")
    return xs[0]

def load_elementembeddings(vendor,blocks,features,elements,vals):
    wh=wheel(vendor,'elementembeddings-0.8.0-*.whl')
    prefix='elementembeddings/data/element_representations/'
    vector_files={
      'emb_matscibert':'matscibert.csv','emb_crystallm':'crystallm_v24c.dim512_atom_vectors.csv',
      'emb_chemeleon':'chemeleon.csv','emb_orb_v2':'orb_v2.csv','emb_mace_mp0':'mace_mp0.csv'
    }
    with zipfile.ZipFile(wh) as z:
        for block,fn in vector_files.items():
            if block not in blocks:continue
            text=z.read(prefix+fn).decode('utf-8-sig').splitlines()
            rr=csv.DictReader(text)
            block_feats=features[block]
            for row in rr:
                e=row['element']
                if e not in vals:continue
                for feat in block_feats:
                    idx=int(feat.rsplit('__',1)[1]); vals[e][feat]=row.get(str(idx),'')
        if 'emb_cgnf' in blocks:
            d=json.loads(z.read(prefix+'cgnf.json').decode())
            for e,arr in d.items():
                if e in vals:
                    for feat in features['emb_cgnf']:
                        vals[e][feat]=arr[int(feat.rsplit('__',1)[1])]
        if 'emb_mod_petti' in blocks:
            d=json.loads(z.read(prefix+'mod_petti.json').decode())
            feat=features['emb_mod_petti'][0]
            for e in elements:
                if e in d: vals[e][feat]=d[e]
        if 'emb_magpie22' in blocks:
            text=z.read(prefix+'magpie.csv').decode('utf-8-sig').splitlines(); rr=csv.DictReader(text)
            for row in rr:
                e=row['element']
                if e in vals:
                    for feat in features['emb_magpie22']:
                        vals[e][feat]=row.get(feat.split('__',1)[1],'')
        if 'emb_oliynyk44' in blocks:
            mapping={
              '1st_ionization_potential_kJ_mol':'1st_ionization_potential_(kJ/mol)',
              'polarizability_A_pow_3':'polarizability(A^3)',
              'Melting_point_K':'Melting_point_(K)','Boiling_Point_K':'Boiling_Point_(K)',
              'Density_g_mL':'Density_(g/mL)','specific_heat_J_g_K':'specific_heat_(J/g_K)_',
              'heat_of_fusion_kJ_mol':'heat_of_fusion_(kJ/mol)_',
              'heat_of_vaporization_kJ_mol':'heat_of_vaporization_(kJ/mol)_',
              'thermal_conductivity_W_m_K':'thermal_conductivity_(W/(m_K))_',
              'heat_atomization_kJ_mol':'heat_atomization(kJ/mol)','Miracle_Radius_pm':'Miracle_Radius_[pm]'
            }
            text=z.read(prefix+'oliynyk.csv').decode('utf-8-sig').splitlines(); rr=csv.DictReader(text)
            for row in rr:
                e=row['element']
                if e in vals:
                    for feat in features['emb_oliynyk44']:
                        suf=feat.split('__',1)[1]; vals[e][feat]=row.get(mapping.get(suf,suf),'')

def parse_table_lines(text):
    out=[]
    for line in text.splitlines():
        s=line.strip()
        if not s or s.lower() in {'missing','na','nan','none'} or s.lower().startswith('missing['):out.append(None)
        else:
            try:out.append(float(s))
            except:out.append(s)
    return out

def load_matminer(vendor,blocks,features,elements,vals):
    wh=wheel(vendor,'matminer-0.10.1-*.whl')
    root='matminer/utils/data_files/'
    with zipfile.ZipFile(wh) as z:
        if 'matminer_jarvis' in blocks:
            d=json.loads(z.read(root+'jarvis/element_chem.json').decode())
            for e,rec in d.items():
                if e in vals:
                    for feat in features['matminer_jarvis']:
                        vals[e][feat]=rec.get(feat.split('__',1)[1])
        if 'matminer_magpie' in blocks:
            bfeatures=features['matminer_magpie']
            special={'IonizationEnergies','OxidationStates'}
            scalar=[]
            for feat in bfeatures:
                suf=feat.split('__',1)[1]
                if suf.startswith('IonizationEnergies_') or suf.startswith('OxidationStates_'):continue
                table='n_ws^third' if suf=='n_ws_pow_third' else suf
                scalar.append((feat,table))
            for feat,table in scalar:
                data=parse_table_lines(z.read(root+f'magpie_elementdata/{table}.table').decode())
                for i,e in enumerate(elements):
                    if i<len(data): vals[e][feat]=data[i]
            ionlines=z.read(root+'magpie_elementdata/IonizationEnergies.table').decode().splitlines()
            oxlines=z.read(root+'magpie_elementdata/OxidationStates.table').decode().splitlines()
            for i,e in enumerate(elements):
                if i<len(ionlines):
                    arr=[fnum(x) for x in ionlines[i].split('\t')]; arr=[x for x in arr if x is not None]
                    for stage in range(1,9):
                        feat=f'magpie__IonizationEnergies_{stage:02d}_eV'
                        if feat in bfeatures and len(arr)>=stage:vals[e][feat]=arr[stage-1]
                if i<len(oxlines):
                    ox=[int(float(x)) for x in oxlines[i].split() if fnum(x) is not None]
                    for q in range(-5,10):
                        tag=f'neg{abs(q)}' if q<0 else f'pos{q}'
                        feat=f'magpie__OxidationStates_has_{tag}'
                        if feat in bfeatures:vals[e][feat]=1 if q in ox else 0
                    for sname in ['count','mean','std','min','max','median','range']:
                        feat=f'magpie__OxidationStates_{sname}'
                        if feat in bfeatures:
                            vals[e][feat]=len(ox) if sname=='count' else (stat(ox,sname) if ox else None)
        if 'matminer_deml' in blocks:
            with tempfile.TemporaryDirectory() as td:
                p=Path(td)/'deml_elementdata.py';p.write_bytes(z.read(root+'deml_elementdata.py'))
                spec=importlib.util.spec_from_file_location('deml_data',p); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
                simple=['atom_num','atom_mass','row_num','col_num','atom_radius','molar_vol','heat_fusion','mp','bp','heat_cap','electron_affin','pauling','electric_pol','GGAU_Etot','mus_fere']
                for e in elements:
                    for key in simple:
                        feat='deml__'+key
                        if feat in features['matminer_deml']:vals[e][feat]=getattr(m,key).get(e)
                    feat='deml__is_magnetic_transition_element';vals[e][feat]=1 if e in m.magn_elem else 0
                    ies=m.ionization_en.get(e,[])
                    for st in range(1,11):
                        feat=f'deml__ionization_energy_{st:02d}_J_per_mol'
                        if len(ies)>=st:vals[e][feat]=ies[st-1]
                    charges=m.charge_states.get(e)
                    if charges is not None:
                        for q in list(range(-4,0))+list(range(1,8)):
                            tag=f'neg{abs(q)}' if q<0 else f'pos{q}'
                            feat=f'deml__charge_state_has_{tag}'
                            if feat in features['matminer_deml']:vals[e][feat]=1 if q in charges else 0
                    for prop,fd in [('xtal_field_split',m.xtal_field_split),('magn_moment',m.magn_moment),('so_coupling',m.so_coupling),('sat_magn',m.sat_magn)]:
                        for q,v in fd.get(e,{}).items():
                            feat=f'deml__{prop}__charge_pos{q}'
                            if feat in features['matminer_deml']: vals[e][feat]=v
                    col=m.col_num.get(e); ve=m.valence_e.get(col,{})
                    for orb in 'spd':
                        feat=f'deml__valence_{orb}_from_column'
                        if feat in features['matminer_deml']:vals[e][feat]=ve.get(orb)
        if 'matminer_miedema' in blocks:
            text=z.read(root+'Miedema.csv').decode('utf-8-sig').splitlines(); rr=csv.DictReader(text)
            for row in rr:
                e=row['element'];
                if e in vals:
                    for feat in features['matminer_miedema']:
                        if feat.startswith('miedema__'):vals[e][feat]=row.get(feat.split('__',1)[1])
            pairs=defaultdict(list)
            lines=z.read(root+'MiedemaLiquidDeltaHf.tsv').decode().splitlines(); pr=csv.DictReader(lines,delimiter=' ')
            for row in pr:
                try:v=float(row['delta_Hf'])
                except:continue
                pairs[row['elem_A']].append(v);pairs[row['elem_B']].append(v)
            for e,arr in pairs.items():
                if e not in vals:continue
                d={'partner_count':len(arr),'partner_mean':statistics.fmean(arr),'partner_std':pstdev(arr),'partner_min':min(arr),'partner_max':max(arr),'partner_median':statistics.median(arr),'partner_range':max(arr)-min(arr),'fraction_negative':sum(x<0 for x in arr)/len(arr),'fraction_positive':sum(x>0 for x in arr)/len(arr),'fraction_zero':sum(x==0 for x in arr)/len(arr)}
                for k,v in d.items():
                    feat='miedema_pair__liquid_deltaHf_'+k
                    if feat in features['matminer_miedema']:vals[e][feat]=v
        if 'matminer_cohesive' in blocks:
            d=json.loads(z.read(root+'cohesive_energies.json').decode());feat=features['matminer_cohesive'][0]
            for e,v in d.items():
                if e in vals:vals[e][feat]=v

def load_mendeleev(blocks,features,elements,vals):
    try:
        from mendeleev import get_all_elements
    except Exception as exc:
        raise RuntimeError('mendeleev==1.1.0 must be installed in the reconstruction environment') from exc
    objects={obj.symbol: obj for obj in get_all_elements() if obj.symbol in elements}
    if 'mendeleev_ionic_radius' in blocks:
        for e,obj in objects.items():
            recs=list(obj.ionic_radii)
            if not recs:continue
            groups={'all':recs,'reliable':[r for r in recs if r.most_reliable], 'cation':[r for r in recs if r.charge>0], 'anion':[r for r in recs if r.charge<0], 'high_spin':[r for r in recs if (r.spin or '').upper()=='HS'], 'low_spin':[r for r in recs if (r.spin or '').upper()=='LS']}
            for g,rs in groups.items():
                for prop in ['ionic_radius','crystal_radius']:
                    arr=[float(getattr(r,prop)) for r in rs if getattr(r,prop) is not None]
                    for sn in ['count','mean','std','min','max','median','range']:
                        feat=f'mend_ionic__{g}_{prop}_{sn}'
                        if feat in features['mendeleev_ionic_radius']:
                            vals[e][feat]=len(arr) if sn=='count' else stat(arr,sn)
            for q in range(-3,9):
                tag=f'neg{abs(q)}' if q<0 else f'pos{q}';rs=[r for r in recs if r.charge==q]
                feat=f'mend_ionic__charge_{tag}_count';vals[e][feat]=len(rs)
                for prop in ['ionic_radius','crystal_radius']:
                    arr=[float(getattr(r,prop)) for r in rs if getattr(r,prop) is not None]
                    for sn in ['mean','std','min','max']:
                        feat=f'mend_ionic__charge_{tag}_{prop}_{sn}'
                        if feat in features['mendeleev_ionic_radius']:vals[e][feat]=stat(arr,sn)
            coord_count_features=[f for f in features['mendeleev_ionic_radius'] if f.startswith('mend_ionic__coord_') and f.endswith('_count')]
            for feat in coord_count_features:
                vals[e][feat]=0
            coords=sorted({r.coordination for r in recs if r.coordination})
            for co in coords:
                rs=[r for r in recs if r.coordination==co]
                feat=f'mend_ionic__coord_{co}_count'
                if feat in features['mendeleev_ionic_radius']:vals[e][feat]=len(rs)
                for prop in ['ionic_radius','crystal_radius']:
                    arr=[float(getattr(r,prop)) for r in rs if getattr(r,prop) is not None]
                    for sn in ['mean','std','min','max']:
                        feat=f'mend_ionic__coord_{co}_{prop}_{sn}'
                        if feat in features['mendeleev_ionic_radius']:vals[e][feat]=stat(arr,sn)
    if 'mendeleev_li_xue_summary' in blocks:
        for e,obj in objects.items():
            for radius_type,short in [('crystal_radius','crystal'),('ionic_radius','ionic')]:
                for q in range(1,9):
                    try:d=obj.electronegativity_li_xue(q,radius=radius_type) or {}
                    except Exception:d={}
                    arr=[float(v) for v in d.values() if v is not None and math.isfinite(float(v))]
                    for sn in ['count','mean','min','max','std']:
                        feat=f'mend_li_xue__{short}_pos{q}_{sn}'
                        if feat in features['mendeleev_li_xue_summary']:vals[e][feat]=len(arr) if sn=='count' and arr else (stat(arr,sn) if arr else None)
    if 'mendeleev_electronegativity_extended' in blocks:
        methods={
          'mend_en_ext__allred_rochow_pyykko':lambda o:o.electronegativity_allred_rochow(),
          'mend_en_ext__cottrell_sutton_pyykko':lambda o:o.electronegativity_cottrell_sutton(),
          'mend_en_ext__gordy_pyykko':lambda o:o.electronegativity_gordy(),
          'mend_en_ext__martynov_batsanov':lambda o:o.electronegativity_martynov_batsanov(),
          'mend_en_ext__nagle':lambda o:o.electronegativity_nagle(),
          'mend_en_ext__sanderson_pyykko':lambda o:o.electronegativity_sanderson(),
        }
        for e,o in objects.items():
            for feat,fn in methods.items():
                try:vals[e][feat]=fn(o)
                except Exception:vals[e][feat]=None

def load_xenonpy(vendor,features,elements,vals):
    candidates=list(vendor.glob('xenonpy_element_data*.csv'))+list(vendor.glob('element_data*.csv'))
    if not candidates:raise FileNotFoundError('Supply the exact original XenonPy-derived CSV to the vendor directory')
    _,fs,rows=read_csv_matrix(candidates[0]); idx={x:i for i,x in enumerate(fs)}
    for row in rows:
        e=row[0]
        if e in vals:
            for feat in features['xenonpy_original']:
                if feat in idx:vals[e][feat]=row[1+idx[feat]]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--public-dir',type=Path,default=Path('.'));ap.add_argument('--vendor-dir',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=True)
    _,_,rows=read_csv_matrix(a.public_dir/'element_data_interpretable.csv');elements=[r[0] for r in rows]
    ex=read_dicts(a.public_dir/'excluded_features.csv')
    byblock=defaultdict(list); byfile=defaultdict(list)
    for r in ex:byblock[r['feature_block']].append(r['feature_name']);byfile[r['dataset_file']].append(r['feature_name'])
    vals={e:{} for e in elements};blocks=set(byblock)
    load_elementembeddings(a.vendor_dir,blocks,byblock,elements,vals)
    load_matminer(a.vendor_dir,blocks,byblock,elements,vals)
    load_mendeleev(blocks,byblock,elements,vals)
    load_xenonpy(a.vendor_dir,byblock,elements,vals)
    out_i=a.output_dir/'optional_element_data_interpretable.csv';out_o=a.output_dir/'optional_element_data_others.csv'
    write_matrix(out_i,elements,byfile['element_data_interpretable.csv'],vals)
    write_matrix(out_o,elements,byfile['element_data_others.csv'],vals)
    print(json.dumps({'elements':len(elements),'optional_interpretable_features':len(byfile['element_data_interpretable.csv']),'optional_other_features':len(byfile['element_data_others.csv']),'output':[str(out_i),str(out_o)]},indent=2))
if __name__=='__main__':main()
