"""Orchestrate and audit native izzi/Cartofreako country SVGs.

Python performs input accounting, exports and page assembly; all cartographic
projection, fitting, outlines, labels and bubbles are drawn by a60-carto-geo.
"""
from __future__ import annotations

import collections
import gzip
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tarfile
import xml.etree.ElementTree as ET

from media_object_audit_figures import validate_country_map

BEGIN = '<!-- BEGIN country-resolution-detail -->'
END = '<!-- END country-resolution-detail -->'
GROUPS = ('combined', 'ge-1080p', 'lt-1080p')


def digest(path):
    with open(path, 'rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def compact_native_svg(source, target):
    """Remove optional circle-tag whitespace; retain every native drawing value.

    Cache-based plates can contain hundreds of thousands of izzi circles.
    Compact only their generated CSS separators and self-closing tag spacing.
    Text, paths, order, numeric precision, colors and opacity are untouched.
    """
    original = Path(source).read_text()
    native_sha = digest(source)
    compact = re.sub(r'<circle\b[^>]*>',
                     lambda m: m[0].replace('; ', ';').replace(' />', '/>'), original)
    Path(target).write_text(compact)
    return {'method':'circle-tag whitespace only', 'native_sha256':native_sha,
            'native_bytes':len(original.encode()), 'published_bytes':len(compact.encode())}


def apportion(weights, expected):
    """Independent integer largest-remainder allocation, over worldwide keys."""
    emitted = sum(weights.values())
    if emitted > expected:
        raise ValueError('geographic weights exceed member total')
    if not emitted:
        return dict(weights)
    result = {key: weight * expected // emitted for key, weight in weights.items()}
    order = sorted(weights, key=lambda k: (-(weights[k]*expected % emitted), k))
    for key in order[:expected-sum(result.values())]:
        result[key] += 1
    return result


def native_key(properties):
    # Match the existing loader's ISO-8859-16 conversion of city bytes.
    city = properties['city'].encode('utf-8').decode('iso8859_16').replace(' ', '-')
    return properties['country_code'] + '_' + city


def verify_weights(geojson, metadata, records, boundary):
    """Reduce original feature weights independently; compare every member/role."""
    from shapely.geometry import shape, Point
    from shapely.prepared import prep
    meta = json.loads(Path(metadata).read_text())
    modes = {m['name']: m['resolution'] for m in meta['collection_cumulative_by_btiha']}
    geoms = {c['iso3']: prep(shape(c['geometry']))
             for c in json.loads(Path(boundary).read_text())['countries']}
    countries = {r['country']: r for r in records}
    raw = {c: {g: dict(downloaders=0, uploaders=0) for g in GROUPS} for c in countries}
    omitted = {c: dict(downloaders=0, uploaders=0, members=[]) for c in countries}
    outside = {c: set() for c in countries}
    inside_cache = {}
    expected = {c: {g: {} for g in GROUPS} for c in countries}
    null = dict(downloaders=0, uploaders=0, features=0)
    data = json.loads(Path(geojson).read_text())
    member_count = 0
    for member in data['collection_cumulative_by_btiha']:
        name = member['id']
        if name not in modes and not member['features']:
            continue  # Native loader also tolerates only empty retired members.
        mode = modes[name]
        group = ('ge-1080p' if mode in ('1080','2160') else
                 'lt-1080p' if mode in ('720','sd') else 'unsupported')
        weights = {role: collections.Counter() for role in ('downloaders','uploaders')}
        codes = {}
        for feature in member['features']:
            props = feature['properties']; coords = feature['geometry']['coordinates']
            if coords == [0, 0]:
                null['features'] += 1
                for role in weights: null[role] += props[role]['size']
                continue
            key = native_key(props); code = props['country_code']; codes[key] = code
            for role in weights: weights[role][key] += props[role]['size']
            if code in countries:
                location = (code, *coords)
                if location not in inside_cache:
                    inside_cache[location] = geoms[code].covers(Point(*coords))
                if not inside_cache[location]: outside[code].add(tuple(coords))
        for code in countries:
            for g in GROUPS:
                expected[code][g][name] = dict(downloaders=0, uploaders=0)
        for role, values in weights.items():
            restored = apportion(values, member['tid_' + role])
            for code in countries:
                value = sum(w for k,w in restored.items() if codes[k] == code)
                if group == 'unsupported':
                    omitted[code][role] += value
                    if value and name not in omitted[code]['members']:
                        omitted[code]['members'].append(name)
                    continue
                original = sum(w for k,w in values.items() if codes[k] == code)
                for g in ('combined', group):
                    expected[code][g][name][role] = value
                    raw[code][g][role] += original
        member_count += 1
    for code, record in countries.items():
        variants = {v['group']: v for v in record['variants']}
        for group, variant in variants.items():
            actual = {m['name']: {role:m[role] for role in ('downloaders','uploaders')}
                      for m in variant['members']}
            if actual != expected[code][group]:
                differences = [n for n in actual if actual[n] != expected[code][group].get(n)]
                raise ValueError(f'{code}/{group}: member weights differ: {differences[:5]}')
            for role in ('downloaders','uploaders'):
                assert sum(m[role] for m in actual.values()) == variant[role]
            variant['raw_published_feature_sums'] = raw[code][group]
        for role in ('downloaders','uploaders'):
            assert variants['combined'][role] == sum(variants[g][role] for g in GROUPS[1:])
            assert variants['combined'][role] == sum(p[role] for p in record['panels'])
        record['excluded_unsupported_resolution'] = omitted[code]
        record['outside_boundary_coordinates'] = sorted(outside[code])
        record['outside_boundary_policy'] = 'diagnostic only; exact country codes retain all weights'
    return {'status':'passed', 'members_checked':member_count,
            'roles':['downloaders','uploaders'], 'worldwide_rescaling_before_filtering':True,
            'null_location_source_wide':null, 'country_partition_and_panel_totals':'passed'}


def verify_cache_accounting(accounting_path, records, boundary):
    """Check slices against a separate native reduction of the prepared cache.

This verifies selection/partitioning, not an independent geolocation of raw IPs.
The reference is written before slicing and contains no IP addresses.
"""
    from shapely.geometry import shape, Point
    from shapely.prepared import prep
    accounting = json.loads(Path(accounting_path).read_text())
    if accounting['input_mode'] != 'sample-cache-cumulative':
        raise ValueError('wrong native cache input mode')
    geoms = {c['iso3']: prep(shape(c['geometry']))
             for c in json.loads(Path(boundary).read_text())['countries']}
    for record in records:
        code = record['country']
        assert record['input_mode'] == accounting['input_mode']
        assert record['dates'] == accounting['dates']
        omitted = dict(downloaders=0,uploaders=0,members=[])
        for member in accounting['members']:
            if member['group'] == 'unsupported':
                for role in ('downloaders','uploaders'):
                    omitted[role] += member['countries'][code][role]
                if any(member['countries'][code].values()):omitted['members'].append(member['name'])
        record['excluded_unsupported_resolution'] = omitted
        for variant in record['variants']:
            expected = {m['name']: (m['countries'][code] if m['group'] != 'unsupported' and
                        (variant['group']=='combined' or m['group']==variant['group']) else
                        dict(downloaders=0,uploaders=0)) for m in accounting['members']}
            actual = {m['name']: {r:m[r] for r in ('downloaders','uploaders')} for m in variant['members']}
            if actual != expected:raise ValueError(f'{code}: cache slice/reference mismatch')
            for role in ('downloaders','uploaders'):
                assert sum(m[role] for m in actual.values()) == variant[role]
        for role in ('downloaders','uploaders'):
            assert record['variants'][0][role] == sum(v[role] for v in record['variants'][1:])
            assert record['variants'][0][role] == sum(p[role] for p in record['panels'])
        record['outside_boundary_coordinates'] = [p for p in accounting['country_coordinates'][code]
                                                   if not geoms[code].covers(Point(*p))]
        record['outside_boundary_policy'] = 'diagnostic only; exact country codes retain all weights'
    return {'status':'passed','input_mode':'sample-cache-cumulative',
            'members_checked':len(accounting['members']), 'roles':['downloaders','uploaders'],
            'reference':'separate native reduction of prepared worldwide cumulative cache',
            'published_geojson_used':False,'publication_threshold_applied':False,
            'worldwide_rescaling_applied':False,'country_partition_and_panel_totals':'passed'}


def extract_cumulative_cache(archive, destination):
    """Extract cumulative JSON members only, without touching the source archive."""
    destination = Path(destination).resolve()
    destination.mkdir(parents=True,exist_ok=True)
    with tarfile.open(archive,mode='r|xz') as stream:
        for member in stream:
            if not member.isfile() or 'cumulative' not in member.name or not member.name.endswith('.json'):
                continue
            target = (destination/member.name).resolve()
            if not target.is_relative_to(destination):raise ValueError('unsafe archive path')
            target.parent.mkdir(parents=True,exist_ok=True)
            with stream.extractfile(member) as src,target.open('wb') as dst:shutil.copyfileobj(src,dst)
    directories = {p.parent for p in destination.rglob('*cumulative*.json')}
    if len(directories) != 1:raise ValueError('expected one cumulative cache directory')
    return directories.pop()


def country_section(records):
    cache_mode = records[0].get('input_mode') == 'sample-cache-cumulative'
    method = ('Input: **sample-cache-cumulative**. These country close-ups are drawn directly '
              'from the original cumulative sample cache after duplicate-BTIH coalescing and '
              'IP geolocation. No published GeoJSON, cell publication threshold or product '
              'rescaling is used.' if cache_mode else
              'Input: **cumulative-geojson**. These country close-ups reconstruct the published '
              'cumulative by-BTIH GeoJSON, with worldwide member rescaling before country selection.')
    lines = [BEGIN, '', '## Country resolution detail', '', method +
             ' No ITU adjustment or missing-hour imputation is applied.', '',
             'Country membership follows the exact source ISO3 code. Boundaries are '
             'Natural Earth 1:10m v5.1.2, with vector lake/reservoir water removed from land; boundary disagreements are retained and '
             'reported in the downloadable receipts. Maps use native izzi and '
             'Cartofreako vector outlines, registered Cahill–Keyes coordinates, '
             'and fixed page-space bubble areas. All countries and resolution views '
             'share the same bubble coefficient and 5% opacity.', '']
    for r in records:
        lines += [f"### {r['name']} ({r['country']})", '',
                  f"Sample: **{r['dates']}**. Radius coefficient: `{r['radius_base']:.12g}`. "
                  'Combined = 1080 + 2160 + 720 + SD; ≥1080p = 1080 + 2160; <1080p = 720 + SD.', '',
                  '<div style="max-width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="Country weight comparison" markdown="1">', '',
                  ('| View | Cumulative-cache downloaders | Cumulative-cache uploaders |' if cache_mode else
                   '| View | Published downloader sum | Rescaled downloaders | Published uploader sum | Rescaled uploaders |'),
                  ('| --- | ---: | ---: |' if cache_mode else '| --- | ---: | ---: | ---: | ---: |')]
        for v in r['variants']:
            if cache_mode:
                lines.append(f"| {v['group']} | {v['downloaders']:,} | {v['uploaders']:,} |")
                continue
            raw = v['raw_published_feature_sums']
            lines.append(f"| {v['group']} | {raw['downloaders']:,} | {v['downloaders']:,} | {raw['uploaders']:,} | {v['uploaders']:,} |")
        lines += ['', '</div>', '', f"[Accounting and layout receipt](figures/{r['receipt_file']})", '']
        if len(r['panels']) > 1:
            lines += ['Insets use independent geographic scales. Bubble areas retain the same weight scale in every panel.', '']
        for v in r['variants']:
            if v['status'] != 'rendered':
                lines += [f"**{v['group']}: no drawable downloader data.**", '']; continue
            stem = Path(v['file']).stem
            if v['group'] != 'combined':
                lines += ['<details markdown="1">', f"<summary>{html.escape(v['group'])} plate</summary>", '']
            lines += [f'<a href="figures/{stem}-4k.webp" target="_blank" rel="noopener"><img src="figures/{stem}.webp" alt="{html.escape(r["name"])} cumulative {v["group"]} downloader map; opens high-resolution image in a new tab"></a>', '',
                      f"[Vector SVG](figures/{stem}.svg) · [3840-pixel long edge](figures/{stem}-4k.webp)", '']
            if v['group'] != 'combined': lines += ['</details>', '']
        lines += ['<details markdown="1">', '<summary>Country-ranked locations and diagnostics</summary>', '',
                  '<div style="max-width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="Country ranked locations" markdown="1">', '',
                  '| View | City | Downloader weight | Label drawn |', '| --- | --- | ---: | --- |']
        for v in r['variants']:
            for label in v['labels']:
                city = html.escape(label['city']).replace('|','&#124;')
                lines.append(f"| {v['group']} | {city} | {label['weight']:,} | {'yes' if label['placed'] else 'no named location'} |")
        lines += ['', '</div>', '', f"Outside-boundary coordinate pairs retained: **{len(r['outside_boundary_coordinates'])}**. "
                  f"Unsupported-resolution downloader weight excluded: **{r['excluded_unsupported_resolution']['downloaders']:,}**.",
                  '', '</details>', '']
    return '\n'.join(lines + [END, ''])


def attach_country_maps(page, manifest_path, figures_dir=None, audit_manifest=None):
    page = Path(page); manifest_path = Path(manifest_path)
    manifest = json.loads(manifest_path.read_text())
    if manifest['validation']['status'] != 'passed':
        raise ValueError('country render manifest has not passed')
    # Full visualization runs have a per-object figure manifest. Annual pages
    # may share a directory, so never update a manifest for another object.
    saved_audit_manifest = None
    if audit_manifest is None:
        candidate = page.parent / 'figure-manifest.json'
        if candidate.is_file():
            value = json.loads(candidate.read_text())
            if value.get('media_object') == manifest['collection']:
                audit_manifest = value
                saved_audit_manifest = candidate
    target = Path(figures_dir) if figures_dir else page.parent / 'figures'
    target.mkdir(parents=True, exist_ok=True)
    for name, sha in manifest['assets'].items():
        source = manifest_path.parent / name
        if digest(source) != sha: raise ValueError(f'country asset digest changed: {name}')
        if source.resolve() != (target/name).resolve(): shutil.copy2(source,target/name)
        if audit_manifest is not None:
            audit_manifest['figures']['country-' + name] = {'file':f'figures/{name}', 'sha256':sha}
    text = page.read_text()
    section = country_section(manifest['countries'])
    if BEGIN in text:
        text = re.sub(re.escape(BEGIN)+'.*?'+re.escape(END), lambda _:section.rstrip(), text, flags=re.S)
    else:
        text = text.rstrip() + '\n\n' + section
    page.write_text(text)
    if saved_audit_manifest is not None:
        write_json(saved_audit_manifest,audit_manifest)
    if manifest_path.resolve() != (target/manifest_path.name).resolve():
        shutil.copy2(manifest_path,target/manifest_path.name)


def render_countries(root, key, geojson, metadata, countries, binary, output, boundary, registry, rasterize,
                     *, input_mode='sample-cache-cumulative', cache_dir=None, cache_archive=None):
    root, output, boundary, registry = map(Path, (root,output,boundary,registry))
    output = output.resolve(); output.mkdir(parents=True,exist_ok=True)
    countries = list(dict.fromkeys(c.strip().upper() for c in countries))
    env = os.environ.copy();env['a60_PREFIX_DIR'] = str(root)
    env.setdefault('a60_DATA_DIR',str(root.parent/'alpha60-data'))
    if input_mode not in ('sample-cache-cumulative','cumulative-geojson'):
        raise ValueError('unknown country input mode')
    if input_mode == 'sample-cache-cumulative':
        if geojson or metadata or (cache_dir is None)==(cache_archive is None):
            raise ValueError('sample-cache-cumulative requires one cache directory or archive and no GeoJSON inputs')
        env.setdefault('a60_GEOLOCATION_DB',str(root.parent/'geoip-databases/ipinfo/standard_location.mmdb'))
    elif cache_dir or cache_archive or geojson is None or metadata is None:
        raise ValueError('cumulative-geojson requires paired published products and no sample-cache input')
    with tempfile.TemporaryDirectory(prefix='country-render-', dir=output) as temporary:
        work = Path(temporary)
        source_identity = {'input_mode':input_mode}
        if input_mode == 'sample-cache-cumulative':
            selected_cache = Path(cache_dir).resolve() if cache_dir else extract_cumulative_cache(cache_archive,work/'cache')
            cache_files = sorted(selected_cache.glob('*cumulative*.json'))
            if not cache_files:raise ValueError('no cumulative cache documents')
            source_identity['cumulative_cache_files'] = [{'file':p.name,'sha256':digest(p),'bytes':p.stat().st_size} for p in cache_files]
            if cache_archive:
                source_identity['cache_archive'] = {'path':str(Path(cache_archive).resolve()),'sha256':digest(cache_archive)}
            database = Path(env['a60_GEOLOCATION_DB'])
            source_identity['geolocation_database'] = {'path':str(database.resolve()),'sha256':digest(database)}
            data_root = Path(env['a60_DATA_DIR'])
            source_identity['torrent_inventory'] = [{'file':p.name,'sha256':digest(p)} for p in sorted((data_root/'torrent'/key).glob('*.torrent'))]
            if not source_identity['torrent_inventory']:raise ValueError('missing torrent inventory')
            command = [str(Path(binary).resolve()),'--quiet','--cumulative-maps',str(selected_cache),key]
        else:
            geojson, metadata = Path(geojson).resolve(), Path(metadata).resolve()
            product = geojson
            if product.suffix == '.gz':
                product = work/'cumulative.geojson'
                with gzip.open(geojson,'rb') as src, product.open('wb') as dst:shutil.copyfileobj(src,dst)
            source_identity.update(geojson_sha256=digest(product),metadata_sha256=digest(metadata))
            command = [str(Path(binary).resolve()),'--quiet','--cumulative-product-maps',str(product),str(metadata),key]
        command += ['--country-boundaries',str(boundary.resolve()),'--country-iso-registry',str(registry.resolve())]
        for code in countries: command += ['--country',code]
        with (output/f'{key}-country-render.log').open('w') as log:
            subprocess.run(command,cwd=work,env=env,stdout=log,stderr=log,check=True)
        records = [json.loads((work/'tmp'/f'{key}-data-country-{c.lower()}.json').read_text()) for c in countries]
        accounting = work/'tmp'/f'{key}-country-source-accounting.json'
        validation = (verify_cache_accounting(accounting,records,boundary)
                      if input_mode=='sample-cache-cumulative' else verify_weights(product,metadata,records,boundary))
        validation['svg'] = []
        validation['svg_serialization'] = {}
        assets = {}
        shutil.copy2(accounting,output/accounting.name)
        assets[accounting.name] = digest(accounting)
        for record in records:
            for variant in record['variants']:
                if variant['status'] != 'rendered': continue
                source = work/'tmp'/variant['file']
                target = output/source.name
                validation['svg_serialization'][target.name] = compact_native_svg(source,target)
                checked = validate_country_map(target,record,variant)
                validation['svg'].append(checked)
                assets[target.name] = digest(target)
                width,height = record['page']
                for edge,suffix in ((2112,''),(3840,'-4k')):
                    png = work/f'{source.stem}{suffix}.png'
                    rasterize(target,png,round(edge*width/max(width,height)))
                    webp = output/f'{source.stem}{suffix}.webp'
                    subprocess.run(['magick',str(png),'-quality','90',str(webp)],check=True)
                    size = subprocess.check_output(['magick','identify','-format','%w %h',str(webp)],text=True)
                    if max(map(int,size.split())) != edge: raise ValueError('incorrect raster dimensions')
                    assets[webp.name] = digest(webp)
            record['receipt_file'] = f"{key}-data-country-{record['country'].lower()}.json"
            write_json(output/record['receipt_file'],record)
            assets[record['receipt_file']] = digest(output/record['receipt_file'])
        manifest = {'schema':'alpha60-country-cartography/1','collection':key,'countries':records,
                    'validation':validation,'assets':assets,
                    'source':{**source_identity, 'boundary_sha256':digest(boundary),'registry_sha256':digest(registry),
                              'renderer_sha256':digest(binary)},
                    'source_files':{str(p.relative_to(root)):digest(p) for p in
                                    [root/'src/a60-svg-cumulative-country.h',root/'src/a60-carto-geo.cc',
                                     root/'src/a60-svg-collection.h',root/'src/a60-btiha-geojson.h']}}
        for repo in ('izzi','cartofreako'):
            manifest['source'][repo+'_commit'] = subprocess.check_output(['git','-C',str(root.parent/repo),'rev-parse','HEAD'],text=True).strip()
        dest = output/f'{key}-country-map-manifest.json';write_json(dest,manifest)
    return dest
