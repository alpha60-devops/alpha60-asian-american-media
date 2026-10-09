#!/usr/bin/env python3
"""Freeze and reduce the approved Gojira case comparisons from latest exports."""
import argparse
from concurrent.futures import ProcessPoolExecutor
from datetime import date
import importlib.util
import json
import multiprocessing
from pathlib import Path
import shutil
from mellon_7_8_stage4 import dump, sha, git, reduce_one, load_json, total, empty, add, ROLES

ROOT=Path(__file__).resolve().parents[1]
RUN_ID='20261008-stage5-gojira-v1'

def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

A=module('analyze-mellon-7-8-stage4')
LEGACY=module('render-mellon-7-6-aapi')

def regional(w,codes):return total(v for c,v in w['countries'].items() if c in codes)

def filtered(rows,codes):
    result=[]
    for w in rows:
        cells={}
        for h,c in w['cells'].items():
            cc={k:v for k,v in c['country_values'].items() if k in codes}
            if cc:cells[h]={'values':total(cc.values()),'countries':sorted(cc)}
        result.append({**w,'cells':cells})
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,required=True);p.add_argument('--site',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--workers',type=int,default=2);a=p.parse_args();out=a.run;out.mkdir(parents=True,exist_ok=True)
    ledger=a.site/'data/mellon-7.6-analysis.json';old=json.loads(ledger.read_text());keys=old['groups']['godzilla'];regions_doc=load_json(a.sources/'alpha60-results/data/region-ranking-definitions.json');regions={k:regions_doc['regions'][k]['country_codes'] for k in ['asia-28','eur-27','usa-can']}
    assert len(set(regions['asia-28']))==28 and {'MAC','TWN'}<=set(regions['asia-28'])
    policy={'pair_weeks':26,'cohort_weeks':26,'daily_keys':keys,'daily_days':105,'cohort_daily_days':105,'cell_country_values':True,'city_keys':keys[:3]}
    rows=[];inputs=[]
    for key in keys:
        oldrow=old['objects'][key];repo=a.sources/f"alpha60-results-{oldrow['year']}"
        meta_path=repo/f'data/json/{key}-cumulative.json';meta=load_json(meta_path)
        audit_path=repo/f'docs/itemized/{key}-sample-cache-audit.md';audit=audit_path.read_text()
        scope='film' if key.startswith('godzilla') else 'one episode' if key.endswith('110') else 'three episodes'
        label={'monarch-legacy-of-monsters-101':'Monarch 101–103','monarch-legacy-of-monsters-201':'Monarch 201–203','monarch-legacy-of-monsters-208':'Monarch 208–210','godzilla-x-kong-the-new-empire':'The New Empire'}.get(key,oldrow['label'])
        rows.append({'key':key,'label':label,'scope':scope,'sample_year':oldrow['year'],'sample_duration':meta['sample_duration'],'source_revision':git(repo,'rev-parse','HEAD'),'companion_export_version':meta['data_version'],'geolocation_version':meta['ip_geolocation_version'],'coverage_notes':[l for l in audit.splitlines() if 'missing' in l.lower() or 'hourly gap:' in l],'producer':{'listed_credit_coverage_complete':False}})
        for path in [meta_path,audit_path]:inputs.append({'repository':repo.name,'path':str(path.relative_to(repo)),'sha256':sha(path)})
    assert len({r['geolocation_version'] for r in rows})==1
    pairs=[{'id':'films','keys':keys[:2]},{'id':'monarch','keys':keys[5:7]},{'id':'historical-film','keys':[keys[0],keys[2]]},{'id':'earlier-season','keys':[keys[5],keys[3]]},{'id':'single-episode-context','keys':[keys[5],keys[4]]}]
    manifest={'run_id':RUN_ID,'created':str(date.today()),'policy':policy,'objects':rows,'pairs':pairs,'regions':regions_doc['regions'],'regions_sha256':sha(a.sources/'alpha60-results/data/region-ranking-definitions.json'),'latest_policy':'Latest upstream main revisions checked before freeze; exact selected files hashed. GeoJSON embedded export version is separate from companion JSON version.','methods':{'weekly':'pooled interval geographic weights / matching worldwide weights','h3':'mean of aligned weekly cell-share differences; exact country-assigned contributions; both sides observed every selected interval','daily':'observed day share and trailing mean of seven consecutive eligible days; no interpolation','timezone':'source date labels; exporter does not certify UTC','inference':'descriptive case comparisons, no work-level bootstrap or causal production-country claim'}}
    dump(out/'selection-manifest.json',manifest);dump(out/'region-definitions.json',regions_doc);dump(out/'region-definition.json',{'regions':[{'id':'asia-28','name':'Asia-28','country_codes':regions['asia-28']}]})
    history=out/'historical';history.mkdir(exist_ok=True)
    shutil.copyfile(ledger,history/'mellon-7.6-analysis.json')
    historical_page=a.site/'docs/godzilla-20261008-historical.md'
    shutil.copyfile(historical_page if historical_page.exists() else a.site/'docs/godzilla.md',history/'godzilla-20261008.md')
    jobs=[(str(a.sources),str(out),r,{k:set(v) for k,v in regions.items()},policy) for r in rows]
    with ProcessPoolExecutor(max_workers=a.workers, mp_context=multiprocessing.get_context("fork")) as pool:
        for status in pool.map(reduce_one,jobs):print(status,flush=True)
    data={k:load_json(out/'objects'/f'{k}.json') for k in keys}
    versions={w['export_version'] for v in data.values() for mode in ['weeks','days'] for w in v[mode]};assert len(versions)==1,versions
    for k,v in data.items():
        assert [w['index'] for w in v['weeks']]==list(range(1,len(v['weeks'])+1)),k
        if k in keys[:3]:assert len(v['weeks'])==26,k
        inputs+=v['inputs']
    for year in sorted({r['sample_year'] for r in rows}):
        repo=a.sources/f'alpha60-results-{year}'
        paths=[x['path'] for x in inputs if x['repository']==repo.name]
        assert not git(repo,'status','--porcelain','--',*paths),'selected source files must match the frozen revision'
    # The film symbol-only revision must still match its historical inputs.
    for key in keys[:3]:
        for source in old['objects'][key]['sources']:
            if '/geojson.week/' in source['path']:
                assert sha(a.sources/f"alpha60-results-{old['objects'][key]['year']}"/source['path'])==source['sha256']
    dump(out/'input-manifest.json',{'inputs':inputs,'geojson_versions':sorted(versions),'companion_versions':sorted({r['companion_export_version'] for r in rows}),'geolocation_versions':sorted({r['geolocation_version'] for r in rows})})
    views={c:[c] for c in ['JPN','USA','CHN','KOR']};views.update(regions)
    weekly=[];daily=[];coverage=[];summaries=[];pair_windows=[]
    for key,d in data.items():
        for mode in ['weeks','days']:
            byindex={w['index']:w for w in d[mode]}
            for i in range(1,(26 if mode=='weeks' else 105)+1):
                w=byindex.get(i);coverage.append({'key':key,'mode':mode,'index':i,'available':w is not None,'dates':w['dates'] if w else None,'eligible':w['sensitivity_eligible'] if w else False,'boundary_flag':w['opening_flag'] if w else None,'audit_gap':w['audit_gap'] if w else None})
                if not w:continue
                for region,codes in views.items():
                    for role in ROLES:
                        for treatment in ['all','without-hosting']:
                            n=A.value(regional(w,codes),role,treatment);den=A.value(w['world'],role,treatment)
                            row={'key':key,'index':i,'dates':w['dates'],'region':region,'role':role,'mode':treatment,'numerator':n,'world':den,'share':A.ratio(n,den),'eligible':w['sensitivity_eligible']}
                            if mode=='days':
                                window=[byindex.get(j) for j in range(i-6,i+1)]
                                values=[A.ratio(A.value(regional(x,codes),role,treatment),A.value(x['world'],role,treatment)) for x in window if x and x['sensitivity_eligible']]
                                row['mean7']=sum(values)/7 if len(values)==7 and None not in values else None
                                daily.append(row)
                            else:weekly.append(row)
    for pair in pairs:
        kk=pair['keys'];common=sorted(set.intersection(*[{w['index'] for w in data[k]['weeks'] if w['sensitivity_eligible']} for k in kk]))
        available=sorted(set.intersection(*[{w['index'] for w in data[k]['weeks']} for k in kk]))
        missing={k:sorted(set(range(1,27))-{w['index'] for w in data[k]['weeks']}) for k in kk}
        pair_windows.append({**pair,'requested':list(range(1,27)),'full':available,'full_window_complete':len(available)==26,'missing_intervals':missing,'jointly_eligible':common})
        for window,indices in [('full',available),('jointly-eligible',common)]:
            for key in kk:
                ww=[w for w in data[key]['weeks'] if w['index'] in indices]
                for region,codes in views.items():
                    for role in ROLES:
                        for treatment in ['all','without-hosting']:
                            n=sum(A.value(regional(w,codes),role,treatment) for w in ww);den=sum(A.value(w['world'],role,treatment) for w in ww)
                            full=sum(A.value(w['world'],role,treatment) for w in data[key]['weeks'])
                            summaries.append({'pair':pair['id'],'window':window,'weeks':'|'.join(map(str,indices)),'key':key,'region':region,'role':role,'mode':treatment,'numerator':n,'world':den,'share':A.ratio(n,den),'world_weight_retained_pct':A.ratio(den,full)})
    for name,values in [('weekly-regions',weekly),('daily-regions',daily),('coverage',coverage),('pair-summaries',summaries)]:A.write_csv(out/(name+'.csv'),values)
    dump(out/'pair-windows.json',pair_windows)
    maps=[];h3=A.H3()
    for region,codes in [('JPN',['JPN']),('asia-28',regions['asia-28'])]:
        left,right=[filtered(data[k]['weeks'],codes) for k in keys[:2]]
        for window,indices in [('full',list(range(1,27))),('jointly-eligible',pair_windows[0]['jointly_eligible'])]:
            assert indices
            name=f'h3-films-{region.lower()}-{window}'
            maps.append({'file':name+'.geojson',**A.difference_map(out,name,[[w for w in left if w['index'] in indices]],[[w for w in right if w['index'] in indices]],indices,{'region':region,'country_codes':codes,'left':keys[0],'right':keys[1],'window':window,'geolocation_version':rows[0]['geolocation_version'],'geojson_version':next(iter(versions))},h3)})
            for support in maps[-1]['weight_coverage']:
                selected_rows=left if support['side']=='left' else right
                n=sum(A.value(regional(w,codes),support['role'],support['mode']) for w in selected_rows if w['index'] in indices)
                support['regional_weight']=n
                support['full_mask_regional_share']=A.ratio(support['full_mask_weight'],n)
            document=load_json(out/(name+'.geojson'))
            document['metadata']=maps[-1].copy()
            (out/(name+'.geojson')).write_text(json.dumps(document,separators=(',',':'),allow_nan=False)+'\n')
            print(name,maps[-1]['full_comparable_cells'],maps[-1]['union_cells'],flush=True)
    dump(out/'map-manifest.json',maps)
    # Exactly the historical shared-city eligibility and ranking; values unchanged.
    selected={p['id']:LEGACY.locations(old['objects'][p['keys'][0]],old['objects'][p['keys'][1]]) for p in pairs[:3]}
    dump(out/'selected-cities-historical.json',selected)
    city_objects={}
    for key in keys[:3]:
        cities={}
        for w in data[key]['weeks']:
            for c in w['cities']:
                entry=cities.setdefault(c['id'],{k:c[k] for k in ['id','city','country','coordinates']})
                if 'downloaders' not in entry:entry.update(empty())
                add(entry,c)
        city_objects[key]={'label':next(r['label'] for r in rows if r['key']==key),'countries':['JPN','USA','CHN','KOR'],'weeks':[w['index'] for w in data[key]['weeks']],'world':total(w['world'] for w in data[key]['weeks']),'cities':list(cities.values())}
    dump(out/'city-objects.json',city_objects)
    dump(out/'selected-cities.json',{p['id']:LEGACY.locations(*(city_objects[k] for k in p['keys'])) for p in pairs if all(k in city_objects for k in p['keys'])})
    diagnostic=[r for r in daily if r['key']=='godzilla-vs-kong' and r['region']=='USA' and r['role']=='downloaders' and r['mode']=='all' and 28<=r['index']<=35]
    dump(out/'daily-assessment.json',{'decision':'Weekly presentation; validated daily data remain downloadable.','reason':'Daily Vs. Kong refines the late-April onset but confirms the sustained USA shift already visible in weeks four and five; it does not establish an event cause.','daily_evidence':diagnostic,'weekly_shares':[r['share'] for r in weekly if r['key']=='godzilla-vs-kong' and r['region']=='USA' and r['role']=='downloaders' and r['mode']=='all' and r['index'] in [4,5]]})
    shutil.copyfile(ROOT/'config/mellon-7.8/stage-5/release-context.json',out/'release-context.json')
    dump(out/'analysis-receipt.json',{'status':'computed','weekly_rows':len(weekly),'daily_rows':len(daily),'coverage_rows':len(coverage),'summary_rows':len(summaries),'daily_files':{k:len(v['days']) for k,v in data.items()},'issues':{k:v['issues'] for k,v in data.items()},'historical_sha256':sha(history/'mellon-7.6-analysis.json'),'limitations':['Film cumulative caches and weekly windows span the same 26 weeks but use different aggregation grains. Monarch pairs use their common available weeks: 24 for 201/208 and 21 for 201/110. Daily diagnostics cover the original first 105 days.','2024 daily geographic exports are unavailable at the selected latest source revisions.','H3 common masks may be sparse; missing and suppressed cells are not zeros.']})
    print('Stage 5 reductions complete',flush=True)

if __name__=='__main__':main()
