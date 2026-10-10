#!/usr/bin/env python3
"""Minimal, target-independent composition-descriptor example (Python 3.10+).

Only flat formulae such as Fe2O3, TiO2 and SrTiO3 are supported. Parentheses,
hydrates, charges, isotopic labels and mixed-site syntax are deliberately rejected.
No predictive model is fitted. Blank constituent values propagate to all feature
summaries; observed atomic-fraction coverage is reported separately.
"""
from __future__ import annotations
import argparse,csv,json,math,re
from pathlib import Path
FEATURES=(('mend_elem__atomic_number','Atomic number','1'),
          ('mend_elem__en_pauling','Pauling electronegativity','1'),
          ('mend_ie__stage_01_eV','First ionization energy','eV'))
FORMULAS=('Fe2O3','TiO2','SrTiO3')
TOKEN=re.compile(r'([A-Z][a-z]?)(\d+(?:\.\d+)?)?')

def load_matrix(path:Path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);id_key=reader.fieldnames[0];rows=list(reader)
    values={r[id_key]:r for r in rows}
    if len(values)!=len(rows):raise ValueError('Duplicate element identifiers')
    return values

def parse_formula(formula:str,allowed:set[str]):
    """Parse a deliberately narrow formula grammar and normalize atomic counts."""
    if not formula or re.search(r'[^A-Za-z0-9.]',formula):raise ValueError(f'Unsupported formula: {formula!r}')
    pos=0;counts={}
    for match in TOKEN.finditer(formula):
        if match.start()!=pos:raise ValueError(f'Invalid syntax at position {pos}: {formula}')
        el,amount=match.groups()
        if el not in allowed:raise ValueError(f'Unknown element: {el}')
        n=float(amount) if amount else 1.0
        if not math.isfinite(n) or n<=0:raise ValueError('Stoichiometric coefficients must be positive and finite')
        counts[el]=counts.get(el,0.0)+n;pos=match.end()
    if pos!=len(formula) or not counts:raise ValueError(f'Invalid formula: {formula}')
    total=sum(counts.values())
    return {el:n/total for el,n in counts.items()}

def summarize(fractions:dict[str,float],values:dict[str,dict[str,str]],feature:str):
    xs=[];missing=[]
    for el,w in fractions.items():
        raw=values[el].get(feature)
        if raw is None:raise KeyError(f'Feature not present: {feature}')
        if raw.strip()=='':missing.append(el)
        else:
            x=float(raw)
            if not math.isfinite(x):raise ValueError(f'Nonfinite value in {el}/{feature}')
            xs.append((el,w,x))
    coverage=math.fsum(w for _,w,_ in xs)
    if missing:
        return dict(mean=None,weighted_sd=None,minimum=None,maximum=None,range=None,atomic_fraction_coverage=coverage,missing_elements=';'.join(missing))
    mu=math.fsum(w*x for _,w,x in xs)
    var=math.fsum(w*(x-mu)**2 for _,w,x in xs) # weighted population variance; no ddof correction
    raw=[x for _,_,x in xs]
    return dict(mean=mu,weighted_sd=math.sqrt(max(0.0,var)),minimum=min(raw),maximum=max(raw),range=max(raw)-min(raw),atomic_fraction_coverage=coverage,missing_elements='')

def write_csv(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader()
        for row in rows:w.writerow({k:('' if v is None else format(v,'.12g') if isinstance(v,float) else v) for k,v in row.items()})

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--out',type=Path)
    a=p.parse_args();root=a.root;out=a.out or root/'outputs';out.mkdir(exist_ok=True,parents=True)
    data=load_matrix(root/'data/element_data_interpretable.csv');records=[];inputs=[]
    with (root/'data/element_feature_metadata.csv').open(encoding='utf-8-sig',newline='') as f:meta={r['feature_name']:r for r in csv.DictReader(f)}
    for formula in FORMULAS:
        fractions=parse_formula(formula,set(data))
        for feature,label,unit in FEATURES:
            if meta[feature]['dataset_file']!='element_data_interpretable.csv':raise ValueError('Unexpected partition')
            for element,weight in fractions.items():
                inputs.append(dict(formula=formula,element=element,atomic_fraction=weight,feature_name=feature,source_value=data[element][feature],unit=unit,source=meta[feature]['source'],source_version=meta[feature]['source_version']))
            records.append(dict(formula=formula,feature_name=feature,feature_label=label,unit=unit,**summarize(fractions,data,feature)))
    write_csv(out/'composition_input_trace.csv',inputs)
    write_csv(out/'composition_descriptors.csv',records)
    print(json.dumps(records,indent=2))
if __name__=='__main__':main()
