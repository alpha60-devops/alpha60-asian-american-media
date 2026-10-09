#!/usr/bin/env python3
"""Render the approved 7.6 Jekyll pages and reproducible SVG figures.

Uses native Izzi for weekly line graphs and Izzi / Cartofreako for city maps.
Uses original cumulative sample-cache country maps; retains weekly comparison data.

Graph style for EVERY subpage: match the animation Disney+ graphs by default.
https://alpha60-devops.github.io/alpha60-results-animation/docs/disney_plus.html
Use native Izzi C++ annotations and direct media-object name labels
on the lines (Atkinson Hyperlegible 12pt), with WEEKS / DOWNLOADERS axes
for weekly downloader counts and the reference red-line hover interaction.
"""
import argparse
import html
import json
from pathlib import Path
import re
import shutil

from izzi_weekly_graphs import IzziWeeklyGraphs, point, series

COUNTRIES = {'IND': 'India', 'PHL': 'Philippines', 'AUS': 'Australia',
             'JPN': 'Japan', 'USA': 'USA', 'CHN': 'China', 'KOR': 'South Korea'}
COLORS = ['#175b8c', '#9b4318', '#606a24', '#4d405d', '#8c416d', '#525252', '#007f78']
MARKERS = ['o', 's', '^', 'D', 'v', 'P', 'X']
STYLES = ['-', '--', ':', '-.', '--', ':', '-']
ROOT = Path(__file__).resolve().parents[1]
WEEKLY_GRAPHS = None


def pct(n, d):
    return 100 * n / d if d else None


def fmt(n):
    return f'{n:,.0f}'


def table(headers, rows):
    return '\n' + '| ' + ' | '.join(headers) + ' |\n| ' + ' | '.join(['---'] * len(headers)) + ' |\n' + ''.join('| ' + ' | '.join(map(str, row)) + ' |\n' for row in rows) + '\n'


def header(title, description):
    return f'''---
layout: default
title: "{title}"
author: "Benjamin De Kosnik <bkoz@gnu.org>"
description: "{description}"
---

{{::nomarkdown}}
<img src="../resources/a60-logo-block-gray.simple.svg?sanitize=true" height="50" width="100" alt="Alpha60">
<div style="height: 50px;"></div>
<link rel="stylesheet" href="../resources/izzi-table-wcag-22.css">
<link rel="stylesheet" href="../resources/mellon-7.6-analysis.css">
<script defer src="../resources/mellon-7.6-analysis.js"></script>
<script defer src="../resources/izzi-weekly-graph-hover.js"></script>
{{:/}}

[Asian American Media results](../index.html)

# {title}

'''


def figure(site, name, caption):
    if WEEKLY_GRAPHS is not None and name in WEEKLY_GRAPHS.specifications and not caption.startswith('Standard Izzi'):
        caption = 'Standard Izzi C++ weekly graphs with media-object names directly on their lines. ' + caption
    return f'''\n{{::nomarkdown}}
<figure class="analysis-figure">
{{% include {name}.svg %}}
<figcaption>{html.escape(caption)} <a href="../resources/{name}.svg">Download SVG</a>.</figcaption>
<div class="map-tooltip" role="status" aria-live="polite" hidden></div>
</figure>
{{:/}}\n\n'''


def locations(a, b):
    # Shared, identified cities only. Absence in a thresholded export is not zero.
    aa = {r['id']: r for r in a['cities'] if r['id'].split(':')[1].isdigit() and int(r['id'].split(':')[1]) > 0}
    bb = {r['id']: r for r in b['cities'] if r['id'].split(':')[1].isdigit() and int(r['id'].split(':')[1]) > 0}
    rows = []
    for key in aa.keys() & bb.keys():
        x, y = aa[key], bb[key]
        if x['downloaders']['size'] + y['downloaders']['size'] < 100:
            continue
        sa = pct(x['downloaders']['size'], a['world']['downloaders']['size'])
        sb = pct(y['downloaders']['size'], b['world']['downloaders']['size'])
        rows.append({'id': key, 'city': x['city'], 'country': x['country'],
                     'coordinates': x['coordinates'], 'a': x['downloaders']['size'],
                     'b': y['downloaders']['size'], 'a_share': sa, 'b_share': sb, 'delta': sa - sb})
    selected = []
    for country in a['countries']:
        local = [r for r in rows if r['country'] == country]
        selected.extend(sorted([r for r in local if r['delta'] > 0], key=lambda r: (-r['delta'], r['id']))[:2])
        selected.extend(sorted([r for r in local if r['delta'] < 0], key=lambda r: (r['delta'], r['id']))[:2])
    return selected


def signed_pp(value):
    return f'{value:+.3f}' if abs(value) >= 0.0005 or value == 0 else f'{value:+.6g}'


def map_plot(site, native, a, b, name, scale):
    points = locations(a, b)
    window = f"1–{len(a['weeks'])}"
    for row in points:
        row['tooltip'] = f"{row['city']}, {COUNTRIES[row['country']]}: {a['label']} {fmt(row['a'])} ({row['a_share']:.3f}% of world); {b['label']} {fmt(row['b'])} ({row['b_share']:.3f}%); difference {signed_pp(row['delta'])} percentage points. Weeks {window}; selected shared city, pooled full-window coverage including flagged intervals."
    native.render(name, {
        'title': a['label'] + ' − ' + b['label'],
        'subtitle': 'City share of worldwide downloader weight · weeks ' + window,
        'scale': scale,
        'countries': [{'code': c, 'name': COUNTRIES[c], 'points': [p for p in points if p['country'] == c]} for c in a['countries']],
    })
    return points


def trend(site, records, name, adjusted=False, extended=False, role="downloaders"):
    countries = records[0]['countries']
    field = 'extended_weeks' if extended else 'weeks'
    def value(r, w, c):
        return w['country'][c][role]['size'] * r['itu_2026']['factor'] if adjusted else pct(w['country'][c][role]['size'], w['world'][role]['size'])
    maximum = max(value(r, w, c) for r in records for w in r[field] for c in countries)
    end = 26 if extended else len(records[0]['weeks'])
    spec = {'title': 'Weekly country ' + role,
            'subtitle': ('Provisional 2026 Internet-user scale · 6.1 billion reference' if adjusted else 'Country share of worldwide interval weight') + f' · weeks 1–{end}',
            'accessible_title': 'Weekly adjusted country ' + role + ' weights' if adjusted else 'Weekly country shares',
            'description': 'Izzi native weekly lines. Common vertical scale; missing intervals unplotted.',
            'columns': 1, 'xmin': 1, 'xmax': end, 'xlabel': 'WEEKS',
            'ticks': [[n, str(n)] for n in ([1,5,10,15,20,26] if extended else range(1,end+1))],
            'panels': [{'title': COUNTRIES[c], 'unit': 'weight' if adjusted else 'percent',
                        'ylabel': role.upper() if adjusted else 'World share (%)', 'y_max': maximum*1.12,
                        'series': [series(r['label'],i,[point(w['week'],value(r,w,c),
                            f"{r['label']} · {COUNTRIES[c]} {role} · week {w['week']} · {w['dates']} · {value(r,w,c):,.3f}" + (' adjusted weight' if adjusted else '% of world')) for w in r[field]])
                                   for i,r in enumerate(records)]} for c in countries]}
    WEEKLY_GRAPHS.render(site,name,spec)


def methods(regional=False, window="1–15"):
    text = '''
## Methods and limits

- **Units:** sum `downloaders.size` or `uploaders.size` in the top-level
  `features` array of each weekly aggregate GeoJSON. Summing the selected intervals
  produces repeated swarm weights across weeks and torrents, not unique people,
  unique addresses over the full window, or completed views. The nested
  `collection_week_by_btiha` is not added again.
- **Window:** weeks WINDOW inclusive, including the opening bin. Every selected
  interval spans seven calendar days within the actual sample cutoff. Some bins
  carry a `-partial` member-coverage flag or overlap an audit gap; the sensitivity
  excludes those elapsed-week indices from every object. Calendar dates differ.
  Matching elapsed weeks does not match release conditions or hourly coverage.
- **Shares:** country or city downloader weight divided by worldwide downloader
  weight over the same intervals, including unclassified-country features.
  Pooled shares use sums of counts, not the unweighted mean of weekly percentages.
  Uploader shares have a separate uploader denominator.
- **Flags:** mobile, hosting and VPN rates divide the country's flagged weight by
  that country's size for the same role. Flags overlap. A mobile flag describes
  IP network classification, not a device, connection technology, citizenship,
  residence or verified audience. Wi-Fi versus cellular usage is not resolved.
- **Hosting sensitivity:** subtract hosting from size in both country and global
  denominators. This removes one flag; it does not identify residential traffic.
- **Difference maps:** geolocated city aggregates keyed by country and GeoNames ID, using
  source representative coordinates. Only shared identified cities with at least
  100 combined downloader weight qualify. Show at most two positive and two
  negative differences per country, ranked by percentage-point difference.
  An absent or suppressed location is not zero. Triangles indicate sign;
  color intensity encodes magnitude on a symmetric scale shared by all difference maps on this page.
  “Hot” and “cold” describe larger and smaller observed shares, without a test of
  statistical significance. They do not describe population-adjusted demand.
- **Export:** all selected files declare H3 resolution 5 and minimum swarm size 3.
  Geographic filtering and aggregation mean these denominators differ from
  companion JSON unique-BTIH totals. Do not interpret the discrepancy as a known
  missing-data percentage. Weekly JSON `collection_week` values are cumulative
  prefixes; the geographic interval series used here is a different product.

'''
    if regional:
        start = text.index('- **Window:**')
        end = text.index('- **Shares:**', start)
        text = text[:start] + '''- **Window:** the matched tables use weeks 1–10,
  including the opening week. The worldwide and extended trends use available seven-day bins
  through week 26 and leave unavailable or shorter trailing bins unplotted.
  Pitt-201 country maps use the full January 9–July 9 cumulative sample cache,
  coalesced by unique BTIH, with every sampled resolution combined.
  A calendar-aligned comparison uses exactly matching seven-day intervals.
  Partial flags and audit gaps remain visible; no missing weights are imputed.
''' + text[end:]
        start, end = text.index('- **Difference maps:**'), text.index('- **Export:**')
        text = text[:start] + text[end:]
        text = text.replace('- **Export:** all selected files', '- **Weekly export:** all selected weekly files')
        text += '- **Country maps:** raw cumulative sample-cache weights after unique-BTIH coalescing and IP geolocation; exact ISO3 selection, no ITU scaling or missing-hour imputation. Member colors and location names use the existing cumulative-audit renderer.\n\n'
    return text.replace("WINDOW", window)


def world_trend(site, records, name, extended=False):
    field = 'extended_weeks' if extended else 'weeks'
    end = 26 if extended else len(records[0]['weeks'])
    spec={'title':'Worldwide weekly circulation',
          'subtitle':f'Provisional 2026 Internet-user scale · 6.1 billion reference · weeks 1–{end}',
          'accessible_title':'Weekly worldwide weights at the 2026 Internet-user scale',
          'description':'Izzi native weekly lines. Separate downloader and uploader scales. Not unique viewers.',
          'columns':1,'xmin':1,'xmax':end,'ticks':[[n,str(n)] for n in range(1,end+1)],
          'xlabel':'WEEKS',
          'panels':[{'title':'Worldwide '+role,'unit':'weight','ylabel':role.upper(),
                     'series':[series(r['label'],i,[point(w['week'],w['world'][role]['size']*r['itu_2026']['factor'],
                         f"{r['label']} · worldwide {role} · week {w['week']} · {w['dates']} · {w['world'][role]['size']*r['itu_2026']['factor']:,.2f} adjusted weight") for w in r[field]])
                               for i,r in enumerate(records)]} for role in ['downloaders','uploaders']]}
    WEEKLY_GRAPHS.render(site,name,spec)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--calculations', type=Path, required=True)
    parser.add_argument('--site', type=Path, required=True)
    parser.add_argument('--cartofreako', type=Path, required=True)
    parser.add_argument('--izzi', type=Path, required=True)
    parser.add_argument('--countries', type=Path, required=True)
    parser.add_argument('--lakes', type=Path, required=True)
    parser.add_argument('--pairs', type=Path, required=True)
    parser.add_argument('--page', choices=['pitt-bear-compare', 'godzilla', 'asia-asian-where'])
    parser.add_argument('--country-manifest', type=Path, help='Verified native sample-cache country manifest for Pitt-201')
    args = parser.parse_args()
    site = args.site
    data = json.loads(args.calculations.read_text())
    records = data['objects']
    pairs = json.loads(args.pairs.read_text())
    global WEEKLY_GRAPHS
    # Enforce the direct-label convention for all AAPI subpage generators.
    collection_keys = {r['label']: k for source in [records, pairs['objects']] for k, r in source.items()}
    WEEKLY_GRAPHS = IzziWeeklyGraphs(args.izzi, collection_keys=collection_keys)
    if args.page not in ('pitt-bear-compare', 'asia-asian-where'):
        from mellon_7_6_native_maps import NativeMaps
        native = NativeMaps(site, args.cartofreako, args.izzi, args.countries, args.lakes)
        data['basemap'] = native.provenance
    if args.page in (None, 'pitt-bear-compare'):
        from mellon_7_6_country_plates import render_country_plates
        manifest = args.country_manifest or site/'docs/figures/pitt-201-country-map-manifest.json'
        country_plates = render_country_plates(site, manifest, table)
        data['pitt_201_country_maps'] = {
            'input_mode': 'sample-cache-cumulative',
            'manifest': 'docs/figures/pitt-201-country-map-manifest.json',
            'displayed_variant': 'combined',
            'replaces': 'pitt_201_resolution_plates (historical weekly by-BTIH product)',
        }
    # Keep the 22k city rows inspectable without 700k lines of indentation.
    published = {**data, 'objects': {k: {**v, 'cities': '__CITY_ROWS_' + k + '__'} for k, v in records.items()}}
    serialized = json.dumps(published, ensure_ascii=False, indent=2)
    for key, record in records.items():
        rows = '[\n' + ',\n'.join('        ' + json.dumps(city, ensure_ascii=False, separators=(',', ':')) for city in record['cities']) + '\n      ]'
        serialized = serialized.replace(json.dumps('__CITY_ROWS_' + key + '__'), rows)
    assert json.loads(serialized) == data
    (site / 'data/mellon-7.6-analysis.json').write_text(serialized + '\n')
    (site / 'data/mellon-7.6-itu-2026.json').write_text(json.dumps(data['itu_policy'], indent=2) + '\n')
    shutil.copyfile(ROOT / 'scripts/analyze-mellon-7-6-aapi.py', site / 'resources/mellon-7.6-analyze.py')
    shutil.copyfile(ROOT / 'docs/development/20260923_swarm_analysis_mellon_7.5_no_more_bets_calculations.json', site / 'data/mellon-7.5-no-more-bets-calculations.json')
    shutil.copyfile(ROOT / 'scripts/extend-mellon-7-6-aapi.py', site / 'resources/mellon-7.6-extend.py')
    if args.page in (None, 'asia-asian-where'):
        render_pilot(site, pairs, WEEKLY_GRAPHS)
    if args.pairs.resolve() != (site / "data/mellon-7.6-pairs.json").resolve():
        shutil.copyfile(args.pairs, site / "data/mellon-7.6-pairs.json")
    shutil.copyfile(ROOT / "scripts/compare-mellon-7-6-pairs.py", site / "resources/mellon-7.6-pairs.py")
    for name, keys in data['groups'].items():
        if name == 'godzilla' and (site / 'data/mellon-7.8/stage5-current.json').exists():
            print('Godzilla is maintained by render-mellon-7-8-stage5.py; preserving stage 5.')
            continue
        if args.page and name != args.page:
            continue
        rr = [records[k] for k in keys]
        regional = name == 'pitt-bear-compare'
        window = f"1–{len(rr[0]['weeks'])}"
        title = 'The Pitt and The Bear: India, Philippines, Australia' if regional else 'Godzilla and Monarch: Japan, USA, China and South Korea'
        text = header(title, 'Geographic and mobile-network comparison at matched sampling weeks')
        text += summaries(name, rr)
        text += '\n## Objects and observation windows\n\n'
        if regional:
            text += 'The comparison includes two three-episode Pitt groups from 2026 and Bear seasons 2–5, sampled in 2023–2026 respectively. Episode groups and a whole-season torrent inventory have different scopes. These are object-specific comparisons, not a ranking of the two entire series. The Bear special (`bear-00`) remains outside this selection.\n'
        else:
            text += 'The selection combines three Godzilla films and four Monarch objects. Monarch 101 and 201 each contain three episodes (101–103 and 201–203); 110 is one episode, and 208 contains episodes 208–210. Film, episode and episode-group scopes differ. These cases cannot isolate a production-country effect from year, title, inventory or distribution. “Korea” means South Korea (KOR); North Korea is not pooled into that result.\n'
        text += table(['Object / key', 'Full available sample', 'Analyzed weeks ' + window, 'Worldwide downloader weight', 'Worldwide uploader weight'], [[f"{r['label']} / `{k}`", r['sample_duration'], r['weeks'][0]['dates'].split('-to-')[0] + ' to ' + r['weeks'][-1]['dates'].split('-to-')[1], fmt(r['world']['downloaders']['size']), fmt(r['world']['uploaders']['size'])] for k, r in zip(keys, rr)])
        text += coverage(name, rr)
        text += itu_section(site, rr, data['itu_policy'])
        fname = 'mellon-7.6-' + name + '-world-weekly-itu-2026'
        world_trend(site, rr, fname, extended=regional)
        world_window = "1–26" if regional else window
        text += figure(site, fname, f'Standard Izzi C++ weekly graphs for all {len(rr)} media objects, with names directly on their lines. Worldwide weekly downloaders and uploaders, weeks ' + world_window + ', scaled to the provisional 6.1-billion 2026 reference. The two role panels use different vertical scales. Lines stop at each object’s last available full bin. Raw interval values are retained in the ledger.')
        if regional:
            text += 'Hover a media-object name to highlight its line in red; keyboard focus or tapping a series also highlights it. Leave the plot or press Escape to restore the original colors. Available full bins: Pitt 201–203 **26**, Pitt 213–215 **23**, Bear S05 **11**, and Bear S02–S04 **26 each**.\n'
        sensitivity = data['coverage_sensitivity'][name]
        text += '\n### Coverage sensitivity\n\n'
        text += 'As a conservative check, exclude every elapsed-week index that has a `-partial` export flag or overlaps an audit-reported gap in **any** compared object, from **all** objects. Partial flags can reflect member-level coverage and are not an estimate of missing hours. Retained week indices: **' + ', '.join(map(str, sensitivity['retained_weeks'])) + '**. The table compares downloader world shares; it does not impute missing observations.\n'
        text += table(['Country', 'Object', 'Weeks ' + window + ' share', 'Retained-weeks share'], [[COUNTRIES[c], r['label'], f"{pct(r['country'][c]['downloaders']['size'], r['world']['downloaders']['size']):.2f}%", f"{pct(sensitivity['objects'][k]['country'][c]['downloaders']['size'], sensitivity['objects'][k]['world']['downloaders']['size']):.2f}%"] for c in rr[0]['countries'] for k, r in zip(keys, rr)])
        text += f"This leaves {len(sensitivity['retained_weeks'])} of {len(rr[0]['weeks'])} intervals. It is a sparse coverage diagnostic; missing observations are not estimated.\n"
        text += '\n## Country distribution and network composition\n\nCounts below are summed weekly swarm weights. Geographic shares use the worldwide role total; flag rates use the country role total.\n'
        for role in ['downloaders', 'uploaders']:
            rows = []
            for c in rr[0]['countries']:
                for r in rr:
                    v = r['country'][c][role]
                    world = r['world'][role]
                    rows.append([COUNTRIES[c], r['label'], fmt(v['size']), f"{pct(v['size'], world['size']):.2f}%", f"{pct(v['mobile'], v['size']):.2f}%", f"{pct(v['hosting'], v['size']):.2f}%", f"{pct(v['vpn'], v['size']):.2f}%", f"{pct(v['size']-v['hosting'], world['size']-world['hosting']):.2f}%"])
            text += '### ' + role.capitalize() + '\n'
            text += table(['Country', 'Object', 'Weight', 'World share', 'Mobile rate', 'Hosting rate', 'VPN rate', 'World share excluding hosting'], rows)
        if regional:
            text += '\n' + country_plates
        if not regional:
            text += '\n## Hot and cold locations\n\nRed circles (Hot) indicate a larger share for the first named object; blue circles (Cold) indicate a smaller share. These are selected differences in **city share of the worldwide swarm**, rather than differences in raw title size. Hover or focus a circle for its values; the following table provides the same evidence.\n'
            pairs = [(rr[0], rr[1]), (rr[0], rr[2])]
            scale = max(abs(p['delta']) for a, b in pairs for p in locations(a, b))
            for i, (a, b) in enumerate(pairs, 1):
                fname = 'mellon-7.6-' + name + f'-map-{i}'
                rows = map_plot(site, native, a, b, fname, scale)
                text += figure(site, fname, ('Selected shared city locations; weeks ' + window + '. ') + 'Full counts and periods are in the calculation ledger. Land: Natural Earth via Cartofreako.')
                text += table(['Country / city', a['label'] + ' weight', b['label'] + ' weight', 'First world share', 'Second world share', 'Difference (pp)'], [[COUNTRIES[p['country']] + ' / ' + p['city'], fmt(p['a']), fmt(p['b']), f"{p['a_share']:.3f}%", f"{p['b_share']:.3f}%", f"{signed_pp(p['delta'])}"] for p in rows])
                positive = max(rows, key=lambda p: p['delta'])
                negative = min(rows, key=lambda p: p['delta'])
                text += f"Among the selected shared locations, {positive['city']} has the largest positive difference ({positive['delta']:+.3f} pp) and {negative['city']} the smallest difference ({negative['delta']:+.3f} pp). These comparisons normalize by each object's worldwide swarm weight; they do not imply the same ordering of absolute counts.\n"
        text += '\n## Weekly behavior\n\nEach line shows that week’s country share of worldwide downloader weight. All panels use the same vertical scale. Comparing shares separates geographic composition from changes in total observed swarm size.\n'
        fname = 'mellon-7.6-' + name + '-weekly'
        trend(site, rr, fname)
        text += figure(site, fname, ('Seven-day interval shares, elapsed weeks ' + window + '; ') + 'calendar dates differ by object. Missing sampling hours remain unadjusted.')
        for role in ['downloaders', 'uploaders']:
            fname = 'mellon-7.6-' + name + '-weekly-itu-2026' + ('-uploaders' if role == 'uploaders' else '')
            trend(site, rr, fname, adjusted=True, role=role)
            text += figure(site, fname, role.capitalize() + ' swarm weights, weeks ' + window + ', at the provisional 2026 Internet-user scale (6.1 billion). Each object uses its sample-start-year factor; country-specific penetration and missing hours are not adjusted.')
        if not regional:
            text += 'Vs. Kong shows a pronounced USA change between weeks 4 and 5 (April 21–27 versus April 28–May 4, 2021): downloader weight rises from **224,155 to 1,210,927**, and world share from **7.54% to 24.41%**. Excluding hosting still leaves a rise from **5.81% to 22.33%**. The weekly aggregate does not establish whether this reflects torrent-inventory changes, collection behavior or demand; it should not be attributed to a release event or mobile adoption without further evidence.\n\n'
        text += weekly_commentary(rr)
        text += '\n<details markdown="1"><summary>Weekly counts, mobile rates and calendar dates</summary>\n\n'
        text += table(['Object', 'Week / dates', 'World downloaders', 'Country', 'Country downloaders', 'World share', 'Mobile rate'] + ['2026 adjusted country weight (provisional)'], [[r['label'], f"{w['week']} / {w['dates']}", fmt(w['world']['downloaders']['size']), COUNTRIES[c], fmt(w['country'][c]['downloaders']['size']), f"{pct(w['country'][c]['downloaders']['size'], w['world']['downloaders']['size']):.2f}%", f"{pct(w['country'][c]['downloaders']['mobile'], w['country'][c]['downloaders']['size']):.2f}%"] + [fmt(w['country'][c]['downloaders']['size'] * r['itu_2026']['factor'])] for r in rr for w in r['weeks'] for c in r['countries']])
        text += '\n</details>\n'
        if regional:
            text += extended_section(site, rr)
            text += calendar_section(site, rr)
        text += projections(regional)
        text += methods(regional, window)
        text += '\n## References and reproduction\n\n'
        text += '- [Weekly graph series and native Izzi renderer provenance](../data/mellon-7.6-weekly-graphs.json). All weekly lines use Izzi `make_line_graph` and its native marker API; download the [C++ renderer](../resources/izzi-weekly-graphs.cc) and [Python wrapper](../resources/izzi_weekly_graphs.py).\n'
        text += '- [Calculation ledger: every interval, country, network field, city and source SHA-256](../data/mellon-7.6-analysis.json). All ten flags for both roles are retained.\n'
        for r in rr:
            for s in r['sources'][:2]:
                text += f"- [{r['label']}: {Path(s['path']).name}]({s['url']}).\n"
            text += f"- [{r['label']}: first analyzed weekly GeoJSON]({r['sources'][2]['url']}); matched and extended interval filenames and hashes are in the ledger. Companion export version `{r['data_version']}`; IP-geolocation version `{r['ip_geolocation_version']}`.\n"
        text += f"- [Native projection source]({data['basemap']['url']}); SHA-256 `{data['basemap']['sha256']}`. Natural Earth data are public domain; [country and lake geometry with upstream hashes](../data/mellon-7.6-map-boundaries.json).\n"
        text += '- [Download the analysis script](../resources/mellon-7.6-analyze.py) and [ITU configuration](../data/mellon-7.6-itu-2026.json). Run with `--source-root /path/to/checkouts --output /path/to/output --itu-config /path/to/mellon-7.6-itu-2026.json`, with the annual repositories checked out at the ledger commits. It emits JSON only. Then run the [extension script](../resources/mellon-7.6-extend.py) in the same directory as the analysis script with `--source-root /path/to/checkouts --ledger /path/to/output/analysis.json` to add extended intervals and by-BTIH resolution weights. [Figure and validation scripts (repository access required)](https://github.com/bdekoz/alpha60/tree/main/scripts): `render-mellon-7-6-aapi.py` and `check-mellon-7-6-aapi.py`.\n'
        if not regional:
            text += production_references()
        (site / 'docs' / (name + '.md')).write_text(text)
    WEEKLY_GRAPHS.save_ledger(site / 'data/mellon-7.6-weekly-graphs.json', merge=bool(args.page))
    for helper in ['izzi-weekly-graphs.cc', 'izzi_weekly_graphs.py', 'mellon-7.6-analysis.css']:
        shutil.copyfile(ROOT / 'scripts' / helper, site / 'resources' / helper)
    index = site / 'index.md'
    content = index.read_text()
    marker = '- [Asian American Media](docs/aam.html)'
    additions = '\n- [Asian-global and U.S. context: three geographic pilot cases](docs/asia-asian-where.html)\n- [The Pitt versus The Bear: India, Philippines and Australia](docs/pitt-bear-compare.html)\n- [Godzilla: Japan, USA, China and South Korea](docs/godzilla.html)'
    if 'docs/asia-asian-where.html' not in content:
        content = content.replace(marker, marker + additions)
    content = content.replace('Asian-global and U.S. context: three geographic pilot cases', 'AAPI and Asian-global: matched geographic comparisons').replace('Godzilla: Japan, USA, China and South Korea', 'Godzilla and Monarch: Japan, USA, China and South Korea')
    index.write_text(content)


def render_pilot(site, pairs, graphs):
    if (site / 'data/mellon-7.8-pairs.json').exists():
        raise ValueError('Current pair selection uses Mellon 7.8; run review-mellon-7-8-pairs.py to preserve its approved producer-country comparison and separate AAM rule.')
    source = (ROOT / 'docs/development/20260922_swarm_analysis_mellon_7.3_asian_v_aapi_where.md').read_text()
    text = header('Asian-global and U.S. context: three geographic pilot cases', 'American Born Chinese, Shogun and No More Bets: geography and network attributes')
    text += '''## Summary

American Born Chinese has a higher USA downloader share than Shogun (17.85%
versus 7.03%), but most of that gap disappears when hosting is excluded
(4.93% versus 4.32%). No More Bets supplies a non-USA-production case: its
USA share is 4.94% and Asia-27 share 24.83%, with 88.82% of its uploader
weight located in Asia-27. The third object has a longer sampling window and
a newer geolocation pipeline. These selected cases describe observed network
geography; they do not establish that production or citizenship predicts audience location.

## Definition and current scope

The proxy is **USA production AND at least two counted U.S. citizens** among
qualifying contributors in `asian-led-global`. Under the reviewed Round 3
rules, American Born Chinese has three counted citizens (YES), Shogun one
(NO), and No More Bets zero plus non-USA production (NO). The current
confirmed cohort is 82 YES / 230 NO, with 26 unresolved candidates separate.
This page is a three-object pilot, not the proposed full-cohort study.

Both original objects also qualify for the broader metadata `aapi-led` slice
and appear in this site's editorial roster. No More Bets qualifies for that
broader metadata slice but is absent from the 47-object editorial roster.
The metadata composition, production/citizenship proxy and editorial roster
are distinct definitions. This analysis does not change the site's roster.

The original pair each spans 105 days / 15 weeks: American Born Chinese
2023-05-24–2023-09-05 (194 BTIHs), Shogun 2024-02-28–2024-06-11 (297).
Both original exports use data version `2025-09-22` and IP-geolocation
version `3:1756800417`. The No More Bets section gives its longer window.

### Geographic boundary

Asia-27 is the project's explicitly approved set, not a general continental
classification: `AFG BGD BRN BTN CHN HKG IDN IND IRN JPN KHM KOR LAO LKA
MAC MDV MMR MNG MYS NPL PAK PHL PRK SGP THA TLS VNM`.
It includes Iran and excludes Taiwan. The exact list controls all totals.

'''
    start = source.index('### Sources and calculation')
    end = source.index('## Round 3 threshold addendum')
    text += source[start:end]
    start = source.index('## Third pilot object: No More Bets')
    text += source[start:]
    text += '''
## Citizenship revision and analysis history

The September 23 citizenship-list extension reduced American Born Chinese's
Asian-global count from four to three after a conflict involving Chin Han;
its YES assignment is unchanged. Shogun remains at one and NO. Only the two
Masters of the Air objects moved across the full-cohort threshold, changing
84/228 to 82/230. The pilot geography did not change. The full-cohort
geographic effect of those reassignments has not been measured.

The linked development analysis retains the dated Round 1–3 history and
the proposed cohort method. Canonical metadata references require repository
access; the geographic exports and calculation ledger are public.

'''
    text += '- [Development analysis and dated revisions (repository access required)](https://github.com/bdekoz/alpha60/blob/64732d07a/docs/development/20260922_swarm_analysis_mellon_7.3_asian_v_aapi_where.md).\n'
    text += '- [Pinned Asia-27 boundary (repository access required)](https://github.com/bdekoz/alpha60/blob/64732d07a/config/mellon-7/geographic-slices-v1.json); the full 27-code definition is reproduced above.\n'
    text = text.replace('(20260923_swarm_analysis_mellon_7.5_no_more_bets_calculations.json)', '(../data/mellon-7.5-no-more-bets-calculations.json)')
    text = text.replace('Pin the canonical v3 report and its artifact digest recorded below;', 'Pin the canonical v3 report and its artifact digest in the development analysis;')
    text = text.replace('the remaining 24 codes', 'the remaining 24 codes (use South Korea for the highlighted Korea comparison)')
    # Pin the two legacy geographic inputs to the pre-publication site commit.
    text = text.replace('/alpha60-results-aapi-led/main/data/', '/alpha60-results-aapi-led/4039b679088456c4b3068f99d9e9314fb9894167/data/')
    from mellon_7_6_pairs_report import render_pairs
    historical = text[text.index('## Summary'):]
    historical = historical.replace('## Definition and current scope', '## Definition and scope at the time')
    historical = historical.replace('The current\nconfirmed cohort', 'The September 23\nconfirmed cohort')
    historical = historical.replace("Asia-27 is the project's explicitly approved set", "Asia-27 was the project's approved pilot set")
    historical = re.sub(r'^(#{2,5}) ', r'\1# ', historical, flags=re.MULTILINE)
    text = header('AAPI and Asian-global: matched geographic comparisons', 'Three matched 15-week pairs, current Asia-28 geography, and the historical pilot')
    text += render_pairs(site, pairs, table, figure, graphs)
    text += '\n## Historical cumulative pilot: Asia-27\n\nThe following September 23 pilot keeps its original cumulative inputs and Asia-27 boundary (without TWN). Its eligibility counts describe that dated review. The September 24 Taiwan extension restored American Born Chinese to four counted citizens in Asian-global and changed the full-cohort proxy from 82/230 to 84/228. The new matched comparisons above use the current evidence and Asia-28.\n\n<details markdown="1"><summary>Original American Born Chinese, Shogun and No More Bets analysis</summary>\n\n'
    text += historical + '\n</details>\n'
    (site / 'docs/asia-asian-where.md').write_text(text)


def summaries(name, records):
    # Authored after inspecting calculated outputs; kept separate for review.
    return (ROOT / 'config/mellon-7' / (name + '-7.6-summary.md')).read_text()


def coverage(name, records):
    text = '\n### Sampling coverage\n\n'
    for r in records:
        notes = '; '.join(n.removeprefix('- ').split('Input: **sample-cache-cumulative**.')[0].strip() for n in r['coverage_notes']).rstrip('; ')
        text += '- **' + r['label'] + ':** ' + (notes or 'No gap inventory found; this does not establish complete hourly coverage.') + '\n'
    return text + '\nThese are full-sample audit notes. Only dates overlapping the selected intervals enter the coverage sensitivity below. Opening bins are retained. Missing hours are not imputed.\n'


def weekly_commentary(records):
    text = ''
    for r in records:
        bits = []
        for c in r['countries']:
            ws = r['weeks']
            peak = max(ws, key=lambda w: w['country'][c]['downloaders']['size'])
            first, last = ws[0]['country'][c]['downloaders'], ws[-1]['country'][c]['downloaders']
            change = 100 * (last['size'] / first['size'] - 1)
            mobile_delta = pct(last['mobile'], last['size']) - pct(first['mobile'], first['size'])
            bits.append(f"{COUNTRIES[c]} peaks in week {peak['week']} ({fmt(peak['country'][c]['downloaders']['size'])}); week {ws[-1]['week']} versus week {ws[0]['week']} weight changes {change:+.1f}%, and mobile rate changes {mobile_delta:+.2f} pp")
        text += '- **' + r['label'] + ':** ' + '; '.join(bits) + '.\n'
    return text + '\nThese are descriptive peaks within the selected bins, not release-day peaks or evidence of a weekday effect. No daily or hourly behavioral claim is inferred from weekly data.\n'


def projections(regional):
    if regional:
        return """
## Map projection and country outlines

The country close-ups use the existing **a60-carto-geo** cumulative-cache
renderer: **Izzi** draws the vectors and **Cartofreako** supplies registered
Cahill–Keyes coordinates. Country outlines and locations fit the available
width or height with a uniform projected scale. Geographic scale differs by
country; circle areas share one weight scale. Natural Earth 1:10m country
polygons retain interior holes and projection seams, with lake water removed.
Location names use the audit's existing centered, weight-sized Apercu text
at their mapped coordinates. Click a preview to open the 3840-pixel image
in a new tab; vector SVGs and accounting receipts are linked below each map.

[Country geometry and upstream hashes](../data/mellon-7.6-cache-map-boundaries.json).
[Native renderer and input manifest](figures/pitt-201-country-map-manifest.json).
"""
    return """
## Map projection and country outlines

The city-difference panels use **Cartofreako's native Cahill–Keyes projection**,
with its one-degree longitude registration, and **Izzi** for the vector SVG.
Each country's complete projected outline and selected city coordinates are
uniformly fitted into its panel, preserving projected proportions. Panel scales
therefore differ by country; geographic area is not comparable between panels.
City values still use the same world denominators and color scale across maps.

Natural Earth v5.1.2 1:10m country polygons have intersecting lake and reservoir
water removed. Interior rings are retained with even-odd filling, and country
polygons are split at the registered octant seams before projection. This keeps
Great Lakes shorelines visible and avoids lines bridging projection cuts.
Boundaries follow Natural Earth's de facto geometry. The six Pitt resolution
plates are documented separately on the Pitt/Bear comparison page.

References: [Cartofreako Cahill–Keyes geometry and octants](https://bdekoz.github.io/cartofreako/docs/pages/projections/cahill-keyes/context.html),
[Izzi](https://github.com/bdekoz/izzi), and the
[country and lake geometry with source hashes](../data/mellon-7.6-map-boundaries.json).
"""


def production_references():
    return (ROOT / 'config/mellon-7/godzilla-7.6-production-references.md').read_text()


def itu_section(site, records, policy):
    text = '''
## ITU adjustment to 2026 — provisional reference

**The 6.1-billion reference for 2026 is the project's provisional estimate,
not an official ITU 2026 observation.** The latest official release checked
on September 24, 2026 covers 2025. This status applies to every adjusted
number and adjusted-count figure on this page.

`2026 adjusted weight = raw weight × 6.1 / source-year Internet users (billions)`.
The sample-start year selects the denominator. This scales global Internet-user
growth; it does not adjust country-specific penetration, sampling coverage,
episodes per object or torrent inventories. It is not an estimate of viewers.
Applying the same multiplier to all counts within an object leaves country
shares, mobile rates and hosting rates unchanged.

The historical 2023 and 2024 denominators retain the project's as-published
vintages for comparability. ITU later revised 2024 from 5.5 to 5.8 billion;
the sensitivity below makes the effect explicit. No official 2026 precision
or confidence interval is implied.
'''
    text += table(['Object', 'Sample year', 'Internet users (billions)', '2026 factor', 'Raw world downloaders', '2026 adjusted world downloaders'], [[r['label'], r['year'], r['itu_2026']['source_users_billions'], f"{r['itu_2026']['factor']:.6f}", fmt(r['world']['downloaders']['size']), fmt(r['itu_2026']['world']['downloaders']['size'])] for r in records])
    text += f'\n### Country counts at the 2026 scale, weeks 1–{len(records[0]["weeks"])}\n\nAdjusted values are rounded only for display. Raw counts and unrounded calculations are retained in the ledger.\n'
    text += table(['Country', 'Object', 'Raw downloaders', '2026 adjusted downloaders', '2026 adjusted mobile downloaders', 'Raw uploaders', '2026 adjusted uploaders'], [[COUNTRIES[c], r['label'], fmt(r['country'][c]['downloaders']['size']), fmt(r['itu_2026']['country'][c]['downloaders']['size']), fmt(r['itu_2026']['country'][c]['downloaders']['mobile']), fmt(r['country'][c]['uploaders']['size']), fmt(r['itu_2026']['country'][c]['uploaders']['size'])] for c in records[0]['countries'] for r in records])
    revised = [r for r in records if r['year'] == 2024]
    text += '\n### Revised 2024 denominator sensitivity\n\nUsing the later 5.8-billion estimate changes every 2024 object’s multiplier from 1.109091 to 1.051724, lowering its adjusted weights by 5.17%. Country shares and mobile rates are unchanged. This replaces only the 2024 denominator; it is not a fully revised historical ITU series.\n'
    text += table(['Country', '2024 object', 'Adjusted with 5.5b', 'Adjusted with revised 5.8b'], [[COUNTRIES[c], r['label'], fmt(r['itu_2026']['country'][c]['downloaders']['size']), fmt(r['itu_2026']['revised_2024_scenario']['country'][c]['downloaders']['size'])] for r in revised for c in r['countries']])
    years = sorted({str(r['year']) for r in records if r['year'] != 2026})
    text += '\nSources: ' + ', '.join(f"[ITU {year}]({policy['years'][year]['source_url']})" for year in years) + f", [ITU 2025 and revised 2024]({policy['years']['2025']['source_url']}), [latest publication index]({policy['official_latest_checked']['url']}), and [versioned calculation policy](../data/mellon-7.6-itu-2026.json).\n"
    return text


def extended_section(site, records):
    text = '''
## Weeks 1–26: available coverage

The extended view retains every available seven-day interval through week 26.
Lines stop at the last full calendar bin: missing future weeks and shorter
trailing bins are not zero. Full-length bins can still contain sampling gaps
or a `-partial` member-coverage flag. The matched ten-week tables above remain
separate from this unequal-length view.
'''
    text += table(['Object', 'Plotted weeks', 'Calendar extent', 'Unplotted trailing coverage'], [[r['label'], f"1–{r['extended_weeks'][-1]['week']}", r['extended_weeks'][0]['dates'].split('-to-')[0] + ' to ' + r['extended_weeks'][-1]['dates'].split('-to-')[1].removesuffix('-partial'), '; '.join(f"week {e['week']}: {e['reason']}" for e in r['extended_exclusions'] if e['reason'] != 'not available') or ('Weeks after available end are missing' if r['extended_exclusions'] else 'None through week 26')] for r in records])
    for adjusted in (False, True):
        name = 'mellon-7.6-pitt-bear-extended-' + ('itu-2026' if adjusted else 'shares')
        trend(site, records, name, adjusted=adjusted, extended=True)
        text += figure(site, name, 'Available weeks 1–26; lines stop at observed full-bin coverage. ' + ('Adjusted downloader weights use the provisional 6.1-billion 2026 reference.' if adjusted else 'Country shares use each interval’s worldwide downloader denominator.'))
    text += '\n<details markdown="1"><summary>Extended weekly values and dates</summary>\n\n'
    text += table(['Object', 'Week / dates', 'Country', 'Raw downloaders', '2026 adjusted downloaders (provisional)', 'World share'], [[r['label'], f"{w['week']} / {w['dates']}", COUNTRIES[c], fmt(w['country'][c]['downloaders']['size']), fmt(w['country'][c]['downloaders']['size'] * r['itu_2026']['factor']), f"{pct(w['country'][c]['downloaders']['size'], w['world']['downloaders']['size']):.2f}%"] for r in records for w in r['extended_weeks'] for c in r['countries']])
    return text + '\n</details>\n'


def calendar_section(site, records):
    a = next(r for r in records if r['label'] == 'The Pitt 213–215')
    b = next(r for r in records if r['label'] == 'The Bear S05')
    aa = {w['dates'].removesuffix('-partial'): w for w in a['extended_weeks']}
    bb = {w['dates'].removesuffix('-partial'): w for w in b['extended_weeks']}
    dates = sorted(aa.keys() & bb.keys())
    assert len(dates) == 11 and dates[0] == '2026-06-26-to-2026-07-02' and dates[-1] == '2026-09-04-to-2026-09-10'
    text = '''
## Same-calendar comparison: Pitt 213–215 versus Bear S05

The two samples overlap in 2026, although they begin 12 weeks apart: April 3
for Pitt 213–215 and June 26 for Bear S05. This comparison pairs **June 26–
September 10, 2026**, matching Pitt elapsed weeks **13–23** to Bear weeks
**1–11**. The shared one-day trailing bin on September 11 is excluded.

This aligns calendar conditions while comparing different points in each
object’s sampling history. The three-episode-versus-season scope still differs.
Both are 2026 samples, so the provisional ITU multiplier is 1: adjusted weights
equal raw weights. The sums below remain repeated swarm weights, not people.
'''
    rows = []
    for c in a['countries']:
        for r, lookup in [(a, aa), (b, bb)]:
            world = sum(lookup[d]['world']['downloaders']['size'] for d in dates)
            weight = sum(lookup[d]['country'][c]['downloaders']['size'] for d in dates)
            mobile = sum(lookup[d]['country'][c]['downloaders']['mobile'] for d in dates)
            hosting = sum(lookup[d]['country'][c]['downloaders']['hosting'] for d in dates)
            rows.append([COUNTRIES[c], r['label'], fmt(weight), f'{pct(weight, world):.2f}%', f'{pct(mobile, weight):.2f}%', f'{pct(hosting, weight):.2f}%'])
    text += '\nWorldwide downloader denominators over these paired bins: ' + '; '.join(r['label'] + ' **' + fmt(sum(lookup[d]['world']['downloaders']['size'] for d in dates)) + '**' for r, lookup in [(a, aa), (b, bb)]) + '.\n'
    text += table(['Country', 'Object', 'Downloader weight / 2026 adjusted', 'World share', 'Mobile rate', 'Hosting rate'], rows)
    text += '\nOver the shared calendar window, Bear S05 has higher downloader weights and worldwide shares in all three countries: India **0.40% versus 0.30%**, Philippines **0.18% versus 0.14%**, and Australia **1.39% versus 0.99%**. This differs from the opening-ten-week comparison, where Pitt 213–215 has higher Philippine and Australian shares than Bear S05. The window choice materially changes those two comparisons. Mobile rates are close: Pitt is higher in the Philippines (**20.94% versus 19.85%**), while Bear is higher in India (**18.37% versus 17.46%**) and Australia (**3.09% versus 2.86%**). These observations do not isolate a release-timing effect.\n'
    text += '\nDuring this window, the Pitt audit reports one missing hour on August 30–31 and nine on September 10–11; Bear reports 29 missing hours spanning August 14–16. The last Pitt gap straddles the end of the selected period. Missing observations are not imputed. These counts should not be interpreted as equally complete samples.\n'
    # Keep the previously approved same-calendar study on its actual date axis.
    maximum = max(pct(lookup[d]['country'][c]['downloaders']['size'], lookup[d]['world']['downloaders']['size']) for lookup in [aa,bb] for d in dates for c in a['countries'])
    name = 'mellon-7.6-pitt-bear-calendar'
    spec={'title':'Pitt 213–215 and Bear S05 in the same calendar weeks',
          'subtitle':'June 26–September 10, 2026 · matched calendar intervals · country downloader shares',
          'description':'Izzi native lines. Existing calendar comparison; different elapsed sampling weeks.',
          'columns':1,'xmin':1,'xmax':len(dates),'ticks':[[i+1,dates[i][:10]] for i in [0,3,6,8,10]],
          'xlabel':'Seven-day interval start',
          'panels':[{'title':COUNTRIES[c],'unit':'percent','ylabel':'World share (%)','y_max':maximum*1.12,
                     'series':[series(r['label'],i,[point(j+1,pct(lookup[d]['country'][c]['downloaders']['size'],lookup[d]['world']['downloaders']['size']),
                         f"{r['label']} · {COUNTRIES[c]} · {d} · {pct(lookup[d]['country'][c]['downloaders']['size'],lookup[d]['world']['downloaders']['size']):.3f}% of world") for j,d in enumerate(dates)])
                               for i,(r,lookup) in enumerate([(a,aa),(b,bb)])]} for c in a['countries']]}
    WEEKLY_GRAPHS.render(site,name,spec)
    text += figure(site, name, 'Exact matching calendar intervals, June 26–September 10, 2026. Elapsed sampling weeks differ by 12.')
    return text


if __name__ == '__main__':
    main()
