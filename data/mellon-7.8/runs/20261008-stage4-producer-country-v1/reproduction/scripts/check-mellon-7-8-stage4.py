#!/usr/bin/env python3
"""Independent reconciliation of selection, sources, calculations and map masks."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path
import subprocess
from statistics import mean, median
from mellon_7_8_stage4 import load_json


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--source-root',type=Path,required=True);a=p.parse_args();run=a.run;root=a.source_root
    m=json.loads((run/'selection-manifest.json').read_text());policy=m['policy'];inputs=json.loads((run/'input-manifest.json').read_text())
    report=json.loads((root/'alpha60-swarm-metadata/reports/candidates/h15-v3.generated.json').read_text())
    population={c['collection_key']:c for s in report['slices'] if s['slice_key']=='aapi-led' for c in s['candidates'] if c['disposition']=='confirmed' and c['reviewed_counts']['actors']+c['reviewed_counts']['creators']>=2}
    objects={r['key']:r for r in m['objects']};assert set(objects)==set(population) and len(objects)==200
    assert digest(run/'producer-country-policy.json')==m['policy_sha256']
    codes={k:set(v['country_codes']) for k,v in m['regions'].items()};assert len(codes['eur-27'])==27 and 'GBR' not in codes['eur-27']
    assert len(codes['asia-28'])==28 and {'MAC','TWN'}<=codes['asia-28'] and codes['usa-can']=={'USA','CAN'}
    assert all(not codes[a]&codes[b] for a in codes for b in codes if a!=b)
    for k,row in objects.items():
        canonical=json.loads((root/'alpha60-swarm-metadata/metadata'/(k+'.json')).read_text())
        tags=set(' '.join(x.lower().split()) for x in canonical['production_tags']);known=set();missing=[]
        for tag in tags:
            if tag in policy['companies']:known.update(policy['companies'][tag]['country_codes'])
            else:missing.append(tag)
        pending=any(r['role'] in ['production_company','animation_studio'] for r in canonical.get('organization_relationships',[]))
        group='unknown'
        if tags and not missing and not pending:group='mixed' if 'USA' in known and len(known)>1 else 'usa-only' if known=={'USA'} else 'non-usa-only'
        assert row['producer']['group']==group and row['producer']['known_countries']==sorted(known)
        assert row['usa_production']==population[k]['usa_production']
    for s in inputs['inputs']:assert digest(root/s['repository']/s['path'])==s['sha256'],s['path']
    # Verify that revision pins do not conceal local changes or untracked inputs.
    for repo,head in m['source_commits'].items():
        assert subprocess.check_output(['git','-C',str(root/repo),'rev-parse','HEAD'],text=True).strip()==head
        paths={s['path'] for s in inputs['inputs'] if s['repository']==repo}
        tracked=set(subprocess.check_output(['git','-C',str(root/repo),'ls-files'],text=True).splitlines());assert paths<=tracked
        dirty=subprocess.check_output(['git','-C',str(root/repo),'status','--porcelain','--untracked-files=no'],text=True).splitlines()
        assert not any(line[3:] in paths for line in dirty)
    data={k:load_json(run/'objects'/(k+'.json')) for k in objects};intervals=0
    for k,d in data.items():
        for w in d['weeks']+d['days']:
            intervals+=1
            for role in ['downloaders','uploaders']:
                for field in ['size','hosting']:
                    expected=sum(v[role][field] for v in w['countries'].values());assert w['world'][role][field]==expected
                    assert sum(v[role][field] for v in w['regions'].values())==expected
                    for reg,cc in codes.items():assert w['regions'][reg][role][field]==sum(v[role][field] for c,v in w['countries'].items() if c in cc)
                    if 'cells' in w:assert sum(v['values'][role][field] for v in w['cells'].values())+w['invalid_h3'][role][field]==expected
    # Whole-file JSON decoding avoids the optimized reader and independently
    # verifies top-level reduction for both grains and every classified group.
    samples=[('beef-02','day',7),('no-more-bets','day',70),('beef-02','week',15),('no-more-bets','week',15),('eternals','week',8),('fistful-of-vengeance','week',8),('arcane-02.1','week',8),('japan-sinks','week',8)]
    raw_results=[]
    for key,mode,index in samples:
        doc=json.loads(gzip.decompress((root/f"alpha60-results-{objects[key]['sample_year']}"/'data'/('geojson.'+mode)/f'{key}-{mode}-{index:05d}.geojson.gz').read_bytes()))
        row=next(w for w in data[key]['weeks' if mode=='week' else 'days'] if w['index']==index)
        for role in ['downloaders','uploaders']:
            for field in ['size','hosting']:
                assert sum(f['properties'][role][field] for f in doc['features'])==row['world'][role][field]
                for reg,cc in codes.items():assert sum(f['properties'][role][field] for f in doc['features'] if f['properties']['country_code'] in cc)==row['regions'][reg][role][field]
        raw_results.append({'key':key,'mode':mode,'index':index,'features':len(doc['features'])})
        del doc
    weekly=list(csv.DictReader((run/'weekly-regions.csv').open()));perwork=list(csv.DictReader((run/'per-work.csv').open()));daily=list(csv.DictReader((run/'daily-home-country.csv').open()))
    for r in weekly:
        w=next(w for w in data[r['key']]['weeks'] if w['index']==int(r['week']));v=w['regions'][r['region']][r['role']];world=w['world'][r['role']];host=r['mode']=='without-hosting'
        n=v['size']-(v['hosting'] if host else 0);d=world['size']-(world['hosting'] if host else 0)
        assert int(r['weight'])==n and int(r['world_weight'])==d
        assert not r['share'] if not d else math.isclose(float(r['share']),100*n/d)
    for r in perwork:
        weeks=[w for w in data[r['key']]['weeks'] if w['index']<=8 and (r['coverage']=='full' or w['sensitivity_eligible'])]
        host=r['mode']=='without-hosting';role=r['role'];reg=r['region']
        n=sum(w['regions'][reg][role]['size']-(w['regions'][reg][role]['hosting'] if host else 0) for w in weeks)
        d=sum(w['world'][role]['size']-(w['world'][role]['hosting'] if host else 0) for w in weeks)
        assert int(r['weight'])==n and int(r['world_weight'])==d and int(r['intervals'])==len(weeks)
    for r in daily:
        dd={w['index']:w for w in data[r['key']]['days']};i=int(r['day']);host=r['mode']=='without-hosting';role=r['role'];home=r['home_countries'].split('|')
        def share(w):
            den=w['world'][role]['size']-(w['world'][role]['hosting'] if host else 0)
            num=sum(w['countries'].get(c,{}).get(role,{}).get('size',0)-(w['countries'].get(c,{}).get(role,{}).get('hosting',0) if host else 0) for c in home)
            return 100*num/den if den else None
        assert math.isclose(float(r['share']),share(dd[i])) if r['share'] else share(dd[i]) is None
        candidates=[dd.get(j) for j in range(i-6,i+1)]
        ok=all(w and w['sensitivity_eligible'] and share(w) is not None for w in candidates)
        if ok:assert math.isclose(float(r['trailing_7_day_share_mean']),mean(share(w) for w in candidates))
        else:assert not r['trailing_7_day_share_mean']
    summaries=json.loads((run/'cohort-summary.json').read_text())
    for s in summaries:
        rr=[r for r in perwork if all(r[k]==s[k] for k in ['group','region','role','mode','coverage']) and r['share'] and (s['population']=='expanded-aapi' or r['asian_global']=='True')]
        assert len(rr)==s['n']
        if rr:
            vals=[float(r['share']) for r in rr];assert math.isclose(mean(vals),s['mean']) and math.isclose(median(vals),s['median'])
            assert math.isclose(100*sum(int(r['weight']) for r in rr)/sum(int(r['world_weight']) for r in rr),s['volume_weighted'])
        if s['clusters']<2:assert s['mean_ci95'] is None
    branches=list(csv.DictReader((run/'evidence-branches.csv').open()))
    assert len(branches)==len(objects) and {r['key'] for r in branches}==set(objects)
    for r in branches:
        obj=objects[r['key']];bases=obj['usa_production']['qualification_basis']
        expected={'known_us_producer':'USA' in obj['producer']['known_countries'],
                  'complete_non_us_producers':obj['producer']['group']=='non-usa-only',
                  'baseline_us_country_or_producer':'reviewed-production-country-or-producer' in bases,
                  'us_commissioner_or_platform':any(x.startswith('platform:') or x.startswith('commissioner:') for x in bases),
                  'frozen_usa_production':obj['usa_production']['value']}
        assert all(r[field]==str(value) for field,value in expected.items())
        assert r['producer_group']==obj['producer']['group']
    branch_summaries=list(csv.DictReader((run/'evidence-branch-regions.csv').open()))
    for s in branch_summaries:
        keys={r['key'] for r in branches if r[s['evidence_branch']]=='True'}
        rr=[r for r in perwork if r['key'] in keys and r['coverage']=='full' and r['share'] and all(r[f]==s[f] for f in ['role','region','mode'])]
        assert int(s['objects'])==len(rr)
        if rr:
            assert math.isclose(float(s['equal_object_mean_share']),mean(float(r['share']) for r in rr))
            assert math.isclose(float(s['volume_weighted_share']),100*sum(int(r['weight']) for r in rr)/sum(int(r['world_weight']) for r in rr))
        else:assert not s['equal_object_mean_share'] and not s['volume_weighted_share']
    expected_strata=defaultdict(lambda:defaultdict(dict))
    for k,obj in sorted(objects.items()):
        weeks=[w for w in data[k]['weeks'] if w['index']<=8]
        complete=[w['index'] for w in weeks if not w['partial']]==list(range(1,9))
        group=obj['producer']['group']
        if complete and group in ['usa-only','non-usa-only'] and obj['languages'] and obj['genre_family']:
            sk=(obj['sample_year'],obj['scope'],tuple(obj['languages']),obj['genre_family'])
            expected_strata[sk][group].setdefault(obj['canonical_work'],k)
    matching=json.loads((run/'matching-manifest.json').read_text())
    assert len(matching)==len(expected_strata)
    for row in matching:
        sk=row['stratum'];key=(sk[0],sk[1],tuple(sk[2]),sk[3])
        expected={g:sorted(v.values()) for g,v in expected_strata[key].items()}
        assert row['groups']==expected
        assert (row['status']=='matched')==bool(expected.get('usa-only') and expected.get('non-usa-only'))
    matched_values=json.loads((run/'matched-comparisons.json').read_text())
    for row in matched_values:
        values=[]
        for side in ['left','right']:
            shares=[]
            for k in row[side]:
                ww=[w for w in data[k]['weeks'] if w['index'] in row['weeks']]
                def amount(v):return v[row['role']]['size']-(v[row['role']]['hosting'] if row['mode']=='without-hosting' else 0)
                den=sum(amount(w['world']) for w in ww)
                shares.append(100*sum(amount(w['regions'][row['region']]) for w in ww)/den if den else None)
            values.append(mean(shares) if all(v is not None for v in shares) else None)
        for side,v in zip(['left','right'],values):
            assert row[side+'_share'] is None if v is None else math.isclose(row[side+'_share'],v)
        if None not in values:assert math.isclose(row['difference_pp'],values[0]-values[1],abs_tol=1e-12)
        if min(len(row['left']),len(row['right']))<2:assert row['ci95'] is None
    dc=list(csv.DictReader((run/'daily-group-coverage.csv').open()))
    assert len(dc)==len(objects)
    day_lookup={k:{w['index']:w for w in d['days'] if w['index']<=policy['cohort_daily_days']} for k,d in data.items()}
    daily_eligible=set()
    for r in dc:
        days=day_lookup[r['key']];missing=sorted(set(range(1,policy['cohort_daily_days']+1))-set(days))
        assert r['missing_days']=='|'.join(map(str,missing)) and int(r['observed_days'])==len(days)
        assert r['complete_window']==str(not missing)
        if not missing:daily_eligible.add(r['key'])
    branch_lookup={r['key']:r for r in branches};daily_buckets=defaultdict(list)
    daily_observations=list(csv.DictReader((run/'daily-group-observations.csv').open()))
    assert len(daily_observations)==sum(len(v) for v in day_lookup.values())*2*2*6
    for r in daily_observations:
        key=r['key'];w=day_lookup[key][int(r['day'])];obj=objects[key];role=r['role'];mode=r['mode'];reg=r['region']
        def val(v):return v[role]['size']-(v[role]['hosting'] if mode=='without-hosting' else 0)
        den=val(w['world'])
        if reg=='producer-home':
            country=obj['producer']['known_countries'] if obj['producer']['group']!='unknown' else None
            num=sum(val(w['countries'][c]) for c in country if c in w['countries']) if country else None
        else:num=val(w['regions'][reg])
        assert int(r['world_weight'])==den
        assert not r['weight'] if num is None else int(r['weight'])==num
        assert not r['share'] if num is None or not den else math.isclose(float(r['share']),100*num/den)
        if key in daily_eligible and r['share']:
            groups=[('producer-group',obj['producer']['group'])]+[('evidence-branch',f) for f in ['known_us_producer','complete_non_us_producers','baseline_us_country_or_producer','us_commissioner_or_platform'] if branch_lookup[key][f]=='True']
            for kind,group in groups:
                for cov in ['full']+(['audit-filtered'] if w['sensitivity_eligible'] else []):
                    daily_buckets[(kind,group,r['day'],role,mode,reg,cov)].append(r)
    daily_summaries=list(csv.DictReader((run/'daily-group-summary.csv').open()))
    assert len(daily_summaries)==len(daily_buckets)
    for r in daily_summaries:
        rr=daily_buckets[tuple(r[f] for f in ['kind','group','day','role','mode','region','coverage'])]
        assert int(r['objects'])==len(rr) and int(r['canonical_works'])==len({objects[x['key']]['canonical_work'] for x in rr})
        assert math.isclose(float(r['equal_object_mean_share']),mean(float(x['share']) for x in rr))
        assert math.isclose(float(r['median_share']),median(float(x['share']) for x in rr))
        assert math.isclose(float(r['volume_weighted_share']),100*sum(int(x['weight']) for x in rr)/sum(int(x['world_weight']) for x in rr))
    maps=[]
    for path in sorted(run.glob('*-h3.geojson')):
        geo=json.loads(path.read_text());meta=geo['metadata'];count=0
        for f in geo['features']:
            p=f['properties'];assert isinstance(p['h3'],str) and ((int(p['h3'],16)>>52)&15)==5
            count+=p['full_window_comparable']
            for role in ['downloaders','uploaders']:
                for mode in ['all','without-hosting']:
                    field=role+'_'+mode+'_delta_pp'
                    if not p['full_window_comparable']:assert p[field] is None
                    if p[field] is not None:assert math.isclose(p[field],p[role+'_'+mode+'_left_share']-p[role+'_'+mode+'_right_share'],abs_tol=1e-12)
            assert f['geometry']['type'] in ['Polygon','MultiPolygon']
            coords=f['geometry']['coordinates'];polys=[coords] if f['geometry']['type']=='Polygon' else coords
            for poly in polys:
                for ring in poly:
                    assert ring[0]==ring[-1] and all(-180<=x<=180 and -90<=y<=90 for x,y in ring)
        assert count==meta['full_comparable_cells'] and len(geo['features'])==meta['union_cells']
        for r in meta['weight_coverage']:assert r['full_mask_weight']+r['outside_full_mask_weight']==r['world_weight']
        maps.append({'file':path.name,'cells':len(geo['features']),'complete_mask':count})
    result={'status':'PASS','population_checked':len(objects),'input_hashes':len(inputs['inputs']),'interval_rollups':intervals,'independent_raw_samples':raw_results,'weekly_rows':len(weekly),'per_work_rows':len(perwork),'daily_rows':len(daily),'cohort_summaries':len(summaries),'map_checks':maps,'limits':['Independent raw reduction samples eight source intervals; all inputs hashed and every saved rollup reconciled.','Producer-country completeness is limited to listed metadata credits and the saved reviewed company mapping.','Single-work matched stratum has no population uncertainty interval.']}
    result.update(evidence_objects=len(branches),evidence_summaries=len(branch_summaries),matching_strata=len(matching),matched_values=len(matched_values))
    result.update(daily_group_observations=len(daily_observations),daily_group_summaries=len(daily_summaries),daily_complete_objects=len(daily_eligible))
    (run/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
