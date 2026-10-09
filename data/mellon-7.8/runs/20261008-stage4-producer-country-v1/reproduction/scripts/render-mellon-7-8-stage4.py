#!/usr/bin/env python3
"""Publish the broader stage 4 report, Izzi figures and accessible H3 maps."""
import argparse
import csv
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import numpy as np
from mellon_7_8_stage4 import dump, sha, ROLES, REGIONS
from izzi_weekly_graphs import IzziWeeklyGraphs, point, series
ROOT=Path(__file__).resolve().parents[1]
LABELS={'asia-28':'Asia-28','eur-27':'EUR-27','usa-can':'USA–Canada','other':'Other classified geography','unclassified':'Unclassified'}
GROUPS={'usa-only':'USA-only listed producers','non-usa-only':'Non-USA listed producers','mixed':'Mixed listed producers','unknown':'Unresolved producer country'}

def table(headers,rows):return '\n| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(str(x).replace('|',' / ') for x in row)+' |\n' for row in rows)+'\n'

def fmt(x):return 'Unavailable' if x is None else f'{x:.2f}'

def fig(name,caption):return '\n{::nomarkdown}\n<figure class="analysis-figure">\n{% include '+name+'.svg %}\n<figcaption>'+caption+' <a href="../resources/'+name+'.svg">Download SVG</a>.</figcaption><div class="map-tooltip" role="status" aria-live="polite" hidden></div></figure>\n{:/}\n'

def chart(graphs,site,name,title,panels,n,xlabel='Elapsed sampling week'):
    footer = ('Producer-country groups · equal-object daily home shares · complete 56-day roster'
              if name.endswith('-daily-groups') else
              'Overlapping evidence groups · equal-object daily regional shares · complete 56-day roster'
              if name.endswith('-daily-evidence') else
              'Two works · daily home-country shares and seven-day means · matching daily worldwide denominator'
              if name.endswith('-daily') else
              'Three producer-country groups · equal-object weekly means · fixed eight-week roster'
              if name.endswith('-cohorts') else
              'Two works · weekly regional shares · matching weekly worldwide denominator')
    ticks=list(range(1,n+1)) if n<=15 else sorted({i for i in [1,7,14,28,42,56,70,84,98,105,n] if i<=n})
    graphs.render(site,name,{'title':title,'subtitle':title,'accessible_title':title,'description':'Observed interval shares, each using its matching worldwide denominator. Missing intervals are unplotted.','allow_label_callouts':True,'footer':footer,'xmin':1,'xmax':n,'ticks':[[i,str(i)] for i in ticks],'xlabel':xlabel,'panels':panels})

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--site',type=Path,required=True);p.add_argument('--izzi',type=Path,required=True);p.add_argument('--map-vendor',type=Path,required=True);p.add_argument('--world',type=Path,required=True);a=p.parse_args();run=a.run;site=a.site
    m=json.loads((run/'selection-manifest.json').read_text());receipt=json.loads((run/'analysis-receipt.json').read_text());summaries=json.loads((run/'cohort-summary.json').read_text());matches=json.loads((run/'matched-comparisons.json').read_text());maps=json.loads((run/'map-manifest.json').read_text())
    objects={r['key']:r for r in m['objects']};weekly=list(csv.DictReader((run/'weekly-regions.csv').open()));daily=list(csv.DictReader((run/'daily-home-country.csv').open()))
    keys=m['policy']['daily_keys'];labels={'beef-02':'Beef S02','no-more-bets':'No More Bets'}
    target=site/'data/mellon-7.8/runs'/m['run_id'];target.mkdir(parents=True,exist_ok=True)
    # Public object ledgers are losslessly compressed, preserving integers and nulls.
    for path in run.iterdir():
        if path.is_file():shutil.copyfile(path,target/path.name)
    (target/'objects').mkdir(exist_ok=True)
    for path in (run/'objects').glob('*.json'):
        (target/'objects'/(path.name+'.gz')).write_bytes(gzip.compress(path.read_bytes(),mtime=0))
    for path in (run/'objects').glob('*.json.gz'):
        destination=target/'objects'/path.name
        if not destination.exists() or not path.samefile(destination):shutil.copyfile(path,destination)
    dump(site/'data/mellon-7.8-stage4-current.json',{'run_id':m['run_id'],'analysis_receipt_sha256':sha(run/'analysis-receipt.json')})
    vendor=site/'resources/stage4-vendor';vendor.mkdir(exist_ok=True)
    for name in ['leaflet.js','leaflet.css','LICENSE']:shutil.copyfile(a.map_vendor/name,vendor/name)
    shutil.copyfile(a.world,vendor/'world.geojson')
    for name in ['mellon-7.8-stage4-map.html','mellon-7.8-stage4-map.js']:shutil.copyfile(ROOT/'scripts'/name,site/'resources'/name)
    graphs=IzziWeeklyGraphs(a.izzi,collection_keys={v:k for k,v in labels.items()})
    # Pair regional trajectories: the requested three boundaries, both roles.
    panels=[]
    for role in ROLES:
        for region in REGIONS[:3]:
            ss=[]
            for j,k in enumerate(keys):
                rr=[r for r in weekly if r['key']==k and r['region']==region and r['role']==role and r['mode']=='all' and r['share']]
                ss.append(series(labels[k],j,[point(int(r['week']),float(r['share']),f"{labels[k]} · {r['dates']} · {LABELS[region]} · {r['share']}%") for r in rr]))
            panels.append({'title':LABELS[region]+' · '+role,'unit':'percent','ylabel':'World share (%)','y_max':100,'series':ss})
    chart(graphs,site,'mellon-7.8-stage4-regional','Beef / No More Bets · three regions',panels,15)
    panels=[]
    for role in ROLES:
        for measure,title in [('share','Daily observed share'),('trailing_7_day_share_mean','Trailing seven eligible days')]:
            ss=[]
            for j,k in enumerate(keys):
                rr=[r for r in daily if r['key']==k and r['role']==role and r['mode']=='all' and r[measure]]
                name=labels[k]+' · '+('USA' if k=='beef-02' else 'China')
                ss.append(series(name,j,[point(int(r['day']),float(r[measure]),f"{name} · {r['date']} · {r[measure]}%") for r in rr]))
            panels.append({'title':title+' · '+role,'unit':'percent','ylabel':'Home-country share (%)','y_max':100,'series':ss})
    chart(graphs,site,'mellon-7.8-stage4-daily','Daily share in the documented producer country',panels,105,'Elapsed sampling day')
    # Fixed-roster cohort means by week; uncertainty and spreads are in the table.
    eligible={r['key'] for r in csv.DictReader((run/'exclusions.csv').open()) if r['eight_week_eligible']=='True'}
    panels=[]
    for role in ROLES:
        for region in REGIONS[:3]:
            ss=[]
            for j,g in enumerate(['usa-only','non-usa-only','mixed']):
                pts=[]
                for week in range(1,9):
                    rr=[r for r in weekly if r['key'] in eligible and r['group']==g and r['week']==str(week) and r['region']==region and r['role']==role and r['mode']=='all' and r['share']]
                    if rr:pts.append(point(week,float(np.mean([float(r['share']) for r in rr])),f"{GROUPS[g]} · week {week} · {len(rr)} objects · equal-object mean"))
                ss.append(series(GROUPS[g],j,pts))
            panels.append({'title':LABELS[region]+' · '+role,'unit':'percent','ylabel':'Mean world share (%)','y_max':100,'series':ss})
    chart(graphs,site,'mellon-7.8-stage4-cohorts','Producer-country groups · descriptive weekly means',panels,8)
    daily_groups=list(csv.DictReader((run/'daily-group-summary.csv').open()))
    for suffix,kind,regions,groups in [
        ('daily-groups','producer-group',['producer-home'],{g:GROUPS[g] for g in ['usa-only','non-usa-only','mixed']}),
        ('daily-evidence','evidence-branch',REGIONS[:3],{'known_us_producer':'Known U.S. producer','complete_non_us_producers':'Reviewed non-U.S. producers','baseline_us_country_or_producer':'Baseline U.S. country/producer','us_commissioner_or_platform':'U.S. commissioner/platform'})]:
        panels=[]
        for role in ROLES:
            for region in regions:
                ss=[]
                for j,(g,label) in enumerate(groups.items()):
                    rr=[r for r in daily_groups if r['kind']==kind and r['group']==g and r['role']==role and r['region']==region and r['mode']=='all' and r['coverage']=='full']
                    if rr:ss.append(series(label,j,[point(int(r['day']),float(r['equal_object_mean_share']),f"{label} · day {r['day']} · {r['objects']} objects · {r['equal_object_mean_share']}%") for r in rr]))
                panels.append({'title':('Producer-home countries' if region=='producer-home' else LABELS[region])+' · '+role,'unit':'percent','ylabel':'Mean world share (%)','y_max':100,'series':ss})
        chart(graphs,site,'mellon-7.8-stage4-'+suffix,'Daily producer-country and platform evidence comparisons',panels,56,'Elapsed sampling day')
    graphs.save_ledger(target/'figure-manifest.json')
    for directory in ['_includes','resources']:
        for svg in (site/directory).glob('mellon-7.8-stage4-*.svg'):svg.write_text(svg.read_text().rstrip()+'\n')
    base='../data/mellon-7.8/runs/'+m['run_id']+'/'
    def link(name,label):return f'[{label}]({base}{name})'
    text='''## Broader producer-country study

This study compares distribution geography by the countries of credited producers.
Platform and commissioner country remain separate AAM qualification evidence.
**Country coverage is limited:** the frozen population has 200 works, but the
reviewed company map resolves every listed producer tag for only 21. The other
179 remain unresolved; a U.S. platform does not resolve their producer country.
These are coverage-limited descriptions, not a census or a causal production effect.

### Population and coverage

'''
    text+=table(['Producer-country group','Selected objects','Complete eight-week exports'],[[GROUPS[g],receipt['producer_groups'].get(g,0),receipt['eligible_groups'].get(g,0)] for g in GROUPS])
    text+='''The population uses confirmed expanded AAPI membership and Threshold 2, with no
citizenship or USA Production filter. The producer grouping requires an exact
sourced country match for every production tag. “Complete” describes the listed
metadata credits; it does not certify all investors, service providers or financing.
Company headquarters identify the credited company's base, not filming locations
or its ultimate parent's nationality. Mixed producers remain a separate group.

The producer-country mapping and matching rules were frozen before the geographic
reduction. All 200 objects remain in the selection and exclusion ledgers. Of these,
149 have the first eight full weekly bins. The 51 shorter or missing windows are
reported rather than padded. Unknown producer groups are available in the downloads.
Beef and No More Bets retain their separate 15-week case comparison; neither has
complete producer-list mapping for the stricter cohort grouping.

'''
    text+=link('selection-manifest.json','Selection, title evidence and company-country coverage')+' · '+link('exclusions.csv','Coverage and exclusion ledger')+' · '+link('producer-country-policy.json','Frozen producer-country and matching rules')+'\n'
    text+='''
### Regional trajectories

The boundaries are **Asia-28**, **EUR-27** and **USA–Canada**, using the existing
regional-ranking definitions. They do not overlap. Other classified and
unclassified geography remain in the worldwide denominator and downloads.
Each curve shows the region's share of that interval's worldwide role total.

'''+fig('mellon-7.8-stage4-regional','Weeks 1–15. Separate calendar years and film/season scopes remain limitations. Counts and hosting-excluded shares are downloadable.')
    paired_rows=[]
    for role in ROLES:
        for region in REGIONS[:3]:
            values=[]
            for mode in ['all','without-hosting']:
                for k in keys:
                    rr=[r for r in weekly if r['key']==k and r['region']==region and r['role']==role and r['mode']==mode]
                    den=sum(int(r['world_weight']) for r in rr)
                    values.append(fmt(100*sum(int(r['weight']) for r in rr)/den) if den else 'Unavailable')
            paired_rows.append([LABELS[region],role,*values])
    text+=table(['Region','Role','Beef share (%)','No More Bets share (%)','Beef excluding hosting (%)','No More Bets excluding hosting (%)'],paired_rows)
    text+=link('weekly-regions.csv','All weekly regional weights and shares')+' · '+link('region-definitions.json','Exact region code lists and source digest')+'\n'
    text+='''
### Cohort distributions and matched comparisons

The following are unadjusted eight-week descriptions. Each sampled object receives
equal weight in the mean and median. The volume-weighted column uses observed
worldwide weights. Bootstrap intervals resample canonical works, keeping repeated
seasons or episode groups together; 1,000 replicates use a fixed saved seed.
Intervals describe variation in this selected, small sample, not uncertainty about
all media or unobserved peer locations.

'''
    rr=[s for s in summaries if s['population']=='expanded-aapi' and s['role']=='downloaders' and s['region'] in REGIONS[:3] and s['mode']=='all' and s['coverage']=='full' and s['group']!='unknown']
    text+=table(['Group','Region','Objects / canonical works','Mean (%)','Median (%)','Middle 50% (%)','Mean bootstrap 95% interval','Volume-weighted (%)'],[[GROUPS[s['group']],LABELS[s['region']],f"{s['n']} / {s['clusters']}",fmt(s['mean']),fmt(s['median']),fmt(s['q25'])+'–'+fmt(s['q75']),'Unavailable' if s['mean_ci95'] is None else '–'.join(fmt(v) for v in s['mean_ci95']),fmt(s['volume_weighted'])] for s in rr])
    text+='''The Asian-global-only sensitivity, hosting-excluded results, uploader results
and audit-filtered summaries are included in the cohort download. Audit filtering
removes flagged opening bins and intervals overlapping recorded gaps; it does not
assert completeness for older audits that lack hourly gap detail. Remaining
sample years, genres, languages and episode/season scopes differ across groups.

Exact matching on sample year, object scope, language and genre family yields
**one stratum: Eternals / Fistful of Vengeance**, English-language action films
sampled in 2022. Their listed producers map to USA and Thailand. Both qualify
under the separate USA Production rule. Japan Sinks supplies the other non-USA
producer case (Japan), but has no eligible opposite-group match under these rules.
The matched stratum has one independent work on each side, so a population-level
confidence interval is unavailable. Missing genre/language evidence is not guessed.

'''
    rr=[s for s in matches if s['region'] in REGIONS[:3] and s['role']=='downloaders' and s['mode']=='all' and s['coverage']=='full']
    text+=table(['Matched region','Eternals share (%)','Fistful share (%)','Difference (percentage points)'],[[LABELS[s['region']],fmt(s['left_share']),fmt(s['right_share']),fmt(s['difference_pp'])] for s in rr])
    if rr:text+=f"\nThe matched films' complete country distributions have Jensen–Shannon divergence **{rr[0]['country_js_divergence_bits']:.4f} bits** (0 means identical exported shares; 1 means disjoint support). This describes thresholded export distributions, not latent audiences.\n"
    text+=link('cohort-summary.csv','Cohort summaries and sensitivities')+' · '+link('per-work.csv','Per-work values')+' · '+link('matching-manifest.json','Matched and unmatched strata')+' · '+link('matched-comparisons.json','Matched effects, coverage sensitivity and country distances')+'\n'
    text+='\n<details markdown="1"><summary>Weekly cohort trajectories</summary>\n\n'+fig('mellon-7.8-stage4-cohorts','Fixed eight-week roster; equal-object weekly means. These unadjusted groups differ in year, genre and scope.')+'\n</details>\n'
    text+='''
### Producer and platform evidence

The evidence flags overlap: a work can have a U.S. producer and a U.S. platform.
The saved baseline country-or-producer flag is kept distinct from confirmed
company-country mappings. Fistful of Vengeance and Japan Sinks illustrate why
non-U.S. producer countries can coexist with USA Production qualification.
Beef and No More Bets keep their sourced producer examples and separate platform
review; no platform's country fills an unresolved production-company credit.

'''
    text+=link('evidence-branches.csv','Per-object evidence flags')+' · '+link('evidence-branch-regions.csv','Regional comparisons by evidence branch')+'\n'
    text+='''
### Daily share in the producer's home country

For Beef, the documented producer-country example is USA (A24); for No More Bets,
China (China Film Corporation). Daily shares divide exported home-country weights
by each day's exported worldwide weights. They use calendar dates in the source
files; the exports do not certify UTC, so no local-time or release-day alignment
is inferred. Home countries differ in scale and network coverage: these curves do
not estimate a home-country advantage.

Both objects have 105 daily exports in the chosen window. Raw observations and
seven-day trailing means are separate. The mean requires seven consecutive eligible
days; flagged boundary days and audit-gap dates leave gaps. No missing day is zero.
Daily sums differ from weekly totals in every tested role/week combination because
these products aggregate at different time grains. Daily curves therefore use daily
exports directly; weekly curves retain weekly exports.

'''+fig('mellon-7.8-stage4-daily','Days 1–105. First six rolling-window positions are unavailable; gap-affected and uncertified boundary-day windows are also unplotted.')
    text+=link('daily-home-country.csv','Daily observations, coverage and seven-day means')+' · '+link('daily-weekly-grain-check.csv','Daily versus weekly grain diagnostic')+'\n'
    dg=receipt['daily_groups']
    text+=f'''
### Daily producer and platform groups

The broader daily view uses the first 56 source calendar days. **{dg['complete_objects']}
objects have all 56 daily exports**; the remaining windows are listed in the
coverage ledger. Producer-home geography is the union of the countries of all
mapped listed producers. Mixed-country homes can cover several countries;
unresolved producer countries have no home-country value.

These are equal-object means on a fixed complete-export roster. The downloads
also contain daily medians, volume-weighted means, both roles, hosting exclusion,
and audit-filtered values. Audit filtering can change the daily denominator;
each row reports its object and canonical-work counts. Complete exports do not
certify complete hours within a day. Curves describe this selected sample.

'''
    text+=table(['Mapped producer group','Complete 56-day objects'],[[GROUPS[g],dg['complete_producer_groups'].get(g,0)] for g in GROUPS])
    text+='''The non-USA daily group contains only Japan Sinks; the mixed daily group
contains only No Time to Die. These single-work curves do not estimate population
effects. Eternals is missing days 25, 26 and 27, and Fistful of Vengeance is missing
day 43, so neither enters the complete-window daily groups. Their weekly matched
comparison remains available; daily completeness is checked separately.

'''
    text+='<details markdown="1"><summary>Daily shares in producer-home countries</summary>\n'+fig('mellon-7.8-stage4-daily-groups','First 56 days; fixed-roster means. Different home-country sizes and observation coverage limit comparisons.')+'\n</details>\n'
    text+='<details markdown="1"><summary>Daily regional shares by producer/platform evidence</summary>\n'+fig('mellon-7.8-stage4-daily-evidence','Evidence branches overlap. All use the same named region and matching daily worldwide denominator.')+'\n</details>\n'
    text+=link('daily-group-observations.csv','Daily per-object observations')+' · '+link('daily-group-summary.csv','Daily group summaries and sensitivities')+' · '+link('daily-group-coverage.csv','Daily window and country coverage')+'\n'
    text+='''
### H3 resolution-5 differences and coverage

The maps compare **cell shares**, with positive values indicating a larger share
for the first work. They join exact H3 IDs at resolution 5 and the same elapsed
weekly index. The default difference is available only if both sides observe that
cell in every selected interval. A missing or suppressed cell is unavailable, not
zero. The coverage view shows those excluded cells explicitly.

Beef / No More Bets has only 62 cells observed on both sides in all 15 weeks;
Eternals / Fistful has 2,722 over eight weeks. Sparse common coverage limits what
the first map can show. World denominators still include weights outside the
common mask; the following table reports that coverage. Export and geolocation
versions agree within each mapped comparison. Country aggregation retains source
country codes; polygon centroids do not assign countries.

'''
    text+=table(['Comparison','Side','Downloader weight retained in full mask (%)'],[[('Beef / No More Bets' if i==0 else 'Eternals / Fistful'),s['side'],fmt(s['full_mask_share'])] for i,mp in enumerate(maps) for s in mp['weight_coverage'] if s['role']=='downloaders' and s['mode']=='all'])
    text+='''
{::nomarkdown}
<iframe src="../resources/mellon-7.8-stage4-map.html" title="Producer-country H3 differences and coverage" style="width:100%;height:920px;border:1px solid #aaa" loading="lazy"></iframe>
{:/}

[Open the interactive map](../resources/mellon-7.8-stage4-map.html). The map supports
role, hosting, coverage and regional views, with a keyboard-accessible cell table.
'''
    for name,label in [('beef-no-more-bets-h3','Beef / No More Bets'),('matched-stratum-1-h3','Eternals / Fistful')]:
        text+='\n'+link(name+'.geojson',label+' GeoJSON')+' · '+link(name+'-coverage.csv',label+' coverage and exact differences')+'\n'
    text+='''
Resolution 8 is not needed for this comparison. The inputs are resolution 5 and
cannot supply finer within-cell locations. IP-geolocation accuracy and observation
density do not support a new resolution-8 claim here; no finer export was generated.

### Data, method and reproducibility

The measures are summed top-level aggregate GeoJSON swarm weights. Nested torrent
features are not added again. Addresses can recur across torrents and intervals;
these are not unique viewers or completed downloads. Hosting exclusion removes the
hosting flag from both numerator and denominator; it does not identify residential
users. Suppression and missing sampling hours remain coverage limits.

The run preserves the 197-work AAM roster and historical comparisons. All producer
classifications are analytical annotations with exact title/company sources. Source
commits and hashes, missing files, daily coverage, sampling windows, region lists,
matching, bootstrap settings and rendering specifications are downloadable.

'''
    for name,label in [('reproduction/README.md','Reproduction instructions and code'),('input-manifest.json','Input hashes and source revisions'),('analysis-receipt.json','Analysis receipt'),('figure-manifest.json','Izzi figure specifications'),('validation.json','Independent validation receipt'),('artifact-manifest.json','Output hashes and table manifest')]:text+='- '+link(name,label)+'\n'
    text+='\nThe scripts `mellon_7_8_stage4.py` (freeze and calculate), `analyze-mellon-7-8-stage4.py`, `render-mellon-7-8-stage4.py` and `check-mellon-7-8-stage4.py` reproduce this run from the pinned checkouts. Public per-object ledgers are compressed JSON in the run’s `objects/` directory.\n'
    (site/'_includes/mellon-7.8-stage4-study.md').write_text(text)
    page=site/'docs/asia-asian-where.md';s=page.read_text();include='{% include mellon-7.8-stage4-study.md %}'
    if include not in s:s=s.replace('## Definition and scope',include+'\n\n## Selected-pair definition and scope',1)
    page.write_text(s)
    # Preserve the integration when the existing paired comparison is regenerated.
    print(json.dumps({'run':m['run_id'],'figures':len(graphs.specifications),'public_objects':len(objects),'page':'docs/asia-asian-where.html'}))

if __name__=='__main__':main()
