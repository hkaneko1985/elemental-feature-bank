#!/usr/bin/env python3
"""Recreate rule-based audit labels and unweighted kappa without AI/API access.

Usage: python scripts/reproduce_tier_audit.py
A reconstructed audit is NOT a re-execution of a historical ChatGPT conversation.
Comparison labels never enter tier_rules.classify(). No independent/blind-rater
inference is made. Python standard library only (3.10+).
"""
from __future__ import annotations
import argparse,csv,json,hashlib,sys
from collections import Counter
from pathlib import Path
from tier_rules import classify,TIERS

def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,rows,fields=None):
    if fields is None:fields=list(rows[0])
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
def agreement(a,b,labels):
    if len(a)!=len(b) or not a:raise ValueError('Empty or unequal label arrays')
    if (set(a)|set(b))-set(labels):raise ValueError('Unexpected label')
    n=len(a);na,nb=Counter(a),Counter(b);matches=sum(x==y for x,y in zip(a,b))
    po=matches/n;pe=sum(na[t]*nb[t] for t in labels)/(n*n)
    return dict(n=n,agreements=matches,agreement_percent=100*po,observed_agreement=po,expected_agreement=pe,kappa=(po-pe)/(1-pe) if pe<1 else None)
def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--out',type=Path)
    args=p.parse_args();root=args.root;out=args.out or root/'outputs';out.mkdir(parents=True,exist_ok=True)
    inputs=read(root/'classification/classification_inputs.csv')
    forbidden={'interpretability_tier','original_tier','reviewer_1_tier','reviewer_2_tier','adopted_tier','dataset_file','dataset_partition','curation_rule','curation_notes','direct_or_derived'}
    if forbidden & set(inputs[0]):raise ValueError('Label/curation fields present in classifier input')
    names=[r['feature_name'] for r in inputs]
    if len(set(names))!=len(names):raise ValueError('Duplicate input feature')
    # Generate all audit labels before loading the comparison table.
    pred={r['feature_name']:classify(r) for r in inputs}
    labels=read(root/'classification/archived_label_pairs.csv');lab={r['feature_name']:r for r in labels}
    if set(pred)!=set(lab):raise ValueError('Label and input feature sets differ')
    assignments=[];mismatches=[]
    for r in inputs:
        name=r['feature_name'];t,rule=pred[name];old=lab[name]
        rr=dict(feature_name=name,feature_block=r['feature_block'],rule_id=rule,original_tier=old['original_tier'],reproduced_audit_tier=t,archived_audit_tier=old['archived_audit_tier'],adopted_tier=old['adopted_tier'],public_value_distribution=old['public_value_distribution'],matches_archived=str(t==old['archived_audit_tier']),same_as_original=str(t==old['original_tier']))
        assignments.append(rr)
        if t!=old['archived_audit_tier']:mismatches.append(rr)
    write(out/'reproduced_assignments.csv',assignments)
    write(out/'rule_reproduction_mismatches.csv',mismatches,list(assignments[0]))
    write(out/'disagreement_decisions.csv',[dict(**r,decision_reason=lab[r['feature_name']]['decision_reason']) for r in assignments if r['same_as_original']=='False'])
    scopes={'all_5200':assignments,'public_1766':[r for r in assignments if r['public_value_distribution']=='include'],'excluded_3434':[r for r in assignments if r['public_value_distribution']=='exclude'],'non_G_2034':[r for r in assignments if r['original_tier']!=TIERS[-1] or r['reproduced_audit_tier']!=TIERS[-1]]}
    metrics=[]
    for name,rs in scopes.items():
        a=[r['original_tier'] for r in rs];b=[r['reproduced_audit_tier'] for r in rs]
        m=agreement(a,b,TIERS);m={'scope':name,**m}
        binary=agreement(['ABC' if t[0] in 'ABC' else 'DG' for t in a],['ABC' if t[0] in 'ABC' else 'DG' for t in b],('ABC','DG'))
        m.update(binary_agreement_percent=binary['agreement_percent'],binary_kappa=binary['kappa']);metrics.append(m)
    write(out/'agreement_metrics_recomputed.csv',metrics)
    confusion=[{'original_tier':a,**{b:sum(r['original_tier']==a and r['reproduced_audit_tier']==b for r in assignments) for b in TIERS}} for a in TIERS]
    write(out/'confusion_matrix_recomputed.csv',confusion)
    rc=Counter(r['rule_id'] for r in assignments);write(out/'rule_usage.csv',[dict(rule_id=k,features=v) for k,v in sorted(rc.items())])
    hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'classification/classification_inputs.csv',root/'classification/archived_label_pairs.csv',root/'scripts/tier_rules.py',root/'scripts/reproduce_tier_audit.py')}
    summary=dict(features=len(assignments),blocks=len(set(r['feature_block'] for r in assignments)),rule_reproduction_mismatches=len(mismatches),original_audit_disagreements=sum(r['same_as_original']=='False' for r in assignments),metrics=metrics,input_and_code_sha256=hashes,python=sys.version,interpretation='Descriptive rule-based consistency audit; not blind or independent inter-rater validation')
    (out/'tier_audit_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    if len(assignments)!=5200 or mismatches:raise SystemExit('FAIL: audit reproduction mismatch')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('input_and_code_sha256','python')},indent=2))
if __name__=='__main__':main()
