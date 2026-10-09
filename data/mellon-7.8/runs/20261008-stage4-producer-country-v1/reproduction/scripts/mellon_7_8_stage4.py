"""Stage 4 producer-country study: frozen selection and interval reductions.

Only top-level aggregate features contribute. Exact producer tags and sourced
company countries are independent of the USA Production platform OR rule.
"""
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import date, timedelta
import argparse
import csv
import gzip
import hashlib
import json
import math
import multiprocessing
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ROLES = ('downloaders', 'uploaders')
FIELDS = ('size', 'hosting')
REGIONS = ('asia-28', 'eur-27', 'usa-can', 'other', 'unclassified')


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n')


def load_json(path):
    if path.exists():return json.loads(path.read_text())
    return json.loads(gzip.decompress(path.with_suffix(path.suffix+'.gz').read_bytes()))


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


def normalize(tag):
    return ' '.join(tag.lower().split())


def classify(record, companies):
    tags = sorted(set(normalize(t) for t in record.get('production_tags', [])))
    resolved = [{'tag':t, **companies[t]} for t in tags if t in companies]
    unresolved = [t for t in tags if t not in companies]
    countries = sorted({c for x in resolved for c in x['country_codes']})
    # Structured relationships supersede incomplete tag-only evidence.
    pending = [r['organization_id'] for r in record.get('organization_relationships', [])
               if r['role'] in ('production_company','animation_studio')]
    complete = bool(tags) and not unresolved and not pending
    group = 'unknown'
    if complete:
        group = 'usa-only' if countries == ['USA'] else 'mixed' if 'USA' in countries else 'non-usa-only'
    return {'group':group, 'listed_credit_coverage_complete':complete,
            'known_countries':countries, 'resolved':resolved, 'unresolved_tags':unresolved,
            'structured_relationships_requiring_review':pending,
            'reason': 'all-listed-tags-mapped' if complete else 'unresolved-company-country-or-scope'}


def genre_family(genres):
    text = ' '.join(genres).lower()
    for family, words in [('animation',['animation','animated','anime']),('action',['action','superhero','martial']),
                          ('comedy',['comedy','sitcom']),('drama',['drama']),('thriller',['thriller']),
                          ('science-fiction',['science fiction','science fantasy']),('fantasy',['fantasy'])]:
        if any(w in text for w in words): return family
    return None


def freeze(source_root, out, policy_path):
    policy = json.loads(policy_path.read_text())
    m = source_root/'alpha60-swarm-metadata'
    report_path = m/'reports/candidates/h15-v3.generated.json'
    report = json.loads(report_path.read_text())
    slices = {s['slice_key']:{c['collection_key']:c for c in s['candidates']} for s in report['slices']}
    population = [c for c in slices['aapi-led'].values() if c['disposition']=='confirmed'
                  and c['reviewed_counts']['actors']+c['reviewed_counts']['creators']>=2]
    region_path = source_root/'alpha60-results/data/region-ranking-definitions.json'
    rd = json.loads(region_path.read_text())
    regions = {r:rd['regions'][r] for r in REGIONS[:3]}
    sets = [set(v['country_codes']) for v in regions.values()]
    assert list(map(len,sets)) == [28,27,2]
    assert all(not sets[i]&sets[j] for i in range(3) for j in range(i))
    repos = {int(p.name[-4:]):p for p in source_root.glob('alpha60-results-20*')
             if re.fullmatch('alpha60-results-20[0-9]{2}',p.name)}
    commits = {p.name:git(p,'rev-parse','HEAD') for p in [m,region_path.parents[1],*repos.values()]}
    rows=[]; inputs=[]
    for c in sorted(population,key=lambda c:c['collection_key']):
        key=c['collection_key']; p=m/'metadata'/(key+'.json'); d=json.loads(p.read_text())
        evidence=classify(d,policy['companies'])
        years=[y for y,p in repos.items() if (p/'data/json'/(key+'-cumulative.json')).exists()]
        assert len(years)==1,(key,years)
        year=years[0];repo=repos[year];meta=repo/'data/json'/(key+'-cumulative.json');am=json.loads(meta.read_text())
        audit=repo/'docs/itemized'/(key+'-sample-cache-audit.md')
        lines=audit.read_text().splitlines() if audit.exists() else []
        notes=[l for l in lines if 'missing' in l.lower() or 'hourly gap:' in l.lower()]
        asian=slices['asian-led-global'].get(key,{})
        ag=asian.get('reviewed_counts',{})
        row={'key':key,'label':d['collection_name'],'sample_year':year,'scope':d['media_object']['type'],
             'canonical_work':d['media_object'].get('canonical_work_key') or key,
             'credit_scope':d['media_object']['credit_scope'],'scope_alignment':c['scope_alignment'],
             'languages':sorted(set(d['release']['original_languages'])),
             'genre_family':policy['genre_overrides'].get(key,{}).get('value') or genre_family(d['release']['genres']),
             'genre_source':policy['genre_overrides'].get(key),
             'producer':evidence,'title_origin_fallback':d['release']['countries_of_origin'],
             'usa_production':c['usa_production'],'threshold':c['reviewed_counts']['actors']+c['reviewed_counts']['creators'],
             'asian_global_eligible':asian.get('disposition')=='confirmed' and ag.get('actors',0)+ag.get('creators',0)>=2,
             'title_sources':d['enrichment']['sources'],'sample_duration':am['sample_duration'],
             'export_version':am['data_version'],'geolocation_version':am.get('ip_geolocation_version'),
             'coverage_notes':notes,'audit_available':audit.exists(),'weekly_available':[], 'weekly_missing':[]}
        for i in range(1,policy['cohort_weeks']+1):
            (row['weekly_available'] if (repo/'data/geojson.week'/f'{key}-week-{i:05d}.geojson.gz').exists() else row['weekly_missing']).append(i)
        rows.append(row)
        for path,rep in [(p,m),(meta,repo),*([(audit,repo)] if audit.exists() else [])]:
            inputs.append({'repository':rep.name,'path':str(path.relative_to(rep)),'sha256':sha(path)})
    for path,rep in [(report_path,m),(region_path,region_path.parents[1])]:inputs.append({'repository':rep.name,'path':str(path.relative_to(rep)),'sha256':sha(path)})
    # Reject a pin that conceals changes to any selected input.
    for rep_name in commits:
        selected={x['path'] for x in inputs if x['repository']==rep_name}
        dirty=git(source_root/rep_name,'status','--porcelain','--untracked-files=no').splitlines()
        assert not any(line[3:] in selected for line in dirty),(rep_name,dirty)
    manifest={'run_id':policy['run_id'],'policy_sha256':sha(policy_path),'policy':policy,'source_commits':commits,
              'metadata_definition':report['definition_id'],'region_definition':rd['definition_id'],
              'region_definition_digest':rd['definition_sha256'],'regions':regions,'inputs':inputs,'objects':rows}
    dump(out/'selection-manifest.json',manifest)
    dump(out/'producer-country-policy.json',policy)
    dump(out/'region-definitions.json',{'definition_id':rd['definition_id'],'source_digest':rd['definition_sha256'],'regions':regions})
    print(json.dumps({'population':len(rows),'groups':dict(Counter(r['producer']['group'] for r in rows)),
                      'eight_week_file_coverage':sum(not r['weekly_missing'] for r in rows)},indent=2))


def read_top(path):
    """Read aggregate object while skipping its large, non-additive BTIH member.

    Exporter writes top-level features before collection_week_by_btiha.
    This exact delimiter is outside the feature array; json.loads verifies the
    resulting aggregate. Tests compare this path with whole-document decoding.
    """
    marker=',"collection_week_by_btiha"'
    with gzip.open(path,'rt') as f:
        text=''
        while True:
            chunk=f.read(1024*1024)
            if not chunk: break
            text+=chunk
            pos=text.find(marker)
            if pos>=0:
                text=text[:pos]+'}'
                break
    return json.loads(text)


def empty(): return {role:{field:0 for field in FIELDS} for role in ROLES}

def add(to, values):
    for r in ROLES:
        for f in FIELDS: to[r][f]+=values[r][f]

def total(rows):
    result=empty()
    for row in rows:add(result,row)
    return result


def excluded_by_audit(start,end,notes):
    for note in notes:
        dates=re.findall(r'\d{4}-\d{2}-\d{2}',note)
        if dates and min(dates)<=end and max(dates)>=start:return True
    return False


def reduce_one(job):
    root,out,row,regions,policy=job;root=Path(root);out=Path(out);key=row['key']
    repo=root/f"alpha60-results-{row['sample_year']}"
    maxweeks=policy['pair_weeks'] if key in policy['daily_keys'] else policy['cohort_weeks']
    # Cell data for the named pair and every fully mapped cohort member.
    cells_needed=key in policy['daily_keys'] or row['producer']['listed_credit_coverage_complete']
    result={'key':key,'weeks':[],'days':[],'inputs':[],'issues':[]}
    start_date=date.fromisoformat(row['sample_duration'][:10]);end_date=date.fromisoformat(row['sample_duration'][-10:])
    for mode,count in [('week',maxweeks),('day',policy['daily_days'] if key in policy['daily_keys'] else policy['cohort_daily_days'])]:
        for index in range(1,count+1):
            relative=f'data/geojson.{mode}/{key}-{mode}-{index:05d}.geojson.gz';path=repo/relative
            if not path.exists():
                result['issues'].append({'type':'missing-file','mode':mode,'index':index});continue
            result['inputs'].append({'repository':repo.name,'path':relative,'sha256':sha(path)})
            doc=read_top(path)
            expected_start=start_date+timedelta(days=(index-1)*(7 if mode=='week' else 1))
            expected_end=min(expected_start+timedelta(days=6 if mode=='week' else 0),end_date)
            errors=[]
            if doc.get('id')!=key or doc.get('duration_type')!=mode or doc.get('duration_index')!=index:errors.append('identity-or-interval-mismatch')
            if doc.get('swarm_hexagon_resolution')!=5 or doc.get('swarm_size_min')!=3:errors.append('resolution-or-threshold-mismatch')
            dates=doc.get('datestamp','');actual_start=dates[:10];actual_end=dates.removesuffix('-partial')[-10:]
            if actual_start!=str(expected_start) or actual_end!=str(expected_start+timedelta(days=6 if mode=='week' else 0)):errors.append('calendar-mismatch')
            if errors:
                result['issues'].append({'type':'invalid-file','mode':mode,'index':index,'errors':errors});continue
            countries={};cells={};world=empty();invalid_h3=empty()
            for feature in doc['features']:
                p=feature['properties'];code=p.get('country_code') or 'UNCLASSIFIED'
                for role in ROLES:
                    assert all(isinstance(p[role][f],int) and p[role][f]>=0 for f in FIELDS)
                    assert p[role]['hosting']<=p[role]['size']
                add(world,p);add(countries.setdefault(code,empty()),p)
                if cells_needed and mode=='week':
                    h=p.get('h3_hexagon',0)
                    if isinstance(h,int) and h>0 and ((h>>52)&15)==5:
                        cell=cells.setdefault(format(h,'x'),{'values':empty(),'countries':set()})
                        add(cell['values'],p);cell['countries'].add(code)
                    else:add(invalid_h3,p)
            partition={g:empty() for g in REGIONS}
            for code,values in countries.items():
                group=next((g for g,codes in regions.items() if code in codes),None)
                group=group or ('unclassified' if not re.fullmatch('[A-Z]{3}',code) or code in ('UNK','XXX','ZZZ','UNCLASSIFIED') else 'other')
                add(partition[group],values)
            assert total(partition.values())==world
            for c in cells.values():c['countries']=sorted(c['countries'])
            if cells_needed and mode=='week':assert total([c['values'] for c in cells.values()]+[invalid_h3])==world
            partial=mode=='week' and (expected_end-expected_start).days!=6
            audit_gap=excluded_by_audit(str(expected_start),str(expected_end),row['coverage_notes'])
            result['weeks' if mode=='week' else 'days'].append({'index':index,'dates':dates,'start':str(expected_start),'end':str(expected_end),
                 'partial':partial,'opening_flag':dates.endswith('-partial') or (mode=='day' and (index==1 or expected_end==end_date)),'audit_gap':audit_gap,
                 'sensitivity_eligible':not(partial or audit_gap or dates.endswith('-partial') or (mode=='day' and (index==1 or expected_end==end_date))),
                 'world':world,'regions':partition,'countries':countries,**({'cells':cells,'invalid_h3':invalid_h3} if cells_needed and mode=='week' else {})})
    dump(out/'objects'/(key+'.json'),result)
    return {'key':key,'weeks':len(result['weeks']),'days':len(result['days']),'issues':len(result['issues'])}


def calculate(root,out,workers):
    manifest=json.loads((out/'selection-manifest.json').read_text())
    assert manifest['policy']==json.loads((out/'producer-country-policy.json').read_text())
    regions={k:set(v['country_codes']) for k,v in manifest['regions'].items()}
    jobs=[(str(root),str(out),row,regions,manifest['policy']) for row in manifest['objects']]
    with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context('fork')) as pool:
        for i,result in enumerate(pool.map(reduce_one,jobs),1):
            if i%10==0 or result['issues']:print(i,result,flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['freeze','calculate']);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--workers',type=int,default=3)
    p.add_argument('--policy',type=Path,default=ROOT/'config/mellon-7.8/stage-4/producer-country-policy.json');a=p.parse_args()
    if a.phase=='freeze':freeze(a.source_root,a.out,a.policy)
    else:calculate(a.source_root,a.out,a.workers)

if __name__=='__main__':main()
