#!/usr/bin/env python3
"""Render the Gojira study in the existing Jekyll site, preserving its history."""
import argparse,csv,ctypes,gzip,html,json,math,shutil,subprocess
from pathlib import Path
from build_mellon_stage5_import import load_builder
from mellon_7_8_stage4 import dump,load_json,sha
from mellon_7_6_native_maps import NativeMaps
from izzi_weekly_graphs import IzziWeeklyGraphs,point,series
B=load_builder();A=B.A;L=B.LEGACY
LABELS={'JPN':'Japan','USA':'USA','CHN':'China','KOR':'South Korea','asia-28':'Asia-28','eur-27':'EUR-27','usa-can':'USA–Canada'}

def table(headers,rows):return L.table(headers,[[str(v).replace('|',', ') for v in row] for row in rows])
def fmt(v):return 'Unavailable' if v is None else f'{v:.2f}'
def read_csv(p):return list(csv.DictReader(p.open()))
def fig(name,caption):return L.figure(None,name,caption)

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--site',type=Path,required=True);a=p.parse_args();work=a.work;run=work/'run';site=a.site
 m=load_json(run/'selection-manifest.json');rows=m['objects'];objects={r['key']:r for r in rows};keys=list(objects);base='../data/mellon-7.8/runs/'+m['run_id']+'/'
 old=load_json(run/'historical/mellon-7.6-analysis.json');city_objects=load_json(run/'city-objects.json');maps=load_json(run/'map-manifest.json');windows=load_json(run/'pair-windows.json');summary=read_csv(run/'pair-summaries.csv');weekly=read_csv(run/'weekly-regions.csv');daily=read_csv(run/'daily-regions.csv');portraits=load_json(run/'cache-map-manifest.json')
 native=NativeMaps(site,Path('/home/bkoz/src/cartofreako'),Path('/home/bkoz/src/izzi'),work/'ne_10m_admin_0_countries.geojson',work/'ne_10m_lakes.geojson')
 graphs=IzziWeeklyGraphs(Path('/home/bkoz/src/izzi'))
 text=L.header('Godzilla and Monarch: Japan and Asia-28','Observed swarm geography: film and episode-group comparisons')
 text+='\n{::nomarkdown}\n<link rel="stylesheet" href="../resources/mellon-7.8-stage5.css"><script defer src="../resources/mellon-7.8-stage5.js"></script>\n{:/}\n'
 def share(key,region,mode='all',role='downloaders',window='full',pair='films'):
  r=next(r for r in summary if all(r[k]==v for k,v in {'key':key,'region':region,'mode':mode,'role':role,'window':window,'pair':pair}.items()));return float(r['share'])
 text+=f'''## How does observed geography differ?

**Minus One has the larger Japanese share in the 2024 film pair:** {share(keys[0],'JPN'):.2f}% of worldwide downloader weight, compared with {share(keys[1],'JPN'):.2f}% for The New Empire over elapsed weeks 1–26. Across Asia-28, the shares are {share(keys[0],'asia-28'):.2f}% and {share(keys[1],'asia-28'):.2f}%. These are descriptive swarm observations, not viewers, nationality or a production-country effect.

The colorful maps below are **dated cumulative audit portraits**. Both film portraits and weekly comparisons span 26 weeks; the Japanese share is larger for Minus One, while Asia-28’s overall share is larger for The New Empire. Different cache and interval grains cannot be substituted for each other. Monarch appears separately as an episode-group comparison.

## Japan: two cumulative audit portraits

Circle area represents downloader weight with one shared coefficient ({portraits['records'][0]['radius_base']:.6f}), **5% opacity and no display minimum**. Each geography uses the same frame and scale for both films. Yellow/orange marks identify 2160 resolution, pink/purple 1080, blue 720 and green SD. Shades identify members within each film; they do not match torrent identities between films. These are original sample caches, coalesced by unique BTIH and geolocated through the native audit renderer.

'''
 for code in ['JPN','asia-28']:
  if code=='asia-28':text+='\n## Asia-28: the same films, one regional frame\n\nMembership is the frozen set of 28 ISO-3 codes, including MAC and TWN once each. Neighboring country-coded observations are excluded.\n'
  text+='\n{::nomarkdown}\n<div class="gojira-portraits">\n'
  for r in portraits['records']:
   if r['country']!=code:continue
   v=next(v for v in r['variants'] if v['group']=='combined');stem=Path(v['file']).stem;label=objects[r['collection']]['label']
   text+=f'<figure><a href="figures/{stem}-4k.webp" target="_blank" rel="noopener"><img src="figures/{stem}.webp" alt="{html.escape(label)}: {LABELS[code]}, cumulative downloader weights, {r["dates"]}; opens 3840-pixel image"></a><figcaption><strong>{html.escape(label)}</strong> · {r["dates"]}. {v["downloaders"]:,} downloader weight. <a href="figures/{stem}-4k.webp" target="_blank" rel="noopener">3840-pixel image</a> · <a href="figures/{stem}.svg">SVG</a> · <a href="figures/{r["receipt_file"]}">Accounting and layout</a>.</figcaption></figure>\n'
  text+='</div>\n{:/}\n'
 text+=f'\n<details markdown="1"><summary>Cache accounting and member colors</summary>\n\n[Complete map manifest]({base}cache-map-manifest.json), [accounting]({base}cache-accounting.json), and inventories for [Minus One]({base}{keys[0]}-cache-inputs.json) and [The New Empire]({base}{keys[1]}-cache-inputs.json) record the actual resolution assignments, shades, source hashes, coordinates and per-member totals. The snapshots span May 2–October 30 and May 14–November 11, 2024: exactly 26 weeks each, matching the interval comparisons. Cache weights count cumulative unique-BTIH observations; interval weights sum repeated observations across weeks, so their totals differ. Repeated views do not add observations to totals.\n\n</details>\n'
 text+='\n## Hot and cold locations\n\n**Minus One compared with The New Empire. Red circle — Hot: a larger share for Minus One. Blue circle — Cold: a smaller share for Minus One.** These signs describe relative share, without a significance or demand claim. Every marker has the same radius. Zero differences have no sign marker.\n\n### Selected shared cities\n\nThe historical selection rule is reapplied to 26 weeks: shared identified cities, at least 100 combined downloader weight, and at most two cities of each sign per country. Shares pool weeks 1–26 using each film’s own worldwide denominator. Focus or hover a circle for its values.\n'
 selected={}
 for pairid,left,right in [('films',keys[0],keys[1]),('historical-film',keys[0],keys[2])]:
  name='mellon-7.8-stage5-city-'+pairid;rr=L.map_plot(site,native,city_objects[left],city_objects[right],name,1);selected[pairid]=rr
  if pairid!='films':text+='\n<details markdown="1"><summary>Historical context: Minus One compared with Vs. Kong (2021)</summary>\n'
  text+=fig(name,'Fixed-size red/blue circles; selected shared cities; pooled worldwide downloader shares, weeks 1–26. Sampling years differ in the historical comparison.')
  text+=table(['City','First share','Second share','Difference (pp)'],[[r['city'],f"{r['a_share']:.6f}%",f"{r['b_share']:.6f}%",L.signed_pp(r['delta'])] for r in rr])
  if pairid!='films':text+='\n</details>\n'
 text+='\n### H3 resolution 5: complete aligned weekly support\n\nThese maps use the **mean of aligned weekly cell-share differences**, unlike the pooled city comparison. A cell receives a sign only when both films have observations in every selected interval. Partial/common-period values remain diagnostic downloads. Missing or suppressed cells are unavailable, never zero. The country/regional curves below support broader comparisons when the common mask is sparse.\n'
 h3=A.H3();h3.lib.cellToLatLng.argtypes=[ctypes.c_uint64,ctypes.POINTER(A.LatLng)];h3.lib.cellToLatLng.restype=ctypes.c_uint32
 for mm in maps:
  doc=load_json(run/mm['file']);name='mellon-7.8-stage5-'+Path(mm['file']).stem;points=[]
  for f in doc['features']:
   pp=f['properties'];center=A.LatLng();assert h3.lib.cellToLatLng(int(pp['h3'],16),ctypes.byref(center))==0
   points.append({'h3':pp['h3'],'coordinates':[math.degrees(center.lng),math.degrees(center.lat)],'delta':pp['downloaders_all_delta_pp'] or 0,'tooltip':'Loading exact H3 values'})
  native.render(name,{'title':'Minus One compared with The New Empire','subtitle':LABELS[mm['region']]+' · '+mm['window']+' · mean weekly share differences','selection_note':'Full common support only; missing support is unavailable. H3 cell centers are display anchors.','scale':1,'countries':[{'code':mm['region'],'codes':mm['country_codes'],'name':LABELS[mm['region']],'points':points}]},boundaries=work/'boundaries.json')
  # A script-free SVG download must itself preserve nulls and exact labels.
  import xml.etree.ElementTree as ET
  path=site/'resources'/(name+'.svg');tree=ET.parse(path);features={f['properties']['h3']:f['properties'] for f in doc['features']}
  for c in tree.getroot().iter():
   if 'data-cell' not in c.attrib:continue
   pp=features[c.get('data-cell')];d=pp['downloaders_all_delta_pp'];tip=f"H3 {pp['h3']}: "+('Unavailable' if d is None else ('Hot' if d>0 else 'Cold' if d<0 else 'Equal')+f"; Minus One {pp['downloaders_all_left_share']:.8g}%; The New Empire {pp['downloaders_all_right_share']:.8g}%; difference {L.signed_pp(d)} pp")+f"; weeks {mm['weeks']}; common {pp['common_intervals']} of {pp['expected_intervals']}."
   c.set('aria-label',tip);c.set('data-tooltip',tip);next(iter(c)).text=tip
   if d is None or d==0:c.set('style','display:none');c.set('tabindex','-1')
  tree.write(path,encoding='unicode');shutil.copyfile(path,site/'_includes'/path.name)
  retained=[r for r in mm['weight_coverage'] if r['role']=='downloaders' and r['mode']=='all']
  text+=f"\n#### {LABELS[mm['region']]} · {mm['window']}\n\n{mm['full_comparable_cells']:,} comparable cells from {mm['union_cells']:,} observed union cells; weeks {', '.join(map(str,mm['weeks']))}. The mask retains {retained[0]['full_mask_regional_share']:.2f}% / {retained[1]['full_mask_regional_share']:.2f}% of the films’ regional downloader weights. Worldwide denominators still define the shares.\n"
  text+=f'''\n{{::nomarkdown}}
<div class="gojira-h3 analysis-figure" data-source="{base}{mm['file']}">
<div class="gojira-legend"><span>Hot: Minus One larger share</span><span>Cold: Minus One smaller share</span></div>
<div class="gojira-controls"><label>Role <select data-role><option value="downloaders">Downloaders</option><option value="uploaders">Uploaders</option></select></label><label>Network weights <select data-mode><option value="all">All observations</option><option value="without-hosting">Hosting excluded</option></select></label><label><input type="checkbox" data-coverage> Show unavailable cells as neutral outlines</label></div>
<p data-status role="status">Loading exact values. The download contains the complete comparison.</p>
{{% include {name}.svg %}}
<p data-detail aria-live="polite"></p><div class="map-tooltip" role="status" hidden></div>
<details><summary>Exact cell shares and coverage</summary><div class="gojira-table"><table><thead><tr><th>H3 ID</th><th>Sign</th><th>Minus One</th><th>The New Empire</th><th>Difference (pp)</th><th>Common intervals</th></tr></thead><tbody></tbody></table></div></details>
<p><a href="{base}{mm['file']}">Complete resolution-5 GeoJSON</a> · <a href="{base}{Path(mm['file']).stem}-coverage.csv">Coverage and partial-period diagnostics</a> · <a href="../resources/{name}.svg">Native SVG</a></p></div>
{{:/}}\n'''
 text+='\n## Regional share trajectories and coverage\n\nJapan, USA, China and South Korea precede Asia-28, EUR-27 and USA–Canada. Every numerator uses the same work, interval, role and hosting treatment as its worldwide denominator. These overlapping country/region views are not a partition. Counts remain observed weights, not viewers. On narrow screens, scroll each chart sideways to see all 26 weeks.\n'
 def chart(pair,role,treatment='all',daily_view=False):
  kk=pair['keys'];panels=[];source=daily if daily_view else weekly
  for region in (['JPN','asia-28'] if daily_view else LABELS):
   ss=[]
   for j,key in enumerate(kk):
    rr=[r for r in source if r['key']==key and r['region']==region and r['role']==role and r['mode']==treatment]
    for field in (['share','mean7'] if daily_view else ['share']):
     pts=[point(int(r['index']),float(r[field]),f"{objects[key]['label']} · {r['dates']} · {region} · {role} · {treatment} · {field}: {float(r[field]):.6f}%") for r in rr if r[field]]
     if pts:ss.append(series(objects[key]['label']+(' · seven-day mean' if field=='mean7' else ' · daily' if daily_view else ''),j+(2 if field=='mean7' else 0),pts))
   panels.append({'title':LABELS[region]+' · '+role+' · '+treatment,'unit':'percent','ylabel':'World share (%)','series':ss})
  name='mellon-7.8-stage5-'+pair['id']+'-'+role+'-'+treatment+('-daily' if daily_view else '-weekly');n=105 if daily_view else 26
  graphs.render(site,name,{'title':objects[kk[0]]['label']+' / '+objects[kk[1]]['label'],'subtitle':'Observed geographic shares · '+treatment,'description':'Matching worldwide denominators; missing intervals are unplotted.','allow_label_callouts':True,'footer':'Daily observed shares and strict seven-consecutive-eligible-day means' if daily_view else 'Weekly observed shares · equal elapsed indices, different calendar dates','xmin':1,'xmax':n,'ticks':[[i,str(i)] for i in ([1,14,28,42,56,70,84,98,105] if daily_view else [1,5,10,15,20,26])],'xlabel':'Elapsed sampling day' if daily_view else 'Elapsed sampling week','panels':panels})
  return fig(name,'Daily shares and trailing means; seven consecutive eligible days are required; gaps remain blank.' if daily_view else 'Weekly geographic shares with matching worldwide denominators. Hosting exclusion does not establish residential traffic.')
 for pair in windows[:2]:
  if pair['id']=='monarch':text+='\n## Monarch: three-episode groups in 2026\n\nMonarch 201–203 and 208–210 are both three-episode samples. They occupy different release positions; matching elapsed indices does not align calendar dates. Monarch 101–103 remains earlier-season context and Monarch 110 is a single episode.\n'
  text+=f"\n### {objects[pair['keys'][0]]['label']} / {objects[pair['keys'][1]]['label']}\n\nRequested window: weeks 1–26; paired available window: weeks **{', '.join(map(str,pair['full']))}**. {'All 26 weeks are available for both objects.' if pair['full_window_complete'] else 'The shorter sample ends before week 26; no missing weeks are treated as zero, and pair summaries use only the available common weeks.'} Jointly eligible sensitivity: weeks **{', '.join(map(str,pair['jointly_eligible']))}**. Windows were selected from boundary flags and audit gaps before comparing effects.\n"
  for role in ['downloaders','uploaders']:
   text+=chart(pair,role)
   text+='<details markdown="1"><summary>'+role.capitalize()+': hosting-excluded trajectories</summary>\n'+chart(pair,role,'without-hosting')+'\n</details>\n'
  text+='\n<details markdown="1"><summary>Both roles: full-window and jointly eligible counts and shares</summary>\n'
  rr=[r for r in summary if r['pair']==pair['id']]
  text+=table(['Object','Region','Role','Treatment','Window','Regional weight','Worldwide weight','Share','World weight retained'],[[objects[r['key']]['label'],LABELS[r['region']],r['role'],r['mode'],r['window'],f"{int(r['numerator']):,}",f"{int(r['world']):,}",fmt(float(r['share']))+'%',fmt(float(r['world_weight_retained_pct']))+'%'] for r in rr]);text+='\n</details>\n'
 text+='\n## What happened around April 28, 2021?\n\nVs. Kong’s USA downloader share rises from 12.44% on April 27 to 22.59% on April 28; hosting-excluded shares rise from 10.60% to 20.69%. The daily files report the same inventory size of 276 BTIH entries across April 26–30, which does not prove unchanged active-member composition.\n\n'
 timeline=load_json(run/'release-context.json')
 text+=table(['Date','Documented event'],[[r['date'],f"[{r['event']}]({r['source']})"] for r in timeline['events']])
 text+=f"\nApril 28 was not a documented U.S. streaming or disc premiere. The nearby sequel report and HBO Max window ending are plausible context, **not an established explanation**. The aggregate observations cannot attribute the increase to either event. [Source review]({base}release-context.json).\n"
 text+='\n## Historical context, methods and downloads\n\n<details markdown="1"><summary>Seven objects, actual scopes and full cache windows</summary>\n'
 text+=table(['Object','Scope','Full available sample','Latest source revision'],[[r['label'],r['scope'],r['sample_duration'],r['source_revision'][:12]] for r in rows]);text+='\n</details>\n'
 text+=f'''\n[Daily usefulness assessment]({base}daily-assessment.json) explains the weekly presentation choice. [Coverage ledger]({base}coverage.csv) distinguishes missing exports, boundary flags and hourly audit gaps. [Pair windows]({base}pair-windows.json) and [pair summaries]({base}pair-summaries.csv) include the historical-film, earlier-season and single-episode context comparisons. [Daily data]({base}daily-regions.csv) cover the first 105 elapsed days and include Vs. Kong and Monarch 101–103, with validated trailing means. Daily Vs. Kong confirms the sustained USA rise already visible weekly: day 28 (April 27) is 12.44%, day 29 (April 28) is 22.59%, and days 29–35 remain 22.59%–24.05%; weekly shares rise from 7.54% to 24.41%. This refines onset timing but does not alter the broad geographic comparison, so the presentation stays weekly. The latest 2024 exports do not supply daily film geography; none is interpolated from weekly data or graph pixels.

<details markdown="1"><summary>Production, distribution and platform evidence</summary>

[UNIJAPAN’s film record](https://jfdb.jp/en/title/9957) credits TOHO as Minus One’s production company and Japanese distributor. [The New Empire’s official site](https://www.godzillaxkongmovie.com/godzillaxkong2024/) identifies a Legendary Pictures production presented with Warner Bros.; Toho retains Godzilla rights and Japanese distribution, and Legendary East distributes in mainland China. [Legendary’s company record](https://www.legendary.com/about/terms/) identifies its California address. These credited relationships support a Japan/USA company-base contrast, while retaining Toho involvement and the joint presentation. They do not establish an exhaustive financing or coproduction census.

[Apple’s season-two announcement](https://www.apple.com/uk/tv-pr/news/2026/02/apple-tv-celebrates-the-season-two-world-premiere-of-monstrous-hit-drama-monarch-legacy-of-monsters/) identifies Legendary Television, Safehouse executive producers, and Toho executive-producer involvement. Apple TV is the platform; it is not substituted for the producer-country evidence. The seven objects are descriptive franchise cases, not independent national production cohorts. Language, distribution, release timing and scope still differ. The AAM roster has not been rebuilt.

</details>

<details markdown="1"><summary>Historical page, counts and provisional ITU adjustment</summary>

[The preserved historical page](godzilla-20261008-historical.html) and its [original calculation ledger]({base}historical/mellon-7.6-analysis.json) retain the original 15-week city selections, former all-seven sensitivity and provisional 2026 ITU counts. The old sensitivity kept weeks 6, 7, 8, 9 and 14. ITU scaling within a work leaves its geographic shares unchanged. The new study therefore leads with raw shares and separate hosting treatments.

</details>

<details markdown="1"><summary>Units, versions and coverage rules</summary>

Only top-level interval GeoJSON features contribute to weekly totals; nested per-member collections are not added again. Pooled shares divide summed geographic weights by summed worldwide weights, including unclassified countries. These sums repeat observations across weeks and torrents. Uploader denominators are separate. Hosting exclusion subtracts the hosting flag from both numerator and denominator; it does not identify residential traffic.

Every selected interval declares export version `20260701`, H3 resolution 5 and minimum swarm size 3. Companion cumulative JSON reports export version `2026-08-05` and geolocation version `6:1777968300`; the interval files do not embed the latter version directly. Exact repository revisions and file hashes are frozen in the manifests. Dates retain source calendar labels; the exporter does not certify a time zone.

Pair sensitivities exclude boundary flags and overlapping hourly audit gaps from both objects using the same elapsed-week indices. Full-window counts retain flagged observations. Shorter samples restrict paired summaries to common available weeks; their unpaired trajectory tail remains visible where observed. No absent interval or suppressed cell becomes zero. The strict 26-week H3 mask is selective; regional curves describe broader geographic shares.

</details>

[Weekly CSV]({base}weekly-regions.csv) · [Daily CSV]({base}daily-regions.csv) · [Pair summaries]({base}pair-summaries.csv) · [Selection and methods]({base}selection-manifest.json) · [Exact input hashes and versions]({base}input-manifest.json) · [Region definitions]({base}region-definitions.json) · [Figures]({base}figure-manifest.json) · [Validation]({base}validation-receipt.json) · [Artifacts and reproduction]({base}artifact-manifest.json).
'''
 # Preserve old entry anchors through links to the dated page.
 import re
 anchors=[]
 for heading in re.findall(r'^##+ (.+)$',(run/'historical/godzilla-20261008.md').read_text(),re.M):
  anchor=re.sub(r'[^\w\- ]','',heading.lower()).replace(' ','-');anchors.append(anchor)
 text+='\n{::nomarkdown}\n<details><summary>Historical section links</summary>'+''.join(f'<p id="{html.escape(x)}"><a href="godzilla-20261008-historical.html#{html.escape(x)}">Historical: {html.escape(x.replace("-"," "))}</a></p>' for x in dict.fromkeys(anchors) if x not in ['hot-and-cold-locations'])+'</details>\n{:/}\n'
 (site/'docs/godzilla.md').write_text(text);shutil.copyfile(run/'historical/godzilla-20261008.md',site/'docs/godzilla-20261008-historical.md')
 graphs.save_ledger(run/'figure-manifest.json');dump(run/'city-render-manifest.json',{'native':native.provenance,'selected':selected})
 for helper in ['mellon-7.8-stage5.js','mellon-7.8-stage5.css']:shutil.copyfile(B.ROOT/'scripts'/helper,site/'resources'/helper)
 target=site/'data/mellon-7.8/runs'/m['run_id'];shutil.copytree(run,target,dirs_exist_ok=True,ignore=shutil.ignore_patterns('objects'))
 (target/'objects').mkdir(exist_ok=True)
 for path in (run/'objects').glob('*.json'):(target/'objects'/(path.name+'.gz')).write_bytes(gzip.compress(path.read_bytes(),mtime=0))
 dump(site/'data/mellon-7.8/stage5-current.json',{'run_id':m['run_id'],'manifest':f'runs/{m["run_id"]}/selection-manifest.json'})
 print('Stage 5 page and figures rendered',flush=True)
if __name__=='__main__':main()
