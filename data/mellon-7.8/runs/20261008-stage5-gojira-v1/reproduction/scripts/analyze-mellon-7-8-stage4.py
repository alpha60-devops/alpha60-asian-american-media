#!/usr/bin/env python3
"""Summarize frozen producer cohorts, matched strata, daily and H3 differences."""
from collections import defaultdict, Counter
import argparse
import csv
import ctypes
import ctypes.util
import json
import math
from pathlib import Path
import numpy as np
from mellon_7_8_stage4 import dump, empty, add, total, ROLES, REGIONS, sha, load_json


def ratio(n,d):return 100*n/d if d else None

def value(t,role,mode):return t[role]['size']-(t[role]['hosting'] if mode=='without-hosting' else 0)

def amounts(rows,role,region,mode):
    return sum(value(w['regions'][region],role,mode) for w in rows),sum(value(w['world'],role,mode) for w in rows)

def complete(rows,n):return [w['index'] for w in rows if not w['partial']]==list(range(1,n+1))

def summarize(values,clusters,weights,rng,reps):
    a=np.array(values,dtype=float)
    if not len(a):return {'n':0,'clusters':0,'mean':None,'median':None,'q25':None,'q75':None,'volume_weighted':None,'mean_ci95':None}
    ids=sorted(set(clusters));result={'n':len(a),'clusters':len(ids),'mean':float(a.mean()),'median':float(np.median(a)),
               'q25':float(np.quantile(a,.25)),'q75':float(np.quantile(a,.75)),
               'volume_weighted':float(np.average(a,weights=weights)) if sum(weights) else None,'mean_ci95':None}
    if len(ids)>=2:
        groups={k:a[np.array(clusters)==k] for k in ids}
        draws=[float(np.concatenate([groups[k] for k in rng.choice(ids,len(ids),replace=True)]).mean()) for _ in range(reps)]
        result['mean_ci95']=[float(x) for x in np.quantile(draws,[.025,.975])]
    return result


def write_csv(path,rows):
    if not rows:return
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


class LatLng(ctypes.Structure):_fields_=[('lat',ctypes.c_double),('lng',ctypes.c_double)]
class Boundary(ctypes.Structure):_fields_=[('numVerts',ctypes.c_int),('verts',LatLng*10)]
class H3:
    def __init__(self):
        self.lib=ctypes.CDLL(ctypes.util.find_library('h3'))
        self.lib.cellToBoundary.argtypes=[ctypes.c_uint64,ctypes.POINTER(Boundary)]
        self.lib.cellToBoundary.restype=ctypes.c_uint32
        self.lib.isValidCell.argtypes=[ctypes.c_uint64];self.lib.getResolution.argtypes=[ctypes.c_uint64]
    def polygon(self,h):
        n=int(h,16);assert self.lib.isValidCell(n) and self.lib.getResolution(n)==5
        b=Boundary();assert self.lib.cellToBoundary(n,ctypes.byref(b))==0
        coords=[[math.degrees(p.lng),math.degrees(p.lat)] for p in b.verts[:b.numVerts]]
        # Split antimeridian polygons instead of drawing across the entire world.
        from shapely.geometry import Polygon, box, mapping
        unwrapped=[coords[0]]
        for x,y in coords[1:]:
            while x-unwrapped[-1][0]>180:x-=360
            while x-unwrapped[-1][0]<-180:x+=360
            unwrapped.append([x,y])
        poly=Polygon(unwrapped)
        polys=[]
        for shift in [-360,0,360]:
            from shapely.affinity import translate
            q=translate(poly,xoff=shift).intersection(box(-180,-90,180,90))
            if not q.is_empty:
                polys.extend(list(q.geoms) if q.geom_type=='MultiPolygon' else [q])
        if len(polys)==1:return mapping(polys[0])
        return {'type':'MultiPolygon','coordinates':[mapping(p)['coordinates'] for p in polys]}


def difference_map(out,name,left,right,weeks,metadata,h3):
    # Every work in each side must have a cell in an interval for that interval
    # to be comparable. No unobserved cell receives a synthetic zero.
    allcells=sorted({h for works in [left,right] for rows in works for w in rows for h in w.get('cells',{})})
    features=[];coverage=[]
    for h in allcells:
        props={'h3':h,'countries':sorted({c for works in [left,right] for rows in works for w in rows for c in w.get('cells',{}).get(h,{}).get('countries',[])})}
        common=[];left_seen=right_seen=0
        for i in weeks:
            groups=[]
            for works in [left,right]:groups.append([next(w for w in rows if w['index']==i) for rows in works])
            seen=[all(h in w.get('cells',{}) for w in g) for g in groups]
            left_seen+=seen[0];right_seen+=seen[1]
            if all(seen):common.append((i,groups))
        props.update(common_intervals=len(common),left_observed_intervals=left_seen,right_observed_intervals=right_seen,
                     full_window_comparable=len(common)==len(weeks),expected_intervals=len(weeks))
        for role in ROLES:
            for mode in ['all','without-hosting']:
                deltas=[];ls=[];rs=[]
                for i,groups in common:
                    shares=[]
                    for g in groups:
                        ss=[ratio(value(w['cells'][h]['values'],role,mode),value(w['world'],role,mode)) for w in g]
                        shares.append(float(np.mean(ss)) if all(v is not None for v in ss) else None)
                    if None not in shares:ls.append(shares[0]);rs.append(shares[1]);deltas.append(shares[0]-shares[1])
                stem=role+'_'+mode
                props[stem+'_delta_pp']=float(np.mean(deltas)) if len(deltas)==len(weeks) else None
                props[stem+'_observed_common_delta_pp']=float(np.mean(deltas)) if deltas else None
                props[stem+'_left_share']=float(np.mean(ls)) if len(ls)==len(weeks) else None
                props[stem+'_right_share']=float(np.mean(rs)) if len(rs)==len(weeks) else None
        features.append({'type':'Feature','properties':props,'geometry':h3.polygon(h)})
        coverage.append({k:( '|'.join(v) if isinstance(v,list) else v) for k,v in props.items()})
    full={f['properties']['h3'] for f in features if f['properties']['full_window_comparable']}
    support=[]
    for side,works in [('left',left),('right',right)]:
        for role in ROLES:
            for mode in ['all','without-hosting']:
                world=sum(value(w['world'],role,mode) for rows in works for w in rows if w['index'] in weeks)
                covered=sum(value(c['values'],role,mode) for rows in works for w in rows if w['index'] in weeks for h,c in w.get('cells',{}).items() if h in full)
                support.append({'side':side,'role':role,'mode':mode,'world_weight':world,'full_mask_weight':covered,'full_mask_share':ratio(covered,world),'outside_full_mask_weight':world-covered})
    obj={'type':'FeatureCollection','metadata':{**metadata,'weeks':weeks,'resolution':5,'threshold':3,'sign':'left minus right; percentage points',
         'missing_policy':'Null if either side lacks a cell in any selected interval. Observed-common value is diagnostic only.',
         'full_comparable_cells':len(full),'union_cells':len(allcells),'weight_coverage':support},'features':features}
    # Compact GeoJSON is substantially smaller than pretty-printed cell polygons.
    (out/(name+'.geojson')).write_text(json.dumps(obj,separators=(',',':'),allow_nan=False)+'\n')
    write_csv(out/(name+'-coverage.csv'),coverage)
    return obj['metadata']


def js_divergence(left,right):
    countries=sorted(set(left)|set(right));p=np.array([left.get(c,0) for c in countries],dtype=float);q=np.array([right.get(c,0) for c in countries],dtype=float)
    if p.sum()==0 or q.sum()==0:return None
    p/=p.sum();q/=q.sum();mid=(p+q)/2
    return float(.5*sum(np.sum(x[x>0]*np.log2(x[x>0]/mid[x>0])) for x in [p,q]))


def evidence_views(out, metadata, perwork):
    branches=[]
    for k,m in metadata.items():
        bases=m['usa_production']['qualification_basis']
        branches.append({'key':k,'known_us_producer':'USA' in m['producer']['known_countries'],
                         'complete_non_us_producers':m['producer']['group']=='non-usa-only',
                         'baseline_us_country_or_producer':'reviewed-production-country-or-producer' in bases,
                         'us_commissioner_or_platform':any(b.startswith(('platform:','commissioner:')) for b in bases),
                         'frozen_usa_production':m['usa_production']['value'],
                         'producer_group':m['producer']['group']})
    fields=['known_us_producer','complete_non_us_producers','baseline_us_country_or_producer','us_commissioner_or_platform']
    summaries=[]
    for branch in fields:
        keys={r['key'] for r in branches if r[branch]}
        for role in ROLES:
            for region in REGIONS:
                for mode in ['all','without-hosting']:
                    rr=[r for r in perwork if r['key'] in keys and r['role']==role and r['region']==region and r['mode']==mode and r['coverage']=='full' and r['share'] not in [None,'']]
                    summaries.append({'evidence_branch':branch,'role':role,'region':region,'mode':mode,'objects':len(rr),
                                      'equal_object_mean_share':float(np.mean([float(r['share']) for r in rr])) if rr else None,
                                      'volume_weighted_share':ratio(sum(int(r['weight']) for r in rr),sum(int(r['world_weight']) for r in rr))})
    write_csv(out/'evidence-branches.csv',branches)
    write_csv(out/'evidence-branch-regions.csv',summaries)


def daily_group_views(out, metadata, data, days):
    """Daily regional/home shares and group means, with explicit fixed-roster coverage."""
    coverage=[];observations=[];buckets=defaultdict(list)
    for key,obj in metadata.items():
        rows={d['index']:d for d in data[key]['days'] if d['index']<=days}
        missing=sorted(set(range(1,days+1))-set(rows))
        full=not missing
        group=obj['producer']['group'];home=obj['producer']['known_countries'] if group!='unknown' else None
        bases=obj['usa_production']['qualification_basis']
        branches=[('producer-group',group)]
        if 'USA' in obj['producer']['known_countries']:branches.append(('evidence-branch','known_us_producer'))
        if group=='non-usa-only':branches.append(('evidence-branch','complete_non_us_producers'))
        if 'reviewed-production-country-or-producer' in bases:branches.append(('evidence-branch','baseline_us_country_or_producer'))
        if any(b.startswith(('platform:','commissioner:')) for b in bases):branches.append(('evidence-branch','us_commissioner_or_platform'))
        coverage.append({'key':key,'producer_group':group,'observed_days':len(rows),'expected_days':days,
                         'complete_window':full,'missing_days':'|'.join(map(str,missing)),
                         'home_country_codes':'|'.join(home) if home else '',
                         'audit_eligible_days':sum(d['sensitivity_eligible'] for d in rows.values())})
        for day,d in sorted(rows.items()):
            for role in ROLES:
                for mode in ['all','without-hosting']:
                    den=value(d['world'],role,mode)
                    for region in [*REGIONS,'producer-home']:
                        num=(sum(value(d['countries'].get(c,empty()),role,mode) for c in home) if home else None) if region=='producer-home' else value(d['regions'][region],role,mode)
                        share=ratio(num,den) if num is not None else None
                        row={'key':key,'day':day,'date':d['dates'],'role':role,'mode':mode,'region':region,
                             'weight':num,'world_weight':den,'share':share,'producer_group':group,
                             'complete_window':full,'sensitivity_eligible':d['sensitivity_eligible']}
                        observations.append(row)
                        if full and share is not None:
                            for kind,branch in branches:
                                for coverage_mode in ['full']+(['audit-filtered'] if d['sensitivity_eligible'] else []):
                                    buckets[(kind,branch,day,role,mode,region,coverage_mode)].append(row)
    summaries=[]
    for (kind,branch,day,role,mode,region,coverage_mode),rows in sorted(buckets.items()):
        summaries.append({'kind':kind,'group':branch,'day':day,'role':role,'mode':mode,'region':region,'coverage':coverage_mode,
                          'objects':len(rows),'canonical_works':len({metadata[r['key']]['canonical_work'] for r in rows}),
                          'equal_object_mean_share':float(np.mean([r['share'] for r in rows])),
                          'median_share':float(np.median([r['share'] for r in rows])),
                          'volume_weighted_share':ratio(sum(r['weight'] for r in rows),sum(r['world_weight'] for r in rows))})
    write_csv(out/'daily-group-observations.csv',observations)
    write_csv(out/'daily-group-summary.csv',summaries)
    write_csv(out/'daily-group-coverage.csv',coverage)
    return {'days':days,'complete_objects':sum(r['complete_window'] for r in coverage),
            'complete_producer_groups':dict(Counter(r['producer_group'] for r in coverage if r['complete_window'])),
            'observation_rows':len(observations),'summary_rows':len(summaries)}


def main():
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);a=p.parse_args();out=a.run
    manifest=json.loads((out/'selection-manifest.json').read_text());policy=manifest['policy'];n=policy['cohort_weeks']
    rng=np.random.default_rng(policy['matching']['bootstrap_seed']);reps=policy['matching']['bootstrap_replicates']
    metadata={r['key']:r for r in manifest['objects']};data={k:load_json(out/'objects'/(k+'.json')) for k in metadata}
    rows=[];exclusions=[];weekly=[];daily=[];source_inputs=list(manifest['inputs']);eligible={}
    for k,m in metadata.items():
        d=data[k];source_inputs+=d['inputs'];ww=[w for w in d['weeks'] if w['index']<=n]
        ok=complete(ww,n);eligible[k]=ok
        reasons=[]
        if m['producer']['group']=='unknown':reasons.append('producer-country-unresolved')
        if not ok:reasons.append('incomplete-eight-week-window')
        if not m['languages']:reasons.append('matching-language-missing')
        if not m['genre_family']:reasons.append('matching-genre-missing')
        exclusions.append({'key':k,'producer_group':m['producer']['group'],'eight_week_eligible':ok,'reasons':'|'.join(reasons),'available_weeks':len(ww),'partial_weeks':'|'.join(str(w['index']) for w in ww if w['partial']), 'unresolved_tags':'|'.join(m['producer']['unresolved_tags'])})
        for w in d['weeks']:
            for role in ROLES:
                for region in REGIONS:
                    for mode in ['all','without-hosting']:
                        num,den=amounts([w],role,region,mode)
                        weekly.append({'key':k,'group':m['producer']['group'],'week':w['index'],'dates':w['dates'],'region':region,'role':role,'mode':mode,'weight':num,'world_weight':den,'share':ratio(num,den),'sensitivity_eligible':w['sensitivity_eligible'],'partial':w['partial']})
        if ok:
            for role in ROLES:
                for region in REGIONS:
                    for mode in ['all','without-hosting']:
                        for coverage in ['full','audit-filtered']:
                            selected=ww if coverage=='full' else [w for w in ww if w['sensitivity_eligible']]
                            num,den=amounts(selected,role,region,mode)
                            rows.append({'key':k,'canonical_work':m['canonical_work'],'group':m['producer']['group'],'sample_year':m['sample_year'],'scope':m['scope'],'region':region,'role':role,'mode':mode,'coverage':coverage,'intervals':len(selected),'weight':num,'world_weight':den,'share':ratio(num,den),'asian_global':m['asian_global_eligible']})
        if k in policy['daily_keys']:
            home=policy['pair_home_countries'][k];byday={w['index']:w for w in d['days']}
            for i in range(1,policy['daily_days']+1):
                w=byday.get(i)
                for role in ROLES:
                    for mode in ['all','without-hosting']:
                        den=value(w['world'],role,mode) if w else 0
                        num=sum(value(w['countries'].get(c,empty()),role,mode) for c in home) if w else None
                        moving=[]
                        for j in range(i-6,i+1):
                            q=byday.get(j)
                            if q and q['sensitivity_eligible']:
                                v=ratio(sum(value(q['countries'].get(c,empty()),role,mode) for c in home),value(q['world'],role,mode))
                                if v is not None:moving.append(v)
                        daily.append({'key':k,'day':i,'date':w['dates'] if w else None,'home_countries':'|'.join(home),'role':role,'mode':mode,'home_weight':num,'world_weight':den if w else None,'share':ratio(num,den) if w else None,'sensitivity_eligible':bool(w and w['sensitivity_eligible']),'trailing_7_day_share_mean':float(np.mean(moving)) if len(moving)==7 else None})
    summaries=[]
    for group in ['usa-only','non-usa-only','mixed','unknown']:
        for population in ['expanded-aapi','asian-global']:
            for role in ROLES:
                for region in REGIONS:
                    for mode in ['all','without-hosting']:
                        for coverage in ['full','audit-filtered']:
                            selected=[r for r in rows if r['group']==group and r['region']==region and r['role']==role and r['mode']==mode and r['coverage']==coverage and r['share'] is not None and (population=='expanded-aapi' or r['asian_global'])]
                            s=summarize([r['share'] for r in selected],[r['canonical_work'] for r in selected],[r['world_weight'] for r in selected],rng,reps)
                            summaries.append({'group':group,'population':population,'role':role,'region':region,'mode':mode,'coverage':coverage,**s})
    strata=defaultdict(lambda:defaultdict(list));matching=[]
    for k,m in metadata.items():
        if eligible[k] and m['producer']['group'] in ['usa-only','non-usa-only'] and m['languages'] and m['genre_family']:
            stratum=(m['sample_year'],m['scope'],tuple(m['languages']),m['genre_family'])
            strata[stratum][m['producer']['group']].append(k)
    matched=[]
    for sk,groups in sorted(strata.items()):
        # Remove repeated sampled units of one canonical work within a stratum.
        for group,keys in groups.items():
            seen=set();chosen=[]
            for k in sorted(keys):
                c=metadata[k]['canonical_work']
                if c not in seen:chosen.append(k);seen.add(c)
            groups[group]=chosen
        status='matched' if groups.get('usa-only') and groups.get('non-usa-only') else 'unmatched-no-opposite-group'
        entry={'stratum':list(sk),'groups':dict(groups),'status':status};matching.append(entry)
        if status=='matched':matched.append(entry)
    comparisons=[]
    for match in matched:
        left=match['groups']['usa-only'];right=match['groups']['non-usa-only']
        common_filtered=[i for i in range(1,n+1) if all(next(w for w in data[k]['weeks'] if w['index']==i)['sensitivity_eligible'] for k in left+right)]
        for coverage,weeks in [('full',list(range(1,n+1))),('audit-filtered',common_filtered)]:
            for role in ROLES:
                for mode in ['all','without-hosting']:
                    countries=[]
                    for keys in [left,right]:
                        dist=defaultdict(float)
                        for k in keys:
                            ww=[w for w in data[k]['weeks'] if w['index'] in weeks]
                            den=sum(value(w['world'],role,mode) for w in ww)
                            if den:
                                for w in ww:
                                    for c,v in w['countries'].items():dist[c]+=value(v,role,mode)/den/len(keys)
                        countries.append(dist)
                    js=js_divergence(*countries)
                    for region in REGIONS:
                        sides=[]
                        for keys in [left,right]:
                            vals=[]
                            for k in keys:
                                ww=[w for w in data[k]['weeks'] if w['index'] in weeks];num,den=amounts(ww,role,region,mode);v=ratio(num,den)
                                if v is not None:vals.append(v)
                            sides.append(float(np.mean(vals)) if len(vals)==len(keys) else None)
                        comparisons.append({'stratum':match['stratum'],'left':left,'right':right,'region':region,'role':role,'mode':mode,'coverage':coverage,'weeks':weeks,'left_share':sides[0],'right_share':sides[1],'difference_pp':sides[0]-sides[1] if None not in sides else None,'country_js_divergence_bits':js,'ci95':None,'ci_reason':'Fewer than two independent works on at least one side' if min(len(left),len(right))<2 else 'See clustered summary uncertainty; stratum difference bootstrap not estimated'})
    # Geography distance of the selected pair over exactly 15 weeks, full country bins.
    pair=policy['daily_keys'];pair_dist=[]
    for role in ROLES:
        for mode in ['all','without-hosting']:
            dist=[]
            for k in pair:
                d=defaultdict(int)
                for w in data[k]['weeks']:
                    for c,v in w['countries'].items():d[c]+=value(v,role,mode)
                dist.append(d)
            pair_dist.append({'role':role,'mode':mode,'country_js_divergence_bits':js_divergence(*dist)})
    assert len({(metadata[k]['export_version'],metadata[k]['geolocation_version']) for k in pair})==1, 'Pair geolocation/export versions differ'
    h3=H3();maps=[]
    maps.append(difference_map(out,'beef-no-more-bets-h3',[data[pair[0]]['weeks']],[data[pair[1]]['weeks']],list(range(1,16)),{'left':pair[:1],'right':pair[1:],'export_versions':[metadata[k]['export_version'] for k in pair],'geolocation_versions':[metadata[k]['geolocation_version'] for k in pair]},h3))
    for i,match in enumerate(matched):
        left=match['groups']['usa-only'];right=match['groups']['non-usa-only']
        versions={(metadata[k]['export_version'],metadata[k]['geolocation_version']) for k in left+right}
        if len(versions)!=1:maps.append({'status':'not-comparable','reason':'geolocation-or-export-version-mismatch','stratum':match['stratum']});continue
        maps.append(difference_map(out,f'matched-stratum-{i+1}-h3',[[w for w in data[k]['weeks'] if w['index']<=n] for k in left],[[w for w in data[k]['weeks'] if w['index']<=n] for k in right],list(range(1,n+1)),{'left':left,'right':right,'stratum':match['stratum'],'export_geolocation_versions':list(versions)},h3))
    # Daily and weekly grains are compared diagnostically, never forced to sum.
    grain=[]
    for k in pair:
        for role in ROLES:
            for w in data[k]['weeks']:
                dd=[d for d in data[k]['days'] if w['start']<=d['start']<=w['end']]
                grain.append({'key':k,'role':role,'week':w['index'],'observed_days':len(dd),'daily_sum':sum(d['world'][role]['size'] for d in dd),'weekly_weight':w['world'][role]['size']})
    dump(out/'input-manifest.json',{'source_commits':manifest['source_commits'],'inputs':source_inputs})
    dump(out/'cohort-summary.json',summaries);dump(out/'matched-comparisons.json',comparisons);dump(out/'matching-manifest.json',matching)
    dump(out/'map-manifest.json',maps);dump(out/'pair-distances.json',pair_dist)
    write_csv(out/'per-work.csv',rows);write_csv(out/'weekly-regions.csv',weekly);write_csv(out/'daily-home-country.csv',daily);write_csv(out/'exclusions.csv',exclusions);write_csv(out/'daily-weekly-grain-check.csv',grain)
    flat=[{**x,'mean_ci95':json.dumps(x['mean_ci95'])} for x in summaries];write_csv(out/'cohort-summary.csv',flat)
    daily_groups=daily_group_views(out,metadata,data,policy['cohort_daily_days'])
    result={'daily_groups':daily_groups,'population':len(metadata),'producer_groups':dict(Counter(m['producer']['group'] for m in metadata.values())),
            'eight_week_eligible':sum(eligible.values()),'eligible_groups':dict(Counter(m['producer']['group'] for k,m in metadata.items() if eligible[k])),
            'matched_strata':len(matched),'matching':matched,'daily_rows':len(daily),'weekly_region_rows':len(weekly),
            'maps':[{'union_cells':m.get('union_cells'),'full_comparable_cells':m.get('full_comparable_cells')} for m in maps],
            'bootstrap_seed':policy['matching']['bootstrap_seed'],'bootstrap_replicates':reps}
    evidence_views(out,metadata,rows)
    dump(out/'analysis-receipt.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
