#!/usr/bin/env python3
"""Independently reconcile source features, tables, windows and H3 masks."""
import argparse,csv,gzip,json,math
from collections import defaultdict
from pathlib import Path
from mellon_7_8_stage4 import sha,read_top,load_json,dump

def close(a,b):assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)
def val(x,r,m):return x[r]['size']-(x[r]['hosting'] if m=='without-hosting' else 0)
def csvrows(p):return list(csv.DictReader(p.open()))
def main():
 p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--sources',type=Path,required=True);a=p.parse_args();run=a.run;m=load_json(run/'selection-manifest.json');objects={r['key']:load_json(run/'objects'/(r['key']+'.json')) for r in m['objects']};checks=defaultdict(int)
 for r in load_json(run/'input-manifest.json')['inputs']:assert sha(a.sources/r['repository']/r['path'])==r['sha256'];checks['input_hashes']+=1
 regions={k:v['country_codes'] for k,v in m['regions'].items() if k in ['asia-28','eur-27','usa-can']};regions.update({k:[k] for k in ['JPN','USA','CHN','KOR']});assert len(set(regions['asia-28']))==28 and {'MAC','TWN'}<=set(regions['asia-28'])
 for meta in m['objects']:
  for grain in ['week','day']:
   for w in objects[meta['key']][grain+'s']:
    path=a.sources/f"alpha60-results-{meta['sample_year']}"/f"data/geojson.{grain}/{meta['key']}-{grain}-{w['index']:05d}.geojson.gz";doc=read_top(path);sums=defaultdict(int);cities=defaultdict(int)
    for f in doc['features']:
     p=f['properties'];country=p.get('country_code') or 'UNCLASSIFIED'
     for role in ['downloaders','uploaders']:
      for field in ['size','hosting']:
       sums[(country,role,field)]+=p[role][field]
       cities[(country+':'+str(p.get('geoname_id')),role,field)]+=p[role][field]
    for role in ['downloaders','uploaders']:
     for field in ['size','hosting']:
      assert sum(v for (c,r,f),v in sums.items() if (r,f)==(role,field))==w['world'][role][field]
      for code,entry in w['countries'].items():assert sums[(code,role,field)]==entry[role][field]
    for c in w.get('cities',[]):
     for role in ['downloaders','uploaders']:
      for field in ['size','hosting']:assert c[role][field]==cities[(c['id'],role,field)]
    checks['raw_interval_reductions']+=1
    if w['index']==len(objects[meta['key']]['weeks']) and grain=='week':assert json.loads(gzip.decompress(path.read_bytes()))['features']==doc['features'];checks['full_document_crosschecks']+=1
 for filename,grain in [('weekly-regions.csv','weeks'),('daily-regions.csv','days')]:
  for r in csvrows(run/filename):
   i=int(r['index']);lookup={w['index']:w for w in objects[r['key']][grain]};w=lookup[i];role=r['role'];mode=r['mode'];codes=regions[r['region']]
   def share(x):return 100*sum(val(v,role,mode) for c,v in x['countries'].items() if c in codes)/val(x['world'],role,mode)
   n=sum(val(v,role,mode) for c,v in w['countries'].items() if c in codes);den=val(w['world'],role,mode);assert (n,den)==(int(r['numerator']),int(r['world']));close(share(w),float(r['share']))
   if grain=='days':
    ww=[lookup.get(j) for j in range(i-6,i+1)]
    if all(x and x['sensitivity_eligible'] and val(x['world'],role,mode)>0 for x in ww):close(sum(share(x) for x in ww)/7,float(r['mean7']))
    else:assert not r['mean7']
   checks[grain+'_rows']+=1
 for pair in load_json(run/'pair-windows.json'):
  assert pair['full']==sorted(set.intersection(*[{w['index'] for w in objects[k]['weeks']} for k in pair['keys']]))
  assert pair['full_window_complete']==(len(pair['full'])==26)
  assert pair['jointly_eligible']==sorted(set.intersection(*[{w['index'] for w in objects[k]['weeks'] if w['sensitivity_eligible']} for k in pair['keys']]))
 for r in csvrows(run/'pair-summaries.csv'):
  ii=list(map(int,r['weeks'].split('|')));ww=[w for w in objects[r['key']]['weeks'] if w['index'] in ii];codes=regions[r['region']];role=r['role'];mode=r['mode'];den=sum(val(w['world'],role,mode) for w in ww);n=sum(val(v,role,mode) for w in ww for c,v in w['countries'].items() if c in codes)
  assert (den,n)==(int(r['world']),int(r['numerator']));close(100*n/den,float(r['share']));checks['pair_rows']+=1
 for mm in load_json(run/'map-manifest.json'):
  doc=load_json(run/mm['file']);codes=mm['country_codes'];weeks=mm['weeks'];lr=[{w['index']:w for w in objects[k]['weeks']} for k in [mm['left'],mm['right']]];full=set()
  for f in doc['features']:
   pp=f['properties'];h=pp['h3'];common=[i for i in weeks if all(any(c in codes for c in w[i]['cells'].get(h,{}).get('country_values',{})) for w in lr)]
   assert len(common)==pp['common_intervals'];assert pp['full_window_comparable']==(len(common)==len(weeks))
   if len(common)==len(weeks):full.add(h)
   for role in ['downloaders','uploaders']:
    for mode in ['all','without-hosting']:
     stem=role+'_'+mode;vv=[];shares=[[],[]]
     for i in common:
      ss=[]
      for side,w in enumerate(lr):
       cv=w[i]['cells'][h]['country_values'];n=sum(val(v,role,mode) for c,v in cv.items() if c in codes);ss.append(100*n/val(w[i]['world'],role,mode));shares[side].append(ss[-1])
      vv.append(ss[0]-ss[1])
     if len(common)==len(weeks):
      close(pp[stem+'_delta_pp'],sum(vv)/len(vv))
      for side in [0,1]:close(pp[stem+('_left_share' if side==0 else '_right_share')],sum(shares[side])/len(shares[side]))
     else:assert pp[stem+'_delta_pp'] is None
     if common:close(pp[stem+'_observed_common_delta_pp'],sum(vv)/len(vv))
     else:assert pp[stem+'_observed_common_delta_pp'] is None
   checks['h3_cells']+=1
  assert len(full)==mm['full_comparable_cells']
  for r in mm['weight_coverage']:
   ww=lr[0 if r['side']=='left' else 1];n=sum(val(v,r['role'],r['mode']) for i in weeks for h,c in ww[i]['cells'].items() if h in full for code,v in c['country_values'].items() if code in codes);assert n==r['full_mask_weight'];assert r['full_mask_weight']+r['outside_full_mask_weight']==r['world_weight']
 historical=load_json(run/'historical/mellon-7.6-analysis.json')['objects'];current=load_json(run/'city-objects.json')
 for key,obj in current.items():
  for role in ['downloaders','uploaders']:
   for field in ['size','hosting']:assert obj['world'][role][field]==sum(w['world'][role][field] for w in objects[key]['weeks'])
  city_totals=defaultdict(int)
  for w in objects[key]['weeks']:
   for c in w['cities']:
    for role in ['downloaders','uploaders']:
     for field in ['size','hosting']:city_totals[c['id'],role,field]+=c[role][field]
  for c in obj['cities']:
   for role in ['downloaders','uploaders']:
    for field in ['size','hosting']:assert c[role][field]==city_totals[c['id'],role,field]
 for old,saved in [(historical,load_json(run/'selected-cities-historical.json')),(current,load_json(run/'selected-cities.json'))]:
  for pair in m['pairs']:
   if pair['id'] not in saved:continue
   left,right=[old[k] for k in pair['keys']];aa={r['id']:r for r in left['cities']};bb={r['id']:r for r in right['cities']};eligible=[]
   for key in sorted(aa.keys()&bb.keys()):
    x,y=aa[key],bb[key]
    if not key.split(':')[1].isdigit() or int(key.split(':')[1])<=0 or x['downloaders']['size']+y['downloaders']['size']<100:continue
    delta=100*x['downloaders']['size']/left['world']['downloaders']['size']-100*y['downloaders']['size']/right['world']['downloaders']['size'];eligible.append((key,x['country'],delta))
   selected=[]
   for country in left['countries']:
    selected+=sorted([x for x in eligible if x[1]==country and x[2]>0],key=lambda x:(-x[2],x[0]))[:2];selected+=sorted([x for x in eligible if x[1]==country and x[2]<0],key=lambda x:(x[2],x[0]))[:2]
   assert [x[0] for x in selected]==[x['id'] for x in saved[pair['id']]]
   for x,y in zip(selected,saved[pair['id']]):close(x[2],y['delta']);checks['selected_city_values']+=1
 receipt={'status':'passed','checks':dict(checks),'limits':'Cache IP geolocation is checked by separate native accounting and database hash, not independently replicated.'};dump(run/'validation-receipt.json',receipt);print(json.dumps(receipt),flush=True)
if __name__=='__main__':main()
